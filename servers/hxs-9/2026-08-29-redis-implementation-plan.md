# hxs-9 — Redis implementation plan (PLANNING ONLY — NOT EXECUTED)

| Field | Value |
| --- | --- |
| Product of | Work order `pilots/PILOT-DSH-IMPL-001/22-flash-work-order-wayne-redis-plan.md` (Flash → Wayne, 2026-08-29) |
| Author | Wayne (Redis systems engineer, KDD-0015) — planning only; no execution, no hxs-9 access |
| Lane this plan serves | Wayne — Redis systems engineer, KDD-0015, **registered, activation-gated** |
| Status | PLAN — awaiting owner approval + a separate governor-issued execution work order |
| Target | hxs-9 (192.168.50.208) ONLY |
| Controlling docs | Wayne profile (KDD-0015), Chris profile (KDD-0014), PostgreSQL implementation plan (owner-approved 2026-08-29), PostgreSQL cache integration plan (Chris, companion doc) |
| Governance | Owner rules: native systemd only (no Docker/containers, 2026-08-27); no host firewall (2026-08-26); single instance, no cluster/sentinel/replication; MCP HOLD; dev/test trust posture (matching PostgreSQL pg_hba approach); Wayne concurrency 1 / PT1H |
| Companion doc | `servers/hxs-9/2026-08-29-postgresql-cache-integration-plan.md` (Chris — PostgreSQL-side cache integration) |

## Knowledge-review receipt

