# 03 — John Knowledge Review Receipt

| Field | Value |
| --- | --- |
| Session ID | `john-initial-20260824-02` |
| Work order | `WO-OLLAMA-AUDIT-HXS4-001` (sha256 `6b048318755fd4acc3bcf4447af75a9c2ab29f204df7a6ce24a5e12440d4377f`) |
| Context hash | `bf55893b954c2527dcfe714d2e77d503c10b22c04b7b0142daddc88a9a8eeb77` |
| Correction session | `initial` |
| Executor role | `john` |
| Target host | hxs-4 (192.168.50.203) |
| Knowledge source | `/opt/tkv-local/ollama` (read locally on hxs-5, where this session runs) |
| Reviewed at | 2026-08-24T10:28:39+00:00 |

## 1. Roster check (delta plan override 4; profile §4.2)

`agents/` in `/home/hxsa/opt/HX-ASF-Servers` contains exactly three lanes:
`_template/`, `john/`, `kimi-k3/`, plus `README.md`.

- **John is the only current Ollama specialist.** No other Ollama agent charter exists.
- **craig is archived history, not a teammate.** All craig material lives in the
  vault under `/opt/tkv-local/ollama/implementation/archive/HX-Infrastructure-main/governance/operations/ollama/`
  (`craig-ollama-specialist.md` plus two dated HTML records) and is cited in John's
  own profile (§2.2) strictly as a *prior specialist profile*. Grep across `agents/`
  finds craig only in reference/inventory contexts.

## 2. Authority and baseline established for Ollama on hxs-4

| Layer | Source | Key facts |
| --- | --- | --- |
| Current fleet registry (this repo) | `servers/SERVER-REGISTRY.md` (imported 2026-08-24) | hxs-4 = 192.168.50.203; i7-14700F 20c/28t; 32 GB DDR5; RTX 5060 Ti 16311 MiB + RTX 5060 8151 MiB; role **Retrieval & AI utility** — consistent with Ollama presence (delta override 1 satisfied) |
| As-found hardware record | `/opt/tkv-local/servers/hxs-4/discovery.md`, `driver-results.md`; vault mirror `implementation/archive/HX-Infrastructure-main/servers/hxs-4/` | Both GPUs confirmed by driver as RTX 5060 Ti (0000:01:00.0) and RTX 5060 (0000:07:00.0); `nvidia-driver-580-server-open` 580.173.02, CUDA 13.0 |
| Commissioned workload record (baseline) | `…/tests/ai-runtime/workloads/qwen35-9b-ollama.json` | COMMISSIONED 2026-08-14, state `OPERATIONAL - LOOPBACK ONLY`; Ollama **0.32.9**; model `qwen3.5:9b-q4_K_M`, digest `6488c96fa5fa`, 9.7B, native ctx 262144 |
| GPU isolation baseline | same record | RTX 5060 UUID `GPU-cc758e31-d23b-3c53-bee6-dae3299a6f11` isolated via `CUDA_VISIBLE_DEVICES` + `GGML_VK_VISIBLE_DEVICES=999` + `OLLAMA_VULKAN=0`; RTX 5060 Ti UUID `GPU-11b1a30e-8c11-001b-7b8b-7b1e15ab6978` must remain invisible to Ollama |
| Acceptance authority | `…/governance/policy/runtime-acceptance-decisions.md` | `accepted-local-runtime` GRANTED (loopback); `accepted-network-consumable` NOT GRANTED — owner ruling 2026-08-14: loopback-bound, remote only via OmniRoute (mechanism undefined); conditions: prompts < 65,536, thinking disabled, listener `127.0.0.1:11434` |
| Measured performance baseline | workload record `measured_residency` | Full-GPU residency to ctx 16384 (6,794 MiB of 8,151); 32768/65536 run CPU/GPU split; ~28 tok/s real generation at 65536; silent truncation to 32,770 tokens on overflow (iss-015); incident `hxs4-wedge-001` (driver wedge from concurrent runners) |
| Version identity | `…/governance/operations/ollama/craig-ollama-specialist.md` (archived), recon record `hx-ollama-reconnaissance…20260815_0228.html` | Corpus source snapshot = **v0.32.11**, commit `39df91c9826b3c0c83677f75cd230d8848d287c3`; commissioned hxs-4 runtime = **0.32.9** |
| Pre-flight (governor, 2026-08-24) | work order / delta plan override 2 | ollama 0.32.9 at `/usr/local/bin/ollama`, service active, API `{"version":"0.32.9"}`, both GPUs present |

