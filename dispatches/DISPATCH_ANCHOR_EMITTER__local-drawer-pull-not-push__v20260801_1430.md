# DISPATCH_ANCHOR_EMITTER
Status: BUILT
Reconciled-Against: 19d6f38 (HEAD at dispatch start)
Design: `docs/design/DESIGN_LEDGER_ANCHOR__detectability-not-resistance__v20260801_1300.md` (D-89)
Dispatch: D-90, 2026-08-01
**Status proposed: NONE. Nothing ruled MET. This is HALF the control — the laptop drawer is not built here.**

Gate passed: bill-ai / [REDACTED-MACHINE-NAME] / `~/hip-roadmap` / `roadmap` @ `19d6f38`, clean.
`~/hip-vo`, `~/hip-dev`, `~/hip-harness` NOT touched. **Nothing ruled MET.**

**THIS IS STILL ONLY HALF THE CONTROL.** The drawer on your laptop is not built by this
dispatch. Until the laptop has actually fetched these records and holds them, they sit on
the same disk as the ledger they attest, readable and deletable by the same uid, and
**detect nothing**. `REQ_ARCHITECTURE_BOUNDARY` §5.2's missing property — an audit anchor
the writer cannot reach — is still missing. What exists now is the emitting half.

---

## What was built

| Piece | Path |
|---|---|
| the emitter | `harness/anchor_emitter.py` |
| acceptance battery, 21 cases | `eval/test_anchor_emitter.py` (13th standing battery) |
| manual runner | `scripts/emit_anchor.sh` |
| daily schedule, **NOT installed** | `scripts/com.hip.anchor.plist.template` |

**No pusher, no uploader, no outbound call, no credential.** Asserted structurally, not
promised: `test_ceil_emit_module_has_no_network_or_subprocess_import` walks the emitter's
import graph and fails if `socket`, `http`, `urllib`, `requests`, `httpx`, `paramiko`,
`boto3`, `subprocess`, `ssl` or friends ever appear. A pusher cannot be added to this
module without turning the suite red, and unlike a source regex it cannot be fooled by a
comment or evaded by an alias.

## The drawer

```
~/hip-anchors/
```

**Outside every git checkout, deliberately.** Anchors are evidence, not source: inside a
worktree they would depend on which branch is checked out, could be swept into a commit,
and would move when a checkout moves. Asserted in
`test_ceil_emit_default_drawer_is_outside_every_git_checkout`.

Filename: `anchor-<seq, zero-padded to 12>-<UTC stamp>.json`

```
anchor-000000007074-20260801T202827Z.json
```

Seq is zero-padded so **lexical sort equals chain order** — the laptop can `ls` and get
chronological order without parsing anything. The UTC stamp is derived from the record's
own `anchored_at`, so a filename cannot disagree with its contents (asserted).

Files are written `0444` via `O_EXCL`, so even a race cannot clobber a written anchor.

## No signing — by D-89's ruling, unchanged

Any key HIP can read, a compromised HIP can read. Authority comes from **your laptop's
possession of a record at a point in time**, not from a secret on the mini. The emitter
holds no key and produces no signature.

---

## Scheduling — and a decision you need to know about

**I did NOT install a launchd agent.** You already run several (`com.hip.autogate`,
`com.hip.demo.dashboard`, `com.hip.voice.orch`, `com.hip.voice`, `com.hip.voice.mem0`),
and quietly adding a sixth background service to your machine is not something a dispatch
should do without you saying so. Verified after the run: `com.hip.anchor.plist` is **not**
in `~/Library/LaunchAgents/`.

**By hand:**
```
~/hip-roadmap/scripts/emit_anchor.sh
```
Safe to run repeatedly. Exits 0 either way.

**Daily, if you want it — one command, your call:**
```
cp ~/hip-roadmap/scripts/com.hip.anchor.plist.template \
   ~/Library/LaunchAgents/com.hip.anchor.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.hip.anchor.plist
```
Daily at 03:15 local, `RunAtLoad` false (an anchor at boot attests a head nobody asked
about). To remove: `launchctl bootout gui/$(id -u)/com.hip.anchor && rm ~/Library/LaunchAgents/com.hip.anchor.plist`.

