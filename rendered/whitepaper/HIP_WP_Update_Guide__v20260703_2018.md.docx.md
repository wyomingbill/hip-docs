HIP White Paper and NDA Document Update Guide
v20260703_2018 MT. Supersedes HIP_Site_Changes_for_WP_NDA__v20260703_1016.md.

This document captures every change, research finding, term definition, AI baseline concept, and fact-check correction from the July 3, 2026 session. Use it as the authoritative guide for updating the public White Paper, WhitePaper Confidential, Technical Annex, Financial Annex written companion, and Prototype Evidence documents.

The site at hip.olindasolutions.com is the reference. Where the site and any prior WP draft conflict, the site governs.


1. AI baseline concepts (new content for WP)
The WP currently assumes the reader understands how AI works. The site now includes three inline sections that ground the reader without condescension. The WP should carry equivalent content.
1.1 Context windows and persistent state
Site location: architecture.html, new section "How AI works today, and why it is not enough," positioned before "The four tiers."

Core content for WP:

Most AI products operate inside a context window: a fixed amount of working memory, typically tens of thousands of words, that holds the current conversation and whatever the product retrieves from its integrations. When the conversation ends, the window clears. The next session starts empty. Some products now offer a "memory" feature that carries a short summary forward, but it is a compressed residue, not a structured understanding.

That design works for a single user asking a single question. It does not work for a household. A household needs context that persists across members, across months, across decisions that reference other decisions. It needs attributed memory: who said what, when, with what authority, and whether it is still true. No context window holds that. No session summary reconstructs it.

HIP replaces the context window with a persistent context graph. The graph is not a chat history. It is a structured, encrypted, temporally-aware store of household facts, relationships, and patterns that compounds with every interaction and never resets.

WP placement: Part I or Part II, before the architecture chapter. Frame as the baseline the reader needs to evaluate the routing architecture.
1.2 Generative AI vs agentic AI, with household goal framing
Site location: platform.html, new section "From generative to agentic," positioned before "The five kernel services."

Core content for WP:

The AI products most people have used are generative: they produce text, images, or summaries in response to a prompt. The user asks, the system answers, the interaction ends.

Agentic AI is a different category. An agent does not just answer. It plans, uses tools, and takes actions on your behalf: scheduling an appointment, filing an insurance claim, coordinating a medication change across family members and a provider. The difference is not intelligence. It is authority. An agent acts, and acting requires identity (who is authorizing this), context (what does the agent know about the household), trust (what is the agent allowed to do), and governance (who reviews, approves, and audits).

Agentic AI also requires a goal. In an enterprise, goals are set by the employer. In a household, goals take a different form: standing instructions set by family members. "Remind me if the refill is not confirmed by Thursday." "Alert us if spending on the project passes a threshold." "If nobody has checked in on Dad by 6pm, text Sarah." The household defines what matters. The system watches, and acts when conditions are met. It does not decide what the household should care about.

Those requirements are why the five kernel services exist. Identity, context, trust, inference, and institutional integration are not features of an application. They are the operating-system layer that makes agentic AI possible in the household. Without them, AI in the home stays conversational. With them, it becomes operational.

WP placement: Part VIII (Platform) or a new Part between Architecture and Platform. Must precede the kernel services discussion.
1.3 Model Context Protocol and the certified trust plane
Site location: platform.html, inside "Institutional integration" kernel description.

Core content for WP:

The emerging industry standard for connecting AI models to external tools and data sources is the Model Context Protocol (MCP). MCP is powerful but open by design: any tool connected is trusted by default, with no identity layer, no consent framework, and no audit trail. The institutional integration kernel functions as a certified equivalent, with the identity, consent, and audit layers that regulated institutions require before they will connect. A bank will not plug into an open MCP. A bank will connect to a trust plane that carries the certification stack, the consent trail, and the custody model its compliance team needs to see.

WP placement: Inside the platform chapter, under the institutional integration kernel description. Also reference in the architecture chapter where the trust boundary is described.


2. Fifth kernel service: Institutional integration
Site location: platform.html, section "The five kernel services."

The WP currently describes four kernel services: Identity, Context, Trust, Inference. Update to five.

