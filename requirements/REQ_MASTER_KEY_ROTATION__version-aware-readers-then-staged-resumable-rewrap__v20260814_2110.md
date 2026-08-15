# REQ_MASTER_KEY_ROTATION — version-aware readers, then a staged resumable re-wrap
Status: **PLAN**
Reconciled-Against: `~/hip-vo` @ `main` `ff79487`; inventory `docs/design/HIP_DEK_INVENTORY__master-key-rotation-prep-survey__v20260814_2010.md` (FM 21)

**DOCS ONLY. Nothing here has been built, and no key operation has been performed.**

## THE REQUIREMENT — Bill's ruling 5, verbatim in effect

> **No rotation without complete DEK inventory, re-wrap, rollback/recovery, and post-rotation
> decrypt proof.**

**All four are CONJUNCTIVE. Three of four is not a partial pass; it is a stop.**

---

## 0. THIS IS HYGIENE, NOT REMEDIATION — the framing correction that governs urgency

**FM 21 corrected FM 19 and FM 20: `HIP_MASTER_KEY` is a PATH, not key material.**
`harness/encryption.py:52` reads it and returns `pathlib.Path(env)`. The value in the
world-readable plist was `[REDACTED-USER-PATH]/hip-dev/data/encryption/.master_key` — 50 characters,
which is why its length read as credential-shaped. **The key file is `-rw-------` inside a
`drwx------` directory; key material was never world-readable.**

**Therefore this REQ is NOT leak remediation and must not inherit remediation's urgency.** What was
disclosed was *where the key lives*. **A rotation done in a hurry against a mis-stated premise is
how the 76 wrapped keys get stranded** — the risk of acting exceeds the risk that prompted it.

## 1. CLAUSE — VERSION-AWARE READERS FIRST. **PREREQUISITE, NOT OPTIONAL.**

**The 13 unwrap sites MUST select the owner key by the row's own `key_version` BEFORE any rotation
runs.** Today every one of them calls `_derive_key(owner)` with no version reference, so the system
can hold exactly one master at a time.

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

**WHY THIS ORDERING IS THE WHOLE DESIGN, stated so it is not traded away under time pressure:**
`key_version` is **already** on every fact node (`KEY_VERSION = 1`; all rows read `1`), so the
**schema** already supports staged rotation. **The readers are the only thing missing.** Until they
are version-aware, a graph cannot hold v1 and v2 rows simultaneously — which means:

* there is **no safe interruption point**;
* a crash at row 40 of 76 leaves a graph **partly unreadable**;
* **the rollback unit is the entire run**, and the only rollback is "restore the old master and
  re-wrap everything back".

**With version-aware readers, the rollback unit becomes THE ROW.** A mixed-version graph is a
*normal, fully readable* state rather than a broken one. **That single change converts an
all-or-nothing migration into a resumable one, and it is the reason this clause comes first.**

**A rotation attempted before this clause is satisfied is a REFUSAL, not a judgment call.**

## 2. CLAUSE — RETENTION OF THE OLD MASTER

**The old master key is retained, OFFLINE and READ-ONLY, until EVERY in-scope graph has proven
re-wrapped.** Not until the run reports success; **until the proof in §4 passes for every graph.**

* **Deleting it at the end of a partially-complete rotation is unrecoverable.** Ciphertext survives
  a rotation; the key to it does not.
* **Retention is not a convenience copy.** It is read-only, outside any tree that a rotation script
  can reach, and its destruction is a **separate, explicit ruling** after the proof — never a
  cleanup step inside the rotation.
* **`MasterKeyLostError` already exists in `harness/encryption.py`** because this state was
  anticipated. This clause exists so it is never reached.

## 3. SCOPE — **RULED BY BILL, 2026-08-14 (FM 24).** The questions are kept below as asked.

| question | RULING |
|---|---|
| **3a — which key domains** | **BOTH, SEQUENCED DELIBERATELY.** Not both at once, and not one only. |
| **3a(ii) — `~/hip-roadmap` has no key** | **AN EXPLICIT KEY-DOMAIN DECISION IS REQUIRED BEFORE ITS FIRST ENCRYPTED USE. NO SILENT THIRD MINT.** |
| **3c — classification** | **HYGIENE, CONFIRMED.** Not remediation. |

