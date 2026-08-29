# Change Record: LightRAG Deployment on hxs-4

| Field | Value |
| --- | --- |
| Date | 2026-08-29 |
| Host | hxs-4 (192.168.50.203) |
| Change type | New service deployment (RAG system) |
| Agent lane | raphael (LightRAG, KDD-0018) |
| Status | COMPLETE — LightRAG operational, V0-V6 PASS |

## What changed

LightRAG v1.5.7 deployed on hxs-4, providing graph-based RAG
(retrieval-augmented generation) capability for the factory.
Documents can be ingested, entities and relations extracted, and
hybrid queries answered with citations.

## Why

The factory needed a graph-based RAG system to support the Second
Brain architecture — document ingestion, entity/relation
extraction, and hybrid query with source citations.

## Before state

No RAG system deployed. hxs-4 had Qdrant (v1.19.0) and Ollama
(Chat-X / Qwen 3.5 9B + bge-m3 embeddings) already running.

## After state

| Property | Value |
| --- | --- |
| Software | `lightrag-hku[api,offline-storage,offline-llm]` v1.5.7 |
| Port | 9621 |
| Venv | `/srv/lightrag/.venv/` |
| Service | `lightrag.service` (systemd, enabled + active) |
| LLM binding | Chat-X (Qwen 3.5 9B) via local Ollama (`127.0.0.1:11434`) |
| Embeddings | bge-m3 via Ollama, 1024 dimensions |
| Vector storage | QdrantVectorDBStorage (`192.168.50.203:6333`) |
| Graph storage | NetworkX (default, JSON files) |
| KV storage | JSON (default) |
| Web UI | Bundled, served at `:9621` |
| Auth | API key (X-API-Key header) |
| MCP server | lightragmcp v1.1.0, 30 tools, stdio transport (on-demand) |

## Verification

V0-V6 gates all PASS. Key evidence:

- **V4 Document lifecycle:** A test document was ingested. Chat-X
  (local Ollama) processed it in ~2 minutes, extracting 9 entities
  and 8 relations. A hybrid query returned the correct answer with
  citation: `"Agent Quinn is responsible for managing the Qdrant
  vector database on hxs-4"` with citation `[[1]] fresh_test.txt`.
- **V5 Qdrant backend:** 3 collections created —
  `lightrag_vdb_entities_bge_m3_1024d` (9 points),
  `lightrag_vdb_chunks_bge_m3_1024d` (1 point),
  `lightrag_vdb_relationships_bge_m3_1024d` (8 points).
- **V6 Health monitoring:** Service active, enabled, health
  endpoint returns healthy.

| Gate | Status |
| --- | --- |
| V0: Pre-state | PASS |
| V1: Install + Version | PASS |
| V2: Config posture | PASS |
| V3: API probe | PASS |
| V4: Document lifecycle | PASS |
| V5: Qdrant backend | PASS |
| V6: Health monitoring | PASS |

**Overall: ALL GATES PASS**

## Conclusion

LightRAG is operational on hxs-4. The LLM binding was switched from
Meta-X via OmniRoute to Chat-X via local Ollama after an OmniRoute
504 timeout — Meta-X 30B was too slow for LightRAG's entity
extraction prompts. Chat-X on local Ollama processes documents in
~2 minutes with no rate-limit issues.

## Rollback

```bash
systemctl stop lightrag
systemctl disable lightrag
pip uninstall lightrag-hku   # from /srv/lightrag/.venv/
rm -rf /srv/lightrag
```

Qdrant collections created by LightRAG can be deleted separately if
a full rollback is required.

## MCP server

lightragmcp v1.1.0 is installed at `/usr/bin/lightrag-mcp-server`.
It uses stdio transport and is launched by MCP clients on demand
(not a daemon). MCP client config:

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

## Sources

- `servers/hxs-4/2026-08-29-lightrag-install-evidence.md`
- `goals/2026-08-29-lightrag-hxs4.md`
- `servers/hxs-4/qdrant-config.md`
- `agents/raphael/profile.md` (KDD-0018)
