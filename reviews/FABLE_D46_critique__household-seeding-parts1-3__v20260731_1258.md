# FABLE_D46_critique — Household Seeding Roadmap, Parts 1–3

Reviewer: Fable
Dispatch: D-46
Scope: Parts 1–3 only (confirmation subroutine, seeding/onboarding, boundary
manager). Parts 4 (safety layer) and 5 (cross-cutting constraint) deliberately
NOT critiqued — reviewed separately — except where Parts 1–3 depend on them.
Doc-Reviewed: `docs/design/HIP_HouseholdSeeding_Roadmap__v20260730_1936.md`
(version v20260730_1936 — the LATEST at review time, per the
`LATEST_HIP_HouseholdSeeding_Roadmap.md` symlink and the docs/INDEX.md row;
NOT the earlier v20260730_1645, which an earlier D-46 pass reviewed)
Version: v20260731_1258 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED
Date: 2026-07-31
Repo state at review: HEAD 4172cc8, branch roadmap

**This document is the critique verbatim as produced, banked unedited.** It is
not summarized and not softened. Findings are the reviewer's claims; per the
`docs/reviews/` convention they are UNVERIFIED by any separate dispatch unless
one says otherwise, and this review proposes no REQ status. Claims marked
`[code-verified]` were checked against the repo at HEAD during the review pass
itself.

Timestamp note, kept so the record shows both: this file was first written under
D-54 with a **UTC** stamp (`v20260731_1858`, i.e. 1858Z) as that dispatch
directed, which deviated from the CLAUDE.md Naming Law's Mountain Time
convention and would have sorted this document ~6 hours out of order against
every other doc in the repo. D-55 corrected it by `git mv` to the equivalent
**Mountain Time** stamp — `v20260731_1258` — which is the canonical name.
**1258 MDT = 1858 UTC; same moment, same document.** The critique body was not
touched by the rename.

---

# D-46 (re-run) — Fable critique of HIP_HouseholdSeeding_Roadmap **v20260730_1936**, Parts 1–3

Gate: PASSED (bill-ai / [REDACTED-MACHINE-NAME] / ~/hip-roadmap / roadmap), HEAD 4172cc8.
Read-only. No lock taken. No design changed. No status proposed.
Parts 4 and 5 skipped per dispatch, except where Parts 1–3 depend on them.

**This reviews `_1936`, not the `_1645` I critiqued earlier.** That matters: D-47/D-48
revised the doc substantially in response to the earlier pass (30KB → 55KB), and
several findings are genuinely fixed. Restating them would be worse than useless. What
follows separates *fixed*, *survives*, and *newly introduced by the revision*.

Claims marked **[code-verified]** were re-checked against HEAD this session, not
carried over.

---

## WHAT THE REVISION ACTUALLY FIXED — credit where it is due

These are real fixes, not cosmetic re-wordings:

- **"Never dead-ends" → "degrades to durable-pending" + a named stranding case**
  (`:96-117`). The unconditional promise is gone, replaced by an honest terminal state
  that the design must *tolerate* rather than eliminate. This is the right shape and
  it is stated without softening.
- **Justification-based trust storage** (`:199-231`), TMS/AGM-style — the rung becomes
  a computed view over stored justifications. Correct representational commitment, and
  the economy-of-mechanism argument for it is sound.
- **The self-certifying test is gone**, replaced by a five-part evaluation portfolio
  (`:478-528`): pre-registered observable, canary metrics forbidden as optimization
  targets, exposure-corrected behavioral outcomes, a held-out arm, and sampled human
  adjudication against an externally-written rubric. This is better than what I
  recommended — the canary-as-tripwire-not-target distinction in (b) is a genuine
  addition.
- **Named house rule: evaluator ≠ optimizer** (`:530-549`), grounded in two real
  incidents from this codebase rather than hypotheticals. Exactly right.
