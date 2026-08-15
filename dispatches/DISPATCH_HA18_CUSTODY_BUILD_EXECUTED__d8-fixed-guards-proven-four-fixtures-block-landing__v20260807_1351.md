STOPPED AT SEGMENT 3 — NEEDS BILL

# DISPATCH_HA18_CUSTODY_BUILD_EXECUTED — D8 fixed, guards proven, four fixtures block landing

Status: BUILT (items 1, 2, 6 complete; items 3–5 built and proven, NOT landed; item 7 not run)
Reconciled-Against: roadmap `4edb613` (pre-dispatch HEAD)

**HA-18** | 2026-08-07 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD + NEW-DEFECT STOP**
**AUTHORITY:** `REQ_DERIVED_WRITE_CUSTODY` + Bill's AUTHOR VALIDITY clause.
**REQ STATUS UNCHANGED: NOT MET** — C1 is not satisfied (§6). Ruled from evidence, not intent.

---

# THE BUILD EXPOSED A NEW CONTRADICTION — STOP, per the dispatch's own preamble

**D8 IS FIXED and its re-derived row decrypts.** But applying AUTHOR VALIDITY at the
canonical boundary **refuses four other fixtures whose provenance is undeclared**, and
`--full` cannot pass while they are refused. That is a new defect, not a reopened gate.

## 1. ITEM 1 — D8 authored as SAM, construction proven

`scripts/demo_seed.py`: D8's author `HOUSEHOLD_OWNER` → `SAM_ID`, with the reason recorded
in the fixture itself.

```
author (input)      = sam
subject (input)     = dad
visibility          = 'member-private'
owner (stamped)     = 'sam'
owner_role (policy) = 'sam'
rule                = '3c-mandatory-exclusion-narrowed'
same key-holder?    = True
```

**Three fields, three meanings — not collapsed:**

| field | value | means |
|---|---|---|
| **author** | `sam` | provenance — who signed the write |
| **subject** | `dad` | who the claim is about |
| **audience** | `member-private` | who may read it |

## 2. ITEM 5 — D8 RE-DERIVED, AND IT DECRYPTS

Re-seeded through the corrected fixture. **No hand-edit, no graph surgery.**

```
risk_pattern rows: 2
  owner=household  active=True  audience=member-private  derived_from=2 parents  FAIL InvalidToken
  owner=sam        active=True  audience=member-private  derived_from=2 parents  DECRYPTS
```

**The re-derived row, as four fields:**

| author | subject | audience | derived_from |
|---|---|---|---|
| `sam` | `dad` | `member-private` | D4 + D5 (2 parents) |

**The lineage that justified the correction SURVIVED the correction** — `derived_from` still
carries both parents, `derivation_method` still `demo_seed.fixture.v1`.

## 2A. ITEM 2 — REQ AMENDED, AND IT LANDED

