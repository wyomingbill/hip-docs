# SESSION TRANSFER — HIP + Workspace Setup
Date: 2026-07-06 (Monday). For: Bill Brewster. Purpose: hand this thread to a new session with ZERO loss of engineering or decisions.

READ THIS FIRST. It is the source of truth for where things stand. Every claim here is grounded in commits or verified runs, not memory.

================================================================================
## PART 1 — MACHINE / ENVIRONMENT REALITY (this caused most of today's confusion)
================================================================================

- TWO machines exist, both have HIP:
  - **Mac** (home `/Users/billbrewster`) — the machine Bill sits at. Contains: `hip-dev`, `job_agent`, `Job Search`, `Clara Barcelo`, `Household_Intelligent_Platform`, and **Google Drive MOUNTED AS A LOCAL FOLDER** (`~/Google Drive/`). Model: 2019 16" MacBook Pro, i9, 32GB, macOS Tahoe 26.5.1 — CAPABLE, runs the desktop app fine.
  - **Mini** ("Server2026") — user `bill-ai`, Tailscale IP `[REDACTED-TAILNET-ADDRESS]`, hostname `[REDACTED-TAILNET-HOST]`. Runs the HIP dashboard, Neo4j, the live demo. This is where HIP infrastructure actually RUNS.

- KEY REALIZATION (took all day): Google Drive is MOUNTED as a folder on the Mac at `~/Google Drive/Brewster/ai_context_files/`. So Drive files are readable as normal local paths — NO MCP connector needed on the Mac. The "Drive is unreliable / can't reach files" problem was largely an artifact of trying to use the Drive MCP in the chat instead of the local mount.

- The context files (`project_job_hunt.md`, `project_clara_barcelo.md`, `overlays_ai.md`, `overlays_saas.md`, `agent.md`, templates) live in `~/Google Drive/Brewster/ai_context_files/`.

- FILE TRANSFER TO CHAT IS BROKEN: document/file attachments to the chat arrive EMPTY every time. WORKAROUND that works: screenshots, or plain text pasted inline. NEVER rely on file-attachment upload to move content to a chat session. CC inline output (tables, mermaid) also transfers fine via screenshot.

- The `<userPreferences>` block auto-injecting into messages all day = platform behavior (profile surfaced into the conversation), NOT a clipboard glitch. Harmless. Ignore its repetition.

================================================================================
## PART 2 — HIP ENGINEERING STATE (the important part — do not lose)
================================================================================

### 2.1 WHAT HIP IS
Household Intelligence Platform. A governed, multi-entity AI memory/operating system. Credibility instrument for Bill's job search (#1 priority) and vehicle for the AI-operating-systems work (#3). It demonstrates: cost-tiered routing inside a confidential enclave, per-member encrypted memory, a disclosure contract (governance enforced in code), and epistemic management (facts classified, reorganized, superseded with an audit trail).

### 2.2 REPOS / PATHS
- `~/hip-dev` — dev repo (private GitHub `wyomingbill/hip-dev`). ACTIVE work. Backs up to origin/main.
- `~/hip-harness` — frozen demo checkout (private `wyomingbill/hip-harness`). Voice server (7860) runs from here, frozen/pre-seam by design.
- `~/hip-deploy` — deploy dir for the public site.
- Interpreter on Mini: `$HIP_DEV_PYTHON` = `[REDACTED-USER-PATH]/hip-dev/.venv/bin/python`
- CC runs in tmux on the Mini historically; now also via the desktop app on the Mac. Model MUST be Sonnet (never Opus) — this is saved as default in CC.

