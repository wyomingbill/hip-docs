# DISPATCH_CEILING_STATUS_BOARD
Status: BUILT
Reconciled-Against: 2026-08-04 (D-148; parent `dcb109d`)

**TYPE:** BUILD (tooling + generated artifact)

**REQ:** NONE for the tool itself — it is a reporting surface over
`REQ_STRUCTURAL_CEILING` and `REQ_CEILING_ACCEPTANCE`, changes no governed
behaviour, and rules nothing. The two documents it reads are its subject, not its
authority.

## WHAT WAS BUILT

`scripts/ceiling_status.py` → `docs/status/CEILING_STATUS.html` (matrix of all 30
requirements grouped by axis, colour-coded, with counts and an acceptance-row
summary) and an appended snapshot row in `docs/status/CEILING_HISTORY.csv`.

**Every status is DERIVED. There is no hardcoded status list**, and a battery case
asserts there never will be: `test_board_carries_no_hardcoded_status_map` fails on
any literal mapping a requirement id to a status. That constraint is the whole
point — a board with its own copy of the truth is a second place for it to drift,
and this project paid five times for exactly that (D-88, D-92, D-100, D-120,
D-129; the count was killed at D-131).

| fact | derived from |
|---|---|
| requirement + axis | ceiling REQ body headings `### R<n> — <title>` under `## <n>. AXIS …`, taken BEFORE §16 |
| ruling status | §16's `### R<n> — **<STATUS>**` entries, FIRST per requirement wins (§16 is newest-first and marks superseded entries `(historical`) |
| acceptance tier | the acceptance REQ's "Tier counts" table, by ENUMERATING the ids each cell lists — never by its stated count |
| blocked-on-a-person | the UNWRITABLE table's authorization column, where it names a person (ethicist, attorney) rather than a build |

**UNDETERMINED is a real, counted outcome, not a fallback bucket.** An
unrecognised §16 status renders UNDETERMINED and appears in the chips and the
CSV; the board says so on its face rather than flattering the number.

## CURRENT READING (2026-08-04, `dcb109d`)

**MET 5 · RULED NOT MET 3 · IN PROGRESS 8 · NOT STARTED 11 · BLOCKED ON A PERSON 3
· UNDETERMINED 0** — 30 accounted for, and the battery asserts the chips sum to the
matrix so a requirement cannot go missing between them.

Acceptance rows: **9 LIVE (gating) · 16 wired and running · 14 UNWRITABLE, never
written and therefore never run.** The board states on its face that a running row
is not a met requirement.

## WHAT THE BOARD FOUND IN THE DOCUMENTS — three defects, all mine, all from D-145

1. **Two malformed table rows.** The LIVE and UNWRITABLE rows of the Tier counts
   table were missing their closing `|`, so the first run parsed **zero tiers** and
   reported 14 UNDETERMINED. Fixed in the document; the parser was ALSO made
   tolerant of an unclosed row, because a status board that silently reports
   nothing because of a cosmetic markdown defect is worse than the defect.
2. **A count that disagreed with its own cell.** The LIVE row said `7` while
   enumerating nine ids. Corrected to `9`, with the reason recorded in the cell:
   the enumeration is the content, the count was the stale claim. The board reports
   any such disagreement rather than picking a winner — that reconciliation table
   is a permanent feature, not a one-off check.
3. **A parsing trap in the UNWRITABLE cell.** It named A2 and A8 as *removed from*
   the tier, so any reader — human or tool — enumerating that cell reads them back
   as UNWRITABLE. The ids are now de-enumerated and the departure described in
   words. (The board survived it only because document order happened to put LIVE
   first, which is luck, not design.)

## ACCEPTANCE — `eval/test_ceiling_status_board.py`, 11 cases, 25th standing battery

**Anti-vacuity is the centre, per the dispatch:** a scan finding zero requirements
**fails** — `derive()` raises `DeriveError` rather than emitting a page, and the
same guard covers a zero-tier parse (which would render "never run: 0", the most
reassuring possible lie). Demonstrated live, not only asserted:

```
refused: parsed ZERO requirements from the ceiling REQ — refusing to emit a board …
```

Also asserted: the parse sees all 30 real requirements each with an axis; the
counts account for every requirement in both directions; an unknown ruling is
UNDETERMINED and **reaches the counts** rather than vanishing; `(historical`
entries are skipped so R18 does not read NOT MET; tier enumeration is independent
of the stated count; `A3–A6` expands to four rows; and history is append-only with
one header and one row per run.

## HARNESS

- Battery 11/11. Standing batteries **415 passed, 8 xfailed** (up from 400).
- `--layer 7`: **L7 27/27**, AUDIT 8/8, four-part-roster PASS,
  COVERAGE-GRID-RATCHET PASS, **RATCHET PASS**.
- Six ABSOLUTE checks individually: **OB6 · G0 · PSA1 · CTX-STRIP · LI1 · CS1 — all
  PASS.**
- The run acquired `graph:7688` through D-146's lock, as the runner now requires.

## DISCLOSURE — I discarded two history rows, deliberately

The first two CSV rows were written by the pre-fix parser (the malformed-table run,
recording 14 UNDETERMINED and 0 LIVE). That is a fact about a **bug**, not about
the documents, and the CSV has no column in which to say so — it would have
rendered as a permanent trend spike that every future reader misreads. I deleted
the file and regenerated a single clean row **before the first commit**, so no
history of record was rewritten. Saying it here rather than letting the file imply
a clean lineage it does not have.

## GOVERNANCE

`docs/status/` is a NEW folder, and CLAUDE.md's Docs Organization list is LOCKED
("do not add folders without updating this file and INDEX.md"). Both updated in
this commit: the entry records that the folder is tool-written, never hand-edited,
and exempt from never-overwrite for the same reason INDEX/BACKLOG/LATEST_DEBT are —
a board whose job is to be current cannot be versioned per run, and the CSV carries
the history instead.

## PROCESS NOTES

- STANDARD PREAMBLE observed; lock read-first then noclobber **before any edit**
  (05:38:52), released after push. Repo `.env.dev` only.
- Committed AROUND the cutover lane's WIP: explicit pathspecs, surgical INDEX
  stage, verified after.

## OPEN

- The board reports the DOC's tier claim. It does not yet cross-check that a row
  claimed LIVE has a test that actually runs — the "classified but never wired"
  hazard from the 2026-08-03 digest. That is a genuine next step and deliberately
  not smuggled in here.
- Nothing ruled.
