# WORK ORDER — Wayne: Redis implementation plan for hxs-9 (knowledge review + plan)

- Issuer: Flash (governor), 2026-08-29.
- Executor: Wayne (Redis systems engineer, KDD-0015).
- Lane: `omniroute/gpt-oss-120b` (OpenAI gpt-oss-120b, AkashML, via OmniRoute hxs-8).
- Target: hxs-9 (192.168.50.208) — PLANNING ONLY, no execution, no hxs-9 access.

## Intent

Produce a Redis implementation plan for hxs-9 — standalone instance, no
cluster/sentinel/replication, native systemd, dev/test posture (matching
the PostgreSQL approach: trust on LAN, no hardening beyond baseline).
Include ACL users, persistence, health monitoring, and the Redis side of
the PostgreSQL cache integration contract.

## Knowledge review (MANDATORY — do this FIRST, before writing anything)

Use the **be-great** skill (evidence-first investigation). Deep-dive the
Redis corpus at `/opt/tkv-local` to build a complete understanding:

1. `/opt/tkv-local/redis-unstable/` — Redis 8.10 Open Source source tree.
   Read the redis.conf (the full commented config — it documents every
   setting). Read 00-RELEASENOTES. Read modules/modules.yaml (pinned
   module versions: redisbloom v8.10.1, redisearch v8.10.0, redisjson
   v8.10.0, redistimeseries v8.10.0, vector-sets). Read the Makefile
   for build/install patterns. Read src/acl.c headers and commands.def
   for ACL command categories. This is REFERENCE ONLY — never deploy
   redis-unstable to production; use the stable release.

2. `/opt/tkv-local/mcp-redis-main/` — MCP Redis Server v0.5.1. Read
   README.md (tool inventory, connection model, permissions). Read
   pyproject.toml (dependencies, version). This is for FUTURE scope
   awareness — MCP is on HOLD per owner directive. Do not configure it.

3. `servers/hxs-9/discovery.md` — hardware (Intel i5-7500, 32 GB RAM,
   238.5 GB NVMe, Ubuntu 24.04), OS state, disk layout.

4. `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` —
   PostgreSQL config, roles, credential model, backup/health patterns.
   You are caching FOR this system — understand it.

5. `servers/hxs-9/2026-08-29-postgresql-install-step2.md` — as-built
   PostgreSQL state (roles: ps-admin, ps-backup, ps-scratch; timers:
   hx-pg-backup, hx-pg-health; pg_hba: trust on LAN).

6. `agents/wayne/charter.md` and `agents/wayne/profile.md` — your own
   lane bounds and the cache contract definition.

Write a knowledge-review receipt at the start of your plan document:
what you reviewed, provenance, version numbers, key findings, gaps.

## Plan document

Write to: `servers/hxs-9/2026-08-29-redis-implementation-plan.md`

Follow the same shape as the PostgreSQL implementation plan. The plan
must include:

1. **Version and source** — stable Redis 8.10 via official channel
   (NOT redis-unstable). Identify the official stable package source
   for Ubuntu 24.04 (PPA, official tarball, or Snap — evaluate and
   recommend with evidence).
2. **Config baseline** — bind LAN+loopback (192.168.50.208 + 127.0.0.1),
   port 6379, dev/test auth posture (no password required from LAN,
   matching pg_hba trust approach), maxmemory policy (e.g., allkeys-lru
   with a bounded maxmemory), persistence mode (RDB and/or AOF — evaluate
   and recommend).
3. **ACL users** — admin (full access), cache-service (read/write on
   cache:* key pattern only), future RAG-service (key pattern reserved,
   not configured). Least-privilege key patterns, no wildcard keyspaces.
4. **Credential model** — entries in
   `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`:
   REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_USERNAME, REDIS_PWD.
   Same pattern as PostgreSQL (values generated at execution, never
   in the plan).
5. **Persistence design** — RDB snapshot schedule or AOF appendfsync,
   backup destination (/var/backups/hx-redis/), recovery test procedure.
6. **Health monitoring** — systemd timer + script (same pattern as
   hx-pg-health): PING, memory, connected clients, persistence status,
   slowlog. No automatic production changes.
7. **PostgreSQL cache integration contract (Redis side)** — cache-key
   structure (e.g., cache:<table>:<id>), serialization format (JSON?),
   TTL rules per data class, invalidation strategy (TTL expiry vs
   active invalidation via LISTEN/NOTIFY), refresh behavior (cache-aside
   pattern), observability (hit/miss metrics).
8. **Validation suite** — V0 (pre-state: no Redis, no 6379), V1 (install
   + version), V2 (service up + listener), V3 (config posture + ACL),
   V4 (ACL user connect + read/write), V5 (persistence + recovery test),
   V6 (timer + health).
9. **Rollback** — full inverse (purge, remove config, remove timers).
10. **Second Brain evaluation** — mandatory statement per AGENTS.md.

## Constraints

- Standalone topology ONLY — no cluster, sentinel, replication, failover.
- MCP on HOLD — no mcp-redis-main deployment.
- RAG/vector/stream DEFERRED — no RedisJSON, RediSearch, RedisBloom,
  RedisTimeSeries, or vector-sets configuration in the initial install.
  Modules can be loaded but not configured.
- Native systemd — no Docker/containers.
- No host firewall (LAN is the boundary).
- hxs-9 ONLY.
- Write-first discipline: create the plan skeleton first, fill sections
  incrementally. If context tightens, stop and close per the gates below.
- `python3 scripts/validate.py` 4/4 after writes.
- Render any manifest-listed .md you create (add it to manifest.txt).
- No secret values in any artifact.
- PLANNING ONLY — no execution, no hxs-9 access, no SSH.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` when the plan document is written
with all 10 sections filled, knowledge-review receipt included, and
validate.py 4/4 PASS pasted.
`[TASK PAUSED — ESCALATION TO GOVERNOR]` with the named remainder if
anything blocks or the context budget is exhausted.
