# DEMO_STATE_MAP — Five-Capability Inventory
Status: BUILT
Reconciled-Against: main 10a8271 (post D-1 commit 7, byte-compat proven) — 2026-07-14

Read-only investigation of the real state of the five demo capabilities, conducted
by parallel code inspection (no estimates from memory). D-1 is complete: the
epistemic record (admitted/withheld + deny reasons GAP-1, guard_kind GAP-2,
delta/park GAP-4) is emitted at all 9 return paths of process_text_query and
byte-compat against the retired shadow is proven.

---

## The five-row state map

| # | Capability | State | Gap to demo-ready | Effort |
|---|---|---|---|---|
| 1 | EPISTEMOLOGY screen | **PARTIAL (~70%)** | epistemic.html exists + styled + polls live D-1 data; schema drift breaks fact-claim lines, delta values, guard label; park not rendered | **~1 day** |
| 2 | ROUTING screen | **BUILT (functional)** | Live pane renders complexity→tier→model per turn; per-tier scores computed but never logged/shown | 0 now; **~0.5 day** for score meter |
| 3 | ENCRYPTION screen | **BUILT (live data)** | Real ciphertext, real HKDF per-member decrypt, working reveal animation; tab-switch is manual; cipher label cosmetically wrong | 0 presenter-driven; **~1–2 days** hands-free |
| 4 | GPT LIVE wired | **PARTIAL (pipe works, integration absent)** | Standalone mic→governed→speaker script wired + debugged against live API; NOT in dashboard, no per-turn re-assembly, panes stay dark during voice | **~1–2 sessions** (wiring, not build) |
| 5 | TWO SCRIPTED JOURNEYS | **(a) BUILT / (b) PARTIAL** | (a) care dyad: L2-gated, hash-current, live-drivable NOW. (b) power-user: context-slice pane live; park/confirm scripts are v3 drafts the runner rejects, unvalidated | (a) 0; (b) **~1 day** |

---

## 1. EPISTEMOLOGY screen — PARTIAL (~70%)

**Exists:**
- `server/static/epistemic.html` (26KB, vanilla JS, "HIP Epistemic Console") served at `/epistemic` — polls `/api/turns?n=50` every 4s. Renders per turn: ADMITTED vs HELD IN MEMORY columns, per-fact trust badges + trust ramp (CONFIRMED/CORROBORATED/ASSERTED/UNCONFIRMED/DERIVED counts), withheld deny reasons via `DENY_PLAIN` map (labels exactly match injection_contract.py emit labels), delta strip, guard banner.
- `/api/turns` (demo_dashboard.py:420) serves the full D-1 record verbatim, now with `since=` (commit 6).
- `/api/fact_history` (demo_dashboard.py:482) serves supersede chains → demo.html TimelineZone (separate view).
- The route docstring calls epistemic.html a "placeholder page" — it is not; it's a near-complete view with schema drift.

**Gap (schema drift vs current D-1 record):**
- `f.claim` expected — record emits attribute/owner/subject, no claim (TD-030) → fact lines render EMPTY (most visible bug)
- delta `from_value/to_value/cause_utterance` expected — stripped per TD-030 → show "—"
- guard banner hardcoded "EMPTY-SET GUARD" — record carries `guard.kind` (access_control | empty_set) → INJ-7 mislabeled
- `park` block not rendered at all; `denied_counts` not rendered
- `/epistemic` reachable only by direct URL — no nav link from demo.html

**Effort: ~1 day (6–9h)** — fix renderFact claim assembly, state-only delta, guard.kind read, park render, nav link, live verify.

## 2. ROUTING screen — BUILT (functional), score-meter missing

**Exists:**
- Live "INFERENCE ROUTING" pane in the dashboard (RoutingRow/RoutingSection, demo_dashboard.py:940/978), 44% width, 2s auto-refresh. Columns QUERY · CLASS · BLOOM · TIER · TIER TARGET · NET. TierBar renders the tier cascade as lit boxes — this IS a complexity→tier visual.
- Two writers to logs/router.jsonl: `_write_routing_log` (voice_orch.py:204) for local turns, `LoggingEscalationStub` (router.py:637) for escalations. `/api/routing` (demo_dashboard.py:202) with `since=`.

**Gap:**
- `classify_complexity_scored()` (router.py:567) computes per-tier similarity scores but NEITHER writer emits them — no numeric score→threshold→tier meter. `/api/routing` and `/api/metrics` docstrings reference `tier_scores`/`exemplar_matches` that nothing produces (stale contract; /api/metrics confidence-gap metric is dead).

**Effort: 0 to demo as-is; ~0.5 day** to plumb scores through RouteDecision → both writers → one UI column.

## 3. ENCRYPTION screen — BUILT, live data

**Exists (all real, not narrative):**
- Envelope encryption (harness/encryption.py): per-fact random DEK → Fernet; DEK wrapped with HKDF-SHA256 owner key. Every encode() stores ciphertext + encrypted_dek (store.py:418); Neo4j Browser genuinely shows opaque ciphertext — the "sealed even from Neo4j" claim is true and load-bearing.
- Two working vault panes (inline dev console `/` + static/demo.html `/demo`): OPERATOR tab shows ciphertext; member tab click plays MASTER→HKDF(member)→KEY→UNLOCK animation then live `/api/decrypt` per fact, per-member isolation real (HKDF).
- demo_seed.py seeds through the normal encode() path — live encrypted rows.

