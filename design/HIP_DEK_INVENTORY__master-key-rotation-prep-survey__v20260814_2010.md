# HIP DEK INVENTORY — master-key rotation prep
Status: BUILT (survey)
Reconciled-Against: `~/hip-vo` @ `main` `ff79487`; live graph reads 2026-08-14 20:10 MDT

**READ-ONLY throughout. No rotation, no key operation, no write to any store.** Findings only.
Keys are reported by SHA-256 prefix; no key material appears here.

---

## 0. THE CORRECTION THAT COMES FIRST — **`HIP_MASTER_KEY` IS A PATH, NOT A KEY**

**FM 19 and FM 20 both recorded *"`HIP_MASTER_KEY` was exposed while world-readable and has not been
rotated."* THAT IS WRONG AS STATED, and it is mine to correct.**

`harness/encryption.py:52` — `_master_key_path()` reads `$HIP_MASTER_KEY` and returns it **as a
filesystem path**:

```python
def _master_key_path() -> pathlib.Path:
    env = os.environ.get("HIP_MASTER_KEY")
    return pathlib.Path(env) if env else DEFAULT_MASTER_KEY_PATH
```

The value in the world-readable plist was **`[REDACTED-USER-PATH]/hip-dev/data/encryption/.master_key`** —
50 characters, and a real path, which is why its length looked credential-shaped.

**What the exposure actually disclosed was WHERE the key lives, not the key.** The key file itself:

| | |
|---|---|
| `~/hip-dev/data/encryption/.master_key` | **`-rw-------`**, 32 bytes |
| its parent directory | **`drwx------`** |

**The key material was never world-readable.** Path disclosure is a real but far weaker exposure
than key disclosure — it removes obscurity, not protection.

**CONSEQUENCE FOR THE OPEN ITEM:** the "last exposed-and-unrotated credential" carried out of FM 19
and FM 20 **is not an exposed credential at all.** Whether to rotate the master key on general
principle remains Bill's call, but **it is no longer leak-driven, and it should not be ranked as
remediation.**

## 1. EVERY DEK WRAPPED BY THE MASTER KEY

### The hierarchy (from `harness/encryption.py`)

```
master key (32 bytes, on disk)
  └─ HKDF-SHA256(master, info="…:<owner>")  →  owner key (Fernet)      ← per owner, DERIVED
       └─ Fernet(owner_key).encrypt(dek)    →  encrypted_dek           ← per fact, STORED
            └─ Fernet(dek).encrypt(value)   →  ciphertext              ← per fact, STORED
```

**DEKs are wrapped by the OWNER key, which is derived deterministically from the master.** So a new
master changes every owner key, and **every stored `encrypted_dek` becomes unopenable** — the
ciphertext is untouched but the key to it is unreachable.

### THERE ARE TWO WRAPPED KEYS PER FACT, NOT ONE

The `:Fact` property list carries **`encrypted_dek`** *and* **`driving_utterance_dek`** — the fact's
value and the utterance that produced it are separately enveloped. **Any rotation plan that counts
facts and not envelopes is half-sized.**

| graph | facts w/ value DEK | utterance DEKs | **total wrapped keys** | owners |
|---|---|---|---|---|
| **7691** `~/hip-vo` | 14 | 14 | **28** | household 5, sam 4, maya 4, bill 1 |
| **7690** `~/hip-cutover-demo` | 13 | 13 | **26** | — |
| **7689** frozen demo | 11 | 11 | **22** | household 5, maya 3, sam 3 |
| **7688** `~/hip-roadmap` | **UNKNOWN** | UNKNOWN | **UNKNOWN** | — |

**TOTAL ACROSS REACHABLE GRAPHS: 76 wrapped keys.**

**7688 IS AN HONEST GAP, NOT A ZERO.** `~/hip-roadmap/.env.dev` pins no `NEO4J_PASSWORD` — that lane
sources it from the operator's shell by design — so **this survey had no credential for it and did
not attempt one.** `7687` and `7692` are listening and refused the stores available here, so their
contents are likewise unmeasured. **A rotation plan must close these before it runs.**

### AND THERE ARE **TWO DISTINCT MASTER KEYS** ON THIS MACHINE

| tree | master key | sha256[:12] |
|---|---|---|
| `~/hip-dev` | present, 32 B, `0600` | **`9d1e52699499`** |
| `~/hip-cutover-demo` | present, 32 B, `0600` | **`9d1e52699499`** — *same key* |
| `~/hip-harness` | present, 32 B, `0600` | **`4b1451f0b69e`** — **DIFFERENT** |
| `~/hip-roadmap` | **ABSENT** (the directory exists) | — |

**"Rotate the master key" is therefore ambiguous, and that ambiguity is itself a finding.** There
are two key domains, and `~/hip-roadmap` has no key file at all — meaning it would **create one on
first use** (`_load_or_create_master_key`), which is a third domain waiting to happen.

## 2. READ PATHS THAT UNWRAP A DEK — 13 sites, 9 modules

