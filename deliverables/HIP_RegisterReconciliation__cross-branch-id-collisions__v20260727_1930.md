# HIP Register Reconciliation — Cross-Branch ID Collisions

Status: PLAN OF RECORD (Phases 1 and 2 executed; Phase 3 — main-side
citation updates — explicitly scoped in Section 8 below, not done)
Reconciled-Against: roadmap `db445bc` (Phase 1) + this Phase 2 dispatch
(DISPATCH 36); main `d4a8a90` (= `origin/main`, unchanged since Phase 1,
not edited by either phase)
Date: 2026-07-27 19:30 MT (Phase 1); 19:35 MT (Phase 2, this update)

Bill's ruling, adopted unchanged: **roadmap's numbering is authoritative,
because roadmap replaces main.** Main's colliding entries get renumbered
on port. The register verdicts and renumbering map below are exactly as
proposed in the read-only audit that preceded Phase 1; nothing was
revised for either phase's filing.

This document is the full audit, filed as the record Phase 2 executed
against and Phase 3 will execute against next. Phase 1 fixed the two
broken citations already live on roadmap and ported
`HIP_ArchitectureWeaknessRegister` unchanged. **Phase 2 (this update) has
now ported all four colliding entries — main's TD-131 as `TD-136`, D-25 as
`D-29`, D-26 as `D-30`, D-27 as `D-31` — verbatim into roadmap's real
registers, with lineage recorded in each entry, and updated D-28's status
after independently verifying its fix in code.** Main was not edited in
either phase. Every main-side file whose own citations still say the old
numbers is scoped as Phase 3, listed in full in Section 8.

---

## 1. Registers that exist on only one branch

| Register | roadmap | main |
|---|---|---|
| `docs/BACKLOG.md` | yes | yes |
| `docs/techdebt/DEBT_REGISTER` (current, via `LATEST_DEBT.md`) | yes -> `DEBT_REGISTER__v20260727_1731.md` | yes -> `DEBT_REGISTER__v20260712_2300.md` |
| `HIP_DefectRegister__v20260715_1930.md` | yes | yes |
| `HIP_ArchitectureWeaknessRegister` | **NO, as of the read-only audit** — ported to roadmap in this same dispatch, see Section 7 | yes (`v20260722_1536.md` + `LATEST_` symlink) |
| `docs/INDEX.md` | yes | yes |
| `docs/deliverables/MANIFEST.md` | yes | yes |

Before this dispatch, exactly one register was branch-exclusive:
`HIP_ArchitectureWeaknessRegister` (AW-01 through AW-05) existed only on
`main`. It has been ported into `roadmap` as part of this filing (Section
7) — not merging the branches, per instruction, just copying that one
file's content in unchanged and correcting its cross-references.

Process note, not an ID collision but relevant to why comparison is messy:
`main`'s "current" debt register file is still named
`DEBT_REGISTER__v20260712_2300.md` but was edited in place across at
least 8 commits from 2026-07-12 through 2026-07-22 (last: `4390240`, the
TD-131 filing) — never re-cut with a fresh timestamp despite 10 days of
material edits. Its own header ("RECONCILED-AGAINST: session 2026-07-12")
is stale relative to its own last entry.

---

## 2. IDs that exist on both branches with different content — the collision set

### TD-131 (`docs/techdebt/DEBT_REGISTER`)

