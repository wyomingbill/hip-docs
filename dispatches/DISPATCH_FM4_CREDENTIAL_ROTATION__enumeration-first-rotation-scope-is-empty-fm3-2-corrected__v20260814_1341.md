# FM 4 — CREDENTIAL ROTATION AFTER REVIEW-PACKAGE EXPOSURE
Status: **STOPPED AT SEGMENT 2** — enumeration complete, rotation scope empty, ruling owed
Reconciled-Against: 2026-08-14. Board claim `7126eb4` on `roadmap`.

REQ: **NONE.** Enumeration, a record correction, and a file move. No product code changed
and — the point of this document — no credential was rotated.

---

## 0. THE EXCEPTION LINE

```
FM 4 — CREDENTIAL ROTATION AFTER REVIEW-PACKAGE EXPOSURE
STOPPED AT SEGMENT 2 — NEEDS BILL
```

**Segment 1 (ENUMERATE) ran and is complete. Segments 2 and 3 (ROTATE, VERIFY) COULD NOT
RUN, because segment 1 established there is nothing to rotate.** A segment that could not
run is a STOP, not a finding — hence the second form, naming the segment.

**Segment 4 (QUARANTINE) ran and is complete**, because its justification survives the
correction: the three packages are stale and must not be sent regardless of what is in them.

**⚠ THE DISPATCH'S PREMISE IS NOT SUPPORTED BY THE ARTIFACT, AND THE PREMISE WAS MINE.**
The context line — *"HIP_CODE_REVIEW.zip contained hip-roadmap/.env.dev and certs/voice.key
among 14 credential/runtime files"* — traces to FM 3's finding FM3-2, which I wrote
yesterday and which is **wrong**. §2 corrects it against the artifact.

---

## 1. WHY THIS STOPPED INSTEAD OF PROCEEDING

The dispatch's own segment 1 says: *"list every credential-bearing file and every distinct
secret in them. That list is the rotation scope — **no guessing**."* Enumeration ran first,
exactly as ordered, and returned an empty scope. **The instruction that would have been
violated by proceeding is the dispatch's own.**

Proceeding anyway would have cost three things and bought nothing:

- **Two in-flight lanes disrupted.** NC 5 (`~/hip-nc`) and VD-60 (`~/hip-cutover-demo`) are
  both IN FLIGHT on the board. Rotating Neo4j passwords means restarting graph services
  under them — the exact thing the dispatch's coordination clause forbids.
- **Provider-side rotations Bill does not owe.** Segment 2 asks for a list of API keys to
  rotate at the provider. **The list is empty**; producing a non-empty one would have sent
  Bill to rotate credentials that were never disclosed.
- **A false exposure event entered into the permanent record**, which is worse than the
  original error because later dispatches would cite it as fact.

---

## 2. THE CORRECTION — FM3-2 WAS WRONG

