# REQ_RETRIEVAL_OUTCOME_INSTRUMENTATION
Status: MET
MET-Ruling: Bill, 2026-07-28 (D-01 dispatch) -- all 7 acceptance items hold
Reconciled-Against: roadmap acda98b (2026-07-28); this UPDATE (build +
assessment), commit pending Bill's review of the staged diff

## THE REQUIREMENT

Bill's own words, verbatim, from the dispatch that opened this REQ:

> Write the REQ FIRST: REQ_RETRIEVAL_OUTCOME_INSTRUMENTATION per Stage 0 of
> docs/research-technical/HIP_CuratorResearch__*_v20260728_1045.md §7.5 —
> outcome fields (correction/override/accepted-answer) on the epistemic
> record keyed to injected_fact_ids and prompt_fact_ids; log rule-based
> ranking order per turn; retrieval-failure metric (D-24/T02-class rate) +
> candidates-per-attribute-family measurement. Register it. Commit.
>
> Build to the REQ. Measurement only — no learner, no ranking change,
> prompt untouched.
>
> Run --layer 7 via scripts/run_harness.sh. RATCHET must stay green.
>
> Assess vs the REQ's acceptance. Mark assessment, not MET.

Which itself points to `HIP_CuratorResearch__learned-retrieval-training-federation__v20260728_1045.md`
§7.5, quoted in full because it is the actual source of the four
deliverables above:

> **Stage 0 — instrument, measure, don't learn (now; no gate required).**
> Extend the epistemic record with outcome fields: per-turn
> correction/override/accepted-answer events, keyed to `injected_fact_ids`
> and `prompt_fact_ids` already logged. Log the rule-based ranking order
> each turn (deterministic logging is fine — no IPS planned, per Part 2).
> Add the retrieval-failure metric: rate of D-24/T02-class events
> (authorized, true, resolved fact not surfaced) and the
> candidates-per-attribute-family measurement from 7.2. **This stage
> produces the number the DISPATCH 38a entry gate needs** — "a measured
> retrieval failure justifies the cost" is currently unmeasurable.

Expanded: this REQ builds exactly the four Stage 0 deliverables above and
nothing past them. Stage 1 (`REQ_LEARNER_SIGNAL_ISOLATION`'s standing
gate), Stage 2 (shadow Curator), and everything past it are explicitly out
of scope — no learner, no ranker, no scoring model, no change to what gets
retrieved, ranked, or sent to any model. This REQ only makes existing,
already-happening decisions visible and measurable.

## THE ACCEPTANCE TEST

Pass/fail, no judgment calls.

