# REQ_D03_D18
Status: BUILT
Reconciled-Against: a067275 (code shipped this session; see commit for hash)

Parent requirement: `docs/requirements/REQ_VOICE_DEMO__one-screen-script-plus-live-voice__v20260715_1601.md`.
This is not a new requirement track — it is the specific defect blocking that
REQ's acceptance-test item 2 ("run a script to completion") on script 3
(`trust_ladder`). D-03/D-18 are the only thing between two working demo
scripts and three.

## THE REQUIREMENT

Bill's words, verbatim:

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
> about putting it back. Do not put it back in this task."

## THE ACCEPTANCE TEST

Six live turns against `server.voice_orch.process_text_query` (real Neo4j,
real Groq/Ollama, no mocks). Verified by **Neo4j state (`fact_id`,
`write_state`, rung), not reply text**, per turns 1-3:

1. Park standing, `"Yes, confirm that."` → parked row PROMOTED
   (`write_state` supersede/ASSERTED-equivalent, `confirmation` set).
2. Park standing, `"yes"` → same (already worked via exact `YES_VOCAB`;
   confirms the fix does not regress the working exact-match path).
3. Park standing, `"No, leave it."` → parked row closed
   (`closed_by='declined'`), head stands unchanged.
4. Park standing, `"What's the weather?"` → gate does NOT own this turn;
   it proceeds to normal routing, same as if no park existed.
5. NO park standing, `"Yes, confirm that."` → `("none", None)`, nothing
   invented, turn proceeds normally.
6. `trust_ladder` run 5x → T01/T02/T03 unchanged and still 5/5 (D-05's
   park-query gate untouched by this change); T04 now resolves to a real
   `CONFIRM_REPLY` backed by an actual promotion, 5/5.

**The invariant this closes:** the gate must never produce a confirmation
string without a promotion behind it. If a turn cannot be classified confirm
or decline, it must say so plainly rather than let the model guess.

**Known, explicit limit of this fix — not silently claimed as closed:** the
discriminator between "a garbled attempt to respond to the confirmation"
and "an unrelated turn" is `is_declarative_utterance` (same mechanism the
F3 write-path fix just used) plus a widened leading-token check (`yes`/`no`
as the first normalized word, in addition to the existing exact-phrase
`YES_VOCAB`/`NO_VOCAB`). This closes every reproduced case (both live
symptoms, both phrasings in THE DEFECT above) without becoming a classifier
or growing an exemplar list. It does NOT catch every conceivable phrasing of
an ambiguous confirmation attempt (e.g., "sure, whatever" with no yes/no
signal word) — those still fall through to ordinary routing today, same as
before this fix. That residual gap is logged as tech debt, not asserted as
closed.

