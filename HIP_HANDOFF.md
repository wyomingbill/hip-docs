# HIP HANDOFF — roadmap lane state
Status: LIVE (exempt from the Naming Law's never-overwrite rule **by Bill's ruling,
2026-08-03, D-141** — one of the four exempt documents, alongside INDEX.md, BACKLOG.md and
LATEST_DEBT.md; the closed list and its reason live under CLAUDE.md's Naming Law)
Reconciled-Against: roadmap `c5c9202` (D-137); created D-137, last updated D-141, 2026-08-03

**This is a STATE document, not a dispatch log.** It says where the roadmap lane IS, what is
true about it, and what would break. Dispatch history lives in `docs/dispatches/` and
`docs/INDEX.md`; do not re-narrate it here.

**Maintenance rule (CLAUDE.md, "The live handoff document"):** the lane that LANDS a
dispatch updates CURRENT STATE **in the same commit**. Never rewritten wholesale. Never
allowed to describe a past state. A lane that cannot honestly update it STOPS.

---

## CURRENT STATE

### ⛔ HEL 1.0 ISOLATION GATE — Bill's ruling, 2026-08-10. Read before any real-household deployment.

**HEL 1.0 is an immutable legacy DEV artifact. Before any real household data enters the system,
start a clean HEL 2.0 chain.** The HEL 1.0 chain is **never appended to, never joined with, and
never made available to the real-household environment. No migration carries HEL 1.0 events
forward.**

**THE JUSTIFICATION, RE-GROUNDED (Bill, 2026-08-10 — read this, the earlier framing was wrong).**
The reason for isolation is **NOT** plaintext-utterance retention. HA-31 continuation 5 read all
108 HEL 1.0 `identity.rejected` payloads (span 2026-07-20 → 2026-08-03) and found **no rejected
utterances and no real household data**: every payload carries exactly `detail`, `member`,
`reason`, `source` — structured decision metadata, fixture identities only, zero address,
medical, phone, email or SSN signals.

**The actual reason is format deficiency:**

1. **HEL 1.0 lacks the keyed commitment.** `keyed_commitment`
   (`harness.ledger_commitment.compute_keyed_commitment`) exists only on HEL 2.0.
2. **HEL 1.0 retains a RAW, dictionary-testable hash.** `payload_sha256` is a bare
   `_sha256` (`harness/epistemic_ledger.py:474`, `:479`); HEL 2.0 removed it, along with
   `payload`, `payload_enc` and `payload_kid` (`:88-91`, D-R-163/Segment 4).

**Do not describe this gate as plaintext-utterance retention.** The two formats partition
perfectly on the `hel` field — 325 events at 2.0 (commitment-only), 108 at 1.0 — and the write
path already emits only HEL 2.0, so this gate governs HISTORY, not future writes.

### ⛔ ERASURE-ENABLEMENT GATE — Bill's ruling, 2026-08-06. Read before touching erasure.

**NO REAL-DATA ERASURE UNTIL *BOTH* OF THESE HAVE LANDED:**

1. **key-custody consolidation** — production keys in one managed location, tests
   structurally unable to write there, legacy copies removed only by a separately
   evidenced migration; and
2. **the semantic-metadata cascade** — the beside-seal graph metadata scrubbed, not just
   the sealed value.

**Authority:** `docs/reviews/RULING_KeyLifecycle__three-rulings__v20260806_2000.md`
(banked HA-13, `a6a1e05`). Bill's own closing sentence:

> "And I would not enable real-data erasure until **both the key-custody cleanup and the
> semantic-metadata cascade have landed**. Otherwise the UI is offering an erasure action
> stronger than the system can presently deliver."

**WHY THE GATE IS TWO CONDITIONS AND NOT ONE.** Either alone leaves the erasure claim
false in a different direction:

- **Custody without the cascade:** the key is gone and the value with it, but HA-10
  measured what stays readable beside the seal on subject `dad` — `subject`, `attribute`,
  **`representation_class=HEALTH_CLAIM`**, `sensitivity=high`, `owner=sam`, timestamps and
  the confidence history. Bill's Ruling 3: *"Dad + `health_condition` + HIGH + authored by
  Sam + date is still meaningful personal information."* That is **primary-record VALUE
  erasure**, not subject erasure.
- **Cascade without custody:** the metadata is scrubbed but the target key may have
  recoverable copies, so "we destroyed the key" is unprovable. HA-08 found the key
  population growing on every harness run (TD-R-172); HA-11 found 16 key-bearing
  directories, not one.

**What has landed toward the gate:** Ruling 2's backup exclusions only — all 16
key-bearing directories are `[Excluded]` from Time Machine as of HA-13, before any backup
destination exists. **That is a precondition, not either gate condition.** Neither
consolidation nor the cascade is started.

**Not to be confused with this gate:** **TD-R-173** (raw query text in
`recall_audit.jsonl`) is by the same ruling a **separate defect, fixed regardless of the
cascade and explicitly not buried under erasure work.** It does not gate erasure and
erasure does not gate it.

- **HEAD:** see `git log -1` — this block is updated at HA-08's own commit. Origin
  `roadmap` is the only live branch; every lane pushes to it. **Dispatch numbering note:
  HA-07 was spent on the standing-rules check (`dded3ae`); the step-5 build is HA-08.**
- **Roadmap lane — LAST LANDED: FM 29** (**TOOLING — no product code**) —
  **`--emit-detect-pattern` FAILS CLOSED (Bill's ruling, narrow scope, 2026-08-15).**
  Absent/empty local policy → exit 8, paths named, stdout empty; valid-policy output
  BYTE-IDENTICAL (pre/post captures, `cmp` clean both scopes); consumer proven both
  directions on `push_docs.sh` without publishing. **TD-R-197 FILED (SEC, needs-Bill):
  the consumer test found push_docs.sh's own exclusion grep dies on its multi-line
  pattern and `|| true` renders "Secret scan: clean." falsely — treat mirror pushes as
  unscanned past stage 1 until repaired.** REQ: Amendment 3 `1d13201` before code
  `645f544`. FM 28 not reopened; city/zoning policy untouched.
- **Roadmap lane — PREVIOUSLY LANDED: FM 28** (**TOOLING + HOME FILE — no product code**) —
  **THE SCRUBBER FAILS CLOSED (Bill's ruling, 2026-08-15).** `~/.hip-scrub-local` created
  (0600, machine-local PII class; every value enumerated from the two shipped packages'
  redaction records — FM 5's three zips and NC 27's round-3 zip — never invented; values
  live ONLY in that untracked home file). `scrub.py`'s certifying modes (`--check`,
  `--scrub`) now REFUSE with exit 8 when the local policy is missing or empty — "clean"
  against no policy is an error, not a pass (NC 27 §4.2 was the shipped near-miss).
  Twins both directions green; all five lane-tool twins green; the real policy catches
  all six NC 27 address variants live (6/6, zero residual). Bill's redaction policy is
  verbatim in `scripts/scrub_patterns.py`: city-only and zoning-district references
  STAY; private-network identifiers, hostnames, credentials, precise private addresses,
  machine/user-specific material are scrubbed. REQ: `REQ_PROCESS_HARDENING_TOOLS`
  Amendment 2 (`c1ed599`, before code). **GAP, named not back-filled:** entries between
  HA-78 and this one (through HA-96, NC 27, FM 27 among others) were not recorded here
  by their lanes; their record is `docs/LANES.md` and the dispatch ledger — this entry
  resumes the discipline without inventing history it did not witness.
- **Roadmap lane — PREVIOUSLY LANDED: HA-78** (**CODE, THREE TREES OUTSIDE THIS LANE'S PAIR**)
  — completed the Groq decommission across the estate ahead of **2026-08-16**. Swept
  `~/hip-dev` (8 files — **the FROZEN DEMO, touched only under Bill's explicit dispatch**,
  otherwise a NOT-pre-authorized class), `~/hip-cutover-demo` (7) and `~/hip-harness` (2).
  **All five trees now resolve CORE from config as `openai/gpt-oss-120b`.**
  **Mirrored, not shared:** the demo trees are worktrees on DIFFERENT BRANCHES and
  hip-harness is a separate repo (TD-132), so none could read HA-77's module — the
  duplication is what TD-132 records. Zero residual executable literals, AST-verified.
  **Proven:** live smoke CORE+MID green on all three; twin 15/15/15 and 9+6-skip on
  hip-harness (absent surfaces); cutover `eval/` **7 failed/371 → 7 failed/386** (+15 = the
  twin, zero new failures or errors); hip-dev 0→15 passing with its 19 pre-existing oracle
  errors unchanged; wiring checked by compile, import and an AST scan for the HA-65
  function-level-import class.
  **DEMO IMPACT NONE, structurally:** the OFFERED 16-turn deck is edge 14 / mid 1 /
  frontier 1 / **CORE 0**, unchanged from VD-57, so a CORE swap cannot move it. Verified by
  census — **`demo_integrity_battery.py` was NOT run**, because its own docstring says it
  fires turns with a reset+seed and would reset the demo graph.
  **FOUND BEYOND THE DECOMMISSION:** hip-harness's fact-change detector was pinned to
  `meta-llama/llama-4-scout-17b-16e-instruct`, which Groq **does not serve today** (live
  `model_not_found`) — dead independently of 08-16, corrected to `openai/gpt-oss-20b`.
  **NOT done:** the CORE token rate is still the old model's in all five trees — repricing
  is a measurement and Bill's to rule on.

- **Roadmap lane — PREVIOUSLY LANDED: HA-77** (**CODE, TWO TREES — `~/hip-roadmap` AND `~/hip-vo`**)
  — **Groq decommissions `llama-3.3-70b-versatile` on 2026-08-16.** Swapped CORE to
  **`openai/gpt-oss-120b`**, verified against Groq's LIVE model list first. Only CORE was
  affected; MID (`llama-3.1-8b-instant`) and the fact-change detector
  (`openai/gpt-oss-20b`) are unaffected.
  **Centralized:** every Groq id now resolves from `config.yaml`'s new `models.groq` block
  via `harness/groq_models.py`, which REFUSES rather than defaulting. No Groq literal
  remains in scanned code (AST twin, 15/tree). **`epistemic_record._compute_net` uses the
  Groq roster to decide OFF-NET vs ON-NET, so a missed swap would have recorded a real
  network crossing as a local turn** — that roster is now DERIVED, not hand-kept.
  **Proven:** live smoke both trees (hip-vo through the egress gateway → `GROQ_OFFNET`;
  roadmap direct, no gateway module there). Binding green — hip-vo governance
  **250/0/0/0**; roadmap batteries **31/1321** vs HA-76's 31/1306 (+15 = the new suite,
  zero new failures); `--layer 7` **RATCHET PASS**.
  **New-model baseline recorded, NO ratchet:** L1 15/15, L2 24/35, L3 3/3, L4 30/34, L7
  27/27 — all identical to the old model. **L6 newly red**, traced NOT to this swap but to
  a **TD-125 detector false negative cascading into a HARD ZERO G1 violation** on the
  UNCHANGED detector model (9 `zero changes` events that run).
  **NOT done:** the CORE token rate is still the old model's — repricing is a measurement
  and Bill's to rule on; marked `RATE STALE` in source.
  **HANDOFF — these break on 2026-08-16 unless their own lanes swap them:** `~/hip-dev` (8
  files, incl. the live `GROQ_MODEL_CORE`), `~/hip-cutover-demo` (7), `~/hip-harness` (2).
  **Coordination finding:** the first `--full` was OOM-killed because Voice 41 was running
  its own concurrently; the lock is keyed per resource and **nothing arbitrates machine
  memory**. Waited rather than killed theirs.

- **Roadmap lane — PREVIOUSLY LANDED: HA-76** (**DOCS + TEST-CONFIG ONLY — no product code,
  graph untouched**) — banked three of Bill's rulings into `REQ_TRANSCRIPT_STORAGE`
  **§9.1–§9.4**:
  **(A) HA-75's work IS STEP 5**, not step 3 — relabeled **by annotation** in the dispatch
  doc, both `docs/INDEX.md` rows and the `docs/LANES.md` row; nothing rewritten, HA-75's own
  contemporaneous analysis left unaltered. Root cause recorded: the sequence lived in the
  contract's table AND a chat-side paraphrase, and **the paraphrase drifted**. Standing rule
  banked — **dispatches cite the contract's own table, never a paraphrase.**
  **(B) `L1:P2` is IMPROVED EVIDENCE and the baseline is UNCHANGED** — *"passing better once
  is not enough"*; a ratchet happens only under its own explicit ruling. Run ids, layer
  result and a suspected cause (live-model variance, marked as suspicion) captured so a
  future ratchet ruling has something to cite. `L2:routing_showcase.T04` left alone.
  **(C) Bill's conversation-state rule banked VERBATIM** — *"One conversation has one
  authoritative ephemeral conversation-state owner, independent of ingress modality or
  worker process."* All four HA-75 points recorded: the in-process buffer is ACCEPTED for
  that step, the multi-process limitation is RECORDED, **file merging is NEVER the
  solution**, and shared process-independent state is a **PREREQUISITE** before voice and
  text share a Conversation Episode. Two sharpeners banked **PROPOSED, not in force**
  (kernel process boundary as the owner; the owner inherits Q1–Q3 so state never becomes
  erasure surface #22) — **BILL TO CONFIRM OR STRIKE.**
  **CORRECTION recorded:** the dispatch asked to cross-reference *"the NC REQs"* — **there
  are none.** The NC work is `docs/design/HIP_DESIGN__dual-model-natural-conversation-v2`,
  status *"ADOPTED DIRECTION (research lane; no requirement filed)"*. §9.3 references what
  exists; when an NC REQ is filed, the rule belongs in it.
  **(D)** Ported `hip-vo@main`'s pytest importlib fix (`pytest.ini` + root `conftest.py`,
  config only): collection on this lane went from **29 collected / 2 errors, interrupted**
  to **72 collected, 0 errors**, and a bare `pytest` now works. Twin
  (`eval/test_import_mode_shadowing.py`, 6) reproduces the break on demand under forced
  prepend mode rather than asserting on remembered history.
  Suite: **31 failed / 1306 passed** vs HA-75's **31 / 1300** — **+6 = exactly the twin,
  zero new failures.** `--full` and the memory harness not re-run: no product code or graph
  changed, and HA-75's binding-gate results stand.

- **Roadmap lane — PREVIOUSLY LANDED: HA-75** (**CODE**) — `REQ_TRANSCRIPT_STORAGE` row-19
  **read path, Q4**: `/api/transcript` no longer reads transcript FILES. The live band is
  fed from `harness/session_transcript_buffer.py`, an in-memory session-scoped buffer
  populated by a tap on the SAME record `write_transcript_turn` writes, and discarded when
  `SessionKeyRegistry.end()` ends the session. **"Never decrypts" is now structural** —
  nothing to decrypt, no file opened — proved by AST over the endpoint's call graph, not by
  a source regex.
  **WRITERS ARE UNTOUCHED and durable transcript surfaces are still written byte-identically**
  (C4), because Bill's sequencing is that the band be proven working BEFORE any durable
  plaintext is removed. Removing those surfaces is a later step and is NOT done here.
  **The buffer holds PLAINTEXT in process memory and that is the ruled answer, not a gap**
  (Q4: "there is nothing to decrypt"); the session content key is NOT used to seal it.
  **Per-process scope is a NEW cost not in Q4's own table:** a separate voice-service process
  would populate its own buffer, not the dashboard's, where the file reader used to merge
  both. Recorded for the later read-path steps.
  Binding gate: batteries **31 failed / 1300 passed** services-up (BEFORE, changes stashed:
  31 / 1287 — **+13, exactly this dispatch's suite, zero new failures**); `--layer 7`
  **RATCHET PASS**; `--full` **BINDING TESTS PASS** with one live-layer regression
  (`L2:routing_showcase.T04`, reported not gated per item 12 as amended — the model answered
  a time query when asked about cable consolidation); memory harness **13/17, inside the
  13–15 pin**. Two pre-existing collection errors (`tests/test_routing.py` known-bad,
  `scripts/test_groq_factchange.py` live-Groq-at-import), neither mine.
  **NOT done, flagged for Bill:** `IMPROVED vs baseline: ['L1:P2'] — update to lock in` was
  left alone, because changing a baseline is not a pre-authorized class.
  **Numbering discrepancy recorded:** the dispatch calls this step 3; the contract's own
  nine-step table numbers this row **step 5** (its step 3 is `query_hash` → keyed
  commitment). Its precondition — step 2, the session content key — IS satisfied (30/30).

- **Roadmap lane — PREVIOUSLY LANDED: HA-51** (**TWO CHECKOUTS — REQ filed, master-key guard landed on
  hip-vo, HA-50's gap and missing ledger row recorded**) —
  **⚠ THIS DISPATCH AND HA-50 TOUCHED `~/hip-vo` (branch `main`), NOT ONLY THIS LANE.** hip-vo is
  a worktree of `~/hip-dev/.git`. Commits: **roadmap `6884aca`** (HA-50 Part A, the Trust
  Boundary Roadmap); **hip-vo `c05b273`** (HA-50 Part B, endpoint auth + guest fallback),
  **`a362d5b`** (HA-51 Part A, the REQ), **`8fd0b52`** (HA-51 Part B, the guard).
  **`REQ_MASTER_KEY_FAIL_CLOSED` IS FILED ON hip-vo AND THE GUARD IS LANDED UNDER IT.**
  `_load_or_create_master_key` now refuses to mint a replacement when sealed data exists —
  **checked before `os.urandom(32)` is ever called**, on the key-absent branch only, so the
  normal path gains no database round-trip. **Status NOT MET; ruling it is Bill's.**
  **THE C4 SIGNAL IS BOTH A SENTINEL AND A GRAPH QUERY, because either alone has a hole** — the
  sentinel answers with no database, the graph query catches a lost sentinel. **`None` means
  "could not ask" and is NEVER read as "no ciphertext"**: an unreachable database is not
  evidence of an empty graph, and a check that answered "no" when it merely failed to ask would
  reintroduce the defect behind something that looks like it passed. **Do not "simplify" that
  to a single signal or collapse None to False.**
  **⛔ BILL-7 — hip-vo HAS NO SANCTIONED GRAPH TARGET, and this has now cost two dispatches.**
  No repo `.env.dev`; `~/.env.dev` is forbidden (pins **7689, the frozen demo**);
  `.env.dev.example` says **7688**, the roadmap lane's graph; `voice_https_orch` defaults to
  **7687**. **All four bolt ports are listening**, so a wrong guess writes into another lane's
  graph instead of failing. **A session must not resolve this by picking one.**
  **RECORDED VERBATIM so nothing downstream reads HA-50 as full system verification:**
  *"Graph/memory integration verification: NOT TESTED (hip-vo has no sanctioned graph
  configuration; endpoint + source twins only)."* **Memory harness: NOT RUN — NO SANCTIONED
  GRAPH, for both HA-50 and HA-51.** Carried in `docs/BACKLOG.md` and both ledger rows. **The
  claims ledger was deliberately not used** — its statuses are computed by the generator and
  never hand-edited, and a coverage gap is not a claim.
  **HA-50 NEVER REGISTERED ITSELF.** It landed two commits and added no ledger row and no
  handoff entry; **HA-51 added its row retroactively.** Same completion-step failure the HA-41
  close-out cleaned up — worth watching for on two-checkout dispatches, where the code lands in
  one repo and the record belongs in the other.
  **THE 7860 SERVER STILL RUNS PRE-FIX CODE** — the auth guards do not take effect until it is
  restarted, and that restart waits on BILL-7.
  **CLAIM IMPACT: none.** **Nothing ruled MET.**

- **Roadmap lane — LANDED EARLIER: HA-49A** (**CODE — step 2 hardened on external review; STILL
  NOTHING WIRED**) —
  **`harness/session_content_key.py` EXISTS AND NOTHING CALLS IT.** Transcripts still write
  verbatim words; **row 19 is exactly as open as before.** Zero production callers, verified by
  grep.
  **THE ENVELOPE IS BOUND. Fernet is GONE from this path — do not put it back.** It authenticates
  its ciphertext but **carries no context**, so an encrypted utterance could be moved between
  sessions, turns or members and still verify. The cipher is **AES-256-GCM with AAD** over
  `{v, session_id, turn_id, member_id, content_type, epoch}`, re-derived on decrypt plus an
  explicit session check.
  **THE CONTENT KEY IS SPLIT, AND THE SPLIT IS THE WHOLE POINT — do not "simplify" it by wrapping
  the key directly.** A wrap is sealed to a member's **long-lived** X25519 key, so a wrapped
  content key would stay recoverable forever. Instead
  `content_key = HKDF(share, salt=session_salt, info=…)`: the **share** is wrapped, the **salt is
  never wrapped, never written, and dies at `end()`.**
  **THE OPERATOR ANSWER, both halves: a persisted wrap STILL UNWRAPS — and the read STILL FAILS.**
  `open_persisted_wrap()` exists to demonstrate the honest half. The share alone cannot
  reconstruct the key.
  **A MEMBER WHO JOINS MID-SESSION CANNOT READ EARLIER TURNS.** Authorization **epochs**: joining
  opens a new one, and no wrap exists for earlier epochs. **Revocation is forward-only** — they
  already saw those turns. An operator change is a revoke plus an authorise. **A reconnecting
  member is not re-authorised**, and a test asserts the epoch does not advance.
  **DO NOT STRENGTHEN THE MEMORY CLAIM.** The guaranteed property is **"the key never reached
  disk"** — not memory erasure; Python cannot guarantee that and the module says so. **A standing
  test fails if the module ever acquires a stronger phrasing**, and the REQ's Q3 carries the
  boundary explicitly. An audit at HA-49A found no existing overclaim anywhere.
  RUNS: binding **1209 passed / 0 failed / 9 xfailed** (58 files; this battery 18 → 30),
  `--layer 7` **EXIT 0** (L7 27/27, L7V2 27/28, AUDIT 9/9), **RATCHET PASS**, memory **13/17
  inside the pin**. Five defect classes proven red then restored.
  **⏳ The commitment window is still open and STILL UNSPENT: 100% of the 27,732 turns are
  committable, nothing has been committed.** Step 4 spends it; step 8 closes it. **Critical order
  unchanged: source fix → commitments → historical erasure → key destruction.**
  **CLAIM IMPACT: none.** **Nothing ruled MET.**
  See `docs/dispatches/DISPATCH_HA49A_ENVELOPE_BOUND__aad-split-key-epochs-and-the-operator-answer__v20260812_1259.md`.

- **Roadmap lane — LANDED EARLIER: HA-49** (**CODE — step 2 of nine built; NOTHING WIRED**) —
  **`harness/session_content_key.py` EXISTS AND NOTHING CALLS IT.** Read that sentence before
  citing this dispatch: **transcripts still write verbatim words, no corpus is committed,
  `/api/transcript` is unchanged, and ROW 19 IS EXACTLY AS OPEN AS BEFORE.** Zero production
  callers, verified by grep rather than asserted. Step 5 is what wires it.
  **WHAT IS BUILT:** the **per-session content key** — a Fernet key wrapped via X25519 to
  **exactly Q2's authorized set** (speaking members + live operator), in memory only, zeroed at
  `end()`, registry with **no persistence layer deliberately** — and the **durable member-keyed
  commitment** (`commit_turn` / `verify_turn_commitment`, HMAC under the member's ledger key).
  **NO NEW CRYPTOGRAPHY: every primitive reused** (`dyad_crypto.seal_to_pubkey`,
  `member_seal_keys`, Fernet, `ledger_commitment.compute_keyed_commitment`).
  **TWO KEY STORES ARE IN PLAY AND BOTH ARE CORRECT** — the wrap uses the X25519 **seal** keypair
  in `~/hip-keys/`, the commitment the 32-byte **ledger** key in `ledger/keys/`. Do not
  "unify" them; they do different jobs with different lifetimes.
  **IF YOU EXTEND THIS, FOUR THINGS ARE LOAD-BEARING:** (1) **the authorization set IS the wrap
  set** — there is no permission list beside it that could drift, and an unauthorized member is
  refused because no ciphertext is addressed to them; (2) **the commitment is member-keyed and
  the content key is session-scoped** *because their lifetimes differ* — the commitment outlives
  the session, the words must not; (3) **`verify_turn_commitment` reads the key without creating
  it**, so a post-erasure state is observed rather than repaired; (4) **`end()` does NOT
  guarantee memory erasure** — Python cannot, Fernet holds immutable `bytes`, and the module
  says so. **The guaranteed property is that the key never reached DISK**, and the twin
  *searches* the filesystem to prove it rather than asserting it.
  **⏳ THE COMMITMENT WINDOW IS STILL OPEN AND STILL UNSPENT.** bill/maya/sam all hold keys, so
  100% of the 27,732 turns remain committable — **but nothing has been committed yet.** Step 4
  spends the window; step 8's key destruction closes it. **Critical order unchanged: source fix
  → commitments → historical erasure → key destruction.**
  RUNS: binding **1197 passed / 0 failed / 9 xfailed** (58 files), `--layer 7` **EXIT 0**
  (L7 27/27, L7V2 27/28, AUDIT 9/9), **RATCHET PASS**, memory **13/17 inside the pin**. Three
  twins proven red by injected defects then restored. **CLAIM IMPACT: none** — a mechanism with
  no caller changes no observable behaviour. **Nothing ruled MET.**
  See `docs/dispatches/DISPATCH_HA49_SESSION_KEY_AND_COMMITMENT__step2-built-nothing-wired__v20260812_1221.md`.

- **Roadmap lane — LANDED EARLIER: HA-48** (**DOCS ONLY — the transcript storage contract
  RATIFIED; NO CODE CHANGED**) —
  **BILL RATIFIED Q1–Q6 AS PROPOSED ON 2026-08-12, WITH FOUR ADDITIONS.**
  `docs/requirements/LATEST_REQ_TRANSCRIPT_STORAGE.md` — **the six dispositions are RULED; cite
  them as decisions.** **Nothing is MET, no surface status moved, and the §7 acceptance fails
  today** — the expected state of a just-ratified contract.
  **⚠ SURFACE COUNT IS NOW 21, NOT 19.** `logs/turns_demo.jsonl` (**row 20**) and
  `logs/router.jsonl` (**row 21**) are ruled IN SCOPE and BLOCKING. **The writer fix must cover
  ROW 19, ROW 20 AND ROW 21 TOGETHER, or none of them meaningfully lands** — and **row 20 is the
  worst of the three: the only surface carrying BOTH SIDES of the conversation** (`query` *and*
  `reply`) with `member` and ~35 routing fields beside them. Write-path rows went 3 → 5.
  **THE COUNT HAS NOW MOVED TWICE (18 → 19 → 21), each time discovered while doing something
  else.** Read it as **twenty-one ENUMERATED, not twenty-one EXISTING**.
  **STANDING RULE, beyond this contract: "a bare truncated hash is dictionary-testable and may
  never be a load-bearing identifier."** Binds `query_hash` (unkeyed, 64-bit), which is
  load-bearing **today**. Q5's `turn_id` satisfies the rule by removing the dependency rather
  than strengthening the digest. **Do not build a new identifier this way.**
  **⛔ THE CRITICAL ORDER IS RULED AND BINDING — do not reorder it:**
  **source fix → commitments while keys exist → historical erasure → key destruction.**
  Each inversion has its own failure: erase-before-commit forfeits verifiability permanently
  (**observed: HA-46A, 0 of 356**); commit-before-source-fix commits a corpus still growing;
  erase-before-source-fix clears a backlog that immediately refills (**why HA-46 was stopped**).
  **BILL'S ACCEPTED LOSS, ON THE RECORD: the migration DELETES the 425 `.txt` files.** The only
  human-readable rendering of every past conversation goes, irreversibly. Verifiability survives
  in the `.jsonl` commitment; **readability does not, and no later dispatch can recover it.**
  **NINE-STEP BUILD ORDER is the contract's own sequence (§6A).** **Step 2 (session key/custody)
  is the PRECONDITION for step 5 (the read path)** — a read path must answer Q2's *"for whom"*
  before it can be correct, and an in-memory buffer built before step 2 would show every viewer
  every member's words, private only by accident of deployment. **Step 2 is shared work with
  `REQ_ERASURE_SURFACES` Q2/step 4 — plan them together, not twice.**
  **⏳ STILL TIME-CRITICAL: bill/maya/sam all still hold keys, so 100% of the 27,732 turns are
  committable today.** That window closes when step 8's key destruction runs.
  No harness run: no code changed. **CLAIM IMPACT: none.** **Nothing ruled MET.**

- **Roadmap lane — LANDED EARLIER: HA-47** (**DOCS + READ-ONLY — the row-19 storage contract
  drafted; NO CODE CHANGED**) —
  **`REQ_TRANSCRIPT_STORAGE` IS DRAFTED AND NOTHING IN IT IS RULED.**
  `docs/requirements/LATEST_REQ_TRANSCRIPT_STORAGE.md`. Six PROPOSED dispositions with
  alternatives; **do not cite any of them as a decision.**
  **⏳ TIME-CRITICAL, AND THIS IS THE ONE THING TO ACT ON: bill, maya and sam ALL STILL HOLD
  KEYS, so 100% of the 27,732 transcript turns are committable TODAY.** HA-46A retained
  **zero** commitments for its 356 entries because those subjects' keys were already gone.
  **Row 19's window is still open and closes the moment Q2's key destruction runs against these
  three members.** TD-R-189's rule is now a binding contract clause: **mint commitments first,
  verify, then erase — never erase plaintext after the key that could commit to it is gone.**
  **⚠ TD-R-190 — THE OBVIOUS ROW-19 FIX IS A TRAP. DO NOT POINT THE DASHBOARD AT `/api/turns`.**
  HA-45 offered that as option B and it would have worked flawlessly — same renderer, same
  shape — **but `/api/turns` reads `logs/turns_demo.jsonl`, which carries `query` AND `reply`
  verbatim plus `member`.** It is in **no inventory** and **no erasure module reaches it**. The
  swap would have closed row 19 on paper while leaving the same words on disk one file over,
  **now including HIP's replies.** `logs/router.jsonl` is a second such surface. Both need
  dispositions in `REQ_ERASURE_SURFACES`.
  **`query_hash` IS NOT A SAFE CORRELATOR:** it is a bare, unkeyed, truncated SHA-256 —
  dictionary-testable, R16's exact prohibition. It is the vignette's *existing* plaintext-free
  path, so **do not build on it**; Q5 proposes a keyed commitment instead.
  **CONSUMER TRUTH, worth knowing before any row-19 build: of SIX consumers of
  `logs/transcript/`, exactly ONE needs the words** — the live band, and only the current
  session. `TurnBubble` renders only `speaker`, `member_id`, `tier`, `text`. **The consent
  vignette's 40-char prefix is an identity match, not a content assertion, and its OR-branch
  already works without plaintext** — dropping it costs no coverage.
  **"NINETEEN SURFACES" MEANS NINETEEN ENUMERATED, NOT NINETEEN EXISTING.** HA-41's inventory
  was scoped, not wrong: a surface no erasure module mentions cannot be found by reading erasure
  modules. That blind spot produced TD-R-188 and has now produced TD-R-190.
  **Row 19 is still BLOCKING and its writer still produces plaintext.** No harness run: no code
  changed. **CLAIM IMPACT: none** — a contract is not a run. **Nothing ruled MET.**
  See `docs/dispatches/DISPATCH_HA47_TRANSCRIPT_STORAGE_CONTRACT__six-dispositions-two-new-surfaces-window-open__v20260812_0948.md`.

- **Roadmap lane — LANDED EARLIER: HA-46A** (**CODE — row 7's legacy corpus erased**) —
  **`recall_audit.jsonl` IS CLEAN. All 356 legacy plaintext entries erased**, entry count
  preserved 360→360 (a field was removed, never a record), 119,259→101,896 bytes.
  **Restart-proved in a fresh process, both ways: 0 text-bearing keys through the supported
  reader, 0 of 6 query strings in the raw bytes**, with all 360 entries and the 4 HA-45-era
  commitments still intact.
  **⚠ ZERO COMMITMENTS COULD BE RETAINED — all 356 are METADATA-ONLY, and this is the finding,
  not an omission.** The 356 name 261 distinct subjects and **none of them still has a key file**
  (the store is healthy at 1,089 keys; those subjects are harness fixtures whose keys went in
  HA-14's 1,390-key sweep). **No key was invented to manufacture a commitment**, per the ruling.
  **So for that corpus, "a later-supplied copy can still be verified" is permanently
  unobtainable.** Costless here — six fixture strings, no member content.
  **READ THIS BEFORE BUILD 2 — TD-R-189: a commitment can only be retained if the subject's key
  OUTLIVES the plaintext.** The ratified build order happens to put corpus erasure (step 2)
  before key lifecycle (step 4), which is the safe order — **but nothing states that the order is
  a REQUIREMENT rather than a coincidence**, and build 2 faces this against 27,732 turns
  belonging to real member sessions rather than fixtures.
  **IF YOU TOUCH `harness/recall_audit_erasure.py`, FOUR THINGS ARE LOAD-BEARING:** atomic
  temp+fsync+`os.replace` (a crash cannot half-erase); **dry-run default** (a destructive default
  is how a survey becomes an incident); idempotent (safe to retry); and **key access READ-ONLY** —
  `_load_or_create_member_key` would CREATE, resurrecting an erased subject's key and committing
  against a freshly-minted key that proves nothing. **No backup copy is made, on purpose:** a
  backup relocates plaintext instead of erasing it.
  **⛔ ROW 19 IS STILL STOPPED AND STILL BLOCKS THE PHASE.** `logs/transcript/` is untouched and
  **verified so** — 425 `.jsonl` + 425 `.txt`, 27,732 lines, byte-identical — and **its writer is
  still producing new plaintext.** The two consumers needing raw words (the demo dashboard's
  `/api/transcript` band and `passthrough_consent_vignette.py:202`) are unchanged; four options
  are in HA-45's doc, **none chosen — NEEDS BILL.**
  RUNS: binding **1179 passed / 0 failed / 9 xfailed** (57 files), `--layer 7` **EXIT 0**
  (L7 27/27, L7V2 27/28, AUDIT 9/9), **RATCHET PASS**, memory **13/17 inside the pin**.
  **CLAIM IMPACT: none** — C-09 gains nothing while the larger surface still holds 27,732 turns
  and keeps growing. **Nothing ruled MET.**
  See `docs/dispatches/DISPATCH_HA46A_RECALL_AUDIT_CORPUS_ERASED__356-cleaned-zero-commitments-retained__v20260812_0702.md`.

- **Roadmap lane — LANDED EARLIER: HA-45** (**CODE — erasure build 1; ROW 7 BUILT, ROW 19
  STOPPED**) —
  **ROW 7 IS DONE: `recall_audit.jsonl` no longer writes the query's words.** It writes
  `query_commitment`, **keyed to the SUBJECT** — so when Q2 destroys an erased member's key,
  **their commitments become unverifiable by anyone** and the record degrades to an opaque
  token. A shared key would have made this surface a dictionary-testing oracle.
  **IF YOU TOUCH THIS PATH, TWO THINGS ARE LOAD-BEARING:** (1) `verify_recall_audit_query`
  **reads the key without creating it** — `_load_or_create_member_key` would MINT a replacement
  for an erased member and resurrect key material Q2 destroyed; a test asserts the keys dir
  stays empty. (2) **The forbidden-key strip is a second, independent barrier** and it is not
  decoration: with the primary fix reverted, the "no plaintext" twins still passed *because the
  strip caught it*. That is also why a source-level twin exists.
  **⛔ ROW 19 IS STOPPED AND THE PHASE CANNOT COMPLETE WITHOUT IT (Q6 ruled it blocking).**
  `logs/transcript/` still writes verbatim member utterances. **Two consumers genuinely need the
  words downstream: `server/demo_dashboard.py` `/api/transcript` renders the conversation to the
  demo's top band, and `eval/passthrough_consent_vignette.py:202` correlates turn 2 by matching
  the query's first 40 characters.** **Do not "just switch it to commitments"** — that blanks the
  demo's transcript band, and the demo is the first finish line.
  **THE WORKAROUND EXISTS AND WAS DELIBERATELY NOT TAKEN:** Q3-C permits *sealed content*, which
  would feed the dashboard via decrypt — but it needs a key decision that **is** Q2 / build-order
  step 4 and condition 1 of the erasure-enablement gate. **Sealing transcripts before the custody
  work would create a second key convention to consolidate later.** Four options are in the
  dispatch doc; **none chosen — NEEDS BILL.**
  **CORPUS MAPPED FOR BUILD 2, AND NOT TOUCHED: 425 `.jsonl` + 425 `.txt` = 850 files**, 27,732
  turns, ~10.5 MB, bill 10,556 / maya 9,096 / sam 8,080, span 2026-07-18 → 08-11. **Both formats
  hold the words — the `.txt` is a second full copy, not a derivative.** Recall audit: **356 of
  356 entries carried query text**; the 4 written since carry commitments, so **build 2's target
  there is the first 356 entries, not the whole file.**
  **HA-46 (build 2) IS STOPPED AT ITS PRECONDITION** — erasing the transcript corpus while the
  transcript writer still appends plaintext would clear a backlog that immediately refills.
  Row 7's half could run independently, but splitting HA-46 is Bill's call.
  RUNS: binding **1168 passed / 0 failed / 9 xfailed** (56 files), `--layer 7` **EXIT 0**
  (L7 27/27, L7V2 27/28, AUDIT 9/9), **RATCHET PASS**, memory **13/17 inside the pin**. New
  battery `eval/test_recall_audit_no_plaintext.py` is **registered in `run_harness.sh`**.
  **Nothing ruled MET; the §7 acceptance still fails — row 19 alone guarantees it. CLAIM IMPACT:
  none.**
  See `docs/dispatches/DISPATCH_HA45_STOP_PLAINTEXT_AT_SOURCE__row7-built-row19-stopped-on-two-consumers__v20260811_2224.md`.

- **Roadmap lane — LANDED EARLIER: HA-44** (**DOCS ONLY — REQ_ERASURE_SURFACES RATIFIED; NO CODE
  CHANGED**) —
  **BILL RULED ALL SIX §6 QUESTIONS ON 2026-08-11 AND THE REQ IS RATIFIED.** Rulings verbatim in
  the REQ's §0A. **`docs/requirements/LATEST_REQ_ERASURE_SURFACES.md` dispositions are now
  RULED, not proposed — cite them as decisions.**
  **BUT NOTHING IS MET AND NO SURFACE STATUS MOVED.** The REQ header is still `PLAN`, every
  HA-41 status is untouched, and **the §7 acceptance FAILS TODAY at eleven rows.** That is the
  ratified target, not a regression. **Ratifying what must happen does not make it have
  happened**, and no work below has started.
  **THE RULINGS:** **Q1** — "governed surface" = **ALL NINETEEN**; the narrow graph+payload
  reading is rejected. **Q2** — destroy key material whose only purpose is the erased subject's
  data (per-fact DEKs, member keypair, wraps); **shared household/care-team keys are NEVER
  destroyed** — remove the erased member's wrap and **rotate the shared key to a new epoch**, so
  **no bystander's data is erased.** **Q3** — rows 7 and 19: **C plus A**, stop writing plaintext
  at the source *and* erase the existing corpus. **Q4** — row 11: **B**, seal render records at
  write time to a per-record key destroyed on erasure. **Q5** — rows 10 and 18: **B**, tombstone
  carries an opaque erasure id + commitment only, naming nothing. **Q6** — row 19 is **IN SCOPE
  and BLOCKING**; fixing transcripts is immediate work.
  **THREE CONSEQUENCES THE RULINGS DO NOT STATE, AND THE FIRST IS PERMANENT:**
  **(1) Q5 CONTRADICTS THE TOMBSTONE THAT EXISTS TODAY** — `fact.erased` currently NAMES what was
  erased, and the chain is append-only, so **those events cannot be removed and stay
  non-compliant forever.** The format change is forward-only by construction; do not file this as
  a fixable defect. **(2) Q2 NEEDS MACHINERY THAT DOES NOT EXIST** — wrap removal and epoch
  rotation, **overlapping the key-custody consolidation already required by the
  erasure-enablement gate; plan them together, not twice.** **(3) ROWS 7, 11 AND 19 ARE
  WRITE-PATH CHANGES, NOT ERASURE CHANGES** — erasure reaching further cannot fix a surface that
  keeps generating plaintext.
  **BUILD ORDER IS REQ §11**, seven steps: (1) stop plaintext at source — **blocking**, row 19
  then 7; (2) erase the existing plaintext corpus; (3) seal render records at write time;
  (4) wrap removal + epoch rotation; (5) tombstone and audit surfaces go opaque; (6) metadata
  surfaces; (7) **extend the verifier to all nineteen — last, because it verifies the other
  six.** Until step 7, the acceptance is a manual claim.
  **THE ERASURE-ENABLEMENT GATE IS UNTOUCHED and NO STEP IS AUTHORISED ON REAL HOUSEHOLD DATA.**
  **CLAIM IMPACT: none** — C-09 is what this bears on, but a ratified specification is not a run.

- **Roadmap lane — LANDED EARLIER: HA-43** (**DOCS ONLY — PHASE 3 OPENER; NO CODE CHANGED**) —
  **`REQ_ERASURE_SURFACES` IS DRAFTED AND NOTHING IN IT IS RULED.**
  `docs/requirements/LATEST_REQ_ERASURE_SURFACES.md`. 19 surfaces, **every disposition marked
  PROPOSED**; three rows carry OPTIONS for Bill instead of proposals. **Do not cite any row of
  it as a decision.**
  **ISSUED AS HA-42, RUN AS HA-43.** HA-42 was already taken by the ruling enactment at
  `8e427dd`; item 10 forbids renumbering an ID four documents already cite.
  **HA-41'S THREE UNKNOWNS ARE RESOLVED TO ZERO, READ-ONLY: summaries NONE-EXISTS** (no
  summary store exists anywhere; consolidation emits derived *facts*, already covered by the
  lineage closure), **exports NONE-EXISTS** (no export writer exists at all), **caches
  IN-MEMORY ONLY** (six, all process-local; two hold subject data — `zep_store`'s hot cache
  and `sio`'s utterance cache — **and the lifecycle's `restart` step is what clears them**, so
  no purge path is proposed, only a REAL process restart in the test).
  **FINDING — TD-R-188, A NINETEENTH SURFACE THE INVENTORY MISSED: `logs/transcript/` retains
  VERBATIM member utterances** — `member_id` plus both sides of every turn, in `.jsonl` and
  `.txt`, *"never truncated, never summarized"*, on disk for three members today, **and no
  erasure module references transcripts.** **Strictly larger than TD-R-173**, and like it,
  **plaintext — no key destruction makes it opaque, because it was never sealed.**
  **READ THIS BEFORE TRUSTING ANY SURFACE INVENTORY: HA-41's was built by asking "what does
  erasure do here?", and that question cannot see a surface no erasure module mentions.** It
  named its own blind spot and could not enumerate what fell inside it. **That is why the REQ's
  no-UNKNOWN gate is written as STANDING, not one-time** — the count went from zero back to
  non-zero within a day.
  **TWO WORDS IN BILL'S LIFECYCLE ARE UNDEFINED AND BLOCK EXECUTION, NOT JUST WORDING:
  "governed surface"** — if it means all nineteen the system fails today at eleven rows, if it
  means graph + payload store it passes today — **and "relevant keys"**, since destroying a
  shared household seal key erases other members too, leaving lifecycle step 5 not executable.
  **NEEDS BILL: six decisions**, listed in the REQ §6 and the dispatch doc §6.
  **THE ERASURE-ENABLEMENT GATE IS UNTOUCHED** — neither condition started. **This REQ is a
  specification, not a step toward enabling erasure on real data.** No harness run: no code
  changed, so HA-41's runs remain the standing evidence. **CLAIM IMPACT: none** — C-09 is what
  this will eventually bear on, but a specification is not a run.
  See `docs/dispatches/DISPATCH_HA43_ERASURE_SURFACES_REQ__nineteen-surfaces-three-unknowns-resolved-one-new__v20260811_2050.md`.

- **Roadmap lane — LANDED EARLIER: HA-42** (**DOCS ONLY — BILL'S THREE RULINGS ENACTED; NO CODE
  CHANGED**) —
  **`REQ_OFFER_MECHANISM` IS MET — Bill's ruling, 2026-08-11.** This supersedes every prior
  statement in this document and elsewhere that it is NOT MET. Ruled from the **A1–A20 + A20b
  table at 17 PASS / 0 FAIL / 4 CANNOT RUN**, the A20b manifest check, and HA-41's final runs:
  binding **1158/0**, `--layer 7` **exit 0**, **no deterministic regression**, memory **13/17**
  inside the 13–15 pin.
  **READ THIS BEFORE CITING THE MET RULING: THE FOUR CANNOT RUNs ARE EXACTLY THE FOUR CONDITIONAL
  CLAUSES — A2, A8, A9, A11 — AND THEY REMAIN CONDITIONAL ON THEIR NAMED FEATURES** (reminder
  delivery, transport layer, member-initiated capability path, explanation feature). **MET does
  not mean everything ran, and the ruling neither waives those clauses nor converts them to
  PASS.** Each binds when its feature exists. The three clauses that were UNCONDITIONAL CANNOT
  RUNs at HA-28 — **A6, A12, A16** — are now PASS, **built rather than excused**; A19's FAIL was
  closed by HA-36.
  **C-14 IS PROVEN — Bill's ruling, 2026-08-11**, its stated missing condition (the
  utterance→`ResponseKind` classifier) now existing with the ratified v1 vocabulary and the grant
  path exercised end to end. **Banked as CLAIMS LEDGER v5**
  (`docs/deliverables/HIP_ClaimsLedger__v5-c14-proven__v20260811_1549.md`); v4 flagged SUPERSEDED
  and retained unaltered; symlink, MANIFEST and INDEX repointed. **Wording unchanged, ONE status
  cell edited, nothing else** — fifteen claims verified byte-identical to v4, **cap unaffected at
  15/15 because a status change is not an addition.**
  **FLAGGED, NOT FIXED, under Bill's own "change nothing else": C-14's TIMELINE cell still reads
  "after the response classifier is built"** — the condition the ruling reports satisfied. Left
  verbatim; the timeline column is forecast-only by the ledger's governing rules and cannot
  influence a status, so nothing is affected. **Correcting it is Bill's call, not a session's.**
  **STATUS IS STILL DECLARED, NOT COMPUTED.** The status generator remains the named next build,
  and `scripts/ceiling_status.py` does not read the claims ledger or this REQ — it reads only
  `REQ_STRUCTURAL_CEILING` and `REQ_CEILING_ACCEPTANCE`, **so no board went stale from these
  rulings and none was regenerated.**
  **OFFER WORK STOPS HERE, per Bill's ruling 3 and the plan of record.** Do not open the next
  offer step. **The four conditional clauses are NOT a backlog item created by this ruling** —
  they bind if and when their features are built for their own reasons.
  **HA-42 RULED NOTHING AND CHANGED NO CODE.** It recorded Bill's rulings and repointed the
  registers. Reported terminal-only; **no dispatch doc exists for HA-42 by design.** Ledger row
  in `docs/INDEX.md` carries the detail.

- **Roadmap lane — LANDED EARLIER: HA-41** (**CODE + INVENTORY + COLLECTOR**, `d2d2e9d`;
  segment 1's code landed at `1fa2258`) —
  **A1–A20 + A20b IS NOW 17 PASS / 0 FAIL / 4 CANNOT RUN**, all four CANNOT RUNs being the
  conditional clauses. **`REQ_OFFER_MECHANISM` IS STILL NOT RULED MET — the table is the
  deliverable and the ruling is Bill's.** Nothing in HA-41 rules it.
  **HA-41 CARRIED THREE DISPATCHES' WORK IN ONE COMMIT, AND THAT IS A REPORTED PROCESS
  FAILURE, NOT A CONVENIENCE: HA-39 NEVER LANDED** — it finished its build and its A1–A20 run
  and ended with no commit and no push (STANDARD PREAMBLE item 8). Its work, and HA-40's, sat
  uncommitted until HA-41 committed them. Nothing was lost and no other lane published them,
  but the tree diverged from `origin/roadmap` for hours with no record.
  **A6 IS NOW MANDATORY WITH NO BYPASS.** `OfferInstanceRegistry.create()` enforces minimality
  on every call; HA-38's opt-in `require_minimal_for` is **removed and nothing replaced it**.
  The situation **kind is read off the situation, never accepted from the caller**. Fixtures got
  a structurally separate path (`FixtureOfferRegistry`), **not a relaxation** — and a standing
  test parses every `.py` under `harness/` and `memory_engine/` and fails if any imports `eval`,
  so production provably cannot reach the subclass.
  **TD-R-184 and TD-R-186 ARE BOTH RESOLVED** (by HA-39 and HA-40 respectively; landed by
  HA-41). The manifest fold is `granted |= (scope_after - scope_before)` and now subtracts
  `authority_change`, so `authority_manifest_for` reports ACTIVE authority and agrees with
  `current_authority`. **No redesign — still derived by replay, never stored.**
  **ERASURE-SURFACE INVENTORY (read-only, nothing changed): 18 surfaces — 4 covered /
  3 partial / 6 untouched / 3 unknown / 1 empty.** The two that most affect the plan's
  acceptance question are **raw query text (TD-R-173)** and **R26's verbatim render records** —
  the words shown to a member, made durable by HA-36 and **erased by nothing.**
  **THE ERASURE-ENABLEMENT GATE ABOVE IS UNCHANGED BY THIS INVENTORY** — it is a survey, not a
  gate condition; neither custody consolidation nor the cascade is started.
  **TD-R-187 FILED, NOT FIXED: the live-layer collector stamps each row with the commit at
  WRITE time, not RUN time.** A `--full` takes 15–20 minutes, so anything committed mid-run
  mislabels the rows — observed today, run `20260811T195452_1fa2258` measured pre-fix code and
  is labelled with the commit that fixed it. **It matters because that CSV is the instrument
  the live-model reproducibility rule is to be set FROM (plan step 12)**, and "same commit,
  different outcome" is exactly the question a mislabelled row corrupts, silently.
  RUNS: binding standing battery (55 files) **1158 passed / 0 failed / 9 xfailed**, `--layer 7`
  **EXIT 0**, memory harness **13/17 inside the 13–15 pin**. Two `--full` collector runs, both
  exit 0, both **BINDING TESTS PASS**; **L4:PW027 differed between them on byte-identical code
  back to back** (run1 PASS / run2 FAIL). Across all 18 recorded runs
  **`L2:routing_showcase.T04` is FAIL 18 / PASS 0 — it has never passed.**
  **CLAIM IMPACT: none.** No claim status moved and none may — status is computed from standing
  runs by the generator, never declared by a session.
  See `docs/dispatches/DISPATCH_HA41_TDR186_ERASURE_INVENTORY__fix-landed-18-surfaces-two-collector-runs__v20260811_1510.md`.

  > **STALENESS NOTED RATHER THAN QUIETLY PAPERED OVER (recorded by the HA-41 close-out,
  > 2026-08-11):** the block below claims LAST LANDED HA-28, but **HA-29 through HA-40 landed
  > without updating CURRENT STATE** — the same failure this document already records for
  > HA-09 through HA-17 further down, now recurred over a longer span. **Their entries are NOT
  > backfilled here**, for the reason given in that earlier note: reconstructing another
  > session's state claim from its report is exactly the drift this document exists to prevent.
  > The HA-41 entry above is written from HA-41's own doc and covers HA-39's and HA-40's work
  > only because HA-41's commit is what landed it.
  > **The dispatch ledger in `docs/INDEX.md` is the complete index** — HA-39 and HA-40 were
  > missing from it too, and the HA-41 close-out added their rows in the same commit as this
  > note. **HA-41's landing was itself incomplete on both counts until that commit**, which is
  > recorded here rather than fixed silently.

- **Roadmap lane — LANDED EARLIER: HA-28** (**CODE + ACCEPTANCE MEASUREMENT**) —
  **A1–A20 HAS BEEN RUN: 12 PASS / 1 FAIL / 7 CANNOT RUN. *(counts corrected HA-29 2026-08-10, caught by Bill; was 11/1/8 — counted from HA-28 §4's table)*  `REQ_OFFER_MECHANISM` IS NOT
  RULED MET — the table is the deliverable and the ruling is Bill's.**
  **THE FAIL IS A19, AND IT IS A REAL DEFECT: the governed record survives a restart and the
  WORDS SHOWN DO NOT.** `OfferInstanceRegistry` is in-process only, so after a restart the
  record proves which TEMPLATE was used and nothing more — a member disputing what they were
  shown could be told the template id. **Proven across two real processes**, not inferred.
  **FIX NEEDED: a durable offer-instance store, or slot values + rendered text carried in the
  R23 event.** Deliberately not built — it is a storage change to the offer path.
  **THE EIGHT CANNOT RUNs ARE MISSING PRODUCT BEHAVIOUR, NOT MISSING TESTS:** no
  reminder-delivery path (A2), no delta-minimality machinery (A6), no transport layer (A8),
  no member-initiated capability path (A9), no explanation feature (A11), no revocation path
  (A16), and **the still-missing utterance→`ResponseKind` classifier (A12)**.
  **THERE IS STILL NO PRODUCTION CALLER OF THE OFFER PATH AT ALL** — all eight `present()`
  callers are fixtures. That single fact is what most of the CANNOT RUNs are expressing.
  **R23 WIRING IS FINISHED:** `present(instance=…)` assembles the full sixteen-field record.
  **`instance` is OPTIONAL on purpose** — making it mandatory would refuse calls that succeed
  today, which is a behaviour change needing its own dispatch. Enforcement is by standing
  test, and a test fails loudly if that ever changes silently.
  **WHEN VERIFYING A REQUIREMENT, COMPARE AGAINST ITS FIELD LIST, NOT AGAINST "DOES IT RUN".**
  HA-27 found a 3-of-16 record sitting behind four passing lifecycle tests.
  RUNS: batteries **970 **SUPERSEDED as a canonical battery result — the exact invocation was not recorded and the result is contradicted by the documented whole-suite invocation (HA-31: 1048 passed / 31 failed). Old number preserved, never deleted.** passed / 0 failed**, L7 27/27, L7V2 27/28, AUDIT 9/9, **RATCHET PASS
  at exit 0**, memory harness **13/17 inside the pin**.
  **CLAIM IMPACT: NONE.** 222 offer tests ran, but every one was already standing —
  **re-running a standing test confirms it still holds; it is not new evidence.**
  See `docs/dispatches/DISPATCH_HA28_OFFER_ACCEPTANCE__r23-wiring-finished-and-a1-a20-measured__v20260810_0917.md`.

- **Roadmap lane — LANDED EARLIER: HA-27** (**CODE — offer mechanism §12 step 8**) —
  **THE GOVERNED RECORD IS COMPLETE AND THE AUTHORITY MANIFEST EXISTS.**
  `harness/governed_record.py` + 29-test battery. R23's 16 fields, R24's process-not-profile
  discipline, R25's cumulative manifest.
  **WHAT VERIFY-FIRST FOUND, AND WHY IT MATTERS TO YOU:** HA-08's four terminal chains all
  worked — but the event carried **3 of R23's 16 fields**, and nothing had ever revealed it
  because **no check compared the event against R23's list.** If you are verifying a
  requirement, compare against its own field list, not against "does it run".
  **FOUR THINGS THAT ARE LOAD-BEARING IF YOU EXTEND THIS:**
  **(1) THE R23 BLOCK MERGES *UNDER* THE LEDGER'S KEYS.** A caller must never be able to
  rewrite `transition` or `situation_id` by passing them in — that is what keeps the state
  machine's account of itself authoritative. A test asserts it.
  **(2) `event_id` IS DETERMINISTIC, NOT RANDOM.** The ledger replays on every load; an id
  that changed per replay would make the record unciteable.
  **(3) SCOPE FIELDS ARE SORTED LISTS, NOT SETS.** Sets have no stable serialisation, and the
  record must be comparable byte-for-byte across replays.
  **(4) THE MANIFEST IS DERIVED, NEVER STORED.** `authority_manifest_for` replays ACCEPTED
  events. **Do not add a stored manifest** — it would be a second source of truth about what a
  member has granted and would disagree the first time an event was replayed or corrected.
  **A DECLINED / LAPSED / INVALIDATED OFFER CONTRIBUTES NOTHING TO THE MANIFEST** — not a
  trait, not a warning, **not a negative entry.** It appears only in `decision_history_for`.
  **AN ABSENT FIELD IS RECORDED AS ABSENT, NEVER INVENTED.** `trigger_rule_version` is empty
  where the boundary lacks the `Situation`. R4 forbids a fabricated trigger label, and a
  plausible guess in a governed record is worse than a blank.
  **CLAIMS LEDGER IS NOW v4 AND THE CAP IS FULL — 15/15.** C-15 added (Bill's wording,
  PROVEN). **A sixteenth claim requires a RETIREMENT; that is Bill's ruling, not a session's.**
  **PARTIAL WIRING, STATED PLAINLY:** a bare `ledger.present(...)` without `record=` still
  writes the original keys. The mechanism is complete; the wiring is not.
  RUNS: batteries **963 passed / 0 failed**, L7 27/27, L7V2 27/28, AUDIT 9/9, **RATCHET PASS
  at exit 0**, memory harness **13/17 inside the pin**. **Nothing ruled MET.**
  **FLAGGED FOR BILL: R23/R24/R25 have no ledger claim, and with the cap full that gap cannot
  be closed by adding one.**
  See `docs/dispatches/DISPATCH_HA27_OFFER_STEP8__governed-record-completed-and-authority-manifest__v20260810_0848.md`.

- **Roadmap lane — LANDED EARLIER: HA-26** (**CODE — offer mechanism §12 step 7**) —
  **A DECLINE IS CONTROL STATE AND CANNOT REACH THE GRAPH OR MODEL CONTEXT.**
  `harness/control_plane_isolation.py` + 38-test battery, enforcing RULING 5 / R20-R22.
  **TWO MECHANISMS, AND BOTH ARE NEEDED.** `refuse_member_fact_write` catches a runtime
  attempt but is blind to an import not yet called; `assert_control_plane_is_isolated`
  catches the attempt being *possible* but is blind to a runtime dictionary key.
  **IF YOU EXTEND THIS, FOUR THINGS ARE LOAD-BEARING:**
  **(1) `refuse_member_fact_write` MUST KEEP ITS NO-SUCCESS-PATH SHAPE.** A test asserts its
  body has no conditional. A version that sometimes permitted a response into the graph would
  need a rule for when, and Ruling 5 has none.
  **(2) DECLARE NEW MODULES, BY WHAT THEY ARE.** A module that HOLDS OFFER STATE goes in
  `CONTROL_PLANE_MODULES`; a module IN THE OFFER PATH goes in `OFFER_PATH_ENTRY_MODULES`.
  Both scans are declaration-driven and **neither can detect an undeclared member.**
  `control_plane_isolation.py` itself is in neither, on purpose — it is a checker, holds no
  offer state, and renders nothing.
  **(3) R20's FOUR READS ARE NAMED BY THE CALLER.** Anything outside `suppress_spent_offer`,
  `member_own_history`, `validate_grant_state`, `compliance_audit` is refused. "We needed the
  data" is how a compliance read becomes a personalization read.
  **(4) R22 BANS CONVERSION METRICS BY EXISTENCE, NOT USE.** An `acceptance_rate` counter is
  one whether or not anything reads it.
  **THE ISOLATION IS ALREADY CLEAN, AND HA-22 IS WHY** — its leaf-module split of
  `CANONICAL_ATTRIBUTES` keeps `extraction_queue` out of this closure too. One fix, two
  requirements. **Do not re-merge that leaf.**
  **CLAIMS LEDGER IS NOW v3** — `LATEST_HIP_ClaimsLedger.md` → v3, with **C-14** (Bill's
  wording, PARTIAL, timeline *"after the response classifier is built"*). v2 superseded and
  retained. **Cap is 15 and 14 are used.**
  RUNS: batteries **934 passed / 0 failed**, L7 27/27, L7V2 27/28, AUDIT 9/9, **RATCHET PASS
  at exit 0**, memory harness **13/17 inside the pin**. **Nothing ruled MET** — A1-A20
  unattempted; REQ still DRAFT-RATIFIED-PENDING.
  **FLAGGED FOR BILL: RULING 5 itself has no ledger claim.** The isolation built here is a
  substantial privacy guarantee that nothing in the ledger covers.
  See `docs/dispatches/DISPATCH_HA26_OFFER_STEP7__control-plane-isolation-decline-is-not-a-member-fact__v20260810_0805.md`.

- **Roadmap lane — LANDED EARLIER: HA-25** (**CODE — offer mechanism §12 step 6**) —
  **`harness/offer_response.py` IS NOW THE ONLY PATH BY WHICH AN OFFER RESOLVES AND THE ONLY
  PATH BY WHICH SCOPE CHANGES.** R15 explicit response, R16 exact set equality, R17 authority
  validation, R18 integrity tie-in. 32-test battery.
  **IF YOU EXTEND THIS, THREE THINGS ARE LOAD-BEARING AND EASY TO UNDO BY ACCIDENT:**
  **(1) `apply_response` MUST NOT GAIN A ROLE PARAMETER.** R17 is enforced by the ABSENCE of
  `role`/`is_owner`/`is_caregiver`/`has_prior_access` — there is nothing to bypass, and a
  signature test fails if one appears. Authority is an explicit `DecisionAuthority` for an
  exact decision domain; wildcards are refused at construction.
  **(2) THE RESPONSE ARRIVES CLASSIFIED, NEVER AS PROSE.** `apply_response` takes a
  `ResponseKind`, never text. R15 forbids reinterpreting a response, and parsing prose here
  would put back the generative surface HA-22 removed. `AMBIGUOUS` is the safe answer.
  **(3) R18 IS CHECKED BEFORE THE RESPONDER, DELIBERATELY.** A wrong-member response to a
  corrupted offer must report the corruption, not the responder — the checks pass in either
  order and only one order tells the truth. There is a test for the ordering itself.
  **THE STATE MACHINE IS STILL HA-08's.** This module classifies, validates, applies a set
  union and calls `spend_ledger`. **Do not add a second one** — it would be a second source
  of truth about whether an offer is resolved.
  **ADDING AN OFFER-PATH MODULE? ADD IT TO `OFFER_PATH_ENTRY_MODULES` FIRST.** HA-22's note
  warned this, and HA-25 confirmed it live: `harness.offer_response` was invisible to the
  purity scan (10 modules) until declared (11, still pure). It is the one failure mode that
  check cannot self-detect.
  **WHAT IS NOT BUILT:** no `ResponseKind` classifier. **Step 6's boundary is complete and
  its caller is not** — turning an utterance into a kind is unbuilt, on purpose.
  **RIDER LANDED:** `REQ_HARNESS_RUNNER` now carries HA-24's exit-code rule, closing HA-24's
  own finding that the runner's exit semantics had no REQ home.
  RUNS: batteries **896 passed / 0 failed**, L7 27/27, L7V2 27/28, AUDIT 9/9, **RATCHET PASS
  at exit 0**, memory harness **13/17 inside the pin**. **Nothing ruled MET** — A1-A20
  unattempted, REQ still DRAFT-RATIFIED-PENDING.
  **FLAGGED FOR BILL: R16 — "acceptance grants exactly what was shown" — has NO ledger claim.**
  It is the strongest guarantee step 6 builds and nothing in the ledger covers it (cap 15,
  13 used).
  See `docs/dispatches/DISPATCH_HA25_OFFER_STEP6__explicit-response-exact-scope-authority-validated__v20260810_0649.md`.

- **Roadmap lane — LANDED EARLIER: HA-22** (**CODE — offer mechanism §12 step 4**) —
  **THE OFFER PATH NO LONGER IMPORTS A MODEL CLIENT, AND THE ABSENCE IS NOW STRUCTURAL.**
  `harness/offer_purity.py` walks the offer path's **import closure** by AST and refuses if
  any module in it can reach a model client, interpreter, generation function or source of
  randomness. Wired into the standing battery (`eval/test_offer_purity.py`, 13 tests).
  **IT FOUND A REAL REACH ON ITS FIRST RUN:** the path imported `harness.extraction_queue`
  (the Groq/Ollama detector) via `inference_permit` and `write_origins` — **two hops below
  the single file HA-06's scans cover.** Nothing ever *called* the detector; both imports
  pulled `CANONICAL_ATTRIBUTES`. It was removed anyway, because step 4 requires that no model
  call CAN enter the path, and "imported but never called" is not a property a check can keep
  true.
  **`harness/attribute_vocabulary.py` IS A LEAF AND MUST STAY ONE.** It holds
  `CANONICAL_ATTRIBUTES` and imports **nothing**; `extraction_queue` re-exports the name so
  all twelve original call sites are unchanged. **Any import added to that leaf is inherited
  by the offer path** and undoes this silently — a battery test asserts it stays empty.
  **BEFORE ADDING A MODULE TO THE OFFER PATH:** add it to `OFFER_PATH_ENTRY_MODULES` in
  `harness/offer_purity.py`, or it is simply not scanned. The check refuses on zero modules,
  on a closure that does not expand, and on a forbidden module that no longer exists (a
  rename would otherwise disarm it silently) — but it cannot refuse on a path member nobody
  declared.
  **USE AST, NOT REGEX, IF YOU EXTEND THIS.** Two fresh proofs from this build: a regex for
  `generate(` returns three false positives (`X25519PrivateKey.generate()` in the crypto
  modules), and a substring scan of `offer_purity.py` fails against its own prose.
  RUNS: batteries **864 passed / 0 failed**, L7 27/27, L7V2 27/28, AUDIT 9/9, **RATCHET
  PASS**, `KEY-HYGIENE-ZERO-ORPHAN` PASS, memory harness **13/17 inside the pin**.
  **Nothing ruled MET** — A10 and A1-A20 unattempted; the REQ is still DRAFT-RATIFIED-PENDING.
  See `docs/dispatches/DISPATCH_HA22_OFFER_STEP4__no-generative-surface-closure-checked-model-client-removed__v20260809_2115.md`.

- **Roadmap lane — LANDED EARLIER: HA-20** (**CODE — harness hygiene + item 12 split**) —
  **`REQ_DERIVED_WRITE_CUSTODY` IS MET (Bill's ruling, 2026-08-07)** and the rule-3a fix is
  **RATIFIED: *"Scope follows the subject, not the author. Keep the fix."*** HA-19 offered
  to revert that change; it stands.
  **ITEM 12 IS NOW SPLIT, AND THIS CHANGES WHAT "DONE" MEANS — read it before claiming any
  build passes.** DETERMINISTIC layers (batteries, L7, L7V2, AUDIT, DISC, SCHEMA, VOICE and
  the ratchet over them) **remain binding and must pass every time.** LIVE-MODEL layers
  (L1, L2, L3, L4, L6) are **reported, not gated**, until a reproducibility rule exists.
  **NO best-of-N. NO invented pass threshold.** A live-layer red is still REPORTED — hiding
  one because it "doesn't gate" breaks the rule as surely as claiming a green ratchet.
  **THE DATA COMES FIRST:** `logs/harness/live_layer_results.csv` gets one row per
  live-layer scenario on **every** `--full`, automatically. The threshold is Bill's to set
  from that file; **do not invent one.**
  **THE ZERO-ORPHAN INVARIANT MOVED.** It is no longer a pytest battery test — it is
  `AUDIT:KEY-HYGIENE-ZERO-ORPHAN` in `eval/harness.py`, running after every layer including
  L7. It used to assert its postcondition *before* the biggest key producers ran, which is
  why every `--full` left keys behind and the next one aborted at the battery gate. Proven
  red-then-green with a planted stray key.
  **TEARDOWN IS WIRED into both layer-7 entrypoints in a `finally`**, plus a fifth producer
  nobody had counted (`ctxstrip_probe_owner`) that the classifier had been failing closed on
  and silently keeping.
  **TWO TRAPS WORTH KNOWING BEFORE YOU TOUCH PROBE PRINCIPALS:**
  **(1) Do NOT enrol a probe into the household circle to give it a wrap.** HA-20 tried
  exactly that (item 5 asked for it) and backed it out: circle membership makes the member a
  permanent participant in the household key tree, and teardown destroys its key — which
  breaks `ensure_household_keys` and therefore EVERY household-circle-shared write, the real
  demo's included. `_provision_household_access` is a documented no-op; the reasoning is in
  its docstring. **The decrypt-skip log noise stays. The real fix is in `read_user_facts`
  and is Bill's call.**
  **(2) Destroying a key without clearing the registry's `seal_pubkey` creates a silent
  desync** — fresh private key, stale registered pubkey, and the probe's own fact becomes
  unreadable to itself. **The symptom is "fact not present", never "key error."** Healed at
  enrolment and at teardown.
  **KNOWN BROKEN, FOUND HERE, NOT FIXED: `harness.household_keys.remove_circle_member`
  raises `sqlite3.OperationalError: no such column: epoch`** — it bumps a column the schema
  does not have. **Circle removal does not work today.** Out of scope; a schema change on the
  custody registry is not a hygiene-dispatch side effect.
  RUNS: batteries **851 passed / 0 failed**, L7 27/27, L7V2 27/28, AUDIT **9/9**, **RATCHET
  PASS**, memory harness **13/17 inside the pin**. `--full` run twice back to back with no
  hand cleanup — see the dispatch doc for both results and the live-layer split.
  See `docs/dispatches/DISPATCH_HA20_HYGIENE_AND_ITEM12__invariant-relocated-teardown-wired-item12-split__v20260809_2014.md`.

- **Roadmap lane — LANDED EARLIER: HA-19** (**CODE — both custody guards LIVE**) —
  **AUTHOR VALIDITY AND THE (visibility, owner) ASSERTION ARE NOW ENFORCED ON EVERY WRITE.**
  Guard B sits at `partition_crypto.classify_write` — the canonical pre-seal boundary, ONE
  site, **positive membership against the enrollment registry, fail-closed**. Guard A is the
  local structural assertion in `WriteClass.__post_init__` and **never consults enrollment**.
  Refusals land in `logs/custody/refusals.jsonl` **without the refused value**.
  **`REQ_DERIVED_WRITE_CUSTODY`'s ACCEPTANCE PASSES END TO END — C1, C2, C3, C4, C7 — AND
  THE REQ IS STILL NOT MARKED MET. Bill rules; the dispatch reports readiness.**
  **C1 IS 11/11 FOR THE FIRST TIME SINCE TD-R-171 WAS FILED.** A from-scratch seed under
  both guards lands 11/11 facts and every active row decrypts.
  **BEFORE YOU WRITE ANY TEST OR FIXTURE THAT CALLS `encode()`: IT MUST AUTHOR AS AN
  ENROLLED PRINCIPAL.** Six fixture sites across four files were writing as invented ids
  that existed in no registry, and all six went red the moment the guard landed. **The fix
  is to ENROL the principal, never to exempt the test** — `eval/harnesslib/principals.py`
  (`enrol_probe_author`) and `memory_harness._mint_principal` do it, and both de-register in
  teardown. A guard taught to ignore fixture-looking ids would make the harness prove a
  system with its custody check off, and would hand any caller a bypass convention.
  **THE CLASSIFIER CHANGED, AND THAT IS THE PART TO READ TWICE.** `write_rule.py` rule 3a
  used to trigger on `author == "household"` — **the classifier derived SCOPE FROM AUTHOR**,
  which is what Bill's clause forbids, and it was the only route by which D3/D10/D11 reached
  household scope. Correcting their author silently reclassified all three to
  member-private. Rule 3a now also triggers on `subj == "household"`, **strictly additive**,
  with 9 fault twins pinning it. **This was HA-19's one judgement call — Bill's item 2 said
  "subject and audience rules unchanged" AND "these remain household facts", and those two
  contradict each other in code; the outcome was taken as the ruling. Reversible in one
  commit if that reading is wrong.**
  **TWO SHARP EDGES FOUND, NEITHER FIXED, BOTH OUT OF SCOPE — do not rediscover them:**
  **(1) `encode()` accepts an unrecognized `write_state`, writes NOTHING to the graph, and
  still emits a success audit record and a fresh `fact_id`** (the lifecycle block has no
  `else`; valid states are `supersede`/`augment`/`correct`/`unresolved` — `"new"` is not
  one). Two lines in `logs/memory_engine/encode_audit.jsonl` claim writes that do not exist.
  **(2) No `author` property is persisted on the Fact node** — provenance is validated at
  write time and then unretrievable; "who said this?" is enforced but unanswerable.
  RUNS: batteries **850 passed**, L7 27/27, L7V2 27/28, AUDIT 8/8, **RATCHET PASS**, memory
  **13/17 inside the pin** (was 8/17 before the enrolment fix). **The one red,
  `test_zzz_no_fixture_keys_survive_the_suite`, is PRE-EXISTING and CROSS-PROCESS** —
  reproduced identically with every HA-19 change stashed; after a sweep the batteries are
  850/0. **NEXT, AND EXPLICITLY HA-20:** relocate that zero-orphan invariant and wire
  teardown into P4 quorum, PSA1, SC1, OB4.
  See `docs/dispatches/DISPATCH_HA19_GUARDS_LANDED__author-validity-enforced-scope-rule-corrected-census-clean__v20260807_1449.md`.

- **Roadmap lane — LANDED EARLIER: HA-18** (**CODE — one line of fixture; REQ amended**) —
  **D8 IS FIXED AND DECRYPTS.** `scripts/demo_seed.py` now authors D8 as `SAM_ID` instead of
  the literal scope marker `"household"`, which HA-16 identified as the actual defect. The
  re-derived row is `visibility=member-private`, `owner=sam`, **same key-holder = True**, and
  **its `derived_from=D4,D5` lineage survived the correction** — the fix is a re-derivation
  through the seed, not a relabel.
  **BUT `--full` IS STILL BLOCKED, AND THE REASON HAS CHANGED — read this before planning
  any dispatch that needs item 12.** It is no longer "D8 is broken." It is that **the OLD
  broken D8 row is still active on the graph beside the fixed one**: the seed treats a
  different `owner` as a different fact, so the legacy `owner=household` row was never
  superseded. Decrypt census is **16 OK / 1 FAIL of 17**, and the single FAIL is that stale
  row. **Clearing it is graph surgery — destructive, not pre-authorized, needs Bill.**
  **TWO GUARDS ARE BUILT AND PROVEN BOTH DIRECTIONS BUT DELIBERATELY NOT LANDED**, their
  code preserved in HA-18's session scratchpad and reproducible from the dispatch doc: a
  LOCAL `(visibility, owner)` structural assertion in `WriteClass.__post_init__` that never
  consults enrollment, and an AUTHOR VALIDITY check at `partition_crypto.classify_write` —
  the canonical pre-seal boundary — by **positive membership against the enrollment
  registry, not a blacklist**, failing closed.
  **WHY THEY DID NOT LAND, AND WHAT THE NEXT DISPATCH MUST NOT DO:** they refuse **D3, D7,
  D10, D11**, four fixtures that also author as `"household"` and, unlike D8, have **no
  declared provenance whatsoever** — no lineage entry, no derivation, no comment naming an
  originating author. With the guard active the seed refuses D3 first and never reaches D8,
  so the graph cannot be seeded at all. **Do not invent authors for those four to make the
  guards land.** That is the ruling HA-18 stopped for.
  `REQ_DERIVED_WRITE_CUSTODY` is **amended and still NOT MET**: §1A carries Bill's AUTHOR
  VALIDITY clause verbatim, C7 adds the negative twin with its proof obligation (no
  ciphertext, no node, refusal recorded), §6 items 4-5 record the two blockers.
  **NEEDS BILL:** (1) who authors a household-attribute fact; (2) supersede or delete the one
  legacy D8 row. **NOT DONE, carried to HA-19:** the zero-orphan invariant relocation and the
  four teardown wirings (P4 quorum, PSA1, SC1, OB4).
  See `docs/dispatches/DISPATCH_HA18_CUSTODY_BUILD_EXECUTED__d8-fixed-guards-proven-four-fixtures-block-landing__v20260807_1351.md`.

  > **STALENESS NOTED RATHER THAN QUIETLY PAPERED OVER:** the block below claims LAST LANDED
  > HA-08, but **HA-09 through HA-17 landed without updating CURRENT STATE** — including
  > HA-13's backup exclusions and HA-14's 1,390-key sweep, both of which changed the machine.
  > Those dispatches' own docs and INDEX rows are complete; the live handoff is what they
  > skipped. Their entries are NOT backfilled here by this dispatch — reconstructing another
  > session's state claim from its report is exactly the drift this document exists to
  > prevent — but the gap is recorded so a reader does not mistake HA-08 for the last work.
  > The dispatch ledger in `docs/INDEX.md` covers HA-01 through HA-18 without gaps.

- **Roadmap lane — LANDED EARLIER: HA-08** (**CODE**) — REQ_OFFER_MECHANISM **§12 step 5**:
  the spend machine is now DURABLE. `harness/spend_ledger.py`, append-only fsynced JSONL in
  `logs/offer_control_plane/` — **not the household graph (R20)**, enforced by an AST test.
  A situation is **SPENT FROM PRESENTATION** (R8's first sentence), no terminal state clears
  it, no edge back to ELIGIBLE, and **a refused re-presentation is itself recorded**.
  **THE RESTART PROOF IS A REAL PROCESS KILL** — one subprocess presents and exits, a second
  interpreter replays the file and is refused. HA-06's in-process dict would pass a
  same-process test and fail this one; that is the whole difference step 5 makes. 18/18.
  **READ THIS BEFORE PLANNING ANY DISPATCH THAT NEEDS ITEM 12: `--full` NOW RUNS PAST THE
  MEMORY GUARD AND ABORTS AT LAYER 2** — `FIXTURE DRIFT: D8 decryption returned None
  (household,dad,risk_pattern)`. **Item 12 is NOT satisfiable by any dispatch until this
  clears (TD-R-171).** The guard's refusal had been MASKING it: fixing the metric did not
  just enable `--full`, it uncovered the blocker underneath. **Not this session's doing** —
  the row is household-sealed with `sensitivity='high'`, so it is an unwrappable household
  key rather than D-R-196's change; `household.seal.key` untouched since 2026-08-05. **NOT
  bisected** — that is its own dispatch.
  **Item 4's guard-metric port was ALREADY on roadmap** (D-D-161/TD-R-166) — nothing to
  port; measured side by side today, `memory_pressure` 12.16GB free vs `vm_stat` 0.06GB.
  **THE ALERT NOW REFUSES RATHER THAN RINGING BLIND (TD-R-170 closed by Bill's ruling).**
  `scripts/dispatch_done.sh` checks mute FIRST: muted → exit 4, state unreadable → exit 5,
  both refusing to attempt playback; unmuted → exit 0, **which now means only that the
  playback command completed, NOT that anyone heard it.** The script never modifies volume
  or mute state.
  Runs: battery **812 passed + 1 skipped** = 795/9 + 18 (the skip is a pre-existing
  conditional in `test_record_graded_refusal.py`, not from this dispatch), L7 27/27, L7V2
  27/28, AUDIT 8/8, **RATCHET PASS**; memory harness 13/17, same four failures, inside the
  pin.
  **TD-R-172: every fixture-writing battery — including the memory harness itself — leaks a
  per-owner `*.seal.key` into `~/hip-keys/` and never removes it.** 18 today. **Deliberately
  NOT cleaned up: "key destruction" is on CLAUDE.md's NOT-pre-authorized list**, so those 18
  files wait on Bill's word. Fixtures only; nothing presents, nothing enabled. Nothing MET.
  See `docs/dispatches/DISPATCH_DURABLE_SPEND__spent-survives-restart-full-unmasked-a-blocker-mute-guard-built__v20260806_1845.md`.
- **Roadmap lane — LAST LANDED: HA-06** (**CODE**) — REQ_OFFER_MECHANISM **§12 step 3**:
  immutable offer instances. `harness/offer_instance.py` holds `AuthorityDelta` (§2.4's
  nine dimensions; **empty means NO CHANGE to that dimension**, per §2.4's own sentence),
  `FixedTemplate`, `SlotType` (closed set of five, **each member carrying its own validator
  so the type IS the registry**), `OfferInstance` (R11's fifteen fields, frozen) and ONE
  renderer. HA-03's `Situation` is imported and its id re-derived — not rebuilt.
  **HOW R18 IS ENFORCED — read this before extending it.** Comparing rendered prose against
  a scope object is not possible; a check shaped that way degenerates into asserting a
  string contains some words, which any reworded pitch also satisfies. Instead **the text is
  a PURE FUNCTION of template + slots + delta**, the delta is an INPUT to `render`, and
  `validate_instance` **re-renders** and compares to `rendered_text_hash`. One assertion
  catches an edited slot, delta, template body or text. **Frozen-ness is NOT the guarantee**
  — `object.__setattr__` and `dataclasses.replace` both walk past it; both routes are proven
  closed by the integrity hashes.
  36/36 tests. The structural no-generative-surface scans (AST, not substring) were **shown
  RED on command** — injecting `import random` and a `variant` parameter each turned the
  right check red — and the module was restored byte-for-byte before commit.
  **HA-03's manifest check was shown CATCHING this dispatch's own new battery** before it
  was registered. The hazard HA-01 and HA-02 each filed is demonstrably closed on the first
  new battery to arrive after it.
  Runs: battery **795/9 = 759/9 + exactly 36**, L7 27/27, L7V2 27/28, AUDIT 8/8, **RATCHET
  PASS**; memory harness 13/17, same four failures, inside the pin. **`--full` NOT run; item
  12 NOT satisfied.**
  **WHAT IS ONLY HALF-BUILT, and it matters for step 5: only "one instance per situation"
  at CREATION is enforced. R8's presentation-time spend machine — spent on presentation and
  staying spent through acceptance, decline, lapse, invalidation, restart and replay — is
  §12 step 5 and is NOT started.** The registry is in-process, so even the creation
  guarantee does not survive a restart (same posture as `offer_gate`). No reviewed-template
  registry exists; templates are validated structurally only. Fixtures only; nothing
  presents, initiates, or is enabled. Nothing MET. See
  `docs/dispatches/DISPATCH_OFFER_INSTANCE__immutable-binding-text-to-effect-identity-and-no-generative-path__v20260806_1810.md`.
- **Roadmap lane — LAST LANDED: HA-05** (**DOCS ONLY — REQ amendment; NO CODE CHANGED**),
  enacting Bill's second 2026-08-06 ruling and **closing the item HA-04 flagged and left**.
  In `REQ_RECORD_GRADED_REFUSAL`, `guard_kind` → **`guard.kind`** everywhere the REQ names
  the RECORD FIELD: acceptance row 1, the framing paragraph, the reader note, and §6 rows
  1–2. §6 row 2 is now **literal record dicts**; row 1's fault twin is "no `guard` block"
  rather than "`guard_kind` null", which is what a hedge record actually looks like.
  **THE REPLACE WAS NOT MECHANICAL — carry this if you touch that REQ.** `guard_kind`
  appears in TWO senses: the record field (changed) and **the emitter's PARAMETER, which
  really is named `guard_kind`** (left alone — the WHAT'S ALREADY DONE table row recording
  it as NOT EMITTED is the authority the whole correction rests on, and rewriting it would
  delete the explanation). Every remaining occurrence was audited by hand; **none now tells
  a reader to read `guard_kind` off a record.** Bill's original acceptance-row text is
  preserved verbatim beneath the changed row.
  **BUILDABILITY PROVEN BY EXECUTION:** the five fixtures were parsed straight out of the
  REQ's own §6 code block and checked against `logs/turns_demo.jsonl` — every key exists on
  a real record, the prescribed predicate gives **[T,T,T,F,F]**, the three fixture kinds
  equal the live kinds by set equality, and **no top-level `guard_kind` exists on any of
  119 live records**. Fresh evidence (119 records, 9 guarded: `access_control` 2,
  `empty_set` 5, `attr_empty_set` 2) independently re-confirms HA-04's three-kinds ruling
  against today's log rather than the REQ's 2026-08-02 figure.
  **KNOWN GAP, named with its cost: no standing test was added**, so nothing re-runs that
  proof automatically and a future §6 edit could reintroduce an unbuildable fixture
  silently. The check that would end this — assert the REQ's own fixture block parses and
  matches a live record — is named in the dispatch and NOT built.
  No harness runs (docs-only, none asked for). Nothing MET. See
  `docs/dispatches/DISPATCH_GRADED_REFUSAL_FIELD_PATH__guard-kind-becomes-guard-dot-kind-and-the-fixture-is-buildable__v20260806_1720.md`.
- **Roadmap lane — LAST LANDED: HA-04** (**DOCS ONLY — REQ amendment; NO CODE CHANGED**),
  enacting Bill's 2026-08-06 ruling. `REQ_RECORD_GRADED_REFUSAL` §6 item 2's ground-truth
  fixture said `guard_kind="access_control"`; it now requires **three fixtures, one per
  guard kind** — `access_control`, `empty_set`, `attr_empty_set`. **The REQ was wrong
  about the system; the system was right.** All three kinds are emitted by shipped code
  (`realtime_adapter.py:369,428` / `voice_orch.py:3162`; `injection_contract.py:806` for
  INJ-6; `injection_contract.py:849` for **INJ-6b**, whose own comment is the authority
  Bill cited). The REQ's own WHAT'S ALREADY DONE section — verified against 43 live
  records — already recorded all three, so §6 contradicted the REQ's own evidence.
  Amended IN PLACE with the prior wording preserved verbatim inside the annotation.
  **CARRY THIS INTO ANY WORK ON THAT REQ: a second inconsistency in the SAME clause is
  flagged and NOT fixed.** §6 still writes the field as `guard_kind`, which that REQ's own
  table records as **NOT EMITTED (0 of 43 records)** — the kind lives nested at
  `guard.kind`. **A fixture built from §6 as it stands will still use a key the record
  does not carry.** Left alone deliberately: the ruling was about the three kinds.
  No harness runs — docs-only, no code touched, none asked for. Nothing MET; no acceptance
  row re-tiered. See
  `docs/dispatches/DISPATCH_GRADED_REFUSAL_THREE_GUARD_KINDS__req-corrected-against-the-system-not-the-reverse__v20260806_1713.md`.
- **Roadmap lane — LAST LANDED: HA-03** (**CODE**) — REQ_OFFER_MECHANISM **§12 step 2**:
  canonical situation identity. `harness/material_change.py` holds `MaterialChangeKind`
  (exactly four, closed like `InitiationClass`, string form refused) and a
  `situation_id` that is **SHA-256 over five components and nothing else** — scheme tag,
  kind, principal, source_authority, event_ref, sorted material_state, every string
  `strip().casefold()`d. That normalization is what makes R6's "semantically equivalent
  resubmission" resolve to one situation.
  **§2.3's prohibition is STRUCTURAL, not a convention:** `RegisteredEvent` has NO field
  for model wording, prompt text, session identity or operator label, so there is nothing
  to pass — and `material_state` refuses those keys plus every R5 non-trigger, because a
  dict is otherwise the back door. `NON_TRIGGERS` **imports** R23's `NOT_A_TRIGGER` as a
  union rather than copying it.
  **`present_offer` NOW REQUIRES a `Situation`** — a bare id string is refused, and a
  forged one is refused by re-deriving the id from the situation's own fields. 16 call
  sites migrated; that battery is unchanged at 59 passed / 2 xfailed.
  **KNOW THIS BEFORE BUILDING §12 STEP 5: `situation_id` is required and recorded but is
  DELIBERATELY NOT in R24's dedup key.** Spending the situation is R8's job. A test pins
  the current behaviour, so a re-key must change that test on purpose.
  **THE SILENT-SKIP HAZARD IS CLOSED.** `eval/test_battery_manifest.py` is listed and
  **self-anchoring** (it asserts it is itself in the list), and it fails in BOTH
  directions: a battery file that exists unlisted, and a listed file that collects
  nothing. Both proven by execution and reverted. Seven exemptions, each with a stated
  reason, each asserted still earned. **HA-01 and HA-02 both filed this hazard instead of
  fixing it; it is fixed.**
  Runs: battery **759/9 = 713/9 + exactly 46**, L7 27/27, L7V2 27/28, AUDIT 8/8, **RATCHET
  PASS**; memory harness 13/17, same four failures, inside the pin. **`--full` NOT run;
  item 12 NOT satisfied.**
  **TWO LIMITS THAT MATTER FOR THE NEXT STEP.** (1) **R24's own text says a material
  change "MAY INCLUDE" the four — an ILLUSTRATIVE list — while RULING 2 treats them as
  closed.** The closed reading is implemented, per the REQ and the dispatch, but closing
  an open list is a ruling and is flagged rather than made silently. (2) **None of the four
  kinds has a real registry behind it** — no care-function toggle, no structured
  care-plan event, no legal-role feed, no validated sensing contract. `source_authority`
  and `event_ref` are structurally validated non-empty strings. **This layer gives a
  canonical identity to an event a registry would emit; it does not prove any such event
  has ever been emitted.** Fixtures only; nothing initiates, nothing is offered, nothing
  enabled. Nothing MET. See
  `docs/dispatches/DISPATCH_SITUATION_IDENTITY__four-kinds-canonical-id-and-the-manifest-check__v20260806_1644.md`.
- **Roadmap lane — LAST LANDED: HA-02** (**CODE + REQ amendment**), enacting two of Bill's
  2026-08-06 rulings. **HA-01's OPEN ITEM IS CLOSED.** The frontier consent prompt is
  **turn-bound consent inside a member-initiated exchange — a REPLY, outside the initiation
  taxonomy by R1's own definition**, belonging to the member-initiated grant-confirmation
  path. That is the third reading HA-01 named and declined to take alone. One line added to
  §2.2's not-an-offer list — *"turn-bound disclosure consent within a member-initiated
  exchange"* — in a **NEW REQ version `v20260806_1625`**; `v20260806_1320` is retained with
  **its body untouched**, so it still stands as the byte-identical copy of Bill's revision,
  which is the property D-R-195 filed it for. Verified by diffing the new body against
  Bill's original source: **one added line, nothing else.**
  **THE PROMPT'S BEHAVIOUR IS UNCHANGED and `harness/initiation.py` was not touched** —
  because the ruling puts the site OUTSIDE the taxonomy, there was no fourth class to add
  and none was added.
  **STILL OPEN AND NAMED: the grant-confirmation path the prompt now belongs to is named in
  Ruling 1 and BUILT NOWHERE.** The ruling classifies site 7; it does not govern it. That is
  a later step of §12.
  **D-R-196's 23 fault twins now run on every battery.** `eval/test_sensitivity_no_default.py`
  was a standalone script that pytest would have collected **ZERO** from — listing it as-is
  would have made the battery look complete while running nothing. Converted to per-case
  tests and registered. All 23 cases unchanged; the four sites whose fault twin and
  anti-vacuity read the SAME live call keep that property via a shared fixture. **The file
  collects 24 items = 23 cases + 1 guard**, stated rather than rounded. Battery **713/9 =
  689/9 + exactly 24**; RATCHET PASS; memory harness 13/17, same four failures, inside the
  pin. `--full` NOT run; item 12 NOT satisfied.
  **THE BATTERY LIST IS STILL MANUAL** — HA-01 filed the hazard, HA-02 added a second file
  to it and did NOT fix the mechanism. A new battery still runs only when someone remembers
  to name it in `scripts/run_harness.sh`, and the failure is silent. Nothing MET. See
  `docs/dispatches/DISPATCH_TURN_BOUND_CONSENT_AND_BATTERY_REGISTRATION__ha01-stop-ruled-and-23-cases-made-collectable__v20260806_1628.md`.
- **DISPATCH SERIES ON THIS LANE: `HA-nn` (HIP Advisor).** The predecessor `D-R-nnn`
  series is **CLOSED and ended at `D-R-196`**. Registered in `CLAUDE.md` STANDARD PREAMBLE
  item 10. A SERIES change, not a lane change — checkout, branch and `TD-R-nnn` unchanged,
  and **no existing `D-R-nnn` ID is renumbered or retired**.
- **Roadmap lane (governance/docs, this document's subject):** Last landed: **HA-01**
  (**CODE**) — **REQ_OFFER_MECHANISM §12 step 1 only: the closed initiation taxonomy.**
  `harness/initiation.py` holds `InitiationClass` (exactly three members —
  `AUTHORIZED_OPERATION`, `SAFETY_INTERRUPT`, `OFFER`) and `emit_or_suppress()`. **The
  closed set is enforced at the API: the STRING `"offer"` is suppressed exactly as `None`
  is**, so the taxonomy cannot widen by typo at a call site. Wired at the one real
  text-path egress (`orchestrator.handle_turn` step 4), declaring `AUTHORIZED_OPERATION`
  and returning the reply byte-for-byte. **NOTHING HIP SAYS TODAY CHANGED.**
  **THE SURVEY'S LOAD-BEARING RESULT, and the thing to know before building step 2: HIP
  HAS NO SYSTEM-INITIATED SPEECH TODAY.** All 11 speech egresses are reply-driven;
  `offer_gate.present_offer` is the only system-initiation API and has no production
  caller. So A1 holds today without changing an utterance — the taxonomy is in place
  BEFORE the thing it governs exists, which is the right order but means its evidence is
  necessarily thin.
  **ONE LIVE SITE IS UNCLASSIFIED AND NEEDS A RULING — this is the open item:**
  `_FRONTIER_CONFIRM_MSG` ("Answering it will send information off your home network.
  Confirm?"), emitted live from `server/voice_orch.py` via
  `control_flow.handle_frontier_request`. `AUTHORIZED_OPERATION` would let operational
  speech carry a request for new authority, which **R3 forbids by name**; `OFFER`
  contradicts §2.2's "confirmation of a member-initiated request" and drags in R4's
  trigger registry, whose four material-change kinds have no usable representation — which
  would make a live prompt un-renderable. A third reading (outside R1's scope, since the
  member initiated) is coherent and was **deliberately not taken unilaterally**, because
  R1's scope boundary is itself what is in question. Nothing classified for it; nothing
  about it changed.
  17/17 fault-twin + anti-vacuity cases pass; battery **689/9 = 672/9 + exactly 17**;
  RATCHET PASS; memory harness 13/17, same four failures, inside the pin. **`--full` NOT
  run; item 12 NOT satisfied.**
  **STANDING HAZARD WORTH CARRYING:** the standing battery in `scripts/run_harness.sh` is
  an **explicit file list**, so a new battery does not run until it is named — the first
  `--layer 7` run here reported 672/9 with the 17 new tests silently un-run. Registered and
  re-run. **D-R-196's own 23-case battery (`eval/test_sensitivity_no_default.py`) is STILL
  unregistered and cannot simply be listed** — it is a standalone script, so pytest would
  collect zero from it and it would look registered while running nothing. Its fault twins
  run only by hand today. Nothing MET; nothing ruled. See
  `docs/dispatches/DISPATCH_INITIATION_TAXONOMY__closed-three-class-set-and-one-site-that-needs-a-ruling__v20260806_1525.md`.
  Immediately prior: **D-R-196**
  (**CODE**) — **THE SENSITIVITY DEFAULTS ARE GONE FROM THE SEVEN NAMED SITES.** Bill's
  2026-08-06 ruling enacted: a fact with no sensitivity label is REFUSED, never stamped
  `medium`. `memory_engine.store.encode()` has **no `sensitivity` default** — omission is a
  `TypeError` at the call, and `None`/`""`/unrecognized raise before any transaction opens;
  `extraction_queue`'s MISSING branch now refuses the fact exactly as its already-hardened
  UNRECOGNIZED sibling three lines above does; the five `row["sensitivity"] or "medium"`
  read-layer idioms (`recall.py`, `api.py`, `extraction_queue` ×2, `memory_dashboard.py`)
  exclude the row and log it. One refusal helper — `harness.sensitivity.require` +
  `MissingSensitivity` (a SUBCLASS of `UnknownSensitivity`, so existing handlers keep
  working). **No new vocabulary, ordering, or level:** the registry has refused since D-75
  and the seven were bypasses of it, not a missing mechanism.
  **BLAST RADIUS, surveyed by AST not grep** (`str.encode()` is textually identical): 60
  `encode()` call sites, 41 already passed a label, and **all 19 that did not were in
  `eval/memory_harness.py` — no production caller relied on the default.** All 19 now state
  `medium`, the exact value the removed default supplied.
  **23/23 fault-twin + anti-vacuity cases pass** (`eval/test_sensitivity_no_default.py`);
  "nothing persisted" is proven by a graph fact-count before and after each refused write.
  Runs: standing battery **672/9 unchanged**, L7 27/27, L7V2 27/28, AUDIT 8/8, **RATCHET
  PASS**; memory harness **13/17 and PROVEN NEUTRAL — a pristine-code control run gave the
  identical 13/17 with the same four failures**. **`--full` NOT run; item 12 NOT satisfied.**
  **READ THIS BEFORE CLAIMING THE GREP IS CLEAN:** C1 is met for the seven and **NOT met
  repo-wide**. 15 matches remain — 11 are Bill's carved-out LOW turn-level defaults in
  `voice_orch.py` (count verified as exactly 11), one is `control_flow.py:166` in the same
  family, one now flows into the refusal branch, one is a benchmark script, and **one is a
  genuine EIGHTH site, `harness/zep_store.py`, still defaulting to `medium` and NOT fixed.**
  **`TD-D-148` was NOT edited from this lane** — demo-branch ID in a demo-branch register,
  still worded OPEN there; roadmap's record is **TD-R-169** (`DEBT_REGISTER__v20260806_1407.md`,
  LATEST repointed). Closing TD-D-148 is the demo lane's act, and it is a decision waiting on
  Bill, not an omission. **The one interpretive call is flagged in the REQ (§2), not buried:**
  read boundaries EXCLUDE the row rather than raise. Nothing MET; nothing ruled. See
  `docs/dispatches/DISPATCH_SENSITIVITY_NO_DEFAULT__seven-substitution-sites-refuse__v20260806_1408.md`.
  Also landed between D-R-195 and this dispatch, by the demo lane working on `roadmap`:
  **D-D-161** (`a32ddaa`) — TD-129's `--full` memory guard was measuring `vm_stat`'s raw
  `Pages free`; metric ported from `f07a630`, 2GB floor unchanged, TD-R-166/167 RESOLVED and
  TD-R-168 filed. It did not update this block; D-R-196 is bringing it current, not claiming
  D-D-161 was registered here.
  Immediately prior: **D-R-195**
  (Lane B worktree, **DOCS ONLY — no code, no graph, no harness, nothing ruled**) —
  **`REQ_OFFER_MECHANISM` is now IN THE RECORD**, filed VERBATIM from Bill's revision at
  `docs/requirements/REQ_OFFER_MECHANISM__governed-initiation-of-new-authority__v20260806_1320.md`:
  the body was copied, not retyped and not summarised, and every line from the first `---`
  onward is byte-identical to the source (`diff` clean, body SHA-256 `3bb8dc3a…` both sides).
  Only the header block differs — Status replaced, `Reconciled-Against` added, and the prior
  header wording quoted inside the new one rather than discarded. It governs the sole
  system-initiated path to authority HIP does not already hold: three initiation classes and
  no fourth, the trigger registry as the only eligibility source (its four material-change
  kinds imported UNCHANGED), one situation → one minimal pre-approved delta spent on first
  delivery, template and delta bound as one immutable versioned object with no generative or
  A/B surface, and a decline held as control state that may never become a fact about the
  member. **Status DRAFT-RATIFIED-PENDING — a real state, not a soft MET:** the text is
  Bill's, but FORMAL RATIFICATION IS THE FUTURE D-R THAT LANDS STEP 1 of the REQ's own
  LANDING ORDER (§12), not this filing. **A1–A20 UNATTEMPTED** (all twenty at ABSOLUTE tier).
  Registered in `docs/INDEX.md` under `requirements/` and in MANIFEST Section B; symlink
  `LATEST_REQ_OFFER_MECHANISM.md` created. **`REQ_STRUCTURAL_CEILING` IS UNTOUCHED** — its
  solicitation section still stands as written; the new REQ's `Supersedes:` header records
  the intent only, and its §12 step 9 orders that swap ONLY after A1–A20 run. **What is NOT
  true yet:** no offer mechanism exists in code, no trigger-registry binding was checked
  against the four change kinds the REQ imports, and nothing in this dispatch verified that
  the REQ is consistent with what is built.
  Immediately prior: **D-R-194**
  (**CODE**) — Bill's two 2026-08-05 rulings enacted. **Ruling (d) is TWO-STEP** and is
  recorded in `REQ_ERASURE_REQUEST_PATH` §(d) with the superseded UNDETERMINED text
  struck through rather than deleted. Built: `begin_fact_erasure` authorizes and
  returns a pending token and **never calls the erasure mechanism**;
  `confirm_fact_erasure` is the second authenticated act and executes. The same route
  serves both steps (no `token` = request, `token` = confirm), **each with its own
  body-bound signature**, and the pending store lives in the DECIDER so D-R-192's
  one-door-one-decider still holds. Unconfirmed requests erase nothing — proven, spy
  at zero — as are mismatched, expired, unknown and replayed confirmations, with an
  anti-vacuity control proving the correct two-step still fires exactly once.
  **F1 IS FIXED, NOT PINNED.** Env loading is now explicit in `load_process_env()`
  called from `main()`, so **importing `server/demo_dashboard.py` no longer changes
  which database the process points at**; the home `~/.env.dev` may never set a graph
  target; and the `NEO4J_URI`/`NEO4J_USER` module constants that would have re-created
  the bug are now resolved lazily. Proven in a clean process with both semantics side
  by side — **old flips 7688 → 7689 (the frozen demo), new holds at 7688**. The
  D-R-192 pin test is inverted to assert the hazard's absence.
  Question **(b) remains UNDETERMINED and refused by default**, untouched. Scope
  unchanged: route still OFF unless `HIP_ERASURE_ROUTE_ENABLED`, fixtures only, zero
  leftovers verified. Runs: **672/9 = baseline 664/9 + exactly the 8 net added
  tests**, every layer identical, RATCHET PASS; memory 13/17 on the pinned set.
  **`--full` REFUSED by TD-129 for the third dispatch running — item 12 NOT
  satisfied.** Not audited: whether other modules share the same import-time env
  pattern. Nothing MET. See
  `docs/dispatches/DISPATCH_TWO_STEP_ERASURE_AND_F1__pending-confirmation-built-import-no-longer-repoints-the-graph__v20260806_1120.md`.
  Immediately prior: **D-R-192**
  (**CODE**) — erasure is no longer unreachable. Built **ONE** route,
  `POST /api/erasure/fact` in `server/demo_dashboard.py`: an authenticated member
  requests erasure of a fact they own. Authenticated by a **body-bound Ed25519
  signature with NO self-signing fallback** (the dashboard box holds every member's
  key, so allowing the fallback would let any token-holder erase anyone's facts — that
  is the second fault twin, not a convenience). The route holds **zero authorization
  logic** and hands the decision to `harness.erasure_request`; a test greps its source
  and fails if ownership logic ever appears. Only `request_fact_erasure` is wired —
  owner-wide erasure is reached by nothing, and the two UNDETERMINED questions
  (cross-person authority; one-step vs two-step) are answered in neither direction.
  **OFF unless `HIP_ERASURE_ROUTE_ENABLED` is set**; fixtures only; zero leftovers
  confirmed by direct query. **Both fault twins proven by execution** with a
  call-counting spy over `erase_fact` still at zero, plus an anti-vacuity control
  proving the spy fires when authorized.
  **FOUND AND NOT FIXED — read this before enabling anything:** `server/demo_dashboard.py:61`
  runs `_load_env_file(~/.env.dev, override=True)` **at import time**, and `~/.env.dev`
  pins `NEO4J_URI=7689` — **the FROZEN DEMO's graph**. Importing the module that now
  hosts the erasure route re-points the process off this checkout's pinned 7688.
  `harness/graph_target.py` refused, so nothing was written, but **that guard is the
  only thing standing there**, and it protects only the first URI resolution in a
  process (the driver is memoised). Enabling the route in a dashboard process without
  fixing this first would put the erasure path in front of the frozen demo's graph.
  Runs: **664 passed / 9 xfailed = baseline 652/9 + exactly the 12 added tests**, every
  layer identical, RATCHET PASS; memory harness 13/17 on the pinned set. **`--full`
  REFUSED by TD-129's memory guard — item 12 NOT satisfied.** Nothing MET. See
  `docs/dispatches/DISPATCH_ERASURE_ROUTE__one-authenticated-owner-scoped-route-off-by-default-fault-twins-proven__v20260805_1823.md`.
  Immediately prior: **D-R-191**
  (Lane B worktree, docs + one `docs/INDEX.md` header rename; **no code**) — three of Bill's
  rulings enacted into the existing records. **C9 RULED: PASSED ON THE LEAK GATE, 0 leaks vs
  6**, recorded in place in `REQ_DEMO_CUTOVER` per D-R-183's precedent, with the LIMIT written
  into the ruling text rather than appended as a caveat — the structural-refusal rate sat at
  26/350 across all three builds while leaks went 10 → 2 → 0, so **a build can clear this gate
  without refusing structurally once more**. The **structural-rate gate stays OPEN with its
  threshold UNSET** until `REQ_UNRESOLVED_SUBJECT_GUARD`'s fix lands. `REQ_DEMO_CUTOVER`'s
  `Status:` is still **NOT MET** — C9 is one of C1–C10. **TD-R-164 RESOLVED** (D-R-190's sweep
  re-verified independently here: `requirements/` = 65 rows, 0 pointing at a `dispatches/`
  file) with its own 13-column row repaired. **TD-R-165 RESOLVED** by rename — the WP/NDA
  package table is now `## deliverables-packages/`, the memo table keeps `## deliverables/`,
  and **all 19 `## ` headers in `docs/INDEX.md` are now distinct**. Two findings reported and
  deliberately NOT acted on (item 4 said rule nothing else): the mirror image of TD-R-164 — a
  REQ row sitting in the `dispatches/` table — and three older register rows carrying a stray
  unescaped pipe each. Nothing else ruled; nothing MET. See
  `docs/dispatches/DISPATCH_ENACT_THREE_RULINGS__c9-leak-gate-td164-resolved-deliverables-header-renamed__v20260805_1722.md`.
  Immediately prior: **D-R-189**
  (**CODE**, not docs-only) — question detection built on `roadmap` from Bill's three
  rulings, which were written into the REQ
  (`docs/requirements/REQ_QUESTION_IS_NOT_A_STATEMENT__one-vocabulary-decisive-and-not-overridable__v20260805_1645.md`)
  **before** any code, so this build is NOT retroactive — that flag belongs to D-R-188's
  version and to `30adeaf`. The four divergent question-word lists are now ONE 30-token
  vocabulary in `harness/question_words.py` (a dependency-free leaf), proven to be exactly
  their union with TD-119's and D-20's imperative openers intact; the single test is applied
  at all four sites **plus `confirmation_gate.py`**, and both duplicate lists are deleted.
  The fault twin on "Has she taken her medication?" passes **both directions** — and the
  fault-injected direction leaks, which is what makes the other direction proof.
  **A standing battery did move and it is not buried:** the first post-change run went
  L7V2 27/28 → 25/28 with RATCHET red, traced to `mutation_targets.py`'s hardcoded line
  numbers (the false red D-102's TD predicts in writing), proven harmless by a content-keyed
  32→32 survivor comparison made *before* anything was touched, resynced, re-run green —
  both runs reported. Final **652 passed / 9 xfailed = baseline 633/9 + exactly the 19 tests
  this build adds**, every layer identical to baseline, RATCHET PASS; memory harness 13/17 on
  the pinned {MEM-115,116,117,118}. **`eval.harness --full` REFUSED at TD-129's 2GB memory
  guard, so Requirements Discipline item 12 is NOT satisfied** — stated, not papered over.
  **THE TWO LANES NOW HOLD DIFFERENT IMPLEMENTATIONS OF THE SAME REQUIREMENT** (`roadmap`:
  one list, `confirmation_gate` wired, no INJ-1c; `demo-cutover-build`: two lists, no
  `confirmation_gate` fix, INJ-1c present) — reconciling them is UNRULED and was not in
  scope. Nothing MET; C9 not ruled. See
  `docs/dispatches/DISPATCH_QUESTION_ONE_VOCABULARY__consolidated-decisive-test-built-and-run__v20260805_1645.md`.
  Immediately prior: **D-R-188**
  (docs only, no code) — wrote the **retroactive REQ** for the question-detection fix that
  shipped at `30adeaf`,
  `docs/requirements/REQ_QUESTION_IS_NOT_A_STATEMENT__decisive-question-test-not-overridable__v20260805_1536.md`,
  **flagged as after-the-fact against Requirements Discipline item 8's own prohibition**, on
  Bill's explicit instruction and on the `REQ_atorvastatin-false-ack` (`c86a414`) precedent.
  **`30adeaf` IS ON `demo-cutover-build`, NOT `roadmap`** — this checkout contains no
  `is_question_utterance`, so every code citation in that REQ and its dispatch doc is read
  from the demo branch and says so. The commit *did* name a REQ
  (`REQ_UNRESOLVED_SUBJECT_GUARD…v20260804_2104`); the real gap is that that REQ governs an
  OUTCOME and never mentions `is_declarative`, question detection, or the SIO override — and
  it does not exist on the branch the code shipped on. All three questions D-R-188 posed are
  **UNDETERMINED, none blocking**, each with what would settle it. Survey found four
  question-word lists sharing only **5 of 27 tokens**, 13 consumer sites, and the two routes
  that bypass `apply_injection_contract` — `harness/realtime_adapter.py` (which got the fix)
  and `harness/confirmation_gate.py` (which did not). **Two measured gaps remain open in the
  shipped fix**: `has`/`have` fall through the decisive test, and a mid-text `?` yields
  opposite verdicts depending on whether the SIO is live. A TD for the list divergence is
  recommended and **not filed** (outside the pre-authorized TEST/TOOL class; item 3 said rule
  nothing). Nothing MET; C9 not ruled. See
  `docs/dispatches/DISPATCH_QUESTION_REQ_RETROFIT__four-lists-every-consumer-and-two-that-bypass__v20260805_1536.md`.
  Immediately prior: **D-R-184**
  (Lane B worktree, docs only) — Option A on the misfiled `docs/INDEX.md` rows: moved
  D-R-178's own row (flagged at D-R-179) from `requirements/`'s table to
  `dispatches/`'s own; filed **TD-R-164** for the other 54 (root cause: every category
  table in `docs/INDEX.md` shares an identical header, so an ambiguous anchor let
  `requirements/` — sitting immediately before `dispatches/` — absorb every misfiled
  row since D-90, the project's entire history); fixed `CLAUDE.md`'s Workflow item 3
  with an explicit anchor instruction so new rows land correctly from now on. The
  sweep for the other 54 is deferred to a future dispatch. See
  `docs/dispatches/DISPATCH_MISFILED_INDEX_ROWS__option-a-one-row-moved-td-filed-anchor-fixed__v20260805_1412.md`.
  Immediately prior: **D-R-183** — recorded Bill's 2026-08-05 ruling, **R2 MET, R8 MET,
  R10 MET**, in `REQ_STRUCTURAL_CEILING` §16 (closing the NOT MET column
  D-143/D-144/D-100 opened); filed **TD-R-163** (authorized standing check for new
  inference sites, same shape as the ledger call-site enumeration test, not built —
  needs a REQ); **re-tiered A10 LIVE with its predicate corrected in the same edit**
  (the A1/D-100 rule) — `_a10_enforced_at_creator` gained `representation`/`permit`
  probes reusing CEIL-A8's and CEIL-A2's own real-path shapes, both manually verified
  to refuse for the specific named reason. Full battery + `--layer 7` clean first run
  (RATCHET PASS); memory harness 13/17, same pinned set. See
  `docs/dispatches/DISPATCH_R2_R8_R10_MET__not-met-column-closes-a2-a10-live__v20260805_1401.md`.
  **Today's 2026-08-05 ceiling-ruling chain, compressed** (full detail in each own
  dispatch doc, not reconstructed here): D-R-174 (read-only, found the rule-3a
  asymmetry) → D-R-176 (`c1538d2`, fixed it) → D-R-178 (`62fd263`, R11 MET) → D-R-179
  (R16 MET, R17 MET, on D-R-173's `ad90444` evidence) → D-R-180 (read-only,
  re-verified R5/R6 HOLD BY ABSENCE unmonitored, R7 ENFORCED, against fresh HEAD) →
  D-R-183 (this entry). §16 today: MET now includes R1, R2, R8, R10, R11, R12, R16,
  R17, R18, R29, R30; NOT MET stays R2's old neighbors' downstream concerns resolved —
  see the REQ doc directly, this line is a pointer and may lag by the time it's read.
  **KNOWN GAP IN THIS BLOCK, STATED PLAINLY RATHER THAN PAPERED OVER:** the individual
  dispatches this lane landed between D-153 and D-R-176 (roughly D-154 through D-175 in
  this lane's own sequence) are NOT reconstructed here — this update only re-grounds
  CURRENT STATE in what is true NOW, per the live-handoff rule's own requirement not to
  describe a past state as current. For the granular record of that intervening span,
  read `docs/dispatches/` and `docs/techdebt/LATEST_DEBT.md` directly rather than
  trusting a chain summary here that this entry does not attempt to provide. Prior chain
  summary, as it read at D-153 (retained as history, not current): **D-151** (`e41d3a8`) the 2026-08-01
  evaluation-methodology review found ALREADY BANKED by another lane — nothing
  re-banked — plus TD-159 (A18/A29/A30 are a VISIBILITY gap, not a coverage gap) and
  TD-160 (dad/household unenrolled, leaving one R9 never-store category without a
  write-time check, for a DATA reason); **D-149** (`ca223d4`) the status board
  cross-checks its own LIVE claims against real runners, 6 of 9 verify; **D-148**
  (`50daa12`) the ceiling status board itself — `docs/status/CEILING_STATUS.html`, every
  status derived, none hardcoded; **D-146 build + B3** (`23b26d1`, `6750593`) kernel-enforced
  resource-keyed locking made a precondition of the harness runner, fail-closed graph
  targeting, and five dormant worktrees retired; **D-145** (`93eb91e`) A2/A8 written, run and
  re-tiered LIVE.
- **Ruling state, historical then current.** R2 and R8 were ruled NOT MET 2026-08-03
  (D-143 `3989ba2` — scope gap: R5/R6/R7 unaddressed; D-144 `317212a` — silent
  absorption), with R10 NOT MET as their downstream consequence. **All three reversed
  2026-08-05 (D-R-183)**, alongside R11 (D-R-178) and R16/R17 (D-R-179) the same day —
  so the §16 picture is now MET: R1, R2, R8, R10, R11, R12, R16, R17, R18, R29, R30; no
  requirement currently stands NOT MET. The status board renders this live and is the
  place to read it — this line is a pointer, not a second copy, and (per the same
  staleness this block just corrected in itself) may lag a landed ruling until it is
  next regenerated.
- **Lane A (build):** landed **R8's write-time representation classifier** (`bc56fc4`,
  D-140) and **D-147** (`ca34ec4`) — which closed the `.env.demo` tracked-config hazard this
  document named at D-146 and traced MEM-116/117/118 to ONE root cause (TD-151's fixture
  restore meeting P8's cross-principal trust-monotonicity gate; filed TD-158, nothing built,
  baseline untouched). Lane A was live on **D-152** during D-153.

- **Demo-cutover lane:** `~/hip-cutover-demo`, branch `demo-cutover-build`, Neo4j **7690**.
  Carries UNCOMMITTED work in the shared `~/hip-roadmap` checkout: four dispatch docs and
  four `docs/INDEX.md` rows, deliberately pending Bill's go-ahead since 2026-08-02. **Any
  lane committing in that checkout must stage around them** (see Process rules).
- **Frozen demo:** `~/hip-dev`, branch `demo-presenter-package`, Neo4j **7689** — the
  untouched fallback. Do not touch it.
- **Lock:** `.hip-lock` in `~/hip-roadmap` was held by session `claude-code-banking` (pid
  60474, "Index Bank 2 — file six findings on the register") at D-137's start. It is
  ADVISORY and unenforced — see TD-148.
- **Tech-debt register:** `DEBT_REGISTER__v20260803_1455.md` at D-137's read; the banking
  lane was filing further findings concurrently, so re-read `LATEST_DEBT.md` rather than
  trusting this line's version number.

---

## 1. THE CEILING REQ — per requirement, from §16 itself

`REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md` (filed D-70,
`98dfb7a`). **§16 is the sole authoritative record**; the preamble deliberately carries no
count (D-131 — five staleness flags in five weeks killed the count for good). Read §16, not
this table, when it matters; this table is a pointer with dates.

| R | §16 status | Note |
|---|---|---|
| R1 | **MET** (D-100, 2026-08-01) | satisfied by D-97's origin/registry work, probed live D-99 |
| R2 | **reported, not ruled** (D-130) | typed inference permit BUILT, enforced at `create_fact_node`; awaits Bill's ruling |
| R10 | **NOT MET** (D-100, 2026-08-01) | **the one ruled NOT MET** — see below |
| R12 | **MET** (D-103, 2026-08-02) | ruled in two stages: direction D-92, MET once the read-path fix (D-102) and A12's check landed |
| R18 | **MET** (D-113, 2026-08-02) | on the operative rule as AMENDED at D-111 (recompute clause removed); MET **with three absences recorded, not conditioned away** |
| R29 | **MET** (2026-08-01) | canonical sensitivity registry |
| R30 | **MET** (2026-08-01) | migration + fail-closed; backfill question ruled D-92 |
| all others | **FILED, acceptance NOT run** | a requirement without a §16 entry is not ruled |

**R10 is blocked behind R2 and R8, structurally — not by unfinished wiring on R10 itself.**
R10 requires `store.py::encode` to revalidate four things at the single materialization
point (`create_fact_node`, D-96). Two are enforced: **origin** (`validate_origin()`, D-97)
and **registry** (D-97). Two are not: **representation** — R8's representation classes do
not exist, which is why A8 is UNWRITABLE; and **permit** — R2's typed permit, which D-130
has now BUILT but which is not yet ruled. **A10 flips when A2 and A8 build**, not before.
The one `PERMIT` elsewhere in the codebase is INJ-3's read-side owner permit — a different
mechanism on the other side of the system; do not conflate them.

---

## 2. THE LANE STRUCTURE — three lanes, and why a fourth build lane is unsafe

**Today:** (A) the build lane, currently on R2/R8; (B) the demo-cutover lane
(`~/hip-cutover-demo`, 7690); (C) the governance lane (rulings, REQs, registers, docs) —
plus the frozen demo (`~/hip-dev`, 7689) which is a fallback, not a lane.

**Why another concurrent BUILD lane is unsafe until TD-148's lock exists.** The lock is
advisory with no enforcement, and it has failed in both directions already:

- **D-107 (2026-08-02) — write-through:** the demo-cutover lane wrote a REQ, a dispatch doc,
  and two INDEX rows into `~/hip-roadmap` **while the roadmap lane held the lock**.
- **D-118 (2026-08-03) — unread clobber:** a session took the lock with a bare `>` after a
  mere existence check and **destroyed another holder's fields unread**; that holder was
  never identified.
- **Standing since filing:** the `taken:` timestamp drifts hours from mtime, which is the
  likeliest reason two sessions can both believe they hold it (flagged three times before
  TD-148 folded it in).

The contended surfaces are not hypothetical: `docs/INDEX.md` (every lane appends rows), the
tech-debt register (versioned file + symlink), `eval/harness_baseline.json` (see TD-150),
the shared `~/hip-harness/registry.db` (rewritten mid-dispatch by unrelated activity at
D-110, now given the cutover lane its own copy), and the Neo4j ports 7687/7688/7689/7690.

**Updated after D-146 (build + B3 retirement) — the graph picture is materially different:**
`7688` now has **exactly one configured checkout** (`~/hip-roadmap`, additionally pinned by
`.hip-graph`), because the two others that carried committed `.env.dev` files pinning it —
`hip-roadmap-crypto-p2` and `hip-roadmap-stage1-wip` — were retired. That collision is gone
by SUBTRACTION, which is stronger than the serialisation the graph lock provides. Remaining
targets, verified from each lane's own config: `hip-roadmap`→7688, `hip-cutover-demo`→7690
(its launcher pins `CUTOVER_NEO4J_URI` and deliberately unsets any inherited `NEO4J_URI`),
`hip-dev`→7689, `hip-vo`→7689 via `.env.demo`. **One known sharing survives — `hip-vo` with
the frozen demo on 7689 — and it is the by-design case Bill excluded from scope.** Two
latent hazards remain named rather than fixed: `.env.demo` is a TRACKED file, so every
worktree carries a copy that would source the frozen demo's env if used in demo mode; and
`~/.env.dev` still pins 7689 with `override=True` (the `.hip-graph` pin is what now catches
that, for any checkout that opts in).
Two lanes are survivable with the discipline below because one of them is docs-only most of
the time. **A second concurrent BUILD lane multiplies the graph/baseline surface, which the
current mitigations do not cover.** TD-148 scopes the real fix: read-before-write, atomic
`O_EXCL`/noclobber creation, drift-proof liveness (holder PID + heartbeat mtime), and a
dead-holder supersession policy. It is UNGOVERNED — it needs a REQ before any build.

---

## 3. THE STANDING BASELINE — what "green" means here

**Memory harness: the pin is 13–15/17, and 15/17 is the CEILING, not a target.**
- **Two rows are permanently red for structural reasons, not defects in what they test.**
  **TD-145**: MEM-116's value verification decrypts via the retired v1 master-key helper
  (`eval/memory_harness.py:1664`) on a checkout where OB6 asserts that key's ABSENCE is
  correct — a structural false-red. **TD-146**: MEM-115(b)'s cross-owner cold-recall rows
  ARE fetched by the subject-scoped Cypher but are dropped at the caller-scoped decrypt
  (`recall.py:228-236`, REQ_CRYPTO_P2) **before** the injection contract runs, so
  `denied_count=0` is recorded faithfully with no contract denial to count. Both are
  crypto-era scenario staleness; both are scoped and deliberately not fixed.
- **Failures must be a subset of {MEM-115, MEM-116, MEM-117, MEM-118}.** MEM-117 flakes —
  it flipped red→green between two consecutive runs at D-127 — and belongs to the
  `fact_change` live-write family (TD-147's addendum).
- **16/17 is a STOP.** A pinned-failing scenario going green unexplained is evidence the
  baseline changed, not evidence of health. Do not celebrate it; investigate it.

**`--full` has a memory guard (TD-129). Its METRIC was broken until D-D-161 (2026-08-06);
the 2GB floor was never the problem.** The guard refuses below 2GB free ("the --full
killer": at low free memory the OS SIGKILLs the run mid-flight), and that policy is
correct and UNCHANGED. What was wrong is what it measured: it read `vm_stat`'s raw
`Pages free` counter, which is near-zero **by design** on modern macOS — the kernel holds
reclaimable pages in `inactive`/`speculative`/the compressor rather than leaving them
free, so on a healthy 32GB machine that counter reads under 1GB essentially always.

**Consequence, stated plainly: this guard produced FALSE REFUSALS, and the prior wording
of this section documented them as real.** Measured live at D-D-161 on the same machine
at the same instant: the old formula read **0.67GB → REFUSE**, while `memory_pressure`
read **14.72GB (46% of 32GB) → allow**. A ~22x understatement. **The two refusals this
section previously cited as evidence ("twice in one day at 1.96GB and 0.53GB") were
almost certainly both false**, as were the `--full` refusals recorded at lines 66, 95 and
131 above — those entries are HISTORY and stay as written, but they should be read as
probable measurement artifacts, not as evidence the machine was ever short of memory.

**FIXED** by porting `demo-cutover-build`'s `f07a630` to this lane (D-D-161, filed here as
**TD-R-166**; that commit's own comment cites "TD-145", which is TD-145 *on
demo-cutover-build*, NOT roadmap's TD-145). The guard now reads `memory_pressure`'s
"System-wide memory free percentage" against `sysctl hw.memsize`, and fails CLOSED if that
value cannot be read. The floor stays 2GB — the metric was fixed, the policy was not
weakened.

Genuine memory pressure is still possible and still worth checking before a long run: at
D-D-161 swap was 89% consumed (6.4GB of 7.2GB) with ~11.6GB of Ollama models resident in
unified memory. Freeing an IDLE ollama model plus a page-reclaim cycle remains the working
method when the guard refuses **on the corrected metric**. A jetsam kill mid-run looks like
a hang.

**One red is deliberately LOUD and must stay red (Bill, D-118).** `L6:record-invariants` —
a single G1 no-orphan-generation violation on the sam/atorvastatin smoke turn. Root cause
(D-119, correcting D-117's own filing): `fact_change` returns `changes:[]` **deterministically**
on the restatement-with-fact-present payload class; transport is exonerated. **The baseline
stays unupdated.** If it goes green, something changed — find out what.

**Layer shape at last full run (D-127):** AUDIT 8/8, DISC 1/1, L1 14/15, L2 25/35 (10 design
skips), L3 3/3, **L4 30/34** (4 design skips — PW016/PW018 skip on unimplemented
retract-without-successor), L6 0/1 (the loud red above), **L7 27/27**, L7V2 27/28 (one
opt-in skip: CT-OUTPUT-GAP needs `HIP_L7_LIVE_OUTPUT_TAINT=1`), SCHEMA 1/1, VOICE 1/1.
**22 standing pytest batteries run before the harness on every pass** (323 passed, 8 xfailed
at D-127). RATCHET PASS means no scenario regressed vs baseline — it does **not** mean
everything is green.

---

## 4. PROCESS RULES — each with the incident that produced it

Rules without their incident get re-litigated. These are in CLAUDE.md; this is why.

| Rule | The incident |
|---|---|
| **REQ first, no code without one named** (Requirements Discipline 8) | D-116 asked for the header rename and named no REQ; it was REFUSED at the gate, and D-117 re-issued it REQ-first. The REQ may not be written retroactively to cover work already done. |
| **An exit code is not an answer** — verification runs unchained (item 13) | `grep -c` exits non-zero when the count is 0. `grep -c … && … || echo "CONFIRMED"` printed a reassuring false all-clear three times: **D-70** (a `git add` silently skipped), **D-75**, **D-88** (an INDEX check aborted mid-chain while `0` was the correct answer). |
| **Full ratchet, not targeted proofs** (item 12) | Item 0, D-03/D-18 and TD-126's remediation each ran narrow live proofs that passed, then shipped a real regression apiece (D-20, D-22) that only `--full` caught. |
| **Lock read-first, then noclobber; report the holder** | D-107's write-through and D-118's unread clobber (TD-148). |
| **Commit AROUND foreign WIP: explicit pathspecs, surgical INDEX staging** | D-107: a parallel lane's uncommitted REQ/dispatch/INDEX rows sat in the shared checkout for days. The method: save the union copy, reset INDEX to HEAD, apply only your rows, `git add`, restore the union. |
| **Wrap-tolerant literal scans; a single-line grep can false-zero** | D-115's "seven sites" survey missed an EIGHTH — a literal wrapped across two adjacent source strings — the exact hazard D-116 had just named. D-117 found it with an AST + comment-joined scan. It has since bitten my own verification twice more. |
| **Never self-rule a REQ MET** | Standing. Sessions report readiness; Bill rules. Also: a passing acceptance row does not carry its requirement (A30 passes while R30's item 5 was unbuilt). |
| **Correct your own prior report when evidence contradicts it** | D-119 corrected D-117/D-118's filed mechanism for TD-147 (a ReadTimeout that had in fact recovered in-call) and withdrew a "turns_demo passed the same shape" claim that was a conflation. |
| **Baseline changes are governance records, not derived state** | `--update-baseline --accept` applied one justification to EVERY red row (D-126) and then dropped the whole `_accepted` map including an unrelated still-red row's text (D-127). Both caught only by reading the diff. TD-150, REQ filed. |
| **A count is a claim that ages; a pointer is not** | The ceiling preamble went stale five times — D-88, D-92, D-100, D-120, and D-129's own re-count. D-131 deleted the count. |
| **Reports route by size; never `open -e`** | Terminal copy and file-open both arrive blank for Bill. Dragging the file works — it is how the D-63 axes document and the REQ drafts moved (D-136). |

---

## 5. OPEN ITEMS, grouped by what actually blocks them

**Blocked on a BUILD (12 ceiling requirements):** R4, R5, R8, R10, R13, R17, R19, R21, R22,
R23, R24, R28. Of these, **R8 is the highest-leverage** — it and R2 together unblock R10,
the only ruled-NOT-MET requirement. R23/R24 are pure build with nothing upstream (Axis 5 is
wholly unbuilt). Five of the twelve need a schema or destructive-write authorization before
work starts (R4, R8, R13 schema; R17, R22 destructive/backup).

**Blocked on a FIXTURE (2):** R6 (a validated sensing contract — the highest fixture cost in
the plan; A6's minimum fixture is specified in REQ_CEILING_ACCEPTANCE) and R25 (the
adversarial prompt-mutation suite).

**Blocked on an OUTSIDE PERSON (3):** R3 (ethicist review before the prohibited-label
taxonomy can be enumerated), R9 (ethicist + explicit authorization to author sensitive-media
fixtures), R15 (ethicist + attorney sign-off, Part 4 ADVISORY tier).

**Blocked on a RULING (Bill only):**
- **R2** — built at D-130, reported not ruled.
- **TD-136** — household-owned facts about non-members reach every member unconditionally
  via INJ-4. Whether the household exemption should cross the network boundary is a product
  decision, open since 2026-07-22.
- The two REQs filed at D-129 need executing dispatches, not rulings:
  **REQ_ASKED_ATTRIBUTE_COVERAGE** (TD-149) and **REQ_BASELINE_RECORD_INTEGRITY** (TD-150).
- **TD-148** (the lock) has no REQ yet and is UNGOVERNED.

**Standing debt that is scoped and deliberately unfixed:** TD-142
(mutation harness hardcodes file:line), TD-145/TD-146 (the two permanent memory reds),
TD-147 (the loud L6 red).

**TD-129 (memory guard) is NO LONGER on that list.** Its POLICY was never debt — the 2GB
floor stands unchanged. Its METRIC was debt, was measured as such at D-D-161, and is
FIXED in this lane as of that dispatch (TD-R-166). See the `--full` memory-guard section
above. Listing TD-129 as "deliberately unfixed" was correct only while the broken metric
was believed to be a policy choice; it was not.

---

## 6. NEXT DISPATCHES — the shortest path to moving the ceiling

1. **R8 representation classes** — the unlock for R10. Needs a REQ; graph-schema write
   authorization required before it starts.
2. **Rule R2** (Bill) — it is built and enforced; the ruling is what makes it count.
3. **TD-148's REQ, then its build** — this is what makes a fourth lane safe, and it gets
   cheaper the sooner it lands.
4. **The two D-129 REQs' executing dispatches** — REQ_ASKED_ATTRIBUTE_COVERAGE closes the
   untargeted-attribute half of the structural-refusal guarantee; REQ_BASELINE_RECORD_INTEGRITY
   stops the harness rewriting its own governance records.
5. **TD-136's ruling** (Bill) — it has been open since 2026-07-22 and it gates whether the
   household exemption is an architecture decision or a defect.

---

## 7. WHAT THE ROADMAP LANE ESTABLISHED, D-70 → D-136 (compressed)

Filed the dimensioned collection ceiling (D-70, `98dfb7a`) and ruled six of its
requirements. Built and ruled the sensitivity registry (R29/R30), the inbound author cap
(R12), the derivation lineage and cascade (R18, amended then ruled). Ported write-time trust
markers into the prompt (D-114) and renamed the header they sit under, in eight sites, after
a survey that found seven (D-115 → D-117, `872ad0c`). Corrected a mislabelled harness red's
mechanism twice, on the record (D-119). Closed the **structural-refusal** gap end to end:
found it (D-121/D-124), filed the REQ (D-125, `b07ab10`), traced it to **resolution
blindness** rather than the admission suppression the REQ first recorded (D-126), fixed it
with graph-wide subject resolution plus admitted-set keying (D-127, `829464f`,
`eval/test_structural_refusal.py`), and ruled it MET (D-128). Filed and then governed the
tooling that was quietly rewriting its own records (TD-150 → `f840161`). Killed the ceiling
preamble's count (D-131). Wrote the session-conduct rules this document's maintenance rule
belongs to (D-135/D-136).
