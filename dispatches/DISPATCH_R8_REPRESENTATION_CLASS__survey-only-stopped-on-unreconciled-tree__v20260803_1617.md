# DISPATCH_R8_REPRESENTATION_CLASS
Status: BUILT
Reconciled-Against: see HASH — this doc originally stopped after the survey (item 2) on an
un-reconciled tree; resumed at item 3 once the tree reconciled (separate dispatch, "Index
Demo — FINISH AND RECONCILE") and completed items 3-7 in this same file, per instruction
("Commit your survey dispatch doc with the build").

**TYPE:** BUILD (originally filed ANALYSIS/survey-only when this dispatch stopped at item 3;
now BUILD — see the RESUMED AT ITEM 3 sections below)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`,
R8 (write-time representation class).

## THE ASK

Dispatch text, verbatim:

```
=== D-140 | ~/hip-roadmap, roadmap | R8: write-time representation class ===
STANDARD PREAMBLE.
NOTE: this checkout is AHEAD 2, BEHIND 2 — another lane (claude-code-banking) has two
unpushed local commits and is behind D-136/D-137. That is THEIR reconciliation. Report the
state, do not perform it, and do not commit on top of an un-reconciled tree. If you cannot
work cleanly, STOP and report.

GOVERNING REQ: REQ_STRUCTURAL_CEILING R8.

1. WHY THIS ONE: R10 is the ceiling REQ's one NOT MET. Its four checks are origin (enforced),
   registry (enforced), permit (R2 built at D-130, unruled), and REPRESENTATION — which needs
   R8's classes, and they do not exist. R8 plus a ruling on R2 unblocks R10.

2. SURVEY FIRST, report before changing anything:
   a. R8's text as filed. Read it.
   b. Verify the representation-class enum is genuinely absent at HEAD, as D-120 recorded.
   c. Which classes R8 names, and which of those HIP can assign HONESTLY at write time from
      what the writer already has. Same discipline as D-105's lineage block — three of eleven
      fields stayed absent and were asserted absent rather than guessed.
   d. Whether assigning a class requires a value-level judgment. D-50 Principle 6 forbids the
      protection from judging member content; a class assigned from ORIGIN or SHAPE is fine, a
      class assigned by reading what the fact SAYS is not.
   STOP AND REPORT if (d) shows the classes cannot be assigned without reading content.

3. THEN BUILD what can be assigned honestly, at create_fact_node — the single materialization
   point. Classes that cannot be assigned honestly are absent and asserted absent.

4. ACCEPTANCE per D-87: fault twin, anti-vacuity. A8 is UNWRITABLE for want of this build —
   report whether it becomes writable. DO NOT re-tier it. Report whether A10 becomes
   satisfiable once R2 is ruled.

5. Run --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
6. Rule nothing MET. Lock read-first noclobber — another lane held it recently.
7. Report LONG: dispatch doc plus status line, path, and hash to the terminal.
```

## WHAT WAS DONE

1. **Machine gate** — `whoami`/`hostname`/`pwd`/`git branch --show-current`: `bill-ai` /
   `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]/hip-roadmap` / `roadmap`. Matched.
2. **Tree-state check, before any survey work** — `git status -sb`, `git fetch origin
   roadmap`, `git rev-list --left-right --count origin/roadmap...HEAD`, `git log --oneline` on
   both local and `origin/roadmap`. Confirmed the dispatch's own note precisely (see WHAT WAS
   FOUND).
3. **Lock check** — `cat .hip-lock`: absent (no file). Not taken, since no commit follows this
   dispatch (see OPEN) — a lock exists to serialize commits/graph-and-harness mutation, and
   this dispatch performs neither.
4. **Survey 2a** — read R8's full text at
   `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md:364-389`,
   and R9 (:391-408, the hard-refused-representations list it references) and R3 (:249-276,
   the prohibited-autonomous-label list R8's `PROHIBITED_AUTONOMOUS_LABEL` class points at),
   plus RULING 1 (:30-38, the D-50 Principle 6 split the dispatch's item 2d cites).
5. **Survey 2b** — confirmed `docs/requirements/` is byte-identical between local HEAD and
   `origin/roadmap` (`git diff origin/roadmap HEAD -- docs/requirements/` empty), so R8's text
   is unaffected by the tree divergence. Grepped the full tree for
   `representation_class`/any of the 14 class-name strings: the only hit is
   `eval/test_ceiling_inference.py`, which mentions R8 in prose (its own docstring, discussing
   why A8/A10 are blocked) — no classifier, no enum, no field exists anywhere. D-120's finding
   confirmed current.
6. **Survey 2c/2d** — read `harness/extraction_queue.py::CANONICAL_ATTRIBUTES` (17 values) and
   `harness/write_origins.py::DERIVABLE_ATTRIBUTES` (2 values), `harness/role_resolution.py`
   and `harness/care_team_keys.py` (for identity/roster-lookup signals), and
   `harness/disclosure.py:269` (to check what `origin=="attributed_import"` actually means in
   this codebase today, rather than assuming). Built the per-class table below.

No file was written or modified. No test was run. No commit was made.

## WHAT WAS FOUND

### Tree state (blocks item 3 onward)

`git status -sb`: `## roadmap...origin/roadmap [ahead 2, behind 2]`.

