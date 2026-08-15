# DEMO DESIGN REVIEW — three-zone demo buildability verdict
STATUS: BUILT
RECONCILED-AGAINST: code main 24b1cc9, 2026-07-05

Read-only engineering review of the proposed 10-15 min single-screen demo
(top band: live conversation; bottom-left: per-utterance pipeline table +
speaker-aware encryption; bottom-right: per-fact epistemic timeline; dual
input: live voice + dropdown-triggered scripted utterances). Every claim
cited against actual code. No build performed.

---

## 1. Left pipeline table — EXISTS

Never deleted. It is the inline React app served at `GET /` of
`server/demo_dashboard.py` (the `_HTML` blob starting ~line 383), built up
across commits `8571bb9` → `04b3a96` → `2192de8` → `89af478` → `64a6bc6`.

`RoutingRow` (demo_dashboard.py:454-490) renders per-utterance:
**query text | sensitivity class chip | Bloom label ("Remember"…"Create") |
TierBar | model target | ON/OFF-net chip**. `TierBar` (line 429) is the
"horizontal options" ask verbatim: all five tiers as segments, selected one
lit and glowing, past tiers dimmed.

Speaker-aware encryption also exists — `VaultSection` + `FactRow`
(lines 526-610): member tabs (OPERATOR VIEW / MAYA SPEAKS / SAM SPEAKS),
operator sees `ENCRYPTED · AES-256-GCM` chips, selecting a member runs an
HKDF key-derivation animation then decrypts owned + household facts via
`POST /api/decrypt`; non-owned facts stay locked. The disclosure rule, made
visible.

Caveats:
- Fed by `GET /api/routing` reading `logs/router.jsonl`. Live sample line
  confirms `query`, `tier`, `tier_target`, `sensitivity_tag`,
  `on_net_sensitive` present — but the log field is `bloom` (null on the
  sampled text-path row) while `RoutingRow` reads `e.bloom_level`. Bloom
  column shows `---` for text-path rows until this one-field mismatch is
  fixed.
- Encryption is a separate zone keyed to facts, not a table column keyed to
  utterances — see rejection R1.

Rebuild estimate: **0.5-1 day** re-layout, not a rebuild.

## 2. Dual input — same pipeline, NOT the same dashboard state

Processing path is genuinely shared: voice `_on_user_text` and
`process_text_query` (server/voice_orch.py:2098) both run
`TurnOrchestrator.decide` → injection contract → tiered generate →
`detect_and_apply_async`; voice_orch.py:1427 comments "mirrors
process_text_query's control-flow block." Both write `router.jsonl`
(left table ✓) and transcripts via `harness/transcript_log.py` (top band ✓).

**The epistemic capture is NOT shared.** The admitted/withheld/delta record
is built only in `scripts/text_demo.py::_run_one` (lines 129-204) and
appended to `logs/turns_demo.jsonl`. Voice turns produce no epistemic
record. Neither does `POST /api/text-query`
(server/voice_https_orch.py:94 — calls `process_text_query`, returns
routing metadata, never writes turns_demo.jsonl). The right zone today only
sees turns run through the `text_demo.py` CLI.

Script runner: exists as CLI, dropdown is net-new but thin.
`scripts/run_demo_script.py` plays `demo_scripts/*.json` (three exist:
`routing_showcase`, `consent_flow`, `care_coordination`) turn-by-turn
against `/api/text-query` with per-turn assertions;
`scripts/demo_player.py` does the same with TTS narration. A dashboard
dropdown needs one new endpoint that spawns a script run + a `<select>`.
~0.5 day.

## 3. Horizontal epistemic timeline — rendering job over existing data

The graph already records everything the timeline needs, written by
`memory_engine/store.py::encode()`:
- `superseded_by` + `valid_to` + `closed_reason` set on the prior node by
  `_tx_supersede` (store.py:226-250) — lineage chain is walkable
- `confidence_log` — list of `{ts, from, to, source}` transition entries
  (store.py:126; reconcile-harden entries added by demo_seed)
- `valid_from`/`valid_to` bitemporal window, `write_state`, `derived_from`
- `trust()` (truth_layer/queries.py) classifies any node's level on demand

