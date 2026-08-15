# HIP EXECUTION MAP — NATURAL CONVERSATION DEMO V1 (PREFLIGHT EXCAVATION)
Status: BUILT
Reconciled-Against: 2026-08-14, `~/hip-vo` @ `main` @ `d74261a`

**NC 7. READ-ONLY: no code was changed, no graph was written, no service was started.**
**Findings only — no fixes, and no re-ruling of settled principles.**

Terrain map for the ten-step vertical slice: **B0 → kernel → text+voice ingress → B1 detector
→ Episode → B2 continuation → voice write → demo+harness → review → certification.**

> **HOW TO READ THE NUMBERS.** Every count here was produced by a script over the tree at
> `d74261a`, not by reading and tallying. Where a heuristic could not decide, the entry says so
> rather than guessing — the project's own rule is to measure the claim against the artifact.

---

## 0. THE HEADLINE NUMBERS

| | count |
|---|---|
| distinct HTTP/WS routes across 4 server modules | **47** |
| **duplicate implementations** (same capability, two code paths) | **8** |
| off-device egress sites | **3 by literal host** |
| **egress bypasses** (off-device, no `permit()`) | **2** — one reachable today |
| **ungoverned ingress** (reaches a model with no gate at all) | **1** |
| import-time environment reads | **32** |
| test files on disk | **37** |
| test files naming an ingress consumer | 5 |
| **of those, test files that actually CALL one** | **0** |

---

## 1. INGRESS — ENTRY POINT TO MODEL CALL

### 1.1 TEXT INGRESS — three implementations

| # | entry point | path to model | governed? |
|---|---|---|---|
| **T1** | `server/demo_dashboard.py:2154` `POST /api/text-query` | → `principal_from_request()` `:2182` → `server/voice_orch.process_text_query` `:2186` → `_governed_turn` `voice_orch.py:2823` → model | **YES** — the governed path |
| **T2** | `server/voice_https_orch.py:109` `POST /api/text-query` | its own handler, `hip_api_text_query` `:110` | **SECOND IMPLEMENTATION of the same route** |
| **T3** | `server/app.py:31` `POST /chat` | `route()` → `requests.post(f"{OLLAMA}/api/chat")` **`app.py:36`** | **NO — see §1.3** |

### 1.2 VOICE INGRESS — three implementations

| # | entry point | path to model |
|---|---|---|
| **V1** | `server/demo_dashboard.py:2768` `WS /ws/voice` | `ws_voice()` → `assemble_governed_context()` `:2789` → OpenAI Realtime |
| **V2** | `server/voice_https_orch.py:311` `POST /api/voice-query` | `hip_api_voice_query` `:312` |
| **V3** | `server/voice_orch.py:3757` `bot(runner_args)` | the pipecat pipeline; `build_task` `:2252` with a `SpeakerVerifier` |

`harness/realtime_adapter.py:318/351` also calls `assemble_governed_context`, so the realtime
path assembles context in **two** places.

### 1.3 ⚠ `server/app.py` IS AN UNGOVERNED INGRESS, AND IT IS COMPLETE

`server/app.py` imports, in full: `json, time, pathlib, datetime, requests, yaml, FastAPI,
BaseModel`. **There is no governance import of any kind** — no permissions, no disclosure, no
egress gateway, no member session, no memory, no speaker identity, no epistemic record.

`POST /chat` takes `inp.message` and `inp.user_id` **from the caller**, routes with a local
`route()`, calls the model at `app.py:36`, logs the turn, and returns the reply. **`user_id` is
whatever the caller says it is.** This is the Phase 0 walking skeleton described in `README.md`
and it is still mounted and still routable.

**For the vertical slice this matters twice:** it is a second answer to "what is the text
ingress", and it is a live counter-example to the claim the slice is meant to demonstrate.

---

## 2. THE 8 DUPLICATE IMPLEMENTATIONS

