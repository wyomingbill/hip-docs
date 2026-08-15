# REQ_BASELINE_RECORD_INTEGRITY — the updater preserves accepted-red justifications
Status: NOT MET
Reconciled-Against: roadmap 32cb04f (TD-150 filed at D-128; both incidents in this
session's history: D-126 at 1591477, D-127 at 829464f)
Filed: 2026-08-03 (D-129, Bill's ruling d)
Decision-Owner: Bill
Related: TD-150 (the scoped debt this governs), REQ_HARNESS_RUNNER (the runner this tool
lives beside), D-17 (the sanctioned accept path whose records this protects)

## THE REQUIREMENT

Bill's ruling, 2026-08-03 (D-129 d), verbatim:

> A tool that silently rewrites accepted-red justifications is a record-integrity hazard,
> and two incidents in two days both caught only by a human reading a diff is not a rate
> anyone should rely on.

The requirement: `eval/harness.py --update-baseline` SHALL NOT modify or drop any
`_accepted` justification except for a row that flipped to passing in the very run being
recorded — and never silently. The justifications are governance records carrying defect
IDs and Bill's rulings; the tool treats them as derived state today, and that inversion is
the defect.

## THE TWO INCIDENTS (the evidence, from the record)

1. **D-126** (`--update-baseline --accept "<text>"`): the ONE accept text was applied to
   EVERY currently-red row, overwriting TD-143's, TD-144's, and L1:P2's recorded
   justifications with an unrelated sentence. Caught in manual diff review; restored
   byte-identical from HEAD before commit.
2. **D-127** (plain `--update-baseline`, layer-4 scope): the ENTIRE `_accepted` map was
   dropped — including L1:P2's still-live justification for a still-red row that did not
   even run in that invocation. Caught in manual diff review; restored by hand.

## THE ACCEPTANCE TEST (from TD-150's five-way scope, fixed at filing)

1. **Per-row accept targeting**: `--accept-row <ROW_ID> "<text>"`; the global `--accept`
   REFUSES (does not guess) when more than one row is newly red.
2. **Preserve-by-default**: an `_accepted` entry is never modified or dropped unless its
   row flipped to passing IN THIS RUN; retiring one prints the retired text to the run
   output.
3. **Still-red refusal**: dropping a justification whose row is still `false` in the
   baseline — or whose row did not run in this invocation's scope — is refused, loudly
   (the L1:P2 shape, twice).
4. **Write-time diff**: every baseline write prints an `_accepted` before/after diff to
   the run output, so review does not depend on someone reading `git diff`.
5. **Round-trip stability battery**: a standing case asserting that an update with no row
   changes leaves `_accepted` byte-identical, plus fault twins for incidents (1) and (2)
   reproducing each against a fixture baseline and asserting the refusal.

## CONSTRAINTS

- The sanctioned accept path's SEMANTICS (D-17: known-red with ID, visible not buried) are
  the thing being protected — no change to what acceptance means, only to what the tool may
  touch.
- The fix must not require hand-editing JSON as the normal flow (that is today's
  workaround, not a design).
- Full RATCHET green per item 12 when built.

## STATUS

**NOT MET. Filed per Bill's D-129 ruling (d); not built; not self-ruled.** The build does
not start until an executing dispatch names this REQ (CLAUDE.md item 8).
