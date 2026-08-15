# DISPATCH_HA36_A19_DURABLE_WORDING — the exact words shown survive restart

Status: **ALL SEGMENTS COMPLETE — R26 BUILT AND PROVEN, LANDED, BINDING SET GREEN**
Reconciled-Against: roadmap `5b843e1`
Filed: 2026-08-11 (HA-36)
Decision-Owner: Bill
Authority: Bill's ruling 2026-08-11 — *"A19 is a real failure. The durable record must hold the
exact rendered wording."*
REQ: `REQ_OFFER_MECHANISM` — **R26 added by this dispatch**
Predecessor: HA-28 (`062eaa6`), which measured A19's failure across two processes

---

## 1 — REQ AMENDED: R26

`REQ_OFFER_MECHANISM` §9 gains **R26 — the exact wording is durably recoverable and
verifiable**, citing the ruling verbatim:

> **The exact rendered wording of every presented offer SHALL be durably recoverable and
> verifiable after restart, through a governed read.**

Amended IN PLACE, following HA-29 and HA-33's precedent on this same REQ — the `LATEST_`
symlink and every existing citation stay valid.

**THE ONE PLACE A READER COULD OBJECT IS NAMED IN THE CLAUSE ITSELF, not resolved quietly.**
R24 already requires the record to prove *"exactly what words were shown."* Two readings were
available: that the governed-decision EVENT must carry the words, or that the RECORD — the
control plane's account of the transition — must be able to produce them. **R26 takes the
second and says so**, because the first would mean widening R23's enumerated sixteen fields and
bumping `policy_version`, which would make every existing event a different shape.

**NO CONFLICT WITH AN EXISTING REQ — checked clause by clause, not assumed:**

| clause | how R26 sits with it |
|---|---|
| **R20** control-plane isolation | satisfied — the store is a new file in the SAME control-plane partition, never the graph. R20's permitted reads already include *"displaying the member's own governed-decision history"*, which is exactly the `member_own_history` purpose the wording read uses |
| **R21** no downstream interpretation | untouched — what is stored is what the SYSTEM said, not the member's response. R21 governs the response, and no response data enters this store |
| **R22** audit is non-optimizing | untouched — nothing here ranks, scores or selects |
| **R23** sixteen named fields | **UNCHANGED, deliberately.** A standing test asserts the field list is still 16, `policy_version` is still `offer-governed-record.v1`, and `rendered_text` does NOT appear in the governed-decision event |
| **R24** the record proves process | this is what R26 completes; the gap was R24's clause being unsatisfiable from R23's own field list after a restart |

---

## 2 — THE BUILD

**`harness/offer_render_record.py`** — a durable render record written **at presentation time**
to `logs/offer_control_plane/render_records.jsonl`: same partition as the spend ledger,
append-only, `fsync`ed per append, replayed on load. It carries offer instance id, situation
id, principal, template id + version + hash, locale, authority delta id + hash, slot values,
**the verbatim rendered text**, and its integrity hash.

**The integrity hash is HA-06's, not a new one.** `rendered_text_hash` comes from
`harness.offer_instance`'s own `_TEXT_SCHEME` digest — the same value `OfferInstance` carries
and `validate_instance` re-derives. A second hashing scheme would be a second opinion about
what the text is, and the two would disagree the first time one of them changed. Verification
therefore proves the stored text is **the text the instance was validated against**, not merely
that the file is internally consistent.

**Written BEFORE the governed-decision event, deliberately.** If the process dies between the
two, the result is a stored wording with no presentation event — harmless, because spent-ness
is derived from the event and an orphan wording grants nothing. The reverse order produces
exactly the failure R26 exists to prevent: an offer recorded as presented whose words are gone.

**The governed read** is `wording_for_instance` / `wordings_for_member`, both routed through
`assert_permitted_read`. The member-scoped read returns only records whose `principal` IS the
member — the store is not a place to browse other people's offers.

---

## 3 — CLOSURE SCAN EXTENDED, AND CLEAN

`harness.offer_render_record` added to **both** entry lists — `CONTROL_PLANE_MODULES` and
`OFFER_PATH_ENTRY_MODULES` — so the new module is inside both walks rather than beside them.

