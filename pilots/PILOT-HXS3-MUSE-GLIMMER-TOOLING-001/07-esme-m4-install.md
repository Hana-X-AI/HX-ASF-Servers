# 07 — Esme (john): M4 Ollama Install + Exact-Tag Pull + Identity Freeze + D5-Budget systemd (hxs-3)

`[TASK COMPLETE — EVIDENCE ATTACHED]`

| Field | Value |
| --- | --- |
| Report ID | ESME-HXS3-M4-INSTALL-001 |
| Task ID | WO-HXS3-JOHN-M4-001 (`PILOT-HXS3-MUSE-GLIMMER-TOOLING-001`, milestone M4) |
| Agent | john / Esme (profile `agents/john/profile.md`), session `john-m4-20260826-01` |
| Target host | `hxs-3` (192.168.50.202), Ubuntu 24.04.4 LTS (noble), kernel 7.0.0-30-generic, x86-64 |
| Executed from | `hxs-5` (192.168.50.204) via SSH `hxsa@192.168.50.202` — askpass helper READS the credential-record table row (`ssh-info.md` "SSH password" row) AT EXECUTION TIME ONLY; no extracted copy ever existed; helper deleted at task end |
| Host-key check | STRICT — pinned ED25519 `SHA256:R/3mdfv7J0Fajo8yryT7JB6B4EoBm47W2rLX+siHEog` (rick M1 F-05), verified against the known_hosts entry before first use; `StrictHostKeyChecking=yes` on every connection |
| Window (UTC) | 2026-08-26T06:00Z → 06:28Z (first target mutation 06:10Z; final verification poll 06:28:05Z). Host local time is EST/-05:00 (rick M1 F-08); hxs-3 journal timestamps below read EST |
| Ollama | **0.32.15** (binary == server; pinned this session — see §5.1) |
| Frozen model identity | `muse-glimmer:30b` @ digest **`de878ce33ad81d060001db1469a02eebe4d86f0ad58cfe52dc062fdcbe4464c1`** |
| Working alias | `hx-muse-glimmer:latest` @ digest **`472ad84e752d0319b65d6fcd862c26c3850cc408b6b9430046db31250994ad99`** (bound to the frozen artifact — §5.5) |
| GPUs | 2× RTX 5060 Ti 16,311 MiB (PNY), driver 580.173.02 (rick's plane, untouched) |

Evidence labels: **FACT** (live host output) / **AUTHORITY** (owner decision, work order, governance) / **UPSTREAM** (publisher/registry statement) / **INFERENCE** / **RECORD** (decision or observation).
All secrets excluded; the SSH credential was never printed, logged, or stored (§12 sanitization).

---

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path /opt/tkv-local/ollama resolves locally here); target hxs-3 (192.168.50.202)
Source: /opt/tkv-local/ollama + HX-ASF-Servers controlling docs + agent-zero-docs v1.1 pilot + Meta corpus records
Reviewed At: 2026-08-26T06:00Z → 06:08Z
Relevant Files:
  - agents/john/profile.md; agents/ roster = carol, john, kimi-k3, rick (all current teammates)
  - pilots/PILOT-HXS3-MUSE-GLIMMER-TOOLING-001/01-state-log.md (rows 1-8: M0/D1-D8, M1 13/13, Meta sources,
    Meta-X call-sign, M4 commissioned), 04-rick-hxs3-os-readiness.md (M1 evidence; F-05 pinned host key;
    identity corroborators; F-08 timezone)
  - 05-work-order-john-m4.yaml + 06-context-packet-john-m4.yaml (this package)
  - goals/2026-08-26-hxs3-muse-glimmer-tooling.md (D1-D8; SC table; stop conditions; one-call-per-turn contract)
  - servers/BLUEPRINT-llm-server.md (§2 OS plane, §3 service plane + preload contract, §5 exposure plane,
    §8 consumer contract incl. Meta-X alias row "hx-muse-glimmer (planned at M4)")
  - servers/AGENTS.md + repo AGENTS.md (records contract; no-host-firewall owner rule; communication contract)
  - pilots/PILOT-HXS2-CODERX-BACKEND-001/07-esme-m4-install.md (install/pull/identity/alias/units pattern —
    third validated use here), pilots/PILOT-HX1-OLLAMA-QWEN27B-001/35-esme-preload-budget.md (D5 budget contract)
  - v1.1 authoritative pilot §3.1 (artifact record), §3.4 (official prompting/inference contract; ATEM; llama.cpp
    b10353 = diagnostic floor only), §12 (Esme deliverables)
  - /opt/tkv-local/ollama/ollama-main/scripts/install.sh (sha256 25f64b81…82c9f — reviewed installer baseline)
  - /opt/tkv-local/ollama/ollama-main/model/parsers/glimmer.go + model/renderers/glimmer.go + x/models/glimmer/
    (glimmer renderer/parser present; parser carries the ATEM tokens — §5.4)
  - /opt/tkv-local/servers/hxs-3/ (discovery.md et al. — historical cross-check, used by rick M1)
Authority/Version Identified:
  - Ollama PIN = 0.32.15 (fleet-consistent blueprint version; Muse support floor 0.32.8 + parser boundary fix
    0.32.9 both covered). Upstream latest = v0.33.0 (governor-fetched 2026-08-26, state log row 7) — deliberately
    NOT taken (one version across all three LLM hosts). RECORD F-J4.
  - Installer downloaded 2026-08-26 from https://ollama.com/install.sh = sha256 25f64b81…82c9f,
    BYTE-IDENTICAL to the TKV-reviewed baseline → authenticity established (FACT).
  - Model: muse-glimmer:30b (owner D3). Read-only registry probes (FACT, pre-pull):
    manifest digest de878ce33ad81d060001db1469a02eebe4d86f0ad58cfe52dc062fdcbe4464c1 (prefix MATCHES the
    packet cross-check de878ce33ad8); config family muse-glimmer, 27.9B, Q4_K_M, renderer glimmer, parser
    glimmer, requires 0.32.8; layers: projector f48b452316f9… 1,400,328,928 B + model 71b5c9c9abbc…
    16,756,681,056 B + params 56380ca2ab89… 42 B; params blob verbatim {"temperature":1,"top_k":64,"top_p":0.95}.
Applicable Tests/Runbooks: profile §7.1/§7.2; v1.1 §3.1/§3.4 identity capture set; hxs-2 07-esme install order;
  35-esme budget arithmetic; blueprint §3 preload contract
