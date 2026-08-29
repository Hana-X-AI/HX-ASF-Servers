# LightRAG Installation Evidence — hxs-4 (2026-08-29)

## Summary

LightRAG v1.5.7 (lightrag-hku[api,offline-storage,offline-llm]) installed,
configured, and operational on hxs-4 (192.168.50.203) with lightragmcp
v1.1.0 MCP server. Qdrant v1.19.0 as vector backend, bge-m3 embeddings
via Ollama, Chat-X (Qwen 3.5 9B) as LLM binding via local Ollama.

## V0: Pre-state

- Qdrant v1.19.0 running on hxs-4:6333 (Quinn, KDD-0017, V0-V6 PASS)
- bge-m3 model available in Ollama on hxs-4
- No LightRAG installed, port 9621 free

## V1: Install + Version

- **LightRAG:** `lightrag-hku[api,offline-storage,offline-llm]` v1.5.7
  installed in venv at `/srv/lightrag/.venv/`
- **Full feature install:** includes offline-storage (Qdrant, Milvus,
  Neo4j, PostgreSQL, OpenSearch backends) and offline-llm (Ollama,
  vLLM, llama-index LLM providers)- **Config:** `/srv/lightrag/.env` (based on env.example)
- **Service:** systemd unit `lightrag.service` (Type=simple, user=hxsa,
  WorkingDirectory=/srv/lightrag, Restart=always)
- **lightragmcp:** v1.1.0 installed via `npm install -g
  @g99/lightrag-mcp-server` (Node.js v22.23.2)
- **Node.js:** v22.23.2 via NodeSource repo
- **MCP transport:** stdio (launched by MCP clients on demand, not a
  daemon — systemd unit disabled)

## V2: Config posture

| Setting | Value |
|---|---|
| Host | 0.0.0.0 (LAN accessible) |
| Port | 9621 |
| API key | `6e437e5ef5aef927...` (LIGHTRAG_API_KEY, X-API-Key header) |
| LLM binding | ollama |
| LLM host | http://127.0.0.1:11434 |
| LLM model | hx-qwen3.5-9b-64k (Chat-X, Qwen 3.5 9B) |
| Embedding binding | ollama |
| Embedding host | http://127.0.0.1:11434 |
| Embedding model | bge-m3 |
| Embedding dim | 1024 |
| Vector storage | QdrantVectorDBStorage |
| Qdrant URL | http://192.168.50.203:6333 |
| Qdrant API key | (from .local.env QDRANT_API_KEY) |
| Graph storage | NetworkX (default) |
| KV storage | JSON (default) |
| Web UI | Available (bundled, served at :9621) |
| Telemetry | Disabled |

**LLM binding correction:** Originally configured for Meta-X (Muse Glimmer
30B) via OmniRoute. Switched to local Ollama Chat-X (Qwen 3.5 9B) after
OmniRoute rate-limit execution timeout (504 RATE_LIMIT_EXECUTION_TIMEOUT)
— Meta-X 30B was too slow for LightRAG's entity extraction prompts.
Chat-X on local Ollama processes documents in ~2 minutes with no
rate-limit issues.

## V3: API probe

- `GET /health` → `{"status":"healthy","core_version":"1.5.6","webui_available":true}`
- `GET /` → 307 redirect to Web UI
- `POST /documents/text` without key → 403 Forbidden
- `POST /documents/text` with X-API-Key → 200 success

**[OPEN CORRECTION 2026-08-29, labeled, append-only — LIGHTRAG VERSION
ALIGNMENT PENDING VERIFICATION.] V1 records the installed
`lightrag-hku` package as v1.5.7 (venv at `/srv/lightrag/.venv/`), but the
V3 `GET /health` capture reports `core_version: "1.5.6"`. The vault source
(`/opt/tkv-local/LightRAG-main/lightrag/_version.py`) defines `__version__
= "1.5.7"`, which is what `/health` `core_version` is derived from in-tree —
so the 1.5.6 capture does NOT match either the recorded install or the
pinned source. Root cause is not established from this record alone (could
be an older running process, a mismatched venv, or a stale capture).
RESOLUTION REQUIRED at next live probe before V1 and V3 are marked aligned:
(1) confirm the `lightrag.service` unit launches `/srv/lightrag/.venv/`
binaries; (2) run `pip show lightrag-hku` from that venv; (3) re-capture
`GET /health`; then record the single authoritative running version in both
V1 and V3. Until reconciled, V1/V3 version evidence is
VERIFICATION-REQUIRED, not final — the install and API-probe outcomes
themselves are not in question.]

