# Goal: Provision the hxs-3 tooling-inference backend (Muse Glimmer 30B via Ollama, mutating pilot)

- Goal ID: 2026-08-26-hxs3-muse-glimmer-tooling (this file's name)
- Version: 1
- Status: **in-progress — M0 authorized** (2026-08-26; historical — see transition)
- Status transition 2026-08-27 **[current]**: **COMPLETE — PASS** — milestones M0/M1/M4/M5/M7/M8 all PASS; owner ACCEPT 2026-08-27 ("Meta-X is accepted into production", state log row 26); SC-06 multimodal **FORMALLY DEFERRED 2026-08-27** (hxs-1 SC-05 class — owner-decided, tracked, not forgotten; returns when the owner calls a vision-probes window). [open correction 2026-08-27: original status entry restored and the closure recorded as a dated transition per the append-only convention] [LABELED COMPLETION EXCEPTION 2026-08-30, append-only: SC-06's formal owner deferral (2026-08-27, state log row 26) is the documented owner-approved exception under the goal template's completion rule — every required success condition passes OR a documented owner-approved exception exists. The SC-06 deferral is tracked and reopens when the owner calls a vision-probes window; the COMPLETE — PASS status is consistent with the template's completion rule under this exception.]
- Owner: Agent-Zero
- Created: 2026-08-26
- Human authority: Agent-Zero
- Agent lane(s): kimi-k3 (governor), rick (Ubuntu OS plane), john/Esme (Ollama plane), carol (knowledge)
- Plan: session plan `patriot-miles-morales-us-agent.md` (approved 2026-08-26); authoritative source pilot v1.1 `agent-zero-docs/pilots/hxs-3/meta/codex_20260825_2332_hxs-3-muse-glimmer-30b-tooling-pilot-and-deepseek-harness-registration.md` (Harness-free mapping per KDD-0006 convention)

## Intent

Provision `hxs-3` as a persistent local **tooling-inference backend** with the
exact Ollama artifact **`muse-glimmer:30b`**, qualified end to end, exposed
fleet-scoped (LAN, no host firewall — owner rule), and registered in the Second
Brain catalog as the discoverable capability of record: the factory's primary
tool agent for the RAG pipeline — a **sequential, one-tool-call-per-turn
specialist**. Parallel tooling happens above the model in KK3's orchestration
plane, never as a claimed model capability. The model proposes at most one tool
call per turn and never authorizes or executes; KK3 retains orchestration,
acceptance, and evidence. **Enforcement contract (2026-08-26, review finding):**
the harness enforces the limit at two levels — a model response containing more
than one tool call is REJECTED, and every accepted call executes serially with
its result returned before the next selection is requested. The request-level
`parallel_tool_calls: false` flag is treated strictly as a compatibility probe
where the serving platform honors it — it is never the enforcement mechanism.

## Scope and target

- Target identity: hxs-3 (192.168.50.202). Registry role: Agent intelligence.
- Baseline (records; M1 re-verifies): i7-5960X 8c/16t, 66 GB RAM, 2× RTX 5060
  Ti 16,311 MiB (driver 580.173.02 validated 2026-08-12), Ubuntu 24.04.4, NVMe
  root, no Ollama, Secure Boot disabled.
- In scope: OS readiness (blueprint mask set incl. hybrid-sleep), Ollama
  install/pin, exact-tag pull + FULL identity freeze (LM + projector digests,
  manifest, template/renderer, license), preload/persistence, native Phase A
  baseline, system-policy preservation, prompt/reasoning compatibility +
  `reasoning_strength` mapping probes, tool contract suite (single, sequential
  dependency, multi-need sequential selection, partial failure, schema/auth
  failures) + one-call-per-turn invariant + ATEM normalization gate, multimodal
  tooling probes, context ladder 32K→64K→128K, persistence + reboot recovery,
  scoped endpoint + boundary proof, catalog registration, consumer-proof task,
  configuration.md, acceptance reconciliation.
- Out of scope: DeepSeek Harness (verified nonexistent); a llama.cpp serving
  plane UNLESS the M4/M5 compatibility gate fires the drafted escape hatch;
  parallel tool calling (registered limit `parallel_tool_calling: false`);
  gpt-oss changes (retained as task-shaped control); LightRAG integration
  (consumer unbuilt); exposure beyond the LAN boundary.
- Constraints: per-milestone work orders; one bounded correction per failed
  correctable gate; commits only with per-instance owner approval (Alert 2).

## Owner decisions

- D1: model store per blueprint (root ext4) — ratified via plan approval.
- D2: endpoint = fleet 192.168.50.0/24, no host firewall (owner rule) —
  ratified via plan approval.
- D3: artifact `muse-glimmer:30b` exact (owner selection 2026-08-26; manifest
  prefix `de878ce33ad8` = cross-check only; local full digest = frozen identity
  at M4).
- D4: Wi-Fi rfkill soft block, boot-persisted (house posture; M1 verifies the
  interface first) — ratified via plan approval.
- D5: operating context = 65,536 (64K); the ladder validates 32K→64K→128K
  first — ratified via plan approval.
- D6: M8 cold reboots pre-approved per-cycle (governor-announced window) —
  ratified via plan approval.
- D7: registration to the Second Brain catalog (Harness-free, KDD-0006
  convention) — ratified via plan approval.
- D8: operating `reasoning_strength` default for the tooling role — deferred
  to M5 mapping evidence (recommend low/medium for latency-bounded tool agent;
  reasoning cannot be disabled — recorded).

## Success conditions and evidence

| ID | Property | Measurement / procedure | Expected result | Evidence | Verifier |
| --- | --- | --- | --- | --- | --- |
| SC-01 | Model identity frozen | exact tag + full local digests (LM + projector), manifest, template/renderer, license | Exact approved artifact recorded | model evidence, ollama show | KK3 gate |
| SC-02 | GPU placement | `ollama ps` + per-GPU telemetry under load | Both 5060 Ti allocated; no unapproved CPU fallback | GPU telemetry | KK3 gate |
| SC-03 | Runtime profile | context ladder 32K→64K→128K on exact digest; operating 64K (D5); KV/latency measured | Operating window qualified with capacity + latency evidence | capacity record | KK3 gate |
| SC-04 | Boot recovery | service restart + 3 cold reboots | Alias resident and ready each time within budget, no manual action | reboot evidence | KK3 gate |
| SC-05 | Tooling contract | contract suite (single/sequential/multi-need/partial-failure/schema-auth) + one-call-per-turn invariant + ATEM→tool_calls normalization + structured/denial + system-policy preservation | Owner-confirmed thresholds met; invariant proven with ENFORCEMENT: any response containing more than one tool call is rejected, accepted calls execute serially with results returned before the next selection; `parallel_tool_calls` flag exercised as a compatibility probe only, never as enforcement | suite results | KK3 gate |
| SC-06 | Multimodal | image-input probes with projector loaded | Images consumed correctly (evidence reported; disposition per the multimodal deferral 2026-08-27 — owner-decided, tracked, reopens on a vision-probes window) | probe evidence | KK3 gate |
| SC-07 | Exposure boundary | bind 0.0.0.0 (loopback preserved), reachability from /24, refusal where testable; no host firewall | Reachable inside 192.168.50.0/24; the LAN itself is the boundary | security evidence | KK3 gate |
| SC-08 | Registration + process | catalog capability record (`parallel_tool_calling: false`) + retrieval package + consumer-proof sequential tooling task + sanitized packages + receipts | Record live; task completes end-to-end; complete packages; KK3 gate; owner sign-off | catalog record, task evidence, pilot record | Agent-Zero |

## Execution controls

- Pre-flight (intake existence check): DONE 2026-08-26 — baseline from
  `/opt/tkv-local/servers/hxs-3/` + directive driver validation (records);
  live re-verification at M1.
- Active charters reviewed: rick, john, kimi-k3, carol (all active).
- Maximum iterations: 1 initial specialist run + 1 bounded correction per
  failed correctable gate.
- Stop conditions: safety, authority, model-identity, Ollama-Muse
  incompatibility (escape hatch: drafted llama.cpp fallback), or repeated
  failure — immediate escalation.
- Rollback / containment: smallest affected layer (blueprint pattern).
- HITL checkpoints: M0 authorization, Gate 0 decisions, each cold reboot,
  threshold confirmations, final sign-off.

## Notes and links

- KDDs: KDD-0007 (adoption). Playbook: PILOT-HX1 (pattern source, third
  validated use), PILOT-HXS2-CODERX-BACKEND-001 (parallel pilot).
- Controlling sources: v1.1 authoritative pilot + Meta llama.cpp guide
  (`doc-1.md`), `/opt/tkv-local/servers/hxs-3/` (historical, cross-check),
  `/opt/tkv-local/ollama` (role knowledge gate), blueprint, catalog retrieval
  package (M1), this file's owner decisions.
- Second Brain evaluation (standing directive): capability LIMITS become
  first-class registry content (`parallel_tool_calling: false`) so every future
  dispatch retrieves the limit; playbook earns its third validated host —
  formal LLM-backend-deployment pattern drafted at M8; retrieval package at
  M0/M1. DFlash/deep integrations deferred per evidence.

<!-- Machine-readable current state (O1, work-state.schema.yaml). The prose
     above is the historical record and is never rewritten; this block is the
     single source every status tool reads. -->

```yaml work-state
id: 2026-08-26-hxs3-muse-glimmer-tooling
status: complete
status_date: 2026-08-27
authority: >-
  PILOT-HXS3-MUSE-GLIMMER-TOOLING-001 state log: 'goal COMPLETE — PASS (governor edit + re-render)'; 'PILOT-HXS3-MUSE-GLIMMER-TOOLING-001 is COMPLETE and CLOSED'
reconcile: none
```
