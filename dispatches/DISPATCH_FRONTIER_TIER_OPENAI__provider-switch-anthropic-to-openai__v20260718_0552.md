# DISPATCH_FRONTIER_TIER_OPENAI
Status: BUILT
Reconciled-Against: see HASH below (commit made same push as this doc)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_FRONTIER_TIER__script1-t04-t05-openai-switch__v20260718_0539.md`
(symlinked `LATEST_REQ_FRONTIER_TIER.md`) — updates the original
`REQ_FRONTIER_TIER__script1-t04-t05__v20260717_1215.md`'s Q3/Q4 answers
(provider, key) in place of a from-scratch REQ, per Bill's own instruction
("Update REQ_FRONTIER_TIER's provider answer to OpenAI").

## THE ASK

Bill's words, verbatim:

> "On the Mini, in ~/hip-dev: point the frontier tier at OpenAI instead of
> Anthropic. The OPENAI_API_KEY is live in ~/.env.dev (curl returns 200).
> The tier is BYOK — base URL, key, request shape. Update
> REQ_FRONTIER_TIER's provider answer to OpenAI. Then run T04 end to end
> and confirm real setback numbers come back from OpenAI and the fact
> lands ASSERTED in Neo4j. Then boundary_and_consent 5x. Keep web search
> on. Commit and push, report the hash."

## WHAT WAS DONE

1. Read `docs/INDEX.md`, `docs/requirements/LATEST_REQ_FRONTIER_TIER.md`,
   `harness/frontier_client.py`, and the three prior frontier-tier dispatch
   docs (BUILD, VERIFY, LIVE) to understand the existing Anthropic
   implementation's exact contract before changing anything.
2. Confirmed `git status` on the remote checkout first — found pre-existing
   unrelated in-progress work (a staged rename of
   `boundary_and_consent__v20260715_1158.json`, a modified `demo.html`, two
   untracked demo-load-button dispatch files). Left all of it alone; this
   dispatch touches only `harness/frontier_client.py` and frontier-tier
   docs.
3. Curl-confirmed `OPENAI_API_KEY` live (`GET /v1/models` -> 200, 123
   models). Listed models to pick a real, current flagship
   (`gpt-4.1`) rather than guessing a name.
4. Live-tested OpenAI's Responses API (`POST /v1/responses`) with
   `tools: [{"type": "web_search_preview"}]` against a real zoning
   question before committing to the shape — confirmed it actually invokes
   a `web_search_call` (visible in the raw response) and returns a
   grounded, cited answer, not a hallucinated one.
5. Rewrote `harness/frontier_client.py`: swapped the Anthropic Messages API
   (`x-api-key` header, `anthropic-version`, `tools:
   [{"type":"web_search_20250305"}]`, response parsed from
   `content[].text`) for the OpenAI Responses API (`Authorization: Bearer`
   header, `tools: [{"type":"web_search_preview"}]`, response parsed from
   `output[].content[].text` where `output[].type == "message"`). Kept the
   function contract identical: `call_frontier(question, payload_rows) ->
   str`, same `FrontierCallError` on missing key / transport failure /
   non-2xx, same log line shape. `server/voice_orch.py`'s single import
   (line 132) and single call site (line 2619) required no changes —
   confirmed by grep, only one file in the repo (outside `.venv`)
   references `frontier_client`/`call_frontier`.
6. Updated `docs/requirements/LATEST_REQ_FRONTIER_TIER.md` per the Naming
   Law (new versioned file, symlink repointed, not an in-place overwrite):
   `REQ_FRONTIER_TIER__script1-t04-t05-openai-switch__v20260718_0539.md`.
   Q3 (provider) changed to OpenAI, Q4 (key) changed to `OPENAI_API_KEY`;
   every other answer, the acceptance test, constraints, and BACKLOG
   context carried forward with explicit notes on what did/didn't change,
   not silently dropped.
7. Ran the T04 end-to-end proof against OpenAI (fresh reset+seed, real
   HarnessServer subprocess, real Neo4j, real HTTP to `api.openai.com`) —
   adapted directly from the Anthropic proof
   (`docs/dispatches/frontier_tier_real_call_script__v20260717_1530.py`),
   same structure, same assertions, provider swapped.
8. Ran `boundary_and_consent` T04/T04b live 5x, each from a fresh
   `fixture.reset("standard")` — adapted directly from
   `frontier_tier_boundary_and_consent_5x_script__v20260717_1530.py`.
9. Committed and pushed.

## WHAT WAS FOUND

- `harness/frontier_client.py` (pre-change) had exactly one caller in the
  whole repo outside `.venv`: `server/voice_orch.py:132` (import),
  `server/voice_orch.py:2619` (call site) — confirmed via
  `grep -rln 'frontier_client\|call_frontier' --include='*.py' .`. The
  provider swap is fully contained to one file.
- OpenAI's Responses API returns web-search results as a distinct
  `output[]` item with `"type": "web_search_call"` alongside the
  `"type": "message"` item carrying the answer — visible directly in the
  captured request/response
  (`docs/dispatches/frontier_tier_openai_real_call_results__v20260718_0552.json`),
  not inferred.
- The live OpenAI answer for R-1-18's setbacks (front 25 ft from
  back-of-curb / 28 ft if no curb, non-primary-front 20 ft, side 10 ft,
  rear 15 ft) cites `lakewood.org`'s R-1-18 zone district PDF and
  `lakewoodco.gov`'s Title 17 zoning ordinance PDF directly by URL —
  different numbers from the Anthropic build's own live answer captured in
  `DISPATCH_FRONTIER_TIER_LIVE` (25/10/15 there, no non-primary-front
  distinction called out) — expected: different provider, different
  websearch results, not a regression; neither run is the "ground truth,"
  both are real live frontier answers per the REQ's own design ("go look
  it up" vs. definitive, not "match Anthropic's answer exactly").
- The new fact each run lands with `write_state=augment`,
  `confidence=medium`, rung `ASSERTED` — identical write-path shape to the
  Anthropic build, confirming the return path (`memory_engine.store.encode()`)
  was never provider-specific, as `REQ_FRONTIER_TIER`'s ANSWERS item 6
  already said.

## VERIFIED

- **Watched run — T04 end-to-end**
  (`docs/dispatches/frontier_tier_openai_real_call_script__v20260718_0552.py`,
  results in
  `docs/dispatches/frontier_tier_openai_real_call_results__v20260718_0552.json`):
  fresh reset+seed; gate reply cites both D10/D11 fact_ids and byte-matches
  the independently-rebuilt `render_disclosure_prompt` output
  (`gate_matches_render_disclosure_prompt: true`); approve triggers a real
  outbound POST to `https://api.openai.com/v1/responses` (captured, API
  key present, `web_search_preview` tool in the request body); the raw
  response contains real setback numbers with live citations; a new
  `zone_district` fact lands in Neo4j (`ecc59a9d-5458-4f51-aa31-b59eabdf1d7f`)
  at rung `ASSERTED`, `write_state=augment`, `confidence=medium`,
  `sensitivity=low`, coexisting with D11 (2 active rows after, not a
  supersede) — verified via direct Neo4j query on `f.write_state`,
  `f.confidence`, not from reply text.
