# DISPATCH_R16_R17_LEDGER_SURVEY
Status: BUILT (survey only — no production code changed, per instruction)
Reconciled-Against: d77af0f (parent HEAD this survey read against)

**TYPE:** ANALYSIS (survey only, explicitly instructed — "no production code changes, no
destructive writes, nothing shipped beyond the survey document")

**REQ:** `docs/requirements/REQ_STRUCTURAL_CEILING__dimensioned-collection-limit__v20260802_2205.md`
R16 and R17. No amendment, no build — nothing here changes either requirement's text.

## THE ASK

Dispatch text, verbatim:

```
=== D-160 | ~/hip-roadmap, roadmap | R16+R17: survey the ledger rebuild, STOP before
    building ===
STANDARD PREAMBLE. Lane A. SURVEY ONLY — no production code changes, no destructive
writes, nothing shipped beyond the survey document.
GOVERNING REQ: REQ_STRUCTURAL_CEILING R16 and R17. D-154 established these are ONE
build, the largest single item in the plan.

WHY THIS IS DIFFERENT: R16 was ruled 2026-07-31 as BOTH mechanisms — opaque keyed
commitments in the append-only chain AND payloads off-ledger under per-member keys.
R17 became load-bearing as a result. A16 and A17 must flip together; certifying a
commitments-only ledger while personal data persists elsewhere unerasable is exactly
the gap that ruling identified. The current ledger DELIBERATELY carries encrypted
personal payloads with crypto-shredding as the designed erasure path, driven by
statute (47 USC 551). That is a ratified design, not an oversight.

1. SURVEY THE EXISTING LEDGER AS BUILT, evidence from the code: what is on the chain
   today, what the chain hash covers and deliberately omits, how crypto-shred and
   payload erasure currently work, and which of R16's permitted/prohibited field lists
   today's records violate. Cite call sites.
2. SURVEY WHAT R17 NEEDS: the seven-step erasure sequence and the machine-verifiable
   erasure report. For each step, say whether a mechanism exists, partially exists, or
   does not exist. D-105's discipline — absent means absent, not glossed.
3. THE COMPATIBILITY QUESTION, answered explicitly: the ledger anchor's validity was
   proven to survive lawful erasure because the chain omits payload content and the
   erased flag. Does the R16 rebuild preserve that property, or does it invalidate
   every anchor taken to date? STOP AND REPORT if it invalidates them — that is a
   different decision than a build.
4. SEGMENT THE BUILD. Propose an ordered sequence of dispatches, each independently
   committable and each leaving the tree green. Name which segment first makes any
   external deletion claim honest, and which segments are prerequisites versus
   parallel. Do NOT build any of them.
5. NAME THE BLAST RADIUS. Which existing behaviours change, which fixtures break,
   what the demo does differently, and whether any segment requires destructive-write
   authorization from Bill before it can run.
6. Rule nothing. Report LONG to a dispatch doc.
```

## WHAT WAS DONE

1. Gate checked — matched. Repo lock acquired, pulled clean.
2. Read R16 (`:590-644`) and R17 (`:646-666`) in full, and R16's own inline "RULED D-71"
   ruling text — noted this ruling lives ONLY in the axis section, not in §16's
   per-requirement ruling record (confirmed: `awk` scan of §16 finds no R16/R17 entry at
   all) — R16/R17 are FILED with a design decision made (D-71: "both mechanisms"), not
   MET/NOT-MET ruled. No dedicated D-71 dispatch doc was found (`grep -rl "D-71\b"`
   returns one incidental mention, not a dispatch doc) — same missing-citation pattern
   D-157 found for "D-154"; the ruling's SUBSTANCE is fully recorded verbatim in R16's
   own text regardless, so this did not block the survey.
3. Read `harness/epistemic_ledger.py` in full (625 lines): the hash-field set, event
   construction, both erasure paths (`destroy_member_key`, `erase_payload`), and
   `verify()`.
4. Read `harness/ledger_anchor.py` in full (206 lines) — the anchor mechanism and its
   own documented, D-89-proven crypto-shred compatibility argument.
5. Read `harness/extraction_queue.py::retract_fact` and `write_facts` — the current
   per-fact retraction path.
6. Read `harness/encryption.py`'s DEK scheme — found the per-fact key granularity R17
   needs already exists structurally (see WHAT WAS FOUND).
7. Read `harness/custody_exit.py`'s dyad re-keying mechanism — a real, adjacent
   key-destruction mechanism, at a coarser (dyad, not fact) granularity than R17 needs.
8. Read `harness/epistemic_record.py::_fact_entry`/`build_epistemic_record` — the actual
   payload shape written into the ledger today via `log_epistemic_record`.
9. Grepped for embedding-deletion, backup-expiry-scheduling, and erasure-report
   mechanisms anywhere in `harness/`, `memory_engine/`, `scripts/` — zero hits for all
   three, confirmed by reading each candidate match, not by grep count alone.
10. Enumerated every real caller of `epistemic_ledger.append()` (4: `identity_keys.py`,
    `epistemic_record.py`, `demo_reset.py`, `verify_ledger.py`) and every test file
    touching the ledger (5: `test_anchor_emitter.py`, `test_ledger_anchor.py`,
    `test_hel_smoke.py`, `test_registry_version_stamp.py`, `harness.py`'s own AUDIT
    block) — the full blast-radius surface for item 5.

    > **CORRECTED 2026-08-04 (D-R-168).** The "4" real callers above was WRONG — it
    > came from a grep for the literal pattern `epistemic_ledger.append(`, which
    > cannot match a file that does `from harness.epistemic_ledger import append`
    > and calls the bare name. **10 more real production call sites existed at every
    > point this survey was written and after**, across `harness/custody_exit.py`,
    > `harness/household_keys.py`, `harness/care_team_keys.py`,
    > `harness/dyad_registry.py`, and `harness/ledger_payload_store.py`'s own audit
    > tombstone — found by D-R-167, AST-enumerated and flipped by D-R-168, which also
    > found 2 further same-module calls inside `epistemic_ledger.py` itself (needing
    > no import at all) that even D-R-168's own first AST pass missed. The TRUE total
    > was 16, not 4. `verify_ledger.py` itself was correctly identified as a
    > non-caller (it never calls `append()` at all) — that part of this line was
    > right. See `docs/dispatches/DISPATCH_LEDGER_CALLERS_FLIPPED__ast-enumeration-
    > sixteen-not-four-standing-invariant-built__v20260804_2019.md` (D-R-168) for the
    > full correction. Old wording kept visible per this project's own "annotate the
    > correction; never silently patch" discipline.
11. Wrote this dispatch doc. No file outside `docs/dispatches/` touched.
12. Released the lock (nothing to commit besides this doc).

## WHAT WAS FOUND

### Item 1 — the existing ledger, evidence from the code

**What's on the chain today.** Every event carries: `hel` (format version), `seq`,
`event_id` (a UUID), `event_type`, `ts`, `actor` (`{"kind", "id"}`), `correlation`,
`prev_hash`, `payload_kid`, `payload_sha256`, `hash`, and EITHER `payload_enc`
(member-actor events: AES-256-GCM ciphertext, inline) OR `payload` (system-actor
events: plaintext, inline) — `harness/epistemic_ledger.py:398-427` (`_build_event`).

**What the chain hash covers and omits.** `_HASH_FIELDS` (`:74-75`) =
`("hel", "seq", "event_id", "event_type", "ts", "actor", "correlation", "payload_kid",
"payload_sha256", "prev_hash")`. **Deliberately absent: `payload`/`payload_enc` and
`erased`** — the module's own comment (`:68-73`) states this is FOR erasability:
`payload_sha256` (a digest computed once, at write time) stands in for the content, so
the content itself can later be nulled without breaking `event_hash()`.

**How crypto-shred and payload erasure work, today.** Two paths, both proven
chain-preserving by `verify()`'s own logic (`:495-554`):
- `destroy_member_key(member_id)` (`:204-232`) — shreds the per-member AES key file.
  Touches NO segment file; appends a `system.note` audit event. Every payload that
  member ever encrypted, on every copy, becomes permanently undecryptable — but the
  CIPHERTEXT BYTES remain inline in the chain forever (only the key is gone).
- `erase_payload(seq)` (`:560-614`) — targeted, single-event, THIS-COPY-ONLY: nulls
  `payload`/`payload_enc` in place, adds `erased` metadata (outside `_HASH_FIELDS`),
  leaves `hash`/`payload_sha256`/`prev_hash` untouched. `verify()` explicitly accepts a
  null content field WITH `erased` metadata as valid (`:529-533`).

**Which of R16's field lists today's records violate — four distinct findings, not one:**

1. **`actor.id`** (plaintext member identifier, e.g. a member's own registry ID) is
   IN `_HASH_FIELDS` — permanently chain-hash-covered, present on every event that
   member's turns generate. Directly matches R16's prohibited "subject or author names;
   stable household-visible identifiers." **Confirmed violation** — and the module's OWN
   docstring already flags this as `HEL-ACTOR-1`, a known Phase-1 gap: "actor.id is
   plaintext in the immortal envelope... NOT pseudonymized here — the correct fix is
   registry-level opaque member IDs (one identifier scheme system-wide)."
2. **`payload_kid`** (`f"member:{member_id}"`, `:419`) — embeds the SAME plaintext
   member identifier a second time, in a field that (unlike `actor`) has no existing
   flag naming it. **Confirmed violation, same category as #1, previously unnamed.**
3. **`payload_enc`** (ciphertext, inline) — R16's prohibited list explicitly names
   "ciphertext containing the claim." Today's chain carries exactly that, for every
   member-actor event. **Confirmed violation** — this is the field R16's rebuild exists
   to eliminate from the chain entirely (moving it off-ledger).
4. **`payload_sha256`/`hash` use plain, unsalted SHA256** (`_sha256()`, `:125-126`), not
   the "appropriate keyed or salted construction" R16 requires so "predictable
   household facts cannot be dictionary-tested." For system-actor events (plaintext
   payload), a low-entropy payload IS dictionary-testable against this hash today.
   **Confirmed construction-level gap**, distinct from the field-presence violations
   above.

**And the reverse direction — R16's own required fields, absent today.** `keyed_commitment`
does not exist as a concept anywhere in the current schema (the whole point of the
rebuild); `policy_version`, `registry_versions`, `service_role`, and a real
`status_or_tombstone` field (today's `erased` is close in spirit, different in shape)
are likewise absent. R16 is not "compliant except for some extra leakage" — the chain
today satisfies **none** of its nine permitted fields by name, and violates at least
four ways beyond that.

**What actually gets written, in practice.** `harness/epistemic_record.py::_fact_entry`
(`:86-126`) is the payload shape reaching `epistemic_ledger.append()` via
`log_epistemic_record` — it carries `fact_id`, `attribute`, `owner`, `subject`,
`confidence`, `sensitivity`, `write_state`, `level` per admitted/denied fact. TD-030's
own value-stripping (`_strip_values`, `_VALUE_KEYS`) already keeps the CLAIM'S VALUE out
— but the claim's SHAPE (who, what attribute, which fact) is fully present, only
encrypted. This is the concrete content the rebuild has to relocate off-ledger.

### Item 2 — R17's seven-step erasure sequence, each step graded

| step | status | evidence |
|---|---|---|
| 1. revoke active access paths | **PARTIAL, and arguably not what R17 means** | `retract_fact` (`harness/extraction_queue.py:713-765`) sets `valid_to`/`closed_by`, excluding the fact from retrieval queries (`WHERE f.valid_to IS NULL`) — but the ciphertext and wrapped DEK remain live and decryptable by anyone holding the owner key. This is a retrieval filter, not an access-path revocation. |
| 2. destroy/render unavailable key material | **PARTIALLY EXISTS — the hard part is already built** | `harness/encryption.py:21-24,149-158`: every `:Fact` already gets **a fresh, per-fact random DEK**, wrapped with the owner key, stored as `encrypted_dek`. The PER-ARTIFACT key granularity R17 requires already exists structurally. What's missing: nothing nulls/destroys a specific fact's `encrypted_dek` on retraction — `retract_fact` never touches it. A related, coarser mechanism exists at dyad granularity: `harness/custody_exit.py::exit_custody` → `atomic_rekey_dyad`, which re-keys an entire dyad on custodian eviction — real, proven key-destruction infrastructure, but not fact-level. |
| 3. delete active database rows where supported | **DOES NOT HAPPEN** | `retract_fact` is `SET f.valid_to = $ts` — a Cypher `SET`, never a `DELETE`. Row, ciphertext, and `encrypted_dek` all persist. Confirmed directly, matching R16's own §7.1 "Current truth" text exactly. |
| 4. remove vector entries, caches, search indexes | **DOES NOT EXIST** | Zero hits for any embedding-deletion code anywhere in `harness/`/`memory_engine/`. Retracted facts' embeddings persist (R16's own §7.1 already states this; re-confirmed by search, not assumed from the REQ's own text alone). |
| 5. append an opaque tombstone to the ledger | **MECHANISM EXISTS, NOT WIRED TO FACT ERASURE** | `erase_payload`/`destroy_member_key` both append real tombstone-shaped audit events to the HEL — but `retract_fact` never calls either; zero references to `epistemic_ledger`/`hel` anywhere in `extraction_queue.py`. The primitive is real; nothing invokes it from a fact-level erasure path today (because no fact-level erasure path exists yet — only retraction). |
| 6. schedule backup expiry | **DOES NOT EXIST — no backup system to schedule against** | `destroy_member_key`'s own docstring names this as an open dependency: "backups hold a copy of the key file; per OQ-2 §6.2 step 3 the deletion MUST be propagated to every backup destination. This function only shreds the primary." No backup/replication code exists anywhere in this checkout (`grep -rln backup` returns only the ledger's own docstrings and an unrelated latency-analysis script). This step depends on infrastructure genuinely outside this codebase today. |
| 7. produce a machine-verifiable erasure report | **DOES NOT EXIST** | No function, format, or test anywhere produces or verifies an erasure report artifact. `ledger_anchor.py`'s anchor mechanism is the closest existing PATTERN (a small, allowlisted, third-party-verifiable record) but is not itself an erasure report and was not built for this purpose. |

**R17's own required per-artifact metadata** (unique artifact ID, separately
controllable DEK, subject/purpose/audience/sensitivity/expiry, lineage, active/
inactive/erased state): `:Fact` nodes already carry most of this in some form
(`fact_id`, `encrypted_dek`, `subject`, `sensitivity`, `derived_from` for lineage,
`valid_to` as a coarse active/inactive signal) — but **no `erased` state exists**
(only active/closed, per R16's own §7.1), and **`purpose`/`audience`/`expiry` are the
SAME absent fields R2/R18/R21/R23 have already been ruled absent for**, D-105/D-130's
own precedent (`purpose_id`, `retention_deadline`/`retention_policy` absent because no
purpose vocabulary or retention mechanism exists) — not re-derived here, cited as the
same, already-established absence.

### Item 3 — THE COMPATIBILITY QUESTION

**Answer: CONDITIONAL, not unconditional — and the condition is a real, load-bearing
design constraint, not automatically satisfied.**

`ledger_anchor.py`'s own compatibility proof (`:36-44`, D-89) rests on ONE specific
fact: **`event_hash()` is computed the identical way for every event, using a FIXED
`_HASH_FIELDS` tuple, and that tuple never includes payload content** — so any
erasure that nulls a non-hashed field leaves `hash`/`prev_hash` (and therefore every
anchor) untouched.

**A naive R16 rebuild breaks this.** If `_HASH_FIELDS` itself is edited to add
`keyed_commitment` and remove `payload_sha256`/`payload_kid` (the obvious first
instinct), `event_hash()` changes for EVERY event uniformly — including the roughly N
historical events already anchored, none of which carry a `keyed_commitment` field at
all. `event.get("keyed_commitment")` would return `None` for them, producing a
DIFFERENT hash than what's stored and anchored. **This would invalidate every anchor
taken to date.** That is the STOP-AND-REPORT scenario item 3 names — but it is not the
only path available, and this survey did not find it to be the FORCED outcome.

**A version-gated rebuild does NOT break it.** The infrastructure to avoid this already
exists, unused: `hel` (the format version tag) is ITSELF one of `_HASH_FIELDS`,
present on every event today (`"1.0"` for all of them). If `event_hash()` is made to
BRANCH on `event.get("hel")` — computing today's `_HASH_FIELDS` set for `hel=="1.0"`
events and a NEW field set for `hel=="2.0"` events — then:
- every existing (`hel=="1.0"`) event's hash computation is byte-identical to today,
  forever; no historical segment is rewritten; every anchor taken against them stays
  valid, unconditionally;
- new events, written under `hel=="2.0"`, use the new commitments-only schema from
  their first day forward.

**This is not this survey asserting the rebuild is safe — it is naming the SPECIFIC
design requirement that makes it safe, which the build must satisfy as its first
segment, before any `hel=="2.0"` event is ever written.** Building the new schema
first and retrofitting version-gating later would risk exactly the scenario item 3
asks to be stopped and reported — so the segmentation in item 4 puts this first,
deliberately, as a hard prerequisite rather than an implementation detail.

### Item 4 — the segmented build (proposed, NOT built)

```
SEGMENT 1 — version-gated event hashing                    [PREREQUISITE, first]
SEGMENT 2 — off-ledger payload store (new, parallel-buildable)
SEGMENT 3 — keyed/salted commitment construction (parallel-buildable)
SEGMENT 4 — wire the v2 writer (commitments + off-ledger store)   [depends on 1,2,3]
SEGMENT 5 — pseudonymize actor.id / payload_kid                [depends on 1; scope TBD]
SEGMENT 6 — per-fact erasure sequence (R17 steps 1-5, 7)        [depends on 4]
SEGMENT 7 — machine-verifiable erasure report + verifier        [depends on 6]
```

**SEGMENT 1 — version-gated `event_hash()`.** Make hashing branch on `event.get("hel")`;
today's `_HASH_FIELDS` becomes the `hel=="1.0"` case, unchanged. No behavior change to
any existing write. Acceptance: every existing test in `test_hel_smoke.py`/
`test_ledger_anchor.py` passes byte-identically; a fault twin proves a synthetic
`hel=="2.0"` event hashes differently than an identical-looking `hel=="1.0"` one.
**This is the segment item 3's compatibility answer depends on — must land first, and
nothing in Segments 2-7 is safe to ship ahead of it.**

**SEGMENT 2 — the off-ledger payload store.** New module: per-member-keyed storage for
what today's `payload_enc` holds, reusing the SAME crypto-shred pattern
`destroy_member_key()` already proves (a fresh per-member key, AES-256-GCM, destroy-key
erasure) rather than inventing a second one. Its own backup/replica story is explicitly
OUT OF SCOPE here — R16's own text calls this "a new off-ledger payload store... none
of which exists today," and this survey found nothing to build it against beyond that.
Independent of Segment 1; can build in parallel.

**SEGMENT 3 — keyed/salted commitments.** A small, focused crypto primitive (HMAC over
the payload, keyed per-member or per-installation) replacing the plain-SHA256 role
`payload_sha256` plays today, closing the dictionary-testing gap R16's own text names.
Independent of Segments 1-2; can build in parallel.

**SEGMENT 4 — the v2 writer.** `_build_event`/`append` gain a `hel=="2.0"` path: write
the payload to Segment 2's store, compute Segment 3's commitment, put ONLY the
commitment + permitted metadata fields inline. `verify()` must handle a chain containing
BOTH `hel` versions side by side (old segments keep old-shape events forever). **This is
the first segment where a NEW event, from the moment it lands, is actually R16-compliant
— but it does not touch existing facts or existing ledger history.** Depends on 1, 2, 3.

**SEGMENT 5 — `actor.id`/`payload_kid` pseudonymization.** The module's OWN docstring
already scopes this as blocked on "registry-level opaque member IDs (one identifier
scheme system-wide)" — a SYSTEM-WIDE identifier change, not a ledger-local one. This
survey recommends treating Segment 5 as its OWN dispatch, possibly its own REQ, rather
than folding it into the R16/R17 sequence — it is a real R16 violation (confirmed above)
but its fix reaches well outside the ledger module, and bundling it risks the rebuild
never landing while waiting on a system-wide identifier scheme. Named, not scoped
further, per this dispatch's own SURVEY-ONLY instruction.

