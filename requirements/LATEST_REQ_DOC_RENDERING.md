# REQ_DOC_RENDERING: Deterministic Text Rendering of Tracked .docx, Wired to a Staleness Gate
Status: MET
Reconciled-Against: 556848a (baseline: scripts/docx_to_text.sh + docs/rendered/); this UPDATE (audit wiring + Runbook note); MET 2026-07-28 per DISPATCH_44

Filed from Bill's dispatch (this session, 2026-07-27), before any code, per
Requirements Discipline item 8. Same session builds against it.

## THE REQUIREMENT

Bill's words, verbatim:

> Make document changes visible in git.
>
> Build scripts/docx_to_text.sh: for every .docx in whitepaper/, business/
> and docs/deliverables/, write a plain-text or markdown rendering to
> docs/rendered/<same-relative-path>.md, tracked in git. Text only, no
> styling. Deterministic output, so an unchanged docx produces a
> byte-identical rendering.
>
> Run it once across every current .docx and commit the renderings as a
> baseline.
>
> Then wire it so it cannot drift: add a check to the audit path that fails
> when a tracked .docx is newer than its rendering. Follow
> REQ_HARNESS_DISCIPLINE, including a fault twin that turns it red when a
> rendering is stale and green when regenerated.
>
> Write REQ_DOC_RENDERING first, from this brief, before the code.
>
> Also add a two-line usage note to docs/deliverables/HIP_OperationsRunbook:
> how to regenerate, and that git diff on docs/rendered/ is how you read a
> document change.
>
> Report: how many documents rendered, total lines, and the hash.

Expanded — decisions made to turn this into buildable acceptance criteria:

**Scope of "every .docx".** Rendered = every `.docx` file physically present
under `whitepaper/`, `business/`, `docs/deliverables/` at render time,
regardless of that file's own git-tracked status. Verified during survey:
`docs/deliverables/*.docx` and most of `whitepaper/*.docx` are gitignored by
pattern (`.gitignore` lines 61-72), yet 38 of 39 on-disk docx across the
three trees remain git-tracked anyway — added before the ignore rule existed
(grandfathered), so the ignore pattern never took effect on them. One file,
`whitepaper/nda/HIP_WhitePaper_Confidential__v20260727_1104.docx`, is
genuinely untracked (post-dates the rule). This is exactly the problem
Bill's opening line names ("make document changes visible in git") — the
binaries are gitignored by design (CLAUDE.md: "binary files gitignored") so
`git diff` shows nothing for a changed docx today, tracked-grandfathered or
not. The renderer therefore does not gate on the source docx's own
git-tracked status; it renders whatever is on disk, so every docx — including
the one currently untracked — gets a tracked text proxy. `business/financial/`
and `docs/deliverables/` currently hold zero `.docx` files; the script does
not fail or warn on an empty match, it just renders what exists.

