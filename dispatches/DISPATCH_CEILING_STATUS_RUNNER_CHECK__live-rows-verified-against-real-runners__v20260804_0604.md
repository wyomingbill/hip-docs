# DISPATCH_CEILING_STATUS_RUNNER_CHECK
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (tooling only — the status board reports over existing REQs, changes no
governed behaviour, rules nothing; same posture D-148 itself took, restated here rather than
assumed)

**REQ:** NONE. Following D-148's own precedent exactly: `scripts/ceiling_status.py` derives
and displays state from `REQ_STRUCTURAL_CEILING` and `REQ_CEILING_ACCEPTANCE` — this dispatch
hardens that same derivation to verify one of its own claims instead of relaying it. No
governed behaviour changes; no requirement is ruled; the tool remains read-only reporting.

## THE ASK

Dispatch text, verbatim:

```
D-149 — cross-check LIVE rows against tests that actually run. The board reports the
document's claim; make it verify the claim. A row tiered LIVE with no runner entry, or
a runner entry no battery satisfies, renders as CLAIMED-NOT-VERIFIED — not as LIVE and
not as an error. Anti-vacuity: a check finding zero runners must refuse to emit.
Report per STANDARD PREAMBLE.
```

## WHAT WAS DONE

1. Gate checked — matched. Repo lock acquired via `scripts/hip_lock.py with repo` before
   reading anything, held for the dispatch's duration.
2. Read D-148's own build (`50daa12`) and `scripts/ceiling_status.py` in full before touching
   it — found `check_registry.py` (the OTHER gated-check registry in this codebase) is keyed
   by scenario name (`L7:PSA1` etc.), not by acceptance-row id, so it was not directly
   reusable; the cross-check needed its own row→runner mapping.
3. Established the ground truth by direct AST scan BEFORE writing any check logic: every
   `test_ceil_a<N>_*` function under `eval/`, cross-referenced against the acceptance
   document's current LIVE set (`{A1, A2, A7, A8, A11, A18, A27, A29, A30}`, 9 rows). Found
   three (A18, A29, A30) with NO matching function anywhere — R18/R29/R30's real coverage
   (`eval/test_lineage_block.py`, `eval/test_sensitivity_registry.py`) predates the naming
   convention this check has to rely on. This shaped the whole design: the check had to be
   honest about what it CAN verify (the convention) without either wrongly claiming these
   three rows have no tests, or silently trusting an unverifiable prose claim to wave them
   through.
4. Built `parse_runners()` (AST-based, never regex — D-75 discipline, proven by a fault twin
   below), `parse_wired_battery_files()` (reads `scripts/run_harness.sh`'s own pytest file
   list, not a second copy of it), and `cross_check_live_runners()` (the row-mutating check
   itself, with the anti-vacuity refusal as its first action).
5. Wired the cross-check into `derive()`, added `claimed_tier`/`runner_note` to each LIVE row,
   split the acceptance summary into `claimed_live`/`live` (now VERIFIED)/`unverified_live`.
6. Updated the HTML rendering (a distinct `CLAIMED-NOT-VERIFIED` style, the runner note shown
   per row) and `main()`'s terminal output (names each unverified row and why).
7. Ran the tool directly against the real documents before writing tests, to confirm the
   design produces a real, non-trivial finding rather than a vacuous all-clear or all-red
   result: `claimed-LIVE=9 verified-LIVE=6 CLAIMED-NOT-VERIFIED=3`.
8. Wrote 10 new tests in `eval/test_ceiling_status_board.py` (D-87: fault twins for both named
   failure shapes, the anti-vacuity refusal, an AST-vs-regex fault twin matching this file's
   own established convention, and a pinned real-data assertion naming the A18/A29/A30 finding
   precisely so a future change to it is a deliberate edit, not a silent drift).
9. Fixed three bugs in my own first draft of those tests by running them, not by re-reading —
   a wording mismatch, a path-computation assumption that didn't hold for a synthetic
   `tmp_path`, and a wrong assumption that this file's own name would not legitimately appear
   in the wired-battery set (it does — it is correctly wired).
10. Ran `--layer 7` — clean. Regenerated `docs/status/CEILING_STATUS.html` and
    `CEILING_HISTORY.csv` with the final code.
11. Staged by explicit pathspec, committed, pushed, verified post-commit, released the lock.

## WHAT WAS FOUND

### The mechanism

