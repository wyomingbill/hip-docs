# RULING_KeyLifecycle — three rulings on custody, backup and the erasure claim

Status: BANKED
**THIS IS BILL'S RULING, 2026-08-06, AUTHORITATIVE.**
Source: pasted into HA-13 by Bill via advisor chat

**This document is NOT a review.** It sits in `docs/reviews/` beside
`CHATGPT_KeyLifecycle__custody-destruction-rotation__v20260806.md` because that is where
Bill ruled the pair should live (Ruling 1 below), but the two carry opposite authority:

| Document | Authority |
|---|---|
| `CHATGPT_KeyLifecycle__…` | one external model's opinion. **UNVERIFIED.** Binding on nothing. |
| **this file** | **Bill's ruling. Authoritative. Binding.** |

A reader who confuses them will treat an opinion as a decision or a decision as an opinion.
The banked review's own header carries the matching warning.

**What this ruling authorizes, enacted by HA-13:** Ruling 2's backup exclusions (§3 of
HA-13's dispatch doc), the separate audit-text defect as a TD, and the erasure-enablement
gate written into `docs/HIP_HANDOFF.md`. HA-11 explicitly refused to run those exclusions
because the authority for them could not be read; **this document is that authority.**

**Everything below this line is Bill's text, byte-for-byte as pasted.**

---

## Rulings

### 1. Review artifact location

**Ruled: `docs/reviews/`.**

Re-save the review file to `~/Downloads` under the exact filename HA-10 expects, then re-fire segment 1 and bank it into `docs/reviews/`.

Do **not** create `docs/research/`. The session correctly stopped rather than inventing repository structure.

Also preserve the failed attempt in the dispatch record: missing source file + incorrect destination in the dispatch. Don't make the successful rerun erase evidence that the first instruction was wrong.

---

### 2. Backup policy

**Ruled: exclude every current key-material path from automatic backup immediately, then consolidate production custody to one managed location.**

The important distinction is:

> **No backup configured today is not a backup policy.**

You currently have accidental safety only because Time Machine has not been enabled. With ~2,800 key-bearing files across eight-plus paths, including dated backup directories, enabling ordinary backup would silently multiply erasure targets.

I would require this sequence:

1. Inventory the current key-bearing paths and preserve the inventory as evidence.
2. Explicitly exclude **all of them** from Time Machine before any backup destination is configured.
3. Consolidate production keys into one canonical custody location.
4. Remove legacy copies only through a separately evidenced migration/cleanup operation.
5. Make tests structurally unable to write into the production location.
6. After consolidation, maintain one explicit backup exclusion rather than eight-plus fragile ones.
7. Treat any future key backup/export as a distinct governed operation.

### Availability ruling

Do **not** solve availability by quietly putting the active key store back into Time Machine.

If recovery is required, build a deliberate key-recovery mechanism with its own policy. An encrypted export can be reasonable, but then it becomes an additional controlled key copy and therefore an additional erasure target.

That means the product eventually has to choose explicitly between:

* **stronger erasure:** no recoverable backup of the subject key; disk loss can destroy access permanently;
* **recoverability:** protected backup exists, and erasure is not complete until the corresponding recovery copy is also destroyed.

There is no architecture that gives you both perfect recoverability and "destroy this one key here and it is definitely gone everywhere."

For this phase: **prefer erasure integrity over availability and leave deliberate key backup out of scope until its custody model exists.**

---

### 3. Erasure claim and surviving metadata

**Ruled: build the metadata-scrub cascade. Do not normalize the current behavior into the permanent erasure definition.**

Your current implementation can honestly be described as:

> **Primary-record value erasure.**

It cannot honestly be called subject erasure while readable metadata still reveals:

* subject;
* attribute;
* representation class;
* sensitivity;
* author;
* timestamps.

For an eldercare system, this residue is not trivial bookkeeping.

After "erase Dad," retaining:

> Dad + `health_condition` + HIGH + authored by Sam + date

is still meaningful personal information. Depending on attribute vocabulary, the metadata can reveal almost as much as the encrypted value.

### The permanent invariant should be

For a successful subject erasure:

```text
No ordinary read path may reveal that an erased subject had
a particular fact, attribute, representation class, sensitivity,
author relationship, or fact timestamp.
```

That requires a cascade over the beside-seal graph metadata.

### But don't destroy your tamper-evidence

Keep the distinction you've already established elsewhere:

The audit layer may preserve an **opaque erasure event**, for example:

```text
event_type: SUBJECT_ERASURE_COMPLETED
opaque_subject_ref: <non-reversible governed identifier>
timestamp
policy_version
operation_result
```

It must not preserve enough information to reconstruct:

```text
Dad had a HIGH health_condition authored by Sam.
```

So:

> **Erase semantic metadata; retain opaque operational proof.**

---

## Raw query audit log

**Separate defect. Fix it regardless of the metadata cascade.**

Full recall query text should not be sitting in plaintext audit telemetry.

The audit system needs to prove things like:

* a recall occurred;
* which policy version governed it;
* which principal requested it;
* decision outcome;
* perhaps a non-reversible request/event commitment where necessary.

It generally does **not** need the complete natural-language query forever.

This should become its own requirement/TD if it isn't already one. Do not bury it as incidental work under graph-node erasure.

---

## Demo fixtures

Committed synthetic fixture values are a different class.

If they are genuinely synthetic and clearly incapable of being confused with production household information, they are not an erasure defect.

But they must remain structurally separated from production data and keys. Don't let the presence of fixture strings in source contaminate the erasure acceptance test.

The session catching and retracting its bogus 711-hit grep result is good evidence behavior. Put that correction in the report rather than merely reporting the final zero.

---

## One additional ruling I would add

The metadata cascade needs **an acceptance definition broader than database deletion**.

After erasure, search for the erased subject across:

* graph properties;
* embeddings/index metadata;
* summaries;
* recall/audit telemetry;
* caches;
* derived objects;
* export artifacts;
* active filesystem key custody.

The test should distinguish three outcomes:

```text
ERASED
    semantic subject information no longer recoverable
    through HIP-managed stores

OPAQUE_PROOF_REMAINS
    erasure/audit evidence exists but reveals no erased semantics

OUTSIDE_ERASURE_BOUNDARY
    explicitly identified artifacts such as synthetic committed fixtures
```

If anything lands in a fourth implicit bucket—"we forgot about that store"—the erasure operation fails acceptance.

---

## Final rulings

**1.** `docs/reviews/`; correct the filename/location and re-fire banking.

**2.** Exclude all current key paths from automatic backup now; consolidate to one production custody location; any recovery copy later requires an explicit governed design.

**3.** Build the metadata-scrub cascade. Current behavior is only primary-record value erasure. Also remove raw recall query text from durable audit logging as a separate defect.

And I would not enable real-data erasure until **both the key-custody cleanup and the semantic-metadata cascade have landed**. Otherwise the UI is offering an erasure action stronger than the system can presently deliver.