### What "BOTH, SEQUENCED DELIBERATELY" binds

**Sequenced is the operative word, and it is a safety property, not scheduling.** The two domains
are rotated **one at a time, each proven complete before the next begins** — because
`9d1e52699499` is held as **independent copies** by `~/hip-dev` and `~/hip-cutover-demo`, and a
concurrent rotation across domains makes a partial failure impossible to attribute: a stranded DEK
could belong to either run.

**Within the shared domain, the two COPIES must move together** — rotating one tree's copy while the
other still holds the old key strands the other's DEKs (7689's 22 envelopes, 7690's 26). **"Sequence
the domains" does not license splitting a domain.**

### What "NO SILENT THIRD MINT" binds — the clause with teeth

`_load_or_create_master_key()` **creates a key when none exists.** In `~/hip-roadmap` that is a
loaded gun: **the first encrypted write there mints a third master key domain silently, and nobody
decides it.** The ruling is that the decision must be **explicit and prior**.

**Therefore, as a hard clause: `~/hip-roadmap` MUST NOT PERFORM A FIRST ENCRYPTED WRITE until its
key domain is ruled.** Two defensible answers exist (join `9d1e52699499`, or mint a fourth
deliberately with its own retention) and **this REQ does not choose between them** — it only forbids
the choice being made by accident, by whichever process happens to encrypt first.

**A guard that REFUSES rather than creating, when no key file is present and no domain is declared,
is the buildable form of this ruling** — named here as the obvious implementation and explicitly
**not built by this REQ**.

### What "HYGIENE, CONFIRMED" binds

§0 stands as written and is now ruled, not merely argued: **this is not leak remediation, and it
must not inherit remediation's urgency.** The corollary is the operative part — **schedule pressure
is not a reason to weaken clause 1 or clause 2.** A rushed rotation is the only way the 76 known
envelopes get stranded, and the exposure that prompted this was a **path**, not key material.

## 3′. THE SCOPE QUESTIONS AS ASKED — kept verbatim

**3b (the three unmeasured graphs) is NOT ruled and remains open** — it is answered by evidence, not
by decision, and FM 24 §S2 surveys it. **The rotation still refuses to start while any in-scope
graph is unmeasured.**


### 3a. WHICH KEY DOMAINS? **Two exist, and one is duplicated.**

| tree | master key | sha256[:12] |
|---|---|---|
| `~/hip-dev` | present, 32 B, `0600` | **`9d1e52699499`** |
| `~/hip-cutover-demo` | present, 32 B, `0600` | **`9d1e52699499`** — **an independent COPY, not a symlink** |
| `~/hip-harness` | present, 32 B, `0600` | **`4b1451f0b69e`** |
| `~/hip-roadmap` | **ABSENT** — directory exists | — |

**"Rotate the master key" is ambiguous and must be disambiguated before the build.** Two
consequences carry:

* **Rotating `9d1e52699499` in one tree strands the other's DEKs** — 7689 (22 wrapped keys) and 7690
  (26) are coupled through duplicated copies of one key. **This is the recovery hazard, and it
  arrives by duplication rather than by backups** (no `.dump` artifacts exist).
* **`~/hip-roadmap` has no key file and would MINT A THIRD DOMAIN on first use**
  (`_load_or_create_master_key`). A rotation that does not decide roadmap's domain creates one by
  accident.

### 3b. THREE GRAPHS ARE UNMEASURED

**7688, 7687, 7692 — an honest gap, not a zero.** `~/hip-roadmap/.env.dev` pins no
`NEO4J_PASSWORD` by design (the operator supplies it), so FM 21 had no credential and **did not
attempt one**. 7687 and 7692 are listening and refused the available stores.

**A graph missed by the inventory is data orphaned permanently.** Clause: **the rotation refuses to
start while any in-scope graph is unmeasured.**

### 3c. THE FRAMING (§0) — confirm that this is hygiene, not remediation.

