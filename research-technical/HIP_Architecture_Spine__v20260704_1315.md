# HIP — Build-for-Deployment Architecture Spine

**Author / design authority:** Bill Brewster — 20+ years building and operating national-scale, governed, multi-entity service-delivery platforms in telecom, cable, and ad tech. Built and ran national video operations at Comcast (X1). Led a multi-entity operational ecosystem at Canoe Ventures. Deep experience in regulated, compliance-heavy environments, translating technical systems into operator business outcomes. HIP applies that operating discipline — execution integrity, governed change, unit-cost economics — to an AI operating system. The architecture below is authored by an operator who has run infrastructure at the scale this platform targets.

**Purpose:** the architecture roadmap for the Superset package — as if building for real deployment on a cable/telco operator's edge. For every layer: is it *new-art* (build and own), *prior-art* (rent from the tool rack), or *prior-art modified*; the OSS substitute to bootstrap on until funding, the production target after; true cost; and the strategic leverage for a cable operator specifically.

**Organizing axis (the thesis as the design rule):** raw intelligence commoditizes, context compounds. Anything in the commoditizing layer is rented (OSS now, managed/commercial at scale). Anything in the compounding layer is built and owned. The sort *is* the strategic argument: building in the commodity layer is a flag; renting in the compounding layer is a moat leak.

**The single load-bearing finding (from the 2026 research scan):** the moat is not model access. Every model is commodity and rentable. The defensible architecture is **secret-handling at the edge** — attestation, key release, revocation, recovery, side-channel control. The operator can run compute, observe health, meter, and bill — but cannot decrypt household memory or prompts outside an attested, user-authorized path. That is the product.

---

## Layer sort at a glance

| # | Layer | Verdict | Compounds or commoditizes | Own it? |
|---|---|---|---|---|
| 1 | Edge inference (models) | Prior-art, rent | Commoditizes | No |
| 2 | Escalation / routing cascade | **New-art** | Compounds (margin) | **Yes** |
| 3 | Context / memory layer | **Modified** (storage rented, injection contract owned) | Compounds (moat) | **Injection: yes** |
| 4 | Encryption / operator-blind boundary | **Modified** (crypto rented, architecture owned) | Compounds (liability moat) | **Architecture: yes** |
| 5 | Confidential-computing enclave | Prior-art, adopt (partner co-build) | Enables the moat | Adopt, don't build |
| 6 | Voice / interaction | Prior-art, rent | Commoditizes | No |
| 7 | Governance / testing harness | **New-art** | Compounds (compliance moat) | **Yes** |
| 8 | Consent / authorization | **New-art** | Compounds (trust moat) | **Yes** |
| 9 | Key management / recovery | **Modified** (primitives rented, hierarchy owned) | Compounds (trust) | **Hierarchy: yes** |

Five of nine layers are commodity or adopt-and-integrate. Four are new-art you own. Those four — routing, injection contract, operator-blind architecture, governance harness — are HIP. Everything else is a tool-rack selection.

---

## 1. Edge inference (the models)

**Verdict: prior-art, rent. Keep swappable — swappability is a feature, not a gap.**

- **OSS-now:** Ollama + Qwen3 8B/14B (Apache 2.0) home tier; Groq-hosted Llama for the current prototype's Mid/Core.
- **Production target — two viable tracks:**
  - *Multi-vendor (portability-first):* Qwen3 8B/14B or Phi-4-mini (MIT) on home/CPE; Mistral Small 4 NIM or Qwen3-32B NVFP4 on operator-edge core. Keeps the model layer swappable across vendors. **Avoid making Meta's custom Llama license the legal foundation** — it is not OSI-open and carries large-user terms a telco legal team will flag.
  - *NVIDIA-vertical (coherence-first):* **NVIDIA Nemotron models** on Nemotron-optimized NIM on NVIDIA confidential GPU. For an operator already standardizing on NVIDIA edge (see layer 5), a single-vendor stack is a real strategic argument: one attestation story, one support contract, one optimization/serving path, one accountable vendor. Nemotron is a first-class model option here, not just infrastructure — the model, the serving (NIM), and the confidential-compute boundary come from one vendor with one integration surface.
