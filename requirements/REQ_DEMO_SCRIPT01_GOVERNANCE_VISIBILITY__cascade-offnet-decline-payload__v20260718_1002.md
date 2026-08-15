# REQ_DEMO_SCRIPT01_GOVERNANCE_VISIBILITY
Status: BUILT
Reconciled-Against: (pending commit — see dispatch HASH)

## THE REQUIREMENT

Bill's own words, verbatim (from DISPATCH: DEMO_SCRIPT01_GOVERNANCE_VISIBILITY__cascade-offnet-decline-payload__v20260718):

> Four objectives on boundary_and_consent (6t). The demo currently shows a good
> answer and hides the governance. Bill: "the demo should show HIP hitting each
> model," and the off-net flag "didn't register." Make the machinery visible.
> Do not fake any of it.
>
> 1. FULL CASCADE VISIBLE. T04 hit the frontier but the routing pipeline never
>    shows that hop — only EDGE/MID rows. Show the frontier turn traversing the
>    tiers: which tiers were tried, which answered. A technologist needs to see
>    edge -> mid -> core -> frontier for the one query that escalated. If the
>    pipeline data does not currently capture the frontier hop, say why and what
>    it would take.
>
> 2. OFF-NET FLAG IS WRONG AND SILENT. Two problems:
>    a. Every row shows NET=ON, but D-08 says NET=ON is FALSE on Groq — edge/mid
>       run on Groq, which is external. The flag is lying on local turns.
>    b. The one turn that genuinely crossed the boundary (T04 -> OpenAI) does not
>       register OFF-NET at all. The real network egress is invisible while the
>       local turns falsely show ON.
>    Fix the semantics: the flag must truthfully distinguish local-only from
>    external-Groq from frontier-egress. This is the demo's core honesty claim —
>    if NET is wrong, the whole "we show you what leaves" story is undermined.
>
> 3. DECLINE PATH. Add a variant where Maya declines at the T04 gate ("No, keep
>    it local"). Prove ON SCREEN:
>    - nothing leaves the boundary
>    - the outbound call is not reached (you traced this at
>      voice_orch.py:2607-2632 — surface it, do not just assert it)
>    - the epistemic timeline shows NO new ASSERTED fact
>    - HIP stays local and says so
>
> 4. CODE-BUILT PAYLOAD, SHOWN. The claim that a model did not compose the
>    payload is invisible. Add a PROOF view or pane showing the outbound payload
>    was assembled by code from fact rows (address, zone_district by fact_id),
>    with the model never in the assembly path. This is the governance claim a
>    technologist will most want to verify.
>
> For each: if it cannot be shown truthfully in the UI, say so plainly rather
> than faking it. Prove each live in the browser, not just the harness.

## THE ACCEPTANCE TEST

Against `boundary_and_consent__v20260717_1330.json` run through the live
dashboard's own API (`/api/demo/load` + `/api/demo/next` — the exact calls
the browser buttons make; browser automation is unavailable this session,
see CONSTRAINTS), fresh reset+seed each time:

