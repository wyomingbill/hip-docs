# DISPATCH_ERASURE_SEQUENCE_COMPLETE
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (R17 — subject-wide graph erasure, the last named gap) + a
methodology note on enumeration discipline + a real design fix found by a test this
dispatch wrote against its own new code.

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R17 (ratified D-71). No amendment, no new REQ doc.

## THE ASK

Bill's instruction, verbatim:

```
=== D-R-170 | ~/hip-roadmap, roadmap | R17: finish the erasure sequence ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R17, ratified D-71.
Built so far: the erasure report (D-R-167) and cascade-aware graph deletion, fixture-
proven (D-R-169). Every production ledger write emits v2 (D-R-168).

NO DESTRUCTIVE AUTHORIZATION. Nothing may delete real data. Fixtures only. If a step
cannot be proven without destroying real data, STOP AND REPORT.

1. RE-GRADE R17's SEVEN STEPS AGAINST HEAD. D-160's grade (one wired-able, three
   absent, three unwired) predates both builds. Say which are now done, which remain,
   and where your grade differs from D-160's and D-R-167's — do not silently supersede
   either.
2. NOTE THE ENUMERATION HISTORY AND ACT ON IT. Four counts in this build have been
   wrong: the grep, the re-grade, the AST scanner's first draft, and D-160's
   hard-delete survey. Each was closed by hand-reading or by running. Grade this by
   the method that has actually worked, and say which you used.
3. BUILD THE NEXT REMAINING STEP — cheapest first, and it must be verifiable through
   the D-R-167 report rather than telling its own story.
4. FAULT TWIN: the step half-done must be CAUGHT, proven by execution.
5. STATE WHAT R17 STILL CANNOT REACH after this lands — backups, v1 events, anything
   outside the graph. That list belongs in the report.
6. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
7. Rule nothing MET.
```

## WHAT WAS DONE

1. Gate checked — matched, tree clean except another lane's own untouched WIP, HEAD
   in sync with `origin/roadmap`.
2. Re-read D-160's own 7-step table and D-R-167's own re-grading, side by side, before
   forming a new grade — not from memory.
3. Re-read the ACTUAL current code of every mechanism this grade depends on
   (`harness/graph_erasure.py`, `harness/erasure_report.py`, `harness/
   derivation_cascade.py`, `harness/extraction_queue.py`) — per item 2's own
   instruction, by hand-reading, not by re-asserting a prior dispatch's own summary.
4. Formed the re-grade (item 1 below): 5 of 7 steps now EXIST AND WIRED for the
   per-artifact erasure operation (both ledger and graph artifacts), 1 is genuinely
   N/A (confirmed a third time, independently), 1 remains externally blocked (no
   backup system). Concluded NOTHING remains to build as one of the 7 NUMBERED steps
   themselves.
5. Identified the real remaining gap is not a STEP but a GRANULARITY: subject-wide
   graph erasure ("erase everything this member owns") has no counterpart to
   `epistemic_ledger.destroy_member_key` — named as OPEN in both D-R-167's and
   D-R-169's own dispatch docs, not invented fresh here.
6. Built `harness/graph_erasure.py::erase_member_facts(owner, ...)` — enumerates
   every `:Fact` owned by `owner` (active or closed), erases each via the ALREADY-
   BUILT, already-tested `erase_fact` (zero new deletion logic, zero risk of a bulk
   path diverging from the single-fact path).
7. Extended `harness/erasure_report.py` with a THIRD target kind, `"member_facts"`,
   behind the SAME `verify_erasure_report` entry point — per item 3's own
   instruction not to tell a second story.
8. Wrote `eval/test_graph_erasure.py`'s own new section (10 cases) for the
   subject-wide path, run against the real dev graph with disposable,
   uniquely-prefixed fixtures, same posture as D-R-169.
