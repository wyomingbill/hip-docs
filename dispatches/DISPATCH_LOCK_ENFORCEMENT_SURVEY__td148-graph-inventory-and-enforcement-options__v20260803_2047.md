# DISPATCH_LOCK_ENFORCEMENT_SURVEY
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** ANALYSIS (REQ filed per item 8; survey + options proposed; explicitly NO code, per
the dispatch's own item 3 — "No code until Bill rules the shape")

**REQ:** `docs/requirements/REQ_LOCK_ENFORCEMENT__td148-enforce-lock-and-separate-graphs__v20260803_2047.md`
(filed this dispatch, Status: PLAN — no build starts from it yet).

## THE ASK

Dispatch text, verbatim:

```
=== D-146 | ~/hip-roadmap | TD-148: make the lock enforce, and separate the graphs ===
STANDARD PREAMBLE. Lane A.
GOVERNING: TD-148 (ungoverned since filing). This dispatch WRITES THE REQ FIRST from
Bill's words below, then builds. Item 8 of Requirements Discipline applies.

BILL'S RULING, the requirement text: the .hip-lock is advisory and has failed three
ways — written through (D-107), clobbered unread (D-118), and taken late twice (D-114,
D-145). A lock that reports compliance it cannot enforce is worse than no lock. HIP's
dev lanes SHALL NOT share one graph, and lock acquisition SHALL precede any write
including the first read of a governed file.

1. SURVEY read-only, report before building: every lane's checkout, its Neo4j port,
   and whether it shares a graph with another. Name which lanes currently collide.
2. Propose the enforcement shape — options, costs, what each actually stops. Do not
   pick. STOP AND REPORT.
3. No code until Bill rules the shape.
```

## WHAT WAS DONE

1. Gate checked (`bill-ai` / `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]/hip-roadmap` /
   `roadmap`) — matched. Tree confirmed `ahead 0 / behind 0`.
2. Lock read first (absent), taken noclobber: `holder: D-146 (TD-148: lock enforcement + graph
   separation, survey+REQ only)`.
3. Filed the REQ first, from Bill's ruling text verbatim, per item 8 of Requirements
   Discipline and the dispatch's own instruction — `Status: PLAN`, since no shape is chosen and
   no build follows this dispatch.
4. Enumerated every git worktree of this repo (`git worktree list`, 9 results) plus every
   `~/hip-*`/`~/neo4j-*` directory under `$HOME` (broader than the worktree list, to catch
   anything not a worktree of THIS repo) — 17 `hip-*` directories and 3 `neo4j-*` directories
   total, then narrowed to which are actual code checkouts vs. supporting/data directories by
   checking each for `.git` and any env file.
5. Read every candidate checkout's own env file (`.env.dev`, `.env`, `.env.demo`,
   `.env.dev.example`) directly for its `NEO4J_URI` (or lack of one).
6. Cross-referenced against LIVE state, not just config: `lsof -iTCP -sTCP:LISTEN` for every
   port in the 7680-7699 range, and `ps aux` for the underlying Neo4j/Java processes, reading
   each one's `--config-dir` to identify which named instance backs which port.
7. Checked the codebase's own HARDCODED fallback default for `NEO4J_URI` when no env is
   sourced at all (`harness/extraction_queue.py`, `harness/zep_store.py`, and hip-vo's
   `server/demo_dashboard.py`).
8. Read `docs/HIP_HANDOFF.md` in full (created D-137 specifically to carry lane structure) as
   existing prior art — cross-checked its own three-lane framing against this survey's broader,
   disk-based inventory rather than assuming it was exhaustive.
9. Checked each dormant-candidate worktree's last-commit date and uncommitted-file count
   (`git log -1`, `git status --short`) to distinguish currently-live lanes from dormant ones
   with latent-only collision risk.
10. Built the options table for item 2 from the concrete failure modes named in Bill's ruling
    text and this survey's own findings — costed each against what it does and does not stop,
    explicitly not selecting one.
11. Wrote this dispatch doc and the REQ doc.
12. Staged both by explicit pathspec, committed, pushed, released the lock. NO other file was
    touched — item 3's "no code" is honored literally: nothing in `harness/`, `memory_engine/`,
    `eval/`, or `scripts/` changed.

## WHAT WAS FOUND

### The live Neo4j instances (verified via `lsof`/`ps`, not inferred from config alone)

