# DISPATCH_HA35_RELOCATION — mutation baseline repaired, RELOCATED built, HA-33 LANDED

Status: **ALL SEGMENTS COMPLETE — HA-33 LANDED, BINDING SET GREEN**
Reconciled-Against: roadmap `01aa901`
Filed: 2026-08-11 (HA-35)
Decision-Owner: Bill
Authority: Bill's ruling 2026-08-11 — repair the starting state, fix TD-R-181, then build, then HA-33
Predecessors: HA-34 (`01aa901`, the diagnosis), HA-33 (`a2c27be`, the fix that could not land)

Executed in the ordered sequence the ruling set. Each step's gate was checked before the next
began, and the census gate was the one that could have stopped everything.

---

## 1 — THE RESTORATION RECORD (written, provenance carried, 142/143 untouched)

Appended to `logs/mutation_survivors.jsonl` as record 144. **It is not a sweep result and says
so in its own body** (`"record_type": "restoration"`, `"is_sweep_result": false`).

| field | value |
|---|---|
| source record | index **141**, `2026-08-10T22:50:28.012131+00:00` |
| content digest | `eeb95a7bfa024faa` — sha256 over 141's survivor + killed coordinate sets, so the re-affirmation is checkable rather than asserted |
| source revision | `a2c27be` verified; `head_at_source_run` recorded separately as `5fa9d9c`, with the reason the two differ |
| evidence | HA-34's dispatch doc **and** its commit `01aa901` |
| authority | Bill, 2026-08-11, dispatch HA-34 |
| 142/143 | `"retained": true`, both timestamps recorded, with the full reason they are not the active reference |

**Verified after writing:** 145 records where there were 144; records 142 and 143 compared
**byte-identical** to their pre-append state; all 144 originals intact; the restoration's content
digest equal to record 141's. Nothing was deleted, modified or hidden.

The immediate effect, measured: `check_no_silent_disappearance` against the unpatched tree went
from the failure HA-34 predicted to **pass, 0 unaccounted** — the controlled baseline was live
again before anything else was touched.

**One property worth stating: `logs/` is gitignored.** The survivor log is not under version
control, so the restoration record's durable provenance is the record's own body plus this
dispatch — not a commit. Said plainly because "it's in the repo" would be wrong.

---

## 2 — TD-R-181 FIXED, BEFORE ANY GATE RUN

**The defect:** Layer 7 called `write_survivor_trend` unconditionally, outside any pass/fail
branch. A run that FAILED the disappearance check still replaced the baseline the next run would
be measured against.

**The fix is in the tooling, not in the caller's discipline.** `accounting_passed` is now a
REQUIRED keyword-only argument: a caller cannot persist a baseline without stating the verdict.
Passing runs append to `logs/mutation_survivors.jsonl`; failing runs append to
`logs/mutation_survivors_rejected.jsonl`, which `read_last_survivor_run` never reads. **Evidence
kept, baseline protected.** This deliberately mirrors the lock rule — acquisition is a
precondition of the tooling, not a step a session can reorder.

**Proven live, as the ruling required.** A deliberately failing scratch run (a phantom previous
survivor at `scratch/module.py:4242`, neither surviving nor killed nor carried):

```
accepted baseline BEFORE : 145 records, 3199846 bytes, sha 28b13091258232ef
scratch run verdict      : pass=False  unaccounted=1
accepted baseline AFTER  : 145 records, 3199846 bytes, sha 28b13091258232ef
  ACCEPTED BASELINE UNTOUCHED (byte-identical): True
  failed-run evidence recorded separately     : 1 new record in mutation_survivors_rejected.jsonl
  last accepted record still the restoration  : True
```

**That one synthetic record is still in the rejected log and is named here so it is not mistaken
for a genuine failed gate run** — its coordinates (`scratch/module.py:4242`) are self-evidently
fixture data. It is the live proof artifact; removing it would remove the evidence.

