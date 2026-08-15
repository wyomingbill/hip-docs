# DISPATCH_FM28 — THE SCRUBBER FAILS CLOSED: `~/.hip-scrub-local` created, certification refuses without it, policy recorded verbatim
Status: BUILT — LANDED
Reconciled-Against: `0c8d611` (`~/hip-roadmap` @ `roadmap`) — the tree state every twin ran at; this doc and its INDEX/HANDOFF rows land in the following commit
Dispatch: FM 28
Date: 2026-08-15 08:49 (Mountain)
REQ: `REQ_PROCESS_HARDENING_TOOLS` **Amendment 2** (`c1ed599`) — landed **BEFORE the code**, per Requirements Discipline item 8
Branch: roadmap · Machine gate `bill-ai` @ `[REDACTED-MACHINE-NAME]` ✓ · Board claim `48fa623` (claim_lane.py scoped claim, first commit)

COMPLETE WITH FINDINGS — 1 ITEM FILED, NOTHING BLOCKING

*(Corrected in place by FM 28 itself, pre-authorized own-report correction class: this line
first read "ALL SEGMENTS COMPLETE — NOTHING NEEDS BILL", which was FALSE by the exception
rule's own test — §5's emit-mode/push_docs fail-closed question is an unresolved question
referred for a ruling. Filed, not blocking; the segments themselves are all complete.)*

---

## 1. WHAT THIS FIXES, AND WHY NOW

NC 27 shipped round 3 **hand-verified** and filed the near-miss (§4.2): `scrub_patterns.py`
reads personal PII patterns from an untracked `.hip-scrub-local`, the file did not exist on
this machine, so `local_entries()` returned `[]` and the tool's household-address class was
EMPTY — *"a session that trusted the tool would have shipped the address."* NC 27 referred
the direction; **Bill ruled it, and ruled BOTH halves**: create the file AND make the tool
refuse. This dispatch is that tooling fix. NC 27 §5's separate referral is ruled in the same
breath: **city-only and zoning-district references STAY.**

## 2. S1 — `~/.hip-scrub-local` CREATED (0600), every value enumerated, none invented

| | |
|---|---|
| **Path** | `~/.hip-scrub-local` — HOME, machine-local, untracked, outside every checkout |
| **Mode** | `0600` (`-rw-------`), written under `umask 077` |
| **Entries** | **10** usable entries across 6 classes (counts only here — values never enter a tracked file, the same discipline `scrub_patterns.py`'s own header states) |

**Provenance, per entry, recorded inside the file itself:** every value comes from the two
shipped packages' redaction records —

- **[R3]** `HIP_REVIEW_governed-voice-round3_946753b_SCRUBBED.zip` diffed file-by-file
  against the tree at `946753b`: **14 substitutions across 12 files recovered, reconciling
  NC 27 §3.3's table exactly** (tailnet-address 4, lan-address 3, tailnet-domain 1,
  tailnet-host 1, home-address full+city 3, home-address full 2).
- **[FM 5]** DISPATCH_FM5 §3.1's enumeration over the three 2026-08-14 zips (one tailnet
  address, one tailnet hostname — embedding the machine and tailnet names, its own note —
  one LAN address, the voice certificate's CN).

Classes: the household address in NC 27's hand-enumerated variant set (full+city,
street-only, `Street` spelling, suffix-less, line-wrapped via `\s+`, URL-encoded — the §4.1
cover-page variant); the tailnet name bare; the machine hostname with/without `.local`, any
casing; the concrete tailnet host address; the two LAN hosts; user-specific material
(home-directory path prefix, ssh `user@` form) per Bill's policy line. **No city-alone
entry, by the same ruling.**

## 3. S2 — FAIL CLOSED, twins both directions

`scrub.py` gains exit code **8** and `require_local_policy()`: the certifying modes
(`--check`, `--scrub`) refuse before touching a file when `local_policy()` resolves no
usable entries. The refusal names every path consulted and the ruling. Resolution chain:
`$HIP_SCRUB_LOCAL` (authoritative when set — a deliberately set path that is missing
REFUSES rather than silently falling through), else `~/.hip-scrub-local`, else the legacy
`<repo>/.hip-scrub-local`. `--emit-detect-pattern` is deliberately NOT widened (§5).

**Twins (committed, hermetic — fixture policy via `$HIP_SCRUB_LOCAL`, synthetic value):**

```
PASS  F1  absent policy refuses BOTH certifying modes (exit 8)   check=8 scrub=8
PASS  F1b empty policy refuses (exit 8)
PASS  F2  present policy detects (7) then scrubs+verifies (0)
PASS  F3  machine-local default policy present, entries >= 1     10 entrie(s), count only
```

Existing acceptance UNCHANGED and green (D1/D2/D3 now carry the fixture policy env
explicitly). **Whole tool suite: ALL FIVE TWINS GREEN** (claim_lane, register_doc,
lane_preflight, lane_preflight_busy, scrub).

**Live, on this machine, un-committed (the "NC 27 address forms are caught" direction):**
a scratch file carrying all six real variant forms, run against the real
`~/.hip-scrub-local` — `--check` exit **7** with three home-address classes hit; `--scrub`
exit **0**, **6/6 substitutions, zero residual against the written file, no address text
remaining** (class names and counts only in this record; the scratch file was 0600 in the
session scratchpad).

## 4. S3 — BILL'S REDACTION POLICY, RECORDED VERBATIM

In `scripts/scrub_patterns.py`'s module doc (the table both consumers read), verbatim:

> city-only and zoning-district references STAY (test semantics needed for review);
> actual private-network identifiers, hostnames, credentials, precise private
> addresses, machine/user-specific material are scrubbed.

With the standing note that widening or narrowing this policy is a ruling, not a session
judgement — the same discipline NC 27 §5 applied when it referred rather than scrubbed.

## 5. RESIDUALS — NAMED, NOT ABSORBED

- **`--emit-detect-pattern` (push_docs.sh's feed) does not fail closed.** The mirror-push
  detector still emits only the tracked classes when the local policy is absent — its
  behaviour is unchanged from pre-FM 28. Whether the PUBLIC-MIRROR gate should also refuse
  on an empty local policy is a separate ruling; widening it here would have changed
  push_docs.sh's behaviour unbidden. Filed in Amendment 2's constraints.
- The round-3 zip and FM 5 zips on `~/Desktop` still contain the scrubbed (clean) copies;
  the UNSCRUBBED staged trees FM 5 §3.2 notes ("copied, not modified") remain wherever FM 3
  pinned them — unchanged by this dispatch, named so the record is complete.

## 6. CLAIM IMPACT

```
CLAIM IMPACT: none
```

(Packaging/scrub tooling and a home dotfile; no ledger claim's evidence base changed.)

## 7. VERIFIED — what actually ran vs what was reasoned

**Watched run:** the zip-vs-tree diffs that recovered the redaction values (reconciled
against NC 27 §3.3's counts exactly); `scrub.py --self-test` green before commit;
`lane_tools_selftest.py` ALL FIVE TWINS GREEN after; the live six-variant catch (6/6, zero
residual). **Reasoned from code:** that no other consumer of `local_entries()` exists
beyond `entries()`/`substitutable()` (grepped); push_docs.sh behaviour unchanged (its feed
mode untouched — not re-run here).

**Commits:** claim `48fa623` (claim_lane.py, board row + scope, pushed) · Amendment 2
`c1ed599` · code `0c8d611` · doc+INDEX+HANDOFF (the commit after this file) · board close
(follows). All pushed in this dispatch.
