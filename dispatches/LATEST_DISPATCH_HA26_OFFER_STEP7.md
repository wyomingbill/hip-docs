# DISPATCH_HA26_OFFER_STEP7 — control-plane isolation: a decline is not a member fact

Status: BUILT
Reconciled-Against: roadmap `6f565ee` (pre-dispatch HEAD)

**HA-26** | 2026-08-10 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD + RIDER**
**GOVERNING REQ:** `REQ_OFFER_MECHANISM__…__v20260806_1625.md` — **RULING 5**, **R20**
(control-plane isolation), **R21** (no downstream interpretation), **R22** (audit use is
non-optimizing).
**Nothing ruled MET. Fixtures only — nothing presents to a real member, nothing enabled.**

**CLAIM IMPACT: C-06, C-14** — see §8.

---

## 1. WHAT WAS BUILT

`harness/control_plane_isolation.py` + `eval/test_control_plane_isolation.py` (**38 tests**).

**Two mechanisms, because either alone is insufficient:**

| | Catches | Blind to |
|---|---|---|
| **Write boundary** (`refuse_member_fact_write`) | a runtime attempt to store a response as a member fact | an import that has not been called yet |
| **Structural ban** (`assert_control_plane_is_isolated`) | the attempt being *possible* at all | a runtime dictionary key |

**The write boundary alone would be behavioural**, and a behavioural check only fires on the
call someone actually makes. The structural ban is what makes *"a decline cannot reach the
graph"* a property of the code rather than a promise about it.

### The write boundary has no success path, deliberately

`refuse_member_fact_write` **always refuses.** There is no branch on which it succeeds, and a
test asserts the function body contains no conditional. **A function that sometimes permitted
an offer response into the graph would need a rule for when — and Ruling 5 does not have
one.** The only correct answer is no, so the only behaviour is refusal plus a record.

### R20's four reads, named by the caller

`assert_permitted_read` takes the purpose and refuses anything outside R20's closed list
(`suppress_spent_offer`, `member_own_history`, `validate_grant_state`, `compliance_audit`).

**The failure mode this guards is not malice.** *"We needed the data"* is how a compliance
read becomes a personalization read without anyone deciding to make it one. Requiring the
caller to name which of the four it is makes the fifth use visible at the call site.

### R22 — conversion metrics banned by EXISTENCE, not by use

`FORBIDDEN_METRIC_FRAGMENTS` is checked against defined names in the control plane. **An
`acceptance_rate` counter is a conversion metric whether or not anything reads it**, because
its existence makes optimizing on it a one-line change.

## 2. THE STRUCTURAL BAN — Ruling 5's list, as modules

`FORBIDDEN_DESTINATIONS` maps each thing Ruling 5 names to real modules, grouped by the
ruling's own categories so the mapping can be checked rather than trusted: the household
graph (`memory_engine.store`, `.consolidate`, `.recall`, `.api`, `extraction_queue`,
`fact_change`, `write_rule`, `sio`), model context and inference (`orchestrator`,
`injection_contract`, `disclosure`, `interpreter`, `frontier_client`, `realtime_adapter`),
embeddings/summaries (`mem0_store`, `zep_store`), and trust/care projections
(`memory_engine.trust`, `care_team_keys`).

**A test asserts every category Ruling 5 names is covered by at least one real module** —
otherwise a category could be "banned" with nothing enforcing it. That test failed on its
first run (my destination descriptions said "model-context assembly" while Ruling 5 says
"model context"), which is exactly what it is for: the mapping is checked against the
ruling's own words, not against my paraphrase of them.

### Result on the real control plane

```
scanned 11 modules — leaks: 0 — metric offenders: 0
  spend_ledger · offer_response · offer_instance · offer_gate · initiation
  material_change · purpose_trigger · inference_permit · representation_class
  write_origins · attribute_vocabulary
```

**Clean on the first run.** Worth naming why rather than claiming credit: HA-22 split
`CANONICAL_ATTRIBUTES` into a leaf module to get the *generative* surface out of the offer
path, and that same split is what keeps `extraction_queue` — a forbidden destination here —
out of this closure too. **One fix, two requirements.**

## 3. ITEM 3 — FOUR FAULT TWINS, EXECUTED

### (d) ANTI-VACUITY FIRST — the decline exists, in the control plane

Every absence test below passes trivially if the decline never happened. **Ruling 5 says a
decline lives in the control plane, not that it vanishes.**

```
state: DECLINED · spent: True
governed_decision transitions: ['PRESENTED', 'DECLINED']
re-presentation after decline -> SituationSpent   (R20's first permitted read)
```

### (a) An attempted decline write is refused and recorded

