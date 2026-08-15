# DISPATCH_A12_RULING
Status: BUILT (rulings recorded; the R30 item-5 build is STOPPED — see the STOP section)
Reconciled-Against: 40c02fa (HEAD at dispatch start)
REQ: `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2129.md` — R12 and R30
Dispatch: D-92, 2026-08-01
**Status proposed: NONE. Nothing ruled MET. No code changed.**

Gate passed: bill-ai / [REDACTED-MACHINE-NAME] / `~/hip-roadmap` / `roadmap`, clean.
HEAD at start: **`40c02fa`** — note this is not `1bc2512` (D-91). A parallel lane landed
**D-55** (chat-handoff INDEX row, `REQ_TRUST_AXES` open-item flag) in between; docs only, no
overlap with this work. `~/hip-vo`, `~/hip-dev`, `~/hip-harness` NOT touched. **No code changed.**

---

## THE STOP — the dispatch is truncated

**Step 2's build specification cuts off mid-list.** The received text ends:

```
2. R30 ITEM 5 — THE BUILD. Bill ruled the backfill: pre-existing facts get a DISTINCT
   "pre-registry" MARKER. Not sensitivity.v1 (untrue — they were classified under TD-137's
   divergent encodings) and not blank (two permanent populations every consumer special-cases).
   Implement the version stamping per R30 item 5 across the three governed contracts:
   - the D-1
```

That is the end of the message. There are no steps 3 onward.

**I did not guess the rest.** I could infer the three contracts from D-88 and D-91 — the D-1
epistemic record (`harness/epistemic_record.py:96,:170,:266`), every `:Fact` node
(`memory_engine/store.py:159,:185,:220`), and the append-only ledger, which dual-writes the
record and inherits its shape. But inferring the *targets* is not the same as having the
*specification*, and this is a schema change across three governed contracts on a live graph.
What is missing is not recoverable by inference:

| Unspecified | Why it matters |
|---|---|
| the marker's exact form | `"pre-registry"` as a literal? a sentinel constant? a null-with-flag? Consumers must agree, and R29's whole lesson is that a second vocabulary drifts from the first. |
| the field name it is stamped into | R30 item 5 says the *version* must be recorded; the field is not named anywhere I can find. |
| whether backfill is a migration or lazy-on-read | 12 live facts today, but the choice determines whether a migration script is authorized — and `scripts/migrate_*.py` touching a live graph is not something to improvise. |
| acceptance criteria | A30 already passes while R30 is NOT MET. What makes item 5 *done* is precisely the thing that was cut off. |
| harness instruction, lock/commit/push steps | Every step 3+ is absent. |

Per the standing pattern — and D-91's own lesson that a confident false statement is the most
expensive kind of wrong — **I recorded the two rulings, which arrived complete, and stopped at
the build.**

---

## WHAT LANDED — both rulings, documentation only

### 1. A12 / R12 — FIX THE CODE, NOT THE RULE (Bill, 2026-08-01)

Recorded in `REQ_STRUCTURAL_CEILING` §16 as a new **R12** entry, and at the head of
`REQ_CEILING_ACCEPTANCE` §4's A12 subsection where a reader meets the row first.

**R12 stands exactly as written.** The two divergent clauses are defects in the read path, not
overreach in the requirement:

- **AGGREGATION** — the owner permit is per-fact and unbounded, so reading back every fact one
  ever stored about a subject reassembles the cross-report file R12 forbids. Bulk readback
  **SHALL be capped**.
- **DERIVATIVES** — `consolidate.py` gives a derived fact *"the same owner and subject as the
  sources"*, so an inference HIP drew from the author's input is owned by the author and the
  same permit reaches it. HIP's own inferences **SHALL stop counting as the author's property**
  merely because they were derived from the author's input.

**The alternative was recorded as REJECTED, explicitly.** Narrowing R12 to describe current
behavior would have made A12 pass immediately and cost nothing to implement. It was rejected
because it would quietly give up the claim:

> *the author can read back what they said; they cannot build a file on you.*

I wrote that into the REQ in those terms, with the reasoning that a product claim is not an
implementation detail — rewriting the requirement to match the code would have retired the claim
without anyone deciding to, which is the exact failure the CONTRADICTED sub-tier exists to
surface rather than absorb.

**A12 stays CONTRADICTED until the read path changes.** Recorded as a **live read-path change
with its own scheduled dispatch — not started here.** Nothing in `harness/` or `memory_engine/`
was touched.

**A16 unchanged, and restated so it isn't assumed to have moved with A12**: flips only when the
both-mechanisms ledger builds, and **must flip together with A17**.

### 2. R30 — the backfill question is now ANSWERED (Bill, 2026-08-01)

Recorded in §16's R30 entry. The ruling: pre-existing facts get a **distinct `pre-registry`
marker**.

- **not `sensitivity.v1`** — that would be *untrue*; those facts were classified under TD-137's
  divergent encodings, not under the registry that superseded them;
- **not blank** — blank leaves two permanent populations every consumer special-cases forever.

A distinct marker says the one true thing: *this fact predates the canonical registry, and the
vocabulary in force when it was classified is not `sensitivity.v1`.*

**This closes the open question D-91 flagged. It does not close the requirement.** §16 now says
so in those words: the ruling is recorded, item 5 remains unimplemented, **R30 remains NOT MET**.

### 3. §16's preamble updated

It read "R18, R29, and R30 have been ruled." Now reads **"R12, R18, R29, and R30 have been
ruled, and R30's backfill question is now answered."** Left unfixed it would have been false the
moment the R12 entry landed — the same class of stale status line D-91 found four of.

---

## What I did NOT do

- **Did not start the R30 item-5 build.** Truncated specification.
- **Did not start the A12 read-path fix.** Explicitly out of scope: its own scheduled dispatch.
- **Did not rule anything MET.** R12 is ruled *as a direction*; R30 stays NOT MET; A12 stays
  CONTRADICTED.
- **Did not run the harness** — no code changed, and the instruction to do so was in the
  truncated portion. The batteries are unaffected: nothing they assert was modified.

## A note on committing

The lock/INDEX/commit/push instruction was also in the truncated portion. I followed the house
pattern from D-81 through D-91 rather than leaving the tree dirty, because a dirty tree blocks
the next dispatch's step-0 gate. Saying so explicitly rather than letting it look instructed.

## To resume the build, I need

1. The **field name** and the **marker's exact literal form**.
2. Whether backfill is a **migration** over the 12 existing facts or **lazy at read time**.
3. The remaining two contracts as you intended them (I believe the record, the `:Fact` nodes,
   and the ledger — but I did not act on that belief).
4. The acceptance criterion for item 5, given A30 already passes while R30 is NOT MET.
