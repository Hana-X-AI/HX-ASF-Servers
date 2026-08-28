# HX Server Registry

Fleet-level source of truth for discovery status, manual role assignment, and Phase 2 status.

Imported from `/opt/tkv-local/servers/SERVER-REGISTRY.md` on 2026-08-24. One edit:
references to hook scripts that read this file at runtime were removed; they do not
exist in this repository.

## Truth-state labels for this document

- Hardware, storage, and GPU fields: `DISCOVERED`, as-found evidence dated 2026-08-13.
- Assigned Role and Workload / Model: `TARGET-STATE`, ratified by the owner on
  2026-08-13. Role-specific implementation is deferred to a later owner-authorized
  phase.
- Reachability and DNS state: see the dated verification block at the bottom.

## Rules

- Add one row per discovered server.
- Hardware fields summarize `servers/<server>/discovery.md`.
- This registry is authoritative for assigned role, approved workload/model,
  discovery lifecycle status, and Phase 2 lifecycle status.
- Roles and workloads/models are entered only after manual review and approval.
- `configuration.md` copies approved role and workload/model values from this
  registry; it does not assign them.
- Agents must not assign roles automatically.
- Phase 2 means repository consolidation and alignment. Server implementation is a
  later owner-authorized phase; Phase 3 is Regroup & Reconciliation.

## Discovery Status Values

```text
IN PROGRESS - discovery is underway or not yet accepted
COMPLETE    - discovery is accepted for fleet comparison
BLOCKED     - discovery cannot complete until a recorded blocker is resolved
```

## Phase 2 Status Values

```text
BLOCKED     - Phase 2 has not been opened
READY       - Phase 2 is open; consolidation may proceed
IN PROGRESS - consolidation work has started
COMPLETE    - consolidation is complete and verified
```

## Registry

