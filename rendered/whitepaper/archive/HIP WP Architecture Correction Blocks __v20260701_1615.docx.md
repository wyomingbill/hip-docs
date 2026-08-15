HIP White Paper: Architecture Correction Blocks

Purpose: these four blocks bring the white paper into line with the locked architecture (edge-cloud base case, no home hardware at launch, one key hierarchy across gateway and phone, attested enclaves not FHE, dedicated CPE optional). Paste each into the master HIP_White_Paper. Block 1 replaces the Executive Summary placeholder. Block 2 replaces the inference cascade section in Part I. Block 3 is a new subsection added to Part I after the cascade. Block 4 replaces the Diagram 1 caption.

No em dashes or en dashes anywhere. Declarative, operator voice.

====================================================================
BLOCK 1. EXECUTIVE SUMMARY (replaces the "to be written last" placeholder)
====================================================================

The most consequential conversations in a person's life happen at home, across a household, over time. No AI system on the market is built for them. Every frontier assistant models a single user, on the provider's servers, under the provider's terms. HIP models the household.

The Household Intelligence Platform is a private, persistent intelligence layer that remembers and connects context across a family over months and years. It identifies who is speaking. It holds the boundary between what the household shares and what an individual keeps private. It runs on cable operator edge infrastructure, under an encryption key the household controls, on hardware the operator runs but cannot read.

The architecture is settled and it is honest about where it runs. Context is managed and inference runs in the secure edge cloud on operator infrastructure. No in-home model and no dedicated home hardware are required at launch. The household holds the key across one key hierarchy: the home anchor is the existing modem or router secure element, so the assistant works when a phone is away or asleep, and the member's phone secure element carries the same hierarchy for mobility, so context travels with the person. Operator-blind computation runs in attested confidential-computing enclaves, not fully homomorphic encryption. The operator cannot read enclave content, though it sees metadata, timing, and sizes. A dedicated in-home device with a local model is a preserved optional upgrade, never the base case.

The defensible asset is not the model and not the routing. Both commoditize. The asset is the organized household context that compounds over time under a key the household controls, and the trust boundary that makes the highest-value use cases, health, finances, eldercare, children, possible at all. A competitor can match the technology in an afternoon and cannot match a year of a family's accumulated understanding at any price.

Every major force now reshaping the AI market makes that asset more valuable. Intelligence is commoditizing, which pushes value off the model and onto the context layer. Owning contested compute is getting more expensive, which rewards the platform that needs the least of it and already owns secured, powered facilities. The physics of where compute can live points at the secured edge close to the home. Cable already owns that edge, in the thousands of facilities, and has begun deploying inference into it with NVIDIA. And a care crisis, a datacenter backlash, a privacy reawakening, and a collapse in institutional trust are converging on the household at the same moment, each favoring a private, household-scoped, low-footprint platform held under a consumer key.

The position is real and undefended. The operator holds the ground by default, not by intent, and the context has not yet been claimed. Because the moat is accumulated context and context compounds only with time, it goes to the earliest credible mover, not the best technology. The window is open because no one has started. It closes the moment someone does.

This document makes the full case: what HIP is, why it is defensible, why the largest forces in the market favor it, why cable is uniquely positioned to deliver it, what the economics look like, and why the window to build it is open now and will not stay open.

====================================================================
BLOCK 2. THE INFERENCE CASCADE (replaces the cascade section in Part I, from "HIP routes across tiers" through the "deployment model is deliberately open" paragraph)
====================================================================

HIP routes across tiers, each with a distinct cost profile and a distinct privacy guarantee.

[DIAGRAM 1 PLACEMENT stays here]

The primary tier answers from household context in the secure edge cloud. A small model running on operator-controlled edge infrastructure responds to the majority of household interactions directly from the context graph. What time is practice. What did we decide about the holiday. When was the last refill. These require no external model and no external cost, and nothing leaves the trust boundary. This is where most interactions live and where the cost advantage is largest. The context is decrypted only inside an attested enclave under the household's key. The operator runs the machine and cannot read its contents.

A freshness tier fetches current information. When a query needs live data, the weather, a score, a current rate, the system sends only the search string. It never sends household context or identity. The web sees a generic query. The result returns and is synthesized inside the boundary against the household's context. The outside world never learns who asked or why.

An enclave tier handles complex reasoning. Some queries need a larger, more capable model. That model runs inside a confidential computing enclave on the operator's edge infrastructure, hardware-secured so that the operator cannot read the data even with physical access to the server. Encrypted in, encrypted during processing, encrypted out. The operator provides the building. The household holds the key.

