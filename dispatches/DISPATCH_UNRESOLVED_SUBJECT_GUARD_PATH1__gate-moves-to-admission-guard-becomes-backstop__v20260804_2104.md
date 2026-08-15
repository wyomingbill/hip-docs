# DISPATCH_UNRESOLVED_SUBJECT_GUARD_PATH1
Status: BUILT (docs only — a REQ amended, a TD filed; no code touched)
Reconciled-Against: roadmap `c6117c1` (2026-08-04); executed evidence at `d9eac55` on
`demo-cutover-build`

**TYPE:** PROCESS — a requirements amendment enacting a ruling, with a verification pass over
every code claim carried into it. **No code changed. Nothing built. Nothing MET. C9 not ruled.**

**REQ:** `docs/requirements/REQ_UNRESOLVED_SUBJECT_GUARD__sensitive-facts-not-admitted-on-subjectless-turns__v20260804_2104.md`
— written by this dispatch, superseding `...__empty-set-guard-fires-when-no-subject-resolves__v20260804_1333.md`.

**LANE / ID:** Index Demo 26 → roadmap lane (`~/hip-roadmap`) → **D-R-171**. Companion filing:
**TD-R-162**. The prior link in this chain is **D-D-149 / TD-D-148** on the demo lane; both are
cited branch-qualified throughout, per preamble item 10.

## THE ASK

Delivered in two parts. The first arrived truncated mid-item-5 (`"ACCEPTANCE rewritten for the
injection gate: telemetry must show"`) and **this session stopped and said so rather than
inferring the acceptance criteria** — recorded here because the stop is part of the dispatch's
history. Items 1-4 stood as received; item 5 onward arrived in the continuation and is
reproduced in the REQ itself.

Bill's ruling: **PATH 1 — FIX ADMISSION, NOT REFUSAL.**

## WHAT WAS DONE

1. Gate: `bill-ai` / `[REDACTED-MACHINE-NAME]` / `[REDACTED-USER-PATH]/hip-roadmap` / `roadmap`.
   Re-verified at the continuation, by which point HEAD had moved twice (`ddbcad8` → `c6117c1`,
   the other lane finishing R17) — so the ID minted here is D-R-171, not D-R-170.
2. Lock: `hip_lock.py who repo` → **free**, checked before any write and again before git. No
   lane live; nothing waited on behind a parked lock.
3. Tree: in sync with `origin/roadmap`; the cutover lane's four untracked dispatch docs still
   parked, unchanged, and left exactly as found. Explicit pathspecs only.
4. Read D-D-149's dispatch doc first, as instructed — it holds the executed evidence and the
   preserved 76-line INJ-6c patch that item 2 designates as the backstop.
5. **Verified every code claim carried into the TD against this branch at HEAD rather than
   from the prior session's memory** — see VERIFIED.
6. Wrote the new REQ version; marked v20260804_1333 SUPERSEDED with a pointer, body unedited;
   repointed `LATEST_REQ_UNRESOLVED_SUBJECT_GUARD.md`; filed TD-R-162 in a new register version
   and repointed `LATEST_DEBT.md`; registered both in `docs/INDEX.md`; wrote this doc.
7. Committed and pushed with the repo lock wrapping **only** the git commands.

## WHAT THE AMENDMENT SAYS

**The gate moves from refusal to injection.** Facts at `sensitivity >= medium` are not
admitted into `result.allowed` on a subjectless turn; facts below `medium` admit as today. The
refusal-side guard built at D-D-149 is retained as the **backstop** — if a `>= medium` fact
somehow reaches the prompt on that path, the empty-set guard fires. *Defense at the door, alarm
inside.*

**Why the previous version failed is now settled by execution, not argument.** The fix was
built exactly to both of its rulings and passed everything it was specified against — B090
refusing structurally with exact telemetry, DC-061/DC-080 unguarded, conformance 39/39, battery
zero delta — and then refused "What is the capital of Brazil?", because fact `9073c508…`
(`attribute=household`, `sensitivity=medium`, `origin=self_report`) is admitted into every
subjectless turn by design. **The threshold was right; the point in the pipeline was wrong.**

That also **closes the prior version's own OPEN item** — *"whether household facts should be
admitted on a subjectless turn at all"* — with executed evidence rather than analysis.

**Acceptance is rewritten as six telemetry-keyed rows**, (a) through (f), reproduced verbatim
from the ruling in the REQ. Two are worth naming here because they are what make the new
requirement falsifiable in ways the old one was not:

- **(c) — a resolved-subject turn must still carry the `>= medium` fact.** Admission is gated
  by subjectlessness, not removed globally. A build that simply drops the fact everywhere
  passes (a) and (b) and fails (c). Without this row, "delete the fact from every turn" would
  score as a pass.
- **(e) — the backstop is proven fault-twin style**, by *forcing* a `>= medium` fact into
  `result.allowed`. If that condition can be reached without forcing, the admission gate has a
  hole and (a) was not really passing.

**The 7690-dashboard precondition is DISCHARGED** (PID 22932, recorded in D-D-149) and is not
carried forward. The `292/1/8` baseline is corrected to the **293/0/8** this checkout actually
produces.