**SEGMENT 6 — the per-fact erasure sequence (R17 steps).** A new function (NOT a
rewrite of `retract_fact`, which is a different operation — stop-reading vs. erasing)
wiring: null `encrypted_dek` (step 2, cheap — the hard infrastructure already exists),
`DELETE` the row where the graph schema allows it (step 3), remove the embedding (step
4), erase the off-ledger payload + append a HEL tombstone reusing Segment 2/4's own
primitives (step 5). Steps 1 and 6 need explicit scoping decisions (see OPEN) rather
than being buildable as stated. Depends on Segment 4 (needs the off-ledger store and v2
writer to exist).

**SEGMENT 7 — the erasure report + verifier.** Closely coupled to Segment 6 — the report
names what Segment 6 actually did (which steps ran, against which artifact, with what
result), verifiable the same way `ledger_anchor.py`'s own allowlisted-field pattern
already works (`ANCHOR_FIELDS`/`FORBIDDEN_ANCHOR_KEYS`, reused as a template, not
duplicated blind).

**Which segment first makes an external deletion claim honest:** **Segment 6**, and
specifically its `encrypted_dek`-destruction sub-step — that is the first point where a
"this fact is gone" claim becomes CRYPTOGRAPHICALLY TRUE rather than "this fact is
hidden from retrieval." Everything before it (Segments 1-5) is necessary
infrastructure; none of it, alone, changes what "erased" means for a live fact.

