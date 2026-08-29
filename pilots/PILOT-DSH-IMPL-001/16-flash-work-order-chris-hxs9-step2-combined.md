# WORK ORDER — Chris: Step 2 (roles, credentials, timers, V4–V6) + pg_hba revert

- Issuer: **Flash** (governor), 2026-08-29 — owner directive.
- Executor: **Chris** (PostgreSQL DBA, KDD-0014).
- Lane: `omniroute/qwen3.8-flash` (Qwen 3.8 Flash, Alibaba Cloud International, via OmniRoute hxs-8).
- Target: hxs-9 (192.168.50.208) ONLY.
- Controlling plan: `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` (incl. Corrections 1–5).
- Step 1 evidence: `servers/hxs-9/2026-08-29-postgresql-install-step1.md` (Checkpoint 1 ACCEPTED, state-log row 44).

## Intent

Two tasks, in this order:

### Task A — pg_hba.conf revert (work order 15, plan Correction 5)

hxs-9 is a dev/test environment. The scram-sha-256 hardening Chris applied
to pg_hba.conf in Step 1 is not wanted. Revert to trust-based posture.

**What Chris did in Step 1 (current live state):**

1. Changed packaged `local all all peer` → `local all all scram-sha-256`.
2. Added `host all all 192.168.50.0/24 scram-sha-256`.
3. Pre-edit backup at `/etc/postgresql/18/main/pg_hba.conf.pre-hx.bak`.

**What to do (exact):**

1. Restore the packaged pg_hba.conf from the pre-edit backup:
   `sudo cp /etc/postgresql/18/main/pg_hba.conf.pre-hx.bak /etc/postgresql/18/main/pg_hba.conf`
2. Add the LAN rule as trust:
   append `host all all 192.168.50.0/24 trust` to pg_hba.conf.
3. Reload: `sudo systemctl reload postgresql`.
4. Verify: `pg_hba_file_rules` error count = 0; `local all all` is `peer`;
   `host all all 192.168.50.0/24` is `trust`; a passwordless TCP
   connection from the LAN succeeds.
5. Update the Step 1 evidence doc §4.3 with a labeled correction block
   (append-only — do NOT rewrite the original text).

### Task B — Step 2: roles, credentials, backup + health timers, V4–V6

Per plan §3–§6 and §9 Step 2 (as corrected by Correction 4 — Chris is the
sole executor). pg_hba is now trust-based (Task A done first), so
passwords are not enforced by hba — but roles and credentials are still
created per the plan for operational identity.

**Roles (plan §3):**

- `ps-admin` — group role (NOLOGIN) + a named LOGIN member. Instance
  administration.
- `ps-backup` — LOGIN, read-only via `pg_read_all_data`. pg_dump service
  role.
- `ps-scratch` — LOGIN, on scratch DB only. Validation round-trip, then
  dropped post-validation.
- `postgres` — packaged superuser, untouched.

No role gets superuser beyond the packaged `postgres`. No application
roles.

**Credentials (plan §4):**

All credentials land in `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`.
Generate passwords at execution time via `openssl rand -base64 24` or
`pwgen`. Values live ONLY in `.local.env` — never printed, logged, or
committed to the repo.

Entries to write:

```text
HX_PG_HOST=192.168.50.208
HX_PG_PORT=5432
HX_PG_ADMIN_ROLE=ps-admin
HX_PG_ADMIN_PASSWORD=<generated>
HX_PG_BACKUP_ROLE=ps-backup
HX_PG_BACKUP_PASSWORD=<generated>
```

**Backup timers (plan §5):**

- `hx-pg-backup.service` + `hx-pg-backup.timer` — daily at
  `OnCalendar=*-*-* 02:17:00`, `Persistent=true`, `RandomizedDelaySec=300`.
- Tool: `pg_dump` (custom format `-Fc`) per database + `pg_dumpall
  --globals-only` for roles, run as the `postgres` OS user.
- Destination: `/var/backups/hx-postgres/`, files `<db>-<date>.dump` +
  `globals-<date>.sql`.
- Retention: 14 daily archives, pruned by the same oneshot.
- Post-validation: exit 0, file non-empty, archive listable
  (`pg_restore --list` exit 0).

**Health timer (plan §6):**

- `hx-pg-health.service` + `hx-pg-health.timer` —
  `OnCalendar=*:0/15`, `RandomizedDelaySec=45`.
- Script: `/usr/local/sbin/hx-pg-health-check` (bounded, read-only,
  exit 0 = healthy):
  1. `pg_isready` on 192.168.50.208:5432.
  2. Connection count vs `max_connections` (warn > 80%).
  3. Blocked-lock count.
  4. Storage: data dir filesystem usage (warn > 80%).
  5. Backup status: newest archive age (warn > 26h).
- The script performs NO automatic production changes.

**Validation (plan §7):**

| ID | Check | Pass criterion |
| --- | --- | --- |
| V4 | Role connect + write/read round-trip | As `ps-admin`: CREATE scratch DB; `ps-scratch` INSERT + SELECT round-trip; drop scratch |
| V5 | Backup + restore drill | `pg_dump` produces non-empty, listable archive; restore into `*_restoretest` DB; row counts match; drop test DB |
| V6 | Timer/monitor live | Both timers enabled+active; one manual trigger of each succeeds; health script exits 0 |

**Evidence doc:**

Produce `servers/hxs-9/2026-08-29-postgresql-install-step2.md` — full
evidence record following the Step 1 doc shape (sanitized command log,
timestamps, V4–V6 receipts, inverse material, boundaries compliance,
secret hygiene proof, validate.py output).

## Constraints

- pg_hba.conf, roles, credentials, timers, health script, validation ONLY.
- No Redis, no MCP, no application schema, no replication, no firewall
  changes, no reboots, no other hosts.
- Secret hygiene: askpass 0700, deleted after, password never
  printed/logged/committed. Credential values live ONLY in
  `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env`.
- `scripts/validate.py` 4/4 after any repo write.
- Render any manifest-listed .md you change.
- Concurrency 1, max session PT1H.
- hxs-9 ONLY.

## Authority

Owner directive 2026-08-29. Plan Corrections 4 and 5. KDD-0014.
AGENTS.md. Work order 15 (pg_hba revert, folded into this combined order).

## Evidence bar

- Pasted `pg_hba_file_rules` output showing the corrected trust-based rules.
- Passwordless LAN connection success proof.
- Pasted SQL output showing roles created with correct privileges.
- Proof that `.local.env` contains the credential entries (mechanism-only
  reference — show the file exists and has the keys, never paste values).
- `systemctl status` output for both timers showing enabled+active.
- V4–V6 receipts with timestamps.
- `validate.py` output pasted.
- Evidence doc written and rendered.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` when Task A + Task B are done, all
V4–V6 pass, evidence doc written, validate.py green.
`[TASK PAUSED — ESCALATION TO GOVERNOR]` with the named remainder if
anything blocks.
