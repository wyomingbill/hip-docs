# FABLE_D84_monolith-vs-services — architecture recon across four trees

Reviewer: Fable
Dispatch: D-84
Subject: whether the governance core should stay MONOLITHIC inside a hard boundary with
voice and demo as contracted clients outside it — assessed against the actual codebase
rather than in principle: the real gate chain and its interdependencies, every import
path that reaches a graph write, the three known boundary violations, misplaced logic in
both directions, the ledger's structural separation (or absence of it), where the
inference boundary actually sits, both columns of the split/don't-split argument, and the
cost to make the write boundary structural such that A10 flips.
Method: read-only across FOUR trees plus the live process table and launchd. Findings are
attributed per tree throughout: hip-roadmap `roadmap` @ 4ae70cc, hip-vo `voice-port` @
d7cf895, hip-harness `voice-latency` @ f8fadbd, hip-dev `demo-presenter-package` @
3d4f46f, and `[live]` for the running processes.
Version: v20260801_0919 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED
Verification: UNVERIFIED — findings are the reviewer's, reproduced from the cited
file:line and process evidence, and NOT independently confirmed by a separate dispatch.
Proposes NO status and NO REQ.
Date: 2026-08-01

**This is the evidence for `REQ_ARCHITECTURE_BOUNDARY`**, banked under D-85 because it
had been left in `/tmp`, outside the repo's provenance record and one reboot from being
gone. Same gap D-60 closed for research pass 3, D-77 for the D-70 survey, and D-80 for
the D-78 recon.

Headline as filed: **the ruling's boundary exists in no running process.** Three
independent `:Fact`-CREATE implementations; roughly fourteen modules reach a graph write,
at least nine of them outside any defensible boundary, all by `import`; the plist
credential fallback lets any process self-serve the graph password; and the live voice
orch runs governance code from the FROZEN hip-harness checkout, which is the ruled
voice-to-core contract exactly inverted.

Two premise corrections the report makes and that should not be lost: **A10's strict-xfail
was never written** (D-77 classified it; no `eval/test_ceiling_inference.py` exists), and
**model calls already cross a process boundary everywhere** — the real inference exposure
is the two model-output-to-write paths and the voice process holding memory-unsafe
parsers in the same heap as the write authority.

---

# D-84 — architecture recon: monolith vs services

Read-only recon. Gate passed (bill-ai / [REDACTED-MACHINE-NAME] / hip-roadmap / roadmap @
`4ae70cc`, clean). No lock, no design change, no status proposed. Tree attribution per
finding: **[roadmap]** = ~/hip-roadmap @ 4ae70cc, **[vo]** = ~/hip-vo voice-port @ d7cf895,
**[harness]** = ~/hip-harness voice-latency @ f8fadbd, **[dev]** = ~/hip-dev
demo-presenter-package @ 3d4f46f, **[live]** = the running processes on this machine, now.

**Headline: the ruling's boundary exists in no running process.** The process that today
holds the memory-unsafe inference runtimes ALSO holds the graph credential, the extraction
write path, the ledger append, and `assemble_governed_context`. The monolith-vs-services
question is downstream of a simpler fact: there are three independent Fact-CREATE
implementations, ~20 write-reaching import paths, and zero of the ruled "one process owns
writes" is built. Detail below.

---

## 2a. The gate chain — real interdependencies

### The map [roadmap]

**READ side** (per turn):
`orchestrator.decide()` → retrieval (`read_user_facts` / `search_facts_by_embedding`,
owner-scoped) → `apply_injection_contract` (INJ-1..7) → disclosure gate →
`strip_context_for_tier` → context assembly → guards (PERSONAL_FACT_GROUNDING_GUARD,
answer-mode selection) → generation.

**WRITE side** (session end / live change):
transcript → `extract_facts` (Ollama qwen32b) → normalization →
`write_facts` → `_write_one` (per fact: `classify_write` → seal-by-class → trust
`classify_trust_props` → P8 monotonicity → CREATE) — or, on the live path,
`fact_change` → `store.encode()` (WriteDecision → write_rule five-rule order → P8 →
`_CREATE_FACT_CQL` → audit append) — or `consolidate._write_derived_node` (its own
classify + its own CREATE). Retractions: `retract_fact` → R18 cascade (D-81, in-transaction).

