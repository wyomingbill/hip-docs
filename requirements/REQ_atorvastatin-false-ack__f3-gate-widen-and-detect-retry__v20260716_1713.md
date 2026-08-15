# REQ_atorvastatin-false-ack
Status: BUILT
Reconciled-Against: (this commit — see docs/INDEX.md for hash)

## THE REQUIREMENT

Bill's own words, verbatim:

> Build §9 item 0 from the amended risk memo (792889f).
>
> The atorvastatin false ack. voice_orch.py:3097-3103 receives delta showing the
> write failed, writes it into the record, and returns the false ack two lines
> later with no branch between them. It knows and says the opposite anyway.
>
> Extend the F3 zero-write check past _SUPERSEDE_PHRASE_RE to all declaratives.
> One condition.
>
> MUST SHIP WITH the detection retry. A zero-write gate makes the P2/i019
> detection miss user-visible; without a retry you have traded a silent lie for
> a loud failure. That is your own finding from the review.
>
> Prove it LIVE, not structurally:
>   1. declarative that WRITES -> ack spoken, delta non-empty, unchanged
>   2. declarative that FAILS to write -> NOT acked. Force the failure if needed.
>   3. "What's Ray on?" (maya) -> still guards
>   4. trust_ladder 5x -> T03 still 5/5
>
> Structural proofs passed and the live path failed twice today. Do not report a
> proof you have not watched run.
>
> Push, report the hash.

## THE ACCEPTANCE TEST

Four live turns, run against `server.voice_orch.process_text_query` (the same
function `/api/text-query` calls) on the actual dev backends (real Neo4j,
real Groq, real Ollama) — not a unit test, not a mock:

1. A declarative with no supersede keyword that lands a real write (sam:
   "I take atorvastatin 20mg every morning.") produces the model's own ack
   unchanged, with a non-empty `delta` in the epistemic record.
2. The same shape of declarative, forced to fail detection (real Groq 401,
   not a mocked return), produces `UNCONFIRMED_UPDATE_REPLY` — NOT the
   model's ack — even though the utterance matches no supersede keyword.
3. "What's Ray on?" asked by maya still resolves to `guard_empty_set`
   (D-02 short-phrasing gap) — unaffected by the F3 change.
4. "What medication is Ray on now?" asked by maya, run 5 times against the
   existing P8-parked state (metformin CORROBORATED head + Jardiance
   UNRESOLVED park), returns variant (a) — head named, park flagged — 5/5.

## WHAT'S ALREADY DONE

- TD-121 F1 (detect_and_apply reads the full active owner+household set
  itself) and the original F3 gate (supersede-phrased declaratives only) —
  RESOLVED 2026-07-09, unchanged by this build.
- P8 park check in `_gate_unconfirmed_update` (runs on every detection turn
  regardless of phrasing) — unchanged.
- D-05 pending-park template reply (`_gate_double_valued_park_query` /
  `_PENDING_PARK_REPLY_TPL`) — unchanged, and is what makes test 4
  deterministic rather than LLM-variance-prone.
- Groq call retry on transport failure (`_GROQ_RETRY_DELAYS`, 2 retries,
  same temperature) — pre-existing, unchanged; distinct from the new
  detection-level retry below.

## WHAT'S KNOWN BROKEN (before this build)

- `_gate_unconfirmed_update` (`server/voice_orch.py`) gated a zero-write
  outcome only when `_SUPERSEDE_PHRASE_RE.search(query)` matched. A plain
  declarative asserting a new personal fact with no supersede keyword —
  "I take atorvastatin 20mg every morning" — matched nothing, so a
  zero-write outcome for it skipped the gate entirely: `reply` (the model's
  ack, generated from the utterance) shipped unchanged even though `delta`
  was empty. No branch existed between reading the failed delta and
  returning the false ack.
- Widening that gate to every declarative, by itself, converts every
  detection false negative into a user-visible spoken refusal — including
  P2/i019 (gpt-oss-20b returns `changes:[]` for some multi-party contexts,
  confirmed deterministic at temperature=0.0, see
  `docs/research-technical/DIAG__p2-i019-detection-miss__v20260714_1500.md`).
  Shipping the widened gate alone trades a silent lie for a loud, frequent
  failure.

## WHAT WAS BUILT

1. `server/voice_orch.py` — `_gate_unconfirmed_update`'s F3 check changed
   from `_SUPERSEDE_PHRASE_RE.search(query)` to `is_declarative_utterance
   (query)`. `_SUPERSEDE_PHRASE_RE` removed (no longer referenced). One
   condition, per the requirement.
2. `harness/fact_change.py` — `detect_and_apply` retries once at
   `temperature=0.2` when the first Groq call returns zero changes, before
   finalizing a `detect_no_changes` outcome. A same-temperature retry
   cannot recover a deterministic false negative, so the retry resamples
   at a different temperature. `_call_groq` takes a `temperature` param
   (was hardcoded 0.0).
3. Logged as TD-125 (retry cost/recovery-rate not yet measured — see
   `docs/techdebt/DEBT_REGISTER__v20260712_2300.md`) and amended into
   TD-121's existing entry.

All four acceptance-test turns were run live and observed (not asserted
structurally) — see commit for the transcript summary.

## CONSTRAINTS

- Must not regress TD-121's original fix (F1 full-facts read) or the P8
  park check, which runs before the F3 check and is unconditional on
  phrasing already.
- Must not regress D-02 (guard_empty_set on short Ray-phrasing) or D-05
  (pending-park template reply) — verified unaffected (tests 3 and 4).
- The detect-retry is a mitigation, not a fix, for the P2/i019 false
  negative rate. TD-123 (prompt hardening) remains the correct long-term
  track; this build does not substitute for it, per the risk memo's
  explicit framing in §10.
- Voice path (`harness/realtime_adapter.py`) does not share this
  checkpoint and remains exposed — risk memo §10, unchanged by this build,
  out of scope here.
