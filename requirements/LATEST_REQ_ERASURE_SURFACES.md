# REQ_ERASURE_SURFACES — what must disappear on member erasure, surface by surface
Status: PLAN
Reconciled-Against: roadmap `8e427dd` (HA-42, 2026-08-11); surface evidence from HA-41's
segment-2 inventory at `d2d2e9d`, extended by HA-43's read-only resolution of the three UNKNOWNs.

> # RATIFIED — Bill's rulings, 2026-08-11 (HA-44). The dispositions below are RULED, not proposed.
>
> **All six §6 questions are answered. Every disposition in §2 is now a RULING and is binding on
> the build.** The three OPTIONS rows are decided: §3 → **C plus A**, §4 → **B**, §5 → **B**.
>
> **WHAT IS STILL NOT RULED, and this is not a formality:**
> - **NO REQUIREMENT IS RULED MET.** Nothing here has been built and nothing has been measured.
>   **The acceptance in §7 FAILS TODAY** — that is the expected state of a just-ratified spec.
> - **No surface STATUS changed.** The HA-41 status column is untouched: ratifying what *must*
>   happen does not make it have happened. Rows still read UNTOUCHED where they were UNTOUCHED.
> - **The ERASURE-ENABLEMENT GATE is untouched.** No real-data erasure until both conditions land.
>
> **PRIOR BANNER, RETAINED — superseded by the ratification above, not deleted:**
>
> > *NOTHING IN THIS DOCUMENT IS RULED. Every disposition below is marked PROPOSED and is a draft
> > for Bill's ruling. No surface is ruled covered, no data is ruled erasable, no data is ruled
> > retainable, and no requirement is ruled MET. Three rows deliberately carry OPTIONS rather than
> > a proposal, because a session choosing among them would be deciding policy, not engineering.
> > This dispatch changed no product code, fixed no surface, and scrubbed nothing.*
>
> **HA-44 changed no product code either.** It recorded rulings and re-derived the build order.

---

## 0A. BILL'S RULINGS — 2026-08-11, verbatim

> **Q1 — "Governed surface" = ALL NINETEEN enumerated surfaces. The recovery sweep runs against
> every one; pass means each shows its ruled post-erasure state. The narrow definition is
> rejected.**
>
> *(Bill's wording, 2026-08-11, preserved verbatim. **The enumeration has since grown to
> TWENTY-ONE** — rows 20 and 21 added by his ratification of 2026-08-12, §2. The ruling binds
> "all enumerated surfaces"; the number in the sentence is the count on the day it was written,
> not a cap. Annotated rather than edited, because rewriting a quoted ruling to keep a number
> current is how a ruling stops being quotable.)*
>
> **Q2 — "Relevant keys" = all key material whose only purpose is the erased subject's data:
> their per-fact DEKs, their member keypair, their wraps. Shared household/care-team keys are
> NEVER destroyed; instead the erased member's wrap is removed and the shared key rotates to a
> new epoch so the dead wrap cannot return. No bystander's data is erased.**
>
> **Q3 — Rows 7 and 19: C plus A. Stop writing plaintext at the source going forward (logs carry
> keyed commitments or sealed content, never raw words), AND erase existing plaintext on member
> erasure.**
>
> **Q4 — Row 11: B. Seal render records at write time to a per-record key that member erasure
> destroys. Live disputes stay provable; after erasure the words are unrecoverable and the sealed
> blob plus hash still proves an offer existed.**
>
> **Q5 — Rows 10 and 18: B. The tombstone carries an opaque erasure id plus commitment only. It
> never names subject, attribute, or content.**
>
> **Q6 — Row 19 is IN SCOPE by Q1's definition. Today's trivial recovery against transcripts
> blocks the acceptance, so fixing that surface is immediate work under the phase scope rule.**

### 0A.1 THREE CONSEQUENCES THESE RULINGS CREATE, named because they are not obvious from the text

1. **Q5 CONTRADICTS THE TOMBSTONE THAT EXISTS TODAY, and the ledger is append-only.** Erasure
   currently appends a `fact.erased` tombstone **naming what was erased**
   (`harness/graph_erasure.py:88`–`:95`). Q5 forbids that. **The format can change going forward;
   the tombstones already written cannot be removed** — removing them is exactly what row 6
   forbids. **Every historical tombstone therefore stays non-compliant with Q5, permanently**,
   and that is a consequence of append-only-ness, not an oversight. Flagged in §9.
2. **Q2 REQUIRES MACHINERY THAT DOES NOT EXIST.** Wrap removal and shared-key **epoch rotation**
   are not built. This is not a change to erasure; it is a new key-lifecycle capability, and it
   **overlaps the key-custody consolidation that is already condition 1 of the standing
   erasure-enablement gate.**
3. **Q1 SETS THE HIGH BAR, AND THE REQ SAID WHAT THAT COSTS: the acceptance fails today at
   eleven rows.** That is now the ratified target, not a warning.

---

## 0. THE PHASE SCOPE RULE — Bill's ruling, 2026-08-11, verbatim

> **A finding becomes immediate work only if it prevents the 18-surface erasure acceptance from
> succeeding; otherwise file it and continue.**

