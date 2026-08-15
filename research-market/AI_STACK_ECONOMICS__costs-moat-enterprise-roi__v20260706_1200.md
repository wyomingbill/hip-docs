# AI_STACK_ECONOMICS
Status: BUILT
Reconciled-Against: HIP WhitePaper (Parts XII-XIII) + financial model (cost-side), 2026-07-06

Completed 24-item research across 6 threads supporting HIP's structural economic argument:
distributed, open-weight, self-hosted AI is structurally advantaged over cloud-API-dependent.
Sources current to Q1 FY2027 / mid-2026.

Format per item: primary source, key data point, confirming source, caveat.

---

## Thread 1: NVIDIA margin dominance / the silicon tax

**1. NVIDIA datacenter GPU gross margin.**
NVIDIA Q1 FY2027 (May 20, 2026): GAAP gross margin 74.9%, non-GAAP 75.0% (companywide). Datacenter revenue $75.2B. FY2026 gross margin 71.1% GAAP.
CAVEAT: NVIDIA does not disclose datacenter-GPU-only gross margin. Defensible claim: "overall gross margin mid-70s, datacenter is dominant segment," NOT "datacenter GPU margin is exactly 75%."

**2. NVIDIA datacenter revenue trajectory.**
$39.1B Q1 FY2026 → $62.3B Q4 FY2026 → $193.7B FY2026 → $75.2B Q1 FY2027 (+92% YoY). Omdia: AI datacenter GPU/accelerator shipments $123B (2024) → $207B expected (2025).
CAVEAT: "Data Center" includes networking, not pure GPU.

**3. NVIDIA AI accelerator market share.**
Reuters (Feb 2025): ~80% share. China-specific ~55% after export-restriction mix shift.
CAVEAT: total-accelerator share, not a clean training-vs-inference split.

**4. Alternative silicon pricing.**
Google TPU v5p ~$4.20/chip-hr, v5e ~$1.20/chip-hr. AWS Trainium2 (Trn2): 30–40% better price-performance vs P5e/P5en GPU instances. Groq: GPT-OSS-20B $0.075 in / $0.30 out per M tokens; Llama 3.1 8B $0.05 in / $0.08 out. AMD MI300X cloud ~$2–6/GPU-hr.
CAVEAT: TPU/Trainium sold as cloud capacity, not retail silicon.

---

## Thread 2: Cloud markup over bare-metal

**5. Cloud GPU vs bare-metal.**
AWS P5 H100 on-demand ~$55.04/hr for 8 GPUs (~$6.88/GPU-hr). CoreWeave HGX H100 ~$49.24/hr for 8. RunPod H100 SXM from ~$3.29/hr.
CAVEAT: clean "3–10x markup" claim needs utilization/depreciation/power/labor assumptions. Rate cards prove price dispersion, not universal markup.

**6. a16z Cost of Cloud.**
a16z (2021): cloud repatriation cuts spend ~50% at scale. a16z (2023): some AI companies spend >80% of capital raised on compute.
CAVEAT: No strong 2024–26 a16z AI-inference-specific restatement found. Use the two originals, not a nonexistent update.

**7. Neocloud vs hyperscaler.**
RunPod H100 SXM ~$3.29/hr vs AWS P5 ~$6.88/GPU-hr.
CAVEAT: "38–66% below hyperscaler" directionally defensible; exact % varies by region/term/type.

**8. Inference cost/token trajectory.**
a16z LLMflation (Nov 2024): ~10x/yr decline; GPT-3-level $60/M tokens (2021) → Llama 3.2 3B ~$0.06/M (1,000x in ~3yr). Epoch AI (Mar 2025): 9x–900x/yr depending on task. 2026 preprint: ~600x decline 2020–2026.
CAVEAT: "600x" is method-sensitive (benchmark-equivalent, not same model family).

---

## Thread 3: Value extraction in closed-model APIs

**9. Closed-model per-token pricing / margin.**
OpenAI GPT-5.5: $2.50 in / $15 out (short context), $5 / $22.50 (long). Anthropic Claude Sonnet 5: $2/$10 intro through Aug 31 2026, then $3/$15. Gemini: $0.10–1.50 in / $0.40–9 out. The Information (Jan 2026): Anthropic lowered 2025 gross-margin projection to ~40% citing inference cost.
CAVEAT: API prices strong; margin estimates weak/paywalled.

**10. Enterprise data flows to model vendors.**
⚠️ STRONGEST EVIDENCE CUTS AGAINST THE BLUNT CLAIM. OpenAI/Anthropic/Google all state business/API data NOT used for training by default. Defensible version: "consumer or opted-in usage can improve shared models; enterprise/API contracts increasingly wall this off."
DO NOT overclaim this in the pitch. HIP's privacy argument is strongest for CONSUMER/household data only.

**11. Vendor lock-in at model API layer.**
Gartner (Nov 2025): unmanaged GenAI technical debt will delay upgrades/raise costs for 50% of enterprises by 2030. BCG (2025): platform switching costs exceed $20M/yr in some cases.
CAVEAT: evidence for prompt/RAG/eval rewrite cost specifically (OpenAI↔Anthropic) still thin.