New kernel description for WP:

Institutional integration. HIP exposes a certified integration surface for the regulated institutions that need to reach into households, including banking, financial services, insurance, and healthcare. The certification stack, spanning SOC 2 Type II, ISO 27701, HIPAA covered-entity readiness, NYDFS Part 500 conformance, and equivalent frameworks by jurisdiction, is held at the platform level and audited on the platform's schedule. Applications that pass their own category-specific certification gate then use this kernel directly, without having to build their own compliance posture, their own vendor-risk relationships with regulated counterparties, or their own auditable custody chain. Once an application is certified for its category, it inherits the platform's institutional standing and can connect households to regulated services through a surface those institutions already accept.

Update every "four kernel services" reference to "five."


3. Application sequencing (replaces launch wedge)
Site location: platform.html, section "The application sequence." operator-case.html, section "Application sequence."

Change from prior WP language: "Family care coordination is the first application shipped" is retired. Replaced with friction-ordered portfolio sequencing.

Heading: "Simple applications ship first. Regulated applications follow."

Core content for WP:

The application catalog is prioritized by three variables at once: build-and-certify friction, strategic importance to the operator, and the depth of household context each category requires. The categories that ship first are the ones that need the least regulatory posture, the least third-party paper, and the shallowest context to be useful on day one.

Household coordination, finance visibility, security integration, and household knowledge are candidate near-term categories. Regulated categories that require HIPAA covered-entity status, FDA analysis, or provider-network agreements are candidates for later phases.

Family care coordination is a strategic destination category. The unmet demand is quantified, the buyer is identified, and the fit is real. It is also the category with the highest certification, partnership, and political lift, and it depends on trust substrate the earlier categories build.

Applications reach the platform from three routes: operator-built, partner-built, and acquired. The operator holds optionality on which categories to build in-house, which to open to partners, and which to bring in through acquisition once traction is demonstrated.

WP placement: Platform chapter (Part VIII). Replace the existing launch-wedge content.


4. Operator Case
Site location: operator-case.html (new page).

The WP Confidential should include an operator case chapter matching the site page. Eight sections:

	•	Why this matters to cable now (rare control-point opportunity)
	•	Retention and ARPU impact
	•	Required infrastructure (rack-level, not campus-level)
	•	Application sequence (friction-ordered, per section 3 above)
	•	Deployment path (full deployment base case, success-based option)
	•	Financial bridge (lease-back, bonus depreciation, asset life)
	•	Risk controls (memory-price, lease-market, open-model, competitive, regulatory, each with documented response)
	•	Next step (scoped review, not a pitch)

Framing throughout: "rare control-point opportunity," not "HIP is inevitable."


5. Success-based rollout optionality
Site location: economics.html, section "Rollout optionality." operator-case.html, section "Deployment path."

Core content for WP:

Two rollout models. Base case is full deployment. Success-based rollout makes growth capex conditional on realized subscriber penetration.

Trade-off stated honestly: better capital efficiency and lower early exposure, at the cost of twelve to eighteen months of extended timeline to full-footprint economics.

Operator-only targeting advantage: billing and service data for identifying high-conversion households (multi-service, on-time payers, smart-home inquiries, care-relevant demographics). Not available to Amazon, Google, or Apple at household-level fidelity.

WP placement: Economics chapter, between "The objection" and "What the model does not assume." Also referenced in the operator case chapter.


6. Governance flows
Site location: architecture.html, final paragraph of "Data protection" section.

Core content for WP:

Governance is part of the architecture, not an addendum. First-class flows for:

	•	Recovery when a key is lost
	•	Access when a household member leaves
	•	Guardianship over minors and eldercare
	•	Response under legal process
	•	Handling of coercion and abuse cases
	•	Support-personnel visibility limits

WP placement: Architecture chapter (Part III), as a subsection following the data protection and key custody discussion. Technical Annex should expand each flow with actors, state transitions, cryptographic operations, and audit trail.


