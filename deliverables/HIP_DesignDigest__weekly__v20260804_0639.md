# HIP Design Digest
A running design note. Newest week on top.

## Week of 2026-08-04 — three requirements ruled not met, and what a lock has to be to count

The prior section ended with a structural-refusal guarantee that had just been fixed and a
set of instruments that made the fix fast. This one is mostly about what happened when
those instruments were pointed at the requirements themselves: three rulings, all NOT MET,
each for a different and more interesting reason than "unfinished."

### Silent absorption is a distinct failure from unbuildable

R8's write-time representation classifier landed (`bc56fc4`) and was ruled **NOT MET** the
same evening (`317212a`). The interesting part is the ground. Four of the fourteen
representation classes are in `ABSENT_CLASSES` — the classifier cannot produce them — but
facts of those kinds are still written every day. They do not bounce. They are absorbed:
`COGNITIVE_OBSERVATION`, `FUNCTIONAL_SUPPORT_STATE` and `EXTERNAL_PROFESSIONAL_DIAGNOSIS`
all land stamped `HEALTH_CLAIM`, because the attribute-name lookup is the only signal
consulted.

The fourth is sharper still. `THIRD_PARTY_NONCARE_DOSSIER` has no single class it lands in
— it **scatters** across whichever class the attribute happens to produce, because the one
signal that would identify it (the subject) is never consulted. So the class is not merely
missing; the system cannot even tell you where its instances went.

**That is a different failure from "we have not built it."** An unbuilt control is visible
as an absence. An absorbed one presents as a stamped, classified, apparently-governed fact,
and the requirement it belongs to reads as further along than it is. Naming it as its own
mode is what made R8's ruling something other than a schedule note.

The reason the subject signal is not consulted is worth recording because it is not a
principle: `dad` and `household` are not enrolled in the identity registry, so a
subject-identity test classified real household facts as third-party dossiers. The honest
move was to remove the test rather than ship a classifier that refuses legitimate writes —
leaving one of R9's six never-store categories with no write-time check behind it, for a
**data** reason. Filed rather than absorbed.

### A requirement can be enforced and still not be met

R2's typed inference permit was built and enforced at the single materialization point, and
was then ruled **NOT MET** (`3989ba2`) on a scope gap: R5, R6 and R7 are inside R2's
requirement and were unaddressed by the build.

R5 — no self-expanding inference — turned out to **hold vacuously, and unmonitored**. Every
site reading `derived` was enumerated: a confidence cap that narrows, a read-path exclusion
that narrows, render-hint text with no side effect, one pinned scorer feature, and the
lineage cascade, which narrows. The one mechanism that could have looked like
self-expansion — the must-confirm queue, which is R5's own explicitly-permitted "neutral
suggestion that human review may help" — is structurally excluded from derived facts,
because its query selects `write_state='unresolved'` and the derived writer always stamps
`augment`.

Holding by absence is not the same as holding by control, and the difference is only
visible if someone goes and looks. The generalisable point: **"no code does X" is a
finding with a shelf life.** It is true until the first commit that adds a path nobody
checked against the requirement, and nothing in the tree announces that moment.

R10 stayed NOT MET as a consequence rather than a judgement — it is downstream of R2 and
R8, and flips when they do, not when someone finishes wiring it.

### What a lock has to be before it counts as one

The advisory `.hip-lock` had failed three ways across the project's history: written through
while another lane held it, clobbered unread, and taken late twice. The build (`23b26d1`)
replaced it with `fcntl.flock` held for the lifetime of the guarded command — a second
process is refused by the kernel, at exit 75, not advised by a convention.

Two design points earned their keep:

**The lock is keyed on the resource, not the checkout.** One lock per repository (shared by
every worktree of it) and one per Neo4j port (shared by every checkout pointed at it). A
per-checkout marker could name neither contended thing, which is exactly how two sessions
could each hold "the lock" and still collide: they held different files, and the thing they
were contending for was a third thing neither file named.

**Acquisition is a precondition of the tooling, not a step.** The harness runner re-execs
itself under the lock. Late-taking is not discouraged; it is unreachable. This matters
because the two late-takes were committed by sessions that knew the rule, meant to follow
it, and did the work first anyway — discipline is not a mechanism.

