---
doc: HIP Interaction Layer Architecture and Roadmap
purpose: NDA section (sales). Systems design thinking, forward development plan, sovereign opportunity in the voice space, component-level alpha.
status: canonical source for NDA assembly
version: v20260710_1032
location: ~/hip-dev/docs/
audience: operator principals, strategic partners under NDA
constraints: no em or en dashes. Every claim must map to a real component or a stated R&D intent, never an implied shipped capability.
---

# The Interaction Layer: Architecture, Roadmap, and Sovereign Opportunity

## 1. The premise: the voice interface is unsettled, and HIP does not bet on which architecture wins

The market for real-time conversational AI is in open motion. In roughly two years it has moved through three distinct architectures, each solving a different problem and each leaving the next one exposed.

The first was the cascade: speech to text, then a text model, then text to speech. Three components chained in series. It proved you could hold a conversation with a frontier model at all, but it pays a latency tax at every handoff and discards everything that is not words, the timing, the intonation, the hesitation that carry half of conversational meaning.

The second was the turn-based audio-native model: a single model that consumes and produces audio directly, removing the service handoffs, but still gated by a decision about when the user has finished speaking. Faster and more natural, still fundamentally a walkie-talkie. One party talks, then the other.

The third, now emerging, is continuous full-duplex: the system models the user's speech and its own speech as concurrent streams and never stops listening while it talks. This is the architecture that finally feels like human conversation rather than radio protocol. It is also early, computationally heavy, weaker at deep reasoning than the text-centered stacks, and materially harder to audit.

No architecture has won. No open standard exists for coordinating the fast conversational loop with slower reasoning. And critically, no vendor has released a governed version of that coordination layer. The frontier labs expose capabilities through APIs and products; they do not expose the orchestration underneath, and they do not expose a control plane an operator could trust with a household.

This is the strategic fact that shapes HIP's entire posture in the voice space. The interaction layer is a moving target. Any company that builds its defensibility into a specific conversational architecture is building on ground that has shifted three times in two years and will shift again. HIP is built the opposite way. HIP treats the conversational model as a replaceable component and locates its defensibility in the layers that do not change when the interface does.

## 2. The layered architecture: what changes, what does not

HIP is a layered system. The layers are separated deliberately so that volatility is isolated to the top and durability accrues at the bottom. This separation is the architecture. It is what lets HIP absorb change at the interaction layer instead of being exposed to it.

**Layer 0: The interaction surface (volatile, replaceable by design).**
This is where speech enters and leaves: the microphone array, echo cancellation, the turn-taking or full-duplex model, the speech synthesis. This is the layer the entire industry is churning. HIP holds this layer at arm's length. It is an adapter, not a foundation. A cascade today, a fused semantic-prosodic turn model next, a full-duplex interaction model when the reasoning, governance, and edge-compute story matures. Each is a swap at Layer 0. None touches the layers below.

**Layer 1: The routing cascade (durable, and already built).**
HIP routes every request across a tiered inference hierarchy: a fast local edge tier, mid and core tiers for heavier reasoning, a frontier tier for the hardest work, and a bring-your-own-key passthrough. A complexity classifier decides where each request goes. This is not a future ambition. It is the operating structure of the current prototype.

The significance is this. The pattern the entire frontier is now converging on, a fast interaction model that handles conversational flow and delegates heavy reasoning to a larger background model, is the interaction-model-plus-reasoning-model split. HIP's routing cascade already implements that split. The fast local tier is the interaction model. The heavier tiers are the background reasoning model. HIP arrived at this structure through operator-cost discipline, not through chasing the voice frontier, and it means that when full-duplex interaction models mature, HIP does not need a new architecture to host them. The interaction model drops into the tier that already exists for it.

**Layer 2: Governed context organization (the moat).**
Beneath routing sits the per-member fact graph: a canonical, encrypted, temporally-enriched organization of household context, isolated per member, with trust boundaries enforced cryptographically. This layer is entirely independent of how speech enters or leaves the system. It does not care whether the interface is a cascade or full-duplex. Raw intelligence commoditizes; context compounds. The organized, governed, per-member context is the asset that grows more valuable over time and cannot be reconstructed by swapping in a better model.

**Layer 3: The deterministic control plane (the trust guarantee).**
Identity, consent, and policy are enforced in deterministic code around the probabilistic core, not inside the model. Per-member envelope encryption, speaker verification, and continuous rather than session-start permission checks live here. This is the same separation that compliance-grade systems require and that shipped frontier interaction systems describe, about the field in general, as non-negotiable: the guarantees come from the infrastructure and processes around the model, not from the model itself, because a probabilistic model cannot be relied on to enforce a hard constraint. HIP puts the constraints where they are testable and enforceable, and lets the model operate within them.

The relationship between these layers is the whole thesis. Layers 2 and 3 are model-agnostic. They carry over unchanged when Layer 0 is swapped. A cascade today and a full-duplex model in eighteen months are identical from the perspective of HIP's moat: the context graph, the routing hierarchy, and the control plane are untouched. The conversational model is a component. The governed system around it is not.

