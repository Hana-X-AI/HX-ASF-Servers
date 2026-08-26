# 13 — Esme (john): fleet web-search enablement — OLLAMA_NO_CLOUD removal on hxs-1/2/3/4

`[TASK COMPLETE — EVIDENCE ATTACHED]`

| Field | Value |
| --- | --- |
| Report ID | ESME-FLEET-WS-001 |
| Task ID | WO-FLEET-JOHN-WS-001 (`PILOT-HXS2-CODERX-BACKEND-001`, GOAL-HXS2-CODERX-001) |
| Agent | john / Esme, session `john-ws-20260826-01` |
| Target hosts | `hxs-1` (192.168.50.200), `hxs-2` (192.168.50.201), `hxs-3` (192.168.50.202), `hxs-4` (192.168.50.203) |
| Executed from | `hxs-5` (192.168.50.204) via SSH `hxsa@<host>` — askpass helper READ the credential-record "SSH password" row (`agent-zero-docs/keys.md/ssh-info.md` line 25, pipe-field 3, code-span unwrapped) AT EXECUTION TIME ONLY; no extracted copy ever existed; helper + wrappers + volatile workspace deleted at task end |
| Host-key checks | hxs-1 known_hosts-pinned (strict, M1-era pin, `StrictHostKeyChecking=yes`); hxs-2 STRICT vs rick M1 F-05 pin `SHA256:b2qlMQz496nUbuZKJu3wwmR0QY/EmN0KQtW4rM2HDcQ` ✓; hxs-3 STRICT vs rick M1 F-05 pin `SHA256:R/3mdfv7J0Fajo8yryT7JB6B4EoBm47W2rLX+siHEog` ✓; hxs-4 TOFU-with-corroboration: known_hosts ED25519 `SHA256:clnX2Pc5Mv3oylGfdoSJd9kmjHZ/HkNE/wbpz3ZNgPM` + live machine-id `a3244b92b98448ad83da8ecad6511889` == `/opt/tkv-local/servers/hxs-4/discovery.md` + eno1 MAC `bc:fc:e7:3e:10:66` == discovery ✓ |
| Window (UTC) | 2026-08-26T07:23Z → 08:15Z |
| Authorized change | Per host: remove ONLY the `Environment="OLLAMA_NO_CLOUD=1"` line from the ollama.service drop-in, `daemon-reload`, restart `ollama.service` ONLY, re-verify. Owner decision 2026-08-26 ("Enable Ollama Cloud web search", hxs-2 log row 14; hxs-3 log row 12; hxs-1 log row 78 cross-ref) |
| Explicitly NOT done | No `:cloud` models, no remote inference, no version changes (hxs-4's 0.32.15 pin belongs to session john-chatx-20260826-01), no endpoint/firewall changes, no reboots, no other service changes; `OLLAMA_AGENT_DISABLE_WEBSEARCH` never set by anyone (verified unset) |

Evidence labels: FACT (live host output) / AUTHORITY / INFERENCE / RECORD.
Sanitization confirmed: no secret value was printed, logged, or stored; the askpass value never left the SSH authentication channel; GIN lines carry no request bodies; the probe query string `hx-availability-probe` is synthetic; sign-in URLs embed each host's PUBLIC key only (public material).

---

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path /opt/tkv-local/ollama resolves locally here);
      targets hxs-1/2/3/4
Source: /opt/tkv-local/ollama + HX-ASF-Servers controlling docs
Reviewed At: 2026-08-26T07:23Z → 07:38Z
Relevant Files: 14 reviewed —
  agents/john/profile.md; agents/ roster = carol, john, kimi-k3, rick (all current)
  pilots/PILOT-HXS2-CODERX-BACKEND-001/11-work-order-john-websearch.yaml + 12-context-packet-john-websearch.yaml (contract)
  pilots/PILOT-HXS2-CODERX-BACKEND-001/01-state-log.md rows 14–15 (owner decision; commissioning)
  pilots/PILOT-HXS3-MUSE-GLIMMER-TOOLING-001/01-state-log.md rows 11–13 (M7 in flight; owner decision record)
  pilots/PILOT-HXS2-CODERX-BACKEND-001/07-esme-m4-install.md + pilots/PILOT-HXS3-MUSE-GLIMMER-TOOLING-001/07-esme-m4-install.md
    (hx2/hx3.conf, F-05 pins, digests)
  pilots/PILOT-HX1-OLLAMA-QWEN27B-001/39-esme-hxs1-exposure-change.md (hx1.conf frozen state; change pattern; guard fields)
  /opt/tkv-local/ollama/ollama-main: envconfig/config.go:237-238,330,437-457 (OLLAMA_NO_CLOUD; NoCloud() also reads
    ~/.ollama/server.json disable_ollama_cloud — checked per host: file ABSENT everywhere);
    internal/cloud/policy.go (403 DisabledError); server/cloud_proxy.go:180-215,362-370 (403 vs 401 path);
    server/routes.go:1873,1884,2138-2164 (POST /api/me; POST /api/experimental/web_search);
    server/routes.go:239-248 (signinURL = connect URL with hostname + base64url public key);
    cmd/cmd.go:138,936-965,2398-2405 (signin flow); cmd/agent_tui.go:268 (OLLAMA_AGENT_DISABLE_WEBSEARCH gate);
    auth/auth.go:53-64 (Sign fails locally when no key — key existence pre-checked per host)
  /opt/tkv-local/servers/hxs-4/discovery.md (machine-id, eno1 MAC — TOFU corroboration)
  servers/AGENTS.md (records contract); HX-ASF-Servers AGENTS.md (no-firewall rule; catalog handoff)
Authority/Version Identified: owner decision 2026-08-26 supersedes the ratified NO_CLOUD posture for the web-search class;
  Ollama 0.32.15 live on all four at execution (hxs-4 pinned 0.32.9→0.32.15 by the parallel Chat-X session at 07:38:16Z —
  packet: "work with whatever version is live"; no version touch here).
Applicable Tests/Runbooks: 39-esme change pattern (byte-copy → one-line removal → install → daemon-reload → service-only
  restart → guard compare); M4 evidence conventions.
