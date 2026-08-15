# DISPATCH_OFFER_INSTANCE — the immutable instance, text-to-effect identity, and a path with no generative surface

Status: BUILT
Reconciled-Against: roadmap `984d071` (pre-build HEAD). **LANDED AT `2e7924a`** — backfilled by the immediately following commit, because a commit cannot contain its own hash.

**HA-06** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **BUILD (code)**
**GOVERNING REQ:** `REQ_OFFER_MECHANISM__governed-initiation-of-new-authority__v20260806_1625.md`,
**§12 LANDING ORDER step 3 ONLY** — "Introduce immutable offer instances binding template
and authority delta."
**NOTHING RULED MET.**

## 1. CHECK FIRST — what exists, and what is reused rather than rebuilt

| Module | Landed | Reused how |
|---|---|---|
| `harness/material_change.py` | HA-03 | `Situation` + `derive_situation_id` **imported**; the id is re-derived from the situation's own fields so a forged one cannot carry an instance. Situation identity is not redefined. |
| `harness/offer_gate.py` | D-R-171, extended HA-03 | Untouched. R24's dedup tuple is a different concern from R11's instance. |
| `harness/initiation.py` | HA-01 | Untouched — nothing here initiates. |
| `harness/purpose_trigger.py` | D-152 | Untouched. |

**No offer-instance, template, rendered-text or authority-delta representation existed** —
a sweep for `offer_instance`, `template_id`, `template_hash`, `rendered_text`,
`authority_delta`, `slot_value` returned nothing. Clean build on HA-03's foundation.

## 2. WHAT WAS BUILT

`harness/offer_instance.py`:

- **`AuthorityDelta`** — §2.4's exact nine dimensions. `principal` and `purpose_id`
  required; the rest default empty, and **empty means "no change to that dimension"**, per
  §2.4's own sentence, never "unspecified".
- **`FixedTemplate`** — reviewed body, typed `slot_schema`, and `delta_clauses`: the delta
  dimensions whose values must appear in the text. That field is the mechanism §3 rests on.
- **`SlotType`** — a closed set of five, from §2.5's own list, **each member carrying its
  own validator, so the type IS the registry**; there is no second place a value can be
  approved.
- **`OfferInstance`** — R11's fifteen fields, frozen, created only through the registry.
- **`OfferInstanceRegistry.create`** — the one constructor. Validates before recording.
- **`render`** — the one renderer. Pure function of (template, slots, delta).

Worked example, printed from the shipped code:

```
offer_instance_id  : offer:33dcbe0696e61c13ea4678c898fd7cce
situation_id       : sit:e77ab2425a5830d4a20999c672cc37f3
authority_delta_id : delta:2af4577b104b9cce25e81f348fb04067
--- rendered text ---
Maya, may I send your daughter a note when a dose is missed?
audience projection: care_team
retention policy: 90 days
```

## 3. HOW R18 IS ENFORCED — and why the obvious design would not have worked

The naive reading of "the text matches the delta" is: render the text, compute the delta
separately, compare them. **That cannot work.** Prose and a scope object are not
comparable, and a check shaped that way degenerates into asserting a string contains some
words — which any reworded pitch would also satisfy.

**What is enforced instead: the text is a PURE FUNCTION of template, slots and delta, and
the instance stores the hash of its own output.** The delta is an *input* to `render`, and
every dimension the template names is interpolated verbatim from it. So the two cannot
drift apart by construction — and `validate_instance` **re-renders** from the instance's
own bound objects and compares to `rendered_text_hash`.

One assertion therefore catches an edited slot value, an edited delta, an edited template
body, and edited text. **The load-bearing proof is that a different delta produces
different text** (`test_a_different_delta_produces_different_text`); without that, "identity"
would be a slogan.

**Frozen-ness is NOT the guarantee, and the tests say so.** `object.__setattr__` walks past
`frozen=True`, and so does `dataclasses.replace`. Both routes are proven closed: the
instance carries hashes of its own inputs and output, so an edit is caught whatever route
it took in.

## 4. FAULT TWINS (item 4) — `eval/test_offer_instance.py`, 36 tests, 36 pass