7. Categorical claim softening (fact-check driven)
The following formulations were found to be overclaims or borderline defensible by the ChatGPT adversarial fact-check (48 items reviewed). All have been corrected on the site. WP must carry the same corrections.
Replace throughout WP and NDA docs:
OLD (do not use)
NEW (use this)
"No system on the market is designed to hold it."
"No large consumer AI platform currently combines household-scoped identity, persistent shared context, household-held custody, and operator-edge inference in one architecture."
"The frontier laboratories cannot build it."
"The frontier laboratories are structurally disincented from building it."
"The device makers cannot build it."
"The device makers are constrained."
"The hyperscalers cannot build it."
"The hyperscalers are misaligned."
"The operator cannot read the data even with physical access."
"The architecture is designed so the operator does not hold plaintext household content or the keys required to decrypt it, subject to the threat model detailed in the technical package."
"Everything is encrypted with a key derived from household voiceprints."
"Cryptographic keys are generated and held in secure elements under the household, with voice authentication acting as one factor in policy-controlled access."
"Each of these forces fits HIP exactly."
"Each has now converged on a shape that maps closely to what HIP is built to hold."
"The catalog is ordered by friction, not by desirability."
"Simple applications ship first. Regulated applications follow."
Principle:
Any sentence that begins "X cannot Y" or claims a competitor is definitionally excluded should be reviewed. Trade-off framing survives scrutiny; categorical framing does not.


8. Research field notes (sourced evidence for WP)
Three research-backed field notes are now live on the site with tightened language per ChatGPT adversarial fact-check. The WP should carry equivalent citations.
8.1 Pew: 71% say AI makes personal info less secure
Source: Pew Research Center, Americans and AI 2026, June 17, 2026, 5,119 U.S. adults. URL: https://www.pewresearch.org/internet/2026/06/17/americans-and-ai-2026-chatbots-smart-devices-and-views-on-impact/

Defensible interpretation: The data validates privacy and custody as first-order adoption barriers for household AI. An architecture in which the operator does not hold plaintext household data addresses the concern the market has already named. It does not prove demand for HIP specifically.

Also from same source: 59% have little or no confidence U.S. companies will develop and use AI responsibly. 3% believe AI will make personal information more secure.

WP placement: Forces chapter, privacy reckoning section.
8.2 YouGov: 68% won't let AI act unsupervised
Source: YouGov, Most Americans use AI but still don't trust it, December 9, 2025, 1,187 U.S. adults. URL: https://yougov.com/en-us/articles/53701-most-americans-use-ai-but-still-dont-trust-it

Defensible interpretation: The market is not ready for unsupervised agentic AI. Consumers will require explicit review, permissioning, and governance before trusting AI systems to act on their behalf. HIP's governance and institutional-integration layers are designed around that adoption barrier.

Also from same source: Only 18% would trust AI even somewhat to make a decision or take an action. 5% trust AI "a lot." 41% distrust. Trust is lower for high-stakes: 19% for finance, 23% for health.

WP placement: Platform chapter, after the agentic AI / kernel services discussion.
8.3 Pew: 49% use chatbots, 24% daily
Source: Pew Research Center, Americans and AI 2026, June 17, 2026, 5,119 U.S. adults. URL: https://www.pewresearch.org/internet/2026/06/17/americans-and-ai-2026-chatbots-smart-devices-and-views-on-impact/

Defensible interpretation: The adoption gap is narrowing. The architecture gap remains. Mainstream chatbots are still primarily individual-user products, not persistent household-context systems. Half the operator's subscriber base is already using AI. The question is whether the operator provides the household layer, or cedes that position to a platform that does not share the operator's custodial relationship.

Also from same source: ChatGPT 44%, Gemini 24%, Copilot 17%, Meta AI 14%, Grok 8%, Claude 6%. 60% have read AI summaries in search results.

WP placement: Why Now chapter.


9. Research data for internal use only (NOT for the site or WP)
The following findings from the AI literacy research pass are useful for calibrating how to write and for pitch conversations. They should NOT appear on the site or in published documents because the interpretations are heuristic, not measured.
9.1 Three-group population segmentation (internal framework)
Derived from combining Pew, YouGov, and Oxford data:

	•	Active users who do not understand the mechanism (~25%)
	•	Aware non-users who distrust AI (~35%)
	•	Non-aware or indifferent (~40%)

