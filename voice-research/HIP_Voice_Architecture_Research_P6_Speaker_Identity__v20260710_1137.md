---
doc: HIP Voice Architecture Research
part: P6 of the voice architecture research set
topic: Attaching speaker identity to a live conversational stream, diarization, verification, multi-speaker scoping
source: ChatGPT deep research output (prompt 6 of 8), reviewed and marked down
status: reference
version: v20260710_1137
location: ~/hip-dev/docs/voice-research/
note: RTF export mangled math; rendered in plain notation from source text. Tables preserved.
---

# Attaching Speaker Identity to a Live Conversational Stream

A production system should treat speaker identity as a real-time side channel attached to every audio frame, transcript fragment, memory write, model input and tool request. It should not ask the conversational LLM to infer identity from raw audio and then trust that inference. The reliable architecture:

```text
microphones
  -> acoustic echo cancellation / noise reduction / beamforming
  -> speech activity + overlap detection
  -> online diarization: which local speaker track is active?
  -> speaker embedding extraction
  -> enrolled-speaker verification / open-set identification
  -> persistent identity and conversation-thread tracker
  -> speaker-attributed ASR
        -> utterance envelope, for example:
           {
             local_track: "room1_speaker_2",
             person_id: "household:bill",
             identity_confidence: 0.97,
             auth_level: "voice_recognized",
             active_interval: [1042.32, 1044.81],
             overlap: false,
             room: "kitchen",
             addressee: "assistant",
             conversation_thread: "kitchen_17",
             audience: ["bill", "guest_1"]
           }
  -> context retrieval + deterministic policy gate
  -> conversational model / tool runtime
```

The important separation, six different problems:

- Diarization: which acoustic speaker spoke when?
- Verification: does this speech match an enrolled person?
- Identification: which enrolled person is the best match, or is the person unknown?
- Authentication: is the evidence strong enough to permit a sensitive action?
- Conversation assignment: which conversation is this utterance part of?
- Authorization: what may this person see or do in the current audience context?

## 1. Speaker diarization

Diarization produces a time-indexed speaker-activity matrix. For a four-speaker model, one frame might read [0.97, 0.03, 0.81, 0.01], meaning speakers 1 and 3 are probably active simultaneously. Modern overlap-aware systems use multi-label outputs, not a single softmax speaker choice, because more than one speaker may be active in the same frame. NeMo Streaming Sortformer produces a (T x S) matrix where S is the maximum number of speakers and each 80 ms frame carries an independent activity probability per speaker; the current open model supports up to four speakers.

**Cascaded diarization:** audio -> VAD -> speech windows -> speaker embeddings -> clustering -> optional overlap-aware resegmentation. Clustering assigns session-local anonymous labels (SPEAKER_00, SPEAKER_01). SPEAKER_00 does not inherently mean Bill. NeMo's cascaded pipeline uses VAD, a speaker embedding model such as TitaNet, clustering, and optionally a neural multi-scale diarization decoder. It extracts embeddings at several window lengths because short windows give good timing but weak identity, while longer windows give stronger identity but poorer temporal resolution. Traditional windows are commonly 1.5 to 3 seconds.

**End-to-end diarization (EEND)** treats the task as multi-label frame classification: each output indicates whether speaker k is active at frame t. EEND was developed partly because conventional single-speaker clustering does not naturally represent overlap. The unresolved issue is speaker permutation: the model's "output 1" has no intrinsic identity. Systems handle this through permutation-invariant training, arrival-time ordering, speaker attractors, speaker-tracing buffers, and persistent speaker caches. Pyannote's segmentation uses permutation-invariant multi-label classification on short chunks; NeMo Sortformer orders speakers by first appearance.

## 2. Speaker embeddings and voiceprints

A speaker-verification model converts variable-length speech into a fixed-dimensional vector, trained so embeddings from the same person are close, embeddings from different people are separated, lexical content matters as little as possible, and channel/microphone/noise variation is partially suppressed. Architectures: x-vector and TDNN systems, ECAPA-TDNN, ResNet speaker encoders, TitaNet, and newer self-supervised encoders. TitaNet uses 1-D depthwise-separable convolutions, squeeze-and-excitation layers, global context and attentive statistics pooling; TitaNet-Large has ~23M parameters.

**Enrollment** creates a reference template per member. For several clean utterances, the simplest template is a normalized weighted mean of the embeddings, with weights favoring longer samples, high SNR, non-overlapped speech, samples from different rooms and microphones, and recent samples. A practical household enrollment captures several samples rather than a single phrase; the objective is to capture expected variation across distance, room acoustics, microphone position, illness, fatigue and speaking style. The stored voiceprint is the embedding template, not necessarily the raw recording. It is still biometric data and should be encrypted and access-controlled.