### Item 5 — the blast radius

**Existing behaviour that changes:** nothing, through Segment 3 — all three are purely
additive/parallel infrastructure. Segment 4 changes what a NEW ledger event looks like
(schema, not behavior any caller observes — `epistemic_record.py`'s own call sites don't
need to change, since `append()`'s signature is unaffected). Segment 6 is the first
segment with an OBSERVABLE behavior change: a fact that goes through the new erasure
path stops existing in Neo4j entirely, where today it merely stops being retrieved.

**Fixtures/tests that break:**
- Segment 1: none expected (byte-identical hashing for existing events) — but
  `test_hel_smoke.py`/`test_ledger_anchor.py` are the acceptance surface and MUST be
  re-run, not assumed.
- Segment 4: `verify()`'s own test coverage needs a genuinely mixed-version chain
  fixture (v1 events followed by v2 events) that does not exist today — a real, new
  fixture to build, not a break.
- Segment 6: `test_structural_refusal.py`'s own anti-vacuity check (cited in D-130's own
  dispatch doc as depending on `ray`/`dad`'s standing fixture facts staying ACTIVE)
  would break if Segment 6's erasure sequence were ever run against a demo fixture fact
  — **the demo seed must never be a target of real Segment 6 erasure**, the same caution
  D-130's own TD-151 fix already established for a different reason (accidental fixture
  erosion via the memory harness). This is a NEW, real risk this survey is naming, not
  one already flagged elsewhere.

