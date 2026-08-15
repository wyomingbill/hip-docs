# FM 23 — SURGICAL STAGING FOR PRODUCT FILES
Status: BUILT — **LANDED**
Reconciled-Against: 2026-08-14, `~/hip-roadmap` @ `roadmap` @ **`1c6abb2`**. Board claim
`b234e76`/`e304818`; REQ `5e25313`.

REQ: `docs/requirements/REQ_SURGICAL_STAGING_PRODUCT_FILES__scope-declaration-and-a-foreign-path-refusal__v20260814_2110.md`
— filed **before the first code edit**, per the FM 6 precedent, **no exception phrase**.

---

## 0. THE EXCEPTION LINE

```
FM 23 — SURGICAL STAGING FOR PRODUCT FILES
COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING
```

**14 twins green both directions, plus a live red/green in a real worktree with the hook
active. NEEDS BILL: nothing.**

---

## 1. THE DEFECT, AND WHY THE ASYMMETRY WAS THE DEFECT

`scripts/staging_guard.sh:26` protects exactly `docs/LANES.md docs/INDEX.md`. **Everything
else in every worktree was unprotected**, and the same sweep that motivated that guard kept
happening one directory over — **three times on 2026-08-14**: NC 14's `8ad909a` took NC 15's
two untracked in-progress files (**one red mid-draft**), the HA-85 doc race, and D-158's
original shape.

**A board row is recoverable from the board. Another lane's half-written source file is not.**

---

## 2. WHAT WAS BUILT

`scripts/scope_guard.sh` — refuses a commit staging paths outside `.hip-scope`, **exit 77**,
naming the foreign paths and the three ways out. Wired into FM 9's dispatcher
(`scripts/hooks/pre-commit`), live via `core.hooksPath`, with the dispatcher's existing rule:
**policy fails closed, infrastructure fails open**, because that hook governs five worktrees.

### The scope declaration — the choice, argued

**`.hip-scope` at the worktree root, per-worktree, UNTRACKED BY DESIGN.**

- **Not the claim's pathspec**, which the dispatch offered: the claim row lives in
  `docs/LANES.md` on `roadmap`, and **four of the five worktrees are on other branches and
  cannot read it** — the LIMIT the board records about itself. A hook resolving a row across
  branches would fail exactly where it is most needed.
- **Untracked**, because a tracked scope file would arrive in every worktree cut from that
  branch **declaring the previous dispatch's scope — the inheritance bug NC 8 hit** when
  `nc-b0` inherited `~/hip-vo`'s `.hip-owns`. Added to `.gitignore` with that reason recorded
  beside it.
- It sits beside `.hip-owns` and `.hip-graph`: the same shape of statement, *this checkout
  declares what it owns*.

**NO DECLARATION = NO CONSTRAINT.** A worktree without `.hip-scope` behaves exactly as before.
**A guard that broke every uninstrumented lane on the day it landed would be a worse defect
than the one it fixes**, and that is an acceptance clause, not a courtesy.

---

## 3. TWIN RESULTS — 14, BOTH DIRECTIONS

`sh scripts/scope_guard_selftest.sh` → **GREEN, 14 passed, 0 failed**, in a throwaway repo.

| clause | assertion | result |
|---|---|---|
| **A4** | no `.hip-scope` → unconstrained | **PASS** |
| **A2** | an in-scope file passes; a declared **directory prefix** passes; the commit actually lands | **PASS ×3** |
| **A1** | a foreign path is **REFUSED (77)**, the refusal **names it**, and **HEAD is unmoved** | **PASS ×3** |
| **A1** | a **MIXED** commit — one of mine, one of theirs — is refused too. **This is the NC 14 shape.** | **PASS** |
| **A6** | the refusal names the escape (`git reset HEAD -- …`) | **PASS** |
| **A3** | the `repo` lock overrides; **a `graph:` lock does NOT** — only `repo` serialises the lanes; the documented bypass works | **PASS ×3** |
| **A5** | an **empty** declaration fails **open**; a **removed** one fails open | **PASS ×2** |

### And a LIVE red/green, in this worktree, with the hook active

```
SCOPE GUARD: REFUSED (exit 77)
  foreign: harness/_fm23_foreign_probe.py
         git reset HEAD -- harness/_fm23_foreign_probe.py
HEAD UNMOVED
```
then, with the foreign path unstaged, the in-scope commit **landed** (`6e0cba9`). Committed
**without** the lock, deliberately, so the override could not mask the refusal.

---

## 4. FILED, NOT BLOCKING (2)

**(FM23-1) The guard cannot protect a commit made under the `repo` lock — and nearly every
dispatch commit is.** A3 honours the lock as an override, matching `staging_guard.sh`, and the
reasoning holds: under the lock the lanes are serialised, so a wide commit is a decision. **But
NC 14's `8ad909a` was itself a locked commit.** So this guard would not have stopped the very
incident that motivated it, and saying otherwise would be false. **What it does stop is the
unlocked sweep** — the ordinary case, and the one nobody is watching. Tightening the override
to require the scope to *also* pass under the lock is a policy change, not a fix; named, not
taken.

**(FM23-2) Nothing writes `.hip-scope` yet.** It is declared by hand, so it protects only a
dispatch that chose to be protected. The obvious closure — `claim_lane.py` writing the scope
when it claims the number, so the two cannot drift — is named in the REQ's OPEN section and
**deliberately not built**: it couples two tools and is a design decision.

---

## 5. WHAT THIS DISPATCH DID NOT DO

- **Weakened `staging_guard.sh`** — untouched, and it keeps exit 76.
- **Changed `core.hooksPath`** — already live; this extends what it dispatches to.
- **Touched product runtime code** — `scripts/` and `.gitignore` only.
- **Wrote `.hip-scope` into any lane** — including this one; the live probe's file was removed.
- **Built the `claim_lane.py` coupling** — FM23-2.

---

## 6. CLAIM IMPACT

```
CLAIM IMPACT: none
```
