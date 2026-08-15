# HA-35 mutation-baseline records — BANKED EVIDENCE COPIES

Banked by **HA-36** per Bill's rider, 2026-08-11. **These are COPIES. The active log was not
moved, rewritten, trimmed or touched** — it remains `logs/mutation_survivors.jsonl`, which is
gitignored, and remains the only record the mutation harness reads.

**Where they live, and why not a new folder:** `docs/dispatches/`, alongside HA-33's
preserved `HA33_writestate_guard_not_landed.patch` — the existing precedent for banking a
non-document artifact next to the dispatch that owns it. CLAUDE.md's Docs Organization list is
LOCKED and adding a folder requires updating that file and `docs/INDEX.md`; that is a
governance change, not this dispatch's business.

**Why copies exist at all:** `logs/` is not under version control, so HA-35's restoration and
backfill records — the ones that repaired the mutation baseline — had no durable provenance
beyond their own bodies and HA-35's dispatch doc. These copies put them in the repo where they
can be diffed against the originals.

## What is banked

`HA36_BANKED_HA35_mutation_baseline_records.jsonl` — two lines, byte-identical to their source lines, in
source order.

| # | source record index | record_type | source timestamp | sha256 of the source LINE |
|---|---|---|---|---|
| 1 | **144** | `restoration` | `2026-08-11T13:14:44.248361+00:00` | `47a7ac37921a72211d6aea288e38c05f57edf50ed1295aa89e1c59ea67fefb34` |
| 2 | **145** | `baseline_backfill` | `2026-08-11T13:24:41.221662+00:00` | `1c6e2b9d9c4ce4d56ed6117c676d3e7176d6bc8e6871981850ca0289933242c6` |

- Source file at banking time: **149 records**.
- Record 144 re-affirms source record **141**
  (`2026-08-10T22:50:28.012131+00:00`), content digest
  `eeb95a7bfa024faa`, verified revision
  `a2c27be`.
- Record 145 backfills fingerprints at revision
  `a2c27be`:
  **33/33**
  survivors fingerprinted,
  **7** killed entries left absent on purpose.
- Recomputed content digest of the banked restoration record: `eeb95a7bfa024faa`
  (equals the source digest above — the copy carries the same survivor set).
- sha256 of the banked file itself: `f0e6384925056252c169e5f22afb08a6d913e64a1a62fb55d5f40da75065e902`

## How to check a copy against its original

```sh
# line N of the active log, 1-indexed, must hash to the value in the table above
sed -n '145p' logs/mutation_survivors.jsonl | tr -d '\n' | shasum -a 256
sed -n '146p' logs/mutation_survivors.jsonl | tr -d '\n' | shasum -a 256

# or compare the banked lines directly
diff <(sed -n '145p;146p' logs/mutation_survivors.jsonl) \
     docs/dispatches/HA36_BANKED_HA35_mutation_baseline_records.jsonl
```

**A mismatch is information, not necessarily corruption.** The active log is APPEND-ONLY, so
the indices above stay valid as it grows; but if the file were ever rebuilt, an index would
move. The `sha256 of the source LINE` column is the durable identifier — match on the hash,
not on the line number.

**These copies are evidence, not a baseline.** Nothing reads them. `read_last_survivor_run`
reads the active log and only the active log; restoring from these would be a new ruling, not
a routine operation.
