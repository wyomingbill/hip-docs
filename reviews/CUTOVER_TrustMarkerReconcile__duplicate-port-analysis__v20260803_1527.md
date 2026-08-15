Source: this session's own read-only analysis (not an external reviewer)
Subject: the duplicate trust-marker port analysis — reconciling two independent, unmerged
ports of the same hip-vo change (demo-cutover-build's own port vs roadmap's separate
same-day port), which version should survive and what is lost dropping the other
Version: v20260803_1527 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED / VERIFIED-BY-EXECUTION — read-only, but every claim below was produced by
diffing and reading the actual committed code on both branches, not by reasoning about it
secondhand. No lock was taken and nothing was committed or edited by the original dispatch.
REQ: NONE PROPOSED by this filing.
Source file: cutover5_reconcile.md (~/Downloads), banked verbatim, unedited below this line.
Date: 2026-08-03

---

# Index Cutover 5 — Reconciling the duplicate trust-marker port

Read-only. No lock taken, nothing committed, nothing edited on either tree. All evidence
below is either a direct `git show`/`git diff`/`git merge-tree` read, or a real function
call against each checkout's own unmodified, already-committed code (both checkouts left
exactly as found — verified by `git status --porcelain` on both being clean throughout).

Two commits compared:
- **roadmap `14811f3`** — "D-114: port the trust marker from hip-vo — write-time labels
  reach the prompt" (a different session), on branch `roadmap`.
- **demo-cutover-build `586b046`** — "D-114 (WIP): provenance-caveat marker + Epistemic
  State panel ported — UNVERIFIED" (this lane), on branch `demo-cutover-build`.

Both fork from the same base, `2f69f2f` (confirmed via `git merge-base roadmap
demo-cutover-build`), and both port hip-vo's `517dd7c`.

---

## 1. Do both touch the same three parts?

| Part | roadmap `14811f3` | demo-cutover-build `586b046` |
|---|---|---|
| Trust-level rendering at all 3 sites | **Yes** — same 3 call sites (recent-context `mem`, known-facts, other-subject) | **Yes** — identical 3 call sites |
| Caveat instruction in `PERSONAL_FACT_GROUNDING_GUARD` | **Yes** — but composed dynamically, f-string-interpolated from `_TRUST_MARKERS` (`f"\"{_TRUST_MARKERS['ASSERTED'].strip()}\""` etc.) | **Yes** — hardcoded literal bracket text, duplicating `_TRUST_MARKERS`'s own strings |
| Header fix ("Confirmed facts about other people" → "Facts about other people") | **No — deliberately skipped.** Commit message states why explicitly (see §3) and flags it open in its own dispatch doc | **Yes** — `SECTION_OTHER_PEOPLE`'s value changed; live-verified working in Cutover 4 |

**Header line, printed from both, verbatim:**

roadmap `14811f3` (`harness/orchestrator.py`, unchanged from before the port):
```
SECTION_OTHER_PEOPLE = "Confirmed facts about other people"
```

demo-cutover-build `586b046`:
```
SECTION_OTHER_PEOPLE = "Facts about other people"
```

---

## 2. Are the trust markers formatted identically?

The `_TRUST_MARKERS` dict **values** are byte-identical between the two (diffed directly,
zero delta). For a fact with real provenance fields, both render identically. Confirmed by
calling each checkout's own `_fact_trust_marker` directly, same input dict, both trees:

**Full-provenance fact (`write_state="supersede"`, `confidence="medium"`, etc.) — both
checkouts, byte-identical output:**
```
medication: Jardiance 10mg  [asserted: reported and confirmed within the household, not verified against an outside source]
```

**They diverge on a field-less dict — a fact with `attribute`/`value` but none of the five
classifier fields (`derived`, `confirmed_by`, `confidence`, `write_state`,
`confidence_log`):**

