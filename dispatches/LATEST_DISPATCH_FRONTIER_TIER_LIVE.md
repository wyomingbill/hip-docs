# DISPATCH_FRONTIER_TIER_LIVE
Status: BUILT (verification only — no product code changed)
Reconciled-Against: c4ebe46

**TYPE:** BUILD (verification)

**REQ:** `docs/requirements/REQ_FRONTIER_TIER__script1-t04-t05__v20260717_1215.md`
(this dispatch verifies the real round-trip DISPATCH_FRONTIER_TIER_BUILD and
DISPATCH_FRONTIER_TIER_VERIFY could not complete because the key was 401; it
does not change the build)

## THE ASK

> "DISPATCH: FRONTIER_TIER_LIVE__real-anthropic-roundtrip__v20260717_1530
> TYPE: BUILD (verification)
> REQ: REQ_FRONTIER_TIER
>
> The ANTHROPIC_API_KEY is now valid on the Mini (curl 200). Your verify
> dispatch at c4ebe46 proved four of five with a synthetic frontier response
> because the key was 401. Redo the two that need the real call.
>
> 1. T04 END TO END, REAL CALL: maya asks the setback question -> gate
>    shows -> payload cites D10/D11 by fact_id -> maya approves -> the
>    address actually goes to Anthropic -> the frontier answers with real
>    setbacks for R-1-18. Print: the rendered payload, the outbound
>    request, the response. Confirm the payload was code-built from fact
>    rows and not model-composed.
> 2. RETURN PATH, REAL RESPONSE: the frontier's answer lands as an
>    ASSERTED fact through the normal write path. Verify in Neo4j:
>    fact_id, rung, write_state. Not reply text. Your synthetic test
>    showed write_state=augment, confidence=medium — confirm the real one
>    matches.
> 3. T05: edge summary, email offer, long answer not read aloud.
> 4. THEN RUN boundary_and_consent 5x, fresh reset+seed each time. Report
>    whether T04/T05 land 5/5, same as trust_ladder.
>
> Do not re-prove (b) — you traced voice_orch.py:2607-2632 and confirmed
> decline structurally cannot reach call_frontier. That is better than a
> re-run.
>
> --full still fails on the same 3 pre-existing tests
> (care_coordination.T01/T02, three_zone_demo.T02 — D-21 residual + D-24).
> Not new, not yours, do not chase.
>
> Push, report the hash."

## WHAT WAS DONE

1. Per CLAUDE.md item 11, read `DISPATCH_FRONTIER_TIER_VERIFY__post-session-loss__v20260717_1500.md`
   (`c4ebe46`) in full before re-tracing anything — it already independently
   re-confirmed everything on both sides of the real call; only the round
   trip itself remained open.
2. Confirmed the key change independently, not on the dispatch's word: bare
   `curl -s https://api.anthropic.com/v1/messages` with the `ANTHROPIC_API_KEY`
   from `~/.env.dev` returned a real `200` (`model: claude-sonnet-5`, a real
   completion) — different from the `401 invalid` every prior dispatch in
   this chain recorded.
