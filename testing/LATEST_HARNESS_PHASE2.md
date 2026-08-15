# Verification Harness Phase 2 — L3 guard mutation, L1 P3-P5, L4 pairwise
Status: BUILT
Reconciled-Against: full 4-layer gate on Mini 2026-07-09 — L1 5/5, L2 22/25 (3 accepted), L3 3/3, L4 1/1, RATCHET PASS

Implements spec §8 Phase 2 (HARNESS_SPEC__verification-harness__v20260709_0736):
Layer 3 guard mutation, Layer 1 invariants P3-P5, Layer 4 pairwise matrix.

## Layer 3 — Guard Integrity (mutation)

`harnesslib/inproc.py`: in-process uvicorn (thread, same app object) — the
one documented process-boundary delta (spec §4); mutations are in-memory
monkeypatches that cannot exist outside a harness run. No guard-disable
surface was added to the server. `mutate_guard(guard, mode)` context
manager; patch points:
- INJ-3: module-global rule fn (`_inj3_cross_member_deny`) — resolved at
  call time inside apply_injection_contract, so the module attr patch works.
- INJ-7/INJ-6b: inline logic — patched by wrapping the call-site binding
  `server.voice_orch.apply_injection_contract`.

Results (all 3/3 PASS):
- **INJ-7 causal both directions.** Disable → access-control string gone
  (falls to empty-set); no plaintext leak under disable (owner-scoped
  retrieval holds independently). Overtrigger → previously-answered
  maya→ray turn refused.
- **INJ-6b causal both directions.** Disable → same words, but
  guard_triggered=False — the refusal became behavioral (model path).
  Overtrigger → maya's own answered medication question refuses.
- **INJ-3 FINDING:** disable produces NO live-path change — retrieval is
  owner-scoped, so cross-member facts never reach the contract. INJ-3 is
  redundant defense-in-depth in the deny direction; live and load-bearing
  in the allow direction (overtrigger degrades own-fact answers). If
  retrieval semantics ever widen (e.g. TD-122 embedding fix), INJ-3
  becomes the only barrier and this layer detects if it fails.

## Layer 1 — P3, P4, P5

- **P3 write state integrity:** writes on member+attr keys with no seeded
  facts → exactly one active head; idempotent re-assertion keeps one head
  (settle window lets async detection expose a violation first).
- **P4 refusal correctness:** 8-cell ground-truth table — self+exists →
  value; cross-member+exists → access-control; self+not-exists →
  structural empty-set (6b-targeted attrs); cross-member+not-exists →
  access-control (existence-invariant, asserted in both directions).
- **P5 supersede integrity:** assert → land → supersede-phrased update →
  chain snapshot: old head closed (valid_to), exactly one active head with
  the new value, rows +1 exactly (no orphans/duplicates).

## Layer 4 — Retrieval Coverage (pairwise)

`eval/gen_pairwise.py` → `eval/pairwise_matrix.json`: greedy all-pairs
over the five spec §5 dimensions; 31 rows cover all 162 achievable pairs.
Constraints are recorded in the matrix header, not silently dropped:
pronoun (no discourse-context resolution), mixed / member by-relation
(TD-120 D2), retracted-this-session runtime-SKIPped where the state
matters (retract-without-successor not implemented — write kinds are
supersede/augment only); cross-member retracted rows still run because
access-control is existence-invariant. Runner orders read-only rows
before graph-mutating just-written setups.

**First-sweep catch (PW023-25):** maya's own seeded appointment (D1)
refused empty-set on every phrasing — the `appointment` attribute had no
INJ-2 relevance pattern, so lookup returned None and INJ-2 unconditionally
denied: the fact was undisclosable to its own owner. Same enumerative-
keyword-gap class as TD-120 D3. Fixed (`_ATTR_KEYWORDS["appointment"]`),
re-run 27/27 live rows PASS (4 skipped).

## Gate evidence

- Per-layer gates green on Mini after each build step, committed
  separately: L3 `7772d66`, P3-P5 `2d995e8`, L4+fix `ed56666`.
- Full 4-layer run (single invocation): L1 5/5, L2 22/25 (3 accepted
  known failures unchanged), L3 3/3, L4 1/1 — RATCHET PASS.
- Baseline now carries L1:P3-P5, L3:INJ-3/6b/7, L4:pairwise.

## Left open (Phase 3, spec §8)

- Layer 5 adversarial boundary; P6 non-fabrication (set-membership);
  gating integration (pre-commit/pre-push/pre-demo).
- Retract-without-successor unimplemented — L4 skip rows become live
  when it lands.
- Boundary mutations (spec §4 mode 3, keyword/threshold perturbation) —
  deferred; disable/overtrigger cover the causality claim.
- High-density and single-member-only fixture variants still Phase-2-
  pending in fixture.py (not needed by the layers built here).
