# FABLE_D78_web-replay-recon — remote voice demo, feasibility across four trees

Reviewer: Fable
Dispatch: D-78
Subject: feasibility recon for a gated web player serving the demo's voice to a remote
viewer — Mode 1 REPLAY (captured traces stepped through) and Mode 2 PRESENTER-DRIVEN LIVE.
Assessed against what exists: trace capture, pane-state reconstructibility, player reuse,
mode-2 plumbing and its security exposure, and audio specifics.
Method: read-only ACROSS FOUR TREES — `hip-roadmap` (worktree, `roadmap`, d7322d7),
`hip-dev` (main, `demo-presenter-package`, 3d4f46f), `hip-vo` (worktree, `voice-port`,
d7cf895 — the live voice path), `hip-harness` (separate repo, `voice-latency`, f8fadbd).
Findings are attributed per tree in the body.
Version: v20260801_0732 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED
Verification: UNVERIFIED as a whole; individual code claims cite file:line and were read
in place.
Date: 2026-08-01 (banked); recon produced 2026-08-01

**This is a named source of `REQ_DEMO_WEB_REPLAY`**, banked under D-80 because it had been
left in `/tmp`. The REQ's own header states its sources are "both banked in
docs/reviews/" — that was not true when the REQ was drafted; this filing makes it true for
this half. See the D-80 commit for the other half, which is NOT banked.

Two findings in this recon corrected premises the dispatch carried, and both are load-
bearing for the REQ: the mini binds `0.0.0.0`, **not** the tailnet IP (`restart-dashboard.sh:16`
explains why), and `POST /api/demo/next` takes no `Request` parameter so it **cannot**
check the session cookie — it is unauthenticated, which TD-101 (SEC, OPEN) already names
as a class.

---

# D-78 — Web replay demo: feasibility recon

Read-only across four trees. No lock, no design change, no status proposed, nothing banked.

## Tree map (findings are attributed to these)

| Tree | Repo | Branch | HEAD | Role |
|---|---|---|---|---|
| `~/hip-roadmap` | worktree of hip-dev | `roadmap` | `d7322d7` | REQ/governance track |
| `~/hip-dev` | main repo | `demo-presenter-package` | `3d4f46f` | demo lane |
| `~/hip-vo` | worktree of hip-dev | `voice-port` | `d7cf895` | **the live voice path** |
| `~/hip-harness` | **separate repo** | `voice-latency` | `f8fadbd` | models + registry.db |

Most findings below are **hip-vo**, which carries the voice path. `hip-harness` holds the Kokoro model files (hip-vo symlinks to them) and `registry.db`.

---

## (a) TRACE CAPTURE — audio is discarded; everything else already persists

**What a voice turn persists today.** The d1.1 epistemic record (`RECORD_VERSION = "d1.1"`, `hip-roadmap/harness/epistemic_record.py:61`) is written per turn to `logs/turns_demo.jsonl` and dual-written to the hash-chained ledger. It carries transcript, `admitted[]`/`withheld[]` fact entries with metadata, routing block (`tier`, `sensitivity_tag`, `tier_target`), guard/deny reasons, delta, and outcome. Routing detail also lands in `logs/router.jsonl`.

**TTS audio does NOT survive. Verified.** `hip-vo/harness/speech.py:90-117` — `KokoroTTS.synthesize()` returns a mono **float32 numpy array @ 24 kHz** and `synthesize_sentences()` yields one chunk per sentence so playback can start early. There is **no disk write anywhere in the voice path** — I grepped `voice_orch.py` and `speech.py` for `wav`, `sf.write`, `open(...,'wb')` and found nothing. Audio is generated, streamed over the WebRTC peer connection (Pipecat SmallWebRTC, `hip-vo/server/voice.py:31-33`), and discarded.

**What "keep per-turn audio keyed to the turn record" would touch.** Small and well-bounded:

1. a capture hook at the `synthesize_sentences()` call site in `voice_orch.py` — concatenate the per-sentence chunks, encode once per turn;
2. an encoder — float32 @ 24 kHz → WAV is stdlib; Opus/MP3 needs a dependency;
3. a write to a new `logs/turn_audio/<turn_id>.{wav,opus}`;
4. a reference field on the record.

**Does the D-1 record contract constrain adding an audio reference?** Not fatally, but it is governed and this is the part to get right. The record is a **pure projection** — `build_epistemic_record` is documented "no engine calls, no I/O" (`:213`) — so the record must carry a *reference* (a path or content hash), never audio bytes, or the projection property breaks. Two further constraints:

- **TD-030** bars fact *values* from logs. Audio of a spoken reply is value-bearing by definition, so the artifact lives outside the record and outside the ledger, referenced only by opaque id.
- The record is **dual-written to the append-only ledger**, so a reference is permanent while the audio file is separately deletable — which is *good* (it matches the chain-retained/payload-erasable shape) but means a deleted audio file leaves a dangling reference the replay must tolerate.

**Verdict: additive, low-risk, and the smallest of the three items.** Nothing about capture requires changing what the record *means*.

---

## (b) PANE STATE — reconstructible except the Vault pane, which reads the live graph

