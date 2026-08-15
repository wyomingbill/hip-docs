---
doc: HIP Voice Architecture Research
part: P8 of the voice architecture research set
topic: Reference architecture for an identity-scoped, edge-deployed, full-duplex household voice system
source: ChatGPT deep research output (prompt 8 of 8), reviewed and marked down
status: reference
version: v20260710_1137
location: ~/hip-dev/docs/voice-research/
note: The source's large edge-architecture diagram was destroyed by RTF export (box-drawing characters lost). It is reconstructed here in plain ASCII from the surrounding text. Math rendered in plain notation. Tables preserved.
---

# Reference Architecture: Identity-Scoped, Edge-Deployed, Full-Duplex Household Voice

## Bottom line

A controlled prototype is buildable from existing components. A reliable household system is not yet proven. The individual technologies exist: full-duplex speech models that listen and speak concurrently, streaming diarization and overlapping-speech separation, speaker embeddings and verification, asynchronous retrieval and delegated reasoning, and attribute-based authorization with permission-aware memory.

What does not exist is a published system that combines these into an open-room assistant that can reliably identify several overlapping speakers, preserve private and shared context, enforce permissions, manage multiple conversations, and avoid revealing information to the wrong person. The architecture must therefore treat identity, addressee, audience, and conversation state as probabilistic, not as settled facts.

## 1. Overall architecture

Reconstructed from the source description (household edge stack, top to bottom):

```text
                        HOUSEHOLD EDGE

  Microphone arrays
     |
  AEC / denoise / beamforming / direction-of-arrival
     |
  Overlap detector -> conditional speech separation
     |
  Online diarization -> speaker-lane registry
     |
     +----------------------------+
     |                            |
  Voiceprint / liveness kernel   Addressee and floor model
     |                            |
     +----------------------------+
     |
  Identity-gating layer
     |
     +-----------------+------------------+
     |                 |                  |
  Vocabulary view   Context projection   Permission view
     |                 |                  |
     +-----------------+------------------+
     |
  Per-speaker interaction-model instances
  (speech/audio + action/control-token output)
     |
     +-----------------------------+
     |                             |
  Room interaction arbiter       Delegation broker
     |                             |
  Audience/output gate          Local -> Mid -> Core -> Frontier
     |                             |
  Room or private audio         Streaming result deltas
     |
  Governed memory: private | household-shared | room-ephemeral | tasks
```

The critical design decision is to use one interaction-model checkpoint with separate stateful instances for each active speaker lane, rather than expecting one existing model to understand an arbitrary number of simultaneous human audio streams. Moshi and PersonaPlex are built around one user stream and one assistant stream; extending that to an arbitrary number of independently identified speakers remains experimental.

## 2. Recommended components

| Layer | Recommended choice | Maturity |
| --- | --- | --- |
| Acoustic front end | Fixed-geometry microphone array, echo cancellation, denoising, beamforming, direction-of-arrival tracking | Established DSP; difficult in reverberant rooms |
| Overlap processing | Overlap detector followed by conditional continuous speech separation | Research-grade |
| Streaming diarization | NVIDIA NeMo online Sortformer; EEND-style as alternative | Usable, but not identity-grade |
| Voiceprint kernel | WeSpeaker ECAPA-TDNN or ResNet embeddings; TitaNet as integrated NeMo option | Established verification component |
| Anti-spoofing | ASVspoof-trained replay and synthetic-speech countermeasure | Necessary but inadequate alone |
| Streaming transcript | Conformer/RNN-T or CTC streaming ASR with identity-selected contextual bias packs | Established |
| Interaction model | PersonaPlex/Moshi-derived speech-to-speech model, extended with an action channel | Two-party prototype |
| Room coordinator | Deterministic arbiter plus small scene-state model | Custom; no standard implementation |
| Authorization | Cedar policy engine using ABAC plus household-relationship attributes | Mature policy technology |
| Memory | Append-only event log, temporal knowledge graph and vector index with private/shared projections | Components exist; governance early |
| Delegation | Hard privacy gate followed by RouteLLM-style quality/latency router | Routing proven; household use unproven |
| Gap filling | MoshiRAG-style lead/body/tail generation with asynchronous result injection | Research prototype |
| Output privacy | Audience-aware "safe-to-say" gate and private-device handoff | No proven complete solution |

## 3. Acoustic and speaker-lane processing

**Room audio front end.** Each room should have a calibrated multi-microphone array producing a cleaned room mixture, direction-of-arrival estimates, beam hypotheses, speech/non-speech probability, overlap probability, an echo-reference signal from the assistant's own speaker, and spatial tracks for active talkers. Direction is a useful continuity signal but must never be treated as identity; people move, trade seats and speak from adjacent rooms.

