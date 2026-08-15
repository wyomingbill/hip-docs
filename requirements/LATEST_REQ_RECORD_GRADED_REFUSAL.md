# REQ_RECORD_GRADED_REFUSAL — refusal checks assert on the execution record, not on reply text
Status: **NOT MET**. **AMENDED IN PLACE 2026-08-06 (HA-04) by Bill's ruling** — §6 item 2's
ground-truth fixture said `guard_kind="access_control"` where the system emits THREE guard
kinds; it now states all three, with the prior wording preserved verbatim inside the
annotation. The ruling's own words: *"the REQ's access_control-only key was the REQ being
wrong about the system — INJ-6b's own comment is the authority."* **Nothing is marked MET.**
**AMENDED AGAIN 2026-08-06 (HA-05), Bill's second ruling:** *"fix §6's field path —
guard_kind becomes guard.kind everywhere in the REQ including acceptance wording… A
fixture must be buildable from §6 as written against a real record."* The field path HA-04
flagged and left is now corrected wherever the REQ names the RECORD FIELD — acceptance row
1, the framing paragraph, WHAT'S ALREADY DONE's reader note, and §6 rows 1-2, which now
carry literal record dicts. **Every prior wording is preserved verbatim in an annotation
at its own site**, including Bill's original acceptance-row text. **The occurrences that
name the emitter's PARAMETER `guard_kind` are deliberately UNCHANGED** — that parameter
really is called `guard_kind`, and the table row recording that it is NOT EMITTED is the
authority this correction rests on; rewriting those would destroy the explanation.
Reconciled-Against: `9dd5aca` (roadmap HEAD at filing, read at filing time — not a remembered hash)
Filed: 2026-08-02 (Voice 37)
Decision-Owner: Bill
Related: `REQ_HARNESS_DISCIPLINE` (four-part standard, §6 below), D-16 (backlog item 12,
the same conflation from the reporting side), TD-132 (paraphrase limit on literal
canaries), `REQ_PROMPT_RECORD_FIDELITY` (the record as the instrument of record)
Sources: Voice 35 recon (read-only, `~/hip-roadmap` @ `827190a`); every claim it carried
was **re-verified against the code at `9dd5aca`** before being written in here, and two
were corrected — see §WHAT'S ALREADY DONE.

**THIS DOCUMENT AUTHORIZES NO BUILD BY ITSELF.** It is the REQ that a build dispatch must
name. Nothing in it was implemented in the dispatch that filed it (Voice 37 — REQ only).

---

## THE REQUIREMENT

Bill's own words, verbatim:

> "A refusal where no model ran and a refusal the model was told to produce look
> identical on screen and are not the same guarantee. Grade from the record."

**Expanded:** The product claim is that access control is *structural* — the gate decides
what enters the prompt, and a denied fact is absent rather than withheld by a cooperative
model. A check that reads the reply string cannot tell those two states apart, because
both produce refusal-shaped prose. Only the execution record distinguishes them: a
structural refusal has a `guard` block carrying `guard.kind` and **no inference**, while a
model-produced refusal
has `inference_ms > 0` and, in the case this requirement exists for, **no guard at all**.
Grading from the record makes the harness assert the guarantee the product actually
claims, instead of asserting that the wording came out right.

---

## THE ACCEPTANCE TEST

Six rows. Each passes or fails; none is a judgment call.

**1. Every Layer-4 outcome that asserts a refusal resolves against the turn RECORD —
`guard.kind` and `inference_ms` — not against reply text.**

> **FIELD PATH CORRECTED 2026-08-06 by Bill's ruling (HA-05, enacting the flag HA-04
> raised). Prior wording preserved, per the same pattern used throughout this REQ.**
>
> **BILL'S ORIGINAL ROW TEXT, VERBATIM:** *"Every Layer-4 outcome that asserts a refusal
> resolves against the turn RECORD — `guard_kind` and `inference_ms` — not against reply
> text."*
>
> **BILL'S RULING:** *"fix §6's field path — guard_kind becomes guard.kind everywhere in
> the REQ including acceptance wording."* The row above is his own text with that one
> substitution applied on his instruction — **the change is his, not a session's
> paraphrase of him**, which is why the original is quoted here rather than replaced.
>
> The prior annotation on this row said to read "`guard_kind`" as the CONCEPT because the
> emitted field is nested. That reading is no longer needed: **the row now names the
> literal path a predicate uses.** Reading it as a literal key name WAS the error that
> cost this build a red Layer-4 run — the row no longer sets that trap.
In scope: the `access_control` and `empty_set` outcomes at
`eval/harnesslib/layer4.py:61-66`. The `no_leak` outcome (`:67-69`) asserts the *absence*
of a wrong refusal and is in scope for the same reason. `value` (`:58-60`) is not a
refusal assertion and is out of scope for this REQ.
PASS when: each of those `s.check(...)` calls resolves on record fields.
FAIL when: any of them resolves on `classify_refusal(text)` or on `text` alone.

