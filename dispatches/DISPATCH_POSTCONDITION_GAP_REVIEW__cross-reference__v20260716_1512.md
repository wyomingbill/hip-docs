# DISPATCH_POSTCONDITION_GAP_REVIEW
Status: BUILT
Reconciled-Against: working tree at 420eb8a + uncommitted D-05 template edits, 2026-07-16 (matches the reviewed doc's own header)

**TYPE:** ANALYSIS

**REQ:** NONE. This was a review of another session's analysis draft, not a
build. No requirements doc governs it — analysis dispatches routinely have
none (CLAUDE.md item 10).

**This dispatch does not duplicate its own content.** The full analysis is
already on file at
`docs/research-technical/ANALYSIS__postcondition-gap-review__v20260716_1512.md`
(BUILT, 311 lines, by "Fable"). This doc is the register entry pointing at
it, per Bill's explicit instruction: "cross-reference, do not duplicate."

## THE ASK

**UNSOURCED.** The dispatch that requested this review was issued to a
different session (the reviewed document's own byline attributes it to
"Fable," reviewing a draft by a "Sonnet" session — `HIP_Theory__postcondition-
gap__v20260716_1500.md`, per the reviewed doc's title and the risk memo's
citation of it). This session has no transcript or record of that original
dispatch's exact wording. Rather than reconstruct a plausible-sounding ask
from the resulting document's content — which is exactly the kind of
back-filled invention this dispatch-register exists to prevent — this field
is left genuinely UNSOURCED. If the original dispatch text exists somewhere
(chat export, other session's log), it should be added here verbatim; until
then, this is honestly incomplete rather than falsely complete.

## WHAT WAS DONE

Per the reviewed document's own structure (summarized, not restated — read
the source for the actual argument):
- Reviewed a draft risk memo (`HIP_Theory__postcondition-gap__v20260716_1500.md`,
  by a prior session) against the live codebase.
- Verified its core claim against file:line evidence (no runtime output
  gate exists).
- Corrected the draft's framing on which invariant is load-bearing (G1 vs
  G0) and on question-keyed vs outcome-state-keyed gate design.
- Re-sequenced the risk memo's fix ordering.
- Traced a provenance gap the draft had flagged (a cited prior risk memo
  reported "NOT FOUND in repo") and resolved it.

## WHAT WAS FOUND

Not restated here — see the source document in full, especially:
- §2: the corrected frame (G1 is a precondition check wearing a postcondition
  gate's clothes; the check that actually matters, G0, exists nowhere).
- §5.1: the provenance-flag resolution (prior risk memo location).
- Its own ordering recommendation, which
  `HIP_SIA_PhaseB__risk-memo__v20260716_1624.md` §9 explicitly adopted
  (per that memo's own "AMENDMENT PROVENANCE" section and commit `792889f`).

This dispatch's OWN contribution beyond pointing at the source: confirming,
in this session, that the review's ordering did in fact propagate — item 0
of the risk memo's §9 (the F3 gate widening + detect retry) shipped at
`c86a414`, and item 0's second half (D-03/D-18, the confirmation gate) at
`3c0cb74` — both directly downstream of this review's re-sequencing.

## VERIFIED

**Watched run:** nothing — this entry is a cross-reference and provenance
check, not a fresh measurement or a live turn.

**Reasoned about:** the review document's own status header (`BUILT`,
reconciled against `420eb8a` + uncommitted D-05 edits) and its citation
chain (draft it reviews, risk memo that adopted it, commits that
subsequently shipped from that ordering) were read and cross-checked
against `docs/INDEX.md` and git log for consistency. No claim in the
reviewed document itself was independently re-verified by this dispatch —
that verification, if any, is recorded in the source document.

## HASH

NONE. Documentation-only cross-reference; no code changed by this dispatch.
(The underlying review itself predates this entry and shipped as
`docs/research-technical/ANALYSIS__postcondition-gap-review__v20260716_1512.md`,
already registered in `docs/INDEX.md`.)

## OPEN

- THE ASK is UNSOURCED, as stated above. If recovered, this doc should be
  updated in place (it is a register entry, not a versioned finding) or a
  superseding version filed.
- This entry does not itself re-verify the reviewed document's claims — it
  only confirms the provenance chain and that the ordering it recommended
  was later adopted and shipped. A skeptical read of the underlying
  analysis itself should go to the source document, not this one.
