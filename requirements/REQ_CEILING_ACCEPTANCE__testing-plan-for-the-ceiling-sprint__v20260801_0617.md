# REQ_CEILING_ACCEPTANCE — testing plan for the ceiling sprint

**Status:** FILED — plan proposed, NOT self-ruled; no tier assignment here is a ruling
**Version:** v20260801_0617 (Mountain Time, per the CLAUDE.md Naming Law)
**Decision-Owner:** Bill
**Filed:** 2026-08-01 (D-77)
**Reconciled-Against:** roadmap `112841a`. Every row below was re-verified against that HEAD, not inherited from the D-70 survey — the tree moved when D-75 landed R29.
**Authority:** `REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2129.md` (verified LATEST via `docs/INDEX.md` and the `LATEST_REQ_STRUCTURAL_CEILING.md` symlink; R29 ruled **MET** and R30 ruled **NOT MET** 2026-08-01, recorded in its §16 at lines 1036 and 1048). `REQ_HARNESS_DISCIPLINE` applies in full.
**Inputs:** `docs/reviews/D63_dimensioned-ceiling-axes__fable-and-chatgpt__v20260731_1917.md`; `docs/reviews/FABLE_D61_critique__progressive-authorization__v20260731_1831.md`; `docs/reviews/FABLE_D70_call-site-survey__structural-ceiling-30-requirements__v20260801_0617.md` (banked under this dispatch — it had been left in `/tmp`); TD-137 (RESOLVED, `d50225e`) and TD-138 (OPEN) in `docs/techdebt/LATEST_DEBT.md`.

---

## 1. WHY THIS REQ EXISTS

`REQ_STRUCTURAL_CEILING` declares 30 requirements and 30 acceptance rows. Twenty-eight of them have no ruling and most have no implementing call site. The risk this document exists to prevent is not that those tests fail — it is that **they are never written, and their absence is mistaken for their passing.**

This project has that failure twice on the record, and both are cited here because they are the pattern, not anecdotes:

- **D-36:** the 23-case learner-isolation adversarial battery — the suite encoding six confirmed security holes — was **referenced by no runner at all**. It existed as code, was never executed, and every expectation in it could have regressed to green-by-deletion without a single run turning red. Confirmed by reproduction.
- **The care-team acceptance (`REQ_CARE_TEAM_READ_AUTH`, D-68):** five prose acceptance rows, **no executable form**, no runner reference, and fixtures that do not exist. The widening they describe is live in production code under a REQ that was never ruled MET. D-69 then found (TD-138) that the same code path is epoch-blind, and that acceptance **row 4 tests only the removal direction — so a fully-run, fully-passing acceptance would have missed the defect entirely.**

The second case is the sharper lesson: a written, plausible, complete-looking acceptance can still be structurally incapable of detecting the defect it exists to catch. Hence the governing rule below.

### THE GOVERNING RULE

> **A check that cannot be shown RED on command is not load-bearing.** Every row in this plan — whatever its tier — carries a named fault twin. A row without one is not "passing"; it is unmeasured.

---

## 2. THE THREE TIERS

**LIVE** — runnable today, wired into `scripts/run_harness.sh`, gating. A failing LIVE row aborts the run non-zero.

**STRICT XFAIL** — wired into the runner with `pytest.mark.xfail(strict=True)`, expected to fail. **The suite goes RED if one unexpectedly passes.** That is the point: an XPASS means either the requirement quietly built or the test stopped testing, and both must interrupt. This is the house pattern already in use at `eval/test_learner_isolation_adversarial.py:347` and described at `eval/test_outcome_classifier_correction.py:15` (the D-27 xfail(strict=True) → XPASS(strict) → real-PASS progression). **A row flips from XFAIL to LIVE only when its requirement builds, and only by explicit dispatch** — never as a side effect of a passing run.

**CONTRADICTED-XFAIL** — a distinct sub-tier, defined in §4. Fails against **deliberate, ratified current behavior**, not against an unbuilt feature.

**UNWRITABLE** — the fixture does not exist. **These tests are NOT written.** Writing a test whose fixture must be invented produces a check that passes against a fiction, which is worse than an absent check because it reports coverage. Each row names its fixture, cost, and required write authorization.

### Tier counts

| Tier | Count | Rows |
|---|---|---|
| LIVE | 12 | A7, A11, A27, A29, A30, A1, A18, A2, A8, A16, A17, A10 — **A1/A18 re-tiered SEE §7.3/§7.6; A2/A8 re-tiered UNWRITABLE→LIVE at D-145, SEE §7.7; A16/A17 re-tiered CONTRADICTED-XFAIL/UNWRITABLE→LIVE at D-R-179 (Bill's ruling, 2026-08-05; R16 MET, R17 MET), SEE §7.8; A10 re-tiered STRICT XFAIL→LIVE at D-R-183 (Bill's ruling, 2026-08-05; R2/R8/R10 all MET), SEE §7.9. Count corrected 7→9 at D-148 (enumeration vs stale count), then 9→11 at D-R-179, then 11→12 at D-R-183.** |
| STRICT XFAIL | 4 | A19, A20, A21, A26 — A10 departed this tier at D-R-183 (RE-TIERED LIVE, SEE §7.9); deliberately not enumerated here, matching the UNWRITABLE row's own D-148 convention below. |
| CONTRADICTED-XFAIL | 1 | **A12 (SEE §4 — RE-TIERED LIVE, D-103)** — A16 departed this tier at D-R-179 (RE-TIERED LIVE, SEE §7.8 and §4); deliberately not enumerated here, matching the UNWRITABLE row's own D-148 convention below. |
| UNWRITABLE | 13 | A3–A6, A9, A13–A15, A22–A25, A28 — **three rows have now been REMOVED from this tier (two at D-145, one — A17 — at D-R-179; all reasons closed, all now LIVE, §7.7/§7.8). Their ids are deliberately NOT enumerated here: this cell lists the rows IN this tier, and naming departed rows made a status board read them back as UNWRITABLE (D-148).** |

**This is a plan, not a ruling.** The counts as filed said 12 of 30 rows could be wired then — 5 gating, 7 as strict-xfail tripwires — and that 16 could not be written honestly at the time; 30/30 rows are now tiered (12 LIVE, 4 STRICT XFAIL, 1 CONTRADICTED-XFAIL, 13 UNWRITABLE), the movement recorded in each cell above rather than by editing this now-historical sentence.

---

## 3. HARNESS DISCIPLINE — the four requirements

Per `REQ_HARNESS_DISCIPLINE`, every check in this plan declares all four. Rows in the UNWRITABLE tier declare what each **would** be, so the gap is scoped rather than vague.

1. **Fault twin** — the specific mutation that turns the check red.
2. **Ground-truth fixture** — hand-authored, never model-graded.
3. **Coverage entry** — roles, scopes, and NAMED UNCOVERED, registered in `check_registry`.
4. **Metamorphic wrapper** — the invariant that must survive a meaning-preserving rewording.

