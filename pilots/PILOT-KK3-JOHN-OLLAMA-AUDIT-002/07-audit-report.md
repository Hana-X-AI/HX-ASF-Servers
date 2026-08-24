# 07 — Audit Report: Ollama on hxs-4 (read-only)

| Field | Value |
| --- | --- |
| Session ID | `john-initial-20260824-02` |
| Work order | `WO-OLLAMA-AUDIT-HXS4-001` / goal `GOAL-OLLAMA-AUDIT-HXS4-001` v1 |
| Correction session | `initial` |
| Target | hxs-4 (192.168.50.203), reached via SSH from hxs-5 |
| Live evidence window | 2026-08-24T10:32:57Z – 10:36:55Z (UTC) |
| Mode | Strictly read-only; zero mutations; zero active inference |

## 1. Executive verdict

**The commissioned hxs-4 Ollama runtime is present, healthy, and matches its 2026-08-14
commissioned baseline on every mandatory audit vector executed.** Ollama 0.32.9 is
reconciled across CLI, service binary, and server API. The commissioned model
`qwen3.5:9b-q4_K_M` (digest `6488c96fa5fa…`) is the only pulled model. GPU isolation
by UUID with Vulkan disabled holds exactly as accepted. The endpoint is loopback-only,
consistent with the owner's 2026-08-14 ruling. No model was loaded at audit time;
no errors, Xid events, OOM kills, or crash restarts appear in bounded journals.

- Tests: 29 defined; **28 executed, 28 PASS, 0 FAIL, 0 BLOCKED, 1 NOT RUN** (HW-05, no authorized storage benchmark).
- Unknowns: default-context behavior versus `OLLAMA_CONTEXT_LENGTH=65536` (F2); model residency at audit time (nothing loaded — a state, not a defect); blob-level store permissions (privilege-limited, F7).
- Decisions needed: OmniRoute remote path (open since 2026-08-14, unchanged); 0.32.9-matched source acquisition or deliberate upgrade decision (F1); default-context intent documentation (F2).
- **No host state was changed by this audit.** No recommendation in section 8 was executed.

## 2. Authority and provenance

- Governing documents: `agents/john/profile.md`; delta plan `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-002/plan.md`; base plan `PILOT-KK3-JOHN-OLLAMA-AUDIT-001/plan.md` (matrix §10, guardrails §11).
- Knowledge review: `03-john-knowledge-review-receipt.md`, `Task May Proceed: YES` (authority/baseline ESTABLISHED). Roster check: John is the only current Ollama specialist; craig material is archived history only.
- Baseline authority: `tests/ai-runtime/workloads/qwen35-9b-ollama.json` (COMMISSIONED 2026-08-14); `governance/policy/runtime-acceptance-decisions.md` (local-runtime GRANTED; network-consumable NOT GRANTED); fleet `SERVER-REGISTRY.md` (hxs-4 = 192.168.50.203, Retrieval & AI utility).
- Version identities: installed/live = **0.32.9** (CLI, ExecStart binary, `/api/version` all agree). Corpus source snapshot = **v0.32.11** (commit `39df91c9826b3c0c83677f75cd230d8848d287c3`) — **NOT version-matched**; per profile §2.3/§9 the corpus source was not used to explain runtime behavior. No 0.32.9 source exists in the corpus.
- Historical precedent used as expectation only, never as current truth: hxs-4 commissioning reports (2026-08-14) and discovery (2026-08-12/13).
- Contradictions found: none between live state and baseline. Declared gaps: F1 (source version), F2 (default-context semantics), F7 (privilege-limited sub-probe).

## 3. Host/runtime snapshot (live, 2026-08-24T10:33Z)

