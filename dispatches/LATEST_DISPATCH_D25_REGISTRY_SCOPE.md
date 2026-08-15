# DISPATCH_D25_REGISTRY_SCOPE
Status: BUILT
Reconciled-Against: 605bb79

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_CRYPTO_P1_DYAD_KEYS__stage4-phase1__v20260719_0830.md`
(DK4 is that REQ's acceptance invariant; this dispatch restores it after the
crypto-p2 merge broke its counting provenance, not its crypto).

## THE ASK

Two dispatches, quoted verbatim. First, the evidence pull (2026-07-21, run on
Bill's MacBook while the mini was offline):

> D-25 MAC-SIDE EVIDENCE PULL — read-only, no fixes, no commits, no push. The
> mini is offline; work only with what exists on THIS machine. [...] STEP 2.
> SUSPECT (a) — CODE READ [...] List every code site that INSERTs into
> dyad_key_wraps, including the f94fb11 epoch and care-team key paths. For
> each site state whether a custody.grant ledger emit is on the same code
> path. [...] STEP 3. SUSPECT (b) — DB SHARING [...] print the resolved
> HIP_REGISTRY_DB path each would use. Same file = suspect (b) live.

Then the fix (2026-07-21, on the mini):

> D-25 FIX — verify first, then build. Branch: roadmap (the unpushed b151267
> merge). Do NOT push until DK4 is green. [...] STEP 2. BUILD:
> a. Add HIP_REGISTRY_DB to .env.dev pointing at a per-checkout registry
> path, mirroring how this checkout isolates Neo4j 7688.
> b. Add a harness guard beside the existing NEO4J_URI guard: refuse to run
> Layer 7 when HIP_REGISTRY_DB is unset or resolves to the shared
> ~/hip-harness/registry.db default.
> c. Move _emit_custody_grant inside the same transactional boundary as the
> dyad_key_wraps INSERT, both sites in dyad_registry.py.
> STEP 3. VERIFY. Run Layer 7 single-layer, not --full. Acceptance: 19/19
> with DK4 green. If red after two attempts, report and stop.

## WHAT WAS DONE

1. **Evidence pull (Mac, read-only).** Located the merge: `b151267` existed
   only on the mini (origin tips were `roadmap=f94fb11`,
   `roadmap-crypto-p2=7b1f087`). Enumerated every `dyad_key_wraps` INSERT in
   both merge parents' trees via `git grep` against the commit objects.
   Resolved `_db_path()` and the HEL ledger dir live from three checkouts.
2. **Fix (mini).** Environment verified first (Neo4j :7688 `RETURN 1 -> 1`
   via bolt driver — cypher-shell is not installed on the mini; ollama
   :11434 and :11435 both up; `.env.dev` present). Then the three changes
   below, committed as a checkpoint before verification.
3. **Verify.** Reseeded via `scripts/demo_seed.py` into the fresh
   per-checkout registry (11/11 facts, maya-ray + sam-ray enrolled), ran
   `--layer 7` single-layer, then negative-tested both guard refusals.
4. **Closeout.** BACKLOG D-25 row rewritten to RESOLVED with root cause and
   fixing hash; this dispatch doc.

## WHAT WAS FOUND

**Root cause — a registry/ledger provenance split, suspect (b), sharper than
filed.** `dyad_registry._db_path()` (harness/dyad_registry.py:49-55 at
7b1f087) honours `HIP_REGISTRY_DB` and defaults to the home-anchored
`~/hip-harness/registry.db` — machine-global. The custody ledger
(`harness/epistemic_ledger.py:99-100`) defaults to `ROOT / "ledger"` —
checkout-local. On the mini, `~/hip-roadmap/.env.dev` pinned
`HIP_REGISTRY_DB` to `$HOME/hip-dev/data/registry.db` (copied from hip-dev's
env), so wraps accumulated in a registry shared with the hip-dev checkout
while grants landed in `~/hip-roadmap/ledger/`. DK4
(eval/harnesslib/layer7_crypto.py: grants >= wraps) counted 3 hip-dev-seeded
wraps against 2 roadmap-local grants: 18/19, DK4 red, crypto intact.
`demo_seed.py`'s dyad step (scripts/demo_seed.py:292-295) skips creation when
the dyad already exists in the shared DB, so the inheriting checkout never
emits the missing grants — the mismatch is stable, not transient.

**Suspect (a) cleared by code read.** Exactly two INSERT sites into
`dyad_key_wraps` exist in both merge parents — `create_dyad` and
`add_custodian` (7b1f087:harness/dyad_registry.py:303 and :375) — and both
call `_emit_custody_grant` on the same path (:308, :380). No other writer
exists in either tree; f94fb11's care-team/epoch key classes
(`care_team_key_wraps`) are ratification docs only, no code. One latent
weakness noted: the emit ran after the SQLite transaction committed, so a
crash in that window could orphan a wrap (one-off, not the systematic
18/19 — but closed anyway, change 3).

**The three changes (all at 605bb79):**
1. `.env.dev` (gitignored — this change lives on the mini, not in git):
   `HIP_REGISTRY_DB="$HOME/hip-roadmap/data/registry.db"` — the registry now
   lives and dies with the checkout whose ledger records its grants.
2. `eval/harness.py` (after run-layer resolution, beside the NEO4J_URI
   guard's refusal idiom): when 7 is in `run_layers`, refuse if
   `HIP_REGISTRY_DB` is unset or resolves to `~/hip-harness/registry.db`,
   before any seeding can touch the shared file.
3. `harness/dyad_registry.py`: `_emit_custody_grant` moved inside the
   `with ... conn:` transaction at both INSERT sites — a failed emit now
   rolls back the wrap row.

## VERIFIED

- **Watched run:** `--layer 7` on the mini at 605bb79 against the dev graph
  (:7688) and the fresh per-checkout registry: `== L7: 19/19 (0 flaked,
  0 skipped)`, DK4 PASS (count + hash-chain verify), PS1/PS2 PASS with all
  four fault injections flipping red, DISC 1/1, SCHEMA 1/1, VOICE 1/1,
  `RATCHET PASS` — first attempt, no retries. Both new guard refusals
  watched fire: `env -u HIP_REGISTRY_DB` → "REFUSING: HIP_REGISTRY_DB not
  set...", `HIP_REGISTRY_DB=$HOME/hip-harness/registry.db` → "REFUSING:
  ... resolves to the shared demo registry..." Seed run watched: 11/11
  facts, both dyads created with custody.grant emitted.
- **Reasoned about:** that the mini's 18/19 was produced by the hip-dev
  registry path specifically (inferred from `.env.dev`'s previous value and
  the 3-vs-2 counts in the D-25 filing; the failing run itself was not
  re-executed against the old path). The rollback behavior of change 3 is
  from reading the context-manager semantics, not from injecting an emit
  failure live.

## HASH

`605bb79` (fix: guard + transactional emit; .env.dev change is gitignored,
described in the commit message), `8df137e` (BACKLOG D-25 → RESOLVED).
Pushed `f94fb11..8df137e` on `roadmap`.

## OPEN

- ~~The guard refuses only the unset/shared-demo cases per the dispatch's
  explicit scope; a future checkout that copies another checkout's
  `.env.dev` (the actual D-25 vector) still passes it.~~ **CLOSED at
  32d393a (2026-07-21):** the guard now also refuses when the resolved
  `HIP_REGISTRY_DB` is outside the checkout root — negative-tested live
  against `~/hip-dev/data/registry.db`, Layer 7 re-run 19/19 with DK4
  green after the change.
- `harness_baseline.json` still lacks the L7 scenario keys
  (`--update-baseline` remains blocked, carried over from the P1 dispatch's
  OPEN).
- The demo checkout's own registry/ledger pairing on the mini was not
  audited — only the dev/roadmap side was.
- Untracked `STAGE1_RUN_SUMMARY.md` in `~/hip-roadmap` observed during this
  work; disposition is Bill's call (reported separately in the closeout).
