# REQ_D21_D23
Status: IN_PROGRESS — items 1/2/4 BUILT and live-verified; item 3 BLOCKED
(see dispatch); D-21's schema root cause fixed and triple-verified, but
`--full` does not cleanly pass (residual stochastic miss, not the original
defect) so this REQ is not being closed as fully done.
Reconciled-Against: 1bd4500 (parent state at time of drafting); HEAD moved
to 98c4b81 while this REQ was in progress (parallel REQ_FRONTIER_TIER,
which cites this REQ's own uncommitted D10/D11 finding — see dispatch's
CROSS-REFERENCE). This REQ's own changes remain uncommitted at time of
writing, see dispatch's HASH section.

Dispatch: `docs/dispatches/DISPATCH_D21_D23__enum-widened-seed-validated-d10d11-blocked__v20260717_1240.md` —
read it first; it has the acceptance-test-by-acceptance-test result,
including the two items this REQ does NOT close.

Parent findings: `docs/dispatches/DISPATCH_DETECTION_MISS_MEASUREMENT__d21-and-td125-numbers__v20260717_1117.md`
(D-21 measured: 20/20 deterministic miss) and
`docs/dispatches/DISPATCH_ENUM_AUDIT__seed-fixtures-outside-detector-schema__v20260717_1135.md`
(D-23: 5/11 seeded fixtures use an attribute outside `CANONICAL_ATTRIBUTES`).
This REQ authorizes the schema decision Bill made on top of those two
measurements — filed before code, per CLAUDE.md item 8.

## THE REQUIREMENT

Bill's words, verbatim:

> "Schema decision. Bill's call, four parts.
>
> 1. ADD `incident` and `medication_status` to CANONICAL_ATTRIBUTES
>    (harness/extraction_queue.py:124-136). "Dad had a fall last week" is the
>    eldercare event this product exists for and the detector cannot emit it.
>    D-21 closes when it lands.
>
> 2. SKIP `risk_pattern`. D8 is DERIVED — system-computed, not spoken. A
>    detector should not emit derived facts. Leave it outside the enum on
>    purpose and say so in the register.
>
> 3. FIX D10/D11 as a SEED BUG, not a schema gap. `household` already covers
>    address and zone_district — its own description names "address" as an
>    example. The seed just used different literal strings. Change the seed to
>    use `household`. Confirm script 1's frontier payload still builds from
>    D10/D11 after — that payload is code-built from fact rows and it must not
>    break.
>
> 4. VALIDATE THE SEED PATH AGAINST THE SAME ENUM. This is the one that
>    matters. demo_seed.py's _seed_one calls store.encode() with `attribute` as
>    an unvalidated free string. The enum is enforced only on the live Groq path
>    (fact_change.py:75). Two write paths, one constrained — that is what let 5
>    of 11 fixtures use attributes the detector cannot produce, and it can drift
>    again tomorrow with nobody noticing.
>
> REQ doc first. Dispatch doc per the register.
>
> PROVE IT LIVE:
>   a. sam: "Dad had a fall last week. He's okay but we're watching it."
>      -> lands. Verify in Neo4j: fact_id, attribute, write_state. Not reply text.
>      Run it 20 times. It missed 20/20 before — I want 20/20 landing now.
>   b. Your 24-utterance corpus -> still 24/24. No regression.
>   c. demo_seed with an attribute outside the enum -> REFUSED, loudly.
>   d. Script 1's frontier payload still builds from D10/D11.
>   e. --full passes. Per CLAUDE.md item 12, not just its own live proofs.
>
> D-21 should go green. If it does not, stop and report why.
>
> Push, report the hash."

**Expanded — one thing checked before writing any code, because it changes
what acceptance-test item (d) can mean:** "Script 1's frontier payload"
(`boundary_and_consent__v20260715_1158.json` T04) is **not built**. The
script's own `description` field says T04/T05 are "omitted (blocked on
PROPOSED DISCLOSURE pane, frontier tier, payload builder, return path, T05
disposition)," and `docs/demo_prep/HIP_DemoScript01_BoundaryAndConsent__prep__v20260715_1000.md`'s
own BUILD LIST opens with "Nothing here exists except the routing." A
repo-wide grep for `PROPOSED DISCLOSURE`, `payload_builder`, `outbound
payload`, `build_payload` returns no hits in `harness/` or `server/`. The
only two places D10/D11's attribute strings appear in code today are
`scripts/demo_seed.py` itself and `eval/oracle/disclosure_oracle.py`'s
`FIXTURE` dict (a transcribed copy used by `access()`/`relevant()`, which
key off `owner`/`subject`, never `attribute` — confirmed by reading both
functions). **There is no live payload-builder code path to "confirm still
builds."** Item (d) is satisfied by: (1) confirming no such code exists to
break, and (2) keeping `disclosure_oracle.py`'s transcribed copy in sync
with the corrected seed so the oracle doesn't silently disagree with reality.
If a live payload-builder existed, this would be a different, larger
acceptance test; it doesn't, so this is what "still builds" can honestly
mean today.

## THE ACCEPTANCE TEST

1. `harness/extraction_queue.py`'s `CANONICAL_ATTRIBUTES` gains `incident`
   and `medication_status` (13 values); `risk_pattern` is deliberately
   absent, with a comment saying why.
2. `scripts/demo_seed.py`'s D10/D11 fixtures use attribute `household`, not
   `address`/`zone_district`. `eval/oracle/disclosure_oracle.py`'s `FIXTURE`
   copy matches.
3. `scripts/demo_seed.py` refuses loudly (raises, does not seed) when a
   fixture's `attribute` is outside `CANONICAL_ATTRIBUTES`.
