# DISPATCH_REPORT_ROUTING
Status: BUILT (docs only; no code, no graph, no harness)
Reconciled-Against: 2026-08-03 (D-136; parent 9d57769 — D-135, landed minutes earlier this
session)

**TYPE:** GOVERNANCE / FRAMEWORK AMENDMENT

**REQ:** NONE — a change to CLAUDE.md's own session-conduct rules on Bill's
direct instruction. No code, no build.

## WHAT LANDED — one new subsection, amending D-135's reporting rule

`### Where the report goes — ROUTE BY SIZE`, inserted between the
exception-reporting rule and the live-handoff rule, plus a two-line rewording
of the lead-in above it (the old "The full report still prints" presumed one
destination; the first-line rule now reads "wherever the report goes —
routing rule below").

**A report is delivered by its size, not by habit. Two routes, one forbidden:**

- **SHORT → TERMINAL.** A screen or two: docs-only dispatches, ruling
  dispatches, gate checks. Bill screenshots them.
- **LONG → THE DISPATCH DOC** in `docs/dispatches/` — explicitly *the doc this
  dispatch is already writing* under Requirements Discipline item 9, NOT a
  second artifact (the failure mode worth pre-empting: a lane writing the
  report twice, in two places, which then disagree). Long means any BUILD
  dispatch, any dispatch with a HARNESS RUN, anything with PER-ROW EVIDENCE.
  The terminal then gets ONLY three things, in order: the status first-line,
  the file path, the commit hash. Bill drags the file into chat. Nothing else
  — "not a summary of the summary, not the highlights," because a partial
  terminal report re-creates the size problem the routing rule exists to solve.
- **FORBIDDEN: `open -e`, and asking Bill to copy out of TextEdit.** The
  reason is recorded in the rule so no session re-derives it by failing again:
  **that route FAILS — the copy arrives blank.** Dragging the file works; it
  is how the D-63 axes document and the REQ drafts moved.

## WHY THIS AMENDMENT EXISTS AT ALL — the route this session used and lost

D-118 already ruled the `/tmp` + `open -e` handoff broken and this session
carried "terminal only" ever since (it is in my session memory from that
ruling). What D-118 did not resolve was what to do when the report is too
long for a screenshot — so long reports kept going to the terminal anyway,
which is the gap D-136 closes. The `docs/dispatches/` doc was always the
right destination: it already exists, it is already committed, it is already
the durable record. The amendment routes to it rather than inventing a
delivery mechanism.

## VERIFIED AS VALUES

- `git diff --numstat CLAUDE.md`: **20 insertions, 2 deletions** — and the
  two deletions audited: they are exactly the reworded lead-in lines, nothing
  else removed.
- Wrap-tolerant scan (whitespace-collapsed, the D-116 lesson applied to my own
  verification — a first-pass single-line grep for "the copy arrives blank"
  read 0 because the phrase wraps): "the copy arrives blank" ×1, "D-63 axes
  document and the REQ drafts moved" ×1, "Bill drags the file into chat" ×1.
- The three exception-report strings still present **exactly once each** —
  D-135's rule was amended, not damaged.

## FINDING — a stale contradicting instruction, flagged NOT edited

`docs/HIP_CHAT_HANDOFF.md:11` still reads *"OUTPUT: dispatches PRINT full
report to terminal; Bill SCREENSHOTS (terminal-copy and file-open both arrive
blank for Bill)"*. Its parenthetical agrees with the forbidden-route reason;
its instruction now contradicts the routing rule for long reports. CLAUDE.md
governs, and that file is another lane's older artifact likely superseded by
D-133's handoff document when it lands — so it is reported here, not edited
(D-131's lesson: do not touch what the dispatch did not name).

## PROCESS NOTES

- Executed in `~/hip-roadmap-d135` — the SAME worktree D-135 used, because
  D-136 arrived mid-turn amending the very rule D-135 was landing. Two
  dispatches, two commits, one worktree; D-135 (`9d57769`) pushed before this
  one was written, so the amendment sits on top of the rule it amends rather
  than being folded into it.
- Temp branch `d135/reporting-protocol` pushed as
  `d135/reporting-protocol:roadmap`; worktree and branch removed after.
- `.hip-lock` taken in the shared checkout, read-first (free), noclobber,
  15:01:40 (held across both dispatches); released after this push.
- Docs only: no code, no graph, no harness.

## OPEN

- `docs/HIP_CHAT_HANDOFF.md`'s contradicting line (above) — needs either an
  edit dispatch or supersession by D-133's document.
- Nothing ruled; nothing else changed.
