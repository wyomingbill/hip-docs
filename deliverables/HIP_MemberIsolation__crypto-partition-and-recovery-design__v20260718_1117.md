# HIP Member Isolation — Cryptographic Partition, Operator-Blind-at-Rest, and Recovery Design
Status: PLAN
Reconciled-Against: main 5d6bde3 (code read 2026-07-18); prior trace DISPATCH_ISOLATION_TRACE__per-member-enforcement-mechanism__v20260718_1002.md

**Type:** Architecture design. No production code. This document specifies a
target; it builds nothing. Every current-state claim carries a `file:line`
you can open; every forward claim that cannot hold cryptographically is
marked as such rather than designed around.

> UPDATE 2026-07-20: Bill ratified the dyad access model (two-review
> reconciled; decision in `REQ_PARTITION_CUSTODY`). The visibility classes
> in §1.2 are extended by the dyad spec's ratified scopes: the dyad layer's
> "dyad-private" is split into CARE-TEAM-PRIVATE (a per-recipient care-team
> key class with epochs, wrapped to each enrolled caregiver — structurally
> this doc's §2.2 household key tree, scoped to the recipient's enumerated
> care team) and PAIR-PRIVATE (one dyad key, unchanged). Sensitivity no
> longer determines audience (handling only), superseding §1.3 rule 3's
> audience role. Schema and epoch mechanics:
> `HIP_MemberIsolation_Dyads__custodial-crypto-entry-exit-overlapping__v20260718_1207.md`
> (UPDATE 2026-07-20 section). Build extension to Phase 1's dyad-keys model;
> nothing built.

---

## 0. Why this document exists, and what changed since the ask was written

A prior session repeatedly asserted this design from memory and was wrong.
This one is grounded in a re-read of the live files at `5d6bde3`. Two facts
in the framing I was handed are now stale against the code, and the design
is honest about both:

1. **D-10 is no longer a fully unauthenticated bypass.** `/api/facts` and
   `/api/decrypt` now require a dashboard session token
   (`server/demo_dashboard.py:150-152, 323, 370`) and `/api/decrypt` is
   fact_id-keyed with a server-tracked selected-member gate
   (`:374`, `:388-390`). **But this changes nothing about the crux:** the
   gate is `owner in (_vault_selected_member, "household")` — a policy check
   — layered over a server that still calls
   `decrypt_fact_value(...)` (`:391-392`) and can therefore derive *every*
   member's key. `_vault_selected_member` is set by
   `/api/session/select-member` (`:179-192`) to any member_id that exists in
   the registry, with **no proof the caller is that member**. So any holder
   of the single shared operator token can select `elena` and read Elena's
   plaintext. D-10 got a fence; the vault it fences is still openable by the
   operator. The root cause the prior trace named — one master key derives
   all — is untouched.