- Identity: hostname `hxs-4`; 192.168.50.203/24 on `eno1`; machine-id `a3244b92…1889` matches discovery; peer verified from hxs-5 (192.168.50.204). [001]
- OS: Ubuntu 24.04.4 LTS, kernel 7.0.0-28-generic x86_64; uptime 6 d 11 h 46 m (boot 2026-08-17 22:47 UTC); load 0.00. [001, 002]
- CPU/NUMA: i7-14700F, 1 socket, 20 cores, 28 threads; 1 NUMA node. [002]
- Memory: 31 GiB RAM (1.5 GiB used, 29 GiB available); 8 GiB swap file, 0 used. [002]
- GPU: RTX 5060 Ti 16311 MiB (`GPU-11b1a30e-…`, 0000:01:00.0) + RTX 5060 8151 MiB (`GPU-cc758e31-…`, 0000:07:00.0); driver 580.173.02, CUDA 13.0; both idle, 0 MiB used, no compute processes; temps 35/37 °C. [006]
- Storage: root ext4 930.5 G on WD SN3000 NVMe, 3% used, 847 G free; ADATA 476.9 G NVMe unallocated (as discovered). [002, 008]
- Service: `ollama.service` active (running) since 2026-08-23 11:46:10 UTC, enabled; MainPID 349591 `/usr/local/bin/ollama serve`; User/Group `ollama` (uid 999/gid 988, groups ollama,video,render); fragment `/etc/systemd/system/ollama.service` + drop-in `hx-commissioning.conf`. [003]
- Effective environment (sanitized; no secrets present): `CUDA_VISIBLE_DEVICES=GPU-cc758e31-d23b-3c53-bee6-dae3299a6f11`, `GGML_VK_VISIBLE_DEVICES=999`, `OLLAMA_VULKAN=0`, `OLLAMA_CONTEXT_LENGTH=65536`, `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_NO_CLOUD=1`; unset: FlashAttention, KV cache type, keep-alive (default 5m0s), debug log requests (false), `OLLAMA_HOST` (default `http://127.0.0.1:11434` per server startup log). [003, 007]
- Listener: TCP `127.0.0.1:11434` only; no LAN/IPv6 bind; no proxy services present. [004, 009]
- Models: pulled = `qwen3.5:9b-q4_K_M` only; loaded = none at audit time. [005]

## 4. Audit test matrix

Evidence files are in `06-raw-evidence-sanitized/`. Commands and exits in `05-command-log.md`.

