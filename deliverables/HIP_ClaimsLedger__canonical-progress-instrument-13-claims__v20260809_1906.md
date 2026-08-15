# HIP CLAIMS LEDGER

> **SUPERSEDED by v2 — `HIP_ClaimsLedger__v2-bills-ruled-statuses__v20260810_0549.md`
> (HA-23, 2026-08-10). Recorded reason: "Bill's status rulings, 2026-08-07 and
> 2026-08-09."** Five statuses changed: C-02, C-03, C-07, C-10 → PROVEN; C-11 → PARTIAL.
> **Claim wording is byte-identical between the two versions.** This file is retained
> unaltered below as the ledger's first version — the governing rules make a reword a
> superseding version, not an edit, and that only means anything if the superseded text
> stays readable.

Status: **SUPERSEDED (was: v1 DRAFT)** — original status line preserved verbatim:
"v1 DRAFT — claim wording awaits Bill's ruling; statuses are Claude's
draft assessment until the status generator computes them from standing runs."
Governing rules (Bill's ruling, 2026-08-07): claims are append-only — reworded
only by superseding version with Bill's recorded reason; only standing evidence
counts; status is computed, never declared, once the generator lands; the
timeline column is forecast only and can never influence a status or weaken an
acceptance; the public test-results page renders from the same computation and
may never exceed this ledger; hard cap 15 claims — adding one retires or
justifies; the claim-to-evidence map changes only by Bill's ruling and gets a
periodic external sufficiency audit.

| # | Claim | Status (draft) | Evidence | Timeline |
|---|---|---|---|---|
| C-01 | A member's private facts are sealed to that member's key; a wrong key cannot read them. | PROVEN | Decrypt census (HA-09/HA-14/HA-18), InvalidToken fault twins, standing battery | now |
| C-02 | Every fact has one coherent custodian: the key that sealed it is the key that reads it, asserted at construction. | PARTIAL | Guards proven both directions (HA-18); enablement = HA-19 | Aug 2026 |
| C-03 | Every fact names an accountable author — an authenticated enrolled member; scope labels can never author, on any ingestion path. | PARTIAL | REQ §1A + C7; Guard B proven (HA-18); enablement = HA-19 | Aug 2026 |
| C-04 | Protected information is withheld structurally, before any model sees it — refusal does not depend on model behavior. | PARTIAL | REQ_STRUCTURAL_REFUSAL guard rows; probe runs show named-refusal coverage incomplete | ruling needed on scope |
| C-05 | To an unauthorized requester, exists-but-withheld is indistinguishable from does-not-exist. | PARTIAL | Three-guard-kinds fixtures, state-3 display ruling (HA-04/HA-05); end-to-end display proof pending | Sep 2026 |
| C-06 | An offer, once presented for a situation, can never be re-presented or reworded — including across restart and replay. | PROVEN | Immutable instances (HA-06), durable spend machine with process-kill twin (HA-08) | now |
| C-07 | Offer text cannot drift from its approved effect; no generative surface exists in the offer path. | PARTIAL | Re-render integrity proven (HA-06); step 4 (strip generative interfaces) not started | Sep 2026 |
| C-08 | Erasure destroys every key copy HIP manages; HIP can no longer decrypt the subject's sealed data. | PARTIAL | Two-step flow built (D-R-194); custody consolidation gated; not enabled on real data | gated: custody consolidation |
| C-09 | Erasure leaves no readable trace that the claim existed — semantic metadata scrubbed, only an opaque proof retained. | UNPROVEN | Ruled (banked ruling doc); cascade not built | pre-first-household |
| C-10 | Key material is never captured by backups, and test keys cannot contaminate production custody. | PARTIAL | 16/16 directory exclusions (HA-13); teardown mechanism (HA-14); zero-orphan invariant relocation pending | Aug 2026 (HA-20) |
| C-11 | The full end-to-end suite passes with no masked or falsely-refused checks. | UNPROVEN | Guard metric fixed (TD-R-166); blocker root-caused; expected at HA-19 | Aug 2026 |
| C-12 | Every requirement ruling rests on executed evidence, and every status is machine-derivable from the documents. | PROVEN | Ceiling 11 MET / 0 NOT MET on executed evidence; status board derives and cross-checks | now |
| C-13 | The household graph has a single writer with fail-closed targeting; no unowned instance is reachable by default. | PROVEN | Kernel lock + no-default targeting (D-146), executed twins both axes | now |

END OF LEDGER v1