2. **There is effectively no sensitivity-based "private vs shared" partition
   at write time today.** The only runtime rule that assigns the shared
   namespace is `effective_owner = "household" if attribute == "household"
   else owner` (`harness/fact_change.py:630`). Everything else is owned by
   the **speaker** (`server/voice_orch.py` writes `owner=self._member_id`;
   `harness/extraction_queue.py:491` encrypts under that `owner`). The
   household-sharing the constraints assume ("adult members must reach Ray's
   meds, the schedule, the address") is **not produced by the write rule** —
   a fact Maya utters about Ray is `owner=maya, subject=ray`, retrieved only
   by *Maya's* own queries (`extraction_queue.py:704-705`). It appears shared
   in the demo only because `demo_seed` seeds those specific facts with
   `owner='household'`. **The partition this design must build does not exist
   yet; it has to be defined, not merely re-keyed.**

Both facts make the design *more* necessary, not less.

---

## 1. The fact partition: private vs shared, and the write-time rule

### 1.1 How `owner` is set today (the ground truth)

- `owner` is the **authenticated speaker's `member_id`** — the *author/
  custodian*, not necessarily the data subject. `server/voice_orch.py`
  attributes every extracted write to `self._member_id`; the write path
  (`extraction_queue.py:_write_one`, `:476-558`) stores `owner` and a
  separate `subject` (which defaults to `owner` for self-facts, `:487`, and
  can differ for third-party facts: `owner=maya, subject=ray`).
- The value is envelope-encrypted **under `owner`**
  (`extraction_queue.py:491` → `encryption.encrypt_fact_value(value, owner)`).
- The shared namespace is a single literal string `"household"`, assigned
  only when `attribute == "household"` (`fact_change.py:630`) or by seeding.
- Retrieval merges "mine + household": `WHERE f.owner = $owner OR f.owner =
  'household'` (`extraction_queue.py:704-705`, `:727`, `:802`).

**Consequence for the design: the cryptographic boundary is `owner`, and
`owner` is the author.** A fact *about* Elena written by Maya is, and will
remain, keyed to *Maya*. This is the single most important honest limit in
the whole design and it recurs in §7. "Member-private" can only mean
"private to the authoring member" unless the subject is themselves a
keyholder.

### 1.2 The three visibility classes (target)

Define an explicit, write-time **visibility class** per fact — a first-class
field, not an inference. Three classes, chosen to match the constraints
minimally:

| Class | `owner` today | Who may decrypt (target) | Wrapped to |
|---|---|---|---|
| `household-shared` | `"household"` | every **adult** member | household key (see §2) |
| `member-shareable` | `<member>` | the author, **and** household adults | household key + author key |
| `member-private` | `<member>` | the author **only** | author key only |

`member-shareable` is the default (it reproduces today's de-facto behavior —
a member's fact reachable by the household — but makes it cryptographic
rather than filter-only). `member-private` is the wall the whole exercise
exists to build.

### 1.3 The write-time rule that assigns the class

The rule must be deterministic, auditable, and grounded in a signal that
already exists. Assign at write time, in this order (first match wins):

1. **Explicit member directive** → `member-private`. A member who says "keep
   this private / don't share this with the family" sets the class directly.
   (Surfaced as a consent affordance, not an LLM guess.)
2. **`attribute == "household"`** → `household-shared`. Unchanged from
   `fact_change.py:630`; the existing rule is correct for this class.
3. **`sensitivity in {high, critical}`** → `member-private` **by default**.
   Grounded in the existing `sensitivity` field, which the extraction LLM
   already emits (`extraction_queue.py:230-235`) and which `permissions.py`
   already treats as a hard cross-member wall (Rule 5: another member's
   high/critical fact is *always* blocked, `permissions.py:127-128`). We are
   promoting an existing **policy** wall into a **cryptographic** one. A
   member may downgrade a specific high-sensitivity fact to `member-shareable`
   via directive (1), but the safe default is private.
4. **Otherwise** → `member-shareable`.

**Who decides:** the write-time pipeline, from (a) an explicit member
directive when present, else (b) the `sensitivity` classification that is
already computed. Not the operator, and not a post-hoc filter. The class is
stamped on the node next to `owner`/`sensitivity` and is immutable for that
fact version (a re-classification is a new version, consistent with the
existing supersession model).

**Honest gap this exposes:** `sensitivity` is today produced by a 7B
extraction model. Making it the trigger for a *cryptographic* wall raises the
stakes on its reliability. A misclassification that marks a truly private
fact `low` wraps it shareable. This is acceptable only because (a) the member
directive overrides it, and (b) the failure is "shared within the household,"
not "leaked to the operator or the internet" — the operator-blind wall (§3)
holds regardless of class. State this to a technologist; do not hide it.

---

## 2. Key structure for member isolation

### 2.1 The core move: symmetric-derived-from-master → asymmetric per-member

Today (`encryption.py`):

- One master key on disk (`_load_or_create_master_key`, `:58-76`).
- `_derive_key(owner)` (`:79-92`) HKDF-derives **any** owner's Fernet key
  from the master, deterministically, on demand.
- `encrypt_fact_value` wraps the per-fact DEK with `_derive_key(owner)`
  (`:113`); `decrypt_fact_value` unwraps with the same (`:121`). **The server
  can produce every key.** That is the whole problem.

Target: **each member holds an asymmetric keypair whose private half never
leaves their device.** The envelope (fresh per-fact DEK sealing the value) is
kept — it is a good design; only the *DEK-wrapping* layer changes.

- **Member keypair** (e.g. X25519 for sealed-box wrapping; Ed25519 alongside
  for signing/enrollment). Generated **on the member's device**. The device
  keeps the private key; the **public key** is registered server-side
  (extend `member_registry` — it already stores per-member rows,
  `member_registry.py`).
- **Per-fact DEK** (unchanged: a fresh symmetric key per fact, sealing the
  value).
- **Wrapping** (this is what changes): the DEK is wrapped to a **reader set**
  by encrypting it *to public keys* (sealed box):
  - `member-private`: DEK sealed to the **author's public key** only.
  - `member-shareable`: DEK sealed to the author's public key **and** to the
    household key (below).
  - `household-shared`: DEK sealed to the **household key** only.

The asymmetry is the point: **the server can *write* a fact a member can
read, without being able to read it itself** — it seals to the member's
public key at write time; only the device's private key unseals. That single
property is what makes operator-blind-at-rest possible without giving up
server-side writes (which the extraction pipeline requires).

### 2.2 Keeping shared facts shared: the household key tree

A household key must be readable by every adult *and* by the server-at-write-
time-only-as-a-writer, and must survive membership churn without re-
encrypting facts.

- The **household keypair** (`HH_pub`, `HH_priv`) is generated once at
  household creation (`member_registry.create_household`,
  `member_registry.py:324`).
- `HH_priv` is **wrapped once per adult**: sealed to each adult member's
  public key, stored server-side as a small set of blobs (a one-level key-
  wrapping tree). The server holds only these sealed blobs; it cannot open
  them.
- A member's device, on session start, fetches its sealed `HH_priv` blob,
  unseals it with its own private key (in device memory), and can then unseal
  household-shared and member-shareable DEKs.
- **Adding an adult** = seal `HH_priv` to the new member's public key (one
  small write). **Removing an adult** = delete their sealed `HH_priv` blob
  **and rotate** the household keypair (generate `HH_pub'`, re-seal to
  remaining adults, re-wrap the DEKs of household facts to `HH_pub'` — a
  bounded background job, not a re-encrypt of values; the value ciphertext
  and its DEK are untouched, only the DEK's *wrapping* changes). Rotation-on-
  removal is required for real revocation; note it explicitly, it is a real
  cost.
- **`can_see_household`** in `permissions.py` (`:61-65`) becomes the rule for
  *who gets an `HH_priv` wrap*: adults and children get one per today's role
  defaults; guests/visitors do not. The role table stays the source of the
  sharing policy; the crypto enforces it instead of a post-fetch filter.

### 2.3 What each principal actually holds

| Principal | Holds | Where | Can decrypt |
|---|---|---|---|
| Member (adult) | own private key; unsealed `HH_priv` (transient) | device only | own facts + household + member-shareable shared to household |
| Member (child) | own private key; unsealed `HH_priv` | device | own facts + household (role-gated) |
| Household | `HH_priv`, wrapped per-adult | server (sealed blobs) + adult devices | shared facts |
| Server / operator | all **public** keys; all sealed blobs; all ciphertext | server | **nothing** (no private key; no master) |

The row that must be true for the whole design is the last one: **after
migration completes, the server holds no secret that unwraps any DEK.**

---

## 3. Operator-blind-at-rest, layered on without breaking isolation or sharing

Operator-blind-at-rest is not a separate mechanism — it is the **emergent
property of §2 once the master key is destroyed.** Because every DEK is
wrapped only to public keys whose private halves live on member devices:

- The operator, holding the database (ciphertext + wrapped DEKs + public keys
  + sealed `HH_priv` blobs), has no private key and no master. Every unwrap
  path requires a member device. **At rest, the operator is blind by
  construction, not by policy.**
- **Isolation is preserved:** a `member-private` DEK sealed to Maya's public
  key cannot be opened by Sam's private key. Cryptographic, not filtered.
- **Sharing is preserved:** household DEKs are openable by any adult via the
  `HH_priv` tree.
- **Server writes still work:** the extraction pipeline seals to public keys;
  it never needs a private key to *write*.

**Explicitly NOT operator-blind at inference (accepted, per scope).** At
query time a member-authenticated session must present unwrapped DEKs /
plaintext to the local edge model so it can answer. During that turn the
plaintext exists in edge-host RAM. A malicious or compromised edge host reads
everything it processes for that turn. This design does **not** close that;
enclaves are the roadmap tier that would, and are out of scope. This is the
first thing to say to a technologist, not the last (see §7).

The unwrap-at-inference happens **member-side**: the member's device (or a
session that has transiently loaded the member's private key after device
authentication) does the unsealing and streams plaintext to the edge model.
The edge/server never persists the private key. This is the boundary between
"operator-blind at rest" (held) and "operator-blind at inference" (not
attempted).

