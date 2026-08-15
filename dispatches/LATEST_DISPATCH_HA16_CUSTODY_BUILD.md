# DISPATCH_HA16_CUSTODY_BUILD — D8 is a FIXTURE defect, not a write-rule defect

Status: BUILT (diagnosis only)
Reconciled-Against: roadmap `e1ae8f0` (pre-dispatch HEAD). **LANDED AT `3796b16`** — backfilled by the immediately following commit.

**HA-16** | 2026-08-07 | `~/hip-roadmap`, branch `roadmap` | TYPE: **DIAGNOSIS + STOP**
**AUTHORITY:** `REQ_DERIVED_WRITE_CUSTODY__…__v20260807_1206.md` (cross-check CLEAN at HA-15).
**NO CODE CHANGED. NOTHING MET. D8 NOT FIXED. `REQ_DERIVED_WRITE_CUSTODY` stays NOT MET.**

---

# STOPPED AT SEGMENT 1 — NEEDS BILL

**The dispatch's premise is wrong, and correcting it is worth more than building against
it.** Item 3 says "correct the derived write path". **The derived write path is already
correct.** The inconsistent `WriteClass` comes from the *fixture*, and the fix is a
different change in a different file with a different blast radius.

## 1. WHAT WAS MEASURED (not inferred)

D8's own seed parameters, pushed through **today's** classifier:

```
classify_write(owner="household", attribute="risk_pattern", subject="dad", …)

  visibility = 'member-private'
  owner      = 'household'
  owner_role = 'household'
  rule       = '3c-mandatory-exclusion-narrowed'

  (visibility, owner) name the same key-holder?  False
```

**Reproduced live.** This is not a legacy row from old code — today's code still produces
the inconsistent pair, which is exactly what HA-15 predicted was constructible.

## 2. WHERE IT ACTUALLY COMES FROM — and it is not the write rule

`harness/write_rule.py:251`, the rule that fired:

```python
return WriteClass(CLASS_MEMBER, author, subject=subj, owner_role=policy_owner,
                  rule="3c-mandatory-exclusion-narrowed")
```

**That line is correct.** It passes `author` as the owner, which is precisely what Bill's
rule requires: *"If `write_class.visibility` is member-private, the owner IS that member."*

The inconsistency arises one level up:

```python
# scripts/demo_seed.py:62
HOUSEHOLD_OWNER = "household"
# …:131
_seed_fact("D8", HOUSEHOLD_OWNER, "dad", …)   # AUTHOR := "household"
```

**The fixture authors as the literal scope marker.** So `author == "household"`, rule 3c
correctly sets `owner = author`, and the result is
`visibility=member-private, owner="household"` — inconsistent **only because the author's
name collides with the reserved household scope string.**

The ratified model forbids this directly:

> "AUTHOR: **the authenticated identity whose device key signed the write.** Always exactly
> one; never inferred."

`"household"` is not an authenticated identity. It is the scope marker
`WriteClass.owner` uses for HOUSEHOLD-CIRCLE-SHARED. **A fixture that authors as a scope
name is malformed under the ratified model**, and D8 is the fact it produced.

## 3. WHY THIS CHANGES THE BUILD, RATHER THAN JUST EXPLAINING IT

| The dispatch assumed | Measured |
|---|---|
| item 3: "correct the derived write path (`store.py` write-class → owner/seal contract)" | The write path already assigns `owner = write_class.owner`, and `write_rule.py` already sets `owner = author` for member-private. **Nothing in that contract is wrong.** |
| item 2: re-derive D8 through "the corrected path" | Re-deriving through today's path reproduces **the same inconsistent pair** — because the malformed input is unchanged. **Re-derivation alone cannot fix D8.** |

**Item 1's constructor assertion is still exactly right** — it would have refused this
`WriteClass` at construction, which is the whole point of Bill's rule. But it would then
**fail the demo seed** rather than fix it, because the seed's own author is the thing that
violates the invariant.

So the build is two changes, not one, and the second is the one nobody has ruled on.

## 4. THE QUESTION FOR BILL

**What is D8's author supposed to be?**

The seed writes five facts as `HOUSEHOLD_OWNER` (D3, D7, D8 and others). For D3/D7 —
household-attribute facts about the household — `visibility` lands household-circle-shared
and `owner="household"` is consistent and correct. **Only D8 narrows**, because its SUBJECT
is `dad` and `risk_pattern` is not in the coordination enum, so rule 3c fires.

Three candidate answers, none of which a session should pick:

1. **The seed should author D8 as a real member** (`sam`, the author of the neighbouring
   `dad` facts). Then 3c narrows to `owner="sam"`, consistent, and D8 becomes a
   member-private derived fact about dad — which may or may not be the demo's intent.
2. **`"household"` should be rejected as an author** at the write boundary, making the
   malformed fixture fail loudly. Correct by the ratified model, and it will break the seed
   until (1) is decided.
3. **Rule 3c should not narrow a household-authored fact** — but that would weaken the
   mandatory subject-exclusion rule, which the ratified model calls "a HARD,
   non-overridable constraint". **This one looks wrong and is listed to be ruled out
   explicitly, not because it is attractive.**

**Answer 1 changes what the demo shows. Answer 2 changes what the system accepts.** Either
is a ruling, and the REQ's acceptance C2/C4 were written before this was known.

## 5. WHAT WAS NOT DONE, AND WHY

**No code changed.** Not the constructor assertion (it would fail the seed before anything
was decided), not the seed, not `store.py`, not the invariant relocation (item 4), not the
four teardown wirings (item 5).

Items 4 and 5 are genuinely independent of this question — **they were carried from HA-14
and remain unblocked** — but landing them inside a dispatch that stopped at segment 1 would
mix an unruled custody question with unrelated test hygiene in one commit. They stay queued.

## 6. RUNS

**None.** No code changed; the tree is `e1ae8f0`, last measured at HA-14's `cc2f257`
(battery 820 passed, L7 27/27, RATCHET PASS, memory 13/17).

**`--full` not attempted. Item 12 remains NOT satisfied** — D8 is unfixed, so Layer 2 still
aborts. That is the honest answer item 6 asked for, and it is unchanged because this
dispatch deliberately changed nothing.

## 7. FINDINGS

1. **D8 is a fixture defect, not a write-rule defect** (§2). `write_rule.py:251` is correct;
   `demo_seed.py:62` authors as a reserved scope marker.
2. **Re-derivation alone cannot fix D8** (§3) — the malformed input is unchanged, so the
   same pair comes back.
3. **The constructor assertion is still right, and would have caught this** — but it fails
   the seed rather than repairing it, so it cannot land before §4 is ruled.
4. **`REQ_DERIVED_WRITE_CUSTODY`'s C2 and C4 were written before this was known** and may
   need a clause about what a valid AUTHOR is. Flagged, not edited.
5. **Items 4–5 remain unblocked and queued** (§5).