Per-fact history (CORROBORATED metformin → superseded → ASSERTED Jardiance)
is reconstructable by walking the supersede chain per
`(attribute, owner, subject)` — a new read-only endpoint
(~`/api/fact_history`) plus the horizontal renderer. **No schema change, no
new capture.** Because it reads the graph, it works for voice-originated
mutations too — sidestepping half of the §2 gap for this zone specifically.

Caveat: `confidence_log` gets its interesting entries (reconcile hardens)
only from `demo_seed.py` post-write enrichment. The live path writes just
the initial `source: "write"` entry plus supersede chains. The timeline
will show supersede transitions richly and confidence transitions only
where seeded. Do not promise "confidence changed" beats from live
utterances; the live path does not generate them yet.

## 4. Top band conversation view — data exists, UI is net-new

Verbatim transcripts are written per session by
`harness/transcript_log.py::write_transcript_turn` (line 79; JSONL + txt;
both voice and text paths call it). Nothing serves them over HTTP —
`demo_dashboard.py` has no transcript endpoint, and `epistemic.html` shows
query/reply per turn card only for text-path turns via `/api/turns`.
Needed: one transcript-tail endpoint + a two-column band. ~0.5-1 day.

## 5. Component verdict table

| component | verdict | where | honest estimate |
|---|---|---|---|
| Left pipeline table | EXISTS | demo_dashboard.py RoutingRow/TierBar (383-524) | 0.5-1d re-layout + bloom field fix |
| Encryption speaker-toggle | EXISTS | demo_dashboard.py VaultSection/FactRow (526-610) | 0.5d port into layout |
| Right epistemic timeline | PARTIAL (data ✓, endpoint ✗, renderer ✗) | store.py supersede chain + confidence_log; epistemic.html delta strip is per-turn, not per-fact | 1.5-2d |
| Top band conversation | PARTIAL (capture ✓, API ✗, UI ✗) | transcript_log.py:79 | 0.5-1d |
| Dual-input unification | PARTIAL (pipeline shared ✓, epistemic capture text-CLI-only ✗) | text_demo.py::_run_one vs voice_https_orch.py:94 | 1-2d to lift capture into the shared path |
| Script-runner dropdown | PARTIAL (CLI ✓, endpoint+UI ✗) | run_demo_script.py, demo_scripts/*.json | 0.5d |

**Total: 4-6 focused days. ~70% assembly, 30% new build** — the new build
concentrated in exactly the two things the demo's story depends on
(per-fact timeline, unified capture).

## Concept rejections (architecture fights back)

**R1 — "Encryption" as a per-utterance table column is wrong.** Encryption
state belongs to facts at rest, not utterances — an utterance has no
ciphertext. The existing VaultSection (facts × active speaker) is the
architecture's true shape. Forcing it into a table column means inventing
fake per-utterance data. Keep the vault as its own speaker-toggled panel
inside the bottom-left zone.

**R2 — "Per-utterance ROW with horizontal state changes" is subtly wrong.**
State changes attach to facts; most utterances change nothing, and one
utterance can change a fact created five utterances earlier — the UI must
mutate an earlier row. Frame the right zone as **per-fact rows** (timeline
cells appearing left-to-right as utterances hit them). Same visual, correct
data model, and the supersede chain provides it for free.

**R3 — Off-net column will be static.** `SERPAPI_KEY` is a placeholder
(`.env.dev`), so every routed turn shows ON-net. Do not script a beat
around an OFF-net flip unless the key is set.

## Single biggest risk: live voice in movement 2

Three compounding facts:

1. **TD-103** (docs/debt/LATEST_DEBT.md): voice server start is
   non-deterministic (launchd I/O error 5, password injection unreliable).
2. Voice turns currently produce **zero** epistemic records, so the demo's
   centerpiece — "my update round where deltas begin" — does not reach the
   right zone at all until capture unification is built and proven.
3. **Port collision discovered this session**: the demo dashboard now
   binds port 7863, which `.env.dev` documents as the dev voice server's
   port. Starting the voice server for the dual-input demo collides with
   the dashboard. Direct consequence of the 2026-07-05 "pin 7863" fix;
   must be re-decided (dashboard to its own port, or voice to 7860-dev)
   before any dual-input work starts. Logged as a blocking prerequisite.

**Fallback preserving ~90% of the story**: run movement 2 as typed input
through the same `/api/text-query` path, and use live voice only for
movement 1's establish beats.