Reminder from D-89 §4: **the interval IS the detection window.** A rewrite of events
appended between two anchors is undetectable by this scheme, forever.

---

## Acceptance — all four, with fault twins

| # | Criterion | Twin |
|---|---|---|
| 1 | an emitted anchor matches the ledger head at emit time | a stale `head_hash` **must** fail verification |
| 2 | the emitter refuses to overwrite an existing anchor | a plain `open(path,'w')` **must** clobber — proving the refusal does work |
| 3 | the anchor leaks nothing (record **and** filename) | a payload-bearing record is refused **before it lands** |
| 4 | a crypto-shred after an anchor does not invalidate it | a rewrite after the anchor **must** be detected |

Twin 4 is the discriminating one: "survives a lawful shred" is only meaningful if
something *doesn't*. Without it the criterion would be satisfied by an anchor that
survives everything, including tampering.

**Anti-vacuity on every scan**, including the sharpest: the leak test would pass against
an anchor leaking everything if the payloads had never contained the canaries, so
`test_ceil_emit_anti_vacuity_canaries_are_really_in_the_ledger` proves they were there.
The import scan likewise asserts it parsed a real module with real entry points.

## One behavior found by exercising the manual path, and kept

Running the emitter twice within the same second refuses; running it again 2 seconds later
writes a **second file for the same seq**, differing only in `anchored_at`. I checked
whether that was a defect and concluded it is not, so I pinned it rather than deduping:

**Two anchors of an unchanged head are evidence.** They attest the head did not move across
that interval — ruling out both appends *and* rewrites in between. Deduplicating by `seq`
would throw that away. The only refusal is a same-second collision, where the two records
would be byte-identical and the second carries no additional evidence. Both behaviors are
now pinned by tests.

## Real anchors emitted

Two, against the live ledger at head **seq 7074**, while testing the manual path. They are
correctly-formed anchors of the real chain, so I left them in place rather than deleting
them — they are the first genuine entries in the drawer:

```
anchor-000000007074-20260801T202827Z.json
anchor-000000007074-20260801T202846Z.json
```

Contents of the first, in full — this is exactly what the laptop will fetch:

```json
{"anchor_version":"hel-anchor.v1","anchored_at":"2026-08-01T20:28:27.344641+00:00",
 "event_count":7074,"head_hash":"sha256:140ea35ebc48cb6fbc2b2b05dee363e4af589c983122fbfdd956b43012ab8a5e",
 "segment":"hel-000001.jsonl","seq":7074}
```

No member id, no attribute, no value, no actor.

---

## Harness

```
standing batteries (13 files): 183 passed, 9 xfailed   (test_anchor_emitter.py: 21 new)
== AUDIT:  8/8   == DISC: 1/1   == L7: 27/27
== L7V2:   27/28 (1 opt-in skip)   == SCHEMA: 1/1   == VOICE: 1/1
RATCHET PASS — no scenario regressed vs baseline.   0 scenario FAILs.
```

All five ABSOLUTE checks read individually from the log: **G0 PASS, PSA1 PASS, CTX-STRIP
PASS, LI1 PASS, CS1 PASS.** `--full` not attempted — TD-129's memory guard refuses it on
this machine state, as anticipated.

**Battery hermeticity verified, not claimed.** These cases call `destroy_member_key`, so it
mattered: each builds its own ledger (`HIP_HEL_DIR`) and its own drawer (`HIP_ANCHOR_DIR`)
under `tmp_path`. The real ledger is intact and the real `member_maya.key` is untouched.

## What is still missing

1. **The laptop side.** Not built here — see the spec below.
2. Whether a countersignature is wanted for v1, or whether possession-with-timestamp is
   enough to start.
3. Whether you want the daily agent installed.
