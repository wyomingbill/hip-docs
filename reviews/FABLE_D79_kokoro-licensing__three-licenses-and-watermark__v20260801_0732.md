# FABLE_D79_kokoro-licensing — three licenses, watermark, and third-party serving

Reviewer: Fable
Dispatch: D-79
Subject: the licenses governing the shipped TTS stack, established separately for the
`kokoro-onnx` package, the model weights (`kokoro-v1.0.onnx`), and the voice packs
(`voices-v1.0.bin`); whether generated audio may be served to third parties; attribution;
and whether any watermark exists or can be disabled.
Method: read-only in `~/hip-vo`, with local filesystem evidence (installed dist-info,
model headers, archive members) plus web confirmation for the upstream model license.
Version: v20260801_0732 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED
Verification: local evidence VERIFIED in-place; upstream license claims from published
sources, cited inline.
Date: 2026-08-01

**This is the evidence for `REQ_DEMO_WEB_REPLAY` R1**, banked under D-80 because it had
been left in `/tmp` — outside the repo's provenance record. Same gap D-60 closed for
research pass 3 and D-77 closed for the D-70 survey.

Findings are the reviewer's. The local half (MIT LICENSE file, absence of watermark code,
archive contents, ONNX header) was verified in place and is reproducible from the paths
cited. The upstream half (Apache 2.0 on the weights and voices) rests on published
sources, not on anything shipped with the bytes on this machine — the report says so
explicitly, and that distinction is the point.

---

# D-79 — Kokoro licensing check

Read-only in `~/hip-vo` (bill-ai / [REDACTED-MACHINE-NAME]). Nothing changed, no lock taken.
Tree clean before and after.

**Bottom line: yes, generated audio can be served to third parties. No watermark. Attribution is not legally required for audio-only distribution, but is required if the model or package is redistributed — and is cheap enough to do anyway.** Two caveats worth reading before this is treated as settled, at the end.

---

## The three licenses — they are NOT the same, and only one is stated in the artifact itself

| # | Artifact | License | How established |
|---|---|---|---|
| 1 | `kokoro-onnx` package v0.4.7 | **MIT** | **Verified locally** — actual LICENSE file |
| 2 | Model weights `kokoro-v1.0.onnx` | **Apache 2.0** | Upstream README (bundled in METADATA locally) + confirmed on hexgrad/Kokoro-82M |
| 3 | Voice packs `voices-v1.0.bin` | **Apache 2.0**, as part of Kokoro-82M — *not separately licensed* | Inferred, see below |

### 1. `kokoro-onnx` package — MIT, verified locally

`.venv/lib/python3.14/site-packages/kokoro_onnx-0.4.7.dist-info/licenses/LICENSE`:

```
MIT License
Copyright (c) 2025 github.com/thewh1teagle
```

Installed in `~/hip-harness/.venv` and `~/hip-dev/.venv` (v0.4.7 in both). Note the package METADATA carries **no `License:` field and no license classifier** — which is why my D-78 recon could not resolve it from metadata alone. The LICENSE file is present but only under `dist-info/licenses/`.

**This covers the wrapper code only** — roughly 200 lines of ONNX-runtime plumbing. It does not reach the weights.

### 2. Model weights — Apache 2.0

The upstream README, bundled verbatim in the local METADATA, states it plainly:

```
## License
- kokoro-onnx: MIT
- kokoro model: Apache 2.0
```

Confirmed against the source repo (hexgrad/Kokoro-82M): Apache 2.0, explicitly permitting commercial use.

**Not verifiable from the file itself.** I read the ONNX header directly: producer is `pytorch 2.6.0`, and there is **no embedded license, doc_string, or NOTICE** in the model. There is also **no LICENSE file beside either artifact** in `~/hip-harness/models/`. So the license is established by upstream publication, not by anything shipped with the bytes on this machine.

### 3. Voice packs — the one that was genuinely open, now resolved

`voices-v1.0.bin` is not an opaque blob. It is a **zip of 54 NumPy arrays**, one per voice — e.g. `af_alloy.npy`, `float32`, shape `(510, 1, 256)`: per-voice style embeddings, not audio samples.

**There is no LICENSE, NOTICE, or README member inside the archive.** I checked; the archive contains `.npy` files and nothing else.

The count is the evidence: **54 voice packs locally, and Kokoro-82M publishes exactly 54 voices** across 8 languages (11 af / 9 am / 4 bf / 4 bm, plus Japanese, Mandarin, Spanish, French, Hindi, Italian, Brazilian Portuguese). Local prefix breakdown matches. So the voice packs are the Kokoro-82M voice set, covered by that repo's Apache 2.0 license. They are **not carved out or separately licensed** — no separate license exists to find.

**Configured voice in this deployment:** `af_heart` (`config.yaml` — American female, speed 1.0, 24 kHz).

---

## The answers

### Can generated audio be served to third parties?