**12. Oracle/database lock-in parallel.**
NO strong primary source drawing the formal analogy. Use as your own framing, not a sourced analyst claim.

---

## Thread 4: Enterprise AI ROI / pilot-to-production wall

**13. BCG AI deployment.**
BCG "Widening AI Value Gap" (Sept 2025, 1,250+ firms): only 5% achieving AI value at scale; 60% little/no material value.
CAVEAT: This is value-at-scale, NOT "70% of pilots fail to reach production." Do not conflate.

**14. McKinsey State of AI (Nov 2025).**
23% scaling an agentic system somewhere; in any individual function, ≤10% scaling agents. Gartner: 30% of GenAI projects abandoned after POC by end-2025.
CAVEAT: McKinsey reports scaling, not a clean "significant ROI" %.

**15. Cost unpredictability as scaling barrier.**
Gartner: escalating costs a named reason 30% of GenAI projects abandoned post-POC. 2026 preprint: agentic tasks use vastly more tokens than chat, high run-to-run variance, poor predictability.

**16. Enterprise migration to self-hosted open weights.**
Reuters (Jul 2026): enterprises shifting from single-provider reliance toward mixed/open-source for flexibility and fine-tuning control.
CAVEAT: named OpenAI/Anthropic → self-hosted Llama/Mistral case studies still sparse.

**17. Data governance as barrier.**
Deloitte (2025): data management, cybersecurity, governance necessary for safe agentic deployment.

---

## Thread 5: Application-layer thinness + context moat

**18. Application-layer differentiation.**
McKinsey (May 2026): when everyone has the same models, winners build advantages competitors cannot copy; same LLMs for productivity is NOT durable advantage. a16z (Mar 2026): AI strengthens durable moats (proprietary data, network effects, brand, embedded workflows).
CAVEAT: "Layer 4 is thinnest" is your framing, not sourced.

**19. Context as competitive moat. ← DIRECT SUPPORT for HIP**
McKinsey (May 2026): privileged data becomes a moat when models deliver capabilities competitors cannot copy; every interaction generates labeled data feeding a compounding flywheel. BCG (Dec 2025): embed proprietary intelligence/context.
CAVEAT: context must be proprietary, cumulative, governed, workflow-tied.

**20. Switching cost from accumulated context. ← DIRECT SUPPORT for HIP**
Stanford Digital Economy Lab (Mar 2026): next-gen personalization requires portable, persistent, user-governed personal memory that persists across interactions and moves across tools. McKinsey: embedded AI creates switching costs via integration, workflow redesign, retraining.

---

## Thread 6: Open-weight economics

**21. TCO self-hosted vs cloud API. ← CRITICAL CAVEAT**
Meta Llama 3.1 (Jul 2024): runs on-prem/cloud/local without sharing data with Meta. 2026 preprint "Beyond Per-Token Pricing": self-hosted H100 ranges $0.21–$15.25 per M output tokens depending HEAVILY on utilization; idle/low-throughput destroys economics.
⚠️ CRITICAL: HIP's entire cost advantage rests on high node utilization. Low utilization kills the unit economics. subs_per_node is the make-or-break input.

**22. Open-weight adoption growth.**
Hugging Face (Mar 2026): 13M users, 2M+ public models, 500K+ datasets, ~doubling; 30%+ of Fortune 500 have verified accounts. Stanford AI Index: 5.6M AI projects on GitHub, Llama 1B+ downloads 2025.

**23. Enterprise open-weight adoption survey.**
No clean Gartner/Forrester % found. Best proxy: 30%+ Fortune 500 on Hugging Face.
CAVEAT: do not claim "X% of enterprises deploy open weights" without a paywalled number.

**24. Inference cost advantage of open weights.**
Groq: Llama 3.1 8B $0.05/$0.08, Llama 3.3 70B $0.59/$0.79 per M tokens vs GPT-5.5 $2.50–5 in / $15–22.50 out and Claude Sonnet 5 $3/$15. 2026 preprints: 40x–200x cheaper on electricity-only basis (consumer/self-hosted).
CAVEAT: 10x–20x advantage defensible for smaller open models at HIGH utilization. NOT automatic for frontier-quality, long-context, or poorly-utilized deployments.

---

## MODEL IMPLICATIONS

1. **Utilization is load-bearing (items 21, 24).** HIP's entire cost advantage rests on high node utilization. subs_per_node / node utilization is the make-or-break input in the financial model.

2. **Context-as-moat is now sourced (items 19, 20).** McKinsey May 2026 + Stanford Mar 2026 directly support HIP's "context compounds, models commoditize" thesis and the portable/user-governed memory framing. This graduates the moat argument from assertion to cited.

3. **The silicon tax is real and quantified (items 1–3).** NVIDIA mid-70s margin, ~80% share = the tax every deployment pays. Supports HIP owning the edge rather than renting frontier API.

4. **The pilot-to-production wall is real but must be cited precisely (items 13, 14).** BCG 5%-at-scale / 60%-no-value, NOT "70% of pilots fail." Gartner 30%-abandoned-post-POC.

5. **Do NOT overclaim enterprise data harvesting (item 10).** Enterprise/API data is increasingly walled off by default. HIP's privacy argument is strongest for CONSUMER/household data, weakest if framed as "enterprises feed competitors."
