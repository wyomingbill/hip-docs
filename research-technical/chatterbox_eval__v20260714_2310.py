#!/usr/bin/env python
"""Chatterbox TTS evaluation on Apple Silicon (HIP research, isolated).

Runs in ~/chatterbox-eval/venv -- NOT hip-dev. Produces samples/ wavs and
results.json with timings. Stages, each independently fail-safe:

  1. device probe (MPS -> CPU) with the Apple Silicon torch.load patch
  2. default-voice generation (timed: load, first-audio, RTF, peak RSS)
  3. Chatterbox Turbo (if the package exposes it)
  4. zero-shot clone from reference.wav (synthesized via macOS `say`)
  5. exaggeration parameter sweep
  6. offline check: HF_HUB_OFFLINE=1 re-generation (set by wrapper) +
     lsof outbound-connection sampling during generation
  7. PerTh watermark: detect on our own output via the perth package

Usage: venv/bin/python chatterbox_eval.py [--stage all|gen|turbo|clone|emo|wm]
"""
from __future__ import annotations

import json
import pathlib
import resource
import subprocess
import sys
import time

HOME = pathlib.Path.home()
EVAL = HOME / "chatterbox-eval"
SAMPLES = EVAL / "samples"
SAMPLES.mkdir(exist_ok=True)
RESULTS = EVAL / "results.json"

results: dict = {}
if RESULTS.exists():
    try:
        results = json.loads(RESULTS.read_text())
    except Exception:
        results = {}


def save():
    RESULTS.write_text(json.dumps(results, indent=2, default=str))


def peak_rss_gb() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3)


def outbound_conns() -> list[str]:
    """Non-localhost established TCP connections of this process."""
    try:
        out = subprocess.run(
            ["lsof", "-a", "-i", "TCP", "-p", str(subprocess.os.getpid()),
             "-n", "-P"], capture_output=True, text=True, timeout=10).stdout
        conns = [ln for ln in out.splitlines()[1:]
                 if "ESTABLISHED" in ln and "127.0.0.1" not in ln
                 and "localhost" not in ln]
        return conns
    except Exception as exc:
        return [f"lsof failed: {exc!r}"]


# ── device probe + Apple Silicon patch ────────────────────────────────────────

import torch  # noqa: E402

if torch.backends.mps.is_available():
    DEVICE = "mps"
    # Chatterbox checkpoints reference CUDA storage; on Apple Silicon every
    # torch.load must be remapped. Community-standard patch:
    _orig_load = torch.load

    def _patched_load(*args, **kwargs):
        kwargs.setdefault("map_location", torch.device(DEVICE))
        return _orig_load(*args, **kwargs)

    torch.load = _patched_load
else:
    DEVICE = "cpu"

results["device"] = DEVICE
results["torch"] = torch.__version__
results["mps_available"] = torch.backends.mps.is_available()
save()
print(f"[eval] device={DEVICE} torch={torch.__version__}", flush=True)

TEXT = ("Good morning Ray. It's eight o'clock — time for your Jardiance, "
        "one tablet with breakfast. Your daughter Maya called earlier and "
        "said she'll stop by around noon.")


def timed_generate(model, text, wav_path, sr, **kwargs):
    t0 = time.perf_counter()
    wav = model.generate(text, **kwargs)
    t1 = time.perf_counter()
    import wave as _wave
    import numpy as _np
    data = wav.squeeze().cpu().numpy()
    pcm = (_np.clip(data, -1.0, 1.0) * 32767).astype(_np.int16)
    with _wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    dur = wav.shape[-1] / sr
    return {"gen_s": round(t1 - t0, 2), "audio_s": round(dur, 2),
            "rtf": round((t1 - t0) / dur, 2), "peak_rss_gb": round(peak_rss_gb(), 2),
            "conns_during": outbound_conns()}


def stage_gen():
    from chatterbox.tts import ChatterboxTTS
    t0 = time.perf_counter()
    model = ChatterboxTTS.from_pretrained(device=DEVICE)
    load_s = round(time.perf_counter() - t0, 1)
    r = timed_generate(model, TEXT, SAMPLES / "01_default_voice.wav", model.sr)
    r["model_load_s"] = load_s
    results["stage_gen_default"] = r
    save()
    print(f"[eval] default: load={load_s}s gen={r['gen_s']}s rtf={r['rtf']}", flush=True)
    return model