**1. Outcome fields on the epistemic record.**
`build_epistemic_record()` gains one new optional field, `outcome`:
`{"kind": "correction" | "override" | None, "target_fact_ids": [...],
"target_turn_ids": [...]}`, populated by a new pure function,
`classify_outcome()`, called from the real write path (not a dead
function only unit tests exercise). Definitions, each tied to an existing,
already-logged signal — no new user-facing behavior invented to detect
them:
  - `correction`: this turn's `delta` contains a write with
    `write_state == "supersede"` whose superseded `fact_id` appears in
    `injected_fact_ids` or `prompt_fact_ids` of a recent prior turn
    (same `member`, lookback window stated in WHAT'S ALREADY DONE) — the
    member was shown a fact and then said something that overwrote it.
  - `override`: this turn's `path == "control_decline"` — the member was
    offered a system-proposed write via the confirmation gate and
    explicitly declined it. This path already exists in the epistemic
    record's path enum; this REQ does not add a new path, only surfaces
    the existing one as an outcome kind.
  - Observable: construct a turn sequence (fixture, not live graph) where
    turn N admits fact F, turn N+1 supersedes F. PASS: turn N+1's record
    has `outcome.kind == "correction"`, `F` in `target_fact_ids`. FAIL:
    `outcome` is null or does not name `F`.
  - Observable: construct a turn on the `control_decline` path. PASS:
    that turn's record has `outcome.kind == "override"`. FAIL: `outcome`
    is null.
  - Observable: a turn matching neither pattern. PASS: `outcome` is
    `{"kind": None, "target_fact_ids": [], "target_turn_ids": []}`, not
    absent — the field always exists so downstream scans never have to
    special-case its absence.

**2. `accepted-answer` is a derived measurement, not a per-turn field.**
Stated and justified, not silently assumed: `accepted-answer` cannot be
known at the time a turn's own record is built, because it is the
*absence* of a future correction or override — it can only be computed by
scanning forward from a turn to the member's subsequent turns. Built as
`accepted_answer_rate(records, lookahead=N)` in the new measurement
module (item 4 below): the fraction of turns with non-empty
`injected_fact_ids` that are NOT the target of a later `correction` or
`override` outcome within `lookahead` subsequent same-member turns.
Observable: a synthetic three-turn sequence (admit, no correction ever)
scores 1.0; a synthetic sequence (admit, then correction within the
window) scores 0.0 for that turn. PASS: both numbers match. FAIL: either
does not.

**3. Rule-based ranking order is already logged — verified, not rebuilt.**
Live-verified end-to-end, not asserted from reading code alone:
`harness/extraction_queue.py:read_user_facts()`'s Cypher query carries
`ORDER BY f.timestamp DESC` (ground truth: most-recent-first); nothing
downstream re-sorts — `harness/injection_contract.py`'s allow/deny loop
(`for fact in facts:`) is order-preserving, and `injected_fact_ids`/
`prompt_fact_ids` are built as plain ordered lists from that loop's
output, never a set or dict-keyed structure that could scramble it.
Observable: call `read_user_facts()` against a fixture with facts at
three distinct timestamps, run the returned list through
`evaluate_injection_contract()`, confirm `result.injected_fact_ids`
preserves the same most-recent-first order the query returned. PASS:
order identical. FAIL: order differs anywhere in the chain. No new field
is added for this item — the deliverable is the live proof plus a doc
comment at the point of logging naming `injected_fact_ids`' order as the
ranking-order record, so a future reader does not have to re-derive this
finding.

**4. Retrieval-failure metric (D-24/T02-class rate).**
New function `retrieval_failure_rate(records)` in
`eval/harnesslib/retrieval_outcome.py`, computing the fraction of records
matching the D-24/T02 shape exactly as amended in
`REQ_CONFIDENCE_DISCIPLINE` (`docs/requirements/LATEST_REQ_CONFIDENCE_DISCIPLINE.md`
line ~330): `intent` in the personal-intent set, `resolved_subjects`
non-empty, `path == "guard_empty_set"`, `admitted == []` — an authorized,
resolved query that surfaced nothing. Observable: a fixture set of
records, some matching the shape, some not (varying each of the four
conditions independently). PASS: the function returns exactly the
fraction of records matching all four conditions, and a synthetic record
matching three of four conditions does not count. FAIL: any
near-miss record is counted, or a true match is missed.

**5. Candidates-per-attribute-family measurement.**
New function `candidates_per_family(records)` in the same module,
computing, per turn, the count of candidate facts (the pre-final-filter
set — `admitted[]` union `withheld[]`, i.e. everything the injection
contract evaluated for that turn, not just what it allowed) sharing the
same `(subject, attribute)` pair, and reporting the fraction of turns
where any `(subject, attribute)` group exceeds 3 — the exact threshold
named in Curator Research §7.2. This is grouping by the literal
`attribute` field, not `injection_contract.py`'s narrower
`_ATTRIBUTE_FAMILIES` (that mapping is query-relevance matching for
`medication`/`medication_status`, a different concept from candidate
density per attribute — stated explicitly so a future reader does not
conflate the two). Observable: a fixture turn with 4 candidate `allergy`
facts for one subject and 1 `schedule` fact. PASS: that turn counts
toward the >3 fraction; a turn with 3 or fewer per group does not. FAIL:
either miscounts.

**6. No behavior change.** `git diff` confirms zero changes to what any
turn retrieves, how it is ranked, or what reaches the prompt or the
model — every change is either a new field on a record already being
built, or a new, separately-invoked measurement module. `scripts/
run_harness.sh --layer 7` RATCHET stays green, no scenario regressed.

**7. Live-wired, not dead code.** `classify_outcome()` is called from a
real call site in the write path (named in WHAT'S ALREADY DONE once
found), not only from a test file — grepping the production call site
confirms this, per this project's standing "no unwired feature" practice.

## WHAT'S ALREADY DONE

- The epistemic record schema (`harness/epistemic_record.py`,
  `build_epistemic_record()`) already carries `injected_fact_ids`,
  `prompt_fact_ids`, `delta` (with `write_state`), `path`, `intent`,
  `resolved_subjects`, `admitted[]`, `withheld[]` — every field this REQ's
  outcome/metric functions read. Not rebuilt.
- The `control_decline` path already exists in the path enum
  (`epistemic_record.py`'s own docstring, "Path enum, the nine return
  paths") and is already set by the confirmation-gate flow. Not rebuilt —
  `override` detection reads it, does not create it.
- The D-24/T02 defect shape is already fully diagnosed in
  `docs/requirements/LATEST_REQ_CONFIDENCE_DISCIPLINE.md` (AMENDMENT,
  2026-07-21) and the specific instance is already fixed
  (`_ATTRIBUTE_FAMILIES` / RETRIEVAL-RELEVANCE rule,
  `harness/injection_contract.py:180-190,735-751`). This REQ does not
  touch that fix; it measures the ongoing rate of the same failure
  *shape* recurring for attribute pairs not yet covered by a declared
  family.
- `read_user_facts()`'s `ORDER BY f.timestamp DESC` and
  `injection_contract.py`'s order-preserving allow/deny loop already
  produce a deterministic, rule-based candidate order today. Not rebuilt
  — verified live per acceptance item 3.
- `logs/turns_demo.jsonl` + the HEL ledger (`harness/epistemic_ledger.py`)
  already durably persist every record this REQ's measurement functions
  scan. Not rebuilt.

## WHAT'S KNOWN BROKEN

- No field on the epistemic record today distinguishes "the member
  corrected a surfaced fact" from any other write — a `supersede` write
  looks identical whether or not the superseded fact was ever shown to
  anyone. This REQ closes that gap for the `correction` and `override`
  kinds specifically; it does not attempt to detect every conceivable
  outcome class (e.g., a verbal "yes that's right" with no write at all
  is not detectable from written state and is explicitly NOT attempted
  here — named as a real, honest gap, not solved by inventing a sentiment
  classifier).
- No existing scan computes the D-24/T02-class rate or the
  candidates-per-family fraction; both are currently invisible, exactly
  the gap Curator Research §7.5 names ("currently unmeasurable").
- This REQ does not wire a new `AUDIT:*` scenario into `eval/harness.py`.
  Curator Research's own words for Stage 0 are "no gate required" — this
  is instrumentation, not a governance check, and does not get the full
  `REQ_HARNESS_DISCIPLINE` four-part treatment (fault-injection twin
  wired into the harness roster, coverage entry, metamorphic wrapper) a
  gated check would need. It does get a live, callable self-test proving
  each function is not vacuous (acceptance items 1-5's own fixtures), just
  not a harness-roster entry. Naming this precisely so it is not read as
  an oversight: a future REQ can promote this to a wired AUDIT check if a
  standing gate on these numbers is ever wanted.

## CONSTRAINTS

- No learner, no ranker, no scoring model, no change to retrieval order,
  no change to what is admitted, ranked, or sent to any model or the
  prompt. This REQ is additive-only: new fields on records already being
  built, plus new, separately-invoked read-only measurement functions.
- `outcome` detection reads only fields already on prior records
  (`injected_fact_ids`, `prompt_fact_ids`, `path`) — it does not read
  fact values (TD-030: values never render outside the vault decrypt
  path), and does not persist anything beyond fact_ids/turn_ids already
  legitimate to log.
- No graph reset, no reseed, no `--full` for this REQ's own verification
  (`--layer 7` only, per the dispatch).
- RATCHET must stay green throughout — this is additive instrumentation;
  it must never cause an existing scenario to regress.
- Do not mark this REQ MET. Assess against the acceptance test above and
  report the result; Bill decides, per this project's standing practice.

## UPDATE 2026-07-28: BUILT, assessed against acceptance items 1-7

Built: `harness/outcome_classifier.py` (new — `classify_outcome()`,
`recent_records_for_member()`), `harness/epistemic_record.py` (new
`outcome` kwarg + field, additive only), `server/voice_orch.py` (new
classification call inside the existing single-choke-point
`emit_epistemic_record` wrapper, same pattern G0's own hook uses),
`eval/harnesslib/retrieval_outcome.py` (new — `retrieval_failure_rate()`,
`candidates_per_family()`, `accepted_answer_rate()`,
`retrieval_outcome_self_test()`). `git diff --stat`: 2 files modified
(38 insertions, 0 deletions — purely additive, nothing removed or
changed), 2 files created.

**Item 1 (outcome fields).** MET. `classify_outcome()` live-called
standalone (not just read from source) for all three shapes: a
`control_decline` path returns `{"kind": "override", ...}`; a
`supersede` delta targeting a fact shown in a recorded prior turn
returns `{"kind": "correction", "target_fact_ids": [...], ...}`; a
`supersede` targeting an unshown fact, and a turn with no delta at all,
both return the null shape — never absent. Then live-wired end to end:
`scripts/text_demo.py --member bill "what do you know about me?"` (a
real turn through the real `process_text_query` path, real graph, no
reset/reseed) produced a real record with `outcome:
{'kind': None, 'target_fact_ids': [], 'target_turn_ids': []}` present
and correctly shaped — not reasoned about, observed.

**Item 2 (accepted-answer is derived).** MET. `accepted_answer_rate()`
built and live self-tested: a 4-record fixture (member `bill` admits f1
never corrected, admits f2 later corrected by a `correction` outcome
targeting f2, plus an unrelated `elena` turn) scores exactly 2/3 —
matches the hand-computed expectation, not just "ran without error."

**Item 3 (ranking order already logged).** MET, live-verified against
the real graph, not just the fixture-scenario language the acceptance
test proposed: `read_user_facts()`'s `ORDER BY f.timestamp DESC`
confirmed by direct source read; then proven end-to-end with a real turn
(`"what do you know about me?"`, 6 admitted facts) by querying Neo4j
directly for each returned `fact_id`'s `f.timestamp` and confirming the
`injected_fact_ids` list order is exactly descending-timestamp order —
`True`, not assumed. No new field added, per the REQ's own design; a
doc-comment now names `injected_fact_ids`' order as the ranking-order
record (`harness/epistemic_record.py`'s schema docstring).

**Item 4 (retrieval-failure metric).** MET. `retrieval_failure_rate()`
live self-tested against a 5-record fixture: one exact D-24/T02-shape
match plus four near-misses (one per condition: wrong intent, no
resolved subject, wrong path, non-empty admitted) — scored exactly
1/5, confirming near-misses are not counted.

**Item 5 (candidates-per-family).** MET. `candidates_per_family()` live
self-tested: a fixture turn with 4 same-subject `allergy` candidates (+1
`schedule`) counts toward the >3 fraction; a 3-candidate turn and a
3-candidates-across-two-subjects turn do not — matches the exact
threshold and per-subject grouping the acceptance test specifies.

**Item 6 (no behavior change).** MET. `git diff --stat` confirms zero
deletions, zero modifications to existing logic — only new optional
kwargs/fields and new, separately-invoked modules. `scripts/
run_harness.sh --layer 7` (log: `/tmp/hip_harness_20260728_1525.log`):
`AUDIT: 8/8`, `L7: 25/25`, `L7V2: 27/28` (1 pre-existing opt-in skip),
`DISC/SCHEMA/VOICE` all green, `RATCHET PASS — no scenario regressed vs
baseline` — identical figures to this morning's pre-build run
(`/tmp/hip_harness_20260728_0514.log`), confirming no regression. The 24
`Traceback` lines in the new log were checked line-by-line: all 24
originate from `harness/extraction_queue.py:775` inside
`read_user_facts()`'s own documented, pre-existing decrypt-skip-on-
failure behavior ("a fact whose value won't decrypt is skipped (logged)
rather than aborting the whole read") — zero originate from any file
this REQ touched.

**Item 7 (live-wired, not dead code).** MET. `server/voice_orch.py`'s
`emit_epistemic_record` wrapper (the single choke point every
`process_text_query` exit path already passes through, per
`REQ_G0_OUTPUT_INVARIANT`'s own precedent) now calls
`classify_outcome()` on every turn — confirmed by the live `text_demo.py`
proof under item 1, not merely by reading the call site.

**All 7 acceptance items hold.** Known, named scope limits (not
failures): `override` outcomes carry no `target_fact_ids` (a declined
confirmation-gate offer isn't attributable to a specific prior fact),
so `accepted_answer_rate()` only detects non-acceptance via `correction`,
stated in that function's own docstring; `recent_records_for_member()`
reads the whole `turns_demo.jsonl` per turn (acceptable at prototype log
sizes, named as a scaling limit in the code comment at its call site,
not hidden); no `eval/harness.py` `AUDIT:*` roster entry was added, per
this REQ's own WHAT'S KNOWN BROKEN section — Curator Research's own words
for Stage 0 are "no gate required."

**Status: BUILT, not MET.** Reports readiness; Bill decides, per this
project's standing practice and this REQ's own CONSTRAINTS.
