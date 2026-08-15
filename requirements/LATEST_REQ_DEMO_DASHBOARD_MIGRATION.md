# REQ_DEMO_DASHBOARD_MIGRATION
Status: NOT MET
Reconciled-Against: REQ_CRYPTO_P3_OPERATOR_BLIND__stage4-phase3__v20260724_1129 (PRE-DESTRUCTION AUDIT FOR PART (c), same session); REQ_CRYPTO_P2_PARTITION_SEALED (MET, the sealing mechanism this checkout needs to adopt); AUDIT_MASTER_KEY_FINDINGS__d26-launchd-vs-harness-key-divergence__v20260722_1529.md

## THE REQUIREMENT

Scoped from this session's pre-destruction audit for REQ_CRYPTO_P3_OPERATOR_BLIND part (c). Bill's framing, from the audit dispatch: "the key at ~/hip-dev/data/encryption/.master_key lives in the DEMO checkout, and the demo still runs pre-partition code that seals with it. Destroying it could break the demo." And, scoping this out as its own job rather than a blocker: "Record it as a separate scheduled job, NOT a blocker on #5."

Expanded: `~/hip-dev` (branch `main`, `com.hip.demo.dashboard` launchd job, port 7871, graph `bolt://localhost:7689`) runs `memory_engine/store.py` as it existed before Stage 4's crypto-partition work — `encode()` calls `harness.encryption.encrypt_fact_value` unconditionally (`store.py:418`), which derives its key from the master key (`KEY_VERSION = 1` hardcoded, `harness/encryption.py:38`). None of `roadmap`'s dyad-sealing (`encrypt_fact_value_for_dyad`) or class-sealing (`encrypt_by_class`/`partition_crypto.classify_write`) work exists on this checkout. Every fact the demo writes is master-key-sealed by construction, not by omission of one call site — this is the entire write path. Measured directly this session: 12/12 facts on 7689 are `key_version=1`, 0 at `key_version=2`.

This REQ scopes moving `~/hip-dev`'s write (and read) path onto `roadmap`'s partition/class-sealed model — the same rework `REQ_CRYPTO_P2_PARTITION_SEALED` and `REQ_WRITE_TIME_CLASSIFIER` already did for `roadmap`. Doing this is what finally lets the demo checkout's own copy of the master key retire — as long as the demo seals every write with it, that key cannot be destroyed without either breaking the demo or leaving it master-key-dependent forever. This REQ does not scope destroying that key itself (that stays out of scope here — see CONSTRAINTS); it scopes only getting the demo off of needing it for new writes.

## THE ACCEPTANCE TEST

Not yet buildable from this scope-only filing — no build starts without a acceptance test that can only pass or fail, and this REQ does not yet have Bill's sign-off on which of the two paths below to take. Recorded here as the fork this REQ must resolve before an acceptance test can be written:

1. **Port roadmap's write path onto hip-dev**, i.e. bring `memory_engine/store.py`, `harness/partition_crypto.py`, `harness/dyad_crypto.py`, `harness/care_team_keys.py`, and `harness/household_keys.py`'s current (ratified) model over to the `hip-dev`/`main` checkout — effectively catching that branch up to everything Stage 4 built on `roadmap`. Largest blast radius: `hip-dev` is the checkout the live demo, investor-facing dashboard, and `voice_https_orch`-adjacent surfaces run from; any regression there is visible to a live audience, not just a harness run.
2. **Merge/rebase `hip-dev`/`main` onto `roadmap`** (or vice versa) so there is one checkout, one write path, one master-key story — eliminating the two-checkout divergence entirely rather than porting code between them. Larger scope, resolves the underlying cause (`AUDIT_MASTER_KEY_FINDINGS`'s D-26: three repos, three copies of `harness/encryption.py`, none agreeing on their own default) rather than one symptom of it.

Whichever path Bill picks, the acceptance test must include, at minimum: every new write on the demo checkout lands `key_version=2` (dyad/class-sealed, never master-derived); existing demo facts either re-seal cleanly or are explicitly, disclosed-ly left as a known v1 population pending a separate migration step; the demo's own `--full`-equivalent (or its own smoke/preflight suite) stays green; and a live run of the actual demo script(s) shows no regression a presenter would see.

## WHAT'S ALREADY DONE

- The target model this REQ ports TO already exists and is proven, on `roadmap`: `REQ_CRYPTO_P1_DYAD_KEYS` (MET), `REQ_CRYPTO_P2_PARTITION_SEALED` (MET, the sealing mechanism), `REQ_CRYPTO_P4_RECOVERY_EVICTION` (MET). Nothing new needs inventing — this REQ is a migration of already-built code to a checkout that predates it, not new design work.
- `DISPATCH_DEMO_GRAPH_SEPARATION__v20260721_1721.md` (d5d37b4) already isolated the demo onto its own Neo4j instance (`bolt://localhost:7689`), so this migration's write-path changes cannot collide with `roadmap`'s own graph (`7688`) mid-work.
- This session's audit (REQ_CRYPTO_P3_OPERATOR_BLIND, 2026-07-24 update) already measured the exact current state this REQ starts from: 12 facts on 7689, all `key_version=1`, demo dashboard confirmed running (PID 46109 at time of audit), write path confirmed to call `encrypt_fact_value` unconditionally.

## WHAT'S KNOWN BROKEN

- `~/hip-dev/memory_engine/store.py` has none of `roadmap`'s `dyad_seal`/`classify_write`/`encrypt_by_class` machinery — a straight `git diff`/port is not a small patch, it is porting an entire phase of work across a divergent branch.
- `~/hip-dev/harness/encryption.py:44`'s `DEFAULT_MASTER_KEY_PATH` constant still points at the stale, orphaned `~/hip-harness/data/encryption/.master_key` (unlike `roadmap`'s copy, which `REQ_MASTERKEY_PATH` already fixed to point at `~/hip-dev`'s own key) — this checkout has not received even that smaller, already-MET fix. Currently masked in practice only because `com.hip.demo.dashboard.plist` sets an explicit `HIP_MASTER_KEY` override that wins over the stale default.
- No decision has been made on the fork in THE ACCEPTANCE TEST above (port vs. merge) — this REQ cannot proceed to a build until Bill picks one.
- The scope of "everything that changed on `roadmap` since `hip-dev`/`main` diverged" is not yet enumerated in this filing — a real build will need its own `git diff`/call-graph pass before starting, per CLAUDE.md's "trace the whole path end to end before changing any part of it."

## CONSTRAINTS

- **This REQ is explicitly NOT a blocker on REQ_CRYPTO_P3_OPERATOR_BLIND's part (c).** Bill's instruction: record as a separate scheduled job. `REQ_CRYPTO_P3_OPERATOR_BLIND`'s revised part (c) sequence (2026-07-24) proceeds against `roadmap`'s own, soon-to-be-decoupled key path and does not wait on this REQ.
- **Does not scope destroying hip-dev's master key.** This REQ only scopes moving the write (and read) path off of needing it for new facts. What happens to the 12 existing `key_version=1` facts (re-seal in place vs. leave as a disclosed legacy population vs. something else) and whether/when hip-dev's copy of the master key is ever destroyed is a decision for a later REQ, once this one is MET.
- **The demo must keep running throughout.** Whatever build eventually executes against this scope must not take down `com.hip.demo.dashboard` or any live presenter-facing surface without an explicit, planned maintenance window — this is investor/demo-facing infrastructure, not a dev sandbox.
- Must not touch `roadmap`'s own graph (`7688`) or its 11 v2 facts — this REQ's scope is entirely `hip-dev`/`7689`.
- Docs only, no code, in this filing. No build starts without Bill choosing between the two paths in THE ACCEPTANCE TEST and a follow-up REQ (or an amendment to this one) naming the acceptance test precisely, per CLAUDE.md's Requirements Discipline item 4 ("if the requirement isn't clear enough to write an acceptance test from, ASK").
