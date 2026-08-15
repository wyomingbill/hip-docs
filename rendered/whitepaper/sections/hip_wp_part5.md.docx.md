Part V: Owning Compute Gets More Expensive
The second market force is economic, and it runs opposite to the assumption most people hold. The intuition is that compute gets cheaper every year, so any compute-dependent business gets easier to run over time. That intuition is wrong for the part of the stack that now governs AI cost. The binding constraint is memory, memory is inflating, the inflation has reached consumers, and the cost of owning the contested layer is rising rather than falling. This section establishes that with sourced figures and then shows why it favors HIP, which is built to need the least of the expensive layer and the most of the cheap one.
Memory, not compute, is the bottleneck
The scarce input in the AI build-out is not raw processing. It is memory capacity and bandwidth, and the spending reflects it. Memory has gone from a minor line in hyperscaler capital budgets to a dominant one in three years.

Year
Memory as share of hyperscaler capex
2023
~8%
2026
~30%
2027
higher (projected)

Per SemiAnalysis, corroborated by Tom's Hardware. The 2027 figure is a projection of further increase, not a fixed number.

The most contested form of memory is High Bandwidth Memory, the stacked DRAM that sits beside AI accelerators and gates their performance. It is made by a very small number of suppliers, which is the structural reason the shortage does not resolve quickly.

HBM supplier
Approximate share (2025)
SK Hynix
61%
Micron
21%
Samsung
17%

Per Reuters. The market is dominated by three suppliers; this concentration is what makes supply slow to expand.

New fabrication capacity for this class of memory takes years to bring online, and the one large new entrant scaling commodity DRAM, China's CXMT, does not produce datacenter-grade HBM. The constraint is therefore not a transient spike. It is a structural feature of a concentrated, capital-intensive, slow-to-expand supply base meeting demand that is still climbing.
The shortage has reached the consumer, which proves it is real
The clearest evidence that this is a genuine economic force, not an industry talking point, is that the cost has reached ordinary consumer hardware, and the manufacturers are naming the cause.

Product
Price action (2026)
Attribution
Apple Mac / iPad
+16.7% to +25%
AI datacenter memory demand, cited by Apple
Microsoft Xbox
+$150
Memory and component costs
Dell PCs
+15% to +20%
Memory cost pressure

Per Reuters and corroborating trade reporting, June 2026. Console bills of materials are now estimated at more than one-third memory cost.

This matters for two reasons. First, it confirms the shortage is severe enough to override the normal downward trend in consumer electronics pricing, which is a high bar. Second, it undercuts the one alternative to a platform like HIP that a skeptic would raise: the idea that households will simply run AI locally on their own hardware. The local-inference path is getting more expensive, not cheaper, because the same memory the datacenters are absorbing is the memory a powerful home machine needs. The do-it-yourself alternative to HIP is being priced out by the same force that is repricing everything else.
Micron's position shows the shortage is locked in
Micron's most recent results illustrate how durable the repricing is. The company is not merely selling more memory at higher prices in a spot market that could reverse next quarter. It has locked in volume and floor pricing through long-term structured agreements.

Micron, Q3 FY2026
Figure
Revenue
$41.46B
Year-over-year growth
+346%
Forward guidance
~$50B
Gross margin
~86%
Structured agreements (SCAs)
Take-or-pay, floor pricing above prior-cycle peak, covering ~20% of DRAM and ~one-third of NAND volume

Per Micron earnings materials. The agreements are Strategic Customer Agreements (SCAs), take-or-pay contracts with floors set above the previous cycle's peak margins.

The significance of the SCA structure is that it converts a cyclical commodity into a contracted one. Floor pricing set above prior-peak margins means the buyers, the hyperscalers, have agreed that this memory will not get cheap again on the timeline that matters. The shortage is not a moment. It has been written into multi-year contracts.
The cost curves diverge by workload, and HIP sits on the cheap side
Here is the structural point that turns the whole force in HIP's favor. Memory is not one thing. The hierarchy splits sharply by cost per bit, and the layers are diverging because the demand is concentrated on the expensive end.