**Gap:**
- Reveal trigger is a MANUAL tab click; nothing consumes the script's `focus: vault:<member>` cues (presenter clicks on cue).
- UI hardcodes "AES-256-GCM"; actual cipher is Fernet (AES-128-CBC + HMAC-SHA256) — technical audience will catch it (trivial fix).
- `/api/decrypt` unauthenticated (TD-101b) — isolation enforced client-side only; soft spot if the pitch is "sealed even from us" and someone opens devtools (+~1 day to gate).

**Effort: presenter-driven ready NOW (~0.5 day polish); hands-free ~1–2 days; server-enforced isolation +1 day.**

## 4. GPT LIVE — PARTIAL: pipe wired and working, dashboard integration absent

**Corrects the suspicion — this is NOT a from-scratch build:**
- `scripts/realtime_voice_demo.py` (538 lines): full mic push-to-talk → PCM16 → live `wss://api.openai.com/v1/realtime` (gpt-realtime-2.1-mini) → governed instructions from `assemble_governed_context()` at session.update → response audio → speaker. Git history shows fixes made against real API errors (event-name, voice-param commits) — this has RUN.
- `scripts/realtime_care_coord_smoke.py`: live text-mode smoke asserting Jardiance recall + cross-member refusal.
- `harness/realtime_adapter.py`: per-turn write-detection hook (SIO shadow classify + detect_and_apply_async) — used by the demo for fact writes. Its own WebSocketTransport is built but unused (adapter is offline-only by policy; scripts drive the socket inline).
- Production voice server is 100% local (Pipecat + faster-whisper + kokoro + qwen2.5) — zero OpenAI deps in requirements.

**Gap (per DEMO_SPEC v20260712T0800, Status: SPEC ONLY):**
1. Dashboard integration — voice path writes NO turn_metadata / transcript / epistemic record → all demo panes stay DARK during a voice session. This is the real long pole for the demo surface.
2. Per-turn governed re-assembly — disclosure context frozen at connect(); mid-session writes don't affect later disclosures (correctness fix regardless of demo).
3. Voice cross-member isolation asserted by source conformance only, not runtime tests.

**Effort: ~1–2 focused sessions — wiring (per-turn metadata/transcript/record emission + context re-assembly), not a build. Auth/session/audio transport already solved.**

## 5. TWO SCRIPTED JOURNEYS

**(a) Care dyad — BUILT, demo-ready NOW:**
- care_coordination.json (4 turns: capture → recall → household context → cross-member fact lock) is L2-gated (expected pair, sha256 hash current), version "1" accepted by demo_run.py, drivable live via `/api/demo/load` + `/api/demo/fire` operator pacing. The most demo-ready script in the repo.
- Polish only: no voices/movement/focus metadata (~1–2h if wanted).

**(b) Power-user (supersession + park/confirm + context slice) — PARTIAL:**
- Context-window slice EXISTS and is live: epistemic.html ADMITTED column is exactly "what reached the model," fed by the D-1 record's admitted[] (= inj.allowed verbatim).
- park_and_confirm__v20260712_1023.json is the right journey (baseline → P8 park → limbo retrieval → P10 confirm/promote) and trust_rungs covers all five rungs — but both are `"draft": true`, have NO _expected.json (not L2-gated), and declare version "3" which demo_run.py:90 REJECTS (accepts only "1"/"2") — cannot be auto-driven today.
- Their richest visuals (park delta strip) flag `d1_required_for` — the D-1 DATA now exists (GAP-4 park/delta in the record); the RENDER is the epistemology-screen gap above.

**Effort: (a) 0. (b) ~1 day: version-guard bump (~1h) + record/hand-fill expected pair (~2–4h) + park render (covered by row 1's day).**

---

## Critical path and long pole

**Demo-ready NOW (zero build):** encryption reveal (presenter-driven), routing pane, care-dyad journey, context-slice pane (admitted column — with the claim-line render bug).

**The critical path** is not one long pole but two short ones in sequence:
1. **Epistemology screen schema-drift fix (~1 day)** — gates the most differentiated content (withheld reasons, trust rungs, guards, park) and simultaneously unlocks journey (b)'s money shots, since GAP-4 park/delta data already flows.
2. **GPT Live dashboard wiring (~1–2 sessions)** — the suspected long pole is half-confirmed: the PIPE works (biggest risk already retired), but until the voice path emits turn metadata + epistemic records, every pane is dark during live voice. This is the only item that makes the demo's centerpiece (live governed voice + live panes) possible.

Everything else (routing scores, hands-free reveal, journey-b validation) is ~0.5–1 day polish that can proceed in parallel or be cut without losing the demo.

**Total distance to full five-capability demo: roughly 4–6 focused days**, with the epistemology fix first (highest leverage per hour) and GPT Live wiring second (the only true blocker for live voice).
