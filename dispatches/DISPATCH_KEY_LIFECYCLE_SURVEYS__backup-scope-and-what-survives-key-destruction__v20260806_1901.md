# DISPATCH_KEY_LIFECYCLE_SURVEYS — backup scope, and what survives key destruction

Status: BUILT
Reconciled-Against: roadmap `f9af09c` (pre-dispatch HEAD). **LANDED AT `de33def`** — backfilled by the immediately following commit.

**HA-10** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **SURVEY ONLY**
**REQ: NONE** — surveys and a banking step; no code change is in scope (item 4).
**NOTHING CHANGED: no code, no deletions, no exclusion edits, no re-keying. NOTHING MET.**

---

# STOPPED AT SEGMENT 1 — NEEDS BILL

**The precondition file is not on disk.** Surveys A and B are independent of it and were
completed in full (§2, §3), because they are read-only and their findings do not depend on
the review.

## 1. SEGMENT 1 — BLOCKED

`~/Downloads/CHATGPT_KeyLifecycle__custody-destruction-rotation__v20260806.md` **does not
exist.** Searched beyond the exact name before concluding: `~/Downloads`, `~/Desktop`,
`~/Documents` for `*keylifecycle*`, `*CHATGPT*`, `*custody-destruction*`, and every `.md`
added to `~/Downloads` today (`cutover7_report.md`, `disk_check_report.md`,
`REQ_OFFER_MECHANISM_revised.md` — none is the review). The `chatgpt*` files present are
older and on other topics.

**Nothing was banked.** Re-save the file and this segment runs on its own.

**A naming-law conflict to settle when it does:** item 1 says bank into `docs/research/`.
**That folder does not exist**, and the LOCKED folder list in `CLAUDE.md` has no such entry.
`docs/reviews/` is purpose-built for exactly this artifact — *"external/second-model review
artifacts captured verbatim … a review records what a reviewer CLAIMED, not what was
verified"* — which is item 1's own `Status: BANKED / Verification: UNVERIFIED` pattern
already written into the framework. **Recommendation: `docs/reviews/`**, unless you mean a
new folder, which would be a LOCKED-list change and therefore your call.

## 2. SURVEY A — BACKUP SCOPE OF KEY MATERIAL

**Found by search, not assumption.** Key material is in **more places than `~/hip-keys/`**:

| Path | Files | Note |
|---|---|---|
| `~/hip-keys` | **2,184** | the main store; not inside any git repo |
| `~/hip-roadmap/ledger/keys` | **631** | **inside the repo working tree** |
| `~/hip-dev/ledger/keys`, `~/hip-vo/ledger/keys`, `~/hip-cutover-demo/ledger/keys` | 3–4 each | one per worktree |
| `~/hip-dev/ledger.mixed-format.bak/keys` | 3 | a backup directory |
| `~/hip-p4-migration-backups/20260721_*` | 1 each | **key material inside dated backups** |
| `~/hip-roadmap/certs`, `~/hip-vo/certs`, `~/hip-harness/certs` | 1 each | TLS certs |
| `~/hip-harness/data/voiceprints` | 1 | biometric-adjacent |

### Is any of it in git? **No — verified, not assumed.**

`ledger/` is gitignored (`.gitignore:14`), `git ls-files ledger/keys` returns **0**, and
`git log --all -- 'ledger/keys/*'` is **empty** — never committed on any branch.

### Is any of it backed up? **No — because nothing is.**

```
$ tmutil destinationinfo
tmutil: No destinations configured.

$ tmutil listlocalsnapshots /
Snapshots for disk /:            (none)
```

**No Time Machine destination. No local snapshots.** And **no cloud-sync root exists on
this machine at all** — `~/Library/Mobile Documents`, `~/Library/CloudStorage`, `~/Dropbox`,
`~/Google Drive`, `~/OneDrive` are all absent, so no key path can be inside one.

### The finding that matters, and it cuts both ways

Every key path reports **`[Included]`** to `tmutil isexcluded` — meaning *not excluded*.

- **Today:** key material is backed up **nowhere**. There is no copy off this disk.
- **The moment a Time Machine destination is configured, all 2,800+ key files are captured
  automatically**, including `~/hip-p4-migration-backups`, because nothing excludes them.

So the current state is simultaneously the safest (no copies) and the most fragile (no
copies), and it is **one setup step away from the opposite exposure**. **No exclusion was
changed — item 2 says the fix is yours.**

## 3. SURVEY B — WHAT SURVIVES KEY DESTRUCTION, for subject `dad`

Verified **by attempting the read**, not by reading intent.

### UNDER-SEAL — unreadable without the key