**This is the pre-authorized correction class** (*"Correct its OWN prior report when later
evidence contradicts it… in a new record that names the old one; do not quietly rewrite
history"*). FM 3's dispatch doc and board row stand as written; this document supersedes
them on this point only.

**FM 3 said (FM3-2), and it is WRONG:**

> *"Package 1 shipped credential and runtime files that package 3 excluded — 14 named,
> including `hip-roadmap/.env.dev` and `certs/voice.key`."*

**The mistake, precisely.** `MANIFEST_REDACTED.txt` inside
`HIP_CODE_REVIEW_REDACTED_20260813.zip` prints a section headed *"Credential/runtime files
excluded (14)"* and lists them. **That is package 3's own EXCLUSION list — the files it
walked past in the LIVE TREES and did not package.** FM 3 read it as an inventory of what
package 1 *included*, and inferred a shipped-credentials finding from a list of
not-shipped credentials. **The manifest was read correctly and reasoned from backwards.**

**Nothing in FM 3 checked package 1 itself.** One `unzip -l` would have settled it, and did:

```
$ unzip -l HIP_CODE_REVIEW.zip | grep -cE "\.env"     ->  2   (both .env.dev.example)
$ unzip -l HIP_CODE_REVIEW.zip | grep -cE "\.key$"    ->  0
$ unzip -l HIP_CODE_REVIEW.zip | grep -cE "\.db($|-wal$|-shm$)"  ->  0
$ unzip -l HIP_CODE_REVIEW.zip | grep -cE "\.pem$"    ->  0
```

**The generalisable lesson, which is the part worth keeping:** an exclusion list and an
inventory are the same shape — a list of paths under a heading — and they mean opposite
things. FM 3 had the artifact in hand and read a *description of* it instead. **A claim
about what a file contains must be measured against that file, never against its
manifest.** This is the same rule the redaction work already follows ("verify against the
delivered artifact") applied one level up, and FM 3 followed it for redaction while
failing to follow it here.

---

## 3. SEGMENT 1 — ENUMERATE. THE MEASURED RESULT

All three packages were opened read-only, extracted to a mode-700 scratch directory,
scanned, and the extraction destroyed afterwards. **4,921 text files scanned across the
three packages.**

### 3.1 Credential-bearing files actually present

| file | present in | what it is | secret? |
|---|---|---|---|
| `hip-roadmap/.env.dev.example` | pkgs 1, 3 | git-tracked template. Ports, `JAVA_HOME`, `$HOME`-relative paths, and `HIP_FRONTIER_CODEWORD=CHANGE_ME` | **NO** |
| `hip-cutover-demo/.env.dev.example` | pkgs 1, 3 | same template | **NO** |
| `hip-roadmap/certs/voice.crt` | pkgs 1, 3 | self-signed X.509 **certificate** — `subject=CN=[REDACTED-LAN-ADDRESS]`, `issuer=CN=[REDACTED-LAN-ADDRESS]`, valid Jul 2026 → Oct 2028 | **NO — public half** |
| `hip-cutover-demo/certs/voice.crt` | pkgs 1, 3 | same | **NO — public half** |

**`voice.key` — the private half — is ABSENT from all three packages.** So is every
`.env` / `.env.dev` / `.env.demo`, every `*.pem` / `*.p12` / `id_rsa`, every `*.db` /
`-wal` / `-shm`, and every `*.npz` voiceprint.

### 3.2 Content-level scan — what the pattern hits actually are

| pattern | hits | verdict |
|---|---|---|
| PEM `BEGIN … PRIVATE KEY` **with a base64 body** | **0** | **no key material anywhere** |
| provider key literals — `sk-`, `sk-ant-`, `gsk_`, `AKIA…`, `ghp_`, `github_pat_`, `xox[baprs]-` | **0** | **no API key was disclosed** |
| `NEO4J_PASSWORD=` | 5 | all `NEO4J_PASSWORD = os.environ.get(...)` in `harness/zep_store.py` — **source code reading the env** |
| `password=` / `api_key=` / `secret=` / `token=` | 41 | all `os.environ.get(...)` or a variable pass-through — **source code**, no literals |
| 64-hex strings | 99 | `script_sha256` fields in `demo_scripts/test/*_expected.json` and `head_hash sha256:` in the ledger-anchor design/spec docs — **content hashes, not tokens** |

**One near-miss worth recording so it is not re-raised:** `scripts/push_docs.sh` matches a
naive `BEGIN.*PRIVATE KEY` search in all three packages. It is the project's **own
pre-push secret-scanning regex** — a guard, not a key. The stricter pattern (header +
base64 body + footer) returns zero.

### 3.3 The 2026-08-12 round, checked too — also clean

Not named in the dispatch, but that round CLOSED with a closeout, so those packages went
off-box as well and the same question applies. `hip_review_f2f17ca.zip`, `hip_source.zip`
and `hip_main.zip` (all still on the Desktop): **zero `.env*`, zero `*.key`, zero `*.pem`,
zero `*.npz`, zero `.git/`.** `hip_main.zip`'s 362 MB is a TTS model
(`models/kokoro-v1.0.onnx`, 325 MB) plus business and whitepaper binaries; its `ledger/`
entries are **empty directories**, and its "transcript" hits are test fixtures and
governance-proof documents, **not live household transcripts.**

**Across all six packages ever built, the rotation scope is empty.**

---

## 4. WHAT *IS* WORTH BILL'S ATTENTION — AND IT IS NOT ROTATABLE HERE

**Private network addressing went off-box in every package.** This is not a credential and
cannot be rotated by this dispatch, but the project's own `scripts/push_docs.sh` scrubs
these exact strings from docs before pushing — **so the project already classifies them as
sensitive**, and they shipped anyway.

| | tailnet `100.72.236.x` | `*.[REDACTED-TAILNET-DOMAIN]` hostname | LAN `10.0.0.x` |
|---|---|---|---|
| `HIP_CODE_REVIEW.zip` | 132 | 6 | 14 |
| `HIP_CODE_REVIEW_REDACTED_20260813.zip` | 136 | 6 | 18 |
| `HIP_VO_REVIEW.zip` | 25 | 3 | 6 |
| **`HIP_REVIEW_demo-cutover_7904c36.zip`** (FM 3, **not yet sent**) | 6 | 1 | 2 |
| **`HIP_REVIEW_advisor-roadmap_d9e2010.zip`** (FM 3, **not yet sent**) | 7 | 1 | 2 |
| **`HIP_REVIEW_governed-voice_65c263e.zip`** (FM 3, **not yet sent**) | 5 | 1 | 2 |

The LAN address is also the CN of the self-signed voice certificate, so it is disclosed by
`voice.crt` independently of any prose.

**Two things follow, and both are Bill's:**

1. **Tailscale-side mitigation** — an ACL review, or rotating the node name / tailnet
   name. **A provider-side action, listed and not touched**, exactly as segment 2 directs
   for provider credentials.
2. **A decision on the three packages that have NOT been sent yet.** They carry the same
   class at roughly 5% of the volume. **They are built and waiting; nothing has left the
   box.** Stripping the addressing from them is a small, contained rebuild if you want it —
   but it is a scope change, not a fix, so it is not being done unasked.

---

## 5. SEGMENT 4 — QUARANTINE. DONE

Moved to **`~/Desktop/REVIEW_STALE_QUARANTINE/`**. **Nothing deleted.**

| file | size | SHA-256 (taken BEFORE the move) |
|---|---|---|
| `HIP_CODE_REVIEW.zip` | 17.5 MB | `83edcff039c07a1a7cfca8268c6ce77daa7a59b47dffae675d7fe4b28db4f5a0` |
| `HIP_VO_REVIEW.zip` | 3.3 MB | `453af6d5411716608618e8e8b87ced4ffe4b125416ed577dbf7b219cbd923b9e` |
| `HIP_CODE_REVIEW_REDACTED_20260813.zip` | 82.5 MB | `f9d4c986bff405e024ebaf9cc03a5633ed4adcfc11d8927cff939ee8645972f2` |

Checksums are recorded in `SHA256SUMS.txt` in the same folder, **taken before the move**,
so the integrity of the evidence is provable rather than asserted. A `README.txt` in the
folder explains why the files are there, what the enumeration found, and that FM3-2 is
corrected — so the folder reads correctly to someone who never sees this dispatch.

**The quarantine justification does not depend on the exposure question.** All three are
STALE (FM 3): 10 / 66 / 31 commits of drift, findings never returned. They must not be
sent, and moving them out of the upload folder is what stops that. **The current packages
remain in `~/Desktop/HIP_REVIEW_20260814/` and were not touched.**

The three 2026-08-12 packages were **left on the Desktop** — outside this dispatch's named
scope, and §3.3 shows they carry nothing that warrants moving them without being asked.

---

## 6. WHAT THIS DISPATCH DID NOT DO

- **Rotated no credential.** No Neo4j password, no certificate, no key, in any tree.
- **Restarted no service.** All six Neo4j instances (7687–7692) and Ollama were left
  running. No lane was interrupted.
- **Touched no provider account**, as instructed — and the list of provider rotations to
  hand over is **empty**, which is the finding, not an omission.
- **Deleted nothing**, including the extraction workspace's source files. The scratch
  extraction was destroyed after scanning; the packages themselves are intact.
- **Did not edit FM 3's dispatch doc or board row.** They stand as written and are
  superseded on this one point by §2.
- **Did not strip network addressing from the pending FM 3 packages.** §4.2 — a scope
  change awaiting a decision.

---

## 7. NEEDS BILL

1. **Confirm the STOP.** If you have evidence a credential left the box that this
   enumeration missed — a package built by a route I have not seen, a paste into a chat, a
   file sent by another channel — **say so and FM 5 rotates immediately.** The enumeration
   covers the six zip packages on this machine and nothing else, and that limit is stated
   rather than glossed.
2. **Tailscale-side mitigation** for the addressing in §4 — ACL review or node/tailnet
   rename. Provider-side, listed not touched.
3. **The three pending FM 3 packages** — send as built, or rebuild with the addressing
   stripped first.
4. **Whether the quarantined zips are eventually deleted.** They are evidence; deleting
   them is a destructive write and is not pre-authorized.

---

## 8. CLAIM IMPACT

```
CLAIM IMPACT: none
```

No evidence bearing on a ledger claim was produced, and no governed surface was touched.

---

## 9. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `~/hip-roadmap` @ `roadmap`.
- Coordination check ran **before** any action: board read (NC 5 and VD-60 IN FLIGHT), all
  seven `hip_lock.py who` resources reported **free**, six Neo4j instances and Ollama
  listening. **Nothing was restarted, so no in-flight run was disturbed.**
- Board: **FM 4 claimed at `7126eb4`** (first commit of the dispatch), closed by this
  dispatch's own commit.
- Enumeration evidence: 4,921 text files scanned; the extraction workspace was mode-700
  and was removed after the scan.
