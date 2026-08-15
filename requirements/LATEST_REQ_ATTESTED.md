# REQ_ATTESTED: Social Multi-Party Attestation — a New Rung, and the Schema Change It Requires
Version: v20260731_0739
Status: DESIGN-DRAFT
Branch: roadmap
Reconciled-Against: 4f8f472 (2026-07-31). Code-verified in D-51 against
`memory_engine/trust.py:27-34,70-78`, `harness/extraction_queue.py:546-563`,
and `docs/design/HIP_HouseholdSeeding_Roadmap__v20260730_1645.md:142-150`.

**NOT BUILT. NOT AUTHORIZED FOR BUILD.** DESIGN-DRAFT, dependent on the
attributed-claim model (D-50). Filed per the D-52 dispatch so the schema cost is on
the record before anyone tries to implement the seeding roadmap's Part 1 as written.

## THE REQUIREMENT

Bill's ruling (D-52 dispatch), verbatim:

> "FILE a NEW REQ for ATTESTED (social multi-party attestation) as a SCHEMA CHANGE,
> NOT built this pass: confirmed_by must become a SET (not a scalar), and each
> attestation must carry PROVENANCE so the system can answer 'could B have heard this
> from A?' — household members are the least-independent attesters, so without
> provenance the rung overcounts agreement in exactly the case it's for. Mark it
> DESIGN-DRAFT, dependent on the attributed-claim model (D-50). Register in INDEX."

And the ruling this REQ implements from D-51, which it must not silently reverse:
**`CORROBORATED` keeps its ratified reconciliation-hardening meaning. Social
attestation gets a NEW rung name (`ATTESTED`). The name is not reused.**

## Why a new rung rather than reusing CORROBORATED

The seeding roadmap (`HIP_HouseholdSeeding_Roadmap:142-150`) proposes that a second
household member independently affirming a fact promotes it `CONFIRMED → CORROBORATED`,
and asserts "This roadmap does not change what `CORROBORATED` means." D-51 verified
that claim is false three ways:

1. **The existing meaning is reconciliation-hardening, not social agreement.**
   `trust.py:73` requires `confidence == "high"` plus a `confidence_log` entry with
   `source == "reconcile"` and `to > from` — an internal consolidation event
   (`memory_engine/consolidate.py:96-100`). No second person appears anywhere in it.
2. **The proposed direction is a demotion** under the ratified write-authority axis:
   `CONFIRMED` (3) → `CORROBORATED` (2) in `TRUST_RANK`.
3. **The transition is unreachable.** `classify_trust_props` is first-match-wins and
   `confirmed_by is not None → CONFIRMED` is evaluated *before* the CORROBORATED
   branch. Exhaustive check over all 144 input combinations: `CORROBORATED` returned
   4 times, **zero with `confirmed_by` set**. Since being at CONFIRMED *is* having
   `confirmed_by` set, the promotion cannot fire for any input.

Reusing the name would additionally reclassify every already-logged fact and
invalidate two specs that pin the current meaning (`DEMO_SPEC:46`,
`D1_RECORD_SPEC:51`) plus a demo fixture (`demo_scripts/test/
park_and_confirm__v20260712_1023.json:45`).

## The two costs, stated before anyone commits to building

### Cost 1 — `confirmed_by` is a scalar; N attestations cannot be represented

