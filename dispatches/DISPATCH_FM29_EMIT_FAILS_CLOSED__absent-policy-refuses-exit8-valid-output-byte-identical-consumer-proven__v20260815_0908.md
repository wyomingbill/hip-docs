# DISPATCH_FM29 — `--emit-detect-pattern` FAILS CLOSED: refusal exit 8, valid output byte-identical, consumer proven both directions
Status: BUILT — LANDED
Reconciled-Against: `645f544` (`~/hip-roadmap` @ `roadmap`) — the tree state every twin and proof ran at; this doc and its INDEX/HANDOFF rows land in the following commit
Dispatch: FM 29
Date: 2026-08-15 09:08 (Mountain)
REQ: `REQ_PROCESS_HARDENING_TOOLS` **Amendment 3** (`1d13201`) — landed **BEFORE the code**, per Requirements Discipline item 8
Branch: roadmap · Machine gate `bill-ai` @ `[REDACTED-MACHINE-NAME]` ✓ · Board claim `7128d73` (claim_lane.py scoped claim, first commit)

COMPLETE WITH FINDINGS — 1 ITEM FILED, NOTHING BLOCKING

---

## 1. SCOPE, HELD NARROW

Bill's ruling closes exactly the residual Amendment 2 named: emit-mode joins the fail-closed
predicate. FM 28 is not reopened (its `require_local_policy()` gate is REUSED, one predicate
for all three modes); the city/zoning policy is untouched (verified: `~/.hip-scrub-local`
unmodified this dispatch — same 10 entries, no city-alone entry).

## 2. THE CHANGE (`645f544`)

`scrub.py --emit-detect-pattern` now calls the same `require_local_policy()` the certifying
modes use: absent or no-effective-patterns local policy → **exit 8**, refusal on **stderr
naming every path consulted, stdout EMPTY** (a consumer capturing stdout must never receive
a partial pattern). With a valid policy the code path is unchanged.

## 3. TWIN RESULTS

```
PASS  E1  emit refuses on absent policy (8), stdout EMPTY, paths named
PASS  E1b emit refuses on empty policy (8), stdout EMPTY
PASS  E2  emit with valid policy: exit 0, byte-equal to the table   365B vs 365B
```

E2 is structural byte-compat: the subprocess output is compared against what the REAL
`emit_detect_pattern()` returns in-process for the same policy — the same function, not a
reimplementation. FM 28's F-twins and D1–D3 all still green; **whole tool suite: ALL FIVE
TWINS GREEN.**

## 4. THE BYTE-COMPAT PROOF (captured before/after)

Captured BEFORE any code change, with the real machine policy present, then re-captured
after; `cmp` clean in both scopes:

| scope | pre sha256 | post sha256 | bytes |
|---|---|---|---|
| `docs` | `48076746c164…269b48` | identical | 661 |
| `all` | `aeb00d1c595c…ee0f4d` | identical | 612 |

**BYTE-FOR-BYTE compatible for consumers, exactly as ruled.**

## 5. THE CONSUMER TEST (`push_docs.sh`, both directions)

- **Refusing state — the UNMODIFIED script, run for real:** with the policy unresolvable it
  printed the scrubber's refusal (naming the consulted path), then its own
  `SECRET SCAN UNAVAILABLE — scripts/scrub.py could not emit a pattern. Refusing to push.`
  and exited 1 **in the scan phase, before the subtree split/push — VISIBLE, nothing
  published.** (The script's `$(…) || { refuse }` guard predates FM 29 and did its job.)
- **Valid state — the script's scan phase verbatim, truncated before the split/push:** the
  scan section was proven byte-identical to the live script (diff clean), run against the
  real policy, and reached `Secret scan: clean.` before the deliberate stop. **The
  truncation is stated, not hidden: running the full script force-pushes the public
  mirror, which this dispatch is not licensed to do.**

## 6. THE 1 ITEM FILED — TD-R-197 (found BY the consumer test, not caused by this change)

During the valid-state run the scan printed `grep: empty (sub)expression`. Traced to the
end: **`push_docs.sh`'s own third grep — the exclusion filter — dies on its own multi-line
pattern** (embedded newlines make grep treat each line as a separate pattern; branch lines
ending in `|` become an empty alternative), **and the pipeline's `|| true` swallows the
death, so `HITS` is empty and the script prints "Secret scan: clean." regardless of real
hits.** Measured: stage 1 returns 2,747 candidate lines over `docs/`, stage 2 leaves 2,741,
stage 3 errors (exit 2) and returns nothing. Not caused by FM 29 — the scan input is
byte-identical (§4) — and pre-existing on every mirror push since the exclusion list took
its multi-line shape. **Filed as TD-R-197 (SEC), flagged needs-Bill: until repaired, a
`push_docs.sh` run should be treated as UNSCANNED past its first stage and hand-verified,
the NC 27 discipline.** Fix direction named in the row; fixing needs a REQ and is not this
dispatch's narrow scope.

## 7. CLAIM IMPACT

```
CLAIM IMPACT: none
```

(Detector-feed tooling; no ledger claim's evidence base changed.)

## 8. VERIFIED — what actually ran vs what was reasoned

**Watched run:** pre/post emit captures and `cmp` (both scopes); `scrub.py --self-test` and
the full five-twin suite; the unmodified `push_docs.sh` refusing run; the verbatim-scan-phase
valid run; the three-stage isolation of TD-R-197 (stage counts and exit codes above).
**Reasoned from code:** that no consumer other than `push_docs.sh` invokes
`--emit-detect-pattern` (grepped `scripts/`); that the refusing run's abort point precedes
every write (the split/push section is below the scan in the script and was never reached —
also observed: no "Pushing" line).

**Commits:** claim `7128d73` (claim_lane.py, board row + scope, pushed) · Amendment 3
`1d13201` · code `645f544` · TD-R-197 filing `b35dc4c` · doc+INDEX+HANDOFF (the commit after
this file) · board close (follows). All pushed in this dispatch.
