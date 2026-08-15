# DEMO BUILD SPEC — one screen, three zones, script-driven with TTS playback
STATUS: PLAN
RECONCILED-AGAINST: code main 26e1b13, docs/planning/DEMO_DESIGN_REVIEW__three-zone-demo-buildability__v20260705_1829.md, 2026-07-05

Build spec for the 10-15 min single-screen demo. Scope per direction:
**voice CAPTURE is out** (no mic, no STT); **TTS playback of a scripted
run is in**. One screen, three live regions, driven by an editable script
the operator starts from the screen. Every turn exercises the real
pipeline and leaves log files openable at the close as proof.

This spec builds on the design review's verdicts. Where a component
EXISTS it is cited; where it is NET-NEW it is spec'd concretely and
estimated on its own line.

---

## 0. Architecture decision that simplifies everything

**The runner drives turns through `scripts/text_demo.run_query()`
in-process — NOT through `POST /api/text-query`.**

Rationale (from the design review): the epistemic record
(admitted/withheld/delta → `logs/turns_demo.jsonl`) is built only in
`scripts/text_demo.py::_run_one` (lines 129-204). The voice server's
`/api/text-query` (server/voice_https_orch.py:94) runs the same pipeline
but writes no epistemic record. Driving `run_query()` directly means:

1. The right zone (epistemic) gets fed for every scripted turn — the
   design review's "dual-input unification" gap disappears from this
   demo's scope entirely.
2. **The voice server is not a demo-day dependency at all.** No STT, no
   `/api/text-query`, no TD-103 launchd risk on the critical path.
3. The port collision resolves itself (see §7).

`run_query()` already: runs the real decide → injection → route →
generate path (`process_text_query`, server/voice_orch.py:2098), fires
fact-change detection, waits for the delta, writes `router.jsonl`,
`turns_demo.jsonl`, and the transcript. It is the single call that
populates all three zones. Verified deterministic 3× this session
(preflight check 5b, scripts/demo_preflight.sh).

---

## 1. Script model — NET-NEW format v2, reusing existing pieces

Two script formats exist today; neither fits alone:
- `demo_scripts/*.json` (v1, read by scripts/run_demo_script.py):
  `{id, member, text, expect_tier, expect_intent, pause_ms, narrate, note}`
  — has assertions and members, no voices, no movements, posts to
  `/api/text-query` (wrong path per §0).
- `data/demo_script.json` (read by scripts/demo_player.py):
  `{query, narrate, narrator_line, pause_ms}` + top-level
  `narrator_voice`/`hip_voice` — has TTS voices, no member, no movement.

**Spec: format v2**, superset of v1, lives in `demo_scripts/`:

```json
{
  "version": "2",
  "name": "three_zone_demo",
  "description": "Establish / operator-update / scripted-update",
  "voices": {
    "maya":     "af_heart",
    "sam":      "am_adam",
    "narrator": "am_michael",
    "hip":      "af_bella"
  },
  "turns": [
    {
      "id": "E01",
      "movement": 1,
      "member": "maya",
      "text": "Ray takes metformin 500mg twice daily",
      "narrate": false,
      "narrator_line": null,
      "pause_ms": 2500,
      "expect_tier": "edge"
    }
  ]
}
```

- `movement`: 1=establish, 2=operator-update, 3=scripted-update. Display
  metadata only — the runner treats all turns identically; the screen
  shows a movement divider when it changes.
- `member` is the speaker; `voices[member]` is the TTS voice.
- `expect_*` fields optional; when present the runner logs
  PASS/FAIL per turn to the status file (reuses run_demo_script.py's
  assertion logic).

**Where scripts live:** `demo_scripts/*.json` (existing dir; the three
v1 scripts stay valid for the CLI player; the runner accepts v2 only).

**Screen load/edit/start (NET-NEW, all on demo_dashboard.py):**
- `GET  /api/demo/scripts` — list `demo_scripts/*.json` (name, version,
  description, turn count).
- `GET  /api/demo/script/{name}` — raw JSON content.
- `PUT  /api/demo/script/{name}` — write edited JSON back to the file
  (validated against the v2 shape before write; 400 on parse error).
- `POST /api/demo/start {name}` — spawn the runner (§2) on that file.
- `POST /api/demo/stop` — terminate the runner.
- `GET  /api/demo/status` — runner state (see §2).

Editability without redeploy: the screen shows the selected script in a
textarea; PUT saves to disk; the runner reads the file fresh at start.
Edits mid-run apply to the *next* run — mid-run mutation is rejected
(see Rejections, R5).

## 2. Runner + TTS playback — NET-NEW `scripts/demo_run.py`

A merge of run_demo_script.py (script walk + assertions) and
demo_player.py (TTS), driving `text_demo.run_query()` per §0.