On the graph side, the fix was the opposite of infrastructure: an unconfigured checkout now
**fails** rather than silently falling back to an unowned default instance that had no
accountable owner. Then five dormant worktrees were retired (`6750593`), which removed the
three-way port collision **by subtraction** — stronger than the serialisation the lock
provides, and cheaper than standing up more database instances on a machine that has
already measured itself out of headroom once.

A latent hazard surfaced in that work and was closed the next morning (`ca34ec4`): the demo
environment file was **tracked**, so every worktree carried a copy pointing at the frozen
demo's graph. Config that follows a checkout around is a hazard whatever its contents.

### A board that reports a claim, and then checks it

The ceiling status board (`50daa12`) renders all thirty requirements from the documents
themselves — no hardcoded status anywhere, and a test that fails if one ever appears. Two
choices are worth carrying:

**A parse that finds nothing must fail, not render.** An empty scan would have produced a
clean page with nothing red on it — the most reassuring possible output and a complete lie.
**And UNDETERMINED is a counted outcome**, not a fallback bucket: a status the text cannot
settle appears on the board as unsettled rather than being quietly sorted somewhere
flattering.

Pointing it at the documents immediately found three defects in them, all introduced by the
same recent edit: two malformed table rows that made the first run parse zero tiers, a
count that disagreed with the ids its own cell listed, and a cell that named rows as
*removed from* a tier — which any enumerator reads straight back into it.

Then the board was made to check its own headline claim (`ca223d4`). It had been reporting
the acceptance document's LIVE tier at face value; now it cross-checks each LIVE row against
a real runner. Six of nine verify. Three do not — **and they are tested.** Their coverage
predates the naming convention the cross-check relies on, so the tool cannot see past the
names. That is a **visibility** gap, not a coverage gap, and the distinction had to be
written into both the tool's output and the register, because the amber cell looks identical
either way to someone skimming.

### One red, three symptoms, two correct mechanisms

The memory harness's persistent failures got traced (`ca34ec4`) rather than re-argued.
MEM-116, MEM-117 and MEM-118 are **one root cause**, not three defects: a fixture that is
deliberately restored to a corroborated trust level, and a governance gate that refuses a
single conversational utterance's attempt to supersede a higher-trust cross-principal
record. Both pieces of code are correct. Their interaction makes the scenario as scripted
unable to pass.

The methodological point is the one worth keeping: **a red that reproduces identically
three times is not flaky, and "environmental" is a claim requiring the same evidence as any
other.** The mechanism was confirmed by capturing the exact log line the gate emits, not by
inference from the symptom.

## Week of 2026-08-03 — protection that scaled with visibility, and the cost of establishing a width

Three things this week were about the same thing from different sides: a guarantee that
looked structural and was not, a plan that looked wired and was not, and instruments that
made the difference visible fast enough to act on.

### The guard protected only the subjects you could already see

The system's claim is that the model cannot decline to reveal what it never saw — disclosure
is decided structurally, before generation, and the model realizes wording inside a decision
already made. For one class of question that claim was not true, and the reason is the
interesting part.

Both empty-set guards share a precondition nobody had written down as a precondition: they
require a RESOLVED subject. Subject resolution matched a named entity against the requester's
own visible facts plus the registered members. A care recipient — Ray, Dad — is deliberately
not a member, and their facts belong to whichever member wrote them. So when Sam asked about
Ray, Ray did not resolve, no guard was eligible, and the turn fell through to the model,
which declined out of its own good manners. **Protection scaled with visibility: you were
structurally protected exactly where you could already see, and left to the model's
cooperation everywhere else.** That is close to backwards — the boundary matters most
precisely where the requester cannot see.

The fix separated two things a single variable had been doing. Resolution now draws on every
subject the graph knows; admission still draws on the registered-member list the access
boundary keys on. **Resolution is not disclosure** — naming a subject admits nothing, and
the two id sets are deliberately never merged, because merging them would have made the
cross-member boundary deny an owner their own care-recipient facts. The refusal then keys on
the admitted set alone, and a withheld-but-visible fact no longer keeps the turn on the model
path. Deny-silently survives by refusal IDENTITY rather than by staying model-side: "exists
but withheld" and "does not exist" produce the same structural refusal, so nothing
distinguishes them to the asker.

