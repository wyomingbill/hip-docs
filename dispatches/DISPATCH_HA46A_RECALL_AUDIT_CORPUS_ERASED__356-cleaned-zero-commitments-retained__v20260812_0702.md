COMPLETE WITH FINDINGS — 1 ITEM FILED, NOTHING BLOCKING

# DISPATCH_HA46A_RECALL_AUDIT_CORPUS_ERASED — 356 legacy entries cleaned, and not one commitment could be kept
Status: BUILT
Reconciled-Against: roadmap `eb97267` (HA-45) at start; landed this dispatch

**Dispatch ID: HA-46A.** Authority: Bill's split ruling, 2026-08-11. Row 7 only.

**All 356 legacy plaintext entries are erased. Restart-proved through both the supported reader
and the raw bytes on disk. Row 19 and the 850 transcript files are untouched — verified, not
asserted.**

**THE HEADLINE FINDING: ZERO commitments could be retained. All 356 are metadata-only** — and
the reason is not a defect in this build. §3.

---

## 1. WHAT WAS DONE

| | before | after |
|---|---|---|
| entries | **360** | **360** — a field was removed, never a record |
| carrying query text | **356** | **0** |
| carrying a commitment | 4 | 4 |
| bytes on disk | 119,259 | **101,896** |

**Dispositions, per entry:**

| disposition | count |
|---|---|
| **metadata-only** (no key context — no commitment invented) | **356** |
| **commitment retained** | **0** |
| already compliant (HA-45-era, untouched) | 4 |
| malformed / skipped | 0 |

Governed record: `logs/memory_engine/recall_audit_erasure_report__v20260812_0700.json`,
erasure id `75f98d19-c8de-4e58-b37c-038fde5822af`.

**The report names no subject, no attribute and no content** — it carries an opaque erasure id
and counts. That is Q5's shape applied to this operation's own record, and it is asserted by a
test rather than left to review.

---

## 2. THE MECHANISM

New module `harness/recall_audit_erasure.py`, with `eval/test_recall_audit_erasure.py`
(11 tests) registered in `scripts/run_harness.sh`.

**Atomic.** The cleaned file is written to a temp file in the same directory, fsynced, then
`os.replace`d over the original. Until that rename the original is intact, so a crash mid-run
cannot leave a half-erased log. Verified: no `*.cleaning-*` residue remains.

**No backup copy was made, deliberately.** A backup of a plaintext corpus relocates the plaintext
rather than erasing it, which is the exact failure this build exists to end. Atomicity provides
the safety a backup would have, without the second copy.

**Dry-run is the default.** `apply=False` performs identical analysis and writes nothing; a
destructive default is how a survey becomes an incident. The dry run was executed first and its
counts matched the applied run exactly.

**Idempotent.** Re-running changes nothing — asserted by a test, because a cleaner that degraded
the file on re-run would be unsafe to retry after a crash.

**Key access is READ-ONLY.** `_read_member_key` reads the key path directly and returns None when
absent. `_load_or_create_member_key` is never called — it would **create** a key, which for an
erased subject means resurrecting key material and then computing a commitment against a
freshly-minted key that proves nothing. The same trap HA-45 avoided in the verify path.

---

## 3. THE FINDING — zero commitments, and why

**Not one of the 356 entries could keep a verifiable commitment.**

- The 356 entries name **261 distinct subjects.**
- **0 of those 261 have a key file.** The key store is present and healthy — `ledger/keys/` holds
  **1,089** member keys — so this is not a misconfigured lookup; those particular keys are gone.
- Every one of the 261 is an **ephemeral harness-fixture subject** (`memtest-*`, `_e_verify_*`,
  `_snd_*`, `_probe_*`), and their keys were destroyed by the test-key hygiene sweep — the
  1,390-key sweep HA-14 built and ran.

**So the "retain a commitment where key context exists" clause was moot for this corpus, and the
instruction's other branch — *do not invent one* — is the branch that applied to all 356.** No
key was created and no commitment was fabricated.

### The consequence, stated plainly

HA-46's original framing wanted *"a keyed commitment per removed entry so a later-supplied copy
can still be verified."* **For this corpus that property is now unobtainable, permanently.** The
words are gone and there is no commitment to check a supplied copy against. The alternative would
have been to mint 261 keys purely to manufacture commitments — which would have been fabricated
context, forbidden by item 1, and worthless besides: a commitment under a key created after the
fact proves nothing about what was recorded at the time.

**This costs nothing real here** — the erased queries are six distinct harness fixture strings,
not member content — **but it would matter for a production corpus**, and the shape of the
problem is general: *a commitment can only be retained if the subject's key outlives the
plaintext.* Filed as **TD-R-189** so the ordering constraint is on the record before build 2
touches transcripts, where the same question will arise against real member sessions.

---

## 4. THE PROOF — after restart, both checks executed

Run in a **fresh Python process** after the erasure, not inferred from the writing process.

**Check A — the supported reader** (`memory_engine.recall.read_recall_audit`):

```
360 entries returned
text-bearing keys present : 0
values containing a query : 0
```

**Check B — the raw bytes on disk:**

```
101,896 bytes
query strings found  : 0 of 6
`"query":` key present : False
```

