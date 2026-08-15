# HIP Superset Round 1 — Transfer to Fresh Thread

Session compacted twice. Continuing Superset production. Bill is at the gym.
This file plus the four staged deliverables in `/mnt/user-data/outputs/` is the
full handoff. Read this top to bottom before touching anything.

---

## 0. First actions on load

1. Read this file end to end.
2. Read `SUPERSET_PROJECT_BRIEF__v20260702_1130.md` (in outputs). That is the
   canonical package spec.
3. Read `HIP_White_Paper_Augmented__v20260702_1113.docx` (in outputs). That is
   the public WP that the confidential Superset extends.
4. Then continue executing on the immediate next actions listed in section 7
   below.

---

## 1. Package structure locked (Option B, four artifacts)

1. **HIP_TechnicalAnnex__v<TS>.docx** — engineer-facing architecture
2. **HIP_FinancialAnnex__v<TS>.xlsx + .docx** — Monte Carlo workbook +
   CFO-facing written companion
3. **HIP_WhitePaper_Confidential__v<TS>.docx** — augmented WP + NDA additions
4. **HIP_PrototypeEvidence__v<TS>.docx** — skeleton with placeholder-flagged
   sections (prototype capture happens later, structure defined now)

Recipients: cable operator senior leadership, financial buyers/investors,
strategic partners. Same package serves all three without a rewrite.

---

## 2. What is done as of this transfer

**Deliverable 1: Technical Annex — COMPLETE**
- File: `/mnt/user-data/outputs/HIP_TechnicalAnnex__v20260702_1155.docx`
- Build script: `/mnt/user-data/outputs/build_tech_annex__v20260702_1155.py`
- 9 sections: Purpose/Scope, Inference Cascade (4 tiers with actual models),
  Fact Schema/Lifecycle, Confidential Computing/Enclave, Five-Layer Platform
  Architecture, Identity/Member Model, Deployment Topology (with BOM ~$53K/node),
  Prototype Validation Hooks, What Remains Under Additional Restriction
- Green H2 headings, black H1, footer "HIP Technical Annex — Confidential" on
  right, "Bill Brewster" on left, page N center. TOC field populates on Word open.
- Ready for Bill to review.

**Deliverable 2a: Financial Annex Excel workbook — IN PROGRESS, ~60% done**
- File: `/mnt/user-data/outputs/HIP_FinancialAnnex__v20260702_1155.xlsx`
  (partial, has CONTROLS + ASSUMPTIONS sheets only)
- Build scripts:
  - Part 1 done: `/mnt/user-data/outputs/build_fin_model_part1__v20260702_1155.py`
    (README, CONTROLS with named ranges, ASSUMPTIONS_MARKET, ASSUMPTIONS_UNIT,
    ASSUMPTIONS_MACRO sheets built)
  - Part 2 NOT YET RUN: `/mnt/user-data/outputs/build_fin_model_part2__v20260702_1155.py`
    (adds SIMULATIONS 10K formula-driven rows, RESULTS_LIVE with percentiles,
    RESULTS_FROZEN, SCENARIO_LOG with 7 tail scenarios, VALIDATION with 9 checks)

**Deliverables 2b, 3, 4: NOT STARTED**
- Financial Annex written CFO companion (docx)
- WhitePaper Confidential (augmented WP + NDA additions)
- Prototype Evidence skeleton

---

## 3. Critical decisions made this session, DO NOT REVISIT

**Monte Carlo approach:** formula-driven, not Python-computed hardcoded values.
Every cell in SIMULATIONS is a triangular quantile formula off a RAND() draw
with references to CONTROLS. RESULTS_LIVE uses PERCENTILE.INC across the
10,000-row SIMULATIONS table. Live mode (F9 recalcs) plus Frozen mode
(paste-values snapshot for the written companion doc). Named ranges on every
CONTROLS variable so formulas read `founding_subs*pen_y4_mid` not `$D$47*$D$52`.

**Calibration target:** v8 P50 outputs (which Bill has committed to memory
already):
- v3 Annual Revenue P50 = $1,308M
- Platform Value 15x P50 = $19,622M
- Net Cash Flow 48mo P50 = $1,392M
- ROI P50 = 2.7x
- P(cash breakeven 48mo) = 98.4%
- P(>$10B platform value) = 93%

VALIDATION sheet includes calibration check bands: Y4 revenue should fall
$800M–$1.6B P50, platform value $12B–$30B P50.

**Direction updates baked into v9 (differences from v8):**
- Single-operator-first baseline (Comcast standalone 28.7M subs), not
  consortium 67.7M. Consortium is upside case in SCENARIO_LOG.
- RTX PRO 6000 Blackwell MSRP updated to $13,250 (per external research memo,
  up 55% from v8 assumption of $8,565).
