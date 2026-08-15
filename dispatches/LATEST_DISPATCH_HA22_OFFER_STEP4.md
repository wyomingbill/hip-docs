# DISPATCH_HA22_OFFER_STEP4 — no generative surface, proven over the import closure

Status: BUILT
Reconciled-Against: roadmap `b20ef2d` (pre-dispatch HEAD)

**HA-22** | 2026-08-09 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD**
**GOVERNING REQ:** `REQ_OFFER_MECHANISM__…__v20260806_1625.md` (current version), §12 step 4,
requirements **R12** (no generative pitch) and **R13** (A/B testing absent by construction).
**Nothing ruled MET. Fixtures only — nothing presents to a real member, nothing enabled.**

**CLAIM IMPACT: C-07** — see §7.

---

## THE HEADLINE

**Step 4's check found a real generative reach in the offer path on its first execution, and
it is one no single-file scan could have seen.** The offer path imported
`harness.extraction_queue` — the module carrying the Groq/Ollama fact detector — **two hops
below** the module HA-06 had scanned. It was removed, and the absence is now structural.

## 1. ITEM 1 — WHAT ALREADY EXISTED, AND WHERE IT STOPPED

HA-06 built three AST scans in `eval/test_offer_instance.py`: no forbidden imports, no
generative/experiment identifiers among defined names, and a pure-string-work assertion on
`render`. **They are correct, they still pass, and none of them is wrong.**

**They scan one file.** `MODULE_PATH` is `harness/offer_instance.py`. The offer path is not
one file:

```
harness.offer_instance ─┐
harness.offer_gate     ─┤
harness.material_change─┼→ harness.purpose_trigger → harness.inference_permit ─┐
harness.initiation     ─┤                          → harness.representation_class
harness.spend_ledger   ─┘                          → harness.write_origins ────┘
```

`inference_permit` and `write_origins` **both imported `harness.extraction_queue`.**

### Was it actually a model call? No — and that is why it needed removing anyway

Both imports pull one name: `CANONICAL_ATTRIBUTES`, a dict of 17 attribute names. **Nothing
in the offer path ever called the detector.**

But step 4's requirement is that **no model call *can* enter the path**, and "it is imported
but never called" is a statement about today's code that no structural check can keep true
tomorrow. Importing `extraction_queue` executes its module body and puts the Groq/Ollama
client in the offer path's namespace, one attribute access away, with nothing preventing a
future edit from reaching it. **The requirement is about what is reachable, not about what is
currently reached.**

## 2. THE REMOVAL — a leaf module for the vocabulary

`harness/attribute_vocabulary.py` (new) holds `CANONICAL_ATTRIBUTES` and **imports nothing at
all.** `extraction_queue` re-exports the name, so **all twelve original call sites are
unchanged** and the two offer-path modules now import the constant without the client.

Verified identical, not merely equivalent:

```
extraction_queue.CANONICAL_ATTRIBUTES is attribute_vocabulary.CANONICAL_ATTRIBUTES → True
entries: 17
```

A battery test asserts the leaf stays a leaf — **any import added there is inherited by the
offer path**, which is the one way this fix silently un-fixes itself.

## 3. ITEM 2 — THE CHECK: `harness/offer_purity.py`

An **import-closure** check, breadth-first from five declared entry modules, by AST.

| | |
|---|---|
| **forbidden first-party** | `memory_engine.interpreter`, `harness.frontier_client`, `harness.extraction_queue`, `harness.fact_change`, `harness.disclosure`, `harness.realtime_adapter`, `harness.epistemic_record`, `harness.model_registry`, `harness.orchestrator` |
| **forbidden third-party/stdlib** | `openai`, `anthropic`, `groq`, `ollama`, `litellm`, `transformers`, `torch`, `requests`, `httpx`, `aiohttp`, `urllib(3)`, `socket`, **`random`**, `secrets`, **`importlib`**, `subprocess` |
| **forbidden call targets** | `call_frontier`, `generate`, `complete`, `completion`, `chat`, `sample`, `paraphrase`, `rewrite`, `choice(s)`, `shuffle` |

