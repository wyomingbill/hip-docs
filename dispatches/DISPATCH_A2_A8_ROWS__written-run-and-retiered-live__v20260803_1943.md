# DISPATCH_A2_A8_ROWS
Status: BUILT
Reconciled-Against: 2026-08-03 (D-145; parent `317212a`)

**TYPE:** BUILD (acceptance rows) + TIER CHANGE

**REQ:** `REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`,
**R2** (row A2) and **R8** (row A8). Plan: `REQ_CEILING_ACCEPTANCE__…v20260801_0617.md`.

## 1. READ FIRST — the filed rows, and whether their UNWRITABLE reasons are closed

| Row | Row text as filed | Filed UNWRITABLE reason | Closed? |
|---|---|---|---|
| **A2** (R2) | "Typed inference permit with declared inputs/predicates" | "New permit type + registry + enforcement at the abstraction boundary" — cost column; authorization "None — pure build" | **YES.** `harness/inference_permit.py` (D-130, `dec92f3`): twelve-field `InferencePermit`, `ABSTRACTION_PERMIT`, `EVIDENCE_FLOOR=2`; enforced in `create_fact_node` on every `origin="derivation"` write (allowed_input_attributes, required_evidence_rule) |
| **A8** (R8) | "Representation classes incl. `UNKNOWN_HIGH_RISK`" | "New enum + write-time validation; **verified absent at HEAD**" | **YES.** `harness/representation_class.py` (D-140, `bc56fc4`): fourteen classes incl. `UNKNOWN_HIGH_RISK`; `create_fact_node` classifies every durable write before persistence and fails closed |

Both verified by reading the code, not the dispatch's assertion. Neither STOP fired.

Note on the ordering the acceptance plan predicted: A10's own comment said representation
and permit were "BLOCKED ON ABSENT SUBSTRATE… A8/A2 both UNWRITABLE." That premise is what
D-130 and D-140 closed; A10 itself is untouched by this dispatch and stays STRICT XFAIL.

## 2. THE ROWS — written against the real path

`eval/test_ceiling_inference.py::test_ceil_a2_*` (5 cases) and
`eval/test_ceiling_representation.py::test_ceil_a8_*` (5 cases), CEIL-A\<N\> namespace,
D-87 standard.

**Asserted against `memory_engine.store.create_fact_node` with a recording transaction —
NOT against D-130's or D-140's standalone probe scripts**, per the dispatch. Both rows apply
`_a10_enforced_at_creator`'s counting rule: **a check counts only if the creator RAISES and
issues NO write**, because a creator that raises after writing has enforced nothing. Every
principal case asserts the refusal AND `not wrote`.

**A2 principals** — an off-permit input attribute in `source_categories` is refused
(message names `allowed_input_attributes`); a derivation naming fewer than `EVIDENCE_FLOOR`
source facts is refused (message names `required_evidence_rule`).

**A8 principals** — an artifact the classifier cannot place (`UNKNOWN_HIGH_RISK`) is refused
for durable persistence; a classifiable artifact is **stamped** by the creator
(`medication` → `HEALTH_CLAIM`, read out of the recorded write parameters, not inferred from
the absence of an exception).

**EXECUTED fault twins — broken implementations, not guards.** Each replaces the mechanism
and asserts the outcome FLIPS. Observed directly (probe output, both directions):

```
A2 normal        -> refused=True  wrote=False  permit_msg=True
A2 BROKEN permit -> refused=False wrote=True   permit_msg=False
A8 normal            -> refused=True  wrote=False  unknown_msg=True
A8 BROKEN classifier -> refused=False wrote=True   unknown_msg=False
```

The twins' assertions were STRENGTHENED after that probe: they now assert
`not refused and wrote` — the flip itself — rather than the weaker "not refused on these
grounds", which could have passed vacuously if some unrelated creator rule had refused.

**Anti-vacuity.** A2: a conforming derivation is not refused on permit grounds, and the
permit declares non-empty input/output sets with an evidence floor ≥ 2. A8: not everything
classifies to the fail-closed bucket (`medication`→HEALTH_CLAIM, `employer`→ORDINARY_CLAIM)
— without this, the fail-closed row would pass for free — and the class vocabulary is
non-degenerate.

## 3. RE-TIERED IN THE SAME EDIT

`REQ_CEILING_ACCEPTANCE` updated in the same commit as the rows (the A1/D-100 rule: a tier
and its predicate move together or the suite goes red): tier counts **LIVE 5→7**,
**UNWRITABLE 16→14**; both UNWRITABLE table rows annotated with what closed them; new
**§7.7** recording the re-tiering, the closure evidence, the twins' observed flips, and the
passing-row-does-not-carry-its-requirement statement.

## 4. RESULTS — each row individually

