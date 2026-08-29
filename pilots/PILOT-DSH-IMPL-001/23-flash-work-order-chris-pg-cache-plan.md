# WORK ORDER — Chris: PostgreSQL-side plan for Redis cache integration

- Issuer: Flash (governor), 2026-08-29.
- Executor: Chris (PostgreSQL systems engineer, KDD-0014).
- Lane: `omniroute/deepseek-v4-pro-baidu` (DeepSeek V4 Pro, Baidu FP8, via OmniRoute hxs-8).
- Target: hxs-9 (192.168.50.208) — PLANNING ONLY, no execution, no hxs-9 access.

## Intent

Produce the PostgreSQL-side plan for the Redis cache integration — what
changes PostgreSQL needs to support the cache contract. You own PostgreSQL;
Wayne owns Redis. You design the read interfaces, views, roles, and triggers
the cache layer needs. PostgreSQL remains the system of record.

## Knowledge review (MANDATORY — do this FIRST, before writing anything)

Use the **be-great** skill (evidence-first investigation). Deep-dive:

1. `/opt/tkv-local/redis-unstable/` — understand Redis data structures
   (strings, hashes, JSON, sets, sorted sets), TTLs, and cache patterns
   (cache-aside, write-through, write-behind). Read redis.conf for
   understanding of how Redis persists and expires data. Read the
   README.md or MANIFESTO for Redis design philosophy. This is REFERENCE
   ONLY — you are understanding the system that will cache YOUR data.

2. `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` — your
   own plan: roles (ps-admin, ps-backup, ps-scratch), credential model,
   backup/health patterns.

3. `servers/hxs-9/2026-08-29-postgresql-install-step2.md` — your as-built
   state: roles created, timers enabled, pg_hba trust posture, backup
   running.

4. `agents/wayne/charter.md` — Wayne's lane boundary and the cache
   contract definition. The contract: Wayne owns cache-key structure,
   TTLs, invalidation, serialization on the Redis side. You own the
   PostgreSQL side: read interfaces, views, roles, triggers.

5. Your own profile (`agents/chris/profile.md`) — your lane bounds.

Write a knowledge-review receipt at the start of your plan document:
what you reviewed, provenance, key findings, gaps.

## Plan document

Write to: `servers/hxs-9/2026-08-29-postgresql-cache-integration-plan.md`

The plan must include:

1. **Read interfaces** — what PostgreSQL views or queries the cache
   layer reads from for cache-aside population. Define the specific
   tables/views a cache-service would read to populate Redis cache
   entries. Include the SQL for any views that need to be created.

2. **Cache-consistency role** — a PostgreSQL role Wayne's cache service
   can use for read-only validation (bounded SELECT on specific views/
   tables). Follow the same role pattern as ps-backup (LOGIN, read-only,
   least-privilege). Include the CREATE ROLE + GRANT statements.

3. **Trigger/notification design** — if cache invalidation uses
   PostgreSQL LISTEN/NOTIFY or triggers, design the PostgreSQL side:
   - Which tables need triggers to notify on change
   - The trigger function SQL
   - The NOTIFY channel naming convention
   - Or: if invalidation is TTL-only (no active invalidation), state
     that and explain why

4. **Credential entries** — any new PostgreSQL role/password for the
   cache integration. Entries in
   `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`:
   HX_PG_CACHE_ROLE, HX_PG_CACHE_PASSWORD. Same pattern as existing
   PostgreSQL credentials (values generated at execution, never in
   the plan).

5. **Validation** — how to verify the cache contract works end-to-end:
   - Cache-service role can connect and read the designated views
   - Triggers fire and NOTIFY messages are produced (if applicable)
   - A cache-aside round-trip works (read from PG → populate Redis →
     read from Redis → verify match)

6. **Rollback** — DROP VIEW, DROP ROLE, DROP TRIGGER/FUNCTION, remove
   credential entries.

7. **Second Brain evaluation** — mandatory statement per AGENTS.md.

## Constraints

- PostgreSQL is the system of record — Redis never replaces it.
- You design the PostgreSQL side ONLY; Wayne owns the Redis side.
- No schema changes beyond what the cache contract requires.
- MCP on HOLD — no postgres-mcp-mai.
- Native systemd — no Docker.
- No host firewall.
- hxs-9 ONLY.
- Write-first discipline: skeleton first, fill incrementally.
- `python3 scripts/validate.py` 4/4 after writes.
- Render any manifest-listed .md you create (add it to manifest.txt).
- No secret values in any artifact.
- PLANNING ONLY — no execution, no hxs-9 access, no SSH.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` when the plan document is written
with all 7 sections filled, knowledge-review receipt included, and
validate.py 4/4 PASS pasted.
`[TASK PAUSED — ESCALATION TO GOVERNOR]` with the named remainder if
anything blocks or the context budget is exhausted.