**"Newer than its rendering."** Implemented as regenerate-and-diff (compare
the renderer's live output against the committed `docs/rendered/*.md` file),
not raw mtime comparison. Reasons: (a) the determinism requirement itself
("unchanged docx produces a byte-identical rendering") makes content
comparison the natural staleness signal — it is what "stale" actually means
here; (b) git checkouts, clones, and `touch` reset mtimes independent of
content, so an mtime-only check would both miss real drift (docx edited,
mtime coincidentally not newer after a checkout) and false-positive on
content-identical files. Regenerate-and-diff is a strict superset of what
"newer" was asking for — it fires in every case mtime would plus cases mtime
would miss. Named here because it is a real interpretation, not literally
what "newer" says.

**Renderer tool.** No `pandoc` or `docx2txt` on this machine (checked, both
absent from PATH); macOS's built-in `textutil` is present and verified
deterministic — `textutil -convert txt -stdout` run twice on the same file
produced byte-identical output. Plain text output, `.md` extension per the
brief's own literal path spec (`docs/rendered/<path>.md`) — content is text,
not markdown syntax, matching "plain-text or markdown rendering" and "text
only, no styling" together. Determinism is same-machine (textutil version
pinned to this box's macOS release), not a cross-platform binary-reproducibility
claim — this codebase is already single-machine-scoped (`scripts/run_harness.sh`
refuses off `[REDACTED-USER-PATH]/hip-roadmap`; the Ops Runbook names "the mini" as
the only place real work runs), so this matches existing practice rather than
introducing a new constraint.

**"Follow REQ_HARNESS_DISCIPLINE."** Read as: build this check to the same
four-part discipline as every other harness check (fault-injection twin,
ground-truth basis, stated coverage, stability under meaning-preserving
variation), and wire it into the same AUDIT block `eval/harness.py` already
runs unconditionally — not as a literal `check_registry.py` roster entry.
The registry's coverage vocabulary (roles x scopes x attribute-splits x
intents, REQ_COVERAGE_MEASUREMENT) is the layer-7/L6 authorization state
space; a document-freshness check has no meaningful mapping onto it, and
REQ_HARNESS_DISCIPLINE's own roster enumeration is an AST scan of
`Scenario(...)` calls in `layer7_crypto.py`/`layer7_crypto_v2.py` plus
`record_invariants.CHECKS` specifically — this check is neither. Precedent
already exists for AUDIT-category scenarios living in the AUDIT block with
no registry entry: `AUDIT:four-part-roster`/`probes`/`fault-injection` and
`AUDIT:COVERAGE-GRID`/`-RATCHET`/`-SELFTEST` all have none (confirmed by
reading `eval/harness.py` and `check_registry.py` directly, and stated
explicitly in the `COVERAGE-GRID` build's own commit message). This REQ
follows that same placement.

## THE ACCEPTANCE TEST

Pass/fail, no judgment calls:

1. `scripts/docx_to_text.sh`, run with no arguments from repo root, renders
   every `.docx` currently on disk under `whitepaper/`, `business/`,
   `docs/deliverables/` to `docs/rendered/<same-relative-path>.md`.
   Observable: after a run, every discovered docx has a corresponding `.md`
   under `docs/rendered/` at the mirrored path, and `docs/rendered/` contains
   no file without a corresponding source docx.
2. Determinism. Observable: run the script twice back to back with no source
   docx changes; `sha256sum` over every file in `docs/rendered/` is identical
   between the two runs.
3. Content is text only. Observable: rendered files contain no docx
   styling/markup artifacts (no XML, no embedded object references) — human
   inspection of a sample plus absence of binary bytes.
4. `docs/rendered/` is git-tracked. Observable: `git add` + `git status`
   shows the rendered `.md` files staged, not ignored; `git check-ignore`
   returns nothing for any file under `docs/rendered/`.
5. The baseline is committed. Observable: one commit contains the renderer
   script and every current rendering.
6. A new check in the harness's AUDIT block (reachable via
   `scripts/run_harness.sh` / `python -m eval.harness`, every gate mode)
   fails when a tracked docx's current content no longer matches its
   committed rendering, and passes once the rendering is regenerated to
   match. Observable: on live content, mutate a copy in a tempdir (not the
   working tree) to simulate drift, see the check's underlying comparison
   report STALE; run the real comparison against the actual committed pair,
   see OK.
7. The check's own fault-injection twin, both directions, live-verified,
   offline, never touching the real working tree during the self-test: (a)
   red-on-command — a real regenerated rendering compared against a
   deliberately corrupted copy of a real committed rendering is reported
   STALE; (b) green — the same real regenerated rendering compared against
   the real, correct committed content is reported OK. Wired as its own
   `AUDIT:*-SELFTEST` scenario, same pattern as `COVERAGE-GRID-SELFTEST` /
   `MUTATION-SCORE-SELFTEST`.
8. `docs/deliverables/HIP_OperationsRunbook__how-to-run__v20260726_1606.md`
   gains a two-line note: the regenerate command, and that `git diff` on
   `docs/rendered/` is how a document change is read. Observable: read the
   file, see exactly that.
9. No regression: the existing AUDIT scenarios (`four-part-roster`,
   `probes`, `fault-injection`, `COVERAGE-GRID`, `COVERAGE-GRID-RATCHET`,
   `COVERAGE-GRID-SELFTEST`) and the full `--layer 7` RATCHET stay green
   after wiring — verified via `scripts/run_harness.sh --layer 7`.
10. Report delivered: count of documents rendered, total line count across
    all renderings, and a hash identifying the baseline (the commit hash the
    baseline lands at).

## WHAT'S ALREADY DONE

Do not redo:
- The AUDIT block pattern in `eval/harness.py` (four-part-roster/probes/
  fault-injection, then `COVERAGE-GRID`/`-RATCHET`/`-SELFTEST`) — this REQ's
  checks extend that same block, same placement discipline, no new file for
  the wiring itself.
- `scripts/run_harness.sh` (REQ_HARNESS_RUNNER, built at e13646e) — the
  guarded entry point this REQ's checks run under; not rebuilt, only used.
- The tempdir-isolated, real-content self-test pattern (`_probe_ob5_paths`,
  `coverage_fault_twin_self_test`) — reused for this REQ's fault twin rather
  than inventing a new self-test idiom.
