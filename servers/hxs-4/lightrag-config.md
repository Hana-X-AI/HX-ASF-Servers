# hxs-4 — LightRAG Configuration

**Configuration date:** 2026-08-29
**Agent lane:** raphael (LightRAG, KDD-0018)
**Status:** Operational (V0-V6 PASS)

## Functional role

LightRAG provides graph-based RAG (retrieval-augmented generation)
for the factory: document ingestion, entity/relation extraction,
and hybrid query with source citations. It supports the Second
Brain architecture by enabling knowledge-graph-augmented retrieval
over ingested documents.

## Technical configuration

| Property | Value |
| --- | --- |
| Software | `lightrag-hku[api,offline-storage,offline-llm]` v1.5.7 |
| Port | 9621 |
| Venv | `/srv/lightrag/.venv/` |
| Config | `/srv/lightrag/.env` |
| Service | `lightrag.service` (systemd, enabled + active) |
| Auth | API key (X-API-Key header) |
| Web UI | Bundled, served at `:9621` |
| Telemetry | Disabled |

## LLM binding

| Property | Value |
| --- | --- |
| Binding | ollama (local) |
| LLM host | `http://127.0.0.1:11434` |
| LLM model | `hx-qwen3.5-9b-64k` (Chat-X, Qwen 3.5 9B) |

The LLM binding was originally configured for Meta-X (Muse Glimmer
30B) via OmniRoute. It was switched to Chat-X via local Ollama
after an OmniRoute 504 timeout (`RATE_LIMIT_EXECUTION_TIMEOUT`) —
Meta-X 30B was too slow for LightRAG's entity extraction prompts.
Chat-X on local Ollama processes documents in ~2 minutes with no
rate-limit issues.

## Embeddings

| Property | Value |
| --- | --- |
| Binding | ollama |
| Embedding host | `http://127.0.0.1:11434` |
| Embedding model | bge-m3 |
| Embedding dimensions | 1024 |

## Vector storage

| Property | Value |
| --- | --- |
| Backend | QdrantVectorDBStorage |
| Qdrant URL | `http://192.168.50.203:6333` |
| Qdrant API key | from `.local.env` (`QDRANT_API_KEY`) |
| Entity collection | `lightrag_vdb_entities_bge_m3_1024d` |
| Chunk collection | `lightrag_vdb_chunks_bge_m3_1024d` |
| Relationship collection | `lightrag_vdb_relationships_bge_m3_1024d` |

## Graph storage

- **NetworkX** (default) — JSON files on disk
- KV storage: JSON (default)

## MCP server

| Property | Value |
| --- | --- |
| Package | lightragmcp v1.1.0 |
| Binary | `/usr/bin/lightrag-mcp-server` |
| Tools | 30 |
| Transport | stdio (launched by MCP clients on demand, not a daemon) |
| Systemd unit | Disabled (on-demand, not a persistent service) |

MCP client config:

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

## Dependencies

| Dependency | Provider | Status |
| --- | --- | --- |
| Qdrant (vector storage) | quinn (KDD-0017) | Operational on hxs-4:6333 |
| Ollama + bge-m3 (embeddings) | john (Ollama engineer) | Operational on hxs-4 |
| Ollama + Chat-X (LLM) | john (Ollama engineer) | Operational on hxs-4 |

## Disabled features

| Feature | Status | Reason |
| --- | --- | --- |
| Rerank | Disabled | No external rerank model configured |
| Neo4j graph storage | Disabled | NetworkX (default) used instead — simpler, file-based |
| PostgreSQL graph storage | Disabled | NetworkX (default) used instead — no external DB dependency for graph storage |

## Rollback

```bash
systemctl stop lightrag
systemctl disable lightrag
pip uninstall lightrag-hku   # from /srv/lightrag/.venv/
rm -rf /srv/lightrag
```

Qdrant collections created by LightRAG can be deleted separately if
a full rollback is required.

## Discovery reference

```text
servers/hxs-4/discovery.md
```

As-found record dated 2026-08-12; preserved unchanged. Do not
modify the discovery record.

## Sources

- `servers/hxs-4/2026-08-29-lightrag-install-evidence.md`
- `governace/goals/2026-08-29-lightrag-hxs4.md`
- `governace/status-reporting/change-lightrag-deploy-2026-08-29.md`
- `servers/hxs-4/qdrant-config.md`
- `agents/raphael/profile.md` (KDD-0018)