Layer
Approximate cost per GB (June 2026)
Role
HBM
Premium tier, not publicly priced
Frontier training and high-end inference
DDR5 RDIMM (server DRAM)
~$40
Datacenter working memory
DDR5 UDIMM (commodity DRAM)
~$13
Consumer and edge working memory
NAND / SSD (1TB client)
~$0.27 to $0.32
Persistent storage

Per TrendForce / DRAMeXchange, June 2026. HBM commands a premium above DRAM, but an exact public per-GB figure is not available, so it is not stated as a number. The spread between server DRAM and NAND is roughly 40x to 148x per bit.

This divergence is the architecture of the opportunity. Active inference is bound by the contested, inflating, fastest-appreciating layer: HBM and high-end DRAM bandwidth. The thing that compounds in value over time, the household context graph, is small, written occasionally, and lives on the cheapest and most abundant layer, NAND. HIP is therefore structurally light on the expensive layer and heavy on the cheap one.

The cleanest form of the argument is about the scarcest component specifically. HBM is the single most supply-constrained part in the AI economy, made by three companies, sold under take-or-pay floors, projected to climb further. A datacenter doing frontier inference is buying exactly that component. HIP's edge tier does not need it. The edge tier runs small, quantized models that fit in commodity memory or unified memory, with no HBM stack required. So while the rest of the industry competes for the one component that is hardest to get and fastest to appreciate, HIP sidesteps it by construction.

One discipline belongs in the record. The strong claim is about levels, not trajectory. Storage is dramatically cheaper per bit than working memory, a structural 40x-plus gap that holds today. It would be convenient to claim the spread is also widening in HIP's favor, but the near-term data does not support that: NAND contract prices are projected to rise faster than commodity DRAM in the immediate term, and HBM profitability has at points fallen below high-capacity DDR5. The memory crunch is not sparing the cheap layer. The honest and still-decisive claim is the one about position: HIP minimizes its exposure to the scarcest, most expensive, most contracted component, and places its compounding asset on the cheapest available layer, regardless of how the layers move quarter to quarter.
The operator edge avoids the other inflating cost
There is a second inflating cost beyond the silicon, and the operator sidesteps it too. Building new datacenter capacity is not only a silicon problem. It is a power and cooling problem, and that half of the cost is structurally inflationary because it is driven by turbines, transformers, and labor that are themselves in shortage.

1GW datacenter, all-in
Approximate cost
Total
~$60B
IT hardware
70% ($41B)
Physical infrastructure (power, cooling, shell)
30% ($19B)

Per Orennia, May 2026, which states that costs are rising further due to demand for turbines, transformers, chips, and labor. Note: the figure sometimes quoted as "$35B silicon plus $25B power and cooling" traces to investor commentary, not an engineering source, and is not used here.

HIP does not build a gigawatt of new capacity. It runs on the operator's existing, already-powered, already-built facilities. The physical-infrastructure cost that inflates fastest in a greenfield build is a cost the operator largely already paid, years ago, for other reasons. HIP's incremental footprint is small hardware in space that is already powered and cooled to the level its low-density inference requires. The cost that is repricing the whole industry upward is the cost HIP and the operator are most insulated from.
The turn
Put the pieces together. The binding resource in AI is memory, memory is inflating, the inflation is contracted in for years and has reached the consumer, and the cost of building new capacity is rising on both the silicon and the power side. Every one of those facts raises the cost of owning AI compute the conventional way.

HIP is built to be on the favorable side of each. It needs the least of the scarcest and most expensive component, because its edge tier runs small models that do not require HBM. It places its compounding asset on the cheapest layer in the hierarchy. And it rides the operator's already-built, already-powered facilities rather than financing new ones into an inflating market. As the cost of owning compute rises for everyone building the conventional way, the platform that minimizes exposure to every inflating layer is the one whose unit economics hold. The model commoditizes, and now the compute around it gets more expensive, and both forces push the durable advantage toward the same place: the platform that needs little of the costly silicon, owns the cheap storage where context lives, and runs on real estate that is already powered. That place is the operator edge, and the next sections show why compute must live there and why cable already owns it.


Sources