| module | sites |
|---|---|
| `harness/fact_change.py` | `:342`, `:367`, `:405` |
| `harness/extraction_queue.py` | `:772`, `:844` |
| `harness/disclosure.py` | `:245` |
| `memory_engine/api.py` | `:204` |
| `memory_engine/recall.py` | `:223` |
| `server/demo_dashboard.py` | `:598`, `:952` |
| `server/voice_https_orch.py` | `:643` |
| `server/memory_dashboard.py` | `:119` |
| `scripts/migrate_fact_schema.py` | `:182` |

**WHAT BREAKS ON AN UN-RE-WRAPPED ROTATION:** every one of these raises at
`Fernet(_derive_key(owner)).decrypt(...)` — **`InvalidToken`**. Concretely: fact recall returns
nothing usable, disclosure cannot render a value, fact-change cannot compare against current state
(so it may treat every existing fact as absent and **write duplicates**), and both dashboards' fact
panels fail. **The data is not destroyed — the ciphertext is intact — but it is unreachable, and
`MasterKeyLostError` exists in this module precisely because that state was anticipated.**

## 3. THE RE-WRAP SURFACE

**A rotation capability must touch, in this order:**

1. **Enumerate every graph** — including the ones this survey could not reach (7688, 7687, 7692). A
   graph missed here is data orphaned permanently.
2. **For each fact: BOTH envelopes** — `encrypted_dek` and `driving_utterance_dek`.
3. **Per owner, not per fact** — the owner key is the unit of derivation (`household`, `bill`,
   `maya`, `sam`), so unwrap-with-old / rewrap-with-new is keyed on `owner`.
4. **Bump `key_version` in the same write as the new `encrypted_dek`.** Not after.
5. **Both master key domains** (`9d1e52699499`, `4b1451f0b69e`), or one is stranded.

### THE ROLLBACK DESIGN CONSTRAINT — and the good news

**`key_version` is ALREADY on every fact node** (`KEY_VERSION = 1` in code; all rows currently read
`1`). **The schema already supports a staged, resumable, per-row rotation** — this does not need to
be built, only used.

**Therefore the rollback point is the ROW, not the run.** A rotation that re-wraps and stamps
`key_version = 2` in one atomic write per row can be interrupted at any point and leave a graph in a
mixed but fully readable state, **provided the readers select the key by the row's own
`key_version`** rather than assuming a global one.

**THAT IS THE CONSTRAINT, stated plainly: the 13 read paths currently derive the owner key with NO
reference to `key_version`.** Until they do, the system cannot hold both versions at once, so any
rotation is necessarily **all-or-nothing with no partial-failure recovery** — the old master must be
retained until the last row is proven, and there is no safe interruption point. **Making the readers
version-aware is the prerequisite that converts this from a risky migration into a resumable one.**

## 4. DECRYPT-PROOF CANDIDATES

Post-rotation access should be proven **end to end, per owner, across both envelopes** — one owner
proving nothing about another, since the keys are independently derived:

| candidate | why |
|---|---|
| a **`household`** fact on 7691 | the shared namespace, 5 rows — the widest blast radius |
| a **`bill`** fact on 7691 | the only `bill`-owned row measured (1) — a single-row owner is the easiest to strand silently |
| a **`maya`** and a **`sam`** fact | distinct derived keys; proves derivation, not just one lucky key |
| any fact's **`driving_utterance_dek`** | the second envelope, which a fact-count-based plan omits |
| a fact on **7689** (frozen) | proves the frozen demo still opens — it is the fallback |

**The proof must be a real read through a real read path** (e.g. `memory_engine/recall.py:223`),
**not a direct `decrypt_fact_value` call in a test harness** — the latter proves the primitive and
not the wiring.

## 5. BACKUPS — THE RECOVERY HAZARD

**No `.dump`, `.backup`, or Neo4j backup artifact was found** under `~` to depth 4.

**But the hazard is present in a different shape, and it is worse:** `~/hip-dev` and
`~/hip-cutover-demo` **share master key `9d1e52699499`**. Rotating "the" master key in one tree
without the other **strands every DEK in the other tree's graph** — the frozen demo (7689, 22
wrapped keys) and the cutover demo (7690, 26) are coupled through a shared key file they each hold a
copy of.

**And the copies are independent files, not a symlink** — so rotating one leaves the other holding
the old key, which is exactly the recovery hazard the question asks about, arriving via
duplication rather than via backups.

**RETENTION RULE THIS IMPLIES:** the old master key must be retained, offline and read-only, until
**every** graph — including the unmeasured ones — is proven re-wrapped. **Deleting it at the end of a
partially-complete rotation is unrecoverable.**

## OPEN — NEEDS BILL

1. **The premise is weaker than recorded.** `HIP_MASTER_KEY` exposure was a **path**, not key
   material. Rotation is a hygiene decision, not remediation (§0).
2. **Two master key domains, and `~/hip-roadmap` has none** — it would mint a third on first use.
   Which domains are in scope?
3. **Three graphs are unmeasured** (7688, 7687, 7692). This survey had no credential for them and
   did not attempt one.
4. **The readers are not `key_version`-aware**, so today a rotation is all-or-nothing with no
   resumable rollback (§3). Making them version-aware is the prerequisite.
