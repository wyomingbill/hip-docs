# HIP DEVELOPMENT OPERATING MODEL
Status: BUILT
Reconciled-Against: `roadmap` @ FM 2's commit, 2026-08-14

**Authority:** Bill's FM 2 dispatch, 2026-08-14. This document is the operating model itself, not a
proposal for one. **It describes how work is coordinated; it rules nothing MET and changes no
requirement.** Where it restates a rule that lives in `CLAUDE.md`, `CLAUDE.md` governs.

**Predecessor state:** FM 1 (`5a27a1a`) searched `docs/` and found **no operating-model document,
no coordinator checkpoint, no worker board and no review queue**. The only coordination instruments
were `docs/LANES.md`, `docs/HIP_HANDOFF.md` and `CLAUDE.md`. This is the first.

---

## 1. TOPOLOGY

```
                            ┌──────────────────────────────────────┐
                            │  BILL                                │
                            │  product · architecture · policy     │
                            │  priority · go/no-go rulings         │
                            └───────────────┬──────────────────────┘
                                            │  dispatches, rulings
                                            ▼
                            ┌──────────────────────────────────────┐
                            │  FABLE MASTER  (coordinator chat)    │
                            │  single canonical coordination point │
                            │  ALL dispatches originate here       │
                            └───┬───────┬───────┬───────┬──────────┘
                                │       │       │       │
              ┌─────────────────┘       │       │       └─────────────────┐
              ▼                         ▼       ▼                         ▼
      ┌───────────────┐        ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
      │ CC-1  BUILD A │        │ CC-2  BUILD B │  │ CC-3  VERIFY  │  │ CC-4  FLEX    │
      └───────┬───────┘        └───────┬───────┘  └───────┬───────┘  └───────┬───────┘
              │                        │                  │                  │
              └────────────┬───────────┴──────────────────┴──────────────────┘
                           ▼
              ┌────────────────────────────┐
              │  IMPLEMENTATION EVIDENCE   │
              │  commits · runs · docs     │
              └────────────┬───────────────┘
                           ▼
              ┌────────────────────────────┐
              │  FABLE MASTER reconciles   │
              └────────────┬───────────────┘
                           │  at gates only
                           ▼
              ┌────────────────────────────┐
              │  ChatGPT independent review│
              │  HIP_REVIEW_<cap>_<HEAD>.zip│
              └────────────┬───────────────┘
                           ▼  findings
              ┌────────────────────────────┐
              │  FABLE MASTER reconciles   │
              └────────────┬───────────────┘
                           │  DISAGREEMENT ONLY
                           ▼
                        ┌──────┐
                        │ BILL │
                        └──────┘
```

**Roles are stable; assignments are temporary.** `CC-1 BUILD A` is a seat, not a subject-matter
owner. A worker's lane, checkout and branch come from its dispatch, not from its seat name.

**What each edge carries:**

| edge | carries | never carries |
|---|---|---|
| Bill → FABLE | dispatches, rulings, priority | implementation detail Bill has not asked to see |
| FABLE → CC-n | capability dispatches (§4) | ad-hoc scope Bill gave FABLE but FABLE has not reconciled |
| CC-n → evidence | commits, runs, dispatch docs, board rows | claims of MET; a worker never rules |
| evidence → FABLE | the reconciled position | — |
| FABLE → ChatGPT | primary evidence at gates (§6) | FABLE's own summary in place of the evidence |
| findings → FABLE | review findings | a verdict FABLE must accept unexamined |
| FABLE → Bill | **disagreement only**, plus §7's alert classes | routine progress |

**Only Bill rules.** ChatGPT reviews, FABLE reconciles, workers build and report. **Status is
computed from standing evidence, never declared by a session** — the claims ledger's governing rule,
unchanged by this document.

---

## 2. COMMAND RULE — one coordination point

**All dispatches originate in the FABLE MASTER chat.** There is exactly one coordination point at a
time.

**Old chats are REFERENCE ONLY.** A prior chat's context, plans and numbering are historical. A
session must not take a number, a scope, or an instruction from an old chat's scrollback — the
board issues numbers (`CLAUDE.md` NUMBER-CLAIM LAW), and the current dispatch issues scope.

