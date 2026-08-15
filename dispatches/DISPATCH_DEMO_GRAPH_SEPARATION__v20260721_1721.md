# DISPATCH_DEMO_GRAPH_SEPARATION
Status: DONE
Reconciled-Against: e975695 (roadmap); ~/hip-dev git_head 8cacb7ef2b70b023f752c89370f72f9b6a4eb57d (main, config-only changes, no code touched)

**TYPE:** INFRA / OPS — no REQ acceptance test; this is a prerequisite fix for REQ_CRYPTO_P4_RECOVERY_EVICTION's #5 (operator-cannot-read) audit and future master-key destruction, not itself a REQ.

## THE ASK

> SEPARATE THE DEMO SERVER'S GRAPH FROM THE #5 GRAPH. Document fully. Do NOT touch the master key. Do NOT stop mid-way and leave the demo broken. Commit WIP checkpoints.

Six steps: write this doc first (current state, before any change); find where the demo's Neo4j target is set; point the demo at its own graph without touching the roadmap graph; restart the demo cleanly and confirm it still works; verify the roadmap graph goes quiet (stable v1 count, no more churn); update this doc with what was actually done, commit, push. Explicitly NOT in scope: touching the master key, re-running the v1→v2 migration (both reserved for later, separately confirmed dispatches).

## CURRENT STATE (as of 2026-07-21, before this dispatch's change)

Discovered during the prior MASTER-KEY AUDIT and MIGRATE dispatches (this session): a live server, `server.demo_dashboard`, PID 21759, listening on port 7871, has been running since before this session started (`cwd=[REDACTED-USER-PATH]/hip-dev`, i.e. a **different checkout** from `~/hip-roadmap`, on **branch `main`**, not `roadmap`).

`main`'s `memory_engine/store.py` never received the Stage 4 crypto-partition work at all — confirmed by direct read: `from harness.encryption import KEY_VERSION, encrypt_fact_value` at the top, and the write path (`store.py:418`, `ciphertext, encrypted_dek = encrypt_fact_value(new_value, owner)`) calls the raw master-key-derived path unconditionally for every write. There is no `partition_classify_write`, no `DYAD_KEY_VERSION`, no class-sealing anywhere in that branch's `store.py`. Every fact this server writes lands as `key_version=1` — solo-decryptable by the master key alone, by construction (single Fernet-DEK sealed via `Fernet(_derive_key(owner))`, no member/dyad/care-team/household wrap of any kind).

Critically, this server's env (`ps eww -p 21759`) shows `NEO4J_URI=bolt://localhost:7688` — **the exact same "dev graph" the `roadmap` branch's REQ_CRYPTO_P4 work and #5 audit target.** It is not a coincidental collision on the URI string; both processes open the identical running Neo4j instance/database.

Consequence, observed directly: the MIGRATE dispatch immediately prior to this one successfully re-sealed all 12 then-live v1 facts to v2 (member/dyad/household-reachable), verified 12/12 round-trip-exact and member-reachable, 0 v1 remaining, full regression green. Within minutes, the demo server's own reset action (`server/demo_dashboard.py`'s reset endpoint, which calls `scripts/demo_seed.main()` on the `main`-branch code) wiped the graph and reseeded it fresh — **all 12 migrated v2 facts were deleted outright** (0 of the 12 fact_ids remained afterward), replaced with new `key_version=1` facts from a fresh seed plus two live text-session writes (`text-maya`, `text-bill`). The v1 count kept moving across repeated checks (14 → 13 → 11) — an actively live, uncoordinated writer, not a one-time collision.

**Why this blocks #5:** REQ_CRYPTO_P4_RECOVERY_EVICTION's #5 (operator-cannot-read, eventual master-key destruction) requires the master key to hold nothing solely. A one-time migration of `roadmap`'s own facts cannot establish that invariant while a separate, unrelated server on an unrelated branch keeps writing new master-key-only material into the exact same graph, indefinitely, outside `roadmap`'s control or visibility.