**A standing caution, from this session's own error.** The A29 static guard in `eval/test_sensitivity_registry.py` was first written as a source regex and **fired on its own explanatory comment** about the old encoding. It was rewritten to walk the AST. A guard that fails on its own documentation gets disabled, and the file exists precisely because TD-137 survived for want of a cross-module check. Structural checks in this plan **must** use AST or import-graph inspection, never a source regex. The same weakness was found in CS1's prompt-touch scan (D-46 §F8: two files, two inconsistent regexes, a span delimited by a movable comment) and must not be reproduced.

---

## 4. CONTRADICTED-XFAIL — the sub-tier, and why it is separate

An xfail that fails against an **unbuilt feature** says "not yet." An xfail that fails against a **ratified design decision** says something entirely different: the requirement and the shipped architecture disagree, and someone must choose. Filing both under one tier would let a genuine architectural conflict masquerade as ordinary backlog.

### A12 — author readback (R12) — **RE-TIERED LIVE (D-103, 2026-08-02). R12 MET.**

**CONTRADICTED-XFAIL -> LIVE**, and the check written in the SAME edit — splitting them reds
the suite (a CONTRADICTED row whose check passes is an XPASS; a LIVE row with no check asserts
nothing). `eval/test_ceiling_audience_a12.py`, 14 cases, in `scripts/run_harness.sh`, passing
on first run — so the ruling rested on a correct premise and the D-103 stop condition did not
fire. Read-path fix landed D-102 (`f074f6a`); full evidence in REQ_STRUCTURAL_CEILING §16, R12.

**Why this row had no check until now, and it is not an oversight:** CONTRADICTED-XFAIL meant
it failed against a RATIFIED design rather than an unbuilt feature, so the sub-tier said it
needed a RULING, not a test. That was correct. The ruling came at D-92, the fix at D-102, the
check and the tier at D-103.

**The named limit survives MET:** the DEK wrap entrenches the author's own ciphertext, so R12
caps what else they receive and never their own sentence. The self-exempt case is asserted
twice for exactly that reason.

The original CONTRADICTED analysis, retained:


**Bill's ruling: R12 stands as written; the INJ-3 owner permit gets bounded on both clauses below.**
The alternative — narrowing R12 to describe current behavior, which would have made this row pass
immediately and cost nothing — was **REJECTED**, because it would quietly give up the claim *"the
author can read back what they said; they cannot build a file on you."* Bulk readback SHALL be
capped (aggregation), and HIP's own inferences SHALL stop counting as the author's property merely
because they were derived from the author's input (derivatives).

**A12 STAYS CONTRADICTED until the read path changes** — the ruling names the fix, it does not
perform it. This is a **live read-path change with its own scheduled dispatch**; D-92 recorded the
ruling and deliberately started nothing. Full statement in `REQ_STRUCTURAL_CEILING` section 16, R12.

The original analysis, unchanged:


**Fails against:** INJ-3's owner permit, `harness/injection_contract.py:19` — *"fact.owner == requester (owner reads what they stored)"*. Verified still present at `112841a`.

