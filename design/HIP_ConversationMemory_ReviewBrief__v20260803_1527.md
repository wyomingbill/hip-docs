Status: SUPERSEDED BY THE REVIEWS ABOVE (reviews/CHATGPT_ConversationMemory__conversation-memory-review__v20260803_1527.md,
and the Fable conversation-memory review — NOT banked in this pass, source file missing
from ~/Downloads at time of filing).
Version: v20260803_1527 (Mountain Time, per the CLAUDE.md Naming Law)
Reconciled-Against: 2026-08-03 (date-tested — read at filing, not remembered)

THIS IS THE DOCUMENT UNDER REVIEW, not a design of record. Its §5 proposed solution was
rejected by both external reviewers — ChatGPT's review of this brief opens "Your diagnosis
is right, but the proposed solution is not yet safe" and names the generative query
rewriter placed before governance as "the central security defect." Do not build against
§5 of this document. Read the reviews above it for the actual critique; this file is
banked for provenance (what was sent out for review), not as current design guidance.
Source file: HIP_ConversationMemory_ReviewBrief.md (~/Downloads), banked verbatim, unedited
below this line.

---

# HIP — Conversation Memory: Current State, Problem, and Candidate Solutions

**For external review (ChatGPT, Fable). Prepared 2026-08-01.**

**What this is:** HIP has no conversation memory. Every turn is independent. We want this reviewed before we design a fix, because the obvious fix breaks the system's central security property.

**How to read the evidence markers:** claims marked **[verified]** were confirmed by reading or executing the live code this week. Claims marked **[inferred]** are reasoning we want challenged. Claims marked **[observed]** are live run outputs.

---

## 1. What HIP is

A household assistant that holds facts about a family — appointments, medications, schedules, an address — and answers questions about them. Multiple people share it. The product claim is that it enforces *who may see what*, structurally, in code, rather than by asking a model to behave.

The enforcement layer is called the **injection contract**. Every turn, before any model is called, it decides which of the household's facts are admitted into the prompt. Facts that are not admitted are not in the prompt at all — the model cannot decline to reveal them because it never sees them.

Concrete example, run live: Sam asks "What medication is Maya on?" The contract denies the fact, the model is never called, and the reply is a deterministic string. The turn record shows `inference_ms = null`. That is the product.

---

## 2. Current state — turn processing

**[verified]** Each turn is fully independent.

- `session_id` is the literal string `f"text-{member}"`. It is a fixed identifier, not a conversation handle. There is no thread behind it.
- The model prompt is rebuilt from scratch on every call: system prompt + the current query. Nothing from any prior turn is appended.
- Governance decisions are recomputed from the raw query text every turn.

**[verified]** The order of operations within a turn:

1. **Disclosure gate check** (`harness/disclosure.py:146-152`, called at `server/voice_orch.py:2830`). A five-term keyword regex — `setback|zoning|zone district|variance|title 17`. On match, the turn builds a consent payload and **returns immediately**. Nothing downstream executes. A turn is either a consent-gate turn or an answering turn; never both.
2. **Intent classification.** Cosine similarity against ~114 exemplars. Below threshold it defaults to `knowledge`.
3. **Complexity / tier classification.** Bloom's-taxonomy level from *phrase patterns* — literal regexes over the query string.
4. **Injection contract.** Decides admitted facts. Sequence includes INJ-3 (cross-member deny) before INJ-2 (relevance), then INJ-4 (household), INJ-5 (never volunteer), INJ-6 (empty-set guard), INJ-7 (named cross-member refusal).
5. **Context assembly** (`assemble_governed_context`). Renders admitted facts into the system prompt.
6. **Generation**, on whichever tier was selected.
7. **Record write.** A per-turn epistemic record: which facts were admitted, which denied and why, tier, whether a model ran.

**[verified]** The only cross-turn state that exists is a narrow `control_state` carrying the previous tier and query plus a frontier-confirm-pending flag. It is consulted only for explicit control verbs — "try again", "reconsider" — and for two purpose-built continuations: approving a frontier disclosure ("Yes, go ahead") and confirming a parked fact write.

So: purpose-built two-step interactions work. General conversation does not.

---

## 3. The problem

**[observed]** Turn A: *"How do I work out whether taking the car on the morning of the 12th conflicts with any appointments?"* → correct answer using two facts.

Turn B: *"What about 8am?"*

The system does not say "I don't know what you're referring to." It answers a **different question**, confidently:

> "You usually start your day around that time, checking emails..."

No error, no hedge, no signal. The turn record looks normal.

**[verified]** The same question with the reference filled in — *"What about 8am on the 12th?"* — answers correctly 5/5, on a lower and more deterministic path.

**Why this matters beyond a bad answer.** The system's honesty story rests on the record: the record shows what was admitted and whether a model ran. But the record cannot show that the *question itself* was incoherent. A turn whose subject was never resolved looks identical in the record to a turn that was fully understood. The failure is invisible to the very instrument we point at to prove correctness.

**Product significance.** The target user is a household talking to a shared assistant, increasingly by voice. Speech uses far more anaphora than typing — "what about her", "is that still true", "the other one". A system that silently misinterprets those is not a household assistant.

---

## 4. Why the obvious fix is dangerous

The obvious fix is to keep a message history and prepend prior turns. In HIP specifically this breaks three things simultaneously. We want this section attacked hardest.

### 4.1 It breaks member isolation — the central product claim

**[verified]** The contract's cross-member checks gate on the *requesting member* of the current turn. Facts admitted for member A were admitted because A asked.

