# HIP Member Isolation — Dyad Custody Model: Custodial Keys, Entry/Exit, Overlapping Dyads
Status: PLAN
Reconciled-Against: main 47851d7 (code read 2026-07-18); extends HIP_MemberIsolation__crypto-partition-and-recovery-design__v20260718_1117.md

**Type:** Architecture spec. No production code. Extends the prior member-
isolation design; does not replace it. §2 (envelope + asymmetric per-member
keys), §4 (2-of-3 threshold recovery), §5 (the 11 server-side key-derivation
sites), and §6 (no-flag-day migration) of the prior doc are assumed and built
on. This spec changes the **reader set** DEKs are sealed to and adds the
**dyad** as a first-class crypto unit. Every current-state claim carries a
`file:line`. Where a claim cannot hold cryptographically, it is marked, not
designed around.

---

## UPDATE 2026-07-20 — RATIFIED DYAD ACCESS MODEL (care-team key class + epochs)

Bill ratified the dyad-private access model (two-review reconciled; decision
recorded in `REQ_PARTITION_CUSTODY`, resolving REQ_CRYPTO_HARNESS_V2
ambiguity 1). Two consequences for THIS spec's data model. **This is a build
extension to Phase 1's dyad-keys model** (`REQ_CRYPTO_P1_DYAD_KEYS` built the
two-hop dyad unwrap; nothing below is built):

**1. A third key class: the care-team key.** The single "dyad-private" class
is split into PAIR-PRIVATE (sealed to one dyad's `D_pub`, exactly the §1
model, unchanged) and CARE-TEAM-PRIVATE (sealed to a per-recipient care-team
key). Each care-recipient with ≥1 enrolled caregiver gets an X25519 care-team
keypair `(CT_pub, CT_priv)`; `CT_priv` is sealed to each enrolled caregiver's
member public key — structurally the household key tree of the prior design
(§2.2 there), scoped to the recipient's enumerated care team, never inferred
from household membership. Additive schema:

```
care_team_keys(
  recipient_ref   TEXT,     -- the care-recipient (subject string / member_id)
  household_id    TEXT,
  ct_pubkey       BLOB,     -- CT_pub for the CURRENT epoch
  epoch           INT,      -- bumped on every membership removal
  created_at      TEXT,
  PRIMARY KEY (recipient_ref, epoch)
)
care_team_key_wraps(
  recipient_ref   TEXT,
  epoch           INT,
  holder_ref      TEXT,     -- member_id of an enrolled caregiver
  wrapped_ctpriv  BLOB,     -- CT_priv sealed to holder's member public key
  grant_kind      TEXT,     -- 'current' | 'backfill' (see epochs below)
  PRIMARY KEY (recipient_ref, epoch, holder_ref)
)
```

A member's keyring (§5.1) gains a third entry kind: wrapped `CT_priv` per
care team they are enrolled in, alongside member key and dyad wraps.

**2. Care-team key epochs (mid-history membership).** A newly added
caregiver receives the CURRENT epoch by default — future care-team facts
plus current active facts (medications, allergies, care plans). Historical
events require an explicit backfill grant (`grant_kind='backfill'` rows for
prior epochs); historical access is NEVER inferred from current membership.
On removal: mint a new epoch (`CT_pub'`/`CT_priv'`), re-wrap forward-going
DEKs to it, seal `CT_priv'` to remaining caregivers only, revoke the removed
caregiver's sessions and cache. Same honest limit as §4.2: rotation blocks
future reads; it cannot un-download plaintext already read.

**3. §5.2's default is FLIPPED.** The paragraph below ("Dyad-scoped
(tightest, default)") predates the ratification and is retained for history:
under the ratified model the default for care/health/safety/coordination
facts about a recipient is CARE-TEAM-PRIVATE, with pair-private by explicit
author directive or mandatorily when the fact's subject is another enrolled
caregiver. The full four-level precedence order (recipient standing policy >
author directive > attribute+subject classification > sensitivity affects
handling never audience), compound-statement splitting, and the accepted
stated cost live in `REQ_PARTITION_CUSTODY`; this spec defers to it.