**How this REQ applies it, stated once so it is not re-derived per row:** the drafting of this
document turned up one surface that HA-41's inventory does not contain (row 19,
`logs/transcript/`) and resolved three UNKNOWNs. **None of that was fixed here.** Row 19 is
filed as **TD-R-188** and recorded in this table; the question of whether it *does* prevent the
acceptance from succeeding is put to Bill in §6 rather than answered by this session, because
the answer turns on whether a transcript is a "governed surface" — Bill's word, and Bill's call.

---

## 1. THE REQUIREMENT — Bill's own words, verbatim

The lifecycle that defines erasure, as Bill stated it:

> **create data → create derivatives → verify they exist → erase → destroy relevant keys →
> restart → attempt recovery from every governed surface → only the opaque proof remains**

And the acceptance question the plan of record states, quoted in HA-41 and carried here
unchanged:

> **"After subject erasure, can HIP still recover meaningful subject data through any supported
> path?"**

**Expanded** (below the quote, so the original survives every rereading): the second quote is
the *test's* question and the first is the *procedure* that asks it. A surface is therefore only
satisfied when erasure **reaches** it — not when the primary copy happened to go. That
distinction is the whole reason this REQ enumerates surfaces instead of asserting "erasure
works".

**Two words in the lifecycle are load-bearing. BOTH ARE NOW DEFINED — Bill ruled them on
2026-08-11 (§0A); the open question below is answered and is retained as the question the ruling
answers:**

1. **"relevant keys"** — which keys a subject erasure destroys. A per-fact DEK is obvious; a
   shared household seal key is not, and destroying one erases other members too (row 16).
   → **ANSWERED by Q2:** subject-only key material is destroyed; **shared keys are never
   destroyed** — the wrap is removed and the key rotates to a new epoch.
2. **"governed surface"** — which of these surfaces the recovery attempt must sweep. If
   it means all of them, the current implementation fails the test at eleven rows. If it means
   the graph and the payload store, it passes today and the words "every governed surface" do
   less work than they appear to (row 19, §6 Q1).
   → **ANSWERED by Q1: ALL enumerated surfaces**, narrow reading rejected — **nineteen at the
   ruling, twenty-one since HA-48.**

---

## 2. THE SURFACE TABLE — one row per surface, every disposition **RULED**

**Status column** is HA-41's inventory verdict, unchanged, except the three UNKNOWNs which HA-43
resolved read-only (marked **†**), row 19 which HA-41 did not contain, and **rows 20 and 21 added
by HA-48** (all marked **NEW**). **A ruled disposition never changes a surface's STATUS** —
ratifying what must happen does not make it have happened.

**Disposition vocabulary:** `ERASE` — must disappear entirely. `ERASE-CONTENT` — content goes, an
opaque shell remains. `RETAIN` — may remain, reason given. `NONE-EXISTS` — nothing to erase
today. `OPTIONS` — Bill chooses; §3, §4, §5.

