# DISPATCH_R4_R8_EXPLICIT_UNKNOWN
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R4 and R8 (amended this dispatch, item 1 — the second, explicit-unknown limb of D-157's own
amendment).

## THE ASK

Dispatch text, verbatim:

```
=== D-158 | ~/hip-roadmap, roadmap | R4/R8: the explicit-unknown limb ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R4/R8, the amendment landed at D-157.

D-157 established with executed evidence that origin carries no positive signal for
COGNITIVE_OBSERVATION/FUNCTIONAL_SUPPORT_STATE, and that pure refusal breaks the
everyday health path (3 of 72 cases, health_condition/incident/care_plan under
self_report). Bill's ruling had TWO limbs — "it refuses, OR CARRIES AN EXPLICIT
UNKNOWN." Only refusal was built. This dispatch builds the other limb.

BILL'S RULING, the requirement text:
"Where a class cannot be honestly determined, the fact is stored with its best
attribute-derived class AND carries a recorded marker that the class was undetermined
between named candidates. The record shall not claim a certainty it does not have.
This is honest bookkeeping, not protection — the fact still sits in the broader class
and is still visible to that class's audience. Differential retention or audience for
these classes requires content-based assignment, which stays deferred as its own
decision."

1. AMEND THE REQ FIRST from those words, including the stated limit. Item 8 applies.
   Record that content-based assignment remains deferred and why — the Principle 6
   collision gets examined on its own, not appended to a build.
2. BUILD: the marker names WHICH candidates were undetermined, not merely that
   something was. A bare "unknown" flag repeats the original defect one level up.
   Facts whose class IS honestly determined carry no marker — the marker must
   discriminate, or it is decoration.
3. THE THREE CASES D-157'S PROBE BROKE ARE YOUR ACCEPTANCE FIXTURE. They must now
   PASS, carrying the marker, rather than be refused. Report each individually.
4. Acceptance per D-87: executed fault twin proving an undetermined fact that carries
   NO marker is caught, plus anti-vacuity proving the marker is not applied to
   everything. Report whether A8 becomes writable. Do not re-tier.
5. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
6. Rule nothing MET.
```

## WHAT WAS DONE

1. Gate checked — matched. Repo lock acquired. **Found an unpushed, fully-committed
   local commit already sitting on `roadmap`** (`b6a7f63`, "REQ_UNRESOLVED_SUBJECT_GUARD
   filed"), landed by another lane sharing this same checkout between D-157's push and
   D-158's start, while the lock was free — confirmed unpushed
   (`git branch -r --contains b6a7f63` returns nothing) and fully committed (not
   uncommitted WIP). Left exactly as found, built on top of it, did not push it
   independently or touch it — flagged in OPEN, not acted on.
2. **Item 1 — amended R8's text FIRST**, immediately after D-157's own amendment,
   verbatim from Bill's ruling, including the stated limit (no retention/audience
   change; content-based assignment stays deferred, named as a D-50 Principle 6
   collision to be examined on its own).
