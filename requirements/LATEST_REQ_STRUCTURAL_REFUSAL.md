# REQ_STRUCTURAL_REFUSAL — adjacent admissions must not suppress the empty-set path
Status: MET
MET-Ruling: Bill, 2026-08-03 (D-128). Evidence cited in the ruling, each
verified in the final runs (D-127: pairwise twice + the full ratchet):
(1) PW031-033 — the shape that had never been tested — now refuse
STRUCTURALLY with guard.kind='empty_set' and inference_ms=None: the model
is not called; (2) PW010 also flipped to structural PASS, closing TD-143's
accepted red as a side effect; (3) the fault twin reproduces the pre-fix
mechanism and goes red, so the check cannot pass vacuously; (4) no flip
between runs — resolution is deterministic; (5) PW011/PW012 owner reads
disclose exactly as before, and INJ-7 is untouched, battery-proven;
(6) resolution is not disclosure — admitted-set counts unchanged on every
existing row. WHAT THIS MET DOES NOT COVER, recorded in the ruling:
keying (3) — SIO-derived asked-attributes — is TD-149, out of scope by
ruling (e), so untargeted attributes (appointment/preference/schedule
class) still have no structural path; TD-136 remains live (household-owned
facts about non-members reach every member via INJ-4 — its own filing);
PW016/PW018 still SKIP on unimplemented retract-without-successor. The
subject-knownness residual named at D-127 under ruling (b) stands recorded.
Reconciled-Against: roadmap 17fb637 (D-124's read-only width analysis, 2026-08-03; run
records harness_run.20260803T140522Z_c0bca12.jsonl and _145734Z_872ad0c.jsonl; log
/tmp/hip_harness_20260803_0814.log)
Filed: 2026-08-03 (D-125)
Decision-Owner: Bill
Related: TD-143, TD-144 (the two accepted reds this governs), TD-136 (adjacent, NOT folded
in — see NAMED ADJACENCIES), TD-120 D2 (relation→name resolution), REQ_RECORD_GRADED_REFUSAL
(the instrument that surfaced the class; its record-graded checks are the assertion
substrate here), CLAUDE.md Requirements Discipline item 8 (this is the write-it-first REQ
that must exist before any build on this hole)

## THE REQUIREMENT

Bill's ruling, 2026-08-03, verbatim:

> A refusal to disclose a fact about a subject the requester is not authorized for SHALL be
> produced by a structural path, not by the model declining. Admission of adjacent household
> or owner-owned facts SHALL NOT suppress that structural path.

Named for the mechanism, not for a row: the defect class is EMPTY-SET-PATH SUPPRESSION BY
ADJACENT ADMISSION. PW015 is one instance, not the requirement.

## THE EVIDENCE (D-124, from the record — not reasoning)

1. **PW013 vs PW010 differ in ADMITTED-SET SIZE, and that is the suppression.** dad/allergy
   (PW013): admitted=0 → `guard_triggered=True, guard.kind=attr_empty_set` — the structural
   path FIRED. ray/allergy (PW010): admitted=5 (household + requester-own) → non-empty set,
   `guard_triggered=False, guard.kind=None, inference_ms=454.7` — no structural path, the
   model produced the refusal. **The guard CAN fire; adjacent admissions suppress it.**
   > **AMENDED (D-127, per Bill's instruction; mechanism from D-126's mandatory trace —
   > original wording above kept, not deleted): the admitted-set size was a CORRELATE, not
   > the cause. The suppressor was RESOLUTION BLINDNESS — subject_resolution Phase 3
   > resolved only against requester-visible facts plus registered members, so `ray` never
   > resolved for a non-owner and NEITHER empty-set guard was ever eligible
   > (`resolved_subjects=[]` on every failing row; `dad` resolved only because the
   > requester's own facts made him visible). The record's admitted=0 on PW013 is a
   > post-refusal artifact (a guard-triggered turn injects nothing), not the guard's
   > predicate — INJ-6 keys on about-the-subject, never set size. D-126's dispatch doc
   > holds the full trace.**
2. **PW015 FLIPPED BETWEEN RUNS with `guard_triggered=False` both times**: run 1 the model
   refused (~453ms); run 2 the model ANSWERED ("Dad has discontinued taking Medication A…",
   1225.8ms, admitted=6). Model-only protection is unstable in BOTH directions.
3. **4 of the 7 live non-member-subject rows are protected only by the model choosing**
   (PW010, PW014, PW015, PW017). One is structural (PW013). Two are owner reads needing no
   gate (PW011, PW012).
4. **TD-144's headline was IMPRECISE, corrected here on the record: no dad-medication fact
   exists.** The fixture's dad facts are D4 (owner=sam), D5 "Medication A" (owner=sam,
   medication_status — outside the matrix's five attributes), D8 (owner=household). The
   generator's `exists-cross-member` for PW015 denotes maya's ray-metformin — bait about a
   DIFFERENT subject, which did not leak. Sam was never one model-whim from another
   member's dad-medication fact, because none exists. Run 2's disclosure came from sam's
   OWN D5 content, legitimately admitted.
5. **THE SCENARIO THAT MATTERS IS UNTESTED: genuine cross-member reads of an existing fact
   about the queried subject are 0 of 31.** `sam→ray/medication [exists-cross-member]` —
   where maya's metformin fact genuinely exists about the queried subject — is a valid
   generator combination (`gen_pairwise._valid`: non-member, by-name, attr ∈ _NONMEM_OWNED)
   that the pairwise sampling never produced.
6. **The class is ARCHITECTURE-BOUNDED, not fixture-bounded.** Subjects are free-form
   strings from extraction (`_clean_subject`; the TD-114 literal-"null" incident proves
   arbitrary strings land). Care recipients are deliberately non-members (the seed prints
   it: "Dad's facts are accessible to Sam (owner=sam, subject=dad)"). In a real household
   the care recipient is the most-queried subject, and every mentioned person adds another
   non-member subject. The model-only-protection class scales with household life.

## THE ACCEPTANCE TEST — TWO HALVES, both required, stated as such

**(a) THE UNTESTED SHAPE GETS ROWS.** Generate the cross-owner combination — a non-owner
member reading another member's existing fact about a non-member subject (at minimum
`sam→ray/medication [exists-cross-member]`, needle `metformin`; the generator already
validates this combination) — and assert on the RECORD, not reply text: per
REQ_RECORD_GRADED_REFUSAL's grading, `guard_triggered=True` with a structural
`guard.kind`, zero foreign-needle presence, and the model not consulted for the refusal
(no inference latency attributable to a disclosure decision). A passing text-graded
refusal with `guard.kind=None` is a FAIL by definition here — that is the exact false
green this REQ exists to kill.