| # | surface | HA-41 status | WHAT MUST DISAPPEAR (**RULED**) | WHAT MAY REMAIN (**RULED**) | WHY | evidence |
|---|---|---|---|---|---|---|
| 1 | Graph `Fact` nodes | COVERED | **ERASE** — the node and every property on it | nothing | The primary record. If this survives, nothing else matters. | `harness/graph_erasure.py:83`, `:110`, `:127` |
| 2 | Derivatives (lineage closure) | COVERED | **ERASE** — every transitively derived fact, one transaction | nothing | **A derivative reconstitutes the original.** Erasing the parent and leaving a child is not erasure, it is relocation. | `graph_erasure.py:59`, `:104`–`:110` |
| 3 | Per-fact DEK on the node | COVERED by construction | **ERASE** — goes with the node | nothing | Key destruction is what makes any surviving ciphertext opaque. This is the mechanism the last lifecycle step depends on. | `graph_erasure.py:14`–`:24` |
| 4 | Fact metadata (owner, subject, attribute, timestamps, `key_version`) | COVERED *(graph only)* | **ERASE** — in the graph | nothing in the graph; copies in rows 7–11 and 19 are those rows' problem, not this one's | **Metadata alone is meaningful personal information** — HA-10 measured it and Bill ruled it: *"Dad + `health_condition` + HIGH + authored by Sam + date is still meaningful personal information."* | same as 1; ruling in `docs/HIP_HANDOFF.md` erasure gate |
| 5 | Off-ledger payload store | COVERED | **ERASE-CONTENT** — the payload bytes | the event shell and its commitment | The shell with no payload **is** the opaque proof the lifecycle ends on. | `harness/epistemic_ledger.py:686`, `harness/ledger_payload_store.py:134` |
| 6 | HEL ledger events themselves | PARTIAL, intentional | **nothing** — the chain is append-only. **But RULED Q5: the tombstone FORMAT must change** — future `fact.erased` events carry an opaque erasure id + commitment only | **RETAIN** — event shell, keyed commitment, and the tombstone **in its Q5 form**. **Tombstones already written, which NAME what was erased, also remain — they cannot be removed without breaking the chain, so they stay non-compliant permanently (§9)** | **This row is the "opaque proof" itself.** Tamper-evidence requires the chain be unbroken; deleting events to prove deletion destroys the instrument. **CAVEAT, not waived:** this holds for **HEL 2.0** (commitment-only). **HEL 1.0 retains a raw, dictionary-testable `payload_sha256`** and is therefore not opaque in the same sense — governed by the standing HEL 1.0 isolation gate, never joined to real-household data. | `graph_erasure.py:88`–`:95`; `harness/epistemic_ledger.py:474`, `:479`; HEL gate in `docs/HIP_HANDOFF.md` |
| 7 | Raw recall/query text (`logs/memory_engine/recall_audit.jsonl`) | UNTOUCHED | **RULED Q3 — C plus A. (C)** stop writing raw words at the source: the log carries a keyed commitment or sealed content. **(A)** erase existing plaintext for the erased subject | keyed commitments / sealed content whose key is destroyed on erasure | Already **TD-R-173**; the plaintext-retention row Bill ruled closes first. **C bounds the problem, A clears the corpus already on disk — neither alone is sufficient.** | `memory_engine/recall.py:36`; no erasure module references `logs/` |
| 8 | Encode audit log (`logs/memory_engine/encode_audit.jsonl`, 11 MB) | UNTOUCHED | **ERASE-CONTENT** — every record naming an erased fact id, owner or subject | aggregate counts and timestamps carrying **no** subject linkage | No free text, but **fact id + owner is a map back to the erased subject**, and the map is as good as the territory for re-identification. | HA-41 probe: no text-bearing keys, subject metadata persists |
| 9 | Consolidation report / must-confirm queue | UNTOUCHED | **ERASE-CONTENT** — per-fact records naming the subject | aggregate counts with no subject linkage | Same reasoning as row 8; both carry per-fact records. | `logs/memory_engine/consolidation_report.jsonl`, `must_confirm_queue.jsonl`; `memory_engine/consolidate.py:143`, `:154` |
| 10 | Control-plane refusal logs | UNTOUCHED | **RULED Q5 — B.** Any principal/subject naming goes; records carry an **opaque erasure id + commitment only** | the opaque record — refusal happened, provably, naming no one | Holds `situation_id`/principal. **Q5's B resolves the R20–R22 collision cleanly:** an opaque record is *more* isolated from the household record, not less, so satisfying erasure here strengthens the isolation rather than weakening it. | `harness/control_plane_isolation.py`, `harness/offer_response.py` → `logs/offer_control_plane/*.jsonl` |
| 11 | Offer control plane — spend ledger and **R26 render records** | UNTOUCHED | **RULED Q4 — B.** The **per-record key** is destroyed on member erasure, making the wording unrecoverable | the **sealed blob + its hash**, which still proves an offer existed and was not altered | Render records hold the **verbatim wording shown to a member**. **B keeps A19's guarantee intact for live disputes and removes it only at erasure** — and it closes the adversarial hole in option A, since "erase me" now destroys the *words*, not the *evidence that an offer occurred*. **Requires sealing at WRITE time**, so it is a change to the write path, not to erasure. | `harness/spend_ledger.py`, `harness/offer_render_record.py` |
| 12 | Embeddings / indexes | EMPTY | **NONE-EXISTS** — the engine writes `"embedding": None` | n/a | Nothing embeds today. **If embedding is ever built it is a NEW surface** and this row must be re-answered, not inherited. | `memory_engine/store.py:247`–`:248` |
| 13 | Summaries | **†RESOLVED → NONE-EXISTS** | **NONE-EXISTS** — no prose-summary store exists | n/a | **No `def *summar*` or `class *Summar*` exists** in `memory_engine/` or `harness/`; every hit is prose in a comment. Consolidation emits derived **facts** (row 2 covers them), and the transcript writer states text is *"never truncated, never summarized."* Same class as row 12: empty, not covered. | grep over `memory_engine`, `harness`: definitions **zero**; prose only at `memory_engine/store.py:471`, `memory_engine/consolidate.py:510`–`:511`, `harness/transcript_log.py:86` |
| 14 | Caches | **†RESOLVED → IN-MEMORY ONLY** | **nothing to erase on disk**; the lifecycle's **restart** step is what clears them | in-process state before restart | **Six caches, all process-local dicts, none persisted:** `transcript_log.py:37` (`_PATH_CACHE`), **`zep_store.py:392` (`set_hot_cache` → `self._hot`, "Pin identity-level facts in memory")**, `curator_shadow.py:438`, `extraction_queue.py:492`, `permissions.py:82`, **`sio.py:259` (`_cache`, keyed on normalized utterance, max 2048)**. Two hold subject data — identity facts and raw utterances — but **only in memory. Bill's lifecycle already answers this row by putting `restart` before the recovery attempt**, which is why no cache-purge path is proposed. | line refs as listed |
| 15 | Exports | **†RESOLVED → NONE-EXISTS** | **NONE-EXISTS** — no export path exists | n/a | **No `def *export*`, no `to_csv`, no `writerow`** anywhere in `harness/` or `memory_engine/`. The only two "export" hits are a literal `"Exported: "` string in a transcript `.txt` header and a re-export of a Python *name* — neither moves data out. **If an export feature is built it is a NEW surface.** | grep: zero writers; `harness/transcript_log.py:64`, `harness/attribute_vocabulary.py:22` |
| 16 | Key generations (member/household seal keys, `key_version`) | PARTIAL | **RULED Q2 — DESTROY** all key material whose **only** purpose is the erased subject's data: **their per-fact DEKs, their member keypair, their wraps** | **RETAIN** shared household/care-team keys — **NEVER destroyed.** Instead: **the erased member's wrap is REMOVED and the shared key ROTATES TO A NEW EPOCH**, so the dead wrap cannot return | **"No bystander's data is erased"** is the governing constraint, and rotation is what makes removal durable — without a new epoch, a recovered old wrap still opens the shared key. **NEW MACHINERY: wrap removal and epoch rotation do not exist**, and this overlaps the key-custody consolidation already required by the erasure-enablement gate. | `harness/test_key_hygiene.py:101`; `harness/partition_crypto.py:20`, `:47` |
| 17 | Backups | UNTOUCHED | **ERASE** — any subject data in any backup | nothing | **A backup is a complete recovery path**, so an unreached backup defeats the lifecycle's last step by itself. **Mitigating fact, not a fix:** all 16 key-bearing directories are `[Excluded]` from Time Machine as of HA-13, **and no backup destination exists yet** — the exposure is latent, not live. | HA-13 exclusions; grep: no `backup` reference in `graph_erasure.py` / `erasure_request.py` |
| 18 | **Erasure verification itself** (meta-surface) | PARTIAL | **RULED — must be EXTENDED to sweep ALL TWENTY-ONE surfaces (Q1; 19 at the ruling, 21 after HA-48)**, and its own output carries an **opaque erasure id + commitment only (Q5)** | the opaque verification record | `verify_erasure_report` checks a claimed erasure against LIVE state, **but only for `ledger_payload` and graph targets.** **Q1 makes the gap twenty-one-wide, not two-wide.** Until it covers every ruled surface, §7 is verified by hand, **which is how a check becomes decorative.** **A verification report that named what it verified would itself violate Q5** — hence the second clause. | `harness/erasure_report.py:357` |
| 19 | **`logs/transcript/` — verbatim member utterances** | **NEW — not in HA-41's 18** | **RULED Q3 — C plus A**, and **RULED Q6 — IN SCOPE and BLOCKING.** (C) stop writing raw turn text; (A) erase the existing corpus for the erased subject | keyed commitments / sealed content whose key is destroyed on erasure | **RULED IMMEDIATE WORK (Q6): today's trivial recovery against transcripts blocks the acceptance.** **Found while resolving row 13.** `write_transcript_turn` appends **`member_id` + verbatim `text`** to `.jsonl` **and** `.txt`, documented *"written verbatim — never truncated, never summarized."* Files exist on disk for **three members** today. **No erasure module references transcripts.** Filed **TD-R-188**. | `harness/transcript_log.py:79`–`:119`, docstring at `:86`; `logs/transcript/transcript_text-{bill,sam,maya}__*.jsonl/.txt` |

