# DISPATCH_FM25 — `.hip-scope` is now the claim's own artifact: atomic by ordering, fails closed, six twins
Status: **BUILT — LANDED** — ruling 12 enforced; both selftests green (10 claim cases + 14 guard cases)
Reconciled-Against: `6bdf0e8` (`~/hip-roadmap` @ `roadmap`)
Dispatch: FM 25
Date: 2026-08-14 21:35 (Mountain)
REQ: **`REQ_SURGICAL_STAGING_PRODUCT_FILES` Amendment 1** (`8c2b2c2`) — landed **BEFORE any code**,
and it TAKES the option the REQ's own OPEN section named and deliberately did not take.

---

## 0. THE EXCEPTION LINE

```
FM 25 — .hip-scope atomic claim artifact: atomic by ordering, fails closed, six twins
COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING
```

---

## 1. THE ATOMICITY MECHANISM — and the statement the ruling asked for

**The board row is NOT WRITTEN.** Of the ruling's two permitted shapes ("board row not written,
or written-then-reverted"), this build takes the first, and gets it **by ORDERING rather than by
revert machinery**: the scope phase runs to completion — create, then verify — **before
`edit_row()` ever executes**, so every scope failure leaves the board byte-untouched *by
construction*. There is no window in which a claim exists without its scope, because the claim
does not begin until the scope is proven.

- **CREATE** — `tmp file in the same directory + fsync + os.replace()`, atomic on POSIX
  (same-directory matters: `os.replace` is atomic only within one filesystem). A directory
  squatting on `.hip-scope` is caught as a create failure *before* the prior-read could
  traceback on it.
- **VERIFY** — the file is **re-read from disk** (never trusted from the write buffer) and
  checked against the preflight's own sources:
  1. content round-trip: disk prefixes == intended prefixes, exactly;
  2. worktree ownership: the file sits at `rev-parse --show-toplevel` of the claimed repo;
  3. branch ownership: not a detached HEAD — a claim with no pushable branch owns nothing;
  4. provisioning coherence, **mirroring `lane_preflight`'s documented tolerance exactly**:
     partial provisioning is the common case (`~/hip-roadmap` itself carries `.hip-graph` and
     no `.hip-owns`); what fails is **disagreement** between the two, or a file that exists but
     cannot be read or parsed.
- **FAIL CLOSED** — any create/verify failure restores a pre-existing `.hip-scope`
  **byte-identical** (or removes the new one if none existed) and exits **4**, a new code with
  exactly one meaning, per the tool's own "an exit code is not an answer" rule.
- **The belt for the other direction:** if the *board* phase fails before the commit exists
  (anchor mismatch, staged-set refusal), the board file is checked out back to HEAD **and** the
  scope is restored — keyed on a `committed` flag that `surgical_commit_and_push` flips the
  moment the commit lands. Post-commit failures (passenger refusal exit 3, a push error) keep
  both, because the claim EXISTS locally and its scope belongs to it.

**Compatibility, stated not slipped in:** `claim` mode now **requires `--scope`**; the legacy
flat invocation still works for row edits and prints a migration note; `close` needs no scope.

## 2. TWIN RESULTS — ten cases, all green

| case | result |
|---|---|
| A1 two sequential claims land, neither swept (pre-existing) | **PASS** |
| A1 commit is board-only (pre-existing) | **PASS** |
| A2 passenger refusal, claim kept locally (pre-existing ×2) | **PASS** |
| **A7** claim lands with a **verified** scope (`exit 0`, prefixes round-trip) | **PASS** |
| legacy flat invocation works + prints the migration note | **PASS** |
| claim without `--scope` refused before anything is written (`exit 2`) | **PASS** |
| **A8** induced CREATE failure (a directory at `.hip-scope`) → **exit 4, board byte-untouched, local and remote** | **PASS** |
| **A9** induced VERIFY failure — **a REAL one, not a stub** (`.hip-owns` 7688 vs `.hip-graph` 7691, the preflight's own disagreement rule) → **exit 4, prior sentinel scope restored byte-identical** | **PASS** |
| **A10 end-to-end**: after A7's claim, FM 23's `scope_guard.sh` **enforces the auto-written scope on the very next commit** — foreign path refused with `SCOPE GUARD: REFUSED (exit 77)` in stderr, in-scope commit passes | **PASS** |

Plus FM 23's own `scope_guard_selftest.sh` re-run for regression: **14/14 green.**

**The seam rule held:** A9's verify-mismatch is a genuine ownership contradiction the preflight
itself would refuse — not an injected hook faking failure (the NC 10 class this project no
longer accepts as proof).

## 3. THREE OF MY OWN FIRST-RUN TWIN FAILURES, CONFESSED — each taught something

1. **A8 read exit 1, not 4:** my prior-read (`scope.read_bytes()`) tracebacked on the induced
   directory *before my own guard could speak*. The fix is in the tool, commented with the twin
   that caught it — the induced failure produced an uncontrolled crash where the ruling demands
   a controlled refusal, which is precisely the difference the twin exists to detect.
2. **A10 asserted the hook's exit code; git reports a refusing hook as COMMIT exit 1.** The
   guard's 77 lives in its stderr banner. The observable is the text, and the twin now says so
   in a comment — the same lesson FM 15's proofs recorded for the staging guard.
3. **The legacy case read exit 3 — a genuine passenger refusal my own test ordering created**
   (A10's local commit preceded it). The tool was right; the twin was wrong; reordered with the
   reason commented.

## 4. FINDINGS FILED

1. **The dogfood claim for FM 25 itself was made with the PRE-change tool** (`01d8320`,
   board-only push verified) — so this dispatch's own claim has no `.hip-scope`. The FIRST
   real-world scoped claim will be the next dispatch's, and that is the honest boundary of
   today's evidence: ruling 12 is proven in twins, not yet exercised on the live board.
2. **`close` mode intentionally writes no scope** — the claim's scope already stands. If a
   dispatch needs to *widen* scope mid-flight, that is an edit to `.hip-scope` (FM 23's
   documented path), not a re-claim; noted so nobody invents a third mechanism.

## 5. CLAIM IMPACT

```
CLAIM IMPACT: none
```

## 6. VERIFIED

- Machine gate ✓; claim `01d8320` **first** (dogfooded, pre-change baseline); amendment
  `8c2b2c2` **before** code; build `6bdf0e8`; all commits by explicit pathspecs under the lock;
  tree clean and in sync after each push.