| Twin | Cases | What it proves |
|---|---|---|
| **An edited instance is rejected** | 7 fields parametrized + slots + bound delta + `dataclasses.replace` | each field edited **separately**, so one over-broad check cannot mask another |
| **A delta/text mismatch is invalid** | render with one delta, bind another (hashes updated to match the swap) | the subtlest attack: enforcement would apply a scope the member never saw |
| **A slot value outside the registry type is refused** | 7 bad values + unknown slot + missing slot | incl. `{recipient}` (would inject a placeholder) and a newline (would forge a clause boundary) |
| **A second instance for a spent situation** | identical repeat **and a new template version** | the reworded retry is refused as hard as the identical one — "a change is a new instance and only via a new situation" |
| **A refused slot leaves no instance behind** | | the situation stays usable; a bad slot value must not permanently burn it |
| **A forged / bare-string situation** | | built on HA-03: the id is re-derived, not trusted |
| **ANTI-VACUITY** | valid instance constructs and validates; a genuinely new situation may create one; render is pure over 50 runs | without these, "refuses everything" would pass every twin above |

## 5. ITEM 3 — the structural proof, and it was shown RED on command

Three checks, AST-based rather than substring, so a docstring discussing R13's
prohibitions is not a hit while a real parameter named `variant` is:

1. **No forbidden import** — model clients, HTTP, `random`/`secrets`, the router, the
   interpreter.
2. **No R13 surface among DEFINED NAMES** — functions, classes, arguments, attributes,
   assignments scanned for `experiment`, `treatment`, `randomiz`, `conversion`, `segment`,
   `variant`, `fallback`, `alternative`, `generate`, `paraphrase`, `tone`, …
3. **The renderer's own body** — the erasure-route shape (`inspect.getsource`, docstring
   stripped) applied to the one function that produces member-facing text.

**A check that cannot be shown red is not load-bearing, so both scans were shown red and
then restored:**

```
RED PROOF A — inject `import random`:
  AssertionError: harness/offer_instance.py imports a model, network or randomness
  interface: ['random']                                         → 1 failed
RED PROOF B — add a `variant` parameter to render():
  AssertionError: R13 forbids these surfaces in the offer path; found:
  ["variant (matches 'variant')"]                               → 1 failed
ANTI-VACUITY — file restored:                                    → 36 passed
```

The module was restored byte-for-byte (`git diff --stat` empty) before anything was
committed.

## 6. WHAT IS ONLY HALF-BUILT, NAMED RATHER THAN IMPLIED

**The spend rule.** R8 spends a situation on PRESENTATION and keeps it spent through
acceptance, decline, non-response, lapse, invalidation, restart and event replay.
**This dispatch enforces only "one instance per situation, ever" at CREATION.** That is
the half item 4 asks for; the rest is §12 step 5 and is not started.

**In-process state only.** `OfferInstanceRegistry` is a dict, like `harness.offer_gate`,
so the guarantee does not survive a process restart. Same limit, stated the same way.

**No template registry exists.** A `FixedTemplate` is validated structurally; there is no
reviewed-template store to check it against — the same honest gap
`harness.purpose_trigger` states about its own unvalidatable fields.

## 7. RUNS (item 7)

| Run | Result |
|---|---|
| Standing battery | **795 passed, 9 xfailed** — 759/9 + exactly the 36 added tests |
| `--layer 7` L7 / L7V2 | **27/27** / **27/28** (1 skipped — the opt-in live-output check) |
| AUDIT / DISC / SCHEMA / VOICE | **8/8 / 1/1 / 1/1 / 1/1** |
| **RATCHET** | **PASS — no scenario regressed vs baseline** |
| Memory harness | **13/17** — failures exactly {MEM-115, MEM-116, MEM-117, MEM-118}, inside the D-109/D-110 pin |

`--full` NOT run; Requirements Discipline item 12 is NOT satisfied and is not claimed.

## 8. ITEM 6 — the new battery registered, and HA-03's mechanism demonstrated

`eval/test_offer_instance.py` added to `scripts/run_harness.sh`. **HA-03's manifest check
was shown catching it first:** with the file present and unlisted, the check failed with
*"neither in scripts/run_harness.sh's standing battery nor in BATTERY_EXEMPT, so they never
run: ['test_offer_instance.py']"*, then passed once registered. **The hazard HA-01 and HA-02
each filed is now demonstrably closed on the first new battery to arrive after it.**

## 9. SCOPE HELD (item 5) AND FINDINGS

**Fixtures only. Nothing presents, nothing initiates, nothing is enabled.** No module
outside `harness/offer_instance.py` changed except the runner's battery list. Nothing HIP
says today changed.

1. **The spend rule is half-built** (§6) — creation only; R8's presentation-time machine is
   step 5.
2. **In-process registry** (§6) — no restart survival, same as `offer_gate`.
3. **No reviewed-template registry exists** (§6) — structural validation only.
4. **`control_flow.py`'s stale "stubs — NOT connected to the pipeline" comment** — carried
   from HA-01 finding 2, HA-02 finding 3, HA-03 finding 4. **Fourth report.** Still outside
   the scope of the dispatch that keeps finding it.
