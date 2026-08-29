# hxs-9 PostgreSQL cache integration — evidence record

| Field | Value |
| --- | --- |
| Task | Work order: Chris PostgreSQL-side cache integration execution (Flash → Chris, 2026-08-29) |
| Executor | Chris (PostgreSQL systems engineer, KDD-0014) |
| Lane | DeepSeek V4 Pro, Baidu FP8, via OmniRoute hxs-8 |
| Target | hxs-9 (192.168.50.208) ONLY |
| Controlling plan | `servers/hxs-9/2026-08-29-postgresql-cache-integration-plan.md` (owner-approved 2026-08-29) |
| Window | 2026-08-29 ~05:02 → 05:04 UTC |
| Credential handling | ps-cache password generated via `openssl rand -base64 24` locally; set on hxs-9 via ALTER ROLE; written to `.local.env` only. SSH password via temp askpass helper (mode 0700), deleted after use. No password values printed, logged, or committed. |
| Result | **PASS — schema, role, views, trigger function created; credentials written; ps-cache validation passes** |

## 1. Pre-state gate

- hxs-9 reachable (ping 0.2ms), PostgreSQL 18.6 active
- `ps-cache` role: absent ✓
- `hx_cache` schema: absent ✓
- Existing roles: ps-admin, ps-admin-login, ps-backup, ps-scratch, postgres — all intact
- pg_hba: LAN trust posture (192.168.50.0/24 trust) — confirmed from step2

## 2. Schema creation

```sql
CREATE SCHEMA hx_cache;
COMMENT ON SCHEMA hx_cache IS 'Cache-integration read interfaces. Owned by Chris (KDD-0014). Read by ps-cache (Wayne''s cache-service).';
```
**Result:** schema created. Owner: postgres (bootstrap superuser).

## 3. Stub view creation

```sql
CREATE OR REPLACE VIEW hx_cache.health_check AS
SELECT
    current_timestamp AS server_time,
    version() AS pg_version,
    current_database() AS database_name;
```
**Result:** view created. Validates the read-interface contract — Wayne's cache-service can `SELECT * FROM hx_cache.health_check` immediately.

## 4. Cache role creation

```sql
CREATE ROLE "ps-cache" WITH
    LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE
    INHERIT NOREPLICATION CONNECTION LIMIT 5
    PASSWORD '<generated>';
```

| Property | Value |
| --- | --- |
| Role name | ps-cache |
| Login | yes |
| Superuser | no |
| Create DB | no |
| Create role | no |
| Replication | no |
| Connection limit | 5 |
| Password | generated via `openssl rand -base64 24` |

**Result:** role created. Most narrowly privileged of all LOGIN roles.

## 5. Grants

```sql
GRANT USAGE ON SCHEMA hx_cache TO "ps-cache";
GRANT SELECT ON ALL TABLES IN SCHEMA hx_cache TO "ps-cache";
ALTER DEFAULT PRIVILEGES IN SCHEMA hx_cache GRANT SELECT ON TABLES TO "ps-cache";
```
**Result:** grants applied. Default privileges confirmed: `ps-cache=r/postgres` on future tables in hx_cache.

## 6. Trigger function (designed, not attached)

```sql
CREATE OR REPLACE FUNCTION hx_cache.notify_invalidate() RETURNS TRIGGER AS $$
-- Channel: hx_cache_inval_<schema>_<table>
-- Payload: JSON with op, schema, table, when, new_id/old_id
-- SECURITY DEFINER, owned by postgres
$$ LANGUAGE plpgsql SECURITY DEFINER;
```
**Result:** function created (`prosecdef=t`). Not attached to any table — ready for future active invalidation deployment.

## 7. Credential entries

Appended to `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`:

```
HX_PG_CACHE_ROLE=ps-cache
HX_PG_CACHE_PASSWORD=<generated>
```

- File perms: 0600 (unchanged)
- Total HX_PG_ entries: 8 (6 pre-existing + 2 new)
- Pattern: consistent with HX_PG_BACKUP_ROLE/HX_PG_BACKUP_PASSWORD convention

## 8. Validation results

