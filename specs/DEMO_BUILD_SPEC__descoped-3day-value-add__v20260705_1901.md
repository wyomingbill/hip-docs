# DEMO BUILD SPEC — descoped 3-day value-add build (one screen, three zones)
STATUS: PLAN
SUPERSEDES: specs/DEMO_BUILD_SPEC__one-screen-three-zones__v20260705_1844.md
RECONCILED-AGAINST: code main d2013e3, 2026-07-05

Descoped amendment of v20260705_1844. Two cuts, everything else carried
forward. Target ~3 focused days. Voice CAPTURE remains out; **TTS
playback is now also out** — deferred to the voice track.

---

## Cut from scope (later, with the voice track)

**C1 — TTS playback / Kokoro voices.** Removes the hip-dev Kokoro
dependency (`harness/speech.py::KokoroTTS`, model files living only in
`~/hip-harness/models/`) and its preflight check entirely. Instead each
script utterance displays as TEXT in the top band as it fires; **the
operator narrates.** The v2 script format keeps its `voices` map as
inert display metadata (§1) so scripts written now survive the TTS
return unchanged.

**C2 — In-browser script editor.** No `PUT /api/demo/script/{name}`, no
mid-run 409 machinery (prior spec R5 — now moot). Scripts are edited as
files on disk in `demo_scripts/`. The screen needs exactly two controls:
a dropdown listing available scripts and a START button (plus STOP).

## Unchanged from v20260705_1844 (restated where load-bearing)

### §0 Architecture: runner drives `text_demo.run_query()` in-process

Unchanged and load-bearing. The epistemic record (admitted/withheld/
delta → `logs/turns_demo.jsonl`) is built only in
`scripts/text_demo.py::_run_one` (129-204); `run_query()` also writes
`router.jsonl` and the transcript — one call feeds all three zones. The
voice server is not a demo-day dependency (no STT, no `/api/text-query`,
no TD-103 exposure). Verified deterministic 3× (preflight check 5b).

### §1 Script model — format v2, dropdown + START only

Format v2 in `demo_scripts/*.json`, merging the two existing formats
(`demo_scripts/*.json` v1: members + assertions, read by
run_demo_script.py; `data/demo_script.json`: voices + narrator lines,
read by demo_player.py):

```json
{
  "version": "2",
  "name": "three_zone_demo",
  "description": "Establish / operator-update / scripted-update",
  "voices": {"maya": "af_heart", "sam": "am_adam", "hip": "af_bella"},
  "turns": [
    {"id": "E01", "movement": 1, "member": "maya",
     "text": "Ray takes metformin 500mg twice daily",
     "pause_ms": 2500, "expect_tier": "edge",
     "note": "operator narration cue — displayed, never spoken"}
  ]
}
```

- `movement`: 1=establish, 2=operator-update, 3=scripted-update.
  Display metadata; the screen shows a divider when it changes.
- `voices`: **inert until TTS returns** (C1). Validated as a dict if
  present, otherwise ignored.
