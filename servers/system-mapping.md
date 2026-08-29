# HX System-to-Server Mapping

**Status:** CURRENT-STATE — reconciled against factory evidence as of 2026-08-29
**Authority:** This document maps systems to servers. `SERVER-REGISTRY.md` owns durable host identity and role. This document owns system placement.
**Predecessors:** `hxs3-workload-placement.md` (retired), `hx-ai-platform-target-architecture-2026-08-21.md` (retired, historical reference at `/home/hxsa/opt/local-tkv/agent-zero-docs/server-system-mapping/`), `hx-ai-platform-target-architecture-diagrams-2026-08-21.md` (retired, same location).

---

## The rule

```
THE SERVER OWNS CAPACITY.
THE SYSTEM IS A WORKLOAD.
```

A server's durable identity (assigned role) does not change when a system is
installed, removed, or swapped. Installation presence is not activation.
The registry assigns the role; this document records what runs there.

---

## MCP architecture decision (2026-08-29)

**Co-located MCP servers with FastMCP as discovery and routing layer.**

- Each system deploys with its own MCP server on the same host (co-located).
  Consumers connect directly to local MCP servers — one hop, no gateway
  bottleneck.
- FastMCP serves as the discovery and routing layer: consumers ask FastMCP
  "where is the Docling MCP server?" and connect directly.
- FastMCP proxies cloud/remote MCP servers that consumers can't reach
  directly (credentials, network, TLS handled by FastMCP's single outbound
  connection).
- FastMCP provides single-endpoint fallback for consumers (like LLMs)
  that can only talk to one MCP URL — it proxies to any MCP server, local
  or remote.

```
Consumer (app/LLM)
  ├── direct connection → local MCP servers (co-located with their systems)
  └── FastMCP (discovery + proxy)
       ├── discovery: "where is X?" → returns address, consumer connects directly
       └── proxy: cloud/remote MCP servers, or single-endpoint fallback
```

All MCP deployment is on HOLD per owner directive 2026-08-29. No MCP
deployment until the owner lifts the hold.

---

## System placement map

### Deployed — running in production, verified

| # | System | Server | Agent | Notes |
|---|---|---|---|---|
| S01 | Qwen-X (Qwen 3.8 27B) | hxs-1 | john | LLM server — deep reasoning & synthesis |
| S02 | Coder-X (Qwen 2.5 Coder 32B) | hxs-2 | john | LLM server — coding |
| S03 | Meta-X (Muse Glimmer 30B) | hxs-3 | john | LLM server — agent intelligence / tooling |
| S04 | Chat-X (Qwen 3.5 9B) | hxs-4 | john | LLM server — basic utility |
| S05 | OmniRoute | hxs-8 | trinity | Model traffic gateway; replaces LiteLLM |
| S06 | PostgreSQL (+MCP) | hxs-9 | chris | State services |
| S07 | Redis (+MCP) | hxs-9 | wayne | Cache + data plane |
| S08 | DeepSeek Harness (DSH) | hxs-15 | morpheus | Agent harness; Gates 6-7 in progress |

### Target-state — not yet deployed

| # | System | Server | Agent | Notes |
|---|---|---|---|---|
| S09 | Qdrant (+MCP) | hxs-4 | quinn | Co-locate with Chat-X; Qdrant on 477 GB NVMe |
| S10 | FastMCP | hxs-20 | sage (new) | MCP gateway — discovery, routing, cloud proxy |
| S11 | Open WebUI | hxs-10 | iris (new) | Web frontend (upgrade hxs-10 to 32 GB with RAM from hxs-8) |
| S12 | Crawl4AI (+MCP) | hxs-6 | scout (new) | Ingestion — crawling |
| S13 | Docling (+MCP) | hxs-12 | piper (new) | Ingestion — parsing |
| S14 | n8n (+MCP) | hxs-13 | ripple (new) | Automation |
| S15 | LangGraph | hxs-11 | erwin (new) | Agent runtime; deferred by implementation order; no LangGraph service live anywhere in fleet; hxs-6 has legacy /srv/LangGraph-Server-Deployment/ on foreign spare disk (2025-11-12, historical artifact, not the HX deployment) |
| S16 | NGINX | hxs-21 | nexus (new) | Reverse proxy / web edge |

### Development and test environments

| Environment | Server | Agent | Notes |
|---|---|---|---|
| Dev | hxs-14 | rick | Development environment |
| Test | hxs-21 | rick | Co-located with NGINX on hxs-21 |

### RAM reallocation

| Source | Current | After | Notes |
|---|---|---|---|
| hxs-8 | 48 GB (using 1.8 GB for OmniRoute) | 32 GB | Donate 16 GB to hxs-10 |
| hxs-10 | 16 GB | 32 GB | Receive 16 GB from hxs-8 |

