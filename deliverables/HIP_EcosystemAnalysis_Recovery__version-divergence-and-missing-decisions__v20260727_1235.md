# HIP Ecosystem Analysis Recovery -- Version Divergence and Missing Decisions

Status: RECOVERY RECORD (not a correction to the document itself; no prose in
HIP_EcosystemAnalysis_NDA is changed by this filing)
Date: 2026-07-27 12:35 MT
Branch: roadmap

## THE FINDING

The Tier-1 diligence package index (`HIP_NDA_Package__tier1-diligence__v20260714_1400.md`)
and `docs/deliverables/MANIFEST.md` mark `HIP_EcosystemAnalysis_NDA__v20260712_1602.docx`
CURRENT and HANDABLE, and that file was never produced: no file of that name exists on
disk, in this machine's git history on any branch of hip-roadmap or hip-dev, or on Google
Drive under the account that would have produced it. The newest file that actually exists,
`HIP_EcosystemAnalysis_NDA__v20260707_0814.docx`, sits in `business/ecosystem/` as an
unregistered orphan -- it is not named in MANIFEST Section B at all. The version MANIFEST's
own tracked chain treats as its last real link, `HIP_EcosystemAnalysis_NDA__v20260707_0618.docx`
(marked SUPERSEDED, since it was superseded by the never-produced 07-12 version), is missing
the eldercare-BAA/PHI resolution and the operator-blind, consent-ledger, and biometric
resolution language entirely -- and that language is exactly what a governance-boundary
consistency check against the rest of the NDA package (Debt Register TD-108/TD-109, the
Confidential WP's operator-custody claims) depends on to hold together.

This document is a recovery record: it reconstructs what changed, when, and in which
surviving file, so the corrections are not lost a second time. It does not edit
`HIP_EcosystemAnalysis_NDA` itself and does not decide anything on Bill's behalf --
see OPEN ITEM FOR BILL at the bottom.

---

## 1. The four surviving versions, and the one that isn't

| Version | Path | Paragraphs | Git commit | Status per MANIFEST |
|---|---|---|---|---|
| v20260706_2123 | `business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260706_2123.docx` | 227 | `a71c9d2` | not registered |
| v20260707_0618 | `whitepaper/nda/HIP_EcosystemAnalysis_NDA__v20260707_0618.docx` (originally committed to `whitepaper/superset/`) | 243 | `df393d5` | **SUPERSEDED** (last version MANIFEST actually tracks) |
| v20260707_0651 | `business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0651.docx` | 247 | `8ca0704` | not registered (orphan) |
| v20260707_0814 | `business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0814.docx` | 253 | `90a5a7d` | not registered (orphan) -- **newest file that exists** |
| v20260712_1602 | -- | -- | **none, at any hash, on any branch** | CURRENT / HANDABLE (per HIP_NDA_Package and MANIFEST) |

Chronology, same day (2026-07-07), all four surviving commits by Bill Brewster:
`a71c9d2` (06:12:50) -> `df393d5` (06:36:22) -> `8ca0704` (08:12:55) -> `90a5a7d` (09:20:16).
`v20260707_0618` is the SECOND version chronologically, not the last -- it was filed 24
minutes after `v20260706_2123` and roughly 1h36m *before* the propagation work order
(`8ca0704`) that introduced the corrections this document is about. MANIFEST's "current"
pointer is pointing at a version that predates the corrections by more than an hour and a
half, not a version that simply lacks later, unrelated updates.

---

## 2. Full commit histories, quoted verbatim

### `git log --all --diff-filter=A -- '*EcosystemAnalysis*'`

Checked against every git repository on this machine: `hip-roadmap` and `hip-dev` (same
remote, identical results), `hip-harness` (zero matches -- unrelated repo), `hip-vo` (not a
git repository on this machine). Only these four commits, ever, on any branch:

```
COMMIT a71c9d23da9ff5a980b3c5914cae54dc26fcba34
Date: 2026-07-07 06:12:50 -0600
Author: Bill Brewster

feat(business): add business case section with financial model and ecosystem analysis

financial/: 3 Python build scripts + current xlsx (v20260705_2020, 550K formulas, 3-scale MC)
ecosystem/: engine.py + build_nda.js + firms.json + category_mesh.json + current NDA docx (19pp)
business/INDEX.md: full manifest with model state, sort distribution, derivation rules
CLAUDE.md: lock business/ section alongside docs/

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>

business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260706_2123.docx
```

```
COMMIT df393d58c67fd23a0415e2bf92ee08cd66079c98
Date: 2026-07-07 06:36:22 -0600
Author: Bill Brewster

docs(whitepaper/superset): add ecosystem analysis NDA v20260707_0618

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>

whitepaper/superset/HIP_EcosystemAnalysis_NDA__v20260707_0618.docx
```

```
COMMIT 8ca0704d375863c08b36280c563aead7b7c36239
Date: 2026-07-07 08:12:55 -0600
Author: Bill Brewster

feat(propagation): apply CHG-1 through CHG-6 from HIP PropagationWorkOrder

File A: build_nda.js - CHG-1 (consent ledger as blast-radius cap), CHG-2 (operator-blind
claim), CHG-3 (on-device voiceprint, decision-gated), CHG-4 (eldercare PHI/BAA, provisional
pending DECISION-1). Path fixes applied (remove /home/claude hardcodes), MT_TS added.
Rebuilt output: HIP_EcosystemAnalysis_NDA__v20260707_0651.docx (+707 bytes over baseline).

File D: build_fin_chg5_risk_opex.py - CHG-5 scoped append to HIP_FinancialAnnex.
Appends COMPLIANCE & PHI RISK section to CONTROLS (risk_compliance_phi_opex_m,
TRIANGULAR $2M-$6M mode $4M, named range registered at D53). Appends PHI compliance
tail risk row to SCENARIO_LOG (row 13, formula-driven off base case). Produced
HIP_FinancialAnnex__v20260707_0708.xlsx. Diff: only rows 52-53 in CONTROLS and row 13
in SCENARIO_LOG added; all prior rows, MC formulas, and named ranges intact.

File E: DEBT_REGISTER__v20260707_0710.md - CHG-6 adds TD-108 (per-fact consent-and-
routing ledger) tagged as primary liability-severity reducer, ship pre-scale.
LATEST_DEBT.md symlink repointed. docs/INDEX.md updated.

Files B/C (public WP + NDA WP) blocked: no assembler script exists for whitepaper/sections/
docx files; cannot follow edit-rebuild-verify without one.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0651.docx
```

```
COMMIT 90a5a7d236fb0fb4682281dd7cf00210af5ab0f5
Date: 2026-07-07 09:20:16 -0600
Author: Bill Brewster

feat(finalization): resolve DECISION-1/2/3, add CHG-8 (HIP_FinalizationOrder)

File A: build_nda.js - finalize CHG-1/2/3/4:
  CHG-2: replace provisional operator-blind para with three resolved verbatim blocks
    (primary claim, operator-learns-something qualifier, metadata sensitivity statement)
    + prohibited-claims guardrail comment.
  CHG-3: replace decision-gated biometric para with resolved 2.3 wording
    ("does not create or store centralized biometric templates"; no consent claims).
  CHG-4: replace provisional PHI safe-default with five-paragraph BA-bounded
    workspace description (DECISION-1: reimbursed eldercare vertical as HIPAA workspace
    under BAA; HIP Core non-HIPAA; Layer 2 $450M/$1.8B figures unchanged).
  All four PROVISIONAL tags flipped to FINAL.
  Rebuilt: HIP_EcosystemAnalysis_NDA__v20260707_0814.docx (30706 bytes).

File D: build_fin_chg5_risk_opex.py - update framing note for DECISION-1 resolution
  (BA-bounded workspace architecture; Layer 2 figures confirmed unchanged).
  Produced HIP_FinancialAnnex__v20260707_0815.xlsx. Diff vs _0708: one cell changed
  (CONTROLS!H53 annotation text only; no formula or named range movement).

File E: DEBT_REGISTER__v20260707_0816.md - add TD-109 (CHG-8 build requirement):
  biometric consent-and-retention control for on-device speaker recognition.
  Full scope: default-off, enrollment consent, consent screen, retention schedule,
  non-biometric fallback, audit events. Gates public consent claims. TD-108 tag
  flipped to FINAL. LATEST_DEBT.md repointed. docs/INDEX.md updated.

CHG-7 not found in build_nda.js - flagged; no content defined for it in either work order.

Files B/C (whitepapers) remain deferred pending assembler unblock.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0814.docx
```

**The referenced work orders, `HIP_PropagationWorkOrder` and `HIP_FinalizationOrder`, do not
exist anywhere in this repository.** Confirmed by filename search (`find . -iname
"*PropagationWorkOrder*" -o -iname "*FinalizationOrder*"`, zero hits) and by content search
(`DECISION-1` appears in exactly one file, `business/ecosystem/build_nda.js`, as inline code
comments, not as a standalone decision record). Whatever instructed CHG-1 through CHG-8 and
DECISION-1/2/3 was never filed as its own document -- only the code comments in
`build_nda.js` survive as a pointer to it:

```
line 122: // FINAL CHG-4 DECISION-1 resolved see HIP_FinalizationOrder
line 194: // FINAL CHG-2 DECISION-2 resolved see HIP_FinalizationOrder
line 200: // FINAL CHG-1 see HIP_FinalizationOrder
line 202: // FINAL CHG-3 DECISION-3 resolved see HIP_FinalizationOrder
```

CHG-1 (consent ledger) carries no DECISION tag -- it shipped as FINAL text from the moment
it was first introduced (`8ca0704`), never gated behind a provisional/decision state the way
CHG-2/3/4 were.

### Google Drive search

`title contains 'EcosystemAnalysis'`: zero results. `fullText contains
'HIP_EcosystemAnalysis_NDA'`: zero results. Not one version of this document -- not the
missing 07-12 version, not even the versions confirmed to exist in this repo's own git
history -- was found on Google Drive under the currently authenticated account. Whatever
produced `v20260712_1602` did not save a copy to this account's Drive, or the account that
produced it is a different one than the one authenticated here.

---

## 3. Both inserted blocks, quoted in full

Both blocks are quoted from `v20260707_0814` (`business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0814.docx`),
the fullest surviving version. Section 2.3 in that file runs paragraphs 27-41; Section 4.3
runs paragraphs 71-77. Paragraph indices below are 0814's own.

### Block 1 -- eldercare BAA/PHI resolution (Section 2.3, paragraphs 34-38)

Introduced provisional at `8ca0704` (07-07 08:12), resolved final at `90a5a7d` (07-07 09:20),
per CHG-4 / DECISION-1.

**Provisional form (v20260707_0651, paragraph 34, one paragraph, superseded by the block below):**

> HIP orchestrates eldercare coordination over consent and references; where HIP handles
> protected health information it does so as a Business Associate under a BAA, with a
> separate PHI data model and minimum-necessary routing. The PHI architecture determines
> which data flows are direct and which are pointer-based; the eldercare coordination layer
> functions under either model, with BAA scope sized to the chosen architecture.

**Final resolved form (v20260707_0814, paragraphs 34-38, five paragraphs):**

> A provider contracts with HIP under a BAA and creates a HIP eldercare workspace for a
> patient and caregiver unit.
>
> PHI-bearing content (care plans, GUIDE coordination tasks, caregiver notes, medication
> reminders, appointment context, escalation events, provider-authored summaries) lives only
> inside the HIPAA eldercare workspace.
>
> The workspace runs in HIP confidential-computing enclaves with PHI-specific access control,
> audit logs, minimum-necessary rules, breach-response procedures, and no off-net or frontier
> routing unless explicitly authorized under the provider's policy and patient and caregiver
> consent.
>
> HIP Core stores non-PHI household facts separately. Any fact derived from provider care
> coordination is tagged PHI=true, source=covered_provider, tenant=provider,
> allowed_destinations=HIPAA_workspace_only.
>
> Consumer household memory may hold references (care_task_id, provider_workspace_id, consent
> state) but not clinical content unless inside the HIPAA workspace.

`v20260707_0618` -- the version MANIFEST's own chain treats as current -- has neither the
provisional nor the final form. Its Section 2.3 goes directly from the Layer 2 sizing
assumptions to "The reimbursed path, where the ceiling comes off," with zero PHI/BAA content
of any kind.

### Block 2 -- operator-blind, consent-ledger, and biometric resolution (Section 4.3, paragraphs 73-77)

Introduced provisional/final-mixed at `8ca0704`, expanded and finalized at `90a5a7d`, per
CHG-1 (consent ledger, shipped final immediately), CHG-2 (operator-blind, DECISION-2), CHG-3
(biometric, DECISION-3).

**Provisional/CHG-1-final form (v20260707_0651, paragraphs 69-71, three paragraphs):**

> The operator cannot read household plaintext content. Metadata, routing decisions, and
> consent records are governed separately and are not exposed as household content. The
> scope of operator visibility is the service relationship, billing, quality of service, and
> aggregate usage, not the substance of household conversations, facts, or cross-app data
> flows.
>
> The mechanism that caps breach severity is the per-fact consent-and-routing ledger. Every
> fact in the household graph carries: sensitivity classification, owner identity, source
> provenance, consent scope, allowed destinations, retention limit, and an immutable audit
> trail. The router cannot deliver a fact outside its consent scope without a logged
> exception the household can review. This control bounds the blast radius of any single
> failure, and it ships before the platform scales, not as a later hardening step. This is
> what separates a governed household substrate from a cloud storage layer with a permission
> flag.
>
> HIP creates no centralized biometric voiceprint or face recognition templates. Speaker
> identification uses on-device embeddings stored locally on the household edge node under
> the same enclave custody as other household data, not in a shared biometric database.

**Final resolved form (v20260707_0814, paragraphs 73-77, five paragraphs -- the consent-ledger
paragraph is byte-for-byte identical to the provisional form above; the operator-blind and
biometric paragraphs are rewritten and expanded):**

> HIP is operator-blind for household plaintext content. When HIP is operating as designed,
> household content is decrypted only inside attested confidential-computing enclaves, and
> the broadband operator does not receive the household encryption key or access to
> household plaintext.
>
> Operator-blind does not mean the operator learns nothing. Network operations, billing,
> abuse prevention, reliability monitoring, enclave attestation, routing tier selection,
> traffic timing, volume, consent and audit metadata, and legally required disclosures are
> governed separately and minimized, but they are not the same as household plaintext
> content.
>
> HIP treats metadata, routing decisions, consent records, and audit logs as sensitive
> operational privacy data. They are minimized, access-controlled, logged, and governed
> separately from household content, but they may still reveal operational or contextual
> facts.
>
> The mechanism that caps breach severity is the per-fact consent-and-routing ledger. Every
> fact in the household graph carries: sensitivity classification, owner identity, source
> provenance, consent scope, allowed destinations, retention limit, and an immutable audit
> trail. The router cannot deliver a fact outside its consent scope without a logged
> exception the household can review. This control bounds the blast radius of any single
> failure, and it ships before the platform scales, not as a later hardening step. This is
> what separates a governed household substrate from a cloud storage layer with a permission
> flag.
>
> HIP does not create or store centralized biometric templates. If speaker recognition is
> enabled, HIP creates local, encrypted speaker embeddings on the household device solely for
> speaker identification and permissioning. These embeddings may be treated as biometric
> information under biometric privacy laws.

`v20260707_0618` has none of this either. Its Section 4.3 ("Consent is the enabler, not just
the shield") is a single paragraph -- the shared introductory sentence that both later
versions keep unchanged -- and goes directly to "4.4 Categories come alive, not just firms"
with no operator-blind statement, no consent-ledger mechanism, and no biometric statement of
any kind.

### Structural confirmation

Paragraph-count arithmetic across the two affected sections confirms these are pure
additions, nothing removed: v20260707_0618 has 243 total paragraphs; v20260707_0814 has 253
(+10). Section 2.3 gained exactly 5 paragraphs (Block 1); section 4.3 gained exactly 5
paragraphs (Block 2, net of the unchanged intro sentence). No other section's paragraph
count differs between these two versions. `v20260707_0814` is a strict superset of
`v20260707_0618`'s content in every section checked.

---

## 4. What even the newest surviving file does not resolve

`HIP_NDA_Package__tier1-diligence__v20260714_1400.md`'s own consistency-check language for
the (never-produced) `v20260712_1602` describes governance-boundary content under a numbered
"Section 11": *"Injection contract (INJ-1 through INJ-7): PASS (Section 11 governance
boundary)"* and *"OP-1..5 expansion roadmap: PASS (Section 11 v2+ scope)."* Neither INJ-1
through INJ-7 nor OP-1 through OP-5 appears anywhere in `v20260707_0814` -- its own Section
11 ("On the State of This Analysis") is a two-paragraph currency disclaimer, unchanged word
for word between `v20260707_0618` and `v20260707_0814`. Whatever added INJ-1..7/OP-1..5
content to a "Section 11" happened only in the lost `v20260712_1602`, sometime after
`v20260707_0814`, and is not recoverable from anything on this machine. This is a second,
separate gap from Blocks 1 and 2 above -- naming it here so a later reader does not assume
`v20260707_0814` is a complete substitute for the missing version.

---

## 5. Reconstruction checklist

Unlike the Confidential White Paper (where the true final version had to be rebuilt
paragraph-by-paragraph from recovered fragments), the Ecosystem Analysis's actual final
prose for Blocks 1 and 2 already exists, verbatim, in a real file already committed to git:
`business/ecosystem/HIP_EcosystemAnalysis_NDA__v20260707_0814.docx` at commit `90a5a7d`.
Nothing needs to be rebuilt from fragments here. What is needed is registration and a
decision on the remaining gap:

1. Confirm `v20260707_0814` (not `v20260707_0618`) is the version any diligence package
   should reference going forward, since it is the only surviving file carrying Blocks 1
   and 2.
2. Register `HIP_EcosystemAnalysis_NDA__v20260707_0814.docx` in MANIFEST Section B as CURRENT
   (or as Bill directs); mark `v20260707_0618` SUPERSEDED BY it explicitly, rather than
   leaving `v20260707_0618` as the last entry in the chain with a phantom `v20260712_1602`
   above it that was never real.
3. Mark `HIP_EcosystemAnalysis_NDA__v20260712_1602.docx` NEVER PRODUCED in MANIFEST, matching
   the same treatment given to `HIP_WhitePaper_Confidential__v20260712_1852.docx` in the
   parallel white-paper rebuild.
4. Re-run the Tier-1 package's own consistency checks (63.7%/84.2M dyad figure absence,
   SIA Gate A/B currency, voice governance currency) against `v20260707_0814` specifically --
   they were last checked against the now-confirmed-nonexistent `v20260712_1602`, not against
   any file that actually exists.
