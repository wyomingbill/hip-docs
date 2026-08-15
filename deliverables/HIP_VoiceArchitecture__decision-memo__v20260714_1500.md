# HIP Voice Architecture -- Decision Memo

Status: BUILT
Version: v20260714_1500 MT
Prepared-By: Claude (Sonnet 4.6)
Reconciled-Against: voice-research P1-P8 (v20260709-v20260710); HIP_Voice_Development_Spec__v20260710_1530; harness/realtime_adapter.py (BUILD-1 fbcd372)
Audience: Technical counterparty under NDA. This memo documents HIP's voice-stack architecture direction and vendor reasoning. It is honest about what is decided versus direction-set-pending-test.

Decision status key used throughout:
- DECIDED: architectural choice locked; rationale is stable regardless of test outcome
- DIRECTION: vendor or technology selected pending Bill's live LiveKit integration test; may be confirmed or revised by test result
- OPEN: requires additional data, negotiation, or Bill's input before closing

---

## 1. The Requirement: Trust Boundary and Multi-Operator Embed

### The non-negotiable axis

Household audio must not leave the operator's trust boundary. This is not a preference -- it is the architecture's load-bearing claim. HIP's governance layer (the injection contract, the epistemic record, member-scoped encryption) protects fact values inside the operator cloud. If audio travels to an external STT provider, the acoustic signal -- which may carry personally identifying voice patterns, medication names, caregiver instructions, and sensitive household information -- transits a path that HIP does not control, does not encrypt under member-scoped keys, and cannot audit. The governance record has no entry point for a sentence that leaves as audio and comes back as text from a third-party endpoint.

The trust boundary requirement has a second axis that is equally binding for commercial deployment: the voice stack must be embeddable and redistributable across many operator clouds. HIP is not a single-tenant SaaS product; it is a platform that deploys per-operator. A voice stack that requires an enterprise license with per-capacity billing, a license server that phones home, or per-operator renegotiation of redistribution rights is not deployable at the operator scale HIP is targeting. Apache-2.0 or functionally equivalent permissive licensing is the only commercial path that permits embed-once-deploy-everywhere.

Every vendor in this memo is scored against both axes: **in-boundary** (audio stays in the operator cloud) and **multi-operator-embed** (licensing permits redistribution without per-operator commercial renegotiation).

### What "in-boundary" means in practice

In-boundary does not mean on-device or on-premise. It means: the audio pipeline runs within the operator's cloud perimeter, under the operator's infrastructure control, without audio crossing to a third-party processing endpoint. STT inference running on a self-hosted model in the operator's Kubernetes cluster is in-boundary. STT inference calling Deepgram's hosted API is not, even if the connection is TLS-encrypted.

Self-hosted STT and TTS models are in-boundary by definition. The commercial question is whether the vendor's license for a self-hosted deployment permits multi-tenant redistribution across many operators by one platform vendor (HIP).

---

## 2. The Architecture: LiveKit Frame + HIP Brain + Swappable STT/TTS

### Overall design (DIRECTION -- pending Bill's live LiveKit test)

HIP adopts a cascaded voice architecture: speech-to-text to text checkpoint to text-to-speech. The cascade is not a compromise forced by the current state of the art; it is a requirement driven by the governance architecture (see Section 3). The text checkpoint between ear and mouth is where the injection contract, the disclosure gates, and the epistemic record live.

The three layers are structurally separate and the contracts between them are stable:

```
HOUSEHOLD AUDIO (microphone array, operator edge)
        |
        v
   LiveKit SFU / media server
   (WebRTC transport, room session management, mixing)
        |
        v
   STT plugin -- self-hosted in operator cloud
   (Whisper / Deepgram self-hosted / Fish-Speech or equivalent)
        |
        v
   ====== TEXT CHECKPOINT ==============================
   |  assemble_governed_context()                      |
   |  -- resolve member from voiceprint session        |
   |  -- injection contract (INJ-1..7)                 |
   |  -- decrypt admitted facts (Fernet/HKDF-SHA256)  |
   |  -- run edge LLM (qwen2.5:7b or equivalent)      |
   |  -- emit_epistemic_record() -> turns_demo.jsonl   |
   |  -- park / confirm / guard events                 |
   =====================================================
        |
        v
   TTS plugin -- self-hosted in operator cloud
   (Deepgram Aura-2 self-hosted / Coqui / Kokoro or equivalent)
        |
        v
   LiveKit SFU
   (audio back to household speaker)
        |
        v
   HOUSEHOLD SPEAKER
```

