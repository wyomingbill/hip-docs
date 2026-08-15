---
doc: HIP Voice Architecture Research
part: P1 of the voice architecture research set
topic: Cascaded vs turn-based audio-native vs continuous full-duplex
source: ChatGPT deep research output (prompt 1 of 8), reviewed and marked down
status: reference
version: v20260709_2154
location: ~/hip-dev/docs/voice-research/
---

# Voice Architecture Taxonomy: Cascaded vs Turn-Based vs Full-Duplex

The three architectures differ less in whether audio is streamed than in **where conversational state and turn control live**:

1. **Cascaded:** audio is converted into text, reasoned over as text, then resynthesized.
2. **Turn-based audio-native:** one multimodal model consumes and emits audio, but an external or internal end-of-turn decision still gates response generation.
3. **Full-duplex:** the system continuously models inbound and outbound speech as concurrent streams; listening does not stop when speaking begins.

A bidirectional WebSocket or WebRTC connection does **not** by itself make a system full-duplex. Many systems stream audio in both directions but still execute a half-duplex state machine: `LISTEN -> ENDPOINT -> THINK -> SPEAK -> LISTEN`.

## Summary matrix

| Property                   | Cascaded STT to LLM to TTS                          | Turn-based audio-native                                                    | Continuous full-duplex                                               |
| -------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Core representation        | Text between components                             | Shared speech/text latent or audio-token model                             | Time-aligned concurrent user/system streams                          |
| Turn boundary              | VAD, endpointing, semantic EOU                      | Usually VAD or model EOU prediction                                        | No mandatory utterance boundary                                      |
| Can listen while speaking? | Usually only through a separate barge-in controller | Often captures audio, but generation is canceled/restarted on interruption | Yes; inbound audio conditions generation continuously                |
| Typical response onset     | Roughly 0.7 to 2.5+ s after endpoint                | Roughly 0.4 to 1.4 s after endpoint in disclosed systems                   | Approximately 0.2 s demonstrated by Moshi                            |
| Semantic intelligence      | Usually strongest; arbitrary text LLM               | Strong, but model-dependent                                                | Currently generally weaker than frontier text-centered stacks        |
| Prosody retention          | Mostly lost at STT boundary                         | Potentially retained                                                       | Retained continuously                                                |
| Observability              | Excellent                                           | Moderate                                                                   | Poorer; internal speech-token state is harder to audit               |
| Tool/RAG integration       | Straightforward                                     | Supported, but tool latency creates awkward silence                        | Architecturally difficult; often requires asynchronous side channels |
| Production maturity        | High                                                | High and growing                                                           | Early; limited commercially verified deployment                      |

Latency figures are not directly comparable across vendors. Some report network-inclusive time to first audio; others report model-only latency, and some measure from **end of detected speech**, which excludes the endpointing delay itself.

---

# 1. Cascaded STT to LLM to TTS

## Pipeline wiring

A production cascade typically looks like:

```text
Microphone
   |
   v
AEC / noise suppression / AGC
   |  10 to 20 ms audio frames
   v
Streaming VAD + streaming ASR
   |
   |-- partial hypotheses --------------|
   |                                    |
   |-- final transcript after endpoint  v
                                dialogue manager
                                      |
                         prompt + tools + memory
                                      |
                                      v
                               text-token LLM
                                      |
                       sentence/clause text chunks
                                      |
                                      v
                                streaming TTS
                                      |
                                      v
                          jitter buffer / playback
```

Separate paths usually handle:

* echo cancellation;
* wake-word detection;
* speaker identification;
* endpointing;
* interruption detection;
* transcript revision;
* tool calls;
* playback cancellation.

The system may overlap stages. For example, partial ASR can be passed to the LLM before the utterance is finalized, and TTS can begin after the first complete clause rather than waiting for the entire answer. A producer-consumer implementation can run LLM generation and TTS concurrently.

## Latency budget

A well-optimized cloud cascade can target the following **engineering budget**:

