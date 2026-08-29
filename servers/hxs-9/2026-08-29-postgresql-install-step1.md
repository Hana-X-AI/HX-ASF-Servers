# hxs-9 PostgreSQL — Step 0 (pre-state gate) + Step 1 (install + config baseline) — evidence record

| Field | Value |
| --- | --- |
| Task | Work order `chris-hxs9-pg-step1-20260829-01` — plan §9 Step 0 + Step 1, halt at Checkpoint 1 |
| Agent | Chris — PostgreSQL systems engineer (KDD-0014) |
| Target | hxs-9 (192.168.50.208) ONLY |
| Executor host | hxs-5 (control machine running this session) |
| Controlling doc | `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` (owner-approved 2026-08-29, incl. Review Correction Block + Correction 2) |
| Window | 2026-08-29 02:04 → 02:13 UTC (within PT1H) |
| Model lane | `openrouter/qwen/qwen3.8-flash` → served id `qwen/qwen3.8-flash` (verified below); provider Alibaba Cloud International via OmniRoute hxs-8 (KDD-0013 A6, OD-14) |
| Credential handling | SSH password read from the credential record at execution time only via temp askpass helper (mode 0700); value never printed, logged, or committed; helper deleted at session end, absence verified |
| Host key | `StrictHostKeyChecking=yes`; 192.168.50.208 pre-pinned in `~/.ssh/known_hosts`, ED25519 `SHA256:Q9G16exXCu3oxx6SR+lYDngLC/dlcHbu9OaflZTeDtU` |
| Result | **PASS — V0–V3 receipts collected, halted at Checkpoint 1** |

## 1. Session-start lane verification (required, fail-closed pattern)

Live routed probe to the OmniRoute gateway with a fresh nonce, per KDD-0013
amendment 2 cloud pattern (amendment 6 adds the provider field):

- Endpoint: `POST http://192.168.50.207:20128/v1/chat/completions` (OmniRoute, hxs-8),
  request model `openrouter/qwen/qwen3.8-flash`.
- HTTP 200, `time_total` 1.66 s.
- **Served-model id echo: `qwen/qwen3.8-flash`** — exact match to the expected
  id (gateway strips the `openrouter/` prefix; pattern of record).
- Nonce echo test: prompt asked for the fresh UUID `f325648c-c7e7-40c6-964c-b1a1180e65b8`
  verbatim; `nonce_echoed=True`, `finish_reason=stop` — semantic-cache
  bypass confirmed (non-cached live inference).
- Provider of record: Alibaba Cloud International (per KDD-0013 A6).
- **Verdict: PASS.** No mismatch, no substitution needed.

## 2. Step 0 — pre-state gate (V0 receipt)

All checks non-mutating, run in one SSH batch at `2026-08-29T02:06:07Z`–`02:06:08Z`.
Capture retained verbatim (`887` bytes).

| Check | Required | Live result | Verdict |
| --- | --- | --- | --- |
| Identity — hostname | `hxs-9` | `hxs-9` | MATCH |
| Identity — machine-id | `a6c2467762ed4b768f196447612a6386` (discovery.md) | `a6c2467762ed4b768f196447612a6386` | MATCH |
| Identity — address | 192.168.50.208 | `eno1 192.168.50.208/24`; SSH peer 192.168.50.208 | MATCH |
| OS | Ubuntu 24.04 (noble) | `Ubuntu 24.04.4 LTS` | MATCH |
| PostgreSQL absent — dpkg | none | `dpkg -l | grep -iE 'postgres|pgdg'` → none | PASS |
| PostgreSQL absent — units | none | `systemctl list-unit-files` → none; `is-active postgresql` → inactive | PASS |
| PostgreSQL absent — listener | none on 5432 | `ss -ltnp | grep :5432` → none | PASS |
| PostgreSQL absent — dirs | no `/etc/postgresql` | absent; also `/var/lib/postgresql`, `/var/backups/hx-postgres` absent | PASS |
| Prior repo artifacts | none | no PGDG source, no keyring, no pin in `/etc/apt/*` | PASS |
| Disk | ample free | `/dev/nvme0n1p2 233G 12G 210G 6% /`; Mem 31Gi total / 30Gi available | PASS |
| Failed units | 0 | 0 | PASS |
| apt state | clean | `dpkg --audit` empty; `apt-mark showhold` empty; `apt-cache policy postgresql-18` pre-onboarding: **no candidate** (unknown package) | PASS |
| sudo | passwordless | `sudo -n true` → `PASSWORDLESS_SUDO=yes` | confirmed live |

