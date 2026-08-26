# Rick — M1 hxs-2 OS Readiness Report

`[TASK COMPLETE — EVIDENCE ATTACHED]`

| Field | Value |
| --- | --- |
| Agent | Rick — Expert Ubuntu Server Engineer |
| Session | `rick-m1-20260826-01` |
| Work order | `WO-HXS2-RICK-M1-001` (`02-work-order-rick-m1.yaml`) |
| Context packet | `03-context-packet-rick-m1.yaml` (goal `GOAL-HXS2-CODERX-001` v1) |
| Pilot | `PILOT-HXS2-CODERX-BACKEND-001` |
| Target | `hxs-2` (192.168.50.201), Ubuntu 24.04.4 LTS (noble), kernel **7.0.0-30-generic** (live-verified; see F-01), x86-64 |
| Executed from | `hxs-5` (192.168.50.204) via SSH `hxsa@192.168.50.201` (askpass pattern; secret read from the credential-record table at execution time only, never printed/logged/stored; helper deleted at task end) |
| Window (host clock, UTC) | 2026-08-26T03:24:11Z → 2026-08-26T03:32:43Z |
| Owner decisions applied | D1 (model store = root ext4), D2 (endpoint allowlist 192.168.50.0/24, ufw staged now / enabled at M8), D3 (CoderX vision-Q4_K_M — no OS-plane action), D4 (Wi-Fi rfkill soft block formalized); standing: Secure Boot stays disabled |
| Mutations performed | Exactly two: (a) `systemctl mask` of sleep/suspend/hibernate/suspend-then-hibernate targets; (b) rfkill soft block of the Wi-Fi device. No reboot. No other change of any kind. |

Evidence labels: **FACT** (live host output), **AUTHORITY** (owner decision / work order / governance), **INFERENCE** (engineering conclusion), **RECOMMENDATION** (not executed).

---

## 1. Knowledge Review

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Source: /opt/tkv-local/ubuntu (ubuntu.com-main corpus, 2127 files) + /opt/tkv-local/servers/hxs-2/ (discovery.md, driver-results.md, pre-work-results.md — historical cross-check only)
Target Host/Scope: hxs-2 (192.168.50.201) — M1 OS readiness, staged ufw design, two authorized mutations per WO-HXS2-RICK-M1-001
Reviewed At: 2026-08-26T03:17Z→03:23Z (from hxs-5)
Relevant Files: 10+
  - /opt/tkv-local/ubuntu/ubuntu.com-main/AGENTS.md
  - /opt/tkv-local/ubuntu/ubuntu.com-main/releases.yaml  (24.04 "noble", point release 24.04.4, EOL April 2029; 26.04 = latest LTS — release-matching enforced)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/about/release-cycle.html, about/release_cycles/ (ubuntu-eol, kernel-eol)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/security/ (index, platform-security, cves/notices/oval/osv/vex pages)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/certified/ + templates/server/ (support posture reference)
  - Corpus-wide targeted searches: "rfkill"/"systemd-rfkill"/"suspend-then-hibernate" (0 hits), "secure boot" (marketing/platform pages only) — same known gap as hxs-1 M1/M2
  - /opt/tkv-local/servers/hxs-2/discovery.md (as-found 2026-08-12), driver-results.md, pre-work-results.md
  - pilots/PILOT-HX1-OLLAMA-QWEN27B-001/03,07 (readiness pattern reference)
Ubuntu Release/Kernel Identified: Ubuntu 24.04.4 LTS (noble); running kernel 7.0.0-30-generic (HWE; installed = archive candidate 7.0.0-30.30~24.04.1); systemd 255 (journal/udev evidence); dkms 3.0.11-1ubuntu13
Applicable Authority/Runbooks/Tests:
  - agents/rick/profile.md (startup §5, lifecycle §6, test-first §7, sanitization §11, escalation §14)
  - 02-work-order-rick-m1.yaml (two authorized mutations; read-only otherwise; stop conditions)
  - 03-context-packet-rick-m1.yaml (13-check enumeration; staged ufw content; evidence requirements)
  - servers/AGENTS.md records contract (both copies); pilots state log seq 1 (M0/D1–D4)
