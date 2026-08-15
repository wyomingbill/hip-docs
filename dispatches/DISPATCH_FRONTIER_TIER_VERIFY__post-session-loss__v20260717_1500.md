# DISPATCH_FRONTIER_TIER_VERIFY
Status: BUILT (verification only — no product code changed)
Reconciled-Against: 5ad1cc9

**TYPE:** MEASUREMENT

**REQ:** `docs/requirements/REQ_FRONTIER_TIER__script1-t04-t05__v20260717_1215.md`
(this dispatch verifies claims made against that REQ by
`DISPATCH_FRONTIER_TIER_BUILD__script1-t04-t05__v20260717_1330.md`; it does
not change the build)

## THE ASK

> "DISPATCH: FRONTIER_TIER_VERIFY__post-session-loss__v20260717_1500
> TYPE: BUILD (verification of existing work)
> REQ: REQ_FRONTIER_TIER
>
> The session that built the frontier tier died before reporting. Two
> commits landed and pushed: b36fa95 (enum widened, seed path validated,
> "D10/D11 blocked") and 5ad1cc9 (frontier tier, disclosure gate, Anthropic
> BYOK, ASSERTED return path).
>
> 1. WHAT BLOCKED D10/D11? ... Report what stopped it.
> 2. RUN THE FIVE PROOFS. None are on record: a. T04 -> gate shows, payload
>    cites D10/D11 by fact_id, Maya approves, frontier answers with real
>    setbacks b. Decline -> nothing leaves. Verify NO outbound call, not
>    just a refusal string. c. Return fact lands ASSERTED. Verify in Neo4j:
>    fact_id, rung, write_state. Not reply text. d. T05 -> edge summary,
>    email offer, long answer not read aloud e. --full passes (CLAUDE.md
>    item 12)
> 3. D11's real value is R-1-18. Seed it.
>
> Report what you watched run versus what you inferred. Push, report the
> hash."

## WHAT WAS DONE

1. Per CLAUDE.md item 11, checked `docs/dispatches/` before re-tracing
   anything. Found `DISPATCH_FRONTIER_TIER_BUILD__script1-t04-t05__v20260717_1330.md`
   already on file (committed in `5ad1cc9`, same day, 13:56) — the prior
   session's own report of this exact work, including a VERIFIED section
   with the same five proofs. **The dispatch's premise ("none are on
   record") is not accurate: a report exists.** What was actually missing
   was independent re-confirmation, since the dispatching session had no
   way to know whether that doc's claims still held on a cold checkout —
   so this dispatch re-ran everything live rather than taking the doc's
   word for it.
2. Read `DISPATCH_D21_D23__enum-widened-seed-validated-d10d11-blocked__v20260717_1240.md`
   in full for the D10/D11 blocker mechanism (item 1).
3. Confirmed the `ANTHROPIC_API_KEY` in `~/.env.dev` state with a bare
   `curl` to `https://api.anthropic.com/v1/messages` — independent of any
   application code.
4. Ran `scripts/demo_reset.py --yes` + `scripts/demo_seed.py` fresh, read
   the console output directly.
5. Wrote and ran `docs/dispatches/frontier_tier_verify_script__v20260717_1500.py`
   against a real `HarnessServer` subprocess (dev Neo4j, real Groq/Ollama
   stack) and real Neo4j reads via `FixtureManager`, mirroring the pattern
   `docs/dispatches/d21_live_proof_script__v20260717_1230.py` already
   established: `verify_seed()`, T04 gate turn, decline turn +
   direct-graph re-check, approve turn (real invalid key) + direct-graph
   re-check, `write_frontier_fact()` called directly with a synthetic
   answer + `trust()` + raw Neo4j property read, `_summarize_frontier_answer_on_edge()`
   called directly. Reset the graph to clean state again afterward.
6. Read `server/voice_orch.py:2607-2644` line by line to trace the decline
   branch structurally, and grepped `harness/frontier_client.py` and
   `harness/disclosure.py` for every outbound-HTTP call site.
7. Ran `scripts/demo_seed.py`'s `_seed_one` directly with an out-of-enum
   attribute to reconfirm the loud-refusal behavior (item 4 of `b36fa95`'s
   four-part decision) on the current tree.
8. Ran `python -m eval.harness --full` in the background (real detector
   calls; ran long), read its actual stdout tail and its RATCHET FAIL line
   verbatim — not a hand-picked subset, per CLAUDE.md item 12.
