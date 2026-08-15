COMPLETE WITH FINDINGS — 1 ITEM FILED, NOTHING BLOCKING

# DISPATCH_HA43_ERASURE_SURFACES_REQ — the Phase 3 opener: a requirement drafted, three unknowns closed, one surface found
Status: BUILT (docs only — no product code changed)
Reconciled-Against: roadmap `8e427dd` (HA-42) at start; landed this dispatch

**Dispatch ID: HA-43.** Docs only. **Nothing was ruled, no product code changed, no erasure fix
was made, and nothing was scrubbed.**

---

## 0. THE DISPATCH ID — a collision, reported before anything else

**This dispatch was issued as HA-42. HA-42 was already taken** — by the ruling-enactment
dispatch landed earlier the same day at `8e427dd`, which is pushed and cited in `docs/INDEX.md`,
`docs/deliverables/MANIFEST.md`, `docs/HIP_HANDOFF.md` and its own commit message.

**It runs as HA-43.** STANDARD PREAMBLE item 10 forbids renumbering an ID other documents
already cite, and HA-42 is cited in four places. Renumbering the landed dispatch to free the
number would break every one of them to fix a label. **Reported rather than silently
renumbered**, because the dispatch Bill issued and the dispatch in the record now have different
numbers, and only this note connects them.

---

## 1. WHAT WAS ASKED, AND WHAT LANDED

| # | asked | landed |
|---|---|---|
| 1 | Draft `REQ_ERASURE_SURFACES` from HA-41's 18-surface inventory, one row per surface, every disposition PROPOSED | **Done — 19 rows** (18 + 1 found while drafting), anchored to file/module evidence |
| 2 | Three rows written as OPTIONS, not proposals: raw query text, R26 render records, audit surfaces | **Done — §3, §4, §5** of the REQ; four options for (a), four for (b), three for (c). **None proposed** |
| 3 | Acceptance = Bill's lifecycle verbatim, plus the no-UNKNOWN gate | **Done — §7**, the eight clauses as an ordered pass/fail table, gate at §7.2 |
| 4 | Resolve the 3 UNKNOWN surfaces, read-only, evidence cited | **Done — all three resolved.** UNKNOWN count is now **zero** |
| 5 | Register per governance; rule nothing | **Done.** Rules nothing |

**The REQ:**
`docs/requirements/REQ_ERASURE_SURFACES__nineteen-surfaces-proposed-dispositions-and-the-lifecycle-acceptance__v20260811_2050.md`

---

## 2. THE THREE UNKNOWNS, RESOLVED — read-only, evidence cited

HA-41 left summaries, caches and exports genuinely unknown, and said so rather than assuming
them absent. **All three are now resolved, and none required a fix** — each resolved to "nothing
exists" or "nothing on disk."

### 2.1 Summaries → **NONE-EXISTS**

**No prose-summary store exists.** A search for definitions — `def *summar*`, `class *Summar*` —
across `memory_engine/` and `harness/` returns **zero**. Every occurrence of the word is prose
inside a comment or docstring: `memory_engine/store.py:471`, `memory_engine/consolidate.py:510`–
`:511`, `harness/transcript_log.py:86`.

Consolidation emits derived **facts**, which the lineage closure (surface 2) already covers, plus
report/queue rows (surface 9). **The transcript writer's docstring states the text is "never
truncated, never summarized"** — the same line that produced the finding in §3.

**Same class as embeddings: empty, not covered.** If summarization is ever built it is a NEW
surface and this row must be re-answered, not inherited.

### 2.2 Caches → **IN-MEMORY ONLY; the lifecycle's restart step is what clears them**

Six caches, **all process-local dicts, none persisted to disk**:

| cache | location | holds |
|---|---|---|
| `_PATH_CACHE` | `harness/transcript_log.py:37` | session_id → file paths |
| **`self._hot`** via `set_hot_cache` | **`harness/zep_store.py:392`** | **identity-level facts — name, members, preferences.** Docstring: *"Pin identity-level facts in memory. Injected every turn, no graph hit."* |
| `_WEIGHT_CACHE` | `harness/curator_shadow.py:438` | scoring weights |
| `_LIFECYCLE_FILE_CACHE` | `harness/extraction_queue.py:492` | file paths |
| `_role_cache` | `harness/permissions.py:82` | role definitions |
| **`_cache`** | **`harness/sio.py:259`** | **keyed on normalized utterance**, max 2048 |

