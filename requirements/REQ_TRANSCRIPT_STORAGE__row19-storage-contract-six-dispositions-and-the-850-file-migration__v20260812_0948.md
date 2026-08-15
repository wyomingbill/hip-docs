# REQ_TRANSCRIPT_STORAGE — the row-19 storage contract
Status: PLAN
Reconciled-Against: roadmap `3cf9619` (HA-46A, 2026-08-12); consumer evidence established
read-only by HA-47.

> # RATIFIED — Bill's ruling, 2026-08-12 (HA-48). Q1–Q6 are RULED, with four additions.
>
> **All six dispositions in §3 are ratified AS PROPOSED and are binding on the build.** Four
> additions were made at ratification and are recorded at **§3A** (surfaces 20 and 21),
> **§3B** (the keyed-commitment rule), **§4** (the ordering clause, now binding) and **§6.2**
> (the accepted `.txt` loss).
>
> **WHAT IS STILL NOT RULED:**
> - **NO REQUIREMENT IS RULED MET.** Nothing is built and nothing is measured. **The acceptance
>   in §7 fails today** — the expected state of a just-ratified contract.
> - **No surface STATUS changed.** Ratifying what must happen does not make it have happened.
> - **The ERASURE-ENABLEMENT GATE is untouched**, and no step here authorises real-data erasure.
>
> **SCOPE WIDENED AT RATIFICATION: this contract governs THREE surfaces, not one** — row 19
> (`logs/transcript/`), **row 20 (`logs/turns_demo.jsonl`)** and **row 21 (`logs/router.jsonl`)**.
> **The writer fix must cover all three**, and all three block the acceptance equally. §3A.
>
> **PRIOR BANNER, RETAINED — superseded by the ratification above, not deleted:**
>
> > *NOTHING IN THIS DOCUMENT IS RULED. Every disposition is PROPOSED and is a draft for Bill's
> > ruling. No writer was changed, no corpus was touched, no consumer was changed. HA-47 was
> > docs + read-only throughout.*
>
> **HA-48 changed no code either.** It recorded the ratification and its four additions.
>
> **One thing here is not a proposal but a measurement, and it is time-critical: all 27,732
> transcript turns can be committed TODAY, and that window closes the moment Q2 destroys the
> three members' keys.** §5.

**Authority:** Bill's ruling, 2026-08-11 — row 19 needs a storage contract before any build, and
**the dashboard never decrypts arbitrary transcript files.** That constraint is treated as
binding throughout and eliminates one otherwise-obvious option at Q4.

---

## 1. WHAT THE CONSUMERS ACTUALLY USE — established read-only, with evidence

HA-45 named two consumers. **A third was found, and it is unaffected.** More importantly, the
investigation turned up **two plaintext surfaces that are in no inventory** (§2), which changes
the answer to Q4.

### 1.1 `/api/transcript` → the dashboard's conversation band

**The endpoint returns the whole record** (`server/demo_dashboard.py:906`): `ts`, `ts_mt`,
`session_id`, `member_id`, `speaker`, `text`, `tier`, `tier_target`.

**`TurnBubble` — the renderer — uses exactly four fields** (`server/static/demo.html:502`–`:531`):

| field | what it draws |
|---|---|
| `speaker` | which side the bubble sits on, and the `HIP` label |
| `member_id` | the speaker name and its colour |
| `tier` | the `[tier]` tag on user turns |
| **`text`** | **the bubble's contents — the only member-content field rendered** |

`ts` is used for `?since=` filtering and sort order, never displayed. Everything the API returns
beyond those is unused by the renderer.

**So the dashboard needs exactly one thing from this surface: the words of the current session.**

### 1.2 The passthrough consent vignette — and its correlation is already redundant

`eval/passthrough_consent_vignette.py:_assert_b2` identifies turn 2's user record and checks it
escalated:

```python
transcript_escalate = any(
    r.get("speaker") == "user" and r.get("tier") == "escalate"
    and t2_query[:40] in (r.get("text") or "")
    for r in transcript)
...
ok = response_ok and (transcript_escalate or new_escalate)
```

**The 40-character prefix distinguishes ONE THING: which transcript record is turn 2's user
turn.** It is an identity match, not a content assertion — the assertion is `tier == "escalate"`.

**And it is one branch of an OR.** The other branch, `new_escalate`, correlates through
`logs/router.jsonl`'s **`query_hash`** and **already works without any plaintext**. The vignette
therefore has a plaintext-free path today; the transcript-text branch is redundant belt to its
braces.

