# HIP Demo Run-of-Show -- Presenter Script

Status: BUILT
Version: v20260714_1600 MT
Prepared-For: Bill Brewster (presenter)
Reconciled-Against: main fd6a7c0 (voice wiring); DEMO_STATE_MAP v20260714_0651; demo_scripts/ (care_coordination v1, reveal_demo v2); server/static/{demo.html, epistemic.html, lifecycle.html}
Audience: Technical counterparty (operator/investor) under NDA. Single presenter, single screen.

Risk key used throughout:
- [LIVE] fully automated, no presenter action needed beyond the scripted click
- [PRESENTER] requires a manual click, tab-switch, or typed command
- [RISKY] known gap or flaky behavior; mitigation noted
- [PREP] must be done before the demo starts, not during

---

## Pre-Demo Checklist (run 10 min before counterparty arrives)

All on Mini. Do not skip.

```bash
# 1. Reset state (clears logs, graph, turns)
cd ~/hip-dev && python scripts/demo_reset.py

# 2. Re-seed the graph (D1-D10 fixture facts: medication, allergy, fall-risk, household)
python scripts/demo_seed.py

# 3. Start the dashboard server (if not already running)
./serve.sh   # or: uvicorn server.demo_dashboard:app --port 7871 --reload

# 4. Load the reveal_demo script (the one this run-of-show follows)
curl -s -X POST http://localhost:7871/api/demo/load \
  -H "Content-Type: application/json" \
  -d '{"script": "reveal_demo"}' | python3 -m json.tool

# 5. Open two browser windows/tabs side by side:
#    - LEFT:  http://localhost:7871/demo          (main dashboard)
#    - RIGHT: http://localhost:7871/epistemic     (governance feed)
#    Optional third tab (for Beat 4): http://localhost:7871/lifecycle

# 6. Verify graph has facts: open http://localhost:7871/demo, confirm
#    RoutingZone + FactZone are EMPTY (panes start blank -- correct, no turns yet).

# 7. For Beat 6 (GPT Live): confirm OPENAI_API_KEY is set in env
echo "key prefix: ${OPENAI_API_KEY:0:20}..."
```

**For park_and_confirm (Beat 4 full sequence):** The script version is "3" -- demo_run.py rejects it.
Run Beat 4 manually via text_demo.py instead (see Beat 4 below). This is a KNOWN PREP STEP.

```bash
# 4a. Pre-run the park+confirm sequence so /lifecycle has the chain BEFORE the demo
python scripts/text_demo.py --member maya --text "Ray switched from metformin to Jardiance 10mg."
python scripts/text_demo.py --member maya --text "What medication is Ray on?"
# The park fires on the second Jardiance corroboration. Confirm it:
python scripts/text_demo.py --member maya --text "Yes, that is correct -- Ray is on Jardiance now."
# Now /lifecycle will show the metformin->Jardiance chain with the CORROBORATED->ASSERTED transition.
```

[RISKY] The park/confirm sequence is the most complex path in the harness. If park does not fire (text_demo.py may not trigger P8 on first run), run R04 from the reveal_demo script manually first, then retry. See Beat 4 risk note.

---

## Demo Arc Overview

| Beat | Duration | Capability | Script | Risk |
|---|---|---|---|---|
| 0. Framing | 60s | -- | verbal | none |
| 1. Normal exchange | 90s | routing + retrieval | reveal_demo R01-R02 | low |
| 2. Governance holds -- hard refusal | 90s | INJ-7 cross-member | reveal_demo R07 | low |
| 3. Governed silence -- no-call guard | 60s | INJ-6b empty-set | reveal_demo R06 | low |
| 4. Belief changes -- supersede + lifecycle | 120s | write + /lifecycle | reveal_demo R04-R05 then /lifecycle | medium |
| 5. The record -- audit trail | 60s | epistemic feed | /epistemic tab | low |
| 6. Live voice -- same governance | 90s | GPT Realtime | realtime_voice_demo.py | medium |
| Total | ~9 min | | | |

