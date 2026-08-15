# DISPATCH_HA28_OFFER_ACCEPTANCE — R23 wiring finished, A1–A20 measured

Status: BUILT (measurement dispatch)
Reconciled-Against: roadmap `4c6b51d` (pre-dispatch HEAD)

**HA-28** | 2026-08-10 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD + ACCEPTANCE RUN**
**GOVERNING REQ:** `REQ_OFFER_MECHANISM__…__v20260806_1625.md`, acceptance table A1–A20.
**`REQ_OFFER_MECHANISM` IS NOT RULED MET. Bill rules after reviewing the table.**
**Fixtures only — nothing presents to a real member, nothing enabled.**

## VERDICT SUMMARY

| | count |
|---|---|
| **PASS** | **11** |
| **FAIL** | **1** |
| **CANNOT RUN** | **8** |

**A19 is the FAIL**, and it is a real defect found by executing the clause rather than
reading the code. §3 has it in full.

---

## 1. ITEM 1 — R23 WIRING FINISHED

**Every `ledger.present()` caller was enumerated first: eight, all in test fixtures. There is
no production caller** — the offer path is not wired to a live turn, which is itself part of
why so much of A1–A20 cannot run.

`present()` now takes `instance=` (and `situation=` when held) and **assembles the full
sixteen-field R23 block itself**, so a caller cannot write the legacy three-field event by
forgetting to build one. All eight call sites updated.

### A scope limit, stated rather than crossed

**`instance` is OPTIONAL, not required.** Making it mandatory would refuse calls that succeed
today — a **behaviour change**, and item 1 stops at record population and says to report a
dependency rather than cross it. So the legacy shape is still *reachable* by omitting the
parameter, and enforcement is by standing test rather than by a refusal this dispatch was not
authorised to add. **A test pins exactly that**, and fails loudly if the parameter ever
becomes mandatory without its own dispatch.

### The standing test, as item 1 specifies it

`test_every_event_of_every_terminal_lifecycle_carries_all_r23_fields` — one complete lifecycle
per terminal outcome, **every** governed event read back, fields compared **directly against
`R23_FIELDS`**, failing on any missing one. Plus
`test_no_supported_transition_writes_the_legacy_three_field_event`.

**Completeness is never inferred from successful execution.** HA-27 found a 3-of-16 record
sitting behind four *passing* lifecycle tests, for exactly that reason.

**The wiring test passes. A1–A20 began only after it did.**

## 2. HOW EACH VERDICT WAS DECIDED

- **PASS** — executed in this dispatch, or covered by a standing test **that ran in this
  dispatch**. 222 offer-related tests were run today across eight batteries; per-file counts
  are in §5.
- **FAIL** — the clause ran and the observed behaviour violated the requirement.
- **CANNOT RUN** — required machinery does not exist, or the required state cannot be
  produced. **What is missing is named.**

**No clause is marked PASS on evidence from an earlier dispatch.** Where a standing test
carries a clause, that test was executed today and is named.

## 3. THE FAIL — A19, PROVEN ACROSS TWO PROCESSES

**A19 (R23–R24):** *"Record reconstruction proves trigger, wording, requested delta, response,
exact scope change, and spent state without exposing decline as profile data."*

Five of six reconstruct from the record alone, executed:

```
trigger        : care-function-registry / care_function_enabled
requested delta: delta:0b722a4973868d943c0aad6a377a7e46
response       : ACCEPTED via explicit_response
scope change   : [] -> ['audience:care_team', 'purpose:medication_adherence']
spent state    : True
```

**"Wording" does not.** The record carries `template_id` + `template_version` and **no slot
values and no rendered text**. Those live on the `OfferInstance` — and
`OfferInstanceRegistry` is **in-process only**, which its own docstring states.

**Executed across two real processes**, not inferred:

```
process 1 (write): words_shown = "Maya, may I notify your daughter?"
process 2 (read) : record_survived            = true
                   offer_instance_id_in_record = offer:6d6156a807...
                   template_identified         = offer.med v1
                   instance_recoverable        = FALSE
                   exact_words_recoverable     = FALSE
```

**The record survives the restart and the words do not.** R24 requires the record to contain
enough to prove *"exactly what words were shown"*; after a restart it proves only which
template was used. A member disputing what they were shown could be told the template id and
nothing more.

**Scope of the failure, stated precisely:** within a single process the words ARE recoverable
from the live registry. It fails across restart — which is the case that matters for a
governed record, since a record whose meaning evaporates on restart is not a record.

**WHAT IS MISSING:** a durable offer-instance store, or slot values + rendered text carried
in the R23 event itself. **Not built here** — it is a storage change to the offer path, and
this dispatch measures the requirement rather than silently finishing product behaviour the
acceptance run discovered.

## 4. A1–A20