| Component                        |       Aggressive target | Common source of tail latency     |
| -------------------------------- | ----------------------: | --------------------------------- |
| Audio capture/frame accumulation |                10-40 ms | Large client chunks               |
| Uplink and media ingress         |               20-100 ms | Cellular routing, TURN relays     |
| AEC/noise processing             |                 5-30 ms | Long filter windows               |
| Streaming ASR partial decoding   | 50-250 ms behind speech | Beam size, model size             |
| End-of-turn silence              |              200-800 ms | Conservative endpointing          |
| ASR finalization/revision        |               50-300 ms | Re-decoding unstable suffix       |
| LLM first token                  |             100-800+ ms | Model size, queueing, long prompt |
| Text chunk accumulation for TTS  |               40-300 ms | Waiting for sentence boundary     |
| TTS first audio                  |               75-400 ms | Non-streaming vocoder or cloning  |
| Downlink/playout buffer          |               20-100 ms | Jitter protection                 |

A realistic optimized response can therefore start around **600 to 1,200 ms after the acoustic end of speech**. Less optimized or reasoning-heavy systems commonly exceed 1.5 to 3 seconds.

The largest controllable delay is often not ASR inference but **endpointing**. Silence-based endpointing must wait long enough to distinguish a completed turn from a hesitation. This produces the fundamental trade-off:

```text
short silence threshold -> lower latency, more premature cutoffs
long silence threshold  -> fewer cutoffs, slower response
```

Amazon Nova's turn-taking documentation illustrates the scale of this problem: its high-sensitivity setting still uses a reported 1.5-second pause duration, although that parameter applies to Nova Sonic rather than a classic cascade.

## Information lost between stages

The hard information bottleneck is the transcript:

```text
audio waveform -> word sequence
```

A conventional transcript generally discards or weakly represents:

* pitch contour;
* speech rate and timing;
* hesitation length;
* loudness;
* breathiness;
* laughter and sighs;
* sarcasm;
* emotional intensity;
* overlapping speakers;
* uncertainty carried through delivery;
* pronunciation evidence relevant to names;
* exact alignment between words and interruptions.

Some information can be reattached as metadata:

```json
{
  "text": "That's fine",
  "confidence": 0.79,
  "emotion": "frustrated",
  "start_ms": 8120,
  "end_ms": 9340
}
```

But those labels are lossy estimates produced by additional models. They are not equivalent to giving the reasoning model access to the original signal.

The TTS boundary causes a second loss. The LLM emits lexical text, and the TTS model invents a delivery. Unless the system explicitly passes style, timing and emphasis controls, the generated voice is not a continuation of the reasoning model's internal interpretation of the user's prosody.

## Failure modes

### Noise and cross-talk

ASR errors become authoritative text. The LLM usually has no acoustic evidence with which to reconsider them.

Example:

```text
Audio: "Cancel order sixty, not sixteen."
ASR:   "Cancel order sixteen."
LLM:   Acts on the wrong order.
```

Confidence scores help, but confidence calibration is imperfect, especially for names, codes and domain terminology.

### Endpointing on hesitation

A user says:

> "I need you to transfer... [500 ms pause] ...the balance, not close the account."

A short endpoint threshold can finalize after "transfer," causing the LLM to start answering or acting before the correction arrives.

### Partial-transcript instability

Streaming ASR may revise the trailing words:

```text
partial 1: "book a flight to Portland Maine"
partial 2: "book a flight to Portland, May..."
final:     "book a flight to Portland May third"
```

Starting the LLM from unstable partials reduces latency but requires:

* rollback;
* speculative decoding;
* cancellation;
* transcript-delta reconciliation.

Otherwise, the model can commit to an interpretation that no longer matches the finalized transcript.

### Barge-in false positives

While TTS is playing, microphone audio contains:

```text
user speech + loudspeaker leakage + room echo + background speech
```

Without strong acoustic echo cancellation, the system may detect its own voice as an interruption. With aggressive suppression, it may erase the user's voice when the user talks over the system.

### Interrupted output and conversation state

The application must track how much speech the user actually heard. The LLM may have generated an entire answer, while playback stopped after the first sentence. If the complete answer is stored in history, the model incorrectly assumes the user heard it.

### Error multiplication

