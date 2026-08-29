# Change Record: Qdrant Deployment on hxs-4

| Field | Value |
| --- | --- |
| Date | 2026-08-29 |
| Host | hxs-4 (192.168.50.203) |
| Change type | New service deployment (vector database) |
| Agent lane | quinn (Qdrant, KDD-0017) |
| Status | COMPLETE — Qdrant operational, V0-V6 PASS |

## What changed

Qdrant v1.19.0 deployed on hxs-4, providing vector similarity
search for LightRAG and the factory's semantic search workloads.

## Why

The factory needed a vector database to support LightRAG's
graph-based RAG pipeline and factory-wide semantic search. Qdrant
was selected as the vector backend per the system mapping
decision (S09: Qdrant on hxs-4).

## Before state

No vector database deployed. hxs-4 had a 477 GB unallocated NVMe
device available for storage.

## After state

| Property | Value |
| --- | --- |
| Software | Qdrant v1.19.0 (prebuilt x86_64 binary) |
| Binary path | `/usr/local/bin/qdrant` |
| Config | `/etc/qdrant/config.yaml` |
| Port | 6333 (HTTP) |
| Bind address | `192.168.50.203` (LAN only) |
| Service | `qdrant.service` (systemd, enabled + active) |
| Storage | `/var/lib/qdrant` on 477 GB NVMe (`/dev/nvme0n1p1`, ext4, 469 GB) |
| Snapshots | `/var/lib/qdrant/snapshots` |
| Auth | API key (stored in `.local.env`, `api-key` header) |
| TLS | Disabled (LAN-only, accepted risk — no host firewall per owner rule) |
| Cluster | Disabled (standalone mode) |
| Telemetry | Disabled |
| Web UI | v0.2.16, served at `/dashboard` (assets downloaded separately) |
| Python client | `qdrant-client==1.19.0` |
| MCP server | `mcp-server-qdrant==0.8.1` (stdio transport) |
| Health monitoring | `qdrant-health.timer` (every 5 min) |

## Verification

V0-V6 gates all PASS. Document lifecycle proven:

- **V3 API probe:** Health, readiness, and collections endpoints
  all respond correctly with API key auth.
- **V4 Collection lifecycle:** Create, upsert, search, scroll,
  delete — all verified with a test collection.
- **V5 Snapshot backup + restore:** Snapshot created, listed, and
  restored via `file:///` URI; data integrity verified (5 points
  recovered with correct IDs and vectors).

| Gate | Status |
| --- | --- |
| V0: Pre-state | PASS |
| V1: Install + Version | PASS |
| V2: Config posture | PASS |
| V3: API probe | PASS |
| V4: Collection lifecycle | PASS |
| V5: Snapshot backup + restore | PASS |
| V6: Health monitoring | PASS |

**Overall: ALL GATES PASS**

## Conclusion

Qdrant is operational on hxs-4. Quinn owns this stack (KDD-0017).
The API key is stored in `.local.env` — never in the repo. No
TLS, no cluster mode — standalone, LAN-bound, API-key-authenticated.

## Rollback

```bash
systemctl stop qdrant
systemctl disable qdrant
rm /usr/local/bin/qdrant
rm -rf /etc/qdrant
# Optionally unmount and remove the NVMe partition:
umount /var/lib/qdrant
# Remove fstab entry
```

## Sources

- `servers/hxs-4/2026-08-29-qdrant-install-evidence.md`
- `servers/hxs-4/2026-08-29-qdrant-implementation-plan.md`
- `servers/system-mapping.md` (S09: Qdrant on hxs-4)
- `agents/quinn/profile.md` (KDD-0017)
