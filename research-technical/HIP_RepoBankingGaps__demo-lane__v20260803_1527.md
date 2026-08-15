TYPE: STATE
Version: v20260803_1527 (Mountain Time, per the CLAUDE.md Naming Law)
Reconciled-Against: 2026-08-03 (date-tested — read at filing, not remembered)

A snapshot of what still had to reach this repo from the demo/cutover lane as of
2026-08-03 — chat output folders, /tmp, ~/Downloads, and conversation scrollback, none of
it in git. THIS IS THE DOCUMENT THAT MOTIVATED INDEX BANK 1: everything it names as
TIER 1/2/3 is what this dispatch banks (see docs/INDEX.md and MANIFEST.md rows filed the
same day). Describes a state, not a build or a design — carries no lifecycle Status field
by design.
Source file: HIP_RepoBankingGaps__demo-lane__20260803.md (~/Downloads), banked verbatim,
unedited below this line.

---

# What still has to reach the repo — demo/cutover lane, 2026-08-01 → 08-03

Everything below exists **only** in a chat output folder, `/tmp`, `~/Downloads`, or a
conversation scrollback. None of it is in a git repo. `/tmp` is cleared on reboot and this
machine has restarted several times during this work.

Ordered by what would hurt most to lose.

---

## TIER 1 — load-bearing, would have to be redone

### 1. The two probe sets (400 items)
- `HIP_ProbeSet1_General_200.txt` — merged from two source lists, with run instructions,
  scoring scheme, and the 33 high-ambiguity items pulled into their own block
- `HIP_ProbeSet2_Governance_200_labeled.txt` — 200 rows with Expected outcome, Resolvable
  flag, and Reason attached to each, plus three focus blocks
- **Where:** chat outputs only
- **Goes to:** `eval/probes/` or `docs/research-technical/`
- **Why it matters:** Set 1 has already been run once. Without the file the run is not
  reproducible and Set 2 cannot run at all.

### 2. Voice 38's baseline results
- `/tmp/voice38_set1_results.csv` — per-item record data for 199 turns
- **Where:** `/tmp`, on a machine that reboots
- **Goes to:** `eval/probes/results/` or alongside the measurement docs
- **Why:** this is the only baseline the cutover's C9 comparison can be measured against.
  Lose it and C9 has no "before".

### 3. The four cutover reports
- `~/Downloads/cutover_comparison.md` (13,840 bytes) — the 16-turn same-vs-different
  comparison, the central evidence for C3/C4
- `~/Downloads/cutover4_report.md` (10,800 bytes) — the C5 and caveat live verification
- `~/Downloads/cutover5_reconcile.md` (14,033 bytes) — the duplicate-port analysis
- `~/Downloads/cutover6_report.md` (7,076 bytes) — the header-fix confirmation
- **Goes to:** `docs/reviews/` in the roadmap repo, registered in INDEX
- **Why:** REQ_DEMO_CUTOVER's acceptance rows cite these. The REQ is filed; its evidence
  is not.

### 4. The two conversation-memory reviews and the brief they answered
- The Fable review — **conversation scrollback only**, never written to a file
- The ChatGPT review — `~/Downloads/chatgpt research context.txt` (note the spaces)
- `HIP_ConversationMemory_ReviewBrief.md` — chat outputs only
- **Status:** Voice 33 was deferred; another session may have banked some of this
  independently on `voice-port` at `547df44`. **Verify before redoing.**
- **Goes to:** `docs/reviews/` and `docs/design/`
- **Why:** both reviewers independently killed a design before it was built. That reasoning
  is the most valuable thing produced in this lane and one half of it has no file at all.

### 5. The two evaluation-methodology reviews and their prompt
- `~/Downloads/gpt-test_research` and `~/Downloads/fable-test_research` (hyphens, no
  extension)
- `HIP_EvalMethodology_ReviewPrompt.md` — chat outputs only
- **Status:** Voice 36 was written; completion never confirmed
- **Goes to:** `docs/reviews/` and `docs/research-technical/`
- **Why:** these name the three builds the testing standard now depends on.

---

## TIER 2 — defects and findings with no register entry

### 6. The Epistemic State panel cannot show any v2 fact's value
`/api/fact_history` only decrypts when `key_version == 1` or an `as_member` param is
supplied. `demo.html:991` never sends `as_member`. So **every** partition-crypto fact
renders as `—` in the panel, not just Ray's medication. Confirmed at the data layer.
Searched `docs/` — not documented anywhere as a named limitation.

**Either** pass the caller identity so values render, **or** file it as a known limit and
decide what the presenter says about the dash. Currently neither.

### 7. `maya.npz` and `sam.npz` fail Fernet decryption
Both touched 2026-08-03 at 13:16; `bill.npz` is untouched since Jul 31 and decrypts fine.
`InvalidToken` against the current key. Found incidentally, not investigated.

**Consequence if it persists:** the scripted-voice demo depends on those two prints. If
they cannot be decrypted, Maya and Sam cannot be recognised from audio and the whole
scripted-voice beat breaks.

Backup exists at `~/hip-harness-backups/voiceprints_20260803_140540/` (outside the repo,
SHA-256 verified).

### 8. `transcription_ms` is structurally null on the demo path
`process_text_query` never does its own STT, so a spoken turn's record is indistinguishable
from a typed one. Named in `REQ_VOICE_TRACE_CAPTURE`'s acceptance rows but not filed as a
defect.

### 9. Voice 38's two live findings
- 6 leaks, 4 of them clean and unwarranted, all on high-ambiguity questions
- 7 items produced the exact structural refusal string with `guard_triggered=False` and
  `path=generation`

The second is the same defect the other lane found as PW010/PW015, arrived at
independently. Neither is on the demo lane's register.

### 10. The recording script's stale-stdin bug
`/tmp/voice12_record_bill.py` skips prompts — `input()` consumes a buffered newline left
over from audio capture. A rewrite dispatch is written and unfired. The script itself is
in `/tmp` and will not survive a reboot.

---

## TIER 3 — state that must not be forgotten

### 11. Adaptation is currently disabled
`~/hip-harness/config.yaml` line 125, `routing.speaker_id.adaptation.enabled: false`.
**Uncommitted working-tree edit**, made for the microphone run. Old value preserved in a
trailing comment.

**This must be reverted after the run.** If it is committed by accident, or forgotten,
passive voiceprint adaptation is off in whatever ships.

### 12. Nothing in this lane has been pushed
- `demo-cutover-build` — several commits, local only
- `hip-harness/voice-latency` — seven voice commits, local only
- `hip-vo/voice-port` — the voice port, local only

A disk failure loses all of it.

### 13. The run-of-show documents from 07-30
Four `.docx` files produced in a chat output folder and never landed in
`docs/deliverables/`. Flagged as orphaned on 2026-07-30 and still orphaned. The run-of-show
of record is now behind the 4-turn boundary script, the reworded park replies, and the
Epistemic State panel.

---

## SUGGESTED SEQUENCE

1. **Save the files off the machine first.** Everything in `/tmp` is one reboot from gone.
2. **Push the three branches.** Cheapest insurance available.
3. **Bank Tier 1** as a single dispatch — reviews to `docs/reviews/`, probe sets and
   results to `eval/probes/`, briefs to `docs/design/`, all registered.
4. **File Tier 2** as register entries. No fixes, just numbered and visible.
5. **Revert the adaptation flag** once the recording run is done, or now if it is deferred.