**roadmap:**
> TD-131 | OPS | **A fresh `git worktree` checkout can't run `eval.harness` without two manual, undocumented steps.** Found building REQ_CRYPTO_P1_DYAD_KEYS (2026-07-20) on a brand-new worktree (`roadmap-crypto-p1`): (1) bare `python3 -m eval.harness` fails inside the harness-owned subprocess server with `ModuleNotFoundError: No module named 'pipecat'` — the project venv is `[REDACTED-USER-PATH]/hip-dev/.venv`, shared across worktrees, but nothing in `eval/harness.py`/the harness server checks or documents this, so a plain `python3` looks like it should work and doesn't; (2) `certs/voice.key` (gitignored, only `voice.crt` is tracked) doesn't exist in a fresh worktree, so the subprocess server fails with `Missing cert/key: .../certs/voice.crt, .../certs/voice.key` even though `voice.crt` IS present — worked around by copying a matching key+cert pair from `hip-dev`'s checkout (confirmed matching pubkey via `openssl x509 -pubkey`/`openssl pkey -pubout`), not by regenerating (which would have produced a mismatched, uncommitted `voice.crt` diff). Fix direction: a `--guards`-time check (mirroring the existing `DEV_MARKER.txt`/`NEO4J_URI` checks in `eval/harness.py:_guards`) that fails loud with the exact fix instead of a bare traceback three layers down. | REQ_CRYPTO_P1_DYAD_KEYS build, 2026-07-20 | OPEN

**main:**
> TD-131 | GATE | **Household facts reach the outbound Groq payload unfiltered on every MID and CORE turn.** Mechanism: `harness/injection_contract.py`'s `_inj4_household` (lines 341-343) admits `owner=="household"` facts unconditionally, before INJ-5's intent gate. `server/voice_orch.py:2603` renders them into the system prompt; that `messages` object passes untouched to `_groq.chat.completions.create()` at line 3314. `strip_context_for_tier` at line 3240 is the only filter before a client call and is gated on `_frontier_strip`, which never fires for MID or CORE. Traced live on both tiers, 2026-07-22: five rows went verbatim — address, zone_district, schedule, trash pickup, and Dad's risk_pattern (elevated fall-risk). Member-owned facts were correctly excluded in the same trace — 8 candidates, 5 admitted, Maya's own appointment and medication and Ray's medication all denied. Not a defect in the sense of broken code — the household exemption (INJ-4) is by explicit design, and member isolation holds. What is unresolved is whether that exemption should extend past the network boundary. Proposed resolution: extend `strip_context_for_tier` to MID and CORE, or accept the exposure and document it as an architecture decision. This is Bill's call, not a session's. | Live trace, run-of-show correction session, 2026-07-22 | OPEN — Bill's decision required

**Verdict: renumber main's entry to `TD-136` on port. Roadmap's TD-131 is untouched.**

**DONE (Phase 2):** filed as `TD-136` in `docs/techdebt/DEBT_REGISTER__v20260727_1935.md`
(`docs/techdebt/LATEST_DEBT.md` repointed there), body verbatim from
main's row above, lineage recorded (original ID, branch, commit
`4390240`) in a bracketed marker at the start of the entry.

### D-24 (`HIP_DefectRegister`) — status collision, not a topic collision

Both branches carry the identical opening text (over-triggering
`medication_status` classification on medication-switch statements, found
2026-07-17). Roadmap's copy ends there: "NOT FIXED — newly found, not
this dispatch's scope to fix." Main's copy has two additional sections
appended after that exact same text: a 2026-07-19 scoping note, and a
**"FIXED 2026-07-21"** resolution citing `REQ_GROQ_MODEL_FIX` and a
`--full RATCHET PASS` verification. Roadmap's own defect register does
not know this defect was closed.

**Verdict: no renumbering needed (same ID, same topic) — this is a
content-staleness gap, not a collision. Flagged for Phase 2 to decide
whether to port main's resolution text into roadmap's D-24 row.**

### D-25 (`HIP_DefectRegister`)

**roadmap** does not carry a `D-25` row in this file at all — it lives in
`docs/dispatches/DISPATCH_D25_REGISTRY_SCOPE__custody-ledger-provenance-fix__v20260721_0636.md`:
registry/ledger custody-count provenance split (`HIP_REGISTRY_DB` pointed
at a shared checkout across worktrees), **RESOLVED** at `605bb79`.