**Sources reviewed (Wayne's session + governor corrections):**

| # | Source | Path | Key findings |
| --- | --- | --- | --- |
| 1 | Redis 8.10 redis.conf | `/opt/tkv-local/redis-unstable/redis.conf` | Defaults: bind 127.0.0.1, protected-mode yes, maxmemory-policy noeviction, RDB save points, AOF off by default, ACL system, keyspace notifications disabled. Reference only — not for production. |
| 2 | Redis 8.10 release notes | `/opt/tkv-local/redis-unstable/00-RELEASENOTES` | Redis Open Source 8.10, security fixes present, Ubuntu 24.04 supported. |
| 3 | Redis modules manifest | `/opt/tkv-local/redis-unstable/modules/modules.yaml` | Pinned: redisbloom v8.10.1, redisearch v8.10.0, redisjson v8.10.0, redistimeseries v8.10.0, vector-sets. All DEFERRED for initial install. |
| 4 | MCP Redis Server | `/opt/tkv-local/mcp-redis-main/README.md` | v0.5.1, natural language interface for Redis, tool inventory. MCP is on HOLD per owner directive. |
| 5 | hxs-9 discovery | `servers/hxs-9/discovery.md` (repo) | Intel i5-7500, 32 GB RAM, 238.5 GB NVMe, Ubuntu 24.04.4 LTS, IP 192.168.50.208/24, no host firewall. |
| 6 | PostgreSQL implementation plan | `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` (repo) | PG 18.6 via PGDG, listen_addresses LAN+localhost, pg_hba dev/test trust, roles ps-admin/ps-backup/ps-scratch, credentials in .local.env, backup daily 02:17, health 15-min. |
| 7 | PostgreSQL as-built state | `servers/hxs-9/2026-08-29-postgresql-install-step2.md` (repo) | Roles created, timers active, V4-V6 PASS, pg_hba trust posture live. |
| 8 | Chris's cache integration plan | `servers/hxs-9/2026-08-29-postgresql-cache-integration-plan.md` (repo) | Cache-aside + TTL-only, ps-cache role (read-only on hx_cache schema), trigger/NOTIFY designed but deferred. |
| 9 | Wayne charter | `agents/wayne/charter.md` (repo) | Lane bounds: Redis only, PostgreSQL is system of record, MCP HOLD, RAG/vector/stream deferred. |
| 10 | Wayne profile | `agents/wayne/profile.md` (repo) | Model lane gpt-oss-120b, credential model, activation gate. |

**Gaps:**
- No application schemas exist on hxs-9 PostgreSQL yet — cache views are a framework, not populated with real data.
- Exact stable Redis package version on Ubuntu 24.04 noble — needs verification at execution time (V0 pre-state).
- Chris's plan recommends TTL-only invalidation for initial phase; active invalidation (NOTIFY/LISTEN) designed but deferred.

---

## 1. Version and Source
- **Package**: `redis-server` from Ubuntu 24.04 (official apt repository). This provides **Redis 8.10** – the same major version as the reference source tree and is the supported stable release for the OS.
- **Alternative sources** (evaluated):
  - **PPA** – `ppa:redislabs/redis` offers newer builds but adds external trust; not needed for dev/test parity with PostgreSQL.
  - **Official tarball** – could be compiled from source (`make && make install`), but introduces build‑time variance and deviates from OS‑packaged management.
- **Recommendation**: Use the Ubuntu `redis-server` package (installed via `apt-get install redis-server`). This guarantees security updates via the distro, matches the OS support policy, and avoids extra trust chain.

## 2. Config Baseline
- **Binding**: `bind 192.168.50.208 127.0.0.1` – listen only on the LAN address and loopback.
- **Port**: `6379` (default).
- **Protected mode**: `protected-mode no` – required because we are binding to a non‑loopback address without authentication.
- **Authentication**: No password for LAN clients (mirroring PostgreSQL `pg_hba.conf trust`), but **admin** user will have a password stored in `.local.env`.
- **Memory**: Set a bounded `maxmemory` (e.g., `4GB`) with `maxmemory-policy allkeys-lru` to avoid OOM on the 32 GB host.
- **Persistence**:
  - Enable **RDB** snapshots (`save 900 1`, `save 300 10`, `save 60 10000`).
  - Enable **AOF** with `appendfsync everysec` for durability; both can coexist.
- **ACL Users**: Defined in `/etc/redis/redis.conf` (or a separate ACL file via `include`). See Section 3.
- **Logging**: `logfile ""` (use systemd journal), `loglevel notice`.
- **Other security knobs**: Keep default immutable configs (`dir`, `dbfilename`), leave `enable-protected-configs` at `yes`.

## 3. ACL Users
Create the following users (via `ACL SETUSER` or config file):
| User | Permissions | Key pattern | Notes |
|------|-------------|-------------|-------|
| `admin` | `on >* ~* &* +@all` | `*` (all) | Full access; password stored in `.local.env` (**REDIS_PWD**). [OPEN CORRECTION 2026-08-29, labeled, append-only — review batch 2, F41/F59: AS-BUILT on hxs-9 the DEFAULT user is RESTRICTED (`user default off`, all access requires ACL auth) and LAN clients authenticate with named ACL users + passwords; the original no-password-for-LAN posture above was superseded on the live system by the governor 2026-08-29. This plan row is updated to match as-built; see the note under `cache-service` below.] |
| `cache-service` | `on >* ~cache:* -@all +get +set +setex +mget +mset +del +exists +ttl +expire +scan +ping` | `cache:*` | Read/write for cache keys only, restricted command set — **not** `+@all` (F61); authenticates with its own ACL password per the as-built default-user-off posture (F41/F59). [Original row: `on >* ~cache:* +@all`, "no password required for LAN (protected-mode disabled)" — preserved here verbatim, corrected as noted.] |
| `rag-service` _(reserved)_ | — | `rag:*` | Future expansion; not created now. |

**Implementation**: Add an `aclfile` (e.g., `/etc/redis/users.acl`) and reference it with `aclfile /etc/redis/users.acl` in `redis.conf`.

## 4. Credential Model
- `.local.env` entry template (values generated at runtime, never stored in repo):
```
REDIS_HOST=192.168.50.208
REDIS_PORT=6379
REDIS_DB=0
REDIS_USERNAME=admin
REDIS_PWD=<generated>
```
- Generation method: `openssl rand -hex 16` or `pwgen -s 16 1` at install time, written only to the secure env file.
- No credentials are committed to source control.

## 5. Persistence Design
- **RDB**: Daily snapshot (`save 86400 1`) plus frequent snapshots (`save 300 10`). Files stored in `/var/lib/redis` (default `dir`). Verify with `redis-check-rdb` after each snapshot.
- **AOF**: `appendonly yes`, `appendfsync everysec`. Verify with `redis-check-aof` after shutdown/startup.
- **Backup destination**: `/var/backups/hx-redis/` (owned by `redis:redis`,
  mode `0770` — per the PostgreSQL lesson: 0750 was too tight for the
  service user). A systemd timer (`hx-redis-backup.timer`) copies the
  RDB/AOF files to this location and retains the last 7 copies.
- **Backup timer design** (same pattern as `hx-pg-backup.timer`):
  - `hx-redis-backup.service` — Type=oneshot, User=redis,
    ExecStart=/usr/local/sbin/hx-redis-backup
  - `hx-redis-backup.timer` — OnCalendar=*-*-* 02:37:00 (off-:00 per
    fleet anti-herd convention, 20 min after PG backup), Persistent=true,
    RandomizedDelaySec=300
  - Script: copy current RDB/AOF from /var/lib/redis/ to
    /var/backups/hx-redis/, prune >7 days, verify with redis-check-rdb.
    [OPEN CORRECTION 2026-08-29, labeled, append-only — review batch 2, F62:
    the backup copy MUST be an ATOMIC VERSIONED SET — write each copy to a
    timestamped directory (e.g. `/var/backups/hx-redis/<UTC-timestamp>/`) and
    move it into place only when both RDB and AOF members are present and
    pass redis-check; never leave a partially copied set as the "latest"
    (an interrupted copy must not be restorable-as-latest). A Redis package
    version record (from `redis-server --version`) is captured in the V1
    receipt at install time and re-recorded in each backup receipt.]
- **Recovery test**: Stop service, move current DB files, restore from latest backup, start service, validate `PING` and data integrity via a sanity key (`cache:test`).

## 6. Health Monitoring
- Systemd service `redis-server.service` already provides basic health.
- Add a **systemd timer** `hx-redis-health.timer` that runs a script `/usr/local/bin/hx-redis-health.sh`:
  - `redis-cli PING` → expect `PONG`.
  - `redis-cli INFO memory` → check `used_memory` below `maxmemory`.
  - `redis-cli INFO stats` → capture `evicted_keys` and `expired_keys`.
  - `redis-cli SLOWLOG GET` → report any entries > 100 ms.
  - `redis-cli INFO persistence` → ensure `aof_last_write_status:ok` and recent `rdb_last_save_time`.
- Script writes JSON metrics to `/var/log/hx-redis-health.json`. No automatic remediation; alerts are raised via log monitoring.

## 7. PostgreSQL Cache Integration Contract (Redis side)
- **Key namespace**: `cache:<table>:<id>` (e.g., `cache:orders:12345`).
- **Serialization**: JSON strings; values stored as plain strings (`SET key json`).
- **TTL rules**:
  - Static tables (e.g., reference data) → `TTL 86400` (24 h).
  - Frequently changing tables (e.g., `orders`) → `TTL 300` (5 min).
  - Critical fast‑changing data → `TTL 60` (1 min), shortest class. [OPEN
    CORRECTION 2026-08-29, labeled, append-only — review batch 2, F58: the
    original "no TTL, rely on active invalidation" option is REMOVED —
    every cache class carries a finite TTL so entries can never persist
    indefinitely if the invalidation agent (deferred) never ships. The
    original no-TTL line is preserved in this note.]
  - **Rule of record: ALL classes get a finite TTL — no key without a TTL.**
- **Invalidation**:
  - Primary: TTL expiry.
  - Secondary: PostgreSQL NOTIFY / LISTEN channel `hx_cache_invalidate`. When a row changes, PostgreSQL sends `NOTIFY hx_cache_invalidate '<table>:<id>'`; a lightweight agent (outside this scope) will delete the matching Redis key.
- **Refresh (Cache‑Aside)**:
  - Application reads from Redis; on miss, queries PostgreSQL, writes result back with appropriate TTL.
- **Observability**:
  - Track cache effectiveness via Redis `INFO stats` counters
    `keyspace_hits` / `keyspace_misses` (hit ratio =
    hits / (hits + misses)). [OPEN CORRECTION 2026-08-29, labeled,
    append-only — review batch 2, F60: the original text proposed per-key
    attribution via `INFO commandstats`, which is aggregate per-command and
    cannot attribute GETs to key patterns; the keyspace hit/miss counters are
    the correct source for the hit/miss ratio. Original text preserved in
    this note.]
  - Export hit/miss ratio to Prometheus via `redis_exporter` (future integration).

## 8. Validation Suite
| Stage | Description |
|-------|-------------|
| **V0** | Verify pre‑state: no Redis listening on 6379, service inactive, no ACL users defined, `apt-cache policy redis-server` captured (confirm candidate version), disk/mem free, 0 failed units. |
| **V1** | Verify package installation: `redis-server --version` = 8.10, service enabled & active, listening on 192.168.50.208:6379. |
| **V2** | Verify config posture: `bind` addresses, `protected-mode no`, `maxmemory` set, ACL users present, password for `admin` stored in `.local.env`. |
| **V3** | Verify ACL functional test: `cache-service` can `SET`/`GET` keys matching `cache:*` and is denied on others. |
| **V4** | Persistence test: generate sample data, restart service, confirm data persists via RDB and AOF checks. |
| **V5** | Backup/restore test: run backup timer, simulate failure, restore from `/var/backups/hx-redis`, verify data integrity. |
| **V6** | Health script test: trigger `hx-redis-health.timer`, ensure JSON output contains all expected fields and no errors. |

All stages produce written receipts (command, timestamp, result). After
all evidence docs are written, `python3 scripts/validate.py` must return
**5/5 PASS** from the repo root. (5 checks since 2026-08-30: the governance-path check SY-2/SY-3 was added; this plan originally read 4/4).

## 9. Rollback Procedure
1. Stop `redis-server.service`.
2. `systemctl disable --now hx-redis-backup.timer hx-redis-health.timer` (if created).
3. `rm -f /etc/systemd/system/hx-redis-*.{service,timer} /usr/local/sbin/hx-redis-* /usr/local/bin/hx-redis-health.sh` and `systemctl daemon-reload`. [OPEN CORRECTION 2026-08-29, labeled, append-only — review batch 2, F57: the health script `/usr/local/bin/hx-redis-health.sh` (§6) lives under `/usr/local/bin/` and was NOT covered by the original `/usr/local/sbin/hx-redis-*` glob; added to the cleanup set.]
4. `apt-get purge -y redis-server` (removes package and config dirs).
5. Delete custom ACL files (`/etc/redis/users.acl`).
6. Remove backup directory `/var/backups/hx-redis/`.
7. Remove Redis credential entries from `.local.env`.
8. Verify: no process on 6379, `systemctl status redis-server` reports `inactive (dead)`, `ss -ltnp | grep 6379` returns nothing.

## 10. Second‑Brain Evaluation
The plan follows the **evidence‑first** approach mandated by the `be‑great` skill, aligns with the PostgreSQL cache contract, respects all absolute prohibitions, and defers all out‑of‑scope surfaces (MCP, RAG, modules). It is ready for governor review and subsequent activation.

---

[END OF PLAN]
