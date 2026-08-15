# REQ_SURGICAL_STAGING_PRODUCT_FILES
Status: PLAN
Reconciled-Against: 2026-08-14, `~/hip-roadmap` @ `roadmap`. Filed by FM 23 **before the
first code edit**, per the FM 6 precedent and with **no exception phrase**.

---

## THE REQUIREMENT

Bill's words, 2026-08-14, verbatim:

> **THE DEFECT, three occurrences today: NC 14's 8ad909a swept NC 15's two untracked
> in-progress files (one red mid-draft); the HA-85 doc race; D-158's original shape. The
> staging guard protects board/docs; product files have nothing.**
>
> **BUILD: extend the pre-commit dispatcher (FM 9's hook, live via core.hooksPath): a commit
> that stages files not matching the claiming dispatch's declared scope is REFUSED naming the
> foreign paths — same fail-closed shape as claim_lane.py's passenger rule. Scope declaration
> mechanism: simplest thing that works (the claim's pathspec or a .hip-scope file); document
> the choice. Twins both directions: foreign sweep refused with HEAD unmoved; clean in-scope
> commit passes; lock-held override per the existing pattern.**

**Expanded.** `scripts/staging_guard.sh:26` protects exactly two paths —
`docs/LANES.md docs/INDEX.md`. Everything else in every worktree is unprotected, and the same
sweep that motivated the guard keeps happening one directory over. **The asymmetry is the
defect: a board row is recoverable from the board; another lane's half-written source file is
not.**

---

## THE ACCEPTANCE TEST

- **A1 RED — a foreign sweep is REFUSED.** A commit that stages a path outside the declared
  scope exits non-zero, **names the foreign paths**, and leaves **`HEAD` unmoved**.
- **A2 GREEN — a clean in-scope commit passes**, unchanged in behaviour from today.
- **A3 OVERRIDE — the existing pattern.** A commit under the `repo` lock is allowed, verified
  from `HIP_LOCK_HELD` exactly as `staging_guard.sh` already does, so the two guards agree on
  what an override is.
- **A4 NO DECLARATION = NO CONSTRAINT.** A worktree with no scope declared behaves exactly as
  it does today. **A guard that breaks every uninstrumented lane on the day it lands is a
  worse defect than the one it fixes.**
- **A5 FAIL OPEN ON INFRASTRUCTURE, CLOSED ON POLICY** — the dispatcher's existing rule
  (`scripts/hooks/pre-commit`): a missing or unreadable scope file must not brick five
  worktrees' commits; a *violated* scope must refuse.
- **A6** the refusal **names the escape** — how to widen the scope, and how to override —
  because a guard that cannot be satisfied gets switched off.
- **A7** twins for A1-A5, executing, run in a throwaway repository.

---

## THE SCOPE DECLARATION — THE CHOICE, AND WHY

**Chosen: a `.hip-scope` file at the worktree root.** One path prefix per line, `#` comments
ignored.

**Why not the claim's pathspec**, which the dispatch offers as the alternative: the claim row
lives in `docs/LANES.md` on `roadmap`, and **four of the five worktrees are on other branches
and cannot read it** — that is the same LIMIT 1 that `docs/LANES.md` already records about
itself. A hook that had to resolve a row across branches would fail exactly where it is most
needed, and it would couple every commit in every lane to the board's format.

**`.hip-scope` is per-worktree, which is what the constraint actually is.** A dispatch owns a
worktree for its duration; the file says what that worktree is allowed to touch, and it is
deleted or rewritten when the next dispatch claims it. It sits beside `.hip-owns` and
`.hip-graph`, which are the same shape of statement — *this checkout declares what it owns* —
and `lane_preflight.py` already reads those.

**It is untracked by design.** A tracked `.hip-scope` would arrive in every worktree cut from
that branch and declare the previous dispatch's scope — **exactly the inheritance bug NC 8
hit** when `nc-b0` inherited `~/hip-vo`'s `.hip-owns` and `lane_preflight` refused it.

---

## WHAT'S ALREADY DONE — REFERENCED, NOT REBUILT

| piece | where |
|---|---|
| the shared dispatcher, live via `core.hooksPath` | `scripts/hooks/pre-commit` (FM 9 §5) |
| the board-file guard and its exit 76 | `scripts/staging_guard.sh` |
| lock verification from `HIP_LOCK_HELD` | `staging_guard.sh`, and `hip_lock.py` which exports it |
| the fail-closed refusal shape that names the offending item | `claim_lane.py`'s passenger rule (exit 3) |

## WHAT'S KNOWN BROKEN

**Three occurrences today**, all one shape — a commit taking files it did not author:
**NC 14's `8ad909a` swept NC 15's two untracked in-progress files, one red mid-draft**; the
HA-85 doc race; and D-158's original shape. `staging_guard.sh` covers two paths and nothing
else.

## CONSTRAINTS

- **Must not break an uninstrumented worktree** (A4).
- **Must not weaken `staging_guard.sh`** — the board guard keeps its behaviour and its exit 76.
- **Must fail open on its own errors** (A5). This hook governs every commit in five worktrees.
- **No product runtime code**; `scripts/` and the hook only.
- **The refusal must be actionable** (A6).

## OPEN — NOT DECIDED BY THIS REQ

**Whether `.hip-scope` should eventually be written by `claim_lane.py`** — so claiming a
number also declares the scope, and the two cannot drift. That couples two tools and is a
design decision, not a defect fix. **Named, and deliberately not taken here.**

---

## AMENDMENT 1 — `.hip-scope` IS WRITTEN BY THE CLAIM, ATOMICALLY (Bill's ruling 12, 2026-08-14, FM 25)

**This amendment TAKES the option the OPEN section above named and deliberately did not take.**
The coupling is now ruled: claiming a number also declares the scope, and the two cannot drift.

### THE RULING — verbatim

> **`claim_lane.py` writes `.hip-scope` ATOMICALLY at claim time, then immediately verifies it
> matches lane/worktree/branch ownership (the preflight's own sources). If it cannot CREATE or
> VERIFY the scope file, THE CLAIM FAILS CLOSED — no partially claimed lane: board row not
> written, or written-then-reverted in the same atomic operation; state which and prove it.**

### THE MECHANISM CHOSEN, AND THE STATEMENT THE RULING ASKS FOR

**The board row is NOT WRITTEN** — atomicity by ORDERING, not by revert machinery. The scope
file is created and verified **before** `edit_row()` ever runs, so a create- or verify-failure
leaves the board byte-untouched by construction; there is no window in which a claim exists
without its scope. The write itself is `tmp-file + fsync + os.replace()` in the worktree root —
atomic on POSIX — and a PRE-EXISTING `.hip-scope` is saved first and **restored byte-identical**
on any later failure (verify failure, board-anchor failure, commit refusal), so no failure path
leaves the worktree with a half-installed declaration either.

### VERIFY = the preflight's own sources

After `os.replace()`, the file is **re-read from disk** and checked:

1. **content round-trip** — the re-read prefixes equal the intended prefixes exactly;
2. **worktree ownership** — the file sits at `git rev-parse --show-toplevel` of the repo being
   claimed, not some other tree;
3. **branch ownership** — the current branch equals the branch the claim will push;
4. **provisioning coherence** — if `.hip-owns`/`.hip-graph` exist they must be readable
   (lane_preflight's rule 2/3 surface); an unreadable ownership file fails the claim closed.

### ACCEPTANCE (adds A7-A10 to A1-A6 above)

- **A7 GREEN:** a successful claim leaves BOTH the board row and a verified `.hip-scope`.
- **A8 RED (create):** an induced create-failure leaves **no claim** — board byte-identical —
  and says why.
- **A9 RED (verify):** an induced verify-mismatch (a REAL one — e.g. wrong-branch ownership,
  never an injected stub, per the NC 10 seam rule) leaves **no claim**, restores any prior
  scope byte-identical, and says why.
- **A10 END-TO-END:** after a successful claim, FM 23's `scope_guard.sh` **enforces the
  auto-written scope on the next commit** — a foreign-path commit in that worktree is refused
  exit 77 with no further configuration.

### COMPATIBILITY, STATED NOT SLIPPED IN

`claim` mode now **requires `--scope`** (one or more path prefixes): a claim without a scope
declaration is exactly the partial state this ruling abolishes. The legacy flat invocation
(no mode word) still edits the board for `close`-type row updates and prints a loud note that
claims must use `claim` mode — existing sessions keep working, and the note is the migration.
