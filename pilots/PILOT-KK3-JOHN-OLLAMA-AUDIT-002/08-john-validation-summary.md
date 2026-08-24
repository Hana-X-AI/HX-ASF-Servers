# 08 — John Validation Summary

| Field | Value |
| --- | --- |
| Session ID | `john-initial-20260824-02` |
| Work order | `WO-OLLAMA-AUDIT-HXS4-001` |
| Context hash | `bf55893b954c2527dcfe714d2e77d503c10b22c04b7b0142daddc88a9a8eeb77` |
| Correction session | `initial` |
| Target | hxs-4 (192.168.50.203) — identity verified (hostname + eno1 address + machine-id match discovery) |
| Live evidence window | 2026-08-24T10:32:57Z – 10:36:55Z UTC |

## What changed

Nothing on the target. Zero mutations: no systemctl state changes, no process signals,
no Ollama model operations, no writes to any state, no active inference. The only local
artifacts created are this evidence package; the askpass helper was deleted.

## What did not change

Host identity, OS, service state, unit files, environment, model inventory, GPU state,
listener set, and journal contents on hxs-4 are exactly as found (all probes read-only;
command log `05-command-log.md` rows 3–11).

## What was tested

29 tests across ID, HW, GPU, SVC, API, MOD, SEC, PERF groups per `04-audit-test-plan.md`
(base plan §10 matrix, full matrix applied — Ollama present).

- Executed: 28 — **Passed: 28** — Failed: 0 — Blocked: 0
- NOT RUN: 1 (HW-05 storage benchmark — no authorized passive data; `NOT ESTABLISHED`)

## Key verified states (all from direct evidence)

- Versions reconciled: CLI `/usr/local/bin/ollama` = ExecStart binary = server API = **0.32.9**. Corpus source is v0.32.11 — declared NOT version-matched; no source-based behavior claims made (receipt 03 §3, report F1).
- Model: exactly one pulled model, `qwen3.5:9b-q4_K_M`, digest `6488c96fa5faab64…9ea7` (matches baseline short digest), Q4_K_M 9.7B. None loaded at audit time.
- Isolation: `CUDA_VISIBLE_DEVICES=GPU-cc758e31-…`, `GGML_VK_VISIBLE_DEVICES=999`, `OLLAMA_VULKAN=0` effective; journal shows runner discovery scoped to the RTX 5060 only.
- Exposure: loopback-only `127.0.0.1:11434`; no proxy/auth layer on hxs-4 — compliant with the owner ruling; remote path remains an open decision (D1).
- Health: no Xid/NVRM/OOM/crash; service's 2026-08-23 restart was a clean external stop/start; one recoverable warmup `cudaMalloc` failure observed (F3, watch item).

## Fact versus inference

- Facts: everything in the §4 matrix except the two labeled items.
- Inference (labeled in report): model-store filesystem placement from mount table + server config (HW-04 limitation); explanation of the F2 default-context behavior is unresolved (observation is fact, mechanism is not).
- NOT ESTABLISHED: current model residency (nothing loaded; read-only audit cannot load); storage performance (HW-05).

## Mutation status

None detected or performed. Host mutation count: 0. The transient-retry budget was not used.

## Sanitization

Evidence scanned for passwords, tokens, keys, cookies, authorization headers: clean
(only benign llama.cpp token-count log lines matched the pattern). The SSH credential
was consumed by the askpass helper only — never printed, logged, or stored.
`/tmp/.hx-askpass.sh` deleted after the session.

## Artifact hashes

`sha256sums.txt` at the evidence root covers every submitted artifact.

## Remaining risks and exact decisions required

1. **D1 (Agent Zero, open since 2026-08-14):** OmniRoute remote-consumption mechanism undefined; endpoint stays loopback until defined and measured.
2. **D2 (Agent Zero):** acquire 0.32.9-matched source, or authorize a deliberate pinned upgrade with rollback (report R3).
3. **D3 (owner doc decision):** record the default-context contract — observed default `num_ctx=4096` despite `OLLAMA_CONTEXT_LENGTH=65536` (report F2/R2).
4. Risk F3 (watch): VRAM-tight model loads with vision warmup on the 8 GB card; keep single-runner settings and the unload-before-num_ctx rule until measured (R4).
5. Limitation F7: blob-level store permissions unverified without privilege (R6, low).

`PASS — AUDIT EVIDENCE PACKAGE COMPLETE`