**Process model:** the dashboard spawns it as a subprocess
(`subprocess.Popen([venv python, "scripts/demo_run.py", "--script", path])`).
Not in-process: `run_query` imports `server.voice_orch`, which pulls
pipecat + warms the edge model (~20 s, observed every text_demo run this
session). That warmup must not block uvicorn. The runner writes
`logs/demo_run_status.json` after every state change:

```json
{"state": "warming|running|done|error|stopped",
 "script": "three_zone_demo", "turn_index": 4, "turn_total": 12,
 "current_turn_id": "U02", "movement": 2,
 "assertions": [{"id":"E01","field":"tier","expect":"edge","got":"edge","ok":true}],
 "started_at": "...", "error": null}
```

`GET /api/demo/status` returns this file; the screen polls it at 1 s to
drive the movement banner and progress indicator.

**TTS path (EXISTS, reused):** `demo_player.py::_TTSEngine` wraps
`harness/speech.py:90 KokoroTTS` (kokoro_onnx). Model files are NOT in
hip-dev (`models/` does not exist here); `.env.demo` points
`KOKORO_MODEL_PATH`/`KOKORO_VOICES_PATH` at `~/hip-harness/models/
kokoro-v1.0.onnx` + `voices-v1.0.bin` — both verified present.
**Read-only use of hip-harness model files is a demo-day prerequisite;
preflight must assert both paths exist** (new preflight sub-check).
The runner builds one `_TTSEngine` per distinct voice in
`script["voices"]`, cached. TTS failure degrades to `--silent` exactly
as demo_player.py does today (warn once, print instead).

**Per-turn sequence (this is the timing/sync spec):**
1. Movement banner update (status file) if `movement` changed.
2. Optional narrator line spoken in `voices.narrator`.
3. Utterance spoken in `voices[member]` — blocking (`sd.wait()`).
4. `await text_demo.run_query(text, member)` — the real pipeline. On
   return, `router.jsonl`, `turns_demo.jsonl`, and the transcript are
   already written; every zone's next poll (2-4 s) picks the turn up.
5. HIP's reply (from the turn record) spoken in `voices.hip` — the
   screen populates *while* the reply is being spoken, which is the
   natural sync: the audience hears the answer as the zones light up.
6. Sleep `pause_ms`, next turn.

No STT anywhere. No mic. Playback only.

## 3. Top band — conversation (capture EXISTS, endpoint + UI NET-NEW)

Per the design review: transcripts are written by
`harness/transcript_log.py:79 write_transcript_turn` (JSONL per session
under `logs/transcripts/`), by both the text path and voice path, but
nothing serves them.

**NET-NEW `GET /api/transcript?since=<iso>&n=<max>`** on
demo_dashboard.py: merge all `logs/transcripts/*.jsonl` records with
`ts >= since`, sort by `ts`, return newest-`n`. Merging matters because
the runner produces one session per member (`text-maya`, `text-sam` —
session_id convention in process_text_query, voice_orch.py:2114), so a
single-session tail would drop half the conversation.

**NET-NEW UI:** two-column band. `speaker=="user"` rows left (member
chip + utterance), `speaker=="hip"` rows right (reply). Rows appear on
poll (2 s). Movement divider inserted when the status file's movement
changes. Reuses epistemic.html's stone palette tokens.

## 4. Bottom-left — routing pipeline + vault (EXISTS, one fix + re-layout)

**EXISTS:** `RoutingRow`/`TierBar` (server/demo_dashboard.py:454-524)
render query | sensitivity chip | Bloom label | horizontal 5-tier bar
with selected tier lit | model target | ON/OFF-net — fed by
`GET /api/routing` reading `logs/router.jsonl` (written by
harness/router.py:628).

**The bloom fix (flagged in the review), two lines:**
1. Renderer reads `e.bloom_level` but the writer emits `bloom`
   (harness/router.py:126). Fix in `/api/routing`: normalize
   server-side — `e["bloom_level"] = e.get("bloom_level") or e.get("bloom")`.
2. Root cause of null blooms: on the exemplar-tiebreak path the computed
   bloom is discarded (`_bloom` unused, harness/router.py:583). Propagate
   it so exemplar-routed rows carry a real value. Rows where bloom is
   genuinely not computed still show `---` — do not fabricate.

**Vault panel (EXISTS):** `VaultSection`/`FactRow`
(demo_dashboard.py:526-610) — member tabs, operator-view ciphertext,
HKDF animation, per-member decrypt via `POST /api/decrypt`. Ported into
the bottom-left zone as its own speaker-toggled panel beside the routing
table. **Rejection R1 stands: encryption is a property of facts at rest,
not utterances — it is NOT a per-utterance column.**

