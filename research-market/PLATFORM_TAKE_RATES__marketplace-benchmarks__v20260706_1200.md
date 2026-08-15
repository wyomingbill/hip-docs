# PLATFORM_TAKE_RATES
Status: BUILT
Reconciled-Against: HIP financial model (marketplace take-rate section), 2026-07-06

Completed platform take-rate and developer-IP research across every major platform model.
Empirical anchor for HIP's 17.5% mode take rate. Sources current to mid-2026.

Format per item: primary source, key data point, confirming source, caveat.

---

## 1. Apple App Store take rate
- **Primary source:** Apple, "App Store Small Business Program," current developer documentation.
- **Key data point:** Standard commission 30%; 15% for Small Business Program developers earning up to $1M/yr. App Store ecosystem facilitated over $1.4T in developer billings and sales in 2025; over 90% of billings and sales paid no commission to Apple.
- **Confirming source:** TechCrunch, "Apple touts $1.4 trillion in App Store billings and sales, 90% without a commission," June 4, 2026.
- **Caveat:** Apple does not disclose App Store commission revenue or exact blended take rate. Effective take rate on total facilitated ecosystem sales is far below 15% because most physical goods, services, and ad transactions are commission-free.

## 2. Google Play Store take rate
- **Primary source:** Google Play Console Help, "Service fees," current developer documentation.
- **Key data point:** 15% on first $1M in annual developer earnings; 30% above $1M. Subscriptions generally 15%. Updated "Apps & Games" terms in 2026 introduced additional lower-fee structures.
- **Confirming source:** TechCrunch, "Google Play drops commissions to 15% from 30% following Apple's move," March 16, 2021.
- **Caveat:** Alphabet does not disclose Google Play commission revenue or blended effective take rate.

## 3. Salesforce AppExchange take rate
- **Primary source:** Salesforce Developer Docs, "How Is Revenue Shared in AppExchange Checkout?"
- **Key data point:** 15% for bank-transfer purchases; 15% + $0.30/transaction for credit-card purchases. Security review fee $999/attempt.
- **Confirming source:** Salesforce/IDC Salesforce Economy study press release, September 20, 2021.
- **Caveat:** AppExchange-specific transaction volume and Salesforce's exact AppExchange take-rate revenue are not publicly disclosed.

## 4. Shopify App Store take rate
- **Primary source:** Shopify Developer Docs, "Revenue share for Shopify App Store developers."
- **Key data point:** Developers keep 100% of first $1M lifetime gross app revenue; 85% above that (Shopify retains 15%). April 2025: annual reset sunsetted, moved to $1M lifetime exemption.
- **Confirming source:** Business Insider, "Shopify rolled back a lifeline it extended to app developers during the pandemic," April 2025.
- **Caveat:** Shopify does not disclose App Store commission revenue separately. 2025 change is less generous for developers who repeatedly stayed below the annual cap.

## 5. AWS Marketplace take rate
- **Primary source:** AWS Marketplace Seller Guide, "Understanding listing fees for AWS Marketplace sellers."
- **Key data point:** Public SaaS subscriptions and AWS Data Exchange: 3%. Private offers tiered: 3% below $1M TCV, 2% from $1M to under $10M, 1.5% at $10M+; renewals 1.5%.
- **Confirming source:** AWSInsider, "AWS Marketplace Tweaks," January 23, 2024.
- **Caveat:** Co-sell credits, private offers, and enterprise discount programs can materially alter net economics. AWS's published take rate is much lower than consumer app stores because enterprise SaaS vendors bring their own sales motion.

## 6. Stripe platform economics
- **Primary source:** Stripe, "Stripe Connect pricing," current documentation.
- **Key data point:** Stripe Connect does not impose a fixed platform take rate. Platform sets its own application fee on top of Stripe's fees. Three-party split: customer payment → platform fee → developer/vendor payout → infrastructure fee.
- **Confirming source:** Stripe, "Platform pricing tool," current documentation.
- **Caveat:** Stripe is a payment and financial-infrastructure platform, not a pure app marketplace.