- The Document Governance Rule's MANIFEST-update pattern for deliverables
  edits (already exercised this same day for the `run_harness.sh` Runbook
  note, per MANIFEST.md's own changelog) — reused for this REQ's Runbook
  note.

## WHAT'S KNOWN BROKEN

The gaps this REQ exists to close:
- `docs/deliverables/*.docx` and most of `whitepaper/*.docx` are gitignored
  by pattern; the majority of on-disk docx stay tracked only because they
  predate the ignore rule (grandfathered — see Expanded section above).
  Either way, `git diff` on a changed docx shows nothing today. There is
  currently no way to see what changed in a document via git.
- One docx on disk right now is genuinely untracked:
  `whitepaper/nda/HIP_WhitePaper_Confidential__v20260727_1104.docx` (matches
  the `whitepaper/nda/*.docx` ignore pattern, postdates it). Named as a fact
  found during survey, not a defect this REQ fixes — its rendering will
  still be produced and tracked.
- No renderer, no `docs/rendered/` tree, and no staleness gate exist
  anywhere in the repo today.
- `docs/rendered/` is a new top-level `docs/` subfolder; CLAUDE.md's Docs
  Organization section is explicitly LOCKED ("do not add folders without
  updating this file and INDEX.md") — both need updating as part of this
  build, not as an afterthought.

## CONSTRAINTS

- Text only, no styling (Bill's words) — plain text extraction, no attempt
  to reconstruct markdown structure (headings, tables) from the docx's own
  formatting.
- Deterministic on this machine: unchanged docx → byte-identical rendering,
  proven by running the renderer twice and diffing, every run.
- `docs/rendered/` must actually be git-tracked — verify no existing or new
  gitignore pattern catches it (the `.docx` ignore patterns are extension-
  scoped and do not match `.md`, but this must be checked, not assumed).
- The new check must not change any existing AUDIT/layer-7/RATCHET
  scenario's pass/fail behavior — additive only, same discipline every prior
  AUDIT addition in this repo has held to.
- Offline: no model calls, no network. `textutil` (a local macOS subprocess,
  no model/network involvement) is the one external-tool dependency this
  REQ introduces, named explicitly rather than silently assumed always
  present — the check must fail loudly, not silently pass, if it's missing.
- No hard-zero/ABSOLUTE semantics claimed for the staleness check itself
  (SERIOUS tier — a stale doc rendering is hygiene, not a security
  invariant); its SELFTEST twin is ABSOLUTE, matching the repo's existing
  pattern for a check-proves-itself scenario.
- No forced `check_registry.py` entry for a check that doesn't fit that
  registry's authorization-state-space vocabulary — named explicitly (see
  Expanded section) rather than shoehorned in.

## UPDATE 2026-07-27: BUILT, all 10 acceptance items hold. Status: BUILT, not MET -- Bill decides.

**Baseline** (556848a): `scripts/docx_to_text.sh` (macOS `textutil`, NUL-
delimited discovery, stderr-as-failure-signal so a corrupt source docx
never silently produces an empty rendering) + `docs/rendered/` (38 of 39
on-disk docx rendered, 14003 total lines). Determinism proven twice:
identical `sha256sum` across two consecutive runs over all 38 convertible
files. `docs/rendered/` confirmed git-tracked (`git check-ignore` empty).
`docs/rendered/` added to CLAUDE.md's LOCKED Docs Organization section.

**One real failure surfaced, not a build defect**:
`whitepaper/archive/HIP_White_Paper_Augmented.docx` is a genuinely
truncated docx (150 bytes, no end-of-central-directory record, unreadable
since its first commit `4eee583`) — the renderer correctly refuses to
write a rendering for it rather than emit a misleading empty file. Logged
as **TD-135** (`docs/techdebt/DEBT_REGISTER__v20260727_1654.md`), named
not fixed — recovering a truncated archive file is out of this REQ's
scope, and live-lineage copies of the same document already exist
(`whitepaper/HIP_White_Paper_Augmented__v20260702_1113.docx` and later).

**Staleness gate** (`eval/harnesslib/doc_rendering.py`, new module):
`discover_docx()`/`rendered_path_for()` mirror the shell script's own
discovery and path logic exactly (same three dirs, same case-insensitive
match, same "append .md" rule). `render_docx()` duplicates the shell
script's stderr-as-failure discipline rather than shelling out to it, so
this check has no dependency on that script's own contract. `_compare()`
is the pure comparison function both the real check and the fault twin
call. `check_all()` classifies every discovered docx OK / STALE / MISSING
/ RENDER_FAILED; a non-OK row is REJECTED (gate-failing) unless its docx
path is named in `docs/techdebt/LATEST_DEBT.md`, in which case it is
FLAGGED (printed every run, does not fail the gate) — same "visible gap,
not silently passed" discipline `harness_audit.py` already uses for
TD-133, generalized without a `check_registry.py` entry (confirmed
unnecessary: `AUDIT:four-part-roster`/`probes`/`fault-injection` and
`AUDIT:COVERAGE-GRID`/`-RATCHET`/`-SELFTEST` all have none either).
Runtime: ~1.7s for all 39 docx (measured) — negligible added cost to
`--layer 7`/`--full`.

**Fault-injection twin (acceptance item 7), both directions, live, real
content, working tree untouched**: `_self_fault_injection()` takes a real
clean (docx, rendering) pair, regenerates it for real via `textutil`, then
compares that real regenerated text against (a) a deliberately corrupted
in-memory copy of the real committed rendering — reported STALE
(red-on-command) — and (b) the real, unmodified committed rendering —
reported OK (green). Verified live twice: once via the module's own
`__main__` (`business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260706_2123.docx`
as the probed pair, `red_on_command=True`, `green=True`), and again by
directly mutating a real committed rendering file
(`docs/rendered/whitepaper/sections/hip_wp_part2.md.docx.md`, appended a
marker line), confirming the real check flips to STALE/REJECTED, then
restoring it and confirming `git diff` on that file is empty and the
check returns to OK — the live path, not just the self-test, proven both
ways.

**Wired** (`eval/harness.py`, extends the existing AUDIT block right
after `COVERAGE-GRID-SELFTEST`, same placement discipline): `AUDIT:
DOC-RENDERING` (SERIOUS) and `AUDIT:DOC-RENDERING-SELFTEST` (ABSOLUTE).

**Runbook note** (acceptance item 8): `docs/deliverables/
HIP_OperationsRunbook__how-to-run__v20260726_1606.md` gained a "Reading
document changes" section — two lines, the regenerate command and the
`git diff docs/rendered/` pointer. `docs/deliverables/MANIFEST.md` updated
in the same commit per the Document Governance Rule (header changelog
entry; Section B row's date was already 2026-07-27, unchanged).

**Live-verified, `scripts/run_harness.sh --layer 7`, two full runs**: AUDIT
grew 6/6 -> 8/8 (the two new scenarios), both PASS; `L7 24/24`, `L7V2
27/28` (1 pre-existing opt-in skip, unchanged); **RATCHET PASS** both
runs, no scenario regressed. `--full` not run this session (not requested;
this REQ's own check is offline/no-model-call and layer-7 already proves
it wired into every gate mode since AUDIT runs unconditionally) — named as
outstanding per CLAUDE.md item 12, not assumed clean.

**Report**: 38 documents rendered, 14003 total lines, baseline commit
`556848a`.

**Acceptance items 1-9 all hold** (1-5 at the baseline commit; 6-9 this
update). Item 10 (the report) is delivered in the session's own reply, not
this doc. Status: BUILT, not MET -- Bill decides.

## UPDATE 2026-07-28: MET, per DISPATCH_44

`docs/dispatches/DISPATCH_44__four-req-met-assessment-against-full-run__v20260728_1023.md`
re-verified items 1-9 fresh against `/tmp/hip_harness_20260728_0514.log`
(a real `--full` run) and the current checkout, rather than relying only
on this doc's own 2026-07-27 record:

- Items 1-5: baseline commit `556848a` confirmed real
  (`git cat-file -t 556848a` -> `commit`); `docs/rendered/` holds exactly
  38 `.md` files today (`find docs/rendered -name "*.md" | wc -l`), no
  drift from the recorded baseline count.
- Item 6: today's log, `AUDIT: doc-rendering staleness` section — `39 docx
  discovered`, `38 OK, 0 REJECTED, 1 FLAGGED`
  (`whitepaper/archive/HIP_White_Paper_Augmented.docx: RENDER_FAILED`,
  matches TD-135 exactly), `audit: PASS (0 missing, 1 debt-flagged)`.
- Item 7: today's log, `DOC-RENDERING-SELFTEST PASS`,
  `red_on_command(stale detected)=True`, `green(real pair clean)=True`.
- Item 8: confirmed present,
  `docs/deliverables/HIP_OperationsRunbook__how-to-run__v20260726_1606.md:34`.
- Item 9: today's `AUDIT: 8/8` (unchanged since this REQ's own 6/6->8/8
  growth — no further drift), `RATCHET PASS` at the end of the log.

Item 10 (the report: document count, line count, hash) was delivered in
the 2026-07-27 build session's own chat reply per this doc's own record,
not independently re-verifiable from disk today; treated as satisfied by
that existing record, not re-derived.

Marking MET here exercises "Bill decides" directly, per DISPATCH_44's own
explicit instruction to do exactly that for any REQ whose items all hold.
