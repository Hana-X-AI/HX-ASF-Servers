# Rick — M1 hxs-3 OS Readiness Report

`[TASK COMPLETE — EVIDENCE ATTACHED]`

| Field | Value |
| --- | --- |
| Agent | Rick — Expert Ubuntu Server Engineer |
| Session | `rick-m1-20260826-01` |
| Work order | `WO-HXS3-RICK-M1-001` (`02-work-order-rick-m1.yaml`) |
| Context packet | `03-context-packet-rick-m1.yaml` (goal `GOAL-HXS3-MUSE-001` v1) |
| Pilot | `PILOT-HXS3-MUSE-GLIMMER-TOOLING-001` |
| Target | `hxs-3` (192.168.50.202), Ubuntu 24.04.4 LTS (noble), kernel **7.0.0-30-generic** (live-verified; drifted from as-found -28, see F-01), x86-64 |
| Executed from | `hxs-5` (192.168.50.204) via SSH `hxsa@192.168.50.202` (askpass pattern; secret read from the credential-record table at execution time only, never printed/logged/stored; helper deleted at task end) |
| Window (host clock, UTC) | 2026-08-26T04:58:32Z → 2026-08-26T05:04:24Z |
| Owner decisions applied | D1 (model store = root ext4), D2 (fleet /24, NO host firewall — verify none exists, never create), D3 (muse-glimmer:30b — no OS-plane action), D4 (Wi-Fi rfkill soft block formalized); standing: Secure Boot stays disabled |
| Mutations performed | Exactly two: (a) `systemctl mask` of **suspend / hibernate / hybrid-sleep / suspend-then-hibernate** targets (the blueprint set — hybrid-sleep IS in; the hxs-2 variant was NOT used); (b) rfkill soft block of the Wi-Fi device. No reboot. No other change of any kind. |

Evidence labels: **FACT** (live host output), **AUTHORITY** (owner decision / work order / governance), **INFERENCE** (engineering conclusion), **RECOMMENDATION** (not executed).

---

## 1. Knowledge Review

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Source: /opt/tkv-local/ubuntu (ubuntu.com-main corpus) + /opt/tkv-local/servers/hxs-3/ (discovery.md, driver-results.md, pre-work-results.md — historical cross-check only)
Target Host/Scope: hxs-3 (192.168.50.202) — M1 OS readiness, 13-check enumeration, two authorized mutations per WO-HXS3-RICK-M1-001
Reviewed At: 2026-08-26T04:55Z→04:58Z (from hxs-5)
Relevant Files: 10+
  - /opt/tkv-local/ubuntu/ubuntu.com-main/releases.yaml (24.04 "noble", point release 24.04.4 — release-matching enforced)
  - Corpus-wide targeted searches: "rfkill"/"systemd-rfkill"/"suspend-then-hibernate" (0 hits) — same known gap as hxs-1 M1/M2, hxs-2 M1
  - /opt/tkv-local/servers/hxs-3/discovery.md (as-found 2026-08-12; machine-id d02a8e3a8d76474390e51a162e9f196d; eno1 MAC 40:8d:5c:e7:d0:e5; wlp5s0 MAC 58:91:cf:e7:53:74)
  - /opt/tkv-local/servers/hxs-3/driver-results.md, pre-work-results.md
  - servers/BLUEPRINT-llm-server.md §2 (suspend targets masked ×4; Wi-Fi rfkill soft block with systemd-rfkill persistence; Secure Boot disabled standing; root ext4 headroom)
  - pilots/PILOT-HXS2-CODERX-BACKEND-001/04-rick-hxs2-os-readiness.md (checklist shape; hxs-2 variant differences noted)
  - goals/2026-08-26-hxs3-muse-glimmer-tooling.md (D1–D8); pilots/.../01-state-log.md seq 1–2 (M0; PCIe x8 caveat; PNY card partner)
  - agents/rick/profile.md (startup §5, lifecycle §6, test-first §7, sanitization §11, escalation §14)
  - HX-ASF-Servers/AGENTS.md (owner posture: no host firewalls anywhere; Secure Boot stays disabled; communication contract)
