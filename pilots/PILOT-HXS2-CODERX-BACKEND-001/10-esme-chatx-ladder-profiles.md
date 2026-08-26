# 10 — Esme (john): Chat-X Pin 0.32.9 → 0.32.15 + GPU-Isolation Relaxation (O2) + Three-Rung Ladder + Profile Freeze

| Field | Value |
| --- | --- |
| Report ID | ESME-CHATX-LADDER-001 (rev 2 — resumed under owner decision O2) |
| Task ID | WO-HXS4-JOHN-L1-001 (`PILOT-HXS2-CODERX-BACKEND-001`, Chat-X bounded alignment + ladder + three profiles) |
| Agent | john / Esme (profile `agents/john/profile.md`), session `john-chatx-20260826-01` (two windows: 07:16–07:45Z pin+blocker; 09:15–09:41Z O2 resume) |
| Target host | `hxs-4` (192.168.50.203), Ubuntu 24.04.4 LTS, RTX 5060 Ti 16,311 MiB + RTX 5060 8,151 MiB, driver 580.173.02 |
| Executed from | `hxs-5` (192.168.50.204) via SSH `hxsa@192.168.50.203` — askpass helper READ the fleet credential-record row (`ssh-info.md` "SSH password" row) AT EXECUTION TIME ONLY in both windows; no extracted copy ever existed; value never printed/logged/stored; helper deleted at task end |
| Host-key check | STRICT — `StrictHostKeyChecking=yes` against the existing known_hosts entry; `NumberOfPasswordPrompts=1` |
| Ollama | **0.32.15** (binary == server; pinned from 0.32.9 in window 1 — §2) |
| Isolation | **RELAXED per owner decision O2 (2026-08-26)**: Ollama-usable VRAM **7.5 GiB → 23.0 GiB** (both GPUs) — §4R |
| Ladder | **COMPLETE** — 32k/64k/128k rungs on the exact digest, 100% VRAM each, KV f16 exactly linear **32,768 B/token**, needles + spot checks per §5R (one recorded attenuation: 32k needle at ~95%) |
| Aliases | **FROZEN** — `hx-qwen3.5-9b-32k`/`-64k`/`-128k`, digest-equality proven ×3; **default usage reference = `hx-qwen3.5-9b-64k`** — §6R |
| Status | **`PASS — TASK COMPLETE`** (with recorded rung attenuation A-1, §5R.3 — disclosed, not concealed) |

Evidence labels: **FACT** (live host output) / **AUTHORITY** (owner decision, work order, governance) / **INFERENCE** / **RECORD**.
All secrets excluded; the SSH credential was never printed, logged, or stored. Thinking content never persisted (counts only).

---

# PART 1 — Window 1 (07:16–07:45Z): pin + blocker (history, superseded by Part 2 resolution)

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path /opt/tkv-local/ollama resolves locally here); target hxs-4 (192.168.50.203)
Source: /opt/tkv-local/ollama + HX-ASF-Servers controlling docs
Reviewed At: 2026-08-26T07:16Z → 07:26Z (window 1); re-confirmed 09:15Z (window 2: state-log rows 17-21 absorbed — Coder-X M6 complete, web-search enablement, O2 commissioning)
Relevant Files: 14 —
  agents/john/profile.md; roster = carol, john, kimi-k3, rick (all current teammates)
  09-work-order-john-chatx.yaml + 10-context-packet-john-chatx.yaml (the contract)
  pilots/PILOT-HXS2-CODERX-BACKEND-001/01-state-log.md rows 13, 17-21 (owner order; Coder-X M6; web-search fleet change; Chat-X blocker + O2 resumption)
  pilots/PILOT-HX1-OLLAMA-QWEN27B-001/09-state-log.md rows 76-78 (Chat-X facts; gemma4 closure; web-search owner decision)
  hxs-1 pattern: 22-esme-m6-capacity-ladder.md, 29-esme-m6b-profiles.md
  pin method: hxs-2 + hxs-3 07-esme-m4-install.md (identical OLLAMA_VERSION pin method)
  sibling contract + result: 07/08-work-order+context-packet-john-m6.yaml; state log row 18 (Coder-X ladder PASS, KV 20,480 B/token, F-M6-7 size-variance class)
  fixtures/: sha256sum -c sha256sums.txt → all 10 OK (needle_probe.py + fixtures_corpus.py used)
  /opt/tkv-local/ollama/ollama-main/scripts/install.sh (reviewed baseline)
  ollama-main/types/model/name.go + server/create.go + server/model.go + manifest/manifest.go (FROM/digest resolution)
  servers/BLUEPRINT-llm-server.md §8; /opt/tkv-local/servers/hxs-4/discovery.md
Authority/Version Identified:
  - Fleet PIN = 0.32.15 (blueprint; installer OLLAMA_VERSION mechanism; installer sha256 25f64b81…82c9f == TKV-reviewed baseline).
  - Model: qwen3.5:9b-q4_K_M, digest 6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7.
  - Owner decision O2 (2026-08-26, state log row 21): relax the hxs-4 GPU isolation to both GPUs, then the full ladder.