**Verification** is a one-to-one claim ("Is this Bill?"), commonly scored by cosine similarity, accepting when the score exceeds a per-member threshold. Alternative back ends include PLDA, adaptive score normalization and learned scoring networks. SpeechBrain's ECAPA and WeSpeaker both support cosine comparison; WeSpeaker also publishes adaptive score-normalization recipes.

**Open-set identification** compares against all enrolled members, assigning the best match only when its score exceeds an accept threshold and preferably when the winning margin over the runner-up is sufficiently large. Otherwise the output must be UNKNOWN. Without the unknown state, the system is forced to misidentify every visitor as the least-dissimilar household member.

## 3. Thresholds are policy decisions

Published verification results usually report equal error rate (EER), the operating point where false-accept and false-reject rates are equal. A lower EER indicates a more discriminative model; it does not specify the threshold a household should use. A production threshold depends on the action:

| Action | Appropriate posture |
| --- | --- |
| Personalize greeting | Lower threshold tolerable |
| Retrieve personal music preference | Moderate threshold |
| Read private messages aloud | High threshold plus audience check |
| Purchase, unlock door, disclose health data | Voice alone insufficient |
| Change access permissions | Require stronger authentication |

A single threshold should not control all behavior. A useful design has at least three states:

```text
score < T1          -> unknown
T1 <= score < T2    -> likely Bill; low-risk personalization only
score >= T2         -> strongly matched Bill; still subject to replay/liveness controls
```

Values must be calibrated on household-like far-field recordings. Thresholds from one model are not portable to another, and clean VoxCeleb EERs should not be treated as expected kitchen performance.

## 4. Maintaining identity across a continuous stream

Two identity layers are needed: a short-lived acoustic track and a persistent household identity.

**Acoustic track.** An online diarizer creates tracks (room1_track_0, room1_track_1). For each clean speech interval it updates a centroid by exponential moving average, but only when the track has high diarization confidence, only one speaker is active, speech is sufficiently long, signal quality is acceptable, and the new embedding is consistent with the existing track. Updating during overlap is dangerous: the centroid can become a mixture of two people and permanently corrupt the track.

**Persistent person match.** The track centroid is compared with enrolled voiceprints (for example: track_2 scores 0.96 Bill, 0.41 Sarah, 0.18 unknown guest). The resolved identity is maintained with hysteresis; the system should not flip from Bill to Sarah because one noisy 400 ms interval scored differently. A useful tracker maintains track_id, candidate_person_id, posterior_confidence, first_seen, last_seen, speaker_centroid, recent_embedding_history, room/location, direction_of_arrival, overlap_state, and identity_lock_state.

**Speaker caches.** NeMo Streaming Sortformer provides a concrete continuity implementation: its Arrival-Order Speaker Cache retains selected embeddings from previously observed speakers and compares new chunks against that cache so the same person keeps the same session label. Other online EEND work uses speaker-tracing buffers or continuously updated attractors; FLEX-STB reported online handling of variable speaker counts and overlap with roughly one-second algorithmic latency.

**Identity is provisional at speech onset.** A diarizer may detect that someone new started speaking within a few hundred milliseconds, but reliable identification usually requires more speech:

```text
0-300 ms:        speech detected; local anonymous track created
300-1,000 ms:    preliminary embedding; likely identity candidate
1-3 seconds:     stable voiceprint comparison; permission-bearing identity decision
```

These are reasonable engineering stages, not universal guarantees. Short acknowledgments such as "yes" or "no" are intrinsically difficult because they contain little speaker evidence.

## 5. Overlapping speech

Overlap introduces two distinct problems: who is active, and what did each active person say. A diarizer may correctly output Bill active 0.94 and Sarah active 0.89 for the same 500 ms interval; that does not produce two clean waveforms and does not let a conventional ASR determine which words belong to whom. Pyannote's overlap-aware segmentation predicts multiple speaker activities at fine frame resolution and can improve assignment, but even its published work describes overlap detection and assignment as unresolved.

Required overlap pipeline: microphone mixture -> overlap detector -> source separation or spatial beamforming (source A, source B) -> speaker embedding on each separated source -> identity match per source -> independent streaming ASR per source.

