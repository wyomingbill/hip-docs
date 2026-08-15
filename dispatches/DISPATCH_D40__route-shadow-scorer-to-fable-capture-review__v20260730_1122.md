# DISPATCH_D40
Status: BUILT
Reconciled-Against: ae74e48 (2026-07-30)

**TYPE:** ANALYSIS

**REQ:** NONE. This dispatch routes an external review and captures its
response verbatim. It produces no code change and proposes no requirement
status, so per Requirements Discipline item 10 it carries no REQ doc — that is
the honest state of review-routing work, not a gap to fill. The code under
review was built to
`docs/requirements/REQ_CURATOR_SHADOW_SCORER__stage2-shadow-metadata-scorer__v20260730_0710.md`
and gated by
`docs/requirements/REQ_LEARNER_TARGET_AUTHENTICATION__target-side-derivation-and-battery-wiring__v20260730_0851.md`;
both were ruled MET by Bill at D-39 (ae74e48) before this review was routed.

## THE ASK

The D-40 dispatch, verbatim as given:

> === D-40 | (~/hip-roadmap, roadmap) | route the built shadow scorer to Fable for code review, capture to repo ===
>
> 0. cd ~/hip-roadmap
>    whoami && hostname && pwd && git rev-parse --show-toplevel && git branch --show-current
>    Expect bill-ai / [REDACTED-MACHINE-NAME] / [REDACTED-USER-PATH]/hip-roadmap / roadmap. Mismatch → STOP.
> 1. Read-only. Snapshot the review target so Fable reviews a frozen copy, not a moving tree:
>    - harness/curator_shadow.py (the scorer + train_weights + validate_shadow_output)
>    - the shadow hook in server/voice_orch.py
>    - the curator_shadow field in harness/epistemic_record.py
>    - eval/harnesslib/curator_agreement.py
>    - the L7:CS1 check + its registry entry
>    Pin the commit (9d867f8 build + any D-38 model_resolver passthrough).
> 2. Route to Fable with this brief: "Attack this shadow scorer. It routes every
>    training example through the isolation gate — which just had a 7th hole found by
>    external review. (a) Can any feature leak cross-household or cross-scope signal —
>    including via sensitivity, the metadata keys, or the agreement metric? (b) Can the
>    train_weights path be poisoned, or bypass the gate the way the gate's own target
>    side was bypassed? (c) Is 'shadow' actually airtight — any path where the scorer's
>    output could reach the prompt? (d) Does the cold-start byte-identical claim hold
>    under adversarial input? Name attack classes the CS1 acceptance test does NOT cover
>    — the gate's coverage had no input-trust axis and that's how 7 holes got through."
> 3. Capture Fable's full response. Do NOT act on findings this pass. Write it to
>    docs/reviews/ (the folder D-35 already added to CLAUDE.md), commit with explicit
>    pathspecs, push. PRINT Fable's review to the terminal for screenshot.

## WHAT WAS DONE

In the order taken:

1. **Environment gate (step 0).** Ran the four-command check. Returned
   `bill-ai` / `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]/hip-roadmap` /
   `roadmap`. Matched; proceeded.
2. **Mapped the review target.** Located each named artifact: the scorer at
   `harness/curator_shadow.py`; the shadow hook at `server/voice_orch.py:2744-2760`
   plus the `sio_attribute` telemetry surface at `:2547`; the `curator_shadow`
   field at `harness/epistemic_record.py:207-211,296`; the agreement metric at
   `eval/harnesslib/curator_agreement.py`; the L7:CS1 check at
   `eval/harnesslib/layer7_crypto.py:1985-2271`; its registry entry at
   `eval/harnesslib/check_registry.py:491-552`; and the `cs1_query_reword`
   probe at `eval/harnesslib/harness_audit.py:513-548`. Added
   `harness/learner_isolation.py` and `harness/model_registry.py` to the
   package — the brief attacks the gate the scorer routes through, and the
   D-38 passthrough is meaningless without the target-side resolver.
3. **Pinned and snapshotted.** Copied the target to a scratchpad snapshot
   directory so the reviewers read a frozen tree.
