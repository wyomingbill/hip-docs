# DISPATCH_SITUATION_IDENTITY — the four kinds, canonical situation identity, and the manifest check

Status: BUILT
Reconciled-Against: roadmap `9bc1417` (pre-build HEAD). **LANDED AT `923bf44`** — backfilled by the immediately following commit, because a commit cannot contain its own hash.

**HA-03** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD (code)**
**GOVERNING REQ:** `REQ_OFFER_MECHANISM__governed-initiation-of-new-authority__v20260806_1625.md`
(the current version, amended at HA-02), **§12 LANDING ORDER step 2 ONLY** — "Make
trigger-registry decision and canonical `situation_id` mandatory for offer creation."
**NOTHING RULED MET.**

## 1. CHECK FIRST — is HA-01's finding still true? (yes)

**No representation of the four material-change kinds exists in code.** Re-verified this
dispatch, not inherited: a sweep for `material_change`, `change_kind`, `care_function`,
`care_plan`, `legal_role`, `sensing_contract`, `material_circumstance` finds

- `material_circumstance_version` as an **unvalidated free-text string field** on
  `harness/purpose_trigger.py::PurposeTrigger` and in `harness/offer_gate.py`'s dedup key;
- `care_plan` as an ordinary FACT ATTRIBUTE in `harness/extraction_queue.py` and
  `harness/representation_class.py` — a different concept entirely;
- nothing else.

`harness/offer_gate.py`'s own docstring already recorded each of the four as "NO
mechanism". **That still holds, and this dispatch does not invent the mechanisms** — it
builds the *identity* layer over events a registry would emit, which is what step 2 asks
for. See §6 for what stays absent.

## 2. THE DERIVATION (item 2), auditable

`harness/material_change.py`. `situation_id` is a SHA-256 over a canonical JSON array of
exactly five components, and **nothing else reaches the hash**:

```
["hip.situation.v1", kind.value, principal, source_authority, event_ref, [[k,v],…]]
```

Worked example, printed from the shipped code:

```
canonical payload: ["hip.situation.v1","clinician_care_plan","maya","clinic-emr-7",
                    "careplan-2026-08-06-0001",[["author_role","clinician"],["plan_version","3"]]]
situation_id     : sit:313360f6997d1cb0ead7e62e260467f4
```

- **`principal` / `source_authority` / `event_ref` are the registered event identity.**
  All three are required; a blank one is refused, because a situation with no event
  identity is not canonical, it is a guess.
- **Every string is normalized `strip().casefold()`, and `material_state` is sorted by
  key.** That normalization is precisely what makes R6's "semantically equivalent operator
  submissions" resolve together — the same world event described twice is one situation.
- **The domain tag `hip.situation.v1` is INSIDE the hash**, so a future deliberate change
  to the derivation is a visible version bump rather than a silent re-identification of
  every historical situation.

**§2.3's prohibition is structural, not a convention.** `RegisteredEvent` has **no field**
for model wording, prompt text, session identity, or an operator label — there is nothing
to pass. And because a dict is an open door, `material_state` refuses those keys too
(`_PROVENANCE_KEYS`) along with every R5 non-trigger. **A thing that cannot change the
world cannot change the identity.**

## 3. THE FOUR KINDS (item 1), and a discrepancy that needs naming

`MaterialChangeKind` — exactly four members, closed the same way `InitiationClass` is
closed (HA-01): the only way to widen it is to edit the enum, and doing so trips a
set-equality assertion. **The string form of a real kind is refused**, for the reason
HA-01 established: a vocabulary that accepts its own names as strings widens by typo.

**THE DISCREPANCY, recorded rather than resolved.** HA-03 item 1 says "imported from the
registry's own definitions". The registry's own definition is R24 in
`REQ_STRUCTURAL_CEILING`, and its wording is:

> "A material change **may include** a newly enabled care function, a new
> clinician-authored care plan, a changed legal role, or a qualifying event from a
> validated sensing contract."

