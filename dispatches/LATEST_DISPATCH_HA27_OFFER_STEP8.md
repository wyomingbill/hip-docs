# DISPATCH_HA27_OFFER_STEP8 — the governed record completed, and the authority manifest

Status: BUILT
Reconciled-Against: roadmap `275acc9` (pre-dispatch HEAD)

**HA-27** | 2026-08-10 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD + RIDER**
**GOVERNING REQ:** `REQ_OFFER_MECHANISM__…__v20260806_1625.md` — **R23** (every transition is
recorded), **R24** (proves process without becoming profile data), **R25** (cumulative
authority manifest).
**Nothing ruled MET. Fixtures only — nothing presents to a real member, nothing enabled.**

**CLAIM IMPACT: C-06, C-15** — see §7.

---

## 1. ITEM 1 — VERIFY FIRST, AND IT FOUND A GAP

Item 1 said verify, cite existing pieces, build only gaps. So the first thing run was a
measurement of HA-08's existing chain, before any code was written.

**All four terminal chains already worked** — cited, not rewritten:

```
ACCEPTED     chain=['PRESENTED', 'ACCEPTED']
DECLINED     chain=['PRESENTED', 'DECLINED']
LAPSED       chain=['PRESENTED', 'LAPSED']
INVALIDATED  chain=['PRESENTED', 'INVALIDATED']
```

**But the event carried 3 of R23's 16 fields.** Thirteen were missing:

```
event_id · offer_instance_id · principal · trigger_rule_id · trigger_rule_version
template_id · template_version · authority_delta_id · scope_before_commitment
scope_after_commitment · response_method · timestamp · policy_version
```

**That is what verify-before-building is for.** The state machine was correct and complete;
the *record* it wrote was a third of what R23 requires, and nothing had failed to reveal it,
because no check had ever compared the event against R23's field list.

## 2. THE GAP, BUILT — ADDITIVELY

`harness/spend_ledger.py` gains **one optional parameter** on `present()` and `resolve()`:
`record: dict | None`. HA-08's state machine, transitions, durability and replay are
untouched.

**The block is merged UNDER the ledger's own keys, never over them:**

```python
{**(record or {}), "event": ..., "transition": ..., "situation_id": ...}
```

**A caller cannot rewrite `transition` or `situation_id` by passing them in** — which is what
keeps the state machine's account of itself authoritative rather than advisory. A test passes
`{"transition": "ACCEPTED", "situation_id": "sit:forged"}` into a DECLINED resolve and asserts
the event still reads DECLINED with the real id, while a non-conflicting caller field lands.

`harness/governed_record.py` assembles the block. Two details that are decisions, not defaults:

- **`event_id` is deterministic**, derived from `(offer_instance_id, transition, at)` — not
  random. The ledger replays on every load, and an id that changed per replay would make the
  record **unciteable**.
- **`scope_before/after_commitment` are SORTED LISTS, not sets.** The event is serialised and
  replayed; a set has no stable serialisation, and two records of the same scope must be
  byte-identical to be *compared* rather than merely inspected.

### An absent field is recorded as absent, never invented

At the `apply_response` boundary the `Situation` object is not in hand, so
`trigger_rule_version` would have to be reconstructed. **It is left empty and present.** R4
forbids a fabricated trigger label, and a plausible-looking guess in a governed record is
worse than a blank — a test asserts the key exists and is empty.

## 3. R25 — THE MANIFEST IS DERIVED, NOT STORED

`authority_manifest_for(member, ledger, purpose=...)` replays the member's **ACCEPTED** events
and unions their deltas.

**There is no stored manifest, deliberately.** A second copy updated on each acceptance would
be a second source of truth about what a member has granted, and the two would disagree the
first time an event was replayed, backfilled or corrected. A test proves derivation by
replaying the same ledger file from disk into a fresh `SpendLedger` and asserting the manifest
is identical.

**Only ACCEPTED contributes.** Parametrized over DECLINED, LAPSED and INVALIDATED — each
resolved with a scope block deliberately attached — and the manifest comes back **empty**.
R25's sentence, as code: a non-accepted offer is not a trait, not a warning, **and not a
negative entry either.**

The manifest also carries a **per-dimension view** (`purpose`, `audience`, `retention`,
`inference`, `action`, `initiation`) so R25's own list can be read as the requirement names it
rather than as one undifferentiated set.

## 4. EVERY READ GOES THROUGH HA-26's NAMED-PURPOSE BOUNDARY

Both public reads take a `purpose` and pass it to `assert_permitted_read`. **There is no
unnamed read** — R20 permits four, and a fifth is refused at the door rather than found later
in a review. Reusing HA-26's gate rather than adding a second one keeps the four-read list in
exactly one place.

## 5. ITEM 4 — FOUR FAULT TWINS, EXECUTED

| | Twin | Result |
|---|---|---|
| **(d)** | anti-vacuity | history shows the **DECLINE**, manifest shows the **GRANT** |
| **(a)** | manifest vs accumulated deltas | **SET EQUALITY** across two acceptances |
| **(b)** | another member's view | sam's history `[]`, manifest empty, **no needle present** |
| **(c)** | unnamed / fifth purpose | **REFUSED** — 6 bad purposes, on both reads |

**(d) is first in the file.** Every absence assertion below it is worthless if nothing was
ever recorded — Ruling 5 says a decline *lives* in the control plane, not that it vanishes.

**(a) is asserted by set equality, not containment**: `manifest.granted == tokens(a) |
tokens(b)`, with the diff printed both ways on failure. Containment would pass a manifest that
granted extra.

**(c) also has its anti-vacuity twin**: all four of R20's purposes are accepted, so the gate
is not merely refusing everything.

