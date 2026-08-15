# DISPATCH_ENACT_THREE_RULINGS
Status: BUILT
Reconciled-Against: `roadmap` at **`c5d5651`** (2026-08-05). Branched from `19c8f28`;
`origin/roadmap` had not moved, so this landed as a fast-forward — verified
`19c8f28..HEAD` contains exactly one commit and no passenger (STANDARD PREAMBLE item 8).

**TYPE:** PROCESS (docs + one `docs/INDEX.md` header rename). **No code changed.**

**REQ:** NONE — this dispatch enacts three of Bill's rulings into existing records. It builds
nothing. C9's ruling lands *in* `REQ_DEMO_CUTOVER`, which is the record, not a REQ this
dispatch serves.

**COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING**

## THE ASK

> === D-R-191 | ~/hip-roadmap, Lane B worktree | Enact three rulings ===
> STANDARD PREAMBLE. DOCS + one header edit. Temp branch, remove worktree after.
>
> 1. RULE C9, Bill 2026-08-05: PASSED ON THE LEAK GATE (0 leaks vs 6), with the limit
>    written into the ruling text: the leak gate does not measure structural refusal —
>    the rate sat at 26/350 across three builds while leaks went 10 -> 2 -> 0, so a
>    build can clear this gate without refusing structurally once more. The
>    structural-rate gate stays OPEN, threshold unset, until the
>    REQ_UNRESOLVED_SUBJECT_GUARD fix lands and the achievable rate is measured.
> 2. TD-R-164: RESOLVED, Bill 2026-08-05 — the deferred sweep completed at D-R-190,
>    54 rows, per-row evidence on file. Addendum, original kept. Fix its own broken row
>    (13 unescaped columns) while touching it.
> 3. TD-R-165: Bill rules RENAME ONE HEADER — the WP/NDA package table (line ~464)
>    gets a distinct name (## deliverables-packages/ or similar); the memo table keeps
>    ## deliverables/. Update the ~36 dependent rows' anchor expectations if any
>    reference the renamed header. Verify both sections resolve uniquely after.
> 4. Rule nothing else. Report SHORT.

## 1 — C9 RULED

Recorded **in place** in `docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260804_1939.md`
(the LATEST version), following D-R-183's precedent for recording a ruling into an existing
REQ — `57e3f51` edited `REQ_STRUCTURAL_CEILING`'s live file rather than cutting a new version,
because a ruling is an addition to the record, not a new thought superseding it.

Two edits: a new **"C9 — RULED"** section near the top, and a pointer at C9's own
`THRESHOLD: OPEN` paragraph so a reader landing there cannot miss it. The amendment's
`C9 IS NOT RULED BY THIS AMENDMENT` line is **annotated as superseded, not deleted**
(pre-authorized correction class).

**The numbers were verified against the evidence before being written into a ruling**, not
copied from the dispatch text:

| run (`docs/testing/`, `demo-cutover-build`) | leaks | structural |
|---|---|---|
| `PROBE_400_RECONCILED__…__v20260804_1930.md` | 10 | 26 = 24 `empty_set` + 2 `access_control` |
| `PROBE_400_RERUN_FIXED_BUILD__…__v20260805_1350.md` | 2 (B044, B092) | 26 of 350 = 7.43% |
| `PROBE_400_RERUN_AFTER_QUESTION_FIX__…__v20260805_1445.md` | 0 | 26 of 350 = 7.43%, third run running |

`Status:` stays **NOT MET** — C9 is one of C1–C10, and item 4 said rule nothing else.

**Recorded, not resolved:** the document carries two denominators for the same rate — the gate
text says **322**, the probe runs report against **350**. The ruling names neither as correct;
the discrepancy is written down rather than quietly picked between.

## 2 — TD-R-164 RESOLVED

New register version `docs/techdebt/DEBT_REGISTER__v20260805_1722.md`, `LATEST_DEBT.md`
repointed. **The original issue text is unaltered**; the resolution is an addendum in the
status cell.

**The sweep was re-verified independently, not taken on D-R-190's word** — walking
`docs/INDEX.md`'s own `## ` headers: the `requirements/` table holds **65 rows, 0 of which
point at a `dispatches/` file**; `dispatches/` holds 115.

**The broken row is repaired.** It carried **8 unescaped `|` characters** inside its issue
cell — two backticked table-header quotations — rendering as **13 columns in a 5-column
table**. Now 5.

## 3 — TD-R-165 RESOLVED, shape (a)

`docs/INDEX.md` line 471 renamed **`## deliverables/` → `## deliverables-packages/`** (the
WP/NDA docx/xlsx package table). The engineering-memo table at line 57 keeps
`## deliverables/`. The renamed section carries an in-file note recording what it was, why,
and that **no folder was added** — CLAUDE.md's LOCKED folder list is untouched and both
sections still describe files under `docs/deliverables/`; the header now names the TABLE.

**Dependent rows: NONE required updating — verified, not assumed.** The two tables hold 19
rows each (38; the ruling's "~36"). No row in either table references the header string in any
cell. Every reference to the literal `## deliverables/` in the repo is PROSE describing the
defect — this register and
`dispatches/DISPATCH_MISFILED_INDEX_ROWS_SWEEP__…__v20260805_1629.md`. That dispatch doc is
history and was **left unaltered**.

**Uniqueness verified after the edit:**

```
total '## ' headers: 19        DUPLICATE headers: NONE
  '## deliverables/'          -> line  57   UNIQUE
  '## deliverables-packages/' -> line 471   UNIQUE
  prefix trap: none — 'deliverables-packages/' does not begin with 'deliverables/'
```

Zero duplicate headers anywhere in the file, not merely in this pair.

## FINDINGS — found here, deliberately NOT acted on (item 4)

1. **The mirror image of TD-R-164 exists.** One REQ row sits in the `dispatches/` table:
   `requirements/REQ_CHECKLIST_GENERATION__td133-item1-template-metamorphic-expansion__v20260726_1226.md`,
   subject *"CheckList-style template metamorphic expansion"*. TD-R-164's scope is
   dispatch-rows-in-`requirements/`, so this does not block its resolution — but it is the
   same defect running the other way, and it is recorded in the register so the sweep's
   "0 remaining" is not read as "the table is clean in both directions."
2. **Three older register rows carry a stray unescaped pipe each** — TD-134, TD-143, TD-144,
   each rendering 6 columns in a 5-column table. Same class as the row this dispatch was told
   to fix; left untouched because the instruction named TD-R-164's row specifically.

## VERIFIED

**Watched run:** the header-uniqueness scan over the committed file; the column-count scan
over every register row (before and after); the `requirements/`/`dispatches/` row-and-file-column
walk; the repo-wide grep for the literal header; the per-run leak/structural figures read out
of the three probe docs on `demo-cutover-build`.

**Corrected mid-dispatch:** an initial column count using `awk -F'|' NF` flagged TD-R-165's row
as malformed too. It is not — that count cannot distinguish `\|` from `|`, and TD-R-165 is
correctly escaped (16 raw pipes, 6 unescaped). Re-counted with a negative-lookbehind before any
edit; only TD-R-164 was broken, exactly as the dispatch said.

**Not done:** no code, no test, no harness run — this dispatch changes no behaviour, so none
was warranted. No probe was re-fired; C9's figures are read from the runs on file.

## OPEN — Bill's

- The **structural-rate gate threshold** remains unset, by this ruling's own terms.
- The **322 vs 350** denominator discrepancy in `REQ_DEMO_CUTOVER`.
- The two findings above.

Nothing else ruled. Nothing marked MET.

---

**D-R-191: C9 RULED — passed on the leak gate, 0 vs 6, with its limit written into the ruling
text and the structural-rate gate explicitly left OPEN at an unset threshold. TD-R-164 RESOLVED
with the sweep re-verified independently (requirements/ = 65 rows, 0 misfiled) and its own
13-column row repaired. TD-R-165 RESOLVED by rename — `## deliverables-packages/` for the
WP/NDA package table, `## deliverables/` kept for memos, all 19 headers now distinct, zero
dependent rows needing an update. Two findings reported and deliberately not acted on. No code
changed; nothing else ruled.**
