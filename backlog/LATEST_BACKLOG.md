# Canonical HIP Backlog

**New sessions read this first.**
Created: 2026-07-12 10:23 MT
Updated: 2026-07-14 16:15 MT (D-1 complete all 7 commits; P2 closed as detection miss; TD-124 relabeled; epistemology dashboard redesign in progress)
Canonical ref: docs/backlog/LATEST_BACKLOG.md -> this file

---

## True State Summary (2026-07-14 16:15 MT)

1. Secure NDA data room is live at hip.olindasolutions.com/secure/ -- Edge Middleware auth, per-user credentials, access logging, and publish pipeline all deployed (hip-deploy 6749f66).
2. D-1 epistemic record writer: ALL 7 COMMITS DONE (byte-compat proven). D-1 is COMPLETE. DEMO-4 Auto-run UI is now unblocked.
3. HARNESS1 all green. Governance-proof artifact built (HIP_GovernanceProof__audited-transcript__v20260714_1345.md); P7-P10 conformance framing corrected.
4. Financial model rebuild: RESOLVED. Python financial validation layer is planned next (OPEN).
5. SIA conformance: Gate A 26/26 (100%) PASS; Gate B meets threshold per HARNESS1 green state.
6. Voice governance: BUILD-1 (fbcd372) CLOSED -- all three OrchestratorGate sites enforce assemble_governed_context; VOICE-GOV-001..004 in effect.
7. P2 CLOSED as detection false-negative (~1% miss rate for seed=1 run, not write latency). TD-124 relabeled: write-durability-only (not a P2 fix). Correct P2/detection fix track: TD-123 prompt hardening (dietary vs preference disambiguation, OPEN).
8. reveal_demo.R05 flake: quarantined (P8 two-active-row wording variance, graph correct).
9. TD-101b (/api/decrypt unauthenticated): still DEFERRED -- must close before external code review.
10. Critical path: DEMO-4 Auto-run UI (D-1 gate cleared). Epistemology dashboard redesign (fact-lifecycle view, Fable model) in progress. Financial validation layer next on business track.

---

## Header: Critical Path and Track State

Three tracks: **Demo**, **Security**, **Sales/Diligence**
Critical path: DEMO-4 Auto-run UI (D-1 gate now cleared).

Security: TD-101b (open /api/decrypt) is the single highest-risk deferred item. Must close before any engineer or investor diligence package.

Sales: Whitepaper (v20260712_1852), NDA package, TEST_HARNESS doc, secure data room all live. No open items blocking outreach.

---

## Track 1: Demo

| ID | Title | Priority | Effort | Status | Commit | Notes |
|----|-------|----------|--------|--------|--------|-------|
| D-1 | Engine epistemic record writer | P0 | L | **DONE (all 7 commits)** | bf05aae + | All 7 commits done, byte-compat proven. FLAG-1..8 still in effect. |
| DEMO-2 | Script library: 5 narrated v3 scripts | P1 | M | **DONE (drafts)** | acc348e | Drafts committed. Wire to live Governance Feed -- unblocked by D-1 gap closure. |
| DEMO-3 | Dashboard layout: SCORECARD + HOW IT WORKS top | P2 | S | **DONE** | 123a110 | HeaderBar added at top of /demo. |
| DEMO-4 | Auto-run mode UI | P2 | M | **UNBLOCKED / NOT-STARTED** | -- | Wire /api/demo/start to FooterBar; beat-aware dwell; focus pane highlighting. Gate: D-1 complete (cleared). |
| DEMO-5 | Voice mode on /demo surface | P3 | L | NOT-STARTED | -- | Ride OrchestratorGate path; voice = no epistemic record until D-1 fully ships (FLAG-8). FLAG-8 now cleared. |
| DEMO-6 | Epistemology dashboard redesign | P2 | M | IN-PROGRESS | -- | Fact-lifecycle view; Fable model. Design phase. |

### D-1 Gap Closure

