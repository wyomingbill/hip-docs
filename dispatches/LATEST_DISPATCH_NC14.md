# NC 14 — SINGLE-DECISION MIGRATIONS, BILL'S ORDER (F1 CONTINUES)
Status: BUILT — **LANDED** on `nc-b0`
Reconciled-Against: 2026-08-14. `~/hip-nc2` @ `nc-b0` @ **`8ad909a`**. Board claim
`80cc314`/`c7d7e3f`; REQ amendment `0db77f3`.

REQ: `REQ_VOICE_INTO_KERNEL__...__v20260814_2013.md` **AMENDMENT 1**, filed before the code.

---

## 0. THE EXCEPTION LINE

```
NC 14 — SINGLE-DECISION MIGRATIONS, BILL'S ORDER (F1 continues)
COMPLETE WITH FINDINGS — 3 ITEMS FILED, NOTHING BLOCKING
```

**All four segments migrated in order. `_on_user_text` 712 → 652 lines, control-flow
56 → 45. 17 twins. Suite failure set back to baseline.**

---

## 1. THE FOUR SEGMENTS

| seg | decision moved to | branches | twins |
|---|---|---|---|
| **S1** speaker identity | `kernel.identify_speaker()` → `SpeakerIdentity` | **56 → 50 (−6)** | 7 |
| **S2** confirmation | `kernel.resolve_control()` → `ControlDecision` | **50 → 45 (−5)** | 5 |
| **S3** disclosure | `kernel.resolve_disclosure_block()` → `DisclosureRefusal` | **45 → 45 (0)** — §2 | 3 |
| **S4** memory-write | `kernel.should_record_for_extraction()` | **45 → 45 (0)** — §3 | 2 |

Each completed with its twin before the next began, per the order Bill set.

**S1** ends the divergence his ruling names: two implementations of *who is speaking* could
agree on **whether** to answer while disagreeing on **for whom**. TD-126's rule — a `no_match`
ranks with `unenrolled`, so a print scoring like noise never clears a floor — is now in one
place and twinned. Identity **fails closed**: no verifier, no audio, a corrupt print or an
unreadable registry all yield a guest with the high-sensitivity floor.

**S2** was the clearest case of a decision that existed only as a side effect: the verb
classification, the pending-confirm override, the handler dispatch and the action reading were
interleaved with the speaking and the transcript writes. **You cannot diff a decision that only
exists as a side effect.** It is now a `ControlDecision` value; the adapter performs the
effects.

**Fail-closed is inherited at every boundary** (Sn.4): a raising classifier declines, a raising
control handler declines, a raising refusal-selector returns a generic refusal. The S2 twin
observes the model counter and asserts **zero calls**.

---

## 2. ⚠ S3 MOVED A REAL DECISION AND THE COUNT DID NOT SEE IT

Choosing between an **access-denied** refusal and an **empty-set** refusal is a decision, not
formatting — the two say different things about the household — and the telemetry row is now
**derived from the refusal**, so the record cannot disagree with what was said.

**The branch count did not move, because the choice was a ternary.** NC 9's method counts
`If / For / While / Try`; a ternary is an `IfExp` and is invisible to it. Measured both ways:
**strict 45, wide (with `IfExp`/`BoolOp`) 77.**

**The REQ's own constraint says a segment whose count does not drop has not migrated a
decision.** By the letter, S3 fails that test. **By the evidence it does not** — the decision
is in the kernel, twinned three ways, and the record is derived from it. **Reported as a
metric blind spot rather than resolved in my own favour**: the rule is right for `If`-shaped
decisions and blind to expression-shaped ones, and that is worth knowing before the next
segment is measured by it.

---

## 3. S4 FOUND THERE WAS NOTHING LEFT TO MIGRATE — AND SAYS SO

**TD-035 removed per-turn Zep write-back**: *"facts reach Neo4j via the extraction queue at
session end (the single Neo4j write path)."* So the only per-turn memory decision on voice is
**whether the utterance is captured for that later extraction**, and that is a function of
identity alone — **already moved by S1**.

It is now a named kernel rule (`should_record_for_extraction`) rather than a bare truth test
repeated at call sites, which is how the S1 copy diverged in the first place. **One line, and
deliberately not more: inventing machinery to make the segment look bigger would be worse than
reporting that the work was already done.**

---

## 4. SUITE DELTA

```
after NC 14 : 20 failed, 516 passed, 39 skipped, 21 errors
baseline    : 20 failed, 499 passed
```
**Failure set back to baseline; +17 passed is exactly this dispatch's twins.**

An intermediate run showed **21** — one new failure, found and fixed before landing (§5).
`/ws/voice` remains out of scope; `demo_dashboard.py:2765`'s realtime endpoint is the
deliberately-red C8 surface and is **pre-existing, not touched, and still red by design**.

---

## 5. FILED, NOT BLOCKING (3)

**(NC14-1) `test_HA65` caught five UnboundLocalError hazards in my own S2/S3 code — and
caught my first fix too.** `if x is None: from … import y as x` binds `x` local at the import
line, so the read above it is unsafe. My first correction assigned to a temporary first; **the
guard still failed, correctly** — a prior assignment does not help, because the read at the
`if` still precedes the import binding. The shape that satisfies it: **the import never
rebinds a name that is read.** NC 9 hit this once; this dispatch hit it five times in one sitting.

**(NC14-2) The branch-count method is blind to expression-shaped decisions** — §2. Both
numbers are now reported. A future segment measured only by the strict count could move a real
decision and read as having done nothing, or add a ternary and read as clean.

**(NC14-3) The migration is decision-by-decision, not line-by-line, and 652 lines remain.**
What is left in `_on_user_text` is routing, streaming, telemetry and transport — plus the
`permit()` at the egress point, which is correct where it is. **The four governance-bearing
decisions Bill named are now the kernel's**; the residue is not a second decision path, and
saying so is a claim this dispatch can support only for those four.

---

## 6. CLAIM IMPACT · NEEDS BILL

```
CLAIM IMPACT: none
```

**NEEDS BILL: nothing.** The order completed as set; no contradiction arose, so no segment
stopped.
