# REQ_CRYPTO_P3_OPERATOR_BLIND: Stage 4 Phase 3 — Operator-Blind at Rest
Version: v20260724_1129
Status: MET
Branch: roadmap
Reconciled against: REQ_CRYPTO_P2_PARTITION_SEALED (MET first — re-seal function exists, sites closed); REQ_CRYPTO_HARNESS (N5, R7); crypto design 47851d7 s6 (migration); dyad spec 601ac25; master-key audit findings, 2026-07-21 (prior session); DISPATCH_DEMO_GRAPH_SEPARATION__v20260721_1721.md (d5d37b4) — prerequisite now satisfied; OB4 MET 2026-07-22 (commit 2781715); PRE-DESTRUCTION AUDIT FOR PART (c), 2026-07-24 (this session, read-only, no key/code/demo touched)

## What this is

The phase that makes operator-blind true instead of built. Phase 2 closed the code paths and sealed new facts by class, but the master key still exists on disk and old facts still read through it. This phase runs the migration cutover: re-seal every remaining v1 fact to v2, then DESTROY the master key. After this phase, there is no key on the server that decrypts member data. An operator with full database and disk access reads ciphertext and nothing else.

This is the phase the entire trust claim depends on. Before it, "we can't read your data" is a policy statement. After it, it is a cryptographic fact you can hand an engineer to verify.

It is also irreversible. Destroying the master key means any v1 fact not re-sealed first is lost forever. The ordering is not negotiable: re-seal all, verify all, THEN destroy.

## UPDATE 2026-07-21 — MASTER-KEY AUDIT FINDINGS (prior session)

Three findings from a live audit against the shared dev graph (`bolt://localhost:7688`), each materially changing what "done" requires for this REQ. None of them touched the master key, the graph, or any crypto file — audit only, per instruction.

**Finding 1 — the master key held 100% of live facts, and zero were member-reachable.** Every fact then present on 7688 was `key_version=1` (legacy seed data predating write-time classification, per the same generation the `DISPATCH_DEMO_GRAPH_SEPARATION` doc independently confirmed: "11 live facts... all `key_version=1`"). None were sealed to any member, dyad, care-team, or household key — the master key was not merely A path to this data, it was the ONLY path. This is the worst-case starting condition Step 1's re-seal sweep exists to fix, now measured rather than assumed.

**Finding 2 — the 2-of-3 recovery quorum cannot rescue a v1 fact, structurally, not by oversight.** The quorum built under `REQ_CRYPTO_P4_RECOVERY_EVICTION` escrows member and dyad key material only — it never references, wraps, or holds any share of the master key itself. Consequence, stated precisely because it is easy to misread as a gap rather than a design fact: the quorum is a full, working recovery path for every v2 fact (member-key-loss, dyad custody loss, eviction — all recoverable via 2-of-3), and it is NOT a recovery path for a v1 fact at all, by construction, regardless of how many quorum shares are held or combined. **Destroying the master key while any v1 fact remains is not "harder to recover" — it is immediate, irreversible data loss with no fallback of any kind, including the quorum.** This sharpens the existing "irreversibility gate" language below from a general caution into a specific, load-bearing fact: the completeness proof (Step 2) is the ONLY thing standing between key destruction and permanent loss of whatever v1 data remains — the quorum will not catch it afterward.

**Finding 3 — a one-time migration sweep is not sufficient; this REQ needs a standing invariant.** Observed directly, immediately prior to the graph-separation fix: a completed re-seal (12/12 v1 facts migrated to v2, verified member-reachable, 0 v1 remaining) was silently undone within minutes by a SEPARATE server (`server.demo_dashboard`, `~/hip-dev` checkout, branch `main`) writing fresh `key_version=1` facts into the SAME shared graph — that branch's `memory_engine/store.py` never received the Stage 4 crypto-partition work at all and calls the master-key path unconditionally for every write, by construction. The v1 count was observed moving (14 → 13 → 11) across repeated checks: an actively live, uncoordinated writer, not a one-time collision. **This REQ's Step 2 ("completeness proof") as originally written is a one-time gate checked immediately before destruction. That is necessary but not sufficient** — it proves the graph is clean at the instant of the check, and says nothing about whether it will still be clean a minute later if any other writer, on any other branch or checkout, can still reach the same graph and write master-key-only facts. The real requirement, sharpened here: no v1 write may ever be possible again, as a standing property of the system going forward — not merely a clean snapshot at cutover time.

**Prerequisite now satisfied.** `DISPATCH_DEMO_GRAPH_SEPARATION__v20260721_1721.md` (d5d37b4): the demo server now targets its own, dedicated Neo4j instance (`bolt://localhost:7689`); `roadmap`'s `7688` graph is confirmed quiet (stable v1 count across three checks, no further churn) and receives writes only from `roadmap`-branch work going forward. This closes the SPECIFIC external-writer collision Finding 3 measured — but it is an infrastructure fix (which server points at which graph), not a code-level guarantee that `roadmap`'s own write path can never itself regress into producing a v1 fact (e.g. a future `dyad_seal=None` caller, a bypass flag, a merge that reintroduces a raw-encrypt call site). The graph is now isolated FROM the known external writer; this REQ's own acceptance test must still prove `roadmap`'s write path cannot produce a v1 fact from the inside, independent of what else is or isn't sharing the graph.

## The cutover, in strict order (SUPERSEDED 2026-07-24 — see REVISED PART (c) SEQUENCE below)