Errors propagate serially:

```text
ASR error
  -> wrong LLM interpretation
     -> fluent TTS rendering of the wrong answer
```

Fluent output can make upstream recognition errors harder for users to detect.

## Production systems

Cascades remain the standard architecture behind many contact-center and custom voice-agent stacks because they allow independent selection of:

* telephony/media layer;
* ASR vendor;
* reasoning model;
* TTS voice;
* compliance transcript;
* tool orchestration.

OpenAI's request-based transcription, text-generation and speech APIs can be wired this way; OpenAI distinguishes these bounded audio APIs from its native Realtime architecture.

Google Cloud Speech-to-Text exposes streaming recognition and real-time voice-activity events suitable for cascade endpointing.

The production advantage is not conversational naturalness. It is **control, inspectability and replaceability**.

---

# 2. Turn-Based Single Audio-Native Models

## Pipeline wiring

Here the central model accepts speech representations directly and emits speech representations directly:

```text
Microphone
   |
   v
AEC / denoise / resample
   |
   v
speech encoder or audio tokenizer
   |
   v
unified multimodal transformer
   |
   |-- optional transcript
   |-- text/tool tokens
   |-- acoustic/codec tokens
           |
           v
       audio decoder
           |
           v
        playback
```

However, the runtime still has a turn controller:

```text
LISTEN
  |
  |-- VAD sees speech
  |
  |-- VAD or semantic EOU sees completion
          |
          v
       GENERATE
          |
          v
        SPEAK
```

The model may receive streaming audio continuously, but meaningful response generation is normally triggered after:

* a silence threshold;
* an explicit `ActivityEnd`;
* a semantic end-of-utterance prediction;
* a client-issued commit.

OpenAI's Realtime API defaults to `server_vad`, which chunks the stream after periods of silence. It also offers `semantic_vad`, where a model estimates whether the user has completed the utterance.

Gemini Live similarly supports default VAD or application-supplied `ActivityStart` and `ActivityEnd` events.

## What "single model" means, and does not mean

"Audio-native" does not necessarily mean that every operation occurs in one homogeneous neural network. A deployed system may still contain:

* a neural audio codec;
* an audio encoder;
* a multimodal transformer;
* separate text and acoustic output heads;
* a vocoder;
* external VAD;
* policy and safety layers;
* tool orchestration.

The important distinction is that semantic reasoning is not restricted to an externally finalized transcript. The model can condition on richer speech representations and may jointly model text and audio outputs.

## Latency budget

A typical turn-based native system still pays:

| Component                         |      Approximate range |
| --------------------------------- | ---------------------: |
| Audio framing and uplink          |              30-150 ms |
| Streaming audio encoding          | 20-100 ms behind input |
| End-of-turn detection             |          200-1,500+ ms |
| Model prefill / response planning |             100-500 ms |
| First speech-token decoding       |              50-300 ms |
| Codec/vocoder buffering           |              40-160 ms |
| Downlink/playout                  |              20-100 ms |

The elimination of explicit STT-finalization and text-to-TTS handoff can save hundreds of milliseconds. But the system does **not** eliminate end-of-turn latency when it remains turn-gated.

AWS reported approximately **1.09 seconds time to first audio**, measured from completion of the user's query to receipt of response audio, for one Nova Sonic evaluation. A separate Nova 2 Sonic deployment reported 1.39 seconds. These figures include model/system behavior but should not be treated as universal model-only numbers.

The main latency benefit comes from:

* no ASR-final transcript barrier;
* no textual handoff into a separate LLM request;
* no separate TTS service request;
* joint or closely coupled semantic/acoustic decoding;
* persistent session state;
* streaming speech-token output.

## Information preserved and lost

Compared with a text cascade, an audio-native model can retain:

* intonation;
* emotional expression;
* timing;
* emphasis;
* hesitation;
* vocal effort;
* speech rate;
* laughter or nonverbal vocalizations;
* potentially speaker characteristics.

Gemini Native Audio explicitly exposes affective dialogue and native audio processing rather than forcing all understanding through a text transcript.

