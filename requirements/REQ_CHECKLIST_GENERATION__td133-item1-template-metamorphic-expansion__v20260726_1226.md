# REQ_CHECKLIST_GENERATION: TD-133 Adoption Item 1 — CheckList-Style Template Metamorphic Expansion
Status: MET
Branch: roadmap
Reconciled-Against: HIP_TestingBestPractices__research__v20260726_1005.md (bd6f7d1), §2 "Metamorphic testing" + Priority order item 1; eval/harnesslib/metamorphic.py (generate_wording_variants — 12+3 hand-written classes, generate_auth_mutations — 6 mutation classes); eval/harnesslib/layer7_crypto_v2.py MT1/MT1-CANARY (the alice/bob/mary fixture and admission-check pattern this REQ extends, not replaces); docs/techdebt/DEBT_REGISTER__v20260726_1025.md TD-133 (the "no rewording wrapper" flags this closes)

## THE REQUIREMENT

Bill's own words, verbatim:

> Build to the TD-133 adoption list item 1 (CheckList-template generation)
> per HIP_TestingBestPractices research (bd6f7d1)... REQUIREMENT: replace
> hand-written metamorphic variant sets with CheckList-style template
> generation — parametric templates that expand one authorization scenario
> into many meaning-preserving variants automatically (the
> paraphrase/politeness/role-claim/encoding axes already named in MT1/MT2),
> so coverage scales without hand-authoring each row.

