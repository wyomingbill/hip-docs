Part VI: Where Compute Must Live
The third market force is physical. Having established that the model is commoditizing and that owning the contested silicon is getting more expensive, the remaining question is where the compute that serves households will actually sit. The answer is not a free choice. It is constrained by two hard physical limits that the market is currently discovering the expensive way, and both limits point at the same kind of location: secured, powered, and close to the home. This section traces the fragmentation of compute out of centralized datacenters, establishes the two limits with sourced evidence, and shows why they converge on the operator edge.
Centralized compute is constrained, so it is fragmenting outward
The starting condition is scarcity. As Part V established, building new centralized capacity is expensive on both the silicon and the physical-infrastructure side, and the physical side is structurally inflationary. A single gigawatt of datacenter runs on the order of $60 billion all-in, and the power, cooling, and shell portion is rising because turbines, transformers, and skilled labor are themselves in shortage. Centralized capacity cannot be built fast enough or cheaply enough to meet demand.

The market's response is to push compute out of the hyperscale campus into every available form and location. The fragmentation is real and well-funded, and it takes several shapes.

The modular and containerized build-out is the most mature. Companies assemble prefabricated compute in factories and drop it onto powered sites, compressing build timelines. Crusoe is the clearest case, with contracted power measured in gigawatts and a modular AI-factory product, and it sits inside a supply chain of established hardware and infrastructure vendors, Dell, Vertiv, Schneider, and others, building containerized and prefabricated capacity. This is not speculative. It is shipping.

The large non-hyperscaler builders are real and at scale. CoreWeave operates more than a gigawatt of active power against a revenue backlog approaching $100 billion, and a tier of neoclouds, Crusoe, Nebius, Lambda, Together, Fireworks, and others, has emerged specifically to supply AI compute outside the hyperscalers. The demand is deep enough to fund an entire new category of infrastructure company.

The decentralized and tokenized networks are the most speculative tier, and they should be read with skepticism. Networks such as Bittensor and its subnets, Akash, io.net, and others assemble compute permissionlessly, often from idle GPUs, frequently with a crypto token attached. Some of this is operational: one decentralized marketplace serves a meaningful volume of inference traffic. But most of the category is permissioned, small-scale, or prototype-stage, and the token-attached capacity claims should be treated as unproven at scale. These networks are evidence of how hungry the market is for distributed compute, not evidence that any of them is a serious platform today.

The exotic answers exist but are early. The Tesla Megapod, often cited as a deployed modular product, is in fact an intent-to-use trademark filed in June 2026 with no shipped product and no announced timeline, and the related concepts of compute at charging stations or in home battery units are speculation rather than plans. Datacenter-in-space is genuinely under development, a single experimental satellite carrying an AI accelerator has launched, and major research efforts target orbital compute demonstrations in the coming years, but it is prototype-stage and should be presented as such. These belong in the picture as evidence of how intense the pressure to find new compute locations has become, not as available capacity.

The pattern across all of it is unmistakable. Compute is being pushed out of the centralized campus toward the edge, by economic necessity. The categories sort cleanly by what they are good at, how far along they are, and, critically, whether they can sit close to the home and meet the security bar that sensitive household data requires.

Category
Example players
Status
Close to home
Secured to standard
Fit for household inference
Hyperscalers
AWS, Azure, GCP
Shipping
No
Yes
Poor (far, costly)
Neoclouds
CoreWeave, Crusoe, Lambda, Nebius
Real at scale
No
Yes
Poor (far)
Modular / containerized
Crusoe modular, Dell, Vertiv
Shipping
Sometimes
Yes
Partial
Decentralized / tokenized
Bittensor, Akash, io.net
Mostly unproven at scale
Variable
No
Poor (security)
Exotic edge
Megapod (trademark only), Powerwall / charger concepts
Speculative
Yes
No
Poor (security)
Orbital
Starcloud, Project Suncatcher
Prototype
No (farthest)
n/a
Not yet
Cable operator edge
Comcast, Charter, Cox facilities
Field trials live
Yes
Yes
Strong

Status and placement per the distributed-compute and shell-space verification. Cable facility specifics are documented in Part VII.

But where compute can actually land is governed by two physical limits, and the table's last two columns are exactly those limits.
The first limit: inference distributes, training mostly does not
The first limit separates the two things AI compute does, and they behave very differently across distance.

Frontier training is extremely sensitive to the distance between nodes. Training a large model means constant, high-bandwidth communication among thousands of accelerators, and that communication degrades sharply when the accelerators are far apart. The crude version of this claim, that training collapses past a couple of kilometers, is too strong and a technical reader would correct it. The accurate version is more interesting. Dense frontier training strongly prefers tightly coupled, colocated clusters, but a wave of low-communication training methods is relaxing the constraint: NVIDIA's own benchmarking shows high scaling efficiency across two datacenters roughly a thousand kilometers apart, and research methods such as DiLoCo and DisTrO cut inter-node communication by orders of magnitude, with at least one model trained across three continents at high utilization. The honest framing is that training is far more latency-sensitive than inference, though new methods are beginning to loosen that. It is not a domain HIP needs to win.

