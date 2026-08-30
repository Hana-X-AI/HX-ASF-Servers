# HX Server Registry

Fleet-level source of truth for discovery status, manual role assignment, and Phase 2 status.

Imported from `/opt/tkv-local/servers/SERVER-REGISTRY.md` on 2026-08-24. One edit:
references to hook scripts that read this file at runtime were removed; they do not
exist in this repository.

## Truth-state labels for this document

- Hardware, storage, and GPU fields: `DISCOVERED`, as-found evidence dated 2026-08-13.
- Assigned Role and Workload / Model: `TARGET-STATE`, ratified by the owner on
  2026-08-13. Role-specific implementation is deferred to a later owner-authorized
  phase. [exception noted 2026-08-28, amended 2026-08-28: two classes of deviation
  from pure TARGET-STATE — (a) DEPLOYED and owner-accepted workloads: the cell is
  prefixed `CURRENT-STATE:` with acceptance date and the superseded target preserved
  as history (hxs-1: Qwen 3.8 27B, owner disposition 2026-08-27 #1; hxs-3: Meta-X
  tooling specialist, production ACTIVE 2026-08-27); (b) owner-advised ROLE changes:
  no deployment claim, the advisory is recorded inline (hxs-5: control plane,
  owner advisory 2026-08-27; hxs-7: replaced by hxs-20, same advisory)]
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
- **System placement** is recorded in `servers/system-mapping.md` — the
  authoritative mapping of systems to servers. This registry owns durable
  host identity and role; the system-mapping document owns which system
  runs on which host.

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
| hxs-1 | hxs-1.hx.local.arpa | 192.168.50.200 | Intel Core Ultra 9 285K, 24c/24t | 128 GB DDR5 non-ECC | 2x RTX 4070 Ti SUPER, 16376 MiB each, 32752 MiB total | 3.6 TB NVMe root; 3.6 TB NVMe + 7.3 TB SATA unallocated | COMPLETE | Deep reasoning & synthesis | CURRENT-STATE: Qwen 3.8 27B (`hx-qwen3.8-27b-64k`, deployed and owner-accepted per owner disposition 2026-08-27 #1; supersedes "unreleased, slot reserved" recorded 2026-08-13 — preserved as history) | READY |
| hxs-2 | hxs-2.hx.local.arpa | 192.168.50.201 | Intel Core i7-5960X, 8c/16t | 66 GB non-ECC | 2x RTX 5060 Ti, 16311 MiB each, 32622 MiB total | 3.6 TB NVMe root; 2x 596.2 GB SATA HDD unallocated | COMPLETE | Coding | Qwen2.5-Coder-32B, AWQ Int4, TP=2, max-model-len 16–24K | READY |
| hxs-3 | hxs-3.hx.local.arpa | 192.168.50.202 | Intel Core i7-5960X, 8c/16t | 66 GB non-ECC | 2x RTX 5060 Ti, 16311 MiB each, 32622 MiB total | 3.6 TB NVMe root; 1.8 TB SATA SSD unallocated | COMPLETE | Agent intelligence | CURRENT-STATE: Meta-X tooling specialist — Muse Glimmer 30B (`hx-muse-glimmer-64k`, production ACTIVE 2026-08-27), primary tool agent for the RAG pipeline (one-call-per-turn contract) | READY |
| hxs-4 | hxs-4.hx.local.arpa | 192.168.50.203 | Intel Core i7-14700F, 20c/28t | 32 GB DDR5 non-ECC | 1x RTX 5060 Ti 16311 MiB + 1x RTX 5060 8151 MiB, 24462 MiB total | 931.5 GB NVMe root; 476.9 GB NVMe unallocated | COMPLETE | Retrieval & AI utility | Qdrant + Web-UI; Qwen2.5-3B; BGE-M3 / Nomic embeddings and BGE-Reranker-v2-m3 via TEI or Infinity | READY |
| hxs-5 | hxs-5.hx.local.arpa | 192.168.50.204 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | Control plane (replaced hxs-cp per owner advisory 2026-08-27) | HX factory control plane (Kimi-K3 governor host) | READY |
| hxs-6 | hxs-6.hx.local.arpa | 192.168.50.205 | Intel Core i5-8500T, 6c/6t | 15.9 GB DDR4 non-ECC | none, Intel UHD 630 integrated only | 238.5 GB NVMe root + 238.5 GB NVMe data (ext4 hxs-6-data @ /srv/data; added 2026-08-28 WO-01/PILOT-HXS6-STORAGE-001 — supersedes as-found "238.5 GB NVMe root, sole device") | COMPLETE | Ingestion — crawling | Crawl4AI (+ MCP) | READY |
| hxs-7 | hxs-7.hx.local.arpa | 192.168.50.206 | Intel Core i5-8500T, 6c/6t | 15.9 GB DDR4 non-ECC, single channel | none, Intel UHD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | MCP services (REPLACED BY hxs-20 per owner advisory 2026-08-27 — hxs-20 ONLINE 2026-08-28, baseline-green) | FastMCP runtime + custom HX MCP servers | READY |
| hxs-8 | hxs-8.hx.local.arpa | 192.168.50.207 | Intel Core i5-9400T, 6c/6t | CURRENT-STATE: 48 GB DDR4 (32 GB Samsung + 16 GB Micron SODIMM, both channels, 2666 MT/s; 46 GiB visible to Linux) per the `servers/hxs-8/discovery.md` addendum 2026-08-27 — RAM was upgraded after the 2026-08-13 baseline; supersedes "16 GB DDR4 non-ECC, single channel" recorded 2026-08-13, preserved as history | none, Intel UHD 630 integrated only | 476.9 GB NVMe root, sole device | COMPLETE | API gateway & control | LiteLLM gateway, PostgreSQL-backed on hxs-9 | READY |
| hxs-9 | hxs-9.hx.local.arpa | 192.168.50.208 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | State services | PostgreSQL + Redis; LiteLLM database; LangGraph checkpoints | READY |
| hxs-10 | hxs-10.hx.local.arpa | 192.168.50.209 | Intel Core i5-7500, 4c/4t | 16 GB DDR4 non-ECC (owner disposition 2026-08-27 #5: current state is 16 GB, OS reads 15 GiB ≈ nominal 16 GB; supersedes the 32 GB recorded 2026-08-13 — two independent readings found 1×16 GB; DIMM topology not inferred; preserved as history) | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | Web application | Open WebUI; CopilotKit / AG-UI | READY |
| hxs-11 | hxs-11.hx.local.arpa | 192.168.50.210 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device, aftermarket | COMPLETE | Agent runtime | LangGraph; Mem0 — separate virtualenvs | READY |
| hxs-12 | hxs-12.hx.local.arpa | 192.168.50.211 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device | COMPLETE | Ingestion — parsing | Docling (+ MCP) | READY |
| hxs-13 | hxs-13.hx.local.arpa | 192.168.50.212 | Intel Core i5-6500, 4c/4t | 32 GB DDR4 non-ECC, 2133 MT/s | none, Intel HD 530 integrated only | 238.5 GB SATA SSD root, sole device | COMPLETE | Automation | n8n (+ MCP) | READY |
| hxs-14 | hxs-14.hx.local.arpa | 192.168.50.213 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device, aftermarket | COMPLETE | Development | Prompt engineering; LangGraph and client development | READY |
| hxs-15 | hxs-15.hx.local.arpa | 192.168.50.214 | Intel Core i5-7500, 4c/4t, no VT-x | 32 GB DDR4 non-ECC | none, Intel HD 630 integrated only | 238.5 GB NVMe root, sole device, aftermarket | COMPLETE | Test & integration | QA, regression, integration testing, benchmarks | READY |
| hxs-20 | hxs-20.hx.local.arpa | 192.168.50.220 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC (2×16 GB Samsung @2400, first live reading 2026-08-28) | none recorded (owner-supplied discovery carries no GPU evidence) | 238.5 GB NVMe root, sole device | COMPLETE (first live inventory 2026-08-28) | MCP services (replaces hxs-7 per owner advisory 2026-08-27) | FastMCP runtime + custom HX MCP servers (target) | READY (baseline-green 2026-08-28) |
| hxs-21 | hxs-21.hx.local.arpa | 192.168.50.21 | Intel Core i5-7500, 4c/4t | 32 GB DDR4 non-ECC (2×16 GB Hynix @2400, mixed revisions, first live reading 2026-08-28) | none recorded (owner-supplied discovery carries no GPU evidence) | 238.5 GB NVMe root, sole device | COMPLETE (first live inventory 2026-08-28) | Standby — designated future control-plane machine (owner advisory 2026-08-27: eventually replaces the hxs-5 machine) | none assigned yet | READY (baseline-green 2026-08-28) |

**Open correction — hxs-7 decommission (2026-08-28, labeled per the append-only
governance rule).** Owner disposition 2026-08-28: "there is no 7 any longer."
Effective 2026-08-28, hxs-7 is **DECOMMISSIONED**: no DNS record (FQDN
NXDOMAIN), no route to host; the MCP-services role recorded in its row above
was already replaced by hxs-20 (owner advisory 2026-08-27; ONLINE 2026-08-28,
baseline-green). The row above is preserved unchanged as the as-found and
as-assigned record; THIS correction is the operative lifecycle state. Fleet
active count: 16.

**Reconciliation note (2026-08-30, audit F1).** `servers/system-mapping.md` was
corrected the same day for three items that disagreed with this registry and with
primary evidence: the S06/S07 rows no longer read as owner-accepted (PostgreSQL
V6 timer-fired activation is still pending), the `(+MCP)` suffix is defined as a
placement contract rather than a deployment claim (MCP is on HOLD), and S17's LLM
binding is corrected from Meta-X/OmniRoute to local Ollama Chat-X. The hxs-8
memory cell in the table above was corrected here in the same pass. Both
documents are reconciled as of 2026-08-30.

**Open correction — hxs-8/hxs-9 stale target-state (2026-08-29, labeled per the
append-only governance rule).** The hxs-8 row's "LiteLLM gateway" and the hxs-9
row's "LiteLLM database; LangGraph checkpoints" are the 2026-08-13 target-state
and are STALE: LiteLLM was replaced by **OmniRoute** (KDD-0008 arc; hxs-8 runs
OmniRoute in production), and LangGraph belongs to hxs-11's row. Owner review
2026-08-29: "we replaced hx_litellm with openrouter." The rows above are
preserved unchanged as the as-assigned record; THIS correction is the current
reading. hxs-9's TARGET-STATE: PostgreSQL 18.6 + Redis 7.0.15 (installed per
KDD-0014 and `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md`;
acceptance of the full deployment is not yet recorded — state-log row 46 records
Step 2 as REPORTED BUT UNVERIFIED, and the Step 2 evidence doc's open correction
notes V6 timer-fired evidence is pending). LangGraph and LiteLLM are entirely
removed from hxs-9.

**Open correction — hxs-11 stale target-state (2026-08-29, labeled per the
append-only governance rule).** The hxs-11 row's "LangGraph; Mem0 — separate
virtualenvs" is the 2026-08-13 target-state and is STALE: Mem0 is retired from
the fleet (role absorbed by PostgreSQL, Redis, Qdrant, catalog per
system-mapping retired/superseded table). LangGraph remains a target-state
system assigned to hxs-11 (S15) but is DEFERRED by implementation order —
no LangGraph service is currently live anywhere in the fleet. Owner agent:
erwin (new, not yet registered). The row above is preserved unchanged as the
as-assigned record; THIS correction is the current reading.

**Open correction — hxs-14 stale target-state (2026-08-29, labeled per the
append-only governance rule).** The hxs-14 row's "Prompt engineering; LangGraph
and client development" is the 2026-08-13 target-state and is STALE: hxs-14 is
the Dev environment (per system-mapping); LangGraph runtime belongs to hxs-11
(S15, deferred), not hxs-14. The row above is preserved unchanged as the
as-assigned record; THIS correction is the current reading.

## Role assignment record — historical

Roles were assigned by the project owner on 2026-08-13, ratifying the mapping in
`governance/fleet-architecture-v0.3.html` (source repository). This registry records
that decision; it did not make it. `hxs-cp` was the control plane, deliberately outside
the fifteen-server fleet, and held no row here; **hxs-5 replaced hxs-cp as the control
plane per owner advisory 2026-08-27** (and hxs-21, ONLINE 2026-08-28 at 192.168.50.21,
is being provisioned to eventually replace the hxs-5 machine).

**Addressing note (2026-08-28):** the `.199+N` pattern does NOT hold for the two new
hosts — hxs-20 lives at 192.168.50.220 (on-host hostname `hx-20`) and hxs-21 at
192.168.50.21 (outside the .200–.214 block). Verified live by rick's 2026-08-28
baseline wave. **Router DNS repaired 2026-08-28 (owner):** `hxs-21.hx.local.arpa`
and `hxs-20.hx.local.arpa` resolve correctly (verified); `hx-20.hx.local.arpa` does
NOT resolve — the canonical FQDN for hxs-20 is `hxs-20.hx.local.arpa` regardless of
the on-host hostname.

**Open correction — system-mapping reconciliation (2026-08-29, labeled per the
append-only governance rule).** The `servers/system-mapping.md` document
(ratified 2026-08-29) reconciles system-to-server assignments against current
factory evidence. The following registry rows are updated by that mapping.
Original rows are preserved unchanged above; THIS correction is the current
reading:

| Server | Registry says (stale) | System-mapping says (current) | Agent |
|---|---|---|---|
| hxs-4 | "Qdrant + Web-UI; Qwen2.5-3B; BGE-M3/Nomic embeddings" | Chat-X (Qwen 3.5 9B) deployed; Qdrant (+MCP) to co-locate (target-state, KDD-0017) — LightRAG and embeddings excluded from Quinn's scope per owner 2026-08-29 | john (LLM), quinn (Qdrant) |
| hxs-8 | "LiteLLM gateway" (already corrected above) | OmniRoute (deployed); RAM to be reduced 48→32 GB (donate 16 GB to hxs-10) | trinity |
| hxs-9 | "PostgreSQL + Redis; LiteLLM database; LangGraph checkpoints" (already corrected above) | PostgreSQL 18.6 + Redis 7.0.15 (both deployed); LiteLLM and LangGraph removed | chris, wayne |
| hxs-10 | "Open WebUI; CopilotKit / AG-UI" | Open WebUI (target-state); CopilotKit/AG-UI removed (SDK, not a server); RAM to be upgraded 16→32 GB | iris (new) |
| hxs-11 | "LangGraph; Mem0" | LangGraph (target-state, deferred); Mem0 retired | erwin (new) |
| hxs-14 | "Prompt engineering; LangGraph and client development" | Dev environment | rick |
| hxs-20 | "FastMCP runtime + custom HX MCP servers (target)" | FastMCP (target-state) — MCP gateway | sage (new) |
| hxs-21 | "Standby — designated future control-plane machine" | NGINX (target-state) + Test environment | nexus (new), rick (test) |

New agents to register per system-mapping: quinn, sage, iris, scout, piper,
ripple, erwin, nexus. See `servers/system-mapping.md` for the complete
mapping and `agents/_template/` + KDD-0016 for the standard profile/charter
template.

Phase 1 (discovery): COMPLETE, verified 2026-08-13 — 15 of 15 records accepted
(historical baseline scope: the original fifteen-server fleet). Current registry:
**17 rows accepted** — hxs-20 and hxs-21 added 2026-08-28 after rick's first live
inventory (baseline-green; their discovery records cataloged as DOC-hxs20-discovery
and DOC-hxs21-discovery). [Correction appended 2026-08-28, labeled: of the 17
accepted rows, hxs-7 is DECOMMISSIONED per the open correction above — **16
active rows**; the accepted-row count is preserved as acceptance history.]
Phase 2 (consolidation): READY.

## Verification — 2026-08-28 (DISCOVERED, post-outage FQDN census)

Checked from hxs-5 (192.168.50.204) after the 2026-08-28 power event and the
owner's router DNS loader re-run:

- FQDN: 16 names resolve via 192.168.50.1 — hxs-1..6, hxs-8..15, hxs-20
  (.220), hxs-21 (.21). **hxs-7 has no record (NXDOMAIN)** — consistent with
  decommission.
- Ping: all 16 registered hosts respond. One live UNREGISTERED address:
  **192.168.50.10** — no DNS record (forward or reverse), TCP 22/80/443
  closed; unidentified device, reported for owner identification, not probed
  further.
- Total fleet count of record: **16 active servers**.

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