9. Updated `docs/BACKLOG.md` row 15b (D-23): item 3 was still marked
   "Bill's call, not yet decided" even though `5ad1cc9` already carries
   Bill's Q8 answer deciding it. Closed the row and cited both dispatches.

## WHAT WAS FOUND

- **D10/D11 blocker (item 1), sourced from
  `DISPATCH_D21_D23__enum-widened-seed-validated-d10d11-blocked__v20260717_1240.md`
  lines 47-79:** setting D10/D11's attribute to `household` (Bill's
  originally-stated migration) made `eval/harnesslib/fixture.py`'s
  `verify_seed` raise `SystemExit: FIXTURE DRIFT: D7 value mismatch —
  registry 'trash pickup is Wednesday' vs graph 'TBD'` on the very next
  `fixture.reset("standard")`. Root cause: `_key_facts`/`verify_seed`
  match on `(owner, subject, attribute)` only and assert exactly one
  active row per triple; `D7` already owns
  `(household, household, household)`, so giving D10 and/or D11 the same
  attribute string creates 2-3 facts at one triple, which `verify_seed`
  can't disambiguate — it silently reads back whichever row the query
  happens to return first. This was live-tested, not theorized, and
  reverted the same session. Bill's answer to Q8 in
  `DISPATCH_FRONTIER_TIER_BUILD` (2026-07-17 13:30) resolved it: do NOT
  migrate to `household`; add `address` and `zone_district` to
  `harness/extraction_queue.py`'s `CANONICAL_ATTRIBUTES` as their own
  values instead (confirmed present, 15 values, in this session's own
  `_seed_one` enum-rejection check below).
- **The `ANTHROPIC_API_KEY` in `~/.env.dev` is still invalid** — a direct
  `curl -s https://api.anthropic.com/v1/messages` with that key returns
  `{"type":"error","error":{"type":"authentication_error","message":"API
  key is invalid."}}`. Identical to what `DISPATCH_FRONTIER_TIER_BUILD`
  already reported. Nothing has changed here; still an external blocker,
  not routed around.
- **`eval/harnesslib/layer2.py`'s `run()` still skips
  `boundary_and_consent__v20260717_1330.json`** (no `_expected.json`
  companion) — `--full` does not exercise T04/T04b live today regardless
  of the key. Confirmed by reading `layer2.py:148-152`, same finding
  already on record.
- **`--full` result: `RATCHET FAIL — regressed vs baseline:
  ['L2:care_coordination.T01', 'L2:care_coordination.T02',
  'L2:three_zone_demo.T02']`** — the identical three test IDs
  `DISPATCH_FRONTIER_TIER_BUILD` already isolated and attributed to
  pre-existing D-21 residual (2 of 3) and newly-registered D-24 (1 of 3),
  confirmed there to predate the frontier-tier build entirely (reproduced
  on `b36fa95` with zero frontier-tier code present). This run introduced
  no code changes before or during the harness run, so an identical
  failure set is expected, not a new finding — it corroborates the prior
  session's isolation rather than repeating it from zero.

## VERIFIED