Contradictions or Gaps:
  1. Parallel sessions in flight: john-m6-20260826-01 (hxs-2 ladder+repoint), john-m7-20260826-01 (hxs-3 ladder+repoint),
     john-chatx-20260826-01 (hxs-4 pin; COMPLETE 07:45Z, last target contact 07:44:39Z). Mitigation: per-host
     quiescence gate before mutation (no parallel POST traffic, stable ActiveEnterTimestamp + drop-in mtime, GPUs idle,
     remote sha re-verified == PRE at install moment); frozen-identity guard = pre/post WITHIN my own change window;
     resident states the ladders legitimately advanced are recorded as FACT with cause (§7).
  2. hxs-2 kernel Xid 31 pre-exists (05:46:59Z, llama-server MMU fault during an interactive client session, stack
     self-recovered; documented + escalated by john-m6 in 08-esme-m6-escalation-xid31.md). My stop condition = any NEW
     Xid in my change windows (zero occurred); the pre-existing one is reported, not concealed.
Task May Proceed: YES
```

## 2. Test definition (recorded before the first mutation, 07:38Z)

| Test | Property | Procedure (per host) | Expected | Pass rule |
| --- | --- | --- | --- | --- |
| T0 | Target identity | `hostname`, `$SSH_CONNECTION`, host-key pin/corroboration, `sudo -n true` | exact host, peer .204→.20x, pin match | all match, else halt |
| T1 | Change locus | `systemctl cat/show ollama`; grep NO_CLOUD; server.json check; `OLLAMA_AGENT_DISABLE_WEBSEARCH` in unit env | exactly one drop-in line; no second cloud-disable source; flag unset | as expected |
| T2 | Pre-state | drop-in byte-copy + sha256; `/api/ps` (hxs-1/2/3) or `ollama list` (hxs-4); NRestarts; Xid count; listener; PRE web-search probe | probe 403 "ollama cloud is disabled: web search is unavailable" | captured; 403 |
| T3 | Bounded mutation | POST authored from byte-copy removing ONLY the NO_CLOUD line; unified diff; remote sha re-verified == PRE at install moment; install 0644 root:root | diff = exactly one removed line; installed sha == POST sha | exact |
| T4 | Restart | `daemon-reload`; `systemctl restart ollama.service` ONLY | active; NRestarts accounted | rc=0, active |
| T5 | Identity guard | POST `/api/ps` vs PRE: name, digest, size_vram == size (100% VRAM), context_length; hxs-4: `qwen3.5:9b-q4_K_M` present | byte-identical on guard fields | drift → restore drop-in immediately, stop |
| T6 | Effective env | `systemctl show -p Environment` pre vs post | ONLY OLLAMA_NO_CLOUD removed | exact |
| T7 | Reachability | loopback `/api/version` all four; LAN from hxs-5 on hxs-1/2/3; hxs-4 LAN still refused | 200 loopback ×4; 200 LAN ×3; refused hxs-4 | as expected |
| T8 | Pre-signin availability | POST `/api/experimental/web_search` POST-change | 401 unauthorized-class (config gate open; activation pending owner sign-in) | 401 observed |
| T9 | Health | journal excerpt; `journalctl -p err` in window; Xid in window AND total | clean; zero NEW Xid | as expected |
| T10 | Residency return | poll `/api/ps` until resident (preload auto-rerun; hxs-4 n/a — on-demand posture) | resident ≤600 s, identity per T5 | within budget |

Stop conditions per work order: service fails to return, identity drift, any Xid → restore that host's drop-in byte-copy, daemon-reload, restart, report. One bounded correction per failed host. **No stop condition triggered on any host; zero restores; zero corrections consumed.**

## 3. Pre-change fleet state (FACT)

| Host | Version | Drop-in carrying NO_CLOUD | sha256 (PRE) | Resident / list state (PRE) | NRestarts | Xid total |
| --- | --- | --- | --- | --- | --- | --- |
| hxs-1 | 0.32.15 | `/etc/systemd/system/ollama.service.d/hx1.conf` (491 B) | `f732f9dbbbc159c4b471e34856e0b1642243badca6160e04dae6e0e1e9116144` | `hx-qwen3.8-27b-64k:latest` digest `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a`, size==size_vram 20,463,789,012 (100% VRAM), ctx 65536, Forever-sentinel | 0 | 0 |
| hxs-2 | 0.32.15 | `/etc/systemd/system/ollama.service.d/hx2.conf` (1013 B, M6-repointed 07:57:55Z) | `234da7c5c31f69b61fdf37c395fdbe513d6dec19fa647e346173fe4f7d903afa` | `hx-qwen3.6-coderx-64k:latest` digest `ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1`, size==size_vram 17,815,411,094 (100% VRAM), ctx 65536, Forever-sentinel | 0 | 1 (pre-existing, §1 gap 2) |
| hxs-3 | 0.32.15 | `/etc/systemd/system/ollama.service.d/hx3.conf` (1042 B, M7-repointed 07:50Z) | `238189e07bd19c08c03a89deef425ae774557e83c1a3d38b8e86e7c27bd63655` | `hx-muse-glimmer-64k:latest` digest `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da`, size==size_vram 18,376,336,340 (100% VRAM), ctx 65536, Forever-sentinel | 0 | 0 |
| hxs-4 | 0.32.15 | `/etc/systemd/system/ollama.service.d/hx-commissioning.conf` (605 B) | `9d90a9918701f2dd283729782bd6d4563fdcd996fcd19653653a72c5a6471bb3` | `ollama list`: `qwen3.5:9b-q4_K_M` id `6488c96fa5fa` present; `/api/ps` empty (on-demand posture) | 0 | 0 |

PRE web-search probe (all four, FACT): `POST /api/experimental/web_search {"query":"hx-availability-probe","max_results":1}` → **HTTP 403** `{"error":"ollama cloud is disabled: web search is unavailable"}` — the source-documented disabled state (`internal/cloud/policy.go` DisabledError). `~ollama/.ollama/server.json`: ABSENT on all four (no second cloud-disable source; `envconfig.NoCloud()` reads it when present). `~ollama/.ollama/id_ed25519{,.pub}`: present on all four (install-time; untouched by me — the sign-in key material already exists).

> Resident-state note (FACT/RECORD): the packet's per-host expectations for hxs-2 (`hx-qwen3.6-coderx` @ `1d297a6a093f…`, ctx 32768) and hxs-3 (`hx-muse-glimmer` @ `472ad84e752d…`, ctx 32768) were legitimately advanced by the authorized ladder sessions to the D5 `-64k` operating profiles BEFORE my changes landed (hxs-3 repoint 07:50Z; hxs-2 repoint 07:58Z). My guard compared pre/post within my own windows against the LIVE states above. The alias the packet names for hxs-1 was unchanged by any ladder (hxs-1's ladder completed earlier; `hx-qwen3.8-27b-64k` @ `766cd9469fb4…`, ctx 65536 — exact packet match).

---

## 4. hxs-1 — execution and proofs (FACT, 07:43:37Z → 07:45Z)

### 4.1 Diff (exactly one line removed)

```diff
--- hx1.conf.PRE	sha256 f732f9dbbbc159c4b471e34856e0b1642243badca6160e04dae6e0e1e9116144
+++ hx1.conf.POST	sha256 e7cd403b27dd959df7fd960dad9cbe0f8a1e43efa9a41257f591c11ee7f64ed3
@@ -6,7 +6,6 @@
 Environment="OLLAMA_CONTEXT_LENGTH=65536"
 Environment="OLLAMA_FLASH_ATTENTION=1"
 Environment="OLLAMA_KV_CACHE_TYPE=f16"
