# DISPATCH_TD147_HANDOFF
Status: BUILT (analysis + register filing; no code changed)
Reconciled-Against: 2026-08-03 (D-119; parent d01e3ad at dispatch time)

**TYPE:** MEASUREMENT/ANALYSIS + TD FILING

**REQ:** NONE — read-only diagnosis per TD-147's handoff plus a register
filing; no build occurred, and D-119's own step 3 is "Change no code."

## THE ASK (D-119, condensed)

> 1. TD-147's handoff: diff the FAILING smoke payload's fact_change request
>    against a SAME-RUN SUCCEEDING one, at the call site. (a) what differs;
>    (b) payload-correlated or arbitrary — TEST the "payload-biased" claim;
>    (c) did the turns_demo success use a different request shape or luck;
>    (d) what is in HIP's control. STOP if (b) says arbitrary.
> 2. File the lock protocol as a TD — D-107 write-through and D-118
>    clobber, plus the thrice-flagged timestamp drift, folded in.
> 3. Change no code. Rule nothing MET.

## HEADLINE — THE RECORDED MECHANISM WAS WRONG, AND THE DIAGNOSIS CHANGES

**TD-147's filed mechanism ("a Groq-side ReadTimeout on retry dropped the
write") is INCORRECT, and so is its "same utterance extracted fine in
turns_demo" claim. Both were mine (D-117/D-118); both are corrected here
and in a TD-147 ADDENDUM, per the DISPATCH_44 / TD-139 correct-in-the-new-
record precedent.** What the instrumentation actually shows:

- `logs/write_latency.jsonl` (DIAG-1, 1,876 records): the failing turns in
  BOTH runs recorded `kind=detect_no_changes, groq_status=ok,
  groq_attempts=1`. **The HTTP calls SUCCEEDED on their first attempt and
  gpt-oss-20b returned `changes: []`.** The one observed ReadTimeout
  (harness_server.log:78) was attempt-0 of the SEMANTIC-RETRY call and
  recovered inside `_call_groq`'s own transport retries — no call
  ultimately failed. Across the ENTIRE latency log there are exactly 3
  hard call-failures (`detect_no_result`), all owner=bill, all HTTPError,
  none today's failing turns. **Transport is exonerated.**
- `turns_demo.jsonl` contains ZERO turns with this utterance. Its G1 PASS
  is vacuous with respect to this shape — my earlier claim conflated it
  with the real same-run successes, which live in harness_run itself.

## (a) WHAT DIFFERS BETWEEN THE FAILING AND SUCCEEDING REQUESTS

