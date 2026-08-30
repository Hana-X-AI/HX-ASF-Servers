# Qdrant Implementation Plan — hxs-4

## Verdict

Install Qdrant server v1.19.0 (prebuilt binary), Python client v1.19.0 (pip), and MCP server v0.8.1 (uv/pip) on hxs-4 as native systemd services. Standalone mode, no cluster. MCP co-located per system-mapping decision. Target: 477 GB unallocated NVMe for storage, LAN-bound API with API key auth.

## Evidence base

| Source | Path | Version | Role |
|---|---|---|---|
| Qdrant server source | `/opt/tkv-local/qdrant-master` | v1.15.5 (vault ref, Rust, Apache-2.0) — **install v1.19.0** (latest, Aug 2026, GitHub releases) | Server binary, config reference, OpenAPI spec |
| Qdrant Web UI | GitHub releases (separate) | v0.2.16 | Static assets downloaded separately and placed in static_content_dir; served at /dashboard |
| Qdrant Python client | `/opt/tkv-local/qdrant-client-master` | v1.15.1 (vault ref) — **install v1.19.0** (latest, GitHub releases) | Client library for consumers |
| MCP server for Qdrant | `/opt/tkv-local/mcp-server-qdrant-master` | v0.8.1 (latest, confirmed on GitHub) | Semantic memory layer, store/find tools |
| hxs-4 discovery | `servers/hxs-4/discovery.md` | 2026-08-12 | Hardware, GPU, storage, network |
| System mapping | `servers/system-mapping.md` | 2026-08-29 | S09: Qdrant (+MCP) on hxs-4 |
| Quinn profile | `agents/quinn/profile.md` | KDD-0017 | Agent scope: server, client, MCP — profile references vault v1.15.5/v1.15.1; plan updates to v1.19.0 for install |
| Governance | `AGENTS.md` | current | No Docker, no host firewall, native systemd |

## Target host: hxs-4 (192.168.50.203)

