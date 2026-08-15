# DISPATCH_HA77 — Groq model decommission (Aug 16): inventory, centralize, swap
Status: BUILT
Reconciled-Against: roadmap `fb6cee7`, hip-vo `f074d8f`

**TYPE:** BUILD — infrastructure config across **two trees**, `~/hip-roadmap` @
`roadmap` and `~/hip-vo` @ `main`.

**REQ:** **NONE, and that is the honest state.** No requirements doc names the
Groq model id — this is infrastructure configuration under the same law as the
graph pins. Filing a REQ for a two-day decommission after the fact would be the
retroactive-REQ contradiction CLAUDE.md item 8 explicitly forbids. Recorded
rather than invented.

**URGENCY:** Groq decommissions `llama-3.3-70b-versatile` on **2026-08-16**.
After that date every request to it fails.

---

## PART A — INVENTORY

**Replacement verified against Groq's LIVE model list before use** (15 models
returned): `openai/gpt-oss-120b` is present and served. So are
`llama-3.1-8b-instant` (MID) and `openai/gpt-oss-20b` (fact-change).

**Only ONE tier is affected: CORE.** MID and the fact-change detector do not use
the dying model.

### This lane's two trees — every occurrence, now config-driven

| file:line (both trees) | literal | code path |
|---|---|---|
| `server/voice_orch.py` (`:167` vo / `:159` rm) | `GROQ_MODEL_CORE` | **typed + voice generation**, CORE tier |
| `server/voice_orch.py` (`:399` vo / `:343` rm) | cost-table key | pricing per 1K tokens |
| `harness/epistemic_record.py` (`:113` vo / `:140` rm) | `_GROQ_MODEL_TARGETS` | **GOVERNANCE — off-net vs on-net** |
| `harness/fact_change.py:56` | `GROQ_MODEL` | detector (`openai/gpt-oss-20b`, unaffected) |
| `scripts/generate_corpus.py:64` | `GENERATOR_MODEL` | corpus generation |
| `server/static/demo.html:120` | `GROQ_MODEL_TARGETS` | **browser** routing display |
| `config.yaml:77` | prose comment | docs |
| `eval/**/passthrough_consent_*.json` | `tier_target` | **historical evidence records — left as written** |

### THE FINDING THAT MATTERS MOST

`harness/epistemic_record._compute_net` uses the Groq roster to decide **OFF-NET
vs ON-NET** for a turn's governance record. **A model id swapped in config but
missed in that roster classifies a real, off-device Groq call as `"on"`** — a
network crossing recorded as a local turn. That is a governance defect, not a
display bug. It is why the roster is now DERIVED from the config point.

### Other lanes — REPORT ONLY, NOT TOUCHED (the handoff)

**All three will break on 2026-08-16 unless their own lanes swap them.**

| checkout | files | notable |
|---|---|---|
| `~/hip-dev` (**frozen demo**) | **8** | live `GROQ_MODEL_CORE:161`, cost table `:345`, `demo.html:120`, `generate_corpus.py:64` |
| `~/hip-cutover-demo` | **7** | `GROQ_MODEL_CORE:165`, `epistemic_record.py:156`, `demo.html:120` |
| `~/hip-harness` | **2** | `GROQ_MODEL_CORE:138`, cost table `:252` — **and TD-132 records this repo has served 7860** |

## PART B — CENTRALIZE

**`harness/groq_models.py`** (new, both trees) resolves every id from
`config.yaml`'s new `models.groq` block. Production and gate-bearing code reads
that module; **no Groq model literal remains in scanned code.**

The module **REFUSES rather than defaulting** — a silent default is exactly how
the decommissioned id survived in five places per tree.

**The browser is the one place no import can reach.** `demo.html` shares no
runtime with Python, so its roster is a genuine duplicate; that duplication is
now **enforced by a twin** asserting the two agree, rather than trusted to the
comment that previously said "update both".

**Twin — `eval/test_groq_model_centralized.py`, 15 tests per tree.** AST scan
over production/gate-bearing code, **docstrings stripped**: this file, the config
module and several call sites NAME the dying id in prose, and matching prose is
not matching code (the trap HA-72 and HA-76 both hit). Planted-literal twin goes
red in **both** directions — it catches a planted id, and does not fire on
ordinary strings. It also asserts the governance roster is **derived** (identity,
not equality) and exercises `_compute_net` directly, so a CORE turn on the new
model is proven to classify off-net.

## PART C — SWAP + PROVE

**C1.** Set at `config.yaml` → `models.groq.core` and `corpus_generator`.

**C2 — LIVE SMOKE, both trees, today, before the old model dies:**

| tree | path | result |
|---|---|---|
| hip-vo | **through the egress gateway** (`permit` → `Destination.GROQ_OFFNET`) | CORE `openai/gpt-oss-120b` → HTTP OK, `served_by=openai/gpt-oss-120b`; MID OK |
| roadmap | **direct** — that tree has no `egress_gateway` module (stated, not worked around) | same two models, both HTTP OK |