---

## 0. Why the reframe, and what in the code already fits it

The prior design hit one wall it stated honestly (prior §7 limit 2):
cryptographic isolation was **author-keyed**, so the aging parent — a keyless
*subject*, not a keyholder — got policy protection, not cryptographic. For
eldercare that is the wrong unit.

The right unit is the **dyad**: the caregiver/care-recipient pair. And the
code already stores facts in exactly that shape — this is not a retrofit onto
a hostile schema:

- `scripts/demo_seed.py:3` (verbatim): *"Household: Maya, Sam. Care
  recipients: Dad (subject only), Ray (Maya's care recipient)."*
- `demo_seed.py:126` seeds `D9` as `owner=MAYA_ID, subject="ray"`;
  `:352` states *"Dad's facts are accessible to Sam (owner=sam, subject=dad)."*
- The write path already separates the two: `_write_one` sets
  `subject = fact.get("subject") or owner` (`harness/extraction_queue.py:487`)
  and stores `owner` (the authenticated speaker) and `subject` (the resolved
  entity) as distinct fields.
- The registry (`harness/member_registry.py`) enrolls **custodians** as
  members (`add_member(..., role="adult")`, `demo_seed.py:192`) and already
  ships a `caregiver` role (`member_registry.py:40, 64`). Care-recipients
  (Ray, Dad) are **never** `add_member`'d — they exist only as `subject`
  strings on facts.

So **a dyad-private fact is, today, already the row `owner=<custodian member>,
subject=<care-recipient>`**. The dyad reframe does not invent a new data
shape; it gives that existing edge a key. The custodian holds the dyad key
**on the recipient's behalf** — the parent needs no device and no password,
and their facts become *cryptographically* sealed to the pair, not merely
policy-filtered.

What the code does **not** have: any `dyads` relation, any custodial-key
concept, and (per prior §0) any real private/shared partition beyond
`attribute == "household"` (`harness/fact_change.py:630`). Those are what this
spec defines.

**Design principle (from the ask, kept literally):** the system enforces the
**boundary** and clean **entry/exit**; the humans manage the relationship.
This spec models the cryptographic edge and its lifecycle only. It does not
model the relationship's content, care plans, or day-to-day — out of scope.

---

## 1. The dyad as the crypto unit

### 1.1 Schema (net-new; additive to `member_registry`)

A `dyads` relation binding a custodian member to a care-recipient:

```
dyads(
  dyad_id            TEXT PRIMARY KEY,
  custodian_member_id TEXT,     -- FK members.member_id (the keyholder)
  recipient_ref       TEXT,     -- the care-recipient: a subject string
                                --   (e.g. "ray","dad"); may later be a
                                --   member_id if the recipient ever enrolls
  household_id        TEXT,     -- FK households.household_id
  dyad_pubkey         BLOB,     -- D_pub (X25519); public, server-stored
  status              TEXT,     -- active | dissolved
  consent_ref         TEXT,     -- pointer to the entry-consent record
  created_by          TEXT,     -- who authorized entry
  created_at          TEXT
)
```

Plus a wrap-storage table (the server holds only *sealed* private keys, never
cleartext):

```
dyad_key_wraps(
  dyad_id       TEXT,   -- FK dyads.dyad_id
  holder_ref    TEXT,   -- member_id of a custodian, OR a recovery-share id
  wrapped_dpriv BLOB,   -- D_priv sealed to holder's member public key
  key_version   INT,    -- bumped on every re-key (exit/rotation)
  PRIMARY KEY (dyad_id, holder_ref, key_version)
)
```

`recipient_ref` is a **subject string** because that is what the data uses
today (Ray/Dad are subjects, not members). If a recipient ever enrolls a
device, `recipient_ref` can point to a `member_id` and the recipient becomes
a co-holder of their own dyad key — a strict upgrade, not a required one.

### 1.2 The dyad keypair and custodial holding

Each dyad has an X25519 keypair `(D_pub, D_priv)`:

- `D_pub` is public, stored on the `dyads` row; the write path seals fact DEKs
  to it.
- `D_priv` is **never stored server-side in cleartext.** It is sealed to each
  custodian's *member* public key (prior §2.1) and stored in
  `dyad_key_wraps.wrapped_dpriv`. The custodian's device fetches its wrap,
  unseals it with the member private key it already holds, and can then unwrap
  dyad-fact DEKs.

This is the whole point in one sentence: **the caregiver's own key unwraps the
dyad key, which unwraps the parent's facts.** The parent holds nothing. The
operator holds `D_pub` and a sealed `D_priv` it cannot open. The keyless
subject is now cryptographically protected *through the custodian*, which is
exactly the gap the prior design could not close.

### 1.3 Sealing a recipient's private fact (two-hop unwrap)

A dyad-private fact keeps the envelope (fresh per-fact DEK sealing the value,
prior §2). What changes is the DEK's wrap: the DEK is sealed to the dyad's
`D_pub` (or to several — §5, overlapping). Read is a **two-hop unwrap**, all
device-side:

```
member_privkey  --unseal-->  D_priv  --unseal-->  DEK  --decrypt-->  value
```

The server can do the first hop's *inverse* (seal to D_pub) to **write**, but
cannot do the unwrap direction at all — it has no member private key and no
D_priv. This preserves the prior design's core property (server writes,
cannot read) one level deeper.

