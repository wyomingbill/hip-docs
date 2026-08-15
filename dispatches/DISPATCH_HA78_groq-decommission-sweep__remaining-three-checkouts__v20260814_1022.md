# DISPATCH_HA78 — Groq decommission sweep: the remaining three checkouts
Status: BUILT
Reconciled-Against: hip-dev `442050a`, hip-cutover-demo `a869637`, hip-harness `14ac694`

**TYPE:** BUILD — infrastructure config across **three trees outside this lane's
usual pair**.

**REQ:** **NONE**, same as HA-77 and for the same reason: no requirements doc
names the Groq model id: this is infrastructure config under the graph-pin law.
Filing one retroactively for a two-day decommission is the contradiction
CLAUDE.md item 8 forbids.

**DEADLINE:** the model dies **2026-08-16**.

**SCOPE NOTE:** `~/hip-dev` is the **FROZEN DEMO**, which CLAUDE.md lists as a
NOT-pre-authorized class. It is touched here **only because Bill's dispatch names
it explicitly.**

---

## A — HANDOFF COUNTS, CONFIRMED LIVE

HA-77's numbers were right: **8 / 7 / 2**.

| tree | files | executable sites | prose-only sites |
|---|---|---|---|
| `~/hip-dev` | **8** | `voice_orch.py:161` (CORE), `:345` (cost key), `epistemic_record.py:111`, `generate_corpus.py:64`, `demo.html:120` | `config.yaml:77`, 2 evidence JSONs, 1 demo-script fixture |
| `~/hip-cutover-demo` | **7** | `voice_orch.py:165`, `:427`, `epistemic_record.py:156`, `generate_corpus.py:64`, `demo.html:120` | `config.yaml:77`, 2 evidence JSONs |
| `~/hip-harness` | **2** | `voice_orch.py:138`, `:252` | `config.yaml:65` |

Only **CORE** is affected anywhere. MID (`llama-3.1-8b-instant`) is unaffected.

## B — CENTRALIZED: MIRRORED, NOT SHARED

**No tree could cleanly read HA-77's mechanism, and the reason is worth stating.**
`hip-dev` and `hip-cutover-demo` are worktrees on **different branches** — each
materializes its own branch's files, so `harness/groq_models.py` (which lives on
`roadmap`/`main`) simply is not present in them. `hip-harness` is a **separate
repository** (TD-132). So the mechanism is copied into each tree, and **that
duplication is itself the thing TD-132 exists to record.**

Per tree: `config.yaml` gains the `models.groq` block; `harness/groq_models.py`
reads it and **refuses rather than defaulting**; `voice_orch`'s
`GROQ_MODEL_MID/CORE` resolve from it. Where the surface exists, so do
`epistemic_record`'s governance roster (**derived**, since it decides OFF-NET vs
ON-NET), `generate_corpus`'s `GENERATOR_MODEL`, and `demo.html`'s browser roster.

**Residual executable literals after the sweep: 0 in all three trees** (AST-
verified). Remaining mentions are prose; three comments that *described current
routing wrongly* were corrected rather than left to mislead.

## C — SWAP + PROVE

| tree | config point | live smoke (CORE) | twin | eval/ differential |
|---|---|---|---|---|
| `~/hip-dev` | `config.yaml models.groq` + `harness/groq_models.py` | **HTTP OK**, `served_by=openai/gpt-oss-120b` | **15 passed** | 0 passed/19 err → **15 passed/19 err** |
| `~/hip-cutover-demo` | same | **HTTP OK** | **15 passed** | 7 failed/371/19 err → **7 failed/386/19 err** |
| `~/hip-harness` | same | **HTTP OK** | **9 passed, 6 skipped** | 9 passed/6 skipped |

**hip-cutover-demo: +15 = exactly this dispatch's twin, ZERO new failures, ZERO
new errors.** **hip-dev**: the 19 errors are pre-existing oracle errors (that
tree's `eval/` had **zero** passing tests before); this dispatch adds the only
ones it has. **hip-harness**'s 6 skips are surfaces that genuinely do not exist
there (no `demo.html`, no `epistemic_record`) — skipping because a surface is
ABSENT is a different statement from passing, and the count shows it.

**Wiring verified without firing anything:** `py_compile` clean; the three modules
import cleanly in every tree; and `voice_orch`'s groq import is **module-level
with no function-level re-import** — the HA-65 `UnboundLocalError` class, checked
by AST because that exact edit shape caused it once already.

### NOT RUN, DELIBERATELY

`scripts/demo_integrity_battery.py` is each demo tree's own full battery. **Its
own docstring says it fires `/api/text-query` turns with "one reset+seed at the
start" — it RESETS THE DEMO GRAPH**, which is precisely what Part D forbids. It
is named here as unrun rather than run and reported as a number.

## D — DEMO IMPACT: NONE, AND STRUCTURALLY SO

The **offered** deck is three files (`server/demo_dashboard.py:1448-1453`):

| file | turns |
|---|---|
| `boundary_and_consent__v20260801_1535.json` | 4 — edge 2, mid 1, frontier 1 |
| `speaker_isolation__v20260729_1600.json` | 7 — edge 7 |
| `trust_ladder__v20260729_1453.json` | 5 — edge 5 |
| **total** | **16 — edge 14, mid 1, frontier 1, CORE 0** |

**Census unchanged from VD-57.** The deck routes **no CORE turn**, so a CORE
model swap cannot move its visible behaviour. Two *superseded, unoffered* deck
versions do each contain a core turn; they are not what the demo loads, and they
were left untouched.

## FOUND AND FIXED, BEYOND THE DECOMMISSION

**`~/hip-harness`'s fact-change detector was pinned to
`meta-llama/llama-4-scout-17b-16e-instruct`, which Groq DOES NOT SERVE TODAY** —
confirmed by a live call returning `model_not_found`. That detector has been dead
**independently of the 08-16 decommission**, and nothing surfaced it because
nothing exercises that tree's detector.

Centralizing forced it to take a config value. It is now `openai/gpt-oss-20b` —
the standard every other tree uses — verified live (HTTP OK). Flagged rather than
folded in silently, because it is a behaviour change to a tree TD-132 already
describes as a diverging second implementation.

## NOT DONE

**The CORE token rate is unchanged in all three trees.** It is keyed by the
constant so the swap carried automatically, but the rate is still
`llama-3.3-70b-versatile`'s. Repricing `openai/gpt-oss-120b` is a measurement and
Bill's to rule on. Marked `RATE STALE` in source. **Same open item as HA-77 — it
now spans five trees.**

## VERIFIED

**Watched run:** the live model list and a live `model_not_found` for the scout
model; CORE+MID smoke on all three trees; the twin on all five trees; the
`eval/` before/after differential via `git stash` on the two demo trees;
`py_compile` and import checks; the AST check for function-level import
shadowing; the deck census read from the offered files.

**Reasoned about:** that the swap cannot move demo behaviour — argued from the
offered deck's tier census (CORE 0), **not** from running the deck, which Part D
forbids.

## CLAIM IMPACT

**CLAIM IMPACT: none.**

## OPEN — NEEDS BILL

1. **CORE token rate repricing**, now across **five** trees.
2. **`~/hip-harness`'s detector was silently dead** and nobody noticed — a
   TD-132 symptom: a diverging second implementation nothing exercises.
3. **Each demo tree's own binding battery is destructive** (reset+seed), so a
   config-only change cannot be proven against it without resetting the demo
   graph. Worth a non-destructive smoke mode.
4. **The estate is now swept** — five trees, all on `openai/gpt-oss-120b`.
