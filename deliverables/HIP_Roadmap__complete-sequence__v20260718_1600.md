# HIP Roadmap: Complete Sequence
Version: v20260718_1600
Status: **SUPERSEDED** (was PLAN OF RECORD) — superseded 2026-08-11 by
`HIP_FinishPlan__three-finish-lines-14-steps__v20260811.md` (Bill's instruction, HA-37).
**Retained unaltered below this header.** It sequenced the confidentiality and truthfulness
builds and that account is still the record of what was decided in July; it is no longer what
the project is executing. The old status is left visible rather than overwritten, per the
correction class: a reader meeting a citation to this doc should be able to see both what it
was and that it was replaced.
Branch: roadmap
Reconciled against: main 688386f; crypto design 47851d7; dyad spec 601ac25; REQ_IDENTITY_BINDING e1888e0

## What this is

The plan of record for two builds: confidentiality and truthfulness. The handoff cited a doc at this path dated _1200. It was never written. This is it, written after reading both specs at file:line. It sequences the work and records the decisions. It builds nothing.

## Two problems. Keep them separate.

Confidentiality: can the wrong person read a fact. Today there is no protection. Member isolation is a database filter over data the server can always decrypt, because one master key derives every member's key. A filter, not a wall.

Truthfulness: does HIP say true things, and does the harness catch it when it does not. The fail-open routing fix, the decision table, G0, calibration, harness phases 2 through 7.

They share one piece: identity binding. Crypto is only as strong as "this is really Maya's device." A fact is only true relative to whose fact it is. Fix identity once, both move.

## Identity binding is device binding

Decided. The device key is the root. Not voiceprint, not a session token on its own. Device binding is the only mechanism that proves identity today and carries the custodian's key tomorrow. Build it once.

Identity is possession of the member's device keypair: the same X25519 and Ed25519 keypair the crypto build puts on the device. Sessions derive from the device key; a session is never issued without it. Stage 1 is the first brick of crypto, not a throwaway. Stage 1 proves who is speaking, nothing more. The keypair carries forward instead of getting thrown away.

Voiceprint stays a hint (TD-127), not the identity root.

## Decisions made this session

1. Identity is device binding.
2. Uncertainty defaults to private. When the classifier is unsure or extraction fails, a fact seals to the author, not the household. This matches fail-closed on the truth track: when unsure, withhold, on both axes. Cost: some facts that should be shared land private until the owner re-shares. The member directive is the release valve.
3. The partition rule is settled by the specs, not open. Three classes, deterministic write rule. See Stage 2.

## Decisions still open

1. Quorum composition. Who holds the three shares of the 2-of-3 recovery split. The same quorum that recovers a key also evicts a custodian: contested power of attorney, suspected abuse, death. The composition is the governance. Pick it so no single party can complete a custody change alone. This is Bill's call, legal and policy, at Stage 4. Not a blocker now.
2. SIA cutover on the truth track. Later, at Stage 5.

## The sequence

Stage 0: branch and consolidate. Done. roadmap branched off main at 688386f. Both specs committed. REQ_IDENTITY_BINDING filed at e1888e0. The ~/hip-roadmap worktree exists so the two tracks never collide.

Stage 1: identity binding. REQ filed, build not started.
Requirement (Bill, verbatim): "The system has to actually check who's talking before it trusts them, and you can't fake being someone else, but I can still demo all three members on one box."
Scope: single speaker, one member per turn. No shared-device conversation this sprint. That is later; device binding leaves the door open. Do not build speaker arbitration.
Enrollment: keys are generated at enrollment. Enrollment is operator-approved for the demo. The demo fixture pre-enrolls bill, maya, and sam. The build does not invent its own enrollment. Unmanaged enrollment is the hole that makes the credential check theater.
Passes when: a turn with no valid credential is rejected, not answered as that member; a forged credential is rejected; voice admits only on a proven credential; a valid credential for bill, maya, or sam is admitted and the presenter can switch among all three on one box with the demo unchanged; no path admits an unverified identity.

Stage 2: partition and custody. Ratify, do not design. The specs define three classes (household-shared, dyad-private, member-private) and a first-match write rule: member directive, then attribute equals household, then high or critical sensitivity defaults to private, else shareable. Decision (a), the uncertainty default, is decided: private. Decision (b), quorum composition, is open, at Stage 4. Blocks neither Stage 1 nor Stage 5.

Stage 3: crypto harness. Its own REQ, written after the partition, because the invariants depend on what private means. Infrastructure, not feature.
Hard-zero, pass or fail: the wrong member or dyad cannot decrypt; a revoked key fails after exit; a dyad-private fact never lands in a household query; an unauthenticated identity is rejected.
Positive half: a fact that should reach the household does. Fail-private over-walls if nobody watches. This catches it, the same way the truth harness has to catch a system that refuses everything.
Red-team fixture: a seeded adversary member tries every bypass, the harness asserts each one fails.
Ledger events (HEL) are the custody audit trail: grant, exit, re-encrypt.

Stage 4: crypto build. Each phase is REQ, build, extend the harness, merge. Order: dyad custodial keys; partition sealed (the roughly 11 server-side key-derivation sites, encryption.py:117-123 the chief one and the linchpin); operator-blind at rest (destroy the master key); recovery and custody exit (the 2-of-3 quorum, one primitive for both). Migration is dual-envelope by key_version: v1 and v2 coexist, four phases, no flag day. The operator-blind claim is made only when the master key is actually destroyed.

Stage 5: truth build. Parallel after Stage 1, no crypto dependency. SIA, the D-01 fail-open fix via SIA Phase B, the decision table, G0, calibration, harness phases 2 through 7. Done when --full passes with G0 wired and hard-zero, and the fail-open rate is on the dashboard.

UPDATED 2026-07-21 (deliberate variance from this plan, Bill-confirmed): the Stage 5 truth REQ is now REQ_CONFIDENCE_DISCIPLINE__truth-track__v20260721_0840, not REQ_TRUTH_TRACK. REQ_TRUTH_TRACK (filed 2026-07-19, phases A-G + T02/D-24) is SUPERSEDED in place -- its own header says so, retained for history. Reason for the variance: REQ_CONFIDENCE_DISCIPLINE was independently ratified 2026-07-21 as the broader confidence-vs-policy architecture (perception-stage typed uncertainty, dominance propagation, deterministic answer-mode selection, G0) that this Stage's truth work sits inside; a phase-ownership map (Bill-confirmed) showed REQ_TRUTH_TRACK's phases A/C/D were already covered or extended by it, and phases B (SIA + 14.3% baseline), E (calibration measurement), F (six remaining truth metrics), G (full ratchet taxonomy: monotonic / opposite-polarity / hard-zero G0-G1-G4), and the T02/D-24 decision were folded in verbatim so nothing was dropped. Stage 5's acceptance bar is unchanged: --full passes with G0 wired and hard-zero and the fail-open rate on the dashboard -- only which REQ document defines "done" has changed.

UPDATED 2026-07-21 (deliberate variance from this plan, Bill-approved): Stage 4's "partition sealed" phase, as originally named above, split into two REQs as the ratified policy grew past what that single phase name described. Neither REQ is renamed by this note; this records which already-filed REQ covers which half.
- (2a) crypto sealing MECHANISM -- REQ_CRYPTO_P2_PARTITION_SEALED__stage4-phase2, MET at 1e549a8. Its acceptance test proved the sealing chokepoint itself: DEKs sealed by class, zero server-derivable keys (PS1-PS4, verified via layer-7, `== L7: 19/19`).
- (2b) write-time classification LOGIC -- REQ_WRITE_TIME_CLASSIFIER__stage4-phase2, filed NOT MET at cfc9e2b. This is the piece "partition sealed" always meant but never built: the code that decides which class a fact gets before (2a)'s sealing runs. It grew to cite the ratifications accumulated on REQ_PARTITION_CUSTODY since (2a) was written and merged -- #1 dyad access model, #2 household-circle, #3 role separation, #6 custody governance -- none of which existed when (2a)'s own acceptance test was authored.
Both REQs keep the literal "stage4-phase2" slug in their filenames -- that duplication is the reason this note exists, not a defect this note fixes. Order going forward: (2a) stays MET and untouched; (2b) is the next build in this Stage.

UPDATED 2026-07-26 (status against this plan, three items; the stage sequence itself is unchanged):
- Stage 5, G0: MET at edb0791 (REQ_G0_OUTPUT_INVARIANT__output-side-fabrication-backstop__v20260726_0735). Both artifacts of the one condition exist and run: the runtime reply gate at process_text_query's single true model-generation exit (reply_source=="model" only -- deterministic template exits are exempt by documented design) and the layer-7 ABSOLUTE-tier standing invariant, auto-run on every --layer 7/--full, --accept mechanically refused. All four acceptance items evidenced live, including a real monkeypatched-model fabrication blocked and a grounded reply passing untouched. Stage 5's remaining scope (SIA cutover, calibration, the rest of REQ_CONFIDENCE_DISCIPLINE's phases) is unchanged by this; G0 was its named hard floor and the context-architecture learning half's precondition (i).
- Stage 4, phase 3 (operator-blind at rest / REQ_CRYPTO_P3_OPERATOR_BLIND part (c)): PROVEN, not yet MET. The plan's own bar -- "the operator-blind claim is made only when the master key is actually destroyed" -- is now satisfied on roadmap: after OB5 (hard-refusal on missing key, 4286517) and a decoupled roadmap-own key path (a430df5), the master key was destroyed Bill-authorized (backed up sha256-verified, overwritten then unlinked) and N5/R7 were proven directly against the 12 live facts (N5: 12/12 raise with no key in existence; R7: 12/12 open via the real class-key path with zero master key present) at b3e2368. The REQ stays NOT MET on purpose: "prove it live" is not "the full ratchet passes" (CLAUDE.md item 12) -- step 5's harness verification does not yet run clean because PS1-PS4's fixture-builders construct v1 facts that are now categorically impossible on roadmap (retire/rework decision made, being executed by the crypto session). Mark this phase MET in this plan ONLY on that session's reported MET hash, not before. Scope boundary unchanged: this is roadmap's key; hip-dev/demo's master key is REQ_DEMO_DASHBOARD_MIGRATION's separately scheduled job, untouched.
- New, deliberate variance (an addition to the Process layer, resequencing nothing): REQ_HARNESS_DISCIPLINE__four-part-check-standard-and-sprint-gate__v20260726_0827 filed (a2b0ebe) and its audit BUILT (003fd9c, 7730044). Every gated check must carry a fault-injection twin, a ground-truth fixture, a coverage entry, and a metamorphic wrapper -- re-asserted at sprint start as a gate, not a memory. The standing audit (eval/harnesslib/check_registry.py + harness_audit.py) enumerates all 52 L6/L7/L7V2 checks on every --full, verifies declarations against source/roster/executable probes, mechanically rejects a twin-less check (proven red-on-command with a synthetic injection every run), and prints 54 registered gaps as TD-133 -- zero HIDDEN gaps, not zero gaps. Reference implementations passing all four: PS1/PS2/OB4/OB5/G0/G1-G4. The REQ itself stays NOT MET until a post-destruction --full runs green without any env override (same gate as phase 3 above; the two close together).

## Branch rules

main is the demo, at ~/hip-dev. The demo session owns it. Do not touch its tree.
roadmap is this work, at its own worktree ~/hip-roadmap. No branch switching, so the tracks cannot collide.
The branch shows in the prompt. Merge main into roadmap before each build phase. Add files by explicit path, never git add -A. roadmap replaces main as the demo when stable.
On a merge conflict: demo files resolve to main, crypto and identity files resolve to roadmap, anything else goes to Bill. Never resolve a conflict outside those two sets silently.

## What this does not protect

1. Not blind at inference. Plaintext sits in edge-host RAM at query time so the model can answer. A compromised edge host reads what it processes. Everything here protects data at rest, not during a query. Enclaves are a later tier, out of scope. Say this first.
2. Author-keyed, not subject-keyed. A fact about the parent, written by the caregiver, is walled to the caregiver. The dyad makes the caregiver the custodian who holds the key for the parent, so the parent's facts seal to the pair. This relocates trust to the custodian. It does not remove it. Who can read Dad's medical facts: his caregivers, by design, no one else.
3. Metadata is cleartext. Owner, subject, attribute, sensitivity, timestamps: all queryable. Only the value is sealed. For eldercare the care-relationship graph is both cleartext and the operator's most valuable signal. Name it.
4. Embeddings leak. Computed from plaintext, stored server-side for search, partially reversible.
5. Recovery stops the operator acting alone, not a coalition. Two shares decrypt. One does not.
6. Exit is a forward boundary, not an eraser. Revocation kills future access. It does not retract what a custodian already read.
7. Sensitivity drives the crypto class, and sensitivity comes from a 7B model. Guardrails: the member directive overrides it, the default is private, and the worst case is shared inside the household, never leaked to the operator.
8. Operator-blind fights the operator's own interest: support, analytics, upsell. That tension is the trust claim. It is a sales conversation, not an engineering one.

## Process

Requirement before code, from Bill's words, no retroactive requirements.
A dispatch doc for every finding and build, registered.
Done means the full ratchet passes, not a narrow proof. The full run takes about 30 minutes. Batch crypto verification.
Verify before reporting.
Every doc gets an INDEX entry and, if a deliverable, a MANIFEST Section B entry, in the same commit. Unregistered is an orphan. A download is not filing.
Every dispatch starts with whoami, hostname, and a branch check.

## Committed docs

Crypto design: HIP_MemberIsolation__crypto-partition-and-recovery-design__v20260718_1117.md (47851d7)
Dyad spec: HIP_MemberIsolation_Dyads__custodial-crypto-entry-exit-overlapping__v20260718_1207.md (601ac25)
Isolation trace: DISPATCH_ISOLATION_TRACE__per-member-enforcement-mechanism__v20260718_1002.md
Stage 1 requirement: REQ_IDENTITY_BINDING__device-binding__v20260718_1530.md (e1888e0)
Backlog: docs/BACKLOG.md
Rules: CLAUDE.md
This doc replaces the never-written _1200 and is the plan of record.