`REQ_DERIVED_WRITE_CUSTODY` gains **§1A AUTHOR VALIDITY** (Bill's clause verbatim),
**acceptance C7** — the negative twin, with its proof obligation spelled out — and **§6
items 4–5**, the two new blockers below, recorded as measured rather than as opinion.

**The amendment lands even though the guards do not**, and the split is deliberate: a REQ
records what the system SHALL do, and Bill's clause is ruled whether or not today's fixtures
can satisfy it. A requirement that waits for its own code to be landable stops being the
thing the code is measured against. **C7 is written so the build cannot narrow it later** —
it demands three simultaneous absences (no ciphertext, no node, refusal recorded), because
"the exception was raised" is consistent with a write that already sealed.

## 3. ITEMS 3 + 5 — BOTH GUARDS BUILT AND PROVEN, NEITHER LANDED

Placement follows item 3's rule — **by what each can legitimately know.**

**Guard A — `WriteClass.__post_init__`, LOCAL structural invariant only.**
`owner == "household"` iff `visibility == CLASS_HOUSEHOLD`. Refused and recorded on
disagreement. **It never consults enrollment**; that is not local, and a constructor that
reached for external state would duplicate the membership check and drift from it.

```
legal member-private : sam
legal household      : household          (C4's reading: STAYS LEGAL)
  (member-private, household)        REFUSED  InconsistentWriteClass
  (household-circle-shared, sam)     REFUSED  InconsistentWriteClass
```

**Guard B — author validity at `partition_crypto.classify_write`, ONE site.** Verified as
the canonical pre-seal boundary: `store.encode`, `consolidate`, `extraction_queue._write_one`
and `seal_pair` all call it *before* `encrypt_by_class`. **Positive membership against the
enrollment registry — not a string blacklist**, so a marker nobody has thought of fails too.
Fails closed if the registry is unreadable.

```
author='sam'       : ACCEPTED -> visibility='member-private' owner='sam'
author='household' : REFUSED  -> not an authenticated enrolled principal
```

**Refusal records** go to `logs/custody/refusals.jsonl`, fsynced, and **never contain the
refused value** — a refused write is content the system declined to hold. Per item 6, the
record is permitted evidence: "rejected before persistence" forbids data side effects, not
the governed record of refusal.

**NEITHER GUARD IS COMMITTED.** Both are preserved verbatim in this session's scratchpad
(`ha18/write_rule.py`, `ha18/partition_crypto.py`) and reverted from the tree, because
landing them turns the harness red — see §4. **The working path is sacred; a guard that is
correct and a tree that is green were not simultaneously available.**

## 4. ITEM 4 — ALL FIXTURE CONSTRUCTION UNDER BOTH GUARDS

```
label author      subject   attribute           result
D1    maya        maya      appointment         OK  member-private / maya
D2    maya        maya      medication          OK  member-private / maya
D3    household   household schedule            REFUSED  InvalidAuthor
D4    sam         dad       incident            OK  member-private / sam
D5    sam         dad       medication_status   OK  member-private / sam
D6    sam         sam       preference          OK  member-private / sam
D7    household   household household           REFUSED  InvalidAuthor
D8    sam         dad       risk_pattern        OK  member-private / sam   <-- fixed
D9    maya        ray       medication          OK  pair-private / maya
D10   household   household address             REFUSED  InvalidAuthor
D11   household   household zone_district       REFUSED  InvalidAuthor

7 construct, 4 REFUSED
```

### The four, reported by name — NOT fixed, per item 4

**D3, D7, D10, D11.** All author as `HOUSEHOLD_OWNER`. **None has provenance as declared as
D8's**: D8 had `DERIVED_PARENTS = {"D8": ("D4","D5")}` naming two `SAM_ID` parents; these
four have **no lineage entry, no derivation, and no comment naming an originating author.**
They are household-attribute facts *about* the household — schedule, household, address,
zone_district — and the question "who said trash pickup is Wednesday?" has no answer in the
fixture. **A session must not pick one.**

**This is the new contradiction the preamble said to stop on**, and it is worth stating
exactly: AUTHOR VALIDITY is correct, and it reveals that **the demo fixture set contains
four facts with no author** — they were only ever writable because `"household"` was
accepted as one. The rule did not break them; it found them already broken.

## 5. WHY THE GUARDS COULD NOT LAND

With Guard B active the seed refuses D3 first and never reaches D8, so the graph cannot be
seeded, so `--layer 7` and `--full` cannot run. Landing the guards would red-line the
harness for every lane on an unruled question.

**So the seed fix landed alone** — it is independently correct, and it is the repair D8
needed — and the guards wait on the ruling for the four fixtures.

## 6. ACCEPTANCE — RULED FROM EVIDENCE

| Clause | Result |
|---|---|
| **C1** census 11/11 | **NOT MET.** 16 OK / 1 FAIL of 17. The FAIL is the **legacy** `owner=household` D8 row, still active. |
| **C2** fresh derived member-private write, consistent and readable | **MET in substance** (§2) — the re-derived row is member-private, `owner=sam`, and decrypts through the normal read path. |
| **C3** inconsistent construction refused and recorded | **PROVEN** (§3), guard not landed. |
| **C4** household-scope write still lands | **PROVEN** (§3) — `WriteClass(CLASS_HOUSEHOLD,"household")` remains legal. |
| **negative twin** (item 6) | **PROVEN** (§3) — `author="household"` refused before sealing, record written, no ciphertext, no node. |

**C1's blocker is not the write path.** The corrected seed wrote a correct new D8 but the
**legacy row was not superseded** — it has a different `owner`, so the seed treats it as a
different fact. Removing it is graph surgery, which the REQ forbids and which is a
destructive write that is not pre-authorized. **It needs a ruling, and it is small: one
legacy row, superseded or deleted.**

## 7. RUNS

**Not run.** The tree carries only the seed fix; the guards are reverted. `--layer 7`,
RATCHET and the memory harness would re-measure HA-14's `cc2f257` result plus one changed
fixture author. **`--full` NOT attempted — C1 is unmet, so Layer 2's D8 fixture check still
fails on the legacy row. Item 12 remains NOT satisfied**, and the reason has changed: it is
no longer "D8 is broken" but "the old broken D8 is still on the graph beside the fixed one."

## 8. WHAT NEEDS BILL — two small, precise rulings

1. **The four authorless fixtures (D3, D7, D10, D11).** Who authors a household-attribute
   fact? Options include a designated household steward member, or a rule that
   household-attribute facts are exempt from AUTHOR VALIDITY — the second weakens the clause
   and is named to be ruled on, not recommended.
2. **The legacy D8 row.** Supersede or delete — one row, destructive, needs your word.

**Both guards are written, proven both directions, and ready to land the moment (1) is
answered.**

## 9. FINDINGS

1. **D8 is fixed and decrypts, with its lineage intact** (§1–2).
2. **Four fixtures have no author at all** (§4) — revealed, not caused, by the rule.
3. **C1 blocked by a legacy row, not by the write path** (§6).
4. **Guards proven but unlanded** (§3, §5) — correctness and a green tree were not
   simultaneously available.
