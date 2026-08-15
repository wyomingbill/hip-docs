# DISPATCH_R11_MET
Status: BUILT
Reconciled-Against: 2026-08-05 (D-R-178; parent `1fe90a1`)

**TYPE:** RULING-RECORD + REGISTER ADDENDUM (docs only; no code, no graph, no harness)

**REQ:** `REQ_STRUCTURAL_CEILING`, R11 — the subject of the ruling being recorded.
Nothing built. Nothing self-ruled.

## 1. R11 RECORDED MET (Bill's ruling, 2026-08-05)

New §16 entry, placed newest-first ahead of R29 so the board's first-per-requirement parse
reads it as current. It records the **sequence**, per the dispatch, rather than just the
verdict:

- **HELD** (2026-08-05 morning) — not on R11's control, which has been built and passing
  since D-87, but on TD-136: household-owned facts start at maximum width, so proving
  nothing WIDENS says nothing about what is BORN wide.
- **ANSWERED** (D-R-174, read-only survey, same day) — `write_rule.classify` carried two
  household-producing rules twelve lines apart with opposite discipline. Level-2's
  `share_household` directive gated on `subj is None or subj == author`; Level-3a did not.
  The same author was refused an explicit request to share a fact about another person and
  granted the identical widening when the extractor happened to label the attribute
  `household`.
- **CLOSED** (D-R-176, `c1538d2`, same day) — rule 3a now carries the directive path's gate
  on **both** triggers, including the `author == "household"` pseudo-owner trigger that D8's
  known collision actually reaches; blocked writes fall through to 3b/3c.

**The ground recorded for MET is therefore not "the control passes"** — it passed all along
— **but that the question the hold existed for is answered and the asymmetry it exposed is
closed.** Evidence at ruling time: `eval/test_ceiling_audience.py` 16 passed / 2 xfailed,
verified in this dispatch. Residues explicitly excluded from the ruling and left on their own
entries: TD-149 and TD-160.

## 2. THE §16 SPLIT AND HEADER PREAMBLE — NOT UPDATED, AND WHY

**There is no split or enumeration to update. Both were deliberately deleted at D-131 by
Bill's own ruling, and re-creating one here would silently reverse it.** CLAUDE.md's Workflow
item 5 is explicit — *on conflict with this law, flag it and follow the law, do not bypass* —
so this is flagged rather than done.

What stands today, verified in the file before writing anything:

> **Status:** FILED. **Rulings are recorded per-requirement in section 16, the sole
> authoritative record. This header deliberately carries no count and no enumeration.**
> (D-131, Bill's ruling, 2026-08-03 — shape (i), the pointer…)

D-131's recorded reason was that the count went stale five times in five weeks — D-88, D-92,
D-100, D-120, and D-129's own re-count — so "the at-a-glance summary it cost is a summary
nobody could trust." Writing `MET R1, R11, R12, R18, R29, R30` into the header would restore
exactly that artefact, and would be wrong within a day of the next ruling.

**The instruction's intent is already satisfied without it:** R11's MET status now lives in
§16 as a per-requirement entry, which is where the pointer says rulings live, and
`docs/status/CEILING_STATUS.html` derives and renders the full MET set on every run —
including R11 from this commit forward. If Bill wants the enumeration back in the header, that
is a reversal of D-131 and should be ruled as one.

## 3. TD-160 ADDENDUM (Bill authorized)

Two lines appended to the existing entry, original kept intact. Verified by live registry
probe rather than inferred:

```
ray        known_subject_ids=True   is_recognized_recipient=True
dad        known_subject_ids=False  is_recognized_recipient=False
household  known_subject_ids=False  is_recognized_recipient=False
elena      known_subject_ids=False  is_recognized_recipient=False
```

Recorded as: **the inconsistency is WITHIN the fixture** — two care recipients built
differently, every identity-keyed check treating them differently — **not a uniform
enrollment gap**. That is a sharper statement of the defect than "dad is not enrolled",
because it locates the problem in the fixture's own inconsistency rather than in a missing
step.

Register cut as `v20260805_0934` from `v20260804_2104`, LATEST repointed, per the register's
own rule that a material change cuts a new version. Noted for the record: D-R-176 edited the
prior version in place rather than bumping; this dispatch follows the stated rule.

## PROCESS NOTES

- STANDARD PREAMBLE observed; machine gate passed (`bill-ai` / `[REDACTED-MACHINE-NAME]`
  / `~/hip-roadmap` / `roadmap`, in sync with origin).
- Docs only — no code, no graph, no harness run. The A11 suite was executed read-only to
  verify the evidence cited in the ruling.
- **D-R-174 has no dispatch doc** — it was a read-only survey reported to the terminal. The
  §16 entry cites it by number for the finding and cites D-R-176's committed doc and hash for
  the fix, so the chain is traceable without inventing an artefact.

## OPEN

- Whether the header enumeration returns is a reversal of D-131 and Bill's to rule.
- TD-149 and TD-160 remain open on their own entries; R11's ruling does not reach them.
- Nothing else ruled.
