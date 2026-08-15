# DISPATCH_DIGEST_AND_HANDOFF_CURRENCY
Status: BUILT
Reconciled-Against: 2026-08-04 (D-153; parent `e41d3a8`)

**TYPE:** DELIVERABLE + STATE DOCUMENT (docs only; no code, no graph, no harness)

**REQ:** NONE — a deliverable update and a currency pass. Nothing built, nothing ruled.

## 1. THE DIGEST — and a correction to the dispatch's premise

**The digest was NOT three days stale, and it did not stop at 2026-08-01 part 2.** Its
newest section was **Week of 2026-08-03** (`v20260803_1602`, written at D-137), which
already carries the first of the four themes this dispatch names: resolution blindness and
REQ_STRUCTURAL_REFUSAL, the model-cooperation finding and what establishing its width cost.
Verified by reading the file, not the dispatch's description of it.

The real gap was **2026-08-03 evening → 2026-08-04**, which is where the other three themes
live. So the new section covers those and does not re-narrate the structural-refusal story —
re-telling it would have produced two accounts of one event in a cumulative document, the
drift the digest's newest-week-on-top format exists to avoid.

New: `HIP_DesignDigest__weekly__v20260804_0639.md`, cumulative (every prior week retained
byte-for-byte, verified), LATEST repointed. **Week of 2026-08-04 — three requirements ruled
not met, and what a lock has to be to count:**

- **Silent absorption as a failure mode distinct from unbuildable.** Four representation
  classes the classifier cannot produce are not refused but ABSORBED — three stamped
  `HEALTH_CLAIM`, the fourth SCATTERED across whichever class the attribute yields, because
  the one signal that would identify it is never consulted. An unbuilt control reads as an
  absence; an absorbed one presents as a stamped, apparently-governed fact.
- **A requirement can be enforced and still not be met.** R2's permit is enforced at the
  single materialization point and was ruled NOT MET on a scope gap. R5 was found to hold
  **vacuously, by absence, unmonitored** — with the generalisation that "no code does X" is
  a finding with a shelf life, true until the first commit nobody checked against it.
- **What a lock must be to count as one:** kernel refusal rather than convention; keyed on
  the RESOURCE not the checkout (a per-checkout marker names neither contended thing);
  acquisition a precondition of the tooling rather than a step, because both late-takes were
  committed by sessions that knew the rule and did the work first anyway.
- **A board that reports a claim and then checks it** — an empty parse must fail rather than
  render a clean page, UNDETERMINED is a counted outcome, and the LIVE cross-check exposed a
  **visibility** gap that looks identical to a coverage gap in a skim.
- **One root cause behind three memory-harness symptoms** — two independently-correct
  mechanisms interacting — with the methodological point that a red reproducing identically
  three times is not flaky, and "environmental" is a claim needing the same evidence as any
  other.

**Every hash cited was verified with `git log`, not recalled:** `bc56fc4` (D-140),
`3989ba2` (D-143), `317212a` (D-144), `93eb91e` (D-145), `23b26d1` and `6750593` (D-146
build and B3), `ca34ec4` (D-147), `50daa12` (D-148), `ca223d4` (D-149). Content sourced
from the dispatch docs themselves — R5's enumeration, R8's absorption table, the P8 log
line — not from this session's recollection of them.

**Document Governance Rule satisfied in this same commit:** MANIFEST header updated
(Last-updated + Updated-by, prior attribution preserved), Section B's CURRENT row repointed
to `v20260804_0639` with the prior CURRENT demoted to SUPERSEDED carrying its
content-retained note. **Section C checked: no WP section maps to the design digest, so
nothing is marked NEEDS-UPDATE — checked, not assumed.**

## 2. HANDOFF CURRENCY

`docs/HIP_HANDOFF.md`'s CURRENT STATE was stale in three separate ways and is now true:

- **HEAD said `c5c9202` (D-137)**; it is `e41d3a8` (D-151).
- **Last-landed said D-146 build**; the roadmap lane has since landed D-148, D-149, D-151
  and now D-153, each named with its verified hash.
- **Lane A was described as "mid-build on R2, reported not ruled"** — which has been
  overtaken twice: R2 was RULED NOT MET at D-143, and Lane A has since landed R8's
  classifier (D-140) and D-147.

A new line records the **ruling state as it now stands** (MET: R1, R12, R18, R29, R30; NOT
MET: R2, R8, R10) and points at the status board rather than restating it — the board is
generated from §16 on every run, and a second hand-maintained copy in this document is
precisely the drift this project has paid for repeatedly. The line is a pointer by design.

## PROCESS NOTES

- STANDARD PREAMBLE observed; lock read-first then noclobber **before any edit** (06:38:14),
  released after push. Own worktree `~/hip-roadmap-d153`, temp branch `d153/digest-currency`,
  pushed as `d153/digest-currency:roadmap`, worktree removed after.
- **Docs only.** No graph, no harness, no `.env.dev` — Lane A holds both and D-152 was live.
- Explicit pathspecs and a surgical INDEX stage; both lanes' rows verified present after the
  push.

## OPEN

- Nothing ruled. The digest records rulings made elsewhere; it makes none.
- D-152's landing (Lane A, live during this dispatch) is not reflected in the digest or the
  handoff — it had not landed when this was written. The next currency pass picks it up.