## 3. Version reconciliation position (delta override 6)

- Installed/expected runtime: **0.32.9**. Corpus source: **v0.32.11**. These differ.
- Per John's profile (§2.3 rule 1, §9), the v0.32.11 corpus source must **not** be
  used to explain 0.32.9 runtime behavior. No 0.32.9-matched source exists in the
  corpus. Consequence: source-level claims about installed behavior are out of
  reach for this audit; behavior claims rest on live read-only evidence and the
  2026-08-14 commissioning measurements only. This is a declared limitation, not
  a blocker — the delta plan anticipates it and requires the reconciliation result
  in the report.

## 4. Applicable tests and runbooks

- Audit matrix: base plan `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-001/plan.md` §10 (ID/HW/GPU/SVC/API/MOD/SEC + passive performance).
- Guardrails: base plan §11 (read-only only); work-order prohibited actions.
- Reference fixtures: `…/tests/ai-runtime/fixtures/*.json` and `hx-*.ps1` harnesses — **reference only**; active inference is out of scope for this audit, so they are not executed.
- Vault `implementation/docs/agent/*.md` files are byte-sized stubs (e.g. one contains only "xburst test 1") — not usable runbooks; noted as a corpus gap.

## 5. Contradictions and gaps

1. **Source snapshot v0.32.11 vs installed 0.32.9** — declared; handled per section 3 (version-matched source rule).
2. **Registry workload list vs commissioned reality** — registry TARGET-STATE for hxs-4 lists Qdrant + Web-UI, Qwen2.5-3B, BGE-M3/Nomic embeddings, BGE-Reranker-v2-m3; the only commissioned Ollama workload is `qwen3.5:9b-q4_K_M`, and registry workloads were confirmed NOT installed as of 2026-08-14. Live state will be re-verified by probe (API-02).
3. No current (non-archived) Ollama install/upgrade runbook exists in the corpus; installation authority is historical (owner instruction 2026-08-14). No mutation is authorized in this audit, so this does not block.

## 6. Receipt

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-4 (192.168.50.203)
Source: /opt/tkv-local/ollama
Reviewed At: 2026-08-24T10:28:39+00:00
Relevant Files: 11 (servers/SERVER-REGISTRY.md; servers/AGENTS.md; agents/README.md;
  /opt/tkv-local/servers/hxs-4/discovery.md;
  /opt/tkv-local/ollama/implementation/archive/HX-Infrastructure-main/SERVER-REGISTRY.md;
  …/servers/hxs-4/discovery.md; …/tests/ai-runtime/workloads/qwen35-9b-ollama.json;
  …/governance/policy/runtime-acceptance-decisions.md;
  …/governance/operations/ollama/craig-ollama-specialist.md;
  …/governance/operations/ollama/hx-ollama-reconnaissance-and-agent-craig-hxs4-audit_gpt-5.6-sol_20260815_0228.html;
  /opt/tkv-local/ollama/ollama-main/version/version.go)
Authority/Version Identified: Ollama 0.32.9 commissioned on hxs-4 (2026-08-14),
  qwen3.5:9b-q4_K_M digest 6488c96fa5fa, loopback-only, RTX 5060 UUID-isolated;
  corpus source snapshot v0.32.11 (commit 39df91c) — NOT version-matched, declared
Applicable Tests/Runbooks: base plan §10 audit matrix + §11 guardrails;
  tests/ai-runtime fixtures (reference only, not executed)
Contradictions or Gaps: source 0.32.11 vs installed 0.32.9 (declared);
  registry TARGET-STATE workloads vs commissioned as-built (to be re-verified live);
  vault agent-docs stubs are not runbooks
Task May Proceed: YES
```