**Conditional separation.** Do not continuously separate all room audio; separation models introduce artifacts, duplicate speech between channels and swap assignments across windows. Instead: run the diarizer on the cleaned mixture, invoke continuous speech separation only when overlap probability exceeds a threshold, provide both the separated stream and the original mixture features downstream, and attach a separation-confidence score to every resulting lane. Cross-window speaker consistency and crosstalk remain open problems in real far-field meetings.

**Online diarization.** Use NeMo's online Sortformer as the primary diarizer (or a modular pipeline of MarbleNet VAD, TitaNet embeddings and multi-scale decoding; EEND-style where overlap performance matters more than modularity). Streaming EEND has demonstrated online operation at ~one-second latency, but online enrollment of unseen speakers and unknown participant counts remain difficult. The output is not "Speaker = Bill" but a lane with principal posteriors (Bill 0.91, Guest_1 0.04, Unknown 0.05), overlap probability, separation confidence, direction, and track age. Diarization answers which segments come from the same source; verification answers how similar that source is to an enrolled member; neither independently establishes identity.

## 4. Voiceprint kernel

**Enrollment.** Each member enrolls using multiple recordings across different rooms and microphone distances, normal/quiet/projected speech, several days rather than one session, optional phone or earbud samples, and periodic consensual template refresh. Store encrypted embeddings and enrollment metadata; raw enrollment audio should be optional and separately protected. WeSpeaker provides production-oriented embeddings (ECAPA-TDNN, ResNet) with CPU, GPU, ONNX and TensorRT paths.

**Runtime identity state.** The kernel combines voice-embedding similarity, diarization continuity, direction/spatial continuity, device proximity where consented, replay/deepfake score, recent explicit authentication, and contradictory evidence from other lanes. It exposes three authorization states:

| State | Permitted behavior |
| --- | --- |
| Verified | Personalized context and ordinary low/medium-risk actions |
| Provisional | Personalized vocabulary and benign context; no consequential action |
| Unknown/ambiguous | Household-public context only |

Thresholds must be calibrated against the desired false-accept rate on the actual microphones and rooms. There is no universal cosine-similarity threshold that safely generalizes across households, devices and acoustic conditions.

**Voiceprint is not high-assurance authentication.** Voice verification should be a convenience credential, not sufficient authorization for purchases, door or alarm control, sending sensitive messages, financial or medical disclosure, changing another member's permissions, or destructive actions. Replay and synthetic-voice generation remain serious weaknesses; ASVspoof performance frequently degrades across unseen attacks, codecs, microphones and environments. High-risk actions should require a passkey, trusted phone confirmation, PIN or another independent factor.

## 5. Identity-gating layer

The identity gate sits between perception and every use of personal data, controlling four operations separately: vocabulary selection, context retrieval, action authorization, and spoken disclosure. A system that gates tool execution but not memory retrieval can still disclose private information; a system that gates retrieval but not spoken output can reveal authorized information to an unauthorized nearby person.

**Vocabulary scope.** For each lane, build a temporary contextual-bias pack: household-common entities plus member contacts, projects/products, current-task entities, and recent corrections. Activate the member-specific portion only after identity reaches at least provisional confidence; unknown speakers receive household-common vocabulary. Dynamic bias lists improve recognition of names and uncommon entities, while indiscriminate biasing damages ordinary-word recognition, so lists turn on only when context warrants.

**Context projection.** Memory divides into at least four scopes: PRIVATE(member), SHARED(household or selected members), ROOM_EPHEMERAL(current interaction only), TASK_EPHEMERAL(delegated job scratch). Every fragment carries owner or joint owners, allowed readers/writers, sensitivity, source/provenance, created/superseded times, confidence, retention policy, whether it may leave the home edge, and whether it may be spoken in front of others. For principal P and audible audience A, the context compiler produces household-public memory plus shared fragments authorized for P and A plus P's private memory when audience policy permits, plus current room and task state. Permission-aware memory and temporal-graph work support this, but published multi-user memory systems are still largely synthetic or experimental.

**Policy engine.** Use Cedar or a comparable analyzable ABAC engine. A decision evaluates subject (asserted principal, identity confidence, household role, guardian relationship), action (read_memory, speak_fact, call_tool, write_memory, send_message, control_device), resource (memory fragment, device, account, conversation, task), and environment (room, audible audience, time, liveness score, network tier, privacy classification, recent step-up authentication). ABAC fits because decisions depend on attributes of subject, resource, operation and environment rather than a static role. Example: permit speak_fact when requester is Bill, fact.owner is Bill, identity_state is verified, and audience is within fact.allowed_audience; otherwise respond generically or transfer the answer to Bill's private device.