- **Withdrawal-recovery rule** (`:579-587`): cooling-off, oblique re-entry, never above
  the depth where withdrawal occurred. This closes the "no re-approach criterion" gap,
  and the at-or-below-depth clause is the part that matters most — it prevents a
  withdrawal from being used as a new floor.
- **Absolute depth ceiling** (`:588-597`), enforced independently of engagement.
- **Withdrawal detection marked OPEN** (`:551-568`) with explicit FP/FN framing rather
  than shipping a plausible heuristic.
- **Custodian bottleneck flagged** as an open implementation concern (`:380-396`).
- **MINIMUM SEED err-low asymmetry** (`:344-354`) — a substantive argument, not a
  restatement.
- **Two-tier expert gate** (BUILD-BLOCKING vs ADVISORY, `:809-842`), with the loosening
  called out as deliberate.

Part 3 went from the weakest section to the strongest. I want that on the record before
the findings below.

---

## FINDING 1 — THE CORROBORATED WIRING IS UNCHANGED, AND NOW CONTRADICTS THREE RATIFIED ARTIFACTS

**Severity: BLOCKING. This is a governance problem now, not just a design bug.**

`:175-183` still reads:

> "**Household agreement → `CORROBORATED`.** When a second household member
> independently affirms a fact already at `CONFIRMED` … it is promoted to
> `CORROBORATED`. This roadmap does not change what `CORROBORATED` means…"

And `:296-298` still builds Zone 2 around producing "`CORROBORATED` promotions."

**[code-verified] at HEAD** — `memory_engine/trust.py:70-78` is unchanged:

```python
    if confirmed_by is not None:
        return "CONFIRMED"
    if confidence == "high" and _has_harden_transition(confidence_log or []):
        return "CORROBORATED"
```

First-match-wins. A fact at CONFIRMED *has* `confirmed_by` set — that is what makes it
CONFIRMED — so the branch is shadowed and the promotion cannot fire for any input.
(D-51 proved this exhaustively: 144 input combinations, `CORROBORATED` returned 4
times, **zero** with `confirmed_by` set.)

**What is new since `_1645` is that this is no longer just wrong — it now contradicts
the project's own downstream rulings:**

1. **D-50's `HIP_ConfirmationModel_PortraitRethink` Principle 3** says it directly:
   the roadmap's version "is a demotion, not a promotion, and is additionally
   **structurally unreachable**."
2. **D-52/D-53 filed `REQ_ATTESTED`** on Bill's ruling that `CORROBORATED` **keeps** its
   reconciliation-hardening meaning and social attestation gets a **new** rung name —
   precisely so the name is not reused.
3. `REQ_TRUST_AXES__record-both-rank-neither` (PLAN) is built on the same ruling.

So the LATEST design roadmap now instructs a builder to do the exact thing two filed
REQs forbid. In a repo whose whole discipline is that documents must not disagree about
ratified state, this is the highest-priority item in the document — and it is a
two-paragraph edit, not a redesign.

---

## FINDING 2 — THE REVISION INTRODUCED A NEW CONTRADICTION WITH BILL'S "RANK NEITHER" RULING

**Severity: HIGH. Introduced by the fix, not present in `_1645`.**

The new justification-storage section lists its first benefit as (`:215-218`):

> "**Trust-ordering.** Comparing two facts' relative confidence becomes a query over
> their justification structures, not a hand-maintained rung-comparison table…"

But Bill ruled (D-53, after external evaluation) **against a ranking axis**: the system
records both signals and **ranks neither**; the consumer weighs them in context.
"Comparing two facts' relative confidence" is a comparator — it is the ranking the
ruling removed, relocated from a table into a query.

The underlying storage commitment is fine and compatible. The *stated benefit* is not.
This needs one sentence reconciling it: justifications make the inputs to a
context-specific judgment *available*, they do not license the system to compute a
relative-confidence verdict of its own.

