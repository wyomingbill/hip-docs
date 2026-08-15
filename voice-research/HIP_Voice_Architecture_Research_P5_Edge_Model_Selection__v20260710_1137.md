---
doc: HIP Voice Architecture Research
part: P5 of the voice architecture research set
topic: Edge model selection for the interaction layer, Jetson Orin Nano Super and RTX PRO 6000 Blackwell
source: ChatGPT deep research output (prompt 5 of 8), reviewed and marked down
status: reference
version: v20260710_1137
location: ~/hip-dev/docs/voice-research/
note: RTF export mangled some math and diagrams; those are reconstructed in plain notation from the source text. Tables preserved.
---

# Edge Model Selection for the Interaction Layer

## Bottom line

For the Jetson Orin Nano Super, use a small text interaction model in a cascaded architecture. The practical candidates are Llama 3.2 1B/3B, Qwen2.5 0.5B/1.5B, or a similarly small controller fine-tuned for turn decisions. None of the currently credible open-weight, audio-native full-duplex systems fits comfortably into the Jetson's 8 GB shared memory while preserving real-time operation.

For the RTX PRO 6000 Blackwell 96 GB, the strongest purpose-built choices are, in order:

1. PersonaPlex-7B, the best available open-weight model for configurable roles, voices, interruptions and backchannels.
2. Moshi-7B, the simplest and best-documented genuinely full-duplex baseline.
3. A hybrid small controller plus larger asynchronous reasoning model, which is likely the best production design.
4. LLaMA-Omni 2 1.5B or 3B, materially smaller but turn-based rather than genuinely simultaneous full-duplex.

Only Moshi and PersonaPlex have credible evidence of sub-300 ms conversational response or interruption behavior as complete audio-native systems. Their published measurements are not on the RTX PRO 6000 specifically, but that GPU has more than enough compute and memory; software support and kernel efficiency will dominate.

## Hardware constraints

### Jetson Orin Nano Super

The device has 8 GB shared LPDDR5 memory, approximately 102 GB/s memory bandwidth, an Ampere GPU architecture, up to 67 INT8 TOPS, and no Blackwell NVFP4 tensor-core execution. NVIDIA positions it for models as large as 8B, but "loads successfully" is not the same as supporting a full speech stack, KV cache, audio codecs and low-latency duplex generation simultaneously.

For a voice system, reserve roughly 0.5 to 1.5 GB for OS, CUDA and runtime; 0.5 to 2 GB for STT; 0.3 to 1 GB for TTS; and 0.5 to 1.5 GB for KV cache and application state. That leaves approximately 3 to 5 GB for the conversational model in a robust deployment.

### RTX PRO 6000 Blackwell

The server/workstation variants provide 96 GB GDDR7 and native Blackwell low-precision acceleration. NVIDIA's NIM and TensorRT-LLM support matrices include RTX PRO 6000 Blackwell profiles using NVFP4, FP8 and BF16 for supported text models. The issue is therefore not capacity. It is whether the model's custom audio codec, multistream scheduler and decoder are implemented in an optimized stack.

## Candidate comparison

Memory figures marked estimated are weight-only or practical runtime estimates from parameter counts. Published projects generally do not provide reproducible peak-VRAM numbers across both requested devices.

