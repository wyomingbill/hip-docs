HIP Superset Project Brief
Source of truth for the confidential Superset package. Read this before any work on the Superset. Do not skip.
0. Versioned file naming, mandatory
Same rule as the site. Every file: <name>__v<YYYYMMDD_HHMM>.<ext> Mountain Time. No exceptions. No overwrites.
1. Canonical Drive locations
	•	Superset canonical: HIP_Superset_Canonical (TO BE CREATED under Household_Intelligent_Platform/)
	•	Prototype evidence: HIP_Prototype_Evidence (TO BE CREATED under Household_Intelligent_Platform/)
	•	Existing site canonical: HIP_Site_Canonical (id 1TFUJAoGVCiFC130crsY_5lElR2G96-V3)
	•	HIP working folder: Household_Intelligent_Platform (id 1xQIBJgNSkrdRoq4eoeK6QcLvPQ5kLOn6)
2. Package structure (Option B, four artifacts)
	•	HIP_WhitePaper_Confidential__v<TS>.docx Augmented public WP as base. Adds three-tier pricing model (Standard, Data-Sharing, Premium Data), cohort throttling, five-layer platform architecture with recovery-authority vs training-authority isolation, architecture-of-trust detail suitable for NDA.

	•	HIP_TechnicalAnnex__v<TS>.docx Four-tier routing internals with actual model selections per tier (qwen2.5:7b edge, Groq llama-3.1-8b mid, Groq llama-3.3-70b core, BYOK frontier). Bloom to tier mapping (L1-2 edge, L3-4 mid, L5-6 core). Canonical 10-attribute fact schema. qwen2.5:32b session-end extraction. Groq Llama 4 Scout for async fact-change detection (0.5s target). Confidential computing target: RTX PRO 6000 Blackwell + Llama 4 Scout FP4 via NIM. Key custody hierarchy from Feasibility doc. All 8 module specs referenced.

	•	HIP_FinancialAnnex__v<TS>.xlsx + HIP_FinancialAnnex__v<TS>.docx Refreshed Monte Carlo. Excel architecture: CONTROLS sheet with probability distribution parameters, 9 assumption sheets, CALCULATION sheet (log only, Python writes and formulas calculate), RESULTS sheet at P10/P25/P50/P75/P90, SCENARIO LOG. Discrete tail-risk scenarios: operator pullout, regulatory shock, valuation compression, supply chain failure. Written companion doc explains inputs, sensitivity, and what the distributions mean without opening the workbook. Prior version location: TO BE FOUND in Drive. If not recoverable, rebuild from architecture spec (adds ~1 day).

	•	HIP_PrototypeEvidence__v<TS>.docx The credibility document. What we built. What works. What the data shows. Session traces. Fact lifecycle examples. Routing accuracy. Latency histograms. KNOWN_ISSUES.md distilled. Three demo vignettes: care coordination, freshness handoff, passthrough consent.
3. Recipients and polish level
Package must serve three recipient classes without a rewrite:

	•	Cable operator senior leadership (technical + operational depth)
	•	Financial buyer or investor (economics + moat + risk)
	•	Strategic partner (NVIDIA, chip vendor, platform partner)

The four documents serve different recipients differently. WhitePaper Confidential and Prototype Evidence go to all three. Technical Annex weights toward operator and partner. Financial Annex weights toward investor and operator CFO organization.
4. Content rules (inherited from BUILD_REQUIREMENTS)
	•	No em dashes. No en dashes. Commas, periods, or word substitution.
	•	All body copy sourced from WP or from data captured in the prototype. No invented content.
	•	Clara Barcelo: NEVER appears. Anywhere.
	•	Watermark with recipient name at production time. Log the NDA date.
5. Prototype data requirements (feeds Prototype Evidence)
Coding thread must produce, before day 5:

	•	Session traces as newline-delimited JSON
	•	routing_matrix.csv, bloom_matrix.csv, latency_by_tier.csv, fact_lifecycle.csv
	•	Three demo vignettes as video or timestamped transcript
	•	All named __v, dropped in HIP_Prototype_Evidence Drive folder

Test data quality bar:

	•	Real speakers, real voices, at least three enrolled members
	•	At least 50 sessions across two weeks
	•	At least 500 fact assertions in the graph
	•	At least one fact retraction and one fact update captured

Unblocking decision required: multi-member testing needs a second person on the harness. If unavailable, scope of Prototype Evidence changes and must be re-declared before day 3.
6. Timeline (one week)
	•	Day 1-2: Technical Annex assembly from existing module specs + Feasibility doc + Key Custody
	•	Day 2-4: Prototype Evidence in parallel with capture work
	•	Day 3-5: Financial Annex, find and refresh Monte Carlo, or rebuild from architecture spec
	•	Day 5-6: WhitePaper Confidential, assembles last, references annexes
	•	Day 7: Package review, cross-references, versioning, canonical Drive folder consolidation
7. External research inputs required
Pull from ChatGPT with citations and dates:

Financial and market:

	•	HBM3E / HBM4 pricing trajectory, contract vs spot spread, take-or-pay coverage rates from Micron, SK Hynix, Samsung
	•	DDR5 RDIMM server-grade and enterprise NAND flash pricing per GB, July 2026, direction over next 24 months
	•	RTX PRO 6000 Blackwell pricing, availability, competing GPU classes for edge inference (L40S, RTX 6000 Ada, H100 secondhand)
	•	Neocloud GPU lease rates for H100, H200, B200, RTX PRO 6000 class (CoreWeave, Lambda, Runpod, Crusoe, Together), 6-month trend
	•	AWS Capacity Block pricing for same GPU classes
	•	OBBBA Section 168(k) latest IRS guidance, 5-year MACRS confirmation, state conformity map, any changes since July 2025

