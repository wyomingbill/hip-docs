# DISPATCH_FM15 — hook enforcement ON: shared `core.hooksPath` live across five worktrees, proven three ways
Status: **BUILT — LANDED** — enforcement live; clean commit allowed, policy violation refused with `HEAD` unmoved, lock path still open
Reconciled-Against: `f4495b6` (`roadmap` HEAD at the flip — read, not remembered)
Dispatch: FM 15 (re-issue of **FM 12**, which STOPPED on its precondition)
Date: 2026-08-14 17:13 (Mountain)
REQ: **`REQ_PROCESS_HARDENING_TOOLS`** acceptance **E1**, and **Bill's ruling 4** — no new REQ; this
dispatch flips a control that was already built and reviewed.
Branch: roadmap · Machine gate `bill-ai` @ `[REDACTED-MACHINE-NAME]` ✓

---

## 0. THE EXCEPTION LINE

```
FM 15 — hook enforcement ON: shared core.hooksPath live across five worktrees, proven three ways
COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING
```

**ROLLBACK, ONE LINE:**

```sh
git -C ~/hip-roadmap config --unset core.hooksPath
```

---

## 1. THE PRECONDITION — CLEAR, AND MEASURED BY THE INSTRUMENT FM 12'S FAILURE PAID FOR

```
scripts/lane_preflight.py --busy   ->   NOT BUSY — nothing is mid-run    (exit 0)
```

It found **four ESTABLISHED bolt connections to 7690** and classified all four as a **resident
service**, not a job:

```
OCCUPIED port 7690  pid 1983  Python  in [REDACTED-USER-PATH]/hip-cutover-demo
                    (resident service — holds a LISTEN socket; not mid-run)
NOT BUSY: 4 connection(s) above all belong to resident services
```

That is the demo dashboard, up 48 minutes at 0.0% CPU, left running by VD-62. Cross-checked by
hand: `ps` shows no battery, ratchet, harness, `pytest`, seed or reset anywhere.

> **THIS IS THE POINT OF FM 14 AND IT IS WORTH STATING.** FM 12 stopped because every lock read
> `free` while a 20-iteration battery held an ESTABLISHED socket — the lock table gave a confident
> false all-clear, and each dispatch hand-rolled its own `ps` pipeline. **This dispatch did not
> hand-roll one.** The distinction between *a service holding a connection pool* and *a job
> mid-run* — the exact judgement FM 12 got wrong — was made **by tooling**, and the tool also
> answered **where** (cwd `~/hip-cutover-demo`), which is what turns "something is running" into
> something a session can act on. A re-issue that re-invented the check would have learned nothing
> from the stop that caused it.

**HA-87 (CC-2) and FM 13/14 (CC-4) were named as possibly live. Neither shows any live process or
graph connection.** FM 14 is landed on the board (`a58bc8e`).

---

## 2. THE FLIP

```sh
git -C ~/hip-roadmap config core.hooksPath [REDACTED-USER-PATH]/hip-roadmap/scripts/hooks
```

**Authority: Bill's ruling 4** — *"All four tools are repo-versioned centrally and enforced across
every active worktree. Not per-worktree hooks."*

Written to the **shared** config `[REDACTED-USER-PATH]/hip-dev/.git/config:8`, so it reaches every
worktree at once. **Verified by asking git itself which hook it would run**, rather than inferring
it from the config value:

| worktree | `git rev-parse --git-path hooks/pre-commit` |
|---|---|
| `~/hip-roadmap` | `[REDACTED-USER-PATH]/hip-roadmap/scripts/hooks/pre-commit` |
| `~/hip-cutover-demo` | `[REDACTED-USER-PATH]/hip-roadmap/scripts/hooks/pre-commit` |
| `~/hip-vo` | `[REDACTED-USER-PATH]/hip-roadmap/scripts/hooks/pre-commit` |
| `~/hip-nc` | `[REDACTED-USER-PATH]/hip-roadmap/scripts/hooks/pre-commit` |

**This closes the limit `staging_guard.sh` names in its own header** — *"hooks are per-worktree and
are NOT version controlled. This protects `~/hip-roadmap` only. A repo-wide answer needs
`core.hooksPath` committed to the tree; named, deliberately not taken."* It is taken now, and the
control has one version-controlled source of truth instead of five copies that drift.

---

## 3. THE PROOFS — THREE, IN A REAL WORKTREE (`~/hip-roadmap`)

