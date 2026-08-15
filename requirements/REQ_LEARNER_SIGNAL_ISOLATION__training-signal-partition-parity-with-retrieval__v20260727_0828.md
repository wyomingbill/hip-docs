# REQ_LEARNER_SIGNAL_ISOLATION: Training-Signal Partition Parity With Retrieval
Status: MET (via successor REQ)

## RE-MET 2026-07-30 (D-39) — resolved through REQ_LEARNER_TARGET_AUTHENTICATION

The D-37 pullback below is CLOSED, not open. D-37 filed
`REQ_LEARNER_TARGET_AUTHENTICATION` as this REQ's successor fix spec — the
same relationship D-29's fix spec had to D-30 — and built the target-side
authentication + battery-wiring fix the pullback named as missing. D-38
cleared the `--full` memory block and ran it green. Bill ruled that
successor REQ MET on 2026-07-30 (D-39), and this REQ is MET through it: the
gate this REQ specifies is `harness/learner_isolation.py`, and that module
now authenticates BOTH operands it compares (example side since D-30,
target side since D-37), fails closed on an empty audience on either side,
and is guarded by a 27-case battery that D-37 proved is wired into every
harness pass rather than merely present.

This REQ's own text is left otherwise UNCHANGED below — the pullback
narrative, the three D-36-confirmed findings, and the root-cause analysis
are the accurate history of why the D-31b MET was premature and remain the
record of that. Read them as history, not as a currently-open problem: the
gap they describe is closed. Full build evidence lives in
`REQ_LEARNER_TARGET_AUTHENTICATION__target-side-derivation-and-battery-wiring__v20260730_0851.md`
(MET) and its own D-37/D-38/D-39 history.

## STATUS PULLED BACK 2026-07-30 (D-37) — a 7th hole, and an unenforced battery (RESOLVED, see above)

The D-31b MET (2026-07-29) was PREMATURE and is withdrawn. Not because the
D-30 fix was wrong — it was right, and it holds — but because it fixed one
side of a two-sided comparison, and neither the 23-case battery nor the
`--full` run that earned the MET could see the other side.

An external review (Fable, two independent reviewers, captured verbatim at
`docs/reviews/FABLE_CuratorReview__test-model-and-gate-code-review__v20260730_0801.md`,
D-35) and its verification dispatch
(`docs/dispatches/DISPATCH_D36__verify-fable-curator-findings__v20260730_0851.md`,
D-36) between them establish three findings, ALL THREE CONFIRMED BY
REPRODUCTION against committed code:

1. **7TH HOLE — empty-audience target-side bypass.** `target["audience"] =
   frozenset()` (empty, not `None`) admits EVERY scope in the household,
   member-private included. `harness/learner_isolation.py:286` tests
   `is None`; an empty frozenset is not `None`, so it falls through to the
   set difference at `:292`, where `frozenset() - anything` is empty and
   therefore names no unauthorized readers. Verified live: the same
   member-private example that correctly returns VIOLATION against a normal
   target returns ADMISSIBLE against an empty one, while `None` still fails
   closed.

2. **THE BATTERY THAT GUARDS THIS GATE RUNS IN NO RUNNER.**
   `eval/test_learner_isolation_adversarial.py` is referenced by nothing
   outside its own docstring; `scripts/run_harness.sh:77` executes only
   `eval/harness.py`; the file is absent from `harness_audit._SCENARIO_FILES`
   and from `check_registry`; there is no Makefile, no CI, no pytest config.
   The 23 cases — including the 6 encoding the D-25 holes — can regress
   silently. **A MET resting on a battery nobody runs is resting on a
   document, not a test.** This alone would justify the pull-back.

3. **DYAD AUDIENCE BRANCH READS NON-EXISTENT COLUMNS** (separate REQ, not
   fixed here — see D-37 Part C). `learner_isolation.py:184-187` reads
   `member_a`/`member_b`/`caregiver`/`recipient`; the live `dyads` table has
   `dyad_id`/`recipient_ref`/`household_id`/`dyad_pubkey`/`status`/`created_at`
   — intersection empty. Every dyad-private fact therefore derives
   `audience == frozenset()`, which (with finding 1) is ADMISSIBLE.

### Root cause, named so the next fix does not repeat it

**D-30 authenticated the EXAMPLE side of the comparison and left the TARGET
side caller-supplied.** `target["household_id"]`, `target["audience"]`, and
`target["model_id"]` are read straight from the caller's dict (`:260`,
`:285`) — never derived, never validated, never bound to a real model. That
is precisely the property D-25 found and D-30 removed from the example side.
The gate authenticates one of the two operands it compares.