A passthrough tier reaches the frontier. When a subscriber explicitly wants a frontier model, their own, on their own subscription, HIP routes the query out, but strips every trace of household context first. The frontier model sees only what the subscriber typed. The platform announces the crossing, so the choice to leave the boundary is always visible and always the subscriber's.

The base case requires no home hardware. Context is managed and inference runs in the secure edge cloud on operator infrastructure. There is no in-home model and no dedicated home appliance at launch. The routing architecture and the privacy guarantee do not depend on an in-home device. A dedicated in-home device with a local model is a preserved optional upgrade for operators who later want on-device inference or a stronger home anchor, modeled as a labeled scenario, never the base case. The platform adapts to that upgrade without rearchitecting the trust model, because the trust model is anchored in the household key hierarchy, not in where the compute sits.

====================================================================
BLOCK 3. NEW SUBSECTION FOR PART I: "How the household holds the key" (insert after Block 2, before "Why this architecture now")
====================================================================

How the household holds the key

The privacy guarantee rests on two mechanisms that an operator's engineers will examine first: how the household holds the key, and how the operator computes on data it cannot read. Both use standard, shipping practice rather than a research bet.

The household holds the key across one key hierarchy, not by syncing a key between devices. There is one household master key. It never exists in plaintext outside a secure element or an attested enclave at the moment of use, and it is never copied between devices in the clear. Each device holds only a credential that lets it independently authorize the edge enclave. At home, the modem or router secure element is the anchor. It holds household key material and can release it to the edge enclave, so the assistant works when the phone is in another room, asleep, or dead. Away from home, the member's phone secure element holds a member key in the same hierarchy and authorizes the enclave on its own, so context travels with the member. A lost phone is revoked by removing its member key from the hierarchy without touching the master. This is the same envelope-encryption and key-hierarchy pattern that cloud key-management systems and multi-device passkeys already use.

Operator-blind computation uses attested confidential-computing enclaves, not fully homomorphic encryption. Computing on ciphertext without decrypting it is not practical for language-model inference at acceptable latency today. HIP does not propose it. Instead, the household key is released into an attested enclave at the edge, the enclave proves it is genuine and unmodified before receiving the key, context is decrypted and inference runs only inside the enclave, and the result returns to the household. The operator, running the machine, cannot read enclave content. The claim is precise and defensible: the operator still sees metadata, timing, sizes, and routing, and cannot read the content of an attested workload.

The primitives here already ship in production. Edge-cloud inference on operator infrastructure is being deployed by Comcast and Charter with NVIDIA. Hardware-held keys in a secure element ship on billions of phones for Apple Pay, Google Wallet, and passkeys. Confidential computing ships as Intel TDX, AMD SEV-SNP, and NVIDIA confidential compute on current GPUs. Envelope encryption and key hierarchies are standard cloud practice. What is new is the assembly of these primitives into a household-scoped configuration at operator scale. That is integration, which is what real platforms do, not invention, which is a bet.

The honest open problems belong in the record. If a household has no capable home anchor and relies on the phone alone, the assistant needs the phone present and awake to authorize the enclave. The mitigations are short-lived delegated session credentials, a cached authorization window, and the home anchor itself. Not every deployed gateway has a secure element strong enough to hold key material and perform attested key release. On capable gateways this works today, and on older ones the fallback is phone-only custody or the normal gateway refresh cycle. Sharing household context across members while preventing one member from silently surveilling another requires per-member keys and an authorization model inside the hierarchy, which the design supports and which is real implementation work. Edge confidential compute is the newest of the four primitives, and its performance, attestation tooling, and cost per query need measurement on the target edge hardware before scale claims are made. Naming these is what makes the rest credible.

====================================================================
BLOCK 4. DIAGRAM 1 CAPTION (replaces the existing Diagram 1 caption)
====================================================================

Diagram 1: The Inference Cascade. A router dispatches each query to one of four tiers based on sensitivity and need. Primary (household context in the secure edge cloud), Freshness (web, stripped query only), and Enclave (confidential compute) all run inside the operator and household trust boundary. Passthrough (the subscriber's own frontier model, context stripped) crosses the boundary explicitly. Every tier runs on operator edge infrastructure. No home hardware is required at launch. The household holds the encryption key across one hierarchy, anchored in the existing gateway secure element at home and carried in the member's phone for mobility.

