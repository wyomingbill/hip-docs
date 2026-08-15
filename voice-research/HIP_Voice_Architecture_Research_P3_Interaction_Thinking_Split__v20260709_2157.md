---
doc: HIP Voice Architecture Research
part: P3 of the voice architecture research set
topic: The interaction model / background reasoning model split
source: ChatGPT deep research output (prompt 3 of 8), reviewed and marked down
status: reference
version: v20260709_2157
location: ~/hip-dev/docs/voice-research/
---

# The Interaction / Thinking Split

The pattern is best described as an **asynchronous fast-path/slow-path conversational architecture**:

```text
                        +------------------------------------------+
Live audio/video/text ->| Interaction model                        |--> Live speech
                        | - floor control                          |
                        | - backchannels / interruptions           |
                        | - immediate low-risk responses           |
                        | - delegation and result-integration      |
                        +--------------+---------------------------+
                                       | delegation event
                                       v
                        +------------------------------------------+
                        | Background reasoning system              |
                        | - larger reasoning model                 |
                        | - retrieval/search                       |
                        | - tools and APIs                         |
                        | - long-horizon planning                  |
                        +--------------+---------------------------+
                                       | partial/final result events
                                       +--------> interaction model
```

The interaction model stays synchronized with wall-clock conversation while the slower system works concurrently. The background result is not necessarily shown directly; it becomes another live input that the interaction model must interpret, prioritize, possibly discard, and incorporate into ongoing speech.

This differs from simply placing a smaller model in front of a larger model. The defining properties are:

1. **The public conversational process never blocks.**
2. **Delegated work has an independent lifecycle.**
3. **The user can continue speaking and alter the task while that work runs.**
4. **Returned results are integrated according to the current conversational state, not merely appended to the transcript.**

Thinking Machines Labs calls this an **interaction model plus an asynchronous background model**. KAME calls its slower output an **oracle stream**. DuplexOmni calls the two components the **interaction layer** and **thinking layer**. MoshiRAG implements a narrower version in which the fast speech model selectively launches retrieval while continuing to speak.

One caveat: **"lightweight" does not necessarily mean small**. The interaction model is latency-optimized, but published systems use front ends in roughly the 7 to 8 billion-parameter range, and Thinking Machines explicitly describes its interaction model as retaining substantive intelligence rather than acting as a simple dialogue controller.

---

## 1. How the interaction model decides when to delegate

There are four distinct mechanisms in the published work.

### A. Learned selective trigger

MoshiRAG trains the speech model to emit a special retrieval token, `<ret>`, when the current question is likely to require external knowledge. The trigger is part of the model's ordinary token output, not a separate classifier bolted onto the system.

When `<ret>` appears:

* The current user transcript and relevant assistant context are packaged into a query.
* Retrieval begins asynchronously.
* The speech model continues generating audio.
* The retrieved reference is later encoded and injected into a dedicated conditioning stream.

The training data explicitly marks where retrieval should begin. Responses are decomposed into a **lead**, which can be spoken without retrieved knowledge, and a **body**, which contains the grounded answer. The trigger is placed before the lead so retrieval can overlap with the early speech.

This is the cleanest concrete example of a learned delegation policy:

```text
Model output:
<ret> "Let me check the exact figure..."
```

The token simultaneously functions as a semantic decision, a scheduler instruction, and a state transition in the runtime.

### B. Continuous speculative delegation

KAME does not wait for a high-confidence trigger. Its speech front end continuously produces partial transcripts, and the background LLM is repeatedly invoked on the expanding transcript.

For example:

```text
t = 0.8 s: "What was NVIDIA's..."
             |- background candidate A starts

t = 1.3 s: "What was NVIDIA's revenue..."
             |- background candidate B supersedes A

t = 1.9 s: "What was NVIDIA's revenue last quarter?"
             |- background candidate C supersedes B
```

The newest candidate receives priority because it is based on the most complete user utterance. The system is therefore computing ahead speculatively rather than waiting for a conventional end-of-turn boundary. KAME's front-end cycle is approximately 80 milliseconds, while its background oracle is updated on a slower 100 to 500 millisecond cadence.

