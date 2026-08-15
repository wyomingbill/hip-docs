# DISPATCH_R24_SURVEY
Status: BUILT
Reconciled-Against: see HASH

**TYPE:** ANALYSIS (survey only — item 1's own STOP condition fired; items 2/3's build was
never reached, per the dispatch's own instruction)

**REQ:** NONE. Analysis dispatch, no code changed, nothing built — Requirements Discipline
item 10's carve-out applies plainly: this dispatch traced whether R24 has anything to build
against and found it does not; there is nothing to file a build REQ for.

## THE ASK

Dispatch text, verbatim:

```
=== D-150 | ~/hip-roadmap, roadmap | R24: one offer per circumstance ===
STANDARD PREAMBLE. Lane A.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R24.

1. SURVEY FIRST, report before building: R24's text as filed, every place the system
   currently initiates an offer or request for expanded access, and what state exists
   today to tell one circumstance from another. STOP AND REPORT if no notion of a
   material circumstance exists — that is R23's vocabulary and may block this.
2. THEN BUILD what can be built honestly. Absent pieces stay absent and are asserted
   absent by a standing test.
3. Acceptance per D-87: executed fault twin, anti-vacuity. Report whether A24 becomes
   writable. Do not re-tier.
4. Rule nothing MET.
```

## WHAT WAS DONE

1. Gate checked — matched. Repo lock acquired via `scripts/hip_lock.py with repo` before
   reading anything, held for the dispatch's duration.
2. Read R24's full text (`:782-801`), R23 immediately before it (`:764-780`, the
   `PURPOSE_TRIGGER` vocabulary R24's own `material_circumstance_version` field belongs to),
   and R25-R27 (`:803-845`) for the surrounding axis's shape.
3. Confirmed R24 sits under `## 8. AXIS 5 — SOLICITATION GOVERNANCE` (`:754`), alongside R23,
   R25, R26, R27.
4. Searched the full tree for any `PURPOSE_TRIGGER`/`purpose_trigger`/`material_circumstance`
   symbol, any offer-initiation function (`def.*offer`, `SYSTEM_OFFER`, `initiate_offer`,
   `solicit`), and any proactive "would you like to enable..." style prompt language anywhere
   in `server/`, `harness/`, `memory_engine/`, `scripts/` — zero hits, all searches.
5. Read `REQ_CEILING_ACCEPTANCE`'s own A23/A24 rows and its tier table, and found the
   acceptance document ITSELF already states the identical finding at filing time (quoted
   below) — this dispatch's live re-verification CONFIRMS that prior note rather than
   discovering something new, and says so rather than presenting it as a fresh finding.
6. Read `eval/test_ceiling_solicitation.py` in full to establish precisely what IS built in
   this axis (A26/A27 only) before concluding R24 has nothing, so the STOP is against a
   complete picture of the axis, not an assumption.
7. Traced `apply_decline` (the one real function `test_ceiling_solicitation.py`'s own
   docstring cites for R26) to `harness/confirmation_gate.py` and read its module docstring —
   confirmed it is the P8 write-confirmation gate (a member confirming or declining a PARKED
   FACT WRITE), a different, adjacent mechanism from R24/R26's "decline a system-initiated
   offer to expand access" — the SAME distinction `test_ceiling_solicitation.py` already draws
   carefully, re-confirmed rather than assumed.
8. **STOPPED per the dispatch's own explicit condition** — did not proceed to item 2 (build).
9. Wrote this dispatch doc. No code touched anywhere.
10. Released the lock (no commit needed beyond this doc — see HASH).

## WHAT WAS FOUND

### R24's text (item 1)

`docs/requirements/REQ_STRUCTURAL_CEILING__...:782-801`. For each `(member, purpose_id,
material_circumstance_version)` tuple, HIP may present **at most one** system-initiated offer;
no automated reminder, rephrased retry, adjacent-offer sequence, or caregiver-mediated retry
for the same circumstance; a new offer requires either the member affirmatively reopening the
purpose, or a genuine material-circumstance-version change (newly enabled care function, new
clinician-authored care plan, changed legal role, a qualifying event from a validated sensing
contract — explicitly NOT continued engagement, another grant's acceptance, time alone, or
operator desire for more data). "This is the offer-rate ceiling. It does not require an
invented per-day or per-month number."

### Every offer-initiation site in the system (item 1) — none exist

Full-tree search for any code that proactively initiates an offer or request for expanded
access: **zero matches**, across every search shape tried (function names, the
`PURPOSE_TRIGGER`/`purpose_trigger` symbol, `material_circumstance`, prompt-template language
resembling an upsell). HIP today is reactive only — every code path this session has read
across D-130 through D-149 (retrieval, disclosure, the injection contract, the confirmation
gate, the frontier tier's own escalation) answers a member's own turn; none of them proposes
that a member grant something new.

### What state exists today to tell one circumstance from another (item 1) — none

**R23's own PURPOSE_TRIGGER vocabulary — the thing R24's `material_circumstance_version` field
belongs to — does not exist anywhere in the codebase.** Confirmed by direct search (matching
this dispatch's own live re-verification) AND by `REQ_CEILING_ACCEPTANCE`'s own A23 row, which
already recorded the identical finding at filing time, quoted verbatim: **"Axis 5 is wholly
unbuilt — verified no `purpose_trigger` / `offer_circumstance` / `solicitation` symbol
exists."** A24 sits in the UNWRITABLE tier (`REQ_CEILING_ACCEPTANCE__...:47`, among
`A22–A25`). This dispatch's contribution is CONFIRMING that prior note still holds today, not
discovering it fresh — stated as such rather than presented as new.

**The one real piece of code anywhere near this axis, R26's `apply_decline`
(`harness/confirmation_gate.py`), is a DIFFERENT mechanism** — it resolves a member's yes/no
response to a PARKED FACT WRITE (the P8 cross-principal trust-monotonicity gate this session
traced in D-147's MEM-118 investigation), not a response to a system-initiated offer to expand
access. `eval/test_ceiling_solicitation.py`'s own docstring already draws this distinction
carefully ("R26 covers decline AND non-response. `apply_decline` exists, so the decline... no
adverse-inference surface whose absence could be asserted") — re-confirmed by reading the
function directly, not re-derived.

### STOP fired (item 1's own condition)

**"STOP AND REPORT if no notion of a material circumstance exists — that is R23's vocabulary
and may block this."** No notion of a material circumstance exists, confirmed by direct search
and by R23's own already-recorded finding. **This dispatch stops here, per its own explicit
instruction — item 2 (build) was not reached.**

A narrower question was considered and rejected: could R24's own dedup LOGIC (a function
gating "has this exact tuple already had an offer?") be built in isolation, taking opaque
`purpose_id`/`circumstance_version` strings with no registry behind them? Rejected, not
attempted: with no `PURPOSE_TRIGGER` registry to validate those identifiers against and no
offer-issuing code path anywhere to call it, such a function would enforce nothing (there is
nothing for it to gate) and would assert a contract for inputs (`purpose_id`,
`material_circumstance_version`) that R23 has not yet defined. Building it would risk being
read as "R24 has a working piece" when the feature it governs does not exist at all — exactly
the "invented mechanism worse than an absent one" this dispatch series has repeatedly avoided
(R2/D-130's `purpose_id`, `retention_policy`; R8/D-140's three absent classes).

### A24's writability (item 3)

**A24 does NOT become writable.** It remains UNWRITABLE, for the identical reason A23 is
UNWRITABLE — R23's vocabulary, which A24 depends on by name (`material_circumstance_version`
is R23's own field), does not exist. Nothing changed this dispatch to alter that. Not
re-tiered — nothing was built to justify re-tiering, so the question does not arise.

## VERIFIED

**Watched run:** every claim above is a direct read or a direct grep executed this dispatch,
not recalled — the `PURPOSE_TRIGGER`/offer-initiation searches were run against the live tree;
`REQ_CEILING_ACCEPTANCE`'s A23 row and tier table were read directly;
`eval/test_ceiling_solicitation.py` and `harness/confirmation_gate.py` were read in full, not
excerpted from memory.

**Reasoned about:** that NO offer-initiation mechanism exists ANYWHERE is a negative claim —
supported by an exhaustive-as-practical search (multiple search shapes, the full `server/`/
`harness/`/`memory_engine/`/`scripts/` tree) but, like any absence claim, not provable by
enumeration alone. Stated with the search terms named so a future session can extend or
re-run it rather than trust the conclusion blind.

## HASH

**NONE.** No code changed, no REQ filed, nothing built. This dispatch doc is the only new
file; committed on its own, docs-only.

## OPEN

- **R23 needs to build first.** R24 (and R25, both UNWRITABLE for the same reason) cannot
  proceed until a `PURPOSE_TRIGGER` registry exists — a versioned entry naming `purpose_id`,
  `required_capability`, the requested representation classes/audience/retention/inference
  permits, and a `material_circumstance_version`. That is a separate, larger build (R23's own
  dispatch), not started here.
- **The isolated-dedup-function option was considered and explicitly rejected**, not merely
  unconsidered — reasoning recorded above so a future dispatch does not re-litigate it without
  the context of why it was declined.
- **Nothing ruled**, per instruction.