**2. A refusal outcome passes only when `inference_ms` is null. A non-null `inference_ms`
on an asserted refusal fails the check.**
Note the deliberate strictness: **null, not falsy.** `record_invariants.py:116` already
carries the fix for this exact bug — *"`if ms:` treats inference_ms=0 as no-inference
(falsy). Use explicit check."* A refusal row with `inference_ms=0` must FAIL row 2, because
zero means the model ran and returned instantly, not that it never ran.

**3. `classify_refusal` is no longer the sole basis for any refusal assertion.**
It MAY remain, and SHOULD, for reporting and for the `detail` string — the wording is still
worth seeing in a failure message. It MAY NOT decide pass/fail.
PASS when: no `s.check(...)` predicate in Layer 4 has `classify_refusal`'s return value as
its only determinant.
FAIL when: any does.

**4. FAULT TWIN — a turn producing refusal-shaped prose while the gate did NOT fire.**
It must **PASS today** and **FAIL after this lands**; removing the violation returns it to
green. This is the row that carries the requirement — see §WHAT'S KNOWN BROKEN for why the
existing G3 invariant cannot catch this case, structurally.
The twin must be executed, not described.

**5. The existing Layer-4 suite still passes on unmodified main.**
No new red from the change itself. **Any row that goes red is reported as a FINDING, not
fixed silently** — a row that was green only because text-matching accepted a
model-produced refusal is a real defect that this change surfaces, and it belongs in a
report and a debt entry, not in a quiet patch to make the suite green again.

**6. `REQ_HARNESS_DISCIPLINE`'s four parts are met** — twin, ground-truth fixture,
coverage entry, metamorphic wrapper. See §6 below for what each means here, so the build
cannot satisfy them nominally.

---

## WHAT'S ALREADY DONE

Do not rebuild any of this. Each was verified by reading the code at `9dd5aca`.

- **`g3_guard_implies_no_inference` exists and is correct**
  (`eval/oracle/record_invariants.py:112-119`). It is the assertion this REQ generalizes,
  and it already carries the `inference_ms=0` falsy fix in a source comment.
- **G3 has real fault twins and mutation killers.** Twins:
  `eval/harnesslib/harness_audit.py:183-185` — a `guard_triggered=True, inference_ms=88`
  record (must fire) against `inference_ms=None` (must not). Killers:
  `eval/harnesslib/mutation_targets.py:644-655` —
  `_kill_g3_guard_plus_inference_caught` and `_kill_g3_guard_without_inference_clean`.
- **CORRECTION TO THE VOICE 35 RECON, verified here: G3 is WIRED, not unwired.**
  `eval/harness.py:441` iterates `record_invariants.CHECKS` over the run's whole record
  corpus at L6, printing per-invariant PASS/FAIL. The recon's framing ("built but unwired")
  understated it. **This matters for scoping: the build must not "wire G3" — G3 runs. The
  gap is a different one, stated in the next section.**
- **The record-grading pattern is already proven in-tree**, on one assertion, on the write
  path: `eval/harnesslib/layer4.py:117-137`, with the reasoning in its own comment —
  *"Asserted on the d1.1 RECORD, not classify_refusal: EMPTY_SET_RE also matches the
  grounding rule's model-emitted refusal, so string classification cannot distinguish a
  structural guard from a model hedge (D-16). Record fields can."*
  It reads `path` and `guard.kind` off the record.
- **The record reader exists and is reusable**: `layer4.py::_last_record_for(query)`
  (`:~40`) returns the newest `logs/turns_demo.jsonl` record matching a query. The build
  should reuse it rather than write a second one.
