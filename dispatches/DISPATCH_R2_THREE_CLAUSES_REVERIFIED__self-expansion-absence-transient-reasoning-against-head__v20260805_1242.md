# DISPATCH_R2_THREE_CLAUSES_REVERIFIED
Status: BUILT
Reconciled-Against: 2026-08-05 (D-R-180; parent `99a54e0`)

**TYPE:** ANALYSIS (read-only survey; no code changes)

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`,
R2 (ruled NOT MET, D-143, 2026-08-03, on a SCOPE gap), with direct bearing on R5, R6, R7.
REQ: existing — no new REQ needed for a read-only survey with no code change
(Requirements Discipline item 10).

**PRIOR TRACE, READ FIRST (Requirements Discipline item 11):** this exact question was
already answered once, in full, at D-143 —
`docs/dispatches/DISPATCH_R2_SCOPE_RULING__not-met-self-expanding-inference-absence-transient-reasoning__v20260803_1924.md`.
That survey's own three-clause verdicts (R5/R6 HELD VACUOUSLY BY ABSENCE, unmonitored;
R7 COVERED by an active tripwire) are **RECONFIRMED below against 2026-08-05 HEAD**, not
merely re-cited — two days and roughly 35 dispatches have landed since D-143, and this
dispatch's own instruction is explicit: "evidence from HEAD, not from memory of D-130"
(extended in spirit to D-143 as well, since it is now itself two days old). **What is new
in this pass, cited precisely, not folded silently into a restatement:** D-143's own claim
that A2 "has never been written or run" is now STALE — D-145, landed the SAME DAY as
D-143, wrote and ran it; a materially wider fresh grep for `derived`-flag consumers turned
up roughly eight more call sites than D-143's own citation, all re-classified below and all
still consistent with D-143's conclusion; and one new string
(`qualifying_sensing_contract_event`) now exists in the tree, traced and shown to be inert
vocabulary, not a functioning mechanism.

## THE ASK

```
=== D-R-180 | ~/hip-roadmap, roadmap | R2's three unestablished clauses, evidence
    against HEAD ===
STANDARD PREAMBLE. Lane A. READ-ONLY SURVEY — no code changes.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R2, ruled NOT MET 2026-08-03 on SCOPE: the
permit build delivered one clause; three were never established. This survey
establishes them so Bill can re-rule.

For EACH of the three, answer with evidence from HEAD, not from memory of D-130:
1. NO SELF-EXPANDING INFERENCE — can any inference widen what the system may infer
   next? Where is that prevented, or is it merely not implemented anywhere? "No code
   does X" needs the enumeration method stated (the four counting failures in the
   ledger build are the cautionary precedent — say HOW you searched).
2. NO INFERENCE FROM ABSENCE — can the system derive a fact from the lack of one?
   Same standard.
3. TRANSIENT REASONING — does intermediate reasoning persist anywhere it shouldn't?
   Name every place inference intermediate state is written, and whether it survives
   the turn.