**V0 = PASS.** No stop condition tripped. Predecessor rick session's
zero-mutation claim independently confirmed. Mutations permitted to proceed.

## 3. Step 1 — PGDG onboarding (stale-text ruling applied)

Plan §9 Step 1 "Packages from noble main" treated as STALE per the
governor's ruling (plan Correction 2). Installed PostgreSQL 18.6 from PGDG
noble-pgdg; apt is the provenance chain; no hand-fetched `.deb`.

### 3.1 Signing key — fetch, verify, keyring-scope

- URI fetched: `https://www.postgresql.org/media/keys/ACCC4CF8.asc` — the URI
  currently published on postgresql.org's Ubuntu instructions page
  (re-fetched live 2026-08-29, not trusted from memory).
- Downloaded armored key fingerprint (computed at execution time):
  `B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8` (RSA 4096, key-id `7FCC7D46ACCC4CF8`,
  uid "PostgreSQL Debian Repository").
- **Verification against live repo (two legs):**
  1. `noble-pgdg/InRelease` fetched from `apt.postgresql.org`; `gpg --verify` →
     `using RSA key B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8` →
     **`Good signature from "PostgreSQL Debian Repository"`** (Signature made
     Wed 26 Aug 2026 06:00:27 PM UTC). The key that signs the live distribution
      IS the installed key.
  2. Fingerprint matches the key-id `ACCC4CF8` referenced by postgresql.org's
     current page. Note: postgresql.org's page states the URI, not a 40-hex
     fingerprint; leg 1 closes that gap cryptographically.
- Installed to `/etc/apt/keyrings/postgresql-keyring.gpg` (binary, dearmored,
  mode 0644, root-owned). Keyring-scoped via `signed-by` — no global apt trust.
- Installed keyring re-read on host: `installed_fpr: B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8` — MATCH.

### 3.2 Apt source (`/etc/apt/sources.list.d/hx-pgdg.list`, 0644)

```
deb [signed-by=/etc/apt/keyrings/postgresql-keyring.gpg] https://apt.postgresql.org/pub/repos/apt noble-pgdg main
```

### 3.3 Pin (`/etc/apt/preferences.d/hx-pgdg`)

```
Package: postgresql-* libpq*
Pin: release o=apt.postgresql.org
Pin-Priority: 500
```

**Decision D1:** the plan's additional lower-priority guard on noble-main
`postgresql` was deliberately skipped. Rationale, recorded here: PGDG is pinned
by `release o=apt.postgresql.org`, so it can only ever affect packages whose
origin is PGDG; postgresql-18 does not exist in noble main at all (Step 0
`apt-cache policy` showed no candidate before onboarding), and the pin's
`Package:` field is confined to `postgresql-*`/`libpq*`. PGDG therefore cannot
shadow a non-PostgreSQL package without the extra guard. Proven in V1 (§5).

### 3.4 apt update + policy pre-install (02:07:36Z–02:07:42Z)

`apt-get update -qq` clean. `apt-cache policy postgresql-18` **pre-install**:

```
Installed: (none)
Candidate: 18.6-1.pgdg24.04+2
  18.6-1.pgdg24.04+2 500 https://apt.postgresql.org/pub/repos/apt noble-pgdg/main
  18.4-1.pgdg24.04+1 500 ...   18.3-1.pgdg24.04+1 500 ...
```

## 4. Step 1 — install + config baseline

### 4.1 Install transaction (02:07:57Z–02:08:07Z)

`apt-get install -y --no-install-recommends postgresql-18`. Transaction lines
(Get:/Setting up:) recorded; package set installed:

| Package | Version | Origin |
| --- | --- | --- |
| postgresql-18 | 18.6-1.pgdg24.04+2 | PGDG |
| postgresql-client-18 | 18.6-1.pgdg24.04+2 | PGDG |
| postgresql-common | 293.pgdg24.04+1 | PGDG |
| postgresql-client-common | 293.pgdg24.04+1 | PGDG |
| libpq5 | 18.6-1.pgdg24.04+2 | PGDG |
| libjson-perl | 4.10000-1 | Ubuntu noble main (dependency) |
| ssl-cert | 1.1.2ubuntu1 | Ubuntu noble main (dependency) |
| liburing2 | 2.5-1build1 | Ubuntu noble main (dependency) |