Applicable Tests/Runbooks: profile §7.1/§7.2; hxs-1 M6/M6b rung + freeze pattern; F-M6-2 unload discipline; F-M6-7 steady-state residency discipline
Contradictions or Gaps:
  1. TKV source snapshot v0.32.11 < pin 0.32.15 (carried gap, recorded openly in all prior pins).
  2. SOURCE FACT (name.go Filepath/String omit the digest part; confirmed live — D-CX-1): the @sha256 FROM
     form is rejected by 0.32.15 create ("invalid model name"); exact-digest identity is proven by pre-create
     /api/tags digest assertion + post-create manifest-layer equality + deterministic-rebuild equality.
  3. RESOLVED: F-CHATX-L1 (window-1 blocker: packet's 24.5 GB capacity premise vs commissioned 8 GB isolation)
     — resolved by owner decision O2; isolation relaxed with provenance (§4R).
Task May Proceed: YES
```

Test plan (recorded before the first mutation, 07:33Z; carried into the resume unchanged plus the O2 amendment step): T0 identity; T1 pin-pre baseline; T2 installer authenticity; T3 pin RC + binary==server==0.32.15; T4 preservation; T5 reload smoke; **T5b (added under O2): versioned one-line drop-in amendment → daemon-reload + restart ollama.service only → both-GPU discovery + usability proof**; T6 per-rung set (create → show num_ctx-only → load → /api/ps size==size_vram → journal KV f16 → needle (window recorded per attempt) → 2 known-answer checks → Xid/OOM scan → controlled unload); T7 KV coefficient from journal `llama_kv_cache` lines across rungs (two deltas); T8 alias freeze (deterministic rebuild + manifest-layer equality) + final state. Stop conditions per work order + resume: pin breaks service (restore 0.32.9 path), OOM, **any Xid → stop and escalate**; one bounded correction per correctable step.

## 2. PIN 0.32.9 → 0.32.15 — **COMPLETE, all tests PASS** (FACT, window 1)

### 2.1 Pre-change state (07:34–07:36Z; evidence 00–03)

- Identity (T0): `hostname` = `hxs-4`; `$SSH_CONNECTION` = `192.168.50.204 … 192.168.50.203 22`; machine-id `a3244b92b98448ad83da8ecad6511889` (== discovery); eno1 `192.168.50.203/24` MAC `bc:fc:e7:3e:10:66`; `sudo -n` OK.
- Version (T1): `ollama version is 0.32.9`; `/api/version` 0.32.9; binary `/usr/local/bin/ollama` 38,912,880 B, sha256 `ce10ceda50776682fd989fd62de4f1dce4892711016b2cb23067d5767599578e`.
- Service: active+enabled, `NRestarts=0`; unit sha256 `b15f3fd1b35239683c73eb5cbc4523693de453f08582c2ee7165315c0f893adc`; drop-in `hx-commissioning.conf` sha256 `9d90a9918701f2dd283729782bd6d4563fdcd996fcd19653653a72c5a6471bb3` (then 7 Environment lines incl. `OLLAMA_NO_CLOUD=1`).
- Model: `qwen3.5:9b-q4_K_M`, digest `6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7`, size **6,594,474,711 B** (live /api/tags; row 76's 6,594,474,111 was a transposition; live authoritative), gguf/qwen35, 9.7B, Q4_K_M, ctx max 262,144, capabilities vision/completion/tools/thinking; store 6.2 G, 4 blobs.
- Baked tag params (FACT, `ollama show`): `temperature 1`, `top_k 20`, `top_p 0.95`, `presence_penalty 1.5` — **no num_ctx baked**; effective ctx 65536 came from the drop-in `OLLAMA_CONTEXT_LENGTH=65536`. Weights blob `sha256-dec52a44569a…99d37c`; `TEMPLATE {{ .Prompt }}`, `RENDERER qwen3.5`, `PARSER qwen3.5`; Apache-2.0.
- Listener `127.0.0.1:11434` only; `/api/ps` empty; RAM 31 Gi; swap 0 B; root 847 G free; zstd present; **Xid = 0**.

### 2.2 Installer authenticity (T2; 07:37Z)

`curl -fsSL https://ollama.com/install.sh` → sha256 `25f64b810b947145095956533e1bdf56eacea2673c55a7e586be4515fc882c9f`, **byte-identical** to TKV `ollama-main/scripts/install.sh` — the reviewed baseline executed on hxs-1/hxs-2/hxs-3. Hash-verified on both sides before execution; never blind-piped.

### 2.3 Pin execution (T3; 07:38:16Z)

`OLLAMA_VERSION=0.32.15 sh /tmp/ollama-install-reviewed.sh` (as `hxsa`; script self-elevates via NOPASSWD sudo — the hxs-2/hxs-3 method) → **INSTALL_RC=0**, ended `>>> NVIDIA GPU installed.` (zero apt/dkms/modprobe activity).

### 2.4 Post-pin verification (T3/T4; 07:38–07:39Z; evidence 06)

| Property | Pre (0.32.9) | Post (0.32.15) | Verdict |
| --- | --- | --- | --- |
| `ollama --version` / `/api/version` | 0.32.9 / 0.32.9 | **0.32.15 / 0.32.15** | binary == server == pin ✓ |
| Binary | 38,912,880 B `ce10ceda…` | 39,159,472 B `eb99a47aad366636488ebd9c163a9180254dffcfdfe359939f9aabc36e2399c8` | ✓ |
| Service | active+enabled | active+enabled, `NRestarts=0` | ✓ |
| Main unit sha256 | `b15f3fd1…93adc` | `11758d469d3f103e53a9612a8ffcb3a3e61834c994c08d412bb051f3c827dbd3` | installer-rewritten; == hxs-2/hxs-3 unit; diff vs pre = PATH line only ✓ |
| Drop-in | `9d90a991…1bb3` | `9d90a991…1bb3` | byte-identical at pin time ✓ |
| Model | digest `6488c96f…93ea7`, 6,594,474,711 B | unchanged; journal `total blobs: 4`, `removed: 0` | store intact ✓ |
| Listener | 127.0.0.1:11434 only | 127.0.0.1:11434 only; `Listening on 127.0.0.1:11434 (version 0.32.15)` | ✓ |
| Xid | 0 | 0 | ✓ |

### 2.5 Reload smoke (T5; 07:40–07:42Z; evidence 08) — PASS, and the window-1 blocker surfaced

Load 14.15 s; known-answer `17 × 23` → **391**, stop; unload polled empty; LAN refusal re-proven from hxs-5. The same smoke exposed F-CHATX-L1 (§3).

**Pin verdict: PASS — 0.32.15 in service, model/store/drop-in/bind preserved, smoke clean.** Recorded pin rollback (never needed): `OLLAMA_VERSION=0.32.9 sh <same reviewed installer>`; pre-hashes in §2.1.

## 3. F-CHATX-L1 — window-1 blocker (history; RESOLVED by owner decision O2)

Recorded in full as the window-1 finding (governance trail: state log row 19, incl. the governor's open correction of row 76's "RESIDENT" wording):

- Packet premise (AUTHORITY as written): "prove resident (100% VRAM on the 5060 Ti — 24.5 GB total makes this capacity-trivial, still measured)".
- FACT: the owner-commissioned drop-in (since 2026-08-14/23, "GPU isolation is MANDATORY") restricted Ollama to the RTX 5060 8 GB only (`CUDA_VISIBLE_DEVICES=GPU-cc758e31…`, Vulkan disabled) — Ollama-usable VRAM 7.5 GiB.
- FACT: at the commissioned default ctx 65536 the model loaded **28%/72% CPU/GPU** (size 8,517,289,242 B vs size_vram 6,109,381,261 B; identical size_vram under 0.32.9 and 0.32.15 — the split predated the pin; row 76 had read the VRAM portion as residency).
- FACT (journal fit-log): model 4,717 + context 2,098 + compute 152 MiB vs 7,531 free → "cannot meet free memory target of 1919 MiB" → layer offload.
- Window-1 conclusion: no rung could meet the mandated 100%-VRAM proof under the isolation; no authorized knob existed → escalated (options O1–O4). **Owner chose O2 (2026-08-26, state log row 21).**

---

# PART 2 — Window 2 (09:15–09:41Z): O2 resumption — amendment, ladder, freeze

## 4R. Isolation relaxation (owner decision O2) — **COMPLETE** (FACT)

### 4R.1 Pause-window state reconciliation (before any mutation)

- Identity re-verified 09:15:42Z (hostname hxs-4, peer .203 from .204, sudo -n OK, uptime 16:52 — no reboot).
- **Drop-in delta detected and attributed (RECORD):** drop-in hash was `f78de2292a96154c3ebe9eeff5d4172cf399989d350d1c987627604fe9345e41` (not window-1's `9d90a991…`), mtime 07:47:09Z, content minus the `OLLAMA_NO_CLOUD=1` line; service restarted 07:47:09Z ("Ollama cloud disabled: false"). Attribution (AUTHORITY): the ratified fleet web-search enablement — state log row 20 (`13-esme-websearch-enable.md`, PASS: exactly `OLLAMA_NO_CLOUD=1` removed per host drop-in + daemon-reload + service-only restart on all four hosts) and hxs-1 log row 78 (owner decision: web search ENABLED; D6 superseded for the web-search class). The f78de229 content was therefore the **authoritative current state**, and the resume's "preserve every other setting" applied to its 6 remaining Environment entries. Drop-in hash chain fully explained: `9d90a991…` (commissioning, window-1 baseline) → `f78de229…` (ratified web-search edit) → `9d1d024c…` (this O2 amendment).
- Both GPU UUIDs captured fresh from `nvidia-smi -L`: GPU0 RTX 5060 Ti `GPU-11b1a30e-8c11-001b-7b8b-7b1e15ab6978`; GPU1 RTX 5060 `GPU-cc758e31-d23b-3c53-bee6-dae3299a6f11`.

### 4R.2 The versioned amendment (T5b; 09:18:26Z candidate, deployed 09:18:45Z)

Exactly one line changed; every other setting preserved (Vulkan-disabled lines, `OLLAMA_CONTEXT_LENGTH=65536`, `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1`; comment block untouched):

```diff
--- hx-commissioning.conf.pre (sha256 f78de2292a96154c3ebe9eeff5d4172cf399989d350d1c987627604fe9345e41)
+++ hx-commissioning.conf.post (sha256 9d1d024ccc27571358adf10b6412acba0045c441217810d099572b5c1b70ca06)
@@ -3,7 +3,7 @@
 [Service]
-Environment="CUDA_VISIBLE_DEVICES=GPU-cc758e31-d23b-3c53-bee6-dae3299a6f11"
+Environment="CUDA_VISIBLE_DEVICES=GPU-11b1a30e-8c11-001b-7b8b-7b1e15ab6978,GPU-cc758e31-d23b-3c53-bee6-dae3299a6f11"
 Environment="GGML_VK_VISIBLE_DEVICES=999"
```

- Provenance (RECORD, per the governor's wording): **owner decision O2, 2026-08-26 — isolation relaxed from RTX 5060-only to both GPUs; the original "GPU isolation is MANDATORY" commissioning predates Chat-X's backend role.**
- Deploy: remote pre-copy captured → local one-line edit → diff verified exactly one line → scp → remote hash match → `sudo -n install -o root -g root -m 0644` → installed hash `9d1d024c…` verified → `sudo -n systemctl daemon-reload` → `sudo -n systemctl restart ollama` (**ollama.service ONLY**). Transfer copy removed.

### 4R.3 Verification (09:19–09:20Z; evidence 15/16) — **23.0 GiB usable, 100% VRAM proof**

- Journal: `user overrode visible devices …(both UUIDs)`; `inference compute id=0 … "NVIDIA GeForce RTX 5060 Ti" total 15.5 GiB available 15.3 GiB`; `inference compute id=1 … "NVIDIA GeForce RTX 5060" total 7.5 GiB available 7.4 GiB`; `vram-based default context total_vram="23.0 GiB"`; `Listening on 127.0.0.1:11434 (version 0.32.15)`.
- Effective Environment: both UUIDs + all preserved entries (verified via `systemctl show`).
- **Usable VRAM before → after: 7.5 GiB (5060 only) → 23.0 GiB (15.5 + 7.5, both GPUs)** (hardware total 24,462 MiB ≈ 23.9 GiB; Ollama-reported total 23.0 GiB).
- Usability proof (steady-state, F-M6-7 discipline — discovery completed 09:19:14Z before any load): bare tag at its 65536 default → load 7.18 s, `/api/ps` **size == size_vram == 8,044,454,869 B, 100% GPU**, ctx 65536 (was 28%/72% CPU/GPU under the isolation); 5060 Ti 8,848 MiB used; unloaded polled to `/api/ps` empty.
- Model list intact; loopback-only; `NRestarts=0` (the manual amendment restart reset the counter — accounted; zero crash restarts all window); **Xid = 0**.

## 5R. The three-rung ladder — **COMPLETE** (FACT)

Rung Modelfiles (sha256 verified identical on both sides before each create): FROM the frozen artifact (`FROM qwen3.5:9b-q4_K_M`, base digest asserted == `6488c96f…93ea7` via /api/tags immediately before each create) with **`PARAMETER num_ctx` as the ONLY changed parameter**; `ollama show` per rung confirms exactly `num_ctx` + the 4 baked params (`temperature 1`, `top_k 20`, `top_p 0.95`, `presence_penalty 1.5`) — no sampling/system/template lines anywhere.

- **D-CX-1 (bounded correction 1 of 1, disclosed):** the first 32k create used `FROM …@sha256:<digest>` → `400 Bad Request: invalid model name` (zero mutation; the digest form is unsupported by 0.32.15 create — consistent with the window-1 source reading). Correction: plain-tag FROM with the three independent identity proofs (pre-create digest assertion; post-create manifest-layer equality, §6R; deterministic rebuild, §6R). Final Modelfile v2 hashes: 32k `225f2a89a26edc0c4dda409bac473affd70f61e1cddd7571ecca861c25c25cf2`, 64k `0af4251166bf1b8985b52b606538959a96dda1ae3aeb596ed4fc47476873e44b`, 128k `ddf4fad191b522aefe431faa4135098c36844dd3c70b8f3a1c9bfd1b3905c164`.

### 5R.1 Per-rung table

| Proof | **32,768** (`hx-qwen3.5-9b-32k`) | **65,536** (`hx-qwen3.5-9b-64k`) | **131,072** (`hx-qwen3.5-9b-128k`) |
| --- | --- | --- | --- |
| Alias digest | `3ef4f2846872a96ec1a8c3321b18ee0ab39e8ac7814374dd94bd7de601279b80` | `5936a390c6c22594ce49e8c77187fc92f4a81126fd04a4eabad7c000b30447d2` | `09faff0fd4d3a5793c4bb99222e865cb9d210cb582319a77bf20d52c5330bf37` |
| `ollama show` params | num_ctx 32768 + 4 baked only ✓ | num_ctx 65536 + 4 baked only ✓ | num_ctx 131072 + 4 baked only ✓ |
| Load (steady-state) | 7.17 s | 7.03 s | 7.14 s |
| Residency `/api/ps` | **size == size_vram == 7,373,575,942 B** | **== 7,725,656,308 B** | **== 10,879,867,286 B** |
| Processor / ctx | **100% GPU** / 32768 ✓ | **100% GPU** / 65536 ✓ | **100% GPU** / 131072 ✓ |
| Per-GPU MiB (Ti/5060) | 5,396 / 2,946 | 8,544 / 0 | 7,454 / 4,236 |
| **KV f16 (journal `llama_kv_cache`)** | **1,024.00 MiB** (K 512 + V 512, f16; 32,768 cells, 8 layers) | **2,048.00 MiB** (K 1,024 + V 1,024; 65,536 cells) | **4,096.00 MiB** (K 2,048 + V 2,048; 131,072 cells) |
| **KV B/token** | 32,768 | 32,768 | 32,768 |
| Needle (versioned `needle_probe.py`, rung's own alias) | **~95% NOT MET** — see A-1 below | **PASS**: 62,125 tok = **94.8%**, `done_reason stop`, needle **found** (`FALCON-61803` line 1550/2385, 65% doc depth), prefill 2,442.1 tok/s cold, eval 2,767, wall 79.6 s | **PASS**: 124,161 tok = **94.7%**, `stop`, **found** (line 3101/4771, 65% doc depth), prefill 2,996.6 tok/s, eval 4,476, wall 170.3 s |
| Known-answer spot checks (identical across rungs) | KA1 `391` stop ✓ · KA2 `13` stop ✓ | KA1 `391` stop ✓ · KA2 `13` stop ✓ | KA1 `391` stop ✓ · KA2 `13` stop ✓ — **flat across all rungs** |
| Journal (rung window) | 0 Xid / 0 OOM / 0 ERROR | 0 / 0 / 0 | 0 / 0 / 0 |
| Controlled unload | polled to `/api/ps` empty ✓ | ✓ | ✓ |
| **Rung verdict** | **CAPACITY PASS; needle ~95% attenuated (A-1)** | **PASS (all)** | **PASS (all)** |

### 5R.2 KV derivation (T7) — exactly linear, f16

Journal-direct per rung (`llama_kv_cache: size = … (N cells, 8 layers, 1/1 seqs), K (f16) …, V (f16) …`):
Δ(32k→64k) = 2,048.00 − 1,024.00 = 1,024.00 MiB / 32,768 tokens = **32,768 B/token**; Δ(64k→128k) = 4,096.00 − 2,048.00 = 2,048.00 MiB / 65,536 tokens = **32,768 B/token**. **KV f16 = 32,768 B/token exactly linear** (8 KV layers — hybrid-attention architecture; K and V both f16, confirmed per line). This supersedes the window-1 estimate ~33,554 B/token (derived from the rounded 2,098-MiB fit figure; the exact allocation is 2,048.00 MiB). Note (RECORD, F-M6-7 class): `/api/ps` absolute size varies with runner placement/flags (the bare tag at 65536 measured 8,044,454,869 B single-GPU vs the 64k rung's 7,725,656,308 B; the 128k load split across both GPUs) — the journal `llama_kv_cache` lines, not `/api/ps` size deltas, are the KV ruler on this host.

### 5R.3 A-1 — the 32k needle attenuation (disclosed in full; no test re-rolled to force a pass)

Four needle attempts on the 32k rung, all preserved (`ev/needle-32k*.json`):

| Attempt | Prompt tokens (% of 32,768) | Headroom (tokens) | Result | eval_count | thinking_chars |
| --- | --- | ---: | --- | ---: | ---: |
| 1 (target ~95%) | 31,237 (95.3%) | 1,531 | `done_reason=length`, needle not reached | 1,531 (truncated) | 5,637 |
| 2 (~91.5%) | 29,989 (91.5%) | 2,779 | `done_reason=length`, needle not reached | 2,779 (truncated) | 10,469 |
| 3 (~86.3%) | 28,273 (86.3%) | 4,495 | **stop + found**, wall 11.2 s | 209 | (concise) |
| 4 (~89.5%) | 29,313 (89.5%) | 3,455 | **stop + found**, wall 68.1 s | 3,432 | (long, converged) |

Interpretation (INFERENCE from these FACTs): this thinking 9B's reasoning on the needle probe grows non-convergently when the remaining generation budget is ≲2,800 tokens at ≥91% depth (prompt + thinking exhausts the context before the answer emits — attempts 1/2 ended exactly at 32,768 total tokens); at ≤89.5% it completes with `stop` and the needle found. Retrieval at depth works (two passes); the **work-order's "~95% depth, done_reason=stop" target is NOT MET at the 32k rung** — a measured model-behavior limit at small context, not a capacity/KV/residency failure (all of which passed), and not a work-order stop condition. The 64k and 128k rungs met ~95% cleanly (94.8%/94.7%, stop+found). The governor's attention is drawn to this asymmetry: it is a Chat-X-specific qualification fact for any future deep-context consumer of the 32k profile (recorded for Carol's catalog; the blueprint's alias-table note for hx-qwen3.5-9b-32k should carry "needle completion proven to 89.5%; ~95% truncates thinking-model output").

## 6R. Alias freeze — **COMPLETE, digest equality proven ×3** (FACT)

`/api/tags` final: exactly `qwen3.5:9b-q4_K_M` (base, untouched) + the three profile aliases (tags only, none resident).

| Alias | Frozen digest | Deterministic rebuild (re-create from the same v2 Modelfile) | Manifest-layer equality vs base manifest |
| --- | --- | --- | --- |
| `hx-qwen3.5-9b-32k:latest` | `3ef4f2846872a96ec1a8c3321b18ee0ab39e8ac7814374dd94bd7de601279b80` | **EQUAL** (reproduced exactly) | weights `dec52a44569a…99d37c` + license `7339fa418c…85cb2` **identical** (marked `"from":"qwen3.5:9b-q4_K_M"`); only the params layer differs (`7b8da8e2…33300`, 81 B — carries num_ctx 32768) |
| `hx-qwen3.5-9b-64k:latest` | `5936a390c6c22594ce49e8c77187fc92f4a81126fd04a4eabad7c000b30447d2` | **EQUAL** | same shared layers; params layer `61dd744d…871e` (81 B — num_ctx 65536) |
| `hx-qwen3.5-9b-128k:latest` | `09faff0fd4d3a5793c4bb99222e865cb9d210cb582319a77bf20d52c5330bf37` | **EQUAL** | same shared layers; params layer `b44b4a03…2737` (82 B — num_ctx 131072) |

All three alias config blobs identical (`ba00e09d…e606`, 213 B — same architecture metadata as the base family). Each alias is content-addressed to the frozen weights; it cannot resolve to anything else and does not follow the upstream tag if re-pulled. No `ollama rm` anywhere (no model-store deletions — creates added three small params blobs only; journal: `total blobs: 4`, `unused blobs removed: 0` at the last service start; store 6.2 G).

**Default usage reference (RECORD): `hx-qwen3.5-9b-64k`** — matches the drop-in's `OLLAMA_CONTEXT_LENGTH=65536` (Chat-X's operating context before and after) and the model's commissioned default; the alias set is the consumer-facing reference per blueprint §8 (alias-only model reference). No config was repointed (preload/persistence/endpoint remain PARKED owner decisions — none implemented).

## 7R. Final state (FACT, 09:40:44Z; evidence 42/43)

- Ollama **0.32.15** binary==server, active+enabled, `NRestarts=0` (zero crash restarts all day); unit `11758d46…27dbd3`; drop-in `9d1d024c…ca06` (the O2 amendment); effective env = both GPUs + Vulkan-disabled + ctx 65536 + NUM_PARALLEL=1 + MAX_LOADED_MODELS=1 (NO_CLOUD absent per the ratified web-search change).
- Tags: base + 3 frozen aliases; **nothing resident** (`/api/ps` empty — owner-provisioned on-demand posture restored; all rung loads unloaded with poll-to-empty discipline).
- Endpoint: loopback-only `127.0.0.1:11434` (LAN refusal re-proven 07:42Z; unchanged since); no firewall anywhere (owner rule); no endpoint change.
- Journal whole window (09:15–09:41Z): **0 ERROR lines, 0 OOM; Xid = 0** (kernel, since 09:15; also 0 across all boots at baseline); only the known F-E2-class GPU-discovery watchdog WARN lines at cold starts.
- RAM 1.4 Gi used; swap 0 B; uptime 17:17 continuous (**no reboot**); remote scratch `/tmp/esme-chatx` removed and verified absent; local askpass + wrappers deleted (below).
- What changed end-to-end (all authorized, all versioned): Ollama 0.32.9→0.32.15; main unit (installer, PATH line); drop-in one line (O2, both GPUs); three alias tags added (params blobs only). What did not change: base tag/digest/weights; all other drop-in lines; bind; firewall; OS/driver; no other models; no sampling changes; no store deletions; no preload/persistence unit; no reboots.

## 8R. Sequential command log — resume window (profile §11.3; sanitized; window-1 log preserved below in §9)

All remote commands as `hxsa@hxs-4` from `hxs-5` (askpass read the credential-record row at execution time only; strict host key; `sudo -n` only). Times UTC, approximate.

| Seq | Time | Where | Command (shape) | Exit | Evidence |
| ---: | --- | --- | --- | ---: | --- |
| 18 | 09:15 | local | rebuild workspace + askpass/rssh/rscp (0700); syntax + shape tests (byte count only) | 0 | §7R note |
| 19 | 09:15 | ssh | identity + state-unchanged recheck; fresh GPU UUIDs; pre-change drop-in capture | 0 | ev11 |
| 20 | 09:16 | ssh+local | drop-in delta forensics (hash f78de229, mtime 07:47:09Z, NO_CLOUD removed) → attributed to ratified web-search session (state log rows 20/78); sshd/auth + journal corroboration | 0 | ev12 |
| 21 | 09:18 | local | one-line sed → candidate; `diff -u` = exactly 1 line; hashes pre/post | 0 | ev13 |
| 22 | 09:18 | ssh | scp candidate (hash match); `sudo -n install` 0644 root:root; installed hash `9d1d024c…`; daemon-reload; **restart ollama.service only**; active; transfer copy removed | 0 | ev14 |
| 23 | 09:19–20 | ssh | verify: both GPUs discovered (15.5 + 7.5 = 23.0 GiB); effective env; model intact; loopback; Xid=0 | 0 | ev15 |
| 24 | 09:20 | ssh | usability smoke: bare-tag load 7.18 s → size==size_vram 8,044,454,869, 100% GPU; unload polled empty | 0 | ev16 |
| 25 | 09:21 | local+ssh | author 3 rung Modelfiles + `ka_spotcheck.py`; sha256; scp fixtures (`needle_probe.py`, `fixtures_corpus.py` — versioned hashes match) + staged files; remote hashes match | 0 | ev17/18 |
| 26 | 09:22 | ssh | 32k create attempt 1 (@sha256 FROM) → **400 invalid model name**, zero mutation (D-CX-1); Modelfiles corrected to plain-tag FROM; new hashes both sides | 1→0 | ev20/21 |
| 27 | 09:23 | ssh | base-digest assert; 32k create → `3ef4f284…`; `ollama show` num_ctx-only; load 7.17 s; residency 100% VRAM ctx 32768; journal KV 1,024 MiB | 0 | ev22/23/24/36 |
| 28 | 09:24–30 | ssh | 32k needle ×4: 95.3% length; 91.5% length; 86.3% stop+found; 89.5% stop+found (A-1) | 1/1/0/0 | ev25/26/28/29/30 |
| 29 | 09:31 | ssh | 32k KA spot checks (391/13, stop, flat); journal 0 Xid/OOM; unload polled empty | 0 | ev31 |
| 30 | 09:31–34 | ssh | 64k create → `5936a390…`; show; load 7.03 s; residency 100% VRAM ctx 65536 (Ti-only 8,544 MiB); needle 62,125 tok 94.8% stop+found (prefill 2,442.1); KA flat; journal clean; unload | 0 | ev32/33/34 |
| 31 | 09:34–39 | ssh | 128k create → `09faff0f…`; show; load 7.14 s; residency 100% VRAM ctx 131072 (7,454+4,236); KV 4,096 MiB; needle 124,161 tok 94.7% stop+found (prefill 2,996.6, eval 4,476); KA flat; whole-ladder journal 0 Xid/0 ERROR/no OOM; unload | 0 | ev35/37/38/39 |
| 32 | 09:39–40 | ssh | alias freeze: deterministic rebuild ×3 → digests EQUAL; manifests read (sudo cat) → layer equality vs base (weights+license shared; params-only delta) | 0 | ev40/41 |
| 33 | 09:40 | ssh | final state sweep (service, NRestarts=0, listener, ps empty, 0 ERROR, Xid=0, store, hashes); evidence JSONs → hxs-5; remote scratch removed (verified) | 0 | ev42/43 |
| 34 | ~09:41+ | local | deliverable updated; **askpass + wrappers deleted** (verified absent); sanitized evidence retained transiently at `hxs-5:/tmp/esme-chatx/ev/` | 0 | §7R note |

## 9. Window-1 command log (preserved, sanitized)

| Seq | Time | Where | Command (shape) | Exit | Evidence |
| ---: | --- | --- | --- | ---: | --- |
| 1 | 07:16 | local | `hostname; date; ip` — session host hxs-5/.204 verified | 0 | §1 |
| 2 | 07:16–26 | local | knowledge review (profile, WO/CP, AGENTS.md, pattern docs, fixtures 10/10 OK, TKV survey, source checks) → receipt + test plan | 0 | §1 |
| 3 | 07:30 | local | credential-file shape probes (line numbers, field counts, whitelisted labels only — values never printed) | 0 | §1 |
| 4 | 07:31 | local | workspace (0700); askpass + wrappers (0700); syntax + shape tests; awk `END`-rule fix (local scaffolding) | 0 | §7R note |
| 5 | 07:34 | ssh | identity: hostname, peer, machine-id, MAC, `sudo -n`, uptime | 0 | ev00 |
| 6 | 07:35–36 | ssh | baseline: binary/version/api/service/unit+drop-in hashes/listeners/models/GPUs/store/journal/Xid=0; unit+drop-in content | 0 | ev01/02/03 |
| 7 | 07:37 | local+ssh | installer download; sha256 == TKV baseline (byte-identical); scp; remote hash match | 0 | ev04 |
| 8 | 07:38 | ssh | `OLLAMA_VERSION=0.32.15 sh …` → RC=0, "NVIDIA GPU installed." | 0 | ev05 |
| 9 | 07:38–39 | ssh | post-pin verify (0.32.15 binary==server, hashes, model intact, loopback, journal, Xid=0); base identity `ollama show` | 0 | ev06/07 |
| 10 | 07:40–42 | ssh | smoke: load 14.15 s → **split discovered** (F-CHATX-L1) → KA 391 stop → nvidia-smi → unload empty; LAN refusal (local) | 0 | ev08 |
| 11 | 07:43 | ssh | journal fit-log capture (KV 2,098 MiB @65536; offload) | 0 | ev09 |
| 12 | 07:44 | ssh | state preserved: remote installer copy removed; ps empty; active; list intact | 0 | ev10 |
| 13–17 | 07:45+ | local | deliverable rev 1 written (receipt NO); askpass deleted; escalation to Kimi-K3 → **owner decision O2 recorded (state log row 21)** | 0 | §3 |

Sanitization confirmed (both windows): no secret value printed, logged, stored, or placed on any command line; credential probes emitted metadata only; the askpass helpers (rebuilt for window 2, deleted at task end) read the credential-record row at execution time only. Session evidence ev00–ev43 contains command output only — no secrets, no thinking content (counts only per A01 §5.2).

## 10R. Configuration files (profile §11.2)

| File | Pre sha256 | Post sha256 | Diff | Owner/mode |
| --- | --- | --- | --- | --- |
| `/etc/systemd/system/ollama.service` | `b15f3fd1…93adc` (0.32.9-era) | `11758d46…27dbd3` | installer rewrite; PATH line only | root:root 0644 |
| `/etc/systemd/system/ollama.service.d/hx-commissioning.conf` | `f78de229…45e41` (ratified web-search state) | **`9d1d024c…ca06`** | **exactly one line** (CUDA_VISIBLE_DEVICES both UUIDs), §4R.2 | root:root 0644 |
| `hx-commissioning.conf.bak-20260823` | `eced5a8f…f1c0` | `eced5a8f…f1c0` | — untouched | root:root 0644 |
| Rung Modelfiles (session staging, removed with scratch) | — | 32k `225f2a89…5cf2`; 64k `0af42511…e44b`; 128k `ddf4fad1…c164` | creations; identical bytes both sides (v2 after D-CX-1) | hxsa 0644 (transient) |

Effective runtime values post-reload: §4R.3 (`systemctl show` Environment + journal discovery lines). Rollback (all steps reversible; none needed): pin → `OLLAMA_VERSION=0.32.9 sh <reviewed installer>`; amendment → reinstall the `f78de229…` content (one-line inverse, full pre-content in ev11/ev13) + daemon-reload + restart ollama.service; aliases → `ollama rm <alias>` (tags only; blobs shared — separate approval per fleet convention; not executed).

## 11R. Validation summary (profile §11.4)

- **What was tested:** T0–T5 (window 1, pin — all PASS); T5b (O2 amendment: one-line diff, deploy, both-GPU discovery, 23.0 GiB usable, 100%-VRAM bare-tag proof — PASS); T6 ×3 rungs (create/show/load/residency/KV/needle/spot/journal/unload); T7 KV linearity; T8 alias freeze + final state. Every defined test executed except none — no NOT-RUN items remain.
- **Passed:** pin suite; amendment; all residency proofs (3/3, size==size_vram, 100% GPU); KV f16 exactly linear 32,768 B/token (two journal deltas); needles 64k 94.8% + 128k 94.7% (stop+found); 32k needle at 89.5%/86.3% (stop+found); spot checks flat ×3 (391, 13; stop); alias digest equality ×3 (rebuild + manifest layers); journal 0 Xid/0 OOM/0 ERROR all window.
- **Failed (disclosed, not concealed):** 32k needle at ~95% (attempts at 95.3% and 91.5% → `done_reason=length`, context exhausted by thinking) — attenuation A-1, §5R.3. No stop condition hit (pin healthy; no OOM; Xid=0 throughout).
- **Corrections used:** bounded correction 1 of 1 (D-CX-1, @sha256 FROM rejected → plain-tag FROM + triple identity proof). No model test was re-run to reach a pass (the four 32k needle attempts are distinct depths, all preserved).
- **Current Ollama state:** 0.32.15 active/enabled, `NRestarts=0`, loopback-only, both GPUs usable (23.0 GiB), on-demand posture (nothing resident).
- **Current model state:** base `qwen3.5:9b-q4_K_M` @ `6488c96f…93ea7` + frozen aliases `hx-qwen3.5-9b-32k` (`3ef4f284…`), `-64k` (`5936a390…` — **default usage reference**), `-128k` (`09faff0f…`); tags only, none loaded.
- **Rollback readiness:** §10R inverses exact; pre-hashes recorded for every changed file; nothing destructive executed anywhere.
- **Remaining risks/decisions:** A-1 (32k deep-depth completion limit → catalog + blueprint alias note); F-M6-7 class (absolute-size variance by placement — use journal KV lines); carried F-E2 watchdog class (benign); parked owner decisions untouched (preload/persistence, LAN posture, firewall — none implemented).

**Second Brain evaluation (standing directive, per work order):** (1) opportunity identified — yes; (2) pattern — four-host ladder/profile uniformity, completed with this host; (3) disposition — **implemented**: Chat-X's measured ladder (incl. the A-1 32k completion limit and the exact 32,768 B/token KV coefficient), the three-alias profile set with digest equalities, the O2 amendment record, and the drop-in hash-chain reconciliation (commissioning → web-search → O2) are catalog content at handoff; (4) evidence — §4R–§7R: the blueprint's uniformity claim now rests on four measured ladders, and Chat-X's record carries the two facts that were wrong in the packet (24.5 GB premise; "baked" ctx) corrected openly. This deliverable goes to Carol for catalog receipt; handoff OPEN until the receipt is cited in the governing log.

**Completion:** `PASS — TASK COMPLETE` (final gate §18: every applicable question answered yes; A-1 and D-CX-1 disclosed; no stop condition hit; no mandatory test failure concealed — the 32k ~95% needle is reported as not met with all four attempts preserved).

```text
Task May Proceed: YES
(with one recorded rung attenuation, A-1: the 32k rung's needle at ~95% depth did not complete —
 done_reason=length at 95.3% and 91.5% (thinking-model generation-headroom exhaustion);
 needle proven stop+found at 89.5% and 86.3% on the same rung; 64k/128k met ~95% cleanly.
 All other work-order requirements PASS: pin 0.32.15, O2 both-GPU relaxation (7.5 -> 23.0 GiB),
 3/3 rungs 100% VRAM, KV f16 exactly 32,768 B/token, spot checks flat, aliases frozen with
 digest equality, -64k default usage reference recorded, endpoint loopback-only, Xid=0.)
```

Signed: **john / Esme** — Expert Ollama Engineer, session `john-chatx-20260826-01`, 2026-08-26T09:41Z (UTC).