**What the demo does differently:** nothing, through Segment 5. Segment 6, if ever
exercised against a REAL member's real fact (not a fixture), makes that fact
permanently gone — this is the intended, correct behavior, but it means Segment 6 is
the first segment for which "run it against the frozen demo or hip-cutover-demo" must
be an explicit, hard refusal, matching this project's own standing rule ("Anything
touching the frozen demo... is the fallback; it is not a lane").

**Destructive-write authorization:** **Segment 6 needs it, explicitly, before it can run
against anything but a fully synthetic/disposable fixture.** `DELETE`ing a Neo4j row and
destroying a per-fact DEK are irreversible by construction — the entire POINT of R17.
Segments 1-5 and 7 are additive (new code, new fields, no deletion) and do not need
destructive-write authorization to BUILD, though Segment 6's own testing will need a
disposable graph, never the shared dev graph's real fixture data, without a separate
authorization for that test run specifically.

## VERIFIED

**Watched, direct:**
- `harness/epistemic_ledger.py` read in full (625 lines), not excerpted from memory —
  `_HASH_FIELDS`, `_build_event`, `destroy_member_key`, `erase_payload`, `verify()` all
  read as complete function bodies.
- `harness/ledger_anchor.py` read in full (206 lines) — the D-89 compatibility proof
  read directly, not summarized from its own docstring's claim alone (cross-checked
  against `epistemic_ledger.py`'s own `_HASH_FIELDS` to confirm the proof's premise
  holds today).
