# Esme (john) — M4 Ollama Install Evidence (hxs-1)

| Field | Value |
| --- | --- |
| Report ID | ESME-M4-EVIDENCE-001 |
| Task ID | WO-HX1-JOHN-M4-001 (`PILOT-HX1-OLLAMA-QWEN27B-001`, milestone M4) |
| Agent | john / Esme (session `john-m4-20260825-01`) |
| Host | `hxs-1` (192.168.50.200), Ubuntu 24.04.4 LTS, kernel 7.0.0-28-generic |
| Session host | `hxs-5` (192.168.50.204); all target actions over SSH `hxsa@192.168.50.200` |
| Window | 2026-08-25T00:37Z → 01:05Z (UTC) |
| Ollama | 0.32.15 (binary == server; installed this session) |
| Model | `qwen3.8:27b` digest `22130167c4c2…79643`, alias `hx-qwen3.8-27b:latest` digest `23508b9c2439…185a8` |
| GPUs | 2× RTX 4070 Ti SUPER 16376 MiB, driver 580.173.02 (rick's plane, untouched) |

Evidence labels per plan §2.2: FACT / AUTHORITY / UPSTREAM / INFERENCE / RECOMMENDATION.
All secrets are excluded; the sudo/SSH credential was never printed, logged, or stored (§14).

---

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path resolves locally here)
Source: /opt/tkv-local/ollama
Reviewed At: 2026-08-25T00:39:05+00:00 → 00:41Z
Relevant Files: 8 reviewed of the corpus —
  ollama-main/scripts/install.sh                    (sha256 25f64b81…82c9f, installer baseline)
  ollama-main/docs/linux.mdx                        (install/unit/user/uninstall procedure)
  ollama-main/docs/faq.mdx                          (keep_alive, multi-GPU placement, flash attention)
  ollama-main/docs/context-length.mdx               (context defaults; ollama ps PROCESSOR/CONTEXT)
  research/hx-research_qwen38-27b-ollama-serving-and-capability-fit_synthesis_2026-08-17 (artifact register, digests)
  research/hx-research_qwen38-27b-quantization-ladder-and-artifact-resolution_synthesis_2026-08-17 (sizes, KV room)
  implementation/archive/HX-Infrastructure-main/tests/ai-runtime/fixtures/16-long-context-serialization.json (serialization-only)
  implementation/archive/HX-Infrastructure-main/tests/ai-runtime/ (fixture suite overview)
Authority/Version Identified: TKV source snapshot = Ollama v0.32.11 reference (profile §2.3);
  reconciled against installed 0.32.15 — see §8 finding F-E7.
Applicable Tests/Runbooks: plan §10.1 install sequence; profile §7.1/§7.2 test suites; linux.mdx unit template.
Contradictions or Gaps:
  1. TKV fixture F16 is serialization-only ("explicitly_not_proven: runtime acceptance") — no TKV runtime
     near-32K fixture exists; a bounded needle probe was constructed for T4 (§5), labeled INFERENCE-free FACT.
  2. TKV research (2026-08-17) notes the default qwen3.8:27b tag is the MTP variant; KDD-0004 (AUTHORITY)
     approves exactly qwen3.8:27b. Live pulled digest MATCHES the TKV register short digest (§6). No conflict.
  3. Pulled model metadata requires Ollama >= 0.32.12; TKV snapshot reference is 0.32.11 — installing the
     current release was therefore REQUIRED, not a drift choice (§8 finding F-E7).