## 4. ACCEPTANCE — observable, pass or fail

1. **STAGED AND RESUMABLE.** The rotation can be killed at any point and resumed, and the graph is
   **fully readable at every intermediate state**. Proven by killing a real run mid-way, reading
   every fact, and resuming to completion.
2. **PARTIAL-FAILURE RECOVERY PER ROW.** A row's new `encrypted_dek` and its `key_version` bump
   land in **one atomic write**. A row is either fully v1 or fully v2 — never a v2 stamp over a v1
   envelope, which would be silent unreadability.
3. **BOTH DEK KINDS.** Every fact carries **two** wrapped keys — `encrypted_dek` **and**
   `driving_utterance_dek`. **A plan sized by fact count is half-sized.** Known surface:

   | graph | value | utterance | total |
   |---|---|---|---|
   | 7691 | 14 | 14 | **28** |
   | 7690 | 13 | 13 | **26** |
   | 7689 | 11 | 11 | **22** |
   | **known total** | | | **76** |

   **Acceptance requires the count of re-wrapped envelopes to equal the count of envelopes found —
   asserted, not assumed.**
4. **DECRYPT PROOF PER GRAPH, PER OWNER, THROUGH A REAL READ PATH.** Owner keys are independently
   derived, so one owner proves nothing about another. Minimum: a `household` fact, the single
   `bill`-owned fact on 7691 (a one-row owner is the easiest to strand silently), a `maya` and a
   `sam` fact, at least one `driving_utterance_dek`, and one fact on the frozen 7689.
   **The proof must run through a real read path** (e.g. `memory_engine/recall.py:223`) — **a direct
   `decrypt_fact_value` call proves the primitive and not the wiring.**
5. **ANTI-VACUITY.** With the OLD master, a re-wrapped row must **fail** to decrypt. A proof that
   passes under both keys has proven nothing about the rotation.
6. **NO DUPLICATE WRITES.** `harness/fact_change.py` compares against current state by decrypting
   it; if a fact is unreadable it reads as absent and the system **writes a duplicate**. Acceptance
   includes a fact-change run post-rotation showing **zero** new rows for facts that already exist.

## 5. CONSTRAINTS — what must not regress

* **The frozen demo (7689) must still open.** It is the fallback; VD-63 froze it and any touch needs
  Bill's explicit unfreeze.
* **No ciphertext is ever rewritten.** Only the DEK envelope and `key_version` change. The value
  ciphertext is untouched, so a failed re-wrap can never corrupt data — only orphan it.
* **No key material in logs, output, commit messages, or documents.** Digests only, as throughout
  FM 20 and FM 21.

## 6. WHAT'S ALREADY DONE — do not redo

**FM 21's inventory** (§1's site list, the 76-envelope count, the two key domains, the absent
roadmap key, the no-backups finding, the `key_version` discovery). **It is a survey, not a build,
and its three unmeasured graphs are its stated limit.**

---

## AMENDMENT 2 — RULINGS 5-7 LANDED (FM 27, 2026-08-14)

### RULING 6 — THE BLOCKING DEFECT: FAIL CLOSED, NEVER MINT

> **`_load_or_create_master_key`'s mint-on-absence dies. New structural rule on the REAL
> startup path of every lane: encrypted data exists + expected key unavailable ⇒ FAIL
> CLOSED — refuse to start the crypto layer, name the graph and the missing domain; NEVER
> mint or substitute. Fresh EMPTY store + no key ⇒ may initialize under the sanctioned
> creation procedure. Acceptance is structural on real startup, not a helper test.**

**THE SANCTIONED CREATION PROCEDURE, defined:** `provision_master_key()` — and only it — may
bring a key into existence, and it is (1) **deliberate**: never called from any encrypt/decrypt
or startup path, operator-invoked only; (2) **logged**: emits a WARNING-level provision record
naming the path, the graph, and the store-verification outcome; (3) **sentinel-written**: a
`.master_key.created` sentinel lands beside the key so a later disappearance is distinguishable
from a fresh install *with no database available at all*. Provision REFUSES when the sentinel
exists or the configured graph holds ciphertext; an unverifiable store (no graph configured)
falls through to the sentinel signal alone — HA-51's precedent — and the provision record says
the store was unverified.

