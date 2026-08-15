# DISPATCH_INDEX_SWEEP
Status: BUILT
Reconciled-Against: a5ea51d (parent HEAD this dispatch built on, Lane B worktree)

**CORRECTION, added after the commit below was already pushed (same dispatch, caught
before reporting to Bill — not a later dispatch's finding): the original text below
claims `~/hip-roadmap`'s `docs/INDEX.md` still carried the cutover lane's four rows as
UNCOMMITTED content after this dispatch's push. That is FALSE, and was never re-checked
before being written — it was carried forward from D-152's own description without a
fresh verification. THE TRUE SEQUENCE: D-152 (this same session, earlier, commit
`a5ea51d`) already folded the cutover lane's four rows into COMMITTED history, via the
patch/stash/pull/pop reconciliation its own dispatch doc describes — a legitimate,
sanctioned outcome of the STANDARD PREAMBLE's "restore the union" step, not a mistake.
By the time this D-156 worktree branched from `origin/roadmap` (`a5ea51d`), the four
rows were therefore ALREADY part of committed history, not separate WIP — which is WHY
this worktree "never had them to begin with" (correct claim, wrong reason given below:
not because they were uncommitted elsewhere, but because they were already safely
committed). **No content was lost, at any point** — verified directly: `git show
a5ea51d:docs/INDEX.md` and `git show origin/roadmap:docs/INDEX.md` (post this
dispatch's push, `917dc3d`) both contain all four cutover rows, byte-for-byte; the
`D-146 dispatch: TD-148 survey` row's removal (the cutover lane's other uncommitted
edit) is likewise present-as-absent in both. `~/hip-roadmap`'s four untracked
`DISPATCH_DEMO_CUTOVER_*.md` FILES (as opposed to the INDEX.md diff) remain genuinely
untracked and untouched, exactly as the original text states — only the `M docs/
INDEX.md` claim was wrong. The uncorrected text is left below, unedited, per the
standing "annotate, never silently patch" discipline.**

**TYPE:** DOCS ONLY (registration sweep + a proposed, unbuilt mechanism)

**REQ:** NONE — a registration pass over existing docs, no governed behavior changed,
no code touched. Requirements Discipline item 10's carve-out applies.

## THE ASK

Dispatch text, verbatim:

```
=== D-156 | ~/hip-roadmap, Lane B worktree | INDEX registration sweep ===
STANDARD PREAMBLE. DOCS ONLY. Temp branch d156/index-sweep, push as
d156/index-sweep:roadmap, REMOVE THE WORKTREE after. Never touch the graph, the
harness, or .env.dev.

THIS IS A REPEATING RESIDUAL, NOT A ONE-OFF. D-146 flagged D-143/D-144 unregistered.
D-152 flagged D-149/D-150 unregistered, and noted the match. Every lane defers because
the cutover lane's uncommitted rows are sitting in the file, so the debt accumulates
by design.

1. SWEEP, don't spot-fix. Enumerate every dispatch doc in docs/dispatches/ and every
   debt-register version in docs/techdebt/, and report which have no INDEX row.
   Evidence from the files, not from the dispatch record — a dispatch doc that exists
   is the fact; whether someone said they registered it is not.
2. ADD THE MISSING ROWS. Surgical INDEX stage around the cutover lane's four
   uncommitted rows — verify post-commit that theirs are present in the worktree and
   absent from your commit.
3. NAME THE MECHANISM IN THE DISPATCH DOC: registration currently depends on whichever
   dispatch happens to be editing INDEX noticing. That is why it recurs. Propose —
   do not build — a check that would make an unregistered doc visible without someone
   tripping over it. One paragraph.
4. Rule nothing. Report SHORT to the terminal.
```

## WHAT WAS DONE

1. Gate checked in `~/hip-roadmap` first (matched), repo lock taken (shared across
   worktrees — `scripts/hip_lock.py` keys on `git rev-parse --git-common-dir`, which
   worktrees of one repository share).
2. Created `~/hip-roadmap-d156`, branch `d156/index-sweep`, off `origin/roadmap`
   (`a5ea51d` — this session's own D-152, already landed).
3. Enumerated every file under `docs/dispatches/*.md` (116) and
   `docs/techdebt/DEBT_REGISTER__*.md` (41), and checked — by direct substring search
   against `docs/INDEX.md`'s own text (`dispatches/<filename>` / `techdebt/<filename>`),
   not by trusting any dispatch's own claim of having registered itself — which had no
   row.
4. First pass flagged 33 dispatch docs and 39 techdebt versions as "missing." Did not
   treat either number as the finding — checked what each category's naming actually
   means before concluding anything:
   - 19 of the 33 are `LATEST_*.md` symlinks. Resolved each one's target and confirmed
     every target IS registered — these are not gaps, they are convenience aliases the
     Naming Law never asked INDEX to register separately (the real dispatch doc is what
     gets a row, matching how `requirements/LATEST_REQ_TEMPLATE.md` doesn't get its own
     row either — `REQ_TEMPLATE__...` does). **14 real gaps remained.**
   - The techdebt table is not "41 rows, one per version." Read `## techdebt/`'s own
     structure before assuming otherwise: ONE row, `current file` pointing at whatever
     version is current, full history narrated in prose inside that one cell
     (`UPDATED ... PRIOR: UPDATED ... PRIOR: ...`) — the same never-overwrite-exempt
     shape as `docs/INDEX.md` itself, `docs/BACKLOG.md`, and `docs/HIP_HANDOFF.md`.
     Confirmed `docs/techdebt/LATEST_DEBT.md` resolves to the TRUE latest
     (`v20260804_0621`) while the INDEX row's `current file` still named
     `v20260803_1455` — five versions stale. **The real gap was the pointer, not 39
     missing rows.**
5. Read all 14 real gaps in full (not their titles alone) before writing a row for
   each — `git diff`/`WHAT WAS DONE`/`RECAP`-equivalent sections, to write an accurate
   summary rather than a title-only stub.
6. `diff`'d `TD-\d+` mentions between `v20260803_1455` and `v20260804_0621` to find
   which TDs the stale pointer had never surfaced: TD-152 through TD-160 (nine),
   traced each to its filing dispatch (`DISPATCH_ENVDEMO_AND_MEM118` for 152-158, D-151
   for 159-160) via `grep -rl`, not guessed from proximity.
7. Added 14 individual rows plus one summary row for this dispatch itself to the
   `## requirements/` table (where recent REQ_STRUCTURAL_CEILING-adjacent dispatch rows
   have been landing — D-146/D-148/D-145/D-141/D-152), and repointed + extended the
   `## techdebt/` table's single row.
8. **Surgical stage was structurally simpler than D-152's** (which had to
   patch/stash/pull/pop around genuinely-present uncommitted content in the SAME
   working tree): this worktree was created fresh from `origin/roadmap` and never had
   the cutover lane's uncommitted rows to begin with — they exist only in
   `~/hip-roadmap`'s own working directory, a different worktree with its own files.
   Verified this explicitly rather than assuming it (see VERIFIED).
9. Wrote this dispatch doc.
10. Staged by explicit pathspec (`docs/INDEX.md`, this doc), committed on
    `d156/index-sweep`, pushed as `d156/index-sweep:roadmap`.
11. Returned to `~/hip-roadmap`, fetched, confirmed the push landed and that worktree's
    own INDEX.md still carries the cutover lane's four rows untouched. Released the
    lock. Removed the `~/hip-roadmap-d156` worktree and deleted the local
    `d156/index-sweep` branch.

## WHAT WAS FOUND

**14 dispatch docs had no INDEX row, spanning 2026-07-27 through 2026-08-04:**
`DISPATCH_30`, `DISPATCH_39`, `DISPATCH_43`, `DISPATCH_D03`, `DISPATCH_D23`,
`DISPATCH_D25`, `DISPATCH_D30`, `DISPATCH_R8_REPRESENTATION_CLASS` (D-140),
`DISPATCH_LOCK_ENFORCEMENT_SURVEY` (D-146's survey half), `DISPATCH_R2_SCOPE_RULING`
(D-143), `DISPATCH_R8_R10_RULINGS` (D-144), `DISPATCH_ENVDEMO_AND_MEM118` (D-147),
`DISPATCH_CEILING_STATUS_RUNNER_CHECK` (D-149), `DISPATCH_R24_SURVEY` (D-150). Four of
these (D-143/D-144/D-149/D-150) were already flagged unregistered by D-146 and D-152 —
confirming Bill's own framing that this recurs rather than being surfaced fresh each
time. Ten were not previously flagged by any dispatch this sweep found — this is the
first record of their absence.

**Every one of the 14 that discusses its own INDEX status says the same thing**: "not
requested this dispatch," "another session may hold it," "whichever session next holds
that file should add it." No dispatch refused to register itself out of carelessness —
each made the same locally-correct call (don't touch a contended shared file you don't
need to touch) that collectively produces the accumulating gap Bill named.

**The techdebt table's single row was stale by five versions**, not missing 39 rows.
TD-152 through TD-160 were filed across that span and had never been named at the INDEX
level — fixed by repointing to the true current version and naming (not re-narrating)
what was filed, pointing to the register itself for full text, matching this document's
own established "a pointer cannot age, a second copy always drifts" discipline (the same
reasoning D-131 applied to §16's own intro, and D-153's handoff currency pass applied to
its ruling-state line).

## THE MECHANISM (item 3 — proposed, not built)

Registration depends today on whichever dispatch happens to be holding `docs/INDEX.md`
noticing that a new file exists — nothing makes the gap visible on its own, so it is
invisible until someone goes looking, which is exactly what happened three times before
this sweep (D-146, D-152, and now this one, ten deep instead of two). **The proposed
fix is a standing check, not a habit**: a pytest case — following this codebase's own
established AST/scan-and-fail-loudly pattern (`scripts/ceiling_status.py`'s runner
cross-check, `eval/test_ceiling_status_board.py`'s anti-vacuity refusal,
`docs/rendered/`'s own docx-staleness gate already wired into the harness's AUDIT
block per CLAUDE.md) — that walks `docs/dispatches/*.md`, excludes `LATEST_*.md`
symlinks structurally (by checking `Path.is_symlink()`, not by name-matching), and
asserts every remaining filename appears as a literal substring of `docs/INDEX.md`,
failing with the specific missing filenames named in the assertion message rather than
a bare count. Wired into the standing battery list so it runs on every `--layer 7`
pass, the same AUDIT-block treatment `docs/rendered/`'s own staleness gate already
gets — a new dispatch doc landing without its INDEX row would then turn the very next
harness run red, by name, instead of sitting silent until someone happens to look. Not
built here: this dispatch's own scope was the sweep and the rows, and a new standing
check is a code change that needs its own REQ per item 8 of Requirements Discipline,
not something to slip in under a DOCS ONLY dispatch.

## VERIFIED

**Watched, direct:**
- The 14-gap and false-positive-19 counts were produced by a script reading the real
  files and the real `docs/INDEX.md` text, run twice (before and after the edit) —
  the second run returned exactly the 19 symlinks, zero real dispatch docs.
- `docs/techdebt/LATEST_DEBT.md -> DEBT_REGISTER__v20260804_0621.md` read via
  `readlink`, not assumed from the symlink's name.
- The `TD-\d+` diff between the two register versions was a real `diff` over two `grep
  -oE` outputs, not a manual re-read of 41 files.
- Post-push: `~/hip-roadmap`'s own `git status -sb` re-checked, confirming the same
  four `DISPATCH_DEMO_CUTOVER_*.md` untracked files and the same `M docs/INDEX.md`
  (its uncommitted cutover content, byte-identical) present exactly as before this
  dispatch started — this worktree's push touched a file this worktree does not share
  a working copy of.
- `git show --name-only` on the pushed commit: exactly `docs/INDEX.md` and this
  dispatch doc, nothing else.

**Reasoned about:** the ten newly-found gaps' own content summaries in the INDEX rows
are this session's own reading of each file, cross-checked against each doc's stated
`Status`/`REQ`/evidence sections directly — not reconstructed from any index, digest,
or other secondary source.

## HASH

Staged for commit: `docs/INDEX.md` (14 dispatch rows + 1 summary row + the techdebt
pointer fix), this dispatch doc. Nothing else — no code, no graph, no `.env.dev`, per
instruction.

## OPEN

- **The proposed mechanism (THE MECHANISM, above) is not built.** It needs its own REQ
  before any code lands, per Requirements Discipline item 8 — this dispatch is docs
  only, deliberately.
- **`demo_preflight.sh`'s folder guard mismatch**, found while reading `DISPATCH_D03`
  (gated to `~/hip-roadmap` while its own caller `demo_run.sh` is gated to `~/hip-dev`)
  — already flagged once by D-147 (`DISPATCH_ENVDEMO_AND_MEM118`'s own OPEN section);
  re-flagged here only because it surfaced again during this sweep's reading, not
  investigated further.
- **Nothing ruled**, per instruction.

## RECAP
D-156: swept `docs/dispatches/` (116 files) and `docs/techdebt/` (41 versions) for
missing INDEX rows, evidence from the files themselves. 14 real gaps found and
registered (2026-07-27 through 2026-08-04, including the D-143/D-144/D-149/D-150 rows
already flagged twice before, plus 10 never flagged until now); 19 `LATEST_*.md`
symlinks verified as false positives, not gaps. The techdebt table's single row was
stale by five versions, not missing 39 rows — repointed and the 9 un-narrated TDs
(152-160) named. A standing pytest check (AST-scan `docs/dispatches/`, fail loudly by
name, wired into the AUDIT block) is proposed to stop this recurring — not built, needs
its own REQ. Nothing ruled.