| Clause | Verdict | Executed evidence | Standing test (ran today) | Remaining gap |
|---|---|---|---|---|
| **A1** (R1) | **PASS** | three initiation classes closed; unclassified suppressed | `test_initiation_taxonomy` — 17 | — |
| **A2** (R2–R3) | **CANNOT RUN** | — | — | **No reminder-delivery path exists.** Nothing can deliver an authorized reminder, so "delivered without an offer" cannot be observed, and neither can the block on broader collection. |
| **A3** (R4) | **PASS** | `create()` refuses a non-`Situation` and a `situation_id` not derived from its own fields; the four kinds are a closed enum | `test_offer_instance` — 36, `test_situation_identity` — 32 | — |
| **A4** (R5) | **PASS** | six non-trigger fault twins: time, engagement, graph fullness, prior yes, prior no, template revision | `test_situation_identity` — 32 | — |
| **A5** (R6) | **PASS** | duplicate delivery, retry, restart and equivalent resubmission all resolve to one `situation_id` | `test_situation_identity` — 32 | — |
| **A6** (R7) | **CANNOT RUN** | — | — | **No bundle/staircase delta machinery exists.** "One trigger maps to one minimal delta" has no minimality check to exercise, and no bundle or staircase twin exists to refuse. |
| **A7** (R8) | **PASS** | spent on presentation; re-presentation refused after every terminal state and across a real process kill | `test_spend_ledger` — 18, `test_offer_response` — 32 | Template change / elapsed time not separately exercised — both reduce to "already spent", which is covered. |
| **A8** (R9) | **CANNOT RUN** | — | — | **No transport layer exists.** There is no delivery step, so a pre-delivery transport failure cannot be produced and post-delivery retry cannot be distinguished from it. |
| **A9** (R10) | **CANNOT RUN** | — | — | **No member-initiated capability path exists.** The "situation remains spent" half is covered by A7; the member re-initiating the same capability cannot be executed. |
| **A10** (R11–R13) | **PASS** | import-closure scan over the offer path: no model client, randomness or generation reachable; no experiment/variant/arm identifier among defined names; slots are typed and validated | `test_offer_purity` — 13, `test_offer_instance` — 36 | Static closure only — a computed dynamic import would evade it (disclosed in the module). |
| **A11** (R14) | **CANNOT RUN** | — | — | **No explanation feature exists.** There is no "requested explanation" path, so fixed explanatory content cannot be exercised. |
| **A12** (R15) | **CANNOT RUN** | boundary half proven: every non-resolving `ResponseKind` refuses, incl. DEFERRAL and CAREGIVER_PREFERENCE | `test_offer_response` — 32 | **The missing utterance→`ResponseKind` classifier.** A12's check names utterances ("whatever you think"); without a classifier they cannot be carried end to end. **The boundary is proven; the path to it is not built.** |
| **A13** (R16) | **PASS** | acceptance yields `scope_after == scope_before ∪ delta` by set equality; empty dimensions grant nothing | `test_offer_response` — 32, `test_governed_record` — 36 | Widening twins are covered as *absence of tokens*; there is no separate "widened audience" adversary object. |
| **A14** (R17) | **PASS** | wrong principal refused and recorded; representative for a different domain refused; wildcard domain refused at construction | `test_offer_response` — 32 | — |
| **A15** (R18) | **PASS** | tampered instance → INVALIDATED, scope unchanged; integrity checked before the responder | `test_offer_response` — 32 | — |
| **A16** (R19) | **CANNOT RUN** | — | — | **No revocation or narrowing path exists** in the offer modules. Neither execution nor the no-delay property can be observed. |
| **A17** (R20–R21) | **PASS** | write boundary refuses every destination Ruling 5 names and records it; import-closure ban; the assembled `local_system_prompt` contains no offer identifier; suppression still works | `test_control_plane_isolation` — 38 | **Caregiver notification is not separately exercised** — no notification path exists to check. |
| **A18** (R22) | **PASS** | control-plane metric scan clean; **and a repo-wide scan of `harness/` + `memory_engine/` for conversion-objective names returned NONE**; reads gated to R20's four named purposes | `test_control_plane_isolation` — 38 | Scan is name-based over first-party code; it cannot see an objective expressed only in a config or a downstream product system. |
| **A19** (R23–R24) | **FAIL** | §3 — reconstruction executed across two processes | `test_governed_record` — 36 (field completeness passes) | **Exact wording unrecoverable after restart.** Needs a durable offer-instance store, or slot values + rendered text in the R23 event. |
| **A20** (R25) | **PASS** | manifest set-equal to accumulated deltas; derived not stored, proven by replay; declined/lapsed/invalidated contribute nothing; decline appears only in the member's own history | `test_governed_record` — 36 | — |

### The eight CANNOT RUNs are one shape

**A2, A6, A8, A9, A11, A16** need product behaviour that does not exist: a delivery path, delta
minimality, a transport layer, a member-initiated capability path, an explanation feature,
and a revocation path. **A12** needs the classifier. **None was built here** — item 3 is
explicit that this dispatch measures the requirement and does not silently finish what the
acceptance run discovers.

**A9 and A12 are partially covered and are still CANNOT RUN**, because half a clause executed
is not the clause.

