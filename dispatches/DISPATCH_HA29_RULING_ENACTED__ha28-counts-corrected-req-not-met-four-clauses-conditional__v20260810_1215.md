# DISPATCH_HA29_RULING_ENACTED — HA-28's counts corrected, REQ ruled NOT MET, four clauses conditional
Status: **COMPLETE** — documents only
Reconciled-Against: roadmap `062eaa6`
Filed: 2026-08-10 (HA-29)
Decision-Owner: Bill
TYPE: CORRECTION + RULING ENACTMENT. No code, no behaviour, no claim change.

## 1. HA-28's COUNTS CORRECTED IN PLACE

**12 PASS / 1 FAIL / 7 CANNOT RUN.** The wrong numbers (`11 PASS, 1 FAIL, 8 CANNOT RUN`) are
preserved verbatim in the correction note, which credits **Bill, 2026-08-10** as the catcher.

**Counted from HA-28 §4's table in the correction itself**, row by row, not re-derived:

| verdict | rows | count |
|---|---|---|
| PASS | A1, A3, A4, A5, A7, A10, A13, A14, A15, A17, A18, A20 | **12** |
| FAIL | A19 | **1** |
| CANNOT RUN | A2, A6, A8, A9, A11, A12, A16 | **7** |
| | total | **20** |

**§4's table was correct as committed and is unchanged** — the error was in the summary line only.

**Ledger rows fixed.** Three places carried the counts, not one: `docs/INDEX.md` line 121 (the
dispatch-ledger row), `docs/INDEX.md` line 226, and `docs/HIP_HANDOFF.md` line 64. All three now
read 12/1/7 with an inline correction marker. The prose "Eight clauses CANNOT RUN" / "THE EIGHT
CANNOT RUNs" was corrected to seven in the same rows. **Fixing all three rather than only the
ledger row was a judgement call** — leaving a known-wrong count in two other places would have
been worse than the inconsistency the dispatch asked to fix.

## 2. BILL'S RULING RECORDED — REQ_OFFER_MECHANISM IS NOT MET

`REQ_OFFER_MECHANISM__…__v20260806_1625.md` Status now reads **NOT MET — ruled by Bill,
2026-08-10**, citing HA-28's corrected §4 table by path and listing every clause per verdict. The
prior `DRAFT-RATIFIED-PENDING` line is retained beneath it.

## 3. ACCEPTANCE TABLE AMENDED — Bill's ruling

- **A2, A8, A9, A11 → CONDITIONAL.** Each binds when its named feature exists — reminder
  delivery, transport layer, member-initiated capability path, explanation feature — **and not
  before. The requirement does not force those features into existence**, so their CANNOT RUN is
  not a debt against this REQ. Marked on each row and in a note above the table.
- **A6, A12, A16 stay UNCONDITIONAL** — real missing offer behaviour: delta minimality, the
  utterance→`ResponseKind` classifier, revocation/narrowing.
- **A19 stays a FAIL** until the durable exact-wording fix lands. Not conditional, not waived.

## 4. LEDGER — NO CHANGE, CONFIRMED

**C-14 already says exactly what the dispatch requires and was not touched.** `docs/INDEX.md`
line 64 carries it as **PARTIAL** with its timeline recorded as *a CONDITION, not a date* —
*"after the response classifier is built"* — which is the utterance→`ResponseKind` path. Verified
by reading; nothing edited.

## 5. RUNS

Docs only; no run could be affected. Batteries run once as the standing floor:

`PYTHONPATH=. python -m pytest -q --import-mode=importlib --continue-on-collection-errors`
→ **990 passed, 58 failed, 9 skipped, 9 xfailed, 34 errors.**

**This is NOT comparable to HA-28's "970 passed / 0 failed"** — that came from a narrower,
service-backed invocation. The full unfiltered suite here includes live-service-dependent tests.
**No PASS is claimed and no floor is asserted from these numbers**; the change is documents-only,
so no test outcome can be attributed to it either way.

## VERDICT

Counts corrected; ruling recorded; four clauses conditional; three unconditional; A19 still FAIL;
ledger untouched. **Nothing ruled MET beyond recording Bill's ruling.**

**CLAIM IMPACT: none.**

## OPEN

- A19's durable exact-wording fix (durable offer-instance store, or slots + rendered text in the
  R23 event).
- A6, A12, A16 remain owed.
- The roadmap lane has no single documented battery invocation — HA-28's and HA-29's absolute
  numbers differ for that reason alone.
