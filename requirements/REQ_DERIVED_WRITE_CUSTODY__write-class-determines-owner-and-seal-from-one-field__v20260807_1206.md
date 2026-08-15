# REQ_DERIVED_WRITE_CUSTODY — the write class determines owner and seal from one field

Status: **MET — Bill's ruling, 2026-08-07, recorded at HA-20.**

> Ruled on HA-19's acceptance table (that dispatch's §9): C1 census **11/11** on a
> from-scratch seed under both guards; C2 a fresh derived member-private write consistent
> and readable; C3 inconsistent construction refused **and recorded**; C4 the household
> scope still lands; C7's negative twin proven **by absence** — no ciphertext, no node, no
> derived child, refusal recorded, and `encrypt_by_class` never reached.

**AND THE RULE-3a FIX IS RATIFIED, in Bill's words:** *"Scope follows the subject, not the
author. Keep the fix."* HA-19 flagged that change as its one judgement call and offered to
revert it; **it is now ratified, not merely tolerated** — see §"ONE THING THE FIX REQUIRED"
below, which stands as the record of why it was needed.

Filed HA-15, 2026-08-07; **AMENDED HA-18** (§1A AUTHOR VALIDITY, acceptance C7, §6 items
4–5); **EXECUTED HA-19** — both guards live, §6 items 4–5 resolved; **RULED MET HA-20.**
Reconciled-Against: roadmap `a2a19c0`; amendments `4edb613`; execution `eac8dfb`; ruling
recorded at `7b776b3`

> **Prior status line, preserved per the annotate-never-silently-patch rule:** *"NOT MET —
> but every acceptance clause has now EXECUTED AND PASSED (HA-19). READY FOR BILL'S RULING;
> a session reports readiness and does not rule MET."* That remained correct until Bill
> ruled; **§6 items 6–7 below are still open and are NOT covered by this ruling.**
Decision-Owner: Bill
Authority: Bill's ruling 2026-08-07 — **write-side custody is authoritative.**
Related: `REQ_PARTITION_CUSTODY__stage2-ratification__v20260721_0831.md` (the ratified
four-scope model and role separation), `REQ_CRYPTO_P2_PARTITION_SEALED`, **TD-R-171** (the
D8 defect this REQ exists to make impossible).

## 1. THE REQUIREMENT — Bill's words, verbatim

> "At write time, the computed write class determines BOTH the sealing key and the row's
> owner, from the same field. If `write_class.visibility` is member-private, the owner IS
> that member and the DEK seals to that member's key. No fact may exist whose
> `audience_policy` and `owner` disagree on which key holds it. The read path keeps
> dispatching on owner and needs no knowledge of this rule."

## 1A. AUTHOR VALIDITY — Bill's words, verbatim (added HA-18, 2026-08-07)

> "Every durable claim SHALL name an authenticated enrolled principal as its author.
> `author` expresses provenance identity and SHALL NOT contain an audience, scope,
> partition, custody, or routing marker. A write with an invalid author SHALL fail before
> sealing or persistence."

**Why this clause is part of THIS requirement and not a separate one.** §1's rule is an
invariant on the (`visibility`, `owner`) pair. HA-16 established that D8's inconsistent pair
was produced by a *valid application of a correct rule to a malformed input*: the fixture
authored as the literal string `"household"`, rule 3c set `owner = author`, and the result
named the household key tree while the visibility named a member key. **§1 makes the bad
pair unconstructible; §1A makes the input that produced it unwritable.** Without §1A, §1
converts a silent unreadable fact into a loud refusal — better, but it still refuses a write
the system should never have been asked to make.

### What follows from the clause, stated so the build cannot narrow it

- **`author` is checked by POSITIVE MEMBERSHIP against the enrollment registry, never by
  blacklisting known-bad strings.** A blacklist admits every scope marker nobody has thought
  of yet; positive membership refuses all of them by construction. `"household"` fails
  because it is not enrolled, not because it is on a list.
- **The check fails CLOSED.** An unreadable or empty registry refuses the write. A custody
  check that passes when it cannot see its own inputs is not a check.