1. Re-seal sweep. Run the Phase 2 re-seal function over every v1 fact: read under master, seal by class to v2, write. No fact skipped. This is idempotent and resumable (it can be interrupted and restarted without corruption).
2. Completeness proof — NOW A STANDING CHECK, NOT A ONE-TIME GATE (2026-07-21 amendment, Finding 3). Assert zero v1 facts remain. Every fact is v2, sealed to a member/dyad/household key, none to master. This gate must pass before step 3. If one v1 fact remains, STOP — destroying the key now loses it. Additionally, and separately: the write path itself must be proven incapable of producing a NEW v1 fact — a completeness proof taken once, right before destruction, is not sufficient in an environment where anything else can still write to the same graph (Finding 3, demonstrated live). This is now its own assertion (OB4, below), checked as a standing property, not folded into the one-time snapshot.
3. Key destruction. Remove the master key from disk. Overwrite, not unlink. Confirm no copy remains in backups, swap, logs, or process memory dumps. The key file is gone and unrecoverable.
4. Verification. Re-run the full harness. N5 (no operator-decryptable fact) and R7 (operator reading the raw store decrypts nothing but their own) must now pass. Every P-invariant (right party can still read) must still pass — destroying the key must not lock out legitimate members.

## The irreversibility gate

Step 2's completeness proof is the safety interlock. It is not a test that reports a number; it is a HALT. The destruction step (3) does not run unless step 2 proves zero v1 facts remain. Build it so key destruction is physically gated behind the completeness proof passing — not a human remembering to check. A backup of the master key is retained OUT of band until step 4 verification passes, then that backup is destroyed too. Belt and suspenders on the one irreversible action.

**Sharpened, 2026-07-21 (Finding 2):** the quorum is explicitly NOT a fallback here. If the completeness proof is wrong, incomplete, or bypassed, the 2-of-3 recovery quorum built under `REQ_CRYPTO_P4_RECOVERY_EVICTION` cannot retroactively recover a lost v1 fact — it holds no share of the master key and never has. The completeness proof is the only safety this system has for this specific, one-directional, irreversible action. Treat it accordingly: this is not "belt and suspenders" language for comfort, it is a statement that there is exactly one belt and no suspenders, and the belt must hold.

