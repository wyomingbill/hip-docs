# DISPATCH_TRUST_MARKER_PORT
Status: BUILT
Reconciled-Against: 2026-08-03 (D-114; parent 501df3d at dispatch time)

**TYPE:** BUILD

**REQ:** `docs/requirements/REQ_CONFIDENCE_DISCIPLINE__truth-track__v20260721_0945.md`
(NOT MET — and stays NOT MET; nothing ruled here). The dispatch named no REQ,
so per the gate the survey established one rather than assuming: that REQ's
own WHAT'S KNOWN BROKEN names this exact gap — **"Write-time trust labels do
not reach the generation-time hedge decision"** — and its ATTRIBUTED_HEDGE
machinery (harness/answer_mode.py, built under it) is the mode-side half
already landed. This port is the prompt-side half: the per-fact grounding the
model realizes the hedge wording from. The caveat on an asserted fact was
already required and unbuilt, exactly as the dispatch's step 2c anticipated.

## THE ASK

> 1. Roadmap LACKS one thing hip-vo HAS: harness/orchestrator.py has no
>    _fact_trust_marker / _TRUST_MARKERS. Added on hip-vo by 517dd7c.
>    Effect: a reply naming an ASSERTED fact carries a provenance caveat.
>    Roadmap replies "Ray is on Jardiance 10mg." flat, on a fact whose rung
>    says it was never verified outside the household. This is core reply
>    behavior, not a demo asset.
> 2. SURVEY FIRST: (a) what 517dd7c actually does — read it, do not infer;
>    (b) whether roadmap's trust ladder still has the rungs the marker keys
>    on — if rung names or semantics moved, this is not a copy; (c) whether
>    any roadmap requirement already speaks to this. STOP AND REPORT if the
>    rungs no longer line up.
> 3. THEN PORT IT if clean. Match roadmap's rung names, not hip-vo's.
> 4. ACCEPTANCE, namespaced per D-87, fault twin and anti-vacuity: an
>    ASSERTED fact's reply carries the caveat; a CONFIRMED fact's does not;
>    the caveat text comes from one place, not authored per reply.
> 5. Run --layer 7 plus RATCHET plus the memory harness. Pin 13-15/17,
>    failures a subset of {115,116,117,118}. 15/17 is the ceiling; 16/17 is
>    a STOP.
> 6. Rule nothing MET.

## WHAT WAS FOUND (survey, before any change)

