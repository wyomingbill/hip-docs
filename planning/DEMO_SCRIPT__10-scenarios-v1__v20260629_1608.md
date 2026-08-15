<!-- STATUS: STALE -->
<!-- RECONCILED-AGAINST: scripts/demo_seed.py (Bill/Sarah fixture — scenario members match but this is the June-29 draft); docs/INDEX.md (superseded; INDEX listed DEMO_SCRIPT__v20260705_1345.md as current); demo is now text-query-first, not voice-recording — 2026-07-05 -->

# HIP Demo Script -- 10 Scenarios

Screen recording of the HIP UI (/hip page) with voice narration.

---

## Scenario 1: Greeting and Identity

**Setup:** Connect to HIP. Say nothing.

**Expected response:** "Hey, I'm here."

**Narrative:** HIP greets the user. Speaker verification identifies Bill from his voiceprint. No login, no PIN -- the voice is the credential.

---

## Scenario 2: Personal Fact Recall

**Say:** "What medication do I take?"

**Expected response:** "You take atorvastatin 20mg daily."

**Narrative:** The fact was stored in the encrypted graph. Retrieved, decrypted, and spoken. All on-device. The dashboard shows EDGE tier, PERSONAL intent, ON-NET. No data left the network.

---

## Scenario 3: Fact Correction (Retraction)

**Say:** "I don't take any medication."

**Wait:** 3 seconds.

**Say:** "What medication do I take?"

**Expected response:** "You don't take any medication."

**Narrative:** The correction was detected by Llama 4 Scout on Groq in under a second. The old fact was retracted in Neo4j. The graph is current before the next question. No batch sync, no cache invalidation delay.

---

## Scenario 4: Preference Recall

**Say:** "What do I like to drink in the morning?"

**Expected response:** "You prefer dark roast coffee in the morning."

**Narrative:** Another personal fact, retrieved from the encrypted graph. Same pipeline as the medication -- the domain classifier recognized this as a preference query and scoped the retrieval accordingly.

---

## Scenario 5: Preference Update

**Say:** "I actually like my coffee black, no milk."

**Wait:** 3 seconds.

**Say:** "Do I like milk in my coffee?"

**Expected response:** "You prefer your coffee black."

**Narrative:** The Groq fact-change detector caught the semantic update. Not a simple retraction -- the model understood that "I like it black" modifies the coffee preference rather than erasing it. The graph reflects the new state immediately.

---

## Scenario 6: Weather (Temporal Routing)

**Say:** "What's the weather supposed to be like today?"

**Expected response:** Real weather data for Lakewood, CO.

**Narrative:** The intent classifier recognized this as a TEMPORAL query. Routed to SerpAPI for live data. The dashboard shows WEB tier, OFF-NET. The model uses only the web results, not training data. Personal context was stripped before the query left the network.

---

## Scenario 7: General Knowledge (Complexity Routing)

**Say:** "Summarize World War II in two sentences."

**Expected response:** Accurate summary of World War II.

**Narrative:** KNOWLEDGE intent, routed by complexity to CORE tier on Groq. The dashboard shows the Bloom's taxonomy level -- this query scored at synthesis, which pushes it to the 70B model. General question, not personal. The model answers from its training data.

---

## Scenario 8: Temporal Reasoning

**Say:** "When is the next trash pickup?"

**Expected response:** "Trash pickup is every Tuesday morning. The next one is [correct date]."

**Narrative:** The fact is stored as "trash pickup every Tuesday morning." Temporal enrichment computed the next occurrence at retrieval time. The model reads the enriched fact and gives a specific date, not a generic schedule.

---

## Scenario 9: Privacy Boundary

**(Narrate -- no live demo required)**

**Narrative:** Personal facts stay on-net. When a query requires the cloud -- weather, complex knowledge -- personal context is stripped before anything leaves the device. The operator's infrastructure is the trust perimeter. HIP never sends "Bill takes atorvastatin" to a third-party API. The query goes out. The facts stay in.

---

## Scenario 10: Dashboard Walkthrough

**(Scroll through the dashboard on screen)**

**Narrative:** The routing log shows every query, its intent classification, which tier handled it, and whether data left the network. The facts panel shows the encrypted graph -- only the verified speaker sees decrypted values. Every decision is auditable. The operator can see what routed where. The consumer can see what was stored.

---

## Closing Narrative

"This is a household AI operating environment built on cable operator edge infrastructure. The consumer's phone holds the key. The operator's hardware holds the vault. Neither works without the other. Privacy is architectural, not policy."
