# DISPATCH_D03_D18
Status: BUILT
Reconciled-Against: 3c0cb74

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_D03_D18__confirmation-gate-no-fallthrough__v20260716_1806.md`
(parent: `REQ_VOICE_DEMO__one-screen-script-plus-live-voice__v20260715_1601.md`
— this dispatch blocks that REQ's acceptance-test item 2, "run a script to
completion," on script 3/`trust_ladder`). Filed BEFORE any code touched this
session, per CLAUDE.md item 8.

## THE ASK

Bill's dispatch, verbatim:

> "D-03/D-18. Second half of §9 item 0 in the amended risk memo (792889f).
> Parent requirement: REQ_VOICE_DEMO. This blocks script 3 — it is the
> fourth turn and the only thing between two working demo scripts and one.
>
> THE DEFECT
>
> T04 "Yes, confirm that." classifies as intent=noise. The confirmation gate
> is never invoked. The turn falls through to the model, and the model says
> "Got it, confirmed." Neo4j immediately after: same two fact_ids, same
> write_state (supersede/unresolved). Nothing promoted.
>
> HIP announces an action it did not take. The record is CORRECT — it says
> unresolved. Only the human was lied to. Nothing in the ledger would ever
> surface this.
>
> Two symptoms, one root cause, both live-observed across 5 runs:
>   3 of 5 — fabricated date confirmation ("Got it, I'm confirming today is
>            Thursday, July 16, 2026...")
>   2 of 5 — D-18 instruction leak: the model confirms its own SYSTEM PROMPT
>            back to the user ("Got it, I'll stick to using English and
>            respond with two to three short sentences as directed")
>
> THE FIX
>
> Your own review's verdict: the confirmation gate must never fall through
> to the model. Not a wider classifier. Not more exemplars. If a park is
> standing and the turn is a response to it, the gate owns the turn —
> confirm, decline, or say plainly it did not understand. The model does
> not speak.
>
> Same shape as the fix you just shipped on the write path: the system had
> the state in hand and let the model talk anyway.
>
> Note _PENDING_PARK_REPLY_TPL and PARKED_UPDATE_REPLY no longer invite
> "say yes" — the invitation was stripped because HIP cannot invite an
> interaction it cannot honor. Once D-03 works, that is a separate decision
> about putting it back. Do not put it back in this task.
>
> PROVE IT LIVE, FORCED. You set the standard yourself with the real 401 on
> the zero-write gate. Structural proofs passed and the live path failed
> twice.
>
>   1. park standing, "Yes, confirm that."   -> PROMOTED. Verify in Neo4j:
>      fact_id, write_state, rung. Not the reply text.
>   2. park standing, "yes"                  -> same
>   3. park standing, "No, leave it."        -> park closed, head stands
>   4. park standing, "What's the weather?"  -> gate does NOT eat an
>      unrelated turn
>   5. NO park standing, "Yes, confirm that." -> does not invent something to
>      confirm
>   6. trust_ladder 5x -> T01/T02/T03 unchanged and still 5/5, T04 now works
>
> The invariant: the gate must never produce a confirmation string without a
> promotion behind it. If a turn cannot be classified confirm or decline, it
> says so. That is the whole defect.
>
> Register D-03 and D-18 as fixed only after you have watched all six pass.
>
> Push, report the hash."

## WHAT WAS DONE

1. Filed `REQ_D03_D18` (per CLAUDE.md item 8) before touching code — THE
   REQUIREMENT quoted verbatim, THE ACCEPTANCE TEST as the six turns above,
   parent REQ named, constraint against reintroducing the stripped "say
   yes" invitation recorded explicitly.
2. Read `harness/confirmation_gate.py` in full: `check_confirmation`,
   `YES_VOCAB`/`NO_VOCAB`, `apply_confirm`/`apply_decline`, TTL/expiry logic.
3. Read `server/voice_orch.py`'s confirmation-gate dispatch block
   (`process_text_query`, around line 2502) to see exactly where a `"pass"`
   verdict fell through to ordinary SIA classification + generation.
4. Implemented the fix: `check_confirmation` now also matches "yes"/"no" as
   the leading normalized word (not just the exact `YES_VOCAB`/`NO_VOCAB`
   phrase), and a declarative utterance matching neither returns a new
   `"unclear"` verdict the gate owns directly (`UNCLEAR_CONFIRMATION_REPLY`)
   — never falling through. A genuine question still passes through via the
   same `is_declarative_utterance` axis the earlier F3 fix (`c86a414`) used.
5. Ran all six acceptance-test turns live against `server.voice_orch.
   process_text_query` on real dev Neo4j (`bolt://localhost:7688`) and real
   Groq/Ollama — no mocks — using fresh `scripts/demo_reset.py --yes` +
   `scripts/demo_seed.py` between isolated cases (P8's trust-regression
   check means a promoted head is no longer CORROBORATED, so re-parking
   against a polluted graph silently stops parking; each case ran against a
   clean D9 CORROBORATED metformin head unless it was the deliberate
   trust_ladder sequence).