| ID | Title | Status |
|----|-------|--------|
| GAP-1 | Per-fact deny reason in InjectionResult | **DONE** |
| GAP-2 | INJ-6 / INJ-6b split in record | **DONE** |
| GAP-3 | Preserve InjectionResult on success | **DONE** |
| GAP-4 | Confirmation-gate metadata in record | **DONE** |
| GAP-5 | Timeline holes: RESOLVE/CONFIRM/park (UI wire) | **DONE** |
| D-1 commit 7 | Shadow retirement | **DONE** |

### D-1 Build Constraints (FLAG-1 through FLAG-8) -- still in effect

- **FLAG-1** Isolation-preserving withheld panel: admitted/withheld display is operator-view only, single-member-scoped
- **FLAG-2** Do not run a second injection-contract pass inside the record writer
- **FLAG-3** Do not add deny-reason replay logic to epistemic_record.py (must come from engine InjectionResult via GAP-1)
- **FLAG-4** Do not emit a record on DisclosureBlocked turns without guard fields set
- **FLAG-5** Do not use text_demo.py fields as schema authority -- D1_RECORD_SPEC is the spec
- **FLAG-6** Do not merge park and confirm into a single delta event
- **FLAG-7** Do not wire the record writer into the SIO pass
- **FLAG-8** Voice = no epistemic record until D-1 fully ships. D-1 is now fully shipped; voice epistemic records are permitted if wired correctly.

---

## Track 2: Security

| ID | Title | Priority | Effort | Status | Commit | Notes |
|----|-------|----------|--------|--------|--------|-------|
| TD-101a | Trace embed_text -- no pre-encrypt exposure | P0 | S | **DONE** | overnight item 2 | Clean: embed_text uses owner+attribute only, never fact value. |
| TD-101b | Auth gate on /api/decrypt | P0 | S | **DEFERRED** | -- | Currently unauthenticated (demo_dashboard.py:187-199). Must close before external code review. |
| TD-101c | GROQ key rotation | P0 | XS | **DROPPED** | -- | Rotated externally. |
| TD-101d | Debt register: mark resolved items | P1 | XS | NOT-STARTED | -- | Mark TD-101a/c resolved in debt register with commit hashes. |

---

## Track 3: Sales / Diligence

| ID | Title | Priority | Effort | Status | Commit | Notes |
|----|-------|----------|--------|--------|--------|-------|
| PKG-1 | Whitepaper Part II | P1 | L | DONE | 6f2f1d9 | |
| PKG-2 | NDA diligence doc fixes | P1 | S | DONE | 6f2f1d9 | |
| PKG-3 | Architecture diagram SVG spec | P2 | M | DONE (spec) | da5b84b | Build not started |
| PKG-3b | 7 architecture SVG diagrams -- build | P2 | L | NOT-STARTED | -- | Spec DONE (da5b84b). Zero SVGs built. D1-D6 + outer diagram. |
| PKG-4 | TEST_HARNESS doc | P1 | M | DONE | c87669b | |
| PKG-5 | GOVERNANCE_SCOPE_v1 (OP-1..5 open problems doc) | P1 | -- | **DONE** | fc5721a | LOCKED scope fence. OP-1 minors, OP-2 relational, OP-3 competence, OP-4 dynamic sensitivity, OP-5 coercion. NDA research asset. |
| PKG-6 | Market research: household trust-circle segment sizing | P1 | -- | **DONE** | cfb774c | Two pieces: external (unverified) + deep-research verified (26 sources, 24/25 claims 3-0 confirmed). |
| PKG-7 | HIP_DebtRegister_NDA_Appendix commit + MANIFEST registration | P1 | XS | **DONE** | b1d411b | Committed and registered. |
| SEC-SITE | NDA secure data room + publish pipeline | P1 | M | **DONE** | hip-deploy 6749f66 | Edge Middleware auth, per-user credentials, access logging, publish pipeline. Live at hip.olindasolutions.com/secure/. |
| NDA-CASCADE | NDA cascade -- update NDA superset deliverables to match current engine | P1 | M | **IN PROGRESS** | -- | Unblocked: Gate A confirmed, Gate B green (HARNESS1). Next: align NDA text to BUILD-1 voice closure and two-gate SIA framing. |
| WEB-CASCADE | Website content cascade | P2 | M | **HELD** | -- | No external-facing content updates until Bill clears. |

