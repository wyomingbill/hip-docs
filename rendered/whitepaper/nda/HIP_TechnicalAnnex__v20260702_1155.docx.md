HIP Technical Annex
Architecture, Routing, and Enclave Design
Confidential. For NDA Distribution Only.
Bill Brewster
Olinda Solutions
July 2026

Table of Contents



1. Purpose and Scope
This annex documents the technical architecture of the Household Intelligence Platform in the depth required by an engineering reviewer, a confidential computing architect, and an infrastructure planning function inside a cable operator. It is intended for readers who have already read the public white paper and want to verify that the architecture is real, deployable, and consistent with the moat the platform is built to defend.
The annex covers: the four-tier inference cascade with actual model selections at each tier, the routing decision surface, the fact schema and lifecycle, the confidential computing enclave design and target hardware, the key custody hierarchy, the multi-member identity model, the deployment topology across operator infrastructure, and the reference bill of materials for a hub-class node.
This annex does not repeat the business case, does not repeat the market forces, and does not restate the moat argument. Those live in the confidential white paper. This document is what an engineer or a confidential computing architect would need to answer the technical questions that the white paper deliberately leaves for this document.
Every specific model, framework, hardware target, and library named in this document has been selected against a working prototype constraint. Where a component has been swapped during prototype development, both the current and the deprecated choice are noted with the reason.

