# Qdrant Installation Evidence — hxs-4 (2026-08-29)

## Summary
Qdrant vector database v1.19.0 successfully installed, configured, and operational on hxs-4 (192.168.50.203) with Python client v1.19.0 and MCP server v0.8.1.

---

## V0: Pre-state Checkpoint
- **Host**: hxs-4 (192.168.50.203), Ubuntu 24.04
- **Disk**: 477 GB unallocated NVMe → partitioned as `/dev/nvme0n1p1`, mounted at `/var/lib/qdrant` (469 GB ext4)
- **Qdrant**: Not installed, port 6333 not listening
- **Python client**: Not installed
- **MCP server**: Not installed

---

## V1: Install + Version
- **Qdrant binary**: v1.19.0 (prebuilt x86_64 from GitHub releases)
- **Install path**: `/usr/local/bin/qdrant`
- **Service**: systemd unit `qdrant.service` enabled and active
- **Config**: `/etc/qdrant/config.yaml` (LAN bind 192.168.50.203:6333, API key auth, telemetry disabled, cluster disabled, static content enabled)
- **Storage**: `/var/lib/qdrant/storage` (collections), `/var/lib/qdrant/snapshots` (backups)
- **Python client**: `qdrant-client==1.19.0` via pip (works in user context)
- **MCP server**: `mcp-server-qdrant==0.8.1` via pipx at `/home/hxsa/.local/bin/mcp-server-qdrant`

**Evidence**:
```
$ qdrant --version
qdrant 1.19.0

$ systemctl status qdrant
● qdrant.service - Qdrant vector database server
     Active: active (running) since Sat 2026-08-29 12:14:13 UTC
```

---

## V2: Config Posture
- **Bind address**: 192.168.50.203 (LAN only, not 0.0.0.0)
- **Ports**: 6333 (HTTP), 6334 (gRPC), 6335 (P2P — disabled)
- **API key**: `1ac8d8a3d638e702b06677e71938c23e26c87a12b8f5c3e9db05991e24d1ad98` (configured)
- **TLS**: Disabled (enable_tls: false)
- **Telemetry**: Disabled (telemetry_disabled: true)
- **Cluster**: Disabled (enabled: false)
- **Static content**: Enabled (enable_static_content: true) — Web UI assets
  not yet installed (static dir empty; requires separate download)
- **Optimizers**: deleted_threshold 0.2, vacuum_min_vector_number 1000, indexing_threshold_kb 10000
- **WAL**: wal_capacity_mb 32, wal_segments_ahead 0

---

## V3: API Probe
- **Health endpoint**: `GET /healthz` → "healthz check passed"
- **Readiness endpoint**: `GET /readyz` → "all shards are ready"
- **Collections endpoint**: `GET /collections` → `{"result":{"collections":[{"name":"test_restore"}]},"status":"ok"}`
- **Root endpoint**: `GET /` → `{"title":"qdrant - vector search engine","version":"1.19.0","commit":"74f3e85b9473c62560006c043e13737ce6b48412"}`

All endpoints respond with API key authentication via `api-key` header.

---

## V4: Collection Lifecycle
**Test collection**: `test_snapshot` (created, used, deleted during testing)
**Restored collection**: `test_restore` (5 points, 128-dim vectors, Cosine distance)

Operations verified:
1. **Create collection**: `PUT /collections/test_snapshot` — success
2. **Upsert points**: 5 points with 128-dim vectors — success
3. **Search**: Vector similarity search — returns correct results with scores
4. **Scroll**: Point enumeration — returns all 5 points
5. **Delete collection**: `DELETE /collections/test_snapshot` — success
6. **Snapshot create**: `POST /collections/test_snapshot/snapshots` — creates `.snapshot` file in `/var/lib/qdrant/snapshots/test_snapshot/`
7. **Snapshot list**: `GET /collections/test_snapshot/snapshots` — lists available snapshots
8. **Snapshot restore**: `PUT /collections/test_restore/snapshots/recover` with `location: "file:///var/lib/qdrant/snapshots/test_snapshot/test_snapshot-444579343199916-2026-08-29-12-27-55.snapshot"` — success, 5 points restored
9. **Verify restored data**: Query returns all 5 points with correct IDs