Configuration Owners Identified: netplan (static eno1-only yaml) → systemd-networkd; systemd/logind owns sleep policy; kernel rfkill + systemd-rfkill (Load/Save) own radio-kill persistence; Ubuntu archive (noble-updates|security/restricted) owns NVIDIA packages; no NetworkManager installed; no second config plane found
Contradictions or Gaps:
  - GAP (known, non-blocking): corpus has no rfkill/suspend/ufw/NVIDIA runbook; profile §4 authority order applied (work order rank 1 → live host rank 4 → release-matched installed behavior rank 5). No corpus content authorized any mutation.
  - DRIFT (expected by packet, resolved live): as-found kernel 7.0.0-28 is no longer running; host rebooted 2026-08-25 15:09:55Z into 7.0.0-30 — see F-01. Packet said "re-verify live"; the live host is the authority.
  - No live/knowledge conflicts remaining.
Task May Proceed: YES
```

## 2. Authority and Target

- **AUTHORITY:** M1 commissioned by owner plan approval 2026-08-26 (state log seq 1). Exactly two authorized mutations (work order `owner_authorizations`): the four sleep-target masks and the rfkill Wi-Fi soft block (D4). NOT authorized: ufw enablement or any firewall change, installs/upgrades, kernel/driver/service changes, reboots.
- **FACT — identity verified before any probe** (evidence `00-identity`): `hostname` → `hxs-2`; `SSH_CONNECTION` → peer `192.168.50.201:22` from `192.168.50.204` (hxs-5); `eno1` → `192.168.50.201/24`, MAC `40:8d:5c:e7:90:d5`; system UUID `038d0240-045c-05e7-9006-e90700080009`; machine-id prefix `0c249b9a…` — UUID/MAC/machine-id all match the 2026-08-12 discovery record. `sudo -n true` → OK (NOPASSWD via `/etc/sudoers.d/90-hx-admin`, per pre-work record).
- **DECISION (D-record, disclosed):** no pre-existing `known_hosts` pin for 192.168.50.201 existed on hxs-5 (user and root stores checked via `ssh-keygen -F`). First connection used `StrictHostKeyChecking=accept-new` (TOFU) per owner-authorized work order directing this exact connection; the presented key was pinned for all subsequent session use and identity was immediately corroborated against the trusted discovery record (machine-id/UUID/MAC above). Presented host key: **ED25519 `SHA256:b2qlMQz496nUbuZKJu3wwmR0QY/EmN0KQtW4rM2HDcQ`** — recorded here so future hxs-2 tasks pin with `StrictHostKeyChecking=yes`. A key mismatch against this fingerprint must halt any future session.

## 3. Test and Recovery Plan (recorded before mutation)

| Test ID | Property | Procedure | Expected | Pass rule |
| --- | --- | --- | --- | --- |
| C-01 | hostname/IP/sudo identity | `hostname`, `ip -br addr`, `id`, `sudo -n true`, machine-id/UUID/MAC cross-check | hxs-2 / .201 / sudo OK / matches discovery | Exact match before probes |
| C-02 | kernel + OS | `os-release`, `uname`, `hostnamectl`, kernel package inventory | 24.04.4 noble; running kernel established live | State recorded; drift → finding |
| C-03 | Secure Boot state | `mokutil --sb-state` | Disabled (standing posture; never enable) | "SecureBoot disabled" |
| C-04 | driver bound + both GPUs | `nvidia-smi` ×2, `lspci -nnk`, `modinfo`, `lsmod` | 580.173.02, 2× RTX 5060 Ti, bound `nvidia` | All present; zero GPU processes required not, but recorded |
| C-05 | DKMS for running kernel | `dkms status`, package origins, holds, `dpkg --audit` | nvidia/580.173.02 built for the running kernel | Built for running kernel; archive-only origin |
| C-06 | storage layout + root free | `lsblk`, `df -hT/-i` | Root ext4 with D1 headroom | Root free space recorded (expect ~3.4 T) |
| C-07 | sleep masks (apply+verify) | pre-state → `systemctl mask sleep.target suspend.target hibernate.target suspend-then-hibernate.target` → 3-view verify | masked ×4; hybrid-sleep untouched | `is-enabled`=masked ×4 AND symlinks→/dev/null AND status view |
| C-08 | rfkill inventory + block + persistence | sysfs inventory → no-routes/no-sessions proof → block → state verify → systemd-rfkill save-state verify | wlan soft-blocked; save file = blocked | state=0/soft=1 held AND saved file = blocked AND units static/active |
| C-09 | network posture | `ip`, `netplan`, `resolvectl`, `ss -lntup`, `networkctl` | eno1 static; enp6s0+wlp5s0 DOWN; :22 + stub DNS only | State matches expectation; surprises → stop |
| C-10 | ufw inactive + staged doc | `ufw status verbose`, unit states, `nft list ruleset` | Inactive; ruleset empty; staged doc produced, never applied | Inactive confirmed; doc delivered |
| C-11 | failed units / wait-online / suspend svcs | `systemctl --failed`, wait-online status, suspend-unit inventory | No unexpected failures | Zero unexpected failed units |
| C-12 | NVRM/AER baseline + Xid | `journalctl -k` scans, all boots | Zero `NVRM: Xid`; AER baseline recorded | Xid count = 0 (stop condition otherwise) |
| C-13 | swap + memory | `free -h`, `swapon --show` | 62 Gi RAM, 8 Gi swap present | State recorded |

Recovery plan (pre-authorized inverses, from the work order):
- rfkill inverse: `echo 1 | sudo tee /sys/class/rfkill/rfkill1/state` (restores unblocked; systemd-rfkill then saves unblocked).
- mask inverse: `sudo systemctl unmask sleep.target suspend.target hibernate.target suspend-then-hibernate.target`.
- Rollback trigger: any failed C-07/C-08 post-check or regression check. Pre-change state captured (§4 before-artifacts: all four targets `static`, no symlinks; rfkill1 `state=1 soft=0 hard=0`; save file existed since 2026-08-12).
- Access risk: none (no SSH/network/PAM/sudo/storage touch). Restart/reboot impact: none either direction.

## 4. Implementation — the two bounded changes

### 4.1 Mutation A — sleep-target masks (C-07)

**FACT — before (03:26:41Z):** all five sleep-family targets `static`; no mask symlinks under `/etc/systemd/system/` (only stock `*.target.wants` dirs); `sleep.conf` and `logind.conf` all defaults.

**FACT — mutation (03:28:25Z):**

```bash
sudo -n systemctl mask sleep.target suspend.target hibernate.target suspend-then-hibernate.target   # exit 0
# Created symlink /etc/systemd/system/{sleep,suspend,hibernate,suspend-then-hibernate}.target → /dev/null  (×4)
```

**FACT — after:** `is-enabled` → `masked` ×4; `ls -la` → four `/dev/null` symlinks (root root); `systemctl status sleep.target` → `Loaded: masked (Reason: Unit sleep.target is masked.)`. `hybrid-sleep.target` remains `static` — deliberately untouched: it is **not** in the authorized set for hxs-2 (note: the hxs-1 mask set differed — it masked hybrid-sleep and left `sleep.target`; this work order authorizes `sleep.target` and not `hybrid-sleep.target`; followed exactly).

**FACT — diff-equivalent artifact (complete filesystem change):**

```text
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/sleep.target -> /dev/null
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/suspend.target -> /dev/null
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/hibernate.target -> /dev/null
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/suspend-then-hibernate.target -> /dev/null
```

### 4.2 Mutation B — rfkill Wi-Fi soft block (C-08, D4)

**FACT — interface identity:** `/sys/class/rfkill/rfkill1` = `phy0`, `type=wlan` ↔ `wlp5s0` (MAC `58:91:cf:e7:8a:38`, matches discovery). `rfkill0` = `hci0` bluetooth — explicitly out of scope, untouched.

**FACT — no routes/sessions proven FIRST (03:27:15Z, re-proven at execution 03:28:48Z):** `wlp5s0` state DOWN, `qdisc noop`, **no IP addresses**; `ip route show table all | grep -c wlp5s0` → **0**; established sessions → exactly one: my own SSH (`192.168.50.201:22` ← `192.168.50.204`); netplan contains no wifi stanza; NetworkManager not installed; `wpa_supplicant` active/enabled but with no configured network, no IP, no routes (observation F-07 — not touched; service changes not authorized).

**FACT — mechanism note (F-03):** the `rfkill(8)` userspace binary is **absent** on hxs-2 (not at `/usr/sbin/rfkill`; PATH verified). The kernel sysfs interface is therefore the block mechanism — the same file the work order's rollback line blesses: `/sys/class/rfkill/rfkill1/state` (1=unblocked, 0=soft-blocked).

**FACT — block (03:28:48Z):**

```bash
echo 0 | sudo -n tee /sys/class/rfkill/rfkill1/state    # exit 0
# pre:  state=1 soft=0 hard=0      post: state=0 soft=1 hard=0
```

**FACT — persistence mechanism verified (systemd-rfkill):** `systemd-rfkill.socket` static + active(listening); the block event triggered `systemd-rfkill.service` at 03:28:48 (journal), which re-created the save-state file at service completion 03:28:53:

```text
/var/lib/systemd/rfkill/pci-0000:05:00.0:wlan  →  content "1"   (Birth 2026-08-26 03:28:53.156Z)
```

**INFERENCE — save-file encoding proven:** the file stores the kernel rfkill **soft** flag (`1` = soft-blocked). Proof by the untouched control pair: bluetooth live `soft=0` ↔ saved `0`; wlan live `soft=1` ↔ saved `1`. The service runs at every boot (journal: 8 boots retained, service ran in each) and restores saved state at device appearance — so the soft block **will be re-applied across reboots by the already-installed mechanism**. Honest caveat (same as hxs-1 M2): boot-persistence is proven by mechanism + saved-state content, not by an observed reboot — reboots are not authorized at M1.

**FACT — held:** live state re-read 03:32:01Z and 03:32:43Z (independent session): `state=0 soft=1`, saved `1`, `wlp5s0` DOWN, 0 routes.

## 5. Regression and access preservation

**FACT (03:32:23Z):** `systemctl --failed` → 0 units (unchanged); `nvidia-smi -L` → both GPU UUIDs; uptime 12:22 continuous (no reboot); listeners unchanged (`0.0.0.0:22`, `[::]:22`, loopback stub DNS `127.0.0.53/54:53` only); `eno1` unchanged; masks ×4 held; rfkill block held; 0 routes on `wlp5s0`.

**FACT (03:32:43Z):** second independent SSH session authenticated post-mutation and observed `masked` ×4 + wlan `state=0 soft=1 saved=1`. Every session in this task was an independent fresh connection (no control-master reuse); password auth worked first attempt every time — the password-failure stop condition was never approached.

## 6. Driver / DKMS re-proof (C-04, C-05)

- **FACT:** `nvidia-smi` 580.173.02, CUDA 13.0. GPU0 `00000000:02:00.0` and GPU1 `00000000:03:00.0`, both **NVIDIA GeForce RTX 5060 Ti**, 16311 MiB each (32622 total), P0, 0 MiB used, no processes; idle 43 °C / 42 °C; power 180 W cap both. UUIDs: `GPU-7a7239a3-08d5-6c44-b847-2118ce93b53c`, `GPU-cdfbf3f2-f38a-8927-41f9-c8dcbd278249`.
- **FACT:** `lspci -nnk` — both VGA functions `Kernel driver in use: nvidia` (MSI 1462:5351 both). Modules loaded: `nvidia`, `nvidia_modeset`, `nvidia_drm`, `nvidia_uvm`; `nouveau` absent from `lsmod`. `modinfo nvidia`: version 580.173.02, Dual MIT/GPL.
- **FACT:** `dkms status` → `nvidia/580.173.02` **installed for 7.0.0-30-generic (running)** and `7.0.0-28-generic`. Finding F-02: not built for `7.0.0-29-generic` (superseded intermediate image; GRUB default boots the newest, -30; impact only if -29 were ever manually selected → recorded, no action authorized).
- **FACT — package plane:** full `nvidia-*-580-server(-open)` set at `580.173.02-0ubuntu0.24.04.1`; `nvidia-driver-580-server-open` installed == candidate, origins **only** `archive.ubuntu.com noble-updates/restricted` + `security.ubuntu.com noble-security/restricted`; `apt-mark showhold` empty; `dpkg --audit` clean; `dkms 3.0.11-1ubuntu13`.
- **FACT (F-01, kernel drift):** running kernel is `7.0.0-30-generic` (`#30~24.04.1-Ubuntu SMP Fri Aug 7 13:27:52 UTC 2 2026`), **not** 7.0.0-28 as the as-found record stated — the packet anticipated this ("re-verify live"). `linux-image-generic-hwe-24.04` installed == candidate `7.0.0-30.30~24.04.1` (noble-updates + noble-security). Images installed: -28, -29, -30 (rollback kernels present). Host rebooted into -30 on 2026-08-25 15:09:55Z (current boot `0e15ba2f…`; journal retains 8 boots). The driver/DKMS/GPU stack is **live-proven on the running kernel** — all GPU evidence in §6 was produced on 7.0.0-30.
- **FACT (record-only per packet):** routine upgradable packages exist (byobu, console-setup, curl, krb5-locales, …). No installs/upgrades authorized or performed.

