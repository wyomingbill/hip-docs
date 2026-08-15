# DISPATCH_TDR171_ROOT_CAUSE — the seal class and the read class disagree on the one derived fact

Status: BUILT
Reconciled-Against: roadmap `9ffc87c` (pre-dispatch HEAD)

**HA-09** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **ANALYSIS + STOP**
**REQ: NONE** — item 1 is a diagnosis; no code change is authorized by its own terms unless
the fix is a one-commit revert or a config restore. It is neither (§2).
**NOTHING RULED MET. NOTHING DELETED. NO CODE CHANGED.**

---

# STOPPED AT SEGMENT 3 — NEEDS BILL

Item 1 (the main job) is **COMPLETE**: the root cause is found and is sharper than a commit
hash. **Item 3 is a STOP on a destructive action whose authorized scope does not match what
is on disk** (§3). Items 2 and 4 were not started — §5 says why.

---

## 1. ITEM 1 — TD-R-171 ROOT CAUSE, FOUND

**Starting from HA-08's evidence, not re-deriving it** (household.seal.key untouched since
Aug 5; row household-sealed at `sensitivity=high`).

### The bisect that wasn't needed, and what replaced it

A git bisect was never reached, because a **decrypt census across every active fact** located
the boundary in one run and located it more precisely than a commit could:

```
valid_from                   owner        subject  attribute      decrypt
2025-06-28T00:30:57.170565   household    househo  schedule       OK
2025-06-28T00:30:57.170565   household    househo  household      OK
2026-01-06T00:30:57.170565   maya         maya     medication     OK
2026-02-08T00:30:57.170565   household    househo  address        OK
2026-02-08T00:30:57.170565   household    househo  zone_district  OK
2026-02-27T00:36:22.128063   maya         ray      medication     OK
2026-05-03T00:30:57.170565   sam          sam      preference     OK
2026-07-04T00:30:57.170565   maya         maya     appointment    OK
2026-07-25T00:30:57.170565   sam          dad      medication_st  OK
2026-07-28T00:30:57.170565   sam          dad      incident       OK
2026-07-30T00:30:57.170565   household    dad      risk_pattern   FAIL InvalidToken
```

**Exactly one fact fails, and four OTHER household-owned facts decrypt fine.** That kills
the household-key-rotation hypothesis outright: a rotated household key would break all
five, not one.

**A hypothesis this dispatch formed and then discarded on its own evidence:** the D8 row's
`valid_from` of 2026-07-30 first looked like a week-old row surviving re-seeds. It is not —
every row shares the timestamp `00:30:57.170565`, so the dates are **fabricated by
`demo_seed.py`** and all eleven were written in the same seed run. Recorded because the
wrong reading was momentarily persuasive.

### What is actually different about D8

```
recorded_at                  owner      subject attribute     flags
2026-07-30T00:30:57.170565   household  dad     risk_pattern  derived=True  aud=member-private
   (every other active fact)                                  derived=False aud=None
```

**D8 is the only `derived=True` fact and the only fact carrying an `audience_policy` — and
that policy is `member-private` while the row's `owner` is `household`.**

`memory_engine/store.py:241` stamps `audience_policy` **only** on derived writes
(`audience_policy if derived_lineage else None`), taking it from the computed write class.

**So the seal and the read disagree, structurally:**

| | follows | value for D8 |
|---|---|---|
| **How the DEK was sealed** | `write_class.visibility` | `member-private` → wrapped to a member key |
| **How the read dispatches** | `owner` | `household` → `decrypt_fact_value_for_caller` routes to the household key tree |

The exact failure, captured live:

```
harness/partition_crypto.py:211  decrypt_fact_value_for_caller
harness/household_keys.py:421    decrypt_fact_value_for_household
harness/dyad_crypto.py:126       unseal_from_privkey  ->  cryptography.fernet.InvalidToken
```

**A member-private-sealed DEK is being unsealed with the household private key.** It cannot
work, and it fails for exactly the one write path that can produce the mismatch.

### The smallest honest fix — and why this dispatch does not build it

Item 1 authorizes a build **only** if the fix is one commit's revert or a config restore.
**It is neither.** The candidates are all larger:

1. **Make the derived write path agree with itself** — if `write_class.visibility` is
   member-private, the row's `owner` must be that member, not `household` (or vice versa).
   That is a change to the write-class → seal/owner contract, and it touches every derived
   write, not one seed row.
2. **Make the read dispatch on `audience_policy` when present** rather than on `owner`
   alone — a change to `decrypt_fact_value_for_caller`'s dispatch, on the live read path.
