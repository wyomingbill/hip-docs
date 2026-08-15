# DISPATCH_HA75 — row-19 ~~step 3~~ **STEP 5**: the live transcript band off files, onto memory

> **RELABELED BY HA-76 (Bill's ruling, 2026-08-14): THIS WORK IS STEP 5.**
> Labeled step 3 by the dispatch in error; **the contract's own table governs**, and
> this row is **step 5** (contract step 3 = `query_hash` → keyed commitment).
> The original wording is struck through rather than replaced, per the
> pre-authorized correction class: annotate the correction, never silently patch.
Status: BUILT
Reconciled-Against: `roadmap` @ HEAD of this dispatch's commit

**TYPE:** BUILD

**REQ:** `docs/requirements/LATEST_REQ_TRANSCRIPT_STORAGE.md`
(`REQ_TRANSCRIPT_STORAGE__row19-storage-contract-six-dispositions-and-the-850-file-migration__v20260812_0948.md`)
— Q1–Q6 RULED at HA-48; the nine-step row-19 order is the contract's own sequence.

**SCOPE:** the read path only (Q4). Writers untouched. Steps beyond this one are
not this dispatch.

---

## 0. A NUMBERING DISCREPANCY — **RULED AT HA-76: THIS IS STEP 5**

> **BILL'S RULING (2026-08-14, banked by HA-76). THE CONTRACT IS THE AUTHORITY.**
>
> **HA-75's work IS STEP 5 of the nine-step contract, not step 3.** It was labeled
> step 3 by the dispatch in error. The contract's own table governs; contract
> **step 3 is `query_hash` → keyed commitment**, which HA-75 did not touch.
>
> **ROOT CAUSE, recorded so the class is visible and not just this instance:** the
> sequence existed in TWO PLACES — the contract's own table, and a chat-side
> paraphrase of it — **and the paraphrase drifted.** Nothing reconciled them,
> because nothing was responsible for doing so: the paraphrase was easier to
> reach for and read authoritative.
>
> **STANDING RULE, recorded into the REQ's notes:** *dispatches cite the
> contract's own table, never a paraphrase of it.*
>
> The section below is HA-75's own contemporaneous analysis and is LEFT AS
> WRITTEN. It reached the right answer from the right evidence — it identified
> the discrepancy, verified step 5's precondition, and flagged it for Bill rather
> than renumbering by itself. What it could not do was rule; that is what this
> annotation supplies.

### HA-75's contemporaneous analysis (unaltered)

The dispatch calls this **step 3**. The contract's own nine-step table
(`§ the ordered table`, rows 1–9) numbers the work differently:

| | contract's table |
|---|---|
| **step 3** | `query_hash` → keyed commitment, or removed as an identifier (§3B) |
| **step 5** | **READ PATH — `/api/transcript` stops reading files; the live band is fed from an in-memory session buffer** (Q4). **PRECONDITION: STEP 2** |

The work this dispatch DESCRIBES — "replace the live transcript path, Q4",
"/api/transcript stops reading transcript FILES entirely" — is unambiguously the
contract's **step 5** row, quoted almost verbatim.

**This was resolved rather than assumed**, because the two readings differ in
what must already exist:

* **The precondition is satisfied.** Step 5 requires step 2 (the per-session
  content key). `harness/session_content_key.py` exists with a 30-test battery
  hardened at HA-49A, and it passes 30/30 here. So the read path is not being
  built ahead of its dependency under either numbering.
* **The dispatch's own question is answered by the contract.** It asked whether
  `session_content_key` "wires here or at step 5". `session_content_key.py`'s
  closing line reads: *"Process-wide registry. **Step 5 is what will populate
  it.**"* — this step. What it wires is the **session lifecycle**, not
  encryption of the buffer; see §2.

**Recorded, not silently adopted:** the dispatch's step numbers and the
contract's table disagree by two for this row, and a future dispatch citing
"step 5" will mean the erasure work under one reading and this work under the
other. Flagged for Bill rather than renumbered by a session.

> **RESOLVED, HA-76:** ruled in favour of the contract's table. This row is
> **step 5**; the ambiguity the paragraph above anticipated is closed, and a
> future dispatch citing "step 5" means THIS work.

## 1. PART A — THE PRE-WIRING GATE

HA-49A's external review listed nine cross-binding twins. **All nine are already
standing in the 30-test battery. None are owed, so nothing was built here.**

| # | review's twin | standing test | |
|---|---|---|---|
| 1 | cross-session ciphertext rejected | `test_ciphertext_from_another_session_is_rejected` | STANDING |
| 2 | cross-turn ciphertext rejected | `test_ciphertext_reattributed_to_another_turn_is_rejected` | STANDING |
| 3 | cross-member ciphertext rejected | `test_ciphertext_reattributed_to_another_member_is_rejected` | STANDING |
| 4 | wrap copied to another session rejected | `test_a_wrap_copied_to_another_session_is_rejected` | STANDING |
| 5 | one member cannot substitute another's wrap | `test_one_member_cannot_substitute_anothers_wrap` | STANDING |
| 6 | restart cannot recover prior-session words | `test_restart_cannot_recover_prior_session_words` | STANDING |
| 7 | `end()` idempotent | `test_end_is_idempotent_and_kills_everything` | STANDING |
| 8 | missing ledger key at verify FAILS, never recreates | `test_a_missing_member_ledger_key_FAILS_and_never_recreates_it` | STANDING |
| 9 | tampered metadata fails, ciphertext untouched | `test_tampered_metadata_fails_with_the_ciphertext_untouched` | STANDING |

**Verified by running, not by reading names:** 30/30 pass. Two were spot-read for
anti-vacuity and both carry a positive control — #1 ends with
`assert a.open_as(env, ...) == WORDS`, and #8 asserts the keys directory is still
empty afterwards (`"verification minted key material"`). The battery's own
docstring states the pairing as a rule.

**Nothing owed ⇒ nothing built.** Per the dispatch: owed cross-binding twins land
now, anything larger is filed not built.

## 2. PART B — THE BUILD

**`harness/session_transcript_buffer.py` (new).** A session-scoped, in-memory
turn buffer. Q4's construction, verbatim in the module docstring.

**`server/demo_dashboard.py::api_transcript` — the reader.** Previously globbed
`logs/transcript/*.jsonl` and parsed every session's records. Now:

```python
from harness.session_transcript_buffer import records as buffered_turns
return JSONResponse(buffered_turns(since=since, n=n))
```

No file is opened. Deliberately **not** pointed at `/api/turns` — Q4 names that
as the obvious shortcut that looks like a fix and solves nothing, because that
surface is itself plaintext.

**The tap.** `harness/transcript_log.write_transcript_turn` gains one call that
hands the **same record** to the buffer. This is a tap, not a change of writer:
nothing below it is altered and the durable bytes are identical (C4). Feeding the
buffer from the same record is what stops the band drifting from the transcript.

**Session lifecycle, and what is NOT wired.** `SessionKeyRegistry.end()` now also
discards the session's buffer, so Q4's *"discarded when the session ends"* is
structural rather than a second thing to remember. **The buffer is NOT sealed
with the session content key** — Q4's whole construction is that the band's words
live only in this process's memory, so *"there is nothing to decrypt"*.
Encrypting a buffer this process would immediately decrypt adds a key-handling
surface and removes nothing.

**The buffer holds plaintext, and that is the ruled answer, not a gap.** Stated
plainly in the module docstring so nobody re-derives it as a defect.

## 3. PART C — ACCEPTANCE

| | claim | result |
|---|---|---|
| **C1** | LIVE: band renders speaker/member/tier/text from the buffer; **not empty** | **PASS** — 4 turns, both members, both speakers, both tiers; ordering and `since` filtering preserved |
| **C2** | STRUCTURAL: reader has no file-read path, by AST, never a regex | **PASS** — 5 tests |
| **C3** | POST-SESSION: the words cannot be recovered through this reader | **PASS** — 3 tests |
| **C4** | WRITERS UNCHANGED: durable surfaces still written byte-identically | **PASS** — 3 tests |
| **C5** | Baseline preserved | **see §4** |

**C2 is proved structurally, as instructed.** The endpoint's AST is walked for
filesystem calls (`open`, `read_text`, `glob`, `iterdir`, …) and for imports of
`pathlib`/`os`/`io`/`glob` or `transcript_log`; the buffer module is scanned the
same way, so the file read cannot simply have moved. A source regex was
explicitly not used: it would pass on a comment saying "no file read" and fail on
the word "open" in a docstring, and neither is the property under test.

**The C2 twin goes RED both ways.** A planted file-reading function is detected
by the scan, AND — the stronger check — reintroducing a real file read into the
actual endpoint turns 2 of the C2 tests red. Restored, all 13 pass.

## 4. C5 — BASELINE

**Preflight (CLAUDE.md, mandatory, four-state):** Neo4j `bolt://localhost:7688`
`java` listening, `NEO4J_PASSWORD` present in the operator environment,
authenticated trivial read returned ⇒ **GRAPH USABLE**. `HIP_REGISTRY_DB` =
`~/hip-roadmap/data/registry.db` — lane-local, not a shared registry.
Ollama up on 11434.

**Binding gate:**

| command | result |
|---|---|
| whole suite (`pytest -q --import-mode=importlib`) | **31 failed / 1300 passed**, services up |
| `eval.harness --layer 7` | **RATCHET PASS** — no scenario regressed |
| `eval.harness --full` | **BINDING TESTS PASS.** Ratchet line reads `RATCHET FAIL — regressed vs baseline: ['L2:routing_showcase.T04']` — a LIVE layer, see below |
| `eval.memory_harness` | **13/17 — inside the 13–15 pin** |

**The differential, like-for-like, same command, same service state:**

```
BEFORE (my changes stashed):  31 failed, 1287 passed, 10 skipped, 9 xfailed, 2 errors
AFTER:                        31 failed, 1300 passed, 10 skipped, 9 xfailed, 2 errors
```

**+13 passed, exactly this dispatch's new suite. Zero new failures** (set
difference of the FAILED lines is empty).