### Horizontal agents (not host-bound)

| Agent | Lane type | Role |
|---|---|---|
| rob | horizontal | Full-stack agentic software engineering — uses dev/test environments |
| gordon | horizontal | Independent QA — qualifies on hxs-15 test environment |
| mia | horizontal | Chief of Staff — management, coordination, routing |
| carol | horizontal | Knowledge stewardship — catalog, no host |
| governor | horizontal | Factory governor — control plane, no host |

### Retired / superseded

| System | Replaced by | Notes |
|---|---|---|
| LiteLLM | OmniRoute (KDD-0008) | Owner: "we replaced hx_litellm with openrouter" |
| vLLM | Ollama | Owner decision 2026-08-21; Ollama is sole serving runtime |
| Mem0 | (retired from list) | Role absorbed by PostgreSQL, Redis, Qdrant, catalog; may return if needed |
| CopilotKit / AG-UI | (removed — SDK, not a server) | Lives inside app projects, not a standalone system |

---

## New agents to register

| Agent | Family | Lane type | System | Status |
|---|---|---|---|---|
| quinn | 3 (Platform Systems) | vertical | Qdrant | Registered (KDD-0017) |
| sage | 3 (Platform Systems) | vertical | FastMCP | New — to be registered |
| iris | 3 (Platform Systems) | vertical | Open WebUI | New — to be registered |
| scout | 3 (Platform Systems) | vertical | Crawl4AI | New — to be registered |
| piper | 3 (Platform Systems) | vertical | Docling | New — to be registered |
| ripple | 3 (Platform Systems) | vertical | n8n | New — to be registered |
| erwin | 3 (Platform Systems) | vertical | LangGraph | New — to be registered |
| nexus | 2 (Infra/Ops) | vertical | NGINX | New — to be registered |

---

## Placement principles

1. **The server owns capacity.** A system is a workload selected to run on a
   host when capacity and isolation requirements are met.
2. **Installation presence is not activation.** A system installed on a host
   is not "running" until its service is enabled, verified, and accepted.
3. **Host identity does not change when the workload changes.** The registry
   assigns the durable role; this document records what runs there.
4. **Coexistence is never assumed.** Multiple systems on one host must be
   capacity-tested together before concurrent operation is claimed.
5. **Runtime isolation.** A system must be removable without making the host
   unusable for another. Environment variables scoped to the runtime, never
   global. Model files separated by identity. Ports configurable and
   documented. Switching systems must not require rebuilding the host.
6. **No Docker/containers.** Native services on systemd (owner rule
   2026-08-27).
7. **No host firewalls.** The LAN (192.168.50.0/24) is the boundary (owner
   rule 2026-08-26). Services bind to the LAN interface as authorized.
8. **Model weights never enter Git.**
9. **MCP surfaces on HOLD** per owner directive 2026-08-29 — no MCP
   deployment until the owner lifts the hold.
10. **MCP servers are co-located** with their systems. FastMCP is the
    discovery and routing layer, not a proxy for local MCP traffic.
    FastMCP proxies cloud/remote MCP servers and provides single-endpoint
    fallback.

---

## Authority hierarchy for placement decisions

1. Owner (Agent Zero) current directive
2. SERVER-REGISTRY.md (durable host identity and role)
3. This document (system-to-server mapping)
4. Ratified KDDs and governance records
5. Discovery records (as-found evidence)
6. Target architecture docs (historical reference only)

---

## Cross-references

This document is the authoritative system-to-server mapping. The following
documents must reference it for traceability:

- `servers/SERVER-REGISTRY.md` — durable host identity and role (references
  this document for system placement)
- `AGENTS.md` — project governance (references this document for the fleet
  deployment map)
- `agents/README.md` — agent roster (references this document for agent-to-
  system assignments)
- `servers/BLUEPRINT-llm-server.md` — LLM server blueprint
- `knowledge/decisions/KDD-0016-agent-taxonomy-and-standard-template.md` —
  agent family taxonomy
- Agent profiles — each platform-system agent's profile references this
  document in its knowledge sources section

---

## Related documents

- `servers/SERVER-REGISTRY.md` — authoritative durable host identity and role
- `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` — PostgreSQL plan
- `servers/hxs-9/2026-08-29-redis-implementation-plan.md` — Redis plan
- `servers/BLUEPRINT-llm-server.md` — LLM server blueprint
- `knowledge/decisions/KDD-0008-trinity-omniroute-adoption.md` — OmniRoute replaces LiteLLM
- `knowledge/decisions/KDD-0016-agent-taxonomy-and-standard-template.md` — agent family taxonomy
- Historical reference (retired): `/home/hxsa/opt/local-tkv/agent-zero-docs/server-system-mapping/`
