# DISPATCH_DEMO_CUTOVER_WIRE_AND_PROVE_C1
Status: BUILT
Reconciled-Against: demo-cutover-build @ 7191493 (~/hip-cutover-demo)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260802_1205.md`
(D-106) — acceptance row C1 (dashboard serves the new demo, /api/preflight reports
all_ok + git_head matching the cutover commit). Builds directly on D-108's C6/C2 port. No
demo script was ported. No scripted turn was fired. No acceptance row is marked MET here —
that is Bill's call, not taken by this dispatch.

## THE ASK

Bill's dispatch, verbatim (item 3, resent in full after the prior truncation):

> "3. WIRE THE WORKTREE TO 7690 AND BRING IT UP (C1).
>
>    THE PRECEDENCE FIGHT, Bill's ruling: solve it in the LAUNCHER, contained to the new
>    tree. Write a start script for ~/hip-cutover-demo that unsets NEO4J_URI (and any other
>    frozen-demo pin ~/.env.dev sets) BEFORE the Python process loads anything, then sets
>    7690 explicitly. Do NOT edit ~/.env.dev. Do NOT change _load_env_file's precedence —
>    that would alter behavior for the frozen demo's dashboard too.
>    The C2 guard stays in place as the backstop; the launcher makes it never need to fire.
>
>    Credential is at ~/hip-keys/neo4j-cutover-demo/NEO4J_PASSWORD. Do not print it.
>
>    Seed the empty 7690 graph with demo_seed.py — roadmap's 522-line version.
>
>    Start the dashboard on a free port. 7870 and 7871 are in use; pick another and say
>    which.
>
> 4. PROVE THE FLOOR. Report to the terminal:
>    - the launcher scrubbing the pin (show NEO4J_URI resolving to 7690, not 7689)
>    - /api/preflight output: all_ok, and git_head matching the worktree HEAD
>    - the seeded fact count on 7690
>    - ~/hip-dev diff (must be empty) and both frozen-demo PIDs before and after
>
> Do not port any demo script. Do not fire a scripted turn. Do not mark any row MET.
> Commit on demo-cutover-build when the floor proves out. Do not push."

## WHAT WAS DONE

1. Machine gate + baseline re-check before touching anything: hip-dev dashboard pid
   `92604` (port 7871), frozen-demo Neo4j pid `22330` (port 7689) — identical to the
   D-108 baseline, confirmed unchanged going in.
2. **Diagnosed the precedence fight precisely before writing anything.**
   `demo_dashboard.py`'s `_load_env_file(pathlib.Path.home() / ".env.dev", override=True)`
   does `if override or k not in os.environ: os.environ[k] = v` for every key the file
   defines — with `override=True` the `k not in os.environ` branch is dead code; a
   shell-level `unset`/`export` before launching python cannot survive this, because the
   override fires again the instant python's own loader runs, unconditionally, regardless
   of what the calling shell already set. Confirmed live in the D-108 dispatch (a plain
   `NEO4J_URI=bolt://localhost:7690` export was clobbered back to 7689) and reasoned about
   again here before design, not re-guessed.
3. Confirmed `~/.env.dev` sets exactly three keys — `NEO4J_URI`, `OPENAI_API_KEY`,
   `ANTHROPIC_API_KEY` (names only, no values read into this doc). Only the first is a
   frozen-demo pin; the other two are generically useful credentials worth preserving.
4. Confirmed `scripts/demo_seed.py`'s fact-writing path (`harness.extraction_queue
   ._get_driver()`) reads `NEO4J_URI` directly from `os.environ.get(...)` with no
   `_load_env_file`/home-dir loading anywhere in that call chain — grepped
   `harness/extraction_queue.py`, `harness/dyad_registry.py`, `harness/household_keys.py`,
   `harness/care_team_keys.py` for `_load_env_file`/`.env.dev`/`NEO4J_URI`: only
   `extraction_queue.py` references `NEO4J_URI`, plainly. Seeding needed no launcher
   workaround — a direct env var export was sufficient and used.
5. Wrote `scripts/cutover_demo_start.sh` in `~/hip-cutover-demo` (see WHAT WAS FOUND for
   the exact mechanism) and made it executable.
6. Ran `demo_seed.py --dry-run` against `NEO4J_URI=bolt://localhost:7690` first, read the
   output, then ran it for real.
