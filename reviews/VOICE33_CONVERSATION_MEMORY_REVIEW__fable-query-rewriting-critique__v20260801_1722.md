# VOICE33_CONVERSATION_MEMORY_REVIEW — Fable
Status: BANKED / **UNVERIFIED-BY-CONSTRUCTION**
Reconciled-Against: banked 2026-08-01 (Voice 33), ~/hip-vo branch voice-port @ c13050a

Reviewer: Fable
Dispatch: "Index Voice 33"
Subject: conversation memory / reference resolution — critique of the query-rewriting
design proposed in section 5 of `HIP_ConversationMemory_ReviewBrief.md`.
REQ proposed: **none.** This review names work items; they are Bill's to rule on and
they belong to the MAIN DEVELOPMENT LANE, not this one. Nothing here authorizes a build.

---

## PROVENANCE — read this before treating anything below as verified

**The source was a conversation, not a file. No independent artifact existed to diff
against. Verification is therefore NOT byte-comparable, and none is claimed.**

This review was produced by Fable in a chat session in response to the brief. It was
never written to disk by its author. At banking time it existed only as conversational
output, so it was reproduced here from that output on Bill's explicit authorization
(Voice 33, 2026-08-01).

**No `diff` was run and no sha256 is presented as verification.** Both would have been
circular — hashing a reproduction against itself proves only that a copy is a copy. The
other review banked in this directory
(`VOICE33_CONVERSATION_MEMORY_REVIEW__chatgpt-research-*`) DOES carry a real
source-file diff and sha256; the asymmetry between the two headers is deliberate and
should not be read as an oversight.

What that means for a reader: treat the text below as a faithful reproduction, not a
verified one. If it matters — for a diligence conversation, or as evidence in a ruling —
the reproduction should be checked against the original chat transcript by a human
before it is relied on.

**Doubly unverified.** Beyond the provenance limitation above, this is a REVIEW: its
findings are the reviewer's claims, and no dispatch has confirmed them against the
codebase. Four claims in it were verified by the reviewer against live code at
`~/hip-roadmap` @ `ebb1713` and are marked as such inline; everything else is argument.

**NOTE ON THE DOCUMENT UNDER REVIEW.** `HIP_ConversationMemory_ReviewBrief.md` was NOT
on disk at banking time. If it is filed later to `docs/design/`, this header should be
amended to cite it.

**CONVERGENCE.** The ChatGPT review banked alongside this one reached the central
finding — that a generative query rewriter placed before governance is a declassification
mechanism controlled partly by attacker-supplied dialogue — independently, from a
different starting point and without sight of this text. Two reviewers converging on the
same defect in section 5 is the strongest signal against the proposed solution.

---

Reviewed. I verified the four claims my sharpest objections depend on rather than arguing from your summary — citations below are from the live code at `ebb1713`.

**The headline: §5's proposed mitigation is refuted by evidence you already quoted in §4.2, and §5's central claimed property is false as designed.** Details in order.

---

## 1. Attack §4.1 — you have overstated it in one direction and understated it in another

**Overstated:** `session_id = f"text-{member}"` is *already per-member*. Naive history keyed on the existing handle does not mix speakers at all — bill's turns accumulate under `text-bill`, sam's under `text-sam`. The leak you describe requires inventing a *new, shared* conversation key. So "naive history leaks across members" is not a property of naive history; it's a property of one specific keying choice you haven't made yet.

