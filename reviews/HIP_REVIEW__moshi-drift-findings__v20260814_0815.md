# HIP_REVIEW — Moshi response-onset drift findings (lab, banked verbatim)

Status: BANKED
Verification: UNVERIFIED
Reconciled-Against: banked VERBATIM from `[REDACTED-USER-PATH]/moshi-lab/FINDINGS__drift__v20260814.md` at repo HEAD `fc5e8a7`, 2026-08-14 (Voice 42). Reconciled against no code, no graph and no harness run.
Source: `[REDACTED-USER-PATH]/moshi-lab/FINDINGS__drift__v20260814.md` — Moshi research lane, RESEARCH MODE, lab identity **ML-02**, dispatch **Voice 39**.
Stage verdict: **STATE-ARTIFACT**

**RESEARCH-MODE FINDINGS. NOT GOVERNED EVIDENCE. THIS DOCUMENT MARKS NOTHING MET.**
Produced under `HIP_PROCESS__moshi-research-lane-method__v20260813_1500.md`, which runs the
research lane deliberately WITHOUT the standard process — no REQ doc, no MET ruling, no harness
run, no lock. Per the `docs/reviews/` rule, a review doc records what its author CLAIMED and its
findings are **UNVERIFIED until a separate dispatch confirms them**. Nothing here is a HIP
requirement or a decision.

**WHY IT IS IN THE REPO AT ALL.** The lane method §3 makes findings docs the ONLY artifacts that
cross from `~/moshi-lab` into a HIP tree, and they cross by a normal docs dispatch. `~/moshi-lab`
is not version controlled, so until this commit these results existed in exactly one place on one
disk. **No lab code crossed.** Graduation of anything here means re-implementation through the
governed process with its own REQ and evidence.

**The body below is VERBATIM and unedited; its own first line is the stage verdict.**

---

STATE-ARTIFACT

# RESPONSE-ONSET DRIFT — FINDINGS
Lane: Moshi research lane, research mode. Lab identity **ML-02**. Dispatch **Voice 39**. **Not M1.**
Authority: `HIP_PROCESS__moshi-research-lane-method__v20260813_1500.md`.
Purpose: settle M0's top open question — is the response-onset drift Bill observed at the
microphone (fast early, near-barge-in late) a tunable parameter, a KV/state artifact, or co-tenancy?
Machine: MacBook Pro, M1 Pro, 10 cores, 32 GB. Lab venv 3.12.14, `moshi_mlx` 0.3.0, `mlx` 0.26.5.
Model: `kyutai/moshiko-mlx-q4`, config `models.config_v0_1()`.

**Isolation gate: PASS**, first act of the session, all assertions including the negative controls.
**Nothing here read HIP data, a HIP credential, or a HIP graph port. No microphone. No Bill.**

---

## THE VERDICT: **STATE-ARTIFACT**

**The model's leaning toward speech steps sharply upward at frame 4096 — the frame at which the
attention cache fills and begins rotating — with the input held byte-identical.** It is not a
sampler parameter and it is not machine load. **It cannot be calibrated away.**

| session | frames | reaches 4096? | leaning before 4096 | after 4096 | step |
|---|---|---|---|---|---|
| 3 min | 2250 | **no** | −18.03, −18.78 (stable) | — | **none — no boundary to cross** |
| 6 min | 4500 | yes | **−18.60** (spread 0.37) | **−15.63** | **+2.96 = 8.1x the spread** |
| 9 min | 6750 | yes | **−17.98** (spread 0.48) | **−15.89** | **+2.09 = 4.4x the spread** |

**The direction is the one Bill reported.** Higher margin = closer to speaking = more likely to come
in over the top of someone. The model becomes measurably more eager once the cache starts rotating.

**It is a STEP TO A NEW LEVEL, not a runaway drift.** In the 9-minute session the two cycles that
lie entirely past the boundary read **−15.14 and −15.17** — indistinguishable from each other. The
model does not keep getting more eager; it moves once and settles.

---

## 1. WHY THE ANSWER IS TRUSTWORTHY: THE INPUT IS BYTE-IDENTICAL

The stimulus is a fixed 899-frame loop, replayed. **Frame `k` and frame `k + 899` receive exactly
the same input.** So a difference between cycles cannot come from what the model is hearing. It can
only come from internal state.

That is what makes the same-phase table decisive (9-minute session):

```
cycle 0  frames    0- 898   margin -17.19
cycle 1  frames  899-1797   margin -18.00
cycle 2  frames 1798-2696   margin -18.28
cycle 3  frames 2697-3595   margin -18.44     <- four cycles, spread 0.48
cycle 4  frames 3596-4494   margin -18.57     <- cache fills mid-cycle (frame 4096)
cycle 5  frames 4495-5393   margin -15.14     <- entirely past the boundary
cycle 6  frames 5394-6292   margin -15.17     <- and stable there
```

