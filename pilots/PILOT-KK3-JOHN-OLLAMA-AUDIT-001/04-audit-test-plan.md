# 04 — John Audit Test Plan

| Field | Value |
| --- | --- |
| Session ID | `john-initial-20260824-01` |
| Work order | `WO-OLLAMA-AUDIT-HXS5-001` (sha256 `d1883f295b36161c8b9950bb807ce3946d963a261a8b3168d2993b2d08ef672d`) |
| Context hash | `725553195e9c2df97c341fdc08b54c1fcd572c0ada69f9bb376e33f01d8278aa` |
| Correction session | `initial` |
| Executor | `john` (local session on hxs-5, no SSH) |
| Plan written | 2026-08-24T09:36+00:00, **before** any Phase-3 audit probe |
| Knowledge receipt | `03-john-knowledge-review-receipt.md` — `Task May Proceed: YES` |

## Expected-result basis

No ratified Ollama baseline exists for hxs-5 (knowledge review G1). Expected results below derive from:

- **B1** — hxs-5 discovery, 2026-08-12 (`…/servers/hxs-5/discovery.md`): no Ollama, no Docker/containerd, no NVIDIA/CUDA, Intel HD 630 only, i5-7500 4C/4T, 32 GB non-ECC, single 238.5 GB NVMe ext4 root, listeners: tcp/22 + systemd-resolved stub only, ufw inactive.
- **B2** — `SERVER-REGISTRY.md`: hxs-5 role `Edge / ingress — NGINX`.
- **B3** — John profile rule: Ollama defaults to loopback unless explicit current authority permits broader exposure; Ollama has no native authentication (MVP1-CONSTRAINTS, hxs-1 precedent).
- **B4** — Work order: Ollama present or absent is a finding, not an audit failure; record facts either way.

Deviation from B1/B2 is recorded as a **finding** (drift since 2026-08-12), not an automatic FAIL. FAIL is reserved for a verified violation of a controlling rule (e.g., Ollama listening on a non-loopback address with no exposure authority), or for mutually inconsistent identity sources.

## Execution rules

- Read-only only. Prohibited: any mutation, `systemctl restart|stop|start|reload|enable|disable|edit`, `kill`/`pkill`, `ollama pull|rm|create|cp|run|stop`, installers/package managers, `fio`/stress/cache-dropping/load generators, reboot/shutdown/driver reload/GPU reset, anything with uncertain side effects.
- Every command logged to `05-command-log.md` (executed, failed, refused, timeout). One retry allowed for a plausibly transient safe failure; no other repeats.
- `sudo -n` used only where it materially improves read-only evidence (listener process names, journal access); passwordless sudo confirmed in pre-work record. No `sudo` command may mutate.
- Raw outputs saved per probe group under `06-raw-evidence-sanitized/`; secrets redacted as `REDACTED` before retention; secret discovery triggers immediate escalation without reproduction.
- API probes bounded: `--connect-timeout 2 --max-time 10`. Journals bounded (`-n`/`tail`).

## Test definitions

### ID — Identity and host baseline

| Test ID | Property | Exact probe | Expected (basis) | Pass rule |
| --- | --- | --- | --- | --- |
| ID-01 | Target and time | `hostname`; `hostnamectl`; `date --iso-8601=seconds`; `ip -4 addr show` | hostname `hxs-5`; local IPv4 `192.168.50.204` present (B1, work order) | PASS only if both match; mismatch aborts session. Executed as identity gate before all probes |
| ID-02 | OS/kernel | `cat /etc/os-release`; `uname -a` | Ubuntu 24.04.x LTS, x86_64; kernel ≥ 7.0.0-28 (B1, drift expected) | PASS: identity captured; kernel drift recorded as observation |
| ID-03 | Resource baseline | `uptime`; `free -h`; `swapon --show`; `df -hT` | ~32 GB RAM, file-backed swap, single ext4 root on NVMe (B1) | PASS: snapshot captured and consistent with B1 within normal drift |
| ID-04 | Ollama identities | `command -v ollama`; `ollama --version`; `dpkg -l \| grep -i ollama`; `snap list`; `ls -la /usr/local/bin/ollama /usr/bin/ollama /opt/ollama`; `systemctl show ollama -p ExecStart FragmentPath`; `curl -fsS --connect-timeout 2 --max-time 10 http://127.0.0.1:11434/api/version` | All sources agree: absent (B1) — or, if present, CLI/binary/server versions reconcile | PASS: all identity sources agree (unanimous absence or reconciled presence); contradiction = FAIL + escalate |

