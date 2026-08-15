# HIP_CuratorResearch: How a Learned Per-Household Retrieval Ranker Is Actually Built
Status: BUILT
Reconciled-Against: roadmap 7b7a8b1 (code/REQ reads 2026-07-27 session: harness/write_rule.py, harness/injection_contract.py, harness/orchestrator.py, harness/epistemic_record.py, harness/partition_crypto.py, REQ_LEARNER_SIGNAL_ISOLATION v20260727_0828, REQ_PARTITION_CUSTODY v20260721_0831, HIP_ContextArch_Reconciliation v20260726_0710); literature verified against primary sources 2026-07-28

## What this is

Research memo, analysis only — ratifies nothing, changes no code. Scopes the
"Curator": a learned model that decides, per query, which of a household's
stored facts to pull into the prompt (today: fixed rules). Parts 1–6 survey
the field from primary sources (three parallel research passes; every
load-bearing claim cited, verification tier flagged). Part 7 applies it to
HIP as engineering recommendations, grounded in the roadmap code and REQs
read this session. Per DISPATCH 38a's ratified framing, this scopes the
GATED MOAT TRACK — retrieval stays rule-based today; this memo defines what
entering that track would actually mean.

Verification labels: claims are cited to primary sources opened directly
during research; figures from search snippets or extrapolation are flagged
inline. Where the field is unsettled, that is stated, not papered over.

---

## Part 1 — What the Curator is, in known terms

The Curator is a **learning-to-rank problem over a tiny personal corpus,
downstream of an authorization gate**. In the literature's taxonomy it is the
"rerank" stage of a two-stage pipeline: candidate generation (rules + INJ
contract) → rerank top-k → context assembly. The model families:

| Family | Size | Latency | Edge/CPE viable? | Needs fact text? |
|---|---|---|---|---|
| **Feature-based LTR (GBDT/LambdaMART, logistic)** | KBs–MBs | **9.6–52 µs/prediction** on x86 CPU ([lleaves benchmark](https://github.com/siboehm/lleaves)) | Trivially | **No — the only text-free family** |
| Dense bi-encoders (all-MiniLM-L6-v2 22.7M; [nomic-embed 137M](https://arxiv.org/abs/2402.01613); BGE-small 33M) | 22–137M | ~1–2 ms/encode x86 CPU ([sbert.net](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html), hardware unspecified) | Yes for inference | Yes (metadata must be serialized to text — folklore practice, no canonical citation) |
| Learned sparse ([SPLADE-v3](https://arxiv.org/abs/2403.06789); [inference-free splade-v3-doc](https://huggingface.co/naver/splade-v3-doc)) | ~66–110M | doc-side variant: zero query-time neural cost | Yes (doc-side variant) | Yes |
| Cross-encoder rerankers ([ms-marco-MiniLM-L-6-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2), 22.7M) | 22M–0.6B | 1,800 docs/s on V100; **no primary source publishes CPU per-pair latency** — third-party anecdote ~100–300 ms per 50 pairs | Plausible at MiniLM scale, unbenchmarked on ARM | Yes (query+doc pair) |
| LLM-as-reranker ([RankGPT](https://arxiv.org/abs/2304.09542)) | 7B+ | ~$0.60/query (GPT-4, 2023 prices), 17–20K tokens/query | No | Yes, full text |

**RAG-with-trained-retriever** ([REALM](https://arxiv.org/abs/2002.08909),
[RAG](https://arxiv.org/abs/2005.11401), [Atlas](https://arxiv.org/abs/2208.03299),
[REPLUG](https://arxiv.org/abs/2301.12652)) trains the retriever against the
generator's likelihood — at **13M–387M passages**. A deliberate search found
**no published trained-retriever work at tens-to-hundreds-of-documents
scale**; whether those training signals function at all with hundreds of
candidates is an open question no paper addresses.
[Self-RAG](https://arxiv.org/abs/2310.11511) — the current-practice
direction — does not train the retriever at all.

---

## Part 2 — Training it

**Implicit feedback → labels.** The founding move is
[Joachims KDD 2002](https://www.cs.cornell.edu/people/tj/publications/joachims_02c.pdf):
treat interactions as **pairwise preferences**, not absolute labels. His
group-level ranker beat 2001-era Google with ~260 clicked queries across ~20
users — the only classic result putting a number on small-cohort ranking.
(Verified against the PDF; a circulating "1,493 examples" figure is NOT in
the paper.) The eye-tracking work
([Joachims et al. SIGIR 2005 / TOIS 2007](https://www.cs.cornell.edu/people/tj/publications/joachims_etal_07a.pdf))
established clicks are position-biased and trust-biased but *relative*
preferences are reliable;
[Craswell et al. WSDM 2008](https://www.microsoft.com/en-us/research/publication/an-experimental-comparison-of-click-position-bias-models/)
gave the cascade model.

**Counterfactual LTR — and why HIP should mostly ignore it.** The IPS
framework ([Joachims/Swaminathan/Schnabel WSDM 2017](https://arxiv.org/abs/1608.04468))
debiases clicks given known propensities — requiring randomization or strong
click-model assumptions, plus enough data that importance-weight variance
doesn't swamp signal ([CRM](https://arxiv.org/abs/1502.02362)). Two
load-bearing negatives: [Oosterhuis 2022](https://arxiv.org/abs/2206.12204)
proves unbiasedness is mathematically limited to affine click behaviors; the
[Baidu-ULTR reproducibility study, SIGIR 2024](https://arxiv.org/abs/2404.02543)
found flagship ULTR methods largely failed to deliver on 1.2B real sessions.
**Nobody studies the tens-of-events regime — per-household IPS is out of the
question.** HIP's signals (corrections, accepted answers, overrides) are
deliberate judgments, not scan-order artifacts — they bypass most of
position/trust bias and land as clean pairwise labels in a 2002-style
objective. The literature on correction-trained retrieval specifically is
thin (nearest template:
[Lawrence &amp; Riezler, ACL 2018](https://aclanthology.org/P18-1169/),
counterfactual learning from human corrections in semantic parsing) — a gap,
not a blocker.

**Cold start and personalization architecture.** The documented industry arc
is **hand-tuned scoring → GBDT → NN, each stage only after the prior
plateaus** ([Airbnb KDD 2019](https://arxiv.org/pdf/1810.09591), verbatim:
"The very first implementation of search ranking was a manually crafted
scoring function"). Production per-tenant patterns: one global model with
tenant features (YouTube;
[Netflix — explicitly one foundation model, per-application not per-user fine-tunes](https://netflixtechblog.medium.com/integrating-netflixs-foundation-model-into-personalization-applications-cf176b5860eb));
global model + light on-device adaptation
([Gboard federated personalization](https://arxiv.org/abs/1910.10252));
MAML-style meta-learning ([MeLU](https://arxiv.org/pdf/1908.00413) —
research-only, and the field
[questions whether it beats tuned baselines](https://arxiv.org/pdf/2308.08354)).

**Model-per-household: skepticism confirmed, with one nuance.** Full separate
rankers per tenant loaded per request: **no production evidence anywhere**
after deliberate search — not Google personal search (global model over
per-user corpora: [SIGIR 2016](https://dl.acm.org/doi/10.1145/2911451.2911537),
[WSDM 2018](https://dl.acm.org/doi/10.1145/3159652.3159732)), not Netflix,
not YouTube. What IS production-real is **multi-LoRA adapter serving** —
[S-LoRA](https://arxiv.org/abs/2311.03285) (thousands of adapters/GPU),
[Punica](https://arxiv.org/abs/2310.18547),
[Predibase LoRAX](https://predibase.com/blog/lora-exchange-lorax-serve-100s-of-fine-tuned-llms-for-the-cost-of-one)
— i.e., shared frozen base + tiny per-tenant delta. No published number
answers "how many per-tenant events before per-tenant learning beats a
global prior"; triangulating from Joachims 2002, low-hundreds of clean
pairwise judgments is where dedicated adaptation historically started paying
off.

---

## Part 3 — Production and lifecycle

**Serving.** The reranker sits between candidate retrieval and context
assembly, scoring 24–100 candidates. Best production benchmark:
[Vespa 2021](https://blog.vespa.ai/pretrained-transformer-language-models-for-search-part-4/)
— adding an int8 MiniLM cross-encoder final phase cost ~18x throughput for
~10% MRR gain.
[Bing 2019](https://azure.microsoft.com/en-us/blog/bing-delivers-its-largest-improvement-in-search-experience-using-azure-gpus/):
77 ms/inference on 20 CPU cores was unacceptable *at web query volume* —
which is precisely not HIP's regime; a chat turn tolerates 100+ ms. Honest
gaps: no primary source exists for the oft-quoted "100–250 ms search SLA,"
and **no rigorous ARM/CPE transformer benchmark exists anywhere** —
Pi-5-class anecdotes imply single-pair MiniLM in tens-to-low-hundreds of ms;
measure locally. GBDT at µs/item is 3–4 orders of magnitude cheaper and
unambiguously CPE-safe.

**Lifecycle.** The documented pattern: offline eval gate → shadow/dark
launch → interleaving → A/B → canary ramp → rollback. Interleaving needs 1–2
orders of magnitude less data than A/B
([Chapelle et al. TOIS 2012](https://www.cs.cornell.edu/~tj/publications/chapelle_etal_12a.pdf);
[Netflix: >100x fewer users](https://netflixtechblog.com/interleaving-in-online-experiments-at-netflix-a04ee392ec55);
[Airbnb KDD 2025: up to 100x sensitivity](https://arxiv.org/abs/2508.00751))
— but still needs thousands of queries, **which a single household never
generates; no published lifecycle practice exists for the per-tenant-tiny
regime**. The canonical regression cautionary tale is
[Kohavi's "Five Puzzling Outcomes"](http://ai.stanford.edu/~ronnyk/puzzlingOutcomesInControlledExperiments.pdf):
a Bing ranking *bug* raised queries/user >10% and revenue >30% — short-term
engagement moves the wrong way under regression; gate on an outcome-level
metric (sessions, task success).

**Evaluation honesty.** Offline nDCG correlates *weakly* with RAG answer
quality — [eRAG, SIGIR 2024](https://arxiv.org/abs/2404.13781): "small
correlation with the RAG system's downstream performance." Position in
context matters independently of recall
([Lost in the Middle](https://arxiv.org/abs/2307.03172)); highly-ranked
plausible distractors hurt while random noise can help
([Power of Noise, SIGIR 2024](https://arxiv.org/abs/2401.14887)). LLM-judge
frameworks ([RAGAS](https://arxiv.org/abs/2309.15217)) have documented
reliability problems ([telecom critique](https://arxiv.org/abs/2407.12873));
the rigorous alternative ([ARES](https://arxiv.org/abs/2311.09476))
reintroduces human labels. **"Did retrieval help the answer" has no settled
measurement** — and it is the metric the DISPATCH 38a entry gate depends on.
HIP's D-24/T02-class defects — authorized true facts silently dropped — are
the *easy* measurable case: retrieval failure with known ground truth.

---

## Part 4 — Federated learning, concretely

**Mechanics and real deployments.**
[FedAvg](https://arxiv.org/abs/1602.05629) (McMahan 2017): server ships
model to a client sample; clients run local epochs; server does
example-weighted averaging; 10–100x fewer rounds than distributed SGD. The
flagship deployment is Gboard:
[1.4M-param LSTM, 100–500 clients/round, 3,000 rounds over 4–5 days; the federated model beat the server-trained one in production](https://arxiv.org/abs/1811.03604).
The client loop physically
([Bonawitz MLSys 2019](https://arxiv.org/abs/1902.01046)): check-in gated on
charging+WiFi+idle, 130% over-selection, 6–10% dropout/round, ephemeral
in-memory aggregation, 2–3 min/round. Apple runs private FL for
QuickType/Hey-Siri (WWDC19) but publishes almost no operational numbers.
Cross-silo:
[EXAM, 20 hospitals, Nature Medicine 2021](https://www.nature.com/articles/s41591-021-01506-3)
(snippet-verified); MELLODDY (10 pharma companies).

**The attacks are real and better than people assume.**
[Deep Leakage from Gradients](https://arxiv.org/abs/1906.08935)
(pixel/token-exact at small batch);
[Inverting Gradients](https://arxiv.org/abs/2003.14053) — single ImageNet
image from a ResNet-152 gradient, recognizable images even from batch-100,
reconstruction "unimpeded" after 100 local FedAvg steps;
[Data Leakage in FedAvg](https://arxiv.org/abs/2206.12395) — >45% of client
images from realistic multi-epoch updates. For text:
[LAMP](https://arxiv.org/abs/2202.08827) and
[FILM](https://arxiv.org/abs/2205.08514) — high-fidelity sentence recovery
from batches up to 128. Malicious-server results void naive trust:
[Robbing the Fed](https://arxiv.org/abs/2110.13057) (weights crafted so data
is linearly encoded in updates) and
[Eluding Secure Aggregation](https://arxiv.org/abs/2111.07380) (inconsistent
models per client make the SecAgg "sum" equal one victim's update — works
against ANY SecAgg, any cohort size).

**Defenses and who runs what.**
[SecAgg](https://eprint.iacr.org/2017/281) (pairwise masking +
Shamir-shared seeds, ~1.7–2x communication overhead, quadratic compute → run
over cohorts of hundreds); [SecAgg+](https://eprint.iacr.org/2020/704) makes
it polylog. [DP-SGD](https://arxiv.org/abs/1607.00133) is example-level;
[DP-FedAvg](https://arxiv.org/abs/1710.06963) moved to **user-level**
clipping — with the explicit finding that utility survives *only with large
user counts*. [DP-FTRL](https://arxiv.org/abs/2103.00039) removed the
sampling requirement a real server can't enforce, unlocking production:
Google now runs
[30+ Gboard models with formal DP, ε 0.994–13.69 at δ=10⁻¹⁰, at 6,500–12,000 clients/round from populations of 0.8M–16.6M devices](https://research.google/blog/advances-in-private-training-for-production-on-device-language-models/),
SecAgg additionally on two models, distributed DP in production for Android
Smart Text Selection. Google's own
[DDP post](https://research.google/blog/distributed-differential-privacy-for-federated-learning/)
concedes the residual: malicious servers and fake clients bypass the
guarantees; their stated fix direction is
[TEE-based confidential aggregation](https://arxiv.org/abs/2404.10764).

**Honest bottom line: bounded, not solved.** FL alone is data
*minimization* — updates are approximately as sensitive as data. FL+SecAgg
protects individual updates from an honest-but-curious server inside a
big-enough cohort. User-level DP is the only piece that bounds what the
*trained model itself* memorizes
([Carlini, USENIX Sec 2021](https://arxiv.org/abs/2012.07805) — verbatim
PII extraction from trained LMs). The full stack covers honest-but-curious
server + other clients + memorization-up-to-ε. It does **not** cover an
actively malicious server (absent TEE attestation), a compromised client
device, or poisoning. "Share the lesson, not the data" is a quantified-risk
engineering guarantee with published ε between 1 and 14 — not an
impossibility proof.

---

## Part 5 — The aggregator

**What it is.** Per [Bonawitz 2019](https://arxiv.org/abs/1902.01046): the
server stores model checkpoints, round plans, and aggregate metrics; under
SecAgg it sees only masked per-client blobs and the cohort **sum**
(per-update state is ephemeral, in-memory, never persisted). It does: client
selection/sampling, plan+checkpoint distribution, straggler dropping,
weighted averaging, DP noise addition (central DP), checkpoint versioning,
federated evaluation, staged fleet rollout as a separate step.

**The uncomfortable scale numbers.** SecAgg is cryptographically *runnable*
at a few hundred clients (Google's per-cohort group size). But the DP
arithmetic does not survive a fleet of hundreds: Google needed **6,500
contributions/round for ε≈5–14 and 12,000+/round for ε≤1**, each device
participating once per ~313–647 rounds. A 300-box fleet contributes
~300/round with every box in essentially every round — noise-to-signal
~20–40x worse, per-user privacy loss composing hundreds of times faster.
**No published precedent exists for useful user-level DP training at
populations of hundreds** (labeled extrapolation from cited numbers — the
literature does not study this regime). Cadence in practice: 25–30
rounds/day at Gboard, gated on phone eligibility; a wired always-on fleet
could go much faster — no published numbers for that setting.

**For an operator-network deployment:** the fleet is operationally
*cross-silo* (stable, addressable, always-on — per
[Kairouz et al.'s taxonomy](https://arxiv.org/abs/1912.04977)) with a
*cross-device* trust model (consumer homes, physically accessible boxes).
Tooling: [Flower](https://flower.ai) (Brave, Samsung, Mozilla pilots —
vendor-published evidence) or
[NVIDIA FLARE](https://arxiv.org/abs/2210.13291) (the most
production-hardened cross-silo option: NHS FLIP across 5+ trusts, Rhino
Health, EXAM lineage; supports HE and confidential computing).
Infrastructure is modest — a coordinator plus aggregation workers handling
KB–MB updates. TEE-hosted aggregation aligns with the confidential-computing
posture already ratified in HIP_ArchitectureForDiligence Section 6. No
published dollar-cost figures exist for either regime.

---

## Part 6 — The honest gaps (field-level)

1. **The small-corpus regime is unstudied.** No trained-retriever work below
   millions of passages; no per-tenant-tiny lifecycle practice; no published
   per-tenant-data threshold for personalization payoff.
2. **"Did retrieval help the answer" has no settled metric** — offline
   ranking metrics correlate weakly with answers; LLM-judge evals have
   documented reliability problems.
3. **Formal DP at hundreds-of-clients scale is unsolved in the published
   record.** Every production DP-FL result rides on populations of millions.
4. **SecAgg's guarantee is conditional on an honest-but-curious server**;
   the malicious-server attacks are practical, and the TEE fix rests mostly
   on Google's own paper so far.
5. **CPE-class ARM inference numbers for transformers are anecdote** — no
   rigorous published benchmark; measure locally.
6. Counterfactual/unbiased LTR — the field's flagship machinery for implicit
   feedback — failed its biggest reality check
   ([Baidu-ULTR](https://arxiv.org/abs/2404.02543)) even at billion-session
   scale.

---

## Part 7 — What HIP should build

Engineering recommendations, grounded in code and REQs read this session:
the four-scope partition (`harness/write_rule.py`), INJ-1..7 downstream of
retrieval (`harness/injection_contract.py`), the TD-030 embedding invariant
(value never embedded, `harness/extraction_queue.py:23-24,32-38`),
`REQ_LEARNER_SIGNAL_ISOLATION`'s acceptance shape, and DISPATCH 38a's
ratification (rule-based indefinitely; learned ranker = gated moat track).

### 7.1 What fits: a GBDT/logistic metadata scorer over contract-admitted candidates. Not a full learned ranker, not (initially) a cross-encoder.

Build the Curator as a **feature-based scorer that reorders and prunes
`injection.allowed`** — strictly *after* INJ-1..7, so it can only narrow,
never source. That placement mechanically satisfies
HIP_ContextArch_Reconciliation row 6(iii) ("ranker placed so it can only
NARROW the authorized candidate set") by dataflow.

Why the others lose:
- **Full learned/dense retriever loses three ways.** (a) The regime is
  unstudied — every trained-retriever paper operates at 13M+ passages; (b)
  no training data yet, and per-household volumes stay in the
  tens-to-hundreds of events where neural rankers have no published win;
  (c) TD-030 means the stored embedding covers `"{owner} {attribute}"` only
  — dense retrieval over *values* would require embedding plaintext values,
  which the architecture correctly forbids next to their own ciphertext.
  The architecture has already voted.
- **Cross-encoder reranker loses *initially*, wins *maybe later*.** Needs
  decrypted value text per candidate pair, adds ~100ms-class CPU latency for
  quality gains demonstrated only on web-scale corpora, and there are no
  labels to tune it with yet. It is the natural Generation-3 upgrade IF the
  metadata scorer's measured ceiling proves too low — per-turn decrypted
  values are legitimately available (7.2). Revisit only on measured failure,
  per the DISPATCH 38a gate.
- **GBDT/logistic wins**: the only text-free family (µs latency, KB-scale
  artifacts, trains on hundreds of examples); matches the documented
  industry arc (rules → GBDT → maybe more,
  [Airbnb](https://arxiv.org/pdf/1810.09591)); the artifact is inspectable
  and diffable — which matters for a system whose pitch is auditable
  governance; and candidate sets are ≤ dozens, where a well-featured GBDT
  plausibly captures most available headroom.

Features, all from what the graph already carries in cleartext or the
per-turn record: attribute (+ attribute-family match to the SIO attribute),
trust rung, confidence, recency (`valid_from` age), supersession state,
subject==requester, key class/scope, sensitivity, guard/intent context,
historical acceptance rate of this fact when previously injected. Position-
bias correction largely drops out: "presentation" is facts-in-a-prompt, and
the labels are corrections/overrides — deliberate judgments, the clean
pairwise signal (Part 2), not scan-order clicks.

### 7.2 The encryption constraint: rank on metadata — less crippling than it sounds, with the honest part stated

- **Inference time:** the turn already decrypts admitted facts for the
  requesting identity, so a value-aware ranker COULD legally see plaintext
  per turn. Not a constraint.
- **Training time is the real constraint:** training on values requires
  *persisting* value-derived training examples — exactly the
  reconciliation's row 31 collision (training record persisting decrypted
  content outside member sealing, vs operator-blind-at-rest and
  HEL-ACTOR-1). A **metadata-only feature space sidesteps this entirely**:
  attribute, owner, subject, scope, timestamps, trust props are already
  cleartext node properties — the training record adds no new exposure
  class. Major simplification of the row-31 decision, not a full escape:
  the *labels* (which fact was corrected/overridden on which query) are
  behavioral data about the household and must live under the household's
  sealing like everything else.
- **Does metadata-only cripple quality?** At this scale, likely not much:
  with ≤ low-hundreds of facts partitioned across a 17-value attribute enum,
  the median candidate set after the injection contract is small and mostly
  disambiguated by attribute-family, recency, trust, and supersession. Value
  text differentiates candidates mainly when multiple active facts share an
  attribute-family for one subject (multi-valued attributes: allergy,
  schedule, relationship). That is a measurable slice: instrument how often
  ranking-within-family has >3 candidates before concluding value-aware
  scoring is needed. No literature answers this (Part 6, gap 1) — HIP's own
  logs can, cheaply; that measurement is Stage 0 work.

### 7.3 The learner gate: what "provably isolated" actually means at this scale

- **Federated + DP across households does NOT give "provably isolated" at
  fleet size hundreds.** Part 5's arithmetic: production-grade user-level DP
  needs thousands of contributions per round from huge populations. At HIP
  scale ε balloons or utility collapses, and an ε=8 guarantee is a
  quantified bound, not the categorical "one household's learning can never
  surface in another's answers" the REQ states. Do not claim it.
- **What satisfies the REQ as written: per-household-only training. No
  pooling, period.** A Curator trained exclusively on household H's own
  admitted facts and outcomes, sealed under H's keys, structurally cannot
  leak across households — isolation provable by *provenance*, not by
  noise. This is exactly what `REQ_LEARNER_SIGNAL_ISOLATION`'s acceptance
  test is shaped to check (training-example provenance), and it is
  checkable deterministically, no DP mathematics required.
- **Minimum viable gate** = the REQ's own standing check, built now, before
  any learner: ABSOLUTE-tier layer-7 check, two-household fixture,
  fault-injection twin that pools two households' facts into one training
  batch and goes red naming the crossing, gate decisions (INJ outcomes,
  deny reasons) structurally excluded from the feature space, reward
  computed only on post-gate outcomes. Every needed pattern already exists
  in the harness (G0/PSA1 wiring, RI1 fixture). The check must also cover
  **intra-household scope crossing** (member-private signal → shared-scope
  ranker) — REQ open question 4, Bill's call (7.6).
- **If cross-household learning is ever wanted** (fleet-level priors for
  cold start): the defensible combination at this scale is **secure
  aggregation (runnable at hundreds) + TEE-hosted aggregator (consistent
  with the ratified confidential-computing posture,
  [Eichner et al.](https://arxiv.org/abs/2404.10764)) + honest large-ε DP
  as a bound, not a boast** — sold as "bounded influence," never as
  isolation. Structurally separate artifacts: a *global prior* trained under
  that regime, plus per-household deltas under the provenance gate — never
  one commingled model.

### 7.4 Hardware reality: everything actually needed fits CPE

- **GBDT/logistic:** inference in microseconds, training on hundreds of
  examples in milliseconds-to-seconds — trains AND serves on any CPE box. No
  GPU, no edge dependency. The strongest practical argument for 7.1.
- **MiniLM-class cross-encoder (the maybe-later upgrade):** 22.7M params,
  ~91MB fp32 / ~23MB int8 — fits 2–8GB ARM easily; Cortex-A latency is
  unbenchmarked in the literature (Part 6, gap 5) but plausibly
  tens-to-low-hundreds of ms per pair; at ≤20 candidates a ~1–3s worst case
  single-threaded — marginal for voice. Measure on actual CPE before
  committing; ONNX int8 gives ~2–3x on CPU
  ([philschmid](https://www.philschmid.de/optimize-sentence-transformers),
  [sbert.net](https://sbert.net/docs/cross_encoder/usage/efficiency.html)).
- **Training location:** for GBDT the question dissolves — CPE trains it
  trivially. Precedent that even neural training on consumer edge works at
  small scale: Gboard trained its 1.4M-param LSTM on phones. CPE-only is not
  a compromise; it is the natural position, and it keeps training-signal
  custody inside the home — worth more to the positioning than any quality
  delta at this scale.

### 7.5 Sequencing, with the gates in the right places

**Stage 0 — instrument, measure, don't learn (now; no gate required).**
Extend the epistemic record with outcome fields: per-turn
correction/override/accepted-answer events, keyed to `injected_fact_ids`
and `prompt_fact_ids` already logged. Log the rule-based ranking order each
turn (deterministic logging is fine — no IPS planned, per Part 2). Add the
retrieval-failure metric: rate of D-24/T02-class events (authorized, true,
resolved fact not surfaced) and the candidates-per-attribute-family
measurement from 7.2. **This stage produces the number the DISPATCH 38a
entry gate needs** — "a measured retrieval failure justifies the cost" is
currently unmeasurable.

**Stage 1 — build the standing gate before any learner exists (the REQ's
own design).** `REQ_LEARNER_SIGNAL_ISOLATION`'s check, wired ABSOLUTE-tier
into layer-7 with the two-household fixture and fault-injection twin. Also
the row-31 decision in its minimum form: training examples = metadata
features + outcome labels, sealed per-household, opaque-ID'd per
HEL-ACTOR-1.

**Gate A (Bill): the entry decision.** Stage 0's measurement either
justifies opening the moat track or it doesn't. If retrieval failure is
rare and mostly attributable to attribute-family gaps, the cheaper fix is
more rules — and the honest recommendation is to take it.

**Stage 2 — shadow Curator (learner exists, cannot act).** Per-household
GBDT over the 7.1 feature set, trained on Stage-0 logs, running in shadow:
score every turn, log its ranking next to the rule ranking, **never touch
the prompt**. Offline eval = agreement with subsequent outcomes. Cold
start: below ~100 outcome events (the Joachims-derived threshold from
Part 2), the scorer IS the rules — hand-set weights reproducing today's
deterministic order, so "no data yet" degrades to exactly current behavior.

**Stage 3 — live, narrowing-only, kill-switched.** The scorer
reorders/prunes within `injection.allowed`, downstream of INJ-1..7,
upstream of prompt assembly, under G0 and PSA1 (both MET) — plus one new
PSA1-style invariant: *curated set ⊆ admitted set*, fault-injected like
everything else. Rollback is a flag back to rule order. Lifecycle at this
scale: no interleaving (needs thousands of queries — Part 3); instead
shadow-vs-live outcome comparison per fleet cohort, with the Kohavi lesson
applied — gate on correction *rate*, an outcome metric, not engagement.

**Gate B (Bill): the pooling decision.** Only if per-household ceilings
prove too low. Then, and only at meaningful fleet scale: global-prior
training under SecAgg + TEE aggregation + honest-ε DP (7.3), prior +
per-household delta kept structurally separate.

**Stage 4 — federated, if ever.** Flower or FLARE on the operator network,
TEE-hosted aggregator. Not before hundreds of participating households; the
Part 5 arithmetic says the DP story is weak below that regardless of
engineering effort.

### 7.6 The calls that are Bill's

1. **The entry trigger, quantified.** DISPATCH 38a ratified "entered when a
   measured retrieval failure justifies the cost" — the threshold (what
   failure rate, which metric, what window) is a product-risk call the
   literature cannot make, and Part 3 shows the field has no settled metric
   to hand over. Stage 0 gives the instrument; Bill sets the trip point.
2. **The scope-crossing definition — REQ_LEARNER_SIGNAL_ISOLATION open
   question 4.** Does one household's member-private signal pooling into
   that SAME household's shared-scope Curator constitute the same violation
   class as cross-household pooling? The REQ currently treats both the same,
   per Bill's "or scopes" wording. Confirming or narrowing that reading
   changes the fixture, the check, and the Curator's per-household
   architecture (one model per household vs one per scope-audience).
   Nothing in any paper touches this — it is HIP's partition semantics.
3. **The pooling stance, as product identity.** Per-household-only forever
   is a *stronger sellable claim* ("your household's learning provably
   never leaves") and a permanently weaker cold start; cross-household
   priors buy quality at the cost of demoting "isolated" to "bounded,
   ε=N." If pooling ever happens, the ε accepted is a risk-tolerance number
   with no technical answer — Google ships 1–14, and at HIP fleet size the
   choice is above that range or below their utility. Same shape as the
   care-team-default trade in REQ_PARTITION_CUSTODY: a deliberate, stated
   cost, decided by Bill and written down before it is built.

---

**Where the field left us honest:** nothing above solves gap 1 (the regime
is unstudied — HIP's own logs are the only evidence that will ever answer
the metadata-quality question), and the "did retrieval help" metric the
entry gate depends on is the least-settled measurement in the stack. The
plan compensates the only way available: instrument first, learn
per-household under a provenance gate checkable without trusting any of the
unsettled mathematics, and defer every pooled-learning claim until the
fleet is big enough that the published numbers actually apply.

---

## Provenance

Produced 2026-07-28 by three parallel research passes (ranking model
families + serving lifecycle; implicit-feedback training + personalization;
federated learning + attacks/defenses + aggregation), each fetching primary
sources directly — full per-source URL lists retained in the session
transcript. HIP-side grounding from the 2026-07-27/28 read-only session
against roadmap 7b7a8b1. Known verification caveats carried forward: EXAM
Nature Medicine and MELLODDY figures snippet-verified only; Apple FL
operational numbers unpublished; TEE-aggregation production status rests on
Google's own paper; Flower/FLARE production evidence is vendor-published;
the small-fleet DP analysis (Part 5) is labeled extrapolation, not a
literature result.