| Server | FQDN | IP  | CPU | RAM | GPU / VRAM | Primary Storage | Discovery | Assigned Role | Workload / Model | Phase 2 |
| ------ | ---- | --- | --- | --- | ---------- | --------------- | --------- | ------------- | ---------------- | ------- |
| hxs-1 | hxs-1.hx.local.arpa | 192.168.50.200 | Intel Core Ultra 9 285K, 24c/24t | 128 GB DDR5 non-ECC | 2x RTX 4070 Ti SUPER, 16376 MiB each, 32752 MiB total | 3.6 TB NVMe root; 3.6 TB NVMe + 7.3 TB SATA unallocated | COMPLETE | Deep reasoning & synthesis | Qwen 3.8 27B (`hx-qwen3.8-27b-64k`, deployed and owner-accepted per owner disposition 2026-08-27 #1; supersedes "unreleased, slot reserved" recorded 2026-08-13 — preserved as history) | READY |
| hxs-2 | hxs-2.hx.local.arpa | 192.168.50.201 | Intel Core i7-5960X, 8c/16t | 66 GB non-ECC | 2x RTX 5060 Ti, 16311 MiB each, 32622 MiB total | 3.6 TB NVMe root; 2x 596.2 GB SATA HDD unallocated | COMPLETE | Coding | Qwen2.5-Coder-32B, AWQ Int4, TP=2, max-model-len 16–24K | READY |
| hxs-3 | hxs-3.hx.local.arpa | 192.168.50.202 | Intel Core i7-5960X, 8c/16t | 66 GB non-ECC | 2x RTX 5060 Ti, 16311 MiB each, 32622 MiB total | 3.6 TB NVMe root; 1.8 TB SATA SSD unallocated | COMPLETE | Agent intelligence | Meta-X tooling specialist — Muse Glimmer 30B (`hx-muse-glimmer-64k`, production ACTIVE 2026-08-27), primary tool agent for the RAG pipeline (one-call-per-turn contract) | READY |
| hxs-4 | hxs-4.hx.local.arpa | 192.168.50.203 | Intel Core i7-14700F, 20c/28t | 32 GB DDR5 non-ECC | 1x RTX 5060 Ti 16311 MiB + 1x RTX 5060 8151 MiB, 24462 MiB total | 931.5 GB NVMe root; 476.9 GB NVMe unallocated | COMPLETE | Retrieval & AI utility | Qdrant + Web-UI; Qwen2.5-3B; BGE-M3 / Nomic embeddings and BGE-Reranker-v2-m3 via TEI or Infinity | READY |
| hxs-5 | hxs-5.hx.local.arpa | 192.168.50.204 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | Control plane (replaced hxs-cp per owner advisory 2026-08-27) | HX factory control plane (Kimi-K3 governor host) | READY |
| hxs-6 | hxs-6.hx.local.arpa | 192.168.50.205 | Intel Core i5-8500T, 6c/6t | 15.9 GB DDR4 non-ECC | none, Intel UHD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | Ingestion — crawling | Crawl4AI (+ MCP) | READY |
| hxs-7 | hxs-7.hx.local.arpa | 192.168.50.206 | Intel Core i5-8500T, 6c/6t | 15.9 GB DDR4 non-ECC, single channel | none, Intel UHD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | MCP services (REPLACED BY hxs-20 per owner advisory 2026-08-27 — hxs-20 currently being provisioned; no pre-work until ready) | FastMCP runtime + custom HX MCP servers | READY |
| hxs-8 | hxs-8.hx.local.arpa | 192.168.50.207 | Intel Core i5-9400T, 6c/6t | 16 GB DDR4 non-ECC, single channel | none, Intel UHD 630 integrated only | 476.9 GB NVMe root, sole device | COMPLETE | API gateway & control | LiteLLM gateway, PostgreSQL-backed on hxs-9 | READY |
| hxs-9 | hxs-9.hx.local.arpa | 192.168.50.208 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | State services | PostgreSQL + Redis; LiteLLM database; LangGraph checkpoints | READY |
| hxs-10 | hxs-10.hx.local.arpa | 192.168.50.209 | Intel Core i5-7500, 4c/4t | 16 GB DDR4 non-ECC (owner disposition 2026-08-27 #5: current state is 16 GB, OS reads 15 GiB ≈ nominal 16 GB; supersedes the 32 GB recorded 2026-08-13 — two independent readings found 1×16 GB; DIMM topology not inferred; preserved as history) | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | Web application | Open WebUI; CopilotKit / AG-UI | READY |
| hxs-11 | hxs-11.hx.local.arpa | 192.168.50.210 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device, aftermarket | COMPLETE | Agent runtime | LangGraph; Mem0 — separate virtualenvs | READY |
| hxs-12 | hxs-12.hx.local.arpa | 192.168.50.211 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | Ingestion — parsing | Docling (+ MCP) | READY |
| hxs-13 | hxs-13.hx.local.arpa | 192.168.50.212 | Intel Core i5-6500, 4c/4t | 32 GB DDR4 non-ECC, 2133 MT/s | none, Intel HD 530 integrated only | 238.5 GB SATA SSD root, sole device | COMPLETE | Automation | n8n (+ MCP) | READY |
| hxs-14 | hxs-14.hx.local.arpa | 192.168.50.213 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device, aftermarket | COMPLETE | Development | Prompt engineering; LangGraph and client development | READY |
| hxs-15 | hxs-15.hx.local.arpa | 192.168.50.214 | Intel Core i5-7500, 4c/4t, no VT-x | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device, aftermarket | COMPLETE | Test & integration | QA, regression, integration testing, benchmarks | READY |

## Role assignment record — historical

Roles were assigned by the project owner on 2026-08-13, ratifying the mapping in
`governance/fleet-architecture-v0.3.html` (source repository). This registry records
that decision; it did not make it. `hxs-cp` was the control plane, deliberately outside
the fifteen-server fleet, and held no row here; **hxs-5 replaced hxs-cp as the control
plane per owner advisory 2026-08-27** (and hxs-21 is being provisioned to eventually
replace the hxs-5 machine).

**Superseded assignment (hxs-3), dated 2026-08-27.** hxs-3's original workload target
was **gpt-oss / LightRAG** (the 2026-08-13 role mapping). That assignment was superseded
by owner decision: hxs-3 is now the **Meta-X tooling specialist** (Muse Glimmer 30B,
`hx-muse-glimmer-64k`, production ACTIVE 2026-08-27 — see the hxs-3 row). The gpt-oss/
LightRAG target is preserved here as history; it is no longer the current assignment.

Phase 1 (discovery): COMPLETE, verified 2026-08-13 — 15 of 15 records accepted.
Phase 2 (consolidation): READY.

## Verification — 2026-08-24 (DISCOVERED)

Checked from hxs-5 (192.168.50.204):

- Ping sweep 192.168.50.200–215: 14 of 16 addresses respond.
  **DOWN: 192.168.50.205 (hxs-6) and 192.168.50.206 (hxs-7).**
- DNS: `nslookup hxs-1.hx.local.arpa 192.168.50.1` returns NXDOMAIN. FQDN resolution
  is down following a router restart. Documented fix: re-run `/jffs/hx-dns-load.sh`
  on HX-Router (see `knowledge/network.md`). Use IP addresses until DNS is restored.
- Recheck 2026-08-24 06:51 UTC: hxs-6 (192.168.50.205) responds again. hxs-7
  (192.168.50.206) is still unreachable: ping 100% packet loss, TCP/22 "No route to
  host".
- Recheck 2026-08-24 06:55 UTC: hxs-7 responds on ping and TCP/22. All 16 addresses
  reachable; the interim failure was the host still coming up.
