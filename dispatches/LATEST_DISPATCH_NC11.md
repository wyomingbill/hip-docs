# NC 11 — MAKE THE TWO RULINGS FIRE ON THE REAL PATH (NC 10 REPAIR)
Status: BUILT — **LANDED** on `nc-b0`
Reconciled-Against: 2026-08-14. `~/hip-nc2` @ `nc-b0` @ **`4167184`**. Board claim
`ba9ebb2`/`3c9e981`; REQ amendment `9719279`.

REQ: `docs/requirements/REQ_KERNEL_GOVERNED_TURN__delta-typed-result-strip-only-web-store-down-refuse__v20260814_1803.md`
— **AMENDMENT 1**, filed **before the repair**. Spec: NC 10's record (`bb58140`, hip-nc).

---

## 0. THE EXCEPTION LINE

```
NC 11 — MAKE THE TWO RULINGS FIRE ON THE REAL PATH (NC 10 repair)
COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING
```

**Both rulings now fire on the DEFAULT path. NEEDS BILL: nothing.**

---

## 1. THE SHAPE NC 10 NAMED, AND WHAT IT COST

> *"A policy is implemented correctly, twinned correctly against an injected seam, and the
> seam simulates a state the production wiring cannot reach. The tests are not wrong about
> what they test. They test a path that does not exist."*

NC 9 shipped two correct policies and nineteen passing twins. **Neither policy could fire.**
The repair is wiring, and the acceptance had to change shape: **a twin that injects the
condition it is testing does not satisfy it.** That rule is now written into the REQ (E1–E7)
rather than assumed.

---

## 2. STORE-DOWN — PROVEN ON THE DEFAULT PROBE

**The defect.** The default probe was `read_user_facts("__kernel_probe__")`, which is
**contractually non-raising** — its own docstring promises `[]` on any failure *including
"Neo4j unreachable"*, precisely so retrieval can never break a turn (TD-011/TD-023). So the
kernel's `except → False` branch was **dead code**. NC 10 measured the consequence with the
graph genuinely down: `store_reachable() → True`, the household turn **ANSWERED**, the model
**called**, the reply *"Wednesdays"*.

**The repair.** `harness/extraction_queue._driver_for_probe()` builds a **throwaway** driver —
never cached, never shared, 3-second connect timeout — and the kernel calls
`verify_connectivity()`, which **raises**. Not cached, deliberately: caching a driver built
while the store was down would poison every later call, and reusing a live one would hide a
store that has since gone away.

**UNREACHABLE is now distinguished from EMPTY**, which is the whole repair: a store that
answers *"no facts"* is up; a store that cannot be dialled is down.

| measured, DEFAULT probe, graph genuinely down | before (NC 10) | after |
|---|---|---|
| `store_reachable()` | **True** | **False** |
| household turn | ANSWERED, model called, *"Wednesdays"* | **REFUSED_STORE_DOWN, 0 model calls** |

---

## 3. WEB SEARCH — PROVEN ON THE REAL GATEWAY

**The defect.** NC 9 asked *"did stripping change the query?"* — and **the strip removes facts
from CONTEXT and never rewrites the query string.** So `sent == query` always, the test was
always True, and the fail-closed branch was unreachable. NC 10 measured *"when is bill's
cardiology appointment"* — NC 9's own example — going out **PERMITTED and unchanged**.

**The repair.** `egress_gateway.household_referent_in(query)` derives the outbound query's
safety **itself**, in three classes ordered by what they cost:

1. **an enrolled member's name** — the registry is the authority on who this household is;
2. **a street-address SHAPE** — matched as a shape, **not against a stored value**, because a
   check that had to read the graph would be unavailable exactly when the store is down;
3. **a first-person or household possessive** — *my*, *our*, *the family's*.

**It returns the referent, not a bool**, so the refusal can say which class fired — a refusal
that cannot explain itself gets switched off. **It fails closed when the registry is
unreadable**: if we cannot enumerate who lives here, we cannot say a query names nobody.

**Measured on the real path, real gateway, real registry, sockets made impossible:**