| Test ID | Property | Expected | Actual | Status | Evidence | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| ID-01 | Target/time | hxs-4 + 192.168.50.203 | both match; peer 192.168.50.204→203 | PASS | 001 | — |
| ID-02 | OS/kernel | Ubuntu 24.04, x86_64 | 24.04.4, 7.0.0-28-generic | PASS | 002 | — |
| ID-03 | Resources | ~31 GiB, swap, NVMe root | 31 GiB/8 GiB swap.img; 3% disk | PASS | 002 | — |
| ID-04 | Ollama identities | 0.32.9 ×3; source declared | CLI 0.32.9; ExecStart same binary; API 0.32.9; corpus v0.32.11 declared NOT matched | PASS | 003, 005 | source-level behavior analysis out of reach (F1) |
| HW-01 | CPU | i7-14700F 20c/28t | match | PASS | 002 | — |
| HW-02 | NUMA | 1 node | 1 node (numactl present) | PASS | 002 | — |
| HW-03 | RAM/swap | ~32 GB | 32,639,044 kB; 8 GiB swap | PASS | 002 | — |
| HW-04 | Model storage | store on root NVMe ext4 | `OLLAMA_MODELS=/usr/share/ollama/.ollama/models`; only `/` + `/boot/efi` mounts → store on nvme0n1p2 ext4 | PASS | 007, 008 | `findmnt -T`/`df` on the store path permission-denied; placement by mount table + server config (labeled inference) |
| HW-05 | Storage perf | none authorized | — | NOT RUN | — | no fio/writes permitted; no authoritative benchmark exists → `NOT ESTABLISHED` |
| GPU-01 | Inventory/driver | 2 GPUs, 580.173.02/CUDA 13.0 | exact match incl. UUIDs | PASS | 006 | — |
| GPU-02 | Topology/procs | recorded; runner only on RTX 5060 | PHB/PHB; no compute processes at audit time | PASS | 006 | nothing loaded at audit time |
| GPU-03 | Driver health | no fresh Xid/NVRM/OOM | none; benign module lines only (boot 2026-08-17; 39-bit DMA note 2026-08-23) | PASS | 007 | bounded window (journal since 2026-08-17) |
| GPU-04 | Isolation | UUID + VULKAN=0 + GGML_VK=999 | all three present, expected values | PASS | 003, 007 | — |
| SVC-01 | Unit/state | active/enabled | active since 2026-08-23 11:46:10, enabled | PASS | 003 | — |
| SVC-02 | Wiring | ollama user; isolation env | as expected; see §3 | PASS | 003 | — |
| SVC-03 | Listener | loopback only | 127.0.0.1:11434 only | PASS | 004 | `-p` without root: owner via MainPID instead |
| SVC-04 | Tuning | values or NOT SET | CONTEXT_LENGTH=65536; NUM_PARALLEL=1; MAX_LOADED_MODELS=1; NO_CLOUD=1; FlashAttention/KV-cache NOT SET (consistent with 2026-08-14 revert); ORIGINS default; MAX_QUEUE=512 (default) | PASS | 003, 007 | — |
| SVC-05 | Service health | no fresh errors | no crash/OOM; clean external restart 2026-08-23 11:46:10; one warmup `cudaMalloc failed` with recovery (F3) | PASS | 007 | request content not logged (DEBUG_LOG_REQUESTS=false) — by design |
| API-01 | Server | 0.32.9 | HTTP 200 `{"version":"0.32.9"}`, 1.7 ms | PASS | 005 | — |
| API-02 | Pulled inventory | qwen3.5:9b-q4_K_M digest 6488c96fa5fa | exactly one model; digest `6488c96fa5faab64…9ea7`; modified 2026-08-14 | PASS | 005 | — |
| API-03 | Loaded inventory | state capture | empty; `ollama ps` empty | PASS | 005 | model not resident at audit time |
| MOD-01 | Identity/quant | Q4_K_M, 9.7B, ~6.6 GB | Q4_K_M, 9.7B, gguf, ctx 262144, emb 4096, caps [vision, completion, tools, thinking]; size 6,594,474,711 B | PASS | 005 | 475-byte delta vs baseline's remote OCI-layer size (6,594,474,236 B) — different measurement basis; digest identical (F5) |
| MOD-02 | Context alignment | ≤65536 accepted envelope | configured `OLLAMA_CONTEXT_LENGTH=65536`; server logged `vram-based default … default_num_ctx=4096`; 2026-08-23 runner loaded n_ctx=4096 | PASS | 003, 007 | default-vs-configured semantics unresolved without 0.32.9 source (F2) |
| MOD-03 | Residency | direct evidence only | not loaded at audit time → residency NOT ESTABLISHED now; 2026-08-23 journal shows runner discovered only `GPU-cc758e31…` (RTX 5060, 0000:07:00.0) and loaded there | PASS | 005, 006, 007 | read-only audit cannot load a model; current residency unproven by design |
| SEC-01 | Exposure | loopback per owner ruling | loopback only; `OLLAMA_HOST` default loopback | PASS | 004, 007 | — |
| SEC-02 | Proxy/auth boundary | NOT ESTABLISHED expected | no nginx/haproxy/caddy/omniroute configs or services on hxs-4 | PASS | 009 | remote path remains an open owner decision (D1), not a violation |
| SEC-03 | Permissions | store owned by service user | `/usr/share/ollama` `drwxr-x--- ollama:ollama`; uid 999 | PASS | 008 | deeper stat/ls permission-denied without privilege (F7) |
| SEC-04 | Secret hygiene | no secrets retained | env/unit/journals contain no secret values; evidence scan clean; credential never logged | PASS | all | — |
| PERF-01 | Passive posture | no regression indicators | GPUs idle 0 MiB; no queue/OOM/fallback in journals; 2026-08-23 chat served at n_ctx 4096 (≈21 tok/s eval, truncated=0) | PASS | 006, 007 | no new measurement authorized; throughput figures are journal-observed single-run, not a benchmark |