This approach buys latency by spending more compute. It also creates cancellation and staleness problems: earlier candidate answers may become invalid as the user completes or revises the question.

### C. Learned per-slice control policy

DuplexOmni divides the stream into approximately 480-millisecond slices. On each slice, the interaction layer emits multiple outputs, including semantic interpretation, conversational speech/text, and a **thinking-control signal**.

Its training vocabulary includes controls such as:

* `[THINK]`: start or continue background reasoning;
* `[WAIT]`: defer commitment or wait for more information;
* `[CUT]`: stop or interrupt an obsolete process or output.

The system therefore represents delegation as a temporally aligned control-token stream. Background results arrive asynchronously and are reintroduced through designated result tokens or channels.

Conceptually, the model is repeatedly making a policy decision:

```text
every 480 ms:
    observe live user state
    observe assistant speech state
    observe background-job state
    emit {
        dialogue_action,
        speech_content,
        background_control
    }
```

### D. Runtime or harness-level policy

The decision need not be learned inside the interaction model. Asynchronous I/O and speculative tool-calling systems can use an external task manager that monitors partial user input, launches safe read-only tools speculatively, cancels calls when the request changes, and interrupts model generation when new information arrives.

In these systems, delegation is principally an orchestration policy rather than a learned speech token. The published Async I/O design distinguishes between speculative safe operations, which can execute immediately, and consequential or write operations, which should remain uncommitted until user intent is sufficiently certain.

---

## 2. How the interaction model fills the gap

The system cannot simply speak arbitrary filler. Early speech constrains what can be said later. A premature factual commitment may make the eventual result impossible to integrate cleanly.

Published systems use several techniques.

### Backchannels and acknowledgment

The interaction model can produce socially normal, semantically inexpensive signals: "Right." "Let me check." "I'm looking at that." brief acknowledgment sounds, or repetition/clarification of the request. These maintain responsiveness without committing to the answer.

### A knowledge-independent lead

MoshiRAG deliberately trains an initial response segment that does not depend on the retrieved material:

> "Let me check the exact numbers, because the reporting periods matter here."

The lead creates a temporal buffer before the answer reaches the first fact that requires retrieval. MoshiRAG calls the delay between response onset and the first key answer content the **keyword delay**. Its architecture attempts to complete retrieval inside that interval.

### Coarse-to-specific response construction

The interaction model can safely begin with information already established in context:

```text
Immediate:
"The acquisition definitely changed the economics..."

After result:
"...and the filing puts the annualized savings at approximately $1.2 billion."
```

The first clause establishes structure and relevance; the second supplies the externally verified fact.

### Continue listening rather than filling

In full-duplex systems, silence is itself a valid output. The model can keep receiving audio, allow the user to elaborate, or ask a narrow clarification while the background job runs. Thinking Machines' design treats silence, overlap, interruption, speech, and tool activity as components of one time-aligned stream rather than as separate turn states.

### Speak a revisable provisional interpretation

KAME is trained with oracle streams that evolve from vague or incomplete guesses toward more accurate final information. The front end learns that early backend text may be provisional and that later updates supersede it. Timing jitter is added during training so the interaction model does not assume results will arrive at fixed boundaries.

The engineering rule is straightforward:

> **Speak early about framing, process, or already-known context. Delay externally dependent nouns, numbers, names, conclusions, and commitments.**

That rule is an architectural inference from the published systems rather than a named standard.

---

## 3. How asynchronous results are woven back into speech

This is the hardest part of the pattern. Launching a second model is easy; integrating its result without producing a conversational seam is not.

### Dedicated conditioning stream

MoshiRAG encodes the retrieved document and feeds it into an additional temporal conditioning pathway. The speech model does not simply receive a visible text message saying "tool result." It receives a learned representation that can condition subsequent audio-token generation. An encoder compresses the reference before injection to keep the streaming cost manageable.

### Oracle token stream

KAME adds a fourth stream to Moshi's existing multistream architecture. The backend LLM's text arrives incrementally as an "oracle" sequence. The speech model attends to that sequence while continuing to decode its own audio.

This allows the model to decide whether the oracle is relevant, whether it supersedes an earlier oracle, whether to use it immediately, and how to convert written reasoning into natural spoken output.

