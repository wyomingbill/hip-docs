# DISPATCH_HA38_A6_A12_A16 — unsupervised block: three builds and a collector run

Status: **ALL FOUR SEGMENTS COMPLETE — THREE BUILDS LANDED, COLLECTOR RUN**
Reconciled-Against: roadmap `7abcd37`
Filed: 2026-08-11 (HA-38)
Decision-Owner: Bill
Authority: Bill's unsupervised-block dispatch, 2026-08-11
Plan of record: `HIP_FinishPlan__three-finish-lines-14-steps__v20260811.md` — **steps 3, 4 and
5. Step 6 (the A1–A20 rerun) was NOT run**, per instruction.

| segment | clause | status | commit |
|---|---|---|---|
| 1 | **A6** — minimal authority delta (R7) | **COMPLETE, LANDED** | `e7fb5f6` |
| 2 | **A12** — utterance → `ResponseKind` (R15) | **COMPLETE, LANDED — did not stop** | `8ada954` |
| 3 | **A16** — narrowing and revocation (R19) | **COMPLETE, LANDED** | `e18a0ae` |
| 4 | collector data — RATCHET `--full` ×2 | **COMPLETE** (after one killed attempt, re-run) | docs only — this doc |

**Nothing is ruled MET. No claim status, REQ status or ledger version changed. The demo lane
was not touched.** Preflight PROCEED (Neo4j 7688 authenticated read; roadmap-local registry).

---

## SEGMENT 1 — A6, MINIMAL AUTHORITY DELTA

### The canonical representation

`canonical_delta()` renders a delta as a sorted tuple of `(dimension, sorted values)` over its
**non-empty dimensions only**. `purpose_id` and `principal` are excluded deliberately: they
identify WHICH offer this is, not how much authority it asks for, and including them would make
every purpose its own minimality class — which is to say, would make the check vacuous.

### Minimality is ratified in advance, then checked by set equality

**"Smallest" cannot be computed at runtime.** There is no metric over authority, and inventing
one would be exactly the *"choose among competing deltas based on likely acceptance"* R7
forbids. So `RATIFIED_MINIMAL_DELTAS` states, per (situation kind, purpose), the one delta
ratified as minimal, and an offer is minimal iff its canonical form **equals** that entry.
It is a literal, not a store — **a registry runtime can write is a registry runtime can choose
from.**

### Three fault directions, all refused, two with distinct exception types

| direction | what it is | why refused |
|---|---|---|
| **BUNDLED** | carries a dimension the ratified entry does not | R7's "combine additional permissions"; each of its named cases — adjacent recipient, category, inference, retention period, recurring action, capability — is its own twin |
| **STAIRCASE** | **omits** a ratified dimension | a proper subset looks *more* minimal and is not: R7 ratifies ONE delta per trigger, so asking for less now means the rest arrives later — R7's "split the delta into multiple offers" |
| **SUBSTITUTED** | right dimensions, different values | runtime does not get to pick a variant |

**The staircase is the direction a bundle-only check would miss entirely**, and a test makes
the argument explicit: it constructs both steps and shows they sum to exactly the ratified
delta, so permitting them permits reaching the same authority by instalments.

`BundledAuthority` and `StaircaseOffer` are distinct types because they are distinct failures
with distinct fixes; one `NotMinimal` would make them look like one problem.

### R7's last sentence, built

`select_minimal_offer()` has the registry select one entry **by pre-ratified precedence**. No
matching entry **fails closed** — unreviewed is not minimal. **Equal precedence is an ERROR,
not a tie-break**: a tie-break invented at runtime is runtime choosing among competing deltas.

### Wired opt-in — a stated scope limit

`OfferInstanceRegistry.create(..., require_minimal_for=<kind>)` enforces minimality **before
rendering**, so an over-broad offer never exists as words anywhere, and a refused offer leaves
no instance. **It is opt-in because making it mandatory would refuse calls that succeed
today** — several existing fixtures build unratified deltas — and that is a behaviour change,
not the check A6 asks for. **Whether creation should refuse unconditionally is recorded for
Bill, not decided here.**