---

## 4. Recovery: both modes on one threshold floor

Recovery is the load-bearing part and it is where operator-blind most easily
dies quietly. The requirement is exact: (a) operator-facilitated convenience
recovery for the common case, **and** (b) a floor where **the operator's own
share is insufficient alone**.

### 4.1 What is being recovered

A member who loses their device loses the **private key** that unwraps their
facts (and their `HH_priv` wrap). Recovery must re-provision that private key
to a new device **without the operator being able to reconstruct it
unilaterally.**

### 4.2 The construction: threshold-split recovery key

At enrollment, generate a **recovery key** `R` for the member. `R` encrypts a
**recovery blob** = the member's private key, stored server-side (the
operator holds the blob but not `R`). Split `R` with a `2-of-3` threshold
scheme (Shamir over the key, or equivalently a 2-of-3 key-wrapping):

- **Share A — operator escrow.** Held by the operator. Enables the operator
  to *facilitate* (run the ceremony, serve the recovery blob).
- **Share B — the household second principal.** The natural eldercare
  holder: a second adult's device (the distant daughter). Sealed to that
  principal's public key.
- **Share C — the member's own backup.** A printed/exported code, a
  passphrase-derived share, or a second personal device.

**Threshold = 2.** Reconstructing `R` requires **any two** shares.

