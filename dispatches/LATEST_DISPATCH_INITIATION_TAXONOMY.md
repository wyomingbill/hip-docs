# DISPATCH_INITIATION_TAXONOMY — the closed three-class set, and one site that needs a ruling

Status: BUILT
Reconciled-Against: roadmap `f5f5483` (pre-build HEAD). **LANDED AT `54e91b5`** — backfilled by the immediately following commit, because a commit cannot contain its own hash.

**HA-01** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD (code)**
**GOVERNING REQ:** `docs/requirements/REQ_OFFER_MECHANISM__governed-initiation-of-new-authority__v20260806_1320.md`,
§12 LANDING ORDER **step 1 ONLY** — "Define the closed initiation taxonomy and suppress
unclassified initiation." No other step of §12 is started here.
**NOTHING RULED MET.**

## SERIES LINEAGE — HA-nn opens here

**This dispatch opens the HIP Advisor series (`HA-nn`) on the roadmap lane.** Its
predecessor series `D-R-nnn` is CLOSED and **ended at `D-R-196`** (the sensitivity-default
build, `90da7fb`). `HA-01` is the first of the new series.

Registered in `CLAUDE.md` STANDARD PREAMBLE item 10 — the table that already owns per-lane
ID prefixes and is where a reader meeting an unfamiliar prefix will look. Recorded there:
the lane/checkout/branch are unchanged (this is a **series** change, not a lane change),
`TD-R-nnn` is unchanged and only the DISPATCH series succeeded, and **no existing `D-R-nnn`
ID is renumbered or retired** — the same rule item 10 already applies to lane prefixes.

## 1. ALREADY-EXISTS CHECK (the dispatch's first instruction)

**No initiation taxonomy exists in code.** A source sweep for `AUTHORIZED_OPERATION`,
`SAFETY_INTERRUPT`, `initiation_class`, `INITIATION`, `system_initiated` returns nothing
but prose in three files. What DOES exist, and is deliberately not duplicated:

| Module | What it is | Relationship to step 1 |
|---|---|---|
| `harness/purpose_trigger.py` | R23's trigger schema + NOT-list guard (D-152) | A LATER step (§12 step 2). Untouched. |
| `harness/offer_gate.py` | R24's one-offer-per-circumstance dedup (D-R-171) | A LATER step (§12 step 5). Untouched. |
| `harness/sensitivity.py` | R29/R30 registry | The house pattern this module copies: one closed set, one module, refusal not default. |

Both `purpose_trigger` and `offer_gate` record the same survey result in their own
docstrings — *"zero offer-initiation sites exist anywhere in this codebase; HIP is
reactive only"* (D-150, re-confirmed D-152, re-confirmed D-R-171). **HA-01 re-derived it
by hand rather than inheriting it** (§2). It holds.

## 2. THE SURVEY — every site that can emit speech (item 2, hand-read)

Read by tracing every speech egress, not by trusting the earlier surveys. `speak()` has
exactly one production caller in the tree; the voice paths emit through pipecat's TTS
service; everything else is a string that becomes one of those two.

