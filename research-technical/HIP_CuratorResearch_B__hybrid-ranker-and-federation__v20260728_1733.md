# HIP_CuratorResearch_B: Hybrid Ranker and Federation (external companion memo)
Status: BUILT
Reconciled-Against: landed verbatim 2026-07-28, NOT reconciled against code or the companion memo -- reconciliation pending Bill's rulings
Provenance: source ChatGPT; received 2026-07-28; landed from ~/Downloads/"ChatGPT-Curator Research 7-28-26.rtf" (200,178 bytes, RTF), converted via textutil -convert html + link-preserving HTML-to-markdown script; all 49 reference hyperlinks preserved; content verbatim, no edits, no reconciliation
Companion-To: HIP_CuratorResearch__learned-retrieval-training-federation__v20260728_1045.md
Known-Disagreements: two, per D-06 dispatch -- (1) semantic feature (this doc recommends an optional frozen semantic encoder as a ranking feature; the companion memo recommends metadata-only features, citing the TD-030 value-embedding invariant), (2) cold-start architecture -- reconciliation pending Bill's rulings, neither doc edited

---

# Curator research: technical and operational design

## Executive conclusion

The Curator should not begin as an end-to-end neural retriever. For HIP’s initial scale—tens to low hundreds of structured facts per household—the right architecture is:

1. **Non-learned authorization and policy gate**

1. **Deterministic graph-based candidate generation**

1. **Lightweight learned reranker**

1. **Optional frozen semantic encoder used as one ranking feature**

1. **Deterministic post-ranking constraints**

1. **Local, encrypted outcome logging and personalization**

The first learned ranker should be a small LambdaMART/gradient-boosted-tree model over metadata, graph features and a semantic-similarity score. It will be materially easier to train, audit, operate and roll back than an end-to-end transformer retriever.

A full neural model per household is not the normal production pattern. The established pattern is a shared base representation plus user or household features, embeddings, calibration parameters, or a very small local head. FedRep and related personalized-federated-learning work explicitly separate a shared representation from a locally trained head. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v139/collins21a))

The most important privacy conclusion is less convenient:

**Federated learning cannot satisfy a literal requirement that one household’s learning never influence another household’s answer.**

That is what federated learning is designed to do: combine household lessons into a shared model. Secure aggregation hides individual updates; differential privacy bounds the influence and inferability of one household. Neither produces zero cross-household influence.

Therefore HIP needs two separately named guarantees:

- **Strict isolation:** household-derived learning remains local. The global model uses only public, synthetic or centrally authored data.

- **Bounded federated privacy:** household learning may affect the aggregate model, but only through clipped, securely aggregated, user-level differentially private updates with a measured privacy budget.

Until HIP explicitly approves the second definition, the learner gate should prohibit federated production updates.

# Part 1 — What the Curator is

## The established problem formulation

The Curator is best described as a **query-conditioned learning-to-rank system over an authorized personal knowledge store**.

For query (q), authorized household facts (F_q), and prompt budget (k), it estimates:

[  s(q,f,\text{household state}) \rightarrow \text{expected usefulness of fact } f  ]

and selects a constrained set:

[  S_k = \operatorname{TopK}_{f \in F_q} s(q,f)  ]

subject to hard rules for authorization, ownership, validity, contradiction handling and prompt budget.

It overlaps four established fields:

- **Information retrieval:** find candidate facts related to the query.

- **Learning to rank:** order candidates by expected usefulness.

- **RAG retriever training:** optimize retrieval using downstream generation outcomes.

- **Personalized recommendation/search:** incorporate household-specific history and preferences.

It is **not primarily a vector-database problem**. At 20–300 facts, scanning every authorized candidate is inexpensive. The difficult problem is deciding which facts are useful, safe, timely and non-distracting.

## Real model families

**FamilyHow it worksRepresentative workTypical footprint and latencyHIP relevanceLexical sparse retrieval**

Matches query and fact terms using BM25-like weights

Traditional BM25; learned sparse methods such as SPLADE

No neural model for BM25; sub-millisecond scanning is realistic at hundreds of facts

Useful baseline and feature

**Learned sparse retrieval**

Transformer predicts expanded lexical terms and weights; uses an inverted index

