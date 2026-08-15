# REQ_CONVERSATION_EPISODE
Status: **PLAN**
Reconciled-Against: 2026-08-14. Kernel pinned at **`8ad909a`** (`~/hip-nc2` @ `nc-b0`) — the same
pin NC 17's B1 REQ carries, deliberately, so the two drafts describe one seam. *(NC 15's
`a51b120` has since added lines above the cited sites; the CONTRACT is the citation, and line
numbers are re-verified by whichever build lands first.)*
Filed by NC 18 — **DOCS ONLY**; the build follows **B1** per the ratified order.
Dispatch: NC 18

---

## THE REQUIREMENT — the settled principles (charter §17), verbatim

> **Episode carries SEMANTIC CONTINUITY ONLY — conversation_id, started_at, last_activity,
> absolute_expiry, typed working frames, branch info; NEVER authority; idle ~5-10 min +
> absolute ~30 min as TUNING PARAMS. An episode never authenticates a speaker — every voice
> turn needs fresh speaker evidence.**

**What "NEVER authority" buys, stated once:** an Episode may make a turn *understood* — never
*permitted*. Reference resolution, topic continuity, working frames: semantics. Principal,
verification tier, consent state, operator session: authority — and none of it may live here,
ride here, or be inferred from here. **A stale episode must be able to make a turn confusing;
it must never be able to make a turn AUTHORIZED.**

## THE SHAPE

One typed object, one owner:

| field | type | notes |
|---|---|---|
| `conversation_id` | opaque id | minted at episode start; never reused |
| `started_at` / `last_activity` | timestamps | `last_activity` advances on every governed turn |
| `absolute_expiry` | timestamp | `started_at + ABSOLUTE_TTL`; **advances never** |
| `working_frames` | **typed** frames | the semantic working set — entities, referents, pending topics. Typed means schema'd and enumerable, not a free dict |
| `branch_info` | typed | which conversational branch this turn extends (minimal semantics at first — see OPEN Q3) |

**RULED BY BILL 2026-08-14 (FM 24) — THESE ARE NOW FIXED VALUES, NOT BRACKETS:**
**`IDLE_TTL = 7 minutes`, `ABSOLUTE_TTL = 30 minutes`.** The mechanism was already fixed here
(both clocks exist, absolute wins); the numbers are now his and are no longer tunable without a
new ruling. *(Prior wording, superseded, kept visible:)* **TUNING PARAMS, not requirements-fixed values:** `IDLE_TTL ≈ 5–10 min`, `ABSOLUTE_TTL ≈ 30
min`. The REQ fixes the *mechanism* (idle-expiry and absolute-expiry both exist, absolute wins);
**Bill sets the numbers** (OPEN Q1).

## THE ACCEPTANCE TEST — each observable, pass or fail

- **E1 — NEVER AUTHORITY, structurally.** The Episode type carries no principal, no
  verification, no consent token, no operator session — proven by its field set (an
  AST/type-shape twin, the NC 15 pattern), not by convention.
- **E2 — no speaker authentication.** A voice turn with a live Episode but WITHOUT fresh
  speaker evidence gets exactly the treatment it gets with no Episode at all — twinned both
  directions.
- **E3 — expiry, both clocks.** Idle lapse ends the episode; absolute expiry ends it even under
  continuous activity; expiry mid-conversation yields a deterministic, stated behaviour (OPEN
  Q4), never a silent identity or authority change.
- **E4 — semantic continuity works.** Within a live episode, a turn depending on a prior turn's
  referent resolves from `working_frames` — the anti-vacuity direction, so the substrate is not
  a box nothing reads.
- **E5 — B1 integration by reference.** B1's detector consults THIS substrate for "is the
  needed state carried"; see the section below.
- **E6 — the seam is the kernel's.** Episode is read/advanced inside `governed_decision()`
  (`harness/kernel.py:234` at `8ad909a`) and travels as fields on `TurnRequest` /
  `TurnDecision` (`harness/turn_request.py:76`, `harness/kernel.py:218`) — **NC 17's
  integration table, reused verbatim; no second mechanism.**