roadmap `14811f3`:
```
preference: likes jazz
```
(renders flat — `_TRUST_FIELDS` guard: "a dict carrying NONE of them has no provenance to
classify")

demo-cutover-build `586b046`:
```
preference: likes jazz  [unconfirmed report]
```
(calls `classify_trust_props` with all-empty/default args anyway; that function's
last-resort fallthrough is `return "UNCONFIRMED"` — confirmed by reading
`memory_engine/trust.py` directly — so a fact with **zero** provenance data gets a
**fabricated** "unconfirmed report" caveat, not an honest "nothing to say about this.")

This is exactly the failure mode Bill named: not a merge conflict, a silent wrong-rung
render. On the Epistemic State panel this would show as a spurious UNCONFIRMED
(bottom-rung, red-flagged) card for a fact that was never actually reported with any
trust signal at all — worse than showing nothing.

Whether this scenario is actually *reached* by any live call path today was not
independently traced in this dispatch (read-only, no code tracing beyond what's needed to
explain the divergence) — the risk is attributed to roadmap's own commit message ("session/
Zep-era shapes" hit this), not independently confirmed against the current call graph.

---

## 3. Does either contain anything the other lacks?

**roadmap `14811f3` has, that demo-cutover-build lacks:**
- The `_TRUST_FIELDS` field-less-dict guard (§2) — a real correctness hardening.
- Single-source-of-truth composition: the guard's bracketed-note examples are generated
  FROM `_TRUST_MARKERS` by f-string, not duplicated as literal text — explicitly citing
  TD-137 (this exact "duplicate the string, let a copy drift" failure class) as the reason.
- A new standing test suite, `eval/test_trust_marker.py` — 9 cases (`CONF-MARKER`), wired
  into `scripts/run_harness.sh` as the 20th battery — covering both render sections, flat
  rendering for CONFIRMED, one-place-ness, the field-less twin + its inverse (a real
  UNCONFIRMED fact IS marked), DERIVED/CORROBORATED mapping, and an AST rung-alignment
  anti-vacuity check (which caught a real bug in the port on its first run).
- A full harness run against the change: 20 batteries, 306 passed / 1 skipped / 8 xfailed,
  AUDIT 8/8, L7 27/27, L7V2 27/28, RATCHET PASS, 0 scenario FAILs, mutation self-test
  confirmed, memory harness held at its pinned 15/17. demo-cutover-build's port has never
  been run through this harness at all.
- Explicit grounding in `REQ_CONFIDENCE_DISCIPLINE` and a stated relationship to
  `harness/answer_mode.py`'s `AnswerMode` (already-built mode-side half; this is named as
  the prompt-side half of the same requirement) — one of Bill's four roadmap governance
  advances, connected explicitly rather than left implicit.
- The deliberate, reasoned decision to leave the header alone and flag it as its own open
  item, rather than change something feeding a check-registry-pinned literal without
  reconciling that check in the same change.

**demo-cutover-build `586b046` has, that roadmap `14811f3` lacks:**
- **The header fix itself** — live-verified working end to end in the prior dispatch
  (Cutover 4): the prompt header now reads "Facts about other people," and both an
  ASSERTED and a DERIVED fact render correctly bracketed underneath it, neither as bare/
  confirmed. Roadmap's version still says "Confirmed facts about other people" over lines
  that can now carry non-CONFIRMED markers — the exact mislabel 517dd7c's header rename
  existed to fix, still live on roadmap.
- **The entire Epistemic State panel** (`server/static/demo.html` — `EPISTEMIC_RUNGS`,
  `EpistemicRungRow`, `EpistemicRecordCard`, `EpistemicFactPanel`, ~120 lines). Roadmap's
  `14811f3` touches only `harness/orchestrator.py` + `eval/test_trust_marker.py` +
  `scripts/run_harness.sh` + docs — confirmed via `git show --stat 14811f3`, zero touch to
  `demo.html`. This is C5, a separate acceptance row from the trust-marker port itself, and
  roadmap has no equivalent of it at all.

**A concrete gap on roadmap's side this comparison surfaces:** with the header left
unfixed, roadmap's own C2-shaped claim — "no fact renders under Confirmed unless it
actually is" — is **still false** on `roadmap` HEAD today, exactly as it was before
`14811f3`. The trust-marker port makes the facts UNDERNEATH the header honest; the header
ITSELF is still the pre-517dd7c mislabel, by roadmap's own explicit, reasoned choice
pending a ruling.

---

## 4. Rebase conflicts

`git merge-base roadmap demo-cutover-build` → `2f69f2f` (the known fork point). Simulated
with `git merge-tree --write-tree c0bca12 586b046` (git 2.50, real 3-way merge computation,
touches no ref, no working tree, no index):

```
CONFLICT (content): Merge conflict in harness/orchestrator.py
```

**Exactly one file conflicts, two hunks, both inside the SAME guard text** — the
dynamically-composed vs. hardcoded bracketed-note examples (§1):

```python
    "=== IF A LISTED FACT CARRIES A BRACKETED NOTE (separate rule — read carefully) ===\n"
<<<<<<< c0bca12
    "Some bullet points end with a bracketed note, like "
    f"\"{_TRUST_MARKERS['ASSERTED'].strip()}\", "
    f"\"{_TRUST_MARKERS['CORROBORATED'].strip()}\", or "
    f"\"{_TRUST_MARKERS['UNCONFIRMED'].strip()}\". These "
=======
    "Some bullet points end with a bracketed note, like \"[asserted: reported and "
    "confirmed within the household, not verified against an outside source]\", "
    "\"[backed up by more than one source]\", or \"[unconfirmed report]\". These "
>>>>>>> 586b046
    "facts ARE listed — always state them. Then add a short provenance note in "
    ...
    "bracketed note. Two examples:\n"
<<<<<<< c0bca12
    f"  - For a fact marked \"{_TRUST_MARKERS['ASSERTED'].strip()}\": state the fact, then "
    "add: \"That's based on a report confirmed within the household, not yet "
    "checked against an outside source like a clinic — so it's held as reported, "
    "not verified.\"\n"
    f"  - For a fact marked \"{_TRUST_MARKERS['CORROBORATED'].strip()}\": state the "
=======
    "  - For a fact marked \"[asserted: reported and confirmed within the "
    "household, not verified against an outside source]\": state the fact, then "
    "add: \"That's based on a report confirmed within the household, not yet "
    "checked against an outside source like a clinic — so it's held as reported, "
    "not verified.\"\n"
    "  - For a fact marked \"[backed up by more than one source]\": state the "
>>>>>>> 586b046
    "fact, then add: \"That's backed up by more than one source, though not "
    ...
```