---

## 3 — TD-R-182 NOT FIXED

Left filed, per the ruling. `find_debt_carry` still cannot match `TD-R-` prefixed IDs.

---

## 4 — THE CENSUS: **33 / 33 / 0**

| # | measure | count |
|---|---|---|
| 1 | total persisted legacy survivors | **33** |
| 2 | uniquely reconstructible from the recorded revision | **33** |
| 3 | ambiguous or unrecoverable | **0** |

**Any ambiguous was a STOP, so this gate was checked before a line of the build was written, and
the first attempt did not pass it.** A content-only fingerprint (site text + enclosing statement
header) left **5 ambiguous** — four `return True` sites that collide inside one function, and one
legacy coordinate (`write_rule.py:358 swap_compare Eq->NotEq`) matching two distinct sites. That
was reported as a weakness of the candidate fingerprint, not treated as the source's ambiguity,
and the fingerprint was strengthened rather than the census accepted. **Declaring STOP on a
fingerprint I had chosen badly would have been the wrong answer.**

**Reconstruction was validated before being trusted.** Sites rebuilt from `git show a2c27be:<file>`
text were compared against the live module walk for all twelve targets: **135 sites, identical
`(index, operator, lineno)` on every one.** Only then was the census computed from it.

---

## 5 — THE BUILD

### The fingerprint — non-identity, on `Mutant` and on the persisted record

`_mutant_key` is **untouched**; identity remains `(module, func, operator, lineno)`. The
fingerprint is added beside it on `Mutant`, on `Survivor`, and in `_mutant_dict`.

It hashes three line-independent things: the site's **structural path** inside the function, the
**site expression's own source text**, and the **enclosing statement's header** — never the
statement's body, which would move the fingerprint whenever anything inside the block changed.

**What it is deliberately NOT stable under, stated rather than discovered later:** inserting or
deleting statements *inside* the same function changes the structural path, so the fingerprint
stops matching and the disappearance is refused as unaccounted. That is the safe direction. **This
mechanism only ever ADDS a way to account for a disappearance; it cannot turn a real one into a
pass** — and there is a standing test asserting exactly that.

**Collisions across all 135 sites of all twelve targets: 0.**

### The RELOCATED path

Placed in `check_no_silent_disappearance` after the debt check and before the unaccounted branch,
exactly as specified. A relocation requires **all** of: same module, function and operator;
identical **non-empty** fingerprint on both sides; a **different** lineno; and **unique 1:1 in both
directions**. Anything else falls through to unaccounted.

The record it produces names both coordinates — `old -> new`, accounted, not disappeared, still
surviving at the new coordinate, not killed, no debt.

### Legacy backfill — from the recorded revision, never today's lines

Appended as record 145, `"record_type": "baseline_backfill"`, citing the restoration record it
supersedes as the active baseline. **Guarded before it ran:** the target modules were asserted
clean and the live sweep asserted to reproduce the baseline's survivor set exactly — if the tree
were no longer `a2c27be`, the fingerprints would have been computed against the wrong lines, which
is precisely what "never today's lines" warns against.

- survivors: **33 of 33 fingerprinted, 0 absent**
- killed_mutants: 95 of 102 fingerprinted, **7 left ABSENT on purpose** — where more than one site
  shares a coordinate, the legacy record cannot say which it was, so the fingerprint is omitted
  rather than guessed. An absent fingerprint can never match a relocation; it fails closed.

### The four standing tests — `eval/test_mutation_relocation.py`, 10 tests

Proven **end to end** where possible: a real module written to disk, really swept, really shifted
by ten inserted lines, really re-swept — not hand-built dicts.

