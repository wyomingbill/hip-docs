# DISPATCH_DEMO_SCRIPT01_GOVERNANCE_VISIBILITY
Status: BUILT
Reconciled-Against: (pending commit — see HASH)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_DEMO_SCRIPT01_GOVERNANCE_VISIBILITY__cascade-offnet-decline-payload__v20260718_1002.md`

## THE ASK

Verbatim, as given (also quoted in full in the REQ doc's THE REQUIREMENT):

> Four objectives on boundary_and_consent (6t). The demo currently shows a good
> answer and hides the governance. Bill: "the demo should show HIP hitting each
> model," and the off-net flag "didn't register." Make the machinery visible.
> Do not fake any of it.
>
> 1. FULL CASCADE VISIBLE. [...] 2. OFF-NET FLAG IS WRONG AND SILENT. [...]
> 3. DECLINE PATH. [...] 4. CODE-BUILT PAYLOAD, SHOWN. [...]
>
> For each: if it cannot be shown truthfully in the UI, say so plainly rather
> than faking it. Prove each live in the browser, not just the harness.

## WHAT WAS DONE

1. Read `docs/INDEX.md`, then traced the full live code path before writing
   anything: `harness/disclosure.py` (payload builder, consent gate),
   `harness/frontier_client.py` (the actual OpenAI call),
   `server/voice_orch.py:2653-2725` (the disclosure gate's wiring —
   confirmed Bill's own line citation, 2607-2632 in his numbering /
   2662-2687 in mine after this session's earlier unrelated edits, matches
   exactly: decline structurally cannot reach `call_frontier`),
   `harness/epistemic_record.py` (the canonical `net` field), and
   `server/static/demo.html` (routing table rendering, `RealtimeChip` as
   the established "don't fake the cascade" pattern, the existing
   `ProofOverlay`).
2. Found, by reading rather than assuming: the frontier hop is not
   mislabeled in the pipeline — it is **entirely absent**, because the
   disclosure gate returns before `router.py`'s dispatch (the only writer
   of `router.jsonl`) ever runs. Documented this precisely in the REQ's
   WHAT'S KNOWN BROKEN before writing any fix, including why a literal
   "edge->mid->core->frontier" ladder for this turn would be fabricated
   (the query never touches mid/core at all — a pre-routing keyword gate
   intercepts it).
3. Found D-08 is real at two independent layers, not just the frontend:
   `server/static/demo.html`'s `RoutingRow.offNet` AND
   `harness/epistemic_record.py:183`'s `net` field both only treated
   `TIER_ESCALATE` (web search) as off-net — Groq-answered mid/core
   (`llama-3.1-8b-instant`/`llama-3.3-70b-versatile`) computed "on" in
   both places. Fixed both, with matched semantics, keyed off
   `tier_target` (the model that actually answered) rather than `tier`.
4. Found, live-reading `harness/disclosure.py:215`: `FRONTIER_MODEL_ID`
   was still `"anthropic:claude-sonnet-4-5-20250929"`, untouched by the
   OpenAI provider swap (01b02bf) — every frontier-written fact since the
   swap carried a wrong `model_id`. Fixed to derive from
   `frontier_client.OPENAI_MODEL` rather than duplicate the string, since
   objective 4's proof surface would otherwise display a fake model name.
5. Added `server/voice_orch.py:_write_disclosure_routing_log` — a
   dedicated `router.jsonl` writer for the disclosure gate's three real
   outcomes (`gate_pending`, `gate_declined`/`gate_unclear`,
   `frontier_crossed`/`frontier_call_failed`), wired into all three
   branches of the existing gate logic. Deliberately NOT reusing
   `_write_routing_log` (which requires a real `decision` object from
   `router.py`'s classifier) — constructing a fake `decision` to force
   through the existing writer would itself be exactly the "faking it"
   the dispatch prohibits.
6. Passed the payload's real fact_ids/attributes into both the new
   routing-log row (`gate_pending`) and `emit_epistemic_record`'s
   `injected_fact_ids` — objective 4's proof, reusing the fact-provenance
   machinery every other turn already uses rather than inventing a new
   claim surface.
7. `server/static/demo.html`: added `netInfo()` (three-way ON /
   OFF·GROQ / OFF·FRONTIER / OFF·WEB / OFF·REALTIME classifier, mirroring
   the backend fix) and `GateChip` (parallel to the existing
   `RealtimeChip` pattern — a dedicated, honestly-labeled chip for
   disclosure-gate rows instead of drawing the cascade `TierBar`, which
   would falsely show edge/mid/core as "tried"). `GateChip` surfaces the
   payload fact_ids/attributes as a hover title on `gate_pending` rows.
   Widened the NET column (36px -> 62px) for the longer labels.
8. Built `demo_scripts/boundary_and_consent_decline__v20260718_1008.json`
   (objective 3) — same T01-T04 as the approve script, T04b changed to
   "No, keep it local." (matches `harness/disclosure.py`'s own
   `_NO_WORDS` leading-word check). Left picker-visible (root
   `demo_scripts/`, not `test/`) per the REQ's stated default — Bill
   described it as a demo variant, not a QA fixture; flagged as a
   reopened, reversible curation decision, not a silent one.
9. Verified all four objectives live against the running dashboard's own
   REST API (`/api/demo/load`, `/api/demo/next`, `/api/routing`,
   `/api/facts`, `/api/transcript`) — browser automation unavailable this
   session (declined earlier by the user). See VERIFIED.
10. Ran `python -m eval.harness --full`, full output read, per CLAUDE.md
    item 12 (voice_orch.py is harness-adjacent).

## WHAT WAS FOUND

Exact citations, all confirmed by direct read before any fix:

- `server/voice_orch.py` (pre-fix): disclosure gate's `is_frontier_disclosure_query`
  branch and its `check_disclosure_response` resolution branch both called
  only `write_transcript_turn`/`emit_epistemic_record` — never
  `_write_routing_log` (`server/voice_orch.py:211-257`, gated to turns that
  go through `router.py`'s own dispatch). Zero `router.jsonl` rows for
  T04/T04b, confirmed by re-running the approve script fresh and observing
  the pre-fix pipeline view had no entries for those turns at all (not
  captured as a screenshot — browser unavailable — but confirmed
  structurally: `_write_disclosure_routing_log` did not exist before this
  dispatch, and it is the only call site that appends to `router.jsonl`
  for this code path).
- `harness/router.py:70`: `TIER_CORE`'s own comment calls it "on-net
  escalation" — the misconception D-08 names is baked into the tier
  definition's comment, not only display code. Left as-is (out of this
  dispatch's scope; the comment doesn't drive any runtime behavior) but
  noted here so it doesn't resurface as a fresh "discovery."
- `harness/disclosure.py:215` (pre-fix):
  `FRONTIER_MODEL_ID = "anthropic:claude-sonnet-4-5-20250929"` — confirmed
  stale by diffing against `harness/frontier_client.py:28`'s
  `OPENAI_MODEL = "gpt-4.1"`, the actual model used since 01b02bf.
- `demo_scripts/boundary_and_consent__v20260717_1330.json`'s own
  `description`/`narration` text (T04, T04b) still says "crosses to
  Anthropic" — same staleness, in demo copy rather than code. NOT fixed
  in this dispatch (out of the four named objectives; fixing it would mean
  a fourth versioned `boundary_and_consent` file under the Naming Law,
  compounding the picker-count question already reopened by item 8 above)
  — logged in OPEN below rather than silently left for a future session to
  rediscover.

## VERIFIED

**Watched run — objectives 1, 2, 4 (approve path), fresh reset+seed via
`/api/demo/load`, then `/api/demo/next` x5 through T04b:**
- `GET /api/routing` after the run: 5 rows, all real, all previously either
  correct-but-mislabeled or (T04/T04b) absent:
  - `"query":"When's trash pickup?"` — `tier_target="qwen2.5:7b"` → netInfo
    computes ON (correct, unchanged).
  - `"query":"What's the best morning to take the car in?"` —
    `tier="mid"`, `tier_target="llama-3.1-8b-instant"` → netInfo computes
    **OFF·GROQ** — this is D-08 fixed and live-caught in the same run, not
    a synthetic example: this turn genuinely routed to Groq.
  - `"query":"What's the setback...variance?"` (T04) —
    `disclosure_kind="gate_pending"`, `tier_target="disclosure_gate"`,
    `assembled_by="code:harness.disclosure.build_payload"`,
    `payload_fact_ids=["40ae7b7b-...","f23150f9-..."]`,
    `payload_attributes=["address","zone_district"]`, `outbound_call=false`.
    Cross-checked against `GET /api/facts`: both fact_ids resolve to real
    `household`-owned `address`/`zone_district` rows — the payload proof
    is genuine data, not asserted text.
  - `"query":"Yes, go ahead."` (T04b) — `tier="frontier"`,
    `tier_target="openai:gpt-4.1"`, `disclosure_kind="frontier_crossed"`,
    `outbound_call=true` → netInfo computes **OFF·FRONTIER**, distinct
    from OFF·GROQ above in the same response.
- `logs/turns_demo.jsonl` tail, same run (the canonical D-1 record, the
  file the PROOF overlay tails verbatim): `net=on` for both local
  `qwen2.5:7b` turns, `net=off` for the Groq mid turn, `net=on` for the
  gate-pending turn (correct — nothing had left yet), `net=off` for the
  frontier-resolved turn. Both the frontend fix and the backend
  `epistemic_record.py` fix confirmed independently, same run.
- `logs/dashboard.log`: `harness.frontier_client:call_frontier ... model=gpt-4.1`
  — the real outbound call, matching `tier_target="openai:gpt-4.1"`
  exactly (no drift between what was logged and what was called).

**Watched run — objective 3 (decline path), fresh reset+seed via
`/api/demo/load` on the new script:**
- Baseline `GET /api/facts` immediately after load (before any turns):
  1 `zone_district` row (`7b1cee33-...`).
- Fired T01-T04, then T04b ("No, keep it local.").
- `logs/dashboard.log`: no new `call_frontier` line — the last one present
  is timestamped before this run's `session_start`, from the prior
  approve-path test.
- `GET /api/facts` after the decline turn: still 1 `zone_district` row,
  same fact_id — no new fact.
- `GET /api/transcript`: last exchange is
  `user: "No, keep it local."` / `hip: "Keeping that local, then."` —
  `DECLINE_DISCLOSURE_REPLY` verbatim.
- `GET /api/routing`: the decline turn's row —
  `disclosure_kind="gate_declined"`, `tier_target="disclosure_declined"`,
  `outbound_call=false` — a real, distinct, on-screen row (not merely
  absent, not merely inferred from transcript prose).

**Watched run — `python -m eval.harness --full`, twice, full output read
both times, exit code captured explicitly (not through a masking pipe):**
- Both runs: `EXIT_CODE=1`, `RATCHET FAIL — regressed vs baseline:
  ['L2:care_coordination.T03']` (`bill: 'Does that change affect the
  household budget?'` — `[FAIL] refusal type none — got empty_set;
  reply='No information on how it affects the household budget was
  shared.'`).
