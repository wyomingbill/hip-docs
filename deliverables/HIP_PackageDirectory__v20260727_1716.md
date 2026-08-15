# HIP Package Directory

Status: AUDIT RECORD (read-only inventory; no prose changed in any surveyed
document; nothing rebuilt, nothing rendered here beyond the existing
docs/rendered/ baseline)
Reconciled-Against: roadmap 9aa45e1; docs/deliverables/MANIFEST.md and
docs/INDEX.md as of 2026-07-27; docs/rendered/ baseline at 556848a; git
history across every local branch (`git log --all`) for existence checks,
since docx binaries are gitignored by design and "not on disk" alone can't
distinguish "never tracked" from "tracked once, since removed"
Date: 2026-07-27 17:16 MT

Every `.docx` row below was read from its `docs/rendered/` text rendering,
not parsed directly, per instruction.

## How to read this

One row per document in the Tier-1 NDA diligence package and its
supporting set (source: `docs/deliverables/HIP_NDA_Package__tier1-diligence__v20260714_1400.md`,
itself 13 days old and NOT treated as ground truth for status below --
only for which documents belong and their intended reading order).
STATUS is reconciled fresh against `MANIFEST.md`, `docs/INDEX.md`, and
actual on-disk/git-history reality as of this session, not copied from any
older doc. Columns:

- **#** -- item number, this directory's own reading order (groups each
  core document with its version history immediately after it, then
  package-governance docs, then the ten gated site pages last)
- **Title**
- **Path** -- current on-disk path, or "--" if not on disk
- **Version**
- **Status** -- CURRENT, SUPERSEDED, STALE, NEVER PRODUCED, or MISSING per
  the brief's vocabulary; two rows below need a sixth word
  (**UNREGISTERED**) because they are real, on-disk files that fit none of
  the five -- called out explicitly, not forced into the wrong bucket
- **Disk** -- physically present right now
- **INDEX** -- named anywhere in `docs/INDEX.md`
- **MANIFEST** -- has its own Section B canonical-file row in
  `docs/deliverables/MANIFEST.md` (a document merely *discussed* in another
  row's prose, e.g. an orphan named inside the Recovery record's text,
  counts as NO here)
- **Rendered** -- has a `docs/rendered/` text rendering (docx only; n/a for
  .md/.xlsx/.html)
- **Last change** -- `git log -1 --date=short` on the file; "--" if never
  tracked

## FINDING, surfaced up front

Beyond the one gap MANIFEST.md already names (`HIP_WhitePaper_Confidential__v20260712_1852.docx`,
flagged 2026-07-27 as claimed CURRENT but never produced), this audit
found the SAME pattern in four more places: three more Confidential-WP
versions in that same superseded chain (rows 3-5), the Ecosystem Analysis
NDA's own claimed-CURRENT file (row 13), and -- the largest one -- the
**entire public White Paper chain from 2026-07-08 onward** (rows 35-39):
none of `v20260712_1852` (claimed CURRENT), `v20260712_1602`,
`v20260711_2311`, `v20260711_1830`, or `v20260708_1604` (all claimed
SUPERSEDED) exist on disk or anywhere in `git log --all` on any local
branch. The real, on-disk, git-tracked public WP stops at `v20260704_1655.docx`
(row 40). Since docx binaries are gitignored by design here, "no git
trace" cannot fully rule out a locally-built-then-deleted file (unlike the
2026-07-27 WP-Confidential finding, this audit did not check Google
Drive) -- so these are reported as MISSING, a narrower claim than NEVER
PRODUCED, and named as an open item for Bill rather than asserted as fact.

---

## The Tier-1 NDA package (core items, HIP_NDA_Package's own reading order) + version history