**Yes.** Apache 2.0 grants a perpetual, worldwide, royalty-free license to use, reproduce, and distribute the work and derivative works, with **no field-of-use restriction and no clause governing model output**. Nothing in Apache 2.0 or MIT restricts what you do with generated audio, and neither license claims ownership of output. Commercial use is explicitly fine.

For the replay demo specifically (D-78 v1): serving pre-generated per-turn WAV/Opus files to a gated remote viewer is **unrestricted by these licenses**.

### Is attribution required?

**Two different answers, and the distinction matters:**

- **Serving generated audio only — no.** Audio output is not a derivative work of the licensed code or weights. Apache 2.0 §4's attribution obligations attach to distributing *the Work or Derivative Works*, not to distributing model output. Nothing legally requires a credit line on the audio.
- **Redistributing the model or package — yes.** If `kokoro-v1.0.onnx`, `voices-v1.0.bin`, or the `kokoro-onnx` source ever ship inside a deliverable, Apache 2.0 §4 requires retaining copyright notice, license text, and any NOTICE file; MIT requires retaining its copyright and permission notice.

**Recommendation:** credit anyway — "Speech synthesized with Kokoro-82M (Apache 2.0)" — in the demo's colophon. It costs nothing, it is accurate, and it pre-empts the question in a diligence setting where the audio's provenance will be asked about.

### Is there a watermark, and can it be disabled?

**No watermark. Verified two independent ways:**

1. **Locally** — grepped the entire installed `kokoro_onnx` package source for `watermark`, `perth`, `resemble`. **Zero matches.** The synthesis path is `Kokoro.create()` → float32 array, with no post-processing stage where a watermark could be applied.
2. **Upstream** — no documented watermarking for Kokoro-82M.

The "can it be disabled" half is therefore moot: there is nothing to disable.

**This is a meaningful contrast the project has already been through.** The Chatterbox TTS evaluation (`hip-vo/docs/INDEX.md:212`, 2026-07-14) **CONFIRMED a PerTh watermark, score 1.0, with no API off-switch** — and that finding was recorded as a real constraint. Kokoro has no equivalent. On the watermark axis specifically, the engine already shipping is the cleaner of the two evaluated.

---

## Two caveats — neither blocks the demo, both should be on the record

**1. The dependency chain is GPL, even though the package is MIT.** `kokoro-onnx` requires `phonemizer-fork==3.3.1`, which is **GPLv3+** (verified locally: classifier `License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)`), and `espeakng-loader` (espeak-ng itself is GPLv3; the loader ships no license metadata locally).

This **does not affect serving generated audio** — GPL governs distribution of *software*, and audio output is not a derivative work of the phonemizer. It **would** matter if HIP ever distributes the synthesis stack as part of a product, where GPLv3 obligations would attach to that distribution. Naming it now because "the TTS is MIT" is the natural shorthand and it is incomplete.

**2. Upstream training-data provenance is permissive-by-claim, and one category is worth knowing.** Kokoro-82M was trained on permissive/non-copyrighted audio: public domain, Apache/MIT-licensed audio, **and synthetic audio generated by closed TTS models from large providers**.

That last category is an upstream risk carried by hexgrad, not by HIP, and Apache 2.0 does not indemnify it. Some closed TTS providers' terms restrict using their output to train competing models. This is a well-known open question about Kokoro's lineage rather than a defect discovered here — but if the audio ever features in a diligence conversation, that is the question that gets asked, and "Apache 2.0" is not a complete answer to it.

---

## Verdict for D-78's cut line

The licensing item I flagged as gating v1 is **cleared for the replay demo**. Serving pre-generated Kokoro audio to gated third parties is permitted, unwatermarked, and needs no attribution — though attribution is recommended. The residual items (GPL dependency chain on stack *distribution*; upstream training-data provenance) do not gate a replay demo and should be recorded rather than resolved here.

Nothing banked, nothing changed.

## Sources

- [hexgrad/Kokoro-82M · Hugging Face](https://huggingface.co/hexgrad/Kokoro-82M)
- [README.md · hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/README.md)
- [VOICES.md · hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)
- [hexgrad/Kokoro-82M voices directory](https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices)
- [GitHub - hexgrad/kokoro](https://github.com/hexgrad/kokoro)
- [Kokoro-82M TTS API | Together AI](https://www.together.ai/models/kokoro-82m)
- [Kokoro TTS Review | VisionStory](https://www.visionstory.ai/open-source/kokoro-tts)
- [Kokoro-82M on Replicate](https://replicate.com/jaaari/kokoro-82m)

Local evidence (not a web source): `kokoro_onnx-0.4.7.dist-info/licenses/LICENSE` and `METADATA` in `~/hip-harness/.venv`; `~/hip-harness/models/kokoro-v1.0.onnx` and `voices-v1.0.bin`; `~/hip-vo/config.yaml`.