Ubuntu Release/Kernel Identified: Ubuntu 24.04.4 LTS (noble); running kernel established live as 7.0.0-30-generic (HWE; installed == archive candidate 7.0.0-30.30~24.04.1); dkms 3.0.11-1ubuntu13
Applicable Authority/Runbooks/Tests: work order (two authorized mutations; stop conditions); context packet (13-check enumeration; evidence requirements); blueprint §2 (mask set; rfkill persistence); state log seq 1 (M0/D-items)
Configuration Owners Identified: netplan (static eno1-only yaml) → systemd-networkd; systemd/logind owns sleep policy; kernel rfkill + systemd-rfkill (Load/Save) own radio-kill persistence; Ubuntu archive (noble-updates|security/restricted) owns NVIDIA packages; no NetworkManager active; no second config plane found
Contradictions or Gaps:
  - GAP (known, non-blocking): corpus has no rfkill/suspend runbook; profile §4 authority order applied (work order rank 1 → live host rank 4 → release-matched installed behavior rank 5). No corpus content authorized any mutation.
  - DRIFT (expected by packet, resolved live): as-found kernel 7.0.0-28 is no longer running; host rebooted 2026-08-25 16:23 UTC into 7.0.0-30 — see F-01. Packet said "re-verify live"; the live host is the authority.
  - DRIFT (record-only): timezone Etc/UTC → America/Panama since discovery — see F-08.
  - No live/knowledge conflicts remaining.