**One caveat that matters to Q5, and it is not a small one:** `query_hash` is
`hashlib.sha256(query.encode()).hexdigest()[:16]` (`harness/escalation_backends.py:220`) — **a
bare, unkeyed, truncated SHA-256.** It is plaintext-free but **dictionary-testable**: a short
natural-language query is trivially recoverable by enumeration. It is the same construction R16
exists to forbid and the same defect that makes HEL 1.0 non-opaque. **Q5 must not entrench it.**

### 1.3 `eval/integration_harness.py` DEMO-002 — a third consumer, unaffected

Asserts both members appear with both speaker labels. Uses `member_id` and `speaker` only
(`:866`–`:875`). **Needs no words.**

### 1.4 Consumers confirmed to need no words

`eval/test_demo_smoke.py` (`member_id`, `speaker`, `ts`, mtimes), `scripts/build_evidence_package.py`
(per-turn metadata), the dashboard's source-list endpoint (`:1150`, filenames only).

**Summary: of six consumers, exactly one needs the words — the live conversation band — and it
only ever needs the CURRENT session's.**

---

## 2. TWO PLAINTEXT SURFACES THAT ARE IN NO INVENTORY — found while answering Q4

**Filed as TD-R-190.** Neither is among `REQ_ERASURE_SURFACES`'s nineteen, and **no erasure
module reaches either** (checked against `graph_erasure.py`, `erasure_request.py`,
`erasure_report.py`, `ledger_payload_store.py` — zero references).

| # | surface | content | extent |
|---|---|---|---|
| **20** | **`logs/turns_demo.jsonl`** | **`query` AND `reply` verbatim**, plus `member`, and ~35 routing/decision fields | 15 records, 50,100 bytes, members **bill, maya, sam** |
| **21** | **`logs/router.jsonl`** | **`query` verbatim**, alongside the weak `query_hash` | 7 records, 2,751 bytes |

### Why this changes Q4 rather than being a footnote

**HA-45 offered "switch the dashboard to the live feed" as option B.** That option reads
`/api/turns`, which reads **`logs/turns_demo.jsonl`** — surface 20. The renderer even maps it
into the same shape (`d1ToTranscriptTurns`, `demo.html:548`), so it would have worked perfectly
and **relocated the plaintext dependency onto an unenumerated surface rather than removing it.**

**That is the trap this contract exists to avoid**, and it is the concrete argument for Q4's
proposed disposition: the fix cannot be "read a different file," because the other file is also
plaintext.

---

## 3. THE SIX QUESTIONS — **RULED** (Bill, 2026-08-12), as proposed

**Every disposition below was ratified exactly as drafted.** The wording is unchanged from the
draft HA-47 put to Bill — nothing was softened or re-scoped at ratification, and the alternatives
are retained beneath each so the ruling and what it rejected can be read together.

**Read "PROPOSED" in the subsections below as "RULED".** The word is left in place rather than
rewritten in eleven spots, because the banner and this paragraph carry the status and a silent
find-and-replace through a ratified document is exactly the edit that later reads as drift.

### Q1 — What transcript content must remain recoverable?

**PROPOSED: the verbatim words of a session remain recoverable only while that session is live.
Nothing durable retains recoverable words.** What persists per turn is structured metadata plus a
keyed commitment.

**Why:** §1 establishes that the only consumer needing words is the live band, and it only ever
shows the current session. **No consumer anywhere reads historical transcript words.** Retaining
them durably serves nothing that was measured.

| alternative | cost |
|---|---|
| All turns recoverable indefinitely (status quo) | Maximal exposure for zero measured benefit; row 19 stays open forever |
| Nothing recoverable, not even live | Live band goes blank; the demo loses its conversation display |
| **Session-scoped (proposed)** | **Historical transcripts become unreadable to humans — a real loss, named at §6.3** |

### Q2 — Recoverable for whom?

**PROPOSED: for the speaking member, and for the live session's operator while that session
runs. For nobody else, and for nobody afterwards.** A holder of the durable file can read
structured metadata and a commitment, never words.

| alternative | cost |
|---|---|
| Any holder of the file (status quo) | Anyone with disk access reads every household conversation |
| Member only | The live demo band could not render another member's turn — DEMO-002 merges maya and sam deliberately |
| Member + auditor holding a key | Adds a standing decryption capability whose custody is unspecified; **conflicts with "the dashboard never decrypts"** in spirit |

### Q3 — Under which key/custody scope?

**PROPOSED: a per-session content key, wrapped to each participating member's key. The session
key is held in memory for the session's life and never written. The durable per-turn commitment
is keyed to the speaking member**, matching HA-45's precedent for row 7.

**Why per-session rather than per-turn or per-member:** per-turn would mint ~27,732 keys and walk
straight into TD-R-172's key-population growth; per-member gives erasure granularity no finer
than "this member, all sessions, forever," which is coarser than Q6 needs.