**[inferred]** If turn N's content persists into turn N+1 and the speaker changed, facts admitted for A are now in B's prompt. Nothing re-evaluates them, because admission already happened.

This is not hypothetical for us. One of our three demo scripts runs three different speakers in sequence and its entire claim is that each gets different governance. Naive history would leak across that boundary — quietly, with the record showing a clean turn.

### 4.2 It breaks relevance scoping

**[verified]** INJ-2 (`harness/injection_contract.py:279-314`) admits a member-owned fact by keyword-matching the *raw query text* against a regex keyed to the fact's attribute name. For `attribute="appointment"` the pattern is:

```
\b(appointments?|appt|scheduled?|visits?|meetings?|when|calendar|upcoming)\b
```

Household-owned facts short-circuit to admitted before this check runs.

**[inferred]** If prior queries remain in the prompt, their keywords keep admitting facts for turns where the current question would not. Relevance decays into "anything mentioned recently," which is the opposite of scoping.

### 4.3 It breaks record fidelity

**[verified]** Each turn's record attests the fact set for that turn.

**[inferred]** With carried history, the model sees a superset of what the record claims. We already have a filed defect in this family — the prompt is assembled from a separately rebuilt local variable rather than from the contract's own output — so the record's fidelity is already a known weak point. Carried history would widen it structurally rather than accidentally.

---

## 5. Candidate solution — resolve references, never carry facts

**Shape:** carry only enough prior context to *complete the question*. Never carry facts, never carry admitted context.

A resolution step runs **before** governance:

```
raw:       "What about 8am?"
resolved:  "What about 8am on the 12th, regarding the appointment conflict?"
           ↓
           full injection contract runs fresh on the resolved query
```

**Claimed properties:**

- No fact crosses a turn boundary. Isolation and relevance scoping are untouched, because the contract still runs from scratch on a single query string.
- The record still attests exactly what was admitted for this turn.
- A speaker change simply re-governs from zero. There is no accumulated state to leak.
- It composes with an already-ruled architectural direction: models propose, only the core commits. The resolver proposes a completed query; it commits nothing.

**Open questions we have not answered:**

1. **What does the resolver read?** Prior queries only, or prior answers too? Answers contain admitted facts, so reading them reintroduces the leak through the back door.
2. **Whose prior turns?** Same speaker only is the conservative answer. But a household conversation is genuinely multi-party — "what about her appointment" said by Bill referring to Maya's turn is legitimate and common.
3. **Does the resolved query go in the record?** We think yes, alongside the raw one, or the record misdescribes what was governed.
4. **The resolver is attacker-influenced.** Its input is prior conversation, which under our threat model includes a hostile household member. A resolver that can rewrite a query can rewrite it into one that admits facts the original would not — e.g. injecting the word "appointment" to trip INJ-2's keyword. **This may be the most serious objection to the whole approach** and we want it examined directly.
5. **What happens when resolution fails?** The current failure mode is a confident wrong answer. Any fix must fail loudly instead. What is the correct behavior for an unresolvable reference?

---

## 6. Alternatives we have considered and not chosen

**Do nothing; require complete questions.** Honest and zero-risk. It is what we do today. It makes the product a command line with a friendlier syntax.

**Carry history but re-run the contract over it each turn.** Re-governs everything every turn against the current speaker. Cost is that the prompt grows and every prior fact gets re-adjudicated, which multiplies the surface where relevance scoping can go wrong. Also unclear what "relevance" means for a fact admitted three turns ago.

**Resolve references inside the model call.** Give the model the history and let it sort it out. Rejected on principle: it moves a governance-relevant decision into the model, and our entire thesis is that governance decisions are structural.

---

## 7. What we want from review

1. **Attack §4.1.** Is naive history actually a cross-member leak, or have we overstated it? Is there a formulation where history is safe?
2. **Attack §5, question 4.** Can a reference resolver be made safe when its input is attacker-influenced? If it can rewrite a query, it can rewrite governance outcomes. Is there a constrained resolution grammar — pronouns and temporal references only, no new content words — that closes this?
3. **Is there prior art?** Multi-party, per-turn-authorized dialogue systems. We would rather adopt a known design than invent one.
4. **Is the failure mode the real problem?** One reading is that the gap is not "no memory" but "no way to signal an unresolved reference." A system that reliably said "I don't know what you mean by *that*" might be sufficient and far cheaper.
5. **What are we not seeing?** We have been close to this code for weeks. We expect there is an obvious objection we have gone blind to.

---

## Appendix — related known behavior, for context

Each of these is verified and relevant to how a reviewer should read the above.

- **Tier is computed from phrasing alone.** It has no relationship to how many facts are in context. A turn scored MID with exactly one fact available. Bloom level comes from literal phrase patterns; "pros and cons" scores 5, "tradeoffs between X and Y" scores 2. Filed as TD-130.
- **Household-owned facts are exempt from all scoping checks by design.** They are admitted into every turn, including questions unrelated to them.
- **Intent classification defaults to `knowledge` below threshold** — and `knowledge` is the intent that strips personal facts and disarms two guards. The default state under uncertainty is the least restrictive one. Filed.
- **The disclosure gate is a hard early return.** A turn cannot both answer from held facts and raise a consent prompt.
- **The voice layer is treated as untrusted by construction**, and a separate ruling requires that voice never hold a graph credential and never execute in the process that owns writes. Any conversation-memory design must not become a way for the voice layer to influence governance across turns.