```
eval/test_ceiling_inference.py::test_ceil_a2_off_permit_input_attribute_is_refused_with_no_write  PASSED
eval/test_ceiling_inference.py::test_ceil_a2_evidence_floor_is_refused_with_no_write              PASSED
eval/test_ceiling_inference.py::test_ceil_a2_fault_twin_broken_permit_goes_red                    PASSED
eval/test_ceiling_inference.py::test_ceil_a2_anti_vacuity_conforming_derivation_is_not_permit_refused PASSED
eval/test_ceiling_inference.py::test_ceil_a2_anti_vacuity_permit_substrate_exists                 PASSED
eval/test_ceiling_representation.py::test_ceil_a8_unknown_high_risk_is_refused_with_no_write      PASSED
eval/test_ceiling_representation.py::test_ceil_a8_classified_artifact_is_stamped_by_the_creator   PASSED
eval/test_ceiling_representation.py::test_ceil_a8_fault_twin_broken_classifier_goes_red           PASSED
eval/test_ceiling_representation.py::test_ceil_a8_anti_vacuity_not_everything_is_unknown          PASSED
eval/test_ceiling_representation.py::test_ceil_a8_anti_vacuity_class_vocabulary_exists            PASSED
```

Combined file run: **29 passed, 1 xfailed** (the xfail is A10, unchanged and still strict).

## 5. A PASSING ROW DOES NOT CARRY ITS REQUIREMENT

**A2 PASSES. A8 PASSES. R2, R8 and R10 remain NOT MET.** R2 was ruled NOT MET at D-143
(scope gap — R5/R6/R7 unaddressed); R8 was ruled NOT MET at D-144 (silent absorption); R10
stays NOT MET and its row A10 is untouched here, still STRICT XFAIL. Nothing in this
dispatch rules anything, and an executed acceptance row is evidence for a ruling, never a
substitute for one. This is the fifth instance of the distinction on file — A30/R30,
A18/R18, A12/R12, A1/R1, and now A2·A8.

## 6. HARNESS

- **Standing batteries: 390 passed, 8 xfailed** (up from 380 — the ten new cases).
- **`--layer 7`: L7 27/27**, L7V2 27/28 (one opt-in skip), **AUDIT 8/8**, four-part-roster
  PASS (59 checks), COVERAGE-GRID-RATCHET PASS, **RATCHET PASS — no scenario regressed**.
- **The five ABSOLUTE checks, read individually from the log — plus CS1, six in total:**
  **OB6 PASS · G0 PASS · PSA1 PASS · CTX-STRIP PASS · LI1 PASS · CS1 PASS.**
- **Memory harness: 13/17, TWICE, byte-identical** — failures exactly
  {MEM-115, MEM-116, MEM-117, MEM-118}. **Inside the 13–15/17 pin, failures a subset of the
  permitted set, and NOT the 16/17 STOP.** At the pin's FLOOR, and MEM-118 is newly red
  against D-127's 14/17→15/17.

  **Investigated, not waved past.** Hypothesis: D-140's new representation classifier now
  runs on every durable write and could be refusing harness writes. **Killed by reading the
  failure text** — MEM-117 reports `trust level is 'CORROBORATED', expected ASSERTED` and
  MEM-118 reports `delta transition='unresolved'`; neither is a classifier refusal. Both are
  graph-state-dependent live-write scenarios, deterministic across two runs, on the dev
  graph this lane shares with the cutover demo lane that has been running today. This
  dispatch added test files and edited one REQ doc — **no product code** — so it cannot be
  the cause. Reported as a finding; chasing it is its own dispatch.

## PROCESS NOTES

- **Lock taken LATE, and recorded rather than hidden.** The gate read `.hip-lock` at the
  start and found it free, but the noclobber TAKE was not performed until 19:43:52, after
  the rows were written and run. The write window was unlocked. No other lane wrote to this
  checkout in that window (verified: `git status` unchanged apart from my files), and the
  lock was free at both readings — but the preamble says take it, and I took it late. Same
  class of miss D-114 recorded.
- Tree was **reconciled before work started**: `0 ahead / 0 behind` origin, unlike D-140 and
  D-142 which both stopped on an unreconciled tree.
- Committed AROUND the cutover lane's WIP (dirty `docs/INDEX.md` + five untracked dispatch
  docs, incl. D-140's R8 survey): explicit pathspecs, surgical INDEX stage, verified after.
- Repo `.env.dev` only.

## OPEN

- **MEM-118 (and MEM-117) at the pin floor** — deterministic, not caused by this dispatch,
  cause not established. Needs its own dispatch; the dev-graph sharing with the cutover lane
  is the first place to look.
- A10 stays STRICT XFAIL and R10 stays NOT MET; A10 flips only when someone rules R2 and R8,
  not when their rows pass.
- Nothing ruled.
