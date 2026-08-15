Source: this session's own live execution and verification (not an external reviewer)
Subject: header-fix confirmation — verifying roadmap's already-landed SECTION_OTHER_PEOPLE
rename (commit 872ad0c) against three requirements, plus an independent harness run
Version: v20260803_1527 (Mountain Time, per the CLAUDE.md Naming Law)
Status: BANKED / VERIFIED-BY-EXECUTION — the task arrived already landed by another lane;
this filing verifies what's there by reading the actual committed code and running the
harness independently, not by trusting the other lane's own commit message.
REQ: NONE PROPOSED by this filing.
Source file: cutover6_report.md (~/Downloads), banked verbatim, unedited below this line.
Date: 2026-08-03

---

# Index Cutover 6 — Land the header fix on roadmap

**The task arrived already done.** Between your message and my first check of `.hip-lock`,
the other lane landed exactly this work: commit `872ad0c`, "D-117: enact the header
rename — REQ revision first, eight sites, one source" (2026-08-03 08:35:28 MT). I did not
duplicate it. This report verifies what's there against your three requirements and adds
one independent harness run of my own — no new commit was made.

## What actually happened, in order

1. Took `.hip-lock` (no lock held at the time).
2. `git log` showed `872ad0c` already on `roadmap` HEAD, same D-number I'd have used
   (`D-117`) — stopped immediately rather than build on top of or duplicate it.
3. Read the commit in full (`git show --stat` + full message) and verified its actual
   file contents against your three requirements directly — not just trusted the commit
   message's own claims.
4. Ran `eval.harness --layer 7` myself, independently, via the guarded
   `scripts/run_harness.sh` wrapper — not a re-read of the other lane's own `--full`
   results.
5. Wrote this report. Releasing the lock now, nothing pushed.

## Requirement 1 — the header fix only, roadmap's trust-marker mechanism untouched

Confirmed on current `roadmap` HEAD (`872ad0c`):
```
SECTION_OTHER_PEOPLE = "Facts about other people"
```
Roadmap's own `14811f3` trust-marker mechanism (f-string-composed guard text, the
`_TRUST_FIELDS` field-less-dict guard) is untouched by `872ad0c` — confirmed by reading
`harness/orchestrator.py` directly, not inferred from the commit message.

`872ad0c` actually went further than the two-line fix you and I both anticipated: it found
**eight** sites needing the change, not the surveyed seven — a wrap-tolerant AST scan
caught an eighth wrapped occurrence in `eval/harnesslib/layer7_crypto.py` (a CTX-STRIP
check label) that a plain grep would have missed. Confirmed directly:
```
$ grep -n "SECTION_OTHER_PEOPLE\|Facts about other people" eval/harnesslib/layer7_crypto.py
1643:            SECTION_OTHER_PEOPLE as _ctx_other_header,
```
Now imports and interpolates the constant instead of carrying its own hardcoded copy.

A broad grep for the old literal across the whole tree confirms zero remaining
occurrences in live code:
```
$ grep -rn "Confirmed facts about other people" --include="*.py" .
(no output)
```

**One thing worth naming plainly: `872ad0c` also filed a REQ revision first**
(`REQ_STRIP_CONTEXT_COMPLETENESS`, superseding the prior MET-ruled version, filed NOT MET,
proposing a re-ruling) — process this dispatch's own three-item instruction didn't ask for,
but which matches this repo's own Requirements Discipline gate (no code change without a
REQ naming it) more strictly than a bare header-string edit would have.

## Requirement 2 — the check_registry.py update

Confirmed:
```
$ grep -n "SECTION_OTHER_PEOPLE\|Confirmed facts\|Facts about other people" eval/harnesslib/check_registry.py
395:            _ORCH, 'SECTION_OTHER_PEOPLE = "Facts about other people"')},
```
The pin now matches the live source exactly, and per the commit message it's now on
**one** source line rather than the prior wrapped two-string shape — the commit's own
stated reason the old literal evaded a whole-literal grep in the first place (attributed
to "this lane's D-116 finding," i.e. the reconcile report from the prior dispatch).

