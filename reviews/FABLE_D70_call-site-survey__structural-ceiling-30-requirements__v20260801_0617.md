# FABLE_D70_call-site-survey — Structural Ceiling, Implementing Call Sites

Reviewer: Fable
Dispatch: D-70 (step 5)
Subject: which of `REQ_STRUCTURAL_CEILING`'s 30 requirements had an implementing
call site at the time of survey; grouped as none / partial / contradicted.
Read against: `REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260731_2057.md`
and the codebase at **HEAD 98dfb7a**.
Version: v20260801_0617 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED
Verification: UNVERIFIED
Date: 2026-08-01 (banked); survey produced 2026-07-31

**Captured verbatim as produced, banked unedited.** Banked under D-77 because it
is a named input to `REQ_CEILING_ACCEPTANCE` and had been left in `/tmp`, outside
the repo's provenance record — the same gap D-60 closed for research pass 3.

**STALE IN ONE KNOWN RESPECT, flagged rather than silently corrected.** The
survey was taken at `98dfb7a`, BEFORE D-75 implemented R29/R30. Its A29/A30
assessment ("R29 worse than absent: three divergent encodings") is no longer
current — the registry landed at `d50225e`, R29 was ruled MET and R30 NOT MET on
2026-08-01. `REQ_CEILING_ACCEPTANCE` re-verified every row against HEAD rather
than inheriting this survey's conclusions, and where the two disagree the
re-verification governs. Everything else in the survey was re-confirmed still
accurate at `112841a`.

---

# D-70 step 5 — implementing call sites for REQ_STRUCTURAL_CEILING's 30 requirements

Read-only survey at HEAD 98dfb7a. Nothing built, no status proposed.

**Headline: 21 of 30 have no implementing call site. 7 are partial. 2 are actively
contradicted by shipped behaviour.** That distribution is normal for a REQ filed with
acceptance not run — but the two contradicted ones are worth separating out, because
they are not "unbuilt," they are "built the other way."

---

## GROUP A — NO IMPLEMENTING CALL SITE (21)

Nothing in the codebase does this today, in either direction.

**Axis 4, inferential reach (6):** R2 typed inference permit · R3 prohibited autonomous
labels · R4 cognition rule · R6 no inference from absence · R7 transient reasoning does
not create durable authority · R9 hard-refused graph representations.

R7 is *vacuously* satisfied today — no path persists transient model reasoning — but
nothing enforces it, so it holds by absence rather than by control.

**Axis 3, audience (3):** R11 outbound propagation cap · R13 three objects not one ·
R15 personal-representative and caregiver conflict control.

R14 (care-team projection) also has none, and is *deliberately* deferred — see the
filed R14 text.

**Axis 2, retention (5):** R17 separately erasable active artifacts · R19 embeddings,
summaries and indexes as governed derivatives · R21 retention clock formula · R22
backup state disclosed honestly · plus the cascade half of R18 (see Group B).

R17 is the sharpest: the only hard delete in the entire codebase is
`server/demo_dashboard.py:1890` `MATCH (f:Fact) DETACH DELETE f` — nuke-the-graph,
demo reset. There is no per-fact, per-member, per-category or per-age delete anywhere.

**Axis 5, solicitation (5):** R23 purpose-trigger registry · R24 one system-initiated
offer per material circumstance · R25 no adaptive persuasion · R27 grant metrics cannot
be optimization targets · R28 cumulative authority manifest.

This axis is uniformly unbuilt, which is expected — it was the fifth axis added by the
ChatGPT pass and never scoped against code.

**Sensitivity registry (2):** R29 single source of truth · R30 migration and fail-closed
behaviour.

R29 is worse than absent: **three divergent encodings exist** and disagree
(`extraction_queue.py:95` four-valued; `curator_shadow.py:95` and `hipconfig.py:30`
both three-valued, each mis-ranking `critical` in a different direction). That is
TD-137, still OPEN pending a ruling on which is authoritative.

---

## GROUP B — PARTIAL (7)

A call site exists and does part of the job.

| R | What exists | What is missing |
|---|---|---|
| **R1** versioned attribute registries | `CANONICAL_ATTRIBUTES` (`extraction_queue.py:122-159`), 17 attributes, refused off-enum at `:229` and `:903` | No versioning at all; enforced on the **extraction path only** — `store.py::encode` does not re-validate and `consolidate.py` never checks a derived attribute |
| **R5** no self-expanding inference | `consolidate.py:435` — derived facts are always `confidence='low'` and can only harden via human confirmation | Caps trust expansion only. Nothing prevents a sensitive hypothesis expanding follow-up questions, audience, permits or retention |
| **R8** write-time representation class | `harness/write_rule.py::classify` exists (REQ_WRITE_TIME_CLASSIFIER) | No `UNKNOWN_HIGH_RISK` fail-closed class; representation validity is not a write precondition |
| **R10** category controls by origin | The `risk_pattern` precedent — deliberately outside `CANONICAL_ATTRIBUTES` so only derivation can emit it (Bill, 2026-07-17, REQ_D21_D23) | Exactly one instance, enforced by *omission from an enum* rather than by an origin check. No general mechanism |
| **R18** derivation lineage and cascade | `derived_from` is written on every derived fact (`consolidate.py:525`) | **The cascade half does not exist.** `derived_from` is never read for invalidation — retracting a source leaves its derived child standing |
| **R20** production data excluded from training | `harness/learner_isolation.py::check_training_example` — a real, MET gate that routes every training example | Governs the *learner* path only. No general "production data excluded from evaluation corpora by default" control |
| **R26** decline and non-response close the circumstance | `confirmation_gate.apply_decline` — a genuine per-item no-cost refusal | Decline is recorded but does not close a *circumstance*; nothing prevents re-approach, and non-response is not modelled at all |

---

## GROUP C — CONTRADICTED BY SHIPPED BEHAVIOUR (2)

Not unbuilt. Built the other way. These need a ruling, not a build ticket.

**R12 — inbound author cap.** The requirement is that an author requesting subject
context receives only their own contribution and permitted receipt, with corroboration,
derivatives and profile absent. **INJ-3's first permit does the opposite:**
`fact.owner == requester` — *"owner reads any fact they stored (any subject)"*
(`injection_contract.py:508-509`). The author retains standing read access, and because
they hold the DEK wrap, removing it is a re-encryption rather than a policy edit. The
filed REQ already names this at its own "NAMED LIMIT — author keeps their own
ciphertext," so the conflict is acknowledged in-document; what is not resolved is that
R12's acceptance (A12) cannot pass against current behaviour.

**R16 — personal data stay off the immutable ledger.** The ledger deliberately *does*
carry member-actor personal payloads, AES-256-GCM encrypted, with **crypto-shredding as
the designed erasure path** (`epistemic_ledger.py:13-18`). That is a shipped, deliberate
architecture decision — erasure by key destruction rather than by absence. R16 asks for
absence. Both cannot hold; this is a genuine design conflict between tamper-evidence and
erasure, and it is the same structural tension D-63 flagged on the retention axis.

---

## What this means for the acceptance

30 acceptance rows exist. Given the above, **A11-A19 and A23-A28 cannot be run at all
today** — no call site to exercise. A12 and A16 would additionally *fail* against
current behaviour rather than being merely unrunnable.

The three requirements with the most real substrate to build on are R18 (lineage exists,
cascade missing — smallest concrete fix), R20 (a MET gate already generalizable), and
R10 (a ratified precedent to extend rather than a mechanism to invent).

Nothing built. No status proposed.
