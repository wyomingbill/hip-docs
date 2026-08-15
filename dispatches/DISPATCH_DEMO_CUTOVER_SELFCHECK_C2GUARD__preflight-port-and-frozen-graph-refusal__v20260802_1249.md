# DISPATCH_DEMO_CUTOVER_SELFCHECK_C2GUARD
Status: BUILT
Reconciled-Against: 2f69f2f (worktree base; code lives uncommitted in ~/hip-cutover-demo)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260802_1205.md`
(D-106) — acceptance rows C6 (self-check system ported) and C2 (frozen-graph refusal guard).
C1 (dashboard serves the new demo, /api/preflight all_ok + git_head) is touched but NOT
claimed — see WHAT WAS FOUND, item 4. No demo script was ported. No scripted turn was fired.

## THE ASK

Bill's dispatch, verbatim, items 1 and 2 (item 3, "WIRE THE WORKTREE", was cut off in
transit with no body — flagged back to Bill rather than guessed at; not attempted here):

> "1. PORT THE SELF-CHECK SYSTEM (C6). From ~/hip-vo: GET /api/preflight,
>    _startup_self_check, _degraded_mode_guard and the _SELF_CHECK_* machinery. Roadmap has
>    none of it. Reconcile against roadmap's own demo_dashboard.py rather than overwriting —
>    report anything roadmap has that hip-vo lacks in the same file.
>
> 2. ADD THE C2 REFUSAL GUARD. The dashboard must REFUSE TO START, loudly, if NEO4J_URI
>    resolves to bolt://localhost:7689. Not degraded mode — refuse.
>    Follow the pattern demo_preflight.sh already uses to hard-pin 7688: a literal check, not
>    reliance on config precedence. ~/.env.dev is a home-directory file loaded with
>    override=True unconditionally; a repo-local .env cannot beat it.
>    FAULT TWIN, required: point it at 7689, confirm it refuses to start. Restore, confirm it
>    starts. Report both transitions."

## WHAT WAS DONE

1. Machine gate: `whoami && hostname && pwd && git branch --show-current` in
   `~/hip-cutover-demo` — confirmed `bill-ai` / `[REDACTED-MACHINE-NAME]` / branch
   `demo-cutover-build`.
2. Took `~/hip-roadmap/.hip-lock` (holder D-108, session `sonnet5-cutover-c6c2`) before any
   write, scoped explicitly to doc registration only — the code build happens entirely in
   the separate `~/hip-cutover-demo` worktree, not in `~/hip-roadmap`'s own working tree.
3. Recorded baseline: hip-dev dashboard pid `92604` (port 7871), frozen-demo Neo4j pid
   `22330` (port 7689). Re-checked identical after every step below.
4. Diffed `~/hip-vo/server/demo_dashboard.py` against `~/hip-cutover-demo/server/
   demo_dashboard.py` (`diff -u`, full file, 12 hunks) before writing anything, to see the
   whole shape of the divergence rather than porting from memory of the self-check region
   alone. Full reconciliation report in WHAT WAS FOUND.
5. Ported, into `~/hip-cutover-demo/server/demo_dashboard.py` only:
   - `_dashboard_token()`'s blank-override `.strip()` fix (REQ_DEMO_SELF_VERIFYING's own
     one real auto-fix; one line, no interaction with anything roadmap-specific).
   - The full self-check block verbatim: `_SELF_CHECK_RESULT`/`_SELF_CHECK_FATAL` globals,
     `_check_api_key`, `_check_registry`, `_check_neo4j`, `_check_operator_token`,
     `_startup_self_check`, the module-level call, `_degraded_mode_guard` middleware,
     `GET /api/preflight`, `_current_git_head` — inserted as a new block immediately after
     roadmap's own `api_session_select_member` (left untouched) and before the
     `# ── API endpoints ──` divider, matching hip-vo's insertion point exactly.
   - Added `import sys` (needed by the new guard below; wasn't imported before).
6. Added the C2 guard immediately after `NEO4J_URI`/`NEO4J_USER` are resolved and before
   `app = FastAPI(...)` — a literal `NEO4J_URI == "bolt://localhost:7689"` check,
   `print(..., file=sys.stderr)` + `sys.exit(1)`, no dependency on config precedence,
   evaluated at MODULE IMPORT TIME (before self-check, before the app object exists, before
   any route is defined) so it fires under every launcher, not just one code path.
7. Fault-twin tested both directions, live, three separate runs (see VERIFIED).
8. Confirmed hip-dev's PID and 7689's PID unchanged after every run.

## WHAT WAS FOUND

**1. The reconciliation (what roadmap has that hip-vo lacks) — not ported, not touched:**
Full diff was 12 hunks; only the self-check hunk (`@@ -178,75 +183,175 @@`) and the tiny
`_dashboard_token()` hunk were ported. The other ten hunks are all roadmap ahead of hip-vo,
confirmed NOT regressed by this dispatch:
   - `api_session_select_member` (roadmap only): Ed25519 signature verification against a
     member's registered pubkey before a vault-tab switch is honored (REQ_IDENTITY_BINDING
     _BUILD step 2), plus clearing/setting the verified voice session so the separate voice
     server (port 7860) trusts this instead of a client-asserted speaker_id (step 4). hip-vo's
     version of this endpoint has none of it — a bare client-asserted member string.
   - `/api/decrypt` (roadmap only): caller-scoped decrypt via
     `harness.partition_crypto.decrypt_fact_value_for_caller` (REQ_CRYPTO_P2_PARTITION
     _SEALED site 9) — a v2 (class-sealed) fact only opens if the session's selected member
     actually holds the right key; also recognizes an active care-team caregiver via
     `harness.care_team_keys.is_active_caregiver` for facts whose owner is the recipient, not
     the reader. hip-vo's version calls the legacy `harness.encryption.decrypt_fact_value`
     unconditionally — no caller-scoping, no caregiver visibility.
   - `/api/fact_history` (roadmap only): same caller-scoped decrypt (site 10) via an
     `as_member` query param, `key_version`/`dyad_id`/`recipient_ref` read and passed through.
     hip-vo's version has no `as_member` param and decrypts everything through the legacy
     unscoped path.
   - `/api/text-query` (roadmap only): requires a real `{member, ts, nonce, sig}` and calls
     `harness.identity_keys.verify_turn` before accepting the turn; rejects with
     `identity_rejected: <reason>` on failure (REQ_IDENTITY_BINDING_BUILD step 2's own named
     defect target — this endpoint specifically). hip-vo's version accepts a bare client-
     asserted member with no verification at all.

   **None of these four were touched.** Confirmed by re-diffing after the edit: every line
   in those four regions is byte-identical to before this dispatch.

