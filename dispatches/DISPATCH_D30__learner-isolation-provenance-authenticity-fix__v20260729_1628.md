# DISPATCH_D30 — learner-isolation provenance-authenticity fix
Status: BUILT (staged for Bill; NOT self-MET)
REQ: docs/requirements/REQ_LEARNER_SIGNAL_ISOLATION__training-signal-partition-parity-with-retrieval__v20260727_0828.md (D-28/D-29 fix spec)
Branch: roadmap
Reconciled-Against: --layer 7 green 2026-07-29 (L7 26/26, AUDIT 8/8, RATCHET PASS); battery 23/23; live resolver smoke vs 7688 (read-only)

## What was built
harness/learner_isolation.py: the gate stops trusting caller household_id/
audience and DERIVES provenance from a server-generated fact_id via an
injectable ProvenanceResolver. RegistryProvenanceResolver (production) reads
the un-forgeable chain: fact owner -> member_registry.household_id (or the
household axis); audience from visibility class -> LIVE roster tables; a
POSITIVE provenance_class=='public' marker (absent today -> carve-out fails
closed). Unprovenanced fact_id -> rejected, never carve-out.

## Holes closed (all 6 from D-25 / /tmp/d25_isolation_attack.md)
HOLE-1/3/4 (forge/omit/null household): derived from fact_id, not caller;
missing/unresolvable -> reject. HOLE-2 (audience forgery): derived from the
fact's sealed reader set. HOLE-5 (shared-base smuggle): positive public
marker, absence != admission. HOLE-6 (currency): audience bound to LIVE
roster, revoked member excluded.

## Tests
- eval/test_learner_isolation_adversarial.py: rewritten to the new contract
  (fixture resolver); all 6 xfail markers REMOVED; 23/23 real PASS.
- L7:LI1 (eval/harnesslib/layer7_crypto.py): two NEW fault twins
  (AUTHENTICITY forgery, CURRENCY revocation) + missing/unresolvable
  fail-closed; 13 sub-checks, green.
- eval/harnesslib/harness_audit.py li1_query_reword probe: updated to
  resolver contract, green.
- eval/harnesslib/check_registry.py L7:LI1 coverage: names AUTHENTICITY +
  CURRENCY regions and the honestly-uncovered slice.

## Discipline Four: all four present (twins, fixture, coverage, metamorphic).

## Honest NOT-MET items (Bill's call)
1. --full NOT run (memory ~80MB free < TD-129 threshold; would SIGKILL).
   Deferred to a clean window. Change is a pure-function gate + test wiring.
2. Live resolver smoke vs 7688: resolves owner=='household' facts correctly
   (household + live circle audience) and fails closed on a fake fact_id;
   member-owned facts resolve to household=None because members.household_id
   is UNPOPULATED on this graph — fail-closed (safe), but a DATA prerequisite
   for production member-scoped training, not a gate-logic defect. Named as
   an uncovered slice in the coverage entry.

## No self-MET. REQ stays NOT MET; the 6 holes are closed at the logic level
and cannot silently regress (battery + L7:LI1 twins fail loudly).