Techniques: multi-label diarization (EEND, pyannote segmentation, Sortformer) can mark more than one speaker active, necessary but insufficient for recovering content. Blind speech separation (Conv-TasNet, SepFormer) splits a mixture into generic channels whose order is arbitrary, so each output still needs voiceprint matching. Target-speaker extraction (SpeakerBeam, VoiceFilter) conditions the separation network on an enrolled speaker representation to directly extract the target person's voice. Microphone arrays and direction of arrival estimate spatial direction and form beams; spatial information is often more useful than voiceprints in the first few hundred milliseconds because direction can be estimated before enough speech accumulates for a stable embedding. The strongest household design combines direction of arrival, beamforming, voiceprint embeddings, face/body tracking where permitted, and conversation history.

Overlap is especially difficult when speakers are close together, in the same direction, one much louder, the room is reverberant, the television contains speech, the assistant's own loudspeaker leaks into the mic, separation artifacts damage embeddings, the user moves while speaking, or two voices are acoustically similar. Acoustic echo cancellation is mandatory for a full-duplex assistant; otherwise assistant playback may be classified as another human or contaminate the user's voiceprint.

## 6. Binding context and permissions to the speaker

The conversational model should receive a structured speaker label, but authorization must occur outside the model. A speaker-attributed event carries utterance_id, speaker (track_id, person_id, status, confidence), speech (text, start, end, overlap), and interaction (addressed_to, conversation_id, audience).

**Context retrieval** should filter memory by principal, conversation, audience, purpose, consent, and resource policy. Bill's model context should not be "everything known about Bill." It should be the subset usable for this purpose, in this room, in front of the current audience, at the current authentication level:

```text
Bill alone:                assistant may read Bill's email aloud
Bill plus unknown guest:   assistant may acknowledge the request but
                           should not reveal email contents through room audio
Child speaking:            shopping tool available; purchase may require parent approval
Unknown visitor:           household-public information only
```

**Tool gating.** The LLM may propose a tool call (for example gmail.search with query is:unread). The runtime evaluates principal, identity_strength, action, resource_owner, audience, and output_channel. The policy engine may permit the search but deny reading results aloud, or require delivery to Bill's phone. The model must not be the final enforcement point. Prompt instructions such as "do not show Sarah's data to Bill" are not an access-control system.

**Separate recognition from authentication.** Voice recognition is vulnerable to replayed recordings, synthetic or cloned voices, telephone playback, enrollment poisoning, changes from illness or aging, and channel mismatch. For high-impact actions, combine voice with another factor: presence of a trusted phone, local device unlock state, a PIN, explicit confirmation, face match, or a cryptographic device credential.

## 7. Open-weight options

Accuracy figures are not directly comparable. EER measures verification; DER measures diarization; different DER results use different datasets, speaker counts, overlap policies, collars and sometimes oracle VAD.

| Option | Function | Published accuracy | Streaming latency | Size / deployment | On-device assessment |
| --- | --- | --- | --- | --- | --- |
| pyannote Community-1 | Full diarization pipeline | DER 11.7% AISHELL-4; 17.0% AMI IHM; 11.2% VoxConverse, no collar, overlap included | No official production streaming latency | CC-BY-4.0; CPU or CUDA; gated but accessible | Strong offline/reference. Full Python/PyTorch awkward for embedded; not an out-of-box low-latency tracker |
| NeMo Streaming Sortformer 4spk v2.1 | E2E online diarization with speaker cache | At 1.04 s latency: 15.09% DER DIHARD 4spk; 6.65% CALLHOME 2spk; 16.67% AMI IHM | 1.04 s input buffering, RTF 0.093 on RTX 6000 Ada; v2 also 320 ms config at RTF 0.18, lower accuracy | ~117M params; four-speaker max; NVIDIA Open Model License | Good on desktop/datacenter GPUs. Possible on Jetson but unproven by NVIDIA benchmark; too heavy for phone CPU |
| NeMo TitaNet-Large | Speaker embedding, verification, clustering backbone | 0.66% EER cleaned VoxCeleb1 | No official per-utterance latency | 23M params; CC-BY-4.0; ONNX via sherpa-onnx | Practical on Jetson and laptop. ~92 MB FP32 weights. Good household voiceprint candidate after calibration |
| TitaNet-Small | Lightweight embedding | 6M params, near-SOTA diarization | No official benchmark | NeMo; ONNX via sherpa-onnx | Better embedded candidate than Large where memory/power matter; needs far-field eval |
| WeSpeaker ResNet293-LM | Embedding, verification, clustering | 0.447% EER VoxCeleb1-O clean with LM tuning and AS-Norm | No official live latency | 28.62M params; 28.10 GFLOPs; 256-D; ONNX; CC-BY-4.0 | Excellent accuracy but heavier than param count implies. Fine on edge GPU; ResNet34 variants more practical for mobile |
| SpeechBrain ECAPA-TDNN | Embedding and verification | 0.80% EER cleaned VoxCeleb1 | No official streaming latency | Apache-2.0; PyTorch/SpeechBrain; cosine | Easy baseline, feasible on edge GPU; benefits from ONNX conversion |
| NeMo ECAPA-TDNN | Embedding and verification | 0.92% EER cleaned VoxCeleb; 1.94% AMI Lapel DER oracle | No official live latency | 22.3M params; 192-D; ~86 MB checkpoint | Similar feasibility to TitaNet-Large; TitaNet slightly better clean numbers in NeMo cards |
| sherpa-onnx diarization stack | Embedded runtime: pyannote-style segmentation + 3D-Speaker or NeMo embeddings | Depends on selected models | Platform-dependent | ONNX Runtime; FP32/INT8; C/C++/Java/Kotlin/Swift/Rust/JS; Android/iOS | Best deployment path in this list for phones, embedded Linux, appliances. Runtime and packaging, not a new model |