- Run 1: no NEW FAILURES line (L6 passed, 1/1). Run 2: `NEW FAILURES (not
  in baseline): ['L6:record-invariants']` — L6 flipping pass/fail with
  zero code change between the two runs matches the already-established,
  pre-existing BILL-4/I-10 hard-zero flake (same behavior observed and
  documented earlier this session on an unrelated dispatch).
- `care_coordination.T03` did NOT flip — failed identically both times,
  same reply text. Checked against `docs/deliverables/
  HIP_DefectRegister__v20260715_1930.md` line 61 (D-16) before concluding
  anything: D-16 already records this EXACT turn, this EXACT failure
  shape (`EMPTY_SET_RE` conflating a model-generated hedge with a
  structural refusal), first observed 2026-07-16 — "FAILed once (of 3
  same-session runs) ... reply='No information on changes to the
  household budget is available at this time.'" — near-identical reply
  wording, same root cause, pre-dating this dispatch by two days.
  Confirmed by tracing, not assumed: `"Does that change affect the
  household budget?"` does not match `harness/disclosure.py`'s
  `_ZONING_QUERY_RE`, so it never reaches `is_frontier_disclosure_query`,
  `check_disclosure_response`, or any branch this dispatch touched: the
  turn's reply text and refusal classification are generated entirely
  outside the code this dispatch changed. The `net` field
  (`harness/epistemic_record.py`, the only place this dispatch touches
  `build_epistemic_record`) has no bearing on reply text or
  `classify_refusal`'s regex match. Concluded: pre-existing D-16 flake,
  not attributable to this dispatch. D-16 itself remains NOT FIXED — not
  this dispatch's scope (a harness-assertion-vocabulary fix, per the
  register's own recommended structural fix: assert `guard_kind` from the
  d1.1 record instead of regex-matching reply text).

