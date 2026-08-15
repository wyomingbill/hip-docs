# DISPATCH_GRADED_REFUSAL_THREE_GUARD_KINDS — the REQ corrected against the system, not the reverse

Status: BUILT
Reconciled-Against: roadmap `1965fa9` (pre-amendment HEAD). **LANDED AT `8370631`** — backfilled by the immediately following commit, because a commit cannot contain its own hash.

**HA-04** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **DOCS ONLY — REQ amendment**
**REQ AMENDED:** `docs/requirements/REQ_RECORD_GRADED_REFUSAL__refusal-checks-assert-on-the-execution-record__v20260802_0744.md`
**NO CODE CHANGED. NOTHING MARKED MET.**

---

## BILL'S RULING, VERBATIM

> "Ruling: state 3 keys on guard_triggered === true. The REQ's access_control-only key was
> the REQ being wrong about the system — INJ-6b's own comment is the authority. Amend the
> REQ citing this dispatch; the correction is recorded, not silent."

## 1. WHAT WAS AMENDED, AND WHERE

`REQ_RECORD_GRADED_REFUSAL` §6 item 2 — REQ_HARNESS_DISCIPLINE's **ground-truth fixture**
clause. It read:

> *"(a) structural refusal — `guard_kind="access_control"`, `inference_ms=None`"*

It now requires **three fixtures, one per guard kind** — `access_control`, `empty_set`,
`attr_empty_set` — each with `inference_ms=None`. Clauses (b) and (c) are untouched.

**Amended IN PLACE, not cut as a new version**, matching this REQ's own established
pattern: it already carries a "CORRECTED IN PLACE 2026-08-02" annotation for an earlier
error, with the superseded wording preserved. The prior wording is preserved verbatim
inside the new annotation, and the header records the amendment so a reader meets it before
§6. **2 lines removed, 49 added** — the Status line and the one fixture line.

## 2. WHY THE REQ WAS WRONG ABOUT THE SYSTEM — verified in code, not argued

Three guard kinds are emitted by shipped code:

| Kind | Emitted at | Guard |
|---|---|---|
| `access_control` | `harness/realtime_adapter.py:369,428`, `server/voice_orch.py:3162`, `server/demo_dashboard.py:3009` | INJ-7 (`path=guard_inj7`) |
| `empty_set` | `harness/injection_contract.py:806` | INJ-6 |
| `attr_empty_set` | `harness/injection_contract.py:849` | **INJ-6b** |

**INJ-6b's own comment is the authority Bill names**, and it says the thing the REQ's
fixture denied:

> "INJ-6b: attribute-targeted empty-set guard (Seam B). A personal QUESTION naming a
> precisely-keyworded attribute must refuse **STRUCTURALLY** when no admitted fact carries
> that attribute — unrelated admitted facts (household schedule etc.) must not keep the
> model in the loop to fabricate an answer."

A fixture keyed on `access_control` alone describes **one of the three** structural
refusals this REQ exists to grade. A predicate built from it rejects genuine structural
refusals as though they were model hedges — **which is the exact conflation the REQ was
written to end.** The REQ was wrong about the system; the system was right.

## 3. THE REQ ALREADY CONTRADICTED ITSELF

This is not new information arriving from outside the document. `REQ_RECORD_GRADED_REFUSAL`'s
own WHAT'S ALREADY DONE section, verified against **43 live records**, states:

> "And there are THREE guard kinds, not the two the parameter comment names:
> `access_control` (20), `empty_set` (2), **`attr_empty_set` (2)** — the last is INJ-6b's
> attribute-targeted guard and is every bit as structural an empty-set refusal. A predicate
> accepting only `empty_set` rejects genuine refusals."

So §6 item 2 contradicted the REQ's own authoritative evidence section, written from live
records. **The amendment removes a self-contradiction in the direction both the evidence
and the code point** — which is why it is a correction rather than a change of policy.

## 4. FLAGGED AND DELIBERATELY NOT FIXED — a second inconsistency in the same clause

§6 still writes the field as **`guard_kind`**, while this REQ's own verified table records:

> `guard_kind` | **NOT EMITTED — 0 of 43 records carry it** | it is the parameter at `:184`;
> the emitter builds the nested block at `:255` and writes it at `:288`

The kind lives NESTED at **`guard.kind`**. **That is the identical defect class this REQ
already corrected once** — a PARAMETER name mistaken for an emitted key — and its own
annotation records what that cost: "a full red Layer-4 run — 13 rows failing for a wrong-field
lookup that looked exactly like a genuine finding — plus unit fixtures that were green
against a record shape that does not exist, which is the worse half."

**Not fixed here.** Bill's ruling is about the three kinds; changing the field name touches
acceptance wording beyond it. **Consequence, stated so nobody is surprised: a fixture built
from §6 as it stands today will still use a key the record does not carry.** Flagged in the
REQ itself, at the point of use, not only here.

## 5. WHAT WAS NOT DONE

- **No code changed.** The three kinds were already emitted correctly; the defect was
  entirely in the REQ's own text.
- **`Status: NOT MET` is unchanged.** Nothing was marked MET, no acceptance row re-tiered.
- **No harness runs.** Docs-only, no code touched, and the dispatch asked for none. Stated
  rather than left as an absence.
- **§6's `guard_kind` field name** — §4.
- **Nothing else in the REQ was edited**, and the earlier 2026-08-02 in-place correction was
  left exactly as it stands.

## 6. FINDING

**One dispatch-shaped observation, recorded because it is the second time this REQ has been
wrong in the same way.** Both errors in `REQ_RECORD_GRADED_REFUSAL` came from writing an
acceptance clause against **the emitter's signature** instead of a real record: the first
mistook the `guard_kind` parameter for an emitted key, and this one took the parameter
comment's two-value vocabulary (`access_control | empty_set`) as complete when the code
emits three. The REQ states the lesson itself — *"build fixtures from a REAL RECORD, never
from the emitter's signature"* — in the section that sits four pages above the clause that
just violated it.
