# DISPATCH_HA33_WRITE_LOSS — defect reproduced, fix proven, NOT LANDED (L7V2 binding failure)
Status: **CLAUSE LANDED — PRODUCT FIX PROVEN BUT NOT LANDED**
Reconciled-Against: roadmap `a7807d8`
Filed: 2026-08-10 (HA-33)
Decision-Owner: Bill
REQ: `REQ_DERIVED_WRITE_CUSTODY` — clause added by this dispatch
Patch: `docs/dispatches/HA33_writestate_guard_not_landed.patch` (**not applied**)

## ITEM 1 — THE DEFECT, EXECUTED (it had only ever been read)

```
encode(write_state='not_a_real_state', owner=maya)
  RAISED?           : NO — returned normally
  returned type     : EncodeResult
  new_fact_id       : 57cb8008-cb06-469b-bc7d-7216032448d5   <-- FRESH ID ISSUED
  Fact nodes before : 0   after: 0   delta: 0                <-- NOTHING WRITTEN
```

Silent write-loss confirmed by observation. HA-19 found it by code reading and
`REQ_DERIVED_WRITE_CUSTODY`'s own KNOWN BROKEN item 6 recorded it; **this is the first execution.**

## ITEM 2 — CLAUSE ADDED (landed)

`REQ_DERIVED_WRITE_CUSTODY`, new **WRITE-STATE VALIDITY** section citing Bill's ruling 2026-08-10:

> **A write with an unrecognized write_state SHALL be refused before sealing or persistence.**

Item 6 is retained as the record of the defect and how long it stood.

## ITEM 3 — THE FIX (proven, not landed)

`InvalidWriteState` beside `InvalidAuthor` in `harness/write_rule.py`; `_KNOWN_WRITE_STATES`
named once in `memory_engine/store.py`; the guard placed immediately after
`partition_classify_write` — beside the author check, **ahead of every seal, key operation and
graph write** — following the `InvalidAuthor` raise-and-record shape exactly.

## ITEMS 4–5 — ANTI-VACUITY AND THE SEVEN ABSENCES, ALL OBSERVED

**Anti-vacuity (canonical attribute `medication`)** — the earlier failure was a bad fixture
(non-canonical attribute), not the change:

| state | result |
|---|---|
| `augment` / `supersede` / `correct` / `unresolved` | **all WROTE**, `node_delta=1` each, fresh fact_id each |

**The refusal, seven absences each its own observation:**

| # | absence | observed |
|---|---|---|
| 1 | no false success result | `returned=None`, `raised=InvalidWriteState` |
| 2 | no fact | `new_fact_id` = `None` |
| 3 | no node | `node_delta = 0` |
| 4 | no ciphertext | `encrypt_by_class` calls = **0** |
| 5 | no seal | `create_fact_node` calls = **0** |
| 6 | no key operation | same — seal and key both occur inside `create_fact_node` |
| 7 | no derivative | facts carrying the refused value = **0** |

**Weakness stated, not hidden:** #5 and #6 share one observation (`create_fact_node` call count),
and #7's query relies on a `value` property that does not exist on Fact nodes (values are sealed),
so it returns 0 trivially — #3's `node_delta=0` is the load-bearing evidence there. **These are
not yet standing tests**; they were executed live.

## ITEM 6 — RUNS, AND WHY THIS DOES NOT LAND

| command | result | vs baseline |
|---|---|---|
| canonical suite | 1048 passed, 31 failed, 10 skipped, 9 xfailed, 2 errors | **unchanged** |
| `--layer 7` | **exit 2 — BINDING FAILURE** | **REGRESSION** (exit 0 at HA-32) |
| RATCHET `--full` | RATCHET FAIL | — |
| memory harness | 13/17 | inside pin |

**`L7V2:MUTATION-NO-SILENT-DISAPPEARANCE` FAILS**, with five unaccounted survivor
disappearances, all at `harness/write_rule.py:357-358`:

> "a survivor list that shrinks vs the previous run is only OK if every removed survivor was
> killed by a new/strengthened check or is carried under a debt ID — an unaccounted shrink is a
> FAIL"

**Cause: inserting `InvalidWriteState` near the top of `write_rule.py` shifted line numbers**, so
survivors recorded against `:357-358` no longer match. The mutation harness cannot tell a moved
line from a vanished one, and it is right to refuse the difference.

**A new BINDING FAILURE means the change does not land.** The patch is preserved; product code is
reverted to `a7807d8`.

## WHAT BILL MUST DECIDE

The survivors did not disappear — they moved. Resolving it is a ruling, not a session's call:
**re-record the survivor baseline** against the new line numbers, or **carry the five under a debt
ID**. The L7V2 selftest passed in the same run ("all four directions hold"), so the check itself
is sound.

## FIXTURE POLLUTION — REPORTED, NOT CLEANED

Anti-vacuity wrote **four real `medication` facts for `maya`** into the roadmap graph on 7688
(values `HA33-augment/supersede/correct/unresolved-<micro>`). They are fixture data in a dev
graph, left in place because deleting graph rows is not this dispatch's authority. **Named so
they are not mistaken for seeded state.**

## CLAIM IMPACT

**None.** No product change landed. The clause is a requirement statement, not evidence — the REQ
is **not** ruled MET and nothing is claimed for it.

## OPEN

- **The L7V2 survivor-baseline ruling** — the only thing blocking this fix.
- **The seven absences as standing tests** — executed, not yet codified.
- **Four fixture facts** on `maya`/`medication` in the 7688 graph.
