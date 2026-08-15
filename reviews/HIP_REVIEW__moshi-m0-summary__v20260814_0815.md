# HIP_REVIEW — Moshi lab, M0 and drift: summary

Status: BANKED
Verification: UNVERIFIED
Reconciled-Against: the two findings docs cited below, banked in the same commit, 2026-08-14 (Voice 42). Reconciled against no code, no graph and no harness run.
Source: cover note written by Voice 42 over research-mode findings produced in `~/moshi-lab`.

**THIS NOTE CLAIMS NOTHING BEYOND THE TWO DOCUMENTS IT CITES.** It is a reading aid, not new
evidence and not a ruling. Both sources are **research mode** under
`HIP_PROCESS__moshi-research-lane-method__v20260813_1500.md` — no REQ, no MET ruling, no harness
run — and their findings are **UNVERIFIED** until a separate dispatch confirms them.

| source | verdict |
|---|---|
| `HIP_REVIEW__moshi-m0-findings__v20260814_0815.md` (lab `FINDINGS__m0__v20260813.md`, ML-01 / Voice 38) | **PASS** |
| `HIP_REVIEW__moshi-drift-findings__v20260814_0815.md` (lab `FINDINGS__drift__v20260814.md`, ML-02 / Voice 39) | **STATE-ARTIFACT** |

---

## What M0 asked and what came back

M0 tested whether Moshi (`kyutai/moshiko-mlx-q4`, 7B, 4-bit, on an M1 Pro) could serve as HIP's
duplex voice layer. Four questions.

**The verdict was PROVISIONAL-PASS PENDING Q2 MIC and was resolved to PASS on 2026-08-14 by Bill's
live microphone test.** Q2 was the one question no amount of measurement could answer without a
human at a microphone.

- **Q1 — compute.** Per-frame cost rises while the attention cache fills, then goes **flat at
  RTF 0.684**. The server runs the Mimi codec and the language model as two OS processes, so the
  pipeline is rate-limited by the slower stage rather than their sum — **RTF 0.684 at steady state
  on both stages**. The model does not progressively fall behind real time.
- **Q2 — duplex, at the microphone.** Bill's words: *"not walkie talkie"*, and *"good at finding
  the semantic end point of my speech"*. Content quality was bad, which Q2 does not grade — a base
  model that turn-takes well and answers poorly is the dual-model premise working, with the larger
  model behind it.
- **Q3 — pre-emission access to the text.** Yes, and stronger than "text arrives first": the audio
  for a frame is generated **from** that frame's text token, so the text is causally upstream of
  the audio an act gate would withhold.
- **Q4 — suppress audio while state continues.** Yes. Audio was withheld while the model's own
  state advanced through the refusal.

## The constraint M0 found

**A hard ceiling at 4096 frames = 5 min 28 s, in BOTH directions of the Mimi codec** — the same
component encodes the microphone and decodes the model's voice, and one shared instance serves
both, so both ends fail together. **The symptom is silence, not an error.** Recovery is to discard
and rebuild the codec: **~0.61 s**, during which streaming state is lost.

**Ruled by Bill, 2026-08-13: ACCEPTED for the research lane as a KNOWN PRODUCT CONSTRAINT.**
Periodic rotation with that gap is the M0/M1 workaround. It is **not** discharged for the product —
a product claim resting on a conversation surviving past 5.5 minutes needs a real engineering
answer (seamless or overlapping rotation), not this gap.

## What the drift measurement settled

M0 left one open question: Bill's response onset drifted over his session — fast early, near
barge-in later — while endpointing stayed good. Three candidates: a tunable parameter, a KV/state
artifact, or co-tenancy.

**Verdict: STATE-ARTIFACT at frame 4096.** With input held byte-identical across a cyclic stimulus,
the model's leaning toward speech **steps up sharply exactly where the KV cache fills and begins
rotating**, in the direction Bill reported. Sessions that never reach 4096 show no step; those that
cross it do. **Not tunable** — the measure is read before the sampler, and a lower-temperature arm
reproduces the step. **Not co-tenancy** — an induced-load arm reproduced it while demonstrably
slowing execution, which is what "load changes speed, not arithmetic" predicts. **Not the codec** —
those runs contained no codec at all, which separates a confound M0 had recorded as inseparable by
observation.

## The two constraints M1 inherits

1. **The 5 min 28 s codec ceiling.** Any M1 experiment running longer than that must rotate the
   tokenizer **and say so in its own findings** — a rotation absorbed silently leaves a reader
   looking at a clean long conversation that never happened.
2. **The behavioural step at 4096 is not a calibration task.** It is tied to the attention cache
   reaching capacity and beginning to evict. No sampler parameter reaches it; any mitigation is
   architectural. Both constraints land at the same frame count, for unrelated reasons.

## Limits, carried from the sources rather than smoothed over

- The drift result measures a **decision variable, not onset latency in milliseconds**; the link to
  "it cut me off" is an inference from direction and magnitude.
- Its stimulus is a synthetic loop, not a conversation; the finding is the **step under identical
  input**, not the absolute values.
- The co-tenancy arm was **weak** (~7% slowdown); the structural argument carries that exclusion.
- **No live full-pipeline session under real co-tenancy has ever been measured.** Both sources name
  this as the gap most likely to surprise someone later.
