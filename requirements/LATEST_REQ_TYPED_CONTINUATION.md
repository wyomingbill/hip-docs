# REQ_TYPED_CONTINUATION
Status: PLAN
Reconciled-Against: 2026-08-15. Pinned at **`0ee55fb`** (`~/hip-nc2` @ `nc-b0`) — the HEAD that
contains all three commits this REQ is grounded on: Episode substrate **`0c7b6ee`** (NC 22),
B1 **`41c130a`** (NC 20) with NC 25's classes (`bfb09df`) and NC 26's frame family (`0ee55fb`),
and the kernel's one-decision-point **`422d330`** (NC 24). Every `file:line` below was read at
`0ee55fb`, not remembered. *(NC 17's convention applies: the CONTRACT is the citation; line
numbers are re-verified by whichever build lands first.)*
Dispatch: **NC 29 — DOCS ONLY. No code was written, and none may be until B1/Episode
verification lands** (the ratified order; NC 28's adversarial verification is in flight).
Siblings: `REQ_UNRESOLVED_REFERENCE_DETECTOR` (B1, NC 17) · `REQ_CONVERSATION_EPISODE`
(NC 18) · `REQ_KERNEL_GOVERNED_TURN` (NC 13/15) · `REQ_VOICE_INTO_KERNEL` (NC 24).
**Neither this REQ nor its siblings restates the other's clauses** — the R-NC1-1
one-spec-per-behaviour rule, applied between siblings.

---

## THE REQUIREMENT

From the ratified acceptance design, verbatim:

> Draft REQ_TYPED_CONTINUATION (B2) from the ratified acceptance design: carry frame PATCH
> (target frame + changed slot), construct a NEW request, AUTHORIZE FROM ZERO — never
> reconstruct a natural-language query from history, never let prior turns carry authority.

### The five ratified clauses

1. **FRAME PATCH.** A continuation travels as a **typed patch** — a *target frame* plus the
   *changed slot* — never as prose.
2. **NEW REQUEST.** The patch is applied by **constructing a new request**, not by mutating
   the one that arrived and not by editing the episode in place.
3. **AUTHORIZE FROM ZERO.** The new request is authorized **as if it had never been
   preceded**. Every gate runs again, from nothing.
4. **NEVER RECONSTRUCT A NATURAL-LANGUAGE QUERY FROM HISTORY.** The continuation is not
   "what the member probably meant, written out".
5. **NEVER LET PRIOR TURNS CARRY AUTHORITY.** History supplies *what is being talked about*.
   It supplies nothing about *what may be done*.

### THE ONE SENTENCE

**B1 is the STOP when conversational state is missing. B2 is the RESOLUTION when it is
present — and the resolution must buy the member no authority they did not have this turn.**

---

## THE GAP THIS FILLS — measured at `0ee55fb`, not assumed

**B1 deliberately stands down the moment a prior turn exists.**
`harness/unresolved_reference.py:361-362`:

```python
if _has_prior_turn(window):
    return UnresolvedReference(False, notes=[*notes, "prior turn present in the window"])
```

So with a live Episode carrying turns, *"and the other one?"* is **`detected=False`** and
`governed_decision` returns `proceed=True` (`harness/kernel.py:429`). The utterance then
reaches the implementation **unchanged**, alongside `prompt_context`'s history
(`harness/conversation_episode.py:245`), and **the model is left to infer what "the other
one" refers to.**

**That inference is the whole exposure.** B1's own ruling history is the argument: NC 25's
ruling 1 moved the detector from phrases to structural classes precisely to keep model
judgement out of a governance-bearing decision. A continuation resolved by generation puts
that judgement back one line later — and this time it decides *which prior thing the member
is now acting on*, which is a strictly worse place for a guess than the one B1 removed it
from.

**B1 and B2 are complements, and their seam is two lines apart** in `governed_decision`
(`harness/kernel.py:403` detect, `:429` proceed). Neither may shadow the other, and a twin
must prove each fires on its own case and not the other's — the same shape B1's REQ requires
of B1 versus the store-down ruling (`REQ_UNRESOLVED_REFERENCE_DETECTOR` C3).

---

## THE ACCEPTANCE TEST

Each row passes or fails. No partial credit. Every mechanism that could fail silently carries
a **twin verified to go red** when the mechanism is removed.

### A. The patch is TYPED — clause 1

- **A1** a continuation produces a **`ContinuationPatch`**-shaped value carrying, at minimum:
  the **target frame's identity**, the **slot** being changed, and the **new slot value**.
  Asserted by construction, not by parsing a string.
- **A2** **no field of the patch is prose**, and none of them is the member's utterance. A
  patch whose "slot" is a sentence has re-implemented clause 4 in a struct.
- **A3** the patch's target is a frame that is **actually in the live episode** at decision
  time. A patch naming a frame the episode does not carry is a **refusal**, not a repair —
  and it must be distinguishable by value from B1's stop, not by reading the reply.
- **A4** **the patch never carries an authority field.** Enforced against the same
  `AUTHORITY_TOKENS` list the Episode types are checked against
  (`harness/conversation_episode.py:86`, exposed by `authority_fields()` at `:402`), so this
  REQ adds no second list that can drift from the first.

### B. A NEW request — clause 2

- **B1** the request that carries the continuation is a **new `TurnRequest`**
  (`harness/turn_request.py:100-115`). The arriving request is **not mutated** — it is frozen
  (`@dataclass(frozen=True)`), so this is provable by identity, and the twin asserts
  `new is not original`.
- **B2** the **episode is not edited to make the continuation work.** `working_frames` after a
  continuation contains what it contained plus this turn's own frame — no rewrite of the
  target, no back-dating. `record_turn_once` (`harness/conversation_episode.py:205`) stays the
  only writer of turn frames on this path.
- **B3** the new request's `session_id` and `episode` are the **same conversation**
  (`turn_request.py:106`, `:115`) — continuation is continuity, so it does not mint a second
  episode. Proven by `conversation_id` equality (`conversation_episode.py:155`).

### C. AUTHORIZE FROM ZERO — clauses 3 and 5, the security core

- **C1** the new request goes through **`governed_decision` again, in full**
  (`harness/kernel.py:353`). Not a subset, not a cached verdict, not a "we already decided
  this conversation was fine".
- **C2** **every existing gate re-runs and can still refuse**, proven one twin per gate at
  `0ee55fb`: store-down (`kernel.py:417`), household-dependence (`:143`), B1 itself (`:403`),
  ambiguous medical write (`:224`, class (b)), claim mismatch (`:257`). A continuation that
  becomes unrefusable because it is a continuation has failed this REQ outright.
- **C3** **the principal on the new request is THIS turn's principal.** Never the target
  frame's `speaker_label` (`conversation_episode.py:114`), which is ATTRIBUTION and is
  documented at `:100-102` as never authorising anything. **The twin: a continuation whose
  target frame is labelled with member X, arriving from member Y, resolves to Y — or refuses
  — and never to X.**
- **C4** **verification evidence is not inherited.** On the spoken path every turn needs fresh
  speaker evidence (the Episode charter's last sentence); a continuation is a turn.
  `TurnRequest.verification` (`turn_request.py:104`) on the new request is this turn's, or
  None — never the target frame's conversation-mates'.
- **C5** **consent and disclosure state are not inherited.** A continuation of a turn that had
  a permit does not have a permit.
- **C6** **NEGATIVE TWIN — the one that decides this REQ.** Take a conversation in which turn
  N was authorized and answered. Make turn N+1 a continuation of it, **with this turn's
  authority removed** (no principal / expired session / failing gate). **It must refuse.** If
  it answers, prior turns carried authority, and clause 5 is broken however good the rest
  looks.

### D. Noninterference and ANTI-VACUITY — the clause that keeps the product alive

- **D1** a turn that is **not** a continuation reaches the implementation **byte-identical** to
  the one that entered — the same equivalence shape NC 14 used per segment.
- **D2** the five `STANDALONE_EXAMPLES` (`unresolved_reference.py:200`) still answer and are
  never treated as continuations. **Short is not dependent, and it is not a continuation
  either.**
- **D3** a continuation the mechanism cannot resolve **holds the turn by asking** — B1's R3
  shape — and does **not** guess. One deterministic clarification, no answering model call
  while the target is unresolved.
- **D4** **B1 and B2 do not shadow each other** (C3-of-B1's shape): with **no** prior turn the
  utterance is B1's and B2 does not fire; with a prior turn present it is B2's and B1 does
  not fire. A twin proves each on its own case **and** on the other's.

### E. No model in the resolution path — clause 4

- **E1** on the continuation path, **zero answering model calls happen before the patch is
  built**, observed at `harness/model_calls.py:31/41` (`record()` / `counting()`), which NC 11
  wired at the two answering sites — the same instrument B1's A1 uses, not a second one.
- **E2** **the patch is never produced by generation.** The build may not resolve a target by
  asking a model which prior turn was meant; if the deterministic rule cannot decide, D3
  applies. **This is the clause most likely to be quietly violated by a "small" helper**, and
  the twin is a source-level assertion backed by a call counter, because a name check alone is
  a weak proxy (the defect `DISPATCH_A10_BATTERY` recorded).
- **E3** no natural-language query is reconstructed anywhere: the utterance that reaches the
  implementation on a continuation is **the member's own words plus a typed patch**, never a
  synthesised sentence.

### F. Modality parity

- **F1** the same continuation, arriving **typed** and **spoken**, produces the **same patch
  and the same decision** — the modality is a field (`turn_request.py:101`), never a different
  answer. B1's D3 rule, applied to B2.
- **F2** the spoken path inherits B2 with **no voice edit**, because the seam is
  `governed_decision`, which both modalities already cross since `422d330`.

### G. Audit

- **G1** every continuation records: the **target frame identity**, the **slot changed**, the
  **modality**, the **session id**, the **member**, and a **query hash** — **never the raw
  utterance**, matching `UnresolvedReference.record` (`unresolved_reference.py:213`) and
  `DisclosureRefusal.record` (`kernel.py:693`).
- **G2** the record is **derived from the decision object**, not built beside it — NC 14 S3's
  property, so a record cannot disagree with what was decided.

---

## INTEGRATION POINTS — CITED AT `0ee55fb`

| what | where | why it is the seam |
|---|---|---|
| **`governed_decision()`** | `harness/kernel.py:353` | **the insertion point**, immediately after B1's stand-down at `:403-413` and before the store-down gate at `:417`. One place, both modalities |
| B1's stand-down | `harness/unresolved_reference.py:361-362` | the exact line where B1 hands the turn on; B2 begins where this returns `False` for *"prior turn present"* |
| `TurnDecision` | `harness/kernel.py:279` | the stop/proceed carrier; already has `episode_id` `:296` and `notice` `:300`. A continuation refusal needs **no new mechanism** — only a new outcome |
| `TurnOutcome` | `harness/kernel.py:46` | add the continuation outcomes here, beside `REFUSED_UNRESOLVED_REFERENCE` `:58`, and register them in `REFUSALS` `:63` |
| `TurnResult` | `harness/kernel.py:71` | what callers receive; `model_called` `:82` is the observable that proves E1 |
| **`ConversationEpisode.working_frames`** | `harness/conversation_episode.py:162` | the frames a patch targets |
| **`WorkingFrame`** | `harness/conversation_episode.py:94`, fields `kind:111` `content:112` `at:113` `speaker_label:114` `speaker_side:120` `extractable:121` | **the blocking shape question — see below** |
| `FRAME_KINDS` | `harness/conversation_episode.py:79` | closed set; `__post_init__` `:123` refuses anything else |
| `AUTHORITY_TOKENS` / `authority_fields()` | `harness/conversation_episode.py:86` / `:402` | A4's checkable list — reused, never copied |
| `conversation_window()` | `harness/conversation_episode.py:235` | what B1 reads; B2 reads frames, not this projection |
| `TurnRequest` | `harness/turn_request.py:100-115`, incl. `episode:115` | frozen, so B1-of-this-REQ is provable by identity |
| `typed_request` / `spoken_request` | `harness/turn_request.py` adapters | F1's parity twins run on both |
| `text_turn` / `text_reply` / `voice_turn` | `harness/kernel.py:452` / `:459` / `:478` | the funnels; `text_reply` is where the notice is dropped (proposal 2) |
| `process_text_query` | `server/voice_orch.py:2819-2820` | the only typed consumer of `text_reply` |
| `model_calls` | `harness/model_calls.py:31`, `:41` | E1's instrument |

### ⚠ THE BLOCKING SHAPE QUESTION — `WorkingFrame` HAS NO SLOTS

**`WorkingFrame.content` is a `str` (`conversation_episode.py:112`).** There is nothing in the
Episode today for a patch to *target a slot of*. Bill's clause 1 says *"target frame + changed
slot"*, so **B2 requires a slotted frame**, and adding one is not a build detail:

* `FRAME_KINDS` is a **closed set** whose `__post_init__` says a new kind *"is a semantics
  question, not a label"* (`:123-127`);
* `WorkingFrame` is `frozen=True, slots=True` specifically so *"a frame cannot grow an
  authority attribute at runtime"* (`:97-98`);
* any slotted frame must pass `AUTHORITY_TOKENS` (`:86`).

**This REQ does not take that decision.** It is named here, at the seam, as the first thing
the B2 build must have ruled — see OPEN, item 1. Proceeding without it would let whoever
writes the first patch-target define the Episode's semantic vocabulary by default, which is
exactly the failure Q3's own deferral record exists to prevent.

---

## THE TWO DEFERRALS B2 NOW OWNS — RESOLVED AS DESIGN PROPOSALS FOR BILL

**Proposals, not rulings. A session never rules.** Each states what is proposed, why, what it
costs, and what would justify widening it later.

### PROPOSAL 1 — Q3, BRANCH SEMANTICS (NC 18 Q3; `REQ_CONVERSATION_EPISODE` §"Q3's DEFERRAL")

**The question as asked:** *"What creates a branch: explicit member cue, topic shift, or both?
Minimal viable definition ships first; widening is his call."*

**PROPOSED: EXPLICIT MEMBER CUE ONLY, for v1. Topic shift does NOT create a branch.**

**Why, in this project's own terms.** A topic-shift branch is a **classifier** decision. NC 25's
ruling 1 moved B1 from phrases to structural classes to keep model judgement out of a
governance-bearing decision — and a branch is *more* governance-bearing than a detection,
because `branch_info` is what B2 would use to **select which prior frame a continuation may
patch**. A wrong topic-shift branch does not merely mis-stop a turn; it silently points the
patch at the wrong conversation. **That is the same failure shape as Q4's silent re-binding of
a referent** — a wrong answer delivered with full confidence — arriving through a different
door.

**What `branch_info` may and may not do under this proposal:**

| may | may not |
|---|---|
| be **set** on an explicit member cue (*"going back to the pharmacy thing"*, *"about the other appointment"*) | be set by inference, topic model, embedding distance, or any model output |
| be **read by B2 to SELECT a patch target** | grant, extend, or imply any authority (C3-C5 apply to it unchanged) |
| be recorded in the audit fields (G1) | extend an episode's lifetime — the two clocks are `conversation_episode.py:48/50` and a branch touches neither |
| carry `parent_branch_id` for the record (`conversation_episode.py:141`) | change who is speaking, or what consent exists |

**The cost, stated:** a member who changes subject without saying so gets **no branch**, so a
later continuation resolves against the linear window and may be **held by D3** rather than
resolved. **Held, never mis-resolved** — the conservative direction, and the one this project
takes everywhere else.

**What would justify widening to topic shift:** a **measured** mis-selection and hold rate over
real conversations — the same evidentiary bar TD-V-025's floor was held to (*"the rule comes
from data or it does not come at all"*). Not a judgement that it feels too strict.

**Note on the deferral's own terms:** `REQ_CONVERSATION_EPISODE` says *"until B2 rules it,
`branch_info` is CARRIED AND NOT INTERPRETED … writing it is permitted; branching on it is
not."* **This proposal, if ruled, is what lifts that prohibition — and only as far as the
"may" column above.**

### PROPOSAL 2 — THE TYPED EPISODE-EXPIRY NOTICE (NC 24 §8 item 3)

**The residual as filed:** *"No typed route renders `notice`. A2.5 carries it to the boundary;
delivering it to a member on a typed surface is a user-visible route decision and is Bill's."*

**The drop site, cited:** `TurnResult.notice` is set (`harness/kernel.py:90`) and carried on
every exit of `governed_turn` (`:209`, `:260`, `:266`, `:269`, `:274`). Then
`text_reply` (`:459`) ends:

```python
return result.reply if result.reply is not None else ""
```

`harness/kernel.py:475` — **`notice` is dropped here**, and `server/voice_orch.py:2819-2820` is
the only typed consumer, so on the typed surface the notice reaches nobody.

**PROPOSED: PREPEND the deterministic notice to the reply as its own leading line, on EVERY
typed turn where `notice` is set — INCLUDING REFUSALS.**

**Why including refusals is the load-bearing half.** Q4's invariant is that the member is
**TOLD**. A notice delivered only on answered turns would go missing on exactly the turns where
the referent is most at risk: *"and the other one?"* after an expiry is a **B1 refusal**
(`kernel.py:405-413`) — the member is asked to clarify while never learning that the
conversation they were clarifying against has ended. **They would answer the clarification
against a conversation that no longer exists.**

**Properties this keeps:** the text is `EPISODE_EXPIRY_NOTICE`
(`conversation_episode.py:54`), **byte-identical, deterministic, no model** — the notice is a
mechanism, not phrasing, which is why that constant is fixed.

**The cost, stated rather than discovered later:** `text_reply`'s legacy contract is `str`, so
prepending **changes the reply string on expiry turns**. Any test asserting byte-equality on a
reply across an expiry boundary must be re-read — not edited to pass, re-read, because a test
that breaks here is reporting a real change in what the member sees.

**The alternative, considered and NOT proposed:** carry the notice as a separate structured
field for each route to render. Rejected for v1 because it is **the current state** — the
notice already exists as a typed field and no route renders it. A design whose delivery depends
on every future consumer remembering has already failed once here.

---

## WHAT'S ALREADY DONE — REFERENCED, NOT REBUILT

- **The Episode substrate** (NC 22, `0c7b6ee`): two clocks, frames, store, notice, and the
  retirement of `_trim_context`. B2 adds no store and no second window.
- **B1** (NC 20 `41c130a`, NC 25 `bfb09df`, NC 26 `0ee55fb`): detection, the structural stop,
  the class vocabulary. **B2 does not re-detect** — it begins where B1 stands down.
- **One decision point per modality** (NC 24, `422d330`): the typed funnel already calls
  `governed_decision` first. **B2 inherits both modalities for free; this is why F2 costs no
  voice edit.**
- **The audit-record shape** (NC 14 S3): derived from the decision object, no raw utterance.
- **The model-call observer** (NC 11, `harness/model_calls.py`): E1's instrument exists.

## WHAT'S KNOWN BROKEN — carried, not fixed here

- **`WorkingFrame` has no slots** (above). B2 cannot be built until that is ruled.
- **`branch_info` is inert by ruling** and stays inert until Proposal 1 is decided.
- **The typed notice reaches nobody** and stays that way until Proposal 2 is decided.
- **NC 21's probe set is not re-runnable** (its own dispatch doc records that the probes lived
  in a session scratchpad that is gone). B2's evidence must not cite it.
- **NC 28's adversarial verification of B1/Episode is IN FLIGHT.** Per the ratified order this
  REQ's build waits on it, and a finding there may change these acceptance rows before any
  code is written.

## CONSTRAINTS — WHAT MUST NOT REGRESS

1. **Every existing kernel gate still decides, and can still refuse, on a continuation** (C2).
   A continuation is a turn, not an exemption.
2. **The Episode charter's NEVER clause is untouched:** no authority lives in, rides on, or is
   inferred from a frame, a branch, or a patch (`REQ_CONVERSATION_EPISODE` §"THE REQUIREMENT").
3. **B1's structural stop is unchanged** — B2 must not widen, narrow, or shadow it (D4).
4. **The suite's failure set** — the same E7-shaped rule the sibling REQs carry.
5. **One spec per behaviour.** B2 owns continuation resolution. It does not restate detection
   (B1's), lifetime (Episode's), or the decision point (NC 13/24's).
6. **`_trim_context` stays retired.** No window-less interregnum, and no second window.

---

## OPEN — BILL DECIDES

1. **THE SLOTTED FRAME (blocking).** `WorkingFrame.content` is a `str`, `FRAME_KINDS` is
   closed, and clause 1 needs a slot to patch. **What shape does a slotted frame take, and is
   adding a kind to that closed set approved?** Nothing can be built until this is answered —
   and answering it by writing code would take the decision by default, which is precisely what
   Q3's deferral record was created to stop.
2. **PROPOSAL 1 — branch semantics.** Explicit member cue only, for v1?
3. **PROPOSAL 2 — the typed expiry notice.** Prepend, on every typed turn including refusals?
4. **Refusal vocabulary.** A1/A3 need at least one new `TurnOutcome`
   (an unresolvable continuation target). **One value or two** — is *"the target is gone"*
   distinct from *"the patch cannot be applied"*? A caller routes on the value, so this is a
   product question, not a naming one.
5. **Ordering against NC 28.** This REQ is written against `0ee55fb`; NC 28 is adversarially
   verifying that same code right now. **Does the B2 build wait on NC 28's verdict?** The
   ratified order says the build follows B1/Episode verification, which reads as yes — stated
   here so it is confirmed rather than assumed.

## HOW THIS REQ IS DISCHARGED

By A1–G2, when the build lands **after B1/Episode verification, per the ratified order**.
A session reports readiness; **Bill rules MET**. **Filed PLAN, stays PLAN.**
