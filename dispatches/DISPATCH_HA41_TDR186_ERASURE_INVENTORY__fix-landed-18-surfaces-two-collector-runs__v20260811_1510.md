# DISPATCH_HA41_TDR186_ERASURE_INVENTORY — three segments: the fix, the inventory, the collector

Status: **ALL THREE SEGMENTS COMPLETE**
Reconciled-Against: roadmap `5c96b14`
Filed: 2026-08-11 (HA-41)
Decision-Owner: Bill
Authority: Bill's unsupervised-block dispatch, 2026-08-11
Plan of record: `HIP_FinishPlan v20260811` — segment 1 closes step 6's remaining defect;
segment 2 is **step 7 preparation**; segment 3 feeds **step 12**.

| segment | what | status | commit |
|---|---|---|---|
| 1 | HA-40's work: A6 mandatory, TD-R-184 + TD-R-186 fixed, A20b added | **COMPLETE, LANDED** | `1fa2258` |
| 2 | read-only erasure-surface inventory | **COMPLETE** | docs only — this doc |
| 3 | two RATCHET `--full` runs, collector | **COMPLETE** | docs only — this doc |

**Nothing ruled MET. No claim, REQ or ledger status changed. Demo lane untouched.**
Preflight PROCEED (Neo4j 7688 authenticated read; roadmap-local registry).

---

## SEGMENT 1 — AND A PROCESS FAILURE TO REPORT FIRST

**HA-39 NEVER LANDED.** It completed its build and its A1–A20 run and then ended with **no
commit and no push** — a straight violation of STANDARD PREAMBLE item 8, and mine. Its work sat
uncommitted in the working tree until this dispatch carried it. Nothing was lost and nothing was
published by another lane in the meantime, but the exposure was real: the tree diverged from
`origin/roadmap` for hours with no record. **Reported rather than quietly folded in**, because
this is the second time in two dispatches that a completion step was missed (HA-37's ledger row
was the first) and the pattern matters more than either instance.

Segment 1 therefore carries HA-39's work **and** HA-40's, in one commit whose message says so.

### A6 is now mandatory, with no bypass

`OfferInstanceRegistry.create()` enforces minimality on every call. HA-38's opt-in
`require_minimal_for` is **removed and nothing replaced it** — an argument that turns the check
off is a bypass, and a bypass that exists will eventually be passed. The situation **kind is
read off the situation, never accepted from the caller**: a caller-supplied kind would be a
caller-supplied answer to *"which minimal delta applies"*, the choice R7 reserves to the
registry. Checked before rendering, so a non-minimal offer never exists as words.

**Fixtures got a structurally separate path, not a relaxation.** `FixtureOfferRegistry`
(`eval/harnesslib/offer_fixtures.py`) overrides one seam and nothing else. **Ratifying the
fixtures' deltas instead would have enlarged what PRODUCTION accepts in order to make tests
pass** — that is how a check becomes decorative.

**Production cannot reach it, proven:** a standing test parses every `.py` under `harness/` and
`memory_engine/` and fails if any imports `eval`. The bypass is safe only because production
cannot instantiate the subclass, so that is the thing checked — plus guards on `create`'s exact
parameter set, on the kind being read off the situation, on the subclass overriding only
`_assert_minimal`, and an anti-vacuity test that the fixture path really does build an
unratified delta.

### TD-R-184 and TD-R-186, both fixed

**TD-R-184:** the fold is `granted |= (scope_after - scope_before)`. The old
update-then-subtract was right for one event and wrong for a sequence, erasing authority the
member still held.

