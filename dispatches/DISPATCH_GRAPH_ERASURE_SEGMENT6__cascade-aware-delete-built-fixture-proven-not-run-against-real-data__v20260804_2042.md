# DISPATCH_GRAPH_ERASURE_SEGMENT6
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (R17 Segment 6 — graph-side erasure mechanism), fixture-proven only,
no destructive authorization requested or used.

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R17 (ratified D-71). No amendment, no new REQ doc.

## THE ASK

Bill's instruction, verbatim:

```
=== D-R-169 | ~/hip-roadmap, roadmap | Segment 6: graph-side erasure, BUILD ONLY ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R17, ratified D-71.
Every production ledger write now emits v2 (D-R-168) and the erasure report is built
(D-R-167). What remains is the graph side: real DEK, row and embedding deletion.

SCOPE — READ THIS FIRST. Bill authorizes BUILDING AND PROVING the mechanism. He has
NOT authorized destroying any real data. Nothing in this dispatch may delete from the
live demo graph, the frozen demo's graph, or any real household data. Prove against
fixtures you create and tear down. If a step cannot be proven without destroying real
data, STOP AND REPORT rather than doing it.

1. SURVEY FIRST, report before building: what a complete graph-side erasure must reach
   — fact rows, DEKs, embeddings, derived children, audit entries, anything else — and
   for each, whether a deletion path exists today. D-160 found the only hard delete in
   the whole codebase is the demo reset. Confirm or correct that against HEAD.
2. BUILD THE ERASURE PATH against a fixture graph. It must be verifiable by the report
   built at D-R-167 — the report is the acceptance instrument, not a second story.
3. THE FAULT TWIN THAT MATTERS: an erasure that leaves something behind — a surviving
   embedding, an orphaned DEK, a derived child — must be CAUGHT BY THE REPORT, not
   pass. Prove that by executing it, not asserting it.
4. NAME WHAT ERASURE STILL CANNOT REACH after this builds. Backups, v1 ledger events,
   anything outside the graph. That list is the honest limit and belongs in the report,
   not in a footnote.
5. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
6. Rule nothing MET. STOP before any run against real data and report what authorization
   that would need.
```

## WHAT WAS DONE

1. Gate checked — matched, tree clean except another lane's own untouched WIP, HEAD in
   sync with `origin/roadmap`.
