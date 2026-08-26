# 08 — Esme (john): M6 PAUSED AT DRIFT CHECK — Xid 31 runner crash on hxs-2 (escalation to Kimi-K3)

`[TASK PAUSED — ESCALATION TO KIMI-K3]`

| Field | Value |
| --- | --- |
| Report ID | ESME-HXS2-M6-ESC-XID31-001 |
| Task ID | WO-HXS2-JOHN-M6-001 (`PILOT-HXS2-CODERX-BACKEND-001`, milestone M6+M6b) |
| Agent | john / Esme, session `john-m6-20260826-01` |
| Target host | `hxs-2` (192.168.50.201), Ubuntu 24.04.4, kernel 7.0.0-30, driver 580.173.02, Ollama 0.32.15 |
| Executed from | `hxs-5` (192.168.50.204) via SSH `hxsa@192.168.50.201` — askpass helper read the credential-record row at execution time only; no extracted copy; host key pinned (F-05) and verified pre-flight |
| Window (UTC) | 2026-08-26T07:15Z → 07:31Z — **read-only throughout; zero target mutations** |
| Target mutations | **NONE** — no creates, no edits, no restarts, no loads/unloads, no installs |
| Escalation trigger | Pre-session **NVRM Xid 31** (MMU fault) with llama-server core dump at 05:46:59Z; context-packet resident state contradicted (nothing resident); profile §13 |

Evidence labels: FACT (live host output) / AUTHORITY / INFERENCE / RECORD.
Sanitization confirmed: no secret value was printed, logged, or stored anywhere; GIN journal lines carry no request bodies; all evidence below is operational.

---

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path /opt/tkv-local/ollama resolves locally here); target hxs-2 (192.168.50.201)
Source: /opt/tkv-local/ollama + HX-ASF-Servers controlling docs
Reviewed At: 2026-08-26T07:15Z → 07:22Z
Relevant Files: 10 reviewed —
  agents/john/profile.md; agents/ roster = carol, john, kimi-k3, rick (all current)
  pilots/PILOT-HXS2-CODERX-BACKEND-001/01-state-log.md (rows 1–13: D1–D8, M4 closed, owner order row 13)
  pilots/PILOT-HXS2-CODERX-BACKEND-001/07-esme-m4-install.md (hxs-2 identity; frozen config hashes; alias binding)
  goals/2026-08-26-hxs2-qwen36-coderx-backend.md (D5: operating ctx 65,536; ladder 32K→64K on the exact digest before freeze)
  servers/BLUEPRINT-llm-server.md §4 (context plane: ladder on the exact digest; KV measured per model; /api/ps context_length is the proof)
  pilots/PILOT-HX1-OLLAMA-QWEN27B-001/22-esme-m6-capacity-ladder.md + 29-esme-m6b-profiles.md (hxs-1 rung procedure,
    digest equality, repoint pattern, F-M6-2 unload discipline, F-E4 preload restart-not-start)
  fixtures/ (needle_probe.py alias-parameterized; fixtures_corpus.py; sha256sums.txt — all 10 verified OK locally 07:21Z)
  /opt/tkv-local/ollama: docs/modelfile.mdx:57,149 (PARAMETER num_ctx); docs/context-length.mdx (VRAM-based defaults);
    docs/faq.mdx:354 + envconfig/config.go:222,230,317,336 (OLLAMA_KV_CACHE_TYPE default f16; OLLAMA_CONTEXT_LENGTH env)
Authority/Version Identified: Ollama 0.32.15 pinned (binary == server, M4); frozen artifact ca661423d6b5…c1df. TKV source
  snapshot (v0.32.11) predates the installed 0.32.15 for the qwen35moe family (carried gap from M4 F-E7-class): empirical
  API evidence on the actual host is the authority for model-specific behavior; snapshot cited only where version-independent.
