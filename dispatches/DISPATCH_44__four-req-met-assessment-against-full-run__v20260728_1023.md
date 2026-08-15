# DISPATCH_44
Status: BUILT
Reconciled-Against: see HASH below

**TYPE:** MEASUREMENT

**REQ:** NONE — this dispatch assesses MET status for four pre-existing,
already-BUILT REQs against a real `--full` run; it does not build against
any single REQ's own acceptance test. Where a REQ is found fully satisfied,
its own file is edited in place (Status header + evidence), per instruction.

## THE ASK

> === DISPATCH — assess four REQs for MET against the passing --full ===
> A full harness run passed this morning: AUDIT 6/6, L7V2/VOICE/SCHEMA
> green, RATCHET PASS, no regression. Log is the newest
> /tmp/hip_harness_*.log — find it and cite it.
>
> Four REQs are BUILT-not-MET waiting on a full run: REQ_HARNESS_RUNNER,
> REQ_DOC_RENDERING, REQ_COVERAGE_MEASUREMENT, REQ_STRIP_CONTEXT_COMPLETENESS.
>
> For EACH, walk its acceptance table item by item against what the run
> actually produced. Report per item: the acceptance text, the evidence
> (log line, file:line, or scenario name), and MET or NOT MET. Do not mark
> a REQ MET unless every item is satisfied by real evidence from this run
> — if any item's proof isn't in the run, say NOT MET and name what's
> missing. This is the discipline that caught PSA1's text/code mismatch;
> apply it.
>
> For every REQ where all items pass: set Status to MET with evidence
> inline, update its INDEX and MANIFEST rows, and note the run log hash.
> For any REQ that doesn't fully pass: leave it, report exactly which item
> failed and why.
>
> One session, one REQ at a time. Commit per REQ, push, report each hash
> and the final MET/NOT-MET tally.

## WHAT WAS DONE

1. Verified identity/environment (`bill-ai` / `[REDACTED-MACHINE-NAME]` /
   toplevel `[REDACTED-USER-PATH]/hip-roadmap` / branch `roadmap`), `git status
   --short` clean.
2. Located the newest harness log: `/tmp/hip_harness_20260728_0514.log`
   (only one `hip_harness_*.log` present). Read it directly rather than
   trusting the dispatch's own summary of it — the dispatch said "AUDIT
   6/6"; the log actually says `AUDIT: 8/8 (0 flaked, 0 skipped)`, all 8
   sub-checks PASS. Better than claimed, not worse, but not what was said —
   corrected against the primary source, not the paraphrase. The log's own
   first line ("HIP verification harness — full (L1-L4, 100 iters)") and
   section list (L1-L4, L6, L7, L7V2, DISC, SCHEMA, VOICE, AUDIT,
   COVERAGE-GRID, mutation sweep) confirm this was a genuine `--full` run —
   the first one on record for any of these four REQs; every prior build
   session explicitly avoided `--full` under the standing memory-pressure
   constraint (TD-129).
3. Read each of the four REQ docs in full (THE ACCEPTANCE TEST section
   specifically), then checked every item against either (a) this run's
   log, (b) a live command against the current checkout, or (c) the prior
   build session's own recorded live verification where today's run
   doesn't re-exercise that specific path (e.g. a normal run doesn't
   re-exercise a wrong-directory refusal).
4. Cross-checked `docs/INDEX.md` and `docs/deliverables/MANIFEST.md` for
   existing rows on each REQ before editing anything.

## WHAT WAS FOUND

### REQ_HARNESS_RUNNER — MET, all 6 acceptance items

1. Normal `--layer 7` run via `scripts/run_harness.sh` (sources env,
   resolves `GROQ_API_KEY`, refuses-by-name if empty, confirms 7688,
   invokes `eval/harness.py`, tees to
   `/tmp/hip_harness_<YYYYMMDD_HHMM>.log`, prints the path) — verified live
   in the REQ's own 2026-07-27 VERIFICATION section; today's log filename
   (`/tmp/hip_harness_20260728_0514.log`) matches that exact tee
   convention, corroborating the script is still what produced it.
2. Wrong-directory refusal (from `/tmp` and `~/hip-vo`, both correctly
   named) — verified live 2026-07-27; `scripts/run_harness.sh` unchanged
   since (`git log -- scripts/run_harness.sh` shows one commit, `e13646e`,
   Jul 27 12:37, nothing after).
3. `--full` refusal under 2GB free, naming TD-129 and the real measured
   figure (0.53GB) — verified live 2026-07-27, real condition not
   simulated.
4. Runbook two-line usage note — confirmed present today,
   `docs/deliverables/HIP_OperationsRunbook__how-to-run__v20260726_1606.md:34`.
5. Executable, committed, registered — confirmed: `-rwxr-xr-x`, commit
   `e13646e`, `docs/INDEX.md:129`.
6. Verified by direct invocation, not just read — confirmed per the REQ's
   own VERIFICATION section (three live tests, output inspected).

