# FABLE_ShadowScorerReview: Adversarial Review of the Curator Stage 2 Shadow Scorer
Status: BUILT
Branch: roadmap
Reconciled-Against: ae74e48 (2026-07-30) — code-identical to 9cbb9ec for every
file reviewed. The pin contains the D-33 shadow-scorer build (9d867f8), the
D-37 target-side authentication fix (a0850c1), and the D-38 `model_resolver`
passthrough (9cbb9ec). D-39 (ae74e48) changed documentation only — "No code
changed this session" — so the reviewed snapshot is the committed code.

## What this document is

D-40 routed the built Curator Stage 2 shadow scorer to Fable for adversarial
code review and captured the response. The review(s) below are reproduced
**VERBATIM** as Fable returned them. They are the artifact; this header is
the only text in this file not written by a reviewer.

**Every finding here is UNVERIFIED by the routing session.** Per the D-40
dispatch's own instruction — "Do NOT act on findings this pass" — nothing
below has been independently confirmed, reproduced, or tested by the session
that filed this document. The reviewers make specific, checkable claims about
line numbers, dataflow, and code paths. Treat every one as a claim to verify,
not a measurement to trust. That verification is its own dispatch.

**No REQ status is proposed, implied, or changed by this document.** This
cuts in both directions and the direction matters here: D-39 (ae74e48, Bill's
ruling) marked REQ_CURATOR_SHADOW_SCORER and REQ_LEARNER_TARGET_AUTHENTICATION
**MET** roughly an hour before this review was routed. A review does not mark
a REQ MET and equally does not un-MET one. Findings below are input to Bill's
judgment about already-MET requirements, not a reversal of it. Both reviewers
were instructed not to propose or imply any status.

## Provenance and method

- Routed 2026-07-30 ~11:05 MDT from `~/hip-roadmap`, branch `roadmap`, by a
  Claude Code session running as bill-ai on [REDACTED-MACHINE-NAME].
- Two independent Fable agents, run in parallel, each given the identical
  D-40 brief and the identical frozen file set. Neither could see the other's
  work or findings. (The dispatch asked for one review; two independent
  reviewers on the same brief is the D-35 precedent and a superset of the
  ask — convergence between two blind reviewers is itself signal, as it was
  in D-35.)
- Both were constrained read-only: no file edits, no harness runs, no pytest,
  no database access, no writing git commands.

## Snapshot fidelity

The dispatch required Fable review a frozen copy, not a moving tree. This
mattered: a **parallel session committed D-39 (ae74e48) while the snapshot
was being taken**, moving HEAD out from under the review. The snapshot was
therefore verified rather than assumed:

- Files were copied to a scratchpad snapshot directory and reviewed there.
- `git diff --quiet HEAD -- harness/ eval/ server/` returned clean at the new
  HEAD, and each copied file was `diff`-confirmed byte-identical to its
  repo counterpart at ae74e48.
- `git diff --name-only 9cbb9ec..ae74e48 -- '*.py'` returned **empty** — D-39
  touched zero Python files.

So the reviewed bytes are the committed bytes at ae74e48, and the findings
apply to committed code, not to a working-tree draft or a superseded version.

## The review target (what was placed in front of the reviewers)

| snapshot file | repo source at ae74e48 |
|---|---|
| `curator_shadow.py` | `harness/curator_shadow.py` (the scorer, `train_weights`, `validate_shadow_output`) |
| `learner_isolation.py` | `harness/learner_isolation.py` (the isolation gate, both resolvers) |
| `model_registry.py` | `harness/model_registry.py` (backs the target-side resolver) |
| `voice_orch__shadow_hook.py.txt` | `server/voice_orch.py` record-emit shadow hook |
| `voice_orch__sio_attribute_telemetry.py.txt` | `server/voice_orch.py` sio_attribute telemetry surface |
| `epistemic_record__curator_shadow_field.py.txt` | `harness/epistemic_record.py` `curator_shadow` field |
| `curator_agreement.py` | `eval/harnesslib/curator_agreement.py` (agreement metric + self-test) |
| `layer7_crypto__L7_CS1_check.py.txt` | `eval/harnesslib/layer7_crypto.py` L7:CS1 scenario |
| `check_registry__L7_CS1_entry.py.txt` | `eval/harnesslib/check_registry.py` L7:CS1 entry |
| `harness_audit__cs1_query_reword_probe.py.txt` | `eval/harnesslib/harness_audit.py` `cs1_query_reword` probe |

Reviewers were permitted read-only reads of the wider repo for context, but
required to anchor findings to the frozen files above.

## The brief, verbatim as routed

> Attack this shadow scorer. It routes every training example through the
> isolation gate — which just had a 7th hole found by external review.
> (a) Can any feature leak cross-household or cross-scope signal — including
> via sensitivity, the metadata keys, or the agreement metric? (b) Can the
> train_weights path be poisoned, or bypass the gate the way the gate's own
> target side was bypassed? (c) Is 'shadow' actually airtight — any path
> where the scorer's output could reach the prompt? (d) Does the cold-start
> byte-identical claim hold under adversarial input? Name attack classes the
> CS1 acceptance test does NOT cover — the gate's coverage had no input-trust
> axis and that's how 7 holes got through.

---
## Convergence map (routing-session framing — NOT reviewer text, NOT verification)

This section is written by the routing session, not by either reviewer. It is
a **reading aid only**. Two blind reviewers agreeing is evidence that a claim
is worth checking first; it is **not** evidence the claim is true. Nothing
below has been verified. Reviewer A numbers findings `F1..F14`; Reviewer B
numbers them `Finding 1..13`. Both label their own confidence in-line; where
they disagree, the disagreement is preserved rather than resolved.

**Independently converged (both reviewers, reached blind):**