Regulatory: 7. State privacy law enforcement 2026 across the current 20-state landscape, settlement amounts, targeted industries 8. NYDFS 23 NYCRR Part 500 updates, third-party assessment requirements, SOC 2 Type II and ISO references 9. HIPAA in AI context, HHS OCR guidance on covered entities using AI for PHI, BAA requirements for AI vendors, recent settlements 10. EU AI Act status July 2026, active provisions, penalties, whether household AI is high-risk

Competitive: 11. Amazon Alexa+ subscriber count, integration depth, household vs individual modeling, privacy architecture claims 12. Google Gemini + Google Home integration, family account modeling, on-device vs cloud split 13. Apple Intelligence household features, Family Sharing + AI, Private Cloud Compute, shipped vs announced 14. Comcast + NVIDIA AI Grid deployment status, hub counts, GPU class, timeline 15. Charter Spectrum equivalent public statements on edge inference

Technical: 16. Open-weight model landscape July 2026, current leaders on Artificial Analysis Intelligence Index, Chatbot Arena, HELM; GLM-5.2 vs Llama-4 vs Qwen3 vs DeepSeek-R2; license terms 17. Confidential computing enclave options: NVIDIA Hopper CC, AMD SEV-SNP, Intel TDX; which are production-ready for GPU inference at scale mid-2026; real deployments 18. Voiceprint identification accuracy for household-size groups (4-8 members), FAR and FRR, robustness to acoustic conditions

Format: single prompt with all 18 items numbered. Ask for citations with dates and source URLs. Ask ChatGPT to flag anything low-confidence.
8. Distribution model
Superset ships as a zip to one named counterparty at a time.

	•	Recipient name embedded in filename: Superset__<recipient>__v<TS>.zip
	•	NDA execution date logged
	•	Watermark on each PDF derivative with recipient name and date
	•	Superset never posted to the site. Never emailed unencrypted. Delivery via Drive share to a named account, or password-protected zip.
9. Sources of record (existing material)
	•	HIP_White_Paper_Augmented__v20260702_1113.docx (public WP, formatted, in this session's outputs, needs to move to canonical)
	•	MASTER HANDOFF (Drive id 1JpyMPmMgN_Rz_AFtJx5bK9JF185EDBb2TdW2hBBjFwE)
	•	HIP Feasibility and Key Custody (Drive id 1lODBb-QTX_AaJ7cbcVtPJsTvSYjOxM)
	•	8 module specs (location TBD, need to inventory)
	•	KNOWN_ISSUES.md on harness at ~/hip-harness
	•	docs/HIP-Transfer-June27.md on harness
	•	docs/demo-script.md on harness
	•	Monte Carlo Excel (LOCATION UNKNOWN, first-day task: find or declare as needing rebuild)
10. Coding thread brief (test the prototype)
Required capture from the harness:

Session-level traces. For each test session, capture:

	•	Timestamp (session start, per-query start/end)
	•	Household member speaking (voiceprint ID + display name)
	•	Query text as transcribed
	•	Which tier the router chose (Primary, Freshness, Enclave, Passthrough)
	•	Which model handled it
	•	Bloom classification level (1-6)
	•	Latency broken down: transcription, routing decision, inference, TTS
	•	Response text
	•	Tokens in and out per model call
	•	Cost per query at each tier

Fact lifecycle traces. For a subset of sessions, capture:

	•	Fact asserted (10-attribute schema type)
	•	Confidence
	•	Temporal enrichment applied
	•	Fact-change detection event (async, Groq Llama 4 Scout)
	•	Retraction event if any, with reason
	•	Time between assertion and enrichment
	•	Time between assertion and detected change

Routing accuracy data. Multi-session batch:

	•	Sample of at least 200 queries labeled with intended tier vs actual tier
	•	Confusion matrix
	•	Cases where router made the wrong choice and why

Bloom classification data. Same 200-query sample:

	•	Human label of Bloom level vs system label
	•	Agreement rate
	•	Where the system disagrees, over vs under classification

Demo vignettes required:

	•	Care coordination. Multi-turn session on a parent's medication change. Show identity scoping, fact assertion, temporal enrichment, connection to earlier context. All queries stay in Primary or Enclave tier.
	•	Freshness handoff. Query needing live web data. Show generic query text sent out (no household context), result returned, synthesis with household context locally.
	•	Passthrough consent. Subscriber requesting a frontier model for a specific query. Show system announcing the crossing, subscriber consenting or declining, both stripped-context and sensitive-context paths captured.

Quality bar:

	•	Real speakers, real voices, at least three enrolled members
	•	At least 50 sessions across two weeks
	•	At least 500 fact assertions in the graph
	•	At least one fact retraction and one fact update captured
	•	Latency from real hardware (Mac Mini M1 Pro), not projections

Do NOT:

	•	Fabricate metrics
	•	Fix bugs quietly during capture window
	•	Stage or cherry-pick vignettes to hide routing failures

Delivery:

	•	Session logs as newline-delimited JSON, one file per session
	•	Aggregate CSVs
	•	Demo vignettes as video or timestamped transcript
	•	All __v, dropped in HIP_Prototype_Evidence
11. Kickoff line for future threads
Superset session. Read the most recent SUPERSET_PROJECT_BRIEF__v*.md from Drive folder HIP_Superset_Canonical before doing anything else. Follow all naming, canonical, and distribution rules in that file.
12. Edit history
v20260702_1130 (initial)

	•	Package structure locked: Option B, four artifacts.
	•	One-week timeline defined.
	•	Prototype data requirements defined for coding thread.
	•	External research inputs listed for ChatGPT pull.
	•	Distribution model defined: per-recipient zips, watermarked, logged.

