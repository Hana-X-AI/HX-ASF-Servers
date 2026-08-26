# 07 — Esme (john): M4 Ollama Install + Exact-Tag Pull + Identity Freeze + D5-Budget systemd (hxs-2)

`[TASK COMPLETE — EVIDENCE ATTACHED]`

| Field | Value |
| --- | --- |
| Report ID | ESME-HXS2-M4-INSTALL-001 |
| Task ID | WO-HXS2-JOHN-M4-001 (`PILOT-HXS2-CODERX-BACKEND-001`, milestone M4) |
| Agent | john / Esme (profile `agents/john/profile.md`), session `john-m4-20260826-01` |
| Target host | `hxs-2` (192.168.50.201), Ubuntu 24.04.4 LTS (noble), kernel 7.0.0-30-generic, x86-64 |
| Executed from | `hxs-5` (192.168.50.204) via SSH `hxsa@192.168.50.201` — askpass helper READS the credential-record table row (`ssh-info.md` "SSH password" row) AT EXECUTION TIME ONLY; no extracted copy ever existed; helper deleted at task end |
| Host-key check | STRICT — pinned ED25519 `SHA256:b2qlMQz496nUbuZKJu3wwmR0QY/EmN0KQtW4rM2HDcQ` (rick M1 F-05), verified against the known_hosts entry before first use; `StrictHostKeyChecking=yes` on every connection |
| Window (UTC) | 2026-08-26T04:10Z → 04:52Z (first target mutation 04:30Z; final verification poll 04:52:09Z) |
| Ollama | **0.32.15** (binary == server; pinned this session — see §5.1) |
| Frozen model identity | `mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M` @ digest **`ca661423d6b51ebeaca999f22cfc0f30c0851b2a6f328b2737bd8cb6eb90c1df`** |
| Working alias | `hx-qwen3.6-coderx:latest` @ digest **`1d297a6a093f7858da9a96e39950b6e7581118708b6121182a811a1f3bf21ba5`** (bound to the frozen artifact — §5.5) |
| GPUs | 2× RTX 5060 Ti 16,311 MiB, driver 580.173.02 (rick's plane, untouched) |

Evidence labels: **FACT** (live host output) / **AUTHORITY** (owner decision, work order, governance) / **UPSTREAM** (publisher/registry statement) / **INFERENCE** / **RECORD** (decision or observation).
All secrets excluded; the SSH credential was never printed, logged, or stored (§12 sanitization).

---

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path /opt/tkv-local/ollama resolves locally here); target hxs-2 (192.168.50.201)
Source: /opt/tkv-local/ollama + HX-ASF-Servers controlling docs + owner-docs CoderX reference
Reviewed At: 2026-08-26T04:10Z → 04:30Z
Relevant Files:
  - agents/john/profile.md; agents/ roster = carol, john, kimi-k3, rick (all current teammates)
  - pilots/PILOT-HXS2-CODERX-BACKEND-001/01-state-log.md (rows 1-7: M0/D1-D8, M1 13/13, Gate 0 PASSED, M4 commissioned)
  - pilots/PILOT-HXS2-CODERX-BACKEND-001/04-rick-hxs2-os-readiness.md (M1 evidence; F-05 pinned host key; identity corroborators)
  - goals/2026-08-26-hxs2-qwen36-coderx-backend.md (D1-D8; SC table; stop conditions)
  - servers/BLUEPRINT-llm-server.md (§2 OS plane, §3 service plane + preload contract, §5 exposure plane, §8 consumer contract)
  - servers/AGENTS.md + repo AGENTS.md (records contract; no-host-firewall owner rule)
  - pilots/PILOT-HX1-OLLAMA-QWEN27B-001/12-esme (install/pull/identity/alias pattern), 35-esme (D5 budget contract), 39-esme (OLLAMA_HOST=0.0.0.0 precedent)
  - /opt/tkv-local/ollama/ollama-main/scripts/install.sh (sha256 25f64b81…82c9f — reviewed installer baseline)
  - /opt/tkv-local/ollama/ollama-main/docs/linux.mdx (unit template, drop-in override, uninstall procedure)
  - /opt/tkv-local/servers/hxs-2/discovery.md (as-found identity cross-check)
  - CoderX knowledge reference §3 (identity), §5 (vision artifact), §12.2 (mandatory identity evidence), §17 (residency), §18 (CX-R01..R13)
