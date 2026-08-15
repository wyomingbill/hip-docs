<!-- STATUS: BUILT -->
<!-- RECONCILED-AGAINST: memory_engine/__init__.py + api.py + store.py + consolidate.py + interpreter.py + recall.py (all present, beyond scaffold described at delivery); eval/memory_harness.py (Phase A-D scenarios present) — 2026-07-05 -->

# Memory Engine Spec — Delivery Report

**Commit:** `76d5228` — `docs/MEMORY_ENGINE_SPEC.md` committed to main in ~/hip-dev,
plus the optional scaffold. Gate re-ran 6/6 green after the scaffold; hip-harness
untouched.

## What the spec covers

**Frozen interface (§1)** — the engine exposes one function,
`candidate_facts(member, query)`, returning the exact fact shape
`read_user_facts()` returns today; the pipeline then runs `resolve_subject` and
`apply_injection_contract` unchanged. The swap at integration is one import line.
Optional additive annotation keys (`unresolved`, `derived`, `tier`, `retired`,
`confirm_when_relevant`) carry engine metadata, and scenario MEM-100 asserts the
contract produces a byte-identical `InjectionResult` with or without them —
proving the annotations can't change what disclosure permits. Every preserved
invariant is mapped to the specific harness scenario that asserts it, including
the structural one: cold facts are excluded by the tier filter in the candidate
query itself, so there is no code path from a live turn to a cold row (MEM-107
seeds a cold fact that would pass every contract rule and asserts it never
reaches the contract).

**Model/code boundary (§2)** — all model judgment lives behind a single
`Interpreter` protocol (`classify_write`, `classify_query_temporality`,
`reconcile`, `abstract`), each call bounded, logged, schema-validated, and
per-method swappable, extending the existing `fact_change.py` prompt/parse path.
The sliding boundary is specced with concrete migration examples (e.g.
MULTI_VALUED overrides folding from code into the prompt without a type change),
and the permanent floors — store, temporal filters, contract, audit, tier
executor — are named as never-migrate. Fine-tuning appears exactly once, as a
Phase-C per-inference cost option for write-state classification, contingent on
measured economics.

**Write model (§3)** — full bitemporal schema on top of the existing `valid_to`:
valid time vs. record time, so CORRECT (belief was always wrong;
`record_closed_at` + `closed_reason=error`) is forever distinguishable from
SUPERSEDE (fact ceased being true). UNRESOLVED is a first-class state with a
confirm-when-relevant marker and code-computed salience; a low-confidence model
decision on any state downgrades to UNRESOLVED. Confidence moves both directions
through clamped, logged transitions — only human confirmation jumps straight to
high.

**Operations, tiers, resolution (§4–§8)** — ENCODE/RETRIEVE/CONSOLIDATE/RECALL
as specified; retrieval fails closed to "current" if temporality classification
fails; the REM pass is batched Core-tier, logged, reversible, with a nightly
compute estimate. Fluid confirmation fires from the retrieval-time marker; the
intentional session is gated by a deterministic salience formula (no nagging
below threshold); confirmation authority mirrors the ownership model so the
colloquy is governed by the same structure as disclosure.

**Harness and phases (§9–§11)** — `memory_harness.py` with permanent scenarios
MEM-100..115 covering all listed seed cases, added to `gate_check.sh` as check 7
only at swap-in. Build order A→E (substrate → retrieve → consolidation →
cold/recall → confirmation) with dependency rationale and per-phase eng-day +
compute costs. The honest-limits section states plainly that a
confidently-wrong write-time classification won't self-flag, and traces exactly
which mechanisms (consolidation revisit, contradiction-loosening, fluid
confirmation, salience escalation) catch it — and the residual case that none
do.

**Scaffold** — `memory_engine/__init__.py` (namespace + module layout docstring,
zero live-pipeline imports) and `eval/memory_harness.py` (exits 0, prints
scaffold notice, deliberately not wired into the gate).

## Open observation

Fresh `issue_INT-001_*.json` files from today (22:18Z) appeared in
`eval/integration_issues/` — INT-001 appears to have failed in some run after
the gate pass. Worth a look before the next promotion; the gate run done just
before commit was green, so it may have been a transient or an ad-hoc run
against unseeded state.
