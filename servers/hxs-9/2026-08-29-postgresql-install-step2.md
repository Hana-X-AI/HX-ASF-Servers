# hxs-9 PostgreSQL — Step 2 (roles, credentials, timers, V4–V6) + pg_hba revert — evidence record

| Field | Value |
| --- | --- |
| Task | Work order 16 (combined) — plan §9 Step 2 + pg_hba revert (Correction 5) |
| Executor | Governor (Phase M bounded direct execution) — Chris's lane (Qwen 3.8 Flash) failed twice on tool-use capability; governor executed directly per Phase M |
| Target | hxs-9 (192.168.50.208) ONLY |
| Controlling doc | `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` (Corrections 1–5) |
| Window | 2026-08-29 03:20 → 03:25 UTC |
| Model lane | Governor lane (DeepSeek V4 Flash via OmniRoute) |
| Credential handling | SSH password read from `.local.env` at execution time via temp askpass helper (mode 0700); value never printed, logged, or committed; helper deleted after use, absence verified |
| Host key | `StrictHostKeyChecking=yes`; 192.168.50.208 pre-pinned in `~/.ssh/known_hosts` |
| Result | **PASS — hba reverted, roles created, credentials written, timers enabled, V4–V6 pass** |

## 1. Task A — pg_hba.conf revert (Correction 5, dev/test posture)

### Pre-revert state (A1)

Current pg_hba_file_rules showed scram-sha-256 hardening from Step 1:

```
118|local|peer
123|local|scram-sha-256
125|host|scram-sha-256
127|host|scram-sha-256
131|host|scram-sha-256
132|local|peer
133|host|scram-sha-256
134|host|scram-sha-256
```

### Revert actions (A2–A4)

1. Restored packaged pg_hba.conf from pre-edit backup:
   `sudo cp /etc/postgresql/18/main/pg_hba.conf.pre-hx.bak /etc/postgresql/18/main/pg_hba.conf`
2. Appended LAN trust rule: `host all all 192.168.50.0/24 trust`
3. Reloaded: `sudo systemctl reload postgresql`

### Post-revert verification (A5)

- `pg_hba_file_rules` error count: **0**
- Trust rules: `host|192.168.50.0|trust` — LAN trust rule present
- Passwordless LAN connect test: `psql -h 192.168.50.208 -U postgres -c "SELECT 1"` → **returned row, trust works**
- Final effective rules:
```
local|{all}|{postgres}||peer
local|{all}|{all}||peer
host|{all}|{all}|127.0.0.1|scram-sha-256
host|{all}|{all}|::1|scram-sha-256
local|{replication}|{all}||peer
host|{replication}|{all}|127.0.0.1|scram-sha-256
host|{replication}|{all}|::1|scram-sha-256
host|{all}|{all}|192.168.50.0|trust
```

Local connections use `peer` (packaged default). LAN connections use `trust` (dev/test posture per owner directive). The scram rules on loopback/localhost are from the packaged file and were not removed — they are harmless since the LAN trust rule takes precedence for LAN traffic.

## 2. Task B — Step 2: roles, credentials, timers, V4–V6

### B1 — Roles created

| Role | Type | Login | Purpose |
| --- | --- | --- | --- |
| `ps-admin` | group (NOLOGIN) | no | Instance administration |
| `ps-admin-login` | LOGIN, member of ps-admin | yes | Named login for admin operations |
| `ps-backup` | LOGIN, REPLICATION | yes | pg_dump service role, `pg_read_all_data` granted |
| `ps-scratch` | LOGIN | yes | Validation round-trip (droppable) |

`postgres` superuser untouched. No role gets superuser beyond packaged `postgres`.

### B2 — Passwords generated and set

Passwords generated via `openssl rand -base64 24` at execution time. Passwords set via `ALTER ROLE ... PASSWORD '...'`. Values never printed in logs (written only to `.local.env`).

### B3 — Credentials written to .local.env

File: `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`

Six entries appended:
```
HX_PG_HOST=192.168.50.208
HX_PG_PORT=5432
HX_PG_ADMIN_ROLE=ps-admin
HX_PG_ADMIN_PASSWORD=<generated>
HX_PG_BACKUP_ROLE=ps-backup
HX_PG_BACKUP_PASSWORD=<generated>
```

Verified: `grep -c 'HX_PG_' .local.env` → **6**. File perms unchanged (0600).

### B4–B5 — Backup service + timer + script

- `/etc/systemd/system/hx-pg-backup.service` — Type=oneshot, User=postgres, ExecStart=/usr/local/sbin/hx-pg-backup
- `/etc/systemd/system/hx-pg-backup.timer` — OnCalendar=*-*-* 02:17:00, Persistent=true, RandomizedDelaySec=300
- `/usr/local/sbin/hx-pg-backup` (0755) — pg_dump -Fc per database + pg_dumpall --globals-only; 14-day prune

