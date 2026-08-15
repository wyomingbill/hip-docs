# NC 22 — EPISODE SUBSTRATE BUILD

Status: BUILT — **LANDED** on `nc-b0`
Reconciled-Against: 2026-08-15. `~/hip-nc2` @ `nc-b0` @ **`0c7b6ee`**. Board claim
`69855a9` (roadmap). Baseline for the suite delta: `41c130a`.

REQ: `docs/requirements/REQ_CONVERSATION_EPISODE__semantic-continuity-only-never-authority__v20260814_2113.md`
(NC 18 `67c0ad6`, + FM 24's parameter edits) — **the spec, filed before the build, not
amended by it.** Acceptance E1–E7; Bill's rulings Q1–Q4 (FM 24, 2026-08-14).

---

## 0. THE EXCEPTION LINE

```
NC 22 — EPISODE SUBSTRATE BUILD
COMPLETE WITH FINDINGS — 3 ITEMS FILED, NOTHING BLOCKING
```

**NEEDS BILL: nothing blocking.** One of the three is an incident in this dispatch's own conduct, not a discovery about the code — see §12b. The REQ's own discharge clause stands — *"a session
reports readiness; Bill rules MET"* — and the REQ stays **PLAN** until he does. It was not
touched by this build.

---

## 1. WHAT LANDED

**One typed owner for the SEMANTIC subset of conversation state**, `harness/conversation_episode.py`:
`ConversationEpisode`, `WorkingFrame`, `BranchInfo`, `EpisodeStore`, and the two functions
the consumers use (`prompt_context_for`, `authority_fields`).

| ruled | built |
|---|---|
| **Q1** — `IDLE_TTL = 7 min`, `ABSOLUTE_TTL = 30 min`, fixed | both constants, both clocks, **absolute wins**; `absolute_expiry` advances never |
| **Q2** — in-process for this stage | module singleton, no file, no restart survival, **no reaper thread** |
| **Q3** — `branch_info` CARRIED AND NOT INTERPRETED | typed and writable; **proven unread** (below) |
| **Q4** — deterministic notice; silent fresh episode PROHIBITED | `EPISODE_EXPIRY_NOTICE` travels on `TurnDecision.notice`; the fresh episode carries **zero** frames |

---

## 2. E1 — "NEVER AUTHORITY" IS STRUCTURAL, NOT A PROMISE

Three mechanisms, because a docstring is not a control:

1. **The field set is read from the type** — `authority_fields()` matches every field of
   every type in the module against `AUTHORITY_TOKENS`, which is held **in the module** so
   the type and its proof cannot drift apart (`STANDALONE_EXAMPLES`, same pattern).
2. **`slots=True`** — `episode.principal = "bill"` raises `AttributeError`. A NEVER clause
   that only lives in prose is one careless line from being false; this one is enforced by
   the interpreter.
3. **The inference is attempted and fails.** An episode carrying an ATTRIBUTION frame that
   says *"maya said it"* is attached to a request claiming `bill`; `resolve_member()` still
   returns `bill`. That is the exact *"the episode says maya was talking, so maya must be
   present"* inference the REQ's Audience-Epoch boundary names.

**One naming decision worth recording:** the transcript-side field is `speaker_side`, not
`role`. `role` is a PERMISSION word in this system (`get_member_by_id(...)["role"]` decides
who may enroll a member), and a field called `role` on a NEVER-AUTHORITY type invites
exactly one misreading. `AUTHORITY_TOKENS` now refuses the name outright.

---

## 3. Q3 — `branch_info` IS PROVEN UNREAD, NOT ASSERTED UNREAD

The deferral record says a typed field with no ruled meaning is how a placeholder becomes a
de-facto behaviour. So the twin does not assert that nothing reads it — it **makes reading
it fail**: `branch_info` is set to an object whose `__getattribute__` raises, and a full
`governed_decision` still decides. If any product path on that turn had touched it, the
turn would have exploded.

---

## 4. Q4 — THE PROHIBITED CASE, TWINNED AS A CASE

The ruling names the failure precisely: *a silent new episode that REINTERPRETS THE
REFERENT*. The twin reproduces it end to end:

| step | measured |
|---|---|
| turn 1 answers, and is recorded | `conversation_window() == 1` turn |
| the episode lapses (idle clock backdated) | — |
| turn 2 is **"and the other one?"** | `notice == EPISODE_EXPIRY_NOTICE` **and** `REFUSED_UNRESOLVED_REFERENCE`, reply `CLARIFICATION`, **0 model calls** |
| the fresh episode | `working_frames == []` — nothing survived to be re-bound |

**Both halves are required and neither is sufficient.** Telling the member while silently
resolving the referent against stale frames would be the same wrong answer with a courtesy
attached; refusing without telling them would leave them believing the conversation
continues.

The notice is delivered on the voice path **before** the answer *and on the refusal path*,
for the same reason.

---

## 5. THE SEAM (E6), AND CONSTRAINT 1 PROVEN IN THE RED

Episode is read and advanced in `governed_decision()` — NC 17's integration table reused,
no second mechanism — and travels as `TurnRequest.episode` / `TurnDecision.episode_id` +
`.notice`.

**Resolution sits OUTSIDE the F2 fail-closed handler, deliberately.** CONSTRAINT 1: *"a
broken or expired Episode must not break refusals."* Inside the handler, a raising episode
store would have converted a STORE-DOWN refusal into a generic ERROR — the substrate
degrading a governance answer, which is the dependency the constraint forbids. Measured
with the store patched to raise on every call:

| condition | outcome |
|---|---|
| episode store raises, household turn, fact store down | **`REFUSED_STORE_DOWN`**, `episode_id=None`, **0 model calls** |

---

## 6. THE HAZARD THIS CAPABILITY CREATED, FOUND AND CLOSED

**The live voice path writes the utterance into session memory BEFORE the kernel gate is
reached** (`voice_orch.py` S4, identity-gated, ~95 lines above the gate). With the episode
now backing session memory, that write put the current utterance into its own window — so
`_has_prior_turn(window)` was true for every identified speaker and **B1 would have stopped
firing on the exact path it exists to protect**, silently, with all 26 of its own twins
still green (they call `governed_decision` directly and never reproduce the ordering).

The rule is one line in the kernel: **a trailing frame that IS this utterance is stripped
before B1 reads the window.** Anything earlier is genuine prior state, including a real
repetition later in the conversation. Both directions are twinned — the voice path's own
write reproduced faithfully (B1 still fires), and a genuine prior turn recorded the same
way (still resolves).

---

## 7. STORE #3 ABSORBED — SESSION MEMORY'S INDEPENDENT LIFETIME ENDS

`harness/session_memory.py` is now a session-keyed VIEW over the Episode. It keeps only
what is genuinely session-scoped and is not conversation semantics: the session id and
`control_state` (RECONSIDER / FRONTIER_REQUEST — turn control, not meaning).

**The measurable consequence, which is the point:** the module used to own a transcript
list *and a 30-minute reaper*, so one conversation had two lifetimes that could disagree
about whether it was still going — NC 7 §4's no-single-owner shape in miniature. Liveness
is now decided once, at read time:

| measured | before | after |
|---|---|---|
| session idle past the idle TTL, no sweep run | transcript intact until a reaper swept | **empty transcript, `idle_seconds() == inf`** |
| threads at import | `session-reaper` daemon started | **none — retired** |
| `evict_idle(ttl_seconds=…)` | applied its own TTL | delegates to the episode store; **the argument is accepted and ignored, visibly** (NC 11's `stripped_query` precedent) |

**The privacy gate survives the absorption and is now visible in the data.** The kernel
records every answered turn for CONTINUITY with `extractable=False`; only writes through
session memory — whose callers have already passed `should_record_for_extraction` — set
`extractable=True`, and only those are returned by the read `enqueue_session_end` uses.
**A guest turn can be understood inside the conversation without ever becoming a candidate
for durable extraction.** Twinned in both directions, plus the extraction consumer itself.

---

## 8. STORE #6 RETIRED — IN THE SAME CAPABILITY, NO INTERREGNUM

`_trim_context(messages, max_turns=8)` has **no caller on the live path**. Prompt context
is `conversation_episode.prompt_context_for()`, bounded by the episode's own reach:

| measured | result |
|---|---|
| 10 turns in a live episode | **system + 10 pairs kept** — the ninth-oldest turn is still there, where the retired window had dropped it |
| the episode has ENDED | **the system prompt ALONE** |

The second row is Q4 applied to the prompt: the model must never be handed the previous
conversation on the same turn the member is told a fresh one began. The retirement is
proven by execution, not by reading the source — `_trim_context` is replaced with a landmine
and the derivation is run.

**The function is left defined and uncalled, annotated SUPERSEDED, rather than deleted** —
same reasoning as NC 11's inert parameter: a fixed-count window is a real fallback shape,
and calling it again would reinstate a second lifetime over one conversation. Visible and
inert beats quietly gone.

---

## 9. THE B1-SCOPE HANDOFF, WHICH IS A REFERENCE AND NOT A COPY

NC 17's **Q2** — *"what counts as 'missing' while there is no state owner?"* — closes by
reference. `harness/unresolved_reference.py`'s R4 note cited
`voice_orch._trim_context(max_turns=8)` as the window's owner; **that citation was about to
name a retired mechanism**, so the note now names the Episode, and the kernel is the one
place the two meet (`window=episode.conversation_window()`).

**The detector's behaviour did not change and its 26 twins are byte-green.** `WINDOW_TURNS`
keeps the value 8 and changes MEANING: it is this detector's own stated reach in its stop
reason, not a claim about how much the Episode holds — an episode's reach is a TIME bound,
and a detector reporting a time in a field called `window_turns` would be lying in a new
way. Widening what the stop reason claims is B2's call, not this handoff's.

**Proof it is the substrate B1 now reads** (measured at the seam, by spying on what the
detector actually receives):

| turn | window B1 received |
|---|---|
| after turn 1 answered | `[{"role": "user", "content": "how does photosynthesis work"}]` — identical to `episode.conversation_window()` |
| the same utterance with no episode at all | `[]` → **`REFUSED_UNRESOLVED_REFERENCE`** |

Neither REQ restates the other's clauses: B1 keeps detection and the structural stop, this
REQ keeps ownership and lifetime.

---

## 9b. NC 21's F3, LANDED WHILE THIS WAS BUILDING — WHAT IT MEANS FOR THIS RECORD

NC 21 (`04a63f8`, docs-only, same branch) measured B1 adversarially and found **F3 — THE R4
WINDOW IS INERT IN PRODUCTION**: `TurnRequest` had no `conversation_window` field, nothing
ever supplied one, so `getattr(req, "conversation_window", None)` was `None` on every
production turn and B1 saw every turn as windowless, forever. **That finding is correct, it
was reached independently, and this build is the repair of its mechanism** — the substrate
is what supplies the window, through `governed_decision`.

Three specifics, matched to F3's own three consequences:

1. **F3.1** — R4's release path was unreachable in production. It is now reached on the one
   production path, and §9's spy measures the window B1 actually receives.
2. **F3.2** — the clarification said *"I don't have the earlier part of this conversation to
   go on"* **while `_trim_context` held up to 8 turns of it**: a false statement about the
   system's own state, deterministic mid-conversation. That window is retired here and the
   claim is now true when it is made — the sentence fires only when the live Episode
   carries nothing.
3. **F3.3** — NC 20's twins passed by handing `detect()` a window themselves, *"silent on
   the seam that never delivers it."* §6 of this record is the same shape found from the
   other side: once the seam DOES deliver, the voice path's pre-gate write would have made
   every turn its own prior turn. **Both are the same lesson — a twin that supplies the
   condition it is testing says nothing about the wiring** (NC 10's rule, twice over), which
   is why the ordering twins here reproduce the voice path's own write instead of a
   hand-built window.

**F4/F5/F6/F7 are NOT touched by this dispatch** and stay filed as NC 21 left them.

---

## 10. TWIN COUNTS

**44 acceptance twins in `eval/test_nc22_episode_substrate.py`, all passing.** Every test
executes code; the model boundary is observed via `harness.model_calls`, never asserted.
The real classifier is initialised (NC 11's rule) — with an uninitialised one every
utterance reads as household-dependent, and a substrate twinned only on refusals would
prove a continuity that never happens.

| group | twins |
|---|---|
| E1 — never authority, structurally | **11** |
| E2 — no speaker authentication, both directions | **2** |
| E3 — both clocks, `advances never`, Q4's notice, **the prohibited case** | **6** |
| E4 — semantic continuity and anti-vacuity | **7** |
| E5 — B1 reads the substrate; the ordering hazard, both directions | **2** |
| E6 — the seam, attached-episode, CONSTRAINT 1 in the red, Q3 unread | **4** |
| store #3 absorbed (incl. the privacy gate and the extraction consumer) | **6** |
| store #6 retired | **3** |
| frame typing — closed kind set, frozen frames, writable `branch_info` | **3** |
| **B1's own suite, re-run on top of the substrate** | **26, green** |

**Time is injected by backdating an episode's own clocks — never by sleeping and never by
patching `time`.** An expiry twin that sleeps seven minutes is a twin nobody runs.

---

## 11. SUITE DELTA — E7, BY FAILURE SET

Baseline taken in a **detached worktree at `41c130a`**, not by stashing: a live neighbour
(NC 21) was working in `~/hip-nc2`, and a stash would have moved the tree under it. The
worktree was created and removed under the repo lock.

**The baseline is one commit behind this build's parent, and that is stated rather than
smoothed over:** NC 21 landed `04a63f8` on `nc-b0` mid-build. It is **docs-only** —
`docs/INDEX.md`, its own dispatch doc, its `LATEST_` symlink, `git show --stat` verified —
so it changes no test and no source, and `41c130a` is the correct source baseline for this
comparison.

| run | passed | failed | errors |
|---|---|---|---|
| baseline `41c130a` | 585 | 20 | 21 |
| NC 22 `0c7b6ee` | **629** | **20** | **21** |

**Failure SET identical — zero new, zero fixed.** `585 + 44 = 629`: the entire delta is
this dispatch's own twins. (`--continue-on-collection-errors` on both sides; two standing
collection errors — `tests/test_routing.py`, known-bad in CLAUDE.md, and
`scripts/test_groq_factchange.py` — abort the run without it, on both sides equally.)

---

## 12. FILED, NOT BLOCKING (2)

**(NC22-1) `TD-R-195` — `claim_lane.py` claim mode cannot take a multi-line commit
message.** The message is interpolated into `.hip-scope` as a single `# claim: <message>`
line, so every continuation line lands uncommented, is read back as a path prefix, and the
round-trip verify fails the claim closed (exit 4). The repo's own `Co-Authored-By:` trailer
makes every compliant message multi-line — **a correct commit message makes a correct claim
impossible.** Hit live at this dispatch's first claim attempt. The fail-closed behaviour is
RIGHT; the gap is that the message is inside the verified region at all. Sibling of
TD-R-194(a)/(b); filed separately so HA-94's row is not rewritten. **Filing pre-authorized
(tool infrastructure); fixing needs a REQ.**

**(NC22-2) This board row is UNEDITABLE BY THE TOOL and was claimed and closed by hand.**
The Natural-conversation row carries **7 bare pipes against a 6-pipe header**, so
`claim_lane.py`'s column guard refuses every edit to it — TD-R-194(b)'s shape, a row the
tool did not break, on a different row from HA-94's. Claimed by hand under the repo lock
(HA-94's precedent), with the anchor asserted unique in the file and the pipe count
asserted unchanged. **The row's break was not repaired here:** merging two cells of another
lane's record is a change to their record, not to this capability's scope.

---

## 12b. I PUBLISHED ANOTHER LANE'S ROW — REPORTED, NOT SMOOTHED OVER

**`c034229` (this dispatch's roadmap commit) contains `TD-R-196`, which is NC 24's filing,
not mine.** NC 24 wrote its row into `docs/techdebt/DEBT_REGISTER__v20260807_1057.md`
between my read of the working-tree diff and my `git add` of that file. I checked the diff
BEFORE staging — it showed one insertion, mine — and then staged the whole file, so the row
that arrived in between rode along.

**Nothing was lost or altered; the row is byte-identical to what NC 24 wrote.** That is not
the test. Preamble item 8 says it in its own words — *"'No harm done' is not the test; 'who
decided' is"* — and no lane decided to publish TD-R-196. It is now on `origin/roadmap`
under a commit whose message does not mention it.

**Not repaired by rewriting history**: the commit is pushed, and history-rewriting is a
destructive class that is explicitly not pre-authorized. NC 24's row stands where it is.

**The lesson is specific and is the one worth carrying:** *surgical staging must verify the
STAGED diff, not the working-tree diff.* A working-tree check is a check of the past — on a
shared file with live neighbours the two are separated by a race window, and every
protection in preamble item 2 (save the union, reset to HEAD, re-apply only your rows) lives
on the other side of `git add`. `staging_guard.sh` did not catch it either: the paths were
all mine by declaration, and the file was legitimately in my scope.

---

## 13. WHAT THIS DISPATCH DID NOT DO

- **Did not touch the five OUT-OF-SCOPE stores or the split's telemetry half.** Disclosure
  pendings, principal/member session, transcript log, operator session, per-session trace,
  `GET /api/last_speaker` — all unchanged. The split's SEMANTIC half is present as the
  `ATTRIBUTION` frame kind and is **never** consulted for authentication.
- **Did not act on `branch_info`.** Q3 stays B2's.
- **Did not build the Audience Epoch**, and added no field that could imply presence.
- **Did not amend either REQ.** B1's scope NOTE was updated to reference the Episode, which
  is what the dispatch ordered; NC 17's REQ text was not edited from here.
- **Did not displace NC 21**, live read-only in the same worktree: its `docs/` scope line
  was kept and this dispatch's prefixes appended beneath it.
- **Did not persist an episode anywhere.** In-process, per Q2.

---

## 14. CLAIM IMPACT

```
CLAIM IMPACT: none
```

Substrate work behind the governed seam; no ledger claim's evidence changes here.

---

## 15. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `~/hip-nc2` @ `nc-b0`.
- `lane_preflight.py --tree ~/hip-nc2` → **OK**, `bolt://localhost:7693`, exit 0; `--busy`
  → **NOT BUSY** before the build.
- Board claimed in the FIRST commit (`69855a9`, roadmap) before any code landed.
- Every twin run unchained; failure sets compared as SETS, not counts.
- The commit contains exactly the seven declared files — staged set verified before the
  commit existed, and the scope declaration widened **deliberately** (with the reason
  written into `.hip-scope`) for `harness/turn_request.py`, which E6 names as part of the
  seam.
- Push refused once by the kernel lock (exit 75) while another lane held it; deferred,
  re-asked `hip_lock.py who repo`, and retried. **Not bypassed.**