Task May Proceed: YES
```

## 2. Authority and Target

- **AUTHORITY:** M1 commissioned by owner plan approval 2026-08-26 (state log seq 1). Exactly two authorized mutation classes (work order `owner_authorizations`): the four named blueprint sleep-target masks (suspend.target, hibernate.target, hybrid-sleep.target, suspend-then-hibernate.target) and the rfkill Wi-Fi soft block (D4). NOT authorized: any firewall design or enablement (owner rule — none anywhere), package installs/upgrades, kernel/driver/service changes, reboots.
- **FACT — identity verified before any probe** (evidence `01-identity`): `hostname` → `hxs-3`; `SSH_CONNECTION` → peer `192.168.50.202:22` from `192.168.50.204` (hxs-5); `eno1` → `192.168.50.202/24`, MAC `40:8d:5c:e7:d0:e5`; machine-id `d02a8e3a8d76474390e51a162e9f196d` — machine-id/MAC/IP all match the 2026-08-12 discovery record. System UUID `038d0240-045c-05e7-d006-e70700080009` captured for the record (discovery did not record one). `sudo -n true` → OK (NOPASSWD via `/etc/sudoers.d/90-hx-admin`, per pre-work record).
- **DECISION (D-record, disclosed):** no pre-existing `known_hosts` pin for 192.168.50.202 existed on hxs-5 (user store checked via `ssh-keygen -F`, exit 1; root store absent). First connection used `StrictHostKeyChecking=accept-new` (TOFU) per owner-authorized work order directing this exact connection; the presented key was pinned for all subsequent session use (`StrictHostKeyChecking=yes`) and identity was immediately corroborated against the trusted discovery record (machine-id/MAC above). Presented host key: **ED25519 `SHA256:R/3mdfv7J0Fajo8yryT7JB6B4EoBm47W2rLX+siHEog`** — recorded here so future hxs-3 tasks pin with `StrictHostKeyChecking=yes`. A key mismatch against this fingerprint must halt any future session.

## 3. Test and Recovery Plan (recorded before mutation)

| Test ID | Property | Procedure | Expected | Pass rule |
| --- | --- | --- | --- | --- |
| C-01 | hostname/IP/sudo identity | `hostname`, `ip -br addr`, `id`, `sudo -n true`, machine-id/MAC cross-check | hxs-3 / .202 / sudo OK / matches discovery | Exact match before probes |
| C-02 | kernel + OS | `os-release`, `uname`, `hostnamectl`, `timedatectl`, kernel package inventory | 24.04.4 noble; running kernel established live | State recorded; drift → finding |
| C-03 | Secure Boot state | `mokutil --sb-state` | Disabled (standing posture; never enable) | "SecureBoot disabled" |
| C-04 | driver bound + both GPUs | `nvidia-smi` ×2, `lspci -nnk`, `modinfo`, `lsmod` | 580.173.02, 2× RTX 5060 Ti, bound `nvidia` | All present; processes recorded |
| C-05 | DKMS for running kernel | `dkms status`, package origins, holds, `dpkg --audit` | nvidia/580.173.02 built for the running kernel | Built for running kernel; archive-only origin |
| C-06 | storage layout + root free | `lsblk`, `df -hT/-i` | Root ext4 with ~18 GB artifact headroom | Root free space recorded (expect ~3.4 T) |
| C-07 | sleep masks (apply+verify) | pre-state → `systemctl mask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target` → 3-view verify | masked ×4; sleep.target untouched | `is-enabled`=masked ×4 AND symlinks→/dev/null AND status view |
| C-08 | rfkill inventory + block + persistence | sysfs inventory → identity → no-routes/no-sessions proof → block → state verify → systemd-rfkill save-state verify | wlan soft-blocked; save file = blocked | state=0/soft=1 held AND saved file = blocked AND units static/active |
| C-09 | network posture | `ip`, `netplan get`, `resolvectl`, `ss -lntup` | eno1 static; enp6s0+wlp5s0 DOWN; :22 + stub DNS only | State matches expectation; surprises → stop |
| C-10 | no firewall present (owner rule) | `ufw status verbose`, unit states, `nft list ruleset`, `iptables -S`, package inventory | No firewall active anywhere; rulesets empty; never create | Absence verified on all three managers |
| C-11 | failed units / wait-online / suspend svcs | `systemctl --failed`, wait-online status, suspend-unit inventory | No unexpected failures | Zero unexpected failed units |
| C-12 | NVRM/AER baseline + Xid | `journalctl -k` scans, all boots | Zero `NVRM: Xid`; AER baseline recorded | Xid count = 0 (stop condition otherwise) |
| C-13 | swap + memory | `free -h`, `swapon --show`, `/proc/swaps` | 62 Gi RAM, 8 Gi swap present | State recorded |

Recovery plan (pre-authorized inverses, from the work order):
- rfkill inverse: `echo 1 | sudo tee /sys/class/rfkill/rfkill1/state` (restores unblocked; systemd-rfkill then saves unblocked).
- mask inverse: `sudo systemctl unmask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target`.
- Rollback trigger: any failed C-07/C-08 post-check or regression check. Pre-change state captured (§4 before-artifacts: all five sleep-family targets `static`, no mask symlinks; rfkill1 `state=1 soft=0 hard=0`; wlan save file existed since 2026-08-12 with content `0`).
- Access risk: none (no SSH/network/PAM/sudo/storage touch). Restart/reboot impact: none either direction.

## 4. Implementation — the two bounded changes

### 4.1 Mutation A — blueprint sleep-target masks (C-07)

**FACT — before (05:02Z):** all five sleep-family targets `static`; no mask symlinks under `/etc/systemd/system/` (only stock `*.target.wants` dirs); `logind.conf` and `sleep.conf` all defaults (section headers only).

**FACT — mutation (05:03Z):**

```bash
sudo -n systemctl mask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target   # exit 0
# Created symlink /etc/systemd/system/{suspend,hibernate,hybrid-sleep,suspend-then-hibernate}.target → /dev/null  (×4)
```

**FACT — after:** `is-enabled` → `masked` ×4 (suspend, hibernate, hybrid-sleep, suspend-then-hibernate); `ls -la` → four `/dev/null` symlinks (root root); `systemctl status` views → `Loaded: masked (Reason: Unit ... is masked.)`. `sleep.target` remains `static` — deliberately untouched: it is **not** in the blueprint set. Note the set difference from hxs-2: hxs-2's work order authorized `sleep.target` and not `hybrid-sleep.target`; this work order authorizes the proven hxs-1/blueprint set — `hybrid-sleep.target` IS masked here and `sleep.target` is not. Followed exactly.

**FACT — diff-equivalent artifact (complete filesystem change):**

```text
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/suspend.target -> /dev/null
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/hibernate.target -> /dev/null
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/hybrid-sleep.target -> /dev/null
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/suspend-then-hibernate.target -> /dev/null
```

### 4.2 Mutation B — rfkill Wi-Fi soft block (C-08, D4)

**FACT — interface identity:** `/sys/class/rfkill/rfkill1` = `phy0`, `type=wlan`, at PCI `0000:05:00.0` ↔ `wlp5s0` (`/sys/class/net/wlp5s0/phy80211` → `phy0`; MAC `58:91:cf:e7:53:74`, matches discovery). `rfkill0` = `hci0` bluetooth — explicitly out of scope, untouched.

**FACT — no routes/sessions proven FIRST (05:02Z, re-proven at execution 05:03:35Z):** `wlp5s0` state DOWN; **0 IP addresses**; `ip route show table all | grep -c wlp5s0` → **0**; sessions on wlp5s0 → **0**; established sessions host-wide → exactly one: my own SSH (`192.168.50.202:22` ← `192.168.50.204`); netplan contains no wifi stanza; NetworkManager inactive; `wpa_supplicant` active/enabled but with no configured network, no IP, no routes (observation F-06 — not touched; service changes not authorized).

**FACT — mechanism note (F-03):** the `rfkill(8)` userspace binary is **absent** on hxs-3 (not at `/usr/sbin/rfkill`; `command -v` verified) — same as hxs-2. The kernel sysfs interface is therefore the block mechanism — the same file the work order's rollback line blesses: `/sys/class/rfkill/rfkill1/state` (1=unblocked, 0=soft-blocked).

**FACT — block (05:03:35Z):**

```bash
echo 0 | sudo -n tee /sys/class/rfkill/rfkill1/state    # exit 0
# pre:  state=1 soft=0 hard=0      post: state=0 soft=1 hard=0
```

**FACT — persistence mechanism verified (systemd-rfkill):** `systemd-rfkill.socket` static + active(listening) since boot; the block event triggered `systemd-rfkill.service` at 00:03:35 EST (05:03:35Z; journal), which completed ("Deactivated successfully") at 00:03:40 EST, re-creating the save-state file:

```text
/var/lib/systemd/rfkill/pci-0000:05:00.0:wlan  →  content "1"   (mtime 2026-08-26 00:03:40.917 EST)
```

**INFERENCE — save-file encoding confirmed:** the file stores the kernel rfkill **soft** flag (`1` = soft-blocked), confirmed by the untouched control pair: bluetooth live `soft=0` ↔ saved `0`; wlan live `soft=1` ↔ saved `1` (same semantics proven on hxs-2). The service has run 13 times across the journal (every retained boot plus events) and restores saved state at device appearance — so the soft block **will be re-applied across reboots by the already-installed mechanism**. Honest caveat (same as hxs-1 M2 / hxs-2 M1): boot-persistence is proven by mechanism + saved-state content, not by an observed reboot — reboots are not authorized at M1.

**FACT — held:** live state re-read 05:04:07Z and 05:04:24Z (independent session): `state=0 soft=1`, saved `1`, `wlp5s0` DOWN, 0 routes.

## 5. Regression and access preservation

**FACT (05:04:07Z):** `systemctl --failed` → 0 units (unchanged); `nvidia-smi -L` → both GPU UUIDs; uptime 12:40 continuous since 2026-08-25 11:23:26 EST (no reboot); listeners unchanged (`0.0.0.0:22`, `[::]:22`, loopback stub DNS `127.0.0.53/54:53` only); masks ×4 held; rfkill block held; 0 routes on `wlp5s0`.

**FACT (05:04:24Z):** second independent SSH session authenticated post-mutation (fresh connection, source port 45516) and observed `masked` ×4 + wlan `state=0 soft=1 saved=1` + `sudo -n` OK. Every session in this task was an independent fresh connection (no control-master reuse); password auth worked first attempt every time — the password-failure stop condition was never approached.

## 6. Driver / DKMS re-proof (C-04, C-05)

- **FACT:** `nvidia-smi` 580.173.02, CUDA 13.0. GPU0 `00000000:02:00.0` and GPU1 `00000000:03:00.0`, both **NVIDIA GeForce RTX 5060 Ti**, 16311 MiB each (32622 total), P0, 0 MiB used, no processes; idle 38 °C / 39 °C; power 180 W cap both. UUIDs: `GPU-3cb368de-b2ea-c6ab-57d1-8d6298831f90`, `GPU-73cb422b-80d9-f53d-c8b7-45dbb32cbea1`.
- **FACT:** `lspci -nnk` — both VGA functions `Kernel driver in use: nvidia` (PNY 196e:143e both, per discovery). Modules loaded: `nvidia`, `nvidia_modeset`, `nvidia_drm`, `nvidia_uvm`; `nouveau` absent from `lsmod`. `modinfo nvidia`: version 580.173.02, Dual MIT/GPL.
- **FACT:** `dkms status` → `nvidia/580.173.02` **installed for 7.0.0-30-generic (running)** and `7.0.0-28-generic`. Finding F-02: not built for `7.0.0-29-generic` (superseded intermediate image; GRUB default boots the newest, -30; impact only if -29 were ever manually selected → recorded, no action authorized).
- **FACT — package plane:** full `nvidia-*-580-server(-open)` set at `580.173.02-0ubuntu0.24.04.1`; `nvidia-driver-580-server-open` installed == candidate, origins **only** `archive.ubuntu.com noble-updates/restricted` + `security.ubuntu.com noble-security/restricted`; `apt-mark showhold` empty; `dpkg --audit` clean; `dkms 3.0.11-1ubuntu13`.
- **FACT (F-01, kernel drift):** running kernel is `7.0.0-30-generic` (`#30~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Aug 7 13:27:52 UTC 2 2026`), **not** 7.0.0-28 as the as-found record stated — the packet anticipated this ("re-verify live"; hxs-2 drifted identically in the same outage window). `linux-image-generic-hwe-24.04` installed == candidate `7.0.0-30.30~24.04.1` (noble-updates + noble-security). Images installed: -28, -29, -30 (rollback kernels present). Host rebooted into -30 on 2026-08-25 11:23:26–35 EST = 16:23 UTC (current boot `c36565db…`; journal retains 8 boots). The driver/DKMS/GPU stack is **live-proven on the running kernel** — all GPU evidence in §6 was produced on 7.0.0-30.
- **FACT (record-only per packet):** routine upgradable packages exist (byobu, console-setup, krb5 set, openssl/libssl3t64, snapd, vim-common, …). No installs/upgrades authorized or performed.

