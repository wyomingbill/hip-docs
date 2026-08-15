# Fact Metadata Timeline Viewer — Investigation and Minimal Spec
Status: BUILT
Reconciled-Against: 56cf7b9 (read-only investigation; no code changes)

Question asked: what is the simple, clear way to VIEW the timeline of fact metadata for
the dashboard demo? Foundational questions answered first, spec last. No build performed.

---

## 1. What are we viewing? The unit is the fact ROW — and the row already IS the event.

The `:Fact` graph is effectively append-only: the only mutation ever applied to an
existing row is *closing* it (`valid_to` set, close-reason recorded, `superseded_by`
pointer written). Every state change opens a NEW row. So the distinction the question
poses — facts vs. events — collapses in this schema: **each fact row is simultaneously a
version of a fact and the write-event that produced it.** The chain
`row → superseded_by → row` over a `(attribute, owner, subject)` key is the complete
event history of that fact. No new unit needs inventing.

Auxiliary event layers that exist alongside the graph (none needed for v1, all
annotatable later):

| Layer | Where | What it adds |
|---|---|---|
| `confidence_log` | per-row property (memory_engine/store.py:126-144) | append-only trust transitions (ts, from, to, source, rationale hash) |
| Fact lifecycle NDJSON (TD-050) | `logs/fact_lifecycle/*.jsonl` | assertion/enrichment/change_detect/retraction events per session, off-graph |
| Recall audit | `logs/` NDJSON (memory_engine/recall.py) | who fetched which cold facts, what was allowed/denied |
| Epistemic record (D-1) | spec'd only (D1_RECORD_SPEC v1138, PLAN) | per-TURN decision record — the read/disclosure side, not the write side |

**Verdict: view fact-row chains. The write history is the graph; the read history (D-1)
is a separate, later layer.**

## 2. Is it just time-bound? No — and there are TWO clocks, unevenly implemented.

The engine-track schema (memory_engine/store.py `_new_node_props`) is genuinely
bitemporal:

- **Valid time** — `valid_from` / `valid_to`: when the fact was true in the world.
- **Record time** — `recorded_at` / `record_closed_at`: when the system learned/closed it.

The two clocks visibly diverge in exactly one place: **corrections.** `_tx_correct`
closes the erroneous row with `closed_reason='error'` + `record_closed_at`, and the
replacement row *inherits the old row's `valid_from`* ("it was always true — we recorded
it wrong"). Supersession, by contrast, starts a new valid period. This distinction is
the single most demo-worthy thing the metadata contains: the record is corrected, the
error remains auditable, and validity is not rewritten.

Axes actually queryable today:

| Axis | Support today | Notes |
|---|---|---|
| Subject/owner | YES — parameter on every read path | `/api/memory-view?subject=`, chain grouping key |
| Valid time window | YES — `/api/fact_history?since=` and `touched_since=` | already built for presentation mode |
| Record time | PARTIAL — stored on engine-track rows, **not returned by `/api/fact_history`** | additive RETURN-clause change when wanted |
| Trust tier | YES — computed server-side per node via `trust()` in the existing endpoint | |
| Lifecycle state | YES — derivable from `valid_to` + close reason per row | see drift flag below |
| Storage tier / salience | In `/api/memory-view` (debug), not in `fact_history` | not needed for v1 |

**Can retrieval already take a time-bound — yes or no?** For the VIEWER: **yes,
effectively.** `/api/fact_history` returns full chains in one pass; "state as of T" is a
pure client-side computation over rows already delivered
(`valid_from <= T < valid_to`, null = open). No new Cypher, no new endpoint, works at
demo scale (hundreds of rows). For the LIVE retrieval path: **no** — `read_user_facts`
and recall are heads-only (`valid_to IS NULL`) with no as-of parameter; if server-side
as-of is ever wanted it is a one-line WHERE clause the schema natively supports. Not
needed for v1 and not proposed.

**Which clock do we scrub? Valid time.** Record time matters only where it diverges
(corrections); render that divergence as an annotation, don't build a second scrubber.

## 3. Existing tools / analogues.

Decisive constraint first: fact values are envelope-encrypted (TD-030) and only the HIP
server process holds the decryption path. **Every generic graph/DB browsing tool can
show ciphertext and metadata only.** The viewer must live behind HIP's own endpoint —
and one already does.

