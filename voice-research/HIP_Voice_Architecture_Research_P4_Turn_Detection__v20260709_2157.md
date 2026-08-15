---
doc: HIP Voice Architecture Research
part: P4 of the voice architecture research set
topic: End-of-speech detection, endpointing, and turn-taking methods
source: ChatGPT deep research output (prompt 4 of 8), reviewed and marked down
status: reference
version: v20260709_2157
location: ~/hip-dev/docs/voice-research/
---

# Voice-AI End-of-Speech Detection

The core mistake is treating **"no speech is currently audible"** as equivalent to **"the user has yielded the conversational floor."** They are different classification problems:

* **VAD:** Is speech present in this audio frame?
* **Endpointing:** Has the current utterance ended?
* **Turn-taking:** Is it appropriate for the system to speak now?
* **Full-duplex control:** What should the system do at this instant: listen, remain silent, backchannel, answer, yield, or stop speaking?

The industry is moving from the first question toward the fourth.

## Comparison

| Method                             | Primary signal                                                              | Typical decision delay after speech | Thinking pauses                                                  | Background noise                                                             | Open implementations                                                       |
| ---------------------------------- | --------------------------------------------------------------------------- | ----------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Silence-based VAD                  | Speech/non-speech frames plus silence timer                                 | Usually **300 ms to 1+ sec**, dominated by timer | Poor; threshold determines how often users are cut off | Poor to moderate; noise may extend turns or generate false speech | WebRTC VAD, Silero VAD, TEN VAD                                            |
| Semantic endpointing               | Partial transcript, syntax, discourse context, predicted EOT token          | Model inference often **10 to 100 ms**, but STT and silence gating may add hundreds of ms | Much better when words reveal continuation | Degrades with ASR errors and competing speech | LiveKit text turn detector, TurnGPT, semantic-VAD research implementations |
| Prosody/audio turn models          | Pitch, rhythm, energy, duration, fillers, raw waveform, often semantics too | Potentially predictive; roughly frame-level to **100 ms**, though many systems still wait for a short pause | Better, especially for continuation intonation and fillers | Better than text-only if trained robustly, but far-field noise corrupts cues | VAP, Pipecat Smart Turn, LiveKit v1-mini                                   |
| Full-duplex continuous decisioning | Parallel user/system audio-token streams and learned conversational state   | No fixed endpoint timer; Moshi reports roughly **200 ms practical model latency** | Best architectural fit; pauses can remain part of an active turn | Still dependent on echo cancellation, source separation and training | Moshi, NVIDIA PersonaPlex                                                  |

These numbers are not directly comparable. A model may take only 12 ms to execute but still be invoked after 300 to 500 ms of observed silence. **Inference latency is not endpoint latency.**

---

# 1. Silence-Based VAD Endpointing

## How it works

A VAD classifies short frames as `P(speech | x_t)`. A state machine then applies smoothing or hysteresis:

1. Several positive frames start a speech segment.
2. Negative frames start a silence counter.
3. If silence exceeds a threshold (commonly several hundred milliseconds) the utterance is committed.
4. New speech before expiry resets the timer.

WebRTC VAD accepts 10, 20 or 30 ms PCM frames and produces a voiced/unvoiced decision. Silero processes approximately 30 ms or larger chunks in under 1 ms on a single CPU thread. Neither of those fast frame decisions determines whether the speaker's **thought** is complete; the application's trailing-silence policy does that.

A representative voice-agent configuration uses a minimum endpointing delay around 500 ms. LiveKit's current defaults without its audio turn detector allow the confirmation window to range from 0.5 to 3 seconds.

## Latency

The computation is nearly free. The latency is deliberately inserted:

```text
L_endpoint ~= L_frame + T_required_silence + L_smoothing
```

For a 500 ms silence threshold, the endpoint detector cannot reliably respond in less than roughly 500 ms, even if downstream processing is instantaneous.

Reducing the threshold creates premature interruptions. Increasing it creates dead air. This is not primarily a model-quality problem; it is an information problem. Silence duration by itself cannot distinguish:

* completed statement;
* word-retrieval pause;
* hesitation;
* breath;
* distraction by the physical task;
* interruption from another person;
* loss of microphone signal.

## False-trigger behavior

### Thinking pauses

This is the canonical failure. A user says:

> "Let me think about that..."