- **Local-only (ahead), not on origin:** `21c78bb` "Index Bank 2: file six demo-lane findings,
  TD-152 through TD-157" and `aaadae3` "Index Bank 1: bank demo-lane's unbanked artifacts to
  docs/ and eval/probes/" — the `claude-code-banking` lane's own unpushed work, sitting on
  this exact checkout.
- **Origin-only (behind), not in local history:** `c5c9202` "D-137: the HANDOFF state
  document, the STANDARD PREAMBLE, pre-authorized ruling classes, and the 2026-08-03 design
  digest" and `5a2fbe9` "D-136: report routing by SIZE — short to the terminal, long to the
  dispatch doc".
- Working tree also carries the now-familiar demo-cutover lane's untouched WIP (`docs/INDEX.md`
  modified, four untracked `DISPATCH_DEMO_CUTOVER_*.md` files) — unrelated to the above,
  confirmed unchanged from prior dispatches, left exactly as found.

**This matches the dispatch's own note exactly.** Per instruction, this is the banking lane's
reconciliation, not performed here. Two independent reasons this blocks committing R8's build
cleanly, beyond the plain non-fast-forward:

1. `git push` would be rejected outright (local and remote have diverged); resolving that is a
   merge or rebase decision explicitly assigned elsewhere.
2. D-137 (origin-only, not merged locally) **created `docs/HIP_HANDOFF.md` and ARMED the rule**
   (from CLAUDE.md, read via `git show origin/roadmap:CLAUDE.md` without merging) that "a lane
   that lands a dispatch updates CURRENT STATE in the SAME commit" and that "if a lane cannot
   honestly update it, that is a STOP." `docs/HIP_HANDOFF.md` does not exist in this local
   working tree (only on origin, behind the two unmerged commits) — so a commit landed here
   right now could not honestly satisfy an already-armed, mandatory rule without first
   performing the reconciliation item 0 assigns to the banking lane.

**Conclusion: cannot work cleanly, per the dispatch's own stated criterion. STOPPING before
item 3 (BUILD).** The survey (item 2) is complete and reported below in full, since it is
read-only and independent of the tree state.

### R8's text (2a)

Fourteen named classes (`docs/requirements/REQ_STRUCTURAL_CEILING__...:370-385`):
`ORDINARY_CLAIM, HEALTH_CLAIM, COGNITIVE_OBSERVATION, FUNCTIONAL_SUPPORT_STATE,
FINANCIAL_CLAIM, LOCATION_STATE, AUTHENTICATION_SECRET, CONTINUOUS_RAW_SURVEILLANCE,
BIOMETRIC_OR_GENETIC_TEMPLATE, RAW_INTIMATE_MEDIA, THIRD_PARTY_NONCARE_DOSSIER,
EXTERNAL_PROFESSIONAL_DIAGNOSIS, PROHIBITED_AUTONOMOUS_LABEL, UNKNOWN_HIGH_RISK`.
`UNKNOWN_HIGH_RISK` must fail closed for durable persistence (:389). The classification event
"SHALL NOT be presented as a judgment that the household statement is true, false, good, bad,
important, or unimportant" (:387) — R8's own text already anticipates the Principle-6 tension
item 2d asks about.

### Representation-class absence (2b)

Confirmed absent at HEAD: no `representation_class` field, no classifier function, no enum
anywhere in the tree (`grep -rln` across every `.py` file for the field name and all 14 class
strings — the only hit is prose in `eval/test_ceiling_inference.py`, not an implementation).
Matches D-120.