**TD-R-186 (HA-40's ruling — narrowly, no manifest redesign):** `authority_manifest_for` now
subtracts `authority_change` events in the same append-order fold, so it reports **ACTIVE**
authority — R25's own words are *"the exact ACTIVE delta"* — and agrees with `current_authority`
for the same event history. **Not a redesign:** still derived by replay, still stored nowhere;
one more event kind consulted.

**Both HA-38's and HA-39's pins fired on their own fixes**, which is what a pin is for: each
asserted a divergence and told the next session to re-read both readers when it stopped. Both
are replaced by agreement assertions.

### A20b added to the acceptance table

A20 as written checks that acceptance **updates** the manifest and says nothing about
afterwards — **a manifest that only ever adds satisfies it completely while reporting revoked
authority.** A1–A20 could report a clean closure with the manifest false. A20b binds the
sequence and requires agreement with the reader that decides access.

Bill's standing test, his steps exactly: accept A; accept B; verify both; revoke A; verify A
removed and B untouched; reconstruct from a **fresh ledger object** and get the same answer —
**both readers compared at every step**. Narrowing covered separately. The TD-R-184
multi-acceptance test is kept. `accepted_situations` is asserted unchanged by a revocation:
revoking authority does not un-accept the offer that granted it.

### Segment 1 runs

| check | result |
|---|---|
| binding standing battery (55 files) | **1158 passed / 0 failed / 9 xfailed** |
| `--layer 7` | **EXIT 0** |
| **A1–A20 + A20b** | **17 PASS / 0 FAIL / 4 CANNOT RUN** — all four CANNOT RUNs are the conditional clauses |

## SEGMENT 2 — ERASURE-SURFACE INVENTORY (READ-ONLY; nothing changed, nothing filed)

Finish-plan **step 7 preparation**. For a controlled subject, every place subject data or its
derivatives can live, what erasure does there today, and the file evidence for that verdict.

**THE ACCEPTANCE QUESTION THIS FEEDS IS NOT "was the row deleted?"** The plan of record states
it as: *"After subject erasure, can HIP still recover meaningful subject data through any
supported path?"* — so a surface is only COVERED if erasure reaches it, not if the primary copy
happened to go.

| # | surface | what erasure does today | verdict | evidence |
|---|---|---|---|---|
| 1 | **Graph `Fact` nodes** | `erase_fact` hard-deletes by id; `erase_member_facts` enumerates and deletes a whole owner's facts | **COVERED** | `harness/graph_erasure.py:83`, `:110` (`DETACH DELETE`), `:127` |
| 2 | **Derivatives (lineage closure)** | `walk_lineage_closure` collects every transitively derived fact; the cascade is deleted **in one transaction** | **COVERED** | `graph_erasure.py:59`, `:104`–`:110` |
| 3 | **Per-fact DEK / key material on the node** | No separate DEK store exists — the DEK lives on the node, so `DETACH DELETE` removes it | **COVERED by construction** | `graph_erasure.py:14`–`:24` (module's own docstring) |
| 4 | **Fact metadata (owner, subject, attribute, timestamps, `key_version`)** | Goes with the node in the same delete | **COVERED** *(in the graph only — see 6–9)* | same as 1 |
| 5 | **Off-ledger payload store** | `erase_payload` (v1) and `erase_payload_for_event` (v2) erase the payload behind a ledger event | **COVERED** | `harness/epistemic_ledger.py:686`, `harness/ledger_payload_store.py:134` |
| 6 | **HEL ledger events themselves** | **Not removed — by design.** Erasure appends a `fact.erased` tombstone naming what was erased; the chain is append-only and tamper-evident | **PARTIAL, intentional** | `graph_erasure.py:88`–`:95` |
| 7 | **Raw recall/query text** | **Nothing.** `logs/memory_engine/recall_audit.jsonl` carries a raw `query` field; no erasure path references it | **UNTOUCHED** | `memory_engine/recall.py:36`; probe: first record has text-bearing key `['query']`; **no erasure module references `logs/` at all** |
| 8 | **Encode audit log** | **Nothing.** `logs/memory_engine/encode_audit.jsonl` (11 MB) records every write with fact ids and owners | **UNTOUCHED** | probe: no text-bearing keys, but subject metadata persists; no erasure reference |
| 9 | **Consolidation report / must-confirm queue** | **Nothing.** Both carry per-fact records | **UNTOUCHED** | `logs/memory_engine/consolidation_report.jsonl`, `must_confirm_queue.jsonl` |
| 10 | **Control-plane refusal logs** | **Nothing.** Isolation and response refusals record `situation_id`/principal | **UNTOUCHED** | `harness/control_plane_isolation.py` → `logs/offer_control_plane/isolation_refusals.jsonl`; `harness/offer_response.py` → `response_refusals.jsonl` |
| 11 | **Offer control plane (spend ledger, render records)** | **Nothing.** Render records hold the **verbatim wording shown to a member** (R26, HA-36) | **UNTOUCHED** | `harness/spend_ledger.py`, `harness/offer_render_record.py`; both append-only under `logs/offer_control_plane/` |
| 12 | **Embeddings / indexes** | Nothing to erase — **the engine does not embed**: `"embedding": None` is written and the code says so | **EMPTY, not covered** | `memory_engine/store.py:247`–`:248` |
| 13 | **Summaries** | No prose-summary store found; consolidation emits derived **facts**, which surface 2 covers | **UNKNOWN** | no summary store referenced by any erasure module |
| 14 | **Caches** | No cache-purge path found; `erasure_report.py` mentions "cache" in prose only | **UNKNOWN** | grep: `cache` appears in `erasure_report.py` text, no code path |
| 15 | **Exports** | No export inventory or purge path; `graph_erasure.py` mentions "export" in prose only | **UNKNOWN** | grep: prose only |
| 16 | **Key generations (member/household seal keys, `key_version`)** | Per-fact DEKs go with the node (3). **Seal keys and key versions are not destroyed on subject erasure**; `destroy_test_keys` exists for FIXTURES only | **PARTIAL** | `harness/test_key_hygiene.py:101`; `harness/partition_crypto.py:20`, `:47` |
| 17 | **Backups** | **Nothing.** No backup exclusion, inventory or purge path in any erasure module | **UNTOUCHED** | grep: no `backup` reference in `graph_erasure.py` / `erasure_request.py`; `erasure_report.py` prose only |
| 18 | **Erasure verification itself** | `verify_erasure_report` checks a claimed erasure against LIVE state — but only for `ledger_payload` and graph targets | **PARTIAL** | `harness/erasure_report.py:357` |

### Counts

| verdict | count | surfaces |
|---|---|---|
| **COVERED** | **4** | graph nodes, derivatives, per-fact DEK, payload store |
| **PARTIAL** | **3** | HEL ledger events (intentional), key generations, erasure verification |
| **UNTOUCHED** | **6** | recall/query text, encode audit, consolidation/must-confirm, refusal logs, offer control plane, backups |
| **UNKNOWN** | **3** | summaries, caches, exports |
| **EMPTY** | **1** | embeddings (nothing embeds today) |
| **total** | **17 + 1** | *(18 rows; "erasure verification" is a meta-surface and is counted in PARTIAL)* |

### What this inventory says, stated plainly

**Erasure today is a GRAPH erasure plus a ledger-payload erasure. It is thorough within those
two surfaces and does not reach outside them.** Every COVERED row is inside the graph or the
payload store; **no erasure module references `logs/` at all**, and six surfaces that
demonstrably hold subject data or subject metadata are therefore untouched.

**The two that would matter most to the plan's acceptance question:**

* **Raw query text** (surface 7) — `recall_audit.jsonl` holds the member's natural-language
  queries. Already filed as **TD-R-173**; this inventory confirms erasure does not reach it.
* **Verbatim offer wording** (surface 11) — R26's render records deliberately store the exact
  words shown to a member, durably and hash-verified. **Nothing erases them.** That is a direct
  consequence of the A19 fix and was not considered when it landed.

**Three UNKNOWNs are genuinely unknown, not assumed absent.** Summaries, caches and exports
have no erasure path and no inventory; whether they hold subject data at all was not
determined, because determining it means enumerating those subsystems and that is step 7's own
work, not this preparation's.

**No fixes, no filings beyond this table**, per instruction. TD-R-173 is cited because it
already exists, not filed anew.

---

## SEGMENT 3 — COLLECTOR DATA

Two `--full` runs back to back under `caffeinate`, on the landed tree `1fa2258`, with progress
markers per run.

| run | run_id | exit | rows | verdict |
|---|---|---|---|---|
| 1 | `20260811T201236_1fa2258` | 0 | 1409 → 1497 | **BINDING TESTS PASS**; regressions `['L2:routing_showcase.T04']`; new failures `['L6:record-invariants']` |
| 2 | `20260811T210409_1fa2258` | 0 | 1497 → 1585 | **BINDING TESTS PASS**; regressions `['L2:routing_showcase.T04', 'L4:PW027']`; new failures `['L6:record-invariants']` |

Memory harness: **13/17** (4 failed) — inside the 13–15 pin.

### Per-run detail, and what differed

```
run 1: 88 scenarios | PASS 71 FAIL 3 SKIP 14   FAIL L1:P2, L2:T04, L6:record-invariants
run 2: 88 scenarios | PASS 70 FAIL 4 SKIP 14   FAIL L1:P2, L2:T04, L4:PW027, L6:record-invariants

differing on byte-identical code, back to back:
   L4:PW027   run1=PASS  run2=FAIL
   1 of 88 scenarios differ
```

**This time the counts differed too** (3 vs 4 failures), unlike HA-38's pair where identical
counts hid different failures. Both shapes are now in the record, which is the point of
collecting rather than reasoning.

### Cross-run history — 18 runs, 1584 rows

| scenario | across all 18 recorded runs |
|---|---|
| `L2:routing_showcase.T04` | **FAIL 18 / PASS 0** |
| `L6:record-invariants` | FAIL 12 / PASS 6 |
| `L1:P2` | FAIL 12 / PASS 6 |
| `L4:PW027` | PASS 16 / **FAIL 2** |

**T04 has still never passed, in eighteen runs.** L6 and L1:P2 remain bimodal at roughly 2:1.
`L4:PW027` is a third shape again — mostly green, occasionally red — which is what a genuinely
flaky live scenario looks like next to one that is simply broken.

**No threshold set, no reproducibility rule proposed, no gate claim, and nothing re-run.**
TD-R-185 stays filed and untouched, per instruction.

---

## FINDING FILED — TD-R-187

**The collector labels a run with the commit at WRITE time, not RUN time.** A `--full` takes
15–20 minutes and Python imports at process start, so anything committed mid-run mislabels the
rows.

Observed exactly today: run `20260811T195452_1fa2258` recorded 88 rows under commit `1fa2258`
(authored 13:54:49). That process started ~13:40, the TD-R-186 edit landed ~13:47, and the
commit was made ~13:52. **It measured the pre-fix code and is labelled with the commit that
fixed it.**

**It matters because this CSV is the instrument the live-model reproducibility rule is to be set
FROM** (plan step 12). "Same commit, different outcome" is exactly the question a mislabelled
row corrupts, and the mislabelling is silent. Cheap fixes exist; not applied, because
instrumenting the collector was not a segment of this dispatch.

---

## CLAIM IMPACT

**none.**

C-06 and C-14 gained standing evidence at HA-38/HA-39 and gain a little more here — A20b makes
R25's manifest checkable as ACTIVE authority, which is part of what "the authority described by
the offer" means for C-14. **No claim status moved and none may**: status is computed from
standing runs by the generator, never declared by a session, and Bill's ruling on
`REQ_OFFER_MECHANISM` is his to make from HA-39's table plus this dispatch's A20b.

**`REQ_OFFER_MECHANISM` remains NOT MET in every document.**

---

## WHAT NEEDS BILL

1. **The REQ ruling.** A1–A20 + A20b is 17 PASS / 0 FAIL / 4 CANNOT RUN, all four conditional.
   Nothing here rules it.
2. **Step 7 scope, from the inventory.** Six surfaces are untouched by erasure and three are
   unknown. The two that most affect the plan's own acceptance question are raw query text
   (TD-R-173) and **R26's verbatim render records** — the words shown to a member, made durable
   by HA-36 and erased by nothing.
3. **TD-R-187** — collector labels; worth deciding before a reproducibility rule is set from
   that data.

---

## OPEN

- **TD-R-187** (new), **TD-R-185**, **TD-R-183**, **TD-R-182**, **TD-R-173** — filed, unfixed.
- **TD-R-184 and TD-R-186 — both CLOSED by this dispatch.**
- The 31 health-check reds — unchanged; Phase 4 in the plan of record.

---

**HA-41: ALL THREE SEGMENTS COMPLETE.** **SEG 1** (`1fa2258`) landed HA-39's never-committed
work alongside HA-40's — **reported as the item-8 failure it was**. A6 minimality is now
MANDATORY with no bypass parameter and the situation kind read off the situation; fixtures use a
structurally separate registry that **production provably cannot reach** (every `harness/` and
`memory_engine/` module parsed for an `eval` import). **TD-R-184 and TD-R-186 both fixed** —
the manifest now reports ACTIVE authority and agrees with the access reader — and **A20b** was
added to the REQ so A1–A20 can never report a clean closure while the manifest is false again.
Binding battery **1158/0**, `--layer 7` **exit 0**, **A1–A20 + A20b: 17 PASS / 0 FAIL / 4 CANNOT
RUN**, all four conditional. **SEG 2** enumerated **18 erasure surfaces: 4 COVERED, 3 PARTIAL, 6
UNTOUCHED, 3 UNKNOWN, 1 EMPTY** — erasure today is a graph erasure plus a ledger-payload
erasure and **no erasure module references `logs/` at all**; the sharpest finding is that
**R26's verbatim render records, made durable by HA-36, are erased by nothing.** **SEG 3** ran
two `--full` runs on the landed tree, both **BINDING TESTS PASS**, memory **13/17 inside the
pin**, collector 1409 → 1585 across 18 runs; **`L2:T04` has now failed 18 of 18** while L6 and
L1:P2 stay bimodal and `L4:PW027` showed a third shape (16 PASS / 2 FAIL). **No threshold, no
rule, no gate claim, nothing re-run.** **TD-R-187 filed:** the collector labels runs with the
commit at write time, so a run that spans a commit is silently mislabelled — which matters
because that CSV is what step 12's rule is to be set from. **CLAIM IMPACT: none. Nothing ruled
MET.**
