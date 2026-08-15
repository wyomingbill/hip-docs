# DISPATCH_REPORTING_PROTOCOL
Status: BUILT (docs only; no code, no graph, no harness)
Reconciled-Against: 2026-08-03 (D-135; parent dec92f3 at dispatch time)

**TYPE:** GOVERNANCE / FRAMEWORK CHANGE

**REQ:** NONE — a change to CLAUDE.md's own session-conduct rules, on Bill's
direct instruction. No code, no build; item 8's gate does not arise.

## WHAT LANDED — one new CLAUDE.md section, three rules

`## Session Reporting and State (MANDATORY)`, placed immediately after
`## Workflow` and BEFORE the long Requirements Discipline block — deliberate:
a lane asked for STATUS must find the shape in seconds, not after scrolling
past thirteen numbered disciplines.

**1. The STATUS query.** Bill fires the single word STATUS; any lane, any
time, answers in the fixed six-line shape and nothing else — LANE / HOLDING /
IN FLIGHT / TREE / NEEDS BILL / LAST LANDED. Recorded as a POSITION REPORT,
not a summary: no narrative, no evidence, no next steps. Four answering rules
added to make it operable rather than aspirational: answer from the machine
(`git status -sb`, the lock file, `git log -1`) never from memory — a STATUS
answered from recollection is worse than none; no line is ever omitted
(`NONE` and `IDLE` are answers, silence is not); an unestablishable fact
reads `UNKNOWN — <why>` rather than a guess; nothing follows the six lines.

**2. Exception reporting in a queued dispatch.** A session reports at the END,
not per segment; the full report still prints, but its FIRST LINE is exactly
one of the three verbatim strings, before any heading. Recorded as a CLAIM,
not a courtesy: `NOTHING NEEDS BILL` is false if any ruling, decision, or
unresolved question is outstanding; a segment that could not run is a STOP
(second form, naming the segment), not a finding; the third form counts what
was FILED and does not block.

**3. The live handoff document.** `docs/HIP_HANDOFF.md`'s CURRENT STATE is
updated by the lane that LANDS a dispatch, IN THE SAME COMMIT; never
rewritten wholesale; never allowed to describe a past state; and a lane that
cannot honestly update it STOPS rather than landing a commit whose CURRENT
STATE it knows to be false.

## TWO FINDINGS, recorded in the rule itself rather than left to be tripped over

**(a) The document this rule governs does not exist yet.** `docs/HIP_HANDOFF.md`
is absent at HEAD `dec92f3`, has NEVER been committed on any branch
(`git log --all -- <path>` empty), and is in none of the sibling checkouts
(hip-cutover-demo, hip-dev, hip-vo, hip-harness — all checked). D-133 appears
nowhere in this repo's history. The rule therefore carries an explicit
PRECONDITION line: it ARMS when D-133's document lands, and until then a lane
cannot satisfy it and must SAY SO rather than inventing the file. Writing the
rule without that line would have made the next lane's first honest act a
violation.

**(b) A name-collision hazard, one character-class away.** `docs/HIP_CHAT_HANDOFF.md`
EXISTS — a different, older document (2026-07-31, `4172cc8`). A lane told to
"update the handoff doc" could plausibly update it and satisfy nothing. The
rule names both paths and says which is which.

**(c) A Naming Law consequence, flagged not smuggled.** A document that must
always be current cannot obey the never-overwrite rule. The section states the
exemption explicitly — same footing as `INDEX.md`, `BACKLOG.md`, and
`LATEST_DEBT.md` — and warns against "fixing" it by cutting a timestamped
version. This is an inference from the rule's own purpose, not Bill's words;
flagged here so he can overrule it.

## VERIFIED AS VALUES

- `git diff --numstat CLAUDE.md`: **59 insertions, 0 deletions** — pure
  addition; nothing existing was edited or removed.
- Each of the three exception-report strings present **exactly once**
  (fixed-string grep, not pattern).
- All **six** STATUS labels present as line-anchored labels.
- Four section headings landed at the intended position (line 59 onward,
  before Requirements Discipline).

## PROCESS NOTES

- Executed in `~/hip-roadmap-d135` (own worktree from `dec92f3`), per the
  standing preamble; temp branch `d135/reporting-protocol` pushed as
  `d135/reporting-protocol:roadmap`; worktree and branch removed after.
- `.hip-lock` taken in the shared checkout (repo-scoped, advisory):
  read-first (free), noclobber, 15:01:40; released after the push.
- HEAD at dispatch start was `dec92f3` (D-130, R2 typed inference permit) —
  landed by another lane AFTER D-131, so this dispatch built on a tree one
  commit newer than the last one this session landed.
- Docs only: no code, no graph, no harness run.

## OPEN

- The rule's precondition: it is inert until D-133's `docs/HIP_HANDOFF.md`
  lands. Whoever lands D-133 should delete the PRECONDITION bullet in the
  same commit — the rule then stands unqualified.
- The Naming Law exemption in finding (c) is my inference; Bill may overrule.
- Nothing ruled MET; nothing else changed.