## 7. Epic Games Store take rate
- **Primary source:** Epic Games Store, "Revenue Share," current distribution documentation.
- **Key data point:** Standard revenue share 88% developer / 12% Epic. Starting June 2025, developers keep 100% of first $1M annual net revenue per product before reverting to 88/12.
- **Confirming source:** The Verge, "Epic is offering developers an alternative to Apple's in-app purchases," May 2025.
- **Caveat:** Low take rate attracted attention but secondary coverage indicates user and revenue impact has been mixed. Low take rate alone does not overcome weaker distribution.

## 8. Roku Channel Store take rate
- **Primary source:** Roku Developer Docs, "Monetization," current documentation.
- **Key data point:** Transactional apps: app receives 80%, Roku retains 20%. Ad-supported apps: Roku routes 30% of ad inventory to Roku fill, or app uses Roku revenue-share ad tag.
- **Confirming source:** Roku 2025 10-K, platform revenue description, filed 2026.
- **Caveat:** Closest cable-like analog; many large content deals are negotiated privately and do not follow default developer terms.

## 9. Xbox / PlayStation store take rates
- **Primary source:** Reuters, "Sony facing $7.9 billion mass lawsuit over PlayStation Store prices," November 21, 2023.
- **Key data point:** Console digital stores generally retain ~30% of digital-game and add-on sales. Microsoft reduced PC game store cut to 12%; console stores remain at traditional 70/30.
- **Confirming source:** International Journal of Research in Marketing, "The rise of the subscription model in the video game console industry," 2025.
- **Caveat:** Sony and Microsoft do not provide a simple public pricing sheet. Console take rates often inferred from litigation, developer agreements, and industry reporting.

## 10. Aggregate take-rate analysis
- **Primary source:** Raj Pabari et al., "A shared-revenue Bertrand game," arXiv, February 11, 2025.
- **Key data point:** Revenue-sharing outcomes depend on the platform's cost structure and the seller's outside option. A high take rate is sustainable only if the platform provides distribution, trust, certification, identity, context, or data access that developers cannot replicate cheaply.
- **Confirming source:** Robin S. Lee, "Vertical Integration and Exclusivity in Platform and Two-Sided Markets," American Economic Review, 2013.
- **Caveat:** No recent McKinsey or a16z cross-industry table found. Empirical pattern holds: stronger distribution monopoly and higher switching costs support higher take rates.

---

## Developer IP protection

### 11. Apple HealthKit / ResearchKit certification
- **Key data point:** Apple requires HealthKit use to be for health or fitness purposes; permissioned by the user, privacy-sensitive local health data access. No HIPAA-like certification cost or timeline published.
- **Caveat:** HIP analogy is controlled API access + strict user-permission and data-use rules, not certification inheritance.

### 12. Salesforce managed package IP protection
- **Key data point:** Managed packages hide protected Apex code and some metadata to protect ISV IP after installation in customer orgs.
- **Caveat:** Fields, objects, flows, configuration, and runtime behavior can still reveal implementation patterns. Protects code better than business logic.

### 13. AWS SaaS Marketplace IP protection
- **Key data point:** SaaS sellers must disclose data handling practices. SaaS products generally protect source code because execution remains in the seller's environment. AWS sees marketplace transaction metadata but does not automatically control the ISV's SaaS application data plane.

### 14. API-mediated platforms and IP boundaries
- **Key data point:** API boundaries protect code but not dependency risk. If HIP exposes identity, context, trust, inference, and integration kernels, developers own app logic but HIP controls the most valuable substrate.

### 15. Developer trust as platform growth driver
- **Key data point:** Developer trust problems show up economically through litigation, platform avoidance, reduced investment, and demands for alternative payment routes. App-store fee disputes, opaque review processes, and API-policy changes all create developer ecosystem risk.

---

## Certification costs (for HIP certification-inheritance model)

### 16. HIPAA compliance cost
- **Key data point:** Credible estimates cluster around $25K–$70K for initial HIPAA program (gap assessment, pen testing, policy work, tooling, internal labor). No single government-issued HIPAA certificate exists.
- **Caveat:** Vendor and consultant estimates, not audited market averages.