Use as qualitative planning framework. Do not present with percentages. Do not publish.
9.2 67% attribute consciousness to ChatGPT (Oxford, n=300)
Interesting but too small a sample and too many inferential leaps for a boardroom-grade document. Dropped from site field notes. Keep as conversation ammunition only.
9.3 No survey measures context window understanding
Absence finding. No major 2023-2026 general-population survey directly tests whether typical users understand context windows, session persistence, or training vs inference. Treat these concepts as technical and explain plainly on first use. Do not claim "nobody understands."
9.4 "Agentic AI" is an industry term
Consumer research measures trust in AI actions, not familiarity with the term "agentic." Translate to ordinary language when writing: "AI that can make decisions or take actions on your behalf."
9.5 Privacy concern is real but not yet architecture-specific
Pew's 71% is broad. Consumers are not yet translating fears into demands for custody, local processing, or key ownership. The concern clusters around data access, surveillance, misuse, breaches, and control. Use this to frame HIP as addressing what consumers feel but cannot yet articulate.


10. Term definitions (glossary for WP appendix)
The site now carries 41 tooltip definitions. The WP should include a Terms and Acronyms section (which already exists) updated with these definitions. Below are the terms added in this session that may not already be in the WP glossary.
AI fundamentals
Term
Definition
GPU
Graphics processing unit. Originally designed for rendering images, now the primary hardware for running AI models. GPUs process many calculations simultaneously, which is what AI inference requires.
AI model / LLM
A software system trained on large amounts of text to predict and generate language. ChatGPT, Claude, Gemini, and Llama are examples.
Inference
Running a trained AI model to produce an answer. Training is expensive and happens once. Inference is cheap and happens every time someone asks a question.
Training
The process of building an AI model by exposing it to large datasets. Costs millions of dollars and requires specialized hardware.
Context window
The amount of text an AI model can hold in working memory during a single conversation. When the window fills, older content is dropped. Between sessions, the window resets entirely.
Frontier model
The most capable AI model available at any given time, typically proprietary and accessible only through a paid API.
Open-weight model
An AI model whose trained parameters are publicly available for download, self-hosting, and modification.
Token
The unit of text an AI model processes. Roughly three-quarters of a word.
Generative AI
AI that produces text, images, code, or other content in response to a prompt.
Agentic AI
AI that can plan, use tools, and take actions on behalf of a user, not just generate text. Requires identity, context, trust, and explicit authorization.
Hallucination
When an AI model confidently produces false or fabricated information.
Edge inference
Running an AI model on infrastructure close to the user, rather than in a distant centralized datacenter.
MCP
Model Context Protocol. An emerging standard for connecting AI models to external tools and data sources.
Hyperscaler
A largest-scale cloud provider such as AWS, Microsoft Azure, or Google Cloud.
Neocloud
A specialized cloud provider focused on GPU compute for AI workloads. CoreWeave, Lambda, RunPod, Crusoe.
Context graph
The organized, structured store of a household's facts, relationships, and patterns. Not a chat history.
Model names referenced on the site
Model
Definition
Llama 2
Meta's 2023 open-weight language model. First large open model competitive enough to shift industry assumptions.
GPT-4
OpenAI's 2023 flagship proprietary model. Set the frontier benchmark open weights have been closing against.
Mixtral
Mistral AI's open-weight mixture-of-experts model. Demonstrated efficient open models could match larger closed ones.
Llama 3.1 405B
Meta's 2024 open-weight model, 405B parameters. Closed the gap to frontier to a few months.
DeepSeek R1
DeepSeek's 2025 reasoning-focused open-weight model. Pulled the gap to weeks.
GPT-5
OpenAI's 2025 successor to GPT-4. Matched by open weights within a single quarter.
GLM-5.2
Z.ai's mid-2026 open-weight model. 750B MoE, MIT license. Current leading open-weight on capability indices.
Hardware and infrastructure
Term
Definition
RTX PRO 6000 Blackwell
NVIDIA's current workstation-class GPU, 96GB GDDR7. Reference hardware for HIP edge nodes. MSRP ~$13,250.
V100
NVIDIA's 2017-era datacenter GPU. Now used for inference and batch. Still commercially available on AWS.
HBM
High bandwidth memory. Premium memory stacked on AI accelerator chips. Required for frontier training, not for household inference.
DRAM / DDR5
Standard system memory. Cheaper than HBM. Sufficient for inference workloads.
NAND / SSD
Flash storage. Cheapest memory tier. HIP's persistent context graph lives here.
NIM
NVIDIA Inference Microservices. Packaged deployment framework for AI models on NVIDIA hardware.
Confidential computing
Hardware-secured compute where data is encrypted in memory and during processing.
Secure element
Tamper-resistant hardware chip for storing cryptographic keys.
PHY
Physical layer functions in a cable network. Signal processing for RF over coax.
MACPHY
Combined media access control and physical layer. Remote MACPHY moves these to edge nodes, freeing hub space.
Cable/telecom
Term
Definition
DOCSIS 4.0
Standard governing broadband over cable. V4.0 enables multi-gigabit and frees hub rack space.
DAA
Distributed access architecture. Moves processing closer to subscriber, frees hub space.
Hub / headend
Powered, secured facilities in cable networks. Hubs serve neighborhoods, headends serve regions.
CPE
Customer premises equipment. The modem or gateway in the home.
MSO
Multiple system operator. A company operating cable systems across multiple markets.
ARPU
Average revenue per user per month.
Net adds
Subscribers gained minus lost in a period.
HFC
Hybrid fiber-coax. Cable's physical network.
Financial/regulatory
Term
Definition
MACRS
IRS depreciation method. Computer equipment depreciates over 5 years.
Section 168(k)
Tax code section governing bonus depreciation. Currently allows 100% year-one deduction.
SOC 2 Type II
Independent security audit. Required by enterprise and regulated buyers.
HITRUST CSF
Certification framework combining HIPAA, ISO, NIST standards. Healthcare-adjacent requirement.
HIPAA
Federal law governing privacy/security of protected health information.
NYDFS Part 500
New York cybersecurity regulation for financial services.
BAA
Business associate agreement. HIPAA-required contract for PHI handling.
Take-or-pay
Supply contract with minimum purchase commitment.
WACC
Weighted average cost of capital. Discount rate for financial models.
Bonus depreciation
100% year-one equipment deduction under current law.
GDPR
EU data protection regulation. Fines up to 4% of global revenue.
FERPA
Federal law protecting student education records.
ISO 27701
International privacy information management standard extending ISO 27001.