Six are **the same method and the same path** in two modules — a request reaching one gets a
different implementation than the same request reaching the other:

| method + path | implementation A | implementation B |
|---|---|---|
| `GET /` | `demo_dashboard.py:2750` | `memory_dashboard.py:171` |
| `GET /api/facts` | `demo_dashboard.py:513` | `voice_https_orch.py:565` |
| `GET /api/members` | `demo_dashboard.py:761` | `voice_https_orch.py:659` |
| `GET /api/routing` | `demo_dashboard.py:606` | `voice_https_orch.py:89` |
| `POST /api/reset` | `demo_dashboard.py:1987` | `voice_https_orch.py:522` |
| **`POST /api/text-query`** | `demo_dashboard.py:2154` | `voice_https_orch.py:109` |

Two more are the same capability under a different spelling:

| capability | A | B |
|---|---|---|
| decrypt | `POST /api/decrypt` `demo_dashboard.py:563` | **`GET`** `/api/decrypt` `voice_https_orch.py:609` |
| demo scripts | `/api/demo/scripts` `demo_dashboard.py:1251` | `/api/demo-scripts` `voice_https_orch.py:196` |

**`POST /api/text-query` is the one that bears on the slice**: the ingress the demo drives has
two implementations, and only one was traced in §1.1.

---

## 3. EGRESS — AND WHERE IT LEAVES THE GATEWAY

`harness/egress_gateway.py` is the intended chokepoint: `permit()` `:175`, `permit_stream()`
`:235`, `Destination` `:51`, `Purpose` `:66`, `EgressRefused` `:59`, and
`_assert_destination_is_truthful()` `:116`.

### 3.1 GATED — off-device calls that do pass it

| site | destination | permit |
|---|---|---|
| `harness/frontier_client.py:133` | `https://api.openai.com/v1/responses` `:27` | `:90` |
| `harness/realtime_adapter.py` | `wss://api.openai.com/v1/realtime` `:75` | `permit_stream` `:130` |
| `server/voice_orch.py:2062` | Groq, `GROQ_BASE_URL` `:165` | `:2042` |
| `server/voice_orch.py:3630` | Groq | `:3616` |
| `harness/fact_change.py:463` | local, via `_call_local` | `:444` |
| `memory_engine/interpreter.py:202` | local | `:194` |

### 3.2 ⚠ THE TWO BYPASSES

**(E1) `harness/escalation_backends.py:400` — `requests.get("https://serpapi.com/search")`.**
`ENDPOINT` is declared at `:368`, the key is read at import time at `:362` (`SERPAPI_KEY`), and
**`escalation_backends.py` contains no reference to `egress_gateway` at all.** This is a
third-party host reached with no permit, no destination assertion, and no refusal path.

**It is wired and reachable, not dead code:**
- `server/voice_orch.py:104` imports `TieredEscalationBackend, WebFetchBackend,
  SerpAPISearchClient`;
- `server/voice_orch.py:1591` describes the live route in its own comment — *"TEMPORAL intent
  used to send 'what time is it' straight through `_decide()` → escalation → SerpAPI
  **unconditionally**"*;
- `harness/temporal.py:98` says the same for remote-time queries;
- `config.yaml:121-123` configures `web_fetch.endpoint: "https://serpapi.com/search"`.

The temporal short-circuit at `voice_orch.py:1596` removed *one* class of query from that path.
**It did not gate the path.**

**(E2) `harness/escalation_backends.py:98` — `requests.post(endpoint, ...)` in
`SearchBackend.search`.** The endpoint is supplied by config, so whether this is off-device is a
configuration question, not a code one. No permit either way. Its docstring says the committed
config points at a stub, which is why this is listed second — **the hazard is that its
destination is not knowable from the code**, which is precisely what
`_assert_destination_is_truthful` exists to prevent.

### 3.3 On-device model calls — 19 sites, none gated, and that is a scoping question not a defect

