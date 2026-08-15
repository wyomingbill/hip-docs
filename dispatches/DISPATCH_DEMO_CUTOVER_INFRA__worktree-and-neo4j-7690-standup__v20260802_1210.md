# DISPATCH_DEMO_CUTOVER_INFRA
Status: BUILT
Reconciled-Against: 2f69f2f (roadmap HEAD both instances were cut/started from)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260802_1205.md`
(D-106) — this dispatch covers the two infra pieces Bill's rulings on that REQ's open items
directly authorized: the Neo4j port choice (ruling 1) and the worktree-not-branch decision
(ruling 2). No demo code, script, or dashboard work is in this dispatch — C1-C10 remain
entirely unattempted.

## THE ASK

Bill's rulings, verbatim (same text recorded in the REQ's own RULINGS section):

> "1. PORT: 7690. Confirmed free. New dedicated instance at ~/neo4j-cutover-demo,
>    its own data dir, own conf, own credentials.
>
> 2. TREE: a NEW WORKTREE of the roadmap repo, not a branch inside ~/hip-roadmap.
>    ...
>
> Record these in the REQ and proceed."

"Record" was done in the REQ doc itself (D-106, same session). "Proceed" is this dispatch:
standing up the two pieces of infrastructure those two rulings concretely unblock.

## WHAT WAS DONE

1. Machine/branch gate per standing protocol: `whoami && hostname && pwd && git branch
   --show-current` — confirmed `bill-ai` / `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]` /
   `roadmap`, before any write.
2. Checked `~/hip-roadmap/.hip-lock` — absent. Checked `git status --porcelain` — clean
   before this session's writes. Clear to write per lock discipline.
3. Confirmed `demo-cutover` branch (`5b7a5bb`, the branch REQ_DEMO_PREFLIGHT_CONSENT_ASSERTION
   was built on) is fully merged into `roadmap` — `git log roadmap..demo-cutover` = 0 commits,
   `git log demo-cutover..roadmap` = 73. It is closed-out history, not a live base; deliberately
   NOT reused for the new worktree.
4. Confirmed ports 7690/7691/7692 free (`lsof -iTCP -sTCP:LISTEN`, only 7687/7688/7689
   listening beforehand) and 7477 (the http port that follows the existing bolt->http
   convention: 7687->7474, 7688->7475, 7689->7476, so 7690->7477) also free.
5. Built `~/neo4j-cutover-demo/{conf,data,import,logs,plugins,run}`. `conf/neo4j.conf` is
   `~/neo4j-hipdev-demo/conf/neo4j.conf` (the closest analog — a demo instance, not the dev
   one) with every `neo4j-hipdev-demo` path rewritten to `neo4j-cutover-demo`, bolt rewritten
   7689->7690, http rewritten 7476->7477, and the trailing HIP-specific comment block
   rewritten to name this REQ instead of TD-054.
6. Generated a fresh random password (`openssl rand -base64 24`, not the shared dev/demo
   password), ran `neo4j-admin dbms set-initial-password` against it via `NEO4J_CONF=~/
   neo4j-cutover-demo/conf` (the `--config-dir` flag does not exist on this subcommand —
   config dir is env-var-only; first attempt with that flag failed, corrected to the env var).
   Password written to `~/hip-keys/neo4j-cutover-demo/NEO4J_PASSWORD`, mode 600 — this
   directory already exists as this project's convention for exactly this kind of secret, not
   a new location invented for this dispatch.
7. Started the instance (`neo4j start` with `NEO4J_HOME`/`NEO4J_CONF`/`JAVA_HOME` set to the
   same values `dev.sh` uses for 7688, config dir swapped). Up in 1s.
8. Created the new worktree: `git worktree add -b demo-cutover-build ~/hip-cutover-demo
   roadmap`, cut from `roadmap` HEAD `2f69f2f` — not from `demo-cutover`, per step 3's finding.

## WHAT WAS FOUND

- `~/neo4j-hipdev-demo/conf/neo4j.conf:383-384` is where the bolt/http port pair is pinned
  for the frozen-demo instance (7689/7476) — the same two lines were the only functional
  edit needed to derive the new instance's conf beyond path substitution.
- Neo4j's `neo4j-admin dbms set-initial-password` takes the config directory from the
  `NEO4J_CONF` environment variable only; it has no `--config-dir` flag (confirmed via
  `--help`, only `--additional-config`, `--expand-commands`, `--require-password-change`,
  `--verbose` exist). Recorded here so the next session doesn't repeat the failed first
  attempt.
- `demo-cutover` (`5b7a5bb`) is 0 commits ahead / 73 behind current `roadmap` — fully
  absorbed, confirmed by `git merge-base --is-ancestor demo-cutover roadmap` returning true.

## VERIFIED

**Watched run, all of it:**
- `lsof -iTCP -sTCP:LISTEN -P` before and after: 7687 (pid 1123, shared homebrew default),
  7688 (pid 1453, roadmap dev), 7689 (pid 22330, frozen demo) unchanged throughout; 7690
  (pid 20331, new instance) came up and stayed up.
- Bolt round-trip against the new instance from `~/hip-roadmap`'s own venv/system python:
  `GraphDatabase.driver('bolt://localhost:7690', auth=('neo4j', <generated password>))`,
  `RETURN 1 AS ok` returned `1`. The generated credential authenticates; this is not just a
  listening port.
- `git worktree list` after creation shows `~/hip-cutover-demo  2f69f2f [demo-cutover-build]`
  alongside the seven pre-existing worktrees, none of which moved.
- Frozen demo (`~/hip-dev`, 7689, pid 22330) checked by PID before and after all of the
  above — unchanged, per REQ's C10 discipline (verified, not assumed, even though C10 as a
  full acceptance row is not being claimed MET by this session).

**Not run / explicitly out of scope for this dispatch:** no code was written against C1-C10.
No dashboard, no `.env` wiring, no self-check port, no script port, no C2 refusal guard.
Those need their own REQ-scoped build dispatch(es) — this one is infra standup only.

## HASH

**NONE for a code commit** — nothing in `~/hip-roadmap`'s tracked tree was committed by this
dispatch. Two new files exist **uncommitted** in the working tree:
`docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260802_1205.md` and
its `LATEST_` symlink (from the filing dispatch, same session), plus this dispatch doc and
the `docs/INDEX.md` registration edit made alongside it. Per standing instruction to commit
only when explicitly asked, these are left staged-in-working-tree for Bill to review and
commit (or ask this session to commit) rather than committed unilaterally.

The new worktree (`~/hip-cutover-demo`, branch `demo-cutover-build`) has no commits of its
own yet beyond the roadmap history it was cut from — it is an empty branch pointer at
`2f69f2f`, not a code change.

## OPEN

- The REQ's own acceptance rows C1-C10 are entirely unattempted. This dispatch only unblocks
  two of the three previously-open decision points; the 18-32 hour build estimate in the REQ
  is untouched by it.
- `~/neo4j-cutover-demo` has no data loaded — no seed has been run against it. The new
  worktree's own `demo_seed.py` (roadmap's 522-line version, already has the crypto/identity
  infra hip-vo lacks per the REQ's WHAT'S ALREADY DONE) has not been pointed at 7690 or run.
- No `.env`/config file exists yet in `~/hip-cutover-demo` wiring `NEO4J_URI` to `bolt://
  localhost:7690`. Deliberately not created this dispatch — that's dashboard-wiring work
  (C1/C2/C6) requiring the self-check system to exist first, not a mechanical env-var copy.
- C2's structural refusal guard (refuse to start if `NEO4J_URI` resolves to 7689) does not
  exist anywhere yet — there is no dashboard on this base to put it in until C6 ports one.
  The home-directory `~/.env.dev` override-hazard the REQ names is still live and unaddressed.
- Whether to commit the two working-tree files (REQ + this dispatch + INDEX row) is Bill's
  call, not taken here.
