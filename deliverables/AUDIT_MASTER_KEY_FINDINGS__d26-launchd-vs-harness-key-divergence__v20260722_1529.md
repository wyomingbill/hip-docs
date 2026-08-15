# Audit: Master Key Findings (D-26)

Status: BUILT
Reconciled-Against: truncated sha256 comparison run 2026-07-22 15:29 on [REDACTED-MACHINE-NAME], against the live filesystem and the installed launchd job com.hip.demo.dashboard.plist
Version: v20260722_1529 MT
Prepared-By: Claude (Sonnet 5)
Purpose: read-only audit confirming or refuting D-26 (launchd plist bakes a different master-key path than the harness default) without exposing key material or plist secret values

This document records conclusions only. It intentionally omits file paths and hash values.
The full inventory, including paths and truncated hashes, is held locally at ~/hip-audit on
the machine where the audit was run. It is deliberately not committed to this repository.

No key file was moved, renamed, overwritten, or destroyed in the course of this audit. The
harness was not run. No graph writes occurred.

## Distinct master key file count

Exactly 2 distinct master key files exist on the audited machine, confirmed by content hash.

## Harness-resolved key versus launchd-resolved key

Both a harness-resolved default key and a launchd-resolved key exist. They are not the same
file. Confirmed by truncated hash comparison: the file the launchd-managed process actually
opens does not match the file the canonical harness default resolves to.

## D-26 status

D-26 is confirmed. The installed launchd job bakes a different key path than the harness
default resolves to.

## Plist embedding a literal key value versus a path

The relevant environment variable in the installed launchd plist holds a filesystem path, not
a literal key value embedded in the plist. No, the master key is not embedded as a value in
the plist.

Separately, and outside the scope of the master-key question, the same plist was observed to
hold several other credentials as literal plaintext values rather than paths. Those variable
names are noted in the local inventory. Their values were not read or printed as part of this
audit.

## Scope note

This document does not identify which key file should be destroyed, retired, or treated as
canonical going forward. That decision belongs to the repository owner and is out of scope
for an audit document.

## Governance note

This finding is an infrastructure/defect-tracking result (D-26), not a change to any research
artifact that backs a WP claim. Part II of the WP-to-research mapping (Section C of this
MANIFEST) already carries a NEEDS-UPDATE note about the single-master-key, not-yet-per-member
state of encryption today. This audit does not change that conclusion; it adds an operational
detail (two key files exist across environments, and the deployed demo path uses a different
one than the harness default) that does not alter what Part II claims. Section C was not
modified by this commit.

## Pointer

Full inventory, including exact file paths, sizes, mtimes, and truncated hashes, is held
locally at ~/hip-audit on the audited machine. It was deliberately not committed here.