- **The tradeoff to make explicitly:** multi-vendor buys portability and licensing safety; NVIDIA-vertical buys operational coherence and a single attestation/support surface. For a first-operator pilot standardizing on NVIDIA confidential GPUs, the vertical stack lowers integration risk; for a portability-hedged platform, keep the model layer swappable. State the choice as a deliberate architecture decision, not a default.
- **True cost:** OSS = engineering time to package + edge compute. Production = per-GPU NVIDIA AI Enterprise (~$4,500/GPU/yr or ~$1/GPU-hr) for NIM packaging, plus edge hardware. NVIDIA-vertical amortizes the same GPU/NIM spend across model + serving + confidential compute rather than integrating three vendors.
- **Operator leverage:** runs on infrastructure the operator already deploys or can stand up cheaply; the tiering means most inference is the cheapest model, which is the operator's margin story. NVIDIA-vertical additionally reduces the operator's integration and vendor-management overhead.
- **Flag:** do not fine-tune a base model. That is investment in the commoditizing layer and it fights the thesis. Interchangeability (or deliberate vertical coherence) is the design win — not owning the weights.

## 2. Escalation / routing cascade — **NEW-ART, OWN IT**

**Verdict: build. This is the cost-control layer and it is already built and gated (Bloom cascade, sensitivity ceiling, 5-tier routing, 91.2% harness).**

- **OSS-now / production:** same code — it's yours. No substitute exists that does governed, tested, sensitivity-capped tier routing.
- **True cost:** already sunk (built). Ongoing = corpus maintenance.
- **Operator leverage:** this is the unit-economics engine. The tier column *is* the per-query cost model. "Cheap by default, escalate only when justified, never escalate off-net when sensitive" is the operator's margin-and-compliance argument in one mechanism. No vendor sells this; it's the thing that makes the P&L work.

## 3. Context / memory layer — **MODIFIED: rent storage, own the injection contract**

**Verdict: the store is prior-art; the governed injection + subject-resolution is new-art and is the moat.**

- **OSS-now:** Neo4j (household graph) + nomic-embed + the injection contract (built, 11/11 gate). Local-first.
- **Production target:** local encrypted household memory as default; TEE-backed pgvector/Qdrant at the operator edge **only** for explicitly authorized, attestation-gated derived memory. Benchmark Zep/Graphiti, Mem0, Letta for memory *quality* — **use none as the security boundary** (the research confirms none offer operator-blind / user-held-key encryption by default).
- **True cost:** OSS = eng time. Production = TEE integration eng + edge storage; local-first pushes most cost to the CPE/home device (operator-favorable).
- **Operator leverage:** this is the compounding moat — subscriber context that gets more valuable over time and creates switching cost. The store commoditizes; the *learned schema + governed injection* is what compounds and what an operator can't buy elsewhere.
- **Design rule (from research):** raw household facts stay home-device local, client-side encrypted. Only derived, authorized summaries reach the operator-edge TEE. Global knowledge and frontier fallback never carry household secrets.

## 4. Encryption / operator-blind boundary — **MODIFIED: rent the crypto, own the architecture**

**Verdict: primitives are prior-art; the operator-blind architecture (operator hosts, cannot read; consumer holds key; neutral recovery) is new-art integration and is the liability moat.**

- **OSS-now:** envelope encryption (HKDF-SHA256, per-member DEKs) — built, and the embedding-invertibility regression already found and fixed (subject+predicate only).
- **Production target:** device-held root keys (Secure Enclave / StrongBox), attestation-gated session-decrypt keys released only inside an attested TEE, per-user and per-household wrapped data keys.
- **True cost:** OSS = eng time (done for the prototype boundary). Production = attestation infrastructure + key-broker + HSM, the genuinely hard and expensive part.
- **Operator leverage:** **this is what de-risks the operator legally.** They host household data they cannot read, so their liability surface collapses. For a compliance-heavy operator, "we host it but cannot see it" is the single most valuable architectural claim in the package.
- **Honest limit for the package:** the prototype proves the *architecture*; the production attestation/key-release path is the funded build. Do not overstate — claim the design and the threat model, not zero-leakage.