**29 standing tests.** Every fault twin is paired with an anti-vacuity half on the ratified
delta: a check that refused everything would satisfy every twin and break the product.

---

## SEGMENT 2 — A12, UTTERANCE → `ResponseKind`

### THE SEGMENT DID NOT STOP, AND THE REASON IS STRUCTURAL

The dispatch said to stop if the mechanism genuinely required a ruling between deterministic
rules and a model. **It does not.** `harness.offer_response` is an ENTRY MODULE of the offer
path's purity closure, and `assert_offer_path_is_pure` refuses any model client, network
surface or randomness reachable from it — `memory_engine.interpreter`,
`harness.frontier_client`, `harness.extraction_queue`, `harness.model_registry` and the rest
are named forbidden destinations. A classifier feeding `apply_response` sits **inside** that
closure, so **a model-backed classifier would fail an existing, already-ratified ABSOLUTE-tier
guard.** The architecture decided this before the module existed.

R15 pushes the same way from the requirement side: acceptance must be EXPLICIT, and *"an
ambiguous response changes no scope."* A classifier that had to be asked what a member probably
meant is the thing R15 forbids. **The reasoning is recorded in the module docstring so it can
be overruled if wrong.**

### The rule that makes it safe

**Whole-utterance exact match against a closed vocabulary, then fail closed.** Substring
matching is deliberately not used — *"no, yes I mean no"* contains "yes", and a substring rule
would accept it.

**The asymmetry is the safety argument.** Misreading an acceptance as ambiguous costs one
repeated interaction. Misreading an ambiguity as acceptance grants authority nobody agreed to.
**Misreading an ambiguity as a DECLINE is also harmful** — decline is terminal and R8 makes
spending permanent — so an unrecognised utterance becomes neither: `AMBIGUOUS`, and the offer
stays open.

### Raw prose stops at the boundary

`Classification` carries the matched vocabulary entry and a hash of the normalised utterance,
**never the words**. `apply_response` has **no text parameter at all** — a standing test
asserts its exact parameter set — so the boundary is enforced by SIGNATURE rather than by
discipline.

### `resolves` and `grants_authority` are separate, and that was a correction

A first draft exposed one flag meaning "resolves the offer", which returns True for a DECLINE.
**Read at a call site, that says a decline granted authority.** They are now two properties:
`resolves` (accept or decline — both end the offer) and `grants_authority` (**EXPLICIT_ACCEPT
and nothing else**), which is A12's own clause as one expression.

`ResponseKind` gains `QUESTION` (R14: asking what an offer means is not deciding) and
`INVALID`. **Both are non-resolving**, so the addition grants nothing new, and a standing test
asserts over the WHOLE enum that exactly two kinds resolve — a future member cannot quietly
become resolving.

### A regression this segment hit, kept as a test

The first cut treated any utterance opening with an interrogative word as a question, so
**"do it" (accept) and "do not" (decline) both classified as QUESTION.** Closed-vocabulary
whole-matches now outrank the first-word heuristic, which only decides what is left over; a
question **mark** still outranks everything.

### All four clauses proven

only explicit acceptance grants authority; ambiguity grants nothing **and does not decline
either** (the offer stays PRESENTED); the wrong person grants nothing even with a flawless
acceptance — with an anti-vacuity half showing an authorized representative CAN accept, or the
wrong-person tests would pass on a system that refused everyone; and classifier output, never
raw prose, enters `apply_response`.

**76 standing tests.**

### Filed, not chased

**The VOCABULARY is narrow and provisional and says so.** "ok" and "sure" classify AMBIGUOUS on
the grounds that they are acknowledgements rather than decisions. **Which phrases count as
explicit acceptance is a ratification question, not a mechanism question**, and narrowness is
safe by construction because every unrecognised phrase already grants nothing. Widening is the
direction that needs review — recorded for Bill, not answered here.

