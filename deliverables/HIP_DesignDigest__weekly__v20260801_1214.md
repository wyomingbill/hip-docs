# HIP Design Digest
A running design note. Newest week on top.

## Week of 2026-08-01 (part 2) — the boundary, and what the testing plan actually was

Same week as the section below, filed later. That one settled *what* HIP may collect. This one is about *where the walls are* — and it is mostly a record of things that turned out not to be true.

### The monolith is right. It is not a boundary.
The ruling stands: the governance core stays monolithic inside a hard boundary, with voice and demo as contracted clients. The gates are ordered and interdependent, splitting the chain multiplies the surfaces where a check can be omitted, and at one household on one box there is no scale pressure at all.

What the recon established is that **the boundary exists in no running process.** Roughly fourteen modules reach a graph write, at least nine of them outside any defensible boundary, and every one of them gets there by `import`. There are three independent `:Fact`-CREATE implementations kept in agreement by comment discipline, and a fourth, older variant running live from the frozen checkout. Neo4j Community has no row-level access control, so the database credential is the entire wall — which makes N processes holding it not a smell but the hole.

So the correct name for the thing is a **reference monitor**, and its target property is **complete mediation**. Monolithic is the deployment shape; complete mediation is the security property; the first does not imply the second. Adopting the name is adopting the obligation.

### Distributing a policy chain and separating privilege are not the same move
Worth stating because the two get argued as one. Splitting an ordered policy chain into cooperating services is bad here — more surfaces, more omission, no isolation gained, and the failure mode is a caller that forgets to call rather than a caller that is refused. Splitting so that compromised code *cannot reach the data* is a different and much better-evidenced move.

The tell that this distinction is real: `INJ-7` is **disabled by default**. Pass `member_ids=None` and the gate is simply off. That is what a convention looks like from the inside — and an RPC boundary would make omission easier, not harder.

### The threat model, and the consequence nobody wants
Ruled in scope: careless code, a hostile household member, a compromised dependency, a remote attacker. The operator is **out of scope for now — deferred, not dismissed**; whoever holds OS root defeats everything here, which bounds what the audit record can ever be credible *to*.

The consequence, stated plainly: **three of those four defeat an in-process boundary in CPython.** Module privacy is a naming convention, annotations are erased at runtime, reflection reaches everything, and an admission proof HMAC'd with a key the forger can read is circular. **Careless code is the only adversary an in-process structural boundary stops** — which is worth building, and is precisely what A10 buys, and no more. Everything else needs the OS boundary: separate process, own UID, a credential the others do not have.

### Voice is untrusted by construction
Not a judgment about a vendor, and it does not change if the vendor changes. Voice parses hostile input in memory-unsafe runtimes; it is the component most likely to be compromised and the one HIP can do least about. **HIP does not secure the voice stack. The boundary holds whatever is on the other side.** Two hard rules: voice never holds a graph credential, and voice never executes in the process that owns writes. `turn/on_route/register_member/session_end` is therefore a **security** boundary, not a modularity one.

The live deployment is that ruling exactly inverted. The voice orchestrator runs governance code from the *frozen* checkout — so every gate improvement since the freeze is absent from the process actually taking audio — while holding the credential, the write path, the ledger append, and Whisper/Kokoro/resemblyzer in one heap.

### Belt and suspenders on identity
The sharpest consequence: **voice asserts identity and HIP believes it.** A compromised voice component claims any identity, and every gate below it then enforces the wrong answer *correctly*. The gates are not bypassed; they are fed a lie.

Ruling: voice asserts, **HIP verifies independently with its own voiceprint**, neither trusted alone. That has a contract consequence with a deadline — independent verification needs *audio*, so `turn(text, resolved_speaker)` becomes `turn(text, asserted_speaker, audio)`. The voice contract is being frozen in the other lane now. A field added to an unfrozen contract is free; the same field added later is a renegotiation. Containment: HIP runs only the embedding model, in its own subprocess, never a full STT stack — otherwise "verify independently" re-imports the whole attack surface it exists to keep out.

### The audit is tamper-evident against nobody
The ledger is genuinely good within its trust model: hash-chained, `F_FULLFSYNC` before the reply leaves, per-member payload keys so erasure is key destruction, chain hash over ciphertext so verification survives a shred.

And it has no structural separation at all. The append is called by the deciding process; `ledger/` and its keys sit under the same UID as everything else. Any HIP process can destroy a member key, delete segments, or rewrite the chain from genesis and re-hash — and verification reads the same disk it is supposed to distrust. **A hash chain custodied by the process that writes it is tamper-evident against nobody.** Also, by design, `append()` never raises toward the caller: a turn whose record failed still answers.

The cheap fix is **anchor, don't split** — sign the chain head periodically to somewhere these processes cannot write. That makes a rewrite *detectable*. A separate custody process makes it *hard*. Those are different properties and not substitutes, and which one is being bought is a ruling that has not been made.

### Models propose, the core commits
Model output is attacker-influenced input, and HIP's can write. Two model-output-to-write paths exist — extraction, and the frontier return path — and **neither has an authority gate** (TD-110). Anyone who can influence a transcript is injecting into a write-capable model channel.

A correction to the framing, though: the model *call* already crosses a process boundary everywhere. The exposure is not the call site. It is those two write paths, egress (TD-131, household facts reaching the MID/CORE payload unfiltered), and the voice process's shared heap.

### The testing plan was a document, not a harness
The uncomfortable one. The ceiling sprint produced a plan classifying all thirty acceptance rows into tiers. An audit of it found **three of thirty rows had an executable check.** The five runner files the plan names did not exist — none of them.