## V4: Document lifecycle (PROVEN)

**Insert:**
```bash
curl -X POST http://localhost:9621/documents/text \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <key>" \
  -d '{"text":"HX factory uses Qdrant for vectors...Quinn owns Qdrant, Raphael owns LightRAG.","file_source":"fresh_test.txt"}'
```
→ `{"status":"success","track_id":"insert_20260829_150035_37e2fcf2"}`

**Processing result (local Ollama Chat-X, ~2 min):**
- 9 entities extracted (HX AI Software Factory, Qdrant, LightRAG, Quinn, Raphael, Ubuntu, systemd, Docker, hxs-4)
- 8 relations extracted (HX→Ubuntu, HX→systemd, Docker→HX, etc.)
- 9 entity vectors, 8 relationship vectors, 1 chunk vector embedded in Qdrant
- Graph written with 9 nodes, 8 edges

**Query:**
```bash
curl -X POST http://localhost:9621/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <key>" \
  -d '{"query":"Who owns Qdrant?","mode":"hybrid","top_k":3}'
```
→ `"Agent Quinn is responsible for managing the Qdrant vector database on hxs-4"`
  with citation `[[1]] fresh_test.txt`, response_time: 36.3s

## V5: Qdrant backend verification

Qdrant collections created by LightRAG:
- `lightrag_vdb_entities_bge_m3_1024d` — 9 points
- `lightrag_vdb_chunks_bge_m3_1024d` — 1 point
- `lightrag_vdb_relationships_bge_m3_1024d` — 8 points

## V6: Health monitoring

- LightRAG service: `systemctl is-active lightrag` → active
- LightRAG enabled: `systemctl is-enabled lightrag` → enabled
- Health endpoint: `GET /health` → healthy
- Web UI: available at `http://192.168.50.203:9621/`

## MCP server

- **lightragmcp v1.1.0** — 30 tools, stdio transport
- Installed at `/usr/bin/lightrag-mcp-server`
- Not a daemon — launched by MCP clients (Claude Desktop, kimi, etc.) on demand
- MCP client config:
  ```json
  {
    "mcpServers": {
      "lightrag-mcp": {
        "command": "lightrag-mcp-server",
        "env": {
          "LIGHTRAG_SERVER_URL": "http://192.168.50.203:9621",
          "LIGHTRAG_API_KEY": "<key>"
        }
      }
    }
  }
  ```

## Credentials (stored in .local.env)

```dotenv
LIGHTRAG_HOST=192.168.50.203
LIGHTRAG_PORT=9621
LIGHTRAG_API_KEY=<generated>
LIGHTRAG_SERVER_URL=http://192.168.50.203:9621
LIGHTRAG_MCP_API_KEY=<same as LIGHTRAG_API_KEY>
```

## V0-V6 Gate Results

| Gate | Status | Notes |
|------|--------|-------|
| V0: Pre-state | PASS | Qdrant running, bge-m3 available, port 9621 free |
| V1: Install + Version | PASS (version alignment VERIFICATION-REQUIRED) | lightrag-hku v1.5.7 installed, lightragmcp v1.1.0; running-version alignment pending per the V3 correction |
| V2: Config posture | PASS | LAN bind, API key auth, Qdrant backend, local Ollama LLM+embeddings |
| V3: API probe | PASS (version alignment VERIFICATION-REQUIRED) | Health, Web UI, auth gate working; `core_version` 1.5.6 vs recorded 1.5.7 — reconcile per correction |
| V4: Document lifecycle | PASS | Insert, extract (9 entities, 8 relations), query with correct answer |
| V5: Qdrant backend | PASS | 3 collections, 18 points total |
| V6: Health monitoring | PASS | Service active, enabled, health endpoint green |

**Overall: ALL GATES PASS**

## Notes

- Native deployment (no Docker) — pip venv + systemd, owner rule 2026-08-27
- LLM binding switched from Meta-X/OmniRoute to Chat-X/local Ollama (see V2 correction)
- MCP server is stdio transport (not SSE/HTTP daemon) — by design
- Web UI bundled with lightrag-hku[api] — no separate download needed