What the numbers do not show: TitaNet's 0.66% and WeSpeaker's 0.447% EER are on VoxCeleb protocols. A kitchen involves six-meter distance, reverberation, appliances, simultaneous speech, children, television audio, different microphones, and sub-one-second segments. A household system should build its own evaluation set and report false-accept rate for unknown guests, false-reject per member, member-to-member confusion, accuracy by speech duration, accuracy during overlap, accuracy by room and microphone, time until stable identity, identity-switch rate per hour, DER, and speaker-attributed WER.

## 8. Recommended real-time identity architecture

**Fast path (every 10-80 ms):** AEC, VAD, overlap probability, direction of arrival, online diarization probabilities. Produces anonymous speaker tracks quickly enough for interruption handling and turn-taking.

**Medium path (on accumulated clean windows):** speaker embedding, track-centroid update, household voiceprint comparison, open-set rejection, identity confidence update. May lag initial speech by one or more seconds.

**Slow path (periodic):** re-cluster recent tracks, correct track swaps, merge repeated appearances, update voice templates only from high-confidence speech, repair transcript attribution, persist confirmed identity mappings.

The live assistant should tolerate corrections. An utterance may initially be tagged unknown and later become Bill. Permission-bearing actions should wait for sufficient evidence rather than retroactively undoing an unauthorized disclosure.

## 9. Parallel conversations in a household

This is harder than ordinary diarization because there are three simultaneous assignment problems: audio frame to speaker, speaker to conversation thread, and thread to authorized context. Diarization solves only the first.

Example, one room: Bill to Sarah "Do we still have dinner reservations?"; teenager to friend "I already sent you the address"; Sarah to assistant "What time was the reservation?"; Bill to assistant "And text it to Mark." The assistant must determine that the first utterance was not directed to it, that Sarah's question belongs to the Bill-Sarah dinner thread, that Bill's instruction refers to the reservation result, which Mark Bill means, whether Sarah may see Bill's contact resolution, whether the teenager's parallel conversation must be excluded, and whether speaking the result aloud exposes private information to the friend. Nothing in a voiceprint resolves this.

**Required conversation state:** maintain concurrent thread objects, each with participants, topic, recent turns, and shared entities, plus an ambient-room object with current people and acoustic tracks. Every utterance gets a thread distribution conditioned on speaker, words, timing, direction, gaze and prior turns, and an addressee distribution (is the assistant addressed?). Useful signals: wake word or assistant name, vocatives ("Sarah", "Dad"), physical orientation and gaze, microphone direction of arrival, adjacency-pair timing, who asked the preceding question, lexical topic continuity, whether the person normally participates in that thread, and explicit household interaction rules.

**Shared context creates contamination risk.** A single room-level transcript fed into one LLM context will blend the parallel conversations; the model may answer a question directed to another person, bind a pronoun to the wrong entity, store a private statement as household-shared memory, expose one conversation's information in another, treat television speech as a household member, or attach an utterance to the right person but the wrong topic. The correct architecture is not "all room speech -> one transcript -> one LLM context." It is:

```text
speaker-attributed events
  -> conversation-thread router
       -> thread A context
       -> thread B context
       -> ambient/shared event layer
  -> speaker- and audience-filtered retrieval
  -> assistant participation decision
```

