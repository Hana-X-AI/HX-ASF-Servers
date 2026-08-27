# Rick — hxs-8 Post-Upgrade Readiness Assessment (p11 Wave 0A)

| Field | Value |
| --- | --- |
| Task ID | rick-hxs8-readiness-2026-08-27 (PILOT-OMNIROUTE-LAYER0-001 Wave 0A) |
| Agent | Rick (Ubuntu Server Engineer) |
| Commission | Governor, 2026-08-27: hxs-8 post-memory-upgrade readiness for the OmniRoute role. READ-ONLY everywhere. |
| Target | hxs-8 (192.168.50.207) ONLY |
| Executor | hxs-5 (192.168.50.204) |
| Boundary compliance | Zero mutations on hxs-8 — no installs, no config writes, no service actions, no firewall touches. The only RETAINED state written anywhere was the hxs-8 host-key pin in hxs-5's `~/.ssh/known_hosts` (executor-side, F-05 mechanism, verified against owner console evidence — see §2). Temporary askpass/SSH helper files were created on hxs-5 during execution and deleted + verified absent at task end; **no state of any kind was written on hxs-8**. (Correction appended 2026-08-27 per review batch 16: retained-vs-temporary writes distinguished.) |
| Evidence window | 2026-08-27T03:38Z – 03:46Z (all times UTC) |
| Result | **PASS — assessment complete; readiness verdicts in §5** |

## 1. Knowledge review receipt

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Source: /opt/tkv-local/ubuntu (re-confirmed present 2026-08-27T03:42:36Z; corpus carries
        no OmniRoute or host-readiness runbook — per profile §4, live state + the
        OmniRoute source snapshot + server records govern)
Target Host/Scope: hxs-8 — read-only post-upgrade readiness (Layer-1 inputs only)
Reviewed At: 2026-08-27T03:38-03:42Z
Relevant Files: servers/hxs-8/discovery.md (2026-08-12 baseline + 2026-08-27 owner
  update; identity; PENDING memory items); pilots/PILOT-OMNIROUTE-LAYER0-001/
  01-state-log.md (p11 M0, Option A, Layer 0 only);
  /opt/tkv-local/OmniRoute-release-v3.8.51/package.json (engines: node
  ">=22.22.2 <23 || >=24.0.0 <27") and README.md (default port localhost:20128);
  /opt/tkv-local/servers/hxs-8/pre-work-results.md (owner console evidence:
  ED25519 host key fingerprint, passwordless sudo preparation);
  /home/hxsa/opt/local-tkv/agent-zero-docs/keys.md/ssh-info.md (access procedure)
Ubuntu Release/Kernel Identified: Ubuntu 24.04.4 LTS noble, 7.0.0-30-generic (live)
Applicable Authority/Runbooks/Tests: governor commission 2026-08-27 (three evidence
  classes + verdict requirement); profile §14 (host-key escalation path — invoked
  and resolved, §2)
Configuration Owners Identified: none changed (read-only task)
Contradictions or Gaps: p11's "hxs-8 offline" state was stale (host online — state
  log seq 1 already resolved this); no other contradictions
