# What HIP governance actually does

Status: CURRENT
Reconciled-Against: roadmap HEAD 2026-07-29; every built-vs-designed status
line verified against the scope doc, the named REQ headers, and the code
before landing (D-13); lines the repo contradicted are marked [corrected]
inline with the accurate statement in place

A plain account of the governance pipeline: what it does on every turn, what
is enforced structurally, and what is designed but not yet built. Written so
a skeptical engineer can check each claim.

## The one-sentence version, corrected

A rough statement is: governance identifies the user and the sensitive
information, assigns it to the proper owner with a level of confidence,
passes it to the model, and confirms veracity on output, maintaining user
isolation and access by user.

That is close. Four points need to be precise, because the precision is the
product.

## 1. Identity is a declared field, not recognition

Every turn arrives with a typed identity. Access is keyed to it. Voice
matching is not real in the system today; it is treated as a future vendor
component, not something this codebase perfects. "Identifies the user" means
the turn carries a declared identity and access is scoped to it.

## 2. Owner and confidence are two separate properties

Each fact carries an owner and a subject: whose fact it is, who it is about.
That is the isolation axis. Separately, each fact carries a confidence or
trust level: how well attested it is. That is the veracity axis. These are
different columns doing different jobs. Isolation is about who may read;
confidence is about how sure the system should be. They are never merged.

## 3. Governance scopes what the model may see, before the model runs

This is the load-bearing correction. Governance does not pass everything to
the model and let the model judge. It decides which facts are allowed into
the prompt before generation. Isolation is a property of the retrieval set,
not of the model declining. When one member is refused another member's
medication, the fact was never in the candidate set for that turn; the guard
fired before any model was called. A model that declines is being agreeable.
A fact that was never retrieved cannot leak. It is a lock, not a promise.

## 4. The output check confirms no fabrication, not truth in the world

The output-side check, G0, is a fabrication backstop scoped to tracked
people: it fires when the answer names a tracked person about whom nothing
was admitted this turn, and it blocks that reply. [corrected: the draft said
G0 "confirms every fact in the answer traces to a fact that was admitted."
That is broader than the built check. G0 checks tracked-person naming
against the admitted set, not per-claim provenance for every fact in the
answer. A separate built check, the prompt-fidelity invariant, proves every
fact rendered into the prompt was contract-admitted. Neither confirms a
fact is true in the world.] Truth in the world is what the confidence
ranking tracks, from provenance and confirmation. There are three separate
things people conflate: which facts are allowed, that is isolation; how well
attested a fact is, that is confidence; and whether the model named a person
it was given nothing about, that is G0. Keep them apart and the account is
airtight.

## The quarantine boundary is membership, not sensitivity

Facts whose subject is a registered member are isolated: only the owner or
subject retrieves them, enforced before the model. Facts owned by the
household are not member-scoped; they enter every turn's context by design,
whether relevant or not. [corrected: the draft also said facts about a
non-member subject are not member-scoped. The code says otherwise. A fact
one member records about a non-member is scoped to its author: no other
member retrieves it, and this was traced live. What registration actually
changes is standing, not author-side scoping. A non-member subject has no
rights of their own over facts naming them, no named refusal on their
behalf, and no standing policy; and a household-owned fact about a
non-member, for example an aging parent's fall-risk pattern, is household
context and travels with every escalated turn. That is the real unquarantined
case.] Registering a person is what draws the rights boundary around their
facts.

## How confidence is established

Two mechanisms. First, provenance and corroboration: a clinic-confirmed
record ranks above one person's unconfirmed report, and the two coexist
rather than one silently overwriting the other. Second, explicit
confirmation events: a person confirming a report promotes it and closes the
record it replaces. When a lower-trust report challenges a higher-trust
head, the report parks as unresolved pending confirmation; confirmation
promotes it, then the old record is marked superseded. No model decides
confidence. A fixed rule reads the trust levels and parks or promotes.

## Conflict resolution: the offline consolidation pass

Write-time capture is fast and, where a contradiction cannot be called
cleanly, parks the fact as unresolved. Resolving parked contradictions is a
separate, scheduled, offline pass, by analogy to memory consolidation during
sleep. Off the request path, with full history in view, it reconciles
contradictions in batch, abstracts structure from repeated episodes, and
prunes stale traces. All logged, all reversible. This keeps the online path
fast and deterministic and puts the expensive integrative reasoning offline.

Where the pass cannot resolve a contradiction from history, it does not
guess. It opens a confirmation subprocess to the owner or a designated
surrogate, bounded by the same custody, isolation, and independence rules as
everything else, and the human's signed answer, not the pass's judgment,
resolves the fact. Where no independent party can confirm, it parks and
records that confirmation is needed and unavailable. It is a witness, not a
guardian.

## What is built and what is designed

Built and enforced today: declared-identity scoping, retrieval isolation
before generation, the owner/subject and confidence properties, the
park-then-confirm rule, the G0 output check, the prompt-fidelity check, and
operator-blind at rest: facts sealed under per-scope keys, and the master
key destroyed.

Designed, not built: per-member keys held on the member's own device
[corrected: the draft said isolation today is a policy check, not
independent cryptography, and that the operator can still derive a member's
key. That describes the frozen demo checkout, not this codebase. Here the
partition is cryptographic: each fact's key is wrapped to the reader set
for its scope, and the master key that once derived every member's key was
destroyed and proven unrecoverable. What remains designed rather than
built is device custody: the per-member private keys are software keys
generated and stored on the operator's box, not held in the member's own
device hardware. An operator with the box cannot use a master key, because
none exists; device-held keys are what would take the operator out of the
custody chain entirely]; operator-blind at inference: the fact is plaintext
in memory on the box while the model uses it, and closing that needs
confidential computing, adopted but not integrated; and the offline
consolidation pass with its confirmation subprocess [corrected in part: a
consolidation module exists in the memory engine code, but the memory
engine is not wired into the live path, and the confirmation subprocess
exists nowhere in code. Designed, not built, remains the honest status].

Operator-blind at rest is proven. Operator-blind at inference is not. The
two are never claimed as one.