4. **Caught HEAD moving mid-snapshot.** A parallel session committed D-39
   (`ae74e48`) while the snapshot was being taken, moving HEAD off `9cbb9ec`.
   This is exactly the hazard step 1 exists to prevent, so the pin was
   re-verified rather than assumed (see WHAT WAS FOUND).
5. **Routed to Fable.** Two independent Fable agents in parallel, identical
   brief, identical file set, blind to each other. The dispatch asked for one;
   two blind reviewers on the same brief is the D-35 precedent and a superset
   of the ask — convergence between blind reviewers is itself signal. Both
   were constrained read-only (no edits, no harness, no pytest, no database, no
   writing git commands) and both were explicitly instructed not to propose or
   imply any REQ status in either direction.
6. **Captured both responses verbatim** to
   `docs/reviews/FABLE_ShadowScorerReview__adversarial-curator-stage2-scorer-review__v20260730_1122.md`,
   with a routing-session header and a convergence map that is explicitly
   labelled as reading aid, not verification.
7. **Did not act on any finding.** No code was read for the purpose of fixing,
   nothing was changed, no status was proposed.

## WHAT WAS FOUND

### Snapshot fidelity (the process finding)

`git rev-parse HEAD` returned `9cbb9ec` at step 0 and `ae74e48` after the
snapshot — a parallel session committed D-39 mid-work. Verification performed
before routing:

- `git diff --name-only 9cbb9ec..ae74e48 -- '*.py'` → **empty**. D-39's own
  commit message states "No code changed this session."
- `git diff --quiet HEAD -- harness/ eval/ server/` → clean at the new HEAD.
- Each snapshot file `diff`-confirmed byte-identical to its repo counterpart.

So the reviewed bytes are the committed bytes at `ae74e48`, and `ae74e48` is
code-identical to `9cbb9ec` (which carries the D-33 build `9d867f8` plus the
D-37 fix `a0850c1` and the D-38 `model_resolver` passthrough). The findings
apply to committed code.

### Context change this dispatch did not anticipate

D-39 (`ae74e48`, 11:01 MDT) ruled **REQ_CURATOR_SHADOW_SCORER** and
**REQ_LEARNER_TARGET_AUTHENTICATION** MET, and re-MET
**REQ_LEARNER_SIGNAL_ISOLATION** via successor. This review was routed at
~11:05 MDT. D-40 is therefore a **post-ruling adversarial review**, not a
pre-ruling check. That does not change what the dispatch asked for, and this
dispatch proposes no status change in either direction — but the ordering is
recorded here so no later reader mistakes the review for input that informed
the MET ruling. It did not; it came after.

### Review findings — ALL UNVERIFIED

Full text in the review doc. Every claim below is a **reviewer claim**, not a
measurement by this session. Line anchors are the reviewers'.

**Both reviewers, independently and blind, converged on:**

- The trainer sources features and labels from `logs/turns_demo.jsonl` via
  `curator_shadow.py:309,314`, an unauthenticated plain-text append; the gate
  authenticates only `fact_id` (and `model_id`), never the feature values or
  the label. Both name this as the same root-cause shape as the prior seven
  holes. Both note the tamper-evident ledger holds the same records and is not
  the store the trainer reads.
- Gate check V4 (`learner_isolation.py:360-364`) is unfireable: the only
  producer, `build_training_examples:322`, stamps the exact constant V4 tests.
- `register_model` has zero callers, so `RegistryModelResolver` resolves the
  production `model_id` (`curator-shadow-default`) to `None`, V0b refuses every
  example, and the trained regime is structurally unreachable — reported as
  `regime: "cold_start"`, indistinguishable from the benign low-data state.
- `_WEIGHT_CACHE` is keyed only on `n_events // 50` — no household, no corpus
  identity, no invalidation.
- The prompt-touch static scan is weak (two files, two different regexes, a
  span delimited by a movable comment) — **but both independently confirm the
  shadow property itself HOLDS**: no path from scorer output to prompt.
- The metamorphic query-reword coverage is vacuous in both the CS1 check and
  the audit probe (identical calls; the probe's `_reword` loop variable is
  never used).
- `historical_acceptance` is unbounded and unclamped, reaching `inf`/`NaN`,
  which lands non-conformant JSON in the record.
