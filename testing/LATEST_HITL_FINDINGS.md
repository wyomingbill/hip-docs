# HITL Phase 4 Findings

Correction 2026-07-11: F-5 was assigned TD-110, not TD-109; TD-109 remains biometric consent and retention (CHG-8). This document is left otherwise unedited as the historical record of the Phase 4 session; the F-5 finding below still reads "elevated to TD-109" in its heading even though the same finding correctly states "Filed as TD-110" in its body. Treat TD-110 as the correct identifier for the cross-member write-authority gap everywhere in this document.

Date: 2026-07-08 (Mountain Time)
Build under test: dashboard on commit d4a031e + HITL routes (a35c933, 959be24), text live path 8/8
Method: manual human-in-the-loop against /demo scripts (reveal_demo, care_coordination), operator-paced
Scope note: 7860 voice server runs the FROZEN hip-harness build and was NOT judged. All findings are against the seam-wired dashboard code (7871).

## Summary

HITL surfaced a systematic correctness bug the automated 8/8 harness did not catch: facts that are asserted and acknowledged in one turn are not retrievable by their own owner in a later turn. Reproduced twice, across two scripts and two members. Root cause appears to be the write path landing facts in a retired/closed state rather than as the active head. Several governance-legibility and demo-UX findings were also logged.

The central lesson: the 8/8 harness validated that E1 produced an acknowledgment, not that the written fact was retrievable, in the correct state, by the correct person. The harness gap spec (companion doc) addresses this.

## Findings

### CORRECTNESS FAILURES

**F-1 (HIGH) Write-then-cannot-read. Owner cannot retrieve own just-asserted fact.**
- care_coordination, turn 6: Sam asserts penicillin allergy (acked, ASSERTED in timeline). Sam then asks "What allergies do I have?" and receives the empty-set refusal "I don't have that confirmed yet."
- care_coordination (Elena variant), turn 2: Bill asserts Elena switched to Jardiance (acked). Bill then asks "What did I tell you about my mother's medication?" and receives "I don't have that confirmed yet."
- Two independent reproductions, two members, two scripts. Systematic, not incidental.
- The fact exists in the epistemic timeline but is not surfaced to the injection contract on retrieval.
- Possible link to TD-044 (INJ-6b keyword bypass).

**F-2 (HIGH, likely root cause of F-1) Write lands in retired state.**
- Epistemic pane shows Bill's just-asserted "medication re elena / Jardiance 10mg" as "closed", struck through, SUPERSEDE, rather than as the active ASSERTED head.
- If the write lands as closed/superseded instead of active head, retrieval correctly finds no active fact, which produces F-1. F-1 and F-2 are probably the same defect observed from two angles (read side and write side).

**F-3 Wrong-person / wrong-gender attribution.**
- Elena variant, turn 3: Bill said "my mother Elena." The budget reply referred to "Dad's health." Attribution flipped person and gender mid-conversation.

### GOVERNANCE LEGIBILITY

**F-4 Cross-member deny uses empty-set phrasing.**
- Sam asks Maya's meds; Sarah asks Elena's meds. Both are INJ-3 cross-member privacy denials, but both render as "I don't have that confirmed yet" (the INJ-6b empty-set string).
- HIP holds the data (e.g. Maya's lisinopril). The honest response is an access-control boundary ("I can only share Maya's information with Maya"), not feigned ignorance.
- The system conflates "I do not know" (epistemic gap) with "I cannot tell you" (access control). For a governance credibility instrument this hides the very boundary it should showcase.

**F-5 (governance design question, elevated to TD-109) Cross-member write authority gap.**
- Maya's single ASSERTED statement superseded Ray's CORROBORATED seed fact with no authority check, trust gate, or provenance audit.
- Asymmetry: INJ-3 blocks cross-member reads, but the write path has no equivalent. One member can silently overwrite another member's health record.
- Trust regression: the incoming fact opened as ASSERTED while the fact it replaced was CORROBORATED. The write path does not check that incoming confidence is at least equal to what it supersedes.
- Two forks require a decision before the next operator demo:
  - Fork A (caregiver authority, intended): Maya has declared authority over Ray/Elena health facts. Supersede is correct, but the demo must surface the authority ("Maya (caregiver) -> Ray") or it looks like a bug.
  - Fork B (write gate required): a single member's assertion about another member lands as UNCONFIRMED, needs corroboration or explicit confirmation to promote to a supersede.
- Filed as TD-110, tagged governance-decision-required.

### DEMO / UX

**F-6 Dialogue pane does not auto-scroll.**
- New question/response does not scroll into view. The evaluator cannot see the current exchange without manual scrolling. Demo-blocking on its own.

**F-7 Q and A render simultaneously (pre-packaged look).**
- Question and answer appear at the same instant, reading as canned pairs rather than live routing. Undercuts the real-time governed-routing story the demo is meant to prove.

**F-8 Routing pipeline does not record every turn.**
- Some turns produce no routing-pipeline row. Inconsistent; reads as broken to an evaluator.

**F-9 Refusal string is robotic and overloaded.**
- "I don't have that confirmed yet" is used for both a true empty set and a privacy denial (see F-4), and reads as a system string rather than an assistant. Single generic phrase for two distinct guard outcomes.

**F-10 Epistemic pane is developer-view, not operator-view.**
- Engine vocabulary surfaces raw (SUPERSEDE, AUGMENT, HARDEN, DERIVED, CONFIRMED/CORROBORATED/ASSERTED, "re null").
- No visual hierarchy: trash pickup and a fall-risk medical pattern carry identical weight.
- The hero object (the medical supersede with old -> new) is buried mid-list and half-cut-off.
- Recommended direction (design sprint, not a live fix): group by member; render confidence as a visual (dots/color) so the trust regression in F-5 becomes legible at a glance; make the supersede the centerpiece with "changed by X, when"; move transition types to hover/detail.

## Per-item checklist status

- HITL-1 (response naturalness): FAIL. Person attribution mostly correct, but F-1 (correctness), F-4/F-9 (refusal phrasing) fail the item.
- HITL-2 (timeline legibility): FAIL on legibility (F-10). Chain is mechanically clean (one transition, old struck, new active, no duplicate Jardiance, no raw fact_ids) but labels need narration.
- HITL-3 (narration fit): FAIL. F-1, F-2, F-3, F-6, F-7, F-8 all observed driving the full script at speaking pace.
- HITL-4, 5, 6: not run. Stopped after F-1/F-2 reproduced, since the write-state defect blocks meaningful further evaluation.

## Recommended next action

Root-cause F-2 (write lands in retired state) first. It is the likely single cause of F-1 and the highest-value fix. Do NOT fix live during HITL. Hand to a bounded CC engine session with the harness-gap spec so the fix is gated, not hand-validated.