**main:**
> D-25 | **trust_ladder T1 park-write record mislabels `reply_source`.** On the P8-park write path, the user-visible reply is the deterministic `PARKED_UPDATE_REPLY` template (server/voice_orch.py:2301) and `record.park` is SET (non-null) — governance outcome, the model does not phrase it. But the d1.1 record carries `reply_source="model"` and a non-null `inference_ms` (the model WAS called for an ack, then discarded in favor of the park template, and the record kept the model attribution). | Live full-deck trace 2026-07-20 (PID 29496, dev Neo4j :7688) | **OPEN — NOT FIXED this session (report-only trace).**

**Verdict: roadmap's D-25 (external, resolved) stays as-is. Main's D-25 renumbers to `D-29` on port.**

**DONE (Phase 2):** filed as `D-29` in `HIP_DefectRegister__v20260715_1930.md`,
body verbatim, lineage recorded (commit `767517a`).

### D-26 (`HIP_DefectRegister` / `AUDIT_MASTER_KEY_FINDINGS`)

**roadmap** does not carry a `D-26` row in this file — it lives in
`docs/deliverables/AUDIT_MASTER_KEY_FINDINGS__d26-launchd-vs-harness-key-divergence__v20260722_1529.md`:
launchd plist's master-key path diverges from the harness default; two
distinct key files by hash.

**main:**
> D-26 | **Speaker-isolation refusal path is bypassed (not broken — bypassed) by declarative/imperative/role-claiming rewordings, which reroute the turn into an unrelated write-detection gate instead.** Metamorphic test of `speaker_isolation` (Sam querying Bill-owned `(bill,elena,medication)`): of 6 rewordings of the same underlying query, 3 are classified `is_declarative_utterance()==True` and intercepted by `_gate_unconfirmed_update` (the TD-121 F3 gate), which discards the model's actual reply and substitutes the generic `UNCONFIRMED_UPDATE_REPLY` template. No leak resulted, but the *intended* isolation-refusal code path never runs for these three. | Live, `member=sam`, dev Neo4j :7688, 2026-07-21 | **OPEN — NOT FIXED, explicitly report-only.**

**Verdict: roadmap's D-26 (external, security finding with its own audit
doc and citation network) stays as-is. Main's D-26 renumbers to `D-30`
on port.**

**DONE (Phase 2):** filed as `D-30` in `HIP_DefectRegister__v20260715_1930.md`,
body verbatim, lineage recorded (commit `a6620d4`). Its internal
"confirmed LIVE... by D-27 below" self-reference was given a bracketed
gloss (not a rewrite) pointing at `D-31`, main's D-27's new number, so it
doesn't become its own dangling citation the moment it lands next to
roadmap's unrelated, pre-existing D-27.

### D-27 (`HIP_DefectRegister`) — the most direct collision: both branches carry their own literal `D-27` row in the same file

**roadmap:**
> D-27 | **`known_facts` is a second fact-render path that bypasses the injection contract entirely, neutralized today only by a caller convention, not by structural enforcement.** `local_system_prompt`'s "Things you know about this person" section (`harness/orchestrator.py:402-421`) renders straight from whatever `known_facts` list a caller passes: `filter_facts` (permission-only) is the sole gate applied, never `apply_injection_contract`'s subject-resolution/relevance/access-control logic (INJ-1..7). The only reason no un-contracted fact reaches the model through this path today is that the real text-path caller always passes `known_facts=[]` — a call-site discipline, not a structural guarantee. | Confirmed by direct code read; already named as a live, open, un-fixed gap in `REQ_PROMPT_RECORD_FIDELITY`'s own WHAT'S KNOWN BROKEN section. | **NOT FIXED — registered, not built.**