That matters because it turns your framing inside out: per-member keying gives you isolation for free — and destroys the thing §5 question 2 calls legitimate and common ("what about her appointment," Bill referring to Maya's turn). **Isolation and multi-party continuity are not two open questions. They are one forced choice, and your document treats them as separable.**

**Understated:** you already own a partial mitigation and haven't credited it. G0 (`g0_invariant.py:59-64`) fires when the reply *names a tracked person other than the requester* while nothing was admitted this turn. Under carried history, this turn's admitted set is empty — so G0 fires on exactly the leak you're worried about.

Except it's name-based (`known_subject_ids`). "Maya's medication is X" trips it. **"Her medication is X" does not.** The mitigation you have covers naive history *except through pronouns* — and pronouns are the entire feature. That is a much sharper statement of the risk than the one in your document, and it survives the "have we overstated it" challenge where your version doesn't.

## 2. Attack §4.2 — implementation-contingent, not intrinsic

INJ-2 keyword-matches the query *string*. If carried history lives in the messages array and the contract governs only the current turn's text, **INJ-2 never sees it and §4.2 evaporates entirely.**

But that same choice makes §4.1 strictly worse: the facts are now in the model's context with nothing re-adjudicating them. §4.2 and §4.1 are the same dial at two settings, not two independent breakages. Concatenate history into the governed string → relevance decays. Keep it in the message array → unre-governed facts. Your document presents these as a list of three things that break; it is really one thing that breaks two ways depending on where you put the text.

(§4.3 stands unchallenged. It's correct and it's the one I'd worry about most in a diligence conversation.)

## 3. Attack §5 question 4 — the constrained grammar does not close it, and your own §4.2 quote is the proof

You propose "pronouns and temporal references only, no new content words."

INJ-2's `appointment` pattern (`injection_contract.py:224`):

```
\b(appointments?|appt|scheduled?|visits?|meetings?|when|...)\b
```

and `schedule` (`:217`):

```
\b(schedules?|appointments?|meetings?|when|time|calendar|...)\b
```

**`when`, `scheduled`, `time`, `calendar`, `upcoming` are temporal references *and* admission keywords.** A resolver restricted to temporal references can emit precisely the tokens that trip INJ-2. The constraint isn't a partial mitigation for these attributes — it's no mitigation at all, because the permitted vocabulary and the admission vocabulary overlap by construction.

This is the strongest thing I can say about the document: **the proposed defence is refuted by a regex you quoted three pages earlier.** You were right to flag question 4 as the most serious objection; you were wrong that a grammar restriction answers it.

The obvious repair — require `admitted(resolved) ⊆ admitted(raw)` — is worse than useless: "What about 8am?" admits nothing, so the subset rule makes the resolved set empty and the feature does nothing. **Any input-side or output-side constraint on a query-rewriting resolver either fails to close the hole or closes the feature.** That's the real result, and it kills the query-rewriting shape rather than repairing it.

## 4. What you're not seeing — §5's central claimed property is false

§5 claims: *"No fact crosses a turn boundary."*

Your own worked example is `"What about 8am on the 12th, regarding the appointment conflict?"` — **"the 12th" and "appointment conflict" came from facts.** The resolved query is a derived artifact of governed facts. And:

- The record writes it: `"query": query` (`epistemic_record.py:263`).
- TD-030's strip set is `{value, from_value, to_value, old_value, new_value, ciphertext, ct}` (`:77`). **`query` is not in it** — and the same set governs the ledger (`epistemic_ledger.py:78`).

Today that's sound, because query text is *user-authored* and therefore contains only what the speaker already knew. **A resolver silently changes the provenance of that field from user-authored to machine-authored-from-facts**, and every downstream component that treats `query` as safe-by-construction was built on the old assumption. So the fact value crosses the turn boundary into the per-turn record and the append-only ledger, through a field explicitly designed on the premise that it couldn't carry one.

Two consequences you'd inherit: the resolved query becomes a derived artifact under R18 with no `derived_from` lineage; and it lands in the HEL, which is append-only — a fact value written there is not retractable by ordinary means, only by crypto-shred of the whole member payload.

**This, not the injection risk, is the finding I'd lead with.** The injection risk is a design problem you can iterate on. This one silently invalidates an invariant that three other subsystems already depend on.

## 5. The shape that survives all of the above — carry IDs, not text

Don't resolve into a query string. Resolve into **referents**, and re-govern them.

The substrate already exists: your per-turn record holds the admitted **fact IDs**. So:

- The resolver reads prior *records* (IDs, subjects, timestamps) — never answer text, never fact values. Question 1 answered: it reads structure, not prose.
- Its output is a candidate referent set — fact IDs — not a rewritten string.
- Turn N+1's admitted set is bounded by `admissible(raw query, current requester) ∪ {ids from prior turns that pass the full contract for THIS requester}`.

What that buys, precisely:

- **No cross-member leak, and multi-party anaphora still works.** Bill says "what about her appointment," it resolves to Maya's fact ID, INJ-3 denies it for requester=Bill. The reference resolved correctly *and* was refused — and the record can say so. That is strictly better than both current behaviour and naive history, and it dissolves the forced choice in §1.
- **The resolver can be wrong but cannot be unsafe.** Worst case it points at the wrong already-in-conversation fact — a correctness bug, bounded by a set that was already legitimately admitted to someone, with every member re-checked against the current speaker. That's the property to design toward, and I'd state it as the acceptance criterion.
- **Nothing fact-derived enters the query string**, so §4 finding stands closed and `query` keeps its provenance.
- It's the honest reading of "models propose, only the core commits" — the resolver proposes *identifiers*, the contract commits.

Question 3 answered: yes, the record must carry the referent binding, or it misdescribes what was governed. Question 5 answered: an empty or ambiguous referent set routes into INJ-6's existing empty-set-guard machinery — you already have deterministic refusal for "nothing admitted"; don't build a second mechanism for "nothing resolved."

## 6. Your question 4 is your best one, and the answer is yes

> *One reading is that the gap is not "no memory" but "no way to signal an unresolved reference."*

Correct, and I'd act on it before anything in §5. A detector needs no model, no rewriting, and no new attack surface: closed-list anaphor in the query **AND** (zero facts admitted **OR** intent below threshold) → deterministic refusal. That converts your §3 failure — a confident wrong answer, invisible in the record — into a loud honest one, which is the whole of the damage you described.

It is also a **strict subset** of the resolver's machinery: the detector *is* the resolver's failure branch. Ship it first and the resolver stops being a risky rewrite and becomes an optimisation over an already-safe floor. If you build only one thing this quarter, build this.

## 7. Prior art — question 3, answered honestly

I can point to the right analogue but not to a canonical design, and I'd rather say so than manufacture a citation.

The closest well-studied problem is **query rewriting under ACL-filtered retrieval**, where the settled result matches your instinct: rewriting must precede the authorization filter and the filter must be re-applied to the rewritten query. Your §5 shape is that pattern, and the known failure mode in that literature is precisely the rewrite-to-widen attack in question 4. Contextual integrity (Nissenbaum) — already in your stack — gives the vocabulary for why multi-party carry-forward is a norm violation rather than a bug.

What I **cannot** point you to is a validated multi-party, per-turn-authorized dialogue design. I don't believe one exists in a form you could adopt, and I'd treat any confident citation of one — from me or anyone — with suspicion. The reference-resolution literature overwhelmingly assumes a single authorized user.

---

## Two things to add to your list

**There is no conversation boundary at all.** `session_id` is a *fixed string per member* — not per conversation. Every turn bill has ever taken shares one identifier. So any memory design must first invent a session boundary and a TTL, and none of your candidates mentions one. "What about 8am?" would resolve against a referent from three weeks ago. This also walks directly into R21 (calculable expiry, **NOT MET**): you'd be introducing new carried state with no retention policy, in a system whose ceiling work says durable writes require one.

**The disclosure gate's hard early return creates referent holes.** A consent-gate turn produces no answer and no admitted facts — so it contributes no referents. "Yes, go ahead" works because it's purpose-built; "what about that?" after a gate turn has nothing to bind to. Whatever the resolver does there, decide it deliberately rather than discovering it.

---

Two corrections to my own framing, for the record: §4.2 is a real risk under the string-concatenation implementation — I'm saying it isn't *intrinsic*, not that it's wrong. And my §5 alternative is a design sketch, not a verified one; the ID-carrying claim about your record substrate is verified, the security argument built on it is mine and should be attacked the same way I attacked yours.
