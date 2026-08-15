# REQ_GOVERNED_REALTIME_INTERACTION — HIP owns governance; the realtime model owns interaction quality only
Status: **PLAN**
Reconciled-Against: `roadmap` `3fc7017`; code cited at each tree's own HEAD — `~/hip-nc2` @ `nc-b0` **`62c0848`**, `~/hip-vo` @ `main` **`940ab5d`**. Read from the machine, not remembered.
Filed: 2026-08-15 16:24 (Mountain), **BEFORE any code is touched**, per Requirements Discipline item 1
Dispatch: NC 36 (DOCS ONLY — **the build follows review**)
Authority: **Bill's ruling B**, reproduced verbatim as §1 and used as the spine of every clause below.

---

## 1. THE REQUIREMENT — BILL'S RULING, VERBATIM

> **HIP owns authenticated identity, subject resolution, authorization, admitted context,
> disclosure, consent, and writes. The external/realtime model/API owns INTERACTION QUALITY
> ONLY — prosody, timing, conversational flow — and operates ONLY on context already admitted
> by HIP. It does not become a second governance authority.**

**THE LAST SENTENCE IS THE ONE THE ARCHITECTURE HAS TO ENFORCE, AND IT IS A NEGATIVE.** Every
other clause describes what something owns; that one describes what must be *unreachable*. A
negative is not satisfied by a model that behaves well — it is satisfied by a boundary the model
cannot cross even when it misbehaves. **Everything in §5 is written to make the negative
structural rather than behavioural**, because a promise from a model is not a control.

---

## 2. THE TERMS, FIXED HERE SO THEY ARE NOT RE-ARGUED PER DISPATCH

| term | means, in this REQ |
|---|---|
| **realtime channel** | any external, low-latency, streaming model or API session (speech-to-speech, duplex, or streaming text) that participates in a live turn |
| **admitted context** | exactly what HIP's governed path has already decided may be used for this turn, for this member, on this subject — the output of the kernel's decision, never an input to it |
| **interaction quality** | prosody, timing, turn-taking, backchannel, disfluency, pacing, barge-in handling — **properties of delivery, not of content** |
| **second governance authority** | any arrangement where the realtime channel's own judgement decides *what may be said, to whom, or whether a fact may be used* |

---

## 3. WHAT IS ALREADY TRUE — THE GROUNDING, CITED AT HEAD

**This REQ is written against landed code, not against a plan.** Four facts already hold and are
load-bearing; a design that contradicts any of them is wrong on arrival.

### 3.1 THE ADMISSION BOUNDARY ALREADY EXISTS AND BOTH MODALITIES CROSS IT

`harness/kernel.py` (`~/hip-nc2` @ `nc-b0`, **`62c0848`**):

- **`governed_decision()` — `harness/kernel.py:353`.** The one pre-generation decision point.
  It runs before any model on both modalities and returns a `TurnDecision`.
- **`governed_turn()` — `:165`, calling `governed_decision` at `:197`.** NC 24 made the typed
  funnel cross the *same* decision point the spoken path crosses, so "one call here is one call
  per typed turn".

**THIS IS THE ADMISSION BOUNDARY, and this REQ adds no second one.** A realtime channel is a
*consumer* of what `governed_decision` already decided. **If a realtime design needs a decision
the kernel does not already make, that is a change to the kernel — filed as such — and never a
decision the realtime channel makes for itself.** NC 25's B1 detector, NC 15's medical split and
the store-down ruling all sit inside this boundary; a realtime path that bypassed it would bypass
all of them at once.

### 3.2 THE WRITE-AHEAD EVIDENCE BARRIERS BIND

`harness/evidence_record.py` (`~/hip-vo` @ `main`, **`940ab5d`**):

- **`write_ahead()` — `:83`.** The durable pre-record. NC 34's ruling 1: no model call without it.
- **`finalize()` — `:106`.** NC 34's ruling 2: no delivery without it.
- **`read_turn()` — `:159`.**

**R-3.2 — NO REALTIME SESSION RECEIVES CONTEXT WITHOUT THE DURABLE PRE-RECORD.** Handing context
to a realtime channel **is** reaching a model, so it is on the far side of barrier 1 by
definition. FM 36 additionally made the ledger's directory fsync raise rather than swallow and
moved the epistemic record onto the blocking path, so "durable" here means durable, not attempted.

### 3.3 THE `/ws/voice` INGRESS STAYS FLAG-OFF — REFERENCED, NOT RELITIGATED