2. The Inference Cascade
Every household query passes through a routing decision before it is served. The routing decision is not a heuristic. It is a classifier operating on three orthogonal signals about the query, and its output determines which of four inference tiers handles the request. The four tiers differ in cost per query, in latency, in privacy guarantee, and in the model class that runs on them.
2.1 The three routing signals
Before the query is dispatched, the router evaluates three questions in parallel:
Freshness. Does answering this query require information the household context graph does not hold, or that changes on a timescale shorter than the graph's refresh cadence. Weather, market prices, current news, real-time availability, and any query whose correct answer would be different an hour from now belong here.
Complexity. Does the query require reasoning that exceeds the capability of the small model running at the trust boundary. The complexity axis is measured against Bloom's taxonomy: remembering and understanding queries fit inside the small model's capability, applying and analyzing queries can be handled by the small model with degraded quality, and evaluating and creating queries must escalate to a larger model.
Sensitivity. Does the query touch content that must not leave the operator's infrastructure. Medications, medical detail, financial account information, minor-child schedules and location, and any content the household has marked as private are sensitivity-gated and cannot be sent to external inference providers regardless of complexity or freshness.
The router combines these three signals into a tier assignment. Freshness overrides complexity when freshness is required and complexity is low. Sensitivity overrides both when sensitivity is high, forcing the query into the enclave tier even if the same query at lower sensitivity would have gone to a passthrough.
2.2 Tier one: primary (edge)
The primary tier answers from household memory. A small model runs on operator-controlled infrastructure inside the trust boundary and responds to the majority of household interactions using only the household's own context graph. No external call is made. The query and its answer remain inside the operator's edge facility for the entire lifecycle.
Model of record: qwen2.5:7b, 8-bit quantized. Runs comfortably on a single Blackwell-generation edge GPU with 24GB of memory, leaves margin for the routing classifier and the fact retrieval pipeline. Latency target: sub-500ms end-to-end from voice input to voice output including transcription and TTS.
Model alternates considered: Llama 3.1 8B, Mistral 7B, Phi-3.5. Selection driven by (a) permissive license enabling commercial self-hosting at national-operator scale, (b) instruction-following quality on household-scoped queries, (c) throughput on the target hardware. Qwen2.5 7B leads on instruction following at the size. Llama 3.1 8B held as fallback.
Query classes served: "What time is practice tonight?" "When was the last refill for Mom's prescription?" "What did we decide about the holiday?" "Who is picking up Jake tomorrow?" Fact retrieval, schedule lookup, decision recall, member-scoped preference queries. All queries where the answer is already in the household context graph and no external information is required.
Bloom coverage: Levels 1 and 2 (remembering, understanding). The small model can also handle level 3 (applying) queries with degraded quality; those queries are routed to the mid tier when complexity budget permits.
Fraction of queries expected: 60 to 75 percent of household queries in steady state, based on prototype instrumentation and analogous voice-assistant deployments. This is the tier that carries the platform economics.
2.3 Tier two: freshness (mid)
The freshness tier handles queries requiring current information the context graph does not hold. The routing decision has already determined that the query needs live data. The tier's job is to fetch that data without leaking any household context to the external source.
Model of record: Groq Llama 3.1 8B for query rewriting and result synthesis. The model runs against Groq's hosted inference API rather than on operator hardware because the freshness workload is bursty and the marginal cost of Groq per-token is lower than reserving edge capacity for a workload with low duty cycle.
Freshness source: SerpAPI or equivalent as the external web search provider. The router sends only the rewritten query string, stripped of household context and member identity. The external provider sees a generic query that could have come from any user.
Query classes served: "What is the weather tomorrow?" "Is the pharmacy still open?" "What movies are playing tonight?" Live data queries where the answer is not in the household context graph and requires an external fetch.
Trust boundary treatment: The synthesis step, where the freshness result is combined with household context, runs on operator infrastructure inside the trust boundary. The external service never sees the synthesis input.
Fraction of queries expected: 10 to 20 percent of household queries in steady state.
2.4 Tier three: enclave (core)
The enclave tier handles complex queries requiring both a larger model and access to the full household context. These queries are too complex for the small edge model, too sensitive to leave the operator's infrastructure, and require reasoning across the context graph in ways the primary tier cannot handle.
Model of record: Groq Llama 3.3 70B, hosted inside the operator's confidential computing enclave. The 70B parameter class is the smallest that reliably handles evaluating and creating queries against household context with the quality bar a paying subscriber requires.
Enclave target hardware: NVIDIA RTX PRO 6000 Blackwell (96GB VRAM) or equivalent. Confidential computing mode enabled through NVIDIA CC and hardware attestation. Estimated throughput penalty for full LLM serving under confidential computing: 5 to 27 percent on Blackwell, per NVIDIA documentation and published benchmarks. The exact penalty depends on model architecture and batch shape.
Alternative frontier weights: Groq Llama 4 Scout FP4 via NIM as the confidential computing path for hub deployment. Llama 4 Scout FP4 is the current best-performing weight class that fits inside 96GB of VRAM with room for KV cache at production batch sizes.
Query classes served: "How should we handle Mom's medication schedule given the new insurance denial?" "What is the best way to reorganize the household budget after the roof estimate came in?" Cross-context reasoning, multi-step planning, care coordination, financial synthesis, any query touching sensitive household detail that exceeds the small model's capability.
Bloom coverage: Levels 4 through 6 (analyzing, evaluating, creating). Level 3 (applying) queries can also route here when the primary tier's confidence is low or when the context load exceeds the primary tier's working memory.
Fraction of queries expected: 5 to 15 percent of household queries in steady state. This is the tier that carries the platform's ability to do serious work on sensitive context.
2.5 Tier four: passthrough (frontier)
The passthrough tier handles queries the subscriber has explicitly directed to a frontier model on their own subscription. HIP is not the primary compute provider for these queries. It is the router that decides whether the subscriber's request is safe to pass through, strips the household context by default, announces the crossing, and lets the subscriber choose whether to override.
Model of record: None. The subscriber's connected frontier account determines the model. Common connections: Claude, ChatGPT, Gemini. HIP does not run the inference; it routes to the subscriber's account.
Default behavior: Household context is stripped from the query before it crosses the trust boundary. The frontier model sees only the subscriber's raw text input, no household context, no member identity, no fact graph references. The crossing is announced to the subscriber in the interface.
Subscriber override: The subscriber can, on a per-query basis, decide to send household context along with the query. This is an affirmative choice, not a default. The system records the choice, and the choice is scoped to the single query, not to the session.
Sensitivity gate: Even with subscriber override, sensitivity-gated content (medications, medical detail, minor-child data, financial account information) cannot be sent through the passthrough tier. The system refuses the crossing regardless of subscriber consent.
Fraction of queries expected: Under 5 percent in steady state. This tier exists because some subscribers want frontier reasoning on non-sensitive work. It is not a growth vector for the platform.
2.6 The routing classifier
The router itself is a small classifier that runs on the edge in front of every query. It is not the primary model, and it is not a language model in the general sense. It is a fast classification stage that emits three signals (freshness required, complexity level, sensitivity level) and a tier assignment.
Implementation of record: A small transformer classifier trained on labeled prototype queries, plus a rules layer that hard-codes sensitivity assignments for the ten canonical fact-attribute types. The rules layer runs first. If the rules layer flags the query as high sensitivity, no learned classifier decision can override.
Bloom mapping table: Level 1 (remember) and Level 2 (understand) map to primary tier. Level 3 (apply) maps to primary tier by default, mid or core if the confidence score is below threshold. Level 4 (analyze) and Level 5 (evaluate) map to enclave tier. Level 6 (create) maps to enclave tier or, with subscriber override and no sensitivity flags, to passthrough.
Session-end extraction: At session end, qwen2.5:32b, quantized, runs the extraction pass that turns the conversation into new fact assertions or updates to existing facts. This is a heavier model than the primary tier because the extraction task is more demanding than in-session response generation. It runs asynchronously and does not block the subscriber.
Async fact-change detection: Groq Llama 4 Scout runs continuously against the fact graph looking for temporal invalidation (a fact that was true is no longer true given new evidence). Target latency for detection: 0.5 seconds from evidence arrival to invalidation flag. Runs async, out of band.

