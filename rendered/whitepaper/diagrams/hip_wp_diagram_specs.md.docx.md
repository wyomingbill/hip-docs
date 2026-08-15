HIP White Paper — Diagram & Chart Specification Tracker
Running list of all visuals for the white paper. Each entry gives the spec, the source/reference for any data, and the exact location in the document. Update as sections are drafted. Hand to designer for production. Data charts carry sourced numbers so they cannot be fabricated in production.

Status key: SPEC = specified, not built · BUILT = produced · PLACEHOLDER = referenced in text, awaiting art

Open dependency: the inference cascade (Diagram 1) is currently four-tier (consumer-facing). If the five-tier architecture (edge / mid / core / frontier / web) is adopted for this audience, Diagram 1 expands to five tiers. UNRESOLVED.


Diagram 1 — The Inference Cascade
	•	Location: Part I: HIP, "The inference cascade" section. Currently described in prose only.
	•	Type: Architecture flow diagram.
	•	Status: SPEC.
	•	Intent: Most queries answered privately on-net; progressively more sensitive/demanding queries move outward across a trust boundary; household holds the key throughout.
	•	Form: Horizontal left-to-right flow, four tiers (or five if architecture decision changes), with a clearly marked vertical trust-boundary line.
	•	Content:
	•	Query enters at left.
	•	Tier 1 Primary (household memory): "Answered from household context. Small model on operator infrastructure. Nothing leaves." Annotate "majority of queries."
	•	Tier 2 Freshness (web): "Live data. Only the search string leaves. No identity, no context." Annotate "generic query out, result synthesized locally."
	•	Tier 3 Enclave (confidential compute): "Larger model inside hardware-secured enclave on operator infrastructure. Encrypted in, during, out. Operator cannot read."
	•	Tier 4 Passthrough (frontier): "Subscriber's own frontier model. Household context stripped first. Crossing is announced."
	•	Trust boundary: vertical line. Tiers 1 and 3 inside operator/household perimeter. Tier 2 sends only stripped query across. Tier 4 explicitly crosses.
	•	Persistent household-key marker travels with the household across all tiers.
	•	Data/source: None (architecture, not data).


Diagram 2 — The Moat
	•	Location: Part II: The Moat. Conceptual spine of the document.
	•	Type: Concentric-layer concept diagram.
	•	Status: SPEC.
	•	Intent: Model and router are replaceable commodity outer layer; context, trust, and feedback loop are the defensible compounding core.
	•	Form: Concentric layers, outer to inner.
	•	Content:
	•	Outer ring ("Commodity / replaceable"): "Open model" and "Router / orchestration." Annotate "downloadable, buildable, anyone can match in an afternoon."
	•	Inner core ("Defensible / compounding"), three reinforcing elements:
	•	Context graph: "accumulated household context, built one interaction at a time, cannot be acquired faster than created."
	•	Trust boundary: "household holds the key; the custody model a frontier lab cannot adopt."
	•	Feedback loop: "private improvement against data no competitor can see." Drawn as arrow circling back into the context graph (shows compounding).
	•	Visual point: outer ring is where competitors compete and lose nothing by being copied; core cannot be crossed. Core elements visibly reinforce each other.
	•	Data/source: None (concept).


Chart 3 — Open-vs-Closed Capability Gap Closing
	•	Location: Part IV: Intelligence Commoditizes, "Open intelligence has a track record" section. Currently rendered as a table; chart is optional companion or replacement.
	•	Type: Line chart.
	•	Status: SPEC.
	•	Intent: The model commoditizes on a closing schedule.
	•	Form: x-axis time; y-axis "months leading open model trails leading closed model."
	•	Data (Epoch AI):
	•	Late 2024 ≈ 12 months
	•	Late 2025 ≈ 3 months
	•	Mid 2026 ≈ 4 months
	•	Annotation: Long-arc sharp narrowing; note slight recent uptick (3→4) for honesty.
	•	Source: Epoch AI, open-vs-closed capability gap data insight.


Chart 4 — The Memory Cost Spread
	•	Location: Part V: Owning Compute Gets More Expensive (Pillar Two). NOT YET DRAFTED.
	•	Type: Horizontal bar chart, log scale on cost-per-GB.
	•	Status: SPEC.
	•	Intent: The asset HIP compounds (context) sits on the cheap layer; the contested working-memory layer is 40x+ more expensive per bit.
	•	Data (verified, late June 2026, per GB):
	•	NAND/SSD (finished, 1TB client SSD): ≈ $0.27
	•	Raw TLC NAND: ≈ $0.32
	•	DDR5 UDIMM (commodity DRAM): ≈ $13
	•	DDR5 RDIMM (server DRAM): ≈ $40
	•	HBM: premium tier above DRAM; exact public $/GB not sourceable — render as "premium, not publicly priced," do NOT fabricate a bar.
	•	Annotation: Bracket "~40x to ~148x spread" between DRAM and NAND. Label cheap end "where HIP's compounding context lives," expensive end "the contested layer HIP minimizes."
	•	Source: TrendForce / DRAMeXchange, June 2026.


Chart 5 — The Edge-Hardware Cost Ladder
	•	Location: Part VI (Where Compute Must Live) or Part VII (Cable Owns the Location). NOT YET DRAFTED.
	•	Type: Horizontal bar chart / labeled ladder, log scale on cost.
	•	Status: SPEC.
	•	Intent: Serving small models at the edge is a four-figure hardware proposition, not a $35B-per-gigawatt one.
	•	Data (verified, NVIDIA Marketplace / retail listings):
	•	Hailo AI accelerator kit: $110
	•	Jetson Orin Nano Super: $249
	•	Jetson AGX Thor: $3,499
	•	DGX Spark: $4,699
	•	RTX PRO 6000 Blackwell: $13,250
	•	Optional contrast marker: far right, "1GW datacenter ≈ $60B all-in (Orennia)" to make the scale gap visceral.
	•	Source: NVIDIA Marketplace; Orennia (datacenter cost).


Chart 6 — The Lease-Back Bridge (optional / schematic)
	•	Location: Part VIII: The Economics. NOT YET DRAFTED.
	•	Type: Two-line or stacked-area chart over the bridge period.
	•	Status: SPEC (schematic, not sourced point data).
	•	Intent: GPUs cash-generating from day one; lease revenue declines as HIP penetration grows and reclaims capacity; total utilization stays high while the mix shifts.
	•	Form: x-axis time (bridge years); one band lease revenue (high early, declining); second band HIP consumer revenue (low early, rising); crossover is the story.
	•	Data/source: Illustrative. Label clearly as a schematic of the bridge dynamic, NOT a forecast, unless verified GPU lease rates and a penetration assumption are attached. Underlying rate cards available from leasing-economics verification (neocloud GPU-hour rates, ~$1.69/GPU-hr breakeven, 6-yr depreciation) if a quantified version is wanted.


Candidate / not yet committed
	•	Five-forces-converging visual (Part III): a possible diagram showing the five socio-political forces converging on the household. Lower priority; Part III reads well as prose. Decide later.
	•	Compounding-over-time chart (Part II or "Why Now"): competitor arrives later with equal tech but zero context while HIP's accumulated context has climbed for a year; gap widens. Visualizes the "cannot be acquired faster than built" argument. Could support Diagram 2 or live in Part IX.

