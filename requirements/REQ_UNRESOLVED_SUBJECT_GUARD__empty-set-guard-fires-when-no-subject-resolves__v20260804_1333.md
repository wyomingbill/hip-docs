# REQ_UNRESOLVED_SUBJECT_GUARD
Status: SUPERSEDED
Reconciled-Against: ef99a9c (2026-08-04)

> **SUPERSEDED 2026-08-04 (Index Demo 26) by
> `REQ_UNRESOLVED_SUBJECT_GUARD__sensitive-facts-not-admitted-on-subjectless-turns__v20260804_2104.md`.**
> **Bill's ruling: PATH 1 — FIX ADMISSION, NOT REFUSAL.**
> This version's fix was **built exactly as ruled at Index Demo 25 (D-D-149, `d9eac55` on
> `demo-cutover-build`)** and **passed everything it was specified against** — B090 refused
> structurally with exact telemetry (`guard_triggered=true`, `guard.kind=empty_set`,
> `inference_ms=null`), DC-061/DC-080 unguarded, `DISC:conformance` 39/39, standing battery
> zero delta (293/8 both ways). **It then refused ordinary knowledge turns:** "What is the
> capital of Brazil?" returned the empty-set template where pristine answers "The capital of
> Brazil is Brasília." **Cause, established from the graph:** fact `9073c508…`
> (`attribute=household`, `sensitivity=medium`, `origin=self_report`) is admitted into EVERY
> subjectless turn by design, so `result.allowed` always holds a `>= medium` fact and a
> refusal-side guard reading that set fires on everything. **The threshold was right and the
> point in the pipeline was wrong — the threshold is not the lever, admission is.** The
> successor moves the gate to injection and keeps this version's guard as the BACKSTOP.
> **Nothing below is edited** — this document is retained intact as the record of what was
> believed before it was executed, including its own OPEN item asking whether household facts
> should be admitted on a subjectless turn at all, which D-D-149 answered with executed
> evidence. Read the successor for the operative requirement and its acceptance test.
> **The slug changed in the successor**, deliberately: the guard firing is no longer the
> requirement. Nothing was MET by this version and nothing is MET by its successor.

**SUPERSEDES `REQ_UNRESOLVED_SUBJECT_GUARD__empty-set-guard-fires-when-no-subject-resolves__v20260804_0806.md`**
(filed `b6a7f63`, Index Demo 12). That version's PROPOSED FIX was built exactly as
written at Index Demo 14 and **regressed the standing battery**. It was reverted, never
committed. The premise is revised here; the prior version is retained unaltered as the
record of what was believed before it was executed.

## AMENDMENT RECORD (Index Demo 15, 2026-08-04)

### 1. EXECUTED EVIDENCE

The fix as specified in v20260804_0806 — INJ-6c keyed on `result.allowed`, placed beside
INJ-6, `has_personal_subject` left untouched — **was built and reverted**.

`eval.harness --layer 7`, run against pristine HEAD *and* against the change so the delta
is attributable rather than assumed:

| Check | Pristine HEAD | With INJ-6c |
|---|---|---|
| `DISC:conformance` (39 cases) | **1/1 PASS** | **0/1 FAIL** |
| `L7V2` | 26/28 | 25/28 |
| `MUTATION-SCORE-SELFTEST` | pass | FAIL (tooling — see TD-R-161) |
| `MUTATION-NO-SILENT-DISAPPEARANCE` | **FAIL** | FAIL (**pre-existing, not caused here**) |
| `L7` 27/27, `SCHEMA`, `VOICE`, `AUDIT` 8/8 | pass | pass |

```
RATCHET FAIL — regressed vs baseline: ['DISC:conformance']
       [FAIL] failed 2/39 cases — DC-061; DC-080
```

Exactly two cases broke, quoted by their own descriptions:

- **DC-061** (group `never_volunteer`) — *"INJ-5 + INJ-4: household facts admitted even on
  knowledge intent; personal facts blocked"*. `expected: guard_triggered: False`,
  `admitted_count: 1`, `admitted_fact_ids: ['f-hh']`.
- **DC-080** (group `household_facts`) — *"INJ-4: multiple household facts always admitted
  for any authenticated member — bypasses INJ-1/INJ-3"*. `expected: guard_triggered: False`,
  `admitted_count: 2`.

Both are subjectless, non-declarative, knowledge-intent turns with household facts in
`result.allowed` — precisely the condition INJ-6c fires on.

### 2. THE REQUIREMENTS CONFLICT

**ORTH-1's disclosure contract encodes as CORRECT the behaviour this REQ called the
defect.** DC-061 and DC-080 do not merely tolerate household facts entering a subjectless
knowledge turn unguarded — they *assert* it, and have asserted it as standing contract
since before this REQ existed.

