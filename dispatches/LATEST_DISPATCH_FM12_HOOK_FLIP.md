# FM 12 — FLIP THE HOOK ENFORCEMENT ON
Status: **STOPPED ON THE PRECONDITION** — `core.hooksPath` NOT set; nothing was changed
Reconciled-Against: 2026-08-14, `~/hip-roadmap` @ `roadmap`. Board claim `00de2ca` / `6450af2`.

REQ: `docs/requirements/REQ_PROCESS_HARDENING_TOOLS__claim-lane-register-doc-lane-preflight-scrub__v20260814_1613.md`
(FM 9). This dispatch is the enable step that REQ's acceptance E1 reserves; no new code.

---

## 0. THE EXCEPTION LINE

```
FM 12 — FLIP THE HOOK ENFORCEMENT ON
STOPPED AT SEGMENT 1 — NEEDS BILL
```

**The dispatch's own precondition was checked first and it FAILED, on three independent
counts. `core.hooksPath` was not set. Nothing on this machine was changed except this
dispatch's two board rows.**

> *"Precondition, check first: no battery or dispatch mid-run in any of the five worktrees
> (VD-62 must be landed). If anything is mid-run, STOP and say so."*

Saying so.

---

## 1. THE PRECONDITION, MEASURED — THREE FAILURES

### 1.1 A BATTERY IS RUNNING RIGHT NOW, AND IT IS THE CANONICAL ONE

```
PID 2827   started Fri Aug 14 16:25:26 2026   elapsed 08:55 at the time of this write
  command : python -u scripts/demo_integrity_battery.py
  cwd     : [REDACTED-USER-PATH]/hip-cutover-demo
  env     : BATTERY_RUNS=20   NEO4J_URI=bolt://localhost:7690
  socket  : TCP 127.0.0.1:55730 -> 127.0.0.1:7690  (ESTABLISHED)
```

This is not an idle process that happens to be named like a battery. **It holds a live bolt
connection to the demo graph and it is the canonical lane test** — the one `CLAUDE.md` on
`demo-cutover-build` defines as *the* command, the one that resets and re-seeds 7690.

**It is roughly a third of the way through.** `BATTERY_RUNS=20` at the documented ~92 s per
iteration is **~31 minutes**; at 8:55 elapsed that leaves **~22 minutes**. The same `CLAUDE.md`
warns in capitals that this duration *"IS NOT A HANG"* — so a long-running battery is the
expected shape, not a stuck process I could reason away.

### 1.2 VD-62 IS OPEN ON THE BOARD

`docs/LANES.md`, Demo lane: **`VD-62 IN FLIGHT`**. The dispatch's precondition names this
directly — *"VD-62 must be landed"* — and it is not landed. NUMBER-CLAIM LAW obligation 3 is
explicit that **a row left open is indistinguishable from a dispatch still running**, so an
open row is a stop in its own right even without §1.1.

### 1.3 VD-62 HAS A COMMIT THAT IS NOT PUSHED

```
~/hip-cutover-demo   ## demo-cutover-build...origin/demo-cutover-build [ahead 1]
  d0282bd  08-14 16:25  VD-62: gate the three open read endpoints, close /openapi.json,
                        unregister /ws/voice by default; route-inventory test
                        — REQ_DEMO_ENDPOINT_CLOSURE
```

Committed at 16:25 — **the same minute the battery started** — and still unpushed. That is a
lane in the middle of its evidence loop: code landed locally, canonical battery running to
certify it, push to follow.

### What DID pass

For completeness, because a partial precondition check is worse than none:

| check | result |
|---|---|
| `repo` lock | free |
| `graph:7687` … `graph:7692` locks | all free |
| other lanes' rows | FM 10 LANDED, NC 6 LANDED, HA-74 CLOSED, ML-02 LANDED, Voice IDLE |
| HA-85 | not "in flight" — awaiting Bill's paste, no process |

**The locks being free is exactly why the process check matters.** `hip_lock.py` guards git
operations and graph ports on request; **a battery does not have to hold a graph lock to be
mid-run**, and this one does not. A precondition answered from the lock table alone would have
returned "all clear" and been wrong.

---

## 2. WHY THIS PARTICULAR FLIP MUST NOT HAPPEN DURING THAT PARTICULAR RUN

The stop is required by the dispatch regardless. But the reason it is a *good* rule here is
worth stating, because it is specific rather than generic caution:

**`core.hooksPath` changes commit behaviour in all five worktrees the instant it is set.**
VD-62's next action, when its battery finishes in ~22 minutes, is to commit and push its
evidence. Setting the hook now means **that commit runs through a dispatcher it has never run
through, installed mid-dispatch by another lane, at the exact moment it is recording a
20-iteration result it cannot cheaply re-run.**

The dispatcher is built to be safe — it chains to any existing per-worktree hook, fails CLOSED
only on a policy violation and OPEN with a warning on an infrastructure problem (FM 9 §5). But
"designed to be safe" and "proven safe in this tree, in this state, right now" are different
claims, and the second is the one that matters when the cost of being wrong lands on somebody
else's 31-minute run.

**There is also nothing to gain by rushing it.** The hook has been built, committed and proven
in both directions since FM 9 (`f6b1e2f`). Twenty-odd minutes changes nothing about it.

---

## 3. WHAT WAS NOT DONE

- **`core.hooksPath` was NOT set.** Verified after the board writes:
  `git -C ~/hip-roadmap config --get core.hooksPath` → **unset**.
