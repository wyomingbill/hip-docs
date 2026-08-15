# HIP CLAIMS LEDGER

> **SUPERSEDED by v3 — `HIP_ClaimsLedger__v3-c14-and-restored-citations__v20260810_0812.md`
> (HA-26, 2026-08-10). Recorded reason: "Add C-14 (Bill's wording, 2026-08-10) and restore
> the six dropped evidence citations."** C-01..C-13 wording is byte-identical between v2 and
> v3. Retained unaltered below — a superseding version only means something if the
> superseded text stays readable.

Status: **SUPERSEDED (was: v2)** — original status line preserved verbatim:
"v2 — claim wording drafted by Claude, statuses RULED BY BILL 2026-08-07
and 2026-08-09 where marked; remaining statuses are draft assessment until the
status generator computes them from standing runs.
Governing rules (Bill's ruling, 2026-08-07): claims are append-only — reworded
only by a superseding version with Bill's recorded reason; only standing
evidence counts; once the generator lands, status is computed, never declared;
the timeline column is forecast only and can never influence a status or weaken
an acceptance; the public test-results page renders from the same computation
and may never state more than this ledger; hard cap 15 claims — adding one
retires or justifies; the claim-to-evidence map changes only by Bill's ruling
and gets a periodic external sufficiency audit.

| # | Claim | Status | Evidence | Timeline |
|---|---|---|---|---|
| C-01 | A member's private facts are sealed to that member's key; a wrong key cannot read them. | PROVEN (draft) | Decrypt census 11/11 (HA-19), InvalidToken fault twins, standing battery | now |
| C-02 | Every fact has one coherent custodian: the key that sealed it is the key that reads it, asserted at construction. | PROVEN — Bill 2026-08-07 | REQ_DERIVED_WRITE_CUSTODY MET; Guard A live; standing custody battery (29 tests) | now |
| C-03 | Every fact names an accountable author — an authenticated enrolled member; scope labels can never author, on any ingestion path. | PROVEN — Bill 2026-08-07 | AUTHOR VALIDITY clause; Guard B live at the pre-seal boundary; C7 negative twin; standing battery | now |
| C-04 | Protected information is withheld structurally, before any model sees it — refusal does not depend on model behavior. | PARTIAL (draft) | Structural-refusal guard rows; probe runs show named-refusal coverage incomplete | ruling needed on scope |
| C-05 | To an unauthorized requester, exists-but-withheld is indistinguishable from does-not-exist. | PARTIAL (draft) | Three-guard-kinds fixtures, state-3 display ruling; end-to-end display proof pending | Sep 2026 |
| C-06 | An offer, once presented for a situation, can never be re-presented or reworded — including across restart and replay. | PROVEN (draft) | Immutable instances (HA-06); durable spend machine with process-kill twin (HA-08) | now |
| C-07 | Offer text cannot drift from its approved effect; no generative surface exists in the offer path. | PROVEN — Bill 2026-08-09 | Re-render integrity (HA-06); import-closure check live, fault twin proven (HA-22). Note: REQ_OFFER_MECHANISM stays NOT MET until A1-A20 run — separate from this claim. | now |
| C-08 | Erasure destroys every key copy HIP manages; HIP can no longer decrypt the subject's sealed data. | PARTIAL (draft) | Two-step flow built; custody consolidation gated; not enabled on real data | gated: custody consolidation |
| C-09 | Erasure leaves no readable trace that the claim existed — semantic metadata scrubbed, only an opaque proof retained. | UNPROVEN (draft) | Ruled (banked ruling doc); cascade not built | pre-first-household |
| C-10 | Key material is never captured by backups, and test keys cannot contaminate production custody. | PROVEN — Bill 2026-08-09 | 16/16 directory exclusions (HA-13); teardown wired, zero-orphan check relocated post-suite and proven both ways, two back-to-back clean --full runs (HA-20) | now |
| C-11 | The full end-to-end suite passes with no masked or falsely-refused checks. | PARTIAL — Bill 2026-08-09 | --full repeatable, binding layers green both runs (HA-20); live-model layers have no reproducibility rule yet, per Bill's item-12 amendment | after live-layer rule is set from collected run data |
| C-12 | Every requirement ruling rests on executed evidence, and every status is machine-derivable from the documents. | PROVEN (draft) | Ceiling 11 MET / 0 NOT MET on executed evidence; status board derives and cross-checks | now |
| C-13 | The household graph has a single writer with fail-closed targeting; no unowned instance is reachable by default. | PROVEN (draft) | Kernel lock + no-default targeting, executed twins both axes | now |

END OF LEDGER v2