4. Live, watched, Neo4j-verified (not reply text):
   a. `sam`: "Dad had a fall last week. He's okay but we're watching it." —
      20/20 independent live turns land a fact with `attribute=incident`,
      `write_state` moves off `unresolved` to its expected trust state.
   b. The 24-utterance regression corpus from
      `DISPATCH_DETECTION_MISS_MEASUREMENT` still lands 24/24 — no
      regression from the enum widening.
   c. Seeding a fixture with an attribute outside the (now 13-value) enum
      is refused loudly (an exception, not a silent write).
   d. No live payload-builder code exists to break; `disclosure_oracle.py`'s
      copy is updated to match the corrected seed (see Expanded note above).
   e. `python -m eval.harness --full` passes, or if it doesn't, every
      failure is read and attributed — not just the targeted turns above,
      per CLAUDE.md item 12.
5. D-21 registered green in `HIP_DefectRegister`. If any of the above does
   not hold, this REQ says so and stops rather than asserting D-21 fixed.

## WHAT'S ALREADY DONE

- D-21 measured: `three_zone_demo.T02`'s utterance misses 20/20 at temp=0.0
  and 20/20 after the temp=0.2 retry (0% recovery) —
  `DISPATCH_DETECTION_MISS_MEASUREMENT__d21-and-td125-numbers__v20260717_1117.md`.
  This REQ does not re-measure that; it fixes the root cause the
  measurement pointed at and re-proves live.
- D-23 audit: 5/11 seeded fixtures (D4, D5, D8, D10, D11) use an attribute
  outside `CANONICAL_ATTRIBUTES` —
  `DISPATCH_ENUM_AUDIT__seed-fixtures-outside-detector-schema__v20260717_1135.md`.
  Read, not redone, per CLAUDE.md item 11.
- TD-123's citation as D-21's fix track is already corrected in both
  `DEBT_REGISTER` and `HIP_DefectRegister` as a different bug (subject-slot
  person-typing, not attribute-category coverage). This REQ does not touch
  TD-123 or its own remaining prompt-hardening work.
- D-03/D-18 (confirmation gate no-fallthrough), TD-121 F1/F3, D-05
  (park-query gate) — unrelated code paths, verified working, not to be
  redone or regressed by this change.
- The 24-utterance corpus and its read-only reproduction script already
  exist (`docs/dispatches/detection_miss_measurement_script__v20260717_1117.py`)
  and were checked before writing a new one, per CLAUDE.md item 11 — reused
  for acceptance-test item 4b rather than rebuilt, adapted only to call the
  live write path instead of `_call_groq` read-only (needed because this
  REQ must prove facts *land*, not just that the detector emits a
  `changes` list).

## WHAT'S KNOWN BROKEN (before this build)

- `CANONICAL_ATTRIBUTES` (11 values) has no category for a discrete event
  (`incident`) or a status-change-to-an-existing-medication-fact
  (`medication_status`). The Groq detector's structured-output schema
  enum-locks `attribute` to this list, so it is structurally unable to
  emit either value at any temperature.
- `scripts/demo_seed.py`'s `_seed_one` calls `memory_engine.store.encode()`
  directly with `attribute` as an unvalidated free string. No enum check
  exists on this path. This is *why* 5 fixtures could drift outside the
  detector's enum with nothing noticing — the seed path and the live-write
  path are two different mechanisms, only one of them constrained.
- A companion gap, found while scoping this REQ, not asked for by name but
  directly implied by "D-21 closes when it lands": `harness/injection_contract.py`'s
  `_ATTR_KEYWORDS` (INJ-2 relevance) has no entries for `incident` or
  `medication_status`. Per `_inj2_relevant`'s own logic
  (`_ATTR_KEYWORDS.get(attribute)` → `None` → deny), a fact written under
  either new attribute would be **write-legal but read-invisible** —  the
  exact defect class already found and fixed once for `appointment`
  (PW023-25/TD-120 D3, see the comment at that dict entry). Leaving this
  alone would make D-21 "land" but never be answerable to Sam asking about
  it later, which defeats the point of adding the category. This REQ closes
  it in the same change: two new `_ATTR_KEYWORDS` patterns, and both added
  to `_TARGETED_ATTRS` (INJ-6b) for the same fabrication-refusal coverage
  `medication`/`health_condition` already get.
- `docs/demo_prep/HIP_DemoScript01_BoundaryAndConsent__prep__v20260715_1000.md`'s
  T04 payload builder is unbuilt (see Expanded note above) — not a defect
  this REQ introduces or is responsible for closing, but material to
  reading acceptance-test item (d) honestly.

## CONSTRAINTS

- Do not add `risk_pattern` to the enum — Bill's explicit call, item 2. Say
  so in the register, not just in code.
- Do not touch TD-123's own remaining scope (subject-slot person-typing
  prompt hardening) — confirmed a different bug, out of scope here.
- Do not touch confirmation-gate code (D-03/D-18/D-19/D-20/D-22) — unrelated
  path, must not regress; `--full` (item 5) is the check that would catch
  a regression there.
- Do not re-seed D4/D5/D8 under a different attribute — Bill's decision is
  to widen the enum to fit D4/D5 as they are, and to leave D8 out on
  purpose. Only D10/D11's literal attribute strings change.
- `python -m eval.harness --full` is the gate per CLAUDE.md item 12 — a
  narrow set of targeted live proofs passing is necessary, not sufficient.
  If `--full` shows a NEW failure this change caused, stop and report it
  rather than shipping past it.
