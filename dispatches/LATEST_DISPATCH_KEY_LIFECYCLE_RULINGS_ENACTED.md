# DISPATCH_KEY_LIFECYCLE_RULINGS_ENACTED — exclusions applied, audit TD filed, erasure gated

Status: BUILT
Reconciled-Against: roadmap `1dad48c` (pre-dispatch HEAD). **LANDED AT `a6a1e05` (ruling banked) and `442c7c4` (rulings enacted)** — backfilled by the immediately following commit.

**HA-13** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **DOCS + SYSTEM CONFIG**
**AUTHORITY:** `docs/reviews/RULING_KeyLifecycle__three-rulings__v20260806_2000.md` — banked
by this dispatch, and the authority HA-11 refused to act without.
**NOTHING MET. No key deletion, no moves, no consolidation, no cascade code.**

**RESUMED AFTER A MID-DISPATCH CONNECTION DROP.** The drop landed between writing the
ruling file and committing it. On resume the file was found untracked and unregistered;
its integrity was re-verified before anything else (§1) rather than assumed.

## 1. SEGMENT 1 — the ruling banked, and verified three times

Written to `docs/reviews/RULING_KeyLifecycle__three-rulings__v20260806_2000.md`.
**HA-12's naming flag was heard: this filename carries `_HHMM`.**

**Truncation check, run three times:**

| When | Begins `## Rulings` | Ends *"…the system can presently deliver."* |
|---|---|---|
| on the paste, before writing | PASS | PASS |
| on the written file | PASS | PASS |
| **after the connection drop, on resume** | **PASS** | **PASS** |

Body SHA-256 `c0e06de5a3ff99035e1e2e5eb6068c335f84dfb06d1e2f3449cb49b034036d8f` — **identical
before and after the drop**, which is what makes the resume safe rather than hopeful.
6 `###` ruling sections, 4 code blocks, 215 lines.

**A RULING IS NOT A REVIEW, and the file says so at the top.** It shares `docs/reviews/`
with `CHATGPT_KeyLifecycle__…` because Ruling 1 puts the pair there, but they carry opposite
authority — one is an unverified external opinion binding on nothing, the other is Bill's
decision and binds. Both headers carry the distinction so neither can be mistaken for the
other. Registered in INDEX under `reviews/` and in MANIFEST Section B (item 2).

## 2. SEGMENT 3 — the inventory, preserved as evidence

Re-derived at execution time, per the ruling's own step 1 (*"Inventory the current
key-bearing paths and preserve the inventory as evidence"*). **16 families, matching HA-11's
count** — no new family appeared:

```
 1  [REDACTED-USER-PATH]/hip-cutover-demo/certs
 2  [REDACTED-USER-PATH]/hip-cutover-demo/ledger/keys
 3  [REDACTED-USER-PATH]/hip-dev/certs
 4  [REDACTED-USER-PATH]/hip-dev/ledger.mixed-format.bak/keys
 5  [REDACTED-USER-PATH]/hip-dev/ledger/keys
 6  [REDACTED-USER-PATH]/hip-harness-backups/voiceprints_20260803_140540
 7  [REDACTED-USER-PATH]/hip-harness-backups/voiceprints_20260803_175228
 8  [REDACTED-USER-PATH]/hip-harness/certs
 9  [REDACTED-USER-PATH]/hip-harness/data/voiceprints
10  [REDACTED-USER-PATH]/hip-keys
11  [REDACTED-USER-PATH]/hip-p4-migration-backups/20260721_165446
12  [REDACTED-USER-PATH]/hip-p4-migration-backups/20260721_222014
13  [REDACTED-USER-PATH]/hip-roadmap/certs
14  [REDACTED-USER-PATH]/hip-roadmap/ledger/keys
15  [REDACTED-USER-PATH]/hip-vo/certs
16  [REDACTED-USER-PATH]/hip-vo/ledger/keys
```

**The drift that justifies directory-level exclusion, measured rather than argued:**
`~/hip-keys` went **2,203 → 2,204** between HA-11 and this dispatch — a single idle-ish
interval. A per-file exclusion list would have been wrong before it was verified. **Item 3's
"never per file" is right, and the count proves it.**

## 3. SEGMENT 3 — exclusions applied and verified

All 16 `tmutil addexclusion` calls succeeded silently (exit 0, no output — the tool's
success mode). Verification, raw:

```
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-cutover-demo/certs"
    [Excluded]  [REDACTED-USER-PATH]/hip-cutover-demo/certs
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-cutover-demo/ledger/keys"
    [Excluded]  [REDACTED-USER-PATH]/hip-cutover-demo/ledger/keys
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-dev/certs"
    [Excluded]  [REDACTED-USER-PATH]/hip-dev/certs
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-dev/ledger.mixed-format.bak/keys"
    [Excluded]  [REDACTED-USER-PATH]/hip-dev/ledger.mixed-format.bak/keys
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-dev/ledger/keys"
    [Excluded]  [REDACTED-USER-PATH]/hip-dev/ledger/keys
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-harness-backups/voiceprints_20260803_140540"
    [Excluded]  [REDACTED-USER-PATH]/hip-harness-backups/voiceprints_20260803_140540
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-harness-backups/voiceprints_20260803_175228"
    [Excluded]  [REDACTED-USER-PATH]/hip-harness-backups/voiceprints_20260803_175228
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-harness/certs"
    [Excluded]  [REDACTED-USER-PATH]/hip-harness/certs
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-harness/data/voiceprints"
    [Excluded]  [REDACTED-USER-PATH]/hip-harness/data/voiceprints
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-keys"
    [Excluded]  [REDACTED-USER-PATH]/hip-keys
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-p4-migration-backups/20260721_165446"
    [Excluded]  [REDACTED-USER-PATH]/hip-p4-migration-backups/20260721_165446
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-p4-migration-backups/20260721_222014"
    [Excluded]  [REDACTED-USER-PATH]/hip-p4-migration-backups/20260721_222014
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-roadmap/certs"
    [Excluded]  [REDACTED-USER-PATH]/hip-roadmap/certs
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-roadmap/ledger/keys"
    [Excluded]  [REDACTED-USER-PATH]/hip-roadmap/ledger/keys
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-vo/certs"
    [Excluded]  [REDACTED-USER-PATH]/hip-vo/certs
$ tmutil isexcluded "[REDACTED-USER-PATH]/hip-vo/ledger/keys"
    [Excluded]  [REDACTED-USER-PATH]/hip-vo/ledger/keys
```

**16 of 16 `[Excluded]`.** Before this dispatch every one read `[Included]` (HA-10, HA-11).

**EXCLUSIONS ONLY.** No consolidation, no deletion, no moves — item 3's boundary and Ruling
2's own sequencing (consolidation is step 3, *"a separately evidenced migration"*).

### Three limits of this mechanism, named because a reader will over-trust it

1. **The exclusion is an xattr on the item** (`com.apple.metadata:com_apple_backup_excludeItem`,
   confirmed present on `~/hip-keys`). **Delete and recreate a directory and the exclusion is
   gone with it** — it does not survive its own path being replaced.
2. **It is per-path, not a rule.** A 17th key family created tomorrow is **not** covered.
   Ruling 2's step 6 anticipates this: *"After consolidation, maintain one explicit backup
   exclusion rather than eight-plus fragile ones."* These 16 are the fragile interim.
3. **No backup destination exists**, so nothing was going to be copied today regardless.
   The value is entirely prospective — which is exactly Ruling 2's point that *"no backup
   configured today is not a backup policy."*

## 4. SEGMENT 4 — TD-R-173 filed, not fixed

`logs/memory_engine/recall_audit.jsonl` stores the **full natural-language query text**
alongside `subject`, `requester` and `reason`, all plaintext — measured on live rows at
HA-10.

Filed as **TD-R-173** (register `v20260806_2036`, LATEST repointed) with Bill's ruling
quoted verbatim, including *"Do not bury it as incidental work under graph-node erasure."*

**Why it is not covered by key destruction, recorded in the row:** the audit log is
**beside-seal** — no key protects it — so destroying a subject's key leaves the query text
and subject id fully readable. And a recall query is itself disclosive: *"what health
conditions did they have in the past?"* names the concern with no answer attached.

**FILED, NOT FIXED.** The fix touches a live audit write path and needs its own REQ.
**Independent by ruling** — it must not wait for the cascade, and the cascade must not
absorb it.

## 5. SEGMENT 5 — the erasure gate, written into CURRENT STATE

Placed at the **top** of `docs/HIP_HANDOFF.md`'s CURRENT STATE, before the dispatch
history, so nobody reaches erasure work without meeting it:

> **NO REAL-DATA ERASURE UNTIL *BOTH*** key-custody consolidation **AND** the
> semantic-metadata cascade have landed.

It cites the banked ruling and quotes Bill's closing sentence. It also records **why the
gate has two conditions**, because either alone leaves the claim false in a different
direction — custody without the cascade is primary-record VALUE erasure only (HA-10's
`representation_class=HEALTH_CLAIM` measurement); cascade without custody makes "we
destroyed the key" unprovable (HA-08's growing key population, HA-11's 16 directories).

**And what has NOT landed toward it:** the exclusions are a **precondition, not either gate
condition**. Neither consolidation nor the cascade is started. TD-R-173 is explicitly
outside the gate in both directions.

## 6. RUNS (item 7)

| Run | Result |
|---|---|
| Standing battery | **812 passed, 1 skipped, 9 xfailed** |
| `--layer 7` L7 / L7V2 | **27/27** / **27/28** |
| AUDIT / DISC / SCHEMA / VOICE | **8/8 / 1/1 / 1/1 / 1/1** |
| **RATCHET** | **PASS** |
| Memory harness | **13/17**, failures exactly {MEM-115, MEM-116, MEM-117, MEM-118}, inside the pin |

`--full` not attempted: TD-R-171 still blocks Layer 2. **Item 12 NOT satisfied.**

## 7. FINDINGS

1. **The exclusions are fragile by construction** (§3) — xattr-based, per-path, and blind to
   a 17th family. Ruling 2 already names the durable answer: consolidate, then hold one
   exclusion.
2. **Key count drifted again during this dispatch** (2,203 → 2,204), which is the measured
   argument for directory-level exclusion and for TD-R-172's teardown fix.
3. **A ruling and a review now share one folder.** Handled by explicit headers on both, but
   `docs/reviews/` is defined in CLAUDE.md as the home for *reviews*; a ruling living there
   is Bill's call and is recorded rather than treated as routine.
4. **The gate's two conditions are independent and neither is started** (§5).
