# DISPATCH_FM26 — 7690 forensics: **FM 24's finding was a FALSE ALARM. The data is intact.**
Status: BUILT
Reconciled-Against: `~/hip-cutover-demo` @ `demo-cutover-build`; live read-only graph access 2026-08-14 22:05 MDT

COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING

**STRICTLY READ-ONLY throughout, under Bill's forensic hold. 7690 received no re-seed, re-key,
reset, consolidation, cleanup, migration, or mutation of any kind.** Every query was
`MATCH`/`RETURN`. No key material appears here.

---

# THE ANSWER, FIRST

## **S2 — DID-DECRYPT. And the rows were never orphaned.**

**All 13 of 7690's encrypted rows decrypt successfully, right now, through the demo's own read
path.**

```
=== decrypting all 13 7690 rows through the V2 caller path (READ-ONLY) ===
  household  household        -> DECRYPTED (25 chars)      maya  appointment       -> DECRYPTED (41)
  household  risk_pattern     -> DECRYPTED (26 chars)      maya  medication        -> DECRYPTED (29)
  household  address          -> DECRYPTED (30 chars)      household schedule      -> DECRYPTED (26)
  household  zone_district    -> DECRYPTED (6 chars)       sam   incident          -> DECRYPTED (25)
  household  zone_district    -> DECRYPTED (1962 chars)    sam   medication_status -> DECRYPTED (36)
  maya       medication       -> DECRYPTED (14 chars)      sam   preference        -> DECRYPTED (21)
  maya       medication       -> DECRYPTED (27 chars)

  DECRYPTED 13/13   FAILED 0
```

**The demo path is the same path.** `server/demo_dashboard.py:734-735` and `:1099/:1135` call
`harness.partition_crypto.decrypt_fact_value_for_caller` — exactly what the probe above used.
**So this is consumer-path evidence, not inference from a green battery**, which is what ruling 3
required.

## MY FM 24 FINDING WAS WRONG. HERE IS EXACTLY HOW.

**FM 24 reported that 7690's DEKs "open with neither master key on disk", implying 26 stranded
envelopes on the cutover lane's canonical graph. That is false, and it is my error alone.**

**The cause:** 7690's rows carry **`key_version = 2`**. Version 2 is a **different envelope scheme
entirely** — `harness/partition_crypto.py`, in which household-shared, dyad, and care-team facts are
sealed under keys from `~/hip-keys/*.seal.key`, **not** under an HKDF derivation of `.master_key`.
**I unwrapped v2 envelopes using the v1 primitive** (`_derive_key(owner)` + `Fernet`). They could
never have opened. The failure was in my test, not in the data.

**Why the error survived my own checks, which is the part worth recording:** I tested *exhaustively
in the wrong dimension.* I ran all 13 rows × all 3 owners × both master domains and reported "zero
unwrap", and I explicitly "ruled out the innocent explanation" by verifying `_HKDF_INFO_PREFIX` was
byte-identical across five trees. **All of that was rigorous and all of it was inside a false frame.**
**I never checked `key_version` on those rows** — the one field that says which scheme applies — and
I never looked for a v2 code path. **Exhaustiveness within a wrong frame reads exactly like rigor
and is not.**

**Two signals I had and did not follow:** FM 21 recorded `key_version` as the basis for staged
rotation *and* recorded 1,148 `~/hip-keys/*.seal.key` files — the v2 key material — and I treated
them as unrelated. FM 24's own snapshot would have shown `key_version = 2` had I printed it.

**Nothing was lost, nothing needs recovery, and no fourth master key is missing.**

---

# S1 — THE FORENSIC SNAPSHOT (banked)

Captured read-only and banked at `/tmp/fm26_7690_snapshot.json` (sha256 `f00f1681f2f70268`).
**13 encrypted rows, 13 nodes total, single label `Fact`.**

