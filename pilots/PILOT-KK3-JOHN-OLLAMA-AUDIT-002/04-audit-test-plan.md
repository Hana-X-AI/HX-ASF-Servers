# 04 — Audit Test Plan (hxs-4 Ollama)

| Field | Value |
| --- | --- |
| Session ID | `john-initial-20260824-02` |
| Work order | `WO-OLLAMA-AUDIT-HXS4-001` |
| Correction session | `initial` |
| Target | hxs-4 (192.168.50.203) via SSH `hxsa@192.168.50.203` from hxs-5 |
| Plan written | 2026-08-24, before any audit probe (receipt 03 precedes) |
| Mode | Strictly read-only; no active inference; read-only API endpoints only (`/api/version`, `/api/tags`, `/api/ps`) |

Expected results derive from the commissioned baseline (receipt 03, section 2):
Ollama 0.32.9; `qwen3.5:9b-q4_K_M` digest `6488c96fa5fa`; loopback `127.0.0.1:11434`;
RTX 5060 (UUID `GPU-cc758e31-d23b-3c53-bee6-dae3299a6f11`) isolated via
`CUDA_VISIBLE_DEVICES` + `GGML_VK_VISIBLE_DEVICES=999` + `OLLAMA_VULKAN=0`; RTX 5060 Ti
(UUID `GPU-11b1a30e-8c11-001b-7b8b-7b1e15ab6978`) reserved and invisible to Ollama;
driver 580.173.02 / CUDA 13.0; host i7-14700F 20c/28t, 32 GB DDR5, Ubuntu 24.04.

Statuses allowed: `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`. A failed mandatory test stops
the session per base plan §16.

## ID — identity and host baseline

| Test ID | Property | Probe (sanitized) | Expected result | Pass rule |
| --- | --- | --- | --- | --- |
| ID-01 | Target and time | `hostname`; `date --iso-8601=seconds`; `ip -4 addr show \| grep 192.168.50.203`; `hostnamectl` | hostname `hxs-4`; address 192.168.50.203 present on a local interface; clock plausible | hostname AND address match; any mismatch aborts session (BLOCKED) |
| ID-02 | OS/kernel | `cat /etc/os-release`; `uname -a` | Ubuntu 24.04 LTS; x86_64 kernel | recorded verbatim; material drift from registry noted as finding, not auto-fail |
| ID-03 | Resource baseline | `uptime`; `free -h`; `swapon --show`; `df -hT` | ~31 GiB RAM; swap present (file-backed per discovery); root fs on 931.5 GB NVMe | snapshot captured; anomalies flagged |
| ID-04 | Ollama identities | `command -v ollama`; `ollama --version`; systemd `ExecStart` (SVC-02); `/api/version` (API-01) | CLI `/usr/local/bin/ollama` 0.32.9; ExecStart binary 0.32.9; server 0.32.9; corpus source v0.32.11 declared NOT version-matched | all three live identities agree at 0.32.9 AND source mismatch is reported, not hidden |

## HW — CPU, memory, NUMA, storage

| Test ID | Property | Probe | Expected result | Pass rule |
| --- | --- | --- | --- | --- |
| HW-01 | CPU topology | `lscpu` | i7-14700F; 1 socket; 20 cores; 28 threads; x86_64 | matches registry |
| HW-02 | NUMA | `lscpu`; `numactl --hardware` only if installed | 1 NUMA node | matches registry; `numactl` absent = NOT RUN for that sub-probe, install nothing |
| HW-03 | RAM/swap | `free -h`; `swapon --show`; `grep -E 'MemTotal|SwapTotal' /proc/meminfo` | ~32 GB total; swap per discovery | snapshot captured |
| HW-04 | Model storage | effective `OLLAMA_MODELS` (from SVC-02 env; default `/usr/share/ollama/.ollama/models`); `findmnt -T <path>`; `lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,ROTA,MODEL`; `df -hT <path>` | model store on root NVMe ext4; adequate free space for 6.6 GB artifact | path, medium, fs, capacity all recorded |
| HW-05 | Storage performance | none authorized (no fio/writes) | `NOT ESTABLISHED` unless authoritative existing benchmark exists | status `NOT RUN` with explicit rationale, no probe executed |

## GPU — accelerator

| Test ID | Property | Probe | Expected result | Pass rule |
| --- | --- | --- | --- | --- |
| GPU-01 | Inventory/driver | `nvidia-smi -L`; `nvidia-smi` | RTX 5060 Ti 16311 MiB + RTX 5060 8151 MiB; driver 580.173.02 / CUDA 13.0 | both GPUs enumerated with expected VRAM; driver recorded |
| GPU-02 | Topology/processes | `nvidia-smi topo -m`; `nvidia-smi --query-compute-apps=pid,name,used_memory --format=csv` | topology recorded; any ollama runner process lands ONLY on the RTX 5060 | recorded; runner on excluded GPU = FAIL (isolation breach) |
| GPU-03 | Driver health | `journalctl -k --no-pager \| grep -Ei 'NVRM\|Xid\|nvidia\|oom' \| tail -100`; bounded `journalctl -u ollama` | no fresh Xid/NVRM/OOM since commissioning; historical 2026-08-14 wedge incident is known | no unexplained driver errors; journal access denial recorded as BLOCKED-for-probe with fallback to `dmesg` if permitted |
| GPU-04 | Isolation | effective service env (SVC-02): `CUDA_VISIBLE_DEVICES`, `OLLAMA_VULKAN`, `GGML_VK_VISIBLE_DEVICES` | `CUDA_VISIBLE_DEVICES=GPU-cc758e31-d23b-3c53-bee6-dae3299a6f11`; `OLLAMA_VULKAN=0`; `GGML_VK_VISIBLE_DEVICES=999` | all three present with expected values; any deviation = FAIL (acceptance condition, iss-013) |

