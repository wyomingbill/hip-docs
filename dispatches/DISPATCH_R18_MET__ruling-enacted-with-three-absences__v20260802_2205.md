# DISPATCH_R18_MET
Status: BUILT
Reconciled-Against: 2026-08-02 (D-113; parent 5b3dc3b at dispatch time)

**TYPE:** PROCESS (two rulings enacted: R18 MET recorded in section 16
verbatim; TD-139's status column replaced with Bill's wording. Doc/register
edits only — zero code changed, zero behaviour changed.)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
— this dispatch CREATES that version, recording Bill's 2026-08-02 R18 MET
ruling. The ruling is Bill's, quoted verbatim in section 16 and in THE ASK
below; nothing here is self-ruled.

## THE ASK

> RULING, Bill, 2026-08-02: R18 IS MET, with three absences recorded in the
> ruling itself.
>
> Ruling text for section 16:
>
>   R18 is MET on the amended operative rule: when a source fact is
>   retracted, its derived children are invalidated. Built and live-proven —
>   D-81's in-transaction cascade to a fixpoint, A18 LIVE and passing with
>   its fault twin, and D-107's live proof that retracting D4 closed the
>   seeded derived child with closed_by='lineage_cascade'. The lineage gate
>   refuses derived writes missing the implemented block, and the seed goes
>   through it.
>
>   MET WITH THREE ABSENCES RECORDED, not conditioned away:
>   (a) Three of eleven lineage fields are absent — purpose_id,
>       retention_deadline, policy_version. Unpopulatable honestly until
>       R23's purpose vocabulary, R21's retention mechanism, and a real
>       policy version exist. Absence held by a standing test. R18 is MET on
>       what it can honestly require; it does not claim those three.
>   (b) "Erase by storage class" holds only in the weak
>       closed-from-retrieval sense.
>   (c) The 12 pre-lineage facts have no ruling for durable, non-reseeded
>       graphs. TD-139's backfill question stays open; R18's MET does not
>       close it.
>
>   WHY MET WITH THREE FIELDS ABSENT: holding R18 open until R21 and R23
>   build would make it hostage to unscheduled requirements. The operative
>   rule is complete and proven; the absent fields are blocked elsewhere,
>   honestly recorded, and tested for. Same shape as R30's MET with its
>   named limitation.
>
> TD-139 STATUS COLUMN, Bill's wording:
>   "PARTIALLY CLOSED (D-105). Eight of eleven fields implemented. Three —
>   purpose_id, retention_deadline, policy_version — absent, blocked on
>   R23's purpose vocabulary, R21's retention mechanism, and a real policy
>   version. Absence asserted by a standing test. The pre-lineage backfill
>   question for durable graphs is unruled."
>
> ALSO: update the MET / NOT-MET split in the REQ preamble in the same edit.
> RUN: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17,
> failures a subset of {115,116,117,118}. 15/17 is the ceiling; 16/17 is a
> STOP. Rule nothing else MET. Lock, commit with explicit pathspecs, push.

## WHAT WAS DONE

1. Machine gate verified (previous turn, D-113 arrived truncated — STOPPED
   and asked rather than enacting a MET ruling from a title; full text then
   supplied). Cutover lane's WIP present (three dispatch docs + three INDEX
   rows, uncommitted) — committed AROUND, explicit pathspecs + surgical
   INDEX stage. `.hip-lock` free → taken → released.
2. REQ cut as new version v20260802_2205 (Naming Law): section 16 gains the
   **R18 — MET (D-113)** block with the ruling text VERBATIM; the D-111
   amendment block re-marked historical (its "status NOT re-ruled" was true
   at its date and is now superseded); the D-111 evidence-both-ways framing
   is retained inside the historical blocks as the record of what the
   ruling weighed. Preamble split RE-COUNTED in the same edit, per the ask —
   and the count fixed a second staleness while there: the header claimed
   "THREE ARE RULED / 27 not run", stale against D-100's R1 MET + R10 NOT
   MET. It now reads **FIVE ruled (R1, R18, R29, R30 MET; R10 NOT MET) / 25
   not run**. Version/Filed lines updated; LATEST symlink repointed.
3. Register cut as v20260802_2205: TD-139's status column is now Bill's
   wording VERBATIM (the D-111-flagged column-vs-entry discrepancy is
   resolved by ruling, not by my paraphrase); a short historical note added
   where the entry's old text said R18 "must NOT be ruled MET on D-81
   alone" (it was ruled MET on far more than D-81 alone); header note
   prepended; LATEST_DEBT repointed.
4. Full evidence run (below). Nothing else ruled.

## VERIFIED

**Watched run (read individually from the logs, this dispatch):**
- 19 batteries: **297 passed / 1 skipped / 8 xfailed**
- **AUDIT 8/8 · DISC 1/1 · L7 27/27 · L7V2 27/28** (1 opt-in skip:
  CT-OUTPUT-GAP) · SCHEMA 1/1 · VOICE 1/1
- **RATCHET PASS · COVERAGE-GRID-RATCHET PASS · 0 scenario FAILs**
- ABSOLUTE individually: **OB6 · G0 · PSA1 · CTX-STRIP · LI1 — all PASS**
- **Mutation self-test finds its mutant at `injection_contract.py:664`**,
  both directions
- **Memory harness: 15/17, failing exactly {MEM-115, MEM-116}** — inside
  the D-109 pin (13-15/17, subset of the four), at D-110's structural
  ceiling. **Not 16/17 — the STOP did not fire.**

**Reasoned about:** none of substance — this dispatch is transcription of
Bill's rulings plus a re-count; the re-count was verified against section
16's actual blocks (grep of `### R\d+ — **` headings), not from memory.

## HASH

Committed this session on `roadmap` (D-113); parent 5b3dc3b.

## OPEN

- The three absent lineage fields land when R23 (purpose vocabulary) and
  R21 (retention) build, plus a real policy version — each through its own
  REQ; the standing test that asserts their absence is retired deliberately
  at that moment, per its own docstring.
- The pre-lineage backfill question for durable graphs — explicitly NOT
  closed by R18's MET, per clause (c) of the ruling.
- R10 remains the ceiling REQ's one NOT MET ruling (blocked behind A2/A8);
  25 of 30 requirements still have acceptance not run.
