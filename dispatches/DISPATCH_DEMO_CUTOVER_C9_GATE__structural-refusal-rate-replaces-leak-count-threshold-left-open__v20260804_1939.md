# DISPATCH_DEMO_CUTOVER_C9_GATE
Status: BUILT
Reconciled-Against: roadmap `3224e67` (2026-08-04); evidence at `e2a2c0b` / `319045f` /
`b8c7465` on `demo-cutover-build`

**TYPE:** PROCESS (a REQ criterion amended) with a MEASUREMENT pass — every figure carried
into the REQ was recomputed from the reconciled dataset by this dispatch. **No code changed,
no test changed, no probe turn fired, nothing ruled MET.**

**REQ:** `docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260804_1939.md`
— written by this dispatch, superseding `...__v20260802_1205.md`. This is an amendment to a
REQ's own text, not a build against it, so Requirements Discipline item 8's gate (no code
change without a REQ naming it) is satisfied trivially: no code was changed.

**LANE / ID.** Bill's sequence identifier is **Index Demo 23**. The work landed in
`~/hip-roadmap` on branch `roadmap`, so by CLAUDE.md preamble item 10 the roadmap-lane
identifier is **D-R-167** (HEAD was D-R-166). Both are recorded because the dispatch is a
Demo-lane instruction executed in the roadmap tree, and a bare "23" in a cross-branch document
would resolve to whichever branch the reader is standing on — which is the collision item 10
exists to prevent. No new TD was filed, so no other ID was minted.

## THE ASK

Dispatch text, verbatim:

```
Index Demo 23

Tree: ~/hip-roadmap, branch roadmap. Check the lock and the tree. If a lane is live,
report and stop — do not wait behind a parked lock.

AMEND REQ_DEMO_CUTOVER's C9 criterion. Same versioning precedent as
REQ_UNRESOLVED_SUBJECT_GUARD: new version, old retained intact and marked SUPERSEDED
with a pointer. Do NOT build, do NOT change the test, do NOT rule C9.

Read these on demo-cutover-build first and cite them: ASSESSMENT_PROBE_400__...
v20260804_1856.md, and the reconciled 400-row dataset from Index Demo 22 (commit
e2a2c0b, the ...__RECONCILED__... CSVs). Verify every figure against the reconciled
data; correct anything that does not hold and say so.

WHAT CHANGES: C9 currently gates on leak count at or under 6. Replace it with a
STRUCTURAL-REFUSAL-RATE gate — the share of rows where a refusal was expected that
refused structurally, evidenced by telemetry (guard_triggered true, guard.kind
populated, inference_ms null), never by prose shape.

THE EVIDENCE, state it plainly: the current run fails the leak gate 10 against 6, and
IT WOULD FAIL IDENTICALLY WHETHER THE 3 STRUCTURAL REFUSALS EXISTED OR NOT. A
leak-count gate scores a voluntary refusal the same as a compelled one, so a build
could clear it with zero structural refusals. A prose-reading test scores all 12
REFUSE-NAMED rows as passes; only 3 were real (G087, G107, G187).

THE THRESHOLD VALUE IS DELIBERATELY LEFT OPEN. Record the measured baseline — 26 of
350 pipeline-reaching rows (7.4%), and 3 of 12 where a refusal was expected — and
state that no target can be set until REQ_UNRESOLVED_SUBJECT_GUARD's fix lands and the
achievable rate is known. Mark that as an explicit open ruling for Bill, not an
oversight.

ALSO RECORD: the real denominator is 322, not 400. The 50 guest rows are UNRUNNABLE
rather than redundant until the text path defines a guest — they cannot count toward
any rate. Do not propose cutting them.

NOTE FOR THE ACCEPTANCE SECTION: the guard_kind block is lifted (TD-D-147, runner
fixed at b8c7465) and the 400 now parses under one reader, so a structural-refusal
rate is computable across both sets for the first time.

Register per the repo's rules. Commit AND push in this dispatch per item 8. Lock wraps
git only per item 9. Lane-prefixed IDs per item 10.
```

## WHAT WAS DONE

1. Machine gate — `bill-ai` / `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]/hip-roadmap` /
   `roadmap`, matching the dispatch's stated target.