| Candidate | Nominal params | Architecture | Genuine full-duplex? | License | Quantization | Approx runtime memory | Published latency | Jetson? | RTX PRO 6000? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Moshi / Moshika | ~7B LLM + Mimi codec | Audio-native, parallel user/assistant audio streams | Yes | CC BY 4.0 weights | Mostly BF16/FP16; community low-bit exists; no official NIM/NVFP4 | ~14-16 GB weights BF16; typically 20-24+ GB runtime | 160 ms theoretical; ~200 ms practical on L4 | No | Yes; sub-300 ms plausible |
| PersonaPlex-7B | 7B | Audio-native Moshi derivative with role and voice conditioning | Yes | NVIDIA Open Model License; MIT code | Official PyTorch; no standard NIM/llama.cpp/vLLM path; no official NVFP4 | At least ~14 GB BF16; ~24 GB VRAM practical | 170 ms smooth-turn; 240 ms interruption-stop on A100 | No | Yes; sub-300 ms plausible |
| Freeze-Omni | Qwen2-7B + ~470M speech enc/dec | Modular audio-native I/O around frozen text LLM | Limited duplex via interruption-state prediction | Per-checkpoint terms; not clean standard license | No official FP4; INT8/AWQ possible for backbone; custom audio layers remain | ~15-18 GB BF16; >20 GB practical | 745 ms model-side avg after interruption; ~1.2 s real-world est | No | Yes, but not sub-300 ms |
| LLaMA-Omni 2 0.5B | 0.5B LLM + 0.5B TTS LM + Whisper-large-v3 + flow/vocoder | Integrated modular SpeechLM | No; turn-based streaming | Check checkpoint-specific Qwen/Whisper/CosyVoice terms | Quantizable components; no official integrated GGUF/NIM/NVFP4 | ~4-7 GB BF16 total; lower with mixed INT8/INT4 | 543 ms reported | Marginal; likely memory-constrained | Yes; not sub-300 ms end-to-end |
| LLaMA-Omni 2 1.5B | 1.5B LLM + same speech stack | Integrated modular SpeechLM | No | Same caveat | Backbone AWQ/GPTQ/GGUF; full stack not in llama.cpp/vLLM | ~6-9 GB BF16; ~4-6 GB aggressively quantized | 553 ms reported | No practical headroom | Yes; not sub-300 ms |
| LLaMA-Omni 2 3B | 3B LLM + ~0.5B TTS + speech | Integrated modular SpeechLM | No | Same caveat | Same | ~9-13 GB BF16; ~5-8 GB mixed low-bit | 568 ms reported | No | Yes; not sub-300 ms |
| MiniCPM-Duplex | 2.4B backbone | Text-oriented duplex; receives input while generating | Duplex at model/control level; not Moshi-style continuous speech | Check checkpoint terms | Conventional low-bit LLM quant; no standard speech NIM | ~4.8 GB BF16; ~2-3 GB INT8/INT4 plus cache | No solid hardware-specific sub-300 ms located | Potentially, with INT4 | Yes |
| DuplexCascade | Qwen2-7B + ASR/TTS | VAD-free cascaded ASR-LLM-TTS using micro-turns | Functionally full-duplex, not audio-native | Check component/checkpoint licenses | Backbone INT8/INT4; components independently quantized | Usually >10 GB total depending on ASR/TTS | No RTX PRO/Jetson number published | No at 7B config | Yes; sub-300 ms unproven |
| Llama 3.2 1B Instruct | 1.24B-class | Text-only cascaded interaction controller | No; needs streaming STT/TTS + duplex controller | Llama 3.2 Community License | GGUF Q4/Q5/Q8, AWQ; ~2 GB INT8; ~1.8-2.3 GB Q4 plus KV | Jetson figures ~27-28 tokens/s quantized | Yes at Q4/INT4 | Easily sub-300 ms model TTFT | Yes |
| DeepSeek-R1-Distill-Llama-8B | 8B | Text-only reasoning model | No | Llama 3.1 license | GGUF/AWQ/GPTQ; vLLM; possible TensorRT-LLM | ~16 GB BF16; ~8 GB INT8; ~4.5-6 GB Q4 plus KV | No relevant full-duplex figure | Loads only at aggressive Q4, poor fit | Fast on RTX, wrong behavioral profile |

## Purpose-built audio interaction models