## 7. Baseline health (C-01…C-03, C-06, C-09…C-13)

- **C-02 OS/kernel:** Ubuntu 24.04.4 LTS noble, x86-64; firmware F22 (2016-06-13). PASS (with F-01 kernel drift, F-08 timezone drift — both record-class).
- **C-03 Secure Boot:** `mokutil --sb-state` → `SecureBoot disabled`, `Platform is in Setup Mode`. Standing posture intact; not touched (owner directive: never enable). PASS.
- **C-06 storage:** `nvme0n1p2` ext4 `/` 3.6 T total, 14 G used, **3.4 T free (1 %)**, inodes 1 %; `nvme0n1p1` vfat `/boot/efi` (6.2 M used); `sda` 1.8 T SATA unpartitioned/unmounted (idle). D1 model-store headroom for the ~18 GB artifact is capacity-trivial. PASS.
- **C-09 network:** netplan static `eno1` only (`192.168.50.202/24`, gw+DNS `192.168.50.1`); `enp6s0` DOWN; `wlp5s0` DOWN; routes only via `eno1`/`lo`; resolved stub `127.0.0.53/54` → upstream `192.168.50.1`; listeners `:22` + loopback DNS only — no unexpected exposure (stop condition not triggered). PASS.
- **C-10 no firewall (owner rule — verify, never create):** `ufw status` → **inactive**, unit disabled/inactive; `nftables` unit disabled/inactive, `nft list ruleset` **empty**; `iptables -S` → default ACCEPT policies, **zero rules**; `firewalld` not installed. No firewall exists anywhere on the host; none was created or staged. PASS.
- **C-11 units:** `systemctl --failed` → **0**; `systemd-networkd-wait-online.service` enabled, `active (exited)`, both ExecStarts `status=0/SUCCESS` this boot; suspend-family services inventoried (`systemd-suspend`, `systemd-hibernate`, `systemd-hybrid-sleep`, `systemd-suspend-then-hibernate`, `systemd-hibernate-resume`, `nvidia-suspend`, `nvidia-hibernate`, `nvidia-resume` — all `inactive`); their entry-point targets are now masked per §4.1 (`sleep.target` excepted, per the authorized set). PASS.
- **C-12 NVRM/AER/Xid:** **`NVRM: Xid` count = 0 this boot and across all 8 retained boots** (strict pattern — avoids the `XID` false-positive class noted in hxs-1 M2). NVRM lines are only the normal load banner (2026-08-25 11:23:35 EST, 580.173.02) and `kbifInitLtr_GB202: LTR is disabled in the hierarchy` (known benign: 2016 X99 chipset lacks PCIe LTR; fires on `nvidia-smi` queries — my own C-04 queries triggered the 23:59 EST instances). AER: only boot-time capability messages (2× `_OSC … OS now controls [… AER …]`, 3× `pcieport … AER: enabled with IRQ N`) — **zero correctable, zero uncorrectable** errors. PASS.
- **C-13 swap/memory:** 62 Gi RAM (1.1 Gi used, 61 Gi available, load 0.00); swap `/swap.img` 8.0 Gi file, 0 B used, priority -1. PASS.