- **Watched run:**
  - `curl` against the real Anthropic endpoint: `401 invalid` (verbatim
    above).
  - `demo_reset.py --yes` + `demo_seed.py`: console output shows `11/11
    fact(s) seeded`, `D10 [CONFIRMED] ... address: [REDACTED-HOME-ADDRESS]`, `D11 [CONFIRMED] ... zone_district: R-1-18`.
  - `FixtureManager.verify_seed()`: returned with no exception —
    `"OK — no drift, no collision"` in this run's own JSON output.
  - `demo_seed._seed_one(..., attribute='not_a_real_attribute', ...)`:
    raised `ValueError: DXX: attribute 'not_a_real_attribute' is not in
    CANONICAL_ATTRIBUTES ([...15 values including 'address',
    'zone_district'...])` — before any driver call (`driver=None` was
    passed and never touched).
  - **(a) gate half:** `POST /api/text-query` "What's the setback for our
    house, and what would it take to get a variance?" as `maya` →
    `"Answering that well means sending some of your household facts to an
    outside model. Here's exactly what would go:\n- address (CONFIRMED,
    456f3c73-...)\n- zone_district (CONFIRMED, c57328e9-...)\nWant me to
    go ahead?"` — cites both fact_ids directly, real rung.
  - **(b) decline:** same session, "No, never mind." →
    `"Keeping that local, then."`; direct Neo4j re-read via
    `FixtureManager._key_facts("household","household","zone_district")`
    shows exactly one active row, same `fact_id` as before the turn — no
    write occurred. Structural check: read `server/voice_orch.py:2607-2632`
    — the `decline` branch (`clear_pending` + reply string) is a sibling
    of, not a caller into, the `approve` branch that holds the sole call to
    `call_frontier`; grepped `harness/frontier_client.py` and
    `harness/disclosure.py` for `requests.` / `urllib` / `http` and found
    exactly one call site (`frontier_client.py:77`, inside `call_frontier`
    only). Decline cannot structurally reach it — this is stronger than
    "no error was observed."
  - **Approve with the real (invalid) key**, same live run: "Yes, go
    ahead." after a fresh gate turn → `"I couldn't reach the outside model
    just now — keeping that local for the moment."`; direct Neo4j re-read
    again shows exactly one active `zone_district` row, same `fact_id` —
    no silent write on failure.
  - **(c) write path, isolated (synthetic answer, since the real key is
    dead):** `harness.disclosure.write_frontier_fact(driver,
    session_id=..., question=..., answer=<synthetic setback text>)` →
    new `fact_id` `d4b07297-...`; `truth_layer.queries.trust(fact_id,
    driver=driver)` → `level='ASSERTED'`, `basis="write_state='augment'
    AND confidence='medium' AND not derived"`; direct Neo4j read of that
    node's raw properties → `{"write_state": "augment", "confidence":
    "medium", "valid_to": None}`. Direct re-read of the
    `(household,household,zone_district)` triple shows **two** active
    rows afterward — the original D11 (`c57328e9-...`, value `R-1-18`)
    and the new fact — coexistence, not supersession, confirmed by fact
    row content, not reply text.
  - **(d) T05 summarizer:** `await
    server.voice_orch._summarize_frontier_answer_on_edge(question,
    synthetic_answer)` → `"Your house is currently within the setback
    requirements, but if you need to encroach, you'd have to request a
    variance through a Board of Adjustment hearing. I'll email the full
    details."` — 2 sentences, no verbatim recitation of the setback
    figures, ends on the email offer.
  - `python -m eval.harness --full`: ran to completion (background,
    real detector/model calls); read its tail directly; final line
    `RATCHET FAIL — regressed vs baseline: ['L2:care_coordination.T01',
    'L2:care_coordination.T02', 'L2:three_zone_demo.T02']`.
  - Reset the graph to clean state (`demo_reset.py --yes` + `demo_seed.py`)
    after the verify script's own turns, before running `--full`.
- **Reasoned about, not independently re-run:**
  - The actual Anthropic round-trip content (model name, `web_search_20250305`
    tool schema, whether the beat holds hedge-without-D11 vs.
    definitive-with-D11 against the real model) — still blocked on the
    invalid key, exactly as `DISPATCH_FRONTIER_TIER_BUILD` reported. **Not
    claimed as done, then or now.**
  - That the two `D-21`-attributed failures in this run's `--full` are the
    same stochastic family as before (not re-isolated turn-by-turn this
    session) — taken on the strength of identical test IDs and the prior
    session's own isolation work (git-stash comparison against `b36fa95`),
    not re-proven from scratch here. Re-isolating on every verification
    pass would be re-tracing what `DISPATCH_FRONTIER_TIER_BUILD` already
    closed, contrary to CLAUDE.md item 11.

## HASH

`d41328f`

## OPEN

- **PROVE LIVE (a) and (c), as literally stated ("frontier answers with
  real setbacks" / return fact lands ASSERTED via the real crossing), are
  still blocked on a working `ANTHROPIC_API_KEY`.** Everything on both
  sides of that call is now independently re-verified live, twice
  (original build session + this one); the round-trip itself has still
  never executed for real. Needs Bill to supply a working key.
- **`--full` does not pass on `main`**, and did not pass before this
  dispatch either — `e. --full passes` is reported here as **not met**,
  plainly, rather than reframed as "passes except for pre-existing
  issues." The three failures are the same ones `DISPATCH_FRONTIER_TIER_BUILD`
  isolated and attributed to REQ_D21_D23's territory (D-21 residual ×2,
  D-24 ×1) — this dispatch adds a second independent reproduction of the
  identical failure set, not a new isolation.
- No `_expected.json` recorded for `boundary_and_consent__v20260717_1330.json`
  still open (same item `DISPATCH_FRONTIER_TIER_BUILD` left open);
  recording one that faithfully covers T04b is itself blocked on the same
  key.
- D-24 (`medication_status` over-triggering on medication-switch
  statements) remains unfixed, out of this dispatch's scope, same as
  before.