### V7a — ps-cache connect + identity
```
 current_user | current_database
--------------+------------------
 ps-cache     | postgres
```
**PASS** — connection succeeds, identity correct.

### V7b — health_check readable
```
          server_time          |                             pg_version                              | database_name
-------------------------------+---------------------------------------------------------------------+---------------
 2026-08-29 05:04:01.324452+00 | PostgreSQL 18.6 ...                                                  | postgres
```
**PASS** — one row returned with server_time, pg_version, database_name.

### V7c — write denied
```
ERROR: permission denied for schema hx_cache
```
**PASS** — ps-cache cannot CREATE TABLE in hx_cache.

### V7d — least-privilege: pg_authid denied
```
ERROR: permission denied for table pg_authid
```
**PASS** — ps-cache cannot read system catalogs beyond its grants.

### V7e — Schema objects confirmed
```
  schema  |     name     | relkind
----------+--------------+---------
 hx_cache | health_check | v
```
**PASS** — health_check view present in hx_cache schema.

### V7f — Role attributes confirmed
```
 rolname  | rolsuper | rolinherit | rolcreaterole | rolcreatedb | rolcanlogin | rolreplication | rolconnlimit
----------+----------+------------+---------------+-------------+-------------+----------------+--------------
 ps-cache | f        | t          | f             | f           | t           | f              |            5
```
**PASS** — LOGIN, no superuser, no create privileges, connlimit 5.

### V7g — Default privileges confirmed
```
 defaclrole | defaclobjtype |          defaclacl
------------+---------------+-----------------------------
 postgres   | r             | {"\"ps-cache\"=r/postgres"}
```
**PASS** — future tables in hx_cache auto-grant SELECT to ps-cache.

### V7h — Trigger function confirmed
```
      proname      | prosecdef
-------------------+-----------
 notify_invalidate | t
```
**PASS** — SECURITY DEFINER function exists in hx_cache, not attached to any table.

### V7i — Role comparison
```
  rolname   | rolcanlogin | rolconnlimit
------------+-------------+--------------
 ps-backup  | t           |           -1
 ps-cache   | t           |            5
 ps-scratch | t           |           -1
```
**PASS** — ps-cache is the most constrained LOGIN role (connlimit 5 vs unlimited for others).

## 9. Deferred validation

Per the plan §6.2 and §6.3:

| Test | Status | Dependency |
| --- | --- | --- |
| Cache-aside round-trip (Steps 2–4) | **DEFERRED** | Wayne's Redis instance + cache-service must be live |
| NOTIFY test | **DEFERRED** | Active invalidation not deployed (TTL-only phase); trigger function is ready |

Wayne can validate his end immediately against `SELECT * FROM hx_cache.health_check` as ps-cache.

## 10. Constraints compliance

| Constraint | Held |
| --- | --- |
| PostgreSQL is system of record — Redis never replaces it | ✓ — all reads originate from PG views; ps-cache is read-only |
| Chris designs PostgreSQL side ONLY | ✓ — no Redis-side decisions |
| No schema changes beyond hx_cache and cache contract | ✓ — one new schema, one new role, one view, one function; no changes to existing objects |
| MCP HOLD | ✓ — no MCP usage |
| hxs-9 ONLY | ✓ |
| Secret hygiene | ✓ — askpass 0700, deleted; password never printed/logged/committed |
| `scripts/validate.py` 4/4 after repo writes | ✓ (see next section) |

## 11. Post-write validation

```
HX-ASF validate — read-only local validation (UD1/UD2, 2026-08-25) — mode: full repo
PASS  wiki-sync — render.py --check: 58/58 manifest documents in sync
PASS  fixture-suite — unittest 57 tests OK; sha256sums 10/10 verified
PASS  catalog-mechanical — 313 records: schema/required/enums/source.section OK
PASS  secret-boundary — repo-wide: 916 files scanned, 0 hits
RESULT: PASS — 4/4 checks, 4 manual gates noted (exit 0)
```

---

*End of evidence record. The PostgreSQL-side cache integration is complete. Wayne can begin Redis-side implementation against the live `hx_cache.health_check` view. Cache-aside round-trip validation deferred until Redis is running.*