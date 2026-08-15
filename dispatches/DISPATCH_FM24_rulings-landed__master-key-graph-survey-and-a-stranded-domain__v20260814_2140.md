# DISPATCH_FM24 — rulings landed in two REQs; master-key graph survey
Status: BUILT
Reconciled-Against: roadmap @ `e4b61d9`; live graph reads 2026-08-14 21:40 MDT

COMPLETE WITH FINDINGS — 4 ITEMS FILED, ONE NEEDS BILL SOON

**S1 docs-only. S2 read-only, NO credential minted.** Keys reported by SHA-256 prefix; no key
material appears here.

---

# S1 — RULINGS LANDED

## `REQ_CONVERSATION_EPISODE` (NC 18, `67c0ad6`) — all four open questions ruled

| # | ruling |
|---|---|
| **Q1** | **`IDLE_TTL = 7 min`, `ABSOLUTE_TTL = 30 min`** — fixed values, no longer brackets. The prior "tuning params ≈ 5–10 min" wording is kept visible and marked superseded. |
| **Q2** | **IN-PROCESS FOR THIS STAGE.** Recorded as a *stage* decision, not a permanent one. |
| **Q3** | **DEFERRED TO B2** — with a deferral record, below. |
| **Q4** | **DETERMINISTIC NOTICE; a silent fresh episode is PROHIBITED.** |

**Q3's deferral is recorded rather than left implicit**, because `branch_info` is already in the
shape table while its semantics are not ruled — and a typed field with no ruled meaning is exactly
how a placeholder becomes a de-facto behaviour, decided by whoever writes the first branch-setting
code. **Until B2: `branch_info` is CARRIED AND NOT INTERPRETED.** Writing it is permitted; branching
on it is not. **A build that acts on it before B2 has taken Q3's decision by default.**

**Q4 is written as the invariant it is.** The prohibited behaviour is named precisely: a silent new
episode that **reinterprets the referent**. If *"it"* or *"that one"* resolved against the old
episode's working frames, a silent restart re-binds those words while the member believes the
conversation is continuous — **a wrong answer delivered with full confidence.** E3's acceptance is
tightened: the notice must fire, and a test must prove a referent from the expired episode is not
silently resolved afterwards.

## `REQ_MASTER_KEY_ROTATION` (FM 22, `6fbf60b`) — scope ruled

| # | ruling |
|---|---|
| **3a** | **BOTH DOMAINS, SEQUENCED DELIBERATELY** |
| **3a(ii)** | **`~/hip-roadmap` needs an explicit key-domain decision before first encrypted use — NO SILENT THIRD MINT** |
| **3c** | **HYGIENE, CONFIRMED** — not remediation |

**"Sequenced" is written as a safety property, not scheduling:** one domain at a time, each proven
before the next, because a concurrent rotation makes a partial failure impossible to attribute — a
stranded DEK could belong to either run. **But sequencing the domains does not license splitting
one:** the two *copies* of `9d1e52699499` must move together.

**"No silent third mint" is given teeth:** `_load_or_create_master_key()` creates on absence, so
`~/hip-roadmap`'s first encrypted write would mint a third domain that nobody decided. The clause
forbids that write until the domain is ruled, and names the buildable form — **a guard that REFUSES
rather than creating** — while explicitly not building it.

**3b (unmeasured graphs) was NOT ruled and stays open** — it is answered by evidence, not decision.
That is S2.

---

# S2 — THE SURVEY (ruling 10)

## Per-graph result

| graph | reachable with a SANCTIONED store? | encrypted rows | envelopes | key_version | master domain |
|---|---|---|---|---|---|
| **7687** | **YES** — `~/.hip-secrets/neo4j-7687.password` | 11 facts (203 nodes total) | **22** (11 value + 11 utterance) | `1` | **`4b1451f0b69e`** |
| **7688** | **NO — UNREACHABLE-BY-DESIGN** | — | — | — | — |
| **7692** | **NO — UNREACHABLE-BY-DESIGN** | — | — | — | — |

**7687 is FM 11's "203 nodes, and no lane declares it"** — now measured: it holds real encrypted
household data and depends on the **hip-harness** key domain.

### 7688 / 7692 — UNREACHABLE-BY-DESIGN, and what would be needed

**No credential was minted, guessed, or derived.** Every sanctioned store was tried and refused.
`~/hip-roadmap/.env.dev` pins **no** `NEO4J_PASSWORD` — that lane takes it from the operator's shell
**by design** (its own comment says so), so no file on this machine holds 7688's credential. 7692 is
declared by no lane at all.

**What would be needed:** for **7688**, the operator supplies the password in the environment and
re-runs this survey — nothing else. For **7692**, a prior question must be answered first: **which
lane owns it, if any.** A credential cannot be sanctioned for a graph with no declared owner.