**(a) What 517dd7c actually does** (read from hip-vo's git, not inferred):
adds `_TRUST_MARKERS` (level → bracketed plain-English marker; CONFIRMED →
""), `_fact_trust_marker(fact)` (classifies via `memory_engine.trust.
classify_trust_props` from fields already on the fact dict), appends the
marker at THREE render sites (recent-context mem lines, the second-person
"Things you know" section, the third-party section), rewrites the grounding
guard's hardcoded "Confirmed facts about other people" header to "Facts
about other people", and adds a bracketed-note instruction block to the
guard. Also adds a T05 re-ask turn to a demo script JSON — a demo asset,
NOT ported.

**(b) The rungs line up — the STOP did not fire.** `memory_engine/trust.py`
is **byte-identical** between hip-vo HEAD and roadmap (diff exit 0):
same five rungs, same first-match order, same `classify_trust_props`
signature. Verified, not assumed. One adjacent trap found and handled: the
sixth key in TRUST_RANK (`UNKNOWN`) is a P8 rank-table sentinel the
classifier never RETURNS — the battery's anti-vacuity case equates the
marker dict with the classifier's actual return set (by AST), not the rank
table.

**(c) A roadmap requirement already speaks to this** — REQ_CONFIDENCE_
DISCIPLINE, as above. The built half: `select_answer_mode` picks
ATTRIBUTED_HEDGE for {ASSERTED, UNCONFIRMED, DERIVED} and the orchestrator
mode-gates the grounding guard (L7V2 SC1-E2E proves it live). The unbuilt
half: the guard told the model to hedge but the prompt never said WHICH
fact deserved it. R12 was checked and is about the inbound author cap —
adjacent (aggregation/derivatives), not this behavior.

**Two roadmap divergences that made this a PORT, not a copy:**
1. **The header rename was NOT taken.** Roadmap's section headers are
   constants (`SECTION_OTHER_PEOPLE`, orchestrator.py) feeding
   REQ_STRIP_CONTEXT_COMPLETENESS's frontier-strip pattern derivation, and
   `eval/harnesslib/check_registry.py` pins the literal
   `'SECTION_OTHER_PEOPLE = "Confirmed facts…'`. Renaming is a
   strip-machinery + check-registry change with its own blast radius —
   out of this dispatch's scope. FLAGGED instead (OPEN below): the header
   still says "Confirmed facts…" over a list that can now carry
   non-confirmed markers — hip-vo fixed this mislabel; roadmap now carries
   it visibly.
2. **Field-less dicts render flat** (roadmap hardening over hip-vo): a
   dict carrying NONE of the five classifier fields (session/Zep-era
   shapes in the mem section) gets NO marker — classifying it would emit
   "[unconfirmed report]" as a fabricated caveat, the exact "wrong caveat,
   worse than none" the dispatch's STOP describes. Asserted by a fault
   twin, paired with its inverse (a real UNCONFIRMED fact IS marked).

## WHAT WAS BUILT

`harness/orchestrator.py`: `_TRUST_MARKERS` (hip-vo's marker text verbatim;
roadmap's rung names — identical anyway), `_fact_trust_marker()` with the
field-less guard, markers appended at roadmap's three render sites
(fact_id/PSA1 plumbing untouched — markers ride the value text, never the
ids), and the guard gains the bracketed-note instruction block **composed
from `_TRUST_MARKERS` by f-string** — the caveat text exists ONCE (hip-vo
had it twice, dict + prose; TD-137's lesson applied at port time). The
"GROUNDING RULE" marker string is unchanged (L7V2 SC1-E2E greps for it).

`eval/test_trust_marker.py` — CONF-MARKER, 9 cases, `test_conf_marker_*`,
wired into run_harness.sh (20th battery): asserted-line-carries-caveat
(second-person AND third-party sections, through the REAL renderer),
confirmed-renders-flat, guard-composes-from-the-dict + every-bracket-is-
from-the-dict (acceptance bullet 3, both directions), field-less fault twin
+ its inverse, DERIVED/CORROBORATED rung mapping, and the AST anti-vacuity
rung-alignment case. **The battery caught one bug in my own work on its
first run** (the D-105 convention, reported not hidden): the anti-vacuity
case originally equated `_TRUST_MARKERS` with `TRUST_RANK`'s keys and went
red on `UNKNOWN` — the rank-table sentinel. Fixed to compare against the
classifier's return set; the docstring records why.

## VERIFIED

**Watched run (read individually from the logs, this dispatch):**
- CONF-MARKER standalone: 9 passed (after the one caught-and-fixed case).
- 20 batteries: **306 passed / 1 skipped / 8 xfailed** (297+9).
- **AUDIT 8/8 · DISC 1/1 · L7 27/27 · L7V2 27/28** (1 opt-in skip) ·
  SCHEMA 1/1 · VOICE 1/1 · **RATCHET PASS · 0 scenario FAILs** ·
  COVERAGE-GRID-RATCHET PASS.
- ABSOLUTE individually: **OB6 · G0 · PSA1 · CTX-STRIP · LI1 — all PASS**
  (PSA1 and CTX-STRIP are the two this change could plausibly have
  disturbed; both hold — markers ride value text, and fact sections strip
  whole).
- **Mutation self-test finds its mutant at `injection_contract.py:664`**,
  both directions.
- **Memory harness: 15/17, failing exactly {MEM-115, MEM-116}** — inside
  the pin (13-15/17, ⊂ {115,116,117,118}), at the structural ceiling; NOT
  the 16/17 STOP shape.

**Reasoned about:** that live replies will actually verbalize the caveat —
the port gives the model the marker and the instruction (hip-vo verified
that live on its branch per 517dd7c's own commit message); roadmap's live
verbalization quality is a demo/HITL observation, not asserted by this
battery, which proves the PROMPT the model receives.

**Process notes, on the record:** `.hip-lock` was taken LATE — survey and
the code edits ran unlocked (a miss against the standing discipline; the
lock file itself records it). D-112 does not exist in this checkout's
sequence (cutover-lane numbering, same as D-106).

## HASH

Committed this session on `roadmap` (D-114); parent 501df3d.

## OPEN

- **The header mislabel, flagged not fixed:** `SECTION_OTHER_PEOPLE` still
  reads "Confirmed facts about other people" over lines that may carry
  asserted/unconfirmed markers — one prompt can now say both. Fixing it
  means the constant, the strip derivation, and check_registry's pin move
  together, its own dispatch.
- Live verbalization quality (does the edge model actually voice the
  caveat well?) — a HITL/demo observation to collect.
- REQ_CONFIDENCE_DISCIPLINE stays NOT MET — this closes one named gap of
  several (intent's UNCERTAIN class and the typed AMBIGUOUS state remain
  explicitly unbuilt).
