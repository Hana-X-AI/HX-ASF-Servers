# KDD-0017: Quinn registration — Qdrant vector database systems engineer

- Date: 2026-08-29
- Status: ratified
- Decider: Agent-Zero
- Related: KDD-0016 (agent taxonomy), `servers/system-mapping.md` (system placement)

## Context

The system-to-server mapping (ratified 2026-08-29) assigns Qdrant to
hxs-4, co-located with Chat-X (Qwen 3.5 9B). hxs-4 has 477 GB
unallocated NVMe — ideal for vector database storage. A dedicated
engineer is needed for the Qdrant stack lifecycle.

## Decision

Register Quinn as the Qdrant vector database systems engineer for HX-ASF.

### Lane assignment

- Model lane: NVIDIA Nemotron 3 Ultra (`openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`,
  provider NVIDIA, via OmniRoute hxs-8) — free tier on OpenRouter.
  Owner-assigned 2026-08-29. CLI alias `omniroute/nemotron-3-ultra` added
  to kimi-code config. `max_output_size=16384` per the row-33 guard class.
  Route probed live: served id `nvidia/nemotron-3-ultra-550b-a55b:free`,
  content `QUINN_LANE_OK`.

### Target host

- hxs-4 (192.168.50.203) — co-located with Chat-X; Qdrant storage on
  477 GB unallocated NVMe.

### Adaptations from source

1. No external source document — this is an original profile created per
   owner directive 2026-08-29.
2. Knowledge base: three Qdrant directories at `/opt/tkv-local/` —
   `qdrant-master` (server v1.15.5), `qdrant-client-master` (Python client
   v1.15.1), `mcp-server-qdrant-master` (MCP server v0.8.1).
3. MCP server co-located with Qdrant on hxs-4 per the system-mapping MCP
   architecture decision (2026-08-29).

### Activation gate

Quinn is registered but activation-gated. Conditions:
1. The Qdrant server instance is implemented and validated on hxs-4.
2. Qdrant API key and credential entries exist in `.local.env`.
3. The governor's explicit activation word.

The instance-exists precondition does NOT block Quinn from installing
Qdrant — he installs his own instance (same ruling as Chris and Wayne).

### Lane boundary

Quinn owns the Qdrant stack: server, Python client, MCP server.
He does not own PostgreSQL (Chris), Redis (Wayne), LightRAG, embedding
models, or any non-Qdrant system.

## Roster entry

`agents/quinn/` created (charter + profile, per KDD-0016 standard
template). Roster row added to `agents/README.md`. Config alias
`omniroute/nemotron-3-ultra` added to kimi-code config.

## Provenance

Original record — no external source document. Created per owner
directive 2026-08-29. Knowledge base: `/opt/tkv-local/qdrant-master`
(v1.15.5), `/opt/tkv-local/qdrant-client-master` (v1.15.1),
`/opt/tkv-local/mcp-server-qdrant-master` (v0.8.1).
