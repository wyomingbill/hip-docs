# REQ_STRIP_CONTEXT_COMPLETENESS
Status: MET
MET-Ruling: Bill, 2026-08-03 (D-118). Evidence cited in the ruling:
(1) eight sites changed in one change-set, including the eighth the earlier
survey missed to the very wrap hazard it had named; (2) the zero-check is
wrap-tolerant by construction — AST string-constant walk plus comment-joined
and collapsed-text scans — and cannot false-zero, because no path depends on
a literal sitting on one line; (3) strip equivalence PROVEN by before/after
on real prompts: stripped outputs byte-identical in every case, with the
sole normalization (the embedded wall-clock sentence) disclosed and
isolated; (4) two real mutants applied and restored byte-exactly:
pin-revert 4 RED, constant-revert 5 RED, 9/9 green after each restore;
(5) CTX-STRIP and PSA1 both PASS. Hardening beyond the rename, recorded per
the ruling: the registry pin now sits on a single source line, killing the
wrap-evasion shape at the root, and the wrap-tolerant scanner is a
permanent battery case (HDR-RENAME) with the wrapped shapes pinned RED.
The full-ratchet L6 red present at ruling time is NOT this REQ's failure —
ruled unrelated (structurally unreachable by the rename; TD-147, filed
this same dispatch), baseline left unupdated and the red left loud.
Supersedes: REQ_STRIP_CONTEXT_COMPLETENESS__frontier-section-header-derivation__v20260727_1851.md
Reconciled-Against: roadmap c0bca12 (D-115 seven-site survey, re-verified standing 2026-08-03)

## WHY A REVISION, NOT A FRESH REQ

D-117's own instruction: "A fresh REQ is the wrong shape — the problem IS
that this REQ's acceptance item 1 pins the old literal." The prior version
is MET (Bill's ruling, 2026-07-29, recorded in that file and left intact
there); its acceptance was proven against the OLD header literal and must be
RE-RUN under this revision. This revision does not disturb the D-28
mechanism the prior version built — the derivation of the strip pattern from
`FACT_BEARING_SECTION_HEADERS` stays exactly as shipped. What changes is one
header's text, and every artifact that pins that text.

## THE REQUIREMENT

Bill's ruling, 2026-08-02, verbatim from D-117:

> The section header becomes "Facts about other people". The old wording is
> FALSE now that the section can carry confirmed, asserted, or unconfirmed
> lines — one prompt would claim confirmed above a line marked asserted. The
> new wording is also hip-vo's, so the two checkouts re-converge instead of
> gaining a third variant.

Per D-117 step 1, this revision records, on its face:

1. **The new literal is `"Facts about other people"`** — the value of
   `SECTION_OTHER_PEOPLE` (`harness/orchestrator.py`) and therefore, by the
   D-28 single-source design, of both the rendered header and the strip
   pattern. **Acceptance item 1's pin moves with it**: the `L7:CTX-STRIP`
   ground-truth fixture in `eval/harnesslib/check_registry.py` re-pins to
   the new literal in the same change.
