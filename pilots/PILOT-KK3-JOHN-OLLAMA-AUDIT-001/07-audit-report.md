# 07 — John Audit Report: hxs-5 Ollama Read-Only Audit

| Field | Value |
| --- | --- |
| Report ID | `AUDIT-HXS5-OLLAMA-john-initial-20260824-01` |
| Work order | `WO-OLLAMA-AUDIT-HXS5-001` (sha256 `d1883f295b36161c8b9950bb807ce3946d963a261a8b3168d2993b2d08ef672d`) |
| Goal | `GOAL-OLLAMA-AUDIT-HXS5-001` v1 |
| Session ID | `john-initial-20260824-01` (correction session: `initial`) |
| Context hash | `725553195e9c2df97c341fdc08b54c1fcd572c0ada69f9bb376e33f01d8278aa` |
| Target | `hxs-5` (192.168.50.204), verified by local session: `hostname` = `hxs-5`, `ip -4 addr` = `192.168.50.204/24` on `eno1` |
| Live evidence period | 2026-08-24T09:30:19+00:00 → 2026-08-24T09:44:32+00:00 (all times UTC) |

## 1. Executive verdict

**Status: `PASS — AUDIT EVIDENCE PACKAGE COMPLETE`.** Ollama is **entirely absent** from hxs-5, verified unanimously across seven independent identity sources (CLI, deb, snap, install paths, systemd, API, process table). This matches the authoritative 2026-08-12 discovery baseline and the fleet role registry (hxs-5 = Edge/ingress — NGINX). Absence is a finding, not a failure: there is no Ollama runtime, model, listener, or exposure to audit beyond proving absence. 24 of 29 tests PASS, 0 FAIL, 0 BLOCKED, 5 NOT RUN (inapplicable or prohibited-class, each justified). **No host state was changed: mutation count 0.** Top unknowns: no ratified Ollama authority exists for hxs-5 (G1); storage and inference performance are `NOT ESTABLISHED` by design. Decision need D1: owner confirmation whether Ollama should ever run on hxs-5.

## 2. Authority and provenance

| Item | Value | Class |
| --- | --- | --- |
| Goal / work order | `GOAL-OLLAMA-AUDIT-HXS5-001` v1 / `WO-OLLAMA-AUDIT-HXS5-001` | Current explicit instruction |
| Knowledge receipt | `03-john-knowledge-review-receipt.md`, `Task May Proceed: YES`, 2026-08-24T09:35:48+00:00 — preceded all audit probes (first probe 09:41+00:00) | Process gate (SC-01) |
| Knowledge source | `/opt/tkv-local/ollama` — local ext4 path on hxs-5 root filesystem (verified: `findmnt -T /opt/tkv-local` → `/dev/nvme0n1p2 ext4`) | Current knowledge authority |
| hxs-5 baseline | `…/servers/hxs-5/discovery.md` (2026-08-12): no Ollama, no GPU, no CUDA | Historical baseline (knowledge) |
| Role authority | `SERVER-REGISTRY.md`: hxs-5 = `Edge / ingress — NGINX`, READY | Ratified registry |
| Source snapshot identity | Corpus `ollama-main` identified as Ollama `v0.32.11`, commit `39df91c9826b3c0c83677f75cd230d8848d287c3` (prior material, Craig profile); tree itself unpinned (`version.go` = `0.0.0`), no `.git` metadata | Prior material |
| Host-specific version pins | hxs-1: `v0.32.14` (doc-009); hxs-4: `0.32.9` historical (act-014) — **neither applies to hxs-5** | Precedent only |
| hxs-5 Ollama approved version/model/workload | **NOT ESTABLISHED — none exists** (gap G1) | Absence of authority |
| Contradictions | None. Live state matches the 2026-08-12 baseline on every audited axis; drift items are routine (§5, F4) | — |
| Historical precedent | hxs-1/hxs-4 material used as precedent only, never as hxs-5 truth | — |

## 3. Host/runtime snapshot (live, 2026-08-24)

