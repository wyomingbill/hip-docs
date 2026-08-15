# DISPATCH_HA19_GUARDS_LANDED — author validity enforced, the scope rule corrected, census clean

Status: BUILT (items 1–9 executed; item 10 referred to Bill) — **RULED AT HA-20, 2026-08-07**
Reconciled-Against: roadmap `eac8dfb` (pre-dispatch HEAD)

> ## BILL'S RULING ON THIS DISPATCH (2026-08-07, recorded at HA-20)
>
> **`REQ_DERIVED_WRITE_CUSTODY` is MET**, ruled on §9's acceptance table.
>
> **The rule-3a subject-keyed scope fix is RATIFIED: *"Scope follows the subject, not the
> author. Keep the fix."*** §4 flagged it as this dispatch's one judgement call and offered
> to revert it in one commit. **It stands, and the principle is now Bill's words rather
> than a session's reading of an outcome.**
>
> **What the ruling does NOT cover:** §10.1–10.2's ratchet reds, §11's findings 7–9, and the
> two out-of-scope discoveries (`encode()`'s silent no-op on an unknown write state; no
> `author` property persisted on the node). Those remain open. Item 12's amendment answering
> §10.2's non-reproducibility finding is HA-20's item 2.

**HA-19** | 2026-08-07 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD**
**AUTHORITY:** Bill's ruling 2026-08-07 (order binding) + `REQ_DERIVED_WRITE_CUSTODY`.
**Both guards are LIVE. C1 is 11/11 for the first time. `REQ_DERIVED_WRITE_CUSTODY` is
ruled ready in §10 — Bill rules MET, not this session.**

---

## THE ONE THING TO READ FIRST

**Item 3's check FAILED on its first execution, and it was right to.** Correcting the four
fixtures' authors silently reclassified **three of them from household-circle-shared to
member-private** — the demo's household facts would have become Sam's private facts. The
cause was not the fixtures: **rule 3a derived SCOPE FROM AUTHOR**, which is the exact
conflation Bill's AUTHOR VALIDITY clause forbids. §3 has the measurement, §4 the fix.

Everything else follows from that being caught before the guards went live, which is what
the binding order was for.

## 1. ITEM 1 — ONE CONSTANT, ONE STORY

`scripts/demo_seed.py`:

```python
DEMO_ONBOARDING_AUTHOR = SAM_ID
```

Sam set up the household and entered the household-level onboarding facts. All four seeds
derive from this constant — **no four unexplained literals**, so a later edit cannot move
one without the others. That drift is precisely how D8 came to disagree with its neighbours.

The comment records what it replaced and why: all four authored as `HOUSEHOLD_OWNER`, the
literal scope marker, which is not an authenticated principal.

## 2. ITEM 2 — D3, D7, D10, D11 AUTHORED FROM THE CONSTANT

Subject and audience rules untouched: `subject` stays `HOUSEHOLD_OWNER` on all four.

## 3. ITEM 3 — THE CHECK FAILED FIRST. THE MEASUREMENT, BEFORE THE FIX

```
lbl  OLD author   OLD visibility           NEW author   NEW visibility           SCOPE UNCHANGED?
D3   household    household-circle-shared  sam          member-private           *** NO ***
D7   household    household-circle-shared  sam          household-circle-shared  YES
D10  household    household-circle-shared  sam          member-private           *** NO ***
D11  household    household-circle-shared  sam          member-private           *** NO ***
```

**Three of four flipped.** Only D7 survived — because its attribute is literally
`"household"`, and that was the one trigger rule 3a had that did not depend on the author.

### Why — `harness/write_rule.py`, rule 3a's trigger as it stood

```python
if (author == "household" or attribute == "household") and (…):
    return WriteClass(CLASS_HOUSEHOLD, "household", …)
```

**`author == "household"` IS "the author determines the scope".** It is the same conflation
the clause names — *"`author` … SHALL NOT contain an audience, scope, partition, custody, or
routing marker"* — sitting inside the classifier rather than inside a fixture. D3, D10 and
D11 reached household scope **only** through it. Removing the malformed author removed their
scope with it.

**D-R-176 had already seen half of this.** Its own comment on that rule names
*"demo_seed.py's D3/D7/D10/D11 fixtures … for genuinely household-wide facts
(subject=HOUSEHOLD_OWNER)"* — it added `subj == "household"` to the rule's GATE and never to
its TRIGGER. The recognition was written down without being wired.

