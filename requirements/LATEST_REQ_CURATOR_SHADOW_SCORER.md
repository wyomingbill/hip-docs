# REQ_CURATOR_SHADOW_SCORER: Stage 2 Shadow Metadata Scorer — Learner Exists, Cannot Act
Status: MET

## MET 2026-07-30 (D-44) — Bill's ruling, recorded

**MET is Bill's call and this block records the call he made** (D-44 dispatch),
per the standing protocol that a session never self-marks MET. The D-42 pullback
below stands as accurate history of why the D-39 MET was premature; this block
says plainly that the gap it named is now closed.

**What the ruling rests on.** The scorer is shadow-proven (byte-identical prompt
with `HIP_CURATOR_SHADOW` on and off), reproduces the deterministic rule order
byte-identical at cold start, and routes every training example through the
MET-hardened isolation gate (`REQ_LEARNER_TARGET_AUTHENTICATION`, unaffected by
the pullback and still MET). External adversarial review is on the record
(D-40, two independent blind Fable reviewers), as is the verification that
followed (D-41 by direct reproduction, D-42's fixes, D-43's green `--full`).

**The four Fable-confirmed substrate defects, each fixed and each re-verified
by re-running D-41's own reproduction against the fixed code:**

1. **Inverted label default at `classify_outcome`** — the filter now reads the
   keys the write path actually produces, `transition == "supersede"` and
   `prior_fact_id` (`harness/outcome_classifier.py:61-63`). D-41's exact
   reproduction, re-run at this commit: correction emitted `True` (was
   `False`), training example labelled `0` (was `1` — the inversion),
   `outcome_event_count` `1` (was `0`), and `shadow_outcome_agreement` returns
   a real `0.0` (was `None`). **The corpus is no longer single-class.**
2. **`register_model` wired** — as the deliberate operator act it was designed
   to be, via `scripts/register_curator_shadow_model.py`, imported by no
   training-path code. The silent-refusal half of the defect is closed
   separately by `_GATE_REFUSED_SENTINEL`, so total gate refusal is no longer
   indistinguishable from genuine low data volume. See the honest limit below.
3. **`_WEIGHT_CACHE` partitioned** — `cache_key = (household_id, n_events // 50)`
   (`harness/curator_shadow.py:444`), so one household's fitted artifact can no
   longer be served for another household's turn.
4. **`historical_acceptance` bounded** — clamped to its declared `[0,1]` domain
   at the source (`harness/curator_shadow.py:155`). D-41's overflow case (1
   injected, 5 corrected) now yields `0.0`, not `-4.0`; no path to `inf`/`NaN`
   in the fit or into the record. `validate_shadow_output` additionally
   constrains ORDER against the turn's own logged scores, so it is no longer
   tautological in-path — D-41 showed a hand-scrambled ranking passing the
   membership-only check unchanged.

**Proof run:** `scripts/run_harness.sh --full`, exit 0, at 81da8b0 (D-43,
`/tmp/hip_harness_20260730_1538.log`): all 5 ABSOLUTE checks PASS (G0, PSA1,
CTX-STRIP, LI1, **CS1**), L7 27/27, AUDIT 8/8 (59 checks, 35 debt-flagged,
unchanged), **RATCHET PASS** — no scenario regressed. Three new standing test
files guard the fixes (`eval/test_outcome_classifier_correction.py`,
`eval/test_curator_shadow_regime.py`,
`eval/test_curator_shadow_value_and_order.py`), wired into
`scripts/run_harness.sh` alongside the D-37 battery.

**HONEST LIMIT, named not buried — the trained regime is still CLOSED.** Fix 2
made registration *possible* and *visible*; it did not perform it. Verified
read-only against the live registry at this commit: the `learner_models` table
still does not exist, so `curator-shadow-default` does not resolve and every
training example is still refused at gate V0b. **The scorer therefore runs in
cold-start regime today, and the trained regime has never executed on real
data.** That is the correct posture — registration is a deliberate operator
act, and this REQ's original coverage entry already named "the trained regime
live on a real graph" as UNCOVERED — but it means this MET certifies that the
learner *can* learn, demonstrated on a real correction end to end, not that it
*has* learned in production. Opening the trained regime is a separate,
deliberate act: run `scripts/register_curator_shadow_model.py`. Whoever does it
should expect the D-41 findings that are latent behind it (notably the
attacker-influenced cold-start threshold) to become live at that moment.

## STATUS PULLED BACK 2026-07-30 (D-42) — the learning substrate is structurally dead

The D-39 MET below was PREMATURE and is withdrawn. Not because the scorer's
ISOLATION properties are wrong — they hold, and D-41's verification confirms
it — but because MET was granted for "the first learner in this codebase,"
and this learner **cannot learn**. That is the gap the D-39 ruling did not
have in view.

D-40 routed the built scorer to two independent Fable reviewers for
adversarial review, captured verbatim
(`docs/reviews/FABLE_ShadowScorerReview__adversarial-curator-stage2-scorer-review__v20260730_1122.md`).
D-41 verified four of their findings by direct reproduction — in two cases
going further than either reviewer, who both explicitly declined to execute
code or query the database
(`docs/dispatches/DISPATCH_D41__verify-fable-scorer-findings__v20260730_1438.md`):

1. **The correction/label substrate is structurally dead — and the label
   isn't missing, it's INVERTED.** `classify_outcome` requires each delta
   entry to carry `write_state == "supersede"` and a `fact_id`; the delta
   the write path actually produces carries neither — the supersede signal
   lives under `transition`, and the fact ids under `prior_fact_id`/
   `new_fact_id`. Verified by RUNNING a synthesized real supersede through
   the actual classifier: it fails to detect the correction on both the
   projected delta and the raw delta. On the real 12-record log,
   `build_training_examples` produces 34 examples, every one labeled `1` —
   a single-class corpus — `shadow_outcome_agreement` returns `None`, and
   the resulting fit is an all-positive-weight projection of the corpus
   mean, exactly the failure mode predicted. Acceptance item 7's own
   evidence (`curator_agreement_self_test`) hand-authors the outcome shape
   the real classifier cannot produce.