**LiveKit (DIRECTION)** is the voice-infrastructure frame: the WebRTC SFU, room/session management, participant events, media routing, and turn-detection hooks. It is open-source under Apache-2.0. HIP does not adopt LiveKit's AI agent SDK (which embeds STT/TTS/LLM as a bundled pipeline) -- it uses LiveKit as a transport and signaling layer only, plugging HIP's own governed-LLM reasoning into the text checkpoint.

**HIP (DECIDED)** is the reasoning and governance layer. It receives text from the STT plugin, runs assemble_governed_context() under the injection contract, calls the edge model, emits the epistemic record, and returns text to the TTS plugin. This layer is identical to the typed-query path that BUILD-1 (fbcd372) delivered. The voice path and the typed path share the same governance enforcement. There is no voice-specific disclosure logic.

**STT and TTS (DIRECTION)** are swappable plugins. The text checkpoint's API contract is fixed; the STT and TTS implementations behind it can be substituted without touching the governance layer. This is the architectural invariant that makes the vendor analysis in Section 4 about cost, quality, and licensing rather than about lock-in.

### Harness current state

`harness/realtime_adapter.py` (BUILD-1, fbcd372) wires the live voice path through assemble_governed_context() and the injection contract at the text checkpoint. It uses OpenAI's Realtime API (GPT-Realtime-2.1-mini) as the current live integration. The LiveKit frame replaces the OpenAI Realtime transport layer without changing the text checkpoint; the governance enforcement is transport-agnostic. VOICE-GOV-001..004 conformance suite ratcheted PASS.

---

## 3. The Governance Rationale: Why the Cascade Is a Requirement

### The sharp point

The STT-to-text-to-TTS cascade is not a limitation of HIP's voice architecture. It is the requirement. Removing the text checkpoint would destroy the governance layer.

**Full-duplex speech-to-speech models (Moshi/Kyutai, OpenAI GPT-4o audio, Gemini Live) have no text checkpoint.** They operate on continuous audio frame sequences -- typically 80 ms codec frames (Moshi) or 50 ms audio tokens (OpenAI) -- producing audio output without an intermediate textual representation that the injection contract can inspect. The model's context window at inference time contains audio tokens, not text tokens. There is no surface where "the injection contract checks this fact before it is spoken" is implementable.

This is not a technical limitation that will be resolved by better engineering. It is structural. A full-duplex system that produces output audio from input audio does not pass through a text representation by design. The text checkpoint does not exist to remove.

### "You cannot audit what has no text"

The epistemic record (d1.1 schema) logs: which facts were admitted, which were withheld and why, which guard fired, what the model was given. It logs at the text checkpoint. If a fact value is spoken by a TTS engine rather than appearing in a text reply, the d1.1 record captures it. If a fact value is spoken directly from an audio-native model's output codec stream, there is no injection pipeline and no d1.1 record -- there is only the audio waveform.

The governance proof (HIP_GovernanceProof__audited-transcript__v20260714_1345.md) demonstrates in R06 and R07 that the disclosure decision is made before the model is called, or without calling the model at all. That is only possible because the text checkpoint interposes between the STT output and the LLM input. A full-duplex model receives audio and produces audio in a single end-to-end pass; the interposition point does not exist.

### Why this is a differentiator, not a compromise

The cascade adds latency relative to a full-duplex system. For a well-tuned cascade the research corpus gives a first-audio target of 700-1,600 ms; full-duplex systems achieve 150-400 ms for the interaction acknowledgment (P7 latency model). The cascade pays roughly 400-800 ms in additional latency for the text checkpoint.

That 400-800 ms buys:

1. **Auditable disclosure.** Every fact that reaches the speaker was admitted through the injection contract. Every withheld fact has a logged deny reason. A counterparty evaluating HIP's governance claim can trace any spoken fact to its fact_id and confirm the trust rung and the injection path. This is not possible with a full-duplex audio model.

