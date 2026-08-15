# REQ_ASKED_ATTRIBUTE_COVERAGE — structural refusal for untargeted attributes
Status: NOT MET
Reconciled-Against: roadmap 32cb04f (REQ_STRUCTURAL_REFUSAL MET at D-128; TD-149 filed at
D-127 ruling e)
Filed: 2026-08-03 (D-129, Bill's ruling c)
Decision-Owner: Bill
Related: REQ_STRUCTURAL_REFUSAL (MET — the same class of gap, closed there for TARGETED
attributes only), TD-149 (the scoped debt this governs), TD-136 (adjacent, its own filing),
REQ_RECORD_GRADED_REFUSAL (the assertion substrate)

## THE REQUIREMENT

Bill's ruling, 2026-08-03 (D-129 c), verbatim:

> Untargeted attributes having no structural path is the same class of gap the now-MET REQ
> just closed for targeted ones — appointment, preference and schedule are deliberately
> outside the target list, and a member asking about those on a non-member subject has no
> structural refusal available.

The requirement: the structural-refusal guarantee REQ_STRUCTURAL_REFUSAL established —
a refusal for an unauthorized subject comes from a structural path, not the model
declining — SHALL extend to attributes outside `_TARGETED_ATTRS`.

## WHAT'S ALREADY DONE

- REQ_STRUCTURAL_REFUSAL (MET, D-128): graph-wide Phase-3 resolution; INJ-6b keyed on the
  admitted set; deny-silently by refusal identity; INJ-7 and owner reads proven untouched.
  All of it holds for the twelve `_TARGETED_ATTRS` only.
- INJ-6 (subject-level) fires when NOTHING about the resolved subject is admitted — so the
  untargeted gap bites exactly when some same-subject fact IS admitted (e.g. a household-
  owned fact about the subject, PW014/PW017's shape) and the asked attribute is untargeted.
- TD-149 scopes the widening path: derive `asked` from the router's SIO attribute
  classification (`classify_sio` already computes `sio.attribute` upstream) instead of
  keyword regexes.

## WHAT'S KNOWN BROKEN

- `_TARGETED_ATTRS` excludes appointment/preference/schedule (and every other loose-keyword
  attribute) by documented over-fire rationale (`harness/injection_contract.py:272`) — the
  exclusion is correct FOR KEYWORD REGEXES and is exactly what SIO classification would
  obsolete.
- PW014 (sam→dad/appointment) and PW017 (sam→dad/preference) are protected only by the
  model choosing, with resolved subjects and admitted adjacent facts — measured at D-124,
  re-confirmed by D-126/D-127's runs (their `no_leak` rows pass on needle-absence, not on
  structural refusal).

## THE ACCEPTANCE TEST (sketch — the executing dispatch refines, the shape is fixed)

1. SIO-derived `asked`: for turns where `sio_source != "fallback"`, the asked attribute
   comes from the SIO classification, mapped through `_attribute_family` parity; keyword
   regexes remain the fallback path (`sio_source == "fallback"` keeps today's behavior
   exactly — no regression surface on degraded turns).
2. An untargeted-attribute query about a resolved, unauthorized subject refuses
   STRUCTURALLY: new L4 rows for the PW014/PW017 shape asserting on the record
   (`guard_triggered=True`, structural kind, `inference_ms=None`), graded per
   REQ_RECORD_GRADED_REFUSAL.
3. NO OVER-FIRE: the :272 rationale is honored by evidence, not hope — a battery of
   ordinary demo turns that merely MENTION kinship/schedule/preference words (the
   documented false-fire shapes) must keep their current outcomes; a fault twin
   demonstrates that keyword-widening (the rejected approach) WOULD over-fire on at least
   one of them, proving SIO-derivation is load-bearing.
4. Owner reads and INJ-7 unchanged (the REQ_STRUCTURAL_REFUSAL non-regression set re-run);
   deny-silently identity holds for untargeted attributes exactly as for targeted.
5. Full RATCHET green per CLAUDE.md item 12; CTX-STRIP and PSA1 individually.

## CONSTRAINTS

- Structural fix only — model behavior satisfies nothing here.
- `sio_source == "fallback"` turns keep today's keyword behavior byte-for-byte.
- The SIO's attribute-classification reliability against the L4 phrasings must be measured
  BEFORE the guard consumes it (a misclassifying SIO turns over-fire into a new defect
  class); if reliability is insufficient, STOP AND REPORT — the fix shape changes.
- TD-136's household-exemption question is adjacent and stays out of scope.

## STATUS

**NOT MET. Filed per Bill's D-129 ruling (c); not built; not self-ruled.** The build does
not start until an executing dispatch names this REQ (CLAUDE.md item 8).
