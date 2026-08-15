# Harness Gap Spec: assertions the live harness (Tier L) must add

Date: 2026-07-08 (Mountain Time)
Companion to: HITL__phase4-findings__v20260708_0951.md
Purpose: convert every defect found by hand in Phase 4 HITL into an automated gate, so it never requires human validation again.

## The core problem

The existing E1-E8 harness (eval/integration_live.py) passed 8/8 while the system could not retrieve a just-written fact. The harness checked that E1 produced an acknowledgment ("not a refusal"), not that the asserted fact was:
1. persisted as the active head (not closed/superseded),
2. retrievable by its owner in a later turn,
3. attributed to the correct person,
4. protected from unauthorized cross-member reads with the correct refusal semantics.

A passing gate that coexists with F-1/F-2 means the gate asserts the wrong thing. This spec fixes that.

## New assertions to add

### G-1 Write lands as active head (covers F-2)
After an assertion turn, query the graph directly (not via the assistant): the newly asserted fact must be the ACTIVE head for (owner, attribute, subject). Assert write_state is active/asserted, NOT closed/superseded. This would have caught F-2 at the source.

### G-2 Owner can read own fact next turn (covers F-1)
After owner asserts fact X in turn N, owner asks for X in turn N+1. Assert the reply CONTAINS the value and is NOT the empty-set refusal string. This is the single most important missing assertion. Run it for at least: personal allergy (Sam/penicillin) and cross-subject medication (Bill re Elena).

### G-3 Empty-set refusal only when truly empty (tightens INJ-6b)
Assert the empty-set refusal fires ONLY when no active fact exists for the (owner, attribute) pair. If an active fact exists, the empty-set string must NOT appear. This separates a true empty set from F-1's false negative.

### G-4 Cross-member deny is distinct from empty-set (covers F-4/F-9)
When member A queries member B's private fact that DOES exist, assert the response is the access-control refusal, NOT the empty-set string, and NOT the plaintext value. Requires two distinguishable refusal strings in the code:
- empty-set: "no active fact exists"
- access-control: "exists but not authorized"
Gate asserts the correct one fires per case.

### G-5 Attribution correctness (covers F-3)
For a turn whose reply names a person, assert the named person matches the fact subject. Bill asserts about "mother Elena"; a downstream reply must not refer to "Dad." Implement as: reply must not contain a person token absent from the turn's fact subjects.

### G-6 Confidence non-regression on supersede (covers F-5 trust-regression)
On a supersede, assert incoming confidence >= outgoing confidence, OR the supersede is explicitly gated (Fork B) / labeled with authority (Fork A). This gate's exact form depends on the F-5 fork decision, so it is specified but PARKED until that decision is made.

## Gate discipline

- Each assertion above is a hard gate: red on failure, same as the existing E1-E8.
- G-1 through G-5 are implementable now against the current fact model.
- G-6 is parked pending the TD-110 fork decision.
- Add these to eval/integration_live.py under the existing Tier L harness so they run on the real HTTP path, not shims.
- Re-run the full gate after the F-2 write-state fix. Expect G-1/G-2/G-3 to go green together if F-2 is the true root cause.

## Order of work

1. Root-cause and fix F-2 (write lands in retired state).
2. Add G-1, G-2, G-3. Confirm they now pass on the fixed code and would have failed on the old code.
3. Add G-4, G-5.
4. Resolve TD-110 fork, then add G-6.
