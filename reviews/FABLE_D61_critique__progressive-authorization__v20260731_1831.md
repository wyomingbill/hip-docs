# FABLE_D61_critique — Progressive Authorization, Critiqued Against HIP

Reviewer: Fable
Dispatch: D-61
Subject: the pass-4 progressive-authorization answer
(`docs/reviews/CHATGPT_research-pass4-engagement-authorization.txt`) critiqued
against HIP specifically — its central claim that engagement may justify
OFFERING a deeper capability but must never itself AUTHORIZE deeper collection,
i.e. that "earn depth" becomes "earn the opportunity to request a scoped depth
grant."
Read against: `docs/design/HIP_HouseholdSeeding_Roadmap__v20260731_1351.md`
(LATEST at review time) and the HIP codebase at HEAD af9e5b0.
Version: v20260731_1831 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED
Verification: UNVERIFIED
Date: 2026-07-31

**Captured verbatim as produced, banked unedited.** Not summarized, not
softened. Findings are the reviewer's claims; per the `docs/reviews/`
convention they are UNVERIFIED by any separate dispatch unless one says
otherwise. **No REQ is proposed by this document, and it changes no design and
no status.** Claims marked `[code-verified]` were checked against the repo at
af9e5b0 during the review pass itself.

Related banked artifacts: the answer under critique is
`CHATGPT_research-pass4-engagement-authorization.txt`; the Finding 5 that
prompted it is stated in
`FABLE_D46_critique__household-seeding-parts1-3__v20260731_1258.md`.

---

# D-61 — Critique of the progressive-authorization answer, against HIP specifically

Gate: PASSED (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap / roadmap), HEAD af9e5b0.
Read-only. No lock. No design changed. No status proposed. Nothing banked.

Source under critique: `docs/reviews/CHATGPT_research-pass4-engagement-authorization.txt`
Read against: `docs/design/HIP_HouseholdSeeding_Roadmap__v20260731_1351.md` (LATEST) and the codebase at af9e5b0.
Claims marked **[code-verified]** were checked this session.

---

## (a) Does progressive authorization sever the Finding 5 loop, or relocate it?

**It severs one edge and relocates the rest — and the part doing the severing is not the part the answer emphasizes.**

Finding 5's loop: confirming earns depth → depth elicits facts → facts need confirming → earns more depth, braked only by withdrawal detection that compliant users never trigger.

The answer's **structural ceiling** (architecture item 1: "Engagement cannot raise this ceiling") genuinely cuts the loop, at the exact point where accumulation converts into permission. That is the load-bearing element.

The **grant machinery relocates it.** Who issues the scoped grant? The same acquiescent user. The loop becomes: engagement → more offers → grants approved → more collection → more engagement. The answer's own diagnosis says the compliant user cannot be detected, so nothing stops that user from approving every grant. You have moved from *engagement authorizes* to *engagement generates authorization requests that the compliant user rubber-stamps* — slower, better-documented, same destination.

**The sharpest internal inconsistency:** "Engagement may trigger an offer, never authorization" leaves **offer rate entirely ungoverned**, while the answer's own §6 gaming list names offer-sequencing as an attack ("ask several easy questions before a sensitive one"). Repeated asking is itself a pressure vector — that is foot-in-the-door and reactance, both of which the surrounding literature it cites would predict. An offer/authorize split without an offer-rate cap is not a control; it is a relabelling.

Teach-back and decision-specific safeguards are a **quality** gate on each grant. Nothing in the proposal is a **rate** limit on grant-seeking. Those are different failures and it only fixes one.

**Verdict:** adopt the ceiling. Treat the grant machinery as necessary but insufficient, and add what the answer omits — a bound on how often the system may ask for a grant at all.

---

## (b) What HIP already has

**Real and built — these are assets, not gaps:**

