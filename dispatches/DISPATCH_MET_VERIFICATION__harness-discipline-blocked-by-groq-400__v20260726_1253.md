# DISPATCH_MET_VERIFICATION: REQ_HARNESS_DISCIPLINE MET check blocked by a care_coordination Groq 400
Status: BUILT (verification + finding, no code changed)
Reconciled-Against: 830ec2f (working tree carried only the concurrent session's untracked REQ_CHECKLIST_GENERATION file, untouched)
TYPE: VERIFICATION / MEASUREMENT
REQ: REQ_HARNESS_DISCIPLINE__four-part-check-standard-and-sprint-gate__v20260726_0827.md (this dispatch is the owner-session's own MET verification, per the TD-133 session's explicit deferral: "that determination belongs to this REQ's own owner")

## What was attempted

The TD-133/crypto session's post-destruction `--full` (documented in its
INDEX update on the REQ_HARNESS_DISCIPLINE row) answered the condition this
REQ's owner had set for MET: AUDIT 3/3 with no env override against the
really-destroyed key. Per CLAUDE.md item 12 ("done means the FULL RATCHET
passes") and "verify before reporting," this session ran its own `--full`
before flipping any status.

## Result: NOT marked MET

`python -m eval.harness --full` (no env override, post-destruction config,
~12:45 MT): exit 1, RATCHET FAIL — `L2:care_coordination.T01` and
`L2:care_coordination.T02` regressed vs baseline.

Everything this REQ governs was green in the same run: AUDIT 3/3
(four-part-roster PASS across the post-retirement roster — 51 checks, 46
flagged gaps, confirming the TD-133 session's registry reconciliation
merged cleanly with the audit), probes PASS, twin-less fault-injection
PASS, L7 23/23, L7V2 23/24 (1 standing opt-in skip), L3 3/3, L6 1/1,
DISC/SCHEMA/VOICE PASS. The REQ stays NOT MET anyway: its own bar is the
full ratchet, and the full ratchet is red.

## The finding

- T01's reply is the F3 write-confirmation gate template
  (`UNCONFIRMED_UPDATE_REPLY`, server/voice_orch.py:2325) — the detection
  cycle produced zero mutations, so the asserted write never reached the
  graph; T02's recall then correctly finds nothing. The gate behaved
  exactly as designed; the failure is upstream of it.
- Root cause per `logs/harness_server.log` (isolation run, 12:50-12:51 MT):
  `fact_change: groq call attempt 0/1 failed (HTTPError('400 Client Error:
  Bad Request ... api.groq.com/openai/v1/chat/completions'))` then
  `groq call failed after 3 attempts ... fact write silently dropped`.
- Payload-specific, not global: in the SAME full run, near-identical
  medication-switch writes succeeded (`reveal_demo.R04` PASS,
  `three_zone_demo.T04` PASS — "Ray switched from metformin to Jardiance
  10mg"), so the Groq API, key, and write path are alive; only the
  care_coordination Elena payload ("My mother Elena was switched from
  metformin to Jardiance, te...") 400s.
- Reproduced: consecutive `--full` and `--layer 2 --script
  care_coordination` runs within ~10 minutes, identical 3x-retry 400
  signature. NOT a flake by the evidence in hand.
- Timeline: this scenario passed in this session's ~09:00 MT `--full`
  (RATCHET PASS) and in the TD-133 session's post-destruction `--full`
  (which flagged only the unrelated L1:HARNESS1.3 timing flake). The 400
  started between those runs and ~12:45 MT with no commit in that window
  touching `harness/fact_change.py` — consistent with a Groq-side change
  (model deprecation/validation change on this request shape) or a
  payload-content rejection, NOT with today's crypto or audit work.
- Note the failure mode itself: the ERROR log line says "fact write
  silently dropped," and the D-01/fail-open family plus risk-memo §10's
  P2/i019 note already govern this class. The F3 gate made it VISIBLE at
  the reply layer (that is the gate working); the 400's root cause is
  still undiagnosed at the request-payload level.

## What this dispatch did NOT do

No code read beyond diagnosis, no code changed, no retry loops added, no
REQ status flipped, no baseline touched (`--update-baseline` NOT run — the
regression stays loud on purpose). Harness code is the concurrent
session's territory today; the request-payload diff (what exactly differs
between T01's Groq request and R04/T04's) is the next diagnostic step and
belongs to whoever owns the fix.

## Handoff

1. Diagnose the 400 at the request level: log/capture the exact request
   body for care_coordination.T01 vs reveal_demo.R04 (same fact_change
   call site) and diff them. Candidates: prompt length/context growth,
   the `medication_status` schema branch (D-24's territory — T01 is a
   medication-SWITCH utterance), or a Groq-side model/validation change.
2. When the fix lands and `--full` is green, REQ_HARNESS_DISCIPLINE's MET
   determination is ready to make with no further condition: everything
   the REQ itself governs passed in this run, twice (this session's audit
   layers + the TD-133 session's post-destruction run).