### Which gates share state

| Gate | State | Shared with |
|---|---|---|
| INJ-1..7 | **NONE — pure function** over (facts, requester, query, subjects, intent) | — |
| `can_retrieve` (permissions) | none — pure | — |
| trust classifier (`memory_engine/trust.py`) | none — pure | — |
| write_rule / sensitivity registry | none — pure | — |
| confirmation gate | parked facts (`write_state`) **in the graph** | the write path — `apply_confirm/apply_decline` SET the same nodes `encode()` wrote |
| disclosure gate | pending-disclosure state per session | frontier path |
| extraction | sqlite queue + Ollama | write path |
| consolidation | reads graph, writes graph | trust classifier, lineage (R18) |
| R18 cascade | **the caller's transaction** (D-81, deliberately) | retract path |

### Ordered — enforced how?

Three different answers, and this is the honest core of 2a:

1. **Inside `apply_injection_contract`: structural.** One function body, fixed order
   (INJ-4 → INJ-5 → INJ-3 → INJ-1 → INJ-2 → 6b/7 at `injection_contract.py:632-691`).
   Cannot be reordered by a caller. Mutation-tested every harness run.
2. **Across the read chain: by call sequence.** `assemble_governed_context` and
   `process_text_query` [both living in `server/voice_orch.py` — see 2d] are the only
   places the sequence retrieval→INJ→disclosure→strip→guards exists. Any new caller
   re-composes it by hand. Concrete proof it's convention: **INJ-7 is disabled by
   default** — `member_ids=None` (the default) turns it off entirely
   (`injection_contract.py:539` docstring). A caller that forgets one kwarg silently
   drops a gate. `memory_dashboard.py` and `recall.py` each compose their own variant.
3. **Across the write chain: copied, not shared.** The classify→seal→trust→P8→CREATE
   sequence exists **three times**: `store.encode()`, `extraction_queue._write_one`,
   `consolidate._write_derived_node`. Each is internally ordered; nothing makes them
   agree. `_write_one:27-38` carries comments explicitly noting where it must mirror
   `store.encode()`'s behavior ("D8 fixture regression", "store.encode() override 4") —
   the mirroring is maintained by comment discipline.

**Which could stand alone:** INJ contract, permissions, trust, write_rule, sensitivity —
all pure, all extractable at zero semantic cost. **Which cannot:** confirmation gate and
the R18 cascade are transactional with the write path (splitting the cascade out would
reintroduce the exact committed-retraction-without-cascade defect D-81 closed);
extraction and consolidation carry queue/LLM state.

---

## 2b. The library problem — every import path that reaches a write

A10 (R10): "an alternate direct call to `store.py::encode` cannot bypass origin,
registry, representation, or permit checks." Verified at HEAD: `encode()` runs
write_rule classification, P8, and seal-by-class — but **none of R10's four named
checks** (origin path, attribute registry, representation class, permit). And — same
correction as A18 — **the A10 xfail was never written**: no `eval/test_ceiling_inference.py`
exists, `grep A10 eval/ scripts/` is empty. D-77 classified it; nobody wired it.

### Writers and their callers [roadmap], caller counts by module

**Path 1 — `store.encode()`** (the would-be official path):
| Caller | Inside/outside would-be boundary |
|---|---|
| `harness/fact_change.py:797` (live change path) | inside |
| `harness/disclosure.py:258` (`write_frontier_fact` — **model output → fact**) | inside |
| `scripts/demo_seed.py:380` | OUTSIDE (ops script) |
| `eval/memory_e2e.py`, `eval/memory_harness.py` (5 sites) | OUTSIDE (harness) |
| `docs/dispatches/*.py` (2 archived scripts) | OUTSIDE |

**Path 2 — `extraction_queue.write_facts` → `_write_one`** (its own CREATE at `:81`):
| Caller | |
|---|---|
| `extraction_queue.py:1005` (session-end worker — **model output → facts**) | inside |
| `scripts/realtime_voice_demo.py:110` | OUTSIDE |
| `scripts/realtime_care_coord_smoke.py:81` | OUTSIDE |
| `eval/care_coord_run.py:164-165` | OUTSIDE |
| `retract_fact`: `fact_change.py:720` + voice-orch manual retract [vo] | mixed |

