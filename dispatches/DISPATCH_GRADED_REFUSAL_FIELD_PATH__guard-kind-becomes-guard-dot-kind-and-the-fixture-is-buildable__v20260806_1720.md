# DISPATCH_GRADED_REFUSAL_FIELD_PATH — `guard_kind` becomes `guard.kind`, and §6 is buildable

Status: BUILT
Reconciled-Against: roadmap `3a956a9` (pre-amendment HEAD). **LANDED AT `614dfe5`** — backfilled by the immediately following commit, because a commit cannot contain its own hash.

**HA-05** | 2026-08-06 | `~/hip-roadmap`, branch `roadmap` | TYPE: **DOCS ONLY — REQ amendment**
**REQ AMENDED:** `docs/requirements/REQ_RECORD_GRADED_REFUSAL__refusal-checks-assert-on-the-execution-record__v20260802_0744.md`
**NO CODE CHANGED. NOTHING MARKED MET.**

---

## BILL'S RULING, VERBATIM

> "Ruling, Bill 2026-08-06: fix §6's field path — guard_kind becomes guard.kind everywhere
> in the REQ including acceptance wording, amended in place citing HA-04, prior wording
> preserved per the same pattern. A fixture must be buildable from §6 as written against a
> real record."

**This closes the item HA-04 flagged and deliberately left.** The annotation cites HA-04, as
instructed; the work is recorded as HA-05 because it is its own commit with its own
evidence.

## 1. THE DISCRIMINATION THAT MADE THIS NON-MECHANICAL

`guard_kind` appears in this REQ in **two different senses**, and a blind
find-and-replace would have destroyed the explanation the correction rests on:

| Sense | Example | Action |
|---|---|---|
| **The RECORD FIELD** a predicate reads | acceptance row 1; "reads `path` and `guard_kind` off the record"; §6 rows 1–2 | **CHANGED to `guard.kind`** |
| **The EMITTER'S PARAMETER**, which really is named `guard_kind` | the WHAT'S ALREADY DONE table row: "`guard_kind` \| **NOT EMITTED — 0 of 43 records carry it** \| it is the parameter at `:184`" | **UNCHANGED** |

Rewriting the second sense would have deleted the very row that proves the first was
wrong. **Every remaining `guard_kind` in the REQ was audited by hand**: all are either
quoted prior wording inside an annotation, Bill's own ruling text, the parameter-sense
statements, or explicit warnings that no record carries a top-level `guard_kind`. **No
occurrence now instructs a reader to read `guard_kind` off a record.**

## 2. WHAT CHANGED

- **Acceptance row 1** — now reads `guard.kind`. Bill's original row text is quoted
  verbatim in the annotation beneath it, and the annotation says plainly that the
  substitution is **his instruction, not a session's paraphrase of him** — which is why
  the original is preserved rather than replaced. The old "read it as the CONCEPT" note is
  retired with its reason: **the row now names the literal path a predicate uses.**
- **The framing paragraph** — "a structural refusal has a `guard` block carrying
  `guard.kind` and no inference".
- **WHAT'S ALREADY DONE's reader note** — "reads `path` and `guard.kind` off the record".
- **§6 row 1 (fault twin)** — the twin is now "no `guard` block (`guard_triggered` false,
  `guard` absent)" rather than "`guard_kind` null", because that is what a hedge record
  actually looks like.
- **§6 row 2 (ground-truth fixture)** — replaced with **literal record dicts**, in the
  shape a real record has, plus the explicit rule: *a predicate must read
  `record["guard"]["kind"]`, never `record["guard_kind"]`*.
- **Header** — records this second amendment and states the parameter-sense carve-out, so
  a reader meets both before reaching the body.

87 insertions, 29 deletions. **Every prior wording is preserved verbatim in an annotation
at its own site**, per the pattern this REQ has used since 2026-08-02.

## 3. "BUILDABLE FROM §6 AS WRITTEN" — PROVEN BY EXECUTION, NOT ASSERTED

Bill's condition is testable, so it was tested. The fixtures were **parsed straight out of
the REQ's own §6 code block** — `ast.literal_eval` over the text of the document, nothing
hand-typed — and checked against real records in `logs/turns_demo.jsonl`:

```
fixtures parsed from §6 as written: 5
every fixture key exists on a real record: OK
predicate over the fixtures (want [T,T,T,F,F]): [True, True, True, False, False]
fixture kinds: ['access_control', 'attr_empty_set', 'empty_set'] | live kinds: ['access_control', 'attr_empty_set', 'empty_set']
no top-level guard_kind on any fixture or any of 119 live records: OK

BUILDABLE FROM §6 AS WRITTEN, AGAINST A REAL RECORD: PROVEN
```

Four things that proves, each of which could have failed independently:

1. **The text parses.** The block is literal record dicts, not prose about them.
2. **Every key a fixture uses exists on a real record** — the check that would have caught
   `guard_kind` had it survived.
3. **The prescribed predicate discriminates**: the three structural fixtures are structural,
   and the hedge and boundary fixtures are not. A fixture set that classified everything the
   same way would pass a shape check and be useless.
4. **The three fixture kinds equal the three kinds live records actually carry** — set
   equality against the graph's own log, not against the emitter.

**RE-VERIFIED AGAINST A REAL RECORD, which is this REQ's own rule applied to its own
correction.** `logs/turns_demo.jsonl` in this checkout, 2026-08-06: **119 records, 9
guarded**, kinds `access_control` 2, `empty_set` 5, `attr_empty_set` 2; a sample guard block
is `{"kind": "access_control", "subject": "maya"}`; `inference_ms` null on it; **no record
carries a top-level `guard_kind`.** That is fresh evidence, not the 43-record figure the REQ
recorded on 2026-08-02 — and it independently re-confirms HA-04's three-kinds ruling.

## 4. WHAT WAS NOT DONE

- **No code changed.** The emitter was always right; the REQ's text was wrong twice.
- **`Status: NOT MET` unchanged.** Nothing marked MET, no acceptance row re-tiered.
- **The parameter-sense occurrences left alone** (§1) — deliberately, and stated in the
  REQ's own header so it does not read as an incomplete replace.
- **No standing test added.** The buildability proof above was executed as evidence for
  this dispatch, not committed as a battery: adding one would put a new file under the
  HA-03 manifest check and is beyond a ruling about REQ wording. **Named as a choice, with
  its cost: nothing re-runs this proof automatically, so a future edit to §6 could
  reintroduce an unbuildable fixture silently.**
- **No harness runs** — docs-only, no code touched, none asked for.

## 5. FINDING

**This is the third correction to the same clause family, and the second caused by the same
root.** HA-04 recorded that both of this REQ's earlier errors came from writing acceptance
against the emitter's signature rather than a real record. This one is the same root reaching
a different field: the parameter comment named two kinds where the code emits three (HA-04),
and the parameter NAME was mistaken for the emitted key (this dispatch, and originally
2026-08-02). **The REQ has now stated that lesson three times and been caught by it three
times.** What would actually end it is the standing check named in §4 and not built — a
check that the REQ's own fixture block parses and matches a live record.
