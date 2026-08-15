---
doc: HIP Voice Architecture Research
part: P2 of the voice architecture research set
topic: How full-duplex works at the model level
source: ChatGPT deep research output (prompt 2 of 8), reviewed and marked down
status: reference
version: v20260709_2157
location: ~/hip-dev/docs/voice-research/
---

# Full-Duplex Mechanics at the Model Level

A full-duplex conversational model does **not** literally perform one infinitely continuous neural computation in both directions. It runs a tightly pipelined causal loop on fixed-duration audio frames or chunks:

1. Encode the newest user-audio interval.
2. Append that representation to the model's persistent context or KV cache.
3. Predict the assistant's audio for a current or slightly future interval.
4. Decode and play that assistant audio.
5. While playback occurs, capture and encode the next user-audio interval.
6. Repeat five to twenty times per second.

At chunk `t`, the model is effectively computing:

```text
p_theta( y_t, a_t | u_<=t, y_<t, a_<t, c )
```

where:

* `u_t` : user-audio tokens or features for chunk t
* `y_t` : assistant speech tokens for chunk t, usually shifted slightly into the future
* `a_t` : optional control, planning, or tool-action tokens
* `c`   : system prompt, conversation history, visual context, retrieved information, and other persistent state

The input stream, output stream, and action stream are logically parallel. Internally, they are generally converted into either:

* a **vector of synchronized token streams per time step**, as in Moshi;
* a **single interleaved sequence of fixed-time blocks**, as in SyncLLM, BayLing-Duplex, and Thinking Machines' public description;
* or an **interleaved audio sequence plus a dedicated action channel**, as in DuplexSLA.

"Simultaneous" therefore means that capture, model inference, speech decoding, playback, and the next capture operation are overlapped in a streaming pipeline. There is still a causal delay of at least one frame or chunk.

---

## 1. The conversational clock

The fundamental design decision is to impose a model-visible clock.

A conventional speech system represents:

```text
complete user utterance
-> transcript
-> complete assistant response
-> speech
```

A full-duplex model instead represents something like:

```text
time 0: user_audio_0 | assistant_audio_0 | action_0
time 1: user_audio_1 | assistant_audio_1 | action_1
time 2: user_audio_2 | assistant_audio_2 | action_2
...
```

Silence is present in the training sequence. So are overlapping speech, abandoned words, backchannels, pauses and interruptions. The model does not merely see the order of sentences; it sees what each participant was doing during each wall-clock interval.

### Causal scheduling

Suppose the chunk duration is 200 ms. At the end of interval `t`, the model has received the complete user input for that interval. It can then generate assistant output for interval `t+1`:

```text
y_(t+1) ~ p_theta( y_(t+1) | u_<=t, y_<=t )
```

That gives a minimum algorithmic delay of approximately one chunk, before codec, network and compute delays.

Some systems predict the user's not-yet-complete current chunk to reduce the effective delay. SyncLLM, for example, predicts an estimate of the current user chunk, uses that estimate to generate the next assistant chunk, and later replaces the estimate with the actual user audio once it arrives. Its published format uses periodic synchronization and speaker tokens around fixed-duration HuBERT-token chunks.

A hard operational requirement follows:

```text
encoding time + model time + decoding time < chunk duration
```

on a sustained basis. If a 160 ms architecture repeatedly takes 220 ms to complete a step, its internal timeline falls behind real time.

---

# 2. Moshi: Parallel Streams Inside One Autoregressive Model

Moshi is the clearest published example of native audio-stream modeling.

## Audio representation

Moshi uses the Mimi neural audio codec. Each 80 ms frame is represented using `Q=8` codebooks:

* one relatively semantic codebook;
* seven additional acoustic codebooks carrying voice, prosody and signal detail.

The codec therefore operates at 12.5 frames per second.

A naive model could flatten all eight codebook tokens into one long sequence. That would multiply the effective autoregressive sequence length. Instead, Moshi uses an **RQ-Transformer** with two dimensions:

1. A large **Temporal Transformer** advances once per 80 ms frame.
2. A smaller **Depth Transformer** generates the multiple stream/codebook tokens associated with that frame.

For frame `s`, the Temporal Transformer produces a state `z_s = TemporalTransformer(V_<s)`. The Depth Transformer then predicts the tokens within frame s: `p(V_(s,k) | V_<s, V_(s,<k))`.

Thus the expensive transformer advances at 12.5 Hz, while the smaller depth model expands each temporal state into all required stream tokens.

## The 17 synchronized streams

Moshi jointly models:

* 1 assistant inner-monologue text stream;
* 8 assistant audio-codebook streams;
* 8 user audio-codebook streams.

