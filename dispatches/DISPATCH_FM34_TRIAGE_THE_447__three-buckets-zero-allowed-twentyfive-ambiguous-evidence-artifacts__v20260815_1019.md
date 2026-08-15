# DISPATCH_FM34_TRIAGE_THE_447
Status: BUILT
Reconciled-Against: `f3bae8c` (`~/hip-roadmap` @ `roadmap`), 2026-08-15

**TYPE:** MEASUREMENT (classification)

**REQ:** **NONE.** Nothing is built and nothing is changed — this dispatch classifies an
existing population against an existing ruling. Requirements Discipline item 10's case,
stated rather than filled with an invented REQ.

**CLAIM IMPACT: none.**

> ### STRICTLY READ-ONLY, AND VERIFIED SO
> **No `docs/` content was mutated. No scrub was run. NO MIRROR PUSH — the mirror stays
> blocked throughout.** The only writes are this dispatch doc, one TD row, one INDEX row
> and two board rows. **No matched value appears anywhere in this document**, its commits,
> or the recap: every figure is a class, a file path, a count, or a structural flag.

---

## BILL'S RULING — verbatim, the instruction this dispatch executes

> Triage the 447. Read-only classification first against the existing redaction policy;
> bring Bill only ambiguous cases. No mirror push until required scrubs are cleared.
> Leave the dead Neo4j credential in public history; record it as rotated/dead historical
> hygiene, no history rewrite.

## THE POLICY IT IS TRIAGED AGAINST — verbatim (FM 28, `scripts/scrub_patterns.py`)

> city-only and zoning-district references STAY (test semantics needed for review);
> actual private-network identifiers, hostnames, credentials, precise private
> addresses, machine/user-specific material are scrubbed.

---

## ⚠ FIRST — A CORRECTION TO FM 31's OWN NUMBER

**"447" is a SUM OF PER-CLASS HITS, not a count of lines.** Measured here:

| figure | value |
|---|---|
| per-class hits (the number FM 31 reported) | **447** |
| **distinct file-line occurrences** | **316** |
| lines matched by more than one class | **111** |

The largest overlap is exact and structural: **`tailnet-address` and `tailnet-address-host`
match the SAME 66 lines** — 66 both, 0 only-a, 0 only-b — so 66 hits are one population
counted twice. FM 31 said "447 real-secret-class lines"; **the honest phrasing is 447
class-hits over 316 occurrences in 175 files.** Corrected here rather than left standing,
per the pre-authorized class *"correct its OWN prior report when later evidence
contradicts it"*. **Both figures are carried below** so nothing silently changes size.

---

## 1. THE THREE BUCKETS

| bucket | occurrences | class-hits | files |
|---|---|---|---|
| **(a) CLEARLY ALLOWED** | **0** | **0** | **0** |
| **(b) CLEARLY MUST-SCRUB** | **291** | **413** | **163** |
| **(c) GENUINELY AMBIGUOUS** | **25** | **34** | **12** |
| totals | 316 | 447 | 175 |

### Per class

| class | (b) hits | (c) hits | policy clause it falls under |
|---|---|---|---|
| `user-path` | 135 | 14 | machine/user-specific material |
| `machine-hostname` | 93 | 0 | hostnames |
| `tailnet-address-host` | 66 | 0 | private-network identifiers |
| `tailnet-address` | 66 | 0 | private-network identifiers |
| `user-ssh` | 18 | 0 | machine/user-specific material |
| `home-address-street` | 10 | 11 | precise private addresses |
| `home-address-full-city` | 8 | 9 | precise private addresses |
| `lan-address` | 7 | 0 | private-network identifiers |
| `tailnet-domain` | 4 | 0 | private-network identifiers |
| `lan-cert-cn` | 4 | 0 | private-network identifiers |
| `tailnet-host` | 1 | 0 | private-network identifiers |
| `tailnet-name` | 1 | 0 | private-network identifiers |
| **TOTAL** | **413** | **34** | |

### ⚠ BUCKET (a) IS EMPTY, AND IT IS EMPTY BY CONSTRUCTION — proven two ways

This is the result most easily misread, so both proofs are stated.

1. **There is no city-alone or zone-district pattern in the table at all.**
   `scrub_patterns.py`'s own module doc says so: *"the machine-local policy file carries NO
   city-alone or zone-district entry, and a session must not add one on its own judgement."*
   A city-only reference is therefore **never detected** and cannot appear in this
   population. **Nothing was "allowed through" — the allowed category is simply not in the
   detected set.**
2. **The one class whose NAME suggests otherwise does not behave that way.** `home-address-full-city`
   sounds like it might carry city-only references. Measured: **all 17 of its hits are ALSO
   matched by `home-address-street`** — 17 with a street component, **0 without**. Every one
   is a precise private address that happens to include the city, not a city-only reference.

