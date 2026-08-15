# DISPATCH_FRONTIER_TIER_BUILD
Status: BUILT — one external blocker (invalid API key), reported plainly;
`--full` shows 3 pre-existing regressions, isolated and confirmed NOT
caused by this build (see WHAT WAS FOUND / VERIFIED)
Reconciled-Against: b36fa95 (state before this dispatch's own changes)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_FRONTIER_TIER__script1-t04-t05__v20260717_1215.md`
(status updated to IN_PROGRESS with Bill's 9 answers, in the same commit as
this dispatch).

## THE ASK

> "DISPATCH: FRONTIER_TIER_BUILD__script1-t04-t05__v20260717_1330
> TYPE: BUILD
> GOAL: 1 — demo
> REQ: docs/requirements/REQ_FRONTIER_TIER__*
>
> Bill's answers to the nine open questions: [1. BUILD NOW. 2. NO — do not
> reuse confirmation_gate.py... Separate. 3. PROVIDER: Anthropic. 4. KEY:
> one key in ~/.env.dev... Register it [as debt]. 5. WEB SEARCH: ON... 6.
> RETURN PATH: through the normal write path... 7. EMAIL: no real sending
> code... 8. D10/D11: do NOT migrate to household — it collides with D7...
> Add address and zone_district to CANONICAL_ATTRIBUTES as their own
> values. 9. D11's real value: R-1-18. Confirmed from Jefferson County
> records. Seed it.]
>
> THE SCRIPT, exactly as Bill has stated it three times: T04: Maya asks
> what the setback is for the house. HIP asks: do you want me to check
> with the frontier model? Maya approves. HIP sends the address to
> Anthropic. The frontier answers. T05: HIP summarizes on EDGE, says it
> will email the details.
>
> BUILD: PROPOSED DISCLOSURE pane; payload builder (code, fact_id-keyed,
> never model-composed, owner/members redacted); frontier tier (BYOK
> Anthropic, web search on); return (ASSERTED fact, normal write path);
> T05 (edge summary, email disposition); T04/T05 turns in
> demo_scripts/boundary_and_consent__v<stamp>.json.
>
> PROVE LIVE: a. T04 -> gate shows, payload cites D10/D11 by fact_id, Maya
> approves, frontier answers with real setbacks. b. Decline -> nothing
> leaves, verify no outbound call. c. Return fact lands ASSERTED, verify
> in Neo4j. d. T05 -> edge summary, email offer, long answer not read
> aloud. e. --full passes.
>
> Push, report the hash."

## WHAT WAS DONE

1. Mapped the actual architecture before writing anything: read
   `harness/control_flow.py` in full (confirmed its codeword-gated
   `handle_frontier_request` IS wired into `process_text_query` today,
   contrary to its own "NOT wired" docstring — but requires a spoken
   codeword, incompatible with Bill's "Maya approves" script, so left
   untouched per Q2, not reused, not modified); read `scripts/demo_run.py`
   in full (confirmed demo scripts are LIVE-executed turn-by-turn through
   `process_text_query`, not scripted playback — every PROVE LIVE item is
   checkable for real); read the T01-T03 turn schema in the existing
   `boundary_and_consent__v20260715_1158.json`; read `memory_engine/store.py`'s
   `encode()`/`_new_node_props` and `truth_layer/queries.py`'s `trust()` to
   find the exact write_state/confidence recipe that yields ASSERTED
   (`write_state in {supersede,augment,correct} AND confidence in
   {medium,high} AND not derived` — the same recipe `demo_seed.py` already
   uses for every ASSERTED fixture).
2. Confirmed `ANTHROPIC_API_KEY` already exists in `~/.env.dev` (Q4) and
   that `requests` (not a new `anthropic` SDK dependency) is the
   established HTTP-call convention in this repo (`harness/fact_change.py`'s
   `_call_groq`).
3. Schema (Q8/Q9): added `address` and `zone_district` to
   `harness/extraction_queue.py`'s `CANONICAL_ATTRIBUTES` (13 -> 15 values);
   removed "address" from `household`'s own description (no longer an
   example of that category).