`parse_runners()` AST-walks every `.py` file under `eval/` for function defs matching
`^test_ceil_a(\d+)_` — the CONVENTION this codebase already declares
(`eval/test_ceiling_inference.py`'s own docstring: "ceiling rows are `test_ceil_a<N>_*` in
`eval/test_ceiling_*.py`"). `parse_wired_battery_files()` reads the exact file list
`scripts/run_harness.sh`'s standing batteries invoke, from that script's own text — not a
second, driftable copy. `cross_check_live_runners()` then, for every row currently tiered
LIVE: if NO matching function exists anywhere, or matching functions exist but none of their
FILES are in the wired set, overwrites that row's displayed tier to `CLAIMED-NOT-VERIFIED`
and records why; otherwise the row stays LIVE with a `runner_note` naming the runner that
verifies it.

### The real finding — not vacuous, not invented for the tests

Against the actual documents: **6 of 9 claimed-LIVE rows verify** (A1, A2, A7, A8, A11, A27 —
all in files already wired into the standing batteries). **3 do not** (A18, A29, A30) — **not
because they lack real coverage** (R18's is `eval/test_lineage_block.py`, 16 cases, D-105/
D-107; R29/R30's is `eval/test_sensitivity_registry.py`, 31 cases, D-75), **but because those
files predate the `test_ceil_a<N>_*` naming convention** the cross-check structurally relies
on. This is reported precisely as that — a naming-convention gap this tool cannot see past,
not a claim that R18/R29/R30 are untested. The runner note for each says exactly this rather
than implying absence.

### Anti-vacuity, executed both directions

`test_board_runner_zero_runners_anywhere_refuses_to_emit`: calling the cross-check with an
empty runner map raises `DeriveError` naming the reason (a scanner defect must not read as
nine coverage gaps). `test_board_runner_wired_entry_anti_vacuity_stays_live`: a genuinely
wired runner is NOT flagged — proves the two refusal-case tests are not passing because the
check flags everything unconditionally.

### A fault twin proving AST discipline, not merely claiming it

`test_board_parse_runners_is_ast_not_regex` plants `def test_ceil_a77_...` inside a comment,
a docstring, and a string literal in a synthetic file — none count. A companion test
(`..._finds_a_real_function`) proves the scanner isn't simply blind: a REAL function def in
the same style IS found. Matches this exact codebase's own repeated caution (D-75: a
source-text scan can be tripped by its own explanatory comment) rather than re-deriving it.

## VERIFIED

**Watched run:**
- `python3 scripts/ceiling_status.py` run directly, three times across this dispatch (before
  writing tests, mid-build, and as the final regeneration) — output read each time, not
  assumed: `claimed-LIVE=9 verified-LIVE=6 CLAIMED-NOT-VERIFIED=3`, identically, all three
  runs.
- `eval/test_ceiling_status_board.py`: `20 passed` standalone
  (`PYTHONPATH=$(pwd) python3 -m pytest ... --import-mode=importlib`), including all 10 new
  cases and the 10 pre-existing ones (confirmed unbroken by this change).
- `--layer 7`: exit 0, RATCHET PASS, standing batteries `424 passed, 8 xfailed` (up from 404
  — the +20 is this dispatch's own new tests). Lock self-acquisition observed live.
- `docs/status/CEILING_HISTORY.csv`: the pre-existing row from D-148's own generation run
  (`acceptance_live=9`, the old, unverified semantics) sits alongside this dispatch's two
  regeneration rows (`acceptance_live=6`, now meaning VERIFIED) — a real, visible trend line
  showing the semantic tightening, left as-is per the tool's own "generated, append-only,
  never hand-edited" discipline rather than pruned.
- `git status` before and after commit: confirmed `docs/INDEX.md` and any other lane's WIP
  untouched.

**Reasoned about:** that A18/A29/A30's real coverage genuinely exists under other names (not
just "the naming convention doesn't match") rests on this session's own prior knowledge of
those dispatches (D-75 for R29/R30, D-105/D-107 for R18) — the tool itself cannot and does not
claim this; its own runner_note text is careful to say only what it can verify (no matching
function under the convention), not "no coverage exists."

## HASH

Staged for commit: `scripts/ceiling_status.py`, `eval/test_ceiling_status_board.py`,
`docs/status/CEILING_STATUS.html`, `docs/status/CEILING_HISTORY.csv`, this dispatch doc.

## OPEN

- **The naming-convention gap itself (A18/A29/A30) is named, not closed.** Renaming
  `eval/test_lineage_block.py`'s and `eval/test_sensitivity_registry.py`'s relevant functions
  onto `test_ceil_a18_*`/`test_ceil_a29_*`/`test_ceil_a30_*` would close it and is the natural
  follow-up — not performed here, out of this dispatch's own scope (it asked for the
  cross-check, not a renaming pass across two other files).
- **The cross-check is scoped to LIVE rows only**, per the dispatch's literal wording. STRICT
  XFAIL and CONTRADICTED-XFAIL rows are NOT verified by this mechanism (confirmed by
  `test_board_runner_non_live_rows_are_never_touched`) — extending it is a natural next step,
  not requested here.
- **The wired-file check confirms a FILE is invoked, not that the SPECIFIC row's test within
  it collects or passes.** A file listed in `scripts/run_harness.sh` but containing a broken
  or erroring `test_ceil_a<N>_*` function would still read as verified today. A stronger
  version could run `pytest --collect-only` against the matched node ids specifically —
  considered, not built, to keep this dispatch's cost proportionate to what was asked.
- **Nothing ruled**, per instruction. No REQ filed, per D-148's own precedent, stated
  explicitly rather than assumed.

## RECAP
D-149: ceiling status board's LIVE rows now cross-checked against real, wired test runners —
6 of 9 verify; 3 (A18/A29/A30) render CLAIMED-NOT-VERIFIED, a naming-convention gap in their
own coverage's file names, not a coverage gap. Anti-vacuity proven both directions. 20/20
tests pass, `--layer 7` clean (424 passed/8 xfailed), nothing ruled.
