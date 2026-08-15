# DISPATCH_HA14_KEY_SWEEP — 1,390 test keys destroyed, teardown built, three TDs closed

Status: BUILT
Reconciled-Against: roadmap `c63e3fc` (pre-dispatch HEAD). **LANDED AT `cc2f257`** — backfilled by the immediately following commit.

**HA-14** | 2026-08-07 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD + IRREVERSIBLE DELETION**
**AUTHORITY:** Bill's ruling 2026-08-07, recorded verbatim in §1.
**NOTHING MET. No seal-fix code — the write-side custody ruling builds as HA-15 behind its REQ.**

**First doc under the new naming law** (`CLAUDE.md`, "Dispatch docs lead with their ID"):
the filename starts with `HA14`.

## 1. THE RULING (item 1), verbatim

> "Full sweep of positively identified test keys, preserve the six real keys explicitly,
> fail closed on anything unclassified, and prove decryptability before and after."

## 2. DECRYPT CENSUS — BEFORE (item 2)

Run first, before a single file was touched.

```
valid_from                  owner       subject  attribute      decrypt
2025-06-28T00:30:57.170565  household   househol schedule       OK
2025-06-28T00:30:57.170565  household   househol household      OK
2026-01-06T00:30:57.170565  maya        maya     medication     OK
2026-02-08T00:30:57.170565  household   househol address        OK
2026-02-08T00:30:57.170565  household   househol zone_district  OK
2026-02-27T02:37:56.247522  maya        ray      medication     OK
2026-05-03T00:30:57.170565  sam         sam      preference     OK
2026-07-04T00:30:57.170565  maya        maya     appointment    OK
2026-07-25T00:30:57.170565  sam         dad      medication_sta OK
2026-07-28T00:30:57.170565  sam         dad      incident       OK
2026-07-30T00:30:57.170565  household   dad      risk_pattern   FAIL InvalidToken

TOTALS: 10 OK, 1 FAIL
```

**Matches item 2's expectation exactly.** The one FAIL is D8 — TD-R-171, known, and **not
this dispatch's to fix** (HA-15).

## 3. CLASSIFICATION (item 3) — produced BEFORE any deletion

**1,396 `*.seal.key` in `~/hip-keys/`.** Reconciled: **6 REAL + 1,390 TEST + 0 UNCLASSIFIED
= 1,396.**

**REAL — spared BY NAME, exact match, never by pattern (6):**

```
alice.seal.key  bill.seal.key  bob.seal.key  household.seal.key  maya.seal.key  sam.seal.key
                                                              [all six present]
```

**A pattern that happened to match `maya.seal.key` would destroy a real custody key, and
nothing downstream recovers from that** — so REAL is an exact-name set, checked first.

**TEST — positively identified by fixture family (1,390):**

| count | family |
|---|---|
| 821 | P4 quorum/custody fixtures (`p4admin_`, `p4lost_`, `p4peera_`, `p4peerb_`, `p4principal_`, `p4smoke_`, `p4r*`) |
| 539 | memory harness fixtures (`memtest-`) |
| 24 | sensitivity / offer batteries (`_snd_`, `_snd_r_`, `_snd_w_`) |
| 2 | diagnostic probes (`_probe_`) |
| 2 | PSA1 partition-seal fixtures (`psa1_`) |
| 1 | SC1 answer-mode fixture (`_sc1_`) |
| 1 | OB4 operator-blind probe (`ob4_probe_owner`) |

**UNCLASSIFIED — kept, never deleted, fail closed: 0.** The fail-closed branch was never
exercised because nothing landed in it — but it existed before the sweep ran, which is the
point.

**OUT OF SCOPE, named so it is not mistaken for coverage:** 827 non-`.seal.key` files remain
in `~/hip-keys/` (identity `*.key`, a Neo4j credential dir). Item 3 scoped this sweep to
`*.seal.key`; those were not classified and not touched.

## 4. THE SWEEP (item 4)

Pre-delete safety assertion first: **the delete list contained 0 of the six real names.**

```
found (total *.seal.key)   : 1396
DELETED (test)             : 1390
spared (real, by name)     : 6
kept (unclassified)        : 0
remaining *.seal.key       : 6
```

Remaining: `alice bill bob household maya sam` — and nothing else.

## 5. DECRYPT CENSUS — AFTER (item 5)