### HW — CPU, memory, NUMA, storage

| Test ID | Property | Exact probe | Expected (basis) | Pass rule |
| --- | --- | --- | --- | --- |
| HW-01 | CPU topology | `lscpu` | i5-7500, 1 socket, 4 cores, 4 threads, no SMT (B1); VT-x: NOT ESTABLISHED (no virtualization line in captured lscpu evidence) | PASS: matches B1 |
| HW-02 | NUMA | `lscpu` NUMA fields; `command -v numactl && numactl --hardware` | 1 NUMA node (B1); `numactl` likely absent — install nothing | PASS: node count established; absent numactl recorded, not a failure |
| HW-03 | RAM/swap | `free -h`; `swapon --show`; `grep -E 'MemTotal\|MemAvailable\|SwapTotal\|SwapFree' /proc/meminfo` | ~31 GiB usable, file-backed swap (B1) | PASS: captured and consistent |
| HW-04 | Model storage | `lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,ROTA,MODEL`; `findmnt -T / -o TARGET,SOURCE,FSTYPE,SIZE,USED,AVAIL,USE%`; `df -hT`; candidate paths `ls -ld ~/.ollama /usr/share/ollama 2>&1`; effective `OLLAMA_MODELS` via env scan (SVC-04) | Single NVMe, ext4 root, no dedicated model store, no `OLLAMA_MODELS` (B1) | PASS: storage layout established; model-store presence/absence recorded |
| HW-05 | Storage performance | None authorized (no `fio`, no writes, no cache-dropping); search for pre-existing authoritative benchmarks only | No authorized benchmark exists | NOT RUN by design; conclusion `NOT ESTABLISHED` |

### GPU — GPU and accelerator

| Test ID | Property | Exact probe | Expected (basis) | Pass rule |
| --- | --- | --- | --- | --- |
| GPU-01 | Inventory/driver | `command -v nvidia-smi`; `nvidia-smi -L`; `lspci -nn \| grep -Ei 'vga\|3d\|display'` | `nvidia-smi` absent; single Intel HD 630 `8086:5912` (B1) | PASS: absence of NVIDIA confirmed; iGPU matches B1 |
| GPU-02 | Topology/processes | `nvidia-smi topo -m` | Inapplicable — no NVIDIA device | NOT RUN (inapplicable); recorded with GPU-01 evidence |
| GPU-03 | Driver health | `journalctl -k --no-pager \| grep -Ei 'NVRM\|Xid\|nvidia\|oom' \| tail -50` (bounded) | No NVRM/Xid; no OOM kills | PASS: no adverse indicators; journal permission limits recorded if hit |
| GPU-04 | Isolation | Effective service configuration (SVC-02 chain) | No Ollama unit → no isolation config | NOT RUN (inapplicable) if SVC-01 confirms no unit |

### SVC — Ollama service and effective configuration

| Test ID | Property | Exact probe | Expected (basis) | Pass rule |
| --- | --- | --- | --- | --- |
| SVC-01 | Unit/state | `systemctl status ollama --no-pager`; `systemctl cat ollama`; `systemctl list-unit-files --no-pager \| grep -i ollama`; `systemctl list-units --all --no-pager \| grep -i ollama` | Unit not found (B1) | PASS: unit presence/absence established and consistent with B1, or drift recorded as finding |
| SVC-02 | Runtime wiring | `systemctl show ollama -p ExecStart -p User -p Group -p Environment -p FragmentPath -p DropInPaths` | Empty / not-found (B1) | PASS: effective wiring established (or absence confirmed) |
| SVC-03 | Listener | `sudo -n ss -lntp` (fallback: `ss -lnt`); specifically check `:11434` | No `:11434` listener; tcp/22 + resolved stub only (B1) | PASS: listener map captured; any `:11434` listener triggers SEC-01 evaluation |
| SVC-04 | Tuning | `grep -rn 'OLLAMA_' /etc/environment /etc/profile.d/ ~/.bashrc ~/.profile ~/.config/environment.d/ 2>/dev/null`; unit Environment from SVC-02 | All Ollama tunables `NOT SET` (B1) | PASS: each tunable reported as value or `NOT SET` with source |
| SVC-05 | Service health | `journalctl -u ollama -n 200 --no-pager` (sudo -n fallback) | No entries / unit unknown (B1) | PASS: journal state established; absence of entries consistent with B1 |

