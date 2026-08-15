# REQ_TRUTH_TRACK: Stage 5 — Fail-Closed Routing, G0, Calibration, and Truth Metrics
Version: v20260719_0910
Status: SUPERSEDED

**SUPERSEDED 2026-07-21 by REQ_CONFIDENCE_DISCIPLINE__truth-track__v20260721_0840
(which now carries phases A-G + T02/D-24, folded in and Bill-confirmed by
phase-ownership map). Retained here for history, not a live REQ — do not
build against this file; build against REQ_CONFIDENCE_DISCIPLINE.**

Branch: roadmap
Reconciled against: [[hip-harness]] root-cause (fail-open routing); HarnessPlan phases 2-7; the four 2026-07-15 defects; care_coordination T02 (backlog #15c); D-24; SIA

## What this is

The truth track. It runs parallel to the crypto track, shares only identity binding, and answers a different question: does HIP say true things, and does the harness catch it when it does not. This REQ collects the truth work into buildable phases with pass/fail gates and the metrics that make truthfulness visible per push.

The crypto track protects who can READ a fact. This track protects whether what HIP SAYS is true. A perfectly isolated system that confidently fabricates is still a failed product. The documentary about Ray's afternoon was not a leak; it was a lie, told to a caregiver, that every existing test passed.

## The root cause this track fixes

FAIL-OPEN ROUTING. The intent classifier defaults to "knowledge" on both below-threshold and embed failure. "knowledge" is the single most dangerous intent: it strips all personal facts (INJ-5), disarms both empty-set guards, and leaves generation open. The system's default under uncertainty is its most dangerous state. Every one of the four defects traces here.

The fix is fail-CLOSED: below threshold WITH a resolved personal subject must not proceed as knowledge. When unsure, withhold. This mirrors the crypto track's fail-private. Both tracks default to safe when the model is uncertain.

## The phases

PHASE A — Fail-closed routing (the core fix).
Below-threshold classification with a resolved personal subject routes to a withhold path, not knowledge. Embed failure does the same. The classifier's uncertainty becomes a refusal to assert, not a license to fabricate.
Acceptance: "What's Ray on?" (idiomatic, below threshold, subject=ray) no longer fabricates; it withholds or asks. Fail-open rate becomes a gated metric, not just visible.

PHASE B — SIA (subject-intent-agreement) and the contradiction check.
resolved_subjects naming a tracked human WHILE intent=knowledge is a contradiction sitting in one record that nothing currently cross-checks. SIA asserts: if a resolved subject is a household member or care recipient, intent may not be "knowledge". This catches the "What's Ray on?" / "Who was Ray Charles?" collision from the SUBJECT side, independent of the classifier.
Acceptance: SIA fires on the contradiction; the 14.3% SIA figure is adjudicated (measured, not cited) and driven down.

PHASE C — G0 (the invariant that does not depend on upstream stages).
Every existing invariant (G1-G4) requires resolved_subjects non-empty — a fabrication with subjects=[] passes all of them (the T04 "Yes, confirm that" case). G0: the reply names a registered member or care recipient while subjects=[] or nothing is admitted about them. G0 is the only check that does not depend on an upstream stage understanding the sentence. It has never been built. Build it. Hard-zero.
Acceptance: G0 catches a fabrication that names a member with empty subject resolution. Demonstrated red by fault-injection.

PHASE D — The decision table (D-01 fail-open closure).
The routing decisions (which intent, which guards, which path) become an explicit table with policy-level expected outcomes, replacing the implicit fail-open default. This is D-01's real fix via the decision table, not a patch on one predicate.

PHASE E — Calibration.
The classifier's confidence must mean something. Calibrate margin-to-correctness so the below-threshold cutoff is principled, not a guessed 0.30. Measure classifier margin distribution (top1-top2) as a per-push metric.

PHASE F — The truth metrics (per push, HarnessPlan phases 2-7).
The numbers that make truthfulness visible, best first:
1. FAIL-OPEN RATE — fraction of turns hitting the fallback. The single most diagnostic number. Nonzero from day one.
2. THIRD-PARTY PERSONAL RECALL on a caregiver-shaped probe set — near zero today, and it is the beachhead. A flat red line for the project's history until fixed.
3. Classifier margin distribution.
4. Corpus-to-exemplar cosine distance (the {noun} finding as a number).
5. Oracle agreement rate.
6. Withheld-own-fact count (utility regression guard — the flip side of fail-closed).
7. G0/G1/G4 counts over the harness's own turn log.

PHASE G — The gate bifurcation.
Not one ratchet. Monotonic ratchet for structural/negative invariants (never regress). OPPOSITE-POLARITY ratchet on oracle-agreement rate (must not decrease). HARD ZERO, never baselinable, --accept refused, on fabrication-class invariants (G0, G1, G4). Every other --accept carries an expiry or a linked debt ID, so a failing positive case cannot be baselined into permanence with one string.

## THE T02 / D-24 DECISION (backlog #15c) — folded in, needs Bill's call

care_coordination T02 is a REAL defect, not test debt: a caregiver asks about a medication change and gets "I don't have that confirmed yet" when Jardiance should surface. The fixture asserts on reply content; fixing the test would delete the assertion that caught it. D-24's two options:

(a) Narrow the classifier's trigger language so the medication-change phrasing classifies personal (not knowledge), so the fact is retrieved.
(b) Widen medication-keyed retrieval so the fact surfaces even when classification is imperfect.

RECOMMENDATION built into this REQ: (a) is the right primary fix because it is the same root cause as Phase A — the query classifies wrong and loses its facts. Fixing classification fixes T02 and the whole class. (b) is a retrieval band-aid that masks the classifier without fixing it, and widening retrieval risks surfacing facts the partition should have withheld — it fights the crypto track. Do (a). Keep (b) only as a measured fallback if (a) cannot reach the phrasing.

DECISION FOR BILL: confirm (a) as primary, (b) rejected or fallback-only. [confirm / choose (b)]

## THE ACCEPTANCE TEST (per phase, pass/fail)

- Fail-open rate is gated and trending down (Phase A/D).
- SIA contradiction fires and is measured (Phase B).
- G0 built, hard-zero, demonstrated red by fault-injection (Phase C).
- Third-party personal recall probe set exists and the number moves off zero (Phase F).
- T02 passes via the chosen fix WITHOUT deleting the assertion that caught it.
- --full passes with all fabrication-class invariants hard-zero and no --accept on them.

## DEMONSTRATION OBJECTIVE

Co-equal to the build. Not rigged. This is the demo that proves HIP does not lie, which is a harder and rarer claim than "HIP is encrypted."

SHOW: The fail-open rate on the dashboard, nonzero, then driven down by the fix. Then the money moment: ask "What's Ray on?" the idiomatic way that used to fabricate a documentary, and watch it withhold or ask instead of invent. Then G0 catching a fabrication live, and fault-injection proving G0 can go red.

LET THEM RUN: Let the engineer try to make HIP fabricate — ask about a care recipient in the phrasing that breaks classification, ask a question with no facts behind it, try to get a confident wrong answer. Watch it refuse to assert what it cannot ground. Let them run the third-party recall probe set themselves.

THE CLAIM IT PROVES: "When HIP is not sure, it does not make something up. We measure how often it is unsure (the fail-open rate), we catch fabrication with an invariant that cannot be silenced, and we show you the exact query that used to lie and now does not."

THE HARDEST QUESTION + HONEST ANSWER: "You fixed the one query you showed me. How many other phrasings still fabricate?" Answer, limit stated first: we do not claim zero fabrication — we claim a MEASURED and FALLING fail-open rate and a hard-zero invariant (G0) that catches the fabrication class, not one phrasing. The honest gap: the classifier was trained almost entirely on first-person examples and the beachhead is third-party caregiver queries, so third-party recall starts near zero and climbs; we show you that number and its trend rather than a single passing demo. A system that claimed no fabrication would be the fabrication. We claim we measure it, gate the worst class at hard-zero, and it improves every push.

## CONSTRAINTS

- Fail-closed must not over-withhold a member's OWN facts (withheld-own-fact metric guards this). Fail-closed on THIRD-party uncertainty, not on a member asking about themselves.
- Do not gate on intent equality — intent is an implementation intermediate; track as metric. Gate on policy-level stage outputs (resolved_subjects, guard_kind, path, dispositions).
- Fabrication-class invariants (G0/G1/G4) are hard-zero, --accept refused. No baselining a lie into permanence.
- T02's fix must not delete the assertion that caught it. The test stays; the system changes.
- This track shares ONLY identity binding with crypto. It does not depend on any Stage 4 phase and runs in parallel.
