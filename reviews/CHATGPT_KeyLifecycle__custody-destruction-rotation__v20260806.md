# CHATGPT_KeyLifecycle — custody, destruction, rotation

Status: BANKED
Verification: UNVERIFIED
Source: pasted into HA-12 by Bill via advisor chat, 2026-08-06

**ONE EXTERNAL MODEL'S OPINION, NOT A RULING.** Nothing below is a HIP requirement, a
ruling, or a decision. It is a review captured verbatim so it can be argued with. Per
`CLAUDE.md`'s `docs/reviews/` entry: *"A review doc records what a reviewer CLAIMED, not
what was verified — every review lands with its findings explicitly marked unverified until
a separate dispatch confirms them, and a review never marks a REQ MET."*

**NOT ONE CLAIM BELOW HAS BEEN VERIFIED AGAINST THIS CODEBASE BY THIS DISPATCH.** Where it
describes HIP's own state (the "18 orphan keys", the file-key custody, the derived-artifact
problem), those descriptions came from the chat that produced it, not from HA-12. Two of
them happen to be independently corroborated by HA-08 and HA-10 — that corroboration is
recorded in HA-12's dispatch doc, not here, so this file stays what it is: the reviewer's
text.

**Banking provenance:** HA-10 and HA-11 both STOPPED trying to bank this from a file in
`~/Downloads` that never existed; the content lived only in a chat. HA-12 banks it from
Bill's inline paste, which is the source of record. HA-10's and HA-11's failed attempts and
the wrong `docs/research/` destination are preserved in their own dispatch docs and INDEX
rows, unedited.

**Everything below this line is the reviewer's text, byte-for-byte as pasted.**

---

## Bottom line

I would **not enable crypto-erasure against real household data in the current file-key design**.

The reason is narrower than "filesystem keys are insecure." Your product is making an **erasure claim**, and erasure-by-key-destruction is only as strong as your ability to account for **every recoverable copy of the target key**. NIST's current media-sanitization guidance says all copies of the target cryptographic key must be sanitizable and specifically warns that cryptographic erase should not be trusted where keys or data have been backed up or escrowed unless those external copies are understood and separately dealt with. ([NIST Publications][1])

With ad-hoc files, abandoned test keys and no backup/custody inventory, you currently cannot make that statement.

A useful distinction throughout:

* **[L] Literature/standards-backed**
* **[J] Engineering judgment for this system**

---

# 1. Creation and custody

## File-based custody: what actually goes wrong

**[L] Plaintext key files are below the normal security baseline.** OWASP says keys should not be stored plaintext, recommends cryptographic vaults or isolated services, and emphasizes inventorying everywhere keys exist in volatile and persistent memory. MITRE separately classifies cleartext secrets on disk as CWE-313. ([OWASP Cheat Sheet Series][2])

The relevant failure modes for HIP are:

| Failure                         | Why it matters specifically to crypto-erasure                                      |
| ------------------------------- | ---------------------------------------------------------------------------------- |
| Ordinary filesystem copying     | `cp`, backup, migration, test fixture or debugging creates another erasure target  |
| Test orphans                    | You no longer know how many target-key copies exist                                |
| Time Machine / snapshots        | A "deleted" active key may exist in earlier machine state                          |
| Cloud-sync folders              | Key custody silently becomes multi-device                                          |
| Editor/temp files               | Manual handling can create invisible secondary copies                              |
| Process memory                  | Reading the file creates a plaintext in RAM                                        |
| Swap/core dumps/crash artifacts | RAM contents can become persistent                                                 |
| Root/admin access               | File permissions do not protect against machine compromise                         |
| SSD remapping/wear leveling     | Overwriting or unlinking a specific file does not prove its old blocks disappeared |

MITRE explicitly notes that sensitive data held in memory may end up in swap, core dumps or crash artifacts; CWE-591 deals specifically with unlocked memory being swapped to disk. ([CWE][3])

And the classic FAST '11 SSD study by Wei et al. found that conventional per-file secure-deletion techniques were ineffective on SSDs because flash translation and remapping defeat the simple "overwrite these blocks" model. ([USENIX][4])

