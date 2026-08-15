# DISPATCH_FM38_SCOPE_WIDENS_NEVER_REPLACES
Status: BUILT
Reconciled-Against: `d9c223f` (`~/hip-roadmap` @ `roadmap`), 2026-08-15

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_PROCESS_HARDENING_TOOLS__claim-lane-register-doc-lane-preflight-scrub__v20260814_1613.md`
— **AMENDMENT 6**, committed at `cf04036` **before the first code edit**.

**CLAIM IMPACT: none.**

---

## THE ASK — Bill's requirement, verbatim

> claim_lane's .hip-scope write must WIDEN, never REPLACE. Multiple concurrent lane
> claims in one worktree must preserve all active attributed scope declarations. Add a
> twin proving lane B's claim cannot erase lane A's scope.

---

## WHY THIS WAS A SAFETY DEFECT, NOT AN INCONVENIENCE

`scope_guard.sh` refuses a commit that stages files outside the declared scope. So a lane
whose declaration a neighbour has silently replaced is **either unguarded, or guarded
against the wrong set — and the guard reports neither.**

**A safety declaration a neighbour can delete without either lane noticing is not a
declaration.**

### The evidence that it was not theoretical — three kinds

1. **THE FM 36 INCIDENT.** A `claim_lane.py` invocation *"executed and PUSHED `c0cc0d7`
   ('probe'), replacing FM 34's identifier with a test placeholder and **overwriting
   `~/hip-roadmap/.hip-scope`**"*, recorded on the board with the bad commit deliberately
   not rewritten.
2. **THE WORKAROUND IS ON THE BOARD, FOUR TIMES.** HA-97, NC 27, NC 30 and NC 22 each say
   some version of *"scope appended to `.hip-scope`, **widened not replaced**"* — every one
   a lane doing by hand what the tool could not do at all.
3. **IT HAPPENED AGAIN WHILE THE AMENDMENT WAS BEING WRITTEN.** FM 38's own claim
   (`c9e836b`) replaced `~/hip-roadmap/.hip-scope`, discarding FM 34's block. **The defect
   demonstrated itself in the act of being filed.** Recorded rather than tidied away.

---

## WHAT WAS BUILT

**One delimited, attributed block per lane**, keyed on the board row prefix — the lane's
identity everywhere else in this tool, so no second naming scheme:

```
# >>> hip-scope lane[| Advisor — `~/hip-vo` @ `main` |] claim: <message>
docs/
scripts/foo.py
# <<< hip-scope lane[| Advisor — `~/hip-vo` @ `main` |]
```

| behaviour | before | after |
|---|---|---|
| a claim | rebuilt the whole file and `os.replace`d it | writes **only its own block**, carries every other line forward |
| the same lane re-claiming | replaced everything | **updates its own block**, never duplicates |
| a close | did not touch the scope at all | **removes only its own block**, after the row has landed |
| legacy hand-written content | destroyed | **preserved verbatim, in place** |

**`scope_guard.sh` is untouched, and that is by design:** the markers are comments, and the
guard reads every non-comment line — so what it enforces is the **union of the blocks**,
which is the widened set. No edit to the guard, no new coupling.

**The close narrows AFTER the row lands, never before:** a scope narrowed by a close that
then failed would leave the lane guarded against nothing while its row was still open. A
failure to narrow is reported, not fatal — the close has landed and re-running it would
find an anchor that no longer matches.

---

## VERIFIED — 7 CASES, BOTH DIRECTIONS, ALL EIGHT SUITES GREEN

| case | result |
|---|---|
| **W5+** B claims after A → **both present and attributed** | **PASS** |
| **W5+** `scope_guard` sees the **union** of both blocks | **PASS** — `docs/alpha`, `scripts/a.py`, `docs/beta` |
| **W5−** the **FM 36 shape reproduced**: the old replacing write **LOSES A's scope** | **PASS** |
| **W3** B closes → B's block gone, **A's intact** | **PASS** |
| **W2** re-claim **updates**, does not duplicate | **PASS** — 1 block |
| **W4** **legacy** unattributed content survives verbatim | **PASS** |
| **W6** scope failure → **exit 4, board byte-untouched** | **PASS** |

**W5− is why this twin set means something.** A twin that only shows the new code behaving
cannot tell you the defect was ever there; this one reconstructs the pre-amendment write
literally and shows lane A's declaration absent afterwards, then shows it surviving under
the new one. **Reproduced, then dead.**

**W4 is the row this could most easily have failed.** Every `.hip-scope` in the estate
today is hand-written, with comments and bare prefixes and **no markers at all**. A build
that understood only its own format would have erased all of it on first contact —
**landing the fix by committing the exact defect it repairs.**

### TWO DEFECTS IN MY OWN FIRST CUT — caught by the fail-closed checks, recorded in the code

1. **The marker separated key from message with a pipe.** But a lane key **is** a board row
   prefix and therefore **contains pipes**, so every key truncated to the empty string and
   no block ever matched its own lane. **VERIFY 1a caught it on the first run** — the
   round-trip check doing exactly the job it exists for. Keys are bracketed now, and the
   reasoning is in the source so the next person choosing a delimiter does not choose that
   one.
2. **The neighbour-survival check asserted EQUALITY** of the lines outside my block. Wrong
   in one direction: creating the file adds a header that legitimately was not there
   before. What *"widens, never replaces"* forbids is **losing** a line, so it is now a
   **subsequence** check — nothing lost, in order.

**Both were caught by the mechanism rather than by review**, which is the argument for
building the verification into the write instead of beside it.

**Reasoned about — not independently executed:**
- That the union semantics leave `scope_guard.sh` unchanged in behaviour. It follows from
  the guard reading non-comment lines and the markers being comments; **the guard itself
  was not re-run against a multi-block file in this dispatch** — the twin asserts the union
  the guard would compute, not the guard computing it.

---

## HASH

| commit | what |
|---|---|
| `c9e836b` | board claim — **and the last time the old write replaced this file** |
| `cf04036` | **REQ Amendment 6 — before code** |
| `d9c223f` | the widening write, the close-narrow, and 7 twins |
| *(this commit)* | dispatch doc, INDEX |

---

## OPEN

1. **The estate's existing `.hip-scope` files are still in the legacy format.** They are
   preserved, not migrated — the first claim in each worktree will append a block beside
   the hand-written lines. **Nothing needs doing**; noted so the mixed shape reads as
   expected rather than as a bug.
2. **`~/hip-roadmap/.hip-scope` holds FM 38's own claim in the OLD replaced form**,
   because it was written by the pre-fix code at `c9e836b`.

   > **CORRECTED AFTER THE CLOSE RAN — the prediction above was wrong, and the old wording
   > is kept visible rather than patched.** This item first read *"this dispatch's close
   > will narrow it under the new code — the first live exercise of the narrow path."*
   > **It did not narrow it, and that is the correct behaviour.** The file is in the legacy
   > format and carries no attributed block for this lane, so `_narrow` found nothing of
   > its own to remove and left every line exactly as found — W4 preserving legacy content
   > verbatim, working. **So the narrow path is proven by twin W3 and has NOT yet run live**,
   > and the file will stay in its legacy shape until the next claim in this worktree
   > appends a block beside it.
3. **Not measured: `scope_guard.sh` executed against a real multi-block file.** The twin
   computes the union the guard would see; it does not run the guard. A follow-up could
   close that gap cheaply.
4. **Attribution is only as good as the lane key.** Two dispatches sharing one board row —
   which happens on this board — share one block. Named, not solved.
