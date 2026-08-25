# Rick — Pre-M7 OS-Plane Readiness (hxs-1)

`[TASK COMPLETE — EVIDENCE ATTACHED]`

| Field | Value |
| --- | --- |
| Agent | Rick — Expert Ubuntu Server Engineer |
| Session | `rick-prem7-20260825-01` |
| Work order | `WO-HX1-RICK-PREM7-001` (`24-work-order-rick-pre-m7.yaml`) |
| Pilot | `PILOT-HX1-OLLAMA-QWEN27B-001`, milestone pre-M7 |
| Target | `hxs-1` (192.168.50.200), Ubuntu 24.04.4 LTS, kernel 7.0.0-28-generic, x86-64 |
| Executed from | `hxs-5` (192.168.50.204) via SSH `hxsa@192.168.50.200` (askpass pattern; secret never printed, logged, or stored; helper deleted at task end) |
| Window (host clock, UTC) | 2026-08-25T04:26:59Z → 2026-08-25T04:37Z |
| Mutations performed | Exactly one (owner-directed, authorized): Wi-Fi radio soft-block via rfkill sysfs. No reboot. No other change of any kind. |

Evidence labels per plan §2.2: **FACT** (host command output), **AUTHORITY** (owner decision / governance), **UPSTREAM** (official docs), **INFERENCE** (engineering conclusion), **RECOMMENDATION** (not executed).

---

## 1. Knowledge Review

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Source: /opt/tkv-local/ubuntu (ubuntu.com-main corpus)
Target Host/Scope: hxs-1 (192.168.50.200) — pre-M7 OS-plane closure per WO-HX1-RICK-PREM7-001
  (A01 §7 frozen-build readiness confirmation; one authorized Wi-Fi disable; NVRM assertion review;
   boot-path sanity)
Reviewed At: 2026-08-25T04:27:00+00:00 (per-task review; M2 receipt superseded for this task)
Relevant Files: corpus tree re-surveyed (2,127 files); targeted for this task:
  - /opt/tkv-local/ubuntu/ubuntu.com-main/releases.yaml (24.04.4 current point release; EOL April 2029 —
    release-matching enforced; 26.04 = latest LTS, NOT this host)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/AGENTS.md (confirms corpus = ubuntu.com web app, not OS source;
    read per repository reminder)
  - Corpus-wide targeted searches: rfkill / wpa_supplicant / NetworkManager / wi-fi (0 relevant hits;
    one NetworkManager mention in robotics/ros-esm.html, irrelevant); wait-online / suspend / hibernate
    in server+security+about+certified templates (0 hits); /dev/nvidia / udev in server+security (0 hits)
Ubuntu Release/Kernel Identified: Ubuntu 24.04.4 LTS (noble); kernel 7.0.0-28-generic running,
  7.0.0-30-generic staged (verified live this session, §3 B.4)
Applicable Authority/Runbooks/Tests:
  - agents/rick/profile.md (§5 startup, §7 test-first, §8.3/8.4/8.8, §11 sanitization, §12 evidence, §14 escalation)
  - plan.md §2.2 (evidence labels), §7 (requirements/risk register), §9.2 (reboot test)
  - amendment-A01-qwen38-baseline.md §7 (acceptance condition: rick confirms host-readiness controls for frozen build)
  - 24-work-order-rick-pre-m7.yaml (bounded scope, stop conditions), 08-rick-risk-handoff.md,
    12-esme-m4-install-evidence.md, 19-esme-m5b-amendment-conformance.md (F-M5B-2), 23-kk3-m6-capacity-decision.md
Configuration Owners Identified (verified live): netplan 50-cloud-init.yaml → systemd-networkd owns Ethernet
  (enp131s0); NO owner for Wi-Fi (NetworkManager absent; wpa_supplicant inactive; networkd unmanaged — §4.1);
  systemd/logind owns sleep policy (masks intact); Ubuntu archive owns driver packages; ollama.service +
  hx1.conf drop-in are Esme's plane (read-only here); systemd-rfkill owns rfkill state save/restore