That matters enormously here:

> **Deleting `/home/bill/.hip/keys/ray.key` is not credible crypto-erasure.**

The problem isn't AES. It is key custody.

---

## Minimum credible step up on your Mac

For a single-node prototype/product, I would **not jump to an external HSM**.

### Minimum: macOS Data Protection Keychain

**[L]** Apple explicitly describes the Keychain as the appropriate place for small secrets and cryptographic keys; secret values are encrypted and access-controlled rather than sitting as ordinary filesystem files. Apple recommends opting into the Data Protection Keychain on macOS with `kSecUseDataProtectionKeychain=true`. ([Apple Developer][5])

Use:

* Data Protection Keychain, not the legacy default file-based keychain;
* `kSecAttrSynchronizable = false`;
* a `ThisDeviceOnly` accessibility class appropriate to your daemon/runtime;
* least-privilege application access;
* no human-readable/exportable key files.

Apple says `ThisDeviceOnly` items do not migrate onto another device through backup restoration. ([Apple Developer][6])

### Better: hardware-bound root

**[L]** Apple's Secure Enclave provides hardware-isolated, non-exportable private-key operations. Apple specifically contrasts it with ordinary Keychain storage: normal Keychain keys may briefly enter application memory, whereas Secure Enclave private keys remain inside the hardware boundary. ([Apple Developer][7])

Your M1-class architecture supports this.

But there is an important limitation: Apple's straightforward Secure Enclave interfaces are for supported asymmetric key operations, not simply "put this existing AES-256 owner key inside the enclave." ([Apple Developer][8])

So a production-strength architecture would likely become an **envelope scheme**:

```text
hardware/device-bound root
          |
          v
protects/wraps key-management material
          |
          v
per-subject DEK
          |
          v
subject ciphertext
```

NIST 800-88 expressly permits crypto-erasure at multiple levels: data-encryption keys, wrapping keys and key-derivation keys can all be target keys, provided the hierarchy is correctly controlled. ([NIST Publications][1])

### HSM?

**[J] Not yet.**

For a household appliance prototype operating on one Mac:

**filesystem key → Data Protection Keychain** is mandatory.

**Data Protection Keychain → hardware-backed/non-exportable root** is highly desirable before claiming strong erasure.

**Network HSM/KMS** adds operational complexity, availability dependency and potentially creates the very external-key-copy problem you are trying to eliminate.

An HSM makes more sense once HIP becomes multi-node/operator infrastructure or you need formal FIPS/enterprise custody controls.

---

## Passphrase wrapping

**[L]** Envelope encryption using a KEK is standard, and OWASP recommends wrapping DEKs where the wrapping key can actually be protected separately. But OWASP also points out that putting the KEK and wrapped DEK in effectively the same security domain provides limited additional protection. ([OWASP Cheat Sheet Series][9])

**[J]** Passphrase wrapping is a weak answer for HIP unless someone must physically enter the passphrase whenever the service starts.

If HIP stores the passphrase so it can run unattended:

```text
encrypted key file
+
passphrase sitting elsewhere on same machine
```

has mostly moved the problem.

For this device, use the OS/hardware trust boundary instead.

---

# 2. What can "the key is gone" honestly mean?

This is the most important part.

NIST defines key destruction very strongly: removal of all traces such that the key cannot be recovered electronically or physically. NIST Part 2 explicitly says destruction is not complete until **all copies, including backups**, have been destroyed. ([NIST Computer Security Resource Center][10])

Your software generally **cannot prove that historical proposition** for an exportable key.

## What you cannot prove

If a key has ever existed as an ordinary file or ordinary process-accessible byte string, after deletion you cannot prove:

> Nobody copied this key previously.

Nor can you prove:

> No recoverable copy exists anywhere on this SSD.

Nor:

> This ciphertext can never again be decrypted by any party.

That last claim is especially indefensible if:

* the key existed in backups;
* the key was copied;
* a test harness touched the same custody path;
* the process generated a core dump;
* memory was swapped;
* an administrator or malware had access before destruction.