| # | property | how |
|---|---|---|
| 1 | relocation recognised on the FIRST run | real sweep, ten lines inserted above the gate, every survivor relocates by exactly +10 on the first comparison — no warm-up, no re-recording |
| 2 | baseline never rewritten by a failed run | accepted file byte-compared before/after a failing persist; plus `read_last_survivor_run` never returns a rejected record |
| 3 | same-function same-operator survivors stay distinct | every site in each `(module, func, operator)` group carries its own fingerprint; **plus the live case** — `classify`'s two adjacent `delete_last_operand(Or)` sites have different fingerprints |
| 4 | ambiguity fails closed | two candidates for one vanished survivor → FAIL; two vanished claiming one candidate → FAIL; a legacy survivor with no fingerprint → FAIL; a genuinely deleted survivor → still FAIL; same line → not a relocation |

---

## 6 — HA-33, REAPPLIED

Patch reapplied to `harness/write_rule.py` (+10) and `memory_engine/store.py` (+33). The five
`classify` survivors moved `:357/:358` → `:367/:368`, as predicted.

### Layer 7, exit 0 on the FIRST controlled run

```
LAYER 7 EXIT = 0
MUTATION-NO-SILENT-DISAPPEARANCE PASS
  5 disappearance(s) this run, all accounted for; 5 RELOCATED:
    classify [delete_last_operand(Or)]   :357 -> :367   fp=9f6fa8fcea8af46e
    classify [swap_compare Is->IsNot]    :358 -> :368   fp=fdaf772c1dab54be
    classify [swap_compare Eq->NotEq]    :358 -> :368   fp=9601a6515b7f9d16
    classify [delete_last_operand(Or)]   :358 -> :368   fp=d86ab7b837d08c7f
    classify [delete_last_operand(And)]  :357 -> :367   fp=86c1c4d450d66723
```

**All three conditions met:** the five accounted as RELOCATED, **0 unaccounted**, and **no new
survivor** — 33 survivors before and after, 135 generated / 102 killed unchanged. The two
`delete_last_operand(Or)` entries carry **different fingerprints**, which is the live proof that
same-function/same-operator sites stay distinct.

The passing run then advanced the accepted baseline to the new coordinates — via a **passing** run,
which is the whole point of the TD-R-181 fix.

### The seven absence proofs — now standing tests, `eval/test_write_state_validity.py`, 18 tests

| # | absence | evidence |
|---|---|---|
| 1 | no false success result | raises `InvalidWriteState`; **no return value was ever assigned** |
| 2 | no fact | no `new_fact_id` issued |
| 3 | no node | whole-graph fact count unchanged; fact_id set unchanged |
| 4 | no ciphertext | `encrypt_by_class` call count **0** |
| 5 | no seal | `create_fact_node` call count **0** |
| 6 | no key operation | **SAME OBSERVATION AS 5, recorded as such** — both happen inside `create_fact_node`, so this is one measurement supporting two claims, not two independent ones |
| 7 | no derivative | **evidence is 3's** — HA-33's original query relied on a `value` property Fact nodes do not carry and returned 0 trivially; zero nodes written is what actually supports it |

Both stated weaknesses are carried into the test file itself, in the test names and docstrings,
so a later reader cannot mistake them for independent corroboration.

Call counts are taken by wrapping the names `store` actually calls, so they measure the real path
rather than a re-import.

**Anti-vacuity:** all four canonical states (`supersede`/`augment`/`correct`/`unresolved`) still
WRITE — `node_delta=1` each, fresh `fact_id` each, and each returned id asserted to name a real
node. Without this, all seven absences would also pass on a guard that refused everything.

**Census and cleanup by captured ID.** The full pre-existing fact_id set and count are captured
BEFORE the first write; teardown deletes only ids this module created and then asserts the graph
returned to its exact prior state. **Measured: 12 Fact nodes before, 12 after, 0 owned by the
battery's synthetic principals.** No `DETACH DELETE` by owner — that is one typo from deleting
rows the battery never wrote, and HA-33 left four facts behind precisely because cleanup was an
afterthought.