-Environment="OLLAMA_NO_CLOUD=1"
 Environment="CUDA_VISIBLE_DEVICES=GPU-2ace9bfc-3a2d-f5b9-d270-82d043f8a7b7,GPU-d675a1cd-7d3d-0903-3b1b-7d95f321a0a9"
```

Pre-change drop-in byte-copy (rollback copy, sha256 `f732f9db…e9116144`):

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_KEEP_ALIVE=-1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_CONTEXT_LENGTH=65536"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_KV_CACHE_TYPE=f16"
Environment="OLLAMA_NO_CLOUD=1"
Environment="CUDA_VISIBLE_DEVICES=GPU-2ace9bfc-3a2d-f5b9-d270-82d043f8a7b7,GPU-d675a1cd-7d3d-0903-3b1b-7d95f321a0a9"
Restart=always
RestartSec=3
TimeoutStartSec=300
LimitNOFILE=65535
```

### 4.2 Mutation + restart proof

- Remote sha re-verified == PRE immediately before install (no parallel writer).
- 07:43:37Z install → installed sha256 `e7cd403b27dd959df7fd960dad9cbe0f8a1e43efa9a41257f591c11ee7f64ed3` (459 B, 0644 root:root) == authored POST ✓; `daemon-reload` OK; `systemctl restart ollama.service` rc=0 at 07:43:38Z — ONLY ollama.service. No reboot; no other unit touched.
- Effective Environment POST: `… OLLAMA_HOST=0.0.0.0 OLLAMA_KEEP_ALIVE=-1 OLLAMA_MAX_LOADED_MODELS=1 OLLAMA_NUM_PARALLEL=1 OLLAMA_CONTEXT_LENGTH=65536 OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=f16 CUDA_VISIBLE_DEVICES=…` — ONLY `OLLAMA_NO_CLOUD` removed ✓. `NRestarts=0` pre and post.

### 4.3 Identity/residency guard (T5/T10) — PASS

Preload auto-ran via `Requires=` propagation: `hx-ollama-preload: OK - hx-qwen3.8-27b-64k resident` 07:44:26Z (Result=success, ExecMainStatus=0); `/api/ps` resident ~30 s after restart (budget 600 s).

| Field | PRE (07:40:33Z) | POST (07:44:4xZ) | Verdict |
| --- | --- | --- | --- |
| name | `hx-qwen3.8-27b-64k:latest` | identical | MATCH |
| digest | `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a` | identical | MATCH |
| size / size_vram | 20,463,789,012 / 20,463,789,012 (100% VRAM) | identical | MATCH |
| context_length | 65536 | 65536 | MATCH |
| details | qwen35 / 27.3B / Q4_K_M | identical | MATCH |
| `ollama ps` | 100% GPU, 65536, Forever | `766cd9469fb4`, 20 GB, 100% GPU, 65536, Forever | MATCH |

`expires_at` sentinel moved (2318-12-06T06:59:42Z → 2318-12-06T07:31:43Z): keep_alive=-1 sentinel recomputed at runner start; not a guard field (39-esme precedent). **IDENTITY GUARD: PASS — no drift; no restore triggered.**

### 4.4 Reachability, availability, health (T7/T8/T9)

