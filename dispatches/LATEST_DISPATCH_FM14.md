# FM 14 — MID-RUN DETECTION IN `lane_preflight` (FM12-1)
Status: BUILT — **LANDED**
Reconciled-Against: 2026-08-14, `~/hip-roadmap` @ `roadmap`. Claim `66ea478`/`eb3b4f6`,
REQ amendment `d96149a`, build `a58bc8e`.

REQ: `docs/requirements/REQ_PROCESS_HARDENING_TOOLS__claim-lane-register-doc-lane-preflight-scrub__v20260814_1613.md`
— **AMENDMENT 1**, filed at `d96149a` **before the first code edit**, as Bill directed
(*"amend REQ_PROCESS_HARDENING_TOOLS, don't file new"*).

---

## 0. THE EXCEPTION LINE

```
FM 14 — MID-RUN DETECTION IN lane_preflight (FM12-1)
COMPLETE WITH FINDINGS — 2 ITEMS FILED, NOTHING BLOCKING
```

**Five twins, 30 assertions, all green.** Ten of them are new and every one runs in both
directions.

---

## 1. THE GAP, RESTATED FROM THE INCIDENT

FM 12 measured it: **all seven lock resources reported `free`** while PID 2827 ran a
20-iteration canonical battery in `~/hip-cutover-demo` against `bolt://localhost:7690`,
holding an ESTABLISHED socket for the duration.

**`hip_lock.py` was not wrong.** It locks what a caller asks it to lock, and a battery never
asks. The gap was that **no instrument answered "is anything running"**, so every dispatch
needing that answer hand-rolled a `ps` pipeline — and reading the lock table instead returns a
*confident false all-clear*, which is the most expensive kind of wrong.

---

## 2. WHAT WAS BUILT

`lane_preflight.py --busy`, plus the same scan wired into the lane gate.

### 2.1 Two independent signals, because either alone has a blind spot

| signal | what it catches | blind spot it covers |
|---|---|---|
| **work processes** — battery, ratchet, injection harness, `gate_check`, governance suite, `pytest`, seed/reset | a job between connections | a connection can outlive the command that opened it |
| **ESTABLISHED bolt connections per graph port** | a live client on a lane's graph | a process can be missed by a name pattern |

### 2.2 It reports WHAT and WHERE, which is the difference between a warning and a fact

**WHAT** is pid, elapsed time and the matched command line. **WHERE** is the process's working
directory, resolved with `lsof -a -p PID -d cwd` — that is what turns *"something is running"*
into *"something is running in this lane"*. For connections it is the port, the socket, the
owning pid and that pid's cwd.

### 2.3 It says what it scanned even when it finds nothing

A silent pass is indistinguishable from a scan that never ran, so the output always echoes the
patterns and the ports before any verdict.

### 2.4 A RESIDENT SERVICE IS NOT MID-RUN — the distinction that keeps the tool usable

**Found while building it, on this machine:** `server.demo_dashboard` (pid 1983) held **four
ESTABLISHED sockets to 7690** with 44 minutes uptime, listening on 7872. A naive scan called
that BUSY — which would have made the demo lane **permanently** blocked and the gate
permanently ignored. **That is how a gate dies.**

**The rule:** a process that holds a `LISTEN` socket is a **server**; its pooled connections
are reported as `OCCUPIED` and do not refuse. **A battery is not a server** — it opens
connections, works, and exits. So the blocking signal is a work process or an **unattributed**
client connection.

### 2.5 The lane gate is scoped; `--busy` is machine-wide

For a lane check, blocking means **work processes whose cwd is inside THIS tree** plus
**non-resident connections on THIS lane's port**. A battery in another tree does not block this
one unless it is on this lane's graph — which the second term catches. Blocking on machine-wide
activity would make the gate noise, and noise is ignored.

`--busy` with no tree is the machine-wide form: **the check FM 12's precondition should have
been able to call.**

### 2.6 Fail-closed

`ps` or `lsof` failing is **exit 8 — SCAN UNAVAILABLE**, never a silent green. Same rule
`push_docs.sh` now follows for its pattern: no scan must never mean "clean". Proven in the twin
by running with a broken `PATH`.

**Exit codes:** `7` BUSY, `8` SCAN UNAVAILABLE — added alongside the existing 2/4/5/6.

---

