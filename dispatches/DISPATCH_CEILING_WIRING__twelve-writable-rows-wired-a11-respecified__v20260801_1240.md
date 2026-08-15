# DISPATCH_CEILING_WIRING
Status: BUILT
Reconciled-Against: 54737cf (HEAD at dispatch start)
REQ: `docs/requirements/REQ_CEILING_ACCEPTANCE__testing-plan-for-the-ceiling-sprint__v20260801_0617.md` (plan) and `REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2129.md` (R1, R10, R11, R18-R21, R26, R27, R29, R30)
Dispatch: D-87, 2026-08-01
**Status proposed: NONE. No requirement ruled MET.**

Gate passed: bill-ai / [REDACTED-MACHINE-NAME] / `~/hip-roadmap` / `roadmap` @ `54737cf`, clean.
`~/hip-vo`, `~/hip-dev`, `~/hip-harness` NOT touched.

**Result: all 12 writable rows are wired. No stop condition fired. No requirement ruled MET.**

Before D-86 the count was 3 of 30. It is now 12 of 12 writable — the other 18 are the 2
CONTRADICTED rows (need rulings) and the 16 UNWRITABLE (fixtures do not exist), both left
alone by instruction.

---

## What landed

| Row | Tier | File | Cases | State |
|---|---|---|---|---|
| A7 | LIVE | `test_ceiling_representation.py` | 10 | tripwire (D-86) |
| **A11** | **LIVE — re-specified** | `test_ceiling_audience.py` | 9 + 1 twin | **control assertion** |
| A27 | LIVE | `test_ceiling_solicitation.py` | 9 | tripwire |
| A29 | LIVE | `test_sensitivity_registry.py` | +4 twins | twin gap closed |
| A30 | LIVE | same | +4 twins | twin gap closed |
| **A18** | **LIVE — tier corrected** | `test_derivation_cascade.py` | 20 | was STRICT XFAIL |
| A1 | STRICT XFAIL | `test_ceiling_inference.py` | 1 red + 4 | red, correctly |
| A10 | STRICT XFAIL | same | 1 red + 4 | red, correctly |
| A19 | STRICT XFAIL | `test_ceiling_retention.py` | 1 red + 3 | red, correctly |
| A20 | STRICT XFAIL | same | 1 red + 3 | red; one third passes |
| A21 | STRICT XFAIL | same | 1 red + 2 | red, correctly |
| A26 | STRICT XFAIL | `test_ceiling_solicitation.py` | 1 red + 3 | red, correctly |

**11 standing batteries: 148 passed, 9 xfailed.** All six XFAIL rows are `strict=True`, so
an unexpected pass would surface as a hard failure. **None did** — the stop condition for
"an XFAIL row that PASSES on first run" was checked and did not fire.

---

## A11 — the ruled re-specification

Bill's ruling of 2026-08-01 replaced D-77's basis. The row is now a **behavioral control
assertion** rather than an absence scan:

- **permitted direction** — `subj == author` widens to `CLASS_HOUSEHOLD`, `owner` becomes
  `"household"`, rule `2-directive-share-household`. Asserted, passing.
- **the requirement** — bill says something about maya and asks to share it with the
  family. The widening restriction blocks it. Asserted, passing.
- **fault twin, executed** — `_unrestricted_classify` reimplements the directive branch
  with the subject check removed; it promotes the third-party claim and therefore fails the
  same assertion the real classifier passes.
- **metamorphic** — four wordings/positions/casings of the directive, all still blocked.
- **anti-vacuity** — the directive phrases still parse, and an AST check confirms the
  restriction is still a guard *inside* `classify()`, so a refactor that moves or deletes
  it is visible structurally and not only behaviorally.

**Hermetic by construction.** `classify()` reads the member/care-team/dyad/standing-policy
registry, and reads there have `CREATE TABLE` side effects (D-52). Every case points
`HIP_REGISTRY_DB` at a per-test temp file, so the battery mutates no shared registry —
notably not the one in the frozen `~/hip-harness` checkout — and runs identically with or
without `.env.dev` sourced.

---

## A18 — tier corrected

Re-tiered STRICT XFAIL → **LIVE**. D-81 built the cascade; the row has passed since. The
classification was right when written and was overtaken by the build.

**R18 REMAINS NOT MET** (Bill, 2026-08-01): TD-139, TD-140, TD-141. Re-tiering records
where the *check* stands and says nothing about the *requirement*. That is now the third
instance on file — A30 passes while R30 is NOT MET, A18 passes while R18 is NOT MET, and
A20 passes in one third while R20 does not.

---

## A29/A30 — the fault-twin gap closed

D-86 found §5 called the AST guard "the twin," but by `REQ_HARNESS_DISCIPLINE`'s definition
— *"the specific mutation that turns the check red"* — it was a guard: never executed
against a mutated consumer, so nothing proved it fires.