| port | PID | backing config dir | identity |
|---|---|---|---|
| **7687** | 1123 (+ 1058, a `NeoBoot` launcher) | default Homebrew `libexec/conf` — no dedicated `~/neo4j-*` home | **UNOWNED.** No lane's own env deliberately targets this port; it is ALSO the codebase's hardcoded silent fallback (see below) |
| **7688** | 1453 | `~/neo4j-dev/conf` | the roadmap build+governance graph |
| **7689** | 22330 | `~/neo4j-hipdev-demo/conf` | the frozen demo's graph |
| **7690** | 20331 | `~/neo4j-cutover-demo/conf` | the demo-cutover lane's dedicated graph |

### Every checkout, its configured port, and its live/dormant status

| checkout | branch | env source | resolves to | status |
|---|---|---|---|---|
| `~/hip-dev` | `demo-presenter-package` | own `.env.dev` | **7689** | active fallback, not a lane (CLAUDE.md) |
| `~/hip-roadmap` | `roadmap` | own `.env.dev` | **7688** | ACTIVE — build lane (A) AND governance lane (C), same checkout, per `HIP_HANDOFF.md` |
| `~/hip-roadmap-crypto-p1` | `roadmap-crypto-p1` | **none** | 7687 (hardcoded fallback) if run bare; 7688 if an operator manually sources hip-roadmap's `.env.dev` first (a common, established pattern in this project) | DORMANT since 2026-07-20, 0 uncommitted |
| `~/hip-roadmap-crypto-p2` | `roadmap-crypto-p2` | own `.env.dev` | **7688** — explicit, committed collision with `~/hip-roadmap` | DORMANT since 2026-07-20, 0 uncommitted |
| `~/hip-roadmap-stage1-wip` | `roadmap-stage1-wip` | own `.env.dev` | **7688** — explicit, committed collision with `~/hip-roadmap` | DORMANT since 2026-07-20, 0 uncommitted |
| `~/hip-ungoverned` | `demo-ungoverned-knowledge` | **none** | same ambiguity as crypto-p1 | DORMANT since 2026-07-22, 0 uncommitted |
| `~/hip-vo` | `main` | `.env.dev.example` (unused template, pins 7688 if ever materialized); `.env.demo` (real, in use) explicitly runs `source ~/hip-dev/.env.dev` | **7689** in demo mode — deliberate, live collision with the frozen demo | last commit 2026-08-01, 0 uncommitted — the LEAST dormant of the non-primary checkouts |
| `~/hip-vo2` | detached HEAD | same files as `~/hip-vo` | same as `~/hip-vo` | DORMANT since 2026-07-23, 0 uncommitted |
| `~/hip-cutover-demo` | `demo-cutover-build` | no `.env.dev` at all, by design — dedicated launcher (`scripts/cutover_demo_start.sh`) runs under `env -i` with a private `$HOME` (`~/hip-cutover-demo-home`, confirmed empty of any `.env.dev`) | **7690**, explicitly set on the launcher's own command line | ACTIVE — lane B, the ONE lane already correctly isolated by construction |

`~/hip-harness` is infrastructure, not a lane in this survey's sense — no `NEO4J_URI` in its
own `.env` (only `SERPAPI_KEY`); its `config.yaml` only names HTTP/service ports (8080, 8090),
not a Neo4j port. It hosts shared models, the shared `registry.db`, and the shared venv other
lanes' harness runs depend on, but does not independently choose a graph — it inherits whatever
`NEO4J_URI` the calling process's environment carries. Named for completeness, not counted as
a colliding lane.

### Collisions, named precisely — three different SHAPES, not one problem

