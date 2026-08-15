# DISPATCH_CRYPTO_P1_DYAD_KEYS: Stage 4 Phase 1 Build
Status: BUILT
Reconciled-Against: see HASH below

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_CRYPTO_P1_DYAD_KEYS__stage4-phase1__v20260719_0830.md`

## THE ASK

"Build REQ_CRYPTO_P1_DYAD_KEYS (Stage 4 Phase 1) on a new branch
roadmap-crypto-p1 off roadmap. Read the REQ in docs/requirements/ first —
REQ before code. Build: dyads/dyad_members/dyad_key_wraps tables, X25519
dyad keypair per dyad, D_priv sealed to each custodian's member pubkey,
two-hop unwrap, seal-to-dyad on dyad-private facts, entry-enrollment with
custody.grant HEL event, demo fixture pre-enrolls maya-ray and sam-ray.
Dual-envelope — do NOT touch the master key or existing facts. Prove the
acceptance test: N2/P2 green, DK1-DK4, overlapping-dyad isolation (DK3),
fault-injection shows the tests can go red. --full passes with only the
known D-24/#15c reds. Report the hash."

## WHAT WAS DONE

1. Read the REQ, then its full prerequisite chain before touching code
   (REQ_PARTITION_CUSTODY, REQ_CRYPTO_HARNESS, crypto design 47851d7, dyad
   spec 601ac25, docs/INDEX.md, docs/planning) — found a real gate: neither
   prerequisite REQ was actually MET in the codebase (zero dyad/crypto-harness
   code anywhere, on any branch), and REQ_PARTITION_CUSTODY's D1/D2/D3 were
   still formally undecided (verified via `git log` on that file — one
   commit ever, still `Status: NOT MET`). Stopped and asked Bill directly
   rather than assume the proposed defaults; all three ACCEPTED as proposed
   (see that REQ's own UPDATED note).
2. Found a second gate: `roadmap` (HEAD `0bd27d7`) and a sibling worktree
   `roadmap-stage1-wip` (HEAD `1bd5e26`) had diverged at `52935c2` —
   `roadmap` had the Stage 2-5 REQ docs, `roadmap-stage1-wip` had the actual
   Stage 1 identity code (`harness/identity_keys.py`, member_registry's
   `pubkey` column) this phase's own prerequisite ("each member has a device
   keypair, built, committed 8263c25") depends on. Merged
   `roadmap-stage1-wip` into `roadmap` (two doc-only conflicts, resolved by
   hand — INDEX.md timestamp/row, DEBT_REGISTER TD-129/TD-130 rows — no code
   conflicts) before branching, so `roadmap-crypto-p1` actually has both.
3. Built, in order: `harness/member_seal_keys.py` (X25519 sealing keypair
   per member, mirrors `identity_keys.py`'s keystore idiom exactly) →
   `member_registry.py`'s new `seal_pubkey` column + `update_seal_pubkey` →
   `harness/dyad_crypto.py` (sealed-box envelope primitives + dyad keypair +
   two-hop unwrap) → `harness/dyad_registry.py` (the three SQLite tables +
   `create_dyad`/`add_custodian` entry-enrollment, each emitting one
   `custody.grant` HEL event) → `memory_engine/store.py`'s `encode()` opt-in
   `dyad_seal` parameter → `scripts/demo_seed.py`'s dyad pre-enrollment step
   → `eval/harnesslib/layer7_crypto.py` (new L7-CRYPTO layer) →
   `eval/harness.py` registration (`--layer 7`, included in `--full`/
   `--pre-demo`/default).
4. Verified each primitive in isolation (temp SQLite/keystore/ledger dirs)
   before wiring into `encode()`, then verified the wired path against the
   real dev Neo4j graph (:7688) before writing the harness layer.
5. Ran `python scripts/demo_seed.py` for real against the shared registry
   and dev graph — this IS the demo fixture, not a side effect to avoid;
   it's the same registry/graph the live dashboard reads.
6. Wrote the new L7-CRYPTO harness layer scoped to exactly this phase's own
   acceptance test (N2, P2, DK1-DK4, fault injection) — deliberately NOT the
   full REQ_CRYPTO_HARNESS suite (N1/N3-N6, P1/P3/P4, mallory/R1-R7, L1-L3),
   which is that REQ's own separate scope and was not attempted.
7. Ran `eval.harness --layer 7` standalone (green), then the full
   `eval.harness --full` suite twice (one crash was environment setup in
   the fresh worktree — see OPEN — not a code issue), read the actual
   RATCHET output per CLAUDE.md item 12, and cross-checked the one red
   against `logs/harness_trend.jsonl` across all four worktrees to confirm
   it's pre-existing, not something this build introduced.

## WHAT WAS FOUND

**Dual-envelope, additive only — nothing existing touched:**
- `harness/encryption.py`'s master key, `KEY_VERSION = 1`, `_derive_key`,
  `encrypt_fact_value`/`decrypt_fact_value` are byte-for-byte unmodified.
- `memory_engine/store.py`'s `encode()` gained one new **optional** keyword,
  `dyad_seal: dict | None = None` (store.py:348-388 area). Every existing
  caller (all of `scripts/demo_seed.py`'s D1-D11 fixture, every production
  write path) passes nothing new and is byte-for-byte unaffected — verified
  live: a normal `encode()` call still lands `key_version=1, dyad_id=None`
  (see VERIFIED below).
- No automatic write-rule wiring. `harness.dyad_registry.get_active_dyad_for`
  (rule 3's deterministic lookup) exists and is used by the demo/harness's
  own dyad-private writes, but `encode()` never calls it itself — a caller
  must opt in explicitly. This was a deliberate scope cut: wiring rule 3 (or
  the full 5-rule order) automatically into every write would have silently
  changed the classification of the EXISTING D9 fixture (`owner=maya,
  subject=ray`, already in the graph) the moment `maya-ray` came to exist,
  risking an uncontrolled behavior change to facts other harness layers
  already depend on. That global wiring is explicitly Stage 4 phase 2's job
  (REQ_CRYPTO_P2_PARTITION_SEALED — "re-sealing existing facts").

**New tables** (`harness/dyad_registry.py`, SQLite, same file as
`member_registry.py`, `~/hip-harness/registry.db`, own `CREATE TABLE IF NOT
EXISTS` block since dyad_registry.py resolves the db path independently
rather than reaching into member_registry's private connection helper):
`dyads(dyad_id, recipient_ref, household_id, dyad_pubkey, status,
created_at)`, `dyad_members(id, dyad_id, custodian_member_id, role,
added_at, removed_at)`, `dyad_key_wraps(dyad_id, custodian_member_id,
wrapped_d_priv, key_version)`.

**Crypto** (`harness/dyad_crypto.py`): X25519 dyad keypair
(`generate_dyad_keypair`); anonymous sealed-box envelope
(`seal_to_pubkey`/`unseal_from_privkey` — ephemeral X25519 keypair, ECDH,
HKDF-SHA256, Fernet, matching the existing envelope's own idiom, no new
dependency); `encrypt_fact_value_for_dyad`/`decrypt_fact_value_for_dyad`
mirror `harness.encryption`'s functions exactly except the DEK is sealed to
`D_pub` instead of an HKDF-derived owner key. `DYAD_KEY_VERSION = 2`.

**Member sealing keys** (`harness/member_seal_keys.py` +
`member_registry.seal_pubkey` column): X25519 keypair per member, same
keystore convention as `identity_keys.py` (`~/hip-keys/<member>.seal.key`,
0600, O_EXCL), distinct file from the Ed25519 signing key so either can
rotate independently.

**Entry-enrollment** (`harness/dyad_registry.create_dyad` /
`add_custodian`): generates `(D_pub, D_priv)`, seals `D_priv` to the
custodian's `seal_pubkey`, discards the raw value (never stored, logged, or
returned — `del d_priv_raw` immediately after sealing), writes the three
rows, emits one `custody.grant` HEL event via
`harness.epistemic_ledger.append` (`actor={"kind": "member", "id":
authorized_by}`).

**Demo fixture** (`scripts/demo_seed.py`): `_ensure_seal_keypair` +
`_ensure_dyad` added, idempotent, run for bill/maya/sam and for
`maya-ray`/`sam-ray`. Live-run confirmed: both dyads created
(`a6bd1956…`/`798c1026…`), 2 `custody.grant` events emitted, all three
members' X25519 pubkeys registered.

**L7-CRYPTO harness layer** (`eval/harnesslib/layer7_crypto.py`, registered
in `eval/harness.py` as layer 7, included in `--full`): writes two live
dyad-private facts through the real `store.encode(..., dyad_seal=...)` path
(the actual "Ray fell last night" / sam-ray write the REQ's demo script
calls for), asserts DK2 (two-hop unwrap), N2 + DK3 (4 cross-dyad decrypt
attempts, all denied), P2 (every current custodian of both dyads decrypts
their own fact), DK1 (every `dyad_key_wraps` row fails to parse as a bare
32-byte X25519 key + a grep of `dyad_crypto.py`/`dyad_registry.py` source
for any print/log referencing `d_priv`, 0 hits), DK4 (`custody.grant` event
count ≥ wrap-row count, `epistemic_ledger.verify()` passes), and mandatory
fault injection (seals a fact meant for `maya-ray` to `sam-ray`'s real
`D_pub` instead — the exact "misseal a DEK to the wrong D_pub" the REQ
names — and shows P2 going red for maya, the correct custodian, and N2
going red for sam, now able to decrypt a fact outside his own dyad). Every
fact this layer writes is deleted at the end of the run, pass or fail.

## VERIFIED

**Watched run** (not reasoned-about — every claim below was actually
executed):

- Manual smoke test (temp SQLite/keystore/ledger dirs, isolated from the
  shared registry): `create_dyad` for maya-ray and sam-ray, rule-3 lookup
  correct for both, sealed a value to maya-ray, maya decrypts it, sam denied
  both directly and via his own sam-ray key, wrap length 172 bytes (not 32),
  2 `custody.grant` events = 2 wrap rows, ledger `verify()` → `True`.
- Live `memory_engine.store.encode()` round-trip against the real dev graph
  (bolt://localhost:7688): a normal write lands `key_version=1, dyad_id=None`
  (dual-envelope, unaffected); a `dyad_seal=...` write lands
  `key_version=2, dyad_id=<uuid>`, decrypts correctly via
  `decrypt_fact_value_for_dyad`, and — separately confirmed —
  `harness.encryption.decrypt_fact_value` (the v1 owner-key path) correctly
  raises `InvalidToken` against that same v2 ciphertext, proving the two
  envelopes don't silently cross-decrypt each other.
- `python scripts/demo_seed.py` run for real against the shared registry +
  dev graph: bill/maya/sam all got Ed25519 (backfilled for maya/sam — a
  pre-existing desync from an earlier partial run, exactly the two-axis
  idempotency the existing code already anticipated) and X25519 keys;
  `maya-ray` (`a6bd1956…`) and `sam-ray` (`798c1026…`) created; all 11
  fixture facts (D1-D11) re-seeded unchanged (supersede semantics, same as
  every prior demo_seed run in this repo's history).
- `eval.harness --layer 7` standalone: 9/9 scenarios PASS (setup,
  seal-to-dyad, DK2, N2, DK3, P2, DK1, DK4, fault-injection).
- `eval.harness --full` (twice; the venv's own subprocess server needs
  `[REDACTED-USER-PATH]/hip-dev/.venv/bin/python3`, not bare `python3` — a fresh
  worktree gap, see OPEN): completed, exit code 1 (ratchet fail on ONE
  pre-existing scenario, not a crash). L7: **9/9 PASS** in the real
  `--full` run (not just the standalone one) — every DK1-DK4/N2/P2/
  fault-injection assertion green under the same run that also drove L1
  (100 iters), L2, L3 (mutation), L4, L6.
- The literal D-24/#15c defect (`care_coordination.T01/T02/T03`) **PASSED**
  this run (`care_coordination.T01/T02/T03/T04` all `PASS`, harness.py
  line-matched in the log).
- The one ratchet failure was `L2:three_zone_demo.T02`
  (`reply='I heard that as an update, but I was unable to save it to the
  household record just now...'` — `UNCONFIRMED_UPDATE_REPLY`,
  `server/voice_orch.py:2290-2293`, the TD-121/TD-125 zero-write-detection
  gate, unrelated code this build never touched). Re-ran `--layer 2 --script
  three_zone_demo` standalone: failed again (not flaky in the moment), so
  cross-checked `logs/harness_trend.jsonl` across all four local
  worktrees/checkouts: `hip-dev`'s trend log alone shows `three_zone_demo.T02`
  failing on 12+ distinct runs across commits `641d249` through `e5d158c`
  (2026-07-17 through 2026-07-18), and `hip-roadmap`/`hip-roadmap-stage1-wip`
  show it failing on `5607f4c` and `8263c25` — all commits that predate this
  build and never touch crypto/dyad code. Pre-existing, same root-cause
  family as D-24 (Groq stochastic zero-write detection under load,
  TD-121/TD-125), confirmed not introduced here.