NIST 800-88 specifically warns that previously unwrapped keys may remain in volatile memory or device registers and those versions also need elimination. ([NIST Publications][1])

### SSD problem

On flash storage, even overwriting the file is not enough. Wear leveling, spare blocks and overprovisioning mean the logical block you overwrite may not be the physical storage containing the old data. NIST itself highlights overprovisioning as a reason an apparently successful overwrite may leave data unchanged. ([NIST Publications][1])

So:

> `rm keyfile` ≠ destruction
> `shred keyfile` ≠ proven destruction on SSD

---

# What you *can* claim

For the current software architecture, a defensible statement would be:

> **HIP deleted the active managed copy of the subject's key and can no longer decrypt the subject's sealed data through the supported system path.**

If you add controlled custody, inventory and backup rules:

> **HIP sanitized all key copies known to and controlled by its key-management system; no managed recovery path remains.**

If you eventually use a hardware-backed, non-exportable target key whose lifecycle prevents export and whose deletion mechanism has trustworthy evidence, the claim can become stronger:

> **The device-bound target key was destroyed through the managed key-storage mechanism, making the protected ciphertext inaccessible through the designed key hierarchy.**

Still do **not** claim:

> "We proved that no copy was ever made."

Hardware non-exportability can make that claim much closer to a structural property **from the point at which the key is created under that architecture**. It cannot retroactively provide it for keys that existed as files yesterday.

### The epistemic distinction

**[J]**

> **Destruction evidence proves execution of a controlled destruction process. It does not prove the historical absence of unauthorized copying.**

Your UI and requirement language should preserve that distinction.

NIST's new SP 800-88 Rev. 2 is actually very aligned with this framing: it devotes a section to **traceability of cryptographic erase operations**, including key generation, wrapping, lifecycle, escrow/injection, sanitization method and whether errors can cause the operation to fail rather than falsely report success. ([NIST Publications][1])

That should sound familiar given the work you've just been doing on HIP's audit semantics.

---

# 3. Rotation

## Yes, you need a rotation mechanism. No, I would not automatically rotate every subject key every 90 days.

Those are different propositions.

**[L]** NIST key-management doctrine uses **cryptoperiods**: keys have finite operational lifetimes determined by factors such as algorithm, exposure, data sensitivity and use. OWASP similarly recommends rotation on compromise, cryptoperiod expiry, usage limits or cryptographic change. ([OWASP Cheat Sheet Series][9])

But your key has another unusual property:

> It is also the erasure handle.

Every rotation potentially turns:

```text
one subject → one key that must disappear
```

into:

```text
one subject → key_v1 + key_v2 + key_v3 + ...
```

That can make reliable deletion **worse**, unless rotation re-encrypts all surviving subject data and reliably destroys every retired generation.

### My ruling for this architecture

**[J] Build rotation before real production use, but initially make rotation event-triggered rather than aggressive calendar rotation.**

Rotate a subject key when:

| Trigger                                                  | Action                                                                                               |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Known or suspected key exposure                          | New key + re-encrypt surviving data + retire old key                                                 |
| Migration from today's file custody                      | Mandatory rotation; don't import the existing file key as the long-term production root if avoidable |
| Algorithm/library vulnerability                          | Rotate/re-encrypt as required                                                                        |
| Device or custody-domain change                          | Establish new custody and re-key                                                                     |
| Restore from backup with uncertain key state             | Treat key state as suspect                                                                           |
| Administrator/developer gained unexpected raw-key access | Treat as potential compromise                                                                        |
| Defined cryptoperiod eventually expires                  | Rotate                                                                                               |
| Usage limit appropriate to selected cipher reached       | Rotate                                                                                               |

A mere household member password change or ordinary consent change does not automatically require DEK rotation unless it alters actual key custody.

### Important rotation invariant

For an erasure system:

```text
current_subject_keys(subject)
```

must be an **enumerable finite set**.

After successful rotation:

```text
decrypt(old_ciphertext, old_key) = no longer required
```

and the old key should be destroyed.

Do not keep retired subject keys indefinitely "in case an old backup needs them." That is normal availability-oriented key-management advice, but it directly undermines an erasure architecture. NIST itself treats backup/recovery as a policy choice, and separately says all copies must ultimately be destroyed.