**Moshi.** Based on a 7B Helium language model and the Mimi streaming codec. It models two synchronized streams (incoming user codec tokens and outgoing assistant tokens through a multistream Transformer), predicts time-aligned text as an internal semantic stream, then acoustic codec layers. It does not require a VAD-defined turn boundary and can continue listening while emitting speech. Official paths: PyTorch, Rust/Candle, MLX. It is not a standard decoder-only Hugging Face model and cannot drop into llama.cpp, vLLM, or NVIDIA NIM for LLMs, which assume conventional text-token generation. There is no official NVFP4/FP4/INT8 production checkpoint; quantizing only the Helium backbone is insufficient because the custom temporal transformer, codec heads and Mimi decoder must stay synchronized in real time. Verdict: not viable on 8 GB Jetson; viable with headroom on RTX PRO 6000; sub-300 ms yes based on L4 results.

**PersonaPlex.** A 7B Moshi-derived model that receives live user audio while autoregressively generating text and speech. Adds text role prompting, audio voice prompting, voice cloning, customer-service role adherence, interruption behavior and backchannels. NVIDIA reports 170 ms smooth turn-taking and 240 ms interruption latency, measured on an A100 using PyTorch. It inherits Moshi's runtime requirements rather than fitting ordinary LLM servers. Verdict: no on Jetson; yes on RTX PRO 6000. It is currently the most useful open-weight interaction-layer model.

**Freeze-Omni.** Better understood as a speech interface around an ordinary text LLM (Qwen2-7B-Instruct plus ~350M speech encoder and ~120M speech decoder) than as a minimal full-duplex model. A chunk-wise state classifier detects continued user speech, interruption, and whether generation should stop. Measured model-side latency was 745 ms average on A100 BF16, excluding 160-320 ms endpoint/state-detection; authors estimate ~1.2 s including network. Too large and too slow for the edge target.

**LLaMA-Omni 2.** Despite the name, based on Qwen2.5, not Meta Llama. Available with 0.5B through 14B backbones. Every size also uses Whisper-large-v3 as speech encoder, a separate 0.5B TTS language model, flow matching and a vocoder, so even the 0.5B version is not a 0.5B total system. Latency 543 ms (0.5B) to 568 ms (3B). Useful for RTX experimentation, neither truly full-duplex nor a clean Jetson candidate.

**MiniCPM-Duplex.** 2.4B MiniCPM backbone designed to accept new input while generating. Relevant as a model-level interruption controller, but weaker public evidence than Moshi or PersonaPlex for continuous audio-native speech. Research candidate, not a drop-in production engine.

**DuplexCascade.** Architecturally significant because it obtains full-duplex behavior without a monolithic audio model: streaming ASR, then Qwen2-7B with micro-turn control tokens, then streaming TTS. It observes control events (user speaking, user finished, user interruption, user thinking, backchannel) and avoids a single hard VAD endpoint by converting conversation into short micro-turns. The released 7B config is too large for an Orin Nano once ASR and TTS are included, but the design is directly applicable to a 1B-3B controller.

## Small text models for a cascaded interaction layer

**Llama 3.2 1B and 3B.** The most relevant Llama variants, produced by structured pruning from Llama 3.1 8B and knowledge distillation from larger teachers. Not audio-native. Their role in the pipeline:

```text
streaming acoustic features
   -> incremental STT / prosodic classifier
   -> Llama 3.2 interaction controller emitting one of:
        WAIT / BACKCHANNEL / SPEAK / STOP / DELEGATE / TOOL
   -> streaming TTS
```

Llama 3.2 1B is best for turn-state classification, deciding whether to speak, selecting acknowledgment phrases, identifying interruption intent, deciding whether to delegate, and producing short fillers. At INT8 or Q4 it fits easily on the Jetson with room for audio components.

Llama 3.2 3B is better for coherent short answers, role consistency, light tool selection, reformulating partial results, and basic conversation repair. Quantized 3B has been reported around 27-28 tokens/s on the Orin Nano Super class. At that rate each token takes ~36 ms, so a first audible phrase of four to six tokens needs roughly 145-220 ms after prefill and after TTS begins consuming text. Sub-300 ms is plausible only when context is short or KV state is persistent, STT delivers stable partial tokens before the user stops, the model produces a short control action or backchannel, and TTS begins on the first few tokens. It does not guarantee sub-300 ms for a complete novel answer after the user finishes.