| # | Site | Emits | System-initiated? | Disposition |
|---|---|---|---|---|
| 1 | `harness/orchestrator.py::handle_turn` step 4 (`self.speech.speak(reply)`) | the answer to a member's query | **No** — reply | **GATED**, declares `AUTHORIZED_OPERATION` (item 4) |
| 2 | `harness/speech.py::SpeechIO.speak` | Kokoro TTS to the speakers | **No** — a sink, not a decision point | Not gated; gating a sink would gate site 1 twice |
| 3 | `server/voice_orch.py` pipecat pipeline | the answer, plus `_ctrl_prepend` announcements | **No** — reply-driven | Not gated this dispatch (see §5) |
| 4 | `server/voice.py`, `server/voice_mem0.py` pipelines | the answer | **No** — reply-driven | Not gated this dispatch |
| 5 | `harness/control_flow.py` RECONSIDER announcements (`"Let me think about that a bit more."`, the CORE-ceiling message) | a tier-step-up announcement prepended to a reply | **No** — rides the member's own turn | Classifies cleanly as `AUTHORIZED_OPERATION` when gated; not wired this dispatch |
| 6 | `harness/control_flow.py` frontier ANNOUNCE / DECLINE / NO-CODEWORD messages | status of the member's own request | **No** — reply | As above |
| 7 | **`harness/control_flow.py::handle_frontier_request` → `_FRONTIER_CONFIRM_MSG`** | *"This query is sensitive. Answering it will send information off your home network. Confirm?"* | **AMBIGUOUS** | **STOP — see §3. NOT CLASSIFIED, NOT GATED, NOT CHANGED.** |
| 8 | `harness/injection_contract.empty_set_refusal` | a structural refusal | **No** — reply | Reaches the member via site 1 |
| 9 | `harness/offer_gate.py::present_offer` | an offer record (no text) | **YES by construction** | `OFFER` by definition. **No production caller** — confirmed again this dispatch; only `eval/test_ceiling_solicitation.py` calls it |
| 10 | `server/demo_dashboard.py`, `harness/realtime_adapter.py` (`response.create`) | relays a turn to the realtime API | **No** — reply-driven | Not gated this dispatch |
| 11 | Background threads (`extraction_queue`, `fact_change`, `session_memory` reaper, `zep_store`, `epistemic_ledger`) | nothing spoken | **No** — none emits speech | Checked explicitly; a background emitter is the shape that WOULD be system-initiated, and there is none |

**LOAD-BEARING RESULT: HIP has no system-initiated speech today.** Every emission is
reply-driven. A1 is therefore satisfiable today without changing a single utterance —
and the honest reading of that is that **the taxonomy is being put in place BEFORE the
thing it governs exists**, which is the right order but means A1's evidence is
necessarily thin. Said plainly rather than dressed up.

## 3. STOP (item 5) — site 7 cannot be classified without a ruling

`_FRONTIER_CONFIRM_MSG` is **live**, not a stub: `server/voice_orch.py` calls
`handle_frontier_request` at two sites and emits `spoken_response` on `confirm_needed`.
A member hears it today.

**Neither available class fits, and here is why each fails:**

- **`AUTHORIZED_OPERATION`** would put a request to expand external disclosure inside
  ordinary operational speech — which is exactly what **R3** forbids: *"An authorized
  reminder, alert, check-in, or safety interrupt SHALL NOT append, embed, imply, or
  sequence into a request for new authority unless a separately eligible offer exists."*
- **`OFFER`** contradicts **§2.2**, which lists *"confirmation of a member-initiated
  request"* among the things an offer is NOT — and it would drag in R4, which requires a
  trigger-registry decision with one of four material-change kinds. `harness/offer_gate.py`'s
  own survey found **none of the four has a usable representation today**, so the prompt
  would become un-renderable — changing what HIP says today, which **item 4 forbids**.

**So nothing is classified for site 7 and nothing about it is changed.** The prompt is
emitted exactly as before.

**The question for Bill, in one line:** when the member's own request is what forces the
authority expansion, is HIP's consent prompt an OFFER, an AUTHORIZED_OPERATION, or
outside the taxonomy because it is not system-initiated at all?

**A third answer is available and is NOT being taken unilaterally:** site 7 may simply be
out of R1's scope, because R1 governs *system-initiated* utterances and this one is not.
That reading is coherent, and it is still a ruling — R1's scope boundary is exactly what
is in question, and a session deciding it would be deciding what the taxonomy covers.

## 4. WHAT WAS BUILT

**`harness/initiation.py`** — `InitiationClass`, an `Enum` with exactly three members, and
`emit_or_suppress()`, R1's gate.

- **The closed set is enforced at the API, not by convention.** `emit_or_suppress` accepts
  ONLY an `InitiationClass` member. The **string** `"offer"` is suppressed exactly as
  `None` is (item 1: *"a code change to one enum, not a string anywhere"*). A vocabulary
  that accepts its own names as strings grows by typo — R29's lesson, applied to a second
  registry.
