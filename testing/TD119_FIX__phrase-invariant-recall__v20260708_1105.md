# TD-119 Fix — phrase-invariant recall of held facts
Status: BUILT
Reconciled-Against: Tier L 10/10 (E1-E8 + G2 + T119), two consecutive green runs, baseline locked 2026-07-08

## Problem

A held, contract-admitted fact ("(about Elena) Jardiance 10mg" verbatim in
model context) answered or refused depending on phrasing alone. The guard's
job is blocking UNheld details, not rationing phrasings.

## What it turned out to be — four stacked defects

1. **Prompt structure (the core defect).** Cross-subject facts rendered
   inline under "Recent context about this person (speak to them as 'you')"
   — the second-person section header beat the "(about X)" annotation.
   Offline paraphrase A/B against qwen2.5:7b: inline 9/15, natural-sentence
   values 13/15, **dedicated section 15/15**. An instruction-only fix (extra
   guard clause explaining the annotation, no restructure) was tried first
   and measurably did nothing. Fix: `other_subject_facts` param on
   `local_system_prompt` renders a "Confirmed facts about other people"
   section before the grounding guard; the guard's allowed-sections list
   names it. **Question turns only** — the first cut partitioned declarative
   turns too and broke E1's CORRECTION-RULE ack (ratchet caught it);
   declarative turns keep the proven inline annotation.
2. **"Tell me X" classified declarative** (no '?', opener unlisted) —
   skipped the grounding guard, fired write-detection on a question. Fix:
   tell/show/give/list/name/remind added to `_QUESTION_OPENER_RE`.
3. **Possessives broke entity extraction** — token "elena's" matched no
   known subject. Fix: possessive normalization in
   `_extract_named_entities`.
4. **Imperative dative "me" resolved subject to the requester** — "Tell me
   Elena's medication" resolved to [bill], the elena fact failed INJ-2
   subject scope, and the guard structurally refused a held fact. Fix:
   `_IMPERATIVE_DATIVE_STRIP_RE` before the first-person check (same idiom
   as the existing relational strip).

## Determinism

Edge text-path temperature 0.3 → 0.0: at 0.3 a held-fact answer flickered to
a refusal ~1-in-8 on marginal phrasings ("What meds does Elena take?"),
making gate and demo nondeterministic. Even at 0.0 Ollama is not strictly
deterministic under load (~1 run in 3 flickered one leg), so T119 legs are
best-of-2: the defects the scenario exists to catch (structural refusals
from resolution/injection) are deterministic and fail both attempts.

## Gate

- T119: 5-phrasing paraphrase matrix over the held Elena fact, best-of-2 per
  leg. RED pre-fix (3/5 phrasings refused), GREEN post-fix.
- E6 in the same suite still asserts the true-empty-set refusal — guard
  over-loosening cannot pass unnoticed.
- Full suite 10/10 twice consecutively; baseline locked with T119=true.
- E1 regression during development was caught by the ratchet and scoped out
  (declarative turns unchanged).

## Diagnostic method note

Every fix here was located by stage-wise instrumentation (retrieval →
resolve_subject → injection → prompt render → model), then verified offline
against the real edge model with repeated sampling BEFORE touching the gate.
The two dead ends (guard-clause-only fix; partition on declarative turns)
were both caught by measurement, not review.