9. **First test run found a real bug in my OWN test's own design**, not in the
   code: a derived-child fixture shared its parent's owner, so the "every fact for
   this owner" enumeration redundantly found it directly, making the assertion about
   which facts were found via CASCADE (vs. direct enumeration) meaningless. Fixed by
   giving the derived child a DIFFERENT owner, which is also the more honest test —
   it now proves cross-owner cascade reachability, a real case (a derived fact need
   not share its parent's owner).
10. **The same first test run found a REAL, separate design gap in my OWN new
    code**, caught by a test I wrote specifically to probe it
    (`test_fact_node_report_still_forbids_owner`): making `owner` legitimate for
    `member_facts` reports, via ONE global `REPORT_FIELDS` allowlist, silently made
    it legitimate for `ledger_payload`/`fact_node` reports too — a hand-forged
    `fact_node` report carrying `owner` would have passed the leak check uncaught,
    exactly the failure `verify_erasure_report` exists to catch. **Fixed by making
    the leak check target-kind-aware** (`_TARGET_KIND_FIELDS`, a per-kind extra-field
    registry, checked against `report["target_kind"]` rather than one blended set)
    — corrected my own just-written module docstring, which had claimed the
    single-global-set design was intentional and sufficient, to match.
11. **Also closed a real, pre-existing gap found while touching this code**:
    `FORBIDDEN_REPORT_KEYS` was declared at D-R-167 but never actually checked
    anywhere — unlike its own named precedent, `ledger_anchor.FORBIDDEN_ANCHOR_KEYS`,
    which IS tested. Wired it into `erasure_report_leaks` for real.
12. Re-ran the full erasure test suite (`test_graph_erasure.py`,
    `test_erasure_report.py`): 26/26 pass.
13. Confirmed zero fixture residue in the real graph (both the `d-r-169-fixture-`
    fact-id prefix and the new `d-r-170-fixture-owner-` owner prefix), by direct
    query.
14. Ran the full standing battery (33 files) via `scripts/run_harness.sh --layer 7`:
    clean on the FIRST attempt this time — `erase_member_facts` introduced zero new
    `epistemic_ledger.append()` call sites (it reuses `erase_fact`'s own existing
    one, via a loop, not a new call), so neither of D-R-169's own two self-caused
    issues (the docstring collision, the standing-invariant count) recurred.
15. **RATCHET PASS — no scenario regressed vs baseline.**
16. Confirmed zero fixture residue a second time, after the full battery run.
17. Ran the memory harness under the graph lock: **13/17**, failing set exactly
    `{MEM-115, MEM-116, MEM-117, MEM-118}` — the same pinned set as every prior
    ledger/erasure dispatch this session, not a new regression.
18. Wrote this dispatch doc, including item 2's own enumeration-methodology note and
    item 5's honest-limits restatement.
19. Staged by explicit pathspec; committed AND pushed as one lock-guarded operation.

## WHAT WAS FOUND

### Item 1 — R17's seven steps, re-graded against HEAD

D-160's own grade, restated for reference: **one wired-able** (step 2 — hard
infrastructure built, not connected), **three unwired** (steps 1, 3, 5 — some
mechanism existed but not the right one, or not connected to fact-level erasure),
**three absent** (steps 4, 6, 7 — genuinely nothing there).

| step | D-160 (2026-08-04, pre-build) | D-R-167 (ledger side only) | **THIS DISPATCH, against HEAD** |
|---|---|---|---|
| 1. revoke access paths | unwired (PARTIAL, retrieval filter only) | EXISTS/WIRED, collapses with 3 | **EXISTS AND WIRED** — `erase_fact`/`erase_member_facts` leave no row to have a path to at all, for either graph artifact type |
| 2. destroy key material | wired-able (DEK infra existed, unconnected) | N/A for targeted; unreported for subject-wide | **EXISTS AND WIRED** — DEK is a node property, deleted with the row (D-R-169); subject-wide now reaches every owned fact (D-R-170) |
| 3. delete active rows | unwired (`SET`, never `DELETE`) | EXISTS/WIRED (ledger payload files) | **EXISTS AND WIRED**, for `erase_fact`'s own explicit-erasure path. `retract_fact`'s own path is UNCHANGED — still `SET` only, BY DESIGN (retraction ≠ erasure, kept deliberately separate at D-160 and unchanged since) |
| 4. remove vector/index entries | absent | N/A, confirmed | **N/A, confirmed a THIRD time**, independently, via fresh source grep — no embedding/vector/fulltext index for `:Fact` exists anywhere in this codebase |
| 5. append opaque tombstone | unwired (mechanism existed, not connected) | EXISTS/WIRED (ledger side) | **EXISTS AND WIRED**, graph side too — `fact.erased`, one per `erase_fact` call, v2, off-ledger |
| 6. schedule backup expiry | absent | absent, unchanged | **UNCHANGED — genuinely absent**, external dependency (no backup system anywhere in this codebase) |
| 7. machine-verifiable report | absent | EXISTS (ledger_payload only) | **EXISTS for all THREE artifact granularities now**: `ledger_payload` (D-R-167), `fact_node` (D-R-169), `member_facts` (D-R-170) — one `verify_erasure_report` entry point |