One residual is worth naming rather than discovering later: subject KNOWNNESS is now
observable — a graph-known name gets a fast structural refusal, an unknown string goes to the
model. That leaks that a NAME is known to the household, not that any FACT exists. Fact-level
indistinguishability is what was required, and it holds.

### The model-cooperation finding, and what it cost to establish its width

The finding itself was cheap: an instrument built to grade refusals from the execution record
rather than from reply text immediately showed rows where no gate fired and the model had run.
Under text grading those rows were green, because the model's refusal reads exactly like a
structural one. **A refusal where no model ran and a refusal the model was told to produce
look identical on screen and are not the same guarantee.**

Establishing how WIDE it was cost four dispatches, and the cost is the lesson. The first
headline was wrong in a way that mattered: it claimed a cross-member fact that EXISTS was
protected only by the model's cooperation. Re-read against the fixture, no such fact existed
— the requester owned the content he was reading, and nothing leaked. The correction did not
make the class less real; it moved it. And it exposed the actual gap: **the scenario that
mattered — a non-owner reading another member's existing fact about a non-member subject —
had zero rows out of thirty-one.** The combination was valid in the generator and had simply
never been sampled. Rows for it had to be written before anything could be measured, and once
written they failed identically across two runs, which is what distinguished a deterministic
code defect from the model-whim flake sitting next to it.

Two habits paid for themselves here. **Grade from the record, not the prose.** And **when a
row's expectation and the code disagree, consider that the expectation is the defect** — one
row was asserting a structural refusal for a case where the design deliberately keeps an
admitted, requester-owned fact in front of the model. That row was corrected, not the product.

### A test plan can be classified and still not exist

An external testing-practice review named three builds. The one that stung: a disclosure
oracle sitting in the repo, with its own test file, **referenced by no runner** — not the
harness, not the batteries, not the shell wrapper. Its sibling in the same package is wired
and runs every pass, which is what makes the orphan legible as an orphan rather than a
convention. Weeks of coverage that reads as present in the tree and is absent at runtime.

The same shape, at a different scale, is in the acceptance plan for the collection ceiling:
thirty rows classified into tiers, twelve of them writable and wired, sixteen honestly marked
UNWRITABLE because their fixtures do not exist. The honesty is the good part. The hazard is
that a classified row and a wired row look alike in a table, and only one of them can fail.
**Classification is a claim about intent; wiring is a claim about behavior.** A plan that
records the difference stays useful; one that blurs it becomes a comfort.

The review's other two builds — two-sided reporting (false-release and false-denial as a
pair, rather than a ratchet that only moves one way) and a tail corpus — have no code at all.
That is worth stating plainly rather than filing as a gap: the ratchet is a regression
detector, not a measurement, and nothing today reports the two error directions together.

### The velocity instruments

Five dispatches took a defect from "the model happens to refuse" to "a structural gate
refuses, proven twice, ruled MET" inside a day. What made that possible was not speed of
typing.

**The ratchet plus an accepted-red baseline.** A known red carries an ID and a justification,
so a new red is visible instantly against a noisy background. This is also the instrument
that nearly failed: the updater rewrote its own accepted justifications twice in two days,
both times caught only by a human reading the diff. A record the tool can silently rewrite is
not a record.

**Fault twins and anti-vacuity, as a convention rather than a virtue.** Every check ships
with a twin that must go red on command and a case asserting the check can see the real tree.
The convention caught a battery that would have passed against an empty scan and, separately,
a scanner that could not see a literal wrapped across two source lines — the same wrap hazard
that had already defeated a hand survey.

**Trace before build, as a gate rather than advice.** The requirement that closed this week
recorded a mechanism that the mandatory pre-build trace then falsified. Had the fix been
built against the filed mechanism, it would have keyed on the wrong thing and passed its own
acceptance. The trace was worth more than the fix.

**Corrections that land as records.** Two filed mechanisms and one headline were wrong this
week and were corrected in new records that name the old ones. The alternative — quietly
better wording next time — is how a register becomes decorative.

**And the format lesson.** A count is a claim that ages; a pointer is not. A status line that
enumerated what had been ruled went stale five times in five weeks, always in the safe
direction and always invisibly, until it was deleted and replaced with a pointer to the
section that actually carries the rulings.

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