- **The record carries the needed fields — CORRECTED IN PLACE 2026-08-02, and the earlier
  wording caused a real error.** What this line said before was: *"`harness/epistemic_record.py:184`
  (`guard_kind`, documented as `access_control | empty_set`)"*. **That cites the PARAMETER name of
  `emit_epistemic_record`, not an emitted field**, and the build read it as a top-level record key.
  It is not one. The cost was a full red Layer-4 run — 13 rows failing for a wrong-field lookup that
  looked exactly like a genuine finding — plus unit fixtures that were **green against a record
  shape that does not exist**, which is the worse half.

  **What the record ACTUALLY carries, verified against 43 live records, not against the emitter:**

  | Field | Where | Note |
  |---|---|---|
  | `guard_triggered` | **top level**, bool | present on every record; true on 24 of 43 |
  | `guard` | **top level**, dict — `{"kind": ..., "subject": ...}` | present iff `guard_triggered`; **the kind lives at `guard.kind`, NESTED** |
  | `guard_kind` | **NOT EMITTED — 0 of 43 records carry it** | it is the parameter at `:184`; the emitter builds the nested block at `:255` and writes it at `:288` |
  | `inference_ms` | top level, `:313` | null iff no model ran |
  | `path` | top level, `:265` | e.g. `guard_inj7` on an access-control refusal |

  **And there are THREE guard kinds, not the two the parameter comment names:**
  `access_control` (20), `empty_set` (2), **`attr_empty_set` (2)** — the last is INJ-6b's
  attribute-targeted guard and is every bit as structural an empty-set refusal. A predicate
  accepting only `empty_set` rejects genuine refusals. This was found by running the suite,
  not by reading the emitter — which is the same lesson as the field error above.

  **The general lesson, worth more than the correction:** build fixtures from a REAL RECORD, never
  from the emitter's signature. A parameter name and an emitted key are different things, and a
  fixture derived from the signature will agree with itself forever.

---

## WHAT'S KNOWN BROKEN

**Every Layer-4 refusal outcome is graded on reply text.**
`eval/harnesslib/layer4.py:54` computes `refusal = classify_refusal(text)`, and `:61-69`
decide `access_control`, `empty_set` and `no_leak` from it. `classify_refusal`
(`eval/harnesslib/server.py:113-123`) is two regexes over the reply string:

```python
if ACCESS_CONTROL_RE.search(text):  return "access_control"
if EMPTY_SET_RE.search(text):       return "empty_set"
return "none"
```

**A model that produces refusal-shaped prose while the gate never fired passes Layer 4
today.** That is the defect, stated as the symptom.

### Why G3 does not already cover this — the structural reason, and the crux of the REQ

G3 is wired and runs over every record. It still cannot catch the case in row 4, and the
reason is its first line (`record_invariants.py:113`):

```python
if not r.get("guard_triggered"):
    return None
```

**G3 asserts one direction only: `guard fired ⟹ no inference`.** A record where no guard
fired short-circuits to clean, whatever else is true of it. The missing direction is the
converse — **`asserted refusal ⟹ a guard fired`** — and no check anywhere asserts it.

So the two halves are:

| Direction | Asserted by | State |
|---|---|---|
| guard fired ⟹ no inference ran | G3, at L6, over the whole corpus | **BUILT and wired** |
| a refusal we asserted ⟹ a guard fired | *nothing* | **THE GAP** |

This is why row 4's twin is the acceptance test and not a formality: a turn with
refusal-shaped prose and `guard_triggered=False` is invisible to G3 **by construction**,
and passes Layer 4 **by text match**. It is currently green in two independent places for
two different wrong reasons.

### Related, already filed, and not to be re-litigated here

- **D-16** (backlog item 12): *"`EMPTY_SET_RE` can't distinguish a structural guard firing
  from a model hedge in the same words."* Same conflation, filed from the reporting side.
- **TD-132**: literal-substring canaries cannot see a paraphrase — the same class of limit
  on string-based judgment, from the leak-detection side.

---

## CONSTRAINTS

What must not regress.

1. **`classify_refusal` and its regexes stay.** Row 3 removes them from the *decision*, not
   from the codebase. They remain correct for reporting, and the F-4 distinction encoded in
   their ordering (`server.py:116-117` — access-control checked first so its wording is
   never mistaken for ignorance) is a real property that must not be lost.