---

## 2. The write-time partition rule (dyad terms)

> SUPERSEDED 2026-07-20: the class list below predates the ratified access
> model. "DYAD-PRIVATE" is split into CARE-TEAM-PRIVATE / PAIR-PRIVATE, and
> sensitivity no longer determines audience (handling only) — the governing
> rule is now the four-level precedence order in `REQ_PARTITION_CUSTODY`.
> Retained for history; the seal-target mechanics (§1, §3-§5) still apply.

Three classes, assigned at write time, first match wins. Grounded in the
existing `owner`/`subject`/`sensitivity` fields and the registry, not an LLM
guess:

1. **HOUSEHOLD-SHARED** — `attribute == "household"` (unchanged,
   `fact_change.py:630`) or a directive marking it shared. Sealed to the
   household key tree (prior §2.2). Readable by all adults. (Schedule,
   address, trash day.)
2. **DYAD-PRIVATE** — `owner != subject` **AND** a dyad exists binding
   `custodian_member_id == owner` and `recipient_ref == subject` **AND**
   (`sensitivity in {high, critical}` **OR** an explicit "keep this to the
   care pair" directive). Sealed to the dyad key(s) in scope (§5). This is the
   parent's medical/sensitive fact, sealed to the pair.
3. **MEMBER-PRIVATE** — `owner == subject` (a self-fact) with
   `sensitivity in {high, critical}` or directive; **or** `owner != subject`
   where the subject is **not** a care-recipient in any dyad (e.g. one adult's
   note about another). Sealed to the author's member key only (prior §1.2).

**Default when nothing matches** → member-shareable (prior §1.2): the author's
fact, additionally readable by household adults. This preserves today's
de-facto behavior for ordinary facts.

**Who assigns:** the write pipeline, deterministically:
- Does `(owner, subject)` match an active `dyads` row? → registry lookup,
  yes/no, no model involved.
- Private vs shareable within a class → the existing `sensitivity` field
  (`extraction_queue.py:230-235`) or an explicit member directive, exactly as
  prior §1.3.

**Honest note (unchanged from prior):** promoting `sensitivity` from a policy
signal to a *cryptographic* trigger raises the stakes on a 7B model's
classification. A fact mis-marked `low` seals shareable, not private. The
directive overrides it, and the failure mode is "shared within the
household," never "leaked to operator/internet" (the operator-blind wall holds
regardless of class). Say this to a technologist.

---

## 3. Entry — the key-grant flow