| 20 | **`logs/turns_demo.jsonl` — `query` AND `reply` verbatim** | **NEW — added HA-48** | **RULED Q3 — C plus A**, and **IN SCOPE + BLOCKING** (Bill, 2026-08-12). Stop writing both sides' words; erase the existing backlog | structured metadata, routing/decision fields, keyed commitments | **The worst of the three plaintext surfaces by content: the ONLY one carrying BOTH SIDES of the conversation** — `query` *and* HIP's `reply` — **plus `member` and ~35 routing fields beside them.** Source behind `/api/turns`; **`REQ_TRANSCRIPT_STORAGE` governs it.** Found because HA-45's proposed row-19 fix (point the dashboard here) would have **relocated the plaintext dependency onto it while looking exactly like a fix.** Filed TD-R-190. | 15 records, 50,100 bytes, members **bill/maya/sam**; zero references in `graph_erasure.py`, `erasure_request.py`, `erasure_report.py`, `ledger_payload_store.py`; `server/demo_dashboard.py:877`; `server/static/demo.html:548` |
| 21 | **`logs/router.jsonl` — `query` verbatim** | **NEW — added HA-48** | **RULED Q3 — C plus A**, and **IN SCOPE + BLOCKING** (Bill, 2026-08-12). Stop writing the query; erase the existing backlog | structured routing fields, and `query_hash` **only once it is a keyed commitment** | Carries the raw query beside `query_hash`. **`query_hash` is a BARE, UNKEYED, TRUNCATED SHA-256 — dictionary-testable, R16's exact prohibition — and it is currently LOAD-BEARING** as the consent vignette's only plaintext-free correlator. **Bill's rule, 2026-08-12: a bare truncated hash may never be a load-bearing identifier.** Filed TD-R-190. | 7 records, 2,751 bytes; `harness/escalation_backends.py:220`; no erasure module reference |

### 2.1 Counts by RULED disposition (was: proposed — all four OPTIONS rows are now decided)

| ruled disposition | count | rows |
|---|---|---|
| **ERASE** | **5** | 1, 2, 3, 4, 17 |
| **ERASE-CONTENT** | **3** | 5, 8, 9 |
| **RETAIN** (opaque proof) | **1** | 6 *(tombstone format must change — Q5)* |
| **SEAL-AT-WRITE, key destroyed on erasure** *(Q3-C, Q4-B)* | **5** | 7, 11, 19, **20**, **21** |
| **OPAQUE-ONLY — no subject, attribute or content** *(Q5-B)* | **2** | 10, 18 |
| **DESTROY subject-only keys; ROTATE shared keys to a new epoch** *(Q2)* | **1** | 16 |
| **NONE-EXISTS** | **3** | 12, 13, 15 |
| **NO DISK STATE — cleared by the lifecycle's restart** | **1** | 14 |
| **total** | **21** | 18 from HA-41 + 1 (HA-43) + **2 (HA-48)** |

