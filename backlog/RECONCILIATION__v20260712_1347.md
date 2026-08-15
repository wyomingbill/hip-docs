# HIP Reconciliation Report
Status: BUILT
Reconciled-Against: main cfb774c, git log (30 commits), harness_baseline.json, docs/ tree
Produced: 2026-07-12 13:47 MT (read-only audit session)

---

## Quick Summary (2-minute read)

**What is done and committed:** Voice-path governance (BUILD-1, fbcd372), Phase B CandidateIntent cutover (7ff101f), P8 write monotonicity + P10 confirmation gate, ORTH-1/ORTH-2/VOICE conformance suites, WP Part II trust-boundary integration into both docx, TEST_HARNESS doc, D1_RECORD_SPEC v2 (1138 committed), DEMO-3 layout, DEMO-2 script drafts (5 scripts), GOVERNANCE_SCOPE_v1 locked doc, two household trust-circle market research pieces, SIO first-sentence fix (b0ba39d).

**What is open:** D-1 engine change (NOT-STARTED, gates everything downstream), DEMO-4 auto-run UI, TD-101b (/api/decrypt open), 7 architecture SVG diagrams (spec done, build not started), debt register NDA appendix untracked, D1_RECORD_SPEC v1005 untracked.

**What is red:** SIA Gate B 85.7% (target 90%) -- known, documented, Phase B cutover deferred pending Bill's call. three_zone_demo.T01 baselined false (stable acknowledged failure). No new regressions.

**What may have slipped:** The GYM_LOG noted D1_RECORD_SPEC as "not found." It now exists in two versions (v1005 untracked, v1138 committed). Backlog still says the spec was produced "this session" but marks it incorrectly as "missing" in item-2 -- needs backlog update. The HIP_DebtRegister_NDA_Appendix is uncommitted and unregistered in INDEX or MANIFEST.

---

## 1. Demo Track

| ID | Backlog Status | Verified Status | Evidence |
|----|---------------|-----------------|----------|
| D-1 | NOT-STARTED | NOT-STARTED | No harness/epistemic_record.py exists; no GAP-1..5 in injection_contract.py. Correctly labeled. |
| DEMO-2 | DONE (drafts, acc348e) | **DONE** | 5 JSON scripts in demo_scripts/ confirmed in acc348e. Wire to live data blocked on D-1. |
| DEMO-3 | DONE (123a110) | **DONE** | 123a110 adds HeaderBar to demo.html. HTTP 200 verified per GYM_LOG. |
| DEMO-4 | NOT-STARTED | NOT-STARTED | No /api/demo/start UI code. Server-side demo_run.run_script exists. Blocked on D-1. |
| DEMO-5 | NOT-STARTED | NOT-STARTED | Voice path now governed (BUILD-1), but no /demo surface rendering. Blocked on D-1 + DEMO-4. |
| D1_RECORD_SPEC | GYM_LOG says "MISSING" | **EXISTS (two versions)** | v1005 (untracked, from this session), v1138 committed at 1c717f5. GYM_LOG item-2 finding was correct at time of writing; v1005 was produced after the GYM_LOG was written. Backlog should acknowledge v1138 as committed. |

**D-1 sub-items (all NOT-STARTED, verified correct):**
D-1-core, GAP-1 through GAP-5, HARNESS-1, MIGRATE -- none of these exist as code in the repo. The spec is built; the build is not started.

---

## 2. Security Track

| ID | Backlog Status | Verified Status | Evidence |
|----|---------------|-----------------|----------|
| TD-101a | DONE (overnight item 2) | **DONE** | GYM_LOG item-5 confirms embed_text uses owner+attribute only; OVERNIGHT_LOG item 2 confirms three write paths all encrypt before logging. |
| TD-101b | DEFERRED | **DEFERRED (open)** | /api/decrypt at demo_dashboard.py:187-199 is still unauthenticated. Confirmed by reading code. HIP_DebtRegister_NDA_Appendix documents this explicitly as highest-severity open item. |
| TD-101c (GROQ rotation) | DROPPED | **DROPPED** | Key rotated externally; plist corrected during demo prep. Backlog notes this correctly. No code change was needed. |
| TD-101d (debt register mark) | NOT-STARTED | **NOT-STARTED** | Debt register (docs/techdebt/DEBT_REGISTER__v20260709_0855.md) still shows TD-101 as a single row without the a/b/c/d breakdown and without "RESOLVED" annotations for TD-101a/c. This is a documentation gap, low priority. |

---

## 3. Sales / Diligence Track

