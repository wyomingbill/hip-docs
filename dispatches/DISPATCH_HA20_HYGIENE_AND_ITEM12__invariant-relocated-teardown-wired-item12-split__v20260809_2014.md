# DISPATCH_HA20_HYGIENE_AND_ITEM12 — invariant relocated, teardown wired, item 12 split

Status: BUILT
Reconciled-Against: roadmap `7b776b3` (pre-dispatch HEAD)

**HA-20** | 2026-08-09 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD + GOVERNANCE**
**AUTHORITY:** Bill's rulings 2026-08-07 (REQ MET; rule-3a ratified; item 12 amended).

**CLAIM IMPACT: C-10, C-11** — see §8. Neither is ruled here; the ledger's statuses are
computed by a generator that does not exist yet.

---

## 1. ITEM 1 — BILL'S RULINGS RECORDED

**`REQ_DERIVED_WRITE_CUSTODY` → MET**, ruled on HA-19's acceptance table (that dispatch's
§9). Recorded in the REQ's status header with the clauses it rests on, and in HA-19's own
dispatch doc as a ruling block at the top.

**The rule-3a subject-keyed scope fix is RATIFIED**, in Bill's words:

> **"Scope follows the subject, not the author. Keep the fix."**

HA-19 flagged that as its one judgement call and offered to revert it in one commit. **It
now stands as a principle in Bill's words rather than a session's reading of an outcome**,
and both documents say so.

**What the ruling deliberately does NOT cover, stated in both places:** HA-19's §10 ratchet
reds, and the two out-of-scope discoveries (`encode()`'s silent no-op on an unrecognised
write state; no `author` property persisted on the node). Those stay open.

## 2. ITEM 2 — ITEM 12 SPLIT: DETERMINISTIC BINDS, LIVE REPORTS

Bill's rule, verbatim, now in `CLAUDE.md` Requirements Discipline item 12:

> **"Deterministic tests remain binding and must pass every time (batteries, L7, L7V2,
> AUDIT, DISC, SCHEMA, VOICE, and the ratchet over them). Tests that depend on live model
> output are reported separately and do not make the build pass or fail until a
> reproducibility rule exists for them. Do not use best-of-N. Do not invent a pass
> threshold — collect repeated runs first, then set the rule from data."**

The amendment records **why** — HA-19's three `--full` runs, the last two byte-identical and
disagreeing on L1/L3/L4/L6 and on the ratchet's own regression list — and spells out the two
forbidden shortcuts (**no best-of-N**, **no invented threshold**), plus the obligation that
a live-layer red is still *reported*: **"A dispatch that hides a live-layer red because it
'doesn't gate' has broken this rule as surely as one that claims a green ratchet it does not
have."**

## 3. ITEM 3 — THE DATA COLLECTOR

`logs/harness/live_layer_results.csv`, appended **automatically by every `--full`** —
`eval/harness.py` calls `reporter.append_live_layer_results(mode="full")`, so collection
cannot depend on a dispatch remembering a separate tool.

```
run_id, ts, commit, mode, layer, sid, status, tier
```

**One row per live-layer scenario per run, not per layer.** `harness_trend.jsonl` already
records per-layer counts and they are not sufficient: the question a reproducibility rule
must answer is *"how often does THIS scenario flip?"*, and "L3 went 3/3 → 1/3" cannot
distinguish one chronically unstable test from three occasionally unstable ones.

`LIVE_LAYERS = {L1, L2, L3, L4, L6}` — the layers HA-19 measured as non-reproducible. L2 is
included because its `routing_showcase` scenarios route through the live model.

**No threshold is implemented anywhere.** That is the point: the rule comes later, from
Bill, out of this file.

**IT IS GITIGNORED, AND THAT IS A LIMITATION WORTH NAMING NOW RATHER THAN AT RULE-SETTING
TIME.** `.gitignore:52` excludes `logs/`, so this series accumulates **on one machine only**
and does not survive a reimage or reach another lane. It was placed under `logs/` because
that is where run output belongs and because committing a file that every `--full` appends
to would put a write into the commit graph on every run. **The trade is deliberate, but if
the reproducibility rule is meant to be set from a shared record rather than this laptop's,
the file needs a home that is tracked — a decision about what the repo carries, and Bill's.**