- **Parked claims / P8 confirmation gate. [code-verified]** `store.py:462` compares `TRUST_RANK[incoming] < TRUST_RANK[head]` on cross-principal supersede → `unresolved` → `confirmation_gate.register` → `apply_confirm` / `apply_decline`. This is already **a scoped, per-item, deliberate human authorization act with an explicit no-penalty decline path** — structurally the closest thing in the codebase to a depth grant. The answer would build on this, not replace it.
- **The trust ladder's `CONFIRMED` rung. [code-verified]** `trust.py:72` — `confirmed_by is not None` is the sole route to CONFIRMED. HIP already encodes "authorization is a human act, never an inference." That is the answer's central principle, already ratified, one level down.
- **The epistemic ledger (HEL). [code-verified]** `harness/epistemic_ledger.py` — hash-chained, `prev_hash`/`payload_sha256`, append-only, AES-256-GCM per-member payloads. This **already satisfies** the answer's control item 5, "maintain immutable event-level logs of prompts, alternatives, disclosures, authorizations, inferences and withdrawals." HIP has the immutable audit substrate the answer asks for. (It also creates the revocation conflict — see e2.)
- **Derived facts cannot self-promote. [code-verified]** `consolidate.py:435` — derived facts are "always confidence='low', tier='hot', derived=True. They can only harden to 'medium' via human confirmation." HIP already implements the answer's "treat inferred data as collected data" in its strongest form: inference cannot raise its own trust.

**Design-only — cannot be credited yet:**

- **Confirmation Subroutine** — Part 1 is pre-spec; no code exists.
- **Justification storage** — Part 1's TMS section is a representational commitment, unbuilt. Partial primitives exist (`confidence_log`, `derived_from`).

**Present but on the wrong axis:**

- **The injection contract** is HIP's strongest control and it is a **read-side** gate (INJ-1..7: who may *see* an admitted fact). Progressive authorization is a **collection-side** problem. The injection contract does nothing to limit what is asked or written. This is worth stating plainly because it is easy to assume HIP's rigor here transfers; it does not.

**Present but broken:**

- **Sensitivity classification. [code-verified]** The answer's decision-specific safeguards key off exactly the categories HIP labels (`low/medium/high/critical`, `extraction_queue.py:95`), but both encodings still misrank `critical` — `curator_shadow.py:95` drops it to a 0.5 default *below* `high`; `hipconfig.py:30` drops it to 0 *below* `low`. Any grant tier keyed on sensitivity inherits that today.

---

## (c) What would have to be rebuilt, and which Part 3 passages die

**Dies outright — "Follow engagement"** (`:513` block): *"A household that engages eagerly may earn depth faster."* This is the precise sentence the answer's central claim forbids. There is no reading under which it survives.

**Dies as written — "Earn depth, don't take it":** the clause *"must be justified by the household's own prior engagement — more time in the relationship, more confirmed facts already on record, more instances of the household volunteering detail unprompted."* All three named justifications become impermissible. The principle **inverts**: engagement justifies nothing about depth; at most it justifies *offering*. The name "earn depth" survives only if redefined to "earn the opportunity to ask for a grant" — which is the answer's own reframing and is a different principle wearing the old label.

**Promoted, not killed — the absolute depth ceiling** (`:651` block). It goes from backstop ("a backstop against 'earn depth' being read as unbounded") to **primary mechanism**. Its value, currently unset, becomes the single most consequential number in Part 3 rather than a safety net.

**Survives with changed meaning — the withdrawal-recovery rule.** Currently governs re-approach after withdrawal. Under grants it governs re-*offer*, and it needs the offer-rate cap identified in (a), which it does not have.

**Survives, demoted — the evaluation portfolio.** Mostly intact, but its canaries move from "how we know depth is serving the family" to "pause triggers only," per the answer's rule that safety metrics may pause but never unlock. Portfolio item (c), behavioral outcomes with exposure correction, loses its role as justification for depth.

**Dies in Part 1, not Part 3, and this is the one the dispatch did not name:** Part 1's *"Confirmation and depth are the same mechanism running in two directions"* (`:131`-region), and the single-queue position in its open questions. Under progressive authorization these **must** separate: confirming an already-volunteered fact needs no grant; eliciting a new one does. One is free, the other is gated. A unified `next_confirmable`/`next_depth_question` queue cannot express that distinction, and Part 1 currently argues explicitly that they are one decision. That is the largest structural rebuild the answer implies, and it lands on the infrastructure part, not the policy part.

---

## (d) Are enthusiasm and compliance separable? Not from dialogue — but HIP's data is not only dialogue

**I agree with the claim as stated, and it is too strong for HIP's actual substrate.** Both halves matter.

**Where it holds:** from free conversational data alone, the latent states are not identifiable. Elaboration rate, answer length, warmth and unprompted disclosure are compatible with enthusiasm, loneliness, deference, impression management and impairment simultaneously. That is sound, it matches the measurement literature it cites, and it **invalidates the canary I proposed in Finding 5** — a depth-per-session-slope or disclosure-volume metric measures engagement, not consent validity, and the answer is right that I was reaching for a signal that does not carry the information.