5. Decide whether the Section-11 INJ-1..7/OP-1..5 content the lost version apparently
   carried (per section 4 above) needs to be written fresh into `v20260707_0814` before it
   is treated as the diligence-ready version, or whether that gap is accepted and named
   in the package index instead, the way the Confidential WP's speaker-verifier NDA-only
   paragraph is being left as a marked placeholder rather than invented.
6. Do NOT treat this recovery record as authorization to edit `HIP_EcosystemAnalysis_NDA`
   prose -- see the open item below and the WP parallel: flag, do not rewrite, until Bill
   decides.

---

## OPEN ITEM FOR BILL -- not a decision made here

The operator-blind paragraph in Block 2 states: *"HIP is operator-blind for household
plaintext content. When HIP is operating as designed, household content is decrypted only
inside attested confidential-computing enclaves, and the broadband operator does not receive
the household encryption key or access to household plaintext."*

Confidential-computing enclaves are not built and were scoped out of the current roadmap
(per the plan of record and REQ_CRYPTO_P3_OPERATOR_BLIND's own honest-limit language: at-rest
operator-blindness is built and proven -- master key destroyed, PS1/PS2/OB4 all hold -- but
at-inference protection needs confidential computing, which does not exist today). As
written, Block 2's paragraph states the enclave-gated decryption as the operating mechanism
without distinguishing it from what is actually proven. This paragraph needs the same
at-rest-versus-at-inference scoping being applied to the Confidential White Paper in the
parallel rebuild (`HIP_WhitePaper_Confidential__v20260727_1104.docx`), not a different
resolution invented independently for this document.

Flagging this for Bill's decision. Not rewritten here.