**Reproduction rerun:** HA-33's exact call shape — `encode(write_state='not_a_real_state')`, which
returned an `EncodeResult` with a fresh `fact_id` while writing zero nodes — now **REFUSES**, and
still writes nothing. Extended to `""`, `"SUPERSEDE"`, `"augment "`, `"unknown"` and `None`, so a
guard that special-cased one string could not pass.

---

## 7 — THE FOUR COMMANDS

| # | command | result |
|---|---|---|
| 1 | canonical suite (unfiltered — the HEALTH CHECK) | **1076 passed / 31 failed / 10 skipped / 9 xfailed / 2 errors** |
| 1b | the BINDING standing battery, 51 files as `run_harness.sh` defines it | **998 passed / 0 failed / 9 xfailed** |
| 2 | `--layer 7` | **EXIT 0** — L7 27/27, L7V2 27/28 (1 opt-in skip), AUDIT 9/9 |
| 3 | RATCHET `--full` | **BINDING TESTS PASS** (exit 0). Live-layer regression `L2:routing_showcase.T04` — REPORTED, NOT GATING (item 12 as amended). `live-layer new failures: none` |
| 4 | memory harness | **13/17** — 4 failed, **inside the 13–15 pin** |

**Suite: +28 passes vs HA-31's 1048 baseline — exactly the 28 tests this dispatch adds (10 + 18).
The 31 failures are the baseline 31, unchanged**, every one already filed: 19 disclosure-oracle
(TD-R-178), 4 ledger-commitment (TD-R-180), 1 `test_sensitive_queries_route_local` (TD-R-179),
7 demo-lane `test_demo_presentation` (HA-30's bucket, not this lane's).

**One failure was mine and it was correct.** The first run showed 32 failures; the extra was
`test_battery_manifest`, refusing two new battery files that were not registered in
`scripts/run_harness.sh`. That guard exists so a battery cannot look registered while running
nothing. Both files were added to the runner and the count returned to 31 — **the manifest guard
did its job and is reported rather than quietly satisfied.**

---

## WHY THE BINDING SET IS GREEN, AND WHAT IS RED ANYWAY

**The landing decision rests on Requirements Discipline item 12 as amended 2026-08-07 (Bill's
ruling, HA-20), which is quoted rather than paraphrased because it is the whole basis:**

> "Deterministic tests remain binding and must pass every time (batteries, L7, L7V2, AUDIT, DISC,
> SCHEMA, VOICE, and the ratchet over them). Tests that depend on live model output are reported
> separately and do not make the build pass or fail until a reproducibility rule exists for them."

| binding component | result |
|---|---|
| standing batteries (51 files) | **998 passed / 0 failed / 9 xfailed** |
| L7 / L7V2 | **27/27** and **27/28** (1 opt-in skip, `CT-OUTPUT-GAP`) |
| AUDIT / DISC / SCHEMA / VOICE | **9/9 / 1/1 / 1/1 / 1/1** |
| RATCHET over those | harness's own verdict: **"BINDING TESTS PASS"** |
| memory harness | **13/17**, inside the 13–15 pin |

**THE RED, REPORTED AND NOT HIDDEN — `L2:routing_showcase.T04`.** The RATCHET line reads
`RATCHET FAIL — regressed vs baseline: ['L2:routing_showcase.T04']`, and that line is in this
report rather than summarised away. The scenario asked *"What's the latest news on cable industry
consolidation?"* and the local model replied *"It's 6:36 AM PDT in La on Tuesday, August 11."* —
required token `cable` absent, tier edge escalated.

**L2 is a live-model layer, so it is reported and does not gate** — the amendment names L1, L2,
L3, L4 and L6 explicitly. `live-layer new failures: none`. **It was not re-run.** Item 12 forbids
best-of-N and forbids inventing a pass threshold, and re-running until this went green would have
been exactly the cherry-picking the amendment exists to stop. Its result is appended to
`logs/harness/live_layer_results.csv` (run_id `20260811T135112_01aa901`), which is where the
reproducibility rule will eventually come from — Bill's, from data, not a session's.