## SVC — service and effective configuration

| Test ID | Property | Probe | Expected result | Pass rule |
| --- | --- | --- | --- | --- |
| SVC-01 | Unit/state | `systemctl status ollama --no-pager`; `systemctl cat ollama` | active (running), enabled; fragment + drop-ins identified | state and unit files captured |
| SVC-02 | Runtime wiring | `systemctl show ollama -p ExecStart -p User -p Group -p Environment -p FragmentPath -p DropInPaths` | `ExecStart=/usr/local/bin/ollama serve`; service user `ollama`; env includes isolation vars | effective values captured and reconciled with ID-04/GPU-04 |
| SVC-03 | Listener | `ss -lnt`; `ss -lntp` (best-effort, no sudo) | TCP 127.0.0.1:11434 listening, owned by ollama; no 0.0.0.0:11434 | loopback-only confirmed |
| SVC-04 | Tuning | SVC-02 environment; unit drop-ins | parallelism, max loaded models, queue, context, FlashAttention, KV cache, keep-alive, debug, origins: value or `NOT SET` | each lever reported with source; no expectation beyond baseline (FlashAttention/KV-cache experiment reverted 2026-08-14 → expect NOT SET) |
| SVC-05 | Service health | `journalctl -u ollama -n 300 --no-pager` (bounded) | no fresh errors/OOM/fallback; request content sanitized | captured; denial handled per GPU-03 rule |

## API / MOD — API and models (read-only endpoints only)

| Test ID | Property | Probe | Expected result | Pass rule |
| --- | --- | --- | --- | --- |
| API-01 | Local server | `curl -fsS --connect-timeout 2 --max-time 10 http://127.0.0.1:11434/api/version` | HTTP 200, `{"version":"0.32.9"}` | body matches 0.32.9 |
| API-02 | Pulled inventory | `curl … /api/tags`; `ollama list` | includes `qwen3.5:9b-q4_K_M` digest `6488c96fa5fa`; record full inventory | commissioned model present with matching digest; extra/missing models recorded as findings |
| API-03 | Loaded inventory | `curl … /api/ps`; `ollama ps` | loaded models with processor split and context; empty = model not resident at audit time | captured verbatim; empty is a state, not a failure |
| MOD-01 | Identity/quantization | API-02 data vs baseline | Q4_K_M, ~6.6 GB artifact (6,594,474,236 B), 9.7B | digest + quantization + size reconcile |
| MOD-02 | Context alignment | API-03 context vs acceptance baseline | any loaded context ≤ 65536; full-GPU residency ceiling 16384 known | reported against acceptance conditions |
| MOD-03 | Offload/residency | API-03 processor field; GPU-02 process query | if loaded: 100% GPU at ≤16384, split above; if not loaded: residency `NOT ESTABLISHED` at audit time (read-only cannot load) | residency stated only from direct evidence, never inferred from `ollama list` |

## SEC — network and security

| Test ID | Property | Probe | Expected result | Pass rule |
| --- | --- | --- | --- | --- |
| SEC-01 | Exposure | SVC-03 listener + effective `OLLAMA_HOST` vs owner ruling (loopback; OmniRoute-only remote path, mechanism undefined) | loopback-only = compliant | any non-loopback bind = FAIL and escalation-worthy finding |
| SEC-02 | Proxy/auth boundary | listener evidence; check for nginx/haproxy/omniroute proxy config referencing 11434 (read-only fs inspection best-effort) | `NOT ESTABLISHED` expected — acceptance record states mechanism undefined | state reported; absence is compliant-with-ruling, recorded as open decision |
| SEC-03 | Permissions | `stat -c '%U:%G %a %n' <model store> <store>/manifests <store>/blobs`; `namei -l <model store>`; service identity from SVC-02 | store owned by service user (`ollama`), not world-writable | ownership/mode recorded; anomalies flagged |
| SEC-04 | Secret hygiene | sanitized env/unit/journal inspection (from SVC-02, SVC-05) | no secret values retained in evidence; `REDACTED` applied | any discovered secret escalated without reproducing it |

## PERF — passive performance assessment (no new load)

| Test ID | Property | Probe | Expected result | Pass rule |
| --- | --- | --- | --- | --- |
| PERF-01 | Passive performance posture | synthesis of GPU-01, API-03, SVC-05 journals vs 2026-08-14 measured ladder (16384 full-GPU; ~28 tok/s at 65536 real generation) | no evidence of regression (fallback, OOM, queueing) in passive data | conclusions limited to `VERIFIED from baseline` / `NOT ESTABLISHED` / `CAPACITY INFERENCE — VALIDATION REQUIRED`; zero new inference |

## Explicitly not run

- Any `ollama pull|rm|create|cp|run|stop`, `/api/generate`, `/api/chat` — prohibited.
- `fio`, stress, cache-dropping, load generation — prohibited.
- `systemctl` state changes, kill/pkill, reboot, driver/GPU reset — prohibited.
- HW-05 active benchmark — `NOT RUN` by design.
