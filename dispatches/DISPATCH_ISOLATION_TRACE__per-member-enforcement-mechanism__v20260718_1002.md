# DISPATCH_ISOLATION_TRACE
Status: BUILT
Reconciled-Against: main (post 33049a4, frontier-tier build landed same session per docs/BACKLOG.md update)

**TYPE:** ANALYSIS

**REQ:** NONE. Read-only code trace, no code touched. Answers "how is
per-member isolation actually enforced," not a build.

## THE ASK

Bill's words, verbatim:

> "ANALYSIS ONLY. How is per-member isolation actually enforced? A
> technologist will ask 'how do you know there's no leakage between
> members,' and I need the mechanism from the code, not the design doc.
>
> Trace and report with file:line:
> 1. When Sam queries, where is the candidate fact set built, and what
>    scopes it to Sam? Is it a decrypt that fails for facts he doesn't own,
>    or a filter applied after retrieval? Those are very different security
>    claims.
> 2. Per-member envelope encryption: where is the data key wrapped/unwrapped,
>    and does unwrapping actually require the querying member's key? Or is
>    there a household master key that could decrypt anything?
> 3. G2 (no-cross-owner-admit) reads near-zero always. Is that because
>    cross-owner admission is structurally impossible (strong), or because
>    the check is looking in the wrong place (vacuous)? Prove which.
> 4. Is there ANY path where two members' plaintext facts coexist in the
>    same model context on the same turn? The household-shared facts
>    (zone_district, schedule) are shared by design — I mean member-private
>    facts.
>
> If isolation is enforced by construction, show the construction. If it's
> enforced by a filter that a bug could bypass, say so. Do not assert it's
> safe."

## WHAT WAS DONE

1. Checked `docs/dispatches/` and `docs/research-technical/` for prior
   tracing of envelope encryption / G2 / owner-scoping — found none that
   trace the actual code path end to end (the defect register's I-07 and
   TD-101/D-10 entries assert conclusions but don't cite the mechanism).
2. Read `harness/encryption.py` in full — the envelope-encryption module.
3. Traced retrieval: `harness/extraction_queue.py:read_user_facts` and
   `:search_facts_by_embedding`, then their callers in
   `harness/orchestrator.py` (`retrieve`, `local_system_prompt`).
4. Traced admission: `harness/injection_contract.py:apply_injection_contract`
   and each `_inj*` predicate it calls.
5. Traced the live call site in `server/voice_orch.py` (`process_text_query`
   → `TurnOrchestrator.decide` → `.retrieve` → `apply_injection_contract`)
   to confirm the trace matches the actual production path, not just a
   test harness path.
6. Read `eval/oracle/record_invariants.py`'s G2 check directly against what
   `admitted[]` actually is (the same `InjectionResult.allowed` from step 4).
7. Checked identity binding upstream of all of the above: `/api/text-query`
   (`server/demo_dashboard.py:1601`) and the voice path's `SpeakerVerifier`
   (`harness/speaker_id.py`).
8. Checked for any code path that queries Neo4j by `subject` rather than
   `owner` and is reachable from a live API (`truth_layer.queries.believed_state`/
   `correction_history`/`provenance`) — confirmed these are eval-harness-only,
   not wired to any live endpoint.
9. Read every `/api/*` route in `server/demo_dashboard.py` that touches
   `:Fact` nodes or ciphertext, to check for a retrieval path that bypasses
   owner-scoping entirely.

## WHAT WAS FOUND

Full answer given to Bill in-conversation with file:line citations for all
four questions. Headline findings, not repeated in full here:

- **Isolation on the live chat path is filter-enforced, not
  decrypt-enforced.** The Cypher `WHERE (f.owner = $owner OR f.owner =
  'household')` in `read_user_facts` (`harness/extraction_queue.py:726-727`)
  and `search_facts_by_embedding` (`:800-802`) is the actual boundary — a
  fact belonging to another member never enters the candidate list at all.
  Decryption (`harness/encryption.py:117-123`) happens AFTER that filter and
  succeeds for any owner string passed to it — it enforces nothing on its
  own.
- **There is a de facto master key.** `harness/encryption.py:79-92`
  deterministically derives every owner's Fernet key from one root secret
  via HKDF. Anyone holding the master key (the server process, always) can
  derive any member's key by calling `_derive_key(owner)` with a different
  string. Confirmed live and exploitable, not just theoretical:
  `server/demo_dashboard.py:212-266` (`/api/facts` + `/api/decrypt`) is an
  unauthenticated, unscoped pair that returns every member's ciphertext and
  decrypts any of it on request — this is TD-101/D-10's territory, now
  traced to the exact mechanism that makes it a full bypass, not a
  narrow one.
- **G2 is structurally near-vacuous, and INJ-3 has one dead branch, both
  for the same reason.** `eval/oracle/record_invariants.py:94-100` checks
  `admitted[]`, which is the *output* of `apply_injection_contract`, which
  itself only ever receives an already-owner-scoped `facts` list (see
  above). `INJ-3`'s `subject == requester` permit branch
  (`harness/injection_contract.py:337-338`) can only matter for a fact
  whose `owner != requester`, but such a fact is never fetched by
  `read_user_facts`/`search_facts_by_embedding` in the first place under
  the current retrieval architecture — so that branch is currently
  unreachable in the live path. Confirmed by reading the retrieval WHERE
  clause and the INJ-3 predicate together, not asserted.
- **Identity binding upstream of all of this is not uniform.** The voice
  path binds `member_id` via `SpeakerVerifier` (`harness/speaker_id.py`,
  thresholds at `:75`) — itself measured weak per TD-127 (0.632-0.677
  against the 0.50 "medium" threshold). The text path
  (`server/demo_dashboard.py:1601-1612`, `/api/text-query`) takes `member`
  as a raw client-supplied string checked only for registry membership —
  no session, password, or biometric check at all. The owner-scoping filter
  is only as trustworthy as this identity claim; on the text path it's
  entirely client-asserted.

## VERIFIED

- **Watched run:** none — this is a static code trace, not a live-turn
  observation. No claim here should be read as "observed running," only
  as "read directly from the cited file:line."
- **Reasoned about:** the entire mechanism, traced hop-by-hop through the
  actual call graph (retrieval → injection contract → prompt assembly) and
  cross-checked against the live server's own call site
  (`server/voice_orch.py:2400-2432`), not just the design docs or the
  defect register's own summaries of it. Where the register's prior claims
  (I-07: "G2 is near-vacuous... structurally impossible") were confirmed
  by this trace, that's noted as confirmation, not fresh discovery; where
  this trace found something the register didn't state as precisely (the
  INJ-3 dead branch, the `/api/facts`+`/api/decrypt` full-bypass mechanism,
  the text-path identity-binding gap), that's flagged as new.

