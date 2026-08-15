# DISPATCH_MISFILED_INDEX_ROWS_SWEEP
Status: BUILT
Reconciled-Against: 2026-08-05 (D-R-190; parent `12857bc`)

**TYPE:** BUILD (docs only — 54 `docs/INDEX.md` rows relocated between two tables in the
same file, one annotation added. No code, no graph, no harness, no row text edited.)

**REQ:** NONE — process/documentation fix (Requirements Discipline item 10). This is the
half of TD-R-164 that D-R-184 deferred.

## THE ASK

```
=== D-R-190 | ~/hip-roadmap, Lane B worktree | Sweep the 54 misfiled INDEX rows ===
STANDARD PREAMBLE. Temp branch, remove worktree after. The anchor fix landed at
D-R-184 and survived its first live banking, so the sweep can no longer be undone by
the next writer. Move all 54 to the dispatches section, verify counts per section
before and after, annotate the move once. Repo lock held for the whole edit — this is
the one case that needs it. Rule nothing. Report SHORT.
```

## WHAT WAS DONE

1. **Machine gate** at `~/hip-roadmap` (`bill-ai` / `[REDACTED-MACHINE-NAME]` /
   branch `roadmap` / HEAD `12857bc`, in sync with `origin/roadmap`), then Lane B set up
   as a fresh worktree at `~/hip-roadmap-d190` (branch `d190/index-row-sweep`, off
   `roadmap` `12857bc`) — the D-R-184/D-156 shape.

2. **Scope confirmed against the file before anything was written.** Every row in the
   `requirements/` section whose *file path cell* begins with `dispatches/`: **54**,
   matching the count carried in the ask and in TD-R-164. The sweep refuses to run on any
   other number — the count is a precondition inside the script, not an observation made
   afterwards.

3. **The move is mechanical and self-verifying.** A single script (a) lifts the 54 rows
   verbatim, (b) deletes them from the `requirements/` table, (c) appends them, in their
   existing relative order, after the last row of the `dispatches/` table, and (d) refuses
   to write anything unless four checks pass on the produced text: per-section row counts
   move by exactly -54 / +54 and every other section by 0; each moved row appears exactly
   once in the whole file and inside `dispatches/`; zero `dispatches/`-path rows remain in
   `requirements/`; and the sorted multiset of all non-blank lines gains exactly one line
   (the annotation) and loses none. That last check is what proves the rows were *moved*
   and not retyped — no cell of any row can differ by a byte and still pass it.

4. **Annotated once**, in the `dispatches/` section's own prose, immediately above the
   table: what moved, where from, why it was there (TD-R-164), that the text is verbatim,
   that the block was appended rather than interleaved so nothing already in the table
   changed position, and that the block's internal order is accretion order preserved as
   evidence — not a sort being asserted.

5. **Repo lock held for the whole edit**, per the ask: `scripts/hip_lock.py with repo`
   wrapped ONE guarded child that did worktree creation → sweep → registration row →
   commit → push → hash backfill → push → worktree removal. All survey, reading and
   drafting happened UNLOCKED beforehand (preamble item 9 — the lock never wrapped a
   sleep or a think).

## COUNTS — verified before and after, every section

| section | rows before | rows after | delta |
|---|---|---|---|
| `## requirements/` | 118 | 64 | **-54** |
| `## dispatches/` | 59 | 114 | **+54 moved, +1 this dispatch's own row** |
| every other section (17 of them, incl. both `## deliverables/`) | — | — | **0** |

After the sweep the `requirements/` table holds 64 rows: 61 with `requirements/` paths
and the 3 non-dispatch anomalies listed under FINDINGS, which were left exactly as found.

## THE 54 ROWS MOVED

Line numbers are positions in the pre-sweep file at `12857bc`. All 54 now sit in the
`dispatches/` table, in this order.

 1. L93 — `DISPATCH_COMPLETION_ALERT__script-owns-the-sound-and-its-limits__v20260804_1123.md + scripts/dispatch_done.sh`
 2. L94 — `DISPATCH_R23_PURPOSE_TRIGGER__schema-and-notlist-guard-built-module-direct-not-creator-path__v20260804_0659.md`
 3. L95 — `DISPATCH_INDEX_SWEEP__fourteen-dispatch-docs-registered-mechanism-proposed__v20260804_0722.md`
 4. L96 — `DISPATCH_CEILING_STATUS_RUNNER_CHECK__live-rows-verified-against-real-runners__v20260804_0604.md`
 5. L97 — `DISPATCH_R24_SURVEY__stopped-no-material-circumstance-vocabulary-exists__v20260804_0616.md`
 6. L98 — `DISPATCH_R2_SCOPE_RULING__not-met-self-expanding-inference-absence-transient-reasoning__v20260803_1924.md`
 7. L99 — `DISPATCH_R8_R10_RULINGS__silent-absorption-not-met-and-preamble-currency__v20260803_1932.md`
 8. L100 — `DISPATCH_30__write_rule_ruling-and-mutation-burndown__v20260727_1926.md`
 9. L101 — `DISPATCH_39__land-observation-custody-positions__v20260727_1945.md`
