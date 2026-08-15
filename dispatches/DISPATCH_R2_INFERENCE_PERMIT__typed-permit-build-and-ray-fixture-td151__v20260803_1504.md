# DISPATCH_R2_INFERENCE_PERMIT
Status: BUILT
Reconciled-Against: dec92f3587d795f28159a32e4e760ae241112c15

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`,
R2 (typed inference permit). §16 amended in this same commit — "R2 — reported, not ruled
(D-130)".

## THE ASK

Dispatch text, verbatim:

```
=== D-130 | ~/hip-roadmap, roadmap | R2: the typed inference permit ===
Gate: expect bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap / roadmap. Mismatch -> STOP.
Tree carries the cutover lane's WIP — commit AROUND it, explicit pathspecs.
Source the REPO .env.dev only. LOCK: read first, noclobber take.
YOU OWN THE GRAPH AND THE HARNESS. Lane B is docs-only in its own worktree.

GOVERNING REQ: REQ_STRUCTURAL_CEILING R2.

1. THE GAP, from D-97: interpreter.abstract()'s prompt constrains the emitted attribute NOT
   AT ALL. HIP controls an inference's TRUST, not its SUBJECT MATTER. R2 is the fix, and it
   also unblocks R10 — the ceiling REQ's one NOT MET.

2. SURVEY FIRST, report before changing anything:
   a. R2's text as filed. Read it.
   b. EVERY call path that reaches abstract() or any other model call that can produce a
      durable claim. R2 governs what may be inferred, so find every inference site.
   c. Which permit fields HIP can populate honestly today and which cannot — same discipline
      as D-105's lineage block, where three of eleven stayed absent and were asserted absent.
   STOP AND REPORT if a required field cannot be populated honestly. An invented permit field
   is worse than an absent one.

3. THEN BUILD what can be built honestly. Enforce where a derived claim becomes DURABLE, not
   inside the model call. Absent fields stay absent and are asserted absent by a standing test.

4. ACCEPTANCE per D-87: fault twin, anti-vacuity. A2 is UNWRITABLE for want of this build —
   report whether it becomes writable. DO NOT re-tier it.

5. Run --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17, failures a subset of
   {115,116,117,118}. 16/17 is a STOP.