## 6. R24 — PROVES PROCESS, WITHOUT BECOMING PROFILE DATA

Two tests, in opposite directions:

- **What it must NOT carry:** every history entry is scanned for `score`, `risk`, `trait`,
  `signal`, `count`, `rate`, `propensity`, `likelihood`, `warning`, `flag`. **The caller gets
  the events; the events do not get an opinion.**
- **What it must prove:** which offer, what words were shown (`template_id`), when, and — via
  exactly one `PRESENTED` in the history — **that no second offer occurred.**

## 7. RIDER — CLAIMS LEDGER v4, AND THE CAP IS NOW FULL

`docs/deliverables/HIP_ClaimsLedger__v4-c15-cap-full__v20260810_0848.md`. v3 marked
**SUPERSEDED** and retained unaltered; **LATEST** repointed; MANIFEST Section B and INDEX
updated.

**C-15, Bill's wording verbatim, status PROVEN — Bill 2026-08-10:**

> *"A member's decline is control state only. It never enters the household record,
> embeddings, summaries, scoring, or model context, and no acceptance metrics exist."*

Evidence: HA-26's standing battery. **This closes the gap HA-26 flagged** — Ruling 5's
isolation had no claim covering it, and now does.

**The header records the cap: 15/15 — FULL.** The governing rules say *"hard cap 15 claims —
adding one retires or justifies."* **The next claim requires a retirement, and that is Bill's
ruling, not a session's.** Recorded in the ledger itself so it is unmissable at the point of
adding a sixteenth.

**C-01..C-14 wording is byte-identical to v3**, verified column by column.

## 8. RUNS

| Run | Result |
|---|---|
| **Batteries** | **963 passed, 0 failed** (934 → 963: +29 from this dispatch) |
| **`--layer 7`** | L7 **27/27** · L7V2 27/28 · AUDIT **9/9** · DISC/SCHEMA/VOICE 1/1 · `KEY-HYGIENE-ZERO-ORPHAN` PASS |
| **RATCHET** (binding) | **PASS · exit 0** |
| **Memory harness** | **13/17 — INSIDE THE PIN** (13–15). Same four: MEM-115/116/117/118 |
| **`--full`** | §8.1 |

### 8.1 `--full` — live layers logged, no gate claim

```
batteries: 963 passed, 0 failed
== L7: 27/27  == L7V2: 27/28  == AUDIT: 9/9  == DISC/SCHEMA/VOICE: 1/1
== L1: 14/15  == L2: 24/35 (10 skip)  == L3: 3/3  == L4: 30/34 (4 skip)  == L6: 0/1
[live-layers] appended 88 scenario result(s)  (run_id=20260810T150432_275acc9)
RATCHET FAIL — regressed vs baseline: ['L2:routing_showcase.T04']
NEW FAILURES (not in baseline): ['L1:P12', 'L6:record-invariants']
BINDING TESTS PASS. LIVE-MODEL TESTS HAVE FAILURES — SEE RUN LOG.
```

**Every binding layer green; exit 0.** The three reds are live-layer and already
characterised: `L2:routing_showcase.T04` (stable — answers a news query with the clock),
`L1:P12` (never baselined; asserts on a `payload` key the reader does not return, so it
cannot pass), and `L6:record-invariants`.

**`L6` again.** Its history across seven collected runs is now:

```
FAIL  FAIL  PASS  PASS  PASS  FAIL  FAIL
```

Four red, three green, **with no code change explaining any of the transitions.** Collector
series: **seven `--full` runs, 616 rows.** Still no rule set, and none invented.

## 9. CLAIM IMPACT

**CLAIM IMPACT: C-06, C-15.**

- **C-06** — the governed record now proves *"that no second offer occurred"* directly, from
  exactly one `PRESENTED` per situation in the member's own history. **Reinforcement of an
  existing status, not a change.**
- **C-15** — added this dispatch at Bill's wording and his PROVEN. **HA-27 produced no new
  evidence for it**; C-15's evidence is HA-26's battery. Naming it records that the claim now
  exists.

**No claim covers R23/R24/R25 themselves** — the governed record's completeness and the
manifest's exactness. **And the cap is now full at 15/15**, so unlike R16 (which C-14 closed)
and Ruling 5 (which C-15 closed), **this gap cannot be closed by adding a claim.** It would
need a retirement. Flagged, not resolved.

## 10. WHAT THIS DOES NOT CLAIM

- **`present()` is not yet emitting a full R23 block from every caller.** `apply_response`
  supplies one on all three terminal transitions it drives; a bare `ledger.present(...)`
  without `record=` still writes the original seven keys. **The mechanism is complete and the
  wiring is partial** — stated plainly rather than implied by a passing test.
- **`trigger_rule_version` is empty on `apply_response`-driven events**, by the reasoning in
  §2. A caller holding the `Situation` gets the real value.
- **Nothing is enabled.** No live path, no real member, and still no `ResponseKind`
  classifier — HA-25's gap stands.
- **Nothing ruled MET.** A1–A20 unattempted; the REQ remains DRAFT-RATIFIED-PENDING.

## 11. FINDINGS

1. **The governed record was a third complete** (§1) — 3 of R23's 16 fields — and nothing had
   revealed it, because no check compared the event against R23's list. Verify-first found it.
2. **The R23 block merges under the ledger's keys** (§2), so a caller cannot rewrite the
   state machine's own account of a transition.
3. **The manifest is derived, proven by replay** (§3); a stored copy would be a second source
   of truth.
4. **A non-accepted offer contributes nothing at all** (§3), not even a negative entry.
5. **The cap is now full at 15/15** (§7). The next claim requires a retirement — Bill's.
6. **R23/R24/R25 have no ledger claim and now cannot get one** without a retirement (§9).
