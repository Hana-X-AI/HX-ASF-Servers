# hxs-4 — Qdrant Configuration

**Configuration date:** 2026-08-29
**Agent lane:** quinn (Qdrant, KDD-0017)
**Status:** Operational (V0-V6 PASS)

## Functional role

Qdrant provides vector similarity search, collection lifecycle
management, and snapshot/restore for the factory. It serves as the
vector backend for LightRAG and supports factory-wide semantic
search workloads.

## Technical configuration

| Property | Value |
| --- | --- |
| Software | Qdrant v1.19.0 (prebuilt x86_64 binary) |
| Binary path | `/usr/local/bin/qdrant` |
| Config file | `/etc/qdrant/config.yaml` |
| Port | 6333 (HTTP) |
| Bind address | `192.168.50.203` (LAN only) |
| Service | `qdrant.service` (systemd, enabled + active) |
| Python client | `qdrant-client==1.19.0` (pip) |
| MCP server | `mcp-server-qdrant==0.8.1` (pipx, stdio transport) |

## Storage

| Property | Value |
| --- | --- |
| Device | 477 GB NVMe (`/dev/nvme0n1p1`, ext4, 469 GB usable) |
| Storage path | `/var/lib/qdrant/storage` |
| Snapshots path | `/var/lib/qdrant/snapshots` |
| Mount | `/var/lib/qdrant` (fstab entry by UUID) |

## Authentication and security

- API key auth (`api-key` header) — key stored in `.local.env`, never in repo
- TLS disabled — LAN-only, accepted risk (no host firewall per owner rule
  2026-08-26; API key transmitted over plaintext HTTP)
- Telemetry disabled
- If a TLS-terminating proxy is deployed later, switch all client URLs to
  https:// and enable `service.enable_tls`

## Web UI

- Version: v0.2.16 (static assets downloaded separately from
  [qdrant-web-ui releases](https://github.com/qdrant/qdrant-web-ui/releases))
- Static content dir: `/usr/local/share/qdrant/static/`
- Access: `http://192.168.50.203:6333/dashboard`

## Collections

| Collection | Purpose | Created by |
| --- | --- | --- |
| `lightrag_vdb_entities_bge_m3_1024d` | LightRAG entity vectors | LightRAG |
| `lightrag_vdb_chunks_bge_m3_1024d` | LightRAG chunk vectors | LightRAG |
| `lightrag_vdb_relationships_bge_m3_1024d` | LightRAG relationship vectors | LightRAG |
| `test_restore` | Snapshot restore test artifact (retained) | Quinn |

## Health monitoring

- Script: `/usr/local/bin/qdrant-health` (checks service active,
  `/healthz`, `/readyz`, `/collections`)
- Timer: `qdrant-health.timer` — every 5 min (OnBootSec=1min,
  OnUnitActiveSec=5min)
- Service: `qdrant-health.service` (oneshot)

## Dependencies

- **None** — Qdrant is standalone. It does not depend on any other
  factory service. LightRAG depends on Qdrant, not the reverse.

## Disabled features

| Feature | Status | Reason |
| --- | --- | --- |
| Cluster mode | Disabled | Standalone deployment — no cluster needed |
| TLS | Disabled | LAN-only, accepted risk (owner rule: no host firewall) |
| gRPC (port 6334) | Optional | Available but not required for current workloads |

## Discovery reference

```text
servers/hxs-4/discovery.md
```

As-found record dated 2026-08-12; preserved unchanged. Do not
modify the discovery record.

## Sources

- `servers/hxs-4/2026-08-29-qdrant-install-evidence.md`
- `servers/hxs-4/2026-08-29-qdrant-implementation-plan.md`
- `servers/hxs-4/discovery.md`
- `governace/decisions/KDD-0017-quinn-registration.md`
- `servers/system-mapping.md` (S09: Qdrant on hxs-4)