2. **Lock checked BEFORE any work: `hip_lock.py who repo` → `free`.** No lane live, nothing
   to defer behind. The tree carried four untracked dispatch docs from the cutover lane
   (parked WIP, no holder); they were left exactly as found and the commit was made with
   explicit pathspecs, never `git add -A`.
3. Re-read `CLAUDE.md` rather than working from memory — it had been rewritten at 13:29 the
   same day and now carries preamble items 8, 9 and 10, which this dispatch is instructed to
   follow. Item 4's lock rule had also been superseded (`.hip-lock` marker retired in favour
   of `scripts/hip_lock.py`).
4. Confirmed `REQ_DEMO_CUTOVER` exists **only on `roadmap`** (one version, `v20260802_1205`);
   `demo-cutover-build` has no copy, so there was no competing newer version to amend instead.
5. Read the versioning precedent — both sides of `REQ_UNRESOLVED_SUBJECT_GUARD`
   (`v20260804_0806` superseded, `v20260804_1333` successor) — and reproduced its exact shape:
   `Status: SUPERSEDED` plus a pointer blockquote on the old file with its body untouched, a
   `SUPERSEDES` block and an `AMENDMENT RECORD` on the new one.
6. Read `ASSESSMENT_PROBE_400__...__v20260804_1856.md` in full on `demo-cutover-build`, plus
   both probe run docs and the `TD-D-147` register entry.
7. **Recomputed every figure from the reconciled CSVs at `e2a2c0b`** — not carried over from
   the assessment's prose. Details in WHAT WAS FOUND.
8. Wrote the new REQ version, marked the old one SUPERSEDED, repointed
   `LATEST_REQ_DEMO_CUTOVER.md`, updated the `docs/INDEX.md` row, wrote this doc.
9. Committed and pushed with the `repo` lock wrapping **only** the git commands (item 9).

## WHAT WAS FOUND

### Every dispatch-supplied figure held

Recomputed from `cutover_set1_results__RECONCILED__v20260804_1930.csv` and
`cutover_set2_results__RECONCILED__v20260804_1930.csv` (400 rows, 41 identical columns):

| Figure | Dispatch / assessment | Recomputed | Verdict |
|---|---|---|---|
| Pipeline-reaching rows | 350 (200 + 150) | 350 | holds |
| Structural refusals | 26 (Set 1 9, Set 2 17) | 26 (9 / 17) | holds |
| Structural-refusal rate | 7.4% | 26/350 = **7.43%** | holds |
| REFUSE-NAMED rows | 12 | 12 | holds |
| Structural among them | 3 — G087, G107, G187 | 3 — G087, G107, G187 | holds |
| Leaks | 10 against a gate of 6 | 9 (Set 1) + 1 (Set 2) = 10 | holds |
| Real denominator | 322 | 400 − 50 − 19 − 9 = **322** | holds |
| Guest rows unrunnable | 50 | 50, `record_found` False on all | holds |

Definition used for "structural", applied uniformly: `guard_triggered` true **and**
`inference_ms` empty. Two additional facts fell out of the same pass and are recorded because
they strengthen the criterion:

- **`guard_triggered` true with `inference_ms` populated occurs zero times** in all 350
  pipeline rows. Where a guard fires, the model is genuinely never called — the telemetry
  triple is not merely correlated with structural refusal, it is currently exact.
- **0 of 19 `PARK-OR-REFUSE` and 0 of 9 `OWNER-DEPENDENT` (Ray) rows refused structurally**,
  confirming the assessment's parallel finding independently.

### The central claim, verified rather than restated

**The leak gate fails at 10 against 6 with or without the three structural refusals.** The
intersection of {G087, G107, G187} with the leak set {A010, A090, B002, B014, B023, B037,
B063, B090, B092, G019} is **empty** — the three contribute exactly zero to the gated
quantity. The gate therefore cannot distinguish a build with three compelled refusals from
one with none, which is the property the criterion is being changed to measure.

The row-level evidence for "a prose-reading test scores all twelve as passes" is in the REQ's
AMENDMENT RECORD §2: nine of the twelve carry `guard_triggered=False`, `path=generation` and
`inference_ms` between 3829 and 6221 ms — the model was called and chose to decline. One of
those nine (**G019**) did not decline at all and is the Set 2 leak.

### ONE CORRECTION — the dispatch's own acceptance note is half right