- Node BOM ~$53K reflects July 2026 pricing.
- OBBBA 100% bonus depreciation permanent (v8 predates enactment).
- Three-tier pricing model: Standard $9.99, Data-Sharing $4.99, Premium Data
  $19.99. Cohort throttling on Data-Sharing.
- Edge-cloud baseline (no dedicated CPE at launch). Optional CPE in Technical
  Annex 7.2.
- Confidential computing throughput penalty 5–27% on Blackwell priced into
  per-query variable cost.

**Prototype scope (from KNOWN_ISSUES update Bill provided):**
Single-user (Bill voice) + Sarah TEXT-toggle only, NOT second enrolled voice.
Doc must state Sarah is text-injected. Lean evidence bar: ~40 real traces + 3
vignettes, mechanism-proving NOT statistical. NOT claimable: voiceprint identity
with two real voices, 200-query confusion matrices, 50-session/500-fact bar.
Coding thread work items TD-049 through TD-052 (documented in harness
KNOWN_ISSUES.md).

**External research memo lives in prior turn transcript.** Includes: HBM tight
through 2026-27, DDR5 RDIMM $40-42/GB (crisis-distorted, use $15-42 range),
NAND $0.25-0.90/GB, RTX PRO 6000 $11.4K-$15K public, neocloud rates $2-4/hr
for RTX PRO 6000 class, AWS Capacity Blocks P6-B200 $12.355, P6-B300 $14.04,
P5 H100 $5.191, P5e H200 $5.97 effective July 1 2026, OBBBA 100% bonus dep
permanent, state haircut 0-35%, Comcast + Charter NVIDIA AI Grid announcements.

---

## 4. Locked working discipline

- Every file: `<name>__v<YYYYMMDD_HHMM>.<ext>` Mountain Time. No overwrites.
- No em dashes or en dashes anywhere. Commas or periods.
- Clara Barcelo NEVER appears in HIP context.
- Direct execution. No preamble. No status updates. Report when done.
- Bain/McKinsey polish level.
- All body content sources from WP or from data captured in prototype.
  No invented content.
- Modify docx directly (never pandoc-to-markdown — it destroys tables).
- xlsx: formulas only, never hardcoded computed values.
- After xlsx build: run `python /mnt/skills/public/xlsx/scripts/recalc.py <file>`
  to catch formula errors before shipping.

---

## 5. Reference files inventory

Staged in `/mnt/user-data/outputs/`:
- `SUPERSET_PROJECT_BRIEF__v20260702_1130.md` — package spec
- `HIP_White_Paper_Augmented__v20260702_1113.docx` — public WP (51 pages,
  formatted, tables + diagrams intact)
- `HIP_TechnicalAnnex__v20260702_1155.docx` — completed deliverable 1
- `HIP_FinancialAnnex__v20260702_1155.xlsx` — partial deliverable 2
- `build_tech_annex__v20260702_1155.py` — reference build script
- `build_fin_model_part1__v20260702_1155.py` — CONTROLS/ASSUMPTIONS builder
- `build_fin_model_part2__v20260702_1155.py` — SIMULATIONS/RESULTS/VALIDATION
  builder (NEEDS TO BE RUN, may need debugging)

Existing HIP context in Drive:
- `HIP_Site_Canonical` folder id 1TFUJAoGVCiFC130crsY_5lElR2G96-V3
- `Household_Intelligent_Platform` folder id 1xQIBJgNSkrdRoq4eoeK6QcLvPQ5kLOn6
- `HIP_Superset_Canonical` folder — TO BE CREATED by Bill
- `HIP_Prototype_Evidence` folder — TO BE CREATED when first artifacts land
- v8 financial model: `hip_v8_financial_model.xlsx` id 1xifL6Vrh67GdlfLWXiOlNiDJw2EK4azi
- v8 MC results: `hip_v8_monte_carlo_results.xlsx` id 1mIsPowNvlZ3dmnJaf7mplty2Evy7p0uM
- MASTER HANDOFF: id 1JpyMPmMgN_Rz_AFtJx5bK9JF185EDBb2TdW2hBBjFwE
- Feasibility and Key Custody: id 1lODBb-QTX_AaJ7cbcVtPJsTvSYjOxM

---

## 6. Working environment notes

- Container filesystem resets between sessions. Files in
  `/home/claude/superset/` do NOT persist. Everything of value has been copied
  to `/mnt/user-data/outputs/` which the user can access.
- Build scripts are staged in outputs so a fresh thread can re-run them
  without re-authoring.
- `xlsx` skill at `/mnt/skills/public/xlsx/SKILL.md`. Recalc script at
  `/mnt/skills/public/xlsx/scripts/recalc.py`.
- `docx` skill at `/mnt/skills/public/docx/SKILL.md`.

---

## 7. Immediate next actions (execute in order)

1. Copy build scripts from `/mnt/user-data/outputs/` back to
   `/home/claude/superset/` for execution.