## 8. 13-point checklist — verdicts

| # | Check (context-packet enumeration) | Verdict | Basis |
| --- | --- | --- | --- |
| 1 | hostname/IP/sudo identity | **PASS** | §2 C-01: hxs-3, .202, sudo -n OK, machine-id/MAC match discovery |
| 2 | kernel + OS | **PASS (finding F-01)** | 24.04.4 noble; running kernel 7.0.0-30 (drift from as-found -28, packet-anticipated, DKMS-covered) |
| 3 | Secure Boot state | **PASS** | Disabled, Setup Mode; standing posture intact |
| 4 | driver bound + both GPUs in nvidia-smi | **PASS** | §6: 580.173.02, 2× RTX 5060 Ti @ 16311 MiB, bound `nvidia` |
| 5 | DKMS status for running kernel | **PASS (note F-02)** | Built for 7.0.0-30 (running) + 7.0.0-28; archive-only origin |
| 6 | storage layout + root free space | **PASS** | Root ext4 3.4 T free (1 %), inodes 1 %; ≥18 GB artifact trivial; SATA SSD idle |
| 7 | the FOUR blueprint masks applied + verified | **PASS** | §4.1: masked ×4 (exact blueprint set, hybrid-sleep included), 3-view verify; sleep.target untouched |
| 8 | rfkill inventory + Wi-Fi block + persistence mechanism | **PASS** | §4.2: rfkill1=phy0/wlp5s0 identity; no routes/sessions proven first; state=0/soft=1 held; systemd-rfkill saved blocked state |
| 9 | network posture | **PASS** | §7 C-09: static eno1; enp6s0/wlp5s0 DOWN; :22 + stub DNS only |
| 10 | no firewall (verify none exists — owner rule) | **PASS** | §7 C-10: ufw inactive, nftables empty/inactive, iptables zero rules, firewalld absent; nothing created |
| 11 | failed units + wait-online + suspend services | **PASS** | 0 failed; wait-online SUCCESS; suspend services inventoried, targets masked |
| 12 | NVRM/AER baseline + Xid count | **PASS** | Xid = 0 (8 boots); AER = benign capability lines only |
| 13 | swap + memory | **PASS** | 62 Gi RAM (61 Gi avail); /swap.img 8 Gi, 0 used |