- `harness/extraction_queue.py::retract_fact` read in full — confirmed `SET`, never
  `DELETE`; zero ledger references anywhere in the file.
- `harness/encryption.py`'s DEK scheme read directly — per-fact key generation
  confirmed at the exact cited lines.
- `harness/custody_exit.py`'s re-keying mechanism read at the function-signature level
  (not exhaustively) — enough to confirm its granularity (dyad) and real existence, not
  its every internal behavior.
- `harness/epistemic_record.py::_fact_entry` read in full — the exact payload shape
  reaching the ledger today, not assumed from R16's own text.
- Grep searches for embedding-deletion, backup-scheduling, and erasure-report code:
  each zero-hit result manually reviewed (not trusted from `grep -c`'s exit code alone,
  per this codebase's own standing D-70/D-75/D-88 caution) before being reported as
  absence.
- `docs/reviews/D63...` and §16's own ruling record: re-confirmed no R16/R17 entry
  exists there, matching the "filed, design-ruled, not MET-ruled" framing.

**Reasoned about, not independently re-derived:** the exact wall-clock/engineering cost
of each segment was not estimated — this survey names WHAT each segment must do and
WHY it is ordered where it is, not how long it would take. Segment 5's "system-wide
identifier scheme" scope was characterized from the module's own docstring citation,
not independently scoped by this survey (a real scoping pass for Segment 5 would be
its own dispatch, per the recommendation above).

## HASH

None — survey only, no file outside `docs/dispatches/` was touched, matching the
dispatch's own explicit instruction.

## OPEN

- **D-71's own dispatch doc could not be located**, same missing-citation pattern
  D-157/D-159 found for "D-154." The ruling's substance is fully recorded in R16's own
  text, so this did not block the survey, but is named for the same reason those prior
  gaps were.
- **R17's step 1 ("revoke all active access paths") and step 6 ("schedule backup
  expiry") need explicit scoping decisions this survey did not make**: step 1 because
  today's closest analogue (retrieval filtering) is not the same guarantee as an access
  revocation, and this survey did not design what a real one would look like; step 6
  because no backup system exists in this codebase to schedule expiry against at all —
  that is infrastructure outside the ledger, named as a real dependency, not scoped.
- **Segment 5 (identifier pseudonymization) is recommended as its own dispatch**, not
  bundled into the R16/R17 sequence — a judgment call recorded so it can be
  overruled, not decided unilaterally as final.
- **The demo-seed erasure risk named under item 5 is new** (not previously flagged in
  any prior dispatch this survey found) — worth carrying into whichever dispatch
  eventually builds Segment 6, so the guard is designed in rather than added after an
  incident.
- **This is a survey, not an estimate or a commitment.** No segment was built, timed,
  or started. Bill's decision on sequencing, staffing, or whether to proceed at all is
  not made here.
- **Nothing ruled.**

## RECAP
D-160: surveyed the existing HEL ledger against R16/R17 and found four distinct R16
violations (plaintext `actor.id`, plaintext `payload_kid`, inline ciphertext
`payload_enc`, unsalted commitment hashing) plus all nine of R16's permitted fields
absent by name. Graded R17's seven erasure steps individually: one partially exists
with its hard infrastructure already built (per-fact DEKs), three genuinely don't
exist, three exist as adjacent-but-not-wired mechanisms. THE COMPATIBILITY QUESTION:
CONDITIONAL — a naive rebuild invalidates every anchor taken to date, but a
version-gated `event_hash()` (using the `hel` field already present on every event)
avoids this entirely and is proposed as the mandatory first build segment. Segmented
into 7 ordered/parallel pieces, named which one (Segment 6) first makes a deletion
claim honest and which one (also 6) needs Bill's destructive-write authorization
before it can run against anything but disposable fixtures. Nothing built, nothing
ruled.
