# DISPATCH_FM37 — scrub the 216, then the filtered mirror
Status: **BUILT — AND STOPPED AT S4. NOT PUBLISHED.**
Reconciled-Against: `99b2e92` (`~/hip-roadmap` @ `roadmap`)
Dispatch: FM 37
Date: 2026-08-15 15:25 → 16:15 (Mountain)
REQ: **`REQ_PUBLICATION_MANIFEST` Amendment 2** — `bc5a779`, **before the first line of code**
Board claim: `362ddb7`

STOPPED AT SEGMENT 4 — NEEDS BILL

---

## THE HEADLINE, BEFORE THE DETAIL

**The pipeline is built and every stage before publication passed. Publication STOPPED at the
staged-copy scan, and the residue is not what the scrub was for.**

- **Mechanical (real-secret) classes in the tree that would ship: ZERO.**
- **The 1,968 lines blocking the scan are the docs-VOCABULARY class** — the words `token`,
  `secret`, `password`, `NEO4J`, `bearer`, `api_key` occurring in documentation *about* secrets
  management. A representative hit is a line naming which source files reference
  `OPENAI_API_KEY`. **No secret value is among them.**
- **Widening the scan's exclusions to reach green is NOT LICENSED** (Amendment 2, A2.1.2), so
  this dispatch stops and reports rather than moving the goalposts.

## S1 — THE SCRUB

**403 substitutions across 218 targets** (174 distinct files; the remainder are `LATEST_*`
symlinks resolving onto the same content). The scrubber verified **zero residual against the
WRITTEN files**, which is its own FM 5 lesson applied.

| class | substitutions |
|---|---|
| `user-path` | 196 |
| `machine-hostname` | 92 |
| `tailnet-address` | 67 |
| `user-ssh` | 18 |
| `lan-address` | 10 |
| `home-address-full-city` | 9 |
| `home-address-street` | 5 |
| `tailnet-domain` | 5 |
| `tailnet-host` | 1 |

**The 12 EVIDENCE-PRIVATE files are byte-identical**, sha256 compared before and after —
untouched by definition, never in the scrub set.

**Mechanical-class residue outside those 12: ZERO.** The 34 mechanical hits that remain in the
repository are all *inside* the 12, which never reach the mirror.

### Readability — FM 34's 79% concern, sampled and answered

FM 34 measured that ~79% of hits sat inside commands and paths, and warned that a scrub could
trade a disclosure problem for a documentation problem. **It did not happen, because the
substitution is structure-preserving:**

```
before:  git -C ~/hip-roadmap config core.hooksPath /Users/…/hip-roadmap/scripts/hooks
after:   git -C ~/hip-roadmap config core.hooksPath [REDACTED-USER-PATH]/hip-roadmap/scripts/hooks

before:  1  /Users/…/hip-dev/ledger/keys
after:   1  [REDACTED-USER-PATH]/hip-dev/ledger/keys
```

The command shape, the flags, the tree name and the relative path all survive; only the home
prefix is gone, and a reader reconstructs the command by substituting their own. **Sampled from
the highest-hit files** (48, 48, 18, 18, 9 hits) — the two 48-hit files are a key-lifecycle
dispatch and its `LATEST_` symlink, whose content is a table of certificate and key directories,
and the table still reads as a table.

## S2 — ASSEMBLY, BECAUSE A SPLIT CANNOT OMIT

**The method, stated as the dispatch asked.** `git subtree split --prefix docs` publishes the
whole subtree *and its history*: it can neither omit a file that is present nor unpublish a blob
already pushed. So the mirror is no longer split — it is **assembled**:

1. `publication_gate.stage()` copies only the manifest-publishable files into a fresh staging
   directory;
2. every excluded artifact leaves a marker at **its own path**, carrying the exact phrase
   **`INTENTIONALLY WITHHELD FROM PUBLIC MIRROR`** and its class, **never its contents** — so
   the 57 known references resolve to a decision instead of a 404;
3. a root `WITHHELD.md` indexes every withholding;
4. the mirror commit is built **from that tree**, as a fresh root.

**Measured on the real tree: 865 files staged, 12 withheld markers, root index present.**

