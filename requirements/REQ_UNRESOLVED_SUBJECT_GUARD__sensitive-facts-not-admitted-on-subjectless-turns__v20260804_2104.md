# REQ_UNRESOLVED_SUBJECT_GUARD
Status: PLAN
Reconciled-Against: roadmap `c6117c1` (2026-08-04); executed evidence at `d9eac55` on
`demo-cutover-build`

**SUPERSEDES `REQ_UNRESOLVED_SUBJECT_GUARD__empty-set-guard-fires-when-no-subject-resolves__v20260804_1333.md`**
(Index Demo 26, 2026-08-04, Bill's ruling: **PATH 1 — FIX ADMISSION, NOT REFUSAL**). That
version's fix was **built exactly as ruled at Index Demo 25 (D-D-149) and failed live
acceptance** — it passed every case it was specified against and then refused ordinary
knowledge turns. The prior version is retained unaltered as the record of what was believed
before it was executed.

**THE SLUG CHANGED, deliberately.** The prior slug —
`empty-set-guard-fires-when-no-subject-resolves` — now describes the wrong mechanism: the
guard firing is no longer the requirement, it is the backstop. A filename that misdescribes
its own requirement is how a reader ends up building the superseded thing. The SUBJECT
(`REQ_UNRESOLVED_SUBJECT_GUARD`) is unchanged, so the lineage and the `LATEST_` symlink still
resolve; only the descriptive half moved.

**Nothing here is MET.** Status is PLAN. Nothing is built by this document. C9 is not ruled.

## AMENDMENT RECORD (Index Demo 26, 2026-08-04)

### 1. THE EXECUTED EVIDENCE

Full record: `docs/dispatches/DISPATCH_UNRESOLVED_SUBJECT_GUARD_BUILD__inj6c-built-and-reverted-live-knowledge-turns-refuse__v20260804_2032.md`
(D-D-149, committed `d9eac55` on `demo-cutover-build`, with the 76-line patch preserved).

**The refusal-side fix was built correctly to both of the prior version's rulings** —
threshold `>= medium` as a named constant, missing sensitivity RAISING with no default
anywhere in the guard, ranked without short-circuit, `has_personal_subject` untouched on the
resolved-subject path — **and it passed everything it was specified against:**

| Specified against | Result |
|---|---|
| B090 refuses structurally | **PASS** — `guard_triggered=true`, `guard.kind="empty_set"` (nested, TD-D-147), `inference_ms=null`, `path="guard_empty_set"`, `resolved_subjects=[]`, no address anywhere in the record |
| DC-061 / DC-080 unguarded | **PASS** — `guard_triggered=False`, admitted 1 and 2, telemetry read from direct contract calls |
| `DISC:conformance` | **PASS — 39/39** |
| Standing battery | **PASS — zero delta**: 293 passed / 8 xfailed with the change, 293 / 8 pristine |
| Test 4 (turns that already refuse) | **PASS** — B056, B068, B075, B082 unchanged |

**And then ordinary knowledge turns refused:**

```
                        WITH the fix                            PRISTINE
capital of Brazil       guard=True  "I don't have that          guard=False  inference_ms=2488
                        confirmed yet."                         "The capital of Brazil is Brasília."
roast a chicken         guard=True  same empty-set template     guard=False  inference_ms=571
                                                                a real answer
```

The pristine set was fired after an actual **dashboard restart**, so the process genuinely
loaded pristine code; the delta is attributable to the change alone rather than assumed.

**THE CAUSE, established from the graph and not inferred.** Fact
`9073c508-54ce-4d68-84d3-623201891adc` — `attribute=household`, **`sensitivity=medium`**,
`owner=household`, `origin=self_report` — **is admitted into EVERY subjectless turn by
design.** Household-owned facts ride into every turn regardless of relevance (Set 1's own
header states this as the system's intended behaviour). So on the subjectless path
`result.allowed` *always* contains a `>= medium` fact, and any refusal-side guard reading
that set fires on everything.

**THE THRESHOLD IS NOT THE LEVER; ADMISSION IS.** `>= medium` was the correct
discriminator — it separates the address from the trash day exactly as the prior version
measured. It was applied at the wrong point in the pipeline. **This resolves the prior
version's OPEN item** — *"whether household facts should be admitted on a subjectless turn at
all… the sensitivity axis makes it live again"* — **with executed evidence rather than
analysis.** The answer is that they cannot be, not at `>= medium`.

### 2. THE REVISED REQUIREMENT

**Facts at sensitivity `>= medium` SHALL NOT be admitted into `result.allowed` on a
subjectless turn.** The gate moves from refusal to **injection**. Facts below `medium` admit
exactly as today.

**The refusal-side guard becomes the BACKSTOP, not the mechanism.** The preserved 76-line
INJ-6c patch is retained for this purpose: if a `>= medium` fact somehow reaches the prompt
on a subjectless turn, the empty-set guard fires. It is no longer expected to fire on any
natural path — its firing is a signal that the admission gate leaked.

> **Defense at the door, alarm inside.**

The two are not redundant. The admission gate is what makes the system behave correctly; the
backstop is what makes a failure of that gate visible instead of silent. A build that lands
only the backstop is the fix that already failed. A build that lands only the gate has no
detection if the gate is later bypassed by a new write path.

### 3. WHAT THIS PRESERVES

- **"What is the capital of Brazil?" answers** — because nothing sensitive is in the prompt to
  guard against. The turn is not refused; it is simply not carrying the address.
- **Trash pickup (`low`) still admits on subjectless turns**, so **DC-061 and DC-080 still
  pass unguarded** and the ORTH-1 contract is untouched. Bill's standing ruling — *do NOT
  amend ORTH-1* — is preserved without strain, because the low-sensitivity path is unchanged.
- **B090 does not leak the address** — because the address never arrives. It either answers
  honestly that it has no route basis, or the backstop fires. **Which one occurs is to be
  recorded, not assumed** (acceptance (b)).
- **Resolved-subject turns are unchanged.** Admission is gated by *subjectlessness*, not
  removed globally: the same `>= medium` fact must still be admitted when a subject actually
  resolves.

### 4. MISSING SENSITIVITY — the standing ruling is unchanged

**Missing sensitivity RAISES.** R29/R30: unknown values are quarantined or rejected, never
downgraded; `sensitivity.rank()` raises by design because *"a returned default is a downgrade
wearing a different name."* No default may be introduced at the admission gate, exactly as
none was introduced at the guard.

**`TD-D-148` (on `demo-cutover-build`) remains the filed deviation** and is not closed by this
amendment: `memory_engine/recall.py:249` and `memory_engine/api.py:241` both do
`row["sensitivity"] or "medium"`, upstream of the injection contract, so a null-sensitivity
fact arrives already wearing `medium`. It is to be fixed separately, on its own dispatch, with
its own decision about `PRE_REGISTRY` facts.

## THE DEFECT (carried forward, mechanism unchanged)

`harness/injection_contract.py` — `has_personal_subject = bool(resolved_subjects)`. INJ-6 and
INJ-6b are both gated on it, so when `resolved_subjects == []` neither runs, while INJ-1
(`owner == "household"`, unconditional), INJ-2 and INJ-5 admit household facts with no subject
required. Facts the contract exists to govern enter the prompt on the one path no gate
watches. Root cause traced at Index Demo 11; not in dispute and not revised here. **What this
amendment changes is where the correction is applied, not what is wrong.**

## THE ACCEPTANCE TEST (REWRITTEN FOR THE INJECTION GATE)

**Telemetry only, never prose.** A reply that reads correctly proves nothing; the turn record
is the evidence. All six must pass.

**(a) A subjectless knowledge turn ("capital of Brazil" class).**
`injected_fact_ids` contains **NO** fact with `sensitivity >= medium`; `guard_triggered=false`;
and the answer is **substantive — not the empty-set template**. All three, together: a turn
that answers while still carrying the address fails (a), and so does a turn that carries
nothing but refuses.

**(b) A subjectless turn that would previously have carried the address (the B090 query).**
The `>= medium` fact is **ABSENT from `injected_fact_ids`**. The turn then either gives an
honest no-basis answer **or** the backstop guard fires — **record which.** Both are
acceptable outcomes; not recording which one occurred is not.

**(c) A properly resolved-subject turn.** The same `>= medium` fact is **PRESENT in
`injected_fact_ids`** and the turn behaves as it does today. **Admission is gated by
subjectlessness, not removed globally** — a build that drops the fact everywhere passes (a)
and (b) and fails here, which is what makes (c) load-bearing.

**(d) DC-061 and DC-080 unguarded; `DISC:conformance` 39/39.** Low-sensitivity facts still
admit on subjectless turns. ORTH-1 is not amended.

**(e) THE BACKSTOP, fault-twin style.** With the preserved patch applied, a `>= medium` fact
**forced** into `result.allowed` on a subjectless turn fires the empty-set guard:
`guard_triggered=true`, `guard.kind=empty_set`, `inference_ms=null`. **A forced condition, not
a natural path** — if this can be produced without forcing, the admission gate has a hole and
(a) is not really passing.

**(f) Standing battery zero delta** against the **293 passed / 0 failed / 8 xfailed** pristine
baseline **this checkout actually produces**. (The previously-circulated `292/1/8` does not
reproduce and is not the baseline — D-D-149 established this by running the battery both
ways.)

**PRECONDITION DISCHARGED.** The prior version's VERIFICATION BLOCKER — no acceptance may be
reported until a dashboard is up on the cutover graph 7690 with its PID and port recorded — is
**satisfied**: `scripts/cutover_demo_start.sh 7872`, **PID 22932**, Neo4j
`bolt://localhost:7690`, registry `~/hip-cutover-demo-home/registry.db` (3 members), 5/5
preflight PASS, recorded in D-D-149. The blocker is not carried forward.

**Known gap, not a blocker for (a)-(e):** `eval.harness --full` could not run in the
`~/hip-cutover-demo` checkout — no `.env.dev`, no in-checkout registry — so the full ratchet
is UNRUN there. (f) is the pytest standing battery, which does run. Provisioning that checkout
is separate work.

## CONSTRAINTS

- **Do NOT amend ORTH-1.** Bill's standing ruling. DC-061 and DC-080 stay as written.
- **Do NOT accept the leak.** Bill's standing ruling.
- **Ordinary general-knowledge turns must ANSWER**, not refuse. This is now an explicit,
  executed-evidence constraint rather than an anticipated one — it is the exact clause the
  previous version failed.
- **Admission is gated by subjectlessness only.** Resolved-subject behaviour must not change.
- **Missing sensitivity raises.** No default at the gate.
- **The backstop is retained, not replaced.** Landing the gate without it removes the only
  detection for a future leak.
- **Do not remove `has_personal_subject` from INJ-6 or INJ-6b.**
- **The frozen demo (`~/hip-dev`, Neo4j 7689) is untouched.**
- **C9 is not ruled by this document.**

## OPEN

- **THE DATA QUESTION (Index Demo 26, its own item).** The live graph carries `household` at
  **`medium`** while the seed (`D7`, "trash pickup is Wednesday") and the ORTH-1 fixtures say
  **`low`**. The most likely explanation is that `TD-D-148`'s silent default has already
  stamped a stored fact — the fact in question is `origin=self_report`, i.e. written by a live
  turn rather than seeded. **Whether to correct that stored value is a DATA-MIGRATION
  decision, separate from this REQ and not decided here.** It matters to acceptance either
  way: (a) and (b) are measured against whatever the graph actually holds, so a migration
  between now and the build would change which facts are `>= medium` without changing a line
  of this document.
- **Which outcome B090 produces** under the gate — honest no-basis answer, or backstop —
  is to be recorded by the build, not predicted here.
- **Whether the ORTH-1 fixtures should gain a sensitivity field** at all, given the gate now
  reads sensitivity at injection. D-D-149 added one to 36 of 38 rows and reverted it with the
  rest of the failed attempt; the assignment table is preserved in that dispatch doc.
- **`allergy` has no assignable sensitivity** — no live rows, absent from the seed, no
  declared attribute family, no write-path default. Two fixture rows were deliberately left
  unassigned rather than guessed.
- **Attribute-level sensitivity cannot see a secret inside a value** — see `TD-R-162`, filed
  from this dispatch. Not in scope here.

## NOT RULED

Nothing in this document marks any requirement MET. Nothing is built. The fix described in the
prior version was built, measured, and reverted; `harness/injection_contract.py` is
byte-identical across `roadmap` and `demo-cutover-build` at
`aa1c1c54bbb3f577f4e7cdc358c4b77318c82f87dc8c999b1368e9da8c6c2cb2`. C9 is not ruled.
`TD-D-148` is not closed. `TD-R-162` is filed, not fixed.