6. Rule nothing MET. Lock, commit with explicit pathspecs, push.
7. PRINT THE FULL REPORT TO THE TERMINAL.
```

Mid-dispatch, the user also directed handling of a collateral finding (see WHAT WAS FOUND /
TD-151 below): approved reseeding the D9 demo fixture and fixing the underlying test-cleanup
gap, then imposed two verification conditions (byte-identical value check; confirm the
anti-vacuity test goes green for the right reason) and asked the cleanup-gap scope question
(which of MEM-116/117/118 lacked cleanup, whether any other scenario shares the shape) plus a
standing instruction to record the whole thing as a TD if none already existed.

## WHAT WAS DONE

1. Gate checked (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap / roadmap) — matched.
2. `.hip-lock` read first, then taken (noclobber): `holder: D-130 (R2: the typed inference
   permit), session: sonnet5, taken: 2026-08-03T15:20:00-0600`.
3. Read R2's text in `REQ_STRUCTURAL_CEILING` (lines 225-247 of the v20260802_2205 filing).
4. Traced every call path reaching a model call capable of producing a durable claim;
   confirmed `_abstract_pass` → `interpreter.abstract()` is the only unconstrained one.
5. Accounted for all 12 permit fields against what the codebase can honestly support today.
   No field required inventing a value — no STOP fired.
6. Built `harness/inference_permit.py` (new file) and wired its enforcement into
   `memory_engine/store.py::create_fact_node`, scoped to `origin=="derivation"`.
7. Raised `_abstract_pass`'s candidate-episode floor in `memory_engine/consolidate.py` to
   match the permit's `required_evidence_rule`.
8. Fixed four pre-existing test/fixture call sites that needed `derived_from`/
   `source_categories` once the new checks landed: `eval/test_ceiling_inference.py`,
   `eval/test_write_origins.py`, `eval/harnesslib/layer7_crypto.py`'s `_OB4Probe`, and
   `eval/memory_harness.py`'s MEM-111 fixture (`attribute="activity"` → `"preference"`,
   `"activity"` not being a real canonical attribute).
9. Ran `--layer 7`; a new, unrelated failure appeared
   (`eval/test_structural_refusal.py::test_sref_graph_known_set_is_not_vacuous`). Root-caused
   it (see WHAT WAS FOUND) rather than proceeding past it.
10. Surfaced the finding and a proposed fix to the user before taking any live-graph-mutating
    action (the fix required a live write, which the tool-permission classifier itself also
    gated); the user approved reseeding D9 and fixing the cleanup gap.
11. Reseeded D9 via `scripts.demo_seed._seed_one` (the seed script's own code path and
    `FIXTURES` tuple), verified the restored value byte-identical to the source by decrypting
    it, and reconfirmed `graph_subject_ids()` and `test_structural_refusal.py` both correct
    for the right reason.
12. Patched `eval/memory_harness.py`: added `_restore_ray_medication_fixture()` and wired it
    into all three of MEM-116/117/118's `finally` blocks; checked no other memory-harness
    scenario shares the same live-pipeline-against-a-fixture shape.
13. Filed TD-151 in the debt register (new versioned file, `LATEST_DEBT` repointed).
14. Recorded R2 in `REQ_STRUCTURAL_CEILING` §16 as "reported, not ruled" — including the A2
    writability finding, explicitly not re-tiering A10.
15. Ran `--layer 7` (clean) and `eval.memory_harness` four consecutive times to confirm
    stability of both fixes.
16. Staged by explicit pathspec (10 files), leaving the cutover lane's `docs/INDEX.md` and its
    four untracked `DISPATCH_DEMO_CUTOVER_*.md` files completely untouched — confirmed via
    `git status` before and after.
17. Committed, pushed to `origin/roadmap`, released the lock.

## WHAT WAS FOUND

**R2's scope (item 2b).** `memory_engine/consolidate.py::_abstract_pass` calls
`interpreter.abstract()` (the live `GroqInterpreter`), which then reaches
`_write_derived_node` → `memory_engine/store.py::create_fact_node` (D-96's single
materialization point) with a model-chosen attribute. This is the ONLY durable-inference site
with an unconstrained output. Confirmed out of scope: `harness/fact_change.py` (schema-enum +
runtime canonical-attribute check), `write_frontier_fact` (hardcoded attribute, never
model-chosen), `Interpreter.reconcile()`/`classify_write()` (operate on an already-fixed
attribute/subject pair).

**Permit field accounting (item 2c).** 9 of 12 fields populated honestly: `permit_id`,
`version`, `allowed_output_attributes` (= `harness/write_origins.py::DERIVABLE_ATTRIBUTES`),
`allowed_input_attributes` (= `harness/extraction_queue.py::CANONICAL_ATTRIBUTES`),
`allowed_subject_roles`, `audience_projection`, `required_evidence_rule`, `required_review`,
`actionability`. 3 stay absent, asserted `None` on the dataclass, not invented:
`prohibited_input_classes` (no input-class taxonomy exists), `purpose_id` (no purpose
vocabulary anywhere in the codebase — blocked on R23), `retention_policy` (no retention
mechanism exists — R21 NOT MET). These three match D-105's identical findings for R18's
`purpose_id`/`retention_deadline`/`policy_version` exactly.

**A2 (item 4).** R10's D-100 ruling (`REQ_STRUCTURAL_CEILING` §16) named R2's absence as the
reason A2 — one of R10's four `create_fact_node` revalidations — was UNWRITABLE. This build
makes A2 writable: a typed permit now exists and is enforced at the same materialization
point origin/registry checks already run at. NOT re-tiered — `eval/test_ceiling_inference.py`
A10 stays `xfail(strict=True)`, unchanged. A8 (R8's representation classes) remains separately
absent; A10 stays blocked on that regardless of R2.

**TD-151, the collateral finding.** `scripts/demo_seed.py`'s D9 fixture is a real fact
(`owner=maya, subject=ray, attribute=medication, value="metformin 500mg twice daily"`,
`session_id="demo-seed"`). `eval/memory_harness.py`'s MEM-116/117/118 (pre-existing, not
introduced by this dispatch) exercise the live pipeline
(`scripts.text_demo.run_query("Ray switched from metformin to Jardiance 10mg", "maya")`)
against this exact key to test supersede detection. Each test's `finally` cleanup
(`_delete_facts_by_session` at `eval/memory_harness.py:103-108`, matching on the test's own
randomized `sid`) never reaches the live pipeline's write, which lands under a FIXED session
id the pipeline derives internally (`"text-maya"`). Compounding this,
`memory_engine/store.py::_tx_supersede`'s no-target branch (`target_fact_id=None`, lines
505-518) closes ALL active rows matching `(owner, subject, attribute)` in one query but
creates only one replacement fact. Three consecutive `eval.memory_harness` runs (verifying the
MEM-111 fixture fix, this dispatch) fully closed D9 with no active replacement. Direct graph
query confirmed: all 6 facts ever written on `(maya, ray, medication)` closed, several
`superseded_by` pointers naming fact_ids that no longer exist in the graph at all (created and
later deleted by a subsequent, equally-uncleaned run). Caught only by
`eval/test_structural_refusal.py::test_sref_graph_known_set_is_not_vacuous`
(`{"ray","dad"} <= graph_subject_ids()`) going red — an acceptance check for an ALREADY-MET
requirement (`REQ_STRUCTURAL_REFUSAL`, ruled MET at D-128) failed not from a regression, but
because a fixture eroded underneath it. Checked and confirmed: no other memory-harness
scenario shares this shape — MEM-115 and earlier use only randomized `memtest-*` owners with
no live-pipeline leg.

## VERIFIED

**Watched run:**
- `--layer 7` (final, post-fix): exit 0. Standing batteries: `323 passed, 8 xfailed`. RATCHET
  PASS. Log: `/tmp/d130_layer7_v4.log`.
- `python3 -m eval.memory_harness`, run 4 consecutive times post-fix: `13/17` every time,
  failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}` — within the pinned 13-15/17
  range, a full subset of the allowed four. 16/17 STOP condition did not fire on any run.