**Reasoned about, not independently pixel-verified:** no browser
automation was available this session (declined earlier by the user, per
the system reminder). Every "prove ON SCREEN" clause above was satisfied
by driving the exact REST endpoints the browser's LOAD/NEXT buttons call
and reading the real JSON responses, plus reading the actual
`server/static/demo.html` React source to confirm what the DOM renders for
that exact data shape (`netInfo()`/`GateChip` traced by hand against the
live API payloads above, field by field). This is not the same as a human
watching pixels render and is stated here plainly rather than silently
substituted, per the REQ's own CONSTRAINTS section.

## HASH

Pending — see the commit that follows this dispatch doc in the same push.

## OPEN

- `demo_scripts/boundary_and_consent__v20260717_1330.json`'s own narration
  text still says the frontier call "crosses to Anthropic" — stale since
  the OpenAI provider swap. Not fixed here (see WHAT WAS FOUND); would
  need its own versioned file under the Naming Law. Flagged, not silently
  carried forward.
- The decline-variant script's picker visibility (root `demo_scripts/` vs
  `test/`) is a judgment call stated in the REQ, not confirmed with Bill.
  Easy to move later; noted so it isn't mistaken for an oversight.
- `harness/router.py:70`'s `TIER_CORE` comment ("on-net escalation") is
  factually wrong per D-08 but drives no runtime behavior — left
  uncorrected, noted so a future D-08-adjacent session doesn't treat it as
  a fresh finding.
- Per-member key storage (TD-128, noted in the OpenAI-swap dispatch) is
  still unaddressed — unrelated to this dispatch, unchanged.
- No pixel-level browser confirmation this session (see VERIFIED) — if
  Bill wants that, either reconnect Chrome (`/chrome`) or check visually
  himself; the data-level proof above is not a substitute, and is labeled
  as such rather than presented as equivalent.