2. **G3 is not to be modified.** It is correct, wired, twinned, and mutation-covered. This
   REQ adds the converse direction; it does not touch the direction that works.
3. **The L6 corpus sweep must keep passing**, including its phantom-record and
   mutation-window exclusions (`eval/harness.py:435-440`).
4. **No change to `harness/epistemic_record.py`'s schema.** Every field this REQ needs
   already exists. A build that widens the record to make the check easier has changed the
   instrument to fit the measurement.
5. **RATCHET must not regress**, and the five ABSOLUTE-tier checks (G0, PSA1, CTX-STRIP,
   LI1, CS1) must stay PASS.
6. **Row 5 is a hard constraint, not a hope.** If converting a row from text-grading to
   record-grading turns it red, **that red is a finding to report**, and the build stops to
   report it rather than adjusting the check until it is green. A check adjusted until it
   passes is the failure mode this whole requirement exists to remove.

---

## §6 — REQ_HARNESS_DISCIPLINE's four parts, stated so they cannot be met nominally

1. **Fault twin.** Row 4's twin, **executed**: a turn whose reply matches
   `EMPTY_SET_RE` or `ACCESS_CONTROL_RE` while the record has **no `guard` block**
   (`guard_triggered` false, `guard` absent) and `inference_ms` non-null. It must be shown
   PASSING before the change and FAILING after — both directions demonstrated, per the
   standing rule that a check which cannot be shown red on command is not load-bearing.
2. **Ground-truth fixture.** Hand-authored record dicts, never model-graded. **Written in
   the shape a REAL record has, so a fixture is buildable from this clause as written** —
   `guard_triggered` and `guard` are top level, the kind is NESTED at `guard.kind`, and
   there is no top-level `guard_kind` key on any record:

   ```python
   # (a) structural refusal — THREE fixtures, one per guard kind.
   {"guard_triggered": True, "guard": {"kind": "access_control", "subject": "maya"},
    "inference_ms": None, "path": "guard_inj7",  "reply": "<refusal text>"}
   {"guard_triggered": True, "guard": {"kind": "empty_set",      "subject": "maya"},
    "inference_ms": None, "path": "guard_inj6",  "reply": "<refusal text>"}
   {"guard_triggered": True, "guard": {"kind": "attr_empty_set", "subject": "maya"},
    "inference_ms": None, "path": "guard_inj6b", "reply": "<refusal text>"}

   # (b) model hedge — NO guard block at all, and a real inference.
   {"guard_triggered": False, "inference_ms": 88, "reply": "<refusal-shaped text>"}

   # (c) the boundary case — a guard WITH inference_ms=0, which row 2 requires to FAIL.
   {"guard_triggered": True, "guard": {"kind": "empty_set", "subject": "maya"},
    "inference_ms": 0, "reply": "<refusal text>"}
   ```

   **A predicate must therefore read `record["guard"]["kind"]`, never
   `record["guard_kind"]`** — the latter is absent from every record and would raise or
   silently read `None`, which is the failure this REQ has now made twice.

   > **AMENDED 2026-08-06 by Bill's ruling, enacted at HA-04. The correction is recorded,
   > not silent.**
   >
   > **PRIOR WORDING, preserved verbatim:** *"(a) structural refusal —
   > `guard_kind="access_control"`, `inference_ms=None`"*.
   >
   > **BILL'S RULING:** *"state 3 keys on `guard_triggered === true`. The REQ's
   > access_control-only key was the REQ being wrong about the system — INJ-6b's own
   > comment is the authority."*
   >
   > **WHY THE OLD WORDING WAS WRONG, and it is the REQ that was wrong, not the code.**
   > A structural refusal carries one of THREE kinds, all three emitted by shipped code:
   > `access_control` (`harness/realtime_adapter.py:369,428`, `server/voice_orch.py:3162`),
   > `empty_set` (`harness/injection_contract.py:806`, INJ-6), and `attr_empty_set`
   > (`harness/injection_contract.py:849`, **INJ-6b**). **INJ-6b's own comment is the
   > authority Bill names:** *"A personal QUESTION naming a precisely-keyworded attribute
   > must refuse STRUCTURALLY when no admitted fact carries that attribute."* A fixture
   > keyed on `access_control` alone therefore describes one third of the structural
   > refusals this REQ exists to grade, and a predicate built from it rejects genuine
   > refusals as though they were model hedges — the exact conflation the REQ was written
   > to end.
   >
   > **THIS REQ ALREADY KNEW.** Its own WHAT'S ALREADY DONE section records, verified
   > against 43 live records, *"there are THREE guard kinds, not the two the parameter
   > comment names: `access_control` (20), `empty_set` (2), `attr_empty_set` (2) — the
   > last is INJ-6b's."* So §6 item 2 contradicted the REQ's own authoritative evidence
   > section. This amendment removes the contradiction in the direction the evidence and
   > the code both point.
   >
   > **THE FIELD PATH — FLAGGED BY HA-04, NOW FIXED BY BILL'S SECOND RULING (HA-05).**
   >
   > HA-04's annotation read, and is preserved here verbatim: *"FLAGGED, NOT FIXED — a
   > second inconsistency in this same item… §6 still writes the field as `guard_kind`,
   > while this REQ's own verified table records that `guard_kind` is NOT EMITTED (0 of 43
   > records) and that the kind lives NESTED at `guard.kind`. … A fixture built from §6 as
   > it stands today will still use a key the record does not carry."*
   >
   > **BILL'S RULING, 2026-08-06:** *"fix §6's field path — guard_kind becomes guard.kind
   > everywhere in the REQ including acceptance wording, amended in place citing HA-04,
   > prior wording preserved per the same pattern. A fixture must be buildable from §6 as
   > written against a real record."*
   >
   > **DONE.** §6 rows 1 and 2 now describe the record's real shape — `guard_triggered`
   > and `guard` at top level, the kind NESTED at `guard.kind` — and item 2 gives literal
   > record dicts a fixture can be built from directly. The model-hedge fixture no longer
   > says `guard_kind=None`; it says what a hedge record actually looks like, which is
   > **no `guard` block at all**.
   >
   > **RE-VERIFIED AGAINST A REAL RECORD, not against the emitter — this REQ's own rule,
   > applied to its own correction.** `logs/turns_demo.jsonl` in this checkout, 2026-08-06:
   > **119 records, 9 with `guard_triggered` true, and all three kinds present** —
   > `access_control` 2, `empty_set` 5, `attr_empty_set` 2. A sample guard block is
   > `{"kind": "access_control", "subject": "maya"}`, `inference_ms` is null on it, and
   > **no record carries a top-level `guard_kind`**. That is fresh evidence, not the
   > 43-record figure this REQ recorded on 2026-08-02.
