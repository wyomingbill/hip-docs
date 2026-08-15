# REQ_CRYPTO_P3_OPERATOR_BLIND: Stage 4 Phase 3 — Operator-Blind at Rest
Version: v20260721_2229
Status: NOT MET
Branch: roadmap
Reconciled against: REQ_CRYPTO_P2_PARTITION_SEALED (MET first — re-seal function exists, sites closed); REQ_CRYPTO_HARNESS (N5, R7); crypto design 47851d7 s6 (migration); dyad spec 601ac25; master-key audit findings, 2026-07-21 (this session); DISPATCH_DEMO_GRAPH_SEPARATION__v20260721_1721.md (d5d37b4) — prerequisite now satisfied

## What this is

The phase that makes operator-blind true instead of built. Phase 2 closed the code paths and sealed new facts by class, but the master key still exists on disk and old facts still read through it. This phase runs the migration cutover: re-seal every remaining v1 fact to v2, then DESTROY the master key. After this phase, there is no key on the server that decrypts member data. An operator with full database and disk access reads ciphertext and nothing else.

This is the phase the entire trust claim depends on. Before it, "we can't read your data" is a policy statement. After it, it is a cryptographic fact you can hand an engineer to verify.

It is also irreversible. Destroying the master key means any v1 fact not re-sealed first is lost forever. The ordering is not negotiable: re-seal all, verify all, THEN destroy.

## UPDATE 2026-07-21 — MASTER-KEY AUDIT FINDINGS (this session)

Three findings from a live audit against the shared dev graph (`bolt://localhost:7688`), each materially changing what "done" requires for this REQ. None of them touched the master key, the graph, or any crypto file — audit only, per instruction.

**Finding 1 — the master key held 100% of live facts, and zero were member-reachable.** Every fact then present on 7688 was `key_version=1` (legacy seed data predating write-time classification, per the same generation the `DISPATCH_DEMO_GRAPH_SEPARATION` doc independently confirmed: "11 live facts... all `key_version=1`"). None were sealed to any member, dyad, care-team, or household key — the master key was not merely A path to this data, it was the ONLY path. This is the worst-case starting condition Step 1's re-seal sweep exists to fix, now measured rather than assumed.

**Finding 2 — the 2-of-3 recovery quorum cannot rescue a v1 fact, structurally, not by oversight.** The quorum built under `REQ_CRYPTO_P4_RECOVERY_EVICTION` escrows member and dyad key material only — it never references, wraps, or holds any share of the master key itself. Consequence, stated precisely because it is easy to misread as a gap rather than a design fact: the quorum is a full, working recovery path for every v2 fact (member-key-loss, dyad custody loss, eviction — all recoverable via 2-of-3), and it is NOT a recovery path for a v1 fact at all, by construction, regardless of how many quorum shares are held or combined. **Destroying the master key while any v1 fact remains is not "harder to recover" — it is immediate, irreversible data loss with no fallback of any kind, including the quorum.** This sharpens the existing "irreversibility gate" language below from a general caution into a specific, load-bearing fact: the completeness proof (Step 2) is the ONLY thing standing between key destruction and permanent loss of whatever v1 data remains — the quorum will not catch it afterward.

**Finding 3 — a one-time migration sweep is not sufficient; this REQ needs a standing invariant.** Observed directly, immediately prior to the graph-separation fix: a completed re-seal (12/12 v1 facts migrated to v2, verified member-reachable, 0 v1 remaining) was silently undone within minutes by a SEPARATE server (`server.demo_dashboard`, `~/hip-dev` checkout, branch `main`) writing fresh `key_version=1` facts into the SAME shared graph — that branch's `memory_engine/store.py` never received the Stage 4 crypto-partition work at all and calls the master-key path unconditionally for every write, by construction. The v1 count was observed moving (14 → 13 → 11) across repeated checks: an actively live, uncoordinated writer, not a one-time collision. **This REQ's Step 2 ("completeness proof") as originally written is a one-time gate checked immediately before destruction. That is necessary but not sufficient** — it proves the graph is clean at the instant of the check, and says nothing about whether it will still be clean a minute later if any other writer, on any other branch or checkout, can still reach the same graph and write master-key-only facts. The real requirement, sharpened here: no v1 write may ever be possible again, as a standing property of the system going forward — not merely a clean snapshot at cutover time.