- **E7 — zero new suite failures** by failure-set comparison.

## THE EIGHT STORES (NC 7 §4) — OWNERSHIP DISPOSITION, ONE EACH

NC 7 §4 found **no single conversation-state owner** across eight stores and three lifetimes
(in-process, request/session-scoped, durable-file). The Episode becomes the owner of exactly
the SEMANTIC subset. Each store, its disposition, and why:

| # | store (NC 7 §4) | lifetime | disposition | why |
|---|---|---|---|---|
| 1 | disclosure pendings (`harness/disclosure.py:47` `_PENDING` + file, TTL 1800 s) | process **and** file | **OUT-OF-SCOPE** | pending CONSENT is authority-adjacent state and stays with the disclosure gate; an Episode that carried it would carry a decision, not a meaning (and its restart-survival is the gate's problem — TD-146's history, not this REQ's) |
| 2 | member session / principal (`harness/member_session.py`, `principal_from_request` `:171`) | request-scoped | **OUT-OF-SCOPE** | this IS authority — the charter's NEVER clause, verbatim |
| 3 | session memory (`harness/session_memory.py`) | session | **ABSORBED** | session-scoped semantic memory is precisely `working_frames`' home; the Episode becomes its owner and the module's independent lifetime ends |
| 4 | transcript (`harness/transcript_log.py:79`) | durable file | **OUT-OF-SCOPE** | the durable audit record outlives every episode by design; an Episode may hold transcript-turn REFERENCES in frames, never own or truncate the record |
| 5 | dashboard operator session (`demo_dashboard.py:173`, `operator_auth.py:45`) | cookie | **OUT-OF-SCOPE** | operator authentication — authority again |
| 6 | conversation history for the prompt (`voice_orch.py:518` `_trim_context(max_turns=8)`) | in-request | **RETIRED** | the 8-turn window is the thing the Episode replaces; NC 7 called it *"the only thing today that resembles conversation memory"* and B1's Q2 prices its inadequacy. When the substrate lands, the window goes — prompt context derives from frames |
| 7 | per-session trace (`voice_orch.py:442`) | file | **OUT-OF-SCOPE** | telemetry/evidence, not continuity; readers of the trace must not become readers of the Episode |
| 8 | last speaker (`voice_orch.py:502` + `GET /api/last_speaker`) | process | **SPLIT** | the STORE is out-of-scope (a telemetry display); the semantic need it gestures at — *turn attribution for reference resolution* ("she said…") — is **absorbed as frame content, and never as authentication** (charter's last sentence, applied) |

**Net: 1 absorbed, 1 retired, 5 out-of-scope, 1 split** — and every out-of-scope row names the
reason, so the next session cannot re-derive a different table from the same evidence.

## HOW B1 RESOLVES AGAINST THIS SUBSTRATE — reference, not duplication

B1's REQ (NC 17) leaves **Q2** open, verbatim: *"What counts as 'missing' while there is no
state owner? … Either B1 is scoped to the window and says so, or the Episode capability lands
first."*

**When this substrate lands, that question closes BY REFERENCE:** *missing* = **not carried in
the live Episode's `working_frames`/`branch_info`** (or no live Episode exists). B1's detector
consults the Episode; it does not grow a window, a cache, or a second store. **Neither REQ
restates the other's clauses** — B1 keeps detection and the structural stop; this REQ keeps
ownership and lifetime — the R-NC1-1 one-spec-per-behaviour rule, applied between siblings.
*(Until this lands, B1's own window-scoping fallback stands; nothing here retro-edits NC 17's
draft.)*

## OUT OF SCOPE — the Audience Epoch boundary, stated

**Audience Epoch — who is PRESENT and what may be spoken aloud in front of them — is a separate
REQ, later.** The Episode knows what the conversation MEANS; it does not know who is in the
room. No presence set, no epoch counter, no audience-conditioned disclosure logic lands here,
and no field of this type may be repurposed to imply presence. The boundary exists because the
failure mode — "the episode says maya was talking, so maya must be present, so speak her facts"
— is exactly the authority-from-semantics inference E1/E2 forbid.

## WHAT'S ALREADY DONE — REFERENCED, NOT REBUILT

- The kernel seam and its types (NC 9/13/14, verified NC 10/12/16) — reused, per NC 17's table.
- B1's detection contract (NC 17) — referenced above.
- The deterministic split (NC 15) — untouched; class (b) fires before any Episode read.

## CONSTRAINTS — WHAT MUST NOT REGRESS

1. Every existing kernel gate (store-down, medical (b), claim mismatch) decides **before or
   without** Episode consultation — a broken or expired Episode must not break refusals.
2. The suite's failure set — E7.
3. `_trim_context` retires only WITH the substrate's landing, in the same capability — no
   window-less interregnum.

## RULED BY BILL — 2026-08-14 (FM 24)

**All four are answered. The questions are kept verbatim below so the ruling reads against what was
actually asked, per the annotate-never-rewrite rule.**

| # | RULING |
|---|---|
| **Q1 — TTL values** | **`IDLE_TTL = 7 min`, `ABSOLUTE_TTL = 30 min`.** Fixed values, not brackets. |
| **Q2 — persistence class** | **IN-PROCESS FOR THIS STAGE.** An episode dies with the process. This is a STAGE decision, not a permanent one — the conservative default the REQ proposed, and restart-survival is exactly what made store #1 a hazard. |
| **Q3 — branch semantics** | **DEFERRED TO B2.** Not answered, not dropped — see the deferral record below. |
| **Q4 — expiry mid-conversation** | **DETERMINISTIC NOTICE. A silent fresh episode is PROHIBITED.** |

### Q3's DEFERRAL, RECORDED SO IT IS NOT ORPHANED

**`branch_info` is in the SHAPE table above but its SEMANTICS are deferred to B2.** That gap is the
thing worth naming: a typed field with no ruled meaning is exactly how a placeholder quietly becomes
a de-facto behaviour, decided by whoever writes the first branch-setting code rather than by a
ruling.

**Until B2 rules it: `branch_info` is CARRIED AND NOT INTERPRETED.** No product behaviour may read it
to make a decision. Writing it is permitted; branching on it is not. **A build that acts on
`branch_info` before B2 has taken Q3's decision by default, which is the failure this record
exists to prevent.**

### Q4's RULING, stated as the invariant it is

**On expiry mid-conversation the member is TOLD, deterministically.** The prohibited behaviour is
specific and worth naming precisely: **a silent new episode that REINTERPRETS THE REFERENT.** If
"it" or "that one" resolved against the old episode's working frames and the episode has ended, a
silent restart re-binds those words to something else while the member believes they are still in
the same conversation. **That is a wrong answer delivered with full confidence — the failure mode
this whole substrate exists to prevent.** Notice is therefore not a courtesy; it is what keeps the
referent honest.

**E3's acceptance is tightened accordingly:** expiry mid-conversation must produce the notice, and a
test must prove that a referent from the expired episode is **not** silently resolved afterwards.

## THE QUESTIONS AS ASKED — kept verbatim



- **Q1 — the two TTL values.** Mechanism fixed here; numbers are his (idle 5–10 min, absolute
  ~30 min are the charter's brackets).
- **Q2 — persistence class.** In-process only (an episode dies with the process), or
  file-backed within `absolute_expiry`? In-process is proposed as the conservative default —
  restart-survival is what made store #1 a hazard — but it is a real product choice.
- **Q3 — branch semantics.** What creates a branch: explicit member cue, topic shift, or both?
  Minimal viable definition ships first; widening is his call.
- **Q4 — expiry mid-conversation.** Deterministic notice ("we've been going a while — starting
  fresh") vs silent new episode. Member-visible behaviour, so his.

## HOW THIS REQ IS DISCHARGED

By E1–E7, when the build lands **after B1 per the ratified order**. A session reports readiness;
**Bill rules MET**. Filed PLAN, stays PLAN.
