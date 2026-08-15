# DISPATCH_FM27 — key lifecycle fails closed: never mint; the map rebuilt; the finding filed
Status: **BUILT — LANDED** — ruling 6 enforced on this lane's real path with 7 structural twins; rulings 5 and 7 landed as records
Reconciled-Against: `565318a` (`~/hip-roadmap` @ `roadmap`)
Dispatch: FM 27
Date: 2026-08-14 21:48 (Mountain)
REQ: **`REQ_MASTER_KEY_ROTATION` Amendment 2** (`2d1c9eb`) — landed **BEFORE any code**
Constraint honoured: **7690 is under FM 26's forensic hold — this dispatch touched CODE and DOCS
only; no twin, probe, or tool went near that graph** (the twins' store is a throwaway temp dir
with the graph env cleared).

---

## 0. THE EXCEPTION LINE

```
FM 27 — key lifecycle fails closed: never mint; map rebuilt; finding filed
COMPLETE WITH FINDINGS — 3 ITEMS FILED, NOTHING BLOCKING
```

**Also the FIRST live scoped claim:** this dispatch's own claim (`a6d9971`) was made with FM 25's
new tool — `.hip-scope` written atomically, verified against ownership (7688/7688 agree), and
**the build commit then went through FM 23's guard UNLOCKED, in-scope, and passed** — the
claim→scope→guard chain exercised end to end on the live board for the first time.

---

## 1. RULING 6 — FAIL-CLOSED TWIN RESULTS, on the REAL startup path

**Where the defect actually was on this lane:** `_load_master_key` already refused (OB5) —
**`provision_master_key` was the hole.** It checked nothing: a deleted key plus a provision call
would have minted a fresh key over sealed data — the exact orphaning OB5 stopped, arriving
through the sanctioned door.

**Built:** refusals now **name the graph and the missing domain** (and whether the sentinel says
a key *was* here — upgrading "missing" to "was here, now gone"); the **sanctioned creation
procedure** is `provision_master_key()` alone — deliberate (no automated caller; verified: only
doc references exist), **logged** (a WARNING provision record naming path, graph, and
store-verification outcome), **sentinel-written** (`.master_key.created`, HA-51's shape); it
**refuses on a present sentinel or graph ciphertext**, and an unverifiable store falls through to
the sentinel signal alone with the record saying so — HA-51's precedent, mirrored not reinvented.

**Twins — 7/7, driven through `encrypt_fact_value`/`decrypt_fact_value`/`provision_master_key`,
the same calls a lane's first real turn makes; no seam injects the condition under test:**

| twin | result |
|---|---|
| **T1** one encrypted row sealed, key file DELETED → real decrypt call **REFUSES**, names graph + domain + "a key existed here and is now gone", **no new key minted** | **PASS** |
| **T2** empty store → real encrypt call **refuses** (startup never mints, even empty) | **PASS** |
| **T2** sanctioned init succeeds: deliberate + **logged** (provision record asserted from caplog) + **sentinel written** (says the store was UNVERIFIED, honestly) → then the real path round-trips | **PASS** |
| **T3** sentinel present + key missing → **BOTH doors refuse** — startup *and* provision (the closed hole) | **PASS** |
| **T3b** deliberate sentinel removal reopens the sanctioned door — the documented escape works | **PASS** |
| unit (labelled as such): graph-ciphertext branch refuses; unresolved-graph is not permission | **PASS ×2** |

**Regression: the key suites 45/45** (`test_key_hygiene`, `test_session_content_key`, + the new file).

**Per-lane status, measured — the honest boundary of "every lane":**

| tree | state |
|---|---|
| `~/hip-roadmap` | **hardened here** — both doors fail closed |
| hip-vo / hip-nc / nc-b0 | HA-51's guard already fail-closed on sealed data/sentinel; **residual named, not hot-edited**: the empty-store mint is implicit, not the deliberate procedure — filed in TD-V-035 for that lane's next crypto capability (editing three live branches cross-lane at 21:40 repeats today's collision pattern) |
| `~/hip-cutover-demo` | OB5 lineage, provision unhardened — **FROZEN (VD-63), recorded, untouched** |
| `~/hip-dev` | **naked mint, no guard at all — the worst residual on the machine** — frozen fallback, not a lane; recorded, untouched |

## 2. RULING 5 — THE REBUILT MAP (in the REQ, with the refusal clause)

`graph → encrypted data → required key/domain → consuming services`, from FM 21 + FM 24:
7687→hip-harness domain ✓ · **7688 UNMEASURED-BY-DESIGN** (credential only in the operator's
shell; unblock = supply it and re-run FM 24's survey) · 7689→hip-dev domain (frozen) ·
**7690→NONE of the on-disk masters opens it, 26 envelopes, forensic hold** ·
7691→**hip-harness's domain, hip-vo has no key file** · **7692 UNMEASURED-BY-DESIGN** (needs an
owner before a survey). **The rotation tool, when built, reads this map and REFUSES TO START
while any row it would touch is unmeasured** — and the map says *why* each unmeasured row is so,
so the refusal is informed rather than a dead end.

## 3. RULING 7 — FILED, NOT FIXED

**TD-V-035** in hip-vo's register (`3efa3e7`): 7691 depends on hip-harness's key domain; hip-vo
holds no key file; **"retire hip-harness" is a data-availability decision**. The prohibition
recorded verbatim: **never fixed by copying keys between trees** — a copied key merges domains
permanently, the 7690 shape repeated voluntarily. **The ownership model is staged as an OPEN Bill
design ruling in the REQ** (per-lane domains vs one household domain with per-graph derivation);
the rotation's boundaries depend on the answer.

## 4. FILINGS

1. **TD-V-035** (ruling 7 + the vo-lineage ruling-6 residual, one row, both halves).
2. **`~/hip-dev`'s naked mint** — recorded in the REQ's per-lane table; frozen, untouchable,
   and therefore a standing hazard the unfreeze decision should weigh.
3. **The provision hole this dispatch closed existed on the OB5 lineage since OB5 landed** —
   the load-path fix trained everyone to look at the load path; the sanctioned door had no
   guard. Same lesson as HA-89's `export` guard: the obvious fix-site is not the only door.

## 5. CLAIM IMPACT

```
CLAIM IMPACT: none
```

## 6. VERIFIED

- Machine gate ✓; claim `a6d9971` **first** (scoped, FM 25's tool); amendment `2d1c9eb`
  **before** code; build `565318a`; TD filing `3efa3e7` (hip-vo, commit-around foreign dirty
  docs, explicit pathspec); every push under the lock; 7690 untouched throughout.