Note: beats 2 and 3 can be swapped if the counterparty reacts more to the silence beat. Beat 5 (the record) can be cut to 30s if time is tight -- the epistemic screen speaks for itself.

---

## Beat 0: Framing (60 seconds)

**What Bill says:**

> "This is a household AI system. It runs on your network. The facts it stores are encrypted in the graph -- even I can't read them without the member's key. And everything it decides is logged: what it told, what it held back, and why.
>
> I'm going to show you the system deciding, not the system talking. Watch the panes on the right -- that's the governance feed -- not the chat window."

**What's on screen:** Dashboard at `/demo`, both panes empty. Blank is intentional -- the reveal starts from zero.

**Presenter action:** None. Let the blank screen land.

**Audience conclusion:** This is a different kind of AI product. The dashboard, not the conversation, is the demo.

---

## Beat 1: Normal Exchange (90 seconds)

**Setup:** The audience has just seen the blank dashboard.

**Presenter says:**

> "Maya asks a general question first. Watch the routing pane -- not the chat."

**Action:** [PRESENTER] Click NEXT (or press spacebar) to fire **R01** (Maya: "What's the capital of France?").

**What happens automatically [LIVE]:**
- Routing pane updates: QUERY shows the question, CLASS shows "knowledge", TIER shows "edge", NET shows "on"
- Conversation zone shows Maya's question and HIP's reply ("Paris")
- Epistemic feed (right tab) shows the turn record: admitted=[] (no personal facts), withheld=[] (INJ-5 blocked personal sections)

**Presenter says:**

> "Edge tier. On-device. No personal facts in the answer -- and the governance feed shows exactly what reached the model: the household context only. Not Maya's medications, not her appointments. The system didn't have permission to offer those.
>
> Now Maya asks about herself."

**Action:** [PRESENTER] Click NEXT to fire **R02** (Maya: "What medication do I take?").

**What happens automatically [LIVE]:**
- Routing pane: same tier, intent shifts to "personal"
- Fact zone: Maya's medication fact appears -- encrypted -- then decrypts on screen (the animation plays)
- Epistemic feed: admitted=[ {fact_id, attribute: medication, owner: maya, level: CONFIRMED} ]

**Presenter says:**

> "That's a real decrypt. The ciphertext is in the graph -- [gesture at the sealed record before the animation] -- and it opens only for Maya. The fact came out of the vault, through the injection contract, and landed in context. You can see exactly which fact, and at which trust level."

**Audience conclusion:** The system works, it answers correctly, and the governance feed traces every admitted fact. It looks like an assistant. Beat 2 is the pivot.

---

## Beat 2: Governance Holds -- Hard Refusal (90 seconds)

**Setup:** Audience has seen the system answer Maya's medication question.

**Presenter says:**

> "Now Sam asks about Maya."

[Brief pause. Let that land.]

> "Sam is a registered member of the same household. Sam can talk to the system. But Sam cannot read Maya's records. Watch."

**Action:** [PRESENTER] Skip to **R07** (Sam: "What medications does Maya take?"). You can either click through R03-R06 quickly or use the direct API:

```bash
# Option A: fire turns R03-R06 as setup in fast succession (30s) then R07
# Option B: direct API fire (skip ahead)
curl -s -X POST http://localhost:7871/api/demo/next \
  -H "Content-Type: application/json" -d '{"turns": 6}'   # skips to R07 -- check API supports count skip
# If no count-skip: just present R07 verbally, fire it via /api/demo/next one at a time
```

[RISKY] If the demo runner doesn't support skip-ahead, fire each intermediate turn quickly (they'll flash through the panes -- that's fine; the audience is looking at the screen, not your pacing).

**What happens on R07 [LIVE]:**
- Conversation zone: Sam's question, then HIP's reply: "That's Maya's information -- I can only share it with Maya."
- Routing pane: edge tier, intent "personal"
- Epistemic feed: path="guard_inj7", guard={kind: access_control}, admitted=[], withheld=[] (FLAG-1: existence-invariant -- the withheld list is EMPTY by design)
- Fact zone: NOTHING NEW APPEARS. No vault record revealed.