Parametrized over **every destination Ruling 5 names** — household knowledge graph,
embeddings, summaries, member traits, trust scoring, vulnerability scoring, care-team
projections, model context, inference inputs, operator optimization. Each refuses with
`RULING 5` and appends `reason=member_fact_write_refused`.

**The refusal record carries the shape of the attempt, never the response.** A refusal log
that copied the response out of the control plane would be the leak it is refusing — asserted
by a test.

### (b) After a decline, the model sees nothing about it — **read, not inferred**

This is the load-bearing test. It builds the **real** `local_system_prompt` the model
receives — via `TurnOrchestrator`, constructed as layer 7's own ctx-strip probe constructs
it, with an empty hot context — and asserts that **no identifier belonging to the declined
offer appears in it**: `situation_id`, `offer_instance_id`, `authority_delta_id`,
`"DECLINED"`, `"declined"`, and the capability name.

**Checking the output surface rather than the code paths leading to it is the whole point.**
It would catch a decline arriving in model context by *any* route — a fact write, a summary,
a trait, a well-meaning "the member declined this" hint — because it does not care how the
text got there, only whether it is there.

The graph half is asserted separately: `read_user_facts("maya")` carries no trace of the
situation, instance, or transition.

### (c) A scratch leak turns the scan red

Injected `from memory_engine.store import encode` into `harness/spend_ledger.py`:

```
RED: RULING 5 / R20-R21 — the control plane can reach a forbidden destination:
  harness.spend_ledger imports 'memory_engine.store' -> the household knowledge graph
```

**Restored byte-for-byte** — `git diff --stat` reports no change to that file. Green again at
11 modules, 0 leaks.

The battery also carries a **standing** version of this twin that mutates nothing: scanning
`memory_engine.store`, `harness.fact_change` and `harness.orchestrator` as entry points
produces leaks on every run, so the check is proven able to go red without a file edit that
could be left behind by a crash.

## 4. ANTI-VACUITY ON THE SCAN ITSELF

The same three refusals HA-22 established, for the same reasons: **zero modules scanned**,
**a closure that does not expand past its entries**, and **a forbidden destination that does
not exist** (a rename would otherwise disarm the guard silently, forever). Plus a fourth
here: the metric-fragment list must be non-empty and must actually match probe strings.

## 5. ITEM 5 + THE DECLARATION TRAP

The battery was refused before registration (`assert not ['test_control_plane_isolation.py']`)
and passes registered.

**`harness/control_plane_isolation.py` is deliberately NOT declared to either scan, and a
draft of this section wrongly said it was.** Checked before publishing, found false, and
corrected here rather than made true by adding a line of code:

- It is **not an offer-path module** — it renders nothing and is never called during an
  offer. Adding it to `OFFER_PATH_ENTRY_MODULES` would widen HA-22's "no generative surface"
  claim to cover a checker, which is not what that scan asserts.
- It is **not control-plane state** — it holds no offer state. Adding it to
  `CONTROL_PLANE_MODULES` would make the scan scan itself, and its `FORBIDDEN_DESTINATIONS`
  tuple contains module-name **strings**, not imports, so a self-scan would prove nothing
  either way.

**The declaration rule still holds for the modules it is about:** a new module that *holds
offer state* goes in `CONTROL_PLANE_MODULES`; a new module *in the offer path* goes in
`OFFER_PATH_ENTRY_MODULES`. Both scans are declaration-driven and neither can detect an
undeclared member — which is exactly why HA-25's trap fired and why this claim was worth
verifying instead of asserting.

## 6. RIDER — CLAIMS LEDGER v3

`docs/deliverables/HIP_ClaimsLedger__v3-c14-and-restored-citations__v20260810_0812.md`.
v2 marked **SUPERSEDED** and retained unaltered; **LATEST** repointed; MANIFEST Section B and
INDEX updated. Recorded reason: *"Add C-14 (Bill's wording, 2026-08-10) and restore the six
dropped evidence citations."*

**C-14, Bill's wording verbatim, status PARTIAL — Bill 2026-08-10:**

> *"Exact-scope offer acceptance. Once a response has been classified as an acceptance, HIP
> grants exactly the authority described by the offer, grants no additional authority, and
> only the intended member may accept it."*

Evidence: HA-25's standing battery. Timeline: **after the response classifier is built** —
which is the honest dependency HA-25 flagged, now recorded in the ledger rather than only in
a dispatch doc.

**C-01..C-13 claim wording is byte-identical to v2**, verified column by column.

### One discrepancy in the rider, reported rather than resolved silently

The rider says *"restore the six dropped evidence citations"* and then names **three cells**:
`D-R-194` → C-08, `HA-04/HA-05` → C-05, `D-146` → C-13. **Those three are restored** (four
IDs across three cells).