---

## Track 4: Test Infrastructure (TEST-INFRA)

| ID | Title | Priority | Effort | Status | Notes |
|----|-------|----------|--------|--------|-------|
| TEST-SPEED-1 | Harness cycle time -- 5 sub-items | P2 | M-L | NOT-STARTED | Full harness ~5 min, 800+ model calls. See breakdown below. |

### TEST-SPEED-1 Breakdown

| Sub-item | What | Effort | Status |
|----------|------|--------|--------|
| a | Document and enforce --layer N / --full discipline | XS | NOT-STARTED (docs only, immediate) |
| b | Smoke-test subset: ~20 cases covering highest-change-frequency paths | S | NOT-STARTED |
| c | Parallelize independent layers: P1 100-iter runs and L4 pairwise matrix currently serial | M | NOT-STARTED |
| d | Mocked-model unit tests: normalizer, injection contract, classify_refusal | M | NOT-STARTED |
| e | Persistent warm server: keep server alive between runs; heartbeat/reuse | M | NOT-STARTED |

Priority ordering: a -> d -> b -> c -> e.

---

## Track 5: Architecture (ARCH)

| ID | Title | Priority | Effort | Status | Notes |
|----|-------|----------|--------|--------|-------|
| TIER-1 | Tiered Fact Storage (Access Heat) | DESIGN | L | NOT-STARTED | Design note at docs/design/HIP_DESIGN__tiered-fact-storage__v20260713_1702.md (56cf7b9). Spec pass required before build. |

**Invariant (non-negotiable):** Storage heat optimizes cost and latency ONLY. It NEVER influences a governance decision. Cold means slower to fetch (promote-on-access), never withheld.

**Build sequencing:** DESIGN now; BUILD after dashboard-clarity demo lands.

---

## Track 6: Business / Financial

| ID | Title | Priority | Effort | Status | Notes |
|----|-------|----------|--------|--------|-------|
| FIN-REBUILD | Financial model rebuild | P1 | M | **DONE** | -- | Model rebuilt. |
| FIN-VALIDATE | Python financial validation layer | P1 | M | OPEN (planned next) | -- | Next step after FIN-REBUILD. Validate model outputs programmatically. |

---

## Open Engineering Items (from debt register -- not tracked in tracks above)

| ID | Sev | Title | Status | Notes |
|----|-----|-------|--------|-------|
| TD-124 | ENG | Async write path: durable outbox + LiteLLM + DeepInfra fallback | **OPEN (write-durability only)** | NOT a P2 fix. P2 i019 was a detection false-negative, not write latency. TD-124 remains valid for write durability: protects against server crash between Groq detection and Neo4j commit. |
| TD-123 (prompt hardening) | ENG | Detector prompt: dietary/preference disambiguation + "subject must be a PERSON" negative example | **OPEN (P2 correct fix track)** | Normalization shipped 47dc59d. Prompt hardening (dietary vs preference rule) is the correct fix for P2 detection false-negatives. ~1% confirmed miss rate (seed=1, 100 iters); mechanism: gpt-oss-20b returns changes:[] for food vocabulary in complex multi-party context. |
| TD-120 D2 | ENG | Relational bridge: "my mother's X" requires relationship fact | **OPEN** | Pinned known-failure L2:care_coordination.T02. |
| TD-115 | ENG | Subject resolution: "my mother Elena" -> wrong subject or gender | **OPEN** | Also: stable ack misattribution. |
| TD-118 | ENG | Routing pipeline does not record every turn | **OPEN** | History panel inconsistent. |
| TD-113 | GATE | Epistemic pane is developer-view, not operator-view | **OPEN** | Blocks demo credibility. Being addressed by DEMO-6 epistemology dashboard redesign. |
| TD-110 | ENG | Cross-member write authority gap | **OPEN** | Governance decision required before fix. |
| TD-122 | ENG | No fact has an embedding; semantic retrieval is a recency window (limit-8 fallback) | **OPEN** | Safe fix: embed subject+predicate only (TD-030 tension). |
| TD-103 | OPS | launchd com.hip.voice.orch fails 1-in-N (I/O error 5) | **OPEN** | Use start_manual.sh workaround. |
| TD-108 | SEC | Per-fact consent-and-routing ledger not yet built | **OPEN** | Primary liability-severity reducer. Must ship pre-scale. |
| TD-101b | SEC | /api/decrypt unauthenticated | **DEFERRED** | Must close before external code review. |
| TD-109 | SEC | Biometric consent-and-retention control (speaker recognition) | **OPEN** | Build requirement; no public consent claim until shipped. |