Identical input, four stable cycles, then a step of roughly 3 log-units that holds.

---

## 2. THE TWO RIVAL HYPOTHESES ARE EXCLUDED — BY CONSTRUCTION, THEN BY EXPERIMENT

**The metric is the logit margin**, `logit(best real word) − logit(<pad>)`, read from the raw text
logits inside the sampler. Two properties of *where* it is read do most of the work:

- **CO-TENANCY cannot produce it.** Machine load changes how fast arithmetic executes, not what it
  computes. The margin is a function of weights, cache and input — all deterministic. A busy machine
  cannot move a logit.
- **TUNABLE cannot produce it.** The margin is read **before** the sampler applies temperature,
  top-p or any threshold. Sampler parameters cannot move it either.

Those are structural arguments, so both were also tested rather than merely asserted:

| control | result |
|---|---|
| **temp 0.3** (vs 0.8), 6 min | step **+2.66** — survives. Not tunable (§5) |
| **induced CPU load**, 6 min | step **+2.51** — survives, while step_ms rose 50.7 -> 54.3. Not co-tenancy (§5) |

---

## 3. A CONFOUND M0 CALLED INSEPARABLE, SEPARATED

M0 recorded that the KV cache boundary and the Mimi codec wall **both** land at frame 4096 — two
unrelated 4096s (`max_seq_len` in the model config; an 8192-row buffer at 2 rows/frame in a Rust
crate that never reads that config) — and concluded that *"the two causes are not separable by
observation alone."*

**These runs contain no codec at all.** The stimulus is pre-encoded once and replayed, so
`StreamTokenizer` is never in the measurement loop and never reaches its wall. **The step at 4096
happens anyway.** So the behavioural change belongs to the attention cache, not to the codec. That
confound is now closed.

---

## 4. THE METRIC HAD TO BE REBUILT TWICE, AND BOTH REBUILDS WERE NECESSARY

Recorded because the first two designs would each have produced a confident wrong answer.

**Attempt 1 — constant silence.** Fed digital silence every frame. Moshi produced a short greeting
and then went permanently quiet: **P(speak) pinned at exactly 0.0000 from ~frame 500 onward**. A
metric sitting on its floor cannot detect an upward drift. Reporting "no drift found" from that run
would have been a false negative from a measurement structurally incapable of returning the answer —
the same failure family that cost M0 two false results. **Stopped and rebuilt.**

**Attempt 2 — speech stimulus, probability metric.** Replaying Moshi's own speech lifted P(speak)
about tenfold, but it still saturated at 0.0000 within a couple of thousand frames. **P = 1e-8 and
P = 1e-5 both print as 0.0000 while differing by three log units** — exactly the range a drift lives
in. **Stopped and rebuilt.**

**Attempt 3 — the logit margin.** Unbounded, never saturates, and resolves the model's leaning long
after the probability has rounded away. Standard deviation ~5 across every session: real dynamic
range. **This is the metric of record; P(speak) is reported alongside it and is only ever zeros.**

**A sensitivity gate is now built into the harness**: a run that is saturated on *both* metrics is
flagged `METRIC_SATURATED` and is forbidden from carrying a drift conclusion. No run used here was
saturated.

**One analysis bug, caught and fixed before it misled anyone.** The same-phase summary originally
compared cycle 0 to the *last* cycle. When the boundary falls mid-cycle that average mixes pre- and
post-boundary frames and dilutes the step to nothing — it printed a confident **"FLAT"** over a
**+2.96** step. It now compares cycles lying entirely before the boundary against frames entirely
after it.

---

## 5. CONTROLS — THE STEP SURVIVES BOTH

Three 6-minute runs, identical stimulus, differing only in the variable under test:

| run | pre-4096 | post-4096 | **step** | vs cycle spread | step_ms |
|---|---|---|---|---|---|
| baseline, temp 0.8 | −18.60 | −15.63 | **+2.96** | 8.1x | 50.7 |
| **TUNABLE control — temp 0.3** | −18.50 | −15.84 | **+2.66** | 8.8x | 52.9 |
| **CO-TENANCY control — induced CPU load** | −18.32 | −15.81 | **+2.51** | 11.0x | 54.3 |

**TUNABLE: ruled out.** Dropping sampler temperature from 0.8 to 0.3 changes the step by 0.3 —
inside run-to-run variation — and leaves the pre-boundary level within 0.1. The margins track each
other frame by frame (at frames 500/1000/1500: −16.88/−17.61/−19.77 at temp 0.8 versus
−16.68/−17.71/−19.56 at temp 0.3). **A sampler parameter does not touch this.**