**Path 3 — `consolidate._write_derived_node`** (its own CREATE at `:54`):
called only via `run_consolidation` — whose only live callers are **eval** modules
(`memory_e2e.py`, `memory_harness.py`). No production trigger found — which corroborates
TD-141 (the one live derived fact has empty lineage; the writer that populates
`derived_from` has no production caller in this tree).

**Bookkeeping writers that hold the same credential:**
- `memory_engine/recall.py:161` — the **read** path SETs `access_count` on facts.
- `harness/confirmation_gate.py:227,264` — SETs `write_state` on parked facts.
- `harness/derivation_cascade.py` — via retract (in-transaction, by design).
- `scripts/migrate_*.py` — 2 migration scripts.

**Non-graph writes with governance weight:** member registry sqlite
(`add_member` — demo_seed, voice-orch enrollment), care-team sqlite (with
`CREATE TABLE IF NOT EXISTS` side effects on *read* — the D-52 finding), voiceprint
store, HEL append (see 2e).

**Count: ~14 distinct modules reach a graph write; at least 9 of them sit outside any
defensible boundary** (scripts, eval, dashboards). Every one of them works by `import`,
and every process that imports `extraction_queue` [roadmap `:65-102`] or `store` gets the
credential resolution for free — including the **plist fallback** (`extraction_queue`
`_neo4j_password`), which exists precisely so that *any* process can self-serve the
graph password. `server/memory_dashboard.py:40` imports the credential accessor
directly. The library problem is not that a hostile caller *could* import the write
function — it's that nine well-meaning callers already did.

---

## 2c. The three known violations — what breaks, what migrates

### (1) Dashboard's in-process import of `process_text_query` [vo]/[dev]/[live]

Today: `demo_dashboard.py` `/api/text-query` and `scripts/demo_run.fire_next_turn` both
`from server.voice_orch import process_text_query` and run the **entire governed turn**
— retrieval, INJ, disclosure, generation, extraction enqueue, graph writes — inside the
dashboard process. Live right now [live]: pid 57308 (cwd hip-vo, :7871) and pid 16187
(cwd hip-harness, :7870) each hold that power, plus the credential.

**If one process owns writes:** nothing about the dashboard's read panes breaks — they
already consume HTTP endpoints and log files. What breaks is `/api/text-query` and the
deck driver: `process_text_query` cannot be imported, so firing a turn must become an
RPC to the owning process. **Migration:** move `process_text_query` behind a local
endpoint on the write-owner; the dashboard's `/api/demo/next` becomes a proxy call.
`demo_run.py`'s deck state file doesn't move. This is exactly the seam D-82 already
mapped (one call site, `demo_run.py:246`). Cost folded into §4.

### (2) Shared `registry.db` [roadmap]/[vo]/[harness] — all of them

`harness/member_registry.py:46`: `DEFAULT_DB_PATH = ~/hip-harness/registry.db` — an
absolute path into the **frozen** tree, shared by every process from every checkout.
Membership is a *governance input* (INJ-7 fires on registry membership; care-team
permits read it), yet any process can `add_member` — and reads have write side effects
(`CREATE TABLE IF NOT EXISTS` in `care_team_keys._connect`, established D-52).

**If one process owns writes:** every INJ-7 decision *reads* the registry, so reads
must stay open or be served by the owner. sqlite WAL tolerates one-writer/many-readers
— so the honest migration is small: registry *mutations* move behind the write-owner's
API; reads stay direct (or move to the same API for one clock). What breaks meanwhile:
enrollment from the voice orch [live, hip-harness tree] would need the RPC. **The real
break is different:** the file lives in the frozen checkout — the roadmap "boundary"
depends on a path inside a tree that is contractually not allowed to change.

### (3) Voice orch on a frozen hip-harness checkout [live]

Verified from launchd, not memory: `com.hip.voice.orch.plist` runs
`cd [REDACTED-USER-PATH]/hip-harness && .venv/bin/python3 -m server.voice_https_orch`
(:7860, pid 16242, KeepAlive). hip-harness sits on `voice-latency @ f8fadbd` —
**the live voice path runs governance code from the frozen tree**, not from roadmap.
Every roadmap gate improvement since the freeze (R29/R30 registry, R18 cascade,
sensitivity fail-closed, trust fixes) is **absent from the process actually taking
audio**.