### 17. SOC 2 Type II cost and timeline
- **Key data point:** Audit fees roughly $7K–$50K; all-in startup spend often $20K–$80K+. Type II requires 3–12 month observation period.
- **Caveat:** SOC 2 is an auditor's attestation report, not a certification in the strict legal sense.

### 18. Certification inheritance (AWS Shared Responsibility Model)
- **Key data point:** HIP platform could reduce developer burden by inheriting infrastructure, logging, key management, audit, identity, and policy controls. Application logic, user consent, data minimization, and misuse risk remain with the app developer.

---

## Platform analog research (cable/telecom)

### 19. Comcast X1 app platform
- **Key data point:** X1 exposes platform features to approved partners including whole-home sign-in. Not a general-purpose open app store. No standard developer take rate publicly disclosed.

### 20. Cable operator app store attempts
- **Key data point:** Dominant pattern was curated operator-controlled app bundles, not broad third-party developer ecosystems. Failure modes: limited hardware, slow UX, closed approval, rights restrictions, later displacement by Roku/Apple TV/Fire TV/smart TV OS.

### 21. Telecom API platforms (CPaaS)
- **Key data point:** Twilio FY2025 revenue $5.07B (+14%); Bandwidth Q1 2026 revenue $209M (+20%). CPaaS providers monetize via usage fees, not marketplace take rates.

### 22. NVIDIA Omniverse / NGC
- **Key data point:** NGC provides GPU-optimized containers, pretrained models, SDKs, Helm charts. No public NVIDIA marketplace take rate found.

---

## Platform revenue scale

### 23. Apple Services revenue
- **Key data point:** Apple Q2 FY2026: total revenue $111.2B, Services ~$31B (~28% of quarterly revenue). App Store not broken out inside Services.

### 24. Salesforce AppExchange ecosystem
- **Key data point:** IDC projected Salesforce ecosystem to create $1.6T in new business revenue by 2026; partners make $6.19 per $1 Salesforce makes by 2026.

### 25. AWS Marketplace transaction volume
- **Key data point:** Canalys estimated enterprise software sales through hyperscaler cloud marketplaces to reach $85B by 2028 (up from $16B in 2023).

### 26. Shopify developer ecosystem
- **Key data point:** Shopify paid out more than $1.3B to developers across its ecosystem in the prior year. Current model: 0% on first $1M lifetime, 15% above.

---

## Regulated vertical platform analogs

### 27. Epic EHR app marketplace
- **Key data point:** Epic Showroom allows vendors with Epic connection to list apps. No standard App Orchard/Showroom take rate publicly disclosed. Regulated integration marketplace, not transparent revenue-share marketplace.

### 28. Plaid (regulated-data platform)
- **Key data point:** 1 in 2 banked U.S. adults use Plaid; 12,000 financial institutions, 20 countries, 1M+ daily connections. Pricing contract-based, not publicly disclosed.

### 29. Open Banking (UK/EU)
- **Key data point:** FCA: open banking payments up 53% YoY in 2025. Mandated access regime, not a proprietary platform take-rate business.

### 30. FDA digital health / SaMD pathway
- **Key data point:** FDA FY2026 establishment registration fee $11,423. Total SaMD clearance cost (consultants, QMS, cybersecurity, clinical validation) far exceeds FDA user fee alone.

### 31. Insurance API platforms
- **Key data point:** Guidewire FY2025 revenue $1.2025B (+23%), subscription/support $731.3M (+33%). No public take-rate or marketplace-fee schedules found for Guidewire, Majesco, or Duck Creek.

---

## MODEL IMPLICATION
HIP's 17.5% mode take rate sits empirically between Roku (20%, operator-platform) and
Salesforce/Shopify (15%, governed ISV). Defensible against benchmarks, not a guess.
AWS 3% is the pure-infra floor; Apple/console 30% is the ceiling HIP undercuts deliberately.