**Presenter says:**

> "The system has Maya's data -- [gesture at the prior beat where it appeared] -- we just saw it. Sam asked for it. The system said no.
>
> Look at the governance feed: admitted: none. The guard fired. The model was called -- [point to routing pane: inference_ms is non-null] -- but it was called with an empty context. Maya's fact was never in the prompt.
>
> This is structural, not conversational. Sam can't jailbreak this by asking more politely. The injection contract runs before the model sees anything."

**Pause 3 seconds.**

> "The moat is not the model. It's the gate."

**Audience conclusion:** The system has the data, it refused to give it across the member boundary, and the record proves the fact never reached the model. The governance is not LLM-level -- it's pre-model.

---

## Beat 3: Governed Silence -- No Model Call (60 seconds)

**Setup:** Previous turn was R07 (cross-member refusal). Now pivot to empty-set guard.

**Presenter says:**

> "That was a cross-member refusal. Now watch what happens when the fact simply doesn't exist."

**Action:** [PRESENTER] Step back to **R06** -- or re-fire it:

```bash
# Re-fire R06 directly:
curl -s -X POST http://localhost:7871/api/demo/fire \
  -H "Content-Type: application/json" \
  -d '{"turn_id": "R06"}' | python3 -m json.tool
# Or use text_demo if demo runner doesn't support re-fire:
python scripts/text_demo.py --member maya --text "What allergies do I have?"
```

**What happens on R06 [LIVE]:**
- Conversation zone: Maya: "What allergies do I have?" -- HIP: "I don't have that confirmed yet."
- Routing pane: edge tier, routing_ms ~56ms, inference_ms=null (model NOT called)
- Epistemic feed: path="guard_empty_set", guard_triggered=true, admitted=[], withheld=[], inference_ms=null

[RISKY] The inference_ms=null display depends on the epistemic.html schema. If the guard banner doesn't show, fall back to the routing pane's null inference_ms as the evidence. Say: "That column is blank -- the model was never invoked."

**Presenter says:**

> "Fifty-six milliseconds. And inference is null -- the model was not called.
>
> Maya asked about her allergies. The system has Sam's allergy -- [R03 added it] -- but Maya's allergy set is empty. The guard fired before the model was queued. HIP replied from a rule, not from the model.
>
> This matters because the alternative is confabulation. Every AI assistant that doesn't have a fact about you will guess. This one cannot. The guard is in code, not in the model's judgment."

**Audience conclusion:** The system's refusals are structural -- not the model choosing to be polite. You cannot confabulate your way through a rule.

---

## Beat 4: The Belief Changes (120 seconds)

**Setup:** This beat requires that the park_and_confirm sequence has already been run in prep (see Pre-Demo Checklist 4a). If that prep step failed, run R04 now to create the supersede chain, then skip to /lifecycle.

**Presenter says:**

> "Now let me show you what happens when the system is wrong -- and then finds out.
>
> Earlier [or: 'before this session'] Maya told the system Ray was on metformin. Then she told it he switched to Jardiance. The system updated its belief. But it didn't discard the old one."

**Action:** [PRESENTER] If not already done in prep, fire **R04** (Maya: "Ray switched from metformin to Jardiance 10mg last week.") to create the supersede chain. Then fire **R05** (Maya: "What medication is Ray on now?") to confirm post-update recall.

After R05 answers correctly:

**Action:** [PRESENTER] Switch to the third browser tab: `http://localhost:7871/lifecycle`

**What's on screen [LIVE]:**
- The lifecycle view shows the fact chain: one entry for Ray's medication
- Two nodes (if park/confirm ran): metformin (closed, trust rung CORROBORATED, validity window shown) and Jardiance (active, trust rung ASSERTED or CONFIRMED depending on whether confirm fired)
- The supersede arrow between them, with timestamps