## 4. ITEM 4 — THE ZERO-ORPHAN INVARIANT, RELOCATED AND PROVEN BOTH WAYS

**Moved** from the pytest battery (`test_zzz_no_fixture_keys_survive_the_suite`) to
`eval/harness.py` as **`AUDIT:KEY-HYGIENE-ZERO-ORPHAN`**, tier ABSOLUTE, running after every
layer.

**Why it could not stay:** `zzz` sorted it last *within the batteries*, but the batteries are
not the last thing that mints keys — L7 and L7V2 run afterwards. **It asserted a
postcondition before the work finished**, then failed on the next invocation for keys it had
never had a chance to see. Not cosmetic: `run_harness.sh` gates the harness behind the
batteries, so every `--full` left keys behind and the next `--full` aborted at the gate.

The battery keeps the **mechanism** tests (classification, fail-closed refusal, destruction,
and `assert_no_live_test_keys`' own red-on-stray-key twin) plus a structural test asserting
the relocated check still exists in `eval/harness.py` — so it cannot vanish in transit.

### The red/green proof, executed

| | run | result |
|---|---|---|
| **GREEN** | clean tree | `KEY-HYGIENE-ZERO-ORPHAN PASS` · AUDIT 9/9 · L7 27/27 · L7V2 27/28 · **RATCHET PASS** · exit 0 |
| **RED** | one stray `_snd_ha20strayproof.seal.key` surviving the suite | `KEY-HYGIENE-ZERO-ORPHAN FAIL` · AUDIT 8/9 · `NEW FAILURES: ['AUDIT:KEY-HYGIENE-ZERO-ORPHAN']` · exit 2 |
| **GREEN again** | stray destroyed | `PASS` · AUDIT 9/9 · **RATCHET PASS** · exit 0 |

The red names the offender rather than just failing:

```
[FAIL] live_test_keys == 0 after every layer has run and torn down — 1 leaked:
       ['_snd_ha20strayproof.seal.key']
```

**A note on how the stray was planted, because the first attempt did not prove what it
looked like.** Planting mid-layer-7 via a log-watcher raced the buffered output and landed
*after* the check — which reported PASS, and would have been a false all-clear had it been
read as the proof. **A key minted mid-layer is destroyed by teardown, which is the desired
behaviour**; to exercise the invariant, the key has to be one that *survives* teardown. A
key present before the run does exactly that, deterministically, and is also the real-world
case — it is precisely the shape of HA-19's 8 leftovers. Both directions are therefore
proven: **teardown removes what a layer mints; the invariant catches what escapes.**

## 5. ITEM 5 — TEARDOWN WIRED INTO THE PRODUCERS

Both layer-7 entrypoints now wrap their body and tear down in a **`finally`** — a probe that
raises must still clean up, or one bad run poisons the next one's battery gate, which is the
exact failure HA-19 hit.

```
[probe-teardown: L7]   destroyed 2 fixture seal key(s), de-registered 0 principal(s)
[probe-teardown: L7V2] destroyed 6 fixture seal key(s), de-registered 5 principal(s)
```

Teardown destroys **the delta**, not the whole directory — destroying everything classified
as a test key would reach into keys a concurrently-running lane minted. The P4 fixture keeps
its own `_ensure_member` (it provisions identity and seal keypairs too) but now calls
`register_for_teardown(mid)`, so it feeds **the one teardown path** instead of growing a
second, divergent one.

### A FIFTH PRODUCER, found by the fail-closed report

`ctxstrip_probe_owner.seal.key` matched no `TEST_KEY_PATTERNS` entry, so the classifier
**failed closed and kept it** — correct behaviour, and the reason it had been accumulating
unnoticed since that probe was written. Item 5 named four producers; this is the one nobody
had counted, and **it was found because the relocated invariant REPORTS unclassified keys
rather than passing silently over them.** Pattern added; the six real keys are untouched and
still spared by name.

### ITEM 5's SECOND HALF COULD NOT BE DONE, AND THAT IS THE FINDING

> **"Also provision the household wrap for enrolled probe principals so the HA-19
> decrypt-skip log noise stops."**

**Built, executed, and BACKED OUT.** It is not safely satisfiable, and the reason outweighs
the noise:

Provisioning a wrap requires enrolling the probe as a household **circle member** — and
circle membership is not a read permission, it makes the member **a permanent participant in
the household key tree**. `ensure_household_keys` unwraps HH_priv through an enrolled circle
member, so a roster entry whose seal key no longer exists takes the whole tree down:

```
FileNotFoundError: [REDACTED-USER-PATH]/hip-keys/ob4_probe_owner.seal.key
  … ensure_household_keys → unwrap_household_privkey → load_seal_private_key
```

**And these probes' keys are destroyed at teardown by design — item 5's own first half.**
The two halves are in direct conflict: **an ephemeral principal cannot also be a permanent
custodian.** Nor is the blast radius local — it breaks `encrypt_by_class` for *every*
household-circle-shared write, the real demo's included.

**The noise stays; it is the cheaper problem.** `read_user_facts` returns household-owned
rows to any enrolled member and skips those it cannot decrypt — the tracebacks are logged,
caught and harmless. **The real fix belongs in `read_user_facts`: don't attempt rows the
caller holds no wrap for, instead of attempting and logging a traceback. That is a change to
the READ PATH and is Bill's call, not a side effect of a hygiene dispatch.** The function is
left in place as a documented no-op so the question is not silently forgotten.

**Damage repaired in the same session:** four probe ids had been enrolled into the circle and
one had been healed a wrap. Roster restored to `['bill','maya','sam']`, stale wrap dropped.
**`remove_circle_member` could not be used — it raises `sqlite3.OperationalError: no such
column: epoch`** (§9, finding 4), so the removal was a targeted `removed_at` update on those
four rows only.

### The subtler fault it exposed on the way — worth more than the feature

Two **deterministic** checks went red mid-build (`L7:PSA1`, `L7V2:SC1`), and the cause is a
trap this dispatch created and then had to fix properly:

**Teardown destroys the key FILE, but the registry row survives with its `seal_pubkey` still
set.** The next run finds a registered pubkey and no private key, mints a fresh private key,
leaves the stale pubkey registered — **writes seal to the old pubkey, reads use the new key,
and the probe's own fact becomes unreadable to itself.** Neither probe reports a key error;
both report the fact as *not present*, which is the least informative possible symptom.

Fixed at **both** ends: `_heal_seal_key_desync` repairs whatever state it finds at enrolment
(so a crashed run's mess does not poison the next one), and teardown now clears the registry
pubkey for every key it destroys. Neither is load-bearing alone, deliberately.

## 6. ITEM 6 — `--full` TWICE, BACK TO BACK, NO HAND CLEANUP — **THE BLOCKER IS GONE**

Both runs issued from one shell, in sequence, **with nothing between them.** No sweep, no
`destroy_test_keys`, no intervention of any kind.

| | run 1 | run 2 |
|---|---|---|
| **battery gate** | `851 passed, 0 failed` | **`851 passed, 0 failed`** |
| keys present at start | `[]` | **`[]` — measured between the runs** |
| teardown, L7 / L7V2 | 3 keys / 3 principals · 6 keys / 6 principals | *(§6.1)* |
| `AUDIT:KEY-HYGIENE-ZERO-ORPHAN` | **PASS** | *(§6.1)* |

**Run 1 left ZERO keys behind**, measured in the same shell between the two invocations:

```
=== keys before run 1: [] ===
FULL#1 EXIT=1
=== NO CLEANUP BETWEEN — keys now: [] ===
```

That is stronger than "run 2's gate survived". **There was nothing for it to survive.**
Before this dispatch run 1 left 8 keys and run 2 aborted at the gate before starting, which
is why HA-19 had to sweep by hand between every pair. **`--full` is repeatable again** — the
precondition for item 12 meaning anything at all.

### One honest gap: the EXIT CODE has not caught up with the rule

`FULL#1 EXIT=1`. The run's deterministic layers were **all green**; the non-zero exit comes
entirely from the live-layer ratchet. **Under item 12's amended rule that run did not fail —
but `run_harness.sh` still says it did.**

**Deliberately not "fixed" here.** Making the exit code reflect the deterministic/live split
is a change to what gates a push, and item 2 is explicit that the live-layer rule comes from
collected data and from Bill, not from a session's judgement. **Named so nobody reads a
non-zero exit as a deterministic failure in the meantime** — read the layer lines, not the
exit code, until Bill rules.

### Run 1 — deterministic layers, the binding set under item 12's amended rule

```
== L7:  27/27      == L7V2: 27/28 (1 skip)     == AUDIT:  9/9
== DISC: 1/1       == SCHEMA: 1/1              == VOICE:  1/1
batteries: 851 passed, 0 failed
[probe-teardown: L7]   destroyed 3 fixture seal key(s), de-registered 3 principal(s)
[probe-teardown: L7V2] destroyed 6 fixture seal key(s), de-registered 6 principal(s)
KEY-HYGIENE-ZERO-ORPHAN  PASS
```

**Every binding layer green.**

### Run 1 — live layers, REPORTED, NOT GATED

```
RATCHET FAIL — regressed vs baseline: ['L2:routing_showcase.T04']
NEW FAILURES (not in baseline): ['L1:P12', 'L6:record-invariants']
[live-layers] appended 88 scenario result(s) to logs/harness/live_layer_results.csv
              (run_id=20260810T023252_7b776b3)
```

All three are live-layer scenarios, all three are already characterised by HA-19, and **none
is in the binding set:**

- **`L2:routing_showcase.T04`** — the one stable regression; answers a news query with the
  clock. Red in all five `--full` runs across HA-19 and HA-20.
- **`L1:P12`** — never baselined; its two checks read `e.get("payload", {})` on events the
  reader returns without a `payload` key at all, so they **cannot pass whatever the code
  does.**
- **`L6:record-invariants`** — red in 2 of 4 observed runs, green in the others, with no code
  change between.

**No gate claim is made either way**, per the amended rule. The collector now has its first
88 rows, and the per-scenario breakdown is exactly the granularity a reproducibility rule
needs:

```
L1  15 rows, 1 non-PASS   P12(FAIL)
L2  35 rows, 12 non-PASS  routing_showcase.T04(FAIL) three_zone_demo.T02(FLAKE) + 10 SKIP
L3   3 rows, 0 non-PASS
L4  34 rows, 4 non-PASS   4 × SKIP
L6   1 row,  1 non-PASS   record-invariants(FAIL)
```

Note it separates **FAIL from FLAKE from SKIP** — a per-layer count could not, and "L2 24/35"
would have hidden a genuine failure among ten scenarios that never ran.

### 6.1 Run 2 — and it left the graph in the same state it found it

```
batteries: 851 passed, 0 failed          <-- the gate that used to abort here
== L7:  27/27      == L7V2: 27/28 (1 skip)     == AUDIT:  9/9
== DISC: 1/1       == SCHEMA: 1/1              == VOICE:  1/1
[probe-teardown: L7]   destroyed 3 fixture seal key(s), de-registered 3 principal(s)
[probe-teardown: L7V2] destroyed 6 fixture seal key(s), de-registered 6 principal(s)
KEY-HYGIENE-ZERO-ORPHAN  PASS
[live-layers] appended 88 scenario result(s)  (run_id=20260810T025902_7b776b3)
RATCHET FAIL — regressed vs baseline: ['L2:routing_showcase.T04']
NEW FAILURES (not in baseline): ['L1:P12', 'L6:record-invariants']
```

**Every deterministic layer identical to run 1. Teardown identical — 3 and 6, both runs.
`KEY-HYGIENE-ZERO-ORPHAN` PASS both runs. The CSV holds 176 rows across two run_ids.**

**ITEM 6 IS SATISFIED:** two `--full` runs back to back, no hand cleanup, **both battery
gates passed**, and the second left the key directory exactly as the first did — empty.

### What the two runs say, and what they carefully do not

The live-layer reds are **identical across both runs**: `L2:routing_showcase.T04`,
`L1:P12`, `L6:record-invariants`. That is two consecutive agreeing runs.

**It is not evidence of reproducibility, and this dispatch will not present it as such.**
HA-19's runs also agreed in pairs before diverging — its runs B and C were byte-identical and
disagreed on four layers. **Two agreeing observations are two observations.** That is exactly
why item 2 forbids inventing a threshold and why the collector exists: the rule gets set from
the series, once the series is long enough, by Bill.

## 7. ITEM 7 — RUNS

| Run | Result |
|---|---|
| **Batteries** | **851 passed, 0 failed** |
| **`--layer 7`** | L7 **27/27** · L7V2 **27/28** (1 skip) · AUDIT **9/9** · DISC/SCHEMA/VOICE 1/1 |
| **RATCHET** (deterministic) | **PASS — no scenario regressed vs baseline** |
| **Memory harness** | **13/17 — INSIDE THE PIN** (13–15). Same four: MEM-115/116/117/118 |
| **`--full` ×2, back to back** | **both battery gates passed, both `KEY-HYGIENE-ZERO-ORPHAN` PASS, 176 rows collected** (§6) |

**Every binding layer under item 12's amended rule passes, in both `--full` runs and in the
standalone `--layer 7`.** Live-layer results are recorded in §6 and in
`logs/harness/live_layer_results.csv`, **with no gate claim either way.**

**Stated plainly so the report cannot be read as a green ratchet:** `RATCHET FAIL` appears in
both runs and both exit non-zero. Under the amended rule those are **live-layer** results —
reported, not gating — and the deterministic set that *does* gate is clean. **The exit code
does not yet make that distinction (§6), so read the layer lines.**

## 8. CLAIM IMPACT

**CLAIM IMPACT: C-10, C-11.**

- **C-10** *("Key material is never captured by backups, and test keys cannot contaminate
  production custody")* — the zero-orphan invariant now actually runs after the producers,
  five producers tear down, and a fifth previously-invisible leak is classified. **This is
  the evidence C-10's "invariant relocation pending" note was waiting on.**
- **C-11** *("The full end-to-end suite passes with no masked or falsely-refused checks")* —
  `--full` can now be run repeatedly without hand cleanup (§6). **C-11 is NOT satisfied by
  that alone:** its live layers still fail intermittently, and item 12's amendment means
  the phrase "the full suite passes" now needs restating in terms of the deterministic /
  live split before it can be assessed at all. **Flagged for Bill as a claim-wording
  question, which is his to rule.**

**No status is asserted here.** The ledger's statuses are computed by a generator that does
not exist yet; naming a claim is a pointer, not a ruling.

## 9. FINDINGS

1. **The invariant was asserting a postcondition before the work finished** (§4) — and the
   consequence was that `--full` could not be run twice.
2. **A fifth key producer existed and was invisible** (§5), found by the fail-closed report,
   not by a failure.
3. **Item 5's two halves contradict each other** (§5) — an ephemeral principal cannot be a
   permanent household custodian. Built, backed out, documented in place.
4. **`harness.household_keys.remove_circle_member` IS BROKEN** — `sqlite3.OperationalError:
   no such column: epoch`. It bumps a `household_keys.epoch` column that does not exist in
   the schema (`household_id, hh_pubkey, created_at`). **Any caller trying to remove a
   circle member today fails**, which matters well beyond this dispatch: it is the removal
   half of household circle management. Found while repairing §5's damage. **Not fixed —
   out of scope, and a schema change on the custody registry is not a hygiene-dispatch side
   effect.**
5. **Destroying a key without clearing its registered pubkey creates a silent desync**
   (§5) whose symptom is "fact not present", not "key error". Fixed at both ends.
6. **`run_harness.sh`'s EXIT CODE still fails on live layers** (§6) — a run whose binding
   layers are all green still exits non-zero. **The tooling has not caught up with the
   amended item 12**, and changing what gates a push is Bill's, not a session's. Until then,
   **read the layer lines, not the exit code.**
7. **The collector's first 88 rows already show why per-scenario was the right grain** (§6) —
   L2's "24/35" conceals one genuine FAIL, one FLAKE and ten SKIPs, three different things a
   per-layer count renders identical.