**Two of the six hold subject data** — identity facts and raw utterances — **but only in
memory.** No cache-purge path is proposed for one reason worth stating: **Bill's lifecycle
already answers this row by putting `restart` before the recovery attempt.** A fresh interpreter
has empty caches. The requirement this creates is not a purge path but a **real** restart in the
test (REQ §7.1 step 6) — a same-process reset fixture would pass while a real restart failed.

### 2.3 Exports → **NONE-EXISTS**

**No export path exists.** No `def *export*`, no `to_csv`, no `writerow` anywhere in `harness/`
or `memory_engine/`. Two hits for the word, neither of which moves data out: a literal
`"Exported: "` string in a transcript `.txt` header (`transcript_log.py:64`) and a re-export of a
Python *name* (`attribute_vocabulary.py:22`).

**Nothing to erase today. If an export feature is built it is a NEW surface.**

---

## 3. THE FINDING — a nineteenth surface, and how the inventory missed it

**`logs/transcript/` retains verbatim member utterances, and no erasure path reaches it. Filed
TD-R-188.**

`harness/transcript_log.py::write_transcript_turn` (`:79`–`:119`) appends **`member_id` and
verbatim turn `text`** — user turns *and* HIP's replies — to **two files per session, `.jsonl`
and `.txt`**. The docstring at `:86` states the text is *"written verbatim — never truncated,
never summarized."* **Transcript files exist on disk today for three members** (`text-bill`,
`text-sam`, `text-maya`).

**No erasure module references transcripts**, confirmed against `graph_erasure.py`,
`erasure_request.py`, `erasure_report.py` and `ledger_payload_store.py`.

### Why HA-41's inventory missed it, and why that is the interesting part

**It was found while resolving row 13.** `transcript_log.py` appeared in the summary search
*precisely because it declares that it never summarizes.*

HA-41's inventory was built by asking, surface by surface, **"what does erasure do here?"** That
question is answered by reading the erasure modules and following what they touch. **A surface
that no erasure module mentions, in a directory no erasure module references, is invisible to
it** — and HA-41 recorded exactly that fact about itself: *"no erasure module references `logs/`
at all."* The inventory named its own blind spot; it just could not enumerate what fell inside
it.

**This is a worked example one day after the inventory was called complete**, which is why the
REQ's UNKNOWN gate (§7.2) is written as **standing, not one-time**.

### It is strictly larger than TD-R-173

TD-R-173 is raw **query** text in `recall_audit.jsonl`. **Queries are a subset of turns**, and
this surface holds every turn plus HIP's replies. Both are plaintext, and the sharp point is the
same for both: **no key destruction makes them opaque, because they were never sealed.** Every
other untouched surface holds identifiers or structured records that need the graph to
interpret; these hold the member's own words, readable with `cat`.

TD-R-173 has a ruling — Bill's key-lifecycle ruling makes it *"a separate defect, fixed
regardless of the cascade."* **TD-R-188 has none.**

### It was filed and left, per the phase scope rule

Bill's rule, verbatim: *"A finding becomes immediate work only if it prevents the 18-surface
erasure acceptance from succeeding; otherwise file it and continue."*

**Filed, not fixed.** By the letter of the rule it does not block: the 18-surface acceptance can
still be run. **By the spirit of the lifecycle it may**, because a recovery attempt against
`logs/transcript/` succeeds trivially today, and the lifecycle's last step says *"attempt
recovery from every governed surface."* **Whether a transcript is a "governed surface" is Q1 of
the REQ and is Bill's call — this session did not answer it**, and did not let its own finding
quietly redefine the phase.

---

## 4. THE REQ — what it contains

**19 rows.** Each carries: the surface, HA-41's status, WHAT MUST DISAPPEAR, WHAT MAY REMAIN,
WHY, and file/module evidence. **Every disposition is marked PROPOSED.**

| proposed disposition | count | rows |
|---|---|---|
| **ERASE** | 5 | graph nodes, derivatives, per-fact DEK, fact metadata, backups |
| **ERASE-CONTENT** (content goes, opaque shell remains) | 3 | payload store, encode audit, consolidation/must-confirm |
| **RETAIN** | 2 | HEL ledger events, shared key generations |
| **OPTIONS — Bill chooses** | 4 | recall query text, refusal logs, R26 render records, **transcripts (new)** |
| **NONE-EXISTS** | 3 | embeddings, summaries, exports |
| **NO DISK STATE — cleared by restart** | 1 | caches |
| **MUST BE EXTENDED** (meta-surface) | 1 | erasure verification |
| **total** | **19** | |

### The three special rows