### Per-class buildability (2c/2d) — 14 classes, three groups

**Group 1 — assignable honestly TODAY, from origin/attribute/subject-identity alone (6):**

| class | signal | basis |
|---|---|---|
| `ORDINARY_CLAIM` | attribute ∈ {`preference`,`relationship`,`employer`,`dietary`,`schedule`,`household`} | attribute-name lookup |
| `HEALTH_CLAIM` | attribute ∈ {`medication`,`medication_status`,`allergy`,`vitals`}, plus the coarse default for `health_condition`/`incident`/`care_plan` (see Group 3 caveat) | attribute-name lookup |
| `FINANCIAL_CLAIM` | attribute == `financial` | attribute-name lookup |
| `LOCATION_STATE` | attribute ∈ {`address`,`zone_district`} | attribute-name lookup |
| `THIRD_PARTY_NONCARE_DOSSIER` | `subject` absent from `harness.role_resolution.known_subject_ids()` and `harness.role_resolution.is_recognized_recipient(subject)` false | identity/roster lookup — structural, not content |
| `UNKNOWN_HIGH_RISK` | fail-closed default when no other class applies | R8's own required behavior |

**Group 2 — definable and honest, but UNREACHABLE by anything the live write paths produce
today (5):**

| class | why definable | why unreachable today |
|---|---|---|
| `AUTHENTICATION_SECRET` | attribute-name pattern match (e.g. "password"/"pin") | no such attribute exists in `CANONICAL_ATTRIBUTES`; R9 already hard-refuses this class of content at the graph level by a separate, pre-existing mechanism |
| `CONTINUOUS_RAW_SURVEILLANCE` | same | no ambient audio/video attribute exists; R9 hard-refuses |
| `BIOMETRIC_OR_GENETIC_TEMPLATE` | same | voiceprints live in a separate, non-exportable identity subsystem per R9's own stated exception, never a `:Fact` |
| `RAW_INTIMATE_MEDIA` | same | text-only memory system; no media-carrying attribute exists |
| `PROHIBITED_AUTONOMOUS_LABEL` | derivation-origin fact whose attribute matches one of R3's 13 named forbidden categories (:253-265) — a name/pattern match, content-blind | `DERIVABLE_ATTRIBUTES` today is exactly `{risk_pattern, lifestyle}` (`harness/write_origins.py`), and neither name matches R3's list, so the check is real but currently dead code |

**Group 3 — NOT assignable honestly today; asserted absent, each for a distinct, named reason
(3):**

- **`COGNITIVE_OBSERVATION`** — no attribute separates a cognitive-decline observation from an
  ordinary `health_condition`/`incident` fact; both would carry the identical attribute
  string, and telling them apart requires reading the free-text value. **This is a direct
  D-50 Principle 6 collision** and matches the banked review's identical finding verbatim
  (`docs/reviews/D63_dimensioned-ceiling-axes__fable-and-chatgpt__v20260731_1917.md:112`:
  "needs a value-level test the enum cannot express and D-50 Principle 6 ... forbids").
- **`FUNCTIONAL_SUPPORT_STATE`** — the same shape-collision as above, generalized: ADL/mobility
  support content (e.g. "needs help bathing") shares attribute space with ordinary
  `health_condition`/`care_plan` facts, with no structural separator. R3 explicitly permits
  HIP to retain "a narrowly defined functional support need" (:273) — so this is a legitimate,
  wanted category, not a prohibited one — but the write-time classifier cannot honestly reach
  it from attribute/origin/subject alone.
- **`EXTERNAL_PROFESSIONAL_DIAGNOSIS`** — a DIFFERENT kind of absence from the two above: not a
  Principle-6 violation, but an absent mechanism. The one plausible signal,
  `origin=="attributed_import"`, already means something else in this codebase today — its
  only real caller is `harness/disclosure.py::write_frontier_fact`, stamped
  `origin="attributed_import"` with the comment "attributed external claim (frontier answer)"
  (`:269`) — the FRONTIER TIER'S OWN AI-GENERATED ANSWER being written back, not a clinician-
  or EHR-imported diagnosis. No mechanism for importing an actual external professional
  diagnosis exists in this codebase. Assigning this class today would either misuse the
  existing origin value (labeling a frontier-model answer as a "professional diagnosis") or
  require inventing a marker nothing produces. Matches R2/D-130's `purpose_id`/
  `retention_policy` precedent exactly: absent because the underlying mechanism doesn't exist,
  not guessed at.

