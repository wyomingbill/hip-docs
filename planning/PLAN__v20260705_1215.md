# HIP Demo Plan — Locked Sequence and Track Discipline

**Version:** v20260705_1215
**Purpose:** The agreed plan of record. Keeps the effort on the conversion path and off the build-forever trap. Read this at the start of any session that threatens to reopen scope.

## The one rule that governs everything
Meetings first. The demo surfaces get built, hardened, locked, and then USED. More build waits until meetings produce signal. The pull is always toward one more feature. That pull is the enemy of the goal. The goal is a job. HIP is the proof-of-thinking artifact that gets Bill in the room. The demo is the credential, not the product.

## Two tracks, parallel, different rules
### Track A — meeting-getters (BUILD, HARDEN, LOCK, THEN STOP)
Scripted-text demo. Three views: orchestration/models, encryption/vault, epistemic/disclosure gate. Real orchestrator via process_text_query. Needs Neo4j + dashboard, NOT voice. Sequence: build -> harden -> script -> lock -> go get meetings. Do not keep polishing after lock.
### Track B — voice (ITERATE HARD, PARALLEL, NEVER RELIED ON)
Voice never blocks traction. Not leaned on until it passes the same acceptance gate as Track A. First item: scripts/start_manual.sh exporting NEO4J_PASSWORD and launching directly, removing the launchd bootstrap dependency. It unblocks echo, barge-in, and TD-042 at once. Then echo cancellation, barge-in, 2-person attribution.

## Acceptance gate — bulletproof, always works (both tracks before use)
- Deterministic: same script in, same result out. Fixed seed, demo_reset before each run.
- Self-checking: preflight verifies Neo4j, dashboard, seed, endpoints before showing anyone.
- Fails loud not weird: Groq timeout falls back to local and says so. No silent slow, no hang.
- One command: demo_run.sh <script> does reset, seed, drive, confirm all three panes.

## Deferred (do NOT solve early)
- Presentation surface: remote-live vs site-embedded. Decide AFTER Track A locks.
- Roadmap for more build: parked until meetings produce signal.

## The reminder
Lock what converts. Mature what compounds in the background. Do not let either steal time from getting meetings. When a session reaches for a new feature before Track A is locked and meetings are underway, that is the drift. Stop and re-read the one rule at the top.