**Continuous authorization.** Authorization cannot occur only at conversation start; identity and audience can change mid-sentence. Reevaluate when a new speaker enters, a verified speaker leaves, overlap creates uncertainty, the response changes from generic to personal, a tool call becomes consequential, a delegated result returns, memory is written, or output changes from a private endpoint to a room speaker.

## 6. Edge interaction model

**Practical baseline.** Use a PersonaPlex/Moshi-derived model as the starting checkpoint (synchronized user/assistant audio streams, streaming neural codec, ~80 ms frames; PersonaPlex adds role and voice conditioning to a 7B Moshi derivative; open implementations in PyTorch, MLX, Rust). This is lightweight relative to a frontier reasoning model but not lightweight enough for ordinary smart-speaker silicon; a 7B-class checkpoint requires an edge GPU, capable NPU or aggressive quantization. A distilled 1-3B interaction model is the desirable production target, but no published 1-3B checkpoint currently demonstrates Moshi-class full-duplex speech, interruption handling, action-token control and multi-user identity scoping. Distilling that behavior is a research program, not a downloadable component.

**Separate interaction instances.** Instantiate the same model once per active speaker lane, each with lane_id, principal posterior, private context projection, shared scene summary, current floor state, outstanding task IDs, and audio/action-token state. Each instance handles listening, backchannels, interruption detection, turn continuation, clarification, delegation decisions, cancellation, and whether a response is for the room or a private endpoint. The room arbiter sees all instances and makes the final audible decision. This avoids forcing private member contexts into one shared transformer KV cache and limits cross-speaker contamination; the cost is that edge compute grows with the number of active speakers.

**Action channel.** Extend the interaction model with an explicit non-audio action channel. DuplexSLA and related work represent speech and control decisions on a shared time axis; Thinking Machines describes ~200 ms micro-turns while a separate model reasons asynchronously. Example outputs: SILENCE, BACKCHANNEL(type=acknowledge), YIELD_FLOOR, INTERRUPT_SELF, ADDRESS(speaker=lane_2), DELEGATE(task=t83, class=calendar_query), CANCEL(task=t77), PRIVATE_HANDOFF(principal=Bill), REQUEST_STEP_UP(action=unlock_door). The interaction model may propose actions; deterministic policy and room-arbitration layers must approve them.

## 7. Room interaction arbiter

Not a general reasoner. A low-latency state machine plus small classifier responsible for determining whether speech is addressed to the assistant, tracking conversational floor, selecting which speaker lane has priority, suppressing duplicate answers from parallel lane instances, deciding whether to backchannel/speak/pause/remain silent, preventing the assistant from talking over urgent human speech, routing sensitive responses to private devices, and cancelling or parking obsolete tasks.

A single room speaker should normally emit only one assistant response at a time. Parallel answers to different people should be delivered through headphones, phones or personal displays; two simultaneous assistant voices in the same room would worsen intelligibility and make privacy enforcement nearly impossible. No published system has solved general addressee detection and floor management for several natural overlapping household conversations; existing full-duplex benchmarks overwhelmingly model one user and one assistant.

## 8. Delegated reasoning cascade

The edge interaction model owns timing and continuity and does not wait synchronously for reasoning. The cascade:

| Tier | Location | Typical work | Data exposure |
| --- | --- | --- | --- |
| Local edge | Home appliance | Household lookup, simple classification, local device control, cached answers | Raw/private context allowed |
| Mid | Access or metro edge | Medium-model reasoning, operator services, broader local retrieval | Filtered identity-scoped context |
| Core | Regional/private cloud | Large-model reasoning, complex planning, enterprise-grade tools | Minimal relevant context |
| Frontier | External provider | Hardest general reasoning or specialist model | Declassified task packet only |

Model names should be replaceable; routing contracts, policy classifications and task schemas should remain stable when models change.

**Delegation envelope.** The interaction model emits a structured task rather than its entire conversation state: task_id, conversation_version, requesting_principal, audience, task_type, normalized question, permitted data fragments, prohibited data classes, maximum routing tier, deadline, output schema, required confidence, tool permissions, memory-write permissions, cancellation token. The privacy gate first determines which tiers are legally and contractually eligible; only then does the quality router optimize for expected answer quality, latency and cost. RouteLLM and FrugalGPT show learned routers and cascades can choose among weaker and stronger models to reduce cost while preserving quality; edge/cloud work shows context-transfer and recomputation costs must be considered. The learned router must never override an authorization denial.