---

## SEGMENT 3 — A16, NARROWING AND REVOCATION

### Revocation is not an offer transition — the central design point

R23's five transitions are a **closed set about an offer's life**. R19 revocation has **no
offer and no trigger**, so modelling it as a transition would both widen a closed set and imply
an offer that does not exist. It appends its own event kind, `authority_change`, to the same
control-plane ledger. **R23's sixteen fields and five transitions are untouched**, asserted by a
standing test.

### The manifest stays derived, never stored

`current_authority` replays grants and changes in append order, so **a revocation takes effect
the moment it is appended** — no cache to invalidate, no session to expire. Proven across a
real reconstruction in a second ledger object.

### Derivative consequences

Revoking a purpose takes **everything granted under it**, read off the record rather than
guessed: tokens granted together by one acceptance belong to that acceptance's purpose. **A
revoked purpose whose audience projection quietly survived would be a revocation in name only.**

### Fault twins in both directions — which for an inverse operation means two things

* it must **work** — access held before is denied after;
* it must be **bounded** — narrowing removes what was named and nothing else, and revoking one
  purpose leaves another's authority intact. **A revocation that took too much would pass every
  access-denied assertion while destroying the product.**

### "SHALL NOT be delayed in order to preserve a product feature"

There is **no parameter, flag or branch** by which a caller can defer, stage or grace-period a
revocation, and a standing test asserts the signatures carry none. **An option to delay IS the
mechanism R19's last sentence forbids**, so the only way to honour it is for the option not to
exist. The behavioural half is proven too: revocation executes immediately and completely even
when the authority removed is the only thing enabling a capability.

Fails closed: revoking something not held **raises** rather than reporting success, so a
mistyped token cannot look like a completed revocation.

**23 standing tests.**

---

## THE DEFECT FOUND WHILE BUILDING — FILED AND NOT CHASED

**TD-R-184.** `governed_record.authority_manifest_for` folds accepted events as
`update(scope_after)` then `difference_update(scope_before)`. That pair is right for ONE event
and **wrong for a sequence**: the second acceptance's `scope_before` contains the first's
tokens, so subtracting it **erases authority the member still holds.**

```
event 1: before []                        after [purpose:A, audience:X]
event 2: before [purpose:A, audience:X]   after [purpose:A, audience:X, purpose:B, inference:Y]

current code   -> ['inference:Y', 'purpose:B']
union-of-deltas -> ['audience:X', 'inference:Y', 'purpose:A', 'purpose:B']
```

**A member who accepts two offers has the first vanish from R25's cumulative manifest** — the
instrument whose entire job is to state what they have granted. It went unnoticed because every
existing caller passes `scope_before=frozenset()`, under which the two forms agree; it appears
the moment scope accumulates across acceptances, which is the real usage.

**IT IS NOT FIXED, AND THAT IS PREAMBLE ITEM 12 BEING APPLIED RATHER THAN QUOTED.** A finding
becomes immediate work only if it blocks the current phase's acceptance criteria. This is R25's
manifest; A16 is revocation and narrowing. `current_authority` folds correctly
(`held |= after - before`) because A16's own acceptance depends on it, and that is the only
part this segment was entitled to touch. **The fix is one line plus a test; what made it a
separate dispatch is scope, not difficulty.**

**CONSEQUENCE WHILE IT STANDS, STATED PLAINLY: two functions now answer "what has this member
granted?" and they disagree after a second acceptance.** A standing test **pins the divergence**
so that fixing TD-R-184 makes it fail loudly and both are re-read together — a silent
convergence is fine, a silent divergence is how two sources of truth persist.

---

## SEGMENT 4 — COLLECTOR DATA

