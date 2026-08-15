# DISPATCH_FM10 — unload the launchd `voice_https_orch` service
Status: BUILT — **service stopped and persistently disabled; plist left on disk**
Reconciled-Against: live machine state, 2026-08-14 16:27–16:30 MDT

**TYPE:** OPERATIONAL. **No code changed, no file in any repo modified except this doc, its
INDEX row and the board.** The only machine change is the launchd service state.

**Bill's authorization, verbatim: "Unload it."**
**SCOPE HELD EXACTLY: stop only. NOT rebound to loopback. Plist NOT deleted.**

**CLAIM IMPACT: none.**

---

## THE EXPOSURE, AND WHY THIS IS THE SECOND KILL

`server.voice_https_orch` was listening on **`*:7860` — all interfaces**, not loopback. FM 1
recorded it as the one service on this machine bound to `0.0.0.0` while every Neo4j instance and
the demo dashboard bind `127.0.0.1`.

**It was killed once before — pid 16242, during trust-boundary phase 0 — and it came back.**

**Launchd is why.** The service is a `LaunchAgent` with:

| key | value | effect |
|---|---|---|
| `RunAtLoad` | **`true`** | starts at login |
| `KeepAlive` | **`{ SuccessfulExit = false }`** | relaunches whenever it exits non-zero |

And its program is not the server directly — it is a `bash -c` wrapper that **force-kills whatever
holds the port and then takes it**:

```
lsof -ti:7860 | xargs kill -9 2>/dev/null; sleep 1; exec … -m server.voice_https_orch --host 0.0.0.0 --port 7860
```

**So a manual `kill` could never have held.** `KeepAlive` restarts the job, and the wrapper's own
first act is to kill any competitor for the port. `launchctl print` recorded **`runs = 2`** at the
moment of this dispatch — the direct evidence that it had already been killed once and restarted.

**Killing the process was never the fix. Unloading the job is.**

---

## BEFORE

```
$ lsof -nP -iTCP:7860 -sTCP:LISTEN
COMMAND   PID    USER   FD   TYPE   DEVICE   SIZE/OFF  NODE  NAME
Python  72415 bill-ai   15u  IPv4  0x7438…      0t0    TCP   *:7860 (LISTEN)
```

- **pid 72415**, started **09:27:36**, parent **1** (reparented to launchd).
- Command: `… -m server.voice_https_orch --host 0.0.0.0 --port 7860`.
- **`*:7860` — all interfaces.**
- **Established connections at the time of the change: NONE.** Only the listener; nothing was
  torn out from under a live client.

```
$ launchctl print gui/501/com.hip.voice.orch
gui/501/com.hip.voice.orch = {
    state = running
    pid   = 72415
    runs  = 2
    path  = [REDACTED-USER-PATH]/Library/LaunchAgents/com.hip.voice.orch.plist
    type  = LaunchAgent
    working directory = [REDACTED-USER-PATH]/hip-vo
}
```

---

## THE COMMANDS, AND WHY BOTH WERE NEEDED

```
launchctl disable gui/501/com.hip.voice.orch     # exit 0
launchctl bootout  gui/501/com.hip.voice.orch     # exit 0
```

**`bootout` ALONE WOULD NOT HAVE SATISFIED THE DISPATCH.** The requirement was that the service
stop **and not return at next boot**. `bootout` removes the job from the running domain — it stops
it now — but the plist lives in **`~/Library/LaunchAgents`**, and **launchd loads that directory at
every user login.** Since the dispatch also requires the plist to stay on disk, `bootout` on its own
would have been undone by the next login.

**`disable` is what makes it persist.** It writes a **disabled override into launchd's own
persistent store**, keyed by label — a record that is independent of the plist file and survives
reboot. The plist can remain exactly where it is and still not load.

**Order: `disable` first, then `bootout`**, so there is no window in which `KeepAlive` could
relaunch the job between the two commands.

**Re-enabling is therefore a deliberate two-step act**, which is the property worth having:
`launchctl enable gui/501/com.hip.voice.orch` followed by `launchctl bootstrap gui/501 <plist>`.
Nothing about a future requirement can re-enable it by accident.

---

## AFTER — all four checks

| check | result |
|---|---|
| `lsof -nP -iTCP:7860 -sTCP:LISTEN` | **nothing listening** ✓ |
| `kill -0 72415` / `ps -p 72415` | **pid 72415 gone**, not present in `ps` ✓ |
| `launchctl print gui/501/com.hip.voice.orch` | **`Could not find service "com.hip.voice.orch" in domain for user gui: 501`** — not loaded ✓ |
| `launchctl print-disabled gui/501` | **`"com.hip.voice.orch" => disabled`** — persistent, survives reboot ✓ |

---

## THE PLIST — LEFT ON DISK, UNLOADED

```
[REDACTED-USER-PATH]/Library/LaunchAgents/com.hip.voice.orch.plist
-rw-r--r--  1 bill-ai  staff  1406  Aug 12 19:57
```

**Not deleted, not edited, byte-unchanged.** Recorded here so the service can be **deliberately**
re-enabled if a future requirement needs it, without reconstructing the job definition.

### ⚠ FINDING, FILED NOT FIXED — THE PLIST CARRIES THREE LIVE SECRETS IN PLAINTEXT

`com.hip.voice.orch.plist` sets **three secret-bearing environment keys in cleartext**:
**`GROQ_API_KEY`**, **`NEO4J_PASSWORD`**, **`SERPAPI_KEY`**. Their **values are deliberately not
reproduced in this document, and were redacted from every command output captured for it** —
`launchctl print` prints them in full to anyone who can run it.

**Two consequences worth stating separately:**

1. **The file is `-rw-r--r--` — world-readable** on this machine.
2. **`launchctl print` exposes them to any process running as this user**, independent of the file
   mode.

**This is adjacent to FM 4** (*credential rotation after review-package exposure*, STOPPED) and is
**not** resolved by this dispatch. **Unloading the service does not rotate a credential.** Filed
here so it is attached to the plist's path rather than discovered again later. **NEEDS BILL** —
whether these three join FM 4's rotation scope.

---

## BILL'S THREE CONFIRMATIONS, RECORDED

Recorded here because this is the dispatch that was open when they were given.

1. **F5 — POST-FREEZE.** The caller-supplied-transcript / SPOKEN-provenance finding is **not**
   freeze-blocking; it is addressed after the demo freeze.
2. **`TD-V-Pnnn` POINTER ROWS ARE A STANDING CONVENTION.** A pointer row in one lane's register,
   naming a finding owned by another lane, is the sanctioned way to make a cross-lane defect
   findable — it is **not** a duplicate ID and does not re-open the numbering question that
   STANDARD PREAMBLE item 10 settles.
3. **THE FREEZE IS PENDING VD-62.** The demo freeze is not taken; **VD-62** — *gate the open read
   endpoints, retire `/ws/voice`, recertify* — stands between the VD-60 rehearsal and the freeze.

---

## WHAT THIS DISPATCH DID NOT DO

- Did **not** rebind anything to loopback. The service is stopped, not reconfigured.
- Did **not** delete or edit the plist. Byte-unchanged on disk.
- Did **not** touch `~/hip-vo`, the service's working directory, or any repository file other than
  this doc, its INDEX row and the board row.
- Did **not** rotate, print or commit any credential value.
- Did **not** stop, restart or inspect any other service, graph or port.