3. Fact Schema and Lifecycle
3.1 The ten canonical attribute types
The context graph is not a free-form text store. It is a typed, attributed graph in which every fact is one of ten canonical attribute types. The types were selected to cover the household decisions HIP is built to serve while remaining tractable for the extraction and retrieval pipelines. Extending beyond ten requires an architecture change, not a data change.
1. medication. Prescription and over-the-counter medications for any household member. Includes dosage, schedule, prescribing provider, purpose, and start and end dates. High sensitivity by default.
2. allergy. Food, environmental, and drug allergies for any household member, with severity classification. High sensitivity.
3. health_condition. Chronic and acute conditions, with active or resolved status, provider references, and treatment notes. High sensitivity.
4. dietary. Restrictions, preferences, and requirements. Medium sensitivity. Elevated to high when tied to a health_condition.
5. preference. General household or member preferences. Low sensitivity unless tagged otherwise.
6. schedule. Recurring commitments (school, work, activities) and one-time appointments. Medium sensitivity. Elevated to high for minor children.
7. employer. Employer, role, and work-related context for adult household members. Medium sensitivity.
8. relationship. Family and social relationships, both within and outside the household. Medium sensitivity.
9. household. Household-scoped facts: address, routines, decisions the household has made, ongoing projects. Medium sensitivity.
10. financial. Budgets, spending patterns, account references (not credentials), major purchases, insurance context. High sensitivity.
3.2 Fact lifecycle
Every fact in the context graph moves through a defined lifecycle. The lifecycle is what allows HIP to remember without accumulating stale or contradictory data.
Assertion. A fact is added to the graph, either through session-end extraction or through explicit subscriber statement. Every assertion carries a source (which session, which member, which utterance), a confidence, and a timestamp.
Enrichment. Temporal boundaries are inferred where possible. Facts that reference a future event get an expiration. Facts that describe a state that changed at a known point in the past get a validity window. Enrichment runs asynchronously after assertion.
Retrieval. When a query needs a fact, retrieval respects the validity window. Facts outside their window are not returned unless the query explicitly asks about the past.
Invalidation. When new evidence contradicts a stored fact, the async fact-change detector (Groq Llama 4 Scout) flags the older fact and proposes an update or a retraction. The subscriber can review; unreviewed changes apply after a grace window.
Retraction. Facts can be explicitly retracted by the subscriber. Retraction preserves the historical fact for audit but removes it from active retrieval. Retraction is reversible.
Export and portability. The full fact graph, including retracted facts, is exportable by the subscriber at any time. The export format is canonical JSON with source attribution and timestamps. Portability is architectural, not a feature.