**DeepSeek-R1-Distill-Llama-8B.** Technically a distilled Llama variant but a poor interaction model: 8B is too large for the Jetson's complete voice stack, it is optimized for extended reasoning, it tends to generate long deliberative outputs, and reasoning behavior works against rapid conversational control. Use it as an asynchronous reasoning layer on the RTX PRO 6000, not as the real-time floor controller.

## Quantization and inference-stack compatibility

### Jetson Orin Nano Super

FP4 is not a meaningful acceleration path here; the Orin Nano is Ampere, not Blackwell, with no native NVFP4 tensor-core execution. An FP4 checkpoint may be dequantized internally with little compute advantage. INT8 is hardware-supported, but for decoder-only LLMs, memory-bandwidth reduction is often more valuable than raw INT8 TOPS. Useful formats: INT8 weights, INT8 activation quantization where calibrated kernels exist, AWQ/GPTQ INT4, GGUF Q4_K_M or Q5_K_M.

Recommended runtime, in order: llama.cpp / Ollama with CUDA offload for 1B-3B models; MLC-LLM or TinyChat/AWQ where the architecture is supported; experimental Jetson TensorRT-LLM only with caution (its official Jetson work initially targeted AGX Orin; Orin Nano support has remained more experimental). AWQ/TinyChat explicitly supports Jetson Orin-class edge GPUs. vLLM is not the first choice on an 8 GB Jetson; its allocator, paged KV cache and server overhead target throughput and concurrency rather than minimal single-session edge latency.

### RTX PRO 6000 Blackwell

FP4/NVFP4 is best for supported conventional text LLMs through TensorRT-LLM, NVIDIA NIM, NVIDIA Model Optimizer, and supported vLLM quantization paths. NVIDIA Model Optimizer supports quantization and export into TensorRT-LLM, TensorRT, vLLM and SGLang, including NVFP4 workflows. INT8 is useful where NVFP4 support is unavailable, particularly for Whisper encoders, classifiers, conventional transformer components, and TTS acoustic models. NIM is relevant to the text reasoning or interaction-controller model, not to Moshi or PersonaPlex as currently released. vLLM is best for Llama 3.2, DeepSeek distilled models, Qwen, asynchronous reasoning services, and high-concurrency delegation, but not for Moshi's or PersonaPlex's native multistream audio decoding without substantial custom model-runner work. llama.cpp is useful for a small controller but cannot directly run the complete purpose-built audio-native models.

## Sub-300 ms assessment

Distinguish four latencies: decision latency (time to decide WAIT/STOP/BACKCHANNEL/SPEAK), first-token latency, first-audio latency, and complete response latency.

| Model/system | Jetson | RTX PRO 6000 | Realistically under 300 ms? |
| --- | --- | --- | --- |
| Moshi | No | Yes | Audio reaction and first speech |
| PersonaPlex | No | Yes | Smooth turn start and interruption stop |
| Freeze-Omni | No | No | Possibly interruption-state classification only |
| LLaMA-Omni 2 | No reliable case | No published sub-300 ms end-to-end | LLM stage alone |
| Llama 3.2 1B cascade | Yes | Yes | Control decision, backchannel, first few text tokens |
| Llama 3.2 3B cascade | Conditionally | Yes | Short decision or phrase with warm KV cache |
| DeepSeek-R1-Distill-8B | No | Model TTFT yes; answer generally no | Not appropriate for interaction loop |
| DuplexCascade 7B | No | Unproven | Individual micro-turn decisions may be under 300 ms |

## Recommended architecture

**Jetson Orin Nano Super:**

```text
AEC / denoise
   -> small streaming ASR (partial transcript)
   -> speech probability + pitch/energy + pause duration
   -> Llama 3.2 1B or 3B Q4 interaction controller, choosing:
        continue listening / acknowledge / interrupt output /
        answer locally / delegate to RTX server
   -> small streaming TTS
```