Worth noting the sequence — the doc was revised (D-48, 19:36) before the ruling
(D-53). This is drift from a later decision, not an error at time of writing. But
`_1936` is the LATEST and reads as current.

---

## FINDING 3 — "SENSITIVITY GATES DEPTH" IS NOW A SELF-CONTRADICTION, AND STILL SITS ON TWO BROKEN ENCODINGS

**Severity: HIGH. Worse than in `_1645`, because the revision raised the standard it fails.**

Part 3 now **explicitly names contextual integrity as its framework** (`:414-430`):
privacy as appropriate flow relative to context norms. Sixty lines later (`:470-476`) it
keeps sensitivity as a **static per-attribute scalar** (`low/medium/high/critical`).

Those are incompatible, and it is CI's central claim that makes them so. Martin &
Nissenbaum's 2016 empirical test found that **once context is controlled for, the
sensitivity of the data type largely loses explanatory power**. The doc now cites the
framework that refutes its own mechanism, and cites it as the section's foundation.
Every other Part 3 principle (earn depth, follow engagement, back off) is
relationship- and context-dependent; sensitivity is the one context-blind input, and
it is the one gating the others.

**[code-verified] at HEAD — both encodings still misrank the most sensitive class:**

```
harness/extraction_queue.py:95   SENSITIVITY_LEVELS = ("low","medium","high","critical")   # 4-valued
harness/curator_shadow.py:95     _ORDINAL = {"high":1.0,"medium":0.5,"low":0.0}
                                 # "critical" misses -> 0.5 default -> ranks BELOW "high"
harness/hipconfig.py:30          SENSITIVITY_RANK = {"low":1,"medium":2,"high":3}
                                 # .get(tag,0) -> "critical" -> 0 -> ranks BELOW "low"
```

Unchanged since the earlier pass. If the Boundary Manager consumes either — and the
doc says sensitivity is "an input the Boundary Manager gives the subroutine" — the
`critical` class gates depth *least*. Any Part 3 spec must declare which encoding is
authoritative and fix it before building a consent control on it.

---

## FINDING 4 — SELF-HEALING vs. NEVER-RE-ASK: THE CONTRADICTION SURVIVES, ONE FIELD FROM BEING FIXED

**Severity: MEDIUM-HIGH. The justification fix nearly resolved it and did not.**

The self-healing bullet (`:118-127`) is **verbatim unchanged**: awaiting-confirmation
state must be re-derivable from "the trust ladder rung, the fact's
`confirmed_by`/`write_state`, the roster of eligible confirmers" — not a side-channel
flag. And `next_confirmable` (`:149-153`) must "never re-surface a fact the confirmer
has already declined within some backoff window."

A decline changes **none** of those three sources. The fact stays at its rung with
`confirmed_by` unset — byte-identical to a fact nobody has ever been asked about. So
either the system re-asks immediately (violating never-re-ask, and "never force"), or
it keeps the forbidden flag.

**The new justification model is one field away from closing this.** `:204-205` stores
"who said this, who confirmed it (if anyone), and what else backs it" — a decline is
none of those. If a justification record also carried *who was asked and declined, and
when*, backoff becomes re-derivable from stored state and both requirements hold
simultaneously. That is a small addition to a schema the doc already says is open
(`:242-246`), and it would make the self-healing claim true rather than aspirational.

---

## FINDING 5 — DEPTH RUNAWAY IS BOUNDED BUT NOT DECOUPLED, AND THE CANARY IS BLIND TO THE POPULATION IT MOST NEEDS TO CATCH

**Severity: HIGH. This is the finding I would most want acted on after Finding 1.**

The absolute ceiling (`:588-597`) is a real fix — it bounds the loop. But the loop
itself is untouched:

- Confirmation and depth-seeking remain **"the same mechanism running in two
  directions"** (`:131`), one decision, one queue.
- "More confirmed facts already on record" remains an explicit depth-earning criterion
  (`:436-437`).