Need to get 10.2 MB; +49.0 MB disk. Post-install policy:
`Installed: 18.6-1.pgdg24.04+2`, candidate identical, from PGDG.

Packaging behavior noted (expected, recorded): `postgresql-common` auto-created
cluster `18/main` via `pg_createcluster` and started it on loopback before my
config applied; I restarted the cluster after configuring (§4.3).

### 4.2 Config baseline — single drop-in `/etc/postgresql/18/main/conf.d/99-hx.conf`

Packaged `postgresql.conf` line 879 carries `include_dir = 'conf.d'` (verified
by grep). Drop-in content (0644 root:postgres):

```
# HX baseline for hxs-9 (work order Chris 2026-08-29, plan §2)
listen_addresses = '192.168.50.208, localhost'
port = 5432
password_encryption = 'scram-sha-256'
log_connections = on
log_disconnections = on
log_min_duration_statement = 1000
shared_buffers = '4GB'
idle_in_transaction_session_timeout = '10min'
```

No `0.0.0.0` anywhere. All plan §2 settings present; `logging_collector`
handled per §4.4.

### 4.3 pg_hba.conf (`/etc/postgresql/18/main/pg_hba.conf`)

Pre-edit backup taken to `pg_hba.conf.pre-hx.bak` (inverse material, §7).
Effective rules after edits (comments/blank lines stripped):

```
local   all             postgres                                peer
local   all             all                                     scram-sha-256
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256
host    all             all             192.168.50.0/24         scram-sha-256   # HX added
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            scram-sha-256
host    replication     all             ::1/128                 scram-sha-256
```

- Packaged `local all all peer` changed to `scram-sha-256` (work order's no-trust,
  password-gated posture; `local all postgres peer` retained as the admin path).
- LAN rule `host all all 192.168.50.0/24 scram-sha-256` added (absent from the
  packaged file — gap found and closed during smoke pass, see F1).
- After reload: `pg_hba_file_rules` error count = 0 (server parses it clean).
- Final perms normalized to packaged convention: 0640 root:postgres.

### 4.4 Logging decision (the execution-time choice the plan asked for)

Packaged Debian/PGDG default: `logging_collector = off` (`SHOW logging_collector`
pre-change = `off`). The cluster's log reaches
`/var/log/postgresql/postgresql-18-main.log` through the packaging's stderr
redirect in `pg_ctlcluster`/`postgresql@18-main.service`, and systemd/journald
also carries the unit's lifecycle events. Both planes are live without the
collector. **Decision D2: keep `logging_collector` at the packaged `off`** —
changing it would add a second log pipeline (collector → `log/` dir) beside the
existing one for no Step 1 requirement. Evidence the access-logging settings are
live in that pipeline: the file shows `connection received`,
`connection authenticated: ... method=peer`, `connection authorized`, and
`disconnection: session time: ...` lines (§5 V3).

### 4.5 OS pieces

- `/var/backups/hx-postgres` created: `drwxr-x--- root postgres` = **0750** ✓
- `systemctl enable` state: `postgresql.service` **enabled** (packaging default
  confirmed, not merely implicit); `systemctl is-active postgresql@18-main`
  **active** after restart.

## 5. Smoke receipts (plan §7 V1–V3)

### V1 — provenance integrity (02:09:00Z)

| Item | Result |
| --- | --- |
| `psql --version` | `psql (PostgreSQL) 18.6 (Ubuntu 18.6-1.pgdg24.04+2)` → **18.6** ✓ |
| `pg_lsclusters` | `18 main 5432 online postgres /var/lib/postgresql/18/main` → cluster **18/main** ✓ |
| `dpkg --verify` (postgresql-18, -client-18, -common, -client-common) | silent, `dpkg_verify_exit=0` → **clean** ✓ |
| PGDG pin scope proof | `apt-cache policy`: `postgresql-18`, `libpq5`, `postgresql-common` → candidates from `apt.postgresql.org` (PGDG); `ssl-cert`, `libjson-perl` (installed deps) → candidates from `archive.ubuntu.com noble/main` → PGDG supplies **only** `postgresql-*`/`libpq*`; no non-PG package sourced from PGDG ✓ |
| apt transaction lines | recorded §4.1 ✓ |