Task May Proceed: YES
```

Rick handoff validation (plan §10.1 step 1): `08-rick-risk-handoff.md` signed 2026-08-25T00:15Z.
No CRITICAL risk open. OPEN items are assigned to M4–M7 scope and testable here: R-005 (Esme —
both-GPU proof, §5 T5), R-015/R-023 (joint — preload alert-not-loop honored, §4 script design),
R-024 (Rick, monitor-only). R-001 closed by KDD-0004 + digest capture. R-008 mitigation (loopback)
implemented and proven in this milestone (§5 T0b). **Verdict: proceed.**

## 2. Test plan (profile §6.1 — recorded before first mutation)

| ID | Property | Procedure | Expected | Pass rule | Result |
| --- | --- | --- | --- | --- | --- |
| T0a | Pre-install state | profile §6.2 probes | no ollama bin/user/unit/listener; GPU UUIDs match handoff | exact match to `07`/`08` baselines | PASS |
| T0b | Loopback before pull | `ss -lntp`, `/api/version`, `/api/tags`, LAN-IP connect attempt | listener `127.0.0.1:11434` only; LAN connect refused | bind loopback-only AND API answers | PASS |
| T1 | Installer authenticity | download, sha256, full read, diff vs TKV | HTTPS origin ollama.com; hash == TKV `scripts/install.sh`; no driver/package authority in our path | hash match AND logic inspection clean | PASS |
| T2 | Install + identity | run reviewed installer; `ollama --version`, `/api/version`, `id ollama`, `systemctl cat` | binary==server version; system user `ollama` no-login; unit per upstream | all checks pass; no driver touch | PASS (0.32.15) |
| T3 | Model identity freeze | pull `qwen3.8:27b`; `/api/tags`, `ollama show`, storage delta | digest matches TKV register short `22130167c4c2`; Q4_K_M GGUF | digest match AND fields captured | PASS |
| T4 | Alias + Modelfile | verbatim Modelfile (plan §6.5), sha256, `ollama create`, `ollama show` | alias `hx-qwen3.8-27b` with num_ctx 32768 + frozen parameters | sha256 recorded; show matches plan | PASS |
| T5 | Drop-in effective state | install `hx1.conf`, daemon-reload, restart, `systemctl show`, journal env line | all plan §4.2 values effective; both UUIDs; NO_CLOUD=1 | effective Environment + startup log match | PASS |
| T6 | Preload script/unit | lint; install; manual non-reboot start; `/api/ps` assertion; then enable | model loaded + asserted resident; unit SUCCESS; enabled only after pass | lint pass + unit SUCCESS + ps match | PASS (27.1 s) |
| T7 | Smoke (8,192 ctx) | generate with `num_ctx=8192`, known answer 17×23 | response `391`; ps CONTEXT 8192 100% GPU | correct answer AND ps state | PASS |
| T8 | Cold start | one controlled `keep_alive:0` unload → preload-script reload | ps empties; reload via unit; residency re-proven at 32768 | unload proven AND reload proven | PASS (9.7 s) |
| T9 | Warm known-answer | same prompt on resident model | `391` with load_duration ≈ 0 | answer correct AND no reload | PASS (load 1 ms) |
| T10 | Near-32K probe | needle-in-haystack 29,789-token prompt | needle retrieved; no OOM; no CPU fallback | exact needle AND 100% GPU | PASS |
| T11 | Both-GPU allocation | `nvidia-smi` per-GPU at rest and under load | both GPUs hold model; both active under load | mem.used > 0 on both under load | PASS (10.4+10.5 GiB) |
| T12 | Idle residency | ≥6 min idle, no requests | model resident past default 5-min eviction | ps unchanged after ≥6 min | PASS (6.7 min) |
| T13 | Journal health | `journalctl -u ollama`, `journalctl -k` scans | no Xid, no OOM, no service restart | zero Xid/OOM; NRestarts=0 | PASS with findings F-E2/F-E3 |

Rollback trigger mapping: any FAIL above → stop, preserve, escalate (profile §13). None triggered.

## 3. Pre-change baseline (FACT, 2026-08-25T00:42:58Z)

- `hostnamectl --static` = `hxs-1`; peer `192.168.50.200`; kernel `7.0.0-28-generic`; up 7 d 1:55.
- No Ollama: `command -v ollama` empty; `systemctl status ollama` "could not be found"; `id ollama` no such user; `/usr/share/ollama` absent; no `:11434` listener; `dpkg -l | grep -i ollama` empty.
- GPUs: `GPU-2ace9bfc-3a2d-f5b9-d270-82d043f8a7b7` (idx 0), `GPU-d675a1cd-7d3d-0903-3b1b-7d95f321a0a9` (idx 1), both RTX 4070 Ti SUPER 16376 MiB, 0 MiB used, driver 580.173.02 — exact match to rick's handoff §1.
- RAM 125 Gi total / 122 Gi free; swap 8 G unused; root ext4 3.4 T free (14 G used); sleep targets `masked` (re-asserted per handoff §3).
- Listeners: `:22` and loopback stub DNS only — matches rick §6.9.

## 4. Implementation record

### 4.1 Installer review (profile §7.1; plan §10.1 step 3) — before execution

- FACT: `curl -fsSL https://ollama.com/install.sh` → sha256 `25f64b810b947145095956533e1bdf56eacea2673c55a7e586be4515fc882c9f` (455 lines), **byte-identical** to TKV `ollama-main/scripts/install.sh` (same sha256). Served over HTTPS from ollama.com. AUTHENTICITY ESTABLISHED.
- FACT (full read): on this host the script (a) extracts `ollama-linux-amd64.tar.zst` to `/usr/local`; (b) creates system user `ollama` (`useradd -r -s /bin/false -U -m -d /usr/share/ollama`), adds it to `render`+`video`, adds invoking user to `ollama`; (c) writes `/etc/systemd/system/ollama.service`, enables + starts it; (d) line 294–297: `check_gpu nvidia-smi` succeeds → `exit 0` **before** all CUDA-driver/DKMS/modprobe/apt logic (lines 318–449), which is unreachable here; ROCm download only on AMD detection — unreachable.
- FACT: prerequisites `curl zstd awk grep sed tee xargs` all present on hxs-1; `https://ollama.com/download/ollama-linux-amd64.tar.zst` reachable (HTTP 200).
- INFERENCE: the installer cannot become GPU-driver or OS-package authority on hxs-1 (working `nvidia-smi`); its mutations are exactly: `/usr/local/{bin,lib/ollama}`, the `ollama` user/group + two group memberships, one systemd unit, enable+start. All inside WO scope ("user/group changes beyond what the reviewed installer itself creates" prohibited — the installer's own are authorized).
- Never blind-piped: transferred as a file, reviewed in full, then executed (`sudo -v` credential cache; script run as hxsa so its inner `sudo` and `whoami` semantics stay upstream-intended).

### 4.2 Install result (FACT, 00:44:42Z → 00:45:06Z)

- `ollama version is 0.32.15`; `/api/version` = `0.32.15` (binary == server). Model metadata later showed `requires 0.32.12` — satisfied.
- `id ollama` = `uid=999(ollama) gid=988(ollama) groups=988(ollama),44(video),993(render)` — system user, `/bin/false` shell, home `/usr/share/ollama` (`drwxr-x--- ollama:ollama`). Matches rick R-014 expectation; no group change needed for CUDA (world-rw nodes); installer-added memberships are its own default.
- Unit: upstream default (`/etc/systemd/system/ollama.service`, `ExecStart=/usr/local/bin/ollama serve`, `User/Group=ollama`, `Restart=always/3s`), `enabled`, `active`.
- Output ended `>>> NVIDIA GPU installed.` — driver logic confirmed skipped; zero apt/dkms/modprobe activity.

### 4.3 Loopback proof BEFORE pull (FACT, 00:46:01Z) — plan §10.1 step 5

- `ss -lntp`: `LISTEN 127.0.0.1:11434` (only). `curl http://192.168.50.200:11434/api/version` → connection refused (0 ms).
- `/api/version` OK; `/api/tags` empty; journal: `Listening on 127.0.0.1:11434 (version 0.32.15)`.

### 4.4 Model pull and identity freeze (FACT, 00:46:30Z → 00:49:16Z)

- `ollama pull qwen3.8:27b` — success in **165.6 s**; sha256 digest verified by client during pull.
- `/api/tags` frozen identity:

| Field | Value |
| --- | --- |
| Tag (AUTHORITY KDD-0004) | `qwen3.8:27b` |
| Digest (sha256) | `22130167c4c20e20c7b71454612966ca8e8171e9b3cc8ab6ce8aa6cbfec79643` |
| TKV register short digest (2026-08-17) | `22130167c4c2` — **MATCH** |
| Format / family | `gguf` / `qwen35` |
| Parameter size | 27.3B |
| Quantization | `Q4_K_M` |
| Size | 17,741,872,154 bytes (16.52 GiB) |
| Model max context | 262,144 |
| Capabilities | completion, tools, thinking, vision |
| parent_model (FACT) | `qwen3.8:27b-q4_K_M` |
| License | Apache License 2.0 |
| Requires | Ollama ≥ 0.32.12 (installed 0.32.15) |

- Storage delta (D1 honored, root ext4): `/` used 14 G → 32 G; models dir `17G`; free still 3.4 T. Path `/usr/share/ollama/.ollama/models` owned `ollama:ollama` (verified before pull).

### 4.5 Modelfile + alias (FACT)

- Modelfile **verbatim plan §6.5** (FROM/8 PARAMETERs/SYSTEM), sha256:
  `dac63d7c3e096585c8b65261bbf139201e384280e40369536963d8439db1d1df` (identical on hxs-5 copy and hxs-1 `/tmp/esme-m4/Modelfile`).
- `ollama create hx-qwen3.8-27b` → alias digest `23508b9c243979f6538b2e71c69ccbcd4f905d5a6313e64b6b108069a15185a8`, size 17,741,872,435 bytes.
- `ollama show hx-qwen3.8-27b` confirms: `num_ctx 32768`, `temperature 0.6`, `top_p 0.95`, `top_k 40`, `min_p 0`, `repeat_penalty 1.05`, `repeat_last_n 256`, `num_predict 8192`, SYSTEM prompt verbatim, base identity unchanged.

### 4.6 systemd drop-in (FACT) — plan §4.2 at 32K

`/etc/systemd/system/ollama.service.d/hx1.conf` (root:root 0644, sha256 `36af1c4212d4797eaa455013ce02f853d3c913554c3b42bde4e6f52783460f38`):

```ini
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_KEEP_ALIVE=-1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_CONTEXT_LENGTH=32768"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_KV_CACHE_TYPE=f16"
Environment="OLLAMA_NO_CLOUD=1"
Environment="CUDA_VISIBLE_DEVICES=GPU-2ace9bfc-3a2d-f5b9-d270-82d043f8a7b7,GPU-d675a1cd-7d3d-0903-3b1b-7d95f321a0a9"
Restart=always
RestartSec=3
TimeoutStartSec=300
LimitNOFILE=65535
```

Effective state after daemon-reload + restart (00:50:07Z), `systemctl show`:
`Environment=PATH=… OLLAMA_HOST=127.0.0.1:11434 OLLAMA_KEEP_ALIVE=-1 OLLAMA_MAX_LOADED_MODELS=1 OLLAMA_NUM_PARALLEL=1 OLLAMA_CONTEXT_LENGTH=32768 OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=f16 OLLAMA_NO_CLOUD=1 CUDA_VISIBLE_DEVICES=GPU-2ace9bfc-3a2d-f5b9-d270-82d043f8a7b7,GPU-d675a1cd-7d3d-0903-3b1b-7d95f321a0a9`; `LimitNOFILE=65535`; `TimeoutStartUSec=5min`; `User/Group=ollama`; `NRestarts=0`; `DropInPaths=/etc/systemd/system/ollama.service.d/hx1.conf`.
Server startup log confirms uptake: `OLLAMA_KEEP_ALIVE:2562047h47m16.854775807s` (∞), `OLLAMA_FLASH_ATTENTION:true`, `OLLAMA_KV_CACHE_TYPE:f16`, `OLLAMA_CONTEXT_LENGTH:32768`, `OLLAMA_MAX_LOADED_MODELS:1`, `Ollama cloud disabled: true`, both UUIDs as `filter_id`, both GPUs `inference compute … library=CUDA compute=8.9 … total 15.6 GiB available 15.4 GiB`; Intel iGPU dropped (Vulkan, expected).
Plan §4.2 rule 2 (PILOT-002) honored: effective context is proven via the Modelfile contract — `/api/ps` `context_length: 32768` (§5), not assumed from the variable.

### 4.7 Preload script + unit (FACT) — plan §4.3

- `/usr/local/libexec/hx-ollama-preload` (root:root 0755, sha256 `79571d639b6acee53d08692b1d1538d506a145784236e2413f681d1a7eb7262a`):

```sh
#!/bin/sh
# hx-ollama-preload — PILOT-HX1-OLLAMA-QWEN27B-001 (plan section 4.3)
# Loads the exact pilot model with keep_alive=-1, then asserts /api/ps residency.
# Bounded retry (12 retries x 5 s delay), hard per-request timeout (900 s).
# On exhaustion it FAILS (alert path per handoff R-015/R-023); it never loops.
# No credentials are embedded or required (loopback-only API).
set -eu

MODEL="hx-qwen3.8-27b"
API="http://127.0.0.1:11434"

# Step 1: bounded load request; empty prompt only loads and pins the model.
curl -fsS --retry 12 --retry-all-errors --retry-delay 5 \
  --connect-timeout 3 --max-time 900 \
  "$API/api/generate" \
  -H 'Content-Type: application/json' \
  -d "{\"model\":\"$MODEL\",\"prompt\":\"\",\"stream\":false,\"keep_alive\":-1}" \
  -o /dev/null

# Step 2: readiness assertion — the exact model must be resident.
ps_json=$(curl -fsS --connect-timeout 3 --max-time 30 "$API/api/ps")
printf '%s' "$ps_json" | grep -q "\"name\":\"$MODEL:" || {
  echo "hx-ollama-preload: FAIL - $MODEL not resident in /api/ps after bounded load" >&2
  exit 1
}
echo "hx-ollama-preload: OK - $MODEL resident"
```

- `/etc/systemd/system/ollama-preload.service` (root:root 0644, sha256 `28c60c7d7f955ce85c36223b08691617a383451d62fc28b05b20a05caa052299`) — verbatim plan §4.3 (`After=network-online.target ollama.service`, `Requires=ollama.service`, `Type=oneshot`, `RemainAfterExit=yes`, `TimeoutStartSec=1200`, `WantedBy=multi-user.target`). No credentials in either file.
- Lint: `sh -n`, `bash -n`, `dash -n` all PASS. `shellcheck` unavailable on hxs-5 and hxs-1 (no ensurepip for an isolated venv; apt install out of scope) — limitation recorded (F-E6); the manual functional test is the real gate.
- Manual non-reboot test (00:51:23Z): `systemctl start ollama-preload.service` → `PRELOAD_RC=0` in **27.1 s** (first-ever cold load), journal `hx-ollama-preload: OK - hx-qwen3.8-27b resident`, unit `active (exited) status=0/SUCCESS`.
- Enabled only after the pass: `systemctl enable ollama-preload.service` → `enabled` (symlink in `multi-user.target.wants`).

## 5. Test execution results (FACT unless labeled)

- **T7 smoke 8,192** (00:52:41Z): generate `num_ctx=8192`, temperature 0 → response `'391'` (17×23). `ollama ps`: `CONTEXT 8192`, `100% GPU`. Note: with `MAX_LOADED_MODELS=1` the 8192-ctx request evicts/reloads the runner (expected; load 14.0 s); first attempt with `num_predict=16` returned empty `response` because thinking consumed the cap (F-E8) — re-run with 64 tokens gave the correct answer.
- **Residency snapshot** (00:52:00Z): `/api/ps` → `hx-qwen3.8-27b:latest`, `size 19,637,657,924`, `size_vram` = size (100% VRAM), `context_length 32768`, `expires_at 2318-…` (keep_alive=-1). `ollama ps`: `100% GPU`, `CONTEXT 32768`, `UNTIL Forever`.
- **T8 cold start** (00:53:36Z): the one authorized controlled unload (`keep_alive:0`) → `/api/ps` `{"models":[]}`, both GPUs 1 MiB — unload proven. Preload-unit reload: first attempt via `systemctl start` was a **no-op** (unit already `active (exited)` with `RemainAfterExit=yes`; F-E4 — recovery must use `restart`). `systemctl restart ollama-preload.service` → RC=0 in **9.7 s**; residency re-proven: `CONTEXT 32768`, `100% GPU`, `size_vram 18,987,394,004`, GPUs 10,350 + 10,480 MiB.
- **T9 warm known-answer** (00:54:30Z): `'391'`, `load_ms=1`, prompt 221 ms, eval 774 ms, total 998 ms — no reload.
- **T10 near-32K probe** (00:55:35Z–00:57:46Z): needle-in-haystack — 1,350 numbered filler lines, needle `The authorization code for the HX-1 pilot gate is ZEBRA-74291.` at line 675; question at end. `prompt_eval_count 29,789` tokens (90.9% of the 32,768 contract), first full prompt eval 22.0 s (≈1,354 tok/s). Deterministic answer with `think:false`, temperature 0: **`'ZEBRA-74291'`**, `done_reason: stop`. No OOM, no truncation, `100% GPU` throughout. (Two thinking-mode attempts returned empty responses with `done_reason: length` at 32/512 thinking tokens — F-E8; capacity itself was already proven by the first run's full 29,787-token eval.)
- **T11 both-GPU allocation**: resident split GPU0 10,630 / GPU1 11,100 MiB (first load), 10,350/10,480 (reload), 10,364/10,502 (probe, idle). Under probe load: util GPU0 84% ↔ GPU1 100% (alternating scheduler activity on **both**). PCIe link widths under load: GPU0 x16, GPU1 x4 — FACT consistent with rick's wired-x4/chipset inference (recorded, not judged; R-005 item (b) answered: not an idle-ASPM artifact). No 50/50 claim made (plan §5.1).
- **T12 idle residency** (01:04:21Z): ≥6.7 min after the last request the model remains resident — `100% GPU`, `CONTEXT 32768`, `Forever`, GPUs unchanged, no unload/evict events in journal. Default 5-min eviction defeated by `KEEP_ALIVE=-1` as designed.
- **T13 journal health**: zero `NVRM: Xid`, zero OOM(-kill/-reaper), `NRestarts=0`, service active since 00:50:07Z. Findings F-E2/F-E3 below are warnings, recorded openly.
- **System state after suite**: RAM used 5.0 Gi / 120 Gi available; swap 0 B; no CPU offload (RSS trivial); listener still `127.0.0.1:11434` only.

## 6. Configuration files (profile §11.2)

| File | Pre-change | Post-change | sha256 (post) |
| --- | --- | --- | --- |
| `/etc/systemd/system/ollama.service` | absent | installer default unit (§4.2) | — (upstream text in §4.2) |
| `/etc/systemd/system/ollama.service.d/hx1.conf` | absent (dir absent) | §4.6 text | `36af1c42…60f38` |
| `/etc/systemd/system/ollama-preload.service` | absent | plan §4.3 verbatim | `28c60c7d…52299` |
| `/usr/local/libexec/hx-ollama-preload` | absent | §4.7 text | `79571d63…7262a` |
| Modelfile (source kept at `/tmp/esme-m4/Modelfile` on hxs-1; canonical copy in this repo below) | absent | plan §6.5 verbatim | `dac63d7c…1d1df` |

Diffs: all files are creations from a null pre-state (diff = full content, shown in §4). Effective runtime values post-reload: §4.6 (`systemctl show` + startup env line). Ownership/permissions: units 0644 root:root; script 0755 root:root; model store `ollama:ollama`. Rollback: `13-esme-rollback.md`.

## 7. Sequential command log (profile §11.3)

Session host `hxs-5`, user `hxsa`; all remote commands via SSH to `hxs-1`; secrets never on any command line (askpass + `sudo -S` stdin). Local-only steps: TKV reads (§1), installer download/hash/read (§4.1), artifact authoring (Modelfile/drop-in/script/unit), `sh/bash/dash -n` lints, probe JSON generation, transfers via `cat`-over-ssh (logged inline). Full remote log:

```text
 1 00:42:44 exit=0 sudo echo SUDO_OK; hostname
 2 00:42:57 exit=0 [baseline: date; hostname; os-release; uname; uptime; ollama probes; ss 11434]
 3 00:43:04 exit=0 [baseline: free; swapon; df; nvidia-smi -L + csv; sleep masks; dpkg; listeners]
 4 00:44:04 exit=0 [prereqs curl/zstd/awk/grep/sed/tee/xargs; HEAD download endpoint → HTTP 200]
 5 00:44:33 exit=0 transfer reviewed installer to hxs-1:/tmp/ollama-install-reviewed.sh
 6 00:44:42 exit=0 sudo -v && sh /tmp/ollama-install-reviewed.sh
 7 00:45:17 exit=0 [version; id ollama; systemctl cat/is-active/is-enabled ollama]
 8 00:46:01 exit=0 [ss 11434; /api/version; /api/tags; LAN-IP curl refused; journal listen line]
 9 00:46:14 exit=0 [journal GPU discovery; ls -ld model store; df]
10 00:47:38 exit=0 command -v shellcheck (absent); du models dir
11 00:46:30 exit=0 ollama pull qwen3.8:27b (165.6 s)
    [Correction 2026-08-25: step numbers record call order, not chronology — the pull
     (step 11, 00:46:30 + 165.6 s ≈ ends 00:49:16) ran concurrently with the
     independent read-only probes in step 10 (00:47:38); step 12 (00:49:24) is the
     first post-pull step. Provenance preserved; no entries altered.]
12 00:49:24 exit=0 [ollama list; /api/tags; ollama show; du; df]
13 00:49:45 exit=0 transfer Modelfile
14 00:49:53 exit=0 ollama create hx-qwen3.8-27b; ollama show; /api/tags
15 00:50:07 exit=0 sudo install hx1.conf; daemon-reload; restart ollama; is-active/is-enabled
16 00:50:16 exit=0 systemctl cat/show ollama (effective state)
17 00:50:26 exit=0 [api/version probe — ONE timeout during startup discovery, F-E1; journal; ss]
18 00:50:54 exit=0 [api/version retry OK; journal inference compute lines]
19 00:51:14 exit=0 transfer preload script + unit
20 00:51:14 exit=0 sudo install script (0755) + unit (0644); daemon-reload
21 00:51:23 exit=0 sudo systemctl start ollama-preload.service → RC=0, 27.1 s
22 00:52:00 exit=0 sudo systemctl enable ollama-preload.service → enabled
23 00:52:00 exit=0 /api/ps; ollama ps (residency snapshot)
24 00:52:41 exit=0 [nvidia-smi split; smoke generate num_ctx 8192 num_predict 16 → empty/thinking]
25 00:53:23 exit=0 [smoke re-run num_predict 64 → '391'; ollama ps CONTEXT 8192]
26 00:53:36 exit=0 [controlled keep_alive:0 unload; ps empty; GPUs 1 MiB]
27 00:53:50 exit=0 sudo systemctl start ollama-preload.service → no-op (F-E4)
28 00:53:50 exit=0 [ollama ps — still empty, no-op confirmed]
29 00:54:07 exit=0 sudo systemctl restart ollama-preload.service → RC=0, 9.7 s
30 00:54:17 exit=0 [ollama ps; /api/ps ctx 32768 vram 100%; nvidia-smi split]
31 00:54:30 exit=0 [warm known-answer → '391', load 1 ms]
32 00:55:24 exit=0 transfer probe.json
33 00:55:35 exit=1 [probe1 + nvidia-smi sampler — sampling shell exited early (F-E1 note); probe completed]
34 00:56:21 exit=0 [ls; pgrep curl; ollama ps — probe found completed]
35 00:56:32 exit=0 [probe1 result: 29,787 tokens evaluated; empty response/thinking cap]
36 00:57:02 exit=0 [probe2 num_predict 512 → thinking cap again; capacity re-proven]
37 00:57:32 exit=26 [probe3 curl -d @file failed — file not yet transferred; my sequencing error]
38 00:57:46 exit=0 [probe3 think:false → 'ZEBRA-74291', done_reason stop]
39 00:58:09 exit=0 [journal scans; NRestarts=0; free; swapon]
40 01:04:21 exit=0 [idle ≥6.7 min: ollama ps; /api/ps; nvidia-smi; unload-event grep — none]
```

Failed/transient steps kept per profile §15: steps 17 (one read-probe timeout), 24/35/36 (thinking-cap empty responses), 27 (start no-op), 33 (sampler exit), 37 (my transfer-sequencing error, corrected at 38).

## 8. Findings, risks, decisions surfaced

- **F-E1 (transient, benign):** one `/api/version` read probe timed out at 00:50:26 during post-restart GPU discovery (~47 s from restart to API-ready: restart 00:50:07 → version OK 00:50:54). Expected during CUDA init; retry succeeded. Also the T10 sampler shell exited early — the probe itself completed; evidence preserved.
- **F-E2 (WARN, watch at M5/M7):** `llama-server GPU discovery watchdog timed out` / `timed out waiting for server startup` (context deadline exceeded) during the first runner builds (00:51:26–27, 00:52:46–47). Discovery retried and succeeded every time; all loads ended 100% GPU. Contributes to runner-start latency (~20–27 s cold) — relevant to D5 accounting (§9) and the R-015/R-023 boot path.
- **F-E3 (driver plane → rick):** one-time kernel `NVRM: iovaspaceDestruct_IMPL: 4 left-over mappings` + `nvAssertFailedNoLog … io_vaspace.c:592/601` (4 lines) at 00:45:23, during the first-ever GPU probe by the installer-started server (pre-drop-in). NOT an Xid; did not recur across the drop-in restart and 4 subsequent load cycles; zero Xid/OOM in the full window. R-002-adjacent observation; no action taken (rick's plane).
- **F-E4 (operational, recorded for M5 recovery):** with `RemainAfterExit=yes`, `systemctl start ollama-preload.service` is a no-op while the unit is `active (exited)`. Recovery and tests must use `systemctl restart ollama-preload.service` (or stop+start). The unit works as designed on boot (units start inactive).
- **F-E5 (gap closed by construction):** no TKV runtime near-32K fixture (F16 is serialization-only); the needle probe used here is the session-constructed bounded alternative (29,789 tokens).
- **F-E6 (limitation):** shellcheck unavailable on both hosts; lint evidence is `sh -n` + `bash -n` + `dash -n` + passing manual functional test.
- **F-E7 (version reconciliation, profile §9):** TKV snapshot reference v0.32.11 vs installed 0.32.15 — same 0.32 line, +4 patch releases. The pulled model's metadata `requires 0.32.12` makes ≥0.32.12 mandatory, so the TKV snapshot could not have served this model; installing current was required. The TKV `install.sh` remains byte-current with upstream (hash match). Binary == server == 0.32.15. No silent substitution: stated openly per profile §3.
- **F-E8 (client guidance for M5+):** thinking is on by default; small `num_predict` caps are consumed by thinking (empty `response`, `done_reason: length`). Deterministic retrieval tests should set `think:false` or budget thinking tokens.
- **F-E9 (TKV note, no conflict):** TKV research flags the default `qwen3.8:27b` tag as the MTP variant (`draft_num_predict 4` present in live parameters; live `parent_model` = `qwen3.8:27b-q4_K_M`). Digest matches the TKV register exactly. KDD-0004 governs; MTP long-context utility is an M5+ quality question, not an M4 identity issue.
- **R-005 items (a)+(b) answered:** both-GPU allocation proven at rest and under load (§5 T11); GPU1 x4 width persists under load (wired/chipset, not ASPM). No 50/50 claim. Carried remainder (P2P-over-PCH performance) is M5 benchmarking scope.
- **Untouched per scope:** rick's plane (driver/kernel/DKMS/packages/masks), network/firewall/DNS, storage topology, no reboot (uptime continued 7 d+), no other tags, no MLX, no 64K promotion, no `OLLAMA_NUM_GPU`/`OLLAMA_GPU_LAYERS`, no bind beyond loopback.

## 9. Durations vs D5 SLO (AUTHORITY D5: detection ≤2 min, recovery ≤15 min, one bounded attempt)

| Measurement | Value | Basis |
| --- | ---: | --- |
| Service restart → API-ready (incl. GPU discovery) | ≈47 s | 00:50:07 restart → 00:50:54 version OK |
| First-ever cold load via preload unit (page-cache cold) | 27.1 s | T6 (00:51:23Z) |
| Controlled cold reload via preload unit (page-cache warm) | 9.7 s | T8 (00:54:07Z) |
| Worst-case automated recovery path (service restart + preload, observed components) | ≈47 s + ≈28 s ≈ **75–90 s** | sum of the two rows above |
| D5 recovery budget | ≤ 15 min (900 s) | AUTHORITY |

INFERENCE: the D5 recovery SLO (≤15 min) is **credible with ~10× headroom** on observed numbers; detection (≤2 min) is an M5 monitoring property, not exercised here. Caveat carried for M7: F-011/R-023 (boot carrier loss up to 33 min) can defeat any preload budget — the unit fails-and-alerts by design (bounded 12×5 s retry), it does not loop.

## 10. Validation summary (profile §11.4)

- **What changed:** Ollama 0.32.15 installed on hxs-1 (user `ollama`, upstream unit); drop-in `hx1.conf` applied (loopback, keep-alive ∞, 1 model, 1 parallel, ctx 32768, FA on, KV f16, NO_CLOUD, both GPU UUIDs, limits); model `qwen3.8:27b` pulled and frozen; alias `hx-qwen3.8-27b` created at num_ctx 32768 from the verbatim Modelfile; preload script + unit installed and enabled.
- **What did not change:** OS/driver/kernel/DKMS/packages (rick's plane incl. sleep masks), network/firewall/DNS, storage topology, Secure Boot state, system uptime (no reboot), any other model/tag.
- **What was tested:** T0a–T13 per §2 (15 tests incl. sub-tests): baseline, installer authenticity, install identity, loopback-before-pull, model freeze (digest match), alias/Modelfile, drop-in effective state, preload lint+manual test+enable, smoke 8192, cold start, warm known-answer, near-32K needle probe, both-GPU allocation, idle residency >6 min, journal health.
- **Passed:** all 15. **Failed:** none. **Not run:** none mandatory (three reboot cycles are M7 scope; 64K is Gate-3 scope).
- **Installed/running:** binary == server 0.32.15; `ollama.service` active+enabled, NRestarts=0; `ollama-preload.service` enabled, last run SUCCESS.
- **Model identity/residency:** §4.4 digests frozen; resident `hx-qwen3.8-27b:latest`, ctx 32768, 100% GPU (size_vram == size), Forever.
- **Endpoint/security state:** `127.0.0.1:11434` only; LAN connect refused; cloud disabled (`NO_CLOUD=1` effective); no auth assumed (loopback is the boundary, plan §6.2).
- **Resource/performance state:** split ≈10.4+10.5 GiB VRAM across both GPUs; RAM 5 Gi used; swap 0; prompt eval ≈1,354 tok/s at 29.8K ctx; warm short-answer ≈1 s.
- **Rollback readiness:** `13-esme-rollback.md`; pre-state was "no Ollama installed"; every artifact hashed; inverse steps exact.
- **Remaining risks/decisions:** F-E2 watchdog latency (M5/M7 watch), F-E3 one-time NVRM assertions (rick), F-E4 restart-not-start recovery note, F-E8 thinking-cap client guidance, F-E9 MTP question for M5 quality gates, R-015/R-023 boot-carrier exposure (M7).

**Completion: `PASS — TASK COMPLETE`** (final gate §18: every applicable question answered yes; F-E6 lint limitation and F-E1/F-E8 transients disclosed, none concealing a mandatory-test failure).

## 11. Artifact hashes

```text
25f64b810b947145095956533e1bdf56eacea2673c55a7e586be4515fc882c9f  install.sh (== TKV ollama-main/scripts/install.sh)
dac63d7c3e096585c8b65261bbf139201e384280e40369536963d8439db1d1df  Modelfile (plan §6.5 verbatim)
36af1c4212d4797eaa455013ce02f853d3c913554c3b42bde4e6f52783460f38  hx1.conf (drop-in)
79571d639b6acee53d08692b1d1538d506a145784236e2413f681d1a7eb7262a  hx-ollama-preload
28c60c7d7f955ce85c36223b08691617a383451d62fc28b05b20a05caa052299  ollama-preload.service
qwen3.8:27b        digest 22130167c4c20e20c7b71454612966ca8e8171e9b3cc8ab6ce8aa6cbfec79643
hx-qwen3.8-27b:latest digest 23508b9c243979f6538b2e71c69ccbcd4f905d5a6313e64b6b108069a15185a8
```

Sanitization confirmed: no secrets, tokens, cookies, private prompts, or user data in this document; synthetic probe content only; LAN addresses already ratified in plan §3.
