# DISPATCH_RESIDUALS_D141
Status: BUILT (docs only; no code, no graph, no harness)
Reconciled-Against: 2026-08-03 (D-141; parent `c5c9202` at dispatch time)

**TYPE:** GOVERNANCE / RULING-RECORD + DOC SUPERSESSION

**REQ:** NONE — a ruling record and a status correction on Bill's direct instruction. No
code, no build.

## 1. THE COLLISION — `docs/HIP_CHAT_HANDOFF.md` marked SUPERSEDED IN PLACE

A status header was PREPENDED; **the body was not touched** (25 insertions, 0 deletions —
verified). The header carries: `Status: SUPERSEDED (D-141, 2026-08-03)`, `Superseded-By:
docs/HIP_HANDOFF.md`, and a blockquote that (a) tells the reader to follow the live handoff
instead, (b) names the specific instruction that is now WRONG — its line ~11 "OUTPUT:
dispatches PRINT full report to terminal", superseded by D-136's route-by-size rule — while
recording that its parenthetical about blank copies remains CORRECT and is now the reason
`open -e` is forbidden, and (c) names the other snapshot-only contents (dispatch numbering
at D-54, the two-sessions-by-screen-position convention, the lock inventory).

Not deleted: its provenance is real, and a superseded record that still says what was true
on 2026-07-31 is worth more than a gap. D-136 found this contradiction and correctly
declined to edit another lane's artifact; D-141 supersedes it on Bill's instruction, which
is what makes the edit legitimate rather than a lane reaching across.

## 2. THE NAMING LAW EXEMPTION — RULED, and recorded where the law lives

New subsection under `## Naming Law`: **"The never-overwrite exemption — a CLOSED list
(Bill's ruling, 2026-08-03)"**, naming exactly four documents — `docs/INDEX.md`,
`docs/BACKLOG.md`, `docs/techdebt/LATEST_DEBT.md`, `docs/HIP_HANDOFF.md` — with the reason
recorded so it is not re-derived: *a document whose entire job is to be CURRENT cannot obey
a rule that forbids updating it in place; versioning one does not preserve history, it
produces two documents that both claim to be current — the failure the Naming Law exists to
prevent, arriving by the opposite route.* The list is CLOSED: adding to it is a ruling.

The provenance is recorded honestly: first stated as a session's INFERENCE and flagged for
overrule, now **confirmed as Bill's ruling, not a session's**. The live-handoff subsection's
bullet no longer states the exemption itself — it points at the Naming Law, so the rule
lives in one place.

**Attribution correction, minor:** the dispatch attributes the original inference to D-136.
It was written at **D-135** (in the live-handoff rule) and flagged for overrule in D-135's
dispatch doc as finding (c); D-136 was the routing-rule dispatch. Recorded here so the
provenance chain reads correctly; nothing about the ruling changes.

## 3. THE LIVE HANDOFF, updated in the same commit — as its own rule requires

`docs/HIP_HANDOFF.md`'s **CURRENT STATE** now records D-141 as last-landed and HEAD as
`c5c9202`, and its Status line cites Bill's ruling rather than the superseded inference.
This is the first dispatch to land under that rule since it was armed at D-137; updating
CURRENT STATE was a condition of committing, not a courtesy.

## VERIFIED AS VALUES

- `docs/HIP_CHAT_HANDOFF.md`: **25 insertions, 0 deletions** — header only, body byte-intact
  (the original first body line and the superseded instruction both still present).
- `CLAUDE.md`: 21 insertions / 3 deletions (the 3 being the replaced inference bullet); the
  closed-list heading, the CLOSED sentence, the D-141 attribution, and the pointer bullet
  each present exactly once under a whitespace-collapsed scan.
- `docs/HIP_HANDOFF.md`: 11 insertions / 7 deletions — Status line and CURRENT STATE only.

## PROCESS NOTES

- STANDARD PREAMBLE observed. Machine gate passed. **Lock READ FIRST** — free at 16:12:10
  (the banking lane had released it) — then taken with `set -o noclobber`; released after
  the push.
- Own worktree `~/hip-roadmap-d141` from `origin/roadmap`; temp branch `d141/residuals`
  pushed as `d141/residuals:roadmap`; worktree and branch removed after.
- Docs only: no code, no graph, no harness.

## OPEN

- Nothing from this dispatch. Both D-136/D-137 residuals are closed.
- Nothing ruled MET; the only ruling recorded is the exemption, which is Bill's.