- **No commit was made in any worktree other than `~/hip-roadmap`**, and there only this
  dispatch's own board rows, written by `claim_lane.py` (board-only, under the repo lock).
- **The running battery was not touched, signalled or interfered with.** Reading `ps`, `lsof`
  and the process environment is passive.
- **VD-62's unpushed commit was left exactly where it is.** It is that lane's to publish.
- **The two proof commits the dispatch asks for were not attempted** — they are the segment
  that depends on the flip.

---

## 4. WHAT RUNNING THIS LOOKS LIKE WHEN THE PRECONDITION CLEARS

No re-derivation needed next time. The precondition is three checks, and all three must be
green **at the moment of the flip**, not earlier in the session:

```sh
# 1. no battery / harness / gate mid-run, in ANY worktree
ps -Ao pid,etime,command | grep -iE "demo_integrity_battery|eval\.harness|injection_harness|gate_check|pytest" | grep -v grep
# 2. the board carries no IN FLIGHT row, and VD-62 in particular is LANDED
# 3. no worktree is ahead of its remote
for t in hip-dev hip-cutover-demo hip-roadmap hip-vo hip-nc; do git -C ~/$t status -sb | head -1; done
```

Then the flip, and the two proofs the dispatch specifies — one clean commit allowed, one
policy-violating commit refused with `HEAD` unmoved, **in a real worktree** (the shared hook's
whole point is that it fires where no local hook exists, so the proof belongs in a worktree
other than `~/hip-roadmap`).

### THE ROLLBACK LINE, PRINTED AS ASKED

```sh
git -C ~/hip-roadmap config --unset core.hooksPath
```

And the enable line it undoes:

```sh
git -C ~/hip-roadmap config core.hooksPath [REDACTED-USER-PATH]/hip-roadmap/scripts/hooks
```

---

## 5. FILED, NOT BLOCKING (2), AND ONE THING REPAIRED

**(FM12-1) The lock table cannot answer "is anything mid-run", and this dispatch is the
demonstration.** Every one of the seven lock resources reported `free` while a 20-iteration
canonical battery held an established bolt connection to 7690. `hip_lock.py` is correct — it
locks what a caller asks it to lock, and the battery never asked. **But a session that reads
"all locks free" and concludes "nothing is running" will be wrong exactly when it matters
most**, which is the shape of every incident in this project's register. The honest answer is
that mid-run detection currently requires a process scan, and no tool does it. `lane_preflight.py`
is the natural home for it. **Named, not built** — the finiteness rule applies, and this
dispatch's job was to stop.

---

**(FM12-2) THE COORDINATOR ROW WAS BROKEN WHILE THIS DISPATCH RAN, AND THE TOOL PRESERVED IT
RATHER THAN CATCHING IT — REPAIRED.** FM 11 claimed at `3b5113a`, between this dispatch's two
board writes, and wrote a shell pipeline into its IN FLIGHT cell:

```
`lsof -ti:7860 | xargs kill -9`
```

**A bare `|` inside backticks still splits a markdown table cell.** The FABLE MASTER row went
to six columns against a five-column header and rendered wrong for every reader of the board.
Repaired at `2b8e9b8` by escaping it — `\|` — with FM 11's text otherwise untouched and its
meaning unchanged.

**Two defects in `claim_lane.py` fell out of it, both fixed at `f67db5c`, twins re-run green:**

1. **It rejected ANY pipe in a replacement**, so it could not write an escaped `\|` at all —
   legitimate cell content. It now counts only UNESCAPED pipes.
2. **It asserted the column count was UNCHANGED, not CORRECT.** That is worse than it sounds:
   an "unchanged" invariant faithfully preserves a break another dispatch introduced, *and*
   refuses the very edit that would repair it. **The table header is now the authority**, so a
   new break is caught and a repairing edit is allowed and announced.

**The generalisable point, which is FM9-4's lesson arriving from the other direction:** an
invariant that compares a thing to its own previous state cannot tell "correct" from
"consistently wrong". FM 9 wrote that check; two dispatches later it protected a broken row.

---

## 6. CLAIM IMPACT

```
CLAIM IMPACT: none
```

---

## 7. NEEDS BILL

**Re-issue when the precondition clears.** Nothing else is outstanding: the hook is built,
committed and proven; only the flip and its two live proofs remain, and they take a minute.

The clearing condition is concrete rather than a judgement call: **VD-62's battery finishes,
that lane pushes and closes its row, and no other lane has started something.** The battery was
~22 minutes from done at 16:34.

---

## 8. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `~/hip-roadmap` @ `roadmap`.
- **The battery was re-checked immediately before this document was written** — still running,
  still holding one established connection to 7690 — so the stop rests on a live reading, not
  on one taken at the top of the dispatch and assumed to hold.
- `core.hooksPath` confirmed **unset** after all board writes.
- Board: FM 12 claimed at `00de2ca` and `6450af2`, both `docs/LANES.md`-only, both written by
  `claim_lane.py` under the repo lock with the passenger gate armed.
- **FM 11 was recorded as a gap and then appeared.** When FM 12 claimed, the board's last
  issued number was FM 10, so the row noted FM 11 as never having reached it — the same way
  FM 7 and FM 8 were. **FM 11 then claimed at `3b5113a`, minutes later, with its own commit
  message saying "claimed after FM 12".** The gap note is therefore stale the moment it was
  written, and is corrected here rather than left to mislead: **FM 11 exists, is IN FLIGHT
  (plist credential rotation), and was claimed after this dispatch, not skipped.**