## THE FIX BEING APPLIED

Point `~/hip-dev`'s demo server at its **own**, separate Neo4j graph — leaving the shared `bolt://localhost:7688` graph exclusively for `roadmap`'s work. The demo's own crypto model (v1-only, master-key-derived) is unaffected by this change and is explicitly out of scope here; the demo keeps working exactly as it does today, just against different, dedicated storage. `roadmap`'s graph configuration is not touched — only the demo's target moves.

## INTENDED END STATE

- Demo server (`server.demo_dashboard`, `~/hip-dev`/`main`) targets a new, dedicated Neo4j graph — up, seeded, serving on port 7871 as before.
- The shared `bolt://localhost:7688` graph receives writes ONLY from `roadmap`-branch work going forward.
- `roadmap`'s live v1 count on 7688 is confirmed STABLE (no further churn) before any future migration re-run.
- Master key: untouched. Migration: not re-run this dispatch — both reserved for a later, separately confirmed step once the graph is provably quiet.

## STEP 2 — WHERE THE DEMO'S GRAPH TARGET WAS ACTUALLY SET (found before editing)

Not one setting — three, layered, and the third one is what made this dispatch take far longer than expected:

1. `~/hip-dev/.env.dev` (repo-local, gitignored): `export NEO4J_URI=bolt://localhost:7688`. Sourced by `dev.sh` and by the `com.hip.demo.dashboard` LaunchAgent's own env baseline expectations. Header comment already claimed "its own port, its own Neo4j instance" as the design intent for keeping hip-dev separate from `~/hip-harness`'s demo (7687) — but never got that same treatment relative to `roadmap`'s 7688, because at the time this file was written `roadmap` and `hip-dev` were presumably assumed to be the same environment, before the crypto-partition work diverged their data models.

2. `~/Library/LaunchAgents/com.hip.demo.dashboard.plist` — the ACTUAL runtime source of truth. `KeepAlive=true`, `RunAtLoad=true`, `EnvironmentVariables` baked directly into the plist (`NEO4J_URI=bolt://localhost:7688`, `NEO4J_PASSWORD=<matches ~/.zshrc's global default>`), completely bypassing shell-sourced `.env.dev` at runtime. This is why editing `.env.dev` alone and manually restarting the process kept reverting: `launchctl`'s `KeepAlive` respawns the process from the plist's own baked-in environment, not from any shell profile. It's also why `launchctl list` (run over SSH) showed nothing — GUI-session LaunchAgents (loaded under `gui/501`) are invisible to `launchctl list` run from a non-GUI SSH session; they only show up via `launchctl print gui/<uid>/<label>`, addressed directly by service target.

3. **`~/.env.dev`** (a SEPARATE file at the home directory root, not inside any checkout) — `server/demo_dashboard.py` has its own hand-rolled env loader (`_load_env_file`, not python-dotenv, which is why grepping for "dotenv" found nothing): it loads `ROOT/.env.dev` (repo-local, gap-filling only) THEN `~/.env.dev` **with `override=True`** — "the live key... overrides," per the code's own comment, originally meant only to patch in a working `OPENAI_API_KEY`/`ANTHROPIC_API_KEY` outside the repo. This file ALSO happened to carry a stale `export NEO4J_URI=bolt://localhost:7688`, and its `override=True` meant it silently clobbered every other fix — the repo's `.env.dev`, the plist's `EnvironmentVariables`, even an explicit inline shell env-var prefix on the launch command — every single time, right at `import server.demo_dashboard`. This was the actual reason the fix didn't "take" through two full plist bootout/bootstrap cycles and three different launch mechanisms; confirmed by direct before/after `os.environ` inspection across the `import` statement itself.

## STEP 3 — THE SEPARATION

