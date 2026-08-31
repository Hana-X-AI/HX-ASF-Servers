# Factory Intake Brief — Ollama Fleet Requalification

## Work Order 1 of 4: hxs-1 / Qwen-X Reference Implementation

| Field | Value |
| --- | --- |
| Status | **DRAFT — for Agent Zero approval and James intake; no execution authority** |
| Date | 2026-08-31 |
| Human owner | Agent Zero |
| Intake recipient | James, Factory Governor |
| Program | Four host-specific work orders: hxs-1, hxs-2, hxs-3, hxs-4 |
| First target | hxs-1 / Qwen-X / Ollama |
| Mission | Audit, remediate, optimize, integrate, and independently requalify each Ollama service as a complete, discoverable, production-ready fleet capability |

## 1. Owner intent

The current Ollama installations are functional but do not meet the owner's standard for a complete, best-practice, optimized service. A prior implementation demonstrated the expected class of result: the Ollama service and model were discoverable through a purpose-built service FQDN rather than an IP address or server name; both GPUs were used appropriately; cache and context behavior were tuned and measured; and the service was usable for RAG, agent tooling, model discovery, and other supported capabilities.

The factory will issue four separate host work orders with this common mission. hxs-1 is first and will become the evidence-based reference implementation. Its audit method, capability schema, evidence package, and acceptance gates will be reused for hxs-2 through hxs-4. Host configuration values will **not** be copied blindly because hardware, model, role, context envelope, and downstream consumers differ.

This document is an intake brief, not a mutation order. James must convert it into the governed goal, context packet, atomic work orders, state-log entries, and agent dispatches required by the repository contract.

## 2. Executive finding

The repository contains substantial historical evidence that hxs-1 passed a Qwen 3.8 27B pilot through M8. That evidence is valuable, but it is not proof of the present live state. The current hxs-1 configuration record explicitly derives from prior evidence rather than a fresh live probe, and the owner now reports that the installation is incomplete relative to the desired service standard.

James must therefore treat the historical M8 result as **precedent and regression baseline only**. The new order must requalify hxs-1 from zero against current live state. No historical `PASS`, catalog `ACTIVE` label, or configuration claim may satisfy a new acceptance condition without current evidence.

The earlier pilot was strong on:

- exact model aliases and digest identity;
- a 32K recovery, 64K operating, and 128K extended context ladder;
- 100% GPU residency under measured profiles;
- use of both RTX 4070 Ti Super GPUs for the 27B workload;
- Flash Attention, f16 K/V cache, preload, bounded recovery, and three cold-reboot cycles;
- native API, thinking, tool-call, long-context, and synthetic RAG/coding tests.

The earlier acceptance was incomplete for today's mission because:

- the required 24-hour soak was owner-deferred and never executed;
- the RAG proof used a synthetic BM25-lite harness, not the real retrieval, embedding, vector-store, generation, and citation path;
- tool tests proved model behavior with controlled tools, not full authorized agent-tool integration;
- the catalog still records a raw IP endpoint for Qwen-X;
- the historical discovery record said no FQDN, while later fleet evidence established the host FQDN `hxs-1.hx.local.arpa`; a separate service FQDN was not established as the consumer contract;
- upstream Ollama has moved beyond the historically recorded `0.32.15`, including material cache fixes in the 0.33 line;
- vision, embeddings, OpenAI compatibility, response semantics, streaming tools, structured output, and discovery were not all closed as an explicit model-by-model capability matrix.

## 3. Shared four-order program contract

Each host order must independently establish:

1. **Identity** — verified host, hardware, GPU UUIDs, Ollama binary provenance, exact version, service unit, model artifacts, tags, digests, quantization, licenses, and Modelfiles.
2. **Service completeness** — boot-safe native systemd service, model preload/readiness, bounded recovery, stable logs, model-store permissions, deterministic configuration, and tested rollback.
3. **Optimization** — measured context, K/V cache, Flash Attention, residency, multi-GPU placement, queueing, concurrency, prefix-cache behavior, cold/warm latency, throughput, VRAM headroom, CPU fallback, temperature, power, and error posture.
4. **Capabilities** — every relevant Ollama and exact-model feature explicitly classified and tested; unsupported or non-applicable features are recorded honestly rather than simulated.
5. **Integration** — purpose-built service FQDN, catalog and routing registration, health/discovery, real consumer use, RAG path, and agent-tool path.
6. **Reliability** — three cold reboots, restart/recovery checks, rollback drill, and a mandatory 24-hour soak unless Agent Zero records a new completion exception.
7. **Evidence** — reproducible pre/post evidence, benchmark data, sanitized command logs, hashes/diffs, independent verification, and synchronous catalog reconciliation for reusable platform knowledge.