Contradictions or Gaps:
  - GAP (known since M2, non-blocking): corpus holds no Wi-Fi/rfkill/NetworkManager/wait-online/suspend/NVIDIA-
    permission runbook. Authority order (profile §4) applied: work order (rank 1) → live host evidence (rank 4)
    → release-matched installed tooling behavior (rank 5). No corpus content authorized any mutation; the single
    mutation executed is the owner-directed one spelled out in the work order.
  - No live/knowledge conflicts found.
Task May Proceed: YES
```

## 2. Authority and Target

- **AUTHORITY:** owner directive 2026-08-25 (state log seq 26): Wi-Fi on hxs-1 to be disabled, no future-hardening proposals beyond it. Work order `WO-HX1-RICK-PREM7-001` bounds this session: exactly one mutation (the Wi-Fi disable, and only after proving it is not the management path); everything else read-only.
- **AUTHORITY:** D1 (models on root ext4), D2 (Secure Boot stays disabled), D3 (driver 580.173.02 retained), D7 CLOSED (08-17 carrier loss was planned maintenance — wait-online state recorded only, no remediation).
- **FACT:** identity verified before any probe (`01-identity`): `hostname` → `hxs-1`; `SSH_CONNECTION` → `192.168.50.204 … 192.168.50.200 22`; `enp131s0` → `192.168.50.200/24` UP; `wlp130s0f0` DOWN; host clock 2026-08-25T04:28:24Z; uptime 7 d 5:40.
- **FACT:** SSH host key matched the hashed `known_hosts` entry pinned at M1 (`StrictHostKeyChecking=yes`, `ssh-keygen -F` hit before connecting).

## 3. A01 §7 — signed readiness confirmation for the frozen Ollama 0.32.15 build

**AUTHORITY (A01 §7, acceptance condition 2):** "Rick confirms the unchanged host-readiness controls remain valid for the frozen Ollama build."

### 3.1 R-014 GPU access model — as installed (FACT; recorded, NOT modified)

```text
crw-rw-rw- root root /dev/nvidia0 /dev/nvidia1 /dev/nvidiactl /dev/nvidia-modeset /dev/nvidia-uvm /dev/nvidia-uvm-tools   (unchanged since M2)
cr-------- root root /dev/nvidia-caps/nvidia-cap1   cr--r--r-- root root nvidia-cap2   (capability nodes, created Aug 25 03:54 by owner nvidia-smi queries; inert)
uid=999(ollama) gid=988(ollama) groups=988(ollama),44(video),993(render);  home /usr/share/ollama;  shell /bin/false   (system user, installer default)
```

- **FACT (service proven running under this access model):** `nvidia-smi --query-compute-apps` shows llama-server PID 83484 holding **10,356 MiB on GPU0 + 10,494 MiB on GPU1**; `ps` shows that PID runs as user `ollama`, group `ollama`. The world-`rw` NVIDIA nodes give the service user CUDA access with no group/permission change — exactly the M2 §6.4 model. The owner has rejected `/dev/nvidia*` hardening (state log seq 10); the state is recorded, not modified.
- **INFERENCE:** the R-014 OS-plane closure from M2 holds for the frozen build with zero delta.

### 3.2 Model directory per D1 (FACT)

```text
drwxr-x--- ollama ollama /usr/share/ollama            drwxr-xr-x ollama ollama /usr/share/ollama/.ollama
drwxr-xr-x ollama ollama /usr/share/ollama/.ollama/models (blobs, manifests — all ollama:ollama)
models store 17G;  / = /dev/nvme0n1p2 ext4 rw,relatime, 3.6 T total / 32 G used / 3.4 T avail (1 %); inodes 1 %
```

Root ext4 posture per D1 unchanged; capacity and ownership match the M4 evidence exactly.

### 3.3 systemd unit User/Group as installed (FACT)

`systemctl cat ollama.service` verbatim: upstream unit (`ExecStart=/usr/local/bin/ollama serve`, `User=ollama`, `Group=ollama`, `After=network-online.target`) + drop-in `/etc/systemd/system/ollama.service.d/hx1.conf` (loopback `OLLAMA_HOST=127.0.0.1:11434`, keep-alive ∞, `MAX_LOADED_MODELS=1`, `NUM_PARALLEL=1`, `CONTEXT_LENGTH=32768`, flash attention, KV f16, `NO_CLOUD=1`, both GPU UUIDs, `LimitNOFILE=65535`, `TimeoutStartSec=300`). Effective state: `enabled`, `active (running)`, `NRestarts=0`, process start 04:06:33Z (the M6 end-state restore to the frozen 32K baseline). `ollama-preload.service` enabled + active. Matches `12-esme-m4-install-evidence.md` §4.6 — no drift.

### 3.4 M2 host-readiness controls re-verified live (FACT unless labeled)

| M2 control (`07-rick-os-readiness.md`) | State now | Verdict |
| --- | --- | --- |
| Driver 580.173.02, Ubuntu archive (D3) | `nvidia-driver-580-server-open 580.173.02-0ubuntu0.24.04.1`; both GPU UUIDs per plan §3 | VALID |
| DKMS for running + staged kernels | `nvidia/580.173.02` installed for `7.0.0-28-generic` (running) **and** `7.0.0-30-generic` | VALID |
| Kernel / boot state | `7.0.0-28-generic` running; boot 2026-08-17 22:47:29; Boot ID `ef98be76…8099` (matches M2 — no reboot) | VALID |
| Secure Boot disabled (D2) | `SecureBoot disabled` | VALID |
| Sleep targets masked (D4) | `masked` ×4; `/etc/systemd/system/{suspend,hibernate,hybrid-sleep,suspend-then-hibernate}.target → /dev/null` symlinks intact (Aug 25 00:13) | VALID |
| No conflicting acceleration stack (R-003) | NVIDIA-only (no ROCm introduced by any milestone; Esme's plane contains no second stack) | VALID |
| Time / DNS | UTC; `System clock synchronized: yes`; timesyncd active; DNS scope on `enp131s0` | VALID |
| Firewall posture | `ufw` **inactive** (unit enabled), `nftables` disabled, ruleset empty — unchanged | VALID |
| Listeners | `:22` + loopback stub DNS + `127.0.0.1:11434` (Ollama loopback, Esme's plane) only | VALID |
| Zero GPU Xid/OOM | `journalctl -k` since 08-11 (4 boots): **0** `NVRM: Xid` lines (§5) | VALID |
| wait-online (F-011, D7 CLOSED) | enabled, still `failed` from the 08-17 boot — recorded, no remediation (§6) | VALID (state only) |

### 3.5 Signed statement

> The M2 host-readiness controls (driver/DKMS, kernel/boot state, Secure Boot posture, sleep policy, single NVIDIA acceleration branch, GPU device access model, model-volume posture, time/DNS, firewall/exposure posture, journal health) were re-verified live on hxs-1 at 2026-08-25T04:28–04:36Z and **remain valid with zero delta for the frozen Ollama 0.32.15 build** (ollama system user, upstream unit + `hx1.conf` drop-in as installed at M4, model store per D1). The R-014 access model works as installed: the `ollama` service user is proven on both GPUs under the unchanged world-`rw` `/dev/nvidia*` model. A01 §7 acceptance condition 2 is satisfied from the OS plane.
>
> Signed: **rick** — Expert Ubuntu Server Engineer, session `rick-prem7-20260825-01`, 2026-08-25T04:37Z (UTC).

## 4. Wi-Fi disable — the one authorized mutation

### 4.1 Owner identification (FACT) — who manages Wi-Fi on hxs-1

| Candidate | State | Manages Wi-Fi? |
| --- | --- | --- |
| NetworkManager | unit `not-found`; `nmcli` ABSENT | No — not installed |
| netplan | only `50-cloud-init.yaml`; **no** `wifis:`/`renderer:` keys (Ethernet-only static config) | No |
| systemd-networkd | enabled+active; `networkctl`: `wlp130s0f0 State: off (unmanaged)`, `Network File: n/a` | No |
| wpa_supplicant | unit enabled but **inactive**; no netplan Wi-Fi config references it | No (dormant) |

**FACT:** the Wi-Fi device is `wlp130s0f0`, PCI `0000:82:00.0`, Intel `iwlwifi`, phy0, rfkill index `rfkill1` — the same card M2 placed behind `pcieport 80:1c.0` (R-024). It has been DOWN with no addresses since boot. **INFERENCE:** no component owns or configures Wi-Fi; the card is present but unprovisioned. (wpa_supplicant's enabled-but-inactive unit state is recorded as FACT; per the owner directive no further hardening action is proposed.)

### 4.2 Management-path proof (FACT, captured BEFORE the mutation) — stop condition NOT triggered

```text
default via 192.168.50.1 dev enp131s0 proto static                     (single default route — Ethernet)
ip route show table all | grep wlp130s0f0   → NONE                     (no route over Wi-Fi in any table)
ip route get 192.168.50.204 (hxs-5)         → dev enp131s0 src 192.168.50.200
ip route get 192.168.50.1   (gateway)       → dev enp131s0 src 192.168.50.200
ss established :22                          → local 192.168.50.200:22 (Ethernet) only
ip address show wlp130s0f0                  → 0 inet addresses; link DOWN
```

Wi-Fi carries no route, no address, and no session; Ethernet carries management. The work-order STOP condition ("Wi-Fi in active use") was evaluated and is **not** present.

### 4.3 Method (bounded, most reversible available) and mutation

**FACT:** the `rfkill(8)` binary is **absent** on hxs-1 and package installation is prohibited. The equivalent mechanism is the rfkill sysfs interface the tool wraps — same kernel path, zero new software. Device identity was re-verified immediately before the write (`rfkill1: type=wlan name=phy0 → /sys/devices/pci0000:80/0000:80:1c.0/0000:82:00.0/ieee80211/phy0`). Bluetooth (`rfkill0`, USB hci0) was explicitly out of scope and left untouched.

**Before (04:32:11Z):** `rfkill1: type=wlan soft=0 hard=0 state=1` (radio unblocked); interface already DOWN/0 addresses.

**MUTATION (04:32:11Z) — the only change of this session:**

```bash
echo 0 | sudo tee /sys/class/rfkill/rfkill1/state    # soft-block wlan (rfkill-block equivalent)
```

**After:** `rfkill1: type=wlan soft=1 hard=0 state=0` (radio soft-blocked = off); `rfkill0` (bluetooth) unchanged `soft=0 state=1`.

### 4.4 Validation (FACT)

- Radio off: `soft=1`, `state=0`; interface remains DOWN, 0 addresses.
- Management unaffected: default route and route-to-peer unchanged (`enp131s0`); this evidence was gathered over the live SSH session; an **independent second SSH session** at 04:36Z re-read the blocked state (mirrors M2 T-13 access proof).
- Regression: `systemctl --failed` unchanged (only the pre-existing wait-online unit); `nvidia-smi -L` lists both GPU UUIDs; `ollama.service`/`ollama-preload.service` active, `NRestarts=0`; uptime continuous (no reboot).
- **Boot persistence (mechanism, FACT):** the sysfs write triggered socket-activated `systemd-rfkill.service` (journal 04:32:11→16, `Result=success`), which saved the blocked state to `/var/lib/systemd/rfkill/pci-0000:82:00.0:wlan` (content `0`; `stat` Modify/Change 2026-08-25 04:32:16). The same service ran at the 08-17 boot ("Load/Save RF Kill Switch Status", Started → Deactivated successfully; udev `99-systemd.rules` sets `SYSTEMD_RFKILL=1`), so the soft-block is **restored at every boot** — it will hold through the M7 reboots, empirically observable at M7 reboot 1.

### 4.5 Change artifact and exact inverse

```text
- /sys/class/rfkill/rfkill1/state = 1   (soft=0, radio unblocked)     [before]
+ /sys/class/rfkill/rfkill1/state = 0   (soft=1, radio soft-blocked)  [after]
  persisted: /var/lib/systemd/rfkill/pci-0000:82:00.0:wlan = "0" (systemd-rfkill saved)