## 5. Gap analysis

| Finding | Component | Observed | Controlling target | Gap | Severity | Impact | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Versioning | live 0.32.9; corpus source v0.32.11 | version-matched source rule (profile §2.3) | no 0.32.9 source in corpus | Low | source-level behavior analysis unavailable; upgrade/rollback reasoning must be empirical | 003, 005, receipt 03 | High |
| F2 | Context config | `OLLAMA_CONTEXT_LENGTH=65536` set; server default `num_ctx=4096` observed | acceptance envelope ≤65536 | effective default (4096) differs from configured value; semantics unresolved without matched source | Medium | clients expecting 65536 without setting `num_ctx` get 4096; silently protective for residency but surprising | 003, 007 | High (observed), Low (explanation) |
| F3 | VRAM headroom | 2026-08-23 load: `cudaMalloc failed` for 4657.81 MiB compute buffer during vision warmup, then recovery and normal service | 8 GB card; baseline incident hxs4-wedge-001 | tight VRAM at load with multimodal warmup | Low-Medium | potential OOM/wedge risk if load conditions worsen (larger ctx + vision + parallel) | 007 | Medium |
| F4 | Service lifecycle | clean stop/start 2026-08-23 11:46:10 after an interactive `/api/chat` test | audit expects no unexplained restarts | none — externally explained, clean | Informational | none; crash excluded | 003, 007 | High |
| F5 | Model size basis | local size 6,594,474,711 B vs baseline remote layer 6,594,474,236 B | digest identity is the control | measurement bases differ; digest matches | Informational | none | 005 | High |
| F6 | Registry target vs as-built | registry lists Qdrant/Qwen2.5-3B/BGE-M3/reranker for hxs-4; Ollama has only qwen3.5:9b | registry is TARGET-STATE | as-built matches commissioning (others not installed) | Informational | capacity note stands: 8 GB card cannot co-host more models at accepted residency | 005, receipt 03 | High |
| F7 | Store permission depth | deeper `stat`/`ls` denied (750 ollama:ollama) | SEC-03 full-depth ideal | blob-level modes unverified | Low | residual permission risk unexamined below top level | 008 | High |
| F8 | CORS defaults | `OLLAMA_ORIGINS` default includes `0.0.0.0` entries | loopback-only listener | none exploitable today | Informational | would matter only if bind is ever widened | 007 | High |
| F9 | Storage | 476.9 GB NVMe still unallocated | discovery record | none | Informational | future model-store headroom option | 008 | High |

## 6. Model/hardware alignment

- `qwen3.5:9b-q4_K_M` (digest `6488c96fa5fa…`, Q4_K_M, 9.7B, gguf) on the isolated RTX 5060 (8151 MiB, compute 12.0) matches the commissioned and accepted pairing; the RTX 5060 Ti remains reserved and invisible to Ollama (env + journal discovery both confirm). [003, 006, 007]
- Baseline (2026-08-14 measurement): 100% GPU residency to ctx 16384 (6,794 MiB); CPU/GPU split at 32768/65536; ~28 tok/s real generation at 65536; silent truncation beyond 65536 (iss-015) — acceptance conditions (bound prompts <65536, thinking disabled) remain the controlling client contract.
- At audit time nothing is loaded (`/api/ps` empty, 0 MiB both GPUs). The only post-commissioning load in journals (2026-08-23) ran at n_ctx 4096 on the correct GPU and served normally after one recoverable warmup allocation failure (F3).
- Alignment verdict: **as commissioned; no drift detected.** Load-time VRAM tightness on the 8 GB card (F3) is the one watch item.

## 7. Network/security assessment