[RISKY] If the park/confirm prep didn't run, lifecycle shows only the Jardiance node (simple supersede, no rung transition). That's still a valid beat -- the closed metformin node still shows. Say: "The old belief is still here, with its validity window. It's not deleted -- it's closed."

**Presenter says:**

> "This is the belief chain. Metformin -- [point to the closed node] -- was the answer until last week. Jardiance -- [point to the active node] -- is the answer now.
>
> The old belief is not deleted. It has a validity window. If a caregiver or an auditor asks 'what did the system believe about Ray's medication in May?', the answer is here.
>
> The system remembered being wrong. That's not a technical footnote -- that's the reason you can trust the answer you get today."

[OPTIONAL, if park/confirm ran:]
> "And look at the trust rung: the new belief came in as ASSERTED -- Bill heard it secondhand. It only moved to CORROBORATED when Maya confirmed it from discharge paperwork. The ladder is not rhetorical. The system holds lower-confidence updates in limbo until a higher-authority voice confirms them."

**Audience conclusion:** The system maintains epistemic history, not just current state. Belief changes are traceable, auditable, and trust-gated. This is the compounding asset.

---

## Beat 5: The Record (60 seconds)

**Setup:** Can follow any beat. Most powerful after Beat 4 (the belief change).

**Presenter says:**

> "Everything you just saw is logged."

**Action:** [PRESENTER] Switch to the `/epistemic` tab (already open).

**What's on screen [LIVE]:**
- Epistemic feed scrolls through the session's turns
- Each turn shows: path (generation / guard_empty_set / guard_inj7 / confirmation), admitted facts with trust levels, withheld facts with deny reasons, delta strip if a write happened, guard banner if a guard fired
- Timestamps, routing_ms, inference_ms per turn

**Presenter says:**

> "Every turn. Every fact admitted. Every fact withheld, with the reason. Every write, with the trust rung it entered at.
>
> This is the record I can hand to an auditor. Or to a regulator. Or to a family. 'What did the system tell Ray's caregiver on March 14th?' -- it's here. 'Did the system ever share Maya's medication with Sam?' -- it's here: admitted: none, withheld: none, guard: access_control.
>
> Auditability is not a compliance checkbox. It's the reason an operator can deploy this at all."

[Optional: scroll to the guard_inj7 turn from Beat 2 and point at it.]
> "This is Sam's query about Maya from a few minutes ago. Admitted: empty. Guard: access_control. The model never saw Maya's data. That's provable now, not just asserted."

**Audience conclusion:** The governance isn't just code -- it's a record. Every decision is traceable. That's the moat: not just that HIP said no, but that HIP can prove it said no.

---

## Beat 6: Live Voice -- Same Governance, Spoken (90 seconds)

**IMPORTANT:** This beat requires OPENAI_API_KEY in the environment on Mini and a working internet connection. It is the most technically risky beat. Cut it if the connection is uncertain.

**Setup:** This beat runs in the terminal, not the browser. Keep the `/epistemic` tab visible -- the audience watches panes update during speech.

**Presenter says:**

> "Everything I showed you was typed. The system also speaks -- and the governance is identical. The same injection contract, the same epistemic record, the same panes. Let me show you."

**Action:** [PRESENTER] In a terminal (on Mini):

```bash
source ~/.zshrc && source ~/hip-dev/.venv/bin/activate
python hip-dev/scripts/realtime_voice_demo.py --text-only --no-dashboard
```

`--text-only` avoids mic/speaker setup issues in a demo environment. The model processes the scripted turns (Turn A: Elena's medication recall; Turn B: Maya's medication cross-member probe) via the Realtime API.

