# KDD-0015: Wayne registration — Redis systems engineer

- Date: 2026-08-29
- Status: ratified
- Decider: Agent-Zero
- Related goals: hxs-9 state-services implementation (registry target-state);
  PostgreSQL-to-Redis cache integration (pairs with Chris, KDD-0014)

## Context

The registry assigns hxs-9 "State services: PostgreSQL + Redis." Chris
(KDD-0014) owns PostgreSQL. The Redis side needs a dedicated engineer.
The owner's candidate profile
`agent-zero-docs/agent-profiles/wayne/wayne-profile.yaml`
(profile_version 2026-08-28T22:50:15Z, digest
`sha256:282d151fa8921fe299b24d98ac3f91981d21a7c6734e313f87cec23dc176dc26`,
preserved unchanged) was reviewed on request 2026-08-29 and dispositioned
by owner directive the same day.

## Decision

Register Wayne as the Redis systems engineer for HX-ASF.

### Lane assignment

- Model lane: OpenAI gpt-oss-120b (`openrouter/openai/gpt-oss-120b`,
  provider AkashML, via OmniRoute hxs-8) — same lane as Carol.
  Owner-assigned 2026-08-29. CLI alias `omniroute/gpt-oss-120b` already
  exists in the kimi-code config (established for Carol, row 33).
  `max_output_size=16384` per the row-33 guard class.

### Adaptations from the source profile (all recorded openly)

1. **Authority chain retargeted:** every "Paul" reference in the source
   profile reads as the governor (Flash) / Agent Zero. Escalation goes
   to the governor, never the owner directly. Distribution via Mia under
   governor-issued work orders.
2. **MCP surfaces — HOLD** (owner directive 2026-08-29): `mcp-redis-main`
   and `postgres-mcp-mai` are deferred. No MCP usage until the owner
   lifts the hold. Same posture as Chris's MCP hold. [LABELED CORRECTION 2026-08-31, append-only: the MCP hold is LIFTED per owner directive 2026-08-31; the 2026-08-29 hold is superseded.]
3. **RAG/vector/stream integration — DEFERRED** (owner directive
   2026-08-29): vector indexes, semantic caching, agent memory, and
   stream-based work queues are out of the initial scope. Separate
   assignment when the owner authorizes.
4. **Model lane assigned:** the source profile specified `coder-x` as
   primary backend. Superseded by the owner's lane assignment
   (gpt-oss-120b via OmniRoute).
5. **Profile location:** `agents/wayne/profile.md` (Markdown, not YAML —
   factory convention). Distilled from the source YAML with adaptations
   above.

### Activation gate

Wayne is registered but activation-gated. Conditions:
1. The Redis instance is implemented and validated on hxs-9.
2. Redis ACL users and credential entries exist in `.local.env`.
3. The governor's explicit activation word.

The instance-exists precondition does NOT block Wayne from installing
Redis — he installs his own instance (same ruling as Chris: the
DBA/cache engineer installs his own system). The gate covers post-install
activation for ongoing operational duties.

### Lane boundary with Chris

Wayne owns the Redis side of the PostgreSQL cache integration contract
(cache keys, TTLs, invalidation, serialization). Chris owns the PostgreSQL
side (schema, queries, roles, triggers). When a cache contract requires
a PostgreSQL change, Wayne hands off to Chris via the governor.

## Roster entry

`agents/wayne/` created (charter + profile, distilled from the candidate
YAML with provenance + source digest recorded). Roster row added to
`agents/README.md`. KDD-0013 amended (Amendment 9: Wayne registered,
EIGHT cloud lanes metered under OD-14).

## Provenance

- Source profile: `/home/hxsa/opt/local-tkv/agent-zero-docs/agent-profiles/wayne/wayne-profile.yaml`
- Source digest: `sha256:282d151fa8921fe299b24d98ac3f91981d21a7c6734e313f87cec23dc176dc26`
- Source preserved unchanged.
- Operative distillation: `agents/wayne/profile.md` + `agents/wayne/charter.md`.