## 5. Confidential-computing enclave — **PRIOR-ART, ADOPT (partner co-build)**

**Verdict: do not build. Adopt NVIDIA GPU CC + Confidential Containers + CPU TEE. This is the highest-leverage adoption and the natural partner co-build.**

- **OSS-now:** not applicable at prototype scale — the current prototype is trusted-local; Mid/Core run on Groq. State this honestly: **"operator-edge enclave is architecture, not running."**
- **Production target (from research):** NVIDIA GPU Confidential Computing on Hopper/Blackwell, deployed via Confidential Containers with composite CPU+GPU attestation, plus Intel TDX or patched/validated AMD SEV-SNP for the control plane. CPU-only TEEs are necessary but insufficient — the GPU accelerator path is the weak point, so confidential GPU is required for real LLM inference.
- **True cost:** high capex (H100/H200/B200-class), NVIDIA AI Enterprise recurring, plus heavy attestation/key-brokerage engineering. This is the funded, hardware-dependent phase.
- **Operator leverage:** converts "operator-blind" from claim to fact, and operators *already have the edge footprint* to host it. This is where HIP becomes an AI substrate on infrastructure they own. It's a co-build candidate precisely because the operator brings the edge estate.
- **Risk flag (from research):** the hard problem is not model availability — it is secret handling: attestation policy, key release, revocation, recovery, side-channels. AMD SEV-SNP had a 2026 "Fabricked" disclosure; Intel TDX 1.5 had a 2026 security assessment finding issues. Firmware/patch trust is now central. Own the security model; do not assume the TEE vendor closes it for you.

## 6. Voice / interaction — **PRIOR-ART, RENT**

**Verdict: rent, keep swappable. Lowest-differentiation layer — do not sink effort here.**

- **OSS-now:** Pipecat (WebRTC) + Whisper small.en + Kokoro TTS + Resemblyzer. Working.
- **Production target:** NVIDIA Parakeet/Canary (NeMo/Riva/NIM) for STT — bundled with the enclave hardware adoption, same NVIDIA stack; Whisper as OSS fallback; Qwen3-ASR as a benchmark candidate. For speaker ID: TitaNet/WeSpeaker for *recognition*, but a commercial anti-spoof stack (ID R&D) for any *authorization* decision — recognizing "sounds like Bill" is not enough to release private memory.
- **True cost:** OSS = low. Production STT bundles into the NVIDIA enclave spend; anti-spoof is per-user commercial licensing when biometric authorization goes live.
- **Operator leverage:** low. It's the skin. Drive demos text-first; voice is a cameo. Do not let audio polish pull effort from the logic layer that is the moat.

## 7. Governance / testing harness — **NEW-ART, OWN IT (underrated moat)**

**Verdict: build. Already built (routing + injection + integration gates, 6-check gate_check.sh, ratchet rule).**

- **OSS-now / production:** yours. No vendor sells a governed change-process for an LLM operating system.
- **True cost:** sunk. Ongoing = scenario maintenance (the ratchet makes it self-densifying).
- **Operator leverage:** for a compliance-heavy operator, a system whose *change process itself is governed, gated, and auditable* is the differentiator. "Every routing decision is deterministic, logged, traceable to a committed rule, gated by a test" is the compliance-and-liability story. This is your operating identity — execution integrity — made mechanical, and it's part of the pitch, not just the engineering.

## 8. Consent / authorization — **NEW-ART, OWN IT**

**Verdict: build. Reconsider/frontier control loop built and gated (codeword gate, sensitivity confirm, INV-1/2/3 proven).**

- **OSS-now / production:** yours.
- **True cost:** sunk.
- **Operator leverage:** the consumer-trust and regulatory story. The auditable claim — "no data leaves the home without a codeword event in the log; reconsider can never reach the network" — is exactly what a security team verifies. Consumer-facing, it's the trust the operator sells.

## 9. Key management / recovery — **MODIFIED: rent primitives, own the hierarchy**

**Verdict: primitives are prior-art; the key hierarchy and threshold-recovery design are the owned integration.**