OpenAI describes Realtime conversations as voice-to-voice interaction without an intermediate application-level STT or TTS step.

What remains lost or distorted:

* codec quantization removes waveform detail;
* model input windows may downsample timing;
* stereo spatial information may be collapsed;
* overlapping voices may be entangled;
* explicit transcripts may not exactly match what the model acoustically inferred;
* generated speech may be conditioned on an internal text plan, even when no external transcript boundary exists.

Thus "native audio" removes the **text API bottleneck**, not all intermediate representation loss.

## Failure modes

### Silence-based false endpoint

Native speech understanding does not fix a poor VAD threshold. A model can understand prosody perfectly and still be triggered too early by an external silence detector.

### Semantic endpoint errors

Semantic VAD reduces sensitivity to ordinary pauses but introduces a different failure mode: it can infer that a grammatically complete phrase is a complete turn even when discourse context says otherwise.

Example:

> "There are three things. First, cancel the card."

The sentence is complete, but the user may be about to give items two and three.

### Interruption implemented as cancellation

Many systems described as allowing "barge-in" do not continuously reason over overlapping speech. Instead:

1. VAD detects user speech during system playback.
2. Current generation is canceled.
3. Unplayed output is discarded or truncated.
4. The new user segment becomes the next turn.

Gemini's documentation states that when VAD detects an interruption, ongoing generation is canceled and discarded; only content already sent to the client remains in session history.

That is responsive turn-taking, but it is not the same as a model jointly interpreting:

```text
its own speech + the user's overlapping words
```

at every time step.

### Ambient speech

An external speaker, television or nearby conversation can trigger a new turn. Unless the system includes personalized VAD or speaker verification, "speech detected" does not mean "the intended user addressed the agent."

### Self-echo

Even an audio-native model requires AEC. If playback leaks into the microphone, the model may hear itself, infer another speaker, or repeatedly cancel its own output.

### Tool-call silence

Native audio removes media-stage handoffs but does not remove:

* database latency;
* search latency;
* API execution;
* multi-step planning.

Tool calls can create conspicuous dead air unless the system produces fillers, acknowledgment speech, asynchronous completion or speculative output.

### Less deterministic auditing

The model may respond correctly to tone or context not represented in the transcript. That improves interaction but makes post-event reconstruction more difficult:

```text
transcript alone != complete effective prompt
```

## Production systems

### OpenAI Realtime / `gpt-realtime`

OpenAI provides persistent Realtime sessions with native voice-to-voice interaction, configurable server or semantic VAD, interruption handling, WebRTC/WebSocket transport and tool use.

OpenAI has also published production infrastructure details for globally routed, stateful WebRTC media sessions, including ICE and DTLS ownership constraints.

### Gemini Live / Gemini Native Audio

Gemini Live accepts continuous audio streams, supports native audio output, VAD, affective dialogue, interruption and tool use. Its production API is bidirectional, but its documented turn-control behavior still includes explicit activity boundaries and cancellation on barge-in.

### Amazon Nova Sonic / Nova 2 Sonic

Nova Sonic uses a persistent bidirectional streaming API and a unified speech-understanding/generation architecture.

Amazon Connect now exposes Nova Sonic as a speech-to-speech model within contact-center flows, making it a concrete production deployment rather than only a research demonstration.

The API is bidirectional, but AWS also exposes explicit endpointing sensitivity and pause-duration controls. That places its normal operational behavior closer to turn-based native speech than to an unsegmented Moshi-style concurrent-stream model.

---

# 3. Continuous Full-Duplex Models

## Pipeline wiring

A true full-duplex model treats conversation as concurrent time series:

```text
Time step t:

user audio tokens[t-k : t]
system audio tokens[t-k : t]
system text/semantic state[t-k : t]
                 |
                 v
       multi-stream causal model
                 |
       |---------|---------|
       v                   v
next system semantic   next system acoustic
token                   tokens
```

The defining property is:

```text
P(system_output_t |
  user_audio_<=t,
  system_audio_<t,
  dialogue_state_<t)
```

The model continues ingesting user audio while generating system speech. It can theoretically learn:

* when to remain silent;
* when to begin speaking;
* when to backchannel;
* when to continue despite noise;
* when an overlap is cooperative;
* when an overlap is an interruption;
* when to yield the floor;
* how to alter an utterance already in progress.

There is no required external `END_OF_TURN` event.

## Moshi architecture

Moshi is the clearest published example.

It uses:

* a streaming neural audio codec, Mimi;
* separate parallel streams for user speech and model speech;
* audio codec tokens rather than only text;
* time-aligned text tokens called an "Inner Monologue";
* hierarchical semantic-to-acoustic generation;
* causal streaming inference.

The model predicts its own speech while simultaneously conditioning on incoming user speech. The authors report a theoretical latency of **160 ms** and approximately **200 ms in practice**.

That latency is architectural reaction latency, not necessarily a complete public-Internet mouth-to-ear SLA.

## Latency budget

A full-duplex model does not wait for an utterance endpoint. Its budget is closer to an interactive control loop:

| Component                       | Representative target |
| ------------------------------- | --------------------: |
| Audio frame / codec step        |              20-80 ms |
| Network ingress                 |              20-80 ms |
| Streaming codec encoding        |              10-40 ms |
| Transformer step and scheduling |             20-100 ms |
| Acoustic-token lookahead        |             20-100 ms |
| Codec decode / playout buffer   |              20-80 ms |
| Total reaction latency          |          ~150-400 ms |

The essential difference is not merely that every box is faster. It is that this term disappears:

```text
endpoint wait = 0 ms as a mandatory gating operation
```

The model may still choose to wait because it predicts that the user is holding the floor. That is learned conversational timing rather than externally imposed silence timing.

## Information preserved

A concurrent speech model can preserve and reason over:

* word content;
* pitch and rhythm;
* overlap timing;
* backchannels;
* laughter;
* interruptions;
* hesitation;
* user response while the model itself is speaking;
* the relationship between its current vocal output and the user's reaction.

This last item is unique. In a turn-based system, the user's "no, stop" usually becomes a cancellation event. In a full-duplex model it can condition the next audio tokens immediately:

```text
model: "I will delete all-"
user:  "No, archive them."
model: "...archive them instead."
```

Theoretically, the model can redirect before finishing the current syntactic unit.

## Failure modes

### Learned turn control is probabilistic

The model must infer silence, backchannels and interruptions from training data. Errors are not confined to an external VAD module; they are embedded in the generative policy.

Possible failures include:

* speaking over the user;
* never yielding;
* treating "uh-huh" as a request to take the floor;
* stopping for incidental noise;
* responding to its own echo;
* producing excessive backchannels;
* continuing a sentence after the user has rejected its premise.

### Acoustic feedback loop

Because the model is always listening while speaking, AEC quality is existential. Residual echo becomes part of the conditioning stream at every timestep.

The model may:

* imitate itself;
* interpret its output as user speech;
* enter repetitive loops;
* falsely infer agreement from leaked playback.

### Multi-speaker ambiguity

Concurrent audio does not inherently solve speaker attribution. A mono microphone mixture may contain:

```text
primary user + second person + television + model echo
```

A full-duplex model needs spatial processing, speaker embeddings, personalized VAD or diarization to determine whose interruption matters.

### Semantic capability pressure

The model's computation is spent jointly on:

* audio encoding;
* timing;
* turn policy;
* lexical generation;
* acoustic generation;
* listening during output.

This is materially harder than running a large text model after a finalized transcript. Moshi's own follow-on work acknowledges that its cognitive capability is limited relative to stronger text-centered systems, motivating asynchronous RAG extensions.

### Tool use and retrieval

A continuously speaking model cannot simply pause its temporal loop for a multi-second tool call.

Possible designs include:

* asynchronous retrieval;
* a separate reasoning model;
* speculative filler speech;
* interruption-safe delayed answers;
* parallel "interaction" and "thinking" layers.

Recent DuplexOmni work explicitly separates an immediate interaction layer from an asynchronous thinking/tool layer. This is a strong indication that a single synchronous full-duplex generator is not sufficient for both natural timing and deep reasoning.

### Safety intervention