## 9. Asynchronous gap filling

**Delegation sequence.** (1) The interaction model detects the request exceeds local confidence, needs a tool, or has a material factual dependency. (2) It emits DELEGATE. (3) The broker creates a versioned envelope. (4) Local processing begins immediately. (5) A higher tier may start speculatively when complexity or deadline warrants. (6) The interaction model keeps listening and managing the conversation. (7) Results return as streaming structured deltas. (8) The output gate validates identity, audience and permissions again. (9) The result is inserted into live interaction state. (10) The model speaks it only if the task is still relevant.

**Lead/body/tail generation.** MoshiRAG provides the most concrete pattern: a locally generated lead (acknowledgement, framing, partial answer), an externally retrieved or reasoned body, and a natural tail. The model continues speaking and listening while retrieval executes. Safe gap filling: acknowledging the request, restating the relevant constraint, giving a locally known part of the answer, explaining what is being checked, asking a genuinely necessary clarification, or yielding the floor and continuing to listen. Unsafe gap filling: inventing a likely answer, repeating generic filler, making a consequential commitment before authorization, or speaking private context merely to occupy latency.

**Stale-result control.** Every task binds to a conversation-state version. A returned result is discarded, parked or reframed when the user cancels, the question changes, another person takes over, the identified speaker changes, the audience changes, a newer task supersedes it, or the result arrives after its usefulness deadline. This prevents an old frontier answer from being spoken into a different conversation.

## 10. Multiple simultaneous speakers and shared context

**Per-speaker lanes, shared scene.** Maintain two separate structures. A speaker lane holds principal posterior, private context view, active task list, speech/prosody state, current addressee hypothesis, and permission token. The household scene holds active lanes, spatial positions, audible audience, shared topic stack, room-public facts, current assistant floor state, pending shared decisions, and conflicting instructions. The shared scene may inform every interaction instance; private lane context may not.

**Shared-memory writes.** A statement made in the room should not automatically become permanent household memory. Use separate write decisions: ephemeral observation (retain only during the interaction), private memory (attach to the speaking member), shared factual memory (available to authorized members), joint decision (requires identified participants and potentially explicit confirmation), and sensitive inference (do not persist without consent). A member saying "I may leave my job" is not authorization to tell the household that the member is leaving their job.

**Conflicting commands.** The policy layer resolves by resource ownership, guardian or delegated authority, household role, existing agreements, recency and explicitness, required consensus, and consequence level. One member may control music volume while another is authorized to change alarm settings; for genuinely joint resources the assistant may need to collect consent rather than choose a winner. There is no established computational model for household authority, consent and changing relationships; reported performance remains far below what would justify autonomous resolution of consequential family disputes.

## 11. Principal failure modes and unsolved problems

| Failure | Consequence | Current status |
| --- | --- | --- |
| Overlapping speaker identity | Private context assigned to the wrong person | No reliable end-to-end solution |
| Diarization/verification correlated errors | Clean but wrongly labeled speaker lane | Insufficiently modeled |
| Voice cloning and replay | Impersonation and unauthorized actions | Open; step-up authentication required |
| Unknown-speaker enrollment | New guest confused with known member | Open-set recognition remains difficult |
| Addressee detection | Assistant answers speech intended for another human | Unsolved in unconstrained rooms |
| Parallel conversations | Context and task crossover | Existing full-duplex models are fundamentally two-party |
| Audible privacy | Correct answer heard by unauthorized bystander | No software-only solution |
| Context bleed between transformer sessions | One member's facts influence another's answer | Requires strict external context isolation |
| Identity drift during long sessions | Authorization persists after the person leaves | Requires continuous reevaluation |
| Separation artifacts and speaker swaps | Words or identities move between lanes | Open in real far-field audio |
| Echo/self-speech confusion | Assistant interrupts itself or treats playback as user speech | AEC reduces but does not eliminate |
| Stale asynchronous results | Answer appears after topic or audience changes | Versioning and cancellation mitigate |
| Router manipulation | Prompt causes inappropriate frontier routing or disclosure | Privacy gate must precede learned routing |
| Memory poisoning | False or malicious statement becomes persistent fact | Provenance and confirmation help; not solved |
| Derived-fact ownership | System infers sensitive facts with no clear owner | Governance problem, not just retrieval |
| Children, aging and voice change | Recognition and permission errors over time | Requires re-enrollment and conservative policies |
| Network failure | Delegated task hangs during live dialogue | Local degraded mode required |
| No integrated benchmark | Component scores hide system-level failures | Major evaluation gap |