The semantics explicitly indicate continuation, but after 500 ms of silence a VAD-only system commits the turn.

Conversational speech includes pauses, lengthening, fillers, repetitions and other disfluencies. An integrated turn-taking study found that distinguishing hesitation from true completion was necessary to avoid cutting off natural speech; its joint ASR/turn model reported 97% recall, 85% precision and 100 ms latency on a disfluency-oriented test set.

### Background noise

Noise produces two opposite failures:

* **False speech:** Television dialogue, another household member, music or an appliance keeps resetting the silence timer. The agent never responds or responds very late.
* **False silence:** The target speaker's quiet or distant speech falls below the detector's confidence threshold, causing an early endpoint or missing the continuation.

Aggressiveness tuning simply shifts the error distribution. A more aggressive VAD rejects more noise but also rejects quiet, distant or atypical speech. A less aggressive VAD retains speech but admits more competing sounds.

## Open-source implementations

* **WebRTC VAD / py-webrtcvad:** Very small, deterministic and fast; 10/20/30 ms frames; useful as a baseline and speech gate.
* **Silero VAD:** MIT-licensed neural VAD, approximately 2 MB, portable through PyTorch and ONNX, with sub-millisecond processing for typical chunks.
* **TEN VAD:** Lightweight streaming neural VAD used in the TEN conversational-agent ecosystem.
* **Sherpa-ONNX endpointing:** Open local ASR with endpoint rules, although its conventional endpointing still commonly relies on trailing blank or silence output.

**Best use:** speech gating, wake-word follow-up, compute suppression and interruption onset, not final turn ownership.

---

# 2. Semantic Endpointing

## How it works

Semantic endpointing asks whether the recognized linguistic sequence appears complete: `P(end-of-turn | partial transcript, conversation context)`.

Implementations generally use one of three mechanisms.

### A. Transcript classifier

A small transformer receives the latest partial transcript and sometimes preceding dialogue. It predicts complete versus incomplete.

The open LiveKit text turn detector formats recent conversation history, leaves the final user message unclosed, and predicts the probability that an end-of-message token should come next. Per-language thresholds convert that probability into an endpoint decision.

### B. Next-token prediction

Models such as TurnGPT are trained so that turn-transition tokens become predictable from syntactic, semantic and pragmatic completeness. They can also project likely completion before the acoustic endpoint.

### C. Joint ASR endpoint token

The streaming recognizer is trained to emit states such as speech, hesitation or `<pause>`, and completed turn or `</s>`. This gives the endpoint model access to acoustic encoder features and linguistic decoder state. The Google turn-taking work used this structure to distinguish pauses from true completion.

Semantic VAD research has also added frame-level punctuation and an explicit artificial-endpoint class to a VAD/ASR objective. One published system reduced average segmentation latency by 53.3% relative to its conventional VAD baseline without a material character-error-rate penalty.

## Latency

A compact semantic model may execute in tens of milliseconds, but the complete path is:

```text
L_semantic_EOT = L_streaming_ASR + L_transcript_stabilization + L_EOT_model + L_confirmation_policy
```

Text endpointing can therefore be slower than its benchmarked classifier runtime suggests. It may wait for the recognizer to emit or stabilize the last word. If it is invoked only after VAD detects silence, its latency is additive to the silence trigger.

Streaming joint-ASR models can reduce that penalty because they update endpoint probabilities as audio arrives rather than waiting for a finalized transcript.

## False-trigger behavior

### Thinking pauses

Semantic models are materially better when the words indicate an unfinished thought:

* "I have three things..."
* "The address is..."
* "Give me a second..."
* "I need the flight from Denver to..."
* conjunctions, subordinate clauses and incomplete lists.

They can hold the floor even during a long silence.

### Their hard limit

Text alone cannot resolve cases where identical words have different vocal delivery:

> "I'd like one large pizza..."

That could be complete or the first item in a longer order. Pitch movement, rhythm and final-syllable treatment may carry the distinction. LiveKit moved from transcript-based models to combined audio-semantic models specifically because transcription removes those signals and adds STT-dependent delay.

### Background noise

Semantic endpointing is vulnerable indirectly:

* Noise corrupts the transcript.
* Competing speakers merge into one transcript.
* A television may produce a perfectly complete sentence, causing a confident but irrelevant turn.
* Partial-ASR revisions can make the endpoint score oscillate.
* Unsupported dialects, code-switching or names can resemble syntactic incompleteness.