### Structured result events and control tokens

DuplexOmni returns partial thinking-layer results through structured asynchronous channels. The interaction layer can request, wait for, revise, or terminate background processing through its control vocabulary.

The important point is that a background answer is treated as an **event with timing and lifecycle state**, not merely as the next message in a chat history.

### Shared response buffer and prefix handoff

RelayS2S uses a related but narrower design:

1. A fast speech-to-speech path generates the beginning of the answer.
2. A slower ASR-LLM path generates the more capable continuation.
3. A verifier checks the fast prefix.
4. The slower model is conditioned on the committed prefix.
5. Both feed one response buffer consumed by TTS.

This avoids restarting the sentence when the slow path becomes available. Its five-word fast prefix creates roughly a two-second computation window for the slower model. RelayS2S reports quality close to the cascade while retaining speech-to-speech-like onset latency.

RelayS2S is not fully continuous or full-duplex in the same sense as KAME or the Thinking Machines design, but it demonstrates the essential **prefix commitment and continuation handoff** mechanism.

### Context-aware insertion

Thinking Machines describes results as streaming back into the interaction model and being introduced at a "context-appropriate moment," rather than forcing an abrupt mode switch. It also says the two models share a rich context package. The public description does not expose the exact result-token schema or training target, so the mechanism is less concrete than MoshiRAG, KAME, or DuplexOmni.

A production integration policy would normally check:

```text
result.job_id
result.based_on_context_version
result.partial_or_final
result.confidence
result.expiration
current_user_intent
current_assistant_sentence_state
current_floor_owner
```

It should discard or revise a result when the current context has materially diverged from the context that launched it.

---

## 4. Latency implications

This architecture does not eliminate reasoning latency. It **moves much of it behind useful conversational activity**.

Three latency measures must be separated:

| Measure                    | Meaning                                                     |
| -------------------------- | ----------------------------------------------------------- |
| **Response-onset latency** | Time until the assistant begins audible behavior            |
| **Answer-content latency** | Time until the first useful or externally dependent content |
| **Completion latency**     | Time until the full reasoning/tool result is available      |

A system can have near-zero onset latency but still require several seconds before giving the key answer.

### Published numbers

* **Thinking Machines:** 200-millisecond time-aligned micro-turns for continuous input/output processing. The company also describes specialized serving work for persistent sessions and frequent small prefills, because conventional inference stacks are optimized for larger, less frequent requests.
* **MoshiRAG:** targets retrieval completion within about two seconds; its authors report degradation when backend delays exceed roughly three seconds. On its benchmark, response onset was effectively immediate, while key-answer delay was approximately 3.1 seconds.
* **KAME:** approximately 80-millisecond interaction cycles and 100 to 500-millisecond backend updates. Its reported median response onset was effectively zero because the model can begin responding before the user has completely finished, versus about 2.1 seconds for the evaluated cascade.
* **DuplexOmni:** 480-millisecond processing slices and reported latency of approximately 0.506 seconds in its evaluation.
* **Async I/O agents:** reported end-to-end speedups of approximately 1.3 to 1.7x in cloud settings and 1.6 to 2.2x at the edge by overlapping user input, reasoning, and tool execution.

These numbers are not directly comparable. They use different definitions, hardware, turn-detection assumptions, workloads, and benchmarks.

### New latency costs introduced by the split

The architecture adds overhead that a standard single-turn loop does not have:

* continuous streaming ASR or audio encoding;
* frequent small model prefills;
* duplicated speculative backend calls;
* result encoding and cross-model transfer;
* cancellation and supersession bookkeeping;
* synchronization between audio, text, tool, and control streams;
* persistent KV-cache and session memory residency.

The pattern primarily improves **perceived latency and conversational continuity**, not necessarily total compute or total time to a fully reasoned answer.

---

## 5. Difference from a standard agentic tool-calling loop

A conventional tool loop is generally sequential:

```text
User turn completes
    v
LLM reasons
    v
LLM emits tool call
    v
Generation pauses
    v
Tool runs
    v
Tool result is appended as an observation
    v
LLM resumes
    v
Final response
```

