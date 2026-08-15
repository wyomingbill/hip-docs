# DESIGN_LEDGER_ANCHOR — anchoring the HEL head: detectability, not resistance
Status: BUILT (both halves — see the D-98 update below; §3's target decision and §7's
"not built" are superseded IN PLACE, not by a new file — see the note for why)
Reconciled-Against: 6698a49 (roadmap HEAD at dispatch start); updated 2026-08-01 (D-98)
Dispatch: D-89, 2026-08-01 (design); D-90 (mini emitter); D-95 (laptop spec); D-98 (laptop
build + this update)
Authority: `REQ_ARCHITECTURE_BOUNDARY__reference-monitor-threat-model-and-contracted-clients__v20260801_0919.md` §5.2

**THIS BUYS DETECTABILITY, NOT RESISTANCE. THAT HAS NOT CHANGED AND WILL NOT.** Nothing
here stops a rewrite. It makes a rewrite *visible* to someone who held an earlier head, and
only up to the position of the oldest anchor still held. Custody separation — a ledger
writer under a different UID that the core cannot reach — is a different, later build, and
this remains not a step toward it, even now that the mechanism is complete end to end.

**UPDATE, 2026-08-01 (D-98) — the mechanism is now a working control, not just a
mechanism.** Updated IN PLACE rather than superseded by a new versioned file: the
document's central thesis (detectability, not resistance) is unchanged and is restated
above, unweakened. What changed is only the answer to "is it built" — §3's target decision
and §7's "not built" characterization, below, no longer describe current reality and are
corrected where they appear, with the original reasoning left intact and dated so the
history of the decision is not lost. A superseding rewrite would have obscured, not
clarified, that this is the same design, now finished.

**Rule nothing MET.** No requirement is ruled by this document — see §5.2's own text in
`REQ_ARCHITECTURE_BOUNDARY` for the property-level statement, updated alongside this file.

---

## 1. The problem, restated from the REQ

The HEL is written, custodied, and verified by the same process, on the same disk, under
the same UID as every other HIP process. Verified this dispatch, not recalled: `ledger/`
and `ledger/keys` are `bill-ai:staff`, **uid 501** — the uid every HIP process runs as.

Any of them can rewrite the chain from genesis and re-hash it, and
`epistemic_ledger.verify()` will still return `True`, because it reads the chain it is
supposed to distrust. Under the ruled threat model — careless code, hostile household
member, compromised dependency, remote attacker — **that detects nothing.**

The ledger is otherwise strong: hash-chained, `F_FULLFSYNC` before the reply returns,
per-member AES-256-GCM payload keys, chain hash over ciphertext, flock'd ordering. The
gap is custody, not construction.

---

## 2. WHAT gets anchored

The chain head only. `harness/ledger_anchor.py::ANCHOR_FIELDS` is the complete permitted
key set, enforced (not documented) by `anchor_leaks()` and by `anchor_to_line()`, which
refuses to serialize a record carrying anything else:

| Field | Why |
|---|---|
| `anchor_version` | format tag (`hel-anchor.v1`) |
| `seq` | chain position being attested |
| `head_hash` | the chained hash at that position |
| `segment` | segment **basename** only — never a path |
| `event_count` | events observed at or below `seq` |
| `anchored_at` | when the record was produced — NOT an event timestamp |

**No payloads, no member identifiers, no attribute names, no actor.** The last one
matters specifically: `actor.id` is plaintext in the immortal envelope (HEL-ACTOR-1, a
known and filed limitation), so copying the tail event through would leak a member id.
The anchor therefore carries chain position and nothing drawn from the event body.

Asserted, not assumed: `test_ceil_anchor_record_contains_no_canary` serializes the record
and searches for the attribute, subject, and value that went into the fixture payloads —
with `test_ceil_anchor_canaries_are_actually_present_in_the_ledger` proving the canaries
were really there, so the leak test cannot pass vacuously.

---