For each clause: ENFORCED (cite the enforcement point), HOLDS BY ABSENCE (state the
search method and its blind spots), or DOES NOT HOLD (cite the counterexample).
UNKNOWN acceptable with the determining test named.
Report LONG to a dispatch doc. Rule nothing.
```

## WHAT WAS DONE

1. Gate checked — matched, tree clean except demo-cutover lane's own 4 untracked docs,
   lock free, HEAD at `99a54e0` (D-R-179) at start.
2. Read D-143's own dispatch doc in full before doing anything else (Requirements
   Discipline item 11), to know exactly what was already established and by what
   method, so this pass adds evidence rather than re-deriving from zero.
3. Re-read R2/R5/R6/R7's exact requirement text (`REQ_STRUCTURAL_CEILING:229-358`) —
   confirmed the same mapping D-143 found: R2's three named clauses are R5 (no
   self-expanding inference), R6 (no inference from absence), R7 (transient reasoning).
4. **R5**, fresh: ran a broader full-tree grep for every `derived`-flag reference (not
   just `derived==True`/`derived=True` literal forms — also `.get("derived")` and
   Cypher `f.derived` projections) across `harness/`, `memory_engine/`, `server/`.
   Classified every hit as either a plain projection/display/audit site or a
   behavioral consumer; traced each behavioral one to its actual effect. Re-read
   `_escalate_pass`'s query and `_write_derived_node`'s `write_state` stamp directly to
   reconfirm their structural exclusion still holds byte-for-byte.
5. **R6**, fresh: re-ran the full-tree grep for sensing-contract/absence vocabulary,
   this time including `eval/` (D-143's own grep did not say whether it did). Traced
   the one new hit found. Re-read `GroqInterpreter.abstract()`'s prompt construction
   and `fact_change.py`'s `detect_and_apply`/`_call_groq` input shape directly.
6. **R7**, fresh: confirmed `eval/test_ceiling_representation.py` (A7) still exists,
   still wired in `scripts/run_harness.sh`, and **executed it live** — 19 passed. Ran a
   fresh, independent grep (not relying on A7's own AST scanner) for
   reasoning/scratchpad/chain-of-thought vocabulary across production code — zero
   hits. Additionally traced ONE SPECIFIC known reasoning-bearing value
   (`DerivedFact.rationale`, the model's own short explanation per abstraction) through
   its full lifecycle to confirm it is never included in the props `_write_derived_node`
   persists.
7. Re-checked A2's own execution status: found it now HAS a real test
   (`eval/test_ceiling_inference.py::test_ceil_a2_*`, 5 cases, written at D-145 the SAME
   DAY as D-143) and ran it live — 5 passed. Confirmed via `git log -S` which commit
   introduced it, since this directly contradicts D-143's own "never executed" line.
8. Checked whether any A5/A6-shaped regression tripwire (matching A7's own shape) has
   been built since D-143 — none found, confirming that OPEN item is unchanged.
9. Checked whether the offer-gate/purpose-trigger mechanism built this session
   (D-152/D-R-171) gives any real caller a path from a derived fact to a widened permit
   or audience — confirmed no: zero real callers construct a `PurposeTrigger` at all,
   the registry it would populate is still an empty, unenacted `MappingProxyType`.
10. Wrote this dispatch doc, registered it in `docs/INDEX.md`, corrected
    `docs/HIP_HANDOFF.md`'s CURRENT STATE (same rule as D-R-179's own fix — landed by
    the lane that lands a dispatch), committed and pushed under the repo lock.

## WHAT WAS FOUND

### Clause 1 — R5, no self-expanding inference: **HOLDS BY ABSENCE, unmonitored** (unchanged from D-143)

R5's text (`:314-325`): a "sensitive hypothesis" (a derived fact) may trigger only a
pause, a neutral human-review suggestion, a predefined authorized workflow, or an
emergency response — never more questions in its own domain, a new/widened permit, a
wider audience, or extended retention.

**Search method, stated plainly:** `grep -rn "derived\s*==\s*True\|derived=True\|\.derived\b"` first, then a WIDER second pass without the narrow anchor
(`grep -rni "derived"` filtered to exclude `derived_from`/`derivation`/`DerivedLineage`
noise) across `harness/`, `memory_engine/`, `server/` — the two-pass approach is
deliberate: the narrow pattern is what D-143 effectively used (4 files cited); the wide
pass exists specifically to check for the blind spot a narrow anchor creates.

**Full enumeration, this pass (16 files touch the flag; classified):**
- **Behavioral/narrowing** (confirmed, re-read directly): `memory_engine/trust.py:69`
  (`if derived:` — confidence cap), `harness/injection_contract.py:530`
  (`fact.get("derived")` — excludes derived facts from the owner-permit read path),
  `harness/curator_shadow.py:128` (one of ten FIXED shadow-scorer feature keys — a
  retrieval-prioritization signal, not evidence-gathering authority),
  `memory_engine/store.py:420` (R18 lineage-block: refuses a derived write missing
  required lineage — a gate, narrows), the R18 cascade (closes derived children on a
  parent's retraction — narrows). **All five match D-143's own citations exactly,
  unchanged.**
- **Presentation-only, hedges rather than expands** (NEW to this citation, not in
  D-143's own list, traced and confirmed inert): `memory_engine/api.py:299`
  (render-hint text), `harness/answer_mode.py:81` and `harness/orchestrator.py:107-120`
  (both feed `derived` into `trust.classify_trust_props` to select a HEDGED
  answer-mode/trust-marker bracket — the D-102/D-107-era trust-ladder mechanism; forces
  more caution in wording, the opposite of expanding authority).
- **Plain projection/audit, no branching at all** (NEW to this citation, confirmed by
  direct read of each): `harness/extraction_queue.py` (4 sites — pending-queue and
  escalation-listing dicts, `derived` copied through for DISPLAY, immediately fed to
  the same `classify_trust_props` where it IS used, never to trigger anything new),
  `harness/fact_change.py:304,323` (returned in a `FactChange` dataclass, exposition),
  `harness/epistemic_record.py:114` (recorded into the ledger event for AUDIT),
  `memory_engine/recall.py:253`, `server/memory_dashboard.py:84,105,144` (dashboard
  display), `memory_engine/store.py:497,511` (dict projection on read).

**The one mechanism that could look like self-expansion** — `_escalate_pass`'s
must-confirm queue (`memory_engine/consolidate.py:722-735`) — re-read directly this
pass: its query is `MATCH (f:Fact {owner: $owner, write_state: 'unresolved'})`
(`:735`), and `_write_derived_node` (`:502-544`) stamps `"write_state": "augment"`
unconditionally (`:544`) — structurally disjoint sets, byte-identical to D-143's own
citation.

**Checked one thing D-143 did not name:** whether this session's OWN new build
(`harness/offer_gate.py`/`harness/purpose_trigger.py`, D-152/D-R-171) gives a derived
fact any path to a widened permit or audience via `PurposeTrigger`. It does not — zero
real callers construct a `PurposeTrigger` anywhere in the tree (`grep -rn
"PurposeTrigger(" harness/ memory_engine/ server/` returns only the docstring
composing-example at `purpose_trigger.py:139`); `PURPOSE_TRIGGER_REGISTRY` remains an
empty, unenacted `MappingProxyType`.

**Verdict: HOLDS BY ABSENCE, unmonitored — same as D-143, now with a materially wider
enumeration (16 files vs. D-143's 5) supporting the same conclusion, and one
additional two-day-old subsystem checked and found not to reopen it.** **What would
break this, stated precisely:** any future code reacting to `derived=True` (or
specifically `attribute='risk_pattern'`) by triggering additional targeted
extraction/questions, a new/widened `inference_permit`, a broader
`audience_policy`/`recipient_ref` than `classify_write` assigned, or a longer retention
window — including, now named explicitly, a future real caller of `PurposeTrigger` keyed
off a derived fact. **No standing regression tripwire exists for this** — confirmed no
`test_ceil_a5_*` function exists anywhere in `eval/` (D-143's own OPEN item, unchanged).

### Clause 2 — R6, no inference from absence: **HOLDS BY ABSENCE, unmonitored** (unchanged from D-143, one new vocabulary item traced and dismissed)

R6's text (`:327-345`): deriving a fact from a signal's absence requires a validated
sensing contract (six named properties); named prohibited examples include "no
medication confirmation → medication not taken."

**Search method:** full-tree, case-insensitive grep for `sensing_contract|
inactivity|days_since|last_seen|no_signal|absence_signal|missingness`, across
`harness/`, `memory_engine/`, `server/`, **and `eval/`** (widened beyond D-143's own
stated scope, which did not say whether tests were included).

**One hit, new since D-143, traced:** `eval/test_ceiling_solicitation.py:314`,
`"qualifying_sensing_contract_event"` — a NAMED STRING inside `_MATERIAL_CHANGE_KINDS`,
the R23/R24 purpose-trigger/offer-gate build's own allowed-vocabulary tuple (built
D-152/D-R-171, after D-143). **This is not a functioning sensing-contract mechanism** —
it is a recognized label a future, real `PurposeTrigger` COULD carry if one ever fired
with this kind, and (per Clause 1's own finding above) zero real callers construct a
`PurposeTrigger` at all. Traced, not assumed: this changes nothing about whether absence
is inferred from anywhere today.

**Structural confirmation, re-read directly:** `GroqInterpreter.abstract()`
(`memory_engine/interpreter.py:368-412`) builds its prompt entirely from `episodes` —
guarded by `if not episodes: return []` at entry, then `facts_block` built from
`f.get("attribute")`/`f.get("confidence")` for facts that DO exist; `owner`/`subject`
pulled from `episodes[0]`. No representation of a missing signal is constructible from
this input shape. `harness/fact_change.py::detect_and_apply` (`:892+`) takes `utterance:
str` — re-read the literal prompt template (`:126`, `'User said: "{utterance}"'`) —
inherently a presence signal; nothing computes or feeds an inactivity/elapsed-time
value into it.

**Verdict: HOLDS BY ABSENCE, unmonitored — unchanged from D-143.** **What would break
this:** any future feature computing an absence/inactivity signal and feeding it to
`abstract()` or `classify_write()`. No sensing-contract mechanism (the six-property gate
R6 requires) exists anywhere to catch it if that happened — confirmed no
`test_ceil_a6_*` function exists anywhere in `eval/`.

### Clause 3 — R7, transient reasoning creates no durable authority: **ENFORCED**

**Enforcement point:** `eval/test_ceiling_representation.py` (A7, R7's own acceptance
row), wired into `scripts/run_harness.sh:125`. **Executed live this dispatch, not
merely confirmed present:** `19 passed` (`PYTHONPATH=$(pwd) $HIP_DEV_PYTHON -m pytest
eval/test_ceiling_representation.py -q --import-mode=importlib`). It AST-scans every
production module for `chain_of_thought`/`reasoning_trace`/`scratchpad`-shaped fields on
any durable write, with an executed fault twin (a synthetic module persisting a
reasoning trace, proven to be flagged) and a metamorphic renaming/aliasing check.

**A second, independent check run this dispatch** (not relying on A7's own scanner):
fresh grep for `reasoning_trace|scratchpad|chain_of_thought|intermediate_reasoning|
thinking_trace` across `harness/`, `memory_engine/`, `server/` — **zero hits** outside
the test file itself.

**Named, per instruction, every place inference intermediate state is written, and
whether it survives the turn:**
- `memory_engine/interpreter.py::GroqInterpreter.abstract()` produces a
  `DerivedFact.rationale` per abstraction (the model's own short explanation, capped at
  200 chars at the call site) — **traced its full lifecycle**: held as a Python
  attribute for the scope of one `_abstract_pass` call, and confirmed by direct read of
  `_write_derived_node`'s CREATE props (`memory_engine/consolidate.py:531-544`) that
  `rationale` is **not** among the fields persisted — only `attribute`, `subject`,
  `owner`, `value` (as ciphertext), and `derived_from` (fact IDs) are written. It does
  not survive the call, let alone the turn.
- `harness/fact_change.py::_call_groq`'s raw model JSON response is held in local
  variables for the scope of `detect_and_apply`, projected down to structured fields
  (`attribute`, `value`, `subject`) before any write — the same shape, verified by the
  absence of any raw-response field in that module's own write path.
- No `:Fact` node property, HEL ledger event field, or dashboard/session record anywhere
  carries a reasoning/rationale/thinking-shaped field — confirmed by the zero-hit grep
  above, which covers the whole tree, not just the two functions traced by name.

**Verdict: ENFORCED — distinguished from Clauses 1/2 precisely because this one has an
ACTIVE, EXECUTED MONITOR that fires on the commit introducing a violation, not only an
absence found today.**

### A2 (context, not this dispatch's own subject): D-143's "never executed" finding is now stale

`eval/test_ceiling_inference.py::test_ceil_a2_*` (5 cases) exists and passes —
**confirmed by `git log -S` that D-145 (`93eb91e`), landed the SAME DAY as D-143,**
wrote and ran it, closing the "no executed acceptance" gap D-143's own §16 entry
states. **This does not change R2's own NOT MET status** — `REQ_CEILING_ACCEPTANCE`
§7.7 already recorded, at D-145 itself, that "R2 is ruled NOT MET (D-143 — scope gap,
R5/R6/R7 unaddressed)... A PASSING ROW DOES NOT CARRY ITS REQUIREMENT," so the scope gap
this dispatch addresses was never actually resolved by A2 passing. Flagged here only
because D-143's literal words ("R2 has no executed acceptance of any kind") are no
longer true as a standalone claim and a future reader citing D-143 verbatim would be
citing something stale.

## VERIFIED

**Watched, executed this dispatch:**
- `eval/test_ceiling_representation.py`: 19 passed.
- `eval/test_ceiling_inference.py -k a2`: 5 passed.
- Every grep command in WHAT WAS DONE/FOUND was run fresh against current HEAD, not
  recalled from D-143's own report.
- `git log -S"test_ceil_a2_off_permit_input_attribute_is_refused_with_no_write"` to
  confirm which exact commit introduced A2's test (`93eb91e`, D-145).
- `memory_engine/consolidate.py:502-544` (`_write_derived_node`'s full CREATE prop
  list), `:722-735` (`_escalate_pass`'s query), `memory_engine/interpreter.py:368-412`
  (`abstract()`'s full body), `harness/fact_change.py:892+,126` all read directly, in
  full, this dispatch — not recalled from D-143's own citations.

**Reasoned about:**
- That the wider, 16-file enumeration for R5 is "materially wider" than D-143's own
  4-file citation is a comparison against D-143's OWN WRITTEN LIST, not a claim that
  D-143 literally searched only 4 files (its own text does not fully disclose its
  search command).
- That no hidden self-expansion or absence-inference mechanism exists ANYWHERE is, as
  D-143 itself noted, an absence claim bounded by the search performed — a
  determined adversary reading this file could always add one tomorrow; this dispatch
  states what would break each finding precisely so that determination is checkable
  later, not asserted as a permanent guarantee.

## HASH

`1ae07e3` — pushed to `origin/roadmap`. Filled in by a same-session follow-up edit
after the commit landed, per the D-R-176/179 convention. Contains: `docs/HIP_HANDOFF.md`,
`docs/INDEX.md`, this dispatch doc.

## OPEN

- **Nothing ruled — per instruction.** This establishes the evidence Bill's own D-143
  ruling asked for; whether R5/R6 being HELD VACUOUSLY BY ABSENCE (unmonitored) is
  sufficient for R2's scope gap to close, or whether R2 stays NOT MET until R5/R6 get
  an active tripwire matching R7's own A7 shape, is Bill's call.
- **R5 and R6 still have no standing regression tripwire** — same OPEN item D-143 named,
  unchanged after this pass. A future build could close this the same way A7 already
  models (an AST/behavioral scan with an executed fault twin); not attempted here
  (read-only survey, no code changes, per the preamble).
- **The three clauses' status is a snapshot, not a permanent guarantee** — any future
  code matching the "what would break this" descriptions above would need to be caught
  by hand today, since only Clause 3 has an active monitor.
- **D-143's own "A2 never executed" line is now stale**, corrected here; D-143's dispatch
  doc itself is left unedited (it is a historical record of what was true 2026-08-03,
  Naming Law: never overwrite) — the correction lives in this new dispatch, per the
  pre-authorized class "correct its own prior report... in a new record that names the
  old one."