**Rows requiring a WRITE-PATH change, not an erasure change: 7, 11, 19, 20, 21** — five of
twenty-one, and the single biggest structural consequence of the rulings. **Erasure cannot fix
these by reaching further; the data must stop arriving in plaintext.** Row 18 must then sweep
**all twenty-one.**

> **COUNT AMENDED 2026-08-12 (HA-48), Bill's ratification.** This table read **19** until rows 20
> and 21 were added. **The change is not bookkeeping:** it widened the write-path fix from three
> surfaces to five, and **rows 19, 20 and 21 must be fixed TOGETHER or none of them meaningfully
> is** — surface 20 alone carries both sides of every conversation.
>
> **AND IT IS THE SECOND TIME THE COUNT HAS MOVED.** HA-41 enumerated 18, HA-43 found row 19,
> HA-48 found rows 20 and 21 — **each discovered while doing something else**, because an
> inventory built by asking *"what does erasure touch?"* cannot see a surface no erasure module
> mentions. **Read "21 surfaces" as twenty-one ENUMERATED, not twenty-one EXISTING**, and treat
> §7.2's no-UNKNOWN gate as the standing instrument it was deliberately written to be.

**UNKNOWN COUNT IS NOW ZERO.** All three of HA-41's UNKNOWNs are resolved to a known status,
read-only, with evidence — which is the §7 gate's precondition. **Resolving them required no
fix**, because all three resolved to "nothing exists" or "nothing on disk".

---

## 3. SPECIAL ROW (a) — raw query text, rows 7 and 19. OPTIONS, not a proposal

**Rows 7 and 19 are the same problem at two scales, and they are presented together because a
ruling on one that ignores the other leaves the larger half open.**

- **Row 7** — `recall_audit.jsonl` holds the member's natural-language **queries**. Already
  **TD-R-173**, and by Bill's key-lifecycle ruling this is *"a separate defect, fixed regardless
  of the cascade and explicitly not buried under erasure work."*
- **Row 19** — `logs/transcript/` holds **both sides of every conversation, verbatim**, with
  `member_id`. Strictly larger than row 7: queries are a subset of turns. **Newly found; filed
  TD-R-188.**

**Why these are the sharpest rows in the table:** they are *plaintext*. Every other untouched
surface holds identifiers, metadata or structured records that require the graph to interpret.
These hold the member's own words, readable with `cat`, and **no key destruction makes them
opaque** because they were never sealed.

| option | what it costs | what it buys |
|---|---|---|
| **A — Erase on member erasure**: delete/rewrite records for the erased subject | Rewriting an append-only log; both files are line-oriented so this is mechanically cheap, but it **breaks append-only-ness as a property** and any tamper-evidence built on it later | The lifecycle's last step passes for these rows with nothing left to argue about |
| **B — Seal at write time to a key destroyed on erasure** | Real work now, on every write path; makes the logs unreadable for ordinary debugging, which is what they exist for | Erasure becomes **key destruction**, consistent with the rest of the architecture, and the records stay in place as opaque proof |
| **C — Stop writing plaintext at all** (hash/structure the query; drop turn text) | **Loses the debugging and evaluation value outright** — the transcripts are what the live-layer work reads | Nothing to erase later; the surface stops existing, which is the only permanent fix |
| **D — Retain, ruled acceptable** | **The lifecycle's last step is then false as written** for these rows, and must be reworded to exclude them | No work; honest only if the exclusion is written into the acceptance, not left implied |

**RULED: C PLUS A** (Bill, 2026-08-11). Both halves, not a choice between them — **C** stops raw
words being written at the source (keyed commitments or sealed content), **A** erases the
plaintext already on disk for the erased subject.

**Why both is the right shape, stated because it is the load-bearing part of the ruling:** C
alone leaves today's corpus — transcripts for three members are on disk right now — readable
forever. A alone leaves the surface generating new plaintext faster than erasure can clear it.
**C bounds the problem; A clears the backlog.** D is rejected, so §7's acceptance text stands
unchanged and no exclusion is written into it.

---

## 4. SPECIAL ROW (b) — R26 render records, row 11. The collision, stated honestly

**This is the hardest row in the table, and it is a collision between two things this project
has already ruled it wants.**

- **R26 exists because of A19.** A member disputing what they were shown could otherwise be told
  only the template id. HA-36 made the **exact words shown** durable and hash-verified so the
  record proves what a member actually saw. **That is a member-protective feature**, built to
  answer *"what did you show me?"*
- **And it is a member's personal data**, retained after that member asks to be erased. **The
  right to be erased and the durable proof of what was said to you are the same bytes.**

**Stated plainly: A19's fix created this surface, and nothing considered erasure when it
landed.** That is not a criticism of the fix — it is the cost of it, surfacing now.

