# DISPATCH_HA32_P12_HEL2 — P12 rewritten to the HEL 2.0 contract; twins proven; P12 clears the ratchet
Status: **COMPLETE WITH FINDINGS**
Reconciled-Against: roadmap `5fa9d9c` (baseline of record remains `1260f3e`)
Filed: 2026-08-10 (HA-32)
Decision-Owner: Bill
TYPE: TEST CHANGE ONLY. **No product code touched. No claim moves. Nothing ruled MET.**

## BILL'S RULING ON HEL 1.0 — 2026-08-10, VERBATIM

> Keep them. Relabel them. Do not retire them. HEL 1.0 tests are legacy-format compatibility
> tests only. They may verify the frozen historical HEL 1.0 records and reader compatibility, but
> they do not participate in P12 acceptance, the HEL 2.0 requirement result, or the current
> ratchet gate. They must be clearly labelled legacy and may not be cited as evidence for
> current-format compliance.

**FINDING ON ITEM 6: the ruling has no target in `layer1.py`.** `grep -n 'get("payload"'` over
the file returns **nothing** after the rewrite — u1b and u5 were the only HEL 1.0 payload readers
there, and both are now HEL 2.0. **No test was relabelled because none remained to relabel.** The
ruling stands for any HEL 1.0 test found elsewhere; none was found in this file. Nothing was
retired.

## ITEMS 1–4 — THE IMPLEMENTATION

`eval/harnesslib/layer1.py`, test-side only. A helper `_hel2_contract(ev, want)` now enforces the
full contract for one identity event, and `_hel2_key_id(ev)` re-derives the key context **from
the event's own `actor`, by the writer's rule** (`epistemic_ledger.py:501-502`):

```python
a = ev.get("actor") or {"kind": "system", "id": "unknown"}
return str(a["id"]) if a.get("kind") == "member" and a.get("id") else "system"
```

**Never hardcoded** — a literal `"identity_gate"` or `"system"` would test today's fixture, not
the contract. The comment in the code says so, so a later edit cannot quietly reintroduce it.

`_hel2_contract` checks, in order: `hel == "2.0"`; `keyed_commitment` present and non-empty; none
of `payload`/`payload_enc`/`payload_kid`/`payload_sha256` on the event; the off-ledger payload
readable via `load_payload(event_id, member_id=<derived>)`; the expected fixture metadata
recovered; and `compute_keyed_commitment(payload, key=_load_or_create_member_key(kid))` equal to
the event's `keyed_commitment`.

- **u1b** → `identity.rejected`, expecting `source="voice-query"`, `reason="missing"`.
- **u5** → `identity.speaker_mismatch`, expecting `verified_member="bill"`,
  `speaker_id_hint="maya"`.

Both perform the **full round trip including commitment verification**, per item 4.

## ITEM 5 — FAULT TWINS, ALL RED, BOTH EVENT TYPES

| twin | `identity.rejected` | `identity.speaker_mismatch` |
|---|---|---|
| **baseline (unmutated)** | **PASS** — contract satisfied, `key_id='system'` | **PASS** |
| commitment **removed** | **RED** — "keyed_commitment absent or empty" | **RED** |
| commitment replaced by **raw SHA-256** | **RED** — "does not verify against the recovered payload" | **RED** |
| **HEL 1.0 field reintroduced** (`payload_sha256`) | **RED** — "forbidden HEL 1.0 field(s) on a 2.0 event" | **RED** |

**The check passes on real events and fails on every mutation — it is a check, not a formality.**
Twins ran on **deep copies**; no ledger record was mutated, so there was nothing to restore and
the hash chain was never at risk.

## ITEMS 7–8 — RUNS, AND WHAT P12 DID

| command | result | vs `1260f3e` baseline |
|---|---|---|
| canonical suite | **1048 passed, 31 failed, 10 skipped, 9 xfailed, 2 errors** | **IDENTICAL — no regression** |
| `--layer 7` | **exit 0** | unchanged |
| RATCHET `--full` | **RATCHET FAIL** — `NEW FAILURES: ['L6:record-invariants']` | **L1:P12 GONE** (was `['L1:P12','L6:record-invariants']`) |
| memory harness | **13/17** | inside the 13–15 pin |

**P12 now passes.** It has dropped out of the ratchet's new-failures list, leaving **L6 as the
only remaining red**, exactly as the dispatch predicted, and L6 stays under the collector rule.

**NO PASS IS CLAIMED.** The standing rule forbids calling anything PASS while a red stands, and
the RATCHET is still FAIL on L6.

**ITEM 7 — a limit, stated rather than glossed:** P12 is no longer a *failure*, so it no longer
appears in the ratchet's new-failures list. **Whether the ratchet keeps a separate baseline
registration that must also be edited was NOT verified**, and no baseline file was edited. If such
a registration exists, it is outstanding. The twins have satisfied the precondition for adding it.

## CLAIM IMPACT

**None.** Test-side only; no product code, no claim status changed, nothing ruled MET. The suite
is byte-identical to the baseline, so no claim gained or lost evidence.

## OPEN

- **L6:record-invariants** — the ratchet's only red, under the collector rule.
- **Ratchet baseline registration for P12**, if one exists separately from the failure list.
- The 31 suite failures remain as filed: TD-R-178 (19), TD-R-180 (4), TD-R-179 (1), 7 demo-lane.