## 3. WHERE — **STOPPED. This is the ambiguity, and it also decides §6.**

The dispatch requires a target "not writable by the UID that runs HIP," and says to
assess rather than assume. Assessed on this box:

| Option | Finding |
|---|---|
| Append-only remote (object-lock bucket etc.) | **No credentials exist** — `~/.aws/credentials`, `~/.config/gcloud`, `~/.azure` all absent. Nothing to write to. |
| Another tailnet device under a different credential | **`tailscale` CLI not available** on this box. No second device is reachable or credentialed, and no receiving service exists. |
| Printed / mailed digest | Available in principle, needs no infrastructure — but it is a **manual operator process**, not something this dispatch can build, and it needs Bill's decision on cadence and custody. |
| The git remote (`github.com/wyomingbill/hip-dev`) | **Fails the criterion.** HIP's own uid holds push credentials — this session has pushed with them all day — so it is writable by exactly the uid the anchor must be protected from. It is also not append-only (force-push). Rejected on the merits, not overlooked. |

**No target satisfying the stated criterion exists on this box today.** Selecting one
requires a credential and a decision that are Bill's, so per §2's instruction I stopped
rather than guessing.

**RESOLVED (D-90, 2026-08-01): Bill ruled the target is his laptop, transport PULL not
push.** None of the three assessed options above were chosen — the laptop is a fourth,
Bill's own hardware, reachable over SSH, to which HIP holds no credential in either
direction and which the mini cannot initiate a connection toward. **BUILT AND EXERCISED
(D-95's spec, executed 2026-08-01 per D-98):** `rsync -av --ignore-existing` pulled from
the laptop, laptop-initiated; two anchors at seq 7074 held read-only (mode 444) on the
laptop; a second fetch transferred nothing, live-proving the pull is genuinely append-only
rather than merely intended to be; a ledger mirror pulled `hel-*.jsonl` only, with
`ledger/keys/` excluded and its absence verified afterward on the laptop side, not assumed;
the verifier was cloned from the GitHub remote, not from the mini, so the checking code
itself did not pass through a channel the mini controls; both anchors verify **MATCH**
against `head_hash sha256:140ea35ebc48cb6fbc2b2b05dee363e4af589c983122fbfdd956b43012ab8a5e`
— confirmed independently from this box, the same value both anchor files on the mini's own
drawer carry.

The laptop-side steps above happened on a machine this session has no access to; recorded
here on the dispatch's account, the same way the choice to trust a REQ author's own
prior-session findings is handled elsewhere in this repo. What this session verified
directly, on this box: both anchor files in `~/hip-anchors/` (seq 7074) carry exactly the
cited `head_hash`.

### The signing key is the same question, and that is the important finding

The dispatch warns: *"if the signing key lives where the core can reach it, the anchor is
forgeable and you have built nothing."* On a single box with one uid, **any key the signer
can read, the core can read.** So a HIP-held signing key is forgeable by precisely the
adversaries anchoring exists to detect. There is no in-process arrangement that fixes
this — the same CPython argument from `REQ_ARCHITECTURE_BOUNDARY` §1 applies.

**The resolution is that HIP does not sign at all.** It emits an unsigned anchor record;
the **receiver countersigns and timestamps** it. The evidentiary weight then comes from
the receiver's possession of the record at a point in time, not from a secret HIP holds —
and HIP holds no forgeable key, because it holds none.

`build_anchor()` is therefore deliberately signature-free. **WHERE and the signing key are
one decision, not two**, and both are stopped together.

---

## 4. HOW OFTEN

Periodic plus on-demand. Recommended, **not ruled**:

- **Periodic:** daily. Cheap (one small record), and it bounds the exposure to a day.
- **On demand:** before and after any operator action on the ledger — key destruction,
  targeted erasure, backup, restore, migration.

**The tradeoff, stated plainly: the interval IS the detection window.** A rewrite of
events appended *between* two anchors is undetectable by this scheme, forever. Anchoring
at seq N proves nothing about events N+1 onward until the next anchor lands. Shortening
the interval shrinks the blind spot and costs almost nothing; the reason not to go to
every-event is that the receiver becomes a hard dependency on the write path, which
conflicts with the D-1 invariant that a governance record never blocks a turn.

A useful asymmetry: an anchor set gives two bounds at once — the **oldest** anchor bounds
how far back a rewrite could have reached undetected, the **newest** bounds how much
recent history is unprotected. `verify_against_anchors()` takes a set for this reason.

---

## 5. VERIFICATION — how a third party checks without HIP's cooperation

`verify_against_anchor(anchor, ledger_dir)` needs **no key, no HIP process, and no payload
access** — only the segment files and the anchor record. Two independent checks:

1. **Internal consistency** — every event at or below the anchored seq must recompute to
   its stored hash via `event_hash`, and `prev_hash` must link. A competent rewriter
   re-hashes consistently and *passes* this, which is exactly why (2) exists and why the
   ledger's own `verify()` is insufficient.
2. **The anchor comparison** — the event at the anchored seq must carry the anchored
   `head_hash`. A rewrite from genesis changes it. **This is the detection.**

Truncation is caught separately: if the anchored seq is absent, the chain is shorter than
the anchor attests.

A mismatch returns `(False, message)` rather than raising. That is deliberate — **a
mismatch is evidence, not an error**, and the caller decides what it means.

---

## 6. THE HIP-SPECIFIC CONSTRAINT — crypto-shred vs chain continuity

**Requirement:** a lawful crypto-shred must destroy payloads while preserving chain
continuity, and the anchoring scheme must not flag it as tampering.

**Proven, not asserted.** Run against a temp ledger this dispatch, and asserted as
standing acceptance cases:

### Why the head does not change for any past event

The chained hash covers `_HASH_FIELDS = (hel, seq, event_id, event_type, ts, actor,
correlation, payload_kid, payload_sha256, prev_hash)`. Two absences are load-bearing:

- **`payload` / `payload_enc` are NOT hashed.** `payload_sha256` — a digest over the
  *ciphertext* for member events — stands in for the content.
- **`erased` is NOT hashed.** It is added after the fact by `erase_payload`.

So, per path:

| Path | Segment files | Past event hashes | Head |
|---|---|---|---|
| `destroy_member_key()` | **untouched** — shreds the key file only | unchanged | advances by an **appended** `system.note` |
| `erase_payload(seq)` | content field nulled **in place** | **unchanged** — `hash`, `payload_sha256`, `prev_hash` all retained | advances by an **appended** `payload.erased` |

**Neither erasure path mutates any past event. Both only APPEND.**

Measured, temp ledger, D-89:

```
BASELINE           seq=4  verify=True
AFTER CRYPTO-SHRED seq=5  verify=True   prefix<=seq4 UNCHANGED: True
AFTER TOMBSTONE    seq=6  verify=True   prefix<=seq4 STILL UNCHANGED: True
```

The tombstoned event was **seq 2 — inside the checked prefix — and its own hash was
unchanged.** That is the decisive observation.

### The consequence

**An anchor at `(seq N, head H)` stays valid forever, however many lawful erasures
follow.** A lawful shred cannot alter any event at or below N, so it can never produce a
mismatch. A rewrite *can*, because it must change events at or below N to be useful.

This is a property of the design rather than luck, and the battery proves that too:
`test_ceil_anchor_fault_twin_a_payload_hashing_chain_would_break` shows that a chain
hashing `payload_enc` directly **would** change hash on tombstone — lawful erasure would
then look identical to tampering — and asserts that the real construction does not.

---

## 7. What was built, and what was not

**Built** (`harness/ledger_anchor.py`, `eval/test_ledger_anchor.py`, 14 cases, in
`scripts/run_harness.sh`):

- `build_anchor()` — the record. Signature-free, chain-position only.
- `anchor_leaks()` / `anchor_to_line()` — the leak predicate, and a serializer that
  refuses a leaky record.
- `verify_against_anchor()` / `verify_against_anchors()` — the third-party verifier.

**NOT built, at time of writing (D-89, 2026-08-01, morning):** the writer-to-target, and any
local signer. Both were blocked on §3's then-unmade decision. Building a local signer with
a locally-readable key would have produced something that *looks* like a control and is
forgeable by the adversaries it names — the exact trap the dispatch warned about, and still
the reason no local signer exists today (see below — that reasoning did not change).

**UPDATE (D-90 + D-95 + D-98, same day): the writer-to-target IS NOW BUILT, on both ends,
and exercised.** Mini side (D-90): `harness/anchor_emitter.py` writes to `~/hip-anchors/`,
no networking code of any kind, asserted by an import-graph check rather than left as a
promise. Laptop side (D-95's spec, D-98's execution): pull-only fetch, append-only local
store, ledger-segment mirror excluding `ledger/keys/`, and a verifier run against anchors
held on the laptop — all detailed in §3's resolution note above. **No local signer was
built, and that was not a shortfall — it was never the plan.** The design was always that
the receiver countersigns, not that HIP signs (§3, "The signing key is the same question").
What is still missing is the countersignature itself: the laptop currently holds anchors
append-only and read-only, but does not yet cryptographically countersign or timestamp
them. Evidentiary weight today rests on the laptop's unsigned possession of an unaltered
file since fetch time — real, but weaker than a countersignature would make it. See §8.

**So: `REQ_ARCHITECTURE_BOUNDARY` §5.2 recorded "an audit anchor the writer cannot reach"
as a property that did not exist. It now does — with the countersignature gap named above
as the honest limit of what "exists" means here, not glossed over.** The property is: a
second machine, unreachable by HIP's own UID and holding no credential from it, possesses a
fingerprint of the chain's position from an earlier point in time, sufficient to detect (not
prevent) a rewrite at or before that position. That is now true and was independently
checked from the mini side (§3). What was previously true — "this is a MECHANISM, not a
CONTROL" — is now the reverse for the anchoring half specifically: the mechanism has an
operating receiver, which is what made it a control. It remains, as it always will,
DETECTABILITY and not RESISTANCE — see the top of this document.