3. **Re-seed just D8** — the smallest of the three, but it is a **graph delete**, which
   CLAUDE.md's NOT-pre-authorized list names explicitly, and it treats the symptom: the next
   derived seed writes the same mismatch again.

**FINDINGS ONLY. This needs Bill**, and the choice between (1) and (2) is a design ruling
about which field is authoritative for sealing, not a repair a session should pick.

**Consequence, unchanged from HA-08:** Requirements Discipline **item 12 remains
unsatisfiable by any dispatch** until this clears.

## 2. ITEM 3 — STOP: the authorized scope does not match the disk

Item 3 authorizes deleting **"the 18 test-generated `*.seal.key` files"**, and requires the
list to appear here **before** any deletion. The list was produced first, and it does not
match the authorization:

| Family | Count | Provably test-generated? |
|---|---|---|
| `p4principal_*`, `p4admin_*`, `p4peerb_*`, `p4peera_*`, `p4lost_*` | **802** | yes — P4 quorum/custody fixtures |
| `memtest-108/109/110/111/113/115-*` | **525** | yes — the memory harness's own fixtures |
| `_snd_*`, `_snd_r_*`, `_snd_w_*` | **20** | yes — D-R-196 / HA-02 / HA-06 batteries |
| `p4smoke_*`, `p4peer_*`, `psa1_*`, `ob4_probe_owner`, `_sc1_*`, `_probe_*` | **~13** | yes |
| `alice`, `bill`, `bob`, `maya`, `sam`, `household` | **6** | **NO — real registry members. Must not be deleted.** |
| **TOTAL `*.seal.key`** | **1368** | |

**Two mismatches, either one sufficient to stop:**

1. **The count HA-08 reported as 18 is now 22.** HA-08 counted `_probe_`+`_snd_` at 18; this
   dispatch's own batteries (spend-ledger, offer-instance) created four more at 18:30 while
   the dispatch was being written. **The authorized set changed size between the
   authorization and the execution** — which is precisely when a destructive instruction
   should be re-confirmed rather than interpreted.
2. **The real test-generated population is ~1362, not 18** — roughly 75× the authorized
   number. Deleting on the *category* rather than the *count* would mean destroying 1,362
   key files under an authorization that named 18.

**NOTHING WAS DELETED.** Key destruction is on CLAUDE.md's NOT-pre-authorized list, and
"delete the 18" cannot be stretched to "delete 1,362" by a session. The two readings need
Bill's word:

- **(A)** delete only the 22 `_probe_`/`_snd_` files this session's batteries created; or
- **(B)** delete all ~1,362 test-generated files, sparing the 6 real members.

**The teardown half of item 3 was also not built**, because writing cleanup into the
batteries before the disposition of the existing files is settled would leave the repo in a
half-state across a ruling. It is a small, non-destructive change and is ready to do on the
word.

## 3. ITEMS 2 AND 4 — NOT STARTED

Both are cheap and independent (TD-R-170's closure is a one-row register edit citing Bill's
2026-08-06 audibility confirmation; TD-159 is a mechanical rename in
`eval/test_lineage_block.py` and `eval/test_sensitivity_registry.py` onto the
`test_ceil_a<N>_*` convention). **They were not started** because item 3 stopped the
dispatch and landing riders around an open destructive ruling would split this work across
two commits for no benefit. They are ready to run as a single follow-up.

## 4. RUNS

**None.** No code changed, so `--layer 7`, RATCHET and the memory harness would re-measure
`9ffc87c` — already recorded at HA-08 (battery 812+1 skipped, L7 27/27, RATCHET PASS,
memory 13/17). **`--full` was not re-run**: item 7 conditions it on item 1's fix landing,
and no fix landed. **Item 12 remains NOT satisfied** (§1).

## 5. A CONFLICT WITH THE STANDING LAW, FLAGGED NOT BYPASSED

Item 8 says to **open the dispatch file itself** on completion. CLAUDE.md's routing rule
says: *"NEVER `open -e`. Never ask Bill to copy out of TextEdit. That route FAILS: the copy
arrives blank."* — a rule earned at D-118 and D-136.

Workflow item 5 says: on conflict with the law, **flag it and follow the law**. So this
dispatch prints the path and does not open the file in TextEdit. If the intent was simply
to have it on screen and the D-118 failure mode no longer applies, say so and it will open
next time.

## 6. FINDINGS

1. **TD-R-171's root cause is a seal-class/read-class disagreement on the derived write
   path** (§1) — not a key rotation, not a stale row, not D-R-196.
2. **Item 3's authorized scope is 75× smaller than the disk reality, and the authorized
   count moved between authorization and execution** (§2). Nothing deleted.
3. **1,368 seal keys exist, 6 of them real members.** Whatever is decided, the six must be
   spared by name, not by pattern.