`random` and `secrets` are there for **R13's "randomization input"**. `importlib` is there
because a dynamic import with a computed name would defeat a static closure — **a limitation
this module states in its own docstring rather than hides.**

### Why AST, not a source regex — with the evidence from this dispatch

The standing rule (D-75) says AST over regex. This build produced two fresh illustrations:

- A regex for `generate(` over `harness/` returns **three confident false positives** —
  `X25519PrivateKey.generate()` in `member_seal_keys`, `household_keys` and `dyad_crypto`.
  Key generation, not text generation.
- **A substring scan of `offer_purity.py` itself would fail against itself**: the file's
  prose necessarily contains every word it forbids.

### The scan result on the real path, after the removal

```
PURE — scanned 10 modules:
   harness.offer_instance           harness.purpose_trigger
   harness.offer_gate               harness.inference_permit
   harness.material_change          harness.representation_class
   harness.initiation               harness.write_origins
   harness.spend_ledger             harness.attribute_vocabulary
```

## 4. ITEM 3 — FAULT TWINS, EXECUTED

**Twin A — direct import into the render path.** Injected
`from harness.frontier_client import call_frontier` into `harness/offer_instance.py`:

```
RED: harness.offer_instance imports from 'harness.frontier_client'
     (forbidden: harness.frontier_client)
```

**Twin B — the case that matters: two hops down.** Restored A, then injected
`from memory_engine.interpreter import interpret` into `harness/purpose_trigger.py`, leaving
`offer_instance.py` **clean**:

```
RED: harness.purpose_trigger imports from 'memory_engine.interpreter'
     (forbidden: memory_engine.interpreter)
```

**And the same injected fault, run through HA-06's single-file scan shape:**

```
HA-06-shape single-file scan finds: NOTHING — it passes
```

**That is the whole justification for step 4 being its own build.** The existing scan is not
wrong; it is not deep enough, and the difference is invisible until something is injected
below it.

**Restored, and green again — verified by `git diff --stat`, which reports no residual change
to either file:**

```
GREEN — 10 modules, 0 violations
```

## 5. ANTI-VACUITY — three refusals, because a purity check is easy to fake

Item 3 requires the check to name what it scanned and to refuse on zero. It refuses on three
things, each closing a distinct way this could report green while enforcing nothing:

1. **Zero modules scanned is a REFUSAL.** An empty entry tuple, or entries resolving to no
   file, would otherwise find no violations and pass.
2. **The closure must expand past the entry set.** These modules demonstrably import one
   another; a closure that never grew would mean imports are not being followed — **exactly
   the bug that makes a deep model call invisible**, and it would look identical to success.
3. **Every forbidden first-party module must EXIST.** A renamed or misspelt target can never
   match, so the guard would report green forever. This is the one most likely to happen by
   accident — a future rename of `frontier_client` would silently disarm it.

The report also carries `scanned` and `files`, and a test asserts every reported file is
real: **a green result whose scope is unstated is not evidence.**

## 6. ITEM 6 — RUNS