**PER-LANE STATUS AT THIS AMENDMENT — measured, not assumed:**

| tree | mint-on-absence | state |
|---|---|---|
| `~/hip-roadmap` | never minted on load (OB5) | **HARDENED BY FM 27**: refusal now names graph + domain; provision gains sentinel + sealed-data refusal (it previously had NEITHER — a deleted key + a provision call would have minted over sealed data) |
| `~/hip-vo`, `~/hip-nc`, `~/hip-nc2` | guard landed at HA-51 (`8fd0b52`) | **fail-closed on sealed data/sentinel — RESIDUAL NAMED, not hot-edited**: the empty-store mint remains IMPLICIT inside `_load_or_create_master_key` rather than a deliberate procedure; filed with ruling 7's finding for that lane's next capability (three live branches at 21:40 was judged the wrong moment to edit them from the FM lane) |
| `~/hip-cutover-demo` | OB5 lineage, provision unhardened | **FROZEN (VD-63)** — recorded, untouched; its graph 7690 is separately under FM 26's forensic hold |
| `~/hip-dev` | **NAKED `_load_or_create_master_key`, no guard at all** | **FROZEN fallback, not a lane** — the worst residual on the machine, recorded and deliberately untouched |

### RULING 5 — THE ROTATION INVENTORY, REBUILT AS THE MAP THE ROTATION MUST READ

**graph → encrypted data → required key/domain → consuming services** (FM 21 + FM 24's
measurements; hashes are sha256[:12] of key bytes):

| graph | encrypted data | required key / domain | consuming services |
|---|---|---|---|
| 7687 (hip-harness) | yes — Fact ciphertext | `4b1451f0b69e` / **hip-harness domain** (matches its on-disk key ✓) | hip-harness tooling, dashboards |
| **7688 (roadmap)** | **UNMEASURED-BY-DESIGN** — credential lives only in the operator's shell, never on disk | roadmap domain — **no key file on disk (absent by measurement, FM 21)** | roadmap lane services, batteries |
| 7689 (frozen demo) | yes | `9d1e52699499` / hip-dev domain | frozen demo (fallback; not a lane) |
| **7690 (cutover)** | yes — **26 envelopes** | **⚠ NONE of the on-disk masters opens it** (`~/hip-cutover-demo` holds `9d1e52699499`, which does NOT open its own graph) | cutover demo dashboard — **UNDER FM 26's FORENSIC HOLD; nothing touches this graph** |
| 7691 (hip-vo) | yes | `4b1451f0b69e` / **hip-harness's domain — hip-vo has NO key file at all** (ruling 7's finding) | voice_https_orch, hip-vo lane |
| **7692** | **UNMEASURED-BY-DESIGN** — needs an owner before it needs a survey (FM 24) | unknown | none declared |

**THE REFUSAL CLAUSE:** the rotation tool, when built, **reads this map and REFUSES TO START
while any row it would touch is UNMEASURED** — and the two unmeasured rows are marked
**unmeasured-BY-DESIGN with their unblock conditions** (7688: operator supplies the shell
credential and re-runs FM 24's survey; 7692: Bill assigns an owner), so the refusal is informed
rather than a dead end. A rotation that runs against an incomplete map is how 7690's stranded
envelopes happen at scale.

### RULING 7 — THE ARCHITECTURE FINDING, FILED NOT FIXED

**hip-vo's graph (7691) depends on hip-harness's key domain** — the crypto-layer face of the
TD-V-032 interpreter/config-domain mismatch family; filed there (TD-V-035 in hip-vo's register).
**THE PROHIBITION, recorded verbatim in the filing: this is NEVER fixed by copying keys between
trees** — a copied key merges two domains permanently and silently, which is the 7690 failure
shape voluntarily repeated. **The intended graph/key ownership model is a BILL DESIGN RULING,
staged here as OPEN:** one domain per lane with per-lane key files? one household domain with
per-graph derivation? — not a session's call, and the rotation's domain boundaries depend on
the answer.