**This retires the qualification FM 31 itself raised** (*"some `home-address-*` rows may be
FM 28 policy-permitted rather than defects"*). Measured and refuted: none are.

---

## 2. BUCKET (c) — EVERY CASE, IN FULL

**25 occurrences, 34 class-hits, 12 files. Every one is a NON-`.md` file, and that is the
discriminator, not a coincidence: these are CAPTURED OR EXECUTABLE ARTIFACTS whose value is
their byte-identity.** The 291 `.md` prose occurrences are unambiguous bucket (b).

**Why this is ambiguous rather than merely awkward:** Bill's own standing rule (recorded
2026-08-15, evidence-handling) is *"never scrub evidence"* — redaction replaces a seeded
value in a review copy, while leak-analysis and evidentiary material stays untouched. The
publication policy says scrub precise private addresses. **On these twelve files the two
rules point in opposite directions, and only Bill can say which wins.**

### (c-1) CAPTURED RESULT ARTIFACTS — 4 files, 20 occurrences

| file | occ | classes |
|---|---|---|
| `docs/dispatches/frontier_tier_openai_real_call_results__v20260718_0552.json` | 11 | `home-address-full-city` 5, `home-address-street` 6 |
| `docs/dispatches/frontier_tier_real_call_results__v20260717_1530.json` | 6 | `home-address-full-city` 3, `home-address-street` 3 |
| `docs/dispatches/frontier_tier_openai_boundary_and_consent_5x_results__v20260718_0552.json` | 2 | `home-address-full-city` 1, `home-address-street` 1 |
| `docs/dispatches/frontier_tier_boundary_and_consent_5x_results__v20260717_1530.json` | 1 | `home-address-street` 1 |

**WHY AMBIGUOUS:** these are byte captures of **real frontier API calls**, and the private
address is in them because **it was the payload actually transmitted off-device**. That is
precisely what makes them evidence — a disclosure record whose whole point is to show what
left. Scrubbing them rewrites the record of what was sent; not scrubbing them publishes a
precise private address. **Recommended disposition (a PROPOSAL, not a ruling): EXCLUDE the
file from publication rather than alter it** — the mirror is a `git subtree split` of
`docs/`, so exclusion is a real option and it preserves both rules at once.

### (c-2) A BANKED PROOF ARTIFACT — 1 file, 7 occurrences

| file | occ | classes |
|---|---|---|
| `docs/dispatches/assets/FM15_hook_enforcement_proof.txt` | 7 | `user-path` 7 |

**WHY AMBIGUOUS:** the `assets/` series exists to hold **byte-identical captures with a
recorded sha256** (the VD-63 / HA-96 banking precedent). **Editing one invalidates the hash
that is the artifact's entire warrant.** The paths in it are the proof — the file
demonstrates a hook firing across worktrees, and the worktree paths are what it proves.

### (c-3) EXECUTABLE PROOF SCRIPTS — 7 files, 1 `user-path` occurrence each

`frontier_tier_verify_script__v20260717_1500.py` ·
`frontier_tier_boundary_and_consent_5x_script__v20260717_1530.py` ·
`frontier_tier_real_call_script__v20260717_1530.py` ·
`frontier_tier_openai_boundary_and_consent_5x_script__v20260718_0552.py` ·
`frontier_tier_openai_real_call_script__v20260718_0552.py` ·
`detection_miss_measurement_script__v20260717_1117.py` ·
`d21_live_proof_script__v20260717_1230.py`

**WHY AMBIGUOUS:** these are **runnable**. A scrub changes what the script does, so a
reviewer re-running the published copy runs different code from the one that produced the
recorded result. **Recommended disposition (PROPOSAL): substitute with a token that keeps
the script runnable after one obvious edit** — e.g. a clearly-marked placeholder path — or
exclude, as with (c-1). **Not decided here.**

---

## 3. THE PROPOSED SCRUB PLAN FOR BUCKET (b) — PROPOSED, NOT EXECUTED

**Nothing below was run.** No file was touched.

### 3.1 Does FM 28's scrubber already handle these? — YES, for all 413

Every bucket-(b) class is **substitutable** — it carries a replacement token in the one
table, so `scripts/scrub.py` can already do the work and **no new pattern is needed**:

| class | existing token |
|---|---|
| `user-path` | `[REDACTED-USER-PATH]` |
| `machine-hostname` | `[REDACTED-MACHINE-NAME]` |
| `tailnet-address`, `tailnet-address-host` | `[REDACTED-TAILNET-ADDRESS]` |
| `tailnet-host` | `[REDACTED-TAILNET-HOST]` |
| `tailnet-domain`, `tailnet-name` | `[REDACTED-TAILNET-DOMAIN]` |
| `lan-address`, `lan-cert-cn` | `[REDACTED-LAN-ADDRESS]` |
| `home-address-street`, `home-address-full-city` | `[REDACTED-HOME-ADDRESS]` |
| `user-ssh` | `[REDACTED-USER]@` |