## 3. THE TWIN — BOTH DIRECTIONS, AND INDEPENDENT OF MACHINE STATE

**The twin creates its own subject and scans its own port.** A twin that scanned the real ports
would be measuring the weather — passing on a quiet machine, failing during someone else's
battery — and proving nothing about the tool.

| assertion | result |
|---|---|
| **F1 GREEN** clean machine passes | **PASS** — exit 0 |
| **F1** states what was scanned (a silent pass is not a pass) | **PASS** — patterns and ports echoed |
| **F2a RED** live process REFUSED | **PASS** — exit **7** |
| **F2a** names **WHAT** (pid + elapsed + command) | **PASS** |
| **F2a** names **WHERE** (working directory) | **PASS** — cwd resolved via `lsof` |
| **F2a** goes green once the process exits | **PASS** — detection is live, not sticky |
| **F2b RED** live bolt-style connection REFUSED | **PASS** — exit **7** |
| **F2b** names the connection and its owner | **PASS** |
| **F2b** classifies the LISTENER as resident, not mid-run | **PASS** |
| fail-closed: scan failure is exit 8, never a silent green | **PASS** |

**Full suite: `python3 scripts/lane_tools_selftest.py` → ALL FIVE TWINS GREEN, 30 assertions.**
The four pre-existing twins were re-run and are unchanged.

**One honest note, the same shape as FM 9's:** the first run of the new twin went **RED on
`F2a names WHERE`**, and the tool was not the problem — the twin spawned its subject without
giving it a working directory of its own, so there was nothing distinctive to find. Fixed in
the twin. **A twin that is wrong in the green direction would have passed a broken tool just as
easily**, which is why it is recorded rather than quietly corrected.

---

## 4. LIVE RESULT — IT WORKED ON THE FIRST REAL RUN

Run against this machine while building it, `--busy` found, correctly and unprompted:

- **four ESTABLISHED connections to 7690** from `server.demo_dashboard` in
  `~/hip-cutover-demo` — classified **OCCUPIED (resident)**, not blocking;
- **three live processes in `~/hip-vo`**, two seconds old, belonging to another session's run.

**The second one is the FM 12 case exactly**: real activity in another lane that no lock
records and that no dispatch would have seen without asking `ps`.

---

## 5. FILED, NOT BLOCKING (2)

**(FM14-1) The pattern list is a name list, and a name list is never complete.** `WORK_PATTERNS`
catches the work this project actually runs, but a job invoked under a name nobody thought of is
invisible to the process half of the scan. **The connection half is the backstop** — that is why
there are two signals and not one — but a job that is between connections at the moment of the
scan can still slip both. **The stronger form is to treat any non-resident client on a graph
port as blocking regardless of its name, which is already the behaviour**; the residual gap is a
CPU-bound job that holds no socket. Named, not chased.

**(FM14-2) `--busy` is available, not yet mandatory.** Nothing forces a dispatch to call it —
the same adoption gap FM9-2 recorded for `claim_lane.py`. FM 12's precondition now *has* a real
check to call, and calling it is still a convention. The shared pre-commit hook (FM 9 §5, still
unflipped) is the only mechanism on the table that would make any of these tools unavoidable.

---

## 6. WHAT THIS DISPATCH DID NOT DO

- **Touched no product runtime code.** `scripts/` only, on `roadmap`, as directed.
- **Signalled, stopped or touched nothing it found.** The scan is strictly read-only — `ps` and
  `lsof` and nothing else.
- **Filed no new REQ** — Amendment 1 was appended to the existing one, which stands unchanged
  above the amendment line.
- **Ran no battery, harness or gate**, and wrote to no graph.
- **Did not flip `core.hooksPath`** — still unset, still FM 12's open item.

---

## 7. CLAIM IMPACT

```
CLAIM IMPACT: none
```

---

## 8. VERIFIED

- Machine gate: `bill-ai` @ `[REDACTED-MACHINE-NAME]`, `~/hip-roadmap` @ `roadmap`.
- **REQ amendment `d96149a` precedes the build `a58bc8e`** in the commit graph, and touches no
  file under `scripts/`.
- `python3 scripts/lane_tools_selftest.py` → **ALL FIVE TWINS GREEN**, 30 assertions.
- All five worktrees still pass `lane_preflight.py` with the new scan wired into the gate.
- Board rows written by `claim_lane.py` under the repo lock, board-only, no passengers.