| Tool / pattern | Fit |
|---|---|
| Neo4j Browser | Raw Cypher tables/graphs; no temporal awareness; ciphertext-only. Dev tool, not a demo view. |
| Neo4j Bloom | Paid, rule-based styling, no bitemporal concept, ciphertext-only. No. |
| NeoDash | Dashboard builder over Cypher; same encryption wall; another service to run. No. |
| Graphiti temporal model (zep_store) | Parallel inactive graph with its own `invalid_at` semantics; not the `:Fact` schema. Irrelevant to this viewer. |
| XTDB / Datomic time-travel consoles | The right *pattern* (as-of scrubbing over an immutable store) — validates the concept; not embeddable. |
| Event-sourcing stream browsers (EventStoreDB etc.) | Same pattern from the event side; not embeddable. |
| `git log --follow` on one file | The closest mental model for a single chain: linear history, each node shows who/when/why. Free as a design analogue. |
| vis-timeline (vis.js, MIT) | Off-the-shelf ranged-bar timeline with groups/zoom. Would fit — but demo.html already has a working custom React renderer; vendoring a library to replace working code is backwards. Hold in reserve if proportional zooming is ever demanded. |
| **HIP's own `/api/fact_history` + `TimelineZone` (demo.html:596)** | **Already built, already the epistemic timeline (DEMO_BUILD_SPEC §5): one row per chain, trust badges, struck-through closed cells, write_state arrows, 4s poll, `touched_since` reveal.** |

## 4. The simple version — what v1 actually is.

The investigation's core finding: **~80% of this viewer already exists.** The gap
between what's built and "a clear timeline of fact metadata" is not a scrubber engine —
it is three small additions to the existing zone:

**V1 (in order of value):**

1. **As-of slider.** One `<input type="range">` spanning min(`valid_from`)…now over the
   chains already in memory. At position T, each chain highlights the row valid at T
   (open cells bold, not-yet-written cells dimmed, closed cells struck). This is the
   whole "media scrubber over metadata" — it is a client-side filter, zero new queries.
2. **Correction rendering.** Where `closed_reason='error'`, badge the cell distinctly
   and show both clocks on hover ("recorded 07-03, corrected 07-09 — valid_from
   inherited"). Requires adding `recorded_at`/`record_closed_at` to the endpoint's
   RETURN clause (additive, read-only). This is the bitemporal governance made visible.
3. **Client-side filters.** Subject dropdown (from `/api/members`), trust-tier badge
   toggle, lifecycle toggle (open / superseded / corrected / retracted). All over the
   already-delivered payload.

**Explicitly deferred:** proportional time axis and zooming (ordinal cells read better
at demo scale), a second record-time scrubber ("audit view"), vis-timeline adoption,
D-1 read-event overlay, lifecycle-NDJSON overlay, any Neo4j-side tooling, any as-of
support in the live retrieval path.

**Recommendation: REUSE.** Extend `/api/fact_history` (two fields) and `TimelineZone`
(slider + filters). Build nothing new; adopt nothing external. Simple beats impressive,
and the simplest thing here is finishing the viewer that exists.

## 5. Flags surfaced by the investigation (not fixed here).

- **Close-reason schema drift.** The extraction track writes `closed_by`
  ('superseded'/'retracted', extraction_queue.py:531,568) while the engine track writes
  `closed_reason` ('superseded'/'error', store.py:284,324). `/api/fact_history` and
  memory_dashboard read only `closed_reason` — extraction-track closes render with no
  reason. Candidate register entry; one-line fix is a coalesce in the readers or a
  migration to one property name.
- **`recorded_at` absent from `/api/fact_history`.** Stored on engine-track rows
  (backfilled by the Phase A migration, store.py:520-575) but not returned; corrections
  currently cannot show their record-time story. Additive fix, part of V1 item 2.
- **Two independent graphs.** zep_store/graphiti RELATES_TO edges with `invalid_at`
  still coexist with the `:Fact` schema (TD-027/TD-030 note in extraction_queue.py
  header). The viewer should stay `:Fact`-only; do not attempt to merge histories.