| Surface | Evidence |
|---|---|
| Fact **values** | `ciphertext` + `encrypted_dek` present on all 3 `subject='dad'` rows; HA-09 already proved a wrong key yields `InvalidToken` |
| **HEL ledger payloads** | every event carries `payload_enc` + `payload_kid` + `payload_sha256`; the plaintext body is not in the file |

### BESIDE-SEAL — readable with no key at all

**The graph node itself**, dumped with no decrypt attempted, exposes for each `dad` fact:

```
subject     = dad                    attribute      = incident
representation_class = HEALTH_CLAIM  sensitivity    = high
owner       = sam                    write_state    = augment
salience    = 0.4                    confidence     = medium
recorded_at / valid_from / timestamp = 2026-07-28T00:30:57…
confidence_log = [{"ts": …, "from": null, …}]   derived_from = []
```

**`representation_class = HEALTH_CLAIM` is the sharp one.** After destroying dad's key, a
reader still learns: *a health claim of kind `incident` about dad, authored by sam, rated
high sensitivity, recorded at this timestamp, with this confidence history.* The **value**
is gone; the **claim's existence, class, subject, author, timing and salience are not.**

**Other beside-seal surfaces:**

- `logs/memory_engine/recall_audit.jsonl` — `subject`, **the full query text**, `requester`
  and `reason`, all plaintext. Verified on live rows, e.g.
  `query='what health conditions did they have in the past?'`. No `dad` row exists today,
  but the format stores queries in the clear for whatever subject is recalled.
- **HEL ledger envelope** — `event_type`, `actor.id`, `ts`, `seq`, `hash`, `prev_hash`,
  `correlation.fact_ids`, `correlation.turn_id`: all plaintext around the sealed payload.
- **`scripts/demo_seed.py`, tracked in git** — the fixture **values in source**, including
  the comment *"D4 (dad fell) + D5 (Medication A discontinued)"*. Key destruction does
  nothing to a plaintext string in a committed file.

### A WRONG READING THIS SURVEY MADE AND CORRECTED, recorded because the number was alarming

A first pass reported **"711 ledger lines mention dad"**, then **"637 in a plaintext
field"**. **Both were wrong.** Field-by-field attribution shows every hit is a **hex or UUID
coincidence** — `sha256:0a8eb**dad**05…`, `49943**dad**-5bfd…`, `**dad**d6eeb-0c61…`,
`p4peera_9**dad**8858`. **Not one is the subject.** The HEL ledger does **not** expose the
subject in plaintext.

This is the D-75 trap in a new costume: a naive grep over hex produces a confident false
statement, and the first two numbers would have gone into a security finding unchallenged.
Corrected before landing; recorded so the correction is the record, not a silent edit.

### The verdict item 3 was asked for

**KEY DESTRUCTION IS PRIMARY-RECORD ERASURE, NOT ERASURE.** It removes the value and the
ledger payload. It leaves the subject, the attribute, the representation class, the
sensitivity, the author, the timing, the confidence history, the audit query text, and — in
the fixtures' case — the value itself in a committed source file.

## 4. RUNS (item 5)

Survey-only dispatches still prove they broke nothing.

| Run | Result |
|---|---|
| Standing battery | **812 passed, 1 skipped, 9 xfailed** — unchanged from HA-08 |
| `--layer 7` L7 / L7V2 | **27/27** / **27/28** |
| AUDIT / DISC / SCHEMA / VOICE | **8/8 / 1/1 / 1/1 / 1/1** |
| **RATCHET** | **PASS** |
| Memory harness | **13/17**, failures exactly {MEM-115, MEM-116, MEM-117, MEM-118}, inside the pin |

`--full` not attempted: TD-R-171 still blocks Layer 2 (HA-09). **Item 12 NOT satisfied.**

## 5. FINDINGS

1. **Segment 1 blocked** — the review file is absent (§1), plus the `docs/research/` vs
   `docs/reviews/` naming question.
2. **Key material lives in 8+ paths, not one** (§2). Any policy written against
   `~/hip-keys/` alone would miss 640+ files, including key material inside dated backup
   directories.
3. **Nothing is backed up, and nothing is excluded** (§2) — one Time Machine setup from
   full capture. Not changed; yours to rule.
4. **Key destruction leaves the claim's class and existence readable** (§3). If the erasure
   claim is meant to be stronger than "the value is gone", the beside-seal metadata is where
   the work is.
5. **Fixture values sit in plaintext in a tracked source file** (§3) — outside any key's
   reach by construction.
6. **A wrong grep-derived number was caught and corrected before landing** (§3).