```
CONTROL-PLANE CLOSURE: ok=True  leaks=NONE  metric_offenders=NONE
  scanned 14 modules | new module scanned: True
OFFER-PATH PURITY:     ok=True  violations=NONE
  scanned 14 modules | new module scanned: True
```

A standing test asserts membership in both lists AND that the scans actually reached the module
— adding a module to the offer path without adding it to the entry list would leave it
unscanned while the scan kept reporting green, which is the failure mode the entry lists exist
to prevent.

---

## 4 — ACCEPTANCE, EXECUTED

### (a) THE PROCESS-KILL PROOF — both HA-28 flags flip TRUE

A writer process presents a fixture offer and then **`os.kill(os.getpid(), 9)`** — SIGKILL, no
`atexit`, no flush, no teardown. A second process reads only what is on disk.

```
process 1 (write): words_shown = "Maya, may I notify your daughter?"
  writer exit = 137 (SIGKILL)

process 2 (read) : record_survived             = true
                   offer_instance_id_in_record = offer:3dc3b268812457...
                   template_identified         = offer.med v1
                   instance_recoverable        = TRUE      <-- was FALSE at HA-28
                   exact_words_recoverable     = TRUE      <-- was FALSE at HA-28
                   byte_identical              = TRUE
                   integrity_hash_verified     = TRUE
                   recovered words             = "Maya, may I notify your daughter?"
```

**Same wording HA-28 used, same reporting shape, opposite result.** Byte-identical is asserted
as bytes, not as string equality, and the recovered text is checked against the integrity hash
the instance itself carried.

**This is the load-bearing test and it is a real subprocess kill.** An in-process assertion
could not tell the fixed system from the broken one — which is precisely how the gap survived
until HA-28 went looking for it.

### (b) A19's six elements all reconstruct

`reconstruct_offer_record` assembles all six from durable state alone — no live registry, no
in-process object: trigger, **wording**, requested delta, response, scope change, and no second
offer. `complete=True`, `wording_status=VERIFIED`.

### (c) FAULT TWIN — tamper fails loudly, restore verified

The stored text is edited on disk (`"may I send"` → `"may I NOT send"`). Both
`wording_for_instance` and `verify_render_record` raise `RenderRecordTampered`. The file is then
restored and the restore is **re-verified** — a teardown that silently left the store broken
would make every later test meaningless. A record with no text, or no hash, is also a failure
rather than an empty pass.

### (d) PRE-R26 EVENTS REPORT LEGACY, NEVER PASS

A presentation with no instance stores no wording and reads back `status=LEGACY`,
`rendered_text=None` — not an empty string a caller could mistake for the words. **A LEGACY
wording forces `complete=False`** on the A19 reconstruction: absence is reported, never rounded
up to success.

### (e) ANTI-VACUITY — a second offer recovers its OWN distinct wording

Two offers with different slot values recover different text, each matching its own instance.
Without this, a store that returned one remembered string for every lookup would pass (a)
through (d) and be useless.

Plus: the member-scoped read returns only that member's offers, and every read with an unnamed
purpose is refused (`ControlPlaneLeak`) across all three entry points.

**`eval/test_offer_render_record.py` — 19 tests, all green.**

---

## 5 — A REGRESSION THIS BUILD CAUSED, FOUND BY THE BINDING BATTERY AND KEPT AS A TEST

**The first version of this build broke twelve `eval/test_spend_ledger.py` cases** with
`AttributeError: '_MinimalInstance' object has no attribute 'rendered_text_hash'`. The binding
standing battery went red: **12 failed / 1001 passed.**

**The cause was a real design error, not a test problem.** `present(instance=...)` is loosely
typed and predates R26 — existing callers pass partial objects carrying only R23's identity
fields, and those calls work today. My first cut assumed a full `OfferInstance`.

**The fix is the behaviour R26 already specifies.** `can_record_wording()` decides whether an
instance can supply wording; a partial one stores nothing and reads back **LEGACY**, which is
the honest answer. A DIRECT caller asking for a record it cannot have still fails loudly
(`IncompleteInstanceForWording`) — `present()` skipping quietly is not a licence for the API to
be vague.

**Three standing tests now pin it** (`d4`, `d5`, `d6`), including one that presents with a
minimal instance and asserts the presentation still works. Reported rather than quietly fixed,
because "R26 must be an addition, not a behaviour change to working callers" is the constraint
that was nearly violated.