- Loopback `/api/version` → `{"version":"0.32.15"}` ✓. LAN from hxs-5: `curl http://192.168.50.200:11434/api/version` → `{"version":"0.32.15"}` ✓.
- POST-change web-search probe → **HTTP 401** `{"error":"Unauthorized"}` (config gate open; activation pending owner sign-in — §8).
- Journal window: clean stop 07:43:37 → start 07:43:38; startup line `msg="Ollama cloud disabled: false"` (FACT — the server's own posture log); `Listening on [::]:11434 (version 0.32.15)`; both RTX 4070 Ti SUPER discovered (driver 13.0); runner start 07:44:19 → `model loaded` → preload generate OK. One WARN pair `llama-server GPU discovery watchdog timed out` + `unable to refresh free memory` — carried-class F-J1 (noted in M4/39-esme evidence), not a regression. `journalctl -p err` in window: **no entries**. Xid in window: **0**; total this boot: **0**.

## 5. hxs-2 — execution and proofs (FACT, 08:09:28Z → 08:12Z)

Sequencing note (RECORD): the parallel john-m6 session (resumed after its Xid-31 escalation, per governor direction) was mid-ladder until ~08:02Z; I executed in its quiescent end-state window (ActiveEnterTimestamp stable 07:58:24Z for 11 min, zero POSTs/180 s, GPUs 0%, drop-in mtime stable). M6's ladder deliverable remains its own session's to file.

### 5.1 Diff (exactly one line removed)

```diff
--- hx2.conf.PRE	sha256 234da7c5c31f69b61fdf37c395fdbe513d6dec19fa647e346173fe4f7d903afa
+++ hx2.conf.POST	sha256 36083e96d241906f5ef4d5f7421b5592d112cb068be2f216feb9c14e9aa4b13c
@@ -11,7 +11,6 @@
 # (draft_num_predict 3, native sampling) govern.
 [Service]
 Environment="OLLAMA_HOST=0.0.0.0"
-Environment="OLLAMA_NO_CLOUD=1"
 Environment="OLLAMA_CONTEXT_LENGTH=65536"
 Environment="OLLAMA_NUM_PARALLEL=1"
 Environment="OLLAMA_MAX_LOADED_MODELS=1"
```

Pre-change drop-in byte-copy (rollback copy, sha256 `234da7c5…f7d903afa`):

```ini
# hxs-2 CoderX service plane — WO-HXS2-JOHN-M4-001 (blueprint §3/§5; owner D2).
# OLLAMA_HOST=0.0.0.0 binds the wildcard address (default port 11434 per
# envconfig Host()); loopback is preserved — the preload script and fixtures
# use 127.0.0.1. The private 192.168.50.0/24 LAN itself is the boundary:
# no host firewall anywhere (owner rule 2026-08-26). Admission control:
# exactly one loaded model, one parallel request. Cloud features disabled.
# M6 (WO-HXS2-JOHN-M6-001): OLLAMA_CONTEXT_LENGTH=65536 is operator-consistency
# with the hx-qwen3.6-coderx-64k operating profile (D5) — the alias Modelfile
# PARAMETER num_ctx remains the effective contract (/api/ps context_length is
# the proof). No sampling variables are set here; the baked tag parameters
# (draft_num_predict 3, native sampling) govern.
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_NO_CLOUD=1"
Environment="OLLAMA_CONTEXT_LENGTH=65536"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
```

### 5.2 Mutation + restart proof

- 08:09:28Z install → installed sha256 `36083e96d241906f5ef4d5f7421b5592d112cb068be2f216feb9c14e9aa4b13c` (981 B, 0644 root:root) == authored POST ✓; `daemon-reload` OK; `systemctl restart ollama.service` rc=0 at 08:09:30Z — ONLY ollama.service.
- Effective Environment POST: `… OLLAMA_HOST=0.0.0.0 OLLAMA_CONTEXT_LENGTH=65536 OLLAMA_NUM_PARALLEL=1 OLLAMA_MAX_LOADED_MODELS=1` — ONLY `OLLAMA_NO_CLOUD` removed ✓. `NRestarts=0` pre and post.

### 5.3 Identity/residency guard (T5/T10) — PASS, with one explained runtime-field variance

Preload auto-ran: `hx-ollama-preload: OK - hx-qwen3.6-coderx-64k resident (digest ec9ebe08a824…)` 08:10:32Z; `/api/ps` resident ~50 s after restart.

| Field | PRE (08:08:41Z) | POST (08:10:2xZ) | Verdict |
| --- | --- | --- | --- |
| name | `hx-qwen3.6-coderx-64k:latest` | identical | MATCH |
| digest | `ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1` | identical | MATCH |
| size_vram == size (100% VRAM) | 17,815,411,094 == 17,815,411,094 | 19,994,918,253 == 19,994,918,253 | 100% VRAM both; absolute differs — explained below |
| context_length | 65536 | 65536 | MATCH |
| details | qwen35moe / 26.2B / Q4_K_M | identical | MATCH |
| `ollama ps` | 100% GPU, 65536, Forever | `ec9ebe08a824`, 19 GB, 100% GPU, 65536, Forever | MATCH |

**Size variance — investigated to ground truth (journal FACTs, not conjecture):** the PRE resident runner was started by the parallel M6 session's final verification load at 08:01:36Z with `-b 512 -ub 512` (and pinned Forever by its ~08:02:5Z pin request); my POST runner was started at 08:10:22Z by the host's frozen preload script with `-b 2048 -ub 2048`. Same model blob `sha256-ce2f69655c…`, same mmproj, same `-c 65536`, same spec/flash-attn flags — only the batch/ubatch differs, which sizes the compute buffer (Δ = +2,179,507,159 B for 4× batch tokens on this hybrid MoE). The POST state is exactly what this host produces at every boot/service start via its hash-witnessed preload path; the NO_CLOUD removal has no mechanism to influence runner sizing. Identity fields (name, digest, blob, ctx, 100%-VRAM residency, Forever) are byte-identical. **IDENTITY GUARD: PASS on the packet's guard fields — no restore triggered.**

### 5.4 Reachability, availability, health (T7/T8/T9)

- Loopback → `{"version":"0.32.15"}` ✓. LAN from hxs-5: `curl http://192.168.50.201:11434/api/version` → `{"version":"0.32.15"}` ✓.
- POST-change web-search probe → **HTTP 401** `{"error":"Unauthorized"}` ✓.
- Journal window: `Ollama cloud disabled: false`; `Listening on [::]:11434`; both RTX 5060 Ti discovered; watchdog WARN pair (carried-class F-J1); `model loaded` 08:10:32. `journalctl -p err` in window: **no entries**. Xid in window: **0**; total this boot: **1** — the pre-existing 05:46:59Z Xid 31 (john-m6's escalation doc; zero NEW Xid).

## 6. hxs-3 — execution and proofs (FACT, 07:59:23Z → 08:01Z)

Sequencing note (RECORD): executed after the parallel john-m7 session reached its quiescent end state (preload repoint landed 07:50Z; zero POST traffic, GPUs 0%, ActiveEnterTimestamp stable across two windows).

### 6.1 Diff (exactly one line removed)

```diff
--- hx3.conf.PRE	sha256 238189e07bd19c08c03a89deef425ae774557e83c1a3d38b8e86e7c27bd63655
+++ hx3.conf.POST	sha256 07824e4e6794b1a4dc9af3dead4e4968d4bb63b629200f736a5e9313e9c3e7d5
@@ -12,7 +12,6 @@
 # (temperature 1, top_k 64, top_p 0.95) govern.
 [Service]
 Environment="OLLAMA_HOST=0.0.0.0"
-Environment="OLLAMA_NO_CLOUD=1"
 Environment="OLLAMA_NUM_PARALLEL=1"
 Environment="OLLAMA_MAX_LOADED_MODELS=1"
 Environment="OLLAMA_CONTEXT_LENGTH=65536"
```

Pre-change drop-in byte-copy (rollback copy, sha256 `238189e0…7bd63655`):

```ini
# hxs-3 Muse Glimmer service plane — WO-HXS3-JOHN-M4-001, repointed by
# WO-HXS3-JOHN-M7-001 (D5 operating profile hx-muse-glimmer-64k).
# OLLAMA_HOST=0.0.0.0 binds the wildcard address (default port 11434 per
# envconfig Host()); loopback is preserved — the preload script and fixtures
# use 127.0.0.1. The private 192.168.50.0/24 LAN itself is the boundary:
# no host firewall anywhere (owner rule 2026-08-26). Admission control:
# exactly one loaded model, one parallel request. Cloud features disabled.
# OLLAMA_CONTEXT_LENGTH=65536 is operator-consistency with the D5 operating
# profile only — each alias Modelfile's PARAMETER num_ctx remains the
# effective per-model contract (hxs-1 pattern). Native-sampling baseline:
# NO sampling variables are set here — the baked tag parameters
# (temperature 1, top_k 64, top_p 0.95) govern.
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_NO_CLOUD=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_CONTEXT_LENGTH=65536"
```

### 6.2 Mutation + restart proof

- 07:59:23Z install → installed sha256 `07824e4e6794b1a4dc9af3dead4e4968d4bb63b629200f736a5e9313e9c3e7d5` (1010 B, 0644 root:root) == authored POST ✓; `daemon-reload` OK; `systemctl restart ollama.service` rc=0 at 07:59:26Z — ONLY ollama.service.
- Effective Environment POST: `… OLLAMA_HOST=0.0.0.0 OLLAMA_NUM_PARALLEL=1 OLLAMA_MAX_LOADED_MODELS=1 OLLAMA_CONTEXT_LENGTH=65536` — ONLY `OLLAMA_NO_CLOUD` removed ✓. `NRestarts=0` pre and post.

### 6.3 Identity/residency guard (T5/T10) — PASS

Preload auto-ran: `hx-ollama-preload: OK - hx-muse-glimmer-64k resident (digest 9dffb015db40…)` 08:00:26Z; `/api/ps` resident ~40 s after restart.

| Field | PRE (07:58Z) | POST (08:00Z) | Verdict |
| --- | --- | --- | --- |
| name | `hx-muse-glimmer-64k:latest` | identical | MATCH |
| digest | `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da` | identical | MATCH |
| size / size_vram | 18,376,336,340 / 18,376,336,340 (100% VRAM) | identical | MATCH |
| context_length | 65536 | 65536 | MATCH |
| details | muse-glimmer / 27.9B / Q4_K_M | identical | MATCH |
| `ollama ps` | 100% GPU, 65536, Forever | `9dffb015db40`, 18 GB, 100% GPU, 65536, Forever | MATCH |

**IDENTITY GUARD: PASS — no drift; no restore triggered.**

### 6.4 Reachability, availability, health (T7/T8/T9)

- Loopback → `{"version":"0.32.15"}` ✓. LAN from hxs-5: `curl http://192.168.50.202:11434/api/version` → `{"version":"0.32.15"}` ✓.
- POST-change web-search probe → **HTTP 401** `{"error":"Unauthorized"}` ✓.
- Journal window: `Ollama cloud disabled: false`; `Listening on [::]:11434`; both RTX 5060 Ti discovered; watchdog WARN pair (carried-class F-J1); `srv llama_server: model loaded` 08:00:25. `journalctl -p err` in window: **no entries**. Xid in window: **0**; total this boot: **0**.

## 7. hxs-4 — execution and proofs (FACT, 07:47:09Z → 07:48Z)

Sequencing note (RECORD): the parallel john-chatx session's last target contact was 07:44:39Z (its pin 0.32.9→0.32.15 landed 07:38:16Z; its deliverable `10-esme-chatx-ladder-profiles.md` records the drop-in `9d90a991…1bb3` byte-identical == my PRE). My change ran 07:47:09Z in a verified-quiet window.

### 7.1 Diff (exactly one line removed)

```diff
--- hx-commissioning.conf.PRE	sha256 9d90a9918701f2dd283729782bd6d4563fdcd996fcd19653653a72c5a6471bb3
+++ hx-commissioning.conf.POST	sha256 f78de2292a96154c3ebe9eeff5d4172cf399989d350d1c987627604fe9345e41
@@ -9,4 +9,3 @@
 Environment="OLLAMA_CONTEXT_LENGTH=65536"
 Environment="OLLAMA_NUM_PARALLEL=1"
 Environment="OLLAMA_MAX_LOADED_MODELS=1"
-Environment="OLLAMA_NO_CLOUD=1"
```

Pre-change drop-in byte-copy (rollback copy, sha256 `9d90a991…471bb3`):

```ini
# HX commissioning override - conservative, loopback only.
# GPU isolation is MANDATORY. hxs-4 has an asymmetric pair (16 GB + 8 GB).
# CUDA_VISIBLE_DEVICES alone is NOT sufficient: the Vulkan backend enumerates
# devices independently and re-exposed the excluded 16 GB card. Vulkan is disabled.
[Service]
Environment="CUDA_VISIBLE_DEVICES=GPU-cc758e31-d23b-3c53-bee6-dae3299a6f11"
Environment="GGML_VK_VISIBLE_DEVICES=999"
Environment="OLLAMA_VULKAN=0"
Environment="OLLAMA_CONTEXT_LENGTH=65536"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NO_CLOUD=1"
```

### 7.2 Mutation + restart proof

- 07:47:09Z install → installed sha256 `f78de2292a96154c3ebe9eeff5d4172cf399989d350d1c987627604fe9345e41` (573 B, 0644 root:root) == authored POST ✓; `daemon-reload` OK; `systemctl restart ollama.service` rc=0 — ONLY ollama.service.
- Effective Environment POST: `… CUDA_VISIBLE_DEVICES=GPU-cc758e31-… GGML_VK_VISIBLE_DEVICES=999 OLLAMA_VULKAN=0 OLLAMA_CONTEXT_LENGTH=65536 OLLAMA_NUM_PARALLEL=1 OLLAMA_MAX_LOADED_MODELS=1` — ONLY `OLLAMA_NO_CLOUD` removed ✓. `NRestarts=0` pre and post. Version untouched by me: 0.32.15 (parallel session's pin, per packet).

### 7.3 Identity guard (T5) — PASS (list-intact contract)

| Field | PRE (07:40Z) | POST (07:47Z) | Verdict |
| --- | --- | --- | --- |
| `ollama list` | `qwen3.5:9b-q4_K_M` id `6488c96fa5fa`, 6.6 GB | identical | MATCH |
| `/api/ps` | empty (on-demand posture) | empty | MATCH |
| listener | `127.0.0.1:11434` only | `127.0.0.1:11434` only | MATCH |

**IDENTITY GUARD: PASS — model list intact; loopback-only posture unchanged.**

### 7.4 Reachability, availability, health (T7/T8/T9)

- Loopback → `{"version":"0.32.15"}` ✓. LAN from hxs-5: `curl http://192.168.50.203:11434/api/version` → **connection refused (0 ms)** ✓ — parked LAN posture unchanged.
- POST-change web-search probe → **HTTP 401** `{"error":"Unauthorized"}` ✓.
- Journal window: `Ollama cloud disabled: false`; `Listening on 127.0.0.1:11434`. Kernel err-level lines in window: 3× ACPI `AE_ALREADY_EXISTS` (`\_SB.PC00.PEG1.PEGP._DSM`) — platform firmware chatter tied to ANY GPU re-probe on this board: 21 identical lines in the parallel session's 07:38:16Z restart window (pre-change) and at Aug 25 16:23 driver-load era; precedent-proven benign, not a regression of this change. Xid in window: **0**; total this boot: **0**.

## 8. Pre-signin web-search availability state (FACT, per host) + the owner's remaining step

Mechanism (source-grounded): the local route `POST /api/experimental/web_search` proxies to Ollama Cloud. With `OLLAMA_NO_CLOUD=1` it is refused locally with 403 `ollama cloud is disabled: web search is unavailable` (`internal/cloud/policy.go`). With the flag removed, the request is signed with the host's ed25519 key (`~ollama/.ollama/id_ed25519`, present on all four since install) and proxied; an unregistered key gets **401** from the cloud. After the owner links each host's key to his ollama.com account (the `ollama signin` URL flow), the same route returns results. Remote inference and `:cloud` models remain unused by policy; the agent-TUI web-search tools are allowed because `OLLAMA_AGENT_DISABLE_WEBSEARCH` is UNSET everywhere (verified in unit files and effective environments on all four; never set by me).

| Host | PRE probe | POST probe | State |
| --- | --- | --- | --- |
| hxs-1 | 403 `ollama cloud is disabled: web search is unavailable` | **401 `{"error":"Unauthorized"}`** | Config gate OPEN; activation pending owner sign-in |
| hxs-2 | 403 (same) | **401 `{"error":"Unauthorized"}`** | Config gate OPEN; activation pending owner sign-in |
| hxs-3 | 403 (same) | **401 `{"error":"Unauthorized"}`** | Config gate OPEN; activation pending owner sign-in |
| hxs-4 | 403 (same) | **401 `{"error":"Unauthorized"}`** | Config gate OPEN; activation pending owner sign-in |

Each host also logged `msg="Ollama cloud disabled: false"` at its post-change service start (the server's own posture line, FACT).

### Owner instruction — one interactive step per host

Run once on EACH host (hxs-1, hxs-2, hxs-3, hxs-4), as any local user (e.g. `hxsa`; the server does the signing, no sudo needed):

```bash
ssh hxsa@<host>        # or on the host console
ollama signin
```

- The command prints `You need to be signed in to Ollama to run Cloud models.` and a per-host URL (`ollama signin` does not mutate anything before you act in the browser; on a headless host the browser-open attempt silently no-ops and the URL prints).
- Open the printed URL in any browser, sign in with YOUR ollama.com account, and approve/connect that host's key.
- Verify: re-run `ollama signin` → expect `You are already signed in as user '<your-account>'`. Web search is then active on that host (`POST /api/experimental/web_search` returns results instead of 401).
- Per-host URLs captured 2026-08-26T08:0x–08:12Z (they are stable per host key; re-running `ollama signin` prints the same one):

```text
hxs-1: https://ollama.com/connect?name=hxs-1&key=c3NoLWVkMjU1MTkgQUFBQUMzTnphQzFsWkRJMU5URTVBQUFBSU52Mld3dTVOem44MlZMK0lkRS9iSjI2VmR0QUVRMWdlRnhQL3ZRMTUxRFE
hxs-2: https://ollama.com/connect?name=hxs-2&key=c3NoLWVkMjU1MTkgQUFBQUMzTnphQzFsWkRJMU5URTVBQUFBSUZVbjdCVnZIeGVPOUdsdzdxQVgzZDBneFFoZCs1OEtBa3BSZTM2VzYrQ1U
hxs-3: https://ollama.com/connect?name=hxs-3&key=c3NoLWVkMjU1MTkgQUFBQUMzTnphQzFsWkRJMU5URTVBQUFBSVBwajZUL2lmTkloRFVjeTVpRTFwQmlyRktDYWJFMHJVbVJXWE1rdDF0c0k
hxs-4: https://ollama.com/connect?name=hxs-4&key=c3NoLWVkMjU1MTkgQUFBQUMzTnphQzFsWkRJMU5URTVBQUFBSUl5dndYbitaaGN0MUh2OVhIQW9uTS9wUDRLT0gyOUdJcGpBVmdVbEorMnY
```

Each host must be signed in INDIVIDUALLY (per-host keys). Sign-out path if ever needed: `ollama signout` on that host.

## 9. Fleet-final state (FACT, 08:13–08:15Z re-sweep)

| Host | Drop-in sha256 (POST, still in force) | NO_CLOUD in effective env | Service | NRestarts | Resident / list |
| --- | --- | --- | --- | --- | --- |
| hxs-1 | `e7cd403b27dd959df7fd960dad9cbe0f8a1e43efa9a41257f591c11ee7f64ed3` | 0 | active | 0 | `hx-qwen3.8-27b-64k` `766cd9469fb4` 100% GPU 65536 Forever |
| hxs-2 | `36083e96d241906f5ef4d5f7421b5592d112cb068be2f216feb9c14e9aa4b13c` | 0 | active | 0 | `hx-qwen3.6-coderx-64k` `ec9ebe08a824` 100% GPU 65536 Forever |
| hxs-3 | `07824e4e6794b1a4dc9af3dead4e4968d4bb63b629200f736a5e9313e9c3e7d5` | 0 | active | 0 | `hx-muse-glimmer-64k` `9dffb015db40` 100% GPU 65536 Forever |
| hxs-4 | `f78de2292a96154c3ebe9eeff5d4172cf399989d350d1c987627604fe9345e41` | 0 | active | 0 | `qwen3.5:9b-q4_K_M` `6488c96fa5fa` in list; ps empty |

## 10. Rollback inverse (per host; est. < 90 s each, no reboot)

Restores the NO_CLOUD posture exactly (byte-copies embedded above: §4.1 hxs-1, §5.1 hxs-2, §6.1 hxs-3, §7.1 hxs-4):

```bash
# per host, from hxs-5 (ssh hxsa@<host>), using the embedded PRE byte-copy:
sudo install -m 0644 -o root -g root <host>.conf.PRE /etc/systemd/system/ollama.service.d/<host>.conf
#   hxs-1 target: hx1.conf   hxs-2: hx2.conf   hxs-3: hx3.conf   hxs-4: hx-commissioning.conf
sudo systemctl daemon-reload
sudo systemctl restart ollama.service
# verify: sha256 == PRE hash (§3); systemctl show -p Environment carries OLLAMA_NO_CLOUD=1;
#         web-search probe returns 403; /api/ps (or list) matches §3; preload re-pins resident model.
```

Rollback does not un-register keys (nothing was registered — sign-in is the owner's pending step; if he has since signed in, `ollama signout` per host precedes posture restoration).

## 11. Sequential command log (profile §11.3; sanitized)

All remote commands as `hxsa@<host>` from `hxs-5` over independent SSH sessions (askpass read the credential-record row at execution time; `StrictHostKeyChecking=yes`; `NumberOfPasswordPrompts=1`; password auth only); privileged steps via `sudo -n` (NOPASSWD). "local" = hxs-5. Times UTC, approximate.

| Seq | Time | Where | Command (shape) | Exit | Evidence |
| ---: | --- | --- | --- | ---: | --- |
| 1 | 07:23–07:33 | local | read profile, WO/CP, AGENTS.md files, state logs, prior esme evidence; TKV survey (NO_CLOUD/web-search/signin source path) | 0 | §1 |
| 2 | 07:33–07:36 | local | host-key verification: `ssh-keygen -F` all four IPs; hxs-2/3 == F-05 pins; hxs-4 corroboration material from discovery.md | 0 | header |
| 3 | 07:36 | local | credential-file shape probes (line numbers, field counts, whitelisted labels only — values never printed) | 0 | §11 note |
| 4 | 07:39 | local | `mktemp -d` workspace (0700); askpass + essh wrappers (0700); `sh -n`/`bash -n`; shape test (byte count 9 only) | 0 | §11 note |
| 5 | 07:39 | ssh ×4 | identity: `hostname`, `$SSH_CONNECTION`, `sudo -n true`, date; hxs-4 + machine-id + eno1 MAC | 0 | header |
| 6 | 07:40 | ssh ×4 | pre-flight captures: version, systemctl cat/show, drop-in sha+stat, `/api/ps`/`ollama list`, listener, key/server.json existence, journal tails, Xid counts | 0 | §3 |
| 7 | 07:42 | ssh hxs-2 | Xid investigation: full Xid line + NVRM context (pre-existing 05:46:59Z Xid 31 identified) | 0 | §1 gap 2 |
| 8 | 07:42–43 | ssh hxs-1 | byte-copy hx1.conf (sha == frozen); PRE probe 403 | 0 | §4.1 |
| 9 | 07:43 | local | author hx1.conf.POST; one-line diff; hashes; remote re-verify | 0 | §4.1 |
| 10 | 07:43:37–38 | ssh hxs-1 | install POST (0644 root:root); sha == POST; daemon-reload; restart ollama.service ONLY; active; NRestarts=0 | 0 | §4.2 |
| 11 | 07:44 | ssh hxs-1 | poll `/api/ps` → resident ~30 s (digest 766cd9469fb4…); preload Result=success | 0 | §4.3 |
| 12 | 07:45 | ssh hxs-1 + local | POST checks: ps/list, probe 401, AGENT flag absent, journal/err/Xid/NRestarts; LAN curl from hxs-5 → 200 | 0 | §4.4 |
| 13 | 07:46–47 | ssh hxs-4 | byte-copy hx-commissioning.conf; PRE probe 403; POST author + diff; quiet re-verify; install 07:47:09Z; reload+restart; active; NRestarts=0 | 0 | §7 |
| 14 | 07:47–48 | ssh hxs-4 + local | POST checks: list intact, loopback 200, LAN refused, probe 401, journal/ACPI precedent check, Xid 0 | 0 | §7.4 |
| 15 | 07:48–08:08 | local/ssh | hxs-2/3 quiescence polls (POST counts, ActiveEnter, GPU util, drop-in mtimes); parallel-session docs read (08-esme-m6-escalation-xid31.md, 10-esme-chatx-ladder-profiles.md) | 0 | §5/§6 seq notes |
| 16 | 07:58–08:01 | ssh hxs-3 | byte-copy hx3.conf (post-M7-repoint); PRE ps/probe/counters; POST author + diff; quiet re-verify; install 07:59:23Z; reload+restart; poll resident ~40 s | 0 | §6 |
| 17 | 08:01 | ssh hxs-3 + local | POST checks: ps guard MATCH, probe 401, LAN 200, journal/err/Xid/NRestarts | 0 | §6.4 |
| 18 | 08:08–08:10 | ssh hxs-2 | byte-copy hx2.conf (post-M6-repoint); PRE ps/probe/counters; POST author + diff; quiet re-verify; install 08:09:28Z; reload+restart; poll resident ~50 s | 0 | §5 |
| 19 | 08:10–08:11 | ssh hxs-2 | size-variance investigation: runner-flag comparison PRE (-b 512, M6 verification load) vs POST (-b 2048, preload script) from journal — explained | 0 | §5.3 |
| 20 | 08:11–08:12 | ssh hxs-2 + local | POST checks: guard fields MATCH, probe 401, LAN 200, journal/err/Xid(0 new)/NRestarts | 0 | §5.4 |
| 21 | 08:0x–08:12 | ssh ×4 | `ollama signin` (read-only URL capture per host; no authentication performed) | 0 | §8 |
| 22 | 08:13–08:15 | ssh ×4 | fleet-final re-sweep: drop-in shas == POST, 0 NO_CLOUD tokens, active, NRestarts=0, ps/list final | 0 | §9 |
| 23 | 08:15+ | local | deliverable written; **workspace + askpass helper + wrappers deleted** (no extracted credential copy ever existed) | — | §11 note |

Sanitization confirmed: no secret value was printed, logged, stored, or placed on any command line at any step. The two background-poll wrapper invocations that timed out (local scaffolding only) touched no target state.

## 12. Validation summary (profile §11.4)

- **What changed:** exactly one line — `Environment="OLLAMA_NO_CLOUD=1"` — removed from the ollama.service drop-in on each of hxs-1 (`hx1.conf`), hxs-2 (`hx2.conf`), hxs-3 (`hx3.conf`), hxs-4 (`hx-commissioning.conf`); `daemon-reload` + `ollama.service`-only restart per host. Pre/post sha256 + unified diffs: §4.1, §5.1, §6.1, §7.1.
- **What did not change:** versions (0.32.15 everywhere; hxs-4's pin is the Chat-X session's), endpoints/binds (hxs-1/2/3 `*:11434`, hxs-4 `127.0.0.1:11434`), firewall (none anywhere — owner rule), model stores, all other env values, all other units, no reboots, no `:cloud` models, no remote inference. `OLLAMA_AGENT_DISABLE_WEBSEARCH`: unset everywhere (verified), never set.
- **Tested:** T0–T10 per host (§2) — identity/SSH, locus, pre-state, bounded mutation, restart, identity guard, effective env, reachability, pre-signin availability, health, residency return.
- **Passed:** all, all four hosts. Identity guards: hxs-1 PASS (byte-identical incl. size); hxs-2 PASS on guard fields with the size variance proven to runner batch flags (§5.3); hxs-3 PASS (byte-identical); hxs-4 PASS (list intact).
- **Running version / models:** 0.32.15 all four; hxs-1 `hx-qwen3.8-27b-64k` @ `766cd9469fb4…` 100% VRAM ctx 65536 Forever; hxs-2 `hx-qwen3.6-coderx-64k` @ `ec9ebe08a824…` 100% VRAM ctx 65536 Forever; hxs-3 `hx-muse-glimmer-64k` @ `9dffb015db40…` 100% VRAM ctx 65536 Forever; hxs-4 `qwen3.5:9b-q4_K_M` present, on-demand.
- **Endpoint/security state:** loopback 200 ×4; LAN 200 from hxs-5 on hxs-1/2/3; hxs-4 LAN refused (posture parked); no cloud disable anywhere; sign-in NOT yet performed (owner step, §8).
- **Resource/health state:** journals clean (only carried-class watchdog WARNs + hxs-4 ACPI chatter, both precedent-proven); zero NEW Xid (hxs-2's pre-existing Xid 31 documented by john-m6); NRestarts=0 ×4.
- **Rollback readiness:** byte-copies embedded; inverse in §10; no rollback needed or triggered.
- **Remaining risks/decisions:** (1) owner sign-in ×4 is the remaining activation gate (§8); (2) hxs-2's pre-existing Xid 31 awaits the governor's disposition of john-m6's escalation (driver/ggml defect triage) — outside this work order; (3) parallel sessions' deliverables (M6 hxs-2 ladder, M7 hxs-3 ladder) are their own sessions' to file — my evidence uses their quiescent windows and cites their authorized edits.

## 13. Second Brain evaluation (standing directive)

1. Opportunity identified: **yes** — a uniform bounded fleet change (four hosts, one shape) with per-host identity guards: the SC-07a pattern generalized to a fleet class.
2. Roadmap capability/pattern: posture changes land in the same versioned/evidenced path as installs — the NO_CLOUD supersession is recorded owner-decision-first (log rows), config-second (this document), catalog-third (Carol's receipt).
3. Disposition: **implemented** — the change itself carries per-host provenance (pre/post hashes + diffs + guard matrices); the pre-signin availability state and the exact owner instruction are first-class deliverable content for the catalog.
4. Evidence/reasoning: the catalog should note the new capability class "fleet posture change (bounded, guarded)" and the pending owner gate (sign-in ×4) so downstream consumers do not mistake "config gate open" for "web search active".

## 14. Handoff

Deliverable `13-esme-websearch-enable.md` goes to Carol for catalog receipt; handoff OPEN until the receipt is cited in the governing logs (hxs-2 state log per row 15 commissioning record).

```text
[KNOWLEDGE REVIEW COMPLETE] — §1 (Task May Proceed: YES)
```

```text
[TASK COMPLETE — EVIDENCE ATTACHED]
Task May Proceed: YES
```

`PASS — TASK COMPLETE`

Signed: **john / Esme** — Expert Ollama Engineer, session `john-ws-20260826-01`, 2026-08-26T08:16Z (UTC).