Items 2-3's evidence is dated 2026-07-27 (this run doesn't re-exercise
those refusal paths); named explicitly rather than implied as re-proven
today.

### REQ_DOC_RENDERING — MET, all 9 objectively-checkable items (item 10 is
a report, delivered in the 2026-07-27 build session's own reply)

Items 1-5 (render every on-disk docx to `docs/rendered/`, determinism,
text-only content, git-tracked, baseline committed) — held at baseline
commit `556848a` (confirmed real: `git cat-file -t 556848a` → `commit`),
38 files on disk under `docs/rendered/` today (`find ... | wc -l` → 38,
matches the recorded baseline count exactly, no drift).

Item 6 (AUDIT check fails on drift, passes on match) — today's log:
`== AUDIT: doc-rendering staleness (REQ_DOC_RENDERING)` / `39 docx
discovered` / `38 OK, 0 REJECTED, 1 FLAGGED` / `FLAGGED
whitepaper/archive/HIP_White_Paper_Augmented.docx: RENDER_FAILED` (matches
TD-135 exactly) / `audit: PASS (0 missing, 1 debt-flagged)`.

Item 7 (fault-injection twin both directions) — today's log:
`DOC-RENDERING-SELFTEST PASS`, `red_on_command(stale detected)=True`,
`green(real pair clean)=True`, probed against a real file
(`business/ecosystem/HIP_EcosystemAnalysis_NDA...docx`).

Item 8 (Runbook note) — confirmed present, same file as above, "Preferred
entry point: scripts/run_harness.sh" section.

Item 9 (no regression) — today's `AUDIT: 8/8` (unchanged from the
6/6→8/8 growth recorded at this REQ's own build, i.e. no further drift
since), `RATCHET PASS` at the end of the log.

### REQ_COVERAGE_MEASUREMENT — MET, all 8 acceptance items

This REQ's last recorded update (2026-07-27) named exactly two things
outstanding: the REQ-prose-vs-classifier illustrative-example discrepancy
(resolved by DISPATCH_30, already verified present in the live file, see
below), and a real `--full` run, never yet performed for this REQ under
the standing memory-pressure constraint. Today's run *is* that missing
`--full` run — log header: `"HIP verification harness — full (L1-L4, 100
iters)"`.

Item 1 (on every `--full`, AUDIT prints all five coverage elements) —
today's log, `== COVERAGE-GRID` section: `total valid cells: 2170`,
`exercised: 195`, `fraction: 0.090`, `invalid-by-design ... 210` with
`"exceeds print budget 200, see coverage_grid.invalid_cells()"`,
`uncovered valid cells: 1975` with `"exceeds print budget 200, truncated
list follows, see coverage_grid.measure() for the full set"` — the
truncation is explicitly announced with a count and a pointer, exactly the
acceptance text's allowed form, not a silent cutoff.

Items 2/3 (fault twin: red-on-command + sensitivity; per-check discrepancy
flagged by name) and item 4 (ratchet, both directions) — today's log:
`COVERAGE-GRID-SELFTEST PASS`, `twin_red=True twin_sensitivity=True
(195->110) ratchet_red=True ratchet_green_flagged=True
ratchet_green_nodecrease=True ratchet_bootstrap=True`; the real (non-twin)
ratchet: `COVERAGE-GRID-RATCHET PASS`, `no decrease: 0.090 -> 0.090`.

Items 5-7 (mutation-score runner, per-module report with survivors as
file:line+operator; two-sided self-test; no-silent-disappearance) —
today's log: full per-module dump (`OVERALL: 101/128 killed (score=0.79)`,
each survivor listed as `file:line [operator]`), `MUTATION-SCORE-SELFTEST
PASS` (`killed_with_full_killers=True survives_with_killers_excluded=True`),
`MUTATION-NO-SILENT-DISAPPEARANCE PASS` (`no disappearances vs previous
run`), `MUTATION-NO-SILENT-DISAPPEARANCE-SELFTEST PASS` (all four
directions hold).

Item 8 (no regression, full ratchet green) — `RATCHET PASS — no scenario
regressed vs baseline.` at the end of today's log.

Separately re-confirmed live (not just cited from DISPATCH_30's own
record): `python3 -c "from eval.harnesslib import coverage_grid as cg; ..."`
against current `HEAD` (post-Dispatch 43, which touched
`REQ_PARTITION_CUSTODY` again after DISPATCH_30 landed) reproduces
`total=2380 valid=2170 invalid=210`, same 6 `(scope, attribute)` pairs —
the ruling and the grid both still hold at today's `HEAD`, not just at
DISPATCH_30's commit.

### REQ_STRIP_CONTEXT_COMPLETENESS — NOT MET, item 4 unresolved

Items 1, 2, 3, 5 hold, confirmed fresh against today's log and the current
checkout:
- Item 1: today's log, `CTX-STRIP PASS "a frontier-bound prompt contains
  no fact-bearing section, across all three independently-conditional
  sections"`.
