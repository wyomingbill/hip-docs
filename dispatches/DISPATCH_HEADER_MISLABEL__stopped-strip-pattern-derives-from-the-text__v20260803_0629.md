# DISPATCH_HEADER_MISLABEL
Status: BUILT (as an analysis; STOPPED before any change, per the dispatch's
own condition)
Reconciled-Against: 2026-08-03 (D-115; parent 14811f3 at dispatch time)

**TYPE:** ANALYSIS

**REQ:** **NONE** — the dispatch's step 3 (the rename) was conditional on the
survey coming back clean; the survey's STOP condition fired, so no build
occurred and no REQ gate arises. The rename, when Bill rules it, sits under
REQ_STRIP_CONTEXT_COMPLETENESS (the strip derivation) and touches a
check_registry ground-truth pin that carries Bill's own D-28 wording.

## THE ASK

> 1. D-114 flagged this and left it open. The prompt header reads "Confirmed
>    facts about other people" but now sits over lines that can carry
>    asserted/unconfirmed markers. ONE PROMPT CAN SAY BOTH.
> 2. SURVEY FIRST: (a) every place that literal appears; (b) whether the
>    strip pattern derives FROM the header text or merely matches it — if it
>    derives, a rename changes what gets stripped, and that is a governance
>    change, not a wording change; (c) what the header should say instead —
>    propose wording; do not invent it silently.
>    STOP AND REPORT if the strip pattern derives from the text. That is a
>    bigger change than a rename and Bill rules it.
> 3. THEN CHANGE IT if the survey is clean: the constant, the derivation, and
>    the registry pin in one edit.
> [4-5: acceptance + harness, conditional on the change]
> 6. Rule nothing MET.

## WHAT WAS FOUND — the STOP fired at 2b

**(2b) THE STRIP PATTERN DERIVES FROM THE HEADER TEXT — decisively, not
arguably.** `_personal_section_pattern()` (`harness/orchestrator.py:756-778`)
builds its regex **fresh on every call** from `FACT_BEARING_SECTION_HEADERS`
— `re.escape(h) for h in FACT_BEARING_SECTION_HEADERS` — and that tuple
contains `SECTION_OTHER_PEOPLE`'s literal text (`:185`). The header string IS
the match source. This is the D-28 design, deliberately: the old hand-written
regex named two of three headers and the third escaped stripping entirely.
Per the dispatch's own condition: STOPPED, nothing changed, Bill rules.

**(2a) Every place the literal appears — SEVEN, not the three the dispatch
named:**
1. `harness/orchestrator.py:185` — the constant (render AND strip both
   source from here).
2. `harness/orchestrator.py:129` — **a second, uncontrolled copy inside
   PERSONAL_FACT_GROUNDING_GUARD's prose** ("...listed under ... /
   'Confirmed facts about other people' above"). Hardcoded, does NOT read
   the constant. Any rename must move this too or the guard names a header
   that no longer exists — a FOURTH member of the dispatch's
   "constant + derivation + pin move together", and already a one-source
   violation on its own.
3. `eval/harnesslib/check_registry.py:388` — the CTX-STRIP roster's
   GROUND-TRUTH FIXTURE pin, and its own comment raises the stakes: the
   pinned text is *"the exact human-verified (Bill's own words, the
   dispatch that opened D-28) header text"*. **The header wording is a
   ruled artifact.** Renaming it revises Bill's D-28 wording — a second,
   independent reason this is Bill's call, beyond the derivation.
4-6. `harness/orchestrator.py:174, :429, :770` — comments/docstrings
   (historical references, low stakes, should move with a rename for
   hygiene).
7. `logs/harness_results.json` — stored prompts from past runs. Inert
   history; nothing re-reads it for stripping.

**The closed-loop nuance, reported for the ruling (this is why the rename
is SAFER than the STOP condition's worst case, but still Bill's):**
render and strip source the SAME constant — `local_system_prompt()` writes
the header from `SECTION_OTHER_PEOPLE` and `_personal_section_pattern()`
matches from the same tuple, rebuilt per call. A rename therefore moves
both TOGETHER by construction: every future prompt renders the new header
and strips on the new header. All four live `strip_context_for_tier`
callers (`server/voice_orch.py:1825,1902,1986,3283`) strip freshly built
messages in the same turn; nothing anywhere re-strips a stored prompt. So
"what gets stripped" is behaviorally unchanged for all future traffic —
the governance risk the STOP names is real in general but bounded here by
the D-28 single-source design. The residual risks are exactly the pin
(:388 — goes red on mismatch already, which is the loud direction) and
the guard's second copy (:129 — silent if missed, the actual hazard).

**(2c) Proposed wording — proposed, not enacted:**
- **RECOMMENDED: "Facts about other people"** — hip-vo's own choice at
  517dd7c, already live on the demo branch. True over confirmed, asserted,
  and unconfirmed lines (the per-line markers now carry the provenance the
  header used to overclaim), minimal diff, and re-converges the two
  checkouts' prompts.
- Alternative: "Facts on record about other people" — also true, slightly
  heavier; "on record" matches the project's record-first vocabulary.
- Rejected: "Known facts about other people" — "known" still smuggles a
  certainty claim over unconfirmed lines.

**The one-edit set, when ruled** (for the executing dispatch): the constant
(:185), the guard prose (:129 — ideally converted to interpolate the
constant, one source, TD-137's lesson), the registry pin (:388 — with its
"Bill's own words" provenance comment re-cited to the new ruling), and the
three comment/docstring references; acceptance per the dispatch's own step
4 (mixed-prompt header truth, before/after strip equivalence, pin-matches-
constant with red-on-mismatch — the last already exists via the AUDIT
four-part fixture check, verified: a rename without the pin goes red today).

## VERIFIED

- **Watched run:** none needed — read-only survey; no code changed, so the
  step-5 harness run does not arise (its trigger was "THEN CHANGE IT").
- **Reasoned about / grep-verified:** the seven-site enumeration (repo-wide
  grep, .venv excluded); the derivation (read, quoted); the closed loop
  (all four callers read); the pin's red-on-mismatch behavior (from the
  AUDIT fixture-marker mechanism, not executed against a mutated tree).

## HASH

Committed this session on `roadmap` (D-115, docs-only); parent 14811f3.

## OPEN

- **The ruling itself:** rename to what, and does Bill authorize revising
  his own D-28 pinned wording. The recommendation is hip-vo's "Facts about
  other people"; the one-edit set above is ready to execute.
- The guard's hardcoded copy (:129) is a standing one-source violation
  independent of the rename — whichever dispatch executes should
  interpolate the constant.
- Nothing ruled MET; nothing changed beyond this doc and its INDEX row.
