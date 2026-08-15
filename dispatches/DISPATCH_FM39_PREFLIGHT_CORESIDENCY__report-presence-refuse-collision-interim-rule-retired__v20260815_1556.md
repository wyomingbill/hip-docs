# DISPATCH_FM39_PREFLIGHT_CORESIDENCY
Status: BUILT
Reconciled-Against: `03a1ea0` (`~/hip-roadmap` @ `roadmap`), 2026-08-15

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_PROCESS_HARDENING_TOOLS__claim-lane-register-doc-lane-preflight-scrub__v20260814_1613.md`
— **AMENDMENT 7**, committed at `e8f628c` **before the first code edit**. It supersedes
Amendment 5's G4 disposition, which FM 32 left explicitly referred to Bill.

**CLAIM IMPACT: none.**

---

## THE ASK — Bill's ruling, verbatim

> held detection stays OPT-IN and VISIBLE, never a blocking default. The default preflight:
> 1. ALWAYS reports the other active holder prominently — identifies BOTH lanes and BOTH
>    scopes in the output.
> 2. BLOCKS on: actual scope overlap; ambiguous ownership (either lane's scope
>    unreadable/undeclared); staged changes that would overwrite another lane's attributed
>    board/scope state (FM 32's staged-diff check feeds this).
> 3. ALLOWS demonstrated non-overlapping parallel work — the FM 35/36 co-residency shape
>    with disjoint scopes passes with the report visible.

Plus: record the retirement of the one-worktree-one-dispatch interim rule, with
debt-register cleanup queued.

---

## THE ONE THING THAT CHANGED, AND IT IS THE WHOLE DISPATCH

FM 32 measured that blocking on **any** held seam refuses lanes that are legitimately
parallel — FM 14's *"clean machine passes"* twin went red the moment that default landed.

**The ruling keeps that finding and sharpens it: co-residency is not the hazard. OVERLAP
is.** So the default gate stops asking *"is anyone else here"* and starts asking *"would we
collide"*.

**Presence is reported. Collision is refused. Disjoint parallel work is allowed.**

---

## ⚠ THE CLAIM ITSELF HAD TO BE MADE BY HAND — AND THE REASON IS THE DISPATCH'S OWN SUBJECT

`claim_lane.py` **refused** this claim, correctly. A neighbour's **uncommitted scrub run**
is sitting in **~180 `docs/` files including `docs/LANES.md`**, so staging the board would
have carried three of their scrubbed rows alongside mine and FM 32's staged-payload check
fired on *"3 rows changed, expected 1"*.

**The guard refusing is what forced the hand-claim, and that is the guard working** — built
by FM 32 for exactly this shape. The claim was then made under the repo lock by STANDARD
PREAMBLE item 2's literal procedure: union saved (366 607 bytes), file reset to HEAD
(366 516 bytes), only this row applied, staged set verified as `docs/LANES.md` alone with a
one-row payload starting with this lane's prefix, then the union restored **with this row on
top**.

**Verified after the fact:** the commit contains `1 file changed, 1 insertion(+), 1
deletion(-)`, and **172 modified files remained in the working tree, untouched.**

---

## WHAT WAS BUILT

`lane_preflight.coresidency_report()`, wired into the **default** path:

| clause | behaviour |
|---|---|
| **P1** | the report prints **unconditionally**, naming **both lanes and both scopes** — on the passing path as well as the blocking one |
| **P2** | **blocks** on actual scope overlap (prefix containment either way), naming the colliding pair |
| **P3** | **blocks** on ambiguous ownership: unreadable, undeclared, an empty declared scope, or unattributed legacy lines sitting alongside lane blocks |
| **P4** | **blocks** on a staged collision — FM 32's index check, moved to preflight time |
| **P5** | **allows** disjoint co-residency, exit 0, report visible |
| **P6** | `--held` unchanged and still opt-in |
| **P7** | a solo lane is byte-unchanged |

**Exit `9` (`EX_CORESIDENCY`) is distinct on purpose** — an exit code is not an answer, so
it means one thing.

**Why P3 is strict:** *you cannot prove disjoint against an unknown.* A lane working
without a declaration is not "probably fine", it is **unmeasurable** — and unattributed
lines alongside attributed blocks belong to nobody, so no lane can be proven disjoint from
them.

### ⚠ A DESIGN ERROR IN MY OWN FIRST CUT — MEASURED, AND CORRECTED BEFORE IT SHIPPED

The first version computed overlap against **other worktrees** and promptly refused this
very tree against `~/hip-vo` on **five "overlaps" that cannot collide**:

```
- SCOPE OVERLAP with [REDACTED-USER-PATH]/hip-vo: 'docs/INDEX.md' vs 'docs/INDEX.md'
  … and four more