### 2.3 THE DOC FRAMEWORK (established today, in ~/hip-dev/docs/)
Categories: `specs/ planning/ testing/ research/ epistemic/ debt/ general/` (+ a research split into `research-technical/` and `research-market/` was IN PROGRESS at end of session — SEE PART 6 WARNING).
- Naming law: `<SUBJECT>__<slug>__v<YYYYMMDD_HHMM>.md` (Mountain Time). Never overwrite.
- `LATEST_<subject>.md` symlink per subject.
- `docs/INDEX.md` = single source of truth (subject | category | current file | status | reconciled-against). STATUS values: PLAN | IN_PROGRESS | BUILT | SUPERSEDED | STALE.
- `CLAUDE.md` instructs every CC session to read INDEX.md FIRST.
- Public docs mirror: `wyomingbill/hip-docs` (readable). Docs served in-browser at dashboard routes: `/universe`, `/hitl`, `/epistemic-design`, etc.

### 2.4 THE INTEGRATION PLAN (the big work today) — Phases 0-3 DONE, text path 8/8
Root cause the plan addressed: **the governed pipeline is built but the live orchestrator routed AROUND it.** Every bug (self-supersede loop, statements-as-queries, retrieval misses) was a symptom of that disconnect. Plan = wire the governed pipeline into the live path, one SEAM at a time, each gated by an automated harness.

- **Phase 0 (call graph + seams + idempotency)** — DONE. Doc: `docs/research/LATEST_LIVE_CALLGRAPH.md`. Identified 5 seams: S-INT (interpretation), S-WRITE (write), S-CLS (classify), S-RET (retrieval), S-CONS (consolidation). Found the self-supersede loop cause.
- **Phase 1 (integration test plan, E1-E8)** — DONE. Doc: `docs/testing/LATEST_INTEGRATION_TEST_PLAN.md`. 8 acceptance scenarios + invariants.
- **Phase 2 (live-path harness "Tier L")** — DONE. `eval/integration_live.py` drives the REAL path (HTTP POST to `/api/text-query`, real orchestrator, direct Neo4j assertions) — NOT in-process shims. Baseline started 4/8. Also fixed ENV-1 (machine guard `socket.getfqdn()` -> `gethostname()`).
- **Phase 3 (wire seams)** — Seam A + Seam B DONE. Text live path now **8/8, gate-enforced, 3 identical runs.**

### 2.5 THE E1-E8 SCENARIOS (what "8/8" means)
- E1 statement -> ONE supersede + acknowledgment ("Got it, Ray switched from metformin to Jardiance 10mg")
- E2 recall retrieves the new value with correct subject
- E3 simple personal -> EDGE, correct answer (no cross-subject leak)
- E4 complex personal -> escalates to CORE (inside enclave)
- E5 cross-subject privacy (Maya asks re Ray; Maya's own facts withheld)
- E6 empty-set unknown fact -> STRUCTURAL refusal (guard_triggered=True, code-enforced, zero model call)
- E7 fact_history single clean chain (no self-supersede)
- E8 idempotency (replay = no-op)

### 2.6 KEY FIXES COMMITTED TODAY (with commit hashes)
- **Idempotency / self-supersede loop** (`3bf594f`): `detect_and_apply_async` fires once/turn; the N writes came from the SAME scripted demo turn being REPLAYED (Groq re-proposes on restatement, writer never compared values). Fix: value-equality guard in `_apply_changes` — decrypt active value, exact-match, log no-op if equal. E7/E8 green.
- **Routing personal-EDGE bug** (`c615fe8`): personal-intent path (`router.py:722-726`) hardcoded TIER_LOCAL and returned BEFORE complexity/Bloom. In HIP the whole edge->core cascade is INSIDE the operator confidential-computing enclave, so tier is a COST decision, NOT a privacy boundary. Fix removed the early return; personal queries now route by complexity. Verified: "What medication do I take?" -> EDGE; "Draft a care plan for Ray weighing fall risk vs meds" -> CORE (bloom 6); WW1/WW2 -> CORE (no regression).
- **Divergent CORROBORATED classifier** (`4fadca2`): `queries.py` (numeric _CONF_ORDER rise) vs `fact_change.py` (any reconcile to medium/high) classified the SAME fact differently by caller — a determinism defect in the core "governed truth" claim. Fixed `fact_change.py` to strict-upward `_CONF_ORDER` matching `queries.py`. 11-case agreement test green.
- **Seam A** (`6c2354b`): declarative-update grounding. A statement wrote correctly but the grounding guard evaluated the PRE-write snapshot, so the CORRECTION-RULE ack never fired ("I don't have that confirmed yet") and recall missed. Fix: for a declarative update to the speaker's own accessible fact, run detection SYNCHRONOUSLY before disclosure, re-retrieve, evaluate post-write. Side effect: closed a real cross-subject leak (prompt's "Things you know" was retrieving AROUND the injection contract) -> E3 flipped green too. Result 7/8.
- **Seam B** (`d4a031e`): structural empty-set refusal. INJ-6b in `injection_contract.py` — a personal QUESTION naming a precisely-keyworded attribute (medication, allergy, health_condition, dietary, employer, financial) fires guard_triggered=True when NO admitted fact AND no candidate fact carries it for a resolved subject. Refusal = code-enforced `empty_set_refusal()`, model never invoked. Scoped so fact-exists-but-denied stays silent (E5 holds) and loose attributes (relationship/schedule/preference) excluded. Result 8/8.
- All pushed to origin: `4fadca2..d4a031e` (11 commits) + later `a35c933`, `959be24`. **VERIFY latest push state — some later commits (a35c933, 959be24) may or may not have been pushed. Run `git -C ~/hip-dev log --oneline -15` and `git status`.**

