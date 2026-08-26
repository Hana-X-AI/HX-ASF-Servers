# 08 — Esme (john): M6 Context Ladder (32K/64K/128K) + Three-Profile Freeze on Coder-X (hxs-2)

`[TASK COMPLETE — EVIDENCE ATTACHED]`

| Field | Value |
| --- | --- |
| Report ID | ESME-HXS2-M6-LADDER-PROFILES-001 |
| Task ID | WO-HXS2-JOHN-M6-001 (`PILOT-HXS2-CODERX-BACKEND-001`, milestone M6+M6b) |
| Agent | john / Esme (profile `agents/john/profile.md`), session `john-m6-20260826-01` |
| Target host | `hxs-2` (192.168.50.201), Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic, driver 580.173.02 |
| Executed from | `hxs-5` (192.168.50.204) via SSH `hxsa@192.168.50.201` — askpass helper READ the credential-record table row (`ssh-info.md` "SSH password" row, line 25 pipe-field 3, code-span unwrapped) AT EXECUTION TIME ONLY; no extracted copy ever existed; helper deleted at task end (verified) |
| Host-key check | STRICT — pinned ED25519 `SHA256:b2qlMQz496nUbuZKJu3wwmR0QY/EmN0KQtW4rM2HDcQ` (rick M1 F-05), re-verified pre-flight; `StrictHostKeyChecking=yes` on every connection |
| Window (UTC) | 2026-08-26T07:15Z → 07:31Z (read-only drift check → escalation `08-esme-m6-escalation-xid31.md`); **resumed 07:40:36Z → 08:12Z under owner decision O1 — RESUME ARMED** (governor supplements, 2026-08-26) |
| Ollama | 0.32.15 (binary == server; unchanged from M4) |
| Frozen artifact | `mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M` @ digest **`ca661423d6b51ebeaca999f22cfc0f30c0851b2a6f328b2737bd8cb6eb90c1df`** (untouched) |
| GPUs | 2× RTX 5060 Ti 16,311 MiB (rick's plane, untouched) |
| Stop conditions | OOM / unapproved CPU fallback / any Xid (armed Xid-watch, governor supplement 1): **none hit** |

Evidence labels: **FACT** (live host output) / **AUTHORITY** (owner decision, work order, governance) / **UPSTREAM** / **INFERENCE** / **RECORD**.
All secrets excluded; `sudo -n` only; thinking content never persisted (counts only, A01 §5.2-class); every model request in this report used synthetic prompts.

---

## 1. Knowledge review receipt (profile §4.3; resume edition)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path /opt/tkv-local/ollama resolves locally here); target hxs-2 (192.168.50.201)
Source: /opt/tkv-local/ollama + HX-ASF-Servers controlling docs
Reviewed At: 2026-08-26T07:15Z → 07:22Z (carried into the resume; nothing in it was invalidated by O1)
Relevant Files: 10 reviewed — agents/john/profile.md; agents/ roster = carol, john, kimi-k3, rick (all current);
  pilots/PILOT-HXS2-CODERX-BACKEND-001/01-state-log.md (rows 1–13); 07-esme-m4-install.md (hxs-2 identity, frozen hashes);
  goals/2026-08-26-hxs2-qwen36-coderx-backend.md (D5: operating ctx 65,536; ladder 32K→64K on the exact digest before freeze);
  servers/BLUEPRINT-llm-server.md §4 (context plane: ladder on the exact digest; KV measured per model; /api/ps context_length is proof);
  pilots/PILOT-HX1-OLLAMA-QWEN27B-001/22-esme-m6-capacity-ladder.md + 29-esme-m6b-profiles.md (hxs-1 rung procedure, digest
  equality, repoint pattern, F-M6-2 unload discipline, F-E4 restart-not-start);
  fixtures/ (needle_probe.py alias-parameterized; fixtures_corpus.py; sha256sums.txt — all 10 verified OK 07:21Z; executed-copy
  hashes on hxs-2 re-verified identical before use, §7);
  /opt/tkv-local/ollama: docs/modelfile.mdx:57,149 (PARAMETER num_ctx); docs/context-length.mdx (VRAM-based defaults);
  docs/faq.mdx:354 + envconfig/config.go:222,230,317,336 (OLLAMA_KV_CACHE_TYPE default f16; OLLAMA_CONTEXT_LENGTH env)
Authority/Version Identified: Ollama 0.32.15 pinned (binary == server, M4). TKV source snapshot (v0.32.11) predates the installed
  0.32.15 for the qwen35moe family (carried gap from M4): empirical API evidence on the actual host is the authority for
  model-specific behavior; snapshot cited only where version-independent (env surface, docs).
Applicable Tests/Runbooks: WO-HXS2-JOHN-M6-001 rung procedure; hxs-1 22/29 pattern; F-M6-2 poll-to-empty unload; F-E4 restart-not-start;
  owner decision O1 — RESUME ARMED with governor supplements 1–6 (Xid-watch; fresh pre-state; hx2.conf naming; owner-session closure).
Contradictions or Gaps:
  1. TKV snapshot predates installed 0.32.15 (carried from M4; disposition unchanged).
  2. RESOLVED at resume: work order said "hx1.conf"; governor supplement 3 settled hx2.conf as the drop-in — preload MODEL+DIGEST
     repoint + OLLAMA_CONTEXT_LENGTH=65536 operator-consistency edit executed exactly as planned (§6).
  3. hxs-1's KV coefficient (45,056 B/token) is hxs-1's dense model; CoderX re-measured here per blueprint §4 → §4.2 (20,480 B/token).
Task May Proceed: YES (under O1 — RESUME ARMED)
```

Target identity re-verified at resume (FACT, 07:40:36Z): `hostname` = `hxs-2`; `SSH_CONNECTION` = `192.168.50.204 … 192.168.50.201 22`; `sudo -n` OK; uptime 16 h 30 m continuous.

## 2. F-M6-0 (RECORD, governor-supplement 1): pre-session Xid 31 — event summary and armed watch

- **Event (FACT, retained journal):** 2026-08-26T05:46:59Z, between M4 close and this task, the M4-pinned runner (pid 7546) crashed serving an interactive ~1,048-token plain-text chat (no vision/mmproj activity): `CUDA error: illegal memory access` in `ggml_cuda_mul_mat_q` (`mmq.cu:159`, cuda_v13 build) with kernel **`NVRM: Xid 31`** (PCI:0000:02:00, MMU Fault GPC2, FAULT_PDE VIRT_READ) → core dump → `/api/chat` HTTP 500 after 31.9 s. GPUs were cool, no throttle events, no capacity pressure (17.6 GB of 31.85 GiB).
- **Recovery (FACT):** driver recovered immediately; new runner serving HTTP 200 by 05:47:32; six-plus successful requests followed through 07:12:14. **Zero Xid since** (all-boots kernel count remains exactly 1, re-verified at every stage boundary of this task).
- **Disposition (AUTHORITY):** recorded by the governor as F-M6-0 — single-event ggml-cuda/qwen35moe defect, driver recovered, zero recurrence. The 192.168.50.115 interactive sessions were the **owner himself** (governor supplement 4) — the foreign-client finding class is closed.
- **Armed Xid-watch (this task):** `journalctl -k --since 05:47:00 | grep -c 'NVRM: Xid'` checked at resume baseline and after every mutation/probe — **0 at every checkpoint** (baseline, per-rung ×3, post-repoint, final). Any recurrence would have stopped the run instantly; none occurred.

## 3. Fresh pre-state (mandatory, governor supplement 2) — fresh-vs-original comparison

Captured fresh at resume (07:40:36Z), not from the packet:

| Item | Original (packet/M4) | First drift check 07:25Z | FRESH at resume 07:40Z | Verdict |
| --- | --- | --- | --- | --- |
| `hx2.conf` sha256 / NO_CLOUD | `09184158…68c35b`, carries `OLLAMA_NO_CLOUD=1` | identical | **identical — NO_CLOUD still present** (the concurrent web-search session's removal had NOT landed at any of my read/edit points; per supplement 2 I applied my edit on top of current content and never re-added anything) | match (current) |
| preload script sha256 | `ab1c8010…fe86f9` (MODEL=`hx-qwen3.6-coderx`, DIGEST=`1d297a6a…`) | identical | identical | match |
| preload unit / ollama.service | `bf3cc694…3e11f57` / `11758d46…27dbd3` | identical | identical | match |
| Base tag / bare alias digests | `ca661423d6b5…c1df` / `1d297a6a09…21ba5` | match | match | match |
| Resident state | alias resident Forever (packet) | **empty** (F-M6-0 crash + keep_alive eviction) | `hx-qwen3.6-coderx` loaded on a 5-min keep_alive by concurrent activity (expired 07:44) | explained drift (§2); corrected by this task's own loads |
| Versions / units / listener / swap / OOM | 0.32.15 / active+enabled / `*:11434`+`:22` / 0 B / 0 | match | match | match |
| Kernel Xid all-boots | 0 (M4) | **1 (F-M6-0)** | 1 (same single event; watch armed) | recorded |

## 4. The ladder (FACT) — rung Modelfiles FROM the frozen digest, `num_ctx` the ONLY change

Rung Modelfiles (authored on hxs-5, sha256 verified identical both sides before any create; diffs between rungs = the header comment line + the `num_ctx` line only):

```dockerfile
FROM mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M
PARAMETER num_ctx <32768|65536|131072>
```

| Rung | Modelfile sha256 | Alias | Alias digest |
| --- | --- | --- | --- |
| 32K | `6ea4fecd0fc0633fb8537da20abcf7be3cb4442f3ff9490de33ffc895287128c` | `hx-qwen3.6-coderx-32k` | **`1d297a6a093f7858da9a96e39950b6e7581118708b6121182a811a1f3bf21ba5`** — byte-identical to the M4-frozen bare alias (the baked params already carry `num_ctx 32768`; deterministic rebuild) |
| 64K | `4357327b136c35d7ae324b221e51610a997ce927f166fd2bcbf70ed34f5f0359` | `hx-qwen3.6-coderx-64k` | **`ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1`** |
| 128K | `69b834163e08bfd06ffb37949b74649e2654784a541ab424e9607fda7952a8ad` | `hx-qwen3.6-coderx-128k` | **`86a55171dc03fa282e54eb2ad986d91bd8d278123d888305975ebbdd6cd6049d`** |

`ollama show` per rung (FACT): `num_ctx` 32768/65536/131072; every other baked parameter verbatim (`draft_num_predict 3`, `min_p 0`, `presence_penalty 1.5`, `repeat_penalty 1`, `temperature 1`, `top_k 20`, `top_p 0.95`) — **zero sampling parameters introduced**. Per-rung load procedure: controlled unload (`keep_alive:0`, `/api/ps` polled to empty — F-M6-2 discipline; empty at poll 1 each time) → load the rung's OWN alias (`keep_alive:-1`) → residency proof → probes.

### 4.1 Per-rung results

| Proof | 32K | 64K | 128K |
| --- | --- | --- | --- |
| `/api/ps` resident size (B) | 17,144,322,454 | 17,815,411,094 | 19,157,588,374 |
| Residency | `size_vram == size` — **100% VRAM** | `size_vram == size` — **100% VRAM** | `size_vram == size` — **100% VRAM** |
| `context_length` (effective) | **32768** | **65536** | **131072** |
| `ollama ps` | 100% GPU · 32768 · Forever | 100% GPU · 65536 · Forever | 100% GPU · 131072 · Forever |
| Per-GPU MiB (of 16,311) | 9,734 / 8,336 | 10,182 / 8,976 | 11,080 / 10,258 |
| Aggregate VRAM headroom | ~14.2 GiB | ~13.3 GiB | ~10.9 GiB |
| Needle probe (lines / needle line) | 1193 / 775 | 2388 / 1552 | 4781 / 3108 (65% doc depth each) |
| Needle prompt tokens (% of ctx) | **31,133 (95.01%)** | **62,203 (94.9%)** | **124,421 (94.9%)** |
| Fixture window [LO, HI] | [30474, 32358] | [60948, 64716] | [121896, 129433] |
| `fixture_valid` / `done_reason` / `needle_found` / `pass` | true / **stop** / **true** / **PASS** | true / **stop** / **true** / **PASS** | true / **stop** / **true** / **PASS** |
| Cold prefill tok/s | 2,224.7 | 1,960.9 | 1,580.2 |
| Needle wall (s) | 20.4 | 39.7 | 86.0 |
| Thinking (counts only) | present, 1,626 chars | present, 1,950 chars | present, 1,276 chars |
| Journal: err-level / Xid / OOM | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Xid-watch post-rung | 0 | 0 | 0 |
| **Rung verdict** | **PASS** | **PASS** | **PASS** |

Fixture calibration (disclosed, hxs-1 D-M6-2 class — not a model re-run): 32K attempt 1 at 1,150 lines landed at 30,015 prompt tokens (91.6%, below the window; needle still found with `stop`) — preserved as `needle-32768-a1.json`. Derived density **26.03 tok/line** (CoderX tokenizer ≈ hxs-1's 26.05 on this corpus); the final probes used the computed line counts above and each landed in-window on the first try.

**3 known-answer spot checks — FLAT across rungs (FACT; thinking ON, stripped from evidence, counts only):**

| Question | 32K | 64K | 128K | `done_reason` |
| --- | --- | --- | --- | --- |
| 17 × 23 | `391` | `391` | `391` | stop ×3 |
| Capital of France | `Paris` | `Paris` | `Paris` | stop ×3 |
| `len([1, 2, 3])` | `3` | `3` | `3` | stop ×3 |

### 4.2 KV growth — measured, f16, exactly linear

| Pair | Δ resident size (B) | Δ ctx | B/token |
| --- | ---: | ---: | ---: |
| 32K → 64K | 671,088,640 | 32,768 | **20,480.0** |
| 64K → 128K | 1,342,177,280 | 65,536 | **20,480.0** |

Linearity proof: S(131072) predicted from S(32768) + 20,480 × 98,304 = **19,157,588,374 B — byte-exact** against the measured 128K residency. **CoderX KV coefficient: 20,480 B/token f16** (hybrid-attention MoE; only the full-attention blocks carry KV — under half of hxs-1's dense-model 45,056 B/token). KV type f16 proven two ways (FACT): no `OLLAMA_KV_CACHE_TYPE` set anywhere (envconfig/config.go:317 default f16), and the runner journal prints `llama_kv_cache: … K (f16) … V (f16)` plus `cache_k=f16, cache_v=f16` at load. The 128K f16 residency (19.16 GB) fits with ~10.9 GiB aggregate headroom — the packet's ~5.8 GiB KV estimate was pessimistic (actual KV at 131072 = 20,480 × 131072 = 2.50 GiB).

## 5. Profile freeze — alias digest equality proofs (FACT)

Manifest sha256 == model digest for every tag (content-addressing verified on disk via `sudo -n sha256sum`):

| Tag | Manifest sha256 == digest | Layers vs frozen base |
| --- | --- | --- |
| `mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M` (source, untouched) | `ca661423d6b5…c1df` | — (the frozen reference) |
| `hx-qwen3.6-coderx` (M4 alias, untouched) | `1d297a6a09…21ba5` | IDENTICAL (4/4 frozen blobs) |
| `hx-qwen3.6-coderx-32k` | `1d297a6a09…21ba5` (**byte-identical manifest to the M4 alias**) | IDENTICAL (4/4) |
| `hx-qwen3.6-coderx-64k` | `ec9ebe08a824…28a9f1` | 3/4 frozen blobs + params blob `a8e8cd294c2e…` |
| `hx-qwen3.6-coderx-128k` | `86a55171dc03…6049d` | 3/4 frozen blobs + params blob `a9271230031b…` |

Layer diffs (base vs 64k/128k): exactly one substitution each — the params blob. Params blob contents (verbatim, FACT): base `{"draft_num_predict":3,"min_p":0,"num_ctx":32768,"presence_penalty":1.5,"repeat_penalty":1,"temperature":1,"top_k":20,"top_p":0.95}` — the 64k/128k blobs differ **only** in the `num_ctx` value. `ollama show --modelfile` per alias: FROM the two frozen weight/projector blobs (`ce2f69655c94…`, `8d81165570ee…`), `TEMPLATE {{ .Prompt }}`, `RENDERER/PARSER qwen3.5`, native params only. **The identity guard holds: every rung is content-addressed to the frozen artifact with `num_ctx` as the only changed parameter.**

## 6. Repoint to the -64k operating profile (FACT; D5) — versioned edits

Fresh pre-edit hashes re-captured immediately before editing (07:56Z; both unchanged from §3 — the concurrent session's NO_CLOUD removal had not landed).

### 6.1 `/usr/local/libexec/hx-ollama-preload` — two-line diff

```diff
-MODEL="hx-qwen3.6-coderx"
-DIGEST="1d297a6a093f7858da9a96e39950b6e7581118708b6121182a811a1f3bf21ba5"
+MODEL="hx-qwen3.6-coderx-64k"
+DIGEST="ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1"
```

sha256 `ab1c8010c3a498736b9f8532f7b664faf7afef0255fddc50b4762cff87fe86f9` → **`c95b734592b23c6ce2943ad329e514d4bb7cb5c7d080df58b12fb68c70164710`**. The `/api/ps` name AND digest assertions repoint together (both parameterized). Lint `sh -n` / `bash -n` / `dash -n` PASS on candidate and installed copy. Ownership/mode unchanged: root:root 0755 (`sudo -n install`).

### 6.2 `/etc/systemd/system/ollama.service.d/hx2.conf` — operator-consistency edit (supplement 3)

```diff
-# Native-sampling baseline: NO context or sampling variables are set here —
-# the baked tag parameters (num_ctx 32768, draft_num_predict 3) govern;
-# the M6 ladder owns any context change.
+# M6 (WO-HXS2-JOHN-M6-001): OLLAMA_CONTEXT_LENGTH=65536 is operator-consistency
+# with the hx-qwen3.6-coderx-64k operating profile (D5) — the alias Modelfile
+# PARAMETER num_ctx remains the effective contract (/api/ps context_length is
+# the proof). No sampling variables are set here; the baked tag parameters
+# (draft_num_predict 3, native sampling) govern.
 [Service]
 Environment="OLLAMA_HOST=0.0.0.0"
 Environment="OLLAMA_NO_CLOUD=1"
+Environment="OLLAMA_CONTEXT_LENGTH=65536"
 Environment="OLLAMA_NUM_PARALLEL=1"
 Environment="OLLAMA_MAX_LOADED_MODELS=1"
```

sha256 `0918415897ac871adbff367a9ec381e4da77e0ef294bd0313a95b2498d68c35b` → **`234da7c5c31f69b61fdf37c395fdbe513d6dec19fa647e346173fe4f7d903afa`**. root:root 0644. `daemon-reload` executed; effective `systemctl show ollama -p Environment` now carries `OLLAMA_CONTEXT_LENGTH=65536` (FACT). The pre-existing `OLLAMA_NO_CLOUD=1` line was carried verbatim — neither removed nor re-added (supplement 2); if the concurrent session's owner-authorized removal lands later, it lands cleanly on top.

### 6.3 Untouched

`ollama-preload.service` `bf3cc694…3e11f57` and `ollama.service` `11758d46…27dbd3` — verified unchanged post-deploy.

## 7. Switch + operating-profile residency proof (FACT)

Sequence (hxs-1 M6b §6 pattern, 07:58:57Z → 08:01:47Z): `sudo systemctl restart ollama` → API up at poll 7 (~21 s; F-E2/F-J1 discovery window, one absorbed info-level `curl: (28)` probe retry — F-M6-1 class) → the `Requires=` propagation ran the edited preload inside the unit window (F-M6B-1): `OK - hx-qwen3.6-coderx-64k resident (digest ec9ebe08…)` at 07:59:25 → **manual non-reboot test** `sudo /usr/local/libexec/hx-ollama-preload` → RC=0, OK line, 0.037 s (M4 gate satisfied on the edited script) → `sudo systemctl restart ollama-preload` (F-E4 restart-not-start) → RC=0, `Result=success`.

**Final residency (steady state, 08:05Z; re-proven after two controlled reloads):**

| Proof | Result |
| --- | --- |
| `/api/ps` name / digest | `hx-qwen3.6-coderx-64k:latest` / **`ec9ebe08a824…28a9f1`** (exact rung digest) |
| `context_length` | **65,536** (effective; runner cmdline `-c 65536` and `llama_context: n_ctx = 65536` corroborate) |
| Residency | `size_vram == size == 17,815,411,094 B` (16.59 GiB) — **100% VRAM**, byte-identical to the rung measurement |
| `expires_at` | `2318-12-06T…` — **Forever** (keep_alive=-1) |
| `ollama ps` | `100% GPU` · CONTEXT 65536 · Forever |
| Per-GPU VRAM | GPU0 **10,182** / GPU1 **8,976** MiB of 16,311 each |
| Known-answer re-proof | `391`, thinking ON (882 chars, count only), `done_reason stop` |
| Units | both active+enabled; `NRestarts=0`; preload `Result=success` |
| Listener | `*:11434` + `:22` (ratified posture; unchanged) |
| Swap / uptime | 0 B used; 16 h 53 m continuous (no reboot) |
| Journal (whole M6 window) | **0 error-level lines; 0 Xid; 0 OOM**; Xid-watch final = **0** |
| In-store tags | source tag + bare alias + all three rung aliases present with frozen digests; **only `-64k` resident** |

**Size-report anomaly — investigated and isolated (disclosed):** the single load executed by the `Requires=` propagation *during the service-restart discovery race* reported size 19,994,918,253 B (+2,179,507,159 vs steady state) while still satisfying every acceptance property (100% VRAM, ctx 65536, digest, Forever). Variable-isolation experiment: an identical curl reload and a second preload-unit load (both outside the race) **both reported exactly 17,815,411,094** — the over-reservation is specific to loads planned while GPU discovery is still timing out ("using old values" class). Recorded as finding F-M6-7; the M4 first-ever load (17,602,392,879 vs steady 17,144,322,454 at 32K) is assessed as the same class (INFERENCE, same mechanism). RECOMMENDATION → monitors/KK3: residency *values* asserted during a service-restart window should be re-read from a steady-state load before alarming; the acceptance properties themselves held in all cases.

## 8. Link-speed telemetry under load (FACT)

Sampled every 2 s during each needle prefill (logs: `linkspeed-{32k,64k,128k}.log`):

- **NIC `eno1`:** `Speed: 1000Mb/s`, `Duplex: Full` — constant idle and under load (all serving is local; the LAN carries SSH/API control traffic only).
- **PCIe per GPU:** idle `gen1 x8` → **under prefill load `gen3 x8`**, which equals the driver-reported maximum (`pcie.link.gen.max 3`, `pcie.link.width.max 8`) on both GPUs — the link trains to full speed under load, no width degradation.
- **Under-load telemetry (needle prefills):** SM util 20–39% per GPU; power peaks ~84–93 W per GPU (vs 180 W cap class); no throttle-reason bits beyond idle-class SW power capping; temperatures stayed ≤45 °C.

## 9. Sequential command log (profile §11.3; sanitized)

Session host `hxs-5`, user `hxsa`; remote = SSH askpass wrapper (secret read from its owner-file at execution time only, never on any command line; `sudo -n` only; `StrictHostKeyChecking=yes` against the F-05 pin; `NumberOfPasswordPrompts=1`). Times UTC; failures/corrections kept.

```text
 1 07:15-07:22 exit=0 [local] knowledge review (profile, WO/CP, state log, M4, goal D5, blueprint §4,
    hxs-1 22/29, fixtures sha256sum -c 10/10 OK, TKV docs/envconfig); roster → [KNOWLEDGE REVIEW COMPLETE]
 2 07:22      exit=0 [local] host-key fingerprint == F-05 pin; credential-row shape probes (field count/
    label/length only — value never printed)
 3 07:23      exit=0 [local] mkdir /tmp/esme-m6 (0700); askpass helper + ssh/scp wrappers (0700);
    shape test non-empty only
 4 07:24:44   exit=0 ssh identity: hostname=hxs-2; peer .204→.201; sudo -n OK; uptime 16h14m [ev 00]
 5 07:25-26   exit=0 ssh drift check → TWO anomalies: /api/ps EMPTY (packet said Forever-resident);
    kernel Xid count 1 (M4 said 0) [ev 01]
 6 07:26-30   exit=0 ssh read-only incident investigation: Xid 31 at 05:46:59 (llama-server MMU fault,
    core dump, chat 500); interactive owner sessions .115; recovery 05:47:32; 0 Xid since; GPU health
    clean; coredumpctl empty [ev 01b/01c/01d]
 7 07:31      exit=0 [local] STOP per profile §13 → escalation 08-esme-m6-escalation-xid31.md written;
    helper deleted. [TASK PAUSED — ESCALATION TO KIMI-K3]
 8 07:40      exit=0 [governor] O1 — RESUME ARMED recorded (supplements 1–6)
 9 07:40:36   exit=0 [local] helper+wrappers rebuilt (0700); ssh identity re-verify; FRESH pre-state:
    all 4 config hashes == M4 (hx2.conf still carries NO_CLOUD — removal not landed); Xid-watch
    baseline 0; bare alias loaded on 5-min keep_alive by concurrent activity [ev 10]
10 07:41      exit=0 [local] author Modelfile-32k/64k/128k (FROM frozen tag + num_ctx only); sha256
    6ea4fecd…/4357327b…/69b83416…; rung diffs = comment+num_ctx lines only [ev 11]
11 07:42      exit=0 scp Modelfiles + fixtures (needle_probe.py, fixtures_corpus.py); remote sha256
    5/5 match (fixtures == frozen sha256sums.txt) [ev 12]
12 07:43      exit=0 ssh ollama create hx-qwen3.6-coderx-32k → digest 1d297a6a…21ba5 (== M4-frozen
    bare alias; deterministic); ollama show: num_ctx 32768, baked params verbatim [ev 13]
13 07:44      exit=0 ssh unload bare alias (poll empty, poll 1); load -32k (15.9 s); residency: size==
    size_vram 17,144,322,454, ctx 32768, Forever, 100% GPU, 9,734/8,336 MiB; Xid-watch 0 [ev 14]
14 07:45      exit=1 ssh needle 32K attempt 1 (1150 lines): 30,015 tok (91.6% — below window; needle
    found, stop) — fixture calibration, kept (D-M6-2 class) [ev 15, needle-32768-a1.json]
15 07:46      exit=0 ssh needle 32K final (1193/775): 31,133 tok (95.01%), stop, FALCON-61803 found,
    prefill 2,224.7 tok/s cold, wall 20.4 s [ev 16, needle-32768.json]
16 07:47      exit=0 ssh KA ×3 on -32k: 391/Paris/3, all stop, thinking counts only; journal window
    0 err / 0 Xid / 0 OOM; Xid-watch 0 [ev 17]
17 07:48      exit=0 ssh create -64k → digest ec9ebe08…28a9f1; show verify (65536, native params);
    unload -32k (poll empty); load -64k (14.1 s); residency 17,815,411,094, 65536, Forever, 100% GPU,
    10,182/8,976 MiB; Xid-watch 0 [ev 18]
18 07:49      exit=0 ssh needle 64K (2388/1552): 62,203 tok (94.9%), stop, found, 1,960.9 tok/s,
    wall 39.7 s; link sampler running [ev 19, needle-65536.json]
19 07:50      exit=0 ssh KA ×3 on -64k: flat; journal clean; Xid-watch 0 [ev 20]
20 07:51      exit=0 ssh create -128k → digest 86a55171…6049d; show verify (131072, native params);
    unload/load; residency 19,157,588,374 == linear prediction BYTE-EXACT; 131072, Forever, 100% GPU,
    11,080/10,258 MiB; Xid-watch 0 [ev 21]
21 07:52-53   exit=0 ssh needle 128K (4781/3108): 124,421 tok (94.9%), stop, found, 1,580.2 tok/s,
    wall 86.0 s; link sampler [ev 22, needle-131072.json]
22 07:54      exit=0 ssh KA ×3 on -128k: flat; journal clean; Xid-watch 0; RAM 7.9 Gi, swap 0 B [ev 23]
23 07:55      exit=0 ssh freeze proofs: manifest sha == digest ×5; layer sets (alias/32k IDENTICAL to
    base; 64k/128k = params-blob-only substitution); params blobs verbatim except num_ctx;
    ollama show --modelfile ×3 [ev 24]
24 07:56      exit=0 ssh layer-diff detail; FRESH pre-edit hashes (both unchanged); preload + hx2.conf
    full content captured [ev 25]
25 07:57      exit=0 [local] build repoint candidates; diffs (preload 2 lines; hx2.conf comment+1 env
    line); sh/bash/dash -n PASS; candidate sha c95b7345…/234da7c5… [ev 26]
26 07:58      exit=0 scp candidates; remote hash match; sudo install (0755/0644 root:root); installed
    sha match; sh -n installed PASS; daemon-reload; effective env carries CONTEXT_LENGTH=65536 [ev 26]
27 07:58:57→  exit=0 ssh restart ollama; API up poll 7; Requires= propagation ran edited preload →
   07:59:25        OK - hx-qwen3.6-coderx-64k resident (one absorbed curl(28) probe retry, F-M6-1 class) [ev 27]
28 07:59:27   exit=0 ssh manual non-reboot test of edited preload → RC=0, OK line, 0.037 s (M4 gate) [ev 27]
29 07:59:3x   exit=0 ssh restart ollama-preload (F-E4) → RC=0, Result=success [ev 27]
30 08:00-02   exit=0 ssh size-anomaly isolation: propagation-load size 19,994,918,253 (+2.18 GB);
    controlled curl reload AND second unit load BOTH 17,815,411,094 — race-specific over-reservation
    (F-M6-7); runner cmdline -c 65536; journal KV f16 lines captured [ev 28]
31 08:05      exit=0 ssh FINAL residency proof: -64k ec9ebe08…, 65536, size==size_vram 17,815,411,094,
    Forever, 100% GPU, 10,182/8,976 MiB; KA 391 stop; 5 tags in-store, only -64k resident; units
    active+enabled NRestarts=0; listener unchanged; swap 0 B; uptime continuous; journal 0 err-level
    all window; Xid-watch FINAL 0 [ev 29]
32 08:06      exit=0 scp needle JSONs + linkspeed logs → hxs-5 evidence; executed-fixture hashes
    re-verified == frozen [ev 30]
33 08:07      exit=0 ssh rm -rf /tmp/esme-m6 (remote scratch removed, verified)
34 08:08      exit=0 [local] askpass helper + wrappers + local candidates deleted (verified); sanitized
    evidence retained transiently at hxs-5:/tmp/esme-m6/evidence (volatile /tmp; this report carries the record)
35 08:09-08:12 exit=0 [local] write deliverable 08-esme-m6-ladder-profiles.md
```

## 10. Configuration files (profile §11.2)

| Artifact | Pre sha256 (fresh, 07:40/07:56Z) | Post sha256 | Diff | Owner/mode |
| --- | --- | --- | --- | --- |
| `/usr/local/libexec/hx-ollama-preload` | `ab1c8010…fe86f9` | **`c95b734592b2…164710`** | 2 lines (MODEL, DIGEST), §6.1 | root:root 0755 (unchanged) |
| `/etc/systemd/system/ollama.service.d/hx2.conf` | `09184158…68c35b` | **`234da7c5c31f…903afa`** | comment block + `OLLAMA_CONTEXT_LENGTH=65536`, §6.2 | root:root 0644 (unchanged) |
| `/etc/systemd/system/ollama-preload.service` | `bf3cc694…3e11f57` | `bf3cc694…3e11f57` | — (untouched) | root:root 0644 |
| `/etc/systemd/system/ollama.service` | `11758d46…27dbd3` | `11758d46…27dbd3` | — (untouched) | root:root 0644 |
| Rung Modelfiles (alias sources) | absent | `6ea4fecd…7128c` / `4357327b…f0359` / `69b83416…52a8ad` | new (§4); content inlined | hxsa scratch (removed at cleanup; aliases content-addressed in-store) |
| Model tags | base + bare alias | + `…-32k` / `…-64k` / `…-128k` | §4/§5 | store `ollama:ollama` |

Effective runtime values post-reload: `systemctl show ollama -p Environment` = `OLLAMA_HOST=0.0.0.0 OLLAMA_NO_CLOUD=1 OLLAMA_CONTEXT_LENGTH=65536 OLLAMA_NUM_PARALLEL=1 OLLAMA_MAX_LOADED_MODELS=1`; effective context proven by `/api/ps context_length 65536` (Modelfile contract) plus runner `-c 65536`.

**Rollback (every step reversible):** restore preload (`ab1c8010…fe86f9`, full pre-content captured in evidence 25) and hx2.conf (`09184158…68c35b`, same capture) via `sudo install` + `daemon-reload`; `ollama rm hx-qwen3.6-coderx-32k hx-qwen3.6-coderx-64k hx-qwen3.6-coderx-128k` (tags only — all weight/projector/template blobs shared with the base tag; the 64k/128k params blobs are rung-only and prune safely; base tag and bare alias never touched); then `restart ollama` → poll `/api/ps` empty → `restart ollama-preload`. No reboot required in either direction.

## 11. Findings, risks, decisions surfaced

- **F-M6-0 (RECORD, per governor):** pre-session Xid 31 (§2) — single-event ggml-cuda/qwen35moe defect; driver recovered; zero recurrence; armed Xid-watch ran this task with 0 events. Owner-session class closed (supplement 4). RECOMMENDATION → rick/KK3: track recurrence; a second event on this stack warrants driver/ggml triage (cuda_v13 `mmq` on Blackwell-class GPUs) before any 128K production use.
- **F-M6-7 (FACT, new):** service-restart discovery-race loads can over-report resident size (+2.18 GB observed) with all acceptance properties intact; steady-state loads report the exact rung value (§7 experiment). The M4 first-load delta is the same class (INFERENCE). → monitors: assert residency values only from steady-state loads.
- **F-M6-1/F-M6B-1 classes (carried):** preload auto-runs via `Requires=` during `restart ollama`; one absorbed info-level probe retry this window — expected, do not alert.
- **F-M6-2 discipline (carried):** all unloads polled `/api/ps` to empty (empty at poll 1 every time); no unload race occurred.
- **KV coefficient (FACT):** 20,480 B/token f16, exactly linear (§4.2); >131,072 remains unauthorized and unconfigured (262,144-native extrapolation ≈ +2.7 GB over the 128K residency — INFERENCE only, untested).
- **Needle calibration (disclosed):** 32K attempt-1 undersized (30,015 tok, 91.6%; found+stop) — preserved (`needle-32768-a1.json`); 26.03 tok/line density; no model re-run was used to reach any pass.
- **hx2.conf NO_CLOUD (FACT):** still present at every one of my read/edit points; my edit carried it verbatim without re-adding anything; the concurrent session's owner-authorized removal applies cleanly after me.
- **Budgets:** bounded corrections **0 of 1** used (no failed correctable rung; the needle attempt-1 was my own fixture calibration; the size anomaly was an investigation, not a correction). Stop conditions: **none hit**. 128K needle found — the extended-fail fallback was not needed; three profiles frozen as ordered.

## 12. Validation summary (profile §11.4)

- **What changed:** three rung aliases created FROM the frozen digest with `num_ctx` as the only changed parameter (digests §4, equality proofs §5); preload repointed to `hx-qwen3.6-coderx-64k` (MODEL+DIGEST); `hx2.conf` gained `OLLAMA_CONTEXT_LENGTH=65536` (operator-consistency); the host switched to the 64K operating profile — resident, Forever, proven.
- **What did not change:** frozen artifact `ca661423d6b5…c1df` and bare alias `1d297a6a09…21ba5` (in-store, tags only); Ollama 0.32.15 (binary == server); preload unit + service unit bytes; all other hx2.conf lines (HOST, NO_CLOUD, NUM_PARALLEL=1, MAX_LOADED_MODELS=1); wildcard bind with loopback preserved; no firewall (owner rule); swap 0 B; uptime continuous (no reboot); no model-store deletions; no sampling changes anywhere; no other models; no endpoint changes; rick's entire plane.
- **What was tested:** knowledge review; target identity; fresh pre-state (supplement 2); per rung — create/digest/`ollama show` parameter verification, controlled unload/load, residency (size==size_vram, effective ctx, Forever, per-GPU split, 100% GPU), needle at ~95% with fixture-valid window + stop + found, 3 known-answer spot checks (flat), journal scan, Xid-watch; KV linearity (three-point, byte-exact prediction); alias digest equalities (manifest sha == digest; layer diffs; params blobs); repoint (lint, fresh pre/post hashes, effective env); switch (restart, propagation, manual script test, F-E4 unit restart); final residency re-proof incl. the anomaly-isolation experiment; link-speed telemetry under load.
- **Passed:** every mandatory test at all three rungs — **32K PASS · 64K PASS · 128K PASS** (capacity + needle + quality-spot, all f16). **Failed:** no mandatory test. **Disclosed (none concealed):** 32K needle attempt-1 fixture calibration (§4.1); F-M6-7 size-report anomaly with isolation experiment (§7); carried F-M6-0 (§2).
- **Installed/running:** 0.32.15 binary == server; `ollama.service` active+enabled (`NRestarts=0`); `ollama-preload.service` active+enabled, `Result=success`.
- **Model identity/residency (end state):** operating profile `hx-qwen3.6-coderx-64k:latest` @ `ec9ebe08a824…28a9f1` on the frozen artifact; resident ctx **65536**, **100% VRAM** (`size_vram == size == 17,815,411,094 B`), **Forever**, both GPUs (10,182 + 8,976 MiB). Also in-store (tags only, not loaded): `…-32k` (`1d297a6a09…21ba5`), `…-128k` (`86a55171dc03…6049d`), bare `hx-qwen3.6-coderx` (`1d297a6a09…21ba5`), source tag (`ca661423d6b5…c1df`).
- **Endpoint/security state:** `*:11434` + `:22` (ratified; unchanged); LAN /24 is the boundary; no service-layer auth (ratified); no credentials in any file; helper deleted (verified).
- **Resource/performance state:** 64K resident 16.59 GiB of 31.85 GiB (~13.3 GiB headroom); 128K profile measured at 19.16 GB (~10.9 GiB headroom); cold prefill 2,224.7 / 1,960.9 / 1,580.2 tok/s at 31K/62K/124K; RAM 7.9 Gi used; swap 0 B; zero Xid/OOM all window.
- **Rollback readiness:** §10 — prior files restorable from versioned captures; aliases tags-only removable; no reboot either way.
- **Remaining risks/decisions:** F-M6-0 recurrence watch (rick/KK3); F-M6-7 monitor guidance; NO_CLOUD removal lands independently (supplement 2); Carol catalog receipt (handoff OPEN until cited in the state log).
- **Second Brain evaluation (standing directive, per work order):** (1) opportunity identified — yes; (2) pattern — hxs-1 ladder/profile pattern, second validated use (cross-host uniformity); (3) disposition — **implemented**: the rung evidence and the three aliases are Coder-X's measured catalog context profile at handoff; (4) evidence — ladders are measured, never assumed: CoderX now has its own numbers (20,480 B/token f16; 128K f16 fits with ~10.9 GiB headroom; needle found at 94.9–95.01% on all rungs), materially cheaper at depth than hxs-1's dense model.

**Completion: `PASS — TASK COMPLETE`** (final gate §18: every applicable question answered yes under the O1 resume; all calibrations, the anomaly, and the carried F-M6-0 disclosed; no mandatory-test failure; end state is the D5-ratified 64K operating profile, resident and proven).

```text
Task May Proceed: YES
```

---

Sanitization confirmed: no secrets, tokens, cookies, private prompts, user data, or thinking content in this document; all prompts synthetic; the askpass helper (deleted, verified) read the credential-record row at execution time only and the value was never printed, logged, or stored; remote scratch removed (verified). Evidence trail: transient sanitized captures at `hxs-5:/tmp/esme-m6/evidence/` (00–30 + needle JSONs + linkspeed logs; volatile `/tmp` — this document carries the record); the pre-resume escalation artifact is `08-esme-m6-escalation-xid31.md` (same directory).

Signed: **john / Esme** — Expert Ollama Engineer, session `john-m6-20260826-01`, 2026-08-26T08:12Z (UTC).
