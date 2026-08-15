---
doc: HIP Voice Architecture Research
part: P7 of the voice architecture research set
topic: Real-time voice AI latency and unit-cost economics
source: ChatGPT deep research output (prompt 7 of 8), reviewed and marked down
status: reference
version: v20260710_1137
location: ~/hip-dev/docs/voice-research/
note: RTF export mangled math; rendered in plain notation. Prices are as published July 10, 2026 and will drift. Tables preserved.
---

# Real-Time Voice AI: Latency and Cost Model

## 1. What latency should mean

The most useful production metric is end-of-user-speech to first audible assistant audio, measured at the user's speaker. For a conventional pipeline:

```text
L_onset = L_capture/uplink + L_endpoint + L_STT-final + L_route
          + L_LLM-TTFT + L_TTS-first-audio + L_downlink/playout
```

For full-duplex systems this formula changes, because capture, interpretation, routing and speculative reasoning occur while the user is still speaking. Latency becomes the residual work remaining after the final phoneme, not the sum of every stage.

Human turn transitions commonly occur around 200-250 ms, with roughly 400 ms a reasonable upper bound for a smooth transition. OpenAI reported 232 ms minimum and 320 ms average audio response latency for GPT-4o; Moshi reports approximately 200 ms in practice. These are model-level reference points, not guaranteed production p95.

| Metric | Target |
| --- | --- |
| Excellent conversational transition | 200-400 ms |
| Strong production p50 | under 500 ms |
| Acceptable production p95 | under 800 ms |
| Noticeably sluggish | 800-1,200 ms |
| Requires an acknowledgment or backchannel | over 1,200 ms |

The under-400 ms target generally requires anticipation or continuous processing. A system that waits 500 ms of silence before beginning inference has already missed the natural human timing window.

## 2. Per-stage latency breakdown

Engineering planning ranges, synthesized from published model numbers and production configurations. First-response latency, not time to finish the full answer. Opus commonly uses 20 ms audio frames. OpenAI's server VAD defaults to 500 ms of silence; Pipecat uses a 200 ms low-level VAD stop interval. Current streaming STT reports ~150-250 ms in favorable conditions. Fast TTS reports ~55-75 ms model-side first-audio latency, excluding network and application overhead.

| Stage | Cascaded (STT / LLM / TTS) | Turn-based audio-native | Full-duplex continuous |
| --- | --- | --- | --- |
| Capture, packetization, uplink | 20-80 ms | 20-80 ms | 20-60 ms |
| VAD / end-of-turn decision | 200-700 ms | 200-500 ms | 0 ms blocking; 20-160 ms state update |
| STT finalization | 100-350 ms | fused; ~20-120 ms encoder flush | fused/continuous; no separate blocking stage |
| Routing / policy | 5-80 ms | 5-40 ms | 0-20 ms per interaction cycle |
| LLM or response inference | 150-800 ms fast; 500-3,000+ ms reasoning | 150-500 ms | 80-250 ms for interaction output |
| TTS first chunk / codec decode | 50-300 ms | 20-100 ms | 20-80 ms |
| Downlink, jitter buffer, playback | 30-100 ms | 30-100 ms | 20-60 ms |
| Typical first-audio result | 700-1,600 ms | 450-900 ms | 150-400 ms for simple interaction |
| Poorly tuned result | 1.5-3+ s | 1-1.5 s | background answer may still take 1-3+ s |

Not every range should be arithmetically added. Streaming STT processes most of the utterance before it ends, and full-duplex systems overlap almost everything.

## 3. Cascaded architecture

Representative fast pipeline: 20 + 200 + 150 + 20 + 250 + 75 + 50 = 765 ms (final audio frame/uplink, endpoint confirmation, STT final, routing, LLM first token, TTS first audio, playback buffer). More conventional configuration: 20 + 500 + 250 + 30 + 500 + 75 + 60 = 1,435 ms. The difference is mostly endpointing and model TTFT.

OpenAI's default server VAD waits 500 ms of silence. Deepgram recommends roughly 300-500 ms for conversational speech where users pause mid-thought. Pipecat's lower-level VAD defaults to 200 ms but can apply a smarter conversational turn strategy above it.

