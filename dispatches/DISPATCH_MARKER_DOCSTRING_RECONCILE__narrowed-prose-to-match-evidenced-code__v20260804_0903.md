# DISPATCH_MARKER_DOCSTRING_RECONCILE
Status: BUILT (docs-only — prose corrected, no code changed)
Reconciled-Against: see HASH

**TYPE:** ANALYSIS (survey) + docs-only correction. No code change; acceptance per D-87
explicitly skipped, per item 4's own instruction to say so rather than leave it implied.

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R4/R8, the D-157 amendment. No new REQ needed — this corrects a docstring against the
existing amendment's own evidence bar, per Requirements Discipline item 10's carve-out for
analysis work.

## THE ASK

Dispatch text, verbatim:

```
=== D-159 | ~/hip-roadmap, roadmap | Reconcile the marker docstring with the code ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R4/R8, the D-157 amendment.

D-158 flagged it: the marker's candidate set is deliberately NARROWER than
harness/representation_class.py's own docstring prose, which reads
FUNCTIONAL_SUPPORT_STATE as also sharing space with health_condition. D-158 used only
D-144's live-evidenced pairings, which was right. But the document and the code now
disagree, and a docstring claiming more than the code does is the same defect class
this project has spent the week removing.

1. SURVEY FIRST, report before changing anything. Enumerate EVERY pairing the docstring
   prose asserts, and for each: is it live-evidenced (name the evidence), plausible but
   unevidenced, or wrong? Evidence from the code and the fixtures, not from the prose
   restating itself. STOP AND REPORT if the survey finds the CODE is the narrow one and
   the prose is right — that is a different fix than the one this dispatch assumes.
2. THEN RECONCILE IN ONE DIRECTION, chosen on the evidence and stated plainly:
   either widen the code to match the prose — which needs the evidence pass D-158 said
   it would need, and you must produce it, not assert it — or narrow the prose to match
   the code, recording WHY each dropped pairing lacked evidence rather than deleting it
   silently.
3. DO NOT SPLIT THE DIFFERENCE. Two documents that half-agree is the state you are
   fixing.
4. Acceptance per D-87 if code changes: executed fault twin, anti-vacuity. If only
   prose changes, say so and skip — but say it, do not leave it implied.
5. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
6. Rule nothing MET.
```

## WHAT WAS DONE

