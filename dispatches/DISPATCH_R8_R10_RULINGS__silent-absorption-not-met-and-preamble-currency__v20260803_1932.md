# DISPATCH_R8_R10_RULINGS
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD (docs-only: two rulings recorded, a read-only survey, a preamble-currency
check, one already-satisfied item verified rather than repeated — no production code changed,
per the dispatch's own preamble)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`,
R8 (write-time representation class), R10 (category controls by origin).

## THE ASK

Dispatch text, verbatim:

```
=== D-144 | ~/hip-roadmap | R8 and R10 rulings, preamble staleness, INDEX residuals ===
STANDARD PREAMBLE. Docs + read-only survey. No production code changes.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R8, R10.
NOTE: D-143 landed the R2 ruling and R2's clause survey. Do not repeat either.

1. RECORD R8 NOT MET in §16, on the SILENT-ABSORPTION ground, expressly not the
   absence ground. Bill's words verbatim:
   "NOT MET, on the silent-absorption ground rather than the absence ground. The
   distinction matters for what happens next — if you rule on absences, the fix is
   'build the missing classes.'"
   Record the ground: R8 requires every stored fact to carry one of fourteen classes;
   attribute-name lookup means a cognitive-decline observation lands as HEALTH_CLAIM
   and a fact about a non-enrolled person lands as ORDINARY_CLAIM. Four categories
   are silently absorbed into broader ones rather than left blank — a hole that reads
   as filled. D-140's build is NOT rejected.

2. RECORD R10 NOT MET. Reason: all four revalidations fire at create_fact_node
   (D-140 verified empirically), but two rest on requirements ruled NOT MET the same
   day. A10 stays xfail(strict=True), untouched. Do not re-tier.

3. SURVEY R8'S ABSORPTION, read-only, evidence not inference: for each of the four
   absent classes, name what a fact of that kind is CURRENTLY stamped as, and by
   which lookup entry.

4. NOTE in §16 that A2 and A8 are both now WRITABLE and neither has ever been written
   or run. Neither requirement has an executed acceptance.

5. FIX THE PREAMBLE STALENESS — Bill's standing instruction, given here. The §16 intro
   and header preamble have been flagged stale four times. Bring both current:
   MET R1, R12, R18, R29, R30. NOT MET R2, R8, R10.

6. INDEX RESIDUALS owed from D-130: its dispatch doc and TD-151's debt-register
   version bump were never registered. Add both rows.

7. Rule nothing else. Report LONG to a dispatch doc.
```

## WHAT WAS DONE

1. Gate checked (`bill-ai` / `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]/hip-roadmap` /
   `roadmap`) — matched. Tree confirmed `ahead 0 / behind 0`, both at the start and
   re-confirmed immediately before commit.
2. Lock read first (absent), taken noclobber: `holder: D-144 (R8/R10 rulings, preamble
   staleness, INDEX residuals)`.
3. **Item 6 checked BEFORE doing anything else**, since its text overlaps D-143's own work:
   grepped `docs/INDEX.md` for the two rows D-143 registered — both present, exactly once
   each, no duplicates. Item 6 is ALREADY SATISFIED by D-143; not repeated, per the same logic
   the dispatch's own NOTE applies to item 1/2's R2 content. See WHAT WAS FOUND.
4. Read `harness/representation_class.py` directly (`_ATTRIBUTE_CLASS_MAP`, `ABSENT_CLASSES`)
   and ran `classify_representation()` live against concrete cases for all four absent classes,
   including dad's own real D4/D5 fixture attributes, to build the survey table with verified,
   not inferred, evidence.
5. Checked `REQ_CEILING_ACCEPTANCE__testing-plan-for-the-ceiling-sprint__v20260801_0617.md`
   directly for A2/A8's current tier (still UNWRITABLE, both, unedited) and grepped `eval/` for
   any test literally named to match that framework — none exists; flagged the naming
   coincidence between this session's own `test_ceil_a8_*` convention (D-140) and the formal
   A8 row, which are NOT the same thing.
6. Read the REQ document's top-of-file header (`:1-22`) and §16's intro paragraph (`:1061`)
   directly, in full, to check for staleness. Found both already correctly pointer-shaped (no
   count, no enumeration) per D-131 — verified, not assumed.
7. Recorded R8's NOT MET ruling in §16 (new dated entry, D-140's prior "reported, not ruled"
   entry annotated historical, not rewritten), including the absorption survey table and the
   A2/A8 finding.