**main:**
> D-27 | **On the REBUILT speaker_isolation script (REQ_SPEAKER_ISOLATION_REBUILD), the INJ-7 structural access-control refusal (T05: Sam asking "What medication is Maya on?") is reached by only 2 of 5 meaning-preserving rewordings of the same query by the same asker.** The other 3 divert to a different mechanism — one of them all the way to a live model-generation call. Query set traced: ORIGINAL and POLITER both hit `path=guard_inj7` correctly; SHORT-IDIOMATIC and SUMMARY both hit `path=guard_empty_set` instead (intent misclassified as `knowledge` not `personal`); PRONOUN ("What medication is she on?") reached `path=generation` — a REAL model call fired, no structural guard at all, "she" never resolved to Maya. | Live, `member=sam`, against `main` `8cbe333`'s shipped script, 2026-07-24. | **OPEN — NOT FIXED, report-only per Bill's instruction. NOT a demo blocker.**

**Verdict: roadmap's D-27 stays (already cross-referenced by the MET
`REQ_PROMPT_RECORD_FIDELITY`). Main's D-27 renumbers to `D-31` on port.**

**DONE (Phase 2):** filed as `D-31` in `HIP_DefectRegister__v20260715_1930.md`,
body verbatim, lineage recorded (commit `720c94c`). Its internal "Same
fix-scope caution as D-26" self-reference was given a bracketed gloss
pointing at `D-30`, main's D-26's new number, for the same reason as
above.

### TD-122 (`docs/techdebt/DEBT_REGISTER`) — minor, same direction as D-24 but reversed

Roadmap's copy has an appended 2026-07-21 re-confirmation paragraph
(root-caused the embedding gap to `harness/fact_change.py`'s migration to
`store.encode()`) that main's copy lacks. Not a topic collision — roadmap
is simply ahead here. **No renumbering; Phase 2 may port the extra
paragraph into main's copy if main content is ever ported back, but that
is out of scope for a roadmap-authoritative reconciliation.**

### `docs/BACKLOG.md` row-keys (its own ordering scheme, a separate ID space from D-/TD-)

