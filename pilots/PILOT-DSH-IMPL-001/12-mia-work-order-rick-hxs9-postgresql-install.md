# WORK ORDER — Rick: hxs-9 PostgreSQL Step 0 (pre-state gate) + Step 1 (install + config baseline)

> **SUPERSEDED 2026-08-29** (OPEN STATUS CORRECTION, labeled, append-only —
> review batch 2, F30): this work order was superseded the same day it was
> issued by **`13-mia-work-order-chris-hxs9-postgresql-install.md`** (work
> order 13) after the owner's DBA ruling (state-log row 42: Chris the DBA
> installs his own database; rick stopped pre-mutation, zero partial state).
> This order is retained in full below as the historical record; it has no
> remaining executable force.

- Issuer: Kimi-K3 (governor) — written by Mia (Chief of Staff, KDD-0012),
  2026-08-29, per owner-approved plan. Distribution executes under this
  Kimi-K3-issued order.
- Executor: **Rick** (Ubuntu Server Engineer, OS plane) — session
  `rick-hxs9-pg-step1-20260829-01`
- Model lane (binding): `omniroute/meta-x` (hxs-3, via OmniRoute hxs-8,
  KDD-0013). **Session-start digest verification REQUIRED**: served model
  digest must equal
  `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da`.
  Fail closed: stop, escalate to Kimi-K3, **no substitution** (cloud
  substitution always prohibited).
- Target: **hxs-9 (192.168.50.208) ONLY** — no other host.
- Controlling doc: `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md`
  (owner-approved 2026-08-29, incl. Review Correction Block + Correction 2).
  This order implements plan §9 Step 0 + Step 1 and **halts at
  Checkpoint 1**.
- Evidence shape precedent: `servers/hxs-15/2026-08-28-dsh-runtime-prep.md`.

## STALE-TEXT RULING (carries the plan's own Correction 2)

Plan §9 Step 1's phrase **"Packages from noble main" is STALE and VOID**.
Superseded by the plan's own Correction 2 (owner version ruling, same date):

- Install **PostgreSQL 18.6 from PGDG noble-pgdg** (`postgresql-18 =
  18.6-1.pgdg24.04+2` verified live by the governor 2026-08-29) — NOT
  postgresql-16 from noble main.
- Repo onboarding, GPG-verified, exactly per plan §1.1:
  1. Fetch the official PGDG signing key from postgresql.org, verify its
     fingerprint against the project's published value, install to
     `/etc/apt/keyrings/postgresql-keyring.gpg` (keyring-scoped, not global
     trust).
  2. Keyring-scoped source:
     `deb [signed-by=/etc/apt/keyrings/postgresql-keyring.gpg] https://apt.postgresql.org/pub/repos/apt noble-pgdg main`.
  3. Apt pin `/etc/apt/preferences.d/hx-pgdg`: `Package: postgresql-* libpq*`,
     `Pin: release o=apt.postgresql.org`, `Pin-Priority: 500` — PGDG can
     never shadow a non-PostgreSQL package.
  4. `apt-get update`; capture `apt-cache policy postgresql-18` **pre and
     post** install.
- Expect `psql --version` = 18.6, cluster `18/main` per `pg_lsclusters`.

## Read first (bounded)

1. `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` — the
   controlling plan; especially §1.1, §2, §7 (V0–V3), §8, §9.
2. `agents/rick/profile.md` + `agents/rick/charter.md` — your contract:
   `/opt/tkv-local/ubuntu` review first, Knowledge Review Receipt,
   test-first/rollback-first, sanitized evidence, escalation protocol.
3. `servers/hxs-9/discovery.md` — as-found identity and envelope
   (machine-id `a6c24677…`, IP `192.168.50.208/24`).
4. `servers/hxs-15/2026-08-28-dsh-runtime-prep.md` — the required evidence
   shape (sanitized sequential command log, pre/post hashes, exact inverses).

## STEP 0 — Pre-state gate (V0 receipt)

Non-mutating. Re-verify live before ANY change:

| Check | Method | Pass criterion |
| --- | --- | --- |
| Identity | `hostname`, machine-id, SSH peer | `hxs-9`, machine-id `a6c24677…` (full value per discovery.md), 192.168.50.208 — ALL MATCH, else halt |
| PostgreSQL absent | units, listeners, `/etc/postgresql` | no postgresql units, no 5432 listener, no `/etc/postgresql` |
| Disk | `df -h /` | ample free (discovery-era ~233 GB free) |
| Failed units | `systemctl --failed` | 0 |
| apt state | `apt-cache policy postgresql-18`, `dpkg --audit`, `apt-mark showhold` | clean; record candidate version + repo before anything |

