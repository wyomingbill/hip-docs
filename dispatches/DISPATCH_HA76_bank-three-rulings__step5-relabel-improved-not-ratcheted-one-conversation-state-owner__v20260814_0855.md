# DISPATCH_HA76 — bank the three rulings
Status: BUILT
Reconciled-Against: `roadmap` @ this dispatch's commit

**TYPE:** BUILD (docs + test-config only — **no product code, graph untouched**)

**REQ:** `docs/requirements/LATEST_REQ_TRANSCRIPT_STORAGE.md` — the rulings are
banked into it as **§9.1–§9.4**.

---

## PART A — NUMBERING: HA-75's work IS STEP 5

**Bill's ruling: the contract is the authority.** HA-75 built the read path and
called it *step 3*. The work was right; the label was not. **§6A row 5 is the
read path**; **§6A row 3 is `query_hash` → keyed commitment**, which HA-75 never
touched.

**Three annotations, none a rewrite** — the original wording stays visible with
what changed it, per the pre-authorized correction class:

| where | annotation |
|---|---|
| HA-75 dispatch doc | title struck through to **STEP 5**; a ruling block at the head of §0; §0's "flagged for Bill" close marked **RESOLVED**; HA-75's own contemporaneous analysis left **unaltered** under its own subheading |
| `docs/INDEX.md` | both rows — the DISPATCH LEDGER row and the `dispatches/` row — carry the relabel inline |
| `docs/LANES.md` | HA-75's landed row carries it |

**Root cause, recorded in every annotation:** the sequence existed in **two
places** — the contract's table and a chat-side paraphrase — **and the paraphrase
drifted.** Nothing reconciled them because nothing was responsible for doing so.

**Standing rule, banked into the REQ (§9.1):** *dispatches cite the contract's own
table, never a paraphrase of it.* Same class as the duplicated phase map and the
duplicated checkout guard: **a second copy of an ordering is a second authority,
and the copy is the one that drifts.**

## PART B — BASELINE: IMPROVED EVIDENCE, NOT A RATCHET

**Bill's ruling: no auto-ratchet. "Passing better once is not enough."**

`L1:P2` is recorded in **§9.2** as IMPROVED EVIDENCE with the **baseline
UNCHANGED**. The harness printed `IMPROVED vs baseline: ['L1:P2'] — update to lock
in`; that is a suggestion from a tool, not a ruling, and changing a baseline is
not a pre-authorized class even for an improvement.

Captured alongside it, so a future ratchet ruling has something to cite: the run
(`--full`, 2026-08-14, roadmap `12c1adc`, services up), the layer result
(`L1: 15/15`), the binding-gate context, and the **suspected cause marked as
suspicion** — nothing in HA-75 touches retrieval, and this lane already records
(HA-19) that three `--full` runs, the last two byte-identical, disagreed on
L1/L3/L4/L6 and on the regression list itself. §9.2 also names what a future
ratchet ruling would need: repeated runs from
`logs/harness/live_layer_results.csv`, a rule set **from that data**, no
best-of-N, no invented threshold.

**`L2:routing_showcase.T04` left alone** — reported non-gating, unrelated, not
chased.

## PART C — ONE AUTHORITATIVE CONVERSATION-STATE OWNER

Banked **verbatim** as §9.3:

> **"One conversation has one authoritative ephemeral conversation-state owner,
> independent of ingress modality or worker process."**

All four recorded for HA-75 specifically: the in-process buffer is **ACCEPTED**
for this step; the multi-process limitation is **recorded explicitly**; **file
merging is NEVER the solution** (it would undo Q4 and reintroduce the plaintext
read the row exists to remove); and shared, process-independent conversation
state is a **PREREQUISITE** before voice and text may participate in the same
Conversation Episode.