## 5. RUNS

| Run | Result |
|---|---|
| **Offer batteries (for A1–A20)** | **222 passed** — initiation 17 · situation 32 · instance 36 · spend 18 · purity 13 · response 32 · isolation 38 · record 36 |
| **All batteries** | **970 **SUPERSEDED as a canonical battery result — the exact invocation was not recorded and the result is contradicted by the documented whole-suite invocation (HA-31: 1048 passed / 31 failed). Old number preserved, never deleted.** passed, 0 failed** (963 → 970: +7 from the R23 wiring test) |
| **`--layer 7`** | L7 **27/27** · L7V2 27/28 · AUDIT **9/9** · DISC/SCHEMA/VOICE 1/1 |
| **RATCHET** (binding) | **PASS · exit 0** |
| **Memory harness** | **13/17 — INSIDE THE PIN** (13–15). Same four: MEM-115/116/117/118 |
| **`--full`** | §5.1 |

### 5.1 `--full`

```
batteries: 970 passed, 0 failed
== L7: 27/27  == L7V2: 27/28  == AUDIT: 9/9  == DISC/SCHEMA/VOICE: 1/1
== L1: 14/15  == L2: 24/35 (10 skip)  == L3: 3/3  == L4: 30/34 (4 skip)  == L6: 0/1
[live-layers] appended 88 scenario result(s)  (run_id=20260810T153311_4c6b51d)
RATCHET FAIL — regressed vs baseline: ['L2:routing_showcase.T04']
NEW FAILURES (not in baseline): ['L1:P12', 'L6:record-invariants']
BINDING TESTS PASS. LIVE-MODEL TESTS HAVE FAILURES — SEE RUN LOG.
```

**Every binding layer green; exit 0.** The three live reds are the same already-characterised
set. **No gate claim is made from this run**, per item 5.

`L6:record-invariants` across eight collected runs: `FAIL FAIL PASS PASS PASS FAIL FAIL FAIL`
— **five red, three green**, no code change explaining the transitions. Collector: **eight
`--full` runs, 704 rows.**

## 6. CLAIM IMPACT

**CLAIM IMPACT: no claim gained new evidence. No status changed.**

Stated precisely, because this dispatch ran 222 tests and it would be easy to read that as
progress on several claims:

- **C-06, C-07, C-14, C-15** all have offer-path evidence, and **every test supporting them
  was already standing before today.** Re-running a standing test confirms it still holds; it
  is not *new* evidence.
- **A19's FAIL is evidence against nothing currently claimed** — no ledger claim covers R23/R24,
  which HA-27 flagged and the full cap (15/15) prevents closing without a retirement.

**No claim status is changed here.** That is Bill's ruling.

## 7. WHAT THIS DISPATCH DOES NOT DO

- **Does not rule `REQ_OFFER_MECHANISM` MET.** **12 PASS, 1 FAIL, 7 CANNOT RUN** — the table is

> ### CORRECTION 2026-08-10 — the verdict counts were wrong. Caught by **Bill**.
>
> **This line as committed read, verbatim:** *"Does not rule `REQ_OFFER_MECHANISM` MET. 11 PASS,
> 1 FAIL, 8 CANNOT RUN — the table is …"*
>
> **The correct counts are 12 PASS / 1 FAIL / 7 CANNOT RUN**, and they are **counted from the
> A1–A20 table in §4 of this document**, row by row, not re-derived from memory:
>
> | verdict | rows | count |
> |---|---|---|
> | **PASS** | A1, A3, A4, A5, A7, A10, A13, A14, A15, A17, A18, A20 | **12** |
> | **FAIL** | A19 | **1** |
> | **CANNOT RUN** | A2, A6, A8, A9, A11, A12, A16 | **7** |
> | | **total** | **20** |
>
> The error was in the summary line only — **§4's table itself was correct as committed and is
> unchanged.** Per the correction pattern the wrong numbers are preserved above rather than
> silently patched. The conclusion this line supports is unaffected: the REQ is still not MET.

  the deliverable, the ruling is Bill's.
- **Does not build the classifier**, per item 3.
- **Does not build the six missing product paths** the CANNOT RUNs name.
- **Does not fix A19.** The gap is named; the storage change is its own dispatch.
- **Enables nothing.** Fixtures only.

## 8. FINDINGS

1. **A19 FAILS, proven across two processes** (§3) — the record survives a restart and the
   words shown do not.
2. **Eight clauses cannot run for want of product behaviour** (§4), not for want of testing.
3. **`present()` had no production caller at all** (§1) — all eight were fixtures, which is
   the same fact the CANNOT RUNs keep expressing from different directions.
4. **The R23 wiring is enforced by test, not by refusal** (§1) — making `instance` mandatory
   is a behaviour change, and item 1's own limit stops short of it.
5. **A18 is clean repo-wide, not just in the control plane** (§4) — the scan found no
   conversion-objective name anywhere in `harness/` or `memory_engine/`.
