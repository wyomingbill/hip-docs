# FABLE_CuratorReview: Curator Test-Model and Gate Code Review
Status: BUILT
Branch: roadmap
Reconciled-Against: 49bc332 (2026-07-30) for the gate
(harness/learner_isolation.py, unmodified by the D-33 build); scorer reviewed
against a pinned 07:42 MDT snapshot of the then-uncommitted D-33 working tree,
**since verified byte-identical to what D-33 committed at 9d867f8** — so the
scorer findings apply to committed code, not to a superseded draft (see
"Snapshot fidelity" below)

## What this document is

D-35 routed the D-34 review package (`/tmp/d34_fable_review_package.md`) to
Fable as two independent read-only reviews and captured both responses. The
two reviews below are reproduced **VERBATIM** as Fable returned them. They
are the artifact; this header is the only text in this file not written by
the reviewer.

**Both reviews are UNVERIFIED by the routing session.** Per the D-35
dispatch's own instruction — "Do NOT act on its findings this pass — just
get the review back intact" — no finding here has been independently
confirmed, reproduced, or tested by the session that filed this document.
Several findings make specific, checkable claims about schema columns, line
numbers, and code paths. Treat every one as a claim to verify, not a
measurement to trust. That verification is its own dispatch.

**No REQ status is proposed, implied, or changed by this document.** Both
reviewers were instructed not to propose MET and both explicitly declined to.
MET remains Bill's ruling alone.

## Provenance and method

- Routed 2026-07-30 ~07:45 MDT from `~/hip-roadmap`, branch `roadmap`, by a
  Claude Code session running as bill-ai on [REDACTED-MACHINE-NAME].
- Two independent Fable agents, run in parallel, each given one of the two
  D-34 briefs plus the file list. Neither could see the other's work or
  findings.
- Both were constrained read-only: no file edits, no harness runs, no pytest,
  no writing git commands. Both confirm they made no writes.
- **Concurrency note:** the D-33 shadow-scorer build was IN FLIGHT when these
  reviews were routed. Session 29d1f95d held `docs/.GRAPH_HARNESS_LOCK` (taken
  07:27 MDT) and its scorer code was uncommitted and being actively edited —
  files were written at 07:35 and 07:37. To give the code reviewer a stable
  target rather than a moving one, the uncommitted files were copied to a
  scratchpad snapshot at 07:42 and both reviews were pinned to that copy.

- **Snapshot fidelity — checked, and the news is good.** D-33 committed at
  `9d867f8` while this document was being assembled, and released the lock.
  The snapshot was then diffed against the committed files:
  `harness/curator_shadow.py` and `eval/harnesslib/curator_agreement.py` are
  **byte-identical** between the 07:42 snapshot and `9d867f8`. The scorer
  findings therefore describe the code that actually landed — they are not
  observations about a draft the author has since moved past. The usual
  in-flight caveat does not apply here, and the "may already be stale" hedging
  the reviewers wrote into their own text (they could not have known) should be
  read in that light. Gate findings never carried the caveat: the gate is
  committed and was untouched by the D-33 diff.

## Convergence between the two reviews

The two reviewers worked independently and did not share findings. They
nonetheless landed on the same defects from opposite directions — one reading
the code adversarially, one reading the test methodology. Convergence is not
proof, but independent agreement is worth more than either review alone, and
these are the items where it happened:

| Defect | Code review | Test-model review |
|---|---|---|
| Target `household_id`/`audience` are caller-asserted; D-30 authenticated only the example side | G-2 (high) | Finding 3 (ranked 3rd) |
| Empty target `audience` is a universal V2 bypass (`frozenset()` is not `None`) | G-2, G-11 | Finding 4 (ranked 4th) |
| `resolver=` keyword is a total bypass of the authenticity guarantee | G-5 | Finding 10 |
| V4 `label_source` verifies a string, not a provenance — and is now unfireable | G-6 | Finding 6 |
| `validate_shadow_output` is tautological in-path | S-6 | Finding 1 (ranked 1st) |
| `historical_acceptance` / weight cache pool across the whole log | S-4 | Finding 7 |
| Feature allowlist is depth-1 while the delegated denylist recurses | S-2 | Finding 11 |
| Agreement metric's lookahead window disagrees with the label builder's | S-5 | Finding 12 |
| The "shadow cannot act" static scan covers only two hard-coded files | S-3 | Finding 16 |

Two significant findings appear in only one review, which is itself worth
noting:

- **Only the test-model review** found that
  `eval/test_learner_isolation_adversarial.py` — the 23-case battery that
  found all six D-25 holes — is wired into no runner at all: absent from the
  audit roster, absent from `check_registry`, and never invoked by
  `eval/harness.py`, `scripts/run_harness.sh`, or any CI (it reports there is
  no Makefile and no `.github/`). If true, the battery's expectations can
  regress silently.
- **Only the code review** found the claim that `_audience_of`'s dyad branch
  reads four column names (`member_a`, `member_b`, `caregiver`, `recipient`)
  that it says do not exist in the `dyads` schema, which would make every
  dyad-private fact derive an empty audience.

Both are unverified. Both are cheap to check.

---
---

# REVIEW 1 of 2 — TEST-MODEL REVIEW (priority)

*Reproduced verbatim as Fable returned it. Unverified by the routing session.*

---

# Methodology Review — Does the Curator Shadow Scorer Repeat the D-23 Blind Spot?

**Reviewer:** read-only dispatch, 2026-07-30. Repo `[REDACTED-USER-PATH]/hip-roadmap`, branch `roadmap`, HEAD `49bc332`, working tree carrying the in-flight D-33 build (uncommitted: `harness/curator_shadow.py`, `eval/harnesslib/curator_agreement.py`, and modifications to `check_registry.py`, `harness_audit.py`, `layer7_crypto.py`, `epistemic_record.py`, `server/voice_orch.py`). No file was modified, no test or harness was run, no writing git command was issued.

---

## Summary — headline conclusion

**The blind spot is not "about to repeat." It has already repeated, in the uncommitted tree, and it is visible in the code as written.**

The framing's thesis holds, but it is aimed one notch off-target. The D-25 defect class is not "fixtures supply the value" in general — it is narrower and sharper than that, and naming it precisely is what makes it fixable:

> **An ASSERTIVE test — one that compares an output against a value the test itself authored, through the same channel the caller controls — can only prove the logic is right given honest inputs. A DIFFERENTIAL test (two runs, one variable) or a STRUCTURAL test (a property of the code graph) has no such channel and is immune by construction.**

Judged on that line, the D-33 build is genuinely mixed and mostly good: acceptance items 4 and 5 are built as *differential* proofs (weights-with vs weights-without; prompt bytes on vs off) and are among the strongest checks in this codebase. But **acceptance item 2 — `curated ⊆ admitted`, the invariant the REQ explicitly "pulls forward into shadow so it is proven before anything can act" — is built as a tautology.** In `harness/curator_shadow.py:424-426`, `admitted_ids` and `ranking` are both derived from the same local variable `allowed` in the same function call, and `score_facts` is a permutation of its input by construction. The in-path assertion cannot fire. The scenario's own comment concedes it: `# unreachable by construction; checked anyway` (`curator_shadow.py:427`). That is exactly the D-23 shape — a real invariant, correctly implemented, validated against a value that cannot disagree with it.

Second headline: **the single artifact that actually caught the six holes is the only one in the whole affair that no gate enforces.** `eval/test_learner_isolation_adversarial.py` is not in the audit roster (`harness_audit.enumerate_roster` scans only `Scenario(...)` calls in `layer7_crypto*.py` plus `record_invariants.CHECKS`), has no `check_registry.py` entry, and is never invoked by `eval/harness.py`, `scripts/run_harness.sh`, any Makefile, or any CI — there is no Makefile and no `.github/` in this repo (VERIFIED). Its 23 security-correct expectations regress silently. The project institutionalized the *fix* and left the *finding mechanism* as folklore.

Third: **the Four is necessary-but-not-sufficient, and I can name the sufficiency gap mechanically rather than rhetorically.** `harness_audit._COVERAGE_KEYS` (`harness_audit.py:54`) is the fixed 4-tuple `("roles", "scopes", "attribute_splits", "intent_classes")`, and `_verify_coverage` (`:623-633`) accepts any non-empty list for each. That schema partitions the *authorization* state space. It has no axis for *input trust*. A coverage entry structurally **cannot** say "this check assumes `household_id` is authentic," so D-23's honest, careful coverage entry named an unfixtured roster slice and could not have named the trust assumption even if the author had thought of it. The gap is in the schema, not only in the execution.

Fourth, and this is the finding I would act on first regardless of the shadow scorer: **D-30 authenticated the example side of the relation and left the target side entirely caller-supplied.** `check_training_example` derives `household_id` and `audience` for the *example* from an un-forgeable `fact_id`, then compares them against a `target` dict whose `household_id`, `audience`, and `model_id` come straight from the caller with no derivation and no validation (`harness/learner_isolation.py:260, 284-292`). A caller that hands the gate `{"audience": frozenset()}` passes V2 unconditionally, for any example in the household, including member-private ones — the code checks `tgt_aud is None`, and an empty frozenset is not None (`:286`). The 23-case battery contains no target-forgery case at all. HOLE-1 has a mirror image that was never looked for.

---

## Question 1 — Does the shadow scorer carry the same blind spot?

I read all nine acceptance items in `REQ_CURATOR_SHADOW_SCORER__stage2-shadow-metadata-scorer__v20260730_0710.md` and, because the build landed while this review was in flight, checked each against what is actually implemented in the working tree.

**Verdict on the stated hypothesis: PARTIALLY HOLDS — and it under-called item 2 while mis-diagnosing item 6.**

### Per-item: who supplies the value, and can that supplier lie?

**Item 1 (input is exactly `injection.allowed`) — NOT blind, but the specified observable was not built.**
The property "output ⊆ input" holds for `score_facts` by construction — it enumerates `facts` and returns their `fact_id`s (`curator_shadow.py:210-225`). A universally-quantified permutation property is not sensitive to which A the fixture picks, so fixture-supplied A is not a defect here. What *was* specified and not built: the REQ demands "a graph/fixture containing authorized-but-not-admitted and unauthorized facts outside A." The CS1 fixture `_cs_facts` (4 facts) **is** the entire universe — there is no out-of-A decoy population; the escapee is a synthetic string `"cs-alien"`. Confidence: VERIFIED (read the CS1 diff). Materiality: low for the pure function, non-zero for the wiring, which item 1's observable was designed to catch.

**Item 2 (curated ⊆ admitted, "asserted — not assumed") — BLIND. The strongest instance in the build.**
`shadow_score_turn` computes `ranking` from `rows` (from `allowed`) and `admitted_ids` from `allowed`, then calls `validate_shadow_output(admitted_ids, ranking)` (`curator_shadow.py:421-426`). Both arguments trace to one local list; the function between them is a stable sort. The assertion is analytically true. The REQ's own words — "asserted in the shadow logging path itself" — are satisfied literally and voided semantically. The only non-vacuous test is the twin, which hand-feeds a value that never occurs on any real path. This is D-23 with different variable names: correct logic, validated against a supplier who cannot disagree. Confidence: VERIFIED. **This is the item to fix before the build is assessed.**