**Direct Bill-to-worker scope changes are legitimate and expected.** Bill may tell a worker
something directly at any time. When that happens:

> **The change is reconciled into FABLE state BEFORE dependent work continues.**

The worker records it, reports it to FABLE, and FABLE lands it in the checkpoint (§3) and the board.
Work that does not depend on the change proceeds meanwhile. **Work that does depend on it waits for
the reconciliation** — not for Bill to repeat himself.

**Why:** a scope change known to one worker and not to the coordinator produces two divergent plans
that both believe they are current. That is the same failure class as a number claimed from chat
memory, and it is what the board exists to prevent.

### 2a. STAGING DISCIPLINE ON SHARED FILES — now enforced by tooling

`docs/LANES.md` and `docs/INDEX.md` are written by every lane. `CLAUDE.md` STANDARD PREAMBLE item 2
requires **surgical staging** on them: save the union copy, reset the file to HEAD, apply only your
own rows, `git add`, restore the union.

**On 2026-08-14 that rule was broken three ways in one morning** — HA-66's duplicate number, two
`--full` runs colliding on memory, and (FM 1 FINDING 10) a plain `git add docs/LANES.md` that swept
FM 1's *uncommitted* board row into HA-78's commit. **A rule that is only remembered is not a
control.** FM 2 therefore installs a **STAGING GUARD** (§2b) that refuses the unsafe commit shape.

### 2b. The staging guard

`scripts/staging_guard.sh`, invoked by `.git/hooks/pre-commit` in this worktree.

**It refuses a commit when BOTH hold:**
1. the staged set includes `docs/LANES.md` or `docs/INDEX.md`, **and**
2. the staged set includes **any other path**, **and**
3. the commit is **not** running under the repo lock (`HIP_LOCK_HELD` is absent).

Board-only and INDEX-only commits always pass. Mixed commits pass **only** under the lock, because
the lock is what makes "no other lane is mid-edit" true rather than hoped. Bypass is
`HIP_STAGING_GUARD=off` (or `git commit --no-verify`), which is deliberate: the guard stops the
accident, it does not fight the operator.

**Twin results — tested in BOTH directions, six cases, in a throwaway repo so nothing real was at
risk:**

| # | staged | lock | expected | result |
|---|---|---|---|---|
| 1 | `docs/LANES.md` alone | none | pass | **PASS** |
| 2 | non-board file alone | none | pass | **PASS** |
| 3 | `docs/LANES.md` + other | **none** | **refuse** | **REFUSED** |
| 4 | `docs/LANES.md` + other | `repo` | pass | **PASS** |
| 5 | `docs/INDEX.md` + other | `graph:7688` only | **refuse** | **REFUSED** |
| 6 | same as 5 | none, `HIP_STAGING_GUARD=off` | pass | **PASS** |

**And then proven on the live repository, on FM 2's own closing commit** — the same staged set both
ways, which is the strongest form of the twin because the payload was real work, not a fixture:

| direction | staged | lock | result |
|---|---|---|---|
| **RED** | `docs/INDEX.md` + 6 other paths | none | **REFUSED**, `HEAD` unchanged at `57ce2d4`, **no commit created** |
| **GREEN** | *identical staging* | `repo` | **PASSED** → `d7a4886` |

Commit ledger confirmed: `base, c1, c2, c4, c6` exist; **`c3` and `c5` were never created.** Case 5
is the one worth naming — **a graph lock does not authorise a mixed board commit**, because only
`repo` serialises the lanes that contend for these files, which is `hip_lock.py`'s own stated
purpose for it.

**Two mechanics stated exactly, because "exit 76" would otherwise be a false expectation:**

- The guard's **own** exit code is **76**. **Git reports `1`** to the caller when a pre-commit hook
  fails — git does not propagate hook exit codes. The refusal message on stderr is the diagnostic,
  not the number.