```

**Separate worktrees have separate working trees and separate indexes**, so `docs/INDEX.md`
in two of them is **two different files**. Overlap is only meaningful **between lanes
sharing one worktree** — the other attributed blocks in this worktree's own `.hip-scope`,
which **FM 38 built the substrate for**. Other worktrees' holders are now **reported, never
blocking**, which is exactly Bill's *"held detection stays opt-in and visible"*.

**Caught by running it on the real tree before committing it**, and the reasoning is in the
source so the next reader does not re-derive it by re-breaking it.

---

## VERIFIED — FIVE TWINS (plus a reverse), ALL NINE SUITES GREEN

| twin | result |
|---|---|
| **T1** disjoint co-residency **PASSES** with the report present | **PASS** — rc=0, 2 lanes, **both named, both scopes named** |
| **T2** overlapping scope **BLOCKS** | **PASS** — rc=9, names the colliding pair |
| **T3** undeclared/unattributed scope **BLOCKS** (ambiguous) | **PASS** — rc=9 |
| **T4** staged shared state **BLOCKS** | **PASS** — rc=9 |
| **T5** solo lane **PASSES**, nothing blocking | **PASS** — rc=0, 1 lane |
| **T5 reverse** the report prints even with one lane | **PASS** — the operator is never guessing whether the scan ran |

`python3 scripts/lane_tools_selftest.py` → **ALL TWINS GREEN** across all nine suites,
including the eight that predate this dispatch.

**Live, on the real tree:** the default preflight now prints the co-residency report,
names `~/hip-vo` as also active and **explicitly not blocking**, and exits **0**.

**Reasoned about — not independently executed:**
- That two worktrees can never collide through the index. It follows from git's worktree
  model (one index per worktree); **not demonstrated by a twin here** — the twins cover the
  same-worktree case, which is the one the ruling is about.

---

## THE INTERIM RULE — RETIRED, AND ITS ABSENCE RECORDED

`docs/design/HIP_PROCESS__development-operating-model__v20260814_1025.md` **§11** (`db0f61b`)
records the retirement, what a lane must still do (declare a scope — now blocking; stage
surgically; read the report), and one honest finding:

**THE INTERIM RULE HAD NO WRITTEN FORM IN THIS REPOSITORY.** `grep` for
*one-worktree-one-dispatch*, *one dispatch per worktree* and their variants across `docs/`
returns **nothing but FM 39's own board row and that new section**. It was a convention
carried in practice, never a document. **Recorded so nobody later hunts for the text being
retired and concludes it was lost.**

**Debt-register row cleanup stays QUEUED** for the next process pass, as instructed.

---

## HASH

| commit | what |
|---|---|
| `ca743f9` | board claim — **hand-made under the lock, because the guard refused** |
| `e8f628c` | **REQ Amendment 7 — before code** |
| `03a1ea0` | the co-residency gate and five twins |
| `db0f61b` | process doc §11 — the interim rule retired |
| *(this commit)* | dispatch doc, INDEX |

---

## OPEN

1. **A neighbour's scrub of ~180 `docs/` files is uncommitted in this worktree.** Not mine
   to commit or revert; left exactly as found. It is why this dispatch hand-claimed, and it
   is a live example of the co-residency the gate now measures.
2. **Debt-register rows describing co-residency as a hazard are now partly superseded.**
   Queued by instruction, not done here.
3. **Cross-worktree collision is asserted from git's model, not from a twin.** The twins
   cover same-worktree co-residency. If cross-worktree ever needs to block, that is a new
   question with a new measurement.
4. **`--held` still blocks on any held seam.** Unchanged by this dispatch and still the
   opt-in escape hatch; whether anything should use it is now genuinely open, since the
   default gate answers the question it was standing in for.