2. **Guard interposition without model cost.** R06 shows INJ-6b firing in 56 ms with inference_ms=null. The empty-set guard returns a canned refusal before the model is called. A full-duplex model processes every audio frame continuously; there is no "do not call the model" path.

3. **Member-scoped decryption at the checkpoint.** Fact values are stored encrypted under per-member HKDF-SHA256-derived keys. Decryption happens at the text checkpoint, inside the governed context assembly, under the injection contract. The decrypted value reaches the model as text and the model produces text; the TTS engine receives the text output, not the raw fact database. A full-duplex audio pipeline has no equivalent decryption checkpoint.

4. **Transport-neutral LLM.** The edge LLM (qwen2.5:7b, or a future replacement) is a text model. Text models at the 7B class are well-supported on operator-grade GPU hardware, quantizable to Q4-Q8, replaceable without changing the governance layer, and priced at near-zero per token for self-hosted deployments. Audio-native models at comparable capability require significantly more compute per session-minute and cannot yet be substituted freely (P7 cost model: continuously active large full-duplex model ~$0.096/minute vs. cascaded ~$0.013-0.026/minute).

**The position to a technical counterparty:** HIP chose the cascade because governance requires a text checkpoint, not because full-duplex is unavailable. Any operator deploying HIP on Moshi or GPT-4o audio would get lower latency and no auditable disclosure. That trade is not available under HIP's governance model.

---

## 4. Vendor Landscape

Scored on five axes:
- **In-boundary:** audio (for STT/TTS) or session data stays in operator cloud; no audio to third-party endpoints
- **Multi-operator-embed:** license permits embed-and-redistribute across many operator deployments by one platform vendor without per-operator commercial renegotiation
- **Eldercare endpointing:** handles natural pauses, slower speech rate, sentence-final hesitations common in older adult speech without premature cutoff
- **Cost (self-hosted):** unit economics for in-boundary self-hosted deployment, per conversation-minute
- **Voice quality:** naturalness, latency to first audio, and (for TTS) speaker fidelity

---

### LiveKit (Voice Infrastructure Frame)

**Role:** WebRTC SFU, room/session management, participant events, media routing, turn-detection hook. Not the STT or TTS -- the transport and signaling layer.

**In-boundary:** YES -- self-hosted in operator cloud. LiveKit's SFU (the open-source server) runs inside the operator's infrastructure. No audio leaves to LiveKit's servers unless the operator uses LiveKit Cloud, which HIP would not use.

**Multi-operator-embed:** YES (with one flag). LiveKit core server and client SDKs are Apache-2.0. Embed-and-redistribute across operator deployments is permitted. **Flag:** LiveKit's turn-detection models (which ship with the Agent SDK, not the core SFU) are licensed under a separate "LiveKit Model License" that is not Apache-2.0. HIP needs to verify: (a) whether the turn-detection models are required for the integration, or whether HIP's own VAD/endpointing logic can substitute; and (b) if the LiveKit Model License permits multi-operator redistribution. This is a pre-integration due-diligence item, not a blocking issue. The core SFU is clean.

**Eldercare endpointing:** DEPENDENT ON PLUGIN -- the SFU layer is transport-only; endpointing is handled at the STT plugin or a VAD layer above it. LiveKit's turn-detection models (if used) need license verification first. HIP can substitute its own silence-threshold VAD without using the LiveKit models.

**Cost:** Open-source core, self-hosted. The SFU itself has no per-minute cost; infrastructure cost is the compute required to run WebRTC sessions. At operator scale, WebRTC SFU is CPU-bound (media processing, STUN/TURN relay) rather than GPU-bound; costs are low per session-minute.

**Voice quality:** Not applicable -- LiveKit is transport, not audio processing.

**Status: DIRECTION.** The LiveKit choice is pending Bill's live integration test. The architecture is designed so that if LiveKit does not perform as expected, the WebRTC transport layer can be substituted (Mediasoup, Janus, Jitsi Videobridge are all Apache-2.0 or MIT alternatives) without touching the text checkpoint or the governance layer.

---

### Deepgram (Self-Hosted STT and TTS)

**Role:** STT plugin (Deepgram Nova-3 / Flux self-hosted); TTS plugin (Deepgram Aura-2 self-hosted).

**In-boundary:** CONDITIONAL. Deepgram offers on-premise deployment. Audio stays in the operator cloud when using the on-premise model. However, Deepgram's on-premise license is a separate enterprise tier from its hosted API.