## 4. THE FIX — HOUSEHOLD SCOPE KEYED ON THE SUBJECT

```python
if (author == "household" or attribute == "household" or subj == "household") and (…):
```

**STRICTLY ADDITIVE.** No write that lands household-circle today stops doing so; the newly
covered set is exactly *subject == "household", attribute != "household", author a real
member.* The `author == "household"` disjunct is left in place and annotated: it is now
unreachable through `classify_write`, but `classify` is called directly by the coverage-grid
tooling, and silently deleting a branch those callers exercise would trade one invisible
change for another.

### This is a judgement call, and it is flagged as one

Bill's item 2 said *"subject and audience rules unchanged; these remain household facts."*
**Those two halves turned out to contradict each other in code** — the outcome could not be
had without touching the rule. This dispatch took the OUTCOME as the ruling ("these remain
household facts") and the "unchanged" clause as an expectation that measurement disproved.
**If that reading is wrong, the fix is one commit to revert** and the four fixtures then need
a different answer.

### Anti-vacuity: 9 fault twins, and what they protect

| case | expected | why |
|---|---|---|
| `sam / ray / household` | **NOT household** | Bill's own probe — a household attribute about a REAL PERSON must still narrow |
| `sam / sam / address` | **NOT household** | a member's own address; the attribute alone must never widen |
| `maya / sam / address` | **NOT household** | 3c mandatory exclusion |
| `sam / dad / risk_pattern` | **NOT household** | D8's shape; 3c is hard and non-overridable |
| `sam / maya / preference` | **NOT household** | characterizations about a person untouched |
| `bill / household / household` | household | D-R-176's P1 fixture keeps working |
| `sam / household / schedule` | household | the case the widening exists for |
| `sam / household / schedule` + *"just between us"* | **NOT household** | level 2 returns above 3a — the author keeps the last word |
| `"household" not in known_subject_ids()` | — | the sentinel can never be RESOLVED as a subject; it arrives only when a caller sets it deliberately |

**Two of these were the TEST being wrong, and are recorded rather than quietly fixed.** The
first draft asserted an exact narrowed class (pair- vs member-private) where the answer
depends on the dyad registry's contents, not on this rule; and it used the utterance
*"keep this private"* when the real directive phrase is `"just between us"` — so the
directive-precedence case proved nothing until corrected. **That last one mattered: this
dispatch had already written the precedence claim into a code comment.**

### Item 3's table, re-run under BOTH guards after the fix

```
lbl author  subject    attribute          visibility               owner      owner_role  rule
D1  maya    maya       appointment        member-private           maya       maya        5-fallback
D2  maya    maya       medication         member-private           maya       maya        5-fallback
D3  sam     household  schedule           household-circle-shared  household  sam         3a-attribute-household
D4  sam     dad        incident           member-private           sam        sam         5-fallback
D5  sam     dad        medication_status  member-private           sam        sam         5-fallback
D6  sam     sam        preference         member-private           sam        sam         5-fallback
D7  sam     household  household          household-circle-shared  household  sam         3a-attribute-household
D8  sam     dad        risk_pattern       member-private           sam        sam         3c-mandatory-exclusion-narrowed
D9  maya    ray        medication         pair-private             maya       ray         3c-mandatory-exclusion-pair
D10 sam     household  address            household-circle-shared  household  sam         3a-attribute-household
D11 sam     household  zone_district      household-circle-shared  household  sam         3a-attribute-household

11 construct, 0 REFUSED
ALL FOUR ONBOARDING SCOPES UNCHANGED: True
```

**Look at D3/D7/D10/D11's three columns together** — `author=sam`, `owner=household`,
`owner_role=sam`. Provenance and custody are carried by different fields at the same time,
which is what "author is not scope" means concretely.

## 5. ITEM 4 — THE LEGACY D8 ROW SUPERSEDED, BY EXACT ROW IDENTITY

Addressed by **fact_id AND elementId together**, never by a semantic query, with a
pre-flight assertion that the target resolved to exactly one ACTIVE row and a post-condition
that exactly one row was touched.

| | |
|---|---|
| **Row superseded** | `fact_id 2b408ded-796e-4a94-958c-c5bb1824a3b1`, `elementId 4:6bf883f2-…:26` |
| **Reason recorded** | *"superseded: malformed legacy author/custody state — authored as the literal household scope marker, sealed member-private with owner='household' (TD-R-171). Corrected by re-derivation, HA-18/HA-19."* |
| **Replacement row** | `fact_id 932b4b45-f702-4089-8666-de7e04dcfd86` (`owner=sam`, member-private, 2 parents) |
| **Before active census** | **17 ACTIVE — 16 OK / 1 FAIL** (the FAIL is this row, `InvalidToken`) |
| **After active census** | **16 ACTIVE — 16 OK / 0 FAIL** |
| **Ledger continuity** | **UNCHANGED** — chain verify PASS, 10101 events both times, file sha256 `975cd74f…` **byte-identical**, last-entry sha `694962cc…` identical |

**NOT deleted, and its malformed state NOT rewritten.** Post-supersession the row still
reads `owner='household'`, `audience_policy='member-private'`, ciphertext intact — that
disagreement IS the history the supersession records as corrected. Only the three lifecycle
fields changed, and they are the same three `memory_engine/store.py`'s own supersede path
writes (`valid_to` / `closed_reason` / `superseded_by`), so no new lifecycle convention was
invented for this.

**One honest note about what this record survives.** A `--full` run resets the graph
(`fixture.reset()` → `demo_reset --yes` → re-seed), so the superseded row is gone from the
graph after §9's runs. It was the right repair for the graph as it stood, its evidence is
here and in the encode audit log, and after a from-scratch seed the legacy row cannot exist
at all — §7 shows C1 clean by construction rather than by repair.

## 6. ITEM 5 — ACTIVE CENSUS CLEAN

**16 ACTIVE rows, 16 OK, 0 FAIL, no `InvalidToken` anywhere**, read back through the real
`decrypt_fact_value_for_caller` path as each row's stamped owner — not through a test-only
shortcut.

## 7. ITEMS 6 + 7 — BOTH GUARDS LIVE

**Guard B — AUTHOR VALIDITY at `partition_crypto.classify_write`.** One site, verified as
the canonical pre-seal boundary for all four producers (`store.encode`, `consolidate`,
`extraction_queue._write_one`, `seal_pair`). **Positive membership against the enrollment
registry**, fail-closed on an unreadable registry. Refusals to
`logs/custody/refusals.jsonl`, fsynced, **never carrying the refused value**.

**Guard A — the `(visibility, owner)` same-key-holder assertion in
`WriteClass.__post_init__`.** Local and structural; **it never consults enrollment**, because
that is not knowable locally and a second copy of the membership check would drift from the
first. C4's household reading governs: `WriteClass(household-circle-shared, "household")`
stays legal.

### Full seed from scratch, under both guards

```
D1 … D11   11/11 fact(s) seeded.
```

### C1 on the from-scratch graph

```
C1 FROM-SCRATCH: 11 ACTIVE rows — 11 OK / 0 FAIL
  dad/risk_pattern  owner=sam  aud=member-private  parents=2   OK
  household/{address,household,schedule,zone_district}  owner=household   OK ×4
  maya/{appointment,medication} owner=maya  ·  ray/medication owner=maya  ·  sam/preference owner=sam
```

**C1's 11/11 is met for the first time since TD-R-171 was filed.**

## 8. THE BLAST RADIUS — SIX PLACES THAT WROTE AS NOBODY

AUTHOR VALIDITY turned up **test fixtures across four files** that authored as ids existing
in no registry. Every one is fixed the same way, and the principle is worth stating once:

> **ENROL THE PRINCIPAL; DO NOT EXEMPT THE TEST.** A guard that ignores ids which look like
> fixtures would make the harness prove the behaviour of a system with its custody check
> disabled — not the system being shipped — and would hand any future caller a naming
> convention that bypasses author validation.

| file | what wrote as nobody | fix |
|---|---|---|
| `eval/test_sensitivity_no_default.py` | `_snd_w_*`, `_snd_r_*` | enrol in fixture, de-register in teardown |
| `eval/memory_harness.py` | 8 × `memtest-*` (MEM-108/109/110/111/113/115) | `_mint_principal()` mints **and enrols**; `_retire_principals()` in the existing key-hygiene teardown |
| `eval/harnesslib/layer7_crypto.py` | `ob4_probe_owner`, `psa1_probe_owner`, `ctxstrip_probe_owner` | `enrol_probe_author()` |
| `eval/harnesslib/layer7_crypto_v2.py` | `_sc1_superseded_owner` | `enrol_probe_author()` |

New shared helper `eval/harnesslib/principals.py` — deliberately **not** named `test_*`, so
pytest does not collect it and the battery manifest does not demand a `run_harness.sh` row
for a helper.

### Two tests that pinned D8's defect as expected behaviour — INVERTED

`eval/test_ceiling_audience.py`'s two A11 D8-shaped tests asserted that
`WriteClass(member-private, owner='household')` was constructible, that `encrypt_by_class`
succeeded on it, and — explicitly — that this was fine because *"member_registry has no row
for the 'household' pseudo-id; ensure_member_seal_keypair generates and persists a keypair
file for it on first use … for ANY member_id, real or not."*

**They described the mechanism of TD-R-171 and called it working.** The keypair they
confirmed was being minted is the member key D8's DEK sealed to, while the node's
`owner='household'` sent the read path to the household tree. They were not wrong about what
the code did; they were wrong that it was acceptable — **"it encodes without error" was never
evidence that it could be read.**

Same inputs, opposite expectation, plus an anti-vacuity case proving the legitimate household
write still lands. Old text preserved verbatim in the file's comments per the
annotate-never-silently-patch rule.

### `eval/harnesslib/fixture.py` — SEED_FACTS' owner is now COMPUTED

`_key_facts` matches `MATCH (f:Fact {owner: $own})` and decrypts as that owner, so
`SeedFact.owner` always had to be the **stamped** owner. Until now that was indistinguishable
from the fixture's column 2, because every fixture's author happened to equal its stamped
owner. **D3/D7/D10/D11 broke the coincidence correctly** — author `sam`, stamped owner
`household`. Reading column 2 would have sent the harness hunting `owner="sam"` rows that do
not exist. It is now computed through the same classifier the write goes through, which keeps
the module's stated "single source of truth" contract true across a *classifier* change and
not merely a *fixture* change. A new `author` field carries provenance separately.

## 8A. ONE NAME, TWO MEANINGS — why this defect was so easy to write

Worth stating plainly, because it explains why D8 stayed broken for two weeks and why item
3's check was needed at all.

**`encode()` takes a parameter called `owner`, and that parameter is the AUTHOR.** Then, part
way through, the write path does:

```python
write_class = partition_classify_write(owner=owner, …)
owner = write_class.owner          # <-- the SAME NAME now means the stamped scope marker
```

**One local variable carries provenance on the way in and custody on the way out.** The
classifier's own docstring already admits it — *"``owner`` is AUTHOR … kept under this
parameter name for backward compatibility"* — and `role_resolution.py` documents why. But a
reader of `demo_seed.py` sees a column called `owner`, writes `"household"` into it meaning
*the household owns this*, and has in fact declared *the household said this*. That is D8,
exactly.

**Not renamed here.** The rename touches every caller of `encode`, `classify` and
`classify_write` and belongs in its own dispatch with its own acceptance; doing it inside a
custody build would mix a large mechanical change into a small semantic one. **What landed
instead is the comment at `FIXTURES`' definition naming field 2 as the AUTHOR and stating
that custody is computed, never declared** — so the next person to add a fixture is not
invited to make the same mistake.

## 9. ITEM 8 — ACCEPTANCE, EXECUTED

| Clause | Result | Evidence |
|---|---|---|
| **C1** census clean post-supersession | **PASS** | 16/16 after supersession (§5–6); **11/11 from scratch** (§7) |
| **C2** fresh derived member-private write, consistent, readable | **PASS** | live: `owner=sam`, `audience_policy=member-private`, `derived=True`, 2 parents, **same key-holder = True**, reads back `'HA-19 C2 probe: derived pattern'` |
| **C3** inconsistent construction refused AND recorded | **PASS** | both directions refused; record written with `reason=visibility_owner_disagree`, **no value in the record** |
| **C4** household-scope write still lands | **PASS** | `WriteClass(household-circle-shared, "household")` legal; 4 household facts land household-scope in the live seed |
| **C7** negative twin | **PASS** | see below |
| **item 3** provenance-not-scope | **PASS** | §4's table — all four unchanged, `owner_role` carries provenance |
| **D8's four fields** | **PASS** | `author=sam` · `subject=dad` · `audience=member-private` · `derived_from=D4+D5` |

### C7, proven by absence rather than by exception

```
before: total=23 active=16 derived=3 refusals=21
after : total=23 active=16 derived=3 refusals=22
raised           : InvalidAuthor
no new node      : True        no new active : True
no derived child : True        refusal recorded: True
rows tagged ha19-c7 on the graph: 0
```

**An exception reaching the caller is consistent with a write that already sealed**, so the
test also spies on `encrypt_by_class` and asserts it was never reached — no DEK is produced
for a refused author. Seven parametrized authors (`household`, `care-team`, `member-private`,
`pair-private`, `""`, `None`, `nonexistent_person`) are all refused, and an enrolled
principal is accepted, so the guard is not vacuously refusing everything.

**Registered as a standing battery: `eval/test_derived_write_custody.py`, 29 tests**, wired
into `run_harness.sh`. A custody invariant proven once in a dispatch is proven for one
commit; this failure mode is silent and has already happened once.

## 10. ITEM 9 — RUNS

| Run | Result |
|---|---|
| **Full seed from scratch, both guards live** | **11/11 seeded** |
| **Batteries** | **850 passed, 1 skipped, 9 xfailed** (HA-14: 820) |
| **`--layer 7`** | **L7 27/27 · L7V2 27/28 (1 skip) · DISC 1/1 · SCHEMA 1/1 · VOICE 1/1 · AUDIT 8/8** |
| **RATCHET** | **PASS — no scenario regressed vs baseline** |
| **Memory harness** | **13/17 — INSIDE THE PIN** (13–15/17). Same four as HA-14: MEM-115/116/117/118 |
| **`--full`** | **RAN TO COMPLETION — Layer 2 no longer aborts.** **RATCHET FAIL**; three reds, all attributed in §10.1, one of them fixed here |

**The memory harness went 8/17 before the enrolment fix and 13/17 after** — six scenarios
(MEM-108/109/110/111/113/115) were red purely because they wrote as unenrolled principals.
Teardown confirmed live: `destroyed 7 fixture seal key(s)`, `de-registered 8 synthetic
principal(s)`.

### The one red, attributed rather than assumed

`eval/test_key_hygiene.py::test_zzz_no_fixture_keys_survive_the_suite` fails **when the
batteries are run immediately after a layer-7 run**, on 8 keys named
`_sc1_superseded_owner`, `ob4_probe_owner`, `p4*`, `psa1_probe_owner`.

**Verified pre-existing, not caused by HA-19: the identical failure with the identical 8 keys
reproduces with every HA-19 change stashed.** Re-run after a sweep, the batteries are
**850 passed, 0 failed**. The invariant is asserting "no fixture keys survive the suite"
against keys left by a *different process* — the cross-process ordering defect whose
relocation is **HA-20's**, exactly as this dispatch scopes it. The new custody battery mints
no keys (14 before, 14 after).

**IT IS WORSE THAN AN ORDERING WART, AND HA-20 SHOULD KNOW BEFORE IT STARTS: THIS BLOCKS THE
RATCHET.** `run_harness.sh` gates the harness behind the batteries, and every layer-7 run
leaves those 8 keys behind — so **`--full` cannot be run twice in a row.** The second
invocation aborts at the battery gate before the harness starts, and a manual
`sweep_stale_test_keys()` is required between runs. Discovered here by doing exactly that
(§10.1's second `--full` died at the gate with `1 failed, 850 passed`). Item 12 says a fix is
not done until the full ratchet passes; **right now the full ratchet cannot even be re-run
without hand intervention**, which makes the relocation a prerequisite for item 12 rather
than tidy-up.

### 10.1 `--full` — IT RAN TO COMPLETION, AND THE RATCHET FAILED

**`--full` reached the end for the first time since TD-R-171 was filed. Layer 2 did not
abort.** Item 12 is satisfiable again — a dispatch can now be held to the full ratchet.

**And the first thing the full ratchet did was fail.** Reported before the good news, because
that is the order that matters:

```
== L1: 12/15  == L2: 24/35 (10 skipped)  == L3: 3/3  == L4: 30/34 (4 skipped)
== L6: 1/1    == L7: 27/27  == L7V2: 27/28  == DISC/SCHEMA/VOICE 1/1  == AUDIT 8/8
RATCHET FAIL — regressed vs baseline: ['L1:P9', 'L2:routing_showcase.T04']
NEW FAILURES (not in baseline): ['L1:P12']
```

**This is exactly what item 12 exists for: three reds that no targeted proof would have
found, surfaced only because `--full` could finally run.** Each is attributed below by
mechanism, not by assertion.

#### L1:P9 — a REAL regression. Cause proven, FIXED here.

Checks 3a/3b/3c all reported `got=None`. The probes call `_coerce_fact` on dicts carrying
`confidence` but **no `sensitivity` key** — and D-R-196's ruling ("a fact with no sensitivity
label is refused at every boundary, not stamped medium") makes `_coerce_fact` return `None`.
Proven directly:

```
P9 probe dict AS WRITTEN (no sensitivity key): None
same dict + sensitivity=low            : {… 'confidence': 'medium' …}
```

**The probes were measuring the sensitivity boundary and never reaching the confidence clamp
they exist to test.** A `sensitivity` label is added to all three; its value is irrelevant and
deliberately not the thing under test. **L1 re-run: P9 PASS, all nine checks green, L1 14/15.**

**This is a D-R-196 regression, not an HA-19 one — and it had been invisible because `--full`
could not complete.** HA-19 did not cause it; HA-19 is why it is visible.

#### L1:P12 — NOT in the baseline, and its two failing checks CANNOT PASS

`L1:P12` has no baseline entry at all (the baseline carries P1–P10 and HARNESS1.x; P11 and
P12 postdate it), so the ratchet reports it as new rather than regressed.

Its `u1b` and `u5` assert on `e.get("payload", {}).get(...)`. **`iter_events` returns no
`payload` key on these events at all:**

```
identity.rejected events: 220
keys on the event: [actor, correlation, event_id, event_type, hash, hel,
                    keyed_commitment, prev_hash, seq, ts, …]
has plaintext payload? False      payload_enc present? False
```

So both checks evaluate `{}.get(...) → None` and are **structurally incapable of passing,
whatever the code does** — the events ARE being written, 220 of them; the probe simply cannot
see inside them. That is the inverse of the anti-vacuity problem: a check that can only be
red. **NOT fixed here** — the repair is in ledger-payload territory, not custody, and this
dispatch is not going to grow a second subject. Named precisely so it can be picked up.

#### L2:routing_showcase.T04 — REPRODUCED, deterministic, and NOT mine

```
[FAIL] required 'cable' present — reply="It's 2:06 PM PDT in La on Friday, August 7."
[FAIL] tier edge — got escalate
```

A live news query answered with **the clock**. Re-run standalone and it reproduces, with the
time advancing between runs — a live routing/tool-selection failure, not a flake.
`routing_showcase.T01–T03` pass on the same live path. **HA-19 touched no routing, model,
search or tier code.** Reported as an open RATCHET FAIL; **this dispatch does not claim to
have fixed it and does not claim the ratchet is green.**

#### `--full` re-run with the P9 fix — P9 CONFIRMED FIXED, and a fourth red appears

```
== L1: 13/15   == L2: 24/35 (10 skip)  == L3: 3/3   == L4: 30/34 (4 skip)
== L6: 0/1     == L7: 27/27  == L7V2: 27/28  == DISC/SCHEMA/VOICE 1/1  == AUDIT 8/8
RATCHET FAIL — regressed vs baseline: ['L2:routing_showcase.T04']
NEW FAILURES (not in baseline): ['L1:P12', 'L6:record-invariants']
```

**P9 is off the regression list — the ratchet's only remaining REGRESSION is T04.** L1's
other two reds are P12 (never baselined, §above) and **P2, which the baseline records as
`False` — it is expected to fail and is not a regression.**

**L6:record-invariants is new in this run and was PASS in the first `--full`.** It is not in
the baseline either. The violation:

```
G1 no-orphan-generation: FAIL (1)   [HARD ZERO]
  [sam] 'I take atorvastatin 20mg every morning.'
    generated about ['sam'] with zero admitted facts about them
    -> 'I heard that as an update, but I was unable to save it to the household record just now.'
```

**A live write failed and the reply said so.** Attribution, measured rather than assumed:

- **Neither guard fired anywhere in this run** — `grep -c "InvalidAuthor|InconsistentWriteClass"` over the entire run: **0**.
- **No custody refusal was recorded for any real member.** All 171 records in
  `logs/custody/refusals.jsonl` name `household`, `care-team`, `member-private`,
  `pair-private`, `nonexistent_person`, `''`, or a `_snd_*`/`memtest-*`/`ob4_*` test id from
  before its enrolment fix. **Not one names `sam`, `maya` or `bill`.**
- The only change between the passing run and this one was adding a `sensitivity` label to
  three P9 parse probes — which cannot reach a live Sam turn about atorvastatin.

**So the custody guards did not cause it.** What did is not visible in this log, and this
dispatch does not guess: **G1 is a HARD ZERO invariant about ungrounded generation, and one
observation in two runs is not a characterisation.** A third `--full` is running for a third
data point; its result is recorded in §10.2.

### 10.2 THREE `--full` RUNS — AND THE LAST TWO HAVE IDENTICAL CODE

The third run was for L6's third data point. It produced something more useful than that.

| | run A (pre-P9 fix) | run B | run C |
|---|---|---|---|
| **code** | — | **identical to C** | **identical to B** |
| batteries | 850 | 850 | 850 |
| **L1** | 12/15 | 13/15 | **14/15 (2 flaked)** |
| L2 | 24/35 | 24/35 | 24/35 |
| **L3** | 3/3 | 3/3 | **1/3** |
| **L4** | 30/34 | 30/34 | **29/34 (2 flaked)** |
| **L6** | 1/1 | **0/1** | 1/1 |
| L7 · L7V2 | 27/27 · 27/28 | 27/27 · 27/28 | 27/27 · 27/28 |
| AUDIT · DISC · SCHEMA · VOICE | 8/8 · 1/1 · 1/1 · 1/1 | same | same |
| **RATCHET regressions** | `L1:P9`, `L2:T04` | `L2:T04` | `L2:T04`, `L3:INJ-3`, `L3:INJ-7`, `L4:PW019` |
| NEW (unbaselined) | `L1:P12` | `L1:P12`, `L6` | `L1:P12` |

**Runs B and C differ by nothing. Not one byte.** And they disagree on L1, L3, L4, L6 and on
the ratchet's regression list itself.

> **THE FINDING: `--full`'s live-model layers are NOT REPRODUCIBLE RUN TO RUN, and the
> RATCHET over them therefore is not either.** The harness says so itself — run C reports
> **"2 flaked"** in L1 and L4. L3 swung 3/3 → 1/3 with no code change; L6's `G1` swung both
> ways; run C invented two INJ regressions that run B did not have.

**This matters more than any single red, and it is worth being blunt about: Requirements
Discipline item 12 says a fix is not done until the full ratchet passes — but a ratchet that
returns a different answer each time cannot carry that weight.** Item 12's guarantee is
currently only as strong as its deterministic layers.

**What IS stable across all three runs:**

- **`L7 27/27`, `L7V2 27/28`, `AUDIT 8/8`, `DISC/SCHEMA/VOICE 1/1`, batteries `850`** —
  every deterministic layer, identical every time. **The custody work lives in these**, and
  they do not move.
- **`L2:routing_showcase.T04`** — red in all three, plus twice more standalone. **The one
  genuinely stable regression**, and it answers a news query with the clock.
- **`L1:P12`** — red in all three; never baselined; its two checks cannot pass (§10.1).

**What is NOT stable: `L1:P9` (fixed — green in B and C), `L3:INJ-3`, `L3:INJ-7`,
`L4:PW019`, `L6:record-invariants`.** Each appears in one run and not the others.

**Neither guard fired in any of the three runs** (`grep -c "InvalidAuthor|InconsistentWriteClass"`
= 0 in each), and no custody refusal names `sam`, `maya` or `bill`. **The intermittent reds
are not the custody guards.**

**HONEST BOTTOM LINE ON ITEM 12: `--full` completes again, which it could not before, and it
FAILS. One stable regression (T04), one impossible unbaselined check (P12), and a set of
intermittent reds that a code-free re-run reshuffles. This dispatch does not claim a green
ratchet, and does not claim the intermittency is new — it claims only that it is now visible,
because `--full` can finally be run more than zero times.**

## 11. FINDINGS

1. **Rule 3a derived scope from the author** (§3–4) — the conflation the clause forbids,
   living in the classifier. Corrected to key on the subject; **the single judgement call in
   this dispatch, flagged in §4 and reversible in one commit.**
2. **C1 is 11/11 for the first time** (§7). The write path, the fixture, and the graph agree.
3. **Six fixture sites across four files wrote as nobody** (§8) — enrolled, not exempted.
4. **Two tests had pinned TD-R-171's mechanism as correct behaviour** (§8) and are inverted.
5. **`SEED_FACTS.owner` was silently relying on a coincidence** (§8) — author == stamped
   owner for every fixture, until household facts got a human author.
6. **The key-hygiene red is pre-existing and cross-process** (§10), proven by stashing.
7. **`--full` COMPLETES AGAIN — and its ratchet is RED** (§10.1). Failures no targeted proof
   would have found. **L1:P9 was a real D-R-196 regression, invisible until now, diagnosed
   and FIXED here** — it is off the regression list. **The only remaining REGRESSION is
   L2:T04**, which answers a news query with the clock, reproduces deterministically, and
   lies outside everything HA-19 touched. L1:P12's two checks assert on a `payload` field the
   event reader does not return and **cannot pass whatever the code does**;
   L6:record-invariants went red in one run of two and **neither guard fired anywhere in that
   run**. Neither is in the baseline. **THE RATCHET IS NOT GREEN AND THIS DISPATCH DOES NOT
   CLAIM IT IS** — what it claims is that `--full` can be run at all again, which it could
   not before, and that every red is attributed by mechanism rather than by assertion.
8. **`--full`'s LIVE-MODEL LAYERS ARE NOT REPRODUCIBLE** (§10.2) — **two runs with
   byte-identical code disagree on L1, L3, L4, L6 and on the ratchet's own regression list.**
   Item 12 leans on a ratchet that currently answers differently each time. Every
   DETERMINISTIC layer (L7 27/27, L7V2 27/28, AUDIT 8/8, DISC/SCHEMA/VOICE, the 850
   batteries) is identical across all three runs — **and that is where the custody work
   lives.**
9. **One side effect this dispatch introduced, named rather than left to be found:** enrolling
   `_sc1_superseded_owner` makes `read_user_facts` return the household-scope rows to it, and
   it holds no household key wrap — so the run logs `decrypt failed … skipping` tracebacks
   for those rows. **Caught and skipped by design, SC1 still PASSES**, but it is new log noise
   with HA-19's name on it. The clean repair is to provision the household wrap for enrolled
   probe principals (the pattern `layer7_crypto_v2`'s P4 fixture already uses via
   `assign_member_to_household`); deliberately not done here to keep the enrolment helper
   minimal.

### Two things found while building, neither in scope, both worth Bill's eye

7. **`encode()` accepts an unrecognized `write_state`, writes NOTHING to the graph, and
   still emits a success audit record and an `EncodeResult` with a fresh `fact_id`.** Found
   while building C2 with `state="new"`: the lifecycle block handles `supersede`, `augment`,
   `correct` and `unresolved` with no `else`, so an unknown state falls through every branch
   silently. Two audit lines in `logs/memory_engine/encode_audit.jsonl` claim writes that do
   not exist. **This is a silent-data-loss shape on the write path** — the same class as
   TD-R-171, arriving by a different route. Pre-existing, untouched, **not filed as a TD
   because production-code TDs are not on the pre-authorized list.**
8. **No `author` property is persisted on the Fact node.** The graph stamps only the computed
   `owner`; provenance is enforced at write time and then **not retrievable from the row**.
   AUTHOR VALIDITY makes the author meaningful — "who said this?" is now a question the
   system validates but cannot answer after the fact.

## 12. WHAT THIS DISPATCH DOES **NOT** RULE

**`REQ_DERIVED_WRITE_CUSTODY` is NOT marked MET here.** Every acceptance clause has executed
and passed with evidence above; **that is a readiness report, and Bill rules.** Item 10's
per-clause table is §9.

**NOT IN THIS DISPATCH, per its own scope:** the zero-orphan invariant relocation and the
four teardown wirings — **HA-20**.