That gives `K = 2Q + 1 = 17` streams per temporal frame.

At training time, the model predicts all 17. At inference time:

* assistant text and assistant audio predictions are sampled;
* predictions for the user stream are discarded;
* actual user-audio tokens are inserted in their place.

The model therefore receives real user speech continuously while continuing to generate its own speech. Overlap is not a special case: both audio tracks can contain non-silent codec tokens in the same frame.

Conceptually, one frame looks like:

```text
frame t
|-- assistant text token
|-- assistant semantic audio token
|-- assistant acoustic token 1
|-- ...
|-- assistant acoustic token 7
|-- user semantic audio token
|-- user acoustic token 1
|-- ...
|-- user acoustic token 7
```

The assistant-side tokens are generated. The user-side tokens are externally supplied.

## Inner monologue

Moshi places a time-aligned assistant text stream before its assistant audio streams in the depth ordering. That text token therefore conditions the semantic and acoustic speech tokens generated for the same general period.

This is not a hidden free-form chain of thought. It is a linguistic scaffolding corresponding to what Moshi is saying. It helps the model settle lexical content before producing lower-level speech tokens.

Moshi does not require an online transcript of the user. User meaning is extracted directly from user audio tokens. The paper explicitly avoids a user-text stream because that would require external streaming ASR and undermine the intended end-to-end design.

## Acoustic delay

Semantic decisions and detailed acoustic realization are difficult to make simultaneously. Moshi therefore delays the higher acoustic codebooks one or two frames behind the semantic codebook.

For an acoustic codebook `q > 1`: `V_(s,q) = A_(s-tau, q)`, where `tau` is commonly one or two 80 ms frames.

This gives the large Temporal Transformer extra future semantic context before it has to determine detailed voice realization. It also contributes to Moshi's roughly 160 ms theoretical and approximately 200 ms practical response latency.

---

# 3. What "Deciding Many Times Per Second" Actually Means

The phrase can describe two materially different mechanisms.

## A. Implicit interaction decisions

In original Moshi, many interaction decisions are expressed through ordinary audio and text-token probabilities, not through a named dialogue-state classifier.

### Listen or remain silent

The assistant emits:

* PAD tokens in its text stream;
* codec tokens that decode to natural near-silence.

Silence is not necessarily a single zero-valued audio token. It is a learned distribution of quiet-room audio, breathing, low-level noise and other near-silent codec states.

### Start speaking

The model transitions from PAD/silent audio to:

* linguistic text tokens;
* non-silent semantic and acoustic speech tokens.

The Moshi paper notes that forcing an `EPAD` text token can cause the model to begin speaking immediately, illustrating that text-stream padding and boundary tokens can influence speech onset.

### Yield during an interruption

While the assistant is speaking, new user tokens continue to enter every 80 ms. If those tokens indicate a meaningful barge-in, the conditional distribution for upcoming assistant frames shifts toward:

* terminating the current linguistic sequence;
* PAD or boundary tokens;
* silent audio tokens.

The audio already sent to the speaker cannot be withdrawn. Only future frames can be changed. Consequently, interruption latency is approximately:

```text
input frame wait + model inference + queued audio + output decoder buffering
```

### Backchannel

The model produces a brief non-silent assistant segment ("right," "mm-hm," "okay") while user audio remains active. Because the training representation contains both tracks, this is an ordinary learned joint pattern rather than a violation of a one-speaker-at-a-time state machine.

---

## B. Explicit state or action tokens

Other architectures make the interaction decision visible as a special token.

### Neural finite-state-machine approach

The 2024 *Full-duplex Speech Dialogue Scheme Based on Large Language Models* defines two dialogue states, `SPEAK` and `LISTEN`, and four transition tokens:

| Token        | Meaning                                                       |
| ------------ | ------------------------------------------------------------- |
| `[C.SPEAK]`  | Continue speaking despite incoming user audio                 |
| `[S.LISTEN]` | Stop speaking and yield                                       |
| `[C.LISTEN]` | Continue listening                                            |
| `[S.SPEAK]`  | Begin speaking, either after completion or as an interruption |

Streaming ASR chunks, generated text and these control tokens are serialized onto one causal token "tape." A generated text token is sent to streaming TTS; a control token changes the speech/listen state. The paper's implementation uses 640 ms ASR updates, so it is architecturally full-duplex but much coarser than Moshi's audio-native frame loop.

This approach explicitly separates:

* **content tokens**: what to say;
* **state-transition tokens**: whether to say it now.

### BayLing-Duplex