| query (NC 10's own) | before | after |
|---|---|---|
| `what is an R-1-18 zone setback requirement` | PERMITTED | **PERMITTED, unchanged** |
| **`when is bill's cardiology appointment`** | **PERMITTED** | **REFUSED** — `member-name:Bill` |
| **`what are the setback rules at [REDACTED-HOME-ADDRESS]`** | **PERMITTED** | **REFUSED** — `address-shape:[REDACTED-HOME-ADDRESS]` |

`query_is_safe_to_send` keeps its `stripped_query` parameter **and ignores it**. Deliberate:
the argument that used to decide is now **visibly inert** rather than quietly deleted.

---

## 4. `model_called` — OBSERVED, NOT ASSERTED

NC 10 finding 3: the kernel set `model_called=True` unconditionally on the answered path, and
an implementation that called **no model** still reported True. It matters because
`process_governed_turn` returns structural replies with no model call — INJ-7 access-control
refusals, the park gate, the confirmation gate — so the field whose entire purpose is to be
trustworthy was lying on every one of them.

`harness/model_calls.py` is a **contextvar** counter — not a global, because turns are
concurrent on the voice path and a module-level counter would attribute one turn's call to
another's result. `record()` fires **at** the line that opens the completion, at both
answering sites in `_governed_turn`. That is the difference between observing and asserting.

Measured with NC 10's own method: impl that calls no model → `model_called=False,
notes=['model calls observed: 0']`; impl that calls one → `True, 1`.

---

## 5. TWIN COUNTS AND SUITE DELTA

**12 acceptance twins in `eval/test_nc11_rulings_on_the_real_path.py`, all on the default
path** — no injected probe, no hand-built payloads, the **real** classifier (initialised, not
monkeypatched), the real gateway, the real registry.

| group | twins |
|---|---|
| store-down on the DEFAULT probe (E1–E3) | **4** |
| web search on the REAL gateway (E4–E5) | **5** |
| `model_called` observed (E6) | **3** |

**NC 10's limit removed honestly:** it could not exercise *"a public turn still answers"*
because an uninitialised classifier makes everything household-dependent. This file
**initialises the real classifier** rather than monkeypatching the classification, so that
direction is now exercised for real.

**Full runs: NC 8's 21 + NC 9's 19 + NC 11's 12 = 52 passing.**

**SUITE: 20 failed / 488 passed — failure SET identical to baseline (20 / 476). Zero new,
zero fixed; +12 passed is exactly this dispatch's twins.**

---

## 6. FILED, NOT BLOCKING (2)

**(NC11-1) Seven NC 8 / NC 9 twins encoded the pre-repair behaviour and are updated with the
supersession annotated in each — never silently.** Three asserted `model_called=True` for
doubles that call no model (**they were asserting the lie NC 10 found**), two stubbed the
gateway with a hand-mangled payload to manufacture a condition the real path cannot produce,
and two met the real store probe once `process_text_query` was wired to the kernel. NC 9's
double now takes `calls_model=` so the claim is explicit at each call site rather than assumed
by the kernel.

**(NC11-2) The referent check is conservative, and that is the fail-closed side, on purpose.**
*"what is my body mass index formula"* is refused for its possessive. The REQ's OPEN section
required the test to be inspectable rather than buried in a regex, and it is — three named
classes, each reporting which one fired — so the cost is visible and tunable. **Not tuned
here**, because loosening a fail-closed rule is a policy change, not a repair.

---

## 7. WHAT THIS DISPATCH DID NOT DO

- **Never touched `~/hip-vo`.** All work in `~/hip-nc2` @ `nc-b0`.
- **Stood up no Neo4j.** The store being genuinely down is the test condition, not an accident.
- **Did not loosen any fail-closed rule** — §6.
- **Did not migrate voice**; `voice_turn` is unchanged and migration remains F1.
- **Did not delete a superseded assertion.** Every one is annotated with what changed and why.

---

## 8. CLAIM IMPACT

```
CLAIM IMPACT: none
```

---

## 9. VERIFIED

- **REQ amendment `9719279` precedes the repair `4167184`** and touches no source file.
- `lane_preflight.py` passes on `~/hip-nc2` before and after.
- Both rulings measured **on the default path**, with the outputs reproduced in §2 and §3.
- Suite failure **set** identical to baseline, captured in single runs after a timeout
  interrupted the first attempt — **the stash was verified restored before continuing**, and
  the interruption is recorded rather than hidden.
