# DISPATCH_R4_R8_ORIGIN_ASSIGNMENT
Status: BUILT (REQ amendment landed; Part B code NOT landed — STOPPED per item 4, own instruction)
Reconciled-Against: see HASH

**TYPE:** BUILD (REQ amendment only — item 1's own instruction, unconditional) + ANALYSIS
(survey and a measured, executed blast-radius probe; the probed code change itself was
reverted, not shipped)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R4 and R8 (amended this dispatch, item 1).

## THE ASK

Dispatch text, verbatim:

```
=== D-157 | ~/hip-roadmap, roadmap | R4/R8: assign by origin, refuse what origin
    cannot reach ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R4 and R8. These are ONE decision, not two —
D-154 established that COGNITIVE_OBSERVATION and FUNCTIONAL_SUPPORT_STATE are exactly
R4's permitted layers 1-2 and are the two classes R8 cannot assign without reading
content.

BILL'S RULING, the requirement text:
"Where a class can be determined from the write path a fact arrived through, assign it
that way. Never read the value. A fact HIP cannot honestly classify shall not quietly
inherit a neighbouring class — it refuses, or carries an explicit unknown."

Recorded with the ruling and NOT to be paraphrased away: Bill is unsettled on whether
origin alone is sufficient, because both origin and content genuinely bear on these
two classes. Origin-based assignment is adopted FOR NOW, with content-based assignment
to be revisited deliberately later. Write that into the REQ amendment as a staged
decision, not a closed one.

1. WRITE THE REQ AMENDMENT FIRST, from Bill's words above. Item 8 applies.
2. SURVEY, report before building: which write paths exist, and which of the four
   absent classes each could honestly determine. The risk_pattern precedent
   (REQ_D21_D23) is the model — a per-category per-write-path restriction.
   STOP AND REPORT if a path's meaning is ambiguous. Note that origin=="attributed_
   import" ALREADY MEANS the frontier model's own answer written back (disclosure.py:
   269), NOT a clinician import — do not reuse it.
3. THEN BUILD. Part A: origin-based assignment where honest. Part B: what origin
   cannot reach REFUSES or carries an explicit unknown — it must not inherit a
   neighbouring class. Absorption is the defect being fixed; do not trade it for a
   different silent default.
4. REPORT THE BLAST RADIUS BEFORE COMMITTING: part B may block writes that succeed
   today. Name which, with evidence from a run, not from reading. If it breaks the
   demo seed or any standing fixture, STOP AND REPORT rather than carving an exception.
5. Acceptance per D-87: executed fault twin proving a fact that cannot be classified
   is refused rather than absorbed, plus anti-vacuity. Report whether A8 becomes
   writable. Do not re-tier.
6. Runs: --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17; 16/17 is a STOP.
7. Rule nothing MET.
```

## WHAT WAS DONE

1. Gate checked — matched. Repo lock acquired via `scripts/hip_lock.py with repo`, pulled
   clean to `01167a9` (another lane's own CLAUDE.md fix — item 4 now correctly describes
   `hip_lock.py` instead of the retired `.hip-lock` marker — noted, not touched).
2. **Searched for D-154's own dispatch doc — found none anywhere in the tree** (`grep -rl
   "D-154" docs/` returns only unrelated TD-154 hits inside debt-register text). D-154's
   CLAIM was not taken on faith: checked it directly against R4's own primary text instead
   (`FUNCTIONAL_SUPPORT_STATE` is R4 layer 2's literal name; `COGNITIVE_OBSERVATION`
   matches layer 1's "event observation" shape) and against `harness/representation_
   class.py`'s own module docstring, which independently states the identical finding —
   the claim checks out from primary sources even though D-154's own record is missing.
   **Flagged as a finding (OPEN), not treated as a blocker** — Requirements Discipline
   item 11 asks to check whether an analysis has already been traced; here it apparently
   was (by whoever/whatever produced "D-154"), but left no traceable doc.
3. Read R4 (`:282-308`) and R8 (`:368-393`) in full, plus R9/R10 (`:395-427`, R10's own
   text already names an "approved support-state permit" for `FUNCTIONAL_SUPPORT_STATE`
   and an origin path for `EXTERNAL_PROFESSIONAL_DIAGNOSIS` — neither built).
4. **Wrote the REQ amendment first** (item 1), verbatim from Bill's ruling text, at both
   R4 (a one-line pointer, "this is one decision, not two") and R8 (the full amendment,
   dated, explicitly staged not closed).
5. Read `harness/write_origins.py` in full — the risk_pattern/`REQ_D21_D23` precedent
   named as the model: a per-ATTRIBUTE per-ORIGIN restriction (`DERIVABLE_ATTRIBUTES`),
   enforced at the creator, with widening requiring a ruling. Confirmed the exact shape
   to replicate if an honest origin-based assignment existed.
6. Read `harness/representation_class.py` in full, including its own module docstring —
   **D-140's OWN survey (2026-08-03) had already answered most of item 2's question**:
   `COGNITIVE_OBSERVATION` and `FUNCTIONAL_SUPPORT_STATE` "share attribute space with
   health_condition/incident" and "care_plan" respectively — telling them apart from an
   ordinary health fact needs the VALUE, which D-50 Principle 6 forbids reading. D-157's
   own genuinely NEW question is whether ORIGIN (a third axis D-140 didn't examine) closes
   that gap where attribute and content both cannot.
7. Surveyed all six origins (`extraction`, `self_report`, `attributed_import`,
   `derivation`, `migration`, `fixture`) against both classes — see WHAT WAS FOUND. No
   path's MEANING was ambiguous (each is clearly documented in `write_origins.py`); item
   2's specific STOP condition did not fire. What was found instead: origin does not add a
   positive signal for either class on any currently-live production path.
8. Confirmed live, via `grep`, that `self_report` (`harness/fact_change.py:809`) and
   `extraction` (`harness/extraction_queue.py:1032`) are real, currently-active origins for
   `health_condition`/`incident`/`care_plan` facts — the paths any Part B would have to
   refuse against.
9. Checked `scripts/demo_seed.py`'s actual 11 fixture facts directly (not assumed): none
   use `attribute="health_condition"` or `"care_plan"`; one (`D4`) uses `"incident"`, with
   `origin="fixture"` — a path this dispatch's own analysis (item 2) found CAN honestly
   claim any class by construction (matching D8's existing `_ENUM_EXEMPT_LABELS`
   precedent), so this alone would not break the demo seed.
10. Checked `eval/memory_harness.py`, `eval/truth_harness.py` (the two other files using
    `attribute="health_condition"` outside the classifier's own test file) — both use
    `origin="fixture"` at their call sites, same as above.
11. **Checked `eval/sia_golden_set.json` and `eval/fact_schema_conformance.json`** — both
    use `health_condition` extensively as a REAL, expected extraction-path attribute (not
    fixture-origin test scaffolding) — the actual, everyday health-fact vocabulary, not an
    edge case.
12. **Built Part A/B as a real, uncommitted, EXECUTED probe** (D-87 discipline — evidence
    from a run, per item 4's own instruction, not from reading): `classify_representation`
    temporarily modified so that `attribute in {"health_condition", "incident",
    "care_plan"}` with `origin != "fixture"` returns `UNKNOWN_HIGH_RISK` (refuse) instead
    of the current `HEALTH_CLAIM` absorption.
13. Ran `eval/test_ceiling_representation_class.py` + `eval/test_ceiling_representation.py`
    (72 cases, the classifier's own standing battery) against the modified code:
    **3 failed** — `test_ceil_a8_attribute_maps_to_the_ruled_class[health_condition-
    HEALTH_CLAIM]`, `[incident-HEALTH_CLAIM]`, `[care_plan-HEALTH_CLAIM]` — exactly the
    three attributes the probe touched, under `origin="self_report"`, real evidence not a
    prediction.
14. **STOPPED per item 4's own explicit instruction** rather than carving an exception.
    Reverted the probe (`git diff --stat harness/representation_class.py` confirmed empty
    before re-running; 72/72 pass again, byte-identical to before the probe).
15. Wrote this dispatch doc.
16. Staged by explicit pathspec (the REQ amendment, this doc — `harness/representation_
    class.py` NOT staged, since it is unchanged), committed, pushed, verified post-commit,
    released the lock.

## WHAT WAS FOUND

### D-154 could not be located as a dispatch record (item 2 area, a finding not a STOP)

No file anywhere in `docs/` names or discusses "D-154." Its claim was independently
re-derived from R4's own primary text instead of trusted — and it checks out (R4 layer 2
is named `FUNCTIONAL_SUPPORT_STATE` verbatim; `harness/representation_class.py`'s own
module docstring, written at D-140 on 2026-08-03, already states the identical finding
about both classes). This dispatch proceeds on the CONFIRMED substance, not on trust in
an unlocatable citation — see OPEN.

### The survey (item 2) — origin adds nothing for either class, on any live path

| origin | could honestly assign `COGNITIVE_OBSERVATION`/`FUNCTIONAL_SUPPORT_STATE`? |
|---|---|
| `extraction` | No. Attribute name (`health_condition`/`incident`/`care_plan`) is shared with ordinary health facts; the origin itself carries no signal about WHICH subtype an extracted utterance was. |
| `self_report` | No, same reason — a live conversational statement under this origin could be either an ordinary health fact or a cognitive-observation/support-state-shaped one; the path name doesn't distinguish them. |
| `attributed_import` | Explicitly excluded per the dispatch's own warning — today's one caller is the frontier model's own answer written back (`harness/disclosure.py:269`), not any kind of clinician or external-observation import. Not reused. |
| `derivation` | Not today. R4's own example ("asked for the appointment time three times in twenty minutes") is shaped like a genuinely derivable, system-computed pattern — analogous to `risk_pattern` — but no such derivable attribute exists yet (`DERIVABLE_ATTRIBUTES` is exactly `{risk_pattern, lifestyle}`, neither maps to either class). Widening it is a ruling per `write_origins.py`'s own stated discipline, not attempted here — out of this dispatch's scope, which is the CLASSIFIER, not a new inference mechanism. |
| `migration` | Reserved, unused (confirmed D-96) — not applicable. |
| `fixture` | YES, honestly — a fixture constructs a KNOWN state by definition (the same reasoning that already exempts D8's `risk_pattern` label). No real fixture currently needs to claim either class, so this is a real but presently unused honest path. |

**Part A's conclusion: for the classes this dispatch is scoped to, no ORIGIN provides a
positive assignment signal beyond what D-140 already found attribute/content cannot.**
This is the concrete shape of Bill's own stated uncertainty ("origin alone" may not be
sufficient) — confirmed, not merely anticipated.

### The blast-radius probe (item 4) — executed, not read

A literal Part B (refuse `health_condition`/`incident`/`care_plan` on any non-fixture
origin, since none can rule out the ambiguity) was built and RUN, not just reasoned about.
Result: **3 of 72 standing-battery cases fail immediately** — precisely the three
attributes, under `self_report`, the primary live conversational-write origin. These are
not edge cases: `health_condition` is CANONICAL_ATTRIBUTES' general-purpose health-fact
slot, used throughout `eval/sia_golden_set.json` (the extraction golden set) and
`eval/fact_schema_conformance.json` (ORTH-2's own schema-conformance corpus) as ordinary,
expected, everyday extraction output — "diagnosed with hypertension," and similar. A
literal Part B would refuse the entire ordinary self-reported/extracted health-fact
pipeline for these three attributes, not merely a narrow cognitive-observation/
support-state subset — because origin cannot narrow the refusal to that subset; it can
only refuse ALL of `health_condition`/`incident`/`care_plan`, or none.

**The demo seed itself is not broken** (none of its 11 fixture facts use `health_
condition`/`care_plan`, and its one `incident` fact is `fixture`-origin, exempt) — but
`eval/test_ceiling_representation_class.py`'s own standing, pinned expectations ARE, and
they stand for the real production pipeline, not test scaffolding. Per item 4's own
instruction ("If it breaks... any standing fixture, STOP AND REPORT rather than carving
an exception") — this is read as reaching that bar: a standing battery's pinned,
evidence-based expectations broke, for the core real-world attribute, under the primary
production origin. **STOPPED here. Part B not built for real, not committed.**

### Why "carving an exception" was not attempted

The only way to keep Part B narrow enough not to break real health-fact writing would be
to exempt `health_condition`/`incident`/`care_plan` from the refusal specifically for
`self_report`/`extraction` — which is exactly the current, unmodified behavior. There is
no honest MIDDLE GROUND between "refuse everything under these attributes" (breaks real
writes) and "refuse nothing" (today's silent absorption, the defect R8 was ruled NOT MET
over) using ORIGIN ALONE — confirming, with executed evidence, Bill's own stated
uncertainty rather than resolving it. That is a finding to report, not a gap to paper
over with a carve-out the dispatch explicitly forbade.

## VERIFIED

**Watched, executed:**
- `grep -rl "D-154" docs/` — returned only unrelated TD-154 hits, confirmed by reading
  each match.
- `harness/fact_change.py:809` and `harness/extraction_queue.py:1032` — both origin
  literals read directly, not recalled.
- `scripts/demo_seed.py`'s 11 `FIXTURES` entries read in full — none use `health_
  condition`/`care_plan`; `D4` uses `incident`/`fixture`.
- `eval/memory_harness.py:1133`, `eval/truth_harness.py:558,612` — both `health_condition`
  call sites read directly, confirmed `origin="fixture"`.
- The Part A/B probe: `classify_representation` modified, `eval/test_ceiling_
  representation_class.py` + `eval/test_ceiling_representation.py` run twice — once with
  the probe (72 run, 3 failed, exact names captured above) and once after reverting (72
  passed) — the revert verified via an EMPTY `git diff --stat` before the second run, not
  assumed clean.

**Reasoned about, not independently re-derived:** that `derivation` COULD honestly support
`COGNITIVE_OBSERVATION` for a FUTURE pattern-based attribute is inference from R4's own
"asked three times in twenty minutes" example matching the shape of a derivable metric,
cross-checked against `risk_pattern`'s existing precedent — not built or tested, since
inventing a new derivable attribute is explicitly out of this dispatch's scope (a
different ruling, per `write_origins.py`'s own stated discipline).

## HASH

Staged for commit: `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit
__v20260802_2205.md` (R4/R8 amendment, item 1), this dispatch doc. `harness/representation_
class.py` NOT staged — the probe was reverted, the file is unchanged from HEAD.

## OPEN

- **D-154's own dispatch doc could not be located.** Either it exists uncommitted/
  unpushed somewhere this checkout cannot see, or the citation itself is imprecise. Not
  investigated further — this dispatch's own re-derivation from primary sources confirms
  the SUBSTANCE independently, so the missing citation does not block anything here, but
  it is a real gap worth someone tracing.
- **Items 5-7 (acceptance/A8-writability report, `--layer 7`/RATCHET/memory-harness runs,
  ruling) are NOT performed.** There is no code change to accept — Part B was reverted.
  A8 does NOT become writable by this dispatch; nothing changed about it.
- **The real open question is exactly the one Bill named as unsettled, now with executed
  evidence behind it**: origin alone cannot honestly assign `COGNITIVE_OBSERVATION`/
  `FUNCTIONAL_SUPPORT_STATE` on any live production path, and a content-blind refusal
  would cost the entire ordinary health-fact pipeline for three core attributes. Content-
  based assignment (deliberately deferred by the REQ amendment itself) is the only
  remaining lever this survey found — not attempted here, per instruction.
- **The `derivation`-origin possibility for `COGNITIVE_OBSERVATION`** (a new, pattern-based
  derivable attribute, analogous to `risk_pattern`) is named as a plausible future
  direction, not scoped or built — widening `DERIVABLE_ATTRIBUTES` is its own ruling.
- **`FUNCTIONAL_SUPPORT_STATE`'s "approved support-state permit"** (R10's own named, unbuilt
  mechanism) is a second, structurally different possible future direction — a NEW,
  permit-gated origin path rather than a repurposing of an existing one — also not scoped
  here.
- **Nothing ruled MET.**

## RECAP
D-157: REQ amendment landed (R4/R8, staged not closed, Bill's exact words) — origin-based
assignment adopted for now, content revisit deferred. Survey found origin adds NO positive
signal for `COGNITIVE_OBSERVATION`/`FUNCTIONAL_SUPPORT_STATE` on any live write path,
confirming D-140's own attribute/content finding extends to origin too. Built and RAN the
Part B refusal as a real probe (not just reasoned about): broke 3/72 of the classifier's
own standing battery, exactly the core `health_condition`/`incident`/`care_plan`
attributes under the primary `self_report` origin — the everyday health-fact pipeline, not
an edge case. STOPPED per the dispatch's own item 4, reverted the probe rather than carve
an exception. A8 not re-tiered, nothing ruled.