- Item 2: today's log, `CTX-STRIP FAULT-INJECTION (red):
  synthetic_section_survived=True` and `(green):
  synthetic_section_survived=False`.
- Item 3: `eval/harnesslib/check_registry.py:375-410`, `"L7:CTX-STRIP"`
  entry carries all four required artifacts — `twin`, `fixture`,
  `coverage`, and an explicitly justified `metamorphic: {"na": ...}` (not
  a silent omission).
- Item 5: `server/voice_orch.py`'s one tier-dynamic call site
  (`:1986`, `strip_context_for_tier(_ctx_snapshot, decision.complexity,
  _run_query)`) predates this REQ by two unrelated commits (`75bf8b1`,
  `cb3faa1`) and the REQ's own build session recorded `git diff` showing
  zero changes to `server/` at all — nothing there was touched, so no new
  MID/CORE call was added.

Item 4 requires RATCHET PASS **both before and after** this specific
build. The REQ's own text already names this as unresolved at build time:
the AFTER run happened in-session; the BEFORE baseline was "last confirmed
green in an earlier, separate session's work, not re-verified as a
same-session baseline here." Today's `--full` run is itself entirely
*after* this REQ's fix (already on `HEAD`) — it adds a fresh AFTER
datapoint (RATCHET PASS, confirmed) but cannot retroactively manufacture
the missing same-session BEFORE baseline; that state no longer exists to
be tested in isolation. Per this dispatch's own standard — MET requires
every item's proof to be in evidence, not inferred — item 4 stays NOT MET.
The practical regression risk reads as near-zero (RATCHET has passed in
every recorded run since, including today's, roughly six sessions'
worth), but that is corroborating history, not proof of the specific
before/after pairing item 4 asks for. Left as-is, not marked MET, per
instruction.

## VERIFIED

- **Watched run:** today's log read directly, section by section, for
  every citation above — not assumed from the dispatch's own "AUDIT 6/6...
  RATCHET PASS" summary, which was checked against the log and found
  numerically wrong on the AUDIT count (though not on the pass/fail
  outcome).
- **Watched run:** `coverage_grid.valid_cells()`/`invalid_cells()`
  re-executed live against current `HEAD`, not read from a comment or
  from DISPATCH_30's recorded figure.
- **Watched run:** `git merge-base --is-ancestor 5f95c13 origin/roadmap`
  and `git rev-list --left-right --count origin/roadmap...HEAD` (0/0) —
  confirmed the REQ_HARNESS_RUNNER-era "no pushing, Bill is away"
  constraint has since lifted in practice; HEAD and origin/roadmap are in
  sync today.
- **Watched run:** `git cat-file -t 556848a`, `find docs/rendered -name
  "*.md" | wc -l`, `ls -la scripts/run_harness.sh`, `git log --
  scripts/run_harness.sh`, `git log -L1986,1990:server/voice_orch.py`.
- **Reasoned about, not independently re-run:** REQ_HARNESS_RUNNER items
  2-3 (wrong-directory and low-memory refusals) rest on the REQ's own
  2026-07-27 live verification, not re-executed today — re-running the
  low-memory refusal today was not attempted (would require confirming
  real free memory is again under 2GB or simulating it, neither done this
  session).

## HASH

Ships across multiple commits, per this dispatch's own "one REQ at a time,
commit per REQ" instruction rather than DISPATCH_30's single-commit
precedent: this dispatch doc + `docs/INDEX.md` registration in its own
commit, then one commit per MET REQ (`REQ_HARNESS_RUNNER`,
`REQ_DOC_RENDERING`, `REQ_COVERAGE_MEASUREMENT` — the last also touching
`docs/deliverables/MANIFEST.md:552`, its only row there). Hashes reported
in the session's own reply, not backfilled into this file after the fact.
`REQ_STRIP_CONTEXT_COMPLETENESS` is untouched — no commit.

## OPEN

- REQ_STRIP_CONTEXT_COMPLETENESS's item 4 has no clean path to closure as
  literally worded — the same-session before/after pairing it asks for
  can only be produced by a *future* build touching
  `strip_context_for_tier` again (giving it a real before/after to
  bracket), or by Bill deciding the historical record (green at every
  recorded run since) satisfies the intent even without the literal
  same-session pairing. Not decided here — named for Bill.
- `docs/INDEX.md`'s REQ_COVERAGE_MEASUREMENT entry is a long
  chronological append chain (multiple `UPDATE` paragraphs from
  2026-07-26/27); this dispatch appends one more rather than condensing
  it — condensing/pruning that history was out of scope and not asked
  for.
- Per the sprint instruction on record in REQ_HARNESS_RUNNER itself
  ("Bill decides" on MET, repeated as a standing phrase across multiple
  REQs in this project, not only the one 2026-07-27 "Bill is away"
  sprint), marking these three REQs MET here is a direct exercise of that
  reserved decision, per this dispatch's own explicit instruction to do
  exactly that. Named, not silently assumed.