1. **Explicit, committed, config-verified collision:** `~/hip-roadmap`, `~/hip-roadmap-crypto-p2`,
   and `~/hip-roadmap-stage1-wip` each carry their OWN real `.env.dev` pinning the identical
   port, 7688. This is not an accident of omission — three separate working trees are
   configured, on purpose (by whoever created crypto-p2/stage1-wip, presumably by copying
   hip-roadmap's own file), to write into the SAME graph every time they run. Currently latent
   (the two siblings are dormant) but would fire immediately if either were reactivated
   alongside any work in `~/hip-roadmap`.
2. **Deliberate, by-design collision with the named fallback:** `~/hip-vo`'s demo mode
   explicitly sources `~/hip-dev/.env.dev`, targeting 7689 on purpose. This is the LEAST
   dormant of the secondary checkouts (commits as recent as 2026-08-01) and the collision is
   live any time hip-vo's demo mode and the frozen demo could both be touched. Whether this
   sharing was ever explicitly sanctioned as an exception to "SHALL NOT share one graph," or
   is itself exactly the kind of case the new requirement is meant to close, is not decided
   by this survey.
3. **Ambiguous, operator-dependent, unaudited resolution:** `~/hip-roadmap-crypto-p1` and
   `~/hip-ungoverned` pin nothing themselves. Their actual graph on any given run is determined
   entirely by whatever a session manually sources beforehand — most likely 7687 (the
   hardcoded, UNOWNED fallback) if run bare, or 7688 if a session follows the STANDARD
   PREAMBLE's habit of sourcing hip-roadmap's `.env.dev` first. Neither outcome is
   deterministically WRONG on its own, but neither is verifiably RIGHT either — this is the
   collision shape hardest to catch after the fact, because it leaves no config trail naming
   what actually happened.
4. **The unowned default (7687) and the home-level override hazard (`~/.env.dev` → 7689,
   `override=True`)** are both STRUCTURAL risks layered under all four checkouts above that
   lack their own explicit pin — named here because TD-148's fix needs to account for both, not
   because either is new (the home-level hazard is already documented in CLAUDE.md's STANDARD
   PREAMBLE item 3).

### Prior art already read and cross-checked, not re-derived

`docs/HIP_HANDOFF.md` (D-137) already names a three-lane model (build + governance, both in
`~/hip-roadmap`; demo-cutover in `~/hip-cutover-demo`; frozen demo as fallback) and already
names "the Neo4j ports 7687/7688/7689/7690" as a contended surface, and already scopes TD-148's
technical shape in outline ("read-before-write, atomic O_EXCL/noclobber creation, drift-proof
liveness, and a dead-holder supersession policy"). This survey's contribution beyond that
document: the FULL disk-based inventory (HIP_HANDOFF.md's three-lane model does not mention
crypto-p1/p2, stage1-wip, hip-ungoverned, hip-vo/vo2 at all — dormant, but real, configured
collision surfaces TD-148's fix should account for even though they are not part of today's
active narrative), and the live process-level cross-check (which port is a real running
instance vs. only a config-file claim, and which instance is genuinely unowned).

## THE ENFORCEMENT SHAPE — OPTIONS, COSTS, WHAT EACH STOPS (item 2, none selected)

### Axis 1 — lock enforcement

| option | mechanism | cost | stops write-through (D-107) | stops unread clobber (D-118) | stops late-taken drift (D-114/D-145) |
|---|---|---|---|---|---|
| **A1. Atomic noclobber + PID/heartbeat liveness** (TD-148's own already-scoped shape, per `HIP_HANDOFF.md`) | `O_EXCL`/`set -o noclobber` file creation; holder PID + refreshed heartbeat mtime instead of a static `taken:` string; a dead-holder supersession policy | Low-moderate: a small shared library/script, called by convention at the start of every dispatch | **NO** — a session that reads the lock, sees another holder, and proceeds anyway is not physically prevented by a marker file, only by its own compliance | **YES** — a blind `>` fails outright at the OS level instead of silently overwriting | **YES** — heartbeat/PID removes the ambiguity that let two sessions each believe they held it |
| **A2. A real mutual-exclusion primitive** (`flock`/`fcntl`, held for the duration of a write, wrapping every write path) | every write path (git commit, graph write, INDEX edit) routes through a common wrapper that blocks on an OS-level lock rather than checking a marker file | Higher: requires a shared wrapper AND requires every lane's every write path to actually call it — a bigger behavior change than a marker file | **YES, if universally adopted** — a second process attempting to acquire an already-held lock is blocked by the kernel, not merely advised | YES (subsumes A1's fix) | YES (subsumes A1's fix) |
| **A3. A git hook (pre-commit/pre-push) that checks/acquires the lock automatically** | lock-checking becomes part of git's own machinery instead of a manual per-dispatch step | Low-moderate; per-worktree setup (or a shared hooks-path) needed across all checkouts | **Partially** — removes "forgot to check," not "chose to override" (`--no-verify` bypasses any hook) | Partially, same caveat | No, doesn't address timestamp drift on its own |

**The honest limit shared by ALL THREE options:** none of them stops a process that does not
call the mechanism at all — a raw `git commit` typed directly, or a session that never sources
the convention. A1 and A3 remain fundamentally advisory unless the write path itself is made
narrow enough that bypassing it is hard; A2 is the only option that converts "advisory" into
"enforced" in the literal sense of Bill's ruling text, and only to the extent every write path
is actually forced through its wrapper.

### Axis 2 — graph separation

| option | mechanism | cost | what it stops |
|---|---|---|---|
| **B1. Dedicated Neo4j instance per lane** (extends the ALREADY-PROVEN pattern: 7689 for the frozen demo, 7690 for demo-cutover) | stand up `~/neo4j-<lane>` instances for every currently-live and reactivatable checkout | **Real, previously-measured cost**: TD-129 recorded 0.07 GB free memory at one point specifically when a second instance was assessed and rejected as infeasible; this machine currently already runs FOUR live JVMs (7687/7688/7689/7690) — adding more for crypto-p1/p2, stage1-wip, hip-ungoverned, hip-vo/vo2 could mean 8-10 concurrent instances | Complete and permanent, for whichever lanes get one — the most thorough fix, contingent on headroom that has not been re-measured since TD-129 |
| **B2. Logical separation within shared instances** (Neo4j multi-database or a labeling/namespace convention) | every query/write path becomes lane-aware and scopes itself | Low infra cost, but likely **not even technically available**: prior project research (banked D-63 review) already found Neo4j Community edition is single-database — this option may require an edition upgrade before it is buildable at all, and even if available, is a much larger and more error-prone CODE change (every query site, not a one-time infra step) | Nothing automatically — safety is exactly as strong as the code discipline behind every query site, the opposite of a structural "SHALL NOT share" |
| **B3. Retire the dormant, non-dedicated lanes** (`git worktree remove` for crypto-p1, crypto-p2, stage1-wip, hip-ungoverned, hip-vo2 — all confirmed 0 uncommitted, dormant 2+ weeks) | shrink the number of checkouts that need isolation at all, rather than isolating everything that currently exists | Low — pure subtraction, no new mechanism | Removes the collision FROM the retired lanes specifically; does nothing for `~/hip-roadmap`, `~/hip-cutover-demo`, `~/hip-dev`, or `~/hip-vo` (the one secondary checkout with recent activity), which still need one of B1/B2 or an explicit sanctioned-sharing ruling |
| **B4. Per-checkout startup guard** (generalizes D-108's already-built C2 guard pattern: refuse to start if `NEO4J_URI` doesn't match the checkout's own expected port) | replicate the existing, proven pattern into every checkout's own server/harness entry point | Low — code-only, and the pattern is already built once | Turns silent MISCONFIGURATION into a loud refusal (closes collision shape 3, the ambiguous/operator-dependent case) — does NOT by itself separate two checkouts that are EACH correctly configured to share a port (crypto-p2/stage1-wip's shape 1 collision still needs B1 or B3) |

**B1/B3/B4 are not mutually exclusive** — B3 (retire dormant lanes) shrinks the problem before
B1 (dedicate instances) is applied to what remains, and B4 (startup guards) is a cheap
complement to either, catching misconfiguration regardless of which of B1/B2/B3 is chosen for
the underlying separation. B2 is flagged as possibly not available at all pending a Community-
edition capability check this survey did not perform (out of scope: item 3 forbids any
building, including a spike to test multi-database availability).

## VERIFIED

**Watched run:** every port/process claim above is read directly from `lsof -iTCP -sTCP:LISTEN`
and `ps aux` output, not inferred from config files alone — config and live state were cross-
checked against each other explicitly (e.g., `~/hip-roadmap-crypto-p1`'s config ABSENCE was
confirmed by direct `ls`/`grep`, not assumed from its not appearing in `HIP_HANDOFF.md`). Every
checkout's dormancy/liveness (`git log -1`, `git status --short`) was executed directly, not
estimated from commit-message dates alone.

**Reasoned about:** which port a checkout with NO committed env file would ACTUALLY resolve to
on any given real run (crypto-p1, hip-ungoverned) is inference about operator behavior, not a
fact this survey could observe directly — stated as an ambiguity (collision shape 3) rather than
asserted as a specific port. The TD-129 memory-constraint citation is prior, already-documented
project history, not re-measured live this dispatch (item 3 forbids running anything that would
need a new Neo4j instance to test).

## HASH

Staged for commit alongside this doc:
`docs/requirements/REQ_LOCK_ENFORCEMENT__td148-enforce-lock-and-separate-graphs__v20260803_2047.md`
(new, Status: PLAN).

## OPEN

- **Bill rules the shape** (item 2's own instruction) — both axes (lock enforcement, graph
  separation) have multiple viable options named above, each costed, none picked. This is the
  next, single decision blocking any build.
- **hip-vo's deliberate 7689 sharing** is a live collision this survey found but did not
  resolve — whether it is a sanctioned exception or exactly the case the new requirement
  closes needs a ruling, separate from the crypto-p2/stage1-wip/hip-roadmap collision (which
  reads as unintentional).
- **B2's actual availability (Neo4j Community multi-database) was not verified live** — flagged
  from prior project research, not confirmed fresh, and this dispatch's own "no code" scope
  did not permit a spike to check.
- **Current free-memory headroom was not re-measured** — TD-129's 0.07 GB figure is the last
  known data point; if B1 (dedicated instances) is the chosen shape, a fresh measurement should
  precede committing to how many new instances the machine can actually hold.
- **Nothing ruled**, per instruction — this dispatch is survey and options only.