**This is Q2/step-4 custody work and must be sequenced with it, not before it** — building a
second key convention ahead of the custody consolidation is the mistake HA-45 declined to make.

> **THE GUARANTEED PROPERTY IS "THE KEY NEVER REACHED DISK" — NOT "THE KEY IS ERASED FROM
> MEMORY" (recorded HA-49A, on external review).** `end()` zeroes the buffers the implementation
> owns, but **Python cannot guarantee that no copy survives in process memory**: `bytes` are
> immutable and the cryptography library holds its own copies. **Do not strengthen this claim in
> this document, in the module, or in any UI text.** The disk-absence property is testable and is
> tested by filesystem search; a memory-erasure claim would be untestable here and false.
>
> **An audit at HA-49A found no such overclaim** in this REQ, the module or the dispatch docs —
> every existing phrasing says "held in memory" or "never written", which is accurate. This note
> states the boundary explicitly so the next reader does not infer the stronger claim from the
> weaker one, and a standing test asserts the module never acquires it.

| alternative | cost |
|---|---|
| Per-member key | Simplest; erasure granularity is member-wide only |
| Per-turn key | Finest granularity; **key explosion, TD-R-172** |
| **Per-session, wrapped to members (proposed)** | Needs wrap + rotation machinery — **the same machinery Q2 already requires**, so it is shared work, not new work |

### Q4 — How does `/api/transcript` read it?

**PROPOSED: it does not. `/api/transcript` stops reading transcript files altogether.** The live
band is fed from an **in-memory, session-scoped buffer owned by the running server**, populated
as turns occur and discarded when the session ends. Durable transcript files become
commitment-only and **are read by nothing.**

**This satisfies Bill's constraint exactly and by construction: the dashboard never decrypts
anything, because there is nothing to decrypt and no file is read.**

**It must NOT be implemented by pointing the band at `/api/turns`** — §2 — because that surface
is itself plaintext. **Naming this explicitly, because it is the obvious shortcut and it looks
like a fix.**

| alternative | cost |
|---|---|
| Dashboard decrypts transcript files | **EXCLUDED by Bill's ruling.** Listed only so the exclusion is visible |
| Server-side decrypt endpoint returning words to the browser | Server must hold keys continuously; words still cross HTTP; recreates the capability the ruling removes |
| Feed the band from `/api/turns` | **Relocates the dependency onto surface 20.** Solves nothing |
| **In-memory session buffer (proposed)** | Historical sessions are no longer viewable in the dashboard; a server restart mid-session loses the band's backlog |

### Q5 — How does the vignette correlate turns without plaintext prefixes?

**PROPOSED: correlate on `turn_id`** — already present in the d1.1 record shape and already used
as the renderer's key (`demo.html:551`). Where a turn id is unavailable, fall back to matching a
**keyed commitment**, never a bare hash.

**And the contract should require `query_hash` to become a keyed commitment** (§1.2). It is
currently a truncated unkeyed SHA-256; leaving it in place would make the vignette's
plaintext-free path depend on a dictionary-testable digest, which trades one exposure for a
quieter one.

**No test coverage is lost by dropping the text branch:** the OR's other half already passes
through the router path.

| alternative | cost |
|---|---|
| **`turn_id` (proposed)** | Cleanest; requires the transcript record to carry it — it does not today |
| Keyed-commitment match | Works with no new field; costs a key read per correlation in a test |
| Keep the bare `query_hash` | **Rejected: R16's exact prohibition**, and it would be newly load-bearing |

### Q6 — What happens on member erasure, and on household erasure?

**PROPOSED — member erasure:** destroy that member's key material (Q2's definition), which makes
every wrap of every session key covering their turns unopenable. **Shared/household keys are
never destroyed — the member's wrap is removed and the shared key rotates to a new epoch**, per
Q2. The durable transcript record **keeps its structured metadata and its commitment** and loses
nothing else, because it never held words.

**PROPOSED — household erasure:** destroy the household key generation together with the member
keys in its scope. No rotation is required, because nothing remains that the rotation would
protect.

**In both cases records are NOT deleted.** A field goes opaque; the entry count is preserved.
That is the shape HA-46A already established for row 7 and it is what keeps the surface
auditable.

| alternative | cost |
|---|---|
| Delete transcript records outright on erasure | No auditable trace that a session occurred; breaks the "opaque proof remains" clause |
| **Key destruction, records retained (proposed)** | Requires the wrap/rotation machinery of Q2 |

---

## 3A. RATIFICATION ADDITION — surfaces 20 and 21 are IN SCOPE and BLOCKING