Semantics answers **whether an utterance is complete**, not **whose utterance it is**.

## Open implementations

* **LiveKit text turn detector:** Open-weight quantized ONNX model operating on transcript context; integrates with Silero VAD.
* **TurnGPT:** Open research implementation for language-model-based turn-shift prediction.
* **Sherpa-ONNX:** Useful for building streaming ASR endpoint-token or blank-token systems locally.
* **Phoenix-VAD:** Published streaming LLM-based semantic endpoint module using sliding-window inference, but its practical openness should be checked at the code/weight level rather than inferred from the paper alone.

---

# 3. Prosody-Based and Audio-Semantic Turn Models

## How they work

Prosody models consume acoustic evidence that text discards, including:

* fundamental-frequency movement;
* final pitch rise or fall;
* energy decay;
* final-syllable lengthening;
* speaking-rate changes;
* rhythm;
* breath and phonation;
* filled pauses;
* temporal spacing;
* overlap and backchannel patterns.

Older systems extracted handcrafted features. Newer systems feed raw or encoded waveforms into causal neural networks.

There are two significant forms.

## A. End-of-turn classifier

A model receives the current audio segment and predicts `P(complete | waveform)`.

Pipecat Smart Turn is a native-audio model used alongside a lightweight VAD. It evaluates PCM audio during pauses, using linguistic and acoustic information rather than a transcript alone. Version 3.2 is BSD-licensed and publishes model weights, datasets and training scripts. Its repository reports approximately 10 ms on some CPUs and under 100 ms on most cloud instances.

The published v3 benchmark reports:

* 8 MB quantized CPU model;
* approximately 12 ms on a modern CPU;
* approximately 60 ms on a low-cost cloud instance;
* preprocessing included;
* support for 23 languages.

Again, that is classifier runtime. Smart Turn is normally invoked after VAD identifies a pause, so total endpoint latency includes the pause required to trigger it.

LiveKit's newer architecture processes audio through parallel branches:

* an audio-to-language semantic branch;
* an acoustic encoder and recurrent layer for timing and prosody;
* a fusion module producing the endpoint probability.

Its `v1-mini` is open-weight and intended for local CPU inference.

## B. Future voice-activity projection

Voice Activity Projection, or VAP, does not simply classify "done." It continuously predicts which participant will be active over a future window.

The open VAP model is causal and incremental. It maps the conversational history into a probability distribution over future two-speaker activity for the next two seconds, divided into progressively larger time bins. This supports prediction of:

* turn continuation;
* turn shift;
* backchannel opportunity;
* overlap;
* pause versus yield.

The available implementation uses a speech encoder and GPT-like causal transformer, with frame-level operation at 50 Hz in its published configuration.

## Latency

Prosody models can make useful predictions **before a long silence exists**. That is their major architectural advantage.

A causal audio model may update every 20 to 40 ms and forecast a likely turn transition. The system can prepare a response speculatively while waiting for stronger evidence.

Published end-to-end work combining acoustic and linguistic cues has demonstrated turn-taking decisions at 100 ms latency.

Practical latency nevertheless depends on policy:

* A predictive system can start preparation before speech ends.
* A conservative system may still require 200 to 300 ms of silence.
* A segment classifier may be fast but invoked only after VAD fires.
* A continuous VAP-style system does not require a discrete invocation point.

## False-trigger behavior

### Thinking pauses

Prosody helps distinguish:

* a continuation rise from terminal falling intonation;
* hesitation lengthening from final lengthening;
* a filled pause from a completed phrase;
* a held floor from a yielded floor.

VAP experiments found that learned turn models use prosodic information even without explicit hand-engineered prosody features.

### Failure modes

Prosody is not universal:

* Intonation varies by language and dialect.
* Questions may have falling or rising contours depending on speaker and language.
* Emotion, fatigue and speech impairment alter pitch and timing.
* Far-field reverberation smears energy and timing cues.
* Noise suppression can distort pitch and word endings.
* A speaker may sound terminal while remaining semantically incomplete.
* Backchannels such as "yeah" may resemble complete turns acoustically.

The strongest practical systems therefore fuse **semantics and prosody**, rather than treating either as sufficient.

## Open implementations