**Re-layout:** the components live as inline Babel JSX in the `_HTML`
string of demo_dashboard.py (line 383+). Extract into a new
`server/static/demo.html` single-screen page (top band / bottom-left /
bottom-right grid) served at `GET /demo`. The existing `/` page stays
untouched as a fallback.

## 5. Bottom-right — epistemic timeline (data EXISTS, endpoint + renderer NET-NEW)

**Per-FACT rows — Rejection R2 stands.** State changes attach to facts,
not utterances; one utterance can mutate a fact created five turns
earlier, which would force the UI to rewrite an old row. Per-fact rows
with timeline cells appearing left-to-right avoid that entirely.

**NET-NEW `GET /api/fact_history`** (read-only, demo_dashboard.py):
walks every supersede chain. Data verified present (design review §3):
`superseded_by` + `valid_to` + `closed_reason` set by
`memory_engine/store.py::_tx_supersede` (226-250); `confidence_log`
transition entries (store.py:126); `trust()` classification on demand
(truth_layer/queries.py).

Response shape:

```json
[{"attribute": "medication", "owner": "maya", "subject": "ray",
  "chain": [
    {"fact_id": "…", "value": "Ray takes metformin 500mg…",
     "trust": "CORROBORATED", "write_state": "supersede",
     "valid_from": "…", "valid_to": "…", "closed_reason": "superseded",
     "confidence_transitions": [{"ts":"…","from":"medium","to":"high","source":"reconcile"}]},
    {"fact_id": "…", "value": "Jardiance 10mg",
     "trust": "ASSERTED", "write_state": "supersede",
     "valid_from": "…", "valid_to": null}
  ]}]
```

Implementation: one Cypher query for all `:Fact` nodes grouped by
`(attribute, owner, subject)`, ordered by `valid_from`; chain-link via
`superseded_by`; decrypt values via `harness.encryption.
decrypt_fact_value` (same as `/api/decrypt`); classify each node with
`trust()`. Poll at 4 s.

**NET-NEW renderer:** one row per chain; cells left-to-right, each cell =
trust badge + value (closed cells struck/dimmed with `closed_reason`,
open cell bold), arrow between cells labeled with `write_state`. Reuses
the epistemic.html trust-badge tokens (`b-CONFIRMED` … `b-ASSERTED`).

**Honest constraint, stated for the script author:** supersede
transitions render richly from live turns. Confidence-change beats
(`CORROBORATED` hardening) exist only where `demo_seed.py` seeded them —
the live path writes only the initial `source:"write"` entry
(store.py:126). **The v2 script MUST NOT contain a narrator line
promising a live confidence-change; the timeline will not show one.**

## 6. Log files / proof — the "revert to the logs" beat

Written during every run, all under `~/hip-dev/logs/`:

| file | written by | proves |
|---|---|---|
| `router.jsonl` | harness/router.py:628, every routed turn | tier/bloom/sensitivity decisions were real |
| `turns_demo.jsonl` | text_demo.py `_append_demo_log`, every runner turn | admitted/withheld/delta per turn (the epistemic record) |
| `transcripts/text-<member>.jsonl` (+ .txt) | transcript_log.py:79 | verbatim conversation |
| `fact_lifecycle/*.ndjson` | extraction_queue TD-050 logger | every proposed/applied fact mutation |
| `demo_run_status.json` | scripts/demo_run.py (NET-NEW) | script id, per-turn assertions PASS/FAIL |
| Neo4j graph itself | store.py encode() | supersede chains queryable live |

**NET-NEW screen affordance:** a `PROOF` button in the screen footer →
`GET /api/demo/proof` returns, for each file above: absolute path, line
count, mtime, and the last 10 raw lines. Rendered in a monospace modal —
the operator clicks PROOF at the close, the audience sees the raw JSONL
that fed the screen. Complementary command for the skeptic:
`tail -f logs/turns_demo.jsonl` in a terminal during the run.

## 7. The port collision — resolved

`.env.dev` exports `PORT=7863` with the comment "Dev voice server port
(demo uses 7860 — do not collide)". The 2026-07-05 fix pinned the
dashboard to that same `$PORT`, so dashboard and dev voice server now
claim the same port.

**Does it matter TTS-only? On demo day: no.** Per §0 the voice server is
not started at all — no STT, no `/api/text-query`. TTS is in-process
audio in the runner subprocess (kokoro_onnx → sounddevice); it binds no
port. Nothing collides in the demo configuration.

**Resolve it anyway** so the landmine doesn't fire when the voice track
returns: add `export DASH_PORT=7871` to `.env.dev`;
`scripts/start_dashboard.sh` and `scripts/demo_preflight.sh` check 2b
switch from `$PORT` to `$DASH_PORT`. `7863` reverts to meaning exactly
what its comment says. Tailscale-only bind behavior (commits `f666db9`,
`24b1cc9`) is unchanged. Trivial cost, folded into build step 1.

---