ReAct formalized the interleaving of reasoning and actions, while mainstream function-calling interfaces represent tool invocation as a model-generated call followed by an externally supplied result associated with that call. Many implementations suspend the answer until the observation is returned.

The interaction/thinking split changes the control model:

| Dimension                          | Standard agentic loop                         | Interaction/background split                                 |
| ---------------------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| **Primary unit**                   | Completed user turn                           | Continuous time slice or micro-turn                          |
| **Public output during tool work** | Usually paused or procedural                  | Continues naturally                                          |
| **Reasoning process**              | Usually one serial model loop                 | Concurrent interaction and reasoning processes               |
| **User interruption**              | Often starts a new turn after completion      | Can revise or cancel in-flight work                          |
| **Tool result**                    | Appended observation, then generation resumes | Asynchronous event or stream                                 |
| **Result timing**                  | Used immediately after return                 | Held until an appropriate speech boundary                    |
| **Speech commitment**              | Normally begins after tool completion         | May begin before result exists                               |
| **Stale work**                     | Limited handling in many frameworks           | Central concern; jobs require versions and cancellation      |
| **Optimization target**            | Task completion and correctness               | Correctness plus floor control, timing and social continuity |
| **Time representation**            | Mostly token/order based                      | Explicit wall-clock alignment                                |

The distinction is therefore not "one model calls another model." Standard multi-agent frameworks do that routinely.

The actual difference is:

> **Control of the conversational floor is separated from completion of the cognitive task.**

The interaction model is a low-latency dialogue policy, scheduler, and renderer. The background system is a cognitive worker. The difficult interface is not a request/response API; it is a versioned, interruptible stream of partial evidence.

---

## 6. Published and open implementations

| System                                   | Split implemented                                                         | Delegation method                                    | Availability                                                                                     |
| ---------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **MoshiRAG**                             | Full-duplex speech model + retrieval/tool backend                         | Learned `<ret>` trigger                              | Open inference code, released model variants and weights; strongest directly usable example.     |
| **KAME**                                 | Fast duplex S2S model + repeatedly invoked text LLM                       | Continuous speculative oracle generation             | Open inference and fine-tuning code plus model weights.                                          |
| **Thinking Machines Interaction Models** | Time-aware interaction model + asynchronous background model              | Learned delegation within 200 ms micro-turns         | Public architectural preview; no public model weights located. Some serving work contributed to SGLang. |
| **DuplexOmni**                           | Interaction layer + pluggable thinking/tool layer                         | `[THINK]`, `[WAIT]`, `[CUT]` control stream          | Published architecture; release promised, but no confirmed complete public release in reviewed sources. |
| **RelayS2S**                             | Fast spoken prefix + slower high-quality continuation                     | Parallel paths and verified prefix handoff           | Code and data reported public; adjacent rather than fully continuous/full-duplex.               |
| **AsyncReasoning**                       | Private reasoning stream + public response stream                         | Concurrent reasoning and response scheduling         | Open reference implementation, including a minimal voice-assistant example; not necessarily a two-model/tool architecture. |
| **DuplexSLA**                            | One speech-language-action model producing audio and actions concurrently | Joint audio/action decoding on roughly 160 ms chunks | Published report and repository, but inference code and checkpoints still marked forthcoming in reviewed repo. |
| **Async I/O / speculative tool agents**  | Interruptible agent generation + concurrent tools and user input          | External event queue and task manager                | Published systems design; more of an agent-runtime pattern than a native conversational model split. |

---

## 7. The unresolved engineering problems

The pattern is credible, but the public work has not fully solved several issues.

### Semantic commitment

Once audio has been spoken, it cannot be retracted invisibly. Systems need explicit rules identifying which claims are safe before background verification.

### Result staleness

Every job needs to record the context version that launched it. A result based on "Find flights to Boston" may no longer be valid after the user says "Actually, make that Austin."

### Competing background jobs

Multiple partial queries may launch overlapping retrievals. The scheduler must decide whether to cancel, merge, deprioritize, or allow all of them to complete.

### Prosodic continuity

A textually valid continuation may still sound wrong if it arrives during an incompatible phrase, intonation contour, or emotional register.

### Tool safety