- The lock is detected via **`HIP_LOCK_HELD`**, which `hip_lock.py` already sets in the guarded
  command's environment and documents as existing *"so tooling underneath can VERIFY it is running
  under the lock rather than trusting that someone took it."* This guard is that tooling; no new
  mechanism was invented.

**KNOWN LIMITS — stated so no one trusts it further than it goes:**

1. **`~/hip-dev/.git/hooks` is SHARED BY ALL FIVE WORKTREES**, not per-worktree. An unscoped hook
   there would have silently changed every lane's commit behaviour mid-flight — including refusing
   the ordinary "dispatch doc + INDEX + board row" commit that lanes make routinely. FM 2 was scoped
   to the roadmap tree, so the installed hook is a **dispatcher that no-ops everywhere except
   `~/hip-roadmap`** (verified: it exits 0 in `hip-cutover-demo`, `hip-nc`, `hip-vo` and `hip-dev`).
   **Widening it to another lane is a change to that lane's behaviour and needs that lane's or
   Bill's say-so** — not a unilateral edit by whoever touches the file next.
2. **Hooks are not version-controlled.** This guard exists on this machine only. A repo-wide,
   durable answer needs `core.hooksPath` pointing at a tracked directory — named here as the real
   engineering answer, **deliberately not taken by FM 2** because it changes every lane at once.
3. **The guard stops a COLLISION; only surgical staging stops you committing another lane's rows.**
   Under the lock, a plain `git add docs/LANES.md` still stages whatever else is in that file. The
   guard makes the unsafe shape loud; it does not make item 2 optional.

---

## 3. CHAT IS THE CONTROL ROOM; THE REPO IS TRUTH

**No state lives only in a chat.** Anything that must survive is in the repo: the board
(`docs/LANES.md`), lane state (`docs/HIP_HANDOFF.md`), dispatch docs, requirements, registers, and
the coordinator checkpoint (`docs/general/LATEST_FM_CHECKPOINT.md`).

**On loss of the FABLE MASTER session, recovery is a READ, not a reconstruction.** In order:

1. `docs/general/LATEST_FM_CHECKPOINT.md` — worker assignments, active capabilities, open decisions
2. `docs/LANES.md` — who holds which number, what is in flight, what is closed
3. `docs/dispatches/` — the most recent docs, by mtime, with their Status lines
4. **git state** — `git worktree list`, per-branch `ahead/behind`, `git log` on each active branch
5. `docs/HIP_HANDOFF.md` CURRENT STATE — gates in force and pending Bill decisions

**Never reconstruct coordination state from memory or from an old chat.** FM 1 is the worked example
of what a machine-read reconciliation produces and how far it can be trusted; its own record shows
the board moving four times during a single read, which is precisely why memory is not admissible.

**A successor reads the machine, then says what it could not establish.** `UNKNOWN — <why>` is an
answer; a guess is not.

---

## 4. CAPABILITY DISPATCHES, NOT MICRO-DISPATCHES

A dispatch delegates a **capability**, not a keystroke. Every dispatch carries these fields:

| field | what it fixes |
|---|---|
| **Objective** | the capability in one sentence |
| **Contract** | the behaviour that must hold when it is done |
| **In scope** | what this dispatch may change |
| **Out of scope** | what it must not touch, named explicitly |
| **Interfaces** | the seams it may use or must preserve |
| **Acceptance** | the evidence that closes it — runs, not assertions |
| **Required tests** | which suites, at which tier (§8) |
| **Destructive boundaries** | what it may never delete, reset, or rewrite |
| **Review requirement** | which gate(s) of §6 apply |
| **Stop conditions** | the list below, and nothing else |

### Workers stop for exactly five things

1. **Product decisions** — what the product should do.
2. **Security or privacy policy** — anything that changes what is protected or from whom.
3. **Architecture expansion beyond the dispatch** — the fix requires a structure the dispatch did
   not authorize.
4. **Destructive ambiguity** — a required step might delete, reset, or rewrite something and the
   dispatch does not clearly authorize it.
5. **Capability-boundary violation** — the work cannot be done without changing something the
   dispatch put out of scope.