**Where it is too strong:** HIP does not have only free dialogue. It has **structured decision outcomes with a genuine no-cost refusal**:

- `confirmation_gate.apply_decline` — a discrete, per-item refusal on a parked claim.
- `outcome.kind` ∈ {correction, override} — where `override` *is* `path == "control_decline"`, a member declining a proposed write.
- `confirmed_by` — a per-fact record of who authorized what.

The answer's own §5 table lists *"Refusal when refusal has no cost — evidence that 'no' is behaviorally available"* among the more useful signals, and its recommended fallback is **within-person counterfactual testing**. HIP already generates that signal structurally, per parked claim, without a cohort: does this member ever decline? does decline rate vary with sensitivity? do they decline when declining costs nothing? A pure conversational agent cannot ask those questions. HIP can.

**Three honest limits that stop this from being a solution:**

1. A member who never declines remains ambiguous — confident and compliant look identical, which is the answer's point surviving in narrower form.
2. **[code-verified]** the parked-claim sample is narrow and non-random: P8 park fires on *cross-principal supersede conflict*, not on a designed contrast. It is opportunistic evidence, not an instrument.
3. D-41 established the correction path was structurally dead until D-42 fixed it, so the historical decline data is thin and the corpus was single-class.

**Verdict:** the answer's claim defeats the free-dialogue canary and does **not** defeat within-person measurement over HIP's confirmation outcomes. That distinction is worth preserving, because it is the one place HIP has better material than the literature assumes — and the answer would have reached a different conclusion had it known the substrate.

---

## (e) The three unscoped items

### e1 — Inference as an end-run: **PARTIALLY HAS IT**, better than the answer assumes on one axis, absent on the other

**[code-verified]** HIP has a live inference producer: `memory_engine/consolidate.py` abstracts higher-order facts from episode clusters via `Interpreter.abstract()`, writing `derived: true` with `derived_from` provenance (`:525`).

**Strong where the answer worries most:** `:435` — derived facts are *"always confidence='low', tier='hot', derived=True. They can only harden to 'medium' via human confirmation."* Inference cannot promote itself. That is precisely "treat inferred data as collected data," already enforced.

**Absent where it also matters:** there is **no category control on what may be inferred**. `Interpreter.abstract()` is an LLM call over the member's own facts and nothing restricts the attribute space of its output. The answer's specific concern — inferring cognitive decline, addiction, finances, family conflict without asking — is unaddressed. HIP controls the *trust* of an inference, not its *subject matter*.

Also note `classify_trust_props` returns `DERIVED` as its **first** branch, so a derived fact is DERIVED regardless of anything else, and `TRUST_RANK["DERIVED"] = 0`. Inference is structurally marked and structurally bottom-ranked — good — but marking is not gating.

### e2 — Revocation propagation: **DOES NOT HAVE IT**, and the codebase says so in its own words

**[code-verified]** `retract_fact` (`extraction_queue.py:644`) sets `valid_to`, `closed_by='retracted'` — a **close, not a delete**. The row persists.

HIP already states the limit explicitly at `injection_contract.py:492-493`: revocation confers *"no new access, not unremembers"* — **"the same limit as every other revocation in this codebase."** That is a house-wide admission matching the answer's concern exactly, and it is more candid than the answer assumes.

**The cascade gap is real and live. [code-verified]** `derived_from` is written by consolidation and **never read for invalidation** — I checked every occurrence in `harness/` and `memory_engine/`. Retracting a source fact leaves its derived child standing. That is the answer's scenario verbatim: *"Deleting the original statement while retaining 'probable cognitive impairment' is not meaningful revocation."* It is not hypothetical here.

**One part may be unachievable rather than unbuilt.** The epistemic ledger is hash-chained and append-only by design. Erasure and tamper-evidence are structurally opposed, and HIP has already chosen tamper-evidence. The answer lists revocation propagation as a to-do; for HIP's ledger it is a **genuine tension requiring a ruling**, not a build task. Embeddings are a smaller question than the answer implies — consolidation writes `embedding: null` — but external stores exist (`mem0_store.py`, `zep_store.py`, `session_memory.py`, `speaker_id.py`) and what they retain is unscoped.