11. Economics section reorder
Site location: economics.html

Current site order (corrected in this session):

	•	The deployment cost
	•	After-tax
	•	Asset life
	•	Why this matters for HIP
	•	The objection
	•	The lease-back bridge
	•	Rollout optionality
	•	What the model does not assume
	•	The risk case

Prior order had Rollout optionality between The objection and The lease-back bridge, which interrupted the question-then-answer flow. WP economics chapter should follow the corrected order.

Also added to "What the model does not assume": "The full model runs 10,000 Monte Carlo scenarios across three subscriber scales, with every input drawn from a documented probability distribution."


12. Lead paragraph updates
12.1 Public page (index.html)
New lead replaces "AI remembers you now" intro:

"AI is being built for the enterprise. Not for the household. The major labs are building copilots for code and documents, agents for office work, and assistants that make an individual employee more productive. Even the consumer efforts are aimed at the single user..."

Closes with the compound defensible claim: "No large consumer AI platform currently combines household-scoped identity, persistent shared context, household-held custody, and operator-edge inference in one architecture."
12.2 Overview page (overview.html)
New lead replaces prior "The problem" section. Structured with two standalone beat lines: "That is the gap." and "A household is not one user." Closes with: "It does not yet understand the home."

Both leads should inform the WP executive summary and Part I framing.


13. Bill Brewster profile
Site location: deep-dive.html, new "About the author" section before footer.

Content for WP author page or cover letter:

Twenty years building and operating governed, multi-entity service delivery systems across cable, telecom, software, and advertising technology. SVP and General Manager at Canoe Ventures, where he built the national addressable advertising platform across six cable operators. National Video Operations and X1 platform at Comcast, where he helped architect and scale the platform now deployed to tens of millions of households. VP Solutions at Mentis Broadband. Director of Business Operations at AT&T/TCI.