3. **Coverage entry.** Registered in `eval/harnesslib/check_registry.py` alongside the
   existing L6 record-invariant entries (`:1014`), with NAMED UNCOVERED stated — in
   particular that this REQ covers Layer 4's refusal outcomes and does **not** extend to
   Layer 1's or Layer 2's refusal assertions, which remain text-graded and are out of
   scope. Scoping that gap explicitly is part of the deliverable.
4. **Metamorphic wrapper.** The invariant that must survive rewording: **a
   meaning-preserving change to the refusal's wording must not change the pass/fail
   outcome.** That is the whole point of the REQ, and it is directly assertable — take a
   passing refusal row, substitute an equivalent refusal phrasing that the regexes do
   *not* match, and the record-graded check must still pass. Under today's text grading it
   would flip to fail, which is the metamorphic failure this change fixes.

---

## OUT OF SCOPE

Named so a build dispatch does not quietly widen.

- Layer 1 and Layer 2 refusal assertions (`layer1.py:112,227`) — still text-graded. Out of
  scope; the coverage entry must say so.
- The `value` outcome (`layer4.py:58`). Not a refusal assertion.
- Two-sided scoring / the opposite-polarity ratchet (backlog item 38, blocked on BILL-6).
  Adjacent, separately governed, **not** authorized by this REQ.
- `disclosure_oracle.py`'s wiring status (Voice 35 finding: referenced by no runner). A
  real gap; a different requirement.
- Any change to the ratchet's direction or to `gen_pairwise`'s probe generation.

## STATUS

**NOT MET.** No acceptance row has been executed. Filed Voice 37, REQ only, nothing built.