**`TOTALS: 10 OK, 1 FAIL`** — same eleven rows, same verdicts, same single known FAIL on
D8. Nothing new.

**A FALSE ALARM THIS DISPATCH RAISED AGAINST ITSELF, recorded rather than quietly fixed.**
The first `diff` of before-vs-after reported a DIFFERENCE and printed `*** STOP ***`. It was
**my own instrumentation**: the BEFORE script appended `(expected: 10 OK, 1 FAIL = D8/…)` to
its totals line and the AFTER script did not. Re-diffed on data rows and on the totals
counts alone, the two are identical. **Item 5 is satisfied**, and the near-miss is the D-75
trap in a third costume — a check whose own formatting manufactures a scary result.

## 6. TEARDOWN — TD-R-172 CLOSED (item 6)

The sweep cleans; this prevents recurrence. **1,390 orphans against 6 real keys is 231
orphans per real key** — the leak was the defect, not the mess.

**`harness/test_key_hygiene.py`** — one classifier, fail-closed:

- `REAL_KEYS` exact-match set; `TEST_KEY_PATTERNS` positive identification; everything else
  **UNCLASSIFIED → kept and reported**.
- `destroy_test_keys()` — **the classification is the gate, not the caller's intent.** A
  caller asking to destroy `maya.seal.key` is refused.
- `sweep_stale_test_keys(report=…)` — **never silent.** A silent sweep would hide the leak
  it cleans: a battery leaking every run would look clean forever because the next run
  tidied up after it.
- `assert_no_live_test_keys()` — names the leftovers, because "some keys leaked" is not
  actionable and "these three leaked" is.

**Wired:** the sensitivity battery destroys its `_snd_*` keys in fixture teardown; the
memory harness sweeps at startup and destroys what it minted in a `finally`.

**`eval/test_key_hygiene.py`** — 8 cases including the standing invariant
`test_zzz_no_fixture_keys_survive_the_suite` (named to sort last). The classifier's
fail-closed behaviour is **tested, not assumed**: an unknown key classifies UNCLASSIFIED,
and `destroy_test_keys` refuses both REAL and UNCLASSIFIED input. Registered in the battery
list; the manifest check accepted it.

**PROVEN LIVE:** the memory-harness run printed
`[key-hygiene] destroyed 7 fixture seal key(s) minted by this run`, and after both harness
runs `~/hip-keys/` holds **exactly the six real keys**.

## 7. RIDERS — TD-R-170 and TD-159 CLOSED (items 7, 8)

**TD-R-170** — acceptance complete. Runs (a) muted → exit 4 and (c) unreadable → exit 5 are
verbatim in HA-08's doc; **run (b) audibility confirmed by Bill, 2026-08-06** — the one
thing the script cannot assert about itself, which is why the guard's zero exit now means
only that the playback command completed.

**TD-159** — mechanical rename only, no test logic: 17 functions in
`eval/test_lineage_block.py` → `test_ceil_a18_*`, 27 in `eval/test_sensitivity_registry.py`
→ `test_ceil_a29_*` (11) / `test_ceil_a30_*` (16). **All 60 still pass.**

**Confirmed by the board's own counters, measured BOTH WAYS** — the pre-rename tree pulled
from git and re-run through the generator:

```
PRE-RENAME :  claimed-LIVE=12 verified-LIVE=9  CLAIMED-NOT-VERIFIED=3
POST-RENAME:  claimed-LIVE=12 verified-LIVE=12 CLAIMED-NOT-VERIFIED=0
```

Exactly the three rows TD-159 named. Measuring both ways beats reading one board, because a
board that had always said 0 would look identical.

### The rename broke a test, and the test had already told us it would

`test_board_real_documents_cross_check_is_not_vacuous_and_finds_a_real_gap` **pinned
`{A18, A29, A30}` as its proof that the board's cross-check is not vacuous.** Closing the
gap removed its witness, and the first `--layer 7` went red — **aborting the harness before
RATCHET ever ran.**

Its own docstring anticipated this exactly: *"If this assertion goes red because those rows
were renamed onto the convention, that is the naming gap closing — **update the pin, do not
widen it.**"*

**The pin was updated to the empty set on that instruction — narrowed, not widened** — and
the docstring now records why. **Non-vacuity does not rest on the pin:** `acc["live"] > 0`
still fails if the scanner finds no runners, and `claimed_live == live + unverified_live`
still fails on a miscount. Both bite with an empty gap.