**The 2 collection errors are pre-existing and neither is mine:**
`tests/test_routing.py` is CLAUDE.md's documented standing known-bad
(`_classify_freshness`), and `scripts/test_groq_factchange.py` is a script that
makes a live Groq call at import time and is collected only because of its name.
Both are unmodified at HEAD.

**Memory harness 13/17 is unchanged by this dispatch** — MEM-115/116/117/118 fail
identically with my changes stashed. 13/17 is *inside* the pin; per CLAUDE.md
16/17 would be a STOP, and this is not that.

**THE `--full` RESULT, STATED EXACTLY.** The harness's own verdict block:

```
BINDING TESTS PASS. LIVE-MODEL TESTS HAVE FAILURES — SEE RUN LOG.
  live-layer regressions: ['L2:routing_showcase.T04']
  live-layer new failures: none
  (Reported, not gating — Requirements Discipline item 12, amended 2026-08-09.)
```

Binding layers, all green: **AUDIT 9/9, DISC 1/1, L7 27/27, L7V2 27/28 (1 skipped),
SCHEMA 1/1, VOICE 1/1.**

`L2:routing_showcase.T04` is a live-model scenario and is **reported, not gated**,
per Bill's HA-20 amendment. Its failure is a plain model misfire, visible in the
reply itself: asked *"What's the latest news on cable industry consolidation?"* it
answered *"It's 7:05 AM PDT in La on Friday, August 14."* — a different question
entirely, with `tier` escalating instead of edge. **Nothing in this dispatch
touches routing, tiering or reply generation**; the read path it changes is the
transcript band. CLAUDE.md already records that this lane's ratchet regression
list is not reproducible across identical code (HA-19 ran `--full` three times;
the last two had byte-identical code and disagreed on L1/L3/L4/L6 and on the
regression list itself).