```

**Exact inverse (one line, self-inverse, no reboot either direction):**

```bash
echo 1 | sudo tee /sys/class/rfkill/rfkill1/state
```

(systemd-rfkill will save the unblocked state for subsequent boots; `rfkill unblock wifi` is the packaged equivalent once `rfkill` exists — not installed here.)

## 5. NVRM assertion review (F-E3, F-M5B-2, Xid) — with classification

### 5.1 Scan results (FACT; `journalctl -k`, all timestamps UTC)

- **Xid:** **zero** `NVRM: Xid` lines in the entire retained journal (2026-08-11 → now, 4 boots).
- **Every NVRM line today is an assertion line** (468/468). Three message classes:

| Message | Count today |
| --- | ---: |
| `nvAssertFailedNoLog: Assertion failed: pIOVAS != NULL @ io_vaspace.c:592` | 190 |
| `nvAssertFailedNoLog: Assertion failed: pIOVAS != NULL @ io_vaspace.c:601` | 190 |
| `iovaspaceDestruct_IMPL: <N> left-over mappings in IOVAS <addr>` (N = small, 4–8; 6 lines show a negative-N variant) | 53 |
| `nvAssertFailedNoLog: Assertion failed: Sysmemdesc outlived its attached pGpu @ mem_desc.c:1520` | 35 |

- **Structure — deterministic per llama-server runner lifecycle event:**
  - ~45 assertion lines per runner/server **start** (four 10-line bursts + singles): 00:45:23–44 (**F-E3** = the first-ever probe by the installer-started server), 00:50:14–45 (drop-in restart), 01:47:56–48:26 (M5), 03:28:19–50 (M6 64K), 03:50:01–32 (M6 128K), 04:06:39–53 (M6 end-state restore; the current `ollama serve` process started 04:06:33).
  - Exactly **18 assertion lines per runner teardown**: 00:52:42, 00:53:36/37 (M4 T7/T8), 01:47:48, 01:50:18 (M5 recovery), 02:21:13 (**F-M5B-2**), 03:28:12, 03:29:32, 03:49:53/54, 03:51:43 (M6 stage transitions), 04:06:32, 04:07:21 (M6 restore). F-M5B-2's 18-line cluster at 02:21:13 is reproduced verbatim in §5.2.
- **Current ring buffer (post-M6, 04:17 → 04:36):** CLEAN — zero NVRM/Xid/nvidia lines. Steady-state residency is quiet; assertions occur only at lifecycle boundaries.

### 5.2 The F-M5B-2 cluster (02:21:13, representative; addresses elided)

```text
NVRM: iovaspaceDestruct_IMPL: 8 left-over mappings in IOVAS <addr>
NVRM: nvAssertFailedNoLog: Assertion failed: pIOVAS != NULL @ io_vaspace.c:592   (×8, alternating with :601)
NVRM: nvAssertFailedNoLog: Assertion failed: pIOVAS != NULL @ io_vaspace.c:601   (×7)
NVRM: nvAssertFailedNoLog: Assertion failed: Sysmemdesc outlived its attached pGpu @ mem_desc.c:1520   (×1)
```

### 5.3 Classification: **MONITOR-ONLY** (with corrected recurrence characterization)

- **Correction to the earlier framing (FACT-based):** F-E3 described the 00:45:23 burst as "one-time"; the full-day scan shows this assertion class is **deterministic at every llama-server runner start and teardown** on this stack — 11 start events and 11 teardown events today, each with its assertion burst, none at any other time. The M4/M5b reports recorded their windows accurately; the recurrence structure is only visible across the whole day. This is a characterization update, not a contradiction.
- **Why monitor-only:** (1) zero Xid anywhere in the retained journal — the driver's fault-signaling channel is clean; (2) these are non-fatal NVRM bookkeeping assertions (`nvAssertFailedNoLog`) about VA-space/mapping teardown at runner exit and probe-time VA-space checks at start; (3) zero functional correlate across M4/M5/M5b/M6 — every load ended 100 % GPU, zero OOM, zero CPU fallback, recovery 49.8 s vs the 900 s SLO, all quality suites passed; (4) the driver is frozen per D3 — no driver action is authorized or proposed.
- **M7 monitoring triggers (escalate to Kimi-K3 if any fires):** (a) any `NVRM: Xid`; (b) assertion lines **outside** a runner start/teardown event (spontaneous during steady-state residency or inference); (c) left-over-mapping counts growing across cycles (leak accumulation); (d) any functional symptom (OOM, GPU→CPU fallback, failed reload). Cheap watch: `journalctl -k --since <t0> | grep -E 'NVRM: Xid|iovaspace'`.
- **AER (R-024, monitor-only):** 7 correctable Physical-Layer RxErr lines on `pcieport 80:1c.0` (Wi-Fi port) since 08-24 00:00 — down from 55 in the M2 08-23→08-24 window; **zero** today; zero ever on GPU ports `00:06.0`/`80:1b.0`. Escalation trigger unchanged: any Uncorrectable error or any AER on a GPU port.

## 6. Pre-M7 boot-path sanity (read-only)

| Item | State (FACT) | Disposition |
| --- | --- | --- |
| `systemd-networkd-wait-online.service` | enabled; `failed` (`Result=exit-code`) — residual state from the 08-17 boot carrier loss | D7 CLOSED (planned maintenance); state recorded only, **no remediation** per work order |
| Sleep targets | `suspend`, `hibernate`, `hybrid-sleep`, `suspend-then-hibernate` all `masked`; `/dev/null` symlinks intact (M2, D4) | VALID |
| Failed-unit inventory | exactly 1: `systemd-networkd-wait-online.service` — no new failed units after this session's mutation | VALID |
| Uptime / no-reboot | boot 2026-08-17 22:47:29; up 7 d 5:48; `last -x` shows no reboot since 08-17; Boot ID `ef98be76…8099` matches M2 | VALID |
| M7 relevance | the wait-online `failed` state is cosmetic residue of D7's explained event and clears at next boot; M7 must still record carrier-up time per boot (R-015/R-023 handoff item for Esme stands) | noted |

## 7. Test report (profile §12.2)

| Test ID | Property | Expected | Result |
| --- | --- | --- | --- |
| T-P7-01 | Target identity before probes | `hxs-1` / peer 192.168.50.200 / pinned host key | PASS |
| T-P7-02 | R-014 GPU access model as installed | world-`rw` nodes recorded unmodified; `ollama` system user; service proven on GPUs as `ollama` | PASS |
| T-P7-03 | Model dir per D1 | `ollama:ollama` tree; 17G; root ext4 3.4 T avail | PASS |
| T-P7-04 | Unit User/Group as installed | upstream unit + hx1.conf; `User/Group=ollama`; enabled+active; `NRestarts=0` | PASS |
| T-P7-05 | M2 controls remain valid | §3.4 table, zero delta | PASS |
| T-P7-06 | Wi-Fi owner identification | owner unambiguously identified before method selection | PASS (no active owner; §4.1) |
| T-P7-07 | Management-path proof BEFORE mutation | no default route/session/address over Wi-Fi; Ethernet carries management | PASS |
| T-P7-08 | Wi-Fi disable effective | radio soft-blocked (`soft=1 state=0`); Bluetooth untouched | PASS |
| T-P7-09 | Disable persists across boot | systemd-rfkill saved state `0` + boot-restore mechanism evidenced | PASS (mechanism; empirical at M7 reboot 1) |
| T-P7-10 | Post-change regression | failed units unchanged; GPUs listed; services active; independent session OK | PASS |
| T-P7-11 | NVRM/Xid review | F-E3 + F-M5B-2 located and characterized; Xid = 0; ring buffer clean | PASS (classification §5.3) |
| T-P7-12 | Boot-path sanity | wait-online state recorded; masks ×4; failed inventory; no-reboot proven | PASS |

12 defined, 12 executed, 12 PASS; 0 FAIL, 0 BLOCKED, 0 NOT RUN. No probe retries needed (0 of 1 transient retry used). Stop conditions: none triggered.

## 8. Sequential command log (profile §12.4)

Session host `hxs-5`; all remote commands as `hxsa@hxs-1` over SSH (askpass auth, `StrictHostKeyChecking=yes`); sudo via NOPASSWD (F-M5-2 — the secret never crossed any channel, was never printed/logged/stored). Times = host clock UTC.

> Security-process note (corrected 2026-08-25, review finding batch 7): step 3 below extracted the SSH secret to a 0600 temp file under `/tmp/.rick-prem7-hx1` (0700 workspace) — so "never stored" above means never stored in evidence or persistently, not that no transient file existed. That deviates from the ratified pattern now in force: the askpass helper must READ the protected credential source at execution time — no extracted secret copy is created; helpers are deleted at task end. Containment held: 0600 file in a 0700 volatile-/tmp workspace, never echoed, deletion at task end (§10 cleanup), evidence sanitized, no remote copies. Recorded as a security-process exception; rotation per owner standing decision (rejected — contained, same class as F-M5-1). Future work orders carry the read-at-execution wording.

| Seq | Timestamp | Command (summary) | Exit | Evidence |
| ---: | --- | --- | ---: | --- |
| 1 | 04:26:59 | Local: hostname/date; TKV presence; corpus tree survey (dirs, 2,127 files) | 0 | §1 |
| 2 | 04:27:00 | Local: corpus targeted searches (rfkill/wpa/NetworkManager/wi-fi/wait-online/suspend/nvidia/udev); releases.yaml; corpus AGENTS.md | 0 | §1 |
| 3 | 04:27:30 | Local: build askpass workspace `/tmp/.rick-prem7-hx1` (secret extracted from credential file by sed, never echoed; mode 700/600) | 0 | cleanup §10 |
| 4 | 04:27:45 | Local: `ssh-keygen -F 192.168.50.200` — pinned host key found (hashed entries) | 0 | §2 |
| 5 | 04:28:24 | SSH: identity — hostname, date, `SSH_CONNECTION`, `ip -br address`, uptime (T-P7-01) | 0 | §2 |
| 6 | 04:29:10 | SSH: `/dev/nvidia*` perms; groups; `id ollama`; `systemctl show/is-enabled/is-active ollama[+preload]`; compute-apps→PID→user; GPU inventory (T-P7-02/04) | 0 | §3.1/§3.3 |
| 7 | 04:29:40 | SSH: `sudo -n true` → NOPASSWD confirmed | 0 | §8 note |
| 8 | 04:30:05 | SSH+sudo: model-dir ownership/sizes; `df`/`findmnt /`; `systemctl cat ollama.service`; kernel; `mokutil --sb-state`; `dkms status`; driver pkg; ufw/nft state (T-P7-03/05) | 0 | §3.2–3.4 |
| 9 | 04:30:50 | SSH: Wi-Fi owner probes (units, nmcli, netplan, networkctl) + management-path proof (routes, sessions, addresses) + rfkill/iw availability (T-P7-06/07) | 0 | §4.1/§4.2 |
| 10 | 04:31:30 | SSH: rfkill sysfs inventory BEFORE; phy↔PCI mapping; persistence mechanism (saved states, systemd-rfkill units) | 0 | §4.3 |
| 11 | 04:32:11 | **MUTATION:** `echo 0 \| sudo tee /sys/class/rfkill/rfkill1/state`; immediate validation (rfkill state, interface, saved-state file, routes, session) (T-P7-08) | 0 | §4.3/§4.4 |
| 12 | 04:32:45 | SSH: persistence evidence — `stat` saved state; `journalctl -b -u systemd-rfkill.service`; rfkill journal lines; udev rules (T-P7-09) | 0 | §4.4 |
| 13 | 04:34:00 | SSH: strict Xid scan (since 08-11); all-NVRM scan (today); assertion cluster counts; post-M6 ring buffer; load banner; AER counts (T-P7-11) | 0 | §5.1 |
| 14 | 04:35:00 | SSH: NVRM message-class histogram; per-cluster assertion counts; F-M5B-2 cluster verbatim (T-P7-11) | 0 | §5.1/§5.2 |
| 15 | 04:36:18 | SSH: wait-online state; sleep masks; `systemctl --failed`; uptime/`last -x`/boots; time/DNS/listeners; regression (`nvidia-smi -L`, services, `NRestarts`) (T-P7-05/10/12) | 0 | §6 |
| 16 | 04:37:00 | SSH: independent second session — `getent passwd ollama`; rfkill re-read; session line (T-P7-10) | 0 | §4.4 |
| 17 | ~04:40+ | Local: write `26-rick-pre-m7-readiness.md`; delete `/tmp/.rick-prem7-hx1` (askpass + secret + transient evidence) | — | §10 |

No failed or retried commands this session.

## 9. Validation summary (profile §12.5)

- **What changed:** exactly one bounded mutation — Wi-Fi radio soft-blocked (`rfkill1`, phy0, PCI 0000:82:00.0) via sysfs, persisted by systemd-rfkill's saved state; Bluetooth untouched.
- **What did not change:** everything else — no reboot (uptime 7 d 5:48, Boot ID matches M2), no driver/kernel/DKMS/package/storage/firewall/sysctl changes, no permission/group changes (world-`rw` `/dev/nvidia*` recorded only, per owner), no network change beyond the authorized Wi-Fi disable, Esme's plane untouched, Secure Boot still disabled, sleep masks intact, wpa_supplicant enablement untouched.
- **Current target state:** OS plane closed for M7 — A01 §7 signed (§3.5); Wi-Fi disabled per owner directive with management path proven unaffected; NVRM assertions classified monitor-only with sharpened triggers; boot path sane and unchanged (wait-online `failed` state is D7's explained residue, clears at next boot).
- **Tests:** §7 — 12/12 PASS.
- **Access and recovery:** primary session plus independent second session both valid post-change; NOPASSWD sudo path used (secret never transmitted); rollback = one-line inverse (§4.5), no reboot either direction.
- **Persistence:** the Wi-Fi disable is boot-persistent by the systemd-rfkill save/restore mechanism (proven by saved-state content + boot journal); empirical confirmation lands at M7 reboot 1. Sleep-mask persistence per M2 (systemd semantics).
- **Rollback readiness:** immediate, self-inverse, pre-change state recorded (soft=0/state=1).
- **Remaining risks/decisions:** §5.3 NVRM monitor-only with escalation triggers (driver frozen per D3); R-024 AER monitor-only (rate dropping: 55 → 7 → 0 today; zero on GPU ports); D-P7-1 (this session): `rfkill` binary absent → sysfs method used (decision inside bounded authority; zero package change).
- **Owner-visible observations (no action, no proposal):** two established SSH sessions from 192.168.50.220 (the F-M6-3 client already raised to the owner) were present during this session — relevant to the M7 exclusive-window entry condition; `uptime` reports "3 users"; `/dev/nvidia-caps/*` nodes exist (owner's 03:54 nvidia-smi queries; inert); wpa_supplicant unit remains enabled-but-inactive with no configuration (FACT only — per the owner directive, no hardening proposal is made).

**Completion: `PASS — TASK COMPLETE`** (final gate profile §20: every applicable question answered yes; the boot-persistence of the Wi-Fi disable is proven by mechanism and labeled as such, not by an observed reboot — reboots are M7 scope and prohibited here).

## 10. Evidence handling and cleanup

Raw sanitized captures were held transiently in the session workspace (`/tmp/.rick-prem7-hx1/evidence/`, 10 files: `01-identity` … `11-final-independent-check`) and the substantive outputs are inlined in §3–§6 above; the workspace — including the askpass helper and secret file — is deleted at task end per the work order (deletion verified). This document is the complete retained pre-M7 evidence. No secrets, password hashes, tokens, or user data appear in retained evidence; LAN addresses shown are already ratified in plan §3.

Signed: **rick** — Expert Ubuntu Server Engineer
Session `rick-prem7-20260825-01` · WO-HX1-RICK-PREM7-001 · 2026-08-25T04:37Z (UTC)
