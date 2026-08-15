# REQ_CRYPTO_HARNESS: Stage 3 Invariants and Red-Team Fixture
Version: v20260719_0810
Status: NOT MET
Branch: roadmap
Reconciled against: REQ_PARTITION_CUSTODY (Stage 2, must be MET first); crypto design 47851d7; dyad spec 601ac25; existing eval.harness (L1-L4 pattern)

## What this is

The test harness for the confidentiality claims. It is infrastructure, not a feature. It exists so that every Stage 4 phase proves itself against pass/fail invariants instead of a demo that looks right. It is written AFTER the partition because the invariants are defined in terms of "private" and "dyad", which the partition REQ fixes.

The rule this enforces: a crypto claim is not true until the harness fails when the claim is violated. A green test that cannot go red proves nothing.

## Two halves, both required

The truth-track harness taught a lesson this must not repeat: a suite with only negative assertions rewards a system that refuses everything. The crypto harness has the mirror risk: a suite that only checks "the wrong person cannot read" rewards a system that walls everything and serves no one. So:

NEGATIVE half (isolation holds): the wrong party cannot read.
POSITIVE half (function holds): the right party can read, and shared facts actually reach the household.

A Stage 4 phase is done only when both halves are green. Neither alone is sufficient.

## The hard-zero invariants (pass/fail, not rates)

These are counts that must be exactly zero or exactly complete. No "99% isolated." A single leak is a failure.

NEGATIVE (must be zero):
N1. A member key cannot decrypt any fact not sealed to it. Count of cross-member decrypts that succeed: must be 0.
N2. A dyad-private fact cannot be decrypted by any key outside the owning dyad. Count: must be 0.
N3. After custody exit, the revoked custodian's old key cannot decrypt any re-sealed fact. Count of post-exit successful decrypts with the old key: must be 0.
N4. A dyad-private fact never appears in a household-scoped query result. Count: must be 0.
N5. No fact's DEK is sealed to an operator-held key. Count of operator-decryptable facts: must be 0. (This is the operator-blind invariant; it is meaningful only after Stage 4 phase 3, but the assertion exists from the start and is expected-red until then, tracked explicitly.)
N6. An unauthenticated identity claim is rejected on every write and read path. Count of admitted unauthenticated turns: must be 0. (Ties to REQ_IDENTITY_BINDING; this harness re-asserts it because crypto trusts identity.)

POSITIVE (must be complete):
P1. Every household-shared fact is decryptable by every household adult member. Count of household members who cannot read a household-shared fact: must be 0.
P2. Every dyad-private fact is decryptable by every current custodian of its dyad. Count of custodians who cannot read their own dyad's fact: must be 0.
P3. Every member-private fact is decryptable by its author. Count of authors locked out of their own fact: must be 0.
P4. The Stage 2 write-rule table (rows 1-9 of REQ_PARTITION_CUSTODY) classifies every row correctly. This is the partition's own acceptance table, run as part of the crypto harness.

## The red-team fixture

A seeded adversary member, "mallory", who is a legitimate household member (so her turns authenticate) but is NOT in any dyad and is NOT the author of the target facts. The harness drives mallory through every bypass and asserts each fails:

R1. mallory calls read on another member's member-private fact -> denied, no plaintext.
R2. mallory calls read on a dyad-private fact for a dyad she is not in -> denied.
R3. mallory presents a copied/replayed credential for another member -> rejected (identity layer).
R4. mallory requests a household query and checks whether any dyad-private fact leaks into the result set -> none do (N4).
R5. mallory, after being added then exited from a dyad, uses her old key on a re-sealed fact -> fails (N3).
R6. mallory attempts to write a fact AS another member (spoofed author) -> rejected.
R7. mallory reads the raw encrypted store directly (simulating operator/db access) and attempts decryption with every key she legitimately holds -> decrypts only her own facts, nothing else.

R7 is the operator-blind proof in miniature: it models what a curious operator with database access can actually read, which after Stage 4 phase 3 must be nothing but ciphertext for facts not hers.

## The ledger as audit trail

Every custody event (grant, exit, evict, re-encrypt) emits a HEL event. The harness asserts:
L1. Every custody state change has a corresponding, ordered, hash-chained ledger event.
L2. The ledger is append-only: no event is mutated or deleted after write.
L3. A custody exit's ledger event precedes the re-encryption it triggered (causal order preserved).

This makes custody changes provable after the fact, which is the legal surface the dyad spec flagged (dispute, estrangement, contested PoA).

## THE ACCEPTANCE TEST (for this REQ itself)

This REQ is MET when:
1. The harness runs as its own layer (proposed: L7-CRYPTO) inside eval.harness, invoked by --full.
2. Every invariant above is implemented as a pass/fail assertion with a count, not a rate.
3. Each invariant can be demonstrated to go RED by a deliberate fault-injection (a "break it on purpose" mode), proving the test can fail. A test that has never been seen to fail is not trusted.
4. The red-team fixture mallory is seeded and all R1-R7 assertions run.
5. N5 and the operator-blind invariants are present and tracked as expected-red until Stage 4 phase 3, not omitted.

## CONSTRAINTS

- This is a test harness. It reads the crypto layer; it does not implement it. If an invariant cannot be asserted because the mechanism does not exist yet (N5 before phase 3), it is written, marked expected-red, and tracked, never skipped.
- Counts, not rates. Every negative invariant is "must be 0"; every positive is "must be complete". No thresholds.
- Fault-injection mode is mandatory (acceptance item 3). An invariant that cannot be shown to fail is not evidence.
- The harness must run on the dev graph without touching production data or the live demo.

## DEMONSTRATION OBJECTIVE

We commit to passing this in front of a skeptical engineer, as a co-equal objective to the harness itself. We do not rig the build for it.

SHOW: The harness running as its own layer under --full, printing each invariant as a named pass/fail with a count. Then fault-injection mode: deliberately break isolation, re-run, watch the specific invariant turn red. Green, then provably-red, then green again.

LET THEM RUN: Hand the engineer the mallory fixture. Let them add their own attack case, a member, a fact, an attempt, and watch the harness classify and block it. Let them run R7 themselves: read the raw encrypted store as "the operator" and try to decrypt every fact.

THE CLAIM IT PROVES: "Our isolation is measured by counts, not vibes. Every leak is a failure the suite catches, and we can show you it catches them, because we break it in front of you."

THE HARDEST QUESTION + HONEST ANSWER: "Your test passes because you wrote it to pass. How do I know it can fail?" Answer: fault-injection mode. Every invariant is demonstrated red on a real injected fault before it is trusted. A test never seen to fail is not evidence, and we do not ship one. And the limit, stated first: this proves isolation at rest and in the database, not at inference time. The local model still sees plaintext at query time. That is a known boundary (enclaves are a later tier), not a gap we are hiding.