Task May Proceed: YES
```

## 2. Identity proof (verified FIRST, before any assessment)

| Check | Expected (authority) | Observed (live) | Result |
| --- | --- | --- | --- |
| Hostname | hxs-8 (discovery) | hxs-8 | MATCH |
| Peer IP | 192.168.50.207 (registry/commission) | 192.168.50.207 (`$SSH_CONNECTION`) | MATCH |
| Machine ID | 91086d5265a74450b7c2047b3b7ca2ae (discovery) | 91086d5265a74450b7c2047b3b7ca2ae | MATCH |
| Host key | SHA256:qtFdqEskYzA8l1nl+E1cW4/Z/TK+mpxWHHpYsGJp2EI (owner's preparation-session console record, `/opt/tkv-local/servers/hxs-8/pre-work-results.md` line 313) | Identical fingerprint from live `ssh-keyscan` probe | MATCH — pinned to hxs-5 `~/.ssh/known_hosts` (entry #20) |

Host-key note (profile §14 path, resolved without escalation): hxs-8 was absent from hxs-5's `known_hosts`, so the first connection correctly failed strict checking (rc=255, recorded in the log). No TOFU acceptance and no check-disabling occurred: the live key was scanned, fingerprinted, and compared against the owner's own first-connection console record before pinning. All subsequent sessions ran `StrictHostKeyChecking=yes`.

## 3. Hardware — baseline vs current

| Area | Baseline (discovery, 2026-08-12) | Current (live, 2026-08-27T03:45-46Z) | Verdict |
| --- | --- | --- | --- |
| CPU | i5-9400T, 1 socket, 6C/6T, no SMT, VT-x, NUMA 1 | Identical (`lscpu`) | MATCH |
| Memory visible | 46 GiB (owner session 01:26Z; original baseline 16 GB) | 46 Gi total / 865 Mi used / 46 Gi available (`free -h`; MemTotal 49,191,184 kB) | MATCH — upgrade confirmed live |
| DIMM topology | **PENDING** (original: 1×16 GB single-channel) | **RESOLVED:** ChannelA-DIMM0 = 32 GB Samsung SODIMM DDR4 (M471A4G43MB1-CTD, rank 2); ChannelB-DIMM0 = 16 GB Micron SODIMM DDR4 (16ATF2G64HZ-2G6E1, rank 2). Both channels populated (48 GB raw → 46 GiB visible) | RESOLVED (was PENDING) |
| Memory speed | PENDING (original: DDR4-2666) | Both DIMMs rated 2667 MT/s, configured 2666 MT/s, 1.2 V | RESOLVED |
| Memory ECC | PENDING (original: None) | Physical Memory Array Error Correction Type: **None** (DMI type 16) — non-ECC confirmed post-upgrade | RESOLVED |
| Channel mode | PENDING | Both channels populated is the established fact; effective interleave/flex-mode behavior (32+16 asymmetric) is **NOT ESTABLISHED** from read-only evidence — see §6 | Partial |
| GPU | None discrete; UHD 630 i915 | UHD 630 only in `lspci` (8086:3e92); no other display/3D device | MATCH |
| Storage | 476.9 GB NVMe (PC SN530), root 1.6% | Same device; `/` 7.6 G used of 468 G (2%), 437 G available; EFI 1% | MATCH (usage drift +0.4-0.5 pt — normal OS growth) |
| Network | eno1 .207/24, 1000 Mb/s full; wlp2s0 DOWN | eno1 UP, speed 1000, operstate up; wlp2s0 DOWN | MATCH |
| Swap | 4.0 GiB, file-backed | `/swap.img` 4 G file, 0 B used | MATCH |
| DMI observation | — | DMI type-16 "Maximum Capacity: 32 GB" reads lower than the 48 GB physically installed and 46 GiB OS-visible. Firmware-reported field, not an operating limit (memory is fully visible). Recorded as an observation, not a defect | NOTED |

Maintenance-reboot evidence: boot time **2026-08-27 01:40:06**, uptime 2 h 5 m at probe time, boot-id `e492546c-02b2-4cc6-b9ca-21b7aacc5e29` — consistent with the owner's 01:26Z upgrade session followed by a reboot.

## 4. OS state

| Item | Baseline / expectation | Current (live) | Verdict |
| --- | --- | --- | --- |
| Release | Ubuntu 24.04.4 LTS noble | Ubuntu 24.04.4 LTS, x86_64 | MATCH |
| Kernel | 7.0.0-30-generic expected (owner update; baseline -28) | 7.0.0-30-generic running | MATCH — HWE update effective |
| Updates | ~10 per login banner (owner session) | `apt list --upgradable` = **5**, all python3.12 3.12.3-1ubuntu0.15 → .16 (libpython3.12-minimal/-stdlib, libpython3.12t64, python3.12-minimal, python3.12) | 5 verified; banner's 10 not reproduced — banner is login-time generated and may predate list refresh or count differently. No lists were updated (`apt update` would be a mutation — not run) |
| Reboot-required | Not reverified at owner session | `/var/run/reboot-required` ABSENT | VERIFIED — none pending |
| Failed units | none | 0 loaded units listed | MATCH |
| Sleep masks | n/a (non-LLM host) | All five sleep-family targets `static` (unmasked) | NOTED — consistent with a non-LLM host; the LLM-host mask set does not apply here (record only) |
| Timezone | Etc/UTC (owner session) | Etc/UTC (UTC, +0000), Local == Universal | MATCH — already fleet-aligned |
| NTP | active, synchronized | `NTP service: active`, `System clock synchronized: yes`, Server **185.125.190.58 (ntp.ubuntu.com)**; `/etc/systemd/timesyncd.conf` all-commented (compiled distro defaults) | RECORDED, NOT CHANGED — hxs-8 was outside the fleet time pass. It runs Etc/UTC but sources time from the distro default, not the pinned `time.cloudflare.com`. Whether the one-source directive extends to hxs-8 is a governor/owner decision (see §5 F-2) |
| ufw | inactive; unit disabled at boot (preparation) | `ufw status verbose` → **Status: inactive** (sudo read of status only) | MATCH — owner no-firewall rule intact; not touched |
| open-vm-tools | installed, upgraded during preparation | `open-vm-tools 2:13.0.10-0ubuntu0.24.04.1` (ii); unit enabled but **inactive**, no vmtoolsd process — normal on bare metal (image heritage, no hypervisor to serve) | VERIFIED — not a defect |
| SSH | port 22, password+pubkey | Listens on 0.0.0.0:22 and [::]:22 (only non-DNS listener) | MATCH |

## 5. OmniRoute-role readiness (Layer-1 inputs, evidence only)

Source-of-truth for requirements: `/opt/tkv-local/OmniRoute-release-v3.8.51/package.json` engines `"node": ">=22.22.2 <23 || >=24.0.0 <27"`; README default `localhost:20128`.

| Input | Requirement | Observed | Verdict |
| --- | --- | --- | --- |
| Node.js | >=22.22.2 <23 \|\| >=24.0.0 <27 | **ABSENT** (node/nodejs/npm/npx all absent) | **GAP — the single hard Layer-1 dependency** |
| Docker/Podman | none (report only) | docker, podman absent; no docker/podman/containerd units | CLEAR |
| Ollama | expected absent (not an LLM backend host) | ollama absent; no ollama unit | MATCH |
| Port 20128 / 20xxx | free for OmniRoute | Listeners: only 22/tcp + systemd-resolved stub 53; nothing in 20000–20999 | CLEAR |
| Conflicting services | no nginx/apache/caddy/gateway daemons | All absent as binaries; zero matching unit files (incl. `*route*`/gateway/omni) | CLEAR |
| Disk for install | ample free space | 437 G available on `/` | CLEAR |
| DNS | resolves itself; working resolver | `getent hosts hxs-8` → 127.0.1.1 (self, /etc/hosts); `getent hosts 192.168.50.207` → hxs-8; resolv.conf → 127.0.0.53 stub (systemd-resolved), upstream 192.168.50.1 | CLEAR |
| ufw | record only | inactive (owner rule: no host firewalls) | CLEAR — LAN boundary governs |
| python3 | — | 3.12.3 present | NOTED |

**Overall verdict: SUITABLE-WITH-FINDINGS.** No blockers beyond the expected Layer-1 dependency gap.

- **F-1 (Layer-1 dependency, expected):** Node.js absent — must be installed at Layer-1 within `>=22.22.2 <23 || >=24.0.0 <27` (a mutation; not performed here).
- **F-2 (fleet-consistency decision for governor/owner):** hxs-8 keeps distro-default NTP (`ntp.ubuntu.com`) and was not in the one-source fleet pass. Timezone is already Etc/UTC. Recorded, not changed.
- **F-3 (hygiene, owner's maintenance lane):** 5 python3.12 upgrades pending; no reboot required. Not applied (mutation, out of scope).
- **F-4 (host-key hygiene):** hxs-8 host key now pinned on hxs-5 against owner console evidence (§2). Fleet key-coverage gap (hxs-8 previously unpinned) is closed for this executor.
- **F-5 (observation only):** DMI type-16 "Maximum Capacity: 32 GB" is lower than the 48 GB installed; OS sees all 46 GiB. Firmware reporting quirk; no action.

## 6. NOT ESTABLISHED / requires mutation (labeled, not performed)

- **Memory channel-mode characterization** (flex-mode interleave behavior of the asymmetric 32+16 GB layout) — dmidecode establishes both channels populated; effective interleaving is not exposed by read-only SMBIOS data. Characterizing it needs a memory-bandwidth benchmark (load-generating; Layer-1+ decision, out of scope).
- **SMART/NVMe health detail** — smartctl/nvme-cli absent; installing them is a mutation (optional Layer-1 hygiene).
- **Fresh apt metadata** — `apt update` not run (mutation); upgradable count reflects the host's current lists.
- **All OmniRoute installation, service, and port-binding work** — Layer-1 scope, not performed.

## 7. Sequential command log (sanitized)

All local commands as hxsa@hxs-5; remote commands as hxsa@hxs-8 over independent fresh SSH sessions; password supplied via execution-time askpass helper only (never in argv/history/logs); sudo via the same stdin mechanism. Every remote command was read-only. The credential value appears nowhere.

| Seq | Timestamp (UTC) | User/Host | Command (sanitized) | Exit |
| ---: | --- | --- | --- | ---: |
| 1 | 03:38~ | hxsa@hxs-5 | Read `servers/hxs-8/discovery.md`; `ls` pilot dir; Read pilot `01-state-log.md` | 0 |
| 2 | 03:41~ | hxsa@hxs-5 | Grep `engines`/port 20128 in `/opt/tkv-local/OmniRoute-release-v3.8.51/package.json` + README | 0 |
| 3 | 03:42:36 | hxsa@hxs-5 | Re-check knowledge dir; create askpass/ssh helpers (mode 700); extraction smoke test `\| wc -c` → 10 | 0 |
| 4 | 03:42:4x | hxsa@hxs-5→hxs-8 | First ssh identity attempt → **FAIL: host key not known (strict checking)** | 255 |
| 5 | 03:43~ | hxsa@hxs-5 | `ls servers/hxs-8/`; grep host-key/fingerprint in server records → none; `ssh-keygen -F … known_hosts.old` → none | 1 |
| 6 | 03:43~ | hxsa@hxs-5 | Grep `/opt/tkv-local/servers/hxs-8/` → owner pre-work ED25519 fingerprint located; read context lines 305-317 | 0 |
| 7 | 03:44~ | hxsa@hxs-5 | `ssh-keyscan -t ed25519 192.168.50.207` → local fingerprint → **MATCH** vs owner console record → append pin to `~/.ssh/known_hosts` (executor-side) | 0 |
| 8 | 03:45:06 | hxsa@hxs-8 | Unprivileged read-only battery: identity/boot-id, os/kernel/uptime, lscpu, free/meminfo, lspci, lsblk/df, ip/link state, timedatectl + timesync-status + conf, `apt list --upgradable` (read-only), reboot-required flag, failed units, sleep masks, runtime presence (node/npm/docker/podman/ollama/nginx/apache2/caddy/python3), conflict units, `ss -lnt/-lnu` + 20xxx check, getent/resolv.conf, open-vm-tools dpkg probe, swapon | 0 |
| 9 | 03:46:00 | hxsa@hxs-8 | open-vm-tools status re-probe (dpkg status-abbrev, vmtoolsd ps, unit alias); single sudo block (read-only): `dmidecode -t memory`; `ufw status verbose` | 0 |
| 10 | 03:47~ | hxsa@hxs-5 | `rm -f` both helpers; `ls` verify absent | 0 |

## 8. Summary

- hxs-8 is verifiably the discovered host (hostname, peer, machine-id, host key all matched to independent records) and is healthy post-upgrade: expected kernel, 46 GiB visible, zero failed units, no reboot pending, storage/network/CPU consistent with baseline.
- All three discovery PENDING memory items are resolved: 32 GB Samsung + 16 GB Micron DDR4-2666/2667 SODIMMs, both channels populated, non-ECC.
- Readiness: **SUITABLE-WITH-FINDINGS** — the only hard gap for Layer-1 is Node.js (absent; required range recorded). Port 20128 and the 20xxx range are free; no conflicting services; disk, DNS, and firewall posture are clear.
- Nothing on hxs-8 was changed. The two fleet-consistency decisions (NTP one-source extension to hxs-8; pending python3.12 updates) are recorded for the governor/owner, not acted on.

`PASS — TASK COMPLETE`