- **A standing test asserts the exact three-member set**, as a set comparison rather than a
  count, so a RENAME trips it too.
- **Naming discrepancy resolved in the open:** the REQ's §3 spells the second class
  `AUTHORIZED_SAFETY_INTERRUPT`; HA-01 spells it `SAFETY_INTERRUPT`. The dispatch's
  spelling is the member; the REQ's is an **alias that resolves to it**, so a reader
  coming from the REQ is not silently wrong and the set is still three.
- **Suppression is `None`, not an exception.** R1's remedy is silence; raising on a live
  speech path is louder than the rule asks.
- **Governed-decision record** appended to `logs/initiation/initiation_decisions.jsonl`,
  fsynced (item 2: *"recorded as a governed decision, not silent"*).
  **THE SUPPRESSED TEXT IS NOT RECORDED — only its length.** Suppressed speech is speech
  the system was not authorized to make; copying it into a durable log creates exactly the
  record R20/R21 spend their length keeping out of household data.
  **NAMED LIMIT: suppressions only, no denominator.** The log answers "which initiations
  were suppressed", never "what fraction". Logging every classified emission would put a
  disk write on every reply turn, which item 4's "changes nothing about what the system
  does today" does not obviously license. Wanting the denominator is a deliberate change.

**`harness/orchestrator.py` step 4 — WIRED.** The one real speech egress in the text path
now routes through the gate declaring `AUTHORIZED_OPERATION`, and `reply` is returned
byte-for-byte. This is the point of wiring it rather than shipping another module with
synthetic tests: `purpose_trigger` and `offer_gate` each confess in their own docstrings
that they have **no real creator path to assert against**. This one does.

**THE READING BEHIND THAT CLASSIFICATION IS FLAGGED, NOT ASSUMED.** A reply to a member's
question is not "initiation" under R1's own words. Item 4 nonetheless directs that today's
authorized speech classify as `AUTHORIZED_OPERATION` and keep flowing, so it is declared —
in the code comment as well as here. What it actually buys: **the egress can no longer emit
without a declared class**, so a future initiation site added above that line cannot reach
a member by forgetting to classify. It gets silence and a record.

## 5. WHAT WAS DELIBERATELY NOT DONE

- **No offers created.** `OFFER` is a name in a closed set. Nothing authors, renders or
  presents one. §12 steps 2–9 are not started.
- **Nothing HIP says today changed.** Sites 3–7 and 10 are not gated; the gate at site 1
  returns its input unchanged.
- **Site 7 not classified** (§3).
- **The voice pipelines are not gated.** They emit through pipecat rather than the
  `SpeechIO` seam, so gating them is a different shape of change and is not step 1's job.
  Named so it is not mistaken for coverage: **the gate covers the text path's egress only.**

## 6. FAULT TWIN + ANTI-VACUITY (item 3)

`eval/test_initiation_taxonomy.py` — **17 cases, 17 pass.**

| Case | Proves |
|---|---|
| closed-set | exactly `{AUTHORIZED_OPERATION, SAFETY_INTERRUPT, OFFER}`, by set equality |
| alias | the REQ's `AUTHORIZED_SAFETY_INTERRUPT` resolves to the same member; still three |
| **FAULT TWIN** ×6 | `None`, `"offer"`, `"AUTHORIZED_OPERATION"`, `"authorized_operation"`, an int, an object → all **suppressed** |
| record | the suppression is recorded; **and the utterance text is asserted ABSENT from the record** |
| **ANTI-VACUITY** ×3 | each of the three classes passes its text through **byte-for-byte** |
| empty-text | a valid class with empty text is NOT a suppression — declaring a class and saying nothing is a different event |
| **egress fault twin** | unclassified → nothing reaches the speech seam, one record written |
| **egress anti-vacuity** | classified → the reply reaches the seam unchanged |
| structural | **AST** (not a regex — a regex matches the comment block) asserts the shipped `handle_turn` calls `emit_or_suppress` with an `InitiationClass` **member, not a string** |

