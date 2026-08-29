# WORK ORDER — Chris: pg_hba.conf revert (dev/test posture)

> **METADATA OF RECORD 2026-08-29** (OPEN CORRECTION, labeled, append-only —
> review batch 2, F34): Issuing authority: **Flash, governor** (owner
> directive chain), 2026-08-29. Controlling plan:
> `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` (posture
> section) as executed under work orders 15/16. Model lane at execution:
> `openrouter/deepseek/deepseek-v4-pro` (DeepSeek V4 Pro, Baidu FP8, via
> OmniRoute — Chris's lane as of the owner directive 2026-08-29; the Qwen
> 3.8 Flash lane name in older orders is superseded). Relationship to WO16:
> this order (WO17) is the revert-only successor to the combined Step 2
> order WO16 — it supersedes WO16's pg_hba leg and is itself marked
> **superseded (executed and closed)** by the reverted posture it produced;
> `servers/hxs-9/2026-08-29-postgresql-install-step2.md` carries the
> execution evidence.

You are Chris, PostgreSQL DBA. Execute on hxs-9 (192.168.50.208).

## Task

Revert pg_hba.conf from scram-sha-256 hardening to trust-based posture (dev/test environment, owner directive).

## Current live state (from your Step 1 work)

File: `/etc/postgresql/18/main/pg_hba.conf`
Pre-edit backup: `/etc/postgresql/18/main/pg_hba.conf.pre-hx.bak`

You changed `local all all peer` to `scram-sha-256` and added `host all all 192.168.50.0/24 scram-sha-256`.

## Steps

1. SSH to hxsa@192.168.50.208 (read the SSH credential through the canonical
   `ssh-info` mechanism — see `knowledge/network.md` / the protected
   ssh-info file of record; do not copy secret values into this document or
   into session logs. [OPEN CORRECTION 2026-08-29, labeled, append-only —
   review batch 2, F35: the original instruction read "SSH password from
   /home/hxsa/opt/local-tkv/agent-zero-docs/.local.env — HX_SSH_PASSWORD";
   corrected to reference the mechanism, not the path/env name or value,
   per the factory's secret-mechanism rule. Original preserved here as
   history.]). Use a temp askpass helper (0700), delete it after.

2. Restore packaged pg_hba.conf:
   `sudo cp /etc/postgresql/18/main/pg_hba.conf.pre-hx.bak /etc/postgresql/18/main/pg_hba.conf`

3. Add LAN trust rule. Append to pg_hba.conf:
   `host all all 192.168.50.0/24 trust`

4. Reload: `sudo systemctl reload postgresql`

5. Verify and paste output:
   - `sudo -u postgres psql -tA -c "SELECT count(*) FROM pg_hba_file_rules WHERE error IS NOT NULL"` → must be 0
   - `sudo -u postgres psql -tA -c "SELECT type, database, user_name, address, auth_method FROM pg_hba_file_rules WHERE auth_method='trust'"` → must show the LAN trust rule
   - `psql -h 192.168.50.208 -U postgres -c "SELECT 1"` → must connect without password (trust works)

6. Update `servers/hxs-9/2026-08-29-postgresql-install-step1.md` §4.3 — append a labeled correction block (do NOT rewrite original text):
   "Correction 5 (2026-08-29): pg_hba.conf reverted to dev/test posture per owner directive. local all all restored to peer. LAN rule changed to trust. scram-sha-256 hba rules removed."

7. Run `python3 scripts/validate.py` — paste output.

## Constraints

pg_hba.conf ONLY. Nothing else. No roles, no timers, no databases.
Askpass 0700, deleted after. Password never printed/logged/committed.