**It was NOT re-run to chase a green.** Best-of-N is explicitly forbidden, and a
re-run until green would be exactly that.

**`IMPROVED vs baseline: ['L1:P2'] — update to lock in.`** Not done: changing a
baseline is not a pre-authorized class, including for improvements. Flagged for
Bill.

**One failure WAS mine and is fixed:**
`test_every_battery_file_is_listed_or_explicitly_exempt` went red because the new
battery existed without being in `scripts/run_harness.sh`'s standing list — the
lane's own rule that a battery which never runs is worthless. Registered; 14/14.

## 5. WHAT THIS STEP COSTS, RECORDED SO IT IS NOT REDISCOVERED AS A BUG

Q4's own alternatives table already accepts two:

* historical sessions are no longer viewable in the dashboard;
* a server restart mid-session loses the band's backlog.

**And one this step adds, which is NOT in that table:** the buffer is **per
process**. Today the dashboard runs `process_text_query` in-process, so the
supported demo path is covered — but a separate voice-service process would
populate its own buffer, not the dashboard's, where the file reader used to merge
both. Recorded here and in the module docstring for the later steps rather than
found later.

## 6. VERIFIED

**Watched run:** the 30-test binding battery (30/30); `eval/test_transcript_band_off_files.py`
(13/13); the C2 mutation check in both directions; the whole-suite BEFORE/AFTER
differential with the stash; `--layer 7`; the memory harness with and without my
changes; the four-state preflight.

**Reasoned about:** that the buffer's per-process scope is acceptable for THIS
step — argued from the dashboard calling `process_text_query` in-process
(`server/demo_dashboard.py:2268`) plus DEMO-002 driving the band through that
path, not from observing a live voice session feed the band. If a voice-service
process is expected to feed this band, that is a step-5/6 wiring question and is
named above rather than assumed away.

## 7. OPEN

- **The step-numbering discrepancy** (§0) — Bill's to reconcile.
- **The per-process buffer scope** (§5) for the later read-path work.
- `eval/harness.py` shadows the `harness` package on this lane too, so
  `--import-mode=importlib` is mandatory here; the `pytest.ini` fix that closed
  this on `hip-vo@main` (TD-V-019) is branch-local and has not been ported.
  Filed, not built — the Finiteness Rule: it does not block this phase's
  acceptance criteria.
