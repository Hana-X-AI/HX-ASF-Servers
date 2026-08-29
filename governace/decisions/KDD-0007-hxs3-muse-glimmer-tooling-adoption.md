# KDD-0007: Adopt the hxs-3 Muse Glimmer 30B tooling pilot

- Date: 2026-08-26
- Status: ratified
- Decider: Agent-Zero
- Related goals: 2026-08-26-hxs3-muse-glimmer-tooling

## Context

The owner commissioned the hxs-3 mission (2026-08-26): deploy Meta's Muse
Glimmer 30B as the factory's primary tool agent within the RAG pipeline, per
the owner-updated v1.1 authoritative pilot. Meta's documentation quality
(explicit runtime boundaries, chat-template/special-token contracts, native
ATEM tool format, one-call-per-turn limitation, reasoning-strength controls,
context/truncation/image/DFlash behavior, compatibility floors, failure modes)
materially improves HX fit and reduces reverse-engineering cost. The corrected
v1.1 architecture registers Muse as a **sequential, one-call-per-turn** tooling
specialist; parallel tooling must occur above the model within KK3's
orchestration plane, never as an advertised model capability. The v1.1's
DeepSeek Harness registration framing maps to the Second Brain catalog
(Harness verified nonexistent, owner 2026-08-26; KDD-0006 convention), and its
"Neo" role is covered by KK3 + john/Esme. The artifact is an official Ollama
library tag (`muse-glimmer:30b`, ~18 GB, LM 27.9B Q4_K_M + 1.92B CLIP
projector, Apache-2.0); the model executes dense (~29.6B) on hxs-3's 2× RTX
5060 Ti with measured placement/KV.

## Options considered

1. Ollama with the official artifact, blueprint-conformant (selected) — uniform
   service/identity/preload/fixture patterns across all three hosts; v1.1's
   ratified choice; escape hatch preserved.
2. Meta's native llama.cpp server (doc-1 path) — first-class architecture,
   ATEM parser, DFlash, reasoning_strength support; rejected as the primary
   because it breaks the blueprint's uniform operations (systemd, /api/ps,
   alias+digest, preload, fixtures); retained as the DRAFTED ESCAPE HATCH if
   the Ollama compatibility gate fails at M4/M5.
3. Defer hxs-3 until after hxs-2 closes — rejected: independent hosts and
   lanes; the factory multiplexes safely; the owner asked to start now.

## Decision

Adopt PILOT-HXS3-MUSE-GLIMMER-TOOLING-001: provision hxs-3 with the exact
`muse-glimmer:30b` artifact via Ollama per the approved plan (session plan
`patriot-miles-morales-us-agent.md`), qualified per the factory playbook, and
registered in the Second Brain catalog with `parallel_tool_calling: false` as
a first-class capability LIMIT, enforced at two levels: responses containing
more than one tool call are rejected, and accepted calls execute serially with
results returned before the next selection (the request-level
`parallel_tool_calls` flag is a compatibility probe only, never enforcement —
review finding 2026-08-26). One tool call per model turn, proposed never
authorized; KK3 owns orchestration, parallelization-above-the-model,
acceptance, and evidence. gpt-oss is retained as task-shaped control, not
displaced. D-items D1–D8 are recorded in the goal file.

## Consequences

Enables: the factory's agent-intelligence node with a documented native tool
contract; capability limits become registry content (every future dispatch
retrieves them); the LLM-backend playbook earns its third validated host,
justifying formal pattern promotion at M8. Forecloses: any parallel-tool claim
for this model, any second serving plane unless the escape hatch fires, any
Harness dependency, LightRAG integration in this pilot (consumer unbuilt).
Revisit if: Ollama fails Muse compatibility (escape hatch), the RAG pipeline
is built (integration pilot), or Meta ships a materially different artifact
(re-qualification on digest change, CX-R02 pattern).