- Listener: `127.0.0.1:11434` only (ss + server startup log). Compliant with the 2026-08-14 owner ruling: direct network consumption refused; remote use only via OmniRoute, whose mechanism is still undefined (open decision D1, not a breach).
- Proxy/auth boundary: none on hxs-4 (no nginx/haproxy/caddy/omniroute configs or running services) — consistent with `accepted-network-consumable` NOT GRANTED.
- Service identity: dedicated `ollama` user (uid 999), groups ollama/video/render; model store top level `drwxr-x--- ollama:ollama` — not readable by other users (verified by denial). Depth unverified (F7).
- Secret hygiene: unit/drop-in contain only non-secret env; server env map shows empty proxy vars; `OLLAMA_DEBUG_LOG_REQUESTS=false` (request bodies not logged); evidence scan found no secrets; the SSH credential was handled via askpass and never stored.
- Residual: IPv6 has no 11434 bind; SSH 0.0.0.0:22 as discovered (out of Ollama scope).

## 8. Recommendation-only remediation plan

**RECOMMENDATION ONLY — NOT AUTHORIZED FOR EXECUTION.** Nothing below was executed. Any command shown is illustrative for a future authorized session.

| ID | Finding | Proposed change | Benefit | Risk | Prerequisite/authority | Validation | Rollback concept | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | all | Keep current configuration (loopback, UUID isolation + Vulkan off, NUM_PARALLEL=1, MAX_LOADED_MODELS=1) | preserves accepted, measured state | none | none | this audit's evidence | n/a | — |
| R2 | F2 | Document the default-context contract: clients must set `num_ctx` explicitly (observed default 4096); reconcile `OLLAMA_CONTEXT_LENGTH` semantics against 0.32.9-matched source before any tuning | removes silent surprise | change without source-grounding could alter memory envelope | R3 source acquisition; owner sign-off on doc | version-matched source read + authorized load test at explicit num_ctx | revert doc/env to current values | Medium |
| R3 | F1 | Acquire Ollama 0.32.9 source snapshot into the corpus, or approve a deliberate upgrade to a current release as a separate authorized task with installer authentication and rollback to 0.32.9 | restores source-grounded analysis; security currency | upgrade without acceptance re-measurement breaks the baseline | Agent Zero decision; install authority (profile §7.1) | pinned-upgrade test suite per profile §7.1 | exact 0.32.9 reinstall + unit/drop-in restore | Medium |
| R4 | F3 | Watch item: keep the unload-before-`num_ctx`-change rule (hxs4-wedge-001); in a future authorized session, measure load behavior with vision warmup at larger `num_ctx` on the 8 GB card | quantify F3 before it wedges | active testing requires authorization; OOM can wedge driver | separate benchmark pilot authorization | predefined load matrix with unload between rungs | stop test; service restart if wedged | Medium |
| R5 | D1 | Remote consumption path: keep loopback until the OmniRoute mechanism is defined and measured (acceptance ruling) | security boundary intact | premature exposure publishes an unauthenticated endpoint | owner decision | measured access path per acceptance contract | return to loopback | High (as standing constraint) |
| R6 | F7 | Authorize a one-off privileged read-only permission audit of the model store (`sudo stat/ls` depth) | closes SEC-03 depth gap | minimal | Kimi-K3/Agent Zero authorization | compare against least-privilege expectation | n/a (read-only) | Low |

## 9. Remaining gaps and decisions

- Blockers: none. All mandatory tests executed except HW-05 (NOT RUN by design).
- Agent Zero decisions: D1 OmniRoute remote mechanism (open since 2026-08-14); D2 source acquisition vs upgrade (R3); any future exposure change (R5).
- Future validation: F3 load-behavior measurement (R4); F2 source-grounding (R2/R3); F7 privileged permission audit (R6); active benchmarking remains a separate pilot.
- Deferred: registry TARGET-STATE workloads for hxs-4 (Qdrant, embeddings, reranker) remain uninstalled — capacity constraint recorded in commissioning.
- Observations only: F4, F5, F8, F9.

## 10. Validation summary

See `08-john-validation-summary.md`. Completion state: `PASS — AUDIT EVIDENCE PACKAGE COMPLETE`.
