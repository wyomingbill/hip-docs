COMPLETE WITH FINDINGS — 1 ITEM FILED, NOTHING BLOCKING

# DISPATCH_HA47_TRANSCRIPT_STORAGE_CONTRACT — the contract drafted, and the shortcut that would have relocated the problem
Status: BUILT (docs + read-only — no writer change, no corpus touch, no consumer change)
Reconciled-Against: roadmap `3cf9619` (HA-46A) at start; landed this dispatch

**Dispatch ID: HA-47.** Authority: Bill's ruling 2026-08-11 — row 19 needs a storage contract
before any build, and **the dashboard never decrypts arbitrary transcript files.**

**The contract:**
`docs/requirements/REQ_TRANSCRIPT_STORAGE__row19-storage-contract-six-dispositions-and-the-850-file-migration__v20260812_0948.md`

**Nothing is ruled.** Six PROPOSED dispositions, each with alternatives and costs.

---

## 1. WHAT THE CONSUMERS ACTUALLY USE — item 1, read-only with evidence

**Of six consumers of `logs/transcript/`, exactly ONE needs the words — and only the current
session's.**

### `/api/transcript` → `TurnBubble`

The endpoint returns the whole record: `ts`, `ts_mt`, `session_id`, `member_id`, `speaker`,
`text`, `tier`, `tier_target`. **The renderer uses four fields**
(`server/static/demo.html:502`–`:531`):

| field | what it draws |
|---|---|
| `speaker` | bubble side, `HIP` label |
| `member_id` | speaker name and colour |
| `tier` | the `[tier]` tag on user turns |
| **`text`** | **bubble contents — the only member-content field rendered** |

`ts` filters `?since=` and sorts; never displayed. **Everything else the API returns is unused.**

### The consent vignette — its 40-character correlation, precisely

```python
transcript_escalate = any(
    r.get("speaker") == "user" and r.get("tier") == "escalate"
    and t2_query[:40] in (r.get("text") or "")
    for r in transcript)
...
ok = response_ok and (transcript_escalate or new_escalate)
```

**The prefix distinguishes exactly one thing: WHICH record is turn 2's user turn.** It is an
identity match. The assertion is `tier == "escalate"`; the text is only how the row is found.

**And it is one branch of an OR whose other branch already needs no plaintext** — `new_escalate`
correlates via `logs/router.jsonl`'s `query_hash`. **Dropping the text branch loses no coverage.**

### Third consumer found — `integration_harness.py` DEMO-002 — unaffected

Asserts maya and sam each appear with both speaker labels; uses `member_id` and `speaker` only.

### Confirmed to need no words

`test_demo_smoke.py` (`member_id`/`speaker`/`ts`/mtimes), `build_evidence_package.py` (metadata),
the dashboard source-list endpoint (filenames).

---

## 2. THE FINDING — the obvious fix would have relocated the problem, not solved it

**Filed TD-R-190.** Two plaintext surfaces exist that are **in no inventory**, and **no erasure
module reaches either** (zero references across `graph_erasure.py`, `erasure_request.py`,
`erasure_report.py`, `ledger_payload_store.py`):

| # | surface | content | extent |
|---|---|---|---|
| **20** | **`logs/turns_demo.jsonl`** | **`query` AND `reply` verbatim** + `member` + ~35 routing fields | 15 records, 50,100 bytes, members bill/maya/sam |
| **21** | **`logs/router.jsonl`** | **`query` verbatim** + `query_hash` | 7 records, 2,751 bytes |

### Why this is the important part of the dispatch

**HA-45 offered "point the dashboard at the live `/api/turns` feed" as a serious option for
row 19.** It would have worked perfectly — the client already maps that feed into the identical
render shape (`d1ToTranscriptTurns`, `demo.html:548`), same `TurnBubble`, no visible difference.

**`/api/turns` reads `logs/turns_demo.jsonl`.** The dashboard would have stopped reading *the*
plaintext file and started reading *a different* plaintext file — one that also carries HIP's
replies, which transcripts and the recall audit do not.

**The failure mode is that it looks exactly like a fix.** Row 19 would have been reported closed
while the same words sat on disk one file over, on a surface no inventory names and no erasure
path touches. **This is the concrete reason Q4's disposition is "read no file at all."**

### A second defect inside the same finding

`query_hash` is `hashlib.sha256(query.encode()).hexdigest()[:16]` —
**bare, unkeyed, truncated.** Plaintext-free but **dictionary-testable**: short natural-language
queries fall to enumeration. It is R16's exact prohibition and the same property that makes
HEL 1.0 non-opaque. It matters *now* because it is the vignette's existing plaintext-free path,
so **a design that leans on it would make a weak digest newly load-bearing.** Q5 proposes a keyed
commitment instead — retiring the defect rather than entrenching it.

### And the inventory blind spot has now repeated

HA-41 stated correctly that *"no erasure module references `logs/` at all"* but enumerated only
the log files it had found. **A surface no erasure module mentions cannot be found by reading
erasure modules.** That produced TD-R-188 (transcripts) and has now produced TD-R-190.
**"Nineteen surfaces" should be read as nineteen ENUMERATED, not nineteen EXISTING** — which is
why `REQ_ERASURE_SURFACES`'s no-UNKNOWN gate was written as standing rather than one-time.

---

## 3. THE SIX DISPOSITIONS — all PROPOSED

