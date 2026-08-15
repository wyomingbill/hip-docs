# DISPATCH_LOCK_AND_GRAPH_BUILD
Status: BUILT
Reconciled-Against: 2026-08-03 (D-146 build; parent `0e0673f`, the D-146 survey)

**TYPE:** BUILD

**REQ:** `REQ_LOCK_ENFORCEMENT__td148-enforce-lock-and-separate-graphs__v20260803_2047.md`
— requirement 1 (lock enforcement) and requirement 2 (graph separation).
**NOTHING IS RULED MET.** The REQ stays PLAN/NOT MET; this dispatch reports readiness
against its acceptance items and names precisely what it does not reach.

## WHAT I PICKED, AND WHAT I REJECTED

### Axis 1 — lock enforcement: **A2 (a real mutual-exclusion primitive)**, resource-keyed

**Picked A2** because Bill's constraint decides it: *"Lock acquisition must be a
precondition of the tooling, not a step a session can reorder — late-take has now happened
twice."* A1 and A3 both leave acquisition as a step. A2 is the only option the survey
itself says "converts advisory into enforced in the literal sense of Bill's ruling text."

**Rejected A1 (atomic noclobber + PID/heartbeat)** — it is TD-148's own scoped shape and it
is not enough: by the survey's own table it does **not** stop D-107's write-through, which
is the failure that actually cost this project a lane's work. A marker file cannot refuse;
it can only report. Its two real wins (no blind clobber, no timestamp drift) are subsumed
here — the flock cannot be clobbered, and liveness is the descriptor rather than a string
anyone must refresh.

**Rejected A3 (git hook)** — `--no-verify` bypasses it, it fixes no drift, and it guards
only git. The harness writes the graph without touching git at all.

**One correction to A2 as surveyed, and it is the thing that makes it work: the lock is
keyed on the RESOURCE, not the checkout.**

    repo          one lock per REPOSITORY, shared by every worktree of it
    graph:<port>  one lock per Neo4j PORT, shared by every checkout pointed at it

A per-checkout `.hip-lock` could express neither relationship, and that is precisely how
two sessions could each believe they held "the lock" and still collide: they held different
files, and the thing they were contending for — one INDEX, one graph — was a third thing
neither file named. Worktrees are the sharp case: `~/hip-roadmap` and every `~/hip-roadmap-*`
worktree share one `docs/INDEX.md`, and now share one `repo` lock.

**Built:** `scripts/hip_lock.py` — `fcntl.flock` held on a descriptor for the lifetime of
the guarded child process. (`flock(1)` does not exist on macOS; I discovered that by running
it, not by assuming, and rewrote the shell draft in Python for the same primitive.) Refusal
exits **75/EX_TEMPFAIL**, distinguishable from the guarded command's own failure. Holder
metadata is written as a *report* — never as the lock, so a stale `.holder` can neither
grant nor deny anything.

**Made a precondition, not a step:** `scripts/run_harness.sh` now **re-execs itself** under
`hip_lock.py with graph:<port>` when `HIP_LOCK_HELD` does not already name that graph. A
session cannot run the harness without the lock, cannot take it late, and cannot forget —
there is no ordering left to get wrong. Proven live: the run's first two lines are
`[hip_lock] acquiring graph:7688` then, after re-exec, `[hip_lock] holding graph:7688`.

Keyed on the **graph**, deliberately not the repo: the harness's contended resource is the
Neo4j instance. The 7690 demo-cutover lane and the 7688 roadmap lane therefore never block
each other, which the REQ's CONSTRAINTS require.

### Axis 2 — graph separation: **B4 (fail-closed target resolution + per-checkout pin)**

**Picked B4** because Bill's other constraint decides it: *"an unconfigured checkout must
FAIL, never silently fall back to 7687."* That is a statement about what the CODE does when
configuration is absent, and no amount of infrastructure answers it.

**Rejected B1 (one Neo4j per lane)** — the REQ's own CONSTRAINTS carry TD-129's measured
0.07 GB free at the moment a second instance was assessed; four JVMs already run. B1 also
would not have satisfied Bill's constraint: a lane with a dedicated instance and an
unconfigured environment still silently fell through to 7687.

**Rejected B2 (logical separation)** — prior banked research says Community edition is
single-database, so it may not be buildable at all, and it would be a change at every query
site rather than one authority.

**Rejected B3 (retire dormant lanes) as an ACTION, kept as a recommendation** — it is
`git worktree remove` against five checkouts I do not own, which is a destructive write and
explicitly not pre-authorized. Recommended in OPEN; not performed.

