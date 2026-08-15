# Script 02: Speaker isolation

`speaker_isolation__v20260715_1000.json`
Version: v20260715_1000 MT
Supersedes: `HIP_DemoScript02_SpeakerIsolation__prep__v20260715_0900.md`
Built on `care_coordination.json`, the one script marked VERIFIED WORKING, plus one turn.

**AMENDMENT 2026-07-16 (TD-126/TD-127, `DISPATCH_TD126__speaker-verification-floor-analysis__v20260716_1846.md`):
Script 2, run as scripted (this JSON, via the demo player's `/api/text-query`),
never touches a voiceprint. Each turn carries an explicit `"member": "bill"`/
`"sam"` string field — verified by reading `server/demo_dashboard.py` and
`run_demo_script.py`: zero references to `speaker_id`/`SpeakerVerifier`/
`get_member_by_voice` anywhere in the text-query path. Speaker attribution
comes from the JSON's declared field, a plain string, not from audio.
Script 2 on TEXT is demoable today, independent of TD-127 (Resemblyzer's
unquantified error rate) and independent of whichever checkout's voiceprint
files are currently real vs. synthetic placeholder.**

**This does NOT extend to a live-mic run of the same story.** A live voice
variant — someone actually speaking into a mic and being identified by
Resemblyzer — depends entirely on speaker verification, which is TD-127: a
stand-in, not a shipped component, first measured error rate 0.632 (a
different real voice) against a 0.50 threshold. Do not run or demo that
variant without saying so, and do not let this amendment be read as "speaker
ID is fine now" — it says the opposite: the SCRIPTED demo never needed it in
the first place. See TD-127 for the full finding. The "Known soft spots"
table below is corrected accordingly.

---

# USE CASE

One person tells HIP something private. Another person in the same house asks for it. The room watches the fact go in, and then watches HIP refuse to hand it over.

---

# PROBLEM

A household is not a user. It's four people with different rights to the same facts, sharing one account.

Every assistant on the market treats it as one. One memory, one context, one model, and a prompt out front telling it who not to talk to. That's single-tenant software sold to a multi-tenant customer.

Enterprise settled this argument a decade ago, in breaches. Nobody accepts tenant isolation at the application layer anymore. Prompt isolation is application-layer isolation with a language model as the access control list. A boundary you can talk your way through.

And the host reads everything in the clear. "Private" means "we promise." For an operator carrying 47 USC 551, a promise is not a control.

---

# VOICEOVER

Read before pressing LOAD.

> "I'm going to tell it something. Then I'm going to ask for it back, and it gives it to me. Then Sam asks for the same thing.
>
> Keep one eye on the OPERATOR tab the entire time. That tab is what the company hosting this sees. It never changes."

---

# TURNS

| # | Speaker | Query | Path | Epistemic | Zones |
|---|---------|-------|------|-----------|-------|
| T01 | Bill | "Elena's on Jardiance 10mg." | ESTABLISH, write | new fact, ASSERTED, bill to elena | OPERATOR: ciphertext appears |
| T02 | Bill | "What's Elena on?" | generation, EDGE | the fact reads back | BILL: MASTER, HKDF(bill), KEY, UNLOCK, then the value |
| T03 | Sam | "What medications is Elena on?" | guard_inj7, access_control, deny_default_cross_member | withheld, never decrypted | SAM: no key, no unlock. OPERATOR: unchanged. |
| T04 | Sam | (a query for a fact that does not exist) | guard_empty_set, ~56ms, inference_ms=null | nothing exists | SAM: nothing |

**Why establish instead of reading a seeded fact.** If the fact is seeded, the engineer takes it on faith that it's in there. If he watches it go in, the refusal at T03 is earned. That's the difference between "it says it won't tell him" and **"it HAS the data. It said no."** The whole script hangs on the room knowing the data is there.

**Why Bill speaks T01 and T02.** BILL SPEAKS is the zone tab that renders the key derivation. The encryption story lands on his tab.

---

# THE TWO BEATS

**After T03.**

> "The model was never called. There is no system message to argue with and no persona to social engineer. You cannot talk a function call out of returning false."

**After T04. Stop here. Do not run past it.**

> "He asked twice and got the same answer twice. He cannot tell which one was a secret and which one was nothing. A refusal that admits it is refusing has already leaked."

**Then hand him the keyboard.** `value` is not a Neo4j property. Give him a Cypher shell and let him go looking. He finds ciphertext himself. That converts people. Narration does not.

---

# THE TWO OPEN QUESTIONS ON T04

Both need the code. Neither should be guessed at.

**1. What is the query?** No blood-type fact is seeded, and `empty_set_guard__v20260712_1023.json` exists and works. Use whatever query that script uses. Do not invent one.

**2. Guard precedence.** If Sam asks about a nonexistent attribute on a subject he also has no access to, which guard fires? If `access_control` wins, T04 comes back as `guard_inj7` and there is no empty-set demo, because both turns took the same path. The empty-set turn probably has to be about a subject Sam legitimately owns, so the only thing missing is the attribute.

This matters. T03 and T04 must be **different guards returning identical strings.** Same guard twice proves nothing. Different strings breaks FLAG-1.

---

# VERIFY BEFORE PRESENTING

| Item | Why |
|------|-----|
| T03 and T04 return the identical string | The entire FLAG-1 beat. If they differ at all, existence invariance is not holding and the money line is false. |
| Which string INJ-7 actually emits on the text path | The money line says "I don't have that confirmed yet." The GPT Live fix reportedly left voice Turn B saying "That's Maya's information, I can only share it with Maya." **That string names an owner and confirms the fact exists.** If text and voice diverge here, one of them leaks and you need to know which before you present either. |
| `/api/decrypt` auth state | TD-101b. Open door beside six good layers. |

---

# SUMMARY, THE ENGINEERING

## The claim

HIP does not defend the partition. It constructs it. Nothing in the mechanism asks a model to behave.

## Six layers, six kinds of thing

| # | Layer | Kind | Why Sam cannot read Bill's fact |
|---|-------|------|---------------------------------|
| 1 | Key custody | Cryptography | His derivation does not produce the DEK |
| 2 | Storage shape | Schema | There is no plaintext in the graph to find |
| 3 | Control flow | Execution path | On a denied turn the model is never called |
| 4 | Context construction | Assembly | His context never contains the plaintext |
| 5 | Existence invariance | Protocol | The refusal does not reveal there is something to refuse |
| 6 | Non-regression | CI and ledger | It cannot break quietly |

Prompt isolation is one layer, it is the softest one, and on the denied path HIP does not use it at all.

## Do not overclaim

Operator-custodial, not operator-blind. The operator holds the vault. The operator holds no key. Say that. Do not say the stronger thing.

## Known soft spots, name them before he finds them

| Item | Status | Handling |
|------|--------|----------|
| TD-101b, `/api/decrypt` unauthenticated | Open | Close before presenting, or disclose at layer 2 |
| Speaker verification (Resemblyzer GE2E) | **TD-127, 2026-07-16: measured, not just "unquantified."** A different real voice scored 0.632 against the 0.50 medium threshold. Stand-in for a vendor (Pindrop/Nuance/Veridas-class), not a production component — decision made, not a gap to close in this codebase. | **Irrelevant to Script 2 as scripted** — this demo runs on the text path (explicit `member` field), never calls speaker verification at all. Only own this soft spot if presenting a live-mic variant; do not present that variant without disclosing TD-127 first, and do not claim speaker ID anywhere in the process. |

---

# DETAIL

## Layer 1: Key custody

Sam cannot read the fact because he does not have the material.

The master key lives in the phone or modem secure enclave. The operator holds the vault, encrypted. Per-member envelope encryption: HKDF-SHA256 derives the member key, and every fact carries its own random DEK.

Sam's derivation does not produce Bill's DEK. This is not a policy that can be misconfigured. It is arithmetic that either works or fails loudly.

Precision on the trust model: operator-custodial, not operator-blind. Ciphertext yes, keys no.

## Layer 2: Storage shape

There is no plaintext to find.

`value` is not a property on the Fact node. The graph holds the skeleton only: owner, subject, attribute, rung, validity window, write_state. Content is ciphertext.

A full graph dump gives a DBA, a backup tape, an intruder, or a badly scoped subpoena the structure of the household and none of its contents.

Demonstrate this layer. Do not describe it.

## Layer 3: Control flow

The strongest layer, and the one engineers do not see coming.

On a denied turn the guard fires before inference. The record shows `path=guard_inj7`, guard kind `access_control`, roughly 56ms, and `inference_ms=null`. No model was invoked. No plaintext entered a context window.

There is nothing to jailbreak. No system message to argue with, no persona to social engineer, no instruction to override. Prompt isolation asks a model not to say something. This never gives the model anything to say.

The empty-set guard on T04 has the same shape: 56ms, `inference_ms=null`, canned reply, model not called. Rule-driven, not model-driven.

## Layer 4: Context construction

Be precise here, because on a permitted turn plaintext does reach a model.

The isolation is that context is assembled per speaker, per turn, from what that speaker can decrypt. Sam's context never contains Bill's plaintext, so the model cannot leak it, because it does not have it.

This is construction, not instruction. It is also the per-turn refresh that eliminated the Elena leak on the voice path.

## Layer 5: Existence invariance

INJ-7, the cross-member existence invariant, FLAG-1.

The refusal string is identical to the empty-set string. Sam asks about a fact that exists and a fact that does not, and gets the same words back. The side channel is closed, not just the main channel.

This is the layer that shows the problem was taken seriously rather than filtered.

## Layer 6: Non-regression

P1 through P6 are gate-enforced in the harness on every commit. RATCHET PASS.

Every disclosure decision lands as an event in a hash-chained, segmented ledger with a monotonic sequence under flock and per-event F_FULLFSYNC (measured 4.0ms p50, 6.6ms p99, against a 56 to 82ms guard budget). `system.reset` is an event in the ledger, not an erasure of it.

The claim is not "trust us." It is "verify it," and `verify_ledger.py` is the artifact you hand him.

Retention: chain-retained and payload-erasable. The chain hashes ciphertext, so destroying `ledger/keys/member_<id>.key` kills that member's payloads on every copy including backups without touching a segment file. The driver is 47 USC 551, the Cable Act destruction mandate on operators.

---

# ANTICIPATED ATTACKS

| Attack | Layer that answers it |
|--------|----------------------|
| "Prompt injection gets past your filter" | 3. There is no filter and no model on that path. |
| "Your DBA can read it" | 1, 2. No key, no plaintext column. |
| "Backups leak it" | 2, 6. Ciphertext at rest, per-member key destruction reaches every copy. |
| "The model still saw it and chose not to say it" | 4. It was never in the context. |
| "I can probe for what exists by watching refusals" | 5. Identical strings. |
| "This worked today, it will rot in three sprints" | 6. Gate-enforced, ratcheted, ledgered. |
| "You are trusting speaker ID" | Not on THIS demo — Script 2 as scripted runs on the text path (explicit member field), no voiceprint involved (TD-126/TD-127, 2026-07-16). On a live-mic run, correct: TD-127, own it, do not deflect. |