def stage_turbo():
    try:
        from chatterbox.tts_turbo import ChatterboxTurboTTS  # newer pkg layout
    except ImportError:
        try:
            from chatterbox.turbo import ChatterboxTurboTTS   # alt layout
        except ImportError:
            results["stage_turbo"] = {"available": False,
                                      "note": "no turbo module in installed package"}
            save()
            print("[eval] turbo: NOT in this package version", flush=True)
            return
    t0 = time.perf_counter()
    model = ChatterboxTurboTTS.from_pretrained(device=DEVICE)
    load_s = round(time.perf_counter() - t0, 1)
    r = timed_generate(model, TEXT, SAMPLES / "02_turbo_voice.wav", model.sr)
    r["model_load_s"] = load_s
    r["available"] = True
    results["stage_turbo"] = r
    save()
    print(f"[eval] turbo: load={load_s}s gen={r['gen_s']}s rtf={r['rtf']}", flush=True)


def _ensure_reference():
    ref = SAMPLES / "reference.wav"
    if ref.exists():
        return ref
    aiff = SAMPLES / "reference.aiff"
    text = ("The quick brown fox jumps over the lazy dog. I have lived in "
            "this house for forty years and I know every creak of its "
            "floors. My grandchildren visit on Sundays and we bake bread "
            "together in the old kitchen.")
    subprocess.run(["say", "-v", "Daniel", "-o", str(aiff), text], check=True)
    subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@22050",
                    str(aiff), str(ref)], check=True)
    return ref


def stage_clone(model=None):
    if model is None:
        from chatterbox.tts import ChatterboxTTS
        model = ChatterboxTTS.from_pretrained(device=DEVICE)
    ref = _ensure_reference()
    r = timed_generate(model, TEXT, SAMPLES / "03_cloned_voice.wav", model.sr,
                       audio_prompt_path=str(ref))
    results["stage_clone"] = r
    save()
    print(f"[eval] clone: gen={r['gen_s']}s rtf={r['rtf']}", flush=True)
    return model


def stage_emotion(model=None):
    if model is None:
        from chatterbox.tts import ChatterboxTTS
        model = ChatterboxTTS.from_pretrained(device=DEVICE)
    text = "Oh no — Ray, did you fall? Are you hurt? Should I call Maya right away?"
    out = {}
    for ex in (0.25, 0.5, 1.0, 1.8):
        r = timed_generate(model, text,
                           SAMPLES / f"04_emotion_ex{str(ex).replace('.','_')}.wav",
                           model.sr, exaggeration=ex)
        out[str(ex)] = {"gen_s": r["gen_s"], "rtf": r["rtf"]}
    results["stage_emotion"] = out
    save()
    print(f"[eval] emotion sweep done: {list(out)}", flush=True)


def stage_watermark():
    import numpy as np
    try:
        import perth
        import librosa
    except ImportError as exc:
        results["stage_watermark"] = {"error": f"import: {exc}"}
        save()
        return
    wm = {}
    for name in ("01_default_voice.wav", "03_cloned_voice.wav"):
        p = SAMPLES / name
        if not p.exists():
            continue
        audio, sr = librosa.load(str(p), sr=None)
        watermarker = perth.PerthImplicitWatermarker()
        score = watermarker.get_watermark(audio, sample_rate=sr)
        wm[name] = float(np.round(float(score), 4))
    # removability probe: does the public generate() API expose a disable?
    from chatterbox.tts import ChatterboxTTS
    import inspect
    sig = str(inspect.signature(ChatterboxTTS.generate))
    wm["generate_signature"] = sig
    wm["disable_flag_in_api"] = ("watermark" in sig.lower())
    results["stage_watermark"] = wm
    save()
    print(f"[eval] watermark: {wm}", flush=True)


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    import os
    results.setdefault("env", {})["HF_HUB_OFFLINE"] = os.environ.get("HF_HUB_OFFLINE")
    m = None
    if stage in ("all", "gen"):
        m = stage_gen()
    if stage in ("all", "turbo"):
        stage_turbo()
    if stage in ("all", "clone"):
        m = stage_clone(m)
    if stage in ("all", "emo"):
        stage_emotion(m)
    if stage in ("all", "wm"):
        stage_watermark()
    print("[eval] DONE", flush=True)