**"May include" is an ILLUSTRATIVE list.** `REQ_OFFER_MECHANISM`'s RULING 2 treats the same
four as CLOSED ("its four already-ratified material-change kinds … imports those four
kinds unchanged"). This module implements the **closed** reading, because that is what the
governing REQ and this dispatch both direct — **but closing an open list is a ruling, and
a session should not make it silently.** Flagged here and in the module docstring.

**The non-trigger list is a UNION, not a second copy.** `NON_TRIGGERS` imports
`harness.purpose_trigger.NOT_A_TRIGGER` (R23's already-enforced closed seven) and adds
R5's own — `prior_refusal`, `template_revision`, `passage_of_time`, `usage_frequency`,
`model_recommendation`, and the rest. R29's lesson applied: one vocabulary, one
definition, so R23's list cannot drift from this one. A standing test asserts the subset
relation.

## 4. THE PROOFS

`eval/test_situation_identity.py` — **32 tests, 32 pass.**

### A5 — five idempotency proofs, EACH ITS OWN TEST (item 3)

| Test | What it re-submits |
|---|---|
| duplicate event delivery | the same event twice — the sensor/queue duplicate |
| retry | identical payload, second attempt after a failed downstream step |
| **service restart** | **a genuinely COLD SUBPROCESS** (`sys.executable -c`), not `importlib.reload` |
| event replay | the same `event_ref` with material state rebuilt from the log, reordered |
| semantically equivalent resubmission | different key order, casing, and whitespace |

**The restart proof was written twice, and the first version is worth recording.**
`importlib.reload` was tried first: it rebinds the module object shared by the whole test
session, so every later `isinstance(kind, MaterialChangeKind)` in the file failed against
the pre-reload class — **18 tests went red from a test-harness artifact.** A proof that
poisons its own session is not a proof. A subprocess is also the stronger claim: it is a
real interpreter start, which is what "service restart" means.

**ANTI-VACUITY for A5:** a genuinely different world event mints a DIFFERENT id, with each
of the five identity components varied independently. Without it, every assertion above
would pass on a constant.

### A4 — six non-trigger fault twins, each its own test (item 4)

passage of time (×3 spellings) · engagement patterns · graph fullness · prior acceptance ·
**prior refusal** · **template revision** — each refused by execution. The last two are
R5's own additions, absent from R23's seven, which is exactly why `NON_TRIGGERS` is a union.

Plus: **a non-trigger smuggled into `material_state` is refused** — the dict is the back
door, and refusing non-trigger KINDS while accepting a non-trigger FIELD would let
engagement change the identity anyway.

**ANTI-VACUITY for A4:** a genuine registered change mints exactly one situation — all four
kinds mint, all four ids differ, and each id re-derives from its own fields. Without it,
"everything is refused" would pass all six twins.

### §2.3 provenance

Five parametrized cases prove `session_id`, `prompt`, `utterance`, `operator_label` and
`model_id` cannot reach the identity, and three prove a blank `principal` /
`source_authority` / `event_ref` is refused.

## 5. OFFER CREATION NOW REQUIRES A SITUATION (item 5)

`harness/offer_gate.py::present_offer` gains a **required** keyword-only `situation`.
Two refusals, both `NoSituationError`, both proven:

- **A bare `situation_id` STRING is refused.** A hand-typed identity is precisely what
  §2.3's derivation exists to prevent.
- **A FORGED `Situation` is refused.** `Situation` is an ordinary frozen dataclass, so it
  can be hand-built with any id. `present_offer` therefore **re-derives** the id from the
  situation's own fields and compares. A situation whose id does not match its content is
  a claim about a registry decision, not one.

**Wired now, deliberately, while the module still has no production caller** — a
requirement added before the first caller costs nothing; one added afterwards is a
migration.

**`situation_id` is REQUIRED and RECORDED but is NOT part of R24's dedup key**, and there
is a test pinning that. Spending the SITUATION is R8, §12 step 5 — a later step. If a
later dispatch re-keys deliberately, that test is the one it must change, which is why it
is pinned now rather than left implicit.

**BLAST RADIUS:** 16 `present_offer` call sites in `eval/test_ceiling_solicitation.py`
migrated to pass a shared fixture situation. That file still passes **59 passed, 2
xfailed** — unchanged. A shared situation is safe precisely because the dedup key does not
include it.

## 6. WHAT STAYS ABSENT — and this is the honest limit of step 2

**None of the four kinds has a real registry behind it.** There is no care-function
enablement toggle, no structured clinician care-plan event, no legal-role change feed, and
no validated sensing contract — `harness/offer_gate.py` surveyed all four at D-R-171 and
this dispatch re-confirms it. So `source_authority` and `event_ref` are accepted as
non-empty strings, **validated structurally and never semantically.**

Stated plainly: **this module gives a canonical identity to an event a registry would
emit; it does not prove any such event has ever been emitted.** Nothing in this codebase
mints a situation from a real world change, because nothing observes one. Same posture
`purpose_trigger` and `offer_gate` each state about themselves — and the reason step 2 is
buildable anyway is that §2.3's derivation rule is fully specified by its own text.

## 7. THE MANIFEST CHECK (item 6) — the silent-skip hazard is closed

`eval/test_battery_manifest.py`, listed in the standing battery and **self-anchoring**: it
asserts that IT is in the list, so the guard cannot be disabled by deleting the one line it
guards.

It closes **both** directions of the hazard, because either alone leaves it open:

1. **A battery file that exists but never runs** — HA-01's own first `--layer 7` reported
   672/9 unchanged while 17 new tests sat unlisted.
2. **A file that is LISTED but collects NOTHING** — D-R-196's `main()`-shaped script, which
   pytest imports and collects zero from. Listing it in that state would have been worse
   than omitting it: the list looks complete and runs nothing.

**Exemptions are decisions, not defaults.** Seven files are exempt, each with a stated
reason; every one is a standalone script defining zero pytest tests. That is *asserted*:
`test_every_exemption_is_still_earned` fails if an exempt file ever grows a real test, and
`test_no_stale_exemptions` fails if one disappears. AST, never a source regex — a regex
for `def test_` also matches the phrase in a docstring.

**PROVEN BY EXECUTION, both directions, then reverted:**

```
FAULT TWIN A — an UNLISTED battery file appears:
  AssertionError: … neither in scripts/run_harness.sh's standing battery nor in
  BATTERY_EXEMPT, so they never run: ['test_zz_ha03_faulttwin.py']   → 1 failed, 13 passed

FAULT TWIN B — a LISTED file that collects nothing:
  AssertionError: … in the standing battery but define NO pytest tests:
  ['test_zz_ha03_empty.py']                                          → 1 failed, 13 passed

ANTI-VACUITY — clean tree:                                            → 14 passed
```

**Why the check lives in a test rather than in shell:** it runs inside the battery block
before the harness with `set -e` in force, so a failure aborts the run exactly as shell
would — while getting Python's AST instead of `grep` and a failure message that names the
file.

## 8. RUNS (item 8)

| Run | Result |
|---|---|
| Standing battery | **759 passed, 9 xfailed** — 713/9 + exactly the 46 added tests (32 situation + 14 manifest) |
| `--layer 7` L7 | **27/27** |
| `--layer 7` L7V2 | **27/28** (1 skipped — the opt-in live-output check) |
| AUDIT / DISC / SCHEMA / VOICE | **8/8 / 1/1 / 1/1 / 1/1** |
| **RATCHET** | **PASS — no scenario regressed vs baseline** |
| Memory harness | **13/17** — failures exactly {MEM-115, MEM-116, MEM-117, MEM-118}, inside the D-109/D-110 pin |

`--full` NOT run; Requirements Discipline item 12 is NOT satisfied and is not claimed.

## 9. SCOPE HELD (item 7) AND FINDINGS

**Fixtures only. Nothing initiates, nothing is offered, nothing is enabled.** Minting is a
pure function; the only `OfferGate` used is in-memory and lives inside tests.
`harness/initiation.py` was not touched. Nothing HIP says today changed.

1. **R24 says "may include"; RULING 2 treats the four as closed.** Implemented closed, per
   the governing REQ and this dispatch — but closing an open list is a ruling (§3).
2. **The four kinds still have no real registry behind them** (§6). Structural validation
   only; `source_authority` and `event_ref` are unvalidated non-empty strings.
3. **`situation_id` is not in R24's dedup key** (§5), pinned by a test so a later re-key is
   deliberate.
4. **`control_flow.py`'s "stubs — NOT connected to the pipeline" comment is still stale**
   — carried from HA-01 finding 2 and HA-02 finding 3, still not corrected, still outside
   the scope of the dispatch that found it. Third time it is being reported.