**Reconstructible from persisted logs alone:**

- **transcript / dialogue** — `/api/turns` reads `logs/turns_demo.jsonl` directly (`hip-vo/server/demo_dashboard.py:778-790`);
- **routing** — `/api/routing` reads `logs/router.jsonl` (`:560`);
- **admitted vs withheld / deny reasons / trust badges** — all in the record's own `admitted[]`/`withheld[]` entries;
- **metrics** — `/api/metrics` from `router.jsonl` + `routing_telemetry.jsonl` (`:613`);
- per-session detail in `logs/turn_metadata/` (7 files present).

**NOT reconstructible — the gap.** `/api/facts` (`:467`) reads **live Neo4j `:Fact` nodes**, not a log. It is the Vault pane's source, and its docstring is explicit that the household-wide "OPERATOR VIEW" is deliberate, load-bearing demo functionality. The graph *mutates as the demo runs* — facts written, superseded, retracted — and **nothing snapshots graph state per turn.** So the Vault pane at turn N cannot be rebuilt from logs.

**What's missing, precisely:** a per-turn snapshot of the non-superseded fact set (metadata only — never ciphertext, per the endpoint's own rule). Two options: snapshot the `/api/facts` response per turn into the trace (simple, ~KBs/turn), or reconstruct by replaying `delta` forward from a seed state (fragile — deltas are a value-stripped projection and `retract` is not represented in them).

**Recommendation: snapshot, don't reconstruct.** The delta projection was already shown insufficient once — D-41 found `classify_outcome` couldn't detect corrections because the delta lacked the keys it needed. Rebuilding vault state from the same projection would repeat that mistake.

**Other in-process state, checked and mostly benign:** `_vault_selected_member` (UI selection), `_demo_task` / `_demo_next_lock` (script execution), `_SELF_CHECK_RESULT` (preflight). None is needed for replay — a replay drives its own selection.

---

## (c) THE PLAYER — closer to "new frontend on existing logs", with one caveat

`hip-vo/scripts/demo_player.py` is **212 lines** and is an *executor*, not a player: `_TTSEngine`, `_speak(engine, text, play_fn)`, `run_demo(...)`. It speaks text through TTS on the host and fires real turns. **Almost none of it is reusable for replay** — replay reads a trace and emits, it never synthesizes or executes.

What *is* reusable is much larger: the dashboard's **entire rendering layer**. The panes already render from `/api/turns` + `/api/routing` JSON. A replay driver that serves the *same JSON shapes* from a trace file instead of from live logs would drive the existing UI essentially unchanged. The `_HTML` blob at `demo_dashboard.py:1397` is the pane renderer.

**Verdict: "new frontend on existing logs," with a caveat.** The honest framing is *new read-only backend behind the existing frontend*. Two real pieces of work: (i) a trace format and a server that replays it turn-by-turn, (ii) the Vault-pane snapshot from (b). The step-through control itself is trivial — it's an index into an array, not the `_demo_next_lock` machinery.

---

## (d) MODE 2 PLUMBING — and the security exposure, stated precisely

**The dispatch's premise is outdated in one important respect.** It says the mini binds `--host [REDACTED-TAILNET-ADDRESS]`. It does not. `hip-vo/scripts/restart-dashboard.sh:16-18` binds **`--host 0.0.0.0`**, with the reason in a comment: *"0.0.0.0, not the tailnet IP: binding [REDACTED-TAILNET-ADDRESS] refused loopback clients."* `restart.sh:32,43` does the same for the orchestrator (7860) and dashboard (7870). **The dashboard already listens on every interface, not just the tailnet.**

**The precedent is Edge Middleware auth, not JWT.** `hip-vo/docs/backlog/BACKLOG__v20260714_1615.md:12,94` — the NDA data room at `hip.olindasolutions.com/secure/` is "Edge Middleware auth, per-user credentials, access logging, publish pipeline," deployed from a **separate repo (`hip-deploy`, commit 6749f66)**. Important difference in kind: that data room serves **static documents**. It has never proxied to a live machine.

### The exposure, named

**1. `POST /api/demo/next` is UNAUTHENTICATED.** `demo_dashboard.py:1283-1297` — `async def api_demo_next():` takes **no `Request` parameter**, so it structurally cannot check the session cookie. Compare `/api/facts` (`:467`), which takes `request: Request` and is session-gated. This is not a subtle gap: the endpoint that *fires a turn against the live graph and the LLM* has no auth at all.

**2. It is already a known, open security item.** TD-101 (SEC, OPEN) in the roadmap register opens with *"Unauthenticated dashboard endpoints still present."* This recon confirms `/api/demo/next` is one of them.

**3. What a public proxy would open.** A proxy that reaches `/api/demo/next` sits on the same origin as every other dashboard endpoint. Unless the proxy allow-lists exactly one path and one method, it exposes: `/api/facts` (household-wide fact **metadata** for every member — by design), `/api/decrypt` (fact_id-keyed decryption), `/api/members`, `/api/metrics`, `/api/preflight`, and the graph-nuking `MATCH (f:Fact) DETACH DELETE f` path at `:1890`.