**(b) THE GUARD TRACE.** Assert the structural path fires REGARDLESS of admitted-set size:
the same unauthorized-subject query must produce a structural refusal with admitted=0 AND
with adjacent household/owner-owned facts admitted (the PW010 shape). Fault twin, both
directions: (RED) suppress the structural path by adding one adjacent admission to a
passing admitted=0 case and assert the check goes red if the guard silently degrades to
model-produced; (GREEN) the identical query with the adjacent admission present passes
once the path is admission-size-independent. Anti-vacuity: the twin must demonstrate the
suppression on today's code before the fix lands (it reproduces PW010's mechanism), so
the check cannot pass vacuously against a tree that never had the hole.

Both halves are namespaced per D-87 when built, wired as a standing battery, and graded
from d1.1 records. The four-part complement (twin/fixture/coverage/metamorphic-or-na)
applies in full per REQ_HARNESS_DISCIPLINE.

## WHAT'S ALREADY DONE

- REQ_RECORD_GRADED_REFUSAL (Voice 37, 4832ef9): refusal checks grade from the execution
  record — the instrument that exposed this class. Its baseline carries PW010/PW015 as
  accepted reds (TD-143/TD-144), visible not buried.
- INJ-7 (member-subject access control) is healthy and out of scope: member-subject rows
  (PW000/PW004/PW005) pass structurally. The verified discriminator is member vs
  non-member SUBJECT.
- PW013 proves the attribute-empty-set path exists and can fire for a non-member subject.

## WHAT'S KNOWN BROKEN

- Admission of adjacent household/owner-owned facts suppresses the empty-set path (evidence
  item 1) — the mechanism this REQ governs.
- The L4 matrix has zero rows for the genuine cross-owner shape (evidence item 5) — the
  acceptance's half (a) closes this.
- Why dad/allergy keyed `attr_empty_set` while ray/allergy did not (resolution vs
  attribute-keying difference, possibly TD-120 D2-adjacent) is OBSERVED but NOT yet traced
  — the build dispatch must trace it before changing anything (CLAUDE.md item 7: trace the
  whole path end to end first).

## NAMED ADJACENCIES — recorded, deliberately NOT folded in

- **TD-136 is live here and stays its own item**: household-owned facts about non-members
  reach every member unconditionally via INJ-4 — observed in PW017's reply, which drew on
  D8 (household-owned fall-risk about dad). Whether the household exemption should cross
  the member boundary this way is TD-136's already-filed question and Bill's call there,
  not this REQ's to preempt.
- **PW016/PW018 SKIP for a different reason**: `retract-without-successor` is not
  implemented (write kinds: supersede/augment only), so two rows of this subject class are
  untested for a reason unrelated to this mechanism. Recorded so the width number is
  honest; closing that is not this REQ's scope.

## CONSTRAINTS

- The fix is structural (injection contract / guard path), NOT a prompt or model change —
  "the model cannot decline to reveal what it never saw" is the product claim being
  restored, and a better-behaved model does not satisfy it.
- INJ-7's member-subject behavior must not regress (PW000/PW004/PW005 stay structural).
- Owner reads must not over-refuse: PW011/PW012 (owner reading their own facts about a
  non-member subject) keep disclosing. A structural refusal that also blocks the owner is
  a new defect, not a fix — hold it with its own check.
- The G1 record invariant and the F3 gate interact with any admitted-set change — RATCHET
  full-green per CLAUDE.md item 12 before done, CTX-STRIP and PSA1 reported individually.

## STATUS

**NOT MET. Filed, not built, not self-ruled.** No code exists for either acceptance half;
the build does not start until this REQ is named by its executing dispatch (item 8).

**RULED: Bill, 2026-08-03, D-128 — MET.** See the MET-Ruling in the Status header for the
six evidence points (each verified in the final runs) and the three recorded non-coverages.
The paragraph above is retained as written, for provenance — it was true at filing; D-126
did the mandatory trace, D-127 built both acceptance halves, D-128 ruled. The session
recorded the ruling; it did not make it.