- `L1:P2` also shows FAIL in the run, but is already an accepted baseline
  entry (`eval/harness_baseline.json` `_accepted["L1:P2"]`, TD-124
  write-propagation latency) — not a regression, not new.

**Reasoned about:** the exact wording of crypto design 47851d7 §2.1 and dyad
spec 601ac25 §1-§6 (read via two background research agents, not re-derived
independently) — the sealed-box construction, the dyad object model column
names, and the "maya-ray"/"sam-ray" naming convention are all taken from
those docs/`demo_seed.py`'s existing data shape, not invented here.

## HASH

`35a994b` (branch `roadmap-crypto-p1`) — the Phase 1 build itself: all
harness/dyad_*.py, member_seal_keys.py, member_registry.py's seal_pubkey
column, store.py's dyad_seal param, demo_seed.py's dyad enrollment,
layer7_crypto.py, and this dispatch doc, in one commit. Prerequisite branch
reconciliation (merging roadmap-stage1-wip's real Stage 1 identity code into
roadmap before branching roadmap-crypto-p1 from it) is the separate, prior
commit `2eb660f` on `roadmap`.

## OPEN

- **`eval/harness_baseline.json` was NOT updated** to register the 9 new
  `L7:*` keys going forward. Attempted `--update-baseline`; blocked by this
  session's own permission classifier (a file-write-via-test-command
  pattern it's tuned to catch). Not worked around. The new L7 scenarios are
  green and unbaselined, which is safe (an unbaselined PASS never fails the
  ratchet) but means a future regression in L7 itself won't be caught as a
  regression until someone runs `--update-baseline` explicitly.