4. Confidential Computing and Enclave Design
4.1 Threat model
The enclave design defends against three classes of adversary. The first is a remote attacker who has compromised the operator's edge infrastructure at the OS or hypervisor level. The second is an internal actor at the operator with legitimate physical or logical access to the enclave hardware. The third is a legal or regulatory compulsion that demands access to plaintext household data.
For all three classes, the design goal is the same: the operator does not hold the plaintext household content, and does not hold the keys required to decrypt it, at any point after the household context has been sealed. The operator holds ciphertext, metadata, and audit logs.
4.2 Hardware target
Enclave hardware of record: NVIDIA RTX PRO 6000 Blackwell in confidential computing mode. Attestation via NVIDIA's remote attestation service. Encrypted memory paths from CPU to GPU across the PCIe bus. Verified boot chain from firmware through driver.
Server platform: Standard 2U server with AMD SEV-SNP or Intel TDX at the CPU level to encrypt the host memory that supplies the GPU. Combining GPU CC and CPU TEE is the current best available path for end-to-end plaintext isolation on commodity hardware.
Throughput penalty: Between 5 and 27 percent on Blackwell for full LLM serving depending on model architecture and batch shape. Prototype benchmarks fall in the 8 to 15 percent range for the workloads HIP runs. The penalty is priced into the unit economics.
Enclave workload: The tier three (core) model, Groq Llama 3.3 70B or Llama 4 Scout FP4 via NIM, runs entirely inside the enclave. The tier one (primary) model runs outside the enclave on the same hardware or on a separate edge node, because tier one workloads do not touch sensitive plaintext beyond what is already retrievable from the household's own context graph.
4.3 Key custody hierarchy
The key hierarchy defines who holds which key, where the key material is generated, and what happens on device loss.
Root key: Generated per household at first enrollment. Derived from voiceprints of enrolled members plus a hardware root of trust anchored in the secure element of the household gateway. The root key is never exported from a secure element.
Derived encryption keys: Per-fact-type and per-member subkeys are derived from the root key using HKDF. This lets retrieval decrypt only the subset of the graph relevant to a query, without exposing the rest.
Gateway anchor: The household gateway (existing modem or router) holds a copy of the root key in its secure element. The gateway participates in every key derivation for household-scoped queries.
Mobile anchor: Each enrolled member's phone secure element holds a member-scoped subkey. Mobility queries use the mobile anchor without needing to reach the gateway.
Recovery: Recovery is a separate authority from the root key, deliberately decoupled from training data authority. See section 5 on the five-layer platform architecture. The recovery path uses a threshold secret-sharing scheme across enrolled family members and a designated secondary custodian.
4.4 What the operator can and cannot see
An honest statement of what the operator holds is essential. Overstatement ("the operator sees nothing") is neither true nor credible.
Operator holds ciphertext of the fact graph. The operator's edge storage contains the encrypted context graph, indexed for retrieval but not readable without the household's key hierarchy.
Operator holds metadata. Query counts, tier hit rates, latency histograms, model call volumes, and error logs are visible to the operator for capacity planning and debugging. Metadata does not include query text or response text.
Operator holds audit logs. The audit trail of when the enclave decrypted content, which key was used, and which household member's session invoked the decryption is available to the operator. The audit log itself does not contain the plaintext.
Operator does not hold plaintext household content. Query text, response text, and fact content are decrypted only inside the enclave for the duration of processing and are not persisted in plaintext to any operator-accessible storage.
Operator does not hold the keys required to decrypt. Root keys and derived subkeys live in household-controlled secure elements. The operator cannot decrypt the ciphertext it stores even under legal compulsion.