### 4.3 The two modes, on that one floor

- **Convenience recovery (95% case):** operator (A) + the household second
  principal's one-tap approval (B) → 2 shares → reconstruct `R` → decrypt the
  recovery blob → re-provision the private key to the new device. The
  operator drives it end to end; the daughter taps "yes, that's Dad getting a
  new phone." Fast, human, no printed code needed.
- **Operator-blind floor:** operator (A) **alone** = one share = **cannot
  reconstruct `R`, cannot decrypt anything.** The threshold makes unilateral
  operator recovery **cryptographically impossible**, not merely disallowed.
  If the second principal is unavailable, the member falls back to their own
  Share C (backup code) + operator = 2. Either way the operator never crosses
  the line alone.

This satisfies both halves with one construction: the operator *facilitates*
(it always holds one share and runs the flow) but *never decrypts
unilaterally* (it never holds two).

### 4.4 Honest limits of the recovery design (stated, not designed around)

- **Threshold defends against *unilateral* operator action, not against
  collusion or compulsion.** If the operator holds A and can coerce, social-
  engineer, or legally compel the holder of B (or seize the member's Share C
  backup), it reaches 2 and decrypts. The floor is "the operator alone
  cannot," which is exactly what was asked — but a technologist will push on
  "cannot alone" ≠ "cannot," and they are right. Name it.
