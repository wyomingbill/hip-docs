# SPEC_ANCHOR_LAPTOP_FETCH — laptop-side pull, drawer, and verification

Status: PLAN — nothing on the laptop side is built yet. This document specifies it.
Reconciled-Against: roadmap `c66d787` (mini-side state at time of writing)

**Hand this document to a fresh session on the laptop. It assumes no prior context about
HIP, this repo, or any other document in it. Everything needed is below or explicitly
named as something you must go get.**

---

## 0. What this is, in five sentences

HIP is a personal household AI system running on a Mac mini ("the mini"). It keeps an
append-only, hash-chained event log (called the HEL — "hash-chained event ledger") of
governance-relevant decisions. That log is written, read, and could in principle be
*rewritten* by the same process on the same disk under the same user account — so if
something on the mini were ever compromised, it could rewrite its own history and the
mini's own verification code would not notice, because it trusts the very chain it is
checking. The fix is to periodically hand a small, tamper-evident fingerprint of the
chain's current position — called an "anchor" — to a *second machine the mini cannot
reach*. That second machine is your laptop. This document is the laptop's half of that
system: how to fetch anchors, hold them, and use them to check the mini's ledger later.
**Nothing here resists a rewrite. It only makes a rewrite detectable after the fact**, and
only for events at or before the oldest anchor you're holding.

---

## 1. The mini-side source directory (the "drawer")

Anchors are written by the mini into a single directory, outside any git checkout:

```
~/hip-anchors/
```

On the actual mini this is `[REDACTED-USER-PATH]/hip-anchors/`. The mini's hostname on the local
network is `[REDACTED-MACHINE-NAME]`, user `bill-ai`. (SSH — macOS "Remote Login" — must
already be enabled on the mini and reachable from wherever the laptop is; that is a
prerequisite to check on the mini side, not something this document configures.)

The mini never pushes to the laptop and holds no credential that could reach the laptop —
see §5. Everything below is initiated **from the laptop**.

---

## 2. Filename convention and record format

Each anchor is one file:

```
anchor-<seq, zero-padded to 12 digits>-<UTC timestamp, YYYYMMDDTHHMMSSZ>.json
```

Example, a real file from the drawer at time of writing:

```
anchor-000000007074-20260801T202827Z.json
```

The zero-padded seq means a plain `ls` on the directory sorts the files into chain order —
you never need to parse a file to know their order. The timestamp in the filename is
derived from the record's own `anchored_at` field, so a filename can never disagree with
what's inside it.

Each file is written **read-only (mode 0444)** by the mini and contains exactly one line of
compact JSON. This is the full, real content of the file above:

```json
{"anchor_version":"hel-anchor.v1","anchored_at":"2026-08-01T20:28:27.344641+00:00","event_count":7074,"head_hash":"sha256:140ea35ebc48cb6fbc2b2b05dee363e4af589c983122fbfdd956b43012ab8a5e","segment":"hel-000001.jsonl","seq":7074}
```

The complete, permitted set of keys — nothing else will ever appear, and if it did you
should treat the file as suspect rather than trust it:

| key | meaning |
|---|---|
| `anchor_version` | format tag, currently `"hel-anchor.v1"` |
| `seq` | chain position being attested (an integer) |
| `head_hash` | the chained hash at that position, `"sha256:<hex>"` |
| `segment` | which ledger segment file this position lives in (basename only, e.g. `hel-000001.jsonl`) |
| `event_count` | how many events the mini had observed at or below this seq when it wrote the anchor |
| `anchored_at` | when the anchor was produced (UTC ISO-8601) — **not** an event timestamp |

Note what is deliberately absent: no signature. The mini does not sign anchors, on
purpose — any signing key the mini could use, a compromised mini could also use, which
would make the signature worthless as evidence. **Authority here comes entirely from your
laptop having possessed a given anchor file since a known point in time** — the file's
existence and unaltered content on your disk is the evidence, not a cryptographic
signature inside it.