**2. A live, load-bearing finding the fault-twin test surfaced (not anticipated going in):**
`~/.env.dev` (Bill's real home-directory file, loaded by the pre-existing
`_load_env_file(pathlib.Path.home() / ".env.dev", override=True)` — present in both trees
already, not introduced by this dispatch) contains `export NEO4J_URI=bolt://localhost:7689`.
Because it loads with `override=True` unconditionally, **setting `NEO4J_URI=bolt://
localhost:7690` directly in the launch environment does not survive** — the home-dir file
clobbers it back to 7689 every time, for this checkout exactly as it would for any other.
First attempt at the "restore, confirm it starts" fault-twin direction (below) hit this
directly: the guard fired again even with 7690 explicitly exported, correctly, because
NEO4J_URI genuinely still resolved to 7689 after env loading.

**This is not a bug in the guard — it is the guard doing exactly its job against the
checkout's current real environment.** But it means: **as configured today, this checkout
cannot actually start the dashboard at all**, guard or no guard, because the one file that
always wins the precedence fight points at the frozen demo's graph. `~/.env.dev` is shared
across every checkout on this machine (hip-dev, hip-vo, roadmap, this worktree) — not
something to change unilaterally as a side effect of this dispatch. This is exactly the
open question item 3 ("WIRE THE WORKTREE") was presumably going to address; it's now a
concrete, live-reproduced blocker rather than a documented risk, and needs Bill's call on
how the new checkout is meant to win that precedence fight (a value only `~/.env.dev`
itself can currently set, an additional override layer this checkout's own code adds, or
something else).