**Routine engineering inside scope does not stop.** Choosing a data structure, naming a function,
adding a test, refactoring within the seam, fixing a bug the dispatch implies — these are the
worker's to make and report, not to ask about.

**This is the FINITENESS RULE's operational form** (`CLAUDE.md` item 12): *a finding does not
automatically become the next task; it becomes immediate work only if it blocks the current phase's
acceptance criteria. Everything else gets filed and stays filed.* A worker that files and continues
is obeying the model. A worker that chases an adjacent defect is not.

---

## 5. PREFLIGHT EXCAVATION

**Before any major build, a read-only dependency survey runs first.** No code changes, no service
starts, no graph writes. It answers, with file and line:

- **entry points** — what actually calls into this area
- **consumers** — who depends on its current behaviour, including tests and demo paths
- **config sources** — every place a value can come from, and which one wins
- **auth boundaries** — where a principal is established, carried, or lost
- **egress** — every path that leaves the device, and what gates it
- **tests that actually execute** — distinguished from tests that are collected, skipped, shadowed
  or xfailed

**Why the last one is its own bullet:** TD-V-019 found **80 shadowed tests** that were collected and
never executed. A survey that counts test files instead of executed tests measures nothing.

**The survey's output is a dispatch input, not a deliverable to defend.** It exists so the build
dispatch can name real seams instead of guessing at them.

---

## 6. REVIEW GATES

Three gates. Each names who reviews, on what evidence, and what the possible outcomes are.

### DESIGN gate — before major architecture

Runs before building, when the shape is still cheap to change. Evidence is the design doc and the
preflight survey. Outcome: proceed, revise, or escalate to Bill.

### CODE gate — after integration, before closeout

**Mandatory when the change touches any of:** trust, privacy, consent, identity, memory, egress, or
security. Otherwise at FABLE's discretion.

**ChatGPT receives PRIMARY EVIDENCE**, packaged as:

```
HIP_REVIEW_<capability>_<HEAD>.zip
```

Primary evidence means the code, the tests, and the run output — **not FABLE's summary of them.** A
reviewer given a summary reviews the summary.

### CLOSEOUT gate

Exactly one of three verdicts, recorded in the dispatch doc and the board row:

| verdict | meaning |
|---|---|
| **CLOSED** | acceptance met on executed evidence; nothing outstanding |
| **CLOSED WITH CAVEATS** | acceptance met; named residue filed as TDs, each with an ID |
| **NOT CLOSED** | acceptance not met; what is missing is named |

### Handling findings

**FABLE may CHALLENGE a finding — with primary evidence.** A review is an input, not a verdict, and
an incorrect finding left standing corrupts the record as surely as a missed defect.

> **FABLE NEVER SILENTLY REINTERPRETS A FINDING AS CLOSED.**

A challenged finding is recorded with the evidence that challenges it, and if the disagreement
survives, it goes to Bill — that is the one thing the topology sends up (§1).

**Precedent this is built from:** the 2026-08-12 code review closed properly, with a closeout
document (`docs/general/CODE_REVIEW_CLOSEOUT__…__v20260813_1955.md` on `main`, `42a6604`) naming the
gate run and the TDs its findings became. That is the shape.

---

## 7. ALERT POLICY (phone)

**Five classes reach Bill's phone. Nothing else.**

1. **Decision required** — work is blocked on a ruling only Bill can make.
2. **Review ready** — a review package is built and needs to be sent, or findings have returned.
3. **Capability complete** — a capability reached CLOSED or CLOSED WITH CAVEATS.
4. **Gate failure** — a review gate returned NOT CLOSED.
5. **Critical runtime or demo failure** — the demo or a live service is broken.

Progress, partial results, interesting findings and routine completions do **not** alert.

**The audible completion alert (`scripts/dispatch_done.sh`) is a separate, weaker mechanism** and
`CLAUDE.md` item 6 states its limits: a session that never calls it, dies, or predates the rule
rings nothing, so **silence proves nothing.** The report is the evidence; the sound is a convenience.

---

## 8. TESTING CADENCE

Three tiers. A dispatch names which apply.