What dominates: (1) endpointing, often 200-700 ms; (2) LLM TTFT, especially with large or reasoning models; (3) TTS chunking, which may wait for punctuation or characters before beginning; (4) network crossings, potentially three remote calls (STT, LLM, TTS). The raw ASR model is not necessarily slow: ElevenLabs lists ~150 ms for Scribe Realtime, and a streaming benchmark cited a 249 ms median for Soniox. Finalization behavior and endpoint configuration frequently add more delay than acoustic inference itself.

## 4. Turn-based audio-native architecture

STT, semantic inference and TTS exist internally but are not exposed as three serial services. A planning budget: 20 (capture) + 300 (endpoint) + 50 (encoder flush) + 10 (routing) + 250 (generation) + 50 (codec) + 40 (playout) = 720 ms. The architecture removes two service boundaries and retains prosody, emotion and nonverbal audio, but does not by itself remove the silence wait. If it remains turn-based, endpointing can still consume 300-500 ms. GPT-4o's 232 ms minimum / 320 ms average shows the lower bound achievable by a unified model; actual application latency can be higher after VAD, network, safety processing and playback buffering.

## 5. Full-duplex architecture

There is no blocking "the user has finished, now start" transition; the system updates state on each audio frame or micro-turn. Moshi uses an 80 ms codec frame and reports ~200 ms practical latency. Thinking Machines describes 200 ms interaction micro-turns. DuplexOmni operates at 480 ms response granularity. A simplified residual budget: 80-200 (decision/generation) + 20-80 (codec) + 20-60 (playout) = 120-340 ms. The model may already have interpreted most of the sentence, selected a likely route, started retrieval, prepared a response prefix, or decided a backchannel is appropriate.

Important distinction: a full-duplex system can produce a natural acknowledgment in 200 ms while the substantive answer remains unavailable for two seconds. It needs two latency measures:

| Measure | Meaning |
| --- | --- |
| Interaction latency | Time until acknowledgment, backchannel or turn response |
| Answer latency | Time until the fact, reasoning result or tool output is available |

A system can score well on the first and poorly on the second.

## 6. Cost assumptions

Normalize to one wall-clock minute of conversation: user speaks 25 s, assistant speaks 20 s, silence/overlap 15 s, four response turns per minute, 150 words/minute, 1.33 tokens/word, six characters/word including spaces. Therefore user text ~183 tokens, assistant text ~146 tokens, assistant characters ~300. Prices use publicly listed rates as of July 10, 2026 and exclude telephony, bandwidth, storage, retrieval databases, search fees and engineering infrastructure.

## 7. Audio-token overhead versus text

At 150 wpm, textualized speech produces ~3.3 text tokens/second. OpenAI Realtime billing uses one user audio token per 100 ms (10 tokens/s) and one assistant audio token per 50 ms (20 tokens/s). Google Live documents ~25 audio tokens/second. Moshi's Mimi codec uses eight codebooks at 12.5 frames/second, producing 100 raw codec tokens/second, though its hierarchical design reduces the main temporal Transformer to 12.5 autoregressive timesteps/second.

| Representation | Rate | Multiple vs text |
| --- | --- | --- |
| Text at 150 wpm | 3.3 tokens/s | 1.0x |
| OpenAI user audio | 10 tokens/s | 3.0x |
| OpenAI assistant audio | 20 tokens/s | 6.0x |
| Gemini Live audio | 25 tokens/s | 7.5x |
| Moshi temporal frames | 12.5 steps/s | 3.8x |
| Moshi raw eight-codebook tokens | 100 tokens/s | 30x |

Raw token count is not directly comparable across architectures. The general conclusion holds: audio models process a much denser temporal stream than text models, and full duplex compounds this by maintaining both user and assistant streams, including silence and overlap.

## 8. Cascaded per-minute cost

Representative stack: Deepgram Flux STT $0.0065/input-audio minute; Deepgram Aura-2 TTS $0.030/1,000 chars; alternative ElevenLabs Flash TTS $0.050/1,000 chars; GPT-5.6 Luna $1/M input, $0.10/M cached input, $6/M output.

STT: (25/60) x $0.0065 = $0.00271. TTS Aura-2: (300/1000) x $0.030 = $0.009; ElevenLabs: $0.015. New LLM tokens: 183 x $1/1M + 146 x $6/1M ~= $0.000485 (raw conversational text is almost free). Context replay is the actual text-model cost driver: four responses reading a 2,000-token cached context = 4 x 2,000 x $0.10/1M = $0.0008 cached, or $0.008 uncached.