Entry is clean; spec it so nothing is implicit.

1. **Precondition.** The custodian is an enrolled member with a device
   keypair (prior §2.1). The care-recipient need not be enrolled and need not
   hold anything.
2. **Consent / authorization.** An authorized principal approves the dyad:
   the household admin (`households.admin_member_id`,
   `member_registry.py:64`), or the recipient themselves if capable, or a
   legal PoA credential (§6). A `consent_ref` records who authorized it and
   under what basis. *This is a governance record, not relationship content —
   in scope.*
3. **Key generation.** The dyad keypair `(D_pub, D_priv)` is generated **on
   the custodian's device** (so `D_priv` is never server-side cleartext).
   `D_pub` is registered on the `dyads` row.
4. **Custodial wrap.** `D_priv` is sealed to the custodian's member public key
   and stored in `dyad_key_wraps`. The dyad is now live: the custodian can
   read dyad-private facts for the pair.
5. **Recovery escrow (ties to §4/exit).** `D_priv` is *also* placed under the
   2-of-3 threshold split from prior §4 — one share to the operator, one to a
   second household/family principal, one to a member backup. This is what
   makes non-cooperative exit possible (§4); entry sets it up so exit never
   needs the departing custodian.
6. **Backfill.** Existing facts already shaped `owner=custodian,
   subject=recipient` that qualify dyad-private (per §2) are re-sealed from
   their current wrap to `D_pub` — a bounded per-dyad job on the custodian's
   device, reusing the prior §6 re-wrap machinery (DEK re-seal, value
   untouched).

Entry adds one dyad row, one `D_pub`, one custodial wrap, and one recovery
split. Reversible until step 4 commits.

---

## 4. Exit — atomic revocation, re-encryption, and non-cooperative removal

Exit is the load-bearing part. It is specified as one primitive with two
triggers (cooperative and quorum), because they are the same mechanism.

### 4.1 The revocation operation (atomic re-key)

To remove a custodian `X` from a dyad, or to rotate a compromised dyad key:

1. **Mint** a new dyad keypair `(D_pub', D_priv')`.
2. **Re-wrap every in-scope dyad-private fact's DEK** from `D_pub` to
   `D_pub'`. The DEK unwrap (needed before re-seal) is done by a *remaining*
   custodian's device, or by the recovery quorum (§4.3) — never by `X`. Value
   ciphertext is untouched; only the DEK wrap changes. Cost is bounded by the
   dyad's fact count.
3. **Seal** `D_priv'` to the **remaining** custodians' member public keys
   (new `dyad_key_wraps` rows at `key_version+1`); re-run the recovery split
   for `D_priv'`.
4. **Delete** `X`'s wrap of `D_priv` and all old-`key_version` wraps; bump the
   `dyads` row to the new key.

**Atomicity.** Steps 1–4 commit as one transaction. The invariant that must
never be observable mid-flight: *both* the old and new key valid for `X`
simultaneously. Either the re-key is complete (facts under `D_pub'`, `X`'s
wrap gone) or nothing changed. A crash mid-re-wrap resumes or rolls back; it
does not leave `X` with live access to a "partially rotated" dyad. This is the
"atomic revocation + re-encrypt under a new key so the old key is dead going
forward" the ask requires.

### 4.2 The honest limit: "no new access," not "unremembers"

Revocation kills **future** unwrap. It **cannot retract what `X` already
decrypted.** Every dyad-private value `X` read during their tenure may persist
in `X`'s notes, screenshots, memory, or a copy they made. Re-keying makes
`X`'s key unwrap *nothing new*; it does not reach into `X`'s head or `X`'s
external copies. State this plainly to the family and the buyer's legal team:
**exit is a forward boundary, not an eraser.** Any claim otherwise is false
and this spec will not make it.

### 4.3 Non-custodian-triggered exit = the recovery quorum

The family must be able to remove a custodian **without that custodian's
cooperation** — dispute, estrangement, suspected elder abuse, death, contested
PoA. This is **the same primitive as the 2-of-3 threshold recovery** (prior
§4), and that identity is the point:

- The dyad's `D_priv` is escrowed under the 2-of-3 split at entry (§3 step 5).
- A **quorum** (any two shares — e.g. household admin's share + operator's
  facilitation share, or two family principals) reconstructs the recovery
  key, unwraps the *current* `D_priv`, performs the §4.1 re-key to `D_priv'`,
  and **omits** `X` from the new wraps — all **without `X` participating.**
- Because reconstruction needs **two** shares, **the operator alone cannot do
  it** (one share). An operator cannot unilaterally evict a family caregiver,
  and a rogue caregiver cannot block their own removal by refusing to
  cooperate — the quorum routes around them.

So entry, key-recovery, and custodian-eviction are **one mechanism**: the
quorum that recovers a lost key is the quorum that evicts a custodian. There
is no separate "admin override," which is exactly what keeps the operator from
being a unilateral back door.

---

## 5. Overlapping dyads — multi-membership and cross-dyad facts

Real families are graphs of overlapping dyads (Maya-Ray, Sam-Ray, and Sam-Dad
already coexist in the seed). The key structure handles this without
special-casing:

### 5.1 A person in multiple dyads → a keyring, not a key

A member's device holds a **keyring**, not a single key:
`{ own member privkey, [ wrapped D_priv for each dyad I am custodian of ],
wrapped HH_priv (household) }`. Maya, custodian of Maya-Ray, holds a wrap of
that dyad's `D_priv`; if Maya later also becomes custodian of Maya-Sam-care,
she holds a second dyad wrap. No collision — each dyad key is independent, and
membership *is* "holding a wrap of that dyad's `D_priv`."

### 5.2 A fact scoped to one dyad vs several (the care circle)

A recipient-private fact is sealed to a **scope set** of dyad public keys:

- **Pair-scoped (PAIR-PRIVATE):** sealed to **one** dyad key. Ray's fact
  that Maya recorded privately is sealed to Maya-Ray only — Sam, even though
  Sam is also Ray's caregiver, cannot read it.
- **Care-team-scoped (CARE-TEAM-PRIVATE):** sealed to the recipient's
  care-team key (`CT_pub`, current epoch — see UPDATE 2026-07-20 above),
  whose `CT_priv` is wrapped to every enrolled caregiver. This is the
  coordination case — Ray's current medication, which every caregiver must
  see.

The **care team** of a recipient = the enumerated set of enrolled caregivers
sharing that `recipient_ref` (never inferred from household membership).
DEFAULT FLIPPED BY THE 2026-07-20 RATIFICATION: care/health/safety/
coordination facts about the recipient default to CARE-TEAM-PRIVATE;
pair-private requires an explicit author directive ("keep this between us")
or applies mandatorily when the fact's subject is another enrolled
caregiver. (The pre-ratification text here had pair-scoped as the default
with care-circle widening by directive — superseded.)

### 5.3 Revocation with overlap stays local

Removing Maya from Maya-Ray re-keys the Maya-Ray dyad (§4.1) AND — under the
ratified care-team model — rotates Ray's care-team key to a new epoch
(UPDATE 2026-07-20 above): `CT_priv'` is sealed to the remaining enrolled
caregivers only, so Maya loses forward access to care-team facts while Sam
is unaffected (his wrap of `CT_priv'` is simply minted alongside). Pair-
private facts sealed to Sam-Ray are untouched. Re-key blast radius is one
dyad plus one care-team epoch, never the household tree.

### 5.4 Peer relationships are not dyads

