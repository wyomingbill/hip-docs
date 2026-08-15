# HIP Pending Queue

Master tracking document. Everything not yet built lives here.
Check this file at the start of every session.

Last updated: v20260707_2230 MT

---

## SITE — Ready to build (no dependencies)

All items below have sources confirmed. Build on next site session.

### Field notes queued

| # | Item | Page | Source confirmed | Status |
|---|---|---|---|---|
| 1 | Water consumption (Google 5.6B gal, Microsoft +34%) | forces.html | Yes (Google/Microsoft sustainability reports) | IN v1506, verify in CC merge |
| 2 | Interconnection queue (2,600 GW, 5+ year, 20-30% completion) | forces.html | Yes (Berkeley Lab) | IN v1506, verify in CC merge |
| 3 | State rate cases (VA GS-5, OH AEP, GA Power, PA PUC) | forces.html | Yes (Reuters + state PUC dockets) | IN v1506, verify in CC merge |
| 4 | Grid Strategies update (coal retirement + 0.5% to 5%) | forces.html | Yes (Grid Strategies LLC) | IN v1506, verify in CC merge |
| 5 | Nuclear scramble update (Google/Kairos, Meta RFPs) | forces.html | Yes (Reuters) | IN v1506, verify in CC merge |
| 6 | Meta Louisiana $2B revised deal | forces.html | Yes (Reuters) | IN v1506, verify in CC merge |
| 7 | Fierce Network edge use case debate | why-now.html | Yes (Fierce Network URL) | IN v2206 |
| 8 | Latis / Charter household intelligence | why-now.html + moat.html | Yes (Parks Associates / LinkedIn) | IN v2206 |

### Analytical sections queued

| # | Item | Page | Status |
|---|---|---|---|
| 9 | Value extraction / "context is not extracted" + alpha | moat.html | IN v1506, verify in CC merge |
| 10 | AI stack economics (four layers, HIP skips 2-3) | economics.html | IN v1506, verify in CC merge |
| 11 | Enterprise parallel (smartest enterprises moving to open weights) | substrate.html | IN v1506, verify in CC merge |

### Content changes queued

| # | Item | Page | Status |
|---|---|---|---|
| 12 | "Household context layer does not exist" -> "is being claimed" | why-now.html | IN v2206 |
| 13 | Latis extraction contrast in moat | moat.html | IN v2206 |

---

## SITE — Need to verify CC merge

Items 1-6 and 9-11 were built in v1506 from my working tree.
CC deployed a different version. v2206 merged Fierce + Latis onto CC's base.
MUST VERIFY: did CC's deployed version already contain items 1-6 and 9-11,
or were those lost when CC deployed? If lost, rebuild on CC base.

Action: diff v2206 against v1506 for forces.html, moat.html, economics.html, substrate.html.

---

## WP — Updates needed

These changes are on the site but NOT yet in the canonical WP (v1655).

| # | Item | WP section |
|---|---|---|
| 14 | Fierce Network edge use case | Why Now |
| 15 | Latis / Charter competitive response | Why Now + Moat |
| 16 | "Context layer being claimed" language | Why Now |
| 17 | Water consumption field note | Forces |
| 18 | Interconnection queue field note | Forces |
| 19 | State rate cases field note | Forces |
| 20 | Meta Louisiana field note | Forces |
| 21 | Grid + nuclear updates | Forces |
| 22 | Value extraction + alpha section | Moat |
| 23 | Stack economics section | Economics |
| 24 | Enterprise parallel | Substrate |

---

## NDA DELIVERABLES — Status

| Deliverable | Status | Next step |
|---|---|---|
| WhitePaper Confidential | v20260704_2142 (Parts I-XIV merged) | Needs items 14-24 above |
| Technical Annex | v20260702_1155 (STALE) | Rebuild from Architecture Spine |
| Financial Annex workbook | v20260704_1412 (current) | No action unless model changes |
| CFO companion doc | v20260702_1913 (STALE) | Full rebuild against current model |
| Prototype Evidence | NOT STARTED | Build from spine proven/funded split |

---

## RESEARCH — Returned, not yet fully built into materials