**The slug changed** — `empty-set-guard-fires-when-no-subject-resolves` →
`sensitive-facts-not-admitted-on-subjectless-turns`. The old slug now names the backstop, not
the requirement, and a filename that misdescribes its own requirement is how a reader builds
the superseded thing. SUBJECT is unchanged, so lineage and the `LATEST_` symlink still resolve.

## TD-R-162 — filed, not fixed

DC-080 stores `f-hh-wifi` = **"wifi password: hunter2"** under `attribute: household`, which
maps to sensitivity **LOW** — an authentication secret at the bottom of the order R29/R30
exists to enforce.

**Neither classification axis can see it, and for the same structural reason: both are
attribute-keyed while the secret is in the value.** R8's `_HARD_REFUSED_ATTRIBUTE_PATTERNS`
matches the attribute NAME (`password`, `pin`, `secret`, …); this fact's attribute name is
`household`, so `classify_representation` returns `ORDINARY_CLAIM`.

**`AUTHENTICATION_SECRET` is dead code against today's write paths**, cited as instructed and
verified two ways: zero attributes in `CANONICAL_ATTRIBUTES ∪ DERIVABLE_ATTRIBUTES` classify to
it, and `store.py:448` raises on `UNKNOWN_HIGH_RISK` **and only that class** — so even a
returned `AUTHENTICATION_SECRET` verdict would be stamped and persisted, not refused.

**The tension is recorded rather than resolved:** the obvious fix — classify on the value — is
what D-50 Principle 6 / R8's RULING 1 forbids, and `representation_class.py`'s own Group-3
reasoning rests on that prohibition. This is not a missing regex; it is a gap between what
attribute-level classification can know and what the ceiling requires. Scope bounded honestly:
DC-080 is fixture data, so nothing leaks in production from this row — but it is one of the two
cases the amended REQ is built to keep passing **unguarded**, so a standing contract case now
asserts that a credential-bearing fact is admitted on a subjectless turn.

## VERIFIED

**Watched run** — every claim in TD-R-162 was executed against roadmap HEAD `c6117c1` this
dispatch, not carried from the prior session:

- DC-080's two facts read directly from `eval/disclosure_conformance.json` — `f-hh-wifi`,
  `attribute: household`, value `"wifi password: hunter2"`.
- `classify_representation(attribute="household", origin="self_report", subject="household")`
  executed → **`ORDINARY_CLAIM`**.
- The classifier executed over the entire `CANONICAL_ATTRIBUTES ∪ DERIVABLE_ATTRIBUTES`
  vocabulary → attributes classifying as `AUTHENTICATION_SECRET`: **`[]`**.
- `AUTHENTICATION_SECRET` defined at `harness/representation_class.py:132`; hard-refused
  attribute patterns at `:160-162`; `store.py:448` confirmed as the sole refusal, on
  `UNKNOWN_HIGH_RISK` only.
- Prior REQ version's body confirmed unedited by diff: **23 insertions, 1 deletion**, the
  single deletion being the `Status:` line.
- Lock state read from the tool, twice, not assumed.

**Reasoned about, not proven here:** that the live graph's `household`-at-`medium` fact was
stamped by TD-D-148's default is the most probable explanation given `origin=self_report` and
the two quoted `or "medium"` sites, but the specific write was never traced to its turn. It is
stated as likely in both the REQ and the register entry, and is exactly why the data question
is filed as OPEN rather than answered. All B090 / battery / conformance figures in this
amendment are **carried from D-D-149's executed run**, cited to that dispatch — this dispatch
re-ran none of them and does not present them as fresh.

## HASH

See the terminal report. Files, all by explicit pathspec:

- `docs/requirements/REQ_UNRESOLVED_SUBJECT_GUARD__sensitive-facts-not-admitted-on-subjectless-turns__v20260804_2104.md` (new)
- `docs/requirements/REQ_UNRESOLVED_SUBJECT_GUARD__empty-set-guard-fires-when-no-subject-resolves__v20260804_1333.md` (Status + pointer only)
- `docs/requirements/LATEST_REQ_UNRESOLVED_SUBJECT_GUARD.md` (repointed)
- `docs/techdebt/DEBT_REGISTER__v20260804_2104.md` (new) + `LATEST_DEBT.md` (repointed)
- `docs/INDEX.md`, and this dispatch doc

The cutover lane's four untracked dispatch docs were **not** staged.

## OPEN

- **The data question, filed as its own OPEN item in the REQ.** The live graph carries
  `household` at `medium` while seed and fixtures say `low`. Whether to correct the stored
  value is a **data-migration decision, separate from this REQ** — and it bears on acceptance,
  since (a) and (b) are measured against whatever the graph actually holds.
- **Which outcome B090 produces** under the gate — honest no-basis answer or backstop — to be
  recorded by the build, not predicted.
- **TD-R-162** needs a ruling on per-fact sensitivity versus the content-blindness rule.
- **TD-D-148** (*on demo-cutover-build*) stays open as the filed deviation.
- **`eval.harness --full` still cannot run in `~/hip-cutover-demo`** — no `.env.dev`, no
  in-checkout registry. Provisioning it is separate work; acceptance row (f) is the pytest
  standing battery, which does run.
- **Nothing ruled MET. C9 not ruled.**