## 7. Baseline health (C-01…C-03, C-06, C-09…C-13)

- **C-02 OS/kernel:** Ubuntu 24.04.4 LTS noble, x86-64; firmware F22 (2016-06-13). PASS.
- **C-03 Secure Boot:** `mokutil --sb-state` → `SecureBoot disabled`, `Platform is in Setup Mode`. Standing posture intact; not touched (owner directive: never enable). PASS.
- **C-06 storage:** `nvme0n1p2` ext4 `/` 3.6 T total, 14 G used, **3.4 T free (1 %)**, inodes 1 %; `nvme0n1p1` vfat `/boot/efi` (6.2 M used); `sda`/`sdb` 596.2 G each unpartitioned/unmounted (idle). D1 model-store headroom is capacity-trivial. PASS.
- **C-09 network:** netplan static `eno1` only (`192.168.50.201/24`, gw+DNS `192.168.50.1`); `enp6s0` off/unmanaged; `wlp5s0` off; routes only via `eno1`; resolved stub `127.0.0.53/54` → upstream `192.168.50.1`; listeners `:22` + loopback DNS only — no unexpected exposure (stop condition not triggered). PASS.
- **C-10 firewall:** `ufw status` → **inactive**; `ufw` unit disabled/inactive; `nftables` disabled/inactive; `nft list ruleset` empty. Staged ruleset in §8 — document only, **never applied**. PASS.
- **C-11 units:** `systemctl --failed` → **0** (contrast hxs-1's wait-online failure — hxs-2 is clean); `systemd-networkd-wait-online.service` enabled, `active (exited)`, both ExecStarts `status=0/SUCCESS` this boot; suspend-family services inventoried (`systemd-suspend`, `systemd-hibernate`, `systemd-hybrid-sleep`, `systemd-suspend-then-hibernate`, `systemd-hibernate-resume`, `nvidia-suspend`, `nvidia-hibernate` — all `inactive dead`; their entry-point targets are now masked per §4.1, `hybrid-sleep.target` excepted). PASS.
- **C-12 NVRM/AER/Xid:** **`NVRM: Xid` count = 0 across all 8 retained boots** (strict pattern — avoids the r8169 `XID` false-positive class noted in hxs-1 M2). NVRM lines are only the normal load banner (2026-08-25 15:09:55) and `kbifInitLtr_GB202: LTR is disabled in the hierarchy` (known benign: 2016 X99 chipset lacks PCIe LTR; fires on `nvidia-smi` queries). AER: exactly 3 lines, all `pcieport … AER: enabled with IRQ N` boot-time capability messages — **zero correctable, zero uncorrectable** errors (contrast hxs-1's Wi-Fi-port RxErr noise — not present here). PASS.
- **C-13 swap/memory:** 62 Gi RAM (1.1 Gi used, 61 Gi available, load 0.00); swap `/swap.img` 8.0 Gi file, 0 B used, priority -1. PASS.

## 8. Staged ufw ruleset — DOCUMENT ONLY (C-10; enablement deferred to M8 per D2)

**AUTHORITY:** D2 endpoint scope = `192.168.50.0/24` (owner chose the /24 over an hxs-5-only scope; the LAN is the authorized HX boundary — state log seq 1). **This document was never applied.** No `ufw` command beyond read-only `status` was run.

```text
# STAGED — hxs-2 CoderX boundary (M1 design; enable at M8 only, with refusal proof)
# Precondition at M8: re-verify ufw inactive, listeners as expected, and this document's diff against then-current exposure.
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 192.168.50.0/24 to any port 22 proto tcp comment 'HX LAN SSH (management)'
sudo ufw allow from 192.168.50.0/24 to any port 11434 proto tcp comment 'CoderX inference endpoint (D2 scope)'
# M8 gate (NOT authorized at M1): sudo ufw enable
# M8 verification (per state log seq 1): allow proof from a 192.168.50.0/24 peer on :11434
# and refusal proof from outside the /24 scope.
```

**INFERENCE:** enabling exactly this set changes nothing for current management access (SSH source 192.168.50.204 is inside the /24), but that is a statement about this ruleset, not authorization to apply it.

## 9. 13-point checklist — verdicts

| # | Check (context-packet enumeration) | Verdict | Basis |
| --- | --- | --- | --- |
| 1 | hostname/IP/sudo identity | **PASS** | §2 C-01: hxs-2, .201, sudo -n OK, machine-id/UUID/MAC match discovery |
| 2 | kernel + OS | **PASS (finding F-01)** | 24.04.4 noble; running kernel 7.0.0-30 (drift from as-found -28, packet-anticipated, DKMS-covered) |
| 3 | Secure Boot state | **PASS** | Disabled, Setup Mode; standing posture intact |
| 4 | driver bound + both GPUs in nvidia-smi | **PASS** | §6: 580.173.02, 2× RTX 5060 Ti @ 16311 MiB, bound `nvidia` |
| 5 | DKMS status for running kernel | **PASS (note F-02)** | Built for 7.0.0-30 (running) + 7.0.0-28; archive-only origin |
| 6 | storage layout + root free space | **PASS** | Root ext4 3.4 T free (1 %), inodes 1 %; SATA pair idle |
| 7 | sleep masks (apply, then verify) | **PASS** | §4.1: masked ×4 (authorized set), 3-view verify; hybrid-sleep untouched |
| 8 | rfkill inventory + Wi-Fi block + persistence | **PASS** | §4.2: rfkill1=phy0/wlp5s0; no routes/sessions proven first; state=0/soft=1 held; systemd-rfkill saved blocked state |
| 9 | network posture (eno1 config, secondary DOWN) | **PASS** | §7 C-09: static eno1; enp6s0/wlp5s0 DOWN; :22 + stub DNS only |
| 10 | ufw inactive + staged ruleset document | **PASS** | §7 C-10 + §8: inactive/empty; document staged, never applied |
| 11 | failed units + wait-online + suspend services | **PASS** | 0 failed; wait-online SUCCESS; suspend services inventoried, targets masked |
| 12 | NVRM/AER baseline + Xid count | **PASS** | Xid = 0 (8 boots); AER = 3 benign capability lines |
| 13 | swap + memory | **PASS** | 62 Gi RAM (61 Gi avail); /swap.img 8 Gi, 0 used |

**13 defined, 13 executed, 13 PASS; 0 FAIL, 0 BLOCKED, 0 NOT RUN.** One read-only probe retry (a `dpkg-query` format string was remote-shell-expanded and returned empty; re-run escaped — failure retained in evidence `03` vs `03b`). No correctable check required its one bounded correction.

## 10. Findings register

- **F-01 (drift, resolved):** kernel 7.0.0-28 → 7.0.0-30 since as-found; host rebooted 2026-08-25 15:09:55Z (plus two earlier same-day boots, owner-side activity). Driver stack live-proven on -30. No action.
- **F-02 (note):** DKMS not built for 7.0.0-29 (superseded intermediate). Only matters if -29 is ever manually booted. Record-only.
- **F-03 (mechanism):** `rfkill` binary absent on hxs-2; sysfs state file is the block/unblock mechanism (matches the work order's rollback line).
- **F-04 (proven semantics):** systemd-rfkill save file stores the kernel soft flag (1=blocked), proven by the bluetooth control pair; wlan save file re-created at block time with blocked state.
- **F-05 (D-record):** TOFU host-key pin — no prior pin existed; fingerprint recorded in §2 for future pinning.
- **F-06 (observation):** `wpa_supplicant` enabled+active with no configured network; rendered moot by the rfkill block; not touched (no service changes authorized). **RECOMMENDATION:** consider its formal disablement under a future authorized service change if D4 wants the Wi-Fi stack fully quiesced.
- **F-07 (record-only):** routine package upgrades pending (curl et al.); no installs authorized.
- **R-01 (risk, accepted-by-design):** boot-persistence of both mutations is proven by systemd semantics + saved state, not by an observed reboot (reboots not authorized at M1). First owner-approved reboot should include a post-boot spot check: `systemctl is-enabled` ×4 + `cat /sys/class/rfkill/rfkill1/state` (expect 0).

## 11. Rollback inverses (exact, ready)

```bash
# Inverse of Mutation B (rfkill block) — from the work order:
echo 1 | sudo tee /sys/class/rfkill/rfkill1/state
# verify: state=1 soft=0; systemd-rfkill will save "0" (unblocked) on its next trigger.

# Inverse of Mutation A (sleep masks):
sudo systemctl unmask sleep.target suspend.target hibernate.target suspend-then-hibernate.target
# verify: is-enabled → static ×4; symlinks gone. Pre-change state had no /etc/systemd/system/*.target entries.

# Staged ufw document: nothing to roll back — never applied.
```

No reboot is required in either direction for any inverse.

## 12. Evidence package

Raw sanitized captures were held transiently in `/tmp/.rick-m1-hxs2/evidence/` on hxs-5 (15 files: `00-identity` … `13-second-session`) and the load-bearing outputs are inlined in §2–§8 above; the workspace — including the askpass helper — is deleted at task end per the work order (no extracted credential copy ever existed; the helper read the credential-record table row at execution time only). This document is the complete retained M1 evidence. No secrets, hashes, tokens, or user data appear in retained evidence; the machine-id is prefix-masked; LAN addresses and the SSH host-key fingerprint (public by design) are shown deliberately.

**Sanitization disclosure (profile §11 honesty requirement):** during credential-file shape verification on hxs-5, one local `sed` mask was mis-scoped and the password value appeared once in the operator session transcript. It was never written to any file, evidence artifact, or this deliverable, and will never be repeated. The credential guide already mandates owner rotation of this plaintext-stored password (`ssh-info.md`, "Required owner security action"); this incident makes that rotation timely. Escalation note to Kimi-K3: recommend the owner execute the rotation at the next credential touch.

**Second Brain evaluation (standing directive):** (1) opportunity identified — yes; (2) pattern: hxs-1 OS-readiness checklist, second validated use on hxs-2; TKV server records as controlling sources applied from day one; (3) disposition: implemented — this checklist, the staged ufw design, and the rfkill-persistence semantics finding (F-04) become catalog content at handoff; (4) evidence: same readiness shape transfers across hosts; F-04 (save-file encoding, binary-absent mechanism) is a new reusable fact for the fleet spine. Deliverable goes to Carol for catalog receipt; handoff OPEN until the receipt is cited in the state log (per context packet `handoff`).

## 13. Validation summary (profile §12.5)

- **What changed:** (a) four sleep targets masked (`sleep`, `suspend`, `hibernate`, `suspend-then-hibernate` — the exact authorized set); (b) Wi-Fi rfkill1/phy0/wlp5s0 soft-blocked, with the systemd-rfkill saved state updated to blocked.
- **What did not change:** everything else — no reboot (uptime continuous through the session), no ufw/firewall change (staged document only), no installs/upgrades, no kernel/driver/DKMS/package changes, no service enable/disable/start/stop, no storage/network/sysctl/user changes; `hybrid-sleep.target` untouched; bluetooth rfkill0 untouched; Secure Boot still disabled.
- **Current target state:** ready at the OS plane for the CoderX backend per 13/13 checks; findings F-01/F-02/F-06 are records to manage, not readiness blockers.
- **Tests:** 13/13 PASS; regression and independent-session proofs PASS.
- **Access and recovery:** primary + independent sessions valid post-change; `sudo -n` path intact; inverses in §11 are immediate and reboot-free.
- **Persistence:** masks are persistent unit-file state; rfkill block is backed by systemd-rfkill saved state (`1` = blocked) restored at every boot — both proven by mechanism, not by an observed reboot (R-01).
- **Rollback readiness:** immediate, self-inverse pairs, pre-change state recorded.
- **Stop conditions:** none hit (no driver/GPU fault, no unexpected exposure, zero Xid, no identity mismatch, password auth first-try throughout).
- **Remaining decisions:** Carol catalog receipt (handoff gate); owner password rotation timing; F-06 wpa_supplicant disposition (future authorized change, if any).

`PASS — TASK COMPLETE`

```text
Task May Proceed: YES
```

## 14. Sequential command log (profile §12.4)

All remote commands executed as `hxsa@hxs-2` from `hxs-5` over independent SSH sessions (askpass auth, password read from the credential-record table at execution time, `NumberOfPasswordPrompts=1`); privileged probes via `sudo -n` (NOPASSWD). Times = host clock UTC. Local (hxs-5) rows marked.

| Seq | Timestamp | Command (summary) | Exit | Evidence |
| ---: | --- | --- | ---: | --- |
| 1 | 03:16–03:23 | Local: profile/work-order/packet/AGENTS reads; corpus tree + targeted searches; hxs-2 TKV records; hxs-1 pattern artifacts | 0 | §1 |
| 2 | 03:22 | Local: credential-row shape check (mis-scoped mask → disclosure incident, §12); shape re-verified fully masked | 0 | §12 |
| 3 | 03:23 | Local: `ssh-keygen -F` user+root known_hosts — no prior hxs-2 pin (TOFU decision, F-05) | 1 | §2 |
| 4 | 03:23 | Local: build `/tmp/.rick-m1-hxs2` (askpass helper + rssh runner, 0700); askpass shape test (non-empty only) | 0 | §12 |
| 5 | 03:23 | First SSH (accept-new TOFU): `hostname` → hxs-2; ED25519 key pinned | 0 | §2 |
| 6 | 03:24:11 | Identity: `hostname; id; SSH_CONNECTION; uptime; sudo -n true; machine-id(prefix); dmidecode UUID; eno1 link/addr` | 0 | §2 (C-01) |
| 7 | 03:24:35 | OS/kernel/SB: `os-release; uname; hostnamectl; mokutil --sb-state` | 0 | §7 (C-02/C-03), F-01 |
| 8 | 03:24:35 | Driver batch: `nvidia-smi` ×2; `lspci -nnk`; `modinfo`; `lsmod` | 0 | §6 (C-04) |
| 9 | 03:25:12 | DKMS/packages: `dkms status; dpkg-query (mangled → empty, retained); apt-mark; dpkg --audit; kernel policy; upgradable list` | 0 | §6 (C-05), F-07 |
| 10 | 03:25:45 | Re-run package inventory with escaped format string (correction of seq 9) | 0 | §6 |
| 11 | 03:26:13 | Storage/memory: `lsblk; df -hT/-i; free -h; swapon; /proc/swaps` | 0 | §7 (C-06/C-13) |
| 12 | 03:26:13 | Network: `ip addr/route(all tables); netplan; resolvectl; ss -lntup; networkctl` | 0 | §7 (C-09) |
| 13 | 03:26:41 | Firewall: `ufw status verbose; is-enabled/-active ufw+nftables; nft list ruleset` | 0 | §7 (C-10) |
| 14 | 03:26:41 | Units/sleep pre-state: `--failed`; wait-online; suspend-unit inventory; is-enabled ×5; `/etc/systemd` symlinks; sleep.conf/logind.conf | 0 | §4.1 (C-07 before), §7 (C-11) |
| 15 | 03:27:15 | NVRM/AER: journal NVRM/Xid (boot + all boots, strict pattern); AER scan; `--list-boots` | 0 | §7 (C-12) |
| 16 | 03:27:15 | rfkill pre-state: sysfs inventory; wlp5s0 identity; 0-routes proof; sessions proof; wifi managers; systemd-rfkill units; save-dir listing | 0 | §4.2 (C-08 before) |
| 17 | 03:28:02 | rfkill binary probe: `/usr/sbin/rfkill` absent (F-03) | 1 | §4.2 |
| 18 | 03:28:25 | **MUTATION A:** `sudo systemctl mask sleep.target suspend.target hibernate.target suspend-then-hibernate.target`; 3-view verify; hybrid-sleep untouched | 0 | §4.1 (C-07) |
| 19 | 03:28:48 | **MUTATION B:** preconditions re-proven; `echo 0 \| sudo tee /sys/class/rfkill/rfkill1/state`; post state/soft/hard; save-dir; service status | 0 | §4.2 (C-08) |
| 20 | 03:30:26 | Persistence detail: `stat` save file (Birth 03:28:53); content; rfkill journal this/all boots | 0 | §4.2, F-04 |
| 21 | 03:32:01 | Live re-read: wlan state=0/soft=1; bt control pair; saved contents; link states | 0 | §4.2 |
| 22 | 03:32:23 | Regression: `--failed`; `nvidia-smi -L`; uptime; listeners; addr; masks ×4; rfkill held; routes | 0 | §5 |
| 23 | 03:32:43 | Independent second session: identity + masked ×4 + wlan state/saved | 0 | §5 |
| 24 | ~03:33+ | Local: write `04-rick-hxs2-os-readiness.md`; delete `/tmp/.rick-m1-hxs2` (helper + evidence) | — | §12 |

Signed: **rick** — Expert Ubuntu Server Engineer, session `rick-m1-20260826-01`, 2026-08-26T03:33Z (UTC).