1. **Cascade visibility.** After T01-T04 fire, `GET /api/routing` contains
   rows for T04 (gate shown) that were previously entirely absent (zero
   rows today — not mislabeled, ABSENT, see WHAT'S KNOWN BROKEN item 1).
   The row is honestly labeled: it does NOT render as if edge->mid->core
   were traversed (they were not — the disclosure gate intercepts before
   `router.py` dispatch runs at all), and the REQ doc states plainly, in
   this section, why a literal edge->mid->core->frontier ladder cannot be
   shown truthfully for this query (see WHAT'S KNOWN BROKEN item 1) and
   what the honest alternative is (a distinctly-labeled non-cascade chip,
   the same pattern already used for realtime voice turns —
   `server/static/demo.html:149-158`'s `RealtimeChip`).
2. **NET flag.** After T01 (edge/local), T02 or T03 (mid/core, Groq), and
   T04b-approve (frontier) fire, the routing table's NET column reads ON
   for the edge/local row and OFF for the Groq row and OFF for the
   frontier row — each distinguishable from the other two, not a single
   collapsed ON/OFF. Verified by reading `tier_target` in the raw
   `/api/routing` response for each row (`qwen2.5:7b` vs
   `llama-3.1-8b-instant`/`llama-3.3-70b-versatile` vs the frontier
   provider tag) and confirming the rendered NET label matches.
3. **Decline path.** A new script variant exists where T04b's text is a
   decline ("No, keep it local." or equivalent, matching
   `harness/disclosure.py`'s own `_NO_WORDS` vocabulary). Run live:
   - `POST /api/demo/next` for the decline turn returns without any
     `harness.frontier_client:call_frontier` log line appearing in
     `logs/dashboard.log` afterward (proves the outbound call was not
     reached — not merely asserted from reading voice_orch.py:2607-2632).
   - `GET /api/facts` shows the same `zone_district` row count before and
     after the decline turn (no new ASSERTED fact).
   - The reply text is `DECLINE_DISCLOSURE_REPLY` ("Keeping that local,
     then.") and this is visible in `/api/transcript`.
   - The routing table (not just the transcript) carries a visible row for
     the decline turn distinct from the approve case — "prove ON SCREEN"
     per Bill's own words, not just in a log tail.
4. **Payload-built-by-code proof.** After T04 (gate shown) fires, either
   the `/api/demo/proof` router source or an equivalent on-screen surface
   shows, for that turn's row: the exact fact_ids and attributes included
   (`address`, `zone_district`) and an explicit marker identifying the
   assembly as code (not a model) — e.g. a field naming
   `harness.disclosure.build_payload` — AND the row carries no
   `model_id`/`inference_ms`/token fields (the absence, on a turn that
   produced a real reply, is itself part of the proof: nothing that looks
   like a model call ran to produce this content).

Every clause above is proven by firing real turns against the live
dashboard process and reading real API/log/file output — no clause is
satisfied by a harness-only run or by prose assertion.

## WHAT'S ALREADY DONE

- The frontier tier itself (disclosure gate, OpenAI BYOK call, ASSERTED
  write-back) is BUILT and live-verified — `REQ_FRONTIER_TIER` (both the
  original and the OpenAI-swap update),
  `DISPATCH_FRONTIER_TIER_BUILD/LIVE/VERIFY/OPENAI`. This REQ does not
  redo any of that; it is entirely about VISIBILITY of governance
  machinery that already runs correctly but is not shown, mislabeled, or
  silent.
- `RealtimeChip` (`server/static/demo.html:145-158`) already establishes
  the exact pattern this REQ needs for the frontier/gate rows: "only what
  actually ran is displayed," a dedicated chip instead of the cascade
  `TierBar` when the cascade genuinely did not run. Reused, not
  reinvented.
- `ProofOverlay` (`server/static/demo.html:1067-1173`) and
  `/api/demo/proof` (`server/demo_dashboard.py:706-748`) already exist,
  already tail real files with sha256 + mtime, and already register
  `router.jsonl` as "every row in the routing table came from this file."
  Objective 4 extends this existing surface; it does not require a new
  pane from scratch.
- D-08 is already registered (`docs/BACKLOG.md` #29,
  `docs/deliverables/HIP_DefectRegister__v20260715_1930.md` line 52) —
  this REQ is D-08's fix, not new-discovery work.

## WHAT'S KNOWN BROKEN

1. **The frontier hop is not mislabeled — it is entirely absent from the
   routing pipeline, and the reason is architectural, not a display bug.**
   `voice_orch.py`'s disclosure gate (lines 2598-2664) resolves and
   returns BEFORE `router.py`'s dispatch ever runs — it never calls
   `_write_routing_log` (`server/voice_orch.py:211-257`, the only writer
   of `router.jsonl`, the file `/api/routing` reads). T04 (gate shown) and
   T04b (decline/approve) currently write ZERO routing-log entries. The
   turns are real (visible in `/api/transcript` and `turns_demo.jsonl`)
   but invisible in the pipeline view specifically.
   **Consequence for objective 1's literal wording:** the query never
   traverses edge->mid->core at all — `is_frontier_disclosure_query`
   (`harness/disclosure.py:57-58`) is a keyword regex checked BEFORE
   ordinary routing/classification runs. There is no cascade escalation to
   show truthfully for this turn. Showing edge/mid/core as "tried" would
   be fabricated. The honest fix: (a) make the gate write real
   routing-log entries (currently the gap), and (b) render them with a
   dedicated non-cascade chip (matching `RealtimeChip`'s established
   pattern) that plainly states the cascade was not traversed and why,
   rather than drawing a false ladder.
2. **D-08 is real and reaches into the canonical record, not just the
   frontend.** Two independent, currently-wrong implementations:
   - `server/static/demo.html:164` (`RoutingRow`'s `offNet` check) treats
     only `web_fetch`/`web_search`/`serpapi`/`realtime` as off-net —
     Groq-routed mid/core (`GROQ_MODEL_MID="llama-3.1-8b-instant"`,
     `GROQ_MODEL_CORE="llama-3.3-70b-versatile"`,
     `server/voice_orch.py:159-160`) render as ON.
   - `harness/epistemic_record.py:183`:
     `"net": ("off" if tier == "escalate" else "on") if tier else None` —
     the SAME bug at the canonical-record layer: only `TIER_ESCALATE`
     (web search) counts as off; Groq mid/core (`tier="mid"`/`"core"`)
     compute `net="on"`. This field is currently unread by any renderer
     (confirmed by grep — dead for display purposes today) but it IS
     written to `turns_demo.jsonl`, which the PROOF overlay tails
     verbatim. Fixing only the frontend would leave a false `"net":"on"`
     sitting in the exact raw file a technologist opens to verify. Both
     need the fix, matched to the same semantics.
   - The authoritative signal for "did this leave the local network" is
     `tier_target` (the model that actually answered — already diverges
     from `tier` alone per `server/voice_orch.py:222-225`'s own
     documented reasoning), not `tier`. `tier_target ==
     LOCAL_MODEL("qwen2.5:7b")` is the only truly local case.
   - Even `harness/router.py:70`'s own comment calls `TIER_CORE`
     "on-net escalation" — the misconception is baked into the tier
     definition's comment, not only the display code. Noted for
     awareness; fixing that comment is in scope as a trivial accuracy
     correction, not a new investigation.
3. **The decline branch is real but produces no evidence trail a UI can
   point at.** `voice_orch.py:2607-2632` confirmed by direct read: the
   `if _disc_verdict == "decline"` branch (line 2609) sets the reply and
   falls through to `write_transcript_turn`/`emit_epistemic_record` —
   `call_frontier` (line 2619) is lexically inside the `else` branch for
   `"approve"` only, so decline structurally cannot reach it. But no
   routing-log row, no distinct field, nothing observable today
   distinguishes a decline from an approve except reading reply text —
   there is nothing to point a technologist at that isn't "trust the
   prose." No demo script exercises the decline path at all today (every
   existing T04b in `boundary_and_consent__v20260717_1330.json` is
   "Yes, go ahead.").
4. **The payload-built-by-code claim has no on-screen evidence, only
   prose in code comments.** `harness/disclosure.py:98-132`
   (`build_payload`) and `render_disclosure_prompt` (135-152) are real,
   already code-only, already fact_id-keyed — the CLAIM is true, but nothing
   surfaces the fact_ids/attributes/assembly-source together on screen or
   in the existing PROOF sources, because (per item 1) no routing-log row
   exists for T04 at all yet.
5. **Side finding, in scope to fix while touching this code (not a new
   REQ, per Requirements Discipline item 6 — "ask the system, not the
   docs" surfaced this live):** `harness/disclosure.py:215`
   `FRONTIER_MODEL_ID = "anthropic:claude-sonnet-4-5-20250929"` is stale —
   the provider swap to OpenAI (`harness/frontier_client.py`,
   commit 01b02bf) updated `frontier_client.py`'s own `OPENAI_MODEL =
   "gpt-4.1"` but never touched this constant. Every frontier-written fact
   since the swap carries a wrong `model_id` in its write-decision
   rationale. Directly relevant here: objective 4's proof surface must not
   itself display a fake model name — fixing this is a precondition for
   objective 4 being honest, not a separate task.

## CONSTRAINTS

- **No browser automation available this session** (declined earlier by
  the user; `/chrome` not connected). Every "prove ON SCREEN" /
  "prove live in the browser" clause in this REQ is satisfied by driving
  the dashboard's own REST API (`/api/demo/load`, `/api/demo/next`,
  `/api/routing`, `/api/facts`, `/api/transcript`, `/api/demo/proof`) —
  the exact endpoints the browser's buttons call — and reading real
  responses, plus reading the actual rendered React source to confirm
  what the DOM would show for that data. This is not equivalent to a
  human watching pixels render, and is stated here plainly rather than
  silently substituted. If Bill wants pixel-level visual confirmation,
  that requires either reconnecting Chrome or Bill checking visually
  himself.
- **Do not fake any signal.** No hardcoded/simulated tier progression, no
  invented "traversed edge/mid/core" state for a turn that didn't. Where
  the truthful answer is "this turn took a different path entirely,"
  the UI must say that, not draw a misleading cascade bar.
- **Existing working paths are sacred.** `RealtimeChip`'s existing
  behavior, the `TierBar` cascade rendering for genuine edge/mid/core
  turns, `ProofOverlay`'s existing four source types, and DEMO-004
  (`/api/demo/proof` returns router/turns_demo/run_status with non-null
  mtime/sha256_8) must not regress. The in-flight uncommitted
  `server/static/demo.html` diff (LOAD button dead-code fix, TALK MODE
  rename, HOW TO READ THIS / PROOF header buttons — from a different,
  unrelated dispatch, still uncommitted as of this REQ) must not be
  clobbered or silently reverted; this REQ's edits build on top of it.
- **Picker scope.** The decline-path script variant (objective 3) is a
  new file under the Naming Law. Whether it belongs in `demo_scripts/`
  root (picker-visible, presentable) or `demo_scripts/test/`
  (proof-only) reopens the "picker shows exactly 3" curation from the
  prior session. Default: picker-visible, since Bill described it as a
  demo "variant" for a live audience, not a QA fixture — stated here so
  the decision is visible and reversible, not buried.
- Per CLAUDE.md item 12: before calling this done, run
  `python -m eval.harness --full` and read the actual RATCHET
  FAIL/NEW FAILURES output. This REQ's changes touch `voice_orch.py`
  (harness-adjacent) — the full ratchet applies, not a targeted subset.