**Stop conditions (any one ⇒ HALT, report, ZERO mutation):** PostgreSQL
present in any form; anything listening on 5432; disk short; any failed
unit; identity mismatch vs discovery.md. Produce the V0 receipt regardless
of outcome.

## STEP 1 — Install + config baseline (V1–V3 receipts)

Scope ceiling: **instance up + configured + reachable. Nothing more.**

1. **PGDG onboarding + install** per the ruling above (keyring → source →
   pin → `apt-get update` → pre-policy capture → `apt-get install
   postgresql-18 postgresql-client-18` → post-policy capture). Plan §1.2
   provenance: apt is the provenance chain; no hand-fetched `.deb`.
2. **Config baseline** — single drop-in
   `/etc/postgresql/18/main/conf.d/99-hx.conf` per plan §2, exactly:

   | Setting | Value |
   | --- | --- |
   | `listen_addresses` | `192.168.50.208, localhost` — **no 0.0.0.0** |
   | `port` | 5432 |
   | `password_encryption` | `scram-sha-256` |
   | `pg_hba.conf` | `host all all 192.168.50.0/24 scram-sha-256`; local peer for postgres admin; **no `trust` anywhere** |
   | `log_connections` / `log_disconnections` | `on` |
   | `log_min_duration_statement` | `1000` |
   | `logging_collector` | decide at execution from the packaged default (journald vs collector); record which |
   | `shared_buffers` | `4GB` |
   | `idle_in_transaction_session_timeout` | `10min` |

3. **OS-level pieces:** `/var/backups/hx-postgres/` root:postgres **0750**;
   service `enabled` + `active`.
4. **Smokes V1–V3** (plan §7):
   - **V1** — `psql --version` = 18.6; cluster `18/main`; `dpkg --verify`
     clean; PGDG pin active (only `postgresql-*`/`libpq*` may come from
     PGDG — prove with apt-cache policy); apt transaction lines recorded.
   - **V2** — `systemctl is-active/is-enabled postgresql` = active/enabled;
     `pg_isready` OK; `ss -ltnp` proves the listener on
     `192.168.50.208:5432` and **not** `0.0.0.0:5432`.
   - **V3** — `SHOW listen_addresses` = `192.168.50.208, localhost`;
     `SHOW password_encryption` = `scram-sha-256`; `pg_hba.conf` grep proves
     no `trust`; a connection attempt **without** a password is REFUSED
     (capture the refusal).

## HARD PROHIBITIONS — Checkpoint 1 scope ceiling

- **NO roles** (`ps-admin`, `ps-backup`, `ps-scratch` — Step 2 material).
- **NO credential entries** anywhere, including `.local.env`.
- **NO timers** (backup/health units are Step 2).
- **NO databases** beyond the packaged default cluster.
- No reboot; no firewall; no other hosts; no scope beyond this order.

## Credential discipline (your own access path)

- SSH via your `SSH_ASKPASS` helper (mode **0700**) reading the
  credential-record row from
  `/home/hxsa/opt/local-tkv/agent-zero-docs/keys.md/ssh-info.md` at
  **execution time only**.
- `SSH_ASKPASS_REQUIRE=force` + `DISPLAY` set; `StrictHostKeyChecking=yes`
  with pre-pinned host key for 192.168.50.208.
- Remote privilege via `sudo -n` (confirm passwordless sudo live at Step 0).
- Helper **deleted at session end**, absence verified.
- **No secret values in any artifact** — REDACTED, per your profile §11.

## Evidence — `servers/hxs-9/2026-08-29-postgresql-install-step1.md`

Required, in the hxs-15 evidence shape:

- pre/post captures (identity, apt-cache policy, listener, service state);
- `dpkg --verify` output;
- `ss -ltnp` listener proof (LAN-bound, not wildcard);
- `SHOW listen_addresses` output;
- no-`trust` proof; passwordless-refused proof;
- sanitized sequential command log (hxs-15 doc §10 format);
- **exact inverses per step** (plan §8 rows are the authority: purge +
  repo/keyring/pin removal restores the absent pre-state);
- Knowledge Review Receipt + test plan per your profile §5/§7.

After your writes: `python3 scripts/validate.py` must end **4/4 PASS** —
paste the result. Final line of the evidence doc:

- `PASS - CHECKPOINT 1 REACHED` (V1–V3 receipts attached, halted at the
  owner checkpoint), or
- `ESCALATION` with the sanitized blocker evidence per your profile §14
  (use `[TASK PAUSED — ESCALATION TO KIMI-K3]`).

## Bounds

hxs-9 ONLY; Step 0 + Step 1 ONLY; halt at Checkpoint 1 — owner review of
V1–V3 receipts precedes anything further. Escalation authority: Kimi-K3.
On model-lane failure: stop the session, report to Kimi-K3, no substitution.