### Two RATCHET `--full` runs, back to back, on commit `e18a0ae`

**A FIRST ATTEMPT WAS KILLED AND PRODUCED NOTHING — reported because the difference matters.**
The background task was stopped externally during run 1's Ollama startup: the collector was
unchanged at 1145 rows, run 2 never began, and the memory-harness output file that survived was
**stale from HA-35's run at 07:51**. Reading it would have attributed HA-35's memory result to
this dispatch. Memory was at 28% free, so the TD-129 threshold was not the cause. The segment
was re-run from the start with per-step progress markers so a second kill could be reported
exactly rather than inferred from files that might predate the run.

| run | run_id | exit | collector rows | verdict |
|---|---|---|---|---|
| 1 | `20260811T190238_e18a0ae` | 0 | 1145 → 1233 (+88) | **BINDING TESTS PASS**; regressions `['L2:routing_showcase.T04']`; new failures `['L6:record-invariants']` |
| 2 | `20260811T191921_e18a0ae` | 0 | 1233 → 1321 (+88) | **BINDING TESTS PASS**; regressions `['L2:routing_showcase.T04']`; new failures `none` |

Memory harness: **13/17** (4 failed) — inside the 13–15 pin.

### The finding the two runs produced

**Identical counts, different failures.** Both runs: 88 scenarios, 72 PASS / 2 FAIL / 14 SKIP.
The failures were not the same ones:

```
L1:P2                  run1=PASS   run2=FAIL
L6:record-invariants   run1=FAIL   run2=PASS
L2:routing_showcase.T04  FAIL in both
2 of 88 scenarios differ, on byte-identical code, back to back
```

**A count-based rule would have called these two runs identical.** That is a concrete argument
about the shape of any future reproducibility rule, produced by running the thing twice rather
than by reasoning about it.

### The whole collector, 15 runs

| scenario | across all 15 recorded runs |
|---|---|
| `L2:routing_showcase.T04` | **FAIL 15 / PASS 0** |
| `L6:record-invariants` | FAIL 9 / PASS 6 |
| `L1:P2` | FAIL 10 / PASS 5 |

**L6 and L1:P2 are bimodal — the variance item 12's amendment was written for. T04 is not.**
It has never passed in any recorded run, and its observed failure is stable in KIND as well as
in verdict: a news question answered with the local time, run after run. It is reported each
time as a "live-layer regression", which frames it as variance; **the data says it is a
standing, reproducible failure that happens to live in a live layer.** Filed as **TD-R-185**.

**No threshold was set, no reproducibility rule proposed, and no gate claim made** — item 12
reserves all three for Bill, set from data. **Nothing was re-run to make anything look
better**; that is the best-of-N the amendment forbids. The two runs are reported exactly as
they came out.

---

## CLAIM IMPACT

**CLAIM IMPACT: none.

Stated precisely, because three builds and 128 new tests could easily read as movement. **No
claim in the ledger covers delta minimality, response classification, or revocation/narrowing**,
and the clauses these serve — A6, A12, A16 — are measured by step 6's A1–A20 rerun, which was
**not run** per instruction. C-14's evidence explicitly waits on *"after the response classifier
is built"*; the classifier now exists, but **whether that moves C-14 is Bill's ruling from the
rerun, not a session's inference**, and nothing here touches its status.

No claim status, REQ status or ledger version changed. `REQ_OFFER_MECHANISM` remains NOT MET.**

---

## WHAT NEEDS BILL

1. **A6 enforcement — should `create()` refuse a non-minimal delta unconditionally?** Built
   opt-in because mandatory would refuse working callers. This is the one A6 decision left.
2. **A12 acceptance vocabulary — how wide?** "ok" and "sure" are AMBIGUOUS today. A mechanism
   ruling is not needed; a vocabulary ratification is.
3. **TD-R-184** — filed, not fixed, with two functions knowingly disagreeing until it is.
4. **A6/A12/A16 clause status is not claimed.** Step 6, the A1–A20 rerun that would measure
   them, was not run per instruction.

