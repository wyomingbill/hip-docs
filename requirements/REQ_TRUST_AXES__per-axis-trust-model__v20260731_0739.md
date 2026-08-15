# REQ_TRUST_AXES: Per-Axis Trust Model — Write Authority, Epistemic Strength, Ranker Relevance
Version: v20260731_0739
Status: SUPERSEDED
Branch: roadmap
Reconciled-Against: 4f8f472 (2026-07-31). Diagnosis code-verified in D-51 against
`memory_engine/trust.py:27-34`, `harness/curator_shadow.py:96-97,199`,
`memory_engine/store.py:274,462`, `harness/extraction_queue.py:563`, and
`docs/design/HIP_HouseholdSeeding_Roadmap__v20260730_1645.md:142-150`.

**SUPERSEDED 2026-07-31 (D-53) by
`REQ_TRUST_AXES__record-both-rank-neither__v20260731_0827.md`.** Bill ruled, after
external evaluation, AGAINST the epistemic-strength RANKING axis this version
specified. The successor replaces it with a two-signal RECORD (`subject_asserted` +
provenance-bearing `attestations`) that is never collapsed into a single verdict.

Two things in this version were wrong and are named rather than quietly dropped:
the ranking itself (the system must not adjudicate self-report against corroboration),
and — more seriously — the **motive-to-misreport attribute table** (adherence, alcohol,
income, cognitive decline), which was a **content-blindness violation** under D-50
Principle 6: it would have made the system the arbiter of which topics its household
underreports. This document is retained as history of why the successor is shaped the
way it is. NO CODE WAS EVER WRITTEN AGAINST IT.

**NO CODE WRITTEN AGAINST THIS REQ YET.** Filed REQ-first per CLAUDE.md
Requirements Discipline item 1, because D-52 dispatched the code change without a
governing REQ and item 8's gate applies. See "Why this REQ exists" below.

## Why this REQ exists (procedural note, stated plainly)

D-52 asked for three code changes (comment `TRUST_RANK` as the write-authority
axis; add an epistemic-strength axis; derive `_TRUST_ORDINAL`). A repo-wide search
found **zero REQ docs scoping `TRUST_RANK` or the trust-ladder ordering** —
`REQ_CONFIDENCE_DISCIPLINE__truth-track` names `trust.py` only in a code-trace
line, not as scope. CLAUDE.md item 8 makes an unnamed-REQ code change a refusal,
with one exception (the literal words "skip the REQ") that was not invoked.

This document is that missing REQ, written **before** any code, which is the
procedure item 1 requires — not a retroactive cover for work already done. Nothing
was built this pass.

## THE REQUIREMENT

Bill's ruling (D-52 dispatch, accepting the D-51 proposal), verbatim:

> "Bill ruled YES to the per-axis proposal from D-51. Implement the parts that are
> safe now:
>   a. KEEP memory_engine/trust.py TRUST_RANK unchanged — it is the WRITE-AUTHORITY
>      axis and DERIVED=0 is correct for it. Add a docstring/comment naming it as the
>      write-authority axis so a future reader doesn't "fix" it.
>   b. ADD a separate EPISTEMIC-STRENGTH axis: independent-source count + source-authority
>      class. Subject-confirmation is NOT uniformly strongest — it is weaker than
>      independent corroboration where the subject has motive to misreport or lacks
>      insight (the domain cases: adherence, alcohol, income, cognitive decline).
>      Encode this as its own function/table, clearly separate from TRUST_RANK.
>   c. DERIVE harness/curator_shadow.py _TRUST_ORDINAL from one of the two axes rather
>      than hand-maintaining it as a fourth drifting table. Fix the DERIVED-above-CONFIRMED
>      inconsistency by derivation, not by hand."

The governing principle, from D-51 and ruled YES: **one name ("trust") currently
covers three different semantic axes, and no declaration says which is which.** The
fix is not to pick a winner but to name the axes and make each ordering correct for
its own axis.

## THE ACCEPTANCE TEST

Observable, pass/fail. Each item must be demonstrable without reading a docstring
for reassurance.

1. **A1 (write authority) is byte-unchanged in behavior.** `TRUST_RANK`'s values are
   identical to `4f8f472`. A test asserts the exact dict, so a future "fix" of
   `DERIVED: 0` fails a check rather than silently changing P8 behavior. The three
   comparison sites (`store.py:274`, `store.py:462`, `extraction_queue.py:563`)
   produce identical verdicts on a fixture table before and after this REQ.
2. **A2 (epistemic strength) exists as its own callable, and is NOT a permutation of
   A1.** A test asserts at least one attribute/fact pair where A1 and A2 order two
   rungs *differently* — i.e. proves the two axes are genuinely distinct rather than
   the same ordering renamed.