**Built:** `harness/graph_target.py`, one authority with two fail-closed layers.
Layer 1: `NEO4J_URI` unset **raises** — there is no default parameter and no reachable
"just use the default" path; the absence of a default is the feature, and the message names
7687 and explains that it is an unowned instance rather than merely reporting "unset".
Layer 2 (opt-in per checkout): a `.hip-graph` pin file naming the expected port, so a
correctly-running lane pointed at the wrong graph by an inherited environment is refused —
generalising D-108's proven C2 guard from one lane to any checkout that drops the file.
This checkout is pinned to 7688. **The pin is UNTRACKED and gitignored on purpose:** a
tracked pin would follow every worktree and refuse the 7690 lane, breaking a working lane
to fix a different one.

**The rewiring, and the problem it surfaced.** Removing the module constant broke ten
`from harness.extraction_queue import NEO4J_URI` sites across the tree (caught by running
the harness, which failed at `fixture.py:294`). Rather than churn ten call sites mid-build,
both modules now resolve the name through **PEP 562 module `__getattr__`** — every existing
import keeps working, and none of them can reach a silent default any more. Verified both
directions: configured → `bolt://localhost:7688`; unconfigured → `GraphTargetError`.

## ACCEPTANCE — `eval/test_lock_and_graph_separation.py`, 10 cases, 24th standing battery

**Item 1 (lock enforcement, D-107 reproduced):** `test_lock_concurrent_take_is_refused_by_the_kernel`
spawns a real second process against the held resource. It is **refused with exit 75** and
never reaches its write. Asserted on the child's actual exit code and the absence of its
output — not on a message.

**Item 2 (lock timing):** partially met, honestly. `test_lock_is_a_precondition_of_the_harness_runner`
asserts the runner re-execs under the lock, so the harness path cannot be entered
lock-less. **The REQ's stricter reading — the lock held before the first READ of any
governed file — is NOT met for arbitrary reads; see OPEN.**

**Item 3 (graph separation):** unset-URI refusal; pin-mismatch refusal; a source tripwire
asserting no module carries a `7687` default again.

**Executed fault twin:** the OLD resolution shape is run in-test and shown to ACCEPT an
unconfigured environment and yield 7687 — the defect demonstrated, not described.
**Anti-vacuity:** a correctly-pinned checkout resolves normally (without it, the refusal
cases would pass for free); and the source tripwire was itself proven to still SEE a
reintroduced default (a probe module was added, the check went RED, the probe was removed).
**Self-caught:** that tripwire's first run failed on my own explanatory COMMENT quoting the
old line — fixed to skip comments, with the incident recorded in the check.

Lane-independence is asserted too: holding `graph:7688` does not block `graph:7690`.

## EVIDENCE

- **Battery: 10/10.** Standing batteries **400 passed, 8 xfailed** (up from 390).
- **`--layer 7`: L7 27/27**, L7V2 27/28 (one opt-in skip), **AUDIT 8/8**, four-part-roster
  PASS, COVERAGE-GRID-RATCHET PASS, **RATCHET PASS — no scenario regressed.**
- **Six ABSOLUTE checks individually: OB6 · G0 · PSA1 · CTX-STRIP · LI1 · CS1 — all PASS.**
- **The lock proved itself in the real run**, not only in tests: `acquiring graph:7688` →
  re-exec → `holding graph:7688`.
- **Memory harness: 13/17**, failures exactly {MEM-115, 116, 117, 118} — identical to
  D-145's two readings, **inside the 13–15/17 pin, not the 16/17 STOP**, at the floor. This
  dispatch did not change it in either direction; the D-145 finding stands unaltered.

## WHAT THIS DOES NOT DO — stated plainly

- **It does not make bypass impossible.** A `git commit` typed directly, or a script that
  never calls `hip_lock.py`, is still unguarded. The survey's honest limit holds: enforcement
  reaches exactly as far as the write paths that route through the wrapper. The harness now
  does; git does not.
- **It does not separate the three checkouts that share 7688** (`~/hip-roadmap`,
  `~/hip-roadmap-crypto-p2`, `~/hip-roadmap-stage1-wip`). It makes them **serialise** on the
  graph lock rather than corrupt each other, and makes a misconfigured one refuse — but
  "SHALL NOT share one graph" is not satisfied by serialisation, and I am not claiming it is.
- **It does not touch `~/hip-vo`'s deliberate 7689 sharing** with the frozen demo, or the
  frozen demo itself.
- **Nothing is ruled MET.**

## PROCESS NOTES