## HASH

NONE. Analysis only, no code changed, no doc other than this dispatch and
the in-conversation report was produced.

## OPEN

- **The `/api/text-query` identity-binding gap (no session/auth binding the
  `member` field to the actual caller) is not the same defect as D-10/
  TD-101b (`/api/decrypt` unauthenticated) — it's a distinct gap in the
  same family (dashboard endpoints trust client-supplied identity/scope
  with no verification).** Not currently its own ID in the defect register
  or `docs/BACKLOG.md`. Flagged here rather than silently folded into
  TD-101's existing "unauthenticated dashboard endpoints" language, since
  TD-101 as written doesn't name this specific mechanism (impersonation via
  the `member` field, not just an open endpoint). Whether it gets its own
  ID is the defect register's call, not this dispatch's — this is
  analysis-only per Bill's instruction.
- **INJ-3's dead `subject == requester` branch is not a bug** — it's inert
  under the current architecture, not exploitable, and may become live if
  retrieval is ever changed to fetch by subject as well as owner (e.g. for
  a future caregiver-authority build, TD-110). Worth re-checking this
  finding specifically if TD-110 ever ships, since that's exactly the kind
  of change that would reactivate this branch.
- **This trace covers the live chat path and the dashboard's fact/decrypt
  endpoints. It does not cover `truth_layer.queries.believed_state`/
  `correction_history`/`provenance`** beyond confirming they're not
  currently wired to any live endpoint — if a future epistemic-timeline UI
  build (`design/HIP_DESIGN__fact-timeline-viewer-investigation`) wires
  `/api/fact_history` to `believed_state`/`correction_history`, those
  queries have NO owner filter in their Cypher today
  (`truth_layer/queries.py:329-357`) and would need one added, not assumed
  present, before going live.