| option | what it costs | what it buys |
|---|---|---|
| **A — Destroy render records on erasure** | **Gives up A19's guarantee retroactively.** If a dispute outlives the erasure — or the erasure is *how* the dispute is buried — the system can no longer prove what it showed. **Note the adversarial shape: "erase me" becomes a way to destroy evidence of what HIP said.** | Erasure is complete and simple to verify |
| **B — Seal to a key destroyed on erasure** | Turns the record opaque to *everyone*, including the member and any future auditor. The **fact** of the offer and its hash survive; the wording does not | Consistent with rows 3/5/6 — the shell stays as proof, the content goes with the key. **Architecturally the most consistent option** |
| **C — Retain with subject fields scrubbed** | **Weakest guarantee, and the honest reason is R26's own design:** the record's value IS the verbatim words. Scrubbing `member_id` while keeping the wording leaves text that a session log or timestamp re-links trivially. **Pseudonymisation is not erasure**, and HA-10 already established that metadata alone re-identifies | Keeps the audit trail readable; cheapest to build |
| **D — Retain in full, ruled acceptable as control-plane audit** | Requires ruling that R26 records are **not** member data but system-accountability records — defensible, and it is the same argument row 6 makes for the ledger. **But it must be ruled, not assumed**, and §7's wording must then say so | No work; keeps A19 whole |

**RULED: B** (Bill, 2026-08-11) — seal render records at write time to a **per-record key that
member erasure destroys.**

**What the ruling buys, in Bill's own framing: "Live disputes stay provable; after erasure the
words are unrecoverable and the sealed blob plus hash still proves an offer existed."**

**It resolves the collision rather than trading one side away.** A19's guarantee is intact for
every dispute that arises while the member exists, and **the adversarial hole in option A is
closed**: erasure destroys the *words*, not the *evidence that an offer occurred*, so "erase me"
can no longer be used to destroy the record that HIP made an offer at all. **Note what it costs:
this is a change to the WRITE path** — sealing must happen at record time, and records already
written in plaintext are legacy that A-style erasure must still clear.

---

## 5. SPECIAL ROW (c) — audit surfaces, rows 10 and 18 and the proof itself

**The question this row answers: what may an erasure leave behind as proof that the erasure
happened?** Something must, or erasure is indistinguishable from data loss — and a system that
cannot prove it erased cannot be audited for erasing.

**What is already designed to be that proof, and is proposed to RETAIN (row 6):** the
`fact.erased` tombstone naming what was erased, the HEL event shell, and its keyed commitment.
The chain is append-only and tamper-evident **by design**, and that design is what the
lifecycle's final clause — *"only the opaque proof remains"* — is pointing at.

**The open question is how much the tombstone may say.** A tombstone that names the subject,
the attribute and the timestamp is **itself** the metadata Bill ruled meaningful in row 4:

| option | what it costs | what it buys |
|---|---|---|
| **A — Tombstone names subject + attribute + time** | **Re-identifying metadata survives the erasure**, in the one surface guaranteed to be retained. The strongest form of the row-4 objection | Richest audit; a reader can verify exactly what went |
| **B — Tombstone carries an opaque erasure id + commitment only** | An auditor must be given the mapping out-of-band to check any specific claim | Proof that *an* erasure occurred and was not tampered with, revealing nothing. **Most consistent with the keyed-commitment design** |
| **C — Tombstone carries a keyed commitment to the subject** | Needs the key-custody consolidation that is already a standing gate condition, so it cannot land before that does | Verifiable *by someone holding the key* and opaque to everyone else |

**Row 10 (control-plane refusal logs) is folded in here deliberately** — it is an audit surface,
not a household surface, and **R20–R22 isolate it from the household record on purpose.** The
same three options apply, and the same warning: scrubbing a control-plane log to satisfy an
erasure rule may weaken an isolation guarantee that was ruled for its own reasons.

**Row 18 is the enforcement of all of this.** `verify_erasure_report` covers `ledger_payload`
and graph targets only. **Whatever Bill rules, the verifier must be extended to check it, or
§7's acceptance is a manual claim rather than a machine-checked one.**

### RULED: B (Bill, 2026-08-11)

> **The tombstone carries an opaque erasure id plus commitment only. It never names subject,
> attribute, or content.**

**Applies to row 10 and row 18 alike**, and the row-10 warning above is answered rather than
overridden: an opaque refusal record is **more** isolated from the household record, not less, so
Q5 strengthens R20–R22's isolation instead of trading against it. **Row 18's own output is in
scope too** — a verification report that named what it verified would violate this ruling.

**THE CONSEQUENCE THIS CREATES, AND IT IS PERMANENT (see §0A.1 and §9):** today's tombstone
**names what was erased**. Q5 forbids that going forward, but the chain is append-only and
**already-written tombstones cannot be removed** — removing them is what this very section
forbids. **Every historical tombstone stays non-compliant with Q5, and no future work can fix
that** without destroying the instrument. The format change is forward-only, by construction.

---

## 6. WHAT NEEDED BILL — **ALL SIX ANSWERED, 2026-08-11.** Rulings verbatim in §0A

**Nothing in this section is outstanding.** Q1 → all enumerated surfaces (19 at the ruling; **21 after HA-48**). Q2 → destroy
subject-only key material, never shared keys; remove the wrap and rotate the shared key to a new
epoch. Q3 → C plus A. Q4 → B. Q5 → B. Q6 → row 19 is in scope and **blocking**.

**The questions are retained below as written, unedited**, so the ruling and the question it
answers can be read together.

### 6.1 The questions as originally posed — RETAINED, all now answered