Contradictions or Gaps:
  - TKV source snapshot v0.32.11 < install target 0.32.15 (snapshot already contains the glimmer model/renderer/
    parser incl. ATEM tokens; the deployed 0.32.15 adds the 0.32.9 parser boundary fix — recorded openly,
    hxs-1 F-E7 precedent class).
  - Upstream latest (0.33.0) ≠ fleet pin (0.32.15) — resolved to the pin (F-J4; state log row 7 disposition).
  - No live/knowledge conflicts; hxs-3 live state re-verified at baseline (packet: "re-verify at start").
Task May Proceed: YES
```

## 2. Test plan and results (plan recorded before first mutation, 06:09Z)

| ID | Property | Expected | Result |
| --- | --- | --- | --- |
| T0a | Session + target identity | hxs-3/.202; machine-id/UUID/MAC match discovery + rick M1; sudo -n OK | **PASS** (§3) |
| T0b | Host-key pin strict check | == rick M1 F-05 fingerprint | **PASS** (header; pre-verified 06:06Z) |
| T1 | Pre-install state | no binary/user/unit/listener/package | **PASS** (§3) |
| T2 | Baseline health | matches rick M1; Xid=0 | **PASS** (§3) |
| T3 | Installer authenticity | sha256 == TKV reviewed baseline | **PASS** (§5.1) |
| T4 | Install + pin 0.32.15 | binary==server==0.32.15; system user; upstream unit; no driver/apt authority | **PASS** (§5.2) |
| T5 | Default bind pre-drop-in | loopback-only; LAN refused | **PASS** (§5.3) |
| T6 | GPU visible to Ollama | BOTH 5060 Ti, library=CUDA | **PASS** (§5.3) |
| T7 | Pull exact tag | success; blobs == registry manifest | **PASS** (§5.4, 3m33s) |
| T8 | Identity freeze (full set) | --version/list/show/show --modelfile//api/show; digest verbatim; family muse-glimmer; template+renderer/parser incl. ATEM presence; projector CLIP 1.92B Q4_K_M; cross-check de878ce33ad8 | **PASS** (§5.4) |
| T9 | Alias binding | FROM-only Modelfile; blob-set equality; baked params preserved (T1/top_k 64/top_p 0.95) | **PASS** (§5.5) |
| T10 | hx3.conf drop-in | exactly the 4 mandated env values; wildcard bind incl. loopback | **PASS** (§5.6) |
| T11 | Preload script+unit | shellcheck clean; TimeoutStartUSec=10min | **PASS** (§5.7, §6) |
| T12 | Preload first run | alias resident; exact digest; 100% VRAM; both GPUs; Forever | **PASS** (§6, 42.5 s cold) |
| T13 | Enablement | both units enabled | **PASS** (§6) |
| T14 | Journal health | no errors; Xid=0; OOM=0; NRestarts=0 | **PASS** (§6; F-J1 watchdog class recorded) |
| T15 | Reachability | 127.0.0.1 AND hxs-5→192.168.50.202:11434 /api/version | **PASS** (§7) |
| T16 | Post-state hygiene | 0 failed units; no reboot; swap 0; storage delta recorded | **PASS** (§6) |
| T17 | Link-speed telemetry | current vs max, idle-loaded AND under inference load (row-2 caveat) | **PASS** (§7.1) |
| T18 | Smoke inference | known-answer 17×23=391; thinking stripped from evidence | **PASS** (§7.2) |

**19/19 PASS; 0 FAIL; 0 BLOCKED; 0 NOT RUN.** Stop conditions (wrong artifact family, Muse load failure, template/ATEM parser absent, GPU not visible to Ollama, service failure after bounded retry, any Xid): **none hit**. Bounded corrections used: **0 of 1** (the hxs-2 F-J2/F-J3 lessons were pre-applied — code-span unwrap in the askpass helper, `install -D` for the libexec path).

## 3. Identity and pre-change baseline (FACT, 06:08:05Z → 06:09:30Z)

- **Identity (T0a):** `hostname` → `hxs-3`; `SSH_CONNECTION` → `192.168.50.204 … 192.168.50.202 22` (hxs-5 → hxs-3); machine-id `d02a8e3a8d76474390e51a162e9f196d`; system UUID `038d0240-045c-05e7-d006-e70700080009`; eno1 `192.168.50.202/24` MAC `40:8d:5c:e7:d0:e5` — all match the 2026-08-12 discovery record and rick M1. `sudo -n true` → OK. Host clock 01:08:05 EST = 06:08:05Z; uptime 13:44 continuous.
- **Pre-install state (T1):** `command -v ollama` empty; `systemctl status ollama` "could not be found"; `id ollama` no such user; `/usr/share/ollama` absent; `dpkg -l | grep -i ollama` count 0; no `:11434` listener. **Ollama was NOT installed** (packet expectation re-verified live).
- **Health (T2):** Ubuntu 24.04.4 LTS noble; kernel 7.0.0-30-generic; RAM 62 Gi (1.0 Gi used); swap 8 Gi, 0 B used; root ext4 3.6 T, 14 G used, **3.4 T free (1%)**; GPUs `GPU-3cb368de-b2ea-c6ab-57d1-8d6298831f90` (0) and `GPU-73cb422b-80d9-f53d-c8b7-45dbb32cbea1` (1), both RTX 5060 Ti 16,311 MiB, 0 MiB used, driver 580.173.02 — exact match to rick M1; 0 failed units; **`NVRM: Xid` count = 0 across all retained boots**.

## 4. Implementation record

### 5.1 Installer review and version pin (T3; profile §7.1)

- FACT: `curl -fsSL https://ollama.com/install.sh` (2026-08-26T06:09Z) → sha256 `25f64b810b947145095956533e1bdf56eacea2673c55a7e586be4515fc882c9f` (455 lines), **byte-identical** to TKV `ollama-main/scripts/install.sh` (same sha256; `diff -q` clean) — the same reviewed baseline hxs-1 M4 and hxs-2 M4 executed. Served over HTTPS from ollama.com. **AUTHENTICITY ESTABLISHED.** Never blind-piped: transferred as a file, hash-verified on both sides (remote sha256 matched before execution), then executed.
- FACT (review stands, same bytes as hxs-1/hxs-2 M4 §4.1): on a host with working `nvidia-smi` the script (a) extracts `ollama-linux-amd64.tar.zst` to `/usr/local`; (b) creates system user `ollama`, adds it to `render`+`video`, adds the invoking user to `ollama`; (c) writes `/etc/systemd/system/ollama.service`, enables + starts it; (d) exits 0 at "NVIDIA GPU installed." **before** all CUDA-driver/DKMS/apt logic. The installer cannot become GPU-driver or OS-package authority here.
- RECORD (F-J4, the pin): upstream latest is **v0.33.0** (governor-fetched 2026-08-26, state log row 7) — deliberately **not** taken. Pin = **0.32.15**, the fleet-validated version (hxs-1 M4→M8 closed PASS; hxs-2 M4 PASS), via the installer's supported `OLLAMA_VERSION` mechanism (install.sh line 42: `VER_PARAM="${OLLAMA_VERSION:+?version=$OLLAMA_VERSION}"`). Rationale: blueprint consistency (one version across all three LLM hosts), brand-new-minor conservatism, and the frozen model artifact predates 0.33.0. The Muse family runtime floor (`requires 0.32.8`) and the 0.32.9 parser boundary fix are both covered by the pin. Upgrade path = a future versioned work order.