**Prerequisite now satisfied.** `DISPATCH_DEMO_GRAPH_SEPARATION__v20260721_1721.md` (d5d37b4): the demo server now targets its own, dedicated Neo4j instance (`bolt://localhost:7689`); `roadmap`'s `7688` graph is confirmed quiet (stable v1 count across three checks, no further churn) and receives writes only from `roadmap`-branch work going forward. This closes the SPECIFIC external-writer collision Finding 3 measured — but it is an infrastructure fix (which server points at which graph), not a code-level guarantee that `roadmap`'s own write path can never itself regress into producing a v1 fact (e.g. a future `dyad_seal=None` caller, a bypass flag, a merge that reintroduces a raw-encrypt call site). The graph is now isolated FROM the known external writer; this REQ's own acceptance test must still prove `roadmap`'s write path cannot produce a v1 fact from the inside, independent of what else is or isn't sharing the graph.

## The cutover, in strict order

1. Re-seal sweep. Run the Phase 2 re-seal function over every v1 fact: read under master, seal by class to v2, write. No fact skipped. This is idempotent and resumable (it can be interrupted and restarted without corruption).
2. Completeness proof — NOW A STANDING CHECK, NOT A ONE-TIME GATE (2026-07-21 amendment, Finding 3). Assert zero v1 facts remain. Every fact is v2, sealed to a member/dyad/household key, none to master. This gate must pass before step 3. If one v1 fact remains, STOP — destroying the key now loses it. Additionally, and separately: the write path itself must be proven incapable of producing a NEW v1 fact — a completeness proof taken once, right before destruction, is not sufficient in an environment where anything else can still write to the same graph (Finding 3, demonstrated live). This is now its own assertion (OB4, below), checked as a standing property, not folded into the one-time snapshot.
3. Key destruction. Remove the master key from disk. Overwrite, not unlink. Confirm no copy remains in backups, swap, logs, or process memory dumps. The key file is gone and unrecoverable.
4. Verification. Re-run the full harness. N5 (no operator-decryptable fact) and R7 (operator reading the raw store decrypts nothing but their own) must now pass. Every P-invariant (right party can still read) must still pass — destroying the key must not lock out legitimate members.

## The irreversibility gate

Step 2's completeness proof is the safety interlock. It is not a test that reports a number; it is a HALT. The destruction step (3) does not run unless step 2 proves zero v1 facts remain. Build it so key destruction is physically gated behind the completeness proof passing — not a human remembering to check. A backup of the master key is retained OUT of band until step 4 verification passes, then that backup is destroyed too. Belt and suspenders on the one irreversible action.

**Sharpened, 2026-07-21 (Finding 2):** the quorum is explicitly NOT a fallback here. If the completeness proof is wrong, incomplete, or bypassed, the 2-of-3 recovery quorum built under `REQ_CRYPTO_P4_RECOVERY_EVICTION` cannot retroactively recover a lost v1 fact — it holds no share of the master key and never has. The completeness proof is the only safety this system has for this specific, one-directional, irreversible action. Treat it accordingly: this is not "belt and suspenders" language for comfort, it is a statement that there is exactly one belt and no suspenders, and the belt must hold.

## THE ACCEPTANCE TEST FOR #5 (operator-cannot-read), IN THREE PARTS — 2026-07-21

Stated cleanly, as its own callout, because this is the claim the whole phase exists to prove:

**(a) Zero v1 facts remain.** Every fact in the store is sealed to a member/dyad/care-team/household key; none are sealed to the master key. This is OB1 below, now understood (Finding 3) as a check that must hold continuously from the moment it first passes through key destruction, not merely at one inspected instant.