**CO-TENANCY: ruled out.** Under induced CPU load the step is +2.51, the same effect. **The load
was real and it did slow the run** — step_ms rose from 50.7 to 54.3 ms and free memory sat lower
throughout — **yet the decision variable did not move.** That is the signature the structural
argument predicts: contention changes how fast the arithmetic runs, not its result.

> **HONEST WEAKNESS OF THE LOAD ARM.** Six CPU spinners produced only a **~7% slowdown**, well
> short of the 0.87 -> 1.37 RTF degradation M0 measured with a second 7B model on the GPU. So this
> is a **weak empirical test of co-tenancy**, and it is reported as such. The weight here sits on
> the structural argument — the margin is a deterministic function of weights, cache and input, and
> no amount of load can change a logit — with the arm as consistent corroboration rather than proof.

**FIVE RUNS, ONE RESULT.** 3 min (no boundary, no step), 6 min, 9 min, temp 0.3, loaded. Every run
that crosses 4096 shows the step; the one that does not, does not.

---

## 6. LIMITATIONS — READ BEFORE QUOTING THIS

1. **This is not a conversation.** The stimulus is a loop of Moshi's own voice, which is
   out-of-distribution. The *absolute* margin values mean nothing conversational. The finding is
   the **step at a specific frame under identical input**, which is a comparison within the run and
   does not depend on the stimulus being realistic.
2. **This measures a decision variable, not onset latency in seconds.** It shows the model's leaning
   toward speech moves sharply at 4096 and in the direction Bill reported. **It does not measure how
   many milliseconds earlier it starts talking.** The link to "it cut me off" is an inference from
   direction and magnitude, not a timing measurement.
3. **It does not prove co-tenancy was absent from Bill's session.** His run had `ollama` resident at
   ~12% free memory, and M0 measured contention moving this lab's RTF from 0.87 to 1.37–1.45.
   **A state mechanism is demonstrated; it is not established as the only thing he felt.**
4. **The changepoint detector is not the instrument.** In the 6-minute session it located frame
   4225; in the 9-minute session it located frame 250 — the initial greeting transient, which is the
   single largest shift in that run. Both are real features. **The cycle-based same-phase test is
   the robust instrument** and it shows the boundary step in both.
5. **One model, one config, one machine.** `config_v0_1`, `max_seq_len` 4096.

---

## 7. WHAT THIS MEANS

**For M1: stop treating this as a calibration task.** Bill's instinct — *"need some calibration
there"* — was the cheapest hypothesis and it is the one the evidence rules out. The onset change is
tied to the attention cache reaching capacity and beginning to evict. **No sampler parameter reaches
it.**

**For the product:** this is a second thing that happens at 5 min 28 s, alongside the codec ceiling
M0 found and Bill ruled on. **A session that runs past 4096 frames is a session where the model's
turn-taking behaviour changes.** Any mitigation is architectural — how context is retained, evicted
or re-seeded — not a knob.

**A cheap next experiment, if M1 wants the mechanism rather than the fact:** the step should move
with `max_seq_len`. Rebuild the cache at a different size and the boundary should move with it. That
would convert "it happens at 4096" into "it happens when the cache rotates", which is the claim
worth having.

---

## 8. EVIDENCE INVENTORY

| file | what it is |
|---|---|
| `drift_3min__ML02.json` | 3 min, speech stimulus, margin metric — **never reaches 4096, no step** |
| `drift_6min__ML02.json` | 6 min — **step +2.96 at the boundary** |
| `drift_9min__ML02.json` | 9 min — **step +2.09**, and two post-boundary cycles stable at −15.14 / −15.17 |
| `drift_6min_TEMP03__ML02.json` | TUNABLE control, temp 0.3 — **step +2.66, survives** |
| `drift_6min_LOADED__ML02.json` | CO-TENANCY control, induced CPU load — **step +2.51, survives** |
| `stimulus__ML02.npy` | the 899-frame speech loop (Moshi's own `" Hi. How I help you?"`), 20–34 distinct codes per book |
| `drift_measure__ML02.py` | harness: cache cap, margin probe, self-check, saturation gate, load watcher |
| `analyze_drift__ML02.py` | analysis: buckets, changepoint, same-phase cycle test |
| `make_stimulus__ML02.py` | stimulus builder |
| `cotenancy_load__ML02.sh` | the induced-load generator |

**SUPERSEDED, kept deliberately so the two dead ends are visible rather than tidied away:**

| file | why it is not evidence |
|---|---|
| `drift_3min_SILENCE__ML02.json` | constant-silence attempt. **P(speak) pinned at 0.0000 from ~frame 500** — the floor effect that forced the stimulus rebuild |
| `drift_3min_SPEECH_SUPERSEDED_no-margin__ML02.json` | speech stimulus but probability metric only, before the logit margin existed. Saturated the same way |

**Machine load is recorded inside every result file** (`load_samples`), per the lab rule M0 wrote
and then failed to wire in. This session wired it in.