### 5.2 Install result (T4; FACT, 06:10:14Z → 06:11:01Z)

- `OLLAMA_VERSION=0.32.15 sh /tmp/ollama-install-reviewed.sh` → `INSTALL_RC=0`; output ended `>>> NVIDIA GPU installed.` (driver logic confirmed skipped; zero apt/dkms/modprobe activity).
- `ollama version is 0.32.15`; `/api/version` → `{"version":"0.32.15"}` (**binary == server == pin**). Binary `/usr/local/bin/ollama` (39,159,472 B).
- `id ollama` → `uid=999(ollama) gid=988(ollama) groups=988(ollama),44(video),993(render)`; home `/usr/share/ollama` (`drwxr-x--- ollama:ollama`). Invoking user `hxsa` added to group `ollama` (installer default).
- Unit: upstream default `/etc/systemd/system/ollama.service` (`ExecStart=/usr/local/bin/ollama serve`, `User/Group=ollama`, `Restart=always`, `RestartSec=3`, `WantedBy=default.target`), **enabled + active**. sha256 `11758d469d3f103e53a9612a8ffcb3a3e61834c994c08d412bb051f3c827dbd3` — identical to the hxs-2 installer-written unit (same installer bytes). Content inlined in §8.

### 5.3 Default bind + GPU visibility BEFORE any change (T5, T6; FACT, 06:11Z)

- `ss -lntp`: `LISTEN 127.0.0.1:11434` only; `curl http://192.168.50.202:11434/api/version` → connection refused (0 ms). Upstream default is loopback-only; the LAN bind arrives only via the authorized hx3.conf (§5.6).
- Journal: `Listening on 127.0.0.1:11434 (version 0.32.15)` (06:10:14Z); **both** GPUs discovered — `inference compute id=0/1 library=CUDA compute=12.0 "NVIDIA GeForce RTX 5060 Ti" driver=13.0 pci_id=0000:02:00.0/0000:03:00.0 total 15.5 GiB` (06:11:01Z, ≈47 s after start, within the default start timeout). Stop condition "GPU not visible to Ollama" cleared.

### 5.4 Pull and identity freeze (T7, T8; FACT, 06:11:27Z → 06:14:59Z)

- `ollama pull muse-glimmer:30b` → success in **3m32.547s** (~108 MB/s observed on the 1.4 GB layer); client verified the sha256 digest during pull; blobs fetched = exactly the registry manifest's layers (`71b5c9c9abbc…` 16 GB model, `f48b452316f9…` 1.4 GB projector, `56380ca2ab89…` 42 B params). Nothing else was pulled; no other tag existed on the host at pull time.
- **FROZEN IDENTITY (the local full digest is authoritative):**

| Field | Value (FACT unless labeled) |
| --- | --- |
| Full name + explicit tag | `muse-glimmer:30b` (official Ollama library artifact; `parent_model: muse-glimmer:30b-q4_K_M`) |
| **Local digest (FROZEN)** | **`de878ce33ad81d060001db1469a02eebe4d86f0ad58cfe52dc062fdcbe4464c1`** (`/api/tags` verbatim; on-disk manifest sha256 == digest, as content-addressing requires) |
| Reference prefix cross-check | `de878ce33ad8` — **MATCH** (registry state has not advanced since the packet observation; the local manifest is byte-equal to the pre-pull registry probe) |
| Size | 18,157,010,252 B (16,756,681,056 LM + 1,400,328,928 projector + 42 params + 226 config — fully accounted) |
| modified_at | 2026-08-26T01:14:59 EST (06:14:59Z) |
| Format / family | `gguf` / `muse-glimmer` (families: `[muse-glimmer]`) — **correct artifact family** |
| Parameter size | 27.9B (`general.parameter_count` 27,854,794,240; size label `28B`); **dense** — 52 blocks (`block_count` 52, matches v1.1 §3.2) |
| Quantization | `Q4_K_M` (file_type 15; quantization_version 2) |
| Model max context | 131,072 (`muse-glimmer.context_length` — 128K declared max; ladder at M7) |
| Capabilities | `completion`, `vision`, `tools`, `thinking` (text/image/tools/thinking all present) |
| Architecture detail | GQA: 32 heads / 2 KV heads, k/v length 128; sliding window 2048; embedding 6656; FFN 19968; RoPE freq_base 500000; final_logit_softcapping 20; logit_scale 0.19611613; tokenizer gpt2 (`pre: llama4`), BOS 200000 / EOS 200001 / EOT 200008 / PAD 200018 |
| Template | `{{ .Prompt }}` (artifact template; chat handled by the built-in renderer) |
| Renderer / Parser | `glimmer` / `glimmer` (`show --modelfile` fields `RENDERER glimmer` / `PARSER glimmer`; config blob identical) — **ATEM tool-parser PRESENT**: the version-matched TKV source `model/parsers/glimmer.go` carries the ATEM tokens (`<atem:function_calls>`, `<atem:invoke name="…">`, `<atem:parameter name="…">`) with glimmer parser states header/content/thinking/tool; `requires 0.32.8`, and the pin 0.32.15 includes the 0.32.9 parser boundary fix |
| Baked parameters (verbatim) | `temperature 1`, `top_k 64`, `top_p 0.95` (params blob `{"temperature":1,"top_k":64,"top_p":0.95}` — no `num_ctx` baked) — **preserved; zero overrides added anywhere** |
| **Projector identity** | `clip`, `general.name "Muse Glimmer Hf"`, type `mmproj`, **1,920,942,592 params (1.92B)**, `Q4_K_M` (file_type 15), `clip.projector_type muse-glimmer`, `has_vision_encoder true`, 50 vision blocks, vision embedding 1536, FFN 8960, 16 heads, image 896 / patch 14, spatial_merge 2, projection_dim 6656, mean/std 0.5 — the CLIP perception component, exactly per packet §current_state |
| License | **UPSTREAM:** `Apache-2.0` ("licensed under Apache 2.0" — ollama.com library page, 06:16Z; v1.1 §3.1; Meta model card). RECORD (F-J3): the pulled manifest carries **no license blob** — `/api/show` has no license field; recorded as publisher-declared, not local-artifact fact |
| `requires` floor | `0.32.8` (pin 0.32.15 covers it plus the 0.32.9 parser boundary fix) |
| Ollama version / host / GPU / OS | 0.32.15 (binary==server) / hxs-3 / 2× RTX 5060 Ti / Ubuntu 24.04.4, kernel 7.0.0-30 (§3) |