2. Surveyed what a complete graph-side erasure must reach, reading the real schema and
   write path directly: `memory_engine/store.py`'s `:Fact` node creation, `harness/
   extraction_queue.py`'s read/retract paths, `harness/derivation_cascade.py`'s R18
   cascade, and a fresh grep for embedding/vector/index code anywhere near `:Fact`.
3. Grepped the WHOLE codebase for every `DELETE`/`DETACH DELETE` to check D-160's own
   "the only hard delete... is the demo reset" claim against HEAD — found it
   incomplete: THREE hard-delete sites exist, not one (see WHAT WAS FOUND). Confirmed
   `scripts/cleanup_test_facts.py` predates D-160's own survey by six weeks (git log),
   so this was a real gap in that survey, not a later addition.
4. Confirmed `encrypted_dek`/`ciphertext` are properties ON the `:Fact` node itself
   (not a separate store, unlike the ledger's off-ledger payloads) — read directly
   from `read_user_facts`'s own `RETURN` clause and `_new_node_props`'s full field
   list — meaning R17 steps 2 and 3 collapse into one action for this artifact type,
   simplifying D-160's own original plan (which anticipated a separate DEK-nulling
   step before deletion).
5. Confirmed embeddings remain genuinely absent (`embedding: None`, always, per
   `memory_engine/store.py`'s own comment "engine track doesn't embed in Phase A")
   and zero Neo4j vector/fulltext index exists anywhere in this codebase — fresh grep,
   zero hits both directions. Step 4 is N/A for facts, same conclusion D-160 reached,
   independently re-verified rather than carried forward unchecked.
6. Read `harness/derivation_cascade.py::cascade_from_parents`/`_active_children` in
   full — the existing R18 cascade WALK is reusable in shape, but its ACTION (close,
   not delete) and its SCOPE (active children only) are both wrong for erasure; built
   a new, parallel walk rather than repurposing this one, reasoned through explicitly
   (see WHAT WAS FOUND item 1).
7. **Designed the mechanism to extend, not duplicate, D-R-167's own report** per item
   2's own instruction: added `build_fact_erasure_report`/a `target_kind` dispatch to
   the EXISTING `harness/erasure_report.py` rather than a second module, so
   `verify_erasure_report` stays the ONE acceptance instrument for both ledger-payload
   and graph-side erasure.
8. Built `harness/graph_erasure.py` (`erase_fact`, `walk_lineage_closure`) and
   extended `harness/erasure_report.py` (`build_fact_erasure_report`, `_fact_state`,
   `_fact_tombstoned`, dispatch in `verify_erasure_report`).
9. Wrote `eval/test_graph_erasure.py` (9 cases) — run against the REAL shared dev
   graph (no hermetic redirection exists for Neo4j the way `HIP_HEL_DIR` redirects
   the ledger), using obviously-synthetic, uniquely-suffixed fixture data
   (`d-r-169-fixture-<random>`), every case cleaning up in `try/finally` regardless of
   pass/fail. Includes THE fault twin item 3 names by description (an orphaned
   derived child, executed not asserted), a missing-tombstone twin, a forged-report
   twin, a multi-level cascade proof, and a proof that erasure reaches CLOSED
   (already-retracted) derived children, which R18's own cascade deliberately does
   not.
10. Ran the new file standalone under the graph lock: 9/9 pass on first run.
11. Verified, by direct query, ZERO fixture residue left in the real graph after the
    run (`MATCH (f:Fact) WHERE f.fact_id STARTS WITH "d-r-169-fixture-"` → 0).
12. **Found and fixed one real, self-inflicted collision with an existing invariant**:
    `harness/graph_erasure.py`'s own module docstring quoted `memory_engine/store.py`'s
    exact `CREATE (n:Fact {...})` Cypher shape while explaining the DEK reasoning —
    tripped `eval/test_fact_write_convergence.py`'s own single-materialization-point
    scanner, which correctly reads docstrings (not just code) as AST string constants
    and correctly does NOT exempt them the way it exempts real Python comments (its
    own anti-vacuity test proves this distinction is deliberate). Rephrased the
    docstring to describe the shape without quoting it verbatim — a real fix to my
    own new file, not a change to the scanner or an exemption carved out for it.
13. **Found and fixed one real, EXPECTED consequence**, exactly the shape the
    standing invariant (D-R-168) exists to catch: `erase_fact`'s own HEL tombstone
    call is itself a 17th real production `epistemic_ledger.append()` call site —
    `eval/test_ledger_callsite_enumeration.py`'s own completeness check correctly
    went red on the first `--layer 7` run after this file landed. Reviewed and added
    deliberately to `EXPECTED_FILE_COUNTS`, not bumped reflexively — plus one stale
    hardcoded `== 16` in the same file's own uniformity assertion, updated to 17.
14. Wired the new test file into `scripts/run_harness.sh`'s standing battery list —
    safe because the script's own graph-lock acquisition (D-146, a PRECONDITION of
    the tooling) already covers every standing-battery pytest call, including this
    one.
15. Ran the full standing battery (33 files) via `scripts/run_harness.sh --layer 7`:
    first pass caught both items 12/13 above; fixed; re-ran clean.
16. **RATCHET PASS — no scenario regressed vs baseline**, confirmed twice (once
    after each fix round) and once more after a small import-hygiene cleanup (see
    item 17).
17. Reduced one minor duplication found during self-review: `graph_erasure.py` had
    redefined `MAX_CASCADE_DEPTH = 32` rather than importing the same constant R18's
    own cascade already declares — fixed to import, so the two walks' depth guards
    can never drift apart. Re-ran the affected tests and the full battery again;
    clean both times.
18. Confirmed zero fixture residue in the real graph a second and third time, after
    the full battery runs.
19. Ran the memory harness under the graph lock: **13/17**, failing set exactly
    `{MEM-115, MEM-116, MEM-117, MEM-118}` — the same pinned set as every prior
    ledger dispatch this session, not a new regression.
20. Wrote this dispatch doc, including item 4's honest-limits list and item 6's
    explicit statement that nothing destructive ran and what authorization a real run
    would need.
21. Staged by explicit pathspec; committed AND pushed as one lock-guarded operation.

## WHAT WAS FOUND

### Item 1 — the survey, and D-160's claim confirmed/corrected

**What a complete graph-side erasure must reach, and its state at HEAD:**

| Target | Deletion path today | Notes |
|---|---|---|
| `:Fact` row | **3 hard-delete sites exist**, none R17-shaped (see below) | corrects D-160 |
| DEK (`encrypted_dek`) | Same as row — property ON the node | no separate step needed |
| Value ciphertext | Same as row — property ON the node | no separate step needed |
| Embeddings | **N/A, genuinely absent** | `embedding: None` always (Phase A never embeds); zero vector/fulltext index anywhere |
| Derived children (R18 lineage) | Walk mechanism exists (`derivation_cascade.py`), action is CLOSE not DELETE, active-only | reused the WALK shape, built a new DELETE-shaped, closed-node-reaching action |
| HEL audit tombstone (step 5) | Mechanism exists (D-R-167/168), **nothing on the graph side calls it** | same as D-160's own finding, unchanged |

**D-160's claim — "the only hard delete in the whole codebase is the demo reset" —
is INCOMPLETE at HEAD, confirmed by a fresh grep for every `DELETE`/`DETACH DELETE`
in production code, not assumed:**

1. `scripts/demo_reset.py:83` — `MATCH (f:Fact) DETACH DELETE f` (blanket, CLI).
2. `server/demo_dashboard.py:1890`'s `/api/reset` endpoint — its OWN, separate,
   inline `MATCH (f:Fact) DETACH DELETE f` — a SECOND, independent implementation of
   essentially the same "wipe and reseed" operation, reachable over HTTP, not a call
   into `demo_reset.py`.
3. `scripts/cleanup_test_facts.py` (TD-041) — a pre-existing (added 2026-06-20, six
   weeks before D-160's own 2026-08-04 survey — confirmed via `git log
   --diff-filter=A`), SCOPED, elementId-targeted delete utility with an interactive
   confirmation prompt. Genuinely missed by D-160's own survey, not added later.

**None of the three is R17-shaped** — none appends a HEL tombstone, none walks
derived-child lineage, `cleanup_test_facts.py`'s own `DETACH DELETE` would silently
orphan any derived child of whatever it deletes (confirmed by reading it: zero
`derivation_cascade`/`epistemic_ledger` references). This is the real gap Segment 6
closes: not "no delete exists," but "no delete reaches everything R17 requires, or
audits itself."

### Item 2 — built, verifiable by D-R-167's own report, not a second story

`harness/graph_erasure.py::erase_fact(fact_id, *, reason, actor)` — one transaction:
counts whether the target existed, walks `walk_lineage_closure` (the full,
unconditional, closed-node-reaching cascade set), `DETACH DELETE`s the target and
every descendant together, then appends ONE `fact.erased` HEL tombstone (v2) naming
everything erased. Idempotent on an already-gone or never-real `fact_id`, matching
`erase_payload_for_event`'s own contract.

`harness/erasure_report.py` extended, not duplicated: `build_fact_erasure_report`
joins the existing `build_erasure_report` behind the SAME `verify_erasure_report`
entry point, dispatched on `report["target_kind"]`. A caller — or a future audit
script — verifies EITHER kind through one function, matching item 2's own
instruction not to build a second acceptance story.

### Item 3 — the fault twin that matters, executed

`test_graph_erasure_catches_an_orphaned_derived_child` — bypasses `erase_fact`'s own
cascade entirely: creates a primary fact and a derived child directly, deletes ONLY
the primary via raw Cypher (the exact shape `cleanup_test_facts.py`'s own existing
delete would produce if pointed at a fact with descendants), then calls
`build_fact_erasure_report` on the primary. **The report correctly shows
`1_access_path_revoked: False` and `orphaned_descendants: [child]`, and
`verify_erasure_report` returns `False`, naming the incompleteness — proven by
executing the bypass and reading the real result, not by asserting the logic would
catch it.** Two further executed twins round this out: a missing-tombstone case
(row+cascade genuinely gone, audit never appended) and a forged-report case (a hand
report claiming success against an untouched fact) — both caught, same discipline as
every prior erasure-report test file this session.

### Item 4 — what erasure still cannot reach, named plainly

- **Backups.** No backup system exists anywhere in this codebase — the same absent
  dependency D-160 and D-R-167 already found for the ledger side, unchanged, now
  equally true for the graph side (there is nothing to schedule expiry against, for
  either surface).
- **v1 ledger events.** Permanent, per the two-population limit established at
  D-R-165 and unchanged since — an erased fact's `fact.erased` tombstone is v2, but
  any `hel=="1.0"` event written before this dispatch (or by any of the codebase's
  still-v1 corners) is not rewritten by an erasure landing after it.
- **Prior `turn.record` references to the erased fact_id.** The ledger is append-only
  by design — a `turn.record` event that admitted this fact into a past reply
  (`epistemic_record.py::log_epistemic_record`) still names the `fact_id` (never the
  VALUE, per TD-030's own value-stripping) in that OLD event, permanently. Erasing
  the fact removes its row, DEK, ciphertext, and derived children; it does not
  retroactively scrub the fact_id's own past appearances in the audit trail. This is
  the graph-side analogue of the same "the chain never rewrites the past" principle
  established for the ledger side at D-R-165, named here for the first time because
  this is the first dispatch where a graph-side erasure exists to make the question
  concrete.
- **Session memory / conversation-turn caches.** Out of THIS dispatch's own "graph
  side" scope by Bill's own framing — in-process, TTL-evicted, self-clearing on
  restart (confirmed via `harness/session_memory.py`), not a durable artifact R17's
  own steps describe.
- **The other two hard-delete paths** (`demo_reset.py`, `demo_dashboard.py`'s
  `/api/reset`) remain exactly what they were: blanket wipes with no cascade
  awareness and no HEL tombstone. `erase_fact` does not replace them and this
  dispatch does not touch them — named as a real, adjacent gap, not fixed here (see
  OPEN).

### Item 6 — nothing destructive ran; what a real run would need

**Every erasure exercised in this dispatch — the green path, all three fault twins,
and every intermediate check — ran against fixture data created and torn down within
the same test, using an obviously-synthetic `d-r-169-fixture-` prefix, confirmed by
direct query to leave zero residue after three separate full-battery runs.** No real
household member's fact, no fixture the demo depends on, and no frozen-demo or
`hip-cutover-demo` data was read, written, or deleted by this dispatch.

**If Bill wants `erase_fact` exercised against a REAL fact** — a real household
member's actual data, whether on the shared dev graph, the demo graph, or the frozen
demo — **that needs his own explicit destructive-write authorization, named as such,
before any dispatch attempts it.** The mechanism is built and proven; running it for
real is a separate decision with irreversible consequences (the row, its DEK, its
ciphertext, and every derived descendant are gone; only the ledger's own audit trail
survives, naming what happened, never what the content was).

## VERIFIED

**Watched, executed:**
- Fresh, whole-codebase grep for every `DELETE`/`DETACH DELETE`, each hit read in
  context before being characterized.
- `git log --diff-filter=A` confirming `cleanup_test_facts.py` predates D-160's own
  survey.
- Direct reads of `_new_node_props`, `read_user_facts`'s `RETURN` clause, and
  `derivation_cascade.py`'s full cascade implementation before designing around them.
- Fresh grep confirming zero embedding/vector/index code anywhere near `:Fact`.
- `eval/test_graph_erasure.py`: 9/9 against the REAL dev graph, fixture-scoped.
- Direct query confirming zero fixture residue, run three separate times (after the
  standalone test run and after two full-battery runs).
- `scripts/run_harness.sh --layer 7`: two real, self-caused issues found and fixed
  (a docstring collision with an existing invariant; the standing invariant's own
  expected-count needing a deliberate, reviewed bump) — both caught by running the
  harness, not by code review; **RATCHET PASS**, confirmed three times across the fix
  rounds.
- Memory harness: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.

**Reasoned about, not independently re-derived:** whether Neo4j's own default
schema/uniqueness constraints (if any exist on `:Fact.fact_id`) interact with
`DETACH DELETE` in any way relevant here was not separately audited — `DETACH DELETE`
is Neo4j's own standard, index-safe deletion primitive, used identically by the three
pre-existing hard-delete sites this survey found, so this dispatch relies on that
established usage rather than re-verifying Neo4j's own guarantees from scratch.

## HASH

Staged for commit: `harness/graph_erasure.py` (new), `harness/erasure_report.py`
(extended), `eval/test_graph_erasure.py` (new), `eval/
test_ledger_callsite_enumeration.py` (expected-set update), `scripts/run_harness.sh`
(wired the new file), this dispatch doc.

## OPEN

- **`scripts/demo_reset.py` and `server/demo_dashboard.py`'s `/api/reset` remain
  R17-unaware blanket deletes** — named in item 1/4, not fixed here. Whether they
  should be taught to call `erase_fact` per-row (so a demo reset is ALSO a properly
  tombstoned erasure) or left as-is (a demo reset is arguably a different KIND of
  operation, not a subject-initiated erasure request) is a real design question this
  dispatch surfaces but does not decide.
- **`scripts/cleanup_test_facts.py` can silently orphan derived children** — a
  pre-existing, real gap (not introduced by this dispatch) now precisely named: its
  own `DETACH DELETE` has no cascade awareness. Worth a follow-up, not built here
  (this dispatch was scoped to BUILD ONLY, against fixtures).
- **Prior `turn.record` ledger events referencing an erased fact_id are not
  scrubbed** — named plainly in item 4, a permanent limit of the append-only design,
  not a gap this dispatch could close.
- **Subject-wide fact erasure ("erase everything this member ever wrote") is not
  built** — `erase_fact` is per-artifact (plus its cascade), matching R17's own
  "smallest practical revocation unit" framing; a subject-wide sweep would need its
  own design, same reasoning D-R-167 already gave for not building subject-wide
  LEDGER reporting.
- **This mechanism has never been run against real data and was not authorized to
  be** — see item 6. Any future dispatch that wants to exercise it for real needs
  Bill's own explicit authorization, named as such at that time.
- **Nothing ruled MET.**

## RECAP
D-R-169: surveyed what graph-side erasure must reach and corrected D-160's own claim
against HEAD — THREE hard-delete sites exist, not one (`demo_reset.py`,
`demo_dashboard.py`'s own separate `/api/reset`, and the pre-existing
`cleanup_test_facts.py`, six weeks older than D-160's survey and missed by it), none
R17-shaped. Built `harness/graph_erasure.py::erase_fact` — hard-deletes a fact and
every descendant transitively derived from it, unconditionally, reaching CLOSED
children too (further than R18's own retraction cascade goes), appends one HEL
tombstone. Extended D-R-167's own `harness/erasure_report.py` with a `fact_node`
target kind behind the SAME `verify_erasure_report` entry point — one acceptance
instrument, not two stories. **Proved the fault twin the dispatch named by
description — an orphaned derived child — CAUGHT BY THE REPORT, executed**: bypassed
the cascade, left a real orphan in the real graph, the report correctly flagged it
incomplete. Two more executed twins (missing tombstone, forged report) round out
D-87. Found and fixed two real, self-caused issues on the first `--layer 7` run: a
docstring collision with the existing single-materialization-point scanner, and the
standing invariant (D-R-168) correctly catching this dispatch's own 17th real ledger
call site — reviewed and added deliberately. Named the honest limits plainly:
backups, v1 ledger events, and — new this dispatch — prior `turn.record` events'
own permanent references to an erased fact_id, none of which erasure can retroactively
touch. **Nothing destructive ran against real data** — every case used
disposable, uniquely-prefixed fixtures, confirmed zero residue three times. Running
this for real needs Bill's own explicit authorization, not requested or used here.
9/9 new tests, full battery green, RATCHET PASS, memory harness 13/17 at the same
pinned failing set. Nothing ruled MET.
