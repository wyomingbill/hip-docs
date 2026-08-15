# REQ_LEARNER_TARGET_AUTHENTICATION: Authenticate the Target Side, and Wire the Battery That Guards It
Status: MET
Branch: roadmap

## MET-Ruling: Bill, 2026-07-30 (D-39 dispatch)

Both preconditions this REQ named at build time are demonstrated:

1. **The 7th hole is closed.** `target["household_id"]`/`audience` are no
   longer caller-supplied — `ModelResolver`/`RegistryModelResolver` derive
   them from the new `learner_models` registry plus the same live-roster
   functions the example side already used, and emptiness now fails closed
   on both operands exactly as `None` does. 3 additional target-side cases
   (target-scope forgery, unregistered model, `None` audience) added
   alongside the empty-audience case itself.
2. **The battery is wired and PROVEN load-bearing, not merely present.**
   `scripts/run_harness.sh` runs the 27-case adversarial battery before the
   harness on every pass. Verified by fault injection: inverting a single
   case's expectation made the run exit 1 and abort BEFORE `eval/harness.py`
   started; reverting restored green. Case `e3` (empty roster both sides)
   was deliberately REVERSED from its old "vacuously admissible" expectation
   to "violation" — the exact reasoning the hole had exploited.

Evidence trail this ruling rests on: an external review (Fable, two
independent reviewers, D-35) found the target-side asymmetry and the
unwired battery; D-36 confirmed both by live reproduction against the
committed gate (plus a third, separately-tracked finding — the dyad schema
defect, deliberately NOT bundled here, see `REQ_DYAD_AUDIENCE_DERIVATION`);
D-37 built the fix to a REQ filed before any code, following the D-27
xfail(strict=True)→XPASS→real-PASS pattern for the new case; D-38 cleared
the `--full` memory block and ran it green. Full evidence in the D-38 block
below and in the D-36/D-37/D-38 dispatch history.

REQ_LEARNER_SIGNAL_ISOLATION, whose MET was pulled back by D-37 on account
of this REQ's findings, is now MET again — through this REQ as its
successor fix spec, the same relationship D-30 had to D-29. See that REQ's
own D-39 status note.

## --full RESULTS (D-38, 2026-07-30)

D-37 built this REQ and deferred `--full` (memory-blocked, 0.29GB free vs the
2GB TD-129 threshold). D-38 freed memory (unloaded three idle Ollama models
on the dev daemon 11434 — the frozen demo daemon 11435 was untouched,
already empty — 0.32GB → 3.83GB free) and ran it. Both daemons confirmed
still listening throughout; no reboot, no cross-graph preflight.

`scripts/run_harness.sh --full`, exit 0:

- **Standing adversarial battery (pre-harness, item 6/7): 27/27, ZERO xfail.**
  Runs before the harness on every pass, as wired by D-37.
- **`--layer 7`: L7 27/27 (0 flaked, 0 skipped). L7V2 27/28 (1 skip —
  CT-OUTPUT-GAP, pre-existing opt-in live-model check, unrelated).**