HA-23's finding counted **six cosmetic evidence changes**, of which three dropped IDs and
three were wording/punctuation (`REQ_STRUCTURAL_REFUSAL` → "Structural-refusal" in C-04, a
comma → semicolon in C-06, and C-01's substantive refresh). **Those three were NOT touched**,
because the rider's own next sentence is *"No other wording changes."* The parenthetical is
specific and the instruction is restrictive; where they could conflict, both were obeyed by
doing exactly what was named. **Flagged so the count is not read as six cells restored.**

## 7. RUNS

| Run | Result |
|---|---|
| **Batteries** | **934 passed, 0 failed** (896 → 934: +38 from this dispatch) |
| **`--layer 7`** | L7 **27/27** · L7V2 27/28 · AUDIT **9/9** · DISC/SCHEMA/VOICE 1/1 · `KEY-HYGIENE-ZERO-ORPHAN` PASS |
| **RATCHET** (binding) | **PASS · exit 0** |
| **Memory harness** | **13/17 — INSIDE THE PIN** (13–15). Same four: MEM-115/116/117/118 |
| **`--full`** | §7.1 |

### 7.1 `--full` — live layers logged, no gate claim

```
batteries: 934 passed, 0 failed
== L7: 27/27  == L7V2: 27/28  == AUDIT: 9/9  == DISC/SCHEMA/VOICE: 1/1
== L1: 14/15  == L2: 24/35 (10 skip)  == L3: 3/3  == L4: 30/34 (4 skip)  == L6: 0/1
[live-layers] appended 88 scenario result(s)  (run_id=20260810T142129_6f565ee)
RATCHET FAIL — regressed vs baseline: ['L2:routing_showcase.T04']
NEW FAILURES (not in baseline): ['L1:P12', 'L6:record-invariants']
BINDING TESTS PASS. LIVE-MODEL TESTS HAVE FAILURES — SEE RUN LOG.
```

**Every binding layer green; exit 0.** The reds are live-layer and already characterised.

**`L6:record-invariants` flipped again.** Its full history in the collector, six runs:

```
FAIL  FAIL  PASS  PASS  PASS  FAIL
```

**Three red, three green, and it was green one run ago with no code change between.** That is
the clearest argument yet for item 12's amendment: under the old rule this dispatch would
have "failed" on a scenario whose last three runs passed.

Collector series: **six `--full` runs, 528 rows.** Still nowhere near enough to set a rule
from, and none is set.

## 8. CLAIM IMPACT

**CLAIM IMPACT: C-06, C-14.**

- **C-06** *("An offer, once presented for a situation, can never be re-presented…")* — the
  decline path now has standing evidence that a spent situation refuses re-presentation
  *after a terminal transition*, which is where C-06's guarantee is actually load-bearing.
  **Reinforcement of an existing status, not a change.**
- **C-14** — added to the ledger this dispatch at Bill's wording and his PARTIAL. **HA-26
  produced no new evidence for it**; C-14's evidence is HA-25's battery. Naming it here
  records that the claim now exists, not that it moved.

**No claim covers Ruling 5 itself.** The isolation built here — *a decline is control state
and reaches neither the graph nor model context* — is a substantial privacy guarantee with
**no ledger claim**, the same gap HA-25 flagged for R16 before C-14 closed it. **Flagged for
Bill: the cap is 15 and 14 are now used.**

## 9. WHAT THIS DOES NOT CLAIM

- **The structural ban is static.** A dynamic import with a computed name would evade it —
  the same disclosed limit as HA-22's purity scan.
- **The model-context test proves the prompt is clean for an empty hot context.** It does not
  prove every possible turn shape is clean; it proves nothing in the offer control plane puts
  offer state into the prompt assembly path, which is what Ruling 5 asks.
- **Nothing is enabled.** No live path, no real member, no classifier — HA-25's gap stands.
- **Nothing ruled MET.** A1–A20 unattempted; the REQ remains DRAFT-RATIFIED-PENDING.

## 10. FINDINGS

1. **The control plane was already clean** (§2) — and HA-22's leaf-module split is why. One
   fix served two requirements.
2. **The category-coverage test caught my own paraphrase** (§2) — it checks Ruling 5's words,
   not mine, and failed until the descriptions matched.
3. **The write boundary has no success path** (§1), asserted structurally.
4. **The model-context twin reads the assembled prompt** (§3b) — output surface, not intent.
5. **The rider's "six" names three cells** (§6). Three restored, three untouched under "no
   other wording changes", both obeyed by doing exactly what was named.
6. **Ruling 5 has no ledger claim** (§8), with the cap now at 14 of 15.
7. **A draft of §5 claimed this dispatch's new module was declared to HA-22's purity
   scan. It was not, and it should not be** — it is a checker, not an offer-path or
   state module. Caught by verifying the claim before publishing rather than by adding
   a line of code to make a written sentence true.