7. Launched the dashboard via the new launcher on port 7872 (7870, 7871 confirmed in use;
   7872-7874 confirmed free before picking 7872), captured its startup log, hit
   `GET /api/preflight` and `GET /` over real HTTP, then killed the process and confirmed
   the port released.
8. Re-checked hip-dev's PID and 7689's PID identical, and `~/hip-dev`'s `git status
   --porcelain` identical (same five pre-existing untracked files, nothing new).
9. Committed on `demo-cutover-build` (`~/hip-cutover-demo`), not pushed.

## WHAT WAS FOUND

**The launcher mechanism.** `scripts/cutover_demo_start.sh`:
- Machine/folder/marker guards matching `dev.sh`'s and `demo_preflight.sh`'s existing
  pattern (hostname, checkout path, `DEV_MARKER.txt` present, `DEMO_MARKER.txt` absent).
- `unset NEO4J_URI NEO4J_PASSWORD NEO4J_USER` in the launcher's own shell first (defense in
  depth against a stray value already exported in the calling terminal) — though, per point
  2 above, this alone would not be sufficient without the next step.
- Reads `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` directly out of the real `~/.env.dev` by
  name (never `NEO4J_URI`) into shell variables, values never echoed anywhere.
- Runs the python process under `env -i` (a fully explicit environment allow-list, nothing
  ambient leaks through) with `HOME` pointed at a new private directory,
  `~/hip-cutover-demo-home`, that has no `.env.dev` in it. `demo_dashboard.py`'s
  `_load_env_file(pathlib.Path.home() / ".env.dev", ...)` therefore hits its own
  `if not path.exists(): return` and the real file is **never read at all** for this
  process — not a value overridden after the fact, a file that was never there. This is
  the one mechanism that actually survives `override=True`; a same-process env-var
  override does not (proven wrong in D-108, reasoned about again above).
- Explicitly sets `NEO4J_URI=bolt://localhost:7690` (never derived from `~/.env.dev`),
  `NEO4J_PASSWORD` read from `~/hip-keys/neo4j-cutover-demo/NEO4J_PASSWORD` (never
  printed), `HIP_REGISTRY_DB` pointed at the real `~/hip-harness/registry.db` by absolute
  path (survives the `HOME` redirect, which would otherwise also move
  `member_registry.DEFAULT_DB_PATH`), and passes through `OPENAI_API_KEY`/
  `ANTHROPIC_API_KEY`/`GROQ_API_KEY` (the last already present in the calling shell from
  `~/.zshrc`, unrelated to `~/.env.dev`).
- `~/.env.dev` itself: **not edited.** `_load_env_file`: **not edited, not called with
  different arguments, not touched at all** — `demo_dashboard.py` is byte-identical to
  what D-108 committed. The fix lives entirely in the new script, as instructed.
- Side effect of the private `HOME`, both judged correct rather than incidental: this
  checkout gets its **own** operator token (`_DASHBOARD_TOKEN_PATH` also resolves under
  `pathlib.Path.home()`) instead of sharing hip-harness's — appropriate for a genuinely
  separate, dedicated checkout, not a workaround. `PLIST_PATH` (a `NEO4J_PASSWORD`
  fallback) also redirects but is never reached, since the password is set explicitly.

**The seed.** `scripts/demo_seed.py` writes two different kinds of state through two
different backends, and only one of them is per-graph:
- Facts (D1-D11) go through `harness.extraction_queue._get_driver()`, which reads
  `NEO4J_URI` directly — these landed on 7690, confirmed (see VERIFIED).
- Members, voiceprints, identity/seal keypairs, dyads, household-circle enrollment, and
  care-team enrollment are backed by `harness.member_registry.DEFAULT_DB_PATH` (SQLite,
  `harness/dyad_registry.py` imports it directly — grepped, confirmed no Neo4j driver
  reference anywhere in that file). Pointing `HIP_REGISTRY_DB` at the real, shared
  `~/hip-harness/registry.db` meant most of these steps correctly reported "already
  present/active — skipping" (idempotent, shared roster and authorization state, not
  graph-scoped) rather than re-creating anything. Two identity keypairs (maya, sam) and
  three enrollments (household circle x3, care team x2) were genuinely new — this registry
  had authorization-key material and household/care-team enrollment recorded for `bill`
  only before this run. This is expected, shared, cross-checkout state, not something this
  dispatch introduced a defect into.

## VERIFIED