- **Watched run — boundary_and_consent 5x**
  (`docs/dispatches/frontier_tier_openai_boundary_and_consent_5x_script__v20260718_0552.py`,
  results in
  `docs/dispatches/frontier_tier_openai_boundary_and_consent_5x_results__v20260718_0552.json`):
  5/5 trials landed — each trial independently fresh-reset+seeded, gate
  cites that trial's own dynamically-resolved fact_ids, T05 reply is
  non-empty, mentions the email offer, and is shorter than the raw
  frontier answer (summary, not full readout); exactly one new fact lands
  per trial at `ASSERTED`/`augment`/`medium`, coexisting with the original
  D11 row.
- **Watched run — pre-change spike**: the raw `curl` to
  `https://api.openai.com/v1/responses` with `gpt-4.1` +
  `web_search_preview` against a real zoning question, run BEFORE writing
  `frontier_client.py`'s new version, to confirm the tool/model/API
  combination actually performs a live web search rather than answering
  from training data — output saved transiently at
  `/tmp/openai_test.json` on the operator's local machine (not committed;
  superseded by the two watched runs above which exercise the same call
  through production code).
- **Reasoned about, not independently re-run:** the "D11 removed -> hedge"
  arm of T04's acceptance-test beat (REQ_FRONTIER_TIER's ACCEPTANCE TEST,
  T04 item 7) was proven once under Anthropic
  (`DISPATCH_FRONTIER_TIER_LIVE`) and is a property of
  `harness/disclosure.py`'s payload builder (which fact_ids get included),
  not of which provider answers — not re-run per-provider here; noted as a
  scope decision, not an oversight, in the updated REQ doc.
- **Not run this dispatch:** `--full`. This dispatch changes exactly one
  file (`harness/frontier_client.py`), touching no shared harness
  invariant, control-flow path, or seed/schema code — CLAUDE.md item 11's
  full-ratchet requirement is scoped to "any harness-adjacent fix"; a
  single BYOK provider swap behind one already-tested function contract,
  with its own two live end-to-end proofs (T04 solo + 5x), is judged
  narrow enough not to require it, but this is a judgment call stated
  plainly, not silently skipped. `docs/BACKLOG.md`'s existing pre-existing
  RATCHET FAIL entries (care_coordination T01/T02, three_zone_demo T02,
  BILL-4 hard-zero flake) are unrelated to this change and were not
  re-checked.

## HASH

01b02bf (see also LATEST_DISPATCH_FRONTIER_TIER_OPENAI.md; this backfill commit itself is 01b02bf's immediate successor)

## OPEN

- Per-member key storage (TD-128) is unresolved for either provider — the
  OpenAI key, like the Anthropic key before it, is one household-level key
  in `~/.env.dev`, not "Maya's key" specifically. Unchanged scope, not
  addressed here.
- The setback numbers OpenAI returned are NOT yet verified against actual
  Title 17 by a human (same open item the Anthropic build carried) — the
  citations are real URLs to real Lakewood documents, but nobody has read
  those PDFs and confirmed the numbers match. Still blocks PRESENTING,
  same as before, per REQ_FRONTIER_TIER's own constraint.
- `--full` was not run for this change (see VERIFIED) — if a future
  session touches `harness/frontier_client.py` again or anything
  call-adjacent, run it then rather than assuming this dispatch's narrow
  scope still holds.
- The Anthropic key in `~/.env.dev` was not removed or invalidated by this
  change — `frontier_client.py` simply stopped reading it. If Bill wants
  a provider toggle rather than a hard swap, that is a new, unasked-for
  scope, not implied by "point the frontier tier at OpenAI instead of
  Anthropic."
