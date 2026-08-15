# DISPATCH_D41 — verify Fable's shadow-scorer findings

Status: BUILT
REQ: NONE — analysis/verification dispatch. It reproduces claims made by two
external reviewers (D-40) against committed code and changes nothing. Per
Requirements Discipline item 10, an ANALYSIS dispatch may carry REQ: NONE and
must say why; this is that statement. The status change this verification
supports, and the fixes it motivates, are dispatched separately (D-42) and
carry their own REQ update, as item 8 requires.
Branch: roadmap
Reconciled-Against: 47a7a42 (2026-07-30, D-40); code under test unchanged
since 9cbb9ec (D-33 build 9d867f8 + D-37 fix a0850c1 + D-38 passthrough,
confirmed identical — `git diff --name-only 9cbb9ec..47a7a42 -- '*.py'`
returns empty, D-39/D-40 are docs-only); live log `logs/turns_demo.jsonl`
(12 records); live registry `~/hip-harness/registry.db` (read against a copy,
never the live file — see "One thing I refused to do" below); full run log
`/tmp/hip_harness_20260730_1005.log`

Gate: PASSED (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap / roadmap).
Graph+harness lock taken, held for the run, released. **No code changed. No
REQ marked. Nothing fixed. Live registry DB not mutated.**

## What this dispatch was

D-40 routed the built Curator Stage 2 shadow scorer to two independent Fable
reviewers and captured both responses verbatim, explicitly unverified
(`docs/reviews/FABLE_ShadowScorerReview__adversarial-curator-stage2-scorer-review__v20260730_1122.md`).
This dispatch verifies four of their findings by reproduction rather than by
re-reading — running the actual code against the actual log, against
synthesized scenarios that isolate one variable at a time, and against a
mutation of the scorer itself — going beyond both reviewers, who were each
constrained to read-only source analysis and explicitly declined to execute
any code or query any database.

## RESULT: 4 of 4 areas CONFIRMED. Nothing refuted.

### (a) Dead correction/label substrate — CONFIRMED, and worse than reported

**The claim:** no `correction` outcome can ever be emitted, so every label is
`1`, `historical_acceptance` is a constant `1.0`, and the agreement metric
returns `None`.

**Root cause — a field-name mismatch.** `classify_outcome`
(`harness/outcome_classifier.py:52-57`) requires each delta entry to carry
`write_state == "supersede"` **and** a `fact_id`:

```python
superseded_ids = {d.get("fact_id") for d in (delta or [])
                  if isinstance(d, dict) and d.get("write_state") == "supersede"
                  and d.get("fact_id")}
```

The delta it actually receives carries **neither key**. `_store_delta`
(`fact_change.py:863-872`) writes the supersede signal under `transition`,
and the fact ids under `prior_fact_id` / `new_fact_id`. The projection then
narrows further — `_D1_DELTA_FIELDS` (`fact_change.py:223`) is
`(subject, attribute, from_state, to_state, transition, prior_fact_id, new_fact_id)`.

**Executed evidence** — a real supersede of a fact the member was shown last
turn:

```
projected delta       : {'subject':'maya','attribute':'medication','from_state':'ASSERTED',
                         'to_state':'ASSERTED','transition':'supersede',
                         'prior_fact_id':'f-PRIOR','new_fact_id':'f-NEW'}
proj has 'write_state': False
proj has 'fact_id'    : False
classify(projected delta) : {'kind': None, ...}      <-- textbook correction, NOT detected
classify(RAW delta)       : {'kind': None, ...}      <-- fails on the raw delta too
classify(hypothetical)    : {'kind': 'correction', 'target_fact_ids': ['f-PRIOR'], ...}
```

`outcome_classifier.py:80` is the **only** producer of `kind: "correction"` in
all production code (grep over `harness/ server/ memory_engine/ scripts/`).
It is unreachable.

**Ruled out the innocent explanation.** The live log being quiet is not the
cause. A synthesized two-turn history where the correction genuinely
happens, with the outcome computed by the *real* classifier exactly as
`voice_orch` computes it:

```
correction emitted?  : False
training examples    : [('f-PRIOR', 1)]        <-- corrected fact labelled ACCEPTED
CONTROL, same turns, outcome hand-forced to the expected shape:
training examples    : [('f-PRIOR', 0)]        <-- correct label
outcome_event_count  : 1
```

**The label is not missing — it is INVERTED.** The single strongest negative
signal in the system (the member corrected this fact) is recorded as a
positive one. Every consumer downstream is correct; only the producer is
broken.

**Downstream consequences, measured on the real 12-record log:**

```
outcome_event_count            : 0
training examples built        : 34
label distribution             : {1: 34}       any label==0? False
acceptance_history corrected   : all 0
historical_acceptance values   : {1.0: 32, None: 2}
agreement metric               : None
```

**And the fit on that corpus** (all 34 labels == 1) — every weight positive,
no discriminative signal, exactly the "positive projection of the corpus
mean" the reviewer predicted:

```
attr_bucket +0.7582  confidence +1.4303  family_match +0.7311
historical_acceptance +1.6721  recency +1.2439  scope_household +1.0090
sensitivity +0.7737  subject_is_requester +0.6165  supersession +1.0517  trust +1.2901
all weights non-negative -> True
```

**Bears directly on the REQ.** Acceptance item 7 ("Agreement-with-outcome
metric — HOLDS") rests on `curator_agreement_self_test`, which
**hand-authors** `{"kind":"correction","target_fact_ids":[...]}` records.
That shape cannot be produced by the classifier. The item passes on a
fixture that cannot occur.

### (b) Nothing registered → every example refused → always cold_start — CONFIRMED, stronger than reported

`register_model` has **zero code callers** — the only occurrence outside the
docs D-40 just wrote is its own definition (`harness/model_registry.py:88`).

**Important nuance the reviewers missed:** that is *by design*, not an
oversight. `model_registry.py:33-39` states plainly: *"REGISTRATION IS AN
OPERATOR ACT. Nothing here is called by the training path. A caller cannot
register the model it is about to train — that would recreate the
caller-asserts-its-own-scope hole this module exists to close."* The defect
is not the absence of callers. It is that **nothing has ever performed the
operator act**, and the resulting total refusal is silent.

**Closed the gap both reviewers left open** (neither could query the DB).
The live registry at `~/hip-harness/registry.db`:

```
tables: care_team_members, care_teams, dyad_key_wraps, dyad_members, dyads,
        household_key_wraps, household_keys, households, members, roles,
        sqlite_sequence, standing_policy_restrictions
learner_models present: False
```

The table does not merely lack a row — **it does not exist**.

**Runtime, against a copy of the live DB** (production `model_id` is
`curator-shadow-default`):

```
get_model('curator-shadow-default')                  -> None
RegistryModelResolver().resolve('curator-shadow-default') -> None
check_training_example(valid example, production resolver):
  "unresolvable training target: example e1 names model 'curator-shadow-default',
   which is not an active registered learner model with a derivable non-empty
   audience ... refused"
```

The example side was given an unimpeachably valid fixture provenance,
isolating the target side as the refuser.

**The regime conflation, executed** — 150 events, far past the 100
threshold:

```
outcome_event_count : 150   (threshold = 100)
above threshold?    : True
regime REPORTED     : 'cold_start'
weights == COLD_WEIGHTS : True
```

The record would read `outcome_events: 150, regime: "cold_start"` — the
total-refusal state is indistinguishable from the benign not-enough-data
state.

This direction is **fail-closed and safe**. The finding is that it is
silent.

### (c) `_WEIGHT_CACHE` unpartitioned — CONFIRMED as a mechanism, LATENT today

`_WEIGHT_CACHE` (`curator_shadow.py:376`) is a module global keyed **only**
by `cache_key = n_events // 50` (`:382`) — no household, no member, no
corpus identity, no TTL, no invalidation.

**Executed** (gate stubbed to admit, isolating the cache question from (b)'s
refusal — household A and household B have entirely different corpora):

```
household A fit  : regime=trained  key=3   A weights[attr_bucket] = +1.9357
household B turn : regime=trained  key=3   B weights[attr_bucket] = +1.9357
cache keys held      : [3]
B GOT A's ARTIFACT?  : True (object identity) / True (equality)
B's OWN fit would be : attr_bucket = +0.8046
B served A's weights instead of its own? : True
```

Household B is served household A's weight object, and B's own fit would
have been materially different. The ingress gate stops A's *examples*
reaching B's model; the egress edge has no equivalent control over which
household a fitted artifact is *applied to*.

**Honest reachability — two gates keep this latent right now:** (1) finding
(b) means no real fit ever occurs in production (the gate had to be stubbed
to force one); (2) `_weights_for` always targets `DEFAULT_HOUSEHOLD_ID` and
`load_records()` reads one log, so today there is one household. This is a
confirmed *mechanism*, not a live leak. It arms the moment a second
household exists **and** a model is registered.

### (d) Three sub-claims — ALL THREE CONFIRMED

**d1 — `historical_acceptance` unbounded → inf/NaN → invalid JSON.
CONFIRMED.**

```
injected=1 corrected=5 -> acceptance = 1 - 5/1 = -4.0   escapes [0,1]: True
validate_feature_dict(feats with -4.0)  -> None   (clean; the allowlist is NAME-only)
feature = inf: validate verdict         -> None   (clean)
  fitted weights all finite?            -> False   (weight = inf)
  resulting score                       -> inf
  json.dumps({"s": inf})                -> {"s": Infinity}   <-- bare Infinity, not valid JSON
```

Nothing anywhere validates a feature *value*; every check in the system is a
key-*name* check. Caveat, stated honestly: reaching a negative value in
production requires a `correction` record, which finding (a) says the
classifier cannot emit — so d1 is reachable today only by writing the log
directly, and arms fully the day (a) is fixed.

**d2 — `validate_shadow_output` tautological in-path. CONFIRMED.**
`shadow_score_turn` builds both operands from the same list: `ranking` from
`rows` (which enumerate `allowed`, `:426`) and `admitted_ids` from `allowed`
(`:427`). A sort can neither add nor remove elements, so the check cannot
fail in-path.

```
real turn curated_subset_ok : True
a SCRAMBLED ranking ['f2','f0','f3','f1'] -> validate_shadow_output = None (PASS)
```

Every permutation passes. It constrains **membership** only, never
**order** — and order is the entire product of a ranker.

**d3 — metamorphic reword check vacuous in BOTH the scenario and the probe.
CONFIRMED.** AST analysis of `_probe_cs1_query_reword`:

```
loop variable '_reword': bound once, READ 0 times in body
  the two "rewordings" are DEAD STRINGS:
    ['What medication is Maya on?', 'which meds does maya currently take']
  both iterations execute byte-identical score_facts() calls
```

The CS1 scenario check (`layer7_crypto.py:2276-2285`) likewise calls
`score_facts` twice with byte-identical arguments. The only non-trivial
assertion in either is `"query" not in extract_features.__code__.co_varnames`
— a check on a *variable name*. **Mutation test:** `extract_features` was
replaced with a version that takes an `utterance` parameter and hashes the
query text directly into a feature:

```
probe on MUTATED query-dependent scorer: PASS
```

A scorer that demonstrably depends on query text passes the check that
exists to prove it does not.

## CS1 is green while all of the above is true

From the last full run (`/tmp/hip_harness_20260730_1005.log:1382`):

```
CS1   PASS   the Curator shadow scorer can only narrow injection.allowed ...
             trains only through the MET isolation gate, and has no code path to the prompt
```

Nine sub-checks, all `[ok]`. Every finding above coexists with that green.

## One thing this dispatch refused to do

`get_model` is a read function with a **write side effect**: it calls
`_connect()` (`model_registry.py:74-81`), which executes
`CREATE TABLE IF NOT EXISTS` and commits. Calling it against the live
registry would have created the `learner_models` table — mutating the state
this dispatch was sent to observe, and destroying the "table does not exist"
evidence. The DB was copied to scratchpad and every resolver call ran
against the copy via `HIP_REGISTRY_DB`.

**Proof the side effect is real and was kept off the live DB:**

```
LIVE     learner_models present: False  | 13 tables
MY COPY  learner_models present: True   | 14 tables
```

The copy grew exactly the table `get_model` creates; the live DB did not.
This side effect is in neither Fable review — flagged here as its own small
finding, and a hazard for any future verification pass against this
registry.

**One thing that could not be attributed, stated rather than glossed:** the
live registry's mtime moved to 13:41, after the copy was taken at 13:40, and
the file now differs from the copy taken. The *schema* is unchanged and
`learner_models` is still absent — that is the evidence this dispatch rests
on, and it holds. But byte-identity of the file across that window cannot be
proven, and is not claimed. The likely cause is another process on this
machine opening the registry through a `_connect()` that runs its own
`CREATE TABLE IF NOT EXISTS` + `commit` (a no-op write that still bumps
mtime) — the parallel demo lane shares this host. Not chased further; it
does not bear on any finding here.

## What this dispatch did NOT do

No fix, no test added, no REQ assessed, nothing committed beyond this
record. The lock was taken and released. No `--full` was run.

## Disposition (carried into D-42)

All four findings bear directly on whether `REQ_CURATOR_SHADOW_SCORER`'s MET
ruling (D-39) was premature — not because the scorer's *isolation*
properties are broken (they are not) but because the *learning* substrate it
was built to prove out is structurally inert.

**What genuinely holds and should not be relitigated:** the scorer is real,
deterministic, value-blind, and structurally shadow. Cold-start byte-identity
holds (verified by both D-40 reviewers, and `rank` is scorer-generated so no
input can perturb it). The isolation gate's own relationship logic is sound
and the D-37 empty-set shape does not recur. The ingress gate is, if
anything, *over*-performing: it currently refuses everything.

**What does not hold:** the scorer cannot learn. Not "learns poorly" — the
label substrate cannot produce a negative example, so the corpus is
single-class and the fit is a positive projection of the mean. Acceptance
item 7's evidence is a fixture whose shape production cannot emit.

**The honest split:** *isolation holds; the learning substrate does not.*
BUILT describes that state accurately. MET does not.

**Explicitly not implicated: `REQ_LEARNER_TARGET_AUTHENTICATION`.** Finding
(b) shows the target side working exactly as designed — it refused an
unregistered target, fail-closed. D-39's ruling on that REQ is not
reconsidered here.

## Suggested next dispatches (carried into D-42 Part B)

1. **Fix (a)** — small blast radius: have `classify_outcome` read
   `transition`/`prior_fact_id` (the keys the projection actually carries),
   rather than widen the projection schema. The acceptance test must drive
   a real supersede end to end rather than hand-authoring the outcome
   record. This is the one that decides whether the scorer can learn at
   all.
2. **Decide (b)'s operator act** — either register `curator-shadow-default`
   as a deliberate operator step, or make the total-refusal state visibly
   distinct from cold start. Today it is silent.
3. **(c) and (d)** are real but latent, and both become live the moment 1
   and 2 land. Sequenced after, not before.
