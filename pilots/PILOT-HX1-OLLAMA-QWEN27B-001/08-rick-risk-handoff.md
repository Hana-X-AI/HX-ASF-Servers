# Rick → Esme — Signed OS Risk Handoff (M2 → M4)

| Field | Value |
| --- | --- |
| From | Rick — Expert Ubuntu Server Engineer (session `rick-m2-20260824-01`) |
| To | Esme (John-Ollama), via Kimi-K3 Gate 1 |
| Pilot | `PILOT-HX1-OLLAMA-QWEN27B-001` |
| Host | `hxs-1` (192.168.50.200), Ubuntu 24.04.4 LTS, kernel 7.0.0-28-generic (running) |
| Signed | 2026-08-25T00:15Z (UTC) |
| Companion evidence | `07-rick-os-readiness.md` (all FACT citations below), `04-rick-inventory.txt` (M1) |
| Plan reference | §7.1 item 10 — values, files, commands, evidence paths, risks, rollback |

**Scope basis:** read-only validation plus one authorized change (sleep-target mask, D4). Nothing below proposes that Esme alter the OS plane; items needing OS mutation are marked **PROPOSED — requires Kimi-K3/owner authorization**, not for Esme to apply.

---

## 1. Handoff values (frozen for M4)

| Value | For use in | Source |
| --- | --- | --- |
| `CUDA_VISIBLE_DEVICES=GPU-2ace9bfc-3a2d-f5b9-d270-82d043f8a7b7,GPU-d675a1cd-7d3d-0903-3b1b-7d95f321a0a9` | ollama.service drop-in (plan §4.2 rule 1: UUIDs, never numeric indices) | FACT `nvidia-smi -L` (07 §6.1) |
| `OLLAMA_HOST=127.0.0.1:11434` | drop-in | AUTHORITY plan §6.2 (no host firewall exists — loopback is the only boundary, see R-008 note) |
| Driver `580.173.02` (Ubuntu archive `580-server-open`, CUDA 13.0) | install pre-check | FACT §6.1 (D3 retain-and-validate) |
| Kernel `7.0.0-28-generic` running; `7.0.0-30-generic` staged | reboot planning | FACT F-010 (07 §6.9) |
| Model path `/usr/share/ollama/.ollama/models` on root ext4, 3.4 T free | capacity + ownership check at M4 | FACT §6.7 (D1) |
| GPU access: no group changes needed (`/dev/nvidia*` world-`rw`) | service-user design | FACT §6.4 |
| Sleep policy: suspend/hibernate/hybrid/suspend-then-hibernate all **masked** | always-on assumption | FACT §4 of 07 |
| Time: UTC, timesyncd synced; DNS: stub → 192.168.50.1; IP: static 192.168.50.200/24 | API/monitoring design | FACT §6.5 |
| Service limits: `LimitNOFILE=65535` fits (hard 1048576; `DefaultLimitNOFILE=524288`) | drop-in (plan §4.2) | FACT §6.6 |
| No ollama binary/user/unit present; listeners `:22` + loopback DNS only | pre-install baseline capture (runbook 10.1 step 2) | FACT §6.2/§6.9 |

## 2. Files and ownership map (what exists, what Esme will create)

| Path | State now | Owner at M4 |
| --- | --- | --- |
| `/etc/systemd/system/{suspend,hibernate,hybrid-sleep,suspend-then-hibernate}.target` | symlinks → `/dev/null` (Rick, this milestone; do not remove without owner decision) | Rick |
| `/usr/share/ollama/` | absent — installer creates it | Esme (verify `ollama:ollama` ownership before first pull) |
| `/etc/systemd/system/ollama.service.d/hx1.conf` | absent — Esme deliverable per plan §4.2 | Esme (Rick reviews GPU/dependency posture first per plan §4.2 preamble) |
| `/usr/local/libexec/hx-ollama-preload` + preload unit | absent — Esme deliverable per plan §4.3 | Esme |
| `/etc/netplan/50-cloud-init.yaml` | static 192.168.50.200/24, gw/DNS 192.168.50.1 | Rick (read-only at M4) |
| `/etc/systemd/sleep.conf`, `logind.conf` | stock defaults (mask, not config, enforces the suspend ban) | Rick |

## 3. Commands Esme will rely on — pre-validated

- `nvidia-smi`, `nvidia-smi -L`, `nvidia-smi topo -m`, `nvidia-smi dmon` — all functional unprivileged as `hxsa`; will work identically for the `ollama` service context (nodes world-`rw`).
- `journalctl -k` readable unprivileged (Xid/OOM watch at M5–M7).
- `systemctl is-enabled suspend.target` must return `masked` — a cheap pre-install assertion Esme should re-run at M4 start.
- API probes per plan §6.1 — not testable until installed (M4); loopback binding must be verified **before first pull** (runbook step 5).

## 4. Risk dispositions (plan §7.3 register)

