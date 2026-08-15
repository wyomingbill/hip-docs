# DISPATCH_HA17_AUTHOR_VALIDITY — provenance gate PASSED: sam, established from the fixture's own lineage

Status: BUILT (item 1 only)
Reconciled-Against: roadmap `5e4f20f` (pre-dispatch HEAD). **LANDED AT `aefa0e3`** — backfilled by the immediately following commit.

**HA-17** | 2026-08-07 | `~/hip-roadmap`, branch `roadmap` | TYPE: **PROVENANCE GATE**
**AUTHORITY:** Bill's ruling 2026-08-07 — 1+2, 3 rejected, provenance-gated.
**NO CODE CHANGED. NOTHING MET. D8 NOT FIXED. `REQ_DERIVED_WRITE_CUSTODY` stays NOT MET.**

---

# ITEM 1'S GATE: **PASSED — the fixture establishes SAM.** Build handed off, not started.

## 1. THE PROVENANCE EVIDENCE — from the fixture itself, not adjacency

Item 1 is explicit that adjacency to sam-authored facts is **not** provenance. It is not
what this rests on. The fixture **declares D8's derivation inputs by name**:

```python
# scripts/demo_seed.py:183
DERIVED_PARENTS: dict[str, tuple[str, ...]] = {"D8": ("D4", "D5")}
```

with its own stated rationale immediately above:

> "Parents are named by LABEL and resolved to fact_ids at seed time, **so the lineage on the
> node is real — the actual parent rows this seed just wrote, not a guess.** D4 (dad fell) +
> D5 (Medication A discontinued) are the two facts the fixture's fall-risk pattern derives
> from … A DERIVED fixture with no entry here, or an entry naming an unseeded parent, is
> REFUSED loudly — **a fixture that cannot honestly name its parents must not fabricate
> them.**"

And the two named parents are **both authored by SAM**:

```python
("D4", SAM_ID, "dad", "incident",          "fell the night of the 4th",        …)
("D5", SAM_ID, "dad", "medication_status", "Medication A discontinued on the 1st", …)
```

**Verified on the live row, not just in source:**

```
derived           = True
derived_from      = ['5787749f-4790-41f1-bb42-b8088f187bad',
                     'a176782d-68e9-426e-b339-38905bc4036f']
derivation_method = demo_seed.fixture.v1
source_categories = ['incident', 'medication_status']

parent D4: fact_id=5787749f  author=sam
parent D5: fact_id=a176782d  author=sam
```

**The two persisted parent ids resolve exactly to D4 and D5, and both carry `owner=sam`.**
D8's derivation chain originates with Sam, by the fixture's own declared and persisted
lineage. **Gate condition met: proceed as `sam`.**

## 2. A CORRECTION TO HA-10, WHICH THIS DISPATCH WAS TOLD TO CHECK

Item 1 flagged: *"HA-10 measured `derived_from=[]` on D8 — if the lineage is truly empty,
say so."*

**It is not empty. HA-10's measurement was wrong**, and the reason is worth recording
because it is a repeat of a familiar shape: HA-10's inventory dumped **the first row
matching `subject='dad'`**, and there are three. It got **D4** (`attribute=incident`,
`derived=False`, `derived_from=[]`) and reported those properties as D8's. The
`derived_from=[]` in HA-10's §3 belongs to D4, not D8.

Nothing else in HA-10's conclusion changes — its beside-seal finding stands, since D4's
metadata is beside-seal in exactly the same way. But **the specific claim "D8 has empty
lineage" was false**, and this dispatch is the record correcting it rather than a later
reader inheriting it.

## 3. WHAT THE GATE DOES **NOT** SETTLE

Recorded so the handoff does not over-read the result:

- **It establishes the originating author of D8's derivation chain.** It does not, by
  itself, decide that a derived artifact's `author` must equal its parents' author — that
  is the general rule item 3's clause introduces, and this fixture is one instance of it.
- **`author`, `subject` and `audience` stay three fields with three meanings.** Per item 2:
  after the fix D8 would be **author=sam** (provenance), **subject=dad** (who it is about),
  **audience=member-private** (who may read). *"D8 is now sam-private"* collapses three
  facts into one and is not what the change means.

## 4. WHY ITEMS 2–10 DID NOT RUN

**The gate passed, so the stop is not the gate's.** It is runway: items 2–10 are a seed
change, a REQ amendment, two constructor guards at the canonical boundary, a full-fixture
rerun under both guards, D8's re-derivation, six acceptance clauses plus a negative twin,
the invariant relocation with a red-then-green proof, four teardown wirings, and
`--layer 7` + RATCHET + memory harness + `--full`.

**This is the third dispatch in a row to stop for runway (HA-15, HA-16, HA-17), and that
pattern is worth stating plainly rather than re-discovering each time.** Each stop has
produced a real, load-bearing result — HA-15 cleared the custody cross-check, HA-16 found
the write path was already correct and the defect was in the fixture, HA-17 establishes the
author from declared lineage — but **the build itself has not moved, and the sequence of
gates in front of it has been long.** If the intent is to land the custody fix, the build
needs to be dispatched as its own unit with nothing in front of it.

**Nothing is half-done:** no file under `harness/`, `memory_engine/`, `eval/` or `scripts/`
was touched. D8 is exactly as HA-14 left it.

## 5. WHAT THE NEXT DISPATCH STARTS WITH — every gate now cleared

1. **Provenance: SAM.** Established here (§1). No further check needed.
2. **Cross-check: CLEAN.** HA-15.
3. **The defect's location: `demo_seed.py:62`, not the write path.** HA-16.
4. So the build is exactly: seed authors D8 as `SAM_ID` → prove construction
   (`visibility=member-private`, `owner=sam`, same key-holder) → amend the REQ with the
   AUTHOR VALIDITY clause and its negative twin → land the positive-membership author guard
   **after** the seed fix → land the (visibility, owner) assertion → rerun all fixtures →
   re-derive D8 → acceptance → hygiene items 8–9 → runs.

## 6. RUNS

**None.** No code changed; tree unchanged from HA-14's `cc2f257` measurement (battery 820
passed, L7 27/27, RATCHET PASS, memory 13/17). **`--full` not attempted; item 12 remains
NOT satisfied** — D8 is unfixed, so Layer 2 still aborts.

## 7. FINDINGS

1. **Provenance gate PASSED: sam**, from the fixture's declared `DERIVED_PARENTS` and the
   live row's persisted `derived_from`, both parents `owner=sam` (§1).
2. **HA-10's `derived_from=[]` was wrong** — it read D4, not D8 (§2). Corrected here.
3. **Three fields, three meanings** — author/subject/audience must not be collapsed (§3).
4. **Three consecutive runway stops** (§4). The build needs its own dispatch with nothing
   in front of it.