**So the plan is a RUN, not a build.** That is the single most useful finding in this
section: nobody needs to write new patterns to clear the mirror.

### 3.2 Scope — 163 `.md` files, 291 occurrences

Concentrated rather than spread: the top file carries 45 occurrences
(`DISPATCH_KEY_LIFECYCLE_RULINGS_ENACTED__…__v20260806_2036.md`), the next 16
(`DISPATCH_KEY_LIFECYCLE_BANK_RERUN__…__v20260806_1921.md`), then 9, 7, 6, 5, 5. **The
long tail is one or two occurrences per file.**

### 3.3 The order it should run in

1. **Rule bucket (c) FIRST** (the 12 files). Running a scrub across `docs/` before that
   ruling would silently take the decision for them, which is exactly what this dispatch
   exists to prevent.
2. Run `scripts/scrub.py` in its certifying mode over the 163 `.md` files. It **fails
   closed** on an absent/empty local policy (FM 28 Amendment 2), so an unconfigured run
   refuses rather than reporting a false clean.
3. **Re-run the repaired `push_docs.sh` scan and require it to reach `Secret scan: clean.`
   on its own predicate** — not on a widened exclusion list. **Widening the exclusions to
   clear the mirror is NOT licensed** (REQ Amendment 4 constraint 3), and tuning a filter
   until a scan goes green is the shape this project forbids.
4. Only then unblock the mirror.

### 3.4 What this plan deliberately does NOT propose

- **No history rewrite** — see TD-R-199 and Bill's ruling.
- **No change to the exclusion list**, for the reason in step 3.
- **No new patterns**, because none are needed (3.1).
- **No decision on the 12 (c) files.**

---

## 4. THE NEO4J HISTORY DISPOSITION — filed as **TD-R-199**

Rotated · dead · reachable at `2717d82~1` · ruled **historical hygiene** · **no history
rewrite**. Filed CLOSED-as-ruled rather than OPEN, so it cannot be picked up later as an
undiscovered issue — which is the job Bill gave it.

**The part of that row which stays live** is not the credential but the limit it exposes:
**a Neo4j password matches none of the 17 substitutable classes**, so FM 31's clean
retrospective means *no class the table can detect as a value is present* — **not** *no
secret is published*. Carry that forward.

---

## VERIFIED

**Watched run** — three read-only probes in the session scratchpad, reproducible from this
doc: `fm34_triage.py` (the three buckets and per-class counts), `fm34_ambiguity.py` (the
full-city/street overlap and the solo-class check), and a file-shape pass (extensions,
symlinks, per-file counts). All reproduce FM 31's repaired three-stage scan by reading
`EXCLUDE_BRANCHES` **out of the shipped `push_docs.sh`**, so the measurement is against the
list that actually ships, not a copy.

**Checked and clean:** **no symlink appears in the hit set**, so no `LATEST_*` pointer
double-counts a real file.

**Reasoned about — not independently executed:**
- That every bucket-(b) class is handled by the existing scrubber. Read from the table's
  tokens; **no scrub was run to confirm it end to end**, and §3.3 step 2 is where that gets
  proven rather than assumed.
- That excluding a file from the subtree split is a real option. It follows from
  `push_docs.sh` using `git subtree split --prefix docs`, but **no exclusion mechanism
  exists in the script today** — building one would be a separate dispatch.

---

## HASH

| commit | what |
|---|---|
| `6a0ace1` | board claim |
| *(this commit)* | dispatch doc, TD-R-199, INDEX row |

---

## OPEN — BILL DECIDES

1. **THE 12 (c) FILES.** Scrub them, or exclude them from publication? The three sub-groups
   may deserve different answers: captured results (c-1), a hashed banked artifact (c-2),
   runnable scripts (c-3).
2. **Is "exclude from publication" a sanctioned outcome at all?** It does not exist in the
   tooling today. If it is, it needs building; if it is not, (c) collapses into scrub-or-
   publish and the evidence-integrity cost is accepted deliberately.
3. **Nothing else is blocked.** The 413 bucket-(b) hits need no ruling and no new
   patterns — only a run, in the order at §3.3.
4. **Not measured: whether a scrub of the 163 `.md` files leaves the documents readable.**
   `user-path` and `machine-hostname` appear inside commands in 79% of hits overall, so
   post-scrub reproducibility is a real question — and it is the same question (c-3) raises
   for scripts. Named here rather than discovered after the run.