**4. What the demo graph contains.** Real-shaped household data for `bill / maya / sam` — medication, health_condition, allergy, incident, financial, relationship, address. Currently 12 `:Fact` nodes. Not synthetic-looking, and the Vault pane is explicitly cross-member by design.

**5. What happens if a request escapes the scripted path.** `fire_next_turn` advances a *loaded script*; it returns 409 if none is loaded or a turn is in flight. So the blast radius of `/api/demo/next` alone is bounded to advancing the script. **The risk is not that endpoint — it is co-residency.** Any public reachability of that origin exposes the unauthenticated siblings, and the mini already binds `0.0.0.0`.

**Consequence for Mode 2: the proxy must be a strict allow-list of one path, one method, on a separate origin, with its own auth — never a reverse proxy to the dashboard.** And TD-101 should close first.

---

## (e) AUDIO SPECIFICS

- **Engine:** `kokoro-onnx` (`hip-vo/harness/speech.py:4` — "onnxruntime; no torch, no spacy"). Models at `hip-vo/models/kokoro-v1.0.onnx` and `voices-v1.0.bin`, both **symlinks into `~/hip-harness/models/`**.
- **Output format:** mono **float32 @ 24 kHz**, in-memory numpy. Serving to browsers needs an encode step (WAV via stdlib `wave`; Opus/MP3 adds a dependency).
- **Per-turn generation time, measured:** `hip-vo/docs/INDEX.md:78` records the first-ever measured voice latency numbers (2026-07-31, M1 Pro, path A): **TTS first-byte 1.3–3.5 s**, plus 2100 ms VAD dead time, ~3.4 s per-connection Whisper/Kokoro reload, and ~7.6 s / ~10.3 s local/frontier stack-up. *For replay this is irrelevant — audio is pre-generated. For Mode 2 it is the dominant cost and a viewer will feel it.*
- **Licensing:** not resolvable from this recon. `kokoro-onnx` is not installed in the interpreter I could reach, and there is **no LICENSE file beside the model artifacts** — the `models/` dir contains only the two symlinks. Kokoro's weights are commonly Apache-2.0 and the voice packs may differ, but **I could not verify either from the repo, so this is an open item, not a green light.** Note the contrast with the Chatterbox evaluation (`hip-vo/docs/INDEX.md:212`), which explicitly checked and **CONFIRMED a PerTh watermark with no API off-switch** — evidence this project already treats TTS licensing/watermarking as a real gate. Serving generated audio to third parties is a distribution step that a purely local demo never took.

---

## ESTIMATES — dispatch-days, riskiest assumption named

| Item | Estimate | Riskiest assumption |
|---|---|---|
| **Trace capture** | **2–3** | That the audio artifact can be referenced from the record without a D-1 contract change requiring its own REQ. It is additive and TD-030-compatible as a reference, but the record is dual-written to an append-only ledger, so the reference is permanent — and the L7 record-invariant checks will need to accept the new field. **If a REQ is required, add 1–2.** |
| **Replay player** | **4–6** | The Vault-pane snapshot from (b). If snapshotting `/api/facts` per turn is acceptable, this is a read-only server plus a trace format and the existing UI barely changes. **If Bill wants vault state reconstructed from deltas instead, this doubles and probably fails** — the delta projection is value-stripped and does not represent retracts. |
| **Mode-2 proxy** | **5–8**, and gated | That TD-101 closes first. The estimate is dominated by **security work, not plumbing**: authenticating `/api/demo/next`, standing up a single-path allow-list proxy on a separate origin, and re-checking every co-resident endpoint. The plumbing alone is ~1 day; the rest is why it is gated. Second risk: 1.3–3.5 s TTS first-byte plus stack-up means a viewer waits several seconds per turn over a WAN, which may simply not demo well. |

**Cross-cutting risk worth stating once:** `REQ_VOICE_COMPONENT` (hip-vo) is **NOT MET** with three open rulings and carries the measured-latency numbers in its own known-broken section. Mode 2 builds a public surface on a path whose own requirement is unruled.

---

## RECOMMENDED CUT LINE

**v1 ships REPLAY only. Mode 2 waits.**

**In v1:** trace capture (audio + per-turn vault snapshot), a read-only replay server, the existing dashboard UI driven from traces, gated behind the *existing* Edge Middleware data-room pattern that already works for documents. Nothing in v1 touches the mini at request time, so nothing in v1 can be made to fire a turn, read the live graph, or reach an unauthenticated endpoint. **A replay is a recording — it has no live attack surface at all**, which is the entire reason to ship it first.

**Waits for Mode 2:** TD-101 closed and `/api/demo/next` authenticated; a single-path allow-list proxy on a separate origin; a ruling on whether multi-second per-turn latency is acceptable to a remote viewer; and the Kokoro licensing question answered before any generated audio is served to a third party.

**The licensing item gates v1 too, not just Mode 2** — replay serves generated audio files to third parties, which is exactly the distribution step the local-only demo never took. It is cheap to resolve and should be resolved first.

Nothing banked. No design changed. No status proposed.
