# KDD-0018: Raphael registration — LightRAG systems engineer

- Date: 2026-08-29
- Status: ratified
- Decider: Agent-Zero
- Related: KDD-0016 (agent taxonomy), KDD-0017 (Quinn/Qdrant — dependency), `goals/2026-08-29-lightrag-hxs4.md` (implementation goal), `servers/system-mapping.md` (S17 placement)

## Context

The system-to-server mapping (ratified 2026-08-29) assigns LightRAG to
hxs-4, co-located with Qdrant (deployed v1.19.0, Quinn) and Chat-X (Qwen
3.5 9B). LightRAG is a graph-based RAG framework that uses Qdrant as its
vector storage backend and requires an LLM binding (Meta-X via OmniRoute)
and an embedding model (bge-m3 via Ollama on hxs-4). A dedicated engineer
is needed for the LightRAG stack lifecycle.

[OPEN CORRECTION 2026-08-29, labeled, append-only: the Context's "Qdrant
(deployed v1.19.0, Quinn)" and Adaptation 6's "dependency satisfied" are
PRESERVED as history but are NOT YET ESTABLISHED as an accepted vector
backend. Verified state: the authoritative `servers/system-mapping.md`
still lists S09 Qdrant under "Target-state — not yet deployed"; Quinn
remains activation-gated (roster + KDD-0017: implemented + credential
entries + governor activation word); no state-log row records Qdrant
acceptance or Quinn's activation word. An install evidence doc
(`servers/hxs-4/2026-08-29-qdrant-install-evidence.md`, v1.19.0 running
2026-08-29) evidences installation, not acceptance. EFFECT: the Qdrant
dependency is PENDING ACCEPTANCE for Raphael's activation gate; Quinn
stays activation-gated until an accepted vector backend is evidenced
(install evidence reviewed + Quinn activation word). Raphael's own
registration stands; only the dependency's satisfied-status is corrected.]

## Decision

Register Raphael as the LightRAG systems engineer for HX-ASF.

### Lane assignment

- Model lane: Qwen-X (`ollama-local/hx-qwen3.8-27b-64k`, hxs-1, via
  OmniRoute hxs-8) — owner-assigned 2026-08-29. Local lane (no OD-14
  cloud metering). CLI alias `omniroute/qwen-x` already exists in
  kimi-code config.

### Target host

- hxs-4 (192.168.50.203) — co-located with Qdrant (Quinn), Chat-X, and
  LightRAG server on port 9621.

### Adaptations from source

1. No external source document — this is an original profile created per
   owner directive 2026-08-29.
2. Knowledge base: four LightRAG directories at `/opt/tkv-local/` —
   `LightRAG-main` (v1.5.7), `lightragmcp-main` (v1.0.0),
   `daniel-lightrag-mcp-main` (v0.1.0), and
   `/home/hxsa/opt/local-tkv/agent-zero-docs/lightrag/` (HX reference docs).
3. MCP server: lightragmcp (Suryan v1.1.0, 30 tools) — owner-selected.
   [OPEN CORRECTION 2026-08-29: v1.0.0 → v1.1.0 per npm package.json.]
4. LLM binding: Chat-X (Qwen 3.5 9B) via local Ollama on hxs-4 —
   owner-selected. [OPEN CORRECTION 2026-08-29: originally Meta-X via
   OmniRoute — switched after OmniRoute rate-limit timeout; Chat-X
   processes LightRAG extraction in ~2 min. Original wording preserved.]
5. Embedding: bge-m3 via Ollama on hxs-4 — owner-selected. Cross-lane
   dependency: john must install bge-m3 before LightRAG can ingest.
6. Vector storage: Qdrant (Quinn's lane) — dependency satisfied.

### Activation gate

Raphael is registered but activation-gated. Conditions:
1. The LightRAG server instance is implemented and validated on hxs-4.
2. bge-m3 model is installed on hxs-4 via Ollama (john's lane).
3. LightRAG API key and credential entries exist in `.local.env`.
4. The governor's explicit activation word.
5. [OPEN CORRECTION 2026-08-29, labeled, append-only: Qdrant vector
   backend is ACCEPTED — install evidence
   (`servers/hxs-4/2026-08-29-qdrant-install-evidence.md`) reviewed and
   Quinn's activation word recorded. Until then the dependency is PENDING
   (see the Context correction above).]

The instance-exists precondition does NOT block Raphael from installing
LightRAG — he installs his own instance (same ruling as Chris, Wayne, Quinn).

### Lane boundary

Raphael owns the LightRAG stack: server, Web UI, lightragmcp MCP server.
He does not own Qdrant (Quinn), Ollama/model installation (john),
OmniRoute (trinity), PostgreSQL (chris), Redis (wayne), or any non-LightRAG
system.

## Roster entry

`agents/raphael/` created (charter + profile, per KDD-0016 standard
template). Roster row added to `agents/README.md`. Config alias
`omniroute/qwen-x` already exists (shared with gordon's prior lane).
System-mapping S17 added.

[OPEN CORRECTION 2026-08-29, labeled, append-only — CURRENT QDRANT
BACKEND STATE (single authoritative declaration). Effective 2026-08-29.
Evidence reference: `servers/hxs-4/2026-08-29-qdrant-install-evidence.md`
(v1.19.0, `qdrant.service` active since 2026-08-29T12:14:13Z, V0–V3:
install/version/config/API probe). CURRENT STATE: Qdrant is INSTALLED on
hxs-4 but is NOT an ACCEPTED vector backend for LightRAG — the dependency
is PENDING ACCEPTANCE. Acceptance requires (a) the install evidence
reviewed by the governor and (b) Quinn's activation word recorded
(roster + KDD-0017 gate still read: activation-gated). This declaration
SUPERSEDES, as the current-state claim, the prior wording "dependency
satisfied" (Adaptation 6) and the Context's "deployed v1.19.0" — both
preserved above as history and now resolved to exactly one state. Quinn
remains activation-gated until an accepted vector backend is evidenced.]

[OPEN CORRECTION 2026-08-29, labeled, append-only — SUPERSEDES the
Activation-gate condition 5 "Qdrant vector backend is ACCEPTED…" wording.
Provenance: review finding, 2026-08-29 (governor review of KDD-0018 after
the Qdrant install evidence and Quinn gating state). The condition-5
"ACCEPTED" phrasing is AMBIGUOUS — it could be misread as Qdrant already
being accepted, which would conflict with the PENDING ACCEPTANCE state
declared above. Reconciliation: the effective state is EXACTLY ONE —
**Qdrant is INSTALLED but NOT ACCEPTED for LightRAG; the dependency is
PENDING ACCEPTANCE; Raphael remains activation-gated** until (a) install
evidence is reviewed by the governor AND (b) Quinn's activation word is
recorded. Condition 5 is corrected to read: "Qdrant vector backend is
ACCEPTED only after install evidence reviewed by the governor AND Quinn's
activation word recorded; until both are on record, the dependency is
PENDING and Raphael stays activation-gated." The original condition-5 text
is preserved above as history; this correction is the operative reading.]

## Provenance

Original record — no external source document. Created per owner
directive 2026-08-29. Knowledge base: `/opt/tkv-local/LightRAG-main/`
(v1.5.7), `/opt/tkv-local/lightragmcp-main/` (v1.1.0),
`/opt/tkv-local/daniel-lightrag-mcp-main/` (v0.1.0),
`/home/hxsa/opt/local-tkv/agent-zero-docs/lightrag/`. Target host: hxs-4
per `goals/2026-08-29-lightrag-hxs4.md`. Model lane: Qwen-X via OmniRoute,
provider hxs-1. LLM binding for LightRAG: Chat-X via local Ollama
(corrected from Meta-X/OmniRoute).