**RESULTS — all six watched live, 2026-07-16, dev Neo4j (bolt://localhost:7688),
fresh `demo_reset.py --yes` + `demo_seed.py` before each isolated case (P8's
trust-regression check means a promoted head is no longer CORROBORATED, so
re-parking against a polluted graph silently stops parking — each case below
ran against a clean D9 CORROBORATED metformin head unless noted):**

1. `"Yes, confirm that."` — Neo4j `write_state` `unresolved` → `supersede`
   on the SAME `fact_id` (`af211251-…` in this run). Reply: `CONFIRM_REPLY`.
   PASS.
2. `"yes"` — same transition, fresh park, `fact_id 33c10b7e-…`. PASS.
3. `"No, leave it."` — parked row closed (`valid_to` set, `closed_by`
   `'declined'`, confirmed via direct Cypher read); metformin head
   (`89af7b51-…`) untouched, still `supersede`/open. Reply: `DECLINE_REPLY`.
   PASS.
4. `"What's the weather?"` (park standing) — real weather answer returned
   (model routed normally); pending token confirmed STILL present
   afterward via `confirmation_gate.peek()` (TTL decremented, not
   consumed/eaten). PASS.
5. `"Yes, confirm that."`, sam, no park pending — `peek('sam')` was `None`
   before and after; reply was ordinary model chatter, nothing invented,
   nothing promoted. PASS.
6. `trust_ladder` T01→T04, 5 runs, fresh reset+reseed each run: T01/T02/T03
   text identical across all 5 runs (D-05 untouched); T04 →
   `CONFIRM_REPLY` and Jardiance 10mg `unresolved`→`supersede` in Neo4j,
   5/5. PASS.

All six pass. D-03 and D-18 registered FIXED in
`HIP_DefectRegister__v20260715_1930.md` on the strength of this run, not
before it.

## WHAT'S ALREADY DONE

- `harness/confirmation_gate.py`: exact-vocabulary `YES_VOCAB`/`NO_VOCAB`
  matching, identity binding to the authenticated actor, TTL expiry (turn
  count + wall clock), `apply_confirm`/`apply_decline` Neo4j transactions —
  all built, all correct, all unchanged by this fix. The defect is entirely
  in what happens when neither vocabulary matches.
- `_PENDING_PARK_REPLY_TPL` and `PARKED_UPDATE_REPLY` already had their
  "say yes / say no" invitation stripped (D-05 correction, same day). **Not
  reintroduced by this task**, per Bill's explicit instruction.
- Item 0 of the risk memo's §9 (F3 gate widened, detect retry) — c86a414,
  the write-path half of the same defect class. This REQ is the second half
  D-03/D-18, same shape, same session's own stated pattern.

## WHAT'S KNOWN BROKEN (before this build)

- `check_confirmation` returns `"pass"` for ANY utterance that is not an
  exact `YES_VOCAB`/`NO_VOCAB` match while a token is pending — including
  utterances that are obviously attempting to respond ("Yes, confirm
  that.", "No, leave it."). The caller (`process_text_query`) treats `pass`
  identically to "no token at all was ever pending" and falls through to
  ordinary SIA classification → generation. `"Yes, confirm that."`
  classifies `intent=noise`, which the injection contract remaps toward
  `knowledge`-shaped handling, and the model — with no state telling it
  whether anything was actually confirmed — invents an answer. Two
  observed shapes: a fabricated date-confirmation, and (D-18) the model
  reaching into its own system prompt and confirming that back to the user
  instead.
- Nothing in the epistemic record or the graph is wrong when this happens —
  `write_state` correctly stays `unresolved`. Only the spoken reply lies.
  No existing ledger check would ever surface this from the record alone.

## CONSTRAINTS

- Do not reintroduce a "say yes / say no" invitation into
  `_PENDING_PARK_REPLY_TPL` or `PARKED_UPDATE_REPLY`. That is explicitly a
  separate, later decision, not part of this task.
- Must not regress trust_ladder T01/T02/T03 (D-05's park-query gate,
  unrelated code path) — verified in acceptance test item 6.
- Must not turn the confirmation gate into a classifier or grow an
  exemplar list. The fix is two deterministic string checks (leading-token
  yes/no, and the existing declarative/question axis), not a new model
  call and not a wider vocabulary corpus.
- The gate must never emit `CONFIRM_REPLY` or any confirmation-shaped
  string without `apply_confirm` (or `apply_decline`) actually having run
  first, in the same turn. Reply text and graph state must never diverge.
- Register D-03 and D-18 as FIXED only after all six acceptance-test turns
  have been watched pass live, not asserted from code reading.

## SIDE EFFECT FLAGGED, NOT PART OF THE FIX

`scripts/demo_reset.py` was run twice (three resets total including cleanup)
to get isolated, deterministic starting states for the six turns above. Its
log-file and voiceprint paths are **hardcoded to `~/hip-harness`
regardless of which checkout invokes it** (`_HARNESS_ROOT =
pathlib.Path.home() / "hip-harness"`, the script's own comment says so:
"Log files are written by the launchd service to the main harness dir
regardless of which worktree this script is invoked from"). Each reset
deleted `hip-harness/data/voiceprints/maya.npz` and `sam.npz` — the
voiceprint files the FROZEN demo checkout's live voice pipeline (port 7860)
would use for speaker verification — and truncated
`hip-harness/logs/voice_orch.log`/`router.jsonl`. `demo_seed.py` recreates
SYNTHETIC placeholder voiceprints on reseed, not a re-enrollment of
whatever was there before. Neo4j deletion was correctly scoped to the dev
instance only (`NEO4J_URI=bolt://localhost:7688` per `.env.dev`) — only the
voiceprint/log paths cross checkouts. **If maya/sam had real enrolled
voiceprints for a live voice demo on hip-harness, they need re-enrollment
before that demo runs.** Not fixed here — flagging so it isn't discovered
the hard way before a voice demo.
