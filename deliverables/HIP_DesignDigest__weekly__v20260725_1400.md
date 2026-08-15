# HIP Design Digest
A running design note. Newest week on top.

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