`REQ_WS_VOICE_OFF_THE_ACTIVE_SURFACE__registered-only-behind-an-off-by-default-flag__v20260814_2130.md`,
NC 19's ruling: *"this is REMOVAL FROM THE ACTIVE ATTACK SURFACE — never describe it as a
realtime migration"* (`server/demo_dashboard.py:2767-2782`). The route is **unregistered**, not
guarded-and-rejecting, because *"a registered handler that refuses has already ACCEPTED the
connection and run code."*

**R-3.3 — THAT RULING IS UPSTREAM OF THIS REQ AND IS NOT REOPENED HERE.** The realtime ingress
stays flag-off **until this REQ's acceptance (§5) exists and passes.** This REQ is the thing NC 19
was waiting for, not a request to revisit NC 19.

### 3.4 TD-V-040 IS THE STANDING COUNTEREXAMPLE THIS REQ EXISTS TO PREVENT

> **TD-V-040 (SEC):** *"The write-ahead evidence barriers (NC 34) DO NOT COVER the real-time
> pipecat voice loop — a third model-reaching, reply-delivering path with NEITHER barrier"*
> (NC 35 adversarial verify, 2026-08-15).

**READ IT AS THE FAILURE MODE, NOT AS A BUG TO FIX ELSEWHERE.** NC 34 wired both barriers into
`process_governed_turn` and its dispatch said "both modalities" — and a **third** path already
existed that reached a model and spoke a reply with neither. **The gap was not a wrong decision;
it was a path nobody enumerated.** A realtime integration is exactly the shape that produces more
of those, which is why §5's proofs are structural: *"we wired the barriers into the paths we knew
about"* is precisely the assurance TD-V-040 falsifies.

---

## 4. PRIOR DESIGN INPUT — RECONCILED, NOT SUPERSEDED

`docs/design/HIP_DESIGN__dual-model-natural-conversation-v2__v20260813_1500.md` (banked HA-66).
**It is reconciled: this REQ generalises it and contradicts none of it.**

| dual-model spec v2 | status under this REQ |
|---|---|
| §5 — *"ConversationObservation in (**evidence; grants no authority**)"* | **ADOPTED AS THE GENERAL RULE.** This is Bill's "not a second governance authority" stated as an interface property. |
| §5 — `AuthorizedResponseEnvelope` out, `may_paraphrase=false`, `may_expand=false` | **ADOPTED** as the shape of admitted content leaving HIP. |
| §6 — Option 3, *"Moshi answers freely from supplied context: **REJECTED** as initial architecture"* | **ADOPTED AND GENERALISED** to any provider: answering freely from supplied context is the second-authority failure. |
| §4 — output classes C0-C5, *"Uncertain class → block"* | **ADOPTED** as the disposition rule for realtime output. |
| §7 — the M0-M5 research staging, Moshi-specific | **NOT SUPERSEDED.** That is a research plan for one candidate provider; this REQ is provider-agnostic and does not choose one (§6). |

**ONE HONEST DISCREPANCY, RECORDED RATHER THAN SMOOTHED.** The A1 design plan
(`HIP_DESIGN__a1-governed-voice-plan__v20260814_0754.md:238-239`) records that
`AuthorizedResponseEnvelope` and `ConversationObservation` **"do not exist in code"**. So §4's
adopted interfaces are **design-only today**. This REQ therefore specifies a *property* the
implementation must have, not a class it must import — the property is what the acceptance tests,
and naming a type that does not exist would make the acceptance unwritable.

---

## 5. THE ACCEPTANCE — SKETCH AT PLAN STATUS

**Three clauses, each a structural proof. Stated as sketch because this REQ is `PLAN`: the build
follows review, and the twins are written when it is ruled.**

### A1 — THE REALTIME CHANNEL CAN NEVER EMIT CONTENT DERIVED FROM UNADMITTED CONTEXT

**STRUCTURAL PROOF, NOT MODEL PROMISE.** The test is not "the model didn't say the unadmitted
thing"; it is "the unadmitted thing was never reachable."

- **A1.1** the realtime session's inputs are **enumerable and asserted** — everything it receives
  in a turn is derived from the `TurnDecision` for that turn, and a twin asserts the *set*, not a
  sample.
- **A1.2** a fact denied by the injection contract, or a subject the kernel did not resolve, is
  **absent from the session's inputs** — proven by inspecting what crossed the boundary, in the
  shape NC 21 used for B1 (observe at the boundary; do not trust the reply).