Ollama is reached from `zep_store.py:265/331`, `extraction_queue.py:322/373/400`, `sio.py:367`,
`voice_orch.py:205/1886/1962/2748/3655`, `app.py:36`, `fact_change.py`, `interpreter.py:329`.
**Whether on-box inference should require a permit is a design decision this document does not
take** — it is recorded because the slice's B2 continuation step will add more of them.

---

## 4. SESSION AND CONVERSATION STATE — WHERE IT LIVES TODAY

| store | location | lifetime |
|---|---|---|
| **disclosure pendings** | `harness/disclosure.py:47` `_PENDING: dict` + `:50` `logs/pending_disclosures.json`, TTL `:51` = 1800 s | process **and** file — survives restart |
| **member session / principal** | `harness/member_session.py`; `principal_from_request()` `:171`; `matches_claim()` `:87` | request-scoped |
| **session memory** | `harness/session_memory.py` | session |
| **transcript** | `harness/transcript_log.py:79` `write_transcript_turn(session_id, member_id, …)` | durable file |
| **dashboard operator session** | `server/demo_dashboard.py:173` `_SESSION_COOKIE`; `server/operator_auth.py:45` `_SESSION_INFO` | cookie |
| **conversation history for the prompt** | `server/voice_orch.py:518` `_trim_context(messages, max_turns=8)` | in-request |
| **per-session trace** | `voice_orch.py:442` `_session_trace_path(session_id)` | file |
| **last speaker** | `voice_orch.py:502` `_log_speaker_change`; `GET /api/last_speaker` `demo_dashboard.py:641` | process |

**There is no single conversation-state owner.** The Episode step of the slice needs one, and
**`_trim_context(max_turns=8)` is the only thing today that resembles conversation memory for
the model** — a fixed window, not an episode.

---

## 5. SPEAKER IDENTITY — SOURCES, AND WHERE EACH IS TRUSTED

| source | where | trusted for |
|---|---|---|
| **voiceprint** | `harness/speaker_id.py:305` `SpeakerVerifier`; config `routing.speaker_id` `:90-95`; voiceprint dir from `HIP_VOICEPRINT_DIR` at import `:60` | the voice path (`build_task` `voice_orch.py:2252`) |
| **operator session cookie** | `server/operator_auth.py:98` `require_operator` | dashboard endpoints |
| **request principal** | `harness/member_session.py:171` `principal_from_request` | `POST /api/text-query` (T1), `demo_dashboard.py:2182` |
| **caller-declared `member`** | payload field on T1/T2 | checked against the principal by `matches_claim` `:87`; `ClaimMismatch` imported at `demo_dashboard.py:2181` |
| **caller-declared `user_id`** | `server/app.py` `/chat` | **trusted with nothing to check it against** |
| **`self.member_id`** | `harness/realtime_adapter.py:308`; default `"demo_member"` `:647` | the realtime session |
| **`user_id` IS the member_id** | `harness/orchestrator.py:558` | standalone orchestrator runs |

**Two of these are self-asserted** (`app.py`'s `user_id`, `realtime_adapter.py`'s
`demo_member` default). **The claim-vs-principal check exists in exactly one place** —
`matches_claim`, reached from T1 — and nothing forces the other ingresses through it.

---

## 6. PROMPT ASSEMBLY · RETRIEVAL · AUTHORIZATION

### 6.1 Prompt assembly — 8 sites, 2 of them the governed one

`server/voice_orch.py:2591` **`assemble_governed_context()`** is the governed assembler, called
from `demo_dashboard.py:2789` (V1) and `realtime_adapter.py:329` and `:354` (**twice**).
Independent assemblers: `harness/zep_store.py:269/335`, `harness/extraction_queue.py:184/219/327`,
`harness/fact_change.py:99/447/515`, `harness/frontier_client.py:92`, `harness/egress_gateway.py:264`.

### 6.2 Retrieval — the fact-read surface

