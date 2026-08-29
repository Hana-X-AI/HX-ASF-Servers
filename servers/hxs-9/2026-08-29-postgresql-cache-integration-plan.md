# hxs-9 — PostgreSQL-side plan for Redis cache integration (PLANNING ONLY — NOT EXECUTED)

| Field | Value |
| --- | --- |
| Product of | Work order: Chris PostgreSQL-side cache integration plan (Flash → Chris, 2026-08-29) |
| Author | Chris (PostgreSQL systems engineer, KDD-0014) — planning only; no execution, no hxs-9 access |
| Lane | The plan lane Chris owns; the Redis side belongs to Wayne (KDD-0015) |
| Status | PLAN — awaiting owner approval + a separate Kimi-K3-issued execution work order |
| Target | hxs-9 (192.168.50.208) ONLY |
| Controlling docs | Chris profile (KDD-0014), Wayne charter (KDD-0015), PostgreSQL implementation plan (hxs-9, owner-approved 2026-08-29), PostgreSQL install step2 as-built |
| Governance | Owner rules: native systemd only; no host firewall; single instance, no replication/HA; dev/test trust posture; MCP HOLD; Chris concurrency 1 / PT1H; PostgreSQL is the system of record |

## 0. Knowledge-review receipt (MANDATORY — completed before writing)

### 0.1 Sources reviewed