**3. C1 touched, not claimed.** The real end-to-end launch (see VERIFIED) returned a
correct `git_head` (`2f69f2f`, the worktree's actual HEAD) but `all_ok: false` — not because
of anything wrong with C2 or C6, but because `OPENAI_API_KEY` and `HIP_REGISTRY_DB` weren't
configured in the sandboxed test environment used to work around finding 2 above. Getting
`all_ok: true` needs real env wiring this dispatch deliberately did not attempt. C1 is
**not** claimed MET by this dispatch.

## VERIFIED

**Watched run, all three:**
- **Refuse direction, real environment, no workaround:** `NEO4J_URI=bolt://localhost:7689`
  exported, `~/hip-dev/.venv/bin/python -c "import server.demo_dashboard"` from
  `~/hip-cutover-demo` → printed the three-line refusal to stderr, exited 1, no port ever
  opened, no Neo4j connection ever attempted (refusal fires before `_get_driver()` exists).
- **Start direction:** since `~/.env.dev`'s real content defeats a plain env-var override
  (finding 2), tested with `HOME` pointed at a scratch directory for the subprocess only
  (`pathlib.Path.home()` resolves from `$HOME`; this makes `~/.env.dev` resolve to a
  nonexistent path for that one process, so its override never fires — no real file was
  read, written, or touched) plus `NEO4J_URI=bolt://localhost:7690` and the generated
  credential from `~/hip-keys/neo4j-cutover-demo/NEO4J_PASSWORD`. Import succeeded, no
  `SystemExit`, `NEO4J_URI` resolved to `bolt://localhost:7690` as read back from the
  module, `_SELF_CHECK_FATAL == False`, neo4j check `{"ok": true, "detail": "connected
  bolt://localhost:7690"}`.
- **Full HTTP launch, same workaround:** `python -m server.demo_dashboard --host 127.0.0.1
  --port 7873` as a real subprocess, port confirmed bound (`lsof`), `GET /api/preflight`
  returned the five checks above plus `"pid": 22005, "git_head":
  "2f69f2fb349c4027747173f22ceace6e7b35733d"` (the worktree's real HEAD), `GET /` returned
  `200` (degraded-mode guard correctly did not block normal routes, since the one fatal
  check — neo4j — passed). Process killed afterward, port confirmed released.
- **hip-dev / 7689 unchanged:** pid `92604` (dashboard) and pid `22330` (Neo4j) checked
  identical before this dispatch, after each of the three test runs above, and at the end.
  `git status --porcelain` in `~/hip-dev` identical before/after (same five pre-existing
  untracked files, none created by this dispatch).
- **Scope check:** `git diff --stat` in `~/hip-cutover-demo` shows exactly one file changed,
  `server/demo_dashboard.py`, +191/-1.

**Reasoned about, not independently re-run:** the ported self-check/guard code itself is
unmodified from hip-vo's version (verified by diff before porting) except for the blank-
override fix, which is also unmodified from hip-vo's version — no new logic was authored in
the ported block, only in the new C2 guard.

## HASH

**NONE.** Nothing committed in either checkout. `~/hip-cutover-demo/server/
demo_dashboard.py` has one uncommitted modification (+191/-1, `git diff --stat` confirmed
clean/scoped). This dispatch doc and its `docs/INDEX.md` row are themselves uncommitted in
`~/hip-roadmap`, left for Bill's explicit go-ahead per standing instruction — same pattern
as D-106/D-107's infra dispatch.

## OPEN

- **Item 3 ("WIRE THE WORKTREE") was never received** — Bill's dispatch cut off after the
  heading with no body. Not guessed at. Needed before this checkout can actually be launched
  for real (see finding 2) or before C1 can be attempted in earnest.
- **Finding 2 is the load-bearing open item**: `~/.env.dev`'s unconditional `override=True`
  load of `NEO4J_URI=bolt://localhost:7689` means this checkout cannot start today without
  either a workaround (as used for testing here, not suitable for real use) or a decision
  from Bill on how the new checkout is meant to win that precedence fight. The guard is
  correct and load-bearing exactly because of this — it is the reason a real launch attempt
  right now would be silently pointed at the frozen demo's graph instead of loudly refusing.
- **C6's block is a straight port, not a redesign.** It still assumes the launchd-plist /
  `~/hip-harness/data/dashboard/.operator_token` conventions hip-vo's checkout uses
  (`_DASHBOARD_TOKEN_PATH`, the `_neo4j_password()` plist fallback). Whether this checkout
  should share those paths with hip-harness/hip-vo or get its own was not decided or
  changed here — flagged, not assumed.
- **C1, C7, C8, C9, C10 remain entirely untouched** by this dispatch, same as the prior
  infra dispatch. No demo script exists on this base yet (C3/C4/C5 unstarted, as instructed
  — none was ported).
- Whether to commit `~/hip-cutover-demo`'s one modified file, and this dispatch doc's own
  registration, is Bill's call, not taken here.