Authority/Version Identified:
  - Ollama PIN = 0.32.15 (blueprint host hxs-1's proven version; installer OLLAMA_VERSION pin, install.sh line 42).
    Upstream latest observed = v0.33.0 (GitHub releases API, 2026-08-26T04:21Z) — deliberately NOT taken
    (brand-new minor, zero HX evidence; both LLM hosts kept on one version). RECORD F-J4.
  - Installer downloaded 2026-08-26 from https://ollama.com/install.sh = sha256 25f64b81…82c9f,
    BYTE-IDENTICAL to the TKV-reviewed baseline → authenticity established (FACT).
  - Model: mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M (owner D3). Read-only registry probes (FACT):
    manifest digest ca661423d6b51ebeaca999f22cfc0f30c0851b2a6f328b2737bd8cb6eb90c1df (prefix MATCHES the
    reference observation ca661423d6b5 — pre-pull cross-check PASS); config family qwen35moe, 26.2B, Q4_K_M,
    renderer/parser qwen3.5; layers: model 16,057,050,592 B + projector 899,283,072 B + template 13 B +
    params 132 B; baked params verbatim {"draft_num_predict":3,"min_p":0,"num_ctx":32768,
    "presence_penalty":1.5,"repeat_penalty":1,"temperature":1,"top_k":20,"top_p":0.95}.
Applicable Tests/Runbooks: profile §7.1/§7.2; reference §12.2 capture set + §13.1; 12-esme install order;
  35-esme budget arithmetic; 39-esme exposure mechanics
Contradictions or Gaps:
  - TKV source snapshot v0.32.11 < install target 0.32.15 (qwen35-family models require a ≥0.32.12-class
    runtime — hxs-1 F-E7 precedent: installing newer than the snapshot is required, recorded openly).
  - Upstream latest (0.33.0) ≠ blueprint pin (0.32.15) — resolved to the blueprint pin (F-J4).
  - No live/knowledge conflicts; hxs-2 live state re-verified at baseline (packet: "re-verify at start").
Task May Proceed: YES
```

## 2. Test plan and results (plan recorded before first mutation, 04:30Z)

| ID | Property | Expected | Result |
| --- | --- | --- | --- |
| T0a | Session + target identity | hxs-2/.201; machine-id/UUID/MAC match discovery; sudo -n OK | **PASS** (§3) |
| T0b | Host-key pin strict check | == rick M1 F-05 fingerprint | **PASS** (header; pre-verified 04:23Z) |
| T1 | Pre-install state | no binary/user/unit/listener/package | **PASS** (§3) |
| T2 | Baseline health | matches rick M1; Xid=0 | **PASS** (§3) |
| T3 | Installer authenticity | sha256 == TKV reviewed baseline | **PASS** (§5.1) |
| T4 | Install + pin 0.32.15 | binary==server==0.32.15; system user; upstream unit; no driver/apt authority | **PASS** (§5.2) |
| T5 | Default bind pre-drop-in | loopback-only; LAN refused | **PASS** (§5.3) |
| T6 | GPU visible to Ollama | BOTH 5060 Ti, library=CUDA | **PASS** (§5.3) |
| T7 | Pull exact tag | success; blobs == registry manifest | **PASS** (§5.4, 3m22s) |
| T8 | Identity freeze §12.2 | full capture; digest verbatim; family qwen35moe; cross-check ca661423d6b5 | **PASS** (§5.4) |
| T9 | Alias binding | FROM-only Modelfile; blob-set equality; baked params preserved | **PASS** (§5.5) |
| T10 | hx2.conf drop-in | exactly the 4 mandated env values; wildcard bind incl. loopback | **PASS** (§5.6) |
| T11 | Preload script+unit | shellcheck clean; TimeoutStartUSec=10min | **PASS** (§5.7, §6) |
| T12 | Preload first run | alias resident; exact digest; 100% VRAM; both GPUs; ctx 32768; Forever | **PASS** (§6, 75 s cold) |
| T13 | Enablement | both units enabled | **PASS** (§6) |
| T14 | Journal health | no errors; Xid=0; OOM=0; NRestarts=0 | **PASS** (§6; F-J1 watchdog class recorded) |
| T15 | Reachability | 127.0.0.1 AND hxs-5→192.168.50.201:11434 /api/version | **PASS** (§7) |
| T16 | Post-state hygiene | 0 failed units; no reboot; swap 0; storage delta recorded | **PASS** (§6) |

**17/17 PASS; 0 FAIL; 0 BLOCKED; 0 NOT RUN.** Stop conditions (wrong artifact family, digest ambiguity, GPU not visible, service failure after bounded retry, any Xid): **none hit**. One bounded correction used (F-J3, my own install sequencing; no service impact). One corrected pre-flight failure (F-J2, credential markdown unwrap; no target contact beyond one refused auth).

## 3. Identity and pre-change baseline (FACT, 04:28:24Z → 04:29:08Z)

- **Identity (T0a):** `hostname` → `hxs-2`; `SSH_CONNECTION` → `192.168.50.204 … 192.168.50.201 22` (hxs-5 → hxs-2); machine-id `0c249b9ad97c48d0b7d33693d120a576`; system UUID `038d0240-045c-05e7-9006-e90700080009`; eno1 `192.168.50.201/24` MAC `40:8d:5c:e7:90:d5` — all match the 2026-08-12 discovery record and rick M1. `sudo -n true` → OK.
- **Pre-install state (T1):** `command -v ollama` empty; `systemctl status ollama` "could not be found"; `id ollama` no such user; `/usr/share/ollama` absent; `dpkg -l | grep -i ollama` count 0; no `:11434` listener. **Ollama was NOT installed** (packet expectation re-verified live).
- **Health (T2):** Ubuntu 24.04.4 LTS noble; kernel 7.0.0-30-generic; uptime 13:18 continuous (no reboot this session, ever — final poll 13:38+); RAM 62 Gi (1.1 Gi used); swap 8 Gi, 0 B used; root ext4 3.6 T, 14 G used, **3.4 T free (1%)**; GPUs `GPU-7a7239a3-08d5-6c44-b847-2118ce93b53c` (0) and `GPU-cdfbf3f2-f38a-8927-41f9-c8dcbd278249` (1), both RTX 5060 Ti 16,311 MiB, 0 MiB used, driver 580.173.02 — exact match to rick M1; 0 failed units; listeners `:22` + loopback stub DNS only; **`NVRM: Xid` count = 0 across all retained boots**.

## 4. Implementation record

### 5.1 Installer review and version pin (T3; profile §7.1)

- FACT: `curl -fsSL https://ollama.com/install.sh` (2026-08-26T04:21Z) → sha256 `25f64b810b947145095956533e1bdf56eacea2673c55a7e586be4515fc882c9f` (455 lines), **byte-identical** to TKV `ollama-main/scripts/install.sh` (same sha256; `diff -q` clean) — the same reviewed baseline hxs-1 M4 executed. Served over HTTPS from ollama.com. **AUTHENTICITY ESTABLISHED.** Never blind-piped: transferred as a file, hash-verified on both sides, then executed.
- FACT (review stands, same bytes as hxs-1 M4 §4.1): on a host with working `nvidia-smi` the script (a) extracts `ollama-linux-amd64.tar.zst` to `/usr/local`; (b) creates system user `ollama`, adds it to `render`+`video`, adds the invoking user to `ollama`; (c) writes `/etc/systemd/system/ollama.service`, enables + starts it; (d) exits 0 at "NVIDIA GPU installed." **before** all CUDA-driver/DKMS/apt logic. The installer cannot become GPU-driver or OS-package authority here.
- RECORD (F-J4, the pin): upstream latest is **v0.33.0** (GitHub releases API 04:21Z) — deliberately **not** taken. Pin = **0.32.15**, the blueprint host's fully-validated version (hxs-1 M4→M8 evidence chain, one day old), via the installer's supported `OLLAMA_VERSION` mechanism (install.sh line 42: `VER_PARAM="${OLLAMA_VERSION:+?version=$OLLAMA_VERSION}"`). Rationale: blueprint consistency (one version across both LLM hosts), brand-new-minor conservatism, and the frozen model artifact predates 0.33.0. Upgrade path = a future versioned work order. The model's family runtime floor (≥0.32.12 class) is satisfied.

### 5.2 Install result (T4; FACT, 04:30:31Z → 04:31:00Z)

- `OLLAMA_VERSION=0.32.15 sh /tmp/ollama-install-reviewed.sh` → `INSTALL_RC=0`; output ended `>>> NVIDIA GPU installed.` (driver logic confirmed skipped; zero apt/dkms/modprobe activity).
- `ollama version is 0.32.15`; `/api/version` → `{"version":"0.32.15"}` (**binary == server == pin**). Binary `/usr/local/bin/ollama`.
- `id ollama` → `uid=999(ollama) gid=988(ollama) groups=988(ollama),44(video),993(render)`; home `/usr/share/ollama` (`drwxr-x--- ollama:ollama`). Invoking user `hxsa` added to group `ollama` (installer default).
- Unit: upstream default `/etc/systemd/system/ollama.service` (`ExecStart=/usr/local/bin/ollama serve`, `User/Group=ollama`, `Restart=always`, `RestartSec=3`, `WantedBy=default.target`), **enabled + active**. sha256 `11758d469d3f103e53a9612a8ffcb3a3e61834c994c08d412bb051f3c827dbd3`.

### 5.3 Default bind + GPU visibility BEFORE any change (T5, T6; FACT, 04:31Z)

- `ss -lntp`: `LISTEN 127.0.0.1:11434` only; `curl http://192.168.50.201:11434/api/version` → connection refused (0 ms). Upstream default is loopback-only; the LAN bind arrives only via the authorized hx2.conf (§5.6).
- Journal: `Listening on 127.0.0.1:11434 (version 0.32.15)`; **both** GPUs discovered — `inference compute id=0/1 library=CUDA compute=12.0 "NVIDIA GeForce RTX 5060 Ti" driver=13.0 pci_id=0000:02:00.0/0000:03:00.0 total 15.5 GiB` (discovery 04:30:11→04:31:00 ≈ 49 s, within the default start timeout). Stop condition "GPU not visible to Ollama" cleared.

### 5.4 Pull and identity freeze (T7, T8; FACT, 04:31:36Z → 04:34:59Z)

- `ollama pull mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M` → success in **3m22.455s** (~113 MB/s); client verified the sha256 digest during pull; blobs fetched = exactly the registry manifest's layers (`ce2f69655c94…` 16 GB model, `8d81165570ee…` 899 MB projector). Nothing else was pulled; no other tag exists on the host.
- **FROZEN IDENTITY (the local full digest is authoritative):**

| Field | Value (FACT unless labeled) |
| --- | --- |
| Full name + explicit tag | `mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M` |
| **Local digest (FROZEN)** | **`ca661423d6b51ebeaca999f22cfc0f30c0851b2a6f328b2737bd8cb6eb90c1df`** |
| Reference prefix cross-check | `ca661423d6b5` — **MATCH** (registry state has not advanced since the reference observation) |
| Size | 16,956,334,345 B (16,057,050,592 LM + 899,283,072 projector + 13 template + 132 params + 536 config — fully accounted) |
| modified_at | 2026-08-26T04:34:59Z |
| Format / family | `gguf` / `qwen35moe` (families: `[qwen35moe]`) — **correct artifact family** |
| Parameter size | 26.2B (`general.parameter_count` 26,213,016,704; size label `27B-A3B`) |
| Quantization | `Q4_K_M` (file_type 15; output tensor Q6_K; imatrix-quantized, 128 chunks/510 entries) |
| Model max context | 262,144 (`qwen35moe.context_length`); **baked operating ctx `num_ctx 32768`** |
| Capabilities | `completion`, `vision`, `tools`, `thinking` |
| Architecture detail | MoE: 184 experts (`expert_count`), **top-8 routing** (`expert_used_count` 8 — the CoderX checkpoint, not the top-10 sibling); 41 blocks; `nextn_predict_layers` 1 (MTP); hybrid attention (`full_attention_interval` 4) + SSM (inner 4096, state 128, groups 16) |
| Template | `{{ .Prompt }}` (13-byte artifact template; chat handled by the built-in renderer) |
| Renderer / Parser | `qwen3.5` / `qwen3.5` |
| Baked parameters (verbatim) | `temperature 1`, `top_k 20`, `top_p 0.95`, `draft_num_predict 3`, `min_p 0`, `num_ctx 32768`, `presence_penalty 1.5`, `repeat_penalty 1` — **preserved; zero overrides added anywhere** |
| **Projector identity** | `clip`, `general.name "Qwen3.6 27B A3B Coder"`, finetune `27b-Coder`, type `mmproj`, **446,571,248 params (~447M)**, F16 (file_type 1), `qwen3vl_merger`, vision embed 1152, projection 2048, image 768/patch 16, 27 blocks — the Coder-family mmproj attached at GGUF packaging, exactly per reference §5 |
| License | **UPSTREAM:** `Apache-2.0` ("Apache-2.0 · research checkpoint." — ollama.com model page, 04:37Z; matches reference §3). RECORD (F-J5): the pulled manifest carries **no license blob** — `/api/show` has no license field; recorded as publisher-declared, not local-artifact fact |
| Ollama version / host / GPU / OS | 0.32.15 (binary==server) / hxs-2 / 2× RTX 5060 Ti / Ubuntu 24.04.4, kernel 7.0.0-30 (§3) |

- `/api/show` full JSON (753 tensors, `model_info`, `projector_info`, modelfile, parameters, template) captured to session evidence `08-identity-apishow.json` (retained transiently; the load-bearing fields are inlined above).
- Storage delta (D1, root ext4): `/` 14 G → 32 G used; models dir `16G`; free still 3.4 T (1%). Path `/usr/share/ollama/.ollama/models` owned `ollama:ollama`.

### 5.5 Alias `hx-qwen3.6-coderx` — bound to the frozen digest (T9; FACT, 04:40:53Z)

- Modelfile (sha256 `39c7fcf835ceda57d1a9ea903ddaa752368b3221415b9e3c049f4fa2dba18113`, identical hxs-5 copy ↔ hxs-2 `/tmp/esme-m4/Modelfile`) — **FROM only; NO PARAMETER/SYSTEM/TEMPLATE lines** (native-sampling baseline; baked tag params preserved):

```dockerfile
# hx-qwen3.6-coderx — WO-HXS2-JOHN-M4-001 (PILOT-HXS2-CODERX-BACKEND-001, M4)
# Working alias bound to the frozen CoderX artifact:
#   mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M
#   digest ca661423d6b51ebeaca999f22cfc0f30c0851b2a6f328b2737bd8cb6eb90c1df
# FROM only — NO PARAMETER/SYSTEM/TEMPLATE lines: the baked tag parameters
# (num_ctx 32768, draft_num_predict 3, native sampling temp 1 / top_p 0.95 /
# top_k 20 / min_p 0 / repeat 1 / presence 1.5) are preserved unchanged
# (native-sampling baseline; M6 ladder owns context changes).
FROM mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M
```

- `ollama create hx-qwen3.6-coderx` → success; the create log shows **all four frozen layers reused** (`ce2f69655c94…`, `8d81165570ee…`, `b507b9c2f6ca…`, `d75e3524b9de…`).
- **Alias digest (FROZEN): `1d297a6a093f7858da9a96e39950b6e7581118708b6121182a811a1f3bf21ba5`** (a new manifest, as expected).
- **Binding proof, three independent ways (FACT):**
  1. Manifest layer comparison (manifests read via `sudo -n cat`, compared locally): alias layers == base layers, **ordered AND set-equal** — the alias is content-addressed to the frozen blobs; it cannot resolve to anything else and does not follow the upstream tag if re-pulled.
  2. `ollama show hx-qwen3.6-coderx` == base identity field-for-field (architecture, 26.2B, Q4_K_M, capabilities, projector, **baked parameters verbatim** — zero added parameters).
  3. Alias config blob `0e1644d922…` carries identical identity metadata (family `qwen35moe`, 26.2B, Q4_K_M, renderer/parser qwen3.5).
- Manifest sha256s on disk: base `ca661423d6b5…c1df` (== its digest, as content-addressing requires); alias `1d297a6a093f…21ba5`.

### 5.6 Service plane — hx2.conf drop-in (T10; FACT, 04:43:48Z install → 04:44:34Z restart)

`/etc/systemd/system/ollama.service.d/hx2.conf` (root:root 0644, sha256 `0918415897ac871adbff367a9ec381e4da77e0ef294bd0313a95b2498d68c35b`) — exactly the four mandated values, nothing else:

```ini
# hxs-2 CoderX service plane — WO-HXS2-JOHN-M4-001 (blueprint §3/§5; owner D2).
# OLLAMA_HOST=0.0.0.0 binds the wildcard address (default port 11434 per
# envconfig Host()); loopback is preserved — the preload script and fixtures
# use 127.0.0.1. The private 192.168.50.0/24 LAN itself is the boundary:
# no host firewall anywhere (owner rule 2026-08-26). Admission control:
# exactly one loaded model, one parallel request. Cloud features disabled.
# Native-sampling baseline: NO context or sampling variables are set here —
# the baked tag parameters (num_ctx 32768, draft_num_predict 3) govern;
# the M6 ladder owns any context change.
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_NO_CLOUD=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
```

Effective state after `daemon-reload` + `systemctl restart ollama` (04:44:34Z; only ollama.service restarted; no reboot):

- `systemctl show ollama`: `Environment=PATH=… OLLAMA_HOST=0.0.0.0 OLLAMA_NO_CLOUD=1 OLLAMA_NUM_PARALLEL=1 OLLAMA_MAX_LOADED_MODELS=1`; `DropInPaths=/etc/systemd/system/ollama.service.d/hx2.conf`; `NRestarts=0`; active/running.
- Server startup log (FACT): `OLLAMA_HOST:http://0.0.0.0:11434`, **`Ollama cloud disabled: true`**, `OLLAMA_MAX_LOADED_MODELS:1`, `OLLAMA_NUM_PARALLEL:1`, `OLLAMA_CONTEXT_LENGTH:0` (server default — the baked tag `num_ctx 32768` governs per model, proven by `/api/ps context_length 32768`), `OLLAMA_KEEP_ALIVE:5m0s` (service default — the preload's request-level `keep_alive:-1` pins Forever, proven by `expires_at` year 2318); `Listening on [::]:11434`; both GPUs re-discovered (`inference compute` CUDA0/CUDA1, 04:45:22).
- Bind: `ss` → `*:11434` (wildcard dual-stack; loopback preserved — §7 matrix). RECORD: API answered on probe attempt 5 (~40 s post-restart, CUDA discovery window — hxs-1 F-E1 transient class, recorded, expected).

### 5.7 Preload script + unit — D5 budgets from day one (T11; FACT)

`/usr/local/libexec/hx-ollama-preload` (root:root 0755, sha256 `ab1c8010c3a498736b9f8532f7b664faf7afef0255fddc50b4762cff87fe86f9`) — the 35-esme bounded-phase contract, pinned to alias + frozen digest:

```sh
#!/bin/sh
# hx-ollama-preload — PILOT-HXS2-CODERX-BACKEND-001 (WO-HXS2-JOHN-M4-001)
# Loads the exact pilot model with keep_alive=-1, then asserts /api/ps
# residency of the exact alias AND its frozen digest. D5-conformant bounded
# phases (35-esme budget contract):
#   Phase 1 API wait: at most 30 fast probes of /api/version
#     (connect-timeout 2 s, max-time 5 s, sleep 2 s between probes);
#     worst case 30*5 + 29*2 = 208 s.
#   Phase 2 model load: ONE attempt, --max-time 300 (cold dual-GPU load of
#     the 16.9 GB artifact is expected in tens of seconds; 300 s is a
#     generous margin); NO retry — a timeout must fail the unit, not
#     extend the budget.
#   Phase 3 assertion: one /api/ps read, --max-time 30; the exact alias
#     name AND the frozen digest must both be present.
# Script worst case: 208 + 300 + 30 = 538 s, below TimeoutStartSec=600 in
# ollama-preload.service, itself 300 s under the 900 s D5 recovery SLO.
# On any exhaustion or failure it FAILS (alert path); it never loops.
# No credentials are embedded or required (loopback-only API).
set -eu

MODEL="hx-qwen3.6-coderx"
DIGEST="1d297a6a093f7858da9a96e39950b6e7581118708b6121182a811a1f3bf21ba5"
API="http://127.0.0.1:11434"
API_PROBES=30

# Phase 1: bounded fast probes until the API answers (no side effects).
tries=0
until curl -fsS --connect-timeout 2 --max-time 5 "$API/api/version" -o /dev/null 2>&1; do
  tries=$((tries + 1))
  if [ "$tries" -ge "$API_PROBES" ]; then
    echo "hx-ollama-preload: FAIL - $API not ready after $API_PROBES bounded probes" >&2
    exit 1
  fi
  sleep 2
done

# Phase 2: single bounded load request; empty prompt only loads and pins the model.
if ! curl -fsS --connect-timeout 3 --max-time 300 \
  "$API/api/generate" \
  -H 'Content-Type: application/json' \
  -d "{\"model\":\"$MODEL\",\"prompt\":\"\",\"stream\":false,\"keep_alive\":-1}" \
  -o /dev/null; then
  echo "hx-ollama-preload: FAIL - single-attempt load of $MODEL failed (--max-time 300)" >&2
  exit 1
fi

# Phase 3: readiness assertion — exact alias AND frozen digest must be resident.
ps_json=$(curl -fsS --connect-timeout 3 --max-time 30 "$API/api/ps")
printf '%s' "$ps_json" | grep -q "\"name\":\"$MODEL:" || {
  echo "hx-ollama-preload: FAIL - $MODEL not resident in /api/ps after bounded load" >&2
  exit 1
}
printf '%s' "$ps_json" | grep -q "\"digest\":\"$DIGEST\"" || {
  echo "hx-ollama-preload: FAIL - resident digest is not the frozen $DIGEST" >&2
  exit 1
}
echo "hx-ollama-preload: OK - $MODEL resident (digest $DIGEST)"
```

`/etc/systemd/system/ollama-preload.service` (root:root 0644, sha256 `bf3cc6948f344a1a74307830b0bee31af6603fd24b3615cd7c13e036c3e11f57`):

```ini
[Unit]
Description=Ollama preload — pin hx-qwen3.6-coderx resident (keep_alive=-1)
After=network-online.target ollama.service
Requires=ollama.service

[Service]
Type=oneshot
ExecStart=/usr/local/libexec/hx-ollama-preload
RemainAfterExit=yes
TimeoutStartSec=600

[Install]
WantedBy=multi-user.target
```

Budget arithmetic (FACT — same table as 35-esme §5, conformant from day one):

| Phase | Mechanism | Worst case |
| --- | --- | ---: |
| 1. API wait | 30 probes (`--connect-timeout 2 --max-time 5`, `sleep 2` between) | 208 s |
| 2. Model load | single attempt, `--connect-timeout 3 --max-time 300`, NO retry | 300 s |
| 3. `/api/ps` assertion | single read, `--connect-timeout 3 --max-time 30` | 30 s |
| **Script total** | | **538 s** |
| Unit `TimeoutStartSec` | | **600 s** (62 s slack) |
| D5 recovery SLO | | **900 s** (300 s margin over unit) |

- Lint (T11): **ShellCheck 0.9.0** (noble archive deb via `apt download`, extracted in a volatile hxs-5 workspace, not installed — 35-esme method): **zero findings** on the preload script (and on the session askpass helper); `sh -n`, `dash -n`, `bash -n` all PASS.
- Effective (FACT): `systemctl show ollama-preload` → `Type=oneshot`, `TimeoutStartUSec=10min`, `RemainAfterExit=yes`.

## 6. Test execution — preload first run, residency, journal (T12–T14, T16; FACT)

**Preload first run (04:45:54Z → 04:47:09Z):** `sudo -n systemctl start ollama-preload.service` → **PRELOAD_RC=0 in 75 s** (first-ever cold load of the 16.9 GB artifact: ~40 s API-ready GPU discovery absorbed by Phase-1 probes + runner build/load). Journal:

```text
Aug 26 04:45:54 hxs-2 systemd[1]: Starting ollama-preload.service - Ollama preload — pin hx-qwen3.6-coderx resident (keep_alive=-1)...
Aug 26 04:47:09 hxs-2 hx-ollama-preload[7517]: hx-ollama-preload: OK - hx-qwen3.6-coderx resident (digest 1d297a6a093f7858da9a96e39950b6e7581118708b6121182a811a1f3bf21ba5)
Aug 26 04:47:09 hxs-2 systemd[1]: Finished ollama-preload.service ... 
```

Unit: `ActiveState=active (exited)`, `Result=success`, `ExecMainStatus=0`.

**Residency (04:47Z, re-verified 04:49:21Z, 04:51:25Z, 04:52:09Z — the last is 5 min post-pin, past the default 5-min eviction window, zero unload/evict journal events):**

| Property | `/api/ps` + `ollama ps` value | Verdict |
| --- | --- | --- |
| name | `hx-qwen3.6-coderx:latest` | exact alias ✓ |
| digest | `1d297a6a093f7858da9a96e39950b6e7581118708b6121182a811a1f3bf21ba5` | **exact frozen digest** ✓ |
| size vs size_vram | 17,602,392,879 == 17,602,392,879 B | **100% VRAM** ✓ |
| processor | `100% GPU` | no CPU fallback ✓ |
| context_length | **32768** | baked ctx, untouched ✓ |
| expires_at | `2318-12-06T04:34:25Z` (`UNTIL Forever`) | keep_alive=-1 pin ✓ |
| per-GPU VRAM | GPU0 **9,940 MiB** + GPU1 **8,772 MiB** (runner pid 7546: 9,932 + 8,764) | **BOTH 5060 Ti hold the model** ✓ |

**Enablement (T13):** `ollama` enabled (installer), `ollama-preload` enabled **after** the first-run pass (symlink in `multi-user.target.wants`). `is-enabled` → `enabled` ×2.

**Journal health (T14):** `journalctl -u ollama --since 04:44` — no error-level entries; three WARN/INFO lines of the **hxs-1 F-E2 watchdog class** (`llama-server GPU discovery watchdog timed out` / `failure during llama-server GPU discovery` / `timed out waiting for server startup`, 04:45:58–04:46:00, first runner build; discovery retried and succeeded; load ended 100% GPU — F-J1, MONITOR). Two further grep hits were benign `failures=0` counter lines. Kernel: **`NVRM: Xid` = 0 this boot and all boots**; OOM = 0; `NRestarts=0`.

**Hygiene (T16):** `systemctl --failed` → 0; listeners `:22`, `*:11434`, loopback runner port, stub DNS (no other exposure); uptime continuous 13:38+ (**no reboot**); swap 0 B used; RAM 3.7 Gi used / 58 Gi available; root 32 G used / 3.4 T free.

## 7. Reachability matrix (T15; FACT, 04:48Z)

| Origin | Target | Result |
| --- | --- | --- |
| hxs-2 loopback | `http://127.0.0.1:11434/api/version` | `{"version":"0.32.15"}` ✓ |
| hxs-5 (LAN, local curl) | `http://192.168.50.201:11434/api/version` | `{"version":"0.32.15"}` ✓ |

Endpoint posture per D2 + blueprint §5: wildcard bind with loopback preserved; no host firewall (owner rule); the private 192.168.50.0/24 LAN is the boundary; no service-layer auth (as designed and ratified).

## 8. Configuration files (profile §11.2)

| File | Pre-change | sha256 (pre) | sha256 (post) | Owner/mode |
| --- | --- | --- | --- | --- |
| `/etc/systemd/system/ollama.service` | absent | — (absent) | `11758d469d3f103e53a9612a8ffcb3a3e61834c994c08d412bb051f3c827dbd3` | root:root 0644 (reviewed installer) |
| `/etc/systemd/system/ollama.service.d/hx2.conf` | absent (dir absent) | — (absent) | `0918415897ac871adbff367a9ec381e4da77e0ef294bd0313a95b2498d68c35b` | root:root 0644 |
| `/etc/systemd/system/ollama-preload.service` | absent | — (absent) | `bf3cc6948f344a1a74307830b0bee31af6603fd24b3615cd7c13e036c3e11f57` | root:root 0644 |
| `/usr/local/libexec/hx-ollama-preload` | absent (dir absent) | — (absent) | `ab1c8010c3a498736b9f8532f7b664faf7afef0255fddc50b4762cff87fe86f9` | root:root 0755 |
| `/tmp/esme-m4/Modelfile` (alias source) | absent | — (absent) | `39c7fcf835ceda57d1a9ea903ddaa752368b3221415b9e3c049f4fa2dba18113` | hxsa:hxsa 0644 |

All five files are **creations from a null pre-state** — unified diff against `/dev/null` equals full content; the four operative files' contents are inlined verbatim in §5.2 (unit per upstream), §5.6, and §5.7, and the Modelfile in §5.5 (diff patch retained in session evidence `22-config-diffs.patch`). Effective runtime values post-reload: §5.6 (`systemctl show` + server-config env line). Install method: `sudo -n install -o root -g root -m 0644/0755` from hash-verified candidates (remote hashes matched local before install; `/tmp` transfer copies removed after). `sudo -n systemctl daemon-reload` after file placement.

## 9. Findings register

- **F-J1 (carried class, MONITOR):** `llama-server` GPU-discovery watchdog timeout during the first runner build (04:45:58–04:46:00) — same class as hxs-1 F-E2. Retried and succeeded; the load completed 100% GPU. It contributes to runner-start latency and is inside the 75 s first-run measurement; the D5 budget absorbs it with wide margin (75 s ≪ 538 s). Watch at M5/M7, as on hxs-1.
- **F-J2 (corrected, disclosed):** first SSH auth attempt failed — the credential value in the access guide is wrapped in markdown backticks; the askpass helper was corrected to strip the code-span (length-only diagnostics; the value was never printed). One refused auth, no lockout approached (`NumberOfPasswordPrompts=1`). No target state touched.
- **F-J3 (corrected, disclosed):** `/usr/local/libexec` did not exist on hxs-2; my first install batch omitted `-D` for the script, so only hx2.conf landed before the `&&` chain stopped. Re-transferred and installed cleanly (script with `-D`, then unit). Nothing was reloaded or started between attempts — zero service impact. One bounded correction consumed.
- **F-J4 (decision record):** upstream latest v0.33.0 observed and deliberately not taken; pinned 0.32.15 (§5.1).
- **F-J5 (record):** no license blob in the pulled manifest; license identity is publisher-declared Apache-2.0 (§5.4).
- **F-J6 (record):** first cold load via the preload unit = 75 s wall (page-cache cold, incl. ~40 s API-ready discovery absorbed by Phase-1 probes). D5 accounting: 75 s observed ≪ 538 s script worst case < 600 s unit ≤ 900 s SLO.

## 10. Stop conditions and bounded corrections

Stop conditions (work order): wrong artifact family — **not hit** (qwen35moe, top-8, CoderX finetune metadata); digest ambiguity — **not hit** (local digest verbatim, prefix cross-check MATCH, single unambiguous artifact); GPU not visible — **not hit** (both discovered, both hold the model); service failure after bounded retry — **not hit**; any Xid — **not hit** (0 across all boots, re-verified at final poll). Bounded corrections: 1 of 1 used (F-J3; F-J2 was pre-flight session setup, not a target gate).

## 11. Rollback notes (work-order scope; nothing executed)

Default rollback stops at units/config (model-store removal is a separately-approved step):

```bash
# 1. Preload unit: sudo systemctl disable --now ollama-preload.service
#    sudo rm /etc/systemd/system/ollama-preload.service /usr/local/libexec/hx-ollama-preload
# 2. Drop-in:    sudo rm /etc/systemd/system/ollama.service.d/hx2.conf
#    sudo systemctl daemon-reload && sudo systemctl restart ollama   # returns to loopback-only default
# 3. Alias:      ollama rm hx-qwen3.6-coderx
# 4. Tag (separate approval required): ollama rm mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M
# 5. Full uninstall (only if separately authorized; per linux.mdx):
#    systemctl stop/disable ollama; rm unit; rm /usr/local/bin/ollama /usr/local/lib/ollama;
#    rm ollama user; rm /usr/share/ollama
```

Byte-copies of every created config are inlined in this document (§5.2, §5.5–§5.7) with pre/post sha256 (§8); pre-state was "no Ollama installed" (§3). No reboot is required in either direction.

## 12. Sequential command log (profile §11.3; sanitized)

All remote commands as `hxsa@hxs-2` from `hxs-5` over independent SSH sessions (askpass reads the credential-record row at execution time; `StrictHostKeyChecking=yes` against the pinned F-05 key; `NumberOfPasswordPrompts=1`); privileged steps via `sudo -n` (NOPASSWD). "local" = hxs-5. Times UTC.

| Seq | Time | Where | Command (shape) | Exit | Evidence |
| ---: | --- | --- | --- | ---: | --- |
| 1 | 04:10 | local | `hostname; date; whoami; ip` — session host hxs-5/.204 verified | 0 | §1 |
| 2 | 04:10–26 | local | read profile, WO/CP, state log, rick M1, goal, blueprint, 12/35/39-esme, AGENTS.mds; TKV survey; roster; hxs-2 TKV records | 0 | §1 |
| 3 | 04:21 | local | download `ollama.com/install.sh`; sha256; `diff -q` vs TKV → byte-identical | 0 | §5.1 |
| 4 | 04:21 | local | GitHub releases API → latest v0.33.0 (observed, not taken) | 0 | F-J4 |
| 5 | 04:22 | local | read-only registry probes: manifest/config/params/template blobs; prefix cross-check PASS | 0 | §1, §5.4 |
| 6 | 04:23 | local | `ssh-keygen -F 192.168.50.201`; ed25519 fingerprint == F-05 pin | 0 | header |
| 7 | 04:24 | local | credential-file shape probes (field counts, header, field names only — value never printed) | 0 | §12 note |
| 8 | 04:26 | local | build workspace, askpass helper + rssh (0700); askpass shape test (non-empty only) | 0 | §12 note |
| 9 | 04:27 | ssh | first connection → **Permission denied** (backtick-wrapped value; F-J2) | 1 | §9 |
| 10 | 04:27 | local | masked shape diagnosis (length/backtick flags only); helper corrected; len-only re-test | 0 | §9 |
| 11 | 04:28:24 | ssh | identity: hostname, `$SSH_CONNECTION`, machine-id, UUID, eno1, `sudo -n true` | 0 | §3 (T0a) |
| 12 | 04:29:08 | ssh | baseline: pre-install absent ×6, OS/kernel/mem/swap/df/GPUs/failed/listeners/Xid=0 | 0 | §3 (T1/T2) |
| 13 | 04:30 | ssh | transfer installer (hash match); `OLLAMA_VERSION=0.32.15 sh …` → RC=0, "NVIDIA GPU installed." | 0 | §5.2 |
| 14 | 04:31 | ssh | T4 verify (0.32.15 binary==server, user, unit); T5 loopback-only + LAN refused; T6 both GPUs CUDA | 0 | §5.2/§5.3 |
| 15 | 04:31:36→34:59 | ssh | `ollama pull mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M` (3m22s, success) | 0 | §5.4 |
| 16 | 04:35 | ssh | identity CLI set: `--version`, `list`, `show`, `show --modelfile`, `/api/tags` | 0 | §5.4 |
| 17 | 04:36 | ssh | `/api/show` full JSON capture (753 tensors, projector_info) | 0 | §5.4 |
| 18 | 04:37 | local | ollama.com model page → "Apache-2.0 · research checkpoint." | 0 | F-J5 |
| 19 | 04:40:53 | ssh | transfer Modelfile (hash match); `ollama create hx-qwen3.6-coderx` → success (4 frozen layers reused) | 0 | §5.5 |
| 20 | 04:41 | ssh+local | alias verify: list/show/manifest paths+hashes; manifests → local; layers identical; alias config equivalent | 0 | §5.5 |
| 21 | 04:42 | local | author hx2.conf + preload script + unit; `apt download shellcheck` + extract; **shellcheck CLEAN**; sh/dash/bash -n; candidate hashes | 0 | §5.7 |
| 22 | 04:43:48 | ssh | transfer 3 files (hash match); pre-state absent; install — PARTIAL (libexec absent; F-J3) | 1 | §9 |
| 23 | 04:44:21 | ssh | re-transfer script+unit; `install -D` script + install unit → INSTALL-OK; post hashes match | 0 | §8 |
| 24 | 04:44:34 | ssh | `daemon-reload`; `restart ollama` → active; API OK attempt 5 (~40 s); bind `*:11434`; Environment exact; `TimeoutStartUSec=10min` | 0 | §5.6 |
| 25 | 04:45:54→47:09 | ssh | `systemctl start ollama-preload` → **RC=0, 75 s**; journal OK line with frozen digest | 0 | §6 |
| 26 | 04:47 | ssh | `/api/ps` (alias, exact digest, size==size_vram, ctx 32768, expires 2318); `ollama ps`; nvidia-smi split | 0 | §6 |
| 27 | 04:48 | ssh | `enable ollama-preload` → enabled ×2; journal scans (Xid 0/0, OOM 0, NRestarts=0); hygiene (0 failed, listeners, uptime, swap, df, du) | 0 | §6 |
| 28 | 04:48 | ssh+local | reachability: 127.0.0.1 OK; hxs-5→192.168.50.201:11434 OK; server-config env line captured | 0 | §7 |
| 29 | 04:49/04:51/04:52 | ssh | idle re-checks: resident, Forever, 0 unload/evict events, NRestarts=0, Xid=0 (04:52:09 = 5 min post-pin) | 0 | §6 |
| 30 | ~04:53+ | local | diffs generated; deliverable written; **workspace + askpass helper deleted** (no extracted credential copy ever existed) | — | §12 note |

Sanitization confirmed: no secret value was printed, logged, stored, or placed on any command line; the askpass helper (deleted at task end with the volatile workspace) read `ssh-info.md` line 25 pipe-field 3 (markdown code-span unwrapped) at execution time only. The one refused authentication (seq 9) and the partial install (seq 22) are retained per profile §15 — no history rewritten.

## 13. Artifact hashes

```text
25f64b810b947145095956533e1bdf56eacea2673c55a7e586be4515fc882c9f  install.sh (== TKV ollama-main/scripts/install.sh)
11758d469d3f103e53a9612a8ffcb3a3e61834c994c08d412bb051f3c827dbd3  /etc/systemd/system/ollama.service (installer-written)
0918415897ac871adbff367a9ec381e4da77e0ef294bd0313a95b2498d68c35b  /etc/systemd/system/ollama.service.d/hx2.conf
bf3cc6948f344a1a74307830b0bee31af6603fd24b3615cd7c13e036c3e11f57  /etc/systemd/system/ollama-preload.service
ab1c8010c3a498736b9f8532f7b664faf7afef0255fddc50b4762cff87fe86f9  /usr/local/libexec/hx-ollama-preload
39c7fcf835ceda57d1a9ea903ddaa752368b3221415b9e3c049f4fa2dba18113  Modelfile (alias source)
mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M  digest ca661423d6b51ebeaca999f22cfc0f30c0851b2a6f328b2737bd8cb6eb90c1df  (FROZEN IDENTITY)
hx-qwen3.6-coderx:latest                     digest 1d297a6a093f7858da9a96e39950b6e7581118708b6121182a811a1f3bf21ba5  (alias; blob-bound to the frozen identity)
hxs-2 host key (pinned, rick M1 F-05)        ED25519 SHA256:b2qlMQz496nUbuZKJu3wwmR0QY/EmN0KQtW4rM2HDcQ
```

## 14. Validation summary (profile §11.4)

- **What changed:** Ollama **0.32.15 pinned-installed** on hxs-2 (user `ollama`, upstream unit); drop-in `hx2.conf` applied (`OLLAMA_HOST=0.0.0.0` loopback-preserved, `NO_CLOUD=1`, `NUM_PARALLEL=1`, `MAX_LOADED_MODELS=1`); model `mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M` pulled and **identity-frozen** (`ca661423d6b5…c1df`); alias `hx-qwen3.6-coderx` created FROM-only and **blob-bound** to the frozen artifact (`1d297a6a09…21ba5`); preload script + unit installed at D5 budgets (538 s < 600 s ≤ 900 s) and enabled.
- **What did not change:** OS/driver/kernel/DKMS/packages (rick's plane incl. sleep masks, rfkill), network/firewall/DNS (**no ufw**), storage topology, Secure Boot state, **no reboot** (uptime continuous), no other models/tags, no context or sampling changes anywhere (baked tag params verbatim), no model-store deletions.
- **Tested:** T0a–T16 (17 tests): identity, pin, installer authenticity, install, loopback-before-LAN, GPU visibility, pull, §12.2 identity freeze, alias binding (3-way), drop-in effective state, preload lint + first run + enablement, residency (alias + exact digest + 100% VRAM both GPUs + ctx 32768 + Forever), journal health, reachability matrix, hygiene.
- **Passed:** 17/17. **Failed:** none. **Not run:** none mandatory (restart/reboot recovery is M7 scope; context ladder M6; quality suites M5).
- **Current Ollama state:** 0.32.15 binary==server, active/enabled, `NRestarts=0`, wildcard bind with loopback preserved, cloud disabled.
- **Current model state:** `hx-qwen3.6-coderx:latest` resident, digest `1d297a6a093f7858da9a96e39950b6e7581118708b6121182a811a1f3bf21ba5`, 100% VRAM (size == size_vram 17,602,392,879 B) across **both** 5060 Ti (9,940 + 8,772 MiB), ctx 32768, Forever.
- **Endpoint/security state:** `*:11434` (0.0.0.0 incl. loopback); reachable from 127.0.0.1 and from hxs-5 over the /24; no host firewall per owner rule; no service-layer auth (ratified posture); no credentials in any file.
- **Resource state:** RAM 3.7 Gi used; swap 0 B; root 3.4 T free; zero Xid all boots.
- **Rollback readiness:** §11 inverses exact; pre-state "no Ollama"; every artifact hashed; byte-copies inlined.
- **Remaining risks/decisions:** F-J1 watchdog class (monitor at M5/M7); F-J4 version pin revisited only by future work order; Carol catalog receipt (handoff gate per context packet).

**Second Brain evaluation (standing directive, per work order):** (1) opportunity identified — yes; (2) pattern — hxs-1 M4 install pattern (second validated use) + D5-budget preload as blueprint default from day one; (3) disposition — **implemented**: the identity freeze (frozen digest pair + blob-binding proof) and the unit contracts become the hxs-2 catalog spine at handoff; (4) evidence — the install/evidence shape transferred cleanly; blueprint-from-day-one (not retrofitted) is the measurable payoff of the hxs-1 lessons. This deliverable goes to Carol for catalog receipt; handoff OPEN until the receipt is cited in the state log.

`PASS — TASK COMPLETE`

```text
Task May Proceed: YES
```

Signed: **john / Esme** — Expert Ollama Engineer, session `john-m4-20260826-01`, 2026-08-26T04:53Z (UTC).
