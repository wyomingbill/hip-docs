# Chatterbox TTS (Resemble AI, MIT) -- Apple Silicon Evaluation
Status: BUILT
Reconciled-Against: measured on the Mini (arm64, 32GB, macOS 26.3) 2026-07-14 22:37-23:05 MT; chatterbox-tts 0.1.7, torch 2.13.0, Python 3.14.4
Companion script: chatterbox_eval__v20260714_2310.py (this directory)
Eval environment: ~/chatterbox-eval on the Mini -- fully isolated venv; hip-dev untouched; demo remains on GPT Live

---

## Verdict (one paragraph)

Chatterbox runs end-to-end on Apple Silicon via MPS -- default 0.5B, Turbo,
zero-shot cloning, and the exaggeration parameter all work, the air-gap
claim is CONFIRMED (generates with HF offline mode forced, zero outbound
connections observed), and the PerTh watermark is CONFIRMED present
(detector score 1.0 on every sample, no API off-switch). But it is **not
real-time on Mini-class hardware**: warm steady-state RTF is ~1.27 (4.4 s
of compute for 3.5 s of audio) and the 0.1.7 API is non-streaming, so
utterance latency equals full generation time -- 4-12 s per reply. That
disqualifies it as the LIVE assistant voice on a Mini, and cleanly
qualifies it for the **voice-preservation / legacy tier** (offline batch
generation, RTF irrelevant, MIT license, in-boundary, no vendor
negotiation) and as a **production candidate for operator-cloud GPU
hardware**, where CUDA + streaming is the configuration Resemble's
sub-200 ms Turbo claims actually describe. The in-boundary licensing hole
is closed; the performance question moves to operator-grade GPUs.

---

## 1. Install

| Item | Measured |
|---|---|
| Package | chatterbox-tts 0.1.7 (PyPI), fresh venv on Homebrew Python 3.14.4 |
| Dependency footprint | 1.5 GB venv (torch 2.13.0 arm64, transformers, diffusers, librosa, s3tokenizer, resemble-perth) |
| Model weights | 7.7 GB HF cache total (0.5B + Turbo + tokenizers/watermarker) |
| Install wall-clock | Not cleanly measured -- the first detached launch lost its timing wrapper (see §6); packages completed in background; re-verification pass confirmed all requirements satisfied in 3 s |

Three environment fixes were required to run at all -- all upstream
issues, none Chatterbox-model problems:

1. **`nohup ... &` over ssh fails on macOS** ("can't detach from console")
   -- launch detached work as `( cmd </dev/null >log 2>&1 & )`.
2. **perth watermarker silently degrades on modern Python:** resemble-perth
   imports `pkg_resources`, removed in setuptools >=81; perth's guard sets
   `PerthImplicitWatermarker = None` and Chatterbox then crashes with
   `TypeError: 'NoneType' object is not callable`. Fix: `pip install
   "setuptools<81"`. (Plain `setuptools` is NOT enough -- >=81 no longer
   ships pkg_resources.)
3. **torchaudio 2.13 dropped built-in save** (wants torchcodec + FFmpeg).
   The eval script writes WAVs with stdlib `wave` instead.

On Apple Silicon the standard `torch.load` monkeypatch
(`map_location=mps`) is required because checkpoints reference CUDA
storage. With it, `from_pretrained(device="mps")` works first try.

## 2. Performance (MPS, Mini: M-series, 32 GB)

| Measurement | Result |
|---|---|
| Device | **MPS** (no CPU fallback needed) |
| Model load (0.5B) | 13.1 s |
| Cold generation, 7.4 s utterance | 12.2 s (RTF 1.65) |
| **Warm steady-state (offline test, 2nd run)** | **RTF 1.27** (4.4 s for 3.5 s audio) |
| Time-to-first-audio | = full generation time; **0.1.7 has no streaming API** |
| Peak RSS | 5.0 GB (0.5B) / 6.8 GB (with Turbo loaded) -- comfortable in 32 GB |
| Token sampling rate | ~29-35 it/s on MPS |

**Turbo (350M):** available in 0.1.7 and runs (load 77 s including weight
download; single cold generation RTF 2.62 -- worse than the 0.5B in this
one measurement, which includes first-inference warmup). The sub-200 ms
claim is a CUDA + streaming figure; nothing resembling it is reachable on
MPS with the non-streaming 0.1.7 API. Turbo on MPS was not faster in the
only comparable measurement taken; a warm A/B was not run.