1. Gate checked — matched. Repo lock acquired, pulled clean (no new commits since D-158).
2. Read `harness/representation_class.py`'s Group 3 docstring in full and enumerated
   EVERY pairing the prose asserts — not three (D-158's own flag undercounted this),
   **FOUR**: the COGNITIVE_OBSERVATION entry names two (`health_condition`, `incident`);
   the FUNCTIONAL_SUPPORT_STATE entry ALSO names two (`health_condition`, `care_plan`) —
   both entries name `health_condition`, which is exactly the collision D-158's own flag
   was pointing at without naming it this precisely.
3. For each pairing, sought PRIMARY evidence, not the docstring restating itself:
   - Checked D-144's own absorption-survey table
     (`docs/dispatches/DISPATCH_R8_R10_RULINGS__...`) directly — confirms the ABSORPTION
     MECHANISM (each attribute maps to `HEALTH_CLAIM` today) for all three attributes
     involved, but does NOT itself independently verify the SEMANTIC overlap claim (that
     a cognitive-observation or support-state utterance would actually be extracted
     under that specific attribute name) — that claim's source is elsewhere.
   - Read `docs/reviews/D63_dimensioned-ceiling-axes__fable-and-chatgpt__v20260731_1917.md`
     in full for the two relevant sections: the AXIS 1 "candidate content" table (which
     the module docstring already cites by line number for COGNITIVE_OBSERVATION), and
     the "Layer 1-5" section (R4's own direct source — the layer examples in R4's text
     are near-verbatim from this review).
   - Checked `eval/sia_golden_set.json`'s own `health_condition`-attributed entries (8)
     for any hint of ADL/mobility/support-arrangement content — found none; all 8 are
     condition-query-shaped ("What's my health condition?"), none support-arrangement-
     shaped.
   - Read `CANONICAL_ATTRIBUTES`' own descriptions for `health_condition` ("Diagnosed or
     reported health conditions") and `care_plan` ("A recipient's documented care plan or
     care-team-agreed course of action") directly, `harness/extraction_queue.py:157,190`.
4. **Reconciled in ONE direction** (item 3's own instruction: do not split the
   difference): narrowed the docstring's FUNCTIONAL_SUPPORT_STATE entry to drop
   `health_condition`, keeping only `care_plan` — matching `harness/representation_
   class.py`'s own `_UNDETERMINED_CANDIDATES_BY_ATTRIBUTE` table (D-158), which was
   already correct. **The drop is recorded IN the docstring, not silently deleted** — a
   dated `CORRECTED, 2026-08-04 (D-159)` note states what was dropped and exactly why,
   per item 2's own instruction.
5. **No code changed.** `_UNDETERMINED_CANDIDATES_BY_ATTRIBUTE`,
   `undetermined_candidates()`, and every call site were already built to the narrower,
   correct set at D-158 — confirmed by re-reading the code (unchanged since D-158) before
   concluding there was nothing to touch there.
6. **Item 4's own instruction followed literally: no fault twin, no new test, no
   acceptance run — stated here rather than left implied**, because no code changed.
7. Ran the item-5 checks anyway, as instructed, to confirm the docstring-only edit is
   genuinely inert: `eval/test_ceiling_representation_class.py` +
   `eval/test_ceiling_representation.py` (105 passed, unchanged from D-158's own count),
   `./scripts/run_harness.sh --layer 7` (RATCHET PASS), `eval/memory_harness.py` under a
   manually-held `graph:7688` lock (13/17, failing set exactly
   `{MEM-115, MEM-116, MEM-117, MEM-118}`).
8. Wrote this dispatch doc, fixed the docstring's own forward-reference to this doc's
   real filename before committing (checked, not assumed).
9. Staged by explicit pathspec, committed, pushed, verified post-commit, released the
   lock.

## WHAT WAS FOUND

### The full survey — all four prose-asserted pairings, graded

| pairing | grade | evidence |
|---|---|---|
| `health_condition` ↔ `COGNITIVE_OBSERVATION` | **LIVE-EVIDENCED** | D-63 banked review, Axis 1, stated directly: "Cognitive facts are already collectable today under `health_condition` ('Diagnosed or reported health conditions')." Cross-checked against D-144's own `classify_representation()` probe confirming the absorption mechanism exists for this attribute. |
| `incident` ↔ `COGNITIVE_OBSERVATION` | **LIVE-EVIDENCED (hedged in its own source)** | Same D-63 review, same sentence, continuing: "and arguably under `incident` ('a discrete reported event — fall, accident, injury, hospitalization')." The review's own word "arguably" is a hedge, but it is a NAMED, CITED analytical finding, not silence — kept as evidenced, hedge preserved by quoting the review's own word rather than upgrading it to unqualified certainty. |
| `care_plan` ↔ `FUNCTIONAL_SUPPORT_STATE` | **LIVE-EVIDENCED (indirect, but real)** | D-144's own probe confirms the absorption mechanism. No review sentence names `care_plan` explicitly, but `CANONICAL_ATTRIBUTES`' own description ("a recipient's documented care plan or **care-team-agreed course of action**") matches the D-63 review's own R4-sourcing "Layer 2: Functional support state" example — "Repeat appointment reminders are **currently enabled**" — closely enough to count as real, traceable support, not a guess. |
| `health_condition` ↔ `FUNCTIONAL_SUPPORT_STATE` | **PLAUSIBLE BUT UNEVIDENCED — DROPPED** | No citation anywhere: not in the D-63 review (which discusses functional support state only via the Layer-2 example above, never ties it to `health_condition`), not in D-144's survey (which tested `care_plan` for this class, never `health_condition`), not in `eval/sia_golden_set.json`'s 8 `health_condition` entries (all condition-query-shaped, none support-arrangement-shaped). `CANONICAL_ATTRIBUTES`' own `health_condition` description ("diagnosed or reported health **conditions**") actively argues against it — an ongoing support **arrangement** is not a diagnosed **condition**. The claim traces to D-140's own docstring phrase "the same shape-collision, **generalized**" — an analogical extension written at build time, not a probed or cited finding. |

**The STOP condition (item 1) does not fire**: the code is the narrow one, but the prose
is NOT shown to be right for the one pairing it claims beyond the code — the opposite:
available evidence argues against that one claim. 3 of 4 pairings are evidenced and
already match the code exactly; only the 4th needed dropping.

### Why "produce the evidence, don't assert it" (item 2) landed on narrowing, not widening

Producing evidence FOR `health_condition`↔`FUNCTIONAL_SUPPORT_STATE` would require either
a citation (none exists, checked directly) or a live extraction-model probe showing a
genuine ADL/mobility utterance gets classified as `attribute="health_condition"` rather
than `"care_plan"` by the real extraction path — not attempted, because
`CANONICAL_ATTRIBUTES`' own two descriptions already point the OTHER way (a support
arrangement matches `care_plan`'s definition, not `health_condition`'s), making a
positive probe result unlikely enough that the evidence-gathering itself would need to
overturn the attribute vocabulary's own stated design rather than merely confirm it —
out of proportion to what this dispatch asked for, and not what the evidence in hand
supports.

## VERIFIED

**Watched, direct:**
- `docs/reviews/D63_dimensioned-ceiling-axes__fable-and-chatgpt__v20260731_1917.md` read
  in full for both relevant sections (Axis 1's candidate-content table, and the
  Layer 1-5 section R4's own text is sourced from).
- `docs/dispatches/DISPATCH_R8_R10_RULINGS__...`'s absorption-survey table re-read
  directly, not recalled.
- `eval/sia_golden_set.json`'s 8 `health_condition`-attributed entries read individually
  (`json.load` + filter, printed and read one by one).
- `harness/extraction_queue.py:157,190` — both `CANONICAL_ATTRIBUTES` descriptions read
  directly.
- `harness/representation_class.py`'s `_UNDETERMINED_CANDIDATES_BY_ATTRIBUTE` and
  `undetermined_candidates()` re-read in full, confirmed unchanged and already correct —
  not assumed from D-158's own report.
- `eval/test_ceiling_representation_class.py` + `eval/test_ceiling_representation.py`:
  105 passed, byte-identical count to immediately after D-158 (confirming the docstring
  edit changed no test-observable behavior).
- `./scripts/run_harness.sh --layer 7`: RATCHET PASS.
- `eval/memory_harness.py`: 13/17, failing set exactly `{MEM-115, MEM-116, MEM-117,
  MEM-118}`.
- `git diff --stat` on `harness/representation_class.py` before committing: confirmed
  the ONLY hunk touched is the FUNCTIONAL_SUPPORT_STATE docstring paragraph — no
  executable line changed.

**Reasoned about, not independently re-derived:** that the D-63 review's own "Layer 2"
example genuinely corresponds to `care_plan` (rather than some other or no attribute) is
an inference from matching two independently-written descriptions (the review's example,
`CANONICAL_ATTRIBUTES`' own text) — not a citation stating the correspondence explicitly
in either source.

## HASH

Staged for commit: `harness/representation_class.py` (docstring only), this dispatch
doc. No other file changed.

## OPEN

- **The `incident`↔`COGNITIVE_OBSERVATION` pairing carries its source review's own hedge
  ("arguably")** — kept as evidenced rather than dropped, since a hedge is not silence,
  but named here so a future reader does not read it as equally certain to the other
  three.
- **Whether a live extraction-model probe would actually confirm or refute
  `health_condition`↔`FUNCTIONAL_SUPPORT_STATE`** was not run — the available evidence
  argues against it strongly enough that this dispatch judged the probe disproportionate
  to what was asked; a future dispatch could still run it if the question resurfaces.
- **Nothing ruled MET.**

## RECAP
D-159: surveyed all FOUR pairings the marker docstring's prose actually asserts (not
three — both Group-3 entries separately named `health_condition`). Three are evidenced
(two via the banked D-63 review's own explicit Axis-1 analysis, one via D-144's probe
plus a close match to the same review's R4-sourcing Layer-2 example) and already match
D-158's code exactly. One (`health_condition`↔`FUNCTIONAL_SUPPORT_STATE`) has no
citation anywhere and is contradicted by `CANONICAL_ATTRIBUTES`' own description —
dropped from the docstring, recorded not deleted, matching D-158's code which was
already correct. Reconciled in one direction (narrowed the prose), not split. No code
changed; acceptance explicitly skipped, stated not implied. `--layer 7` RATCHET PASS,
memory harness 13/17 inside pin. Nothing ruled.