- `expect_*` optional; asserted per turn into the status file (reuses
  run_demo_script.py's assertion logic).
- `note`: operator narration cue, shown small in the status strip.

Endpoints (all on demo_dashboard.py, read/execute only — no writes):
- `GET  /api/demo/scripts` — list name/description/turn-count of
  `demo_scripts/*.json` where `version == "2"`.
- `POST /api/demo/start {name}` — spawn runner. `name` validated
  `^[a-z0-9_]+$`, resolved strictly inside `demo_scripts/`.
- `POST /api/demo/stop` — terminate runner.
- `GET  /api/demo/status` — contents of `logs/demo_run_status.json`.

### §2 Runner — NET-NEW `scripts/demo_run.py`, no TTS

Subprocess spawned by the dashboard (`run_query` imports
`server.voice_orch` → pipecat + ~20 s edge-model warmup; must not block
uvicorn). Status file `logs/demo_run_status.json` written on every state
change:

```json
{"state": "warming|running|done|error|stopped",
 "script": "three_zone_demo", "turn_index": 4, "turn_total": 12,
 "current_turn_id": "U02", "movement": 2, "note": "…",
 "assertions": [{"id":"E01","field":"tier","expect":"edge","got":"edge","ok":true}],
 "started_at": "…", "error": null}
```

Per-turn sequence (TTS steps deleted): update status (movement banner,
narration `note`) → `await text_demo.run_query(text, member)` → sleep
`pause_ms` → next. Pacing is entirely `pause_ms`; the operator narrates
over it. Machine/folder guard identical to demo_reset.sh:12-25.

### §3 Top band — conversation (endpoint + UI NET-NEW)

Capture exists (`harness/transcript_log.py:79`, JSONL per session under
`logs/transcripts/`; nothing serves it). NET-NEW
`GET /api/transcript?since=<iso>&n=` merges all
`logs/transcripts/*.jsonl` with `ts >= since`, sorted by `ts` — merge is
required because the runner produces one session per member
(`text-maya`, `text-sam`; voice_orch.py:2114). UI: two-column band,
user rows left (member chip + utterance), hip rows right; movement
divider from the status file; 2 s poll; stone palette tokens from
epistemic.html.

### §4 Bottom-left — routing + vault (EXISTS, one fix + re-layout)

`RoutingRow`/`TierBar` (demo_dashboard.py:454-524) and
`VaultSection`/`FactRow` (526-610) exist. Two-part Bloom fix:
1. **Root cause:** harness/router.py:583 discards the computed `_bloom`
   on the exemplar-tiebreak path — propagate it so exemplar-routed rows
   carry a real Bloom value.
2. Field mismatch: renderer reads `e.bloom_level`, writer emits `bloom`
   (router.py:126) — `/api/routing` normalizes
   `bloom_level = e.get("bloom_level") or e.get("bloom")`.
Rows with genuinely uncomputed bloom still show `---`; never fabricate.

Vault ports in as its own speaker-toggled panel beside the routing
table. **R1 stands: not a per-utterance column.**

Layout: extract components from the `_HTML` Babel blob (demo_dashboard.py
:383+) into NET-NEW `server/static/demo.html`, served at `GET /demo`.
The `/` page stays untouched as fallback.

### §5 Bottom-right — per-FACT epistemic timeline (endpoint + renderer NET-NEW)

**R2 stands: per-fact rows,** never per-utterance. NET-NEW read-only
`GET /api/fact_history`: one Cypher pass over all `:Fact` nodes grouped
by `(attribute, owner, subject)` ordered by `valid_from`, chain-linked
via `superseded_by` (set by `memory_engine/store.py::_tx_supersede`,
226-250), values decrypted via `harness.encryption.decrypt_fact_value`,
each node classified with `trust()` (truth_layer/queries.py),
`confidence_log` transitions included per node (store.py:126). Response
shape as v20260705_1844 §5. Renderer: one row per chain; cells
left-to-right (trust badge + value; closed cells struck with
`closed_reason`; open cell bold; arrows labeled with `write_state`);
4 s poll; epistemic.html trust-badge tokens.

**R6 honored (see sample script below):** the live write path produces
SUPERSEDE transitions only. Confidence-change cells render only where
`demo_seed.py` enriched `confidence_log`. No script or narration cue may
promise a live confidence change.

### §6 Proof beat — headline affordance, spec'd properly

This closes the show; it is not a cat command. NET-NEW:

- `GET /api/demo/proof` returns, for each proof source:
  `{key, label, path, line_count, mtime, sha256_8, tail: [last 12 raw lines]}`.
  Sources: `logs/router.jsonl` (routing decisions),
  `logs/turns_demo.jsonl` (epistemic records incl. delta),
  `logs/transcripts/*.jsonl` (verbatim conversation, one entry per file),
  `logs/demo_run_status.json` (script + per-turn assertions), and a
  live re-query of `/api/fact_history` (what the right zone read, direct
  from Neo4j — not a file, labeled as such).
- **PROOF button** in the screen footer → full-screen overlay, one tab
  per source. Each tab: file path + line count + mtime + short hash in a
  header strip, raw JSONL lines in a monospace scroll region, and a
  one-line caption tying it to the zone it fed ("every row in the
  routing table above came from this file"). The `sha256_8` and mtime
  make the "this was written during the run you just watched" claim
  checkable — the operator can compare mtime against the run's
  `started_at` on the status tab.
- Overlay is read-only; files persist after the run for terminal
  inspection by a skeptic.

### §7 Port — DASH_PORT

`export DASH_PORT=7871` in `.env.dev`; `start_dashboard.sh` and
`demo_preflight.sh` check 2b switch from `$PORT` to `$DASH_PORT`.
`PORT=7863` reverts to its documented meaning (dev voice server — see
.env.dev comment "demo uses 7860 — do not collide"). Tailnet-only bind
(commits f666db9/24b1cc9) unchanged. With TTS cut, nothing in this build
binds any port except the dashboard.

## Sample script (R6-safe), ships as `demo_scripts/three_zone_demo.json`

Movement 1 (establish): queries against seeded D1-D9 — routing rows,
vault decrypt beat, timeline shows seeded chains incl. D9's seeded
CORROBORATED hardening (the ONLY confidence transition on screen, and
the note says "seeded corroboration", not "watch it change").
Movement 2 (operator-update): operator-attributed supersede beats —
e.g. maya: "Ray switched from metformin to Jardiance 10mg last week" →
live SUPERSEDE cell appears on D9's row (verified reproducible,
preflight 5b). Movement 3 (scripted-update): sam-attributed supersede on
a D4/D5 fact, same shape. All narration cues describe supersede/
reclassification only.

## Revised build order + honest estimates

| step | work | status | estimate |
|---|---|---|---|
| 1 | DASH_PORT=7871 (.env.dev, start_dashboard.sh, preflight 2b); `/demo` skeleton (three-region grid) | net-new (small) | 0.25 d |
| 2 | Bloom fix (router.py:583 propagation + /api/routing normalize); port RoutingRow/TierBar/VaultSection into `/demo` | fix + re-layout of EXISTING | 0.5 d |
| 3 | `GET /api/fact_history` + horizontal per-fact renderer | net-new | 1 d |
| 4 | `GET /api/transcript` + top-band two-column UI | net-new (capture exists) | 0.5 d |
| 5 | `scripts/demo_run.py` (v2 format, no TTS, status file, assertions) + `/api/demo/{scripts,start,stop,status}` + dropdown/START/STOP UI | net-new | 0.5 d |
| 6 | PROOF endpoint + overlay; `demo_run.sh`; preflight additions (DASH_PORT; drop Kokoro check); sample v2 script | net-new (small) | 0.25-0.5 d |

**Total: 3-3.25 days.** The 5-7.5 d of v20260705_1844 shed ~2 d of TTS
voices, editor machinery, and the Kokoro preflight surface.

Gate discipline: `scripts/gate_check.sh` 6/6 must stay green after every
step; step 2 touches `harness/router.py` (live routing path) so the
routing harness threshold check is the specific guard there; any bug
found ratchets into a MEM/INT scenario before its fix merges.

## DEMO-SAFETY

**One operator action:** NET-NEW `scripts/demo_run.sh` — machine/folder
guard → `source .env.demo` → `demo_reset.sh` (wipe + seed D1-D9,
verified identical across 3× cycles) → `start_dashboard.sh` (tailnet
bind, retry-checked) → `demo_preflight.sh` must exit 0 (delta smoke-test
5b included; Kokoro check dropped per C1) → prints the `/demo` URL.
Operator opens it, picks the script, presses START — the single
show-time action; the run then populates all three zones
deterministically to completion.

**Determinism:** seed + supersede beats verified reproducible (3×). Groq
(fact-change detection) is the one nondeterministic dependency; its
failure mode is a missing delta cell, never a crash (timeout → clean
no-op). Script places movement-2/3 supersede beats on movement-1/seed
facts — the verified shape.

**Exposure (TD-101; register has no TD-107 — TD-101 is the operative
item):** every new endpoint inherits the dashboard's Tailscale-or-
loopback bind, never 0.0.0.0. With C2 cut there are no write endpoints;
`POST /api/demo/start` is the only execute endpoint — name whitelisted
`^[a-z0-9_]+$`, resolved strictly inside `demo_scripts/`, one run at a
time (second start while running → 409).

## Rejections carried forward

- **R1:** encryption as per-utterance column — vault panel instead.
- **R2:** per-utterance epistemic rows — per-fact rows.
- **R3:** off-net beats — `SERPAPI_KEY` placeholder; all rows show ON.
- **R4:** live mic/STT — out (now joined by TTS playback, C1).
- **R5:** retired with C2 — no editor, nothing to desync.
- **R6:** narrated live confidence-change beats — live path produces
  supersede only; sample script §above complies.