| owner | attribute | key_version | recorded_at | ct len | dek len | utterance envelope |
|---|---|---|---|---|---|---|
| household | household | **2** | 2025-07-05 | 120 | 232 | yes |
| household | schedule | **2** | 2025-07-05 | 120 | 232 | yes |
| household | address | **2** | 2026-02-15 | 120 | 232 | yes |
| household | zone_district | **2** | 2026-02-15 | 100 | 232 | yes |
| household | risk_pattern | **2** | 2026-08-06 | 120 | 232 | yes |
| household | zone_district | **2** | **2026-08-14** | **2700** | 232 | yes |
| maya | medication | **2** | 2026-01-13 | 120 | 232 | yes |
| maya | medication | **2** | 2026-03-06 | 120 | 232 | yes |
| maya | appointment | **2** | 2026-07-11 | 140 | 232 | yes |
| maya | medication | **2** | **2026-08-14** | 100 | 232 | yes |
| sam | medication_status | **2** | 2026-08-01 | 140 | 232 | yes |
| sam | incident | **2** | 2026-08-04 | 120 | 232 | yes |
| sam | preference | **2** | 2026-05-10 | 120 | 232 | yes |

**Every row is `key_version = 2`** — the field that would have prevented FM 24's error. **Two rows
were written today (2026-08-14)**, so this is a live, actively-written graph, not a stale one.

**Provenance:** `~/hip-cutover-demo/.hip-graph` declares *"This checkout writes
bolt://localhost:7690. The cutover demo lane. 7690 is its canonical battery graph (CLAUDE.md).
Provisioned by FM 9 on Bill's ruling 3."*

**Tested-keys record, corrected:** the v1 masters `9d1e52699499` and `4b1451f0b69e` return
`InvalidToken` on these rows — **and that is CORRECT BEHAVIOUR, not a defect.** They are v1 keys;
these are v2 envelopes. The correct key material is the `~/hip-keys/*.seal.key` set, and it opens
**13/13**.

**One real thing FM 24 found that still stands:** the cutover tree's `_derive_key` calls
**`_load_master_key()`** where every other tree calls `_load_or_create_master_key()`. **That tree
REFUSES rather than minting on absence** — the hardening the other four lack, and the shape
`REQ_MASTER_KEY_ROTATION`'s "no silent third mint" clause asks for. **It already exists here and
should be the port source.**

---

# S3 — FREEZE CONSEQUENCE

**THE EVIDENCE SUPPORTS NEITHER OF THE TWO BRANCHES AS FRAMED, because both assumed the data was
orphaned. It is not.**

* **The demo DOES depend on decrypting these rows** — `demo_dashboard.py:734/1099/1135` is the
  consumer path, so "demo-never-depends" is **false**.
* **But the dependency is SATISFIED** — 13/13 decrypt through that exact path today.

**Therefore: THE FREEZE IS NOT BLOCKED, and no re-certification is owed.** VD-60's green battery and
the 16/16 rehearsal were green **because the data was fine**, not because they failed to exercise
decryption. **`demo-freeze-20260814` at `d0282bd` stands unaffected.**

**RECOMMENDED (Bill rules): RELEASE THE FORENSIC HOLD on 7690.** It was taken on my false alarm.
Nothing about the graph requires preservation as evidence, and the hold blocks ordinary demo
operation — including `demo_reset`, which the demo needs.

---

# TIME MACHINE — LOOK ONLY

**Destination exists:** `Clean Disk`, Kind `Local`, ID `FC4B1B8F-5C16-41AE-A613-DF158593E5D7`.

**Backups could NOT be enumerated:** `tmutil listbackups` returns
`NSPOSIXErrorDomain Code=1 "Operation not permitted"` — this process lacks Full Disk Access.
**So the question "does any backup hold a `.master_key` candidate" is UNANSWERED, not answered
negatively.** Nothing was restored, mounted, or modified.

**It is also now MOOT:** no key is missing, so there is nothing to recover. Answering it would need
Full Disk Access granted to the terminal — **worth doing only if some future dispatch actually needs
a historical key.**

## CLAIM IMPACT

**CLAIM IMPACT: none.**

## OPEN — NEEDS BILL

1. **Release the forensic hold on 7690** (recommended — it rests on my error).
2. **FM 24's dispatch doc and board row carry the false finding.** They should be **annotated, not
   rewritten**, per the correction class — this dispatch is the correcting record. Confirm that
   treatment.
3. Not blocking, carried from S1: **the cutover tree's `_load_master_key()` refuse-on-absence is the
   port source** for the "no silent third mint" clause in `REQ_MASTER_KEY_ROTATION`.
