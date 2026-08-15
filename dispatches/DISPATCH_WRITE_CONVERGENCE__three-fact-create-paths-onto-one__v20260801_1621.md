# DISPATCH_WRITE_CONVERGENCE
Status: BUILT
Reconciled-Against: c66d787 (HEAD at gate; D-95 landed mid-dispatch, docs only, no overlap)
REQ: `docs/requirements/REQ_ARCHITECTURE_BOUNDARY__reference-monitor-threat-model-and-contracted-clients__v20260801_0919.md` — step 1 of the D-84 four-step single-writer plan
Dispatch: D-96, 2026-08-01
**Status proposed: NONE. Nothing ruled MET. Steps 2-4 NOT started.**

Gate passed: bill-ai / [REDACTED-MACHINE-NAME] / `~/hip-roadmap` / `roadmap` @ `c66d787`, clean.
(HEAD moved since D-93: a parallel lane landed D-94 — R30 ruled MET, docs only, no overlap.)
`~/hip-vo`, `~/hip-dev`, `~/hip-harness` NOT touched. **Nothing ruled MET.**

Authority: `REQ_ARCHITECTURE_BOUNDARY`. This is **step 1 only** of D-84's four-step plan.
Steps 2–4 (origin vocabulary, caller plumbing, the A10 battery) are NOT started.

---

## STEP 3 DELIVERABLE — the semantic diff, produced BEFORE any change

All three paths were read in full at `c66d787`. The differences fall into two classes:
**(A) shape divergences that are parameterizable** — the same stored bytes can be produced
through one materialization point with per-path parameters — and **(B) policy divergences
that CANNOT be reconciled without a behavior change.** Class B is documented and deferred,
not resolved by choosing.

### The three paths at a glance

| | `store.encode` → `_new_node_props`/`_CREATE_FACT_CQL` | `extraction_queue._write_one` | `consolidate._write_derived_node` |
|---|---|---|---|
| node shape | full 30-property Phase-A schema | **minimal** (~17 properties; no `recorded_at`, `tier`, `salience`, `confidence_log`, `derived`, `migration_status`; **no `write_state` unless parked** — "historical shape", deliberate) | full-ish, hardcoded (`confidence='low'`, `sensitivity='medium'`, `write_state='augment'`, `tier='hot'`, `salience=0.3`, `derived=true`) |
| embedding | **always `None`** ("engine track doesn't embed in Phase A"; `orchestrator.py:274` documents these facts as invisible to embedding retrieval) | **real vector** over subject+predicate | `null` |
| supersession | four lifecycle tx (`supersede`/`augment`/`correct`/`unresolved`); closes with **`closed_reason`** + `superseded_by` | inline close with **`closed_by` + `closed_session`** + `superseded_by`; skipped for MULTI_VALUED or when parked | none — pure CREATE |
| P8 park | `prospective_level(write_state, confidence)` vs head; on regression → `write_state='unresolved'`, **confidence forced `'low'`**, `confirm_when_relevant=true` | incoming hardcoded UNCONFIRMED; on regression → skip close, `write_state='unresolved'`, **extraction confidence KEPT**, no confirm flag | none |
| overrides | MULTI_VALUED, CORRECT-no-target, θ_WRITE, P8 | MULTI_VALUED (as skip-close), P8 | none |
| audit | `encode_audit.jsonl` append | none | none |
| confidence_log | seeded entry | absent | `[]` |
| utterance | encrypted (`driving_utterance_ct/dek`) | absent | `null` (absent) |

### Class B — NOT reconcilable without behavior change (documented, deferred, not chosen)

1. **`write_state` on extraction rows.** `classify_trust_props` (`memory_engine/trust.py:75`)
   classifies `write_state ∈ {supersede, augment, correct}` up the ladder. Extraction rows
   deliberately carry **no** `write_state`, so they classify UNCONFIRMED. Making
   `_write_one` a full `encode()` caller stamps `write_state` on every extraction fact and
   **reclassifies them on the trust ladder**, changing P8 outcomes and the demo ladder.
2. **Embedding.** Full unification either strips vectors from extraction facts (semantic
   retrieval regression) or adds them to encode-written facts (facts that are today
   *documented* as invisible to embedding search become visible). Either direction is a
   behavior change.
