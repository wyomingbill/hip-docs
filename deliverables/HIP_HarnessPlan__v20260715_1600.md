# HIP Test Harness Plan

Version: v20260715_1600 MT
Source: Fable architecture review, 2026-07-15
Supersedes: everything proposed in chat earlier today

---

## THE REQUIREMENT, RESTATED

An orthogonal harness that:

1. GROWS WITH THE SYSTEM
2. Runs an END-TO-END REGRESSION ON EVERY PUSH
3. Emits METRICS THAT CAN BE TRACKED

Phases 1, 5, 6 are the three clauses. Phases 0, 2, 3, 4, 7 are the debt that makes them mean anything.

---

## THE TWO CONCEPTUAL CORRECTIONS

Everything below is wiring plus these two.

**Expectations flow from policy in exactly ONE place.** Today there are two oracles and they contradict each other. `disclosure_oracle.py` is policy-written and its docstring condemns implementation-derived oracles. `gen_pairwise.py` inlines its expectations in `_concretize` and its docstring says they are "constrained to combinations that have a deterministic expected outcome on the CURRENT build." Both ship. The matrix is an implementation-derived oracle wearing a generator costume, and `_valid()`'s exclusion list is the implementation's blind spots given amnesty.

**The gate must push in both polarities.** The current ratchet is monotonic over a scenario population where `value` is the only positive assertion. Every refusal-shaped change is indifferent or improving to every other row. The fixed point of that gate is a system that refuses everything, and nothing measures the truthfulness of what it does say. That is not a metaphor. It produced "Ray is watching a documentary about space exploration."

---

## PHASE 0 — CLOSE TODAY

Blocking. Nothing else starts until these land.

| # | Item | Note |
|---|------|------|
| 0.1 | Run "Who was Ray Charles?" | Decides whether the INJ-6 patch stands. If it guards, `has_personal_subject` must mean a household subject that BEARS FACTS, not any token that pattern-matched a name. |
| 0.2 | Correct PW014, PW029, PW030 expectations to `empty_set` | They expect `no_leak` and now get `empty_set`. They are red because the system stopped fabricating. The expectation was copied off a defect. |
| 0.3 | Fix G3's falsy check | `if ms:` treats `inference_ms=0` as no-inference. |
| 0.4 | Investigate `denied_counts={}` on guarded turns | Was `inj5=4` pre-patch, now empty. INJ-5 still fires. Either the guard path emits a thinner record or the counts are lost. The fail-open metric depends on this visibility. |
| 0.5 | Commit and push | Report the hash. |

**Exit:** the five manual queries behave, three matrix rows corrected, RATCHET PASS.

---

## PHASE 1 — WIRE WHAT EXISTS

Highest leverage in the plan. Lowest risk. Do this before building anything new.

`grep oracle eval/harness.py` returns nothing. Three correct artifacts exist and none of them runs on a push. That is the entire complaint, precisely stated.

| # | Item |
|---|------|
| 1.1 | `record_invariants --gate` becomes Layer 6 in `eval/harness.py` |
| 1.2 | Layer 6 runs over BOTH `logs/turns_demo.jsonl` AND the harness run's own turn log, so every scenario turn is also a property test |
| 1.3 | `test_disclosure.py` (the oracle runner) becomes a layer, asserting dispositions + `resolved_subjects` per record |
| 1.4 | Fabrication-class invariants (G1, G4) gate at HARD ZERO. Never baselined. `--accept` refused. |

**Exit:** a push cannot fabricate about a person without turning something red.

---

## PHASE 2 — ONE ORACLE

The first conceptual correction.

| # | Item |
|---|------|
| 2.1 | Delete `expected` from `gen_pairwise._concretize`. The oracle computes it. |
| 2.2 | `disclosure_oracle` gains an INTENT dimension. It has none today and intent is the master switch on INJ-5. |
| 2.3 | `disclosure_oracle.FIXTURE` verified against `demo_seed.FIXTURES` **in code at import**. The current cross-check validates the matrix against `access()`, both defined in the same file. That is self-consistency, not fixture-consistency. The "verify before trusting" comment is a bug report filed against its own file. |
| 2.4 | `_valid()` stops excluding. Gaps are generated and SKIP-marked so they stay counted. |
| 2.5 | `no_leak` dies as an outcome. It asserts only "no access-control refusal and no foreign needle" (layer4.py:50-53), so it passes on fabrication. Replaced by oracle disposition plus the G-invariants. |

**Exit:** one source of expectations. `gen_pairwise` generates traffic and nothing else.

---

## PHASE 3 — FAIL CLOSED

The root cause. Not the guard, the classifier.

`classify()` defaults to `knowledge` on BOTH below-threshold AND embedding failure. `knowledge` is the unique intent that simultaneously strips all personal facts via INJ-5, disarms both empty-set guards, and leaves `path=generation` open. **The system's default state under uncertainty is its most dangerous state.**

| # | Item |
|---|------|
| 3.1 | Below threshold WITH a resolved personal subject must not proceed as `knowledge` |
| 3.2 | Third-party exemplars into `personal`. All ~30 entries are first-person today. The beachhead is eldercare, which is entirely third-party. |
| 3.3 | G0: reply names a registered member or care recipient while `resolved_subjects=[]` or nothing admitted about them. Closes G1's blind spot. |
| 3.4 | Cross-stage consistency check, in-line: `resolved_subjects` naming a tracked human while `intent=knowledge` is a contradiction sitting in one record. Nothing cross-checks it today. |

**Exit:** fail-open rate measured and falling. G0 gated.

Note 3.3 is not optional. G1 requires `resolved_subjects` non-empty, and trust_ladder T04 died with `intent=noise, subjects=[]`. A fabrication with `subjects=[]` passes all four G checks today.