**Anti-vacuity, in the same run:** all 360 entries are still present, each carrying its
operational metadata (`ts`, `subject`, `requester`, `reason`, `cold_fact_ids_fetched`,
`allowed_fact_ids`, `denied_count`), and the 4 HA-45-era commitments survive intact. **Without
this half, an empty file would have passed both checks above.**

**On the six needles:** the check searched for the actual distinct query strings, so it is a
direct search rather than a schema inference. Those strings were held only for the duration of
the check and the list was deleted immediately after. They are harness fixture strings already
present in tracked source (`eval/test_key_hygiene.py`, `eval/memory_harness.py`), so holding them
briefly created no exposure that did not already exist.

### Durability check, unplanned but worth recording

The three verification commands then ran the full harness, which **wrote four new audit entries
through the live path.** Re-read afterwards: **364 entries, zero `query` keys, 8 commitments.**
The corpus stays clean under real traffic, and the new entries commit rather than transcribe.

---

## 5. FAULT TWIN — planted, cleaned, verified gone both ways, restored

`test_fault_twin_planted_plaintext_is_gone_both_ways` plants a distinctive scratch entry
(*"does dad still take metoprolol twice a day"*) in a scratch corpus, asserts it is present, runs
**the same code path**, then verifies:

- **(a) supported reader** — no text-bearing key on the entry;
- **(b) raw bytes** — neither the full string nor the tokens `metoprolol`, `twice a day`,
  `dad still` survive;
- **anti-vacuity** — the entry is still there, with `reason` and `denied_count` intact.

State restored: the twin runs entirely in `tmp_path` and never touches the real corpus.

The battery's other twins cover both directions of the commitment rule — **no commitment invented
when the key is absent** (and the key is only ever looked up, never created) and **a real,
verifiable commitment retained when a key exists** — because "no commitment" alone would be
unfalsifiable.

---

## 6. WHAT WAS NOT TOUCHED — verified

| | before | after |
|---|---|---|
| `logs/transcript/*.jsonl` | 425 files, 27,732 lines, 7,390,396 bytes | **identical** |
| `logs/transcript/*.txt` | 425 files | **identical** |

**Row 19 and the 850 transcript files are exactly as they were.** No other surface was touched:
`encode_audit.jsonl`, `consolidation_report.jsonl` and `must_confirm_queue.jsonl` are untouched,
and no graph, ledger or key operation ran.

**Row 19's write path still produces plaintext** — that is HA-45's open STOP, unchanged by this
dispatch, and the phase still cannot complete without it.

---

## 7. RUNS

Repo `.env.dev` sourced (`NEO4J_URI=bolt://localhost:7688`), never `~/.env.dev`.

| command | result |
|---|---|
| **Standing binding battery**, 57 files | **1179 passed / 0 failed / 9 xfailed** — was 1168/56; **+11 is exactly this dispatch's battery** |
| **`--layer 7`** | **EXIT 0.** L7 **27/27**, L7V2 **27/28** (1 skipped), AUDIT **9/9**, DISC 1/1, SCHEMA 1/1, VOICE 1/1 |
| **RATCHET** | **PASS — no scenario regressed vs baseline** |
| **Memory harness** | **13/17** — inside the 13–15 pin. Not 16/17, so no STOP |

**No deterministic regression.** No live reds to report: `--full` was not run, since this dispatch
changed no live path and asked for no collector run.

---

## 8. FILED — TD-R-189

**A commitment can only be retained if the subject's key outlives the plaintext.** Erasing a
plaintext corpus *after* its subjects' keys are gone forfeits the verifiability that committing
was supposed to buy. Observed here at 356/356. Harmless in this instance (fixture queries), but
it is an **ordering constraint on build 2**, where transcripts belong to real member sessions and
the same key-lifetime question decides whether their commitments are worth anything.

**Filed, not fixed** — it blocks nothing in this dispatch's acceptance, and the fix is a
sequencing decision about build 2 and Q2/step 4, which is Bill's.

---

## CLAIM IMPACT

**none.**

C-09 (*"Erasure leaves no readable trace that the claim existed"*) is what this bears on. One of
two ruled plaintext surfaces is now clear of its legacy corpus — **but the other still holds
27,732 turns and its writer is still producing more**, so the claim gains nothing. Status is
computed from standing runs by the generator, never declared by a session.

---

## RECAP

**HA-46A** — **356 legacy recall-audit entries cleaned; 0 commitments retained, 356
metadata-only**, because none of the 261 distinct subjects still has key context (their keys went
in the test-key hygiene sweep) and **no key was invented to manufacture one.** 4 HA-45-era
entries already compliant and untouched; entry count preserved 360→360; 119,259→101,896 bytes.
**Restart-proved in a fresh process: 0 text keys via the supported reader, 0 of 6 query strings
in the raw file, metadata and the 4 commitments intact.** Fault twin planted/cleaned/verified
both ways. **Transcripts untouched: 425+425 files, 27,732 lines, byte-identical.** Binding
**1179/0/9xf**, layer 7 **exit 0**, RATCHET **PASS**, memory **13/17**. **TD-R-189 filed.**
Nothing ruled MET.
