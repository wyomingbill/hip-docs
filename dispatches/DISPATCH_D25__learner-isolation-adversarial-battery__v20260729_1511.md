# D-25 — adversarial battery vs the learner training-signal isolation gate

Date: 2026-07-29 (Mountain Time)
Gate: PASSED (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap / roadmap).
Lock: graph+harness, taken and released. Target under test:
harness/learner_isolation.py (REQ_LEARNER_SIGNAL_ISOLATION). Test code:
eval/test_learner_isolation_adversarial.py (NEW; does not touch the gate).
**No production code changed.**

Note on sequencing: D-26 already pulled the Stage-1 MET back to NOT MET on
the ONE hole it could confirm from code (provenance forgery), because this
D-25 report had not landed yet. This battery is that report — it re-proves
D-26's hole as a runnable test AND finds five more, all one root cause.

## Result: 23 cases, 17 PASS, **6 HOLES**

A case is a HOLE when the gate did the security-WRONG thing — a
should-be-violation that passed, or a legit input wrongly blocked. All 6
holes are the first kind (should-block, passed). None are false-blocks:
every legitimate input the battery tried was admitted correctly.

## The gate's exact contract (read from code)

check_training_example runs, in order: (V3) recursive ban on
GATE_DECISION_FEATURE_KEYS in `features`; (V4) `label_source` must equal
"post_gate_outcome"; then **`ex_hh is None` returns admissible immediately
(the public/synthetic carve-out)**; (V1) `ex_hh != tgt_hh` → violation
(incl. shared-base direction); (V2) audience set-containment
`tgt_aud - ex_aud` non-empty → violation, with a fail-closed branch when
either roster is None. Everything from V1 down treats caller-supplied
`household_id` and `audience` as GROUND TRUTH.

## The 6 holes, named precisely

**HOLE-1 — provenance forgery (household).** [case a1] An example whose
signal truly came from H2, stamped `household_id=H1`, trained into H1's
model → gate returns admissible. Should be a violation. The gate never
binds the example to a verifiable source; the label is trusted. (This is
D-26's confirmed hole, now reproduced as a passing-should-be-blocking
test.)

**HOLE-2 — provenance forgery (audience/scope).** [case a2] A
member-private (alice-only) signal stamped with the full circle roster
passes scope-containment. Should be a violation. `audience` is
caller-supplied, never derived from the fact's sealed reader set — so the
same forgery that defeats the household axis defeats the scope axis.

**HOLE-3 — provenance omission (absent field).** [case e1] An example that
simply OMITS `household_id` is read as None → routed to the
public/synthetic carve-out → admissible for ANY target. Should be
fail-closed as unprovenanced. Note the asymmetry: a missing `label_source`
fails CLOSED (case e4-family confirms label/audience absence is caught),
but a missing `household_id` fails OPEN.

**HOLE-4 — provenance null (explicit None on real data).** [case e2] Same
as HOLE-3 but with `household_id=None` set explicitly on real household
data → carve-out → admissible. The carve-out cannot tell "genuinely
public" from "household data with the label cleared."

**HOLE-5 — shared-base smuggling (the severe consequence).** [case f3]
Real household data with `household_id` dropped, trained into the SHARED
BASE (household_id=None target) → admissible. This is HOLE-3/4 aimed at
the worst target: the shared base is by definition cross-household, so the
carve-out is a direct data-laundering channel into a model every household
sees. No valid target-household match is even needed — just clear the
label. Arguably worse than HOLE-1 because it requires no matching target.

**HOLE-6 — no live-enrollment binding (roster freshness).** [case h1] A
member who was JUST REVOKED but is still present in the caller-passed
`audience` snapshot is trusted; training a model whose roster still
includes them passes. Should be a violation — REQ_PARTITION_CUSTODY
ratified epoch/rotation so a revoked member gets no new access. The gate
has no `care_team_keys.is_active_caregiver` / epoch binding; it believes
whatever roster snapshot the caller hands it. (case h2, just-ADDED member,
passes/flags by set-containment luck, not by epoch logic — the temporal
dimension is simply absent.)