**Bill's ruling, 2026-08-12.** `logs/turns_demo.jsonl` and `logs/router.jsonl` are added to
`REQ_ERASURE_SURFACES` as **rows 20 and 21**, and to this contract's scope.

> **They carry verbatim words with member names, recovery against them succeeds trivially today,
> and they block the acceptance the same as row 19. The writer fix must cover all three.**

| # | surface | content | extent | erasure reaches it |
|---|---|---|---|---|
| **20** | `logs/turns_demo.jsonl` | **`query` AND `reply` verbatim**, plus `member`, plus ~35 routing/decision fields | 15 records, 50,100 bytes, members **bill, maya, sam** | **no** |
| **21** | `logs/router.jsonl` | **`query` verbatim**, alongside the weak `query_hash` | 7 records, 2,751 bytes | **no** |

**Evidence:** neither appears in `REQ_ERASURE_SURFACES`'s original nineteen; zero references in
`graph_erasure.py`, `erasure_request.py`, `erasure_report.py` or `ledger_payload_store.py`.
Surface 20 is the source behind `/api/turns` and the client maps it into the same render shape
(`d1ToTranscriptTurns`, `server/static/demo.html:548`). Filed as **TD-R-190**.

**THE PRACTICAL CONSEQUENCE, AND IT IS THE POINT OF THE ADDITION: "fix row 19" is no longer a
sufficient description of the work.** A writer fix covering transcripts alone leaves `query` and
`reply` — **HIP's replies too, which transcripts alone would not have exposed** — accumulating in
surface 20 with member names attached. **All three surfaces stop producing plaintext together, or
none of them meaningfully does.**

**Row 20 is strictly the worst of the three by content**: it is the only surface carrying both
sides of the conversation *and* the full routing decision beside them.

---

## 3B. RATIFICATION ADDITION — the keyed-commitment rule

**Bill's ruling, 2026-08-12:**

> **A bare truncated hash is dictionary-testable and may never be a load-bearing identifier.**

**Binding wherever an identifier stands in for content.** Concretely, today:

- **`query_hash` is `hashlib.sha256(query.encode()).hexdigest()[:16]`**
  (`harness/escalation_backends.py:220`) — unkeyed and truncated to 64 bits. A short
  natural-language query falls to enumeration; the digest is a lookup key for the words, not a
  substitute for them.
- **It is currently load-bearing**, which is what makes this urgent rather than theoretical: it
  is the consent vignette's only plaintext-free correlation path
  (`passthrough_consent_vignette.py`, the `new_escalate` branch).

**Required:** `query_hash` becomes a **keyed commitment** — the same
`compute_keyed_commitment` construction HEL 2.0 and row 7 already use — or it stops being relied
on for identity. **Q5's `turn_id` correlation satisfies the rule by removing the dependency
entirely**, which is why it is the ruled disposition rather than "strengthen the hash".

**This is the same defect class as HEL 1.0's `payload_sha256`** and it is what R16 exists to
forbid. Recorded as a rule rather than a one-off fix so the next identifier is not built the same
way.

---

## 4. CONTRACT CLAUSE — the TD-R-189 ordering rule

**RULED BINDING at ratification — Bill, 2026-08-12:**

> **Any retained post-erasure evidence requiring cryptographic verification must have its
> governed keyed commitment minted and verified BEFORE the subject key is destroyed.**

The clause as originally drafted, retained because it states the same rule from the plaintext
side and both directions matter:

> **Commitments are minted while the subject's key exists. Plaintext is never removed after the
> key that could commit to it is gone.**

### 4.1 THE CRITICAL ORDER — ruled, and it is a sequence, not a preference

```
  1. SOURCE FIX          stop all three surfaces producing plaintext
        ↓
  2. COMMITMENTS         mint AND verify, while the subject keys still exist
        ↓
  3. HISTORICAL ERASURE  remove the existing plaintext corpora
        ↓
  4. KEY DESTRUCTION     Q6's member/household erasure
```

**Every arrow is load-bearing and each inversion has a distinct failure:**

- **Erasing before committing** (3 before 2) forfeits verifiability permanently — **observed, not
  hypothetical: HA-46A retained 0 commitments for 356 entries** because the keys were already
  gone.
- **Destroying keys before committing** (4 before 2) is the same loss by the other route, and is
  the one the ratified wording names directly.
- **Committing before the source fix** (2 before 1) commits a corpus that is still growing —
  the mint is incomplete the moment it finishes.
- **Erasing before the source fix** (3 before 1) clears a backlog that immediately refills. This
  is exactly why **HA-46 was stopped at its precondition.**

**A turn whose subject key is already gone can only become metadata-only, and the count is
reported** — never repaired by minting a key after the fact, which would fabricate the context
whose absence is the finding.

