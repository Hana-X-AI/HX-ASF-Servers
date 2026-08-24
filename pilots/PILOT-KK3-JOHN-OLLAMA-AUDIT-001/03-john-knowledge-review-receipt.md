# 03 — John Knowledge Review Receipt

| Field | Value |
| --- | --- |
| Session ID | `john-initial-20260824-01` |
| Work order | `WO-OLLAMA-AUDIT-HXS5-001` (sha256 `d1883f295b36161c8b9950bb807ce3946d963a261a8b3168d2993b2d08ef672d`) |
| Context hash | `725553195e9c2df97c341fdc08b54c1fcd572c0ada69f9bb376e33f01d8278aa` |
| Correction session | `initial` |
| Executor role | `john` |
| Target identity verified | `hxs-5`, local IPv4 `192.168.50.204/24` on `eno1`; method: local session, no SSH; verified 2026-08-24T09:30:19+00:00 |

## Mandatory receipt

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5
Source: /opt/tkv-local/ollama
Reviewed At: 2026-08-24T09:35:48+00:00
Relevant Files: 14 (listed below; survey evidence: 06-raw-evidence-sanitized/kr-01-knowledge-survey.txt)
Authority/Version Identified: NO HXS-5 OLLAMA BASELINE EXISTS. hxs-5 assigned role is
  "Edge / ingress — NGINX" (SERVER-REGISTRY.md); hxs-5 discovery (2026-08-12) records no
  Ollama installed. Corpus Ollama source snapshot identified as v0.32.11, commit
  39df91c9826b3c0c83677f75cd230d8848d287c3 (prior material, craig-ollama-specialist.md).
  Host-specific approved pins exist only for hxs-1 (v0.32.14, doc-009 runtime locks) and
  historically hxs-4 (0.32.9, act-014). No approved Ollama version, model, or workload
  target is ratified for hxs-5.
Applicable Tests/Runbooks: implementation/hx-ai-infrastructure-roadmap/documents/doc-011/
  (runbook.md, acceptance.md — hxs-1-scoped precedent); implementation/archive/
  HX-Infrastructure-main/tests/ai-runtime/hx-runtime-acceptance.ps1 (contract precedent);
  governance/policy/ai-runtime-acceptance-contract.md (acceptance classes)
Contradictions or Gaps: G1 no hxs-5 Ollama authority baseline (role registry assigns NGINX,
  not Ollama); G2 kernel drift 7.0.0-28 -> 7.0.0-30 since discovery (routine updates, not a
  contradiction); G3 knowledge-site loopback-only directive of 2026-08-18 is RESCINDED for
  that service and is not Ollama authority. No contradiction blocking audit execution.