**13 defined, 13 executed, 13 PASS; 0 FAIL, 0 BLOCKED, 0 NOT RUN.** No probe retries and no corrections were needed (the hxs-2 `dpkg-query` escaping lesson was pre-applied — all format strings ran escaped, first pass).

## 9. Findings register

- **F-01 (drift, resolved):** kernel 7.0.0-28 → 7.0.0-30 since as-found; host rebooted 2026-08-25 16:23 UTC (same outage window class as hxs-2). Driver stack live-proven on -30. No action.
- **F-02 (note):** DKMS not built for 7.0.0-29 (superseded intermediate). Only matters if -29 is ever manually booted. Record-only.
- **F-03 (mechanism):** `rfkill` binary absent on hxs-3 (second host confirmed); sysfs state file is the block/unblock mechanism (matches the work order's rollback line).
- **F-04 (confirmed semantics):** systemd-rfkill save file stores the kernel soft flag (1=blocked), confirmed by the bluetooth control pair; wlan save file re-created at block time with blocked state. Service ran 13 times across the journal (every boot).
- **F-05 (D-record):** TOFU host-key pin — no prior pin existed; fingerprint recorded in §2 for future pinning (`SHA256:R/3mdfv7J0Fajo8yryT7JB6B4EoBm47W2rLX+siHEog`).
- **F-06 (observation):** `wpa_supplicant` enabled+active with no configured network; rendered moot by the rfkill block; not touched (no service changes authorized). **RECOMMENDATION:** consider its formal disablement under a future authorized service change if D4 wants the Wi-Fi stack fully quiesced.
- **F-07 (record-only):** routine package upgrades pending (openssl, krb5, snapd et al.); no installs authorized.
- **F-08 (drift, record-only):** timezone changed from `Etc/UTC` (discovery 2026-08-12) to `America/Panama (EST, -0500)`; clock synchronized, NTP active, RTC in UTC. No readiness impact; recorded so future log timestamps are read correctly and the discovery record is understood as superseded on this point.
- **F-09 (record-only):** stale rfkill save file `/var/lib/systemd/rfkill/pci-0000:04:00.0:wlan` (content `0`, dated 2026-08-12) — no device currently exists at PCI 04:00.0; harmless leftover from an earlier configuration; untouched (not in scope).
- **R-01 (risk, accepted-by-design):** boot-persistence of both mutations is proven by systemd semantics + saved state, not by an observed reboot (reboots not authorized at M1; D6 pre-approves the M8 cold-reboot cycles). First reboot should include a post-boot spot check: `systemctl is-enabled suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target` (expect masked ×4) + `cat /sys/class/rfkill/rfkill1/state` (expect 0).

## 10. Rollback inverses (exact, ready)

```bash
# Inverse of Mutation B (rfkill block) — from the work order:
echo 1 | sudo tee /sys/class/rfkill/rfkill1/state
# verify: state=1 soft=0; systemd-rfkill will save "0" (unblocked) on its next trigger.

# Inverse of Mutation A (sleep masks — exact blueprint set):
sudo systemctl unmask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target
# verify: is-enabled → static ×4; symlinks gone. Pre-change state had no /etc/systemd/system/*.target mask entries.

# Firewall: nothing to roll back — none exists and none was created (owner rule).
```

No reboot is required in either direction for any inverse.

## 11. Evidence package

Raw sanitized captures were held transiently in `/tmp/.rick-m1-hxs3/evidence/` on hxs-5 (9 files: `00-tofu-first-connect` … `14-second-session`) and the determinative outputs are inlined in §2–§7 above; the workspace — including the askpass helper — is deleted at task end per the work order (no extracted credential copy ever existed; the helper read the credential-record table row at execution time only). This document is the complete retained M1 evidence. No secrets, secret-derived hashes, tokens, or user data appear in retained evidence; the SSH host-key SHA-256 **fingerprint is intentionally retained** — it is a public host key, by design non-secret, and is not a credential-derived hash; LAN addresses are shown deliberately; the machine-id is shown because the work order's identity-corroboration requirement makes it the evidence.

**Sanitization disclosure (profile §11 honesty requirement):** the credential-row shape check on hxs-5 was performed with an `awk` field probe returning field count and a masked label only; the value was never printed, logged, written to any file, or repeated — no disclosure incident occurred in this session (the hxs-2 M1 mis-scoped-mask lesson was pre-applied). The credential guide's standing owner-rotation advice from the hxs-2 incident remains the owner's call and is unchanged by this session. *(Corrected 2026-08-26 per review finding: a credential-derived `value_len` metric was removed from this paragraph — masked-value metrics of the secret do not belong in retained evidence even without the value; it was also inaccurate. The "no hashes" claim above was corrected the same day to distinguish the intentionally retained public SSH host-key fingerprint from secret-derived hashes. Remaining content unchanged.)*

**Second Brain evaluation (standing directive):** (1) opportunity identified — yes; (2) pattern: OS-readiness checklist, **third validated host use** (hxs-1 → hxs-2 → hxs-3); blueprint mask set applied uniformly for the first time (hybrid-sleep included from the start); (3) disposition: implemented — this checklist, F-03 (binary-absent sysfs mechanism now confirmed on two hosts), F-04 (save-file encoding), and the F-05 pin become catalog content at handoff; (4) evidence: 13/13 PASS with the uniform blueprint set — the blueprint's uniformity claim holds on the third host; the only drift found (kernel, timezone) is record-class, not readiness-blocking. Deliverable goes to Carol for catalog receipt; handoff OPEN until the receipt is cited in the state log (per context packet `handoff`).

## 12. Validation summary (profile §12.5)

- **What changed:** (a) four sleep targets masked (`suspend`, `hibernate`, `hybrid-sleep`, `suspend-then-hibernate` — the exact blueprint set); (b) Wi-Fi rfkill1/phy0/wlp5s0 soft-blocked, with the systemd-rfkill saved state updated to blocked (`1`).
- **What did not change:** everything else — no reboot (uptime continuous through the session), no firewall created/staged/touched (none exists, owner rule verified), no installs/upgrades, no kernel/driver/DKMS/package changes, no service enable/disable/start/stop, no storage/network/sysctl/user changes; `sleep.target` untouched; bluetooth rfkill0 untouched; Secure Boot still disabled; stale `pci-0000:04:00.0:wlan` save file untouched.
- **Current target state:** ready at the OS plane for the Muse Glimmer tooling backend per 13/13 checks; findings F-01/F-02/F-06/F-08/F-09 are records to manage, not readiness blockers.
- **Tests:** 13/13 PASS; regression and independent-session proofs PASS.
- **Access and recovery:** primary + independent sessions valid post-change; `sudo -n` path intact; inverses in §10 are immediate and reboot-free.
- **Persistence:** masks are persistent unit-file state; rfkill block is backed by systemd-rfkill saved state (`1` = blocked) restored at every boot — both proven by mechanism, not by an observed reboot (R-01).
- **Rollback readiness:** immediate, self-inverse pairs, pre-change state recorded.
- **Stop conditions:** none hit (no driver/GPU fault, no unexpected exposure, zero Xid, no identity mismatch, password auth first-try throughout).
- **Remaining decisions:** Carol catalog receipt (handoff gate); F-06 wpa_supplicant disposition (future authorized change, if any); F-08 timezone record noted for Carol's catalog.

`PASS — TASK COMPLETE`

```text
Task May Proceed: YES
```

## 13. Sequential command log (profile §12.4)

All remote commands executed as `hxsa@hxs-3` from `hxs-5` over independent SSH sessions (askpass auth, password read from the credential-record table at execution time, `NumberOfPasswordPrompts=1`); privileged probes via `sudo -n` (NOPASSWD). Times = host clock UTC (host local time is EST/-05:00, see F-08). Local (hxs-5) rows marked.

| Seq | Timestamp | Command (summary) | Exit | Evidence |
| ---: | --- | --- | ---: | --- |
| 1 | 04:54–04:58 | Local: profile/work-order/packet/AGENTS reads; corpus tree + targeted searches (0 hits); hxs-3 TKV records; blueprint §2; hxs-2 M1 doc; goal file; state log | 0 | §1 |
| 2 | 04:56 | Local: credential-row shape check — awk field-length probe, value never printed (`value_len=13`) | 0 | §11 |
| 3 | 04:58 | Local: `ssh-keygen -F` user known_hosts — no prior hxs-3 pin (exit 1); root store absent (TOFU decision, F-05) | 1 | §2 |
| 4 | 04:58 | Local: build `/tmp/.rick-m1-hxs3` (askpass helper + rssh runner, 0700); askpass shape test (non-empty only) | 0 | §11 |
| 5 | 04:58 | First SSH (accept-new TOFU): `hostname` → hxs-3; ED25519 key pinned; peer .202:22 ← .204 | 0 | §2 |
| 6 | 04:58:32 | Identity: `hostname; id; SSH_CONNECTION; sudo -n true; machine-id; dmidecode UUID; eno1 link/addr; uptime` | 0 | §2 (C-01) |
| 7 | 04:59:21 | OS/kernel/SB: `os-release; uname; hostnamectl; timedatectl; mokutil --sb-state; kernel image inventory; HWE meta policy` | 0 | §7 (C-02/C-03), F-01, F-08 |
| 8 | 04:59:45 | Driver batch: `nvidia-smi` ×2; `lspci -nnk`; `modinfo`; `lsmod` | 0 | §6 (C-04) |
| 9 | 05:00:30 | DKMS/packages: `dkms status; dpkg-query (escaped formats); apt-mark; dpkg --audit; driver pkg policy; upgradable list` | 0 | §6 (C-05), F-02, F-07 |
| 10 | 05:01:00 | Storage/memory: `lsblk; df -hT/-i; free -h; swapon; /proc/swaps` | 0 | §7 (C-06/C-13) |
| 11 | 05:01:30 | Network: `ip link/addr/route(all)/rule; netplan get; resolvectl; ss -lntup; ss established` | 0 | §7 (C-09) |
| 12 | 05:01:50 | Firewall absence: `ufw status verbose; is-enabled/-active ufw+nftables; nft list ruleset; iptables -S; pkg inventory` | 0 | §7 (C-10) |
| 13 | 05:02:10 | Units/sleep pre-state: `--failed`; wait-online; suspend-service inventory; is-enabled ×5; `/etc/systemd` symlinks; logind/sleep conf | 0 | §4.1 (C-07 before), §7 (C-11) |
| 14 | 05:02:30 | NVRM/AER: `--list-boots`; NVRM this boot; Xid strict counts (boot + all boots); AER scan + error counts | 0 | §7 (C-12) |
| 15 | 05:02:50 | rfkill pre-state: sysfs inventory; device links; wlp5s0 identity; 0-routes/0-addrs/0-sessions proof; wifi managers; systemd-rfkill units; save-dir contents | 0 | §4.2 (C-08 before) |
| 16 | 05:03:05 | **MUTATION A:** `sudo systemctl mask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target`; 3-view verify; sleep.target untouched | 0 | §4.1 (C-07) |
| 17 | 05:03:35 | **MUTATION B:** preconditions re-proven; `echo 0 \| sudo tee /sys/class/rfkill/rfkill1/state`; post state/soft/hard; bt control; rfkill journal; save-dir contents | 0 | §4.2 (C-08) |
| 18 | 05:04:07 | Regression: `--failed`; `nvidia-smi -L`; uptime; listeners; masks ×4; rfkill held; save-file stat; routes; rfkill service run count | 0 | §5 |
| 19 | 05:04:24 | Independent second session: identity + masked ×4 + wlan state/saved + sudo | 0 | §5 |
| 20 | ~05:05+ | Local: write `04-rick-hxs3-os-readiness.md`; delete `/tmp/.rick-m1-hxs3` (helper + evidence) | — | §11 |

Signed: **rick** — Expert Ubuntu Server Engineer, session `rick-m1-20260826-01`, 2026-08-26T05:05Z (UTC).