**Shared household memory must remain separate from thread context.** A fact can be private to Bill, shared between Bill and Sarah, shared with all adults, shared with the entire household, public to current guests, or ephemeral to this conversation only. The speaker who states a fact is not automatically the sole owner, and presence in the same room does not automatically grant future access. Each memory write needs provenance and scope: fact, source_speaker, conversation, heard_by, visibility, confidence, and whether it was derived from overlap.

## Bottom line

The implementable design: (1) online overlap-aware diarization creates stable anonymous tracks; (2) speaker embeddings match those tracks to enrolled identities; (3) an open-set resolver preserves UNKNOWN rather than forcing a member match; (4) a persistent tracker uses speaker caches, centroids and hysteresis; (5) separation or beamforming is required when two people speak simultaneously; (6) conversation-thread routing determines who is talking to whom and which context applies; (7) a deterministic policy layer gates memory retrieval, tool execution and output disclosure using speaker, authentication strength and audience; (8) voice identity is not sufficient authentication for high-impact actions.

For a household prototype, the strongest practical combination: microphone array plus AEC, NeMo Streaming Sortformer for online tracks, TitaNet or a smaller WeSpeaker model for enrolled identity, a separate thread/addressee tracker, and an external permission and consent engine. Pyannote Community-1 is the stronger offline benchmark and evaluation tool; NeMo Streaming Sortformer is the more directly usable live component; TitaNet, ECAPA or WeSpeaker perform persistent identity resolution. None of them solves conversation membership or household authorization by itself.

---

# HIP Relevance Notes

1. This is the technical spine for HIP's speaker-verification / identity kernel, and it validates the existing design direction. HIP already has Resemblyzer GE2E speaker verification and per-member envelope encryption; this research says that is necessary but not sufficient, and names the missing pieces: online diarization (Sortformer), open-set UNKNOWN handling, hysteresis-based persistent tracking, and continuous rather than session-start authorization.
2. The hardest, unclaimed problem here is HIP's exact multi-member governance problem. "Whose utterance is this, which thread, which authorized context" is the same three-layer assignment that HIP's per-member fact graph and envelope encryption already partially address. HIP is not starting from zero; the fact graph is the context-isolation layer this research says is required.
3. The recommended stack is NVIDIA-native (NeMo Sortformer, TitaNet), which aligns with the existing enclave and partner relationship. Concrete first components to evaluate: TitaNet-Large or a WeSpeaker ResNet for enrolled voiceprints (both edge-viable on the Jetson), Sortformer for live tracks (RTX tier, unproven on Jetson).
4. The governance-defining line for HIP: authorization must occur outside the model, and voice identity is not sufficient authentication for high-impact actions. That is HIP's deterministic-control-plane thesis applied to the identity layer. The policy engine (Cedar-style ABAC) gating memory retrieval, tool execution and spoken disclosure is the concrete form the HIP control plane should take.
5. Open build requirement CHG-8 (biometric consent-and-retention controls, speaker_id.py writing .npz embeddings) is directly informed here: the stored voiceprint is biometric data, must be encrypted and access-controlled, and enrollment should capture multi-room, multi-condition samples with consensual periodic refresh. This research is the spec basis for CHG-8.

# Reference Sources

NeMo diarization intro: docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/speaker_diarization/intro.html
NeMo Streaming Sortformer 4spk: huggingface.co/nvidia/diar_streaming_sortformer_4spk-v2
NeMo diarization models: docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/speaker_diarization/models.html
EEND: arxiv.org/abs/2003.02966
pyannote segmentation (Bredin 2021): isca-archive.org/interspeech_2021/bredin21_interspeech.pdf
pyannote Community-1: huggingface.co/pyannote/speaker-diarization-community-1
TitaNet: arxiv.org/abs/2110.04410
TitaNet-Large weights: huggingface.co/nvidia/speakerverification_en_titanet_large
SpeechBrain ECAPA: huggingface.co/speechbrain/spkrec-ecapa-voxceleb
WeSpeaker ResNet293-LM: huggingface.co/Wespeaker/wespeaker-voxceleb-resnet293-LM
NeMo ECAPA NGC: catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/ecapa_tdnn
sherpa-onnx: k2-fsa.github.io/sherpa/onnx/index.html
FLEX-STB online EEND: arxiv.org/abs/2101.08473
VoiceFilter: google.github.io/speaker-id/publications/VoiceFilter/
Overlap separation/diarization: arxiv.org/pdf/2001.11482