**C3 — BINDING SUITES (model-independent). Both green.**

| tree | suite | result |
|---|---|---|
| hip-vo | governance suite | **250 collected / 0 failed / 0 errors / 0 skipped** |
| roadmap | batteries, services up | **31 failed / 1321 passed** — HA-76 baseline was 31 / 1306; **+15 = exactly this dispatch's suite, ZERO new failures** |
| roadmap | `--layer 7` | **RATCHET PASS**, L7 27/27, L7V2 27/28 |

**C4 — NEW-MODEL BASELINE EVIDENCE. Recorded beside the old numbers. NO ratchet,
no gating change, no expectation rebase.**

| layer | OLD (HA-76, `llama-3.3-70b-versatile`) | NEW (HA-77, `openai/gpt-oss-120b`) |
|---|---|---|
| L1 | 15/15 | **15/15** |
| L2 | 24/35 (10 skipped) | **24/35 (10 skipped)** |
| L3 | 3/3 | **3/3** |
| L4 | 30/34 (4 skipped) | **30/34 (4 skipped)** |
| L6 | 1/1 | **0/1 ← new failure, see below** |
| L7 / L7V2 | 27/27 / 27/28 | **27/27 / 27/28** |
| AUDIT / DISC / SCHEMA / VOICE | pass | **pass** |

`BINDING TESTS PASS`. Live-layer regression `L2:routing_showcase.T04` is
**unchanged from HA-76** — pre-existing, not chased. Results appended to
`logs/harness/live_layer_results.csv` (`run_id=20260814T160806_5b3c7c0`).

**No material routing or threshold shift observed:** L1–L4 counts are identical
across the model change, which is the closest thing to a routing-% comparison
this harness produces.

### The one new failure, chased rather than filed under "live layer"

`L6:record-invariants` — `G1 no-orphan-generation: 1 violation [HARD ZERO]`.

**It is NOT my wiring.** G1 examines `path`, `resolved_subjects`, `delta`,
`inj2_declarative_override` and `admitted` — none of which this dispatch touches.
The `_compute_net` roster change is proven correct by its own twin.

**It is a TD-125 cascade.** The violating turn is declarative —
`[sam] "I take atorvastatin 20mg every morning."` — and its reply is *"I was
unable to save it to the household record just now."* G1 exempts declarative
turns only when a write landed (`delta` non-empty) or INJ-2 matched; here
extraction failed, so `delta=[]` and G1 fired. The run logged **9 `zero changes
for owner=…` detector events**, one on `owner=sam` adjacent to that turn.

**Worth Bill's attention as possibly new information: a TD-125 false negative can
cascade into a HARD ZERO governance invariant**, not just a missing write.

**C5 — TD-125: THE DECOMMISSION CANNOT CHANGE THE ZERO-CHANGES SHAPE, because
TD-125's detector never used the dying model.**

* **roadmap** — the detector runs on Groq, with **`openai/gpt-oss-20b`**, which is
  not decommissioned and was not changed here.
* **hip-vo** — `_call_groq` has been **DISABLED since HA-55**
  (`REQ_EGRESS_GATEWAY` rule 2); every caller uses `_call_local` against Ollama.

Empirically consistent: the shape still appears (9 events) on the unchanged
detector. **The pin and TD-125 stand exactly as ruled.**

## NOT DONE, DELIBERATELY

**The CORE cost rate is unchanged.** `_MODEL_RATES_PER_1K` is keyed by the
constant so the swap carried automatically, but the rate is still
`llama-3.3-70b-versatile`'s. **Repricing `openai/gpt-oss-120b` is a measurement
and Bill's to rule on** — not a guess smuggled in with a model swap. Marked
`RATE STALE` in the source.

## A COORDINATION FINDING

My first `--full` was **SIGKILLed (rc=137)** by macOS memory pressure at 11% free.
The cause was two concurrent full ratchets: **Voice 41 was running its own
`eval.harness --full`** under the `graph:7691` lock. I did **not** kill it — I
waited ~27 minutes and re-ran cleanly at 47% free.

**The lock is keyed per RESOURCE (`repo`, `graph:PORT`) and nothing arbitrates
MACHINE MEMORY.** Two lanes on different graphs take no contending lock and OOM
each other anyway. Filed for Bill; not fixed here (Finiteness Rule — it did not
block this phase's acceptance criteria).

## CLAIM IMPACT

**CLAIM IMPACT: none.**

## OPEN — NEEDS BILL

1. **Three other checkouts still carry the dying id** and break on 2026-08-16 —
   `~/hip-dev` (8 files), `~/hip-cutover-demo` (7), `~/hip-harness` (2). Their
   lanes swap their own trees; the table above is the handoff.
2. **CORE token rate needs repricing** for `openai/gpt-oss-120b` (measurement).
3. **A TD-125 false negative can cascade into a HARD ZERO G1 violation** —
   evidence recorded, no pin or expectation touched.
4. **No lock arbitrates machine memory** across concurrent full-ratchet runs.