**Why the discipline did not catch it (Fable's "necessary but not
sufficient" finding).** `harness_audit._COVERAGE_KEYS` is the fixed 4-tuple
`("roles", "scopes", "attribute_splits", "intent_classes")` — every axis is
an axis of the AUTHORIZATION state space. There is no axis for INPUT TRUST.
A coverage entry structurally cannot say "this check assumes its target dict
is honest," so the D-23 entry named an unfixtured roster slice, scored the
honest maximum available to it, and still could not surface the actual gap.
The four-part standard was satisfied, not violated, by a check that was
six-ways — now seven-ways — broken.

Re-earning MET required, at minimum: the target side authenticated, the
empty-audience case failing closed, the battery WIRED so it runs every pass,
all cases green under that wiring, and `--full` green. Successor REQ (MET,
D-39):
`REQ_LEARNER_TARGET_AUTHENTICATION__target-side-derivation-and-battery-wiring__v20260730_0851.md`.
**All of the above is now done — see the RE-MET block at the top of this
document.**

Prior rulings retained below for the record.

MET-Ruling (WITHDRAWN by D-37, above): Bill, 2026-07-29 (D-31b dispatch) — the provenance-authenticity
fix (D-30) passed the --full house bar on a clean-memory window (D-31): all
4 ABSOLUTE checks green (G0/PSA1/CTX-STRIP/LI1), LI1 13 sub-checks pass,
RATCHET PASS exit 0, and the 23-case adversarial battery all real PASS (the
6 D-25 holes closed, zero xfail remaining). GRANTED WITH ONE NAMED LIMIT
(disclosed in the coverage entry): the production RegistryProvenanceResolver
FAILS CLOSED on member-owned facts until enrollment populates
members.household_id — a DATA prerequisite, not a logic defect. The gate
logic is proven (fixture battery + L7:LI1); member-scoped training is safely
REJECTED (never leaked) until the column is populated. See the D-31b block
and the D-26/D-28/D-29/D-30 history below. Prior rulings retained for the
record:
MET-Ruling (SUPERSEDED by D-26): Bill, 2026-07-29 (D-23b dispatch) -- the Stage-1 isolation gate
is MET: L7:LI1 green on the two-household fixture, both fault twins red
naming their crossing (cross-household pooling incl. shared-base direction;
intra-household scope crossing naming unauthorized readers), L7 26/26 +
AUDIT 8/8 (four-part-roster 58 checks, zero new gaps) + RATCHET PASS,
exit 0 (D-23 run, commit 487b38b). Basis: the check is deterministic --
no model call, no graph dependency -- so layer-7 is its full test surface;
--full not required for it, same basis as the strip-context MET ruling
(D-20). The gate remains STANDING: it predates any learner, and the first
commit introducing learner code meets it on its first --layer 7. OQ 1-3
remain open; OQ4 answered by the D-23 rulings
Branch: roadmap
Reconciled-Against: HIP_ContextArch_Reconciliation__master-plan-diff__v20260726_0710.md
STEP 4 (why this REQ exists, verbatim source of the gate); REQ_G0_OUTPUT_INVARIANT__
output-side-fabrication-backstop__v20260726_0735.md (MET — precondition (i) of three);
REQ_PROMPT_RECORD_FIDELITY__factid-set-parity-prompt-vs-admitted__v20260726_1717.md
(MET 2026-07-27 — precondition (ii) of three); REQ_HARNESS_DISCIPLINE__four-part-check-
standard-and-sprint-gate__v20260726_0827.md (MET — the four-part standard this REQ's
acceptance test is drawn from); this session's read-only trace of
harness/injection_contract.py, harness/dyad_registry.py, eval/harnesslib/
layer7_crypto_v2.py (RI1), no code touched, no harness run for this filing.
D-28/D-29 (2026-07-29) additionally reconciled against a read-only trace of
memory_engine/store.py, harness/member_registry.py, harness/care_team_keys.py,
harness/household_keys.py, harness/write_rule.py, harness/partition_crypto.py,
and the D-27-committed eval/test_learner_isolation_adversarial.py (b39c539) —
no code touched, no harness run for this filing either.

## UPDATE 2026-07-29 (D-23, Bill's rulings + Curator Stage 1 build)

Bill ruled, and this update encodes as the law this REQ's check now
enforces (the gate is BUILT as of this update; assessment staged for Bill,
not self-marked MET):

1. **STRICT isolation, provenance-carried.** Every learner training
   example carries household provenance. The check FAILS if a training
   example's household provenance is not the single household the target
   model serves. No cross-household pooling of household-sourced data,
   ever. A shared base model may exist ONLY if trained on public/
   synthetic/centrally-authored data with NO household provenance — that
   path is allowed; a household-sourced example crossing into any other
   household's model, or into the shared base, is the violation.
2. **Intra-household scope crossing is the SAME violation class** — this
   ANSWERS open question 4 below (Bill's "or scopes" clause confirmed): a
   training example whose signal originates from a member-private scope
   must not train a broader-scope (household-shared) model. Audiences are
   ROSTERS (explicit member-id sets, RI1 discipline), and the test is set
   containment: every reader of the target model must be authorized for
   the example's source scope. Broader-into-narrower is admissible.
3. **Check shape as ruled:** ABSOLUTE-tier, layer-7, two-household
   fixture, PLUS a fault-injection twin that pools across households
   (red, naming the crossing) AND a second twin that crosses scopes
   intra-household (also red, naming the unauthorized readers).
4. **Gate decisions structurally excluded; labels post-gate only.** INJ
   outcomes/deny reasons/guard flags are banned from any future feature
   space by key vocabulary (recursive), and label_source must be the
   literal "post_gate_outcome".

**What was built (Curator Stage 1 — the gate, NOT a learner):**
`harness/learner_isolation.py` — the enforcement surface a future learner
MUST route every training example through (check_training_example /
check_training_batch, GATE_DECISION_FEATURE_KEYS, POST_GATE_LABEL); pure
provenance validator, no graph, no model, violation strings that NAME the
crossing. `L7:LI1` scenario (ABSOLUTE tier, eval/harnesslib/
layer7_crypto.py, joins G0/PSA1/CTX-STRIP in the absolute_keys gate):
clean two-household fixture (hh-alpha = the alice/bob/mary rosters,
hh-beta = dana/eli, disjoint) green; pooling twin red naming example +
both households, green on removal; intra-household scope twin red naming
unauthorized readers, green against the member's own model; feature-key
and label-provenance probes red; metamorphic property (verdict invariant
under query rewording) checked in-scenario AND as executable audit probe
`li1_query_reword` (eval/harnesslib/harness_audit.py). Registered in
check_registry.py as L7:LI1 with all four artifacts, coverage naming its
unfixtured slice honestly (pair/care-team rosters reduce to the same
set-containment test; named for the first real learner build).

The check was built with NO learner existing — the gate predates the
learner, per this REQ's own standing-refusal-gate design. Open questions
1-3 below remain open (OQ4 is answered by ruling 2). Status stays NOT MET
pending Bill's MET assessment against the acceptance test (run evidence in
DISPATCH_D23).

## UPDATE 2026-07-29 (D-26 — MET PULLED BACK: gate trusts unvalidated provenance)

The D-23b MET is withdrawn. Status returns to NOT MET. The Stage-1 gate
and its L7:LI1 check are a real partial and are NOT deleted — the pullback
corrects the STATUS to the truth, it does not undo the build.

**Why:** the gate stops honest MISLABELING but not FORGED provenance,
which is the actual isolation threat. Confirmed directly from the built
code this pass (harness/learner_isolation.py), independent of the
adversarial report:

- **HOLE — provenance forgery (confirmed from code).** check_training_
  example reads `ex_hh = example.get("household_id")` (line 132) and
  `ex_aud = example.get("audience")` (line 156) as GROUND TRUTH. It
  validates the RELATIONSHIP between the declared provenance and the
  target (cross-household, shared-base, scope-containment), but never
  whether the declared `household_id`/`audience` is REAL. A caller that
  labels an hh-beta-sourced example `household_id="hh-alpha"` (or widens
  its `audience` roster) passes the gate clean — the forged label is the
  crossing, and the gate cannot see it. Nothing in the module ties a
  training example back to a verifiable source: zero references to the
  fact registry, a signature, a fact_id, or the epistemic record (grep
  confirmed). The two-household fixture and both fault twins in L7:LI1
  only ever exercise HONESTLY-labelled examples, so a green LI1 proves
  the relationship logic, not that provenance is trustworthy — which is
  exactly the gap that made "provably isolated" premature.

**Provenance of this pullback, stated honestly:** the dispatch (D-26)
cited an adversarial-test report at `/tmp/d25_isolation_attack.md`. That
file was NOT present at the named path, and no d25/isolation/attack file
exists anywhere in /tmp this session. This block therefore records ONLY
the hole the dispatch text itself named (provenance forgery) AND that I
independently re-confirmed against the code — it does NOT enumerate other
holes the D-25 battery may have found, because that report could not be
read and its findings must not be invented. If the D-25 report surfaces,
its remaining holes should be appended here before any re-MET.

**What MET now additionally requires (beyond the D-23b criteria):** the
gate must bind each training example's provenance to a source it cannot
forge — the fact's own sealed record / registry identity / epistemic-
record lineage — so that `household_id` and `audience` are DERIVED from
verified state, not accepted from the caller. The acceptance test needs a
fault twin that FORGES provenance (mislabels an example's household or
widens its roster) and must go red; today's fixture only tests honest
labels. Until that exists and is green, this REQ is NOT MET.

## UPDATE 2026-07-29 (D-28/D-29 — provenance-authenticity fix specified; REQ only, no code)

D-25's adversarial battery (report at `/tmp/d25_isolation_attack.md`)
re-proved D-26's hole from code AND found five more, all one root cause:
the gate validates the RELATIONSHIP between caller-supplied
`household_id`/`audience` and the target, but never their AUTHENTICITY (is
this the real household?) or CURRENCY (is this roster still current?).
D-27 committed the battery as a standing `xfail(strict=True)` regression
(`b39c539`, `eval/test_learner_isolation_adversarial.py`) so the 6 holes
cannot silently regress further and the fix proves itself the moment they
flip to PASS. D-28 traced, read-only, which of the fix's required
primitives already exist in this codebase vs. must be built. This update
specifies the fix from that trace; no code changes in this filing.

**The 6 holes and what the fix binds to:**

- **HOLE-1** (provenance forgery, household) and **HOLE-3/HOLE-4**
  (omission / explicit-None household_id routed to the public carve-out):
  derive `household_id` from a chain the caller cannot forge, never accept
  it as a field on the incoming example dict.
  - A training example must carry the real Neo4j `fact_id` it was derived
    from — server-generated, `memory_engine/store.py:496`
    (`new_fact_id = str(uuid.uuid4())`), never caller input.
  - The Fact node itself has no `household_id` property
    (`memory_engine/store.py:149-224`, `_new_node_props`/`_CREATE_FACT_CQL`)
    — it must be derived from the fact's `owner` field via
    `harness/member_registry.py:203 get_member_by_id(owner)["household_id"]`
    (SQLite `members.household_id`, column at `member_registry.py:62`).
  - Fail-closed default: if a fact_id does not resolve through this chain
    to a real household_id, the example is UNPROVENANCED and REJECTED, for
    every target including household-matched ones — not routed to the
    carve-out. This closes HOLE-3/HOLE-4 as a behavior change on top of the
    same chain, no new lookup required.

- **HOLE-2** (provenance forgery, audience/scope): derive `audience` from
  the fact's actual sealed-reader set, dispatched by the fact's visibility
  class — already computed at write time (`harness/write_rule.py`
  `CLASS_CARE_TEAM`/`CLASS_HOUSEHOLD`/`CLASS_DYAD`/`CLASS_MEMBER`, imported
  by `harness/partition_crypto.py`) — never accept `audience` as a caller
  field.

- **HOLE-6** (no live-enrollment binding): bind audience to LIVE roster
  state at check time, not a caller-passed snapshot — the exact pattern
  `harness/injection_contract.py:515-517` already uses live for a
  different gate (INJ-3):
  - Care-team-private axis: `harness/care_team_keys.py:141
    is_active_caregiver()` / `:127 list_caregivers()` (SQLite
    `care_team_members`, `removed_at IS NULL`).
  - Household-circle axis: `harness/household_keys.py:192
    is_circle_member()` / `:169 list_circle_members()` (SQLite
    `household_circle_members`, `removed_at IS NULL`).
  - CAVEAT (D-28): do NOT bind to `household_key_wraps` (the crypto wrap
    table) as the currency source — by that module's own docstring, wraps
    are NOT stripped on removal (full quorum-gated eviction is
    REQ_PARTITION_CUSTODY #6, unbuilt). The roster tables above are the
    live-currency source; the wrap tables lag and would silently
    reintroduce HOLE-6.

- **HOLE-5** (shared-base smuggling, the severe one — no target match
  needed, just clear the label): the public/synthetic carve-out must FAIL
  CLOSED on a POSITIVE, verified marker, never on mere absence of
  household_id. D-28 confirmed no such marker exists anywhere in the Fact
  node schema or codebase today (searched for is_public/is_synthetic/
  public_marker/any positive classification field — none found;
  "public/synthetic" appears only in comments, docstrings, and
  eval-fixture naming). This is new surface, not a rewire: a Fact-node
  property set at write time by whatever process authors central/synthetic
  content, verified — not inferred — by the gate. Until it exists, the
  shared base must refuse ALL examples that do not carry it.

**Acceptance test:** the 6 `pytest.mark.xfail(strict=True)` cases already
committed in `eval/test_learner_isolation_adversarial.py` (D-27, `b39c539`)
ARE the acceptance test — `a1` (HOLE-1), `a2` (HOLE-2), `e1` (HOLE-3), `e2`
(HOLE-4), `f3` (HOLE-5), `h1` (HOLE-6). Each already asserts the
SECURITY-CORRECT verdict; `strict=True` means an unexpected PASS is a hard
failure today, so the fix is done when, and only when, all 6 flip from
XFAIL to PASS and their `hole=` markers are removed from the `CASES` table
— not before, and not partially. The 17 non-hole cases in the same file
(cross-household pooling, intra-household scope containment, mixed-batch,
three+ households, carve-out directionality, order invariance/dedup) must
stay green throughout — this fix must not regress the relationship math
D-25 already confirmed sound.

Per REQ_HARNESS_DISCIPLINE, MET additionally requires the full Four for
this fix's own check, not only re-use of the base gate's existing four:

1. **FAULT-INJECTION TWIN** — already built: the 6 xfail cases above ARE
   the twin (each names its hole, each must go red-to-green on the fix).
2. **GROUND-TRUTH FIXTURE** — human-verified: the two-household
   (hh-alpha/hh-beta) fixture already in
   `eval/test_learner_isolation_adversarial.py`, plus L7:LI1's own
   alice/bob/mary fixture; extend only if the fix's new lookups (fact_id
   resolution, live roster calls) need cases the current fixture doesn't
   cover (e.g., an unresolvable fact_id, a caregiver revoked mid-test).
3. **COVERAGE ENTRY** — `check_registry.py`'s existing L7:LI1 entry must be
   updated to name the new region tested: provenance AUTHENTICITY
   (fact_id→owner→registry resolution) and CURRENCY (live roster binding),
   as distinct from the RELATIONSHIP slice it already declares — any
   region still untested (e.g., dyad-private audience derivation, if not
   covered) must be named honestly, not silently folded into an existing
   row.
4. **METAMORPHIC WRAPPER** — the existing in-scenario property (verdict
   invariant under query rewording) and the `li1_query_reword` audit probe
   cover this already; confirm it still holds once the gate reads
   registry/roster state instead of pure caller input (the property is
   about query wording, not about where provenance comes from, so it
   should be unaffected — verify, don't assume it carries over for free).
5. **RATCHET PASS** on `--full` before and after (Requirements Discipline
   item 12). This fix adds live SQLite reads to a check that
   `harness/learner_isolation.py`'s own docstring currently describes as
   pure ("never reads the graph, never calls a model") — that docstring
   claim must be corrected honestly (now reads the registry/roster tables,
   still never calls a model), and `--full` timing confirmed unaffected.

Status stays NOT MET. This filing specifies the fix; it does not build it.

## UPDATE 2026-07-29 (D-30 — provenance-authenticity fix BUILT; staged for Bill, NOT self-MET)

The D-28/D-29 fix spec above is now built. Status stays NOT MET pending
Bill's MET ruling (and the --full house bar, deferred — see below).

**Built (`harness/learner_isolation.py`, production code):** the gate no
longer accepts `household_id`/`audience` from the caller. An example carries
a server-generated `fact_id`; the gate DERIVES provenance via an injectable
`ProvenanceResolver`. Production `RegistryProvenanceResolver` reads the
un-forgeable chain — fact `owner` -> `member_registry.household_id` (or the
household axis for owner=='household'); audience from the fact's visibility
class -> LIVE roster (`care_team_keys.list_caregivers` /
`household_keys.list_circle_members`, both `removed_at IS NULL`); a POSITIVE
`provenance_class=='public'` marker (absent in schema today -> carve-out
fails closed). Unprovenanced (missing/unresolvable fact_id) -> rejected,
never carve-out.

**All 6 D-25 holes closed, proven:** `eval/test_learner_isolation_adversarial.py`
rewritten to the new contract with a fixture resolver — all 23 cases now
run as REAL PASS (the 6 xfail markers REMOVED). L7:LI1 extended with two new
fault twins (AUTHENTICITY: a forged stamp is ignored, the true foreign
household is derived and flagged; CURRENCY: a revoked member gone from the
LIVE roster makes a model still listing her a crossing) plus
missing/unresolvable-fact_id fail-closed checks. `--layer 7`: L7 26/26,
AUDIT 8/8, four-part-roster PASS (58 checks, 0 new gaps), RATCHET PASS.

**Discipline Four (per REQ_HARNESS_DISCIPLINE), status:** (1) fault twins —
built, red/green both directions, incl. the two new D-30 twins; (2)
ground-truth fixture — two-household + fixture resolver, human-verified; (3)
coverage entry — L7:LI1 registry updated naming AUTHENTICITY + CURRENCY, and
honestly naming the still-uncovered slice; (4) metamorphic — in-scenario +
`li1_query_reword` audit probe, both updated to the resolver contract, both
green.

**Two honest items that keep this NOT MET until Bill rules:**
1. `--full` NOT run (memory ~80MB free, below TD-129's OOM threshold — a
   run now would SIGKILL, a false failure). REQ acceptance item 5 wants
   `--full` before/after; deferred to a clean memory window. The change is
   a pure-function gate + test wiring (no live turn path touched), so a
   regression outside L7 is unlikely, but this is unverified, stated plainly.
2. Live smoke of `RegistryProvenanceResolver` against graph 7688 (read-only)
   confirmed the chain resolves correctly for `owner=='household'` facts
   (household + live circle audience) and fails closed for a fake fact_id —
   BUT member-owned facts (owner=maya/sam) resolve to household=None because
   the demo `members.household_id` column is not populated on this graph. It
   fails CLOSED (safe: member facts reject, never leak), but the production
   resolver cannot admit legitimate member-scoped training until enrollment
   populates household_id. That is a DATA prerequisite, not a gate-logic
   defect — the gate logic is proven by the fixture battery and L7:LI1. The
   coverage entry names live-graph resolver reads as an uncovered slice.

The 6 D-25 holes are closed at the LOGIC level and cannot silently regress
(the battery + L7:LI1 twins fail loudly). MET is Bill's call on the two
items above.

## UPDATE 2026-07-29 (D-31b — MET granted by Bill, with a named data limit)

Bill rules the isolation gate MET. Evidence and the disclosed limit:

**--full verification (D-31, clean-memory window after reclaiming the
duplicated qwen2.5:7b across both Ollama daemons):**
- L1 15/15, L2 25/35 (10 skip), L3 3/3, L4 27/31 (4 skip), L6 1/1,
  L7 26/26, L7V2 27/28 (1 skip), SCHEMA 1/1, VOICE 1/1, AUDIT 8/8;
  RATCHET PASS — no scenario regressed vs baseline; exit 0, no SIGKILL.
- All 4 ABSOLUTE checks green: G0, PSA1, CTX-STRIP, LI1.
- LI1: 13 sub-checks pass, including the D-30 twins proven live —
  forged household_id stamp IGNORED (gate derives true H2 from the
  fact_id and flags it); revoked member gone from the LIVE roster ->
  crossing; household-sourced example refused from the shared base
  (verified-public only); missing + unresolvable fact_id both rejected
  fail-closed.
- `eval/test_learner_isolation_adversarial.py`: 23/23 real PASS, the 6
  former-hole cases closed, zero xfail markers remaining.
- This clears D-30's honesty item 1 (`--full` deferred). The change
  touches no live turn-path code; RATCHET PASS confirms no collateral
  regression.

**NAMED LIMIT (Bill's ruling — MET is granted WITH this disclosed):** the
production `RegistryProvenanceResolver` resolves `owner=='household'` facts
correctly (household + live circle audience) and fails closed on an
unresolvable fact_id, but MEMBER-OWNED facts (owner=maya/sam) resolve to
household=None because `members.household_id` is not populated on the dev
graph. Consequence: the production resolver FAILS CLOSED on member facts —
member-scoped training is safely REJECTED, never leaked — until enrollment
populates that column. This is a DATA prerequisite, not a gate-logic
defect: the gate logic is proven by the fixture battery and L7:LI1, and the
fail-closed direction is the safe one. It is disclosed in the L7:LI1
coverage entry (`check_registry.py`) as a named uncovered slice
(live-graph resolver reads), not folded silently into a covered row.

**REQ_HARNESS_DISCIPLINE Four — all met for this fix:**
1. FAULT-INJECTION TWINS — the 23-case battery (6 former holes now pass)
   + L7:LI1's inline twins (pool, scope, forgery, revocation), each
   red-on-command / green-on-removal.
2. GROUND-TRUTH FIXTURE — the two-household (hh-alpha/hh-beta) fixture +
   the FixtureResolver ground truth, human-verified, no model grading.
3. COVERAGE ENTRY — L7:LI1's `check_registry.py` entry names the new
   AUTHENTICITY (fact_id->owner->registry derivation) and CURRENCY (live
   roster binding) regions, AND names the still-uncovered slice
   (dyad-private audience derivation; live-graph resolver reads / the
   members.household_id data prerequisite) honestly.
4. METAMORPHIC WRAPPER — the in-scenario property + the `li1_query_reword`
   audit probe, both updated to the resolver contract, both green on
   `--full`.

Status: MET. The three ContextArch preconditions (G0, prompt-fidelity,
learner-signal isolation) are now all MET — the gate to the Curator's
learning track is built, proven, standing, and closed until a learner
comes to meet it (with the member.household_id data prerequisite named for
whoever builds that learner).

## THE REQUIREMENT

Bill's own words, verbatim:

> A learner that ranks context must never train on, or be able to read, anything
> the requesting identity was not authorized to see. Training signal is subject
> to the same partition as retrieval. A ranker that learns across households or
> scopes is a leak with a delay.

Expanded, in HIP_ContextArch_Reconciliation STEP 4's own words (the reconciliation
that names this precondition): the ratified law is "confidence... may never create
permission" (REQ_CONFIDENCE_DISCIPLINE) and audience is "decided only by
deterministic facts" (REQ_PARTITION_CUSTODY) — restated by the Context & Interaction
Intelligence proposal's own §8 rule, quoted directly in STEP 4: **"The learning
system must never be permitted to optimize authorization policy."** STEP 4 names
this as gap 3 of three, in its own words:

> Training-signal isolation exists nowhere. The proposal's own rule... has no
> mechanism: nothing yet guarantees a learner's reward is computed only on
> post-gate outcomes, that gate decisions are excluded from its feature/gradient
> space, or that household personalization weights cannot reach gate inputs.

And table row 6 (P4b), the same STEP's own framing of what must be ratified before
any learned ranker ships, precondition (iii) verbatim: **"ranker placed so it can
only NARROW the authorized candidate set, never source outside it."** STEP 4's
bottom line collapses G0 + the prompt⊆admitted invariant + this gap into "three
builds" required before "adopting the learned Context Manager is safe" — this REQ
is the third, filed because STEP 4 itself says "no REQ exists — needs one."

Both STEP 4 quotes above describe the SAME failure mode Bill's words name: a
learner is not a retrieval-time gate, it is a persistent artifact (weights,
gradients, a reward history) that can smuggle an unauthorized fact across a
boundary — household, scope, or identity — long after the turn that leaked it is
gone. Retrieval enforces the partition per-turn, structurally, via
`apply_injection_contract` (INJ-1..7) and owner-scoped Cypher reads. A learner
that is ever trained on pooled signal from more than one identity/household/scope
without each one being mutually authorized for the others' contributed facts
re-opens that same boundary with no per-turn gate to catch it — "a leak with a
delay," in Bill's words, because the leak surfaces in a later turn's ranking
behavior, not in the training step that caused it.

## THE ACCEPTANCE TEST

Pass/fail, per item. Any single failure is FAIL; no partial credit. Per STEP 4,
no learner exists yet in this codebase — this REQ's check is therefore a STANDING
REFUSAL gate, wired now, so that the FIRST commit introducing any learner-training
code path is checked against it on its very first `--full`, not retrofitted later.

1. An ABSOLUTE-tier, hard-zero layer-7 check, `--accept` mechanically refused via
   the same `layer7_crypto_v2.py` mechanism G0/PSA1 use, wired unconditionally into
   `eval/harnesslib/layer7_crypto.py` `run()` (auto-run on every `--layer 7`/
   `--full`, no hand-run step).
2. The check asserts: for any code path that constructs a learner's training
   signal (features, reward, gradient batch, replay buffer, or ranking-weight
   update) from more than one requesting identity's admitted facts, every
   identity contributing to that signal must be independently, mutually
   authorized for every fact any other contributing identity supplied — under
   the SAME four scopes retrieval already enforces (pair-private /
   care-team-private / household-circle-shared / member-private, per RI1,
   `eval/harnesslib/layer7_crypto_v2.py`'s roster-invariant scenario). Equivalently,
   per STEP 4 gap 3: gate decisions (INJ-1..7 outcomes, deny reasons) must be
   structurally excluded from the learner's own feature/gradient space — a reward
   signal may be computed only on POST-gate outcomes, never on which gate fired
   or why.
3. FAULT-INJECTION TWIN: a probe constructs a synthetic training-signal path that
   pools admitted facts from two disjoint households (or two disjoint scopes
   within one household) into a single gradient/reward computation; the check
   turns red on command, naming the identities/scope that crossed. Removing the
   cross-boundary pooling turns it green. Both directions must hold or the metric
   FAILs (REQ_HARNESS_DISCIPLINE standard #1).
4. GROUND-TRUTH FIXTURE: human-verified, not model-graded — extend the existing
   alice/bob/mary four-scope fixture with a second household (or a second
   disjoint scope) whose admitted sets are independently verified disjoint from
   the first. The oracle for "does this training example ever contain another
   identity's authorized-only fact" is this verified fixture (REQ_HARNESS_DISCIPLINE
   standard #2).
5. COVERAGE ENTRY: the check declares which slice of the training-signal state
   space it covers — which scope pairs (pair-private × care-team-private ×
   household-circle-shared × member-private) and which household-boundary
   crossings are exercised — registered in `check_registry.py` the same way every
   other check's four-part declaration is tracked (REQ_HARNESS_DISCIPLINE
   standard #3).
6. METAMORPHIC WRAPPER: meaning-preserving rewordings of the query/context that
   produced a given training example do not change the isolation verdict (same
   pattern as MT1/MT2; REQ_HARNESS_DISCIPLINE standard #4).
7. RATCHET PASS on `--full` before and after, any pre-existing failures named as
   pre-existing (Requirements Discipline item 12).

## WHAT'S ALREADY DONE (do not redo)

- **Precondition (i), G0, is built and MET** (`REQ_G0_OUTPUT_INVARIANT`,
  `44e3626`/`44ff3d3`) — the output-side backstop and the ABSOLUTE-tier wiring
  pattern this REQ's check copies.
- **Precondition (ii), the prompt⊆admitted invariant, is built and MET**
  (`REQ_PROMPT_RECORD_FIDELITY`, MET 2026-07-27, PSA1 wired ABSOLUTE-tier
  into `layer7_crypto.py run()`) — this REQ does not re-scope it; it is the
  sibling precondition, not this one.
- **REQ_HARNESS_DISCIPLINE is MET** and its four-part standard is exactly where
  acceptance items 3-6 above come from — do not invent a different quality bar.
- **The partition retrieval already enforces exists and is built.** Four scopes
  as explicit key-wrap rosters, never a label (RI1, `eval/harnesslib/
  layer7_crypto_v2.py`); `apply_injection_contract` (INJ-1..7,
  `harness/injection_contract.py`) runs the deterministic authorization gate
  downstream of any ranking, before any fact text reaches the model
  (`harness/orchestrator.py:517-524` per STEP 4's own citation). This is the
  partition this REQ's check measures a future learner's training signal
  against — this REQ does not build or change that partition.
- **No learner, ranker, training pipeline, reward computation, or gradient path
  exists anywhere in this codebase today.** Verified this session: no module
  named ranker/learner/reward/gradient exists under `harness/`, `eval/`,
  `server/`, or `memory_engine/`. This REQ's check is therefore, today, a
  standing gate with nothing yet to fire against — its job is to exist BEFORE
  a learner is proposed, not to prove one is currently safe.

## WHAT'S KNOWN BROKEN

- **Nothing enforces this today because nothing needs to yet — but "nothing
  needs to yet" is exactly the state STEP 4 warns will end silently.** Per
  STEP 4: "nothing yet guarantees a learner's reward is computed only on
  post-gate outcomes, that gate decisions are excluded from its
  feature/gradient space, or that household personalization weights cannot
  reach gate inputs." If a learner lands before this check exists and is wired,
  it lands unchecked.
- **The mechanism this REQ's check would use has no analog yet.** G0 and
  REQ_PROMPT_RECORD_FIDELITY's check both have a concrete object to compare
  today (a reply string; an assembled prompt) against a concrete oracle
  (`resolved_subjects`/`admitted[]`; `record.admitted[]`). A training-signal
  isolation check has no learner's training loop to instrument yet — this
  REQ's acceptance test (item 2) specifies the PROPERTY the check must hold
  once one exists; the concrete instrumentation points (which function
  constructs a gradient batch, where a reward is computed) cannot be named
  until STEP 4's row 16 decision (whether to adopt a learned-ranker track at
  all) is made. See OPEN QUESTIONS.
- **Personalization weights are a second, adjacent vector STEP 4 names but does
  not resolve.** "household personalization weights cannot reach gate inputs" —
  P8 (table row 13, lightweight per-household personalization) is a CONSISTENT
  EXTENSION already, independent of any learned ranker; this REQ's check must
  also cover personalization weights specifically, not only a ranker's own
  training signal, per STEP 4's own parenthetical. Not yet instrumented for the
  same reason as above: no personalization-weight mechanism is built.

## CONSTRAINTS

- Do not change any existing check's pass/fail behavior.
- Do not touch the demo on main or graph 7689.
- Layer 7, AUDIT, and full RATCHET stay green — before and after.
- Hard zero, never `--accept`-able, matching G0/G1/G4/REQ_PROMPT_SUBSET_ADMITTED's
  own never-baseline set (REQ_CONFIDENCE_DISCIPLINE Phase G taxonomy) — a build
  that ships a learner behind a flag, an acceptable baseline, or an exemption for
  this check has not built this REQ.
- This REQ does NOT authorize building a learned ranker. It defines what must be
  true before one could ship (STEP 4's own framing: "adopting the learned Context
  Manager is safe only behind three builds"). Whether to build one at all is
  STEP 2 row 16's own NEW DECISION REQUIRED, Bill's to make, not this REQ's.
- No new model calls in the check itself: like PSA1, this is a deterministic
  structural/set comparison (which identities' facts contributed to which
  training example), not a model judgment call.

## OPEN QUESTIONS FOR BILL

HIP_ContextArch_Reconciliation does not settle these; they are not decided here:

1. **Does this REQ also own row 6(iii)'s "narrow only, never source outside"
   property, or is that fully precondition (ii)'s (REQ_PROMPT_RECORD_FIDELITY)
   territory?** Row 6(iii) is about what candidates a ranker may SOURCE at
   inference time (retrieval-time candidate boundary); Bill's words for this
   REQ are about what a learner may TRAIN ON / READ (training-time signal
   boundary). STEP 4's bottom line folds both into "three builds," but the two
   properties could be proven by two different mechanisms at two different
   points in the pipeline. This REQ's acceptance test scopes training signal
   only (per Bill's words) — confirm whether row 6(iii) needs its own REQ or
   folds into REQ_PROMPT_RECORD_FIDELITY's existing scope.
2. **Row 31's training-record crypto class, retention, and identity form is an
   explicit NEW DECISION REQUIRED in STEP 2/4, not decided by this REQ.** STEP 4:
   "the §20 training record... would persist decrypted content and household_id
   outside member sealing — colliding with operator-blind-at-rest and
   HEL-ACTOR-1 unless sealed and opaque-ID'd." If any training-record persistence
   is ever built, does it need its own REQ (sealing scheme, retention window,
   opaque-ID form per HEL-ACTOR-1), separate from this REQ's isolation check? This
   REQ's check as scoped tests WHETHER cross-identity pooling happened, not HOW
   any resulting record is stored at rest.
3. **Row 16 itself — adopt the learned-ranker track at all, or hold retrieval
   rule-based (Generation 1-2 only)?** This REQ is written to be true either way
   (a gate that holds vacuously with no learner is still a real, checked gate),
   but the concrete instrumentation points named in WHAT'S KNOWN BROKEN cannot be
   finalized until this decision is made — naming a function to instrument
   before the function's design exists would be inventing scope this REQ was
   told not to invent.
4. **Does "learns across households or scopes" (Bill's words) include a SINGLE
   household's own member-private facts pooling into that same household's
   shared-scope training signal** (e.g., ray's member-private facts leaking into
   a ranker trained to serve the household-circle-shared scope for the SAME
   household), or is the boundary strictly cross-household? The four ratified
   scopes (RI1) already separate member-private from household-circle-shared
   WITHIN one household — STEP 4 does not say whether intra-household
   cross-scope pooling is the SAME violation class as cross-household pooling,
   or a lesser one. This REQ's acceptance item 2 currently treats both the same
   (any scope crossing, not only household crossing) per Bill's own "or scopes"
   clause — confirm this reading is correct.

## WHY THIS REQ EXISTS

It is precondition (iii) of three for the context-architecture learned ranker,
per `HIP_ContextArch_Reconciliation` STEP 4. Precondition (i) is G0, MET.
Precondition (ii) is `REQ_PROMPT_RECORD_FIDELITY`, MET 2026-07-27. STEP 4's
own bottom line: "Adopting the learned
Context Manager is safe only behind three builds: G0..., a prompt⊆admitted
layer-7 invariant..., and learner/training isolation (no REQ exists — needs
one)." This is that REQ.
