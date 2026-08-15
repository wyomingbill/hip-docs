# REQ_HARNESS_DISCIPLINE: Four-Part Check Standard and Sprint Gate
Status: MET
Branch: roadmap
Reconciled-Against: 97448c0 (working tree additionally carries uncommitted OB5/G0-adjacent changes to eval/harnesslib/layer7_crypto.py, harness/encryption.py, harness/identity_keys.py, harness/member_seal_keys.py, and the REQ_CRYPTO_P3 doc — untouched by this REQ); REQ_G0_OUTPUT_INVARIANT__output-side-fabrication-backstop__v20260726_0735.md; REQ_CRYPTO_P3_OPERATOR_BLIND__stage4-phase3__v20260724_1129.md (OB4/OB5 as the fault-twin pattern's reference cases); docs/techdebt/ register (TD-132, TD-122 named below); d83a111 (blocking condition cleared — REQ_GROQ_CALL_RESILIENCE MET, see UPDATE below)

## UPDATE 2026-07-26 (MET)

This REQ's own bar, stated in its CONSTRAINTS section, was the full ratchet
(CLAUDE.md item 12) staying green — it was blocked only by the
`care_coordination.T01`/`T02` Groq 400 (`json_validate_failed` via
reasoning-token overrun on gpt-oss-20b, root-caused in
DISPATCH_GROQ_400_ROOTCAUSE, fixed under REQ_GROQ_CALL_RESILIENCE at d83a111).
That blocker is now cleared.

`python -m eval.harness --full` at d83a111 ([REDACTED-USER]@[REDACTED-MACHINE-NAME],
roadmap, foreground): RATCHET PASS. AUDIT 3/3 (0 missing artifacts, 46
debt-flagged gaps — TD-133's own honest-gap register, printed not hidden).
`care_coordination.T01`/`T02` both PASS. The four-part standard's own
mechanical enforcement (`AUDIT:four-part-roster` + probes + fault-injection,
wired into every `--full`) ran clean; the reference-implementation checks
(PS1/PS2/OB4/OB5/G0/G1/G4 successors, per REQ_CRYPTO_P3's PS1-4 retirement
and OB6's introduction) all pass their four columns per the AUDIT roster.

One pre-existing, unrelated flake observed in this run: L1:P2 (owner
retrieval), iteration i019, an async-write-timing race — same class as the
previously-diagnosed R04/PW012/HARNESS1.3 flakiness, already traced away from
crypto/audit work in REQ_CRYPTO_P3's own report. Not a new regression (RATCHET
PASS confirms no scenario regressed vs baseline) and not in scope for this REQ.

REQ_HARNESS_DISCIPLINE: MET.

REQ only, no code. This REQ scopes the standard; nothing is built by this filing.

## THE REQUIREMENT

Bill's words, verbatim:

> the standard every check in the harness must meet before it counts as MET. No check ships without all four:
>
> 1. FAULT-INJECTION TWIN — a deliberately constructed violation that turns the check red on command, green on removal. A check never shown to fail proves nothing. (Pattern exists: OB4's static scan fired against consolidate.py; PS1/PS2/OB5/G0 all have this.)
> 2. GROUND-TRUTH FIXTURE — the expected answer is human-verified, not model-graded alone. A teacher model may assist ranking; it may not be the sole oracle. (Pattern exists: alice/bob/mary.)
> 3. COVERAGE ENTRY — the check declares what slice of the authorization state space it covers (which roles, scopes, attribute-taxonomy splits, intent classes), so untested regions are visible, not invisible.
> 4. METAMORPHIC WRAPPER — where the check tests a decision, meaning-preserving rewordings must not change it. (Pattern exists: MT1/MT2.)
>
> STANDING RULE (the point of this REQ): these four are re-asserted at the START of every sprint, not rediscovered per feature. A new check merged without its twin, fixture, coverage entry, and metamorphic wrapper is a FAIL of this REQ regardless of what it tests.
>
> WHY: harness discipline gets forgotten at sprint start; this REQ makes the standard a gate, not a memory.

Expanded: this REQ governs the harness itself, not any feature the harness tests. Its
subject is second-order — the checks that check the system. "MET" for any future check
means the check plus its four artifacts, and the audit script below is the mechanical
enforcement so the standard survives sprint boundaries without relying on anyone
remembering it.

## THE ACCEPTANCE TEST

DEMONSTRATION OBJECTIVE: 4-part. Each part passes or fails, no judgment calls:

1. An audit script lists every layer-7 check and flags any missing one of the four
   (fault-injection twin, ground-truth fixture, coverage entry, metamorphic wrapper).
   Observable: run the script, get a complete roster with a four-column status per
   check; a check absent from the roster is itself a FAIL of the audit.
2. The audit runs on `--full` and reports coverage gaps. Observable: `python -m
   eval.harness --full` output contains the audit's gap report; the audit running
   only when hand-invoked does not satisfy this part (same standing-invariant standard
   OB4/OB5 already meet — wired into every run, not a one-time grep).
3. A check added without a fault-twin is rejected by the audit. Observable: add a
   synthetic twin-less check, run the audit, see it flagged as a violation (red); remove
   the synthetic check, audit goes green. This is the audit's own fault-injection twin —
   the standard applies to its enforcer.
4. The existing hard-zero checks (PS1/PS2/OB4/OB5/G0/G1/G4) pass the audit as
   reference implementations. Observable: all seven appear in the roster with all four
   columns satisfied. If any of the seven fails a column, that is a real gap to close
   before this REQ is MET — not an exemption to grandfather in.

## WHAT'S ALREADY DONE

Verified working pieces this build must NOT redo — these are the patterns the standard
generalizes, each already live:

- Fault-injection twin pattern: OB4's static scan fired against a real violation
  (consolidate.py, 2026-07-21) before its fault-injection probes were formalized;
  PS1-PS4 each carry a named fault-injection (reopen a derivation site, seal a DEK to
  master — both must go red); OB5 probes a disposable tempdir key path via
  $HIP_MASTER_KEY override; G0's harness scenario includes fault-injection
  red-on-command with `--accept` mechanically refused. Verified: Layer 7 RATCHET PASS
  runs at 2781715 (OB4), the 2026-07-24 OB5 evidence run, and REQ_G0's acceptance
  items 3-4.
- Ground-truth fixture pattern: the alice/bob/mary fixtures — human-verified expected
  answers, not model-graded.
- Metamorphic pattern: MT1/MT2 (MT2-DECRYPT-REVOKE turned from NAMED-PENDING skip to
  real PASS under REQ_CRYPTO_P4, commits d0562d1/acbe2dc/80f7021).
- Hard-zero tier mechanics: the ABSOLUTE tier with `--accept` mechanically refused
  already exists (layer7_crypto_v2.py's ABSOLUTE-tier bullets; G0 joined it under
  REQ_G0). The audit's rejection semantics (part 3) should reuse this mechanism, not
  invent a parallel one.

## WHAT'S KNOWN BROKEN

The gaps this REQ exists to close, named:

- Not every check has a fault-twin today. The pattern exists (see above) but is not
  universal, and nothing enforces it on a newly merged check.
- The oracle is model-graded in places — who grades the teacher? A teacher model may
  assist ranking; where it is currently the sole oracle, that check fails standard #2.
- No coverage metric exists. No check today declares which slice of the authorization
  state space (roles, scopes, attribute-taxonomy splits, intent classes) it covers, so
  untested regions are invisible rather than visible.
- Metamorphic runs on the demo script only, not all checks. MT1/MT2 exist but the
  wrapper is not applied wherever a check tests a decision.
- Named limits that STAY OPEN on the register, not closed by this REQ: TD-132
  (paraphrase evades canary) and TD-122 (embeddings null). World-class is zero HIDDEN
  gaps, not zero gaps — this REQ's job is making every gap visible and gated, and these
  two are the honest examples of visible, registered, still-open gaps.

## CONSTRAINTS

- The existing Layer 7 RATCHET must not regress: currently green (RATCHET PASS
  verified this session, 2026-07-26). The audit is additive — it must not change any
  existing check's pass/fail behavior, only report on and gate the checks themselves.
- Hard-zero semantics are sacred: G0/G1/G4 (and PS1/PS2/OB4/OB5) stay never-baselinable,
  never config-gated. The audit must not introduce a path that lets a hard-zero check be
  accepted or skipped.
- No new model calls in the audit itself — it is a static/structural check over the
  harness, same discipline as G0's no-new-model-calls constraint.
- The standing rule is part of the requirement, not commentary: re-assertion at sprint
  START. A sprint that begins without the audit green (or its gaps explicitly registered
  as debt with IDs) is a FAIL of this REQ regardless of what the sprint builds.
- Per Requirements Discipline item 8, no code for this REQ starts until a dispatch
  names this doc.
