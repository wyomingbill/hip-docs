# DISPATCH_R18_CASCADE
Status: BUILT
Reconciled-Against: 8025e10 (HEAD at dispatch start)
REQ: `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2129.md`, R18 (authority verified via `docs/INDEX.md` + `LATEST_REQ_STRUCTURAL_CEILING.md` symlink, both resolving to v20260731_2129)
Dispatch: D-81, 2026-08-01
Acceptance row: A18
**Status proposed: NONE. R18 is NOT self-ruled MET. See "Why R18 is not MET" below.**

## What was asked

Build R18, the `derived_from` cascade. The dispatch stated two rules, both of
which match the REQ text verbatim — no disagreement, so no STOP:

1. Recompute from still-authorized parents, else invalidate immediately.
2. A child SHALL NOT survive merely because another parent still exists.

## Step 2 — the defect, confirmed at HEAD before any change

`derived_from` was **written** (`memory_engine/consolidate.py:477, 525, 533`) and
**read extensively** (`truth_layer/queries.py` at lines 88, 228, 306, 365, 455,
461, 476, 494, 502, 505, 510, 534, 552, 583, 585) — but every read is lineage
DISPLAY or traversal. None is invalidation. `retract_fact` and `_retract_one` in
`harness/extraction_queue.py` had **no cascade at all**: grepping their bodies for
`derived|cascade|child` returned nothing.

The traversal needed to fix it already existed, used only for display, at
`truth_layer/queries.py:505`:

```
MATCH (f:Fact) WHERE $fid IN f.derived_from
```

So this was not a missing capability. It was a capability wired to the read path
and not to the write path.

## Step 4 — the pre-change inventory (the gate)

Run read-only against live Neo4j **before** any change, per the dispatch's
STOP condition:

| Measure | Value |
|---|---|
| total `:Fact` nodes (incl. closed) | 12 |
| `derived = true` | 1 |
| `derived = true` AND `derived_from` populated | **0** |
| derived children with a retracted parent | **0 — the defect had never fired** |
| dangling `derived_from` refs (parent row absent) | 0 |

**No STOP condition.** No retracted-parent children existed, so nothing had to be
adjudicated before building.

The inventory also produced a finding the dispatch did not ask for: the reason
the defect never fired is that **no lineage was ever written**. Filed as TD-141.
The cascade is therefore correct and currently **inert against live data** — it
cannot reach a child whose `derived_from` is empty. "The cascade passes its
battery" and "the graph is protected" are separate claims and are recorded here
as separate claims.

## What was built

**`harness/derivation_cascade.py`** (new). `cascade_from_parents` walks
descendants to a fixpoint and closes each one; `cascade_from_closed` recovers
fact_ids for a retraction identified by `(attribute, owner[, subject])`, which is
how the retract path actually closes facts.

Three decisions that are **stricter** than a naive reading of R18's pseudocode,
each deliberate:

1. **Recompute is not attempted synchronously.** Re-deriving needs an LLM
   abstraction call. Inside the retraction path, a timeout or refusal would leave
   the child ACTIVE — precisely what R18 forbids. So the child is closed FIRST
   and unconditionally, and recompute eligibility is recorded on the closed node
   (`cascade_recompute_eligible`, `cascade_recompute_from`) for a later pass.
   An invalidated-then-re-derived child is correct; a live child whose recompute
   failed is not. **That later pass does not exist yet — TD-140.**
2. **Unknown parents count as unauthorized.** A `derived_from` entry naming a
   nonexistent fact cannot be shown to still authorize anything, so it does not
   count toward survival.
3. **Cascade runs in the caller's transaction.** A committed retraction with a
   separately-failed cascade would leave children active. `retract_fact` was
   converted from bare `sess.run` to `sess.execute_write` for this reason.

Closed children are stamped `closed_by = 'lineage_cascade'`, distinguishable in
the audit record from a direct retraction. `MAX_CASCADE_DEPTH = 32` stops a
lineage cycle from hanging the retract path.

## Step 5 — A18, wired LIVE

**Correction to a dispatch premise:** the dispatch said to flip A18 from XFAIL to
LIVE. There was no XFAIL to flip — `grep A18 eval/ scripts/` returned nothing.
REQ_CEILING_ACCEPTANCE (D-77) *classified* A18 as STRICT XFAIL but never wrote
it; only A29/A30 were ever wired (D-75). A18 was written LIVE directly.

`eval/test_derivation_cascade.py`, 18 passed / 2 xfailed, registered in
`scripts/run_harness.sh` as a standing battery (44 → 75 → now 93 cases across the
battery block).

**The fault twin is the load-bearing part.** `_surviving_parent_cascade`
implements the plausible wrong rule — invalidate only once ALL parents are gone —
and every requirement-carrying assertion runs against both it and the real
cascade.