**Fix applied during execution:** backup directory `/var/backups/hx-postgres` was `0750 root:postgres` (group r-x, no write for postgres). Changed to `0770 root:postgres` so the postgres OS user can write backup files.

### B6 — Health service + timer + script

- `/etc/systemd/system/hx-pg-health.service` — Type=oneshot, User=postgres
- `/etc/systemd/system/hx-pg-health.timer` — OnCalendar=*:0/15, RandomizedDelaySec=45
- `/usr/local/sbin/hx-pg-health-check` (0755) — 5 checks: pg_isready, connection count, blocked locks, storage, backup age

**Fix applied during execution:** the health script's backup-age check originally looked for `*.dump` only. Since the only non-template database is `postgres` (skipped by the backup script per `datname != 'postgres'`), only `*.sql` (globals) files are produced. Fixed to check for `*.dump` OR `*.sql`.

### B7–B8 — Timers enabled

```
hx-pg-backup.timer: active, enabled (next: 2026-08-30T02:20:08Z)
hx-pg-health.timer: active, enabled (next: 2026-08-29T03:30:40Z)
```

### B9 — V4: role connect + write/read round-trip — PASS

```
CREATE DATABASE scratch_test OWNER "ps-admin-login"
GRANT ALL ON SCHEMA public TO "ps-scratch"
CREATE TABLE test_val (id serial PRIMARY KEY, val text)
INSERT 0 1
 id | val
----+-------
  1 | hello
(1 row)
DROP DATABASE scratch_test
```

### B10 — V5: backup + restore drill — PASS

```
pg_dump -Fc -f /tmp/v5-test.dump postgres
pg_restore --list /tmp/v5-test.dump → OK
createdb v5_restoretest → pg_restore → OK
dropdb v5_restoretest
rm /tmp/v5-test.dump
```

### B11 — V6: timer manual trigger + health — PASS

Initial run: health service failed (no backup existed yet — expected). After manual backup run and health script fix:

```
hx-pg-health-check → HEALTHY (exit 0)
hx-pg-health.service → Result=success
hx-pg-backup.service → Result=success
```

### B12 — Final state capture

**Roles:**
```
ps-admin|f          (NOLOGIN group)
ps-admin-login|t    (LOGIN)
ps-backup|t         (LOGIN)
ps-scratch|t        (LOGIN)
```

**Timers:**
```
NEXT                        LEFT LAST PASSED UNIT               ACTIVATES
Sat 2026-08-29 03:30:40 UTC 6min  -    -       -  hx-pg-health.timer hx-pg-health.service
Sun 2026-08-30 02:20:08 UTC 22h   -    -       -  hx-pg-backup.timer  hx-pg-backup.service
```

**Backup files:**
```
/var/backups/hx-postgres/globals-20260829.sql (1526 bytes, postgres:postgres)
```

**Service results:** both `success`.

## 3. Fixes applied during execution

| Fix | Problem | Resolution |
| --- | --- | --- |
| Backup dir perms | `0750 root:postgres` — postgres group had r-x but not write | Changed to `0770 root:postgres` |
| Health script backup check | Looked for `*.dump` only, but only `*.sql` (globals) files exist | Fixed to check `*.dump` OR `*.sql` |

Both are execution-time corrections consistent with the plan's "decide at execution" posture for operational details.

## 4. Boundaries compliance

| Prohibition | Held |
| --- | --- |
| No Redis / MCP / application schema / replication / firewall / reboot | ✓ |
| hxs-9 ONLY, pg_hba + roles + credentials + timers ONLY | ✓ |
| Secret hygiene: askpass 0700, deleted after, password never printed/logged/committed | ✓ |
| Credential values live only in `.local.env` | ✓ (6 entries, file 0600) |
| Temp scripts deleted on hxs-9 and locally | ✓ |

## 5. Chris lane failure note

Chris's Qwen 3.8 Flash lane was attempted twice (work orders 16 and 17). Both sessions produced reasoning text ("Let me begin") but zero tool calls — no SSH, no file writes, no evidence. The model can reason about the task but cannot execute tool-use (SSH, file operations) through the kimi CLI in standalone mode. This is a lane capability gap, not a work-order defect. The work was executed by the governor under Phase M bounded direct execution (KDD-0001 §2.3) — same authority that governed the Step 1 review and acceptance.

## 6. Post-write validation

`python3 scripts/validate.py` — 4/4 PASS (run after evidence doc write + Step 1 doc update + HTML render):

```
HX-ASF validate — read-only local validation (UD1/UD2, 2026-08-25) — mode: full repo
PASS  wiki-sync — render.py --check: 53/53 manifest documents in sync
PASS  fixture-suite — unittest 57 tests OK; sha256sums 10/10 verified
PASS  catalog-mechanical — 311 records: schema/required/enums/source.section OK
PASS  secret-boundary — repo-wide: 884 files scanned, 0 hits
RESULT: PASS — 4/4 checks, 4 manual gates noted (exit 0)
```

PASS — STEP 2 COMPLETE + pg_hba REVERTED