**Multi-operator-embed:** UNCERTAIN -- NEEDS CLARIFICATION. Deepgram's on-premise license is per-capacity (typically per core or per instance). A platform vendor (HIP) that deploys Deepgram on-premise across many operator clouds is likely redeploying the license, which generally requires either: (a) an OEM/redistribution agreement with Deepgram, or (b) per-operator Deepgram licensing that each operator holds independently. Neither is Apache-2.0 embed-and-redistribute. The specific risk: if HIP packages Deepgram as part of its platform and deploys it on operator infrastructure, Deepgram may treat that as redistribution requiring an OEM agreement. This is a known seam in enterprise self-host licenses. **Requires direct Deepgram conversation on OEM/redistribution terms before committing.**

**Eldercare endpointing:** STRONG. Deepgram's utterance_end_ms and endpointing parameters are well-documented and tunable. Nova-3 has strong accuracy on accented and older-adult speech in published benchmarks. Tuning the silence threshold to 600-800 ms (vs. the default 300-500 ms) handles natural pauses in older adult speech without premature cutoff. This is a configuration parameter, not a model change.

**Cost (self-hosted, per minute):** At hosted API rates (not on-premise pricing, which is contract-specific): STT ~$0.0065/audio-minute; TTS Aura-2 ~$0.030/1,000 characters. P7 cost model: ~$0.013-0.020/conversation-minute for the full cascade. On-premise cost is server-side amortized over sessions; for an operator running at scale, on-premise is significantly cheaper than hosted API per-minute rates.

**Voice quality:** STT accuracy is strong (Nova-3 / Flux). Aura-2 TTS is clear and natural, suitable for eldercare use cases. Not at ElevenLabs-level expressiveness, but appropriate for an assistant voice.

**Status: DIRECTION (conditional on OEM/redistribution clarification).** Deepgram is the current working assumption for the self-hosted in-boundary STT/TTS plugin. The multi-operator-embed licensing question must be resolved before committing.

---

### ElevenLabs (Premium / Branded Voice Tier)

**Role:** Optional premium TTS layer for operators or households that want higher expressiveness or a branded voice. Not the governed-core stack.

**In-boundary:** NO -- hosted-only. ElevenLabs does not offer a self-hostable or on-premise deployment. Audio (or text, for TTS) leaves the operator cloud to ElevenLabs' servers. This disqualifies ElevenLabs from the in-boundary governed core.

**Multi-operator-embed:** NOT APPLICABLE for the core. For the optional premium tier, ElevenLabs can be integrated per-household as an API call; no redistribution of the model is required, so the licensing question is simpler. Operators would hold their own ElevenLabs API keys or HIP would act as an API reseller.

**Eldercare endpointing:** N/A -- TTS only (text in, audio out). Quality for eldercare TTS: EXCELLENT. ElevenLabs' expressiveness, pacing, and voice clarity are the highest of any commercially available TTS. Their licensed-voice marketplace also permits named-voice licensing (e.g., a caregiver or family member's voice for a household's personal TTS profile), which is a differentiated eldercare use case.

**Cost:** ~$0.050/1,000 characters (Flash). P7 cost model: ~$0.015-0.026/conversation-minute for TTS alone. Premium tier above the governed-core cost.

**Voice quality:** BEST IN CLASS for expressiveness. The gap vs. Deepgram Aura-2 is meaningful for long-form conversational responses; for short assistant replies it is smaller.

**Recommended role: Optional per-household opt-in premium TTS tier.** Household pays for ElevenLabs expressiveness; audio transits ElevenLabs under household consent and disclosure. This is a separate billing tier above the governed core, not part of the default in-boundary stack. The household's consent to audio leaving the trust boundary for premium voice quality is an explicit product decision, not a governance architecture choice.

**Status: DIRECTION (premium-tier design, not core).** ElevenLabs is explicitly excluded from the in-boundary governed core. Its role as a premium opt-in tier requires Bill's decision on product structure and pricing.

---

### AssemblyAI (Hosted STT)

**Role:** STT alternative to Deepgram.

**In-boundary:** NO -- hosted API only. AssemblyAI does not offer self-hosted or on-premise deployment. Audio leaves the operator cloud for every transcription request.

