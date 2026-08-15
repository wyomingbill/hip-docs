# DISPATCH_RULING_D131
Status: BUILT (docs only; no code, no graph, no harness)
Reconciled-Against: 2026-08-03 (D-131; parent f840161 at dispatch time)

**TYPE:** GOVERNANCE / DOC CORRECTION under Bill's ruling

**REQ:** NONE — a ruling-directed doc-shape change; no code, no build.

## THE RULING (Bill, 2026-08-03) — shape (i), THE POINTER — applied

Both count-carrying regions of `REQ_STRUCTURAL_CEILING v20260802_2205`
now carry a pointer and no numbers, with THE REASON recorded in the same
edit that removed the number, per the instruction:

- **Header**: "Rulings are recorded per-requirement in section 16, the
  sole authoritative record. This header deliberately carries no count
  and no enumeration." The reason, verbatim in substance: five flags in
  five weeks (D-88, D-92, D-100, D-120, and D-129's own re-count) is the
  evidence that the count was never reliable enough to glance at, so the
  at-a-glance summary it cost is a summary nobody could trust; a pointer
  cannot age; shape (ii) would keep the count and add a parser with its
  own failure modes, and the count would still lie between an edit and
  the next run.
- **§16 intro**: same pointer, same reason, same edit — including the
  record that this very paragraph's "updated in the same edit" promise
  was broken once (D-113). The ruling-history NARRATIVE sentences are
  retained (R30's backfill sequence, R1/R10 together, R12's two stages)
  because they are history, not counts. The closing rule is now
  count-free: "a requirement without an entry below is FILED with
  acceptance NOT run."
- **§16's per-requirement entries are untouched** — they are the record.

## VERIFIED AS VALUES (wrap-tolerant, per the house lesson)

Whole-file, whitespace-collapsed scan: `ARE RULED` 0, `of 30
requirements` 0, `Of those, MET` 0, `have been ruled` 0. The pointer
phrase present exactly twice (header + §16 intro). Nine `### R<n>`
status headings intact in §16. First-pass single-line greps miscounted
in BOTH directions (a wrapped pointer phrase read as missing; a window
artifact read as a leftover) — re-verified wrap-tolerantly before
trusting either number, which is the D-116/D-117 lesson applied to my
own verification.

## PROCESS NOTES — the OWN-WORKTREE constraint

- Executed in `~/hip-roadmap-d131` (fresh worktree from f840161), per the
  dispatch — NOT in ~/hip-roadmap. Because git forbids checking `roadmap`
  out twice, the worktree carried temp branch `d131/preamble-pointer`;
  pushed as `d131/preamble-pointer:roadmap`; worktree and temp branch
  removed after the push (stray worktrees are the wrong-checkout hazard
  the runbook names). Gate: user/host verified; the path check is
  satisfied by the dispatch's own constraint.
- `.hip-lock` taken in the SHARED checkout (~/hip-roadmap) — the advisory
  lock is repo-scoped — read-first (free), noclobber, 13:48:01; released
  after push.
- **RECONCILIATION NOTE for ~/hip-roadmap**: its `roadmap` checkout is
  now one commit behind origin and its worktree carries the cutover
  lane's uncommitted INDEX rows. The next `git pull --ff-only` there will
  refuse over the dirty `docs/INDEX.md`; the clean sequence is: save the
  four cutover rows (they are pure additions), reset INDEX to HEAD, pull,
  re-apply the rows. Left for whichever session next works that checkout,
  ON PURPOSE — this dispatch was ordered not to touch it.
- Docs only: no graph access, no harness run, no code.

## OPEN

- ~/hip-roadmap's ff-pull reconciliation (above).
- Nothing ruled MET; nothing else changed.
