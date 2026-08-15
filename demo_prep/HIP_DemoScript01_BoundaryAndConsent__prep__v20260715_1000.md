# Script 01: Boundary and consent

`boundary_and_consent__v20260715_1000.json`
Version: v20260715_1000 MT
Supersedes: `HIP_DemoScript01_BoundaryAndConsent__prep__v20260715_0900.md`
Speaker: Maya, all five turns.

---

# USE CASE

One person, five questions, each one needing more than the last. The first three are answered inside the house. The fourth cannot be, and it stops at the boundary and asks.

---

# PROBLEM

Every household assistant on the market sends every question to a frontier model. "When's trash pickup" gets answered by the largest model ever built.

Enterprise has a name for this. The lazy tax. You pay frontier rates for lookup work because routing is harder than not routing. It's the biggest number on the page with the weakest defense behind it, and enterprises are looking now.

Consumers don't call it anything, because nobody sees the bill. It isn't free. It's subsidized. A lab is buying adoption and eating the difference.

Bet on two things. Enterprises will engineer the tax out. And the labs will end the consumer subsidy, one way or another.

"One way or another" is the operator's problem. If it ends in price, your COGS gets set by a vendor's decision you don't control. If it ends in ads, every question asked inside the home becomes ad inventory, and you're the one who put the device there.

The cascade is not a feature. It's the hedge.

---

# VOICEOVER

Read before pressing LOAD.

> "Five questions from one person, getting harder as they go. Watch the routing pane and nothing else.
>
> Every assistant on the market today sends all five of these to a frontier model. Enterprise calls that the lazy tax. Consumers don't call it anything, because a lab is paying it for them. For now.
>
> Watch where each of these actually runs. Then watch the fourth one, because that one leaves your network, and before it does, it stops and asks."

---

# TURNS

| # | Query (Maya) | Bloom | Tier | Facts pulled |
|---|---|---|---|---|
| T01 | "When's trash pickup?" | 1 Remember | EDGE | D7 |
| T02 | "Can I schedule the plumber for 8am Tuesday?" | 3 Apply | EDGE to MID | D3 |
| T03 | "What's the best morning to take the car in?" | 5 Evaluate | EDGE to MID to CORE | D1, D3, D7 |
| T04 | "What are the setback rules for zoning at my house, and what do I have to do to get a variance?" | n/a | GATE, then FRONTIER | D10, D11 |
| T05 | (disposition) | 1 | EDGE | new row |

**Why Maya speaks.** T03 needs D1, which is `maya to maya`. Sam cannot see it and asking as Sam fires INJ-7 in the middle of a routing demo. Maya can see D1, D3, D7, and the household rows. Nothing cross-member fires. Script 01 stays about routing and nothing else.

**No query asserts a fact.** Every turn is a question with nothing in it. If the speaker supplies the facts, the graph contributed nothing and the escalation is theater. This is also why no turn mentions Dad, the fall, or the medication. That material is script 03's and it drags the rungs into a script that is not about rungs.

---

# THE LINE THAT SEPARATES INSIDE FROM OUTSIDE

T01 through T03 are answered from the household's own facts. T04 is a question about the world. Lakewood municipal code is not in the graph and never will be.

The boundary is not a difficulty threshold. It is a knowledge boundary. Inside, your facts. Outside, the world's facts.

This is what kills "prove your 70B can't do that." The 70B genuinely cannot. It does not know Jefferson County setbacks, and it should not pretend to.

---

# T04 IN DETAIL

The turn the whole script exists for.

1. HIP does not call out. It stops.
2. It builds the outbound payload from the fact rows, by code, never composed by a model.
3. Every clause cites its `fact_id` and its rung. No fact_id, no exit.
4. Maya approves. FRONTIER lights. The call goes.

```
OUTBOUND, pending approval
  address       [REDACTED-HOME-ADDRESS]
                D10  CONFIRMED  household
  zone_district [pull from city map, TBD]
                D11  CONFIRMED  household
  [owner]       redacted
  [members]     redacted
```

**You cannot anonymize a zoning question.** The address has to go or there is no answer. So the beat is not "watch it strip the identifying data." It is: **the question goes, the questioner doesn't.** The lab learns someone wants setback rules for that lot. It learns nothing about who lives there, how many of them, or anything else in the graph.

That is a stronger claim than redaction because it is honest about the tradeoff instead of pretending there isn't one.