**The fresh root has two halves and both are stated.** It removes those blobs from the mirror's CURRENT PUBLISHED refs and history. **It is NOT erasure and NOT guaranteed deletion** — prior clones, forks, caches and host-side retention may persist. **The private repository remains the historical and evidentiary record.** And it **discards the
public mirror's commit history**. The push was already `--force`; this makes what force means
explicit. **Wording corrected per Bill's ruling 2 (FM 37 continuation): the earlier phrasing here
read "unpublishes previously leaked blobs", which overclaimed.**

**The 216 were promoted `PENDING-SCRUB` → `PUBLIC` only after being measured clean**, not
because the scrub was run.

## S3 — THE LOCK: THE SCAN RUNS ON WHAT SHIPS

`scripts/publication_scan.sh` is **FM 31's three stages extracted verbatim**, with the one
directory made a parameter. Extracted rather than reimplemented, so detector and gate cannot
drift — the same failure FM 9's one-table fix addressed a layer down. `push_docs.sh` now scans
**the staged tree**, after assembly and after markers, instead of the private source tree.

**Twinned in both directions, which is the whole point:**

| twin | result |
|---|---|
| a secret planted in **staging** and **absent from source** is caught | **PASS** — a source-tree scan could not have caught it |
| the same scan **passes** a clean staging tree | **PASS** — the detector is not simply refusing everything |

**19 twins green** overall. Three older assertions were updated because Amendment 2 changed the
contract, and **each was made stricter, not looser**: the marker phrase is now pinned verbatim,
the classification twin asserts exclusion at the staging boundary, and the promotion twin
asserts *measured cleanliness* rather than a row count.

## S4 — PUBLISH ONLY IF CLEAN → **NOT PUBLISHED. STOPPED AT: the staged-copy scan.**

```
STAGED SCAN EXIT: 1        1,968 hit lines
```

**Composition of the residue — this is the finding:**

| word | hits | what it actually is |
|---|---|---|
| `token` | 966 | operator tokens, confirmation tokens, pending tokens — the system's own vocabulary |
| `secret` | 264 | prose about secret handling |
| `password` | 130 | prose about credential policy |
| `NEO4J` | 24 | env-var names |
| `bearer` | 13 | auth-scheme prose |
| `api_key` | 12 | e.g. a line listing which files reference `OPENAI_API_KEY` |

**These are the detect-only, non-substitutable class.** They carry no replacement token by
design, because they are words, not values. **A documentation repository whose subject is
governed memory and credential handling cannot stop containing them.**

**So "clean on its own predicate" is unreachable for this corpus** — not because the scrub left
anything, but because the predicate includes a vocabulary class that fires on documentation
about secrets. Three ways out exist and **all three are rulings, not session edits**:

1. **Narrow the vocabulary class to value-shaped matches** (`token\s*[:=]\s*\S{16,}` rather than
   the bare word) — the detector then measures secrets instead of subject matter.
2. **Accept the documented-usage exclusions** the scan's third stage already has, extended to
   cover these — **explicitly not licensed to this dispatch**, and the reason it stopped.
3. **Publish with the vocabulary class scoped out of the staged scan only**, on the argument
   that the staged tree has already been scrubbed of every substitutable class.

**Nothing was published. No partial publish occurred.**

## WHAT LANDED ANYWAY, AND WHY IT WAS WORTH IT

The scrub is durable value independent of publication: **403 real private values are gone from
174 tracked documents**, and the repository is materially safer whether or not the mirror ever
ships. The pipeline is built and twinned end to end; only the final gate is red, on a predicate
question.

## CLAIM IMPACT

```
CLAIM IMPACT: none
```

## NEEDS BILL

1. **The predicate ruling (S4).** Which of the three routes — narrow the class, extend the
   documented-usage exclusions, or scope the vocabulary class out of the staged scan? Publication
   is blocked until one is chosen, and choosing is not a session's call.
2. **The fresh-root consequence (S2).** Confirm that discarding the public mirror's commit
   history is acceptable in exchange for unpublishing the previously leaked blobs.
3. **The 34 mechanical hits inside the 12 EVIDENCE-PRIVATE files** remain, by design. They never
   reach the mirror; they do remain in the private repository, which is where the ruling put them.