3. **A2 is attribute-relative, demonstrated on the four named domain cases.** For
   `adherence`, `alcohol`, `income`, and a cognitive-decline attribute, a test
   asserts that N independent corroborations outrank subject-confirmation; and for a
   self-report-authoritative attribute (e.g. a stated preference), it asserts the
   reverse. A single global ordering fails this test by construction — that is the
   point of the test.
4. **A3 (`_TRUST_ORDINAL`) is derived, not hand-written.** A test asserts
   `_TRUST_ORDINAL` equals the value computed from its source axis for all five
   rungs, so drift between the table and the axis is a FAIL. The literal
   `DERIVED: 1.0 > CONFIRMED: 0.9` inversion is gone as a *consequence* of
   derivation, not by hand-editing the numbers.
5. **A3 is total over the rung vocabulary.** All five rungs (`DERIVED`, `CONFIRMED`,
   `CORROBORATED`, `ASSERTED`, `UNCONFIRMED`) resolve without hitting a default. A
   test asserts no rung falls through to the neutral `0.5` — the same defect class as
   the `critical` sensitivity miss D-41 confirmed.
6. **CORROBORATED's meaning is unchanged.** A test asserts
   `classify_trust_props` still returns `CORROBORATED` for exactly the
   reconciliation-hardening predicate (`confidence == "high"` and a `reconcile`
   harden transition) and for nothing else. Social attestation does NOT enter this
   REQ — see `REQ_ATTESTED`.
7. **`--layer 7` green, RATCHET PASS**, plus `--full` green before any MET is
   proposed. The shadow scorer (`REQ_CURATOR_SHADOW_SCORER`, MET at D-44) consumes
   `_TRUST_ORDINAL` at `curator_shadow.py:199`, so A3 changes a MET component's
   feature values: CS1 must stay green and the ratchet must not move.

## WHAT'S ALREADY DONE

- **The diagnosis, code-verified (D-51).** All three orderings extracted verbatim
  with file:line; `_TRUST_ORDINAL`'s values proven to be a one-to-one order-preserving
  map of the first-match-wins *evaluation* sequence documented at `trust.py:66-67`
  (`1.0, 0.9, 0.7, 0.4, 0.1` against `DERIVED → CONFIRMED → CORROBORATED → ASSERTED →
  UNCONFIRMED`) — i.e. a dispatch sequence mistaken for a magnitude.
- **`TRUST_RANK`'s purpose is already documented and defended** at `trust.py:15-19`:
  the P8 monotonicity ordering, with `DERIVED` at the bottom deliberately because "it
  is a provenance category, not a strength." Item (a) is a clarifying restatement, not
  a discovery.
- **The CORROBORATED reachability bug is confirmed** (D-51, exhaustive over 144 input
  combinations: 4 returns of `CORROBORATED`, zero with `confirmed_by` set). That is
  recorded here as context; it is NOT fixed by this REQ, because keeping
  reconciliation-hardening as the ratified meaning is the ruling.

## WHAT'S KNOWN BROKEN

- `_TRUST_ORDINAL` ranks `DERIVED` (1.0) above `CONFIRMED` (0.9), contradicting
  `trust.py:17-18`'s explicit statement that DERIVED is "a provenance category, not a
  strength." Live, in a MET component's feature space.
- No epistemic-strength axis exists at all. The seeding roadmap's Part 1 assumes one.
- **OPEN, needs Bill's input before A2 can be built:** item (b) is not yet specified
  tightly enough to write code from. Specifically: (i) what is the authoritative list
  of motive-to-misreport / low-insight attributes, and is it a hand-maintained table
  or derived from the existing sensitivity classification? (ii) what does the A2
  callable return — a scalar, a `(count, authority_class)` tuple, or a comparator?
  (iii) does A2 have any consumer this pass, or is it built ahead of its caller (as
  the isolation gate was)? Per Requirements Discipline item 4, these are asked rather
  than guessed.

## CONSTRAINTS (what must not regress)

- **P8 write-monotonicity is ratified and load-bearing.** `TRUST_RANK` must not change
  values. `DERIVED = 0` is correct for the write-authority axis and is not a bug.
- **`CORROBORATED` keeps its reconciliation-hardening meaning.** Two specs pin it
  (`DEMO_SPEC:46`, `D1_RECORD_SPEC:51`) and a demo fixture depends on the current rank
  relationship (`demo_scripts/test/park_and_confirm__v20260712_1023.json:45`).
  Reusing the name for social attestation would silently reclassify every already-logged
  fact.
- **`REQ_CURATOR_SHADOW_SCORER` is MET (D-44).** A3 changes its feature encoding.
  The MET rests on a green `--full` at 81da8b0; this REQ must not regress CS1, any
  ABSOLUTE check, or the ratchet. If it does, the honest move is a pullback, per the
  D-42 precedent — not a quiet re-baseline.
- **The three A1 comparison sites must keep identical verdicts.** Changing what
  `TRUST_RANK` means to any of them is a P8 behavior change, which is out of scope.
- No self-MET. MET is Bill's ruling.