**DISCLOSED HONESTLY: my probe loop triggered `Neo.ClientError.Security.AuthenticationRateLimit` on
both ports.** Trying several stores in sequence against one graph is exactly the TD-V-006 pattern
HA-65 recorded. **It self-clears (~180 s) and nothing was damaged**, but it is a real side effect of
how I surveyed, and the method note is: **probe once per graph with the store that should own it,
never iterate stores.**

> **⚠⚠ THIS FINDING IS FALSE. CORRECTED BY FM 26 (2026-08-14), same session, same author.**
> **7690's 13 rows are `key_version = 2` — a DIFFERENT envelope scheme (`harness/partition_crypto.py`),
> sealed under `~/hip-keys/*.seal.key`, not under an HKDF derivation of `.master_key`. FM 26 decrypted
> ALL 13 through the demo's own read path: 13/13, zero failures.** The v1 masters returning
> `InvalidToken` is CORRECT behaviour, not evidence of loss. **Nothing was stranded; no master key is
> missing.** The error was mine: I tested exhaustively (13 rows x 3 owners x 2 domains) inside a FALSE
> FRAME, and never checked `key_version` — the one field that says which scheme applies.
> **Left standing per the annotate-never-rewrite rule; FM 26 is the correcting record.**

## ⚠ FINDING THAT OUTRANKS THE SURVEY — **7690's DEKs OPEN WITH NEITHER MASTER KEY ON DISK**

The survey's domain check was run across every graph, and it did not come out as FM 21's
tree-based inference predicted. **Domains follow the GRAPH, not the tree:**

| graph | master domain | the tree that "owns" it holds… |
|---|---|---|
| 7691 (`~/hip-vo` lane) | **`4b1451f0b69e`** | hip-vo has **no key file at all** — it depends on **hip-harness's** domain |
| 7689 (frozen demo) | `9d1e52699499` | matches `~/hip-dev` ✓ |
| 7687 | `4b1451f0b69e` | matches `~/hip-harness` ✓ |
| **7690 (cutover demo)** | **NONE OF THE MASTERS ON DISK** | `~/hip-cutover-demo` holds `9d1e52699499`, which **does not open its own graph** |

**Tested exhaustively, not sampled: all 13 facts, all 3 owners (`household` 6, `maya` 4, `sam` 3),
against both known domains. Zero unwrap.** The obvious innocent explanation was ruled out first —
**`_HKDF_INFO_PREFIX` is byte-identical (`hip-fact-envelope:v1:`) in all five trees**, so this is not
a derivation mismatch. **Only three `.master_key` files exist anywhere under `~`.**

**7690 is not an abandoned graph.** `~/hip-cutover-demo/.hip-graph` declares it: *"This checkout
writes bolt://localhost:7690. The cutover demo lane. 7690 is its canonical battery graph (CLAUDE.md).
Provisioned by FM 9 on Bill's ruling 3."*

**The likely mechanism is the one this REQ exists to prevent, already realised:**
`_load_or_create_master_key()` **mints a key when none is present**, so a lost or moved key file is
silently replaced and every pre-existing DEK is stranded. `_refuse_if_sealed_data_exists()` and
`MasterKeyLostError` exist to catch exactly that — and **no sentinel file is present in any tree's
`data/encryption/`** (each contains only `.master_key`), so the guard had nothing to fire on.

**WHAT I HAVE NOT ESTABLISHED, stated so this is not over-read:** I did **not** prove the demo reads
these rows. **VD-63's certifying battery was green**, which means either the demo does not decrypt
these 13 facts on its green path, or it was re-seeded after the key changed. **Whether this breaks
the frozen demo is UNVERIFIED** — but 26 envelopes on a declared canonical graph currently have no
key on this machine, and that is true regardless.

**Bearing on the rotation:** a rotation scoped to "both domains" would have **silently skipped 7690
entirely** — its data belongs to neither. **The REQ's refusal-to-start-while-unmeasured clause just
paid for itself.**

## CLAIM IMPACT

**CLAIM IMPACT: none.**

## OPEN — NEEDS BILL

1. **7690's stranded envelopes — the one that needs attention soon.** 26 envelopes on the cutover
   demo's canonical battery graph open with no key on this machine. Is a fourth master archived
   somewhere off this box, or is that data already lost? **Do not let anything re-seed or re-key
   7690 before this is answered** — a re-seed would erase the evidence of what happened.
2. **`~/hip-vo` has no key file and depends on hip-harness's domain** — TD-132's coupling reaching
   the crypto layer. It makes "retire hip-harness" a data-availability decision, not just an
   ownership one.
3. **7688 needs the operator's shell credential** to be measured; **7692 needs an owner** before a
   credential could be sanctioned at all.
4. **No sentinel files exist**, so `_refuse_if_sealed_data_exists()` has nothing to fire on in any
   tree. Minor, and adjacent: `~/hip-cutover-demo/data/encryption` and `~/hip-harness/data/encryption`
   are `drwxr-xr-x` where `~/hip-dev`'s is `drwx------` (the key files themselves are all `0600`).