1. **Q1 — What is a "governed surface"?** The lifecycle's recovery step sweeps "every governed
   surface". If that means all nineteen, the system fails today at eleven rows. If it means the
   graph and payload store, it passes today. **This single definition decides whether the
   acceptance is a high bar or a low one**, and it also decides whether row 19 blocks under §0's
   scope rule — which is why this session did not answer it.
2. **Q2 — What are "relevant keys"?** Row 16. Per-fact DEKs are clear; shared household seal
   keys are not, and destroying one erases other members' data too.
3. **Q3 — Rows 7 and 19** (plaintext queries and transcripts): options A–D in §3.
4. **Q4 — Row 11** (R26 render records): options A–D in §4. **The erasure-vs-proof collision.**
5. **Q5 — Rows 10 and 18** (audit surfaces and the tombstone): options A–C in §5.
6. **Q6 — Does row 19 change the phase's scope?** It is filed (TD-R-188) and by the letter of §0
   it is not immediate work, because the 18-surface acceptance can still be run. **By the spirit
   of the lifecycle it may be**, since a recovery attempt against `logs/transcript/` succeeds
   trivially today. **Named, not decided.**

---

## 7. THE ACCEPTANCE TEST

### 7.1 The lifecycle — Bill's words, verbatim, in order

> **create data → create derivatives → verify they exist → erase → destroy relevant keys →
> restart → attempt recovery from every governed surface → only the opaque proof remains**

Executed as a single end-to-end test against a controlled subject, each step observable and each
either passing or failing:

| step | Bill's clause | observable pass condition |
|---|---|---|
| 1 | create data | Facts exist for the controlled subject, ids recorded. |
| 2 | create derivatives | At least one transitively derived fact exists, lineage recorded — so step 7 tests row 2 and not just row 1. |
| 3 | **verify they exist** | Every surface ruled ERASE/ERASE-CONTENT is **positively shown to hold subject data before erasure.** **This step is the anti-vacuity half of the test:** without it, a surface that never held data passes step 7 for the wrong reason and the test proves nothing. |
| 4 | erase | The erasure path runs to completion and reports what it claims to have erased. |
| 5 | destroy relevant keys | **RULED Q2.** The subject's per-fact DEKs, member keypair and wraps are destroyed. **Shared household/care-team keys are shown STILL PRESENT and still usable by other members** — and the erased member's wrap is shown **removed**, with the shared key **rotated to a new epoch**. **A replay of the removed wrap against the rotated key must FAIL**; that check is what proves the removal is durable rather than cosmetic. **No bystander's data is erased** — asserted, not assumed. |
| 6 | **restart** | A **real process restart** — a fresh interpreter, not a reset fixture. **This step is what clears row 14's in-memory caches**, and a same-process test would pass while a real one failed. |
| 7 | attempt recovery from every governed surface | **RULED Q1: "governed surface" = ALL ENUMERATED SURFACES — 19 at the ruling, TWENTY-ONE after HA-48.** A recovery attempt is made against **every one**, and each **shows its ruled post-erasure state.** **A surface not attempted is a FAIL, not a skip** — and the narrow graph+payload reading is explicitly rejected, so this clause is the high bar. |
| 8 | only the opaque proof remains | What remains is exactly what §5's ruling permits — tombstone, event shell, commitment — **and nothing else.** Verified as an allowlist: anything remaining that the ruling does not name is a FAIL. |

### 7.2 The UNKNOWN gate — required, and currently satisfied

> **THE ACCEPTANCE CANNOT PASS WHILE ANY SURFACE IS UNKNOWN.** Every surface must be resolved to
> **covered** or **ruled-may-remain** before the lifecycle can be ruled. An UNKNOWN surface is
> not a small gap: **it is an unmeasured recovery path**, and step 7 cannot sweep what has not
> been enumerated.

**Status as of this REQ: SATISFIED — zero UNKNOWNs.** HA-41's three (summaries, caches, exports)
are resolved in rows 13, 14 and 15, read-only and with evidence. **This gate is standing, not
one-time:** any new surface returns the count to non-zero, **which is exactly what row 19 did to
HA-41's inventory within a day of it being written.**

### 7.3 What this acceptance does NOT claim

- It does not rule any REQ MET, and it does not rule erasure safe for real data.
- **The ERASURE-ENABLEMENT GATE is untouched by this document.** Bill's standing ruling stands:
  no real-data erasure until **both** key-custody consolidation **and** the semantic-metadata
  cascade have landed. Neither is started. **This REQ is a specification, not a step toward
  enabling erasure on real data.**
- It says nothing about HEL 1.0, which is governed by its own isolation gate.

---

## 8. WHAT'S ALREADY DONE — must not be rebuilt

| piece | how it was verified |
|---|---|
| Graph fact erasure + **lineage-closure cascade in one transaction** | `harness/graph_erasure.py:59`, `:104`–`:110`; HA-41 inventory rows 1–2 |
| Off-ledger payload erasure, v1 and v2 | `harness/epistemic_ledger.py:686`; `harness/ledger_payload_store.py:134` |
| `fact.erased` tombstone on an append-only, tamper-evident chain | `graph_erasure.py:88`–`:95` |
| Per-fact DEK removal **by construction** (no separate DEK store exists) | `graph_erasure.py:14`–`:24` |
| `verify_erasure_report` against LIVE state (graph + `ledger_payload` only) | `harness/erasure_report.py:357` |
| The 18-surface inventory itself | HA-41, `d2d2e9d` |
| Time Machine exclusion of all 16 key-bearing directories | HA-13 |