### 2.7 THE DEMO (three-zone, operator-paced)
- URL (from Mac browser over Tailscale): `http://[REDACTED-TAILNET-ADDRESS]:7871/demo`
- Also: `/hitl` (HITL checklist), `/epistemic` (timeline), `/universe` (system map), `/epistemic-design` (design reference)
- Dashboard bound TAILNET-ONLY on 7871 (LAN refused, verified). Started via launchd on current code. `/api/text-query` was ADDED to the dashboard (commit `a35c933`) so the browser tests the SEAM-wired code in-process on hip-dev — the 7860 voice server is frozen/pre-seam and does NOT reflect the seams.
- Demo run model rebuilt (commit `901acff`, refined `959be24`): **starts EMPTY, operator-paced, one question per "Next" click, no auto-advance.** Dashboard reveals facts ONLY as dialogue touches them (`touched_since=<session_start>`) — NOT pre-loaded seed. Bill's explicit requirement: dialogue reveals functionality, one capability per turn.
- A purpose-built script `demo_scripts/reveal_demo.json` (additive, existing scripts untouched): R01 routing (vault stays empty) -> R02 first encrypted-record reveal + decrypt -> R03 clean fact write -> R04 supersede chain + ack -> R05 recall -> R06 structural refusal -> R07 cross-member privacy (nothing appearing IS the beat).
- Household fixture: Maya/Sam/Dad/Ray (also Bill/Sarah in some seeds). D1-D9 seeded. Note demo also uses "Elena" (Bill's mother) metformin->Jardiance as the supersede example in newer runs.
- HONEST demo notes: (a) household context appears after turn 1 regardless of question — INJ-4 injects household facts every routed turn; the script narration owns that beat. (b) Known S-INT wart: allergy write renders subject "null" (Groq emits literal "null" string) — logged, ratchet-first fix, NOT patched.

### 2.8 WHAT'S NOT DONE (HIP)
- **DIV-2: VOICE PATH RUNS NO CONTRACT AT ALL.** Seam A/B fixed the TEXT path (what Tier L measures). Voice (7860) is ungoverned, untested. This is the biggest remaining integration gap. INJ-6b etc. land there "for free" once voice is wired.
- **Phase 4 (HITL testing)** — checklist built at `/hitl` (HITL-1 naturalness, HITL-2 timeline legibility, HITL-3 narration fit, HITL-4 routing plausibility, HITL-5 empty-set beat, HITL-6 edge realism). Bill has NOT yet worked through it. This is HUMAN judgment — the machine can't do it.
- **Phase 5 (reconcile demo to tested path)** — prerequisite done (dashboard restarted on 8/8 code, verified). Full in-browser E1-E8 re-verification by Bill not yet complete.
- **TD-108 (MOST DANGEROUS MISSING ARTIFACT, Bill's words):** a canonical, append-only, per-fact EPISTEMIC EVENT RECORD `{event_id, ts, turn_id, fact_id, subject, attribute, from_state, to_state, from_value, to_value, transition, cause_utterance, source}`. Currently `/api/fact_history` RECONSTRUCTS from graph-walk (superseded_by/valid_to/confidence_log) — a VIEW, not a recorded event stream. This log IS the regulatory/governance audit artifact the whole thesis rests on, AND it's the clean fix for the timeline being "hand-built visualization over insufficient data." Two design forks to decide: (1) source-of-truth vs parallel-audit; (2) inline-write (touches frozen pipeline / MEM-100 byte-identical) vs async-write. Deferred — decide when it's built, likely folds into the S-WRITE seam decision.
- Other divergences from the universe map (`docs/research/LATEST_SYSTEM_UNIVERSE.md`): 17 total, ~4-5 governance/correctness. Key open ones: candidate_facts() not wired live (INJ tier filter bypassed), no cold-tier exclusion in retrieval, /api/decrypt unauthenticated (TD-101, tailnet-only mitigates), consolidation (harden/confirm/resolve) built but OFFLINE-only (facts don't climb trust live).

### 2.9 THE EPISTEMIC MODEL (spec'd — reference, built as a 5-piece diagram set)
Life of an utterance through HIP (Bill wanted this decomposed piece-by-piece, spec'd not live):
1. **INTERPRET** — utterance -> structured candidate (attribute, subject, owner, value, confidence) -> compared to prior fact for same key -> one of 4 write decisions: SUPERSEDE (replaces, close prior + open new), AUGMENT (adds alongside), CORRECT (prior was error, close as error), UNRESOLVED (can't tell / low confidence, keep both flag).
2. **WRITE** — bitemporal graph. valid_from/valid_to, closed_reason (superseded vs error), superseded_by, record_closed_at, confidence_log. Nothing deleted, only closed.
3. **CLASSIFY** — trust LADDER, first-match-wins, fixed order: DERIVED (system-inferred, checked FIRST, permanently second-class) -> CONFIRMED (authority signed off) -> CORROBORATED (independent sources agree) -> ASSERTED (single clear source) -> UNCONFIRMED (catch-all). The ORDER is the governance — deterministic, explainable, no re-weighing.
4. **RETRIEVE + DISCLOSE** — disclosure contract = series of ANDs: subject-scope AND relevance AND current-and-trusted. Empty-set guard: if nothing clears, REFUSE, don't fabricate.
5. **CONSOLIDATE** — offline (harden asserted->corroborated, resolve unresolved, confirm->confirmed). BUILT BUT NOT WIRED LIVE. So live: facts enter at birth level, stay unless superseded; they do NOT climb on their own.
Reference artifact (PDF) committed at `~/hip-dev/docs/epistemic/EPISTEMIC_REFERENCE__v20260706.pdf`. The three-layer plan: SPEC (details) -> REFERENCE (diagrams + use cases) -> PRESENTATION (abstracted). Only REFERENCE PDF exists so far.

================================================================================
## PART 3 — INFRASTRUCTURE / WORKSPACE (set up today)
================================================================================

### 3.1 THE DECISION: unified workspace = Claude DESKTOP APP (runs on the Mac) + CC inside it
- Desktop app confirmed WORKING on Bill's Mac (earlier "too old" was wrong — machine is capable). Has Home (chat) + Code (CC) tabs. Point CC at a folder via "Select folder…". Reads that folder's CLAUDE.md.
- This is the "one spot for chats + files" Bill wanted. Files are LOCAL on the Mac; Drive is a mounted folder; CC has direct file tools. No Mini-relay, no paste-relay needed for Mac-local work.
- Model in the desktop app kept flipping to Opus 4.8 — MUST be set to Sonnet 4.6 (Bill's cost rule; Opus already burned ~$24.82 in credits earlier via a session-limit "continue on credits" moment + auto-reload past the $20 cap; auto-reload should be turned OFF as a guard).

### 3.2 CONTEXT DIRS + LAWS
- `~/context/` created on the MINI (job search / business / generative). Has a `CLAUDE.md` encoding Bill's profile, priorities, HOW-TO-WORK, resume constraints, file-management, Sonnet-only. Also a `FILE_MANAGEMENT_LAW.md` was being created (homes, naming law, mandatory research INDEX, resume targeted-edits-only, Drive create-only handling, git-backup).
- OPEN QUESTION not fully resolved: whether non-HIP work lives on the Mini (`~/context`) or should be Mac-local (since Bill sits at the Mac and files are there). Leaning: keep everything on the machine where it's git-backed, avoid duplicate copies drifting. HIP RUNS on the Mini; the Mac may have a clone. **Verify whether Mac `~/hip-dev` and Mini `~/hip-dev` are the SAME git repo (same origin) or two separate copies — if separate, that's a drift risk to resolve (pick ONE canonical).**

### 3.3 FILE MANAGEMENT RULES (the "never deviate" law Bill demanded)
- Files live in ONE home, git-backed. Naming law `<SUBJECT>__<slug>__v<YYYYMMDD_HHMM>.md`, never overwrite.
- Research: dedicated folder + mandatory `INDEX.md` (subject | file | date | summary | tags). A research file without an INDEX row is NOT archived. Retrieval = read INDEX first, never guess filenames.
- RESUME (critical constraint): TARGETED in-place edits (str_replace of specific text) ONLY. NEVER regenerate the whole document. Version every change, diff new vs old to confirm nothing reworded/dropped/compressed. No restructuring, no generic corporate language.
- Drive MCP is CREATE-ONLY (no edit-in-place, no delete). "Update" a Drive file = read + create new versioned file. But on the Mac, Drive is a MOUNTED FOLDER so normal file ops work — prefer that over MCP.
- CC: if a request would VIOLATE the law (e.g. "just overwrite", "regenerate the resume"), FLAG the conflict and follow the LAW, not the request.

### 3.4 CC OPERATION NOTES
- Modes (desktop app, bottom-left toggle / shift+tab in terminal): Manual permissions | Accept edits | Plan mode | Auto mode | Bypass permissions.
- "Accept edits" auto-accepts edits but NOT flagged `cd`-before-git / sensitive-path commands. Those show "Always allow" (whitelist the type) vs "Allow once".
- To reduce approval prompts: use `git -C ~/hip-dev ...` instead of `cd ~/hip-dev && git ...` — the `cd`-before-git triggers the "untrusted hooks" warning every time.
- CC sessions are LOCAL to the machine — they do NOT appear on the phone. Phone only syncs chats. Don't leave an untrusted CC run going unwatched.

================================================================================
## PART 4 — DEBT REGISTER (docs/debt/LATEST_DEBT.md)
================================================================================
- TD-101 (SEC): unauthenticated dashboard endpoints; /api/decrypt returns plaintext. Tailnet-only mitigates. NEVER public funnel until auth ships.
- TD-102 (GATE): stray issue_INT-001 files after passing gate (transient). 
- TD-103 (OPS): launchd voice-server start non-deterministic (I/O error 5).
- TD-104 (OPS): Neo4j password had special char (!) — friction. (Rotated earlier.)
- TD-105/106/107 (demo-safety): subject-resolution, port pinning (7871), exposure tailnet-only — RESOLVED.
- TD-108 (ENG): canonical epistemic event record — see 2.8. THE big one.
- S-INT "null" subject wart (Groq literal "null") — ratchet-first fix pending.

================================================================================
## PART 5 — STANDING RULES (established across the session)
================================================================================
- Model: Sonnet 4.6, NEVER Opus. Haiku for scoring only. (Saved as CC default.)
- Every CC research/diagnostic writes to a file in docs/ (versioned + LATEST symlink) AND pastes the small consumable table inline (attachments to chat arrive empty).
- Gate green after every seam; ratchet every fix into a scenario; commit each; don't push unless told.
- RESTART the dashboard on new code before verifying (stale-code masked fixes repeatedly today — "gate proves code, not deployment" is the recurring failure).
- Don't design/assert against the system without reading actual code/git-state first. This failure (inventing features, re-speccing built work) cost hours.
- Bind tailnet-only, never public funnel until endpoints are authed.
- Demo narration framing: "governed cost economics within a confidential enclave" — personal stays local when simple, escalates on complexity, all inside the trust boundary. Every "why didn't it do X" has a governance answer.
- LEVERAGE: Bill's #1 is the job search. HIP is a credibility instrument, NOT the job. Multiple times today HIP became the work and the job search got zero minutes. Continuing to wire HIP past "demonstrably works" is negative leverage vs #1 unless a specific opportunity needs it. This is the honest recurring flag.

================================================================================
## PART 6 — END-OF-SESSION STATE / WARNINGS (what was mid-flight when transfer requested)
================================================================================
- A hip-dev docs REORG was IN PROGRESS and NOT COMPLETED/VERIFIED. Bill directed splitting research into `research-technical/` and `research-market/`. CC (on Mac, Sonnet) was mid-reorg: creating dirs, moving files, renaming to naming law (e.g. trust_model_v1.txt -> TRUST_MODEL__v1-raw-source__v20260702_1454.txt), creating a `.claude/projects/.../memory` dir. **Bill lost trust in the autonomous run and needs to VERIFY before continuing.**
- FIRST ACTION on return to the Mac:
  ```
  git -C ~/hip-dev status
  git -C ~/hip-dev log --oneline -15
  ```
  Confirm exactly what CC did. Keep or revert from VERIFIED state. Do NOT grant blanket "Always allow" to an untrusted run — use narrow, checkable steps.
- Also verify push state: `a35c933` and `959be24` may not be pushed. `git -C ~/hip-dev push origin main` if clean and intended.
- Auto-reload on usage credits should be turned OFF (Settings) as a spend guard.

================================================================================
## PART 7 — WHERE TO GO NEXT (Bill decides; ranked by his own leverage rule)
================================================================================
1. **Verify the mid-flight reorg** (Part 6) — required before any more hip-dev file work.
2. **Job search (#1)** — the pivot repeatedly deferred. Context at `~/Google Drive/Brewster/ai_context_files/project_job_hunt.md` (readable as a local file on the Mac). The 8/8 demo is now a real proof-of-capability artifact for VP/Director Ops/Transformation conversations — "governed multi-entity AI operating model, working prototype," honestly framed (tailnet demo, voice unwired).
3. **HITL testing (Phase 4)** — Bill works the `/hitl` checklist in-browser against the live 8/8 demo. Human judgment on naturalness/legibility/narration-fit/edge-realism.
4. **TD-108 event record** — the audit artifact; likely the highest-value HIP build if HIP work continues, because it's where the timeline and the governance-thesis converge.
5. **Voice contract (DIV-2)** — wire the injection contract into the voice path so it matches the text path.

================================================================================
END OF TRANSFER. Nothing here is guessed — grounded in commits, verified runs, and this thread. When resuming, read Part 1 (env), Part 2 (HIP state), Part 6 (mid-flight warning) first.
================================================================================