| ID | Backlog Status | Verified Status | Evidence |
|----|---------------|-----------------|----------|
| PKG-1 (WP Part II) | DONE (6f2f1d9) | **DONE** | bc4917e integrated trust-boundary into both docx; 6f2f1d9 updated MANIFEST; docs/deliverables/ has both v20260711_1830 versions. |
| PKG-2 (NDA diligence fixes) | DONE (6f2f1d9) | **DONE** | Same commit; MANIFEST Section B updated. |
| PKG-3 (diagram spec) | DONE (spec, da5b84b) | **SPEC DONE, BUILD NOT STARTED** | DIAGRAM_SPEC__architecture-visuals__v20260711_1809.md exists and committed at da5b84b. 7 SVGs specified (D1-D6 plus one). No SVG files exist in whitepaper/diagrams/export/ or source/. Backlog correctly notes "Build not started." |
| PKG-4 (TEST_HARNESS doc) | DONE (c87669b) | **DONE** | docs/research-technical/TEST_HARNESS__architecture-and-invariants__v20260711_1900.md committed. INDEX updated. |

---

## 4. Committed Work Not in Backlog

These commits landed after the GYM_LOG was written (after ~11:00 MT). All are from Bill's direct session.

| Commit | What | Backlog ref | Action needed |
|--------|------|-------------|---------------|
| 1c717f5 | D1_RECORD_SPEC v1138 committed (regenerated -- prior run did not persist) | GYM_LOG item-2 said MISSING; now EXISTS | Backlog needs update: D1_RECORD_SPEC is committed at 1c717f5 |
| fc5721a | GOVERNANCE_SCOPE_v1 LOCKED -- v1 principal taxonomy fence with OP-1..5 | Not in backlog at all | Add to Sales/Diligence track as reference doc; DONE |
| b0ba39d | SIO first-sentence extraction fix -- FAIL-06 G1 governance failure resolved | Not in backlog (SIA track item) | Add as SIA maintenance item DONE; G1 governance failures drop by 1 |
| cfb774c | Two household trust-circle market research pieces | Not in backlog | Add as DONE under market research reference |

---

## 5. Gate / Test Status

| Gate | Current State | Verified Against |
|------|--------------|-----------------|
| RATCHET (harness_baseline.json) | 82/83 pass, 1 baselined fail (three_zone_demo.T01) | baseline file read directly |
| Known-flaky | 2 entries: routing_showcase.T01, reveal_demo.R05 | baseline file read directly |
| L2:three_zone_demo.T01 | baselined false (stable, TD-115 ack misattribution) | BUILT annotation in TEST_HARNESS doc |
| ORTH-1 (disclosure, 39 cases) | ratcheted PASS (GYM_LOG item-5) | OVERNIGHT_LOG + eval/harness_baseline.json |
| ORTH-2 (schema, 46 cases) | ratcheted PASS (GYM_LOG item-5, e85699c) | same |
| VOICE conformance (VOICE-GOV-001..004) | ratcheted PASS (fbcd372) | baseline has VOICE:conformance |
| SIA Gate A (26/26 governance-critical) | **PASS** | SIA_SHIP_BAR doc; b0ba39d resolves 1 additional FAIL-06 failure |
| SIA Gate B (133 total, >=90% target) | **RED: 85.7% (114/133)** | SIA_SHIP_BAR doc; b0ba39d fixes phrase_free_supersede; FAIL-06 G1 fix reduces known-fail list by 1 -- but sia_trend.jsonl is on Mini so exact post-b0ba39d count is not locally verifiable |
| Phase B cutover decision | **DEFERRED, BILL'S CALL** | PHASE_B_READINESS doc (Gate B below 90% UX target) |

**SIA Red flag note:** Gate A passes (the governance gate); Gate B is below the UX target. This is a documented, stable state. b0ba39d (first-sentence extraction fix) addresses FAIL-06 which was a Gate A failure, but the 85.7% Gate B figure predates that fix. The post-fix Gate B number is not locally verifiable (sia_trend.jsonl lives on Mini). There is likely a small improvement from b0ba39d but Gate B is still below 90%.

---

## 6. Loose Ends Inventory

### GROQ key rotation
**Status: CLOSED.** Key rotated externally. Stale plist corrected during demo prep. Backlog marks TD-101c DROPPED. No further action needed.

### three_zone_demo.T01 baseline
**Status: STABLE ACKNOWLEDGED FAILURE.** Baselined false, TD-115. Ack misattribution -- maya says "Ray takes metformin," ack replies "YOU take metformin." This is a known model behavior. The TEST_HARNESS doc documents it. No regression path; stays in baseline as false.

### OP-1..5 open problems
**Status: DOCUMENTED, LOCKED.** GOVERNANCE_SCOPE_v1 (fc5721a) names all five:
- OP-1: Minors and consent gradients
- OP-2: Facts owned by a third party about a relationship between two members
- OP-3: Recipient-competence-aware disclosure
- OP-4: Contextually variable sensitivity
- OP-5: Coercion and duress detection
These are in the NDA via the open problems section. None are on the engineering roadmap (v1 scope fence). The LOCKED doc gates any scope extension on Bill unlocking.

