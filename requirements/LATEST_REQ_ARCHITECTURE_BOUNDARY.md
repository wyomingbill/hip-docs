# REQ_ARCHITECTURE_BOUNDARY — reference monitor, threat model, and contracted clients
Status: FILED
Reconciled-Against: 4ae70cc (roadmap HEAD at filing, verified by reading it at filing time — not a remembered hash)
Dispatch: D-85, 2026-08-01
Acceptance: **NOT RUN.** No acceptance row in this REQ has been executed. Nothing here is MET.

**WHAT THIS DOCUMENT IS.** It records **rulings already made** by Bill and the
architectural facts those rulings rest on. It is not new design and it authorizes no
build. Where it names a gap, the gap is recorded — not scheduled, not fixed.

**EVIDENCE.** Two artifacts, both banked verbatim under D-85:

- `docs/reviews/FABLE_D84_monolith-vs-services__architecture-recon-four-trees__v20260801_0919.md`
  — the code-grounded recon, read-only across four trees plus the live process table.
  UNVERIFIED (reviewer's findings, not independently confirmed).
- `docs/reviews/CHATGPT_D84_architecture-research__reference-monitor-and-runtime-isolation__v20260801_0919.md`
  — the external research pass supplying the reference-monitor / complete-mediation
  vocabulary this REQ adopts. UNVERIFIED, citations unchecked by this dispatch.

Where the two disagree in what they can support: the research pass supplies the naming and
the literature; the recon supplies the `file:line` evidence that the property is currently
absent. **This REQ adopts the vocabulary and records the absence.**

---

## 1. THREAT MODEL (ruling 2a)

### In scope

| # | Adversary | What they can do |
|---|---|---|
| T1 | **Careless code** | A well-meaning caller imports the write function and skips the gate chain. Not hypothetical: nine current callers already do (§2). |
| T2 | **A hostile household member** | An authenticated principal of the system attempting to read or write outside their own boundary. |
| T3 | **A compromised dependency** | Arbitrary code executing inside a HIP process, with that process's full authority. |
| T4 | **A remote attacker** | Reaching the box over the network — the dashboard endpoints, the voice transport, or a malicious model/audio artifact parsed by a memory-unsafe runtime. |

### Out of scope FOR NOW — deferred, not dismissed

| # | Adversary | Why deferred |
|---|---|---|
| T5 | **The operator** | On operator-provided hardware, whoever holds OS root defeats every boundary in this document. No in-box structure defends against the box's owner. This is a real limit on what the ledger can be credible *to*, and it is deferred rather than dismissed: it must be answered before any claim that the record is credible to a third party. |

### THE CONSEQUENCE, stated plainly

**Three of the four in-scope adversaries defeat an in-process boundary in CPython.**

T2, T3, and T4 all end with code running inside a HIP process. In CPython there is no
in-process boundary that survives that: module privacy is a naming convention, type
annotations are erased at runtime, reflection and monkeypatching reach everything, and a
"capability token" held in the same address space as its holder is forgeable by anything
in that address space. An admission proof HMAC'd with a key the forger can read is
circular.

**T1 — careless code — is the ONLY adversary an in-process structural boundary stops.**
That is a real and worthwhile property: it is the one that stops the nine callers below
from drifting further, and it is what A10 buys.

**Everything else needs the OS boundary: a separate process, its own UID, and a credential
the other processes do not have.** This is a ruling about where effort has to go, not a
schedule for going there.

---

## 2. THE MONOLITH RULING (ruling 2b)

### Ratified

**The governance core stays MONOLITHIC inside a hard boundary, with contracted clients
outside it.** The gates are ordered and interdependent; splitting the ordered policy chain
into cooperating services multiplies the surfaces where a check can be omitted, and there
is no scale pressure whatsoever — one household, one box, single-digit users.

The core is hereby named for what it is: a **REFERENCE MONITOR**, and its target property
is **COMPLETE MEDIATION** — every read, disclosure, inference-context construction,
mutation, and export involving governed data is mediated by it, with no path around.

**Monolithic is the deployment shape. Complete mediation is the security property. The
first does not imply the second.** Adopting the name is adopting the obligation.

### It does not have that property today — recorded, not scheduled

Evidence from the D-84 recon, `[roadmap @ 4ae70cc]` unless noted:

- **Roughly fourteen modules reach a graph write; at least nine sit outside any
  defensible boundary** — `scripts/demo_seed.py`, `scripts/realtime_voice_demo.py`,
  `scripts/realtime_care_coord_smoke.py`, `scripts/migrate_*.py` (2), `eval/memory_e2e.py`,
  `eval/memory_harness.py`, `eval/care_coord_run.py`, and the dashboards.
- **Every one of them works by `import`.** There is no admission point to pass.
- **Three independent `:Fact`-CREATE implementations exist** — `memory_engine/store.py::encode`,
  `harness/extraction_queue.py::_write_one` (its own `CREATE` at `:81`), and
  `memory_engine/consolidate.py::_write_derived_node` (its own `CREATE` at `:54`). They are
  kept in agreement by **comment discipline** — `_write_one` carries in-source notes about
  mirroring `store.encode()`'s overrides. A fourth, older variant runs live from the frozen
  tree (§3).
- **The plist credential fallback lets any process self-serve the graph password.**
  `harness/extraction_queue.py::_neo4j_password` falls back to reading `NEO4J_PASSWORD`
  from the launchd plist when the environment does not carry it. `server/memory_dashboard.py:40`
  imports that accessor directly. Convenience that is, precisely, the anti-pattern.
- **Neo4j Community has no row-level access control** (fine-grained access control is an
  Enterprise feature), so **the credential is the entire wall.** N processes holding it is
  not a smell; it is the hole.
- **Ordering is enforced three different ways.** Structural inside
  `apply_injection_contract` (one function body, fixed order, mutation-tested). By call
  sequence across the read chain — and the proof that this is convention rather than
  structure is that **INJ-7 is disabled by default**: `member_ids=None` turns it off
  entirely, so a caller that omits one keyword argument silently drops a gate. Copied
  three times on the write chain.
- **A10's strict-xfail was never written.** `REQ_CEILING_ACCEPTANCE` (D-77) classified A10
  as STRICT XFAIL, but no `eval/test_ceiling_inference.py` exists at HEAD. This is the same
  correction A18 required at D-81: classified is not wired. Cross-referenced in §6.

---

## 3. THE VOICE BOUNDARY (ruling 2c)

### Ratified

**Voice is UNTRUSTED BY CONSTRUCTION, regardless of vendor.** This is not a judgment about
any particular STT, TTS, or speaker-ID implementation, and it does not change if the vendor
changes. **HIP does not secure the voice stack. The boundary holds whatever is on the other
side of it.**

The reasoning is structural, not reputational: the voice component parses hostile input
(audio, codecs, model files) in memory-unsafe runtimes. It is the component most likely to
be compromised and the one whose compromise HIP can do least about.

### Two hard rules

1. **Voice never holds a graph credential.**
2. **Voice never executes in the process that owns writes.**

### The contract is a SECURITY boundary

`turn` / `on_route` / `register_member` / `session_end` is hereby a **security boundary,
not merely a modularity one.** It is where an untrusted component's assertions become
requests to a trusted one. Every parameter crossing it is attacker-influenced until the
core validates it.

### The live deployment is this ruling exactly inverted — recorded

From the D-84 recon, verified against launchd and the live process table, not from memory:
`com.hip.voice.orch.plist` runs `cd [REDACTED-USER-PATH]/hip-harness && .venv/bin/python3 -m
server.voice_https_orch` (:7860, KeepAlive). `[harness]` sits on `voice-latency @ f8fadbd`.

- The live voice path runs **governance code from the FROZEN checkout** — every roadmap
  gate improvement since the freeze (R29/R30 sensitivity registry, the R18 cascade,
  fail-closed sensitivity, the trust fixes) is **absent from the process actually taking
  audio**.
- That same process holds the graph credential, the extraction write path, and the HEL
  append, **and** runs Whisper (ctranslate2), Kokoro (onnxruntime), and resemblyzer
  (torch) — the memory-unsafe parsers and the write authority share one heap.
- Both hard rules above are violated by the running system today.

---

## 4. THE INFERENCE BOUNDARY (ruling 2d)

### Ratified — a contract direction, NOT a build

**Model output is attacker-influenced input, and HIP's model output can write.**

**MODELS PROPOSE; ONLY THE CORE COMMITS.** A model's output is a *proposal* that must
pass admission with the same suspicion as any other untrusted input. No model output
carries write authority by virtue of having been produced inside the boundary.

This states a direction. It authorizes no code and schedules no work.

### The two paths that exist today — recorded

| Path | Where | What it does |
|---|---|---|
| Extraction | `harness/extraction_queue.py::extract_facts` (Ollama, `:345`) → `write_facts` → `_write_one` | transcript → model → graph facts |
| Frontier return | `harness/frontier_client.py::call_frontier` → `harness/disclosure.py::write_frontier_fact` (`:241`) → `store.encode()` (`:258`) | remote model answer → graph fact |

**Neither has an authority gate. TD-110 records this** (any authenticated member can
supersede another member's health fact — no authority check, no provenance gate, no
corroboration requirement; INJ-3 blocks cross-member READ, nothing equivalent exists on
WRITE). An attacker who can influence a transcript is injecting into a write-capable model
channel.

**A premise correction the recon makes, carried here so it is not lost:** the model *call*
already crosses a process boundary everywhere — local models are Ollama over HTTP, Groq and
OpenAI are remote. No model weights execute inside a governance-composing process **except
in the voice process** (§3). The exposure is therefore not "the model call is inside the
boundary"; it is (a) the two write paths above, (b) egress — **TD-131**, household facts
reaching the MID/CORE Groq payload unfiltered, `strip_context_for_tier`
(`harness/orchestrator.py:703`) not covering those tiers — and (c) the voice process's
shared heap.

---

## 5. THE TWO PROPERTIES THAT DO NOT EXIST (ruling 2e)

The security story rests on two properties. **Neither is built.** Recorded here so that no
future document can assume them.

### 5.1 A single-writer process that actually exists

**Ruled:** governance lives with the data; exactly one process owns writes to the fact
store; everything else is a client of it.

**Reality:** there is no such process. There are N processes sharing one credential — three
dashboards were running at recon time (two of them able to import `process_text_query` and
execute a full governed turn in-process), plus the frozen voice orch, plus every script and
eval module. The ruling describes an intended architecture, not a deployed one.

### 5.2 An audit anchor the writer cannot reach

**Reality:** `harness/epistemic_ledger.py` is strong within its trust model — hash-chained
segmented JSONL, `F_FULLFSYNC` before the reply returns, per-member AES-256-GCM payload
keys with crypto-shred, chain hash over ciphertext so verification survives shredding,
flock'd multi-process append ordering, TD-030 value-stripping, spool-on-failure.

**And it has no structural separation whatsoever.** The append is called from the deciding
process. `ledger/`, `ledger/keys/`, and the spool sit under the **same UID** as every other
HIP process. Any of them can call `destroy_member_key()`, delete segments, or rewrite the
chain from genesis and re-hash — and verification reads the same disk it is supposed to
distrust. **A hash chain custodied by the process that writes it is tamper-evident against
nobody.**

Two further facts, recorded without judgment:

- **Audit is best-effort by design.** `append()` never raises toward the caller — the D-1
  invariant, "governance outcome identical with or without the record." A turn whose record
  failed still answers. Defensible as availability; it is also, precisely, an audit the
  decision-maker can proceed without.
- **Anchoring and separation are different properties.** Signing the chain head
  periodically to somewhere these processes cannot write makes a rewrite *detectable*. A
  separate custody process makes it *hard*. Cheap and expensive respectively; they are not
  substitutes. Bill has now built the cheap one (below) — that is a fact about what exists,
  not a formal ruling that forecloses the expensive one; **whether separation is ever also
  built remains Bill's call and is still not made here.**

**UPDATE (D-98, 2026-08-01): the anchor this section named as absent now exists — stated
here with its limit in the same breath, not as a separate footnote.** A second machine
(Bill's laptop) that HIP holds no credential to and cannot initiate a connection toward now
holds `(seq, head_hash)` records fetched, at its own initiative, from `~/hip-anchors/` on
this box (`harness/anchor_emitter.py`, D-90; laptop fetch/verify per
`SPEC_ANCHOR_LAPTOP_FETCH`, D-95; built and exercised, D-98). Two anchors at seq 7074,
mode 444, both independently verified from this box to carry
`head_hash sha256:140ea35ebc48cb6fbc2b2b05dee363e4af589c983122fbfdd956b43012ab8a5e`. A
rewrite of the chain at or before seq 7074, from this point forward, is now detectable by a
party this UID cannot reach or compromise. **This buys DETECTABILITY, not RESISTANCE.**
Nothing stops the rewrite described two paragraphs above — the same UID can still call
`destroy_member_key()`, delete segments, or rewrite the chain from genesis, and
`epistemic_ledger.verify()` would still return `True`. What changed is that a rewrite at or
before an anchored position is no longer *invisible* to everyone, only to the writer's own
verification. **And the interval between anchors is the detection window, permanently and
by construction:** a rewrite of events appended between two anchors — or after the newest
one currently held — is undetectable by this scheme, forever, because no third party holds
a fingerprint of that position to compare against. This is not a residual bug to close; it
is the shape of what "periodic anchoring" *is*.

**Open, recorded rather than assumed closed:** cadence is not set (daily is a
recommendation in the design note, not a ruling), and no launchd job is installed on
either machine — both the mini's emission and the laptop's fetch were run by hand for
this proof, so today the detection window is bounded only by how often a human remembers
to run both steps, which could be arbitrarily long. The receiver countersignature
described in the design note as the intended source of evidentiary weight is unbuilt; what
exists today is the laptop's unsigned, read-only, append-only possession of the anchor
files since fetch time — real evidence, but resting on trusting the laptop's filesystem
state as reported, not on an independently checkable signature. Full detail:
`DESIGN_LEDGER_ANCHOR__detectability-not-resistance__v20260801_1300.md` §3 and §8.

---

## 6. CROSS-REFERENCES

| Item | Where | Relation to this REQ |
|---|---|---|
| **TD-110** | `docs/techdebt/LATEST_DEBT.md` | The §4 gap, already filed: cross-member write with no authority gate. The "models propose, core commits" direction is the shape of its eventual fix. Still OPEN, governance-decision-required. |
| **TD-131** | filed on `voice-port` (`4390240`) | Egress half of §4: household facts reach the MID/CORE Groq payload unfiltered. |
| **A10 / R10** | `LATEST_REQ_STRUCTURAL_CEILING` `:921`, `LATEST_REQ_CEILING_ACCEPTANCE` `:120` | The acceptance row for §2's complete-mediation target. **Its strict-xfail was never written** — same correction A18 needed at D-81. `encode()` performs none of R10's four checks (origin, attribute registry, representation class, permit). |
| **Ledger anchoring** | §5.2, no ID yet | Not filed as a TD — the anchor half is now BUILT and exercised (D-90/D-95/D-98, §5.2 update), so there is no defect to file; custody separation, the more expensive alternative property, remains an unmade, unbuilt ruling and is still recorded here rather than pre-empted. |
| **TD-137 / backlog #49** | `LATEST_DEBT.md` (RESOLVED for sensitivity), backlog | The two-clones divergence. Why backlog item #54 skips 51–53 (§7). |
| **REQ_VOICE_COMPONENT** | `docs/requirements/` on `voice-port` | Owns the contract §3 makes a security boundary. The Voice 21 freeze is why backlog #54 is urgent-before-freeze. |
| **D-82 recon** | `/tmp/d82_stt_in_the_demo_recon.md` — **UNBANKED** | Established the deck/voice seam and the enrolled-print separation numbers. Flagged: still outside the provenance record. |

---

## 7. WHAT THIS REQ DOES NOT DO

- **It rules nothing MET.** No acceptance has been run.
- **It authorizes no code.** CLAUDE.md item 8's gate is not satisfied by this document for
  any build; a build needs its own REQ or an explicit extension of this one.
- **It does not choose between anchoring and custody separation** (§5.2).
- **It does not schedule the single-writer migration.** §5.1 records absence; the D-84
  recon estimates 4.5–6 dispatch-days for the in-process half (A10 → LIVE) and notes that
  the hostile-caller boundary is additional work on top. Neither is authorized here.
- **It does not answer T5** (the operator). Deferred explicitly, §1.
- **It changes no code.** D-85 was a filing dispatch.

Companion backlog item: **#54 — independent speaker verification ("belt and suspenders")**,
`docs/BACKLOG.md`. Flagged URGENT-BEFORE-FREEZE because it changes the voice contract's
signature and that contract is being frozen in the other lane now.