---

## OPEN

- **TD-R-184** (this dispatch), **TD-R-182**, **TD-R-183** — filed, unfixed.
- **`REQ_OFFER_MECHANISM` remains NOT MET.** Three clauses now have standing evidence; the
  rerun that would measure them is step 6 and was not run.
- The 31 health-check reds — unchanged, and the plan of record treats them as Phase 4 cleanup.

---

**HA-38: ALL FOUR SEGMENTS COMPLETE.** Steps 3–5 of the plan of record built and landed; step 6
not run, per instruction. **SEGMENT 1 — A6** (`e7fb5f6`): canonical delta representation plus a
minimality check that is **set equality against a pre-ratified registry, because "smallest"
cannot be computed at runtime and inventing a metric is the thing R7 forbids**. Three fault
directions refused — BUNDLED, **STAIRCASE** (a proper subset looks more minimal and is the
split R7 forbids; a test shows the two steps sum exactly to the ratified delta), and
SUBSTITUTED — each paired with an anti-vacuity half. Precedence selects one entry; **equal
precedence is an error, not a tie-break**. Wired **opt-in** at offer creation, before rendering,
because mandatory would refuse working callers. 29 tests. **SEGMENT 2 — A12** (`8ada954`):
**did not stop, and the reason is structural** — `offer_response` is an entry module of the
offer path's purity closure, so a model-backed classifier would fail an already-ratified
ABSOLUTE-tier guard; the architecture decided this before the module existed, and the reasoning
is recorded so it can be overruled. **Whole-utterance exact match, then fail closed**; substring
matching deliberately unused because "no, yes I mean no" contains "yes". Unrecognised is
AMBIGUOUS, **not declined** — decline is terminal and R8 makes spending permanent. Raw prose
stops at the boundary: `apply_response` has no text parameter and a test asserts its exact
signature. `resolves` and `grants_authority` split after a first draft made a **decline read as
granting authority**. 76 tests. **SEGMENT 3 — A16** (`e18a0ae`): revocation is **not an offer
transition** — R19 has no offer, so R23's closed five stay closed; it appends its own event
kind. Manifest stays derived, so revocation takes effect on append with no cache to invalidate,
proven across a real reconstruction. Derivative consequences enforced; **fault twins both
directions**, including the bounded one a revocation that took too much would pass. **No
parameter exists by which revocation could be delayed** — an option to delay is the mechanism
R19 forbids. 23 tests. **A DEFECT FOUND AND FILED, NOT CHASED — TD-R-184:**
`authority_manifest_for` erases a member's earlier grant on their second acceptance; hidden
because every existing caller passes an empty `scope_before`. **Not fixed — item 12 applied,
not quoted:** it is R25's manifest, not A16's criteria. Consequence stated plainly: **two
functions now disagree about what a member has granted**, and a standing test pins the
divergence so fixing it fails loudly. **SEGMENT 4:** two `--full` runs, both **BINDING TESTS
PASS**, collector 1145 → 1321 (+176 rows); memory **13/17, inside the pin**. **A first attempt
was killed and produced nothing** — reported because the surviving memory output was stale from
HA-35 and would have been misattributed. **The two runs produced a real finding: identical
counts, different failures** (`L6` FAIL→PASS, `L1:P2` PASS→FAIL) on byte-identical code, so a
count-based rule would call them identical. Across all 15 recorded runs **`L2:T04` is FAIL
15/15 — never once passed**, while L6 and L1:P2 are bimodal: T04 is a standing reproducible
failure that happens to live in a live layer, not variance. Filed **TD-R-185**. **No threshold,
no reproducibility rule, no gate claim, and nothing re-run to look better.** **CLAIM IMPACT:
none. Nothing ruled MET; no claim, REQ or ledger status changed; demo lane untouched.**
