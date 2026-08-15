# DISPATCH_D03 — demo-cutover: consent-gate preflight check + graph pin
Status: BUILT (check built and enforcing; MET assessment is Bill's — see ASSESSMENT)
REQ: docs/requirements/REQ_DEMO_PREFLIGHT_CONSENT_ASSERTION__roadmap-demo-parity__v20260722_2018.md
Branch: demo-cutover (from roadmap; NO merge — per dispatch)
Reconciled-Against: live runs on graph bolt://localhost:7688, 2026-07-28 19:25-19:55 MT

## WHAT WAS BUILT (scripts/demo_preflight.sh only)

1. **Graph pin, script-top, before any check runs**: hard refusal unless
   NEO4J_URI == bolt://localhost:7688 exactly — unset included, no fallback,
   no default. Rationale in-file: the script wipes+reseeds the graph it
   points at, and the pre-existing defaults DISAGREED (Check 3 inline: 7688;
   reset/seed helpers via harness.extraction_queue: 7687 — the hip-harness
   live graph). All downstream defaults are now unreachable.
2. **Header usage comment fixed**: `source ~/hip-roadmap/.env.dev` (was
   `~/hip-dev/.env.demo` — the exact footgun the D-05 read-only dispatch
   flagged: hip-dev's .env.dev points at 7689, the frozen demo's graph).
3. **Checkout guard corrected to roadmap**: EXPECTED_DIR was $HOME/hip-dev —
   the script could not run from this checkout at all, while the REQ's own
   claim is "verified behavior on roadmap." DEMO_MARKER refusal retained.
   Enabling change, required by the REQ's demonstration objective.
4. **Interpreter resolution**: roadmap has no .venv; PYTHON now resolves via
   HIP_DEV_PYTHON (same pattern as scripts/run_harness.sh). Using hip-dev's
   venv BINARY is not sourcing hip-dev's env — NEO4J_URI stays pinned.
5. **Check 5c — the REQ's three assertions**, bracketed by reset+seed before
   and restore after (finally-guarded, pass or fail), same standard as 5b:
   - pane payload == exactly the two expected fact record IDs, derived live
     from the seeded graph by (owner=household, attribute=address|
     zone_district) — the same derivation the live gate itself uses
     (harness/disclosure.py household_disclosure_fact_ids) — and no others;
   - approve ("Yes, go ahead.") → path=frontier_disclosure_resolved,
     tier_target=FRONTIER_MODEL_ID, non-empty reply containing concrete
     setback data (keyword + digit);
   - decline ("No, keep it local.") → tier_target=disclosure_declined,
     structurally never a frontier crossing.
   Turn texts taken verbatim from the boundary_and_consent fixtures
   (T04/T04b, demo_scripts/boundary_and_consent__v20260717_1330.json and
   _decline__v20260718_1008.json), driven in-process via
   scripts.text_demo._run_one → server.voice_orch.process_text_query.
6. **Fault-injection twin** (REQ_HARNESS_DISCIPLINE standard #1):
   DEMO_PREFLIGHT_FI=consent_extra_id | consent_decline_sends each turn the
   check red naming the corruption. `--consent-only` mode runs 5c standalone.

## RED/GREEN EVIDENCE (all live, 2026-07-28)

- Baseline: `git show roadmap:scripts/demo_preflight.sh | grep -c consent`
  → 0. The beat had no execution assertion before this build (the REQ's
  PROBLEM statement, confirmed).
- RED (pin): unset NEO4J_URI → "PREFLIGHT ABORT: NEO4J_URI='<unset>'…",
  exit 1, nothing touched.
- RED (FI, pane): injected bogus ID → FAIL naming the 3-vs-2 ID set.
- RED (FI, decline): injected send-on-decline → FAIL naming
  tier_target='openai:gpt-4.1' where 'disclosure_declined' was required.
- LIVE RESULT: pane leg GREEN (exactly two IDs:
  35427e15… + 5a706f5d…, per-seed), decline leg GREEN (no-send), approve
  leg **RED — TRUE POSITIVE**: frontier call failed because roadmap's
  .env.dev OPENAI_API_KEY is dead (verified directly: HTTP 401 from
  api.openai.com). This is the runbook's standing secrets note proven live.
  Full-check GREEN is blocked by environment (live key), not by code.

## GRAPH SAFETY

7689 and 7687 untouched (pin makes them unreachable; nothing from ~/hip-dev
was sourced). 7688 after all runs: total=11 active=11 v1=0 — canonical seed
restored, no v1 regression.

## ASSESSMENT (vs the REQ's three assertions + the 5b standard; MET is Bill's)

Assertions 1 and 3: built, enforcing, live-green, FI-proven red-on-command.
Assertion 2: built and enforcing — currently red on a genuine environment
defect (dead OpenAI key), which is precisely the class of failure the REQ
orders the check to catch ("the live demo beat is broken and must not be
presented"). The 5b standard (fresh seed, restore after, hard-fail
semantics, do-not-present message) is matched. Recommendation: land a live
OPENAI_API_KEY in ~/hip-roadmap/.env.dev, re-run
`scripts/demo_preflight.sh --consent-only`, and judge MET on that output.