You are choosing **erasure over indefinite recoverability**. That needs to be an explicit custody policy.

---

# 4. Test hygiene

There isn't a canonical NIST rule saying "pytest key fixtures must use `/tmp/hip-test-keys-UUID`." This portion is mostly application of established environment-separation and key-lifecycle principles.

**[L]** NIST treats generation, storage, use and destruction as one continuous key lifecycle, and OWASP emphasizes inventory/accountability. Production and development secrets should also be segregated; OWASP explicitly recommends separate secrets-management environments when appropriate, and Google similarly recommends clean environment separation. ([NIST Computer Security Resource Center][11])

### For HIP, I would require

**[J]**

```text
test key namespace != production key namespace
```

at an architectural level, not by naming convention alone.

For example:

```text
HIP_KEY_DOMAIN=TEST
HIP_KEY_DOMAIN=PRODUCTION
```

and production code refuses to cross domains.

Test fixtures should:

1. Mint keys into a per-test or per-run temporary custody namespace.
2. Use clearly synthetic owner IDs.
3. Never access the production Keychain service/account/tag.
4. Register every generated key in a fixture-owned inventory.
5. Destroy all fixture keys in teardown/finally.
6. Run a post-suite invariant:
   `live_test_keys == 0`.
7. Fail the suite if leftovers exist.
8. Sweep stale test namespaces at test startup, but report the sweep rather than silently hiding hygiene failures.
9. Never put real household ciphertext under test keys or test ciphertext under production keys.

The fact that you found **18 orphan keys** is not a cleanup nuisance. For a crypto-erasure architecture, it is evidence that the current lifecycle abstraction is incomplete.

I would turn that into a standing invariant:

```text
keys_created
- keys_intentionally_live
- keys_destroyed
= 0 unexplained keys
```

after every battery.

---

# 5. Known-bad patterns to rule out by name

| Pattern                               | Evidence                                                                                                                                                                 | Mapping to HIP                                                        |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| **Key escrow defeats crypto-erasure** | NIST warns CE should not be trusted where keys have been backed up/escrowed unless external copies are accounted for. ([NIST Publications][1])                           | A copied owner key means deleting the active copy does not erase      |
| **Backup resurrection**               | NIST: destruction incomplete until backups are destroyed; Time Machine retains historical backups automatically. ([NIST Publications][12])                               | Restoring yesterday's key file can resurrect today's "erased" subject |
| **SSD secure-delete fallacy**         | Wei et al. showed file-level overwrite methods fail reliably on SSDs. ([USENIX][4])                                                                                      | `rm`/overwrite cannot be your erasure primitive                       |
| **Plaintext key spillage**            | CWE-316: in-memory secrets may land in swap/core dumps. ([CWE][3])                                                                                                       | Reading a seal-key file expands its custody boundary                  |
| **Unlocked-memory/swap leakage**      | CWE-591. ([CWE][13])                                                                                                                                                     | Long-lived owner keys in process memory may become persistent         |
| **Secret/key sprawl**                 | OWASP calls for key inventory, accountability and lifecycle management. ([OWASP Cheat Sheet Series][2])                                                                  | Your 18 orphan test keys are exactly this class                       |
| **KEK/DEK co-location**               | OWASP notes envelope encryption adds limited protection where attacker can acquire both layers. ([OWASP Cheat Sheet Series][9])                                          | Passphrase/KEK next to the owner key is cosmetic                      |
| **Accidental synchronization**        | macOS Data Protection Keychain can be configured to sync; `ThisDeviceOnly` and non-synchronizable settings exist specifically to constrain this. ([Apple Developer][14]) | A synced erasure key silently becomes multi-device custody            |

There is **not**, to my knowledge, one canonical published incident called "the backup-resurrected-a-crypto-erased-user incident." The standards literature treats it as a known architectural failure condition rather than relying on one famous breach. I would not manufacture an incident citation.

Likewise, "key in swap" is a well-established weakness class, but the evidence is primarily systems-security literature and vulnerability taxonomy rather than one decisive eldercare/consumer-AI case.