| Run | Result |
|---|---|
| **Batteries** | **864 passed, 0 failed** (851 → 864: +13 from this dispatch's battery) |
| **`--layer 7`** | L7 **27/27** · L7V2 **27/28** (1 skip) · AUDIT **9/9** · DISC/SCHEMA/VOICE 1/1 |
| **RATCHET** (deterministic) | **PASS — no scenario regressed vs baseline** |
| `AUDIT:KEY-HYGIENE-ZERO-ORPHAN` | **PASS** (HA-20's relocated invariant, still green) |
| **Memory harness** | **13/17 — INSIDE THE PIN** (13–15). Same four: MEM-115/116/117/118 |
| **`--full`** | §6.1 — live layers logged to the collector |

**The deterministic set is green**, which under item 12's amended rule is what "the build
passes" means.

**The manifest mechanism worked as designed and is worth recording:** the new battery was
refused before it was registered —
`assert not ['test_offer_purity.py']` — and only passed once added to `run_harness.sh`. The
self-registration rule HA-03 built caught this dispatch, exactly as intended.

### 6.1 `--full` — live layers, reported, no gate claim

```
batteries: 864 passed, 0 failed
== L7: 27/27   == L7V2: 27/28   == AUDIT: 9/9   == DISC/SCHEMA/VOICE: 1/1
KEY-HYGIENE-ZERO-ORPHAN  PASS
== L1: 13/15   == L2: 24/35 (10 skip)   == L3: 3/3   == L4: 30/34 (4 skip)   == L6: 1/1
[live-layers] appended 88 scenario result(s)  (run_id=20260810T034419_b20ef2d)
RATCHET FAIL — regressed vs baseline: ['L2:routing_showcase.T04']
NEW FAILURES (not in baseline): ['L1:P12']
```

**Every deterministic layer green.** The two reds are live-layer scenarios, both already
characterised: `L2:routing_showcase.T04` (the one stable regression — answers a news query
with the clock, red in every `--full` since HA-19) and `L1:P12` (never baselined; its two
checks read a `payload` key the event reader does not return, so they **cannot pass whatever
the code does**). **Neither is in the binding set and no gate claim is made either way**, per
item 12's amended rule.

**`FULL EXIT=1`** — as HA-20 recorded, `run_harness.sh`'s exit code still fails on live
layers and no longer means what item 12 means. **Read the layer lines, not the exit code.**

**L6 was green this run** (1/1) having been red in both of HA-20's. The collector now shows
that directly, which is exactly what it was built for:

```
record-invariants   20260810T023252_7b776b3  FAIL
record-invariants   20260810T025902_7b776b3  FAIL
record-invariants   20260810T034419_b20ef2d  PASS
```

**The series stands at three `--full` runs, 264 rows** — HA-19's runs predate the collector,
so they are not in it. **Still far too little to set a rule from, and none is set.**

## 7. CLAIM IMPACT

**CLAIM IMPACT: C-07** — *"Offer text cannot drift from its approved effect; no generative
surface exists in the offer path."*

The ledger's v1 draft records C-07 as **PARTIAL**, with evidence *"Re-render integrity proven
(HA-06); step 4 (strip generative interfaces) not started."* **Step 4 is now built**, and its
second clause has standing evidence for the first time: a closure-level structural check, two
executed fault twins, and one real generative reach removed.

**No status is asserted.** Statuses are computed by a generator that does not exist yet;
naming a claim is a pointer, not a ruling. **And C-07's first clause is not this dispatch's**
— text-to-effect identity is HA-06's re-render integrity proof, untouched here.

## 8. WHAT THIS DOES NOT CLAIM

- **Not a dynamic guarantee.** The closure is static. A computed `importlib.import_module`
  would evade it — which is why `importlib` is forbidden to these modules, and why the
  limitation is written into `offer_purity.py`'s docstring rather than left for a reader to
  discover.
- **Not a claim about the rest of the system.** `memory_engine.store`, `harness.fact_change`
  and `harness.write_rule` all reach forbidden surfaces and **should** — they are not the
  offer path. The battery uses them as fault twins precisely because that is legitimate.
- **Nothing ruled MET.** §12 step 4 is built; A10 and the rest of A1–A20 are unattempted, and
  the REQ remains DRAFT-RATIFIED-PENDING.

## 9. FINDINGS

1. **The offer path could reach the Groq/Ollama detector** (§1) — two hops below HA-06's
   scan, via `CANONICAL_ATTRIBUTES`. Removed by splitting the vocabulary into a leaf module.
2. **A single-file scan is blind to it** (§4), proven by injecting the fault and watching
   HA-06's shape pass while the closure check went red.
3. **Twelve call sites were unaffected** (§2) — the re-export makes the split invisible, and
   the constant is verified to be the same object through both names.
4. **The forbidden-module list needs its own existence check** (§5). A rename would disarm
   the guard silently; that is now a refusal.
5. **The manifest mechanism caught this dispatch's own battery** (§6) before it was
   registered.