* **Voice Activity Projection:** MIT-licensed implementation with pretrained model state and inference code; training-data dependencies are less completely open.
* **Pipecat Smart Turn v3.2:** BSD-2-Clause; open weights, data, training and inference.
* **LiveKit Turn Detector v1-mini:** Open-weight local CPU model using fused semantic and acoustic audio branches.
* **Continuous Turn-Taking RNN:** MIT-licensed reimplementation of earlier continuous transition-relevance-point modeling.

---

# 4. Full-Duplex Continuous Decisioning

## What "eliminating turn detection" actually means

Full duplex does **not** eliminate the need to decide when the system should speak. It eliminates a separate, irreversible **end-of-user-turn gate**.

A turn-based pipeline looks like:

```text
user audio
   v
VAD declares endpoint
   v
ASR finalizes
   v
LLM runs
   v
TTS speaks
```

A full-duplex model maintains concurrent streams:

```text
user audio tokens -------------->
                         shared causal model state
system audio tokens <--------------
```

At each audio-token interval, the model effectively selects among behaviors such as:

* produce silence;
* continue listening;
* emit a backchannel;
* begin a substantive response;
* continue speaking;
* stop speaking because the user interrupted;
* overlap briefly;
* yield the floor.

The user is never globally marked "finished." Instead, the probability of each system behavior evolves continuously.

## Moshi mechanism

Moshi represents the user's speech and the model's own speech as parallel audio-token streams generated from a neural audio codec. It also generates time-aligned internal text tokens (its "inner monologue") ahead of acoustic tokens. Because both speaker streams remain active, interruptions, overlaps and interjections are represented directly rather than forced into alternating segments.

Moshi reports:

* theoretical latency: **160 ms**;
* practical latency: approximately **200 ms**;
* open implementation.

NVIDIA PersonaPlex is based on Moshi's architecture and weights, adding role and voice conditioning while retaining simultaneous listening and speaking.

## Latency

There is no mandatory 500 ms endpoint timeout. The model can:

1. infer a probable response while the user is still talking;
2. emit silence until confidence rises;
3. start speaking immediately after a projected transition;
4. stop if new user audio indicates interruption.

That produces low apparent response gaps without requiring reckless early commitment.

The reported 200 ms figure for Moshi is model-streaming latency, not a guarantee that every answer begins 200 ms after the user's last phoneme. The learned policy may deliberately wait, backchannel or remain silent.

## False-trigger behavior

The binary errors of endpointing become continuous behavioral errors:

| Turn-based error       | Full-duplex analogue                           |
| ---------------------- | ---------------------------------------------- |
| Premature endpoint     | Agent begins talking too early                 |
| Delayed endpoint       | Agent remains silent too long                  |
| False speech detection | Agent attends to irrelevant speaker/noise      |
| Missed interruption    | Agent continues talking over user              |
| Wrong backchannel      | Agent emits "uh-huh" at an inappropriate point |
| Fragmented turns       | Agent repeatedly starts and stops              |

Full duplex makes errors more recoverable (the model can stop speaking) but does not make them disappear.

Recent work specifically identifies excessive silence and mistimed interaction as remaining issues in full-duplex models. A 2026 alignment study applied separate reinforcement-learning objectives for pause handling, turn-taking, backchanneling and user interruption to Moshi and PersonaPlex.

## Open implementations

* **Kyutai Moshi:** Open code and model ecosystem for speech-text full-duplex dialogue.
* **NVIDIA PersonaPlex:** Public code and weights under a model-specific license; real-time full-duplex speech-to-speech.

These are substantially more computationally demanding and operationally less predictable than VAD-plus-pipeline systems.

---

# Why Silence Endpointing Fails in Homes

Home interaction violates nearly every assumption behind a fixed silence timer.

## 1. Silence is not controlled

In a call center, a close microphone captures one person under relatively constrained conditions. In a home, the acoustic field contains:

* television dialogue;
* music;
* children and other adults;
* kitchen appliances;
* water, ventilation and cleaning equipment;
* room reverberation;
* the assistant's own loudspeaker output;
* speech arriving from different distances and directions.

A generic VAD detects **speech**, not the intended speaker or addressee. Speaker-conditioned VAD research exists precisely because standard VAD cannot distinguish target speech from non-target speech at the frame level.

## 2. Household speech is not a prepared command

