# HIP_REVIEW — Moshi M0 feasibility findings (lab, banked verbatim)

Status: BANKED
Verification: UNVERIFIED
Reconciled-Against: banked VERBATIM from `[REDACTED-USER-PATH]/moshi-lab/FINDINGS__m0__v20260813.md` at repo HEAD `fc5e8a7`, 2026-08-14 (Voice 42). Reconciled against no code, no graph and no harness run.
Source: `[REDACTED-USER-PATH]/moshi-lab/FINDINGS__m0__v20260813.md` — Moshi research lane, RESEARCH MODE, lab identity **ML-01**, dispatch **Voice 38**.
Stage verdict: **PASS** (resolved 2026-08-14 by Bill's live microphone test; was PROVISIONAL-PASS PENDING Q2 MIC)

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

PASS

# M0 — MOSHI FEASIBILITY, FINDINGS
Lane: Moshi research lane, research mode. Lab identity **ML-01**. Dispatch **Voice 38**.
Authority: `HIP_PROCESS__moshi-research-lane-method__v20260813_1500.md` (read first, as instructed).
Machine: MacBook Pro, Apple M1 Pro, 10 cores (8P/2E), 32 GB, macOS 26.5.2.
Lab: `~/moshi-lab`, venv on Python 3.12.14, `moshi_mlx` 0.3.0, `mlx` 0.26.5, `rustymimi` 0.4.1.
Model: `kyutai/moshiko-mlx-q4` (7B, 4-bit), config `models.config_v0_1()` — the repo ships no
`config.json`, so the loader falls back, and every number here is against that fallback config.

**Nothing in this stage read HIP data, a HIP credential, or a HIP graph port.**

**STEP 1 was performed within this stage, by the preceding lab session, and is inherited by this
one.** `brew install python@3.12` (3.12.14 — the only interpreter present was 3.14.4, which `mlx`
ships no wheels for) and the venv at `~/moshi-lab/.venv` both timestamp **17:01**; the weights
downloaded at **17:04–17:05**. This session opened at ~17:11 and adopted all of it, as instructed.

**Download total, measured rather than asserted** (`du` over the HF cache, this session):

| blob | size | stamped |
|---|---|---|
| `model.q4.safetensors` | 4.5 GB | 17:05 |
| Mimi tokenizer | 367 MB | 17:05 |
| SentencePiece text tokenizer | 540 KB | 17:05 |
| web UI `dist.tgz` (`moshi-artifacts`) | 576 KB | 17:04 |
| **combined** | **4.9 GB** | |

**4.9 GB against the 20 GB stop condition** — approached to roughly a quarter, never threatened.
Stated because "no model download was needed" would be wrong for the stage: this session found the
weights cached, and they were cached *because M0 had already downloaded them*.

---

## THE VERDICT: **PASS** — resolved 2026-08-14

**All four questions are answered. None of them failed.**

| | question | result |
|---|---|---|
| **Q1** | compute, RTF ≤ 1 sustained 5 min | **MET, with room** — cost plateaus **flat at RTF 0.684**, both stages (§3) |
| **Q2** | duplex, live mic | **YES — "not walkie talkie"**, and semantic endpointing is **good** (§5) |
| **Q3** | pre-emission access to the text stream | **YES** — exact hook, audio causally downstream of text, 0 order violations (§1) |
| **Q4** | suppress audio while state continues | **YES** — state advanced through the refusal, words still forming mid-gate (§2) |

**This was PROVISIONAL-PASS PENDING Q2 MIC until 2026-08-14.** Q2 was the only outstanding item;
Bill ran it and it came back positive on the mechanism. The verdict is now final.

**Two things travel with the PASS. Neither blocks the lane; both are real:**

- **A KNOWN PRODUCT CONSTRAINT** — the 5 min 28 s codec ceiling, ruled ACCEPTED for research on
  2026-08-13 and explicitly **not** discharged for the product (§4).
- **THE TOP M1 OPEN QUESTION** — response-onset timing drifted over Bill's session, fast early and
  near-barge-in later. Not investigated, by instruction. Three candidate mechanisms with different
  fixes, one of which would not respond to tuning at all (§5).

**What the PASS does not claim:** content quality. The base model answers badly, Bill said so
plainly, and Q2 does not grade it. **That is the dual-model premise working, not failing** — Moshi
is the duplex voice layer; the brain goes behind it.

**The single most important new fact: the compute cost has a ceiling, and the language model sits
comfortably under it.** The per-frame cost rises while the attention cache fills, tops out around
step 3000–3500, and then **goes flat at 54.72 ms against an 80 ms budget — RTF 0.684, with 2 of 504
plateau frames over budget** (§3.3). Drift across the plateau is +0.47 ms. **Moshi does not
progressively fall behind real time.** That was the live risk this morning and it is now closed.

**Two things still qualify the pass:**

1. **~~The FULL-pipeline steady state lands on the line, RTF ~1.0.~~ SUPERSEDED WITHIN THIS
   DOCUMENT — see §3.4a. The full-pipeline steady state is RTF ≈ 0.68.** The Mimi codec is
   measured directly and is **expensive — 21.3 ms encode + 21.8 ms decode, comparable to the 7B
   model itself**. But `local_web.py:432-437` runs the codec and the LM in **two separate
   processes**, so the pipeline is rate-limited by the slower stage, not their sum:
   `max(54.72, 43.11) = 54.72 ms → RTF 0.684`. The "~1.01" reading came from composing them
   additively, which is what the *single-process measuring harness* does and what the *real server
   does not*.

   **Consequence, and it inverts an assumption this document held all day: the 5-minute run's
   0.969 is a PESSIMISTIC bound, not a flattering one** — it serialised work the architecture
   overlaps. (Reconstructed from measured parts: blocking encode 21.3 + LM 51.3 + async decode
   enqueue 7.7 = 80.3 ms vs 77.49 ms measured, within 4%.) The 887-of-3750 frames over budget
   belong to that serialised harness too.

   **The codec is still where to look if compute ever binds** — 43 ms against the LM's 54.7 —
   and two-thirds of it is the encoder, the same component carrying the §4 wall. **But it is not
   currently binding, and the qualification that stands is narrower than it looks:** the overlap
   is only free when cores are spare, and §6 measured this machine failing that test.
2. **A hard ~5.5-minute ceiling exists in BOTH directions of the audio codec**, unknown before
   today, whose symptom is silence rather than an error (§4). **RULED BY BILL 2026-08-13: ACCEPTED
   for the research lane as a KNOWN PRODUCT CONSTRAINT** — periodic tokenizer rotation with the
   ~0.61 s gap is the M0/M1 workaround. **It does not clear the constraint for the product**: any
   later product claim needs a real engineering answer (seamless or overlapping rotation), not this
   gap. So it no longer blocks the lane, and it is not discharged either.

**PARK-COMPUTE, PARK-CONTROL and FAIL-VALUE are all off the table, and each for a measured reason:**

- **not PARK-COMPUTE** — RTF 0.684 at steady state, flat, on both stages.
- **not PARK-CONTROL** — Q3 and Q4 passed on executed evidence, not inspection.
- **not FAIL-VALUE** — the duplex behaviour Bill went to the microphone to test is present and the
  semantic endpointing is good. **Bad answers from a 7B base model are not a value failure**; they
  are the reason the design puts a larger model behind it.

**The one live caution, carried from §5:** Bill's session ran under co-tenancy with `ollama`
resident and ~12% free memory, and §6 measured this lab's own RTF going 0.87 → 1.37–1.45 under
exactly that kind of load. **A contended machine remains the most likely way this PASS degrades in
practice**, and it is one of the three candidate explanations for the onset drift.

---

## 0. ISOLATION GATE — PASS (fail-closed, first act of the session)

Both prior M0 attempts died here. This session's gate passed on the first try, for the reason
`STOP__m0-isolation-gate-2` predicted: **the blocker was process inheritance, and a fresh agent
process does not inherit it.** No configuration change was needed or made.

| # | assertion | result |
|---|---|---|
| 1 | no `NEO4J_*` in environment | PASS |
| 2 | no `HIP_*` in environment | PASS |
| 3 | `NEO4J_PASSWORD` not inherited (length 0) | PASS — this is the one that failed twice before |
| 4 | no env value references a HIP path/graph/credential | PASS |
| 4b | cwd outside every HIP checkout | PASS |
| 5 | `~/moshi-lab` is not a git checkout | PASS |
| 6 | no HIP graph connection held | PASS — all four graphs observed listening, **none contacted** |

The gate is now a script — `isolation_gate.sh` — rather than hand-rolled per session, because it
had been written three different ways in three sessions and the first version reached a **wrong
root cause** (it blamed `~/.zshrc`; the carrier was the parent process). It is name-only and
length-only throughout: the first M0 attempt printed the live Neo4j password into its own
transcript with `env | grep '^NEO4J'`, which emits `NAME=VALUE`. No value appears anywhere in this
session's output or in this document.

**The gate was proved to fire, in both directions** — a gate that has never failed is not evidence:

```
negative control 1: cwd inside a HIP checkout      -> FAIL 4b, exit 1
negative control 2: NEO4J_PASSWORD=<dummy> present -> FAIL 1 and 3, exit 1
clean, from ~/moshi-lab                            -> PASS, exit 0
```

Assertion 4b exists because the coarse version of assertion 4 flagged `PWD` as a credential leak
when this session had `cd`'d into `~/hip-roadmap` to claim its board row. Location and credential
are different faults and now read as different assertions.

---

## 1. Q3 — PRE-EMISSION ACCESS TO THE TEXT STREAM: **YES**

**This is the strongest result in M0 and it is better than "the text arrives first".**

### The exact hook, in the installed source

`~/moshi-lab/.venv/lib/python3.12/site-packages/moshi_mlx/models/lm.py`, `Lm._sample`:

```
:484   text_logits = self.text_linear(transformer_out)
:488   text_token, _ = text_sampler(text_logits)
:490   on_text_hook(text_token)              <-- THE GATE SEES THE TOKEN HERE
:492   audio_tokens = self.depformer.sample(
:493       transformer_out,
:494       audio_sampler,
:495       text_token,                       <-- the audio is BUILT FROM that text token
:496       self.depformer_cache, ...)
:500   on_audio_hook(audio_tokens)
```

**The audio for a frame is not merely later than the text — it is derived from it.** `text_token`
is an *input* to `depformer.sample()`. That is the property an act gate needs: the text is
causally upstream, so a gate that reads at `:490` is reading a decision the audio has not yet been
committed to.

### Executed evidence

`q4_act_gate__ML01.json`, 1200 frames, hooks installed on both sides:

| measure | value |
|---|---|
| `on_text_hook` fired | 1200 / 1200 frames |
| text events / audio events | 1200 / 1200, strictly alternating |
| **`order_violations`** | **0** |
| `q3_text_precedes_audio_every_frame` | **true** |

Independently confirmed by the other lab session's 3750-frame run: 7500 hook events, 3750/3750,
0 order violations. **Two runs, different lengths, same conclusion.**

### The lead: exactly one frame = 80 ms — MEASURED, and a correction

`LmGen.last_audio_tokens()` reads `gen_idx = step_idx - 1 - max_delay` (`generate.py:139`). For
`config_v0_1()`, `audio_delays = [0,1,1,1,1,1,1,1] * 2`, so `max_delay = 1`:

```
lead_frames_min : 1        lead_frames_max : 1        lead_ms : 80.0
```

Min equals max across all 1200 frames — the lead is constant, not an average.

> **CORRECTION, recorded rather than quietly fixed.** This session first told the other lab
> session the lead was **2 frames / 160 ms**, having read `audio_delays` off `config1b_202412()`,
> which is a *different model config* that this run does not use. The correct value is 1 frame /
> 80 ms. It halves the budget an act gate would have, so it is worth having right before anything
> is specified against it. The other session had made the same slip by a different route
> (computing `1 + max_delay`) and both were corrected.

**Do not confuse this with the inner monologue's semantic lead.** The 80 ms is codebook
interleaving. How far the text token sits ahead of the *audible* word is a different question and
**nobody has measured it.** It is not claimed here.

---

## 2. Q4 — SUPPRESS AUDIO WHILE STATE PROCESSING CONTINUES: **YES**

### The gate point in the production server

`local_web.py`, the model loop — text and audio leave on **two separate channels**:

```
:174   text_token = gen.step(data)                      <-- state advances, UNCONDITIONALLY
:180   server_to_client.put_nowait((1, _text))          <-- text out, channel 1
:183   server_to_client.put_nowait((0, audio_tokens))   <-- audio out, channel 0   <-- GATE HERE
```

**Withholding audio is skipping one line.** Note the production server does not even need the
`lm.py` hook: `:175` puts the text token in the loop's own hands before `:183` emits anything.

### Executed evidence — the gate triggers on what the text SAYS

`q4_act_gate__ML01.py` arms on text content (the 6th real word), not a frame number, because HIP's
gate will not know in advance which frame to refuse:

| measure | value |
|---|---|
| gate triggered on text content | **true** — closed at frame 14 on reading word #6 |
| audio frames withheld | **150** (12.0 s) |
| audio frames emitted | 1049 |
| **`state_advanced_through_gate`** | **true** — `final_step_idx` 1200 == expected 1200 |
| words formed *during* the refusal | 3 |
| transcript overall | `" Hi there, how's your day?"` |
| **transcript while gated** | **`" your day?"`** |

**The model kept forming words through the refusal.** `gen.step()` had already advanced
`step_idx`, written the frame's audio tokens into `gen_sequence` and updated the KV cache before
the gate ran; only the waveform was stopped. The model's state continues as though it had spoken.

### A refusal is CHEAPER than speaking

```
step_ms_mean_open  : 72.43 ms      step_ms_mean_gated : 64.74 ms
```

Suppression skips the Mimi decode call, so gating costs **-7.7 ms/frame** of caller time. A gate
that refuses often does not degrade the compute budget; it improves it.

**Do not read 7.7 ms as the decode's cost.** `decode()` is asynchronous, so this is only the
enqueue cost the caller pays. The decode itself is **21.81 ms** when measured directly (§3.4) —
nearly three times larger.

### Honest weakness, not papered over

`transcript_after_reopen` is **empty**: the model said nothing for the 1036 frames after the gate
reopened. **This is not read as gate damage**, because the ungated 5-minute run also produced one
short greeting (`" Hi, what's going on?"`) and then went quiet for 3750 frames — on silence input
this model simply stops talking. But it is a **weak control**: different run, stochastic sampling,
no fixed seed. A same-seed A/B would settle it. It is not thought necessary, because the claim Q4
makes is that state *advances* through the refusal, and `final_step_idx == 1200` plus the
mid-refusal `" your day?"` carry that claim on their own.

---

## 3. Q1 — COMPUTE: **MET, AND WITH ROOM. RTF 0.684 AT STEADY STATE, BOTH STAGES.**

### 3.1 The full-pipeline number — the only one that answers the question as asked

3750 frames = exactly 300.0 s, full pipeline (Mimi encode + LM + Mimi decode), **uncontended**:

| | |
|---|---|
| **RTF overall** | **0.969** |
| RTF first quarter | 0.874 |
| **RTF last quarter** | **1.050** |
| frames over the 80 ms budget | **887 / 3750 (24%)** |
| p50 / p95 / p99 / max (ms) | 76.2 / 87.1 / 121.5 / 623.1 |

**Q1's criterion — RTF ≤ 1 sustained over 5 minutes — is met.** With no margin: the last quarter
is already above real time, and a quarter of all frames miss the budget individually.

*Provenance, since this run was inherited rather than produced here:* written 17:11:26 by the
previous lab session, which is **before** this session's first process started at 17:13:40. It is
therefore uncontended, and that was verified by timestamp, not assumed.

### 3.2 Why this is a RAMP, not a steady state — the fact that reframes Q1

The LM's attention cache is **`RotatingKVCache(max_size=4096)`** — `lm.py:316` calls
`make_rot_cache()`, and `transformer.py:286` sizes it from `cfg.max_seq_len` (**4096**), *not* from
`cfg.context` (3000). So per-step cost **rises while the cache fills** and only reaches steady
state at frame **4096 = 327.68 s = 5 min 28 s**.

**A 3750-frame run stops 346 frames short of that.** Every RTF the lab had was therefore a ramp
average, which flatters the model, and the rising last quarter is the ramp still climbing rather
than noise. Both lab sessions initially misread `context=3000` as the cache size; the correction
was made independently by both and agreed.

### 3.3 The steady state: **MEASURED, ON THE FIFTH ATTEMPT — and the LM does not run away**

**RESULT FIRST.** `q1_plateau_instrumented.json`, 4600 steps, LM-only, `reached_plateau: true`:

| | |
|---|---|
| **plateau mean** | **54.72 ms/frame** — against an 80 ms budget |
| **plateau RTF** | **0.684** |
| plateau frames measured | 504 (steps 4096–4599) |
| plateau p50 / p95 | 54.28 / 57.99 ms |
| **plateau drift** | first half **54.48** → second half **54.95** ms — **+0.47 ms, i.e. FLAT** |
| **plateau frames over budget** | **2 of 504** |
| ramp mean / RTF | 51.65 ms / 0.646 |

**The per-step cost stops climbing.** Per 500-step block: 48.7 → 46.8 → 48.5 → 50.7 → 53.0 → 54.1 →
**55.9** (steps 3000–3499) → 54.8 → 54.8 → 54.5. It rises while the cache fills, tops out around
step 3000–3500, and then **flattens**. This is exactly the behaviour `RotatingKVCache` predicts and
it is the single most important thing M0 did not know this morning: **the cost curve has a ceiling,
and that ceiling is comfortably inside the real-time budget for the language model.**

*Measured by the other lab session on the fifth attempt overall, using the memory instrumentation
described below. ML-01's four attempts and the diagnosis path that made it possible are recorded
honestly; the number is theirs.*

**What this does NOT settle: the FULL pipeline.** This figure excludes Mimi encode and decode. Add
them back and the steady state lands between:

| bound | codec cost added | full-pipeline plateau | RTF |
|---|---|---|---|
| optimistic | 7.7 ms (decode alone, measured §2) | **62.4 ms** | **0.78** |
| pessimistic | ~28 ms (by difference vs the full-pipeline run's last quarter, **inflated by that run's spinning busy-wait**) | **82.7 ms** | **1.03** |

**So the full-pipeline steady state straddles real time**, and which side it falls on depends on a
codec cost nobody has measured cleanly. That is now the sharpest open question in M0, and it is
much narrower than "does this work at all".

> **CLOSED LATER THE SAME SESSION — the codec was measured (§3.4) and the straddle resolved
> (§3.4a): RTF ≈ 0.68.** The two rows above are superseded. Both were built by adding the codec to
> the LM, and the server does not add them — it runs them in separate processes. Left visible
> because the reasoning that produced the range was sound and only the composition was wrong.

### 3.3.1 How the measurement was won — four failures and one diagnosis

Because the ceiling in §4 kills the audio codec at the exact frame the cache stops growing, the
plateau cannot be observed by any run that drives Mimi. `q1_steady__ML01.py` was written to get
around this: pre-encode one frame of silence, retire the `StreamTokenizer`, replay the codes so the
**LM never touches the encoder** and can run past 4096.

**Three attempts, none finished. The stall is reproducible.** The process enters uninterruptible
wait and stops progressing, with system memory around **10–11% free**:

| attempt | by | reached | outcome |
|---|---|---|---|
| 1 | ML-01 | step ~1500 of 6000 | killed deliberately to yield the GPU — see §6; not a stall |
| 2 | ML-01 | **step ~2500** of 6000 | 10% free, swap 38.6 / 39.9 GB, stalled 4 min, `stat=U`, 8–12% CPU |
| 3 | ML-01 | **step ~500** of 6000 | started with 54% free; fell to 11% within 90 s, stalled identically |
| 4 | other lab session | **all 4600 steps — COMPLETED** | **memory-instrumented, `mx.set_cache_limit(512 MB)`** — crossed 4096 and delivered the plateau. Peak 6.85 GB |

Attempt 3 is the informative one: it began on a **deliberately cleaned machine** (54% free, after
attempt 2's process was reaped) and still collapsed within 90 seconds. **So this is not contention
and not transient**, and no amount of waiting or scheduling fixes it.

**PART OF IT WAS OUR HARNESS, NOT THE MACHINE — and this correction cost a fourth attempt to find.**

The first reading here was that the stall was structural: q4 weights (~4.5 GB) plus a full rotating
KV cache (32 layers x 4096 positions x 32 kv-heads x 128 head_dim x 2 (k+v) x 2 bytes bf16 =
~2.1 GB) gives a **~7 GB peak that lands exactly at frame 4096**, against ~7 GB free. The
arithmetic is correct *(contributed by the other lab session, and checked here)*. **It was not the
whole explanation.**

Attempt 3 lost ~13 GB in 90 seconds at step ~500, where weights plus a 12%-full cache account for
only ~5 GB. The missing 8 GB was **MLX's GPU buffer cache, which is unbounded by default** — the
other lab session diagnosed this and proved it with two lines: `mx.set_cache_limit(512 MB)` plus
per-250-step sampling of `mx.get_active_memory()` / `get_cache_memory()` / `get_peak_memory()`.

**Attempt 4, so instrumented, behaved completely differently** — the allocator cache pinned at
0.48–0.49 GB against its ceiling while `active` rose ~0.12 GB per 250 steps, which is the KV cache
filling **and nothing else**:

```
after load+warmup   active=4.44GB  cache=0.13GB  peak=4.58GB
step 1000           active=4.98GB  cache=0.49GB  peak=5.15GB
step 2000           active=5.48GB  cache=0.48GB  peak=5.82GB
step 3500           active=6.23GB  cache=0.49GB  peak=6.56GB
```

**With the cache capped, the run completed** — all 4600 steps, past 4096, at a **6.85 GB peak**.
The ~7 GB footprint arithmetic was therefore *correct about the size* and wrong about the
consequence: 7 GB was always affordable on this machine. What was not affordable was 7 GB **plus an
unbounded allocator cache**, which is what every earlier attempt was actually asking for.

**One fix, two lines, turned four failures into a result.** Anyone repeating this must set the
cache limit; without it the run dies well before the plateau and the failure looks like the machine.

> **THIS DIAGNOSIS WAS WRONG TWICE BEFORE IT WAS RIGHT.** Both errors are kept visible, in order,
> because the shape of them is the useful part:
>
> 1. **"Pre-existing machine condition."** First reading: 16 days of uptime, saturated swap,
>    nothing to do with the lab. **Wrong, and unfair to the machine** — killing the stalled process
>    moved memory 11% → 54% free and swap 38.6 → 27.3 GB, so the run was the dominant consumer.
> 2. **"Structural — peak footprint equals free memory."** Second reading, with correct arithmetic
>    behind it. **Also wrong as an explanation**: it could not account for attempt 3 shedding ~13 GB
>    at a step where the experiment needed ~5 GB. The unbounded allocator cache did.
>
> **Both errors blamed the environment for a fault in our own tooling**, which is the same reflex
> that misattributed the contention in §6. What broke the pattern was *instrumenting the thing
> being blamed* rather than reasoning about it.
>
> **A trap worth carrying:** the stalled process reported an **RSS of 16–21 MB** while holding the
> machine down. MLX's Metal allocations never appear in RSS. Use `mx.get_active_memory()` /
> `get_cache_memory()` / `get_peak_memory()`, or system-wide free memory and the swap delta across
> a kill — never per-process RSS.
>
> **The ~27 GB swap baseline with no lab process running is unchanged and still worth knowing.**
> It just is not what killed the measurement.

### The ramp, for completeness

The climb to the plateau, LM-only against the 80 ms budget, per 250 frames:

| step | 500 | 1000 | 1500 | 2000 | 2500 | 3000 | **3500** |
|---|---|---|---|---|---|---|---|
| ms/frame | 45.4 | 47.0 | 49.0 | 51.4 | 53.4 | 54.2 | **55.9** |
| RTF | 0.57 | 0.59 | 0.61 | 0.64 | 0.67 | 0.68 | **0.70** |

The climb is steady and **decelerating**, and it stops entirely at the plateau (§3.3). ML-01's own
clean segments agree where they overlap — 44.5–47.5 ms over steps 0–1500, and 61.95 ms over steps
2000–2500 on a machine still carrying background load.

So the LM alone has real headroom — roughly **45–62 ms against an 80 ms budget** — and climbs about
1.5 ms per 500 steps as the cache fills. **Extrapolation to 4096 is deliberately not reported as a
result**, though the partial data would support one.

**This question is now CLOSED** — see the plateau result at the top of §3.3. What remains open is
the *full-pipeline* steady state, which needs the Mimi codec cost measured cleanly rather than
inferred by subtraction, and that is a short CPU-side job.

### 3.4 Where the budget actually goes — the codec, not the model

**MEASURED DIRECTLY, not inferred** (`codec_cost.json`, other lab session, 1800 frames each side,
serial and in isolation):

| | mean ms/frame | p95 |
|---|---|---|
| Mimi **encode** (user audio in) | **21.30** | 22.36 |
| Mimi **decode** (Moshi's voice out) | **21.81** | 22.85 |
| **codec total, serial** | **43.11** | |

**The codec is comparable in cost to the 7B language model itself** — 43 ms against the LM's
54.7 ms plateau. That is the opposite of where anyone would look first, and it is the most
actionable number in this document: if compute becomes binding, the audio codec is the target, not
the model.

> **CORRECTION TO THIS SECTION'S EARLIER FIGURE, which was mine.** §2 observes that gating audio
> saves **7.7 ms/frame** of caller time, and this section previously offered that as "Mimi decode
> alone". **That was wrong.** `StreamTokenizer.decode()` is asynchronous — it hands work to a
> background thread — so 7.7 ms is the *enqueue* cost the caller pays, not what the decode costs.
> The real figure is **21.81 ms**, nearly three times larger. The §2 observation still stands as
> written (a refusal is cheaper for the caller); what was wrong was reading an enqueue cost as a
> codec cost.

### 3.4a THE STRADDLE IS RESOLVED — and it falls on the GOOD side: **RTF ≈ 0.684**

**The server does not pay LM + codec. It pays the slower of the two.** `local_web.py:432-437`
starts **two separate OS processes**:

| process | owns | cost/frame | RTF |
|---|---|---|---|
| `web_server` (p1) | the **only** `StreamTokenizer` — all encode and decode | 43.11 ms | 0.539 |
| `model_server` (p2) | the LM — **never touches Mimi**, receives codes over a `multiprocessing.Queue` | 54.72 ms | **0.684** |

```
rate-limited by the slower stage : max(54.72, 43.11) = 54.72 ms -> RTF 0.684
the sum                          :     54.72 + 43.11 = 97.83 ms -> RTF 1.223  <-- only a
                                                                    single-process harness pays this
```

**VERIFIED INDEPENDENTLY IN THE SOURCE, not accepted on report** — this reverses a conclusion, so it
was checked rather than taken: `model_server` (lines 114–187) contains **zero** references to
`rustymimi`, `mimi`, `encode` or `decode`; its input arrives at `:172` as `client_to_server.get()`.
The sole `StreamTokenizer` is constructed at `:207`, inside `web_server`. Both are launched as
`multiprocessing.Process` and started back to back.

**So every "full pipeline" number this lab holds — including the 0.969 — is a HARNESS artifact.**
`m0_experiments.py` runs encode, LM step and decode in **one** process and **blocks** on
`get_encoded()` before stepping the LM, so the codec *could not* overlap the model. That
serialisation is self-imposed by the measuring instrument and does not exist in the server.

**The reconciliation that makes this confident rather than hopeful** *(other lab session)*: rebuild
the 5-minute run from independently measured parts — blocking encode 21.3 + LM 51.3 + async decode
*enqueue* 7.7 = **80.3 ms**, against **77.49 ms** actually measured. **Within 4%.** The
decomposition explains the number it was derived from, and the 7.7 ms enqueue cost sits in it
exactly where the correction above says it should — with 21.8 ms in that slot the arithmetic would
not close.

> **BOTH SESSIONS WERE WRONG IN THE SAME DIRECTION ALL DAY.** We assumed the ramp average
> *flattered* the model and that the true steady state would be worse. **It is the reverse:** the
> ramp average was *inflated* by harness serialisation, and the true steady state is better.
> **0.969 is a pessimistic bound, not a flattering one.**

**Caveats, stated because this result will be quoted without them:**
- **The overlap is only free when cores are spare.** §6 is this machine failing exactly that test.
- **43.11 ms is serial latency measured in isolation.** Inside a live turn encode and decode share
  one tokenizer in one process, so the codec stage is *bounded by* 43.11 ms, not equal to it.
- It remains below the LM either way, which is why the conclusion is robust: the LM is the
  rate-limiting stage, and it plateaus flat at 0.684.

> ### 3.4a RESOLVED — the overlap is not a hope, it is the architecture
>
> The row above labelled *"observed in practice, ~81 ms, RTF ~1.01"* is **an artefact of the
> measuring harness, not a property of the server**, and the distinction decides Q1.
>
> `m0_experiments.py` runs encode, LM step and decode in **ONE process**, and it *blocks* on
> `get_encoded()` before stepping the LM. So the codec could not overlap the model — the harness
> forbade it. Reconstructing that run from the measured parts:
> `blocking encode 21.3 + LM 51.3 + async decode enqueue ~7.7 = 80.3 ms` against **77.49 ms
> measured** — it reconciles to within 4%, which is what confirms the decomposition.
>
> **`local_web.py` does not do that.** Lines 432-437 start **two separate processes**:
>
> | process | owns | steady-state cost |
> |---|---|---|
> | `web_server` (p1) | the `StreamTokenizer` — **all** encode and decode | **43.11 ms** → RTF 0.539 |
> | `model_server` (p2) | the LM — **never touches Mimi**, receives codes over a queue | **54.72 ms** → RTF 0.684 |
>
> They run concurrently, on different cores, communicating through
> `multiprocessing.Queue`. The pipeline is therefore rate-limited by the **slower stage**, not by
> the sum:
>
> ```
> pipeline rate = max(54.72, 43.11) = 54.72 ms  ->  RTF 0.684
> sum (what a single-process harness pays) = 97.83 ms  ->  RTF 1.223
> ```
>
> **Q1's steady-state answer is RTF ≈ 0.68, rate-limited by the language model, with the codec
> inside budget on its own core.** The 0.969 of §3.1 is a *pessimistic* bound — it serialised work
> the real architecture overlaps — not a flattering one, which is the opposite of what this
> document assumed for most of the day.
>
> **Two caveats, both real.** The concurrency is only free when there are cores to spare, and §6
> measured this machine failing exactly that test — a CPU-only job halved a GPU-bound one through
> unified memory. And 43.11 ms is a serial per-frame latency measured in isolation; inside a live
> turn encode and decode share one tokenizer, so their combined cost is *bounded by* 43.11 ms
> rather than equal to it.

---

## 4. NEW BLOCKER FOUND: A HARD 5 min 28 s CEILING IN **BOTH** DIRECTIONS

**This was not known before today and nothing in M0's brief anticipated it.**

`rustymimi` 0.4.1's streaming tokenizer dies after exactly **4096 frames = 327.68 s = 5 min 27.7 s**
of continuous audio, with:

```
error in encoder thread narrow invalid args start + len > dim_len: [8192, 32], dim: 0, start: 8192, len: 2
```

8192 rows consumed 2 per frame = 4096 frames. Characterised **without the LM at all** — `rustymimi`
is a separate Rust crate that never sees the model config, so the wall can be isolated on CPU with
no GPU and no model load (`encoder_ceiling__ML01.py`):

| phase | result |
|---|---|
| self-check, 50 frames | **50/50** — the harness had to prove itself before being allowed to report a wall |
| clean frames | **exactly 4096** |
| first stall | **frame 4096 = 327.68 s** |
| same instance afterwards | **0/20 — never recovers** |
| fresh `StreamTokenizer` | **200/200 clean**, rebuild cost **0.61 s** |

**The decoder walls identically** — measured separately by the other lab session
(`decoder_ceiling.json`): 4096 clean frames, same frame, byte-identical error text, same
non-recovery, same fresh-instance fix. **So this is one buffer pattern hit once per direction.**

**Why that is worse than either wall alone: at 5 min 28 s the stack stops hearing and stops
speaking at the same moment.** And `local_web.py:207` builds **one shared `StreamTokenizer` for
both directions**, so a single wall takes out both ends of a live conversation together.

**The symptom is silence, not an error.** The reader loops at `local_web.py:231` and `:239` are
`while True` with no error path, so the conversation simply goes quiet while the page still looks
connected. Anyone testing this would read it as "the model broke".

**Workaround, with a cost, not a fix:** discard both tokenizers and build new ones — there is **no
`reset()`** on the class, confirmed on both sides. 0.61 s on a quiet machine, and streaming state
is lost, so it is an audible gap mid-conversation every 5.5 minutes.

### RULED BY BILL, 2026-08-13 — **ACCEPTED for the research lane. KNOWN PRODUCT CONSTRAINT.**

> **ACCEPTED for the research lane — periodic tokenizer rotation with the ~0.61 s audible gap every
> ~5.5 minutes is the M0/M1 workaround. Record it as a KNOWN PRODUCT CONSTRAINT: any product claim
> later needs a real engineering answer (seamless or overlapping rotation), not this gap.**

**What this unblocks:** M0 and M1 proceed. The lane is not parked, and the rotation workaround is
the sanctioned way to run past 5 min 28 s for research purposes.

**What it explicitly does NOT license, and this is the load-bearing half of the ruling:** the gap is
acceptable *in the lab*, not *in the product*. **A product claim that rests on a conversation
surviving past 5.5 minutes needs a real engineering answer — seamless or overlapping rotation — and
this workaround is not it.** A rotation that stops the conversation for 0.61 s and loses streaming
state is a research convenience being spent against a debt that has not been paid.

**The shape that answer will need to take**, recorded now while the mechanism is fresh rather than
rediscovered later: build the replacement `StreamTokenizer` *before* the wall, run both briefly in
parallel, and cut over at a frame boundary — the 0.61 s is construction cost, and construction can
happen off the critical path. Nothing in `rustymimi`'s API prevents this; it exposes no `reset()`,
but it does not stop a second instance existing. **Unverified — no prototype was built and this is
a direction, not a result.**

**Carried into M1 as a standing constraint, not a to-do:** any M1 experiment running longer than
5 min 28 s must rotate, and must say so in its own findings rather than silently absorbing the gap.

---

## 5. Q2 — DUPLEX MIC TEST: **ANSWERED 2026-08-14 BY BILL. DUPLEX WORKS.**

**Run under co-tenancy** — `ollama` resident, ~12% system memory free. That is the realistic HIP
condition, not a clean-room one, and it matters for reading the timing observation below.

### Bill's observations, verbatim

> *"There was some latency in response toward the end. It would almost cut me off before I finished
> my sentence. In other words, its response was very fast at the beginning. So, need some
> calibration there."*
>
> *"It was good at finding the semantic end point of my speech."*
>
> *"Not walkie talkie, but needing tuning and maybe a larger brain behind it to help answer these
> questions."*

Content quality: **bad** — *"this AI is an idiot and knows nothing."*

### What Q2 does and does not grade

**Q2 grades turn mechanics, not content.** Bill flagged the content quality himself as expected of a
7B base model and explicitly not what this test measures. That is the correct reading, and it is
worth stating why it is not a bad result: **"maybe a larger brain behind it" is the dual-model
architecture the research lane exists to test.** Moshi's job in that design is the duplex voice
layer; the content comes from elsewhere. A base model that turn-takes well and answers badly is the
premise working, not failing.

### The result

| question | answer |
|---|---|
| **Is it duplex, or half-duplex push-to-talk?** | **DUPLEX. "Not walkie talkie."** |
| **Endpoint detection — does it find where a sentence ends?** | **GOOD.** *"good at finding the semantic end point of my speech"* |
| **Response-onset timing** | **DRIFTED over the session — fast early, near-barge-in later.** Needs calibration |
| Content quality | Bad, and out of scope — see above |

**Q2 PASSES on the question it was built to answer.** The duplex mechanism works and the semantic
endpointing — the hard part, and the thing a VAD threshold cannot do — works well.

### THE ONE REAL FINDING: response-onset timing drifts over a session

**This is the top M1 open question and it is NOT investigated here, by instruction.** Recorded with
enough structure that M1 can start from it rather than rediscover it.

**The observation:** response onset was *very fast* early in the session and by the end the model
would *almost cut Bill off before he finished a sentence*. The drift is toward **earlier** onset —
it became progressively more eager, not slower. Endpoint detection stayed good throughout, so
whatever moved, it was not the model's ability to find the end of a sentence.

**Three candidate mechanisms, and they have different fixes:**

1. **A tunable parameter.** Sampler settings or an onset threshold. Moshi has no explicit VAD — turn
   taking is learned — so "tuning" here means sampler/decision parameters, not a knob labelled
   endpointing. **Cheapest to test, and Bill's own reading ("need some calibration there").**
2. **A state / KV-growth artifact — and there is a specific reason to suspect this one.** The
   attention cache fills at **frame 4096**, and at that exact frame it stops growing and begins
   **rotating**, evicting oldest context. §3.3 measured the compute cost flattening there. **"Toward
   the end" of a multi-minute session is precisely when that transition happens.** If the drift
   tracks the cache filling, it is structural, not tunable — and no amount of parameter calibration
   fixes it.
3. **Co-tenancy compute contention.** `ollama` was resident with ~12% memory free. §6 measured this
   lab's own RTF going from 0.87 to 1.37–1.45 under contention. **A model running behind real time
   produces mistimed onsets**, which is exactly the reported symptom.

**Does it interact with the 4096-frame ceiling?** **Possibly, and the coincidence is worth stating
plainly rather than leaving for someone to notice:** the KV cache fills at 4096 frames and the Mimi
codec dies at 4096 frames. **Those are the same number by coincidence** (one is `max_seq_len` in the
model config, the other an 8192-row buffer at 2 rows/frame in a Rust crate that never reads that
config — §4). But it means **the last ~30 seconds before the codec wall are also the frames where
the cache begins rotating.** Any behavioural change "toward the end" of a ~5-minute session lands in
that window, and the two causes are not separable by observation alone.

**What would distinguish them, for M1 to run rather than for this session to attempt:**
- Log the **frame index** at which the drift appears and compare it to 4096. If it tracks 4096
  across sessions of different lengths, it is (2), not (1).
- Run the same script **twice — quiet machine and contended** — to separate (3) from the rest.
- If it is (1), the drift should be reproducible at any frame index and adjustable by parameter.

**Do not assume tunable.** Bill's instinct — "need some calibration" — is the cheapest hypothesis
and may well be right, but hypothesis (2) predicts the same symptom and would not respond to
calibration at all. Testing the frame index first costs almost nothing and rules out the expensive
mistake.

---

## 5a. The Q2 package as delivered

Everything was installed and pre-downloaded; nothing downloaded at run time.

- Launcher: `~/moshi-lab/launch_q2.sh` — strips every `NEO4J_*`/`HIP_*` name from the environment
  before starting anything, so the server cannot inherit a credential even from a shell that has one.
- Instructions: `~/moshi-lab/Q2_MIC_TEST__printed-instructions.md` — four turn-mechanics tests,
  four yes/no answers plus one latency impression.

Two fixes were made to that package this session, both of which would otherwise have wasted Bill's trip:

1. **`--steps 15000`.** The upstream default is 4000 frames = 5 min 20 s, and it does not end
   politely — `generate.py:68` raises `ValueError: reached max-steps 4000` and the session dies
   mid-sentence, inside the test window.
2. **The 5 min 28 s ceiling is now written into the instructions**, because fix (1) alone would
   have promised a 20-minute session that the audio path cannot deliver, and the failure is silent.
   Bill is told to keep runs under five minutes, that silence past that point is this ceiling and
   not his microphone, and that it is worth reporting if it happens.

---

## 6. THE OTHER FINDING: THIS MACHINE CANNOT MEASURE ITSELF WHILE BUSY

**Four separate measurements were invalidated by contention today, and the largest cause was this
session's own mistake.** Recording it because every RTF number this lane produces is affected.

| # | what happened | effect |
|---|---|---|
| 1 | Two lab sessions ran M0 concurrently, unaware of each other | RTF read **1.37–1.45** where the same model alone read **0.87**. Proof: the other process jumped 146% → 275% CPU the instant this one was killed |
| 2 | The other session's 4500-step run hung at the codec wall | Unbounded `while True` at `m0_experiments.py:109-112` with no error path — one codec fault spins forever. It burned a core for ~20 minutes with no progress and never wrote its output |
| 3 | A "CPU-only" test contended with a GPU run | Unified memory: 3.4 cores of CPU load halved a GPU-bound MLX job. **There is one resource on this machine, not two** |
| 4 | **This session's own orphaned process** | A kill that never happened (below) left two of this session's own runs racing for five minutes, and the slowdown was initially misattributed to the other session |

### The mistake worth carrying, because it happened twice in one afternoon

Both of this session's false results came from **a check structurally incapable of returning the
answer it was read as giving** — not from a wrong measurement:

- **The orphan.** `pkill -f "bin/python q1_steady__ML01.py"` matched nothing, because the
  interpreter's argv[0] is `.../Python.framework/.../MacOS/Python`, not `bin/python`. The
  *verification* used the same pattern, so it returned a confident "confirmed: my Q1 run stopped"
  that was false. **Verify a kill BY PID (`ps -p <pid>`), never by the pattern used to kill it.**
- **The first encoder-ceiling script** bounded its wait by *iterations* rather than *time*. 200
  tight polls elapse in microseconds and give an asynchronous encoder thread no chance to answer,
  so it reported a healthy encoder as walled **from frame 0**. The fix that makes such a script
  trustworthy is the **self-check phase**: 50 frames must succeed before the harness is permitted
  to report a ceiling at all.

This is the same failure family as CLAUDE.md's Requirements Discipline item 13 — *an exit code is
not an answer* — arriving through `pkill` and a poll loop rather than through `grep -c`.

**Consequence for the lane:** `sample_load.sh` was written to record concurrent load alongside each
run and then **not wired into the runs**, which is this session's own miss. Every RTF number this
lab keeps should carry what else was running, or it is not reproducible.

---

## 7. WHAT WAS NOT DONE

No HIP data read, no HIP credential held, no HIP graph contacted, no HIP-owned path written. No
Q2 mic test. No fixed-seed A/B for the gate.

> **UPDATED before delivery: the Mimi codec's per-frame cost WAS measured** (§3.4 — 21.30 ms
> encode, 21.81 ms decode, 1800 timed frames each, separate instances) and the steady state it left
> open is resolved in §3.4a. This paragraph previously recorded it as the highest-value remaining
> work; it is done, and **Q2 is now the only open item in M0.**

**Still genuinely not done:** no live full-pipeline run past 4096 frames — the §4 ceiling makes one
impossible without rebuilding the tokenizers mid-run, which is why §3.4a is composed from two
measured stages rather than observed end-to-end. That composition is reconciled against a measured
run to within 4%, but it is a composition, and it is the one number in this document that a live
session could still contradict.

*(No download was needed by THIS session; M0's 4.9 GB was pulled by the preceding session at
17:04–17:05 — see the header. The 20 GB stop was approached to about a quarter, stage-wide.)*

> **UPDATED before delivery: `m0_experiments.py`'s unbounded wait IS now fixed**, by the session
> that wrote it. The wait is bounded in *time* (2.0 s, not iterations — the trap from §6), stalls
> are counted into `encoder_stalls` / `encoder_walled` rather than priced silently into `step_ms`,
> and the run abandons itself at the first stall instead of spinning. Reported `steps` is now the
> count actually completed, so a walled run cannot quietly report a full-length RTF. Patched and
> syntax-checked only — **not re-run**, because the machine was in use.

The only HIP-tree writes in this dispatch are `docs/LANES.md` board rows — the claim (`972da7d`),
the close (`3fa729f`) and the corrections that followed it — all pushed. **No lab artifact crosses the border** (method
doc §3); this document is the only thing eligible to, and only via a normal docs dispatch.

---

## 8. NEEDS BILL — **NOTHING. M0 IS CLOSED.**

Both items that needed a decision have been decided. Kept struck through rather than deleted so the
record shows what was asked and when it was answered.

1. ~~**Q2 mic test — ~10 minutes at the machine.**~~ **DONE 2026-08-14.** Bill ran it; results and
   the drift finding at §5. **Nothing outstanding here.**
2. ~~**A ruling on the 5 min 28 s ceiling.**~~ **RULED 2026-08-13 — ACCEPTED for the research lane**
   as a KNOWN PRODUCT CONSTRAINT; periodic rotation with the ~0.61 s gap is the M0/M1 workaround,
   and any later product claim needs a real engineering answer instead. Full ruling at §4. **Nothing
   outstanding here.**
3. **Machine memory — FYI only; it cost four attempts but did NOT block the result.** The machine
   carries a **~27 GB swap baseline with no lab process running**. That is worth knowing for any
   timing work here, not just Moshi's. **It is not what stalled the measurement** — an unbounded
   MLX allocator cache was, and capping it (`mx.set_cache_limit`) delivered the plateau on the
   fifth attempt at a 6.85 GB peak. No action needed.
4. **CARRIED FORWARD, still open, not created by this lab.** Voice 1 found two LaunchAgent plists
   holding `NEO4J_PASSWORD` in plaintext — `~/Library/LaunchAgents/com.hip.voice.orch.plist` and
   `com.hip.demo.dashboard.plist`. With Voice 1's fix the credential now lives in **three** places
   on disk (`~/.hip-env` plus those two), so a rotation must reach all three. **M0 did not touch
   them and no value was read.** Also still Bill's call: the first M0 attempt printed the live
   password into its own transcript, and whether that warrants rotation was never ruled on.

---

## 9. WHAT M1 INHERITS

**Read this section first if you are starting M1.** The rest of this document is evidence; this is
the part that changes what M1 does.

**1. THE TOP M1 OPEN QUESTION — response-onset drift (§5).** Response onset was fast early in Bill's
session and near-barge-in by the end, while semantic endpointing stayed good throughout. **Three
candidate mechanisms with different fixes:** a tunable parameter, a KV-cache/state artifact at the
4096-frame boundary, or co-tenancy contention. **Test the frame index first** — it is nearly free
and it rules out the expensive mistake of calibrating something structural. Bill's instruction was
to record this, not investigate it; M0 did not investigate it.

**2. A STANDING CONSTRAINT, not a to-do.** Any M1 experiment running longer than **5 min 28 s** must
rotate the Mimi tokenizer and **must say so in its own findings**. Absorbing the ~0.61 s gap
silently would leave a reader looking at a clean long conversation that never happened.

**3. THE HOOKS ARE FOUND AND HOLD.** M1 does not need to rediscover them: `lm.py:490` for
pre-emission text (audio is causally downstream, §1), `local_web.py:183` for the audio gate, and
one frame — 80 ms — of lead between them.

**4. MEASUREMENT HYGIENE THIS STAGE PAID FOR.** Four measurements were invalidated before anything
was learned (§6). The cheap protections: **cap the MLX allocator** (`mx.set_cache_limit`) or long
runs die looking like a machine fault; **record concurrent load beside every timing number**;
**verify a kill by PID, never by the pattern used to kill it**; and **give any harness a self-check
phase that must pass before it is allowed to report a failure** — two of this stage's false results
came from checks structurally incapable of returning the answer they were read as giving.

**5. THE ONE THING NOT MEASURED CLEANLY.** The codec's per-frame cost is known (21.3 ms encode /
21.8 ms decode) and the pipeline composes by `max`, not sum, because the server runs two processes
(§3.4a). What has never been measured is a **live full-pipeline session under real co-tenancy** —
every number here is either synthetic or single-process. That is the gap most likely to surprise
someone later.