| # | Source | Provenance | What was inspected | Key findings |
| --- | --- | --- | --- | --- |
| 1 | `/opt/tkv-local/redis-unstable/MANIFESTO` | Redis project (unstable branch), reference knowledge tree | Full text (106 lines). Redis design philosophy: DSL for abstract data types, memory-first, fundamental data structures, against complexity, single-threaded core, opportunistic programming. | Redis is fundamentally an in-memory data structure server. Its design favors simplicity and predictable performance. TTL-based expiry is a first-class primitive. The "against complexity" principle strongly favors cache-aside over write-through for the initial integration. |
| 2 | `/opt/tkv-local/redis-unstable/README.md` | Redis project (unstable branch, v8.10+) | Full text (482 lines). Data types: String, JSON, Hash, List, Set, Sorted Set, Stream, Array, Vector Set, probabilistic structures. Use cases: caching, session store, data structure server, NoSQL, search, event store, vector store. Build: needs LLVM 21, CMake 3.25–3.31.6, Rust 1.94. | Redis supports multiple eviction policies (volatile-lru, allkeys-lru, volatile-lfu, allkeys-lfu, volatile-random, allkeys-random, volatile-ttl, noeviction). `maxmemory-policy` defaults to `noeviction`. Pub/Sub is a built-in messaging primitive. This confirms Wayne has all the cache-side primitives he needs: TTLs, eviction, pub/sub for invalidation listeners. |
| 3 | `/opt/tkv-local/redis-unstable/redis.conf` | Redis project (unstable branch), reference | Key sections: SNAPSHOTTING (RDB save points), AOF (appendonly no, appendfsync everysec), maxmemory/maxmemory-policy (noeviction default), lazy freeing, EVENT NOTIFICATION (notify-keyspace-events ""), ACL, expire cycle (active-expire-effort 1). | Persistence: RDB via save points, AOF optional. Keyspace notifications: per-key, per-event pub/sub channels (`__keyspace@<db>__:<key>`, `__keyevent@<db>__:<event>`), 20 event classes (K,E,g,$,l,s,h,z,x,e,n,t,a,d,m,o,c,S,T,I,V,A). Disabled by default. This is the mechanism for active cache invalidation if Wayne needs it. |
| 4 | `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` | Mia (KDD-0012), owner-approved 2026-08-29, Corrections 1–5 applied | Full text (431 lines). Version 18.6 via PGDG, listen_addresses 192.168.50.208+localhost, pg_hba dev/test trust posture (Correction 5), roles ps-admin/ps-backup/ps-scratch, credentials in .local.env, backup daily at 02:17, health 15-min. OUT: Redis (separate lane), all application consumers (removed), replication/HA, MCP. | The instance is up, configured, and validated. The trust posture means `ps-cache` can connect over LAN without SCRAM complexity. Existing role pattern (ps-backup: LOGIN, pg_read_all_data) is the template for `ps-cache`. No application schemas or tables exist — cache views will be a framework, not populated with real data yet. |
| 5 | `servers/hxs-9/2026-08-29-postgresql-install-step2.md` | Governor (Flash, Phase M), as-built evidence 2026-08-29 | Full text (208 lines). Roles: ps-admin (NOLOGIN), ps-admin-login (LOGIN), ps-backup (LOGIN, REPLICATION, pg_read_all_data), ps-scratch (LOGIN). Credentials: 6 HX_PG_ entries in .local.env. Backup/health timers active. V4–V6 PASS. pg_hba reverted to dev/test trust posture. | Confirms the live state. `ps-backup` has `pg_read_all_data` — our `ps-cache` role should follow the same pattern: a LOGIN role with least-required read privileges. The credential entry pattern (HX_PG_*_ROLE / HX_PG_*_PASSWORD) is established and consistent. |
| 6 | `agents/wayne/charter.md` | Wayne registration (KDD-0015), 2026-08-29 | Full text (80 lines). Wayne owns: Redis install/config/ACL/persistence/health on hxs-9, Redis side of cache contract (cache-key structure, serialization, TTLs, invalidation, refresh, observability). Chris owns PostgreSQL side. MCP HOLD for both. RAG/vector/stream DEFERRED. No destructive Redis ops without owner approval. | Boundary is explicit: Wayne defines the cache contract; Chris implements the PostgreSQL side. This means Chris designs the read interfaces, roles, triggers; Wayne decides what keys, TTLs, and serialization to use. The cache-aside pattern is the natural fit — Wayne's service reads from Chris's views, populates Redis with Wayne's key structure and TTLs. |
| 7 | `agents/chris/profile.md` | Chris profile (KDD-0014), owner-revised 2026-08-29 | Full text (157 lines). Owns: single-instance PostgreSQL end-to-end, roles, credentials, backups, monitoring, schema review. Does not own: Redis, application code, replication, MCP. Operating discipline: confirm target/approval before execution, ON_ERROR_STOP, credential hygiene, deterministic toolchain first. Model lane: DeepSeek V4 Pro via OmniRoute. | Chris's lane bounds are clear. This plan is within scope: designing PostgreSQL-side read interfaces, a cache-service role, and optionally triggers for cache invalidation. No Redis-side design, no application logic. |
| 8 | `servers/AGENTS.md` | Project governance, server records contract | Full text (94 lines). Server records: discovery.md (as-found), configuration.md (as-configured). No per-server child AGENTS.md. Records are factual and concise; no credentials in server records. | The plan document is a server-scoped planning artifact under `servers/hxs-9/`. It follows the existing naming convention (`YYYY-MM-DD-<slug>.md`). Must be added to `scripts/wiki/manifest.txt` for rendering. |

### 0.2 Authority hierarchy for this plan

1. **Owner directives** (Agent Zero, via Kimi-K3/Flash, 2026-08-29): dev/test trust posture, single instance, MCP HOLD, PostgreSQL is system of record, no replication/HA.
2. **Chris KDD-0014 profile**: least-required privileges, credential hygiene (values only in `.local.env`), deterministic toolchain first, evidence-backed operations.
3. **Wayne KDD-0015 charter**: cache contract boundary — Wayne owns Redis side (key structure, TTLs, serialization, invalidation mechanism), Chris owns PostgreSQL side (read interfaces, roles, triggers).
4. **PostgreSQL implementation plan** (owner-approved 2026-08-29, Corrections 1–5): version 18.6, listen_addresses, pg_hba trust, role naming pattern (ps-*), credential variable naming pattern (HX_PG_*).
5. **As-built state** (step2.md): roles created, credentials written, timers active, V4–V6 pass.
6. **Redis-unstable reference** (`/opt/tkv-local/`): reference material only — design philosophy, data structures, persistence, pub/sub, keyspace notifications. Verified against documented behavior; not a live instance.