Users speak while cooking, repairing something, carrying a child, dressing, driving, searching a drawer, looking at a label, calculating quantities, or coordinating with another person.

These activities create planning pauses:

> "Set a timer for... hold on, I need to see the package... twelve minutes."

Higher cognitive load increases spoken hesitation frequency, including silence, fillers and lengthening. A fixed timer interprets precisely those task-induced hesitations as turn completion.

## 3. Hands-occupied users cannot repair through the screen

In a desktop interface, an erroneous submission can be corrected with a keyboard or button. In a kitchen, workshop, vehicle or caregiving situation:

* push-to-talk is unavailable;
* a "continue speaking" button defeats the point;
* touching the screen may be unsafe or impossible;
* the user may not be facing the device;
* visual feedback may be invisible.

The cost of a premature endpoint is therefore higher. The user must verbally stop the assistant, repeat the command and reconstruct context.

## 4. There is no usable universal threshold

Consider a fixed threshold `T`:

* Small T: low response latency, frequent cutoffs.
* Large T: fewer cutoffs, conspicuous dead air.
* Persistent noise: timer may never reach T.
* Quiet continuation: timer reaches T despite ongoing intent.

No threshold resolves this because the relevant variable is **intent to continue**, not silence duration.

## 5. Homes are multi-party environments

A household member may say "yeah" to another person while the primary user is speaking to the assistant. A child may answer a question addressed to a parent. Someone may interrupt with relevant information.

A VAD-plus-timer architecture has no representation of target speaker, addressee, conversational floor, side conversation, backchannel, collaborative completion, or interruption priority.

This is a conversation-state problem, not an acoustic-segmentation problem.

---

# What Replaces Silence-Based Turn Detection

For deployable systems, the replacement is not one model. It is a layered **continuous floor-management stack**.

## Near-Term Production Architecture

```text
Microphone array
    |
    |- acoustic echo cancellation
    |- beamforming / source separation
    |- noise suppression
    |- speaker-conditioned speech activity
                 |
                 v
       streaming audio + partial ASR
                 |
        +--------+---------+
        | semantic cues    |
        | prosodic cues    |
        | speaker identity |
        | dialogue state   |
        | task context     |
        +--------+---------+
                 v
       continuous floor controller
                 |
   LISTEN / HOLD / BACKCHANNEL / RESPOND
        / YIELD / INTERRUPT / ABORT
```

### 1. VAD remains, but is demoted

VAD continues to provide speech onset, compute gating, interruption candidates, audio segmentation hints, and wake-session timeout. It no longer has unilateral authority to close the turn.

### 2. Target-speaker and source filtering

A home system needs some combination of microphone-array beamforming, acoustic echo cancellation, speaker embeddings, target-speaker VAD, source separation, and addressee or wake-word context. This addresses the problem that television speech and household speech may both be genuine human voice activity.

### 3. Joint semantic-prosodic endpoint probability

The system continuously estimates:

```text
P( yield | audio, partial words, prosody, speaker, dialogue history, current task )
```

A pause after "let me check" should produce a low yield probability. A falling contour after a semantically complete direct command should produce a high one.

### 4. Multi-action output, not binary output

A useful controller should classify more than continue/end:

* **HOLD:** User retains floor despite silence.
* **BACKCHANNEL:** Give a short acknowledgment without taking the floor.
* **RESPOND:** Begin substantive output.
* **CLARIFY:** The user appears finished but the request is incomplete.
* **YIELD:** Stop because the user interrupted.
* **IGNORE:** Speech belongs to another source or conversation.

VAP-style models and full-duplex speech models are structurally closer to this requirement than endpoint classifiers.

### 5. Speculative but cancelable response preparation

The system can begin LLM inference, retrieval, tool planning, or response drafting before it commits to audible output. If the user continues, the speculative work is canceled or updated. This reduces apparent latency without speaking prematurely.

### 6. Native barge-in

Once the assistant starts speaking, the input side must remain active. A new target-speaker signal should be classified as backchannel, correction, interruption, or unrelated background speech. Stopping TTS whenever any voice is detected merely transfers the same VAD problem from endpointing to interruption handling.

---

# Bottom Line

**Silence-only endpointing is acceptable for short, rehearsed commands in controlled audio. It is fundamentally inadequate for natural household conversation.**

The practical migration path is:

1. **VAD plus fixed timer** : cheapest, brittle.
2. **VAD plus transcript-semantic endpointing** : fewer thinking-pause interruptions.
3. **Audio-semantic/prosodic turn prediction** : better timing and lower STT dependency.
4. **Continuous floor controller** : multiple conversational actions rather than binary completion.
5. **Full-duplex speech-native model** : removes the discrete endpoint as a system boundary.

For a home system, the most defensible current design is **speaker-aware acoustic processing plus continuous fused semantic/prosodic turn prediction**, with VAD used only as a low-level signal. Full duplex is the destination, but current full-duplex models still require stronger reasoning, tool integration, household speaker attribution and behavioral alignment before they can replace the entire production stack.

---

# HIP Relevance Notes

1. This is the most immediately actionable document for the current prototype. The prototype's voice path uses silence-based endpointing (the Whisper cascade). Section "Why Silence Endpointing Fails in Homes" is a precise diagnosis of why that path breaks in HIP's actual target environment, and it is not a tuning problem, it is an architecture problem.
2. The five-step migration path is a concrete roadmap. HIP does not need to jump to full-duplex to get a large win. Moving from step 1 (VAD + fixed timer) to step 3 (audio-semantic/prosodic turn prediction) using open components (Pipecat Smart Turn v3.2, LiveKit v1-mini, VAP) is a bounded, testable upgrade that runs on CPU and does not require retraining a speech model.
3. The multi-party home problem maps directly onto HIP's multi-member governance model. "Whose utterance is this" is the same question as "which member's context and permissions apply." Target-speaker VAD and speaker embeddings are the acoustic-layer version of the voiceprint identity kernel already in the HIP design. The turn-detection stack and the identity kernel should be designed together, not separately.
4. The "continuous floor controller" with multi-action output (LISTEN/HOLD/BACKCHANNEL/RESPOND/YIELD/IGNORE) is the near-term target for HIP's interaction layer, achievable without a monolithic full-duplex model. IGNORE (speech belongs to another source) is where governance and identity gate the acoustic stream before anything reaches the reasoning cascade.
5. Concrete open components to evaluate on the edge hardware: Silero VAD (2 MB, sub-ms), Pipecat Smart Turn v3.2 (8 MB, ~12 ms CPU, BSD, 23 languages), LiveKit v1-mini (fused semantic/acoustic, local CPU), VAP (MIT, causal, predictive). All CPU-viable, which matters for the Jetson tier.

# Reference Sources

py-webrtcvad: github.com/wiseman/py-webrtcvad
LiveKit turn detector docs: docs.livekit.io/agents/logic/turns/turn-detector/
Turn-taking prediction for conversational speech: arxiv.org/abs/2208.13321
Silero VAD: github.com/snakers4/silero-vad
TEN VAD: github.com/ten-framework/ten-vad
Sherpa-ONNX endpoint example: github.com/k2-fsa/sherpa-onnx
LiveKit turn-detector weights: huggingface.co/livekit/turn-detector
TurnGPT paper: arxiv.org/abs/2010.10874
Semantic VAD low-latency: arxiv.org/abs/2305.12450
LiveKit end-of-turn detection v1.0: livekit.com/blog/solving-end-of-turn-detection
TurnGPT repo: github.com/ErikEkstedt/TurnGPT
Sherpa-ONNX docs: k2-fsa.github.io/sherpa/onnx/
Phoenix-VAD streaming semantic endpoint: arxiv.org/abs/2509.20410
Pipecat Smart Turn: github.com/pipecat-ai/smart-turn
Smart Turn v3 announcement: daily.co/blog/announcing-smart-turn-v3-with-cpu-inference-in-just-12ms/
VAP project page: erikekstedt.github.io/VAP/
Voice Activity Projection repo: github.com/ErikEkstedt/VoiceActivityProjection
How much does prosody help turn-taking: arxiv.org/abs/2209.05161
Continuous Turn-Taking RNN: github.com/mumair01/Continuous-Turn-Taking-RNN
Moshi paper: arxiv.org/abs/2410.00037
NVIDIA PersonaPlex: github.com/NVIDIA/personaplex
Multi-faceted interactivity alignment in full-duplex: arxiv.org/abs/2606.11167
Personal VAD speaker-conditioned: arxiv.org/abs/1908.04284
Cognitive load and hesitation frequency (MDPI): mdpi.com/2226-471X/8/1/71