| Axis | Observed value | Evidence |
| --- | --- | --- |
| Hostname / IP | `hxs-5` / `192.168.50.204/24` on `eno1` | `id-01-identity.txt` |
| OS / kernel | Ubuntu 24.04.4 LTS, Linux 7.0.0-30-generic, x86-64 | `id-01-identity.txt` |
| CPU | Intel Core i5-7500 @ 3.40 GHz, 1 socket, 4 cores, 4 threads (no SMT), VT-x | `hw-01-cpu.txt` |
| NUMA | 1 node (node0: CPUs 0-3); `numactl --hardware` captured | `hw-01-cpu.txt` |
| RAM / swap | 31.2 GiB usable (32,739,940 kB); 8.0 GiB file-backed swap | `hw-01-cpu.txt`, `id-01-identity.txt` |
| GPU / accelerators | None discrete; Intel HD Graphics 630 `8086:5912` only; no `nvidia-smi`; no NVIDIA/CUDA | `gpu-01-inventory.txt` |
| Storage | Single KIOXIA 238.5 GB NVMe; ext4 root 232.6 G, 6-7 % used (14.9 G); no dedicated model store; `~/.ollama`, `/usr/share/ollama`, `/var/lib/ollama` all absent | `hw-04-storage.txt` |
| Service identity | No `ollama.service` unit, fragment, drop-in, user, or group | `svc-01-unit.txt`, `api-01-probes.txt` |
| Listener | No `:11434`. Listeners: tcp/22 sshd (all interfaces), tcp+udp/53 systemd-resolved stub (loopback), loopback-only dev tooling (`code-110a328ea5` pids 9054/11437; `MainThread` pids 11468/9169) | `svc-03-listener.txt` |
| Effective Ollama config | Every tunable `NOT SET`: no `OLLAMA_HOST`, `OLLAMA_MODELS`, context, parallelism, queue, FlashAttention, KV-cache, keep-alive, backend, proxy, cloud, debug, or origins configuration anywhere (env files, shell profiles, systemd, process env) | `svc-04-env.txt`, `svc-01-unit.txt` |
| Model inventory / residency | None pulled, none loaded: no binary (`ollama list`/`ollama ps` exit 127), no API (`/api/tags`, `/api/ps` connection refused), no store directories | `id-04-ollama-identities.txt`, `api-01-probes.txt` |
| Ollama journal | `journalctl -u ollama`: no entries | `svc-04-env.txt` |

## 4. Audit test matrix

| Test ID | Property | Expected | Actual | Status | Evidence | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| ID-01 | Target and time | `hxs-5` + `192.168.50.204` local | Both verified 2026-08-24T09:30:19+00:00; local session, no SSH | PASS | `id-01-identity.txt` | None |
| ID-02 | OS/kernel | Ubuntu 24.04.x, x86_64 | Ubuntu 24.04.4 LTS, 7.0.0-30-generic (baseline had -28) | PASS | `id-01-identity.txt` | Kernel drift recorded as observation |
| ID-03 | Resource baseline | ~32 GB RAM, file swap, NVMe root | 31.2 GiB RAM, 8 GiB swap, root 6-7 % used | PASS | `id-01-identity.txt` | Point-in-time snapshot |
| ID-04 | Ollama identities | Unanimous absence (B1) | Absent across CLI/dpkg/snap/paths/systemd/API (exits 1/127/1/2/0-empty/7) | PASS | `id-04-ollama-identities.txt` | Source-vs-installed reconciliation moot: nothing installed |
| HW-01 | CPU topology | i5-7500, 1S/4C/4T | Matches B1 exactly | PASS | `hw-01-cpu.txt` | None |
| HW-02 | NUMA | 1 node | 1 node; `numactl` present, `--hardware` captured | PASS | `hw-01-cpu.txt` | None |
| HW-03 | RAM/swap | ~31 GiB, file swap | 32,739,940 kB RAM; 8,388,604 kB swap | PASS | `hw-01-cpu.txt` | None |
| HW-04 | Model storage | Single NVMe ext4; no model store | Confirmed; store dirs absent; `/opt/tkv` rclone mount noted | PASS | `hw-04-storage.txt` | None |
| HW-05 | Storage performance | No authorized benchmark | No benchmark exists or was run | NOT RUN | `05-command-log.md` (refused table) | Prohibited class (`fio`/writes/cache-drop); conclusion `NOT ESTABLISHED` |
| GPU-01 | Inventory/driver | No NVIDIA; Intel HD 630 | `nvidia-smi` absent (127); lspci shows only `8086:5912` | PASS | `gpu-01-inventory.txt` | None |
| GPU-02 | Topology/processes | Inapplicable | No NVIDIA device exists | NOT RUN | `gpu-01-inventory.txt` | Probe inapplicable; would only reproduce exit 127 |
| GPU-03 | Driver health | No NVRM/Xid/OOM | Kernel journal grep empty | PASS | `gpu-01-inventory.txt` | Current boot journal window only |
| GPU-04 | Isolation | No unit → no config | No Ollama unit exists | NOT RUN | `svc-01-unit.txt` | Inapplicable absent service |
| SVC-01 | Unit/state | No unit (B1) | `status` exit 4, `cat` exit 1, no unit files/units | PASS | `svc-01-unit.txt` | None |
| SVC-02 | Runtime wiring | Empty | `Environment/User/Group/FragmentPath/DropInPaths` all empty | PASS | `svc-01-unit.txt` | None |
| SVC-03 | Listener | No `:11434` | Confirmed via `sudo -n ss -lntp` + UDP map | PASS | `svc-03-listener.txt` | None |
| SVC-04 | Tuning | All `NOT SET` | No `OLLAMA_*` in env files, profiles, process env, systemd | PASS | `svc-04-env.txt` | User-scope scan limited to `hxsa` account; no other users' profiles read |
| SVC-05 | Service health | No entries | `journalctl -u ollama`: no entries | PASS | `svc-04-env.txt` | None |
| API-01 | Local server | Refused (B1) | `curl` exit 7 connection refused | PASS | `id-04-ollama-identities.txt` | None |
| API-02 | Pulled inventory | Unavailable | `/api/tags` refused; `ollama list` 127 | PASS | `api-01-probes.txt` | None |
| API-03 | Loaded inventory | Unavailable | `/api/ps` refused; `ollama ps` 127 | PASS | `api-01-probes.txt` | None |
| MOD-01 | Identity/quantization | No store (B1) | All three store candidates absent | PASS | `hw-04-storage.txt` | Absence proven; no digests applicable |
| MOD-02 | Context alignment | No target exists | No model, no hxs-5 workload target (G1) | NOT RUN | `03-john-knowledge-review-receipt.md` | `NOT ESTABLISHED` — no controlling target |
| MOD-03 | Offload/residency | No loaded models | No server, no models, no GPU | NOT RUN | `api-01-probes.txt` | Residency not claimable; never inferred from inventory |
| SEC-01 | Exposure | No Ollama listener | Port 11434 closed host-wide; nothing proxied | PASS | `svc-03-listener.txt` | Stronger than loopback: nothing to expose |
| SEC-02 | Proxy/auth boundary | None needed | No nginx/haproxy/caddy/traefik running; `nginx` binary absent | PASS | `api-01-probes.txt` | Boundary `NOT ESTABLISHED` by absence; see F5 |
| SEC-03 | Permissions | No ollama identity/store | `getent passwd/group ollama` exit 2; no store dirs | PASS | `api-01-probes.txt` | None |
| SEC-04 | Secret hygiene | Zero secrets retained | Scan clean (2 benign matches: command string, path) | PASS | `sec-04-hygiene.txt` | Pattern-based scan; no secret was ever observed in output |
| PERF-01 | Passive performance | No workload surface | No Ollama workload; journals empty | PASS | `svc-04-env.txt`, §8 | All performance conclusions `NOT ESTABLISHED` |