- **(a) Plaintext — rows 7 and 19.** Presented together, because ruling on the query log while
  ignoring the transcripts leaves the larger half open. Four options: erase / seal to a key
  destroyed on erasure / stop writing plaintext / retain-and-rule-acceptable. **Option D is
  honest only if §7's acceptance text changes with it** — that is stated in the REQ, because a
  retained surface plus an unchanged "every governed surface" clause is a false acceptance.
- **(b) R26 render records — row 11. The collision, stated without softening:** *the right to be
  erased and the durable proof of what was said to you are the same bytes.* A19's fix created
  this surface and nothing considered erasure when it landed. Four options, with the adversarial
  shape named — **under option A, "erase me" becomes a way to destroy evidence of what HIP
  said.** B (seal to a destroyed key) and D (rule it control-plane audit) are the two coherent
  positions; C (scrub subject fields) is included **with why it is weak**, since the record's
  entire value is the verbatim words and pseudonymisation is not erasure.
- **(c) Audit surfaces — rows 10 and 18.** What may remain as proof the erasure happened. The
  designed answer is the `fact.erased` tombstone plus the HEL event shell and commitment; the
  open question is **how much the tombstone may say**, since a tombstone naming subject +
  attribute + time is itself the metadata Bill ruled meaningful. Three options. Row 10 is folded
  in with a warning: **scrubbing a control-plane log to satisfy an erasure rule may weaken the
  R20–R22 isolation that was ruled for its own reasons.**

### The acceptance section

**Bill's lifecycle verbatim**, as an ordered eight-clause pass/fail table. Two clauses carry
load the prose does not make obvious, and the REQ says so:

- **Step 3, "verify they exist", is the anti-vacuity half.** Without it, a surface that never
  held subject data passes step 7 for the wrong reason and the test proves nothing.
- **Step 6, "restart", must be a real process restart** — that is what clears row 14's in-memory
  caches, and a reset fixture would pass where a real restart failed.
- **Step 8 is verified as an allowlist:** anything remaining that the ruling does not name is a
  FAIL.

**The UNKNOWN gate is in and is currently SATISFIED — zero unknowns.** Written as **standing,
not one-time**, for the reason §3 demonstrates.

---

## 5. TWO WORDS IN THE LIFECYCLE ARE UNDEFINED

Named here because they are the difference between a high bar and a low one, and neither is a
session's to define:

1. **"governed surface"** — if it means all nineteen, the system fails today at eleven rows. If
   it means the graph and the payload store, **it passes today**, and the clause does less work
   than it appears to.
2. **"relevant keys"** — per-fact DEKs are clear. **Shared household seal keys are not:
   destroying one erases other members too.** Until this is settled, lifecycle step 5 is not
   executable.

---

## 6. WHAT NEEDS BILL

1. **Q1 — what is a "governed surface"?** Decides the bar, and decides whether row 19 blocks.
2. **Q2 — what are "relevant keys"?** Row 16.
3. **Q3 — rows 7 and 19**, plaintext queries and transcripts: options A–D.
4. **Q4 — row 11**, R26 render records: options A–D. The erasure-vs-proof collision.
5. **Q5 — rows 10 and 18**, audit surfaces and how much the tombstone may say: options A–C.
6. **Q6 — does row 19 change the phase's scope?** Filed under the scope rule; named, not decided.

---

## 7. WHAT DID NOT HAPPEN — stated so silence is not read as coverage

- **No product code changed. No erasure fix, no scrub, no purge path, no verifier extension.**
- **Nothing ruled.** No REQ MET, no disposition ruled, no claim status moved.
- **No surface was fixed to make a count look better.** Rows 13/14/15 resolved to
  "nothing exists" on the evidence, not because resolving them was convenient.
- **The ERASURE-ENABLEMENT GATE is untouched**; neither condition is started, and this REQ is a
  specification, not a step toward enabling erasure on real data.
- **No harness run.** This dispatch changed no code, so there is nothing to re-measure; HA-41's
  runs remain the standing evidence.

---

## CLAIM IMPACT

**none.**

No claim status moved and none may — status is computed from standing runs by the generator,
never declared by a session. C-09's erasure wording is the claim this work will eventually bear
on, **but nothing here is evidence for it**: a specification is not a run.

---

## RECAP

**HA-43** — drafted `REQ_ERASURE_SURFACES` (19 surfaces, every disposition PROPOSED, nothing
ruled); resolved HA-41's three UNKNOWNs read-only to zero; **found a nineteenth surface —
`logs/transcript/` verbatim member utterances, no erasure path reaches it — filed TD-R-188**;
wrote Bill's lifecycle verbatim as the acceptance with a standing no-UNKNOWN gate; six decisions
put to Bill. **Issued as HA-42, run as HA-43** — that number was taken by `8e427dd`.