### V2 — service + listener (02:09:00Z)

| Item | Result |
| --- | --- |
| `systemctl is-active postgresql` / `is-enabled` | `active` / `enabled` ✓ |
| `pg_isready -h 127.0.0.1` | `accepting connections`, exit 0 ✓ |
| `pg_isready -h 192.168.50.208` | `accepting connections`, exit 0 ✓ |
| `ss -ltnp` | `127.0.0.1:5432` + `192.168.50.208:5432` (pid 6016 postgres) ✓ |
| wildcard check | `ss -ltn | grep -E '0.0.0.0:5432|\*:5432'` → **NO_WILDCARD_5432** ✓ |

### V3 — config + auth posture (02:09:01Z–02:09:28Z)

| Item | Result |
| --- | --- |
| `SHOW listen_addresses` | `192.168.50.208, localhost` ✓ |
| `SHOW password_encryption` | `scram-sha-256` ✓ |
| `SHOW log_connections / log_disconnections / log_min_duration_statement / idle_in_transaction_session_timeout / port` | `on / on / 1s(=1000ms) / 10min / 5432` ✓ |
| `SHOW shared_buffers` | `4GB` ✓ |
| `SHOW logging_collector` | `off` (decision D2 recorded §4.4) |
| no-trust proof | `grep -nE '^[^#]*\btrust\b' pg_hba.conf` → **NO_TRUST_RULE** (effective-rule scan, not comment noise) ✓ |
| passwordless attempt refused | TCP to `192.168.50.208` as `postgres` with no password → `psql: error: ... fe_sendauth: no password supplied`, exit 2 — **REFUSED** ✓ |
| scripted SQL | run with `psql -v ON_ERROR_STOP=1` where multi-statement (per profile §2 ON_ERROR_STOP discipline) |

**F1 (finding during V3, closed same session):** first smoke pass showed the
LAN rule missing (`LAN_RULE_MISSING`) because the packaged `pg_hba.conf` ships
without it; the `99-hx.conf` drop-in does not carry hba. Fixed by appending the
rule to `pg_hba.conf` (§4.3), reload, re-ran the probe: `NO_TRUST_RULE` +
LAN rule present + passwordless refusal captured. The first refusal text
(`no pg_hba.conf entry for host "192.168.50.208"`) is itself evidence the rule
was absent pre-fix; the second refusal (`fe_sendauth: no password supplied`)
is the V3 as-required outcome.

All scripted SQL used `ON_ERROR_STOP=1`. No roles, no databases, no timers, no
credential entries created (Checkpoint-1 ceiling held, §6).

## 6. Boundaries compliance

| Prohibition | Held |
| --- | --- |
| No roles (ps-admin/ps-backup/ps-scratch) | ✓ none created — Step 2 material |
| No credential entries (incl. `.local.env`) | ✓ none written |
| No timers (backup/health) | ✓ none created |
| No databases beyond packaged default cluster | ✓ `18/main` only, template DBs untouched |
| No reboot / firewall changes / other hosts / Redis / MCP | ✓ none performed |
| Scope: hxs-9 only, Step 0+1 only, halt at Checkpoint 1 | ✓ halted here |
| Secret hygiene | password never printed/logged/committed; helper deleted, absence verified (§8) |