Totals: **24 PASS / 0 FAIL / 0 BLOCKED / 5 NOT RUN** (29 defined). No mandatory test failed; no stop condition triggered.

## 5. Gap analysis

| Finding | Component | Observed | Controlling target | Gap | Severity | Impact | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Ollama runtime | Absent across 7 identity sources | No ratified Ollama target for hxs-5 (role: NGINX) | None — observed state matches baseline and role | Informational | No Ollama service exists to assess | `id-04-ollama-identities.txt` | High |
| F2 | Authority baseline | No hxs-5 Ollama version/model/workload/exposure authority exists | Registry assigns NGINX, not Ollama | G1: absence of authority, not of compliance | Informational | Any future Ollama commissioning lacks a ratified baseline | `03-john-knowledge-review-receipt.md` | High |
| F3 | Storage performance | Not measured | None authorized | `NOT ESTABLISHED` (benchmark class prohibited) | Informational | Model-store I/O fitness unproven if commissioning is ever desired | `05-command-log.md` | High |
| F4 | Host drift since 2026-08-12 | Kernel -28→-30; root 4.7 %→6-7 %; new loopback-only dev listeners (`code-110a328ea5`, `MainThread`) | B1 discovery record | Routine drift, no contradiction | Low | None for Ollama; listeners are loopback-only | `id-01-identity.txt`, `svc-03-listener.txt` | High |
| F5 | Assigned role implementation | nginx not installed/running on hxs-5 | Registry role `Edge / ingress — NGINX` (READY ≠ configured) | Role implementation not begun — adjacent observation, outside Ollama scope | Informational | None for this audit; relevant to role owners | `api-01-probes.txt` | High |
| F6 | Inference performance | No workload, no telemetry | None | `NOT ESTABLISHED` | Informational | No capacity claim made or implied | `svc-04-env.txt` | High |

## 6. Model/hardware alignment

