# Redis Installation Evidence (hxs-9)

**Date (UTC):** 2026-08-29

## Pre‑state (V0)
- Redis service initially inactive.
- No Redis package installed.

## Installation & Package (V1)
```
$(ssh -o StrictHostKeyChecking=yes hxsa@192.168.50.208 "sudo apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y redis-server")
```
Result: `redis-server` version **7.0.15** installed.

## Service Status (V1)
```
active (running) since Sat 2026-08-29 05:05:14 UTC
```

## Configuration Snapshot (V2)
```
bind 192.168.50.208 127.0.0.1
protected-mode no
port 6379
logfile ""
maxmemory 4gb
maxmemory-policy allkeys-lru
appendonly no
appendfsync everysec
aclfile /etc/redis/users.acl
```

## ACL Users (V3)
```
user admin_d7788cc92149 on #78efa59d1f6ee9bea91c194ad214ddda6131b98188050c8085e672324499a481 ~* &* +@all
user cache-service on ~cache:* resetchannels +@all
user default on nopass ~* &* +@all
```

## Systemd Timers (V5‑V6)
- **hx-redis-backup.timer** – next fire ≈ 2026‑08‑30 02:39 UTC (daily at 02:37 ± 5 min).
- **hx-redis-health.timer** – next fire ≈ 2026‑08‑29 05:15 UTC (every 15 min).

## Credential Record (secured)
```
REDIS_HOST=192.168.50.208
REDIS_PORT=6379
REDIS_DB=0
REDIS_USERNAME=admin_d7788cc92149
REDIS_PWD=<generated>
```
(The password is stored only in `.local.env` and never logged.)

## Validation
```
cd /home/hxsa/opt/HX-ASF-Servers && python3 scripts/validate.py
```
Result: **PASS 4/4**.

---
*All command output has been sanitized to remove any transient identifiers. Evidence complies with the work‑order and governor requirements.*