## Build order (net-new isolated), with honest estimates

| step | work | status | estimate |
|---|---|---|---|
| 1 | `DASH_PORT=7871` (+ start_dashboard.sh, preflight 2b); `/demo` page skeleton — three-region grid, stone palette | net-new (small) | 0.5 d |
| 2 | Bloom fix (router.py:583 propagation + /api/routing normalize); port RoutingRow/TierBar/VaultSection into `/demo` | fix + re-layout of EXISTING | 0.5-1 d |
| 3 | `GET /api/fact_history` + horizontal per-fact renderer | **net-new** | 1.5-2 d |
| 4 | `GET /api/transcript` + top-band two-column UI | **net-new** (capture exists) | 0.5-1 d |
| 5 | `scripts/demo_run.py`: v2 script format, per-speaker Kokoro voices, `run_query()` drive, status file, assertions | **net-new** (merges two existing CLIs) | 1-1.5 d |
| 6 | Script select/edit/start UI + `/api/demo/*` endpoints | **net-new** | 0.5-1 d |
| 7 | PROOF affordance + `demo_run.sh` + preflight additions (Kokoro paths, DASH_PORT) | net-new (small) | 0.5 d |

**Total: 5-7.5 focused days.** Higher than the design review's 4-6
because TTS playback and script-from-screen entered scope; the dual-input
unification (1-2 d) left it (§0).

Suggested order is as numbered: 1-2 give a populated screen from
existing data in a day, 3-4 complete the three zones, 5-6 make it
operator-driven, 7 hardens the show.

## DEMO-SAFETY

**One operator action to a running, populated screen:**
NET-NEW `scripts/demo_run.sh` (referenced concept, now spec'd):
1. Machine/folder guard (same block as demo_reset.sh:12-25).
2. `source .env.demo` — brings NEO4J_PASSWORD, KOKORO_* paths, DEMO_MODE.
3. `scripts/demo_reset.sh` — wipe + seed D1-D9 (deterministic; verified
   identical across 3× reset/seed cycles this session).
4. `scripts/start_dashboard.sh` — kills stale processes, binds
   Tailscale-IP-or-loopback, retry-checked start.
5. `scripts/demo_preflight.sh` — must exit 0 (includes the delta
   smoke-test check 5b: subject=ray, from_state=CORROBORATED,
   transition=supersede; plus new Kokoro-paths check).
6. Prints the `/demo` URL. Operator opens it, selects the script,
   presses START. That press is the single show-time action.

**Determinism:** seed graph verified identical across 3 runs; the
metformin→Jardiance delta verified identical across 3 clean cycles
(preflight 5b now gates it). Groq is the one non-deterministic
dependency (fact-change detection, harness/fact_change.py); its failure
mode is a missing delta cell, never a crash (timeout → clean no-op,
design review §3a). The script should place movement-2/3 supersede beats
on facts seeded by movement 1, which is the verified-reproducible shape.

**Exposure (TD-101):** all new endpoints (`/api/demo/*`,
`/api/transcript`, `/api/fact_history`) inherit the dashboard's bind:
Tailscale interface or loopback, never 0.0.0.0 (start_dashboard.sh,
commits f666db9/24b1cc9). `PUT /api/demo/script/{name}` and
`POST /api/demo/start` are write/execute endpoints on an
unauthenticated server — acceptable ONLY because of tailnet-only bind;
they must validate `name` against a whitelist regex
(`^[a-z0-9_]+$`) and resolve strictly inside `demo_scripts/` (no path
traversal). Note: the register has no TD-107; TD-101 is the operative
exposure item, and the demo must never run with a 0.0.0.0 bind.

**Proof:** run ends → PROOF modal (§6) shows the raw logs the screen was
fed from. Files persist after the run for terminal inspection.

## Rejections (carried forward + new)

- **R1 (stands):** encryption as a per-utterance column — fights the
  at-rest encryption model; vault panel keyed to facts × speaker instead.
- **R2 (stands):** per-utterance epistemic rows — state attaches to
  facts; per-fact rows with left-to-right cells.
- **R3 (stands):** any off-net beat — `SERPAPI_KEY` is a placeholder in
  `.env.dev`; every row will show ON-net. The v2 script must not narrate
  an off-net flip.
- **R4 (new, scope):** live mic / STT — out by direction. The runner
  never touches WhisperSTT; `harness/speech.py` is used for KokoroTTS
  only.
- **R5 (new):** mid-run script editing — the runner reads the file once
  at start; allowing live mutation means the status file, assertions,
  and TTS cache can desync from what's on disk. Edits apply to the next
  run; the PUT endpoint returns 409 while a run is active.
- **R6 (new):** narrated live confidence-change beats — the live write
  path cannot produce them (§5 honest constraint); only seeded facts
  show hardening transitions. Scripts promising them will demo a blank.