The HIP thesis is grounded in operational experience with the specific systems cable operators run: headend and hub infrastructure, subscriber management, conditional access, content delivery, advertising operations, and the capital planning that governs all of them.


14. Deep Dive page CTA updates
Site location: deep-dive.html

Reader-scoped package framing (CTO, CFO, strategy, legal) with two CTA buttons: "Request NDA package" (mailto with pre-filled body) and "Schedule a technical review" (Google Calendar booking link).

Also on operator-case.html: "Schedule a review" button links to same Google Calendar. Both use: https://calendar.app.google/K9kYgx9tuq5JYucu8


15. Financial Annex rebase items (Round 2)
Flagged for the Monte Carlo workbook rebuild:

	•	Application sequencing shift. Family care is no longer the ramp driver. Rebase to platform subscription + household coordination as month-one revenue. Family care as year-3+ regulated category.
	•	Institutional integration as a separate revenue line, not a footnote.
	•	Success-based rollout as an explicit scenario with 12-18 month timeline shift.
	•	Certification cost as OPEX line item (HITRUST, HIPAA, NYDFS Part 500, SOC 2 Type II).
	•	Tier pricing re-anchored: Premium $19.99 anchored to YouTube Premium comp (30-40M US paying households). Data-Sharing tier lowered to 20% mode (pay-to-escape-data revealed preference). Standard absorbs the shift to 65% mode.


16. Existing field notes inventory (already on site, fold into WP)
17 sourced field notes across 7 pages. All carry linked primary sources. Full inventory in HIP_FieldNote_Sources__v20260703_0823.md. Priority items for WP:

	•	Charter + Comcast NVIDIA AI Grid (substrate proof)
	•	Amazon Alexa+ 97% device coverage (competitor validation)
	•	Google Gemini for Home (household category validation)
	•	RTX PRO 6000 Blackwell $13,250 MSRP (hardware pricing)
	•	Micron HBM fully contracted through 2026 (memory bottleneck)
	•	OBBBA 100% bonus depreciation permanent (tax treatment)
	•	California GM $12.75M privacy settlement (enforcement dollars)
	•	Edelman Trust Barometer 2026 (custodian argument)
	•	EU AI Act high-risk delay to December 2027 (regulatory)
	•	Epoch AI open-vs-closed gap at 4 months (open-weight thesis)
	•	Comcast 82K broadband losses + 3.6% ARPU growth Q1 2026 (urgency)
	•	AARP $1.01T unpaid family caregiving (demand quantification)
	•	Blackwell CC 13-27% throughput penalty (enclave pricing)
	•	Microsoft 4-to-6-year server useful life (asset life defense)
	•	NVIDIA L40S/L4 inference bifurcation (two-phase asset life)
	•	Neocloud + AWS Capacity Blocks pricing (bridge revenue)
	•	Microsoft Wisconsin datacenter cancellation (backlash pattern)
	•	Pew 71% privacy concern (adoption barrier, new this session)
	•	YouGov 68% trust-to-act (agentic barrier, new this session)
	•	Pew 49% chatbot usage (market timing, new this session)


17. Power reckoning (pending, not yet on site)
ChatGPT research prompt drafted for four items:

	•	Grid Strategies LLC load growth report
	•	PJM capacity auction 833% price spike
	•	FERC Amazon/Talen behind-the-meter rejection
	•	Hyperscaler nuclear scramble (Microsoft/Constellation TMI, Google/Kairos, Amazon/Talen Cumulus)

When research returns, callouts go on forces.html under AI build-out backlash. WP forces chapter gets a "Grid physics" subsection.


18. Fact-check driven language calibration
48 claims reviewed adversarially. Results:

	•	40 site claims checked: most FACT or DEFENSIBLE. Categorical claims (items 2, 3, 13, 14, 34) required softening, all corrected on site per section 7 above.
	•	8 research/interpretation claims checked: items 41-43 DEFENSIBLE with tightened language (applied). Item 44 OVERCLAIM (dropped). Items 45-48 internal-use-only (section 9 above).