5. Five-Layer Platform Architecture
The confidential platform is not a monolith. It is five distinct layers, each with its own authority model and its own operator relationship. The separation is architectural and it is deliberate: some authorities must never couple to others.
5.1 Layer 1: Encrypted context storage
The ciphertext store. Holds the encrypted fact graph, encrypted session traces (short retention), encrypted media (very short retention, ephemeral). The operator runs the storage, the household holds the keys. No inference happens at this layer.
5.2 Layer 2: Recovery authority
The recovery authority is the mechanism that allows a household to recover from device loss, member death, or gateway failure without giving the operator access to plaintext. Recovery uses a threshold scheme: a defined subset of enrolled family members plus a secondary custodian (designated at enrollment) can jointly reconstruct the root key material.
Critical isolation: Recovery authority MUST NOT couple to training authority. A recovery event unlocks the household's own context for the household. It does not unlock the context for use as training data by the operator or any partner. This isolation is enforced at the platform level and is inspected as part of any audit.
5.3 Layer 3: Consent and rights management
The layer that records what the household has consented to and enforces it at every downstream operation. Consent is per-fact-type, per-member, per-recipient. A consent to share medications with the household's care coordinator does not extend to the household's insurance company. Consent is revocable and revocation is enforced immediately at all layers above.
5.4 Layer 4: Derived intelligence
The inference layer. All four tiers of the cascade live here. Reads from the encrypted store (with the household's key), respects the consent layer, writes back new facts and updated facts as a side effect of inference.
5.5 Layer 5: Model training authority
The layer that governs whether household data can be used to train or fine-tune models. Explicit consent required per fact type per model. Consent is opt-in, not opt-out. Revocation removes the household's data from future training runs but does not retroactively remove influence from already-trained model weights (that is a fundamental limit of the current state of ML; disclosed at consent time).
Critical isolation: Training authority MUST NOT couple to recovery authority. A household member consenting to training does not authorize recovery. A recovery event does not create training rights. These are enforced by separate authorization surfaces with separate audit trails.

6. Identity and Member Model
HIP identifies household members by voiceprint. This is the identity mechanism at the primary interface (voice) and it is the anchor for the member-scoped subkeys in the key hierarchy. It is not the sole identity mechanism, but it is the one that carries the operational load.
6.1 Voiceprint enrollment
At enrollment, each household member records a short set of utterances. The enrolled voiceprint is stored as a set of speaker embeddings, encrypted under the household root key. Enrollment is done once per member and updated as needed.
6.2 Voiceprint accuracy in a household context
Voiceprint identification accuracy in a household of four to eight enrolled members, under normal acoustic conditions, is currently in the 90 to 99 percent range for clean voice and degrades meaningfully with children's voices and noisy environments. Voiceprint alone is not authentication-grade for high-value operations. It is identification-grade, sufficient for scoping which member's context a query touches.
Authentication-grade escalation: For operations requiring authentication (financial actions, medical account changes, sensitive content sharing) the platform escalates to a second factor. The second factor is device-bound (the member's enrolled phone or the household gateway) and is required in addition to voiceprint.
6.3 Shared vs. member-private context
Every fact in the context graph is scoped either to the household (shared) or to a specific member (private). Shared facts are readable by any authenticated household member. Private facts are readable only by the member the fact belongs to, and by the household's designated care coordinator role if that role has been consented for the fact type.
This scoping is enforced at retrieval, not at storage. All facts live in one graph. Retrieval respects the scoping and returns only the subset the querying member is authorized to see.

7. Deployment Topology
7.1 Reference topology of record
The architecture of record deploys entirely on operator edge infrastructure. No dedicated in-home hardware is required at launch. Every subscriber can begin using HIP the day the operator turns it on.
Primary tier: Runs on hub-class Blackwell edge nodes. Latency budget: sub-500ms end-to-end.
Freshness tier: Runs on Groq hosted inference. Query rewrite and result synthesis inside the operator boundary.
Enclave tier: Runs on confidential computing capable Blackwell hardware in the same or adjacent hub facility. Latency budget: sub-2s for complex queries.
Passthrough tier: Egress to subscriber-connected frontier accounts, over TLS, with context stripping enforced at the operator boundary.
7.2 Optional in-home hardware
An optional in-home CPE running a local primary tier model is available for operators who want it. It changes latency slightly (sub-300ms end-to-end for primary tier queries) and it changes the trust boundary shape (the household holds the primary tier compute in the home). It does not change the trust guarantee, because the guarantee depends on the key, not the location.
7.3 Reference bill of materials, hub-class node
A single hub-class node serves 2,000 to 5,000 household subscribers depending on query mix and enclave utilization. The BOM below is the current reference point; final specification is operator-specific and depends on facility power, cooling, and network profile.
GPU: 2 x NVIDIA RTX PRO 6000 Blackwell (96GB each). One dedicated to primary tier, one to enclave tier. Sticker price approximately $13,250 each at July 2026 MSRP. Total GPU: ~$26,500.
Server platform: 2U server, AMD EPYC or Intel Xeon Scalable, 512GB DDR5 ECC, dual 100GbE, redundant PSU. Server platform approximately $18,000.
Storage: 8TB NVMe for hot context, 32TB SATA SSD for warm context, network-attached tape or object storage for cold archive. Storage tier approximately $6,000.
Networking and edge: Included in hub facility. No incremental cost.
Confidential computing licensing: NVIDIA CC per-GPU license, quantity two. Approximately $2,500.
Total node hardware cost: Approximately $53,000 per node at July 2026 pricing.
Per-subscriber hardware cost (5,000-sub node): Approximately $10.60 per subscriber, before tax treatment.
Per-subscriber hardware cost, after-tax (bonus depreciation, 21% federal): Approximately $8.37 per subscriber. Additional state-conformity variance applies.

8. Prototype Validation Hooks
This section documents what has been validated on the working prototype, what is in progress, and what is scoped for the next validation cycle. The prototype runs on a Mac Mini M1 Pro ([REDACTED-USER]@[REDACTED-LAN-ADDRESS], Tailscale [REDACTED-TAILNET-ADDRESS], repo at ~/hip-harness). Voice server runs on port 7860 under launchd (com.hip.voice.orch). Public demos available via Tailscale Funnel.
8.1 Validated on the prototype
Bloom-based routing cascade: Working. Prototype instrumentation confirms routing decisions across primary, mid, and core tiers with the classifier described in section 2.6.
Intent classification: Working. Prototype classifies query intent as a precursor to Bloom-level assignment.
Fact lifecycle: Working end-to-end. Session-end extraction (qwen2.5:32b) writes to Neo4j via the extraction queue. Retrieval wired into system prompt through read_user_facts.
Temporal enrichment: Working. Facts receive validity windows on assertion.
Async fact-change detection: Working. Groq Llama 4 Scout runs the detection pass. Target 0.5s latency achieved on the prototype workload.
HIP-branded UI at /hip: Working. Subscriber-facing interface deployed on the harness.
Voice server on port 7860 via launchd: Working. Tailscale Funnel enables public demonstration URLs.
8.2 Known issues in scope for the current validation cycle
The prototype maintains a KNOWN_ISSUES.md file with tracked technical debt. Items in scope for the current validation cycle:
Echo cancellation: Under active work. Impacts voice quality on hardware with combined speaker and microphone.
Barge-in: Under active work. Impacts natural conversation flow.
Multi-member testing (M4-05, Tests 2 through 5): Requires a second enrolled voice. Scoping decision pending.
8.3 Prototype evidence dataset (in progress)
A dedicated Prototype Evidence document will accompany this annex when the current validation cycle completes. It will contain session traces, fact lifecycle examples, routing accuracy data against a labeled query set, Bloom classification agreement data, latency histograms per tier, and three demo vignettes (care coordination, freshness handoff, passthrough consent).

9. What Remains Under Additional Restriction
This annex is confidential. It goes only to counterparties under NDA. Even within the annex, three items are held for a further layer of restriction and are available only to counterparties who have advanced to a deeper diligence tier.
Vendor pricing detail. The specific negotiated pricing for Groq inference, NVIDIA CC licensing, and hosted infrastructure components is available under a supplementary agreement. Rate cards are shared, negotiated terms are not.
Operator-specific reference architectures. Reference architectures customized to Comcast, Charter, or a specific tier-two operator's infrastructure are available on a per-operator basis, executed under a separate memorandum.
Full financial detail. Complete storage and inference bills of materials, model call volume assumptions, and capacity planning at three subscriber scales live in the Financial Annex. This annex references the shape of the economics; the numbers live there.