**Where this grade differs from D-160's and D-R-167's, stated plainly:** D-160
graded against a codebase where none of this existed; D-R-167 graded the LEDGER
side only, correctly leaving the graph side exactly as D-160 found it. This
dispatch's grade is not a correction of either — it is the FIRST grade taken after
the graph-side mechanism (D-R-169) and its subject-wide extension (this dispatch)
both landed, and it reflects that: **for the per-artifact and per-subject erasure
OPERATIONS specifically (not for `retract_fact`, which remains a deliberately
different, non-destructive operation), all seven of R17's steps are now either
EXISTS-AND-WIRED (5 of 7) or correctly, permanently N/A/blocked (2 of 7). Nothing
remains as an unbuilt NUMBERED step.**

### Item 2 — the enumeration history, and the method used here

Four counts in this build's own history were wrong, each closed by a specific,
nameable method, not by re-asserting a prior claim:

| Wrong count | What it undercounted | Closed by |
|---|---|---|
| The grep (D-160/D-R-166) | 4 real ledger callers, actually 16 | **Running** an AST scanner (D-R-168) |
| D-R-168's own re-grade annotation, first draft | miscounted 12 vs. 15 sites still-v1 before D-R-166's own flip | **Hand-deriving** the before/after arithmetic methodically, before landing |
| The AST scanner's own first draft (D-R-168) | 2 same-module calls inside `epistemic_ledger.py` itself | **Hand-reading** the file directly (no pattern could have found it without the file being read) |
| D-160's hard-delete survey | 1 hard-delete site claimed, actually 3 | **Running** a fresh, exhaustive grep + `git log` (D-R-169) |

**The method that has actually worked, every time: either RUN something (a scanner,
a grep, a test, the harness itself) against the real current state, or HAND-READ
the actual file — never re-assert a prior dispatch's own summary as if re-deriving
it.** This dispatch's own item 1 re-grade used BOTH: hand-read every mechanism's
current source before grading it (step 3 of WHAT WAS DONE), and this dispatch's OWN
new build was itself caught by a THIRD instance of the pattern mid-dispatch (see
item 3 below) — proving the discipline still catches real gaps when applied
honestly to fresh work, not just retrospectively to old claims.

### Item 3 — built, and caught by its own test before landing

