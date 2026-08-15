# REQ_KERNEL_GOVERNED_TURN
Status: PLAN
Reconciled-Against: 2026-08-14. `~/hip-nc2` @ `nc-b0` @ `f6dcdd3` (NC 8's tree).
Filed by NC 9 **before the first code edit**.

**THIS IS A DELTA REQUIREMENT (R-NC1-1): it REFERENCES the proven voice contract and does not
duplicate it.** What A1 (Voice 41) already built and proved is listed under WHAT'S ALREADY DONE
and is **not** restated as a requirement here. Only the delta is required.

---

## THE REQUIREMENT

Bill's words, 2026-08-14, verbatim:

> **OBJECTIVE (charter §15, settled): ONE modality-independent governed_turn() kernel. Typed
> TurnRequest in, TurnResult out. Text and voice are adapters producing a governed request; no
> independent copies of authorization, retrieval, consent, disclosure, prompt assembly, egress
> policy, or memory-write policy survive this capability on the text path.**
>
> **SCOPE: extract from the existing text path (process_text_query and its duplicates — the
> map's 8 duplicate implementations are the target list). Voice ADAPTER interface defined but
> voice migration itself stays in the F1/migration capability.**
>
> **STRIP-ONLY web search: outbound query must itself be safe; if protected household
> information is intrinsically required, fail closed or route to the governed consent path.
> Twins.**
>
> **STORE-DOWN REFUSE: fact store unreachable -> structural refusal for household-dependent
> turns, NO answering model call; pure public/general questions may continue. Twins both
> directions (household turn refused; public turn answers).**

**Expanded — and the delta must be stated precisely, because most of the kernel already
exists.** `server.voice_orch.process_governed_turn` already declares itself *"THE governed
turn. One implementation, whatever the modality"*, already takes a `TurnRequest`, already
derives the member from the principal, already raises `ClaimMismatch` in one place, and already
wraps the whole turn in `turn_provenance`. **That contract is proven and is referenced, not
rebuilt.**

**Four things it does not yet do, and they are this REQ:**

1. it returns a bare `str`, so a caller cannot see *what happened* — only what was said;
2. **STORE-DOWN REFUSE** is not implemented: NC 8 measured the turn answering *"Trash pickup is
   on Wednesdays. I don't have that confirmed yet."* with the fact store unreachable;
3. **STRIP-ONLY web search** is not implemented: NC 8 left web egress failing closed pending
   exactly this ruling (NC8-1);
4. the voice **adapter interface** is not named, so "voice is an adapter" is an intention
   rather than a signature.

---

## THE ACCEPTANCE TEST

**Twelve observations. Every ruling is exercised in both directions.**

### A. The kernel and its typed result

- **A1** `governed_turn(req)` returns a **`TurnResult`**, not a string, carrying at minimum:
  the reply, a typed outcome, the refusal reason when refused, the modality, the member, and
  **whether an answering model call happened**.
- **A2** **BEHAVIOURAL EQUIVALENCE.** The same `TurnRequest` through the pre-existing path and
  through the kernel **match on every governance-bearing field**. A difference is a failure,
  not a note.
- **A3** the voice adapter interface exists as a **signature that accepts a spoken request and
  returns the same `TurnResult`** — defined, not migrated.

### B. STORE-DOWN REFUSE — both directions

- **B1 RED** a **household-dependent** turn with the fact store unreachable is **structurally
  refused**, and **no answering model call is made** — asserted by observing the model boundary,
  not by trusting the reply text.
- **B2 GREEN** a **pure public/general** turn with the same store unreachable **still answers**.
- **B3** the refusal is **structural**: it names the store as the cause and does not invent a
  household value. NC 8's measured *"Trash pickup is on Wednesdays"* must not recur.
- **B4 FAIL CLOSED ON DOUBT.** If household-dependence cannot be determined, the turn is
  treated as household-dependent. Unclassifiable is not public.

### C. STRIP-ONLY web search — both directions

- **C1 GREEN** a query carrying no protected household information is permitted to a web-search
  destination **stripped**, and the outbound payload is asserted to be the stripped one.
- **C2 RED** a query that **intrinsically requires** protected household information **fails
  closed** — `EgressRefused`, no socket — or is routed to the governed consent path. It is never
  silently sent stripped-but-useless.
- **C3** the destination is **classified**, and a web-search destination is **strip-only**: no
  consent gate is imposed and no unstripped send is possible.

### D. Tests and regressions

- **D1** every test added is an **executing** test. **Source-text assertions do not count**
  (NC 8's rule, and NC 7's finding that 22 of 37 files assert over `read_text()`).
- **D2** **anti-vacuity**: assertions are on content and on observed side effects, never on
  "did not raise".
- **D3** **zero new suite failures**, established by **failure-SET comparison** against a
  baseline that stashes only the source edits.

---

## WHAT'S ALREADY DONE — REFERENCED, NOT REBUILT (R-NC1-1)

| proven contract | where | NC 9 does not touch it |
|---|---|---|
| **ONE governed implementation, any modality** | `voice_orch.process_governed_turn:2784` | the kernel wraps it; it is not reimplemented |
| **member DERIVED from principal; `ClaimMismatch` raised in ONE place** | `harness/turn_request.py:58`, `:76` | unchanged |
| **`typed_request` / `spoken_request` adapters** | `turn_request.py:193`, `:210` | reused as the adapter layer |
| **provenance binds the WHOLE turn**, so all fourteen record-emit sites inherit it | `epistemic_record.turn_provenance` | unchanged — a fifteenth outcome inherits it too |
| **egress gateway is the chokepoint** — `permit()`, `Destination`, `_assert_destination_is_truthful` | `harness/egress_gateway.py` | extended with a web destination; policy unchanged elsewhere |
| **typed intent failure, fail-closed** | NC 8, `intent_classifier.py` | reused for household-dependence, including its fail-closed rule |
| **the ungoverned ingress is closed** | NC 8, `server/app.py` | unchanged |

**A correction to NC 7's own framing, recorded so this REQ is not scoped from a wrong number:**
the map counted **8 duplicate implementations**, and both `/api/text-query` routes
(`demo_dashboard.py:2186`, `voice_https_orch.py:160`) **already call `process_text_query`** —
so the duplication on the text path is at the **HTTP surface**, not in the turn logic. The
kernel work is therefore *typing and ruling*, not de-duplicating a second turn implementation.
**The remaining duplicate routes are an HTTP-surface question and stay out of scope**, exactly
as the dispatch says.

---

## WHAT'S KNOWN BROKEN

1. **`_governed_turn` returns `str` from 15 separate return statements** across ~931 lines.
   A caller cannot distinguish answered-from-facts, answered-from-model, refused, or blocked.
2. **Store-down answers.** Measured by NC 8 against an unreachable graph:
   *"Trash pickup is on Wednesdays. I don't have that confirmed yet."* The provenance caveat
   was correct; the invented specific was not.
3. **Web egress fails closed pending policy** (NC8-1). This REQ carries the ruling that
   resolves it.
4. **No voice adapter signature** — "voice is an adapter" is currently prose.

---

## CONSTRAINTS — WHAT MUST NOT REGRESS

- **`~/hip-vo` is not touched.** Work is in `~/hip-nc2` @ `nc-b0`.
- **No graph writes; no Neo4j is stood up.** The lane declares 7693 and nothing listens there.
- **The proven contract keeps working**: principal derivation, `ClaimMismatch`, provenance
  binding, and the existing refusal paths behave exactly as they do today.
- **Voice is NOT migrated.** Interface only; migration is the F1 capability.
- **Out of scope:** HTTP-surface route dedup, conversation state, the frozen tree, the demo
  lane.
- **A refusal must never be softer than what it replaces.** If the kernel refuses where the old
  path answered, that is the ruling working; if it answers where the old path refused, that is a
  regression.
- **Exit codes are not answers** — verification steps run unchained.

---

## OPEN — NOT DECIDED BY THIS REQ

**What counts as "intrinsically requires protected household information" (C2) is a judgement
with a policy edge.** The implementation must state the test it used and keep it inspectable,
rather than burying it in a regex. A query naming a household member is clearly in; a query
about a public place the household happens to live near is clearly out; the middle is not
settled and the implementation must **fail closed** there and say so.

---

# AMENDMENT 1 — THE RULINGS MUST FIRE ON THE DEFAULT PATH (NC 11, 2026-08-14)

**AMENDED, NOT REPLACED.** Everything above stands as filed. NC 10's adversarial verification
(`bb58140`, hip-nc) found that acceptance B1-B4 and C1-C3 were **twinned against seams the
production wiring cannot reach**, so the policies were correct and inert. This amendment adds
the acceptance that would have caught that.

## THE REQUIREMENT — Bill's words, 2026-08-14, verbatim

> **1. STORE-DOWN: replace the default probe. It must distinguish UNREACHABLE from EMPTY — a
> real connectivity check (driver session/ping) that RAISES or returns False on failure, never
> read_user_facts (its []-on-any-failure contract is the dead branch). Twin ON THE DEFAULT
> PROBE: store genuinely down -> structural refusal, model provably not called (patched
> client). Public query still answers. No injected probe in the acceptance path.**
>
> **2. WEB SEARCH: make the safety test compare against a REAL rewritten query. If the gateway
> only strips context, the kernel must derive the outbound query's safety itself: protected
> household tokens/referents intrinsically in the query -> fail closed or route to the consent
> exception, per Bill's ruling. Twin ON THE REAL GATEWAY: NC 9's own example ("when is bill's
> cardiology appointment") must NOT go out unchanged; a clean public query goes out. No
> hand-built payloads in the acceptance path.**
>
> **3. model_called becomes OBSERVED, not asserted — set where the call happens; guard/park/
> confirmation replies show False. NC 10's finding-3 method is the twin.**
>
> **4. Rerun NC 9's 19 + NC 10's probes; zero new suite failures by set comparison.**

## THE ACCEPTANCE TEST — the seam rule is itself an acceptance criterion

- **E1** the DEFAULT probe reports DOWN against a genuinely unreachable store, and
  **UNREACHABLE is distinguished from EMPTY**.
- **E2** household turn + store down, **no probe and no implementation injected**: structural
  refusal, and the model is **provably** not called — observed at a patched model client.
- **E3** public turn + store down, **with the real classifier**, still answers. No
  monkeypatched classification.
- **E4** on the REAL gateway with the REAL registry: NC 9's own example does not go out; an
  address query does not go out; a clean public query goes out unchanged. **No hand-built
  payloads.**
- **E5** the referent check **fails closed when the registry is unreadable**.
- **E6** `model_called` is False for an implementation that calls no model and True for one
  that does — NC 10 finding 3's own method — and the counter is turn-scoped.
- **E7** zero new suite failures **by failure-set comparison**.

**A TWIN THAT INJECTS THE CONDITION IT IS TESTING DOES NOT SATISFY E1-E6.** That is the rule
NC 10's findings are made of, and it is now written down rather than assumed.

---

## AMENDMENT 2 — THE SMUGGLE-EDGE DETERMINISTIC INTENT SPLIT (Bill's ruling, 2026-08-14, NC 15)

Appended per the standing amendment pattern (HA-86/FM 14): the amendment PRECEDES the code in
the commit graph and touches no source file. Everything above stands unchanged.

### THE RULING — Bill's words, verbatim

> **No blanket park-all, no categorical refusal of first-person medical:**
> **(a) recognized first-person medical FACT ASSERTION with write semantics -> park-and-confirm;**
> **(b) ambiguous medical assertion/write intent -> deterministic clarification/refusal, NO model, NO write;**
> **(c) legitimate medical question/retrieval -> normal governed query path.**
> **The fix must NOT turn arbitrary medical language into durable memory merely because it is
> first-person. The split is deterministic — classifier proposes nothing here.**
> **Web-search egress inherits: class (b) never leaves the device.**

Context: NC 12 §4 measured nine of ten referent smuggles passing the NC 11 check, and named
`what medication am I taking` first. This ruling answers the WRITE-SEMANTICS half of that edge.

### THE ACCEPTANCE TEST (amendment scope)

- **A2-1** The split is a pure deterministic function — no model, no `intent_classifier`, no
  I/O — returning a typed class plus a REASON (a refusal that cannot explain itself gets
  switched off). Same input, same class, every time.
- **A2-2 (a)**: a recognized first-person medical fact assertion with write semantics and a
  concrete value routes to the NORMAL governed path, whose park-and-confirm machinery holds it —
  the kernel does not invent a second park.
- **A2-3 (b)**: ambiguous medical assertion/write intent returns a DETERMINISTIC clarification
  from a fixed template. **The implementation is never invoked** (proven with a recording
  impl — model_called=False, zero impl calls, therefore zero writes, since writes live in the
  impl).
- **A2-4 (c)**: an interrogative/retrieval medical turn — INCLUDING first-person
  (`what medication am I taking`) — routes to the normal governed path. **Never (a), never (b).**
- **A2-5** Order is pinned: question-shape is tested BEFORE assertion-shape, so a first-person
  question cannot be captured as an assertion.
- **A2-6** NC 12's ten smuggles are re-run through the split and the mapping REPORTED —
  **expected: none lands in (a) or (b)**, which is the no-over-capture constraint proven on
  real adversarial inputs.
- **A2-7** Egress: a class-(b) query presented to web-search egress is REFUSED with a distinct
  typed exception, zero sockets opened. (Classes (a)/(c) at egress are NOT changed by this
  amendment — any widening there is a separate ruling.)
- **A2-8** Zero new suite failures by failure-set comparison, and **the seam rule above applies
  in full: a twin that injects the condition it is testing satisfies nothing** — (b)'s
  no-model/no-write is proven through the DEFAULT path of the split, not through a stub of it.

### CONSTRAINTS

1. **No blanket park-all**: (c) and out-of-domain medical language must reach the normal path.
2. **No categorical refusal**: first-person medical QUESTIONS are answered, not refused.
3. **Nothing becomes durable memory merely for being first-person medical**: only (a) may reach
   the park path, and park-and-confirm itself still gates the write.
4. **(b) is model-free and write-free by construction** — decided before the implementation is
   resolved, like the STORE-DOWN gate.
5. Deterministic means INSPECTABLE: lexicon and shapes live in one module with reasons.

### KNOWN SCOPE LIMIT AT FILING

NC 14 is IN FLIGHT on `nc-b0` with uncommitted work in `harness/kernel.py` — the wiring site.
The split module, its twins and the mapping land without touching NC 14's files; **the kernel
gate and egress inherit are STOPPED until NC 14 reaches a committed boundary**, and this REQ
stays PLAN until the wiring lands and Bill rules.
