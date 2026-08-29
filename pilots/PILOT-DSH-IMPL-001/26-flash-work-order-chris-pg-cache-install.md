# WORK ORDER — Chris: PostgreSQL cache integration on hxs-9 (EXECUTION)

- Issuer: Flash (governor), 2026-08-29. Owner approved the plan.
- Executor: Chris (PostgreSQL systems engineer, KDD-0014).
- Lane: `omniroute/deepseek-v4-pro-baidu` (DeepSeek V4 Pro, Baidu FP8, via OmniRoute hxs-8).
- Target: hxs-9 (192.168.50.208) ONLY.
- Controlling plan: `servers/hxs-9/2026-08-29-postgresql-cache-integration-plan.md` (owner-approved 2026-08-29).

## Intent

Create the PostgreSQL-side cache integration per the approved plan:
hx_cache schema, ps-cache role, views, trigger function (designed but
not attached), credentials, and validation.

## Steps (per the plan)

1. **Lane verification** — session-start probe, verify served-model id.
2. **SSH to hxs-9** — askpass 0700, deleted after.
3. **Create schema** — `CREATE SCHEMA hx_cache`.
4. **Create ps-cache role** — LOGIN, read-only, `GRANT USAGE ON SCHEMA hx_cache TO ps-cache`, `GRANT SELECT ON ALL TABLES IN SCHEMA hx_cache TO ps-cache`, `ALTER DEFAULT PRIVILEGES IN SCHEMA hx_cache GRANT SELECT TO ps-cache`.
5. **Set password** — `ALTER ROLE ps-cache PASSWORD '<generated via openssl rand>'`.
6. **Create stub views** — `hx_cache.health_check` view (for immediate contract validation). Pattern: one view per cached table (future), explicit column lists, `_pg_updated_at` for versioning.
7. **Create trigger function** — `hx_cache.notify_invalidate()` (SECURITY DEFINER, NOTIFY channel `hx_cache_inval_<schema>_<table>`, JSON payload). NOT attached to any table — ready for future use.
8. **Credentials** — write HX_PG_CACHE_ROLE=ps-cache, HX_PG_CACHE_PASSWORD=<generated> to `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`.
9. **Validation** — ps-cache connect + read (SELECT from hx_cache.health_check works), cache-aside round-trip (deferred until Redis is running — Wayne's parallel task), NOTIFY test (deferred).
10. **Evidence doc** — write `servers/hxs-9/2026-08-29-postgresql-cache-integration-evidence.md`.
11. **Validate** — `python3 scripts/validate.py` 4/4 PASS, render if manifest-listed.

## Constraints

- PostgreSQL is the system of record — Redis never replaces it.
- You design the PostgreSQL side ONLY.
- No schema changes beyond hx_cache and the cache contract.
- MCP HOLD — no postgres-mcp-mai.
- hxs-9 ONLY.
- Secret hygiene: askpass 0700, deleted after, password never printed/logged/committed.
- Wayne's Redis install runs in parallel — coordinate the end-to-end validation after both are done.
- `scripts/validate.py` 4/4 after repo writes.
- Concurrency 1, max session PT1H.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` when schema/role/views/trigger created, credentials written, ps-cache validation passes, evidence doc written, validate.py 4/4 PASS.