- **OSS-now:** device Secure Enclave/StrongBox + Shamir/SLIP-39 shares.
- **Production target (from research):** device-held root keys; per-user and per-household wrapped data keys; short-lived edge-session decrypt keys released only after attestation; 2-of-3 or 3-of-5 recovery split across user devices, a trusted recovery contact, and a neutral escrow/HSM. **The operator never holds enough material to recover household memory.**
- **True cost:** OSS primitives free; production = HSM + escrow governance + recovery UX + abuse-case modeling (household-coercion scenarios must be explicitly designed).
- **Operator leverage:** completes the operator-blind guarantee — recovery authority is never coupled to the operator or to training authority. This is the "we can't see it even to recover it" claim that makes the liability story airtight.

---

## Integration architecture (how they compose)

```
HOME BOUNDARY (client-side encrypted, operator cannot see)
  Home/CPE device: Qwen3-8B/Phi-4-mini · wake/route/consent/private summary
  Local encrypted memory (raw facts, names, schedules, medical) — default residence
  Device key in Secure Enclave/StrongBox
        │  only derived, authorized, redacted summaries cross ▼  (codeword + attestation)
OPERATOR EDGE (attested TEE — operator hosts, cannot read plaintext)
  Confidential GPU (NVIDIA CC) + Confidential Containers + CPU TEE (TDX/SEV-SNP)
  Core LLM: Mistral Small 4 / Qwen3-32B NVFP4 · heavier reasoning, family synthesis
  TEE-backed pgvector/Qdrant — authorized derived memory only, attestation-gated decrypt
        │  explicit user authorization only ▼
FRONTIER (external, off-net) — redacted, scoped, logged; never the default path
```

The routing cascade (2), injection contract (3), operator-blind architecture (4), governance harness (7), and consent layer (8) are the owned connective tissue that makes this composition governed rather than a pile of rented parts. That connective tissue is HIP.

---

## Phased roadmap

**Phase A — Bootstrap on OSS (now, largely done):** local-first, trusted-local prototype. Ollama/Qwen + Neo4j + envelope encryption + the four owned layers, all gated. Proves the architecture. **This exists.**

**Phase B — Prove operator-edge (funded, partner co-build):** stand up one confidential-GPU edge node (NVIDIA CC + Confidential Containers + CPU TEE). Move Mid/Core off Groq onto the attested edge. Wire attestation-gated key release. This is where "operator-blind" becomes fact. Requires funding and an operator's edge estate — the natural first-operator pilot.

**Phase C — Scale:** production key hierarchy + threshold recovery + HSM; commercial anti-spoof for biometric authorization; multi-member voice; per-household provisioning. Unit economics harden here.

---

## Cost basis (both, per Superset convention)

**Build economics (to get there):**
- Phase A: sunk (prototype engineering).
- Phase B: 1 confidential-GPU node (H100/H200-class capex) + NVIDIA AI Enterprise (~$4,500/GPU/yr) + attestation/key-broker engineering (the dominant eng cost) + one operator-pilot integration.
- Phase C: HSM + escrow governance + anti-spoof licensing + multi-device recovery UX + provisioning automation.

**Deployment economics (per household at scale):** feeds the existing Monte Carlo model. The tiering is the lever — most queries resolve on the cheapest (home/edge) tier at ~zero marginal token cost; only authorized escalations incur edge-GPU or frontier cost. Per-household run cost is dominated by (a) home-device compute (operator-favorable, pushed to CPE), (b) amortized operator-edge GPU for the authorized-derived-memory fraction, (c) rare frontier calls. The unit-cost story is: **context compounds in value while marginal inference cost stays near the cheapest tier.**

---

## The one-line strategic call

The models are commodity; the moat is governed, operator-blind secret-handling at the edge. HIP owns exactly the four layers that compound — routing (margin), injection contract (context moat), operator-blind architecture (liability moat), governance harness (compliance moat) — and rents everything that commoditizes. For a cable operator, that maps to: their edge estate becomes an AI substrate, they host household intelligence they are not liable for reading, and the unit economics stay near the cheapest tier by construction. The funded build is the confidential-computing enclave and the production key hierarchy — the two places where "operator-blind" moves from proven architecture to running fact, and the natural place a first operator co-invests.