| Configuration | Cost per wall-clock minute |
| --- | --- |
| Aura-2 TTS, cached context | $0.0130 |
| ElevenLabs TTS, cached context | $0.0190 |
| Aura-2, uncached context | $0.0202 |
| ElevenLabs, uncached context | $0.0262 |

Approximately 1.3-2.6 cents per conversation minute under these assumptions.

## 9. Turn-based native-audio cost

OpenAI pricing: GPT-Realtime-2.1 audio in $32/M, audio out $64/M, text in $4/M, text out $24/M. GPT-Realtime-2.1-mini audio in $10/M, out $20/M, text in $0.60/M, out $2.40/M. For 25 s user speech = 250 input audio tokens; 20 s assistant speech = 400 output audio tokens.

Large model: input 250 x $32/1M = $0.008; output 400 x $64/1M = $0.0256; text 146 x $24/1M = $0.0035; base total ~= $0.0352, about 3.5 cents/minute before context. With 8,000 cached context tokens/minute at $0.40/M (+$0.0032), ~$0.0384/minute.

Mini model: 250 x $10/1M + 400 x $20/1M + 146 x $2.40/1M = $0.0025 + $0.008 + $0.00035 ~= $0.011, about 1.1 cents/minute before context. OpenAI notes the entire conversation becomes input to subsequent responses, so later turns grow more expensive; prompt caching helps but changing instructions, tools or history breaks the cache.

## 10. Full-duplex continuous cost

Two billing regimes. Speech-gated: only committed speech segments billed, silence filtered by VAD; looks like the 25 s/20 s calculation. Truly continuous: an always-running full-duplex model advances both streams for the entire wall-clock minute, including silence, listening and overlap; especially relevant to self-hosted systems where the GPU stays occupied even when no API token is billed.

Using OpenAI prices as a normalized token-price equivalent, large model continuous minute: input 60 s = 600 audio tokens, output 60 s = 1,200 audio tokens; 600 x $32/1M + 1,200 x $64/1M = $0.0192 + $0.0768 = $0.096/minute, about 9.6 cents per continuously active session-minute before text, context or tools. Mini model continuous: 600 x $10/1M + 1,200 x $20/1M = $0.006 + $0.024 = $0.030/minute. This is an economic normalization, not a claim that a particular API bills silence this way; OpenAI states its VAD can filter empty audio from token billing, but self-hosted full-duplex models still consume GPU cycles continuously.

## 11. Interaction model plus delegated reasoning

Assume a continuous interaction layer at the GPT-Realtime-2.1-mini equivalent, a background model at GPT-5.6 Terra, delegation once every five conversation minutes (0.2 jobs/minute), each background job 2,000 input + 300 output tokens, Terra pricing $2.50/M input and $15/M output.

Background job: 2,000 x $2.50/1M + 300 x $15/1M = $0.005 + $0.0045 = $0.0095/job. Amortized: 0.2 x $0.0095 = $0.0019/minute.

Continuous split system: $0.030 (interaction) + $0.0019 (background) = $0.0319/minute. Versus $0.096 large continuous: about 67% reduction. Speech-gated split: $0.01066 (mini interaction) + $0.0019 = $0.01256/minute. Versus $0.0352 large speech-gated: about 64% reduction. Architectures from Thinking Machines, KAME and DuplexOmni use this general split: the fast layer handles timing and conversational behavior while a stronger model or tool layer runs concurrently.

Sensitivity to heavier reasoning: a stronger background job on GPT-5.6 Sol (5,000 input at $5/M = $0.025; 1,000 output at $30/M = $0.030; $0.055/job) at 0.2 jobs/minute = $0.011/minute. Continuous split then $0.030 + $0.011 = $0.041/minute, still ~57% below the $0.096 large-continuous equivalent. The split loses its advantage when nearly every utterance delegates, background prompts include very large retrieved contexts, multiple speculative jobs launch and are discarded, or the interaction model itself is not materially smaller or cheaper.

## 12. Self-hosted cost formula

For self-hosted systems, token pricing is less useful than occupied GPU time. For one continuously running model, cost per minute is (GPU dollars/hour / 60) divided by (concurrent sessions per GPU x utilization). Full duplex tends to reserve compute continuously, reducing opportunities for aggressive batching. For a split architecture, cost is the reserved interaction-tier capacity plus (probability of delegation x background job cost). The interaction tier requires reserved low-latency capacity; the background tier can generally be pooled, batched and multiplexed because it is not responsible for every 100-200 ms conversational deadline. That infrastructure effect may be more important than per-token API pricing.