BayLing-Duplex uses a single autoregressive backbone with aligned user-audio, assistant-text and assistant-audio channels. Its text channel contains four state tokens:

* `[SILENCE]`: remain silent;
* `[ASSISTANT]`: start a reply;
* `[PAD]`: text generation is complete, but corresponding audio is still playing;
* `[EPAD]`: both text and speech are complete.

No additional turn-taking head is used. The state token, response text and assistant speech are all standard next-token predictions inside the same model sequence. The assistant channels are shifted one block ahead of the user channel to maintain causality.

This layout gives the model an explicit intermediate decision:

```text
[SILENCE]
```

versus:

```text
[ASSISTANT] Yes, that is correct ... [PAD] ... [EPAD]
```

That decision is repeated at each block boundary.

---

# 4. Speak, Pause, Interrupt and Backchannel Are Not the Same Decision

A binary speech detector is insufficient. A native full-duplex model ideally distinguishes at least the following:

| State/action               | Assistant audio              | Internal/action output         |
| -------------------------- | ---------------------------- | ------------------------------ |
| Continue listening         | Silence                      | `listen` or implicit silence   |
| Hold a deliberate pause    | Silence                      | Preserve pending response plan |
| Begin response             | Speech onset                 | `response` or start token      |
| Continue speaking          | Speech                       | Continue content generation    |
| Yield to user              | Transition to silence        | `interrupt`/yield token        |
| Ignore incidental barge-in | Continue speech              | Continue-speaking token        |
| Backchannel                | Brief speech                 | `backchannel`                  |
| Self-correct               | Stop/restart speech          | New content or repair marker   |
| Invoke tool                | Speech may continue or pause | Structured tool-call tokens    |

The distinction between **silence because the model has nothing to say** and **silence because it is deliberately waiting** matters. Without an explicit action or plan channel, both may look identical at the waveform level. The model must infer the difference from its hidden state.

---

# 5. Tool Calls Require a Second Output Plane

A tool call cannot be represented only as audible speech. The system needs machine-readable output that a runtime can intercept.

The clean formulation is `p_theta( y_t^audio, a_t^action | history )`, where the model jointly predicts:

* assistant speech for the conversational timeline;
* a structured action sequence for the orchestration runtime.

## DuplexSLA

DuplexSLA publishes a concrete three-channel design:

1. **User channel**: causal user-audio features.
2. **Assistant channel**: assistant text anchor plus discrete assistant-audio tokens.
3. **Action channel**: transcript fragments, planning text, turn-taking labels or structured tool calls.

All three are synchronized to the same fixed-size chunk clock and serialized inside one decoder context. Its action channel can emit labels such as response, interruption or backchannel, as well as delimited JSON-style tool calls. The action lane has a per-chunk token budget, allowing it to operate without blocking assistant speech generation.

A simplified model output might look like:

```text
CHUNK 184
assistant_audio:
    <audio tokens for "Let me check that">

action:
    <toolcall_begin>
    {"name":"calendar.search","arguments":{"date":"tomorrow"}}
    <toolcall_end>
    <action_end>
```

The runtime then:

1. recognizes the tool delimiters;
2. parses and validates the JSON;
3. dispatches the tool outside the model;
4. returns the result as a later model input;
5. lets the model decide when and how to weave the result into speech.

The model does not itself access the calendar or browser. It emits a symbolic request that the orchestration layer executes.

An important advantage is concurrency. The assistant can say "I'm checking your calendar" while the action channel emits the actual calendar query. It does not need to speak the JSON or stop audio generation to construct the call.

---

# 6. Thinking Machines Labs' Interaction-Model Design

Thinking Machines Labs describes a broader multimodal version of this architecture.

## Published mechanism

Its interaction model divides continuous input and output into **200 ms micro-turns**. The model receives an interleaved sequence:

```text
input_0, output_0,
input_1, output_1,
input_2, output_2,
...
```

Each input micro-turn can contain audio, video and text. Each output micro-turn can contain text and audio. At five micro-turns per second, silence, overlap, user movement, visual changes and assistant speech remain aligned to a shared clock.

Unlike Moshi, the published design does not describe a neural audio codec with multiple discrete codebooks. Thinking Machines says it uses:

* dMel audio features passed through a lightweight embedding;
* image patches passed through an hMLP;
* a shared Transformer;
* text unembedding for text output;
* a flow-based Mel audio head for speech output.

Those components are co-trained from scratch. The system keeps a persistent streaming sequence in GPU memory so each 200 ms request extends an existing KV context rather than rebuilding a new inference request.

## Interaction model plus background model

Thinking Machines separates two timescales:

* the **interaction model** maintains the 200 ms real-time loop;
* an asynchronous **background model** performs longer reasoning, search, browsing and tool workflows.

When the interaction model delegates work, it sends a rich conversation context to the background model. Results stream back, and the interaction model decides when to introduce those results into the live exchange. This avoids forcing a large reasoning model to meet every 200 ms deadline.

This means the complete Thinking Machines system is not literally one model doing everything. It is:

```text
real-time interaction model
        ^ shared context/results
asynchronous reasoning/tool model
```

The interaction model owns conversational timing. The background model owns work that cannot reliably finish within the conversational deadline.

## What Thinking Machines has not published

The public May 2026 description does **not** specify:

* an exact interaction-control vocabulary;
* whether `speak`, `yield`, `backchannel` or `delegate` have named special tokens;
* the exact serialization of simultaneous text and audio outputs;
* the training loss for silence versus speech;
* whether tool delegation is emitted through a structured token lane, a latent decision or a separate internal head;
* detailed training-data construction for interruptions and timing.

The company says dialogue management is implicit and that there is no separate dialogue-management component. Therefore, it would be unjustified to claim that its model uses specific control tokens analogous to BayLing's `[SILENCE]` or the neural FSM's `[S.LISTEN]`. Its published architectural clock is concrete; its exact action representation remains undisclosed.

---

# 7. How the Model Learns Timing Behavior

Ordinary next-token text training is insufficient. The training data and objective must preserve the wall-clock relationship between the two speakers.

## Stage 1: learn linguistic competence