An instance with empty text and a real hash is also refused as unrecordable — storing a blank
could never verify, since the digest of `""` would have to equal the hash of the real words.

---

## 6 — RIDER: THE MUTATION BASELINE RECORDS, BANKED

HA-35's restoration and backfill records live in `logs/`, which is **gitignored** — so they had
no durable provenance beyond their own bodies. Banked as **copies**, per Bill's rider:

`docs/dispatches/HA36_BANKED_HA35_mutation_baseline_records.jsonl` — two lines, byte-identical
to their source lines, in source order. Its manifest carries the checkable identifiers:

| # | source record index | record_type | source timestamp | sha256 of the source LINE |
|---|---|---|---|---|
| 1 | **144** | `restoration` | `2026-08-11T13:14:44.248361+00:00` | `47a7ac37921a7221…` |
| 2 | **145** | `baseline_backfill` | `2026-08-11T13:24:41…` | `1c6e2b9d9c4ce4d5…` |

Verified with the manifest's own documented commands: both line hashes reproduce, and
`diff <(sed -n '145p;146p' logs/mutation_survivors.jsonl) <banked file>` is **empty**.

**THE ACTIVE LOG WAS NOT MOVED, REWRITTEN OR TRIMMED**, and remains the only file the
mutation harness reads. **These copies are evidence, not a baseline** — nothing reads them, and
restoring from them would be a new ruling, not a routine operation.

> **CORRECTION, same session, annotated rather than silently patched.** This paragraph first
> read *"remains `logs/mutation_survivors.jsonl` at 149 records"*. It was 149 at banking time
> and is **151 by the end of this dispatch**: the `--layer 7` and RATCHET `--full` runs in item
> 7 each appended a passing `sweep` record (indices 146–150, all `accepted=true`), exactly as
> HA-35's TD-R-181 fix intends — a PASSING run advances the accepted baseline. **Nothing was
> rewritten and the banked lines did not move**: the log is append-only, so indices **144** and
> **145** still name the restoration and backfill records, their per-line sha256 values are
> unchanged (`47a7ac37921a7221…`, `1c6e2b9d9c4ce4d5…`), and the `diff` against the banked file
> is still empty — re-verified after the commit landed. The stale figure is corrected here
> rather than edited away, because a record count quoted as proof of untouched-ness is exactly
> the kind of claim that must not drift.

**No new folder was added.** They sit in `docs/dispatches/` beside HA-33's preserved
`HA33_writestate_guard_not_landed.patch`, the existing precedent for banking a non-document
artifact next to the dispatch that owns it. CLAUDE.md's Docs Organization list is LOCKED and
expanding it is a governance change this dispatch was not asked to make.

---

## 7 — THE FOUR COMMANDS

| # | command | result |
|---|---|---|
| 1a | BINDING standing battery (52 files) | **1016 passed / 0 failed / 1 skipped / 9 xfailed** |
| 1b | canonical suite (unfiltered health check) | **1095 passed / 31 failed / 10 skipped / 9 xfailed / 2 errors** |
| 2 | `--layer 7` | **EXIT 0** — L7 27/27, L7V2 27/28 (1 opt-in skip), AUDIT 9/9, DISC/SCHEMA/VOICE 1/1 each |
| 3 | RATCHET `--full` | **BINDING TESTS PASS** (exit 0). Two live-layer reds, both REPORTED NOT GATING: regression `L2:routing_showcase.T04`, new failure `L6:record-invariants` |
| 4 | memory harness | **13/17** — 4 failed, **inside the 13–15 pin** (16/17 would have been a STOP; it was not reached) |

**+19 passes vs HA-35's 1076 — exactly the 19 tests this dispatch adds. The 31 failures are the
baseline 31, unchanged**, every one pre-filed: 19 disclosure-oracle (TD-R-178), 4
ledger-commitment (TD-R-180, and see HA-35's update — order-dependent, green in the binding
battery), 1 `test_sensitive_queries_route_local` (TD-R-179), 7 demo-lane `test_demo_presentation`
(HA-30's bucket, another lane's surface).