Full fact-check results available in the ChatGPT response document. Reference when writing WP to ensure no overclaim language creeps back in.


19. Site-to-document mapping (reference)
Site page
WP chapter
NDA document
overview.html
Executive Summary, Part I
WhitePaper Confidential
forces.html
Part II: Forces
WhitePaper Confidential
moat.html
Part III: The Moat
WhitePaper Confidential
architecture.html
Part III: Architecture
Technical Annex
platform.html
Part VIII: Platform
WhitePaper Confidential, Technical Annex
substrate.html
Parts IV-VI
Technical Annex
economics.html
Part VII-VIII
Financial Annex companion
operator-case.html
New chapter
WhitePaper Confidential
why-now.html
Part IX: Why Now
WhitePaper Confidential
deep-dive.html
Cover letter / transmittal
NDA package framing


20. Edit history
v20260703_2018 (this version)

	•	Supersedes v20260703_1016.
	•	Added: AI baseline concepts (context windows, generative vs agentic with goal framing, MCP/trust plane).
	•	Added: 41 term definitions with tooltips (glossary for WP appendix).
	•	Added: three research field notes with fact-checked language.
	•	Added: internal-use-only research calibration data.
	•	Added: Financial Annex Round 2 rebase items including tier pricing re-anchoring and certification OPEX.
	•	Added: economics section reorder and Monte Carlo sentence.
	•	Added: lead paragraph updates for index and overview.
	•	Added: Bill Brewster author profile.
	•	Added: Deep Dive and Operator Case CTA updates with calendar link.
	•	Preserved: all field note sources with URLs from v1016.
	•	Preserved: categorical softening table from v1016.
	•	Preserved: governance flows from v1016.


21. Power reckoning (COMPLETED, now on site)
Supersedes section 17 which flagged this as pending. Research returned, field notes built, conclusion written.
21.1 Site location
forces.html, AI build-out backlash section. Four callouts in sequence followed by a two-paragraph conclusion:

	•	Memphis Starlink discount (existing)
	•	Microsoft Wisconsin datacenter cancellation (existing)
	•	Grid load spike + PJM 833% capacity auction (new)
	•	Hyperscaler nuclear scramble: FERC/Talen + Microsoft/TMI (new)
	•	Conclusion: consumer subsidy + HIP positioning advantage (new)

Also: operator-case.html, Required Infrastructure section, new paragraph on positioning advantage.
21.2 Core content for WP forces chapter
Grid load spike:

U.S. electricity demand was essentially flat for twenty years. In December 2023, Grid Strategies LLC reported that five-year peak demand growth forecasts from regional grid operators had nearly doubled in a single year. The reversal is driven by datacenter construction, industrial reshoring, and electrification hitting a grid that was not built to absorb them simultaneously.

The market consequence arrived in July 2024. PJM's Base Residual Auction for the 2025-2026 delivery year cleared at $269.92 per MW-day, up from $28.92 the prior year. That is an 833 percent increase in the cost of grid reliability, paid by utilities and passed to ratepayers across 13 states and Washington, D.C.

Sources:

	•	Grid Strategies LLC: https://gridstrategiesllc.com/wp-content/uploads/2023/12/National-Load-Growth-Report-2023.pdf
	•	PJM Interconnection: https://insidelines.pjm.com/pjm-capacity-auction-secures-resources-six-years-in-advance/

Hyperscaler nuclear scramble:

In November 2024, FERC rejected a proposed arrangement between Amazon and Talen Energy to supply datacenter power directly from the Susquehanna nuclear plant in Pennsylvania through a behind-the-meter connection, bypassing the public grid. FERC found the arrangement could compromise grid reliability for other ratepayers. In September 2024, Microsoft signed a 20-year power purchase agreement with Constellation Energy to restart Three Mile Island Unit 1, a shuttered nuclear reactor, at a reported premium of approximately $100 per MWh, roughly double the average wholesale price.

Sources:

	•	Reuters (FERC/Talen): https://www.reuters.com/business/energy/us-ferc-rejects-talen-energy-amazon-power-deal-2024-11-01/
	•	Reuters (Microsoft/Constellation): https://www.reuters.com/markets/deals/constellation-inks-power-deal-with-microsoft-restart-three-mile-island-reactor-2024-09-20/