| Research file | Items | Used | Unused |
|---|---|---|---|
| Stack economics (24 items) | NVIDIA margins, cloud markup, value extraction, enterprise ROI | Partially (stack layer section built) | TCO comparison, Hugging Face stats, enterprise survey |
| Platform economics (34 items) | Take rates, IP protection, certification, cable precedents | Analysis done in chat | None built into site (founder intent opaque) |
| Ecosystem developers (36 items) | 9 categories of companies | Analysis done in chat | None built into site (conversation material) |
| AI literacy (20 items) | Pew, YouGov, Oxford | 3 field notes built | Oxford dropped, internal calibration items |
| Rate cases (5 items) | VA, OH, GA, PA, national framing | Field note built | All used |
| Field note gaps (9 items) | Various | Most used | Epoch AI URL, Blackwell CC paper verification |
| Power research (4 items) | Grid, PJM, FERC, nuclear | All used | All used |

---

## ECOSYSTEM / DEVELOPER ANALYSIS — For conversations only

Not for the site. Ready for whiteboard in meetings.

| Category | Key companies | HIP unlock |
|---|---|---|
| Family coordination | Cozi, Maple, FamilyWall | Identity + context kernels |
| Eldercare | Honor, Papa, CareLinx | Context + institutional integration |
| Health data | Human API, 1upHealth, Particle | Trust + institutional integration |
| Household finance | Monarch, Copilot, YNAB, Plaid | Context + trust |
| Home automation | Home Assistant, SmartThings | Identity + inference |
| Family safety | Life360, Bark | Identity + context |
| Education | Khan Academy, Duolingo | Identity + inference (age-appropriate) |
| Insurance | Policygenius, Lemonade, Hippo | Institutional integration |
| Robotics adjacency | Wetour Robotics (Orchestra) | Identity + context + trust + governance |

---

## PLATFORM ECONOMICS — For conversations only

Not published. Ready for whiteboard.

- Recommended take rate: 12-20%, anchor at 15%
- IP protection model: API boundary (Stripe pattern) + no source access (Apple pattern)
- Certification inheritance: platform holds SOC 2/HIPAA/NYDFS, apps inherit
- Comparable platforms: Salesforce AppExchange, Roku, Epic EHR, Plaid
- Cable X1 failure modes: closed SDK, CPE-dependent, slow approval. HIP avoids all three.

---

## VIDEO — Staged, not started

Shot list at HIP_Video_ShotList__v20260702_1706.md. 45 seconds, 6 acts.
Intel/NASDAQ 1990s pace reference. Pixabay for stock footage.

---

## PIPELINE (how to not forget)

1. Start every session: "Read HIP_Pending_Queue" from Drive
2. New information arrives: analyze, add to queue with status
3. Build session: pull from queue, build, mark done, update queue
4. End every session: update queue file, upload to Drive
5. One canonical version of each document. Never branch.

---

## Edit history

**v20260707_2230 (initial)**
- Full inventory of all pending items across site, WP, NDA, research, ecosystem, platform, video
- CC merge verification flagged
- Pipeline established

---

## UPDATE v20260708

### Added: Lead paragraph rewrite (index.html + overview.html)

New opening copy, approved. Replaces current lead on both pages:

"The modern home is connected, but it does not have memory.

AI is being built for the individual. One person, one inbox, one assistant, one private context. The enterprise version is bigger. The consumer version is smaller. Neither understands the home, because the home does not work that way. A household is not just an individual. It is a living system of people, roles, obligations, decisions, permissions, and history. For a single person, that system is simple. For a family, it is not. In both cases, the intelligence layer that holds it does not exist.

That is why the home matters. Every person carries their own memory: their medications, their finances, their preferences, their commitments. But the hardest decisions in daily life are not contained inside one person's context. They are shared: how to care for an aging parent, how to manage money, what was decided last month and whether it still holds. These decisions happen across people and across time. They require memory that is both personal and shared, with authority, trust, and continuity across both.

The foundation is not another chatbot, speaker, or app. It is a household intelligence layer: identity for every person who lives there, personal context each member owns, shared context the household builds together, permissions that reflect real relationships, and a trust model strong enough for the most private parts of life.

That layer does not exist yet."

Status: APPROVED. Apply to index.html and overview.html on next site deploy.

### Added: CSS bug for CC

The lead paragraph section on the current live site has a right border/margin that is shorter than the rest of the page paragraphs. Visible on overview.html. CC to investigate and fix. Likely a max-width or padding issue on the section container.

### Added: Multimodal interface challenge

Queue for future content development (not the lead paragraph). The challenge of modal communication in the home: voice-first, hands occupied, no screen, interrupted, multimodal. Architecturally different from enterprise AI. Consider for architecture.html or a new section. Research the Wetour Robotics / Spatial Intent Fusion angle as supporting evidence.
