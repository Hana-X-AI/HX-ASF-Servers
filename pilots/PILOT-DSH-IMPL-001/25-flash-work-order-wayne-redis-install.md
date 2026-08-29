# WORK ORDER — Wayne: Redis installation on hxs-9 (EXECUTION)

- Issuer: Flash (governor), 2026-08-29. Owner approved the plan.
- Executor: Wayne (Redis systems engineer, KDD-0015).
- Lane: `omniroute/gpt-oss-120b` (OpenAI gpt-oss-120b, AkashML, via OmniRoute hxs-8).
- Target: hxs-9 (192.168.50.208) ONLY.
- Controlling plan: `servers/hxs-9/2026-08-29-redis-implementation-plan.md` (owner-approved 2026-08-29).

## Intent

Install Redis on hxs-9 per the approved plan. Standalone instance,
dev/test posture, no cluster/sentinel/replication, native systemd.

## Steps (per the plan)

1. **Lane verification** — session-start probe to OmniRoute, verify served-model id `openai/gpt-oss-120b`.
2. **V0 pre-state** — SSH to hxs-9, verify no Redis on 6379, service inactive, `apt-cache policy redis-server` captured, disk/mem free, 0 failed units.
3. **Install** — `apt-get install redis-server`. Verify version = 8.10.
4. **Config** — edit `/etc/redis/redis.conf`: bind 192.168.50.208 127.0.0.1, protected-mode no, port 6379, maxmemory 4GB, maxmemory-policy allkeys-lru, RDB save points, AOF appendonly yes appendfsync everysec, logfile "" (journal), aclfile /etc/redis/users.acl.
5. **ACL users** — create admin (password generated via openssl rand), cache-service (no password, ~cache:* +@all), rag-service reserved (not created).
6. **Credentials** — write REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_USERNAME, REDIS_PWD to `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`.
7. **Backup** — create /var/backups/hx-redis/ (0770 redis:redis), hx-redis-backup.service + .timer (OnCalendar *-*-* 02:37:00, Persistent, RandomizedDelaySec 300), backup script /usr/local/sbin/hx-redis-backup.
8. **Health** — hx-redis-health.service + .timer (OnCalendar *:0/15, RandomizedDelaySec 45), script /usr/local/sbin/hx-redis-health-check.
9. **V1–V6** — run all validation steps, capture receipts.
10. **Evidence doc** — write `servers/hxs-9/2026-08-29-redis-install-evidence.md` with sanitized command log, timestamps, V0–V6 results, rollback material.
11. **Validate** — `python3 scripts/validate.py` 4/4 PASS, render if manifest-listed.

## Constraints

- Standalone ONLY — no cluster/sentinel/replication.
- MCP HOLD — no mcp-redis-main.
- RAG/vector/stream DEFERRED — no module config.
- Native systemd — no Docker.
- No host firewall.
- hxs-9 ONLY.
- Secret hygiene: askpass 0700, deleted after, password never printed/logged/committed. Credential values only in .local.env.
- Chris's PostgreSQL cache integration runs in parallel — coordinate the end-to-end validation after both are done.
- `scripts/validate.py` 4/4 after repo writes.
- Concurrency 1, max session PT1H.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` when Redis is installed, configured, ACLs created, credentials written, timers enabled, V0–V6 pass, evidence doc written, validate.py 4/4 PASS.