Also note: **two anchor files can legitimately share the same `seq`** with different
timestamps. That is not a bug or a duplicate to discard — it means the mini's chain head
had not moved between those two times, which is itself useful evidence (it rules out both
new writes and silent rewrites in that interval). Never delete one on the assumption it's
redundant.

---

## 3. The fetch: SSH from the laptop, copy new anchors only, never delete

Run this **from the laptop**, never from the mini. It copies any anchor files that don't
already exist locally, and touches nothing else on the mini.

```bash
mkdir -p ~/hip-anchors-laptop
rsync -av --ignore-existing \
  [REDACTED-USER]@[REDACTED-MACHINE-NAME]:hip-anchors/ \
  ~/hip-anchors-laptop/
```

`--ignore-existing` is the load-bearing flag: it makes this an append-only pull. A file
that already exists locally is never touched, never re-copied, never overwritten — which
matters because if the mini were ever compromised and an attacker tried to alter a
previously-fetched anchor on the mini side, `rsync` would not pull that altered version
over an existing local copy. The only way an anchor changes on your laptop is if it never
existed there before.

If `rsync` isn't available, the equivalent with plain `scp` (less safe — it does not skip
existing files on its own, so check before running it a second time, or just always run
into a fresh empty directory and diff):

```bash
scp '[REDACTED-USER]@[REDACTED-MACHINE-NAME]:hip-anchors/anchor-*.json' ~/hip-anchors-laptop/
```

Run this periodically — by hand is fine. There is no push mechanism and there should never
be one (§5).

---

## 4. The local store: append-only, one file per anchor, nothing overwritten

`~/hip-anchors-laptop/` (or wherever you point §3 at) is the laptop-side drawer. Treat it
the same way the mini treats its own:

- **Never edit a file in this directory.** Never delete one, even one that looks
  redundant (see the same-seq note in §2).
- **Never re-run a fetch into the same directory with a tool that overwrites.** `rsync
  --ignore-existing` and a fresh `scp` into an empty dir are both safe; a bare `scp` into
  an existing populated dir is not, unless you've confirmed it can't clobber.
- If you want extra safety, `chmod 444` every file after fetching (matching what the mini
  already does) so a later mistake can't overwrite them even with `>`.
- Back this directory up somewhere separate from your normal laptop backup if you want the
  anchors to survive laptop loss too — that's a judgment call, not part of this spec.

---

## 5. Verifying a fetched anchor against the mini's ledger

An anchor by itself only proves *that a chain position existed at some point*. To check
whether the mini's **current** ledger still agrees with an anchor you hold, you need two
more things: a copy of the mini's ledger event data, and the verification code.

**5a. Pull a read-only copy of the ledger segments — never the keys.**

The ledger lives on the mini at `~/hip-roadmap/ledger/`. It contains segment files named
`hel-<6 digits>.jsonl` (the actual chained events — this is what you check against) and a
`keys/` subdirectory (cryptographic key material, mode `700` on the mini). **Never fetch
`ledger/keys/`.** It is not needed for verification — anchoring and verification only ever
touch hashes, never payloads or keys — and pulling it would hand your laptop something it
has no business holding.

```bash
mkdir -p ~/hip-ledger-laptop
rsync -av \
  --include='hel-*.jsonl' --exclude='keys/' --exclude='*' \
  [REDACTED-USER]@[REDACTED-MACHINE-NAME]:hip-roadmap/ledger/ \
  ~/hip-ledger-laptop/
```

This one is a read-only mirror, not append-only-forever like the anchor drawer — it's fine
to re-sync it each time you want to check, since its whole purpose is to reflect current
mini state (that's exactly what you're checking against the *old, fixed* anchor).

**5b. Get the verification code.** Do not fetch this from the mini — pull it from the
project's git remote instead, so the code you're checking with isn't itself something a
compromised mini could have handed you:

```bash
git clone https://github.com/wyomingbill/hip-dev.git ~/hip-roadmap-laptop-readonly
```

The two files that matter are `harness/ledger_anchor.py` and `harness/epistemic_ledger.py`.

**5c. Run the check.** From `~/hip-roadmap-laptop-readonly`, with `HIP_HEL_DIR` pointed at
the copy you pulled in 5a:

```bash
cd ~/hip-roadmap-laptop-readonly
HIP_HEL_DIR=~/hip-ledger-laptop python3 - <<'PY'
import json, glob
from harness.ledger_anchor import verify_against_anchor

for path in sorted(glob.glob("/Users/<you>/hip-anchors-laptop/anchor-*.json")):
    anchor = json.loads(open(path).read())
    ok, msg = verify_against_anchor(anchor)
    print(f"{path}: {'OK' if ok else 'MISMATCH'} — {msg}")
PY
```

(Replace `/Users/<you>/` with your actual home directory path.)

**What this actually checks**, per anchor: every event in the pulled ledger copy at or
below the anchor's `seq` recomputes to its own stored hash and links correctly to the
previous event's hash (catches a rewrite that forgot to re-chain), **and** the event
sitting exactly at the anchored `seq` carries the exact `head_hash` the anchor recorded.

**What a mismatch means: evidence, not an error.** `verify_against_anchor` never raises an
exception on a mismatch — it returns `(False, message)` deliberately, because a mismatch
is not a bug in this tool, it's the thing this whole system exists to surface. If you get
`MISMATCH`, it means the mini's ledger, as it exists right now, disagrees with a state you
captured and have held, unaltered, since an earlier point in time. Concretely: **the chain
was rewritten at or before that anchor's position, after the anchor was taken.** That is
worth treating seriously — it's exactly the compromise scenario this system was built to
catch. A mismatch does not by itself tell you what changed or why; it tells you *that*
something did, and *no later than which point*. The oldest anchor that still matches
brackets how far back the rewrite could reach; if you hold multiple anchors, checking all
of them (oldest to newest) narrows the window further.

A `MATCH` result is not a guarantee nothing is wrong elsewhere — it only proves the chain
has not been altered at or below that specific seq since that specific anchor was taken.
Events after the last anchor you're holding are outside what any anchor can attest to.

---

## 6. What the laptop must NEVER do

- **Never hold a credential the mini could use.** No SSH key, token, password, or
  certificate that grants the mini (or anything running on it) any access to the laptop —
  not to this directory, not to anything else. The entire design depends on this being
  true in principle, not just in practice: if the mini held or could obtain such a
  credential, a compromise of the mini would reach the laptop too, and the laptop drawer
  would stop being independent evidence.
- **Never let the mini initiate a connection, transfer, or command toward the laptop.**
  Every action in this document runs *from* the laptop, *to* the mini — SSH out, `rsync`
  pulling, `git clone` from GitHub (not from the mini). If at any point a setup would have
  the mini push, upload, notify, or otherwise reach outward toward the laptop, that setup
  is wrong regardless of how convenient it seems — it recreates exactly the channel this
  design exists to not have. The mini-side code (`harness/anchor_emitter.py`) is written
  with **no networking code at all** — no sockets, no HTTP client, no SSH client, nothing
  — and that absence is enforced by an automated check on the mini side, not left as a
  promise. The laptop side must hold up its own half of that same guarantee.
- **Never treat a `MATCH` result as proof the mini is currently trustworthy.** It only
  proves the chain hasn't moved, at or below one specific position, since one specific
  past moment. It says nothing about events after the last anchor, and nothing about
  anything outside the ledger entirely.
- **Never delete or edit anything in either local drawer** (`~/hip-anchors-laptop/`, and
  by extension the anchor files inside it) once fetched, even ones that look redundant or
  suspicious. A suspicious-looking anchor is itself evidence — deleting it destroys the
  thing you'd need to explain what happened.