**Why it is a clause and not a note:** HA-46A erased 356 recall-audit entries and could retain
**zero** commitments, because those subjects' keys had already been destroyed by an earlier
sweep. The words went and nothing verifiable replaced them. That was costless only because the
content was fixture strings.

**How it binds the 850-file migration — this is the operative part:**

1. **Mint first.** Every one of the 27,732 turns gets its commitment **before** any plaintext is
   removed and **before** any member key is destroyed.
2. **Verify before erasing.** A turn whose commitment cannot be recomputed and checked is not
   erased; it is reported.
3. **Then erase.** Only after 1 and 2.
4. **Any turn whose subject key is already gone can only become metadata-only, and the count is
   reported** — never silently accepted, and never repaired by minting a key after the fact,
   which would fabricate the context whose absence is the finding.

**The ratified build order (`REQ_ERASURE_SURFACES` §11) happens to put corpus erasure at step 2
and key lifecycle at step 4 — the safe order. This clause makes that ordering a REQUIREMENT
rather than a coincidence**, which is exactly what TD-R-189 asked for.

---

## 5. THE WINDOW IS OPEN NOW — a measurement, not a proposal

**All three transcript members still hold keys, so 100% of the corpus is committable today:**

| member | turns | key exists |
|---|---|---|
| bill | 10,556 | **yes** |
| maya | 9,096 | **yes** |
| sam | 8,080 | **yes** |
| **total** | **27,732** | **27,732 / 27,732 committable — 100%** |

**This is the opposite of HA-46A's result and it is time-sensitive.** The moment Q2's key
destruction runs against these members, the figure drops toward zero and cannot be recovered.
**§4's clause is what protects it; the migration's minting step must precede any key destruction
for bill, maya or sam.**

---

## 6. THE 850-FILE MIGRATION — PROPOSED, gated on this contract being ratified

**Nothing below runs until Bill ratifies §3.** Extent, from HA-45's map: **425 `.jsonl` + 425
`.txt` = 850 files, 27,732 turns, ~10.5 MB.**

### 6.1 The `.jsonl` corpus — 425 files, converts

Per record: **drop `text`, add `text_commitment`** (keyed to `member_id`, §3 Q3), **add `turn_id`**
if absent (Q5). Keep `ts`, `ts_mt`, `session_id`, `member_id`, `speaker`, `tier`, `tier_target` —
every field any consumer uses. **Entry count preserved; a field is removed, never a record.**
Atomic per file, dry-run first, idempotent — the shape HA-46A proved.

### 6.2 The `.txt` corpus — 425 files, ERASED not converted. **A LOSS BILL ACCEPTED ON THE RECORD**

> **RULED, Bill, 2026-08-12: the migration DELETES the 425 `.txt` files rather than converting
> them. The only human-readable rendering of past conversations is lost. Accepted deliberately.**

**Recorded as an accepted loss rather than a design detail, because that is what it is.** It is
the most destructive line in this contract, it is irreversible, and it was ruled with the
consequence stated rather than discovered during the build.

**What is lost:** every past conversation's readable form — 425 files, the full text of 27,732
turns across bill, maya and sam, spanning 2026-07-18 to 2026-08-11.

**What is not lost:** the `.jsonl` sibling keeps each turn's structured metadata and its keyed
commitment, so **nothing becomes unverifiable** — a supplied copy of any turn still checks out
while the member's key exists. **Nothing becomes readable again, though**, and no later dispatch
can undo this by finding a cleverer conversion: the words will not be on disk.

**Why deletion rather than conversion:** a `.txt` transcript's entire body *is* the words, under
a session header and `[timestamp] SPEAKER:` prefixes. Strip the words and the file is an empty
frame — no structured content, no reader, no purpose. **Conversion would produce 425 files that
exist only to look like the migration was gentler than it was.**

**Rejected alternative, and why:** sealing the `.txt` corpus instead of deleting it costs a
second sealed store with **no identified reader** — §1 establishes that nothing reads these files
— and every sealed store is custody surface that Q2/step-4 must then consolidate.

**These files have no structured content. Their entire body is the words**, plus a session header
and `[timestamp] SPEAKER:` prefixes. **A `.txt` transcript with the words removed is an empty
frame with no reader and no purpose**, so conversion is meaningless and the proposal is deletion.

**Stated plainly because it is the most destructive line in this document:** this permanently
removes the only human-readable rendering of every recorded conversation. Its commitment lives on
in the `.jsonl` sibling, so nothing becomes *unverifiable* — but nothing becomes *readable*
again either.

**Alternative:** keep the `.txt` files sealed rather than deleted. Costs a second sealed store
with no identified reader, and Q4 establishes that nothing reads them.

