# NC 20 — B1 DETECTOR BUILD (CAPABILITY)
Status: BUILT — **LANDED** on `nc-b0`
Reconciled-Against: 2026-08-14. `~/hip-nc2` @ `nc-b0` @ **`41c130a`**. Board claim
`ddbd0c9`/`a1bf9fd`; REQ amendment `a856863`.

REQ: `REQ_UNRESOLVED_REFERENCE_DETECTOR__...__v20260814_2056.md` (NC 17, `19a1fd4`)
**as amended by NC 20 with Bill's R2/R3/R4, filed before the first line of B1 code.**

---

## 0. THE EXCEPTION LINE

```
NC 20 — B1 DETECTOR BUILD (CAPABILITY; Bill's rulings 2-4 bind)
COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING
```

**26 twins across seven classes, all passing. Suite failure set identical to baseline.
NEEDS BILL: nothing.**

---

## 1. WHAT WAS BUILT

`harness/unresolved_reference.py` — four classes of dependency: **anaphoric reference,
continuation, bare assent, repeat-prior-action**. **Several carry no pronoun at all**, which is
the clause NC 17 put first because it is the one most easily lost. *"What is my address"*
carries one and remains the **store-down ruling's** case; a twin proves the two do not shadow
each other.

**Anti-vacuity is checked FIRST**, by exact match on the ratified five, **so no amount of
pattern drift below can ever swallow them.** That ordering is the mechanism, not a comment.

**Wired into `kernel.governed_decision()`** per NC 17's integration table — **both modalities
inherit with no voice edit** — and it fires **before the store probe**, so the stop does not
depend on the store being reachable.

---

## 2. THE THREE RULINGS, AS BUILT

**R3 — ambiguity fails closed BY ASKING.** One fixed clarification, byte-identical run to run,
and **no answering model call while unresolved**, observed at `harness/model_calls.py` rather
than trusted from the reply. **The turn is held, not lost** — which is why anti-vacuity
survived the ruling instead of being traded against it.

**R4 — the 8-turn window, as a TEMPORARY BOUNDED SCOPE superseded by Episode.** The window size
is explicit, and **the stop reason names its own reach** (*"…none is present in the 8-turn
window"*), so nobody reads an interim boundary as a design. A prior turn in the window resolves
the reference and B1 does not fire.

**R2 — class (a) never leaves at web egress.** `FACT_ASSERTION_WRITE` now refused alongside
NC 15's class (b), **with class (c) and `NOT_MEDICAL` untouched** — R2.2's anti-vacuity, because
a rule refusing all medical egress would pass R2.1 and break the product. The refusal says it
is defence in depth: a class (a) turn arriving at egress means a path skipped the kernel.

---

## 3. TWIN COUNTS BY CLASS — 26

| class | twins |
|---|---|
| **structural stop** (typed outcome, no model call, deterministic reason, fixed clarification, no retrieval/write, fires before the probe) | **6** |
| **anti-vacuity (R3.3)** — the five standalone questions, plus brevity, plus the household case | **7** |
| **R4 bounded scope** | **3** |
| **noninterference (N1)** | **2** |
| **ASR (N2)** — manufactured anaphor, manufactured name, dropped negation, changed number, spoken≡typed | **5** |
| **audit (N3)** — derived record, no raw utterance | **1** |
| **R2 egress** — class (a) refused with no socket; class (c) not refused | **2** |

---

## 4. SUITE DELTA

```
after NC 20 : 20 failed, 585 passed
baseline    : 20 failed, 559 passed
NEW: (none)   FIXED: (none)   +26 = exactly this dispatch's twins
```
By failure-**set** comparison, stashing only the source edits.

---

## 5. FILED, NOT BLOCKING (2)

**(NC20-1) A phrase can belong to two classes, and the first draft picked the less useful
one.** *"And the other one?"* is both a continuation and an anaphor; the initial ordering
reported `continuation`. Detection was identical either way — the class is diagnostic, not
behavioural — **but a stop reason that names the wrong half is a stop reason nobody can act
on**, so anaphor is now checked first as the more specific missing referent. Found by the twins
disagreeing with the detector, and fixed in the detector rather than in the assertion.

**(NC20-2) The detector is lexical, and that is a scoped choice with a visible cost.** It
matches referring language, not meaning, so a dependency phrased without any of the four
patterns is missed, and a standalone question that happens to contain *"that"* would fire were
it not for the exact-match anti-vacuity guard ahead of it. **The guard is what makes the
lexical approach safe at this scope, and it only covers the ratified five** — a sixth
standalone form would need adding there, deliberately. Named as the boundary of the approach,
not as a defect to chase now.

---

## 6. WHAT THIS DISPATCH DID NOT DO

- **Edited no voice code** — B1 entered at the kernel and voice inherited it.
- **Touched no `/ws/voice`, no demo lane, no frozen tree.**
- **Wrote no graph and started no service.**
- **Did not widen the anti-vacuity set** beyond the ratified five.
- **Did not loosen NC 15's class (b) rule** — R2 added class (a) beside it.

## 7. CLAIM IMPACT

```
CLAIM IMPACT: none
```