3. **Park semantics.** encode forces `confidence='low'` + `confirm_when_relevant=true` on a
   P8 park; `_write_one` keeps the extraction confidence and sets no confirm flag. And
   encode's θ_WRITE low-confidence override has no extraction counterpart. Unifying means
   choosing one policy.
4. **Close vocabulary.** encode closes with `closed_reason`; `_write_one` closes with
   `closed_by`/`closed_session`. `truth_layer/queries.py` consumes **both** vocabularies at
   ~14 sites. Unifying is a data-model decision plus reader updates. (Also outside step 1's
   scope: this is the *close* path, not the *CREATE* path.)
5. **Audit / confidence_log / utterance encryption** are encode-only features. Extending
   them to the other writers is new behavior.

### Why this is NOT a STOP

D-84's step 1 offered two shapes: *"`_write_one` and `_write_derived_node` become `encode()`
callers **(or thin transaction-participants of it)**."* The first shape is blocked by every
item in class B. The second is not: a single materialization function with per-path
parameters reproduces each path's stored bytes **exactly**, because of one Neo4j semantic —

**null-valued entries in a CREATE property map are not stored.** This is not assumed; it is
live-evidenced read-only: `encode`'s props dict has *always* included `valid_to=None`,
`superseded_by=None`, `record_closed_at=None`, `closed_reason=None`, `embedding=None`,
`last_accessed=None` — and the D-93 property-key inventory of the 12 encode-written live
facts shows **none of those keys exist** on any node (28 distinct keys, none of the
always-None ones present). So a caller passing `None` for its historically-absent
properties stores the identical node it stores today.

Convergence target: **one CQL string, one creator function, three parameterizations.**
Supersession, parking, overrides, audit — all stay exactly where they are. That is what
step 1 buys: when step 2 places R10's origin checks at the creator, there is no second
CREATE to bypass them.

---

## What was built

**One materialization point:** `memory_engine/store.py::create_fact_node(tx, props)`.
Derived-from-the-CQL key set (`_FACT_PROP_KEYS` is parsed out of `_CREATE_FACT_CQL`'s own
parameters, so the two can never disagree). It refuses unknown keys — a misspelled property
silently vanishing is how schema drift starts — nulls every omitted key, and **stamps
`sensitivity_registry_version` unconditionally**, so a caller can neither omit nor forge the
R30 stamp.

**Six call sites converged onto it:** encode's four lifecycle transactions
(`_tx_supersede`, `_tx_augment`, `_tx_correct`, `_tx_unresolved`),
`extraction_queue._write_one` (function-level import — store imports this module at top
level, so a top-level import back would be a cycle), and
`consolidate._write_derived_node`. Each passes exactly the properties it historically
wrote and omits the rest. **Supersession, parking, overrides, and audit stay where they
were** — that is the step-1 scope line, and the class-B divergences above are why.

**There is now exactly ONE `CREATE (…:Fact …)` string in production code** (`harness/`,
`memory_engine/`, `server/`, `truth_layer/`) — verified by AST scan, standing as
`test_ceil_conv_exactly_one_fact_create_exists`. The eval/ occurrences are this battery's
own fault twins plus the L7 crypto harness's fixture writer, both excluded with the reason
stated in-file.

## Equivalence proof — a graph copy was ASSESSED and REJECTED; here is what ran instead

D-84 asked for the memory harness AND a before/after diff on a graph copy. The graph-copy
options on this box, assessed at dispatch time rather than assumed:

- **A second Neo4j instance** (the only real "copy" target): **0.07 GB free memory** at
  assessment, docker absent, Neo4j Community is single-database, and `neo4j-admin dump`
  needs the source offline — stopping the dev instance is barred by the standing no-restart
  rules. Booting a second JVM into 0.07 GB risks the OS SIGKILLing the live demo stack —
  TD-129's exact failure mode. **Rejected on those grounds, stated rather than silently
  downgraded.**

What ran instead — three legs, none of them inspection:

1. **Captured-write equivalence (executed, before AND after).** At `c66d787`, before any
   edit, recording doubles drove all three writers and captured the exact CREATE property
   maps — four variants: encode props, `_write_one` unparked, `_write_one` parked (with the
   head-retention assertion), `_write_derived_node`. After the edit, the identical script
   ran again. Result: **ALL FOUR STORED SHAPES BYTE-IDENTICAL** (26 / 14 / 15 / 24 stored
   properties respectively — the shape divergence itself is visible in those counts, and it
   is preserved, not homogenized). The null-drop rule the comparison relies on is
   **live-evidenced, read-only**: encode has always passed `valid_to=None`,
   `superseded_by=None`, `record_closed_at=None`, `closed_reason=None`, `embedding=None`,
   `last_accessed=None` — and 0 of the 12 live facts carry any of those keys.