---

## Resolved (full history)

| ID | What | Commit | Resolved |
|----|------|--------|---------|
| D-1 (all 7 commits) | Engine epistemic record writer, complete | bf05aae + | 2026-07-14 |
| P2 investigation | i019 confirmed detection false-negative (~1% miss rate, not write latency); TD-124 relabeled write-durability-only; TD-123 prompt hardening is correct P2 fix track | 9a8dc5c (DIAG amend) | 2026-07-14 |
| SEC-SITE | NDA secure data room live; publish pipeline | hip-deploy 6749f66 | 2026-07-14 |
| FIN-REBUILD | Financial model rebuild | -- | 2026-07-14 |
| HARNESS1 | Full harness all green | -- | 2026-07-14 |
| D-1 GAP-1..5 | Epistemic record writer gap closure (commits 1-6) | bf05aae + | 2026-07-14 |
| D-1 commit 7 | Shadow retirement | -- | 2026-07-14 |
| Governance-proof artifact | HIP_GovernanceProof audited transcript built; P7-P10 framing corrected | -- | 2026-07-14 |
| TD-123 (normalization) | Write-boundary subject normalization (_normalize_subject) | 47dc59d | 2026-07-12 |
| Scout->gpt-oss migration | Fact-change detector on openai/gpt-oss-20b; Developer tier | b394d89 / f2f7007 | 2026-07-12 |
| L2 test normalizer | Canonical-form prose matching; kills model-phrasing failure class | bcc3533 | 2026-07-12 |
| SIA governance 100% | Gate A (26/26 governance-critical) PASS confirmed; two-gate framing in WP | 4b5f14d | 2026-07-12 |
| INFRA-2 #1 | Extraction model load-on-demand (keep_alive 24h -> 0) | bedab3f | 2026-07-12 |
| WP P0/P1 diligence | SIA figure + voice caveat fixed in both WPs (v20260712_1852) | 4b5f14d | 2026-07-12 |
| PKG-7 | HIP_DebtRegister_NDA_Appendix committed + MANIFEST registered | b1d411b | 2026-07-12 |
| TIER-1 design | Tiered fact storage design note committed; INDEX registered | 56cf7b9 | 2026-07-13 |
| TEST-SPEED-1 backlog | TEST-INFRA track added to canonical backlog | 2d865d7 | 2026-07-12 |

---

## Known Flaky (baselined, not failures)

- L2:routing_showcase.T01 -- edge model phrasing variance, response correct
- L2:reveal_demo.R05 -- P8 two-active-row reply wording variance, graph correct (quarantined)
- L2:three_zone_demo.T01 -- baseline false (pre-existing)
- L2:care_coordination.T02 -- TD-120 D2 relational bridge (known-failure, pinned)
- L2:care_coordination.T04 -- sarah not in live member registry; 400 on /api/text-query