The smoke sequence asserts the IDENTICAL utterance five times per run —
maya, sam, sam again, sam a third time, bill (file order; positions
identical in both runs). Same system prompt, same `_USER_TEMPLATE`, same
utterance string. **The only varying request component is `facts_block`** —
`detect_and_apply` reads the owner+household active set FRESH per call
(TD-121's full-read design, `read_user_facts(owner, limit=None)`).

| instance (file order) | delta | outcome |
|---|---|---|
| maya | 1 | write_committed |
| sam #1 | 1 | write_committed — **writes the fact** |
| **sam #2 (next record)** | **0** | **detect_no_changes → F3 refusal → the G1 red** |
| sam #3 (12 turns later) | 1 | write_committed |
| bill | 1 | write_committed |

The failing request is the one whose `facts_block` contained **the
identical just-written fact** (sam #1 landed it seconds earlier). Sam #1's
request lacked the fact (new → change). Sam #3's request had the fact AND
~12 intervening household turns' worth of grown context — and extracted a
change again. Exact request byte-sizes are not recorded by DIAG-1 (it
captures timing/status, not bodies); the content difference is established
from the write ordering, not assumed.

## (b) PAYLOAD-CORRELATED OR ARBITRARY? — CORRELATED, AND THE STOP DOES NOT FIRE

Tested, not repeated: outcomes are **position-stable across two independent
full runs** — six sam calls (3 per run): #1 ✓✓, #2 ✗✗, #3 ✓✓. The
temperature-0.2 semantic retry ALSO returned zero on #2 in both runs. That
is deterministic-given-payload behavior (matching the risk-memo §10
P2/i019 finding: "gpt-oss-20b returns changes:[] for some multi-party
contexts, confirmed deterministic at temperature=0.0"), not an arbitrary
availability failure. **D-119's STOP condition ("if (b) shows it is
arbitrary") does not fire.** "Payload-biased" survives testing, with a
sharper statement: the bias is at the level of a PAYLOAD CLASS —
**restatement-of-an-already-recorded-fact** — not of this literal string
(the same string succeeds when the fact is absent, and even flip-side
succeeds at position #3 with a larger context).

## (c) THE SUCCEEDING SAME-RUN INSTANCES — DIFFERENT REQUESTS, NOT LUCK

Correction on the record: not turns_demo (see HEADLINE). The same-run
successes are the four sibling instances in harness_run. Each succeeded
with a **materially different request document** — fact absent (maya,
sam #1, bill on his own graph) or context grown (sam #3). No evidence
supports "got lucky on timing": timing was healthy everywhere (1 HTTP
attempt, sub-timeout latencies), and the one instance with the
just-written-fact-present payload failed BOTH runs, retry included.

## (d) WHAT IS IN HIP'S CONTROL — REAL LEVERS EXIST; THIS IS NOT AVAILABILITY

The F3 gate's own design comment (server/voice_orch.py:2314-2315) already
handles restatements: "**mutations==0 with noops>0 is NOT gated — the
value was already current, so the ack is truthful.**" The defect is that
the model returns `changes:[]` instead of EMITTING the restated fact (which
apply would classify as an idempotent no-op → truthful ack). The failure
starves the exact path built for it. Levers, scoped not built:

1. **Extraction-prompt semantics** (model-side, cheap to test): instruct
   the extractor to emit a restatement as a change (idempotent re-assert)
   rather than omitting it; testable against the P2/i019 corpus plus this
   smoke shape.
2. **Structural restatement detection** (model-free, HIP-only): before
   `UNCONFIRMED_UPDATE_REPLY` fires on a zero-changes declarative, check
   the graph directly — if the asserted (subject, attribute) holds an
   ACTIVE value consistent with the utterance, the truthful reply is a
   match-ack, not a failure claim. Fix shape and its G1 interaction are
   Bill's to rule (the ack must ground in the existing fact for G1's
   exemption logic).
3. **Retry policy: already saturated for this class.** The semantic retry
   at temp 0.2 returned zero deterministically both runs; more identical
   retries buy nothing. Transport retries/timeout tuning are IRRELEVANT
   here — transport never failed.
4. **Model choice / n-best**: heavier levers if 1-2 prove insufficient.

Answer to the dispatch's dichotomy: **NOT "entirely a Groq-side
availability issue."** It is a model-semantics defect on a nameable payload
class, with at least one fully HIP-side structural lever (2) that requires
no Groq cooperation at all.

Historical footnote that raises confidence this is the right frame: this
utterance IS the F3 gate's own founding case — risk-memo §9 item 0 records
that the plain-declarative form "I take atorvastatin 20mg every morning"
once skipped the supersede-phrase check entirely and shipped a false ack;
the gate was widened to every declarative because of it. The G1 red is the
same lineage biting one layer down: the gate now fires, but on a
restatement it fires FALSELY (the record was not lost; it already exists).

## TD-148 FILED — the lock protocol (register v20260803_1027)

Two failures in one effort, same class — the lock is advisory with no
enforcement:
- **D-107 (2026-08-02): write-through** — the demo-cutover lane wrote REQ +
  dispatch + INDEX rows into ~/hip-roadmap while `.hip-lock` was held by
  the roadmap lane's D-107.
- **D-118 (2026-08-03, 08:56:33): clobber** — a session (this one) took the
  lock with a bare `>` after a mere existence check and OVERWROTE an
  existing lock unread; holder fields destroyed, holder never identified.
  Corroborating trace: `harness_run.jsonl` was archived at 08:57:34 by an
  unidentified process (`harness_run.20260803T145734Z_872ad0c.jsonl`) —
  the clobbered holder was plausibly starting a harness run one minute
  after losing its lock.
- **Folded in (no TD existed — checked): the thrice-flagged timestamp
  drift** — HIP_CHAT_HANDOFF.md:15 ("'taken:' timestamp drifts hours from
  mtime — likely why concurrent sessions both think they hold the lock.
  Cheap fix pending, not yet done"), its pending-list entry (:119), and
  the 2026-08-01 live observation of the D-91 lock.

Fix scope NAMED, not built, per the dispatch: read-before-write (read and
report holder fields; defer if held); atomic noclobber creation (O_EXCL /
`set -o noclobber`, or mkdir-as-lock); a liveness field that cannot drift
(holder PID + filesystem-derived heartbeat mtime, refreshed during long
dispatches, with 'taken:' cross-checked against mtime at read); a dead-
holder policy (liveness probe fails + heartbeat stale beyond threshold →
takeover permitted ONLY with a recorded supersession note preserving the
dead lock's fields); same discipline extended to the two doc-scoped locks
(`docs/.INDEX_MANIFEST_LOCK`, `docs/.GRAPH_HARNESS_LOCK`).

## PROCESS NOTES

- Gate passed. Lock taken per the new protocol: READ FIRST (absent), then
  noclobber write — 10:20:12 MT. Released after push.
- Repo `.env.dev` only. No code changed. Nothing ruled MET.
- Committed AROUND the cutover lane's WIP (same four docs + INDEX rows),
  explicit pathspecs, surgical INDEX stage.

## VERIFIED

- **Read from instruments, not inferred:** the per-call groq_status/
  attempts for both runs' failing turns (write_latency.jsonl, matched by
  turn_id); the five-instance pattern and its file order (both archived
  harness_run files); turns_demo's zero atorvastatin turns (grep, read as
  a value); the whole-file failure census (3 detect_no_result, all bill/
  HTTPError).
- **Reasoned about:** facts_block content at each instance (from write
  ordering + TD-121's full-read design; bodies not recorded by DIAG-1 —
  stated as such, not overclaimed).

## OPEN

- Which lever (d.1 structural, d.2 prompt, both) — Bill rules; TD-147
  stays OPEN with its addendum until a fix dispatch lands.
- TD-148's build — awaits its own REQ per the register's GOVERNED rule.
- The clobbered lock's holder identity — the 08:57:34 archive trace is the
  best remaining evidence if a lane reports a lost lock or a vanished
  harness run.
