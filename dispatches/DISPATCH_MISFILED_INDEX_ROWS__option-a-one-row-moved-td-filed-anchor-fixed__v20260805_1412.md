# DISPATCH_MISFILED_INDEX_ROWS
Status: BUILT
Reconciled-Against: 2026-08-05 (D-R-184; parent `402d152`)

**TYPE:** BUILD (docs only: one row moved, one TD filed, one CLAUDE.md instruction fixed)

**REQ:** NONE — process/documentation fix, no governed behavior changes (Requirements
Discipline item 10).

## THE ASK

```
=== D-R-184 | ~/hip-roadmap, Lane B worktree | Option A on the misfiled rows ===
STANDARD PREAMBLE. Temp branch, remove worktree after.
1. Move D-R-178's row to the dispatches table, annotated. One row only.
2. File a TD for the other 54 with the root cause: the insert helper anchors on the
   first "| D-" line instead of the dispatches section header, so rows land in
   whatever table comes first. The sweep is its own future dispatch, AFTER the helper
   is fixed.
3. Fix the helper anchor in CLAUDE.md's instruction so new rows land right from now on.
4. Rule nothing. Report SHORT.
```

## WHAT WAS DONE

1. Gate checked at `~/hip-roadmap` first (matched), then set up Lane B: found a stale,
   clean, unused worktree at `~/hip-roadmap-d181` (branch `d181/index-row-fix`, 4
   commits behind, no unique work) — removed it, created a fresh one at
   `~/hip-roadmap-d184` (branch `d184/misfiled-index-rows`, off `origin/roadmap`
   `402d152`), matching D-156's own precedent shape exactly.
2. **Confirmed the scope before acting on it**: grepped `docs/INDEX.md`'s
   `requirements/` section (lines 83-209) for rows whose file path starts with
   `dispatches/` — 55 hits, all contiguous, immediately after the requirements/
   table's own template row, in newest-first order (D-R-178 at the top, D-90 at the
   bottom) — confirming Bill's own count and the "accumulate at one wrong anchor"
   shape before filing anything.
3. **Moved D-R-178's row** (the one flagged at D-R-179) from the `requirements/`
   table to the `dispatches/` table, in chronological position (between D-R-179 and
   the "R11's 3a gap closed" row), annotated with a note naming the move and pointing
   to TD-R-164 for the other 54.
4. **Filed TD-R-164** (new debt-register version, `v20260805_1411`, LATEST repointed):
   the root cause — every one of `docs/INDEX.md`'s ~14 category tables shares an
   identical four-column header, so an instruction to "add a row to the dispatches
   table" cannot distinguish tables without also matching the preceding
   `## <category>/` header; `requirements/` sits immediately before `dispatches/` in
   file order and absorbed every misplaced row. Spans D-90 through D-162 — the
   project's entire history, not a recent regression. The sweep for the other 54 is
   explicitly deferred, per instruction, to a future dispatch AFTER the anchor fix
   lands (so the sweep's own new rows don't repeat the mistake).
5. **Fixed `CLAUDE.md`'s Workflow item 3**: added an explicit anchor instruction
   (match the exact `## <category>/` header for the doc's own category, never the
   generic table-header text or a nearest-"D-"-prefixed-row heuristic), citing
   TD-R-164 as the evidence. Also fixed an adjacent one-word path typo in item 4
   (`docs/debt/LATEST_DEBT.md` → `docs/techdebt/LATEST_DEBT.md`, the correct path per
   this same file's own Docs Organization section) while already editing the same
   numbered list.
6. Wrote this dispatch doc, registered it in `docs/INDEX.md`'s **dispatches/** table
   (verified by re-reading the section header immediately above the insertion point —
   the exact discipline item 3 above now names), updated `docs/HIP_HANDOFF.md`
   CURRENT STATE, committed and pushed from the worktree under the repo lock, then
   removed the worktree.

## WHAT WAS FOUND

Confirmed structurally, not estimated: all 55 misfiled rows sat in one contiguous
block, `docs/INDEX.md:90-193` at read time, immediately following the `requirements/`
table's own template row. D-156's own `DISPATCH_INDEX_SWEEP` (2026-08-04) checked for
a DIFFERENT gap in the same neighborhood — dispatch docs with NO row at all (14 found)
— and did not catch this one, since it verified a row's EXISTENCE, not its correct
TABLE; both gaps can (and did) coexist.

## VERIFIED

**Watched:** the 55-row grep count, the stale-worktree check (clean, no unique
commits), the post-move counts (54 remaining in `requirements/`, D-R-178's row present
and correctly positioned in `dispatches/`).

**Reasoned about:** the EXACT mechanism by which 54 different dispatches (or sessions)
independently made the same anchoring mistake is inferred from the row pattern
(contiguous, newest-first, immediately after the first identically-shaped table) and
from Bill's own characterization in the dispatch text, not independently reconstructed
per-dispatch — no single session's own reasoning trace was available to confirm HOW
each one located the wrong table.

## HASH

`963382e` — pushed to `origin/roadmap` (from Lane B worktree branch
`d184/misfiled-index-rows`). Filled in by a same-session follow-up edit after the
commit landed. Contains: `CLAUDE.md`, `docs/HIP_HANDOFF.md`, `docs/INDEX.md`,
`docs/techdebt/LATEST_DEBT.md` (repointed), `docs/techdebt/DEBT_REGISTER__v20260805_1411.md`
(new), this dispatch doc.

## OPEN

- **The other 54 misfiled rows are not moved** — deferred to a future sweep, per
  instruction, now that the anchor is fixed so the sweep won't repeat the mistake.
- **Nothing ruled**, per instruction.