**Item 3 (metadata-only, ten declared keys) — MIXED. Fixture half is differential and strong; structural half was not built; the allowlist has a depth bug.**
The value-blindness proof (CS1 sub-check iv) is *differential* — two facts identical in metadata, different in value, byte-identical feature dicts — and is immune to the D-25 problem. Good. But:
- The REQ's first observable also demanded a *structural* check: "the extractor module imports nothing from the decrypt path; grep for the decrypt entry points in the extractor comes back empty." No such scan exists in the CS1 scenario or in `harness_audit.py` (VERIFIED). It was true at write time by inspection; nothing will notice when it stops being true.
- `validate_feature_dict` (`curator_shadow.py:173-179`) iterates `for k in features` — **top level only** — for both the forbidden-value-key check and the declared-key allowlist, while the gate-decision check it delegates to (`_find_gate_decision_key`) *is* recursive. So `{"attribute": {"value_text": "SECRET"}}` passes both the value-key refusal (nested key never inspected) and the allowlist (top-level key `attribute` is declared). It then reaches `_encode`, where `attr.encode()` on a dict raises `AttributeError`, swallowed by the broad `except` in `_weights_for` (`:395`) → cold weights. Fails safe, by accident, one layer downstream of where it should fail. Confidence: VERIFIED.
- The allowlist is enforced on the **training** path (`train_weights`) and **not** on the **logging** path: `shadow_score_turn` writes `"features": {fid: feats ...}` into the epistemic record (`:439`) without ever calling `validate_feature_dict`. The one place the declared vocabulary is written to disk every turn is the one place it is not checked. Confidence: VERIFIED.

**Item 4 (shadow only, byte-identical prompt) — NOT blind. The best-constructed item.**
The prompt comparison is differential (same turn, `HIP_CURATOR_SHADOW=0` vs `=1`), and it stands next to a structural proof (the static scan at CS1 sub-check v). Fixture-chosen turns are a weak proof, but they are not the load-bearing one. Two real limits, both structural rather than assertive: the scan's file list is hard-coded to `server/voice_orch.py` and `harness/orchestrator.py` — a *third* module importing the scorer into a prompt path is invisible; and the regex `shadow_score_turn|harness\.curator_shadow` misses `from harness import curator_shadow as cs` (the text `harness import curator_shadow` matches neither alternative) unless the call site also spells `shadow_score_turn`. Same known-limitation class as the PS1 space-before-paren evasion already characterized in `harness_audit.py:266-276`, and it should be named the same way. Confidence: VERIFIED.

**Item 5 (every example through the MET gate) — NOT blind on the observable; BLIND on the label.**
The observable "the resulting weights are identical to a run where that example was never offered" is *differential* and is implemented as such (CS1 sub-check vi: `_cs_w_gated == _cs_w_clean` and `_cs_w_bypass != _cs_w_gated`). That is a genuinely good test and I would hold it up as the model.
But underneath it: the gate's V4 check is `example.get("label_source") != POST_GATE_LABEL` (`learner_isolation.py:243`), and the **only producer of training examples in this codebase stamps that field with the passing literal unconditionally** — `"label_source": POST_GATE_LABEL` at `curator_shadow.py:322`. V4 is now unfireable by construction. The label's actual provenance is the `outcome`/`admitted` content of `logs/turns_demo.jsonl`, and nothing verifies the label was in fact computed on post-gate outcomes. This is HOLE-1's exact structure — a trusted field, self-certified by the caller, checked for relationship rather than authenticity — reintroduced one layer above the gate that was fixed to stop doing it. Confidence: VERIFIED.
Also: `resolver` is a public keyword argument on both `check_training_example` and `check_training_batch` (`:221-223`, `:303-305`) and is forwarded straight through `train_weights` (`curator_shadow.py:327-341`). The "un-forgeable chain" is one keyword away from forgeable, and the battery's own `FixtureResolver` is the working proof-of-concept. See Q3.