## 9. WHAT'S KNOWN BROKEN

1. **Erasure does not reach `logs/` at all.** No erasure module references it. Rows 7–11 and 19
   are all downstream of this single fact.
2. **Row 19 was missed by the inventory** — and it is the largest plaintext surface in the
   system. Filed **TD-R-188**.
3. **Row 18: the verifier is narrower than the erasure.** It cannot check most of what a ruling
   here would require.
4. ~~**Row 16: "relevant keys" is undefined**~~ — **ANSWERED by Q2.** Replaced by a build gap:
   **wrap removal and shared-key epoch rotation do not exist.** Lifecycle step 5 is executable
   in specification but not yet in code.
5. **Row 6 caveat: HEL 1.0's `payload_sha256` is a raw, dictionary-testable hash** — "opaque
   proof" is true of HEL 2.0 and not of HEL 1.0.
6. **NEW, created by Q5 and permanent: historical `fact.erased` tombstones NAME what was
   erased.** Q5 forbids that going forward, but the chain is append-only and those events cannot
   be removed. **No future work fixes this** — the format change is forward-only by
   construction, and every tombstone written before it stays non-compliant.
7. **NEW, created by Q1: the acceptance now fails at eleven rows**, where the narrow reading
   would have passed today. That is the ratified target, stated so nobody reads the failure as a
   regression.
8. **Rows 7, 11 and 19 need WRITE-PATH changes, not erasure changes.** Erasure reaching further
   cannot fix a surface that keeps generating plaintext.

---

## 11. BUILD ORDER — what these rulings imply, in dependency order

**Nothing below is built. This is the order the rulings force, not a schedule**, and it is
derived here rather than left implicit because Q3's "C plus A" and Q6's "blocking" together
decide what comes first.

### Step 1 — STOP THE PLAINTEXT AT THE SOURCE (Q3-C). Rows 19, then 7
**Blocking, per Q6.** `harness/transcript_log.py::write_transcript_turn` and
`memory_engine/recall.py` stop writing raw words; logs carry keyed commitments or sealed content.
**First because it is the only step that bounds the problem** — every day it is deferred adds
plaintext that step 2 must then clear. Row 19 leads row 7 because it is strictly larger (turns
are a superset of queries).

### Step 2 — ERASE THE EXISTING PLAINTEXT CORPUS (Q3-A). Rows 19, 7
The transcripts on disk today for three members, and `recall_audit.jsonl`. **Separate from step 1
and not optional:** C protects the future, A clears the past, and the acceptance sweeps both.

### Step 3 — SEAL RENDER RECORDS AT WRITE TIME (Q4-B). Row 11
Per-record key, destroyed on member erasure. **A write-path change like step 1**, and it carries
the same legacy tail: records already written in plaintext must be cleared as in step 2.

### Step 4 — KEY LIFECYCLE: WRAP REMOVAL + EPOCH ROTATION (Q2). Row 16
**New machinery.** Destroy subject-only key material; remove the erased member's wrap from shared
keys and rotate those keys to a new epoch. **Overlaps key-custody consolidation, which is already
condition 1 of the erasure-enablement gate** — these should be planned together, not twice.

### Step 5 — TOMBSTONE AND AUDIT SURFACES GO OPAQUE (Q5-B). Rows 6, 10
New `fact.erased` format: opaque erasure id + commitment, naming nothing. Control-plane refusal
logs likewise. **Forward-only; §9 item 6 is permanent.**

### Step 6 — METADATA SURFACES (ERASE-CONTENT). Rows 8, 9
Encode audit, consolidation report, must-confirm queue: records naming an erased fact id, owner
or subject go; aggregate counts with no subject linkage may stay.

### Step 7 — EXTEND THE VERIFIER TO ALL TWENTY-ONE (Q1). Row 18
**Last, because it verifies the other six**, and its own output must be opaque per Q5.
**Until this lands the acceptance is a manual claim**, which is how a check becomes decorative.

### Standing, not a step
- **Row 17, backups:** latent — no backup destination exists. **Must be answered before one is
  created**, not after.
- **Rows 12, 13, 15** (embeddings, summaries, exports): NONE-EXISTS today. **If any is ever
  built it is a new surface and re-opens the §7.2 gate.**
- **Row 14, caches:** no work; the lifecycle's restart step covers it.

### What this order does NOT authorise
**No step here is authorised to run on real household data.** The ERASURE-ENABLEMENT GATE is
unchanged and neither of its conditions has landed.

## 10. CONSTRAINTS — what must not regress

- **The ledger chain stays append-only and tamper-evident.** No ruling here may delete HEL events
  to satisfy an erasure claim; that destroys the instrument that proves the erasure.
- **R20–R22 control-plane isolation** must not be weakened to satisfy row 10.
- **The ERASURE-ENABLEMENT GATE holds.** Both conditions, unchanged.
- **The HEL 1.0 isolation gate holds.** No migration carries HEL 1.0 events forward.
- **A19/R26's guarantee** may be traded away only by an explicit ruling under §4 — never as a
  side effect of an erasure fix.
- **No erasure work proceeds on real household data** under any ruling in this document.