- **A1.3 THE ADVERSARIAL HALF.** With a denied fact present in the *store* and absent from the
  admitted set, the realtime channel must be unable to produce it **even when prompted directly
  for it**. A twin that only checks the happy path proves nothing about a second authority.
- **A1.4 ANTI-VACUITY.** A channel that emits nothing satisfies A1.1-A1.3 and is useless. An
  admitted-context turn must still produce a normal spoken reply — the same trade NC 20's R3.3
  and NC 26's constraint 1 each had to make explicit.

### A2 — A GOVERNANCE REFUSAL TERMINATES OR REDIRECTS THE REALTIME STREAM DETERMINISTICALLY

- **A2.1** when the kernel refuses — B1's `REFUSED_UNRESOLVED_REFERENCE`, the store-down ruling,
  class (b) medical, disclosure, consent — the realtime stream **stops or is redirected to the
  canonical refusal**, byte-identical run to run, with **no model call** while unresolved (R3.2's
  existing property, extended to the streaming case).
- **A2.2 THE HARD CASE, NAMED: a refusal that arrives MID-STREAM.** A duplex channel may already
  be speaking when governance refuses. **The REQ requires the behaviour to be deterministic and
  specified, not merely fast** — and does not pre-judge whether that is hard-stop or redirect
  (§6, open decision 3).
- **A2.3** the refusal text remains **HIP-constructed** — the dual-model spec's C4: *"the model
  never decides, rewrites, explains, or embellishes."*

### A3 — THE EPISTEMIC RECORD NAMES WHAT THE REALTIME SESSION WAS GIVEN

- **A3.1** the per-turn record states **what was admitted to the realtime channel** — sufficient
  to reconstruct the boundary decision, in the derived-from-the-decision shape NC 14 S3 fixed and
  E1/E2 require.
- **A3.2 NO RAW UTTERANCE**, per E1, unchanged.
- **A3.3** the record distinguishes **realtime-delivered** from **HIP-delivered** content, so a
  later reader can tell which authority produced which words. Without this, A1 is unauditable
  after the fact.
- **A3.4** both barriers appear in the record for the realtime path — **the direct answer to
  TD-V-040**, whose defect was a path that produced neither.

---

## 6. OPEN — BILL DECIDES. STAGED, NOT TAKEN.

**None of these is inferred, defaulted, or "obvious". They are staged because taking them is a
ruling and this dispatch is docs-only.**

1. **WHICH PROVIDER(S).** Moshi (local, the dual-model spec's candidate), a hosted realtime API,
   or more than one behind an adapter. **Not chosen here.** Each has a different trust boundary,
   and §5's proofs must hold for whichever is picked — which is why the REQ is provider-agnostic.
2. **WHERE THE AUDIO BOUNDARY SITS — STT/TTS LOCAL vs REMOTE.** Whether raw member audio ever
   leaves the device is a **privacy-boundary decision, not a latency decision**, and it interacts
   with the egress gateway (`REQ_EGRESS_GATEWAY`) and the sensitivity ceiling. **Staged.**
3. **MID-STREAM REFUSAL BEHAVIOUR (from A2.2):** hard-stop versus redirect-to-canonical. Both are
   deterministic; they differ in what a member experiences. Raised here because A2 cannot be
   twinned until it is answered.

**A note on the shape of the last one:** it is an open question this REQ *discovered* rather than
inherited, and it is staged rather than defaulted for the reason NC 25's ruling 3 and NC 26's
NC26-F2 were — a session that picks the default has made the ruling and not recorded that it did.

---

## 7. CONSTRAINTS — WHAT MUST NOT REGRESS

- **The one decision point stays one.** No second admission boundary (§3.1).
- **Both write-ahead barriers stay binding on every path**, including this one (§3.2, TD-V-040).
- **`/ws/voice` stays flag-off until §5 exists and passes** (§3.3) — this REQ does not license
  turning it on.
- **No new best-effort governance evidence.** FM 36's ruling 4 boundary applies: anything feeding
  authorization, disclosure, consent or memory-commitment blocks.
- **Nothing here reopens TD-V-040 or TD-V-041.** Both remain NC 35's, needs-Bill.

---

## 8. WHAT THIS REQ DOES NOT AUTHORIZE

**No code.** `Status: PLAN`. The build follows review, per the dispatch. **It authorizes no
provider selection, no ingress flag flip, and no audio-boundary change** — all three are §6's,
and §6 is Bill's.

**Status: PLAN — not ruled MET, and not ruled anything else.** Sessions report readiness; Bill
rules.