**Precisely what diverges** (this is narrower than the D-70 survey stated, and D-71 corrected it in the REQ itself): the owner permit is **consistent** with the readback R12 preserves. It diverges on two clauses only — **aggregation** (the permit is per-fact and unbounded, so reading back every fact one ever stored about a subject reconstructs the forbidden cross-report file) and **derivatives** (`consolidate.py` gives a derived fact *"the same owner and subject as the sources"*, so a fact derived from the author's own statements is **owned by the author** and the same permit reaches it).

**What flips it:** a ruling to bound the owner permit, **or** a change to derived-fact ownership. Both are code changes to a live read path. Note R12's own NAMED LIMIT (§6.5): the author's retention of their own ciphertext is **entrenched by the DEK wrap** — removing it is a re-encryption, not a policy edit — so A12 can never assert the author loses their own sentence.

**UPDATE (D-101/D-102, 2026-08-02): the read path has changed — both clauses, not just one.**
`_inj3_cross_member_deny`'s owner-permit no longer reaches a `derived` fact (DERIVATIVES), and
`apply_injection_contract` now caps owner-permit-only admissions to `owner_permit_cap` (default 8,
keyed to `voice_max_facts`) per OTHER subject (AGGREGATION) — self-facts, household, and care-team
facts exempt. **Verified by direct execution, not just read** — this dispatch is not asserting this
from the diff alone:

```
AGGREGATION (medication attr): allowed=8 denied=2 reasons=['deny_aggregation_cap', 'deny_aggregation_cap']
SELF-EXEMPT: 10 self-facts -> allowed=10 denied_aggregation_cap=0
DERIVATIVES: 1 derived fact about elena, owner=bill -> allowed=0 denied=1 reasons=['deny_default_cross_member']
DERIVATIVES self-subject: 1 derived fact about bill, owner=bill -> allowed=1
```

**A12 STAYS CONTRADICTED — this is a report, not a re-tiering.** No `test_ceil_a12_*` fixture
exists (A12 was, per this section's own instruction, never wired — "they need rulings, not
fixtures"), so there is no fault-twin-proven acceptance row, only the direct-execution check
above. Re-tiering — and writing A12's actual acceptance fixture, since none exists yet to
correct — is Bill's call, same as A1's and A18's were, and per instruction needs the tier flip
and any fixture in one edit, not done here.

### A16 — ledger contents (R16) — **RE-TIERED LIVE (D-R-179, 2026-08-05). R16 MET.**

**CONTRADICTED-XFAIL -> LIVE.** The fixture was already written and executed at D-R-173
(`ad90444`, same day) — `eval/test_ceiling_retention.py`, CEIL-A16 section, 4 cases — so this
re-tiering records a ruling landing on an already-proven row, not a tier moving ahead of its
check. See §7.8 for the full evidence and §16 of `REQ_STRUCTURAL_CEILING` for Bill's ruling
text and its permanent limit (every pre-cutover v1 event stays forbidden-field-bearing
forever).

**Flipped only when D-71's both-mechanisms ledger built, and flipped together with A17** —
exactly as this section originally said it must. Restated here because a reader arriving at
A12's ruling once asked whether A16 moved too; at the time (D-92/D-103) it had not. It has
now, together with A17, at D-R-179.

The original CONTRADICTED analysis, retained as history:


**Fails against:** the ratified crypto-shredding design. `harness/epistemic_ledger.py:13` — *"Payload encryption + crypto-shredding (OQ-2 §3 — the PRIMARY erasure path)"*. The ledger deliberately carries AES-256-GCM member-actor payloads; erasure is by key destruction, not absence.

**Not a defect.** Its driver is statutory: `docs/specs/EPISTEMIC_LEDGER__hel-oq2-backup-replica__v20260714_1615.md` §3.1 — *"Backup without a destruction mechanism creates operator liability: 47 USC 551 and the GDPR right-to-erasure reach every copy, including replicas."*

**What flips it:** the R16 ruling of D-71 (**both** mechanisms — opaque keyed commitments in the chain **and** payloads off-ledger under per-member keys) being **built**. The REQ already names that cost: a ledger rebuild plus a new off-ledger store, with **R17 promoted to load-bearing** — if active artifacts are not separately erasable, splitting payloads out of the chain buys nothing.

**Sequencing note:** A16 and A17 must flip together. Flipping A16 alone would certify commitments-only while the personal data persists elsewhere unerasable.

---

## 5. ROW-BY-ROW

Each entry: **tier · runner entry · fixture · fault twin**. Rows touching the MET Curator scorer state their L7:CS1 interaction, per D-75's precedent.

### LIVE (5)

**A7 (R7) — transient reasoning creates no durable authority.**
Runner: `eval/test_ceiling_representation.py::test_a7_*`. Fixture: AST walk over `harness/`, `memory_engine/`, `server/` asserting no write path persists model reasoning traces; verified at HEAD that no `chain_of_thought` / `reasoning_trace` / `scratchpad` persistence exists. Twin: a synthetic module that writes a reasoning trace to a durable store must be flagged. Metamorphic: renaming the field or aliasing the import must not evade — hence AST, not regex.
*Vacuously true today.* Recorded as such: it holds by **absence**, not by control. Its value is regression detection.

**A11 (R11) — no promotion of member-private third-party claims.**
Runner: `eval/test_ceiling_audience.py::test_a11_*`. Fixture: import-graph scan proving no code path rewrites a member-owned fact's `owner`/scope to `household` or a care-team scope; plus a behavioral case asserting a member-private third-party claim is not visible household-wide. Twin: a synthetic promotion helper must be flagged. Metamorphic: reworded queries resolving to the same subject must not change visibility.
*Preventive.* Passes because no promotion path exists — which is exactly what must not silently change.

**A27 (R27) — no objective rewards grant acceptance or sensitive-data growth.**
Runner: `eval/test_ceiling_solicitation.py::test_a27_*`. Fixture: static scan of training configs, metric definitions, and dashboard queries for any objective keyed on acceptance rate, disclosure volume, or graph depth. Twin: a synthetic metric definition rewarding acceptance must be flagged. Metamorphic: renaming the metric must not evade.
**L7:CS1 interaction:** the Curator scorer is shadow-only and CS1 already proves it has no code path to the prompt. A27 is the *optimization-target* half of the same concern and must not be read as re-proving CS1's no-act property. Partly vacuous today (no grant machinery exists), so it guards against introduction.

**A29 (R29) — one sensitivity registry.** **Already LIVE.**
Runner: `eval/test_sensitivity_registry.py`, wired at `scripts/run_harness.sh`. Fixture: hand-authored level table. Twin: AST guard fails if any consumer re-introduces a literal sensitivity ordering. Metamorphic: `rank()` has no default parameter, so no caller can reintroduce a default. **R29 ruled MET 2026-08-01.**

**A30 (R30) — `critical` outranks `high` everywhere.** **Already LIVE.**
Runner: same file, 31 cases total with A29. Fixture: cross-module ordering table over registry, curator `_encode`, router threshold, permissions. Twin: unknown-value cases assert `UnknownSensitivity` rather than a default. **R30 ruled NOT MET** — item 5 unimplemented — **but A30 itself passes.** Recorded explicitly: *a passing acceptance row does not carry its requirement.*
**L7:CS1 interaction:** A30 asserts ordering inside the MET scorer's `sensitivity` feature. D-75 changed that feature's value (low 0.0→0.25, high 1.0→0.75); the key set is unchanged and cold-start uses recency only. CS1 held at `--layer 7` exit 0. Any future change here must re-run CS1 and report it.

### STRICT XFAIL (7)

**A1 (R1) — off-allowlist derived attribute refused.**
Runner: `eval/test_ceiling_inference.py::test_a1_*` (xfail strict). Why red: `DERIVABLE_ATTRIBUTES` **does not exist** (verified at HEAD); `consolidate.py` never validates `df.attribute` against any allowlist, while `extraction_queue.py:229,:903` validates only the extraction path. Fixture: derived-fact write with an off-allowlist attribute; plus the `risk_pattern` twin, which must be **accepted** (it is deliberately outside `CANONICAL_ATTRIBUTES` per Bill's 2026-07-17 ruling so only derivation may emit it). Flips when: the allowlist builds. **Warning carried from D-63:** the allowlist is a *second* vocabulary — it must contain `risk_pattern` while excluding things `CANONICAL_ATTRIBUTES` contains, so the two overlap without nesting. That is the drift shape that produced three contradictory trust orderings.

**A10 (R10) — `store.py::encode` cannot be bypassed.**
Runner: `eval/test_ceiling_inference.py::test_a10_*` (xfail strict). Why red: `encode` exists at `memory_engine/store.py:352` and performs **no** origin, registry, representation, or permit check. Fixture: a direct `encode()` call bypassing the extraction path. Twin: the same call routed through the guarded path must succeed. Flips when: R10's checks land at the encode boundary.

**A18 (R18) — retracting a parent invalidates dependent children.**
Runner: `eval/test_ceiling_retention.py::test_a18_*` (xfail strict). Why red: `derived_from` is **written** by `consolidate.py:525` and read for lineage display (`truth_layer/queries.py:228,:306,:365`) but **never read for invalidation**. Fixture: source fact + derived child; retract the source; assert the child is invalidated. Twin: the "surviving prohibited cognitive child" case the row names. Flips when: the cascade builds. *Smallest concrete fix in the whole plan, and it has a live defect behind it.*

**A19 (R19) — erased source IDs leave no active vector entries.**
Runner: `eval/test_ceiling_retention.py::test_a19_*` (xfail strict). Why red: embeddings are stored over `"{owner} {attribute}"` (`extraction_queue.py:23,:32-38`) and **survive retraction** — `retract_fact` sets `valid_to` and clears nothing. Fixture: write a fact, retract it, assert no active vector entry references it. Twin: a monolithic cross-policy summary write must be refused. Flips when: R19's derivative governance builds. *Narrow but real: the value never entered the vector (TD-030 holds), yet the existence and shape of a retracted fact persist.*

**A20 (R20) — production data excluded from training/evaluation/export.**
Runner: `eval/test_ceiling_retention.py::test_a20_*` (xfail strict). Why red **in part**: the *training* third is genuinely gated — `learner_isolation.check_training_example` exists, is MET, and L7:LI1 proves it. The *evaluation* and *export* thirds have no equivalent control. Fixture: production-derived record offered to an evaluation/export path. Twin: the training path must still refuse a cross-scope example. Flips when: export policy + lineage build. **Recorded honestly: one third of this row already passes; the row as written does not.**

**A21 (R21) — calculable expiry; missing retention policy blocks writes.**
Runner: `eval/test_ceiling_retention.py::test_a21_*` (xfail strict). Why red: no retention-policy mechanism exists. Fixture: a feature with no retention policy attempting a durable write. Twin: a feature with a policy must produce a calculable expiry. Flips when: R21 builds.

**A26 (R26) — decline and non-response preserve baseline service.**
Runner: `eval/test_ceiling_solicitation.py::test_a26_*` (xfail strict). Why red: `confirmation_gate.apply_decline` exists — so the *decline* half is partly testable — but **non-response is not modelled at all**, and there is no "adverse inference" or caregiver-notification surface to assert the absence of. Fixture: decline a parked claim, assert subsequent service is unchanged and no adverse record is written. Twin: a synthetic adverse-inference write must be flagged. Flips when: the circumstance model (R24) exists to define non-response.

### UNWRITABLE (16)

Fixtures do not exist. **Not written.** Each names the fixture, its cost, and the write authorization required.

| Row | Missing fixture | Cost | Write authorization needed |
|---|---|---|---|
| **A2** (R2) | Typed inference permit with declared inputs/predicates | New permit type + registry + enforcement at the abstraction boundary | None — pure build — ~~UNWRITABLE~~ REASON CLOSED at D-130 (harness/inference_permit.py). **RE-TIERED LIVE, D-145** — row written against the real creator path; see §7.7 |
| **A3** (R3) | Fixture set for every prohibited autonomous-label class | Requires the prohibited-label taxonomy to be enumerated first | Ethicist review (Part 4 adjacency) before fixtures are authored |
| **A4** (R4) | Separate write kinds: observation / support state / temporary hypothesis | Schema change on `:Fact` + write-path branching | Graph schema write + migration of 12 existing nodes |
| **A5** (R5) | A "sensitive hypothesis" object plus permit/retention surfaces to observe non-expansion | Depends on A2 and A4 landing first | None — pure build, but sequenced |
| **A6** (R6) | **A validated sensing contract.** Pure design today — nothing in the codebase represents one | Highest fixture cost in the plan | See the A6 note below |
| **A8** (R8) | Representation classes incl. `UNKNOWN_HIGH_RISK` | New enum + write-time validation; verified absent at HEAD | Graph schema write — ~~UNWRITABLE~~ REASON CLOSED at D-140 (harness/representation_class.py). **RE-TIERED LIVE, D-145** — row written against the real creator path; see §7.7 |
| **A9** (R9) | Credential / continuous-surveillance / graph-biometric / raw-intimate-media / third-party-dossier fixtures | Six hostile fixture families, several requiring synthetic sensitive media | **Explicit authorization to author sensitive-media fixtures**; ethicist review |
| **A13** (R13) | Three separately audienced objects from one third-party input | Depends on the R13 object model | Graph schema write |
| **A14** (R14) | Care-role projection + emergency-access expiry | **Blocked upstream:** `REQ_CARE_TEAM_READ_AUTH` is NOT MET, its own acceptance has no executable form (D-68), and TD-138 (epoch-blindness) is OPEN in that path. Both care-team tables are EMPTY, so the INJ-3 permit cannot fire at all | Registry writes to enroll caregivers; **TD-138 resolved first** |
| **A15** (R15) | A conflict/safeguarding hold object | Depends on Part 4's safeguarding process, which is expert-gated | **Ethicist + attorney sign-off** (Part 4 ADVISORY tier) |
| **A17** (R17) | Separately erasable active artifacts across row, key, vector, cache, index | ~~The only hard delete in the codebase is `server/demo_dashboard.py:1890`... nuke-the-graph. No per-fact delete exists anywhere~~ REASON CLOSED at D-R-169/170/172 (`harness/graph_erasure.py`, `harness/erasure_request.py`) — cascade-aware per-fact and per-member erasure, machine-verifiable report, real (if unenabled) request path. **RE-TIERED LIVE, D-R-179** — row written and run at D-R-173, against the real request path; see §7.8 | ~~Graph destructive-write authorization~~ none needed — fixture-scoped only, no real/destructive data touched |
| **A22** (R22) | Backup + restore cycle with tombstone reapplication | Requires a backup/restore path and a UI distinguishing four erasure kinds | Backup infrastructure; destructive-restore authorization |
| **A23** (R23) | Purpose-trigger registry | Axis 5 is wholly unbuilt — verified no `purpose_trigger` / `offer_circumstance` / `solicitation` symbol exists | None — pure build |
| **A24** (R24) | Circumstance-version model | Same; A26 depends on this | None — pure build |
| **A25** (R25) | Adversarial prompt-mutation suite | Suite + a stability record. **Tier already ruled:** D-70 moved A25 ABSOLUTE→STANDARD because a flaky adversarial suite at ABSOLUTE would block every sprint | None — pure build |
| **A28** (R28) | Cumulative authority manifest | Depends on categories, audiences, permits, expiries all existing to reconstruct from | None — sequenced last |

### A6 — the minimum fixture, stated as the dispatch requires

A6 asserts that **missing confirmation produces no derived fact absent a validated sensing contract.** A "sensing contract" is pure design: nothing in the codebase represents a sensor, its validation, or its coverage guarantee.

**The minimum fixture that would make A6 writable** is not a sensor. It is a **declared, checkable sensing-contract record** carrying: the observable it claims to sense; its coverage window; its known false-negative mode; and an explicit validity flag. A6 then becomes testable **without any sensor existing**: assert that an absence-derived write is refused when no contract record covers the observable, and permitted when one does.

That is a small, cheap fixture — a record type and a validation function — and it is the difference between A6 being untestable and A6 being a strict-xfail. **Recommended: build the contract record, move A6 to STRICT XFAIL.** Until then it stays UNWRITABLE, because a test asserting "no inference from absence" with nothing to distinguish sensed-absence from unknown-absence would pass vacuously and report coverage it does not have.

---

## 6. WHAT THIS REQ DOES NOT CLAIM

- **No tier assignment is a ruling.** All 30 rows remain unruled except R29/R30, whose status is recorded in the authority REQ.
- **A passing row does not carry its requirement.** A30 passes while R30 is NOT MET. Stated in the plan so no future reader reads a green suite as a met requirement.
- **The LIVE count is 5, and three of those are near-vacuous today** (A7, A11, A27 hold by absence). Their value is regression detection, not present assurance. Recorded rather than counted as coverage.
- **Nothing here is built.** No test file in this plan exists yet except `eval/test_sensitivity_registry.py`, which D-75 landed.
- **UNWRITABLE is not a backlog ranking.** It is a statement that writing the test today would produce a check that passes against a fiction.


---

## 6. WIRED vs CLASSIFIED — amended by D-86, 2026-08-01

**This section records EXECUTION STATE ONLY. It proposes no status, rules no requirement
MET, and changes no tier assignment above.** Sections 1-5 are left exactly as filed.

The audit behind it: `/tmp/d86_ceiling_acceptance_audit.md`, and the per-row table is
reproduced in the D-86 dispatch doc.

### The finding

**3 of 30 rows had an executable check when D-86 began.** The five runner files named in
section 5 — `test_ceiling_representation.py`, `test_ceiling_audience.py`,
`test_ceiling_solicitation.py`, `test_ceiling_inference.py`, `test_ceiling_retention.py`
— **none of them existed.** A18's absence was found at D-81 and A10's at D-84; D-86
establishes that this was true of every unbuilt row, not those two.

**In fairness to this plan, it never claimed otherwise.** Its own words: *"This is a plan,
not a ruling. The counts say 12 of 30 rows CAN be wired now."* The gap recorded here is in
the SYSTEM, not in this document — with one exception, A18, where the plan is now stale.

### State after D-86

| Row | Tier as classified (§2) | Execution state | File |
|---|---|---|---|
| A7 | LIVE | **WIRED by D-86** — 10 cases, green | `eval/test_ceiling_representation.py` |
| A11 | LIVE | **NOT WIRED — STOPPED, see below** | — |
| A27 | LIVE | not wired (downstream of the A11 stop) | — |
| A29 | LIVE | WIRED (D-75), verified not rebuilt | `eval/test_sensitivity_registry.py` |
| A30 | LIVE | WIRED (D-75), verified not rebuilt | same |
| A18 | STRICT XFAIL | **WIRED (D-81) and LIVE-PASSING — tier is STALE** | `eval/test_derivation_cascade.py` |
| A1, A10, A19, A20, A21, A26 | STRICT XFAIL | not wired (downstream of the A11 stop) | — |
| A12, A16 | CONTRADICTED-XFAIL | not wired — out of D-86's scope by instruction | — |
| 16 UNWRITABLE rows | UNWRITABLE | not wired — fixtures still absent | — |

All seven standing batteries green at `--layer 7`: 103 passed / 2 xfailed. AUDIT 8/8,
DISC 1/1, L7 27/27, L7V2 27/28 (1 opt-in skip), SCHEMA 1/1, VOICE 1/1, **RATCHET PASS, no
ABSOLUTE-tier check red.**

### A18 — the tier is now wrong, in the safe direction

Classified STRICT XFAIL. D-81 built the cascade, and the row **passes**. Recorded here
rather than silently re-tiered: **re-tiering is Bill's call.** Note what it does not mean —
R18 is **NOT MET** (TD-139, TD-140, TD-141). A passing row does not carry its requirement,
exactly as this plan already records for A30.

### A11 — STOP. §5's rationale and fixture are falsified at HEAD

**D-86 stopped here rather than guessing, and wired nothing after it.**

Section 5 says A11 *"passes because **no promotion path exists**"* and specifies an
*"import-graph scan **proving no code path rewrites** a member-owned fact's `owner`/scope
to `household` or a care-team scope."*

**Promotion paths do exist, and they are ratified:**

| Path | Site |
|---|---|
| `share_household` directive → `CLASS_HOUSEHOLD`, owner rewritten to `"household"` | `harness/write_rule.py:160-168` |
| `share_care_team` directive → `CLASS_CARE_TEAM` | `harness/write_rule.py:170-179` |
| `flag_safety` → care team, subject excluded | `harness/write_rule.py:181+` |
| attribute default `attribute == "household"` | `harness/write_rule.py:191`, `harness/fact_change.py:693` |

**R11 is nonetheless satisfied — by a CONTROL, not by absence.** The household-circle
widening restriction, ratified 2026-07-21 (`harness/write_rule.py:161-167`): an author may
widen to household-circle only for facts about themselves or generic household facts,
`if subj is None or subj == author`, otherwise falling through without widening; plus
care-team paths gated on `is_recipient` **and** `is_active_caregiver`; plus the mandatory
subject-exclusion rule generalized the same day.

**Why this blocked the row instead of being a footnote.** Writing §5's fixture as specified
produces a check that is **red on arrival against correct, ratified behavior** — and the
only way to make it green would be to delete the widening feature. Writing the *right*
check instead — a behavioral assertion that a third-party claim does not widen while a
self-claim does — is a **different assertion than this plan authorizes**, and it converts
A11 from an absence scan into a real test of a live access-control path.

**Recommendation for Bill's ruling, not a self-substitution:** re-specify A11 as a
behavioral test of the widening restriction. It would be one of the few ceiling rows that
asserts a control that **actually exists** rather than an absence. And correspondingly:
A11 is **not** "vacuously true today." That characterization holds for A7 and A27; it does
not hold for A11.

### A7 — wired, and what it is worth

Written as a **regression tripwire and labelled as one in its own docstring**, so no later
reader mistakes it for coverage. It holds by ABSENCE: nothing refuses a reasoning-trace
write; nothing ever attempted one. Its value is catching the commit that introduces one.

AST-based, never a source regex — with `test_a7_scanner_ignores_comments_and_docstrings`
asserting the D-75 failure directly (that dispatch's first A29 guard fired on its own
explanatory comment). Fault twin executed, so red-on-command is demonstrated rather than
asserted; metamorphic variants cover renames and aliased imports; and
`test_a7_scan_actually_covered_the_packages` guards against the vacuous pass where a scan
walking zero files reports no offenders.

### A29/A30 — a fault-twin gap, recorded

§5 calls the AST guard "the twin." By `REQ_HARNESS_DISCIPLINE`'s own definition — *"the
specific mutation that turns the check red"* — it is a **guard**, not a twin: no mutated
consumer is executed and proven to fire it. A18's twin and A7's twin are both executed.
Recorded as a gap in those two rows' four-part coverage, **not** as a defect in the
registry they protect.


---

## 7. WIRING COMPLETE — amended by D-87, 2026-08-01

**Execution state and two corrections. No tier is re-derived here beyond the two Bill
ruled, no requirement is ruled MET, and sections 1–5 stay as filed.** Section 6 (D-86)
recorded the audit; this records what was wired against it.

### 7.1 State — 12 of 12 writable rows are now wired

| Row | Tier | File | State |
|---|---|---|---|
| A7 | LIVE | `eval/test_ceiling_representation.py` | WIRED (D-86) — regression tripwire |
| A11 | LIVE | `eval/test_ceiling_audience.py` | **WIRED (D-87) — control assertion, re-specified; see 7.2** |
| A27 | LIVE | `eval/test_ceiling_solicitation.py` | WIRED (D-87) — regression tripwire |
| A29 | LIVE | `eval/test_sensitivity_registry.py` | WIRED (D-75); **executed twin added D-87, see 7.4** |
| A30 | LIVE | same | WIRED (D-75); **executed twin added D-87, see 7.4** |
| **A18** | **LIVE — tier CORRECTED, see 7.3** | `eval/test_derivation_cascade.py` | WIRED (D-81), passing |
| **A1** | **LIVE — tier CORRECTED, see 7.6** | `eval/test_ceiling_inference.py` | WIRED (D-87), re-derived predicate + re-tiered (D-100), passing |
| A10 | STRICT XFAIL | same | WIRED (D-87), red |
| A19 | STRICT XFAIL | `eval/test_ceiling_retention.py` | WIRED (D-87), red |
| A20 | STRICT XFAIL | same | WIRED (D-87), red — one third already passes |
| A21 | STRICT XFAIL | same | WIRED (D-87), red |
| A26 | STRICT XFAIL | `eval/test_ceiling_solicitation.py` | WIRED (D-87), red |

Untouched by instruction: A12 and A16 (CONTRADICTED — they need rulings, not fixtures)
and the 16 UNWRITABLE rows (their fixtures still do not exist).

**Eleven standing batteries: 148 passed, 9 xfailed.** `--layer 7`: AUDIT 8/8, DISC 1/1,
L7 27/27, L7V2 27/28 (1 opt-in skip), SCHEMA 1/1, VOICE 1/1, **RATCHET PASS**, 0 scenario
FAILs, and all five ABSOLUTE checks PASS (G0, PSA1, CTX-STRIP, LI1, CS1). `--full` was not
attempted — TD-129's memory guard refuses it on this machine state, as expected.

**No XFAIL row passed unexpectedly.** All six are `strict=True`, so an unexpected pass
would have surfaced as a hard failure and triggered the stop condition. None did.

### 7.2 A11 — corrected basis (Bill's ruling, 2026-08-01)

**Section 5's basis for A11 was wrong and is superseded.** It read: *"passes because no
promotion path exists,"* with a fixture *"proving no code path rewrites a member-owned
fact's owner/scope to household."* D-86 stopped on this rather than writing it.

Promotion paths exist and are **ratified**: `share_household` rewrites `owner` to
`"household"` (`harness/write_rule.py:160-168`); `share_care_team` (`:170-179`);
`flag_safety` (`:181+`); and the attribute default (`:191`, `harness/fact_change.py:693`).
Writing the specified fixture would have produced a check **red on arrival against correct
behavior**, whose only green path was deleting a ratified feature.

**R11 is satisfied by a CONTROL, not by absence** — the household-circle widening
restriction, **ratified 2026-07-21** (`harness/write_rule.py:161-167`):

```python
if directive == "share_household":
    # an author may widen to household-circle only for facts about themselves
    # or generic household facts — never a fact about someone else without
    # THEIR standing policy. If blocked, fall through to levels 3+.
    if subj is None or subj == author:
```

with the care-team paths additionally gated on `is_recipient(subj)` **and**
`is_active_caregiver(subj, author)`, and the mandatory subject-exclusion rule generalized
the same day.

**A11 stays LIVE, but as a control assertion.** It now asserts behaviorally, in both
directions, that promotion to household scope occurs **only** under that restriction: a
self-claim widens, a third-party claim does not. Fault twin `_unrestricted_classify`
reimplements the directive branch with the subject check removed and is **executed** — it
promotes bill's claim about maya and therefore fails the same assertion the real
classifier passes.

**This is materially better than the row it replaces.** A11 is now one of very few ceiling
rows asserting a control that *actually exists* rather than an absence — and correspondingly
**A11 is no longer "vacuously true today."** That characterization still holds for A7 and
A27; it does not hold for A11.

### 7.3 A18 — tier CORRECTED to LIVE

**A18 is re-tiered from STRICT XFAIL to LIVE.** D-81 built the cascade and the row has
passed since; D-86 identified the tier as stale. The classification was correct when
written and was overtaken by the build.

**R18 REMAINS NOT MET** — ruled by Bill, 2026-08-01, recorded in §16 of
`REQ_STRUCTURAL_CEILING`. TD-139 (the lineage block is 2 of 11 fields), TD-140 (the
recompute branch never executes — R18 says recompute-then-invalidate and only invalidate
exists), TD-141 (the live graph's one derived fact has empty `derived_from`, so the cascade
is correct but inert).

**A passing row does not carry its requirement.** This is now the third instance on file —
A30 passes while R30 is NOT MET, A18 passes while R18 is NOT MET, and A20 passes in one
third while R20 does not. Re-tiering A18 records where the *check* stands, and says nothing
about where the *requirement* stands.

### 7.4 A29/A30 — the fault-twin gap is closed

D-86 found that §5 called the A29 AST guard "the twin," but by `REQ_HARNESS_DISCIPLINE`'s
own definition — *"the specific mutation that turns the check red"* — it was a **guard**:
real, but never executed against a mutated consumer, so nothing proved it fires.

Closed in D-87, matching the A7 pattern. The guard's logic was extracted to
`_local_ordering_names()` so a twin can execute it, and four cases now run:

- **A29 twin** — a consumer re-introducing a local `SENSITIVITY_RANK` literal **is** flagged.
- **A29 partial twin** — TD-137's actual shape (`critical` below `high`) **is** flagged.
- **A29 discriminating half** — a low/medium/high **confidence** table is **NOT** flagged.
  Without this the twin would prove only that the guard fires, not that it fires on the
  right thing; a guard that flags a legitimate confidence table is a nuisance, and a
  nuisance guard gets disabled.
- **A29 prose immunity** — comments and docstrings describing the old encoding are **NOT**
  flagged. This is the D-75 defect asserted directly rather than trusted.

Plus three executed A30 twins against `_order_is_correct`: TD-137's real ordering, a
`critical == high` tie (the near-miss a `>=` comparison would admit), and a **defaulting**
rank function (the silent-downgrade shape D-75 found in three places), together with an
anti-vacuity case proving the predicate accepts the real registry.

### 7.5 Conventions adopted, and why

**Namespacing.** Ceiling acceptance rows are `test_ceil_a<N>_*`, in files named
`eval/test_ceiling_*.py`, and are referred to as **CEIL-A<N>** in prose. D-86 established
the need: **four independent A-numbering schemes coexist in this repo** — the ceiling's
A1–A30, care-coordination A1–A4 (`eval/care_coord_run.py:26`), demo-smoke A1–A4
(`eval/test_demo_smoke.py:132`), and L5 red-team A1–A5 (`eval/harness.py:9`). A bare `A1`
is ambiguous across four meanings, and a naive grep overstated coverage by four rows. A7's
functions were renamed from `test_a7_*` to `test_ceil_a7_*` so the convention has no
exceptions.

**What a fault twin means for an XFAIL row.** A LIVE row's twin is a broken implementation
that must go red. An XFAIL row is *already* red, so "it can go red" proves nothing — the
real hazard is an xfail red for the **wrong reason** (a typo, a bad import, a predicate
that could never pass whatever was built). So every XFAIL row here carries a
`*_predicate_accepts_a_conforming_fixture` case, **not** xfail, running the same predicate
against a synthetic implementation that *does* have the feature. If the predicate cannot
accept a conforming fixture, the xfail is decorative. Several also carry a near-miss case
proving the predicate is not trivially satisfied.

**Anti-vacuity everywhere.** Every scanning row asserts its corpus is non-empty and its
target still exists, because a scan that walks zero files reports no offenders and looks
identical to a pass.

**Two predicate bugs were found this way, in D-87's own checks.** A26's predicate demanded
an exact module-level name and rejected `record_non_response` — it would have been
unsatisfiable by any real implementation. A27's scanner missed
`optimize(objective="acceptance_rate")`, where the forbidden term is the keyword *value*
rather than the keyword. Both were caught by the conforming-fixture and twin cases, which
is precisely what they exist for, and both are fixed.

### 7.6 A1 — tier CORRECTED to LIVE (D-100, 2026-08-01)

**A1 is re-tiered from STRICT XFAIL to LIVE.** D-99 probed the requirement live and proved
the row's own red was false — the enforcement A1 asks for exists — but deliberately left the
predicate and tier both unchanged, because correcting the predicate alone would XPASS a
`strict=True` xfail and red the suite. D-100 applies both together, in the same edit, exactly
as D-99's report specified.

**Why the OLD predicate was stale, in both halves — the discriminating detail is that it was
stale for reasons different from why the row was originally filed red.** It scanned
`DERIVABLE_ATTRIBUTES` in four candidate files (`harness/extraction_queue.py`,
`memory_engine/consolidate.py`, `harness/write_rule.py`, `harness/sensitivity.py`) that
deliberately excluded `harness/write_origins.py`, where the allowlist now actually lives
(D-97). It also looked for enforcement **inside `_write_derived_node`'s own AST body** — but
since D-96 converged the three `:Fact` CREATE paths onto one materialization point,
`_write_derived_node` **delegates** to `memory_engine.store.create_fact_node` rather than
validating inline, so even a predicate correctly pointed at `write_origins.py` would still
have read the wrong function and found nothing.

**Fixed by probing behaviourally instead of reading source** — the same fix D-99 applied to
A10 (§7.4's neighbor, not a coincidence: both rows' predicates broke for the identical D-96
reason). The new predicate, applied verbatim from D-99's report:

```python
def _a1_enforced() -> bool:
    from harness.write_origins import DERIVABLE_ATTRIBUTES        # must exist
    import memory_engine.store as _store
    rec = _ProbeRecorder()
    try:
        _store.create_fact_node(rec, _probe_props("not_on_the_allowlist"),
                                origin="derivation")
        return False                                              # not refused
    except ValueError as e:
        if "derivation may not emit" not in str(e) or rec.calls:
            return False                                          # wrong reason, or wrote
    rec = _ProbeRecorder()
    _store.create_fact_node(rec, _probe_props("risk_pattern"), origin="derivation")
    return bool(rec.calls)                                        # twin accepted
```

Shares `_ProbeRecorder`/`_probe_props` with CEIL-A10. Two now-obsolete companion tests of the
deleted AST-based predicate (`*_predicate_accepts_a_conforming_fixture`,
`*_predicate_rejects_an_allowlist_that_is_never_consulted`) were removed rather than left
dangling — they tested the discriminating power of a predicate mechanism that no longer
exists, matching D-99's own precedent for A10's obsolete companions.

**R1 IS MET** — ruled by Bill, 2026-08-01, recorded in §16 of `REQ_STRUCTURAL_CEILING`.
Unlike A18/R18 (where the row passing did NOT carry its requirement, because R18's gap is
substantive and independent of A18's own mechanics), here the row and the requirement move
together: A1's own predicate, correctly derived, **is** R1's acceptance test, and Bill's
ruling states plainly that the requirement is satisfied by the same evidence that makes the
row pass. Recorded as a MET requirement, not merely a re-tiered row, for that reason —
the general caution "a passing row does not carry its requirement" still applies by default
to every OTHER row in this document and is not weakened by this one exception.

**Evidence, read individually from the log:** standing batteries 244 passed / 8 xfailed (was
245/9 at D-99 — net change accounted for exactly: −2 from removing the two obsolete
companion tests, −1 more from A1 leaving the xfail column, +1 from A1 entering the passed
column). `AUDIT: 8/8`, `L7: 27/27`, `L7V2: 27/28` (1 opt-in skip, unchanged), `SCHEMA: 1/1`,
`VOICE: 1/1`, `RATCHET PASS`, 0 scenario FAILs, all five ABSOLUTE individually: `G0 PASS`,
`PSA1 PASS`, `CTX-STRIP PASS`, `LI1 PASS`, `CS1 PASS`. **Memory harness 13/17 — identical to
the D-96/D-97/D-99 baseline, failing the same four (MEM-115/116/117/118), zero delta** — the
step-3 STOP-on-delta condition did not fire. `--full` refused by TD-129 (`>=2GB free memory`
guard), as anticipated; not fought.

**A passing row usually does not carry its requirement — recorded here as the exception, not
the rule, so it is not mistaken for a change in that convention.** A30/R30, A18/R18, and A20
(passes in one third)/R20 all still stand as prior instances of a passing row that does
*not* carry its requirement; A1/R1 is different because R1's own text names exactly A1's
behavior as the whole of what it requires, with nothing further downstream the way R30's
item 5 or R18's recompute branch were.


### 7.7 A2 and A8 — RE-TIERED UNWRITABLE → LIVE (D-145, Bill's explicit instruction)

Both rows were tiered UNWRITABLE for the same kind of reason: **the thing the row
would assert against did not exist.** Both reasons are now closed, and the rows were
written and run in the same edit as this re-tiering (the A1/D-100 rule: a tier and its
predicate move together, or the suite goes red on the mismatch).

| Row | Filed UNWRITABLE reason | What closed it |
|---|---|---|
| **A2** (R2) | "New permit type + registry + enforcement at the abstraction boundary" | `harness/inference_permit.py` (D-130, `dec92f3`) — the twelve-field `InferencePermit` and `ABSTRACTION_PERMIT`, enforced in `create_fact_node` on every `origin="derivation"` write |
| **A8** (R8) | "New enum + write-time validation; verified absent at HEAD" | `harness/representation_class.py` (D-140, `bc56fc4`) — fourteen classes incl. `UNKNOWN_HIGH_RISK`, classified in `create_fact_node` before persistence, failing closed |

**Both rows assert against the REAL path** — `memory_engine.store.create_fact_node`
with a recording transaction — not against D-130's or D-140's own standalone probe
scripts. Per `_a10_enforced_at_creator`'s counting rule, **a check counts only if the
creator RAISES and issues NO write**; both rows assert the refusal AND the absence of
the write, because a creator that raises after writing has enforced nothing.

Each row carries an EXECUTED fault twin — a broken implementation, not a guard — and
an anti-vacuity case:

- **A2's twin** replaces `ABSTRACTION_PERMIT` with one whose `allowed_input_attributes`
  admits the off-permit attribute. Observed: the identical write flips from
  *refused, no row issued* to **accepted and written**.
- **A8's twin** replaces `classify_representation` with one that never fails closed.
  Observed: the unplaceable artifact flips from *refused, no row issued* to
  **accepted and written**.
- **Anti-vacuity, A2:** a conforming derivation is NOT refused on permit grounds, and
  the permit declares non-empty input/output sets with an evidence floor ≥ 2.
- **Anti-vacuity, A8:** not everything classifies to the fail-closed bucket
  (`medication`→HEALTH_CLAIM, `employer`→ORDINARY_CLAIM), which would otherwise make
  the fail-closed row pass for free; and the class vocabulary is non-degenerate.

**A PASSING ROW DOES NOT CARRY ITS REQUIREMENT.** R2 is ruled **NOT MET** (D-143 —
scope gap, R5/R6/R7 unaddressed) and R8 is ruled **NOT MET** (D-144 — silent
absorption). Both remain NOT MET after this dispatch, and **R10 remains NOT MET**: A10
is downstream of A2 and A8, and its own row is unchanged here. This is the fifth
instance of that distinction on file (A30/R30, A18/R18, A12/R12, A1/R1, and now
A2·A8).

### 7.8 A16 and A17 — RE-TIERED CONTRADICTED-XFAIL/UNWRITABLE → LIVE (D-R-179, Bill's ruling, 2026-08-05)

Both rows were blocked on the same named condition: **the R16 ruling of D-71 (both
mechanisms, built together) with R17 promoted to load-bearing — "A16 and A17 must flip
together."** That condition closed across D-R-161 through D-R-172 (the ledger v1→v2
cutover across all 17 real production call sites, and the cascade-aware erasure mechanism
with its machine-verifiable report and real request path), confirmed gone at D-R-173,
which wrote and ran both rows for the first time — **the SAME edit that flips the tier
carries no new fixture: D-R-173 already built and ran it, this records the ruling landing
on an already-proven row, not a tier moving ahead of its check.**

| Row | Filed blocker | What closed it |
|---|---|---|
| **A16** (R16) | "The ledger deliberately carries AES-256-GCM member-actor payloads; erasure is by key destruction, not absence." CONTRADICTED-XFAIL — fails against ratified design, not an unbuilt feature | The D-71 ruling **built**: `harness/epistemic_ledger.py` + `harness/ledger_commitment.py` + `harness/ledger_payload_store.py`, all 17 real production call sites cut over to `hel_version="2.0"` (D-R-161 through 168) |
| **A17** (R17) | "The only hard delete in the codebase is `server/demo_dashboard.py:1890`... nuke-the-graph. No per-fact delete exists anywhere." UNWRITABLE — the fixture did not exist | `harness/graph_erasure.py` (`erase_fact`, `erase_member_facts`, cascade-aware, D-R-169/170), the machine-verifiable report (`harness/erasure_report.py`, D-R-167/169/170/172), and the real request path (`harness/erasure_request.py`, D-R-172) |

**Both rows assert against the REAL mechanism** — `harness.epistemic_record.log_epistemic_record`
(the one call site every real household turn already reaches) for A16, and
`harness.erasure_request` (the real, if unenabled, request path) for A17 — not against a
standalone probe script, matching the same discipline §7.7 established for A2/A8.

Each row carries an EXECUTED fault twin, written at D-R-173:

- **A16's twin** (`test_ceil_a16_fault_twin_a_v1_event_fails_the_same_check`): the
  identical forbidden-field check, run against a genuine `hel=="1.0"` event, correctly
  finds a forbidden field — proving the check discriminates version, not merely asserting
  a tautology against the v2 path alone.
- **A17's twin** (`test_ceil_a17_fault_twin_an_incomplete_erasure_is_caught`): an
  incomplete erasure (cascade bypassed, one derived child left behind) is correctly
  refused by `verify_erasure_report` rather than passed.
- **Anti-vacuity, A16** (`test_ceil_a16_anti_vacuity_forbidden_and_permitted_sets_are_real`):
  the forbidden/permitted field sets themselves are non-trivial, not empty-by-construction.
- **Anti-vacuity, A17** (`test_ceil_a17_anti_vacuity_erasure_mechanism_and_report_both_exist`):
  the functions under test are real, not renamed out from under the row.

**UNLIKE A2/A8, this is not only "a passing row that does not carry its requirement" —
R16 and R17 are THEMSELVES ruled MET here (Bill, 2026-08-05), recorded in full in
`REQ_STRUCTURAL_CEILING` §16.** The distinction still matters and is recorded exactly:
the row passing at D-R-173 was the EVIDENCE; the ruling is a separate act, made here, not
self-assigned by the row's own green result. Both rulings carry PERMANENT limits stated
in the ruling text itself, not left as silent residue:

- **R16:** every `hel=="1.0"` event written before its own respective cutover remains
  forbidden-field-bearing forever — the two-population reality, accepted as the price of
  anchor preservation at D-R-161.
- **R17:** the backup step is externally blocked (no backup system exists to schedule
  expiry against); the vector step is structurally N/A (no embedding/vector store exists
  for it to remove); and — the largest limit — **no real caller anywhere in this codebase
  reaches either mechanism from an actual request**; the request path proven here is real
  but unconnected to any live, authorization-triggered flow, and that connection is a
  separate, unfiled requirement.

### 7.9 A10 — RE-TIERED STRICT XFAIL → LIVE (D-R-183, Bill's ruling, 2026-08-05)

A10 was blocked on a DIFFERENT condition than its own filed text: not that `encode`
performs none of R10's four revalidations (D-99 already disproved that — origin and
registry landed at `create_fact_node` and were proven to fire), but that the other two,
representation and permit, were **DOWNSTREAM of R8 and R2**, both then unproven. R2 and
R8 are both ruled MET above, the same dispatch, discharging A10's own stated block.

**The predicate and the tier flip land in this SAME edit — the A1/D-100 rule** (a tier
and its predicate move together or the suite goes red on the mismatch — an unedited
predicate would XPASS a strict xfail the moment it was un-marked, and an edited
predicate left under `xfail(strict=True)` would silently hide a real result either
way). `eval/test_ceiling_inference.py::_a10_enforced_at_creator` gained two new probes,
reusing CEIL-A8's and CEIL-A2's own real-path shapes rather than inventing a third
mechanism:

| Check | Probe added | Reuses |
|---|---|---|
| **representation** | `_probe_props("totally_unrecognized_attribute_xyz")` via `fixture` origin (the same D8/`risk_pattern` origin-exemption CEIL-A8's own fault twin uses) — refused as `UNKNOWN_HIGH_RISK`, no write issued | `test_ceil_a8_fault_twin_unknown_high_risk_refuses_the_write`'s exact shape |
| **permit** | `_derivation_props(source_categories=["medication", "not_a_real_attribute"])` via `derivation` origin — refused under `allowed_input_attributes`, no write issued | `test_ceil_a2_off_permit_input_attribute_is_refused_with_no_write`'s exact shape |

Both verified, this dispatch, to refuse for the SPECIFIC named reason (not merely SOME
exception): the representation probe's exception message reads `"representation_class
classified as UNKNOWN_HIGH_RISK"`; the permit probe's reads `"outside R2's
allowed_input_attributes"`. `test_ceil_a10_all_four_revalidations_land_at_the_creator`
is no longer `xfail`; its anti-vacuity companion (renamed from "two buildable checks"
to `test_ceil_a10_all_four_checks_do_fire`, since all four now do) asserts all four by
name. The two existing meta-level fault twins
(`test_ceil_a10_fault_twin_a_creator_enforcing_nothing_scores_zero`,
`test_ceil_a10_fault_twin_raising_after_the_write_does_not_count`) needed no change —
they monkeypatch `create_fact_node` entirely, so they already exercised the probe's own
discriminating logic regardless of how many real checks exist behind it.

**A TO-DO the ledger call-site enumeration precedent suggests, not built here:** a
standing check that catches new inference sites the same way
`eval/test_ledger_callsite_enumeration.py` catches new ledger call sites — filed as
TD-R-163 alongside R2's own MET ruling above, since the gap it names (R5/R6 hold by
absence with no regression tripwire) is the same shape as A10's own history (a check
that stays correct only as long as someone remembers to re-derive it by hand).