## Requirement 3 — exactly one definition of `_TRUST_MARKERS` and `_fact_trust_marker`

```
$ grep -n "^_TRUST_MARKERS: dict\|^def _fact_trust_marker" harness/orchestrator.py
93:_TRUST_MARKERS: dict[str, str] = {
110:def _fact_trust_marker(fact: dict) -> str:
```
**Exactly one of each.** No duplication, no later-definition-shadowing risk — the hazard
named in Cutover 5's reconcile report (Python's later-`def`-wins silently shadowing the
tested version, invisible to git) does not exist on roadmap HEAD, because roadmap's own
commit is the only orchestrator.py change here — demo-cutover-build's duplicate,
weaker copy was never merged in.

## The harness run

`--full` was **refused by its own TD-129 guard**: free memory measured at 0.64GB against
the script's 2GB floor at the moment I ran it (checked directly via `vm_stat`; the memory
in use belongs to pre-existing Chrome/Claude-desktop processes, not anything this session
started — not killed). Rather than bypass a safety guard built specifically to stop a
`--full` run from being SIGKILLed mid-flight, I ran `--layer 7` instead — the layer that
directly contains the check this change touches (`L7:CTX-STRIP`) — via the same guarded
`scripts/run_harness.sh` wrapper, independently of the other lane's own `--full` runs.

**Result: exit 0, RATCHET PASS, no failures anywhere in the run.**

Directly relevant checks:
- `CTX-STRIP  PASS` — both fault-injection twin directions: the synthetic-fourth-section
  RED case (proves the check can actually fail) and the GREEN case once
  `FACT_BEARING_SECTION_HEADERS` covers it. This is the check the header rename could most
  plausibly have broken; it's green.
- `SC1  PASS` / `SC1-E2E  PASS` — the AnswerMode-gated grounding-guard mechanism this
  whole port lives inside of, proven live end-to-end (a real turn, CONFIRMED fact →
  PLAIN_STATEMENT with no guard text appended; a parked/uncorroborated fact →
  ATTRIBUTED_HEDGE with the guard text actually present in the prompt the model received).
- `AUDIT: 8/8` — one FLAGGED item, a pre-existing, unrelated `.docx` render failure
  (`whitepaper/archive/HIP_White_Paper_Augmented.docx` — a known-corrupt file, tracked
  separately as TD-135, nothing to do with this change).
- `L7: 27/27`, `L7V2: 27/28` (1 opt-in-only skip, `CT-OUTPUT-GAP`, same as every prior run
  this session cited) — both green.
- `DISC: 1/1`, `SCHEMA: 1/1`, `VOICE: 1/1` — all green.
- Standing adversarial batteries (pytest, run before the harness proper, includes both
  `eval/test_trust_marker.py` and `eval/test_header_rename.py`): **316 passed, 8 xfailed**
  — the same xfailed count as every prior run cited across this session, no new red.
- A repeated `decrypt failed for attribute=... owner=...; skipping` line appears many
  times in the raw log — checked, this is caught-and-logged inside
  `harness/extraction_queue.py::read_user_facts`'s existing exception handling (an
  `InvalidSignature` on stale/rotated fixture keys), not a test failure — no scenario,
  check, or battery reports red anywhere near it, and it's not new to this run (the same
  shape appears throughout the log regardless of which fact is being decrypted).

hip-dev's dashboard (pid `92604`, port 7871) and Neo4j (pid `22330`, port 7689) — this
harness run touches only roadmap's own dev graph (port 7688) — confirmed unchanged before
and after; `~/hip-dev` `git status` identical (same five pre-existing untracked files).

## Status

`roadmap` HEAD is `872ad0c` — unchanged by this dispatch. Lock released. Nothing pushed.
No new commit was made; there was nothing left to commit. No acceptance row marked MET.