`harness/extraction_queue.py` is the main one: `search_facts_by_embedding` `:797`, plus Cypher
reads at `:553/578/615/630/663/673/753/827`. Also `harness/disclosure.py:169`,
`harness/zep_store.py:308/365`, `memory_engine/`.

### 6.3 Authorization — 3 real deciders, and a duplicate

| decider | site |
|---|---|
| **`authorize_disclosure()`** | `harness/disclosure_authority.py:466`; called at `server/voice_orch.py:3069` |
| **`permissions.can_retrieve`** | referenced from `disclosure.py:266` and `disclosure_authority.py:83` |
| **`require_operator`** | `server/operator_auth.py:98` |
| cross-member deny | `harness/injection_contract.py:317` `_inj3_cross_member_deny` |
| **duplicate** | `voice_orch.py:2960` builds `_approve_authz` separately from the `_authz` produced at `:3069` — **two authorization objects in one function** |

### 6.4 Memory writes — 7 sites

`harness/extraction_queue.py:591` (`CREATE (n:Fact …)`) and `:688` `write_facts`;
`harness/disclosure.py:484` `write_frontier_fact`; `memory_engine/store.py:210`;
`memory_engine/consolidate.py:511`; `harness/transcript_log.py:79`;
`harness/member_registry.py:327` `create_household`.

**Three independent modules create `:Fact` nodes.** The B1 detector and B2 continuation steps
will need to know which one is canonical.

---

## 7. CONFIG AND ENV — 32 IMPORT-TIME READS

Read at **module import**, so they bind before any dispatch can set them, and a missing one
fails at import rather than at use:

`HIP_VOICEPRINT_DIR` `speaker_id.py:60` · `HIP_HEL_DIR`/`HIP_HEL_SEAL_BYTES`
`epistemic_ledger.py:98/107` · `NEO4J_USER|PASSWORD` `zep_store.py:92/93`,
`extraction_queue.py:101/430`, `voice_https_orch.py:566`, `demo_dashboard.py:125/132` ·
`HIP_MASTER_KEY` + `NEO4J_*` `encryption.py:52/90` · **`SERPAPI_KEY` `escalation_backends.py:362`**
· `OPENAI_API_KEY` `frontier_client.py:53`, `realtime_adapter.py:104`, `demo_dashboard.py:2769` ·
`HIP_FRONTIER_CODEWORD` `control_flow.py:41` · `HIP_LOCAL_CHAT_URL`/`HIP_FACT_CHANGE_MODEL`
`fact_change.py:429/431` · `GROQ_API_KEY` `fact_change.py:504`, `voice_orch.py:1042`,
`interpreter.py:153` · `HIP_REGISTRY_DB` `member_registry.py:93` · `HIP_SIO_OLLAMA_URL`
`sio.py:40` · `HIP_DASHBOARD_TOKEN` `operator_auth.py:48` · `HIP_MEMORY_MODEL`
`interpreter.py:153` · `NEO4J_URI` `memory_dashboard.py:30`.

**`NEO4J_PASSWORD` is read at import in six modules.** The `~/hip-nc` incident is the
precedent: a checkout with no `.env.dev` failed closed at that guard, which is what stopped an
inherited pin from becoming an inherited write.

---

## 8. ⚠ TESTS THAT CLAIM COVERAGE vs TESTS THAT EXECUTE THE PATH

**Five test files name an ingress consumer. ZERO of them call one.**

`eval/test_phase0_trust_boundary.py`, `eval/test_member_session_principal.py`,
`eval/oracle/test_disclosure.py`, `eval/test_graph_resolver_consumers.py`,
`eval/test_a1_governed_voice.py` reference `process_text_query` / `process_governed_turn` /
`_governed_turn` / `assemble_governed_context` — by import, by monkeypatch, or inside a string
being asserted over. A search for an actual invocation (`await X(` or `= X(`) returns **nothing**.

**22 of 37 test files assert over source text** (`read_text()`, `ast.parse`,
`inspect.getsource`). Structural assertions are legitimate — several of this project's best
proofs are structural — but **a structural test cannot fail when the runtime behaviour changes
while the source shape holds.**