Two adults with no care relationship (the ask's "Maya-Sam") are **not** a
dyad — dyads are specifically caregiver↔care-recipient. Peer facts use
member-private or household-shared. Keeping dyads scoped to care (not "any
pair") is what keeps the design principle honest: model the care boundary,
not every human relationship.

---

## 6. Custody transfer and dissolution (where the buyer's legal team pushes)

All of these compose the §3 (add) and §4 (remove) primitives; none needs new
crypto.

- **Custody transfer (Maya → Sam, or a rotating professional caregiver):**
  ADD the incoming custodian (§3: seal `D_priv` to their pubkey), then —
  only if the outgoing custodian is being cut off — REMOVE the outgoing one
  (§4 re-key). A hand-off that keeps both is just an add. Transfer ≠ re-key
  unless someone is being denied forward access.
- **Death of a custodian:** non-cooperative exit (§4.3). The custodian cannot
  participate; the quorum re-keys and omits them. Their device key, now
  inaccessible, unwraps nothing new even if the device is later recovered.
- **Death of the care-recipient:** the dyad dissolves. Two lawful
  dispositions, mechanism-identical, choice is legal/policy: **(a) succession**
  — seal the final `D_priv` to an estate/PoA principal so records survive;
  **(b) crypto-shred** — destroy every wrap of `D_priv` and the recovery
  shares, rendering the recipient's private facts permanently unrecoverable
  (the value ciphertext remains but no key can ever unwrap it). Crypto-shred
  is the same mechanism the prior design's ledger backup spec uses for member
  deletion — "rm the key = every copy is dead."
- **Contested PoA / dispute:** the **quorum composition is the governance.**
  Define it so no single party decides — e.g. quorum = { household admin,
  operator-facilitator, one of [ second family principal | verified legal-PoA
  credential ] }. The operator holds one share and runs the ceremony but
  **cannot complete a custody change alone.** That is simultaneously the
  legal-safety property (the operator is not the decider, so not the liable
  seizer) and the go-to-market tension (§8): an operator that wants unilateral
  "just fix grandma's account" control does not get it by construction.
- **Suspected elder abuse:** the family removes a suspected-abuser custodian
  via §4.3 without their cooperation. The **mechanism** supports it; the
  **judgment** (is this abuse?) is human and legal, never the system's. The
  spec provides the lever, not the verdict.

The legal team's sharpest question will be *"who is in the quorum, and does the
operator's facilitation create custody-decision liability?"* The answer this
design is built to give: the operator facilitates (one share, runs the flow)
but cannot decide or complete alone — so the operator is a **notary, not a
guardian.** That distinction is the whole legal posture, and it falls out of
the threshold, not out of a policy promise.

---

## 7. How this maps onto the prior design's 11 sites

The dyad reframe does not undo prior §5; it changes **what the reader set is**
and adds one schema site. The retire-the-master, go-asymmetric,
device-side-decrypt spine is unchanged.

| Prior site | What the dyad reframe changes |
|---|---|
| 4 `encryption.py:105-114` `encrypt_fact_value(plaintext, owner)` | the second arg stops being "owner" and becomes a **reader-set resolver**: `visibility_class × (owner, subject)` → `{ member pubkey | household key tree | one-or-more dyad D_pub }`. Dyad-private → seal DEK to the dyad key(s) in scope (§5). |
| 5 `encryption.py:117-123` `decrypt_fact_value(ct, dek, owner)` **(chief)** | still must not exist server-side. Device-side unwrap becomes **two-hop** for dyad facts: `member_privkey → D_priv → DEK` (§1.3). The single-hop symmetric-from-master path this function embodies is the exact thing being deleted. |
| 6 `extraction_queue.py:491` `_write_one` → encrypt | stamps the **visibility class** and, for dyad-private, looks up the `dyads` row for `(owner, subject)` to pick the seal targets. The `(owner, subject)` fields it already writes are the dyad key. |
| 7 `extraction_queue.py:723-724` / 8 `:806-808` read/search decrypt | server returns wrapped DEK **plus which key it is under** (member / household / dyad_id); the device resolves via its keyring (§5.1). |
| 9 `demo_dashboard.py:391-392` `/api/decrypt` / 10 `:746` fact_history | cannot decrypt v2 dyad facts at all; hands wrapped material to an authenticated custodian device. The current `_vault_selected_member` policy gate (`:388-390`) is *replaced* by "can your keyring unwrap it," which is cryptographic, not a server-side string check. |
| 11 `extraction_queue.py:704-705` owner `WHERE` filter | unchanged in role: a UX/perf pre-filter, no longer the boundary. Note it now under-selects for care-circle facts (a fact sealed to Sam-Ray but `owner=maya` won't match Sam's `owner` filter) — the filter must widen to "facts my keyring can open," or simply over-return ciphertext and let the device decide. |
| **NEW site 12** `harness/member_registry.py` | add the `dyads` and `dyad_key_wraps` tables (§1.1). Not a key-derivation site — additive schema and sealed-wrap storage. The registry becomes the source of truth for *who is in which dyad*, which is what the write path consults to pick seal targets. |

`encryption.py:117-123` remains the linchpin: as long as a server-side
`decrypt_fact_value(ct, dek, owner)` works for any owner, the dyad wraps are
theatre. The dyad model is only real once that function is gone server-side
and the two-hop unwrap lives on custodian devices.

---

## 8. Honest limits that survive the dyad reframe

Lead with these.

1. **Still not operator-blind at inference.** Plaintext lives in edge-host RAM
   during every turn (prior §7.1). The dyad reframe protects data at rest and
   in the DB; it protects nothing during a query. Out of scope; enclaves are
   the roadmap tier. Say it first.
2. **The reframe relocates trust to the custodian — it does not remove it.**
   The keyless parent is now cryptographically protected from the operator and
   from non-custodian family — but **not from their own custodian.** Someone
   must hold the key for a keyholder-less subject, and that someone can read
   everything in the pair. "Cryptographically protected" for the recipient
   means "protected from everyone *except* the caregiver(s) you are in a dyad
   with." That is inherent to keyless-subject custody, not a bug — and it is
   the honest answer to "so who can read Dad's medical facts?": his
   caregivers, by design, and no one else.
3. **The dyad graph itself is new cleartext metadata.** Values are sealed, but
   `dyads` rows, `subject`, `attribute`, `sensitivity`, and timestamps stay
   queryable plaintext (prior §7.5). The operator now additionally learns the
   **care-relationship graph** — who cares for whom — in the clear. For
   eldercare that graph *is* the prime analytics/upsell signal, so the
   metadata leak is not incidental; it is the most commercially valuable thing
   the operator can still see. Name it.
4. **Embeddings still leak** (prior §7.6): per-fact embeddings computed from
   plaintext, server-side for search, partially undo value encryption via
   inversion. Unchanged.
5. **Recovery/eviction stops *unilateral*, not *collusive*, action.** The
   quorum can be gamed if enough shareholders collude (operator + one family
   member evict another; or two family members seize a contested custody). The
   threshold guarantees "no single party alone," not "no coalition." With
   custody at stake the consequences are higher than with mere key recovery —
   state the raised stakes.
6. **Exit is a forward boundary, not an eraser** (§4.2) — re-stated here
   because it is the limit families will most want to not be true.
7. **Go-to-market tension, now doubled.** Operator-blind-at-rest already
   removes the operator's read access the operator may want (support,
   analytics, upsell). The dyad model adds a second: the operator **facilitates
   but cannot decide** custody changes (§6) — an operator wanting unilateral
   "fix grandma's account" control does not get it. And the one thing operator-
   blind leaves the operator (the cleartext dyad graph, limit 3) is exactly
   the eldercare upsell signal — so the commercial pull is toward exposing
   more metadata, against the subscriber-trust posture. The place the design
   fights the buyer's own wishes is the place its trust claim lives; that
   tension is the moat, and it is a sales conversation, not an engineering
   one.

Nothing here is built. This is the spec a real build implements by adding the
`dyads`/`dyad_key_wraps` schema, changing the reader-set resolver at prior
sites 4/6, making the unwrap two-hop and device-side at sites 5/7/8/9/10,
migrating per prior §6, and keeping §8 in front of the buyer, not behind it.