2. **The check_registry pin held Bill's own words** — the header text from
   the dispatch that opened D-28, recorded there as human-verified ground
   truth. **Changing it is DELIBERATE, not a correction of an error.** The
   D-28 wording was right for its time; the section has since gained
   asserted/unconfirmed lines (D-114's trust markers), which is what made
   the old wording false. The pin's provenance comment is re-cited to this
   ruling (Bill, 2026-08-02, D-117).
3. **The strip derivation is the risk.** `_personal_section_pattern()`
   derives its regex from `FACT_BEARING_SECTION_HEADERS`, so the rename
   changes what gets stripped **unless proven otherwise**. The proof
   required is behavioral — before/after comparison on real prompts built by
   `TurnOrchestrator.local_system_prompt()` — not inspection. If what gets
   stripped changes at all, the build STOPS before committing.

## THE ACCEPTANCE TEST

Items 1–5 are the prior version's items, re-based on the new literal — they
must be RE-RUN, not inherited:

1. `L7:CTX-STRIP` (ABSOLUTE tier) hard zero: a real prompt built by
   `TurnOrchestrator.local_system_prompt()` with all three fact-bearing
   sections populated, stripped via `strip_context_for_tier(messages,
   "frontier", query)`, contains NONE of the three section headers — the
   third now being **"Facts about other people"**. The registry fixture pin
   carries the new literal and stays on a single source line (the old pin
   wrapped across two adjacent string literals, which is exactly how it
   evaded a whole-literal grep — D-116's finding).
2. Fault-injection twin, both directions, unchanged mechanism: synthetic
   fourth section survives (RED), then strips once the derivation source
   covers it (GREEN).
3. `check_registry.py` carries the four REQ_HARNESS_DISCIPLINE artifacts for
   `L7:CTX-STRIP`, fixture re-pinned per item 1.
4. `--layer 7` green AND the full ratchet green (CLAUDE.md item 12 is the
   house bar; the prior version's layer-7-only constraint stays superseded
   per the 2026-07-29 ruling recorded in it).
5. No call site anywhere gains a NEW `strip_context_for_tier` call for
   `tier in ("mid", "core")` — TD-131 remains Bill's open decision.

New items, this revision's own:

6. **HEADER TRUTH**: a prompt whose other-people section mixes a confirmed
   fact and an asserted fact (real renderer, real markers) carries a header
   that is true over both — it asserts nothing about confirmation. Battery
   check, namespaced per D-87.
7. **STRIP EQUIVALENCE**: for identical fact inputs, the stripped output
   (what leaves the device) is byte-identical before and after the rename,
   proven by recorded before/after runs on real prompts — frontier tier,
   plus one non-frontier case for the history filter. The removed region
   differs only by the renamed text itself.
8. **OLD-LITERAL ZERO, line-wrap-tolerant**: the old literal appears nowhere
   in live code, verified by a method that cannot false-zero on wrapped
   occurrences — AST string-constant walk (implicit adjacent-literal
   concatenation resolved at parse time) plus comment-marker-normalized
   full-text scan. The wrapped-pin shape is itself a pinned RED case in the
   battery: a site left on the old literal — INCLUDING a line-wrapped one —
   goes red. `logs/` run records are inert history, excluded by stated
   scope, not silently.

## WHAT'S ALREADY DONE

- The D-28 fix (prior version of this REQ, MET): derivation of the strip
  pattern from `FACT_BEARING_SECTION_HEADERS`, `L7:CTX-STRIP` with twin both
  directions, registry entry. Untouched by this revision except the pinned
  text.
- D-114: per-fact trust markers render into the prompt (why the old header
  wording became false). D-115: the seven-site survey and the closed-loop
  analysis (render and strip source the same constant; all four live
  callers strip freshly built messages — nothing re-strips stored prompts).

## WHAT'S KNOWN BROKEN

- The header mislabel itself: "Confirmed facts about other people" sits over
  lines carrying `[reported within the household...]`-class markers — one
  prompt claims both. FLAGGED OPEN at D-114, confirmed at D-115, ruled at
  D-117.
- `PERSONAL_FACT_GROUNDING_GUARD`'s prose (`harness/orchestrator.py:129`)
  carries a hardcoded copy of the header — a standing one-source violation
  and the silent-miss hazard of any rename. This revision requires it to
  derive from the constant (TD-137's one-place-ness lesson), or be left
  hardcoded and loudly flagged if that is more than a small change.

## CONSTRAINTS

- Do NOT extend `strip_context_for_tier` to MID or CORE (TD-131, Bill's).
- Do NOT change what gets stripped: acceptance item 7 is the proof, and a
  behavioral difference is a STOP, not a note.
- The other two headers (`SECTION_RECENT_CONTEXT`, `SECTION_KNOWN_FACTS`)
  are out of scope — no wording change, no derivation change.
- RATCHET stays green throughout; nothing in the roster regresses.
- Memory harness pin: 13–15/17, failures a subset of
  {MEM-115, MEM-116, MEM-117, MEM-118}; 16/17 is a STOP (a pinned-failing
  scenario going green unexplained is evidence of a changed baseline, not
  of health).

## PROPOSED STATUS

Per D-117 step 1: this revision proposes its own status and does not
self-rule. **Filed NOT MET.** The prior version's MET ruling covered the old
literal; every acceptance item above must be re-proven under the new one.
When the executing dispatch (D-117) attaches that evidence, the proposal is
**READY FOR RE-RULING — Bill decides.** Nothing here is ruled MET.

**RULED: Bill, 2026-08-03, D-118 — MET.** See the MET-Ruling in the Status
header for the evidence cited and the recorded hardening. The proposal text
above is retained as written, for provenance. The session recorded the
ruling; it did not make it.