### API / MOD — API and models

| Test ID | Property | Exact probe | Expected (basis) | Pass rule |
| --- | --- | --- | --- | --- |
| API-01 | Local server | `curl -fsS --connect-timeout 2 --max-time 10 http://127.0.0.1:11434/api/version` | Connection refused, exit 7 (B1) | PASS: server presence/absence established (refusal consistent with B1) |
| API-02 | Pulled inventory | `curl … /api/tags`; `ollama list` | Unavailable / command not found (B1) | PASS: inventory state established; if models exist, names+digests captured |
| API-03 | Loaded inventory | `curl … /api/ps`; `ollama ps` | Unavailable / command not found (B1) | PASS: residency state established; never inferred from pulled inventory |
| MOD-01 | Identity/quantization | Depends on API-02; fallback `ls -la ~/.ollama/models /usr/share/ollama/.ollama/models 2>&1` | No model store (B1) | PASS if digests captured, or absence of any store proven; else NOT RUN |
| MOD-02 | Context alignment | Derived from MOD-01 + approved workload target | No hxs-5 workload target exists (G1) | NOT RUN if no model; conclusion `NOT ESTABLISHED` (no controlling target) |
| MOD-03 | Offload/residency | `/api/ps`/`ollama ps` + passive GPU evidence | No loaded models (B1) | NOT RUN if API-03 absent; residency never claimed from `ollama list` |

### SEC — Network and security

| Test ID | Property | Exact probe | Expected (basis) | Pass rule |
| --- | --- | --- | --- | --- |
| SEC-01 | Exposure | SVC-03 listener map + effective `OLLAMA_HOST` (SVC-04) + governing authority check (none exists) | No Ollama listener at all (B1) — stronger than loopback | PASS: no non-loopback Ollama exposure; any non-loopback listener without authority = FAIL |
| SEC-02 | Proxy/auth boundary | `systemctl list-units --type=service --state=running --no-pager \| grep -Ei 'nginx\|haproxy\|caddy\|traefik\|ollama'`; `command -v nginx` | No Ollama proxy needed (B1); nginx presence recorded (B2 assigns NGINX role) | PASS: actual boundary state established or `NOT ESTABLISHED` recorded |
| SEC-03 | Permissions | `getent passwd ollama`; `getent group ollama`; `stat -c '%U:%G %a %n'` on model-store candidates | No ollama user/group/store (B1) | PASS: ownership/permissions established or absence proven |
| SEC-04 | Secret hygiene | Review all captured evidence pre-retention; `grep -rniE '(token\|passwd\|password\|secret\|api[_-]?key\|bearer\|private.key)' 06-raw-evidence-sanitized/` after capture | No secret values retained | PASS: zero secrets in evidence; any discovery = immediate escalation, value never reproduced |

### PERF — Passive performance assessment

| Test ID | Property | Exact probe | Expected (basis) | Pass rule |
| --- | --- | --- | --- | --- |
| PERF-01 | Passive performance posture | Existing evidence only: SVC-05 journal, ID-03 baseline, MOD-01..03 results; no inference load, no benchmark | No Ollama workload → no performance surface (B1) | PASS: analysis performed and every performance claim labeled `NOT ESTABLISHED` or `CAPACITY INFERENCE — VALIDATION REQUIRED` |

## Coverage summary

29 tests: ID-01..04, HW-01..05, GPU-01..04, SVC-01..05, API-01..03, MOD-01..03, SEC-01..04, PERF-01. Every test gets a status of PASS / FAIL / BLOCKED / NOT RUN with evidence path and limitation in `07-audit-report.md`. No test requires mutation; any test that would require mutation is NOT RUN with justification rather than executed.