- **"Before sealing or persistence" means the check sits at the canonical pre-seal boundary,
  at ONE site** — `partition_crypto.classify_write`, which every producer
  (`store.encode`, `consolidate`, `extraction_queue._write_one`, `seal_pair`) calls before
  `encrypt_by_class`. Duplicating it into callers would create sites that drift.
- **This is not the (`visibility`, `owner`) assertion, and the two do not belong at the same
  site.** The structural assertion is LOCAL to `WriteClass` and consults nothing external;
  the author check requires enrollment state. A constructor that reached for the registry
  would duplicate this check and drift from it.

## 2. CROSS-CHECK AGAINST THE RATIFIED PARTITION-CUSTODY DECISIONS — **NO CONFLICT**

Item 2 makes a conflict a STOP. The check was run clause by clause wherever the ratified
model touches owner semantics. **The result is no conflict, and the reason is load-bearing
enough to state precisely rather than assert.**

### The clause that decides it

`REQ_PARTITION_CUSTODY` §Role separation defines **OWNER** as a *policy* role:

> "OWNER (derived, not author-filled): SUBJECT when SUBJECT is an enrolled member with
> standing-policy rights … otherwise AUTHOR. **OWNER names whose level-1 policy applies.**"

and **BENEFICIARY** as the *key* role:

> "BENEFICIARY: not an input. It is the computed key-wrap target set … never a field an
> author fills in."

**A rule that made the row's `owner` the key-holder would collapse those two — unless the
policy role already lives somewhere else. IT DOES**, and this codebase already implements
the separation:

```python
# harness/write_rule.py
class WriteClass:
    visibility: str    # one of the four CLASS_* constants
    owner: str         # the node's stamped `owner` property (AUTHOR, or the literal "household")
    owner_role: str|None = None   # derived policy OWNER — audit/testing
```

`WriteClass.owner` is documented, in the source, as **the stamped seal/scope marker**;
`WriteClass.owner_role` carries the ratified policy OWNER, set from
`resolve_owner(subj, author)`. **Bill's rule governs the `visibility`/`owner` pair and does
not touch `owner_role`.** So the ratified level-1 lookup keeps its input and the mandatory
subject-exclusion rule keeps its trigger.

### Clause-by-clause

| Ratified clause | Touches owner semantics? | Conflict? |
|---|---|---|
| Four scopes; "scope decides which keys can unwrap its DEK" | yes — scope→key | **No.** This rule says the same thing and adds that the stamped `owner` must agree with it. |
| MEMBER-PRIVATE = "the authoring member only. DEK sealed to that member's keypair alone" | yes | **No.** Bill's rule restates it and forbids the row disagreeing. |
| Level 1 "OWNER'S STANDING POLICY" | yes — but on `owner_role` | **No.** Untouched; `owner_role` is a separate field. |
| BENEFICIARY "never a field an author fills in" | yes — key-wrap target | **No.** The rule makes `owner` a *function of the computed class*, which is the opposite of author-declared. |
| Mandatory subject-exclusion (SUBJECT != AUTHOR …) | conditions on SUBJECT/AUTHOR | **No.** Neither is `owner`. |
| Roster invariant; SUBJECT_VISIBILITY wrap omission | key-wrap construction | **No.** Below this rule, unchanged. |
| Uncertainty rule / fail-private | scope selection | **No.** Selects the class; this rule only enforces internal consistency of whatever class is selected. |

**One caveat recorded, not waved past:** the rule's phrase *"the owner IS that member"* is
correct for MEMBER-PRIVATE, PAIR-PRIVATE and CARE-TEAM-PRIVATE, where `WriteClass.owner` is
the AUTHOR. For **HOUSEHOLD-CIRCLE-SHARED** the stamped owner is the literal string
`"household"`, which is a scope marker and not a member at all. The rule must therefore be
read as *"owner and visibility must name the same key-holder"*, not as *"owner is always a
member"* — otherwise it would forbid the household scope the ratified model requires.
Acceptance clause (d) exists to pin exactly that.

## 3. WHAT THE RULE MAKES IMPOSSIBLE — and what D8 is

D8 (`TD-R-171`) is on the graph right now:

```
owner = "household"   subject = "dad"   derived = True   audience_policy = "member-private"
```