So: confirming earns depth → depth elicits facts → facts need confirming → earns more
depth, now running up against a ceiling instead of running away. The two activities
still have opposite consent polarities — confirmation asks about what was already
volunteered; elicitation expands the collected set — and merging them means trust
earned cheaply is spent expensively.

**The sharper problem is that the new canary metrics cannot see the failure mode.**
Portfolio item (b) tracks **withdrawal rate, decline rate, disengagement rate**. Every
one of those requires the household to emit a *negative* signal. The population most at
risk from unbounded deepening — the agreeable, the socially compliant, the lonely, the
cognitively declining — emits none of them. They engage *more*, which under "follow
engagement" (`:441-446`) earns depth *faster*, and they trip no canary because they
never withdraw.

The tripwire is structurally blind to exactly the case it exists to catch. A canary
that only fires for users who push back is not protecting the users who don't.

Two additions would close it, neither large: a canary that does **not** depend on a
negative signal (e.g. depth-per-session slope, or absolute disclosure volume relative
to cohort), and decoupling the confirmation queue from the elicitation queue so earned
trust is not fungible across them.

---

## FINDING 6 — PART 2: WHAT SURVIVES

**6a. The custodian rationale is still empirically backwards.** The revision
acknowledges the **queue** (`:380-396`) but retains the reasoning (`:189-192`): "a
custodian who could bulk-confirm a dependent's entire profile in one tap is a custodian
who never actually reviewed most of it."

Past a modest N the consent-fatigue and warning-habituation literature is consistent
in the opposite direction: repeated individually-low-stakes confirmations train
automaticity, and attention *per item* declines with count. A custodian facing 60
sequential confirmations is less attentive by item 15, not 60× more attentive.