Four orders remain separate because each host must be independently authorized, can fail independently, and requires a host-specific model/hardware/capability contract. hxs-1 supplies the method; it does not dictate the answer for hxs-2, hxs-3, or hxs-4.

## 4. Proposed hxs-1 parent objective

> Establish hxs-1 as the current, fully evidenced reference implementation for the Qwen-X Ollama service: audit the live host and the complete local Ollama knowledge corpus; identify gaps against current upstream, HX architecture, exact model support, and measured workload requirements; remediate only within approved boundaries; optimize the dual-GPU runtime; register a stable service FQDN; prove native, compatible, RAG, agent-tool, and discovery paths; complete reliability and rollback testing; and obtain independent qualification with no unresolved critical or high-severity finding.

### Proposed target identity

| Item | Historical or intended value | Treatment in this order |
| --- | --- | --- |
| Host | hxs-1, historically `192.168.50.200` | Verify live before any other probe; IP is evidence, not consumer configuration |
| Host FQDN | `hxs-1.hx.local.arpa` | Verify as host identity |
| Service call-sign | Qwen-X | Preserve unless owner changes fleet role |
| Recommended service FQDN | `qwen-x.hx.local.arpa` | **Owner decision required**; use a service alias distinct from host identity |
| Role | Deep reasoning and synthesis backend | Reconcile with current registry and consumers |
| GPUs | 2 × NVIDIA RTX 4070 Ti Super, historically 16,376 MiB each | Verify model, UUID, topology, driver, health, and workload placement live |
| Model family | Qwen 3.8 27B | Preserve exact artifact unless owner separately authorizes model replacement |
| Operating profile | Historical 64K alias `hx-qwen3.8-27b-64k` | Requalify; do not assume it remains optimal |
| Runtime | Ollama native systemd | Preserve architecture; no containers |
| Exposure | Private LAN, no service-layer auth | Preserve owner-authorized boundary; no host firewall |

## 5. Required phase gates

### Phase A — read-only audit and remediation design

No service, model, DNS, operating-system, or repository mutation is permitted in Phase A.

John must begin with the mandated live knowledge review of:

```text
/opt/tkv-local/ollama/
/opt/tkv-local/ollama/ollama-main/
```

The review must descend through all materially relevant subdirectories, including runtime/server code, API adapters, discovery, agent/tool support, integration fixtures, thinking, model management, documentation, launch/runtime configuration, GPU/cache logic, and archived HX evidence. The receipt must identify:

- filesystem type and mount/source identity;
- total directory/file counts;
- snapshot or commit identity when present;
- local snapshot Ollama version and its difference from both the installed version and current official upstream;
- specific files/directories used to derive each audit vector;
- contradictions, stale material, archived material, and unknowns;
- `Task May Proceed: YES/NO` before host probes begin.

John then performs the live hxs-1 audit, while Bailey defines tests and expected results before active qualification. Phase A produces a severity-ranked findings register and a proposed remediation plan. Every remediation item must state the evidence, exact change, expected benefit, risk, prerequisites, validation, rollback, owning lane, and whether it is authorized.

**Gate A:** James and Agent Zero review the findings, planned mutations, downtime, DNS alias, upgrade decision, and rollback. Phase B cannot begin on an inferred or open-ended scope.

### Phase B — bounded remediation and active qualification

Only Gate-A-approved changes may execute. Unknown OS, driver, DNS/router, storage, or network changes become separate Rick work orders rather than being folded into John's Ollama scope. The service is independently qualified after remediation and again after the soak window.