Speculative search is relatively safe. Speculative purchasing, messaging, deletion, account changes, or medical instructions are not. Side-effecting operations require a separate commitment boundary.

### Compute economics

Continuous oracle generation can be substantially more expensive than a single call after turn completion. Selective triggers reduce cost but risk missing situations where delegation was needed.

### Training data

The model needs examples containing live timing, partial user utterances, interrupted or corrected requests, delayed/partial/contradictory tool results, appropriate backchannels, stale-job cancellation, sentence-level integration points, and decisions not to expose an irrelevant result.

Thinking Machines and DuplexOmni describe synthetic or purpose-built temporal training regimes, while KAME explicitly simulates evolving and delayed oracle information.

---

## Bottom Line

This is becoming a distinct architecture rather than a minor optimization to tool calling.

The most concrete current forms are:

1. **Selective asynchronous augmentation:** MoshiRAG.
2. **Continuous tandem fast/slow inference:** KAME.
3. **Learned micro-turn control over an asynchronous thinking layer:** DuplexOmni and the Thinking Machines design.
4. **Runtime-level speculative concurrency:** Async I/O agent systems.
5. **Fast-prefix/slow-continuation handoff:** RelayS2S.

The architectural breakthrough is not delegating work. Agents already do that. It is allowing the assistant to **remain an active participant in a live conversation while delegated cognition is incomplete**, and then making the returned information subordinate to the conversation's current timing, intent and floor state.

A robust implementation would treat the interaction model as three systems at once:

```text
1. Dialogue policy:
   speak / listen / pause / interrupt / clarify

2. Concurrent-work scheduler:
   launch / update / cancel / prioritize / commit

3. Result renderer:
   ignore / paraphrase / defer / integrate / correct
```

That is the meaningful difference from a standard tool-calling loop.

---

# HIP Relevance Notes

1. This is the load-bearing document for HIP. The interaction/thinking split maps directly onto the existing routing cascade: interaction model = edge tier, background reasoning = Mid/Core/Frontier, and the delegation trigger is the analogue of the Bloom's complexity classifier. The cascade was already built on this logic; the research names it and supplies open reference implementations (MoshiRAG, KAME).
2. MoshiRAG is the single most usable external reference. It is open code + weights, full-duplex, with a learned `<ret>` delegation trigger and an asynchronous retrieval backend. That is a working template for HIP's edge-tier-delegates-to-cascade pattern. Worth cloning and reading before any HIP full-duplex design work.
3. The "three systems at once" framing (dialogue policy, concurrent-work scheduler, result renderer) is a clean spec skeleton for the HIP interaction layer. The scheduler and renderer are where governance attaches: HITL gates, per-member permissions, and refusal handling live in the scheduler's commit step and the renderer's ignore/defer branch.
4. The unresolved problems section is a direct risk register for HIP. Tool safety (the commitment boundary for side-effecting operations) and semantic commitment (which claims are safe before verification) are the two that intersect hardest with HIP's governed/operator-consensual posture. These are not solved in the literature, which means they are HIP's opportunity to define, not just adopt.
5. Result staleness with context versioning (`result.based_on_context_version`) is a concrete design requirement that the current prototype's fact-change detection (Groq Llama 4 Scout, 0.5s) is already adjacent to. The versioning discipline needed here is the same discipline the fact graph already enforces.

# Reference Sources

Thinking Machines interaction models: thinkingmachines.ai/blog/interaction-models/
MoshiRAG repo (kyutai-labs): github.com/kyutai-labs/moshi-rag
MoshiRAG paper: ar5iv.org/abs/2604.12928
KAME tandem architecture: arxiv.org/html/2510.02327v1
DuplexOmni real-time full-duplex interaction: arxiv.org/html/2606.09186v1
Async I/O and speculative tool calling: arxiv.org/html/2605.13360v1
RelayS2S dual-path speculative generation: arxiv.org/html/2603.23346v1
ReAct reasoning and acting: arxiv.org/abs/2210.03629
KAME weights (SakanaAI): huggingface.co/SakanaAI/kame
AsyncReasoning (yandex-research): github.com/yandex-research/AsyncReasoning
DuplexSLA: arxiv.org/abs/2605.20755