---

# A design issue worth making explicit

There is a trap in saying:

> "All facts are encrypted under the owner's key, therefore destroying the key erases the owner."

That is true only if **every recoverable representation requiring erasure** is actually underneath that cryptographic boundary.

You need to inventory:

```text
raw claim ciphertext
derived facts
embeddings
summaries
indexes
cached plaintext
logs
audit records
exports
test fixtures
backups
```

If an embedding or derived classification remains readable without the owner's key, owner-key destruction is not subject erasure. It is only **primary-record crypto-erasure**.

That is adjacent to the lineage problem you already identified in the structural-ceiling work.

---

# Minimum changes I would require before turning real-data erasure on

Shortest version:

1. **Kill filesystem key custody.** Move real per-subject keys into macOS Data Protection Keychain at minimum; no production raw-key files. ([Apple Developer][14])
2. **Separate test and production key domains structurally**, and make every fixture destroy its keys with a zero-orphan postcondition.
3. **Inventory every possible key copy path**: active store, Time Machine/local snapshots, iCloud/sync, exports, logs, crash dumps and recovery mechanisms.
4. **Define the exact erasure claim.** For now: "all HIP-managed key copies destroyed / HIP can no longer decrypt," not "the key cannot exist anywhere."
5. **Make erasure fail closed.** If any registered copy, backup state or destruction operation is unresolved, erasure does not report success.
6. **Build key versioning and compromise rotation**, even if you initially use event-triggered rather than frequent scheduled rotation.
7. **Prove that subject-derived data share the erasure boundary or have their own cascade**, so killing the seal key does not leave readable derived artifacts.

I would consider those seven a gate. **HSM deployment is not a gate. Hardware-backed/non-exportable custody is the next architectural step, but ordinary files should not survive into the first real-data crypto-erasure test.**

[1]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r2.pdf "Guidelines for Media Sanitization"
[2]: https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html?utm_source=chatgpt.com "Key Management - OWASP Cheat Sheet Series"
[3]: https://cwe.mitre.org/data/definitions/316.html?utm_source=chatgpt.com "CWE - CWE-316: Cleartext Storage of Sensitive Information in Memory (4.20)"
[4]: https://www.usenix.org/blog/reliably-erasing-data-flash-based-solid-state-drives?utm_source=chatgpt.com "Reliably Erasing Data from Flash-Based Solid State Drives | USENIX"
[5]: https://developer.apple.com/documentation/security/storing-keys-in-the-keychain?changes=la&utm_source=chatgpt.com "Storing Keys in the Keychain | Apple Developer Documentation"
[6]: https://developer.apple.com/documentation/security/ksecattraccessiblewhenunlockedthisdeviceonly?utm_source=chatgpt.com "kSecAttrAccessibleWhenUnlockedThisDeviceOnly | Apple Developer Documentation"
[7]: https://developer.apple.com/documentation/Security/protecting-keys-with-the-secure-enclave?changes=_7&utm_source=chatgpt.com "Protecting keys with the Secure Enclave | Apple Developer Documentation"
[8]: https://developer.apple.com/documentation/cryptokit/secureenclave?changes=_7__6&utm_source=chatgpt.com "SecureEnclave | Apple Developer Documentation"
[9]: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html?utm_source=chatgpt.com "Cryptographic Storage - OWASP Cheat Sheet Series"
[10]: https://csrc.nist.gov/glossary/term/key_destruction?utm_source=chatgpt.com "Key destruction - Glossary | CSRC"
[11]: https://csrc.nist.gov/Projects/Key-Management/faqs?utm_source=chatgpt.com "Key Management | CSRC"
[12]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt2r1.pdf "Recommendation for Key Management: Part 2 – Best Practices for Key Management Organizations"
[13]: https://cwe.mitre.org/data/definitions/591?utm_source=chatgpt.com "CWE - CWE-591: Sensitive Data Storage in Improperly Locked Memory (4.20)"
[14]: https://cwe.mitre.org/data/definitions/591?utm_source=chatgpt.com "CWE-591"