**Cloned generation:** RTF 10.0 on the first clone call -- this includes
one-time reference conditioning (voice embedding), cacheable per voice.
Still far from real-time.

**Exaggeration sweep:** parameter works (0.25 / 0.5 / 1.0 / 1.8 all
generated); note exaggeration=0.25 tripled generation time (RTF 5.7) in
this run -- low-exaggeration sampling appears to run longer.

## 3. Zero-Shot Clone -- honest assessment

The reference was synthesized with macOS `say -v Daniel` (British male,
~20 s) because no natural speech WAV exists on the box. The clone
generated successfully from it. **Subjective speaker-fidelity judgment
requires ears I don't have -- Bill must listen** (command below). Two
honest caveats: (a) cloning a concatenative synthetic voice is a WEAKER
test than cloning a real human -- Chatterbox's blind-test results were on
natural speech; (b) if `03_cloned_voice.wav` sounds like generic TTS
rather than recognizably "Daniel," rerun with a real human reference
before concluding anything -- the eval script takes any wav:
`venv/bin/python chatterbox_eval.py clone` after replacing
`samples/reference.wav`.

## 4. The two claims that matter -- CONFIRMED

**(a) Air-gap / zero outbound: CONFIRMED.** With `HF_HUB_OFFLINE=1` and
`TRANSFORMERS_OFFLINE=1` forced, the model loads from cache and generates
normally; `lsof` sampling of the process during generation showed **zero
established non-localhost TCP connections**. During the initial ONLINE
run, the only observed endpoints were Hugging Face CDN (CloudFront/AWS)
serving the weight downloads -- no telemetry endpoints, no license
server. After weights are cached, the network is not needed and not used.

**(b) PerTh watermark: PRESENT, ON BY DEFAULT, NO API OFF-SWITCH.** The
perth detector returns score **1.0** on both the default-voice and cloned
samples. `ChatterboxTTS.generate()` exposes no watermark parameter
(signature: repetition_penalty, min_p, top_p, audio_prompt_path,
exaggeration, cfg_weight, temperature), and the watermarker is
constructed unconditionally in `ChatterboxTTS.__init__`. Strictly,
"non-removable" is false -- the package is MIT and one source edit
removes it -- but as shipped, every output is watermarked and detectable
with the open perth package. For HIP this is arguably a FEATURE:
provable AI-provenance on generated household audio.

## 5. Viability for HIP

| Use | Verdict |
|---|---|
| Live assistant TTS on Mini-class edge | **NO** -- warm RTF ~1.3, no streaming; 4-12 s replies |
| Live assistant TTS on operator-cloud GPU | **CANDIDATE** -- MIT, in-boundary, air-gapped; CUDA + streaming (Turbo) is the configuration the sub-200 ms claim describes. Needs a CUDA-hardware test before relying on it |
| Voice-preservation / legacy premium tier | **YES, TODAY** -- batch generation is RTF-insensitive; MIT closes the licensing gap Cartesia left (voice cloning NOT self-hostable per OQ-3); zero vendor negotiation |
| Vendor-negotiation leverage | Real: a credible MIT self-host TTS with cloning strengthens HIP's position in the Deepgram/Cartesia OEM conversations |

The voice memo's fallback stack ("Whisper + Kokoro") gains a third leg:
Chatterbox for cloning/legacy. The governed-core live-TTS decision is
unchanged pending an operator-GPU test.

## 6. Play the samples (Bill)

```bash
for f in ~/chatterbox-eval/samples/*.wav; do echo "== $f"; afplay "$f"; done
```

Listen order: `01_default_voice.wav` (baseline), `reference.wav` (the
Daniel reference), `03_cloned_voice.wav` (judge: recognizably Daniel, or
just "a voice"?), `04_emotion_ex0_25.wav` vs `04_emotion_ex1_8.wav`
(exaggeration range on the fall-alert line).

Everything lives in `~/chatterbox-eval/` (venv, weights cache in
`~/.cache/huggingface`, samples, results.json, eval.log). Nothing touches
hip-dev. Delete the whole directory + HF cache to reclaim ~9 GB.

## 7. Ops note for the record

The first install attempt appeared dead (no log, 13 MB venv) because
`nohup ... &` over ssh dies on macOS without stdin redirected; the pip
process actually survived long enough to complete later, which is why the
relaunch found everything satisfied but timing was lost. The working
detach pattern for all subsequent long ops:
`( script.sh </dev/null >log 2>&1 & )` -- double-fork subshell, all three
streams redirected, state and exit codes written to files so an ssh drop
loses nothing.
