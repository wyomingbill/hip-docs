# DISPATCH_HA80 — restatement check before F3 (Option A) + F3 log fix
Status: BUILT
Reconciled-Against: `roadmap` @ this dispatch's commit

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_atorvastatin-false-ack__f3-gate-widen-and-detect-retry__v20260716_1713.md`
— the governing REQ for the F3 declarative gate, which this change modifies.
Item 8's gate is satisfied by naming an existing REQ; **none was written
retroactively.**

**RULING IMPLEMENTED (Bill, HA-80): Option A.** Wording-only was rejected.

---

## WHAT WAS BUILT

**A structural already-known check runs BEFORE the F3 failure claim can fire.**
When the detector proposes zero changes and the utterance canonically restates a
fact the record already holds, the reply acknowledges it. No failure claim, no
write, and the determination is recorded.

`server/voice_orch.py`:

* **`_restates_known_fact(query, facts)`** — structural, **no model call**. It
  must not depend on the detector whose blank output caused the problem.
* **`ALREADY_RECORDED_REPLY`** — *"You've told me that before — it's already in
  the household record, so there was nothing new to save."*
* Wired into `_gate_unconfirmed_update` **after** the P8 park check (REQ
  constraint: P8 runs first and is unconditional) and **before** the F3 claim.
* The outcome records `already_recorded` **both ways** plus
  `already_recorded_attribute`, so a reader can tell a
  determination-of-not-known from the check never having run.

**The comparison is HA-74's `canonical_fact_value`. Nothing was invented.** Its
prohibition is carried over intact: no fuzzy equality, and the stored value is
matched on **word boundaries**, so `atorvastatin 20mg` cannot match an utterance
about 25mg or 120mg.

**On containment, stated rather than glossed:** HA-74 forbade substring matching
for *fact identity* — deciding whether two stored values are the same fact, where
a loose match silently merges a dose change. This asks a different question: does
an utterance **assert** a fact the record already holds. An utterance is a
sentence and the fact is a phrase inside it, so containment is the shape of the
question, not a relaxation of the identity rule. Identity itself is still exact,
and a short-value guard plus word boundaries keep it from firing loosely.

**Fail-safe direction:** the check never raises; any error falls through to the
existing F3 behaviour rather than suppressing it. An utterance carrying
unresolved transition narration returns `None` from `canonical_fact_value`, and
that refusal is the signal to leave F3 alone rather than guess.

**LOG FIX (both lines).** `loguru` formats with `{}`; `%`-style silently drops the
arguments. Bill named `:2408`; **the P8 line immediately above had the identical
defect** (`parked=%d`) and is fixed with it — leaving one broken after fixing its
neighbour would have been odd. Named here rather than slipped in.

## ACCEPTANCE

| | required | result |
|---|---|---|
| **1** | TD-147's shape: restatement no longer claims save failure; record shows the determination | **PASS — live** |
| **2** | Anti-vacuity: a genuinely NEW fact still writes, 3/3 | **PASS** |
| **3** | A CHANGED value still supersedes, unaffected | **PASS — live** |
| **4** | L6 single-row result reported, no pin/expectation changes | **reported below — G1 STILL FIRES** |
| **5** | The log line prints real counters on a live fire | **PASS** |

### (1) and (3) — live, end to end through `process_text_query`

```
1 NEW      -> normal ack      'You take atorvastatin 20mg every morning to help manage your cholesterol levels.'
2 RESTATE  -> ALREADY-RECORDED "You've told me that before — it's already in the household record,
                                so there was nothing new to save."
3 CHANGED  -> normal ack      'You take atorvastatin 40mg every morning to help manage your cholesterol levels.'
```

Turn 2 is the exact utterance from HA-77 C4's G1 violation. **Before this change
it produced *"unable to save it to the household record"*.** Turn 3 proves a real
change still supersedes — the check does not stand between the user and a write.

### (2) — anti-vacuity, and the guards

`eval/test_restatement_before_f3.py` — **18 passed.** New facts never match
(3/3 parametrised); changed doses, changed frequency and the `20mg`-inside-`120mg`
word-boundary trap all correctly return no match; transition utterances never
match; trivially short stored values cannot match by accident; an error falls
through instead of suppressing F3; and AST scans assert the comparison is
HA-74's with no fuzzy matching, that the check runs before the failure claim, and
that P8 still runs first.

### (5) — the log, on the live fire

```
HA-80: declarative produced no write, but the asserted fact is ALREADY RECORDED
(attribute=medication subject=sam) — acknowledging instead of claiming a failed
save (proposed=0 mutations=0 noops=0)
```

Real counters, zero literal placeholders. It also **confirms HA-79's diagnosis
empirically**: `proposed=0` means the detector proposed nothing at all, not that
it proposed something the no-op path lost.

### (4) — L6, reported honestly

```
[harness-run] empty or missing — skip
[turns_demo] turns_demo.jsonl
    G1 no-orphan-generation: FAIL (1)
      [sam] 'I take atorvastatin 20mg every morning.'
        generated about ['sam'] with zero admitted facts about them
        -> "You've told me that before — it's already in the household record…"
== L6: 1/1 (0 flaked, 0 skipped)   record-invariants  PASS
```

**THE `1/1 PASS` IS VACUOUS AND MUST NOT BE READ AS A FIX.** `harness_run.jsonl`
is the gate (`eval/harness.py:287`), it was **0 bytes** because a targeted live
run writes to `turns_demo.jsonl` and not to the gate log, so the scenario passed
having scored nothing.

**The informational scan still shows G1 FAIL (1), on the same turn, now carrying
the new reply.** That is the honest delta:

> **HA-80 fixes the falsehood told to the user. It does NOT change the record's
> grounding shape, so G1 still fires.**

G1 tests generation grounding — `path=generation`, `delta=[]`,
`inj2_declarative_override=0`, no admitted facts about the subject. None of those
changed: there is still no write (correctly — the fact is already there) and the
fact still is not admitted back into context on the turn that restates it.

**No pin, baseline or expectation was touched.** Whether G1 should exempt a
determined restatement — the record now carries `already_recorded=True`, which
would be the natural exemption key — **is Bill's to rule, not a session's.**

## VERIFIED

**Watched run:** the three live turns through `process_text_query`; the log line
from that fire; the 18-test suite; the direct probe of the check across
restatement / dose-change / frequency-change / transition / new-fact /
short-value / boundary cases; `--layer 6`; the battery-manifest test after
registering the new file; and `harness_run.jsonl` measured at 0 bytes.

**Reasoned about:** that the P8 and D-02/D-05 constraints hold — argued from
ordering in the gate (asserted by two tests) rather than by re-running those
scenarios.

**Not run:** `--full` and the memory harness, per the dispatch's scheduling
constraint.

## CLAIM IMPACT

**CLAIM IMPACT: none.**

## OPEN — NEEDS BILL

1. **L6 G1 still fires**, by design, on a turn that is now behaving correctly.
   Whether a determined restatement should be exempt from G1 — keyed on
   `already_recorded` — is a ruling, and the delta is deliberately left for it.
2. **The fact is not admitted back into context** on the turn that restates it,
   which is what leaves the generation ungrounded. A retrieval/admission
   question, untouched here.
3. **TD-123 / TD-125 untouched**, as instructed. This is a symptom fix at the
   gate; the detector's `changes:[]` on restatements is unchanged.