**If one process owns writes:** this is the violation that becomes intolerable —
the frozen orch writes to the same graph with pre-fix write logic; two generations of
`_write_one` disagree about sealing/sensitivity semantics against one store.
**Migration:** the voice orch becomes a *client* (the already-ruled contract:
turn/on_route/register_member/session_end); its writes route to the owner process
running current code; the frozen tree keeps only capture + STT + speaker-verify.
This is precisely the Voice-to-core contract — the recon's finding is that the running
system is the contract's exact inversion: the frozen tree holds the write authority
and the current tree holds none of the traffic.

---

## 2d. Misplaced logic — the full list, both directions

### Core logic living in the voice module (`server/voice_orch.py` — 3,541 lines) [roadmap, mirrored in vo]

| What | Where | Why it's core |
|---|---|---|
| `assemble_governed_context` | `:2468` | THE read-side gate composition — retrieval→INJ→disclosure. Imported *back* by dashboards and `harness/realtime_adapter.py` |
| `process_text_query` | `:2653` | the entire governed turn (the only other full composition) |
| `DisclosureBlocked` | `:2448` | the disclosure contract's exception type — callers must import it from the voice module |
| `_gate_double_valued_park_query` | `:2351` | a GATE |
| `_gate_unconfirmed_update` | `:2389` | a GATE |
| `_build_requester` | `:619` | constructs the requester principal used by INJ |
| `UNCONFIRMED_UPDATE_REPLY` / `PARKED_UPDATE_REPLY` | `:2324` | governed-wording contract (D-46/D-27 lineage) |
| core-pin logic (`_is_core_pin_query` / `_build_core_pin_reply`) | `:2355+` | routing policy |
| `emit_epistemic_record` wrapper | `:2681` | the D-1 audit emission point |
| routing/disclosure log writers | `:212,:277` | the telemetry every pane and half the harness asserts against |

### Voice logic living in the core package (`harness/`) [roadmap]

`harness/speech.py` (Whisper + Kokoro), `harness/speaker_id.py` (resemblyzer,
voiceprint crypto), `harness/voice_session.py`. These pull torch/onnx/audio deps into
the same import namespace as the injection contract.

### Neither-direction misplacements worth naming

- **`extraction_queue.py` is a grab-bag with the credential in it**: Neo4j config +
  `_get_driver` + `_neo4j_password` (with plist fallback) + embeddings client + sqlite
  queue + the write path + the *read* path (`read_user_facts`,
  `search_facts_by_embedding`) + the attribute vocabulary (`CANONICAL_ATTRIBUTES`).
  Consequence: the **read-side gate imports from the write module**
  (`injection_contract.py:81`), the dashboard imports the credential accessor
  (`memory_dashboard.py:40`), and anything needing embeddings drags the write path in.
- **`recall.py`** (read) performs writes (`access_count`), so the read path cannot be
  given a read-only credential as-is.
- **`fact_change.py`** mixes the Groq client with write-decision logic — a remote-model
  call site inside the write path module.

---

## 2e. The ledger [roadmap]

What exists (`harness/epistemic_ledger.py`) is genuinely good **within** its trust
model: hash-chained segmented JSONL, `F_FULLFSYNC` before the reply leaves, per-member
AES-256-GCM payload keys with crypto-shred (`destroy_member_key`), chain hash over
ciphertext so verify survives shredding, flock'd multi-process appends, TD-030
value-stripping, spool-on-failure.

**Structural separation today: none.**
1. The append is called from the deciding process (`emit_epistemic_record` →
   `turns_demo.jsonl` AND the HEL, `epistemic_record.py:306`; key-custody modules
   append directly).
2. `ledger/`, `ledger/keys/`, and the spool are files under the **same UID** as every
   other process. Any of the six hip processes on this box can call
   `destroy_member_key()`, delete segments, or rewrite the chain from genesis and
   re-hash — verification reads the same disk it distrusts.
