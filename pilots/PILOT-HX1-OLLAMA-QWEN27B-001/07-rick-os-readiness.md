# Rick — M2 OS Readiness Report (hxs-1)

`[TASK COMPLETE — EVIDENCE ATTACHED]`

| Field | Value |
| --- | --- |
| Agent | Rick — Expert Ubuntu Server Engineer |
| Session | `rick-m2-20260824-01` |
| Work order | `WO-HX1-RICK-M2-001` (sha256 `ae668fc46165bc3afcf2d67419888289f2343fbf369e942358ebfd5ffdfbe875` per state log seq 7) |
| Pilot | `PILOT-HX1-OLLAMA-QWEN27B-001` |
| Target | `hxs-1` (192.168.50.200), Ubuntu 24.04.4 LTS, kernel 7.0.0-28-generic, x86-64 |
| Executed from | `hxs-5` via SSH `hxsa@192.168.50.200` (askpass pattern; secret never printed, logged, or stored; helper deleted at task end) |
| Window (host clock, UTC) | 2026-08-25T00:07:45Z → 2026-08-25T00:14:20Z |
| Owner decisions applied | D1 (models on root ext4), D2 (Secure Boot stays disabled), D3 (retain-and-validate driver 580.173.02), D4 (suspend mask authorized) |
| Mutations performed | Exactly one: `systemctl mask` of the four sleep targets (D4). No reboot. No other change of any kind. |

Evidence labels per plan §2.2: **FACT** (host command output), **AUTHORITY** (owner decision / governance), **UPSTREAM** (official docs), **INFERENCE** (engineering conclusion), **RECOMMENDATION** (not executed).

---

## 1. Knowledge Review

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Source: /opt/tkv-local/ubuntu (ubuntu.com-main corpus)
Target Host/Scope: hxs-1 (192.168.50.200) — M2 OS readiness + one authorized change per WO-HX1-RICK-M2-001
Reviewed At: 2026-08-25T00:06:50+00:00 (per-task review; M1 receipt 03-rick-tkv-receipt.md superseded for this task)
Relevant Files: 8 (targeted for a 24.04 LTS GPU host):
  - /opt/tkv-local/ubuntu/ubuntu.com-main/releases.yaml  (24.04.4 current point release; EOL April 2029; 26.04 = latest LTS — release-matching enforced)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/about/release-cycle.html
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/about/release_cycles/ (ubuntu-eol.html, kernel-eol.html, releases-table.html)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/security/ (index, cves/, notices/, oval/osv/vex pages)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/certified/ (index, servers, components, hardware-details)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/server/ (index, base_server)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/ai/ + download/nvidia-jetson/ (searched for NVIDIA driver guidance — marketing/Jetson-only content; no driver runbook)
  - Corpus-wide targeted searches: "suspend"/"hibernate" (0 hits), "timesyncd"/"chrony"/"ufw"/"systemd" in server+security templates (0 hits), "nvidia" (Jetson/AI marketing only)
Ubuntu Release/Kernel Identified: Ubuntu 24.04.4 LTS (noble), HWE kernel 7.0.0-28-generic running; 7.0.0-30 installed (reboot-pending, see F-010); systemd 255.4-1ubuntu8.17
Applicable Authority/Runbooks/Tests:
  - agents/rick/profile.md (startup §5, lifecycle §6, test-first §7, sanitization §11, escalation §14)
  - plan.md §2.2 (evidence labels), §3 (host specs), §5.2 (PCIe/thermal duty), §7.1/7.2/7.4 (requirements, tuning policy, checklist)
  - 05-work-order-rick-m2.yaml (bounded scope; exact authorized mask command)