This matters because the doc frames the bottleneck as a **UX pacing** problem ("whether
the answer is pacing the queue across many sessions…"). It is an **efficacy** problem:
the friction may produce *less* review than a well-designed risk-tiered alternative
(batch the low-sensitivity bulk with per-item opt-out; force genuine individual
attention only on high/critical). Pacing a queue that does not produce attention just
spreads the same non-attention over more sessions.

Still unaddressed: what happens to a dependent's fact the custodian *declines* to
confirm. The dependent cannot self-confirm — that is the premise — so it strands. That
is now at least an honest state (durable-pending), which is an improvement.

**6b. MINIMUM SEED's denominator is still undefined.** "Measured on CONFIRMED coverage"
(`:340-343`) — coverage is a ratio, and the denominator is the set of facts the
household has not told you about yet, which is unknowable. The err-low argument
(`:344-354`) is good reasoning about *where to set a number* but cannot rescue a metric
that has no denominator. If it is instead an absolute count, the doc's own anti-gaming
goal fails in the other direction (100 confirmed pet facts clear a bar that 10 confirmed
care facts do not).

**6c. Seeding as designed cannot ship, and the doc does not say so plainly.** The
narrator-describes-others mechanic *is* Part 4 item 1 (disclosure about another adult),
now placed in **ADVISORY** (`:826`). ADVISORY explicitly means "none of them should
reach real users ahead of that review" (`:839`). Zone 2 is entirely
narrator-describes-others. So Part 2's core mechanic is in a category that cannot reach
users — which may well be the right call, but the doc presents Part 2 as buildable
without noting that its central flow is gated. The two-tier split is an improvement; it
just needs the consequence stated where Part 2 is read.

**6d. "High-value first" is still contradicted by the doc's own ordering.** Zone 3
(care) is described as "the material the rest of HIP is actually built to help with"
(`:299-302`) — the highest-value zone — and placed third. The operative principle is
**low-sensitivity first**, which is a different and defensible principle. The doc
conflates low-friction, low-sensitivity, and high-value and uses them interchangeably.

---

## FINDING 7 — THE RESEARCH-GROUNDING APPENDIX MISDESCRIBES WHAT THE REVIEWS FOUND

**Severity: MEDIUM, but it is the finding with the longest half-life, because it
misrepresents the review record itself.**

The section opens (`:848-854`):

> "external review — the Fable review (D-46, parts 1-3), a separate ChatGPT research
> review, and the additional research passes behind this revision (D-48) — has
> **repeatedly confirmed that its design choices land inside established, named bodies
> of work rather than reinventing untested territory**."

As the author of the D-46 review being cited: **that is not what it found.** It found
the design *reinvented* progressive profiling without citing it, *misappropriated*
motivational interviewing, *mis-stated* the funnel technique's purpose, and *omitted*
the one citation most relevant to Zone 1. Recasting a critique as confirmation is a
distortion of the record, and in a repo that banks reviews verbatim precisely so
claims can be checked against sources, it is the kind of drift worth catching early.
The banked artifact (`docs/reviews/FABLE_D46_seeding-critique.md`) contradicts the
characterization.

Specific problems that survive in the appendix itself:

- **Motivational interviewing (`:860-863`) is still misappropriated.** MI's reflective
  listening serves the *client's* own articulated goal; its ethics depend on that
  alignment, and MI explicitly warns against the "righting reflex" — steering toward an
  outcome the client did not choose. Repurposing the technique to lower resistance to
  disclosure *for the system's data needs* keeps the form and inverts the frame. The
  appendix repeats the borrowing without engaging the objection.
- **Foot-in-the-door is absent** — and it is the single most relevant citation for
  Zone 1's "bank several easy `CONFIRMED` facts before any harder ground is touched"
  (Freedman & Fraser 1966). Its absence is conspicuous in a section added specifically
  to ground this design, because it is the citation that raises an ethical question
  about a document whose first principle is "never force." Name it and defend it, or
  reorder the zones.
- **Funnel technique (`:864-867`) is cited for the wrong property.** The doc claims the
  ordering is "research-validated" for friction reduction (`:287-289`). The funnel's
  documented purpose is reducing order/priming effects and protecting response rates on
  later items. The shape is right; the stated warrant is not.
- **Active learning (`:873-878`) is cited without its pathologies.** Two land directly
  on this design: **oracle fatigue** — which is Finding 6a's custodian queue, arriving
  from a literature the doc already cites — and **uncertainty-sampling bias**, which
  preferentially surfaces the most anomalous items and fights "low-friction first" head
  on. A grounding section that names the technique and omits its known failure modes is
  doing half the job.
- **Trauma-informed design and crisis-response (`:879-888`) are asserted, not
  grounded** — no framework named. SAMHSA's six principles would be the citation for
  the first.

**Correcting my own earlier flag:** the provenance note at `:12-24` says no captured
artifact for the research passes exists. **That is now stale — [code-verified]**
`docs/reviews/` contains `CHATGPT_research-pass1.txt`, `-pass2-selfcertifying.txt`,
`-pass3-trust-axis-evaluation.txt`, and `FABLE_D46_seeding-critique.md`. D-49 banked
them. The flag can be retired on the next revision, and I withdraw the equivalent
concern I raised in D-53.

---

## FINDING 8 — SMALLER, BUT CONCRETE

- **`eligible_confirmers` still derives nothing today. [code-verified]** All five rows
  in the live registry have `household_id = NULL` (`bill`, `maya`, `sam`, `p4smoke_x`,
  `p4smoke_y`), and `dyads` still has no member columns (`dyad_id, recipient_ref,
  household_id, dyad_pubkey, status, created_at`). Under the doc's own mandate to derive
  confirmers from server-authoritative state, essentially **every member-owned fact
  lands in durable-pending on day one**. The new durable-pending framing makes this
  honest — but it also makes a live blocking defect look like a designed state. The doc
  should name it as a current blocker, not let the terminal state absorb it.
- **Part 1 / Part 3 separation is still circular** (`:599-610`). The Boundary Manager
  maintains the ceiling; Part 1 consults it; but the engagement signal that *sets* the
  ceiling comes from confirmation outcomes Part 1 produces. Ceiling → what is surfaced →
  outcomes → engagement → ceiling. The claim of "independently-tunable" is false, and
  the cited injection-contract precedent does not apply — that one is genuinely
  one-directional.
- **The stranding case does not quite cover third-party subjects.** `:108-117` names
  estranged/deceased/never-a-customer/dependent-without-custodian. A fact whose subject
  is not a household member at all (a neighbour, a member's doctor) has no authorized
  confirmer *by construction*, not by unavailability. Substantially absorbed by
  durable-pending; worth a clause.

---

## WHAT I WOULD FIX, IN ORDER

1. **Finding 1** — align the CORROBORATED wiring with `REQ_ATTESTED` and D-50
   Principle 3. Two paragraphs. It is currently instructing a build that two filed REQs
   forbid.
2. **Finding 5** — add a canary that does not depend on a negative signal, and decouple
   the confirmation and elicitation queues.
3. **Finding 3** — declare the authoritative sensitivity encoding, fix `critical`, and
   reconcile a static scalar with the CI framework Part 3 now claims.
4. **Finding 4** — add declines to the justification record; it makes self-healing true.
5. **Finding 7** — correct the appendix's opening characterization, add foot-in-the-door,
   and add active learning's failure modes.

No design changed, no lock taken, no status proposed. Parts 4 and 5 not critiqued.

---

## CORRECTIONS

Corrections the reviewer made to their own claims, carried here so the banked
artifact does not preserve a withdrawn concern as though it still stood. Both
were issued before this document was banked; neither was prompted by a
challenge to the finding.

**1. WITHDRAWN — the concern that the research passes behind the D-48 revision
were unbanked.**
The roadmap's own provenance note (`v20260730_1936:12-24`) states that no
captured artifact for the research passes it cites exists in `docs/reviews/` or
`docs/dispatches/`. At review time that note was **stale**, and the critique
verified so: `docs/reviews/` contains `CHATGPT_research-pass1.txt`,
`CHATGPT_research-pass2-selfcertifying.txt`,
`CHATGPT_research-pass3-trust-axis-evaluation.txt`, and
`FABLE_D46_seeding-critique.md`. D-49 banked them. The provenance gap the
roadmap flags for itself is closed; the flag can be retired on the roadmap's
next revision. This correction appears in Finding 7 of the critique above and is
restated here so it is not missed.

**2. WITHDRAWN — the equivalent flag raised in D-53.**
While filing `REQ_TRUST_AXES__record-both-rank-neither__v20260731_0827.md`
(D-53), the same reviewer flagged that the external evaluation cited for Bill's
"record both, rank neither" ruling — referred to in the dispatch as
*gptresearch3* — was **not banked** in `docs/reviews/`, and recorded that gap in
the REQ itself (OPEN item 4), in the D-53 INDEX row, and in the D-53 commit
message, on the reasoning that the ruling's basis was therefore unverifiable
from the repo.

That flag is **withdrawn**: `CHATGPT_research-pass3-trust-axis-evaluation.txt`
is present in `docs/reviews/` and is the artifact in question. The ruling's
basis IS verifiable from the repo.

**Consequence not yet actioned, named here rather than left implicit:** the
withdrawal is recorded in this banked review, but the three places the original
flag was written — `REQ_TRUST_AXES__record-both-rank-neither__v20260731_0827.md`
(OPEN item 4), its `docs/INDEX.md` row, and commit `88a3cb1`'s message — still
carry the flag as though it stood. The commit message is immutable and correctly
records what was known at the time; the REQ and the INDEX row are not, and
should be corrected under their own dispatch. D-54's scope is banking this
critique, so no edit to those was made here.