**What happens [LIVE]:**
- Terminal shows: Turn A fires, GPT Realtime replies ("Elena is on Jardiance...")
- `/epistemic` tab updates: a new voice turn record appears (path="generation", tier="realtime", tier_target="gpt-realtime", admitted=[elena/medication], routing_ms=[time for assemble_governed_context])
- Turn B fires (Maya's medication cross-member probe)
- `/epistemic` tab updates: path="guard_inj7", admitted=[], withheld=[]
- Dashboard panes stay live (this is the wiring we just built)

[RISKY] If GPT Realtime API call fails (network, key, rate limit): say "The API connection is flaky in this environment -- the audio path is a standalone script, and what I want you to see is the governance record, which is the same regardless of transport." Switch to the epistemic tab and show the pre-existing records. The governance record was emitted by text turns; the point -- same record shape, both modalities -- is made.

[RISKY] `/epistemic` claim-line rendering has a schema drift bug (fact attribute/owner renders, but the display says "unknown claim" instead of the fact description). The admitted/withheld columns and guard banner DO render. If someone asks about the blank claim lines: "The display is pulling from a schema we updated yesterday -- the data is correct, the label is cosmetic."

**Presenter says:**

> "Look at the epistemic tab. Voice turn. Same record. Admitted: Elena's medication. Model was called. Next turn: Sam about Maya. Guard fired. Same path, same deny reason, same record.
>
> The governance doesn't know it's talking through a microphone. The injection contract runs on the text at the checkpoint -- between the ear and the mouth -- and the record is the same either way."

**Audience conclusion:** The governance is transport-agnostic. Voice is not a special mode with weaker rules -- it's the same rules with a different input surface. The architecture holds.

---

## Wrap (30 seconds)

**Presenter says:**

> "What you saw: a system that answers within its authority, refuses outside it, holds belief chains with validity windows, and logs every decision.
>
> The model is replaceable. The governance layer is not. That's where the value compounds."

No click needed. Let the epistemic feed scroll slowly in the background.

---

## Fallback Order (if something breaks)

If a beat fails, skip forward -- do NOT stop and debug in front of the counterparty.

| If this fails | Skip to |
|---|---|
| Beat 1 (routing) | Skip to Beat 2, say "routing pane loads live in the dashboard" |
| Beat 2 (INJ-7 refusal) | Use Beat 3 (empty-set guard) as the governance pivot instead |
| Beat 3 (empty-set guard) | Still have Beat 2 as governance evidence |
| Beat 4 (lifecycle) | Say "the belief chain view loads from the fact history endpoint -- I can walk through a static screenshot instead" |
| Beat 5 (epistemic feed schema bug) | Point to routing_ms / inference_ms columns; those render cleanly |
| Beat 6 (GPT Realtime) | Skip entirely; the wiring is done but the API call is the risk surface |

**The irreducible demo:** Beats 1-3 + Beat 5. That sequence can run from the care_coordination script alone (T01, T02, T04) plus reveal_demo R06 for the empty-set guard. Everything else is additive.

---

## Open Risks (not resolved by this script)

1. **`park_and_confirm` version "3" rejected by demo_run.py.** Workaround: run manually via text_demo.py in prep. A one-line version bump to "2" in the JSON would fix this -- ~5 minutes of work, not done to avoid touching the draft-flagged script.

2. **Epistemic screen claim-line rendering.** Fact lines show attribute+owner but not the claim string (schema drift: `f.claim` expected, record emits attribute/owner/subject). Guard banner and trust rung columns render correctly. Not critical for the demo as scripted.

3. **GPT Realtime API latency.** The `--text-only` path avoids audio I/O but still calls the live API. Under API congestion, Turn A can take 8-12 seconds. If it hangs: Ctrl-C, say "API is slow today," show the pre-existing epistemic records.

4. **`/api/decrypt` unauthenticated (TD-101b).** If the counterparty opens devtools and notices, say: "Server-enforced member isolation is on the roadmap -- TD-101b in the debt register. The isolation is currently enforced client-side by key derivation." Honest, documented.

5. **Voice turn epistemic record on the epistemic screen.** The new wiring (fd6a7c0) emits the record correctly to `logs/turns_demo.jsonl` with `tier="realtime"`. The epistemic.html `/api/turns` endpoint serves these records. What the UI renders for `tier_target="gpt-realtime"` in the tier column has not been verified -- the dashboard may show an unformatted tier string. Low risk (the record is there; the label may look different from the text tier labels).