**A flaw the twin caught in my own test.** The transitivity case was first
written with a single-parent chain, and the twin PASSED it: with one parent,
"any parent gone" and "all parents gone" coincide, so the case discriminated
nothing and would have xfailed vacuously. It was rewritten with a surviving
second parent, which is what makes the twin diverge. This is the whole argument
for asserting that the twin is *still broken* before calling `pytest.xfail` —
without that assertion the vacuity would have shipped looking green.

Coverage of the four HARNESS DISCIPLINE requirements:

- **Fault twin** — yes, parametrized, proven discriminating in both directions.
- **Ground-truth fixture** — synthesized lineage graphs, declared in-file. Honest
  limit: constructed, not human-verified from production data.
- **Coverage entry** — pytest batteries are not in the AUDIT block's enumeration
  (it enumerates harness scenarios); registration is via `run_harness.sh`, the
  precedent A29/A30 set at D-75.
- **Metamorphic wrapper** — present, but NOT a rewording wrapper: nothing here
  consumes an utterance. The meaning-preserving transformation available on this
  input is ORDER, so the wrapper asserts the outcome is invariant under
  permutation of both the lineage list and the retracted-root list. If either
  changed the outcome, a child's fate would rest on write order.

## Known limitation of the battery, stated rather than buried

The battery runs against a **simulated** graph (`FakeTx`), not live Neo4j, because
testing a missing cascade requires constructing multi-level lineage, mixed
retracted/active parents, and a cycle on demand — which against live Neo4j means
either mutating the frozen demo graph (forbidden) or standing up a throwaway DB
(not available here). A battery that silently skips when the DB is absent is a
check that cannot be shown RED on command, which REQ_CEILING_ACCEPTANCE names as
disqualifying.

The gap that leaves — whether the Python simulation faithfully models the Cypher —
was closed separately: **all 5 cascade queries were validated against live Neo4j
with `EXPLAIN`** (parsed and planned by the real planner, not executed; graph
untouched, re-verified at 12 facts after). That proves syntax and semantics
against the real schema. It does not prove execution semantics, and is not
claimed to.

## Step 6 — harness

`--full` was **refused by the harness's own TD-129 guard** (needs ≥2GB free, 0.37GB
available) — not skipped by choice. I did not free memory by killing processes,
with the demo frozen and the standing no-reboot rule in force. CLAUDE.md item 12
wants `--full`; this is a machine-state block on satisfying it and is flagged
here rather than papered over.

`--layer 7` ran clean:

```
== AUDIT:  8/8     (0 flaked, 0 skipped)
== DISC:   1/1
== L7:     27/27   (0 flaked, 0 skipped)
== L7V2:   27/28   (0 flaked, 1 skipped — CT-OUTPUT-GAP, opt-in by design)
== SCHEMA: 1/1     == VOICE: 1/1
RATCHET PASS — no scenario regressed vs baseline.
```

**No ABSOLUTE-tier check went red.** All six standing batteries green (88 cases).
The only `FAIL` string in the log is a pre-existing `RENDER_FAILED` flag on
`whitepaper/archive/HIP_White_Paper_Augmented.docx`, unrelated to this change.

## Why R18 is NOT MET — three named gaps

Not a self-ruling. Bill rules.

- **TD-139** — R18's 11-field lineage metadata block does not exist. A `:Fact`
  carries `derived` and `derived_from`: **2 of 11**, and `parent_artifact_ids`
  only by rename. So R18's "erase it according to its storage class" is satisfied
  only in the weak sense that closing removes from retrieval — nothing erases by
  storage class, because no storage class is recorded.
- **TD-140** — the recompute branch is deferred, never executed. Every cascaded
  child is invalidated and none is recomputed. Stricter than R18 in the safe
  direction, under-delivering it in the useful one.
- **TD-141** — the live graph's one derived fact has empty `derived_from`,
  violating R18's opening sentence in *data*. The cascade is inert against it.

R19 (embeddings, summaries, and indexes as governed derivatives) is untouched by
this dispatch — the cascade closes `:Fact` nodes and does not reach embeddings.

## Files changed

| File | Change |
|---|---|
| `harness/derivation_cascade.py` | NEW — the cascade |
| `harness/extraction_queue.py` | cascade hooked into both retract paths; `retract_fact` made transactional |
| `eval/test_derivation_cascade.py` | NEW — A18, 18 passed / 2 xfailed, with fault twin + metamorphic wrapper |
| `scripts/run_harness.sh` | battery registered |
| `docs/techdebt/DEBT_REGISTER__v20260731_2300.md` | TD-139, TD-140, TD-141 |
