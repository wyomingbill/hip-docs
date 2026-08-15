# DISPATCH_KEY_LIFECYCLE_BANK_RERUN — precondition absent again; inventory re-derived, nothing executed

Status: BUILT
Reconciled-Against: roadmap `de823fb` (pre-dispatch HEAD). **LANDED AT `d040a9e`** — backfilled by the immediately following commit.

**HA-11** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **STOP + read-only inventory**
**REQ: NONE.**
**NOTHING CHANGED: no exclusions set, no TD filed, no handoff gate written, no code, no key
deletion, no moves. NOTHING MET.**

---

# STOPPED AT SEGMENT 1 — NEEDS BILL

## 1. THE PRECONDITION — BOTH FILES ABSENT

```
CHATGPT_KeyLifecycle__custody-destruction-rotation__v20260806.md   MISSING
RULING_KeyLifecycle__three-rulings__v20260806.md                   MISSING
```

Searched beyond the exact names before concluding — `~/Downloads`, `~/Desktop`,
`~/Documents`, `~/hip-roadmap` for `*KeyLifecycle*`, `*three-rulings*`, `RULING_*`,
`*custody-destruction*`. **Nothing.**

**A diagnostic worth more than the miss itself:** nothing at all has been written to
`~/Downloads`, `~/Desktop` or `~/Documents` **in the last three hours**. The newest file in
`~/Downloads` is still `Connect_Sponsors.xlsx` at 14:10. **So this is not a naming
mismatch — no new file arrived anywhere.** The save did not land, or landed somewhere none
of the usual locations covers. Worth checking the browser's own download destination before
a third attempt.

## 2. WHY SEGMENTS 2–4 DID NOT PROCEED — this is not HA-10

At HA-10 the surveys were genuinely independent of the missing review, so they ran in full.
**Here they are not.** Every remaining segment derives its authority from the document that
is missing:

| Segment | Depends on the missing ruling how |
|---|---|
| **2 — backup exclusions** | *"AUTHORIZED BY RULING 2"*. `tmutil addexclusion` changes this machine's backup configuration. **The authority for that change is a document that does not exist**, so it cannot be read, quoted, or verified. Executing a system change on an unreadable authority is precisely what the preamble exists to prevent. |
| **3 — file the TD** | *"Bill's ruling: separate defect …"* — an enactment of the same missing ruling. |
| **4 — erasure-enablement gate** | *"cite the banked ruling doc"* — impossible; the citation target does not exist. |

**Item 2's exclusions are the one I want to name explicitly.** The defect is real and I
verified it myself at HA-10 — every key path is `[Included]`, one Time Machine setup from
full capture. The fix is a one-line command per path. **It was still not run**, because
"authorized by Ruling 2" is a claim about a document, and a session that acts on an
authority it cannot read has not been authorized; it has guessed.

## 3. WHAT DID GET DONE — the inventory, re-derived fresh (item 2's first half)

Read-only, no authority required, and **it justifies item 2's own instruction not to reuse
HA-10's list.**

```
2203  [REDACTED-USER-PATH]/hip-keys
 639  [REDACTED-USER-PATH]/hip-roadmap/ledger/keys
   4  [REDACTED-USER-PATH]/hip-dev/ledger/keys
   3  [REDACTED-USER-PATH]/hip-vo/ledger/keys
   3  [REDACTED-USER-PATH]/hip-dev/ledger.mixed-format.bak/keys
   3  [REDACTED-USER-PATH]/hip-cutover-demo/ledger/keys
   1  [REDACTED-USER-PATH]/hip-vo/certs
   1  [REDACTED-USER-PATH]/hip-roadmap/certs
   1  [REDACTED-USER-PATH]/hip-p4-migration-backups/20260721_222014
   1  [REDACTED-USER-PATH]/hip-p4-migration-backups/20260721_165446
   1  [REDACTED-USER-PATH]/hip-harness/data/voiceprints
   1  [REDACTED-USER-PATH]/hip-harness/certs
   1  [REDACTED-USER-PATH]/hip-harness-backups/voiceprints_20260803_175228
   1  [REDACTED-USER-PATH]/hip-harness-backups/voiceprints_20260803_140540
   1  [REDACTED-USER-PATH]/hip-dev/certs
   1  [REDACTED-USER-PATH]/hip-cutover-demo/certs
```

