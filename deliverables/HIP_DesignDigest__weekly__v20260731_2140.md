# HIP Design Digest
A running design note. Newest week on top.

## Week of 2026-08-01

**Consent, authorization, and the dimensioned ceiling.**

### The defect
Every depth control fired only on a negative signal — withdrawal, decline, disengagement. The population most at risk of over-collection emits none of them. Compliant, lonely, deferential, and cognitively declining members engage MORE, which under "follow engagement" earned depth FASTER. The safety mechanism was structurally blind to exactly the users it existed to protect.

### The fix is not a better detector
No validated instrument separates enthusiasm from compliance in free conversation without a cohort. Elaboration rate, answer length, warmth, and unprompted disclosure are engagement measures, not consent-validity measures.

### Control rule
Engagement may justify OFFERING a deeper capability; it may never itself AUTHORIZE deeper collection. Depth stops being earned and becomes granted.

### The ceiling is dimensioned, not scalar
Categories and representations, retention, audience, inferential reach, plus solicitation as a fifth axis. The harm runs on kind, not volume.

### A trust cap is not an inference ceiling
HIP capped an inference's confidence but never its subject matter. A low-confidence "probably has dementia" is still stored, exposable, and stigmatizing.

### Authorship is not ownership of the subject
The author keeps their own sentence — entrenched by the DEK wrap. They do not get the subject's response, corroboration, derivatives, aggregation, or profile.

### Thesis extension
Context management compounds, and so does the governance record. The five axes are not a compliance layer bolted on; they are the constraint set that makes the memory architecture defensible to an operator carrying Cable Act obligations.

### Method note
The strongest findings came from adversarial review by a reviewer holding the codebase, cross-checked against a literature pass by a reviewer holding neither. Where they disagreed was where the decision actually was.

### Artifacts filed this week
Every claim above is traceable to a committed artifact. Reviews are banked verbatim and UNVERIFIED by the sessions that filed them; the REQ is FILED with acceptance NOT run.

| Artifact | Path | Landed |
|---|---|---|
| D-46 critique of the seeding roadmap, Parts 1-3 (banked verbatim) | `docs/reviews/FABLE_D46_critique__household-seeding-parts1-3__v20260731_1258.md` | `d5433da` |
| D-61 critique of the progressive-authorization answer, against HIP | `docs/reviews/FABLE_D61_critique__progressive-authorization__v20260731_1831.md` | `92a4646` |
| D-63 dimensioned-ceiling axes — two sources in one file, unmerged | `docs/reviews/D63_dimensioned-ceiling-axes__fable-and-chatgpt__v20260731_1917.md` | `0dab917` |
| `REQ_STRUCTURAL_CEILING` — first filing (30 requirements, 30 acceptance rows) | `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2057.md` | `98dfb7a` |
| `REQ_STRUCTURAL_CEILING` — current, supersedes the above | `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2129.md` | `b0bc8e3` |
| TD-137 — sensitivity `critical` misranks below both `high` and `low` | `docs/techdebt/DEBT_REGISTER__v20260731_1352.md` | `9acc5a2` |
| TD-138 — care-team authorization is epoch-blind | `docs/techdebt/DEBT_REGISTER__v20260731_2016.md` | `78939bc` |

Two notes on that table rather than a clean summary. The REQ is listed twice on purpose: `98dfb7a` is the filing the dispatch referenced, and `b0bc8e3` supersedes it the same day with the R16 ruling (both mechanisms — opaque commitments in the chain, payloads off-ledger under per-member keys), an R12 rewording to a propagation cap, and a false-MET correction. And both TDs are OPEN, neither fixed: TD-137 awaits a ruling on which of three divergent sensitivity encodings is authoritative, and TD-138 is dormant only because no care team is enrolled — it arms on the first enrollment.

---

## Week of 2026-07-25

### Thesis
The durable IP is not the model. It is context management, memory architecture, interaction management, and governance. Models commoditize. Memory and governance compound.

### Architecture
Swappable components: voice, interaction manager, context manager, router, reasoning model, memory. Each replaceable without rebuilding the others. OpenRouter is a good dev start: one API, one bill, easy model comparison. Direct contracts later.

### Context manager
Context is an optimization problem, not a retrieval problem. Maximize expected answer quality under token and privacy constraints. Move from top-K vector retrieval to utility-optimized context packs. Test for including a memory: does it improve this answer.

Ten scoring dimensions: relevance, confidence, importance, recency, sensitivity, authority, volatility, dependency, retrieval cost, actionability.

Learning loop: start with rules plus bloom, collect outcomes, corrections, counterfactuals, then train a small retrieval-policy model. Large teacher model grades offline.

### Interaction manager
Distinct from the context manager. Decides turn-taking, modality, private vs shared. Multi-party voice is unsolved; plan a multi-modal fallback. Training data comes from real household interactions: acceptances, overrides, corrections.

### Sequencing
Depth over raw household count early. Tens, then hundreds. Validate context and memory with text or push-to-talk first. Delay full-duplex voice until the brain proves itself.
