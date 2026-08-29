# WORK ORDER — Chris: hxs-9 PostgreSQL Step 0 (pre-state gate) + Step 1 (install + config baseline), halt at Checkpoint 1

- Issuer: Kimi-K3 (governor) — written by Mia (Chief of Staff, KDD-0012),
  2026-08-29, per owner directive ("Chris is the DBA and installs his own
  database"). Distribution executes under this Kimi-K3-issued order.
- Executor: **Chris** (PostgreSQL systems engineer, KDD-0014) — session
  `chris-hxs9-pg-step1-20260829-01`. Launch shape:
  `kimi -m openrouter/qwen/qwen3.8-flash --agent-file agents/chris/profile.md`.
- Activation status: **ACTIVE** — profile §10 revised 2026-08-29 by owner
  directive; the original activation gate (instance-must-exist-first) is
  VOID, activation word given ("proceed with install"). You install your own
  database.
- Model lane (binding): `openrouter/qwen/qwen3.8-flash` — upstream provider
  **Alibaba Cloud International**, via OmniRoute hxs-8 (KDD-0013
  amendment 6). **Session-start identity verification REQUIRED, cloud
  pattern per amendment 2**: the gateway must echo the exact served-model id
  `qwen/qwen3.8-flash`, confirmed by a live routed probe at session start.
  Fail closed: mismatch, unresolvable identity, or unhealthy endpoint ⇒
  stop before any inference, report to Kimi-K3, **no substitution** (cloud
  substitution outside the OD-14 exception is always prohibited). Your lane
  rides the OD-14 exception (six cloud lanes, metered).
- Target: **hxs-9 (192.168.50.208) ONLY** — no other host.
- Controlling doc: `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md`
  (owner-approved 2026-08-29, incl. Review Correction Block + Correction 2).
  This order implements plan §9 Step 0 + Step 1 and **halts at
  Checkpoint 1** — an owner gate (via Kimi-K3), not optional.
- Predecessor session of record: rick's earlier hxs-9 session was stopped
  BEFORE any mutation — hxs-9 is in pre-state (verified: zero changes).
  [SUPERSESSION NOTE 2026-08-29, labeled, append-only — Mia per Flash work
  order 19 (F17): rick's assignment to the hxs-9 install (state-log rows
  41–42 lineage) is SUPERSEDED/CANCELLED by owner lane ruling 2026-08-29
  (state-log row 42: "Chris is the DBA, Chris installs his own database") —
  stopped pre-mutation, zero partial state; this order (13) is the SOLE
  ACTIVE authorization for the hxs-9 PostgreSQL install, executed by Chris.]
- Concurrency 1, max session PT1H (profile §8).

## STALE-TEXT RULING (carries the plan's own Correction 2)

Plan §9 Step 1's phrase **"Packages from noble main" is STALE and VOID**.
Superseded by the plan's Correction 2 (owner version ruling, 2026-08-29):

- Install **PostgreSQL 18.6 from PGDG noble-pgdg** (`postgresql-18 =
  18.6-1.pgdg24.04+2`, governor-verified live 2026-08-29) — NOT
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
     post** install. apt is the provenance chain — no hand-fetched `.deb`.
- Expect `psql --version` = 18.6, cluster `18/main` per `pg_lsclusters`.

## Read first (bounded)

1. The controlling plan above — especially §1.1–§1.2, §2, §7 (V0–V3), §8, §9.
2. Your contract: `agents/chris/profile.md` + `agents/chris/charter.md` —
   knowledge review first, ON_ERROR_STOP, credential discipline, evidence
   gates.
3. `servers/hxs-9/discovery.md` — as-found identity and envelope
   (machine-id `a6c24677…`, IP `192.168.50.208/24`).
4. `servers/hxs-15/2026-08-28-dsh-runtime-prep.md` — the required evidence
   shape (sanitized sequential command log, pre/post captures, exact
   inverses).
5. Knowledge review per profile §3: survey `/opt/tkv-local` (including the
   `npostgres-master` tree) with **be-great** before acting; verify against
   the live environment; reference material, never assumed current.

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

1. **PGDG onboarding + install** per the stale-text ruling above.
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
     (capture the refusal). Use `psql` with `ON_ERROR_STOP` for any scripted
     SQL.

## HARD PROHIBITIONS — Checkpoint 1 scope ceiling

- **NO roles** (`ps-admin`, `ps-backup`, `ps-scratch` — Step 2 material,
  created after Checkpoint 1 under a follow-on order; profile §10's ruling
  that you create your own credential entries applies to that phase, not
  this one).
- **NO credential entries** anywhere, including `.local.env`.
- **NO timers** (backup/health units are Step 2).
- **NO databases** beyond the packaged default cluster.
- No reboot; no firewall; no other hosts; no Redis; no MCP usage (HOLD);
  no scope beyond this order.

## Credential discipline (your own access path)

- SSH via your `SSH_ASKPASS` helper (mode **0700**) reading the
  credential-record row from
  `/home/hxsa/opt/local-tkv/agent-zero-docs/keys.md/ssh-info.md` at
  **execution time only**.
- `SSH_ASKPASS_REQUIRE=force` + `DISPLAY` set; `StrictHostKeyChecking=yes`
  with a pre-pinned host key for 192.168.50.208.
- Remote privilege via `sudo -n` (confirm passwordless sudo live at Step 0).
- Helper **deleted at session end**, absence verified.
- **No secret values in any artifact** — REDACTED; credential values never
  printed, logged, or committed (profile §2).

## Evidence — `servers/hxs-9/2026-08-29-postgresql-install-step1.md`

Required, in the hxs-15 evidence shape:

- session-start lane verification record (served-model id echo + probe
  result);
- pre/post captures (identity, apt-cache policy, listener, service state);
- `dpkg --verify` output;
- `ss -ltnp` listener proof (LAN-bound, not wildcard);
- `SHOW listen_addresses` output;
- no-`trust` proof; passwordless-refused proof;
- sanitized sequential command log (hxs-15 doc §10 format);
- **exact inverses per step** (plan §8 rows are the authority: purge +
  repo/keyring/pin removal restores the absent pre-state);
- completion-gate record per your profile §5 (commands/SQL used, results,
  pass/fail verdict — never credential values).

After your writes: `python3 scripts/validate.py` must pass — paste the
result. Final line of the evidence doc:

- `PASS - CHECKPOINT 1 REACHED` (V0–V3 receipts attached, halted at the
  owner checkpoint), or
- `ESCALATION` with the sanitized blocker evidence — use
  `[TASK PAUSED — ESCALATION TO KIMI-K3]`. Escalation path: Kimi-K3 always,
  never the owner directly.

## Bounds

hxs-9 ONLY; Step 0 + Step 1 ONLY; halt at Checkpoint 1 — owner review of
the V0–V3 receipts precedes anything further (roles, credentials, timers,
and validation V4–V6 are post-checkpoint material). Escalation authority:
Kimi-K3. On model-lane failure: stop the session, report to Kimi-K3, no
substitution.
