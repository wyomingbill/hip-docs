# DISPATCH_HA25_OFFER_STEP6 — explicit response, exact scope, authority validated

Status: BUILT
Reconciled-Against: roadmap `0db200e` (pre-dispatch HEAD)

**HA-25** | 2026-08-10 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD + RIDER**
**GOVERNING REQ:** `REQ_OFFER_MECHANISM__…__v20260806_1625.md` §12 step 6 — **R15** (explicit
response only), **R16** (exact-scope application), **R17** (principal and authority
validation), with **R18**'s integrity tie-in.
**Nothing ruled MET. Fixtures only — nothing presents to a real member, nothing enabled.**

**CLAIM IMPACT: C-06** — see §7.

---

## 1. WHAT WAS BUILT

`harness/offer_response.py` — the only path by which an offer resolves and the only path by
which scope changes. `eval/test_offer_response.py` — **32 tests**, registered in the standing
battery.

**Four things it deliberately does NOT do**, because each already exists or must not exist:

| Not done | Why |
|---|---|
| a second state machine | `harness.spend_ledger` (HA-08) owns states, terminal transitions and durability, with a process-kill proof. **A second would be a second source of truth about whether an offer is resolved.** |
| its own event log | Same module already appends governed-decision events. Item 4 said reuse; this reuses. |
| free-text parsing | A response arrives **already classified**. See §3. |
| spent-ness logic | HA-08's, unchanged. Step 6 only reaches terminal states. |

## 2. R17 — THE PART THAT IS ABOUT WHAT IS *ABSENT*

R17: *"Household role, account ownership, caregiver status, or prior access alone SHALL NOT
substitute for decision authority."*

**`apply_response` has no parameter through which a role could substitute.** There is no
`role`, no `is_owner`, no `is_caregiver`, no `has_prior_access` — only `authorities`, a list
of explicit `DecisionAuthority` grants. **The requirement therefore holds by construction
rather than by a check that could be bypassed**, and a test asserts the signature stays that
way, so adding such a parameter later breaks the battery rather than quietly weakening R17.

`DecisionAuthority` carries exactly three fields — principal, decision domain, and who holds
it. **A wildcard domain is refused at construction:**

```
DecisionAuthority(principal="maya", decision_domain="*")     -> ValueError
DecisionAuthority(principal="maya", decision_domain="all")   -> ValueError
```

*"Authorized for everything" is "prior access alone" wearing a different hat*, and R17's
"this exact decision domain" is the phrase that rules it out.

## 3. R15 — THE RESPONSE ARRIVES CLASSIFIED, NOT AS PROSE

`ResponseKind` is a **closed enum with eleven members**, nine of which exist only to be
refused. R15 names them: silence, continued conversation, an adjacent answer, prior
acceptance, a caregiver's preference, inferred sentiment, engagement, *"whatever you think"*,
and any ambiguous response.

**An enum with only ACCEPT and DECLINE would have been shorter and worse** — every other case
would fall into "unhandled", and unhandled is where silent acceptance lives.

**`apply_response` never sees the member's words.** Mapping an utterance to a `ResponseKind`
is a caller's job above this boundary, and `AMBIGUOUS` is the safe answer when in doubt.
Two reasons, both load-bearing:

1. **R15 forbids reinterpreting a response.** A function that read prose would have to
   interpret it, exactly where the requirement says not to.
2. **HA-22 has just finished proving the offer path has no generative surface.** Text
   interpretation here would put one back.

A test asserts the signature takes `kind: ResponseKind` and no `text`/`utterance`/`message`.

**The neutral instruction is a CONSTANT**, not a template: R15 permits a fixed instruction
and forbids asking again, and anything parameterised could be personalised — *a personalised
re-prompt is asking again.* A test asserts it contains no braces and no re-pitch words.

## 4. R16 — SET EQUALITY, EVALUATED

Scope is a set of **dimension-namespaced tokens**, so R16's equation is checkable directly
rather than by inspection:

```
scope_after == scope_before | delta_applied        (GrantResult.exact)
```

**Empty delta dimensions produce NO token.** §2.4 says an omitted field means no change to
that dimension; emitting a token for it would grant something the offer never named — the
precise "nothing more" R16 forbids. The fixture's delta declares four dimensions, and the
test asserts `action:`, `initiation:`, `inference:` and `representation:` are **absent** from
the grant.

**Namespacing matters:** an `action_authority` of `notify` and an `initiation_authority` of
`notify` are two different grants, not one.

The union is asserted after the fact even though it is unreachable by construction — *the
requirement is set equality, and an unchecked union is only equality by inspection.*

## 5. ITEM 3 — FOUR FAULT TWINS, EXECUTED

| | Twin | Result |
|---|---|---|
| **(d)** | intended principal's explicit yes | **GRANTS EXACTLY THE DELTA**, `exact_set_equality: True`, manifest lists it, state `ACCEPTED` |
| **(a)** | response from the wrong member | **REFUSED**, `reason=responder_not_authorized` recorded, state stays `PRESENTED` |
| **(b)** | accept against a tampered instance | **INVALIDATED**, grants nothing, state `INVALIDATED` |
| **(c)** | *"whatever you think"* | **RESOLVES NOTHING**, neutral instruction returned, state stays `PRESENTED` |

**(d) is the first test in the file, deliberately.** Every refusal above is worthless on a
module that refuses everything; the anti-vacuity case has to come first or the rest is
decoration.

**(c) is parametrized over every non-resolving enum member**, not a hand-written list — so a
future `ResponseKind` cannot be added without being tested.

**(b) tampers via `object.__setattr__`**, precisely because the dataclass is frozen: the
guarantee is HA-06's re-derived hashes, not the frozen flag.

### The ordering finding, which is a decision and not an accident

**R18 runs FIRST — before the responder is even examined.** A wrong-member response to a
*corrupted* offer must report the corruption, not the responder. Reporting "not authorized"
would leave the tampering undetected and the record actively misleading. There is a test for
this exact ordering (`test_integrity_is_checked_before_the_responder_is`), because the two
checks pass in either order and only one order tells the truth.

**And R18 invalidates the OFFER — it does not merely block the grant.** The situation reaches
a terminal state and can never be re-presented (R8). A mismatch is the end of the offer, not
a retryable error.

## 6. ITEM 6 + THE OFFER-PATH TRAP HA-22 WARNED ABOUT

The battery was refused before registration (`assert not ['test_offer_response.py']`) and
passes registered — HA-03's self-registration mechanism working again.

**More importantly:** HA-22's handoff note says *"BEFORE ADDING A MODULE TO THE OFFER PATH:
add it to `OFFER_PATH_ENTRY_MODULES`, or it is simply not scanned."* Checked, and it was
true — `harness.offer_response` was **not** in the purity scan's closure when first written:

```
before: scanned: False   modules: 10
after : OFFER PATH STILL PURE — 11 modules, offer_response scanned: True
```

**The new module is now declared and clean.** This is the one failure mode HA-22's check
cannot self-detect, the note existed for exactly this dispatch, and it caught it.

## 7. RIDER — `REQ_HARNESS_RUNNER` AMENDED

One amendment, citing Bill's 2026-08-09 ruling verbatim, recording the exit-code contract
HA-24 built. **No other REQ text changed; status stays MET; acceptance untouched.**

It also answers HA-24's own open governance finding: that REQ's scope was **preconditions and
refusals**, so the runner's *exit semantics* had no REQ home and lived only in a dispatch
doc. They now have one.

## 8. RUNS

| Run | Result |
|---|---|
| **Batteries** | **896 passed, 0 failed** (864 → 896: +32 from this dispatch) |
| **`--layer 7`** | L7 **27/27** · L7V2 27/28 · AUDIT **9/9** · DISC/SCHEMA/VOICE 1/1 · `KEY-HYGIENE-ZERO-ORPHAN` PASS |
| **RATCHET** (binding) | **PASS** · **exit 0** |
| **Memory harness** | **13/17 — INSIDE THE PIN** (13–15). Same four: MEM-115/116/117/118 |
| **`--full`** | §8.1 |

