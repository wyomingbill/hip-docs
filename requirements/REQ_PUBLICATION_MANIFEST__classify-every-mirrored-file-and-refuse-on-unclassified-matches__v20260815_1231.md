# REQ_PUBLICATION_MANIFEST
Status: PLAN
Reconciled-Against: `80d03c6` (`~/hip-roadmap` @ `roadmap`), 2026-08-15. Filed by FM 35 **before
the first code edit**.
Inputs: **FM 31** (the push-scan that fails closed — the detector) and **FM 34** (the triage that
produced the buckets this manifest is seeded from).

## THE REQUIREMENT — Bill's words, 2026-08-15, verbatim

> **1. Publication manifest: every file the mirror pipeline touches carries a class — PUBLIC /
> PRIVATE / EVIDENCE-PRIVATE. Exclusion happens BEFORE mirror staging.**
>
> **2. FAIL-CLOSED: publication REFUSES if an unclassified file contains a scrub-class match (the
> FM 31 scan is the detector). An unclassified clean file: state the chosen default and why.**
>
> **3. Evidence stays byte-identical and hash-verifiable in the private repo. Public docs must not
> claim an excluded proof is publicly reproducible — sweep existing docs for such claims and list
> them (report, don't edit).**
>
> **4. Redacted derivatives: supported, clearly labeled NON-EVIDENCE, never overwriting the
> original. The 7 runnable proof scripts keep their authoritative copies private.**
>
> **5. Seed the manifest: FM 34's 25 bucket-(c) files → EVIDENCE-PRIVATE; the 163 must-scrub .md
> files stay PENDING-SCRUB (the scrub run is a separate dispatch); do NOT push.**

## ONE COUNT IN THE DISPATCH NEEDS CORRECTING BEFORE IT IS SEEDED

**Bucket (c) is 25 OCCURRENCES across 12 FILES, not 25 files.** FM 34's own table:
*"(c) GENUINELY AMBIGUOUS — 25 occurrences, 34 class-hits, 12 files."* The manifest classifies
**files**, so the seed is **12 EVIDENCE-PRIVATE entries** carrying 25 occurrences between them.
Bucket (b)'s "163" IS a file count and is used as given. Recorded here rather than silently
reconciled, because a seed that claimed 25 entries would not match the 12 the pipeline can find.

## THE CHOSEN DEFAULT, AND WHY — the question Bill asked to be answered explicitly

**An unclassified file that is CLEAN defaults to PUBLIC.**

- **It preserves exactly today's behaviour.** Publication already mirrors everything under `docs/`
  whenever FM 31's three-stage scan is clean. A clean unclassified file publishing is not a new
  exposure; it is the status quo, and the detector that decides "clean" is the same one that
  gates the push today.
- **The alternative silently un-publishes ~400 documents.** Defaulting to PRIVATE would drop
  every not-yet-classified file out of the mirror on the next run — a large invisible behaviour
  change wearing safety's clothes, and it would make adoption an all-or-nothing migration instead
  of an incremental one.
- **The fail-closed guarantee lives where the risk is.** Unclassified **plus a scrub-class match**
  REFUSES the whole publication. That is the rule that protects secrets; a default of PUBLIC on
  clean files does not weaken it.
- **THE RESIDUAL, STATED:** a file carrying a secret of a class the detector does not know about,
  left unclassified, would publish. That is the *current* pipeline's limit too — this REQ does not
  worsen it and does not fix it. **Offered for overrule:** if Bill wants default-PRIVATE, it is a
  one-line change in the gate plus a classification pass over `docs/`.

## THE ACCEPTANCE TEST

- **P1 — UNCLASSIFIED + MATCH REFUSES.** A file not in the manifest that carries a scrub-class
  match makes publication refuse, non-zero, naming the file and the class. Nothing is staged.
- **P2 — EVIDENCE-PRIVATE NEVER REACHES STAGING.** No file classed EVIDENCE-PRIVATE or PRIVATE
  appears in the staged publishable set.
- **P3 — PUBLIC CLEAN PASSES.** A classified-PUBLIC file with no match is staged, so the gate is
  not merely a brake.
- **P4 — EXCLUDED ARTIFACTS ARE BYTE-IDENTICAL AFTER A FULL RUN.** The sha256 of every
  EVIDENCE-PRIVATE file is recorded before and compared after; unchanged, or the test fails.
  **Exclusion must not be implemented by editing the thing excluded.**
- **P5 — REDACTED DERIVATIVES.** A derivative is a NEW path, labelled NON-EVIDENCE, and the
  original is untouched and still EVIDENCE-PRIVATE. Overwriting an original is a hard failure.
- **P6 — THE SEED IS EXACT.** 12 EVIDENCE-PRIVATE entries (FM 34 bucket (c)), 163 PENDING-SCRUB
  entries (bucket (b)); counted from the manifest, not asserted in prose.

## CONSTRAINTS

- **Exclusion happens BEFORE staging, and "staging" is `git subtree split --prefix docs`.**
  A split publishes the *whole subtree and its history*, so it cannot omit a file that is present
  in `docs/`. **Therefore the gate REFUSES while any PRIVATE / EVIDENCE-PRIVATE file exists under
  `docs/`** — that is the only way "never reaches staging" is true today, and it is deliberately
  louder than filtering.
- **The manifest lives OUTSIDE `docs/`** (`scripts/publication_manifest.tsv`) so it is not itself
  mirrored: a public list of which files were withheld is a signpost, and the manifest's job does
  not require publishing it.
- **No file's content is altered by this dispatch.** Not the 12, not the 163.
- **DO NOT PUSH** (Bill's instruction). Commits land locally; the exposure of an unpushed commit
  is named in the report, per STANDARD PREAMBLE item 8.

## WHAT THIS REQ DOES NOT CLAIM

- **It does not remove already-published history.** `git subtree split` has previously published
  `docs/` history; excluding a file now prevents future publication of its current content but
  does **not** unpublish blobs already pushed to the public mirror. **Naming this is part of the
  requirement** — a manifest that implied otherwise would be worse than none.
- **It does not run the scrub.** The 163 stay PENDING-SCRUB; that run is a separate dispatch.
- **It does not classify all of `docs/`.** Only the seed is authoritative; everything else is
  unclassified and governed by the default above.

---

## AMENDMENT 1 — FM 35 SCOPE ADDITION (Bill, 2026-08-15, from the adopted ruling's final text)

**Filed before the amendment's code.** Three refinements; two are built now and the third is
explicitly deferred.

### A1.1 — ABSENCE MUST READ AS A DECISION, NOT A GAP

> **The mirror RECORDS that an artifact was intentionally withheld (a manifest entry or
> placeholder naming the class, never the contents) — so absence reads as a decision, not a gap.**

**THIS REVERSES A REASONING IN THE PARENT REQ, AND THE REVERSAL IS RIGHT.** The parent placed the
manifest outside `docs/` because *"a public list of which files were withheld is a signpost."*
That reasoning was answering the wrong risk: a placeholder naming the **class** discloses nothing
a reader could not infer from the gap itself, while an unexplained gap is strictly worse — it
reads as sloppiness, and it leaves the 57 dangling references this dispatch already found
pointing at nothing. **The parent's placement stands (the manifest still lives outside `docs/`);
what changes is that the STAGED MIRROR gains notices.**

- **A1.1.1** every excluded file gets a placeholder **at its own path**, so a reader following a
  reference lands on the explanation rather than a 404.
- **A1.1.2** the placeholder names **the class and nothing else about the file** — no contents,
  no excerpt, and **no hash**: a digest of a withheld artifact is a weak oracle against guessed
  contents, and the parent REQ's hash-verifiability requirement is satisfied **in the private
  repo**, which is where it was scoped.
- **A1.1.3** a root index lists every withheld path with its class, so the decision is auditable
  at a glance rather than by walking the tree.

### A1.2 — THE ESCAPE MUST BE DETECTED, NOT ONLY PREVENTED

> **Twin: an EVIDENCE-PRIVATE artifact somehow entering mirror staging turns the public-build
> gate RED — the escape is detected, not just prevented.**

**Prevention and detection are different properties and only one of them survives a bug in the
preventer.** `stage()` excludes; that is prevention. **`verify_staged()` inspects the staged tree
and fails RED** if an excluded artifact is present — by path **and by content hash**, so an
escape that arrives under a different name is still caught.

- **A1.2.1** an EVIDENCE-PRIVATE / PRIVATE / PENDING-SCRUB file present in staging → RED.
- **A1.2.2** the same content present under a **different filename** → RED (hash comparison).
- **A1.2.3** the placeholders A1.1 writes must NOT trip it — a gate that flags its own notices is
  not a detector.

### A1.3 — NOTE ONLY, DELIBERATELY NOT BUILT NOW

> **Sanitized public REPRODUCER scripts may be derived from the 7 proof scripts — derivatives
> clearly labeled, originals untouched.**

**Recorded as a future capability, not a task in this dispatch.** When it is built: a reproducer
is a **new path**, labelled **NON-EVIDENCE**, classed `PUBLIC`, and the original stays
`EVIDENCE-PRIVATE` and byte-identical — the shape P5 already twins. **What it must not become:** a
reproducer that is presented as the proof. The original produced the recorded result; a sanitized
derivative produces *a* result, and the two must never be cited for each other.

---

## AMENDMENT 2 — FM 37: THE SCRUB, THE FILTERED MIRROR, AND THE LOCK

**Filed before the first line of FM 37 code.** Amendment 1 made absence legible and the escape
detectable; this one makes publication actually possible — and moves the scan to the artifact
that ships.

### THE REQUIREMENT — Bill's pipeline, verbatim

> **scrub -> verify -> assemble filtered staging -> exclude EVIDENCE-PRIVATE -> withheld markers
> -> scan the staged copy -> publish only if clean.**
>
> **S3 THE LOCK: the publication scan runs ON THE EXACT STAGED ARTIFACT THAT WILL BE PUSHED —
> not the private source tree, not an intermediate.**
>
> **S4 PUBLISH ONLY IF CLEAN. If any stage fails, STOP with the stage named — no partial
> publish.**

### A2.1 — THE SCRUB IS MECHANICAL, AND ITS SUCCESS CRITERION IS NOT NEGOTIABLE

- **A2.1.1** only the substitutable (mechanical) classes are replaced; each carries a token in
  the ONE shared table. **The 12 EVIDENCE-PRIVATE files are untouched BY DEFINITION** — they are
  not in the scrub set, and a scrub that reached them would be the defect this whole capability
  exists to prevent.
- **A2.1.2** afterwards FM 31's scan must reach clean **ON ITS OWN PREDICATE**. **Widening
  `EXCLUDE_ARGS`, adding a documented-usage excuse, or otherwise moving the goalposts to reach
  green is NOT LICENSED.** If it will not go clean, that is a STOP with the residue reported.
- **A2.1.3** **READABILITY IS PART OF THE ACCEPTANCE, not a courtesy.** FM 34 measured that ~79%
  of hits sit inside commands and paths. A scrub that leaves a runbook's commands unreadable has
  traded a disclosure problem for a documentation problem. The highest-hit files are sampled and
  the finding is reported either way.

### A2.2 — ASSEMBLY, BECAUSE A SPLIT CANNOT OMIT

`git subtree split --prefix docs` publishes the whole subtree **and its history**, so it can
neither omit a present file nor unpublish an already-pushed blob. The parent REQ's answer was to
**refuse** while an excluded file was present. **This amendment replaces refusal with assembly:**
the mirror branch is built from the manifest-filtered staging tree, not split from `docs/`.

- **A2.2.1** each excluded artifact leaves a marker containing the exact phrase
  **`INTENTIONALLY WITHHELD FROM PUBLIC MIRROR`** and its class, **never its contents** — so the
  57 known references resolve to a decision instead of a 404.
- **A2.2.2** **THE MIRROR BECOMES A FRESH ROOT, AND THAT IS A DELIBERATE CONSEQUENCE WITH TWO
  HALVES.** It removes those blobs from the mirror's CURRENT PUBLISHED refs and history. **It is NOT erasure and NOT guaranteed deletion** — prior clones, forks, caches and host-side retention may persist. **The private repository remains the historical and evidentiary record.** The parent REQ's stated limitation
  (*"does not unpublish blobs already pushed"*) is ADDRESSED to that extent and no further —
  **corrected wording, Bill's ruling 2, FM 37 continuation.** It also **discards the public mirror's commit history**, which
  is a real loss and is stated rather than discovered. The push was already `--force`; this makes
  what force means explicit.

### A2.3 — THE LOCK: THE SCAN RUNS ON WHAT SHIPS

- **A2.3.1** the publication scan runs over **the staged tree**, after assembly and after markers
  are written — not over `docs/`, not over an intermediate.
- **A2.3.2** **TWIN: a secret planted in STAGING and absent from SOURCE is caught.** A scan of
  the source tree cannot catch it, so this twin is the difference between the two designs and is
  the reason the lock exists.
- **A2.3.3** publish only on a clean staged scan. **Any stage failing STOPS and names the stage;
  a partial publish is never an outcome.**

### CONSTRAINTS ADDED

- **No goalpost moving.** Neither the detector's pattern table nor the scan's exclusions may be
  weakened to reach a clean result in this dispatch.
- **The scrub set is re-measured at run time.** The manifest is authoritative for CLASSIFICATION;
  the detector stays authoritative for RISK (established when Amendment 1's staging caught two
  files that landed four minutes after the seed).
- **Sequence order is load-bearing.** Scanning before assembly, or publishing before scanning,
  fails this amendment even if the result happens to be clean.

---

## AMENDMENT 3 — FM 37 CONTINUATION: VALUE-SHAPED DETECTION, AND THE FRESH-ROOT WORDING

**Filed before the first line of the continuation's code.** Two rulings.

### RULING 1 — THE VOCABULARY CLASSES BECOME VALUE-SHAPED (verbatim)

> **ROUTE 1: the vocabulary classes become VALUE-SHAPED — detection triggers on credential-like
> structures (assignments like token=<long value>, bearer tokens, key formats, high-entropy
> strings), never on the bare words. Anti-vacuity twins: a REAL planted secret in each reshaped
> class still trips the gate; the documentation lines that caused the 1,968 no longer do.**

**What was wrong with the old class, in one line:** `password|secret|api_key|token|NEO4J|bearer`
matched the SUBJECT MATTER of a repository about credential handling. FM 37 measured 1,968 such
lines — `token` 966, `secret` 264, `password` 130 — and a representative hit merely named which
source files reference `OPENAI_API_KEY`. **A detector that fires on the word "password" in a
sentence about passwords is measuring the topic, not the risk.**

- **A3.1** the bare-word class is REMOVED and replaced by structures: a credential-shaped
  ASSIGNMENT (name, separator, long opaque value), a BEARER token, an AUTHORIZATION header, and a
  JWT. The existing provider-key prefixes, PEM blocks and AWS ids are kept as they already were —
  they were always value-shaped.
- **A3.2** **ANTI-VACUITY IS PER CLASS, NOT IN AGGREGATE.** For every reshaped class, a twin
  plants a REAL-shaped secret of that class and asserts the gate trips. A single omnibus test
  would let one class silently stop working.
- **A3.3** **THE DOCUMENTATION LINES MUST GO QUIET.** Twins assert that the exact shapes which
  produced the 1,968 — an env-var name with a `file:line` reference, prose about tokens, a
  `NEO4J_USER|PASSWORD` label — no longer match.
- **A3.4** **HIGH-ENTROPY ALONE IS NOT A TRIGGER, AND THAT IS DELIBERATE.** This repository
  documents sha256 digests constantly (every banked artifact carries one). A bare
  high-entropy rule would flag every one of them and reintroduce the same false-positive
  failure in a new costume. Entropy is used only INSIDE a credential structure — a long opaque
  value in an assignment, after a `Bearer`, in a JWT — never on its own.

### RULING 2 — THE FRESH-ROOT WORDING IS CORRECTED EVERYWHERE (verbatim)

> **FRESH ROOT CONFIRMED, with the wording correction recorded everywhere the trade is
> described: the fresh root REMOVES old blobs from the CURRENT PUBLISHED refs/history — never
> claim erasure or guaranteed deletion; prior clones, forks, caches, or host retention may
> persist. Private repo remains the historical/evidentiary record.**

- **A3.5** every description of the trade — this REQ, the dispatch record, the board row, and
  the pipeline's own comments — says **removed from the current published refs and history**, and
  **never** "erased", "deleted" or "unpublished" without qualification.
- **A3.6** the qualification travels WITH the claim, not in a footnote: **prior clones, forks,
  caches and host-side retention may persist.** A reader who sees only the first half must not be
  able to come away believing deletion was achieved.
- **A3.7** **the private repository remains the historical and evidentiary record.** The mirror is
  a publication surface, not an archive, and nothing in this pipeline makes it one.

### THE ACCEPTANCE

- **A3.8** the staged scan is re-run under the reshaped predicate; **publication proceeds only on
  clean**, and S4's rule is unchanged — any stage failing is a STOP naming the stage.