The implementation matched the REQ. **The REQ was wrong.** No amount of coding closes
this: any implementation faithful to v20260804_0806 fails these two cases, and any
implementation that passes them is not the fix that version specified. This was a
requirements defect wearing the costume of a build task, and it could only surface by
executing it.

### 3. THE REVISED PREMISE

`result.allowed` **cannot separate the two cases.** Both are `owner=household` facts
admitted on a subjectless knowledge turn:

- "trash pickup is Wednesday" reaching a general-knowledge answer — **acceptable**
  (DC-061/DC-080 say so).
- "[REDACTED-HOME-ADDRESS]" reaching a routing answer — **a leak** (B090).

Membership in `result.allowed` is identical for both. The predicate is blind to the only
thing that actually differs.

**The discriminator is SENSITIVITY.**

**Bill's ruling (Index Demo 15 dispatch, 2026-08-04), recorded as given:** pursue
sensitivity; **do NOT amend ORTH-1** and **do NOT accept the leak**. Both escape routes —
relaxing the contract, or ruling the address disclosure acceptable — are closed by
ruling, not by analysis.

### 4. WHAT THE ORIGINAL REQ MISSED

v20260804_0806's CONSTRAINTS anticipated the wrong failure. It said:

> **Ordinary general-knowledge turns must keep working.** A turn that admits no facts must
> not refuse.

It guarded the **admits-nothing** case and wrote Test 2 to enforce it. **DC-061 and DC-080
are turns that DO admit facts and must still not refuse.** That case was unforeseen. The
`result.allowed` clause was described in that version as "the load-bearing clause… what
confines the new refusal to turns where facts WOULD ACTUALLY have entered the prompt" —
correct as far as it went, and exactly the wrong axis.

## SENSITIVITY: WHAT ACTUALLY EXISTS (verified, not assumed)

Checked before writing, per the dispatch. **The discriminator exists.** It is not
hypothetical and was not invented for this REQ:

- **`harness/sensitivity.py`** — the canonical registry (authority: `REQ_STRUCTURAL_CEILING`
  R29/R30, closing TD-137 at D-75). Four-valued, order authoritative:
  `low`=10, `medium`=20, `high`=30, `critical`=40. `SENSITIVITY_REGISTRY_VERSION = "sensitivity.v1"`;
  pre-registry facts carry `PRE_REGISTRY = "pre-registry"`.
- **`sensitivity` is a stored property on the Fact node**, not a derived value — read as
  `f.sensitivity` in `memory_engine/recall.py:81` and `memory_engine/api.py:140,164`, and
  returned in the fact dict (`api.py:251`), so **facts reaching
  `apply_injection_contract` already carry it**.

Live values, queried against the roadmap graph (7688) rather than read off the seed:

| attribute | value | sensitivity |
|---|---|---|
| `address` | "[REDACTED-HOME-ADDRESS]" | **medium** |
| `household` | "trash pickup is Wednesday" | **low** |
| `zone_district` | "R-1-18" | low |
| `schedule` | — | low |
| `medication` | — | high |
| `risk_pattern` | — | high |

**A threshold at `>= medium` separates the two cases exactly**: it guards B090's address
while leaving DC-061/DC-080's `low` household facts admitted and unguarded.

**Three obstacles, named rather than waved past — none is a reason not to proceed, and
all three are build work this REQ has not authorized:**

1. **`harness/injection_contract.py` never references sensitivity.** Verified by grep: the
   string does not appear in the file. Every INJ rule keys on attribute/owner/subject. The
   field is present in the fact dicts but has never been read here.
2. **The ORTH-1 fixtures carry no sensitivity field at all.** DC-061's and DC-080's facts
   have exactly `['attribute', 'fact_id', 'owner', 'subject', 'value']`. A guard reading
   `fact.get("sensitivity")` gets `None` on every conformance case. The fixtures must gain
   the field, or the guard needs a ruled policy for its absence.
3. **Absence cannot be defaulted silently, and today it is.** `sensitivity.rank()` RAISES
   `UnknownSensitivity` by design — R29/R30 forbid defaulting because "a returned default
   is a downgrade wearing a different name." But the read layer *already* defaults:
   `recall.py:249` and `api.py:241` both do `row["sensitivity"] or "medium"`. A
   sensitivity-gated guard would inherit that default and treat every null-sensitivity
   fact as `medium` — i.e. **guard it**. Whether that is right is a ruling, not an
   implementation detail, and it is flagged here as an OPEN question rather than answered.

## DEFECT (carried forward, unchanged in mechanism)