**Item 6 (cold start) — the hypothesis PARTIALLY HOLDS, but there is a worse defect than the one hypothesized.**
Where the count comes from: `outcome_event_count(records)` over `logs/turns_demo.jsonl` (`curator_shadow.py:243-266`). So it is neither "config-supplied" (the hypothesis's bad case) nor derived from the server of record — it is derived from a **local, append-only, integrity-unprotected JSONL log, read whole, treated as one household by the module's own admission** (docstring, `:48-52`). That is weaker than the Neo4j+registry chain D-30 established as the standard for provenance, and it is the same channel that supplies the labels and the acceptance history. The test never exercises the derivation at all: CS1 passes `records=[]` directly, bypassing `load_records()` entirely. So the framing's instinct is right in structure and wrong in the specific mechanism. **PARTIAL HOLD.**

Two things I found here that are worse than the hypothesis:

1. **The threshold counts a population disjoint from the one that produces labels.** `outcome_event_count` counts records where `outcome.kind is not None` — that is `"correction"` **or** `"override"` (`harness/outcome_classifier.py:37-46`). But `build_training_examples` produces a `0` label only from corrections, because overrides carry no `target_fact_ids` (Stage 0's own named limit, `curator_shadow.py:285-295`). **100 overrides and zero corrections flips the regime to "trained" and hands `_fit_weights` an all-positive-label corpus.** With zeros init and `g = y - p > 0` every step (`:362-368`), the weights diverge monotonically for 200 epochs and produce an arbitrary ordering. There is no test for a single-class fit. Confidence: VERIFIED.
2. **The REQ's own sentence "The event count is the ONLY thing that may change which regime a household is in" is false in the built code.** If every example is gate-rejected, `train_weights` returns `dict(COLD_WEIGHTS)` (`:346-347`), and `_weights_for` then reports regime `"cold_start"` because `weights != COLD_WEIGHTS` is False (`:400`). Gate rejections are a second regime determinant. In production this is not hypothetical: the D-31b named limit means member-owned facts resolve `household=None` and are rejected, and most `admitted` entries in the record stream are member-owned. **The trained regime is currently unreachable on real data, and the code will report that as "cold_start."** The *behavior* is honest and safe; the *acceptance sentence* is not what the code does. Confidence: VERIFIED for the code path; INFERRED (high) for "most entries are member-owned," from the D-30 live smoke finding restated in the REQ.

**Item 7 (agreement metric) — BLIND in a specific and interesting way: the metric's denominator excludes its own failures.**
The hand-computed fixture (`curator_agreement.py:48-80`, expecting exactly `1.0 / 0.0 / 0.5 / None`) is textbook-correct discipline and I have no criticism of it. The problem is what the metric reads on real data. `shadow_outcome_agreement` skips any record where `len(ranking) < 2` (`:26-28`). When `validate_shadow_output` fires, `shadow_score_turn` suppresses the ranking to `[]` (`:429-432`) — so **exactly the turns where the invariant failed become invisible to the offline eval**. A self-measuring system whose failures delete themselves from its own score. Confidence: VERIFIED.
Separately: the two lookahead windows disagree. `build_training_examples` slices the raw stream first (`records[i+1:i+1+lookahead*3]`, then filters by member, then `[:lookahead]`, `:302-303`); `curator_agreement` filters the entire remaining stream then slices (`:30-31`). The metric is not measuring the same lookahead the labels were built from. Confidence: VERIFIED.

**Item 8 (the Four) — present and mechanically verifiable; see Q2 for why that is not reassuring.**
The registry entry declares `"twin": {"marker": (_L7C, "CS1 FAULT-INJECTION (red)")}`, `"fixture": {"marker": (_L7C, '"fact_id": "cs-f1"')}`, a four-key coverage dict, and `"metamorphic": {"probe": "cs1_query_reword"}`. All four will verify green under `_verify_ref` / `_verify_coverage`. The coverage entry is unusually honest — it names the trained regime as untested on a real graph, names `key_scope` as coarse, names the recency-as-rank deviation. It still has no slot in which to say "item 2's assertion is vacuous," because no such slot exists.

**Item 9 (audit + ratchet)** — process item, not a methodology question. Noting only that `--full` is again deferred (TD-129 memory guard), the second consecutive build in this REQ chain to defer it; that is Bill's call, not mine, and it is named rather than glossed.

### The generalization worth keeping

Sorting the nine items by *test shape* rather than by subject matter separates them cleanly:

| Shape | Items | Exposure to the D-25 defect |
|---|---|---|
| Differential (two runs, one variable) | 4 (prompt bytes on/off), 5 (weights with/without), 3-fixture (value-blindness) | **Immune.** There is no authored expected value to forge. |
| Structural (property of the code graph) | 4-scan, 3-import-grep (*specified, not built*) | **Immune to forgery, exposed to scope** — the scan's file list is the attack surface. |
| Assertive (output vs authored value) | 1, 2, 6, 7-fixture | **Exposed.** Item 2 is fully vacuous; 6 bypasses its own derivation; 1's decoy population is absent. |

That is the recommendation in one line: **for a security-relevant invariant, prefer a differential or structural proof; where an assertive test is unavoidable, the authored value must arrive through a channel the caller demonstrably cannot reach, and the check must say which channel that is.**

---

## Question 2 — Is the Four sufficient?

**No — but the framing's proposed remedy ("add an adversarial test as a fifth artifact") would not have worked, and I want to argue that before proposing anything.**

### First, the counter-argument, stated fairly

There is a real case that D-23 was an execution failure, not a standard failure. The original `REQ_LEARNER_SIGNAL_ISOLATION` did not ask for authenticity — D-26's own retrospective (lines 107-120 of that REQ) says the acceptance test "verified the relationship logic, not that provenance is trustworthy," and D-29 had to *add* the authenticity requirement afterward. If the requirement did not demand it, no check discipline was going to conjure it. On that reading, the Four did its job — it forced four artifacts that all told the truth about a check that was answering the wrong question, and the wrong question came from the REQ.

I take this seriously. It is partly right: the REQ under-specified, and the Four is not a requirements-elicitation tool.

### Why it is nonetheless a standard failure

Two pieces of evidence move me off the pure-execution reading.

1. **The coverage entry could not have expressed the gap.** `_COVERAGE_KEYS = ("roles", "scopes", "attribute_splits", "intent_classes")` (`harness_audit.py:54`), and `_verify_coverage` accepts any non-empty list per key (`:629-633`). Every axis in that schema is an axis of the *authorization state space* — who, which scope, which attribute, which intent. There is no axis for "what this check assumes about the honesty of its inputs." The D-23 entry (`git show 487b38b:eval/harnesslib/check_registry.py`) did the right thing within the schema: it named the unfixtured pair/care-team roster slice explicitly rather than hiding it. It scored the honest maximum available and still could not surface the actual gap. **A gap the schema cannot express is a standard gap, not an execution gap.** This is the direct answer to "why did the coverage entry not help."

2. **The blind spot reproduced under the same standard, with a different author, one week later.** Item 2's vacuous assertion in the uncommitted CS1 build is not a memory lapse — it is what a careful engineer produces when the standard says "assert the invariant" and says nothing about the channel the asserted value arrived through. One occurrence is execution. Two occurrences under the same standard, in the same repo, in adjacent dispatches, is the standard.

### Why "add an adversarial battery" is not a valid fifth artifact

The mechanical contract in `harness_audit._verify_ref` (`:582-620`) is strict and good: a `marker` must be a literal actually present in the named file; a `probe` must exist in `PROBES` **and have run green this run**; a `scenario` must be in the enumerated roster; a `debt` must match `_DEBT_ID_RE`; anything else is `MISSING`. Adversariality cannot be expressed in that contract. You can verify that a battery file exists and ran green — and a green battery proves exactly nothing about what it did not try. That is the Four's own failure mode reproduced one level up, and it would be worse than the disease, because a green "adversarial" column would read as coverage.

### What I propose instead — two options, ranked, both mechanically verifiable with zero new primitives

**Option A (recommended, cheapest): add a fifth required coverage key, `trust_boundary`.**
A one-token change to `_COVERAGE_KEYS` at `harness_audit.py:54`. `_verify_coverage` already requires each key to be a non-empty list, so the enforcement is free and identical to the existing four. Each check must then declare, in prose the auditor can print, **which of its inputs are derived from state the caller cannot forge, which are caller-supplied, and what happens when a caller-supplied one lies.** Applied to D-23, the honest entry would have read: *"household_id and audience are caller-supplied; the check validates their relationship to the target, not their authenticity; forgery is uncovered."* That entry would have been printed on every single run, in front of everyone, before the MET.
Cost, stated plainly: this turns all 59 registry entries red until each declares. That is a forced sweep — which is the point, and also the reason it should be Bill's call and not a session's.

**Option B (more targeted): split the `twin` artifact into two verified kinds.**
The registry entry becomes `"twin": {"relationship": <ref>, "trust": <ref>}`, and `_verify_ref` runs unchanged on each — markers must be real literals, probes must be green. A **relationship twin** is what exists today: honest data, wrong relation (D-23's pooling and scope twins). A **trust twin** supplies a *hostile value through the channel the caller controls* and must go red (D-30's authenticity and currency twins are exactly this — they already exist, they just have no name). Where a check genuinely has no caller-controlled input, `{"na": "..."}` is a valid declaration and the auditor prints it. This fixes the artifact that was actually vacuous rather than adding a fifth one, and it is strictly within the existing verification contract.

**On the choice:** Option A makes the assumption *visible*; Option B makes it *falsifiable*. They are complementary and the honest recommendation is both, A first (cheap, immediate, sweeps the whole roster) and B second (expensive, and only worth doing after A reveals how many checks actually have a caller-controlled input).

**The limit of any such proposal, stated so it is not oversold:** a mechanical audit can force a *declaration* and verify a *named artifact*. It cannot force the declaration to be complete. Neither can the existing coverage entry, which has been carrying that same limitation for four months and is still worth having. This converts an invisible assumption into a visible one. It does not make anyone right.

### And the enforcement gap that dwarfs both options

`eval/test_learner_isolation_adversarial.py` — the artifact that found all six holes — is **not enforced by anything** (VERIFIED: absent from `enumerate_roster`'s two scanned files and from `record_invariants.CHECKS`; absent from `check_registry.REGISTRY`; no `pytest` invocation in `eval/harness.py`, `scripts/run_harness.sh`, or anywhere in `scripts/`; no Makefile, no CI). Its 23 security-correct expectations, including the 6 that encode the holes, can regress to green-by-deletion without a single run turning red. **The most valuable test in this repository is the least protected one.** Fixing that requires no new standard at all — it requires wiring, and it is the highest ratio of safety to effort available here.

---

## Question 3 — Attack classes absent from the battery

Ordered by what I would build first. Each is labeled **IN SCOPE** (a per-example gate can and should address it) or **OUT OF SCOPE BY CONSTRUCTION** (a per-example gate cannot see it; the honest move is a named uncovered region, not a test). I have tried hard not to blur that line, since the framing correctly identifies blurring it as how a coverage entry becomes a lie.

### IN SCOPE — the gate can address these, and does not

**3.1 Target forgery — the mirror image of HOLE-1/HOLE-2. (No case in the battery. Highest severity.)**
D-30 authenticated the example. The target was never touched. `target["household_id"]`, `target["audience"]`, and `target["model_id"]` are read directly from the caller's dict (`learner_isolation.py:260, 285`) with no derivation, no registry lookup, and no binding between `model_id` and `audience`. Cases a1/a2 forge the example's provenance; **nothing forges the target's.** Concretely: declare a target whose `audience` is narrower than the model's real readership and every V2 check passes while the artifact is read by people outside the declared set. The gate validates a *derivation* against a *declaration* and authenticated only one of them.

**3.2 Empty target audience as a universal V2 bypass. (Adjacent case e3 exists and is marked "acceptable"; the asymmetric case is untested.)**
`if ex_aud is None or tgt_aud is None` (`:286`) fails closed on None. `frozenset()` is not None, so an empty target audience proceeds to `frozenset() - ex_aud` = ∅ → no unauthorized readers → **admissible for every example in the household, including member-private ones** (`:292-293`). Case e3 tests empty-on-both-sides and reasonably calls it vacuous; nobody tested narrow-source/empty-target. Combined with 3.1 this is a one-line universal bypass of the entire intra-household scope check. This is the closest thing to a seventh hole in the current gate. VERIFIED.

**3.3 Resolver substitution.**
`resolver` is a public keyword parameter defaulting to the production resolver (`:221-223`, `:303-305`), forwarded verbatim by `train_weights` (`curator_shadow.py:329, 341`). Any caller in any module can pass a fixture resolver and receive whatever provenance it likes; `FixtureResolver` in the battery is the working exploit. Testable exactly the way CS1's prompt-touch scan already works: a static scan asserting no non-test module passes `resolver=` to either gate entry point. (The scan must allow `eval/` — `layer7_crypto.py`'s CS1 legitimately injects one.)

**3.4 Time-of-check-to-time-of-use against the live roster.**
`RegistryProvenanceResolver` reads the roster fresh per example (`:177-195`) with no epoch, no version, and no caching. A 10,000-example batch performs 10,000 independent roster reads; a revocation mid-batch means the early examples were validated against a roster that no longer exists, and the fit consumes all of them. D-25's HOLE-6 fixed *staleness of a caller snapshot*; it did not address *drift within a validation window*. IN SCOPE and fixable with the mechanism `REQ_PARTITION_CUSTODY` already ratified: read the roster epoch once, re-read after the fit, discard on mismatch. Currently untestable because no epoch is surfaced.

**3.5 Label-source authenticity.**
Covered above (item 5): V4 is unfireable because the sole example producer hard-codes the passing literal (`curator_shadow.py:322`). Testable as a differential: build examples from a record stream whose `outcome` blocks were tampered with, and assert the labels change / the batch is refused.

**3.6 Type confusion on rosters — still open, and D-25 already flagged it as luck.**
Case e6's note says it plainly: "blocks here, still not a type check." The D-30 fix added no `isinstance` guard; `frozenset(tgt_aud) - frozenset(ex_aud)` (`:292`) will happily decompose a string into characters. Now that the target audience comes from `list_circle_members()` rather than a test literal, the failure mode is a silent semantic change rather than a visible test artifact. Two lines to fix, one case to add.

**3.7 Cross-household pooling through the *scoring* path, which the gate does not sit on.**
This is the one I would most want re-read by someone else, because it is a real architectural finding rather than a test gap. `acceptance_history(recs)` (`curator_shadow.py:269-280`) pools `injected_fact_ids` and correction targets across **every record in the log**, and the resulting dict is passed into `score_facts` for the current turn (`:422-423`). Likewise `_WEIGHT_CACHE` is keyed on `n_events // 50` **only** — not on household, not on target — and the training target is always built from `DEFAULT_HOUSEHOLD_ID` (`:374-400`). The isolation gate governs the *training example* path and has no visibility into either. Today this is latent: one household, one log, and the module names it as a *scaling* limit ("the outcome-event count treats the whole log as one household"). **It is not a scaling limit. It is an isolation limit, and it should be reclassified as one in the coverage entry.** The moment a second household exists, household B's turn reads household A's cached weights and A's pooled acceptance statistics, and every per-example gate in the codebase passes green while it happens.

### OUT OF SCOPE BY CONSTRUCTION — name these as uncovered regions; do not write per-example tests for them

**3.8 Differencing / composition across model artifacts.** Train M1 on a household's corpus and M2 on the same corpus minus one member's contributions; the difference discloses that member. Every example in both fits is individually admissible and correctly gated. A per-example gate cannot see a relation between two artifacts. This needs a *model-lifecycle* invariant (no two models over overlapping audiences from one corpus; or a formal disclosure bound), not a gate case. Name it.

**3.9 Aggregate poisoning / denial-of-truth.** A member who can trigger corrections at will drives `historical_acceptance` for a true fact toward 0 and — at Stage 3 — gets it demoted out of the prompt. Every training example is provenance-clean and gate-admissible. The gate is per-example; the attack is distributional. Harmless in shadow, principal at Stage 3. Name it as an uncovered region **and** as a Stage-3 entry blocker.

**3.10 Gradient/weight-level leakage.** Ten metadata features and a linear fit have negligible memorization capacity, so I rate the classic form of this low-risk here (INFERRED, medium-high confidence). But the *logged* artifact is a different matter and is not out of scope: `shadow_score_turn` writes the full per-fact feature dict for every admitted fact of every turn into `logs/turns_demo.jsonl` (`:439`), unvalidated (see item 3 above), and the same build added `sensitivity` and `write_state` to `_fact_entry` (`epistemic_record.py:96-97`) — which is shared with the **denied**-fact path via the `deny_reason` parameter (`:115-116`). So metadata about facts the requester was *refused* now includes their sensitivity classification. The marginal disclosure over what the record already carried is small, but it is a new surface added by a build whose acceptance criteria never mention the log's contents. Name it; consider bounding it.

**3.11 Statistical inference across individually-clean examples.** With ten coarse metadata features this is weak in the abstract — but see 3.7, which is the concrete instance and *is* in scope because it flows through an identifiable code path rather than through the model.

---

## Question 4 — How the shadow scorer should be tested differently

The tree is uncommitted; all of this can still land in the build rather than in a follow-up dispatch. Ordered by value, with the D-25 question answered for each.

**4.1 Make item 2 non-vacuous by moving the assertion across a boundary.**
Today `validate_shadow_output` compares two views of one local variable. Instead, assert the invariant against the *record*, not the *call*: after `build_epistemic_record` produces the turn's record, check `set(rec["curator_shadow"]["ranking"]) ⊆ {e["fact_id"] for e in rec["admitted"]}`. Those two now travel through different code paths — `admitted` via `_fact_entry` projection, `ranking` via the scorer — so the assertion can actually fail, and it will catch precisely the Stage-3 class of bug where the two drift. This is also the natural home for it as a **Layer-6 record invariant** (`eval/oracle/record_invariants.CHECKS`), where G1-G4 already live, where `enumerate_roster` already picks checks up automatically, and where `_probe_record_invariant_twins` already establishes the red/green fixture pattern. Cost: small. Value: converts the REQ's flagship invariant from decorative to real.

**4.2 Wire the adversarial battery into the roster before adding anything else.**
Independent of the scorer, and the single highest-value change available. Options, cheapest first: (a) an `AUDIT`-category `Scenario` that imports `CASES` from `eval/test_learner_isolation_adversarial` and asserts all 23 verdicts — it enters `enumerate_roster` automatically via the `Scenario(...)` AST scan, needs a `check_registry` entry, and can carry its own fault twin trivially (flip one expectation, see red); or (b) a `harness_audit` probe, which gets green-this-run verification for free via `_verify_ref`'s probe branch. Then do the same for CS1's battery when it exists. **A battery nobody runs is a document, not a test.**

**4.3 Add a target-forgery and empty-audience block to the battery (findings 3.1/3.2), and re-run the scorer against it.**
Minimum cases: (i) target household matches but target `audience=frozenset()`, member-private source → must be a violation; (ii) target `audience` understating the model's real roster → must be a violation, or the concept "declared audience" must be documented as unenforceable and named as an uncovered region; (iii) `model_id` not bound to any registered model → refusal. Case (i) is a two-line addition and, on my reading of `learner_isolation.py:286-293`, will fail today. **I am not proposing a verdict on what that means for any REQ's status — only that the case be run.**

**4.4 Fix the label tautology at the producer, not the gate (finding 3.5).**
`build_training_examples` should not stamp `label_source`. Either derive it from the record (e.g. `post_gate_outcome` only when the record carries a classified `outcome` block and the fact appears in `admitted`, else a value the gate rejects), or have `train_weights` verify the claim against the record rather than accept it. Then add the differential twin: tamper with a record's `outcome`, assert the label changes or the example is refused. As it stands, the codebase's only V4 test is in LI1's scenario using hand-authored examples — the composition is untested.

**4.5 Make the cold-start threshold measure the population it claims to (finding on item 6).**
Two independent problems, both small fixes: count *corrections* (the events that actually produce labels) for the threshold, or count both and add a separate guard that refuses to leave cold start on a single-class corpus; and state the regime honestly when gate rejections empty the batch, rather than reporting `cold_start` for what is really `trained_but_no_admissible_data` (`:346-347`, `:400`). Add the missing test: a fixture at 150 override-only events must **not** silently produce diverged weights. There is no such case today.

**4.6 Enforce the declared vocabulary where it is actually written (finding on item 3).**
Call `validate_feature_dict` on the dict `shadow_score_turn` logs, not only on the one `train_weights` consumes — and make the allowlist recursive, matching `_find_gate_decision_key`'s existing depth. Add the structural check item 3 specified and the build skipped: a scan asserting `harness/curator_shadow.py` imports nothing from the decrypt path. That is a marker-style check, mechanically verifiable by `_verify_ref` exactly as written.

**4.7 Repair the agreement metric's self-erasure and its lookahead disagreement (finding on item 7).**
Suppressed turns must count against the metric or be reported separately with an explicit count — a failed invariant must never be able to improve the score by leaving the denominator. And reconcile the two lookahead windows (`curator_agreement.py:30-31` vs `curator_shadow.py:302-303`) so the metric grades the same window the labels were built from, or document why they legitimately differ.

**4.8 Write the coverage entry against the trust axis now, whether or not the fifth key lands.**
The CS1 coverage entry is already the most honest in the registry. It should additionally say, in prose: which inputs are server-derived (the example's provenance, via the resolver) and which are caller-supplied (the target dict; the record stream; the `resolver` parameter itself); and it should reclassify the whole-log pooling of `acceptance_history` and `_WEIGHT_CACHE` from a *scaling* limit to an **isolation** limit (finding 3.7). That reclassification costs nothing today and is the difference between a coverage entry and a lie the day a second household exists.

**4.9 Name 3.8 and 3.9 as uncovered regions and as Stage-3 preconditions.** Do not write per-example tests for them. A per-example gate cannot see a relation between two artifacts or a distribution over many turns, and pretending otherwise is worse than silence.

---

## Ranked findings

| # | Finding | Where | Confidence |
|---|---|---|---|
| 1 | **The blind spot has already repeated.** Item 2's `curated ⊆ admitted` in-path assertion compares two derivations of one local variable and cannot fire; the scenario comment concedes it. The REQ's flagship "asserted, not assumed" invariant is decorative. | `harness/curator_shadow.py:421-427` | VERIFIED |
| 2 | **The adversarial battery is enforced by nothing.** Not in `enumerate_roster`, not in `check_registry`, never invoked by `eval/harness.py`, `run_harness.sh`, any Makefile, or any CI (none exist). All 23 security-correct expectations can regress silently. | `eval/test_learner_isolation_adversarial.py`; `harness_audit.py:59-93`; `eval/harness.py` | VERIFIED |
| 3 | **D-30 authenticated only the example side.** The target's `household_id`, `audience`, and `model_id` are caller-supplied with no derivation and no binding; the battery has zero target-forgery cases. HOLE-1 has an unexamined mirror image. | `harness/learner_isolation.py:260, 284-292`; battery cases a1/a2 | VERIFIED |
| 4 | **Empty target audience is a universal V2 bypass.** `frozenset()` is not `None`, so the fail-closed branch is skipped and every household example — including member-private — is admitted. Case e3 tests the symmetric case and calls it acceptable; the asymmetric case is untested. | `harness/learner_isolation.py:286-293`; battery case e3 | VERIFIED |
| 5 | **The Four's coverage schema has no trust axis.** `_COVERAGE_KEYS` is a fixed 4-tuple over the authorization state space, verified only for non-emptiness. D-23's coverage entry could not have named its own trust assumption. This is a standard gap, not only an execution gap. | `harness_audit.py:54, 623-633`; `487b38b:check_registry.py` L7:LI1 | VERIFIED |
| 6 | **V4 (`label_source`) is now unfireable.** The only training-example producer stamps the passing literal unconditionally — a trusted, self-certified caller field, checked for relationship not authenticity. HOLE-1's structure, one layer above the gate that was fixed to stop doing this. | `harness/curator_shadow.py:322`; `learner_isolation.py:243` | VERIFIED |
| 7 | **Cross-household leakage lives on the scoring path, where no gate sits.** `acceptance_history` pools the entire log; `_WEIGHT_CACHE` is keyed on event count alone, not household; the target is always `DEFAULT_HOUSEHOLD_ID`. Currently classified as a *scaling* limit. It is an *isolation* limit. | `harness/curator_shadow.py:269-280, 374-400` | VERIFIED (latent today: one household) |
| 8 | **The cold-start threshold counts events that produce no labels.** Overrides increment the count but yield no `0` labels, so 100 overrides flip the regime into a single-class logistic fit with diverging weights. No test exists for a single-class corpus. | `curator_shadow.py:262-266, 285-295, 362-368`; `outcome_classifier.py:37-46` | VERIFIED |
| 9 | **"The event count is the ONLY thing that may change which regime a household is in" is false in the built code.** Gate rejections empty the batch → `COLD_WEIGHTS` → reported as `cold_start`. Safe behavior, wrong acceptance sentence — and in production the trained regime is currently unreachable via the D-31b data limit. | `curator_shadow.py:346-347, 400`; REQ item 6 | VERIFIED (code); INFERRED-high (production reachability) |
| 10 | **The resolver is one keyword argument from forgeable.** `resolver=` is public on both gate entry points and forwarded by `train_weights`; the battery's own `FixtureResolver` is the working exploit. No scan restricts it to test code. | `learner_isolation.py:221-223, 303-305`; `curator_shadow.py:329, 341` | VERIFIED |
| 11 | **The declared feature vocabulary is enforced on the training path and not on the logging path**, and the allowlist is top-level-only while the gate-decision ban it delegates to is recursive. Nested value keys evade both and fail on a downstream `AttributeError` swallowed by a broad `except`. | `curator_shadow.py:173-179, 439, 395` | VERIFIED |
| 12 | **The agreement metric excludes its own failures from its denominator.** Suppressed rankings become `[]`, and `len < 2` skips them — failed invariants improve the score by disappearing. The metric's lookahead also disagrees with the one that built the labels. | `curator_agreement.py:26-31`; `curator_shadow.py:302-303, 429-432` | VERIFIED |
| 13 | **TOCTOU against the live roster within a batch.** Per-example fresh roster reads, no epoch, no version; a revocation mid-batch leaves earlier examples validated against a roster that no longer exists. `REQ_PARTITION_CUSTODY` already ratified the epoch mechanism the gate does not use. | `learner_isolation.py:177-195` | VERIFIED (mechanism); INFERRED (exploitability) |
| 14 | **Two of item 3's and item 1's specified observables were not built:** no decrypt-path import scan, and no out-of-admitted-set decoy population in the CS1 fixture (the escapee is a synthetic string). | CS1 diff in `layer7_crypto.py`; REQ items 1, 3 | VERIFIED |
| 15 | **Type confusion on rosters remains open**, exactly as D-25 case e6 flagged it ("blocks here, still not a type check"); D-30 added no `isinstance` guard, and the roster now comes from live tables rather than test literals. | `learner_isolation.py:292`; battery case e6 | VERIFIED |
| 16 | **The static shadow-cannot-act scan is scoped to two hard-coded files** and to literal spellings; a third module, or `from harness import curator_shadow as cs`, is invisible to it. Same known-limitation class as PS1's space-before-paren evasion, and should be characterized the same way. | CS1 sub-check (v); `harness_audit.py:266-276` for the precedent | VERIFIED |
| 17 | **Additive metadata disclosure went unexamined:** `sensitivity` and `write_state` were added to `_fact_entry`, which is shared with the denied-fact path, so sensitivity classifications for *refused* facts now reach the plaintext log. Small delta, zero acceptance coverage. | `epistemic_record.py:92-97, 115-116` | VERIFIED |

**Not proposed, deliberately:** no REQ status change of any kind. Findings 3, 4, 6, and 15 concern `REQ_LEARNER_SIGNAL_ISOLATION`, which is MET by Bill's D-31b ruling; findings 1, 8, 9, 11, 12, and 14 concern an unassessed in-flight build. What to do with any of them is the project owner's call, not this review's.

---
---

# REVIEW 2 of 2 — CODE REVIEW

*Reproduced verbatim as Fable returned it. Unverified by the routing session.
Scorer findings (Part 2) are pinned to the 07:42 MDT snapshot, which was
afterwards confirmed byte-identical to the code D-33 committed at `9d867f8` —
so where the reviewer hedges that its scorer findings "may already be stale,"
that hedge is now known not to apply.*

---

# Adversarial Code Review — Learner Isolation Gate (D-30) and Curator Shadow Scorer (D-33 snapshot)

**Reviewer:** independent read-only adversarial review
**Repo:** `[REDACTED-USER-PATH]/hip-roadmap`, branch `roadmap`, commit `49bc332`
**Gate reviewed at:** committed state (`harness/learner_isolation.py`, unmodified by the in-flight build); registry entry read via `git show 49bc332:eval/harnesslib/check_registry.py`
**Scorer reviewed at:** the pinned 07:42 MDT 2026-07-30 snapshot in `/private/tmp/claude-501/-Users-bill-ai/5a15f620-ad25-4f90-8ab4-689effe0621f/scratchpad/d33_snapshot_0742/`. Every scorer finding below is against that snapshot and may already be stale.
**Nothing was written, run, or executed.** No harness, no pytest, no git write. All findings are from reading source.

---

## Headline conclusion

**There is a seventh hole, and it is the same root cause as the first six.**

D-25 found that the gate validated the *relationship* between caller-supplied fields and the target, never their *authenticity*. D-30 fixed that for exactly one field: `household_id`/`audience` on the example. It did not fix it for the other two things the caller supplies.

1. **The gate never binds the payload to the provenance.** `check_training_example` authenticates `example["fact_id"]` and then authorizes `example["features"]` — two independent, caller-controlled keys with no checked relationship between them. A hostile learner takes an honest, resolvable, same-household fact_id and attaches the *features of a different fact* — a member-private one, a dyad-private one, another household's — and the gate returns `None`. No forgery, no unresolvable id, no resolver override. The gate's guarantee is "this **fact_id** may train this model." The learner's need is "this **example** may train this model." The unchecked gap between those two sentences is the whole exploit.

2. **The target side of the comparison is still entirely caller-asserted.** D-30 derived the example's household and audience. It left `target["household_id"]` and `target["audience"]` exactly as D-25 found the example side: stamped by the caller, never derived, never verified. `audience=frozenset()` is vacuously authorized against every scope in the household.

Both are structurally invisible to the 23-case battery — not "the battery happens to miss them," but *the battery cannot express them*. Every case builds features from one constant helper (`_ex`, line 101) and hand-writes honest target dicts. Features are inert scenery in all 23 cases; targets are ground truth by construction. The battery's design encodes the assumption that both are trustworthy.

Beyond those two, one certain code defect in an untested production branch (the dyad audience derivation reads four column names that do not exist in the `dyads` schema) and one certain latent multi-household collapse (`_household_of` maps every household-owned fact to the literal string `"default"`).

On the scorer snapshot: **the shadow-placement claim holds** — I verified tree-wide that `shadow_score_turn` has exactly one production reference, inside the record-emit closure, after the reply exists. The value-blindness claim holds by construction. The cold-start byte-identical claim holds. The most serious scorer issue is not a security hole but a modelling defect: **in the trained regime the fit will systematically invert recency**, because labels are near-all-positive, there is no intercept term, and `recency` is an unnormalized unbounded rank.

---

# PART 1 — GATE FINDINGS (definitive; committed code)

## G-1 — CRITICAL — Provenance is authenticated; the payload it authorizes is not bound to it

**Class:** genuine exploitable hole. **Confidence:** high — this is a direct read of the control flow, not an inference.

**File/lines:** `harness/learner_isolation.py:221-300`. Specifically: `fact_id` is read at line 252 and used only at line 253; `features` is read at line 236 and used only for the denylist scan. Nothing correlates them, anywhere.

**Trigger:**

```python
check_training_example({
    "example_id": "x",
    "fact_id":    <any resolvable fact_id whose scope is the target's own circle>,
    "features":   <feature dict derived from a member-private or dyad-private fact>,
    "label_source": "post_gate_outcome",
}, {"model_id": "curator-h1-house", "household_id": H1, "audience": CIRCLE1})
# -> None (admissible)
```

Walk it: V3 passes (no denylisted key). V4 passes (correct string). V0 resolves the fact_id to `Provenance(H1, CIRCLE1)` — genuine, live, un-forged. V1 passes: `H1 == H1`. V2 passes: `CIRCLE1 - CIRCLE1 = ∅`. Returns `None`. Alice's private medication signal is now in the household-circle model's gradient, and every check the gate performed was performed correctly on a fact that has nothing to do with the data in the example.

**Security consequence:** the intra-household scope crossing — violation class (b), one of the four crossings the module exists to catch — is reachable with zero forgery. The cross-household form needs one resolvable fact_id belonging to the target household, which any caller operating in that household has. The public carve-out form is worse and unbounded: `fact_id=<any public fact>` + arbitrary features → line 265 returns `None` for **any** target including the shared base, before the household check ever runs. That form is not reachable today (see D-2 in "did not break"), but it is the day the marker becomes writable.

**Would the battery catch it?** **No — structurally cannot.** All 23 cases route through `_ex()` (line 101), which hard-codes `features={"attribute": "medication", "trust_rung": 2}` for every case. Not one case varies features independently of fact_id. Case `e1` is the only exception (`{"a": 1}`) and it varies neither. The battery's model of an example is "a provenance pointer plus decoration," so the question "does the decoration match the pointer?" cannot be asked in its vocabulary. Adding cases will not fix this; the fixture shape has to change.

**Corroborating evidence from the in-flight work:** the D-33 CS1 twin (snapshot diff, `layer7_crypto.py` section vi) constructs `_cs_bad = dict(_cs_exs[0], example_id="cs-t:cs-x", fact_id="cs-x", label=0)` — an example carrying **cs-f1's features under cs-x's fact_id**. The twin relies on the gate catching it, and the gate does — but only because `cs-x` resolves to a foreign household. Flip the two fields (keep the honest fact_id, swap the features) and the identical construction is admitted. The codebase already treats "build an example by pasting a different fact_id onto an existing feature dict" as a normal idiom.

**What would close it (owner's call, not a proposal to build):** the binding has to be server-side — the gate deriving features from the fact_id itself, or a server-computed digest over the fact's metadata captured at extraction time and re-checked at gate time. The scorer already owns a deterministic, value-blind extractor keyed on the fact dict, so the shape exists in-repo.

---

## G-2 — HIGH — The target's household and audience are caller-asserted; D-30 fixed one side of a two-sided comparison

**Class:** genuine exploitable hole (same root cause as HOLE-1/HOLE-2, mirrored). **Confidence:** high.

**File/lines:** `harness/learner_isolation.py:260` (`tgt_hh = target.get("household_id")`) and `285` (`tgt_aud = target.get("audience")`). Neither value is ever derived, resolved, or cross-checked against `target["model_id"]`.

**Trigger — the vacuous-audience form:**

```python
target = {"model_id": "m", "household_id": H1, "audience": frozenset()}
```

`unauthorized = frozenset() - frozenset(ex_aud) = ∅` → line 300 returns `None` for **every** H1-scoped example: alice-private, bob-private, dyad-private, care-team, circle. One declared field pools every scope in the household into one model. The model's actual readership is whatever the operator wired up; the gate only ever saw the string the caller typed.

**Trigger — the narrowed-audience form:** declare `audience=frozenset({"alice"})` and every H1 example whose derived audience contains alice is admitted, including household-circle facts and, via any scope alice belongs to, signals she is the only authorized reader of — then serve the model to the whole circle. The battery *blesses* this direction: case `c3` ("broader→narrower allowed, MUST pass") is exactly the narrowing move, treated as safe because in the fixture the declared narrow audience is true.

**Trigger — the household form:** set `target["household_id"]` to the example's derived household and V1 passes unconditionally. The example's household is now unforgeable; the target's is a free variable, so the *comparison* is still under caller control from one end.

**Security consequence:** the gate reduces to "a caller may train any model on any example, provided the caller describes the model honestly." That is precisely the property D-30 removed from the example side and left in place on the target side. The docstring (line 65) describes `target["household_id"]` as "operator config," which is the only place this trust assumption appears — and `audience` gets no such note at all. It is an unnamed trust boundary.

**Would the battery catch it?** **No — structurally cannot.** All five targets (lines 94-98) are hand-written module constants whose audiences are, by construction, the truth. The FixtureResolver is described in-source as "the human-verified oracle: the caller cannot influence it" — and it resolves *examples only*. There is no oracle for targets, and no case supplies a dishonest one. Note also that no case tests a **non-empty source audience against an empty target audience**: `e3` tests empty-on-both-sides and declares it acceptable, which is a different and much weaker statement than the one the code actually makes.

**Asymmetry worth naming:** a `ModelResolver` (model_id → true readership) is the exact mirror of `ProvenanceResolver` and does not exist. Until it does, "the gate does not trust the caller for provenance" is true of one operand.

---

## G-3 — HIGH — `_household_of` collapses every household-owned fact to the literal string `"default"`

**Class:** genuine hole, latent-but-certain (needs a second household to fire). **Confidence:** high — verified the constant.

**File/lines:** `harness/learner_isolation.py:169-175`. `harness/member_registry.py:52`: `DEFAULT_HOUSEHOLD_ID = "default"`.

**Trigger:** any deployment with more than one household. Every `owner == "household"` fact — from *every* household — derives to `Provenance(household_id="default", audience=frozenset(list_circle_members("default")))`. Two consequences chained:

- **V1 is defeated by construction.** Household B's household-owned fact and a household-A model both carry `"default"`. `ex_hh != tgt_hh` is False. Cross-household pooling — the primary crossing the gate exists to catch — passes.
- **V2 is defeated too.** The derived audience is the circle of `"default"`, not of the fact's real household, so the containment check compares the target's readers against the wrong roster in both directions.

The surrounding schema is multi-household-ready and this code is not: `household_circle_members` is keyed by `household_id` (`harness/household_keys.py:180-182`), `dyads` carries a `household_id` column, and `members` is expected to carry `household_id` (that is exactly the D-31b limit). The resolver simply never asks which household. Note the sibling branch does ask: `get_member_by_id(owner)['household_id']` is the correct, per-household lookup — the household axis is the one case that hardcodes.

**Security consequence:** on the first multi-household deployment, the gate silently returns `None` for cross-household pooling of household-scoped facts. This is a fail-*open* on the exact case the module was built for, and it will produce no violation string, no log line, and no test failure.

**Would the battery catch it?** **No — structurally cannot.** All 23 cases inject `FixtureResolver`; `RegistryProvenanceResolver` is never constructed or executed by any case. The L7:LI1 coverage entry is honest about this ("the RegistryProvenanceResolver's LIVE reads against a real seeded graph are exercised by-construction/by the fixture, not yet by a live graph"), but the entry frames it as a *coverage* gap. It is not only a coverage gap — there is a defect sitting in the uncovered code.

---

## G-4 — HIGH — The dyad audience branch reads four column names that do not exist; every dyad-private fact derives an EMPTY audience, and the branch has no currency filter

**Class:** genuine defect, certain. **Confidence:** high — verified against the schema DDL.

**File/lines:** `harness/learner_isolation.py:181-188`:

```python
d = get_dyad(dyad_id)
if not d:
    return None
members = {d.get("member_a"), d.get("member_b"),
           d.get("caregiver"), d.get("recipient")}
return frozenset(m for m in members if m)
```

`get_dyad` is `SELECT * FROM dyads` (`harness/dyad_registry.py:117-122`). The `dyads` schema (`harness/dyad_registry.py:70-77`) is:

```
dyad_id, recipient_ref, household_id, dyad_pubkey, status, created_at
```

**None of `member_a`, `member_b`, `caregiver`, `recipient` is a column.** The actual custodians live in a *different* table, `dyad_members` (`custodian_member_id`, `role`, `added_at`, `removed_at`), which this branch never reads. Even `recipient_ref` — the one real column with a near-miss name — is missed, because the code asks for `recipient`.

**Two independent consequences:**

1. **Every dyad-private fact derives `audience == frozenset()`.** Empty is not `None`, so the fail-closed check at line 286 does **not** fire. Instead `unauthorized = frozenset(tgt_aud) - frozenset()` = the entire target audience. Against a normal target that blocks — over-strict, with a violation string that names *every* reader as unauthorized and asserts a "live source audience []" that is a fabrication, not a derivation. Against a target declaring `audience=frozenset()` (see G-2) it **admits** — dyad-private data, the most tightly partitioned class in the system under REQ_PARTITION_CUSTODY, trains a model whose declared readership is empty.

2. **No currency filter — HOLE-6 reintroduced in this branch.** `get_dyad(dyad_id)` returns the row regardless of `status`. Its two siblings in the same module both filter (`get_active_dyad_for` requires ACTIVE; `get_dyad_for_recipient` requires `status = 'active'`), and the two *other* audience branches both bind to live tables (`list_caregivers` filters `removed_at IS NULL`; `list_circle_members` filters `removed_at IS NULL`). The dyad branch filters on nothing. Even after the column names are corrected, a custodian who has **exited custody** would remain in the derived audience — the precise currency failure D-30 was built to close, in the one branch nothing exercises.

**Would the battery catch it?** **No — structurally cannot.** Same reason as G-3: no case runs the production resolver. The registry entry names dyad derivation as uncovered; that named gap is concealing two live defects, not a hypothetical risk.

**Secondary observation on the same function:** branch selection at lines 181-195 is by **property presence** (`if dyad_id:` … `if recipient_ref:` …), not by the fact's visibility class. The docstring at line 118 says "audience ← the fact's **visibility class** → LIVE roster." The write path (`memory_engine/store.py:474-493`) does keep `dyad_id` and `recipient_ref` mutually exclusive and class-derived, so today presence and class coincide. That is a coupling to a write-path invariant that neither module states and no test pins. Any future write path that stamps `recipient_ref` on a fact for context — not for scope — silently widens that fact's derived audience to the whole care team, and widening the *source* audience is the dangerous direction (V2 checks `tgt ⊆ ex`).

---

## G-5 — MEDIUM — The `resolver` keyword is a total bypass; the authenticity guarantee is caller-elective

**Class:** design smell that is an exploitable hole under the stated threat model. **Confidence:** high on the mechanism; the severity depends on where the trust boundary is actually drawn.

**File/lines:** `harness/learner_isolation.py:222` and `231`: `resolver = resolver or _DEFAULT_RESOLVER`. No mode flag, no production assertion, no type identity check.

**Trigger:** `check_training_example(ex, tgt, resolver=Yes())` where `Yes.resolve` returns `Provenance(tgt["household_id"], frozenset(tgt["audience"]))` — or simply `Provenance(None, None, is_public=True)`, which short-circuits at line 265 for every target including the shared base. The entire D-30 fix is one keyword argument wide.

**The uncomfortable part:** the 23-case battery passes `resolver=FIX` in **every** case (`_chk`, line 118). The attack and the test suite are the same call. There is no signal in the code that distinguishes them, which means there is nothing a static check could key on either.

**Would the battery catch it?** **No — the battery is an instance of it.** Its own helper is the exploit primitive.

**Honest framing:** if the trust boundary is "the learner process is trusted and the gate is a discipline it applies to itself," this is not a hole. But that reading contradicts the module's own framing — "the ENFORCEMENT SURFACE a future learner MUST route every training example through" — and it contradicts the D-30 rationale, which was that the caller must not be able to assert provenance. A caller who can pass `resolver=` can assert provenance in one hop. The gate should either name this assumption in the docstring's trust list or make the injection unavailable outside test context. Right now it is neither named nor constrained.

---

## G-6 — MEDIUM — V4 (label provenance) verifies a string, not a provenance

**Class:** design smell shading into a hole; same root cause as the original six. **Confidence:** high.

**File/lines:** `harness/learner_isolation.py:243-247`. The check is `example.get("label_source") != "post_gate_outcome"`.

Nothing about the label's derivation is verified. The field is a caller-typed constant; any caller stamps it. Bill's ruling ("labels post-gate only") is enforced as spelling. In the snapshot scorer this becomes visibly circular: `build_training_examples` (snapshot line 322) stamps `"label_source": POST_GATE_LABEL` — importing the very constant the gate will compare against — on labels the same function just computed. The producer certifies itself and the gate confirms the certificate matches the constant the producer imported.

**Security consequence:** a poisoned label is a poisoned reward is a poisoned model. Labels are the one input the gate is *supposed* to constrain (ruling 4 of the D-23 law) and it constrains them less than it constrains features. A caller who wants to invert every label does so freely; V4 is satisfied.

**Would the battery catch it?** **No cases at all.** The 23-case battery has zero V4 cases — every `_ex()` hard-codes the correct string. The L7:LI1 harness scenario has exactly one (`layer7_crypto.py:1941`, `label_source="gate_decision"` → expects a violation), which proves the equality check fires on one wrong value. Neither asks whether the field means anything.

---

## G-7 — MEDIUM — `_find_gate_decision_key` is a denylist with concrete, demonstrable gaps

**Class:** hardening gap plus three concrete misses. **Confidence:** high on the misses (verified against the real `InjectionResult`).

**File/lines:** `harness/learner_isolation.py:76-81` (the frozenset) and `203-218` (the recursion).

**Concrete misses.** `GATE_DECISION_FEATURE_KEYS` is meant to be "the injection-contract outcome vocabulary." The actual `InjectionResult` (`harness/injection_contract.py:374-404`) declares thirteen fields. Three are gate-decision outcomes and are **absent** from the denylist:

| `InjectionResult` field | in denylist? |
|---|---|
| `inj2_declarative_override` (count of facts admitted via the INJ-2 declarative bypass) | **no** |
| `allowed` (the admitted set itself) | **no** |
| `injected_fact_ids` (the post-gate injected list) | **no** |

`features = {"inj2_declarative_override": 1}` passes V3 cleanly today. (I checked the `denied_inj4/6/7` hypothesis: those fields do not exist, so the 1/2/3/5 pattern in the denylist is not a gap — it mirrors the real field set. The gap is elsewhere.)

**The structural gaps, which no amount of list-tending fixes:**

- **Rename.** The check is key-name equality. The deny vocabulary itself — `deny_never_volunteer`, `deny_default_cross_member`, `deny_subject_scope`, `deny_relevance` (`injection_contract.py:642-690`) — rides through under any key name: `{"reason_code": "deny_relevance"}` passes.
- **Values are never inspected.** `{"attribute": "denied_inj1"}` passes the gate's denylist *and* the scorer's allowlist. "Structurally excluded from any learner feature space" is true of the key names only.
- **Containers the recursion does not descend.** Lines 213: `dict`, `list`, `tuple` only. A non-`dict` Mapping (`types.MappingProxyType`, `collections.UserDict`, `ChainMap`) or any object with a `__dict__` (`SimpleNamespace`, a dataclass instance) terminates the walk at line 218 with `None`. `features = {"m": types.MappingProxyType({"denied_reasons": [...]})}` is admitted.
- **No type check on `features` at all.** Line 236 is `example.get("features") or {}`; a string, an int, or a custom object is scanned and trivially clean.
- **Only `features` is scanned.** A learner that reads any other example key — `query_text`, or an arbitrary key the caller adds — gets gate-decision data untouched. The one-key scope is convention.

**The divergence worth flagging to the owner:** the scorer's REQ (acceptance item 3) demanded an **allowlist**, and the snapshot's `validate_feature_dict` implements one. The **gate** — the surface that will police every future learner, including ones nobody has written — is still a denylist. Two different guarantees, and the weaker one is on the load-bearing surface.

**Would the battery catch it?** **No cases at all.** The 23-case battery has zero V3 cases. The L7:LI1 harness scenario has one (`layer7_crypto.py:1931`, a nested `denied_reasons`), which proves the recursion descends one level of `dict` for one listed key. Neither probes completeness, nor renames, nor non-`dict` containers, nor values.

---

## G-8 — MEDIUM-LOW — Roster currency is checked; fact currency is not

**Class:** genuine gap, same class as HOLE-6. **Confidence:** medium-high.

**File/lines:** `harness/learner_isolation.py:160-166`. The read is `MATCH (f:Fact {fact_id: $fid}) RETURN ... LIMIT 1` — no filter on `valid_to`, `record_closed_at`, `closed_reason`, or `superseded_by`.

Fact closure in this system is **soft** (`memory_engine/store.py:291-330`: `SET f.valid_to = $ts, f.record_closed_at = $ts, f.closed_reason = 'superseded'`). A superseded, retracted, or user-deleted fact therefore still resolves and still yields a full `Provenance`, so it remains admissible for training indefinitely. D-30 bound the *roster* to live state; the *fact* is read as if lifecycle did not exist.

**Security consequence:** deletion does not propagate to the learner. A fact the household retracted — including one retracted *because* it was wrong or because someone exited — keeps training the model every time the example set is rebuilt. In a system whose custody model has an explicit exit path, that is a real erasure gap.

**Would the battery catch it?** **No — structurally cannot.** `FixtureResolver` is a static dict with no lifecycle dimension; no case can express "this fact was closed."

---

## G-9 — LOW-MEDIUM — Violation strings are a provenance and roster oracle, and the scorer pipes them to stderr

**Class:** information disclosure; genuine but bounded. **Confidence:** medium-high.

**File/lines:** `harness/learner_isolation.py:277-279` and `294-298`.

The violation strings embed derived, server-authoritative state:
- V1 returns `"example {ex_id} derives to household '{ex_hh}'"` — a **fact_id → household** oracle that works **across** households. Fact_ids are not secret: `injected_fact_ids` is written into every epistemic record.
- V2 returns `"live source audience {sorted(ex_aud)}"` — the **full live roster** of the example's source scope. Submit a fact_id against `{"household_id": <its household>, "audience": frozenset({"attacker"})}` and the refusal enumerates the dyad or care-team membership for you. The refusal is more informative than the acceptance.

This is amplified downstream: in the 07:42 snapshot, `train_weights` returns violation strings and `_weights_for` (line 391-393) prints each one to **stderr**, with `example_id` formatted as `f"{turn_id}:{fact_id}"`. So the derived household, the live roster, the turn id and the fact id land together in process logs.

**Ordering note (the seam as posed):** V3 and V4 do run before provenance, so a caller can distinguish "my feature dict is dirty" from "my provenance is wrong" without the gate ever touching the graph. That is a mild timing/behavior oracle but I could not build anything meaningful on it — the ordering leaks nothing the caller does not already know about its own example. The real oracle is the *content* of the V1/V2 strings, not the order.

**Would the battery catch it?** **No.** Several cases assert violation strings *contain* these substrings (`"cross-household pooling" in v`), i.e. the battery treats the disclosure as the desired behavior. That is a defensible trade (a violation you cannot diagnose is a violation nobody fixes) but it should be a stated decision, not an accident.

---

## G-10 — LOW — Return-value discipline: the gate is advisory in shape

**Class:** design smell. **Confidence:** high (it is a signature-level observation).

`check_training_example` returns a string; `check_training_batch` (line 303-308) returns a list of violations and **drops nothing** — it hands back the diagnosis and keeps none of the data. A caller who ignores the return value trains on everything, and the gate has no way to know or complain. There is no API that returns the *admitted subset*, which is the shape an enforcement surface wants. Compare the snapshot scorer, which does implement drop-and-log correctly (`train_weights` returns `(weights, violations)` and the rejected examples are provably absent from the list `_fit_weights` receives) — the right pattern exists, one layer up, by convention rather than by the gate's shape.

For a module whose docstring says "MUST route every training example through," the signature makes the safe path optional and the unsafe path the default.

---

## G-11 — LOW — Audience type discipline: `is None` is the only check

**Class:** hardening. **Confidence:** high.

Line 286 checks only `is None`; line 292 does `frozenset(tgt_aud) - frozenset(ex_aud)` on whatever arrives. Consequences:

- A **string** source roster decomposes to characters. Case `e6`'s own note concedes this ("blocks here, still not a type check") — and it blocks only because the case chose the safe direction. Source `"alice"` against target `"ace"` yields `{'a','c','e'} - {'a','l','i','c','e'} = ∅` → **admissible**. The battery tested the direction that happens to pass.
- A **non-iterable** target audience (`audience=5`) raises `TypeError` out of the gate. That is fail-closed by crash rather than by decision, and in the snapshot scorer it is swallowed by `_weights_for`'s bare `except Exception` (line 395) into a silent cold-weights fallback.
- An **empty** target audience is vacuously authorized — see G-2, where it is the exploit rather than an edge case.

`e3` blesses empty-on-both-sides as "vacuous set containment, acceptable." I think that is defensible in isolation and indefensible in combination with G-2, because the same vacuity that makes `e3` harmless is what makes the empty *target* a universal key.

---

## G-12 — LOW today, HIGH on the day it changes — the public carve-out is unconditional and pre-empts every other check

**Class:** design smell with a dated fuse. **Confidence:** high; I verified the current fail-closed claim.

Line 265: `if prov.is_public: return None`. Before the household check, before the audience check, for **any** target. And the gate never validates the `Provenance` invariant its own dataclass docstring asserts (line 90-96, "`household_id` is None ONLY when `is_public` is True") — a `Provenance(H1, CIRCLE1, is_public=True)` returns admissible for the shared base with a household attached.

**I confirmed the carve-out genuinely fails closed today.** `provenance_class` appears nowhere in the codebase except the three lines of `learner_isolation.py` that read it; `_CREATE_FACT_CQL` (`memory_engine/store.py:215-236`) is a fixed property list; and there is **no** `SET n += $props`-style dynamic property write anywhere in the tree. The docstring's claim is accurate.

**But trace the day it changes.** Whoever adds `provenance_class` will be adding a public/synthetic marker for some authoring or seeding process, and on that day a single property becomes a total exemption from every check in this module — with no second factor, no audit trail, no assertion that `household_id is None`, and nothing in the test suite that will go red. Combined with G-1 (features unbound to the fact_id), a single public fact_id becomes an unlimited carrier for arbitrary household content into the shared base. The carve-out is currently protected by the absence of a feature, which is not a control.

---

# PART 2 — SCORER FINDINGS (against the 07:42 snapshot only; the author may already have changed any of these)

## S-1 — MEDIUM — The trained regime will invert recency (modelling defect, not a security hole)

**Class:** genuine correctness defect. **Confidence:** high on the mechanism; medium on how badly it shows in practice, which depends on the correction rate.

**Snapshot lines:** `curator_shadow.py:351-369` (`_fit_weights`), `183-200` (`_encode`), `285-324` (`build_training_examples`).

Three facts compose badly:

1. `build_training_examples` labels every admitted fact `1` unless a later correction targets it (line 321). Corrections are rare by construction, and overrides carry no `target_fact_ids` (the inherited Stage-0 limit), so the training set is overwhelmingly — often entirely — positive.
2. `_fit_weights` has **no intercept/bias dimension** (`_ENCODED_DIMS`, line 103-105, is ten feature dims, no constant). There is nothing to absorb the base rate.
3. Every encoded dimension is **non-negative**, and `recency` is `float(features.get("recency_rank") or 0)` — a raw, unnormalized, unbounded rank (0, 1, 2, … n), while every other dim is bounded in [0, 1].

With all `y = 1`, the gradient `g = y - p` is strictly positive on every step, so `w[d] += lr * g * x[d]` makes **every** weight monotonically non-decreasing — and `recency`, having by far the largest feature magnitudes, accumulates the largest coefficient. Score is `Σ w·x` sorted descending, so **higher rank (older) sorts first**. Cold start uses `{"recency": -1.0}` (newest first). The regime flip at the 100-event threshold therefore flips the sign on the only dimension the cold regime uses.

**Consequence:** the moment the scorer leaves cold start, the shadow ranking will tend to invert the rule order for a degenerate reason — class imbalance with no intercept and unscaled features — not because it learned anything about relevance. The danger is interpretive: Stage 2's whole purpose is to compare the shadow ranking against the rule ranking, and a large, systematic divergence produced by a modelling artifact is exactly the shape a real signal would take. The agreement metric will surface it as poor agreement *if* it is read as a falsification test rather than a number to improve. I would not want this regime to flip on live data before that is understood.

**Battery relevance:** out of scope for the isolation battery. The CS1 twin's own trained-regime check (snapshot section vii) only asserts the output stays a *permutation* of the admitted set — it deliberately allows order to "legitimately diverge," so it will pass while the inversion is happening.

## S-2 — MEDIUM — The allowlist is depth-1 while the denylist is deep

**Snapshot lines:** `curator_shadow.py:162-180`.

`validate_feature_dict` iterates `for k in features` — **top-level keys only** — while `_find_gate_decision_key`, which it calls first, recurses arbitrarily deep. So the allowlist guarantee ("the declared ten, exactly") holds at depth 1 and stops. A nested payload under a *declared* key — `{"attribute": {"anything": ...}}` — passes validation entirely. Values are never type-checked either; a declared key may hold any object.

What actually stops it is incidental: `_encode` line 188 does `attr.encode()`, which raises `AttributeError` on a dict, which propagates to `_weights_for`'s bare `except Exception` and silently degrades to cold weights. The feature space is being defended by a crash in an unrelated function.

**Battery relevance:** the CS1 twin (snapshot section iii) checks three flat violating keys and one clean extractor output — depth-1 cases only, so this is invisible to it.

## S-3 — MEDIUM — The "shadow cannot act" static scan under-covers the property it certifies

**Snapshot lines:** the `_cs_scan` block in the `layer7_crypto.py` diff.

**The property is true today — I verified it independently and tree-wide.** `shadow_score_turn` has exactly one production reference: `server/voice_orch.py:2755`, inside the nested `emit_epistemic_record` closure (defined at `voice_orch.py:2681`), after `reply_out` is final and after the G0 check, and `_emit_epistemic_record` itself has exactly one call site (`voice_orch.py:2762`). Every other reference is in `eval/`. The return value flows only into `kwargs["curator_shadow"]` → `build_epistemic_record` → the log. Structurally shadow. Good.

**The check that is supposed to keep it true is narrower than the claim:**
- It scans exactly **two files** (`server/voice_orch.py`, `harness/orchestrator.py`). A reference added in any third module is invisible. The synthetic red fixture is literally named `local_system_prompt` — the author had that module in mind — yet `local_system_prompt` is never scanned. The correct shape for the invariant is a tree-wide reference scan, which is what I ran by hand.
- The regex `shadow_score_turn|harness\.curator_shadow` misses the valid import form `from harness import curator_shadow as cs`.
- The "inside the hook" span is defined by `str.find` on two literal source strings. Move or duplicate the marker comment and the span moves with it. It does fail closed if the marker disappears (`span_a == -1` → every hit flags), which is the right default.

## S-4 — MEDIUM — `historical_acceptance` is a feature whose provenance is the whole log

**Snapshot lines:** `curator_shadow.py:269-280`, `146-147`, and `423`.

`acceptance_history(recs)` is computed over **every record in the log** — all members, and (per the module's own named limit) all households — and its output becomes the `historical_acceptance` feature. It is the one declared feature that is not a property of the fact as seen by this member: it encodes how often *other people* were injected with that fact and *how often they corrected it*.

Two consequences:
- It ties directly to **G-1**: the isolation gate checks the provenance of the `fact_id` and can never see that a *feature value* was derived from a pooled corpus. The scorer has already built the first feature the gate is structurally blind to. If per-scope models arrive (an open REQ question), this feature carries cross-scope aggregate behavior into a scoped model and the gate will approve every such example.
- It is now **persisted per-turn in plaintext** — `shadow_score_turn` logs the full `features` map into the epistemic record, so every turn's record gains a per-fact behavioral aggregate about the household's correction history. Not a value leak (TD-030 holds; see below), but it is a genuinely new class of derived signal in a file that is read wholesale.

## S-5 — MEDIUM-LOW — Training labels and the offline metric use different lookahead windows

**Snapshot lines:** `curator_shadow.py:302-303` vs `curator_agreement.py:30-31`.

`build_training_examples` takes `records[i+1 : i+1+lookahead*3]` and then filters to same-member, keeping the first 10 — a hard 30-record distance cap. `shadow_outcome_agreement` scans `records[i+1:]` **with no distance cap** and takes the first 10 same-member records however far away they are.

So the two disagree about what "later corrected" means. The metric can count a correction 500 turns downstream that the label builder structurally could not see. Offline eval is therefore not measuring the same label the model was fit on. Separately, the 30-record cap in the label builder silently **loses** corrections whenever members interleave (a busy household easily pushes the 10th same-member turn past 30 records), which biases the training set optimistically — toward label 1 — which is the same imbalance that drives **S-1**.

## S-6 — LOW — `validate_shadow_output` is tautological in-path, and does not catch the failure modes that are actually reachable

**Snapshot lines:** `curator_shadow.py:228-238`, called at `426`.

Both arguments derive from the same `allowed` list in the same function, so `curated ⊄ admitted` is unreachable by construction — the snapshot's own comment says so ("unreachable by construction; checked anyway"), which is honest. It is a fault-twin target, not an in-path assertion, and calling it "the in-path curated⊆admitted assertion" overstates what it does at runtime. I could not construct a superset: `score_facts` emits exactly one row per input fact and never sources outside the list.

What it does *not* catch is what can actually happen: facts with a missing `fact_id` produce `None` entries that pass the membership test, and duplicate/`None` fact_ids silently collapse the `scores` and `features` dicts (line 438-439), so the logged feature map can have fewer entries than the ranking — and `build_training_examples` later reads that map by fact_id (line 314).

## S-7 — LOW — `_fit_weights`'s underscore is documentation, not a boundary

**Snapshot lines:** `curator_shadow.py:351-357`.

Calling it "the no-bypass line" overclaims; a leading underscore is a naming convention, and the harness itself imports it (`from harness.curator_shadow import _fit_weights as _cs_fit_raw`) to demonstrate exactly that. The *evidence* the twin produces is real and valuable — gated fit ≡ clean fit, bypassed fit ≠ either, so the gate provably changes the artifact. But that is a demonstration that the gate matters when used, not a mechanism that prevents not using it. Same shape as **G-10**: the safe path is a convention at every layer of this stack.

## S-8 — LOW — The named scaling limits are honest, and one of them now accelerates itself

**Snapshot lines:** `curator_shadow.py:48-52`, `243-259`, `418-423`.

The docstring names the whole-file read per scored turn and the single-household outcome count. Both are accurately described. Two things to add:

- Per scored turn the scorer now does a whole-file read **plus** `outcome_event_count` (O(N)) **plus** `acceptance_history` (O(N)), and at each refit boundary `build_training_examples` (O(N)) — and this runs **on the reply path**, inside the emit closure before `return reply_out`. "Shadow" is a claim about content, and it is correct about content; it is not a claim about latency or availability, and the growth is quadratic in log length.
- The scorer now writes a per-fact `features` map into every record, so the log grows measurably faster than before — the mechanism whose cost is O(log size) is itself increasing the log size. The named limit tightens on its own.
- `_WEIGHT_CACHE` (line 374) is keyed on `n_events // 50` with **no household component**. Under the single-household assumption that is fine; on a multi-household log it serves household A's fitted weights to household B — and combined with **G-3**, which makes the gate admit B's household facts into A's fit, the multi-household story fails on two independent axes at once.
- The regime flip is user-influenceable in the ordinary sense: `outcome_event_count` counts correction/override records over the whole log, so a household (or anyone able to drive turns) can push past `COLD_START_THRESHOLD = 100` and promote the scorer out of rule-order reproduction into the regime described in **S-1**. That is inherent to outcome-driven learning, not a defect, but the threshold is the only thing standing between the current byte-identical behavior and S-1, and it is reachable by ordinary use.

---

# PART 3 — WHAT I TRIED THAT DID NOT BREAK

These are real results. Each is something I attacked and could not move.

**D-1 — The V1/V2 relationship math is sound.** I went at the derived-value comparison from several directions: asymmetry between the two containment directions, ordering effects, aliasing between `ex_hh` and `tgt_hh`. Broader→narrower is correctly allowed; narrower→broader is correctly blocked; the shared-base direction is correctly special-cased with a distinct message; V1 short-circuits before V2 so a household mismatch is never masked by an audience coincidence. D-25's assessment that this logic is sound survives my reading. **Every hole I found is upstream of this math, in what gets fed into it.**

**D-2 — The public carve-out genuinely fails closed today.** I tried to find any way to set `provenance_class` on a `:Fact`. `_CREATE_FACT_CQL` (`memory_engine/store.py:215-236`) is a fixed property list; the only `SET f.*` statements in the store are the lifecycle closures (lines 291, 304, 330, 647), all with literal property names; and there is no `SET n += $props` or equivalent dynamic-property write anywhere in the tree. `provenance_class` appears in exactly three places, all inside `learner_isolation.py`. The docstring's claim is accurate. My concern in **G-12** is entirely about the day that changes, not about today.

**D-3 — `fact_id` is genuinely unforgeable.** `memory_engine/store.py:496`: `new_fact_id = str(uuid.uuid4())`, server-side, at encode time. The premise the whole D-30 fix rests on holds.

**D-4 — The scorer's value blindness holds.** `extract_features` (snapshot 128-159) reads exactly ten named metadata keys, never iterates the fact dict, and never touches `value`, `ciphertext`, `encrypted_dek`, `embedding`, or any driving-utterance field. `_encode` derives `attr_bucket` from the `attribute` *name*, which is metadata. Two facts differing only in value do produce byte-identical feature dicts. I could not find a path from a value to a feature. TD-030 holds through this addition.

**D-5 — The cold-start byte-identical claim holds.** `COLD_WEIGHTS = {"recency": -1.0}` and `_encode["recency"] = rank`, so `score_i = -rank_i`; `rows.sort(key=lambda r: -r[1])` sorts ascending by rank; the sort is stable, so ties (all-zero scores when `recency_rank` is missing) preserve input order. The claim is exactly true as written, for the reason stated.

**D-6 — The agreement metric is correct against its own hand-computed fixture.** I recomputed all four cases by hand from `curator_agreement.py:21-45`: case A yields 1 pair correct → 1.0; case B yields 1 pair wrong → 0.0; A + case-C pooled yields 1 of 2 → 0.5; case D yields no pair → `None`. All four match `want`. The distinct-member trick to keep lookahead windows from crossing fixtures is sound. This is a genuinely hand-checkable, non-model-graded fixture — the strongest piece of the snapshot.

**D-7 — I could not produce a `curated ⊄ admitted` superset.** `score_facts` emits one row per input fact and cannot source outside the list it was given; the only production caller passes `injection_result.allowed` directly. The property holds structurally; my criticism in **S-6** is that the assertion is therefore not doing in-path work, not that the property is false.

**D-8 — The shadow placement claim holds tree-wide.** Verified by exhaustive reference search, not by the snapshot's own scan. One production call site, inside the record-emit closure, post-reply, post-G0, return value flows only to the log. **S-3** is about the durability of that property, not its current truth.

**D-9 — The ordering-oracle hypothesis (V3/V4 before provenance) did not pan out.** I could not construct anything a caller learns from *which* violation returns first that it does not already know about its own example. The real disclosure is the *content* of the V1/V2 strings (**G-9**), not the order of the checks.

---

# Summary table

| # | Finding | Class | Severity | Battery would catch? |
|---|---|---|---|---|
| G-1 | Features never bound to the authenticated fact_id | exploitable hole | **critical** | No — structurally cannot |
| G-2 | Target household/audience wholly caller-asserted; empty audience is a universal key | exploitable hole | **high** | No — structurally cannot |
| G-3 | `_household_of` collapses all household facts to `"default"` | latent hole, certain | **high** | No — production resolver never executed |
| G-4 | Dyad branch reads non-existent columns → empty audience; no status/removal filter | defect, certain | **high** | No — production resolver never executed |
| G-5 | `resolver=` kwarg is a total bypass | smell / hole per threat model | medium | No — the battery *is* the exploit |
| G-6 | V4 verifies a string, not a label's provenance | smell → hole | medium | No cases at all (1 in the L7 scenario) |
| G-7 | Denylist vs allowlist; 3 real field misses; renames, values, non-`dict` containers | hardening + concrete misses | medium | No cases at all (1 in the L7 scenario) |
| G-8 | Closed/superseded facts still resolve and remain admissible | gap | med-low | No — fixture has no lifecycle |
| G-9 | Violation strings disclose derived household + live roster; scorer prints to stderr | disclosure | low-med | No — battery asserts the disclosure |
| G-10 | Advisory return shape; no admitted-subset API | smell | low | n/a |
| G-11 | No roster type check; string rosters compare char-wise | hardening | low | Partially — `e6` tests the safe direction only |
| G-12 | Public carve-out unconditional, pre-empts all checks, no second factor | dated fuse | low now / high later | No — fails closed today |
| S-1 | Trained regime inverts recency (no intercept, unscaled rank, all-positive labels) | defect | medium | n/a (scorer) |
| S-2 | Allowlist is depth-1; nested payloads pass | hardening | medium | n/a |
| S-3 | Static "cannot act" scan covers 2 files; regex misses a valid import form | coverage gap | medium | n/a |
| S-4 | `historical_acceptance` pooled over whole log; gate blind to feature provenance | smell (ties G-1) | medium | n/a |
| S-5 | Label window ≠ metric window; 30-record cap loses corrections | correctness | med-low | n/a |
| S-6 | `validate_shadow_output` tautological in-path; misses `None`/duplicate collapse | overclaim | low | n/a |
| S-7 | `_fit_weights` underscore is not a boundary | overclaim | low | n/a |
| S-8 | O(N)×4 per turn on the reply path; log growth self-accelerating; cache key lacks household | honest limit, partly load-bearing | low | n/a |

---

## Closing note on the battery itself

The most useful thing I can say is not any single finding. It is that **the 23-case battery covers V0, V1, and V2 only.** It has zero cases for V3 (feature hygiene) and zero for V4 (label provenance) — both of which are direct rulings from Bill's D-23 law — and it executes `RegistryProvenanceResolver` zero times, so the entire production derivation chain (**G-3**, **G-4**, **G-8**) is outside its reach by construction. The L7:LI1 scenario adds exactly one V3 case and one V4 case, each a single-value existence check.

More fundamentally: the battery's fixture shape hard-codes the two assumptions that **G-1** and **G-2** break. Features are a constant decoration in all 23 cases; targets are ground truth by construction. Those are not gaps you close by adding cases to the existing file — the `_ex()` helper and the module-level target constants would have to change shape first, because the current shapes cannot express the attack.

D-25's verdict on the old gate was that it checked relationships and not authenticity. My verdict on the new one: **it now authenticates one of the three things the caller supplies.** The example's provenance pointer is unforgeable. The payload that pointer authorizes, and the model that payload is authorized *for*, are still whatever the caller says they are.

**No REQ status is proposed or implied by this review. All rulings are the project owner's.**