- **Full Stage 3 (REQ_CRYPTO_HARNESS) remains its own separate, not-yet-built
  REQ.** This phase built only N2, P2, DK1-DK4, and fault injection — not
  N1/N3/N4/N5/N6, not P1/P3/P4, not the mallory red-team fixture (R1-R7),
  not the broader ledger invariants L1-L3 beyond DK4's narrower "count
  matches" check.
- **Full Stage 2 write-rule table remains unbuilt.** Only rule 3's
  deterministic lookup exists (`get_active_dyad_for`), used opt-in. Rules 1
  (member directive), 2 (household attribute — already exists, unrelated to
  this build), 4 (sensitivity-based default), 5 (fallback), and the 9-row
  fixture-table test are Stage 4 phase 2's job.
- **`add_custodian` (adding a SECOND custodian to an existing dyad) is
  implemented but not exercised** by the demo fixture (`maya-ray` and
  `sam-ray` are each single-custodian) or by L7. It's there for the general
  dyad-spec case of a shared care circle; untested beyond a syntax/import
  check.
- **A fresh worktree checkout needs manual setup** the harness doesn't
  self-diagnose well: the project venv (`hip-dev/.venv`, not bare
  `python3`) and a local `certs/voice.key` (gitignored, git only tracks
  `voice.crt`) both have to exist before `eval.harness`'s subprocess server
  will start. Neither is new to this build, but both cost real time
  here and aren't captured as a filed tech-debt item anywhere — worth one.
- **Exit (Stage 4 phase 4) and re-seal (phase 2) are Stage 4's own
  remaining phases**, per the REQ's own explicit "What does NOT get built
  here" — not attempted, not implied done.