- `/api/show` full JSON (`verbose`) captured to session evidence `08-identity-apishow.json` (model_info incl. full tensor list, projector_info, modelfile, parameters, template); the determining fields are inlined above.
- Storage delta (D1, root ext4): `/` 14 G → 33 G used; models dir `17G`; free still 3.4 T (1%). Path `/usr/share/ollama/.ollama/models` owned `ollama:ollama`.

### 5.5 Alias `hx-muse-glimmer` — bound to the frozen digest (T9; FACT, 06:18:00Z)

- Modelfile (sha256 `0504cecd5cfdb70a6e203d7fc209d1f0c1040403fdfe5eb15005e74782ad3068`, identical hxs-5 copy ↔ hxs-3 `/tmp/esme-m4-Modelfile` before removal) — **FROM only; NO PARAMETER/SYSTEM/TEMPLATE lines** (native-sampling baseline; baked tag params preserved):

```dockerfile
# hx-muse-glimmer — WO-HXS3-JOHN-M4-001 (PILOT-HXS3-MUSE-GLIMMER-TOOLING-001, M4)
# Working alias bound to the frozen Muse Glimmer artifact:
#   muse-glimmer:30b
#   digest de878ce33ad81d060001db1469a02eebe4d86f0ad58cfe52dc062fdcbe4464c1
# FROM only — NO PARAMETER/SYSTEM/TEMPLATE lines: the baked tag parameters
# (temperature 1, top_k 64, top_p 0.95) are preserved unchanged
# (native-sampling baseline; the M7 ladder owns any context change).
FROM muse-glimmer:30b
```

- `ollama create hx-muse-glimmer` → success; the create log shows **all three frozen layers reused** (`f48b452316f9…`, `71b5c9c9abbc…`, `56380ca2ab89…`).
- **Alias digest (FROZEN): `472ad84e752d0319b65d6fcd862c26c3850cc408b6b9430046db31250994ad99`** (a new manifest, as expected; `ollama list` ID prefix `472ad84e752d` consistent).
- **Binding proof, three independent ways (FACT):**
  1. Manifest layer comparison: alias layers == base layers, **ordered AND set-equal** — same config `57b82200bf7c…`, same three layer digests in the same order (only the `from` provenance annotation differs: `muse-glimmer:30b` vs `muse-glimmer:30b-q4_K_M`; annotations are not content). The alias is content-addressed to the frozen blobs; it cannot resolve to anything else and does not follow the upstream tag if re-pulled.
  2. `ollama show hx-muse-glimmer` == base identity field-for-field (architecture, 27.9B, 131072 max ctx, Q4_K_M, capabilities, projector, **baked parameters verbatim** — zero added parameters).
  3. Alias config blob is the **same** config blob `57b82200bf7c…` as the base (digest-equal → identical identity metadata: family `muse-glimmer`, 27.9B, Q4_K_M, renderer/parser glimmer).
- Manifest sha256s on disk: base `de878ce33ad8…64c1` (== its digest, as content-addressing requires); alias `472ad84e752d…ad99`.

### 5.6 Service plane — hx3.conf drop-in (T10; FACT, 06:19:24Z install → 06:20:06Z restart)

`/etc/systemd/system/ollama.service.d/hx3.conf` (root:root 0644, sha256 `b4f98c2f829bc7ba86690e8bfbc73748a2c4b858425e37593aa1402b7a20627c`) — exactly the four mandated values, nothing else:

```ini
# hxs-3 Muse Glimmer service plane — WO-HXS3-JOHN-M4-001 (blueprint §3/§5; owner D2).
# OLLAMA_HOST=0.0.0.0 binds the wildcard address (default port 11434 per
# envconfig Host()); loopback is preserved — the preload script and fixtures
# use 127.0.0.1. The private 192.168.50.0/24 LAN itself is the boundary:
# no host firewall anywhere (owner rule 2026-08-26). Admission control:
# exactly one loaded model, one parallel request. Cloud features disabled.
# Native-sampling baseline: NO context or sampling variables are set here —
# the baked tag parameters (temperature 1, top_k 64, top_p 0.95) govern;
# the M7 ladder owns any context change.
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_NO_CLOUD=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
```

Effective state after `daemon-reload` + `systemctl restart ollama` (06:20:06Z; only ollama.service restarted; no reboot):