### 6.3 What the demo keeps seeing

**During a live session: everything, unchanged.** The band renders from the in-memory buffer
(Q4), so speaker, member, tier and words all appear exactly as today.

**After the session ends: nothing from these files.** Historical conversations stop being
viewable in the dashboard. **That is a genuine capability loss and it is the price of Q1** — it
should be ratified with eyes open, not discovered during the build.

**Unaffected either way:** DEMO-002, `test_demo_smoke`, `build_evidence_package`, and the
source-list endpoint — none reads words (§1).

### 6.4 Surfaces 20 and 21 — **IN SCOPE as of ratification**

> **SUPERSEDED 2026-08-12 by Bill's ratification (§3A).** This subsection previously read:
> *"Surfaces 20 and 21 are NOT in this migration. `turns_demo.jsonl` and `router.jsonl` (§2) need
> their own dispositions in `REQ_ERASURE_SURFACES`."* **That was HA-47's draft position and Bill
> ruled the other way**: both surfaces are in this contract's scope, the writer fix covers all
> three, and they block the acceptance equally. Old wording kept visible per the
> pre-authorized correction class.

**Their backlogs migrate with the transcripts** — build-order steps 4 and 7 cover all three
corpora, not just row 19's. They are small today (15 records / 50,100 bytes and 7 records /
2,751 bytes) but they are **live and growing**, and surface 20 is the only one of the three
carrying **both sides of the conversation** plus the routing decision beside them.

**The draft's own warning is what the ruling acted on:** migrating transcripts while
`turns_demo.jsonl` kept recording `query` and `reply` verbatim would have left the same words on
disk one file over.

---

## 6A. THE BUILD ORDER — nine steps, ruled as this contract's own sequence

**Bill's ruling, 2026-08-12.** This is the contract's sequence, not a suggested schedule.
**Nothing below is built.**

| # | step | depends on |
|---|---|---|
| **1** | **SOURCE FIX — all three surfaces stop writing words.** Transcripts (19), `turns_demo.jsonl` (20), `router.jsonl` (21). Durable records keep structured metadata + a member-keyed commitment. **All three together — §3A.** | — |
| **2** | **SESSION KEY / CUSTODY SCOPE.** Per-session content key, wrapped to each participating member's key, held in memory and never written (Q3). Sequenced with `REQ_ERASURE_SURFACES` Q2/step 4 — **shared work, not new work.** | 1 |
| **3** | **`query_hash` → keyed commitment**, or removed as an identifier (§3B). | 1 |
| **4** | **MINT AND VERIFY COMMITMENTS over the historical corpora**, while bill/maya/sam's keys still exist. All 27,732 turns plus the surface-20 and 21 backlogs. **Verify each; report any that cannot be committed.** | 1 |
| **5** | **READ PATH — `/api/transcript` stops reading files; the live band is fed from an in-memory session buffer** (Q4). **PRECONDITION: STEP 2.** | **2**, 1 |
| **6** | **CONSUMER MIGRATION — `turn_id` correlation.** Add `turn_id` to the transcript record; move the vignette off the text branch (Q5). | 1, 3 |
| **7** | **HISTORICAL ERASURE.** `.jsonl` corpora converted; **the 425 `.txt` files deleted** (§6.2); surface 20 and 21 backlogs cleared. | **4** |
| **8** | **ERASURE INTEGRATION (Q6).** Member erasure destroys the member's key material, removes their wrap, **rotates shared keys to a new epoch**; household erasure destroys the generation. **This is where key destruction happens — after step 7.** | 7, 2 |
| **9** | **EXTEND THE VERIFIER** to sweep surfaces 19, 20 and 21 and assert the ruled post-erasure state; wire it into §7's acceptance. **Last, because it verifies the other eight.** | 1–8 |

### Why step 2 is named as step 5's precondition

**Step 5 is a READ path, and a read path has to answer "for whom" before it can be correct.**
Q2 rules that words are recoverable **for the speaking member and the live session's operator,
and nobody else.** An in-memory buffer built before step 2 would have no authorization model at
all: whoever loaded the dashboard would see every member's words, because nothing would express
whose turns a given viewer may see. **Step 2's per-session key wrapped to each participating
member is precisely the mechanism that encodes Q2's answer**, and step 5 without it is a buffer
that is private only by accident of deployment.

**Note it also satisfies the critical order (§4.1):** step 1 is the source fix, step 4 the
commitments, step 7 the erasure, step 8 the key destruction — 1 → 4 → 7 → 8, in that order,
with nothing able to jump the queue.

---

## 7. ACCEPTANCE — what "done" would mean, once ratified