**Gate B:** Gordon verifies claims against live state from a different host where feasible. James runs the governor verification checklist; Carol reconciles authority and reusable platform knowledge before closure; Agent Zero alone accepts completion and authorizes any merge.

## 6. hxs-1 audit and qualification matrix

Every test receives `PASS`, `FAIL`, `BLOCKED`, or `NOT RUN` with evidence and limitations. “Installed,” “endpoint returned 200,” or “historically passed” is not sufficient qualification.

| Vector | Minimum evidence and acceptance intent |
| --- | --- |
| Authority and identity | Hostname/address gate; OS/kernel; machine identity; registry role; exact GPU UUIDs; installed CLI/server/API versions; binary path, hash, ownership, installer provenance, signed upstream asset; source snapshot version/commit; exact model tag, digest, size, quantization, capabilities, Modelfile, parameters, license |
| Service wiring | Full effective systemd unit and drop-ins; dedicated service identity; startup ordering; environment provenance; model-store path/permissions; enabled/active state; no duplicate services or shadow binaries; bounded shutdown/start/restart behavior |
| Network boundary | Effective bind, IPv4/IPv6 listeners, CORS/origins, proxy variables, LAN reachability, no unintended off-LAN path, no host firewall, no container proxy, no unapproved public or cloud route |
| DNS and discovery | Host FQDN and approved service FQDN resolve from the development/control host and at least two fleet consumers; `/api/version`, `/api/tags`, `/api/ps`, `/v1/models`, and health probes work through the service name; consumer configuration contains no raw host IP or host-name dependency |
| GPU and driver | Inventory, UUIDs, topology, PCIe link, compute mode, driver/runtime versions, kernel errors, Xid/OOM history, running processes, idle/load temperature and power; no unapproved competing workload |
| Model placement | Direct `/api/ps` plus GPU-process evidence under representative load; no CPU fallback; both GPUs used when the model/context requires distribution; actual split and VRAM headroom recorded. Equal GPU utilization is not required—measured optimal placement is |
| Context and memory | Re-test 32K recovery, 64K operating, and 128K extended profiles only if they remain required; prove actual effective context, prompt handling, truncation behavior, VRAM, latency, quality, and recovery at each rung |
| Cache | Cold/warm prefix reuse; cancelled/retried prefill behavior; time-to-first-token; prompt-eval work; stable restore behavior; K/V cache memory/quality comparison; evidence that client prompt construction does not defeat cache reuse |
| Concurrency and queue | Explicit `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, queue limit, request admission, backpressure, timeouts, cancellation, and recovery; serialized consumer contract verified if concurrency remains one |
| Performance | Machine-readable benchmark runs with prompt/input/output sizes; cold and warm TTFT; prompt and decode tokens/second; end-to-end latency; VRAM/RAM/CPU; power/temperature; errors; repeat count and variance; workload-representative long-context and tool cases |
| Reliability | Preload/readiness; exact alias and digest resident after boot; three cold reboots; service/process recovery; interrupted request; failed preload; disk/permission negative tests where safe; rollback drill; mandatory 24-hour soak with periodic health, residency, GPU, latency, error, and journal capture |
| Observability | Actionable service, model, version, digest, residency, queue, restart, latency, GPU memory/temperature/power, Xid/OOM/CPU-fallback, and preload state; use existing HX monitoring surfaces or recommendation-only output—do not create a new stack implicitly |
| Security and hygiene | Dedicated user; least-privilege model store; sanitized evidence; no secret content; no cloud model substitution; no `:cloud` models; request logging posture; minimum necessary CORS; current owner LAN boundary recorded explicitly |

## 7. Capability qualification contract

“Use Ollama's tools as much as possible” means the factory must evaluate every material feature, not blindly enable everything. Each capability is classified as `REQUIRED`, `QUALIFIED`, `UNSUPPORTED`, `NOT APPLICABLE`, or `OWNER-GATED` for the exact installed Ollama version and exact Qwen-X artifact.

| Capability | hxs-1 qualification requirement |
| --- | --- |
| Native text APIs | `/api/chat` and `/api/generate`, streaming and non-streaming, deterministic structured tasks, long text, cancellation, and error semantics |
| Text perception | Representative comprehension, extraction, classification, synthesis, conflicting-evidence, no-answer, and long-context tests |
| Thinking | Explicit `think` behavior, streaming reasoning separation, client handling, and quality/latency cost for the exact Qwen model |
| Structured outputs | JSON mode and enforced JSON Schema; valid, invalid, nested, optional, and refusal cases; downstream parser validation |
| Tool calling | Single tool, parallel tools, multi-turn agent loop, streaming tool calls, schema rejection, timeout, denial, malformed result, idempotency, loop-depth, and prompt-injection tests |
| Embeddings | Verify endpoint semantics with an approved embedding model if hxs-1 is intended to serve embeddings; otherwise mark model-local embeddings unsupported/not applicable and prove integration to the designated fleet embedding service |
| RAG | Real end-to-end path: representative corpus → approved embedding service → Qdrant/retrieval → Qwen-X generation → citations/source references; include relevant, irrelevant, conflicting, poisoned, duplicate, stale, and no-answer cases |
| OpenAI compatibility | `/v1/models`, `/v1/chat/completions`, `/v1/embeddings` where applicable, and non-stateful `/v1/responses`; streaming, tools, structured output, reasoning, errors, and timeouts through an actual HX consumer |
| Anthropic compatibility | Qualify only if supported by the selected Ollama version and required by an HX consumer; otherwise record unsupported/not applicable |
| Vision | Qualify only if the exact Qwen-X artifact declares and proves vision. Do not infer vision from Ollama runtime support or substitute a different model to make the row pass |
| Web search/cloud | Owner-gated. Reconcile the fleet web-search decision, credentials, egress, auditability, `OLLAMA_NO_CLOUD`, and prohibition on cloud-model substitution before enabling or claiming it |
| Model management | List/show/ps/version; exact alias and digest; safe create/copy only when authorized; pull provenance and rollback; no mutable `latest` dependency |
| Discovery | Service FQDN, native model listings, Second Brain capability record, OmniRoute registration where applicable, health/readiness, and successful discovery/use by at least one authorized factory consumer |

Current official Ollama documentation confirms native support for single, parallel, multi-turn, and streaming tool calls; embeddings for semantic search and RAG; JSON-schema structured outputs; thinking fields for supported models; vision for vision-capable models; and OpenAI-compatible endpoints. These runtime features remain conditional on the exact model and client integration and therefore require live qualification rather than documentation-only acceptance. See [Tool calling](https://docs.ollama.com/capabilities/tool-calling), [Embeddings](https://docs.ollama.com/capabilities/embeddings), [Structured outputs](https://docs.ollama.com/capabilities/structured-outputs), [Thinking](https://docs.ollama.com/capabilities/thinking), [Vision](https://docs.ollama.com/capabilities/vision), and [OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility).

## 8. Optimization questions the order must answer

1. Is the currently installed Ollama version still appropriate? The repository historically records hxs-1 at `0.32.15`; current official upstream is `0.33.2`, and `0.33.0` introduced material prefill/prefix-cache corrections. The order must compare source, changelog, security/behavioral risk, installer provenance, regression coverage, and deterministic rollback before recommending or performing an upgrade. See [official Ollama releases](https://github.com/ollama/ollama/releases).
2. Does the exact 27B artifact distribute optimally across both GPUs at the intended context? Ollama normally prefers one GPU when a model fits and distributes across GPUs when it does not. Both-GPU use must be proven under representative load, but equal utilization is not an acceptance condition. See [Ollama FAQ](https://docs.ollama.com/faq).
3. Is f16 still the best K/V cache choice? Official documentation states f16 is the precision default, q8_0 uses about half the memory with a small precision cost, and q4_0 uses about a quarter with more risk. The decision must be empirical for Qwen-X tasks and long context; memory savings alone cannot define “optimized.” See [Ollama FAQ](https://docs.ollama.com/faq).
4. Does Flash Attention operate on the selected backend/devices, and what measured memory/latency benefit does it provide?
5. Are the 32K/64K/128K profiles still the correct consumer contract, and do clients avoid overriding server-owned context?
6. Does the prompt construction used by real agents preserve reusable prefixes, or does volatile content destroy K/V-cache value?
7. Is preload genuinely ready rather than merely active, and does it assert the exact alias and digest after reboot?
8. Are queue limits, timeouts, cancellation, and retry behavior bounded for the serialized service?

## 9. Real integration requirements

### Service naming and routing

The consumer contract must use a stable service identity, not a machine identity or IP address. Recommended owner decision:

```text
Qwen-X service: qwen-x.hx.local.arpa
Host identity:   hxs-1.hx.local.arpa
Evidence-only:   192.168.50.200 (verify live)
```

DNS work belongs to Rick. Ollama and model configuration belong to John. OmniRoute registration belongs to Trinity. Catalog reconciliation belongs to Carol. James must not collapse these lanes into an Ollama-only mutation order.

### RAG

The historical BM25-lite synthetic harness remains a useful unit fixture but cannot satisfy the new RAG acceptance condition. The active qualification must use the intended HX components and a representative corpus, while respecting the current MCP deployment hold. A passing result must prove retrieval quality, source attribution, no-answer behavior, conflict handling, prompt-injection resistance, context budgeting, and failure propagation. John owns Qwen-X behavior; Raphael/Quinn own their systems and may be dispatched for read-only integration validation or separate authorized corrections.

### Agent tooling

At least one authorized factory consumer must discover Qwen-X through the approved route/FQDN and complete a bounded real tool loop. Start with safe read-only tools. The suite must distinguish:

- model emitted the correct tool request;
- harness validated and authorized it;
- tool executed or was denied correctly;
- result returned to the model;
- model produced a grounded final response;
- timeouts, malformed schemas, injection attempts, duplicate calls, and runaway loops were safely contained.

A canned tool-call JSON response is a unit test, not end-to-end agent-tool qualification.

## 10. Proposed success conditions

| ID | Acceptance condition | Required evidence | Verifier |
| --- | --- | --- | --- |
| SC-01 | Live TKV review precedes probes and identifies local snapshot/version/provenance | John knowledge receipt with `Task May Proceed` | James gate |
| SC-02 | All live identity sources reconcile or execution stops | Identity matrix, hashes, source comparison | James + Gordon |
| SC-03 | Historical M8 claims are re-proven or explicitly superseded | Historical-to-live reconciliation table | Gordon |
| SC-04 | Every audit vector and capability has an honest status and evidence | Audit and capability matrices | Gordon |
| SC-05 | Gate-A findings and remediation scope receive owner approval before mutation | Signed/recorded Gate-A decision | Agent Zero |
| SC-06 | Approved service FQDN resolves and works from required consumers; no raw IP remains in consumer configuration | DNS probes, config search, endpoint tests | Rick + Gordon |
| SC-07 | Exact model and intended contexts show no CPU fallback and measured optimal GPU placement | `/api/ps`, GPU telemetry, benchmark dataset | John + Gordon |
| SC-08 | Cache, context, queue, concurrency, preload, and timeout settings are evidence-optimized | Comparative benchmark and configuration rationale | Bailey + Gordon |
| SC-09 | Native text, streaming, thinking, structured output, and required compatibility APIs pass | Versioned capability suite | Bailey + Gordon |
| SC-10 | Single, parallel, multi-turn, and streaming tool use pass unit and real-harness tests | Tool transcripts and containment cases | Bailey + Gordon |
| SC-11 | Real RAG path passes retrieval, citation, conflict, no-answer, stale, and injection cases | End-to-end RAG evidence package | Bailey + Gordon |
| SC-12 | Discovery/catalog/routing use the call-sign and service FQDN consistently | Consumer proof and catalog/routing records | Trinity + Carol + Gordon |
| SC-13 | Service survives three cold reboots and returns the exact resident alias/digest within the recovery SLO | Boot-cycle evidence | Gordon |
| SC-14 | 24-hour soak completes with no unexplained restart, Xid, OOM, CPU fallback, digest drift, or critical latency/error regression | Soak log and summarized metrics | Gordon |
| SC-15 | Rollback is executable and tested at the smallest changed layer | Pre/post hashes, diffs, backups, rollback drill | Gordon |
| SC-16 | Evidence is complete, sanitized, cataloged, and independently reconciled to live state | Governor checklist + Carol receipt | James + Carol |
| SC-17 | Agent Zero records final acceptance; merge is not automatic | Owner decision record | Agent Zero |

No completion exception should be used for SC-11, SC-13, SC-14, or SC-15 unless Agent Zero makes a new, explicit, dated decision after reviewing the risk. The recommended default is that the 24-hour soak is mandatory for this requalification.

## 11. Agent lanes and responsibilities

| Lane | Responsibility |
| --- | --- |
| James | Intake, authority parsing, governed decomposition, immutable context/work-order hashes, evidence gate, escalation; no operational execution |
| Mia | Management, sequencing, dependency routing, owner checkpoints |
| John | Ollama corpus review, runtime/model audit, approved Ollama/model changes, tuning, evidence production |
| Rick | Host OS/systemd platform issues outside John's unit boundary; DNS/router/service FQDN; driver/kernel work only under separate explicit authority |
| Bailey | Test design before changes, fixtures, benchmark schema, capability/RAG/tool/reliability suites |
| Gordon | Independent live-state verification, regression qualification, soak and rollback acceptance |
| Trinity | OmniRoute/service routing integration if in scope |
| Raphael / Quinn | Real RAG and vector/retrieval integration within their own lanes; no implicit service mutation |
| Carol | Catalog disposition, reusable platform knowledge, endpoint/capability record reconciliation |

## 12. Authorization boundaries

### In scope after Gate A approval

- hxs-1 Ollama binary/service/unit/drop-ins and model aliases identified in the approved write set;
- exact Qwen-X model profile and approved model-store artifacts;
- approved service FQDN and corresponding HX registry/catalog/routing records through the correct lanes;
- bounded active inference, cache, GPU, context, tool, RAG, reboot, soak, and rollback tests;
- sanitized evidence and repository documentation required by the factory.

### Explicitly out of scope unless separately authorized

- replacing the Qwen-X model family or fleet role;
- GPU firmware, BIOS, kernel, driver, storage partition, or network redesign;
- containers or Ansible;
- host firewall installation or activation;
- public Internet exposure or new authentication gateway;
- training, fine-tuning, or model modification beyond approved Modelfile/profile aliases;
- deployment of MCP servers while the fleet MCP hold remains active;
- installing a complete RAG stack on hxs-1;
- cloud-model fallback or `:cloud` model use;
- secret content in commands, evidence, chat, repository, or logs.

### Stop conditions

Stop and escalate on target mismatch, authority conflict, unexpected service or binary, source/version contradiction, model digest drift, secret exposure, unsafe GPU/driver state, Xid/OOM/wedge, unplanned CPU fallback, off-LAN exposure, missing rollback, test result outside the authorized safety envelope, undeclared mutation, or evidence-integrity failure.

## 13. Required deliverables

James should require exact repository-relative destinations before dispatch. At minimum:

1. approved goal and program relationship to the next three host orders;
2. context packet and atomic work-order package(s);
3. John knowledge-review receipt;
4. pre-change read-only audit report and raw sanitized evidence with checksums;
5. capability matrix and benchmark/test plan written before mutation;
6. Gate-A owner decision and authorized write set;
7. remediation record with pre/post hashes and unified diffs;
8. machine-readable benchmark and soak datasets plus human summary;
9. real RAG and real agent-tool integration evidence;
10. DNS/FQDN, discovery, OmniRoute, and catalog reconciliation evidence;
11. reboot, recovery-SLO, rollback-drill, and 24-hour-soak reports;
12. Gordon independent qualification;
13. governor verification checklist receipt;
14. Carol catalog receipt for reusable platform and authority changes;
15. Agent Zero final acceptance record.

## 14. Decisions reserved for Agent Zero

James should present these as explicit owner choices rather than filling them silently:

1. **Service FQDN:** approve `qwen-x.hx.local.arpa` as the recommended stable service identity, or provide another alias.
2. **Upgrade authority:** authorize Phase A to assess the current signed Ollama release and let Gate A decide whether a pinned upgrade is allowed; no automatic latest-version upgrade.
3. **Downtime/test window:** authorize the bounded restarts, three cold reboots, active performance tests, rollback drill, and 24-hour soak defined by the accepted test plan.
4. **RAG integration boundary:** authorize read-only use of existing RAG/embedding/vector services for end-to-end validation; any correction to those services requires their own lane/order.
5. **Web search/cloud posture:** confirm whether Ollama web search is required, owner-gated, or excluded for Qwen-X; cloud model substitution remains prohibited.

### Recommended defaults

- Approve `qwen-x.hx.local.arpa`.
- Permit a pinned upgrade only after Gate-A evidence, authenticated installer/artifact verification, regression plan, and tested rollback.
- Require all three reboot cycles, rollback drill, and 24-hour soak; do not reuse the prior soak deferral.
- Permit read-only real RAG integration testing but no downstream service mutation under this order.
- Keep web search owner-gated until egress, credentials, audit, and `OLLAMA_NO_CLOUD` implications are explicitly reconciled.

## 15. James intake instruction

> Intake this as the first of four host-specific Ollama Fleet Requalification work orders. Preserve the owner intent and boundaries in this brief. Establish hxs-1/Qwen-X as the reference implementation, but do not inherit its historical M8 PASS as current truth. Decompose the work into a read-only Phase A audit with a hard Agent Zero gate, followed by only the bounded remediation and active qualification approved at that gate. Require John to perform the complete live `/opt/tkv-local/ollama/ollama-main` knowledge review before probes; require Bailey-authored tests before mutation; route DNS, OS, driver, RAG, routing, and catalog work through their correct lanes; require Gordon's independent live qualification; and do not close without the rollback drill, three cold reboots, 24-hour soak, real RAG path, real agent-tool path, service-FQDN discovery, governor receipt, Carol reconciliation, and Agent Zero's final acceptance. Return the proposed goal, milestones, agent routing, exact write sets, owner checkpoints, and work-order/context-packet package for approval before dispatch.

## 16. Evidence basis and limitations

### Repository evidence reviewed

- `AGENTS.md`; `servers/AGENTS.md`
- `agents/james/profile.md`
- `agents/john/profile.md`; `agents/john/charter.md`
- `agents/john/codex_20260824_0205_ollama-directory-reconnaissance-inventory.md`
- `servers/BLUEPRINT-llm-server.md`
- `servers/hxs-1/discovery.md`; `servers/hxs-1/configuration.md`
- `servers/system-mapping.md`; `SERVER-REGISTRY.md`
- `governace/goals/2026-08-24-hx1-ollama-qwen38-27b.md`
- `governace/goals/2026-08-24-ollama-audit-hxs4.md`
- `governace/decisions/KDD-0003-ollama-audit-pilot-adoption.md`
- `governace/decisions/KDD-0004-hx1-qwen-pilot-adoption.md`
- `pilots/PILOT-HX1-OLLAMA-QWEN27B-001/` planning and completion evidence
- `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-001/` and `002/` test plans/reports
- `knowledge/catalog/documents/DOC-backend-qwen-x.yaml`
- `governace/process/governor-verification-checklist.md`
- `pilots/_templates/work-order.yaml`

### Current upstream sources reviewed

- [Ollama releases](https://github.com/ollama/ollama/releases)
- [Ollama tool calling](https://docs.ollama.com/capabilities/tool-calling)
- [Ollama embeddings](https://docs.ollama.com/capabilities/embeddings)
- [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs)
- [Ollama thinking](https://docs.ollama.com/capabilities/thinking)
- [Ollama vision](https://docs.ollama.com/capabilities/vision)
- [Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility)
- [Ollama FAQ](https://docs.ollama.com/faq)

### Limitations

This intake was prepared from the available repository evidence and current official Ollama documentation. This Work Mode session did **not** directly inspect the present hxs-1 host or the live `/opt/tkv-local/ollama/ollama-main` filesystem. The prior Claude-agent implementation described by Agent Zero was not recovered as a current authoritative artifact, so its claimed behavior is treated as the owner's acceptance benchmark, not copied configuration. These limitations are intentional inputs to the work order: live state, live TKV identity, and current integration behavior must be established by the factory before any remediation or acceptance claim.

