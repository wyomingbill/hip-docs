STOPPED AT SEGMENT 1 — NEEDS BILL

# DISPATCH_HA45_STOP_PLAINTEXT_AT_SOURCE — row 7 built, row 19 stopped on item 5
Status: BUILT (row 7) / STOPPED (row 19)
Reconciled-Against: roadmap `dc7db43` (HA-44) at start; landed this dispatch

**Dispatch ID: HA-45.** Authority: `REQ_ERASURE_SURFACES` Q3-C, blocking per Q6.

**Row 7 (`recall_audit.jsonl`) is BUILT and green. Row 19 (`logs/transcript/`) is STOPPED under
the dispatch's own item 5** — two consumers genuinely require the raw text downstream of the
write, and item 5 says name them rather than weaken the design to feed them.

**The existing corpus on both surfaces is untouched, as instructed.** Its map is §4, for build 2.

---

## 1. THE STOP — row 19, and why it is item 5 rather than a defect

Item 5, verbatim: *"If any consumer genuinely requires the raw text downstream of the write …
STOP and name it — do not weaken the design to feed it."*

**Two consumers read the transcript's `text` field back out of the durable log:**

| consumer | what it does with the words | verdict |
|---|---|---|
| **`server/demo_dashboard.py:906`, `/api/transcript`** | Returns whole records **including `text`**, merged across per-member session files, to the dashboard's top band — **which renders the conversation to the room.** | **GENUINELY needs the words.** Commitment-only blanks the demo's transcript band. |
| **`eval/passthrough_consent_vignette.py:202`** | `t2_query[:40] in (r.get("text") or "")` — correlates *which* turn is turn 2 by matching the query's first 40 characters. | **Needs the words as written**, though the need is correlation and could in principle be met by a turn id. |

**Three other readers of `logs/transcript/` do NOT need the words** and would survive the change
untouched — recorded so the STOP is scoped to what actually blocks:
`eval/test_demo_smoke.py` (reads `member_id`, `speaker`, `ts`, mtimes),
`scripts/build_evidence_package.py` (per-turn metadata), and the dashboard's own source-list
endpoint (`:1150`, filenames only).

**Not conflated:** `eval/harnesslib/layer2.py`, `scripts/run_demo_script.py` and
`scripts/demo_run.py` also read `turn["text"]`, but from **demo SCRIPT files** — the turns being
sent in, not the transcript being written out. They are not consumers of this surface.

### Why this was not worked around

Q3-C permits *"keyed commitments **or sealed content**"*, and **sealed content would feed the
dashboard** via a decrypt path — so a workaround exists on paper. It was not taken, for three
reasons, and the choice is Bill's rather than mine:

1. **It is a much larger build than "stop writing plaintext."** Sealing needs a key choice
   (per-member? per-session?), a seal/unseal path, and a dashboard decrypt path.
2. **It front-runs Q2.** Key custody is exactly step 4 of the ratified build order and
   **condition 1 of the standing erasure-enablement gate.** Minting a new sealed store with new
   keys before that work would be a second key convention to consolidate later.
3. **Commitment-only would break a working, load-bearing path** — the demo's transcript band —
   and the REQ's own CONSTRAINTS make working paths sacred. **The demo is the first finish line
   in the plan of record.**

### What Bill needs to decide

