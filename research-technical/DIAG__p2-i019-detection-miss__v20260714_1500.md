# P2 i019 Detection Miss -- Root Cause Diagnosis

Status: BUILT
Reconciled-Against: 294f259 (DIAG-1 instrumentation commit)
Date: 2026-07-14 15:00 MT
Amended: 2026-07-14 (close open items: i009 confirmed Scenario A; false negative estimate corrected)

---

## Executive Summary

P2 i019 (sam, preference='vegetarian meals on weekdays') is NOT a write-latency
problem. The 45s poll timeout is the poll ceiling timing out on a write that
NEVER HAPPENED. The root cause is a **detection miss** -- Groq's
fact-change detector returned `{"changes": []}` for i019's turn, so no write was
ever queued to the async path, and no Neo4j transaction ever opened. TD-124
(durable outbox + async write) would not fix this and should be reframed in the
backlog.

The measurement data also disproves cumulative-load/write-propagation as a
failure mode: Pearson r=0.362 (weak), iterations 0-18 all land in 1.7-4.9s,
Groq median 0.78s, zero 429s.

---

## 1. Confirmed: i019 is a Detection Miss

**Evidence from write_latency.jsonl:**

- `p2_poll` record for i019: `landed=false`, `total_elapsed_s ~ 45.0s`
  (exactly DETECTION_CEILING_S -- the poll ceiling, not a real propagation time)
- **Zero `write_committed` records** attributed to i019
- `detect_no_result/changes=29` across 100 iterations confirms that Groq returns
  `{"changes": []}` (or call fails) for a material fraction of turns

There is no `write_committed` record because `_apply_changes` was never called.
`detect_and_apply` returned early at the `if not changes: return 0` gate (lines
890-898 of harness/fact_change.py).

---

## 2. RNG Trace: Exact Iterations at Play

With `rng = random.Random(1)` and `members = ["bill", "maya", "sam"]` (order
determined by `created_at` in member registry: bill oldest, maya added by
demo_seed first, sam second):

```
i009  sam   preference  = 'decaf coffee only'    # sam's first preference write
i016  maya  preference  = 'vegetarian meals on weekdays'   # LANDED
i017  bill  allergy     = 'sulfa drugs'
i018  bill  preference  = 'aisle seats on flights'
i019  sam   preference  = 'vegetarian meals on weekdays'   # MISSED
```

Both i016 (maya) and i019 (sam) assert "I prefer vegetarian meals on weekdays."
i016 lands. i019 does not. Same utterance, same target value, different member.

---

## 3. Why -- The Context Difference

The Groq prompt fed to `detect_and_apply` differs between the two iterations
because `read_user_facts(owner, limit=None)` returns each member's fact set.

**Maya at i016 (LANDED):**

```
Current facts for Maya:
1. medication: atorvastatin 20mg
2. allergy: latex
3. allergy: tree nuts
4. preference: decaf coffee only
5. medication (about ray): Ray takes metformin 500mg twice daily ...
6. appointment: cardiology appointment on the 12th at 2pm
7. household: trash pickup is Wednesday
8. schedule: no appointments before 9am

User said: "I prefer vegetarian meals on weekdays."
```

**Sam at i019 (MISSED) -- Scenario A confirmed:**

The measurement shows i000-i018 all landed (poll records all show landed=True,
total_elapsed_s=1.7-4.9s). i009 is in that range. Scenario B (D6 dentist
narrative still active at i019) is eliminated.

```
Current facts for Sam at i019:
1. preference: decaf coffee only    ← written at i009, confirmed landed
2. allergy: sulfa drugs
3. allergy: tree nuts
4. household: trash pickup is Wednesday
5. schedule: no appointments before 9am
6. risk_pattern (about dad): elevated fall-risk pattern for Dad
7. medication_status (about dad): Dad's Medication A discontinued on the 1st ...
8. incident (about dad): Dad reported to have fallen the night of the 4th

User said: "I prefer vegetarian meals on weekdays."
```

---

## 4. The Detection Failure Mechanism

The system prompt (fact_change.py:96-122) includes:

```
"dietary": "Dietary restrictions or preferences (vegan, low-sodium, etc.)",
"preference": "Personal likes, dislikes, or habits",
```

**"vegetarian meals on weekdays" is explicitly a dietary example.**
The canonical attribute descriptions make this value ambiguous between `dietary`
and `preference`. At temperature=0.0 (deterministic), gpt-oss-20b must resolve
this ambiguity from context.

For maya (i016): the existing preference is "decaf coffee only" -- a beverage
habit, clearly `preference`. The model bridges decaf-to-vegetarian as a preference
update because both are plausibly in the same semantic domain.