`confirmed_by` is read as a single value throughout
(`harness/extraction_queue.py:550,558,794`; `trust.py`'s `confirmed_by: str | None`).
There is nowhere to put a second attester. `ATTESTED` is therefore a **schema
change** — a new multi-valued structure plus a migration for existing rows — not a
new branch in a classifier. The seeding roadmap does not name this cost anywhere.

### Cost 2 — household members are the least independent attesters available

This is the substantive design problem, and it is worse in this domain than in the
general case. Two members agreeing may be **one source counted twice**: they talk
constantly, and B may have learned the fact from A. A rung that counts raw agreement
will systematically overcount independence in exactly the setting it was built for
(the seeding interview's "People" zone, where members describe each other).

So each attestation must carry enough **provenance** to answer *"could B have heard
this from A?"* — at minimum: who attested, when, and what the system had already
disclosed to that attester before they did. Note the third element: the system itself
is a transmission channel. If HIP told B the fact and B then affirms it, that is not
independent attestation, it is an echo, and only the system's own disclosure log can
detect it.

## THE ACCEPTANCE TEST

Pass/fail, observable. **Not runnable until the schema change lands** — listed now so
the build is specified before it starts, per Requirements Discipline item 1.

1. **`ATTESTED` is a distinct rung.** `CORROBORATED` continues to return for exactly
   the reconciliation-hardening predicate and nothing else; a test asserts the two are
   never conflated and that no previously-logged fact changes rung under the new code.
2. **Multi-valued attestation round-trips.** A fact with three attesters stores and
   reads back all three with their provenance. A scalar-shaped write fails loudly
   rather than silently keeping the last writer.
3. **The echo case is caught — this is the load-bearing test.** Given: A asserts a
   fact; the system discloses it to B; B affirms it. The system must classify this as
   **one** independent source, not two. A test asserts the independence count does not
   increment. Without this test the rung is decorative.
4. **The hearsay case is caught.** B affirms a fact B could have learned from A
   out-of-band (shared household, prior turn in a shared conversation). The system
   must either not count it as independent or record the dependency explicitly. This
   case may be undecidable in general — if so, the honest outcome is a named
   uncertainty in the record, not a silent independence claim.
5. **Attestation cannot be self-issued.** A member attesting their own fact is
   subject-confirmation (`CONFIRMED`), not attestation. A test asserts the subject is
   excluded from their own attester set.
6. **No custodian bulk-attest.** Consistent with the seeding roadmap's own
   no-bulk-confirm ruling, a custodian cannot attest a dependent's facts en masse.
7. **`--full` green, RATCHET PASS**, and no rung reclassification of existing data,
   before any MET is proposed.

## WHAT'S ALREADY DONE

- Nothing built. The diagnosis (D-51) and the naming ruling (D-52) are the whole of
  the prior work.
- The distinction this REQ rests on — write-authority axis vs. epistemic-strength axis
  — is filed separately as `REQ_TRUST_AXES__per-axis-trust-model__v20260731_0739.md`.
  `ATTESTED` is an **epistemic-strength** concept and must not be added to
  `TRUST_RANK`, which is the write-authority axis.

## WHAT'S KNOWN BROKEN / OPEN

- **DEPENDENCY: the attributed-claim model (D-50) is not settled.** Attestation is a
  claim attributed to a person; if D-50's model lands differently, this REQ's
  provenance shape changes with it. Do not build ahead of it.
- **OPEN:** does an attestation decay? A member's affirmation from 18 months ago, on a
  fact that has since been superseded twice, is not obviously still evidence. No
  position taken here.
- **OPEN:** what happens on *disagreement* — B asserts the fact is false. The current
  ladder has no negative-evidence rung, and this REQ does not invent one. Named so it
  is not discovered mid-build.
- **OPEN:** does `ATTESTED` outrank `CONFIRMED` on the epistemic-strength axis, and
  for which attributes? Per `REQ_TRUST_AXES`, subject-confirmation is weaker than
  independent corroboration precisely where the subject has motive to misreport or
  lacks insight (adherence, alcohol, income, cognitive decline) — so the answer is
  plausibly attribute-relative rather than global. Bill's call, and it is the
  interesting question this rung exists to make askable.

## CONSTRAINTS (what must not regress)

- **`CORROBORATED` is not renamed, redefined, or repurposed.** Ratified meaning stands.
- **`TRUST_RANK` is not extended.** `ATTESTED` belongs on the epistemic-strength axis.
  Adding a rung to the write-authority ordering would change P8 park behavior.
- **No silent reclassification.** No fact already in the graph may change rung as a
  result of this build.
- **Attestation must never be inferable as a way to raise trust without a person.**
  The rung's whole value is that a human vouched; a system-derived path to `ATTESTED`
  would make it worthless and is out of scope by construction.
- No self-MET. MET is Bill's ruling.