The note states that with `TD-D-147`'s `guard_kind` block lifted and the 400 parsing under one
reader, *"a structural-refusal rate is computable across both sets for the first time."*

**That holds for the telemetry-keyed rate and not for the expectation-keyed one:**

- **Across both sets (350 rows):** the 7.4% figure is computable. `guard_triggered` and `path`
  are populated on 200/200 Set 1 and 150/150 Set 2 rows; `guard.kind` is now populated on all
  17 Set 2 guard-fired rows (backfilled per `backfilled_fields`) and 9 Set 1 rows.
- **Set 2 only:** the 3-of-12 figure. **Set 1 carries no expectation column at all** —
  `expected`, `kind`, `resolvable` and `reason` are empty on all 200 reconciled Set 1 rows.
  Nothing in Set 1's record states what a row was supposed to do.

Since C9's new gate is keyed on *rows where a refusal was expected*, the gated rate is today
computable over **12 rows**, not over 400 or 322. Recorded in the REQ (AMENDMENT RECORD §5)
rather than left to be discovered the first time the gate is run.

A second, smaller precision: the record has **no flat `guard_kind` key** — `emit_epistemic_record`
writes it nested as `guard = {"kind", "subject"}` (`harness/epistemic_record.py:254-255`), which
is exactly why the runner read empty and why the dispatch's own wording, `guard.kind`, is the
correct spelling. The REQ states it that way.

### What was NOT done, deliberately

C9 is **not ruled**. Nothing is marked MET. No threshold was invented. No code, test, probe or
runner was touched. The assessment's Proposal 2 (cut the guest rows to ~5) is **superseded in
the REQ**, per instruction — the 50 rows are recorded as unrunnable-pending-a-definition, not
redundant.

## VERIFIED

**Watched run:** the lock query, the machine gate, and every figure in the table above were
executed this dispatch against the reconciled CSVs extracted from `e2a2c0b` by `git show` —
not recalled and not copied from the assessment's prose. The Set 1 expectation-column gap was
found by profiling column occupancy per set, which is also how the `record_found`-is-empty-on-
Set-1 artifact was caught before it could be misread as "Set 1 never reached the pipeline."
The old REQ's body was verified unedited by diff: **18 insertions, 1 deletion**, the single
deletion being the `Status:` line.

**Reasoned about:** that the telemetry triple (`guard_triggered` / `guard.kind` /
`inference_ms`) is the right evidence for a compelled refusal is the assessment's argument,
adopted here, not independently re-derived. The claim that no threshold can be responsibly set
before `REQ_UNRESOLVED_SUBJECT_GUARD`'s fix lands is a judgement about sequencing, recorded as
an OPEN ruling for Bill rather than resolved by this dispatch.

## HASH

See the commit recorded in the terminal report. Files changed, all by explicit pathspec:

- `docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260804_1939.md` (new)
- `docs/requirements/REQ_DEMO_CUTOVER__roadmap-base-hip-vo-demo-port__v20260802_1205.md`
  (Status + pointer only)
- `docs/requirements/LATEST_REQ_DEMO_CUTOVER.md` (symlink repointed)
- `docs/INDEX.md` (REQ row)
- this dispatch doc

The cutover lane's four untracked dispatch docs were **not** staged and remain in the working
tree exactly as found.

## OPEN

- **The C9 threshold — Bill's, explicitly.** Recorded as OPEN item 4 in the amended REQ. The
  sequence: `REQ_UNRESOLVED_SUBJECT_GUARD`'s fix lands → the achievable rate is measured →
  Bill sets the number → C9 can pass or fail on it. Until then C9 is measured and reported
  against the criterion and stays unruled.
- **The expectation-keyed denominator.** Set 1 cannot contribute rows to it without an
  expectation column. Whether that is closed by re-running Set 1 through the banked runner —
  which the assessment notes would break the Voice 38 baseline continuity, and which Bill
  already rejected at Index Demo 22 for that reason — or by leaving the gate keyed on Set 2
  alone, is unresolved and not decided here.
- **The guest question.** The 50 rows stay unrunnable until the text path defines what a guest
  is. Recorded, not answered.
- **Ray ownership**, still open, still blocking 9 rows plus G019's grade. Untouched by this
  amendment.