- `eval/test_structural_refusal.py` run directly via pytest: `7 passed` (was 1 error prior to
  the D9 reseed — collection succeeded once run under the same `PYTHONPATH`/
  `--import-mode=importlib` invocation `scripts/run_harness.sh` uses).
- D9 restore verified by direct decrypt: fetched the reseeded fact's `ciphertext`/
  `encrypted_dek`/`key_version`/`dyad_id`, decrypted via
  `harness.partition_crypto.decrypt_fact_value_for_caller`, compared byte-for-byte
  (`.encode()` equality) against `scripts.demo_seed.FIXTURES`'s own D9 tuple value —
  identical: `"metformin 500mg twice daily"`.
- `harness.role_resolution.graph_subject_ids()` called directly, before and after the reseed:
  before = `{bill, dad, household, maya, sam}` (ray absent); after =
  `{bill, dad, household, maya, ray, sam}` (ray present) — confirmed for the stated reason
  (D9's fixture fact active again), not coincidentally.
- The fault-twin checks for R2's new `create_fact_node` guards (off-allowlist
  `source_categories`, single-parent `derived_from`) executed live against a stub transaction
  recorder — both raise `ValueError` with no write issued.
- `git status` run immediately before and immediately after `git add`/`git commit` — confirmed
  the cutover lane's `docs/INDEX.md` (modified) and four untracked
  `DISPATCH_DEMO_CUTOVER_*.md` files were never staged.

**Reasoned about:**
- That `fact_change.py`/`write_frontier_fact`/`reconcile()`/`classify_write()` are out of R2's
  scope is a code-reading conclusion (schema/enum/hardcoded-value inspection), not something
  independently exercised live in this dispatch beyond the standing batteries that already
  cover those paths.
- The exact mechanism by which a `superseded_by` pointer came to name a fact_id absent from
  the graph (a later run's own uncleaned chain link closing an already-orphaned intermediate)
  is inferred from the sequence of `_tx_supersede` calls and the observed data, not captured
  by an instrumented trace of the specific transaction that did it.

## HASH

`dec92f3587d795f28159a32e4e760ae241112c15` — pushed to `origin/roadmap`
(`712e9cd..dec92f3`). 10 files changed: `harness/inference_permit.py` (new),
`memory_engine/store.py`, `memory_engine/consolidate.py`, `eval/test_ceiling_inference.py`,
`eval/test_write_origins.py`, `eval/harnesslib/layer7_crypto.py`, `eval/memory_harness.py`,
`docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`,
`docs/techdebt/DEBT_REGISTER__v20260803_1455.md` (new), `docs/techdebt/LATEST_DEBT.md`
(repointed).

## OPEN

- **R2 itself is not ruled** — reported only, per instruction ("rule nothing MET"). Bill's
  call.
- **A2/A10/R10 are not re-tiered.** Whether A10 should move off `xfail(strict=True)`, and
  whether R10's D-100 "NOT MET" ruling should be revisited now that permit enforcement exists,
  is explicitly left to a future dispatch.
- **A8 (R8's representation classes) remains unbuilt** — A10 stays blocked on it independent
  of R2's outcome.
- **`prohibited_input_classes`, `purpose_id`, `retention_policy` remain absent** — blocked on
  an input-class taxonomy, R23, and R21 respectively, in that order of dependency.
- **TD-151's exact transaction-level mechanism** for how an intermediate `superseded_by`
  target came to be deleted (as opposed to merely closed) was not instrumented live — the
  fix (restore + clean up on every future run) makes the question moot going forward but the
  precise sequence across the three prior harness runs was reconstructed, not captured.
- **This dispatch's report was originally printed in full to the terminal** per the dispatch's
  own item 7; this doc was written after the fact, in response to a mid-conversation change to
  the reporting protocol (full report to a dispatch doc under `docs/dispatches/`, terminal
  gets only the status line and path, going forward). `docs/INDEX.md` was deliberately NOT
  updated to register this doc, consistent with "commit AROUND" the cutover lane's WIP already
  sitting on that file — a follow-up dispatch should reconcile the INDEX registration for both
  this doc and TD-151's debt-register version bump.