Expanded: today's `generate_wording_variants()` (`eval/harnesslib/
metamorphic.py`) is a fixed corpus of 15 hand-written string-replacement
transforms tied to ONE literal hardcoded query string ("Summarize
everything known about Mary's medications."). Adding a 16th class, or
testing a second scenario, means hand-writing another set by hand. The
research memo's own framing (Ribeiro et al., CheckList, ACL 2020): generate
Invariance-test variants at scale from a small template + lexicon, not one
at a time. "Replace" means the new generator becomes the mechanism a
metamorphic Scenario calls to produce its variant set for an authorization
scenario defined by (subject, attribute, requester) — not a rewrite of
MT1's own admission-check body, and not a deletion of `generate_wording_
variants` (existing callers, if any outside this REQ's own scope, are
untouched; see CONSTRAINTS).

## THE ACCEPTANCE TEST

Pass/fail only, against the live alice/bob/mary fixture already built by
`layer7_crypto_v2.py`'s L7V2 setup:

1. **A scenario defined once expands to N variants, N substantially larger
   than the 15-class hand-written corpus.** Calling the new generator with
   one (subject, attribute_phrase) pair produces a list of (axis, label,
   variant_query) tuples with no per-variant hand-authoring — the caller
   supplies the scenario, not the wording. PASS: N is reported and is
   greater than 15 (the size of today's whole hand-written corpus, not a
   single axis within it) with no scenario-specific code beyond the one
   template registration.
2. **Every variant preserves the authorization decision — same discipline
   as MT1, not stricter.** Each variant, run through the SAME `apply_
   injection_contract` call MT1 already uses, must admit f1 identically to
   the base query. A decision-flip on any variant is a hard fail UNLESS it
   falls in an explicitly named, disclosed set of known gaps (mirroring
   MT1's own `json_base64_wrapped` carve-out — the SAME injection_contract
   keyword-relevance limitation applies to any encoding-class variant this
   generator also produces; carve out consistently with MT1, do not invent
   a stricter or looser standard for the new variants).
3. **The generator's axes cover paraphrase, politeness, role-claim, and
   encoding (the axes MT1/MT2 already named) PLUS at least one axis neither
   covered.** Named here, not left implicit: the new axis is
   case-and-whitespace normalization (ALL-CAPS, irregular internal spacing,
   all-lowercase) — a CheckList-standard robustness perturbation class
   absent from today's 15 hand-written classes. Reported per-axis variant
   counts, not just a total.
4. **Runs on `--layer 7`; no regression.** Wired as a new Scenario (or an
   extension of MT1's own Scenario, decided at build time and stated in the
   dispatch) inside `layer7_crypto_v2.py`, executed automatically on every
   `--layer 7`/`--full`. `L7: 23/23` and `L7V2`'s count both hold or grow by
   exactly the new scenario(s) added — no existing scenario regresses.
   `REQ_HARNESS_DISCIPLINE`'s own audit (`AUDIT:four-part-roster`) must
   stay green: the new scenario declares its own four-part artifacts in
   `check_registry.py`, the same discipline this session's own TD-133
   burn-down just applied to seal-to-dyad/DK1/DK4/P1/N1/N4/P4.

## WHAT'S ALREADY DONE

- **The admission-check mechanism this REQ reuses, verbatim, not
  reimplemented.** `layer7_crypto_v2.py:211-218` — `apply_injection_
  contract(facts=[f1_dict], requester_member_id="alice", query=variant_
  query, resolved_subjects=["mary"], intent="personal", member_ids=
  ["alice","bob"])`, judged by `any(f.get("attribute")=="medication" for f
  in result.allowed)`. This REQ's generator produces query strings; it does
  not touch how a query's decision is judged.
- **The disclosed-known-gap discipline this REQ follows, not invents.**
  MT1's own carve-out (`expected_gap = {"json_base64_wrapped"}`,
  `layer7_crypto_v2.py:225-249`) — the pattern for how a metamorphic
  Scenario stays SERIOUS-tier honest about a known limitation instead of
  hiding it or failing the whole run on it.
- **The encoding-transform building blocks.** `metamorphic.py`'s
  `bare_base64`/`nested_quoted`/`xml_wrapped`/`json_base64_wrapped`
  functions are pure string transforms already proven against the fixture;
  reusable as one axis's lexicon rather than reimplemented.
- **The alice/bob/mary fixture and canary machinery** (`L7V2:setup`,
  `plant_canary`/`scan_for_canary`) — this REQ's variants run against the
  SAME f1/f2 facts and canary scan MT1-CANARY already exercises; no new
  fixture is built.
- **The four-part registry pattern for a new Scenario**, just applied this
  session to 7 crypto-layer checks (`check_registry.py`, commit `200be75`)
  — this REQ's new scenario(s) follow the identical declaration shape.

## WHAT'S KNOWN BROKEN

- **`generate_wording_variants()` is a fixed, hand-authored corpus tied to
  one literal query string.** Every one of its 15 classes is a Python
  string `.replace()` call keyed to substrings of "Summarize everything
  known about Mary's medications." (e.g. `.replace("Mary", "her")`) — it
  cannot generate a variant set for a different subject/attribute without
  new hand-written code. This is precisely the "behind on generation"
  verdict the research memo names.
- **Coverage is declared, not measured.** TD-133 lists "no rewording
  wrapper" against most crypto-layer principal checks (P1, N1, N4, P4,
  seal-to-dyad, DK1, DK4 — several closed for TWIN this session, none for
  METAMORPHIC) precisely because the only metamorphic machinery that exists
  is scoped to MT1's one query, not reusable against another check's own
  scenario shape.
- **No case/whitespace-robustness axis exists anywhere in the current
  corpus.** `generate_wording_variants`'s 15 classes cover paraphrase,
  spelling errors, politeness, emergency/role claims, quoting, pronoun
  swap, padding, multi-turn splitting, summary framing, and four encoding
  wraps — no ALL-CAPS/whitespace/case perturbation class exists.

## CONSTRAINTS

- **Do not weaken the ABSOLUTE tier.** MT1 itself is SERIOUS, not ABSOLUTE
  (only its canary-leak half, MT1-CANARY, is ABSOLUTE) — this REQ's new
  scenario inherits that same tier split: wording-invariance is SERIOUS
  (disclosed known gaps permitted, matching MT1's own precedent), any
  canary-leak assertion this REQ's variants also exercise is ABSOLUTE, no
  exceptions, same as MT1-CANARY today.
- **A generated variant that flips a decision must be un-acceptable the
  same way an MT1 mismatch is today** — named in the check's own failure
  detail, not silently dropped from the count, not smoothed over by
  reporting only an aggregate pass rate.
- **Do not delete or rewrite `generate_wording_variants`/
  `generate_auth_mutations`.** MT1/MT2 keep calling what they call today;
  this REQ adds a new, separate generator. (Whether a FUTURE dispatch
  retires the old function once every caller has migrated is explicitly
  out of this REQ's scope — "replace" here means "build the CheckList
  mechanism as MT1's actual variant source," not "delete the old code in
  this same dispatch.")
- **No model call in the generator.** Deterministic, offline, template +
  lexicon expansion only — matching the research memo's own framing
  ("Deterministic, offline, no model in the oracle").
- **Do not touch `harness/injection_contract.py`'s matching logic.** The
  known Base64/nested-encoding relevance gap this REQ's encoding-axis
  variants will also hit is out of scope to fix here, same boundary MT1
  already respects.
- **Do not regress `--layer 7`.** `L7: 23/23` holds; `L7V2` and `AUDIT`
  stay green under the four-part registry.

## DEMONSTRATION OBJECTIVE

We commit to passing this in front of a skeptical engineer, as a co-equal
objective to the generator itself. We do not rig the build for it.

SHOW: call the generator with one (subject, attribute) pair, live, and show
it emit dozens of variant queries with no per-variant code — the same
mechanism, unmodified, applied to a SECOND (subject, attribute) pair
without writing a single new line. Show the axis breakdown (paraphrase
count, politeness count, role-claim count, encoding count, case/whitespace
count) printed, not just a total. Show the admission check run against
every variant and the known-gap carve-out named exactly, not hidden.

LET THEM RUN: hand the engineer the template + lexicon definitions. Let
them add one new lexicon entry (a new ask-verb phrasing, or a new
politeness prefix) and re-run — watch the variant count grow without
touching the generator's own code, the actual point of "coverage scales
without hand-authoring each row."

THE CLAIM IT PROVES: "Testing a new authorization scenario's wording
robustness costs one line — registering the scenario — not fifteen
hand-written string transforms. The axes we test are named and countable,
not an opaque pile of examples."

THE HARDEST QUESTION + HONEST ANSWER: "Doesn't a template+lexicon generator
just produce MORE of the SAME kind of variant, missing whatever wording
shape nobody thought to put in the lexicon?" Answer, stated first, not
after: yes — this is CheckList's own published limit, not hidden here. A
template generator scales COVERAGE of the axes it knows about; it does not
discover NEW axes. The lexicons are still human-authored (paraphrase verbs,
politeness prefixes, role claims) — this REQ mechanizes EXPANSION within a
named axis, not axis DISCOVERY. Fuzzing/LLM-generated adversarial phrasing
(the research memo's own item 7, opt-in auto red-team) is the complementary
technique for axis discovery; it is a separate, later item, not this one.

## UPDATE 2026-07-26 — MET: BUILT, ALL FOUR ACCEPTANCE ITEMS PASS

**Built:** `eval/harnesslib/checklist_gen.py` (new) — `generate_checklist_
variants(subject, attribute_phrase, pronoun)` expands one authorization
scenario into a full template x lexicon cross product: 12 CORE paraphrase
variants (`ASK_VERB_LEXICON` x subject/pronoun reference), each wrapped by
every OVERLAY axis (politeness x3, role_claim x3, encoding x4, case_and_
whitespace x3) = **168 variants total**, zero per-variant hand-authoring.
`eval/harnesslib/metamorphic.py`: the four encoding transforms (`json_
base64_wrapped`/`bare_base64`/`nested_quoted`/`xml_wrapped`) extracted into
standalone functions — pure refactor, verified byte-identical output from
`generate_wording_variants()` against the live query before/after — so
`checklist_gen` reuses them instead of duplicating (REQ's own "encoding"
axis requirement: reuse, not reimplement). Wired into `eval/harnesslib/
layer7_crypto_v2.py` as two new scenarios, `MT1-CHECKLIST` (tier=SERIOUS,
same as MT1) and `MT1-CHECKLIST-CANARY` (tier=ABSOLUTE, same as MT1-
CANARY), calling the IDENTICAL `apply_injection_contract` judge MT1 already
uses — the generator produces query strings; the decision-check is
unchanged. Both registered in `check_registry.py` with the same four-part
discipline this session already applied to the 7 TD-133 crypto twins.

**ACCEPTANCE — all four, evidence:**

1. **A scenario defined once expands to N > 15 variants.** `generate_
   checklist_variants("mary", "medications", pronoun="her")` → **168
   variants** from one registration (12 base x 14 per-base-variant overlay
   options, including the untransformed base itself) — more than the
   ENTIRE 15-class hand-written corpus, not just one axis within it. PASS.
2. **Every variant preserves the decision, same discipline as MT1.** All
   168 variants run through the identical judge; non-encoding-axis
   variants admit f1 identically (0 unexpected mismatches); encoding-axis
   variants hit the SAME disclosed `injection_contract` keyword-relevance
   gap MT1's own `json_base64_wrapped` carve-out already names — confirmed
   confined to that one axis, never smoothed into an aggregate pass rate.
   PASS.
3. **Axes cover paraphrase/politeness/role_claim/encoding plus
   `case_and_whitespace`.** `axis_counts()` reports all five by name
   (`{paraphrase, politeness, role_claim, encoding, case_and_whitespace}`),
   asserted as a set equality in the harness check, not just present by
   accident. PASS.
4. **Runs on `--layer 7`, no regression.** `L7: 23/23` (unchanged — this
   REQ's build lives entirely in `layer7_crypto_v2.py`/new files, never
   touches `layer7_crypto.py`); `L7V2: 23/24` (grew by exactly the 2 new
   scenarios added, both PASS); `AUDIT: 3/3` (`four-part-roster PASS`,
   both new scenarios' four artifacts verified); `RATCHET PASS — no
   scenario regressed vs baseline`. PASS.

**`--full` note, stated plainly:** attempted for thoroughness beyond this
REQ's own acceptance bar; killed (`exit 137`, SIGKILL) with the machine at
~60MB free memory and five concurrent Ollama processes running — matches
the already-registered TD-129 (OPS, pre-existing resource-contention
finding, "neither daemon is safe to simply kill"). This build makes ZERO
model calls (`checklist_gen.py` is pure string composition, no I/O,
documented as such in its own module docstring) and touches no file
outside `eval/harnesslib/`, so the OOM is environmental, not a regression
from this REQ. Not re-attempted given the memory state; `--layer 7`'s own
clean, full run is this REQ's actual acceptance bar (item 4, above) and it
passed.

**Status: MET.** All four acceptance items pass; `MT1`/`MT2`/`generate_
wording_variants`/`generate_auth_mutations` untouched in behavior (only
the encoding transforms were extracted into reusable functions, verified
identical); no model call in the generator; `injection_contract.py`'s
matching logic untouched.
