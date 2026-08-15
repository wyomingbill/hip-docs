# MARKET_RESEARCH: Household Trust-Circle Segment Sizing (Verified Deep-Research Run)
Status: BUILT
Reconciled-Against: deep-research workflow run wf_d86f5317-2df, 2026-07-12; 26 sources fetched, 128 claims extracted, 25 adversarially verified (24 confirmed 3-0, 1 refuted 0-3); verifiers independently downloaded and parsed the primary Census/AARP files
Provenance: Claude session deep-research harness (fan-out search, source fetch, 3-vote adversarial verification per claim, synthesis). Companion piece: MARKET_RESEARCH__household-trust-circle-segment-sizing-external__v20260712_1331.md (external analysis, unverified, broader modeled estimates).

Verification flags used throughout:
- **[V]** survived 3-vote adversarial verification against the primary source (verifiers downloaded and parsed the actual Census xls / AARP PDF)
- **[E]** extracted from a primary source by a fetch agent but not adversarially verified (dropped from the verify budget)
- **[D]** derived / analyst estimate; no direct published figure

---

# Headline numbers

**1-2 person households are 63.7% of all US households: 84.2M of 132.2M (2024).** [V] One-person: 38.5M (29.1%). Two-person: 45.7M (34.6%). Preliminary 2025: 86.2M of 134.8M (64.0%), with a Vintage-2025 methodology-break caveat. Source: Census CPS ASEC, Historical Households Table HH-4 (https://www.census.gov/data/tables/time-series/demo/families/households.html). ACS 2023 corroborates independently (28.8% living alone of 131.3M households, table S1101).

**3-4 person households are 27.5% (36.4M).** [V] The target structure outnumbers the "family household" structure 2.3 to 1.

**The strongest-fit dyad pools:** ~29.2M couple-only households (lower bound), ~15.2M households of a 65+ adult living alone, 63M family caregivers of whom ~6.5M are long-distance.

---

# 1. Size distribution, US and international

| Size | US 2024 (CPS) | Share |
|---|---|---|
| 1 person | 38.5M | 29.1% [V] |
| 2 person | 45.7M | 34.6% [V] |
| 1-2 combined | 84.2M | 63.7% [V] |
| 3-4 person | 36.4M | 27.5% [V] |
| 5+ | ~11.7M | ~8.8% [D, residual] |

International (extracted, not adversarially verified; treat as directional): EU-27 2024 is MORE skewed toward small households than the US: 35.2% one-person + 30.2% two-person = **65.4%** 1-2 person (Eurostat ilc_lvph03) [E]. Japan 2023: single-person households are the largest category at **34.0%** (18.5M), with couple-only households second (Nippon.com from MHLW data) [E]. Norway/Sweden approach half of households single-person [E]. The small-trust-circle structure is not a US quirk; it is the developed-world modal household, which matters if the operator thesis extends to European or Japanese telcos.

---

# 2. Dyad segments

| Dyad | Count | % of 132M HH | Status |
|---|---|---|---|
| (a) Couple, no one else in household | **29.2M+** married-couple two-person HH (2023 CPS Table H1); cohabiting couple-only HH add from the 7.6M two-person nonfamily pool, so true total plausibly **32-35M** | 22-26% | [V] for 29.2M floor; [D] for the cohabitor add |
| (b) Couple + one adult child at home | No direct count. Sits inside 19.9M three-person HH. Context: 59.7M people (18%) lived multigenerationally in 2021; 31% of adults 25-29 live in multigen households (Pew) | unmeasured | [E] context; count is an open question |
| (c) Single adult + involved adult child elsewhere | Bounded by: 15.2M 65+ solo households x caregiver involvement rates. See (e) | -- | [D] |
| (d) Individual + caregiver (any) | 63M caregivers, 59M caring for adults (AARP/NAC 2025); 40% co-reside, 35% live within 20 min, ~11% live 1+ hour away (**~6.5M long-distance caregivers** [D from verified 11%]) | -- | [V] rates; [D] count |
| (e) Aging parent alone but monitored | ~3 in 10 adult care recipients in home/community settings live alone (AARP/NAC 2025, caregiver-reported) [V]. Applied to the recipient base: roughly **5-16M households** | 4-12% | [D] range |
| Other: spouse-as-sole-confidant dyads | GSS: share of adults whose ONLY confidant is their spouse nearly doubled 1985 to 2004 (5.0% to 9.2%) | -- | [E] |

Key anchors behind those rows, all [V]: married-couple households overall are 62.3M (47.1%, down from 71% in 1970); householders 65+ living alone are 11.6% of all households (~15.2M derived; ACS B11010 cross-check ~15.8M); 32.2% of all households contain someone 65+ (~42M derived) and 42.1% contain someone 60+ (~55M derived).

---

# 3. Eldercare and remote care

- **65+ living alone:** 15.2M households [V-derived]. Person-level: 26% of 65+ adults lived alone in 2023 (Pew, from ACS microdata), and living alone rises steeply with age: 38% of adults 85+ vs 24% of 65-84 [E].
- **Caregivers:** 63M family caregivers in 2025, 24% of all US adults, up ~45-50% since 2015 (AARP/NAC Caregiving in the US 2025) [V]. Honest caveat, verified: the 2025 wave broadened definitions (~11M paid-via-Medicaid/VA caregivers included), so part of that growth is methodological.
- **Distance:** 40% of caregivers co-reside (up from 34% in 2015), 35% within 20 minutes, 11% an hour or more away [V]. About 3 in 10 adult care recipients live alone [V]: that is the remote-monitoring dyad, directly measured.
- **Sandwich generation:** 23% of all US adults have a 65+ parent plus a dependent child (Pew 2022); 54% of adults in their 40s [E]. Narrow definition (65+ parent AND minor child, actively caregiving): 2.5M [E]. 29% of caregivers self-report as sandwich [V].
- **Trajectory:** 65+ population 58M (2022) to 82M (2050) [E, Census projections]; 85+ nearly doubles to 11.8M by 2035 and 13.7M by 2040 [E, Census P25-1144]; older adults outnumber children by 2034 [E]. The caregiver support ratio (45-64 adults per 80+ adult) falls from 7:1 (2010) to 4:1 (2030) to under 3:1 (2050) [E, AARP PPI]: each remote adult child carries more parents with less sibling backup, which increases per-dyad willingness to pay for coordination tooling. Solo-living growth 2010-2020 was entirely driven by 65+ households (9.4% to 11.1% of all households while under-65 solo declined) [V].

**Refuted claim to avoid:** "54% of 65+ live with a spouse, so ~80% of older adults are in 1-2 person households" failed verification 0-3 (the "lives with a spouse" category does not imply couple-only household). Do not use the ~80% framing in any deliverable.

---

# 4. Multi-principal vs single-principal

No source directly measures this; honest decomposition [D]:

- Structurally multi-person: **~70%** of households (2+ residents); multi-principal governance applies on its face.
- One-person households: 29%, but not all single-principal. Applying the verified caregiver-involvement rates to the 15.2M elderly-solo subset, plus non-elderly solos with involved family: an estimated **8-15M "solo but governed" households** where an outside party needs scoped access. That is exactly the existence-invariance and caregiver-grant machinery, applied across a network boundary rather than a living room.
- Genuinely single-principal (one occupant, no involved other): plausibly **15-22% of households** [D]. The "solo ager" datum: ~1 in 10 adults 50+ has no partner or children at all [E, AARP via NPR]: a real single-principal floor.

So roughly **78-85% of households are multi-principal** once involved outside parties are counted. The single-user framing addresses the minority case.

---

# 5. Trust-circle size

All [E]: extracted from primary academic sources but not in the verified set, and the literature carries a known dispute:

- The canonical GSS "important matters" study (McPherson, Smith-Lovin and Brashears, ASR 2006, https://journals.sagepub.com/doi/10.1177/000312240607100301): mean core discussion network fell from **2.94 confidants (1985) to 2.08 (2004)**; by 2004, 43.6% of adults discussed important matters with at most one person, and ~63% had 0-2 confidants. Known caveats: a 2008 coding erratum and Fischer's 2009 challenge to the zero-confidant level. Use the "about 2, range 2-3" reading, not the isolation-crisis reading.
- Pew 2011 replication: mean 2.16 core ties, stable vs 2008 (1.93).
- Networks became more spouse- and kin-centered: spouse-as-confidant rose 30% to 38% (1985-2004), and adults with any non-kin confidant fell from 80% to 57%. Sensitive sharing has been collapsing INTO the household.
- Dunbar-layer research: the innermost "support clique" is ~5 people, with simulation work showing near-maximal trust (0.97+) required to maintain it.

Direct answer: yes, the data support the design premise. The modal American shares sensitive matters with **1-3 people, increasingly spouse and kin**. The 1-2 primary-party governance model matches the empirically observed trust topology; Dunbar's ~5 support clique is a sensible ceiling for the grant model rather than a target.

---

# 6. Verdict

**Mass market, unambiguously, with one discipline required in how it is claimed.**

- By structure alone: 84M households (64%) are 1-2 person. [V]
- Strong-fit dyads with a clear governance relationship: ~29-35M couple-only + ~15M elderly-solo = **~45-50M households** before any caregiving overlay. [V/D]
- The remote-governance overlay (the eldercare wedge, HIP's sharpest demo): 6.5M long-distance caregivers, ~3-in-10 care recipients living alone, support ratio halving by 2030. This subset alone, **6-16M households**, is bigger than most VC-fundable "mass markets," and it is the fastest-growing household configuration in the country. [V rates, D counts]
- Conservative intersection of "small circle + at least one involved second party": **20-40M US households** [D: flagged, no source measures this intersection directly].

The discipline: the VERIFIED mass-market number is the 64% structural figure; the 20-40M addressable figure is a derivation and should be presented as such in any deliverable.

Strategic note reinforcing the scope decision: the dyad market is not a single-user market. Even the 29% solo households skew toward configurations with an involved outside party. The demand center of gravity is exactly the bounded v1 taxonomy (two adults, or one adult plus one remote caregiver with scoped grants), and the GSS kin-centering trend says trust circles are getting smaller and more household-shaped over time, not larger.

**Gaps that remain open** (nothing survived verification): direct EU/Japan verified comparison; a direct count of couple-plus-adult-child households; Census 2035-2040 household-type (vs population) projections. The trust-circle literature is solid but carries the Fischer dispute; cite it as "about 2 confidants, range 2-3, kin-centered" and it will survive diligence.

---

## Verified sources (24/25 claims confirmed 3-0)

- Census Historical Households Tables HH-1/HH-4: https://www.census.gov/data/tables/time-series/demo/families/households.html
- Census CPS ASEC 2023 Table H1: https://www.census.gov/data/tables/2023/demo/families/cps-2023.html
- ACS 2023 1-year Table S1101: https://data.census.gov/table/ACSST1Y2023.S1101
- Census America Counts, one-person households: https://www.census.gov/library/stories/2023/06/more-than-a-quarter-all-households-have-one-person.html
- Census families press release 2024: https://www.census.gov/newsroom/press-releases/2024/families-living-arrangements.html
- Pew, older adults living alone: https://www.pewresearch.org/short-reads/2025/12/04/a-smaller-share-of-older-us-adults-live-alone-today-than-in-1990/
- AARP/NAC Caregiving in the US 2025: https://www.aarp.org/pri/topics/ltss/family-caregiving/caregiving-in-the-us-2025/ (report PDF: doi 10.26419/ppi.00373.001)

## Extracted-only sources ([E] claims)

- Eurostat household composition: https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Household_composition_statistics and ilc_lvph03
- Japan household data: https://www.nippon.com/en/japan-data/h02059/
- OECD Family Database SF1.1: https://webfs.oecd.org/els-com/Family_Database/SF_1_1_Family_size_and_composition.pdf
- McPherson et al., Social Isolation in America (ASR 2006): https://journals.sagepub.com/doi/10.1177/000312240607100301
- Pew Social Networking and Our Lives (2011): https://www.pewresearch.org/internet/2011/06/16/social-networking-sites-and-our-lives-2/
- Dunbar-layer trust simulation: https://pmc.ncbi.nlm.nih.gov/articles/PMC10559249/
- Pew sandwich generation (2022): https://www.pewresearch.org/short-reads/2022/04/08/more-than-half-of-americans-in-their-40s-are-sandwiched-between-an-aging-parent-and-their-own-children/
- Pew multigenerational households (2022): https://www.pewresearch.org/social-trends/2022/03/24/the-demographics-of-multigenerational-households/
- Sandwich caregivers (NSOC/NHATS): https://pmc.ncbi.nlm.nih.gov/articles/PMC10023280/
- ACL Profile of Older Americans 2023: https://acl.gov/sites/default/files/Profile%20of%20OA/ACL_ProfileOlderAmericans2023_508.pdf
- AARP PPI caregiver support ratio: https://www.aarp.org/content/dam/aarp/research/public_policy_institute/ltc/2013/baby-boom-and-the-growing-care-gap-insight-AARP-ppi-ltc.pdf
- Census P25-1144 Demographic Turning Points: https://www.census.gov/content/dam/Census/library/publications/2020/demo/p25-1144.pdf
- PRB Aging in the US fact sheet: https://www.prb.org/resource/fact-sheet-aging-in-the-united-states/
- NPR solo agers: https://www.npr.org/2026/07/09/nx-s1-5886348/solo-agers-demographics-caregiving-family-aging
