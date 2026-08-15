# DISPATCH_DOCS_BUNDLE_FOUR_FIXES
Status: BUILT
Reconciled-Against: 2026-08-05 (D-R-193; parent `2499216`)

**TYPE:** BUILD (DOCS ONLY — three files, no code, no graph, no harness, no test run.)

**REQ:** NONE — documentation corrections (Requirements Discipline item 10). Two of the three
enact records that already exist elsewhere (D-R-190's finding 2; Bill's 2026-08-05 denominator
ruling); the third is a rendering defect.

**Nothing ruled.** Item 4 of the ask, honoured literally: no REQ marked MET, no TD resolved, no
threshold set.

## THE ASK

```
=== D-R-193 | ~/hip-roadmap, Lane B worktree | Docs bundle: four small fixes ===
STANDARD PREAMBLE. DOCS ONLY. Temp branch, remove worktree after.
1. Move the REQ_CHECKLIST_GENERATION row from the dispatches table to requirements/ —
   the mirror image of the 54, annotated.
2. Fix the stray unescaped pipe in the TD-134, TD-143 and TD-144 rows.
3. In REQ_DEMO_CUTOVER: annotate the 322 denominator SUPERSEDED per Bill's ruling
   2026-08-05 — the rate denominator is 350, matching the banked probe runs. Original
   kept.
4. Rule nothing else. Report SHORT.
```

## 1. THE MIRROR-IMAGE ROW — moved, annotated

`docs/INDEX.md`. One row whose file cell reads
`requirements/REQ_CHECKLIST_GENERATION__td133-item1-template-metamorphic-expansion__v20260726_1226.md`
sat inside the **`dispatches/`** table (pre-edit line 192). Moved to the `requirements/`
table, anchored on the `## requirements/` section header per CLAUDE.md Workflow item 3,
inserted at the top of that table with the other newest rows. Row text otherwise unchanged;
one annotation appended to its own last cell naming the move, the dispatch, and why it is
worth a line: **TD-R-164's ambiguous anchor cut in both directions.** D-R-190 swept 54 rows
one way; this is the one that went the other way, and a sweep of the 54 alone would have left
the category still mixed.

Counts, verified either side: `dispatches/` **116 → 115** rows, `requirements/` **65 → 66**.
Every other section unchanged. **D-R-190's annotation still reads true** — the row removed sat
*above* that dispatch's appended block, so "the last 54 rows of this table were moved in from
`requirements/`" is still an accurate description of the last 54 rows (asserted in the edit
script, not eyeballed).

## 2. THREE STRAY UNESCAPED PIPES — fixed, and nothing else in those rows touched

`docs/techdebt/DEBT_REGISTER__v20260805_1722.md` (the live register, reached through
`LATEST_DEBT.md`). A normal row in this table has **6 unescaped pipes**. Three had 7, so
markdown split the notes cell in two and rendered each row with a spurious extra column:

| row | the stray pipe | inside |
|---|---|---|
| TD-134 | `only \`None\`/\`""\` are possible for a \`str  \|  None\`-typed input` | an inline type union |
| TD-143 | `` `sam→ray/allergy [not-exists\|direct]` `` | an inline case label |
| TD-144 | `` `sam→dad/medication [exists-cross-member\|plural]` `` | an inline case label |

Each is now `\|`. **Backticks do not protect a pipe inside a markdown table** — that is why
all three survived review as "already in code spans".

The fix is asserted, not asserted-to: for each row the script checks that the repaired line is
byte-identical to the original once every pipe is normalised, i.e. **the only change is the
backslash**. No wording, no status, no ID, no date moved.

**Edited in place rather than cutting a new register version.** The register's own rule is
"one running register … when this file changes materially, cut a new timestamped version." A
rendering repair that provably changes no content is not a material change, and cutting a
version for it would put a second file in the lineage whose only difference is three
backslashes. Stated here so the choice is visible and reversible rather than assumed.

## 3. THE 322 DENOMINATOR — annotated SUPERSEDED, original kept

`docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260804_1939.md` (the
`LATEST_REQ_DEMO_CUTOVER` target). This document asserts the 322 denominator in **four**
places; all four are annotated and **not one character of the original is removed**:

| site | treatment |
|---|---|
| `### 4. THE DENOMINATOR IS 322, NOT 400` | a `> SUPERSEDED 2026-08-05 (D-R-193)` block directly under the heading, above the untouched original |
| the "does not reconcile the two denominators" paragraph | `RECONCILED 2026-08-05 (D-R-193)` sentence appended — the paragraph that recorded the discrepancy as open is the reason a ruling was possible, so it stays as written |
| `**DENOMINATOR: 322, not 400.**` (acceptance section) | inline `*(SUPERSEDED … ruled 350)*` |
| "the real denominator for rate purposes is **322, not 400**" | inline `*(SUPERSEDED … ruled 350)*` |

**What the annotation says, and deliberately does not say.** Superseded is the choice of
denominator *for rate purposes*. The derivation (400 − 50 guest − 19 PARK-OR-REFUSE − 9
OWNER-DEPENDENT = 322) stays on the record, and so does the decision **not** to cut the 50
unrunnable guest rows — the ruling disturbs neither, and reading it as authority to cut rows
would be reading in something Bill did not say.

Post-conditions asserted: four annotation sites present, every original occurrence of `322`
still in the file, and no in-place rewrite of `322` to `350` anywhere.

## VERIFICATION

The whole bundle ran as one script with 17 assertions, dry-run first against a
`git archive HEAD` export (all pass) before it was allowed near the worktree. The three files
are the only ones touched.

## HASH

`fa753a1` — made on Lane B worktree branch `d193/docs-bundle`, fast-forwarded onto `roadmap` and pushed to `origin/roadmap` inside the same locked run. Filled in by a same-session follow-up edit after the commit landed, per the established convention. Contains four files: `docs/INDEX.md`, `docs/techdebt/DEBT_REGISTER__v20260805_1722.md`, `docs/requirements/REQ_DEMO_CUTOVER__…__v20260804_1939.md`, and this dispatch doc.

## WHAT WAS NOT DONE

- **Nothing ruled** (item 4). TD-134 stays OPEN, TD-143/TD-144 keep the resolution states they
  already carried, no REQ marked MET, C9 untouched.
- **The 350 ruling is recorded, not applied**: no rate anywhere in the repo was recomputed, and
  no other document that cites 322 was hunted down — this dispatch names one file because the
  ask named one file.
- **`REQ_DEMO_CUTOVER`'s prior version (`v20260802_1205`) is untouched**, annotation or
  otherwise.