2. **`register_model` has zero callers — by design, not oversight** (the
   module's own docstring: "REGISTRATION IS AN OPERATOR ACT... a caller
   cannot register the model it is about to train"). The defect is that
   **the operator act has never been performed**, and the resulting total
   refusal is silent. A copy of the live registry (never the live file — see
   below) confirms the `learner_models` table does not exist at all among
   its 13 tables — stronger than either reviewer found, since both declined
   to query the database. Run directly against production's real
   `model_id`: `get_model('curator-shadow-default') -> None`,
   `RegistryModelResolver().resolve(...) -> None`, and
   `check_training_example` refuses with an explicit "unresolvable training
   target" message. At a synthesized 150 outcome events (past the 100
   threshold), the record would read `outcome_events: 150, regime:
   "cold_start"` — total refusal is indistinguishable from not-enough-data.
   Fail-closed and safe; the finding is that it is silent.
3. **`_WEIGHT_CACHE` has no household or corpus-identity component in its
   key** — `cache_key = n_events // 50`, a plain integer — **PROVEN live**,
   not just read: with the gate stubbed to isolate the cache question from
   finding 2's refusal, household A's fit and household B's turn land in
   the same cache bucket, and B is served A's weight object BY PYTHON
   OBJECT IDENTITY, when B's own fit would have produced materially
   different weights. Latent today only because finding 2 means no real fit
   ever occurs, and because this deployment has one household.
4. **`historical_acceptance` is unbounded** (nothing asserts `corrected ≤
   injected` — demonstrated reaching `-4.0` and, separately, `inf`, which
   `json.dumps` then serializes as a bare, non-conformant `Infinity`
   token), **`validate_shadow_output` is tautological in-path**
   (`ranking` and `admitted_ids` both derive from the same `allowed` list —
   demonstrated by feeding it a hand-SCRAMBLED ranking, which passes: order
   is unconstrained, only membership is checked), and **the metamorphic
   query-reword check is vacuous in both places it exists** (the CS1
   scenario's own sub-check makes two byte-identical calls; the audit
   probe's `_reword` loop variable is never referenced in the call it
   guards — demonstrated by a mutation test: `extract_features` rewritten to
   take the query text directly and hash it into a feature still passes
   the probe, because the probe only checks a *variable name*, never
   behavior).

**Methodology finding neither reviewer caught, worth naming on its own:**
`get_model` is a read function with a WRITE side effect — it runs `CREATE
TABLE IF NOT EXISTS` and commits on every call. Verifying finding 2 against
the live registry directly would have created the very table whose absence
is the evidence. D-41 ran every resolver call against a copy instead,
proven by the copy growing to 14 tables while the live file stayed at 13.
Any future verification against this registry should copy first.