**16 path families, not HA-10's 8** — this pass widened the pattern to `*.pem` as well as
`*.key`, which surfaced `hip-harness-backups/voiceprints_*` and four more `certs`
directories HA-10's narrower search missed. **HA-10's inventory was incomplete, and this
dispatch's own record says so.**

**And it was already stale by count:** `~/hip-keys` went **2,184 → 2,203** and
`ledger/keys` **631 → 639** in the ~20 minutes since HA-10 — because every harness run
mints more (TD-R-172). **Any exclusion list is out of date the moment a battery runs**,
which is an argument for excluding the *directories* rather than enumerating files, and for
TD-R-172's teardown fix landing before consolidation is designed.

**Current state, unchanged by this dispatch:**

```
$ tmutil destinationinfo
tmutil: No destinations configured.
$ tmutil isexcluded ~/hip-keys
[Included]  [REDACTED-USER-PATH]/hip-keys
$ tmutil isexcluded ~/hip-roadmap/ledger/keys
[Included]  [REDACTED-USER-PATH]/hip-roadmap/ledger/keys
```

## 4. HA-10'S FAILED FIRST ATTEMPT — PRESERVED, per item 1

Item 1 requires HA-10's failure to stay on the record rather than be erased by a rerun. It
is preserved in three places and this dispatch adds a fourth:

1. **HA-10's dispatch doc** (`…__v20260806_1901.md`) — records the missing file and the
   `docs/research/` destination question, unedited.
2. **HA-10's `docs/INDEX.md` row** — carries the STOP and the naming conflict.
3. **HA-10's commit `de33def`** — its message states both.
4. **Here:** HA-10 named `docs/research/` as non-existent and recommended `docs/reviews/`;
   **Bill's ruling in this dispatch's item 1 confirms `docs/reviews/`.** The wrong
   destination and its correction both stand on the record. Nothing was rewritten.

## 5. RUNS (item 6) — NOT RUN, and why, rather than silently skipped

**No file in the repository changed except this dispatch doc and its INDEX row.** No code,
no config, no fixtures. `--layer 7`, RATCHET and the memory harness would re-measure the
identical tree HA-10 measured 20 minutes ago (battery 812 + 1 skipped, L7 27/27, L7V2
27/28, AUDIT 8/8, RATCHET PASS, memory 13/17 inside the pin, `de33def`).

**Stated as a choice, not an omission.** If you want them run on every dispatch regardless
of whether anything changed, say so and they will be.

`--full` not attempted: TD-R-171 still blocks Layer 2. **Item 12 NOT satisfied.**

## 6. WHAT IS READY TO RUN THE MOMENT THE FILES LAND

Nothing here needs re-deciding — only the two files:

- **Segment 1:** bank both into `docs/reviews/` with SHA-256 proven both sides, register in
  INDEX + MANIFEST Section B.
- **Segment 2:** `tmutil addexclusion` over the 16 paths above (re-derived again at that
  point, since the list moves), each verified with raw `tmutil isexcluded` output.
- **Segment 3:** the plaintext-`recall_audit` defect files as **TD-R-173** (172 is taken by
  the seal-key leak).
- **Segment 4:** the erasure-enablement gate into `HIP_HANDOFF.md` CURRENT STATE, citing the
  banked ruling.

## 7. FINDINGS

1. **Both precondition files are absent, and nothing has been saved to any usual location
   in three hours** (§1) — a save-destination problem, not a naming one.
2. **Segments 2–4 all derive authority from the missing ruling** (§2). Unlike HA-10, there
   was no independent work to complete.
3. **HA-10's key inventory was incomplete (8 families vs 16) and is already stale by count**
   (§3). Re-deriving per dispatch is right, and directory-level exclusions will age better
   than file lists.
4. **TD-R-173 is the next free number** — TD-R-172 is the seal-key leak from HA-08.
