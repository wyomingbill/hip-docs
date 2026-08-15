# DISPATCH_BANK_AND_FILE
Status: BUILT
Reconciled-Against: 2026-08-04 (D-151; parent `0132475`)

**TYPE:** VERIFICATION + REGISTER FILING (docs only; no code, no graph, no harness)

**REQ:** NONE — a banking check and two tech-debt filings. Nothing built, nothing ruled.

## 1. THE REVIEW — ALREADY BANKED. NOTHING RE-BANKED, AND NOTHING RECONSTRUCTED.

**The dispatch's premise is stale, and the correct action was to do nothing.** D-151 states
the 2026-08-01 evaluation-methodology review "exists ONLY in a chat transcript" and cites
D-121's verification that `docs/reviews/` held sixteen artifacts, none of them this one.
That was true when D-121 checked it on the morning of 2026-08-03. **Another lane banked it
that same afternoon**, in the 15:27 batch that also landed the CUTOVER_* artifacts and
`CHATGPT_ConversationMemory`:

- `docs/reviews/CHATGPT_EvalMethodology__evaluation-methodology-review__v20260803_1527.md`
  — 325 lines
- `docs/reviews/FABLE_EvalMethodology__evaluation-methodology-review__v20260803_1527.md`
  — 30 lines (dense; each numbered item is one long line, not a stub — read in full to
  confirm rather than inferred from the line count)

Both carry the reviews-capture header discipline: reviewer named, subject stated,
`Status: BANKED`, **`Verification: UNVERIFIED`** with the explicit note that findings are the
reviewer's and confirmed by no dispatch, `Source:` naming the file each was banked verbatim
from (`~/Downloads/fable-test_research.txt` for the Fable leg), and "banked verbatim,
unedited below this header."

**Verified as content, not just as filenames** — all four findings the dispatch names are
present in the banked text: two-sided evaluation (Fable item 2, the biometrics FAR/FRR
construction), the policy-oracle recommendation (item 3, model-based access-control testing,
ACPT/Margrave), the trace-assertion caveat (item 4, "asserting on mechanism, not text" as
runtime verification over structured execution traces), and the observation about reporting
both error rates rather than one direction (item 6, "costs one paragraph in the report
format; do it this week, it is not a build"). The three named builds for the quarter are in
the Fable leg verbatim.

**So the STOP clause did not arise and neither did the banking.** The dispatch's condition
was "if the source text is not recoverable from any file on disk, SAY SO AND STOP — do not
reconstruct from memory or paraphrase." The text was recoverable — it was already recovered,
by someone else, from the same `~/Downloads` sources. Re-banking it would have produced a
duplicate pair of artifacts under a second timestamp, which is the precise harm the reviews
folder's naming law exists to prevent.

**The search that established this, recorded so it is not repeated:** no transcript file
exists dated 2026-08-01 at all; every file on disk containing the review's signature term
pair (`false-denial` + `oracle`) outside `docs/reviews/` is this session's own scratchpad or
INDEX working copy from 2026-08-03 onward — i.e. downstream discussion, not the source. Had
the banked pair not existed, the honest answer would have been the STOP, because a summary
written from a session's memory is exactly what a reviews folder must not contain.

## 2. TD-159 — the A18/A29/A30 rows are a VISIBILITY gap, not a coverage gap

Filed with D-149's distinction as the entry's whole content, because that is the thing most
likely to be lost in a skim: **these three requirements are tested, and their tests run.**
R18's coverage is `eval/test_lineage_block.py` (16 cases, D-105/D-107); R29/R30's is
`eval/test_sensitivity_registry.py` (31 cases, D-75); both files are wired into the standing
batteries and pass every run. The status board's cross-check matches rows to runners by the
`test_ceil_a<N>_*` convention, and both files **predate that convention**, so the tool cannot
see past the names. The board already says so per-row rather than implying absence — but a
reader skimming three amber rows can still read them as untested, which is why the register
now carries it.

**What would close it:** rename the relevant functions onto `test_ceil_a18_*` /
`test_ceil_a29_*` / `test_ceil_a30_*`. Mechanical, two files, no new test logic, no change to
what is asserted. Named in D-149's own OPEN and left out of its scope deliberately. The
alias-map alternative is recorded and rejected as a default: it would put the row-to-test
relationship in a second place that can drift.

## 3. TD-160 — the dad enrollment gap, and the R9 category it leaves unenforced

Filed SEC, because the consequence is a control consequence even though the cause is data.
`subject="dad"` and `subject="household"` are not enrolled in the identity registry although
both are in scope. D-140's R8 classifier originally derived `THIRD_PARTY_NONCARE_DOSSIER`
from a subject-identity test — subject absent from `known_subject_ids()` and not
`is_recognized_recipient(...)` — which is the correct SHAPE for the category. Standalone
unit tests caught, **before the classifier reached `create_fact_node`**, that real fixture
facts about dad and household classified as third-party dossiers, because neither passes the
registry check. D-140 removed the subject-identity check and moved the class into
`ABSENT_CLASSES` rather than ship a classifier that refuses legitimate household writes.

**The residue, recorded plainly as the dispatch requires:** R9 names six never-store
categories; five have a live write-time signal and this one has none. **The reason is a data
gap, not a principle** — nothing decided third-party dossiers are acceptable and no
requirement was weakened. The category is currently unreachable by live write paths, which
bounds the exposure without closing it; it arms the moment a write path produces a genuinely
external subject. Closing it means enrolling dad and household — a modelling question about
how a care recipient and a shared scope are represented, not data entry — then restoring the
derivation and re-running D-140's 13 cases plus the fixtures. The absence is asserted by a
standing test meanwhile, so a placeholder cannot be added quietly.

## PROCESS NOTES

- STANDARD PREAMBLE observed. Lock read-first then noclobber **before any edit** (06:18:57).
  Own worktree `~/hip-roadmap-d151`, temp branch `d151/bank-and-file`, pushed as
  `d151/bank-and-file:roadmap`, worktree removed after.
- **Docs only.** No graph, no harness, no `.env.dev` — Lane A holds both and D-150 is live.
- Committed with explicit pathspecs and a surgical INDEX stage, expecting Lane A's D-150 row
  to arrive concurrently; both verified present after the push.
- Register cut as a new version (`v20260804_0621`) from `v20260804_0525`, LATEST repointed.

## OPEN

- TD-159's rename and TD-160's enrollment both await their own dispatches.
- Nothing ruled. The banked review remains **UNVERIFIED** by its own header — banking is not
  confirmation, and no dispatch has yet checked its findings against this codebase.