## 8. Open, for Bill

1. ~~**The target** (§3) — which of the three, and with what credential.~~ **RESOLVED
   (D-90): the laptop, PULL not push. Built and exercised (D-95, D-98).**
2. **Cadence is still NOT SET.** §4's "daily" is still only a recommendation, not a
   ruling — nothing changed here today. **No launchd job is installed on either machine.**
   The mini side has a manual runner (`scripts/emit_anchor.sh`) and an uninstalled daily
   plist template, exactly as D-90 left them; the laptop side's fetch (§3 above) was run by
   hand for D-98's proof and has no scheduled job either. Until one or both are scheduled,
   the detection window (§4) is bounded only by however often someone remembers to run
   both steps by hand — which could be arbitrarily long, undermining the "cheap, shrinks
   the blind spot" case for a short interval that §4 argues for.
3. **The receiver's countersignature is still unbuilt.** Still open in exactly the form
   this section originally posed it — whether it's required for v1 or whether
   possession-with-timestamp is enough to start — except it is no longer a hypothetical
   about a not-yet-built receiver: the receiver exists now and is running without one.
   **Evidentiary weight today rests on the laptop's possession alone** — an unsigned file,
   held read-only and append-only, that nothing on the mini can reach or alter. That is
   real evidence (§3's resolution note), but it is possession-based, not cryptographic:
   anyone who can be convinced the laptop's disk is what it claims to be has to trust that
   claim, not verify a signature independent of it.
4. Whether anchor submission may ever block a turn. Recommended **no** — it would conflict
   with the D-1 invariant that the governance record never changes the governance outcome.
   Unaffected by today's update; still open, still recommended no.