3. **Deliberate and worth restating: audit is best-effort by design.** `append()` never
   raises toward the caller (the D-1 invariant — "governance outcome identical with or
   without the record"). A turn whose record failed still answers. That is a defensible
   availability choice; it is also the definition of an audit the decision-maker can
   proceed without.

**Cost to separate:** a ledger-writer process under its own UID owning `ledger/` +
keys, fed over a local socket — ~2-3 dispatch-days, and the failure semantics must be
redesigned (socket down → spool locally → reconcile, or the D-1 invariant breaks).
**The cheap alternative that buys most of the value: anchoring, not separation** —
periodically sign the chain head and put it where these processes can't write
(~0.5 dispatch-day). Anchoring makes rewrite *detectable*; separation makes it *hard*.
Those are different properties; the REQ backlog should name which one is being bought.

---

## 2f. Inference [roadmap]/[vo]/[live]

**Correction to the dispatch's premise: the model *call* already crosses a process
boundary everywhere.** Local models are Ollama over HTTP (`extraction_queue.py:345`,
voice orch edge model); Groq and OpenAI are remote. No model weights execute inside
any governance-composing process — with the exception of the **voice** models: Whisper
(ctranslate2), Kokoro (onnxruntime), resemblyzer (torch) run **in the voice orch
process** [live: pid 16242, frozen tree] — which is also the process holding the graph
credential, the extraction path, and the HEL append. The memory-unsafe parsers and the
write authority share a heap *today*.

What "treat inference as untrusted" changes, concretely, in this codebase:

1. **Ingress (model output is attacker-influenced input).** Two model-output→write
   paths exist: `extract_facts` → `write_facts` (session end), and `call_frontier` →
   `write_frontier_fact` → `encode()` (`disclosure.py:241-258`). Both currently write
   with the session's full authority. Untrusted-inference means both become *proposals*
   validated at admission — which is R10's origin-path rule stated in security terms.
   TD-110 (cross-member supersede, no authority check) is this gap already filed.
2. **Egress (what leaves the boundary).** TD-131 [vo tree, filed 4390240]: household
   facts reach the MID/CORE Groq payload unfiltered — `strip_context_for_tier` exists
   (`orchestrator.py:703`) but doesn't cover those tiers. Untrusted-inference makes the
   egress payload a disclosure decision per call, which is the discipline the frontier
   path already has and the tier path lacks.
3. **The runtimes.** Nothing changes for Ollama/Groq (already out). The change is
   acknowledging the voice process's Whisper/Kokoro/resemblyzer as the unsafe-parser
   zone and stripping that process of standing write authority — which is the same
   migration as 2c(3).

---

## 3. Where a split helps / where it hurts — both columns, grounded

### WOULD HELP

| Split | Grounding |
|---|---|
| Write authority into one owner process | 2b: ~14 modules reach writes via import; three CREATE implementations drift (comment-discipline mirroring in `_write_one`); frozen-tree orch writes with stale logic against the same graph |
| Voice orch → credential-less client | it holds the unsafe parsers + mic + write authority in one heap [live]; the ruled contract already names the seam |
| Ledger custody (or at minimum external anchoring) | 2e: same-UID keys mean crypto-shred and chain-rewrite are available to every process; anchoring is 0.5 day |
| Registry mutations behind the owner | 2c(2): governance input writable by any process, reads with write side effects, lives in the frozen tree |
| Extraction admission into the owner | model-output→write with full authority (TD-110); R10/A1/A10 all land naturally at one admission point |
| Dashboard → pure client | it already is one for reads; only `process_text_query` and the credential import violate it |

### WOULD HURT

| Split | Grounding |
|---|---|
| INJ gates as a service | pure functions applied per-fact over dozens of facts per turn; a network hop per evaluation is latency with zero isolation gain — the caller still chooses whether to call (INJ-7's `member_ids=None` shows the risk is *omission*, which RPC makes easier, not harder) |
| write_rule / trust / sensitivity out of the write transaction | `_write_one:41-51` classifies trust *inside* `tx.run` mid-transaction; `encode()` classifies before P8 in one transaction. Split = the check and the write no longer commit atomically — the exact defect class R18/D-81 just closed for retraction |
| Confirmation gate from the write path | parks are graph state (`write_state`); `apply_confirm` and the original write must see one transactional world |
| R18 cascade as its own service | it runs in the caller's transaction BY DESIGN (D-81); separating it reintroduces committed-retraction-without-cascade |
| Consolidation/extraction into per-gate microservices | they're batch jobs with queue state; the win is *admission* control at the writer, not distribution of the pipeline stages |
| Ledger as a *remote* service | D-1 wants the record durable before the reply leaves; 4-6.6ms local fsync budget tolerates a local-socket hop, not a network dependency on the answer path |

The two columns agree with the standing ruling in shape — monolithic governance core,
contracted clients — and disagree with the deployment in every particular.

---

## 4. Cost to make the write boundary structural in one process (A10 → LIVE)

**Premise correction first (same as A18):** there is no A10 XFAIL to flip. It would be
written LIVE with its twin, new.

What A10 actually needs — `encode()` revalidating origin, attribute registry,
representation class, and permit, such that a direct call cannot skip them:

| Step | Work | Est. |
|---|---|---|
| 1 | **Converge three CREATE paths on one.** `_write_one` and `_write_derived_node` become `encode()` callers (or thin transaction-participants of it). This is the load-bearing step: after it, "the checks at encode" means the checks, period | 2–3 days |
| 2 | **Define the origin vocabulary and permit evidence.** R10's checks need an `origin` the caller cannot fabricate freely: extraction / self_report / attributed_import / derivation / migration / fixture, plus the attribute-registry and representation checks. Requires the A1 allowlist (`DERIVABLE_ATTRIBUTES` — does not exist; D-77 warning about the second-vocabulary drift applies) | 1 day |
| 3 | **Plumb origin through every legitimate caller** (~10 modules incl. eval/scripts; fail-closed = every unplumbed caller breaks loudly, which is the point) | 1 day |
| 4 | A10 battery + fault twin (a bypassing direct call must be REFUSED; the twin proves the check can go red), harness + RATCHET | 0.5–1 day |

**Total: 4.5–6 dispatch-days.** Note what this buys and doesn't: in CPython, a hostile
importer can still monkeypatch `encode` itself — in-process structure stops *careless*
callers (all nine current ones), not hostile ones. The hostile-caller boundary is the
separate-process/credential migration (2c), which is additional work on top.

**Riskiest assumption: that the three write paths are semantically reconcilable.**
`_write_one` and `encode()` already diverge in documented ways (`embedding=None`
invisibility note at `orchestrator.py:274`; the D8-fixture mirroring comments; encode's
WriteDecision machinery vs `_write_one`'s inline supersede) — and the frozen orch
[live] runs a *fourth*, older variant against the same graph. Unifying may change live
write behavior in cases no fixture currently pins, and the demo graph is frozen: the
convergence must be proven by the memory harness *and* a before/after diff on a graph
copy, not by inspection. Second-order risk: fail-closed origin checks break every eval
seed and script until step 3 lands — steps 1–3 are one atomic dispatch or the tree is
red in between.

---

## Answers in one line each

- **2a** — INJ order is structural; the cross-module chain is call-sequence convention
  (INJ-7 off by default proves it); the write chain is copied three times.
- **2b** — ~14 modules reach writes, ≥9 outside any boundary; A10's runner was never
  written; encode lacks all four R10 checks.
- **2c** — dashboard: one import becomes one RPC; registry: mutations move, reads can
  stay; frozen orch: the live inversion of the ruled contract, and the migration IS the
  contract.
- **2d** — ten core items live in voice_orch.py; three voice modules live in harness/;
  extraction_queue is a grab-bag holding the credential.
- **2e** — ledger integrity is real against crashes, absent against any same-UID
  process; anchoring (0.5d) buys detectability, separation (2-3d) buys resistance.
- **2f** — model calls already cross processes; the actual gaps are the two
  model-output→write paths (TD-110) and tier egress (TD-131); the unsafe runtimes share
  a heap with write authority in the voice process.
- **3** — split authority and custody; do not split gates, transactions, or the chain.
- **4** — 4.5–6 dispatch-days to A10-LIVE; riskiest assumption is that the three (four,
  counting frozen) write paths mean the same thing.

Nothing changed in any tree. No status proposed; R10/A10 remain Bill's to rule.