With turn-based systems, safety evaluation can occur before speech output begins. In full-duplex generation, output may already be audible before a complete semantic sequence exists.

Safety therefore needs:

* streaming token-level moderation;
* low-latency output gating;
* codec-token rollback or muting;
* action confirmation outside the conversational stream.

### State reconstruction

Conversation logs require more than alternating messages. The record must preserve:

* two synchronized audio timelines;
* overlap intervals;
* generated-but-not-played audio;
* user speech heard during system output;
* cancellation and redirection points.

A simple sequence such as:

```json
[
  {"role": "user", "text": "..."},
  {"role": "assistant", "text": "..."}
]
```

is structurally inadequate.

## Production and deployed systems

### Moshi

Moshi is open-source and publicly deployable, with released inference code and a live demonstration. It is the best-documented true full-duplex architecture.

It should be described as an operational research system or deployable reference implementation, not as evidence of mass-scale contact-center production.

### MoshiRAG

Kyutai's MoshiRAG keeps the full-duplex interaction model while adding asynchronous retrieval. It demonstrates the likely production pattern: immediate speech interaction in one loop and slower knowledge acquisition in another.

### Research systems

Freeze-Omni supports streaming speech input/output and adds duplex dialogue training, but published comparisons distinguish it from Moshi's unconditional concurrent-stream design; some systems rely on VAD-assisted duplex control.

Other relevant systems include:

* **SyncLLM:** synchronous text-stream modeling for full-duplex dialogue under delayed network input.
* **LSLM:** a model designed to listen while speaking using parallel listening and speaking channels.
* **DuplexCascade:** a 2026 VAD-free cascaded architecture using chunk-level "micro-turns" and control tokens. It is important because it shows that full-duplex behavior need not require a monolithic native-audio model.
* **FireRedChat:** combines personalized streaming VAD, semantic endpointing and explicit barge-in control in a practical modular system.

There is currently limited public primary-source evidence that the major commercial voice APIs expose a **Moshi-style, continuously conditioned full-duplex model** in production. OpenAI, Google and AWS expose bidirectional streaming and interruption, but their public documentation often describes VAD-delimited turns, generation cancellation or endpointing controls. It is therefore technically unsafe to classify them as fully continuous solely from product demonstrations or the word "duplex."

---

# Direct Technical Conclusions

## Latency

The architectures remove different latency terms:

```text
Cascade:
endpoint + ASR finalize + LLM TTFT + text buffering + TTS TTFA

Turn-based native:
endpoint + unified-model TTFA

Full-duplex:
continuous frame processing + learned decision to respond
```

Full-duplex offers the lowest possible reaction latency because it does not require a committed turn boundary. Turn-based native models remove service handoffs but can still feel slow when endpoint detection is conservative. Cascades can approach native-model latency through speculative ASR, early LLM invocation and incremental TTS, but their cancellation logic becomes complex.

## Information fidelity

```text
Cascade:
audio -> text bottleneck -> regenerated prosody

Turn-based native:
audio semantics retained within each turn

Full-duplex:
audio semantics + overlap dynamics retained continuously
```

The most important information lost by cascades is not generic "emotion." It is **timing-conditioned meaning**: whether a pause is hesitation, whether an overlap is agreement or rejection, and whether a change in tone occurred in reaction to the system's speech.

## Reliability

Cascades localize failures and are easiest to debug. Audio-native models reduce serial error propagation but make internal interpretation less visible. Full-duplex systems move turn-taking from deterministic application logic into a probabilistic generative policy, improving naturalness but expanding the behavioral test surface.

## Production suitability

* **Regulated transactions, complex tools, exact transcripts:** cascaded architecture remains the safest default.
* **General-purpose assistants and customer interactions where conversational quality matters:** turn-based native audio is the current practical center of gravity.
* **Companions, coaching, natural backchanneling, collaborative dialogue and embodied agents:** full-duplex is architecturally superior, but the reasoning, safety, observability and deployment stack remains immature.

The likely durable production architecture is not one of the three in pure form. It is a **hybrid**:

```text
continuous low-latency interaction model
        +
asynchronous high-capability reasoning/tool model
        +
explicit transaction and safety controller
```

That design preserves full-duplex timing without forcing the conversational audio model to perform every reasoning, retrieval and control function itself.

---

# HIP Relevance Notes

Direct hooks into the current prototype, flagged for the design spec:

1. The prototype voice path (Whisper STT to routing to inference to TTS) is the cascade in section 1. Its dominant controllable delay is endpointing, not inference. Any latency work should attack the silence threshold before the model tiers.
2. The hybrid conclusion (continuous interaction model + asynchronous reasoning/tool model + explicit safety/transaction controller) maps onto the existing routing cascade: the interaction model is the edge tier, the reasoning/tool model is Mid/Core/Frontier, and the governance layer is the transaction/safety controller. This is the same split DuplexOmni and MoshiRAG converge on independently.
3. Full-duplex moves turn-taking from deterministic app logic into a probabilistic policy. That expands the test surface and weakens auditability, which is in direct tension with HIP's governed/observable posture. The safety controller in the hybrid is not optional for HIP; it is the differentiator.
4. Moshi (open weights) and DuplexCascade (VAD-free, non-monolithic) are the two reference points worth tracking. DuplexCascade matters because it shows full-duplex behavior without a single native-audio model, which is more compatible with a tiered routing architecture than a monolithic Moshi drop-in.

# Reference Sources

Toward low-latency voice agents survey: arxiv.org/pdf/2508.04721
Amazon Nova turn-taking controllability: docs.aws.amazon.com/nova/latest/nova2-userguide/sonic-turn-taking.html
OpenAI Realtime and audio guide: developers.openai.com/api/docs/guides/realtime
OpenAI Realtime VAD guide: developers.openai.com/api/docs/guides/realtime-vad
OpenAI Realtime conversations: developers.openai.com/api/docs/guides/realtime-conversations
OpenAI gpt-realtime announcement: openai.com/index/introducing-gpt-realtime/
OpenAI low-latency voice at scale: openai.com/index/delivering-low-latency-voice-ai-at-scale/
Google Cloud Speech-to-Text voice activity events: docs.cloud.google.com/speech-to-text/docs/voice-activity-events
Gemini Live API best practices: docs.cloud.google.com/gemini-enterprise-agent-platform/models/live-api/best-practices
Gemini Live API overview: docs.cloud.google.com/gemini-enterprise-agent-platform/models/live-api
Gemini Live API reference (multimodal-live): docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/multimodal-live
Gemini Live native audio in Vertex AI: cloud.google.com/blog/topics/developers-practitioners/how-to-use-gemini-live-api-native-audio-in-vertex-ai
AWS Nova Sonic vs cascading architectures: aws.amazon.com/blogs/machine-learning/building-real-time-voice-assistants-with-amazon-nova-sonic-compared-to-cascading-architectures/
AWS Loka Nova 2 Sonic voice agent: aws.amazon.com/blogs/machine-learning/how-loka-built-a-natural-low-latency-voice-agent-with-amazon-nova-2-sonic/
Amazon Nova Sonic speech model: docs.aws.amazon.com/nova/latest/userguide/speech.html
Amazon Connect Nova Sonic speech-to-speech: docs.aws.amazon.com/connect/latest/adminguide/nova-sonic-speech-to-speech.html
Moshi speech-text foundation model: arxiv.org/abs/2410.00037
MoshiRAG asynchronous knowledge retrieval: kyutai.org/blog/2026-04-30-moshi-rag/
DuplexOmni real-time full-duplex interaction: arxiv.org/abs/2606.09186
Freeze-Omni low-latency speech-to-speech: arxiv.org/abs/2411.00774
SyncLLM synchronous full-duplex dialogue agents: homes.cs.washington.edu/~gshyam/Papers/syncllm.pdf
LSLM language model can listen while speaking: ojs.aaai.org/index.php/AAAI/article/view/34665/36820
DuplexCascade full-duplex speech-to-speech: arxiv.org/html/2603.09180v1
FireRedChat pluggable full-duplex voice interaction: arxiv.org/html/2509.06502v1