- **Eldercare's sharp edge:** the whole recovery model assumes the member is
  a keyholder with a second principal. The aging parent (Elena) is often the
  *subject*, not a keyholder, and may have no second device and no engaged
  distant relative. For such a subject there is nothing to recover because
  there was never a member-held key — her protection was policy/author-keyed
  all along (§1.1, §7). The design serves the *caregiver's* privacy
  cryptographically and the *care-recipient's* privacy only as policy, and
  that asymmetry is inherent to who holds keys.
- **Share B liveness:** convenience recovery depends on a reachable second
  principal. If B is unreachable and the member never set up C, they are
  locked out — the price of the operator not being able to do it alone. This
  is the deliberate cost of the floor; surface it at enrollment, not at loss.

---

## 5. Every site that assumes server-side key derivation (the change list)

These are the exact points a real build must change. All are the same root:
`encryption.py` can produce any key server-side, and every caller relies on
it.

| # | Site | What it assumes | Change |
|---|---|---|---|
| 1 | `harness/encryption.py:58-76` `_load_or_create_master_key` | one on-disk master secret exists | retire; destroyed at end of migration (§6 Phase 3) |
| 2 | `harness/encryption.py:79-92` `_derive_key(owner)` | server can HKDF any owner's key from master | remove for v2; server holds only **public** keys |
| 3 | `harness/encryption.py:95-102` `derive_member_key` / `derive_household_key` | same, per member / household | replace with public-key lookup + sealed-box wrap |
| 4 | `harness/encryption.py:105-114` `encrypt_fact_value(plaintext, owner)` | wraps DEK with server-derivable symmetric key | wrap DEK to the reader set's **public** keys (§2) |
| 5 | `harness/encryption.py:117-123` `decrypt_fact_value(ct, dek, owner)` | **server can unwrap any owner's DEK** — the core violation | must not exist server-side for v2 facts; unwrap moves to the member device |
| 6 | `harness/extraction_queue.py:491` `_write_one` → `encrypt_fact_value(value, owner)` | write path seals under server-derivable owner key | seal to owner/household **public** key; stamp visibility class (§1.3) |
| 7 | `harness/extraction_queue.py:723-724` `read_user_facts` per-row `decrypt_fact_value` | server decrypts on read | server returns wrapped DEKs + ciphertext; **device** decrypts |
| 8 | `harness/extraction_queue.py:806-808` `search_facts_by_embedding` per-row decrypt | same | same; note embeddings themselves are a separate leak surface (§7) |
| 9 | `server/demo_dashboard.py:391-392` `/api/decrypt` server-side `decrypt_fact_value` | server holds keys to decrypt on request | endpoint cannot decrypt v2 facts at all; it can only hand back wrapped material to an authenticated device |
| 10 | `server/demo_dashboard.py:746` `/api/fact_history` chain decrypt | same | same |
| 11 | `harness/extraction_queue.py:704-705, 727, 802` owner `WHERE` filter | this filter **is** the isolation boundary | filter stays as a UX/perf optimization; it is **no longer the security boundary** — crypto is. A bug in the filter can no longer leak plaintext, only over-fetch ciphertext the caller can't open |

Site **5** is the one that matters most: as long as a server-side
`decrypt_fact_value(ct, dek, owner)` exists and works for arbitrary `owner`,
none of the other changes buy real isolation. The presence of that function,
callable by the server for any owner, is the single-sentence statement of why
the current system is filter-isolated and not crypto-isolated
(confirmed identical to the prior trace's finding, DISPATCH_ISOLATION_TRACE
lines 72-89).

**Adjacent, not key-derivation but load-bearing for the new root of trust:**
the identity binding that decides *which public key gets wrapped to* and
*which device authenticates to unwrap*. Today the text path takes `member` as
a client-asserted string (`/api/text-query`, no session binding — prior
trace, and `select-member` `demo_dashboard.py:179-192` inherits the same
weakness), and the voice path uses measured-weak speaker ID
(`harness/speaker_id.py`, TD-127). Crypto isolation is only as strong as
"this is really Maya's device." The design **moves the root of trust from
protecting one master key to protecting device-key custody and enrollment** —
a better place for it, but not a free one (§7).

