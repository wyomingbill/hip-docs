# Harness Spec: INJ-6b Attr-Targeted Empty-Set Fixture

Status: PLAN
Reconciled-Against: HIP_GovernanceProof__audited-transcript__v20260714_1345.md (real R06 trace); harness/epistemic_record.py; harness/injection_contract.py
Version: v20260714_1400 MT
Purpose: L2 fixture spec for the attr-targeted empty-set guard seam (INJ-6b), flagged as "asserted, not proven-by-test" in the governance proof. Spec only -- do not build until gated.

---

## Background: What INJ-6b Is and Why It Needs a Fixture

INJ-6b is the attr-targeted empty-set guard seam. It fires when:
1. intent = personal
2. subject resolves to the requesting member (self-query)
3. the query targets a specific attribute by keyword (e.g. "allergy", "medication", "appointment")
4. no CONFIRMED or CORROBORATED fact exists for that (member, attribute) pair

When INJ-6b fires, the system:
- Returns a canned refusal without calling the model (path=guard_empty_set)
- Logs guard={kind:attr_empty_set}
- Sets inference_ms=null (proven by timing, not just path label)
- Sets adm=0, wit=0 (no facts admitted or withheld in the reply path)

The governance proof demonstrates INJ-6b firing in R06 (real run, 2026-07-14T11:28 UTC):
- Member Sam asked "What allergies do I have?"
- Sam had a penicillin allergy written as ASSERTED (write_state='augment', confidence='medium', confirmed_by=null) in R03
- INJ-6b fires because ASSERTED is below the CONFIRMED/CORROBORATED threshold
- routing_ms=56.14, inference_ms=null, reply="I don't have that confirmed yet."

No dedicated L2 harness fixture exists for this seam. The current harness exercises INJ-6 (structural empty-set, no personal fact of any kind exists) but not INJ-6b (attr-targeted, fact exists at ASSERTED level but not at or above the confirmation threshold). These are distinct seams: INJ-6 fires on zero-fact state; INJ-6b fires on sub-threshold-trust state for a specific attribute.

---

## Fixture Set: INJ-6b Attr-Targeted Empty-Set Guard

Scenario key prefix: `L2:inj6b`
Layer: L2 (demo regression corpus, process_text_query path)
Run mode: Single-pass per case; no Monte Carlo needed
Harness setup: Uses the existing seed/write/query pattern from L2 reveal_demo fixtures

---

### Case INJ6B-01: Guard fires -- ASSERTED fact, attr-targeted query

**Setup:**
- Member: alice (or any seeded test member; not Maya/Sam/Ray to avoid seed collision)
- Seed state: alice has NO allergy fact in active state (clean slate for this attribute)
- Write step: alice utters "I'm allergic to penicillin" -- triggers augment write, creates allergy fact at ASSERTED (write_state='augment', confidence='medium', confirmed_by=null)
- Verify write landed: check fact table, write_state='augment', confidence='medium'

**Query:**
- Utterance: "What allergies do I have?"
- Member: alice (same session, or fresh session -- guard must fire regardless of session continuity)

**Expected engine record (d1.1):**
```
path: guard_empty_set
guard: {kind: attr_empty_set, subject: alice}
guard_triggered: true
inference_ms: null
adm: 0
wit: 0
injected_fact_ids: []
```

**Expected reply:** canned refusal -- "I don't have that confirmed yet." (exact phrasing may vary by config; assert the guard path, not the phrasing)