`harness/graph_erasure.py::erase_member_facts` + `harness/erasure_report.py::
build_member_erasure_report` (target_kind `"member_facts"`). **A fifth instance of
item 2's own pattern happened WHILE BUILDING THIS**, not before it: the first test
run found (a) a design flaw in my own test fixture (a derived child sharing its
parent's owner, making the enumeration-vs-cascade distinction untestable) and (b) a
REAL security-relevant gap in the report module itself — a single global
`REPORT_FIELDS` allowlist meant `owner` being legitimate for one report kind made it
silently legitimate for all three, so a hand-forged `fact_node` report carrying
`owner` would have passed `verify_erasure_report`'s own leak check uncaught. **Both
found by running the new test suite against real behavior, not by review** — fixed
before this dispatch's own build could be called complete, matching item 2's own
instruction to grade "by the method that has actually worked."

### Item 4 — the fault twin, executed

`test_member_erasure_catches_a_half_done_erasure` — bypasses `erase_member_facts`
entirely: creates three facts for one owner, erases only two directly via
`erase_fact` (simulating a crash or an enumeration bug mid-sweep), then builds a
`member_facts` report against the FULL originally-intended three-fact list. **The
report correctly shows `remaining_fact_count: 1` and `1_access_path_revoked: False`,
and `verify_erasure_report` returns `False`.** A second, DIFFERENT half-done shape is
also proven: `test_member_erasure_independent_check_catches_what_the_callers_list_omits`
— `erase_member_facts` runs CORRECTLY against its own snapshot, but a new fact for
the same owner appears afterward (a race, or a write landing after the enumeration).
A report trusting only the caller's own `erased_fact_ids` list would show false
success; the report's OWN independent, list-blind remaining-count check catches it
instead — proving the "never trust the caller's own claim" discipline this whole
module family has followed since D-R-167 holds for the NEW report kind too, not just
inherited by name.

### Item 5 — what R17 still cannot reach, restated and extended

- **Backups.** Still no backup system anywhere in this codebase — unchanged since
  D-160, confirmed a third time.
- **v1 ledger events.** Permanent, per the two-population limit (D-R-165),
  unaffected by anything built since.
- **Prior `turn.record` references to an erased fact_id.** Named at D-R-169,
  unchanged — the ledger never rewrites the past.
- **`retract_fact`'s own path.** Deliberately, permanently different from erasure —
  a retraction closes, never deletes; this is correct behavior, not a gap, but
  worth restating so a future reader does not expect `retract_fact` to gain
  erasure's own guarantees.
- **The two other hard-delete sites** (`demo_reset.py`, `demo_dashboard.py`'s own
  `/api/reset`) remain R17-unaware blanket wipes — named at D-R-169, unchanged.
- **There is still no live TRIGGER anywhere in `server/` connecting a real
  household request to `erase_fact`/`erase_member_facts`.** Named for the first
  time here, precisely because subject-wide erasure (this dispatch) makes the
  question concrete: the MECHANISM for "a member asks to have their data erased"
  now fully exists and is fixture-proven, but nothing in the live system can reach
  it — no API endpoint, no voice command, no admin action calls either function
  from real request-handling code. Wiring a real trigger is a genuinely different,
  larger decision (who may request erasure, through what interface, under what
  authorization) that this dispatch does not make.

## VERIFIED

**Watched, executed:**
- Direct re-reads of `graph_erasure.py`, `erasure_report.py`, `derivation_cascade.py`,
  `extraction_queue.py` before forming the item 1 re-grade — not re-asserted from
  memory of prior dispatch docs.
- `eval/test_graph_erasure.py`'s new section: found real bugs in both the new test's
  own fixture design and the new report code's leak check, both fixed, then 26/26
  (whole file) passing.
- Direct query confirming zero fixture residue (both prefixes), twice.
- `scripts/run_harness.sh --layer 7`: clean on the first attempt — no self-caused
  regression this time, confirmed by re-checking the callsite-enumeration and
  fact-write-convergence invariants explicitly stayed green; **RATCHET PASS**.
- Memory harness: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.

**Reasoned about, not independently re-derived:** whether `erase_member_facts`'s own
per-fact loop (calling `erase_fact` N times rather than one bulk transaction) could
leave a partial state visible mid-run if interrupted was not stress-tested under
concurrency — each individual `erase_fact` call is atomic (its own transaction), but
the SEQUENCE across facts is not, by design (matching this dispatch's own fault-twin
proof that a report can and does catch exactly this partial state, rather than
preventing it from ever occurring).

## HASH

Staged for commit: `harness/graph_erasure.py` (extended),
`harness/erasure_report.py` (extended, target-kind-aware leak check),
`eval/test_graph_erasure.py` (extended), this dispatch doc.

## OPEN

- **No live trigger connects any real request to `erase_fact`/`erase_member_facts`**
  — named plainly in item 5, the most significant remaining gap, and a genuinely
  different kind of decision (interface, authorization) than anything this
  dispatch or its predecessors were asked to make.
- **`retract_fact`'s own path stays deliberately unwired to the ledger** — correct,
  not a gap, restated so it is not mistaken for one.
- **The two other hard-delete sites remain R17-unaware** — named at D-R-169,
  unchanged, not fixed here.
- **Nothing ruled MET.**

## RECAP
D-R-170: re-graded R17's seven steps against HEAD, hand-reading every mechanism's
current code rather than re-asserting prior summaries — **five of seven now EXIST
AND WIRED for the per-artifact/per-subject erasure operation** (steps 1/2/3/5/7),
one remains genuinely N/A (step 4, embeddings, confirmed a third time), one remains
externally blocked (step 6, no backup system). Nothing remains as an unbuilt
NUMBERED step; `retract_fact`'s own path stays deliberately, permanently different
from erasure, not a gap. Named and acted on the enumeration-history pattern item 2
asked for: four prior wrong counts, each closed by hand-reading or by running, never
by re-trusting a prior claim — and a FIFTH instance happened mid-dispatch, caught by
this dispatch's own new tests: a fixture design flaw, and a real security-relevant
gap in the new report code (a global allowlist silently making `owner` legitimate
for every report kind, not just the one it was added for) — both fixed before
landing. Built `erase_member_facts`, the graph-side counterpart to
`destroy_member_key`, reusing `erase_fact` with zero new deletion logic, extended
under the SAME `verify_erasure_report` entry point. Proved the fault twin item 4
asked for, twice: a half-done sweep caught by the per-fact re-check, and a
DIFFERENT half-done shape — a fact appearing after the snapshot — caught only by the
report's own independent, list-blind remaining-count check. Restated the honest
limits and named one new, more significant one: the mechanism is complete and
fixture-proven, but nothing in the live system can reach it yet — no real trigger
exists. 26/26 new/extended tests, full battery green on the first attempt, RATCHET
PASS, memory harness 13/17 at the same pinned failing set. Nothing destructive ran
against real data. Nothing ruled MET.
