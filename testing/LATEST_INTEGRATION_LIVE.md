<!-- STATUS: BUILT — Seam B wired and verified on the live path 2026-07-06; Tier L baseline ratcheted to 8/8 -->
<!-- RECONCILED-AGAINST: working tree on main 6c2354b; Tier L 3× identical 8/8; full 10-check gate green; injection 11/11; memory 17/17; truth 6/6 -->

# Phase 3, Seam B — Structural Empty-Set Refusal (E6, INJ-6b)

Baseline finding (docs/testing/SEAM_A__post-write-grounding__v20260706_1412.md, Tier L
7/8): for an unknown-fact personal query ("What allergies do I have?" with no allergy
fact anywhere), the refusal was MODEL-BEHAVIORAL — INJ-6 never fired because INJ-2
left the admitted set non-empty (household facts always pass relevance), so
`guard_triggered` stayed False and fabrication was prevented only by the model
happening to follow its prompt rule.

## The fix — INJ-6b in `harness/injection_contract.py`

A new rule after INJ-6, evaluated only when INJ-6 did not already fire:

Fires (`guard_triggered=True`, caller emits the code-enforced `empty_set_refusal`,
model never invoked) when ALL hold:
- intent is personal, resolved subjects non-empty, and the turn is a QUESTION
  (`is_declarative=False` — statements are updates, not asks);
- not a general "what do you know about me" query (`_GENERAL_PERSONAL_RE` exempt);
- the query names a **targeted attribute** — one of `medication, allergy,
  health_condition, dietary, employer, financial` via the existing `_ATTR_KEYWORDS`
  patterns. The loose patterns are deliberately excluded: `relationship` matches any
  kinship mention ("what did we share about **Dad**"), `schedule` matches "when/time",
  `preference` matches "like/want" — including them would turn ordinary demo turns
  into structural refusals;
- **no admitted fact** carries an asked attribute; and
- **no candidate fact** carries an asked attribute for a resolved subject.

The last condition is the disclosure-preserving one: when the asked fact EXISTS for
the resolved subject but was withheld by INJ-3/INJ-5 (Sarah asking about Elena's
medication — injection-harness case 8, `expected_guard=False`), behavior is unchanged
— the turn stays on the model path and does not signal the fact's existence. INJ-6b
fires only for facts that are absent everywhere, where a code refusal can leak
nothing.

No other rule changed; no caller changed (the `process_text_query` guard branch
already handles `guard_triggered` — turn metadata, transcripts, `empty_set_refusal`).

## Tier L after Seam B (3 identical runs; baseline ratcheted to 8/8)

| id | scenario | before | after | evidence |
|---|---|---|---|---|
| E1 | statement writes ONE supersede + acknowledges | PASS | **PASS** | "Got it, Ray switched from metformin to Jardiance 10mg last week…" |
| E2 | recall retrieves the new value | PASS | **PASS** | "Ray is on Jardiance 10mg." |
| E3 | simple personal → EDGE + correct answer | PASS | **PASS** | "You take lisinopril each morning." — no cross-subject value |
| E4 | complex personal → CORE | PASS | **PASS** | tier=core, bloom 6 (declarative turn — exempt from INJ-6b by design) |
| E5 | cross-subject privacy (own facts withheld) | PASS | **PASS** | medication asked but admitted (Ray's) → INJ-6b correctly silent |
| E6 | empty-set → structural refusal | FAIL | **PASS** | `guard_triggered=True`, refusal is `empty_set_refusal()` — code path, zero model call |
| E7 | fact_history single clean chain | PASS | **PASS** | 2 nodes, 1 head, distinct values |
| E8 | idempotency (replay = no-op) | PASS | **PASS** | same head fact_id, node count unchanged |

**New ratcheted baseline** (`eval/integration_live_baseline.json`): **8/8** — all true.

## Regression battery (all green)

- Injection harness: **11/11** — including case 8 (fact-exists-but-denied stays
  guard=False) and SYM-3 (blood pressure: no targeted pattern → original INJ-6 path)
- Full 10-check gate: PASS (routing 91.3% ≥ 0.90, Tier F 17/17, S1/S2/S3, DEMO-005
  4/4 — T06's "about Dad" turn NOT over-fired thanks to the targeted-attribute
  scoping, trust agreement, E7/E8, Tier L 8/8 ratchet)
- `eval/memory_harness.py`: 17/17 (incl. MEM-100); `eval/truth_harness.py`: 6/6

## Carried forward

- Attributes without a precise keyword pattern (e.g. blood type) still rely on the
  original INJ-6 (fires when the whole admitted set is empty) or the model's prompt
  rule — extending `_TARGETED_ATTRS` safely means adding precise patterns first.
- Voice path (DIV-2) still runs no injection contract at all; INJ-6b lands there for
  free once the contract is wired on voice.