1. A live session renders speaker, member, tier and words in the band, with **no transcript file
   read and nothing decrypted by the dashboard.**
2. **On ALL THREE surfaces (19, 20, 21)**, every durable record carries metadata + commitment and
   **no words** — including surface 20's `reply`, not only `query` — verified through the
   supported reader **and** the raw bytes, after a **real process restart**.
   **A recovery attempt against any of the three returns nothing meaningful; a surface not
   attempted is a FAIL, not a skip.**
3. A supplied copy of a turn's text **verifies against its commitment** while the member's key
   exists.
4. After member erasure, the same check **returns false and mints no key material**, and the
   record's metadata and commitment survive.
5. **Shared/household keys still open other members' data** after a member erasure — no
   bystander loss.
6. The vignette and DEMO-002 pass **without any plaintext correlation.**
7. `0` of `27,732` turns are erased without a verified commitment, or the exceptions are counted
   and reported (§4).

**None of this is claimed. Nothing is MET.**

---

## 8. CONSTRAINTS

- **The dashboard never decrypts arbitrary transcript files.** Bill's ruling; Q4 is built to make
  it structurally impossible rather than merely disallowed.
- **No bystander's data is erased** (Q2).
- **The ERASURE-ENABLEMENT GATE holds**; nothing here authorises real-data erasure.
- **`REQ_ERASURE_SURFACES` Q3-C still governs row 19** — this contract specifies *how* to satisfy
  it, and cannot relax it.
- **Row 19 remains BLOCKING** (Q6 of that REQ) until a build lands.

---

## 9. NOTES BANKED AT HA-76 (Bill's rulings, 2026-08-14)

### 9.1 STANDING RULE — cite the table, never a paraphrase

> **Dispatches cite the contract's own table (§6A), never a paraphrase of it.**

**Why this is a rule and not a reminder.** HA-75 built the read path while calling
it *step 3*. The work was correct; the label was not. **§6A row 5 is the read
path** — *"`/api/transcript` stops reading files; the live band is fed from an
in-memory session buffer (Q4). PRECONDITION: STEP 2"* — and **§6A row 3 is
`query_hash` → keyed commitment**, which HA-75 never touched.

**ROOT CAUSE: the sequence existed in two places.** The contract's table, and a
chat-side paraphrase of it. **The paraphrase drifted, and nothing reconciled
them** — because nothing was responsible for doing so. The paraphrase was easier
to reach for and read authoritative.

**RULING (Bill, 2026-08-14): HA-75's work IS STEP 5.** The dispatch doc, its
INDEX rows and its LANES row are relabeled **by annotation, never rewritten** —
the original wording stays visible with what changed it, per the pre-authorized
correction class.

The general form: **a second copy of an ordering is a second authority, and the
copy is always the one that drifts.** Same class as the duplicated phase map
(`in_phase` vs `PHASE_STEPS`) and the duplicated checkout guard — a rule kept in
two places gets fixed in one.

### 9.2 BASELINE — `L1:P2` is IMPROVED EVIDENCE, and the baseline is UNCHANGED

> **Bill's ruling: no auto-ratchet. "Passing better once is not enough."**
> A ratchet happens only under its own explicit ruling.

**What was observed.** HA-75's `--full` run emitted:

```
IMPROVED vs baseline: ['L1:P2'] — update to lock in.
```

**What was done: nothing.** The baseline is untouched. Changing a baseline —
*including for an improvement* — is not a pre-authorized class, and the harness
printing *"update to lock in"* is a suggestion from a tool, not a ruling.

**RECORDED AS IMPROVED EVIDENCE, so a future ratchet ruling has something to
cite:**

| | |
|---|---|
| scenario | `L1:P2` — owner retrieval, Layer 1, 20 iters, seed=1 |
| observed | HA-75's `--full`, 2026-08-14, roadmap `12c1adc`, services up (7688 authenticated, Ollama 11434) |
| layer result that run | `L1: 15/15 (0 flaked, 0 skipped)` |
| binding-gate context | `BINDING TESTS PASS`; `--layer 7` RATCHET PASS separately |
| baseline action | **NONE. Unchanged.** |

**SUSPECTED CAUSE, explicitly marked as suspicion and not measurement.** No
change in HA-75 touches retrieval — it changed a transcript READ path and added
an in-memory buffer. The likeliest explanation is the same live-model variance
this lane already records: **CLAUDE.md notes HA-19 ran `--full` three times, the
last two with byte-identical code, and they disagreed on L1/L3/L4/L6 and on the
ratchet's own regression list.** A single better run of a live-model layer is
therefore weak evidence by construction, which is exactly why one improvement
does not move a baseline.