`memory_engine/store.py` stamps `owner = write_class.owner`; `audience_policy` is stamped
from `write_class.visibility`. So D8 came from a `WriteClass` whose `owner` said *household
key tree* while its `visibility` said *member key* — **an internally inconsistent class
object**, which is why `decrypt_fact_value_for_caller` (dispatching on `owner`) hands a
member-sealed DEK to the household unwrap path and raises `InvalidToken`.

**This REQ's rule is precisely the invariant whose absence allowed that object to exist.**

## 4. THE ACCEPTANCE TEST

| ID | Clause |
|---|---|
| C1 | **Decrypt census 11/11** — D8 opens. Run before and after; the 10 that already opened still open. |
| C2 | A fresh **derived member-private** write lands `owner = <that member>` and decrypts through the normal read path. |
| C3 | **Fault twin, executed:** a write attempting `owner`/`visibility` disagreement is **REFUSED** and the refusal recorded. |
| C4 | **Anti-vacuity:** a derived **household-visible** write still lands `owner = "household"` — the rule must not collapse the household scope (§2's caveat). |
| C5 | D8 is fixed **by re-derivation through the corrected path** — no hand-edit, no graph surgery. The path that wrote the mismatch writes the correction. |
| C6 | `--layer 7` + RATCHET + memory harness unchanged; `--full` attempted and item 12's status reported honestly. |
| **C7** | **§1A's NEGATIVE TWIN, executed:** a write whose `author` is a scope/audience marker rather than an enrolled principal is **REFUSED BEFORE SEALING** — proven by three simultaneous absences, not by catching the exception: **no ciphertext produced, no node persisted, and the refusal recorded.** Added HA-18. |

**C7's proof obligation, stated precisely because "it raised" is not the claim.** An
exception reaching the caller is consistent with a write that already sealed and persisted.
The twin passes only if, after the refusal, the graph has no new node for that write and no
DEK was produced. **The refusal RECORD is a permitted side effect and not a violation of
"before persistence"** — that clause forbids persisting the *claim*, and a governed record
that a claim was refused is the opposite of persisting it. **The record SHALL NOT contain
the refused value:** refused content is content the system declined to hold, and writing it
into a log would persist by the back door exactly what the front door refused.

**Tier: ABSOLUTE for C1–C4.** A fact whose owner and audience disagree is unreadable by the
system that wrote it — the failure mode is silent data loss.

## 5. WHAT'S ALREADY DONE — do not redo

- **The two-field separation already exists** (§2). This REQ does not introduce
  `owner_role`, and must not disturb it.
- **`store.py` already assigns `owner = write_class.owner`.** The gap is that nothing
  asserts the class was internally consistent before it was used.
- **The read path already dispatches on `owner`** and, per Bill's rule, needs no change.
- **HA-09 already diagnosed D8** — seal class vs read class. Not re-derived here.

## 6. WHAT'S KNOWN BROKEN

1. **D8 is live and unreadable** (TD-R-171). `--full` aborts at Layer 2 on it, so
   Requirements Discipline **item 12 is unsatisfiable for every dispatch** until it clears.
2. **No invariant guards `WriteClass` construction today** — the inconsistent object was
   constructible, and nothing said so.
3. **Whether other rows share D8's shape is unmeasured.** Only D8 fails the census, but
   "only one row fails today" is not "only one row was written wrong."

### Measured at HA-18 — two new blockers, both needing a ruling

4. **FOUR FIXTURES HAVE NO VALID AUTHOR: D3, D7, D10, D11.** All author as the literal
   `"household"`, and all are refused by §1A. **This is a pre-existing defect the clause
   revealed, not one it caused** — they were writable only because the scope marker was
   accepted as a principal. Unlike D8, **none has declared provenance**: no `DERIVED_PARENTS`
   entry, no derivation, no comment naming an originating author. They are household-
   attribute facts (schedule, household, address, zone_district) whose author is genuinely
   unknown, and **a session must not invent one.** Needs Bill.
5. **D8's LEGACY ROW IS STILL ACTIVE BESIDE THE CORRECTED ONE.** Re-seeding with
   `author=sam` wrote a correct new row that decrypts, but the old `owner="household"` row
   was not superseded — the seed treats a different `owner` as a different fact. **C1 is
   therefore 16 OK / 1 FAIL of 17, and the FAIL is the legacy row, not the write path.**
   Clearing it is graph surgery, which §7 forbids and which is a destructive write outside
   the pre-authorized classes. Needs Bill.

**Consequence for §1A's landing:** the author guard cannot land while (4) stands, because
the seed refuses D3 before it reaches D8, so the graph cannot be seeded and `--full` cannot
run. The guard is built and proven both directions (HA-18 §3); it waits on the ruling.

### RESOLVED AT HA-19, 2026-08-07 — items 4 and 5 are CLOSED

Bill ruled on both. **Item 4:** `DEMO_ONBOARDING_AUTHOR = SAM_ID` — Sam set up the household
and entered its onboarding facts; D3/D7/D10/D11 all derive their author from that one
constant. **Item 5:** the legacy D8 row was **superseded by exact row identity, not
deleted**, its malformed author and custody state left intact as the history the
supersession records as corrected. Both guards are live and every acceptance clause passes.

### ONE THING THE FIX REQUIRED THAT THIS REQ DID NOT ANTICIPATE — **RATIFIED (Bill, HA-20)**

> **"Scope follows the subject, not the author. Keep the fix."** — Bill, 2026-08-07.
>
> HA-19 raised this as its one judgement call, on the grounds that Bill's own instruction
> held two halves that contradicted each other in code ("subject and audience rules
> unchanged" AND "these remain household facts"). **The outcome reading was correct and the
> principle is now stated in his words rather than inferred from an outcome.**

Correcting the four authors **silently reclassified D3, D10 and D11 from
household-circle-shared to member-private.** `harness/write_rule.py` rule 3a triggered on
`author == "household"` — **the classifier itself derived SCOPE FROM AUTHOR**, which is the
conflation §1A forbids, and it was the only route by which those three reached household
scope. Rule 3a now also triggers on `subj == "household"` — strictly additive, nine fault
twins, full reasoning in HA-19 §3–4. **Recorded here because it changes an access-scope rule
and this REQ is where a reader will look for that.**

### WRITE-STATE VALIDITY — Bill's ruling 2026-08-10 (HA-33)

> **A write with an unrecognized write_state SHALL be refused before sealing or persistence.**

The refusal is **raised, never returned**, and is recorded through the same custody-refusal path
`_assert_valid_author` already uses for `InvalidAuthor` — same REQ citation, same
"refused before sealing or persistence; the refusal has been recorded" guarantee. Because the
check sits beside the author check and ahead of every seal, key operation and graph write, the
absence of side effects is **structural**: no fact, no node, no ciphertext, no seal, no key
operation, no derivative, and no false success result.

**This clause closes KNOWN BROKEN item 6 below**, which is retained as the record of the defect
and of how long it stood. The canonical states are `supersede`, `augment`, `correct`,
`unresolved`, named once in `memory_engine/store._KNOWN_WRITE_STATES` so the guard and the
lifecycle block cannot drift apart.

### KNOWN BROKEN, STILL — found at HA-19, out of its scope

6. **`encode()` accepts an unrecognized `write_state`, performs NO graph write, and still
   emits a success audit record and a fresh `fact_id`.** The lifecycle block handles
   `supersede`/`augment`/`correct`/`unresolved` with no `else`. **Same silent-loss class as
   TD-R-171, by a different route.** Not filed as a TD — production-code TDs are not on the
   pre-authorized list.
7. **No `author` property is persisted on the Fact node.** §1A makes provenance meaningful
   at write time; the row does not carry it afterwards, so "who authored this?" is enforced
   and then unanswerable.

## 7. CONSTRAINTS

- **`owner_role` is not touched.** Collapsing it would break ratified level-1 policy lookup.
- **The read path is not changed** — Bill's rule says so explicitly.
- **The household scope survives** (§2 caveat, C4).
- **D8 is fixed by re-derivation only.** No hand-edit, no Cypher surgery.
- **Nothing marked MET without acceptance evidence in the dispatch doc.**