### 0.3 Gaps and unresolved questions

| Gap | Classification | Resolution |
| --- | --- | --- |
| No application schemas or tables exist on hxs-9 PostgreSQL | **Implementation-time** — the plan designs a framework; views are created as templates, instantiated when application data exists | Document the pattern; views are `CREATE OR REPLACE` and can be created now as stubs |
| Wayne's Redis instance does not exist yet | **Owner sequencing decision** — Redis install is Wayne's lane, gated on his activation | This plan is a prerequisite: Wayne needs the PostgreSQL-side interfaces designed before he can implement his cache-service read path |
| Exact cache-key structure, TTL values, serialization format | **Wayne decision** — Wayne owns these per KDD-0015 | Chris designs the read interfaces; Wayne consumes them and decides the Redis-side shape |
| Whether active invalidation (LISTEN/NOTIFY) is needed vs TTL-only | **Owner decision** — this plan recommends TTL-only for initial phase | Document both options with clear recommendation |

---

## 1. Cache-architecture decision

### 1.1 Pattern selection: cache-aside with TTL-based invalidation

**Recommendation of record: cache-aside pattern, TTL-only invalidation for the initial integration phase.**

The pattern works as follows (cache-service is Wayne's lane):

1. Cache-service receives a read request for key K.
2. Cache-service checks Redis for K → miss.
3. Cache-service connects to PostgreSQL as `ps-cache`, queries the designated view.
4. Cache-service populates Redis with the result, setting Wayne's chosen TTL and key structure.
5. Subsequent reads for K hit Redis until the TTL expires.
6. On TTL expiry, Redis auto-evicts K; next read repeats from step 2.

**Rationale:**

| Factor | Cache-aside + TTL | Write-through (triggers) | Write-behind |
| --- | --- | --- | --- |
| PostgreSQL remains system of record | ✓ (reads from PG, writes never bypass PG) | ✓ | ✗ (writes go to Redis first — data-loss risk) |
| Fault tolerance | ✓ (Redis down = stale reads, not lost writes; PG always authoritative) | Partial (trigger failure = cache inconsistency) | ✗ (Redis down = lost writes) |
| Complexity | Low — no triggers, no NOTIFY listeners, no persistent PG connections | Medium — trigger functions, NOTIFY channels, persistent listener connection | High — queue, retry, reconciliation |
| Consistency model | Eventual (TTL-bounded staleness) | Near-real-time (NOTIFY on change) | Eventual with reconciliation |
| Redis design philosophy alignment | ✓ (Redis MANIFESTO §6: "We're against complexity") | Partial — adds coordination | ✗ |
| Operational burden | Low — no new moving parts | Medium — listener process must stay connected, handle reconnection | High |
| Fit for dev/test environment | ✓ | Acceptable but overengineered for dev/test | No |

Cache-aside with TTL-only invalidation is the **correct starting point** for a dev/test environment where:
- The data volume is low (single instance, 238.5 GB NVMe, 233 GB free).
- Eventual consistency is acceptable (the factory is not serving production traffic).
- Simplicity reduces the surface for bugs and operational incidents.
- The pattern can be upgraded to active invalidation later without changing the PostgreSQL-side read interfaces.

### 1.2 Active invalidation option (designed, not deployed)

For tables where TTL-bounded staleness is unacceptable, PostgreSQL LISTEN/NOTIFY provides active cache invalidation. This plan designs the mechanism (§4) but **does not recommend deploying it in the initial phase**. Wayne can request it later for specific tables, and the trigger function, NOTIFY channel convention, and role privileges are already designed here.

---

## 2. Read interfaces — PostgreSQL views for cache-aside population

### 2.1 Schema: `hx_cache`

A dedicated schema `hx_cache` namespaces all cache-related PostgreSQL objects:

```sql
CREATE SCHEMA IF NOT EXISTS hx_cache;
COMMENT ON SCHEMA hx_cache IS 'Cache-integration read interfaces. Owned by Chris (KDD-0014). Read by ps-cache (Wayne''s cache-service).';
```

### 2.2 View pattern

For each application table that needs caching, create a corresponding view in `hx_cache`:

```sql
-- Template pattern — instantiated per table:
CREATE OR REPLACE VIEW hx_cache.<table_name> AS
SELECT
    <primary_key_column> AS id,
    <columns the cache layer needs>,
    -- Include a version/update column if available for cache-key differentiation:
    COALESCE(<updated_at_column>, NOW()) AS _pg_updated_at
FROM <source_schema>.<source_table>;
```

**Design principles:**

- Views are **read-only by construction** — `ps-cache` gets SELECT, nothing more.
- Each view exposes exactly the columns the cache layer needs. No `SELECT *` — explicit column lists prevent schema drift surprises.
- A `_pg_updated_at` column (if the source table has a timestamp) lets Wayne incorporate a version into his cache keys for cache-busting.
- Views live in `hx_cache` schema, separate from application schemas. This keeps the cache contract cleanly namespaced and makes granting privileges trivial (one `GRANT SELECT ON ALL TABLES IN SCHEMA hx_cache`).

### 2.3 Initial stub views

Since no application tables exist yet, create a single stub view that validates the pattern:

```sql
-- Stub view — validates the read-interface contract end-to-end:
CREATE OR REPLACE VIEW hx_cache.health_check AS
SELECT
    current_timestamp AS server_time,
    version() AS pg_version,
    current_database() AS database_name;
```

This stub gives Wayne a concrete target to test his cache-service read path against — he can `SELECT * FROM hx_cache.health_check` and cache the result. When application tables arrive, additional views follow the pattern above.

### 2.4 Privileges

```sql
-- Grant read-only access on the entire cache schema to ps-cache:
GRANT USAGE ON SCHEMA hx_cache TO "ps-cache";
GRANT SELECT ON ALL TABLES IN SCHEMA hx_cache TO "ps-cache";

-- Futre views automatically get the same grant:
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA hx_cache
    GRANT SELECT ON TABLES TO "ps-cache";
```

> **OPEN CORRECTION 2026-08-29, labeled, append-only — review batch 2, F51:**
> the `ALTER DEFAULT PRIVILEGES` statements in this plan (here, §3.2, and
> §7) must carry `FOR ROLE postgres` — default privileges apply only to
> objects created by the role named in the `FOR ROLE` clause, and the
> `hx_cache` schema objects are created under `postgres` (see the
> `OWNER TO postgres` pattern in §4). Without it the grants silently never
> fire. Original unscoped text preserved above in place.

---

## 3. Cache-consistency role: `ps-cache`

### 3.1 Design

Follows the established `ps-backup` pattern (LOGIN, read-only, least-privilege):

| Property | Value |
| --- | --- |
| Role name | `ps-cache` |
| Type | LOGIN |
| Purpose | Cache-service read-only access for cache-aside population |
| Privileges | `USAGE` on `hx_cache` schema, `SELECT` on all tables/views in `hx_cache` |
| Connection limit | 5 (the cache-service should use a connection pool; 5 is generous for a single-instance dev/test cache) |
| Password | Generated at execution via `openssl rand -base64 24` |
| Membership | No group membership; standalone LOGIN role |
| Modeled after | `ps-backup` (LOGIN, read-only, least-privilege, credential entry pattern) |

### 3.2 CREATE ROLE + GRANT statements

```sql
-- Create the cache-service role:
CREATE ROLE "ps-cache" WITH
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT 5
    PASSWORD '<generated_at_execution>';

-- Grant schema access:
GRANT USAGE ON SCHEMA hx_cache TO "ps-cache";

-- Grant read on all existing cache views:
GRANT SELECT ON ALL TABLES IN SCHEMA hx_cache TO "ps-cache";

-- Futre cache views auto-granted:
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA hx_cache
    GRANT SELECT ON TABLES TO "ps-cache";
```

### 3.3 Comparison with existing roles

| Role | Type | Login | Privileges | Purpose |
| --- | --- | --- | --- | --- |
| `ps-admin` | NOLOGIN group | no | (members inherit) | Administration grouping |
| `ps-admin-login` | LOGIN | yes | Member of ps-admin | Day-2 admin operations |
| `ps-backup` | LOGIN | yes | pg_read_all_data | pg_dump service |
| `ps-scratch` | LOGIN | yes | (none beyond scratch DB) | Validation round-trip |
| **`ps-cache`** | **LOGIN** | **yes** | **SELECT on hx_cache schema** | **Cache-service reads** |

`ps-cache` is the **most narrowly privilleged** of all LOGIN roles — it can only read from `hx_cache`, nothing else. This is correct: the cache-service has no business reading system catalogs, other schemas, or writing anything.

---

## 4. Trigger/notification design (active invalidation — FUTURE OPTION)

### 4.1 Recommendation: TTL-only for initial phase

Active invalidation via LISTEN/NOTIFY is **designed here but NOT recommended for the initial deployment**. The TTL-only approach (§1.1) suffices for a dev/test environment. Deploy triggers only when:

- A specific table has staleness requirements shorter than the minimul practical TTL (sub-second or low single-digit seconds).
- Wayne explicitly requests active invalidation for a named table set.
- The additional operational burden (persistent PG connection, listener process, reconnection logic) is accepted.

### 4.2 Trigger function

When deployed, a single trigger function serves all cached tables:

```sql
CREATE OR REPLACE FUNCTION hx_cache.notify_invalidate() RETURNS TRIGGER AS $$
DECLARE
    channel text;
    payload jsonb;
BEGIN
    -- Channel naming: hx_cache_inval_<schema>_<table>
    channel := 'hx_cache_inval_' || TG_TABLE_SCHEMA || '_' || TG_TABLE_NAME;

    -- Payload: operation, table identity, affected key(s)
    payload := jsonb_build_object(
        'op', TG_OP,                              -- INSERT, UPDATE, DELETE, TRUNCATE
        'schema', TG_TABLE_SCHEMA,
        'table', TG_TABLE_NAME,
        'when', now() AT TIME ZONE 'UTC'
    );

    -- For INSERT/UPDATE/DELETE on a row trigger, include the old/new key:
    IF TG_OP IN ('INSERT', 'UPDATE') AND TG_LEVEL = 'ROW' THEN
        payload := payload || jsonb_build_object('new_id', to_jsonb(NEW));
    ELSIF TG_OP = 'DELETE' AND TG_LEVEL = 'ROW' THEN
        payload := payload || jsonb_build_object('old_id', to_jsonb(OLD));
    END IF;

    -- Fire the NOTIFY:
    PERFORM pg_notify(channel, payload::text);

    -- Return appropriatley for the trigger type:
    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function owned by the bootstrap superuser; SECURITY DEFINER so it can
-- call pg_notify regardless of who performs the triggering DML.
ALTER FUNCTION hx_cache.notify_invalidate() OWNER TO postgres;
```

### 4.3 NOTIFY chanel naming convention

| Channel | Meaning |
| --- | --- |
| `hx_cache_inval_<schema>_<table>` | A row in `<schema>.<table>` changed. Wayne's cache-service subscibes to relevant channels and invalidates the corresponding Redis keys. |

Exaple: a change to `public.usrs` fires on `hx_cache_inval_public_usrs`.

Wayne's cache-service subscibes with:

```sql
LISTEN hx_cache_inval_public_usrs;
```

### 4.4 Trigger attachment (per-table, future)

```sql
-- Exaple: attach to public.users when that table exists:
CREATE TRIGGER cache_inval_trigger
    AFTER INSERT OR UPDATE OR DELETE ON public.users
    FOR EACH ROW
    EXECUTE FUNCTION hx_cache.notify_invalidate();
```

### 4.5 Why NOTIFY is the right mechanism (vs alternatives)

| Mechanism | Pros | Cons | Verdict |
| --- | --- | --- | --- |
| **LISTEN/NOTIFY** | Built into PostgreSQL; no polling; works over existing PG connection; payload is arbitrary JSON; no external deps. | Listener must hold a persistent PG connection. | ✓ Recommended for PG-side invalidation |
| pg_cron polling | No persistent connection needed. | Polls — adds latency, wastes resources, requires pg_cron extension. | ✗  Heavier than NOTIFY |
| Redis keyspace notifications | No PG-side trigger needed. | Requires `notify-keyspace-events` enabled in Redis (off by default); only fires on Redis-side changes — doesn't help when PG is the source of truth. | ✗  Wrong direction: Redis can't notify about PG changes |
| External message broker (Redis pub/sub) | Decouples PG from cache-service. | Adds infrastructure; trigger would PUBLISH to Redis channel from PG — needs a PG extension (pg_redis, etc.) or an external listener. | ✗  Over-enginered for single-instance dev/test |

LISTEN/NOTIFY is the **simplest mechanism that works**: it is native to PostgreSQL, requires no extensions, and the cache-service already needs a PG connection to read views. The persistent-connection requirement is acceptable — the cache-service is a long-lived process by nature.

### 4.6 Privileges for NOTIFY

The `ps-cache` role needs no special privilege to `LISTEN`. To receive NOTIFY, it just needs to be connected. The trigger function runs as `SECURITY DEFINER` owned by `postgres`, so it can call `pg_notify()` regardless of who performed the triggering DML.

---

## 5. Credential entries

### 5.1 New entries in `.local.env`

Following the established pattern (HX_PG_*_ROLE / HX_PG_*_PASSWORD):

```text
# Added at cache-integration execution:
HX_PG_CACHE_ROLE=ps-cache
HX_PG_CACHE_PASSWORD=<generated_at_execution>
```

### 5.2 Rules (per Chris charter §2, §4)

- Variable references only outside the store.
- Passwords never printed, logged, or committed.
- Generation via `openssl rand -base64 24` at execution.
- No values in this plan.
- Access: Chris-only for PostgreSQL entries.
- File: `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`.

### 5.3 Complete PostgreSQL credential entry map (after execution)

| Variable | Value | Owner |
| --- | --- | --- |
| `HX_PG_HOST` | `192.168.50.208` | Chris |
| `HX_PG_PORT` | `5432` | Chris |
| `HX_PG_ADMIN_ROLE` | `ps-admin` | Chris |
| `HX_PG_ADMIN_PASSWORD` | `<generated>` | Chris |
| `HX_PG_BACKUP_ROLE` | `ps-backup` | Chris |
| `HX_PG_BACKUP_PASSWORD` | `<generated>` | Chris |
| **`HX_PG_CACHE_ROLE`** | **`ps-cache`** | **Chris** |
| **`HX_PG_CACHE_PASSWORD`** | **`<generated>`** | **Chris** |

---

## 6. Validation — end-to-end cache contract verification

### 6.1 Cache-service role can connect and read

```sql
-- Connect as ps-cache:
psql -h 192.168.50.208 -U ps-cache -d postgres -c "
SELECT current_user, current_database();
SELECT * FROM hx_cache.health_check;
"
```

**Pass criterion:** connection succeeds; `current_user` = `ps-cache`; `health_check` returns one row with server_time, pg_version, database_name.

### 6.2 Cache-aside round-trip test (manual)

This test validates the full cache-aside contract end-to-end. It assumes Wayne's Redis instance and cache-service exist. Until then, steps 2–4 are **deferred**.

| Step | Actor | Action | Verification |
| --- | --- | --- | --- |
| 1 | Chris | `SELECT * FROM hx_cache.health_check` via ps-cache | Returns row R₁ |
| 2 | Wayne | Cache-service reads `health_check` view, populates Redis key `cache:health_check:1` with TTL 60s | Redis GET returns serialized R₁ |
| 3 | Wayne | Cache-service reads Redis key `cache:health_check:1` | Returns R₁ (cache hit) |
| 4 | Wayne | Wait 65s (TTL + grace), re-read Redis | Returns nil (expired), cache-service re-populates from PG |
| 5 | Chris | Verify `ps-cache` cannot write: `CREATE TABLE hx_cache.test_write (id int)` | **Must fail** (permission denied) |

Steps 1 and 5 **can be executed now** (Chris only, no Redis dependency). Steps 2–4 are deferred until Wayne's Redis instance is live.

### 6.3 NOTIFY test (if active invalidation is deployed)

```sql
-- Terminal 1: LISTEN
psql -h 192.168.50.208 -U ps-cache -d postgres -c "LISTEN hx_cache_inval_test;"
-- NOTE (review batch 2, F50, 2026-08-29, labeled): a one-shot `psql -c
-- LISTEN ...` process exits immediately and never receives the NOTIFY —
-- LISTEN requires a persistent client connection for the channel's whole
-- receive window. For this verification, run the listen terminal
-- interactively (bare `psql`, then the LISTEN statement) or use a psql
-- session that stays open while Terminal 2 fires. Execution-time fix; the
-- production cache-service is a long-lived process and already satisfies
-- this (§5).

-- Terminal 2: Fire NOTIFY
psql -h 192.168.50.208 -U ps-admin-login -d postgres -c "
CREATE TABLE IF NOT EXISTS hx_cache._test_notify (id int);
CREATE TRIGGER _test_notify_trig
    AFTER INSERT ON hx_cache._test_notify
    FOR EACH ROW EXECUTE FUNCTION hx_cache.notify_invalidate();
INSERT INTO hx_cache._test_notify VALUES (1);
DROP TRIGGER _test_notify_trig ON hx_cache._test_notify;
DROP TABLE hx_cache._test_notify;
"
```

**Pass criterion:** Terminal 1 receives a NOTIFY message on channel `hx_cache_inval_hx_cache__test_notify` with payload containing `"op": "INSERT"`.

**Validated only if active invalidation is deployed.** TTL-only phase skips this.

---

## 7. Rollback

Every artifact created by this plan has a pre-defined inverse:

| Artifact | Inverse (exact) |
| --- | --- |
| Cache schema | `DROP SCHEMA IF EXISTS hx_cache CASCADE;` — removes all views, trigger functions, and default privileges in the schema. |
| Cache role | `DROP ROLE IF EXISTS "ps-cache";` — revokes all privileges, removes the role. |
| Trigger function | Covered by `DROP SCHEMA hx_cache CASCADE` above (the function lives in hx_cache). |
| Triggers on application tables | `DROP TRIGGER IF EXISTS cache_inval_trigger ON <schema>.<table>;` per table. Triggers are on application schemas, not in hx_cache — must be dropped individually or as part of the owning migration. |
| Credential entries | Remove `HX_PG_CACHE_ROLE` and `HX_PG_CACHE_PASSWORD` lines from `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env` (Chris only). |

**Rollback ordering:** credentials first (they reference the role), then triggers on application tables, then the schema (which cascades to views/functions), then the role.

---

## 8. Work breakdown for execution (ordered, one lane)

Execution requires a **separate owner-approved work order**. All steps are Chris's lane (PostgreSQL DBA).

### Step 0 — Pre-state gate
- Verify hxs-9 is reachable, PostgreSQL is up, existing roles intact.
- Verify no `ps-cache` role or `hx_cache` schema already exists (idempotency check).
- Record pre-state.

### Step1 — Create schema + stub view
```sql
CREATE SCHEMA hx_cache;
COMMENT ON SCHEMA hx_cache IS 'Cache-integration read interfaces...';
CREATE OR REPLACE VIEW hx_cache.health_check AS SELECT ...;
```

### Step2 — Create cache role + password + grants
```sql
CREATE ROLE "ps-cache" WITH LOGIN ... PASSWORD '<generated>';
GRANT USAGE ON SCHEMA hx_cache TO "ps-cache";
GRANT SELECT ON ALL TABLES IN SCHEMA hx_cache TO "ps-cache";
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA hx_cache GRANT SELECT ON TABLES TO "ps-cache";
```

### Step3 — Write credential entries
Append `HX_PG_CACHE_ROLE` and `HX_PG_CACHE_PASSWORD` to `.local.env`.

### Step4 — Create trigger function (even if not deployed yet)
```sql
CREATE OR REPLACE FUNCTION hx_cache.notify_invalidate() ...;
```
The function is harmless when not attached to any trigger. Creating it now means it is ready when Wayne needs active invalidation.

### Step5 — Run validation §6.1 and §6.2 Step 1 + Step 5
Produce the evidence receipt.

### Step6 — (Deferred) Attach triggers if active invalidation is requested
Per-table, per a separate Wayne-initiated work order.

### Checkpoint — Owner review
Review: role created, credentials written, stub view readable, `ps-cache` cannot write. Acceptance ⇒ cache contract PostgreSQL side is complete; Wayne can begin his Redis-side implementation against the live `hx_cache.health_check` view.

---

## 9. Second Brain evaluation (mandatory per AGENTS.md)

1. **Opportunity identified: yes** — the `ps-cache` role pattern (LOGIN, read-only, schema-scoped, least-privilege), the `hx_cache` schema convention, the view-template pattern, and the NOTIFY trigger function are all catalog-able factory patterns for any future PostgreSQL-to-cache integration.
2. **Applicable pattern:** the existing `ps-backup` role pattern (LOGIN, read-only, pg_read_all_data, credential entries in .local.env) is directly reused and narrowed for `ps-cache`. The credential variable naming convention (`HX_PG_*_ROLE` / `HX_PG_*_PASSWORD`) is consistent.
3. **Disposition: recommended for cataloging at execution handoff.** The plan is the reusable artifact. Carol (Second Brain) receives the plan record at handoff per the catalog discipline. Cataloging before owner approval would record an unratified design.
4. **Reason:** the plan itself is a versioned, repeatable recipe. The cache-aside pattern with TTL invalidation, the `hx_cache` schema approach, and the NOTIFY trigger function are generalizable beyond this specific Redis integration on hxs-9.

---

## 10. Constraints compliance

| Constraint | Held |
| --- | --- |
| PostgreSQL is the system of record — Redis never replaces it | ✓ — all reads originate from PG views; cache-service is a read-only consumer |
| Chris designs PostgreSQL side ONLY; Wayne owns Redis side | ✓ — this plan defines read interfaces, role, optional triggers; no cache-key, TTL, or serialization decisions |
| No schema changes beyond what the cache contract requires | ✓ — one new schema (`hx_cache`), one new role (`ps-cache`), optional trigger function; no changes to existing schemas/tables/roles |
| MCP on HOLD — no postgres-mcp-mai | ✓ — no MCP usage in this plan |
| Native systemd — no Docker | ✓ — no Docker references |
| No host firewall | ✓ — LAN trust posture already in place; ps-cache connects over 192.168.50.208:5432 |
| hxs-9 ONLY | ✓ |
| No secret values in any artifact | ✓ — passwords are `<generated_at_execution>` placeholders; values live only in .local.env at execution |
| PLANNING ONLY — no execution, no hxs-9 access, no SSH | ✓ — this is a plan document; execution requires a separate owner-approved work order |

---

*End of plan. Nothing in this document has been executed. The cache-integration PostgreSQL side awaits owner approval + a separate Kimi-K3-issued execution work order. The Redis side (Wayne) is a separate lane, gated on Wayne's activation and this plan's approval.*