**(b) No write path can produce a v1 fact. — MET, 2026-07-22, see UPDATE below.** A standing, structural property of the code — not a snapshot, not a promise, not "nothing currently does this." Every caller that can write a `:Fact` node must go through class-sealing (member/dyad/care-team/household); no code path may call the raw master-key-derived encrypt function for a NEW write, ever, regardless of caller, branch, or bypass flag. This is new (OB4 below) — Finding 3 proved the original Step 2 gate alone does not establish this, because a completeness snapshot taken once says nothing about a write that happens after it.

**(c) After master-key destruction, a fact opens through a member key and does not open through anything server-side.** The positive half (a legitimate member's key still opens their own fact — the existing P1-P3 regression guard) and the negative half (no key the server itself holds, derives, or could derive opens ANY fact) both hold simultaneously. This is N5/R7 below, restated as the plain claim it proves rather than the invariant IDs alone.

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
- **OB4 (NEW, 2026-07-21, Finding 3): no code path can write a v1 fact, as a standing property, not a one-time snapshot.** (Part (b) of the three-part test above.) Assertable two ways, both required: (i) a static audit of every `:Fact`-writing call site (the same class of enumeration PS1's server-derivation audit already does for decrypt/derive call sites) confirming each one routes through class-sealing, none through the raw master-key encrypt path; (ii) a live fault-injection — attempt a write via whatever caller/flag/bypass currently exists that could produce `key_version=1` (e.g. an explicit `dyad_seal=None`-style raw path, if one still exists after Phase 2) and confirm it is refused or itself class-seals, never silently succeeds as v1. Unlike OB1 (checked once, before destruction), OB4 is meant to run on every `--full`/`--layer 7` invocation going forward, the same way PS1/PS2 already do for their own server-derivation and master-seal audits — a regression here must be caught by the harness automatically, not rediscovered by a live audit each time.

Fault-injection (mandatory): inject one un-re-sealed v1 fact before cutover; OB3 must halt the destruction. Restore a master-key copy in a backup path; OB2 must go red. Attempt a v1-producing write via any surviving raw-encrypt path; OB4 must go red. Prove the interlocks fire.

## DEMONSTRATION OBJECTIVE

Co-equal to the build. This is the demo that closes an investor or an operator's security team. Not rigged.

SHOW: The cutover, then the proof. Run the re-seal sweep, show zero v1 remain, destroy the key on screen. Then become the operator: full disk, full database, the deleted key is gone. Try to read a member's fact. Ciphertext. Try every recovery — swap, backup, logs. Nothing. The wall is now the key's absence, not the code's politeness. Then show OB4: attempt a write via any surviving raw path and show it refused or class-sealed, never silently landing as v1 — the wall holds looking forward, not just at the instant of the snapshot.

LET THEM RUN: This is the strongest proof in the whole system. Hand the engineer root on the box. Let them search for the master key, dump memory, read the raw store, run the decrypt function as the server. Let them try to read Ray's medication as the operator. It cannot be done, and they proved it themselves, with root. Let them also try to write a new fact through every code path they can find and confirm none of them produce a v1 result.

THE CLAIM IT PROVES: "The operator cannot read customer data. Not 'does not' — cannot. There is no key on this machine that decrypts it, and you just verified that with root access. And no write, from anywhere, can ever hand the operator a new fact it can read either."

THE HARDEST QUESTION + HONEST ANSWER: "The local model reads plaintext at query time to answer. So the operator CAN read the data — just snapshot memory during a query." Answer, limit stated first and unflinching: yes. This phase makes the operator blind AT REST and in the database. At inference time, the caller's key unwraps the fact and the local model sees plaintext in RAM for that turn; an operator who compromises the running host during an active query for that user can read that turn's data. That is the accepted boundary of this roadmap — enclaves close it and are a later tier, out of scope here. What we eliminated is the far larger exposure: the operator reading the whole store at leisure, any user, any time, from disk. We traded "read everything, always" for "maybe read one active turn if you compromise the live host in the moment." State that trade honestly; it is a strong one and it survives scrutiny precisely because we do not overclaim it.

SECOND HARDEST QUESTION, new 2026-07-21: "You migrated everything once before and a different server undid it within minutes. How do I know this won't happen again?" Answer, limit stated first: it already did happen once, in this exact environment, and the fix (graph separation, `DISPATCH_DEMO_GRAPH_SEPARATION`) closes the SPECIFIC external writer we found — it does not, by itself, prove no future writer or code path can do the same thing from inside `roadmap` itself. That is exactly why OB4 exists as a standing, automatically-re-checked harness assertion rather than a one-time proof: the claim is not "we checked once," it is "the system cannot produce this failure mode, checked every time we run the gate."

## CONSTRAINTS

- Ordering is law: re-seal all, prove complete, destroy, verify. Destruction is gated behind the completeness proof as a physical interlock, not a checklist.
- Idempotent, resumable re-seal. A crash mid-sweep must not lose or double-seal a fact.
- Out-of-band master-key backup retained until step 4 verification passes, then destroyed. This is the only safe copy during the irreversible window.
- Do NOT claim operator-blind at inference. The claim is at-rest and in-store. Every demo script and doc states the inference-time limit in the same breath as the claim.
- The demo must still run after cutover. If any legitimate reader is locked out, the phase failed — P-invariants are the guard.
- **NEW (2026-07-21): do not re-run the migration or destroy the master key while ANY other process may still be writing to the same graph.** Confirm graph exclusivity (per `DISPATCH_DEMO_GRAPH_SEPARATION`'s method — repeated stable-count checks over several minutes, not a single snapshot) before every re-seal sweep and before key destruction, every time, not just once at the start of this phase's build.
- **NEW (2026-07-21): OB4 is not satisfied by a one-time audit.** It must be wired into the harness as a repeatable, automatically-run assertion (mirroring PS1/PS2's existing pattern) before this REQ can be marked MET — a hand-run static grep, done once, does not satisfy "no code path CAN produce a v1 fact" as a standing claim.

## UPDATE 2026-07-22 — PART (b) MET: OB4 PASSED LIVE

Part (b) of the three-part acceptance test (OB4) is MET. Evidence:

- commit 2781715, clean tree, run under HIP_DEV_PYTHON from ~/hip-roadmap
- Layer 7: 48 PASS / 0 FAIL / 1 SKIP across 49 scenarios, RATCHET PASS
- OB4 green: static scan clean, both fault-injection probes correct
- graph unchanged 2,11 before and after; ob4_probe_owner did not survive
- the one non-green is CT-OUTPUT-GAP, an opt-in skip, unrelated to OB4
- log: ~/hip-audit/L7_20260722_1529.log

**This REQ itself is NOT marked MET.** Part (b) alone does not close the REQ. Part (a) (zero v1 facts remain) has been separately maintained; part (c) — post-destruction proof, including the master-key destruction step itself — has not started. The master key has not been touched.

### Open items against part (c), as facts, not plans

1. **Destruction currently has no unambiguous target.** hip-roadmap's `harness/encryption.py` default resolves to hip-dev's key file, which is also what the running demo dashboard (launchd job `com.hip.demo.dashboard.plist`) uses. Cross-reference `AUDIT_MASTER_KEY_FINDINGS__d26-launchd-vs-harness-key-divergence__v20260722_1529.md` — that audit additionally found 2 distinct `.master_key` files exist on this machine (hip-harness's own and hip-dev's), that the three repo copies of `harness/encryption.py` do not agree on their own default (each defaulting to a different one of those two files depending on which repo's copy of the file is imported), and that D-26 (launchd plist bakes a different key path than hip-harness's own canonical default) is confirmed. Before any destruction step can run, which of the on-disk key files is "the" master key to destroy, and which checkouts/services must be repointed or retired first, is not yet decided.
2. **OB4's static half has no synthetic negative control.** Downgraded from gate to open item: the scan already returned non-zero against a real violation on 2026-07-21 (consolidate.py), so it has demonstrated it can fire.