SPLADE and SPLADE v2 ([arXiv](https://arxiv.org/abs/2107.05720))

Usually BERT-class encoder; substantially more machinery than HIP’s corpus requires

Overkill initially

**Dense bi-encoder**

Encodes query and fact separately; ranks by vector similarity

DPR; sentence-transformer models ([ACL Anthology](https://aclanthology.org/2020.emnlp-main.550/))

Small MiniLM example: 22.7M parameters, about 91 MB in FP32, 384-dimensional embeddings ([Hugging Face](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2))

Good as a frozen semantic feature

**Late interaction**

Produces multiple token vectors per query and document and scores token-level matches

ColBERTv2 ([arXiv](https://arxiv.org/abs/2112.01488))

Roughly BERT-class model plus token-vector storage; production implementations report tens-of-milliseconds retrieval over very large collections ([GitHub](https://github.com/stanford-futuredata/ColBERT))

Strong retrieval technology, unnecessary at household scale

**Cross-encoder reranker**

Concatenates query and fact and runs full transformer attention for every pair

MiniLM cross-encoders; standard retrieve-then-rerank pipelines ([SentenceTransformers](https://www.sbert.net/docs/cross_encoder/usage/usage.html))

A 22.7M-parameter MiniLM-L6 reranker is about 91 MB; its published model card reports about 1,800 pairs/second on a V100 GPU, not on CPE hardware ([Hugging Face](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2))

Useful as a later teacher or top-10 reranker

**Feature-based learned-to-rank**

Scores hand-designed and learned features using trees, linear models or small neural networks

LambdaMART; XGBoost rank:ndcg ([Microsoft](https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/))

Usually kilobytes to a few megabytes; scoring hundreds of rows is normally negligible on a CPU

Best initial Curator

**Trainable RAG retriever**

Trains the retriever jointly or indirectly from the generator’s likelihood or answer quality

RAG, REALM, REPLUG and Atlas ([arXiv](https://arxiv.org/abs/2005.11401))

Normally one or more 100M-class retrievers plus a generator; training is GPU-oriented

Future research, not first product

|  |  |  |  |  |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

### Why dense retrieval is not enough

A dense encoder can learn that:

“What medicine is Dad currently taking?”

is semantically close to:

“Metformin 500 mg twice daily.”

But semantic similarity alone does not know:

- whether the fact belongs to Dad or another member;

- whether the requester can access it;

- whether it has been superseded;

- whether it was asserted or medically confirmed;

- whether it conflicts with another fact;

- whether including it creates unwanted disclosure;

- whether the same fact has already been represented more authoritatively.

Those are first-class HIP features. That favors a learned-to-rank layer above semantic retrieval.

# Part 2 — Training the Curator

## 2.1 Training examples

A training example should record the state of the ranking decision, not merely the final answer:

    household-local example

    ├── query representation

    ├── authorized candidate fact IDs

    ├── candidate feature vectors

    ├── ranker scores and positions

    ├── selected facts

    ├── policy version

    ├── ranker version

    ├── generator and prompt version

    ├── user outcome

    └── propensity/exploration information

The labels can be pointwise, pairwise or listwise:

- **Pointwise:** Was this fact useful?

- **Pairwise:** Was fact A more useful than fact B?

- **Listwise:** How good was the whole selected fact set?

LambdaMART and neural rankers are usually trained pairwise or listwise because ordering matters more than predicting a perfectly calibrated absolute relevance number.

## 2.2 HIP’s available signals

### Strong positive signals

- The user explicitly asks HIP to use a fact.

- The user adds a previously omitted fact and the corrected answer succeeds.

- A correction identifies exactly which stored fact should have been retrieved.

- The user confirms that a fact was relevant to the answer.

- A caregiver or recipient explicitly approves a retrieved context set.

### Strong negative signals

- “Do not use that.”

- A fact is identified as stale, superseded or about the wrong person.

- The user removes a fact from the context.

- Retrieval violates an explicit audience or purpose directive.

- The user says the answer overemphasized irrelevant history.

### Weak and confounded signals

- No correction.

- Continued conversation.

- Acceptance of an answer.

- A positive rating on the final response.

- A successful tool action.

These may indicate that retrieval was good, but they may also reflect generator quality, user patience, low stakes or failure to notice an omission.

HIP therefore cannot treat “answer accepted” as a clean relevance label.

## 2.3 Implicit feedback and bias

Search and recommendation systems have long used clicks and interactions as ranking labels. The central difficulty is that users interact with what the old ranker chose to present. Highly ranked results receive more exposure and therefore more interactions even when they are not intrinsically better.

Joachims and colleagues developed counterfactual learning-to-rank methods using **inverse propensity scoring**, weighting observations according to their probability of being displayed. This can produce unbiased ranking estimates under the specified exposure model. ([Microsoft](https://www.microsoft.com/en-us/research/publication/unbiased-learning-rank-biased-feedback/))

The major hazards are:

- **Position bias:** items placed earlier are more likely to affect the outcome.

- **Selection bias:** unselected facts receive no observable outcome.

- **Presentation bias:** how the fact is worded or placed changes its effect.

- **Trust bias:** users may accept highly positioned information because the system appears to trust it.

- **Policy confounding:** a fact may be absent because it was unauthorized rather than irrelevant.

- **Generator confounding:** retrieval may be correct but the model may use the fact badly.

IPS also has high variance when an action was rarely selected. Doubly robust estimators combine an outcome model with propensity weighting and can reduce variance, but still depend on modeling assumptions. ([DOI.org](https://doi.org/10.1145/3569453)) Research has also shown that ordinary position-based IPS can remain biased under more complicated trust and presentation effects. ([UvA DARE](https://dare.uva.nl/id/314dc0b9-096a-4e7d-a42c-95b97eba3a6b))

### A HIP-specific complication

The household does not normally see a ranked list of facts. The facts are inserted into a prompt and consumed by an LLM.

That means classic click-position models do not transfer cleanly. HIP has two distinct exposure effects:

1. **Fact selection:** whether the Curator retrieved the fact.

1. **Prompt position and presentation:** whether the generator noticed or properly used it.

The field has not settled a generally accepted counterfactual estimator for downstream RAG outcomes under this combined exposure and generation process.

## 2.4 Required exploration

To learn causally rather than merely imitate the existing rule system, HIP eventually needs controlled variation.

Safe mechanisms include:

- Randomly swapping the order of two similarly scored, authorized facts.

- Occasionally including or excluding a low-risk marginal candidate.

- Interleaving outputs from the rule ranker and learned ranker.

- Offline replay using a frozen generator.

- Leave-one-fact-out answer generation for evaluation.

Interleaving has been used extensively to compare search rankers with less traffic than conventional A/B tests. ([CaltechAUTHORS](https://authors.library.caltech.edu/records/r3zrn-kd453)) Airbnb has described using interleaving and counterfactual evaluation to screen ranking changes before full A/B tests, while retaining A/B testing as the final online standard. ([Airbnb Tech](https://airbnb.tech/infrastructure/academic-publications-airbnb-tech-2025-year-in-review/))

For HIP, exploration must never cross policy, key-class, consent or safety boundaries. Only the ranking of already-authorized facts may be varied.

## 2.5 Generator-derived supervision

RAG research provides another route: train a retriever according to how much a document improves the generator’s likelihood or answer quality.

- **RAG** jointly fine-tunes a dense retriever with a generator. ([arXiv](https://arxiv.org/abs/2005.11401))

- **REALM** trains retrieval through a language-model objective. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v119/guu20a.html))

- **REPLUG** keeps the language model frozen and trains the retriever from the model’s document-conditioned scores. ([ACL Anthology](https://aclanthology.org/2024.naacl-long.463/))

HIP could locally generate labels such as:

[  \Delta U(f) =  U(\text{answer with } f) -  U(\text{answer without } f)  ]

But this is expensive and inherits the judge model’s errors. It should be used for offline teacher labels and regression testing, not assumed to be ground truth.

## 2.6 Cold start

A new household has too little interaction history for a household-specific model.

The established answer is:

1. Start with a **shared base ranker**.

1. Use rules and explicit metadata as fallback.

1. Personalize with a small amount of local state.

1. Revert to the base when confidence is low.

Research systems such as **FedRep** share a learned representation while keeping a local personalized head. **Per-FedAvg** learns an initialization designed to adapt in a few local steps. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v139/collins21a)) Another line of work combines a global representation with local nearest-neighbor memorization rather than training an entire local network. ([arXiv](https://arxiv.org/abs/2111.09360))

For HIP, cold-start ranking should initially rely on:

- explicit policy;

- query–fact semantic similarity;

- graph distance;

- subject/attribute match;

- trust level;

- temporal validity;

- corroboration;

- contradiction state;

- source reliability;

- fact usage history;

- authored domain rules.

## 2.7 Shared model versus model per household

### Full separate model per household

This is generally a poor architecture for HIP:

- Sparse labels cause severe overfitting.

- Models become hard to evaluate consistently.

- Thousands or millions of artifacts must be versioned.

- Models may remain stale for months.

- Loading transformer weights per request wastes memory and latency.

- Cross-household improvements cannot be reused.

- Operational rollback becomes household-specific.

A tiny household-specific tree, calibration vector or linear head is operationally possible. A separate transformer ranker per household is not the normal scalable production design.

### Shared model with personalization

The established large-scale pattern is:

- shared feature extraction;

- shared ranking backbone;

- user or household features;

- user embeddings or local state;

- possibly a small local head.

LinkedIn’s feed stack, for example, uses multiple shared ranking stages rather than loading a complete model per member. ([LinkedIn Engineering](https://engineering.linkedin.com/teams/data/artificial-intelligence/feed)) Netflix has similarly described shared recommendation models with learned user and entity representations. ([Netflix TechBlog](https://netflixtechblog.com/foundation-model-for-personalized-recommendation-1a0bd8e02d39))

### HIP recommendation

Use:

- one shared, versioned base scorer;

- a household-local calibration or small final layer;

- encrypted household feature state;

- rules whenever local confidence or data volume is insufficient.

# Part 3 — Production and lifecycle

## 3.1 Where the Curator runs

The production request path should be:

    Query and authenticated speaker

    │

    ▼

    Hard identity, consent and policy gate

    │

    ▼

    Authorized graph traversal / candidate generation

    │

    ▼

    Feature construction

    ├── metadata and graph features

    └── optional semantic similarity

    │

    ▼

    Learned reranker

    │

    ▼

    Deterministic post-ranking constraints

    │

    ▼

    Decrypt selected facts / compose prompt

    │

    ▼

    Generator

The Curator must run **after authorization** and **before prompt assembly**.

It must not be permitted to override authorization. A learned score can determine whether an authorized fact is useful; it cannot make an unauthorized fact eligible.

## 3.2 Latency reality

At HIP’s corpus size, approximate practical targets are:

**ComponentReasonable HIP targetHardware**

Graph candidate generation

Under 1–5 ms

Ordinary CPU

Metadata feature construction

Under 1 ms for hundreds of facts

Ordinary CPU

LambdaMART/tree scoring

Well under 1 ms for hundreds of candidates

Ordinary CPU

Frozen MiniLM query embedding

Roughly single-digit to tens of milliseconds on optimized modern CPUs; hardware-dependent

Capable CPE CPU/NPU

MiniLM cross-encoder over 5–10 facts

Potentially tens of milliseconds on CPU; must be measured

High-end CPE or edge

Cross-encoder over 100 facts

Usually inappropriate for CPE latency

Edge GPU/CPU pool

|  |  |  |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

The published MiniLM model sizes make them small enough to fit on CPE hardware, but the public model cards do not establish performance on HIP’s actual ARM/x86 gateway targets. The 22.7M-parameter MiniLM bi-encoder and reranker are about 91 MB in FP32 and become substantially smaller with quantization. ([Hugging Face](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2))

The correct conclusion is:

- **Tree/linear Curator inference:** clearly CPE-capable.

- **Frozen MiniLM embedding inference:** probably CPE-capable on current higher-end hardware, subject to benchmarking.

- **Small local-ranker training:** CPE-capable.

- **Transformer fine-tuning:** technically possible, but not operationally justified for HIP’s sparse labels.

- **Large cross-encoder or end-to-end retriever training:** edge or data-center workload.

## 3.3 Production lifecycle

A ranker release must bind together:

- model version;

- feature-schema version;

- graph-schema version;

- policy version;

- semantic-encoder version;

- prompt-composer version;

- generator version;

- training-data window;

- privacy-accounting state.

### Recommended release sequence

1. **Unit and invariant tests**

  - Unauthorized facts can never become candidates.

  - Revoked facts disappear.

  - Superseded facts lose eligibility.

  - Key-class boundaries hold.

  - Missing features fail closed.

1. **Offline replay**

  - Run historical turns using the old and new rankers.

  - Compare selected fact sets.

  - Generate answers with a frozen generator.

  - Review high-disagreement and high-risk cases.

1. **Shadow deployment**

  - New Curator ranks live requests.

  - Existing rules still determine production prompts.

  - Record differences and projected outcomes.

1. **Canary**

  - Limited households or operator sites.

  - Automatic fallback on latency, error or outcome regression.

1. **Staged rollout**

  - Expand only after predefined gates.

  - Retain rule-system fallback.

1. **Rollback**

  - One control-plane operation restores the previous signed model or rule-only ranking.

Airbnb has described shadow execution, reversible deployment, automatic fallback and staged ranking rollouts. LinkedIn similarly uses canary evaluation and automated comparison before broad production release. ([Airbnb Tech](https://airbnb.tech/infrastructure/building-a-next-generation-key-value-store-at-airbnb/))

## 3.4 What breaks when retrieval regresses

A bad Curator can:

- omit a decisive fact;

- retrieve a stale fact;

- favor highly used facts over currently relevant facts;

- retrieve redundant facts and crowd out a necessary one;

- place conflicting facts in the same prompt without status;

- overweight recency;

- overweight trust and miss a relevant unconfirmed concern;

- retrieve a semantically related fact about the wrong household member;

- create longer prompts that degrade the generator;

- cause the generator to anchor on distractors.

Authorization leakage must not be among these failure modes because the policy gate is outside the learned ranker.

### Monitoring signals

Monitor at least:

- correction and override rate;

- “missing fact” reports;

- irrelevant-context reports;

- stale or superseded fact inclusion;

- conflicting-fact inclusion;

- top-(k) churn relative to baseline;

- percentage of turns with no retrieved fact;

- percentage hitting maximum prompt budget;

- latency by CPE type;

- fallback rate;

- score and feature drift;

- outcome differences by household type and fact category;

- model-version-specific incident rates.

## 3.5 Evaluation

### Offline ranking metrics

- **Recall@k:** Did the Curator include every required fact?

- **Precision@k:** How much selected context was useful?

- **nDCG@k:** Were highly relevant facts placed earlier?

- **MRR:** How early was the first decisive fact?

- **MAP:** Useful when multiple facts are relevant.

- **Coverage:** Can the system retrieve across fact categories and members?

- **Diversity/redundancy:** Did several selected facts repeat the same information?

- **Policy violations:** Must remain exactly zero.

- **Temporal correctness:** Was the valid fact selected rather than the newest recorded fact?

- **Contradiction handling:** Were conflicting facts represented correctly?

### Online ranking evaluation

- Household-level A/B testing.

- Interleaving of rule and learned rankers.

- Explicit context correction rate.

- Re-ask or reformulation rate.

- Successful task completion.

- Human review of sampled high-risk turns.

Randomization should occur at household level for persistent experiments, not independently on every query, to prevent the experience and learned state from mixing across experiment arms.

### The honest problem: retrieval quality is not answer quality

A fact set can receive excellent nDCG and still hurt the final answer. LLMs do not consume ranked passages like humans scan search results. Distracting or conflicting context can degrade generation even when the relevant passage is present.

Recent work has shown that traditional metrics such as nDCG, MAP and MRR can correlate poorly with downstream RAG utility because they do not model distraction or how generators consume context. ([ACL Anthology](https://aclanthology.org/2026.eacl-long.391/))

Frameworks such as **KILT**, **RAGAS** and **RAGChecker** evaluate combinations of provenance, context relevance, groundedness and answer quality, but no automatic metric is universally reliable across generators and tasks. ([ACL Anthology](https://aclanthology.org/2021.naacl-main.200/))

HIP therefore needs two test sets:

1. **Fact-selection gold set:** Which facts belong in the prompt?

1. **End-to-end answer set:** Did their inclusion actually improve the response?

The strongest test is causal:

Compare the same frozen generator with and without the candidate fact, holding everything else constant.

Even that is generator-specific and must be periodically repeated when the generator changes.

# Part 4 — Passing lessons up through federated learning

## 4.1 What federated learning actually does

The canonical algorithm is **Federated Averaging**, or FedAvg, introduced by McMahan and colleagues.

A round works as follows:

1. The server selects eligible clients.

1. It sends the current model and training instructions.

1. Each client trains locally on its private examples.

1. The client produces a model delta or gradient update.

1. The server aggregates updates, usually weighted by local example counts.

1. The server creates the next global model.

1. The process repeats.

FedAvg reduces communication by performing multiple local optimization steps before aggregation. The original paper reported large reductions in communication rounds relative to fully synchronized distributed SGD on its experimental tasks. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v54/mcmahan17a.html))

Google’s production federated-learning system uses synchronous rounds involving selected device cohorts, on-device example stores, local computation, aggregation and repeated model distribution. Its architecture separates coordinators, client selectors and aggregation workers and is designed for populations ranging to tens or hundreds of millions of devices. ([arXiv](https://arxiv.org/abs/1902.01046))

## 4.2 Real deployments

The most established deployment is **Gboard mobile keyboard prediction**.

Google has deployed federated learning for next-word prediction and related keyboard models without centrally collecting raw typed text. ([Google Research](https://research.google/pubs/federated-learning-for-mobile-keyboard-prediction/))

More recently, Google reported production use of **DP-FTRL** for more than 20 Gboard language models and said all of its neural next-word prediction language models had been trained with formal differential-privacy guarantees. Two reported deployments also used secure aggregation. ([Google Research](https://research.google/pubs/federated-learning-of-gboard-language-models-with-differential-privacy/))

Google has also reported federated keyboard experiments spanning tens of millions of users. ([Google Research](https://research.google/pubs/federated-learning-of-n-gram-language-models/))

## 4.3 FedAvg successors

FedAvg works poorly when clients have highly different data and local training causes models to drift in different directions.

Relevant successors include:

- **SCAFFOLD:** introduces control variates to correct client drift under non-IID data. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v119/karimireddy20a.html))

- **FedAdam/FedYogi:** apply adaptive server-side optimization to aggregated updates. ([ICLR](https://iclr.cc/virtual/2021/poster/2691))

- **FedRep:** shares a representation while keeping personalized heads local. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v139/collins21a))

- **DP-FTRL:** supports differentially private federated training under more realistic participation patterns than methods that assume precise random sampling. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v139/kairouz21b.html))

For HIP, FedRep-like separation is especially relevant:

- shared generic ranking representation;

- household-local final calibration/head;

- only the shared component is eligible for aggregation.

## 4.4 Update inversion and leakage

Keeping raw data on the client does not mean the update is harmless.

### Demonstrated attacks

**Deep Leakage from Gradients** showed that input images and text could be reconstructed from shared gradients under certain training configurations. ([NeurIPS Papers](https://papers.nips.cc/paper/2019/hash/60a6c4002cc7b29142def8871531281a-Abstract.html))

**Inverting Gradients** demonstrated high-fidelity reconstruction from gradients, including some averaged-batch settings. ([NeurIPS Papers](https://papers.nips.cc/paper/2020/hash/c4ede56bbd98819ae6112b20ac6bf145-Abstract.html))

Attack success depends on factors such as:

- batch size;

- model structure;

- local training steps;

- gradient precision;

- prior knowledge;

- whether the attacker sees individual or aggregated updates;

- whether clipping and noise are applied.

Not every published attack transfers directly to a production FL deployment, but the literature establishes that an unprotected model update cannot be treated as non-private. Comparative evaluations also find significant assumptions and variable effectiveness across attacks and defenses. ([NeurIPS Proceedings](https://proceedings.neurips.cc/paper_files/paper/2021/hash/3b3fff6463464959dcd1b68d0320f781-Abstract.html))

## 4.5 Secure aggregation

Secure aggregation cryptographically masks client updates so that the server can recover the sum but not an individual participant’s update.

The Bonawitz et al. protocol:

- protects individual vectors from the server;

- tolerates client dropout;

- uses pairwise masks and secret sharing;

- reveals an aggregate only after enough clients complete the protocol.

The original work was designed for high-dimensional vectors and large client cohorts and reported practical communication expansion rather than orders-of-magnitude overhead. ([Google Research](https://research.google/pubs/practical-secure-aggregation-for-privacy-preserving-machine-learning/))

Google’s production architecture describes multi-round secure-aggregation protocols and cohorts containing hundreds of clients. ([arXiv](https://arxiv.org/abs/1902.01046)) Google has also described only releasing the aggregate when hundreds or thousands of users participate. ([Google Research](https://research.google/blog/federated-learning-collaborative-machine-learning-without-centralized-training-data/))

Secure aggregation protects against the aggregator directly inspecting one household’s update. It does **not**:

- stop the final global model from memorizing information;

- limit one household’s influence;

- prevent malicious client poisoning;

- protect a compromised client device;

- prevent leakage through repeated aggregates with carefully changing cohorts;

- guarantee that the aggregate itself is safe.

Research has demonstrated that participant changes across repeated secure-aggregation rounds can expose additional information unless the system controls participation and composition carefully. ([arXiv](https://arxiv.org/abs/2106.03328))

## 4.6 Differential privacy

### DP-SGD

Differentially private stochastic gradient descent generally:

1. Clips each example or client update to a maximum norm.

1. Adds calibrated random noise.

1. Tracks the cumulative privacy loss across training and releases.

Abadi et al.’s DP-SGD work established the modern deep-learning approach using clipping, Gaussian noise and privacy accounting. ([Google Research](https://research.google/pubs/deep-learning-with-differential-privacy/))

### User-level versus record-level DP

For HIP, **user-level—or more precisely household-level—DP** is necessary.

Record-level DP bounds the effect of one training event. A household could contribute hundreds of correlated events and still have substantial total influence.

Household-level DP instead asks:

How much can the released model change if all training data from one household is added or removed?

That is the relevant privacy unit.

### DP-FTRL

DP-FTRL applies differential privacy through a follow-the-regularized-leader training process and can handle practical federated participation without requiring exact Poisson sampling assumptions. Google has deployed it for Gboard models. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v139/kairouz21b.html))

### Costs

Differential privacy causes:

- lower signal-to-noise ratios;

- reduced utility for rare patterns;

- slower convergence;

- larger required cohorts;

- a finite privacy budget across releases;

- difficult tradeoffs between privacy, personalization and model quality.

Secure aggregation and distributed noise generation can reduce the amount of trust placed in one central server. Research on distributed discrete Gaussian mechanisms has shown experimentally that secure aggregation and distributed DP can approach central-DP utility under some conditions. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v139/kairouz21a.html))

## 4.7 The guarantee is bounded, not absolute

“Share the lesson, not the data” is useful product language but not a complete security guarantee.

Federated learning can provide:

- raw-data locality;

- secure hiding of individual updates;

- formal bounds on household influence;

- reduced central collection of sensitive events.

It does not inherently provide:

- immunity to gradient leakage;

- zero memorization;

- zero cross-household influence;

- protection from compromised CPE;

- protection from malicious training code;

- protection from poisoning or backdoors;

- freedom from metadata leakage;

- protection against information revealed through model outputs.

Model-poisoning research has shown that a malicious federated client can implant backdoors, and secure aggregation can make anomalous individual updates harder for the server to inspect. ([Proceedings of Machine Learning Research](https://proceedings.mlr.press/v108/bagdasaryan20a.html))

# Part 5 — The aggregator

## 5.1 What it is

The aggregator is not a warehouse of household training data. It is a coordinated set of server-side services:

    Client eligibility and selection

    │

    ▼

    Round coordinator

    │

    signed model + plan

    │

    ▼

    Household CPE clients

    local data → local training

    │

    clipped/masked updates

    │

    ▼

    Secure aggregation workers

    │

    aggregate update only

    │

    ▼

    Server optimizer

    │

    ▼

    Evaluation and privacy gate

    │

    ▼

    Signed global-model registry

## 5.2 What it stores

- Current and previous global model versions.

- Model signatures and hashes.

- Training-plan versions.

- Feature-schema versions.

- Aggregate model updates.

- Aggregate operational metrics.

- Cohort and threshold configuration.

- Privacy-accounting ledger.

- Release approvals and audit records.

- Evaluation results.

- Rollback artifacts.

## 5.3 What it should never see

Under the intended architecture:

- decrypted household facts;

- raw household queries;

- raw user corrections;

- local example records;

- individual unmasked model updates;

- household-local personalization heads;

- unencrypted derived embeddings;

- direct mappings between model updates and named household members.

Network-level services may still know that a device participated. Device identity, account identity and federated-learning pseudonym should therefore be separated.

## 5.4 Round structure

1. **Eligibility**

  - Current software and model schema.

  - Sufficient local examples.

  - Device idle or below resource limits.

  - Valid operator attestation.

  - Participation budget not exhausted.

1. **Client selection**

  - Random or controlled sampling.

  - Avoid selection based on rare sensitive conditions.

  - Enforce one household’s participation cap.

1. **Distribution**

  - Signed model.

  - Feature schema.

  - Training code or declarative plan.

  - Clipping norm.

  - Local step count.

  - Secure-aggregation parameters.

1. **Local training**

  - Read only encrypted local examples after authorization.

  - Train shared component.

  - Retain local head locally.

  - Clip household update.

1. **Protection**

  - Apply secure-aggregation masks.

  - Apply distributed or client-side DP mechanism as designed.

1. **Aggregation**

  - Release only if participation threshold is met.

  - Combine weighted or normalized updates.

  - Apply FedAvg, FedAdam, SCAFFOLD or another approved optimizer.

1. **Evaluation**

  - Offline regression suite.

  - Privacy accountant.

  - Poisoning and anomaly checks on permissible aggregate signals.

  - Canary evaluation.

1. **Release**

  - Sign approved model.

  - Publish to operator model registry.

  - Gradually distribute to CPE clients.

## 5.5 Cohort size

There is no universal client count at which secure aggregation suddenly becomes “private.”

Three numbers matter:

1. **Cryptographic threshold:** enough clients to reconstruct the aggregate after dropout.

1. **Anonymity set:** enough clients that one contribution is difficult to isolate.

1. **DP cohort size:** enough signal that required noise does not destroy utility.

Production literature commonly discusses cohorts in the hundreds, while Google’s broader descriptions refer to aggregates released from hundreds or thousands of participants. ([arXiv](https://arxiv.org/abs/1902.01046))

### HIP engineering requirement

For an initial production federated Curator:

- **Target:** 1,000 or more completed household updates per released aggregate.

- **Operational floor:** 100 completed households, only for testing and availability—not as a claim of strong anonymity.

- **No production release:** when the formal privacy mechanism cannot meet its approved household-level privacy budget.

Early HIP deployments may not have enough active households or labels to meet this. That is a reason to delay federation, not lower the threshold until the story works.

## 5.6 Cadence

Google’s production systems operate through repeated rounds rather than one monolithic training job. The actual cadence varies by application and client availability. ([arXiv](https://arxiv.org/abs/1902.01046))

For HIP:

- Collect eligible local examples continuously.

- Run aggregation rounds daily once population supports it.

- Release Curator models weekly at first.

- Allow emergency rollback immediately.

- Increase release cadence only when automated evaluation is mature.

- Limit each household’s participation per privacy epoch.

Household outcomes are likely too sparse for meaningful hourly global updates.

## 5.7 Cost

Primary production sources do not publish credible stand-alone dollar costs for running their federated-learning infrastructure. A precise number would be fabricated.

For HIP’s small ranker, the major cost will not be matrix multiplication. It will be:

- client orchestration;

- certificate and key infrastructure;

- secure-aggregation protocol traffic;

- model distribution;

- privacy-accounting implementation;

- compatibility testing across CPE versions;

- monitoring and SRE;

- privacy and security review;

- red-team testing;

- retained rollback infrastructure.

Server-side arithmetic for a sub-megabyte or few-megabyte ranker is minor. Network use scales approximately with:

[  \text{clients per round}  \times  (\text{model download}+\text{protected update upload})  ]

Secure-aggregation messages add protocol overhead beyond the model vector itself.

## 5.8 Where it belongs in the operator network

Do **not** deploy a separate aggregator at every local edge site initially. Small site populations reduce cohort diversity and privacy.

Place the first aggregator in the operator’s central or large regional cloud:

- coordinator cluster;

- client-selection service;

- secure-aggregation workers across fault domains;

- server optimizer;

- privacy accountant;

- model registry and signing service;

- audit and approval service;

- observability stack;

- offline simulation and replay environment.

Edge sites may cache signed model versions and relay eligible client connections, but they should not receive household plaintext or individual updates.

# Part 6 — Honest gaps

## 6.1 Retrieval utility is not solved

The field does not have a universal metric for:

“Did this retrieved context causally improve this answer?”

Ranking metrics, LLM judges, attribution scores and human evaluations each measure different things. Generator changes can invalidate an otherwise stable retrieval benchmark.

## 6.2 Prompt-position bias is not well characterized

Classic ranking literature models human examination and clicks. HIP needs to model how an LLM consumes ordered, structured household facts. That is a related but different exposure mechanism.

## 6.3 Sparse explicit household feedback

Corrections and overrides may be highly valuable but rare. Non-corrections are ambiguous. HIP may require:

- structured user feedback;

- local teacher-model labels;

- carefully constrained exploration;

- domain-authored test cases.

## 6.4 Privacy–utility tradeoff for rare household patterns

Household-level DP will suppress rare, distinctive learning most aggressively. Those rare patterns may be exactly where personalization is valuable.

## 6.5 Poisoning remains difficult

Secure aggregation hides individual contributions, which is valuable for privacy but can impede update-level anomaly detection. Robust aggregation under secure aggregation is still an active engineering and research problem.

## 6.6 Right to deletion from a trained model

Removing local facts is straightforward. Removing their historical contribution from an already released federated model is not. DP limits contribution but does not provide exact machine unlearning.

## 6.7 Changing ontology and graph semantics

A Curator trained using one fact schema may behave incorrectly when:

- trust states change;

- key classes change;

- ownership semantics change;

- valid-time handling changes;

- new relationship roles appear.

The feature schema and governance model must be treated as part of the model contract.

## 6.8 Formal privacy does not equal semantic safety

A global model can satisfy a formal privacy budget and still learn an undesirable population-level behavior. DP protects individual contribution, not fairness, correctness, policy alignment or absence of harmful correlations.

# Part 7 — Engineering recommendation for HIP

## 7.1 Build a hybrid reranker

### Recommended architecture

    A. Hard policy and key-class eligibility

    B. Neo4j graph candidate generation

    C. Metadata and graph feature construction

    D. Frozen small semantic encoder

    E. LambdaMART reranker

    F. Deterministic context-set constraints

    G. Prompt assembly

### Why this wins

At tens to low hundreds of facts:

- exhaustive authorized-candidate scoring is affordable;

- approximate nearest-neighbor retrieval is unnecessary;

- structured graph metadata is unusually valuable;

- labels will initially be sparse;

- auditability matters more than benchmark novelty;

- a tree model can mix categorical, temporal, trust and semantic features;

- inference is comfortably CPE-capable;

- the rule system remains a reliable fallback.

### Why a full learned retriever loses

A DPR/SPLADE/ColBERT-style first-stage retriever would add:

- substantial training-data requirements;

- difficult negative sampling;

- more opaque failures;

- additional embedding lifecycle and revocation issues;

- more CPE runtime complexity;

- little speed benefit over scanning 100 facts.

### Why a pure rules system eventually loses

Rules cannot efficiently learn:

- household-specific relevance preferences;

- interactions among query type, fact category and recency;

- when an older corroborated fact beats a recent assertion;

- the marginal usefulness of including one more fact;

- patterns reflected in repeated corrections.

### Why a pure cross-encoder loses initially

A cross-encoder may produce stronger semantic relevance estimates, but:

- it scores every query–fact pair separately;

- CPE latency grows linearly with candidate count;

- it is harder to explain;

- it needs more supervised examples;

- it does not natively enforce HIP’s graph and policy structure.

Use it later as an offline teacher or to rerank only the top 5–10 candidates.

## 7.2 Initial feature set

### Hard eligibility—not learned

- requesting member;

- authenticated speaker;

- fact audience;

- subject;

- owner/author;

- key class;

- consent state;

- purpose limitations;

- revocation state;

- valid-time eligibility.

### Ranking features

**Query features**

- detected intent;

- subject/member requested;

- attribute requested;

- temporal language;

- action versus factual query;

- sensitivity class.

**Fact features**

- attribute and entity type;

- subject/owner/author relationship;

- trust state;

- corroboration count;

- valid-time distance;

- record-time recency;

- supersession state;

- contradiction state;

- source type;

- historical correction count;

- last successful use;

- frequency of use;

- explicit user priority.

**Query–fact interaction**

- lexical overlap;

- semantic cosine similarity;

- intent–attribute match;

- subject match;

- temporal compatibility;

- graph distance;

- expected token cost;

- redundancy with other selected facts.

**Set-level constraints**

- maximum facts and tokens;

- diversity by attribute;

- avoid duplicate facts;

- represent contradictions explicitly;

- prefer one authoritative representation where facts are equivalent.

## 7.3 Encrypted facts and transient plaintext

### Can the Curator rank cleartext available for only one turn?

Yes.

A valid architecture is:

1. Policy gate determines which encrypted fact objects may be considered.

1. Eligible values are decrypted within the requesting household’s trusted execution boundary.

1. Semantic features are computed transiently.

1. The ranker scores candidates.

1. Only selected facts enter the prompt.

1. Plaintext buffers and temporary representations are discarded.

Persistent training examples remain encrypted under the household’s keys.

### Embeddings are derived private data

A fact embedding can expose semantic information about the fact. It should inherit:

- the fact’s key class;

- audience restrictions;

- revocation lifecycle;

- deletion requirements;

- encryption-at-rest treatment.

Do not put cleartext embeddings from every household into a shared vector database and call the source facts encrypted.

### Metadata-only ranking

Metadata-only ranking is useful for:

- authorization;

- subject matching;

- trust;

- recency;

- valid-time handling;

- contradiction management;

- source reliability.

It is insufficient for semantic relevance. It cannot reliably distinguish:

- “Dad takes metformin”

- “Dad stopped taking metformin”

- “Dad asked what metformin is”

- “Susan is allergic to metformin”

unless those distinctions are perfectly normalized into structured attributes.

It also does not eliminate privacy concerns. Metadata such as attribute=alcohol_use, owner=father, or trust=unconfirmed may itself be sensitive.

### Recommended two-stage treatment

1. **Metadata and graph gate** over all eligible encrypted objects.

1. **Transient semantic scoring** on the reduced authorized set.

1. Store any reusable fact embedding encrypted under the same key class as the fact.

1. Recompute or delete the embedding whenever the fact changes, is revoked or is re-keyed.

Given the initial corpus size, decrypting all authorized candidates for the turn may be simpler and safer than building a complicated selective-decryption optimization.

## 7.4 The learner-isolation gate

### Literal interpretation

One household’s learning can never influence another household’s answer.

Under that definition:

- no federated household updates may enter the shared model;

- secure aggregation is insufficient;

- differential privacy is insufficient;

- central de-identification is insufficient.

The minimum viable implementation is:

- shared ranker trained only on public, synthetic and centrally authored examples;

- household feedback stored encrypted locally;

- household-specific calibration or local head trained only on that household’s CPE;

- local parameters never uploaded;

- global model updates cryptographically signed;

- runtime proves which model components are shared and which are local;

- local logs and heads are destroyed or re-keyed with household revocation.

That is the only clean route to **zero cross-household learning influence**.

### Bounded federated interpretation

A viable formal requirement would be:

No aggregator sees an individual household update, and each household’s effect on any released global Curator is formally bounded by user-level differential privacy.

The specific stack should be:

1. **Household-level update clipping**

1. **Secure aggregation**

1. **DP-FTRL or a validated user-level DP federated optimizer**

1. **Participation and contribution caps**

1. **Minimum release cohort**

1. **Privacy accounting across every model release**

1. **Local-only household head**

1. **Public/synthetic base pretraining**

1. **Signed training plan and client attestation**

1. **Gradient inversion, membership-inference and canary tests**

1. **Poisoning and robustness evaluation**

1. **No release when the approved privacy budget is exceeded**

### What must be proven

HIP would need evidence for:

- individual updates are cryptographically unavailable to the server;

- clipping occurs before an update leaves the trusted client;

- noise generation matches the claimed mechanism;

- the privacy accountant covers repeat participation and repeat releases;

- cohort composition cannot be manipulated to isolate a household;

- local heads are excluded from aggregation;

- raw examples and plaintext embeddings never leave;

- model and training code are signed and attested;

- rollback cannot reinstall a model trained outside the approved pipeline;

- experimental and production populations remain separated.

Even then the guarantee is bounded, not absolute.

## 7.5 CPE hardware recommendation

### Run on CPE

- Neo4j or local graph traversal.

- Eligibility checks.

- Feature construction.

- LambdaMART or small linear/MLP ranker.

- Frozen quantized MiniLM encoder, after hardware validation.

- Local encrypted outcome logging.

- Local training of a tiny calibration layer or ranking head.

### Do not require CPE to perform

- full transformer fine-tuning;

- end-to-end RAG retriever training;

- repeated cross-encoder replay across large local histories;

- global privacy accounting;

- secure aggregate reconstruction;

- global model evaluation and release.

Gboard proves that meaningful neural training can be performed on consumer devices, but that does not mean HIP should fine-tune a transformer on every gateway. Gboard operates at enormous population scale with mature device orchestration and highly repeated training signals. ([Google Research](https://research.google/pubs/federated-learning-for-mobile-keyboard-prediction/))

For HIP, CPE is appropriate for:

- inference;

- feature extraction;

- tiny local personalization;

- construction of protected federated updates.

The operator edge or regional cloud should handle:

- global aggregation;

- offline teacher models;

- extensive counterfactual replay;

- model evaluation;

- signed rollout.

# Build sequence

## Stage 0 — Instrument the rule system

**Ship first. No learned production behavior.**

Build:

- candidate impression log;

- selected fact log;

- policy and model versions;

- explicit correction and override events;

- answer outcome events;

- prompt-position records;

- encrypted local training-example store;

- offline replay harness;

- fact-selection gold test set;

- end-to-end answer regression set.

The current rules remain authoritative.

### Gate

No durable learning until the logs have been reviewed for cross-household identifiers, key-class inheritance and deletion behavior.

## Stage 1 — Offline hybrid Curator

Train a LambdaMART model from:

- authored scenarios;

- synthetic household graphs;

- manually labeled query–fact pairs;

- existing rule scores;

- locally replayed examples that remain inside the approved environment.

Use a frozen MiniLM encoder to produce semantic-similarity features.

Deploy in shadow mode. Do not alter prompts.

### Promotion criteria

- zero authorization violations;

- better Recall@k on required facts;

- no material increase in distracting facts;

- acceptable CPE latency;

- explainable disagreement reports;

- clean rollback.

## Stage 2 — Production hybrid Curator

Enable the learned reranker behind:

- hard policy gate;

- deterministic context constraints;

- rule-system fallback;

- canary rollout;

- automatic rollback.

Do not yet personalize globally from household outcomes.

### Failure behavior

Any feature, model or decryption error returns to the deterministic rules.

## Stage 3 — Local household personalization

Add a small local component:

- calibration vector;

- feature offsets;

- small linear head;

- possibly local nearest-neighbor memory over prior ranking examples.

Train it from explicit corrections and high-confidence local outcomes.

Keep it encrypted and household-local.

### Learner gate status

This stage satisfies strict cross-household isolation because household-derived parameters never leave the household boundary.

## Stage 4 — Federated research sandbox

Build the aggregator, but do not let its output affect production answers.

Test with:

- synthetic households;

- internal opt-in households;

- privacy red-team datasets;

- controlled gradient-inversion attacks;

- malicious-client simulations;

- repeated-round differencing attacks;

- client dropout;

- model rollback;

- privacy-budget exhaustion.

Implement:

- household-level clipping;

- secure aggregation;

- DP-FTRL;

- release cohort thresholds;

- privacy accounting;

- local-head exclusion;

- signed model distribution.

### Gate

The resulting model remains sandboxed until HIP decides that a bounded differential-privacy guarantee is an acceptable replacement for literal zero influence.

## Stage 5 — Federated global Curator

Proceed only after that policy decision.

Recommended operating model:

- daily federated rounds;

- weekly model release;

- at least approximately 1,000 completed households in an ordinary release cohort;

- formal household-level privacy budget;

- local personalization retained;

- staged rollout;

- rules always available as fallback.

The first federated component should be a **small differentiable scoring layer**, not the entire MiniLM encoder.

A practical progression is:

1. Keep semantic encoder frozen.

1. Federate a small linear or two-layer scorer over standardized features.

1. Keep household calibration local.

1. Consider federating deeper representation layers only after sufficient labels and privacy evidence exist.

LambdaMART is ideal for the early centrally trained Curator, but standard FedAvg does not directly train decision trees. Moving to federation therefore likely requires either:

- a small neural/linear ranker trained from the same features; or

- a specialized federated-boosted-tree protocol, which is operationally less aligned with the mature mobile-FL stack.

The first approach is cleaner.

# The three decisions that are yours

## 1. What “isolation” means

You must decide between:

- **Zero cross-household learning influence**, which rules out household-trained shared models; or

- **Formally bounded influence**, using household-level DP plus secure aggregation.

The literature cannot make these equivalent. They are different guarantees.

## 2. What failure the Curator should optimize hardest against

The loss function must reflect HIP’s actual priorities:

- omission of a decisive fact;

- inclusion of irrelevant facts;

- use of stale facts;

- failure to represent contradiction;

- excessive prompt size;

- correction frequency;

- answer-level task failure.

The field cannot tell HIP whether missing one critical medication fact is worth ten irrelevant-context inclusions. That is a product and risk decision.

## 3. Where decrypted semantic processing is permitted

You must decide whether decrypted fact values may be processed:

- only on in-home CPE;

- in an operator-hosted confidential-computing environment;

- or in an ordinary operator-controlled service.

That decision determines whether the Curator can use an edge cross-encoder, how embeddings are stored, what can be replayed centrally, and how much engineering must remain on the CPE.

Everything else can follow from those three calls.
