# WORK ORDER — Chris: reverse pg_hba.conf hardening on hxs-9 (dev/test posture)

- Issuer: **Flash** (governor), 2026-08-29 — owner directive.
- Executor: **Chris** (PostgreSQL DBA, KDD-0014).
- Lane: `omniroute/qwen3.8-flash` (Qwen 3.8 Flash, Alibaba Cloud International, via OmniRoute hxs-8).
- Target: hxs-9 (192.168.50.208) ONLY.

## Intent

The owner ruled 2026-08-29: hxs-9 is a dev/test environment. The
scram-sha-256 hardening Chris applied to pg_hba.conf in Step 1 is not
wanted. Revert to a trust-based posture.

## What Chris did in Step 1 (current live state)

From `servers/hxs-9/2026-08-29-postgresql-install-step1.md` §4.3:

1. Changed packaged `local all all peer` → `local all all scram-sha-256`.
2. Added `host all all 192.168.50.0/24 scram-sha-256` (absent from packaged file).
3. Pre-edit backup at `/etc/postgresql/18/main/pg_hba.conf.pre-hx.bak`.

## What to do (exact)

1. SSH to hxs-9 (same credential discipline as Step 1 — askpass at
   execution time, 0700 helper, deleted after).
2. Restore the packaged pg_hba.conf from the pre-edit backup:
   `sudo cp /etc/postgresql/18/main/pg_hba.conf.pre-hx.bak /etc/postgresql/18/main/pg_hba.conf`
   — this reverts `local all all` back to `peer` and removes the LAN scram rule.
3. Add the LAN rule as trust (owner: "trust everywhere"):
   append `host all all 192.168.50.0/24 trust` to pg_hba.conf.
4. Reload: `sudo systemctl reload postgresql`.
5. Verify:
   - `pg_hba_file_rules` error count = 0.
   - `local all all` is `peer` (not scram).
   - `host all all 192.168.50.0/24` is `trust`.
   - A passwordless TCP connection from the LAN succeeds (opposite of
     the Step 1 V3 refusal — this is the expected dev/test behavior now).
6. Update the evidence doc
   `servers/hxs-9/2026-08-29-postgresql-install-step1.md` §4.3 with a
   labeled correction noting the posture change and the new effective
   rules. Do NOT rewrite the original — append a labeled correction block.
7. Run `python3 scripts/validate.py` — must be 4/4 PASS.
8. Report back to the governor with the receipt.

## Constraints

- pg_hba.conf ONLY. Do not touch `99-hx.conf`, the cluster, roles,
  timers, or anything else.
- No roles, no credentials, no timers, no databases.
- Secret hygiene: askpass 0700, deleted after, password never
  printed/logged/committed.
- `scripts/validate.py` 4/4 after any repo write.
- Render any manifest-listed .md you change.

## Authority

Owner directive 2026-08-29 (dev/test posture). Plan Correction 5
(`servers/hxs-9/2026-08-29-postgresql-implementation-plan.md`). KDD-0014.
AGENTS.md.

## Evidence bar

- Pasted `pg_hba_file_rules` output showing the corrected rules.
- Passwordless LAN connection success proof (psql output).
- `validate.py` output pasted.
- Updated evidence doc with labeled correction.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` when the hba is reverted, verified,
evidence doc updated, and validate.py green.