**IS IT MINE?** No, and that was tested rather than assumed. A news-routing turn shares no code
path with a write-state guard, and with the product patch stashed the unrelated reds reproduce
unchanged. More directly: **the mutation, write-state and relocation work is all deterministic and
all of it is green**; the only red is a local model answering a news question with the time.

**THE 31 HEALTH-CHECK REDS ARE OUTSIDE THE BINDING SET AND ALL PRE-FILED** — 19 disclosure-oracle
(TD-R-178), 4 ledger-commitment (TD-R-180), 1 `test_sensitive_queries_route_local` (TD-R-179),
7 demo-lane `test_demo_presentation` (HA-30's bucket, another lane's surface). CLAUDE.md: *"A red
in the health check is never on its own grounds to block a landing... Only the BINDING GATE
decides landing."*

**AND ONE OF THOSE 31 TURNS OUT NOT TO BE WHAT IT LOOKED LIKE.** `eval/test_ledger_commitment.py`
is IN the binding battery. Run alone: **17 passed, 0 failed.** Run inside the 51-file battery:
**green.** Run inside the unfiltered suite: **4 failed.** So TD-R-180's four failures are an
ORDERING/POLLUTION effect, not "a rejection path that does not reject" — a different defect,
triaged differently. Recorded as an UPDATE under TD-R-180 (which stays OPEN, number unchanged),
because starting its triage from the whole-suite number alone would send it the wrong way.

---

## FINDINGS FILED

| id | what |
|---|---|
| **TD-R-183** | `scripts/test_groq_factchange.py` posts to `api.groq.com` **in its module body** and has no test function at all. It errored at COLLECTION (`KeyError: 'choices'`), and without `--continue-on-collection-errors` two collection errors **abort the entire suite** — `CLAUDE.md`'s canonical invocation does not carry that flag, so the documented binding gate is one third-party outage from measuring nothing while looking like a decisive red. Also names the second, separable defect: HA-31's comparable 1048/31/2 baseline can only have been produced *with* that flag, which is not recorded anywhere. |

Also recorded: an **UPDATE under TD-R-180** (stays OPEN, number unchanged) noting its four
failures are order-dependent — green alone and green in the binding battery, red only in the
unfiltered suite. An observation, not a resolution, and not investigated further.

Carried forward unfixed by instruction: **TD-R-182**. Filed by HA-34 and **FIXED by this
dispatch: TD-R-181**.

---

## SCOPE HELD

- **No graph cleanup.** HA-34's census proved the graph clean and this dispatch re-measured it:
  12 Fact nodes before and after, all `origin: fixture`.
- **The four untracked demo-lane dispatch docs are untouched**, left exactly as found.
- **Baseline-selection architecture not reopened.** The TD-R-181 fix conditions an existing write
  and adds a separate rejected-run log; it adds no selector to `read_last_survivor_run`.
- **Mutation testing not redesigned.** `_mutant_key`, the operator set, the killer sets, the sweep
  runner and the scoring are all unchanged. One non-identity field was added and one accounting
  path was inserted.

---

## CLAIM IMPACT

**CLAIM IMPACT: none.**

Stated precisely, because landing a product fix and adding 28 tests could easily be read as
progress against the ledger. It is not. `REQ_DERIVED_WRITE_CUSTODY`'s WRITE-STATE VALIDITY clause
now has standing evidence where it previously had a live observation in a dispatch — but **no
claim in `LATEST_HIP_ClaimsLedger.md` covers write-state validity, mutation-survivor bookkeeping,
or baseline custody**, so no claim gained or lost evidence and no status moved. Status is computed
from standing runs by the generator, never declared here.

**`REQ_DERIVED_WRITE_CUSTODY` IS NOT RULED MET.** Its clause is now enforced and proven; the
ruling is Bill's and this dispatch does not pre-empt it.