**What the egress pair does NOT prove, stated in the test file itself:** it does not
construct an `Orchestrator` and drive `handle_turn` end to end (that needs a router, a
graph and a model). It resolves the gate through `harness.orchestrator`'s own namespace,
so a removed import breaks it; the AST test carries the "shipped line is shaped this way"
half. Neither alone is the claim.

## 7. RUNS (item 6)

**A CAUGHT GAP, REPORTED WITH BOTH ATTEMPTS.** The FIRST `--layer 7` run reported the
battery at **672 passed / 9 xfailed — unchanged**, i.e. the 17 new tests did not run. The
standing battery is an **explicit file list** in `scripts/run_harness.sh`, not a directory
scan, and a new file is invisible to it until it is named. That list's own comment block
says exactly why it exists: an unlisted battery "could regress to green-by-deletion without
a single run turning red" (D-36 finding (b)). `eval/test_initiation_taxonomy.py` was added
to the list and `--layer 7` re-run. **Both runs are reported because a silently re-run check
is indistinguishable from a cherry-picked one.**

| Run | Result |
|---|---|
| Standing battery, FIRST run (file not yet listed) | 672 passed, 9 xfailed — **the 17 new tests did not run** |
| Standing battery, after registering the file | **689 passed, 9 xfailed** — 672/9 baseline + exactly the 17 added tests |
| `--layer 7` L7 | **27/27** |
| `--layer 7` L7V2 | **27/28** (1 skipped — the opt-in live-output check) |
| AUDIT / DISC / SCHEMA / VOICE | **8/8 / 1/1 / 1/1 / 1/1** |
| **RATCHET** | **PASS — no scenario regressed vs baseline** |
| Memory harness | **13/17** — failures exactly {MEM-115, MEM-116, MEM-117, MEM-118}, inside the D-109/D-110 pin |

`--full` NOT run; Requirements Discipline item 12 is NOT satisfied and is not claimed —
the dispatch named three runs and `--full` was not among them.

## 8. FINDINGS

1. **Site 7 needs a ruling** (§3). The only thing blocking a complete answer to item 2.
2. **`harness/control_flow.py`'s own section comment is stale.** It reads *"Main handlers
   (stubs — NOT connected to the pipeline)"*, and each handler's docstring says *"Phase 3
   wiring: orchestrator calls this…"* as future tense. **`server/voice_orch.py` calls both
   handlers today**, at four sites. Not corrected here — correcting a comment is a code
   change and HA-01's scope is step 1 — but it materially misleads a reader assessing what
   is live, which is how this dispatch nearly under-rated site 7.
3. **The taxonomy governs nothing yet, and that is the honest state.** With zero
   system-initiated sites, A1 holds today without changing an utterance. Its value is
   prospective: the gate is in place before the first initiation site exists.
4. **The gate covers the text path only** (§5). The voice pipelines emit outside it.
5. **A new battery does not run until it is named in `scripts/run_harness.sh`** (§7). Fixed
   for this dispatch's file. Worth knowing as a standing hazard: the list is manual, and
   the failure is silent — a green run and an un-run battery look identical.
6. **HA-01 FOUND THAT ITS OWN PREDECESSOR LEFT ONE UNREGISTERED, AND IS NOT FIXING IT
   HERE.** `eval/test_sensitivity_no_default.py` (D-R-196, 23 cases) is absent from that
   list — and could not simply be added, because it is a **standalone script** with a
   `main()`, not a pytest module: pytest would import it and collect zero tests, which is
   worse than absence because it would look registered. So **D-R-196's fault twins run only
   when invoked by hand**, exactly the exposure finding 5 describes. Recorded against
   D-R-196's own report, which claimed those 23 cases as evidence without noting they sit
   outside the standing battery. Fixing it means either converting that file to pytest
   functions or adding a separate invocation line — a change to another dispatch's
   deliverable, outside HA-01's scope, and Bill's call.