**Net: 6 of 14 classes assignable and reachable today; 5 of 14 definable and honest but dead
code against the current write paths; 3 of 14 must be asserted absent, for three distinctly
different reasons (two Principle-6 collisions, one absent-mechanism).** Per item 2's own
instruction this is reported, not silently absorbed — and per the R2/D-130 precedent, a
partial-absence finding of this shape would ordinarily not itself have stopped the dispatch
(item 3 already anticipates "classes that cannot be assigned honestly are absent and asserted
absent"). **The tree state is what stopped this dispatch, not the Group 3 finding on its own.**

## RESUMED AT ITEM 3 — the tree reconciled

The banking lane's reconciliation happened as a separate dispatch ("Index Demo — FINISH AND
RECONCILE"): four local commits rebased onto `origin/roadmap` with `--autostash`, byte-verified
against a pre-rebase INDEX snapshot, pushed. Tree confirmed `ahead 0 / behind 0` before this
build resumed. Gate re-checked (unchanged: `bill-ai` / `[REDACTED-MACHINE-NAME]` /
`[REDACTED-USER-PATH]/hip-roadmap` / `roadmap`). Lock read first (free), taken noclobber
(`holder: D-140 (R8: write-time representation class)`).

### WHAT WAS DONE (continued)

7. Built `harness/representation_class.py` (new file): the 14-class registry, `ABSENT_CLASSES`,
   the Group 2 attribute-name-pattern tables (R9's four hard-refused classes, R3's 13
   prohibited-label fragments), the Group 1 attribute-to-class lookup (19 entries — all 17
   `CANONICAL_ATTRIBUTES` plus both `DERIVABLE_ATTRIBUTES`), and
   `classify_representation(*, attribute, origin, subject)`.
8. Unit-tested the classifier standalone against 13 hand-picked cases before touching
   `create_fact_node` — this is what caught the `THIRD_PARTY_NONCARE_DOSSIER` defect (see WHAT
   WAS FOUND) before it could reach the creator or the harness.
9. Corrected the classifier: removed the subject-identity check, moved
   `THIRD_PARTY_NONCARE_DOSSIER` into `ABSENT_CLASSES`, re-verified all 13 cases plus the
   dad/household cases pass.
10. Wired enforcement into `memory_engine/store.py::create_fact_node`: added
    `representation_class: $representation_class` to `_CREATE_FACT_CQL` (auto-extends
    `_FACT_PROP_KEYS`), computed `_rep_class` and raised on `UNKNOWN_HIGH_RISK`, stamped
    `full["representation_class"]` alongside `artifact_type`.
11. Direct stub-transaction tests against `create_fact_node` (normal write stamps the right
    class; `UNKNOWN_HIGH_RISK` refuses with no write issued; `dad`/`household` fixture-shaped
    facts classify correctly) — all passed before running the standing batteries.
12. Wrote `eval/test_ceiling_representation_class.py` (57 cases) and registered it in
    `scripts/run_harness.sh`.
13. Ran `--layer 7`; found and fixed 5 failures in `eval/test_fact_write_convergence.py` (the
    D-96 shape-convergence pins) and 1 in the L7 harness itself (PSA1's synthetic probe
    attribute) — see WHAT WAS FOUND for each.
14. Found and fixed a real ordering bug in `create_fact_node`: the R8 check originally ran
    before the unknown-property structural check.
15. Re-ran `--layer 7` (clean, exit 0) and `eval.memory_harness` three times (stable).
16. Verified A10's satisfiability directly and standalone, mirroring
    `_a10_enforced_at_creator()`'s own probe shape without editing that file — see WHAT WAS
    FOUND.
17. Recorded R8 in `REQ_STRUCTURAL_CEILING` §16 as "reported, not ruled", matching R2/D-130's
    precedent.
18. Staged by explicit pathspec (8 files: the two new files, plus
    `memory_engine/store.py`, `eval/harnesslib/layer7_crypto.py`,
    `eval/test_fact_write_convergence.py`, `scripts/run_harness.sh`,
    `docs/requirements/REQ_STRUCTURAL_CEILING__...md`, and this dispatch doc) — `docs/INDEX.md`
    (cutover lane's WIP) and the four untracked `DISPATCH_DEMO_CUTOVER_*.md` files confirmed
    untouched via `git status` before and after.
19. Committed, pushed, released the lock.

### WHAT WAS FOUND (continued)

**A real classifier defect, caught by testing against actual fixture data before it reached
production code.** The original design placed `THIRD_PARTY_NONCARE_DOSSIER` in the assignable
group, keyed on `harness.role_resolution.known_subject_ids()`/`is_recognized_recipient()` —
structural, not content, sound reasoning. Direct testing found `subject="dad"` and
`subject="household"` BOTH fail that check: `known_subject_ids()` returned a large registry set
containing neither string; `is_recognized_recipient("dad")` and `is_recognized_recipient(
"household")` both `False`; `grep -n '"dad"' scripts/demo_seed.py` confirmed dad is named only
as a raw `subject` string in D4/D5/D8 and is never passed to `_ensure_dyad` or
`_ensure_care_team_member` (only `"ray"` is, at lines 550-551/561-562). Assigning the class
from this signal would have misclassified D3, D4, D5, D7, D8, D10, D11 — seven of the demo's
eleven canonical fixture facts — as non-care third-party dossiers. Fixed by moving
`THIRD_PARTY_NONCARE_DOSSIER` into `ABSENT_CLASSES` (now 4, not 3) and removing the
subject-identity branch from `classify_representation` entirely, rather than special-casing
"dad" (which would have been exactly the kind of guess this dispatch's discipline forbids — dad
isn't structurally special, he's a symptom of an incomplete enrollment). Recorded as a
build-time correction, not a survey error: the survey's Group 1 placement was reasoned
correctly from the code that exists; only running it against real data exposed the gap.

**Five pre-existing test/fixture sites needed updating for the new check, plus one real
ordering bug in the new code itself — kept separate, not conflated:**
- `eval/test_fact_write_convergence.py`'s `_BEFORE` fixture (the D-96 shape-convergence
  proof) pins the exact stored-property set for three "through-the-path" write shapes. Adding
  `representation_class` is a real, deliberate shape change — recorded as a documented v4 delta
  in the file's own docstring, alongside v2's `origin` and v3's R18 lineage block, with the
  computed value for each fixture (`risk_pattern`→`HEALTH_CLAIM`,
  `employer`→`ORDINARY_CLAIM`) stated and justified, not just pasted in.
- The same file's `test_ceil_conv_creator_stamps_version_unconditionally` used a placeholder
  attribute `"a"` — not a real attribute, and irrelevant to what that test actually checks (R30
  version-stamp behavior) — swapped for `"employer"`.
- `eval/harnesslib/layer7_crypto.py`'s PSA1 fault-injection probe wrote a synthetic
  `"psa1_probe_attribute"` — the probe tests prompt/record fidelity plumbing, not attribute
  content — swapped for the canonical `"preference"`.
- **The one REAL bug, not a fixture mismatch:** `create_fact_node`'s R8 block originally ran
  BEFORE the `unknown = set(props) - _FACT_PROP_KEYS` structural check. A malformed props dict
  missing `attribute` entirely (as `test_ceil_conv_creator_refuses_unknown_keys` deliberately
  constructs, to prove a misspelled key is refused) reached the classifier first, which
  correctly-but-unhelpfully returned `UNKNOWN_HIGH_RISK` and masked the test's intended
  "unknown :Fact properties" error. Fixed by moving the R8 block to run after the structural
  check — a malformed shape is a schema defect and should get the schema error, not a semantic
  one about content it never had.

**A10's satisfiability (item 4), verified directly and empirically, not reasoned about.**
Wrote a standalone script mirroring `eval/test_ceiling_inference.py::_a10_enforced_at_creator(
)`'s exact probe shape (same `_ProbeRecorder`, same `_probe_props`, same "refuses AND issues no
write" counting rule) without editing that file, and added probes for the two checks it could
not previously test (representation, permit — both now buildable):
```
origin:          True  (unknown write origin 'not_a_real_origin')
registry:         True  (origin 'extraction' requires a canonical attribute)
representation:   True  (representation_class classified as UNKNOWN_HIGH_RISK)
permit:           True  (derivation input includes attribute(s) outside R2's allowed_input_attributes)
found: ['origin', 'permit', 'registry', 'representation']
all four found: True
```
**A10's underlying predicate is structurally satisfiable TODAY** — all four of R10's
revalidations fire at `create_fact_node`, independent of whether Bill has formally ruled R2
(or R8) MET. Ruling is a governance act on whether a REQ's content is acceptable; it is not a
precondition for whether the code enforces what the REQ describes — the code already does.
NOT re-tiered: `test_ceil_a10_all_four_revalidations_land_at_the_creator` stays
`xfail(strict=True)`, `_a10_enforced_at_creator()` in that file is untouched, per explicit
instruction. Whether to flip it — and whether R10's D-100 "NOT MET" ruling should be revisited
now that all four checks fire — is Bill's call.

## VERIFIED

**Watched run (survey phase):** none — read-only, no code changed.

**Watched run (build phase, this session):**
- `harness/representation_class.py` imported directly; 13 hand-picked classification cases
  checked against expected output, including the dad/household cases that caught the defect.
- `memory_engine.store.create_fact_node` called directly with a stub transaction recorder:
  normal write stamps the correct class; a synthetic unrecognized attribute via `fixture`
  origin raises `ValueError` mentioning `UNKNOWN_HIGH_RISK` with zero calls recorded on the
  recorder (no write issued); `subject="dad"`/`subject="household"` fixture-shaped writes
  classify correctly post-fix.
- `eval/test_ceiling_representation_class.py`: `57 passed` standalone
  (`PYTHONPATH=$(pwd) python3 -m pytest ... --import-mode=importlib`).
- `eval/test_fact_write_convergence.py`: `17 passed` standalone, after the `_BEFORE`/attribute
  fixes.
- `./scripts/run_harness.sh --layer 7`: three consecutive runs — v1 exit 1 (5 failures,
  `test_fact_write_convergence.py`, diagnosed above), v2 exit 1 (1 failure, PSA1 probe,
  diagnosed above), v3 exit 0, RATCHET PASS, standing batteries `380 passed, 8 xfailed`, zero
  failures. Logs: `/tmp/d140_layer7_v1.log` through `_v3.log`.
- `python3 -m eval.memory_harness`: three consecutive runs, `13/17` every time, failing set
  exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`; `graph_subject_ids()` confirmed `ray`/`dad`
  both active after each run (TD-151's D-130 fix holding).
- The A10 satisfiability probe above, run directly against live `memory_engine.store`.
- `git status` before and after `git add`/`git commit`: confirmed `docs/INDEX.md` and the four
  untracked `DISPATCH_DEMO_CUTOVER_*.md` files were never staged.

**Reasoned about:** the survey's per-class table (unchanged from the original filing, except
`THIRD_PARTY_NONCARE_DOSSIER`'s group, corrected above with direct evidence, not reasoning
alone). The claim that ruling status doesn't gate code behavior (A10 discussion) is a governance
reading, not a code fact — stated as such.

## HASH

See the commit landed alongside this doc's own update — staged and pushed together with
`harness/representation_class.py`, `eval/test_ceiling_representation_class.py`,
`memory_engine/store.py`, `eval/harnesslib/layer7_crypto.py`,
`eval/test_fact_write_convergence.py`, `scripts/run_harness.sh`, and the
`REQ_STRUCTURAL_CEILING` §16 update.

## OPEN

- **R8 itself is not ruled** — reported only, per instruction ("rule nothing MET"). Bill's
  call.
- **A8/A10/R10 are not re-tiered.** Whether A10 should move off `xfail(strict=True)`, and
  whether R10's D-100 "NOT MET" ruling should be revisited now that all four of its checks
  fire, is explicitly left to a future dispatch.
- **`COGNITIVE_OBSERVATION`, `FUNCTIONAL_SUPPORT_STATE`, `EXTERNAL_PROFESSIONAL_DIAGNOSIS`,
  `THIRD_PARTY_NONCARE_DOSSIER` remain absent** — the first three per the original survey, the
  fourth per this build's own finding. None invented, none guessed.
- **The care-recipient enrollment gap this build surfaced (dad lacks the formal
  dyad/care-team registration ray has) is NOT filed as a TD and NOT fixed** — it belongs to a
  different mechanism (`harness.role_resolution`/`scripts/demo_seed.py`'s enrollment flow) than
  this classifier, and fixing it wasn't asked for here. Flagged for a follow-up dispatch to
  decide whether it needs a TD.
- **This report is LONG** (per-class evidence tables, live probe output, harness-run evidence)
  — routed to this dispatch doc per the D-136 routing rule; terminal gets only the status line,
  this path, and the hash.