| tier | when | what runs | budget |
|---|---|---|---|
| **Inner loop** | continuously while building | the touched module's tests | **5–10 min** |
| **Capability integration** | when a capability is wired | the **real consumer path**, anti-vacuity checks, fault injection | minutes to tens of minutes |
| **Certification** | before closeout | the aggregate gate; destructive runs **only where authorized** | long |

**Capability integration is where most real defects are caught**, because it exercises the path a
consumer actually takes rather than the path a unit test constructs. **Anti-vacuity is not optional:**
a test that passes because nothing happened is worse than a missing test, since it reports safety.
**Fault injection proves the negative** — the guard refuses, the twin goes red.

### The heavy-suite rule — ONE AT A TIME ON THIS MACHINE

> **`--full`, the memory harness and the layer batteries are HEAVY. Exactly one runs on this machine
> at a time. The coordinator schedules them.**
>
> **A session that finds another heavy run in progress WAITS. It never kills it.**

**This is not a precaution, it is an incident report.** On 2026-08-14 Voice 41's `--full` and
HA-77's `--full` ran concurrently and **OOM-collided**; Voice 41's run was additionally
*"contaminated by the concurrent HA-77 lane's then-uncommitted CORE model swap."* Two lanes ran the
heaviest job in the repo at once and each corrupted the other's result. HA-77's own closing note
records that **nothing arbitrates machine memory across concurrent `--full` runs** — that arbitration
is the coordinator's job, and this is the rule that assigns it.

**Detection is by `ps`, not by lock** — FM 1 found a live `--full` running with `repo` and all five
`graph:` locks reporting free. A session checks for a running harness process before starting one.

---

## 9. SETTLED NATURAL-CONVERSATION PRINCIPLES

Recorded here as settled direction. **These are design principles, not requirements: nothing here is
ruled MET, and FM 1 established that there are no NC REQs — the NC work is an ADOPTED-DIRECTION
design doc.**

1. **Governance before voice activation.** The governed path exists before the voice path uses it.
2. **Typed frames, not query rewriting.** A turn becomes a typed request; it is not paraphrased into
   a new query.
3. **Reauthorize every continuation from zero.** Prior turns supply **semantics, never authority**.
4. **An unresolved reference is a deterministic, pre-model STOP.** Not a guess, not a clarification
   the model invents.
5. **The current principal carries authority; conversation state never authenticates.**
6. **Models propose; the deterministic core commits.**
7. **External inference only via the egress boundary.**
8. **An uncertain memory write DEFERS.**
9. **Unknown durable memory has exactly three dispositions:** a typed governed fact, a restricted
   expiring quarantine, or not retained. **Promotion out of quarantine is a separate governed
   process** — never an upgrade that happens by default.
10. **Authentication strength travels with identity.** A measured tier is evidence that moves with
    the principal, never a label applied downstream.
11. **ASR is an integrity boundary.** Partials never enter governance. Low-confidence names, numbers
    and negations are never silently authoritative.
12. **Barge-in is concurrency.** A cancelled turn never speaks, never writes memory, never creates
    consent, and never becomes common ground.
13. **A voice memory write needs a bound confirmation ceremony — the model's own TTS can never
    satisfy it.**

**Live constraints these interact with, carried from Voice 41 and not to be undone:** the egress
suite is **RED ON PURPOSE** at `server/demo_dashboard.py:2765` (re-adding the `CLIENT_SIDE_MARKUP`
exemption hides TD-V-022, it does not fix it); `SPOKEN_CONFIRM_MIN_CONFIDENCE = 0.55` is a **measured**
placement between an observed mis-hear (0.427) and the observed correct band (0.581–0.846) and moving
it needs a re-measurement, not a preference (TD-V-025); **A1b is not started** and its latency is
deliberately not estimated, per Bill's ruling R-1 *(a) THEN (b)*.

---

## 10. EFFICIENCY METRICS

Tracked to tell coordination overhead from real throughput. **Measured, not estimated; and no metric
here gates anything** — they inform how the model is tuned.