New, fully dedicated Neo4j Community instance: `~/neo4j-hipdev-demo` (own `conf`/`data`/`logs`/`plugins`/`import`/`run` dirs, cloned from `~/neo4j-dev/conf/neo4j.conf` with paths retargeted), bolt on `:7689`, HTTP on `:7476` (both previously unused on this box — `7688`/`7475` stay roadmap's, `7687`/`7474`-ish stay hip-harness's demo). Fresh admin password generated (`openssl rand -base64 24`, stripped of `/+=`), set via `neo4j-admin dbms set-initial-password` before first boot (Neo4j's own documented requirement), instance started via `neo4j start` with `NEO4J_HOME`/`NEO4J_CONF` pointed at the new dirs — same pattern `dev.sh` itself uses for the 7688 instance, just parameterized differently. Verified reachable and empty (0 nodes) via the Python driver before touching anything else.

All three config layers above updated to point at the new instance, all three consistently:
- `~/hip-dev/.env.dev`: `NEO4J_URI=bolt://localhost:7689`, plus `NEO4J_PASSWORD` pinned explicitly (a deliberate deviation from the file's own "never pin it" convention, documented inline in the file itself — this checkout's credential now answers to nothing else on the box, no coupling to `~/.zshrc`'s global default).
- `~/Library/LaunchAgents/com.hip.demo.dashboard.plist`: same `NEO4J_URI`/`NEO4J_PASSWORD` values, backed up to `~/hip-p4-migration-backups/20260721_165446/plist-backups/com.hip.demo.dashboard.plist.orig` before editing, reloaded via `launchctl bootout gui/501/com.hip.demo.dashboard` + `launchctl bootstrap gui/501 <plist>` (the correct pair for a GUI-session LaunchAgent — plain `kill` + manual relaunch doesn't survive `KeepAlive`, and doesn't NEED to once the plist itself is fixed).
- `~/.env.dev` (home root): `NEO4J_URI=bolt://localhost:7689` (its only Neo4j-related line; no `NEO4J_PASSWORD` in this file, so the plist's pinned password flows through untouched once the URI conflict is resolved).

No `roadmap` file touched. No `hip-dev` CODE touched — every change here is to `.env.dev` files (gitignored, or entirely outside any repo) and one `.plist`, never to `server/demo_dashboard.py` or any other tracked source.

## STEP 4 — RESTART CONFIRMATION

`launchctl kickstart -k gui/501/com.hip.demo.dashboard` after the final config fix. `GET /api/preflight`: `all_ok: true`, `neo4j: {"ok": true, "detail": "connected bolt://localhost:7689"}`. Ran `scripts/demo_seed.main()` directly against the new instance: `11/11 fact(s) seeded` (Maya/Sam/Dad fixture, D1–D11), `rc: 0`. Confirmed independently via the driver: 11 live facts on 7689. `GET /api/status` (the dashboard's own live UI poll target): `{"neo4j": true, "member_count": 3, "fact_count": 11, "routing_count": 3}`. The demo is fully up, seeded, and serving on port 7871 — unbroken.

## STEP 5 — ROADMAP GRAPH (7688) NOW QUIET

Checked three times: immediately after separation (11 live facts, all `key_version=1`, leftover from before the fix), again ~3 minutes later (11, same key_version breakdown), and again ~15 seconds after that (11, with the exact same 11 `fact_id`s, byte-for-byte identical set both times). Contrast with the MIGRATE dispatch's observed behavior before this fix: the count moved 14 → 13 → 11 within seconds of repeated checks, an actively live writer. It is now stable — no external writer touching 7688 anymore.

**Stable v1 count on 7688: 11.** These are NOT the 12 facts the MIGRATE dispatch re-sealed (those are confirmed gone — wiped by the demo's reset-and-reseed before this dispatch started); they are a later demo-seed generation's leftovers, now frozen in place since the demo no longer writes here. Migrating them is the next, separate, explicitly-deferred step.

## OUTCOME

Master key: untouched, as instructed. Migration: not re-run, as instructed. Demo: not left broken at any point after the final fix landed — verified up, connected, seeded, serving. `roadmap`'s graph is now exclusively `roadmap`'s, confirmed quiet by direct observation rather than assumed from the config change alone.