10. L102 — `DISPATCH_43__ratify-observation-perception-custody__v20260727_2104.md`
11. L103 — `DISPATCH_D03__demo-cutover-consent-check-graph-pin__v20260728_1955.md`
12. L104 — `DISPATCH_D23__curator-stage1-learner-isolation-gate__v20260729_1316.md`
13. L105 — `DISPATCH_D25__learner-isolation-adversarial-battery__v20260729_1511.md`
14. L106 — `DISPATCH_D30__learner-isolation-provenance-authenticity-fix__v20260729_1628.md`
15. L107 — `DISPATCH_ENVDEMO_AND_MEM118__tracked-config-hazard-fixed-p8-monotonicity-traced__v20260804_0528.md`
16. L108 — `DISPATCH_LOCK_ENFORCEMENT_SURVEY__td148-graph-inventory-and-enforcement-options__v20260803_2047.md`
17. L109 — `DISPATCH_R8_REPRESENTATION_CLASS__survey-only-stopped-on-unreconciled-tree__v20260803_1617.md`
18. L117 — `DISPATCH_DIGEST_AND_HANDOFF_CURRENCY__week-of-0804-and-current-state__v20260804_0639.md`
19. L118 — `DISPATCH_BANK_AND_FILE__review-already-banked-two-tds-filed__v20260804_0621.md`
20. L139 — `DISPATCH_DEMO_GRAPH_SEPARATION__v20260721_1721.md`
21. L160 — `DISPATCH_CEILING_WIRING__twelve-writable-rows-wired-a11-respecified__v20260801_1240.md`
22. L161 — `DISPATCH_CEILING_ACCEPTANCE_AUDIT__three-of-thirty-wired-a7-landed-a11-stopped__v20260801_0930.md`
23. L162 — `DISPATCH_R18_CASCADE__derived-from-invalidation-on-retraction__v20260801_0755.md`
24. L163 — `DISPATCH_LOCK_AND_GRAPH_BUILD__flock-resource-keyed-and-failclosed-target__v20260803_2113.md`
25. L164 — `DISPATCH_CEILING_STATUS_BOARD__derived-matrix-history-and-antivacuity__v20260804_0544.md + scripts/ceiling_status.py + **docs/status/CEILING_STATUS.html**`
26. L165 — `DISPATCH_A2_A8_ROWS__written-run-and-retiered-live__v20260803_1943.md`
27. L167 — `DISPATCH_TD140_RECOMPUTE__stopped-recompute-requires-a-model-call__v20260802_0639.md`
28. L169 — `DISPATCH_TD141_SEED_LINEAGE__the-derived-fact-that-never-was__v20260802_1222.md`
29. L170 — `DISPATCH_MEM_BASELINE_REPIN__repin-13-15-and-file-mem116-staleness__v20260802_1610.md`
30. L171 — `DISPATCH_MEM115_TRACE__structural-not-flaky-contract-never-sees-member-private__v20260802_2105.md`
31. L172 — `DISPATCH_TD140_RULING__recompute-clause-removed-invalidate-only__v20260802_2112.md`
32. L173 — `DISPATCH_R18_MET__ruling-enacted-with-three-absences__v20260802_2205.md`
33. L174 — `DISPATCH_TRUST_MARKER_PORT__hip-vo-caveats-onto-roadmap-rungs__v20260803_0525.md`
34. L175 — `DISPATCH_HEADER_MISLABEL__stopped-strip-pattern-derives-from-the-text__v20260803_0629.md`
35. L176 — `DISPATCH_HEADER_RENAME__req-revision-eight-sites-one-source__v20260803_0753.md`
36. L177 — `DISPATCH_RULING_D118__req-revision-met-l6-red-filed-td147__v20260803_0858.md`
37. L178 — `DISPATCH_TD147_HANDOFF__zero-changes-not-timeout-restatement-class-lock-td148__v20260803_1027.md`
38. L179 — `DISPATCH_STRUCTURAL_REFUSAL_TRACE__resolution-blindness-not-admission-suppression-rows-added__v20260803_1136.md`
39. L180 — `DISPATCH_STRUCTURAL_REFUSAL_FIX__graph-wide-resolution-split-sets-admitted-keying__v20260803_1300.md`
40. L181 — `DISPATCH_RULING_D128__structural-refusal-met-td150-updater-hazard__v20260803_1332.md`
41. L182 — `DISPATCH_RULING_D129__four-rulings-preamble-destaled-fifth-flag__v20260803_1329.md`
42. L183 — `DISPATCH_RESIDUALS_D141__chat-handoff-superseded-exemption-ruled__v20260803_1613.md`
43. L184 — `DISPATCH_HANDOFF_AND_STANDING_RULES__state-doc-preamble-preauth-digest__v20260803_1602.md`
44. L185 — `DISPATCH_REPORT_ROUTING__short-to-terminal-long-to-dispatch-doc__v20260803_1506.md`
45. L186 — `DISPATCH_REPORTING_PROTOCOL__status-query-exception-reporting-live-handoff__v20260803_1503.md`
46. L187 — `DISPATCH_RULING_D131__preamble-pointer-shape-count-deleted__v20260803_1348.md`
47. L188 — `DISPATCH_R2_INFERENCE_PERMIT__typed-permit-build-and-ray-fixture-td151__v20260803_1504.md`
48. L189 — `DISPATCH_A10_BATTERY__step4-a10-wired-a1-false-red-stopped__v20260801_1854.md`
49. L190 — `DISPATCH_WRITE_ORIGINS__origin-vocabulary-and-failclosed-plumbing__v20260801_1652.md`
50. L191 — `DISPATCH_WRITE_CONVERGENCE__three-fact-create-paths-onto-one__v20260801_1621.md`
51. L192 — `DISPATCH_R30_ITEM5__registry-version-stamp-and-pre-registry-backfill__v20260801_1535.md`
52. L193 — `DISPATCH_A12_RULING__fix-the-code-not-the-rule-r30-build-stopped__v20260801_1524.md`
53. L194 — `DISPATCH_DOC_CLEANUP__stale-claim-audit-and-unchained-verification-rule__v20260801_1438.md`
54. L195 — `DISPATCH_ANCHOR_EMITTER__local-drawer-pull-not-push__v20260801_1430.md`