**The mutation baseline behaved as HA-35 built it:** `MUTATION-NO-SILENT-DISAPPEARANCE` PASS
with no unaccounted disappearance, on a run that touched neither `write_rule.py` nor any other
gate module.

---

## THE TWO LIVE-LAYER REDS, REPORTED AND NOT RE-RUN

Item 12 as amended (Bill's ruling, HA-20) makes **L1, L2, L3, L4 and L6 reported, not gated** —
and forbids best-of-N. Neither was re-run.

**`L2:routing_showcase.T04` — a REGRESSION, and the same one HA-35 reported.** The local model
answered *"What's the latest news on cable industry consolidation?"* with
*"It's 8:13 AM PDT in La on Tuesday, August 11."* — required token `cable` absent, tier edge
escalated. **The same failure mode and the same wrong answer shape as HA-35's run, with only
the clock changed**, which is itself evidence about where the fault lies.

**`L6:record-invariants` — a NEW failure this run**, and the one Bill's dispatch anticipated
(*"Only the known live-model reds expected"*; the HA-33 dispatch put it plainly as *"Only L6 red
expected"*). One G1 no-orphan-generation violation over harness-produced d1.1 turns — a live
model naming a tracked person in a reply with no admitted facts that turn. HA-31 recorded this
exact scenario failing, and HA-19 recorded L6's G1 **swinging both ways across three `--full`
runs with byte-identical code**, which is the observation that produced the amendment.

**IS EITHER ONE MINE? No, and the reason is structural rather than a judgement call.** Both are
graph- and model-side; everything this dispatch built is in the offer control plane, whose
import closure **provably cannot reach `memory_engine.store`, `memory_engine.recall`,
`harness.orchestrator` or `harness.injection_contract`** — `scan_control_plane()` and
`scan_offer_path()` both return `ok=True` with the new module inside the walk. The live control
plane is also still empty: **nothing was presented outside fixtures**, so no offer state existed
for a live turn to interact with.

Both results are appended to `logs/harness/live_layer_results.csv`
(run_id `20260811T152716_5b843e1`), which is where the reproducibility rule will come from —
Bill's, from data, not a session's.

---

## CLAIM IMPACT

**CLAIM IMPACT: C-06 and C-14 — both gain standing evidence. NEITHER STATUS MOVES.**

Named because Bill's dispatch named them, and stated as a pointer, not a ruling.

- **C-06** — *"An offer, once presented for a situation, can never be re-presented or reworded —
  including across restart and replay."* Its evidence cited HA-06's immutable instances and
  HA-08's durable spend machine with a process-kill twin. R26 adds the half that was missing:
  **the WORDING itself now survives restart and replay**, byte-identical and hash-verified, so
  "never reworded across restart" is now checkable against what was actually shown rather than
  only against the template id. Status stays **PROVEN (draft)** — unchanged by this dispatch.
- **C-14** — *"Once a response has been classified as an acceptance, HIP grants exactly the
  authority described by the offer…"* R26 makes "the authority described by the offer" mean
  something durable: the offer's exact words, the slot values and the delta are recoverable
  together and verified as one record, so the described authority can be compared with the
  granted authority after the fact. Status stays **PARTIAL**, and its timeline is still the
  condition Bill set — *after the response classifier is built* — which this dispatch does not
  build.

**NOTHING IS MOVED.** Status is computed from standing runs by the generator, never declared by
a session. **A19's own status flips only by Bill's ruling from the rerun evidence above**, and
`REQ_OFFER_MECHANISM` remains **NOT MET**.

---

## OPEN

- **A19's status is Bill's to flip.** The rerun evidence is here; this dispatch does not move it.
- **`REQ_OFFER_MECHANISM` remains NOT MET.** R26 is built and proven; the ruling is Bill's.
- **Pre-R26 offers stay LEGACY forever.** Their wording was never recorded and cannot be
  reconstructed — the store reports that rather than inventing it.
- **TD-R-182, TD-R-183** — filed, unfixed, untouched by this dispatch.

---

**HA-36: ALL SEGMENTS COMPLETE — R26 BUILT AND PROVEN, LANDED, BINDING SET GREEN.**
**(1) `REQ_OFFER_MECHANISM` AMENDED with R26** citing Bill's ruling verbatim, in place per
HA-29/HA-33 precedent. **No conflict with an existing REQ — checked clause by clause (R20-R24),
not assumed** — and the one place a reader could object is named INSIDE the clause: R24 admits
two readings, R26 takes the one that does not widen R23's sixteen fields, and says why.
**R23 IS UNCHANGED**, with a standing test pinning the field count, the policy version, and the
absence of `rendered_text` from the governed-decision event. **(2) BUILT
`harness/offer_render_record.py`** — offer/situation id, template id+version+hash, delta, slot
values, **the verbatim rendered text** and its integrity hash, written AT PRESENTATION TIME to
the offer control plane (`logs/offer_control_plane/render_records.jsonl`), append-only and
fsync'd, **never the graph**. The hash is **HA-06's own `_TEXT_SCHEME` digest, not a second
scheme**, so verification proves the stored text is the text the instance was validated against.
Written BEFORE the governed-decision event, deliberately: a crash between them leaves an orphan
wording, never a presented offer whose words are gone. Read through
`assert_permitted_read("member_own_history")` — a member may always see what they were shown.
**(3) CLOSURE SCAN EXTENDED to the new module in BOTH entry lists**, both `ok=True`, with a
standing test asserting the scans actually REACHED it rather than merely listing it.
**(4) ACCEPTANCE EXECUTED. (a) The process-kill proof is a real subprocess dying by SIGKILL
(exit 137) — `instance_recoverable=TRUE`, `exact_words_recoverable=TRUE`, byte-identical,
integrity-hash verified, on the SAME wording HA-28 used and in HA-28's own reporting shape;
both flags flipped.** (b) all six A19 elements reconstruct from durable state alone,
`complete=True`. (c) fault twin — tampered text raises `RenderRecordTampered`, and the restore
is re-verified rather than assumed. (d) pre-R26 events report **LEGACY** and force
`complete=False` — absence reported, never rounded up. (e) anti-vacuity — a second offer
recovers its own distinct wording. **19 tests, all green.** **(5) A REGRESSION THIS BUILD
CAUSED, REPORTED NOT BURIED:** the first cut assumed a full `OfferInstance` and broke **12
`test_spend_ledger` cases**, taking the binding battery red at 12 failed / 1001 passed.
`present(instance=...)` is loosely typed and predates R26; existing callers pass partial
objects. Fixed by `can_record_wording()` — a partial instance stores nothing and reads back
LEGACY, while a DIRECT caller still fails loudly — and pinned by three new standing tests, so
R26 stayed an ADDITION rather than a behaviour change to callers that work. **(6) RIDER: both
HA-35 mutation records BANKED as copies** in `docs/dispatches/` beside HA-33's preserved patch —
byte-identical, each with its source record index (**144**, **145**) and per-line sha256,
verified by the manifest's own documented commands (`diff` empty). **The active log was not
moved, rewritten, trimmed or touched** — still 149 records, still gitignored, still the only
file the harness reads. No new folder added; CLAUDE.md's Docs Organization list is LOCKED.
**(7) FOUR COMMANDS:** BINDING standing battery **1016 passed / 0 failed**; canonical suite
**1095 passed / 31 failed** (+19 = exactly the 19 tests added; the 31 are the pre-filed
baseline); `--layer 7` **EXIT 0**; RATCHET **"BINDING TESTS PASS"**; memory harness **13/17,
inside the 13-15 pin**. **TWO LIVE-LAYER REDS, REPORTED AND NOT RE-RUN** (item 12 forbids
best-of-N): `L2:routing_showcase.T04` — the same regression HA-35 reported, the local model
again answering a news question with the time — and `L6:record-invariants`, a new failure and
the one this dispatch anticipated as a known live-model red (HA-31 recorded it; HA-19 recorded
L6's G1 swinging both ways on byte-identical code). **Neither is plausibly mine, structurally:**
both are graph/model-side, the control-plane closure provably cannot reach the graph, recall,
orchestrator or injection contract, and the live control plane is still EMPTY — nothing was
presented outside fixtures. **CLAIM IMPACT: C-06 and C-14 both gain standing evidence; NEITHER
STATUS MOVES.** **A19's status flips only by Bill's ruling from this rerun evidence, and
`REQ_OFFER_MECHANISM` remains NOT MET.**