### Strategy doc
**Status: NOT WRITTEN (was it specified?).** No file named STRATEGY or STRATEGIC_PLAN exists in docs/. The backlog does not list it as an item. The GYM_LOG does not mention it. The GOVERNANCE_SCOPE_v1 doc is the closest thing to a strategic scope statement. If there was a specific strategy document requested, it was not produced and is not in scope of any current backlog item.

### Market research
**Status: COMMITTED (cfb774c).** Two pieces committed: external analysis (unverified, broader modeled estimates) and session-deep-research run (26 sources, 25 claims adversarially verified, 24 confirmed 3-0). These are not in the current backlog. They should be added. The existing research-market/ corpus (6 docs from 2026-07-06) remains BUILT.

### Demo modes / diagrams unbuilt
**Status: SPEC DONE, BUILD NOT STARTED.**
- 7 SVG architecture diagrams: spec at DIAGRAM_SPEC__architecture-visuals__v20260711_1809.md (da5b84b). Zero SVGs built. PKG-3 correctly notes "Build not started."
- Demo auto-run (DEMO-4): NOT-STARTED. Server-side runner exists (demo_run.run_script). UI wire-up not started.
- Demo voice mode (DEMO-5): NOT-STARTED. Blocked on D-1 + DEMO-4.

### HIP_DebtRegister_NDA_Appendix untracked
**Status: UNTRACKED AND UNREGISTERED.** File exists at docs/deliverables/HIP_DebtRegister_NDA_Appendix__v20260711_2312.md (2312 timestamp = 2026-07-11 23:12). Not in git, not in MANIFEST Section B (binary deliverables table doesn't list it), not in INDEX. This is an orphaned artifact by MANIFEST governance rules. It should be committed and registered before any diligence package goes out.

### D1_RECORD_SPEC version confusion
**Status: RESOLVED, NEEDS BACKLOG CLEANUP.**
- v1005 (untracked): written in the previous context window (this session, ~10:07), never committed. Content exists on disk only.
- v1138 (committed, 1c717f5): the regeneration Bill ran after the GYM_LOG noted the spec was missing. This is the canonical version in git.
- Backlog item-2 says "NOT FOUND" -- that was accurate at 11:00 MT. As of 1c717f5 it is found and committed.
- The v1005 file on disk is a prior-session artifact. It should be committed (registering two versions per naming law) or deleted. It is not registered in INDEX.

### BUILD-1 voice scope in WP MANIFEST
**Status: CORRECTLY NOTED, NOT STALE.** The MANIFEST Section C for Part II (harness scope) includes the explicit caveat: "Voice-path hardening to run that same enforcement chain end to end is open engineering work, tracked in the debt register as Code Review Finding 4." fbcd372 (BUILD-1) shipped after that MANIFEST note -- the caveat has been resolved by BUILD-1. The MANIFEST note predates fbcd372 and should be updated to reflect that BUILD-1 closes "Code Review Finding 4" for the voice injection-contract bypass. This is a minor MANIFEST stale item; the WP is not wrong, just no longer fully current in that footnote.

---

## 7. Recommended Backlog Updates

The canonical backlog (BACKLOG__v20260712_1100.md, pointed to by LATEST_BACKLOG symlink) needs these corrections before the next session:

1. **D1_RECORD_SPEC item-2:** Mark as DONE (1c717f5). The v1138 version is committed.
2. **Add GOVERNANCE_SCOPE_v1:** DONE (fc5721a). Sales/Diligence track or general reference.
3. **Add b0ba39d SIO fix:** DONE (b0ba39d). Minor item; SIA maintenance.
4. **Add market research:** DONE (cfb774c). Two pieces.
5. **Add PKG-5 HIP_DebtRegister_NDA_Appendix:** OPEN -- commit + register in MANIFEST + INDEX.
6. **Flag MANIFEST stale note:** BUILD-1 closed Code Review Finding 4; update MANIFEST Part II harness-scope caveat.
7. **Add v1005 D1_RECORD_SPEC disposition:** Either commit (two-version naming law) or delete (prior-session artifact superseded by v1138).
8. **Add SVG diagrams as open item:** PKG-3 is spec-DONE, but the actual SVG build should be a separate NOT-STARTED item so it does not appear done.

---

## 8. Nothing Found That Is Broken Unexpectedly

- No regressions in baseline beyond the known three_zone_demo.T01 false.
- No known-flaky count change (still 2).
- SIA Gate A clean (even with FAIL-06 now fixed in b0ba39d, Gate A was already PASS before).
- BUILD-1 voice governance conformance is gated and green.
- Phase B cutover is explicitly deferred, not stale or forgotten.
- TD-101b (/api/decrypt) is open, known, deferred, documented in the NDA appendix. The constraint (local-only or VPN, no public internet exposure) is documented.