---

## 6. Migration path, no flag day

Dual-envelope by `key_version` (the field already exists on every node —
`encryption.KEY_VERSION`, stamped at `extraction_queue.py:553`). Today all
nodes are v1 (symmetric/master). Introduce **v2** (asymmetric/sealed).

- **Phase 0 — enrollment, no fact changes.** Generate per-member and
  household keypairs on devices; register public keys; build the `HH_priv`
  wrap tree; run the recovery split (§4). Master key still present; all facts
  still v1; nothing observable changes. Reversible.
- **Phase 1 — write-forward.** New writes land v2 (sealed to public keys,
  visibility class stamped). Reads dispatch on `key_version`: v1 → existing
  server-side path (operator can still read v1), v2 → device-unwrap path.
  `read_user_facts`/`search_facts_by_embedding` return a mix transparently.
  **The system is now half-migrated and fully working.** Operator-blind is
  NOT yet true (v1 facts still server-readable) — say so plainly; do not
  claim the property until Phase 3.
- **Phase 2 — lazy re-wrap, per member, in the background.** When a member's
  device is online and authenticated, it unwraps that member's v1 facts (via
  the still-present master, server-assisted), re-seals them to the member's
  public key as v2, and the old v1 blob is deleted. Household facts re-wrapped
  to `HH_pub`. This is per-member and incremental — **no global cutover, no
  flag day.** A member who never comes online keeps working on v1.
- **Phase 3 — master retirement (the moment operator-blind becomes real).**
  When telemetry shows ~zero v1 facts for active members, **destroy the on-
  disk master key** (site #1). From this instant, site #5 (`decrypt_fact_value`
  for arbitrary owner) is dead: no secret on the server unwraps anything. Any
  residual v1 facts for dormant members become unrecoverable-by-server (a
  deliberate, announced consequence — the honest cost of actually retiring
  the master, and the difference between "operator-blind" as a claim and as a
  fact).

The ratchet is **per-member and per-fact**, keyed on `key_version`. That is
what makes it flag-day-free: v1 and v2 coexist indefinitely; the security
property strengthens monotonically as members migrate; the claim "operator-
blind at rest" is only made at Phase 3 completion and is gated on the master
key actually being gone.

---

## 7. Honest limits — what this does NOT protect, and where a technologist pushes

Lead with these; they are the credibility of the whole design.

1. **Not operator-blind at inference. This is the big one.** Plaintext lives
   in edge-host RAM during every turn (§3). A compromised or malicious edge
   host — the operator's own hardware — reads everything it processes. All of
   §2–§6 protects data *at rest and in the database*; it protects nothing
   *during a query*. A serious technologist will say "so the operator can
   just read RAM," and they are correct. The answer is: yes, and closing that
   is the enclave tier, explicitly out of scope here. Do not oversell.

2. **Cryptographic isolation is author-keyed, not subject-keyed.** A fact
   *about* Elena written by Maya is walled to Maya, not to Elena
   (§1.1). "Member-private" means "private to the authoring member." The
   care-*recipient*, who typically holds no device and no key, receives
   **policy** protection, not cryptographic protection. For the eldercare
   beachhead specifically, this means the person the product is nominally
   about is the one principal the crypto cannot directly protect. This is
   inherent to who can hold a key, not a fixable gap — state it, don't paper
   over it.

3. **Identity binding is the new soft underbelly.** Moving the root of trust
   from "protect the master key" to "protect device custody + enrollment"
   trades one hard problem for another. If an attacker enrolls a device as
   Maya, or the text path's client-asserted `member` field
   (`/api/text-query`; `select-member` `demo_dashboard.py:179-192`) lets them
   claim to be Maya, the crypto wraps to / unwraps for the attacker. Weak
   speaker ID (TD-127) and unauthenticated text identity (prior trace,
   OPEN item) become *more* load-bearing under this design, not less. The
   design is incomplete without a real device-enrollment and session-binding
   story; that is the next REQ, not this one.