Both sides render to the **same output text** — this conflict is purely mechanical
(f-string-composed vs. hardcoded-literal), trivially resolvable by keeping either side's
expression form.

**What git does NOT flag — and both are real hazards a clean rebase would hide:**

1. **Silent duplicate definitions.** `_TRUST_MARKERS` and `_fact_trust_marker` are each
   defined **twice** in the merge-tree result — roadmap's version (with the `_TRUST_FIELDS`
   guard) lands first in the file, demo-cutover-build's version (without it) lands second,
   a few dozen lines later, with no conflict marker anywhere near either — git's line-based
   diff sees them as two independent, non-overlapping insertions, not the same edit made
   twice. Python's later-definition-wins semantics at module scope mean **the SECOND
   `def _fact_trust_marker` silently shadows the first at runtime** — in this merge
   direction, that's demo-cutover-build's weaker (no field-less guard) version winning,
   invisibly, over roadmap's hardened one, even though both are sitting right there in the
   file. Resolving the two printed conflict hunks alone does **not** fix this — an
   unstated third step (deleting one whole duplicate definition) is required and nothing
   in `git rebase`'s own conflict-resolution flow would prompt for it.
2. **The header change applies with zero conflict.** `SECTION_OTHER_PEOPLE`'s new value
   auto-merges cleanly — because roadmap never touched that line, there's nothing to
   conflict with. A rebase would carry demo-cutover-build's header fix straight through,
   silently, and with it the `eval/harnesslib/check_registry.py:388-389` fixture-marker
   break (§3's roadmap-side reasoning) — confirmed directly: that check's `L7:CTX-STRIP`
   entry pins the literal source string `'SECTION_OTHER_PEOPLE = "Confirmed facts about
   other people"'` against `harness/orchestrator.py`, and
   `eval/harnesslib/harness_audit.py:629-641`'s marker-validation is a literal
   `in`-substring check against that file's text — it would report `MISSING`, not `OK`,
   the moment the header text changes. Nothing about a rebase's mechanics would surface
   this; only actually running the harness after would.

---

## Which version should survive

**Neither wholesale — the underlying mechanism should be roadmap's, the header fix should
be kept and threaded through properly, and the panel is not part of this choice at all.**

- **The trust-marker/caveat mechanism itself: roadmap `14811f3` is the safer base.** It has
  the field-less-dict guard demo-cutover-build lacks (a real fabricated-caveat risk,
  demonstrated in §2, not hypothetical), composes the guard text from one source instead of
  two copies, and is the only one of the two actually run through the harness (20
  batteries, a dedicated 9-case test suite, RATCHET PASS). Dropping it in favor of
  demo-cutover-build's version means inheriting the field-less fabrication risk and losing
  test coverage that already caught one real bug during its own construction.

- **The header fix is real, live-verified, and correct — and should not be dropped either.**
  Keeping roadmap's version as-is leaves the C2-shaped claim false on roadmap today (§3).
  What's missing is not the fix itself but the follow-through roadmap's own author declined
  to do unilaterally: updating `check_registry.py`'s pinned literal (and re-running
  `L7:CTX-STRIP`) in the SAME change that renames the header, so the AUDIT stays honest
  instead of either staying red or silently drifting. That reconciliation — not a ruling on
  which port wins — is what's actually blocking the header fix from landing safely on
  roadmap's mainline.

- **The Epistemic State panel is orthogonal to both and unique to demo-cutover-build.**
  It's C5, not part of "the duplicate port" — roadmap has nothing to compare it against.
  Whichever trust-marker implementation is kept, the panel isn't at stake in that choice
  and has no counterpart to lose.

**What's lost by dropping demo-cutover-build's orchestrator.py port specifically:**
nothing that isn't already better-covered on roadmap, except the header fix — which is
worth carrying over deliberately (with its check_registry follow-through) rather than
inherited as a side effect of picking one branch's file wholesale over the other's.

**What's lost by dropping roadmap's port instead:** the field-less-dict correctness
guard, the single-sourced guard text, and the only test/harness evidence either port has —
a materially worse position than the reverse.