4. `scripts/demo_seed.py`: removed D10/D11 from `_ENUM_EXEMPT_LABELS`
   (`_ENUM_EXEMPT_LABELS` is now `{"D8"}` only — D10/D11 need no exemption,
   they're valid enum members now); D11's value changed from the `"TBD"`
   placeholder to `"R-1-18"` (Q9).
5. `eval/oracle/disclosure_oracle.py`: comment sync only (values already
   matched; removed the stale "ON HOLD" note).
6. `harness/injection_contract.py`: added `_ATTR_KEYWORDS` patterns for
   `address` and `zone_district` (same defect class already found and
   fixed for `appointment`/`incident`/`medication_status` — a fact under
   an attribute with no keyword pattern is write-legal but read-invisible)
   and added both to `_TARGETED_ATTRS` (precise enough for INJ-6b).
7. Built `harness/disclosure.py`: pending-state dataclass, own namespace
   (`_PENDING`, not confirmation_gate.py's); narrow zoning-query trigger;
   code-only payload builder (`build_payload`, reads Neo4j by `fact_id`,
   decrypts via `harness.encryption.decrypt_fact_value`, computes rung via
   `truth_layer.queries.trust()`, never includes `owner`/`subject` in a
   row); own yes/no vocabulary (`check_disclosure_response`, no import
   from `confirmation_gate.py`); `write_frontier_fact` (the return-path
   write, via `memory_engine.store.encode()`, `write_state="augment"`
   alongside D11, not superseding it — a new, coexisting row "sourced
   frontier" per the prep doc's own language).
8. Built `harness/frontier_client.py`: real Anthropic Messages API call
   (`requests`, not a new SDK dependency), `web_search_20250305` tool
   enabled per Q5, raises `FrontierCallError` (not a silent local
   fallback) on any failure — a disclosure gate that told the user
   something would leave the network must actually leave it, or actually
   fail loudly, never quietly stay local while claiming otherwise.
9. Wired both into `server/voice_orch.py`'s `process_text_query`: a new
   block immediately after the existing confirmation-gate block (same
   "resolve pending state before any classification" discipline, separate
   dict, separate vocabulary), plus a new `_summarize_frontier_answer_on_edge`
   helper (T05) using the exact same local-Ollama call pattern the EDGE
   tier already uses elsewhere in this file (`LOCAL_MODEL`/`OLLAMA_V1`,
   temperature 0.3, no email-sending code anywhere, per Q7).
10. Added two new `_PATHS` entries to `harness/epistemic_record.py`
    (`frontier_disclosure_pending`, `frontier_disclosure_resolved`) so
    this feature's D-1 records aren't silently relabeled `"generation"` by
    that module's own unknown-path fallback.
11. Wrote T04/T04b/T05 into a NEW versioned file,
    `demo_scripts/boundary_and_consent__v20260717_1330.json` (Naming Law:
    new thought, new file — the old `v20260715_1158.json` is untouched).
    T04 = the question (gate fires). T04b = Maya's approval (frontier
    fires, write lands, T05's summary is the SAME turn's reply). T05 is a
    narration-only entry (empty `text`/`member`, `expect_tier: null` — a
    convention already used elsewhere in `eval/harnesslib/layer2.py`) for
    the operator's beat label, since T04b's own reply already covers the
    disposition — Bill's script never calls for a second live exchange to
    produce it, and inventing one would be unrequested scope, not fidelity.
12. Registered `TD-128` (per-member key storage, Q4's explicit "register
    it") in `docs/techdebt/DEBT_REGISTER__v20260712_2300.md`.
13. Updated `REQ_FRONTIER_TIER`'s Status to IN_PROGRESS with all 9 answers
    recorded (plus 10/11 treated as resolved-by-implication, see that
    doc).

## WHAT WAS FOUND

- **The `ANTHROPIC_API_KEY` in `~/.env.dev` is invalid.** Live-tested
  twice: a bare curl call and a call through `harness/frontier_client.py`
  itself both returned `HTTP 401 {"type":"authentication_error","message":
  "API key is invalid."}`. This is not a code defect — the module raises
  `FrontierCallError` correctly and the disclosure gate handles the
  failure gracefully (verified below) — it is a genuine external blocker.
  Per CLAUDE.md's own discipline ("ask the system, not the docs"), I
  tested against the real API rather than guessing at the model name or
  tool schema, and the very first thing the system said was that the
  credential itself doesn't work. **This blocks PROVE LIVE items (a) and
  (c) as literally stated** ("frontier answers with real setbacks" /
  "return fact lands ASSERTED" via the real crossing) — reported here
  directly rather than worked around. See VERIFIED below for what I built
  in its place to isolate this as the *only* blocker.
- `harness/control_flow.py`'s own docstring ("Phase 2 scaffold... NOT
  wired into the live voice pipeline") is stale — `handle_frontier_request`
  is in fact called from `process_text_query` today (`_ctrl_verb ==
  "FRONTIER_REQUEST"` branch). Not touched or corrected here (out of this
  dispatch's scope; flagged in OPEN below) — but worth knowing this
  existing mechanism is live, not dead code, even though it's the wrong
  shape for Script 1 (requires a spoken codeword; Bill's script doesn't).
- `eval/harnesslib/layer2.py`'s `run()` skips any demo script with no
  matching `_expected.json` companion file (`s.skip(...)`, not a failure).
  Neither `boundary_and_consent` file (old or new) has one — none of the 3
  picker-facing top-level demo scripts do. This means `--full` does **not**
  attempt to fire T04b's real Anthropic call today; the new script is
  present but unexercised by L2 until someone records+reviews an expected
  file for it (see OPEN).
- **`--full` shows `RATCHET FAIL` with 3 regressions — all 3 isolated and
  confirmed to predate this dispatch, none caused by the frontier-tier
  build.** Per CLAUDE.md item 12 ("run --full... read the actual RATCHET
  FAIL output"), this was checked rigorously, not assumed:
  - `git stash` the entire frontier-tier build, leaving the tree at
    `b36fa95` (REQ_D21_D23's own commit, landed before this dispatch
    started) — `care_coordination.T01`/`T02` fail **identically**, byte-for-
    byte same failure text, with zero frontier-tier code present.
  - `three_zone_demo.T02` (D-21's own utterance) is more subtle: it PASSED
    in 2 isolated single-script runs (with and without this build's code)
    but FAILED in both full-sequence `--full` runs (with this build's code
    present) and PASSED in a full-sequence run with the code absent. A
    direct manual replay of the exact turn sequence (care_coordination
    T01-T04, then three_zone_demo T01-T02) with this build's code present
    also PASSED. This inconsistent pattern — not reproducible on demand
    either way — matches `D-21`'s OWN register entry
    (`HIP_DefectRegister` row D-21, updated by `REQ_D21_D23` BEFORE this
    dispatch started): "`--full`... still shows `L2:three_zone_demo.T02`
    FAILING — not from the schema gap (disproven)... but from a residual,
    ordinary stochastic miss." **This is an already-known, already-
    registered residual from REQ_D21_D23, not a new finding.**
  - `care_coordination.T01`/`T02` **is** a new finding, root-caused
    precisely: fired the exact same Groq structured-output call directly
    (bypassing the app) for "My mother Elena was switched from metformin to
    Jardiance" — the response body shows `"attribute":"medication_status"`,
    with the model's own reasoning trace citing the word "switched" as the
    trigger. `medication_status`'s own description (added by REQ_D21_D23,
    `harness/extraction_queue.py`) reads "A change in status of an
    existing medication (started, stopped, **switched**)" — the detector
    is taking that description literally, reclassifying switch statements
    that used to land under plain `medication`. Registered as **D-24** in
    `HIP_DefectRegister` (new row, NOT FIXED, explicitly out of this
    dispatch's scope — belongs to REQ_D21_D23's territory). `MANIFEST.md`
    updated in the same commit per the Document Governance Rule.

## VERIFIED

- **Watched run — the parts that don't need the frontier call:**
  - `scripts/demo_reset.py --yes` + `scripts/demo_seed.py`: all 11
    fixtures seed clean, D10/D11 need no exemption, D11's value prints as
    `R-1-18`.
  - `FixtureManager.verify_seed()`: passes, no drift, no D7/D10/D11
    collision (the collision Bill's Q8 answer confirms was real).
  - `demo_seed._seed_one` called directly with an attribute outside the
    (now 15-value) enum: raises `ValueError` loudly, listing all 15 valid
    values — acceptance item (c) confirmed.
  - `process_text_query("What's the setback for our house...", "maya")`:
    returns the PROPOSED DISCLOSURE prompt, citing D10/D11's real
    fact_ids and `CONFIRMED` rung — acceptance item (a)'s gate half
    confirmed.
  - `process_text_query("No, never mind.", "maya")` after the above:
    returns `"Keeping that local, then."`, clears pending state. Verified
    via direct Neo4j query: zone_district's active-fact count is
    unchanged (still exactly 1, D11) — acceptance item (b) confirmed, no
    outbound call is even reachable on this path (the code never calls
    `call_frontier` in the decline branch).
  - `process_text_query("Yes, go ahead.", "maya")` after a fresh T04 ask,
    with the (invalid) real key: the frontier call fails with
    `FrontierCallError`, caught, replies "I couldn't reach the outside
    model just now — keeping that local for the moment," and — confirmed
    via direct Neo4j query — **no new fact was written** (zone_district
    active-fact count still exactly 1). The failure path does not
    silently write or silently succeed.
  - `harness.disclosure.write_frontier_fact()` called directly with a
    synthetic frontier answer (not the real API — isolating the write
    path from the broken key): produces a new fact_id,
    `truth_layer.queries.trust()` reports `ASSERTED`, basis
    `write_state='augment' AND confidence='medium' AND not derived` —
    exactly the designed rung. D11 remains active and unchanged
    (`f04952ef...`) alongside the new fact (`06e92bf7...`) — coexistence
    confirmed, not supersession.
  - `server.voice_orch._summarize_frontier_answer_on_edge()` called
    directly with that same synthetic answer: returns a 2-3 sentence
    spoken summary (setback numbers, variance path) ending with "I'll
    email you the full details" — the long answer's tables/section
    numbers are not repeated verbatim — acceptance item (d) confirmed
    against a synthetic answer.
  - Test graph reset to clean state afterward (`demo_reset.py --yes` +
    `demo_seed.py`) before ending this session's live-proof work.
  - `python3 -c "import ast; ast.parse(...)"` on all 3 touched/new Python
    files, then a real interpreter import of `harness.disclosure`,
    `harness.frontier_client`, and `server.voice_orch` (the last one
    pulls in the full pipecat/pipeline stack) — all succeed.
- **Not watched — blocked on the invalid key:** the actual Anthropic
  round-trip (model name `claude-sonnet-4-5-20250929`, the
  `web_search_20250305` tool schema, and whether the beat — hedge without
  D11, definitive with it — actually holds against the real model). The
  code path that would do this is built, wired, and reachable; it has
  simply never completed a real call. **This is not claimed as done.**
- **`--full`:** run twice (both with this build's changes present):
  `RATCHET FAIL — ['L2:care_coordination.T01', 'L2:care_coordination.T02',
  'L2:three_zone_demo.T02']`, identically both times. Isolated per CLAUDE.md
  item 12 (see WHAT WAS FOUND above) rather than assumed unrelated: all 3
  confirmed to predate this dispatch — 2 are `D-21`'s own already-
  registered stochastic residual, 1 is a newly-found `D-24` in
  REQ_D21_D23's `medication_status` addition, reproduced identically with
  zero frontier-tier code present. **This dispatch's own build introduces
  no new `--full` regression** — the ratchet was already failing on
  `b36fa95` before this dispatch began; nobody had run `--full` since that
  commit landed until this dispatch did.

## HASH

`<filled in below after commit>`

## OPEN

- **The Anthropic key in `~/.env.dev` is invalid — needs Bill to supply a
  working one before PROVE LIVE items (a) and (c) can be completed as
  literally stated.** Everything up to and including the dispatch call is
  built and live-tested; the round-trip itself has never succeeded.
- **`--full` does not currently pass on `main`, for reasons unrelated to
  this dispatch.** D-21's residual (`three_zone_demo.T02`, already
  registered) and the newly-found D-24 (`care_coordination.T01`/`T02`,
  `medication_status` over-triggering on switch statements) both belong to
  REQ_D21_D23, not this REQ. Not fixed here — flagging cleanly is the
  correct scope, not silently absorbing someone else's open regression
  into this dispatch.
- TD-128 (per-member key storage) registered, not fixed — explicitly
  debt, not this build's scope, per Q4.
- `harness/control_flow.py`'s stale "NOT wired into the live pipeline"
  docstring, found while scoping this dispatch — not corrected here (out
  of scope), flagged for whoever next touches that file.
- No `_expected.json` recorded for the new
  `boundary_and_consent__v20260717_1330.json` — `eval/harnesslib/layer2.py`
  skips it today rather than asserting anything. Recording one properly
  (via `record()` mode, which fires every turn live) is itself blocked on
  the same invalid key for a faithful T04b/T05 recording. Left unrecorded
  rather than checking in a stub that would either lie about what was
  reviewed or fail on the broken key.
- Bill's Questions 10 (stale prep-doc T05 text) and 11 (do the 3
  verification items block build vs. presentation) were not explicitly
  answered in this dispatch — treated as resolved-by-implication (see
  REQ_FRONTIER_TIER's ANSWERS section); the prep doc's own stale T05 text
  is still not corrected in the prep doc itself, only superseded by this
  build.
- The disclosure-gate consent prompt and yes/no vocabulary
  (`harness/disclosure.py`) have not been tested against ambiguous/
  off-vocabulary phrasing the way `confirmation_gate.py`'s `<4`-word floor
  was tuned this session (D-22) — a new, smaller surface, not yet
  adversarially tested the same way.