## FINDINGS — recorded, not ruled on, not acted on

1. **The 54 were NOT one contiguous block.** D-R-184's own dispatch doc records them as
   "55 hits, all contiguous, immediately after the requirements/ table's own template
   row, in newest-first order (D-R-178 at the top, D-90 at the bottom)". At `12857bc`
   they sit in **six clusters** — L93-109, L117-118, L139, L160-165, L167, L169-195 —
   interleaved with genuine `requirements/` rows (REQ_DEMO_CUTOVER, REQ_VOICE_DEMO,
   REQ_HARNESS, REQ_CRYPTO_P2/P3, REQ_CONFIDENCE_DISCIPLINE, REQ_DEMO_WEB_REPLAY,
   REQ_STRUCTURAL_CEILING and others). The distinction matters to the root cause: a
   single contiguous run reads as ONE wrong insertion point used repeatedly, while six
   clusters read as the ambiguous anchor resolving to *different* wrong lines at
   different times — which is the stronger version of TD-R-164, not a weaker one. Nothing
   in this dispatch depends on which reading is right; the correction is recorded because
   the earlier count was published and this sweep is the first thing to re-walk it.

2. **The mirror-image misfile exists and was left alone.** One row with a
   `requirements/` path sits inside the `dispatches/` table:
   `requirements/REQ_CHECKLIST_GENERATION__td133-item1-template-generation__v20260726_1226.md`
   (L240 pre-sweep). It is outside the stated scope of "the 54", and moving it is a
   judgement call of exactly the class the ask forbids here.

3. **Two other categories are misfiled into `requirements/` as well**, also left as
   found: `design/DESIGN_LEDGER_ANCHOR__detectability-not-resistance__…` and
   `design/DESIGN_EARNED_CALIBRATION__validated-correctness-not-…` (L196, L197), plus one
   row whose file cell is not a single path at all —
   `docs/techdebt/LATEST_DEBT.md (TD-139) + eval/test_lineage_block.py` (L168), which no
   category anchor can route because it names two files in two categories.

4. **Ordering inside the moved block is accretion order, not chronological.** The 54 span
   2026-07-21 to 2026-08-04 and are not sorted among themselves; the `dispatches/` table
   they joined is itself only newest-first for its top ~14 rows and accretion-ordered
   below that. Appending preserved both orders exactly and moved nothing that was already
   there. Interleaving all 54 by date would have rewritten the position of most rows in
   the table — a bigger change than the one that was asked for, made on a sort the file
   does not actually maintain.

## WHAT WAS NOT DONE

- **Nothing ruled.** TD-R-164 is NOT marked RESOLVED by this dispatch — the sweep it
  deferred is now done, but declaring the debt closed is Bill's call.
- **No row text was edited** — not a subject, not a status, not a reconciled-against
  cell. The multiset check in step 3 is the proof.
- **The four anomalies under FINDINGS were not touched.**
- TD-R-165 (two sections headed `## deliverables/`, which the D-R-184 anchor does not
  disambiguate) is untouched and still OPEN.

## HASH

`06f3b37` — the sweep commit, made on Lane B worktree branch `d190/index-row-sweep`,
fast-forwarded onto `roadmap` and pushed to `origin/roadmap` inside the same locked
run. Filled in by a same-session follow-up edit after the commit landed, per the
established convention. Contains exactly two files: `docs/INDEX.md` (54 rows moved
between two tables, one annotation, one registration row) and this dispatch doc.

## OPEN

- **Does this close TD-R-164?** The deferred sweep is complete; the register entry still
  reads OPEN. Bill's call, not a session's.
- **The mirror-image row (finding 2) and the three non-dispatch rows (finding 3)** are
  filed and unaddressed. They are small, but each one is another instance of the same
  anchor ambiguity, and one of them (finding 3's two-file row) cannot be fixed by any
  anchor rule at all.