Inference distributes far better, and that is the half that matters for households. Serving a model to answer a query does not require thousands of accelerators in constant communication. It requires a copy of the model running near the user. Replicated inference close to where people are is not only feasible, it is the architecture the edge-AI industry is actively building, and the lower latency near the user is a feature rather than a compromise. Household AI is an inference workload, not a training workload. It lives squarely on the side of the limit that distributes well.

This is the first reason compute for households moves to the edge: the thing households need, inference, is exactly the thing that tolerates being distributed close to them.
The second limit: physical security gates the location
The second limit is the one the market keeps rediscovering, and it is the decisive one. Compute cannot live just anywhere, because the data it processes has to be physically protected.

The security requirements for handling sensitive data are not informal. They are codified. Federal standards such as NIST SP 800-53 specify physical access authorization and control for systems handling protected information, and datacenter security practice, documented by the hyperscalers themselves and by facility-standards bodies, includes access authorization, monitored entry, and controlled physical perimeters. A facility that processes a household's health, financial, and personal data has to meet these requirements, or the regulated institutions whose data is involved will not participate and the privacy guarantee is hollow.

This is why the exotic edge locations fail for this workload. A compute cabinet at a charging station, a battery unit in a home, a node recruited permissionlessly from an idle gaming machine, none of these meets the physical-security bar for sensitive household data. They may be fine for rendering, for non-sensitive batch work, for workloads where the data does not matter. They are not fine for the interior life of a family. The physical-security limit does not make distributed compute impossible. It restricts sensitive distributed compute to secured, monitored, access-controlled facilities. That restriction is the whole game.
The two limits converge on one kind of place
Put the two limits together. Household AI is inference, so it distributes well and wants to be close to the home for latency. And it processes the most sensitive data a person has, so it must run in a physically secured, access-controlled facility. The winning location for household inference is therefore a place that is simultaneously close to the home, already powered, and secured to the standard that sensitive data requires.

[Diagram 7: AI Compute Builder Positioning Map. A 2x2 plotting every category of AI compute builder against the two limits: distance from the home (horizontal) and physical security to the sensitive-data standard (vertical). Hyperscalers and neoclouds sit secure but far. Decentralized and exotic-edge options sit close or cheap but insecure. Orbital sits far and prototype. The top-right quadrant, secure and close to the home, is empty except for one occupant: the cable operator edge. The empty quadrant is the argument. See diagram spec tracker for full build spec.]

That is a precise description, and it eliminates almost every option the market is currently chasing. Centralized hyperscale campuses are secure and powered but far from the home and expensive to build. Charging stations and home nodes are close but not secure. Permissionless networks are neither secure nor trusted. Orbital compute is years away and unproven. The one kind of facility that satisfies all three conditions at once, close to the home, already powered, and already secured, is not a new build at all. It already exists, in the thousands, owned by the cable operator.

The market has mapped this problem precisely and keeps arriving at the edge of the answer without naming it. Compute must distribute because the center cannot hold the load. Inference is the part that distributes. Security is the gate that decides where it can land. The facility that clears the gate and sits closest to the household is the operator's own. The next section shows that this is not a hopeful analogy. Cable owns exactly these facilities, in verified numbers, with verified power and security, and the operators and their silicon partner have already begun deploying inference into them.


Sources
	•	Orennia, "What It Costs to Build a 1 GW Data Center," May 2026, for the all-in cost stack and structural inflation of physical infrastructure.

	•	Crusoe newsroom and disclosures on contracted power and modular AI-factory product; trade reporting on the modular supply chain (Dell, Vertiv, Schneider, and others).

	•	CoreWeave Q1 2026 results (active power above 1 GW; revenue backlog approaching $100 billion); reporting on the neocloud category (Crusoe, Nebius, Lambda, Together, Fireworks).

	•	Galaxy Research and trade coverage of decentralized compute networks (Bittensor, Akash, io.net); decentralized inference volume via OpenRouter; skeptical assessments of decentralized-network scale and maturity.

	•	Trademarkia and Data Center Dynamics on the Tesla "Megapod" intent-to-use trademark filing (June 2026, not in commerce); reporting that Supercharger and Powerwall compute concepts are unconfirmed.

	•	Starcloud experimental AI satellite; Google Project Suncatcher and other orbital-compute research and demonstration plans.

	•	NVIDIA NeMo benchmarking on multi-datacenter training scaling efficiency; DiLoCo and DisTrO low-communication training methods; INTELLECT-1 cross-continent training.

	•	Akamai, Equinix, and operator materials on distributed and edge inference; the Comcast and NVIDIA edge-inference field trial.

	•	NIST SP 800-53 physical access controls (PE-2, PE-3); hyperscaler datacenter physical-security documentation; Uptime Institute facility security guidance.