**Both sharpeners banked as PROPOSED (§9.4), not in force, for Bill to confirm or
strike:** (i) the authoritative owner is the **governed-turn kernel's** process
boundary, adapters are clients — a standalone state service is not the default
answer, because two governance-embedding processes plus a third state service is
**three brains, the disease one layer down**; (ii) wherever it lives it
**inherits Q1–Q3's properties** — memory-only, keyed recoverability, dies with the
session, never persisted/swapped/exported — **so conversation state can never
become erasure surface #22**.

### One correction to the ask

The dispatch said to cross-reference *"the NC REQs"*. **There are no NC REQs.**
The natural-conversation work is a design doc —
`docs/design/HIP_DESIGN__dual-model-natural-conversation-v2__v20260813_1500.md`,
status **"ADOPTED DIRECTION (research lane; no requirement filed)"** (HA-66,
`4a7b82f`). §9.3 cross-references what actually exists — that design's §2 "Three
components" (the **HIP Kernel**, *"unchanged from the governed text path"*, which
is the document sharpener (i) argues from) and its §5 M3 milestone (*"first
intersection with the conversation-memory track"*) — plus `REQ_ERASURE_SURFACES`
Q3-C and this contract's Q1–Q3. Recorded rather than papered over: a rule
cross-referenced to a document that does not exist is unenforceable. **When an NC
REQ is filed, this rule belongs in it.**

## PART D — PYTEST IMPORT-MODE PORT

Config only, already proven on `hip-vo@main` (TD-V-019). `pytest.ini` pins
`--import-mode=importlib`; a root `conftest.py` keeps the repo importable however
pytest was invoked. `testpaths` deliberately unset — a bare `pytest` must not
imply running every `eval/` script.

**The broken shape, reproduced on this lane before the port:**

```
ERROR eval/test_session_content_key.py
ERROR eval/test_transcript_band_off_files.py
!!!! Interrupted: 2 errors during collection !!!!
29 tests collected, 2 errors
```

**After:** `72 tests collected`, zero errors; and a bare `pytest` (no `-m`, no
flags) now runs the session-key battery 30/30.

**Twin — `eval/test_import_mode_shadowing.py`, 6 tests.** It does not assert on
remembered history: it **reproduces the failure on demand** by forcing
`--import-mode=prepend` and requiring collection to break, and it measures the
fixed state by running collection in a subprocess rather than by reading config
text. It also asserts the shadow still exists (`eval/harness.py`), so if that file
ever goes away the guard is retired rather than kept as cargo.

## VERIFIED

**Watched run:** the broken shape before the port and the recovered shape after;
bare `pytest` 30/30; the twin 6/6; the battery manifest 14/14 after registering
the new file; and the whole suite.

**Whole-suite differential, same command, same service state:**

```
HA-75 (its own landing run):  31 failed, 1300 passed, 10 skipped, 9 xfailed, 2 errors
HA-76 (this dispatch):        31 failed, 1306 passed, 10 skipped, 9 xfailed, 2 errors
```

**+6 = exactly this dispatch's twin. Zero new failures** (set difference of FAILED
lines is empty). The `--import-mode` flag was **not** passed on the command line —
it came from `pytest.ini`, which is the port working.

The two standing collection errors are unchanged and neither is mine:
`tests/test_routing.py` (CLAUDE.md's documented known-bad) and
`scripts/test_groq_factchange.py` (a script making a live Groq call at import).

**Reasoned about:** that the import-mode pin is safe for the whole repository —
argued from the differential above and from CLAUDE.md already REQUIRING the same
flag in this lane's canonical invocation, not from an audit of every suite's
import style.

**Not run:** `--full` and the memory harness. This dispatch changes no product
code and no graph; the whole-suite differential is the relevant evidence, and
HA-75's binding-gate results stand.

## CLAIM IMPACT

**CLAIM IMPACT: none** — docs and test-config only; C-09's timeline moves only at
step 9.

## OPEN — NEEDS BILL

- **§9.4's two PROPOSED sharpeners: confirm or strike.** Neither is in force. A
  later document citing 9.4 must check which way it went.
- **No NC REQ exists** for the conversation-state rule to live in permanently
  (see Part C's correction). Filing one is not this dispatch's scope.