## The beat that proves the thesis

Run T04 both ways.

**Without D11 in the payload**, the frontier model answers: I can't confirm your zone district, it's probably R-1-6 or R-1-9, here are both tables, go pull it off the city map yourself.

**With D11 in the payload**, it answers the actual question.

The frontier model knows Title 17 cold. Section numbers, the 20% minor/major threshold, the waiver lever at 17.2.6, the six criteria, the six-month lockout. Enormous intelligence, all of it useless, because it was missing one fact about the house.

Raw intelligence commoditizes. Context compounds. The model says it for you by failing.

---

# T05 IN DETAIL

The frontier answer is roughly a thousand words with tables in it. Nobody says that out loud.

> HIP: "Short version. Your setbacks come off your zone district, which is R-1-6. Front twenty-five feet, sides five, rear fifteen. What you're describing needs a minor variance, which the director decides, so no public hearing. Want the details on your phone, or should I hold onto it?"
>
> Maya: "Hold onto it."

- ROUTING: EDGE. **The summary runs on the 7B.** The frontier did the thinking, the local model does the talking. The cascade works in both directions and the expensive tier never touches the interface.
- EPISTEMIC: new row, ASSERTED, sourced frontier.

**Two things this does.**

It is the second gate. The first governs what goes out. This one governs where the answer lands. Maya chose the destination instead of having it chosen for her. Coming in and going out, both doors.

"Hold onto it" makes the graph the destination. The answer does not evaporate at the end of the turn. It sits at ASSERTED, and the next time anyone in the house asks about zoning it is already there and already labeled as an outside opinion nobody verified.

**Rung policy, settled.** A frontier response enters at ASSERTED. An outside model is a source making a claim, same as a person. UNCONFIRMED means nobody has stood behind it, and the model did.

---

# SEEDS REQUIRED

Two new rows in `demo_seed.py`.

| ID | Rung | Owner to subject | Attribute | Value |
|----|------|------------------|-----------|-------|
| D10 | CONFIRMED | household to household | address | [REDACTED-HOME-ADDRESS] |
| D11 | CONFIRMED | household to household | zone_district | TBD, pull from city zoning map |

`eval/harnesslib/fixture.py` derives `SEED_FACTS` from `demo_seed.FIXTURES`, so adding here propagates. Seed values hold only the value, no narration.

---

# BUILD LIST

Nothing here exists except the routing.

1. **PROPOSED DISCLOSURE pane.** Outbound payload, one row per fact, each citing fact_id and rung, approve or deny. Without it T04 is narration and the script is dead. Build first.
2. **Frontier tier wired.** BYOK, one provider, Maya's key.
3. **Payload builder.** Code, reading fact rows. Never model-composed. A model will invent a clause and the pane will render it clean, because redaction only removes what it recognizes as identifying. It cannot tell that a clause is fiction. Model-composed payloads build a pane that certifies hallucinations.
4. **Return path.** Frontier response lands as a fact at ASSERTED.
5. **T05 disposition.** Summary on EDGE, then the phone-or-hold prompt, then the write.
6. **`narration` field** per turn in the script schema.

The JSON is not written. `demo_run.py --script` expects a specific shape and I have not seen an existing script file. Build it against `park_and_confirm__v20260712_1023.json`'s schema rather than from this table.

---

# VERIFY BEFORE PRESENTING

| Item | Why |
|------|-----|
| Zone district, off the Lakewood zoning map | D11's value. Everything in T04 and T05 depends on it. |
| The setback table against actual Title 17 | The numbers go on screen. The April 2026 repeal checks out (voters reverted to prior zoning, roughly 65/35). The section citations and distances do not, yet. |
| Whether the frontier model needs WEB to know about the repeal | It post-dates most training. If the model searched, T04 lights **two** tiers, not one, and the routing pane story changes. |
| What `NET` prints on a Groq call | MID and CORE are Groq today, which is external. If the pane prints NET ON over a Groq call, that is a false claim on screen at T02 and T03. |

---

# DISCLOSE, DO NOT GET CAUGHT

MID and CORE are Groq in the demo. In the target architecture they run in the operator hub on the RTX PRO 6000 / NIM enclave, on-net by construction. Say it in the voiceover, in your own words, before he asks. Disclosed it is a roadmap. Discovered it is the thing he tells the room about after you leave.