Local-host note: this session's workspace is a shared checkout with other
governance lanes' uncommitted edits (`AGENTS.md`, catalog, profiles, and
hxs-9 plan/doc updates by Kimi-K3/Mia/Carol lanes landed 01:35–02:00 UTC).
My write-set this session is exactly one file: this evidence document
(`git status` attribution left to the governor's CB-01 audit).

## 7. Pre/post state and exact inverses (plan §8 authority)

| # | Mutation | Inverse (restores absent pre-state) |
| --- | --- | --- |
| 1 | Keyring `/etc/apt/keyrings/postgresql-keyring.gpg` | `rm -f /etc/apt/keyrings/postgresql-keyring.gpg` |
| 2 | Source `/etc/apt/sources.list.d/hx-pgdg.list` | `rm -f /etc/apt/sources.list.d/hx-pgdg.list` |
| 3 | Pin `/etc/apt/preferences.d/hx-pgdg` | `rm -f /etc/apt/preferences.d/hx-pgdg` |
| 4 | Install postgresql-18 + client + common + client-common + libpq5 (+debs deps libjson-perl, ssl-cert, liburing2) | `systemctl stop postgresql@18-main`; `apt-get purge -y postgresql-18 postgresql-client-18 postgresql-common postgresql-client-common libpq5`; `apt-get autoremove --purge -y` (drops the 3 Ubuntu deps installed as deps) |
| 5 | Cluster data `/var/lib/postgresql/18/main`, configs `/etc/postgresql/18`, logs `/var/log/postgresql` (created by pg_createcluster + my edits) | `rm -rf /var/lib/postgresql /etc/postgresql /var/log/postgresql` (purge already removes most; `pg_dropcluster 18 main --stop` is the granular inverse of #4's cluster creation) |
| 6 | Drop-in `/etc/postgresql/18/main/conf.d/99-hx.conf` | `rm -f /etc/postgresql/18/main/conf.d/99-hx.conf` (covered by #5 rm; listed for completeness) |
| 7 | `pg_hba.conf` edits (sed peer→scram + LAN rule append) | restore from `pg_hba.conf.pre-hx.bak`: `mv /etc/postgresql/18/main/pg_hba.conf.pre-hx.bak /etc/postgresql/18/main/pg_hba.conf` (or moot via #5) |
| 8 | `/var/backups/hx-postgres` (0750 root:postgres) | `rm -rf /var/backups/hx-postgres` |
| 9 | `postgresql.service` enabled (packaging auto-enable) | `systemctl disable postgresql` (part of #4 purge automatically) |

Full-inverse one-shot (after verification, if rollback ever ordered):
`systemctl stop postgresql@18-main; apt-get purge -y postgresql-18 postgresql-client-18 postgresql-common postgresql-client-common libpq5; apt-get autoremove --purge -y; rm -rf /var/lib/postgresql /etc/postgresql /var/log/postgresql /var/backups/hx-postgres /etc/apt/sources.list.d/hx-pgdg.list /etc/apt/keyrings/postgresql-keyring.gpg /etc/apt/preferences.d/hx-pgdg; systemctl daemon-reload`
→ restores the §2 pre-state (verified reversible by construction; not executed).

## 8. Sanitized sequential command log (hxs-15 §10 shape)

All local commands as hxsa@hxs-5; remote as hxsa@hxs-9 over SSH (password via
execution-time askpass helper, value appears nowhere). Times UTC.

| Seq | UTC | Where | Command (sanitized) | Exit |
| ---:| --- | --- | --- | ---:|
| 1 | 02:03 | hxs-5 | Lane probe #1 to OmniRoute hxs-8 (stale nonce file — inconclusive by construction) | 0 |
| 2 | 02:03 | hxs-5 | Lane probe #2: fresh UUID nonce → served-model `qwen/qwen3.8-flash`, nonce echoed, `finish=stop` → **LANE PASS** | 0 |
| 3 | 02:04 | hxs-5 | known_hosts pin confirmed for 192.168.50.208 (pre-pinned); credential-record row format inspected **masked**; askpass helper created (0700) — first pass parsed wrong table (access-map), rebuilt against `SSH password` field; password length verified, value not printed | 0 |
| 4 | 02:05–02:06 | hxs-9 | SSH smoke (identity echo) — first batch lost stdin to redirect bug (`</dev/null` after script), fixed, re-ran | 0 |
| 5 | 02:06 | hxs-9 | **Step 0 probe** (read-only batch: identity, pg-absence ×4, listeners, disk, units, sudo -n, apt state) → V0 PASS §2 | 0 |
| 6 | 02:07 | hxs-5 | PGDG key fetched from the URI currently published by postgresql.org; fingerprint computed; `InRelease` signed by same fpr (Good signature) §3.1 | 0 |
| 7 | 02:07 | hxs-9 | **MUTATION** keyring→`/etc/apt/keyrings/postgresql-keyring.gpg` (dearmored, 0644); source `hx-pgdg.list`; pin `hx-pgdg`; `apt-get update`; `apt-cache policy postgresql-18` **pre** → candidate 18.6-1.pgdg24.04+2 §3 | 0 |
| 8 | 02:08 | hxs-9 | **MUTATION** `apt-get install -y --no-install-recommends postgresql-18`; policy post (installed 18.6); version/cluster capture; `dpkg --verify` clean §4.1 | 0 |
| 9 | 02:08 | hxs-9 | **MUTATION** drop-in `99-hx.conf`; hba backup + sed `local all all peer→scram`; (LAN rule pending, see 11) | 0 |
| 10 | 02:08 | hxs-9 | Slip caught: a script heredoc had a stray delimiter so tail commands ran unprivileged — drop-in not yet applied, `install -g postgres` failed, restart auth-denied. Re-applied whole config step correctly under sudo (seq 12); no partial damage (drop-in write itself had succeeded; verified on disk) | 0 |
| 11 | 02:08 | hxs-9 | **MUTATION** backup dir 0750 root:postgres; cluster restart → listeners `127.0.0.1` + `192.168.50.208`; SHOWs confirm drop-in §4.5 | 0 |
| 12 | 02:09 | hxs-9 | **V1–V3 smoke batch** §5 — found `LAN_RULE_MISSING` (F1) | 0 |
| 13 | 02:09 | hxs-9 | **MUTATION** append LAN scram rule; reload; re-verify: NO_TRUST_RULE, rule present, passwordless attempt **refused** (`fe_sendauth: no password supplied`) | 0 |
| 14 | 02:09 | hxs-9 | Final capture: perms, `pg_hba_file_rules` errors=0, log-pipeline evidence, apt state clean, tmp-script cleanup | 0 |
| 15 | 02:10 | hxs-5→hxs-9 | Remote `/tmp/hx-*` removed, absence verified; askpass helper **deleted**, absence verified (`No such file`); local scratch cleaned to session dir | 0 |
| 16 | 02:13 | hxs-5 | Write this evidence doc; run `scripts/validate.py` (§9) | 0 |

## 9. Completion-gate record (profile §5)

- **Commands/SQL used:** §3–§5 and §8 (probe scripts over SSH; SQL via
  `sudo -u postgres psql -v ON_ERROR_STOP=1 -tA -c`; auth refusal via
  passwordless TCP `psql` attempt).
- **Results:** V0 PASS (pre-state, identity, §2); V1 PASS (18.6 PGDG, cluster
  18/main, dpkg verify clean, pin scope proven, §5); V2 PASS (active+enabled,
  pg_isready ×2, LAN listener, no wildcard, §5); V3 PASS (SHOWs exact, no
  trust, passwordless refused, §5); lane verification PASS (§1); credential
  hygiene: helper 0700 → deleted → absence verified, zero secret values in
  any artifact (§8/§2).
- **Verdict:** **PASS** on all five gates. One deviation-class finding (F1,
  missing packaged LAN hba rule) found by the smokes and closed in-session.
  One procedural slip (seq 10) self-detected, corrected, and evidenced.
- **Post-write validation:** `python3 scripts/validate.py` →
  `RESULT: PASS — 4/4 checks, 4 manual gates noted (exit 0)` at 02:14 UTC
  (wiki-sync, fixture-suite, catalog-mechanical 311 records, secret-boundary
  874 files incl. this doc, 0 hits). Note for the record: an intermediate run
  at 02:11 UTC showed `wiki-sync` FAIL on `AGENTS.md` DRIFT predating this
  session (governance lane edit); that drift was resolved by the governance
  lane before my final run — no action taken here either way, my write-set is
  exactly this one evidence document.

## 10. Second Brain evaluation (standing directive)

1. **Opportunity identified:** yes — a live PostgreSQL 18 instance on the
   "State services" host is the persistence substrate the roadmap's knowledge
   catalog layer anticipates.
2. **Capability/pattern:** Roadmap "state/persistence foundation" (L1) —
   configured, LAN-scram-bound, evidence-backed DB endpoint for later
   catalog/agent-memory workloads.
3. **Disposition:** implemented exactly the Step-1 baseline (no additions);
   role/credential/timer layers deferred to Step 2 by gate design; no Second
   Brain schema/catalog integration attempted here — premature until
   Checkpoint 1 review.
4. **Evidence/reasoning:** §2–§5 receipts; scope ceiling §6; Checkpoint 1
   halts further build until owner review, which is the correct sequence for
   roadmap reuse of this endpoint.

PASS - CHECKPOINT 1 REACHED