## The 17 PASS cases (what the gate DOES do right — the real partial)

The relationship logic is sound and worth keeping:
- b. mixed-batch: 99 clean + 1 crossing → the one bad example still flags
  (check_training_batch returns all violations; one poison in 100 goes red).
- c1/c2/c3. intra-household scope: member-private→household-shared FAILS;
  same-scope PASSES; broader→narrower (household signal → member model)
  PASSES.
- d1-d4. three+ households: A→B, B→C, A→C all fail; a four-household pool
  into A flags exactly the 3 foreign examples. Pairwise logic generalizes.
- e3. empty rosters both sides → vacuously admissible (acceptable).
- e4. audience absent (household set) → fail-closed violation.
- e5. example for a household in no roster → cross-household violation.
- e6. audience passed as a STRING → fails closed here (frozenset('a') vs
  frozenset('alice') containment happens to flag) — but see the note: this
  is luck, not a type check; a crafted single-char string could fail open.
  Logged as PASS because this specific input blocked, flagged as fragile.
- f1/f2. carve-out correct direction: genuine public→shared base PASSES;
  household-STAMPED→shared base FAILS.
- g1/g2. order invariance and dedup: stateless purity, no masking.
- h2. just-added member not in source snapshot → flagged.

## Assessment (per dispatch step 5)

**6 holes → the battery did its job; finding them is the success.** Do NOT
fix this pass (dispatch instruction) and do NOT re-MET (already NOT MET
from D-26). The build is a REAL PARTIAL: the relationship math (household
inequality, scope set-containment, batch completeness, shared-base
direction) is correct and standing. What is unbuilt is provenance TRUST.

**Root cause — one, not six.** Every hole is the same defect: the gate
accepts `household_id` and `audience` from the caller and validates only
their RELATIONSHIP to the target, never their AUTHENTICITY or CURRENCY.
Forge them (HOLE-1/2), omit/null them (HOLE-3/4/5), or hand a stale
snapshot (HOLE-6) — all pass.

**Does the fix design change? YES — extend it in two ways beyond what
D-26 named.**
1. D-26's named fix (derive `household_id`/`audience` from the fact's
   sealed record / registry identity / epistemic lineage, not from the
   caller) closes HOLE-1 through HOLE-5. Keep it. Add a forgery fault twin
   (mislabel household, widen roster) AND an omission twin (drop the
   household_id) — both must go red; today's L7:LI1 fixture only tests
   honest labels.
2. NEW, not in D-26: the carve-out must require a POSITIVE, verified
   public/synthetic marker, not mere ABSENCE of a household_id — otherwise
   HOLE-3/4/5 survive even with derivation, because "no provenance" still
   reads as "public." Fail-closed on unprovenanced input.
3. NEW, not in D-26 (HOLE-6): the audience must be bound to CURRENT
   enrollment (care_team_keys.is_active_caregiver / the ratified epoch),
   not a one-time snapshot — deriving from sealed state once is not enough
   if that state can be stale; revocation must be enforced at check time.

**Staging the battery.** eval/test_learner_isolation_adversarial.py is
deterministic (pure function, no graph/model) and is the natural
regression proof: its expected verdicts already encode the
security-correct answers, so the day the gate is fixed, the 6 HOLE rows
flip to PASS and the file asserts 0 holes. Recommend committing it now as
the standing adversarial record (it is TEST code, not production) so it is
not lost — the way this very report was lost before D-26 looked for it.

## Provenance of THIS report

Written to /tmp/d25_isolation_attack.md and existence-proved on disk
(test -f + wc -l) before this session claimed any result. Full raw run in
the session scratchpad (d25_battery.log); reproduce any time with
`.venv/bin/python -m eval.test_learner_isolation_adversarial`.