In fairness the plan never claimed otherwise; it says so in its own text. But the tier label *LIVE* means "runnable today and gating," and rows so labelled gated nothing, because they were not written. Two rows were caught this way before the audit (`A18`, `A10`); the audit established that this was the universal state rather than two misses.

Two smaller findings worth carrying. First, **four independent A-numbering schemes collide in this repo** — the ceiling's A1–A30, plus care-coordination, demo-smoke, and red-team schemes that also start at A1. A naive grep would have overstated coverage by four rows. Second, `A11`'s stated rationale — "passes because no promotion path exists" — is **false**: three ratified promotion paths exist, and R11 is satisfied by an actual *control* (the household-circle widening restriction) rather than by absence. Writing the fixture as specified would have produced a check red on arrival against correct behavior, whose only green path was deleting a ratified feature. That row is now stopped pending a ruling.

The general lesson, and it is not a new one here: **a passing row does not carry its requirement, and a classified row is not a wired one.**

### Earned calibration — an idea with its collision attached
`R18` is ruled **NOT MET**. The cascade built this week is correct as far as it goes, but only the `else` branch exists: everything is invalidated, nothing is ever recomputed. The built half errs toward *less* inference, which is the safe direction to fail.

The idea for closing it: early on, retracting a source kills the derived fact; over time HIP should rebuild from surviving parents, governed by a system-level confidence measure that starts small and grows.

The collision, recorded up front so it is not rediscovered: **a measure keyed on usage re-imports the engagement-earns-depth defect the ceiling eliminated.** The compliant, lonely, or cognitively declining household uses HIP most and would earn the most inferential latitude.

The defensible version keys on **validated correctness, not usage** — confirm rate on HIP's own derived facts, correction rate, survival through cascades — measured against ground truth HIP does not control. The discriminating consequence: a household that uses HIP constantly but corrects it half the time earns **less** latitude, not more. And a scope line makes it buildable: the measure may gate *inferential recovery* (whether an existing derived fact survives a parent retraction, inside the ceiling, since categories, audience, and retention still bind) and **shall not** gate *collection depth*, which the control rule forbids.

### Method note
The pattern that produced the good findings held again, in a sharper form: a reviewer holding the codebase, a reviewer holding only the literature, and the disagreement between them marking where the decision was. This week both agreed on direction and differed in what they could support — the literature pass supplied the naming (reference monitor, complete mediation), the code pass supplied the `file:line` evidence that the property is absent. Neither was sufficient alone. Worth noting too that the sharpest self-correction came from a test: a fault twin caught a case in its own battery that would have passed vacuously.

### Artifacts filed this week (part 2)
Hashes verified with `git log --diff-filter=A`, not recalled. Reviews are banked verbatim and UNVERIFIED by the sessions that filed them; REQs are FILED with acceptance NOT run; the design note proposes no requirement.

| Artifact | Path | Landed |
|---|---|---|
| R18 cascade — implementation | `harness/derivation_cascade.py` | `4ae70cc` |
| A18 acceptance battery + fault twin | `eval/test_derivation_cascade.py` | `4ae70cc` |
| D-81 dispatch — cascade built, R18 NOT MET | `docs/dispatches/DISPATCH_R18_CASCADE__derived-from-invalidation-on-retraction__v20260801_0755.md` | `4ae70cc` |
| TD-139 / TD-140 / TD-141 — the three R18 gaps | `docs/techdebt/DEBT_REGISTER__v20260731_2300.md` | `4ae70cc` |
| Fable architecture recon across four trees (banked verbatim) | `docs/reviews/FABLE_D84_monolith-vs-services__architecture-recon-four-trees__v20260801_0919.md` | `ae87034` |
| ChatGPT architecture research pass (banked verbatim) | `docs/reviews/CHATGPT_D84_architecture-research__reference-monitor-and-runtime-isolation__v20260801_0919.md` | `ae87034` |
| `REQ_ARCHITECTURE_BOUNDARY` — threat model, monolith, voice, inference | `docs/requirements/REQ_ARCHITECTURE_BOUNDARY__reference-monitor-threat-model-and-contracted-clients__v20260801_0919.md` | `ae87034` |
| Backlog #54 — independent speaker verification, urgent before the voice freeze | `docs/BACKLOG.md` | `ae87034` |
| A7 acceptance battery (regression tripwire, AST-based) | `eval/test_ceiling_representation.py` | `b88e629` |
| D-86 dispatch — the acceptance audit, A11 stopped | `docs/dispatches/DISPATCH_CEILING_ACCEPTANCE_AUDIT__three-of-thirty-wired-a7-landed-a11-stopped__v20260801_0930.md` | `b88e629` |
| `REQ_CEILING_ACCEPTANCE` — the plan audited above (§6 added D-88) | `docs/requirements/REQ_CEILING_ACCEPTANCE__testing-plan-for-the-ceiling-sprint__v20260801_0617.md` | `d7322d7` |
| Earned-calibration design note (filed against TD-140) | `docs/design/DESIGN_EARNED_CALIBRATION__validated-correctness-not-usage__v20260801_1214.md` | this commit |

Three notes rather than a summary. **`REQ_ARCHITECTURE_BOUNDARY` authorizes no code** — it records rulings and, deliberately, records the two properties the security story rests on that do not exist: a single-writer process that actually exists, and an audit anchor the writer cannot reach. **The ChatGPT pass's citations were not checked** by the session that banked it, and where it describes HIP's code it is repeating a framing rather than reporting an observation — which is exactly why the code-grounded recon is banked beside it. And **`A18` passes while `R18` is NOT MET**, which is the same shape as `A30` passing while `R30` is NOT MET: the acceptance row and the requirement are different objects, and this is now the second week in a row that distinction has done real work.

---


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