## 13. Cost comparison summary

| Architecture | Approx cost/minute | Latency profile |
| --- | --- | --- |
| Cascaded, inexpensive components | $0.013-$0.026 | 700-1,600 ms |
| Turn-based native, mini | $0.011-$0.015 | 450-900 ms |
| Turn-based native, large | $0.035-$0.067 | 300-800+ ms |
| Full-duplex large, continuously active | $0.096+ | 150-400 ms interaction |
| Full-duplex mini interaction + selective Terra delegation | $0.032 | 150-400 ms interaction; slower deep result |
| Full-duplex mini + heavy Sol delegation | $0.041 | Same interaction timing; higher answer quality |

These are inference estimates, not all-in operating costs.

## 14. Bottom line

1. The natural conversational target is 200-400 ms to first audible behavior. Under 500 ms is a strong practical target; p95 should stay below roughly 800 ms.
2. Silence-based endpointing is the primary structural problem in cascaded and turn-based systems. A 500 ms silence threshold consumes the entire natural-response budget before reasoning starts.
3. Cascaded systems remain economically efficient. Text operates at roughly 3-4 tokens per second of speech, while audio representations commonly require 10-25 billable tokens per second or substantially more raw codec tokens.
4. Full duplex buys latency by consuming continuous compute. It replaces serial waiting with always-on audio processing, parallel streams and speculative work.
5. A lightweight interaction model plus selective background reasoning is the strongest economic design. In the worked example it reduces cost by roughly 60-70% versus continuously running the large model, while retaining low conversational latency.
6. Context replay may become more expensive than the current utterance. Cache stability, context compaction and state externalization are therefore first-order cost controls.
7. Measure both interaction latency and answer latency. A fast backchannel can hide a two-second tool call, but it does not make the tool call faster.

---

# HIP Relevance Notes

1. This is HIP's native language rendered for voice: unit cost per token, made concrete. The headline result is that the interaction-model-plus-selective-delegation design (which is HIP's routing cascade) cuts cost 60-70% versus running the large model continuously, while keeping conversational latency. That is a quantified defense of the architecture HIP already built, in the terms HIP sells in.
2. The self-hosted formula (section 12) is the one that matters for HIP's operator-edge model, and it points somewhere the API pricing does not: the real economic lever is that the reasoning tier can be pooled and batched while only the interaction tier needs reserved low-latency capacity. That is an operator-infrastructure argument, not a token-price argument, and it favors HIP's edge-plus-cascade design over a monolithic continuous model.
3. Context replay as the dominant text cost (sections 8, 14) is a direct hook to HIP's fact graph. Cache stability, context compaction, and state externalization are named as first-order cost controls, and the governed fact graph is exactly a context-externalization and compaction mechanism. HIP's moat layer is also a cost-control layer.
4. Endpointing named again as the primary structural cost-and-latency problem. Consistent with P4. The near-term endpointing upgrade is not just a UX fix; it recovers the response-time budget the cost model says is otherwise consumed before reasoning starts.
5. Two-number measurement discipline (interaction latency vs answer latency) should be built into the HIP dashboard. The current dashboard tracks routing metrics; adding a clean split between time-to-acknowledge and time-to-answer would make HIP's latency story honest and measurable, and it maps to the interaction/reasoning split the whole architecture rests on.

# Reference Sources

Voice agent latency survey: arxiv.org/html/2503.04721v3
Opus RTP (RFC 7587): datatracker.ietf.org/doc/html/rfc7587
OpenAI Realtime session create: developers.openai.com/api/reference/resources/realtime/subresources/sessions/methods/create/
Deepgram pricing: deepgram.com/pricing
ElevenLabs API pricing: elevenlabs.io/pricing/api
Hello GPT-4o: openai.com/index/hello-gpt-4o/
OpenAI Realtime costs: developers.openai.com/api/docs/guides/realtime-costs
OpenAI pricing: developers.openai.com/api/docs/pricing
Moshi repo: github.com/kyutai-labs/moshi
Thinking Machines interaction models: thinkingmachines.ai/blog/interaction-models/
