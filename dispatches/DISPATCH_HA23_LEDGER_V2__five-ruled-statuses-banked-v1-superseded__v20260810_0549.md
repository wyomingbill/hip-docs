# DISPATCH_HA23_LEDGER_V2 — five ruled statuses banked, v1 superseded

Status: BUILT (docs only)
Reconciled-Against: roadmap `8928e0c` (pre-dispatch HEAD)

**HA-23** | 2026-08-10 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BANKING**
**AUTHORITY:** Bill's status rulings, 2026-08-07 and 2026-08-09.
**NO CODE. NOTHING RULED MET. The status generator was again NOT built.**

**CLAIM IMPACT: C-02, C-03, C-07, C-10, C-11** — statuses banked, **no new evidence
produced by this dispatch.**

---

## 1. WHAT LANDED

| | |
|---|---|
| **v2 (CURRENT)** | `docs/deliverables/HIP_ClaimsLedger__v2-bills-ruled-statuses__v20260810_0549.md` |
| **v1 (SUPERSEDED)** | `HIP_ClaimsLedger__canonical-progress-instrument-13-claims__v20260809_1906.md` — **retained unaltered below its new header** |
| **LATEST symlink** | repointed to v2 |
| **Recorded reason** | *"Bill's status rulings, 2026-08-07 and 2026-08-09."* |
| **Truncation check** | first line `# HIP CLAIMS LEDGER`, last line `END OF LEDGER v2`, 13 claim rows — **PASS** |

The five rulings, as banked:

| Claim | v1 | v2 |
|---|---|---|
| **C-02** | PARTIAL | **PROVEN — Bill 2026-08-07** |
| **C-03** | PARTIAL | **PROVEN — Bill 2026-08-07** |
| **C-07** | PARTIAL | **PROVEN — Bill 2026-08-09** |
| **C-10** | PARTIAL | **PROVEN — Bill 2026-08-09** |
| **C-11** | UNPROVEN | **PARTIAL — Bill 2026-08-09** |

## 2. THE CONSTRAINT ITEM 1 PROTECTED, VERIFIED RATHER THAN ASSERTED

Item 1: *"No claim wording changes."* Checked column by column, not by eye:

```
CLAIM WORDING (column 2), v1 vs v2 → IDENTICAL — no claim wording changed
```

**That is the constraint that actually matters here.** The ledger's own governing rules make
a reword *"a superseding version with Bill's recorded reason"* — so a silent wording drift
inside a status-only update would defeat the instrument. There is none.

## 3. THE FULL DELTA — including what item 1 did not name

Item 1 says the only changes are the five statuses. **Bill's own v2 text contains more than
that**, and it is reported here in full rather than landed quietly, because "I banked your
text verbatim" and "only five things changed" cannot both be true unsupervised.

**Landed verbatim as Bill wrote it** — banked content is his to word (the HA-21/HA-12/HA-13
precedent), so nothing was reconciled back toward v1 by this session.

### (a) Eight rows gained `(draft)` — a label, not a status change

`C-01, C-04, C-05, C-06, C-08, C-09, C-12, C-13` keep their **v1 status value exactly** and
now read `PROVEN (draft)`, `PARTIAL (draft)`, `UNPROVEN (draft)`. This makes per-row what
v1's header already said globally. **No status value moved.**

### (b) Evidence cells: five substantive, six cosmetic

**Substantive — the five ruled rows, repointed at the dispatches that earned the ruling:**

- **C-02** → "REQ_DERIVED_WRITE_CUSTODY MET; Guard A live; standing custody battery (29 tests)"
- **C-03** → "AUTHOR VALIDITY clause; Guard B live at the pre-seal boundary; C7 negative twin"
- **C-07** → import-closure check live, fault twin proven (HA-22)
- **C-10** → teardown wired, zero-orphan check relocated post-suite, two back-to-back clean `--full` runs (HA-20)
- **C-11** → `--full` repeatable, binding layers green both runs (HA-20)

v1's C-11 evidence read *"expected at HA-19"* — an expectation that **did not hold**, since
HA-19's `--full` ratchet failed. v2 replaces a forecast with a measurement, which is the
correction that matters most in this delta.

**Cosmetic — and one of them is a small loss worth naming:** six cells drop their dispatch-ID
citations (`(D-R-194)` from C-08, `(HA-04/HA-05)` from C-05, `(D-146)` from C-13),
`REQ_STRUCTURAL_REFUSAL` → "Structural-refusal" in C-04, and a comma → semicolon in C-06.
**Dropping the IDs costs traceability** — those were the pointers from a claim back to the
dispatch that produced its evidence. **Flagged, not restored:** editing banked content is
Bill's, not a session's. A future version can put them back in one line.

### (c) Timelines on the five ruled rows

Four move to `now`. **C-11's stops being a date at all** — *"after live-layer rule is set
from collected run data"* — which is exactly right under item 12's amended rule forbidding an
invented threshold, and the first row in this ledger whose timeline is a **condition** rather
than a forecast.

## 4. WHAT DID NOT HAPPEN

- **No status was computed.** All thirteen are still declared. **The status generator remains
  the named next build** in `docs/BACKLOG.md` and was deliberately not built (item 5 of
  HA-21, restated by item 5 here).
- **Nothing ruled MET.** In particular `REQ_OFFER_MECHANISM` stays NOT MET — **v2's C-07 says
  so in its own evidence cell**, separating the claim from the REQ. A PROVEN claim is not a
  MET requirement, and this is the first row in the ledger to state that distinction.
- **No runs.** Docs only; no repository code changed.
- **CLAIM IMPACT names five claims and produced evidence for none of them.** The rulings rest
  on HA-19, HA-20 and HA-22; this dispatch only records them.

## 5. FINDINGS

1. **Claim wording is byte-identical across the version boundary** (§2), verified per column.
2. **The delta exceeds item 1's five statuses** (§3) — eight `(draft)` labels, eleven evidence
   cells, five timelines. Landed as Bill wrote it; reported rather than reconciled.
3. **Six dispatch-ID citations were dropped from evidence cells** (§3b) — a small traceability
   loss, flagged for a future version, not silently repaired.
4. **C-11's timeline is now a condition, not a date** (§3c), consistent with item 12's ban on
   inventing a threshold.
5. **v1 is retained readable** (§1) — a superseding version only means something if the
   superseded text survives.