**Watched run, all of it:**
- **Pin scrubbed, live:** dry-run and real seed runs both connected successfully with
  `NEO4J_URI=bolt://localhost:7690` exported directly (seed path needs no launcher, see
  finding 4). The dashboard launcher's own startup log printed
  `NEO4J_URI: bolt://localhost:7690` and the self-check line
  `[PASS] neo4j: connected bolt://localhost:7690` — not 7689, with the real, unmodified
  `~/.env.dev` present on disk the entire time.
- **Fact count:** `MATCH (f:Fact) RETURN count(f)` against 7690 directly (a fresh
  Python/neo4j-driver query, not read from the seed script's own claim) →
  **total=11, live (valid_to IS NULL)=11** — matches `demo_seed.py`'s own "11/11 fact(s)
  seeded" line exactly.
- **`/api/preflight`, real HTTP call, port 7872:**
  `{"all_ok": true, "pid": 25367, "git_head":
  "2f69f2fb349c4027747173f22ceace6e7b35733d", "checks": [openai_api_key: PASS,
  groq_api_key: PASS, registry_db: PASS (3 members), neo4j: PASS (connected
  bolt://localhost:7690), operator_token: PASS]}`. `git_head` matches
  `~/hip-cutover-demo`'s own `git rev-parse HEAD` at seed/launch time (`2f69f2f`) exactly.
- **`GET /`:** `200`.
- **hip-dev / 7689, before and after:** dashboard pid `92604` (port 7871) and Neo4j pid
  `22330` (port 7689) identical at every checkpoint (before item 3 started, after the
  seed, after the live dashboard test, after cleanup). `~/hip-dev`'s `git status
  --porcelain` identical throughout — same five pre-existing untracked files (none
  created by this or any prior dispatch this session), nothing new.
- **Cleanup:** test dashboard process killed, port 7872 confirmed released
  (`lsof` empty) before moving on.
- **Scope of the commit:** `git diff --stat` on `demo-cutover-build` before committing
  showed exactly two files — `server/demo_dashboard.py` (D-108's change, still uncommitted
  until now) and the new `scripts/cutover_demo_start.sh`. Nothing else.

**Reasoned about, not independently re-run:** `_ensure_dyad`/`_ensure_household_circle_
member`/`_ensure_care_team_member`'s SQLite-vs-Neo4j split was confirmed by reading
`harness/dyad_registry.py`'s imports (no Neo4j driver reference in the file) rather than
by, e.g., pointing `HIP_REGISTRY_DB` at an empty throwaway file and re-running to observe
the difference — the import-level evidence was judged sufficient and a second live run
against a scratch registry was not performed.

## HASH

`~/hip-cutover-demo` (branch `demo-cutover-build`): **`7191493`** — committed, not pushed.
Contains D-108's `server/demo_dashboard.py` change (self-check port + C2 guard, previously
uncommitted) and this dispatch's `scripts/cutover_demo_start.sh`, together, per Bill's
explicit "commit on demo-cutover-build when the floor proves out."

`~/hip-roadmap` (branch `roadmap`): **NONE.** This dispatch doc and its `docs/INDEX.md` row
are themselves uncommitted, same pattern as every prior roadmap-side doc this session,
pending Bill's explicit go-ahead — the "commit on demo-cutover-build" instruction named
that branch specifically, not this one.

## OPEN

- **C1 is proven live, not marked MET.** That determination is explicitly Bill's, per the
  REQ's own CONSTRAINTS and this dispatch's own instruction ("do not mark any row MET").
- **The registry-sharing design (facts isolated per-graph, identity/authorization state
  shared via one SQLite file across every checkout) was discovered, not decided, by this
  dispatch.** It was already the shape of `demo_seed.py`/`harness.member_registry` before
  today. Flagged for visibility in case it's not the intended isolation boundary for the
  cutover demo specifically — nothing was changed to alter it either way.
- **`~/hip-cutover-demo-home`** (the launcher's private HOME) now exists on disk with a
  freshly generated operator token in it. Not cleaned up — the whole point is for it to
  persist across restarts (comment in the launcher explains why) rather than regenerate
  the token every launch.
- **C3, C4, C5, C7, C8, C9, C10 remain entirely untouched.** No demo script exists on this
  base. The dashboard was proven up and briefly torn down for this dispatch's live test —
  it is not left running.
- Whether to commit this dispatch doc + its `docs/INDEX.md` row in `~/hip-roadmap` is
  Bill's call, not taken here.