**WHAT A FUTURE RATCHET RULING WOULD NEED**, named here so the next dispatch does
not have to re-derive it: repeated runs recorded in
`logs/harness/live_layer_results.csv`, and a rule set **from that data** — not a
threshold invented to fit. Per item 12 as amended: no best-of-N, no invented
pass threshold.

**`L2:routing_showcase.T04` was LEFT ALONE** — reported non-gating, unrelated to
this work (a model answering a time query when asked about cable-industry
consolidation), and **not chased**.

### 9.3 ONE AUTHORITATIVE CONVERSATION-STATE OWNER

> **Bill's rule, VERBATIM:**
>
> **"One conversation has one authoritative ephemeral conversation-state owner,
> independent of ingress modality or worker process."**

Text and voice **may hold local caches**. The authoritative session/episode state
— **including the transcript/audit band used for conversational continuity** — is
**shared through the conversation-state owner**. It is **not reconstructed by
reading files**, and **not independently accumulated per process**.

**FOR HA-75 SPECIFICALLY, all four, recorded together:**

1. **The in-process buffer is ACCEPTED for this step.** It satisfies Q4 as ruled
   and is the correct thing to have built.
2. **The multi-process limitation is RECORDED EXPLICITLY.** The buffer is
   per-process: today the dashboard runs `process_text_query` in-process so the
   supported demo path is covered, but a separate voice-service process would
   populate its own buffer, not the dashboard's — where the file reader used to
   merge both. This is a real gap, not a footnote.
3. **FILE MERGING IS NEVER THE SOLUTION.** Restoring a file-merge to paper over
   (2) would undo Q4 and reintroduce the plaintext read this whole row exists to
   remove. It is excluded permanently, not deferred.
4. **Shared, process-independent conversation state is a PREREQUISITE** before
   voice and text may participate in the same Conversation Episode. Until it
   exists, the two modalities do not share an episode — and must not pretend to.

**CROSS-REFERENCES — and one correction about what exists.**

The dispatch asked for this to be cross-referenced to *"the NC REQs"*. **There are
no NC REQs.** The natural-conversation work is a DESIGN doc:
`docs/design/HIP_DESIGN__dual-model-natural-conversation-v2__v20260813_1500.md`,
whose own status line reads **"ADOPTED DIRECTION (research lane; no requirement
filed)"** (banked HA-66, `4a7b82f`). Recorded rather than papered over, because a
rule cross-referenced to a document that does not exist is unenforceable, and a
later reader would go looking.

* **NC design v2 §2, "Three components"** — Conversation Model (no authority, no
  memory authority), **HIP Kernel** (deterministic; identity/tier, authorization,
  memory admission, audit, disclosure boundary — *"Unchanged from the governed
  text path"*), Reasoning Model. **This is the document 9.4(i) argues from**: the
  kernel is already the component that must be single across modalities.
* **NC design v2 §5, M3** — *"asynchronous HIP bridge (candidate request → kernel
  → AuthorizedResponseEnvelope) … First intersection with the conversation-memory
  track"* — the milestone at which point 4 above (shared state as a prerequisite)
  becomes load-bearing rather than anticipatory.
* `REQ_ERASURE_SURFACES` **Q3-C** — row-19 governance, which this contract
  implements and cannot relax.
* This contract's **Q1–Q3** — session key, custody scope, memory-only key
  material; the properties 9.4(ii) proposes the state owner must inherit.

**When an NC REQ is filed, this rule belongs in it** — pointing at a design doc is
the best available anchor today, not the right long-term home.

---

### 9.4 PROPOSED — two sharpeners (Claude's, **BILL TO CONFIRM OR STRIKE**)

**These are PROPOSALS, not rulings, and are marked so deliberately.** Neither is
in force. A later document citing 9.4 must check whether it was confirmed.

**(i) The authoritative owner is the GOVERNED-TURN KERNEL's process boundary.**
Ingress adapters — the dashboard, the voice service — are **CLIENTS** of it,
not peers holding their own authoritative state.

**A standalone conversation-state service is NOT the default answer.** Two
processes each embedding governance, plus a third service holding state, is
**three brains — the same disease one layer down.** The kernel that already
decides governed turns is the thing that should own the conversation's
authoritative state, because it is already the thing that must be single.

**(ii) Wherever the authoritative state lives, it INHERITS Q1–Q3's properties.**
Memory-only; keyed recoverability; dies with the session; **never persisted,
never swapped, never exported.**

**So that conversation state can never become erasure surface #22.** The row-19
work removes a durable plaintext surface; introducing a shared state owner
without these properties would create a new one with a different name, and the
inventory would be wrong again — this time about a component built *by* the
erasure work.