Task May Proceed: YES
```

## Files reviewed (14)

| # | Path | Relevance |
| ---: | --- | --- |
| 1 | `/opt/tkv-local/ollama/implementation/archive/HX-Infrastructure-main/servers/hxs-5/discovery.md` | Current hxs-5 baseline (2026-08-12): i5-7500 4C/4T, 32 GB non-ECC, Intel HD 630 only, no discrete GPU, no CUDA, single 238.5 GB NVMe, **no Ollama installed**, ufw inactive |
| 2 | `/opt/tkv-local/ollama/implementation/archive/HX-Infrastructure-main/servers/hxs-5/pre-work-results.md` | Human preparation record: passwordless sudo, fleet key, ufw disabled, SSH active |
| 3 | `/opt/tkv-local/ollama/implementation/archive/HX-Infrastructure-main/SERVER-REGISTRY.md` | Fleet registry: hxs-5 role `Edge / ingress — NGINX`, status READY |
| 4 | `/opt/tkv-local/ollama/ollama-main/version/version.go` | Source snapshot `Version = "0.0.0"` (unpinned source tree); no `.git` metadata present |
| 5 | `/opt/tkv-local/ollama/ollama-main/AGENTS.md` | Build-only instructions; no constraint on read-only audit |
| 6 | `/opt/tkv-local/ollama/craig-ollama-specialist.md` | Prior specialist profile; identifies corpus source as Ollama `v0.32.11`, commit `39df91c9826b3c0c83677f75cd230d8848d287c3`; source-grounded audit evidence list |
| 7 | `/opt/tkv-local/ollama/research/MVP1-CONSTRAINTS.md` | hxs-1 execution constraints: `OLLAMA_HOST=127.0.0.1:11434` because Ollama has no authentication; `OLLAMA_CONTEXT_LENGTH` explicit; flash-attention gating of KV cache type — hxs-1-scoped precedent |
| 8 | `/opt/tkv-local/ollama/research/README.md` | Evidence-tier standard; research records are evidence, not decisions |
| 9 | `/opt/tkv-local/ollama/implementation/hx-ai-infrastructure-roadmap/documents/doc-009/0003-hxs1-mvp1-runtime-locks.md` | hxs-1 approved pin: Ollama `v0.32.14`, commit `d67ad834…`, model `qwen3.8:27b-q4_K_M`, listen `127.0.0.1:11434` — hxs-1-only authority |
| 10 | `/opt/tkv-local/ollama/implementation/hx-ai-infrastructure-roadmap/documents/doc-011/runbook.md` | hxs-1 MVP-1 execution runbook (preflight patterns reused as audit probe precedent) |
| 11 | `/opt/tkv-local/ollama/implementation/knowledge-site/audit/claude_20260818_2051_agent-api-loopback-only-directive.md` | Loopback-only directive — header confirms **RESCINDED 2026-08-18**; knowledge-site scope, not Ollama authority |
| 12 | `/opt/tkv-local/ollama/implementation/archive/HX-Infrastructure-main/governance/logs/actions-and-issues.md` | Open/resolved issues: `iss-013` (Vulkan ignores `CUDA_VISIBLE_DEVICES` — resolved), `iss-014` (GPU overcommit wedge — resolved), `iss-015` (silent prompt truncation — open, upstream), `act-001`/`act-011` (hxs-5 DNS records), `act-014` (hxs-4 Ollama 0.32.9 commissioning) |
| 13 | `/opt/tkv-local/ollama/implementation/archive/HX-Infrastructure-main/governance/policy/ai-runtime-acceptance-contract.md` | Acceptance evidence classes (referenced; engine-neutral contract precedent) |
| 14 | `/opt/tkv-local/ollama/implementation/archive/HX-Infrastructure-main/tests/ai-runtime/hx-runtime-acceptance.ps1` | Runtime acceptance script precedent (Windows harness; not executed) |

## Authority and version resolution

| Item | Value | Source class |
| --- | --- | --- |
| hxs-5 assigned role | Edge / ingress — NGINX | Ratified registry (historical, 2026-08-13) |
| hxs-5 approved Ollama version | **NOT ESTABLISHED** — none exists | Absence in registry/knowledge |
| hxs-5 Ollama installed state (knowledge) | Not installed as of 2026-08-12 | hxs-5 discovery.md (historical evidence) |
| Corpus source snapshot | Ollama `v0.32.11`, commit `39df91c9826b3c0c83677f75cd230d8848d287c3` | Prior material (Craig profile); source tree itself unpinned (`0.0.0`) |
| hxs-1 approved pin | `v0.32.14`, commit `d67ad834…` | doc-009 runtime locks (host-specific, not hxs-5) |
| hxs-4 historical | `0.32.9` (act-014, 2026-08-14) | Historical precedent only |

Because no hxs-5 Ollama baseline exists, expected audit results are derived from the 2026-08-12 discovery baseline (no Ollama, no discrete GPU) and the role registry. Per the work order, Ollama being present or absent is a finding, not an audit failure; any live drift from the 2026-08-12 discovery record will be recorded as a finding and flagged for reconciliation.

## Contradictions or gaps

- **G1 (gap):** No ratified Ollama version, model, workload, or exposure authority exists for hxs-5. Audit expected-results therefore cite the discovery baseline and registry, and every "controlling target" in gap analysis is labeled accordingly.
- **G2 (drift, not contradiction):** Live kernel `7.0.0-30-generic` vs discovery `7.0.0-28-generic`; consistent with routine package updates (discovery noted 32 upgradable packages).
- **G3 (stale-authority hazard, resolved):** The knowledge-site loopback-only directive is rescinded; it is not used as Ollama exposure authority. Ollama exposure assessment defaults to John's profile rule (loopback unless explicit current authority states otherwise).
- No contradiction that blocks audit execution was found.

## Decision

`Task May Proceed: YES` — authority structure established; live evidence will reconcile installed state against the 2026-08-12 baseline.