21.3 Five leaps the WP must make explicitly
The WP should not just report the data. It should draw the conclusions. These are defensible, not categorical. Each follows from the evidence.

Leap 1: Same household, both sides. The household paying higher electricity rates because of datacenter load growth is the same household that would subscribe to HIP. The PJM capacity price spike flows to residential bills across 13 states. HIP's edge model uses existing power in existing facilities. The household gets AI without subsidizing someone else's datacenter.

Leap 2: Political tailwind HIP rides for free. Community opposition to datacenters, rate-case fights at state PUCs, FERC blocking behind-the-meter deals, cancelled projects in Wisconsin. These are not HIP's problems. They are HIP's proof environment. Every fight the centralized model loses makes the distributed model more attractive to the operator and more defensible to the regulator. The WP should state this directly.

Leap 3: Operator gets a positioning statement no hyperscaler can claim. A cable operator deploying HIP can say: "We bring AI to your home without building a datacenter in your neighborhood, without raising your electricity bill, without consuming your water." Amazon, Google, and Microsoft cannot make that statement. The operator case chapter should carry this language.

Leap 4: Power crisis connects to the trust argument. The communities opposing datacenters are the same households that do not trust Big Tech with their data. Opposition to the infrastructure and distrust of the custodian are the same sentiment expressed in two different forums. HIP addresses both: private custody AND community-aligned deployment. The moat chapter should connect these.

Leap 5: Consumer acquisition message. "Your AI does not cost your neighbor anything" is a message that resonates in exactly the markets where datacenter opposition is highest, which are also the markets where cable operators have the densest subscriber bases (Virginia, Georgia, Ohio, Texas). The operator case chapter should name this positioning explicitly.
21.4 Additional terms for WP glossary
Term
Definition
PJM
PJM Interconnection. The regional transmission organization coordinating the wholesale electricity market across 13 U.S. states and Washington, D.C.
Base Residual Auction
PJM's annual auction procuring capacity commitments from power generators. Clearing price sets the cost of grid reliability, passed to ratepayers.
MW-day
Megawatt-day. Unit of capacity pricing in wholesale electricity markets.
Behind-the-meter
A power arrangement where a large consumer connects directly to a generator on the same site, bypassing the public grid.
PPA
Power purchase agreement. A long-term contract fixing the price of electricity between a generator and a buyer.
Grid interconnection queue
The formal process for connecting a new power source or large load to the electrical grid. Wait times average five or more years in the largest U.S. markets.
21.5 Pending research: state PUC rate cases
A ChatGPT prompt has been staged (ChatGPT_RateCase_Research__v20260703_2101.md) targeting five items:

	•	Virginia Dominion Energy datacenter rate allocation
	•	Ohio AEP datacenter tariff proposal
	•	Georgia Power datacenter load forecast and rate impact
	•	Any other state with datacenter-driven residential rate increases
	•	National framing piece (Reuters/Bloomberg/WSJ)

When research returns, one additional field note will be added to forces.html with specific dollar amounts showing residential ratepayers subsidizing datacenter load. This closes the evidence chain with hard numbers.
21.6 WP chapter placement
	•	Forces chapter: full power reckoning subsection with both field notes and all five leaps stated explicitly.
	•	Economics chapter: cross-reference to power advantage (HIP adds no material grid load).
	•	Operator Case chapter: positioning advantage paragraph (no datacenter, no rate increase, no water).
	•	Moat chapter: connection between infrastructure opposition and data trust (same sentiment, two forums).
	•	Why Now chapter: reference to accelerating tailwind (each centralized loss strengthens distributed case).


22. Updated edit history
v20260703_2018 (initial)

	•	Comprehensive guide created with 20 sections.

v20260703_2107 (this addendum)

	•	Section 21 added: power reckoning completed with five explicit leaps.
	•	Section 17 (pending) superseded.
	•	Six new glossary terms added.
	•	Rate-case research prompt flagged as pending.
	•	WP chapter placement mapped for power content.

