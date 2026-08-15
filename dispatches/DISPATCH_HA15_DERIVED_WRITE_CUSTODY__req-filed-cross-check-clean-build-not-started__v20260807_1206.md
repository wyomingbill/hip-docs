# DISPATCH_HA15_DERIVED_WRITE_CUSTODY — REQ filed, cross-check clean, build NOT started

Status: BUILT (items 1–2 only)
Reconciled-Against: roadmap `a2a19c0` (pre-dispatch HEAD). **LANDED AT `354c8e2`** — backfilled by the immediately following commit.

**HA-15** | 2026-08-07 | `~/hip-roadmap`, branch `roadmap` | TYPE: **REQ + CROSS-CHECK**
**AUTHORITY:** Bill's ruling 2026-08-07 — write-side custody is authoritative.
**NO CODE CHANGED. NOTHING MET. D8 NOT FIXED.**

---

# STOPPED BEFORE SEGMENT 3 — NEEDS BILL

**Not because item 2's gate fired — it did not. The cross-check is CLEAN.** This dispatch
stopped for a different and simpler reason, stated plainly in §3: **insufficient remaining
runway to build a custody write-path change, re-derive D8, run four acceptance clauses,
relocate the invariant, wire four batteries and run `--full`** — and a half-built change to
the sealing contract, unverified, is worse than none.

## 1. SEGMENT 1 — REQ FILED

`docs/requirements/REQ_DERIVED_WRITE_CUSTODY__write-class-determines-owner-and-seal-from-one-field__v20260807_1206.md`,
**Status: NOT MET**, Bill's rule recorded verbatim, acceptance C1–C6 written but unrun.

## 2. SEGMENT 2 — CROSS-CHECK: **NO CONFLICT**

Item 2 makes a conflict a STOP before any code. It was run clause by clause against
`REQ_PARTITION_CUSTODY__stage2-ratification__v20260721_0831.md`.

### The question, and why it looked like a conflict at first

The ratified model separates two roles that both sound like "owner":

- **OWNER** — *"SUBJECT when SUBJECT is an enrolled member with standing-policy rights …
  otherwise AUTHOR. **OWNER names whose level-1 policy applies.**"*
- **BENEFICIARY** — *"the computed key-wrap target set … **never a field an author fills
  in**."*

Bill's rule says the row's `owner` follows the sealing key. **On a first pass that reads as
collapsing the policy role onto the key role** — which would break level-1 standing-policy
lookup, the *highest* precedence rule in the ratified write order, and would be a genuine
STOP.

### What the code actually shows — the finding that settles it

It does not collapse anything, because **the separation already exists as two fields**:

```python
# harness/write_rule.py
class WriteClass:
    visibility: str    # one of the four CLASS_* constants
    owner: str         # the node's stamped `owner` property (AUTHOR, or the literal "household")
    owner_role: str|None = None   # derived policy OWNER — audit/testing
```

`WriteClass.owner` is documented **in the source** as the stamped seal/scope marker;
`owner_role` carries the ratified policy OWNER from `resolve_owner(subj, author)`. **Bill's
rule governs the `visibility`/`owner` pair and never touches `owner_role`.** Level-1 lookup
keeps its input; the mandatory subject-exclusion rule keeps its trigger (it conditions on
SUBJECT and AUTHOR, neither of which is `owner`).

The full clause-by-clause table is in the REQ §2. Seven clauses touch owner semantics;
**none conflicts.**

### One caveat recorded rather than waved past

*"the owner IS that member"* is right for MEMBER-PRIVATE, PAIR-PRIVATE and
CARE-TEAM-PRIVATE, where `WriteClass.owner` is the AUTHOR. For **HOUSEHOLD-CIRCLE-SHARED**
the stamped owner is the literal `"household"` — a scope marker, not a member. The rule has
to mean *"owner and visibility must name the same key-holder"*, not *"owner is always a
member"*, or it would forbid the household scope the ratified model requires. **Acceptance
clause C4 exists to pin that**, and it was written before any code precisely so the build
cannot quietly narrow the scope set.

### What the cross-check sharpened about D8

`store.py` stamps `owner = write_class.owner`; `consolidate.py` stamps
`audience_policy = write_class.visibility`. D8 carries `owner="household"` with
`audience_policy="member-private"` — so it came from a **`WriteClass` object that was
internally inconsistent**: its `owner` named the household key tree while its `visibility`
named a member key.

**That is a sharper statement than HA-09's.** HA-09 said the seal class and read class
disagree. This says *where*: a single class object was constructible with a
(visibility, owner) pair that names two different key-holders, and **nothing asserted
otherwise at construction.** Bill's rule is exactly that missing assertion.

## 3. WHY THE BUILD DID NOT START

Item 2's gate did not fire. **This is a runway stop, not a governance one, and it is mine
to own rather than dress up.**

Items 3–7 are: change the write-class→owner/seal contract; re-derive D8 through the
corrected path; execute four acceptance clauses including a fault twin; relocate the
zero-orphan invariant and prove it red with a deliberately stray key; wire teardown into
four more batteries; then `--layer 7`, RATCHET, memory harness and `--full`.

**Starting a change to the sealing contract and stopping partway would leave the write path
in a state no acceptance had checked** — on the one code path whose failure mode is
silently unreadable facts, which is what D8 already is. The REQ and the cross-check are
complete and independently useful; the build is a clean unit of work that should begin with
runway to finish and verify it.

**Nothing was half-done:** no file under `harness/`, `memory_engine/` or `eval/` was
touched, and D8 is exactly as HA-14 left it.

## 4. WHAT IS READY, AND IN WHAT ORDER

Nothing below needs re-deciding — the REQ pins all of it:

1. **The invariant relocation and the four teardown wirings (items 5–6) are independent of
   the custody rule** and were already named at HA-14 as the first thing to pick up. They
   touch no sealing code and could land on their own.
2. **The custody build (items 3–4)**: enforce the (visibility, owner) agreement at
   `WriteClass` construction — refuse and record on disagreement (C3) — then re-derive D8
   through the corrected path (C5), with C4 guarding the household scope.
3. **`--full` and item 12** become reachable only after C1 shows 11/11.

## 5. RUNS

**None.** No code changed, so `--layer 7`, RATCHET and the memory harness would re-measure
the tree HA-14 already measured at `cc2f257` (battery 820 passed, L7 27/27, RATCHET PASS,
memory 13/17). **`--full` not attempted: TD-R-171 is unfixed, so Layer 2 still aborts and
item 12 remains NOT satisfied** — which is the honest answer item 7 asked for, arrived at
without running it.

## 6. FINDINGS

1. **No conflict with the ratified custody model** (§2) — because `owner` and `owner_role`
   are already separate fields, a fact this dispatch verified in source rather than assumed.
2. **The household-scope caveat** (§2) — the rule needs the "same key-holder" reading, and
   C4 pins it.
3. **D8's cause is now stated at construction granularity** (§2) — an internally
   inconsistent `WriteClass`, not merely two layers disagreeing.
4. **Items 5–6 are unblocked by any of this** and can land independently (§4).