- **LI1 PASS. G0/PSA1/CTX-STRIP/LI1 (the full ABSOLUTE tier) all PASS.**
- **AUDIT 8/8 — 59 checks enumerated, 0 missing artifacts, 35 debt-flagged
  gaps (unchanged from D-37's `--layer 7` run).**
- **CS1 PASS** (Curator shadow scorer's own check — this REQ's target-side
  fix required a two-line forward of `model_resolver` through
  `curator_shadow.train_weights`, so CS1 is a direct consumer).
- **`care_coordination.T01`/`T02` (the D-26/Groq-400 history) both PASS.**
- **RATCHET PASS — no scenario regressed vs baseline** (line "RATCHET PASS —
  no scenario regressed vs baseline.", exit 0).
- COVERAGE-GRID-RATCHET PASS (no unaccounted coverage-fraction decrease).

Two things observed in the run, both pre-existing and unrelated to this REQ,
named so they are not mistaken for new regressions:

1. **`L1:P2` (owner retrieval), iteration `i019`, sam/preference — FAIL.**
   Same iteration index, same scenario, same "write landed as active fact but
   count did not increase / value not active within 45.0s" signature named in
   REQ_HARNESS_DISCIPLINE's own MET report as "an async-write-timing race —
   same class as the previously-diagnosed R04/PW012/HARNESS1.3 flakiness."
   `eval/harness_baseline.json` records `"L1:P2": false` — the baseline
   itself does not assert this scenario always passes, so RATCHET correctly
   does not count it as a regression. Nothing in this REQ touches Layer 1
   write-timing.
2. **`decrypt failed for attribute=..., skipping` tracebacks for
   `psa1_probe_owner`.** That name is the PSA1 scenario's own synthetic
   fault-injection owner (`eval/harnesslib/layer7_crypto.py:1544`), not a real
   enrolled member — it has no `household_key_wraps` row by construction, so
   the read path correctly raises, is caught, logged, and skipped rather than
   crashing. Expected behavior of an existing probe, not new code.

Both preconditions this REQ named for re-earning MET were demonstrated here
— the wired battery green (D-37) and `--full` green (D-38) — and Bill ruled
MET on that evidence (D-39, above).

Reconciled-Against: f30ecd5 (2026-07-30), a0850c1 (D-37 build), --full green
this session (D-38, above);
REQ_LEARNER_SIGNAL_ISOLATION (status pulled MET → NOT MET by D-37 — this REQ
is its successor fix spec, the same relationship D-29 had to D-30);
DISPATCH_D36__verify-fable-curator-findings__v20260730_0851.md (all three
findings CONFIRMED by reproduction);
docs/reviews/FABLE_CuratorReview__test-model-and-gate-code-review__v20260730_0801.md
(the external review that found them, captured verbatim, D-35);
REQ_HARNESS_DISCIPLINE (MET — the Four, and the `_COVERAGE_KEYS` schema whose
missing trust axis is named below).

## THE REQUIREMENT

Bill's words, verbatim, from the D-37 dispatch that opened this REQ:

> - Authenticate the TARGET side too: target household_id/audience derived from the
>   verified registry/live-roster chain, same as the example side got in D-30 —
>   NOT caller-supplied. Fail closed on empty audience (frozenset()) exactly as on None.
> - Wire eval/test_learner_isolation_adversarial.py into run_harness.sh so the 23
>   cases run every harness pass and cannot regress silently.

Expanded. The gate compares two operands: the example's scope and the target
model's scope. D-30 made the first un-forgeable and left the second a
caller-typed dict. Every hole D-36 confirmed lives in that asymmetry. This
REQ closes it by giving the target side the same treatment the example side
already has — an injectable resolver, a production implementation that reads
server-authoritative state, and fail-closed behavior on anything it cannot
verify.

The second clause is not secondary. A gate whose adversarial battery runs in
no runner is a gate with no regression protection at all; the 23 cases that
encode the six closed holes can be deleted or inverted and every harness pass
stays green. Wiring the battery is a precondition of this REQ being MET, not
a nice-to-have.

## THE ACCEPTANCE TEST

Pass/fail per item; any single failure is FAIL; no partial credit.

**1. The target's scope is DERIVED, never read from the caller.**
`check_training_example` obtains the target's `household_id` and `audience`
from a `ModelResolver` keyed on `target["model_id"]` — structurally mirroring
`ProvenanceResolver`/`fact_id`. Any `household_id`/`audience` keys still
present on the caller's target dict are IGNORED, exactly as the example
side's are today. Observable: a target dict stamped `household_id=H1,
audience=CIRCLE1` whose `model_id` resolves to household H2 is judged against
H2 — the stamp carries no weight. FAIL: any verdict that changes when only
the stamped (non-`model_id`) fields change.

**2. An unresolvable `model_id` is refused, fail-closed.**
No `model_id`, or one the registry does not know, yields no `ModelScope` and
the example is REFUSED — never admitted, never routed to the shared-base
carve-out. This is the exact mirror of the D-30 unprovenanced-`fact_id` rule.
Observable: `model_id` absent → violation; `model_id="never-registered"` →
violation.

**3. An EMPTY audience fails closed on BOTH sides, exactly as `None` does.**
The 7th hole. `frozenset()` must be refused wherever `None` is refused, on
the target side and on the example side. Observable: member-private example
vs target audience `frozenset()` → VIOLATION (today: ADMISSIBLE). Also
household-circle example vs empty target → VIOLATION. And an empty *derived
source* audience → VIOLATION rather than the current
blocks-by-accident-or-admits-by-accident behavior.
**This intentionally changes an existing battery expectation.** Case `e3`
("empty roster both sides (vacuous) -> admissible is acceptable") is
REVERSED to expect a violation. That reversal is a deliberate, named
decision of this REQ, not an incidental edit: vacuous set-containment is
defensible in isolation and indefensible once an empty target audience is
known to be a universal key. The case is rewritten, not deleted, so the
change is visible in the battery's own history.

**4. The relationship math is UNCHANGED.**
D-25 and Fable both assessed the V1/V2 containment logic as sound; it must
not regress. Cross-household inequality, shared-base direction,
broader→narrower admissibility, and the intra-household containment test all
behave exactly as before on non-empty, resolvable inputs. Observable: every
pre-existing battery case except `e3` keeps its current expectation and
passes.

**5. Production derivation reads server-authoritative state.**
`RegistryModelResolver` resolves `model_id` → a registered learner model →
its `household_id` and `scope_class`, and derives the audience from the SAME
live roster functions the example side uses (`list_circle_members`,
`list_caregivers`, with their `removed_at IS NULL` currency), never from a
caller snapshot. A model must be explicitly registered by an operator act;
self-registration by the training caller is NOT a substitute and is not
built. Observable: registering a model and revoking a member changes the
derived audience on the next call, with no caller involvement.

**6. The battery runs on every harness pass.**
`eval/test_learner_isolation_adversarial.py` is executed by
`scripts/run_harness.sh` (or by `eval/harness.py` under it) on every run, its
result is visible in the output, and a failing case fails the run. Observable:
invert one expectation → the harness pass goes red; restore it → green. FAIL:
the battery being runnable-by-hand only, which is today's state.

**7. The 24th case exists and follows the D-27 pattern.**
The empty-audience case is added to the battery marked
`xfail(strict=True)` BEFORE the fix, demonstrating it red against the unfixed
gate, then flipped to a real PASS by the fix. All 24 cases run under the
wiring from item 6, with zero xfail remaining at the end. FAIL: landing the
case already-passing with no demonstration that it ever failed.

**8. The Four, for anything new.**
Any new or materially changed check carries its twin, fixture, coverage entry
and metamorphic wrapper per REQ_HARNESS_DISCIPLINE, and
`AUDIT:four-part-roster` stays green with zero new missing artifacts. The
L7:LI1 coverage entry is updated to name the target side honestly — including
that model registration is an operator act the gate trusts, which is this
build's own named trust boundary.

**9. Layer 7 and the ratchet stay green; `--full` before any MET.**
`--layer 7` green (LI1 and all ABSOLUTE checks), RATCHET PASS before and
after, and `python -m eval.harness --full` per Requirements Discipline item
12 before any MET is proposed. **No MET is proposed by the build.** MET is
Bill's ruling and, for this REQ, additionally requires items 6 and 9 both
demonstrated green.

## WHAT'S ALREADY DONE (do not redo)

- **The example side is authenticated and correct** (D-30, 82e86a9):
  provenance derived from a server-minted `fact_id` via `ProvenanceResolver`,
  live-roster audience binding, positive public marker. Do not touch this
  logic; mirror it.
- **The relationship math is sound** — confirmed independently by D-25 and by
  both Fable reviewers. It is not what is broken.
- **The 23-case battery exists and is well-built** (D-27/D-30). It needs
  WIRING and one reversed expectation plus one new case, not a rewrite.
- **The one production caller already derives its target audience from the
  live roster voluntarily** (`curator_shadow._weights_for` calls
  `list_circle_members(DEFAULT_HOUSEHOLD_ID)`). The gate simply never
  enforced it. This is why item 5 is a small change in production behavior.

## WHAT'S KNOWN BROKEN

- The 7th hole (empty target audience) — the thing this REQ exists to close.
- The battery runs nowhere — item 6.
- **The dyad audience branch reads columns that do not exist** — CONFIRMED by
  D-36 against the live DB. **DELIBERATELY NOT IN SCOPE HERE.** Different root
  cause (schema drift in an untested branch), different acceptance. It gets
  its own REQ; bundling a coding error into a security fix makes both harder
  to assess. Named here only so it is not mistaken for an oversight.
- **No learner-model registry exists today.** This REQ builds a minimal one
  because item 1 is impossible without it. It is deliberately small: model_id,
  household_id, scope_class, status, created_at. It is NOT a model lifecycle
  system and does not attempt to be.
- **The coverage schema still has no trust axis.** Fable's Option A (a fifth
  `trust_boundary` coverage key) would turn all ~59 registry entries red until
  each declares, which is a forced sweep and Bill's call, not a session's. NOT
  built here; carried as an open question.

## CONSTRAINTS

- **The working path is sacred.** RATCHET green before and after; layer 7 and
  AUDIT stay green; the demo on main and graph 7689 untouched.
- **Do not weaken the example side** to make the target side symmetric. If the
  two disagree, the stricter behavior wins.
- **Fail closed on every axis**: unresolvable model, empty audience, empty
  roster, missing scope class. Absence is never admission — the D-30 rule,
  applied to the new operand.
- **No self-registration.** The gate must not accept a model the caller
  invented at call time; registration is a separate, explicit act.
- **Do not mark this REQ MET**, and do not re-mark REQ_LEARNER_SIGNAL_ISOLATION
  MET. Both are Bill's rulings. The build reports and stages.

## OPEN QUESTIONS FOR BILL

1. **Does the `trust_boundary` fifth coverage key land?** Fable's Option A.
   Cheap to implement, but turns every registry entry red until declared —
   a deliberate forced sweep across ~59 checks.
2. **Should model registration require a quorum or operator ceremony**, as
   custody operations do under REQ_PARTITION_CUSTODY? This build treats
   registration as a plain administrative write. If a registered model's
   audience is a security boundary, its registration may deserve the same
   protection custody grants get.
3. **What happens to a model whose household's roster empties?** This build
   fails closed (no training). The alternative — treat an empty roster as
   "nobody reads it, so anything may train it" — is the reasoning that
   produced the 7th hole, so it is rejected here, but the disposition of such
   a model is a lifecycle question this REQ does not answer.