**The binding set is green** — which, under item 12 as amended and HA-24's exit contract, is
what "the build passes" now means, and `--layer 7` returned **exit 0** accordingly.

### 8.1 `--full` — live layers logged, no gate claim, **and exit 0**

```
batteries: 896 passed, 0 failed
== L7: 27/27   == L7V2: 27/28   == AUDIT: 9/9   == DISC/SCHEMA/VOICE: 1/1
== L1: 13/15   == L2: 24/35 (10 skip)   == L3: 3/3   == L4: 30/34 (4 skip)   == L6: 1/1
[live-layers] appended 88 scenario result(s)  (run_id=20260810T130610_0db200e)
RATCHET FAIL — regressed vs baseline: ['L2:routing_showcase.T04']
NEW FAILURES (not in baseline): ['L1:P12']
BINDING TESTS PASS. LIVE-MODEL TESTS HAVE FAILURES — SEE RUN LOG.
FULL EXIT=0
```

**This is HA-24's exit contract working in production for the first time outside its own
proof.** Every binding layer green, the two known live reds reported in full, and **exit 0** —
where before HA-24 this identical run would have exited non-zero and needed a paragraph
explaining why that did not mean failure.

The two reds are unchanged and already characterised: `L2:routing_showcase.T04` (stable, red
in every `--full` since HA-19) and `L1:P12` (never baselined; its checks read a `payload` key
the event reader does not return, so they cannot pass). **No gate claim either way.**

Collector series: **five `--full` runs, 440 rows** (HA-24's case-(a) run appended too).

## 9. CLAIM IMPACT

**CLAIM IMPACT: C-06** — *"An offer, once presented for a situation, can never be
re-presented or reworded — including across restart and replay."*

Step 6 is where offers reach **terminal** states, and this dispatch adds standing evidence
that a resolved situation stays spent and cannot be re-presented
(`test_a_terminal_state_leaves_the_situation_spent`, `test_a_second_resolution_is_refused`).
**That is a reinforcement of C-06's existing PROVEN (draft) status, not a change to it** —
the durability itself is HA-08's.

**No other claim moves, and two near-misses are worth naming so nobody reads them in:**

- **C-07 does not move.** Its second clause is about generative surfaces; step 6 adds no
  rendering. The purity scan simply grew to cover a new module.
- **There is no ledger claim for "acceptance grants exactly what was shown."** R16 is the
  strongest thing built here and **no claim currently covers it.** Flagged for Bill: this may
  warrant a claim, and the ledger's cap is 15 with 13 used.

## 10. WHAT THIS DOES NOT CLAIM

- **Nothing is enabled and nothing presents.** Fixtures only; no real member, no live path.
- **No `ResponseKind` classifier exists.** Turning an utterance into a kind is deliberately
  outside this module and unbuilt — **the honest state is that step 6's boundary is complete
  and its caller is not.**
- **Nothing ruled MET.** A1–A20 unattempted; `REQ_OFFER_MECHANISM` remains
  DRAFT-RATIFIED-PENDING.

## 11. FINDINGS

1. **R17 is enforced by the absence of a parameter** (§2), asserted by a signature test —
   stronger than a check, because there is nothing to bypass.
2. **The response arrives classified, never as prose** (§3) — R15 forbids reinterpretation,
   and prose here would reintroduce the surface HA-22 removed.
3. **Integrity is checked before authority** (§5) — the two orders differ only in which
   truth the record tells, so the order is tested.
4. **`harness.offer_response` was invisible to the purity scan until declared** (§6) — the
   trap HA-22's handoff note predicted, caught by following the note.
5. **R16 has no claim in the ledger** (§9). The strongest guarantee built here is uncovered.