| Risk | Disposition | Detail / evidence |
| --- | --- | --- |
| R-002 GPU drivers | **VALIDATED — residual item carried** | 580.173.02 from Ubuntu archive only, installed==candidate, no holds, DKMS built for running `-28` **and** staged `-30`; zero Xid/NVRM errors 08-11→08-25. Residual: first owner-approved reboot will boot `7.0.0-30` — Esme must re-run `nvidia-smi -L` + `dkms status` before any acceptance step after that reboot (FACT F-010). |
| R-003 CUDA/ROCm | **CLOSED (NVIDIA-only)** | No ROCm/amdgpu/`/opt/rocm`; only inert `ocl-icd-libopencl1`. Esme constraint stands: no ROCm install, no second stack (work-order prohibited action continues to apply fleet-side). |
| R-004 Secure Boot | **CLOSED (state recorded)** | `SecureBoot disabled`; standing directive D2 = never enable. Unsigned/DKMS module load is a non-issue while D2 stands. |
| R-005 Multi-GPU assumption | **OPEN — Esme-owned, with new OS fact** | OS plane proves both GPUs eligible. New FACT: GPU1 PCIe link is **Gen4 x4 (max x16)**, GPU0 x16; topo `NODE`, no NVLink — bandwidth-asymmetric pair. Esme must (a) prove both-GPU allocation via `ollama ps` + per-GPU telemetry under load, (b) re-query `pcie.link.width.current` under load (ASPM downshift vs wired-x4 cannot be separated in read-only M2), (c) never promise a 50/50 split (plan §5.1). |
| R-013 Storage | **REDUCED to monitoring** | Root ext4 3.4 T free (1 %), inodes 1 %; model path on always-mounted root fs (D1); no separate mount dependency exists. M4 actions for Esme: verify `/usr/share/ollama` ownership before pull; record storage delta after pull (runbook step 7); capacity alerting remains a monitoring duty at M5+. |
| R-014 Permissions | **OS plane CLOSED; M4 verification item** | `/dev/nvidia*` world-`rw` root:root → service user needs **no** group/permission change for CUDA; `video`/`render` groups govern only the Intel DRM nodes. Esme: confirm `ollama` user is system-type with no login shell (upstream installer default) and that the unit runs as that user. Note for owner (not a request): world-`rw` GPU nodes mean any local account can use the GPUs; tightening is a possible future hardening change, not pilot scope. |
| R-015 Boot ordering | **OPEN — joint Rick+Esme; new evidence** | New FACT F-011: `systemd-networkd-wait-online.service` is enabled but **failed** at the 08-17 boot because the NIC had no carrier for ~33 min, then flapped twice. Config itself is standard (netplan drop-in, `-i enp131s0:degraded`, 120 s timeout). Implications: (1) preload unit's bounded retry (12×5 s per plan §4.3) can be defeated by a slow carrier — Esme should treat `/api/ps` assertion failure with retry-budget exhaustion as an alert, not a loop; (2) M7 three-reboot test must record carrier-up time per boot. **PROPOSED (needs Kimi-K3 authorization, not M4 scope):** wait-online drop-in adjustment (scoped interface/timeout) and/or switch/cable inspection. No OS change made. |
| R-016 Suspend/resume | **MITIGATED at OS plane** | All four sleep targets masked (07 §4, diff + 4-view validation + unmask inverse). Esme inherits: processor-split alert (plan §4.5) remains the detection half of this risk. |
| R-017 Thermal/power | **BASELINE SET — monitoring continues** | Idle: 40/36 °C, ≈40 W draw vs 285 W caps, SM 2640/2610 MHz; TCPU 43 °C. Persistence mode Disabled (untouched per plan 7.2 "conditional"). GPU1 x4 link may shift performance/thermal balance under soak — see R-005. lm-sensors absent (no CPU/fan telemetry beyond sysfs zones; installing it is PROPOSED, not authorized). |

### New risks found in M2 (appended to register numbering)

| Risk | Level | Description | Mitigation / proof | Owner |
| --- | --- | --- | --- | --- |
| R-023 Boot network delay | High | Physical carrier can be absent for tens of minutes at boot (observed 33 min + flaps on 08-17), failing `networkd-wait-online` and potentially starving the preload retry budget | See R-015 disposition: preload must alert-not-loop on retry exhaustion; M7 records carrier timing; PROPOSED wait-online remediation + physical link inspection (switch/cable/port) awaiting authorization | Rick + Esme |
| R-024 PCIe AER on Wi-Fi port | Low-Medium | 55 correctable Physical-Layer RxErr lines (≈9 bursts, 08-23→08-24) on `pcieport 80:1c.0` = Wi-Fi card (bus 82), which is DOWN/unused; zero AER on GPU ports | Monitor-only: include `journalctl -k | grep "AER"` in M5+ health checks; escalation trigger = any Uncorrectable error or any AER on GPU ports `00:06.0`/`80:1b.0` | Rick |

### Owner-visible observations (not risks, no action requested)

- **O-1:** Hailo-8 AI co-processor present (`84:00.0`), no driver/stack loaded — inert; does not affect the CUDA branch. Intel NPU/iGPU present, stock drivers.
- **O-2:** One user session counted by `uptime` with empty `who` (typical of non-login processes); no unauthorized listeners or logins observed.

## 5. Rollback summary (OS plane)

| Item | Inverse | Reboot needed |
| --- | --- | --- |
| Sleep-target mask | `sudo systemctl unmask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target` | No |
| Everything else | Nothing to roll back — all other M2 work was read-only | — |

Esme's own install-rollback duties are unchanged per plan §10.2; the OS baseline to restore against is exactly the state in `07-rick-os-readiness.md` §6 plus the mask.

## 6. Gate-1 readiness statement

From the OS plane: driver retained and validated (D3), Secure Boot recorded disabled (D2), model volume validated on root ext4 (D1), suspend disabled (D4), no conflicting acceleration stack, baselines frozen, and the two open items (R-005 bandwidth proof, R-015/R-023 boot-network behavior) are assigned and testable within M4–M7 scope. I find **no OS-plane blocker** to Esme proceeding at M4.

Signed: **rick** — Expert Ubuntu Server Engineer
Session `rick-m2-20260824-01` · WO-HX1-RICK-M2-001 · 2026-08-25T00:15Z (UTC)
