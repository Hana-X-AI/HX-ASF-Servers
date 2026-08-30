# Goal: Implement LightRAG and LightRAG MCP server on hxs-4

- Goal ID: 2026-08-29-lightrag-hxs4 (this file's name)
- Version: 1
- Status: draft
- Owner: Agent-Zero
- Created: 2026-08-29
- Human authority: Agent-Zero
- Agent lane(s): **raphael** (LightRAG systems engineer, Family 3,
  vertical, hxs-4; KDD-0018 ratified, registered 2026-08-29; lane Qwen-X
  via OmniRoute hxs-1). LLM binding: **local Ollama on hxs-4**
  (`LLM_BINDING=ollama`, `hx-qwen3.5-9b-64k`) per owner decision 2026-08-29 —
  the earlier Meta-X/OmniRoute binding is superseded (preserved as history).
  Embedding model (bge-m3) install on hxs-4 via Ollama requires john's lane
  (Ollama engineer).

## Intent

Install and configure LightRAG v1.5.7 (graph-based RAG framework) and a
LightRAG MCP server on hxs-4, using Qdrant as the vector storage backend.
LightRAG combines knowledge graphs with vector search for dual-level
retrieval. The MCP server exposes LightRAG's document management, query,
and knowledge graph operations through the Model Context Protocol. This
creates a production RAG capability for the HX factory — semantic search,
entity extraction, and knowledge graph queries against ingested documents.

## Scope and target

- Target identity: hxs-4 (192.168.50.203), co-located with Qdrant (deployed,
  v1.19.0) and Chat-X (Qwen 3.5 9B)
- Baseline: Qdrant v1.19.0 running and validated on hxs-4 (V0–V6 PASS,
  evidence at `servers/hxs-4/2026-08-29-qdrant-install-evidence.md`);
  Qdrant API key in `.local.env`; 477 GB NVMe mounted at `/var/lib/qdrant`
- In scope:
  - LightRAG server v1.5.7 (Python, `lightrag-hku[api]` via pip/uv)
  - LightRAG Web UI (bundled with `lightrag-hku[api]`)
  - lightragmcp MCP server (Suryan v1.1.0, owner-selected — see decision below)
  - Qdrant as vector storage backend (`QdrantVectorDBStorage`)
  - LLM binding via local Ollama on hxs-4 (`LLM_BINDING=ollama`,
    `LLM_BINDING_HOST=http://127.0.0.1:11434`, `LLM_MODEL=hx-qwen3.5-9b-64k`) —
    the selected binding per owner decision 2026-08-29; the earlier "via
    OmniRoute (hxs-8)" requirement is superseded for the LLM binding (preserved
    as history)
  - Embedding binding via Ollama on hxs-4 (Chat-X) or OmniRoute
  - Credentials in `.local.env`
  - systemd services for LightRAG server and MCP server
  - Native deployment (no Docker, owner rule 2026-08-27)