**BOTH RUNS ARE REPORTED**, because a silently re-run check is indistinguishable from a
cherry-picked one.

## 8. ITEM 9 — the open-file clarification

One line added to `CLAUDE.md`'s routing rule, above the D-118 prohibition: **"open the file"
means open it in the default app so the report is on Bill's screen; the D-118 prohibition is
on COPY-PASTING OUT of the opened window, not on opening.** HA-09 flagged this conflict and
followed the law; the clarification settles it.

## 9. RUNS (item 11)

| Run | Result |
|---|---|
| Standing battery, FIRST `--layer 7` | **1 failed** — the TD-159 pin above; **harness aborted before RATCHET** |
| Standing battery, after the pin update | **820 passed, 1 skipped, 9 xfailed** |
| `--layer 7` L7 / L7V2 | **27/27** / **27/28** |
| AUDIT / DISC / SCHEMA / VOICE | **8/8** / 1/1 / 1/1 / 1/1 |
| **RATCHET** | **PASS** |
| Memory harness | **13/17**, failures exactly {MEM-115, MEM-116, MEM-117, MEM-118}, inside the pin |

**Item 11's note held:** memory-harness key counts dropped (7 destroyed at teardown), the
17-test result did not move.

`--full` not attempted: TD-R-171 still blocks Layer 2. **Item 12 NOT satisfied.**

## 10. FINDINGS

1. **The sweep is not the fix; the teardown is** (§6). Without it the 1,390 return.
2. **A test pinned a defect as its non-vacuity witness** (§7). Fixing the defect broke the
   test. Its docstring had pre-authorised the update, which is the only reason this was a
   pin change rather than a stop — **worth copying as a pattern: a check that pins a known
   gap should say what to do when the gap closes.**
3. **827 non-`.seal.key` files in `~/hip-keys/` were out of scope** (§3) and are unswept.
4. **The false-alarm STOP in §5** — third appearance of the family where a check's own
   formatting produces a confident wrong answer.

---

## 11. CORRECTION, MADE BY THIS DISPATCH AGAINST ITSELF — post-commit

**§6 claimed: *"after both harness runs `~/hip-keys/` holds exactly the six real keys."*
That was true when measured and is NO LONGER TRUE. It is corrected here rather than edited
above, so the wrong claim and its correction both stand.**

A final check after committing found **14** seal keys, not 6. The 8 extra:

```
_sc1_superseded_owner.seal.key   ob4_probe_owner.seal.key   psa1_probe_owner.seal.key
p4admin_d3c40017.seal.key        p4lost_d3c40017.seal.key   p4peera_d3c40017.seal.key
p4peerb_d3c40017.seal.key        p4principal_d3c40017.seal.key
```

All 8 classify **TEST**, zero UNCLASSIFIED — so the classifier is right and the sweep's
scope was right. **They were minted by the SECOND `--layer 7` run** (the one after the
TD-159 pin update) by batteries this dispatch did NOT wire: the P4 quorum/custody suite,
PSA1, SC1 and the OB4 probe.

### What this means for TD-R-172's closure — narrower than §6 claims

| Claim in §6 | Corrected |
|---|---|
| "every fixture-writing battery … destroys its keys" | **Two are wired** — the sensitivity battery and the memory harness. **The P4, PSA1, SC1 and OB4 producers are NOT**, and they leak on every `--layer 7`. |
| "PROVEN LIVE … holds exactly the six real keys" | True at that instant; **8 leaked afterwards.** |

**And the invariant did not catch it, which is the more useful finding.**
`test_zzz_no_fixture_keys_survive_the_suite` runs inside the standing-battery block, which
executes **before** the harness's own layer-7 scenarios mint their keys. **The invariant is
real but positioned too early to see the biggest remaining leakers.** A postcondition that
runs before the thing it guards is a postcondition in name only.

**TD-R-172 is therefore re-scoped, not re-opened**: the mechanism, classifier and invariant
are built and proven; the wiring covers 2 of ~6 producers and the invariant needs to run
after the harness, not inside it. Recorded in the register row rather than left implied by a
closure that reads broader than it is.

**Not fixed here.** Wiring four more batteries and relocating the invariant is real work
with its own blast radius, and this dispatch had already committed. It is the first thing
HA-15 or a successor should pick up.