6. Registered D-03 and D-18 as FIXED in `HIP_DefectRegister__v20260715_1930.md`,
   updated `MANIFEST.md` Section B, updated `docs/INDEX.md`, updated the
   `trust_ladder__v20260716_1600.json` demo script's stale "DO NOT RUN T04"
   warning.
7. Logged TD-126 (found during live proof, not this dispatch's target):
   `scripts/demo_reset.py`'s hardcoded `~/hip-harness` paths deleted maya/
   sam's voiceprints on the frozen demo checkout — flagged, not fixed,
   inside this same dispatch's constraints (fixing it was out of scope for
   a confirmation-gate REQ).
8. Committed and pushed: `3c0cb74`.

## WHAT WAS FOUND

- `harness/confirmation_gate.py:109-143` (pre-fix): `check_confirmation`
  returned `("pass", token)` for ANY utterance not an exact `YES_VOCAB`/
  `NO_VOCAB` match while a token was pending. `server/voice_orch.py:2510`
  (pre-fix) treated `"pass"` identically to `"none"` (no token at all) —
  both fell through to ordinary classification and generation. `"Yes,
  confirm that."` classifies `intent=noise`; nothing downstream knew a
  confirmation had been attempted and missed, so the model free-associated
  an answer.
- Fix: `harness/confirmation_gate.py` — leading-word check added to the
  YES/NO branches; new `"unclear"` verdict for a declarative match-neither
  case; `UNCLEAR_CONFIRMATION_REPLY` constant added. `server/voice_orch.py`
  dispatch block extended to own `"unclear"` the same as `"confirm"`/
  `"decline"`, never letting it reach the model.

## VERIFIED

**Watched run — all six, live, Neo4j state checked directly (not reply
text) for the first three:**
1. `"Yes, confirm that."` — `write_state` `unresolved`→`supersede` on the
   SAME `fact_id` (`af211251-…`). `CONFIRM_REPLY` spoken. PASS.
2. `"yes"` — same transition, fresh park (`fact_id 33c10b7e-…`). PASS.
3. `"No, leave it."` — parked row closed (`valid_to` set, `closed_by
   ='declined'`, read directly via Cypher); metformin head (`89af7b51-…`)
   untouched. `DECLINE_REPLY` spoken. PASS.
4. `"What's the weather?"` with park standing — real weather answer
   returned; `confirmation_gate.peek('maya')` confirmed the token STILL
   pending afterward (TTL decremented, not consumed). PASS.
5. `"Yes, confirm that."`, sam, no park pending — `peek('sam')` was `None`
   before and after; ordinary model chatter, nothing invented, nothing
   promoted. PASS.
6. `trust_ladder` T01→T04, 5 runs, fresh reset+reseed each: T01-T03 text
   identical across all 5 runs; T04 → `CONFIRM_REPLY` + Jardiance
   `unresolved`→`supersede` in Neo4j, 5/5. PASS.

**Reasoned about:**
- That the fix does not regress any OTHER confirmation-adjacent code path
  beyond what the six turns exercise — the change is narrowly scoped
  (`check_confirmation` + one dispatch branch), and the existing
  `tests/test_injection_declarative.py` suite (16 tests, unrelated to this
  gate but exercising `is_declarative_utterance`, the shared discriminator)
  was re-run and passed, but this is inference from a nearby suite, not a
  dedicated regression test for `confirmation_gate.py` itself (none exists).

## HASH

`3c0cb74`

## OPEN

- No dedicated unit test exists for `confirmation_gate.py`'s new branch
  logic — the six live turns are the only verification on file. A future
  regression would currently only be caught by re-running those turns live,
  not by an automated suite.
- The residual gap named in `REQ_D03_D18` itself: a declarative confirmation
  attempt with no yes/no signal word at all (e.g., "sure, whatever") still
  reaches `"unclear"` only if it's declarative-shaped; anything ambiguous in
  a stranger way than the two reproduced symptoms was not exhaustively
  enumerated, only the reproduced cases were closed.
- TD-126 (demo_reset.py cross-checkout damage), found inside this dispatch's
  live-proof work, is explicitly NOT fixed here — see
  `docs/dispatches/DISPATCH_TD126__speaker-verification-floor-analysis__v20260716_1846.md`
  and the follow-on BUILD dispatches for its two code fixes.