| # | Title | Path | Version | Status | Disk | INDEX | MANIFEST | Rendered | Last change |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Confidential White Paper / NDA superset -- claimed CURRENT | -- | v20260712_1852 | MISSING (MANIFEST/Package-Index both label CURRENT/HANDABLE; flagged 2026-07-27 as never produced -- no file on disk, in `git log --all`, or on Drive) | NO | yes | yes | n/a | -- |
| 2 | Confidential WP -- prior (chain) | -- | v20260712_1602 | MISSING (MANIFEST labels SUPERSEDED, implying prior existence; not found on disk or in `git log --all` on any branch -- same unverified-existence pattern as row 1, Drive not checked) | NO | no | yes | n/a | -- |
| 3 | Confidential WP -- prior (chain) | -- | v20260711_2311 | MISSING (same as row 2) | NO | no | yes | n/a | -- |
| 4 | Confidential WP -- prior (chain) | -- | v20260711_1830 | MISSING (same as row 2) | NO | no | yes | n/a | -- |
| 5 | Confidential WP -- prior (chain, real) | `whitepaper/nda/HIP_WhitePaper_Confidential__v20260704_2142.docx` | v20260704_2142 | SUPERSEDED (real file -- this is the version the 2026-07-27 reconstruction was built from) | YES | no | yes | YES | 2026-07-07 |
| 6 | **Confidential WP -- RECONSTRUCTED (read this one)** | `whitepaper/nda/HIP_WhitePaper_Confidential__v20260727_1104.docx` | v20260727_1104 | CURRENT -- PENDING BILL REVIEW (built via python-docx from row 5 since the true v20260712_1852 was never produced; not a continuation of the SUPERSEDED chain, a new artifact standing in for the lost one) | YES | yes | yes | YES | untracked (gitignored; filesystem mtime 2026-07-27) |
| 7 | WP Part II trust-boundary draft | `docs/deliverables/WP_PartII_TrustBoundary_DRAFT__v20260711_1800.md` | v20260711_1800 | INTEGRATED (folded into the WP chain; correctly excluded from the Tier-1 package per HIP_NDA_Package's own orphan check) | YES | no | yes | n/a | 2026-07-11 |
| 8 | WP Part II trust-boundary draft (prior) | `docs/deliverables/WP_PartII_TrustBoundary_DRAFT__v20260711_1730.md` | v20260711_1730 | SUPERSEDED | YES | no | yes | n/a | 2026-07-11 |
| 9 | NDA Open Problems / Expansion Roadmap | `docs/deliverables/NDA_OpenProblems__expansion-roadmap__v20260713_1100.md` | v20260713_1100 | CURRENT | YES | yes | yes | n/a | 2026-07-13 |
| 10 | Debt Register NDA Appendix | `docs/deliverables/HIP_DebtRegister_NDA_Appendix__v20260713_1100.md` | v20260713_1100 | CURRENT | YES | yes | yes | n/a | 2026-07-13 |
| 11 | Debt Register NDA Appendix (prior) | `docs/deliverables/HIP_DebtRegister_NDA_Appendix__v20260711_2312.md` | v20260711_2312 | SUPERSEDED | YES | no | yes | n/a | 2026-07-12 |
| 12 | Ecosystem Analysis NDA -- claimed CURRENT | -- | v20260712_1602 | MISSING (MANIFEST/Package-Index label CURRENT; per the 2026-07-27 Recovery record, no file of this name exists on disk, in `git log --all`, or on Drive) | NO | yes | yes | n/a | -- |
| 13 | Ecosystem Analysis NDA (prior, real) | `whitepaper/nda/HIP_EcosystemAnalysis_NDA__v20260707_0618.docx` | v20260707_0618 | SUPERSEDED (real; the Recovery record's own "last real link" in this table's chain, though it is missing content two newer real drafts below carry) | YES | no | yes | YES | 2026-07-07 |
| 14 | **Ecosystem Analysis Recovery record (read this one)** | `docs/deliverables/HIP_EcosystemAnalysis_Recovery__version-divergence-and-missing-decisions__v20260727_1235.md` | v20260727_1235 | CURRENT (the finding doc itself; changes no prose, names the gap) | YES | yes | yes | n/a | 2026-07-27 |
| 15 | Ecosystem Analysis NDA (real, newest, unregistered orphan) | `business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0814.docx` | v20260707_0814 | **UNREGISTERED** (real, newest existing draft; per the Recovery record it lacks the INJ-1..7/OP-1..5 "Section 11" content the lost v20260712_1602 apparently carried) | YES | discussed only, not its own row | discussed only, not its own row | YES | 2026-07-07 |
| 16 | Ecosystem Analysis NDA (real, unregistered) | `business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0651.docx` | v20260707_0651 | **UNREGISTERED** | YES | no | no | YES | 2026-07-07 |
| 17 | Ecosystem Analysis NDA (real, unregistered) | `business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260706_2123.docx` | v20260706_2123 | **UNREGISTERED** | YES | no | no | YES | 2026-07-07 |
| 18 | Financial Annex (xlsx, live model) | `business/financial/HIP_FinancialAnnex__v20260713_2010.xlsx` | v20260713_2010 | CURRENT | YES | yes | yes | n/a | 2026-07-13 |
| 19 | Financial Annex (xlsx, prior v10) | `business/financial/HIP_FinancialAnnex__v20260713_1707.xlsx` | v20260713_1707 | SUPERSEDED | YES | no | yes | n/a | 2026-07-13 |
| 20 | Financial Annex (xlsx, prior) | `business/financial/HIP_FinancialAnnex__v20260705_2020.xlsx` | v20260705_2020 | SUPERSEDED | YES | no | yes | n/a | 2026-07-07 |
| 21 | Financial Annex methodology / parameter defense | `business/financial/HIP_FinMethodology__parameter-defense__v20260713_1708.md` | v20260713_1708 | CURRENT | YES | yes | yes | n/a | 2026-07-13 |
| 22 | Financial Annex review memo | `business/financial/HIP_FinModel_ReviewMemo__v20260713_2017.md` | v20260713_2017 | CURRENT, but **not in MANIFEST.md** (registered in docs/INDEX.md only -- a real registration gap, small, named here) | YES | yes | **no** | n/a | 2026-07-13 |
| 23 | Financial Annex (docx, formatted) | `whitepaper/nda/HIP_FinancialAnnex__v20260702_1913.docx` | v20260702_1913 | STALE (excluded; rebuild from xlsx before a formal distribution needs a formatted narrative version) | YES | yes | yes | YES | 2026-07-07 |
| 24 | Technical Annex (NDA) | `whitepaper/nda/HIP_TechnicalAnnex__v20260702_1155.docx` | v20260702_1155 | STALE -- superseded for Tier-1 purposes by row 26; this docx itself untouched | YES | yes | yes | YES | 2026-07-07 |
| 25 | Prototype Evidence (NDA) | `whitepaper/nda/HIP_PrototypeEvidence__v20260702_1615.docx` | v20260702_1615 | STALE (excluded) | YES | yes | yes | YES | 2026-07-07 |
| 26 | **Architecture for Diligence (closes Gap 1, read in place of row 24)** | `docs/deliverables/HIP_ArchitectureForDiligence__scope-borders-testing-and-target__v20260727_1606.md` | v20260727_1606 | DRAFT -- for Bill's ratification | YES | yes | yes | n/a | 2026-07-27 |
| 27 | Governance Proof -- audited transcript + conformance summary | `docs/deliverables/HIP_GovernanceProof__audited-transcript__v20260714_1345.md` | v20260714_1345 | CURRENT | YES | yes | yes | n/a | 2026-07-14 |
| 28 | Governance Proof (prior) | `docs/deliverables/HIP_GovernanceProof__audited-transcript__v20260714_1330.md` | v20260714_1330 | SUPERSEDED | YES | no | yes | n/a | 2026-07-14 |
| 29 | Market research -- household trust-circle segment sizing (verified) | `docs/research-market/MARKET_RESEARCH__household-trust-circle-segment-sizing-verified__v20260712_1331.md` | v20260712_1331 | CURRENT (research artifact -- Package Index states this class deliberately does not require a MANIFEST row) | YES | yes | no (by design) | n/a | 2026-07-12 |
| 30 | Market research -- household trust-circle segment sizing (external) | `docs/research-market/MARKET_RESEARCH__household-trust-circle-segment-sizing-external__v20260712_1331.md` | v20260712_1331 | CURRENT (same by-design MANIFEST exemption) | YES | yes | no (by design) | n/a | 2026-07-12 |

## Package governance documents

| # | Title | Path | Version | Status | Disk | INDEX | MANIFEST | Rendered | Last change |
|---|---|---|---|---|---|---|---|---|---|
| 31 | Tier-1 NDA Package Index (this directory's structural source) | `docs/deliverables/HIP_NDA_Package__tier1-diligence__v20260714_1400.md` | v20260714_1400 | CURRENT, but 13 days stale on STATUS specifics (see FINDING above) -- structurally still the right reading-order source | YES | yes | yes | n/a | 2026-07-14 |
| 32 | Tier-1 NDA Package Index (prior) | `docs/deliverables/HIP_NDA_Package__tier1-diligence__v20260713_1314.md` | v20260713_1314 | SUPERSEDED | YES | no | yes | n/a | 2026-07-13 |
| 33 | Deliverables Manifest (governs Section B canonical status for every row above) | `docs/deliverables/MANIFEST.md` | -- (running doc) | LIVE | YES | yes | -- | n/a | 2026-07-27 |

## Public White Paper (supporting -- the source the Confidential WP builds from)

| # | Title | Path | Version | Status | Disk | INDEX | MANIFEST | Rendered | Last change |
|---|---|---|---|---|---|---|---|---|---|
| 34 | Public White Paper -- claimed CURRENT | -- | v20260712_1852 | MISSING (see FINDING above -- entire 2026-07-08+ chain phantom) | NO | yes | yes | n/a | -- |
| 35 | Public White Paper -- prior (chain) | -- | v20260712_1602 | MISSING (same pattern) | NO | no | yes | n/a | -- |
| 36 | Public White Paper -- prior (chain) | -- | v20260711_2311 | MISSING | NO | no | yes | n/a | -- |
| 37 | Public White Paper -- prior (chain) | -- | v20260711_1830 | MISSING | NO | no | yes | n/a | -- |
| 38 | Public White Paper -- prior (chain) | -- | v20260708_1604 | MISSING | NO | no | yes | n/a | -- |
| 39 | Public White Paper -- real, newest on disk | `whitepaper/HIP_White_Paper_Updated__v20260704_1655.docx` | v20260704_1655 | **UNREGISTERED** as current (real file; MANIFEST's chain jumps past it straight to the phantom v20260708_1604+ versions) | YES | no | no (this exact filename has no Section B row) | YES | 2026-07-07 |

---

## The ten gated site pages

Per `HIP_Site_Changes_for_WP_NDA__v20260703_1016.md.docx` and
`HIP_WP_Update_Guide__v20260703_2018.md.docx` §19 ("Site-to-document
mapping"): these pages are stated to be the reference the WP/NDA text is
meant to match ("The site is now the reference"). They are external,
gated, and not part of this git repository -- no path, no rendering, no
registration is possible or expected. `index.html` (the public landing
page) is explicitly a separate, ungated page per the update guide §12.1
and is NOT counted among the ten.

| # | Title | Path | Version | Status | Disk | INDEX | MANIFEST | Rendered | Last change | Maps to (NDA doc) |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 | Site page -- overview.html | external, not repo-tracked | -- | CURRENT (external; stated as the reference, not verifiable from this repo) | n/a | no | no | n/a | n/a | WhitePaper Confidential -- Exec Summary, Part I |
| 41 | Site page -- forces.html | external, not repo-tracked | -- | CURRENT (external) | n/a | no | no | n/a | n/a | WhitePaper Confidential -- Part II Forces |
| 42 | Site page -- moat.html | external, not repo-tracked | -- | CURRENT (external) | n/a | no | no | n/a | n/a | WhitePaper Confidential -- Part III Moat |
| 43 | Site page -- architecture.html | external, not repo-tracked | -- | CURRENT (external) | n/a | no | no | n/a | n/a | Technical Annex (-> row 24/26) -- Part III Architecture |
| 44 | Site page -- platform.html | external, not repo-tracked | -- | CURRENT (external) | n/a | no | no | n/a | n/a | WhitePaper Confidential + Technical Annex -- Part VIII |
| 45 | Site page -- substrate.html | external, not repo-tracked | -- | CURRENT (external) | n/a | no | no | n/a | n/a | Technical Annex -- Parts IV-VI |
| 46 | Site page -- economics.html | external, not repo-tracked | -- | CURRENT (external) | n/a | no | no | n/a | n/a | Financial Annex companion -- Part VII-VIII |
| 47 | Site page -- operator-case.html | external, not repo-tracked | -- | CURRENT (external) | n/a | no | no | n/a | n/a | WhitePaper Confidential -- new chapter |
| 48 | Site page -- why-now.html | external, not repo-tracked | -- | CURRENT (external) | n/a | no | no | n/a | n/a | WhitePaper Confidential -- Part IX Why Now |
| 49 | Site page -- deep-dive.html | external, not repo-tracked | -- | CURRENT (external) | n/a | no | no | n/a | n/a | NDA package framing -- cover letter / transmittal |

---

## Summary

- **49 items** tracked across the Tier-1 package, its version history, its
  governance docs, the public WP, and the ten gated site pages.
- **On disk and real:** 30 of 39 non-site-page rows (77%).
- **MISSING (claimed CURRENT or SUPERSEDED, not found on disk or in any
  branch's git history):** 9 rows -- rows 1-4 (Confidential WP chain),
  row 12 (Ecosystem Analysis NDA claimed-current), rows 34-38 (the entire
  post-2026-07-08 public WP chain). None of these nine were checked
  against Google Drive by this audit (only row 1 has had that check done,
  by the 2026-07-27 Recovery finding).
- **UNREGISTERED (real files with no MANIFEST/INDEX row of their own):**
  4 rows -- three business/ecosystem Ecosystem Analysis drafts (15-17) and
  the real newest public WP (39).
- **One MANIFEST registration gap found:** row 22 (Financial Annex review
  memo) is in docs/INDEX.md but has no MANIFEST.md Section B row.
- **Reconciled/current reading path today:** rows 6, 9, 10, 14, 18, 21,
  26, 27 -- the Confidential WP RECONSTRUCTED, NDA Open Problems, Debt
  Register Appendix, Ecosystem Recovery record (which itself points to
  row 15 as the best-available real ecosystem draft), Financial Annex
  xlsx + methodology, Architecture for Diligence, and Governance Proof.