---

## V5: Snapshot Backup + Restore
- **Snapshot location**: `/var/lib/qdrant/snapshots/test_snapshot/`
- **Snapshot files**: Multiple `.snapshot` files with `.checksum` companions
- **Restore method**: `file://` absolute URI required (relative paths fail with "relative URL without a base")
- **Restored collection**: `test_restore` — status green, 5 points, 128-dim Cosine vectors
- **Data integrity**: All 5 original points recovered with correct IDs and vectors

**Key finding**: The `recover_snapshot` API requires `file:///absolute/path/to/snapshot.snapshot` format.

---

## V6: Health Monitoring
- **Script**: `/usr/local/bin/qdrant-health` (executable, returns 0 on healthy)
- **Checks**: systemd service active, `/healthz` returns "passed", `/readyz` returns "ready", `/collections` returns status ok
- **Timer**: systemd timer `qdrant-health.timer` — runs every 5 minutes (OnBootSec=1min, OnUnitActiveSec=5min)
- **Service**: `qdrant-health.service` (oneshot, runs the health script)
- **Status**: Timer enabled and active, timer has fired (LAST/PASSED populated)

**Evidence**:
```
$ /usr/local/bin/qdrant-health
OK: Qdrant is healthy

$ systemctl list-timers | grep qdrant
-  Sat 2026-08-29 12:42:13 UTC  18ms ago qdrant-health.timer  qdrant-health.service
```

---

## MCP Server
- **Version**: 0.8.1 (installed via pipx)
- **Service**: `mcp-server-qdrant.service` (enabled, active)
- **Transport**: stdio (default)
- **Environment**:
  - `QDRANT_URL=http://192.168.50.203:6333`
  - `QDRANT_API_KEY=1ac8d8a3d638e702b06677e71938c23e26c87a12b8f5c3e9db05991e24d1ad98`
  - `COLLECTION_NAME=mcp_memory`
  - `EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2`
- **Tools exposed**: `qdrant-store`, `qdrant-find`
- **Read-only mode**: Not enabled (both tools available)

---

## Credentials (stored in `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`)
```dotenv
QDRANT_HOST=192.168.50.203
QDRANT_PORT=6333
QDRANT_API_KEY=1ac8d8a3d638e702b06677e71938c23e26c87a12b8f5c3e9db05991e24d1ad98
QDRANT_COLLECTION=default_collection
QDRANT_URL=http://192.168.50.203:6333
COLLECTION_NAME=mcp_memory
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

## Web UI
- **Status**: NOT SERVED — the prebuilt binary does not bundle the Web UI
  static files. The config has `enable_static_content: true` and
  `static_content_dir: /usr/local/share/qdrant/static/`, but the directory
  is empty. The Web UI assets must be downloaded separately from the
  [qdrant-web-ui releases](https://github.com/qdrant/qdrant-web-ui/releases)
  (v0.2.16) and extracted to the static content directory.
- **Access**: `http://192.168.50.203:6333/dashboard` — returns 404 until
  static files are installed.
- **Follow-up**: Download and extract web UI assets to
  `/usr/local/share/qdrant/static/` under a future work order.

---

## Verification Commands Run
All commands executed via SSH from hxs-5 (hxsa@192.168.50.204) to hxs-4 (hxsa@192.168.50.203) using askpass pattern with `HX_SSH_PASSWORD` from `.local.env`.

---

## V0–V6 Gate Results
| Gate | Status | Notes |
|------|--------|-------|
| V0: Pre-state | PASS | Documented above |
| V1: Install + Version | PASS | Qdrant 1.19.0, client 1.19.0, MCP 0.8.1 |
| V2: Config Posture | PASS | LAN bind, API key, TLS off, cluster off |
| V3: API Probe | PASS | healthz, readyz, collections all OK |
| V4: Collection Lifecycle | PASS | Create, upsert, search, delete, restore |
| V5: Snapshot Backup + Restore | PASS | file:// URI works, data verified |
| V6: Health Monitoring | PASS | Script + timer active, returns 0 |

**Overall**: ALL GATES PASS