Most published systems begin with either a pretrained text LLM, a speech-language model initialized from a text LLM, or (in Thinking Machines' case) a multimodal interaction model trained jointly from scratch.

Moshi initializes its Temporal Transformer from its Helium text model. It mixes text-only batches into later audio training to reduce catastrophic forgetting.

## Stage 2: learn audio tokens and text/audio alignment

The model learns to predict audio codec tokens, align linguistic text with speech frames, reconstruct or generate intelligible speech, and represent silence and timing.

Moshi randomizes the relative text/audio delay between -0.6 and +0.6 seconds during audio pretraining. This teaches the same architecture to support different causal relationships between text and speech. It also downweights the overwhelmingly common padding tokens so that "predict silence everywhere" does not dominate the loss.

## Stage 3: learn two synchronized speakers

The model needs aligned two-channel audio:

```text
channel A: user only, silence elsewhere
channel B: assistant only, silence elsewhere
```

That preserves onset and offset times, overlap, pauses, interruptions, backchannels, and failed turn entries.

Moshi constructs initial multistream data using diarization and later fine-tunes on natural two-channel conversational audio, including the Fisher telephone corpus. SyncLLM likewise uses separated real conversational channels after initial synthetic alignment training.

This stage teaches a conditional timing distribution:

```text
p( assistant starts at t | user audio through t, dialogue history )
```

not merely `p( assistant response text | finished transcript )`.

## Stage 4: synthetic interaction shaping

Real conversational recordings are limited and may not contain enough targeted behaviors. Training pipelines therefore synthesize examples containing frequent backchannels, interruptions at specific semantic moments, false starts, user corrections, short acknowledgments, topic shifts, environmental noise, and deliberate assistant interjections.

Moshi generates synthetic dialogues whose prompts explicitly request backchanneling and other conversational behavior. Its synthetic text is rendered with distinct assistant and user voices and aligned onto separate tracks.

The neural-FSM paper creates transcripts marked with the four control tokens at appropriate interruption and continuation points, then performs supervised fine-tuning so control decisions become ordinary next-token predictions.

## Stage 5: timing-specific supervised learning

For explicit-control architectures, the target data contains the state token at the correct wall-clock block:

```text
t=0.0  [SILENCE]
t=0.2  [SILENCE]
t=0.4  [SILENCE]
t=0.6  [ASSISTANT] I think-
t=0.8  ...
```

For an interruption:

```text
assistant speaking
user: "No, stop-"
model target at next available block:
    [S.LISTEN]
```

The loss is standard cross-entropy, but rare decision tokens often need reweighting. Otherwise, silence, padding and ordinary continuation overwhelm relatively rare interruption examples.

## Stage 6: preference training on timing

Timing can also be optimized through preference pairs where the words are held constant and only the onset or stopping time changes.

BayLing-Duplex constructs preferred and rejected examples that differ in assistant timing rather than semantic content. It uses supervised full-duplex examples followed by preference optimization so the model learns that:

* a response at 500 ms may be preferred to the same response at 1.5 seconds;
* stopping immediately after a meaningful user interruption is preferred to continuing;
* interrupting during an incomplete clause is worse than entering at an appropriate semantic boundary.

This is essential because conventional response-quality preference data is largely indifferent to whether the same answer started 300 ms or two seconds later.

## Stage 7: echo, noise and playback augmentation

Because the microphone hears the assistant's own speaker output, training or deployment must address acoustic echo. Otherwise, the model may interpret its own speech as a second user.

Approaches include:

* conventional acoustic echo cancellation;
* providing the model with a known assistant-output reference;
* training with delayed, reverberated assistant audio mixed into the user channel;
* random gain, noise and room impulse-response augmentation.

Moshi explicitly augments the user stream with delayed versions of Moshi's own output to improve robustness to playback leakage and reverberation.

---

# 8. Architectural Comparison

| System                | Time representation                                               | Assistant output                                  | Interaction control                                              | Tools                                                                       |
| --------------------- | ----------------------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Moshi**             | 80 ms frames; 17 parallel streams                                 | Text plus 8-codebook audio                        | Mostly implicit through PAD, boundary and audio tokens           | Not central to original architecture                                        |
| **SyncLLM**           | Fixed-duration interleaved speaker chunks, demonstrated at 160 ms | Discrete HuBERT speech units                      | Implicit from synchronized two-speaker generation                | Not a primary published mechanism                                           |
| **Neural FSM**        | Streaming ASR/text tape; 640 ms updates in implementation         | Text sent to TTS                                  | Four explicit state-transition tokens                            | Could be represented as text actions, but not its focus                     |
| **BayLing-Duplex**    | Aligned user audio, assistant text and assistant audio blocks     | Speech tokens conditioned by inner-monologue text | `[SILENCE]`, `[ASSISTANT]`, `[PAD]`, `[EPAD]`                    | Not the principal contribution                                              |
| **DuplexSLA**         | Fixed synchronized audio/action chunks                            | Assistant audio channel                           | Dedicated response, interruption and backchannel labels          | Structured calls on a parallel action channel                               |
| **Thinking Machines** | 200 ms multimodal input/output micro-turns                        | Text and flow-decoded audio                       | Publicly described as implicit; exact representation undisclosed | Asynchronous background model; exact delegation token mechanism undisclosed |

---

# Bottom Line

At the model level, full duplex requires four things:

1. **A clocked representation.** User speech, assistant speech, silence and actions must be aligned to fixed wall-clock intervals.
2. **Causal multistream conditioning.** Every new assistant frame is conditioned on the latest user frame as well as the assistant's own prior output.
3. **A learned output for interaction state.** This may be implicit (silence versus speech tokens) or explicit (`listen`, `speak`, `yield`, `backchannel` and tool-call tokens).
4. **Timing-preserving training data.** The model must be trained on synchronized dual-channel conversations and deliberately constructed interruption, overlap, pause, tool and backchannel examples.

The deepest architectural change is not audio input or low-latency TTS. It is that **conversational timing becomes part of the autoregressive prediction problem**. The model predicts not just what should eventually be said, but what its speech and action channels should contain during the next 80 to 200 milliseconds.

---

# HIP Relevance Notes

1. The tool-call mechanism (section 5, DuplexSLA) is the cleanest fit for HIP's governance posture: a **structured action channel separate from speech** is exactly where refusal strings, HITL gating, and per-member permission checks would attach. The action lane is interceptable and auditable in a way that speech tokens are not. If HIP goes full-duplex, the governance layer lives on the action plane, not inside the audio stream.
2. The inner-monologue text stream (Moshi) is a natural anchor point for HIP's fact-graph conditioning. A time-aligned assistant text stream that precedes audio generation is where retrieved facts and member context can be injected before the model commits to speech.
3. The "second output plane" requirement means HIP cannot bolt full-duplex onto the current cascade by swapping the STT/TTS ends. The action channel has to be trained or wired in from the architecture level, which is CC build territory, not a config change.
4. Sustained real-time constraint (`encode + model + decode < chunk duration`) is a hard hardware gate. On the RTX PRO 6000 target this is plausible for a 200 ms chunk; on Jetson Orin Nano Super it needs measurement before committing. This is the first thing to benchmark if the full-duplex path is pursued.

# Reference Sources

SyncLLM synchronous full-duplex dialogue agents: arxiv.org/html/2409.15594v1
BayLing-Duplex native full-duplex speech dialogue: arxiv.org/html/2606.14528
DuplexSLA full-duplex spoken language model with action: arxiv.org/html/2605.20755
Thinking Machines interaction models: thinkingmachines.ai/blog/interaction-models/
Moshi speech-text foundation model: arxiv.org/abs/2410.00037