**Multi-operator-embed:** NOT APPLICABLE -- no on-premise option to embed.

**Eldercare endpointing:** STRONG accuracy on real-world speech in published benchmarks; word error rate is competitive with Deepgram Nova. Endpointing is configurable.

**Cost:** Similar to Deepgram hosted rates.

**Assessment: EXCLUDED from the in-boundary governed core for the same reason as ElevenLabs -- no self-hosted deployment path.** AssemblyAI would be a reasonable STT choice in a trust-boundary-optional architecture; it is not available for HIP's in-boundary requirement.

---

### Cartesia (Self-Hostable TTS)

**Role:** TTS plugin alternative.

**In-boundary:** CONDITIONAL. Cartesia offers a self-hosted / private deployment option.

**Multi-operator-embed:** UNCERTAIN. Cartesia's self-hosted license terms are not publicly detailed at the level needed to confirm multi-operator redistribution. Requires the same OEM/redistribution due-diligence as Deepgram.

**Eldercare endpointing:** N/A -- TTS only.

**Cost:** Cartesia Sonic's SSM (state-space model) architecture produces first-audio in ~55 ms (published); faster than Aura-2 on a per-request basis. Self-hosted infrastructure cost is GPU-dependent; SSM models are memory-efficient.

**Voice quality:** Strong for latency-sensitive use cases. Slightly less expressive than ElevenLabs; comparable to Deepgram Aura-2. Cartesia's SSM architecture is better suited to very low-latency applications than transformer-based TTS.

**Status: DIRECTION (backup TTS option).** Cartesia is a credible alternative to Deepgram Aura-2 as the self-hosted TTS plugin, particularly if latency is the primary concern. License due-diligence required before committing.

---

### Open-Source Stack (Whisper / Fish-Speech / Kokoro / Coqui / Moshi -- No License Friction)

**Role:** Full in-boundary, no-license-friction STT and TTS.

**In-boundary:** YES -- self-hosted by definition.

**Multi-operator-embed:** YES. Whisper is MIT. Fish-Speech is Apache-2.0 (weights) or CC-BY-4.0 (depending on variant). Kokoro is Apache-2.0. Coqui XTTS-v2 is CPML (non-commercial restriction -- verify before use). Moshi is CC-BY-4.0 (weights). MIT and Apache-2.0 are freely embeddable and redistributable without commercial renegotiation.

**Eldercare endpointing:** VARIABLE. Whisper (large-v3 or turbo) has strong transcription accuracy including for older adult speech; its endpointing behavior requires a VAD wrapper (Silero or similar) for real-time use because Whisper was designed for batch transcription. Streaming Whisper integrations (faster-whisper, WhisperLive) add real-time capability at the cost of increased complexity. Fish-Speech and Kokoro have strong TTS quality for self-hosted options; neither has been evaluated specifically for eldercare pacing.

**Cost:** Self-hosted infrastructure only. No per-minute API cost. For a GPU-accelerated deployment, Whisper large-v3 turbo runs at roughly 15-20x real-time on an A10G, meaning one GPU can handle many concurrent sessions. Kokoro / Fish-Speech TTS is similarly GPU-efficient.

**Voice quality:** Whisper transcription accuracy is competitive with commercial STT on clean speech; it degrades more under heavy background noise. Open-source TTS (Kokoro, Fish-Speech, Coqui) is approaching commercial quality for clear assistant voices; it is not yet at ElevenLabs expressiveness.

**Status: VALID FALLBACK for the governed core; no license friction.** If Deepgram's OEM/redistribution terms do not support multi-operator embed, the open-source stack (Whisper + Kokoro) is the no-negotiation in-boundary alternative. HIP should test the open-source stack as a parallel path during Bill's LiveKit integration work.

---

### Moshi / Kyutai (Full-Duplex Speech-to-Speech)

**Role considered:** Real-time voice model.

**In-boundary:** YES -- CC-BY-4.0 weights, self-hostable.

**Multi-operator-embed:** CONDITIONAL. CC-BY-4.0 requires attribution; commercial redistribution is permitted with attribution. No per-operator renegotiation required.