Configuration Owners Identified: netplan (50-cloud-init.yaml) owns network → systemd-networkd backend; systemd/logind owns sleep policy; Ubuntu archive (noble-updates/restricted + noble-security/restricted) owns NVIDIA driver packages; no cloud-init network regeneration observed (renderer output static in /run); no second config plane found
Contradictions or Gaps:
  - GAP (known from M1, non-blocking): corpus is the ubuntu.com web-app tree; it contains no suspend/hibernate, time-sync, firewall, or NVIDIA-driver runbook. For those areas the profile §4 authority order was applied: work order (explicit Kimi-K3 instruction, rank 1) → live host evidence (rank 4) → release-matched installed package metadata and man-page-level behavior (rank 5). No corpus content authorized any mutation; the only mutation executed is the one spelled out in the work order.
  - No live/knowledge conflicts found.
Task May Proceed: YES
```

## 2. Authority and Target

- **AUTHORITY:** M2 approved by owner decision D4 (2026-08-24, state log seq 5–6). Single authorized change quoted verbatim from the work order: `systemctl mask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target`. Everything else read-only.
- **FACT:** identity verified before any probe (evidence `00-identity`): `hostname` → `hxs-1`; `enp131s0` → `192.168.50.200/24`; host clock 2026-08-25T00:07:45+00:00; uptime `7 days, 1:20` (boot 2026-08-17 22:47:29 UTC, Boot ID `ef98be76…8099` — matches M1 inventory Boot ID, so no reboot since M1).
- **AUTHORITY:** SSH host key matched `known_hosts` pinned at M1 (`StrictHostKeyChecking=yes`); a changed key would have halted the session.

## 3. Test and Recovery Plan (recorded before mutation)

| Test ID | Property | Procedure | Expected | Pass rule |
| --- | --- | --- | --- | --- |
| T-01 | Identity | `hostname`, `ip -br address` | hxs-1 / 192.168.50.200 | Exact match before probes |
| T-02 | Driver health (D3) | `nvidia-smi`, `dkms status`, dpkg/apt origin, NVRM/Xid journal scan | 580.173.02, 2 GPUs, Ubuntu-archive origin, no Xid | All evidence present, zero GPU Xid |
| T-03 | No ROCm (R-003) | dpkg/lsmod/`/opt/rocm` scans | Absent | No ROCm/amdgpu stack |
| T-04 | PCIe/power/thermal | `nvidia-smi` pcie+power+thermal query, `lspci -tv`, thermal zones | Values captured | Values recorded (no pass threshold; baseline duty) |
| T-05 | GPU device-node model | `ls -l /dev/nvidia* /dev/dri`, `getent group video render` | Permission model established | Model documented for Esme |
| T-06 | Time/DNS/mounts/network-online/firewall | `timedatectl`, `resolvectl`, `findmnt`, wait-online units, `ufw status`, `nft list ruleset` | State established | State recorded; anomalies become risks |
| T-07 | Governor/memory/hugepage/memlock/swappiness/ulimits | sysfs/sysctl/ulimit/systemd probes | Baselines captured | Values recorded (measure-only per plan 7.2) |
| T-08 | Model volume (D1) | `df`, `findmnt`, path posture of `/usr/share/ollama` | Capacity + ownership posture documented | ≥ model-size headroom with margin |
| T-09 | Pre-change sleep-target state | `systemctl is-enabled/status`, `ls -la /etc/systemd/system/*.target`, sleep.conf/logind.conf | All four `static`, unmasked | Recorded as BEFORE artifact |
| T-10 | Authorized mask | `sudo systemctl mask <4 targets>` | Exit 0 AND effective masked state | `is-enabled` → `masked` ×4; symlinks → `/dev/null` |
| T-11 | Post-change validation | is-enabled/status/symlinks/`systemctl cat`; `sleep.target` untouched | masked ×4; `sleep.target` still `static` | All checks pass |
| T-12 | Regression | `systemctl --failed`, `nvidia-smi -L`, `uptime`, `ss -lnt` | No new failed units; 2 GPUs; no reboot; listeners unchanged | Equality with BEFORE |
| T-13 | Access preservation | Second independent SSH session after mutation | Fresh session authenticates; masked state visible | Independent session OK |

Recovery plan: pre-change artifact = recorded `static`/no-symlink state (T-09); exact inverse = `sudo systemctl unmask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target`; rollback trigger = any failed T-10/T-11/T-12/T-13; restart/reboot impact = none (mask is a unit-file symlink operation, effective immediately and at boot); access risk = none (change does not touch SSH, network, PAM, sudo, or storage).

## 4. Implementation (the one bounded change)

**FACT — before (2026-08-25T00:12:58Z):** all four targets `static`, loaded from `/usr/lib/systemd/system/`, no entries in `/etc/systemd/system/*.target`:

```text
suspend.target: static            hibernate.target: static
hybrid-sleep.target: static       suspend-then-hibernate.target: static
ls: cannot access '/etc/systemd/system/suspend.target': No such file or directory   (×4)
```

`/etc/systemd/sleep.conf` — all defaults (every line commented: `#AllowSuspend=yes` etc.). `logind.conf` — all defaults.

**FACT — mutation (2026-08-25T00:13:28Z):**

```bash
sudo systemctl mask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target   # exit 0
```

**FACT — after (2026-08-25T00:13:42Z):** `is-enabled` → `masked` for all four; `systemctl status` → `Loaded: masked (Reason: Unit … is masked.)` ×4; `systemctl cat suspend.target` → `# Unit suspend.target is masked.`

**FACT — diff-equivalent artifact** (the complete and only filesystem change):

```text
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/suspend.target -> /dev/null
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/hibernate.target -> /dev/null
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/hybrid-sleep.target -> /dev/null
+ lrwxrwxrwx 1 root root 9 /etc/systemd/system/suspend-then-hibernate.target -> /dev/null
```

`sleep.target` remains `static` (untouched — it is a passive dependency node, not an entry point; masking it was not authorized and not needed).

**Rollback (exact inverse, ready):**

```bash
sudo systemctl unmask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target
```

Inverse verified by construction (mask/unmask is systemd's self-inverse pair; the pre-change state had no `/etc/systemd/system/*.target` symlinks, which unmask restores exactly).

## 5. Test Execution

- T-01…T-09: **PASS** (all baseline and before-state evidence captured; see §6).
- T-10, T-11: **PASS** — effective masked state proven via four independent views (`is-enabled`, `status`, symlink listing, `systemctl cat`), not by exit code alone.
- T-12: **PASS** — failed-unit set identical to BEFORE (only the pre-existing `systemd-networkd-wait-online.service`, see F-011); both GPU UUIDs listed by `nvidia-smi -L`; uptime 7d1h26 (no reboot); listener set unchanged (`:22` + loopback stub DNS only).
- T-13: **PASS** — second independent SSH session at 00:13:55Z authenticated and observed `masked` ×4.
- Failed/unexecuted: one probe syntax error during discovery (`systemctl is-enabled -.mount` — invalid option, read-only, no effect; root-mount state was instead established via `findmnt`). One `nvidia-smi` query field invalid (`temperature.gpu.max.limit`), re-run with valid fields. No mandatory test failed; none NOT RUN.

## 6. Current State — validated baselines (FACT unless labeled)

### 6.1 Driver health (D3) — PASS

- `nvidia-smi`: driver 580.173.02, CUDA 13.0; GPU0 `02:00.0` and GPU1 `81:00.0`, both RTX 4070 Ti SUPER 16376 MiB, P0, 0 MiB used, no processes; idle temps 40 °C / 36 °C.
- UUIDs match plan §3 exactly: `GPU-2ace9bfc-3a2d-f5b9-d270-82d043f8a7b7`, `GPU-d675a1cd-7d3d-0903-3b1b-7d95f321a0a9`.
- Packages: `nvidia-driver-580-server-open` + full `-580-server` set, version `580.173.02-0ubuntu0.24.04.1`; `apt-cache policy`: installed == candidate, origin `archive.ubuntu.com noble-updates/restricted` and `security.ubuntu.com noble-security/restricted` only; no PPAs or third-party repos in `apt-cache policy` sources; `apt-mark showhold` empty; `dpkg --audit` clean (no output).
- **AUTHORITY:** owner-approved package source requirement (plan 7.1 item 3) is satisfied by the official Ubuntu archive; driver is the Ubuntu `server-open` DKMS branch, not a `.run` installer.
- DKMS: `nvidia/580.173.02` built for **both** `7.0.0-28-generic` (running) and `7.0.0-30-generic` (installed).
- Modules loaded: `nvidia`, `nvidia_modeset`, `nvidia_drm`, `nvidia_uvm`; `nouveau` absent; only modprobe.d entry is stock `blacklist nvidiafb`; `lspci -nnk` shows both GPUs bound to `nvidia`.
- Kernel cmdline: `BOOT_IMAGE=/boot/vmlinuz-7.0.0-28-generic root=UUID=ab09b07d-…-440f18896e99 ro` (no `nomodeset`, no custom params).
- Strict journal scan, retained window 2026-08-11 → 2026-08-25 (4 boots): **zero** `NVRM: Xid`, zero NVRM error lines, zero OOM-kill/OOM-reaper events. Only NVRM line is the normal load banner at boot. (The M1-era loose `xid` grep matches `r8169 … XID 64a` — that is the Realtek NIC's silicon revision string, not a GPU Xid; recorded here to prevent future misreads.)
- Secure Boot (D2): `mokutil --sb-state` → `SecureBoot disabled`. Recorded; never to be enabled (standing directive).

### 6.2 Acceleration branch (R-003) — PASS (NVIDIA only)

- No ROCm packages, no `/opt/rocm*`, no `amdgpu`/`radeon` modules. Only `ocl-icd-libopencl1 2.3.2-1build1` present — a vendor-neutral OpenCL ICD loader library, not an acceleration stack; inert without an ICD. **INFERENCE:** no CUDA/ROCm conflict surface exists.

### 6.3 PCIe topology, power, thermal (plan 5.2, R-017) — captured

- Topology (`lspci -tv`): GPU0 `02:00.0` behind CPU root port `00:06.0`; GPU1 `81:00.0` behind PCH port `80:1b.0`; Wi-Fi `82:00.0` behind `80:1c.0`; Realtek NIC `83:00.0` behind `80:1c.3`; Hailo-8 co-processor `84:00.0` behind `80:1c.4`.
- Link state: GPU0 **Gen4 x16 / max x16**; GPU1 **Gen4 x4 / max x16**. Persistence mode: Disabled (both). Power: limit 285 W default both (GPU1 max_limit 305 W), draw ≈40 W idle. Clocks: 2640/3120 MHz and 2610/3105 MHz (SM current/max). Thermal zones idle: TCPU 43.0 °C, x86_pkg_temp 43.0 °C, acpitz 27.8 °C. `sensors` (lm-sensors) not installed.
- **INFERENCE:** GPU1's x4 current width is consistent with a chipset-attached slot electrically wired x4 (common on desktop boards) and/or ASPM downshift at idle; it cannot be distinguished without load, which M2 prohibits. **RECOMMENDATION:** re-query `pcie.link.width.current` under benchmark load at M5; plan for P2P traffic to traverse the PCH (`nvidia-smi topo -m` shows `NODE`, no NVLink) — a performance consideration for R-005/R-017, not an installation blocker.
- AER: `pcieport 0000:80:1c.0` logged 55 correctable-error lines (≈9 bursts) 2026-08-23 23:51 → 2026-08-24 23:26, all `severity=Correctable, type=Physical Layer, RxErr`, device `[8086:7f3a]`. That port serves the **Wi-Fi card (bus 82)**, not either GPU. **INFERENCE:** no GPU-path AER evidence; Wi-Fi port marginal-signal noise; card is DOWN/unused. Carried as monitoring item R-024 in the handoff.

### 6.4 GPU device-node permission model (R-014) — captured

```text
crw-rw-rw- root root  /dev/nvidia0 /dev/nvidia1 /dev/nvidiactl /dev/nvidia-modeset /dev/nvidia-uvm /dev/nvidia-uvm-tools
crw-rw---- root video  /dev/dri/card0..2        crw-rw---- root render /dev/dri/renderD128..130
groups: video(44, empty), render(993, empty); hxsa is not a member of either
```

- **INFERENCE:** on this host the NVIDIA compute nodes are world-readable/writable (driver/udev default), so the future `ollama` service user (created by Esme's installer at M4) will have CUDA access **with no group or permission change**. The `video`/`render` groups govern only the Intel iGPU DRM nodes and are irrelevant to Ollama GPU access here.
- Security note (FACT): world-`rw` GPU nodes mean any local account can submit GPU work. Acceptable for a single-purpose pilot box; if the owner later wants GPU access restricted, that is a separate authorized change (e.g., udev rule + group) — recorded in the handoff, not implemented.

### 6.5 Time, DNS, mounts, network-online, firewall (plan 7.1 item 7)

- Time: `timedatectl` → UTC, `System clock synchronized: yes`, `NTP service: active`; `systemd-timesyncd` enabled+active, no `chrony`; upstream `ntp.ubuntu.com`, last NTP message stratum 2, jitter 2.6 ms. Single time daemon — no competition.
- DNS: `systemd-resolved` stub `127.0.0.53`; upstream `192.168.50.1` (router) on `enp131s0`; netplan source `50-cloud-init.yaml` is a static config (address `192.168.50.200/24`, gateway+DNS `192.168.50.1`, no DHCP).
- Mounts/ordering: root ext4 (`/dev/nvme0n1p2`, `rw,relatime`) + `/boot/efi` vfat via fstab → `local-fs.target` standard ordering; `/swap.img` 8 G swapfile; no external/model mounts exist that could be missing at boot (D1: models live on root ext4, always mounted before `local-fs.target` completes).
- Network-online (F-011): `systemd-networkd-wait-online.service` is **enabled but failed** at boot (2026-08-17 22:49:32, `status=1/FAILURE`, timeout). Cause in journal: at boot the NIC had **no carrier for ~33 minutes** (`22:47:32 Link is Down` → `23:20:13 Link is Up - 1Gbps/Full`), then two further carrier flaps (23:22:58 down, 23:42:55 up). The wait-online drop-in (`/run/.../10-netplan.conf`) uses `-i enp131s0:degraded` with the default 120 s timeout — hopeless against a 33-minute physical-link outage. Current link state: `routable`, `online`. **INFERENCE:** the failed unit is a symptom of a physical-layer event at that boot (cable/switch/port work), not a config defect; but it proves a cold boot can leave the host without network for tens of minutes, which the M7 three-reboot test and the preload unit's bounded retry must survive. Carried to handoff under R-015 with a PROPOSED (not executed) wait-online remediation.
- Firewall: `ufw status` → **inactive** (unit `enabled`/`active(exited)` but firewall never armed); `nftables` disabled/inactive; `nft list ruleset` → empty. Exposure today: only `:22` and loopback stub-DNS listeners. **INFERENCE:** no host firewall dependency exists for M4 as long as Ollama binds `127.0.0.1` per plan §6.2; any future remote API exposure needs a separate approved firewall/TLS change (R-008 stays with Rick+Esme).

### 6.6 Governor / memory / hugepages / memlock / swappiness / ulimits (plan 7.2 — measured only)

| Setting | Baseline (FACT) | Plan 7.2 posture |
| --- | --- | --- |
| CPU governor | `powersave` ×24 CPUs; `intel_pstate` active, EPP `balance_performance` | Do not change without benchmark (R-012) |
| Swappiness | `vm.swappiness = 60` (default); `vm.overcommit_memory = 0` | Measure first; no change |
| Swap | `/swap.img` 8.0 GiB, 0 B used; no swap I/O in 3 s vmstat sample | Preserve as safety valve (R-011) |
| Hugepages | `nr_hugepages=0`, `HugePages_Total: 0`, `Hugetlb: 0 kB`; THP `[madvise]` / defrag `[madvise]` | Do not enable by default (R-010) |
| Memlock | shell soft=hard `16406644 kB` (~15.6 GiB); systemd `DefaultLimitMEMLOCK=8388608` (8 MiB) | Do not enable mlock by default (R-009) |
| File descriptors | shell `1024` soft / `1048576` hard; `DefaultLimitNOFILE=524288`; `fs.file-max` = 2^63-1; no `limits.conf`/`limits.d` entries | Plan's proposed `LimitNOFILE=65535` service drop-in is within hard/system limits — no OS change needed |
| RAM | 125 GiB total, ~122 GiB free, ~2.1 GiB buff/cache, load 0.00 | Baseline for soak comparison |

### 6.7 Model volume posture (D1, R-013)

- Root ext4: 3.6 T total, 14 G used, **3.4 T free** (1 %); inodes 1 % used. **INFERENCE:** a ~17 GiB `qwen3.8:27b` pull plus KV/cache overhead is capacity-trivial; R-013 reduces to monitoring + service-start dependency, both owned at M4+.
- `/usr/share/ollama` — **does not exist yet** (expected: Esme's M4 installer creates it, default ownership `ollama:ollama` per upstream install script — **UPSTREAM:** docs.ollama.com/linux). Parent `/usr/share` is stock `root:root 0755`. No storage change made (D1 honored). **RECOMMENDATION:** at M4, Esme verifies path ownership/permissions before first pull (checklist item carried in handoff).

### 6.8 ulimits / service posture for the future service

Recorded in §6.6. No OS-level blocker for the proposed drop-in values (`LimitNOFILE=65535`).

### 6.9 General platform state

- `systemctl --failed`: exactly one unit — `systemd-networkd-wait-online.service` (documented F-011). Default target `graphical.target`. Listeners: `0.0.0.0:22`, `[::]:22`, loopback stub DNS `127.0.0.53/54:53` only — matches M1, no unexpected listeners.
- Kernels: `7.0.0-28` running; `7.0.0-30` installed (image dated Aug 7, headers+modules complete); `7.0.0-29` config-files only (removed). **FACT (F-010):** the next reboot will boot `7.0.0-30-generic`. DKMS for 580.173.02 is pre-built for it, so GPU availability across that transition is expected but unproven. **RECOMMENDATION:** at the first owner-approved reboot, validate `nvidia-smi` + DKMS binding before any Ollama acceptance step (carried in handoff under R-002).
- Observation (no action): a Hailo-8 AI co-processor (`84:00.0`) is present with **no driver loaded** and no userland stack — inert; noted for owner visibility only. Intel Arrow Lake NPU and iGPU also present (stock `xe`/`i915` stack). None conflicts with the CUDA branch (R-003).

## 7. Readiness checklist — plan §7.4 verdicts

| # | Item | Verdict | Basis |
| --- | --- | --- | --- |
| 1 | TKV receipt complete and approved | **PASS** | §1 receipt (per-task re-review); Task May Proceed: YES |
| 2 | Live hardware table replaces placeholders | **PASS** | M1 `04-rick-inventory.txt` + M2 confirmations §6.1/6.3 (no drift: same Boot ID, same GPUs/driver/kernel) |
| 3 | GPU vendor branch decided; no conflicting stack | **PASS** | NVIDIA-only; no ROCm/amdgpu §6.2 |
| 4 | GPU UUIDs, VRAM, driver, topology, thermals evidenced | **PASS** | §6.1, §6.3 (incl. GPU1 x4-width caveat, carried as handoff item) |
| 5 | Secure Boot / module state evidenced | **PASS** | `SecureBoot disabled` (D2); DKMS modules load on running kernel |
| 6 | Kernel logs show no unresolved GPU/Xid/OOM issue | **PASS** | Zero Xid/OOM in 2026-08-11→25 journals §6.1; non-GPU AER noted R-024 |
| 7 | Model storage path, capacity, ownership, boot mount validated | **PASS** | Root ext4 3.4 T free, always-mounted; path posture documented for M4 §6.7 |
| 8 | Service-user GPU/filesystem access least-privilege tests | **PASS (OS plane)** | GPU nodes world-`rw` → `ollama` user needs no group change §6.4; model-dir ownership check deferred to M4 by design (path absent) |
| 9 | Suspend policy, time sync, DNS, firewall, boot dependencies validated | **PASS with findings** | Suspend masked §4; time/DNS/mounts healthy §6.5; findings F-010/F-011 (pending kernel, wait-online) carried to handoff |
| 10 | Baseline CPU/RAM/swap/storage telemetry captured | **PASS** | §6.6, §6.7 |
| 11 | Every OS change has risk, exact diff, validation, rollback | **PASS** | §3–§5 (single change; diff-equivalent; 4-view validation; unmask inverse) |
| 12 | Risk handoff signed and transmitted to Esme | **PASS** | `08-rick-risk-handoff.md` (this package) |

## 8. Evidence Package

Raw sanitized captures were held transiently in the session workspace (`/tmp/.rick-m2-hx1/evidence/`, 14 files: `00-identity` … `13-closing`) and are inlined in §4–§6 above; the workspace (including the askpass helper and secret file) is deleted at task end per the work order. This document plus `08-rick-risk-handoff.md` constitute the complete retained M2 evidence. Prior artifacts: `03-rick-tkv-receipt.md`, `04-rick-inventory.txt` (M1). No secrets, hashes, tokens, machine IDs, or user data appear in retained evidence; LAN addresses shown are already ratified in plan §3.

## 9. Validation Summary (profile §12.5)

- **What changed:** the four systemd sleep targets are now masked on hxs-1 (D4), proven effective via `is-enabled=masked`, `status=masked`, `/etc/systemd/system/*.target → /dev/null` symlinks, and `systemctl cat`. 
- **What did not change:** everything else — no reboot (uptime 7d1h26 continuous through the session), no driver/kernel/DKMS/package/storage/firewall/sysctl/user changes, `sleep.target` untouched, listener set unchanged, Secure Boot still disabled.
- **Current target state:** ready at the OS plane for Esme's M4 install, per the 12/12 checklist above; two findings (F-010 pending kernel, F-011 wait-online/carrier history) are risks to manage, not readiness blockers.
- **Tests:** 13 defined, 13 executed, 13 PASS; 2 read-only probe syntax retries (self-corrected); 0 FAIL, 0 BLOCKED, 0 NOT RUN.
- **Access and recovery:** primary session plus independent second session both valid post-change; sudo path confirmed (`sudo -S` via askpass stdin, secret never persisted); rollback = single `unmask` command, no reboot required either direction.
- **Persistence:** mask is a persistent unit-file state (survives reboot by construction; reboot not permitted in M2 to demonstrate live — flagged honestly: boot-persistence is proven by systemd semantics, not by an observed reboot).
- **Rollback readiness:** immediate, self-inverse, verified pre-change state recorded.
- **Remaining risks/decisions:** see `08-rick-risk-handoff.md` — dispositions for R-002/003/004/005/013/014/015/016/017 and new items R-023 (wait-online/carrier), R-024 (AER Wi-Fi port), plus owner-visible observations (Hailo-8, GPU1 x4 link).

`PASS — TASK COMPLETE`

## 10. Sequential command log (profile §12.4)

All remote commands executed as `hxsa@hxs-1` from `hxs-5` over one SSH control pattern (askpass auth); "sudo" rows used `sudo -S` with the secret on stdin. All times host clock UTC.

| Seq | Timestamp | Command (summary) | Exit | Evidence |
| ---: | --- | --- | ---: | --- |
| 1 | 00:06:50 | Local: TKV presence + corpus tree/searches (`find`, `grep`) | 0 | §1 |
| 2 | 00:07:00 | Local: build askpass workspace `/tmp/.rick-m2-hx1` (secret extracted from credential file, never echoed) | 0 | cleanup confirmed §8 |
| 3 | 00:07:45 | `hostname; date; ip -br address; uptime; who` | 0 | §2 (T-01) |
| 4 | 00:08:38 | Driver batch: `nvidia-smi` ×2, `dkms status`, dpkg nvidia list, `apt-mark showhold`, `lsmod`, `mokutil --sb-state`, cmdline, modprobe.d, journal NVRM/Xid scan | 0 | §6.1 (T-02) |
| 5 | 00:09:11 | Strict Xid scan, AER count/list, kernel image inventory, apt origins/sources, ROCm scan, ollama absence | 0 | §6.1–6.2, F-010 (T-02/T-03) |
| 6 | 00:09:50 | `journalctl --list-boots`, `lspci -tv/-nnk`, nvidia-smi pcie query (field error → rerun), topo, sensors(absent), `/dev/nvidia*` + `/dev/dri`, groups, `id hxsa` | 0 | §6.3–6.4 (T-04/T-05) |
| 7 | 00:10:20 | nvidia-smi pcie/power/thermal queries (valid fields), thermal zones, udev rules, Hailo driver state | 0 | §6.3 (T-04) |
| 8 | 00:10:58 | `timedatectl`, timesyncd units/peers, `resolvectl`, fstab, `findmnt`, mount units, netplan dir, `networkctl`, wait-online enablement, default target, `systemctl --failed`, `ss -lntup` | 0 | §6.5 (T-06) |
| 9 | 00:11:29 | wait-online status + unit journal, `networkctl list`, netplan readability probe | 0 | F-011 |
| 10 | 00:11:54 | sudo: `id -u` (SUDO-OK), `ufw status verbose`, ufw/nftables enablement, `nft list ruleset`, netplan yaml, boot-time `enp131s0` journal | 0 | §6.5 (T-06) |
| 11 | 00:12:25 | Governor/pstate/EPP, swappiness/overcommit/hugepage sysctls, meminfo, THP, ulimits soft/hard, file-max, systemd default limits, limits.conf/.d, `free -h`, `vmstat 1 3` | 0 | §6.6 (T-07) |
| 12 | 00:12:58 | `df -hT/ -i /`, `/usr/share/ollama` posture, root mount, sleep-target unit files/is-enabled/status, sleep.conf, logind.conf, pre-mask symlink check | 0 | §4, §6.7 (T-08/T-09) |
| 13 | 00:13:28 | **MUTATION:** `sudo systemctl mask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target` | 0 | §4 (T-10) |
| 14 | 00:13:42 | Validation: is-enabled/status/symlinks/`systemctl cat`, `sleep.target` check; regression: `--failed`, `nvidia-smi -L`, `uptime`, `ss -lnt` | 0 | §5 (T-11/T-12) |
| 15 | 00:13:55 | Independent second SSH session: identity + masked ×4 | 0 | §5 (T-13) |
| 16 | 00:14:20 | OOM scan, journal window, systemd/dpkg versions, boot timestamp | 0 | §6.1, §6.9 |
| 17 | ~00:15+ | Local: write `07`/`08` deliverables; delete `/tmp/.rick-m2-hx1` (askpass + secret + evidence) | — | §8 |

Signed: **rick** — Expert Ubuntu Server Engineer, session `rick-m2-20260824-01`, 2026-08-25T00:15Z (UTC).