- `validate_shadow_output` is tautological in-path — it constrains membership,
  never order.

**Reviewer A only (single-source, unconfirmed, and the most consequential
claim in the document):** `F1` — the correction/label substrate is structurally
dead. A traces `_D1_DELTA_FIELDS` and the `_store_delta` call site
(`fact_change.py:246`, `:863-873`) and reports neither carries `write_state`
nor `fact_id`, so `classify_outcome`'s `superseded_ids` is always empty and no
`correction` outcome can be emitted. If true: every training label is `1`,
`historical_acceptance` is a constant `1.0`, and the agreement metric returns
`None` on any real log. A cites all 12 records in the live log as supporting
evidence. B did not examine the outcome producer.

**Reviewer B only:** the feature allowlist is recursive for gate-decision keys
but top-level-only for value/undeclared keys (`curator_shadow.py:162-180`), so
a nested payload under a declared key validates clean; `sensitivity ==
"critical"` misses `_ORDINAL` and encodes to `0.5`, below `"high"`; gate
violation strings print live roster membership to stderr; `COLD_WEIGHTS` is a
mutable global that the regime label is computed against; `HIP_CURATOR_SHADOW`
is an exact-`"0"` match; plus five prose/code divergences. B also contributes a
ten-row mutation table of edits to `curator_shadow.py` that B argues CS1 would
not catch, and observes that CS1's own gate-bypass fixture is built on the same
features/`fact_id` decoupling the poisoning finding exploits.

**What both reviewers affirmed as holding** (recorded because a review that
only lists defects misrepresents the artifact): the shadow placement is real
and correctly built; `extract_features` is genuinely value-blind; the
cold-start byte-identical property holds under adversarial input because `rank`
is scorer-generated; and the D-37 empty-set (`frozenset()` is not `None`) shape
does **not** recur. Reviewer A calls the gate's own relationship logic "the
strongest thing in this snapshot."

## VERIFIED

- **Watched run:** the environment gate (four commands, output matched);
  `git rev-parse HEAD` before and after the snapshot (caught the D-39 move);
  `git diff --name-only 9cbb9ec..ae74e48 -- '*.py'` (empty);
  `git diff --quiet HEAD -- harness/ eval/ server/` (clean); per-file `diff` of
  every snapshot copy against its repo counterpart (all identical). These are
  the only claims in this dispatch this session observed directly.
- **Reasoned about:** nothing. This session did not independently evaluate any
  review finding — deliberately, per the dispatch's "Do NOT act on findings
  this pass."
- **NOT verified, explicitly:** every finding in the review document. Both
  reviewers were read-only and neither executed the code they reviewed; both
  say so in their own "what I could not determine" sections. Two blind
  reviewers converging raises priority for verification; it is not verification.

## HASH

Committed this dispatch: see the D-40 commit on `roadmap`. Code changed: **none** —
the only files added or modified are the review document, its LATEST symlink,
this dispatch doc, and the two `docs/INDEX.md` rows registering them.

## OPEN

1. **Verification is a separate dispatch and has not been done.** Every finding
   above is a claim. The D-36 precedent (live-reproducing the D-35 findings
   before acting) is the shape that fits here.
2. **Reviewer A's F1 is the highest-value thing to check first** and has no
   second opinion. It is cheap to test: drive a real supersede write through
   `fact_change` → `classify_outcome` and observe whether a `correction`
   outcome with non-empty `target_fact_ids` ever appears. If A is right, the
   agreement metric, the labels, and one declared feature are all inert, and
   several other findings change severity as a consequence.
3. **Both REQs are already MET.** Nothing here changes that, and this dispatch
   does not ask to. What Bill does with confirmed findings against an
   already-MET requirement — amend, log as debt, open a successor REQ, or
   accept as named limits — is his ruling, not this session's.
4. **Not asked and not done:** no fix, no test, no harness run, no `--full`.
   The dispatch was explicitly capture-only.
5. **Scope left out:** the reviewers read the ten snapshot files plus live-repo
   context. Neither queried the SQLite `learner_models` table (out of scope for
   a read-only pass), so the "zero `register_model` callers" finding is
   confirmed at the repo level but its runtime consequence is inferred — an
   out-of-band manual registration would change it.