- CPU: Intel i7-14700F, 20 cores, x86_64
- RAM: 32 GB DDR5
- GPU 1: PNY 16 GB VRAM (Chat-X / Qwen 3.5 9B — already deployed)
- GPU 2: MSI 8 GB VRAM (idle — not Quinn's scope)
- Storage: 931 GB NVMe (root, 1.2% used) + **477 GB NVMe (unallocated, no filesystem)**
- Network: 1 Gb/s copper, 192.168.50.203
- OS: Ubuntu Server (kernel per discovery)
- Secure Boot: disabled (owner directive)

## Plan

### Step 0 — Pre-state verification (V0)

1. SSH to hxs-4 as `hxsa` (askpass pattern, grep-only credential extraction from `.local.env`)
2. Confirm: no Qdrant running, no port 6333 listener, no `/etc/qdrant` directory
3. Confirm: 477 GB NVMe (`/dev/nvme1n1`) still unallocated
4. Record: `hostname`, `uname -r`, `free -h`, `lsblk`, `ss -tlnp | grep 6333`
5. **STOP** — present V0 evidence to the governor for go/no-go

### Step 1 — Prepare storage and install Qdrant server (V1–V2)

**1a. Partition and mount the 477 GB NVMe:**
- **Revalidate the device before touching it.** Confirm `/dev/nvme1n1`
  matches the discovery record by serial (ADATA LEGEND 700, serial
  `4O4020822989`), size (476.9 GB), partition table (none), filesystem
  (none), and mount state (not mounted). Abort on any mismatch:
  ```bash
  lsblk -b -o NAME,SERIAL,MODEL,SIZE,FSTYPE,MOUNTPOINTS /dev/nvme1n1
  # Verify: SERIAL=4O4020822989, MODEL=ADATA LEGEND 700, SIZE~476.9G,
  # FSTYPE empty, MOUNTPOINTS empty
  ```
- Create single partition on `/dev/nvme1n1`
- Format ext4: `mkfs.ext4 /dev/nvme1n1p1`
- Mount at `/var/lib/qdrant`: create mount point, add fstab entry (by UUID)
- Create subdirectories: `storage/`, `snapshots/`
- Set ownership: `chown -R qdrant:qdrant /var/lib/qdrant` (after user creation)

**1b. Create qdrant system user:**
- `useradd -r -s /usr/sbin/nologin -d /var/lib/qdrant qdrant`
- No login shell, no sudo

**1c. Download prebuilt binary:**
- Qdrant publishes prebuilt x86_64 Linux binaries on GitHub releases
- Download `qdrant-x86_64-unknown-linux-gnu.tar.gz` for v1.19.0 from GitHub releases
- Verify checksum (SHA-256 from the release page)
- Extract to `/usr/local/bin/qdrant`
- `chmod 0755 /usr/local/bin/qdrant`
- Verify: `/usr/local/bin/qdrant --version` → 1.19.0

**1d. Create config:**
- Copy `/opt/tkv-local/qdrant-master/config/config.yaml` to `/etc/qdrant/config.yaml`
- Edit:
  - `storage.storage_path: /var/lib/qdrant/storage`
  - `storage.snapshots_path: /var/lib/qdrant/snapshots`
  - `service.host: 192.168.50.203` (LAN bind, not 0.0.0.0)
  - `service.http_port: 6333`
  - `service.enable_tls: false` (LAN-only, no host firewall per owner
    rule; API key transmitted over plaintext HTTP — accepted risk for
    dev/test LAN, documented here per Qdrant's TLS recommendation. If a
    TLS-terminating proxy (e.g. NGINX on hxs-21) is deployed later, switch
    all client URLs to https:// and enable `service.enable_tls` or proxy
    TLS termination)
  - `service.api_key: <generated>` (API key auth, not no-auth)
  - `cluster.enabled: false` (standalone)
  - `telemetry_disabled: true`
- `chmod 0640 /etc/qdrant/config.yaml`, `chown qdrant:qdrant`
- **Never** put the API key in the repo — write it to `.local.env`

**1e. Create systemd unit:**
```ini
[Unit]
Description=Qdrant vector database server
After=network.target

[Service]
Type=simple
User=qdrant
Group=qdrant
ExecStart=/usr/local/bin/qdrant --config-path /etc/qdrant/config.yaml
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

**1f. Web UI (separate download, v0.2.16):**
- The prebuilt Qdrant binary does NOT bundle the Web UI static files
- Download the web UI assets from `qdrant-web-ui` v0.2.16 GitHub releases
- Extract to the `static_content_dir` path (`/usr/local/share/qdrant/static/`)
- Config in `/etc/qdrant/config.yaml`:
  - `service.enable_static_content: true` (default — already on)
  - `service.static_content_dir: /usr/local/share/qdrant/static`
- Web UI accessible at `http://192.168.50.203:6333/dashboard` after assets installed
- Until assets are installed, `/dashboard` returns 404

**1g. Start and verify:**
- `systemctl status qdrant` — active, running
- `/usr/local/bin/qdrant --version` — 1.19.0
- `ss -tlnp | grep 6333` — listening on 192.168.50.203:6333

**V2 — Config posture check:**
- `curl -s http://192.168.50.203:6333/` — health endpoint
- `curl -s http://192.168.50.203:6333/readyz` — ready
- `curl -s -H "api-key: <key>" http://192.168.50.203:6333/collections` — empty list, no auth error
- `curl -s http://192.168.50.203:6333/collections` (without key) — 403
- `curl -s http://192.168.50.203:6333/dashboard | head -5` — web UI HTML served (after assets installed; 404 until then)

### Step 2 — Install Python client (V3)

**2a. Install:**
- `pip install qdrant-client==1.19.0` (system-wide or venv per owner preference)
- Verify: `python3 -c "from qdrant_client import QdrantClient; print('OK')"`

**2b. API probe:**
- `python3 -c "from qdrant_client import QdrantClient; c = QdrantClient('http://192.168.50.203:6333', api_key='<key>'); print(c.get_collections())"` — returns empty list

**V3 — API probe PASS:**
- Collections list endpoint works with API key
- Health and readyz respond
- No-auth requests rejected

### Step 3 — Collection lifecycle test (V4)

- Create a test collection: `c.create_collection("test_collection", vectors_config=...)`
- Upsert points: `c.upsert(collection_name="test_collection", points=[...])`
- Search: `c.query_points(collection_name="test_collection", query=[...], limit=3)` then access `result.points` (v1.19.0 — `search()` is deprecated)
- Delete collection: `c.delete_collection("test_collection")`
- Verify clean state: `c.get_collections()` — empty

**V4 — Collection lifecycle PASS:**
- Create, upsert, search, delete all work
- No residual test data

### Step 4 — Snapshot backup and restore (V5)

- Create snapshot: `curl -X POST -H "api-key: <key>" http://192.168.50.203:6333/snapshots`
- List snapshots: `curl -H "api-key: <key>" http://192.168.50.203:6333/snapshots`
- Restore full-storage snapshot: stop Qdrant, restart with
  `qdrant --config-path /etc/qdrant/config.yaml --storage-snapshot /var/lib/qdrant/snapshots/<name>.snapshot`,
  then verify data. For collection-level snapshots, use
  `PUT /collections/{collection_name}/snapshots/recover` (not the
  invalid `/snapshots/<name>/restore` endpoint)
- Verify data restored matches pre-snapshot state

**V5 — Snapshot backup + restore PASS:**
- Snapshot created, listed, restored, verified

### Step 5 — Health monitoring (V6)

- Create health check script at `/usr/local/bin/hx-qdrant-health.sh`:
  ```bash
  #!/bin/bash
  curl -sf --connect-timeout 5 --max-time 10 http://192.168.50.203:6333/readyz > /dev/null || exit 1
  exit 0
  ```
- Create systemd service: `qdrant-health.service` (oneshot, runs health script):
  ```ini
  [Service]
  Type=oneshot
  ExecStart=/usr/local/bin/hx-qdrant-health.sh
  TimeoutStartSec=30
  ```
- Create systemd timer: `qdrant-health.timer` (every 15 min)
- Enable and start timer

**V6 — Health monitoring PASS:**
- Timer active, health script exits 0

### Step 6 — Install MCP server

**6a. Install:**
- `pip install mcp-server-qdrant==0.8.1` (or `uvx mcp-server-qdrant`)
- Verify: `mcp-server-qdrant --help`

**6b. Configure environment:**
- MCP server connects to Qdrant via env vars
- Add to `.local.env`:
  ```dotenv
  QDRANT_URL=http://192.168.50.203:6333
  QDRANT_API_KEY=<same as server>
  COLLECTION_NAME=mcp_memory
  EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
  ```

**6c. Create systemd unit for MCP server (streamable-http transport):**
```ini
[Unit]
Description=MCP server for Qdrant (semantic memory layer)
After=network.target qdrant.service

[Service]
Type=simple
User=qdrant
Group=qdrant
EnvironmentFile=/etc/qdrant/mcp.env
ExecStart=/usr/local/bin/mcp-server-qdrant --transport streamable-http
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```
- Create `/etc/qdrant/mcp.env` with the MCP env vars (chmod 0640, chown qdrant:qdrant)
- Bind to 127.0.0.1:8000 (localhost only — consumers connect via localhost or FastMCP proxy)

**6d. Start and verify:**
- `systemctl daemon-reload && systemctl enable mcp-server-qdrant && systemctl start mcp-server-qdrant`
- `systemctl status mcp-server-qdrant` — active
- Test: `curl -s http://127.0.0.1:8000/` — MCP server responds

### Step 7 — Credentials

Write all credentials to `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`:
```dotenv
QDRANT_HOST=192.168.50.203
QDRANT_PORT=6333
QDRANT_API_KEY=<generated by openssl rand -hex 32>
QDRANT_COLLECTION=<default collection name>
QDRANT_URL=http://192.168.50.203:6333
COLLECTION_NAME=mcp_memory
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```
- Never print, log, or commit values
- Variable references only in repo files

### Step 8 — Evidence and validation

- Record all commands used (never credential values)
- Record service status, collection state, snapshot status
- Run `python3 scripts/validate.py` — must be **5/5 PASS** (5 checks since 2026-08-30: the governance-path check SY-2/SY-3 was added; this plan originally read 4/4)
- Render any manifest-listed .md changed
- Write evidence doc to `servers/hxs-4/2026-08-29-qdrant-install-evidence.md`

## Validation summary (V0–V6)

| Gate | What | Pass criteria |
|---|---|---|
| V0 | Pre-state | No Qdrant running, NVMe unallocated, disk free |
| V1 | Install + version | Binary v1.19.0, service active |
| V2 | Config posture | Bind 192.168.50.203:6333, API key set, no-auth rejected, web UI at /dashboard (after assets installed) |
| V3 | API probe | Health, readyz, collections list with key |
| V4 | Collection lifecycle | Create, upsert, search, delete — clean |
| V5 | Snapshot backup + restore | Create, list, restore, verify data |
| V6 | Health monitoring | Timer active, health script exit 0 |

## Governance compliance

- Native systemd only (no Docker) — owner rule 2026-08-27
- No host firewall — owner rule 2026-08-26 (LAN is the boundary)
- Standalone mode, no cluster — no separate assignment
- API key auth required — no unauthenticated access
- Credentials in `.local.env` only — never in repo
- Quinn owns this stack (KDD-0017) — governor-issued work order required for execution
- MCP co-located per system-mapping MCP architecture decision

## Execution authority

This is a plan. Execution requires:
1. Governor-issued work order to Quinn
2. Quinn executes on hxs-4 with SSH credentials
3. Quinn halts at V0 checkpoint for governor go/no-go
4. Evidence doc produced after completion
5. Quinn's activation gate: instance implemented + credential entries + governor's word

## Sequencing

Steps 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8, with checkpoints at V0 (pre-state) and after V2 (config posture). Steps 6 (MCP) can run after step 1 completes.