Skips/xfails are concentrated in `test_graph_resolver_consumers.py` (6), `tests/test_routing.py`
(5), `tests/test_memory.py` (5), `tests/test_permissions.py` (4).

**For the certification step of the slice this is the single most important row in this
document:** the consumer path the demo will drive has **no executing test today.**

---

## 9. THE B0 GAP LIST — GROUND HARDENING, CONCRETELY

**B0-1 — "permissive intent fallback". `harness/intent_classifier.py:190-212`.**
`classify()` returns `("knowledge", 0.0)` at **`:197`** when the embedding is unavailable, and
`("knowledge", best_score)` at **`:211`** when every route scores below
`CONFIDENCE_THRESHOLD`. **`knowledge` is the default in both directions** — the initial
`best_route = "knowledge"` at `:201` means an empty `_route_vecs` (i.e. `initialize()` never
called) also yields `knowledge`. **Three distinct failure modes converge on one permissive
answer, and the caller cannot distinguish them from a confident classification** — the returned
confidence is the only signal, and `0.0` and "below threshold" are different situations.

**B0-2 — a second identity default.** `harness/realtime_adapter.py:647` `member_id =
"demo_member"`. Unlike `_build_requester`, this one is not fail-closed.

**B0-3 — role fallbacks bypass the DB.** `harness/permissions.py:57-71` `_ROLE_DEFAULTS` is used
"when the DB is unavailable or role_id not found". Unknown roles get guest, which is correct;
**the hazard is that a DB outage silently switches the authority for every role.**

**B0-4 — the ungoverned ingress.** §1.3, `server/app.py`.

**B0-5 — the ungated web egress.** §3.2, `harness/escalation_backends.py:400`.

**B0-6 — two authorization objects in one function.** §6.3, `voice_orch.py:2960` vs `:3069`.

**ALREADY HARDENED — do not re-open (recorded so the slice does not redo it):**
`_build_requester` `voice_orch.py:680-706` **fails closed**: a registry miss is a **guest**, not
an adult. Its docstring records that it used to fall back to adult/full and that HA-50 Phase 0
changed it — *"the fallback is the exact case where identity is least established, so it must
be the least privileged, not the most."*

---

## 10. TOP 5 HAZARDS FOR THE BUILD

1. **The consumer path has no executing test (§8).** Five files claim it; none calls it. Every
   later step's "it still works" rests on structural assertions and live smoke.
2. **`POST /api/text-query` has two implementations (§2).** The slice will harden one. Which one
   the demo actually reaches is a deployment fact, not a code fact.
3. **`server/app.py` is a complete ungoverned ingress (§1.3)** — self-asserted `user_id`, direct
   model call, zero governance imports. It is a live counter-example to the claim the slice
   exists to demonstrate.
4. **SerpAPI egress bypasses the gateway and is reachable (§3.2, E1).** Off-device, no permit,
   no destination assertion; `voice_orch.py:1591` and `temporal.py:98` both describe it as
   reached *unconditionally* from escalation.
5. **No conversation-state owner (§4).** Eight stores, three lifetimes, and `_trim_context`'s
   fixed 8-turn window is the closest thing to episodic memory. The Episode step has no seam to
   attach to yet.

---

## 11. WHAT THIS EXCAVATION DID NOT DO

- **Changed no code, wrote to no graph, started no service.** Read-only throughout.
- **Ruled nothing.** Every "hazard" is a finding for the build dispatch to scope.
- **Did not re-open settled principles** — §9 explicitly records `_build_requester`'s
  fail-closed behaviour as settled, so the slice does not relitigate it.
- **Did not resolve which server is deployed.** Which of the duplicate implementations answers
  a live request is a runtime question this document deliberately leaves open.
- **Did not classify on-box inference as a bypass** (§3.3) — that is a design decision, not a
  measurement.
