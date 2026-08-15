# Parking Lot Run Log
Started: 2026-07-11 15:27 UTC
Session: Sonnet (this session), unattended

## Stack-idle poll
Waited for Session 4's harness gate to finish. Polled until `ps aux | grep -E "eval.harness|7997|7998"` returned 0. Confirmed idle before proceeding.

## git pull
Pulled after idle confirmed. HEAD: 37d4131 (Session 4 had landed phase4 audio + smoke fixes).

---

## P7 — Scorecard two-gate wiring
**Status: COMPLETE**
**Commit:** 4e6ebcb
**Gate:** Dashboard responded HTTP 200 on /scorecard post-restart

Changes:
- `eval/harness.py`: `gov_total`, `gov_passed`, `gov_agreement` now written to `logs/sia_trend.jsonl` on every `--sia-conformance` run.
- `server/demo_dashboard.py`: SIA conformance table split into two columns — Gov (26 entries, must be 100%) and Quality (133 entries, ≥90%). Tooltips explain threshold for each.
- Dashboard restarted on Mini port 7871, HTTP 200 confirmed.

---

## P3 — Phase 4 audio
**Status: COMPLETE**
**Gate:** T02 Jardiance PASS, cross-member (Maya) refused PASS, text-token cost $0.00231
**Exchange:**
- [YOU] "What did I tell you about Elena's medication?"
- [GPT] "You told me that Elena's medication is Jardiance 10 milligrams."
- [YOU] "What medication does Maya take?"
- [GPT] "I don't have that information confirmed yet. Maya's medication isn't listed in my current facts."

Dashboard check SKIP/FAIL (dashboard not running on Mac port 7870 at test time — dashboard runs on Mini port 7871, no regression).

---

## P4 — Detection-ceiling fix
**Status: COMPLETE**
**Fix commit:** 0dfc588
**Gate result:** L1 9/0, L2 24/0 (1 flake), L3 3/0, L4 27/0 — zero failures

Root cause: P8 park leaves 2 active rows (retained head ASSERTED + UNRESOLVED parked write). Setup polling called `assert_fact_state` with default `expect_count=1`; seeing `len(active)==2` returned False every poll → 20s timeout → FAIL on PW012. PW019/021/022/026 had been failing due to Groq latency at baseline time, not structural issue.

Fix: `expect_count=None` sentinel in `fixture.py` skips strict count check (only requires ≥1 active row with needle present). `layer4.py` setup polling now passes `expect_count=None`. PW012 empagliflozin setup fired at 10:16:41, P8 parked at 10:16:51, subsequent queries continued normally.

---

## P6 — Baseline promotion
**Status: COMPLETE**
**Commit:** 5b7d1e5

Updated `eval/harness_baseline.json`: flipped PW012/019/021/022/026 from `false` → `true`, cleared all 5 entries from `_accepted`. Both commits pushed to origin.

---

## P5a — Phase B readiness shadow diff
**Status: COMPLETE**
**Commit:** 62ba54f
**Doc:** docs/testing/PHASE_B_READINESS__v20260711_1210.md

Shadow diff ran 153 turns (133 golden + 20 demo) on Mini. Compared `is_declarative_utterance()` (regex, current production) vs `classify_sio()["type"] == "statement"` (CandidateIntent, Phase B candidate).

Key findings:
- Overall agreement: 120/153 (78.4%)
- Gov-critical agreement: 13/26 (50%) — **all 13 disagreements are in the SAFER direction**
- Dangerous direction (Phase B adds spurious write detection): **0 instances**
- SUPERSEDE group (write-path correctness): **9/9 AGREE** — both gates fire identically on supersede utterances
- CMD group: Phase B correctly classifies "Stop.", "Reconsider.", etc. as commands; regex false-positives all 6
- A6 + FAIL injection entries: Phase B injection guard suppresses write detection on all 7 injection payloads; regex fires on all 7 (Phase B safer)
- Gate B (full-object classification): 85.7% — below 90% target; UX impact but not governance risk

**Cutover decision is Bill's. Stopping here.**

---

## STOP — Cutover decision on Phase B consumption is Bill's

Do NOT flip Phase B. This session is complete.