## 12. What is established versus experimental

**Established enough to build with:** streaming VAD and ASR, speaker embeddings, online diarization under controlled conditions, contextual vocabulary biasing, attribute-based policy enforcement, local versus remote model routing, private/shared data stores, two-party full-duplex speech prototypes.

**Research-grade but usable in a prototype:** conditional overlapping-speech separation, online EEND and Sortformer in uncontrolled rooms, Moshi/PersonaPlex-class full-duplex interaction, action-token interaction control, asynchronous reasoning injection, permission-aware multi-user memory.

**No proven solution:** reliable open-set identity during overlapping household speech, one model managing several simultaneous human audio streams, robust addressee detection across parallel conversations, voice-only high-assurance authorization, preventing audible disclosure to bystanders, correct ownership and consent for inferred household memories, end-to-end evaluation combining identity, permissions, overlap, delegation and privacy.

## Reference design conclusion

The defensible architecture is not an omniscient room model. It is a collection of identity-scoped speaker lanes, each served by a fast edge interaction model, coordinated by a deterministic room arbiter and constrained by a policy engine. Heavy reasoning is delegated through a privacy-first cascade and returned asynchronously as versioned result deltas. Shared household context exists as a governed projection, not as one unrestricted communal prompt. The most important safety rule: uncertain identity may personalize recognition, but it must not authorize consequential action or private disclosure. That boundary is what turns speaker recognition from a convenience feature into a usable household security architecture.

---

# HIP Relevance Notes

1. This is the capstone: it is HIP's architecture, described from the outside by someone solving the general problem. Identity-scoped lanes, a fast edge interaction model, a deterministic arbiter, a policy engine, a privacy-first delegation cascade, and governed context as a projection rather than one communal prompt. Every one of those is a HIP layer already named in the roadmap. The research independently reconstructs the HIP design, which is the strongest possible coherence check on the architecture.
2. The single most important safety rule stated here ("uncertain identity may personalize but must not authorize consequential action or private disclosure") should be lifted verbatim into HIP's governance spec and the NDA. It is the precise, defensible articulation of the operator-custodial trust model, and it draws the line between a convenience feature and a security architecture.
3. The delegation envelope (section 8) is a concrete schema HIP can adopt directly. It maps onto HIP's existing per-member envelope encryption and fact-scoping: conversation_version, permitted data fragments, prohibited data classes, maximum routing tier, memory-write permissions. This is the interface contract between HIP's interaction layer and its cascade, and it is where governance is enforced.
4. The failure-modes table (section 11) is HIP's risk register and its differentiation map at once. Every "no proven solution" row is whitespace where HIP's governed design can define the answer rather than adopt one: open-set identity during overlap, addressee detection across parallel conversations, audible-privacy enforcement, and consent for inferred memories. These are the governance problems HIP's operator record and fact graph are built to address.
5. The honest framing (buildable prototype, not a proven reliable system) is exactly right for the NDA's R&D posture. HIP presents this as the forward development path with named unsolved problems, not as a shipped capability. The "established / research-grade / no proven solution" tiering in section 12 is a ready-made maturity map for the roadmap and for staging the build.
6. The per-lane-instance decision (one checkpoint, separate stateful instance per speaker) is the concrete answer to how HIP's multi-member model runs on the interaction layer without cross-member context bleed. It is the runtime expression of per-member envelope encryption and context isolation, and it sets the compute-scales-with-active-speakers constraint that the RTX PRO 6000 tier has to absorb.

# Reference Sources

Moshi paper: arxiv.org/html/2410.00037v2
Overlap separation/diarization: arxiv.org/pdf/2001.11482
NeMo diarization models: docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/speaker_diarization/models.html
WeSpeaker: ar5iv.labs.arxiv.org/html/2210.17016
ASVspoof: arxiv.org/abs/2109.00537
Contextual biasing: arxiv.org/abs/2306.00804
Permission-aware / multi-user memory: arxiv.org/abs/2505.18279
NIST ABAC SP 800-162: csrc.nist.gov/pubs/sp/800/162/upd2/final
DuplexSLA: arxiv.org/html/2605.20755v2
MoshiRAG: arxiv.org/html/2604.12928v2
RouteLLM / cascade routing: arxiv.org/html/2406.18665v3
Multi-user memory/identity routing: arxiv.org/abs/2604.25022