**Assessment: ARCHITECTURALLY EXCLUDED.** Moshi has no text checkpoint. As detailed in Section 3, a full-duplex speech-to-speech model is structurally incompatible with HIP's disclosure governance. Moshi cannot be used as the reasoning layer, only as a component in a hybrid where its output is intercepted and re-governed -- which defeats its latency advantage and creates an audit gap at the intercept point. Moshi is not a vendor choice; it is an architecture that conflicts with HIP's requirements.

Note: Moshi is cited here because it is the most capable open-source full-duplex model and counterparties may ask why HIP did not adopt it. The answer is Section 3.

---

## 5. Licensing Insight: Apache-2.0 and the Embed-Redistribute Gap

### The gap

Most vendor enterprise self-host licenses do not permit what HIP needs: a platform vendor embedding the vendor's model in operator infrastructure across many operator deployments. The standard enterprise self-host license covers one entity, one deployment. A multi-operator platform deployment is redistribution or OEM embedding, which typically requires a separate commercial agreement.

Apache-2.0 (and MIT) are the exceptions. They explicitly permit:
- Modification and redistribution in any form
- Commercial use
- Distribution as part of a larger work (embed)
- No per-deployment licensing, no license server, no phone-home

For HIP deploying across 10 or 50 operator clouds, the operational cost of per-operator vendor license negotiations is significant. The LiveKit core SFU (Apache-2.0) is deployable at that scale without renegotiation. Whisper (MIT) and Kokoro (Apache-2.0) are deployable at that scale without renegotiation.

### The LiveKit model license flag

LiveKit's AI Agent SDK includes turn-detection models that are NOT Apache-2.0. They are distributed under a separate "LiveKit Model License." The specific terms of the LiveKit Model License need to be verified before HIP relies on those models for multi-operator deployment. The questions to verify:

1. Does the LiveKit Model License permit a platform vendor to deploy the models on infrastructure controlled by a third-party operator (not the platform vendor)?
2. Is redistribution of the model as part of a larger platform package permitted, or does each operator need a separate license?
3. Is there a license server or phone-home requirement?

If the LiveKit Model License does not permit multi-operator embed, HIP should substitute its own VAD/endpointing (Silero VAD is MIT-licensed and well-supported) and avoid the LiveKit turn-detection models. The core SFU remains clean.

### The Deepgram / Cartesia OEM gap

Deepgram and Cartesia self-host licenses are enterprise agreements. Enterprise agreements are negotiable; they are not inherently incompatible with multi-operator embedding. The question is whether OEM or redistribution rights are available, at what price, and whether a license-server requirement exists. HIP needs a direct conversation with both vendors. The alternative -- open-source STT/TTS -- has no such dependency.

---

## 6. Recommendation and Open Questions

### Recommended architecture (DIRECTION -- pending Bill's live LiveKit test)

**Governed core (in-boundary, required for all operators):**
- LiveKit (Apache-2.0 core SFU): transport and session management
- Deepgram Nova-3 / Flux self-hosted: STT plugin (subject to OEM/redistribution clarification)
- HIP text checkpoint: assemble_governed_context(), injection contract, edge LLM (qwen2.5:7b), epistemic record
- Deepgram Aura-2 self-hosted: TTS plugin (same license caveat)
- Fallback to Whisper + Kokoro if Deepgram OEM terms do not fit multi-operator embed

**Premium optional tier (per-household opt-in, audio leaves boundary under explicit consent):**
- ElevenLabs TTS: for operators or households paying for premium voice quality or branded voices
- Consent and disclosure to audio boundary crossing is required before enabling; this is a product and legal design item, not a technical one

**Architecturally excluded:**
- Moshi / full-duplex speech-to-speech (no text checkpoint -- structurally incompatible with disclosure governance)
- AssemblyAI (hosted-only STT -- no self-host path, audio leaves boundary)
- ElevenLabs in the governed core (hosted-only TTS -- same reason)

### Open questions requiring Bill's input or action before closing

**OQ-1 (LiveKit Model License, BILL):** Verify LiveKit Model License terms for multi-operator embed. Specifically: can HIP deploy LiveKit's turn-detection models on operator infrastructure? If not, HIP substitutes Silero VAD (MIT) and the core architecture is unchanged.

**OQ-2 (Deepgram OEM, BILL):** Initiate Deepgram conversation on OEM/redistribution terms for a multi-operator platform deployment. If Deepgram requires per-operator licensing or a license server, move to open-source STT (Whisper + faster-whisper) as the governed-core STT.