**AMENDMENT 2026-07-16** (`HIP_SIA_PhaseB__risk-memo__v20260716_1624.md` §9,
adopted by Bill; reconciled in
`REQ_SIA_PHASEB__reconcile-plans-and-file-requirement__v20260716_1736.md`):
this phase's position in the sequence above does NOT govern G0's actual
build priority. The risk memo's adversarial review
(`ANALYSIS__postcondition-gap-review__v20260716_1512.md` §2) re-ranked G0 to
item **0b — second in the whole exit-gate sequence**, ahead of Phase 0/1/2
of this plan entirely, because the risk-memo's G0 is a RUNTIME gate on the
live reply (closes I-06's defect class — the atorvastatin/D-03/D-18 family —
before it is ever spoken), not the offline/gate-time invariant this section
specs. Both are real, separate artifacts checking the same condition; only
one name. **The risk memo is authoritative on when the runtime gate ships.**
This section's 3.3 still stands, unchanged, as the spec for the harness-side
invariant, which still gates a push rather than a reply and is still
sequenced here in Phase 3. Item 0b (the runtime gate) is, as of this
amendment, still unbuilt — c86a414 shipped only the risk memo's item 0
(F3 gate widened to all declaratives + detection retry), not 0b.

---

## PHASE 4 — TRAFFIC THAT GROWS

The "grows with the system" clause.

The semantic frame (role x subject_ref x attribute x fact_state) is finite and enumerable. Keep the combinatorics. The linguistic surface is unbounded and hand-listing it is the trap. All five `PHRASINGS` templates interpolate `{noun}` from a fixed table, so the generator's surface distribution is a proper subset of the classifier's exemplar neighborhood. Layer 4 measures the classifier agreeing with itself.

| # | Item |
|---|------|
| 4.1 | Idiom bank. Curated, adversarial. Grows by ONE ENTRY PER INCIDENT. Entry one is "What's Ray on?" |
| 4.2 | Paraphrase pool, LLM-generated, regenerated per push |
| 4.3 | **Enforced minimum cosine distance from every classifier exemplar.** Surface novelty measured, not hoped for. |

The fix for an un-enumerable dimension is to make it generative and measure its distance from the training distribution. Not to enumerate harder.

**Exit:** the corpus-to-exemplar distance metric is non-degenerate.

---

## PHASE 5 — METRICS

Per push, appended to `harness_trend.jsonl` beside the existing trend records.

| # | Metric | Why |
|---|--------|-----|
| 1 | **Fail-open rate** | Fraction of turns where the classifier returned the fallback. The single most diagnostic number in the system. Would have been visibly nonzero from day one. |
| 2 | **Third-party personal recall** | On a labeled caregiver-shaped probe set. Approximately zero today. Would have been a flat red line for the project's entire history, and it is the beachhead. |
| 3 | Classifier margin distribution | Median and minimum top1-top2. The `{noun}` problem is near-threshold mass a template corpus never samples. |
| 4 | Corpus-to-exemplar distance | The `{noun}` finding as a number instead of a post-mortem. |
| 5 | Oracle agreement rate | T03 shows as a step down. |
| 6 | Withheld-own-fact count | The utility failure class, directly. |
| 7 | G1 / G4 counts | Over the harness's own turn log, not just the demo log. G1=4 was sitting in the log before anyone looked. The number was free the whole time. |
| 8 | Guard fires by kind, empty-context generation count | INJ-6 firing zero times across all runs ever is a loud number for a supposedly load-bearing guard. |

**Exit:** eight numbers per push, trending.

---

## PHASE 6 — RECORD FIDELITY

Everything above stands on an unchecked assumption.

`admitted[]` is the system's self-report. Nothing verifies it equals the facts actually serialized into the prompt. A bug between the contract and prompt assembly makes every per-stage assertion a lie.

| # | Item |
|---|------|
| 6.1 | Hash the injected block into the record |
| 6.2 | Assert the hash matches `admitted[]` |

**Exit:** the record is a contract, not a claim.

---

## PHASE 7 — THE GATE

Bifurcate. Do not replace.

| Population | Gate |
|------------|------|
| Structural / negative invariants (access matrix, guard-implies-no-inference, G2-class) | Monotonic ratchet. "Never regress" is correct semantics here. |
| Oracle agreement rate | **Opposite-polarity ratchet.** Must not decrease. |
| Fabrication class (G0, G1, G4) | **Hard zero. Never baselined. `--accept` refused.** |
| Known failures | `--accept` carries an expiry or a linked debt ID. A failing positive case can be baselined into permanence with one string today. |

---

## WHAT TODAY GOT WRONG

Kept verbatim so it does not repeat.

1. Built three artifacts beside the harness with no gate wiring. The requirement was stated three times and the deliverable satisfies none of its three clauses.
2. Left `gen_pairwise`'s implementation-derived expectations standing while writing an oracle whose docstring condemns exactly that pattern. Both ship and contradict.
3. `record_invariants` points at the demo log by default. A convenience sample. Finding bugs by hand, mechanized.
4. Misdiagnosed the guard as predicate coupling when the operative defects are the classifier's fail-open default and INJ-6 starvation by INJ-4.
5. G1 inherits the subjects-empty blind spot, unflagged, even though T04's death mode is cited in the oracle file.
6. The oracle fixture is hand-transcribed with a comment saying "verify before trusting" instead of code that verifies.
7. Nothing asserts the record is faithful to the prompt actually sent.

---

## ORDER

0, then 1. Phase 1 is the requirement's second clause and it is mostly wiring.

Then 3 before 2, because fail-open is the root cause and Phase 3 is smaller.

Then 2, 4, 5. Phase 6 whenever, but before anyone cites a per-stage assertion as proof.

Phase 7 lands with each population as it arrives.