4. **Recovery threshold stops unilateral operator decryption, not collusion
   or compulsion** (§4.4). "The operator cannot alone" is the delivered
   property; "the operator cannot" is not, and cannot be, given the operator
   holds a share and the infrastructure.

5. **Metadata stays cleartext by design.** `attribute`, `owner`, `subject`,
   `sensitivity`, `confidence`, timestamps, and the supersession graph remain
   queryable plaintext (the envelope encrypts only the value —
   `encryption.py:1-5` docstring; `extraction_queue.py:_write_one` stores all
   of these cleartext). The operator learns *that* Elena has a `medication`
   fact of `high` sensitivity updated last Tuesday — just not its value.
   Metadata/traffic analysis over a household's fact graph is a real residual
   and, for some threat models, most of the leak.

6. **Embeddings are a side channel.** `search_facts_by_embedding`
   (`extraction_queue.py:770+`) stores an `embedding` per fact
   (`_write_one`, `:550`) computed from the plaintext value. An embedding is
   not the plaintext but is far from opaque — nearest-neighbor and inversion
   attacks recover a lot. If embeddings stay server-side cleartext (needed for
   server-side semantic search), they partially undo value encryption. Either
   move semantic search device-side (costly) or accept the embedding leak
   (name it). This design flags it; it does not resolve it.

7. **Sharing is coarse (household-or-private).** The 2-class member partition
   (§1.2) has no per-fact ACL — "share this one fact with the caregiver but
   not the children" requires per-fact wrap sets and re-wrapping on
   membership change. Designable, but a real complexity and revocation cost;
   the current design deliberately does not include it.

8. **Go-to-market tension — operator-blind fights the operator's own
   interests.** The buyer is the operator, and some operators *want* to read
   subscriber data: support ("let me see what's wrong"), analytics, upsell.
   This design **removes** that ability at rest by construction. That is a
   feature to the subscriber and a cost to the operator. The honest resolution
   is a **member-consented, per-fact analytics channel** (the member opts to
   additionally wrap a fact's DEK to an operator analytics key) rather than a
   standing backdoor — but any operator-readable channel reintroduces exactly
   the trust the architecture removes, so it must be opt-in, per-fact, and
   revocable, never blanket. An operator that insists on blanket read access
   is asking for the master key back; this design's answer is "then you don't
   get to claim operator-blind," and that trade is a sales conversation, not
   an engineering one. The place operator-blind conflicts with the operator's
   interest is precisely the place the product's trust claim lives — the
   tension is the moat, not a bug in it.

---

## 8. Summary for a technologist (the elevator version)

- **Today:** member isolation is a Cypher `WHERE owner = $me OR 'household'`
  (`extraction_queue.py:704-705`) over values the server can always decrypt,
  because one master key derives every member's key
  (`encryption.py:79-123`). It is a filter, not a wall.
- **Target:** per-member asymmetric keys, private halves on devices; per-fact
  DEKs sealed to a reader set of public keys; a household key tree for
  sharing; the master key destroyed at end of migration. Isolation and
  operator-blind-at-rest become cryptographic facts, not policy.
- **The write-time partition** (`member-private` vs `member-shareable` vs
  `household-shared`) is decided by member directive → `attribute` →
  `sensitivity`, grounded in fields that already exist.
- **Recovery** is 2-of-3 threshold: the operator facilitates with one share
  and can never decrypt with one share.
- **The limits are load-bearing, not footnotes:** not blind at inference;
  crypto protects the author, not the care-recipient subject; identity
  binding becomes the new root of trust; metadata and embeddings still leak;
  recovery stops unilateral, not collusive, operator access.

Nothing in this document is built. It is the design a real build changes the
eleven sites in §5 to implement, migrating per §6, with the honesty of §7
kept in front of the buyer, not behind it.