| claim | A | B |
|---|---|---|
| The trainer reads features/labels from an unauthenticated `logs/turns_demo.jsonl`; the gate authenticates `fact_id` and nothing about the example's content — same root-cause shape as the prior seven holes | F2 | Finding 1 |
| Gate check V4 (`label_source`) is unfireable: the only producer stamps the exact constant the gate tests | F2 | Finding 1 |
| `register_model` has zero callers, so the production model_id resolves to nothing, every example is refused at V0b, and the trained regime is unreachable — silently, and indistinguishably from cold start | F4 | Finding 4 |
| `_WEIGHT_CACHE` is keyed only on `n_events // 50` — no household, no corpus identity; one artifact serves every household | F3 | Finding 3 |
| `outcome_event_count` is a global unfiltered count, so activity outside a household can flip that household's regime | F3 | Finding 3 |
| The "shadow cannot act" static scan is weak: two files only, two different regexes, span delimited by a movable comment | F8 | Finding 6 |
| …but the shadow property itself **does** hold today — no path from scorer output to prompt | F8/(c) | Finding 6/(c) |
| The metamorphic query-reword check is vacuous in both the scenario and the audit probe (identical calls; the probe's `_reword` loop variable is unused) | F9 | Finding 9 |
| `historical_acceptance` is unbounded (`corrected` is not bounded by `injected`), unclamped, and can carry `inf`/`NaN` into the fit and into the record as invalid JSON | F6 | Findings 8, 9 |
| `validate_shadow_output` is tautological in-path — it compares a list against itself and constrains membership, never order | F10 | Finding 9 |
| `allowed` can carry fact_id-less or duplicate facts, putting `null` in the ranking and silently collapsing `scores`/`features` keys | F10 | Finding 9 |
| Cold-start byte-identity **holds** — `rank` is scorer-generated, so no adversarial fact content can permute the order | (d) | (d) |
| The D-37 empty-set/`frozenset()` shape does **not** recur; the gate's own relationship logic is sound | (b) | (b) |

**Raised by only one reviewer (no second opinion — verify independently):**

- **A only, and A's most consequential claim:** `F1` — the correction/label
  substrate is structurally dead. A traces `_D1_DELTA_FIELDS` and the
  `_store_delta` call site and reports that neither carries `write_state` or
  `fact_id`, so `classify_outcome`'s `superseded_ids` is always empty, so no
  `correction` outcome can ever be emitted. If true this means every training
  label is `1`, `historical_acceptance` is a constant `1.0`, and the agreement
  metric returns `None` on any real log. A cites the live 12-record log as
  supporting evidence. B did not examine the outcome producer.
- **A only:** `F5` (one malformed log line permanently disables the scorer via
  the blanket handler), `F11` (dead caller-asserted `household_id`/`audience`
  still constructed at the `_weights_for` call site — the exact shape of the
  7th hole, left live as decoration), `F12` (`sensitivity`/`write_state` now
  projected onto `withheld[]` denied facts), `F13` (the hook runs synchronously
  inside the ledger's write-ahead window), `F14` (attribute vocabulary not
  re-asserted by the scorer).
- **B only:** `Finding 2` (the feature allowlist is **recursive** for
  gate-decision keys but **top-level-only** for value keys and undeclared keys —
  a nested payload under a declared key validates clean), `Finding 7`
  (`sensitivity == "critical"` misses `_ORDINAL` and encodes to the neutral
  `0.5`, i.e. *below* `"high"`, in the permissive direction), `Finding 10`
  (gate violation strings print live roster membership to stderr),
  `Finding 11` (`COLD_WEIGHTS` is a mutable global that the regime label is
  computed against, so both fail together), `Finding 12` (`HIP_CURATOR_SHADOW`
  is an exact-`"0"` match, and the byte-identical proof's control arm depends
  on it), `Finding 13` (five prose/code divergences: `recorded_at` vs
  `valid_from`, case-sensitive `subject_is_requester`, trust-rung collapse on
  the reconstruction path, the allowlist not running in-path, and
  `_TRUST_ORDINAL` encoding ladder match-order as trust magnitude).
- **B only, and structurally notable:** B's mutation table — ten concrete edits
  to `curator_shadow.py` that B argues CS1 would not catch — plus B's
  observation that CS1's own gate-bypass fixture (`_cs_bad`, pairing one fact's
  features with another's `fact_id`) is built on the very decoupling that makes
  the poisoning in A-F2/B-Finding-1 possible.

**Where the two differ in emphasis rather than substance:** A frames the
central defect as "nobody authenticated the record the example was extracted
from"; B frames it as "the gate authenticates one of three operands." These
are the same finding seen from two angles. Both explicitly note the current
single-user prototype context bounds the practical threat model, and both say
so without softening the structural claim.

**Both reviewers independently declined to propose any REQ status**, as
instructed, and both volunteered that specific properties **hold** — the
shadow placement, the value-blindness of `extract_features`, the cold-start
arithmetic, and the D-30/D-37 gate relationship logic. A calls the gate's own
logic "the strongest thing in this snapshot."

---

# REVIEW 1 of 2 — Reviewer A (verbatim)

# Reviewer A — Adversarial Security Review: Curator Stage 2 Shadow Scorer

## 1. What I reviewed and how

**Target:** frozen snapshot at `/private/tmp/claude-501/-Users-bill-ai/517c9464-b7c5-4c16-a31a-5faa79ed81c7/scratchpad/d40_snapshot/`, pinned to `ae74e48` ("D-39: rule REQ_LEARNER_TARGET_AUTHENTICATION + REQ_CURATOR_SHADOW_SCORER MET"), branch `roadmap`.

**Mode:** read-only. I read files, grepped, and ran text-analysis over source *strings* (regex offsets in `server/voice_orch.py`, key-histogram over `logs/turns_demo.jsonl`). I did not import or execute any target module, did not run the harness or any test, did not start a server, did not touch Neo4j, and made no writes. **I rule on nothing.** These are findings.

**What I traced, end to end:**
- The live dataflow into `build_training_examples`' `features`: `injection_contract` → `injection_result.allowed` → `shadow_score_turn` → `epistemic_record.build_epistemic_record` → `log_epistemic_record` → `logs/turns_demo.jsonl` → `load_records` → `logged.get(fid)` → `train_weights` → `check_training_example` → `_fit_weights`.
- The label substrate: `fact_change._store_delta` → `_project_write_record` → `_store_outcome` → `voice_orch` → `outcome_classifier.classify_outcome` → record `outcome` → `acceptance_history` / `build_training_examples` / `curator_agreement`.
- Both gate operands: `RegistryProvenanceResolver` (Neo4j + member_registry) and `RegistryModelResolver` (`learner_models` via `model_registry.py`), including whether anything registers a model.
- Every reference to `curator_shadow` / `shadow_score_turn` in the repo, and every prompt-building function in `harness/` and `server/`.
- The CS1 scenario's nine checks against the code paths production actually executes.

I checked each prose claim against code: *"value-blind by construction"*, *"the ONLY training entry point"*, *"unreachable by construction"*, *"byte-identical"*, *"shadow cannot act"*, *"drop-and-log ... provably never reaches the fit"*.

Anchors below are `snapshot-file:line`. Live-repo files are named as `~/hip-roadmap/<path>` and are cited only as the upstream/downstream context for a snapshot-anchored finding.

---

## 2. Findings

### F1 — The entire outcome/label substrate the scorer trains on is structurally dead
**Severity: HIGH** (not a disclosure vuln — a correctness/soundness failure that invalidates the learner's stated training signal and the acceptance test's own evidence). **CONFIRMED by reading + live-log evidence.**

**Anchors:** `curator_shadow.py:262-266` (`outcome_event_count`), `:269-280` (`acceptance_history`), `:304-321` (`build_training_examples` label derivation), `:146-147` (`historical_acceptance`). Upstream producer: `~/hip-roadmap/harness/outcome_classifier.py:52-57`; producer of the data it reads: `~/hip-roadmap/harness/fact_change.py:223-224` and `:863-873`.

**What the code actually does.** All three snapshot functions above gate on `outcome.kind == "correction"`. The only producer of that value in the repo is `outcome_classifier.py:80`, reached only when:

```python
superseded_ids = {
    d.get("fact_id") for d in (delta or [])
    if isinstance(d, dict) and d.get("write_state") == "supersede"
    and d.get("fact_id")
}
```

The `delta` it receives is the D-1 projection, built at `fact_change.py:246` from `_D1_DELTA_FIELDS = ("subject", "attribute", "from_state", "to_state", "transition", "prior_fact_id", "new_fact_id")`. The single `_store_delta` call site (`fact_change.py:863-873`) writes exactly `subject / attribute / from_value / to_value / from_state / to_state / transition / prior_fact_id / new_fact_id`. **Neither the raw delta nor the projection ever carries a `write_state` key or a `fact_id` key.** `superseded_ids` is therefore always empty and `classify_outcome` returns `NO_OUTCOME` on every turn except `path == "control_decline"` (an override, which by Stage 0's own limit carries no `target_fact_ids`).

**Consequences, all inside the snapshot:**
- `outcome_event_count` (`:262`) counts only `control_decline` overrides — the 100-event cold-start threshold is effectively unreachable by corrections.
- `acceptance_history` (`:277`) never increments `corrected`, so `historical_acceptance` = `1.0 - 0/n` = **constant 1.0** for every fact ever injected. A declared feature is a constant.
- `build_training_examples` (`:307`, `:321`) produces `corrected_ids = set()` and therefore **`label == 1` for every example, always**. `_fit_weights` (`:353-371`) with `y ≡ 1` has `g = y - p > 0` on every step: weights drift monotonically along the mean feature vector. The "trained" regime would not be an outcome-derived model; it would be a positive projection of the corpus mean.
- `curator_agreement.shadow_outcome_agreement` (`curator_agreement.py:32-36`) collects an empty `corrected` set → `total == 0` → returns `None` on any real record stream.

**Live evidence:** all 12 records in `logs/turns_demo.jsonl` have `outcome.kind == null`; every `delta` is empty; every logged `curator_shadow.features[*].historical_acceptance` is `1.0`.

**Why CS1 does not see it:** `curator_agreement_self_test` (`curator_agreement.py:60-75`) hand-constructs `{"kind": "correction", "target_fact_ids": ["f-bad"]}` records directly. The test asserts the *metric arithmetic* over a record shape the production classifier cannot emit. CS1 never calls `classify_outcome`, `build_training_examples`, or `acceptance_history`.

**Confidence: high** on the code reading and the live log. I did not execute `classify_outcome`, so I cannot rule out a caller elsewhere passing raw (non-projected) deltas — but I grepped: all four production call sites (`voice_orch.py:2740, 3201, 3264, 3473`) route through `take_detection_outcome`, which returns only what `_store_outcome` stored, which is `_delta_proj`.

---

### F2 — The training corpus is read from an unauthenticated file; the gate authenticates the example's *identity* but never its *content* or its *origin*
**Severity: HIGH.** **CONFIRMED by reading.**

**Anchors:** `curator_shadow.py:243-259` (`load_records`), `:309` (`logged = ((r.get("curator_shadow") or {}).get("features")) or {}`), `:314` (`feats = logged.get(fid) or extract_features(...)`), `:317-323` (example assembly), `:340-347` (`train_weights`), and `learner_isolation.py:369-388` (V0/V0b).

**What the code actually does.** `check_training_example` derives `household_id` and `audience` from `fact_id` and from `model_id`. It derives **nothing** about `features` or `label`. V3 (`learner_isolation.py:353`) is a *key-name* scan; V4 (`:360`) is a string equality on a caller-supplied `label_source`. `validate_feature_dict` (`curator_shadow.py:162-180`) is also purely key-name. So the gate's authenticated surface is `{fact_id, model_id}`; everything that actually shapes the fitted weights — the ten feature values and the label — is taken on faith from `logged.get(fid)`.

`logged` comes from `load_records()` → `logs/turns_demo.jsonl`. That file is a plain `open(..., "a")` + `json.dumps` append (`~/hip-roadmap/harness/epistemic_record.py:311-315`), mode `0644`, no signature, no chain, no integrity check. The codebase *has* the right store: `log_epistemic_record` dual-writes the identical record to `harness/epistemic_ledger.py` — hash-chained, `F_FULLFSYNC`'d, AES-256-GCM per-member payload encryption, tamper-evident by design. **The trainer reads the unauthenticated copy.**

**Concrete attack.** An actor with write access to `logs/turns_demo.jsonl` (any local process running as the user; any backup/sync path; any script) appends:

```json
{"turn_id":"x1","member":"maya","admitted":[{"fact_id":"<a REAL household fact_id>"}],
 "curator_shadow":{"features":{"<that fact_id>":{"attribute":"medication",...,"historical_acceptance":-500.0,"recency_rank":0,...}}},
 "outcome":{"kind":null,"target_fact_ids":[],"target_turn_ids":[]}}
```

The `fact_id` is genuine, so `RegistryProvenanceResolver` resolves it to the real household; V1/V2 pass; `validate_feature_dict` passes (all ten keys, correct names); `label_source` is set to `"post_gate_outcome"` by `build_training_examples` itself (`:322`) — the attacker doesn't even have to supply it. The example reaches `_fit_weights` **fully gate-approved**, with attacker-chosen feature values, repeated as many times as they append lines. The gate's "drop-and-log ... provably never reaches the fit" (`:35-44`) is true and irrelevant: nothing was dropped.

**This is the same root-cause shape as the prior seven.** D-25 found the gate validating a *relationship* between values it never authenticated. D-30 authenticated the example side's provenance. D-37 authenticated the target side's scope. Nobody authenticated **the record the example was extracted from**. `fact_id` proves *which household a fact belongs to*; it proves nothing about *whether this turn happened, whether these features were computed by the scorer, or whether this label reflects a real outcome*.

**Confidence: high** on the code path. **Medium** on the practical threat model: this is a single-user prototype on Bill's machine, so "write access to the log" is not currently a meaningful adversary boundary. It becomes one the instant this runs multi-tenant, or the log is synced/restored, or any second process writes it. The finding is that *the design has no answer*, not that it is being exploited today.

---

### F3 — One global weight artifact is applied to every household; the gate controls what goes *in*, nothing controls what it is applied *to*
**Severity: MEDIUM-HIGH.** **CONFIRMED by reading.**

**Anchors:** `curator_shadow.py:376` (`_WEIGHT_CACHE: dict[int, dict[str, float]]`), `:379-402` (`_weights_for`), `:405-425` (`shadow_score_turn`), `:262-266` (`outcome_event_count`), `:269-280` (`acceptance_history`).

**What the code actually does.**
1. `_WEIGHT_CACHE` is a module-global keyed **only** by `n_events // 50` (`:382`). No household, no member, no corpus identity.
2. `_weights_for` hardcodes the training target to `DEFAULT_HOUSEHOLD_ID` (`:387-390`). The gate will therefore drop every non-default-household example — correctly — and then the resulting weights are cached globally.
3. `shadow_score_turn` takes `member` (`:405`) and uses it **only** as `requester=` for the `subject_is_requester` feature (`:424`). It is never used to select weights. Every household in the process is scored by the one artifact trained on the default household's data.

The isolation gate's entire purpose is that household A's signal must not shape a model household B reads. Here A's signal shapes the *only* model, and B is scored by it. The gate is enforced on the ingress edge and absent on the egress edge.

4. `outcome_event_count` (`:262-266`) has no household or member filter. The module docstring names this ("the outcome-event count treats the whole log as one household") — but the consequence is not named: **household B's activity flips household A's regime out of cold start**, which is precisely the condition under which A's byte-identical rule-order guarantee (`:29-33`) stops holding. That is a cross-household control-flow influence on a stated safety property.
5. `acceptance_history` (`:269-280`) also has no household filter, and this limit is **not** named anywhere in the docstring or the L7:CS1 coverage entry. Its output is persisted per-turn into `curator_shadow.features[*].historical_acceptance` (`:441`) and into the encrypted ledger payload.

**On the disclosure question specifically, being precise:** today the *corrected* side is dead (F1), so `historical_acceptance` is `1.0` iff the fact appeared in *someone's* `injected_fact_ids` before, `None` otherwise. Within a household that crosses no boundary the injection contract doesn't already cross — every contributing injection was itself contract-admitted to some reader in that fact's audience. Across households it does cross, unconditionally, because there is no filter at all. And the moment F1 is fixed, `historical_acceptance` becomes a *behavioral* signal (how often other people corrected this fact) persisted into this member's record with no gate anywhere on the scoring path.

**The structural point:** `check_training_example` runs on exactly one path — `train_weights`. The *scoring* path (`shadow_score_turn` → `acceptance_history` → `extract_features` → persisted `features`) aggregates across the whole record stream and passes through **no gate at all**.

**Confidence: high** on the code. This deployment is single-household today, so the cross-household leg is latent, not live.

---

### F4 — In production the training path is dead-closed, and nothing says so
**Severity: MEDIUM.** **CONFIRMED by reading + grep.**

**Anchors:** `curator_shadow.py:384-396`, `learner_isolation.py:381-388` (V0b), `model_registry.py:126-139` (`get_model`, ACTIVE-only), `model_registry.py:88-115` (`register_model`).

`_weights_for` calls `train_weights(..., target={"model_id": MODEL_ID_PREFIX + DEFAULT_HOUSEHOLD_ID, ...})` with **no** `model_resolver`, so `check_training_example` binds `_DEFAULT_MODEL_RESOLVER = RegistryModelResolver()` (`learner_isolation.py:309, 348`). That reads `learner_models` via `get_model`. **`register_model` has zero callers in the entire repository** — I grepped `--type py` across the tree; the only hits are the module's own definition and two prose references in `eval/harnesslib/check_registry.py`. The table is empty. `get_model` returns `None` → `tgt_scope is None` → V0b refuses **every** example → `admitted` is empty → `train_weights` returns `dict(COLD_WEIGHTS)` (`:349`).

So: once `n_events` crosses 100, every refit drops 100% of examples, prints one stderr line **per example** (`:393-395`), caches `COLD_WEIGHTS`, and reports `regime: "cold_start"` alongside `outcome_events: 350`. Fail-closed and directionally correct — but silent about *why*, noisy in the wrong channel, and it means the entire trained regime is unreachable in production. The L7:CS1 twin (vi) uses `_CsResolver`/`_CsModelResolver` fixtures (`layer7_crypto__L7_CS1_check.py.txt:201-220`) and therefore cannot observe this.

**Confidence: high** on the grep; **medium** on the runtime conclusion, since I did not query the SQLite DB (out of scope) and an operator could have registered a row out of band.

---

### F5 — One malformed log line silently and permanently disables the scorer
**Severity: MEDIUM.** **CONFIRMED by reading.**

**Anchors:** `curator_shadow.py:243-259` (`load_records`), `:265` (`r.get(...)`), `:444-447` (blanket `except Exception`).

`load_records` catches `json.JSONDecodeError` per line but appends **any** valid JSON value — including `"x"`, `5`, `[]`, `null`. Every consumer then calls `r.get(...)` unguarded: `outcome_event_count:265`, `acceptance_history:274,276`, `build_training_examples:287,291,309`. A single line containing `"x"` raises `AttributeError` inside `outcome_event_count`, which propagates to `shadow_score_turn`'s blanket `except Exception` (`:444`) → one stderr line → `return None`. **Every subsequent turn**, forever, until that line is removed. The record field is `null`, indistinguishable from "guard path / empty admitted set / disabled" per the epistemic-record docstring (`epistemic_record__curator_shadow_field.py.txt:15-16`). There is no counter, no health signal — unlike `epistemic_record._emit_fail_count`, which this module's own sibling uses for exactly this.

The same shape applies to `outcome` being a non-dict (`(r.get("outcome") or {}).get(...)` handles `None` but not `"x"` or `[]`).

**Confidence: high.**

---

### F6 — No feature-value validation anywhere; `historical_acceptance` is unbounded and can reach NaN/Inf, which produces invalid-JSON records
**Severity: MEDIUM** (latent-HIGH once F1 is fixed). **CONFIRMED by reading; the trigger is latent because of F1.**

**Anchors:** `curator_shadow.py:146-147`, `:162-180` (`validate_feature_dict` — names only), `:183-200` (`_encode`), `:353-371` (`_fit_weights`).

`acceptance = 1.0 - (corrected / injected)` (`:147`). Nothing establishes `corrected ≤ injected`: `injected` counts records where the fact appeared in `injected_fact_ids`; `corrected` counts *correction records naming it*, and one fact can be correction-targeted in many later turns while being injected once. Result: `historical_acceptance` can be arbitrarily negative. `_encode` does a bare `float(acc)` (`:197`) with no clamp; `validate_feature_dict` never inspects a value.

Downstream: `_fit_weights` does `w[d] += lr * g * x[d]` (`:370`) with `lr=0.1`, `epochs=200`, unbounded `x`. `z` is clamped (`:367`) but `w` is not, so a large-magnitude feature drives weights to `inf` and then `nan` (`inf * 0.0`). `weights != COLD_WEIGHTS` is then True, so `regime` reports `"trained"` (`:402`); `_score` returns `nan` for every fact; `rows.sort(key=lambda r: -r[1])` (`:224`) with mixed `nan`/finite keys yields an arbitrary order; `round(nan, 6)` is `nan`; and `json.dumps(record, default=str)` (`epistemic_record.py:314`) emits **bare `NaN`**, which is not valid JSON. Python's `json.loads` accepts it, so the log stays self-consistent — but the hash-chained ledger and any strict external consumer (`eval/oracle/record_invariants.py`) now hold non-conformant records, and `curated_subset_ok: true` is still asserted over a meaningless ranking.

The same unvalidated-value channel accepts a non-`str` `attribute` (`:188` `attr.encode()` → `AttributeError`) and a non-numeric `recency_rank` (`:193` `float()` → `ValueError`), each of which kills the whole fit or the whole turn's shadow via the blanket handlers.

**Confidence: high** on the code; **the negative-acceptance trigger is currently unreachable because of F1** — I am flagging it as a landmine that arms itself the day the correction path is fixed.

---

### F7 — "EXACTLY the declared ten keys" is enforced in one direction only
**Severity: MEDIUM.** **CONFIRMED by reading.**

**Anchors:** `curator_shadow.py:162-180`, `:341`, `:183-200`.

`validate_feature_dict` iterates `for k in features` and rejects unknown keys. It never checks that all ten are *present*. `{}` validates clean. `train_weights` compounds this: `validate_feature_dict(ex.get("features") or {})` (`:341`) coerces a missing/`None`/empty `features` to `{}`, which validates clean, and `check_training_example`'s V3 does the same coercion (`learner_isolation.py:353`). `_encode` then fills every absent key with a neutral default (`0.5`/`0.0`/`""`, `:189-200`). A truncated or empty feature dict trains silently as a fully-neutral example.

CS1 (iii) checks `set(_cs_feats) == set(_CS_KEYS)` (`layer7_crypto__L7_CS1_check.py.txt:125`) — but only on `extract_features`' *own* output, never as a property of `validate_feature_dict`. Since production features arrive via `logged.get(fid)` (`:314`), not via `extract_features`, the one place the ten-key invariant is checked is the one place it cannot be violated.

Related, same file: `_ORDINAL`/`_TRUST_ORDINAL` lookups (`:191, 198`) are case-sensitive with a silent neutral fallback — `"HIGH"` scores identically to an unknown vocabulary item, with no signal. And `hashlib.md5` (`:188`) raises under a FIPS-enabled OpenSSL, which would disable the shadow on every turn via the blanket handler.

**Confidence: high.**

---

### F8 — The "shadow cannot act" static scan covers 2 of ≥7 prompt-building modules, uses two different regexes, and its "hook span" is a defeatable text heuristic
**Severity: MEDIUM.** **CONFIRMED by reading + offset analysis.**

**Anchor:** `layer7_crypto__L7_CS1_check.py.txt:153-190`.

Three independent gaps:

**(a) File coverage.** The scan reads exactly `server/voice_orch.py` and `harness/orchestrator.py` (`:167-168`). Prompt text in this codebase is also built by `harness/escalation_backends.py::build_local_prompt`, `harness/disclosure.py::render_disclosure_prompt`, and there are prompt-assembly surfaces in `server/voice_mem0.py`, `server/voice.py`, `server/voice_https_orch.py`, and `harness/speech.py`. None are scanned. A reference to the scorer in any of them is invisible to CS1.

**(b) The two scans use different regexes, and the weaker one guards the file that actually calls the scorer.** For `voice_orch.py` the pattern is `r"shadow_score_turn|harness\.curator_shadow"` (`:159`). For `orchestrator.py` it is `r"shadow_score_turn|curator_shadow"` (`:177`). The string `from harness import curator_shadow` matches **neither** alternative of the voice_orch pattern; a subsequent `curator_shadow.score_facts(...)` outside the hook span would also match neither. The broader pattern is applied to the file that must contain zero references; the narrower one to the file that legitimately contains three.

**(c) The span is `str.find` on two literals.** `span_a = src.find("REQ_CURATOR_SHADOW_SCORER (Curator Stage 2, D-33)")`, `span_b = src.find("_emit_epistemic_record(identity_verified")` (`:156-157`) — **first** occurrences. I measured the current file: marker at byte 133109 (line 2744), emit at 134113 (line 2762), three scorer refs at 133786/133816/133864 (lines 2754-2755). Tight today. But placing that exact marker string anywhere earlier — a module docstring, a comment — moves `span_a` to the top of the file and makes every reference above line 2762 "inside the hook." Nothing pins the span to a function body, an AST node, or a call graph. The `span_b == -1` direction fails safe (all hits flagged); the `span_a` direction fails **open**.

**What the scan does prove:** that the two named files are textually clean today. That is real and worth having. It is not "shadow cannot act."

**Confidence: high** on (a)/(b)/(c) as code properties.

---

### F9 — The metamorphic query-reword coverage is vacuous in both the scenario and the audit probe
**Severity: MEDIUM.** **CONFIRMED by reading.**

**Anchors:** `layer7_crypto__L7_CS1_check.py.txt:276-285`; `harness_audit__cs1_query_reword_probe.py.txt:26-34`.

In the scenario, `_cs_m1` and `_cs_m2` are two calls to `score_facts` with **byte-identical arguments** (`:276-279`); the assertion `[r[0] for r in _cs_m1] == [r[0] for r in _cs_m2]` can only fail if `score_facts` is nondeterministic. In the probe, the loop variable `_reword` (`:27`) is **never referenced in the loop body** — the two "rewordings" are dead strings; the four `score_facts` calls differ only in `weights`.

Both then lean on `"query" not in extract_features.__code__.co_varnames` — a signature check on one function, which says nothing about `score_facts`, `_encode`, or `shadow_score_turn`.

More importantly, the metamorphic relation is stated with a precondition the tests hold by fiat: *"rewordings that resolve to the same SIO attribute"*. `sio_attribute` **is** query-derived — `voice_orch__sio_attribute_telemetry.py.txt:21` sets `telemetry["sio_attribute"] = (sio or {}).get("attribute")` from the SIO classifier's output on this turn's query, and it feeds `attribute_family_match` (`curator_shadow.py:143-145`), which is a scored dimension. A genuine reword that lands on a different SIO attribute **will** change the ranking. The test asserts invariance under the one condition where invariance is trivial and never exercises the condition where the property is actually at risk.

**Confidence: high.**

---

### F10 — The in-path `curated⊆admitted` assertion compares a list to itself; and `allowed` can carry fact_id-less facts, putting `null` in the shadow ranking
**Severity: LOW-MEDIUM.** **CONFIRMED by reading.**

**Anchors:** `curator_shadow.py:223` (`rows.append((fact.get("fact_id"), ...))`), `:426-428`, `:228-238` (`validate_shadow_output`); upstream `~/hip-roadmap/harness/injection_contract.py:633-637` and `:695-698`.

`ranking` is `[fid for fid, _, _ in rows]` where `rows` enumerates `allowed`; `admitted_ids` is `[f.get("fact_id") for f in allowed]` — the *same* list, same source, same order. `validate_shadow_output` therefore tests a list against itself. The `# unreachable by construction; checked anyway` comment (`:429`) is honest and the check is fine defense-in-depth, but it has **zero discriminating power in-path**: its only real exercise is the fault twin, which hand-builds both arguments (`layer7_crypto__L7_CS1_check.py.txt:91`). Any CS1 evidence that "the scored set never escapes injection.allowed" comes from a hand-constructed call, not from the production path.

Separately: the injection contract appends to `allowed` unconditionally but to `injected_fact_ids` only `if fact_id:` (`injection_contract.py:633-637`, `:695-698` — the author explicitly anticipated missing fact_ids). So `allowed` can contain a fact with no `fact_id`. Then `ranking` contains `None`, `admitted_ids` contains `None`, the subset test passes (`None in {None, ...}`), `scores`/`features` get a JSON key of `"null"`, and `curated_subset_ok` reports `True` — while the rule ranking `injected_fact_ids` is one element shorter. This directly breaks the epistemic-record claim that the two rankings are *"comparable per-turn without a join"* (`epistemic_record__curator_shadow_field.py.txt:12-13`). If two facts in `allowed` ever share a `fact_id`, `scores` and `features` silently collapse to one entry while `ranking` claims two slots, and `build_training_examples` emits two examples with an identical `example_id` (`:318`), double-weighting them in the fit.

**Confidence: high** on the code. **Unverified:** whether a fact_id-less or duplicated fact actually occurs at runtime — I did not exercise retrieval.

---

### F11 — Dead, misleading target operands in the exact shape that produced the 7th hole
**Severity: LOW.** **CONFIRMED by reading.**

**Anchor:** `curator_shadow.py:386-390`.

```python
target = {"model_id": MODEL_ID_PREFIX + DEFAULT_HOUSEHOLD_ID,
          "household_id": DEFAULT_HOUSEHOLD_ID,
          "audience": frozenset(list_circle_members(DEFAULT_HOUSEHOLD_ID))}
```

`check_training_example` reads **only** `target["model_id"]` (`learner_isolation.py:381`); D-37 made `household_id`/`audience` explicitly ignored. So this call site constructs, and imports `list_circle_members` to construct, two caller-asserted fields that are pure decoration. The 7th hole *was* a caller-asserted `target["audience"]`. Leaving one here, live, populated, and adjacent to a `model_id`, is a standing invitation for a future reader or refactor to reintroduce the exact bug. It also means a `list_circle_members` failure raises into `_weights_for`'s handler and silently cold-caches for no reason.

**Confidence: high.**

---

### F12 — The scorer's needs widened the record's projection of *denied* facts
**Severity: LOW.** **CONFIRMED by reading.**

**Anchors:** `~/hip-roadmap/harness/epistemic_record.py:84-100` (`_fact_entry` now emits `sensitivity` and `write_state`, commented "so training-example features are reconstructable from the record alone"), used for `withheld[]` at `:227-229`.

The two additive keys land on **both** `admitted[]` and `withheld[]`. `withheld[]` holds facts the injection contract *denied* — including INJ-3 cross-member denials. Those entries now carry a `sensitivity` label they did not carry before. FLAG-1 keeps `withheld` empty on `access_control` records, so INJ-7 existence-invariance is intact. This is an incremental widening along an axis (`attribute`, `owner`, `subject`, `confidence` were already logged) that was already accepted — but it was made to serve the learner, and no CS1 check touches the `withheld` side of the projection at all.

**Confidence: high** on the code; **low** on materiality.

---

### F13 — "It can't act" is true for reply content and false for latency and durability ordering; a transient failure pins the regime for a 50-event window
**Severity: LOW.** **CONFIRMED by reading.**

**Anchors:** `voice_orch__shadow_hook.py.txt:92-101` (hook), `curator_shadow.py:420` (`load_records()` per turn), `:353-371` (`epochs=200` over the full corpus), `:396-401` (cache-on-failure).

The hook runs **synchronously on the user-visible turn thread**, before `_emit_epistemic_record`. Every scored turn does a whole-file read; above threshold, a refit is a 200-epoch pass over the entire training corpus, on that thread. The ledger's stated write-ahead property is "no reply leaves the system before its governance record is durable" — the scorer sits *between* the reply being produced and that record being written, so it delays both. The module docstring's "The kill switch is implicit (it can't act)" (`:9`) is accurate about reply *text* and inaccurate about turn *timing*.

Also: `_weights_for` caches `COLD_WEIGHTS` into `_WEIGHT_CACHE[cache_key]` on any exception (`:400`). A single transient Neo4j blip pins the cold regime for the whole `n_events // 50` window with no retry and no visible state beyond one stderr line.

**Confidence: high** on the code path; I did not measure any latency.

---

### F14 — Attribute-namespace blindness rests on a producer-side check the scorer never re-asserts
**Severity: LOW.** **PLAUSIBLE — needs verification.**

**Anchors:** `curator_shadow.py:140` (`attribute = fact.get("attribute")`), `:158` (returned verbatim), `:188` (`md5(attr.encode())`); producer-side check at `~/hip-roadmap/harness/extraction_queue.py:229` (`if attribute not in CANONICAL_ATTRIBUTES: return None`).

The "value-blind" claim (`:23-25`) is **correct as stated**: `extract_features` reads only named metadata keys and never iterates the fact dict — I verified there is no `for k in fact` anywhere in the extractor, and CS1 (iv) genuinely tests it (`layer7_crypto__L7_CS1_check.py.txt:133-143`). Where the claim is thinner than it reads: `attribute` is a free string copied verbatim into the persisted feature dict and hashed into `attr_bucket`. Its closed-vocabulary property is enforced only at `_coerce_fact` on the LLM-extraction path. `memory_engine/store.py::encode` does not re-validate `attribute` against `CANONICAL_ATTRIBUTES`, so any non-extraction writer (seed scripts, migrations, direct `encode` callers) can mint a Fact node with an arbitrary attribute string, which the scorer will then carry into the feature space and the training corpus unchecked.

**Confidence: medium.** I confirmed `_coerce_fact` enforces the enum and that `store.py` does not; I did not enumerate every `encode()` caller.

---

## 3. Direct answers to (a)–(d)

### (a) Can any feature leak cross-household or cross-scope signal — including via `sensitivity`, the metadata keys, or the agreement metric?

**Not via `sensitivity`, and not via the metadata keys themselves — that part holds.** `sensitivity` is a fact property (`high`/`medium`/`low`), read by name, ordinal-encoded (`:198`), and it is already logged on the record independently of the scorer. `extract_features` genuinely never iterates the fact dict and never names a value key; `_FORBIDDEN_VALUE_KEYS` (`:87-91`) is belt-and-braces on a surface that is already closed by construction. CS1 (iv) tests the right property with the right fixture. **This one is fine.**

**Yes via `historical_acceptance`, on the household axis.** `acceptance_history` (`:269-280`) pools `injected_fact_ids` and correction targets over the **entire** record stream with no household, member, or scope filter, and its output is persisted per-turn into the record. Within a household, every contributing injection was itself contract-admitted, so it crosses no boundary the injection contract doesn't already cross — I want to be precise rather than alarming about that. Across households it crosses unconditionally, and unlike `outcome_event_count`, **this is not named as a limit anywhere** — not in the module docstring, not in the L7:CS1 coverage entry. Today its information content is degraded to a single bit ("this fact was surfaced before") because of F1; fix F1 and it becomes a behavioral signal about who corrected what. See **F3**.

**Yes via `outcome_events`, as a control-flow leak.** `outcome_event_count` (`:262`) is a global count written into every record and used to select the regime. Household B's activity moves household A's `outcome_events` and can flip A out of cold start — which is exactly the condition under which A's byte-identical guarantee stops holding. See **F3**.

**The agreement metric is clean, and inert.** `shadow_outcome_agreement` (`curator_agreement.py:21-45`) reads only `curator_shadow.ranking` and `outcome.target_fact_ids`, filters `later` by `member`, and computes a pairwise concordance. It is read-only, offline, and has no caller on any live path. Its one real problem is that it returns `None` on any real log (F1), and that its lookahead window (`records[i+1:]` then `[:lookahead]`, `:30-31`) is a **different window** from the trainer's (`records[i+1:i+1+lookahead*3]` then `[:lookahead]`, `curator_shadow.py:302-303`) — so the metric measures agreement with a labeling the trainer did not use.

### (b) Can the `train_weights` path be poisoned, or bypass the gate the way the gate's target side was bypassed?

**Bypass: no, not in the way D-25/D-36 found.** I tried to find the 7th-hole shape again on both operands and it is closed. `check_training_example` derives both sides; caller-supplied `household_id`/`audience` are genuinely ignored on the example *and* the target; `frozenset()` is refused symmetrically at `learner_isolation.py:423` (`if not ex_aud or not tgt_aud`) and again at derivation time in `RegistryModelResolver.resolve` (`:286-287`); `get_model` filters `status = 'active'` (`model_registry.py:135-137`); `is_public` requires a positive marker that does not yet exist in the schema, so the carve-out fails closed. `_fit_weights` is private by underscore only — Python enforces nothing, and CS1 itself imports it (`layer7_crypto__L7_CS1_check.py.txt:24`) — but within the shipped code `train_weights` is in fact the only caller. **The gate's own logic is the strongest thing in this snapshot.**

**Poisoning: yes, comprehensively — and the gate is not designed to stop it.** The gate authenticates *whose* data an example is. It authenticates nothing about *what the example says*. Three channels, in decreasing privilege:

1. **Log write (F2).** Full control of features and labels, using genuine in-household `fact_id`s that pass every check. The tamper-evident ledger holding the same records is not the store the trainer reads.
2. **No privilege — label-window manipulation.** `build_training_examples` filters by member *after* a fixed 30-record slice (`:302`). Any member, or any process emitting records, can push a correction outside another member's window by generating turns, flipping a would-be `label 0` to `label 1`. Cross-member influence on labels with no special access.
3. **No privilege — feature drift.** `historical_acceptance` is driven by how often a fact appears in anyone's `injected_fact_ids`, i.e. by asking about it. Unbounded and unclamped (**F6**).

And in production today the path is dead-closed anyway because no model is registered (**F4**), so none of this is currently reachable — which is fail-closed and correct, but is not what the acceptance test demonstrates.

**On the ordering question you asked specifically:** features are extracted before the gate runs (`:314` then `:341-343`), and `validate_feature_dict` is evaluated first in the `or` chain. This creates no security ordering problem — a dropped example is genuinely absent from the list `_fit_weights` receives (`:345`, `:350`), so "provably never reaches the fit" is true. The real ordering problem is different and upstream: features are *sourced* from an unauthenticated log before anything authenticates the record they came from.

### (c) Is "shadow" actually airtight — any path where the scorer's output could reach the prompt?

**For reply text today: yes, and I could not find a way around it.** I grepped every reference to `curator_shadow` in the repo. The consumers are: `curator_shadow.py` itself, `epistemic_record.py` (writes the field), `layer7_crypto.py` (the test), `curator_agreement.py` (offline metric), and `harness_audit.py` (the probe). **No prompt-building function reads the field.** I checked the one plausible feedback loop — `outcome_classifier.recent_records_for_member` reads the same log per turn — and confirmed it reads only `injected_fact_ids` / `prompt_fact_ids` / `turn_id` (`outcome_classifier.py:62-66`), never `curator_shadow`. The hook is genuinely downstream of the reply (`voice_orch__shadow_hook.py.txt:92-101`), `reply_out` is untouched, and `curator_sio_attribute` is popped unconditionally so `build_epistemic_record` never sees it. **This is real and it is well built.**

**Three qualifications.**

1. **The scan that "proves" it proves much less than claimed** (F8): 2 of ≥7 prompt modules, two different regexes with the weaker one on the file that matters, and a text-position span that fails open. My grep is currently stronger evidence than CS1's check.
2. **There is a closed loop, shadow→shadow.** The scorer's own output (`curator_shadow.features`) is read back as the training features (`:309, :314`). The learner trains on features it produced. That is not a prompt path — it is a self-amplification path, and it is the vector F2 rides.
3. **It is not fully inert.** It runs synchronously on the turn thread with per-turn whole-file I/O and a potential 200-epoch fit (F13). It cannot change *what* is said; it can change *when*, and it sits inside the ledger's write-ahead window.

### (d) Does the cold-start byte-identical claim hold under adversarial input?

**Yes, for output order — and it holds for a good reason.** Under `COLD_WEIGHTS = {"recency": -1.0}`, `_score` reduces to `-1.0 * float(rank)` where `rank` comes from `enumerate(facts)` (`:219`) — **generated by the scorer, never read from the fact**. So the score sequence is `0.0, -1.0, -2.0, ...`, strictly decreasing and independent of every attacker-controlled input. The sort is stable and the ranking equals the input order for *any* fact content. The live log confirms it (scores `0.0, -1.0, ..., -5.0`; `ranking == injected_fact_ids`). **No adversarial fact content can permute the cold-start order.** This is the cleanest property in the snapshot.

**Three qualifications.**

1. **It can degrade to no output.** A non-`str` `attribute` reaches `attr.encode()` (`:188`) and the blanket handler (`:444`) returns `None`. Fail-safe, not fail-wrong — but "byte-identical" becomes "absent."
2. **The rankings can differ in length.** A fact_id-less fact in `allowed` puts `null` in the shadow ranking and not in the rule ranking (**F10**), so byte-identity holds against `allowed` but not against `injected_fact_ids`.
3. **Cold start is not attacker-stable.** The *regime* is selected by a globally-pooled, unfiltered event count (**F3**), so whether you get the guarantee at all is influenced by activity outside the scored household.

**Prompt byte-identity under `HIP_CURATOR_SHADOW=0` holds** — the hook cannot reach `reply_out`. But note the toggle is read per-turn from the environment at `:415`, inside the try block, so a scorer that has already crashed reports the same `None` as a disabled one.

---

## 4. Attack classes the CS1 acceptance test does NOT cover

The gate's coverage entry had no input-trust axis and seven holes went through. CS1's coverage entry has the same gap, plus two more: no **artifact-application** axis and no **production-binding** axis. Systematically:

**A1 — Corpus authenticity (the input-trust axis, again).**
*Why the test can't see it:* CS1 calls `_cs_turn(..., records=[])` (`:75`), passing the corpus in explicitly. `load_records` is never called. `build_training_examples` is never called. Every training example in the test is hand-built from `extract_features` (`:221-226`). The single path production actually uses to obtain features — `logged.get(fid)` from a plaintext file — is untested end to end.
*A covering test would:* point `_RECORDS_PATH` at a fixture log, call `build_training_examples` → `train_weights` on it, and assert that (i) a record whose `curator_shadow.features` were not produced by the scorer is rejected or provably cannot affect the fit, and (ii) the trainer's corpus is the ledger, or is cross-checked against it.

**A2 — Feature *value* domain (as opposed to key names).**
*Why the test can't see it:* every existing check — `validate_feature_dict`, `_find_gate_decision_key`, CS1 (iii) — is a name check. CS1 (iii) supplies three *bad key names* and asserts refusal; it never supplies a bad *value*.
*A covering test would:* assert a per-key domain (`attribute ∈ CANONICAL_ATTRIBUTES`; `historical_acceptance ∈ [0,1] ∪ {None}`; `recency_rank` a non-negative int `< len(allowed)`; `confidence`/`sensitivity` in vocabulary; `trust_rung ∈ _TRUST_ORDINAL`), and drive `None`/`NaN`/`inf`/`1e308`/non-`str`/wrong-type values through `train_weights` and `score_facts`, asserting refusal — not the current blanket-except silence.

**A3 — Production resolver binding.**
*Why the test can't see it:* twin (vi) injects `_CsResolver` and `_CsModelResolver` (`:201-217`). It exercises gate *logic*, which is correct, and asserts nothing about `RegistryProvenanceResolver` (Neo4j) or `RegistryModelResolver` (`learner_models`). Because `register_model` has no callers, the real path refuses 100% of examples — invisible here.
*A covering test would:* assert `get_model(MODEL_ID_PREFIX + DEFAULT_HOUSEHOLD_ID)` resolves to an active row, or assert explicitly that the trained regime is currently unreachable and record that as the acceptance state rather than demonstrating a regime that cannot run.

**A4 — What the fitted artifact is *applied* to (the missing egress axis).**
*Why the test can't see it:* every twin is about what enters the fit. Nothing in CS1 examines `_WEIGHT_CACHE`, its key, or which household's turns are scored by a given weight vector. Twin (vii) scores `_cs_facts` with `_cs_w_clean` and checks only that the output is a permutation.
*A covering test would:* score two households' turns in one process and assert either that they receive different weight artifacts or that `_WEIGHT_CACHE` is keyed by household — i.e. mirror the ingress isolation property on the egress edge.

**A5 — Cross-household aggregation on the *scoring* path.**
*Why the test can't see it:* `records=[]` means `acceptance_history` and `outcome_event_count` are called on an empty list. Both functions' cross-household behavior is untouched, and `acceptance_history`'s lack of a household filter is not even named as a limit.
*A covering test would:* build a two-household record fixture and assert household A's `outcome_events` and every `historical_acceptance` in A's turns are bit-identical with and without household B's records present.

**A6 — Log robustness / silent-disable.**
*Why the test can't see it:* the scorer is never given a real or malformed log.
*A covering test would:* feed logs containing a non-object JSON line, `outcome` as a string, `curator_shadow.features` as a list, and a `null` fact_id in `admitted` — asserting the scorer degrades **visibly** (a counter, like `epistemic_record._emit_fail_count`) rather than returning `None` indistinguishably from "not scored."

**A7 — Prompt-reachability beyond two files.**
*Why the test can't see it:* F8(a)/(b)/(c).
*A covering test would:* AST- or import-graph-scan **all** of `harness/` and `server/` for any reference to the module or any of its public names (not a regex over two files with two different patterns), pinned to function boundaries rather than `str.find` offsets — plus, ideally, a runtime tripwire that raises if `shadow_score_turn` is entered with a prompt-assembly frame on the stack.

**A8 — Real metamorphic query-invariance.**
*Why the test can't see it:* both the scenario check and the audit probe compare identical calls; the probe's reword strings are an unused loop variable (F9).
*A covering test would:* drive two genuinely different phrasings through the real SIO classifier and assert either identical rankings **or** an explicitly named, bounded dependence on `sio_attribute` — since `sio_attribute` is query-derived, the honest property is conditional and the test should say so and check the condition.

**A9 — Label-window integrity and trainer/metric agreement.**
*Why the test can't see it:* CS1 never calls `build_training_examples`, so its 30-record pre-filter window is never exercised, and the divergence from the agreement metric's unbounded window is never compared.
*A covering test would:* place a correction beyond 30 intervening records and assert the trainer's label and the metric's `corrected` set agree — i.e. that one member's turn volume cannot silently flip another member's labels.

**A10 — The outcome producer end to end (this is how F1 survived).**
*Why the test can't see it:* the agreement self-test hand-authors `{"kind": "correction", "target_fact_ids": [...]}`. CS1 asserts the *metric's arithmetic* over a shape `classify_outcome` cannot emit.
*A covering test would:* drive a real supersede write through `fact_change` → `classify_outcome` → the record, and assert a `correction` outcome with a non-empty `target_fact_ids` actually appears — the one assertion that would have caught the `write_state`/`fact_id` field mismatch immediately.

**Cross-cutting observation.** CS1's construction has a recurring pattern: it hand-builds the object under test, then tests it. Ranking vs. admitted set (both hand-passed), features (from `extract_features`, never from the log), the corpus (`records=[]`), the resolvers (fixtures), the outcome records (hand-authored), the rewordings (unused). Nine checks, and the number that exercise a value produced by the production pipeline is close to zero. That is precisely the structure that let seven holes through the gate — not a lack of tests, a lack of tests **on inputs the system did not manufacture itself**.

---

## 5. What I could not determine

- **Runtime behavior.** I executed nothing from the target modules. Every dynamic claim (NaN propagation, sort behavior under NaN keys, `AttributeError` propagation through the blanket handlers, `json.dumps` emitting bare `NaN`) is derived from reading plus Python semantics, not observed. All are marked CONFIRMED-by-reading, not CONFIRMED-by-execution.
- **`learner_models` table contents.** I confirmed `register_model` has no callers in the repo. I did not query the SQLite DB, so an out-of-band operator registration would change F4's conclusion.
- **Whether `allowed` ever actually contains a fact_id-less or duplicated fact.** The contract's `if fact_id:` guard shows the author expected it; I could not exercise retrieval to confirm it occurs.
- **Latency of a real refit (F13).** Unmeasured — no household is near the 100-event threshold, and I did not benchmark.
- **Exhaustive prompt-reachability.** I grepped for the module name and enumerated prompt-building functions. A dynamic reference (`importlib` with a constructed name, a registry/dispatch table, a plugin path) would evade both my grep and CS1's scan. I found no evidence of one; I cannot prove absence.
- **Complete `encode()` caller audit (F14).** I confirmed `_coerce_fact` enforces `CANONICAL_ATTRIBUTES` and `store.py` does not re-check; I did not enumerate every writer.
- **Snapshot completeness.** I reviewed the ten provided files plus live-repo context. I cannot rule out a consumer of `curator_shadow` outside the tree I searched.
- **Whether F1 is a known, accepted Stage-0 limit.** The docstrings name several honest gaps ("overrides carry no target_fact_ids"; "pre-build records lack sensitivity/write_state") but I found **no** written acknowledgement that corrections are unreachable, and the code, the coverage entry, and the self-test all read as if the correction path works. I am reporting it as an undocumented defect; if it is a known accepted limit recorded somewhere I did not read, that changes its framing but not its effect on the training signal.


---

# REVIEW 2 of 2 — Reviewer B (verbatim)

# Reviewer B — Adversarial Review: Curator Stage 2 Shadow Scorer

**Target:** frozen snapshot of `~/hip-roadmap` @ `ae74e48` (branch `roadmap`), at
`/private/tmp/claude-501/-Users-bill-ai/517c9464-b7c5-4c16-a31a-5faa79ed81c7/scratchpad/d40_snapshot/`

---

## 1. What I reviewed and how

I verified the pin: `git rev-parse HEAD` in the live repo returns `ae74e481654fe9796ef42b301e7467323fa1fbb7`, matching `PINNED_COMMIT.txt`. This pass was **strictly read-only** — Read, `rg`, `sed`, `ls`, and read-only `git log`/`rev-parse`. I ran no tests, no harness, no server, no Python, and touched no database. I made no edits. I offer **no status ruling** on any requirement; these are findings only.

I traced, in the snapshot: `extract_features` → `_encode` → `_score` → `score_facts` → `shadow_score_turn` (the scoring path); `load_records` → `build_training_examples` → `train_weights` → `check_training_example` → `_fit_weights` (the training path); `_weights_for` / `_WEIGHT_CACHE` (the regime path); and every `except Exception` and `print(..., file=sys.stderr)`.

I read the live repo read-only for the things the snapshot asserts but does not contain: who actually reads the `curator_shadow` record field; whether `curator-shadow-<household>` is registered anywhere; what `_fact_entry` puts in the record `admitted` entries; the real sensitivity/confidence/trust vocabularies; how `outcome.target_fact_ids` is produced; the retrieval `ORDER BY`; and every emit path.

Line numbers below are **snapshot line numbers**. For the two files where I confirmed the live offset: `layer7_crypto__L7_CS1_check.py.txt` line *N* ↔ `eval/harnesslib/layer7_crypto.py` line *N+1984*; `voice_orch__shadow_hook.py.txt` line *N* ↔ `server/voice_orch.py` line *N+2659*.

**Disclosure:** one `rg` sweep for `HIP_CURATOR_SHADOW` incidentally printed a single line from `docs/reviews/FABLE_CuratorReview__test-model-and-gate-code-review__v20260730_0801.md`. I did not open that file and did not read further. My Finding 6 (static-scan blindness) was reached from reading the CS1 scan code before that grep ran; I flag the overlap so it is not mistaken for independent corroboration.

**Severity calibration.** Nothing in this module reaches the prompt (see (c) — that one genuinely holds). I therefore cap severity at HIGH. "HIGH" here means: an attacker-reachable defect that materially breaks a claim the REQ rests on, or that silently disarms a guarantee, in a component that is one operator action away from being live. It does not mean live disclosure.

---

## 2. Findings

### Finding 1 — The training path authenticates the `fact_id` and trusts the feature vector and label sitting next to it in an unauthenticated file
**Severity: HIGH** — this is the exact D-25 shape (validate the *relationship*, never authenticate the *origin*), reproduced one layer up: the gate authenticates one field of the example and the producer hands it three more that nothing authenticates.
**Anchor:** `curator_shadow.py:309`, `:314`, `:321-322`; `learner_isolation.py:360-364`; `curator_shadow.py:243-259`.
**Confidence: CONFIRMED by reading.**

`build_training_examples` sources each example's features from the record stream:

```python
logged = ((r.get("curator_shadow") or {}).get("features")) or {}    # :309
feats = logged.get(fid) or extract_features(entry, ...)             # :314
"label": 0 if fid in corrected_ids else 1,                          # :321
"label_source": POST_GATE_LABEL,                                    # :322
```

`records` comes from `load_records` (`:243-259`), a plain `open()` of `logs/turns_demo.jsonl` with **no signature, no HMAC, no ownership check, no line count, no schema check** — malformed lines are silently skipped (`:255-256`) and an unreadable file returns `[]` (`:257-258`). I confirmed against the live repo that `harness/epistemic_record.py:314` writes this log with `json.dumps(record, default=str)` and nothing integrity-protects it.

The gate then resolves only `example["fact_id"]` (`learner_isolation.py:369-375`). It never asks whether the `features` dict and the `label` beside that fact_id were produced by the system that minted the fact_id. So:

**Attack.** Append lines to `logs/turns_demo.jsonl` containing (a) a real household `fact_id` read out of the same file, (b) `curator_shadow.features.<fid>` set to any values you like within the declared ten key names, and (c) `outcome: {"kind":"correction","target_fact_ids":[<fact to demote>]}`. Every such example passes `validate_feature_dict` (names only — see Finding 2), passes gate V0 (the fact_id is genuine and in-household), passes V1/V2 (same household, same roster), and reaches `_fit_weights` with attacker-chosen feature values and an attacker-chosen label.

**V4 is vacuous against this producer.** The gate's label-provenance check (`learner_isolation.py:360-364`) compares `label_source` to a constant. `build_training_examples` **stamps that exact constant unconditionally** at `:322`, on every example, regardless of where the record came from. The check can never fail for the only producer that exists. The *label value* — the thing that actually steers the fit — is read from `outcome.target_fact_ids` in the log and is never checked at all.

I want to be precise about the trust boundary: writing to `logs/turns_demo.jsonl` requires local filesystem access, not a remote request. This is not a network-reachable exploit. But the file is `-rw-r--r--` in a working tree, is truncated routinely by `scripts/demo_reset.py` (confirmed: `demo_reset.py:37` lists it), and is the *sole* input to both the training set and the cold-start counter. The system treats a mutable local file as authenticated provenance, which is the property the gate was built to eliminate.

---

### Finding 2 — The feature allowlist is recursive for gate-decision keys and top-level-only for value keys and undeclared keys
**Severity: HIGH** — the module's central claim ("EXACTLY these ten keys", "value-derived key refused") is enforced one level deep, while the check immediately above it on the same object is recursive. CS1's twin tests only the level that works.
**Anchor:** `curator_shadow.py:162-180`.
**Confidence: CONFIRMED by reading.**

```python
bad = _find_gate_decision_key(features)      # :169  RECURSIVE (learner_isolation.py:312-327)
if bad: return ...
for k in features:                           # :173  TOP-LEVEL ONLY
    if str(k) in _FORBIDDEN_VALUE_KEYS: ...  # :174
    if str(k) not in DECLARED_FEATURE_KEYS: ...  # :177
```

`_find_gate_decision_key` walks nested dicts and lists. The two loops beneath it iterate `features` exactly once, at depth 0.

**Attack.** `{"attribute": {"value_text": "SECRET-A", "query_embedding": [0.1]}}` returns `None` from `validate_feature_dict` — clean. `"value_text"` is not in `GATE_DECISION_FEATURE_KEYS` so the recursive check ignores it; `"attribute"` is declared so the top-level loop ignores it; the nested keys are never visited by anything.

**What actually happens in-path today, stated honestly:** the smuggled payload does *not* get learned. `_encode` (`:183-200`) will hit `attr.encode()` on a dict (`:188`) or `_ORDINAL.get({...})` on an unhashable (`:191`, `:198`) and raise, which `_weights_for`'s handler converts to cold weights (Finding 4). So today this manifests as a **durable denial-of-learning primitive**, not a leak. It becomes a leak the moment any consumer iterates `features` rather than `_encode`-ing it — and one such consumer already exists: the record itself logs `curator_shadow.features` verbatim (`curator_shadow.py:441`), and `harness/epistemic_record.py:314` dual-writes the record into the canonical ledger.

CS1's twin (iii) at `layer7_crypto__L7_CS1_check.py.txt:108-113` tests three **top-level** keys only. It cannot see this.

---

### Finding 3 — `_WEIGHT_CACHE` is keyed on a counter, not on the data; weights outlive the log that produced them, and the record carries no weight identity
**Severity: HIGH** — a fitted artifact is served against data it was not fit on, and nothing logged makes that detectable or the shadow output reproducible.
**Anchor:** `curator_shadow.py:376`, `:382`, `:396`, `:400-402`, `:440-443`.
**Confidence: CONFIRMED by reading** (the cache mechanics). **PLAUSIBLE** on the exact operational sequence, which depends on process lifetime I could not observe.

```python
_WEIGHT_CACHE: dict[int, dict[str, float]] = {}   # :376  module-level, process-lifetime
cache_key = n_events // 50                        # :382  the ONLY key
```

The key is a bucket of the outcome-event count. It is **not** a function of household, of the record set, of the log's length, or of any content hash. There is no TTL and no invalidation path — nothing in the module or the repo clears `_WEIGHT_CACHE`.

Three consequences:

1. **Stale weights across a log reset.** `scripts/demo_reset.py` truncates `logs/turns_demo.jsonl` (confirmed, `demo_reset.py:37`; `eval/harnesslib/fixture.py:77` documents this as per-scenario behavior). In any long-running server process, a fit performed at bucket *k* against record set A survives the truncation and is served for every turn while the *refilled* log's `n_events` sits back in bucket *k* — a completely different record set. The record then reports `outcome_events: N` describing log B and a `ranking` produced by weights fit on log A, with nothing indicating the mismatch.

2. **Cross-household serving, if the deployment ever grows.** The docstring names the single-household limit for the *count* (`:50-52`) but does not name it for the *cache key*. Because the key is only the count, household A's fit is served for household B's turn whenever both sit in the same bucket. `shadow_score_turn(records=...)` (`:407`, `:420`) lets a caller supply an arbitrary record set whose fit is then cached under a key derived solely from that set's event count — so the first caller to reach a bucket pins the weights for every subsequent turn in the process, whatever data they used.

3. **The output is not reproducible from the record.** The logged dict (`:435-443`) contains `regime`, `outcome_events`, `ranking`, `scores`, `features` — and **no weights, no weight hash, no fit identity, no record-set identity.** For a component whose stated purpose is offline eval of the shadow ranking against outcomes, you cannot, from the record, determine which weight vector produced a given `ranking`. `curator_agreement.shadow_outcome_agreement` therefore pools rankings from arbitrarily many different weight vectors into one agreement number with no way to partition them.

CS1 never touches this code. Its cold-start check passes `records=[]` (`layer7_crypto__L7_CS1_check.py.txt:75`), so `n_events == 0` and `_weights_for` returns at `:381` before the cache branch. `_WEIGHT_CACHE`, `cache_key`, `load_records`, and `build_training_examples` have **zero coverage** in CS1.

---

### Finding 4 — `regime` conflates "gate refused everything" with "not enough data", and in this repo the trained regime is unreachable while reporting itself as cold start
**Severity: HIGH** — the one field that tells an auditor which regime ran cannot distinguish the safe state from total gate failure, and the system is currently in the indistinguishable state.
**Anchor:** `curator_shadow.py:348-349`, `:387`, `:393-395`, `:397-402`.
**Confidence: CONFIRMED by reading** for the code path; **CONFIRMED by grep** for the registry state.

```python
if not admitted:
    return dict(COLD_WEIGHTS), violations                       # :348-349
...
weights = _WEIGHT_CACHE[cache_key]
return ("trained" if weights != COLD_WEIGHTS else "cold_start"), weights   # :401-402
```

`regime` is derived by comparing the weight dict to `COLD_WEIGHTS`. Four *distinct* states collapse to the string `"cold_start"`: (a) genuinely below threshold; (b) every example dropped by the gate; (c) the fit raised and the handler at `:397-400` substituted cold weights; (d) `build_training_examples` produced nothing. Only (a) is benign. States (b)–(d) are reported to the epistemic record as if the system simply had not learned yet — while `outcome_events` in the same dict reads 5,000.

**And the system is in state (b) right now.** `_weights_for:387` computes the target as `MODEL_ID_PREFIX + DEFAULT_HOUSEHOLD_ID` = `"curator-shadow-default"`. `RegistryModelResolver.resolve` (`learner_isolation.py:260-266`) calls `model_registry.get_model`, which returns the ACTIVE `learner_models` row or `None`. I grepped the entire repository: **`register_model` has zero callers** — the only occurrence outside `docs/` is its own definition at `harness/model_registry.py:88`. Nothing registers `curator-shadow-default`. CS1's fixture registers `"curator-shadow-hh-alpha"` in an in-memory dict (`layer7_crypto__L7_CS1_check.py.txt:213`), which is not the model_id production computes.

So in production every example is refused at gate V0b ("unresolvable training target", `learner_isolation.py:384-388`), `admitted` is empty, `train_weights` returns `COLD_WEIGHTS`, and the trained regime is structurally unreachable — **silently**. This is a *fail-closed-to-safe* outcome, which is the right direction. My finding is not that it fails; it is that it fails **indistinguishably from success-at-low-volume**, so no reader of the record and no run of CS1 can tell.

Secondary: `:393-395` prints one stderr line **per dropped example**, inside the fit branch. With the model unregistered and a log at threshold volume, every cache-miss fit emits one line per admitted fact per turn across the whole log — a stderr flood, and the mechanism that makes the flood *look* like normal drop-and-log rather than total refusal.

---

### Finding 5 — `train_weights` is not the only training entry point in any enforceable sense, and the gate's exclusion is asserted by the fixture rather than enforced
**Severity: MEDIUM** — the docstring's "ONLY training entry point" (`:331`) and "provably never reaches the fit" (`:335-337`) are true only for callers that choose to call it.
**Anchor:** `curator_shadow.py:327-350`, `:353-359`; `layer7_crypto__L7_CS1_check.py.txt:24`, `:227`, `:235`.
**Confidence: CONFIRMED by reading.**

`_fit_weights` is module-private by a leading underscore, which Python does not enforce and which CS1 itself imports across the module boundary at `:24` (`_fit_weights as _cs_fit_raw, # bypass on purpose`) and calls at `:235`. The no-bypass property is a naming convention plus one test that deliberately violates it. That is honest — the docstring says so — but "provably never reaches the fit" overstates what the underscore buys: it is provable for the batch handed to `train_weights`, not for the process.

More materially, **CS1's own bypass fixture depends on Finding 1's decoupling**:

```python
_cs_bad = dict(_cs_exs[0], example_id="cs-t:cs-x", fact_id="cs-x", label=0)   # :227
```

The "cross-household" example is `cs-f1`'s **features** wearing `cs-x`'s **fact_id**. The gate accepts that construction without objection because it never checks that features correspond to their fact_id. So the test that proves the gate materially changes the fit is built on the very property that lets Finding 1's poisoning through. A test cannot be evidence for a property its own fixture violates.

Minor, same anchor: `train_weights:341-343` short-circuits — if `validate_feature_dict` returns a violation, `check_training_example` is never invoked. No security consequence (the example is dropped either way), but it means the isolation gate does not see feature-invalid examples at all, so the gate's own V3 telemetry undercounts.

Also at `:362`, `_fit_weights` uses `ex["features"]` (subscript) while `train_weights:341` and the gate both use `.get(...) or {}`. An example dict with no `features` key survives both checks and raises `KeyError` in the fit — a one-line crash reachable through the public API.

---

### Finding 6 — The "shadow cannot act" proof is a two-file regex scan over a comment-delimited span
**Severity: MEDIUM** — the property currently **holds** (I verified it independently); the *proof* of it does not generalize and would not survive the change it exists to catch.
**Anchor:** `layer7_crypto__L7_CS1_check.py.txt:153-190`.
**Confidence: CONFIRMED by reading** (scan construction). **CONFIRMED by grep** (the property holds today).

The scan reads exactly two files — `server/voice_orch.py` and `harness/orchestrator.py` — and matches `shadow_score_turn|harness\.curator_shadow` in the first, `shadow_score_turn|curator_shadow` in the second (two different regexes for the same property). Four independent gaps:

1. **File list.** I grepped every `emit_epistemic_record`/`log_epistemic_record` caller in the live repo: `harness/realtime_adapter.py`, `server/demo_dashboard.py`, `scripts/realtime_voice_demo.py`, `scripts/text_demo.py`, `scripts/check_bytecompat_d1.py` — **none of these are scanned.** Any of them, or any new retrieval/ranking module, could import the scorer invisibly.
2. **Symbol list.** The regex looks for `shadow_score_turn` and the module path. It does **not** look for `score_facts`, `extract_features`, `_score`, or `_weights_for` — all public-enough, all importable, and `score_facts` alone is sufficient to reorder a fact list before prompt assembly.
3. **Import form.** `from harness import curator_shadow as cs` followed by `cs.score_facts(...)` matches neither alternative in either regex.
4. **The span is a comment.** `span_a = src.find("REQ_CURATOR_SHADOW_SCORER (Curator Stage 2, D-33)")` and `span_b = src.find("_emit_epistemic_record(identity_verified")`. Moving that marker comment earlier in `voice_orch.py` widens the "allowed" span arbitrarily. A structural proof whose boundary is a movable string is not structural.

**The property itself holds today**, and I say so plainly: `rg` over the live repo shows the only non-eval, non-doc importer of `harness.curator_shadow` is `server/voice_orch.py:2754`, inside the emit hook, and the only readers of the record's `curator_shadow` field are `eval/harnesslib/curator_agreement.py` (offline) and `build_training_examples`. There is no path to retrieval or prompt.

---

### Finding 7 — `sensitivity == "critical"` encodes to the neutral midpoint, ranking *below* `"high"`
**Severity: MEDIUM** — the D-33 feature added specifically to carry sensitivity is wrong for the most sensitive class in the vocabulary, and wrong in the permissive direction.
**Anchor:** `curator_shadow.py:95`, `:198`.
**Confidence: CONFIRMED by reading** both sides.

```python
_ORDINAL = {"high": 1.0, "medium": 0.5, "low": 0.0}      # :95
"sensitivity": _ORDINAL.get(features.get("sensitivity"), 0.5),   # :198
```

The live vocabulary is four-valued: `harness/extraction_queue.py:95` declares `SENSITIVITY_LEVELS = ("low", "medium", "high", "critical")` and validates against it at `:261`; `harness/permissions.py:55` defines `_HIGH_SENSITIVITY = frozenset(("high", "critical"))` and `:22` documents the four values. So `"critical"` → `.get` miss → **0.5**, the same encoding as *unknown*, and strictly less than `"high"` → 1.0. The single most protected class in the system is encoded as mid-sensitivity.

Two aggravators. First, `_ORDINAL` is shared between `sensitivity` (`:198`) and `confidence` (`:191`) purely because their vocabularies happened to coincide today — `memory_engine/consolidate.py:55` and `harness/extraction_queue.py:94` confirm confidence is three-valued — so either vocabulary extending silently corrupts the other feature. Second, `.get(..., 0.5)` means an unknown value is indistinguishable from a genuine `"medium"`; there is no "unknown" channel and no logging of the miss.

CS1's fixture uses only `high`/`medium`/`low` (`layer7_crypto__L7_CS1_check.py.txt:44-60`), so it cannot reach this. (Corroboration that this is a repo-wide shape rather than a one-off: `harness/hipconfig.py:30` has the same three-key `SENSITIVITY_RANK` with a `.get(tag, 0)` default, which sorts `"critical"` *below* `"low"`. That file is outside my target; I note it only because it shows the pattern.)

---

### Finding 8 — `historical_acceptance` is unbounded below and escapes its documented `[0,1]` domain; a member can drive it arbitrarily negative
**Severity: MEDIUM** — an in-band, no-file-access primitive for arbitrarily dominating a trained score.
**Anchor:** `curator_shadow.py:146-147`, `:197`; `curator_shadow.py:269-280`.
**Confidence: CONFIRMED by reading** the arithmetic; **PLAUSIBLE** on the exact number of corrections achievable per lookback window, which depends on runtime behavior I did not execute.

```python
injected, corrected = (history or {}).get(fact.get("fact_id"), (0, 0))
acceptance = None if injected == 0 else 1.0 - (corrected / injected)   # :147
...
"historical_acceptance": 0.5 if acc is None else float(acc),           # :197  no clamp
```

`acceptance_history` (`:269-280`) counts injections from `injected_fact_ids` and corrections from `outcome.target_fact_ids` **independently**; nothing bounds `corrected ≤ injected`. From the live `harness/outcome_classifier.py:51-83`, a `correction` fires whenever this turn's `delta` supersedes a fact_id that appeared in *any* of the member's last 20 records. One injection at turn T can therefore be matched by many corrections across T+1…T+20, each producing another `target_fact_ids` entry for the same fact. With `injected=1, corrected=K`, `acceptance = 1-K`, unclamped.

Under `COLD_WEIGHTS` this dimension carries weight 0, so it is inert today. Under any trained weight vector, a single feature at −19 while every other feature is in [0,1] dominates the linear score outright, deterministically forcing that fact to one end of the ranking. It is a ranking-control primitive that requires only ordinary in-band member behavior — no file access, no forged input.

Related, and I want to be equally clear where the concern *does not* hold: `acceptance_history` is computed over the whole log with **no member filter**, so member A's correction behavior changes the `historical_acceptance` value member B's turn sees. I traced whether that is a scope crossing and concluded **it is not**: the lookup is keyed by fact_id and only fact_ids already in this turn's `injection_result.allowed` are consulted, and INJ-3 prevents another member's personal facts from ever entering that set. The only facts whose history can cross members are household-owned facts, whose audience is the whole circle. Under the D-23 ruling this is in-scope signal, not a crossing.

---

### Finding 9 — Infinity and NaN can enter the fit and the record; the subset assertion cannot detect a destroyed ranking
**Severity: MEDIUM** — an integrity defect in the ledger and a blind spot in the only in-path assertion.
**Anchor:** `curator_shadow.py:197`, `:224`, `:353-371`, `:440`.
**Confidence: CONFIRMED by reading** for the arithmetic and the assertion's blindness; **PLAUSIBLE** for the exact NaN-sort permutation, which I did not execute.

`float(acc)` at `:197` accepts any value the log carries. `float("1e400")` is `inf`. `_fit_weights` initializes `w` to zeros (`:361`) and computes `z = sum(w[d] * x.get(d, 0.0) ...)` (`:366`) — with `w[d] == 0.0` and `x[d] == inf`, IEEE gives `0.0 * inf = nan` on the very first row. The `max(-30, min(30, z))` clamp at `:367` guards `math.exp` but not `w`: `min(30.0, nan)` returns `30.0` (the NaN comparison is False, so the incumbent is kept), so no exception is raised and the loop proceeds, propagating `±inf` into `w` at `:370`.

Downstream: `_score` (`:207`) then produces `inf` or, if weights of both signs are present, `nan`. Two consequences:

- **`round(nan, 6)` / `round(inf, 6)` land in the record** at `:440`, and `harness/epistemic_record.py:314` serializes with plain `json.dumps`, which emits bare `NaN`/`Infinity` tokens — **not valid JSON per RFC 8259**. The record is dual-written verbatim into the canonical ledger, so any strict-JSON consumer of the ledger breaks on that line.
- **`validate_shadow_output` cannot see it.** `rows.sort(key=lambda r: -r[1])` (`:224`) with NaN keys yields an arbitrary permutation (all NaN comparisons are False, so Timsort's decisions are meaningless). But the result is still a permutation of the input, so `outside` at `:233` is empty and `curated_subset_ok` is reported `True`. **The subset assertion is satisfied by every possible ordering of the admitted set** — including a completely destroyed one. It constrains membership, never order, and order is the entire output.

Same anchor, separate mechanism: `score_facts:223` uses `fact.get("fact_id")`, which can be `None`. I confirmed in `harness/injection_contract.py:633,695` that `result.allowed.append(fact)` is unconditional while `injected_fact_ids.append` is guarded by `if fact_id:` — so `allowed` can hold facts with a missing or empty fact_id. Two such facts produce two `None` entries in `ranking` but **one** entry in the `scores` and `features` dicts (`:440-441`), because dict keys collapse. The record then silently under-reports, and nothing asserts `len(ranking) == len(scores)`. `validate_shadow_output` passes, because `None in set([None, ...])` is True.

---

### Finding 10 — The gate's violation strings print live roster membership to stderr
**Severity: LOW–MEDIUM** — modest today (single household, member ids not secrets), but it is the isolation gate's diagnostics emitting exactly the data the gate protects, into an unpartitioned sink.
**Anchor:** `curator_shadow.py:393-395`, `:398`, `:430`, `:445-446`; `learner_isolation.py:423-436`.
**Confidence: CONFIRMED by reading.**

`_weights_for:393-395` prints every gate violation string verbatim to stderr, one line per dropped example. Those strings embed:

- `learner_isolation.py:430-436` — `sorted(ex_aud)`, `sorted(tgt_aud)`, and `sorted(unauthorized)`: **the full live membership of both the source scope's roster and the target model's roster**, plus the specific member ids that constitute the crossing.
- `:423-429` — `{ex_aud!r}` and `{tgt_aud!r}`: both frozensets of member ids.
- `:407-409` — both household ids.
- `:372-375` — the raw `fact_id`.
- `ex_id`, which `build_training_examples:318` constructs as `f"{turn_id}:{fid}"` — turn id and fact id.

Server stderr is typically a shared, non-household-partitioned sink with weaker access control than the encrypted store. There is no redaction, no truncation, and no rate limit — and per Finding 4 the current unregistered-model state makes this fire once per example on every fit attempt.

Lower-confidence amplifier at `:398` and `:445-446`: `{exc!r}` is printed unredacted. A poisoned string in a logged feature reaches `float()` and produces `ValueError: could not convert string to float: '<attacker content>'`, placing attacker-chosen text on stderr. I rate this minor because the content originated in the log the attacker already controls.

---

### Finding 11 — `COLD_WEIGHTS` is a mutable module global, and the regime label is computed by comparing against that same global
**Severity: LOW** — no live mutation exists; this is defense-in-depth, but the coupling is worth naming because both guarantees fail together and silently.
**Anchor:** `curator_shadow.py:101`, `:381`, `:402`.
**Confidence: CONFIRMED by reading.**

The byte-identical cold-start guarantee (claim (d)) rests entirely on `COLD_WEIGHTS = {"recency": -1.0}` being exactly that. It is an ordinary mutable dict at module scope, exported by name and imported by CS1 (`:24`-region) and the audit probe. If anything ever mutated it in place, the cold order silently stops reproducing the rule order — **and simultaneously** `weights != COLD_WEIGHTS` at `:402` starts evaluating against the mutated value, so the regime would still be labelled `"cold_start"`. The guarantee and its self-report share a single mutable point of failure. I checked both importers: CS1 uses `dict(_CS_COLD)` and the probe uses `dict(COLD_WEIGHTS)` — both copy. Nothing mutates it today.

Related, same area: `_weights_for:401` returns `_WEIGHT_CACHE[cache_key]` — the live cached object, not a copy — while the cold branch at `:381` returns `dict(COLD_WEIGHTS)`, a copy. The asymmetry means any future caller that mutates the returned trained weights corrupts the cache for every subsequent turn in the process.

---

### Finding 12 — The kill switch is an exact-string comparison, and the byte-identical acceptance proof's control arm depends on it
**Severity: LOW** — but it sits directly under claim (d)'s evidence.
**Anchor:** `curator_shadow.py:415`.
**Confidence: CONFIRMED by reading.**

```python
if os.environ.get("HIP_CURATOR_SHADOW", "1") == "0":
```

Default is ON. Only the literal `"0"` disables. `HIP_CURATOR_SHADOW=false`, `=no`, `=off`, `=disabled`, `=""`, or `"0 "` with a trailing space **all leave the scorer running**, with no warning. The module docstring (`:9-11`) states this toggle exists "solely so the byte-identical-prompt acceptance proof can run the same turn with and without the scorer." If that proof's off-arm ever sets a value other than exactly `"0"`, it compares scorer-on to scorer-on and passes trivially. Nothing in the proof asserts that the scorer actually did *not* run — there is no counter, no sentinel, no returned marker to check.

---

### Finding 13 — Documented-claim mismatches I could check
**Severity: LOW** each; grouped because each is a one-line divergence between prose and code.
**Confidence: CONFIRMED by reading** both sides.

**(a) `recency_rank` does not carry `valid_from` ordering.** `curator_shadow.py:24-27` justifies rank-as-recency by asserting "the rule order IS timestamp-DESC … so rank preserves exactly the ordering information `valid_from` age would." The live retrieval query at `memory_engine/recall.py:87` is `ORDER BY f.recorded_at DESC` — *recorded_at*, when the row was written, not *valid_from*, when the fact became true. These diverge for any backdated or re-recorded fact. The check_registry coverage entry (`check_registry__L7_CS1_entry.py.txt:40-43`) repeats the claim as a "named deviation," which makes it load-bearing. Additionally the `ORDER BY` has **no secondary sort key**, so the rule order among facts sharing a `recorded_at` is unspecified.

**(b) `subject_is_requester` is case-sensitive where the contract is not.** `curator_shadow.py:155` does `fact.get("subject") == requester`. `harness/injection_contract.py:413-414, 450, 506` case-fold both sides throughout. A fact with `subject="Maya"` admitted for requester `"maya"` yields `subject_is_requester=False` — the feature systematically disagrees with the contract that admitted the fact.

**(c) The reconstruction path recomputes a trust rung from props the record does not carry.** `build_training_examples:314` falls back to `extract_features(entry, ...)` where `entry` is a record `admitted` entry. Live `harness/epistemic_record.py:86-98` shows `_fact_entry` emits `fact_id, attribute, owner, subject, confidence, sensitivity, write_state` — and **not** `derived`, `confirmed_by`, or `confidence_log`. `_trust_rung` (`curator_shadow.py:110-125`) guards on `"write_state" not in fact`, but `_fact_entry` writes that key **unconditionally**, so the guard is always satisfied on reconstruction and `classify_trust_props` runs with `derived=False, confirmed_by=None, confidence_log=None` every time — systematically collapsing DERIVED/CONFIRMED/CORROBORATED to ASSERTED or UNCONFIRMED. This is precisely the failure `_fact_entry`'s own comment says the guard prevents ("classify on partial props would silently misreport UNCONFIRMED"). The record already stores the *correct* rung at `entry["level"]`, and `extract_features` does not read it.

**(d) The allowlist does not run in-path.** `validate_feature_dict` is called only from `train_weights:341`. Neither `score_facts` nor `shadow_score_turn` validates the extractor's output. The docstring at `:78` calls it "Allowlist-enforced," and CS1 (iii) invokes it manually on `_cs_feats`, which together read as in-path enforcement. It is training-path-only.

**(e) `_TRUST_ORDINAL` encodes ladder *match order* as trust *magnitude*.** `curator_shadow.py:96-97` assigns DERIVED = 1.0 > CONFIRMED = 0.9. Live `memory_engine/trust.py:64-78` documents that ladder as "first-match-wins … evaluation order," not a trust ranking. Encoding a system-inferred fact as more trustworthy than a human-confirmed one is an unjustified assumption inherited from an ordering that was never meant to be a magnitude.

---

## 3. Direct answers to (a) — (d)

### (a) Can any feature leak cross-household or cross-scope signal — including via sensitivity, the metadata keys, or the agreement metric?

**Not via the feature values themselves. Yes via two channels beside them.**

The value-blindness claim **holds as written**: `extract_features` (`:128-159`) reads `attribute`, `owner`, `subject`, `confidence`, `write_state`, `sensitivity`, and `fact_id` by name and never iterates the fact dict. Two facts identical in metadata and different in value produce identical feature dicts. I traced every read and found no value key touched. `sensitivity` is a stored metadata label validated against a closed four-value vocabulary (`extraction_queue.py:95`), not derived from value text at feature time — Bill's D-33 ruling is consistent with what the code does. It is, however, *wrong* for `"critical"` (Finding 7).

Cross-household leakage via the features requires the same `fact_id` in two households, which uuid4 makes infeasible. That one holds.

The two real channels are beside the features:

1. **`outcome_events` is a global aggregate stamped into every household's record** (`:262-266`, logged at `:439`). It counts outcome events across the *whole log* with no household or member partition. In the multi-household deployment the docstring contemplates (`:50-52`), household A's record carries an integer that is a running count of household B's corrections, and household B's activity determines when household A leaves cold start. Low bandwidth, but it is a cross-household signal written into a per-household record.

2. **`_WEIGHT_CACHE` is not partitioned at all** (Finding 3). This is the sharper version of the same limit: the docstring names the *count* as single-household but never names the *cache key*, so one household's fitted artifact serves another household's turn whenever both sit in the same 50-event bucket.

**The agreement metric does not leak.** I read `curator_agreement.py` closely. `shadow_outcome_agreement` (`:21-45`) filters the lookahead by `x.get("member") == member` (`:30`) and only ever compares fact_ids *within a single record's own logged ranking* (`:37-39`) — it never joins across members or households. Pairs are drawn from `ranking`, which is by construction a subset of that turn's admitted set. **This one is clean; I found no crossing in it.** Its weakness is elsewhere: it pools rankings produced by arbitrarily many different weight vectors into one number, with no way to partition them, because the record logs no weight identity (Finding 3.3).

**Within-household, cross-member:** `historical_acceptance` genuinely does aggregate all members' correction behavior (`:269-280`, no member filter). I traced whether that constitutes an intra-household scope crossing under the D-23 ruling and concluded **it does not** — the lookup is keyed by fact_id, only fact_ids already in this turn's `allowed` set are consulted, and INJ-3 keeps another member's personal facts out of that set. The only facts whose history crosses members are household-owned, whose audience is the whole circle. Stated plainly: this one holds.

### (b) Can the train_weights path be poisoned, or bypass the gate the way the gate's own target side was bypassed?

**Poisoned: yes — Finding 1, and it is the same root cause as the prior seven.** The gate authenticates `example["fact_id"]` and nothing else about the example. The `features` dict and the `label` are read from `logs/turns_demo.jsonl`, an unauthenticated local file, and the *only producer of examples* (`build_training_examples:322`) unconditionally stamps the exact `label_source` constant the gate's V4 checks — so V4 is structurally incapable of firing. The gate validates the *relationship* between a genuine fact_id and a caller-supplied household/audience; it never authenticates that the *feature vector and label beside that fact_id* came from the system that minted it. That is D-25's shape, moved one layer out.

**A second, weaker but fully in-band poisoning path:** `outcome_event_count` (`:262-266`) counts any record with a non-null `outcome.kind`, which includes `"override"`. Per live `harness/outcome_classifier.py:45-46`, `override` fires on `path == "control_decline"` — a member declining a confirmation prompt — and carries **no** `target_fact_ids`. So an ordinary household member saying "no" to 100 confirmation prompts pushes `n_events` past `COLD_START_THRESHOLD` and flips the deployment out of the safe byte-identical regime, onto a fit whose labels are all 1 (no corrections were produced). No file access required. **This is latent today** only because of Finding 4 — the model is unregistered, so the fit produces nothing. One `register_model` call, which the docs correctly describe as the intended operator act, arms it.

**Bypass: not in the D-37 sense, but the no-bypass proof is weaker than stated.** `_fit_weights` is private only by convention; CS1 imports and calls it across the module boundary (`layer7_crypto__L7_CS1_check.py.txt:24, 235`). More importantly the fixture that proves the gate "materially excludes" the example is itself built by pairing one fact's features with another's fact_id (`:227`) — the exact decoupling Finding 1 exploits. The proof and the hole are the same construction.

I looked specifically for the D-37 empty-set shape (`frozenset()` is not `None`) elsewhere in this module and did **not** find a recurrence: `learner_isolation.py:423` now uses `not ex_aud or not tgt_aud`, which is correct for both `None` and empty. `curator_shadow.py:348` (`if not admitted`) fails to cold weights, the safe direction. Those hold.

### (c) Is "shadow" actually airtight — any path where the scorer's output could reach the prompt?

**Today: yes, it is airtight. I could not find a path, and I looked hard.**

I traced every consumer in the live repo, not just the two files CS1 scans. `rg` over the whole tree shows the only non-eval, non-doc importer of `harness.curator_shadow` is `server/voice_orch.py:2754`, inside the emit hook, which runs after the reply is produced and whose return value is placed only into `kwargs["curator_shadow"]` (`voice_orch__shadow_hook.py.txt:96-101`). `reply_out` is never touched. `harness/epistemic_record.py` treats the field as pure projection (`:296`). The only readers of the field are `eval/harnesslib/curator_agreement.py` (offline eval) and `build_training_examples`. `harness/orchestrator.py` has zero references. There is no ranking, retrieval, or prompt consumer.

**Three qualifications, none of which break it today:**

1. **The proof does not generalize** (Finding 6): two files, two inconsistent regexes, four un-scanned emit paths, no coverage of `score_facts`/`extract_features`, defeated by an import alias, and a span delimited by a movable comment.
2. **There is a loop, just not to the prompt.** `shadow_score_turn` writes `features` into the record (`:441`); `build_training_examples` reads them back as training input (`:309`, `:314`); the fit produces weights; the weights produce the next ranking. The scorer trains on its own logged output. This closes no path to the prompt — but it is what makes an append to the log a *durable* poisoning primitive rather than a one-turn one, and the docstring presents it as a fidelity feature ("scored exactly as the turn saw them") rather than as loop closure.
3. **The kill switch cannot act** — true, as claimed, and correctly characterized as implicit. But the *off* setting is a fragile exact-string match (Finding 12), and claim (d)'s own control arm depends on it.

### (d) Does the cold-start byte-identical claim hold under adversarial input?

**The arithmetic holds. The claim's scope and its evidence are narrower than stated.**

The arithmetic is sound and I verified it by hand. Under `COLD_WEIGHTS = {"recency": -1.0}`, `_score` (`:205-207`) iterates `weights.items()` — one dim — giving `score_i = -1.0 * float(rank_i) = -rank_i`. `float(features.get("recency_rank") or 0)` at `:193` receives an `enumerate` index, always a small non-negative int, exactly representable. `rows.sort(key=lambda r: -r[1])` sorts ascending on `rank`, which is already the input order, and Python's sort is stable, so equal keys cannot reorder. There are no equal keys anyway — ranks are distinct. **The cold output is the input order, exactly, for any admitted set.** No adversarial *fact metadata* changes this, because under cold weights no other dimension is consulted at all; you could set every other feature to anything and the order would not move.

Four things do break around it:

1. **An attacker chooses when cold start ends** (answer (b)): 100 confirmation-declines, or 100 appended log lines with any `outcome.kind`, and `n_events` crosses the threshold. The guarantee is unconditional *within* the regime and the regime boundary is attacker-controlled. `COLD_START_THRESHOLD = 100` is never exercised by any test (CS1 passes `records=[]`, so `n_events == 0`).
2. **The guarantee and its self-report share one mutable global** (Finding 11). If `COLD_WEIGHTS` is ever mutated in place, the order stops reproducing *and* `weights != COLD_WEIGHTS` at `:402` silently re-baselines, so the record still says `"cold_start"`.
3. **"Byte-identical" is asserted twice with different meanings.** The *ranking* identity is what I verified above and it holds. The *prompt* identity (docstring `:9-11`) is trivially true — the hook runs after the prompt left — but its stated evidence is a differential run under `HIP_CURATOR_SHADOW`, whose off-arm is an exact-string comparison with no assertion that the scorer did not execute (Finding 12).
4. **The reference order it reproduces is not what the docstring says it is.** The claim is that rank carries `valid_from` ordering; the live query is `ORDER BY f.recorded_at DESC` with no tiebreak (Finding 13a). The shadow order faithfully reproduces the rule order; the rule order is not the one documented.

---

## 4. Attack classes the CS1 acceptance test does NOT cover

The gate's coverage had no input-trust axis and seven holes came through. CS1's coverage has the **same** gap plus three more. Systematically:

### Axis 1 — Input trust (the same axis that let the seven through)
**Why the test cannot see it.** Every input CS1 feeds the scorer is a hand-authored Python literal in the same file: `_cs_facts` (`:43-61`), `records=[]` (`:75`), `_cs_exs` built by calling `_cs_extract` on those same literals (`:221-226`). CS1 never once reads `logs/turns_demo.jsonl`, never calls `load_records`, never calls `build_training_examples`, and never constructs an example from a record. There is no test in which the scorer receives data it did not itself produce. The entire class of "what happens when the record stream is hostile" is invisible by construction.

**What a covering test would have to do.** Write an adversarial JSONL fixture and drive `build_training_examples` → `train_weights` from it. At minimum: a real in-household fact_id paired with a fabricated feature vector; a fabricated `label`; 100+ synthetic `outcome.kind` records to force the threshold crossing; a nested payload under a declared key; a feature value of `"1e400"`, `"nan"`, `-99`, and a non-string `attribute`. Then assert something *about the resulting weights*, not merely that nothing crashed. The correct fix, though, is upstream of the test: bind the feature vector and label to the fact_id cryptographically or derive them server-side, so the gate authenticates all three operands rather than one.

### Axis 2 — Cross-boundary correspondence: does `features` belong to `fact_id`?
**Why the test cannot see it.** CS1's cross-household fixture *is* a mismatched pair — `_cs_bad = dict(_cs_exs[0], fact_id="cs-x")` (`:227`) — deliberately. The test needs the mismatch to work in order to construct its poisoned example, so it can never assert that mismatches are refused. The property is not just untested; the test suite depends on its absence.

**What a covering test would have to do.** Assert that an example whose `features` were not derived from its own `fact_id` is refused — which requires the gate to be able to tell, which requires a binding that does not currently exist. This is a design gap the test surfaces rather than a test gap alone.

### Axis 3 — Nesting depth in the feature allowlist
**Why the test cannot see it.** Twin (iii) at `:108-113` supplies three flat, single-level dicts. The recursive check (`_find_gate_decision_key`) and the flat checks (`_FORBIDDEN_VALUE_KEYS`, `DECLARED_FEATURE_KEYS`) are exercised on the same depth-0 input, so their divergence at depth ≥ 1 is invisible.

**What a covering test would have to do.** Assert `validate_feature_dict({"attribute": {"value_text": "SECRET"}})` is **not** `None`, and the same for a list-nested payload, a key at depth 3, and a non-string key. Today the first of those returns `None`.

### Axis 4 — The trained regime, end to end
**Why the test cannot see it.** CS1 exercises the trained path only through hand-built weight dicts fed *directly* to `score_facts` (`:251-252`, and `trained = {...}` at the probe's `:25`). `shadow_score_turn` is called exactly once, with `records=[]`, which returns from `_weights_for:381` before the trained branch. **`_WEIGHT_CACHE`, `cache_key`, the `except Exception` handler at `:397-400`, the regime string at `:402`, `load_records`, `outcome_event_count`, `acceptance_history`, and `build_training_examples` all have zero coverage.** The coverage entry (`check_registry__L7_CS1_entry.py.txt:49-51`) names "the trained regime live on a real graph" as uncovered — but the uncovered surface is much larger than that phrase implies: it is the entire regime-selection and caching machinery, which needs no graph at all to test.

**What a covering test would have to do.** Drive `shadow_score_turn` with a synthetic record stream that crosses the threshold, then assert: the reported `regime` matches the weights actually used; a second call at a different `n_events` in the same bucket does not silently reuse a fit from a different record set; and a fit failure reports itself distinguishably from cold start.

### Axis 5 — Production resolvers and the registry
**Why the test cannot see it.** Twin (vi) injects `_CsResolver` and `_CsModelResolver` (`:201-217`), in-memory dicts keyed on `"curator-shadow-hh-alpha"`. Production computes `"curator-shadow-default"` (`curator_shadow.py:387`) and binds `RegistryProvenanceResolver`/`RegistryModelResolver`. CS1 therefore proves the gate's *logic* and proves nothing about the wiring — which is how Finding 4 (zero `register_model` callers; the trained regime structurally unreachable and silently indistinguishable from cold start) survives a green CS1.

**What a covering test would have to do.** Assert that `RegistryModelResolver().resolve(MODEL_ID_PREFIX + DEFAULT_HOUSEHOLD_ID)` returns a `ModelScope` — i.e. that the model production will actually name is registered — and that `_weights_for` at `n_events ≥ threshold` does not report `"cold_start"`.

### Axis 6 — Value-domain and vocabulary coverage
**Why the test cannot see it.** `_cs_facts` uses only `high`/`medium`/`low` for both `sensitivity` and `confidence`, only `""`/`"confirmed"`/`"supersede"` for `write_state`, and `derived=False, confirmed_by=None, confidence_log=[]` on all four facts. The fourth sensitivity level `"critical"` (Finding 7), the DERIVED/CONFIRMED/CORROBORATED rungs, unknown-vocabulary values, `None`, empty string, and non-string types are all outside the fixture. The `_ORDINAL.get(..., 0.5)` neutral default means every one of these silently produces a plausible-looking number rather than an error.

**What a covering test would have to do.** Assert `_encode` over the **declared** vocabularies rather than a four-fact sample — a table-driven check that every value in `SENSITIVITY_LEVELS`, `CONFIDENCE_LEVELS`, and the five trust rungs maps to a distinct, correctly-ordered encoding, and that an out-of-vocabulary value is distinguishable from a valid one.

### Axis 7 — Numeric adversariality
**Why the test cannot see it.** All fixture facts produce features in `[0, 1]` with small integer ranks. Nothing in CS1 supplies `inf`, `nan`, a negative `historical_acceptance`, a large `recency_rank`, or a string where a float is expected. The `min`/`max` clamp at `:367` guards `math.exp` and gives the impression the fit is numerically hardened; it does not guard `w`, and NaN silently defeats it (`min(30.0, nan) == 30.0`).

**What a covering test would have to do.** Assert `_fit_weights` returns all-finite weights for adversarial feature values, and assert `shadow_score_turn` never emits a non-finite number into the record. Neither property holds today.

### Axis 8 — Sort-order semantics (the subset assertion's blind spot)
**Why the test cannot see it.** Twin (ii) green (`:98-102`) and check (vii) (`:254-259`) are both **tautologies**. `score_facts` returns exactly one row per input fact and then sorts; a sort can neither add nor remove elements. So `sorted(_cs_rank_tr) == sorted(_cs_ids)` and `_cs_vout(_cs_ids, ranking) is None` are true for **every possible implementation of `_score`**, including one that returns random numbers. The subset invariant constrains membership only — and order is the entire product. Nothing in CS1 asserts anything about *which* order the trained regime produces.

**What a covering test would have to do.** Assert order, not membership: given a specific weight vector and specific facts, assert the exact expected ranking, hand-computed. And separately assert `len(ranking) == len(scores) == len(features)` so the duplicate/None fact_id collapse (Finding 9) surfaces.

### Axis 9 — Metamorphic: the query-text property is enforced by a variable-name string match
**Why the test cannot see it.** This is the weakest construction in the suite. CS1 (ix) at `:276-285`:

```python
_cs_m1 = _cs_score(_cs_facts, sio_attribute="medication", requester="maya", weights=dict(_CS_COLD))
_cs_m2 = _cs_score(_cs_facts, sio_attribute="medication", requester="maya", weights=dict(_CS_COLD))
```

These are **byte-identical calls**. `[r[0] for r in _cs_m1] == [r[0] for r in _cs_m2]` is true for any deterministic function. The audit probe (`harness_audit__cs1_query_reword_probe.py.txt:27-34`) is worse: it loops `for _reword in ("What medication is Maya on?", "which meds does maya currently take")` and **never uses `_reword`** — the loop variable is dead, and `ranks[0] == ranks[2]` again compares identical calls.

The only non-tautological content in both is `"query" not in extract_features.__code__.co_varnames` — a check that the literal string `"query"` does not appear among the function's local and parameter names. Rename the parameter `utterance`, `text`, `q`, or `user_input`, hash it into a feature, and **both the CS1 check and the audit probe pass**.

**What a covering test would have to do.** Actually vary the query. Drive the full turn path with two rewordings that resolve to the same SIO attribute, and assert the two resulting `curator_shadow.ranking` values are equal. The current tests establish only that the function is deterministic.

### Mutation summary — changes to `curator_shadow.py` that CS1 would not catch

I worked these through against each sub-check:

| Mutation | CS1 result | Why it survives |
|---|---|---|
| Delete `validate_feature_dict(...)` from `train_weights:341` | **passes** | (vi)'s bad example is rejected on `fact_id`, not features |
| `COLD_START_THRESHOLD = 100` → `1` | **passes** | (i) uses `records=[]`, `n_events == 0`, always cold |
| `cache_key = n_events // 50` → `cache_key = 0` (one global fit forever) | **passes** | branch never entered |
| `_weights_for` returns `("cold_start", trained_weights)` — mislabel the regime | **passes** | regime only checked in the cold path |
| Make the `validate_shadow_output` suppression branch (`:429-434`) return the ranking anyway | **passes** | `violation` is `None` in (i); the branch has zero coverage |
| `_encode`'s `"sensitivity"` line reads `attribute` instead | **passes** | keys unchanged, value-blindness unchanged, cold weights ignore it |
| Change `lr`/`epochs` in `_fit_weights` | **passes** | (vi) compares gated-vs-clean-vs-bypass; all three shift together |
| Add an `utterance` param to `extract_features` and hash it into a feature | **passes** | (ix) only bans the literal name `"query"` |
| Leak the value into `attribute` **conditioned on `owner == "household"`** | **passes** | (iv) tests exactly one fact, `_cs_facts[0]`, `owner="maya"` |
| Remove the `except Exception` at `:444` | **passes** | never triggered |

For contrast, the checks that **are** load-bearing and would catch a real regression: (i) catches a reversed or perturbed cold-start sort; (ii) red catches a neutered `validate_shadow_output`; (iii) catches a *new* feature key or a removed refusal; (iv) catches an *unconditional* value leak into an existing key; (vi) catches removing the gate call from `train_weights`. That is a real, non-trivial core — the problem is that the surface around it is much larger than the tests reach, and four of the nine sub-checks assert propositions that cannot fail.

---

## 5. What I could not determine

- **Whether any of the numeric findings reproduce at runtime.** I did not execute Python. Finding 9's `0.0 * inf = nan` and `min(30.0, nan) == 30.0` follow from IEEE 754 and CPython's `min` semantics, and I state them with confidence; the exact permutation Timsort yields on NaN keys I mark PLAUSIBLE because I did not run it. Similarly Finding 8's maximum achievable negative `historical_acceptance` depends on how many corrections actually land in a 20-record lookback window in practice.

- **Whether `logs/turns_demo.jsonl` is writable by anything other than the server user in the real deployment.** I observed `-rw-r--r-- bill-ai staff` in this working tree. Finding 1's severity is a function of who can append to that file in production, which I cannot see from here. What I *can* state is that the code applies no integrity check regardless of who writes it.

- **Whether `learner_models` is populated in any live database.** I established that `register_model` has zero callers in the repository. I did not query any SQLite file (out of scope), so an out-of-band manual registration — which the module's own docstring describes as the intended operator act — would not be visible to me. Finding 4's code path is confirmed; its current *state* is inferred from the absence of any registering code.

- **Process lifetime.** Finding 3's stale-weights scenario requires a server process that outlives a log reset. I could not observe deployment topology, restart policy, or whether the demo runs as a long-lived process or per-turn.

- **Whether the byte-identical-prompt acceptance proof exists and how its control arm is set.** The REQ doc references it (`docs/requirements/REQ_CURATOR_SHADOW_SCORER__...:104`) but I did not open the proof or any dispatch doc. Finding 12 identifies a fragility in the mechanism the docstring says that proof uses; I make no claim about how the proof actually invokes it.

- **The seven prior holes.** I did not read the D-25/D-30/D-36/D-37 dispatch docs. My characterization of the root cause ("validated the relationship, never authenticated the origin") comes from `learner_isolation.py`'s own module docstring at `:9-40` and `:67-81`, not from the underlying findings. If that docstring mischaracterizes the prior work, my Finding 1 framing inherits the error — though the finding itself stands on the code independently.

- **Reviewer A's findings.** By construction. One line of an existing review doc appeared incidentally in grep output (disclosed in §1); I did not read the document, and I have no visibility into overlap or divergence.