- `systemctl show ollama`: `Environment=PATH=… OLLAMA_HOST=0.0.0.0 OLLAMA_NO_CLOUD=1 OLLAMA_NUM_PARALLEL=1 OLLAMA_MAX_LOADED_MODELS=1`; `DropInPaths=/etc/systemd/system/ollama.service.d/hx3.conf`; `NRestarts=0`; active/running.
- Server startup log (FACT): `OLLAMA_HOST:http://0.0.0.0:11434`, **`Ollama cloud disabled: true`**, `OLLAMA_MAX_LOADED_MODELS:1`, `OLLAMA_NUM_PARALLEL:1`, `OLLAMA_CONTEXT_LENGTH:0` (server unset — no context override anywhere; the effective per-model ctx is the VRAM-based default, F-J2), `OLLAMA_KEEP_ALIVE:5m0s` (service default — the preload's request-level `keep_alive:-1` pins Forever, proven by `expires_at` year 2318); `Listening on [::]:11434`.
- Bind: `ss` → `*:11434` (wildcard dual-stack; loopback preserved — §7 matrix). RECORD: API answered on probe attempt 7 (~20 s post-restart, CUDA rediscovery window — hxs-1 F-E1 transient class, recorded, expected).

### 5.7 Preload script + unit — D5 budgets from day one (T11; FACT)

`/usr/local/libexec/hx-ollama-preload` (root:root 0755, sha256 `d37dc30fb43ebfe674db37fdd963f219a4ef31867512a549558db930559dfd84`) — the 35-esme bounded-phase contract, pinned to alias + frozen digest:

```sh
#!/bin/sh
# hx-ollama-preload — PILOT-HXS3-MUSE-GLIMMER-TOOLING-001 (WO-HXS3-JOHN-M4-001)
# Loads the exact pilot model with keep_alive=-1, then asserts /api/ps
# residency of the exact alias AND its frozen digest. D5-conformant bounded
# phases (35-esme budget contract):
#   Phase 1 API wait: at most 30 fast probes of /api/version
#     (connect-timeout 2 s, max-time 5 s, sleep 2 s between probes);
#     worst case 30*5 + 29*2 = 208 s.
#   Phase 2 model load: ONE attempt, --max-time 300 (cold dual-GPU load of
#     the 18.2 GB artifact is expected in tens of seconds; 300 s is a
#     generous margin); NO retry — a timeout must fail the unit, not
#     extend the budget.
#   Phase 3 assertion: one /api/ps read, --max-time 30; the exact alias
#     name AND the frozen digest must both be present.
# Script worst case: 208 + 300 + 30 = 538 s, below TimeoutStartSec=600 in
# ollama-preload.service, itself 300 s under the 900 s D5 recovery SLO.
# On any exhaustion or failure it FAILS (alert path); it never loops.
# No credentials are embedded or required (loopback-only API).
set -eu

MODEL="hx-muse-glimmer"
DIGEST="472ad84e752d0319b65d6fcd862c26c3850cc408b6b9430046db31250994ad99"
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

`/etc/systemd/system/ollama-preload.service` (root:root 0644, sha256 `3b0e00b62163c536626ee79dafecdc144b01c7b17214baae74986bd9b44ca5f6`):

```ini
[Unit]
Description=Ollama preload — pin hx-muse-glimmer resident (keep_alive=-1)
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

- Lint (T11): **ShellCheck 0.9.0** (noble archive deb via `apt download`, extracted in a volatile hxs-5 workspace, not installed — 35-esme method): **zero findings** on the preload script (and on the session askpass/ssh/scp helpers); `sh -n`, `dash -n`, `bash -n` all PASS.
- Effective (FACT): `systemctl show ollama-preload` → `Type=oneshot`, `TimeoutStartUSec=10min`, `RemainAfterExit=yes`.

## 6. Test execution — preload first run, residency, journal (T12–T14, T16; FACT)

**Preload first run (06:21:14Z → 06:21:56Z):** `sudo -n systemctl start ollama-preload.service` → **PRELOAD_RC=0 in 42.5 s** (first-ever cold load of the 18.2 GB artifact: API-ready rediscovery absorbed by Phase-1 probes + runner build/load). Journal:

```text
Aug 26 01:21:14 hxs-3 systemd[1]: Starting ollama-preload.service - Ollama preload — pin hx-muse-glimmer resident (keep_alive=-1)...
Aug 26 01:21:56 hxs-3 hx-ollama-preload[7452]: hx-ollama-preload: OK - hx-muse-glimmer resident (digest 472ad84e752d0319b65d6fcd862c26c3850cc408b6b9430046db31250994ad99)
Aug 26 01:21:56 hxs-3 systemd[1]: Finished ollama-preload.service ...
```

Unit: `ActiveState=active (exited)`, `Result=success`, `ExecMainStatus=0`.

**Residency (06:22Z, re-verified 06:28:05Z — 6+ min post-pin, past the default 5-min eviction window, zero unload/evict journal events):**

| Property | `/api/ps` + `ollama ps` value | Verdict |
| --- | --- | --- |
| name | `hx-muse-glimmer:latest` | exact alias ✓ |
| digest | `472ad84e752d0319b65d6fcd862c26c3850cc408b6b9430046db31250994ad99` | **exact frozen digest** ✓ |
| size vs size_vram | 17,839,465,428 == 17,839,465,428 B | **100% VRAM** ✓ |
| processor | `100% GPU` | no CPU fallback ✓ |
| context_length | **32768** | VRAM-based default (F-J2), no override anywhere ✓ |
| expires_at | `2318-12-06T01:09:13-05:00` (`UNTIL Forever`) | keep_alive=-1 pin ✓ |
| per-GPU VRAM | GPU0 **10,170 MiB** + GPU1 **8,908 MiB** (runner pid 7484: 10,162 + 8,900) | **BOTH 5060 Ti hold the model** ✓ |

- RECORD (F-J2, ctx provenance): the tag bakes **no** `num_ctx`; the server journal shows `msg="vram-based default context" total_vram="30.9 GiB" default_num_ctx=32768` and the runner launched with `-c 32768 -np 1 --flash-attn auto --context-shift` against `--model` blob `sha256-71b5c9c9…` + `--mmproj` blob `sha256-f48b4523…` (the frozen artifacts themselves). Effective ctx 32768 is Ollama 0.32.15's deterministic VRAM-based default for this hardware+model — **not** an HX override (`OLLAMA_CONTEXT_LENGTH` unset) and **not** a baked tag param. The M7 ladder owns any context change (D5 64K operating applies only after the ladder).

**Enablement (T13):** `ollama` enabled (installer), `ollama-preload` enabled **after** the first-run pass (symlink in `multi-user.target.wants`). `is-enabled` → `enabled` ×2.

**Journal health (T14):** `journalctl -u ollama -p err --since 06:11` — **no error-level entries**; three WARN/INFO lines of the **hxs-1 F-E2 / hxs-2 F-J1 watchdog class** (`llama-server GPU discovery watchdog timed out` / `failure during llama-server GPU discovery` / `timed out waiting for server startup`, 06:21:17–06:21:19Z, first runner build; discovery retried and succeeded; load ended 100% GPU — F-J1, MONITOR). Kernel: **`NVRM: Xid` = 0 this boot and all boots**; OOM = 0; `NRestarts=0`.

**Hygiene (T16):** `systemctl --failed` → 0; listeners `:22`, `*:11434`, loopback runner port, stub DNS (no other exposure); uptime continuous 13:59+ (**no reboot**); swap 0 B used; RAM 3.0 Gi used / 59 Gi available; root 33 G used / 3.4 T free; models dir 17 G.

## 7. Reachability matrix (T15; FACT, 06:24Z)

| Origin | Target | Result |
| --- | --- | --- |
| hxs-3 loopback | `http://127.0.0.1:11434/api/version` | `{"version":"0.32.15"}` ✓ |
| hxs-5 (LAN, local curl) | `http://192.168.50.202:11434/api/version` | `{"version":"0.32.15"}` ✓ |

Endpoint posture per D2 + blueprint §5: wildcard bind with loopback preserved; no host firewall (owner rule — none created, none exists); the private 192.168.50.0/24 LAN is the boundary; no service-layer auth (as designed and ratified).

### 7.1 Link-speed telemetry (T17; FACT — state-log row-2 PCIe caveat)

`nvidia-smi --query-gpu=pcie.link.gen.current,pcie.link.gen.max,pcie.link.width.current,pcie.link.width.max` (per GPU), model resident:

| State | GPU0 gen cur/max | GPU1 gen cur/max | width cur/max (both) | Note |
| --- | --- | --- | --- | --- |
| Resident, idle | 1 / 3 | 1 / 3 | **8 / 16** | ASPM downshift to Gen1 (2.5 GT/s) at idle |
| Resident, **under smoke-inference load** | **3 / 3** | **3 / 3** | **8 / 16** | full Gen3 (8.0 GT/s) negotiated under load; power draw spiked to ~82 W / ~77 W during active generation |

**INFERENCE:** the idle Gen1 reading is power-management downshift, not a wiring limit — both links train to their Gen3 ceiling under load. The **x8 width against the x16 device max is the hard wiring constraint** (row-2 caveat confirmed live under load: ~Gen3 x8 per card). This is the capacity variable the M4 telemetry requirement and the M7 ladder must carry; it does not block M4 (model loads 100% VRAM across both GPUs and serves).

### 7.2 Smoke inference — known-answer (T18; FACT, 06:26Z)

- Request: `POST /api/chat` model `hx-muse-glimmer`, user message `Compute 17 * 23. Reply with only the final number.`, `stream:false`, `keep_alive:-1`, `think:false` (request-level response shaping only — no server/default change; D8 reasoning mapping remains M5 scope).
- Result: **HTTP 200 in 41.47 s**; `message.content` = **`391`** (17 × 23 = 391 — known-answer **PASS**); `message.thinking` **absent** (the flag was honored for this turn; nothing required stripping — only the final content is retained in evidence regardless); eval_count 38, prompt_eval_count 70.
- The remote response file was deleted after extraction; no model output beyond the final answer is retained.

## 8. Configuration files (profile §11.2)

| File | Pre-change | sha256 (pre) | sha256 (post) | Owner/mode |
| --- | --- | --- | --- | --- |
| `/etc/systemd/system/ollama.service` | absent | — (absent) | `11758d469d3f103e53a9612a8ffcb3a3e61834c994c08d412bb051f3c827dbd3` | root:root 0644 (reviewed installer) |
| `/etc/systemd/system/ollama.service.d/hx3.conf` | absent (dir absent) | — (absent) | `b4f98c2f829bc7ba86690e8bfbc73748a2c4b858425e37593aa1402b7a20627c` | root:root 0644 |
| `/etc/systemd/system/ollama-preload.service` | absent | — (absent) | `3b0e00b62163c536626ee79dafecdc144b01c7b17214baae74986bd9b44ca5f6` | root:root 0644 |
| `/usr/local/libexec/hx-ollama-preload` | absent (dir absent) | — (absent) | `d37dc30fb43ebfe674db37fdd963f219a4ef31867512a549558db930559dfd84` | root:root 0755 |
| `Modelfile` (alias source, transient `/tmp` copy) | absent | — (absent) | `0504cecd5cfdb70a6e203d7fc209d1f0c1040403fdfe5eb15005e74782ad3068` | hxsa:hxsa 0644 (remote copy removed after create) |

Installer-written `/etc/systemd/system/ollama.service` (byte-copy):

```ini
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

[Install]
WantedBy=default.target
```

All five files are **creations from a null pre-state** — unified diff against `/dev/null` equals full content; the operative contents are inlined verbatim in §5.5, §5.6, §5.7, and above (diff patch retained in session evidence `25-config-diffs.patch`, sha256 `590c5ef0e3083b1db39bce00354a72cec5cb464644c8c64f6b30a5f293f3a17f`). Effective runtime values post-reload: §5.6 (`systemctl show` + server-config env line). Install method: `sudo -n install -o root -g root -m 0644/0755 [-D]` from hash-verified candidates (remote hashes matched local before install; `/tmp` transfer copies removed after). `sudo -n systemctl daemon-reload` after file placement.

## 9. Findings register

- **F-J1 (carried class, MONITOR):** `llama-server` GPU-discovery watchdog timeout during the first runner build (06:21:17–06:21:19Z) — same class as hxs-1 F-E2 and hxs-2 F-J1. Retried and succeeded; the load completed 100% GPU. It contributes to runner-start latency and is inside the 42.5 s first-run measurement; the D5 budget absorbs it with wide margin (42.5 s ≪ 538 s). Watch at M5/M7, as on hxs-1/hxs-2.
- **F-J2 (record — ctx provenance):** no `num_ctx` is baked in the tag; effective `context_length 32768` is Ollama 0.32.15's **VRAM-based default** (`vram-based default context … default_num_ctx=32768`, 30.9 GiB total VRAM) — deterministic for this hardware+model, not an HX override. M7 ladder owns context changes (D5 64K operating only after the ladder).
- **F-J3 (record):** no license blob in the pulled manifest; license identity is publisher-declared Apache-2.0 (§5.4). Same class as hxs-2 F-J5.
- **F-J4 (decision record):** upstream latest v0.33.0 observed (state log row 7) and deliberately not taken; pinned 0.32.15 (§5.1).
- **F-J5 (record):** `think:false` was honored at request level for the smoke turn (no thinking field emitted); the operating reasoning default is unchanged — D8/`reasoning_strength` mapping probes remain M5 scope.
- **F-J6 (record):** first cold load via the preload unit = 42.5 s wall (page-cache cold, incl. rediscovery absorbed by Phase-1 probes). D5 accounting: 42.5 s observed ≪ 538 s script worst case < 600 s unit ≤ 900 s SLO.
- **F-J7 (record):** link telemetry (§7.1) — Gen3 under load on both cards; x8 width is the wiring ceiling (row-2 caveat confirmed under load). Carried as the M7 ladder's capacity variable.

## 10. Stop conditions and bounded corrections

Stop conditions (work order): wrong artifact family — **not hit** (family `muse-glimmer`, dense 27.9B, correct projector); Muse load failure — **not hit** (first-attempt cold load 42.5 s, 100% GPU); template/ATEM parser absent — **not hit** (template captured; `RENDERER glimmer` / `PARSER glimmer`; ATEM tokens present in the version-matched parser); GPU not visible — **not hit** (both discovered, both hold the model); service failure after bounded retry — **not hit**; any Xid — **not hit** (0 across all boots, re-verified at final poll). The llama.cpp fallback was **not** needed and no second serving plane was introduced. Bounded corrections: **0 of 1 used** (hxs-2 F-J2 code-span-unwrap and F-J3 `install -D` lessons pre-applied; no failed gate occurred).

## 11. Rollback notes (work-order scope; nothing executed)

Default rollback stops at units/config (model-store removal is a separately-approved step):

```bash
# 1. Preload unit: sudo systemctl disable --now ollama-preload.service
#    sudo rm /etc/systemd/system/ollama-preload.service /usr/local/libexec/hx-ollama-preload
# 2. Drop-in:    sudo rm /etc/systemd/system/ollama.service.d/hx3.conf
#    sudo systemctl daemon-reload && sudo systemctl restart ollama   # returns to loopback-only default
# 3. Alias:      ollama rm hx-muse-glimmer
# 4. Tag (separate approval required): ollama rm muse-glimmer:30b
# 5. Full uninstall (only if separately authorized; per linux.mdx):
#    systemctl stop/disable ollama; rm unit; rm /usr/local/bin/ollama /usr/local/lib/ollama;
#    rm ollama user; rm /usr/share/ollama
```

Byte-copies of every created config are inlined in this document (§5.2/§8 unit, §5.5 Modelfile, §5.6 drop-in, §5.7 script+unit) with pre/post sha256 (§8); pre-state was "no Ollama installed" (§3). No reboot is required in either direction.

## 12. Sequential command log (profile §11.3; sanitized)

All remote commands as `hxsa@hxs-3` from `hxs-5` over independent SSH sessions (askpass reads the credential-record row at execution time; `StrictHostKeyChecking=yes` against the pinned F-05 key; `NumberOfPasswordPrompts=1`); privileged steps via `sudo -n` (NOPASSWD). "local" = hxs-5. Times UTC.

| Seq | Time | Where | Command (shape) | Exit | Evidence |
| ---: | --- | --- | --- | ---: | --- |
| 1 | 06:00 | local | `hostname; date; whoami; ip` — session host hxs-5/.204 verified | 0 | §1 |
| 2 | 06:00–07 | local | read profile, WO/CP, AGENTS.mds, state log, rick M1, goal, blueprint, hxs-2 07-esme, hxs-1 35-esme, v1.1 §3.1/§3.4/§12; TKV survey; glimmer parser/renderer source; roster | 0 | §1 |
| 3 | 06:06 | local | `ssh-keygen -F 192.168.50.202`; ed25519 fingerprint == F-05 pin | 0 | header |
| 4 | 06:07 | local | read-only registry probes: manifest (prefix de878ce33ad8 MATCH), config, params blobs | 0 | §1, §5.4 |
| 5 | 06:07 | local | credential-file shape probes (line/field counts + row labels only — value never printed) | 0 | §12 note |
| 6 | 06:07 | local | build workspace `/tmp/.esme-m4-hxs3` (0700): askpass + rssh + rscp; askpass shape test (non-empty only) | 0 | §12 note |
| 7 | 06:08:05 | ssh | identity: hostname, `$SSH_CONNECTION`, machine-id, UUID, eno1, `sudo -n true`, date, uptime | 0 | §3 (T0a) |
| 8 | 06:08:30 | ssh | baseline: pre-install absent ×6, OS/kernel/mem/swap/df/GPUs/failed/Xid=0 | 0 | §3 (T1/T2) |
| 9 | 06:09 | local | download `ollama.com/install.sh`; sha256; `diff -q` vs TKV → byte-identical | 0 | §5.1 |
| 10 | 06:09 | ssh | transfer installer (remote hash match) | 0 | §5.1 |
| 11 | 06:10:14 | ssh | `OLLAMA_VERSION=0.32.15 sh …` → INSTALL_RC=0, "NVIDIA GPU installed." | 0 | §5.2 |
| 12 | 06:11 | ssh | T4 verify (0.32.15 binary==server, user, unit hash); T5 loopback-only + LAN refused; T6 both GPUs CUDA | 0 | §5.2/§5.3 |
| 13 | 06:11:27→14:59 | ssh | `ollama pull muse-glimmer:30b` (3m32.5s, success) | 0 | §5.4 |
| 14 | 06:15 | ssh | identity CLI set: `--version`, `list`, `show`, `show --modelfile` | 0 | §5.4 |
| 15 | 06:15 | ssh | `/api/show` verbose full JSON capture; `/api/tags` (frozen digest verbatim); blobs + on-disk manifest inventory | 0 | §5.4 |
| 16 | 06:16 | local | ollama.com library page → "licensed under Apache 2.0" | 0 | F-J3 |
| 17 | 06:18:00 | ssh | transfer Modelfile (hash match); `ollama create hx-muse-glimmer` → success (3 frozen layers reused) | 0 | §5.5 |
| 18 | 06:18 | ssh | alias verify: list/show/alias manifest/manifest hashes (3-way binding proof) | 0 | §5.5 |
| 19 | 06:18 | local | author hx3.conf + preload script + unit; `apt download shellcheck` + extract; **shellcheck CLEAN**; sh/dash/bash -n; candidate hashes | 0 | §5.7 |
| 20 | 06:19:24 | ssh | transfer 3 files (hash match); pre-state absent ×3; `install [-D]` ×3 → INSTALL-OK; `/tmp` copies removed; `daemon-reload`; post hashes root:root 0644/0755 | 0 | §8 |
| 21 | 06:20:06 | ssh | `restart ollama` → active; API OK attempt 7 (~20 s); bind `*:11434`; Environment exact; `TimeoutStartUSec=10min`; server-config env line | 0 | §5.6 |
| 22 | 06:21:14→21:56 | ssh | `systemctl start ollama-preload` → **RC=0, 42.5 s**; journal OK line with frozen digest | 0 | §6 |
| 23 | 06:22 | ssh | `/api/ps` (alias, exact digest, size==size_vram, ctx 32768, expires 2318); `ollama ps`; nvidia-smi per-GPU split | 0 | §6 |
| 24 | 06:22 | ssh | load-journal capture: `vram-based default context … 32768`; runner cmdline (frozen blobs, -np 1); watchdog class lines | 0 | §6, F-J1/F-J2 |
| 25 | 06:23 | ssh | `enable ollama-preload` → enabled ×2; journal scans (err=0, OOM=0, Xid=0, NRestarts=0); hygiene (0 failed, uptime, swap, df, du) | 0 | §6 |
| 26 | 06:24 | ssh+local | reachability: 127.0.0.1 OK; hxs-5→192.168.50.202:11434 OK; idle link speeds | 0 | §7, §7.1 |
| 27 | 06:25→26 | ssh | smoke inference (HTTP 200, 41.47 s) with concurrent link-speed/power polling under load | 0 | §7.1, §7.2 |
| 28 | 06:26 | ssh | smoke result extraction (`content='391'`, thinking absent); remote temp file removed | 0 | §7.2 |
| 29 | 06:28:05 | ssh | final re-check (6+ min post-pin): resident, exact digest, size==vram, ctx 32768, expires 2318, 0 unload/evict; NRestarts=0; Xid=0; unit byte-copy | 0 | §6, §8 |
| 30 | ~06:29+ | local | diffs generated; deliverable written; **workspace + askpass helper deleted** (no extracted credential copy ever existed) | — | §12 note |

Sanitization confirmed: no secret value was printed, logged, stored, or placed on any command line; the askpass helper (deleted at task end with the volatile workspace) read `ssh-info.md` line 25 pipe-field 3 (markdown code-span unwrapped — hxs-2 F-J2 lesson pre-applied) at execution time only. Every gate passed first attempt; there were no refused authentications and no failed commands to retain beyond the recorded expectations (§2).

## 13. Artifact hashes

```text
25f64b810b947145095956533e1bdf56eacea2673c55a7e586be4515fc882c9f  install.sh (== TKV ollama-main/scripts/install.sh)
11758d469d3f103e53a9612a8ffcb3a3e61834c994c08d412bb051f3c827dbd3  /etc/systemd/system/ollama.service (installer-written)
b4f98c2f829bc7ba86690e8bfbc73748a2c4b858425e37593aa1402b7a20627c  /etc/systemd/system/ollama.service.d/hx3.conf
3b0e00b62163c536626ee79dafecdc144b01c7b17214baae74986bd9b44ca5f6  /etc/systemd/system/ollama-preload.service
d37dc30fb43ebfe674db37fdd963f219a4ef31867512a549558db930559dfd84  /usr/local/libexec/hx-ollama-preload
0504cecd5cfdb70a6e203d7fc209d1f0c1040403fdfe5eb15005e74782ad3068  Modelfile (alias source)
muse-glimmer:30b        digest de878ce33ad81d060001db1469a02eebe4d86f0ad58cfe52dc062fdcbe4464c1  (FROZEN IDENTITY)
hx-muse-glimmer:latest  digest 472ad84e752d0319b65d6fcd862c26c3850cc408b6b9430046db31250994ad99  (alias; blob-bound to the frozen identity)
hxs-3 host key (pinned, rick M1 F-05)  ED25519 SHA256:R/3mdfv7J0Fajo8yryT7JB6B4EoBm47W2rLX+siHEog
```

## 14. Validation summary (profile §11.4)

- **What changed:** Ollama **0.32.15 pinned-installed** on hxs-3 (user `ollama`, upstream unit); drop-in `hx3.conf` applied (`OLLAMA_HOST=0.0.0.0` loopback-preserved, `NO_CLOUD=1`, `NUM_PARALLEL=1`, `MAX_LOADED_MODELS=1`); model `muse-glimmer:30b` pulled and **identity-frozen** (`de878ce33ad8…64c1`); alias `hx-muse-glimmer` created FROM-only and **blob-bound** to the frozen artifact (`472ad84e752d…ad99`); preload script + unit installed at D5 budgets (538 s < 600 s ≤ 900 s) and enabled.
- **What did not change:** OS/driver/kernel/DKMS/packages (rick's plane incl. sleep masks, rfkill), network/firewall/DNS (**no firewall anywhere — owner rule verified, none created**), storage topology, Secure Boot state, **no reboot** (uptime continuous), no other models/tags, no context or sampling changes anywhere (baked tag params verbatim; ctx = server VRAM-default, untouched), no model-store deletions, no second serving plane.
- **Tested:** T0a–T18 (19 tests): identity, pin, installer authenticity, install, loopback-before-LAN, GPU visibility, pull, full identity freeze (incl. template/renderer/parser + ATEM presence + CLIP projector), alias binding (3-way), drop-in effective state, preload lint + first run + enablement, residency (alias + exact digest + 100% VRAM both GPUs + ctx + Forever), journal health, reachability matrix, link-speed-under-load telemetry, smoke known-answer, hygiene.
- **Passed:** 19/19. **Failed:** none. **Not run:** none mandatory (reasoning-mapping probes M5; quality suites M5/M6; context ladder M7; restart/reboot recovery M8).
- **Current Ollama state:** 0.32.15 binary==server, active/enabled, `NRestarts=0`, wildcard bind with loopback preserved, cloud disabled.
- **Current model state:** `hx-muse-glimmer:latest` resident, digest `472ad84e752d0319b65d6fcd862c26c3850cc408b6b9430046db31250994ad99`, 100% VRAM (size == size_vram 17,839,465,428 B) across **both** 5060 Ti (10,170 + 8,908 MiB), ctx 32768 (VRAM-based default, F-J2), Forever.
- **Endpoint/security state:** `*:11434` (0.0.0.0 incl. loopback); reachable from 127.0.0.1 and from hxs-5 over the /24; no host firewall per owner rule; no service-layer auth (ratified posture); no credentials in any file.
- **Resource state:** RAM 3.0 Gi used; swap 0 B; root 3.4 T free; zero Xid all boots; link Gen3-under-load / x8-wired both cards (§7.1).
- **Rollback readiness:** §11 inverses exact; pre-state "no Ollama"; every artifact hashed; byte-copies inlined.
- **Remaining risks/decisions:** F-J1 watchdog class (monitor at M5/M7); F-J2 ctx default recorded for the M7 ladder; F-J7 x8 capacity variable carried to M7; Carol catalog receipt (handoff gate per context packet — OPEN until the receipt is cited in the state log).

**Second Brain evaluation (standing directive, per work order):** (1) opportunity identified — yes; (2) pattern — hxs-1/hxs-2 M4 install pattern (**third validated use**) + the Meta-X capability record; (3) disposition — **implemented**: the identity freeze (frozen digest pair + blob-binding proof + renderer/parser/projector identity) and the unit contracts become the Meta-X catalog spine at handoff; (4) evidence — three hosts, one shape: the blueprint's uniformity claim held again (19/19 first-pass, zero bounded corrections consumed); the divergences found (VRAM-default ctx 32768 vs hxs-2's baked 32768; x8 link width vs hxs-2) are recorded facts for the catalog, not defects. This deliverable goes to Carol for catalog receipt; handoff OPEN until the receipt is cited in the state log.

`PASS — TASK COMPLETE`

```text
Task May Proceed: YES
```

Signed: **john / Esme** — Expert Ollama Engineer, session `john-m4-20260826-01`, 2026-08-26T06:29Z (UTC).