3. Confirmed `demo_seed.py` still seeds D11 at its real value (`R-1-18`,
   `scripts/demo_seed.py:148-154`) — item 3 of the ask ("D11's real value is
   R-1-18. Seed it") is already satisfied by the current tree; nothing to
   change.
4. Wrote and ran `docs/dispatches/frontier_tier_real_call_script__v20260717_1530.py`
   against a real `HarnessServer` subprocess (dev Neo4j) with the now-valid
   key: fresh `fixture.reset("standard")`, independently resolved D10/D11's
   current fact_ids via `harness.disclosure.household_disclosure_fact_ids`
   and built the expected payload via `build_payload` (same functions
   production code calls), fired the real T04 gate turn and the real T04b
   approve turn through `server.post_turn`, then read the resulting Neo4j
   state directly via `FixtureManager._key_facts` and `truth_layer.queries.trust`.
5. `HarnessServer` spawns `python -m server.voice_https_orch` as a
   subprocess (`eval/harnesslib/server.py:141-142`), so a `requests.post`
   spy installed in the parent process (this script) cannot see the HTTP
   call the disclosure gate makes inside that child. The graph write already
   proves the round trip happened for real (the new fact's stored value IS
   the frontier's real answer, read via Neo4j — not reply text). To also
   print the literal wire-level request body, made one supplementary call to
   the exact same production function, `harness.frontier_client.call_frontier`,
   in this process (where the spy is active), with the identical question
   and the identical code-built payload rows — same real key, same real
   network call, not a re-implementation of the request-building logic.
6. Ran `docs/dispatches/frontier_tier_boundary_and_consent_5x_script__v20260717_1530.py`:
   5 independent trials, each a fresh `fixture.reset("standard")`
   (demo_reset.py --yes + demo_seed.py + verify_seed(), same "fresh
   reset+seed" `FixtureManager` already used for repeated live-proof trials
   in `docs/dispatches/d21_live_proof_script__v20260717_1230.py`), then a
   real T04 gate turn + real T04b approve turn against the live server, with
   the T04-cites-fact_ids / T05-mentions-email / summary-shorter-than-raw /
   coexistence / rung / write_state / confidence checks all evaluated per
   trial against live Neo4j reads and reply text.
7. Ran `python -m eval.harness --full` (background, real detector/model
   calls) after the above, per CLAUDE.md item 12 — not narrow proofs alone.
   Read its actual stdout tail directly, not a hand-picked subset.
8. Per the ask, did NOT re-run the decline path — `DISPATCH_FRONTIER_TIER_VERIFY`
   already traced `server/voice_orch.py:2607-2632` line by line and confirmed
   the `decline` branch is a sibling of, not a caller into, the `approve`
   branch holding the sole call to `call_frontier` (`harness/frontier_client.py:77`,
   the only outbound-HTTP call site in `harness/frontier_client.py` or
   `harness/disclosure.py`). Not repeated here.
9. Reset the graph to clean state (`fixture.reset("standard")`) at the end
   of both new scripts, and confirmed directly afterward
   (`zone_district` active-row count = 1, value `R-1-18`, the original D11).
10. Updated `docs/BACKLOG.md` rows `BILL-1`, `#0`, and `#47` to close the
    "one external blocker" language now that the real round trip has
    completed. Updated `docs/INDEX.md`.

## WHAT WAS FOUND

- **Key is live:** `curl` against `https://api.anthropic.com/v1/messages`
  with the current `~/.env.dev` key returns HTTP 200 with a real completion.
  Previously `401 authentication_error` in both `DISPATCH_FRONTIER_TIER_BUILD`
  and `DISPATCH_FRONTIER_TIER_VERIFY`.
- **(1) T04 end to end, real call — watched run, not inferred:**
  - Gate reply (code-built): `"Answering that well means sending some of
    your household facts to an outside model. Here's exactly what would
    go:\n- address (CONFIRMED, 3a929cab-f211-4c01-898e-311f7ebc7866)\n-
    zone_district (CONFIRMED, 292979a3-c9fe-4b86-ae62-a3ffee2e4a54)\nWant
    me to go ahead?"` — this reply string was asserted, by direct string
    comparison in the script, to be byte-identical to
    `harness.disclosure.render_disclosure_prompt()` called directly on a
    payload independently built (in this script, not by the server) from
    the same two fact_ids via `harness.disclosure.build_payload()`
    (`gate_matches_render_disclosure_prompt: true` in the JSON output). This
    is the strongest form of "code-built, not model-composed" available: the
    live reply matches, character for character, a payload the harness
    reconstructed from raw Neo4j fact rows, independent of the server's own
    internal call to the same function.
  - Captured outbound request body (via the supplementary direct
    `call_frontier` call, same real key, item 5 above):
    ```json
    {
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "tools": [{"type": "web_search_20250305", "name": "web_search"}],
      "messages": [{"role": "user", "content":
        "A household is asking: What's the setback for our house, and what would it take to get a variance?\n\nKnown facts about their situation (from verified household records):\n- address: [REDACTED-HOME-ADDRESS] (rung=CONFIRMED, fact_id=b7d32fd5-...)\n- zone_district: R-1-18 (rung=CONFIRMED, fact_id=7c8db6a8-...)\n\nAnswer using these facts plus your own knowledge and web search if needed. ..."}]
    }
    ```
    Headers: `anthropic-version: 2023-06-01`, `content-type: application/json`,
    `x-api-key` present (value not logged). The body contains only the
    question and the two payload rows' attribute/value/rung/fact_id —
    nothing else, confirming `harness/frontier_client.py:31-70` adds no
    content beyond formatting `payload_rows`.
  - Real response, live-server run (T04b reply, spoken to Maya): `"The
    setback requirements for your R-1-18 zoned property in Lakewood, CO are
    25 feet front, 10 feet side, and 15 feet rear. To get a variance, you
    must show exceptional circumstances that aren't self-imposed and
    necessary to use the property reasonably, without harming neighbors or
    public welfare. I'll email you the full details."`
  - Real response, supplementary direct call (item 5): a longer, independent
    web-search-grounded answer landing on the same specific numbers (25 ft
    front / 10 ft / 15 ft setbacks under "Table 17.5.1 of the Lakewood
    Zoning Ordinance") and the same Board-of-Adjustment variance path — two
    separately-fired real calls, same underlying facts, consistent specific
    answer. This is the actual frontier answering with real setbacks for
    R-1-18, not a synthetic stand-in.
- **(2) Return path, real response — verified in Neo4j, not reply text:**
  - New fact_id `397bc118-7b3e-4c53-9ccb-4f67a0de7089` (main live-server run)
    written by `harness.disclosure.write_frontier_fact` →
    `memory_engine.store.encode()`, the normal write path.
  - `truth_layer.queries.trust(fact_id, driver=driver)` → `level='ASSERTED'`,
    `basis="write_state='augment' AND confidence='medium' AND not derived"`.
  - Direct raw-property Neo4j read of that node: `{"write_state": "augment",
    "confidence": "medium", "valid_to": null, "sensitivity": "low"}` —
    **matches the synthetic test's prediction in `DISPATCH_FRONTIER_TIER_VERIFY`
    exactly** (`write_state=augment`, `confidence=medium`).
  - `zone_district` active-row count after the write: 2 — the original D11
    (`R-1-18`, CONFIRMED) plus the new frontier-sourced row — coexistence,
    not supersession, same as the prior synthetic proof.
- **(3) T05 — confirmed on the same live turn (T04b's reply IS T05's
  disposition; `boundary_and_consent__v20260717_1330.json`'s T05 entry has
  no separate live turn by design — `narrate` field, empty `text`):**
  - Ends on the email offer: `"...I'll email you the full details."`
  - Never recites the raw answer in full — the reply is 3 sentences; the
    fact landed in the graph (the actual frontier text) runs to ~4,100
    characters with headers, a criteria list, and an application-process
    section. The spoken reply contains none of that structure.
  - Confirmed programmatically in the 5x script (not eyeballed only): for
    every trial, `len(reply_text) < len(raw_answer_stored_in_graph)`.
- **(4) boundary_and_consent 5x, fresh reset+seed each time — 5/5 landed:**
  All five trials, independently: `t04_cites_both_fact_ids=True`,
  `t05_nonempty=True`, `t05_mentions_email=True`,
  `t05_summary_shorter_than_raw_answer=True`, exactly one new fact per
  trial, `coexistence_two_active_rows=True`, `new_fact_rung=ASSERTED`,
  `new_fact_write_state=augment`, `new_fact_confidence=medium` — identical
  profile across all 5 trials, each against freshly-generated fact_ids (not
  hardcoded — resolved per trial via `household_disclosure_fact_ids`).
  `trust_ladder` itself was not re-run here (not asked); this reports
  `boundary_and_consent`'s own 5/5 landing rate on T04/T05, at the same
  full-landing standard.
- **--full: differs slightly from the ask's stated baseline, reported
  plainly rather than smoothed over:**
  - `RATCHET FAIL — regressed vs baseline: ['L2:care_coordination.T01',
    'L2:care_coordination.T02']` — 2 of the 3 named tests, matching the
    ask (D-21 residual, already isolated in `DISPATCH_D21_D23`).
  - `three_zone_demo.T02` **passed** this run
    (`eval/harness.py`'s own scorecard line: `three_zone_demo.T02 PASS
    sam: "Dad had a fall last week..."`) — not a discrepancy to chase, D-24
    (medication-status over-triggering) is inherently a stochastic-trigger
    defect, and a pass on one run of a stochastic defect is expected, not
    evidence it's fixed.
  - `NEW FAILURES (not in baseline): ['L6:record-invariants']` — specifically
    `G1 no-orphan-generation: 1 violation(s) [HARD ZERO]`. Checked against
    `docs/BACKLOG.md` row `BILL-4` before treating this as a new finding:
    **`BILL-4` already registers this exact gate as a known flake — "G1
    hard-zero gate... ~91% failure rate on `--full`, one repeat-offender
    query"** (`eval/oracle/record_invariants.py:18` also documents a 2026-07-15
    baseline of 4 G1 violations). G1/G4 are HARD ZERO by design
    (`eval/harness.py:409`, `_hard_zero_keys`) — no baseline-accept
    mechanism exists for them (`eval/harness.py:403-408`'s comment: "no
    accept, no baseline excuse"), which is exactly why it prints under NEW
    FAILURES instead of RATCHET FAIL every time it fires, at ~91% of runs,
    regardless of what else changed. Not new, not caused by this dispatch's
    scripts — pre-existing, already tracked, explicitly out of scope
    (`BILL-4` is UNGOVERNED, no REQ). Not chased, per the ask.
  - `boundary_and_consent__v20260715_1158` and `__v20260717_1330` both
    still `SKIP — no expected file` (`eval/harnesslib/layer2.py:148-152`) —
    same known gap as both prior dispatches in this chain; `--full` does not
    exercise T04/T04b on its own regardless of the key.

## VERIFIED

- **Watched run:**
  - `curl` against the real Anthropic endpoint: `200`, real completion body.
  - `fixture.reset("standard")` + `verify_seed()`: clean, no drift, in both
    scripts (main run and each of the 5 boundary_and_consent trials).
  - T04 gate reply, byte-matched against an independently-rebuilt payload:
    cites both live fact_ids, code-built.
  - T04b approve reply, live server, real key: real setback numbers for
    R-1-18 (25/10/15 ft), ends on email offer, 3 sentences.
  - Supplementary direct `call_frontier` call: real HTTP 200, captured
    request body (model, tools, full user message) and real response text
    (~4,100 chars, web-search-grounded, consistent numbers).
  - Neo4j direct reads: new fact_id, `write_state=augment`,
    `confidence=medium`, `valid_to=null`, `ASSERTED` via `trust()` — twice,
    once for the main run and once per boundary_and_consent trial (5x).
  - Two active `zone_district` rows post-write, all 6 real-call runs (1 main
    + 5 trials) — coexistence, not supersession, every time.
  - `python -m eval.harness --full`: ran to completion; read its actual
    stdout tail verbatim, not a hand-picked subset.
  - Graph reset to clean state (single active D11 row, `R-1-18`) after every
    script, confirmed by direct query.
- **Reasoned about, not independently re-run this dispatch:**
  - The decline path (item (b) in the original five proofs) — per the ask's
    explicit instruction, relying on `DISPATCH_FRONTIER_TIER_VERIFY`'s own
    structural trace of `voice_orch.py:2607-2632` and the outbound-call-site
    grep, both already on record.
  - Whether `L6:record-invariants`'s G1 flake and the `three_zone_demo.T02`
    pass are literally the same underlying stochastic mechanism as
    previously characterized — taken from `docs/BACKLOG.md` (`BILL-4`) and
    `eval/oracle/record_invariants.py`'s own baseline note, not re-isolated
    from zero this session, consistent with CLAUDE.md item 11.
  - `trust_ladder`'s own 5/5 landing rate — cited by the ask as the
    comparison point, not re-run here (out of this dispatch's scope; the
    ask asked to run `boundary_and_consent` 5x, not `trust_ladder`).

## HASH

`eb2e274`

## OPEN

- `BILL-4`'s G1 hard-zero flake (~91% failure rate, one repeat-offender
  query) remains open, ungoverned, no REQ — unrelated to the frontier tier,
  not this dispatch's scope, not chased.
- No `_expected.json` recorded for either `boundary_and_consent` script
  version — `--full` still does not exercise T04/T04b on its own. Recording
  one is a separate, still-open piece of work.
- D-24 (medication-status over-triggering) remains unfixed; this run's
  `three_zone_demo.T02` pass is one data point on a stochastic defect, not
  evidence of a fix.
- Per-member frontier key storage (`TD-128`) remains explicit debt, not
  addressed here — this run used the single household key in `~/.env.dev`.