- **Lock taken FIRST this time** — read-first then noclobber, before any edit, at 21:04:55.
  D-114 and D-145 both took it late; that is the failure this build exists to make
  impossible, and it would have been absurd to repeat it while fixing it.
- Repo `.env.dev` only. The cutover lane's WIP (dirty `docs/INDEX.md` rows, four untracked
  dispatch docs) untouched; explicit pathspecs and a surgical INDEX stage; verified after.
- `.hip-graph` written locally and gitignored — no other checkout is affected.

## OPEN

- **Item 2's strict reading** (lock before the first READ of a governed file) needs either a
  read-path wrapper or a git hook; A3 was rejected as a primary mechanism but is the natural
  complement here, and `--no-verify` remains its ceiling.
- ~~**B3 recommended, not performed**~~ — **DONE, same day, on Bill's explicit
  authorisation. See the ADDENDUM below.**
- The `.hip-lock` marker file still exists and is now redundant with `hip_lock.py`. Retiring
  it needs a decision about the sessions and docs that still reference it.
- MEM-115/116/117/118 at the pin floor — unchanged here, still D-145's open finding.

---

## ADDENDUM — B3 EXECUTED (Bill's authorisation, 2026-08-03, same day)

The body above rejected B3 as an action because retiring checkouts is a destructive write
against lanes this session does not own. Bill then authorised it explicitly, with a
condition: *"Confirm each is dormant before you remove it."*

**Dormancy confirmed per checkout BEFORE removal — not asserted from the survey's claim:**

| Checkout | Branch | Uncommitted | Last commit | Live processes |
|---|---|---|---|---|
| `hip-roadmap-crypto-p1` | `roadmap-crypto-p1` | 0 | `2477dbe`, 2026-07-20 | none |
| `hip-roadmap-crypto-p2` | `roadmap-crypto-p2` | 0 | `1e549a8`, 2026-07-20 | none |
| `hip-roadmap-stage1-wip` | `roadmap-stage1-wip` | 0 | `cd815f6`, 2026-07-20 | none |
| `hip-ungoverned` | `demo-ungoverned-knowledge` | 0 | `f8194be`, 2026-07-22 | none |
| `hip-vo2` | **detached HEAD** | 0 | `ef99a57`, 2026-07-23 | none |

`git status --porcelain` counted tracked AND untracked; idle 12–14 days against 2026-08-03;
`pgrep -f <path>` for holders.

**THE ONE REAL HAZARD, checked before it could bite:** `hip-vo2` was on a **detached HEAD**,
which has no branch ref — removing that worktree could have orphaned `ef99a57`. It is
contained in `main`, `voice-port`, `origin/main` and `origin/voice-port`. Every one of the
five tips was verified reachable from other refs INCLUDING `origin/*` both before and after
removal. **Working directories only were removed; no branch was deleted**, so reachability
is belt-and-braces rather than the sole protection.

Removals ran under `scripts/hip_lock.py with repo` — the first non-harness use of the
mechanism this dispatch built.

**WHAT IT CHANGED, and it is more than tidiness.** The survey's *shape-1 collision* —
three checkouts each carrying a committed `.env.dev` pinning **7688** — is now **gone by
SUBTRACTION**, which is strictly stronger than the serialisation the graph lock provides.
`7688` has exactly one configured checkout: `~/hip-roadmap`, additionally pinned by
`.hip-graph`. Verified from each remaining lane's own config: `hip-roadmap`→7688,
`hip-cutover-demo`→7690 (launcher pins `CUTOVER_NEO4J_URI`, deliberately unsets inherited
`NEO4J_URI`), `hip-dev`→7689, `hip-vo`→7689 via `.env.demo`.

**One known sharing survives — `hip-vo` with the frozen demo on 7689 — the by-design case
Bill excluded from scope.** So the body's limit *"it does not separate the three checkouts
that share 7688 … serialisation is not separation"* is now **superseded for 7688
specifically**, and the honest remaining statement is narrower: one deliberate sharing,
excluded by instruction.

**A latent hazard found while verifying, named not fixed:** `.env.demo` is a **TRACKED**
file, so every worktree carries a copy that sources the frozen demo's env in demo mode. My
first port survey tripped over exactly that and reported all four lanes as 7689-bound; the
picture above is the corrected one, taken from each lane's own `.env.dev` and launcher.

**REQ_LOCK_ENFORCEMENT is still NOT MET.** Acceptance item 3 is materially closer for 7688,
but item 1's honest limit (bypass outside the wrapper) and item 2's strict reading (lock
before the first READ of a governed file) are unchanged, and nothing here is ruled.