Two were asked for. **The third is the one that makes the other two mean something**: without it,
"a commit was refused" is indistinguishable from a control that blocks everything.

| # | what | lock | result | `HEAD` |
|---|---|---|---|---|
| **1** | clean commit — no board file staged | **none** | **ALLOWED**, exit 0 | `f4495b6` → **`32cb397`** |
| **2** | `docs/LANES.md` **+ another path** | **none** | **REFUSED — staging guard exit 76**, commit exit 1 | `32cb397` → **`32cb397` UNMOVED** |
| **3** | *the same two paths as proof 2* | **`repo`** | **ALLOWED**, exit 0 | `32cb397` → **`de14158`** |

**Proof 2's refusal, verbatim from the run:**

```
STAGING GUARD: REFUSED (exit 76)

  A shared board file is staged alongside other paths, with no repo lock held.

  shared: docs/LANES.md
  other: docs/dispatches/assets/FM15_hook_enforcement_proof.txt
```

— and it prints the two ways forward (commit the board file by itself, or run under the lock) plus
the preamble item 2 surgical-staging reminder and the deliberate bypasses.

**`HEAD` UNMOVED IS THE LOAD-BEARING PART**, and it was read before and after rather than inferred
from the exit code: `32cb397` both sides. A pre-commit hook that refuses *after* moving `HEAD`
would be worse than none.

**Proofs 2 and 3 are the same two paths and the same content.** The only variable is
`HIP_LOCK_HELD`. That is what establishes **fail-closed on policy, not a blanket block** — the
guard refuses the one shape it targets and gets out of the way otherwise.

**The edits used were real, not synthetic.** Proof 2's `docs/LANES.md` change is this dispatch's
own in-flight row recording proof 1; proof 3 committed it. Nothing was staged that I would not
otherwise have wanted to land, so no junk entered the board to manufacture a red.

**Transcript: `docs/dispatches/assets/FM15_hook_enforcement_proof.txt`.**

---

## 4. FINDINGS

### 4.1 FILED — this reaches the FROZEN demo tree, and that is recorded rather than passed over

VD-63 froze `~/hip-cutover-demo` at `d0282bd` and requires **Bill's explicit unfreeze** for changes
to it. `core.hooksPath` is repo-wide, so it now governs commits there too.

**It changes no file, no commit and no tag in that tree.** What it changes is how a *future* commit
there would be screened — and only ever in the direction of **harder to write to without the lock**,
which runs with the freeze rather than against it. **Recorded because "repo-wide" and "frozen lane"
are two facts that a later reader deserves to see reconciled, not discovered.**

### 4.2 FILED — the cross-worktree behaviour is proven by resolution, not by a commit

Every proof above ran in `~/hip-roadmap`. **No commit test was run in another worktree, and that
was deliberate:** the demo tree is frozen, and the remaining trees belong to live lanes whose
commit history is not mine to add to for a demonstration.

**What is proven for the other four is that git resolves the shared hook there** (§2 table, git's
own `rev-parse --git-path` answer). **What is not proven by execution is the refusal firing in
those trees.** The hook is the same file and the guard is path-independent, so there is no reason
to expect a difference — but *no reason to expect* is not *measured*, and the two are not merged
here. The first lane to attempt a mixed board commit will be the live test.

---

## 5. WHAT THIS DOES NOT DO

- **It does not fight the operator.** `HIP_STAGING_GUARD=off` and `git commit --no-verify` remain,
  by the guard's own design. This stops the accident, not the intent.
- **It does not enforce surgical staging.** The lock stops the *collision*; only surgical staging
  stops a lane committing another lane's rows, and that remains a discipline the guard's own
  refusal message restates rather than a control.
- **It does not fail closed on infrastructure.** A missing or unreadable guard warns and **allows**.
  A control that can brick five lanes' commits when a path moves is worse than the defect it
  prevents — that is the dispatcher's stated design, not an omission.

---

## 6. CLAIM IMPACT

```
CLAIM IMPACT: none
```

A repository control. No ledger claim's evidence is touched.

---

## 7. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `~/hip-roadmap` @ `roadmap`.
- Precondition by `lane_preflight.py --busy`, exit 0, **NOT BUSY**; cross-checked against `ps`.
- FM 15 claimed on `docs/LANES.md` in this dispatch's **first** commit (`f4495b6`), before the flip.
- `HEAD` read from the machine before and after every proof.
- **Rollback: `git -C ~/hip-roadmap config --unset core.hooksPath`**
