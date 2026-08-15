# Verification Harness — Phase 1 build
Status: BUILT
Reconciled-Against: full run 2026-07-09, L1 2/2 + L2 20/25 (3 accepted known failures, 2 known-flaky), baseline recorded

Implements Phase 1 of docs/testing/LATEST_HARNESS_SPEC.md: fixture manager,
reporter, Layer 2 (demo regression), Layer 1 invariants P1 + P2.

## What was built

- `eval/harness.py` — entry point (--layer, --seed, --iterations, --script,
  --record-expected, --update-baseline --accept).
- `eval/harnesslib/server.py` — harness-owned server lifecycle on port 7997
  (spec amendment 2), refusal classifier (access_control vs empty_set).
- `eval/harnesslib/fixture.py` — reset/seed variants (standard, empty; the
  rest Phase 2), seed-drift verification, assert_fact_state() with decrypt.
  Mirrors demo_seed D1-D9 plaintext for leak assertions.
- `eval/harnesslib/reporter.py` — PASS/FAIL/SKIP/FLAKE, baseline ratchet
  with exit codes 0/1/2, --accept justification requirement, trend file
  (logs/harness_trend.jsonl), results JSON.
- `eval/harnesslib/layer2.py` — demo scripts as test inputs; hash-paired
  *_expected.json with required/must_not/refusal/tier/graph assertions;
  honors the script's own pause_ms (the demo's timing IS part of its
  contract); graph asserts poll to the 20s detection ceiling; --record mode
  emits skeletons that FAIL until human-reviewed.
- `eval/harnesslib/layer1.py` — P1 member isolation (seeded RNG over
  member-pairs x seeded facts x phrasing templates; member-personal targets
  demand the access-control refusal, care-recipient targets demand no-leak),
  P2 owner retrieval (write + paraphrase read-back; retry-once = FLAKE).
  One baseline scenario per invariant (any iteration failure = invariant RED).

## First-sweep results (the layer paying for itself on day one)

- L1:P1 PASS — 20 iterations, zero leaks, zero wrong refusal types.
- L1:P2 PASS — all write+read cycles, all paraphrases.
- L2 caught, on its first recording pass:
  1. care_coordination.T04 cannot fire: speaker "sarah" absent from the
     live member registry (400) — script/registry mismatch (register note).
  2. three_zone_demo.T01: ack says "YOU take metformin" to Maya about Ray
     even when the write lands subject=ray (TD-115 related).
  3. TD-121 (new): Groq extraction nondeterminism — the T04 supersede
     sometimes never lands while the ack claims it did. Quarantined
     _known_flaky; the ack-asserts-unlanded-write case is the demo-credibility
     hazard.
  4. A false alarm avoided: T05's "stale value" was the harness ignoring
     pause_ms; honoring script pacing resolved it (and the pacing dependency
     is now explicit — see TD-121 candidate fixes).
- care_coordination.T02 (TD-120 D2, relational recall) pinned as a known
  failure until the relationship-write fix lands.

## Baseline

`eval/harness_baseline.json`: 24 passing scenarios, 3 accepted known
failures (justifications in _accepted), 2 _known_flaky (TD-121). Exit 2 on
any failure not in this file.

## Phase 2 next (per spec §8)
Layer 3 guard mutation (INJ-3/6b/7, in-process server), P3-P5, Layer 4
pairwise matrix. Fixture variants high-density + single-member-only.
