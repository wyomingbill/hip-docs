# DISPATCH_D21_D23
Status: BUILT (partial — see BLOCKED and RESIDUAL below)
Reconciled-Against: (uncommitted at time of writing — see HASH)

**TYPE:** BUILD + MEASUREMENT

**REQ:** `docs/requirements/REQ_D21_D23__canonical-attribute-enum-expansion-and-seed-schema-validation__v20260717_1200.md`

## THE ASK

Bill's schema decision, four parts, quoted in full in the REQ doc. Summary:
(1) add `incident`/`medication_status` to `CANONICAL_ATTRIBUTES`; (2) skip
`risk_pattern` on purpose; (3) fix D10/D11 as a seed bug (`household`, not
`address`/`zone_district`); (4) validate the seed path against the same
enum. Prove live: (a) 20x "Dad had a fall..." lands, Neo4j-verified; (b) the
24-utterance corpus stays 24/24; (c) an out-of-enum seed attribute is
refused loudly; (d) Script 1's frontier payload still builds from D10/D11;
(e) `--full` passes. "D-21 should go green. If it does not, stop and report
why."

**This report stops and reports why, on two of the five items.** Read
before assuming D-21 is closed.

## WHAT WAS DONE

1. **`harness/extraction_queue.py`**: `CANONICAL_ATTRIBUTES` gained
   `incident` and `medication_status` (13 values total). `risk_pattern`
   deliberately absent, with a comment stating why (DERIVED, never spoken,
   never detector output — Bill's call, item 2).
2. **`harness/injection_contract.py`** (companion fix, not explicitly named
   in the ask but directly implied by "D-21 closes when it lands" — see
   REQ's WHAT'S KNOWN BROKEN): added `_ATTR_KEYWORDS` regex entries for both
   new attributes and added both to `_TARGETED_ATTRS` (INJ-6b). Without
   this, a written `incident`/`medication_status` fact would be write-legal
   but read-invisible — the same defect class already found and fixed once
   for `appointment` (PW023-25/TD-120 D3).
3. **`scripts/demo_seed.py`**: `_seed_one` now raises `ValueError` before
   any write if a fixture's `attribute` is outside `CANONICAL_ATTRIBUTES`
   and the fixture's label isn't on `_ENUM_EXEMPT_LABELS`. D8 is the
   permanent exemption (risk_pattern/DERIVED). D10/D11 are a **temporary**
   exemption — see BLOCKED below; this is not the same shape as D8 and the
   comment in the file says so.
4. **`eval/oracle/disclosure_oracle.py`**: `FIXTURE`'s D10/D11 entries are
   unchanged from before this session (see BLOCKED) — kept in sync with
   the seed, which is also unchanged for those two.

## BLOCKED: item 3 (D10/D11 → `household`)

**Not applied. Reverted after live-testing it broke the fixture.**

Live-tested this session: setting both D10 and D11 to
`attribute="household"` and running `fixture.reset("standard")`
immediately raised:

```
SystemExit: FIXTURE DRIFT: D7 value mismatch — registry
'trash pickup is Wednesday' vs graph 'TBD'.
```

Root cause: `eval/harnesslib/fixture.py`'s `_key_facts`/`verify_seed` match
facts on `(owner, subject, attribute)` **only**, and assert exactly 1 active
row per triple, per fixture. D7 already owns `(household, household,
household)` — "trash pickup is Wednesday." Setting D10 and/or D11 to the
same attribute string creates 2 or 3 facts at the identical triple, which
`verify_seed` cannot disambiguate; it silently reads back whichever row the
query happens to return first, not necessarily the one being checked.

This is not the same finding as `DISPATCH_ENUM_AUDIT`'s original D10/D11
note (a live-utterance supersession risk, never tested). It is a harder,
immediate problem: **the fixture-verification mechanism itself has no way
to hold more than one household-owned fact under one attribute name.**
Bill's stated reasoning ("household already covers address and zone
district") is correct as a *classification* claim about what the live Groq
detector would produce — but the harness's own seed/verify layer needs a
finer key than `attribute` alone to keep multiple co-existing household
facts distinct, and that's a data-model question, not a string-rename.

**Reverted, not silently worked around:** D10/D11 are back to their
original literal attributes (`address`, `zone_district`), temporarily added
to `_seed_one`'s `_ENUM_EXEMPT_LABELS` (with a comment marking this as
on-hold, not permanent, distinct from D8's real exemption), and
`disclosure_oracle.py`'s copy is unchanged to match. The dev graph was
restored to a clean, `verify_seed`-passing baseline after the failed test
(confirmed: `RESET+SEED+VERIFY: OK`).

**This is Bill's call, not mine to route around.** Options as I see them,
not chosen here:
- Give D10/D11 a real distinguishing key beyond `attribute` (e.g., the
  live detector already writes a `subject`/value — but owner=subject=
  household for both; would need either separate attributes that both map
  to `household`'s semantic scope without colliding, or a schema change to
  `_key_facts`/`verify_seed` to key on `(owner, subject, attribute, ...)`
  plus something else).
- Keep D10/D11 as literal `address`/`zone_district` permanently (the
  original D-23 finding stands: a live utterance would file under
  `household` and not supersede these rows — a known, documented,
  accepted gap rather than a fixed one).
- Something else Bill decides. Not guessed here.

## RESIDUAL: item (e), `--full`, and whether D-21 is "green"

**`--full` does not cleanly pass. `L2:three_zone_demo.T02` (D-21's own
scenario) still fails — for a different reason than before, not the
original one.**

### What's proven fixed

The **structural, deterministic, 100%-both-temperatures** miss that WAS
D-21 is conclusively gone. Three independent pieces of evidence:

1. A single, isolated, unhurried live turn against the real server
   (`server.post_turn`, real Groq, real Neo4j, `time.sleep(3)` before the
   turn so this is not a rapid-loop artifact) produced a genuinely new
   Neo4j fact: `fact_id=60f3308d-ef4b-4ab6-b306-1bf2405c498e,
   attribute=incident, write_state=augment`.
2. A direct synchronous call to `harness.fact_change.detect_and_apply`
   (bypassing the async wrapper entirely) completed in 4.6s with
   `mutations=1`, `delta=[{subject: dad, attribute: incident, ...,
   transition: supersede, ...}]`.
3. A full re-run of the *exact* frozen-context, read-only measurement
   script from `DISPATCH_DETECTION_MISS_MEASUREMENT` (unmodified — same
   file, same methodology, so this is an apples-to-apples comparison to
   the original "20/20 miss, 0% recovery" number): **17/20 direct hits at
   temp=0.0, 3 misses, 2 of the 3 recovered by the temp=0.2 retry — net
   19/20 (95%) after retry**, versus 0/20 (0%) before this fix. The
   24-utterance aggregate corpus stayed **0/24 misses — no regression**
   (item b, satisfied cleanly).

Also live-verified: 20 independent (reset → seed → live turn → Neo4j read)
cycles all landed a real, distinct fact (`docs/dispatches/d21_live_proof_script__v20260717_1230.py`,
raw results in the sibling `.json` file) — 20/20 by that measure. Read
together with #3 above: the enum change made the fact reliably detectable
and writable; it did not make it perfectly deterministic, and it was never
going to — the schema gap was the 100% blocker, and closing it exposes
whatever ordinary, non-zero stochastic miss rate this utterance has, same
as everything else Groq classifies.

### What's NOT fixed, and not something this REQ's scope reaches

`three_zone_demo.T02`'s harness check (`required_present: ["dad"]` in the
reply text) still fails on the current `--full` run. Traced, not guessed:

- Server log for that turn: `WARNING:harness.fact_change: zero changes for
  owner=sam — retrying detect once at temperature=0.2`, followed by
  `TD-121 F3: declarative produced no write (proposed=%s mutations=%s
  noops=%s) — replacing ack with unconfirmed reply` (the `%s` placeholders
  print literally uninterpolated in this codebase's logger — a separate,
  minor, pre-existing logging defect, not touched here).
- Reply shipped: `UNCONFIRMED_UPDATE_REPLY` ("I heard that as an update,
  but I was unable to save it... Nothing was changed"). Neo4j, checked in
  the same turn, shows the write DID land (see evidence #1 above, same
  turn). **The reply is false in the opposite direction from before**: pre-
  fix, nothing landed and (per the original D-21 finding) the ack didn't
  say so correctly either; post-fix, on an unlucky trial, something lands
  and the ack claims it didn't.
- This is the residual ~1-in-20 stochastic miss from evidence #3 above,
  hitting the live async path on this specific `--full` run. It is not
  reproduced by every call (my direct test above got mutations=1 on the
  first try) — it is exactly as unreliable as an ordinary LLM detection
  call, which is the point: the schema block that made it 100% reliable-
  *wrong* is gone, replaced by whatever background reliability rate this
  utterance now shares with the rest of the corpus (evidence #3's 95% net,
  not 100%).
- **This looks like the same family as I-10/H-06** (`HIP_DefectRegister`:
  "nondeterministic LLM detection step, DETECT_WAIT_S timeout-sensitive"),
  not a new defect and not a re-emergence of D-21's schema gap — but I have
  not proven that identity, only the family resemblance (a detection
  outcome the F3 gate reads as zero-mutation when the graph shows
  otherwise). Flagged as a hypothesis, not confirmed, per this repo's own
  discipline on that distinction.

**I am not marking D-21 green in the register.** The schema-gap root cause
is fixed and proven three independent ways. The demo script's own
assertion is not yet reliably passing, and `--full` — read for real, not
skipped per CLAUDE.md item 12 — shows exactly that. Marking it green would
be the same mistake this whole engagement exists to catch: trusting a
reply-shaped signal over the graph.

## REGISTER UPDATES (this dispatch)

- `HIP_DefectRegister.md` D-21: root cause (schema gap) marked FIXED and
  triple-verified; scenario-level pass NOT yet clean, residual stochastic
  miss documented, cross-referenced to I-10/H-06 as a hypothesis.
- `HIP_DefectRegister.md` D-23: items 1/2/4 FIXED (enum widened, risk_pattern
  excluded on purpose, seed-path validation added + INJ-2/6b companion);
  item 3 (D10/D11) explicitly BLOCKED, not fixed, with the fixture-key
  finding above; not silently dropped.
- `docs/BACKLOG.md` rows 15/15b updated to match.
- `TD-125`: unaffected by this dispatch, no new information.

## HASH

Not pushed. Per CLAUDE.md item 12 and this REQ's own CONSTRAINTS ("if
`--full` shows a NEW failure this change caused, stop and report it rather
than shipping past it") — `--full` does not cleanly pass, and item 3 is an
open data-model question, not a decision I made unilaterally. Committed
locally so the verified, working parts (items 1/2/4, live proofs a/b/c) are
not lost; not pushed pending Bill's call on the two open items above.

## CROSS-REFERENCE

While this REQ was in progress (uncommitted), a parallel REQ landed on top
of it: `docs/requirements/REQ_FRONTIER_TIER__script1-t04-t05__v20260717_1215.md`
(commit `3f8e0f9`, 12:12) independently cites this session's working D10/D11
diff and the same D7/`verify_seed` collision, and corrects its own stale
"D10/D11 migrating to household, already decided" premise on the strength
of it. No conflict — that REQ's payload-builder design (key on `fact_id`,
never on the attribute string) is consistent with, and strengthened by,
this dispatch's finding that the migration is blocked, not just unlanded.

## OPEN, FOR BILL

1. **D10/D11 disambiguation.** `household` is semantically right per your
   own reasoning; the harness's fixture-verify layer can't hold 3 facts
   under one attribute today. How do you want this resolved — see the
   three options sketched in BLOCKED above, or something else?
2. **The residual stochastic miss on `three_zone_demo.T02`.** Accept it as
   the same ordinary reliability rate the rest of the corpus has (document
   the ~95% net rate, same as any other detected fact, and let `--full`
   flake on it exactly as it already does for I-10-family issues)? Or is
   this worth a dedicated retry-of-the-retry / detection-reliability pass
   before D-21 is called closed? Not decided here.