### e3 — Edge consent: **HAS THE OPPOSITE**, explicitly and by design

**[code-verified]** INJ-3's first PERMIT condition (`injection_contract.py:~470`): *"fact.owner == requester — owner reads any fact they stored (any subject)."*

The author of a claim about another person **always** retains read access to it. The subject does not enter the read path. This is exactly the answer's point — *"Speaker authorization is not subject authorization"* — and HIP currently resolves it entirely in the speaker's favour.

HIP has the *representation* (owner and subject are distinct fields throughout; D-50's portrait model treats claims as attributed and keeps both perspectives). What it lacks is any *policy* giving the subject a say over a claim someone else made about them. Unscoped, and it interacts with the seeding roadmap's narrator mechanic, where narrator-describes-others is the central Zone 2 flow.

---

## (f) Where the answer is wrong, overreaching, or importing constraints HIP does not have

**1. "No collection metric can unlock additional collection" is stated absolutely, and would forbid a pattern HIP has already shipped and ruled MET.** `REQ_CURATOR_SHADOW_SCORER`'s cold-start design is exactly a collection metric (≈100 outcome events) unlocking a capability (the trained regime). The answer states the *narrow* version once — *"Only explicit, purpose-specific authorization may increase sensitivity, retention, audience or inferential reach"* — and the *broad* version elsewhere. The narrow one is defensible; the broad one over-claims and would retroactively condemn a ratified HIP design. Adopt the narrow phrasing.

**2. The regulatory section imports a deployment HIP does not have.** GDPR Art. 9, DPIA obligations, the AI Act's exploitation prohibition, WA MHMD, CPRA/CPA — all assume a deployed, multi-tenant consumer service. HIP is a single-household prototype on operator-custodial hardware with no per-member device keys (Part 5's own constraint). "A DPIA would very likely be required" is not currently true. This is valuable forward-looking material presented as present exposure.

**3. It treats the elder as the paradigm user, and HIP's hardest case is a different one.** EASI, LFDSS, dementia assent — the whole vulnerability apparatus is elder-focused. HIP's household includes **dependents with custodians**, where the subject *cannot* grant at all. The custodian-grants model runs straight into the answer's own "what if the trusted caregiver is the threat," which it raises and then does not reconcile with its recommendation that caregiver authorization be "conflict-screened and narrowly scoped" — a phrase carrying no mechanism.

**4. Teach-back is recommended without costing it, in a voice-first system that has already discovered this failure mode.** Asking a user to restate what will be stored, who may access it and for how long — per sensitive category, by voice — is a heavy conversational burden. It collides with the roadmap's never-shame and low-friction commitments, and more pointedly with the **custodian-queue bottleneck already flagged in Part 2**. HIP has already learned that per-item friction at volume produces habituation rather than attention; teach-back per category risks reproducing exactly the failure the answer warns about elsewhere in its own text.

**5. The offer/authorize split is internally inconsistent** without an offer-rate cap — see (a).

**6. Minor:** it concedes the "computers as social actors" effect "has been challenged in newer work," then leans on relational-dependency arguments that need that effect to hold. Not fatal; worth noting before the dependency framing is built on.

**Where it is right, and HIP should take it:** the diagnosis itself — *acquiescence plus deferential vulnerability, with absence of dissent misread as authorization* — is correct, better-named than my Finding 5, and grounded in constructs (Kipnis, Belmont voluntariness, acquiescence response style) that HIP can cite. "Structural ceiling first, detection only as a brake" matches HIP's own fail-closed instincts everywhere else. And its control item 5 is already satisfied by the ledger.

---

## What I would put to Bill, in order

1. **Adopt the structural ceiling.** It is the part that actually severs the loop, it is already half-present as the absolute depth ceiling, and it needs a number.
2. **Add an offer-rate bound.** The answer omits it and its own gaming analysis requires it.
3. **Split Part 1's unified queue.** Confirmation and elicitation cannot share a queue under grant semantics. This is infrastructure, not policy, and it is the largest implied rebuild.
4. **Scope the `derived_from` cascade (e2).** Smallest concrete fix with a live defect behind it: retracting a source currently leaves its derived child standing.
5. **Rule on ledger-vs-erasure.** Not a build task — a genuine designed conflict needing a decision.
6. Do **not** adopt the broad "no collection metric may unlock collection" phrasing; take the narrow one.

Nothing banked. No design changed. No status proposed.
