# Goal: Ollama Fleet Requalification — Wave 1 of 4 — hxs-1 / Qwen-X (hxs-2/3/4 follow later)

- Goal ID: 2026-08-31-ollama-fleet-requalification-hxs1-qwen-x (this file's name)
- Version: 1
- Status: approved
- Owner: Agent-Zero
- Created: 2026-08-31
- Human authority: Agent-Zero
- Agent lane(s): james (governor/intake), mia (management), john (Ollama), rick (OS/systemd/DNS), bailey (test design), gordon (independent QA), trinity (OmniRoute), raphael/quinn (RAG read-only), carol (catalog)

## Intent

Requalify hxs-1 from zero against current live state so that the Qwen-X Ollama
service becomes a complete, discoverable, production-ready fleet capability. The
historical M8 PASS is precedent and a regression baseline only — it is not proof
of the present state, and no historical PASS, catalog `ACTIVE` label, or
configuration claim satisfies a new acceptance condition without current
evidence. This is Wave 1 of the owner's four-host Ollama Fleet Requalification
program and is scoped to hxs-1 only. hxs-2, hxs-3, and hxs-4 are not authorized
or dispatched here; they follow as separate waves only after hxs-1 is fully
complete and Agent Zero records approval. hxs-1 supplies the audit method,
capability schema, evidence package, and acceptance gates those later waves
reuse, without copying host configuration values.

Source of record (intake): `/home/hxsa/opt/local-tkv/agent-zero-docs/projects/llm-audit/2026-08-31-factory-intake-ollama-fleet-requalification-wo1-hxs1.md`

## Scope and target

- Target identity: hxs-1 (192.168.50.200), role Deep reasoning & synthesis, call-sign Qwen-X, model Qwen 3.8 27B (`hx-qwen3.8-27b-64k` historical alias).
- Baseline: to be re-established live in Phase A. The current `servers/hxs-1/configuration.md` is derived from prior evidence, not a fresh live probe, and the owner reports the installation is incomplete against the desired service standard.
- In scope (after Gate A): hxs-1 Ollama binary/service/unit/drop-ins and model aliases named in the approved write set; exact Qwen-X model profile and approved model-store artifacts; approved service FQDN `qwen-x.hx.local.arpa` (D1) and corresponding registry/catalog/routing records through the correct lanes; Ollama upgrade to the latest version if a newer release exists (D2); three full reboots + one performance run (D3); full access to the current RAG pipeline for end-to-end validation with no new RAG systems installed (D4); web-search verification of the current ON posture (D5); bounded inference, cache, GPU, context, tool, and RAG tests; sanitized evidence and repository documentation.
- Out of scope unless separately authorized: replacing the Qwen-X model family or fleet role; any work on hxs-2, hxs-3, or hxs-4 (future waves, not part of this goal); GPU firmware, BIOS, kernel, driver, storage partition, or network redesign; containers or Ansible; host firewall installation or activation; public Internet exposure or a new authentication gateway; training, fine-tuning, or model modification beyond approved Modelfile/profile aliases; MCP server deployment while the fleet MCP hold is active; installing new RAG/retrieval/embedding/vector systems (D4 — use the current pipeline only); cloud-model fallback or `:cloud` model substitution (distinct from Ollama web-search cloud, which is ON per D5); secret content in commands, evidence, chat, repository, or logs.
- Constraints: native systemd service (no containers); private-LAN exposure boundary (no host firewall, owner rule 2026-08-26); local-model-first (no cloud substitution); append-only governance edits; each cold reboot individually authorized.

## Success conditions and evidence

| ID | Acceptance condition | Required evidence | Verifier |
| --- | --- | --- | --- |
| SC-01 | Live TKV review precedes probes and identifies local snapshot/version/provenance | John knowledge receipt with `Task May Proceed` | James gate |
| SC-02 | All live identity sources reconcile or execution stops | Identity matrix, hashes, source comparison | James + Gordon |
| SC-03 | Historical M8 claims are re-proven or explicitly superseded | Historical-to-live reconciliation table | Gordon |
| SC-04 | Every audit vector and capability has an honest status and evidence | Audit and capability matrices | Gordon |
| SC-05 | Gate-A findings and remediation scope receive owner approval before mutation | Signed/recorded Gate-A decision | Agent Zero |
| SC-06 | Approved service FQDN resolves and works from required consumers; no raw IP remains in consumer config | DNS probes, config search, endpoint tests | Rick + Gordon |
| SC-07 | Exact model and intended contexts show no CPU fallback and measured optimal GPU placement | `/api/ps`, GPU telemetry, benchmark dataset | John + Gordon |
| SC-08 | Cache, context, queue, concurrency, preload, and timeout settings are evidence-optimized | Comparative benchmark and configuration rationale | Bailey + Gordon |
| SC-09 | Native text, streaming, thinking, structured output, and required compatibility APIs pass | Versioned capability suite | Bailey + Gordon |
| SC-10 | Single, parallel, multi-turn, and streaming tool use pass unit and real-harness tests | Tool transcripts and containment cases | Bailey + Gordon |
| SC-11 | Real RAG path passes retrieval, citation, conflict, no-answer, stale, and injection cases | End-to-end RAG evidence package | Bailey + Gordon |
| SC-12 | Discovery/catalog/routing use the call-sign and service FQDN consistently | Consumer proof and catalog/routing records | Trinity + Carol + Gordon |
| SC-13 | Service survives three cold reboots and returns the exact resident alias/digest within the recovery SLO | Boot-cycle evidence | Gordon |
| SC-14 | ~~24-hour soak~~ — REMOVED by owner D3 (2026-08-31, "overkill"); reliability window is three full reboots + one performance run | n/a — owner decision | Agent Zero (D3) |
| SC-15 | Rollback capability is executable at the smallest changed layer for any remediation change | Pre/post hashes, diffs, backups | Gordon |
| SC-16 | Evidence is complete, sanitized, cataloged, and independently reconciled to live state | Governor checklist + Carol receipt | James + Carol |
| SC-17 | Agent Zero records final acceptance; merge is not automatic | Owner decision record | Agent Zero |

Owner D3 (2026-08-31) removes the 24-hour soak as overkill; the reliability
window is three full reboots + one performance run, so SC-14 is removed by owner
decision rather than deferred. No completion exception is used for SC-11, SC-13,
or SC-15 unless Agent Zero makes a new, explicit, dated decision after reviewing
the risk. Rollback capability (SC-15) remains required as a safety mechanism for
any remediation change.

## Execution controls

- Pre-flight (intake existence check): this intake brief exists and is DRAFT (no execution authority). Registry-role consistency is re-verified live in Phase A (M2), not assumed from `servers/hxs-1/configuration.md`.
- Active charters reviewed (Phase M): james, john, rick, bailey, gordon, trinity, raphael, quinn, carol, mia. Qualified agents available: YES — subject to per-dispatch lane capability probe (ST-5).
- Maximum iterations / retries: 1 initial run + 1 bounded correction per failed correctable gate.
- Time / token limits: per-dispatch context budget (Phase A read-only bounded; see work orders).
- Stop conditions: target mismatch, authority conflict, unexpected service or binary, source/version contradiction, model digest drift, secret exposure, unsafe GPU/driver state, Xid/OOM/wedge, unplanned CPU fallback, off-LAN exposure, missing rollback, test result outside the authorized safety envelope, undeclared mutation, evidence-integrity failure.
- Rollback / containment: smallest affected layer, deterministic inverse, pre/post sha256 + unified diff; rollback capability retained (SC-15) but no separate rollback drill (D3).
- HITL checkpoints: owner decisions D1–D5 (below), Gate A (findings + write set + upgrade + DNS + downtime + rollback), each cold reboot, Gate B (governor checklist + Gordon qualification + Carol receipt), Agent Zero final acceptance.

## Owner decisions (HITL, answered 2026-08-31)

- D1 — Service FQDN: APPROVED `qwen-x.hx.local.arpa` (distinct from host `hxs-1.hx.local.arpa`).
- D2 — Upgrade authority: APPROVED auto-update — if a newer Ollama release exists, update to it; John's safe-install protocol (download, authenticate, hash, inspect) and a rollback path still apply.
- D3 — Test window: three full reboots + one performance run. The 24-hour soak is removed as overkill. Rollback remains a safety requirement.
- D4 — RAG: full access to any system in the current RAG pipeline; no new systems installed.
- D5 — Web search / Ollama cloud: ON and active on all four hosts; test and verify. Cloud-MODEL substitution remains prohibited.

## Notes and links

- KDDs: KDD-0003 (Ollama audit pilot adoption), KDD-0004 (hx1 Qwen pilot adoption), KDD-0013 (model lanes), KDD-0016 (agent taxonomy), KDD-0024 (two-stage handoff closure).
- Program relationship: Wave 1 is hxs-1 only. hxs-2, hxs-3, and hxs-4 are separate future waves that do not begin until hxs-1 is fully complete and Agent Zero records approval; they are out of scope for this goal. This goal establishes the reusable method and gates.
- Related goals: `2026-08-24-hx1-ollama-qwen38-27b` (historical M8 precedent), `2026-08-27-fleet-baseline-deployment`.
- Target-lock precedent: `PILOT-KK3-JOHN-OLLAMA-AUDIT-001` FAIL (wrong target hxs-5) and `-002` PASS (hxs-4) are the audit pilots; this goal's target is locked to hxs-1 (192.168.50.200, call-sign Qwen-X) for all downstream agents, enforced fail-closed by plan.md §0 and each live work order.
- Blueprint: `servers/BLUEPRINT-llm-server.md` (downstream-consumer contract §8).
- Pilot directory: `pilots/PILOT-OLLAMA-FLEET-REQUAL-HXS1-001/`.

## Amendments and history

Append-only. This goal is DRAFT; no status change, scope change, or acceptance
has been recorded yet.

<!-- REQUIRED machine-readable state. -->

```yaml work-state
id: 2026-08-31-ollama-fleet-requalification-hxs1-qwen-x
status: approved
status_date: 2026-08-31
authority: >-
  Scope-lock complete: owner D1-D5 answered 2026-08-31 (FQDN qwen-x.hx.local.arpa;
  auto-update; three full reboots + one performance run, no soak; full current-RAG-pipeline
  access with no new systems; web search ON). Rollback capability-only and the
  web-search-vs-cloud-model split confirmed by owner.
reconcile: none
```