3. **Item 2 — built the marker** in `harness/representation_class.py`:
   `_UNDETERMINED_CANDIDATES_BY_ATTRIBUTE` (the specific, evidenced pairings — see WHAT
   WAS FOUND) and `undetermined_candidates(*, attribute, origin)`, returning the named
   candidate set or `None`. Wired into `memory_engine/store.py::create_fact_node`:
   computed alongside (not instead of) the existing `classify_representation()` call,
   stamped as a NEW property `representation_class_undetermined` (added to
   `_CREATE_FACT_CQL` so `_FACT_PROP_KEYS` — itself regex-derived from the CQL, per this
   file's own drift-proof convention — picks it up automatically).
4. Verified live, directly, before writing any test: `classify_representation()`'s
   returned class is UNCHANGED for all three attributes (still `HEALTH_CLAIM`) and the
   marker correctly discriminates (ambiguous attributes get the named pair; ordinary
   attributes like `medication`/`preference`/`address` get `None`; `fixture` origin gets
   `None` even for the ambiguous three).
5. **Item 3 — the three D-157-broken cases as the acceptance fixture**: wrote a
   parametrized test (`health_condition`/`incident`/`care_plan` × `self_report`/
   `extraction`, six cases) asserting each now classifies normally (not refused) AND
   carries its correct marker — see WHAT WAS FOUND for each reported individually.
6. **Item 4 — acceptance**: an executed fault twin at the pure-function level (wiping
   `_UNDETERMINED_CANDIDATES_BY_ATTRIBUTE`, proving the real tests depend on real table
   content) and a SECOND fault twin at the creator-path level (monkeypatching
   `harness.representation_class.undetermined_candidates` itself — matching this
   codebase's own established pattern for patching a function `create_fact_node`
   re-imports on every call, the same shape
   `test_ceil_a8_fault_twin_broken_classifier_goes_red` already uses for
   `classify_representation`) — proving the creator's OWN stamping, not just the pure
   function, depends on real wiring. Anti-vacuity: 16 ordinary attributes parametrized,
   all confirmed marker-free; the demo seed's own 11 fixtures confirmed marker-free
   (D4's `incident`/`fixture` included).
7. Ran `eval/test_ceiling_representation_class.py` standalone (86 passed) and combined
   with `eval/test_ceiling_representation.py` (101 passed) — clean on first run, no
   fixups needed.
8. Ran the full standing-battery list (24 files): **487 passed, 9 xfailed** —
   +33 over D-152's last recorded baseline (454/9), exactly this dispatch's own addition
   (29 in the classifier-level file, 4 in the creator-path file).
9. Ran `./scripts/run_harness.sh --layer 7`: AUDIT 8/8, DISC 1/1, L7 27/27, L7V2 27/28,
   **SCHEMA 1/1 (ORTH-2, 46 cases — the real fact-schema conformance corpus, unaffected
   by the new property)**, VOICE 1/1, **RATCHET PASS**.
10. Ran `eval/memory_harness.py` under a manually-held `graph:7688` lock (the script does
    not self-acquire one): **13/17 passed**, failing set exactly
    `{MEM-115, MEM-116, MEM-117, MEM-118}` — inside the pinned range, not the 16/17 STOP.
11. Wrote this dispatch doc, fixed the REQ amendment's own forward-reference to this
    doc's real filename (written after the timestamp was picked, per the established
    self-correction discipline — checked before committing, not after).
12. Staged by explicit pathspec, committed, pushed, verified post-commit, released the
    lock.

## WHAT WAS FOUND

### The marker's exact content (item 2) — evidenced pairings, not the docstring's wider prose

`harness/representation_class.py`'s own Group 3 docstring (D-140) uses broader language
("FUNCTIONAL_SUPPORT_STATE... shares attribute space with ordinary health_condition/
care_plan facts") than what this build encodes. **Deliberately narrower**: the marker
uses only the SPECIFIC, live-probed pairings D-144's absorption survey actually tested
(`docs/dispatches/DISPATCH_R8_R10_RULINGS__...`'s own table):

```
health_condition  ->  {HEALTH_CLAIM, COGNITIVE_OBSERVATION}
incident           ->  {HEALTH_CLAIM, COGNITIVE_OBSERVATION}
care_plan          ->  {HEALTH_CLAIM, FUNCTIONAL_SUPPORT_STATE}
```

Widening this to match the docstring's fuller prose (e.g., adding
`FUNCTIONAL_SUPPORT_STATE` to `health_condition`'s own candidate set) is a future
finding needing its own live evidence, not assumed here from prose alone — named in
OPEN.

### Item 3 — each of D-157's three broken cases, reported individually

All three now PASS (not refused), and each carries its named marker, verified directly:

| attribute | origin | `classify_representation()` | `undetermined_candidates()` |
|---|---|---|---|
| `health_condition` | `self_report` | `HEALTH_CLAIM` (unchanged) | `{COGNITIVE_OBSERVATION, HEALTH_CLAIM}` |
| `incident` | `self_report` | `HEALTH_CLAIM` (unchanged) | `{COGNITIVE_OBSERVATION, HEALTH_CLAIM}` |
| `care_plan` | `self_report` | `HEALTH_CLAIM` (unchanged) | `{FUNCTIONAL_SUPPORT_STATE, HEALTH_CLAIM}` |

Same three, also confirmed under `extraction` (the other real production origin that
reaches these attributes, per D-157's own finding that origin doesn't distinguish
candidates — only the fixture/non-fixture split matters) — identical results, six cases
total, all green.

### The creator, not just the pure function, stamps it (item 3/4)

`eval/test_ceiling_representation.py`'s new tests assert against the REAL creator path
(`create_fact_node` with a recording tx, this file's own established A8 convention — no
live graph needed, the same mock-tx pattern the file already uses): `health_condition`/
`self_report` stamps `representation_class_undetermined = ["COGNITIVE_OBSERVATION",
"HEALTH_CLAIM"]` on the CREATE map; `medication`/`self_report` and `health_condition`/
`fixture` both stamp `None` (which Neo4j drops entirely at persistence, per this
codebase's own established null-omission convention — not asserted against a live graph
here, but consistent with how every other `None`-valued property in `_CREATE_FACT_CQL`
already behaves).

### A8's writability (item 4) — unaffected, not re-tiered

**A8 is already LIVE** (verified by D-149's runner cross-check) and this build changes
NOTHING about what makes it so: `classify_representation()`'s return value is byte-
identical before and after this dispatch for every attribute, including the three this
build's marker touches. This dispatch adds a wholly SEPARATE, additive property; it does
not alter A8's own mechanism, acceptance criteria, or evidence. **A8's tier is
unaffected — not re-tiered, because there is nothing about it to re-tier.**

## VERIFIED

**Watched, executed:**
- Direct probe (`python3 -c ...`) of `classify_representation`/`undetermined_candidates`
  across all three ambiguous attributes, three ordinary attributes, and all origins,
  read line-by-line before any test was written.
- `eval/test_ceiling_representation_class.py` standalone: 86 passed (29 new).
- `eval/test_ceiling_representation_class.py` + `eval/test_ceiling_representation.py`:
  101 passed (33 new total, 4 in the creator-path file).
- Full standing-battery list (24 files): 487 passed, 9 xfailed (+33 over D-152's 454/9).
- `./scripts/run_harness.sh --layer 7`: AUDIT 8/8, L7 27/27, L7V2 27/28, SCHEMA 1/1
  (ORTH-2, 46 cases — real fact-schema conformance, confirms no downstream schema
  consumer broke), VOICE 1/1, RATCHET PASS.
- `eval/memory_harness.py`, correct interpreter, manually-held `graph:7688` lock:
  13/17, failing set exactly `{MEM-115, MEM-116, MEM-117, MEM-118}`.
- `git status`/`git show --name-only` before and after commit: confirmed only this
  dispatch's own files landed; the cutover lane's untracked files and `b6a7f63` (the
  other lane's own unpushed commit, now an ancestor of this one, untouched in content)
  both exactly as found.

**Reasoned about, not independently re-derived:** that the marker's candidate pairings
are the CORRECT and COMPLETE set for each attribute rests on D-140's/D-144's own prior
survey work, taken as evidenced input, not re-probed against fresh live data this
dispatch.

## HASH

Staged for commit: `harness/representation_class.py`, `memory_engine/store.py`,
`eval/test_ceiling_representation_class.py`, `eval/test_ceiling_representation.py`,
`docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
(R8 amendment), this dispatch doc.

## OPEN

- **An unpushed commit from another lane (`b6a7f63`, "REQ_UNRESOLVED_SUBJECT_GUARD
  filed") was found already sitting on this checkout's `roadmap` branch**, ahead of
  origin, before this dispatch started. Left exactly as found and built on top of, per
  standard practice for a fully-committed (not partial/uncommitted) change — but this
  dispatch's own push will carry it to origin as a side effect, since it's already an
  ancestor. Flagged so it isn't read as this dispatch's own work if noticed later.
- **The marker's candidate set is deliberately narrower than D-140's own docstring
  prose** (see WHAT WAS FOUND) — widening it to match, or confirming the narrower set is
  correct, needs its own live-evidenced pass, not attempted here.
- **The `representation_class_undetermined` property's real-graph null-omission
  behavior was not verified against a LIVE Neo4j write in this dispatch** — confirmed
  only via the recording-tx mock (this file's own established convention for A8's
  creator-path tests, not a gap unique to this build) and by analogy to every other
  `None`-valued `_CREATE_FACT_CQL` property already behaving this way in production.
- **Content-based assignment remains deferred**, per the REQ amendment's own stated
  limit — this build does not open that question.
- **Nothing ruled MET.**

## RECAP
D-158: built the explicit-unknown limb of R4/R8's amendment — a marker naming WHICH
candidate classes (not a bare flag) a fact might honestly be, for the three attributes
D-157 found ambiguous. All three of D-157's broken cases now PASS, unchanged in their
assigned class, carrying the correct marker — reported individually. Facts with an
honestly-determined class carry no marker (verified for 16 ordinary attributes + the
demo seed's own 11 fixtures). Two executed fault twins (pure-function and creator-path)
plus anti-vacuity, all green. A8 unaffected, not re-tiered — its own mechanism didn't
change. 487/9 batteries (+33), `--layer 7` RATCHET PASS including ORTH-2's real schema
conformance, memory harness 13/17 inside pin. Nothing ruled.