2. **The captures are now STANDING, not one-off.** The four pre-convergence maps are
   embedded verbatim as fixtures in `eval/test_fact_write_convergence.py`; every harness
   run re-derives the current shapes and asserts byte-identity against them.
3. **The memory harness, before AND after, same env.** Post-change: 13/17, failing
   MEM-115/116/117/118. Then the SAME harness at the pre-change commit via a throwaway
   worktree (`git worktree add /tmp/d96-baseline c66d787`, removed after): **13/17,
   failing the identical four.** The four failures are pre-existing and environmental
   (cross-owner recall audit, Groq-dependent detect_and_apply, a trust-level expectation,
   and the turn-record path — none of them node materialization). Every scenario that
   exercises the converged writers — MEM-100..111, 113: supersede, augment, correct,
   unresolved, consolidation harden/loosen, demote/promote, derived tagging — **passes
   identically before and after. The delta is zero.**

One environmental note for honesty: the first post-change memory-harness attempt hit an
AuthError because I sourced `~/.env.dev` (copying `restart-dashboard.sh`'s pattern), which
carries a stale credential that overrode the working resolution. Re-run with the repo
`.env.dev` only — the pattern every dispatch this session has used. The baseline run used
the same resolution, so the comparison is like-for-like.

## Batteries updated, and why

`test_registry_version_stamp.py` (CEIL-RV) asserted that `_write_one` and
`_write_derived_node` each stamp the version themselves. After convergence they must NOT —
the creator stamps unconditionally. The battery now asserts the two-part invariant that
actually holds: **the creator stamps (constant, never a literal), and the former paths
DELEGATE to the creator.** A path that neither stamps nor delegates writes unmarked facts,
and that is the case the reworked check catches. Its docstring records the D-96 change.

New: `eval/test_fact_write_convergence.py` (CEIL-CONV, 17 cases, 15th standing battery) —
the one-CREATE invariant with fault twin and comment-immunity, the creator's contract
(refuses unknown keys, nulls omitted keys, unforgeable stamp), the four standing
equivalence fixtures with an anti-vacuity case proving they are non-trivial and mutually
distinct, and delegation checks on all six call sites.

## Harness

```
standing batteries (15 files): 218 passed, 9 xfailed   (test_fact_write_convergence.py: 17 new)
== AUDIT:  8/8   == DISC: 1/1   == L7: 27/27
== L7V2:   27/28 (1 opt-in skip)   == SCHEMA: 1/1   == VOICE: 1/1
RATCHET PASS — no scenario regressed vs baseline.   0 scenario FAILs.
```

All five ABSOLUTE checks read individually from the log: **G0 PASS, PSA1 PASS, CTX-STRIP
PASS, LI1 PASS, CS1 PASS.** `--full` not attempted — TD-129's memory guard (0.07 GB free at
assessment makes the refusal certain), as the dispatch anticipated; not fought.
**ORTH-2 fact schema (46 cases) passed** — a write-path change is exactly what that
conformance check exists to catch, and it did not flinch.

Live graph verified untouched after BOTH memory-harness runs: 12 facts, 12 `pre-registry`,
0 memtest leftovers.

## Mid-dispatch note

HEAD moved twice under this dispatch: D-94 (R30 ruled MET) had landed before the gate, and
**D-95 (anchor fetcher spec) landed mid-dispatch while my changes sat uncommitted.** Both
docs-only, committed with explicit pathspecs, zero overlap with the touched files —
verified by diff, and my working tree was intact. Noted because a parallel-lane commit
under a dirty tree is exactly the collision the lock protocol exists for; the lock was
taken before my own INDEX/commit steps, as always.

## What this dispatch did NOT do

- **Steps 2–4 of the D-84 plan** — no origin vocabulary, no caller plumbing, no A10
  battery. A10's xfail stands unchanged (`encode()` still performs none of R10's four
  checks — the checks do not exist yet; step 1 built the place they will live).
- **No policy unification** — the five class-B divergences stand, documented.
- **Ruled nothing MET.**