**What this REQ's acceptance test actually proved, restated honestly:** the
scorer is shadow-only (verified, holds), value-blind (verified, holds),
cold-start byte-identical to the rule order (verified, holds — the
reviewers' cleanest finding), and its gate over-refuses in production rather
than under-refusing (verified, holds — fail-closed, the safe direction).
**What it did not prove, and what the acceptance items assumed it had**: that
the scorer can produce a trained model at all. It cannot, on the data this
deployment has ever produced, because the one signal that would let it
leave cold start is never emitted.

**Explicitly NOT undermined: `REQ_LEARNER_TARGET_AUTHENTICATION`.** Both
Fable reviewers independently searched this scorer for the 7th-hole shape
(a caller-asserted or empty target operand) recurring and found it does
not — D-37's fix holds here. The one target dict this scorer constructs
(`curator_shadow.py:387-390`) is read by `model_id` only; the
`household_id`/`audience` fields built alongside it are inert, per D-37's
design (the caller cannot assert scope; only decoration remains). D-42
leaves that REQ's MET status untouched.

**Re-earning MET requires, at minimum:** a real path from a real turn to a
real `correction` outcome (fixing the `write_state`/`fact_id` field mismatch
between `fact_change`'s delta projection and `outcome_classifier`'s
expectations), an operator act that actually registers a model so the
trained regime is reachable at all, a `_WEIGHT_CACHE` keyed on
household/corpus identity, and a bounded `historical_acceptance`. Part B,
below, builds all four under this same REQ — sequenced per D-41's own
recommendation (fix (a) first; it decides whether the scorer can learn at
all), each with an `xfail(strict=True)` test demonstrating the defect red
before the fix and green after, the same discipline D-27/D-37 used.

## PART B — FIX SPEC (D-42), acceptance for the four confirmed defects

Pass/fail per item; each closes exactly one D-41 finding.

**B1 (closes finding 1 — dead/inverted correction substrate).**
`classify_outcome` (`harness/outcome_classifier.py`) reads the delta fields
the write path actually produces — `transition == "supersede"` and
`prior_fact_id` — instead of the `write_state`/`fact_id` keys that are never
set. Observable: a synthesized real supersede (the same shape D-41 used)
produces `{"kind": "correction", "target_fact_ids": [<prior_fact_id>]}`,
not `NO_OUTCOME`. `xfail(strict=True)` test added first, demonstrating the
current miss; flips to real PASS when the fix lands. **No change to
`fact_change.py`'s delta shape** — the fix reads what already exists rather
than widening what gets projected, the smaller and lower-risk of D-41's two
named options.

**B2 (closes finding 2 — silent total refusal, indistinguishable from
cold-start).** Two parts, since D-41 named the operator act as deliberately
out of scope for any code path: (i) `_weights_for` reports a regime the
audit can actually tell apart from cold-start when every example was gate-
refused versus when there is genuinely no data — a new regime value (e.g.
`"gate_refused"`) or an explicit reason string, not a silent fold into
`"cold_start"`. (ii) The registration itself is **not** performed by
production code (that would recreate the caller-asserts-its-own-scope hole
`model_registry.py`'s own docstring exists to prevent) — it is named here as
an explicit, separate operator action, with a one-time script or documented
manual step Bill can run when ready to open the trained regime. Observable:
a fixture where every example is gate-refused reports a regime distinct
from a fixture with zero events; `register_model` remains uncalled by any
training-path code.

**B3 (closes finding 3 — unpartitioned weight cache).** `_WEIGHT_CACHE`'s
key includes the target's `household_id` (or `model_id`, since that already
encodes household — `MODEL_ID_PREFIX + household_id`) alongside the event
bucket. Observable: the cross-household reproduction D-41 built (two
households, gate stubbed to admit) shows household B's cache lookup misses
and produces its own fit, never A's object, even when both land in the same
event bucket.

**B4 (closes finding 4 — unbounded value, tautological assertion, vacuous
metamorphic check).** Three independent, small fixes: (i) `historical_
acceptance` is clamped to `[0.0, 1.0]` (or the record fails validation)
before it reaches `_encode`; (ii) `validate_shadow_output` additionally
asserts `ranking == sorted-by-score order` is consistent with the *scores*
dict logged beside it — order, not just membership — so a scrambled ranking
against its own scores fails; (iii) the metamorphic check is rewritten to
actually vary a real, behavior-affecting input (drive two genuinely
different `sio_attribute` values, or accept D-41's mutation test as the
standing regression by asserting query-text independence structurally —
`extract_features`'s signature contains no query parameter AND its
`__code__.co_names`/closure never references one — rather than a variable-
name string match alone).

**Sequencing (D-41's own recommendation, followed here):** B1 first — it
decides whether the scorer can learn at all. B2 next. B3/B4 are real but
latent; both arm the moment B1+B2 land, so they are fixed in the same pass
rather than deferred, but their tests are independent of B1/B2's.

**Every fix gets an `xfail(strict=True)` test demonstrating the defect
first**, per finding, following the D-27/D-37 pattern: red before the fix,
`XPASS(strict)` the moment the fix lands, then the marker comes off for a
real PASS. **No self-MET.** `--layer 7` must stay green; `--full` if memory
allows.

## PART B — BUILT (D-42, same session as the pullback above)

All four fixes landed, each proven against a real test before the fix
existed:

- **B1** (`harness/outcome_classifier.py`): `classify_outcome`'s
  `superseded_ids` filter now reads `transition == "supersede"` and
  `prior_fact_id` — the keys the D-1 delta projection actually carries —
  instead of `write_state`/`fact_id`, which no delta anywhere in the
  codebase ever sets. `eval/test_outcome_classifier_correction.py`: two
  cases carried `xfail(strict=True)`, proven red, then `XPASS(strict)` the
  instant the fix landed, markers removed — 5/5 real PASS.
- **B2(i)** (`harness/curator_shadow.py`): `train_weights` now returns a
  third value (`len(examples)`, offered before gating); `_weights_for`
  reports a new regime, `"gate_refused"`, distinct from `"cold_start"`,
  exactly when events crossed the threshold, examples were offered, and
  none were admitted. `eval/test_curator_shadow_regime.py` (monkeypatch —
  the pre-fix collapse was confirmed directly against the committed source
  rather than via a live xfail-red run, since the fix changes
  `train_weights`' return arity): 4/4 PASS, including the exact D-41
  reproduction and controls for below-threshold, zero-offered, and the
  real-trained-fit path.
- **B2(ii)** (`scripts/register_curator_shadow_model.py`, new): the
  deliberate operator act — register / retire / show — never imported by
  any training-path code. Tested by hand against a scratch copy of the
  registry (never the live file, per D-41's own write-side-effect
  caution); live registry confirmed untouched afterward.
- **B3** (`harness/curator_shadow.py`): `_WEIGHT_CACHE`'s key is now
  `(household_id, n_events // 50)`, not a bare integer; `shadow_score_turn`
  resolves the requester's own household via `get_member_by_id` before
  calling `_weights_for`, falling back to `DEFAULT_HOUSEHOLD_ID` on an
  unresolvable member (the existing safe default). Test added to
  `eval/test_curator_shadow_regime.py`: two households landing in the same
  event bucket now get materially different fits — the exact shape D-41
  proved live by object identity.
- **B4** (`harness/curator_shadow.py`, `eval/harnesslib/layer7_crypto.py`,
  `eval/harnesslib/harness_audit.py`): (i) `historical_acceptance` clamped
  to `[0.0, 1.0]` at the point it is computed; (ii) `validate_shadow_output`
  gained an optional `scores` parameter and, when supplied, asserts
  `ranking` matches score-descending order, not just membership — wired at
  the one production call site and strengthened in the CS1 scenario's own
  assertion; (iii) both metamorphic checks (the CS1 scenario's sub-check
  and the `cs1_query_reword` audit probe) rewritten to prove a genuine
  `sio_attribute` dependency (an unrelated attribute measurably moves a
  trained ranking) plus a structural, code-object-level check that
  `extract_features` carries no query-text-shaped name anywhere — replacing
  two byte-identical calls and a bare variable-name string match.
  `eval/test_curator_shadow_value_and_order.py`: 7/7 PASS.

**44 test cases across 4 files**, wired into `scripts/run_harness.sh`
alongside the D-37 isolation battery so a regression on any of them fails
the run before the harness even starts, not merely fails a hand-run
`pytest` invocation. `--layer 7`: L7 27/27, AUDIT 8/8 (59 checks, 0 missing
artifacts, unchanged), LI1 PASS, CS1 PASS, RATCHET PASS. `--full` NOT run
this pass — 0.08GB free, well under the 2GB TD-129 threshold; not forced.

**Not self-MET. Staged for Bill.** Re-earning MET now additionally requires
`--full` green on top of everything above.

## `--full` RESULTS (D-43, 2026-07-30) — STAGED FOR BILL, NOT SELF-MET

Memory freed the D-38 way: three idle Ollama models unloaded on the dev
daemon (11434) only — `qwen2.5:7b`, `qwen2.5:3b`, `nomic-embed-text`; the
frozen demo daemon (11435, `qwen2.5:7b` loaded "Forever") untouched and
confirmed unchanged before and after. 0.39GB → 2.31GB free, clearing the
2GB TD-129 threshold. Both daemons confirmed still listening throughout.

`scripts/run_harness.sh --full`, exit 0:

- **Standing batteries (pre-harness, all 4 files, 44 cases): PASS.**
- **`--layer 7`: L7 27/27, L7V2 27/28 (1 pre-existing opt-in skip).**
- **All 5 ABSOLUTE checks PASS: G0, PSA1, CTX-STRIP, LI1, CS1.**
- **AUDIT 8/8 — 59 checks, 0 missing artifacts, 35 debt-flagged (unchanged).**
- **RATCHET PASS — no scenario regressed vs baseline.**

Two items observed, both pre-existing and unrelated to this REQ, named so
they are not mistaken for new regressions: `L1:P2` iteration `i019`
FAIL — the same documented async-write-timing race named in
REQ_HARNESS_DISCIPLINE's own MET report and in the D-38 `--full` run
(identical iteration index; `eval/harness_baseline.json` records
`"L1:P2": false`, so RATCHET does not score it); `L2:three_zone_demo.T02`
FLAKE — explicitly named and quarantined as TD-125 (OPEN, a documented Groq
extraction false-negative on multi-party declaratives, already an accepted
flaky scenario, not new).

**The proof the scorer can now learn**, run live against the actual fixed
pipeline (not re-stating the standing-battery unit tests above, a separate
end-to-end construction): a two-turn history where turn 0 has the shadow
scorer's own logged ranking (`curator_shadow.ranking`, length 2 — the real
shape `shadow_score_turn` produces) and turn 1 is a genuine supersede of one
of turn 0's facts, built with the exact delta shape
`harness.fact_change` produces in production (`transition`/`prior_fact_id`,
not the `write_state`/`fact_id` keys D-41 found nothing ever sets):

```
classify_outcome() on the real supersede:
  {'kind': 'correction', 'target_fact_ids': ['f-PRIOR'], 'target_turn_ids': ['t0']}

build_training_examples() labels:
  fact_id='f-PRIOR' label=0   <- the corrected fact, correctly labeled 0
  fact_id='f-OTHER' label=1
  fact_id='f-NEW'   label=1

shadow_outcome_agreement(): 0.0   <- a real, hand-verifiable number, not None
```

The `0.0` is not a placeholder — it is the CORRECT value for this fixture:
turn 0's ranking put the fact that later got corrected (`f-PRIOR`) ranked
*above* the fact that didn't (`f-OTHER`) — the wrong direction — so the one
qualifying (corrected, accepted) pair scores as disagreement, `0/1 = 0.0`.
Before the D-42 fix, this same construction produced `outcome.kind: None`,
every label `1` (including `f-PRIOR`'s), and `shadow_outcome_agreement`
returning `None` on any real log — exactly D-41's finding. The mechanism
that was structurally dead now runs correctly end to end.

Both preconditions this REQ's Part B section named for re-earning MET are
now demonstrated: the four fixes built and tested (D-42), and `--full`
green (D-43, above).

**Status: BUILT, not MET.** D-33's build stands — nothing here is being
un-built, and the honest properties named above (shadow, value-blind,
cold-start-correct, fail-closed) remain true and remain the REQ's real
partial credit. What is withdrawn is the claim that the learner in the
name "Curator Stage 2 Shadow Metadata Scorer" is currently capable of
learning anything.

## MET-Ruling (WITHDRAWN by D-42, above): Bill, 2026-07-30 (D-39 dispatch)

MET against all 9 acceptance items (D-33's own assessment) with the one
item left open at build time — `--full` — now closed:

- **Shadow-proven, structurally cannot act.** Zero diff to prompt assembly:
  the same fixture turn run with the scorer on vs off produces
  byte-identical `prompt_fact_ids` and system prompt. The only production
  reference to `shadow_score_turn` is inside the post-reply record-emit
  closure in `server/voice_orch.py`; no import or call reaches prompt
  assembly.
- **Cold-start byte-identical to the rule order.** Below the outcome-event
  threshold, `COLD_WEIGHTS` reproduces `injected_fact_ids`'s order exactly —
  "no data" degrades to today's behavior, per the memo's own cold-start
  rule.
- **Routes every training example through the now-hardened isolation gate.**
  `train_weights` calls `check_training_example` unconditionally; a
  gate-rejected example is dropped and never reaches the fit
  (`_fit_weights`, module-private, bypassed only by the CS1 fault twin on
  purpose to prove the gate matters). D-38 added the two-line
  `model_resolver` passthrough so this now routes through D-37's
  target-side-hardened gate, not the pre-D-37 example-only version — CS1's
  own `--full` PASS (below) is direct evidence the passthrough works, not an
  assumption.
- **`--full` GREEN (D-38, 2026-07-30), closing the one item open at D-33
  build time** (then REFUSED by TD-129 at 0.10GB free). CS1 PASS, all 4
  ABSOLUTE checks PASS, the D-37-wired 27-case isolation battery 27/27
  zero-xfail, AUDIT 8/8 unchanged, RATCHET PASS — no scenario regressed vs
  baseline. Full run detail in this doc's own "UPDATE 2026-07-30 (D-33...)"
  section, item 9.

Evidence trail: D-33 built and self-assessed against all 9 items but did not
self-MET; D-38 cleared the `--full` memory block (same window as
`REQ_LEARNER_TARGET_AUTHENTICATION`'s D-38 run) and ran it green; Bill ruled
MET on that evidence (D-39).
Reconciled-Against: roadmap f315d3b (2026-07-30);
HIP_CuratorResearch__learned-retrieval-training-federation__v20260728_1045.md
§7.1/§7.2/§7.5 (Stage 2)/§7.6; REQ_RETRIEVAL_OUTCOME_INSTRUMENTATION (MET —
Stage 0, the training-signal and cold-start-reference source);
REQ_LEARNER_SIGNAL_ISOLATION (MET 2026-07-29 D-31b, with the named
members.household_id data limit — the gate this scorer must route every
training example through); REQ_HARNESS_DISCIPLINE (MET — the Four and
AUDIT:four-part-roster, eval/harness.py:536). Read-only this filing:
harness/learner_isolation.py (check_training_example / check_training_batch,
GATE_DECISION_FEATURE_KEYS, POST_GATE_LABEL),
eval/harnesslib/retrieval_outcome.py, eval/harnesslib/check_registry.py
(L7:LI1 entry). REQ ONLY — no scorer code in this filing, per the dispatch's
own words.

## UPDATE 2026-07-30 (D-33 — BUILT, assessed against all 9 items; staged for Bill, NOT self-MET)

Built to this REQ under Bill's D-33 rulings: **sensitivity INCLUDED** as the
tenth feature (metadata, not value text — closes OPEN QUESTION 2);
guard/intent context stays excluded per LI1 ruling 4. Two build choices
this filing names (per the REQ's own design): OPEN QUESTION 3 resolved in
the build as a new optional `curator_shadow` field on the epistemic record
(Stage-0 pattern — per-turn adjacency to `injected_fact_ids` for free);
OPEN QUESTION 4 implemented as DROP-AND-LOG interim (a gate-rejected
example is excluded from the fit and its violation string logged/returned;
it is provably absent from what the fit receives) — Bill's ruling can flip
this to refuse-batch without touching the gate.

**Built:** `harness/curator_shadow.py` (new — ten-key allowlisted feature
extractor, deterministic linear/logistic scorer, cold-start weights,
`train_weights` gate-routed training, `validate_shadow_output` — the
in-path curated⊆admitted assertion, `shadow_score_turn` — the one entry
point); `eval/harnesslib/curator_agreement.py` (new — the
agreement-with-outcome metric + hand-computed self-test);
`harness/epistemic_record.py` (additive: `curator_shadow` kwarg/field;
`sensitivity`/`write_state` metadata keys on fact entries so training
features reconstruct from records); `server/voice_orch.py` (the shadow
hook at the record-emit choke point — post-prompt, post-reply — plus a
telemetry-only `sio_attribute` line and three `curator_sio_attribute`
kwargs, popped before the record builder ever sees them);
`eval/harnesslib/layer7_crypto.py` (L7:CS1, ABSOLUTE tier);
`eval/harnesslib/check_registry.py` (L7:CS1 four-artifact entry);
`eval/harnesslib/harness_audit.py` (`cs1_query_reword` executable probe).

**Assessment against the 9 acceptance items** (evidence:
`/tmp/hip_harness_20260730_0740.log`, live records in `logs/turns_demo.jsonl`):

1. **Input = exactly injection.allowed — HOLDS.** The hook reads
   `injection_result.allowed` at the emit choke point, downstream of
   INJ-1..7; the scorer has no fetch/add path. L7:CS1 (i)/(ii); live turn:
   shadow set == admitted set (6 real facts).
2. **curated⊆admitted asserted — HOLDS.** `validate_shadow_output` runs
   in-path on every scored turn (violation ⇒ ranking suppressed
   fail-closed + flagged) AND as the L7:CS1 fault twin: an out-of-set
   fact_id flagged BY NAME (red), real output passes (green).
3. **Metadata-only, declared ten keys — HOLDS, one named deviation.**
   Allowlist enforced (undeclared key refused by name); gate-decision and
   value-derived keys refused (twins red); extractor output is exactly the
   ten keys and validates clean; value-blindness proven (metadata-identical
   facts, different values ⇒ byte-identical feature dicts). NAMED
   DEVIATION: `recency` is carried as RANK in the rule order, not raw
   `valid_from` age — the retrieval dict carries no timestamp, and the rule
   order IS timestamp-DESC (Stage 0 item 3), so rank preserves exactly the
   ordering information; declared in the coverage entry, not hidden.
4. **Shadow only — HOLDS, proven live.** Same real turn run with
   HIP_CURATOR_SHADOW=0 and =1: `prompt_fact_ids` and `injected_fact_ids`
   byte-identical both ways; scorer-off record carries `curator_shadow:
   null`, scorer-on logs ranking/scores/features BESIDE the rule ranking
   in the same record. Static-scan twin: a synthetic prompt-assembly
   source calling the scorer is flagged (red); in the real sources the
   scorer is referenced only inside the emit hook, zero references in
   `harness/orchestrator.py` (green). The hook runs after prompt assembly
   and reply generation by construction.
5. **Every training example through the MET gate — HOLDS.**
   `train_weights` is the only training entry point; every example passes
   `check_training_example` (production default = the D-30
   `RegistryProvenanceResolver` — the authenticity fix is inherited, not
   reimplemented). No-bypass twin: the gated fit drops the cross-household
   example (crossing named) and equals the clean fit exactly; the
   deliberate `_fit_weights` bypass yields different weights. The D-31b
   limit is inherited and named: member-owned facts fail CLOSED until
   `members.household_id` is populated — household-scope-only training.
6. **Cold start byte-identical — HOLDS, fixture AND live.** L7:CS1 (i):
   fixture ranking == rule order exactly; live real-graph turn (0 outcome
   events, regime `cold_start`): shadow ranking byte-identical to
   `injected_fact_ids`.
7. **Agreement-with-outcome metric — HOLDS.**
   `shadow_outcome_agreement` with the formula fixed in its docstring;
   hand-computed fixture expectations (1.0 / 0.0 / 0.5 / None) match
   exactly, wired into L7:CS1.
8. **The Four — ALL PRESENT.** Twins: subset-escape, banned/undeclared
   feature keys, prompt-touch scan, gate no-bypass — each red on command,
   green on removal. Ground-truth fixture: hand-authored four-fact fixture
   with decoy SECRET-* values + the hand-computed agreement numbers.
   Coverage entry: L7:CS1 in `check_registry.py`, uncovered slices named
   honestly (trained regime not yet live on a real graph — no household
   has ~100 outcome events; key_scope coarse household-vs-member;
   per-scope-audience architecture awaits Bill). Metamorphic: in-scenario
   + the `cs1_query_reword` executable probe (scoring is query-text-free
   by signature).
9. **Audit + ratchet — LAYER 7 GREEN; --full NOW GREEN (D-38, 2026-07-30).**
   `AUDIT:four-part-roster`: 59 checks enumerated (58 → 59, CS1 added),
   ZERO CS1 flags, debt-flagged gaps unchanged at 35 — the audit script
   passes the new check. `--layer 7`: L7 27/27 (CS1 joins the ABSOLUTE
   roster with G0/PSA1/CTX-STRIP/LI1), AUDIT 8/8, L7V2 27/28 (1
   pre-existing opt-in skip), SCHEMA/VOICE green, **RATCHET PASS — no
   scenario regressed**. `--full` was REFUSED at build time by the runner's
   TD-129 guard (0.10GB pages-free) and DEFERRED to a clean memory window,
   the D-30 precedent.

   **D-38 cleared that window and ran it.** Memory freed by unloading three
   idle Ollama models on the dev daemon (11434) — the frozen demo daemon
   (11435) untouched, already empty; 0.32GB → 3.83GB free, both daemons
   confirmed still listening. `scripts/run_harness.sh --full`, exit 0:
   **CS1 PASS**, all 4 ABSOLUTE checks (G0/PSA1/CTX-STRIP/LI1) PASS, the
   D-37-wired 27-case adversarial isolation battery 27/27 zero-xfail (runs
   pre-harness on every pass), AUDIT 8/8 unchanged, `care_coordination.T01`/
   `T02` (the Groq-400 history) both PASS, **RATCHET PASS — no scenario
   regressed vs baseline.** Two unrelated, pre-existing items observed and
   named, neither a regression: `L1:P2` iteration `i019` FAILs on the same
   documented async-write-timing race the REQ_HARNESS_DISCIPLINE MET report
   already names (baseline records `"L1:P2": false`, so RATCHET does not
   score it); `psa1_probe_owner` decrypt-skip tracebacks are that scenario's
   own synthetic fault-injection owner correctly failing to decrypt (no
   `household_key_wraps` row by construction) — caught, logged, not a crash.

   One code change in this window, made under D-37 (a different REQ) and
   noted here for completeness: `curator_shadow.train_weights` gained a
   `model_resolver` passthrough parameter so it can forward the new
   target-side authentication D-37 added to the isolation gate. Two lines,
   no behavior change to anything CS1 tests — CS1 PASS above is evidence,
   not assumption. The live-path mitigation named at build time (one
   additive never-raise hook at the emit choke point, two real
   `process_text_query` turns green end-to-end) still stands; `--full`
   above is the fuller proof that mitigation was standing in for.

**Status: BUILT, not MET (D-39's MET WITHDRAWN by D-42).** Both open
verification items named at build time — the wired isolation battery and
`--full` — were demonstrated green (D-37, D-38 respectively), which was the
basis for Bill's D-39 MET ruling. D-40's external review + D-41's
verification subsequently found the scorer's learning substrate is
structurally dead (see the dated D-42 block at the top of this document);
Bill pulled the ruling back on that finding. The battery/`--full` evidence
above remains accurate — it just was not sufficient, because nothing in
the acceptance test exercised whether a real `correction` outcome could
ever be produced.

## THE REQUIREMENT

Bill's own words, verbatim, from the D-32 dispatch that opened this REQ:

> Read the Curator memo §7.5 Stage 2 + REQ_RETRIEVAL_OUTCOME_INSTRUMENTATION
> (Stage 0, MET) + REQ_LEARNER_SIGNAL_ISOLATION (the gate, MET). Write
> REQ_CURATOR_SHADOW_SCORER specifying:
> - A GBDT/logistic METADATA-ONLY scorer over injection.allowed, strictly
>   downstream of INJ-1..7 (can only narrow, never source). Features: attribute,
>   attribute-family match, trust rung, confidence, recency, supersession,
>   subject==requester, key class/scope, historical acceptance rate. NO value text.
> - SHADOW MODE ONLY: scores every turn, logs its ranking next to the rule ranking,
>   NEVER touches the prompt. Kill switch is implicit (it can't act).
> - Cold-start rule: below ~100 outcome events the scorer's weights reproduce the
>   current deterministic rule order — "no data" degrades to exactly today's behavior.
> - Every training example passes the MET isolation gate (learner_isolation.py)
>   before use — the scorer inherits the provenance-authenticity fix. State this.
> - Acceptance: shadow ranking logged per turn; agreement-with-outcome metric;
>   curated⊆admitted invariant asserted; and the full REQ_HARNESS_DISCIPLINE Four
>   (fault twin, ground-truth fixture, coverage entry, metamorphic wrapper) BEFORE
>   any MET. No MET proposed until the audit script passes it.

The memo section this stages, `HIP_CuratorResearch__*__v20260728_1045.md`
§7.5, quoted verbatim as the design source:

> **Stage 2 — shadow Curator (learner exists, cannot act).** Per-household
> GBDT over the 7.1 feature set, trained on Stage-0 logs, running in shadow:
> score every turn, log its ranking next to the rule ranking, **never touch
> the prompt**. Offline eval = agreement with subsequent outcomes. Cold
> start: below ~100 outcome events (the Joachims-derived threshold from
> Part 2), the scorer IS the rules — hand-set weights reproducing today's
> deterministic order, so "no data yet" degrades to exactly current behavior.

Expanded: this REQ specifies the first artifact in this codebase that is a
learner. Everything before it was scaffolding built in the correct order:
Stage 0 (MET) made outcomes measurable; Stage 1 (MET) built the standing
refusal gate BEFORE any learner existed, precisely so that this build meets
it on its first `--layer 7`. The scorer this REQ specifies scores and logs —
it has no path to act. Acting (Stage 3: live narrowing, kill-switched) is a
separate future REQ behind Bill's gates and is NOT authorized here.

**Feature-list reconciliation, stated so it cannot be mis-built:** memo §7.1's
feature list includes two items the dispatch's list above deliberately omits.
(1) "guard/intent context" is EXCLUDED PERMANENTLY: the memo predates Bill's
D-23 ruling 4 (REQ_LEARNER_SIGNAL_ISOLATION), which bans INJ outcomes, deny
reasons, and guard flags from any future feature space by key vocabulary,
recursively — enforced today by `GATE_DECISION_FEATURE_KEYS` in
`harness/learner_isolation.py`. The ruling supersedes the memo. (2)
"sensitivity" is omitted from the dispatch's list and therefore from this
REQ's feature space; whether it joins is Bill's call (OPEN QUESTIONS, 2).
The feature space is the dispatch's nine, exactly — no additions without a
new ruling.

## THE ACCEPTANCE TEST

Pass/fail per item; any single failure is FAIL; no partial credit.

**1. Placement by dataflow: input is exactly `injection.allowed`.**
The scorer's candidate input for a turn is the post-INJ-1..7 admitted set —
taken strictly downstream of `evaluate_injection_contract`
(`harness/injection_contract.py`), the same object whose order
`injected_fact_ids` records (Stage 0, acceptance item 3). No code path lets
the scorer add, fetch, or substitute a candidate — it can only reorder/score
what the contract admitted. Observable: a fixture turn with admitted set A,
against a graph/fixture containing authorized-but-not-admitted and
unauthorized facts outside A; the shadow output's fact_id set is a subset of
A (permutation or pruning of A, never a superset). FAIL: any fact_id outside
A appears in any shadow output, ever.

**2. curated ⊆ admitted, asserted — not assumed.**
The Stage-3 memo names this invariant for the live scorer; this REQ pulls it
forward into shadow so it is proven before anything can act. Per turn, the
logged shadow ranking's fact_id set ⊆ that turn's `admitted[]`, asserted in
the shadow logging path itself AND checked as a layer-7 scenario with its
own fault-injection twin (item 8). Observable: the twin constructs a shadow
output containing one out-of-admitted-set fact_id → check red, naming the
fact_id and turn; removing it → green. FAIL: either direction fails.

**3. Metadata-only feature space — NO value text.**
The feature extractor's vocabulary is a DECLARED frozenset of exactly the
nine dispatch features: `attribute`, attribute-family match (to the SIO
attribute), trust rung, confidence, recency (`valid_from` age), supersession
state, `subject == requester`, key class/scope, historical acceptance rate
(from Stage 0's outcome fields — the fraction of prior injections of this
fact not followed by a correction/override, `accepted_answer_rate`'s
per-fact analog). Observables, each pass/fail:
  - The extractor never reads a fact's value, plaintext, ciphertext, or
    embedding-of-value, and never calls the vault decrypt path (TD-030:
    values never render outside vault decrypt). Verified structurally (the
    extractor module imports nothing from the decrypt path; grep for the
    decrypt entry points in the extractor comes back empty) AND by fixture:
    two facts identical in all nine features but different values produce
    byte-identical feature vectors.
  - No feature key is in `GATE_DECISION_FEATURE_KEYS` — the gate's own
    recursive key-vocabulary check runs against every training example
    (inherited, item 5) AND a probe feeds a feature dict containing a
    banned key (e.g. `guard_kind`) → refused/red.
  - A probe feeds a feature dict containing a value-derived key (e.g.
    `value_text`, `value_embedding`) → refused/red. This requires the
    extractor (or gate wrapper) to enforce a declared-vocabulary allowlist:
    any key NOT in the declared frozenset is a refusal, not a pass-through.

**4. Shadow only — structurally cannot act.**
  - Zero diff to prompt assembly: for any turn, `prompt_fact_ids`, the
    assembled prompt, and the reply path are byte-identical with the scorer
    enabled vs disabled. Observable: the same fixture turn run both ways,
    records compared — identical except the shadow-log artifact itself.
  - The shadow ranking is logged EVERY turn, next to the rule ranking:
    keyed to the turn, alongside `injected_fact_ids` (whose order IS the
    rule ranking, per Stage 0 item 3's proven claim), so the two orders are
    comparable per-turn without a join. Where it is logged (new optional
    epistemic-record field, Stage-0 pattern, vs sidecar log) is OPEN
    QUESTIONS 3 — either way this item's observable holds: for a live turn,
    both orders retrievable, keyed to the same turn id.
  - Kill switch is implicit: there is NO code path from scorer output to
    prompt assembly. Verified structurally: the scoring module is imported
    only by the shadow-logging call site; grep/callgraph shows no import or
    call from `orchestrator.py`'s prompt-assembly path or any
    injection-contract path. The fault twin for this property (item 8)
    synthetically wires scorer output toward the prompt path → red.

**5. Every training example passes the MET isolation gate — inherited, not
reimplemented.**
Every example reaches any fit/update/weight computation ONLY through
`harness/learner_isolation.py`'s `check_training_example` /
`check_training_batch`, with provenance DERIVED via the production
`RegistryProvenanceResolver` — the scorer thereby inherits the D-30
provenance-authenticity fix (forged household stamp ignored and flagged,
audience from live rosters `removed_at IS NULL`, missing/unresolvable
fact_id rejected fail-closed, shared-base carve-out requires the positive
verified-public marker) and the D-23 rulings (labels
`label_source == "post_gate_outcome"`, gate-decision keys refused
recursively). Observables:
  - A training batch containing one gate-rejected example (forged
    provenance, pooled household, scope crossing, missing fact_id) is
    handled per the batch policy this build names (drop-exactly-that-example
    with the gate's violation string logged, or refuse-the-batch — OPEN
    QUESTIONS 4), and the rejected example provably never reaches the fit:
    the resulting weights are identical to a run where that example was
    never offered.
  - No-bypass is fault-twinned (item 8): a synthetic path that feeds an
    example to the fit without the gate → red.
  - INHERITED NAMED LIMIT, restated from the D-31b MET ruling: member-owned
    facts resolve household=None until enrollment populates
    `members.household_id`, so the production resolver FAILS CLOSED on them
    — member-scoped examples are safely REJECTED, never leaked. At build
    time this scorer therefore trains on household-scope examples only.
    That is inherited safe behavior and a DATA prerequisite, not a defect
    this REQ fixes or works around.

**6. Cold-start rule: "no data" degrades to exactly today's behavior.**
Below ~100 outcome events for the household (the Joachims-derived threshold,
memo Part 2/§7.5), the scorer's weights are hand-set such that its output
order reproduces the current deterministic rule order — most-recent-first
(`ORDER BY f.timestamp DESC`, preserved order-preserving through the
contract, per Stage 0 item 3's live proof). Observable: a fixture household
with fewer than 100 outcome events → shadow ranking is byte-identical to
`injected_fact_ids` order on every turn; a fixture at/above the threshold is
permitted to diverge. The event count is the ONLY thing that may change
which regime a household is in. FAIL: any sub-threshold turn where the two
orders differ.

**7. Agreement-with-outcome metric (the memo's "offline eval").**
A read-only function in `eval/harnesslib/` computes agreement between logged
shadow rankings and subsequent Stage-0 outcomes (correction / override /
accepted-answer), fixture-tested against a hand-computed expectation exactly
(Stage 0 item 2's pattern — a synthetic sequence where the shadow ranking
demoted a later-corrected fact scores measurably better than one that
promoted it; the fixture's expected number is computed by hand and must
match, not just "runs without error"). The exact formula is fixed in the
build and stated in the function's docstring; the acceptance is the
hand-computed match, so the formula cannot be arguable after the fact.

**8. The full REQ_HARNESS_DISCIPLINE Four, BEFORE any MET.**
  1. FAULT-INJECTION TWIN(s), red on command / green on removal, each
     naming its violation: out-of-admitted-set candidate in shadow output
     (item 2); banned/undeclared feature key (item 3); scorer output wired
     toward the prompt path (item 4); gate-bypassed training example
     (item 5); sub-threshold order divergence (item 6).
  2. GROUND-TRUTH FIXTURE, human-verified, never model-graded: extend the
     existing two-household (hh-alpha/hh-beta) + alice/bob/mary fixtures
     with outcome-event sequences whose correct shadow behaviors (orders,
     counts, agreement numbers) are hand-computed.
  3. COVERAGE ENTRY in `check_registry.py`, declaring the covered slice
     honestly: which scopes (household-scope-only training per the named
     data limit), which feature keys are probed, cold-start vs
     post-threshold regimes, and naming what is NOT covered (member-scoped
     training — blocked on the data prerequisite; live-graph training runs)
     rather than folding it into a covered row.
  4. METAMORPHIC WRAPPER: meaning-preserving rewordings of the query behind
     a turn change neither the isolation verdicts nor the invariant results
     (MT1/MT2 pattern; `li1_query_reword` precedent).

**9. Audit and ratchet — the MET precondition.**
The new check(s) appear in `AUDIT:four-part-roster` (eval/harness.py:536)
with all four columns satisfied, zero new gaps; `scripts/run_harness.sh
--layer 7` and the full RATCHET stay green before and after; `--full` per
Requirements Discipline item 12 before any MET assessment. **No MET is
proposed until the four-part audit script passes the new check(s)** — and
MET itself is Bill's ruling, never self-marked.

## WHAT'S ALREADY DONE (do not redo)

- **Stage 0 is MET** (`REQ_RETRIEVAL_OUTCOME_INSTRUMENTATION`): `outcome`
  fields live-wired on every record via `classify_outcome()`
  (harness/outcome_classifier.py, called from voice_orch.py's
  emit_epistemic_record choke point); `accepted_answer_rate` /
  `retrieval_failure_rate` / `candidates_per_family` in
  `eval/harnesslib/retrieval_outcome.py`; and the rule ranking order proven
  to BE `injected_fact_ids` order (timestamp DESC, order-preserving chain,
  live-verified against Neo4j). The scorer's training labels, its
  historical-acceptance feature, and its cold-start reference order all
  already exist as logged artifacts. Do not rebuild any of them.
- **Stage 1, the gate, is MET** (D-31b): `harness/learner_isolation.py`
  (check_training_example / check_training_batch, GATE_DECISION_FEATURE_KEYS,
  POST_GATE_LABEL, injectable ProvenanceResolver with the production
  registry-chain resolver), L7:LI1 ABSOLUTE-tier (13 sub-checks incl. the
  D-30 authenticity/currency twins), the 23-case adversarial battery all
  real-PASS (`eval/test_learner_isolation_adversarial.py`), coverage entry
  naming its uncovered slices. The gate predates this learner BY DESIGN —
  this build meets it on its first `--layer 7`; it does not modify it.
- **REQ_HARNESS_DISCIPLINE is MET** — the Four and their mechanical
  enforcement (`AUDIT:four-part-roster` wired into every run) are the
  quality bar items 8–9 come from. Do not invent a different one.
- **The ABSOLUTE-tier wiring pattern exists** (G0/PSA1/CTX-STRIP/LI1 in
  `eval/harnesslib/layer7_crypto.py` run(), `--accept` mechanically
  refused) — reuse it for any new hard-zero check, don't parallel it.
- **No learner/scorer/ranker code exists in this codebase today** (verified
  through the LI1 history and re-affirmed by this filing's read-only trace)
  — there is nothing to redo; this REQ is the first specification of one.

## WHAT'S KNOWN BROKEN

- **Nothing computes a learned score today.** The scorer, its feature
  extractor, the shadow log, the agreement metric, and the cold-start
  weight set do not exist. That is the gap this REQ scopes — and only in
  shadow.
- **Gate A is NOT decided, and this REQ does not decide it.** Memo §7.5
  puts Bill's entry decision between Stage 0's measurement and any learner:
  "Stage 0's measurement either justifies opening the moat track or it
  doesn't." The trip point (which failure rate, what window — §7.6 item 1)
  is un-set. This REQ makes Stage 2 buildable the day Bill opens the gate;
  FILING IT DOES NOT OPEN IT. A build dispatch against this REQ before that
  decision jumps the queue and must say so (Backlog Discipline).
- **Two memo features are excluded** (reconciliation in THE REQUIREMENT):
  guard/intent context permanently (LI1 ruling 4 / GATE_DECISION_FEATURE_KEYS
  — the ruling postdates and supersedes the memo), sensitivity pending
  Bill's word.
- **Outcome history is thin.** Stage 0 landed 2026-07-28; historical
  acceptance rate and training labels exist only for turns since. Early
  shadow operation will be cold-start by definition — which is exactly what
  the cold-start rule is for, not a blocker.
- **Member-scoped training is blocked on data, fail-closed** (the D-31b
  named limit): until enrollment populates `members.household_id`, the
  gate rejects member-owned examples. Household-scope-only training is the
  honest initial regime; the coverage entry names it.
- **Model-per-what is half-decided.** LI1's rulings answer the violation
  class (intra-household scope crossing = same class; audiences are
  rosters; broader-into-narrower admissible), so the minimum compliant
  Stage 2 build is one scorer per household trained only on examples whose
  audience covers the household-circle roster — which is also all the gate
  currently admits under the data limit. One-model-per-scope-audience
  remains open (LI1 OQ, memo §7.6 item 2) and is NOT settled here; named so
  it is decided deliberately, not discovered mid-build.

## CONSTRAINTS

- **REQ only this pass — no scorer code.** The dispatch's own words.
- **Shadow may never touch the prompt.** Zero change to what any turn
  retrieves, ranks into the prompt, or sends to any model. The scorer's
  entire observable output is its log line. Any diff to prompt assembly is
  a FAIL of this REQ regardless of what else works.
- **The gate is the law, not a convention:** no training example reaches
  any fit except through check_training_example/check_training_batch; no
  feature key from GATE_DECISION_FEATURE_KEYS; labels post_gate_outcome
  only; provenance derived, never caller-supplied.
- **No value text, ever** — TD-030's discipline extends to the feature
  space: no decrypt calls, no value-derived features, no embedding of
  values.
- **The working path is sacred:** RATCHET green before/after; layer 7 and
  AUDIT stay green; the demo on main and graph 7689 untouched; no changes
  to injection_contract.py's decisions or read_user_facts' order.
- **This REQ does not authorize Stage 3** (live narrowing) — that requires
  its own REQ, the curated⊆admitted invariant already proven here in
  shadow, and Bill's explicit gate. It also does not authorize pooling of
  any kind (Gate B territory, memo §7.5).
- **Do not mark this REQ MET.** Assess against the acceptance test and
  report; Bill decides. No MET is even PROPOSED until AUDIT:four-part-roster
  passes the new checks (acceptance item 9).

## OPEN QUESTIONS FOR BILL

1. **Gate A's trip point** (§7.6 item 1): what measured D-24/T02-class
   failure rate, over what window, opens the Stage-2 build. Stage 0's
   instrument is live; the number is yours.
2. **Does `sensitivity` join the feature set?** Memo §7.1 lists it; your
   dispatch list omits it; this REQ excludes it pending your word.
3. **Where does the shadow ranking live** — a new optional field on the
   epistemic record (additive, Stage-0 pattern, per-turn adjacency for
   free) or a sidecar log? Metadata-only rankings avoid row-31's sealing
   collision either way, but the record's schema is governed surface.
4. **Batch policy on a gate-rejected example:** drop-exactly-that-example
   (log the violation string, train on the remainder) or refuse the whole
   batch? Drop-and-log maximizes signal; refuse-batch is the more
   conservative posture toward a poisoned source.