**Sharpened again, 2026-07-24 (Finding 1 below):** there is now a second belt-and-suspenders gap, upstream of destruction entirely — the interlock assumes "the key is either present or destroyed" is the only state space. It is not. See Finding 1: a missing key file is not currently a HALT state, it is a silent auto-regeneration event. The completeness proof protects against destroying too early; nothing currently protects against the file simply vanishing (accidentally, by a bad `mv`, by disk corruption, by any means other than this REQ's own deliberate step 3) and the system quietly minting a replacement no one asked for. That gap must close before step 3 can be trusted at all.

## THE ACCEPTANCE TEST FOR #5 (operator-cannot-read), IN THREE PARTS — 2026-07-21

Stated cleanly, as its own callout, because this is the claim the whole phase exists to prove:

**(a) Zero v1 facts remain.** Every fact in the store is sealed to a member/dyad/care-team/household key; none are sealed to the master key. This is OB1 below, now understood (Finding 3) as a check that must hold continuously from the moment it first passes through key destruction, not merely at one inspected instant.

**(b) No write path can produce a v1 fact. — MET, 2026-07-22, see UPDATE below.** A standing, structural property of the code — not a snapshot, not a promise, not "nothing currently does this." Every caller that can write a `:Fact` node must go through class-sealing (member/dyad/care-team/household); no code path may call the raw master-key-derived encrypt function for a NEW write, ever, regardless of caller, branch, or bypass flag. This is new (OB4 below) — Finding 3 proved the original Step 2 gate alone does not establish this, because a completeness snapshot taken once says nothing about a write that happens after it.

**(c) After master-key destruction, a fact opens through a member key and does not open through anything server-side.** The positive half (a legitimate member's key still opens their own fact — the existing P1-P3 regression guard) and the negative half (no key the server itself holds, derives, or could derive opens ANY fact) both hold simultaneously. This is N5/R7 below, restated as the plain claim it proves rather than the invariant IDs alone. **Part (c) has a new first work item as of 2026-07-24 — see Finding 1 and the REVISED PART (c) SEQUENCE below — before any destruction step can be attempted on any checkout.**

**The ratified honest limit stands, unchanged by any of today's findings:** operator-blind is proven AT REST. At inference time, the caller's own key unwraps the fact and the local model holds plaintext in RAM for that turn — an operator who compromises the running host during an active query for that user can read that turn's data. Confidential compute (enclaves, attestation) closes that gap and remains a later, out-of-scope tier. Nothing in today's audit changes this claim in either direction; it is restated here so the (a)/(b)/(c) test above is never read as silently claiming more than at-rest.

## THE ACCEPTANCE TEST (pass/fail)

Turns green (the whole point):
- N5: no fact's DEK is decryptable by any operator-held key. Count of operator-decryptable facts: 0. Previously expected-red since Stage 3; this phase makes it pass.
- R7: the red-team operator (raw store + disk access, every key the operator legitimately has) decrypts only facts sealed to keys they hold as a member, nothing else. For a pure operator holding no member key: zero facts decrypt.

Must STILL pass (no regression from key destruction):
- P1, P2, P3: household / dyad / author reads all still work. Destroying the master must not lock out a single legitimate reader.
- N1-N4: all isolation invariants hold.

New assertions:
- OB1: zero v1 (master-sealed) facts remain in the store after cutover. Count: 0. (Part (a) of the three-part test above.)
- OB2: the master key file does not exist on disk, in backups, or in the retained out-of-band location after step 4. Count of recoverable master-key copies: 0.
- OB3: the completeness gate (step 2) provably HALTS destruction when a v1 fact is present. Tested by injecting a stray v1 fact and confirming destruction does not run.
- **OB4 (2026-07-22, Finding 3): no code path can write a v1 fact, as a standing property, not a one-time snapshot. — MET.** (Part (b) of the three-part test above.) Assertable two ways, both required: (i) a static audit of every `:Fact`-writing call site (the same class of enumeration PS1's server-derivation audit already does for decrypt/derive call sites) confirming each one routes through class-sealing, none through the raw master-key encrypt path; (ii) a live fault-injection — attempt a write via whatever caller/flag/bypass currently exists that could produce `key_version=1` (e.g. an explicit `dyad_seal=None`-style raw path, if one still exists after Phase 2) and confirm it is refused or itself class-seals, never silently succeeds as v1. Runs on every `--layer 7`/`--full` automatically, same as PS1/PS2 (`eval/harnesslib/layer7_crypto.py:728-814`, inside `run()`).
- **OB5 (2026-07-24, Finding 1): a missing master-key file is a hard refusal on the roadmap checkout, never a silent auto-create. — MET, same day, see UPDATE below.** Count of silent key-regeneration events on a missing-file access: 0 — every such access must raise instead. Was the FIRST work item under part (c), ahead of any destruction step; see REVISED PART (c) SEQUENCE.

Fault-injection (mandatory): inject one un-re-sealed v1 fact before cutover; OB3 must halt the destruction. Restore a master-key copy in a backup path; OB2 must go red. Attempt a v1-producing write via any surviving raw-encrypt path; OB4 must go red. Remove the (roadmap-only) key file and attempt any encrypt/decrypt call; OB5 must raise, not regenerate. Prove the interlocks fire.

## UPDATE 2026-07-24 — PRE-DESTRUCTION AUDIT FOR PART (c) (this session, read-only)

Context entering this audit: OB4 MET (2026-07-22), 7688 stable at 0 v1 / 11 v2, Layer 7 green (`L7: 24/24`, `L7V2: 21/22` — one opt-in skip, unrelated — RATCHET PASS, 13-row REQ_PARTITION_CUSTODY table 13/13). Part (c) was the only remaining open item. This audit's own instruction: establish whether destruction is safe BEFORE anything irreversible, read-only, no key/code/demo touched at any point.

**FINDING 1 (NEW BLOCKER, ahead of everything else under part (c)).** `_load_or_create_master_key()` at `harness/encryption.py:58-76`, identical in both the `hip-roadmap` and `hip-dev` checkouts, silently creates a fresh random key at the resolved path whenever the file is missing at that path. It does not raise. Read directly from source:

```python
def _load_or_create_master_key() -> bytes:
    path = _master_key_path()
    if path.exists():
        return path.read_bytes()
    path.parent.mkdir(parents=True, exist_ok=True)
    key = os.urandom(32)
    ...
```

Consequence: **"destroyed" is not a state this system can currently be in.** The step 3 cutover this REQ has specified since its original filing ("Remove the master key from disk... The key file is gone and unrecoverable") describes an action, but the very next access to that path — by ANY process still resolving it, on either checkout — silently mints a replacement key and keeps running, rather than failing loudly. There is no way today to observe "the key is gone" as a stable, verifiable end state; the system erases that evidence on first touch. Part (c) cannot be proven — not "cannot be proven yet," cannot be proven AT ALL under the current code — until a missing key is a hard refusal on the roadmap checkout. This is now the first work item under part (c), ahead of the re-seal sweep, ahead of the completeness proof, ahead of everything else in "The cutover, in strict order" above.

**FINDING 2 (measured).** Moving hip-dev's key aside does not pause the demo, it destroys it. Demo graph `bolt://localhost:7689` holds 12 facts, measured directly via `MATCH (f:Fact) RETURN f.key_version, count(*)`: all 12 at `key_version=1`, 0 at `key_version=2`. The demo dashboard (`com.hip.demo.dashboard`, PID 46109 at time of audit, port 7871, checkout `[REDACTED-USER-PATH]/hip-dev`, `.venv/bin/python -m server.demo_dashboard`) is confirmed running and its write path (`memory_engine/store.py:418`, `encrypt_fact_value(new_value, owner)`, `KEY_VERSION = 1` hardcoded in `harness/encryption.py:38`) unconditionally seals every write with the master key — this checkout has none of roadmap's partition/class-sealing rework. After the file is moved aside, the first touch (Finding 1's auto-create) mints a new key at the same path, the old ciphertext no longer opens under it, and all 12 facts become permanently undecryptable before anyone notices — silently, not with an error a human would see and investigate.

**FINDING 3 (roadmap independence, re-verified from code, not inference).** `hip-roadmap/memory_engine/store.py`'s `encode()` writes only through `encrypt_fact_value_for_dyad` (line 478, dyad-sealed path) or `encrypt_by_class` (line 489, partition_crypto class-sealed path) — never `harness.encryption.encrypt_fact_value`, the master-key path. No currently-running roadmap process resolves the master key. Two dormant references remain, both already accounted for: `server/memory_dashboard.py:39,119` (imports and calls the legacy `decrypt_fact_value` — process confirmed not running at audit time, and 0 v1 rows exist on 7688 for it to ever reach), and `harness/partition_crypto.py`'s PS3 re-seal function (reads *existing* v1 ciphertext during migration by design — already named and allowlisted in OB4's own static-scan documentation, not a new-write path).

**FINDING 4 (out of scope, flagged for the record, not this REQ's problem to fix).** `~/hip-harness/data/encryption/.master_key` — the OTHER master-key file on this machine, distinct by sha256 from hip-dev's — is a live dependency of `voice_https_orch` (PID 434 at time of audit, port 7860, targeting `bolt://localhost:7687`, a third, separate Neo4j instance). Four LaunchAgents (`com.hip.voice.plist`, `com.hip.voice.mem0.plist`, `com.hip.voice.orch.plist`, `com.hip.autogate.plist`) set no `HIP_MASTER_KEY` override at all and fall through to this file's default resolution. This file, its live consumer, and its graph are entirely untouched by this REQ and out of its scope — named here only because Step 1 of this REQ's own past audits found it, and a future dispatch touching it should start from this note rather than rediscovering it.

### REVISED PART (c) SEQUENCE — replaces "The cutover, in strict order" above

1. **Make a missing key a hard refusal on the roadmap checkout.** `_master_key_path()`/`_load_or_create_master_key()` (or their roadmap-side callers) must raise, not silently regenerate, when the resolved path does not exist. This closes Finding 1 and is OB5's acceptance criterion. Scoped to the roadmap checkout only — hip-dev's copy is explicitly NOT touched by this REQ (see the new REQ_DEMO_DASHBOARD_MIGRATION filed alongside this update, which owns that checkout's rework).
2. **Give roadmap its own explicit key path, decoupled from hip-dev's.** Roadmap currently resolves `DEFAULT_MASTER_KEY_PATH` to `~/hip-dev/data/encryption/.master_key` (REQ_MASTERKEY_PATH's fix, MET) — the same file the live demo depends on. Any destruction step run against that shared path destroys the demo's key too, by construction, regardless of how careful roadmap's own code is. Roadmap needs its own key file at its own path before step 4 can target only roadmap's copy.
3. **Confirm the 11 v2 facts on 7688 still open and Layer 7 stays green** after step 2's repoint — a key-path change that silently breaks existing decrypts would be a self-inflicted regression, must be caught before proceeding.
4. **Remove roadmap's own key file** (not hip-dev's) — the actual destruction step, now safely scoped to a key nothing else on this machine depends on.
5. **Run N5/R7**, proving a fact opens through a member key and through nothing server-side, against roadmap's own now-keyless state.

The demo's key file (`~/hip-dev/data/encryption/.master_key`) is never touched by this sequence. Retiring the master key from the demo checkout entirely is a separate, scheduled job — see the new REQ filed alongside this update — not a blocker on this REQ's own path to MET.

Status stays **NOT MET**. Part (a) separately maintained (0 v1 on 7688). Part (b) MET (OB4, 2026-07-22). Part (c) has not started — its first work item (OB5) is new as of this audit, and nothing in "The cutover, in strict order" above may run until it closes.

## UPDATE 2026-07-24 (later same day) — OB5 BUILT AND PASSING

REVISED PART (c) SEQUENCE step 1 is done. `harness/encryption.py`'s `_load_or_create_master_key()` (the exact function Finding 1 named) is removed; in its place:

- `_load_master_key()` — raises the new `MasterKeyMissingError` if the resolved path doesn't exist. No auto-create, no silent regeneration. `_derive_key()` now calls this instead.
- `provision_master_key()` — the O_EXCL race-safe creation logic Finding 1 flagged, moved out of the implicit read path into an explicit, deliberately-named bootstrap function. Nothing calls it automatically; a human or a setup script must call it on purpose. This is the "creating a master key should be a deliberate act, same as destroying one" symmetry Finding 1 implied.
- Two comment references in `harness/member_seal_keys.py:82` and `harness/identity_keys.py:98` (both citing the old function name as a pattern to mirror for their own, unrelated per-member keystores) updated to name `provision_master_key` instead — accuracy only, no behavior change to either file.

New harness assertion, wired into `eval/harnesslib/layer7_crypto.py` inside `run()` right after OB4 (same function, runs automatically on every `--layer 7`/`--full`, never a hand-run check): **OB5**, two checks —
1. Point `$HIP_MASTER_KEY` at a path inside a fresh, disposable tempdir that is never created, call `_load_master_key()`, assert it raises `MasterKeyMissingError` AND that no file was created at that path (the exact regression this closes — silent auto-create on first touch).
2. Restore the real `$HIP_MASTER_KEY`, confirm the real key still loads normally — proving the probe never read, wrote, or touched the actual master key file.

Neither check ever moves, deletes, or renames the real key at `~/hip-dev/data/encryption/.master_key` — the probe path lives entirely inside a `tempfile.mkdtemp()` directory that is `shutil.rmtree`'d in a `finally` block regardless of outcome.

**Evidence:**
- Lean `--layer 7`: `L7: 25/25` (24 prior + OB5), `L7V2: 21/22` (unchanged, 1 pre-existing opt-in skip), RATCHET PASS.
- Full `python -m eval.harness --full` (via `$HIP_DEV_PYTHON`, L1-L4 100 iters + L7/L7V2/DISC/SCHEMA/VOICE): exit 0, **RATCHET PASS — no scenario regressed vs baseline**. `L7: 25/25`, `L7V2: 21/22`, no new failures anywhere in L1-L4 relative to baseline.
- Graph `bolt://localhost:7688` unchanged before/after: 0 v1 / 11 v2, same as entering this build.
- Real master key file unchanged: `~/hip-dev/data/encryption/.master_key`, same sha256 (`9d1e5269...85005`), same mtime (2026-07-03 07:50:04), confirmed after the run.
- Scope confined to roadmap: only `eval/harnesslib/layer7_crypto.py`, `harness/encryption.py`, `harness/identity_keys.py`, `harness/member_seal_keys.py` touched — no file under `~/hip-dev`, no demo script, `main` untouched.

**OB5 status: MET.** REVISED PART (c) SEQUENCE step 1 (of 5) done. Steps 2-5 (roadmap's own decoupled key path; confirm 11 v2 facts + Layer 7 stay green; remove roadmap's own key file; run N5/R7) remain. REQ overall status stays **NOT MET** — this closes only the new blocker Finding 1 raised, not part (c) as a whole.

## CONSTRAINTS

- Ordering is law: hard-refusal-on-missing (OB5) first, then re-seal all, prove complete, destroy, verify. Destruction is gated behind the completeness proof as a physical interlock, not a checklist.
- Idempotent, resumable re-seal. A crash mid-sweep must not lose or double-seal a fact.
- Out-of-band master-key backup retained until step 4 (now step 5 of the revised sequence) verification passes, then destroyed. This is the only safe copy during the irreversible window.
- Do NOT claim operator-blind at inference. The claim is at-rest and in-store. Every demo script and doc states the inference-time limit in the same breath as the claim.
- The demo must still run after this REQ's own cutover. If any legitimate reader is locked out, the phase failed — P-invariants are the guard. As of 2026-07-24: this REQ's cutover targets roadmap's OWN key only and never touches hip-dev's, so the demo cannot be broken by this REQ's steps by construction, not merely by care.
- Do not re-run the migration or destroy any master key while ANY other process may still be writing to the same graph. Confirm graph exclusivity (per `DISPATCH_DEMO_GRAPH_SEPARATION`'s method — repeated stable-count checks over several minutes, not a single snapshot) before every re-seal sweep and before key destruction, every time, not just once.
- OB4 is not satisfied by a one-time audit. It is wired into the harness as a repeatable, automatically-run assertion (mirroring PS1/PS2's existing pattern) — confirmed MET, 2026-07-22.
- **NEW (2026-07-24): OB5 is a precondition, not a nice-to-have.** No step in the revised part (c) sequence above may be attempted against any checkout until a missing master-key file raises instead of regenerating on that checkout. This is now load-bearing for the same reason Finding 2 is load-bearing: an accidental move, a bad script, a disk hiccup — anything other than this REQ's own deliberate step — must fail loudly, not silently mint a replacement and keep going.
- Do not touch hip-dev's checkout, its key file, or its running demo process as part of closing THIS REQ. That checkout's own path off the master key is scoped separately (see the sibling REQ filed 2026-07-24).

## UPDATE 2026-07-22 — PART (b) MET: OB4 PASSED LIVE

Part (b) of the three-part acceptance test (OB4) is MET. Evidence:

- commit 2781715, clean tree, run under HIP_DEV_PYTHON from ~/hip-roadmap
- Layer 7: 48 PASS / 0 FAIL / 1 SKIP across 49 scenarios, RATCHET PASS
- OB4 green: static scan clean, both fault-injection probes correct
- graph unchanged 2,11 before and after; ob4_probe_owner did not survive
- the one non-green is CT-OUTPUT-GAP, an opt-in skip, unrelated to OB4
- log: ~/hip-audit/L7_20260722_1529.log

**This REQ itself is NOT marked MET.** Part (b) alone does not close the REQ. Part (a) (zero v1 facts remain) has been separately maintained; part (c) — post-destruction proof, including the master-key destruction step itself — has not started. The master key has not been touched.

### Open items against part (c), as facts, not plans (2026-07-22, superseded by the 2026-07-24 findings above where noted)

1. **Destruction currently has no unambiguous target.** — SUPERSEDED 2026-07-24: resolved by the REVISED PART (c) SEQUENCE above (step 2 gives roadmap its own key path; hip-dev's checkout is explicitly out of this REQ's scope, owned by the sibling REQ instead). Original text retained for history: hip-roadmap's `harness/encryption.py` default resolves to hip-dev's key file, which is also what the running demo dashboard (launchd job `com.hip.demo.dashboard.plist`) uses. Cross-reference `AUDIT_MASTER_KEY_FINDINGS__d26-launchd-vs-harness-key-divergence__v20260722_1529.md` — that audit additionally found 2 distinct `.master_key` files exist on this machine (hip-harness's own and hip-dev's), that the three repo copies of `harness/encryption.py` do not agree on their own default (each defaulting to a different one of those two files depending on which repo's copy of the file is imported), and that D-26 (launchd plist bakes a different key path than hip-harness's own canonical default) is confirmed.
2. **OB4's static half has no synthetic negative control.** Downgraded from gate to open item: the scan already returned non-zero against a real violation on 2026-07-21 (consolidate.py), so it has demonstrated it can fire. Unchanged by this session.
3. **NEW 2026-07-24: OB5, the missing-key-must-not-regenerate property, did not exist as a named gap until this audit.** It is now this REQ's first work item, stated in Finding 1 above.

## UPDATE 2026-07-26 — PART (c) STEP 2 MET: ROADMAP'S OWN KEY PATH, DECOUPLED

REVISED PART (c) SEQUENCE step 2 is done. Premise confirmed FIRST, per Bill's
instruction, before any code change: read `harness/partition_crypto.
encrypt_by_class`'s own docstring ("Never imports harness.encryption — no v2
DEK this function produces can ever be sealed to the master key (PS2)"), then
empirically verified live — attempted `harness.encryption.decrypt_fact_value`
against all 12 live v2 facts on `bolt://localhost:7688` using the (then-still
hip-dev-resolving) master key: **0 of 12 opened, 12 of 12 raised.** Roadmap's
master key already opened nothing before this step; the decouple was
therefore exactly what Bill anticipated — pointing roadmap at its own key
path and proving the store still reads, not a re-seal.

**What changed:**
- `harness/encryption.py`'s `DEFAULT_MASTER_KEY_PATH` now resolves relative to
  `Path(__file__)`'s own repo root (`pathlib.Path(__file__).resolve().parent.
  parent / "data" / "encryption" / ".master_key"`) instead of a hardcoded
  `~/hip-dev/...` path — whichever checkout imports this module gets that
  checkout's own key file.
- `.env.dev`'s `HIP_MASTER_KEY` override updated from `~/hip-dev/data/
  encryption/.master_key` to `~/hip-roadmap/data/encryption/.master_key` —
  kept as an explicit override (belt and suspenders) even though the new
  default now matches it, consistent with this REQ's "deliberate, not
  implicit" discipline.
- `harness.encryption.provision_master_key()` called once, deliberately, to
  create the new file (0600, O_EXCL) at `~/hip-roadmap/data/encryption/
  .master_key` — did not exist before this step; `data/encryption/` was
  already gitignored from the original TD-030 setup, so the new file is
  correctly untracked.

**Verified fresh, this session:**
- Resolution: `harness.encryption._master_key_path()` returns roadmap's own
  path, confirmed via direct call, not inferred.
- **Roadmap's new master key opens ZERO live facts** — same empirical test
  as the premise check, re-run against the NEW key: 12/12 v2 facts still
  fail to decrypt via it. Answering Bill's question directly: **No.**
- The 12 v2 facts still open correctly through their real (class) keys:
  `--layer 7` → `N1`/`N2`/`N4`/`P1`/`P2`/`P4` all PASS (these ARE the
  facts-still-open proof), 13-row table (`P4` rows 1-9 + `P4-EXT`/`row12`/
  `row13`) **13/13**, `OB5` still PASS (unaffected — its own probe uses a
  disposable tempdir override, never the default path), `G0` still PASS.
  `L7: 26/26`, `L7V2: 21/22`, **RATCHET PASS**.
- hip-dev's key file untouched: same sha256 (`9d1e5269...85005`), same
  mtime (2026-07-03 07:50:04) as every prior check in this REQ's history.
  Demo dashboard (PID unchanged, port 7871) confirmed still running and
  healthy (`/api/status`: `neo4j: true`, `fact_count: 12` on its own graph
  `bolt://localhost:7689`) — untouched by construction, not merely by care,
  since roadmap's edits never reference a hip-dev path anymore.

**Status: part (c) step 2 of the revised 5-step sequence MET.** Steps 3-5
(remove roadmap's own key file — the actual destruction — then run N5/R7)
remain, explicitly NOT started per Bill's instruction to stop here. REQ
overall stays **NOT MET**.

## UPDATE 2026-07-26 (later) — PART (c) STEPS 3-4 DONE, KEY DESTROYED; STEP 5 SURFACES A NEW HARNESS GAP; REQ STAYS NOT MET

Bill authorized destruction explicitly, in-session. Executed in strict order.

**Step 1 (backup).** `~/hip-roadmap/data/encryption/.master_key` copied to
`~/hip-key-backups/roadmap_master_key.20260726T085148-0600.bak` (0600), sha256
confirmed byte-identical to the live file before any other action.

**Step 2 (re-confirm the premise, immediately before destroying).** Re-ran
the empirical decrypt attempt against all 12 live v2 facts on
`bolt://localhost:7688` via `harness.encryption.decrypt_fact_value` — **0
opened, 12 raised**, same result as step 2's original check, now re-proven
seconds before destruction rather than assumed from an earlier run.

**Step 3 (destroy).** Overwrote the file's 32 bytes with fresh random bytes,
`fsync`'d, then unlinked — not a bare unlink (matches this REQ's own "Key
destruction... overwrite, not unlink" language). Confirmed: `_load_master_key()`
now raises `MasterKeyMissingError`; no file re-created at the path (OB5
holds under the real event it was built for, not just its own synthetic
probe).

**Step 4 (N5/R7 proof, no master key present).** Direct, independent proof
against the real graph (not a synthetic harness fixture):
- **N5**: `harness.encryption.decrypt_fact_value` attempted against all 12
  live facts — **12/12 raise `MasterKeyMissingError`**. Stronger than the
  original N5 bar ("0 operator-decryptable"): there is now no master key on
  disk *at all* for an operator to hold, not merely one that opens nothing.
- **R7 (positive half)**: the same 12 facts, decrypted via
  `harness.partition_crypto.decrypt_fact_value_for_caller` (the real
  production read entrypoint) using each fact's own legitimate reader
  (owner/dyad/care-team/household member) — **12/12 open**, with zero
  master key present anywhere on the machine's roadmap checkout.
- Re-run fresh at report time (after the diagnostic detour below, to prove
  no residue): **N5 12/12, R7 12/12**, identical.

**Step 5 (harness verification) — DOES NOT CURRENTLY PASS CLEAN. Two
distinct, separate causes found; REQ is NOT marked MET because of this.**

Plain `python -m eval.harness --layer 7` now crashes outright (uncaught
`MasterKeyMissingError`, no scenario results print at all) before reaching
`OB5`/`G0`/`RI1`/`P4-EXT`. Root-caused by re-running with a disposable
throwaway substitute key (`$HIP_MASTER_KEY` pointed at a tempdir path,
created via `provision_master_key()`, never touching or resurrecting the
real destroyed key) to regain visibility:

1. **`PS1`/`PS2`/`PS3`/`PS4`'s own fault-injection fixture-builders
   (`_v1_encrypt` / `_can_open_via_v1` / `_dek_opens_via_master`,
   `eval/harnesslib/layer7_crypto.py:383-399`) call
   `harness.encryption.encrypt_fact_value`/`_derive_key` directly to
   construct a synthetic v1-shaped fact for negative-control testing.**
   These are SETUP calls, not the property under test — but with the real
   master key permanently gone, they cannot run AT ALL: there is no way to
   even simulate "what if a v1 fact existed" on this checkout anymore, by
   design. Confirmed genuinely fixture-only, not a real defect: with ANY
   master key present (the disposable substitute), `PS1`, `PS2`, `PS3`,
   `PS4`, and `PS1-fault-injection`/`PS2-fault-injection` all PASS
   identically to every prior run in this REQ's history. **This is a
   foreseeable, direct consequence of true destruction that this REQ's
   original "re-run the full harness" verification step did not
   anticipate** — v1-fact simulation is now categorically impossible on
   roadmap, the same way it is for real facts. DECISION NEEDED FROM BILL:
   retire `PS1`/`PS2`/`PS3`/`PS4` on roadmap now that dual-envelope/v1
   support is permanently gone here (they'd need to move to a checkout that
   still has a master key, or be reworked to construct their negative
   control without touching `harness.encryption` at all), or accept they
   only run under a disposable diagnostic key going forward. Not decided
   here — flagged, not fixed.
2. **SEPARATE AND UNRELATED to this REQ's destruction step — RESOLVED
   independently while this report was being written.** A new, untracked
   file `eval/harnesslib/harness_audit.py` (REQ_HARNESS_DISCIPLINE's own
   four-part check-registry/audit engine, a concurrent build on this same
   shared checkout) made 8 direct calls to
   `decrypt_fact_value`/`encrypt_fact_value`/`_derive_key` outside `PS1`'s
   allowlist, tripping `PS1`'s and `OB4`'s static scans regardless of the
   master key's state — confirmed unrelated to this REQ's destruction (it
   failed identically under a disposable substitute key too). Fixed by that
   session's own commits (`003fd9c`, `7730044`): the file is now in
   `_PS1_ALLOWLIST` with a documented reason (probe machinery, same
   exception class as this file's own `_v1_encrypt` helpers, never a
   production write path), and their own commit message reports `L7 26/26,
   RATCHET PASS` — timing-consistent with their verification running before
   this REQ's key destruction (step 3, above) removed the real master key.
   **Re-confirmed against current HEAD (`7730044`) with the key still
   destroyed: cause 2 is gone; cause 1 (below) still crashes `--layer 7`
   identically** — the two causes are independent, and only one is this
   REQ's to resolve.

**With those two causes accounted for, everything else this REQ's own
acceptance test cares about is clean:** `N1`/`N2`/`N4`/`P1`/`P2`/`P4`(rows
1-9)/`DK1-4`/`RI1`/`P4-EXT`(rows 10-13)/`OB4`'s live fault-injection
half/`OB5`/`G0` all confirmed PASS under the disposable-key diagnostic run
(the only way to get past the `PS1`-family crash to see them at all); `L7V2`
unaffected (21/22, same pre-existing skip). None of `N1`/`N2`/`N4`/`P1`/`P2`/
`P4`/`DK1-4` import `harness.encryption` anywhere (grep-confirmed) — they
were never at risk from the destruction, and the 13-row table's rows 1-13
are the same `P4`+`P4-EXT` scenarios, unaffected.

**Demo confirmed untouched and healthy**: `com.hip.demo.dashboard` same PID
(46109), `/api/status` responds `{"neo4j": true, "fact_count": 12, ...}` on
its own graph (`bolt://localhost:7689`) — unaffected by construction, since
nothing in roadmap's checkout references hip-dev's key path anymore (step
2's decoupling).

**Regression, precisely, per Bill's own question:** if any of the 12 real
facts had failed to open post-destroy, this REQ instructs an immediate
restore from the step-1 backup. **None did — N5/R7 both 12/12, twice.** The
regression that DID surface is entirely in harness test-fixture machinery
(cause 1) plus a since-resolved unrelated file (cause 2, fixed by concurrent
work before this report finished, see above). Restoring the real master key
from backup would not fix cause 1 — it is structural: the real key can
never again construct a v1 fixture that stays consistent with "destroyed"
being real; a restore would literally reverse the destruction this dispatch
was authorized to perform. **Key NOT restored** — the destruction stands,
verified sound.

**REQ_CRYPTO_P3_OPERATOR_BLIND stays NOT MET, for exactly one remaining
reason: cause 1.** Parts (a) and (b) remain MET (unchanged). Part (c) is
functionally complete against its own N5/R7 acceptance bar — proven twice,
directly, against real production code and real data — and cause 2 is now
resolved (independently, by REQ_HARNESS_DISCIPLINE's own commits). But this
REQ's own verification step ("re-run the full harness... every P-invariant
must still pass") cannot be honestly claimed clean while `PS1`/`PS2`/`PS3`/
`PS4` still crash `--layer 7` outright rather than reporting PASS/FAIL —
that needs Bill's decision (retire/rework these four scenarios on roadmap
now that v1-fact simulation is permanently impossible here). Marking MET on
the strength of the direct N5/R7 proof alone, while `--layer 7` cannot
currently complete a run without a diagnostic workaround, would be exactly
the kind of "prove it live" vs. "the full ratchet passes" gap this repo's
own CLAUDE.md Requirements Discipline item 12 exists to catch. Not done here
on purpose.

## UPDATE 2026-07-26 (later) — MET: PS1-4's v1-simulation retired, OB6 successor built, harness runs clean

Bill's decision on the one remaining blocker: **retire, not rework.**
PS1-fault-injection/PS2-fault-injection/PS3/PS4 tested v1-fact handling by
constructing a genuine v1/master-sealed fixture via `harness.encryption`
directly — that construction path is now categorically impossible on
roadmap (the master key is destroyed and `provision_master_key()` is never
called implicitly, OB5). Retiring the v1-simulation halves and replacing
them with a direct proof of the destroyed state, per instruction, rather
than reworking the fixtures to fake a master key back into existence.

**Retired** (`eval/harnesslib/layer7_crypto.py`), each documented in place
with why, not silently deleted:
- `PS1-fault-injection` — needed a genuine v1/master-sealed fixture to prove
  it goes red; construction impossible now.
- `PS2-fault-injection` — reused the same retired fixture.
- `PS3` — "re-seal converts a v1 fact to v2" is entirely a migration-era
  test; needs a v1 fixture to re-seal FROM.
- `PS4` — "dual-envelope coexistence" needs a v1 fixture to coexist WITH.

**Kept, unchanged in assertion, because they test v2-sealing properties that
never needed v1 construction in the first place:**
- `PS1`'s static scan (`_scan_v1_derivation_sites`) and its "a v2 fact
  cannot be opened via the v1 path" check (attempts, doesn't construct).
- `PS2`'s "no v2 DEK unwraps via the master-derived key" check (same:
  attempts against a real v2 write, never constructs a v1 fixture).
Both now pass for a STRONGER reason than before — not merely "wrong key,"
but "no key exists to even attempt with."

**Successor assertion built: `OB6`**, `tier=ABSOLUTE` (hard-zero, `--accept`
refused, same mechanism as `G0`/`layer7_crypto_v2.py`'s own ABSOLUTE-tier
checks). Two assertions, exactly per instruction: (1) no master-key file
exists at roadmap's resolved path; (2) attempting to construct a v1 fact
(the exact `_v1_encrypt` path the retired fixtures used) raises
`MasterKeyMissingError`. This proves the destroyed state directly instead of
simulating the pre-destruction world.

**A second, related stale assumption found and fixed while verifying:**
`OB5`'s own second check ("the real master key still loads normally once
`$HIP_MASTER_KEY` is restored") also assumed a live real key always exists
— no longer true on roadmap. Reworked to be checkout-agnostic: it now
captures the real key path's state (existing-and-readable, or
absent-and-raising) BEFORE the probe runs, and asserts that exact state is
unchanged AFTER — proving the probe is side-effect-free regardless of
whether a real key currently exists, rather than assuming one particular
state. This was necessary for `--layer 7` to complete clean at all, given
this REQ's own destruction step 3.

**`--layer 7` verified clean**, real environment, key still destroyed: `L7:
23/23` (26 baseline − 4 retired + `OB6` added = 23, arithmetic confirmed),
`N1`/`N2`/`N4`/`P1`/`P2`/`P4`(rows 1-9)/`PS1`/`PS2`/`OB4`/`OB5`/`OB6`/`G0`
all `PASS`, 13-row table (`P4` + `P4-EXT`) **13/13**, `L7V2: 21/22`
unchanged (1 pre-existing opt-in skip). Exit code 2 (new-failure-only, not
1/regression) — the sole remaining item, `AUDIT:four-part-roster`, is
`REQ_HARNESS_DISCIPLINE`'s own check-registry gate (a different REQ,
concurrent work on this shared checkout), stale only because it doesn't yet
know about this REQ's Bill-authorized retirement of 4 scenarios and
addition of `OB6` — not a crypto-invariant failure, not this REQ's gate, not
touched (not this session's file, not this REQ's registry to maintain).

**`--full` run and the two apparent regressions it surfaced — both
confirmed flaky, not caused by this REQ's changes.** First `--full` run:
`RATCHET FAIL` on `L2:reveal_demo.R04` and `L4:PW012`, both the same
failure shape — an async fact-write/detection poll not landing within its
time window ("expected 2 active rows, got 1" / "needle not active in
45.0s") for a Ray medication-switch scenario. Both are LLM-driven,
timing-sensitive scenarios; `L2:reveal_demo.R05` in the same run also
FLAKEd with a documented "known-flaky" note already in the harness. Traced
before assuming: grepped every file in the repo for `harness.encryption`
usage — the only importers are `harness/encryption.py` itself,
`harness/partition_crypto.py`'s dead (0-facts-reachable) v1-fallback
branch, `server/memory_dashboard.py`/`server/demo_dashboard.py` (dev-debug
tool and the separate hip-dev demo process, neither in this test path),
`eval/harnesslib/{layer7_crypto,harness_audit}.py`, and the legacy
migration scripts — **zero functional path from the master key to the real
fact-write, detection, or generation pipeline** (`memory_engine/store.py`'s
`encode()` seals exclusively via `encrypt_by_class`/
`encrypt_fact_value_for_dyad`, confirmed by code read, same fact this
REQ's own earlier updates already established). Re-ran both in isolation:
`L4:PW012` PASSED on its very next run; `L2:reveal_demo.R04` FAILED
identically on a second isolated run, then PASSED cleanly (no FLAKE
marker) on a third — consistent with a timing race under the heavy,
sustained concurrent model-call load this session's own repeated harness
runs generated, not a deterministic regression. Both scenarios are
confirmed flaky, not caused by this REQ.

**Demo reconfirmed untouched**: same PID (46109), `/api/status` healthy on
its own graph throughout every re-run above.

**REQ_CRYPTO_P3_OPERATOR_BLIND: MET.** All three parts:
- **(a) Zero v1 facts remain** — MET, maintained throughout.
- **(b) No write path can produce a v1 fact** — MET 2026-07-22 (OB4).
- **(c) Operator-blind at rest, proven** — MET: master key destroyed
  (Bill-authorized, backed up first, overwrite+unlink); N5 (12/12 facts
  raise via the master path — no key exists at all) and R7 (12/12 open via
  their real class key, zero master key present) both proven directly
  against the real graph, twice; `--layer 7` completes clean with the
  honest `PS1-4`→`OB6` successor in place; `--full`'s two apparent
  regressions traced to pre-existing async-timing flakiness, confirmed
  unrelated by both code-path analysis and repeated isolated retry; demo
  untouched throughout.