**OQ-3 (Cartesia license, BILL):** If Cartesia is the preferred TTS alternative (for latency reasons), initiate the same OEM conversation as OQ-2.

**OQ-4 (LiveKit live test, BILL):** Bill's in-progress live LiveKit test. The architecture direction above is contingent on the test confirming: (a) LiveKit SFU handles WebRTC session management at the required latency for household voice; (b) the text-checkpoint integration (STT output feeding assemble_governed_context(), governed text output feeding TTS input) works cleanly with LiveKit's room event model; (c) no architectural surprises in the agent/plugin interface that would require re-design.

**OQ-5 (ElevenLabs premium tier, BILL):** Product decision: does HIP offer an ElevenLabs-powered premium voice tier? If yes, the consent and disclosure mechanism for audio leaving the operator boundary needs to be designed and disclosed in the Debt Register or a separate consent spec. This is a product-commercial decision, not a technical architecture decision.

**OQ-6 (Eldercare endpointing calibration, BUILD):** Regardless of STT vendor, the silence threshold and endpointing parameters for eldercare speech need calibration against real older-adult audio samples. A 300-500 ms default silence threshold (Deepgram default, OpenAI server VAD default) is too aggressive for older adult speech patterns. Target: 600-800 ms configurable, with an operator-settable profile. This is a configuration-and-testing item, not a model change.

### What is decided regardless of the LiveKit test result

- The cascade architecture (STT -> text checkpoint -> TTS) is DECIDED. It is not a temporary measure pending full-duplex maturity; it is a permanent requirement of the governance architecture.
- HIP's text checkpoint (assemble_governed_context(), injection contract, epistemic record) is DECIDED. BUILD-1 delivered it. The voice path uses the same enforcement as the typed path.
- Full-duplex audio-native models (Moshi, GPT-4o audio, Gemini Live) are DECIDED excluded from the reasoning layer. Section 3 is the stable argument.
- Audio must not leave the operator trust boundary in the governed core. DECIDED. ElevenLabs and AssemblyAI are excluded from the governed core on this basis.
- Apache-2.0 or equivalent permissive licensing is the target for the governed-core components. DECIDED. OEM/redistribution due-diligence on Deepgram and Cartesia is an open question, not a challenge to this decision.

---

## Vendor Summary Table

| Vendor | Role | In-boundary | Multi-op-embed | Eldercare endpointing | Cost/min (self-hosted) | Quality | Status |
|---|---|---|---|---|---|---|---|
| LiveKit (SFU) | Transport frame | YES | YES (Apache-2.0 core); model license FLAG | N/A (transport) | Low (CPU SFU) | N/A | DIRECTION (pending live test) |
| Deepgram (self-hosted) | STT + TTS plugin | YES (on-premise) | UNCERTAIN (OEM needed) | STRONG (tunable) | ~$0.013-0.020/min (hosted ref) | Strong | DIRECTION (OEM TBD) |
| ElevenLabs | Premium TTS (opt-in) | NO (hosted) | N/A (API) | N/A (TTS only) | ~$0.015-0.026/min (TTS only) | BEST | DIRECTION (premium tier only) |
| AssemblyAI | STT | NO (hosted) | N/A | STRONG | Similar to hosted Deepgram | Strong | EXCLUDED (boundary) |
| Cartesia | TTS alternative | CONDITIONAL | UNCERTAIN (OEM needed) | N/A | Low (SSM, GPU-efficient) | Strong, low-latency | DIRECTION (backup, OEM TBD) |
| Whisper + Kokoro | OSS STT + TTS | YES | YES (MIT/Apache-2.0) | VARIABLE (VAD wrapper needed) | Infrastructure only | Competitive | VALID FALLBACK |
| Moshi / full-duplex | Full-duplex voice | YES (self-hosted) | CONDITIONAL (CC-BY-4.0) | N/A | Self-hosted GPU | High | EXCLUDED (no text checkpoint) |

---

*This memo is prepared for NDA-level distribution to technical counterparties. The demo system described herein operates locally or over VPN; no unauthenticated network path to the running system is exposed to the public internet. See HIP_DebtRegister_NDA_Appendix for network boundary constraints.*