Use Llama 3.2 1B INT8/Q4 if the controller mainly emits actions; Llama 3.2 3B Q4 if it must also generate short conversational language. Do not make it produce long answers; constrain it to a small action vocabulary plus very short utterances.

**RTX PRO 6000 Blackwell:** run two layers. A PersonaPlex or Moshi real-time audio interaction loop (immediate turn-taking, backchannels, interruption handling, short conversational output), and an asynchronous text reasoning service (Llama/Qwen/distilled model under vLLM or NIM) whose result is injected into the ongoing interaction. For a prototype, choose PersonaPlex over Moshi because role prompting and voice conditioning make it easier to turn the raw duplex model into a defined assistant. For a research baseline or maximum architectural transparency, choose Moshi.

The Jetson should not attempt to run PersonaPlex or Moshi locally. It should operate as the room-side audio processor, speaker/turn controller and privacy gateway, with the full audio-native interaction model on the RTX PRO 6000.

---

# HIP Relevance Notes

1. This directly answers HIP's two-hardware question. The split is clean: Jetson is the room-side processor and privacy gateway running a quantized 1B-3B controller; the RTX PRO 6000 hosts the full audio-native interaction model plus the async reasoning tier. That maps onto HIP's existing edge-to-frontier cascade with the interaction model living at the RTX tier, not the Jetson.
2. The current HIP enclave target (RTX PRO 6000 Blackwell, Llama 4 Scout FP4 via NIM) is the right home for the reasoning tier and, per this research, also the only viable home for a Moshi/PersonaPlex-class interaction model. The Jetson cannot host either. That is a hard architectural fact to carry into the deployment-model decision.
3. PersonaPlex is the concrete prototype starting point named here, and it is NVIDIA-licensed, which fits the existing NVIDIA revenue-share/credit-support relationship already in the NDA. Worth noting the alignment: the recommended interaction model and HIP's named infrastructure partner are the same vendor.
4. Sub-300 ms on the Jetson is achievable only for control decisions and backchannels, never for full novel answers. That confirms the P4 conclusion and sets the honest expectation for the edge tier: it is a floor controller and gap-filler, not an answerer. Answers come from the RTX tier.
5. No 1-3B checkpoint yet demonstrates Moshi-class full-duplex with action-token control and multi-user identity scoping. Distilling one is a research program, not a download. This is the same whitespace the interaction-OS note flagged, now stated at the model level: the small governed interaction model HIP would want does not exist and would have to be built.

# Reference Sources

NVIDIA Jetson Orin Nano Super boost: developer.nvidia.com/blog/nvidia-jetson-orin-nano-developer-kit-gets-a-super-boost/
NVIDIA NIM supported models: docs.nvidia.com/nim/large-language-models/1.15.0/supported-models.html
Moshi repo: github.com/kyutai-labs/moshi
Moshi paper: arxiv.org/abs/2410.00037
PersonaPlex (NVIDIA ADLR): research.nvidia.com/labs/adlr/personaplex/
PersonaPlex paper: arxiv.org/abs/2602.06053
PersonaPlex weights: huggingface.co/nvidia/personaplex-7b-v1
Freeze-Omni: arxiv.org/html/2411.00774v3
LLaMA-Omni 2 repo: github.com/ictnlp/LLaMA-Omni2
LLaMA-Omni 2 paper: arxiv.org/html/2505.02625v1
MiniCPM-Duplex: github.com/thunlp/duplex-model
DuplexCascade: arxiv.org/abs/2603.09180
Llama 3.2 edge/mobile: ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/
Jetson LLM benchmarking: ericxliu.me/posts/benchmarking-llms-on-jetson-orin-nano/
DeepSeek-R1-Distill-Llama-8B: huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B
TensorRT-LLM: github.com/NVIDIA/TensorRT-LLM
LLM-AWQ: github.com/mit-han-lab/llm-awq
NVIDIA Model Optimizer: github.com/NVIDIA/Model-Optimizer