---

## OPEN

- **TD-R-182** — `find_debt_carry` cannot see `TD-R-` IDs. Filed, not fixed, per instruction.
- **TD-R-183** — live API call at collection time, and the canonical invocation's behaviour when
  any collection error exists.
- **TD-R-177/178/179/180** — the baseline 31 reds, unchanged by this dispatch.
- **`REQ_DERIVED_WRITE_CUSTODY` is NOT ruled MET.** The clause now has standing evidence; the
  ruling is Bill's.

---

**HA-35: ALL SEGMENTS COMPLETE — HA-33 LANDED, BINDING SET GREEN.** Executed in the ordered
sequence Bill set, each gate checked before the next began. **(1) Restoration record written** —
record 141 re-affirmed with provenance, digest `eeb95a7bfa024faa` checkable against 141's content,
revision `a2c27be` recorded; records 142/143 verified **byte-identical afterward**, retained in
full with the reason they are not the active reference. **(2) TD-R-181 FIXED FIRST** —
`accounting_passed` is now a required argument of `write_survivor_trend`, so a caller cannot
persist a baseline without stating the verdict; failing runs go to a separate rejected log that
`read_last_survivor_run` never reads. Proven live: a deliberately failing scratch run left the
accepted baseline **byte-identical** while its evidence landed separately. **(3) TD-R-182 left
filed. (4) CENSUS 33 / 33 / 0** — and the first fingerprint I tried left **5 ambiguous**, which
would have been a STOP; that was a weakness in a fingerprint I chose, not ambiguity in the source,
so it was strengthened rather than the STOP declared. Revision-text reconstruction was validated
against the live walk (**135 sites identical**) before the census was computed from it.
**(5) BUILT** — non-identity fingerprint on `Mutant`/`Survivor`/`_mutant_dict` with `_mutant_key`
**untouched**; RELOCATED path enforcing 1:1 **both ways** and failing closed otherwise; backfill
from the recorded revision, **33/33 survivors, 7 killed entries left ABSENT rather than guessed**;
**0 fingerprint collisions across all 135 sites**; four standing tests as 10 pytest cases, proven
end-to-end on a real module really shifted by ten lines. **(6) HA-33 REAPPLIED — Layer 7 EXIT 0 ON
THE FIRST CONTROLLED RUN**, the five accounted **RELOCATED** `:357/:358 -> :367/:368`, **0
unaccounted, no new survivor** (33 before, 33 after); the two `delete_last_operand(Or)` entries
carry **different fingerprints**, the live proof that same-function/same-operator sites stay
distinct. **Seven absence proofs are now standing tests** (18 cases) with both stated weaknesses —
5/6 sharing one observation, 7 resting on 3's evidence — carried into the test names themselves;
anti-vacuity captures census and full fact_ids before its first write and cleans up by those IDs,
**graph measured 12 nodes before and 12 after**; the reproduction rerun **refuses**, extended to
five more unrecognized states so a guard special-casing one string could not pass. **(7) FOUR
COMMANDS:** binding battery **998/0**, `--layer 7` **exit 0**, RATCHET **"BINDING TESTS PASS"**,
memory **13/17 inside the pin**. **THE ONE RED IS REPORTED, NOT HIDDEN AND NOT RE-RUN:**
`L2:routing_showcase.T04`, a live-model layer that item 12 as amended explicitly does not gate —
the local model answered a news question with the time. **NO GRAPH CLEANUP** (census re-proved it
clean), demo-lane docs untouched, baseline-selection architecture not reopened, mutation testing
not redesigned. **TD-R-183 filed** (live API call at collection time aborts the documented
canonical invocation); **TD-R-180 updated** — its four failures are order-dependent, green alone
and green in the binding battery. **CLAIM IMPACT: none. `REQ_DERIVED_WRITE_CUSTODY` is NOT ruled
MET — that is Bill's call.**