No models are pulled, loaded, or configured on hxs-5; there is no tag, digest, quantization, context, or residency to assess (MOD-01 absence proven; MOD-02/03 NOT RUN). Hardware alignment facts: CPU-only host (i5-7500, 4C/4T, no AVX-512 class acceleration; VT-x present), 31.2 GiB RAM, no discrete GPU, 205.8 GB free on the sole NVMe device. **Inference, labeled `CAPACITY INFERENCE — VALIDATION REQUIRED`:** a host of this class could serve only small CPU-quantized models at low concurrency; the 18 GB-class artifacts in current HX hxs-1 material are not relevant here. No alignment target exists (G1), so no compliance verdict is possible or claimed.

## 7. Network/security assessment

- **Listener:** port 11434 is closed; no Ollama process exists. Exposure is not merely loopback — it is absent (SEC-01 PASS). Live listeners are SSH (22, all interfaces, consistent with baseline), systemd-resolved stub (53, loopback), and loopback-only dev tooling (F4).
- **Authorized exposure:** no exposure authority exists for Ollama on hxs-5; none is needed while nothing is installed. John profile default (loopback-only absent explicit authority) is recorded for any future commissioning.
- **Proxy/auth boundary:** no reverse proxy runs on this host; boundary state is `NOT ESTABLISHED` by absence (SEC-02). Ollama's lack of native authentication (knowledge: MVP1-CONSTRAINTS) makes this the correct default should Ollama ever be installed.
- **Service identity / permissions:** no `ollama` user, group, or store directory exists (SEC-03 PASS).
- **Origin posture / secret hygiene:** no CORS/origin configuration exists (no service). Retained evidence contains zero secrets (SEC-04 PASS); no secret was observed in any probe output.

## 8. Recommendation-only remediation plan

| ID | Finding | Proposed change | Benefit | Risk | Prerequisite/authority | Validation | Rollback concept | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | F1 (Ollama absent, compliant) | None — no remediation required or proposed | Preserves compliant state | None | n/a | n/a | n/a | None |
| R2 | F2/G1 (no authority baseline) | Record this audit's absence finding in fleet records; if Ollama is ever desired on hxs-5, ratify version pin, model, store path, and loopback bind **before** any installation work order | Prevents unauthorityd drift; gives any future audit a controlling target | None — documentation only | Agent Zero decision (D1) | Registry/knowledge update reviewed at next audit | Revert documentation change | Medium |
| R3 | F6 (performance unknown) | If commissioning is ever authorized, run a separate bounded benchmark pilot (CPU-only, small model, loopback) under its own work order | Capacity becomes measured, not inferred | Load on a 4C host; must be separately authorized | D1 + new work order | Predefined benchmark contract; residency proven via `/api/ps` | Unload model; remove store content | Low (deferred) |

**RECOMMENDATION ONLY — NOT AUTHORIZED FOR EXECUTION**

If D1 ever authorizes Ollama on hxs-5, the loopback-default drop-in pattern (version-matched to the then-ratified Ollama release; environment keys per `envconfig` of the matching source) would be:

```bash
# NOT AUTHORIZED FOR EXECUTION — illustrative only
sudo systemctl edit ollama   # drop-in:
# [Service]
# Environment="OLLAMA_HOST=127.0.0.1:11434"
sudo systemctl daemon-reload && sudo systemctl restart ollama
curl -fsS http://127.0.0.1:11434/api/version   # post-change verification
```

Rationale: Ollama has no native authentication (knowledge: MVP1-CONSTRAINTS #6); John's profile defaults to loopback absent explicit exposure authority. Any such change requires a separate authorized work order with test-first plan; it is `VALIDATION REQUIRED` and out of scope here.

## 9. Remaining gaps / decisions

- **Blockers:** none. No stop condition triggered at any point.
- **Agent Zero decisions needed:**
  - D1: Is Ollama intended ever to run on hxs-5? If yes, commission an authority baseline (version, model, store, bind) before any installation work order. If no, record this audit as the standing conformance evidence.
  - D2 (adjacent, outside Ollama scope): note F5 — the assigned NGINX edge/ingress role is not yet implemented on hxs-5; route to the role owner if relevant.
- **Future validation:** storage benchmark (F3) and CPU-only inference benchmark (F6/R3) only under separate authorized work orders.
- **Deferred work:** none within this audit's scope.
- **Observations:** F4 drift items (kernel, root usage, loopback dev listeners) — informational, no action.

## 10. Validation summary

See `08-john-validation-summary.md` for the complete statement: tests executed 24 PASS / 0 FAIL / 0 BLOCKED / 5 NOT RUN; fact vs inference separation (F6 and §6 capacity note are the only inference-labeled content); mutation status zero; artifact hashes; risks; and exact decisions D1–D2.

Package note: artifacts follow the pilot plan §12 layout exactly (Markdown only); the AGENTS.md dual HTML convention is superseded by that layout for this package.