8. Added a D-144 addendum to R10's existing D-100 entry (already once corrected by D-143),
   updating the "one leg ruled, one leg unruled" framing to "both legs now ruled NOT MET."
9. Since the header and §16 intro were both already current in the sense of "carries no stale
   count" (nothing to fix there), extended each location's own established historical-
   narrative convention with a brief, non-count clause naming today's three rulings — matching
   the existing pattern (`R1 and R10 were ruled together at D-100`, `R12 was ruled in two
   stages`) rather than reintroducing anything count-shaped. See WHAT WAS FOUND for why this
   was judged the correct scope for item 5, rather than a larger rewrite.
10. Wrote this dispatch doc.
11. Staged by explicit pathspec, committed, pushed, released the lock.

## WHAT WAS FOUND

### R8's silent-absorption survey (item 3)

`ABSENT_CLASSES` is exactly the four D-140 already named:
`COGNITIVE_OBSERVATION, FUNCTIONAL_SUPPORT_STATE, EXTERNAL_PROFESSIONAL_DIAGNOSIS,
THIRD_PARTY_NONCARE_DOSSIER`. Live-probed against `harness.representation_class
.classify_representation`:

| absent class | stamped as | lookup entry | live evidence |
|---|---|---|---|
| `COGNITIVE_OBSERVATION` | `HEALTH_CLAIM` | `"health_condition"`/`"incident"` | `classify_representation(attribute="health_condition", origin="self_report", subject="dad")` → `HEALTH_CLAIM` |
| `FUNCTIONAL_SUPPORT_STATE` | `HEALTH_CLAIM` | `"care_plan"` | `classify_representation(attribute="care_plan", ...)` → `HEALTH_CLAIM` |
| `EXTERNAL_PROFESSIONAL_DIAGNOSIS` | `HEALTH_CLAIM` | `"health_condition"` (origin never consulted) | `classify_representation(attribute="health_condition", origin="attributed_import", ...)` → `HEALTH_CLAIM` |
| `THIRD_PARTY_NONCARE_DOSSIER` | whatever the attribute alone maps to — no fixed entry | any of 19, since `subject` is never consulted (removed during D-140's own build) | dad's real D4 (`attribute="incident"`) → `HEALTH_CLAIM`; D5 (`attribute="medication_status"`) → `HEALTH_CLAIM`; a hypothetical `attribute="preference"` for the same subject → `ORDINARY_CLAIM`; `attribute="address"` → `LOCATION_STATE` |

The fourth row is the sharpest illustration of "silent absorption" as its own failure mode,
distinct from "unbuildable": there is no SINGLE class `THIRD_PARTY_NONCARE_DOSSIER` facts land
in — they scatter across whichever class the attribute happens to produce, because the one
signal (`subject`) that would identify them is not consulted at all.

### A2/A8: writable, unexecuted, and a naming coincidence flagged

`REQ_CEILING_ACCEPTANCE__...:47,203,208` lists A2 and A8 among 16 UNWRITABLE rows, unedited
since filing — confirmed by direct read, not recalled. No test anywhere is wired to that
formal framework for either row (a repeat of D-143's own A2 finding; extended to A8 here).
**Flagged plainly, not silently left ambiguous:** `eval/test_ceiling_representation_class.py`'s
57 cases (D-140) use a `test_ceil_a8_*` naming prefix, matching this codebase's general
`test_ceil_a<N>_*` convention (documented in `eval/test_ceiling_inference.py`'s own docstring)
— that prefix is NOT a claim that this file IS the formal A8 acceptance row, and it does not
re-tier `REQ_CEILING_ACCEPTANCE`'s A8 entry. Real, substantial, passing code coverage exists;
an EXECUTED ACCEPTANCE in the formal sense does not.

### Header and §16 intro: already current, not stale — a narrower fix than the dispatch's
### framing implied

Both were read directly. The header (`:3-4`) already says "This header deliberately carries no
count and no enumeration" (D-131). §16's intro (`:1061`) already says the identical thing for
itself. Neither has regressed to a count since D-131 landed — confirmed by direct read, not by
trusting the D-131 dispatch's own claim that it would hold. **There is no stale NUMBER to fix in
either location** — D-131's "pointer, not a count" design is doing exactly what it was built to
do: nothing ages here because nothing here is a count.

What WAS missing, and what item 5 is read to actually be asking for: neither location's
historical-narrative thread (the non-count, prose-only "R30's backfill question was answered
first... R1 and R10 were ruled together at D-100... R12 was ruled in two stages" sentence, and
the header's own "Filed:" amendment chain) had been extended to mention today's three rulings.
Both extended, in the SAME prose-only, non-enumerated style the existing sentences already use
— not a new count, not a new list, a continuation of the narrative D-131 explicitly preserved
("Historical narrative retained because it is history, not a count").

### Item 6: already satisfied by D-143, verified not repeated

Both residual rows (D-130's dispatch doc; the `techdebt/` pointer row's TD-151 update) were
confirmed present, exactly once each, via direct grep of the current `docs/INDEX.md` before any
other work in this dispatch began. This dispatch's own NOTE ("D-143 landed the R2 ruling... do
not repeat") applies by the same logic to item 6, even though the NOTE's literal text only
named items 1/2 — repeating a completed INDEX registration would create a duplicate row, a
worse outcome than simply verifying and reporting.

## VERIFIED

**Watched run:** `harness.representation_class.classify_representation` called live for all
four absorption examples plus dad's two real fixture attributes, output captured directly (see
survey table above). `REQ_CEILING_ACCEPTANCE__...md` read directly for A2/A8's tier. `eval/`
grepped directly for any formal-framework test matching A2/A8; zero hits beyond this session's
own informally-named `test_ceil_a8_*` file. `docs/INDEX.md` grepped directly for both D-130
residual rows before touching anything — one hit each, confirmed already present.

**Reasoned about:** that item 5's intent, given the header/§16-intro are already correctly
pointer-shaped, is best satisfied by a narrative extension rather than a larger rewrite is this
session's own judgment call, explained above rather than asserted. The "historical-narrative
thread is what's actually missing" reading is inference from the dispatch's own phrasing
("bring both current" alongside a ground-truth MET/NOT-MET list) plus direct observation that
no count-shaped text exists to be brought current — not something stated outright by the
dispatch itself.

## HASH

Staged for commit alongside this doc:
`docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
(§16: R8 NOT MET ruling + absorption survey, R10 addendum, header/§16-intro narrative
extensions). `docs/INDEX.md` NOT touched this dispatch (item 6 already satisfied, verified not
re-edited).

## OPEN

- **R8's four absent classes remain unbuilt, and are now explicitly ruled unbuilt-by-
  absorption rather than merely unwritten.** Whether the fix is a subject-aware or content-
  aware extension to the classifier (and if content-aware, how that squares with D-50
  Principle 6 — the same collision D-140's own survey already found for `COGNITIVE_OBSERVATION`
  and `FUNCTIONAL_SUPPORT_STATE` specifically) is not decided here.
- **R2 and R8 are both NOT MET; A2 and A8 both writable, neither executed.** Whether either
  requirement should get a formal acceptance row written and run, independent of any further
  build, is Bill's call.
- **R10 stays NOT MET on two now-ruled legs.** Whether R10 itself should be revisited, narrowed,
  or left exactly as filed once R2/R8's underlying gaps are eventually closed is not decided
  here.
- **Nothing else ruled**, per instruction.