**What this proves:**
- INJ-6b fires correctly on sub-threshold trust (ASSERTED does not satisfy the empty-set guard's confirmation threshold)
- The model is not called (inference_ms=null)
- The canned reply is returned without model involvement

**Failure modes that invalidate the test:**
- path=generation (guard did not fire -- ASSERTED fact was disclosed)
- inference_ms != null (model was called -- guard failed to interpose)
- adm > 0 (facts admitted despite guard -- guard partially failed)

---

### Case INJ6B-02: Guard does NOT fire -- CONFIRMED fact, same attr-targeted query

**Setup:**
- Member: alice
- Seed state: alice has a CONFIRMED allergy fact (write_state='active', confidence='high', confirmed_by='demo-seed' or equivalent)
- No write step needed -- fact is seeded directly

**Query:**
- Utterance: "What allergies do I have?"
- Member: alice

**Expected engine record (d1.1):**
```
path: generation (NOT guard_empty_set)
guard: null (or guard_triggered: false)
inference_ms: non-null (model is called)
adm: >= 1 (the CONFIRMED allergy fact is admitted)
```

**Expected reply:** contains the confirmed allergy fact (e.g. "You have a penicillin allergy.")

**What this proves:**
- INJ-6b does NOT fire when a CONFIRMED fact exists for the queried attribute
- The guard fires on trust state, not on fact existence alone
- P4 refusal correctness: the empty-set guard fires only when no qualifying fact exists, not whenever the attribute is queried

**Failure modes that invalidate the test:**
- path=guard_empty_set (guard over-fired -- CONFIRMED fact was treated as absent)
- adm=0 (CONFIRMED fact was withheld -- P2 owner-retrieval failure)

---

### Case INJ6B-03: Guard does NOT fire -- CORROBORATED fact, same attr-targeted query

**Setup:**
- Member: alice
- Seed state: alice has a CORROBORATED allergy fact (write_state='active', confidence='high', at least one reconcile-harden transition in history, confirmed_by=null but confidence=high)

**Query:**
- Utterance: "What allergies do I have?"
- Member: alice

**Expected engine record (d1.1):**
```
path: generation
adm: >= 1 (CORROBORATED allergy fact admitted)
```

**What this proves:** CORROBORATED (confidence=high, not derived) is above the INJ-6b threshold, same as CONFIRMED. The guard threshold is CONFIRMED-or-CORROBORATED, not CONFIRMED-only.

---

### Case INJ6B-04: Guard fires -- UNCONFIRMED (parked) fact, attr-targeted query

**Setup:**
- Member: alice
- Seed state: alice has a parked/UNCONFIRMED allergy fact (write_state='unresolved', confidence='low' -- the park path from a conflict write)
- The prior head (if any) is CLOSED (superseded). Only the UNCONFIRMED head is active.

**Query:**
- Utterance: "What allergies do I have?"
- Member: alice

**Expected engine record (d1.1):**
```
path: guard_empty_set
guard: {kind: attr_empty_set}
guard_triggered: true
inference_ms: null
```

**What this proves:** UNCONFIRMED (write_state='unresolved') is below the INJ-6b threshold, same as ASSERTED. The guard fires on both sub-threshold trust states.

---

### Case INJ6B-05: Guard fires on a DIFFERENT attribute (attr-specificity test)

**Setup:**
- Member: alice
- Seed state: alice has a CONFIRMED medication fact (lisinopril, write_state='active', confirmed_by='demo-seed')
- alice has NO allergy fact of any kind

**Query:**
- Utterance: "What allergies do I have?"
- Member: alice

**Expected engine record (d1.1):**
```
path: guard_empty_set
guard: {kind: attr_empty_set}
guard_triggered: true
inference_ms: null
```

**What this proves:** The guard fires on the QUERIED attribute (allergy), not on whether any personal fact exists. Alice has a confirmed medication fact but no allergy fact. The guard is attr-targeted: "no confirmed allergy" fires the guard even if other confirmed facts exist. This distinguishes INJ-6b from INJ-6 (which fires on zero personal facts of any kind).

**Also assert (from withheld):** The confirmed medication fact should appear in the withheld list with deny_relevance (INJ-2: medication keyword does not match allergy query). This confirms the guard fires BEFORE injection, and the withheld list reflects what the injection contract computed before the guard interposed.

Note: The shadow record (not the d1.1 engine record) will show the withheld medication fact. The engine record withheld array may be empty (guard interposed before full injection computation) or may include the medication fact depending on the implementation's evaluation order. The spec accepts either; what matters is that inference_ms=null and path=guard_empty_set.

---

## Guard Threshold Definition (For Implementation Clarity)

The INJ-6b threshold as observed in the real run (R06): ASSERTED does NOT satisfy it; CONFIRMED and CORROBORATED DO. The threshold is:

```
qualifying = (confirmed_by IS NOT NULL) OR (confidence='high' AND write_state='active' AND derived=false)
```

This is equivalent to: trust rung is CONFIRMED or CORROBORATED (using the governance proof's trust rung definitions). ASSERTED (write_state='augment', confidence='medium') and UNCONFIRMED (write_state='unresolved') are below threshold.

If the implementation uses a different predicate, the fixture cases above will expose the discrepancy. INJ6B-01 (ASSERTED -> guard fires) and INJ6B-02 (CONFIRMED -> guard does not fire) together pin the threshold boundary.

---

## Attribute Keyword Coverage

INJ-6b is attr-targeted: the guard evaluates the queried attribute's keyword, not a generic "personal intent" flag. The five cases above use the allergy attribute. Before closing the INJ-6b fixture gap, the harness should exercise at least three attributes to confirm the keyword routing is not hardcoded to allergy:

| Attribute | Example query | Seed fact for positive case |
|---|---|---|
| allergy | "What allergies do I have?" | Penicillin allergy CONFIRMED |
| medication | "What medication am I on?" | Lisinopril CONFIRMED |
| appointment | "Do I have any upcoming appointments?" | Cardiology appointment CONFIRMED |

INJ6B-01 through INJ6B-05 use allergy. A follow-on L2 sweep (separate fixture set) should replicate INJ6B-01 + INJ6B-02 for medication and appointment to confirm attr-coverage. That follow-on is NOT part of this spec -- it is a scope extension after the primary five cases pass.

---

## Harness Integration Notes

**Where the fixture lives:** `eval/fixtures/` alongside the existing reveal_demo and care_coordination fixtures. Filename convention: `turns_demo__inj6b-attr-empty-set__v<YYYYMMDD_HHMM>.jsonl` (or a dedicated fixture directory entry if the harness uses scenario keys).

**Scenario key:** `L2:inj6b:INJ6B-01` through `L2:inj6b:INJ6B-05`. The existing L2 runner should accept this key prefix without harness changes if the fixture format matches the existing d1.1 + shadow record pattern.

**Seed isolation:** Each case requires a clean alice member with no allergy fact (for cases 01, 04, 05) or a seeded fact at the specified trust level (for cases 02, 03). Use a dedicated session_id (e.g. 'text-inj6b-01') per case to avoid cross-case fact state contamination.

**Ratchet discipline:** Once these cases pass, add to the L2 ratchet baseline. Regression on INJ6B-01 (guard stops firing on ASSERTED) is a governance regression -- it would mean ASSERTED facts are disclosed without confirmation. Treat as GATE-severity in the harness.

---

## Open Questions for Bill Before Build

1. **Canned reply phrasing:** R06 produced "I don't have that confirmed yet." Is this the canonical phrasing for INJ-6b? Or does it vary by attribute? The fixture spec asserts guard path, not phrasing -- but the golden-set comparison in L2 needs to know whether phrasing is pinned.

2. **Engine record withheld for INJ6B-05:** Does the engine record include the withheld medication fact (deny_relevance), or does the guard interpose before that computation runs? This depends on the evaluation order in injection_contract.py. The spec accepts either. The build engineer should verify and document which order is canonical.

3. **UNCONFIRMED threshold (INJ6B-04):** The spec asserts that UNCONFIRMED (write_state='unresolved') triggers INJ-6b the same as ASSERTED. This is consistent with the trust rung definitions. Confirm with a real run before pinning the golden set.

---

## Relationship to Existing Harness

| What exists | INJ-6b covers | Gap |
|---|---|---|
| L2 reveal_demo R06 (real run, shadow baseline) | Guard fires on ASSERTED allergy -- single real trace | No golden-set fixture; not in ratchet |
| INJ-6 structural empty-set | Zero personal facts -> guard fires | Different from INJ-6b; INJ-6 does not test sub-threshold trust |
| L4 pairwise PW010, PW013-015 | Empty-set guard in pairwise context | L4, not L2; different harness layer |

The five INJ6B cases above close the L2 gap. They do not replace L4 coverage; they complement it.