`harness/injection_contract.py:654` — `has_personal_subject = bool(resolved_subjects)`.
INJ-6 (`:797`) and INJ-6b (`:813`) are both gated on it, so when `resolved_subjects == []`
**neither guard runs**, while INJ-1 (`owner == "household"` unconditional), INJ-2
(household returns `True`) and INJ-5 (household "not personal") admit household facts with
no subject required. Facts the guard exists to govern enter the prompt on a path the guard
never sees. Root cause traced at Index Demo 11; the mechanism is not in dispute and is not
what this amendment revises.

## THE ACCEPTANCE TEST (REWRITTEN)

Evidence is **telemetry, never prose**. `guard_triggered == true` in the turn record is the
only accepted proof of a structural refusal; a reply that merely reads like a refusal is a
FAIL.

**Test 1 — sensitive facts on the subjectless path MUST refuse structurally.** With no
subject resolved and at least one admitted fact at sensitivity `>= medium`, the turn must
show `guard_triggered == true`, `guard_kind ∈ {empty_set, attr_empty_set}`, and
`path == "guard_empty_set"`. B090 is the reference case (`address`, medium).

**Test 2 — non-sensitive household facts on the SAME path must NOT refuse.**
**DC-061 and DC-080 must still pass, unguarded** — `guard_triggered == false`,
`admitted_count` unchanged (1 and 2 respectively). This test is the one v20260804_0806
lacked, and it is what makes the fix falsifiable.

**Test 3 — turns that admit nothing must not refuse.** Every item with
`injected_fact_ids == []` has `guard_triggered == false`. (Carried forward; still rejects
dropping `has_personal_subject`.)

**Test 4 — no regression on turns that already refuse structurally.** B056, B068, B075,
B082 (all `resolved_subjects=['bill']`, `guard_kind=empty_set`) still show
`guard_triggered == true`.

**Test 5 — the full ORTH-1 contract holds.** `DISC:conformance` reports **39/39**, not
37/39. Any implementation that trades DC-061/DC-080 for B090 has not met this requirement.

**Test 6 — the full ratchet.** `eval.harness --full` reports RATCHET PASS, read from the
actual RATCHET FAIL / NEW FAILURES output. Note the standing pre-existing failure
`L7V2:MUTATION-NO-SILENT-DISAPPEARANCE`, which fails on pristine HEAD and must not be
counted as caused by this work.

All six must pass. Anything less is not done.

## THE VERIFICATION BLOCKER (precondition for any future acceptance run)

**Acceptance has never been runnable, and was not run at Index Demo 14.** Tests requiring
live turns — the B090 reference case and any probe-firing test — need a live dashboard on
the **cutover graph, Neo4j 7690**. At Index Demo 14 the only dashboard running was
**PID 92604, cwd `~/hip-vo`, bound to 7689 — the frozen demo**, which is explicitly out of
bounds ("Anything touching the frozen demo… it is the fallback; it is not a lane").

**No acceptance run may be reported as passed or failed until a dashboard is up on 7690.**
Any future dispatch attempting acceptance must first stand one up and record its PID and
port in the report. The battery (`--layer 7`, `--full`) needs no dashboard and remains
runnable; that is the only part of acceptance Index Demo 14 could execute, and it is what
produced the evidence in section 1.

## CONSTRAINTS

- **Do NOT amend ORTH-1.** Bill's ruling. DC-061 and DC-080 stay as written and must pass.
- **Do NOT accept the leak.** Bill's ruling. The address disclosure on B090 is not to be
  reclassified as acceptable.
- **Turns admitting no facts must not refuse** (carried forward).
- **The write path must not be guarded into silence** — `not is_declarative` is retained
  for the reason recorded at INJ-6 (D-15).
- **Do not remove `has_personal_subject` from INJ-6 or INJ-6b.** Both gates stay; any fix
  is additive.
- **The frozen demo (`~/hip-dev`, Neo4j 7689) is untouched.**
- **C9 is not ruled by this document.**

## OPEN

- **What sensitivity threshold, and ruled by whom.** `>= medium` separates the measured
  cases, but it is a proposal, not a ruling.
- **What a missing/null sensitivity means at the guard.** The registry says raise; the read
  layer says default to `medium`. These contradict, and a guard gated on sensitivity forces
  the question. Needs a ruling before build.
- **Whether the ORTH-1 fixtures gain a sensitivity field**, and whether adding one to a
  standing contract's cases is itself a contract change requiring its own ruling.
- **Whether household facts should be admitted on a subjectless turn at all** — named in
  v20260804_0806 and still out of scope, but the sensitivity axis makes it live again.

## NOT RULED

**Nothing in this document marks any requirement MET.** Status is PLAN. The fix was built,
measured, and reverted; nothing is committed to `harness/injection_contract.py`. C9 is not
ruled. TD-156 (*on demo-cutover-build*) is not closed. TD-149 (*on roadmap*) is not closed.
The two colliding TD-146 entries remain flagged, not reconciled.