- Out of scope:
  - Qdrant server itself (already deployed, Quinn's lane)
  - Embedding model serving infrastructure (TEI/Infinity) — use Ollama or
    OmniRoute for embeddings, not a separate embedding server
  - Docling/Crawl4AI ingest pipelines (separate systems S12/S13, future)
  - Neo4j or PostgreSQL graph storage — graph storage stays on the default
    NetworkXStorage (file-persisted GraphML); no PostgreSQL/Neo4j graph backend
- Constraints:
  - No Docker/containers (owner rule 2026-08-27)
  - No host firewall (owner rule 2026-08-26, LAN is the boundary)
  - Native systemd services only
  - LightRAG server binds to LAN (192.168.50.203:9621)
  - API key authentication required
  - Credentials in `.local.env` only, never in repo
  - Qdrant dependency is satisfied (deployed, API key available)
  - LLM binding must use local models (local-model-first rule) — the selected
    binding is **local Ollama on hxs-4** (`LLM_BINDING=ollama`,
    `LLM_BINDING_HOST=http://127.0.0.1:11434`, `LLM_MODEL=hx-qwen3.5-9b-64k`)
    per the owner decision 2026-08-29; the earlier "via OmniRoute" constraint
    and Meta-X routing are superseded for this binding (preserved as history)

## Knowledge sources for the implementing agent

The agent assigned to this goal must survey these knowledge directories
using the **be-great** skill before acting:

1. `/opt/tkv-local/LightRAG-main/` — LightRAG v1.5.7 source (Rust/Python,
   Apache-2.0). Contains: `lightrag/` (core library), `lightrag/api/` (server),
   `lightrag_webui/` (web UI), `env.example` (configuration reference),
   `lightrag/kg/qdrant_impl.py` (Qdrant storage backend),
   `pyproject.toml` (dependencies, optional extras: api, offline-storage,
   offline-llm), `lightrag.service.example` (systemd unit template),
   `docs/` (deployment guides). Reference only; install from PyPI
   (`lightrag-hku[api]`).

2. `/opt/tkv-local/lightragmcp-main/` — LightRAG MCP Server v1.1.0 (npm
   package.json; Python `__init__.py` reads v1.0.0 — npm is the install
   source and authoritative) by Lalit Suryan (MIT). Node.js/Python hybrid,
   30 tools. Requires a running LightRAG server at `LIGHTRAG_SERVER_URL`.
   Install via `npx` or `npm install -g`. Tools: document management (10),
   query (3), knowledge graph (8), system management (9). Config:
   `LIGHTRAG_SERVER_URL`, `LIGHTRAG_API_KEY`, `LIGHTRAG_WORKSPACE`. See
   `TOOLS_SUMMARY.md` for the full tool list and `API_REFERENCE.md` for
   endpoint details.

3. `/opt/tkv-local/daniel-lightrag-mcp-main/` — Daniel LightRAG MCP v0.1.0
   by Daniel Simpkins (MIT). Pure Python, 22 tools. Requires LightRAG server
   at `LIGHTRAG_BASE_URL`. Install via `pip install -e .`. Tools: document
   management (6), query (2), knowledge graph (6), system management (4+1
   health check). See `CONFIGURATION_GUIDE.md` and `IMPLEMENTATION_GUIDE.md`
   for setup. Lighter weight, fewer dependencies.

4. `/home/hxsa/opt/local-tkv/agent-zero-docs/lightrag/` — HX reference
   docs: `lr1.md` (LightRAG MCP bridge overview), `LightRAG-API-for-Retrieval-
   Augmented-Generation.md` (API integration guide with mcp-config.json
   examples), PDF version.

## MCP server decision

**Owner decision (2026-08-29): Install lightragmcp (Suryan) v1.1.0** — 30
tools, higher maturity, npm install. The daniel-lightrag-mcp is the fallback.

## LLM and embedding decisions (owner, 2026-08-29)

- **LLM binding:** [OPEN CORRECTION 2026-08-29, labeled: originally
  configured for Meta-X (Muse Glimmer 30B on hxs-3) via OmniRoute.
  Switched to Chat-X (Qwen 3.5 9B) via local Ollama on hxs-4 after
  OmniRoute rate-limit execution timeout (504 RATE_LIMIT_EXECUTION_TIMEOUT)
  — Meta-X 30B was too slow for LightRAG's entity extraction prompts.
  Chat-X on local Ollama processes documents in ~2 minutes. Original
  OmniRoute/Meta-X wording preserved as history.]
  `LLM_BINDING=ollama`, `LLM_BINDING_HOST=http://127.0.0.1:11434`,
  `LLM_MODEL=hx-qwen3.5-9b-64k`.
- **Embedding binding:** bge-m3 via Ollama on hxs-4 (Chat-X GPU).
  `EMBEDDING_BINDING=ollama`, `EMBEDDING_BINDING_HOST=http://127.0.0.1:11434`,
  `EMBEDDING_MODEL=bge-m3`, `EMBEDDING_DIM=1024`.
  bge-m3 installed by john's lane (Ollama engineer) — VERIFIED available
  on hxs-4, embeddings probe passed HTTP 200.

## Agent: raphael

- Name: raphael
- Role: LightRAG systems engineer
- Family: 3 (Platform Systems)
- Lane type: vertical
- System: S17 LightRAG (+MCP) on hxs-4
- Model lane: Qwen-X (`ollama-local/hx-qwen3.8-27b-64k`, hxs-1, via OmniRoute
  hxs-8) — owner-assigned 2026-08-29
- Status: Registered (KDD-0018, ratified 2026-08-29)
- Knowledge dirs: `/opt/tkv-local/LightRAG-main/`,
  `/opt/tkv-local/lightragmcp-main/`,
  `/opt/tkv-local/daniel-lightrag-mcp-main/`,
  `/home/hxsa/opt/local-tkv/agent-zero-docs/lightrag/`

## Success conditions and evidence

| ID | Property | Measurement / procedure | Expected result | Evidence | Verifier |
| --- | --- | --- | --- | --- | --- |
| SC-01 | LightRAG server installed | `lightrag-server --version` or `pip show lightrag-hku` | v1.5.7 installed | command output | governor |
| SC-02 | LightRAG server running | `systemctl is-active lightrag` | active (running) | systemctl status | governor |
| SC-03 | LightRAG API responds | `curl http://192.168.50.203:9621/health` | 200 OK, health check passed | curl output | governor |
| SC-04 | Qdrant backend configured | LightRAG config uses `QdrantVectorDBStorage` with Qdrant URL and API key | Collections created in Qdrant after document insert | Qdrant collections list | governor |
| SC-05 | LLM binding works | LightRAG config uses the selected local Ollama binding on hxs-4 (`LLM_BINDING=ollama`, `LLM_MODEL=hx-qwen3.5-9b-64k`) — the OmniRoute/Meta-X binding is superseded (owner decision 2026-08-29, preserved as history) | Query returns generated text | query output | governor |
| SC-06 | Embedding binding works | LightRAG config uses the owner-selected Ollama embedding configuration on hxs-4 — model **bge-m3**, dimension **1024** (no OmniRoute alternative; the embedding path is Ollama on hxs-4 only) | Document ingestion creates vectors in Qdrant; vector count > 0 and embedding dimension = 1024 | vector count > 0 + config shows bge-m3/1024 | governor |
| SC-07 | LightRAG Web UI accessible | `curl http://192.168.50.203:9621/` returns HTML | Web UI loads | curl output | governor |
| SC-08 | MCP server installed and running | `systemctl is-active lightrag-mcp` | active (running) | systemctl status | governor |
| SC-09 | MCP server responds | MCP client can connect and call `get_health` tool | Health check returns OK | MCP client output | governor |
| SC-10 | Document lifecycle | Insert test document, query it, delete it | Query returns relevant results; clean state after delete | API call sequence | governor |
| SC-11 | Credentials stored | All LightRAG credentials in `.local.env`; verify the required variable NAMES exist without printing their values | QDRANT_URL, QDRANT_API_KEY, LIGHTRAG_API_KEY, LLM_BINDING (plus LLM_BINDING_HOST/LLM_MODEL) vars present; any missing entry is a validation failure | command: `set -a; . ./.local.env; set +a; for v in QDRANT_URL QDRANT_API_KEY LIGHTRAG_API_KEY LLM_BINDING LLM_BINDING_HOST LLM_MODEL; do [[ -v "$v" ]] \|\| { echo "MISSING: $v"; exit 1; }; done; echo "SC-11 OK: required vars present (values not printed)"` — run non-interactively with stdin closed so it cannot block | governor |
| SC-12 | systemd units persist | `systemctl is-enabled lightrag lightrag-mcp` | both enabled | systemctl output | governor |
| SC-13 | Repo validation | `python3 scripts/validate.py` | 4/4 PASS | validate output | governor |
| SC-14 | LightRAG test suite | Run LightRAG core tests: `bash -o pipefail -c 'cd /opt/tkv-local/LightRAG-main && python3 -m pytest tests/ -x --timeout=60 2>&1 \| tail -5'` | Core tests pass (425 test files) | pytest output | governor |
| SC-15 | lightragmcp test suite | Run MCP server tests: `bash -o pipefail -c 'cd /opt/tkv-local/lightragmcp-main && python3 -m pytest tests/ -x 2>&1 \| tail -5'` | MCP server tests pass (1 test file: test_server.py) | pytest output | governor |
| SC-16 | bge-m3 model available on hxs-4 | `curl http://192.168.50.203:11434/api/tags \| grep bge-m3` | bge-m3 model listed (installed by john's lane) | curl output | governor |

## Execution controls

- Pre-flight: Qdrant v1.19.0 running on hxs-4 (VERIFIED — V0–V6 PASS,
  Quinn evidence doc); Qdrant API key in `.local.env` (VERIFIED)
- Active charters reviewed: raphael (KDD-0018, registered, lane Qwen-X)
  owns LightRAG; Quinn (KDD-0017) owns Qdrant (dependency). Qualified
  agent available: YES (raphael).
- Maximum iterations / retries: 3 per step
- Time / token limits: PT1H per session
- Stop conditions: Qdrant dependency failure, LLM binding failure,
  permission denied on hxs-4, validate.py FAIL
- Rollback / containment: systemd stop (lightrag + lightrag-mcp) + uninstall
  BOTH installed components: uninstall LightRAG from the Python environment
  actually used by the deployment (whether installed via pip or uv —
  `pip uninstall lightrag-hku` or `uv pip uninstall lightrag-hku` in the
  deployment venv) and remove the npm-installed lightragmcp package
  (`npm uninstall lightragmcp`); Qdrant data preserved (LightRAG creates its
  own collections, does not modify existing)
- HITL checkpoints: bge-m3 install on hxs-4 (john's lane — cross-lane
  dependency); LLM model confirmation (local Ollama binding, hx-qwen3.5-9b-64k —
  the OmniRoute/Meta-X binding is superseded per owner decision 2026-08-29);
  embedding dim verification (bge-m3 = 1024); pytest presence verification
  before SC-14/15

## Architecture

```text
Document ingest → LightRAG server (hxs-4:9621)
                    ├── LLM binding → Ollama (hxs-4) → Chat-X (Qwen 3.5 9B)
                    ├── Embedding binding → Ollama (hxs-4) → bge-m3 (installed by john)
                    ├── Vector storage → Qdrant (hxs-4:6333, Quinn's lane)
                    ├── Graph storage → NetworkX (default)
                    ├── KV storage → JSON (default)
                    └── Web UI → bundled, served at :9621

MCP clients → lightragmcp (Suryan v1.1.0, 30 tools)
                └── connects to LightRAG API (hxs-4:9621)
```

**MCP transport (SC-09 reachable):** lightragmcp runs stdio; a systemd-managed
stdio process is not directly reachable by independent MCP clients. Use
**client-launched stdio** for local MCP clients (the client spawns the
lightragmcp process itself, e.g. via an mcp-config command entry) — this makes
SC-09 reachable without a persistent network server. Where remote clients must
reach it, define and test a **network bridge** (e.g. the stdio process wrapped
behind a socket/stream adapter) and record the tested transport in the
acceptance evidence. The systemd-managed stdio process alone does not satisfy
SC-09 unless the client-launch or bridge path is exercised and documented.


## Configuration (key env vars for .local.env)

```dotenv
LIGHTRAG_HOST=192.168.50.203
LIGHTRAG_PORT=9621
LIGHTRAG_API_KEY=<generated>
LLM_BINDING=ollama
LLM_BINDING_HOST=http://127.0.0.1:11434
LLM_MODEL=hx-qwen3.5-9b-64k
EMBEDDING_BINDING=ollama
EMBEDDING_BINDING_HOST=http://127.0.0.1:11434
EMBEDDING_MODEL=bge-m3
EMBEDDING_DIM=1024
LIGHTRAG_VECTOR_STORAGE=QdrantVectorDBStorage
QDRANT_URL=http://192.168.50.203:6333
QDRANT_API_KEY=<from QDRANT_API_KEY in .local.env>
LIGHTRAG_SERVER_URL=http://192.168.50.203:9621
LIGHTRAG_MCP_API_KEY=<same as LIGHTRAG_API_KEY>
```

## Notes and links

- KDDs: KDD-0017 (Quinn/Qdrant — dependency), KDD-0018 (raphael registration),
  KDD-0016 (agent taxonomy)
- Related goals: 2026-08-29 Qdrant implementation (servers/hxs-4/2026-08-29-qdrant-implementation-plan.md)
- System mapping: S17 LightRAG (+MCP) on hxs-4, agent raphael (registered
  KDD-0018)
- Cross-lane dependencies: john (Ollama) must install bge-m3 on hxs-4 before
  LightRAG can ingest; quinn (Qdrant) provides the vector backend
- Test suites: LightRAG core (425 test files in tests/), lightragmcp (1 test
  file: test_server.py), daniel-lightrag-mcp (5 test files) — all in vault
- Second Brain: PL-3 "Retrieval & Governed Knowledge" lists LightRAG as
  a target-state component — this goal implements it
- Knowledge dirs (give to the implementing agent):
  - `/opt/tkv-local/LightRAG-main/` (v1.5.7 source)
  - `/opt/tkv-local/lightragmcp-main/` (MCP server v1.1.0 npm, 30 tools)
  - `/opt/tkv-local/daniel-lightrag-mcp-main/` (MCP server v0.1.0, 22 tools)
  - `/home/hxsa/opt/local-tkv/agent-zero-docs/lightrag/` (HX reference docs)

Completion rule: this goal is done only when every success condition passes
with its required evidence and the verifier accepts the correct artifact —
not when the work feels done. The full contract model lives in
`agents/kimi-k3/goal-setting-guidance.md` (KDD-0002).