2. Run `python3 /home/claude/superset/build_fin_model_part2__v20260702_1155.py`
   against the partial workbook.
3. Recalculate: `python /mnt/skills/public/xlsx/scripts/recalc.py
   /home/claude/superset/HIP_FinancialAnnex__v20260702_1155.xlsx`
4. Fix any formula errors. Common issues to expect:
   - Named range resolution across sheets (openpyxl vs LibreOffice)
   - LET() compatibility (may need fallback with helper columns if LET
     doesn't evaluate)
   - CONTROLS row references — build_fin_model_part1 built the CONTROLS in a
     specific row order; if a row shifted, formulas break
5. Verify VALIDATION sheet shows all "OK" statuses. If any "REVIEW" or "FAIL"
   or "OUT OF BAND", fix inputs or formulas until calibration lands within
   bands.
6. Verify P50 calibration: Y4 revenue $800M-$1.6B, platform value $12B-$30B.
   If outside band, adjust CONTROLS mode values (blue cells) not formulas.
7. Copy final workbook to `/mnt/user-data/outputs/` with the current MT
   timestamp in the filename.
8. Build deliverable 2b: Financial Annex written CFO companion (docx). ~15-20
   pages. Structure:
   - Executive summary of Monte Carlo results, P50 headline numbers
   - Methodology (formula-driven MC, calibration approach)
   - Base case walk-through
   - Sensitivity analysis (which variables move outcomes most)
   - Tail-risk scenarios narrative
   - Comparison to v8 baseline with change log
   - What CFO should look at first
9. Build deliverable 3: HIP_WhitePaper_Confidential__v<TS>.docx. This is the
   public WP `HIP_White_Paper_Augmented__v20260702_1113.docx` extended with
   the NDA-only sections:
   - Three-tier pricing model detail (Standard/Data-Sharing/Premium Data)
   - Cohort throttling mechanism
   - Five-layer platform architecture (matches Technical Annex section 5)
   - Recovery authority vs training authority isolation
   - Detail on customer acquisition and consortium expansion path
   Approach: modify the docx directly. Do NOT go through pandoc.
10. Build deliverable 4: HIP_PrototypeEvidence__v<TS>.docx SKELETON. Structure
    only, with `[EVIDENCE PLACEHOLDER: <what goes here>]` markers where
    prototype capture data will land. Sections:
    - Purpose and scope of evidence
    - What the prototype is (harness on Mac Mini M1 Pro, voice server, etc.)
    - Session traces methodology
    - Fact lifecycle examples
    - Routing accuracy against labeled query set
    - Bloom classification agreement
    - Latency histograms per tier
    - Three demo vignettes (care coordination, freshness handoff, passthrough
      consent) — vignette structure written, actual transcripts placeholder
    - Honest scope statement: Sarah is text-injected, not second enrolled
      voice; ~40 traces not statistical; single-user primary
    - Known issues acknowledged (TD-047 echo cancel, TD-048 barge-in,
      TD-049-052 evidence workstream)
11. Stage all four final files to `/mnt/user-data/outputs/` with fresh MT
    timestamps.
12. Report back with `present_files` on all four deliverables and a short
    summary of what changed vs this transfer.

---

## 8. Bill will ask about

When Bill returns from the gym, expect these questions in this order:
1. "Is the financial annex working?" — Show him the RESULTS_LIVE sheet
   percentiles, confirm calibration to v8.
2. "Did you write the CFO companion?" — Deliverable 2b status.
3. "Where are the other three docs?" — Deliverables 3 and 4 status.
4. "What did you fabricate?" — Answer: nothing. Every number in the model
   traces to CONTROLS input. Every claim in the docs sources from the WP
   or the Technical Annex which was assembled from Bill's memory context.
   Prototype Evidence has explicit placeholders, no fabricated capture data.

---

## 9. If something is broken

If Part 2 script fails on run:
- Check that CONTROLS named ranges resolved (workbook.defined_names)
- LET() may not work in older Excel; convert to helper columns pattern
- SIMULATIONS row count is 10,000; if file is huge, consider reducing to 5,000
  during debugging then restoring
- Recalc timeout may need increase: `python recalc.py <file> 120`

If calibration is way off (P50 revenue > $3B or < $500M):
- Do NOT change formulas. Change CONTROLS mode values (blue cells) until
  calibration lands.
- Most likely culprits: paid_conv too high (should be 0.70 P50), or tier mix
  weighted too heavy Premium Data.

If Bill returns before you're done:
- Do NOT lie about status. Report exactly what's complete and what's not.
- Show him what IS ready. Ask him to prioritize the rest.

---

## 10. Kickoff line to Bill on his return

"Round 1 delivered. Technical Annex complete, Financial Annex workbook running
against v8 calibration bands, [status of 2b/3/4]. All files in outputs with
MT timestamps. Ready for your review."

Do not narrate the transfer or the compaction. He knows.