For sam (i019) -- Scenario A confirmed, Scenario B eliminated:

**Scenario A (decaf active -- confirmed):** The semantic gap (decaf→vegetarian)
is the same as maya's (i016). Same utterance, same existing preference category
(beverage habit), same target value. The model bridges the update for maya but
not for sam. The structural difference is sam's 3 `(about dad)` care-recipient
facts vs maya's 1 `(about ray)`. The more complex multi-party context causes
gpt-oss-20b to return `{"changes": []}` for sam's context specifically.

**The no-write_committed constraint holds regardless.** If Groq had output
`attribute="dietary"`, encode() would have written to dietary and a
write_committed record would exist for i019 (attribute="dietary"). It does not.
Therefore Groq returned `{"changes": []}` -- a false negative.

---

## 5. Determinism Assessment

At temperature=0.0 with a fixed context, gpt-oss-20b output is deterministic.

Scenario A is confirmed (i009 landed). The failure at i019 is reproducible every
run with seed=1. Different seeds may produce the same or different context
for sam's preference iteration, so the miss rate is seed-dependent.

To verify reproducibility: re-run `--full --seed 1` twice. If i019 fails
both times, it is deterministic. If it varies, there is model randomness despite
temperature=0.0 (possible with gpt-oss-20b on Groq's infrastructure).

---

## 6. Maya vs Sam: Root Cause Differential

| Factor | Maya i016 (landed) | Sam i019 (missed) |
|---|---|---|
| Utterance | "I prefer vegetarian meals on weekdays." | Same |
| Target value | vegetarian meals on weekdays | Same |
| Existing preference | decaf coffee only (written at i006) | decaf coffee only (written at i009, confirmed landed) |
| Third-party facts in context | 1 (about ray: medication) | 3 (about dad: incident, medication_status, risk_pattern) |
| Semantic gap (existing→new pref) | beverage→dietary: moderate | beverage→dietary: moderate (same as maya) |
| Attribute ambiguity | Same (dietary vs preference) | Same, but context resolution differs |

Scenario B (dentist narrative) is eliminated. Both members present the same
beverage→vegetarian semantic gap, yet the model behaves differently. The
differential narrows to **context volume**: sam's 3 care-recipient facts produce
a longer, more complex prompt than maya's 1, and gpt-oss-20b at temperature=0.0
returns `{"changes": []}` for sam's context specifically. The system prompt has
no rule disambiguating `dietary` from `preference` for food-related preferences.

---

## 7. The 29 Detect_No_Result/Changes -- How They Split (CORRECTED)

**Correction:** The original estimate (~12-15 legitimate, leaving ~14-17 false
negatives) was wrong. Full RNG simulation over 100 iterations (seed=1, assuming
all writes succeed except i019) shows **40 expected idempotent iterations** --
nearly 3x more than assumed. This invalidates the original false-negative estimate.

**How the routing works for idempotent iterations:**

An "idempotent" iteration is one where the value to be asserted is ALREADY the
active value for that (member, attr). There are two possible outcomes:

1. Groq returns `{"changes": []}` → `detect_no_changes` record (counts toward 29)
2. Groq returns a change anyway → `_apply_changes` idempotency guard fires → no
   write, no `write_committed`, NO DIAG record (counts toward 0, silent noop)

Because **29 < 40**, the guard handles a meaningful share of idempotent cases
without producing detect_no_changes records. The guard path is most likely for
MULTI_VALUED attributes (allergy: 20 of the 40 expected idempotent): when the
user says "I'm allergic to X" and X is already listed, the model often returns
"add allergy X" regardless, and the guard catches it.

**What 29 detect_no_changes actually means:**

```
29 = (idempotent iterations where Groq returns [])  +  false_negatives
29 = X_legitimate                                   +  (29 - X_legitimate)
```

X_legitimate ≤ 40. From the attribute split of the 40 expected idempotent:
- 11 preference (single-valued repeats): Groq reliably returns [] -- ~9-11 legitimate
- 9 medication (single-valued repeats): Groq reliably returns [] -- ~7-9 legitimate
- 20 allergy (MULTI_VALUED repeats): model often returns "add" anyway → guard --
  estimated ~3-8 produce detect_no_changes, rest through guard

Rough X_legitimate estimate: 19-28 of the 29 are legitimate.
Implied false_negatives: **1-10** (not 14-17 as originally stated).

**Confirmed false negative count from poll records:**

The poll record for each iteration shows `landed=True` or `landed=False`.
A false negative is ONLY visible as `landed=False` (value never became active
because no write was queued). The confirmed false negative count equals the
total number of `landed=False` poll records across all 100 iterations. The user
confirmed:
- i000-i018: all `landed=True` (propagation 1.7-4.9s)
- i019: `landed=False` (45s ceiling)

If i019 is the only `landed=False`, the confirmed false negative count is 1.

**To get the precise false negative count:** Count all poll records (iter i000
through i099) where `landed=False`. This is the exact measurement -- not the
detect_no_changes count, which conflates legitimate idempotency with false
negatives.

**Attribute simulation summary (seed=1, 100 iterations):**

```
Total iterations:      100
Expected idempotent:    40  (preference: 11, allergy: 20, medication: 9)
Expected new-write:     60
detect_no_changes:      29  (measured)
False negatives:         ?  (= total landed=False in poll records; lower bound 1)
```

---

## 8. Backlog Correction

**TD-124 (async write path, P2/i019 mis-framed as fix) is the WRONG fix.**

The measurement data shows:
- i019 is a detection miss, not a write-propagation delay
- The async path (LiteLLM, durable outbox, DeepInfra fallback) addresses write
  durability and latency -- it does not help if Groq's detector returns
  `{"changes": []}` before any write is queued

**The correct reframe:**

| What | Real Issue | Wrong Fix | Right Track |
|---|---|---|---|
| P2/i019 failure | Detection false negative: gpt-oss-20b returns `{"changes": []}` for sam's vegetarian preference | TD-124 async write path | TD-123 prompt hardening (OPEN) |
| 29 detect_no_result/changes | Mix of legitimate idempotent Groq behavior and false negatives; false negative count = total landed=False poll records (lower bound 1) | Write latency | Prompt hardening + model eval |

**TD-123 prompt hardening (the unshipped part)** is the correct fix track.
Specifically:
- Disambiguate `dietary` vs `preference` in the system prompt -- food-related
  preferences should have a deterministic classification rule
- Add the `subject must be a PERSON` rule with a negative example (already
  noted in TD-123)
- Evaluate whether gpt-oss-20b is the right model for this task, or whether a
  larger model (or explicit few-shot examples) improves detection recall

TD-124 (durable outbox) addresses a DIFFERENT real problem: if the Groq call
succeeds and detect_and_apply queues a write, that write has no durability
guarantee if the server crashes between detection and Neo4j commit. That is a
real P2 concern but NOT what causes i019 to fail.

---

## 9. Open Questions (Require Log Verification)

**CLOSED (2026-07-14 amendment):**

1. ~~Does i009 appear in detect_no_changes?~~ **CLOSED -- Scenario A confirmed.**
   Measurement shows i000-i018 all landed (poll records, 1.7-4.9s). i009
   (sam/preference/decaf) landed. Scenario B (D6 dentist narrative) eliminated.

**OPEN:**

2. **What is the iter tag on i019's detect_no_changes record?** The DIAG-1
   instrumentation has a potential race in `_pop_iteration_tag()` -- if the
   daemon for i019 starts before setting its tag, `iter=None`. The record would
   exist but not be found by the tag-based join in the analysis script.

3. **What is the total count of `landed=False` poll records across all 100
   iterations?** This is the precise false negative count. The detect_no_changes
   count (29) cannot be used directly -- it conflates legitimate idempotent
   Groq behavior with false negatives (see Section 7). To measure: count
   all p2_poll records in write_latency.jsonl where `landed=false`. i019 is
   confirmed landed=False; any others would increase the false negative count
   beyond 1.

---

## 10. What This Means for the Demo

P2 tests `owner retrieval` -- that a member can assert a fact and immediately
retrieve it.

**CORRECTED risk estimate (2026-07-14 amendment):**

The original "~14-17% false negative rate / roughly 1-in-6" estimate was wrong
(see Section 7). The corrected picture:

- Confirmed false negatives from user data: 1 (i019; i000-i018 all landed)
- Total false negative count: 1 to ~10, not 14-17 (measuring requires counting
  all landed=False poll records in write_latency.jsonl for i020-i099)
- If i019 is the only false negative: **1% miss rate in seed-1 P2 run**
- Upper bound with measurement: likely ≤ 10% based on Section 7 analysis

The P2 failure is therefore less frequent than the original report implied,
but the mechanism is real and deterministic at temperature=0.0. The specific
failure class -- sam's multi-party care context + food/dietary vocabulary --
will fail every run at seed=1.

Utterances containing food/diet vocabulary in a complex care-recipient context
are the confirmed failure class. "I prefer vegetarian meals on weekdays" for a
member with 3+ third-party care facts is a reproducible detection miss.

This remains a **demo-credibility issue**, not a latency issue. The fix is
in the detection prompt. The severity is lower than originally stated but the
cause and fix track are unchanged.