- Row **`48`**: roadmap = TD-129 (ollama daemon contention); main = "Deck cross-script state: household-shared only" (no D/TD number).
- Row **`49`**: roadmap = TD-135 ("two local clones... separate INDEX/MANIFEST") — **retargeted to TD-137 in Phase 1, this dispatch, see Section 6**; main = D-26 (speaker-isolation metamorphic test, i.e. main's D-26 above).
- Row **`50`**: roadmap = "Prompt completeness" (cites proposed `REQ_PROMPT_COMPLETENESS`, no D/TD number of its own); main = TD-131 (extend `strip_context_for_tier` to MID/CORE — i.e. main's TD-131 above).

**Verdict: `docs/BACKLOG.md` needs a manual row-by-row reconciliation
pass — explicitly Bill's, not mechanically renumbered by this document.
Not touched beyond row 49 in this dispatch.**

---

## 3. IDs that exist on only one branch, per register

| Register | roadmap-only | count | main-only | count |
|---|---|---|---|---|
| `DEBT_REGISTER` (TD-) | TD-129, TD-130, TD-132, TD-133, TD-134, TD-135 | **6** | (none) | **0** |
| `HIP_DefectRegister` (D-) | D-28 | **1** | D-25, D-26 | **2** |
| `HIP_ArchitectureWeaknessRegister` (AW-) | (was 0, now ported — see Section 7) | **0** | AW-01..AW-05 | **5** |
| `BACKLOG.md` row-keys | 0b, 0c, 37b | **3** | 15c, 51, 52, 53 | **4** |
| `BACKLOG.md` BILL- rows | — | **0** | BILL-7 | **1** |

D-27 and TD-131 are not in this table — they exist on both with
different content, so they're in the collision set (Section 2), not
here. H-01..H-09 and I-01..I-10 (`HIP_DefectRegister`) are identical on
both branches — no divergence found.

---

## 4. Highest ID in use, per register, per branch

| Register | roadmap | main |
|---|---|---|
| `DEBT_REGISTER` (TD-) | **TD-135** (before Phase 1's TD-137 assignment below) | **TD-131** (gap: 129/130 never used on main) |
| `HIP_DefectRegister` (D-) | **D-28** | **D-27** |
| `HIP_ArchitectureWeaknessRegister` (AW-) | n/a before this dispatch | **AW-05** |
| `BACKLOG.md` numeric rows | **50** | **53** |
| `BACKLOG.md` BILL- rows | **BILL-6** | **BILL-7** |

After Phase 1: roadmap's TD sequence highest in use was **TD-137**
(BACKLOG row 49's retargeted reservation, reserved only) with **TD-136**
reserved by the AW register port's cross-reference (also not yet filed).

**After Phase 2 (this update), filed for real:**

| Register | roadmap, post-Phase-2 |
|---|---|
| `DEBT_REGISTER` (TD-) | **TD-137** (`docs/techdebt/DEBT_REGISTER__v20260727_1935.md` holds TD-136; TD-137 remains a BACKLOG-row-49 reservation only, not yet filed). **Next real filing starts at TD-138.** |
| `HIP_DefectRegister` (D-) | **D-31** (D-29, D-30, D-31 now real rows). **Next real filing starts at D-32.** |
| `HIP_ArchitectureWeaknessRegister` (AW-) | **AW-05** (ported unchanged, no new entries added). |

---

## 5. Citations that resolve differently today — confirmed, not hypothetical

**a)** `docs/deliverables/HIP_DefectRegister__v20260715_1930.md`,
`docs/INDEX.md`, and `docs/deliverables/MANIFEST.md` all exist under the
same filename on both branches and all cite D-25/D-26/D-27 — the same
file path resolves to a different defect depending on which branch's
checkout you're standing in.

**b)** **Fixed in this dispatch (Phase 1, Section 6):**
`docs/requirements/REQ_PROMPT_SUBSET_ADMITTED__layer7-prompt-record-fidelity__v20260726_1617.md`
(roadmap-only, filed 2026-07-26) cited `docs/BACKLOG.md:77` and
"TD-131/BILL-7" assuming main's definitions — neither of which resolves
on roadmap (roadmap's `BACKLOG.md` has no BILL-7 row; line 77 is blank;
roadmap's own TD-131 is the unrelated worktree finding). This predates
any session working on the register-collision problem itself — it was
silently broken since the day it was filed.

**c)** **Fixed in this dispatch (Phase 1, Section 6):** same-branch
collision, not cross-branch: `docs/BACKLOG.md` row 49 on roadmap reserved
TD-135 on 2026-07-26 for "two local clones diverge" but never filed it
into the real register; a later session (2026-07-27) filed a real,
unrelated TD-135 (corrupt archived docx) against the register's own
next-available number, since the register had no such row to collide
against — only BACKLOG's forward-reference did.

**d) Still open, not fixed by this dispatch** (out of Phase 1's explicit
scope — porting these entries is Phase 2): every citation of main's
TD-131 (the Groq-payload meaning) outside `docs/techdebt/DEBT_REGISTER`
itself remains pointed at a number that means something else on roadmap,
until Phase 2 ports it as TD-136:
- `docs/BACKLOG.md` (main, row 77, the BILL-7 text itself)
- `docs/requirements/REQ_FRONTIER_LABEL_CONVERSATION_PANE__display-tier-chip__v20260721_1058.md` (main)
- `docs/requirements/REQ_ROUTING_PANE_INFERENCE_MS__replace-class-column-with-inference-ms__v20260722_1934.md` (main)
- `docs/dispatches/DISPATCH_HOUSEHOLD_FACTS_GROQ_PAYLOAD__mid-core-payload-trace-and-followups__v20260722_1647.md` (main)

And every citation of main's D-25/D-26/D-27 remains pointed at numbers
that mean something else on roadmap, until Phase 2 ports them as
D-29/D-30/D-31:
- `docs/deliverables/HIP_DemoScript03_TrustLadder__prep__*.md` (3 versions, main) — D-25
- `docs/requirements/REQ_CORE_BEAT_DETERMINISTIC.md`, `REQ_DEMO_INTEGRITY_BATTERY*.md` (main) — D-25
- `docs/deliverables/HIP_Demo20MinRunOfShow__*.md` (5 versions, main) — D-26
- `docs/dispatches/DISPATCH_ISOLATION_METAMORPHIC__speaker-isolation-reword-fragility__v20260721_1319.md` (main) — D-26
- `docs/deliverables/HIP_Demo20MinRunOfShow__v20260724_1749.md` (main) — D-27

None of these live on roadmap, so none of them are "silently wrong on
roadmap" today — they're main-only documents, correct in main's own
context, that will need updating if/when their content is ever ported
into roadmap under the new numbers. Listed here so Phase 2 has the
complete citation-update list in one place.

---

## 6. Phase 1 actions taken (this dispatch)

1. **`docs/requirements/REQ_PROMPT_SUBSET_ADMITTED__layer7-prompt-record-fidelity__v20260726_1617.md`**:
   appended a CITATION REPAIR note immediately after the dangling
   `TD-131`/`BILL-7`/`docs/BACKLOG.md:77` reference. Original text left
   intact (never overwritten); the note states plainly what the citation
   meant (main's TD-131, the Groq MID/CORE payload finding), confirms it
   is unresolvable on roadmap as written, names the present-day
   roadmap-native pointer (`D-28`) and the future pointer once ported
   (`TD-136`).
2. **`docs/BACKLOG.md` row 49**: `TD-135` retargeted to `TD-137` in the
   row's own title and a RETARGETED note appended explaining why (135
   taken by an unrelated real entry; 136 reserved by this same dispatch
   for the AW-register port's cross-reference). No other row touched.
3. **`docs/deliverables/HIP_ArchitectureWeaknessRegister__v20260722_1536.md`**:
   ported from main `4390240`, AW-01 through AW-05 content byte-for-byte
   unchanged; only the header's own cross-reference paragraph was
   rewritten to name `TD-136` (roadmap's future number for main's TD-131)
   instead of main's `TD-131`, with an explicit note that TD-136 has not
   yet been filed into the real debt register (Phase 2). `LATEST_HIP_ArchitectureWeaknessRegister.md`
   symlink created, matching main's own convention. Registered in
   `docs/INDEX.md` and `docs/deliverables/MANIFEST.md` Section B in the
   same commit as this document.

## 7. Phase 2 actions taken (DISPATCH 36)

1. **`docs/techdebt/DEBT_REGISTER__v20260727_1935.md`** cut (new
   timestamped file, per the Naming Law — the prior file,
   `DEBT_REGISTER__v20260727_1731.md`, is untouched and stays committed
   history unmodified; `LATEST_DEBT.md` repointed to the new file). Main's
   `TD-131` (commit `4390240`) ported as **`TD-136`**, body verbatim after
   a bracketed lineage marker naming the original ID, branch, and commit.
   Roadmap's own `TD-131` was not touched.
2. **`HIP_DefectRegister__v20260715_1930.md`** (edited in place, matching
   how D-24/D-27/D-28 were already added to this same file): main's
   `D-25`, `D-26`, `D-27` (commits `767517a`, `a6620d4`, `720c94c`
   respectively) ported as **`D-29`**, **`D-30`**, **`D-31`**, each body
   verbatim after its own bracketed lineage marker. D-26's and D-27's
   mutual internal cross-references ("D-27 below" / "Same fix-scope
   caution as D-26") were given minimal bracketed glosses pointing at
   their new numbers, so porting them didn't recreate the exact kind of
   dangling/ambiguous citation this whole reconciliation exists to fix.
   Roadmap's own D-25 (external, resolved), D-26 (external, security
   finding), and D-27 (known_facts bypass) were not touched.
3. **`docs/deliverables/HIP_ArchitectureWeaknessRegister__v20260722_1536.md`**:
   confirmed its `TD-136` cross-reference (written in Phase 1 as a
   forward reference) now resolves to a real entry; updated the "not yet
   been filed" disclaimer to say so, and to name that D-28 was fixed for
   its own scope under `REQ_STRIP_CONTEXT_COMPLETENESS` without touching
   TD-136's broader question.
4. **D-28 status update, `HIP_DefectRegister__v20260715_1930.md`**:
   verified independently in code (not assumed from the REQ's existence)
   — see Section 9 for the full verification record — then updated to
   FIXED, citing `REQ_STRIP_CONTEXT_COMPLETENESS` and commits `f2deae1`
   (scope), `95327c0` (fix), `3472d1f` (hard-zero check + fault-injection
   twin). Original "NOT FIXED" text left intact, FIXED update appended,
   same convention as every other status update in this session. Also
   updated D-28's own stale "has not been ported to roadmap's own
   register" clause about TD-131, since it now has been (item 1 above).
5. This document updated throughout: collision-set verdicts (Section 2)
   marked DONE with lineage, highest-ID table (Section 4) updated
   post-port, and this section rewritten from a forward-looking task list
   into a completed action log.

## 8. Phase 3 — main-side citation updates (not done, explicitly scoped, main not touched)

Every file below is **on `main` only**, correct in main's own context
today, and cites one of the four ported IDs by its **old** number. None
of these are "silently wrong" right now — main was not edited by Phase 1
or Phase 2, so main's own citations still correctly resolve *on main*.
They become Phase 3's job only if/when main's content is ever ported
into roadmap, or if main itself is ever updated to adopt the new
numbers — neither decided here, per instruction not to propose merging
the branches.

**Citing main's `TD-131` (now `TD-136` on roadmap):**
- `docs/BACKLOG.md` (main, row 77 — the `BILL-7` row's own text)
- `docs/requirements/REQ_FRONTIER_LABEL_CONVERSATION_PANE__display-tier-chip__v20260721_1058.md`
- `docs/requirements/REQ_ROUTING_PANE_INFERENCE_MS__replace-class-column-with-inference-ms__v20260722_1934.md`
- `docs/dispatches/DISPATCH_HOUSEHOLD_FACTS_GROQ_PAYLOAD__mid-core-payload-trace-and-followups__v20260722_1647.md`
- `docs/deliverables/HIP_ArchitectureWeaknessRegister__v20260722_1536.md` (main's own copy — the ported roadmap copy is already fixed, item 3 above; main's original is untouched and still correctly self-consistent on main)

**Citing main's `D-25` (now `D-29` on roadmap):**
- `docs/deliverables/HIP_DemoScript03_TrustLadder__prep__v20260720_1606.md`
- `docs/deliverables/HIP_DemoScript03_TrustLadder__prep__v20260720_1618.md`
- `docs/deliverables/HIP_DemoScript03_TrustLadder__prep__v20260720_1751.md`
- `docs/requirements/REQ_CORE_BEAT_DETERMINISTIC.md`
- `docs/requirements/REQ_DEMO_INTEGRITY_BATTERY.md`
- `docs/requirements/REQ_DEMO_INTEGRITY_BATTERY__check5-scoped-structural__v20260720_1947.md`

**Citing main's `D-26` (now `D-30` on roadmap):**
- `docs/deliverables/HIP_Demo20MinRunOfShow__v20260721_1832.md`
- `docs/deliverables/HIP_Demo20MinRunOfShow__v20260721_2224.md`
- `docs/deliverables/HIP_Demo20MinRunOfShow__v20260722_1526.md`
- `docs/deliverables/HIP_Demo20MinRunOfShow__v20260724_1132.md`
- `docs/deliverables/HIP_Demo20MinRunOfShow__v20260724_1749.md`
- `docs/dispatches/DISPATCH_ISOLATION_METAMORPHIC__speaker-isolation-reword-fragility__v20260721_1319.md`

**Citing main's `D-27` (now `D-31` on roadmap):**
- `docs/deliverables/HIP_Demo20MinRunOfShow__v20260724_1749.md` (same file as above — cites both D-26 and D-27)

**Also main-side, not yet resolved either way (named in Section 2, not
renumbered — a status gap, not an ID collision):**
- Main's own `D-24` carries a `FIXED 2026-07-21` resolution
  (`REQ_GROQ_MODEL_FIX`) that roadmap's `D-24` row does not have. Porting
  that resolution text into roadmap is a content decision, not a
  renumbering — listed here so it isn't dropped, not because it's part
  of the ID-collision renumbering itself.

**Also still open, entirely separate from the ID work above:**
- `docs/BACKLOG.md` row-by-row reconciliation (rows 48, 50, 15c/0b/0c/37b,
  51-53, BILL-7) — explicitly Bill's, not mechanical, per the original
  audit and both dispatches' own instructions.
- Whether `docs/INDEX.md`/`docs/deliverables/MANIFEST.md` stay
  branch-scoped or need a narrower fix limited to the rows that collide.

No branch merge is proposed or implied anywhere in this document, per
instruction. `main` was not edited by Phase 1 or Phase 2.

## 9. D-28 fix verification (independent, not assumed from the REQ's existence)

A concurrent session shipped `REQ_STRIP_CONTEXT_COMPLETENESS` (`f2deae1`
scope, `95327c0` fix, `3472d1f` hard-zero check) while this reconciliation
was in progress. Instructed to verify the fix in code rather than assume
completeness from the REQ existing. Four independent checks, all this
session:

1. **Read the fix itself** (`git show 95327c0 -- harness/orchestrator.py`):
   `FACT_BEARING_SECTION_HEADERS`, a three-element tuple, is now the
   single source both `local_system_prompt`'s three section-building
   sites and `strip_context_for_tier`'s match regex derive from
   (`_personal_section_pattern()`, built fresh per call, not a
   module-level constant compiled once at import). The old
   `_PERSONAL_SECTION_RE` named only two of three headers by hand; that
   asymmetry is exactly what let the third section escape.
2. **Reproduced D-28's exact triggering shape directly**, live, against
   the current `strip_context_for_tier`: a system prompt whose only
   fact-bearing section is "Confirmed facts about other people" (`mem`
   and `known` both empty). Before the fix this passed through
   unstripped; run against current code, the fact does not appear in the
   stripped output. `facts removed=True` logged.
3. **Regression-checked** the two previously-working sections
   (`mem`-only, `known`-only prompts) against current code — both still
   strip identically, no behavior change.
4. **Ran the real harness**, `scripts/run_harness.sh --layer 7`: `L7:CTX-STRIP
   PASS`; its fault-injection twin `PASS` both directions (red: a
   synthetic fourth section not yet in `FACT_BEARING_SECTION_HEADERS`
   survives stripping, proving the check can fail; green: adding it to
   the tuple strips it cleanly); full `RATCHET PASS`, exit 0.
5. **Confirmed scope**: `git diff f2deae1..3472d1f -- server/voice_orch.py`
   is empty — no new `strip_context_for_tier` call site was added for
   MID/CORE tiers, so `TD-136`'s own broader "should the household
   exemption extend past the network boundary" question is genuinely
   untouched by this fix, not quietly resolved as a side effect, matching
   the REQ's own stated CONSTRAINTS.

**Verdict: FIXED, D-28's own scope, complete.** Nothing remains open in
D-28's own scope. `TD-136` (the broader MID/CORE tier-gating question) is
a separate, deliberately out-of-scope item and remains OPEN.