| option | consequence |
|---|---|
| **A — Seal transcript content** (Q3-C's second half) | Dashboard keeps working via decrypt; erasure becomes key destruction, consistent with Q4-B. **Costs a key decision that belongs to Q2/step 4** — likely should be sequenced *after* it, not before. |
| **B — Commitment-only, and change the dashboard** to render from the live session rather than the durable log | Cleanest separation: live display ≠ durable retention. **Costs a dashboard change in the demo path**, and the vignette needs a turn id to correlate on. |
| **C — Commitment-only, accept the dashboard band goes blank** | Cheapest; **breaks the demo's transcript band.** Named for completeness, not recommended. |
| **D — Defer row 19 until after step 4** (key custody) | Honest sequencing: row 19 is blocking per Q6, so **this defers the phase**, and today's plaintext keeps accumulating meanwhile. |

**Nothing is proposed and nothing was chosen.** Note that Q6 already ruled row 19 blocking, so
whichever option is taken, **the phase does not complete until it lands.**

---

## 2. ROW 7 — BUILT

### What changed

`memory_engine/recall.py::_append_recall_audit` **no longer writes the query's words.** It writes
a keyed commitment computed at the boundary:

```
"query": query            →   "query_commitment": "hmac-sha256:<64 hex>"
```

`query` remains a *parameter* — the caller has it, and converting inside the writer means no call
site has to remember to. Three call sites feed it; none changed.

**The commitment is keyed to the SUBJECT**, and that is the erasure property this row exists for:
Q2 destroys the erased subject's key material, so **after that member is erased their commitments
can no longer be verified by anyone.** The record degrades to an opaque token rather than
remaining a testable hash. A shared or system key would leave every commitment verifiable
forever and turn this surface into a dictionary-testing oracle — precisely what R16 exists to
prevent.

**Mechanism reused, not invented:** `compute_keyed_commitment` over `_load_or_create_member_key`
— the proven HEL 2.0 path, unchanged.

### Fail-closed, in two independent layers

1. **`_commit_query` never raises and never falls back to the words.** On a weak key, an OSError
   or an import failure it logs and records `None`. A recall must not break, and must not leak.
2. **A forbidden-key strip runs on every record.** Any of
   `query, query_text, text, utterance, raw_query, prompt` present in the dict is deleted before
   the write, with an error logged. **The log losing a field is recoverable; the log gaining
   plaintext is not.**

### The governed read path

`verify_recall_audit_query(entry, query, subject=None)` — a later-supplied copy of a query can
still be checked against what was recorded, which is the point of committing rather than
deleting.

**It reads the key WITHOUT creating it**, and that detail is load-bearing:
`_load_or_create_member_key` would **mint a replacement key** for an erased member, silently
resurrecting key material Q2 had destroyed and handing back a fresh key that verifies nothing.
Verification must observe the post-erasure state, not repair it. It also keeps this path out of
TD-R-172's key-population growth. **Asserted by a test**, not left to review.

### Nothing downstream broke, and that was checked before building

All three readers of `recall_audit.jsonl` — `eval/memory_harness.py` (two sites) and
`eval/memory_e2e.py` — use only `reason`, `allowed_fact_ids`, `cold_fact_ids_fetched`,
`denied_count`, `subject`, `requester`. **None reads `query`.** That is why row 7 was buildable
while row 19 was not.

---

## 3. FAULT TWINS — proven red, then restored

New standing battery: **`eval/test_recall_audit_no_plaintext.py`, 10 tests, registered in
`scripts/run_harness.sh`** (the manifest check would otherwise fail it as a silent skip).

**Every twin has an anti-vacuity half**, because "no plaintext" is the easiest assertion to pass
for the wrong reason — an empty record satisfies it.

| twin | anti-vacuity half |
|---|---|
| The query text, and every distinctive token in it, is absent from the file | The four operational fields the real readers use are present and correct |
| No forbidden text-bearing key is in the record | The commitment IS present, is `hmac-sha256:` + 64 hex, and **is not a bare SHA-256 of the words** (which would be dictionary-testable) |
| A wrong copy does not verify | The **right** copy does verify, through the governed path |
| Verification returns False when the key is gone | …and **mints no key material** doing it — the keys dir is asserted empty before and after |
| A commitment that cannot be computed records `None` | …and the record still lands, still carrying no words |

### Proven red

The fix was reverted in place (`"query": query` restored), the battery re-run, and the file
restored from a pre-edit copy:

```
4 failed, 6 passed          ← defect reintroduced
10 passed                   ← restored
```

**A result worth reporting rather than glossing: the two "no plaintext" twins still PASSED with
the defect reintroduced** — because the forbidden-key strip caught `query` and dropped it before
the write. The four that went red were the commitment twins and the source check. **That is the
second barrier doing real work**, and it means the plaintext did not leak even with the primary
fix removed. It is also why the source-level twin exists: without it, the strip would mask a
regression in the writer.

**Restored state verified:** defect absent from the file, commitment line present, 10/10 green.

---

## 4. THE CORPUS — measured, NOT touched. This is build 2's map

**Nothing in `logs/` was erased, rewritten, or moved.** The battery writes only to `tmp_path`.

### Row 19 — `logs/transcript/`

| | |
|---|---|
| `.jsonl` files | **425** |
| `.txt` companions | **425** |
| turns (jsonl lines) | **27,732** — 13,886 `user`, 13,846 `hip` |
| bytes | **7,390,396** jsonl + **3,133,573** txt = **~10.5 MB** |
| date span | **2026-07-18 → 2026-08-11** |
| members | **bill 10,556** / **maya 9,096** / **sam 8,080** turns |

**Both formats hold the words.** The `.txt` companion is not a derivative to ignore — it is a
second full copy in a different shape, and build 2 must clear both. **850 files, not 425.**

### Row 7 — `logs/memory_engine/recall_audit.jsonl`

| | |
|---|---|
| entries at measurement | **356** |
| entries carrying query text | **356 of 356 — all of them** |
| bytes | **117,739** |

**Now 360 entries.** The four added during this dispatch are the harness runs exercising the real
path, and they are the live proof of the build — same scenario, before and after:

```
pre-fix  (356) "query": "does this person have any allergies?"
post-fix (360) "query_commitment": "hmac-sha256:2a3202bf8e4b5da6901e2a6ecc44832d…"
```

**All 4 post-fix entries carry a commitment and none carries a `query` key.** Build 2's target on
this surface is therefore **the first 356 entries**, not the whole file.

---

## 5. RUNS

Repo `.env.dev` sourced (`NEO4J_URI=bolt://localhost:7688`), never `~/.env.dev`.

| command | result |
|---|---|
| **Standing binding battery**, 56 files | **1168 passed / 0 failed / 9 xfailed** — was 1158/0/9 at 55 files; **+10 is exactly this dispatch's new battery** |
| **`--layer 7`** | **EXIT 0.** L7 **27/27**, L7V2 **27/28** (1 skipped), AUDIT **9/9**, DISC 1/1, SCHEMA 1/1, VOICE 1/1 |
| **RATCHET** | **PASS — no scenario regressed vs baseline** |
| **Memory harness** | **13/17** — inside the 13–15 pin. Not 16/17, so no STOP |
| Battery manifest check | 14/14 — the new file is registered |
| Erasure batteries (`test_erasure_request`, `test_erasure_route`) | 27 passed |

**No deterministic regression.** No live-layer reds to report: `--full` was not run, because this
dispatch changed no live path and asked for no collector run.

---

## 6. WHAT DID NOT HAPPEN

- **Row 19's write path is unchanged** — it still writes verbatim utterances. **The STOP is not a
  partial build; nothing was started there.**
- **No corpus erasure** on either surface. Build 2 owns it.
- **No render-record sealing.** Build 3 owns it.
- **Nothing ruled MET.** `REQ_ERASURE_SURFACES` stays PLAN; row 7's status moves only when Bill
  says so, and the §7 acceptance still fails — row 19 alone guarantees it.
- **The erasure-enablement gate is untouched.**

---

## 7. HA-46 CANNOT START — reported here because it was issued before this landed

**HA-46 (erasure build 2) states: "PRECONDITION: HA-45 landed — the write paths no longer produce
plaintext; if not landed, STOP."**

**That precondition is not met, and will not be met by this dispatch even now that it has
landed.** Row 7's write path no longer produces plaintext; **row 19's still does.** HA-46's own
scope covers both surfaces, and erasing the transcript corpus while the transcript writer keeps
appending fresh plaintext would clear a backlog that immediately begins refilling.

**HA-46 is therefore STOPPED at its precondition, not started.** It becomes runnable once row 19's
option is chosen and built. **Row 7's half of HA-46 could be run independently** — the 356
pre-fix audit entries are a self-contained target — but splitting HA-46 is Bill's call, not a
session's.

---

## CLAIM IMPACT

**none.**

C-09 (*"Erasure leaves no readable trace that the claim existed"*) is the claim this work bears
on. **It gains nothing here**: one of two ruled plaintext surfaces stopped producing new
plaintext, the existing corpus on both is untouched, and status is computed from standing runs by
the generator, never declared by a session.

---

## RECAP

**HA-45** — **row 7 BUILT**: `recall_audit.jsonl` writes a subject-keyed commitment, never the
query's words; 10-test battery registered; fault twin proven red then restored; binding
**1168/0/9xf**, layer 7 **exit 0**, RATCHET **PASS**, memory **13/17** inside the pin.
**ROW 19 STOPPED under item 5** — the demo dashboard's `/api/transcript` renders the words and
the passthrough vignette correlates on them; four options laid out, none chosen. **Corpus mapped
for build 2: 425 jsonl + 425 txt, 27,732 turns, ~10.5 MB, three members; 356 of 356 audit entries
carry query text.** **HA-46 stopped at its precondition.** Nothing ruled MET.