| Q | proposed |
|---|---|
| **Q1 — what stays recoverable** | **Words only while the session is live.** Durable records keep structured metadata + a keyed commitment, never words. No consumer reads historical words. |
| **Q2 — for whom** | **The speaking member, and the live session's operator while it runs.** A file holder gets metadata and a commitment, never words. |
| **Q3 — key/custody scope** | **Per-session content key, wrapped to each participating member's key**, held in memory only; the durable per-turn commitment is keyed to the speaking member (HA-45's precedent). Per-turn keys would hit TD-R-172's key explosion; per-member gives erasure granularity coarser than Q6 needs. **This is Q2/step-4 custody work and must be sequenced with it.** |
| **Q4 — how `/api/transcript` reads it** | **It doesn't. It stops reading transcript files entirely**; the band is fed from an in-memory session buffer. Bill's "never decrypts" constraint becomes structural rather than a rule — there is nothing to decrypt and no file is read. **Explicitly NOT by switching to `/api/turns`** (§2). |
| **Q5 — vignette correlation** | **Correlate on `turn_id`**, with a keyed-commitment match as fallback; **and `query_hash` should become a keyed commitment.** No coverage is lost — the OR's other branch already passes. |
| **Q6 — erasure** | **Member:** destroy the member's key material; **shared/household keys are never destroyed — remove the member's wrap and rotate to a new epoch** (Q2). **Household:** destroy the household generation and its member keys; no rotation needed. **Both: records are not deleted** — a field goes opaque, entry counts preserved, the HA-46A shape. |

Each carries its alternatives and their costs in the REQ; the ones ruled out are listed too,
including the option Bill's own constraint eliminates.

---

## 4. THE TD-R-189 ORDERING CLAUSE — and the window is open now

Written into the contract as a binding clause, not a note:

> **Commitments are minted while the subject's key exists. Plaintext is never removed after the
> key that could commit to it is gone.**

**How it binds the migration:** mint commitments for all 27,732 turns **first**; **verify** each
before erasing; **then** erase; and any turn whose subject key is already gone becomes
metadata-only **with the count reported**, never repaired by minting a key after the fact.

**The measurement that makes this urgent — and it is the opposite of HA-46A's result:**

| member | turns | key exists |
|---|---|---|
| bill | 10,556 | **yes** |
| maya | 9,096 | **yes** |
| sam | 8,080 | **yes** |
| **total** | **27,732** | **100% committable TODAY** |

**HA-46A retained zero commitments because its subjects' keys were already gone. Row 19's are
not — yet.** The window closes the moment Q2's key destruction runs against these three members.
**The clause exists to keep the migration's minting step ahead of it.** The ratified build order
already happens to sequence them safely; this clause makes that a requirement rather than a
coincidence, which is what TD-R-189 asked for.

---

## 5. THE 850-FILE MIGRATION — PROPOSED, gated on ratification

- **`.jsonl`, 425 files, 27,732 turns — CONVERTS.** Drop `text`, add `text_commitment` (keyed to
  `member_id`), add `turn_id` where absent. Keep every field a consumer uses. Entry count
  preserved. Atomic, dry-run first, idempotent — HA-46A's proven shape.
- **`.txt`, 425 files — ERASED, not converted.** Their entire body *is* the words, plus a header
  and speaker prefixes. **A `.txt` with the words removed is an empty frame with no reader.**
  Stated plainly because it is the most destructive line in the contract: this permanently
  removes the only human-readable rendering of every recorded conversation. The commitment
  survives in the `.jsonl` sibling, so nothing becomes unverifiable — but nothing becomes
  readable again either.
- **What the demo keeps seeing:** during a live session, everything, unchanged — speaker, member,
  tier, words, from the in-memory buffer. **After the session ends, nothing from these files.**
  Historical conversations stop being viewable in the dashboard. **A genuine capability loss,
  named so it is ratified with eyes open rather than discovered mid-build.**
- **Surfaces 20 and 21 are NOT in this migration** and need their own dispositions — migrating
  transcripts while `turns_demo.jsonl` keeps recording `query` and `reply` verbatim would leave
  the same words on disk one file over.

---

## 6. WHAT DID NOT HAPPEN

- **No writer changed, no corpus touched, no consumer changed.** Read-only throughout.
- **Nothing ruled.** Six dispositions, all PROPOSED; no REQ is MET.
- **No harness run**, and none was called for: no code changed. Working tree carries only the new
  contract, the dispatch doc, the register entry and the INDEX/handoff rows.
- **Row 19 remains BLOCKING**, and its writer still produces plaintext.
- **The erasure-enablement gate is untouched.**

---

## CLAIM IMPACT

**none.** C-09 is what this bears on; **a contract is not a run**, and two more plaintext surfaces
were found than were known yesterday.

---

## RECAP

**HA-47** — drafted `REQ_TRANSCRIPT_STORAGE`: six PROPOSED dispositions with alternatives, the
TD-R-189 ordering rule as a binding clause, and the 850-file migration shape. **Established
read-only that of six consumers only ONE needs words — the live band, current session only — and
that the vignette's 40-char prefix is a redundant identity match whose OR-branch already works
without plaintext.** **FOUND AND FILED TD-R-190: `turns_demo.jsonl` (query AND reply verbatim)
and `router.jsonl` (query verbatim) are plaintext surfaces in no inventory, reached by no erasure
module — and HA-45's "switch to the live feed" option would have relocated the dashboard's
dependency onto one of them while looking exactly like a fix.** Also flagged `query_hash` as a
bare truncated SHA-256. **100% of the 27,732 turns are committable today; that window closes when
Q2 destroys bill/maya/sam's keys.** Nothing ruled.