| metric | what a bad number means |
|---|---|
| **Capabilities per week** | the throughput the model exists to raise |
| **Bill interruptions per capability** | dispatches are under-specified, or stop conditions are too broad |
| **Micro-dispatch count** | work is being delegated below the capability level (§4) |
| **Start-to-proof time** | the lag from dispatch issued to acceptance evidence standing |
| **Defects first found at certification** | inner-loop and integration tiers are too weak (§8) |
| **Review findings** | per gate, and how many survive challenge (§6) |
| **Worker idle from coordination** | workers waiting on the coordinator rather than on work |

**A caution that belongs with the metrics:** none of these measures correctness, and a model tuned
to raise throughput while lowering evidence quality would look excellent on every row above. They
are diagnostics for the coordination layer, not a scoreboard for the product.

---

## KNOWN LIMITS OF THIS DOCUMENT

1. **`main` cannot read it.** Like `docs/LANES.md`, this doc lives on `roadmap`; `main` diverged at
   `688386f` and runs an older `CLAUDE.md` with no STANDARD PREAMBLE. **A worker dispatched into
   `~/hip-vo` @ `main` cannot read this operating model or the board that issues its number.** This
   is `docs/LANES.md` LIMIT 1, inherited unchanged, and it is the single largest hole in the model.
2. **The staging guard is one worktree deep** (§2b) and is not version-controlled.
3. **Nothing here is enforced except the staging guard.** Every other rule is a convention a session
   follows or forgets — the same class of mechanism `CLAUDE.md` item 6 warns about for the audible
   alert. The durable answer for the rest is harness-level enforcement, named as the known direction
   and not built here.
4. **This document records a model; it does not prove it works.** Its metrics (§10) have no baseline
   yet.

---

## 11. CO-RESIDENCY — THE ONE-WORKTREE-ONE-DISPATCH INTERIM RULE IS RETIRED

**Bill's ruling, FM 39, 2026-08-15.** Two dispatches may share one worktree. The interim
rule that forbade it is **RETIRED as of this ruling.**

**WHY IT EXISTED, AND WHY IT NO LONGER DOES.** It existed because co-residency could not be
made *safe* — the tooling could neither see a neighbour nor prove the two would not
collide, so the only available answer was "don't". Three dispatches changed what is
available:

* **FM 32** — guards inspect the STAGED payload rather than inferring safety from the
  working tree, so a neighbour's staged row can be detected instead of silently
  overwritten;
* **FM 38** — `.hip-scope` WIDENS rather than replaces, so two lanes in one worktree each
  keep an **attributed** declaration instead of the second erasing the first;
* **FM 39** — the default preflight **reports every co-resident lane and its scope**, and
  refuses on the three things that actually collide: **scope overlap, ambiguous ownership,
  and a staged collision**.

**So the question moved from "is anyone else here" to "would we collide".** Presence is
reported; collision is refused; demonstrated disjoint parallel work is allowed. **A rule
forbidding what the gate now permits would contradict the gate**, which is why the
retirement lands with the ruling rather than after it.

### WHAT A LANE MUST STILL DO

1. **Declare a scope.** Not declaring one is now a BLOCKING condition, not a soft
   preference — you cannot prove disjoint against an unknown.
2. **Stage surgically.** One worktree is one index; the preflight refuses staged shared
   state while a co-resident exists, and `claim_lane.py` refuses a payload that touches
   more than its own row.
3. **Read the co-residency report.** It is printed on the passing path too, precisely so a
   pass never hides who else is in the tree.

### ⚠ THE INTERIM RULE HAD NO WRITTEN FORM IN THIS REPOSITORY — searched, not assumed

`grep` for *one-worktree-one-dispatch*, *one dispatch per worktree* and their variants
across `docs/` returns **nothing but FM 39's own board row and this section**. The rule was
an operating convention carried in practice, never a document. **Recorded so nobody later
hunts for the text being retired and concludes it was lost.**

### QUEUED, NOT DONE

**Debt-register row cleanup stays QUEUED for the next process pass** — the rows that
describe co-residency as a hazard are now partly superseded, and revising them is a
register pass of its own. Named here rather than left to be discovered as drift.