Applicable Tests/Runbooks: WO-HXS2-JOHN-M6-001 rung procedure; hxs-1 22/29 pattern; F-M6-2 poll-to-empty unload; F-E4 restart-not-start.
Contradictions or Gaps:
  1. TKV snapshot predates installed 0.32.15 (carried from M4; disposition unchanged).
  2. Work order says "hx1.conf"; hxs-2's equivalent drop-in is hx2.conf (4 env values, no OLLAMA_CONTEXT_LENGTH). Planned
     interpretation (not executed): preload MODEL+DIGEST repoint to -64k plus hxs-1-pattern operator-consistency edit on
     hx2.conf. Flagged for Kimi-K3 confirmation at resume.
  3. hxs-1's KV coefficient (45,056 B/token) is hxs-1's dense model; CoderX (hybrid-attention MoE) must be re-measured
     per blueprint §4 — the ladder was to do this.
Task May Proceed: NO — paused at drift check (§2); escalation below.
```

Target identity verified before any action (FACT, 07:24:44Z): `hostname` = `hxs-2`; `SSH_CONNECTION` = `192.168.50.204 … 192.168.50.201 22`; `sudo -n` OK; uptime 16 h 14 m continuous (no reboot). Host key: known_hosts ED25519 fingerprint `SHA256:b2qlMQz496nUbuZKJu3wwmR0QY/EmN0KQtW4rM2HDcQ` == rick M1 F-05 pin (verified 07:22Z, `StrictHostKeyChecking=yes` on every connection).

## 2. Drift check (FACT, 07:25–07:26Z) — the stop trigger

| Item | Frozen value (M4 / context packet) | Observed 07:25Z | Verdict |
| --- | --- | --- | --- |
| `ollama --version` / `/api/version` | 0.32.15 / 0.32.15 | 0.32.15 / 0.32.15 | match |
| Base tag digest | `ca661423d6b5…c1df` | `ca661423d6b5…c1df` (16,956,334,345 B) | match |
| Alias `hx-qwen3.6-coderx` digest | `1d297a6a09…21ba5` | `1d297a6a09…21ba5` (16,956,334,009 B) | match |
| **Resident model** | alias resident, `size_vram == size == 17,602,392,879`, ctx 32768, **Forever** | **`/api/ps` EMPTY; both GPUs 0 MiB** | **DRIFT — explained by §3** |
| preload script sha256 | `ab1c8010…fe86f9` | `ab1c8010…fe86f9` | match (untouched) |
| hx2.conf sha256 | `09184158…68c35b` | `09184158…68c35b` | match (untouched) |
| preload unit sha256 | `bf3cc694…3e11f57` | `bf3cc694…3e11f57` | match (untouched) |
| ollama.service sha256 | `11758d46…27dbd3` | `11758d46…27dbd3` | match (untouched) |
| Units | both active+enabled | both active+enabled; `NRestarts=0`; up since 04:44:34Z | match |
| Environment | 4 mandated values | `OLLAMA_HOST=0.0.0.0 NO_CLOUD=1 NUM_PARALLEL=1 MAX_LOADED_MODELS=1` | match |
| Listener | `*:11434` + `:22` | `*:11434` + `:22` | match (no endpoint change) |
| Swap / disk | 0 B used / 3.4 T free | 0 B used / 3.4 T free (1%) | match |
| **Kernel Xid, all boots** | **0 (rick M1 ×8 boots; M4 re-verified)** | **1 — `Xid 31` at 05:46:59Z (this boot)** | **DRIFT — the escalation** |
| Kernel OOM | 0 | 0 | match |

## 3. The incident (FACT, from the retained journal; this boot, uptime continuous)

Timeline (UTC, 2026-08-26):

- **04:47:09** M4 preload pinned `hx-qwen3.6-coderx` Forever (runner pid 7546; GPUs 9,940 + 8,772 MiB).
- **05:04** governor live-verified residency (state log row 9).
- **05:43:54 → 05:45:49** interactive client on 127.0.0.1 browses `HEAD /`, `/api/tags`, `/api/status`, `/api/experimental/model-recommendations`, `/api/show` ×5, `/api/generate` (1.8 ms), `/api/ps` — the request signature of a desktop/web UI driven over the interactive SSH session from **192.168.50.115** (`last`: hxsa pts/0 04:06:57→06:17:58; two later sessions 06:21→06:35, 06:54→07:14). Same foreign-local-client class as hxs-1 F-M6-3; here LAN-bind is ratified and loopback is a boundary, not authentication.
- **05:46:28** `POST /api/chat` task 0 launches: `new prompt, n_ctx_slot = 32768, n_keep = 4, task.n_tokens = 1048` (a ~1K-token text prompt; **zero** clip/mmproj/image/vision log lines in the window — not a vision request). Sampler chain shows the frozen baked parameters verbatim (presence_penalty 1.5, temp 1, top_k 20, top_p 0.95).
- **05:46:59** prompt processing logged only **24 tokens in 30.78 s (0.78 tok/s — pathologically slow)**, then `created context checkpoint 1 of 32`, then:
  - `ggml-cuda.cu:106: CUDA error: an illegal memory access was encountered` — `current device: 0, in function ggml_cuda_mul_mat_q … mmq.cu:159`;
  - kernel: **`NVRM: Xid (PCI:0000:02:00): 31, pid=7546, name=llama-server, channel 0x00000003 … MMU Fault: ENGINE GRAPHICS GPC2 GPCCLIENT_T1_4 faulted @ 0x4_03200000. FAULT_PDE ACCESS_TYPE_VIRT_READ`**;
  - `llama-server terminated … signal: aborted (core dumped)`; the chat request returns **HTTP 500 after 31.9 s**.
- **05:47:03–05:47:08** GPU-discovery watchdog timeouts (F-J1/F-E2 class, amplified during driver recovery post-fault).
- **05:47:18** new runner listening; **05:47:32 and 05:47:57 `/api/chat` 200** — stack recovered and serving within ~40 s.
- **06:23 → 07:12** continued interactive serving, all 200: `/api/generate` 06:23:31 (11.8 s, model reload), chats 06:27:20, 06:27:27, 06:54:44, 06:58:03, 06:58:04, 07:00:26, **07:12:14 (16.7 s)** — six-plus successful post-crash requests.
- **~07:17:17** runner evicted at default keep_alive (~5 min idle; the Forever pin died with crashed pid 7546). Teardown produced the known NVRM `pIOVAS`/`mem_desc` assertion class (hxs-1 F-E3/F-M5B-2 — not an Xid).
- **07:25:34** my own drift-check probes (2× `/api/version`, `/api/tags`, 2× `/api/ps`, `HEAD /`).
- **Xid count since 05:47:00: 0.** `coredumpctl list`: no entries (no persistent core retained).

## 4. GPU/driver health now (FACT, 07:29Z)

- GPU0 40 °C / 26.8 W, GPU1 38 °C / 16.7 W; both 0 MiB used; throttle-reason masks `0x0` / `0x4` (idle class only); SW-power-cap counter 173,570 µs (idle-capping artifact; zero HW/thermal/brake events).
- ECC: N/A (consumer); retired-pages pending: N/A; channel/TPC repair pending: No.
- Reading (INFERENCE): not thermal, not power, not capacity (17.6 GB resident of 31.85 GiB; prompt only 1,048 tokens of 32,768). The fault fired inside `ggml_cuda_mul_mat_q` (quantized matmul kernel, cuda_v13 build) on device 0 during early decode-graph compute on the qwen35moe hybrid MoE — consistent with a **llama.cpp/ggml CUDA defect class on this architecture/driver**, not a hardware-degradation signature. Single occurrence; driver recovered; no recurrence across the subsequent serving window.

## 5. Why this stops the task (AUTHORITY)

- Work order stop conditions: "OOM, unapproved CPU fallback, **any Xid**" — scoped to the ladder, but a pre-session unexplained Xid on the exact stack the ladder must stress materially changes the risk of the required per-rung "no Xid" proofs.
- Profile §13: immediate stop on "unexpected system state", "evidence of potential GPU/driver instability", and "inconsistency between remote knowledge and live state" — all three are present (packet says resident Forever; nothing is resident; an Xid exists where the frozen record says zero).
- Escalating is not optional under the profile; resuming requires recorded Kimi-K3 direction.

## 6. System state (preserved, untouched by this session)

- Ollama service: active+enabled since 04:44:34Z, `NRestarts=0`, 0.32.15 binary == server.
- Model/load state: base tag + alias in-store with frozen digests (§2); **nothing loaded**; preload unit has not run since 04:47:09Z (its pin died with the crashed runner; nothing re-pinned — correct behavior).
- GPU/CPU state: idle, healthy telemetry (§4); Xid all-boots count = 1 (05:46:59Z, §3).
- Network/listener: `*:11434` + `:22` (ratified posture; unchanged).
- Files changed by this session: **none on hxs-2**. On hxs-5: volatile `/tmp/esme-m6/` (helper, wrappers, sanitized evidence captures 00/01/01b/01c/01d) — helper and wrappers deleted at session end per contract.
- Last successful test: drift-check probes 07:25:34Z (all 200).
- Failed or unexecuted tests: the entire M6 ladder (rungs 32K/64K/128K), alias freeze, repoint, and re-proof — **NOT STARTED**.

## 7. Risk of proceeding without direction

The ladder's 128K deep-prefill (~124K-token ingest) is the heaviest ggml CUDA workload this stack has faced. If the 05:46 fault class recurs under it, the run would fail mid-proof (armed stop conditions catch it), but an un-briefed recurrence could also be misread as a capacity result. Proceeding silently would additionally conceal from the owner that their interactive session crashed the serving runner — a fact the factory needs regardless of the ladder (driver/ggml defect triage, and the F-M6-3-class "any local/LAN client can drive the API" posture).

## 8. Rollback state

Nothing to roll back: zero mutations this session. The M6 rollback plan in the work order stands unexecuted. End-state recovery of residency (the repointed preload) is itself part of the paused work; if Kimi-K3 directs an immediate re-pin before a full resume decision, the one-command path is `sudo systemctl restart ollama-preload` (existing MODEL/DIGEST still frozen-correct) — not executed, awaiting direction.

## 9. Decision or direction required

1. **Proceed or hold the M6 ladder.** Options:
   - **O1 (recommended):** authorize the ladder to proceed as ordered with stop conditions armed; record the 05:46 Xid as finding F-M6-0 (rick's plane: driver 580.173.02 + cuda_v13 ggml `mmq` on qwen35moe/Blackwell-class GB206; possible repro work order), plus the foreign-client observation (F-M6-3 class). Any in-ladder Xid/OOM/CPU-fallback stops the rung immediately per the work order; a recurring crash signature converts the ladder result to extended-fail reporting.
   - **O2:** hold the ladder; rick investigates GPU/driver first (driver known-issue sweep, `cuda_v13` vs `cuda_v12` runtime, mmq/Blackwell reports; possibly evaluate 0.33.0 in a separate work order).
   - **O3:** proceed reduced (32K+64K only). Not recommended — the armed stop conditions already provide this protection honestly, and 128K evidence is exactly what D5/M6b need.
2. **Confirm the "hx1.conf" interpretation** (§1 gap 2): preload MODEL+DIGEST repoint to `hx-qwen3.6-coderx-64k` + operator-consistency `OLLAMA_CONTEXT_LENGTH=65536` added to **hx2.conf** (the hx1.conf-equivalent drop-in), Modelfile remaining the effective contract.
3. **Awareness:** the 05:43–07:12 interactive use of CoderX from 192.168.50.115 (incl. the crashed request) — if that was the owner, this report corroborates their observed 500; if not, it is a foreign-client finding for the governor.

## 10. Evidence paths

- Pilot artifact: this file.
- Sanitized session evidence (volatile): `hxs-5:/tmp/esme-m6/evidence/` — `00-identity.txt`, `01-drift-check.txt`, `01b-anomaly-investigation.txt`, `01c-xid-evidence.txt`, `01d-gpu-health.txt` (full journal excerpts, GIN timeline, GPU telemetry; volatile `/tmp` — this document carries the record).
- Primary source on target (untouched): `journalctl -u ollama --since "2026-08-26 05:30:00"` and `journalctl -k | grep 'NVRM: Xid'` on hxs-2.

Awaiting direction. On a recorded O1 (or O2/O3) decision I can resume immediately: the session plan, fixture set (verified against `sha256sums.txt`), rung procedure, and freeze/repoint sequence are staged from the completed knowledge review.

Signed: **john / Esme** — Expert Ollama Engineer, session `john-m6-20260826-01`, 2026-08-26T07:31Z (UTC).