## 3. The alpha: where HIP holds an edge the frontier labs do not

The advantage is not that HIP will build a better full-duplex model than the frontier labs. It will not, and it does not need to. The alpha is in the components the frontier labs are structurally unable or unwilling to build, and in the way those components combine.

**Alpha 1: Governed multi-entity context at the household scale.**
The frontier labs build one model serving many isolated users. HIP builds a governed system serving one household of distinct members with distinct, cryptographically enforced boundaries and a shared context that respects them. This is the multi-entity governance problem, and it is the exact problem HIP's operator record was built solving at national scale. A household is a multi-entity governance problem wearing a domestic face: a parent, a child, an elder, each with different vocabulary, different permissions, different consent, sharing a context that must remain both coherent and separated. No frontier voice product is architected for this. Their unit is the user. HIP's unit is the governed household.

**Alpha 2: The interaction-plus-reasoning split, already operational and cost-disciplined.**
The frontier labs are publishing the fast-loop-plus-background-model pattern now as a research direction. HIP is already running it, because it fell out of operator token-cost discipline. HIP's native language is unit cost per token, and the routing cascade exists precisely to spend heavy compute only when a request earns it. This means HIP's version of the split is not a latency trick bolted on for voice; it is a cost-and-governance architecture that the voice frontier happens to have arrived at from the other direction.

**Alpha 3: The governed interaction operating system, which no one has released.**
There is a clean whitespace here, and it is worth naming precisely. Open research has produced the fast interaction model (the conversational loop) and the asynchronous reasoning backend (retrieval, tools, planning). What no one has released, open or closed, is the coordinating layer on top: the governed interaction operating system that adds interrupt logic, waiting and deferral, confidence thresholds, state management, and, above all, continuous permission-awareness across the whole exchange. The frontier labs expose the pieces. They do not expose a control layer an operator could trust with a family's data. HIP's control plane and routing cascade are the beginnings of exactly that layer. This is the component-level alpha with the longest runway.

**Alpha 4: The trust architecture as a structural, not cosmetic, difference.**
Two systems can hold the same household data and be opposites in trust design. One organizes that data for the platform's benefit and treats the user as the product. HIP organizes it under an operator-custodial model where the member holds the keys and enforcement is continuous and cryptographic. Same data asset, opposite trust architecture. For a sovereign or operator context, that difference is the entire proposition.

## 4. The sovereign opportunity in the voice space

The interaction layer is where sovereignty is won or lost, because it is the layer closest to the person. The words spoken in a home, to a household assistant, are the most intimate data an AI system will ever touch: medical, financial, familial, developmental. A sovereign systems opportunity exists precisely because the frontier products route that data to a datacenter and enforce trust nowhere the operator can inspect.

HIP's architecture is a sovereign systems architecture by construction. Storage sits at the operator edge. The deployment model is left open for optionality, so the same system can run in configurations that keep data inside a sovereign boundary. The routing cascade means the interaction and most reasoning happen locally, with only the hardest requests optionally escalating, and even that escalation is a policy decision the control plane governs rather than a default the platform imposes. The operator positioning triad holds: no datacenter, no rate increase, no water. A household-scale interaction system that runs at the operator edge, keeps context sovereign, and enforces trust in inspectable code is a category the frontier labs are not positioned to offer, because their business is the datacenter and the aggregated user.

This is the roadmap's north star. As the interaction layer matures toward full-duplex, HIP's value is not that it will have the best voice. It is that it will be the only voice a sovereign operator can deploy without surrendering the household's context and trust to a third party. The interaction model improves and commoditizes on someone else's research budget. The governed, sovereign, edge-resident system around it is what HIP owns.

## 5. The development path: modular adaptation as the operating principle

The roadmap is built on one principle: keep the interaction surface modular so the durable layers never have to move. Concretely, HIP develops along a bounded, staged path rather than betting the architecture on a single interface generation.

The near-term work hardens the interaction surface within the current cascade, specifically by replacing brittle silence-based endpointing with fused semantic and prosodic turn prediction, a bounded and edge-viable upgrade that makes the current system feel conversational without touching the layers below. The medium-term work formalizes the interaction-and-reasoning split that the routing cascade already embodies, tightening the delegation boundary, the gap-filling behavior, and the point at which the control plane intercepts. The longer-term work is the governed interaction operating system itself: the coordinating, permission-aware layer that is the standing whitespace, developed as HIP's own component rather than adopted from a frontier that has not built it. And throughout, the interaction model at Layer 0 remains a swappable adapter, so that whatever the frontier ships next, cascade, turn-based, or full-duplex, HIP integrates it as a component and preserves everything below it unchanged.

This is what modular adaptation means in practice. HIP does not predict the winning interface. It builds so that the winning interface, whenever it arrives and whoever builds it, plugs into a governed household system that was already right. The research is live and ongoing because the space is fast-moving; the architecture is designed to absorb that motion rather than be overtaken by it. The components are real, operating in the current prototype at Layers 1 through 3, and the forward work is the disciplined extension of components that exist, not the invention of ones that do not.
