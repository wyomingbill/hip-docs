# DISPATCH_ENUM_AUDIT
Status: BUILT
Reconciled-Against: 10b5304 (measurement/audit only, no code changed)

**TYPE:** MEASUREMENT

**REQ:** NONE. No code, no prompt, no fixture changed — a schema audit
against the existing enum. Per CLAUDE.md item 11, this continues
`DISPATCH_DETECTION_MISS_MEASUREMENT__d21-and-td125-numbers__v20260717_1117.md`
rather than re-deriving it; read that first for the underlying measurement.

## THE ASK

Bill's dispatch, verbatim:

> "Confirm your hypothesis before anything else. One check:
>
> grep -n -A15 "CANONICAL_ATTRIBUTES" harness/*.py | head -30
>
> If incident and medication_status are absent from the enum, then:
>   1. TD-123's framing is wrong — it is prompt hardening for a schema
>      problem. No prompt reaches an enum. Say so in the register.
>   2. D4 and D5 are seeded with attributes the detector CANNOT EMIT. The
>      fixture contains fact types the live system could never produce.
>      "Sam told HIP about Dad's fall" is not reproducible — check whether
>      any seeded fact has an attribute outside the enum, and list them.
>   3. That is a demo problem, not a detection problem. Anyone who says
>      "Dad had a fall" at the demo gets a refusal.
>
> Report the enum's 11 values and which seeded facts fall outside it. No
> fix."

## THE ENUM — 11 VALUES, `harness/extraction_queue.py:124-136`

```
medication, allergy, health_condition, dietary, preference, schedule,
appointment, employer, relationship, household, financial
```

Enforced at `harness/fact_change.py:75`:
`"attribute": {"type": "string", "enum": sorted(CANONICAL_ATTRIBUTES)}` —
inside `_CHANGES_SCHEMA`, the structured-output schema sent to Groq for
every live detection call. The model is STRUCTURALLY unable to emit an
`attribute` value outside this list; it is not a matter of prompt wording.

**Confirmed: `incident` and `medication_status` are both absent.**

## THE FULL AUDIT — EVERY SEEDED FIXTURE (`scripts/demo_seed.py:49-141`)

| Fixture | Attribute used | In the 11-value enum? |
|---|---|---|
| D1 | `appointment` | yes |
| D2 | `medication` | yes |
| D3 | `schedule` | yes |
| **D4** | **`incident`** | **NO** |
| **D5** | **`medication_status`** | **NO** |
| D6 | `preference` | yes |
| D7 | `household` | yes |
| **D8** | **`risk_pattern`** | **NO** |
| D9 | `medication` | yes |
| **D10** | **`address`** | **NO** |
| **D11** | **`zone_district`** | **NO** |

**5 of 11 seeded fixtures (45%) use an attribute string outside the
detector's enum.** Confirmed mechanically: `_seed_one`
(`scripts/demo_seed.py:187-218`) calls `memory_engine.store.encode()`
directly with `attribute` as a free-form string parameter — no enum
validation exists at the graph-write layer. The enum constraint is
enforced ONLY on the Groq structured-output path
(`detect_and_apply`/`_call_groq`), which real spoken/typed turns go
through and seeding does not. This is structurally why the fixture can
contain fact types the live system could never independently produce:
two different write paths, only one of them constrained.

**Not all five are the same failure shape — reported precisely, not
lumped:**

- **D4 (`incident`), D5 (`medication_status`), D8 (`risk_pattern`) — no
  matching enum category exists at all.** The closest available bucket
  for a fall or a medication-status change would be `health_condition`,
  and it is a stretch either way ("Diagnosed or reported health
  conditions" describes a standing condition, not a discrete event like a
  fall or a discontinuation). D8 is additionally seeded at `DERIVED` trust
  level — system-computed, not naturally something a person would say in
  first-person speech ("there's an elevated fall-risk pattern" is not a
  turn anyone speaks) — lower practical exposure than D4/D5, but
  structurally the same gap if anyone tried.
- **D10 (`address`), D11 (`zone_district`) — a different shape of
  mismatch.** `household`'s own enum description explicitly names
  "address" as an example it covers: `"Household-level facts (address,
  trash day, shared routines)"`. A live utterance like "We moved to a new
  address" would most likely be correctly classified by Groq as
  `household` — a valid, in-enum category. But the SEEDED fact is stored
  under the literal attribute `address`, not `household`. If the
  supersession/write logic keys off an exact `(owner, subject, attribute)`
  match (as TD-121's F1 fix and `_apply_changes` do elsewhere in this
  codebase), a live address update would land as a NEW, unrelated
  `household` fact rather than superseding the existing `address`-labeled
  seed row — a continuity/supersession bug, not a flat detection miss.
  This was NOT independently tested in this dispatch (no live utterance
  was run against D10/D11); flagged as a structural finding from the
  schema audit, not a measured reproduction like D4's.
- **D11 specifically** carries its own comment
  (`scripts/demo_seed.py:131-133`) marking it a placeholder tied to a
  specific script's outbound payload ("Script 01 T04"), not obviously
  something anyone would assert conversationally — lower practical
  exposure than D10, similar in kind.

## THE THREE CONCLUSIONS, PLAINLY

**1. TD-123's framing is wrong for D-21 — and more specifically wrong
than "prompt hardening can't reach a schema," it is likely the wrong
DEFECT entirely.** Re-reading TD-123's actual written text
(`docs/techdebt/DEBT_REGISTER__v20260712_2300.md`, TD-123 row): its
documented scope is Groq misfiling a fact's VALUE into the person-typed
SUBJECT slot ("subject=shellfish" for "I'm allergic to shellfish") — a
subject-typing bug, not an attribute-category bug. Its own "REMAINING"
line names one open task: subject-must-be-a-PERSON prompt hardening. That
has nothing to do with D4/D5/D8/D10/D11's missing-or-mismatched attribute
categories. Separately, `DIAG__p2-i019-detection-miss__v20260714_1500.md`
also cites "TD-123" as the fix track for i019's dietary/preference
disambiguation — a THIRD, different framing, also not about missing enum
categories, and not reflected in TD-123's own current register text
either. No prompt reaches an enum regardless of which of TD-123's two
citations is meant — the conclusion holds under either reading, but the
citation itself is unreliable and should not be used to route this work
without checking. **Corrected in the register: see below.**

**2. Listed above.** D4 and D5, plus D8/D10/D11 found by extending the
same check to every fixture, not just the two named in the ask.

**3. Confirmed as a demo/fixture problem, with the caveat on practical
reach stated per-fixture above.** D4 is the proven case (D-21, live
reproduction, 20/20). D5 is structurally identical and unobserved live —
someone saying "Dad's medication was stopped" or similar would plausibly
hit the same wall, not yet tested. D8/D10/D11 carry the same structural
gap with lower practical likelihood of ever being spoken as a live turn.

## VERIFIED

**Watched run:** the grep Bill specified, run exactly as given. The full
fixture list read directly from `scripts/demo_seed.py:49-141`, cross-
checked against the enum read directly from
`harness/extraction_queue.py:124-136`. The encode()-bypasses-the-enum
mechanism confirmed by reading `_seed_one`'s actual call
(`scripts/demo_seed.py:194-218`) — not inferred, the direct-write call
site is right there with `attribute` as a plain string argument, no
schema/enum in the call path.

**Reasoned about:** whether a live utterance for D10/D11 would actually
reproduce a failure was not tested (no Groq call was made for this
dispatch — this was a static code/fixture audit, not a repeat of the
previous dispatch's live measurement). The `household`-vs-`address`
supersession-bug claim follows from reading `_apply_changes`'s matching
logic elsewhere in this codebase, not from observing D10/D11 fail live.
D8's "lower practical exposure" is a judgment about natural speech
patterns, not a measurement.

## HASH

NONE — audit only, no code changed.

## OPEN

- D5, D8, D10, D11 are structural findings, not live-reproduced failures
  like D4/D-21. If confirmation matters before anyone acts on them, they
  would need the same live-measurement treatment D-21 got (extend the
  corpus from the parent dispatch, same read-only methodology).
- Whether to fix the schema (add an event/incident category), fix the
  fixture (re-seed D4/D5/D8/D10/D11 under enum-legal attributes), or
  accept the demo-scope limitation is not decided here — explicitly out
  of scope ("No fix").
- TD-123's own citation inconsistency (subject-typing vs. dietary/
  preference vs., now, neither of those being D-21's actual mechanism) is
  itself worth someone cleaning up independently of this defect — not
  attempted here.
