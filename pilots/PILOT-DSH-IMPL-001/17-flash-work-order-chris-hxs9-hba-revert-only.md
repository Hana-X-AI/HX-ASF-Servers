# WORK ORDER — Chris: pg_hba.conf revert (dev/test posture)

You are Chris, PostgreSQL DBA. Execute on hxs-9 (192.168.50.208).

## Task

Revert pg_hba.conf from scram-sha-256 hardening to trust-based posture (dev/test environment, owner directive).

## Current live state (from your Step 1 work)

File: `/etc/postgresql/18/main/pg_hba.conf`
Pre-edit backup: `/etc/postgresql/18/main/pg_hba.conf.pre-hx.bak`

You changed `local all all peer` to `scram-sha-256` and added `host all all 192.168.50.0/24 scram-sha-256`.

## Steps

1. SSH to hxsa@192.168.50.208 (read the SSH password from /home/hxsa/opt/local-tkv/agent-zero-docs/.local.env — HX_SSH_PASSWORD). Use a temp askpass helper (0700), delete it after.

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