The guard's logic was extracted to `_local_ordering_names()` so a twin can execute it:

- a re-introduced local `SENSITIVITY_RANK` literal **is** flagged;
- TD-137's actual shape (`critical` below `high`) **is** flagged;
- a low/medium/high **confidence** table is **NOT** flagged — the discriminating half,
  without which the twin proves the guard fires but not that it fires on the right thing;
- prose describing the old encoding is **NOT** flagged — the D-75 defect asserted rather
  than trusted.

Plus three executed A30 twins against `_order_is_correct`: TD-137's real ordering, a
`critical == high` tie (the near-miss a `>=` would admit), and a **defaulting** rank
function (the silent-downgrade shape D-75 found in three places) — with an anti-vacuity
case proving the predicate accepts the real registry.

---

## Conventions adopted

**Namespacing: `test_ceil_a<N>_*` in `eval/test_ceiling_*.py`, written CEIL-A<N> in prose.**
D-86 established the need: **four independent A-numbering schemes coexist here** — the
ceiling's A1–A30, care-coordination A1–A4, demo-smoke A1–A4, and L5 red-team A1–A5. A bare
`A1` has four meanings. A7's functions were renamed from `test_a7_*` so the convention has
no exceptions.

**What a fault twin means for an XFAIL row — this needed deciding.** A LIVE row's twin is a
broken implementation that must go red. An XFAIL row is *already* red, so "it can go red"
proves nothing. The real hazard is an xfail red for the **wrong reason**: a typo, a bad
import, a predicate that could never pass whatever was built. So every XFAIL row carries a
`*_predicate_accepts_a_conforming_fixture` case — **not** xfail — running the same
predicate against a synthetic implementation that *does* have the feature. Several also
carry a near-miss proving the predicate is not trivially satisfied (e.g. A1 rejects an
allowlist that exists but is never consulted; A10 rejects an `encode()` mentioning two of
the four checks).

**Anti-vacuity everywhere.** Every scanning row asserts its corpus is non-empty and its
target still exists. A scan walking zero files reports no offenders and is indistinguishable
from a pass.

---

## Two bugs the discipline caught — in D-87's own checks

Worth recording because it is the argument for the pattern, made against itself:

1. **A26's predicate demanded an exact module-level name.** Its conforming fixture defined
   `record_non_response`, which did not match `non_response`, so the predicate rejected it.
   That predicate would have been **unsatisfiable by any real implementation** — a
   permanently-red xfail that could never flip. Fixed to substring matching.
2. **A27's scanner missed `optimize(objective="acceptance_rate")`** — the forbidden term is
   the keyword *value*, not the keyword. The scanner flagged `kw.arg` and positional
   strings but not `kw.value`. A real hole in the tripwire, found by the executed twin.

Both surfaced from the conforming-fixture and twin cases, which is exactly what they exist
for.

---

## Harness

```
standing batteries (11 files): 148 passed, 9 xfailed
== AUDIT:  8/8   (0 flaked, 0 skipped)
== DISC:   1/1
== L7:     27/27 (0 flaked, 0 skipped)
== L7V2:   27/28 (0 flaked, 1 skipped — CT-OUTPUT-GAP, opt-in by design)
== SCHEMA: 1/1   == VOICE: 1/1
RATCHET PASS — no scenario regressed vs baseline.
```

**All five ABSOLUTE checks PASS**, verified individually in the log rather than inferred
from the summary:

| Check | Result |
|---|---|
| G0 — output-side fabrication backstop | PASS |
| PSA1 — prompt/record fidelity | PASS |
| CTX-STRIP — no fact-bearing section in a frontier prompt | PASS |
| LI1 — learner example never crosses households or scopes | PASS |
| CS1 — Curator scorer narrows only, value-blind, no path to prompt | PASS |

**0 scenario FAILs.** `--full` not attempted — TD-129's memory guard refuses it on this
machine state, as the dispatch anticipated. Not fought.

---

## Stop conditions — all checked, none fired

| Condition | Result |
|---|---|
| REQ text vs D-77 classification disagree | **A11 — resolved by Bill's ruling before this dispatch**, not re-encountered |
| an XFAIL row PASSES on first run | none; all six red under `strict=True` |
| a row needs a fixture that does not exist | none among the 12 writable rows |
| anything ABSOLUTE red | none — all five PASS |

## What this dispatch did not do

- Ruled no requirement MET. R18 stays NOT MET; R11 is not ruled by wiring A11.
- Did not touch A12, A16, or the 16 UNWRITABLE rows.
- Amended `REQ_CEILING_ACCEPTANCE` only with §7 (execution state + the two corrections);
  §§1–5 unchanged, §6 (D-86's audit) unchanged.
- Touched no tree but `~/hip-roadmap`.
