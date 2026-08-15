# DISPATCH_COMPLETION_ALERT
Status: BUILT
Reconciled-Against: 2026-08-04 (D-162; parent `d846460`)

**TYPE:** BUILD (one script) + FRAMEWORK RULE

**REQ:** NONE — session-conduct tooling on Bill's direct instruction. No governed
behaviour changes, no graph, no harness. Nothing ruled.

## THE PROBLEM, AS DIAGNOSED IN THE DISPATCH

D-153 was silent while D-149 and D-150 rang. Not because the rule was ignored — because
**a session reads `CLAUDE.md` once, at startup, and then works from what it remembers.**
Every edit to a rule therefore reaches only sessions that start afterwards. The alert rule
had landed between those dispatches, so two sessions knew it and one could not.

## WHAT WAS BUILT

`scripts/dispatch_done.sh`, one argument, matched to the report's own first line:

```
scripts/dispatch_done.sh complete    # ALL SEGMENTS COMPLETE — NOTHING NEEDS BILL
scripts/dispatch_done.sh findings    # COMPLETE WITH FINDINGS — N ITEMS FILED …
scripts/dispatch_done.sh stopped     # STOPPED AT SEGMENT N — NEEDS BILL
```

**Prints nothing on success; the sound is the whole output.** On failure it writes one line
to stderr and exits non-zero — `2` for a usage error (no argument, unknown outcome, extra
arguments), `3` for an environment failure (`afplay` absent, sound file unreadable,
playback failed). The distinction matters: a session can tell "I called it wrong" from "the
machine could not ring", and report the second honestly rather than leaving Bill to read
silence.

Verified across every path: `complete`, `findings`, `stopped` each exit 0 with empty
stdout AND stderr; no-argument, unknown-argument and two-argument calls each print one
stderr line and exit 2.

## WHAT THE RULE NOW SAYS, AND WHY IT NAMES A SCRIPT

CLAUDE.md's STANDARD PREAMBLE item 6 no longer names sound files. It names the command,
and says why: **the script owns which sound plays, how many times, and what happens when
the sound is missing.** A session must remember one stable line. The sound, the repetition
count, and the failure handling can all change without a single open session needing to
relearn anything — which is the only part of the staleness problem a file edit can fix.

## WHAT THIS DOES NOT FIX — recorded as a limit, not a footnote

The rule now carries these in its own text, because a limit that lives only in a dispatch
doc is a limit nobody reads at the moment it matters:

- **A session that never calls the script rings nothing.** Nothing enforces the call. It is
  a convention a session follows or forgets — exactly what the lock was before D-146 made
  acquisition a precondition of the tooling rather than a step.
- **A session that dies mid-run rings nothing.** A crash, a killed process, an interrupted
  turn: all produce the same silence as a dispatch still working.
- **A session that began before this rule landed does not know to call it at all.** This is
  the original defect and **this dispatch does not fix it.** Naming the script fixes the
  cost of changing the SOUND; it does nothing about the staleness of the RULE. Any session
  currently open — including one reading this — may be working from a CLAUDE.md that
  predates D-162.
- **Therefore silence means only that no sound was played.** Running, stuck, finished,
  failed: all four are silent. **SILENCE IS NOT PROOF OF PROGRESS.** The report is the
  evidence; the sound is a convenience laid on top of it.

**The durable fix is named in the rule and deliberately not built here:** a harness-level
hook that fires on session stop regardless of what any session remembers. That is the only
shape that survives session age, because it does not depend on a session having read
anything. It belongs to the harness configuration, not to this repo's framework file, and
building it was not this dispatch's ask.

## PROCESS NOTES

- STANDARD PREAMBLE observed; machine gate passed (`bill-ai` / `[REDACTED-MACHINE-NAME]`
  / `~/hip-roadmap` / `roadmap` — the mini, not the laptop).
- **Dispatch numbering confirmed against the log, not assumed:** last logged plain-numbered
  dispatch is **D-160**; another lane is running its own `D-R-161` sequence concurrently.
  D-162 is unambiguous.
- Own worktree `~/hip-roadmap-d162`, temp branch `d162/alert-script`, removed after push.
  **A stale worktree from the stopped D-161 banking dispatch was cleared first** — it held
  no work, and stray worktrees are the wrong-checkout hazard this project has already paid
  for.
- Another lane is mid-build in the shared checkout (`harness/epistemic_ledger.py` modified,
  `eval/test_ledger_hash_versioning.py` untracked, plus `harness/injection_contract.py`);
  explicit pathspecs and a surgical INDEX stage keep this commit clear of all of it.

## OPEN

- The harness-level stop hook, if Bill wants the alert to survive session age rather than
  merely survive sound changes.
- Nothing ruled.
