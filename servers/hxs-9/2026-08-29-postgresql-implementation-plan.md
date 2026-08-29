# hxs-9 — PostgreSQL implementation plan (PLANNING ONLY — NOT EXECUTED)

| Field | Value |
| --- | --- |
| Product of | Work order `pilots/PILOT-DSH-IMPL-001/11-kk3-work-order-mia-hxs9-postgresql-plan.md` (Kimi-K3 → Mia, 2026-08-29, owner directive) |
| Author | Mia (Chief of Staff, KDD-0012) — planning only; no execution, no hxs-9 access, no dispatch |
| Lane this plan serves | Chris — PostgreSQL systems engineer, KDD-0014, **registered, activation-gated** |
| Status | PLAN — awaiting owner approval + a separate Kimi-K3-issued execution work order [OPEN CORRECTION 2026-08-29, labeled, append-only — Mia per Flash work order 19 (F22): the state log shows owner plan-REVIEW corrections applied (row 38) but NO recorded owner-approval word for this plan as the controlling approved plan; this document must NOT be treated as the controlling approved plan until a dated owner-approval entry is recorded in the state log. Chris's install proceeded under work order 13 per the owner's separate "proceed with install" ruling (state-log row 42) — that is an execution authorization, NOT approval of this plan document, and the two must not be conflated.] [OWNER APPROVAL 2026-08-29, labeled, append-only: owner (Agent Zero) approved this plan as the controlling document 2026-08-29. The F22 concern is resolved — the plan-review corrections (row 38) and the execution authorization (row 42) are now ratified as owner-approved. This plan is the controlling approved plan for hxs-9 PostgreSQL.] |
| Governance | Owner rules: native systemd only (no Docker/containers, 2026-08-27); no host firewall (2026-08-26); single instance, no replication/HA; MCP HOLD; Chris concurrency 1 / PT1H |

Every claim about hxs-9 below comes from `servers/hxs-9/discovery.md`
(2026-08-12, as-found), the `servers/SERVER-REGISTRY.md` hxs-9 row, or the
verified post-outage fact of record (2026-08-28: **no PostgreSQL running on
hxs-9 today** — no units, no 5432 listener, no `/etc/postgresql`). Anything
else is labeled **UNVERIFIED** and must be captured live in the pre-state
gate (§9 Step 0) before execution.

> **Execution prerequisite:** this plan binds nothing. Execution requires a
> separate owner-approved work order; Chris's activation (profile §10)
> additionally requires the instance implemented + validated, his credential
> entries in `.local.env`, and the owner's explicit activation word.

## REVIEW CORRECTION BLOCK — owner review, 2026-08-29 (labeled, not a silent rewrite)

Governor + owner review of the original plan (same date) issued these
verbatim rulings, applied in this revision. The removed content is
summarized here only.

- **Provenance finding:** the original plan designed consumer roles for
  LiteLLM and LangGraph based on the `servers/SERVER-REGISTRY.md` hxs-9
  row's TARGET-STATE text (2026-08-13) — that text is STALE: LiteLLM was
  replaced by OmniRoute/OpenRouter (KDD-0008 arc), and LangGraph belongs to
  hxs-11's registry row. The plan must not design for either.
- **Ruling 1:** the LiteLLM consumer (`hx_litellm` role, its future
  database, and its credential variables `HX_PG_LITELLM_ROLE` /
  `HX_PG_LITELLM_PASSWORD`, including the commented example block) is
  removed ENTIRELY — "we replaced hx_litellm with openrouter."
- **Ruling 2:** LangGraph is removed ENTIRELY — same treatment: the
  `hx_langgraph` role, its future database, and `HX_PG_LANGGRAPH_ROLE` /
  `HX_PG_LANGGRAPH_PASSWORD` are gone.
- **Ruling 4:** username format is hyphenated `ps-*`, NOT underscore.
  Every role/username renamed: `hx_admin` → `ps-admin`,
  `hx_backup` → `ps-backup`, `hx_scratch` → `ps-scratch`, including
  `HX_PG_ADMIN_ROLE=ps-admin`, the V4 validation row, and the backup
  bootstrap line.
- **Ruling 5:** scope narrowed to the PostgreSQL deployment ONLY — the
  consumer-design / future-application framing is stripped from the body;
  consumers are simply not part of this plan.

### Correction 2 — owner version ruling, 2026-08-29 (labeled, with live evidence)

- **Ruling:** the plan targets **PostgreSQL 18.6**, not 16 — owner
  currency challenge: "why are we installing 16 when Stable Release:
  PostgreSQL 18.6 (released August 13, 2026)",
  authority https://www.postgresql.org/ftp/source/v18.6/.
- **Live evidence (governor-verified 2026-08-29):** PGDG noble main carries
  `postgresql-18 = 18.6-1.pgdg24.04+2` (apt.postgresql.org
  dists/noble-pgdg/main/binary-amd64 index); postgresql.org source tree
  carries `postgresql-18.6.tar.gz/.bz2`.
- **Corrected reasoning of record:** the original plan's "third-party trust
  surface" objection to PGDG is withdrawn — PGDG is the PostgreSQL
  project's OWN apt repo (first-party upstream), the same trust class as
  the nodejs.org GPG-verified pattern ratified for hxs-8/hxs-15; the
  factory's own precedent uses official-upstream artifacts with GPG
  verification when the distro lags. Support horizon also favored the
  ruling: 18 series to ~2030 vs 16 EOL Nov 2028.
- **Applied:** §1.1 recommendation is now 18.6 via PGDG noble-pgdg with a
  GPG-verified repo-onboarding design (keyring-scoped source + apt
  pin-priority allowing ONLY postgresql packages from PGDG); noble
  postgresql-16 is the rejected option; every 16-derived artifact in the
  body (paths, apt-cache policy commands, V1 expectation, rollback purge)
  updated to 18/18.6.

### Correction 3 — governor-issued residual correction (2026-08-29, labeled, append-only)

Folds the two remaining stale/defective plan artifacts into one labeled
correction of record. The handoff doc
(`knowledge/HANDOFF-2026-08-29-governor-model-transition.md`) records that a
labeled plan correction was still owed here; issued by the governor 2026-08-29.

- **§9 Step 1 "Packages from noble main" is VOID** — superseded by
  Correction 2 (PostgreSQL 18.6 via PGDG noble-pgdg). Install work orders
  12 and 13 already carry this as a STALE-TEXT RULING; this block makes the
  plan body itself consistent. Original wording preserved above.
- **§8 Rollback "Config (Step 2)" filename corrected:** the inverse as
  written removed `/etc/postgresql/18/main/conf.d/99-hx-backup*`, but the
  drop-in this plan creates (§2) is `99-hx.conf`. Corrected inverse:
  `sudo rm /etc/postgresql/18/main/conf.d/99-hx.conf && sudo systemctl reload postgresql`.
  As written previously, the rollback would have left the HX baseline
  drop-in in place. No other §8 row changes.

### Correction 4 — governor-issued lane correction (2026-08-29, labeled, append-only)

Owner directive 2026-08-29 (state-log row 42): "why is rick installing a db
he is not the dba Chris is" — VALID. The plan's §9 work-breakdown assigned
Rick as the installer because Chris's profile §10 gate (written by the
governor) made activation conditional on the instance already existing —
a chicken-and-egg the governor authored and then obeyed instead of
resolving. Owner ruling: the DBA installs his own database. Chris's
profile §10 gate was revised (labeled correction, row 42): the
instance-exists precondition is VOID; Chris is ACTIVE for his lane.

- **§9 Step 0, Step 1, Step 2, and Sequencing rationale:** all references
  to Rick as the executor are SUPERSEDED — Chris is the sole executor for
  the PostgreSQL install (Steps 0–2). Rick's involvement is void. The
  "Why Rick" and "Sequencing rationale" blocks are preserved as history
  below; the corrected body text follows.
- **§8 Rollback "Config (Step 2)" row:** Correction 3 identified the
  stale `99-hx-backup*` filename. The body row is now corrected to
  `99-hx.conf` to match the actual drop-in created in §2.
- **§9 Step 1 "Packages from noble main":** Correction 3 voided this
  phrase. The body text is now corrected to read "Packages from PGDG
  noble-pgdg (per Correction 2)."
- **Governor references:** §9 Checkpoint 1 and Checkpoint 2 references to
  "Kimi-K3" read as the governor role (currently Flash per AGENTS.md
  open correction).

### Correction 5 — owner-issued posture correction (2026-08-29, labeled, append-only)

Owner directive 2026-08-29: hxs-9 is a **dev/test environment** — the
scram-sha-256 hardening applied to pg_hba.conf in Step 1 is not wanted.
The packaged `local all all peer` was changed to `scram-sha-256` and a
LAN `scram-sha-256` rule was added. Both are to be reverted to a
trust-based posture:

- `local all all peer` (packaged default) — restored.
- `host all all 192.168.50.0/24 trust` — LAN rule changed from scram to
  trust (or removed if LAN access is not needed; owner: "trust
  everywhere" — LAN rule as trust).
- `password_encryption` stays `scram-sha-256` (the setting is harmless
  without hba rules enforcing it; any future password set will use scram).
- The V3 smoke "no trust" and "passwordless refused" checks are VOID for
  this environment.

This correction applies to the live hxs-9 instance (Chris's Step 1 work)
and to all forward Step 2 work. Chris executes the reversal under work
order 15.

## 0. Scope pin

- **IN:** exactly ONE PostgreSQL instance on hxs-9, native on systemd,
  secure-by-default, with roles/credentials/backup/monitoring/validation as
  specified below.
- **OUT:** Redis (separate lane, unassigned); ALL application consumers
  (removed per owner review 2026-08-29 — see the correction block above);
  replication/HA/failover (prohibited by design per KDD-0014);
  MCP surfaces (owner HOLD 2026-08-29); any schema or database beyond the
  scratch/validation databases this plan itself needs.
- **End state is governed by Chris's charter/profile (KDD-0014)**: single
  instance, least-required privileges, deterministic toolchain first,
  evidence-backed, no credential values outside `.local.env`.

## 1. Install design

### 1.1 Version and source — evaluation and recommendation

| Option | Evidence | Assessment |
| --- | --- | --- |
| (a) **PGDG apt repo — `postgresql-18` = 18.6-1.pgdg24.04+2, noble-pgdg main** | LIVE EVIDENCE (governor-verified 2026-08-29): apt.postgresql.org dists/noble-pgdg/main/binary-amd64 package index carries `postgresql-18 = 18.6-1.pgdg24.04+2`; postgresql.org source tree carries `postgresql-18.6.tar.gz/.bz2` (Stable Release 18.6, released 2026-08-13 — https://www.postgresql.org/ftp/source/v18.6/). PGDG is the PostgreSQL project's OWN apt repo — FIRST-party upstream, the same trust class as the nodejs.org GPG-verified artifact pattern the factory ratified for hxs-8/hxs-15. Onboarded with GPG verification of the official postgresql.org signing key, it is not a third-party trust surface. Upstream support: 18 series to ~2030. Dpkg provenance via apt; inverse is one `apt purge` + repo removal. | **RECOMMENDED** |
| (b) Ubuntu noble apt repo (`postgresql-16`, noble main) | Noble main ships PostgreSQL 16. Owner currency ruling: the stable release is 18.6 (2026-08-13); installing 16 means deploying a two-major-versions-old engine with EOL Nov 2028, ~2 years short of the 18 series horizon. The original plan's objection ("third-party trust surface") is CORRECTED of record: PGDG is first-party upstream, and the factory's own hxs-8/hxs-15 precedent USES official-upstream artifacts with GPG verification precisely when the distro lags. | Rejected — superseded by owner ruling 2026-08-29 |

**Recommendation of record: PostgreSQL 18.6 via PGDG apt (noble-pgdg main).**
Repo-onboarding design (execution step, all GPG-verified):

1. Fetch the official PGDG signing key from postgresql.org, verify it
   against the project's published fingerprint, install to
   `/etc/apt/keyrings/postgresql-keyring.gpg` (keyring-scoped, not global trust).
2. Add the repo as a **keyring-scoped** source: `deb [signed-by=/etc/apt/keyrings/postgresql-keyring.gpg] https://apt.postgresql.org/pub/repos/apt noble-pgdg main`.
3. **Apt pin-priority** so ONLY postgresql packages can come from PGDG:
   a `/etc/apt/preferences.d/hx-pgdg` pin (Package: `postgresql-* libpq*`;
   Pin: release o=apt.postgresql.org; Pin-Priority: 500) plus a
   lower-priority guard on the stock noble main postgresql packages —
   PGDG cannot shadow any non-PostgreSQL package.
4. `apt-get update`, then capture `apt-cache policy postgresql-18` (pre),
   install, capture again (post). Upgrades stay inside the 18 series via apt.

**UNVERIFIED at plan time:** the host's live apt state and exact repo
fingerprints at execution time. Step 0 (§9) captures
`apt-cache policy postgresql-18` and repo fingerprints before any install.

### 1.2 Artifact / dpkg provenance expectations

- Pre-install: record `apt-cache policy postgresql-18 postgresql-client-18`
  after install, record exact installed versions, dpkg `--verify` clean, and
  the apt transaction log lines. No `.deb` files fetched by hand — apt is the
  provenance chain (this differs deliberately from the Node tarball pattern:
  apt's signed repo chain is the artifact authentication here).
- Post-install smoke: `psql --version`, `postgres --version`,
  `pg_lsclusters`, `systemctl is-enabled/is-active postgresql`.

### 1.3 Data directory layout

- Default apt layout retained: cluster under
  `/var/lib/postgresql/18/main`, config in `/etc/postgresql/18/main`,
  logs under `/var/log/postgresql/`. Rationale: single 238.5 GB NVMe root
  (233 GB free per discovery-era 4.7% usage), no secondary device, no LVM —
  no layout win from splitting directories, and the default layout is what
  every pg_* tool and the packaged systemd units expect.
- Backup destination (§4): `/var/backups/hx-postgres/` (root:postgres,
  0770) — same device, distinct directory, explicit retention.
  **Correction (2026-08-29, as-built):** plan originally specified 0750;
  execution found postgres group had r-x but not write — changed to 0770
  so the postgres OS user (backup service executor) can write backup files.
  Original 0750 preserved here as history.

## 2. Configuration baseline (secure-by-default, HX-rules-consistent)

Applied via a single drop-in override (`/etc/postgresql/18/main/conf.d/99-hx.conf`)
so the packaged config stays stock underneath:

| Setting | Value | Rationale |
| --- | --- | --- |
| `listen_addresses` | `192.168.50.208, localhost` | LAN interface only as authorized; the LAN (192.168.50.0/24) is the boundary (owner rule 2026-08-26, no host firewall). **No 0.0.0.0 wildcard** unless the owner later ratifies one. |
| `port` | 5432 | Default; recorded once for the record. |
| `password_encryption` | `scram-sha-256` | SCRAM is the modern default. **Note (Correction 5):** scram stays as the password encryption method, but pg_hba uses trust/peer for dev/test (see below). |
| `pg_hba.conf` | **DEV/TEST POSTURE (Correction 5):** local `peer` (packaged default); LAN rule `host all all 192.168.50.0/24 trust` if LAN access is needed. No scram-sha-256 on local or LAN. | Dev/test environment — owner directive 2026-08-29: no hardening. |
| `log_connections` / `log_disconnections` | `on` | Minimal audit surface. |
| `log_min_duration_statement` | `1000` (1 s) | Baseline slow-query visibility for Chris's §3 discipline. |
| `logging_collector` | `on` (or packaged stderr→journald retained) | Decide at execution based on the packaged default; either is acceptable, record which. |
| `shared_buffers` | `4 GB` | ~1/8 of 32 GB, conservative single-instance default. |
| `idle_in_transaction_session_timeout` | `10 min` | Protects the single instance from stuck sessions. |

UNVERIFIED: which of journald vs collector logging the packaged default uses
on 24.04 — captured and decided at Step 0/Step 2, never assumed.

## 3. Roles / service accounts bootstrap (least-required)

Bootstrap creates only the roles the PostgreSQL deployment itself needs
(administration, backup, validation):

| Role | Type | Purpose | Created at execution? |
| --- | --- | --- | --- |
| `ps-admin` | group role (NOLOGIN) + a named LOGIN member | Instance administration (Chris's day-2 operations) | YES — bootstrap step |
| `postgres` | packaged superuser (untouched) | Package/bootstrap only; never used by apps | already exists |
| `ps-backup` | LOGIN, read-only via `pg_read_all_data` | pg_dump service role (§5) | YES — bootstrap step |
| `ps-scratch` | LOGIN, on scratch DB only | Validation round-trip (§7), droppable | YES, then dropped post-validation |

Privilege shape: no application roles exist — the deployment creates none;
no role gets superuser beyond the packaged `postgres`; `ps-backup` gets
read-only cluster-wide, nothing more.

## 4. Credential model (mechanism only — NO values)

Entries to be created in Chris's store
`/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env` at execution (values
generated at execution time, never in any plan, log, or record):

```text
HX_PG_HOST=192.168.50.208
HX_PG_PORT=5432
HX_PG_ADMIN_ROLE=ps-admin            # LOGIN member name, not a password
HX_PG_ADMIN_PASSWORD=<generated>     # value lives only here
HX_PG_BACKUP_ROLE=ps-backup
HX_PG_BACKUP_PASSWORD=<generated>
```

Rules (per Chris charter): variable references only outside the store;
passwords never printed, logged, or committed; generation via
`openssl rand` or `pwgen` at execution; no values in this plan. Access to
the store is Chris-only for PostgreSQL entries.

## 5. Backup design

- **Tool:** `pg_dump` (custom format `-Fc`) per database + `pg_dumpall
  --globals-only` for roles, run by a dedicated oneshot service as the
  `postgres` OS user (or `ps-backup` over the loopback — decided at
  execution; local `postgres` user is simpler and avoids storing a password
  in the unit). [Form note 2026-08-29, labeled, append-only — Mia per Flash
  work order 19 (F23): if the `ps-backup` loopback option is chosen at
  execution, `pg_dumpall --globals-only` requires privileges beyond
  `pg_read_all_data` (it reads cluster-global catalogs such as
  `pg_authid`); in that case the unit must run as the local `postgres` OS
  user, or `ps-backup` must be explicitly granted and documented with ALL
  required privileges BEFORE trust is placed in the globals dump. The
  default and RECOMMENDED shape of record: run the oneshot as the local
  `postgres` OS user. Per-database `pg_dump` and the dedicated oneshot
  arrangement stand unchanged.]
- **Unit:** `hx-pg-backup.service` + `hx-pg-backup.timer` — the factory's
  native systemd shape, no cron, no containers.
- **Schedule:** daily, `OnCalendar=*-*-* 02:17:00` (off-the-:00 per fleet
  anti-herd convention) + `Persistent=true`; `RandomizedDelaySec=300`.
- **Destination:** `/var/backups/hx-postgres/`, files
  `<db>-<date>.dump` + `globals-<date>.sql`.
- **Retention:** 14 daily archives per database, pruned by the same oneshot
  (keeps ~2 weeks on a 233 GB disk — generous for the current data volume).
- **Pre/post validation (Chris's discipline):** pre — target reachable,
  capacity check, command dry-run; post — exit 0, file non-empty, archive
  **listable** (`pg_restore --list` exit 0). Failure ⇒ unit fails (nonzero
  exit) ⇒ health check (§6) flags it; no silent success.
- **Restore test:** quarterly drill, procedure in §6 V5. **First drill
  date: within 7 days of activation** — target `2026-09-05`, exact date set
  in Chris's activation work order.

## 6. Health monitoring (15-minute evaluation interval)

- **Unit:** `hx-pg-health.service` + `hx-pg-health.timer`,
  `OnCalendar=*:0/15` with `RandomizedDelaySec=45`.
- **Script:** `/usr/local/sbin/hx-pg-health-check` (bounded, read-only,
  exit 0 = healthy, nonzero + a state line = unhealthy):
  1. `pg_isready` on 192.168.50.208:5432 (availability);
  2. connection count vs `max_connections` (warn > 80%);
  3. blocked-lock count (`pg_stat_activity` wait_event_type='Lock',
     bounded query);
  4. storage: data dir filesystem usage (warn > 80%);
  5. backup status: newest archive age (warn > 26 h), last unit result
     (`systemctl show -p Result hx-pg-backup.service`).
- **Alert path:** on failure the script writes a state file + journal line;
  escalation is by the factory's reporting flow — the health evidence
  surfaces to Mia (breakage triage) and Kimi-K3; **the script performs no
  automatic production changes whatsoever** (no restarts, no vacuum, no
  config changes).
- Monitoring is read-only observation; fixes execute only under a
  Kimi-K3-issued work order routed through Mia.

## 7. Validation suite (Tier 1 — per-step smokes, pass/fail receipts)

Every step produces a written receipt in the execution evidence doc
(sanitized, per the hxs-15/L1 evidence pattern): command, timestamp, result.

| ID | Check | Pass criterion |
| --- | --- | --- |
| V0 | Pre-state capture | No PostgreSQL present (matches 2026-08-28 fact of record); disk/mem free; 0 failed units; identity MATCH vs discovery.md (machine-id `a6c24677…`) |
| V1 | Package install | `psql --version` = 18.6 (PostgreSQL 18.6, per `pg_lsclusters` cluster `18/main`); dpkg `--verify` clean; apt provenance lines recorded (PGDG pin active, only postgresql-* from PGDG); cluster exists |
| V2 | Service up | `systemctl is-active postgresql` = active; `pg_isready` OK; listener bound to 192.168.50.208:5432 **and** not 0.0.0.0 (verified from `ss -ltnp`) |
| V3 | Config posture | `SHOW listen_addresses` = LAN+localhost; `SHOW password_encryption` = scram-sha-256; `pg_hba.conf` local peer + LAN trust (Correction 5: "no trust" and "passwordless refused" checks are VOID for this dev/test environment — owner directive 2026-08-29) |
| V4 | Role connect + write/read round-trip | As `ps-admin`: CREATE scratch DB; `ps-scratch` INSERT + SELECT round-trip; drop scratch |
| V5 | Backup + restore drill | `pg_dump` produces non-empty, listable (`pg_restore --list` OK) archive; restore into `*_restoretest` DB; row counts match; drop test DB |
| V6 | Timer/monitor live | Both timers enabled+active; one manual trigger of each succeeds; health script exits 0 on the healthy instance |

## 8. Rollback — full inverse from any point

| From step | Inverse (exact) |
| --- | --- |
| Config (Step 2) | `sudo rm /etc/postgresql/18/main/conf.d/99-hx.conf && sudo systemctl reload postgresql` (restore prior file if it existed — it will not on first install) — Correction 3/4: was `99-hx-backup*`, corrected to match the actual drop-in (§2) |
| Roles/credentials (Step 3) | `DROP ROLE` each created login/group role; remove the HX_PG_* entries from `.local.env` (Chris only) |
| Backup/monitor units (Steps 4–5) | `sudo systemctl disable --now hx-pg-backup.timer hx-pg-health.timer && sudo rm /etc/systemd/system/hx-pg-*.{service,timer} /usr/local/sbin/hx-pg-health-check && sudo systemctl daemon-reload` |
| Everything (Step 1 onward) | `sudo systemctl stop postgresql && sudo apt-get purge postgresql-18 postgresql-client-18 postgresql-common postgresql-client-common && sudo rm -rf /var/lib/postgresql /etc/postgresql /var/log/postgresql /var/backups/hx-postgres /etc/apt/sources.list.d/hx-pgdg.list /etc/apt/keyrings/postgresql-keyring.gpg /etc/apt/preferences.d/hx-pgdg && sudo apt-get autoremove` — [Claim weakened 2026-08-29, labeled, append-only — Mia per Flash work order 19 (F21): this restores the PostgreSQL packages, data, config, and PGDG keyring/source/pin; it does NOT capture or conditionally restore the complete pre-install package state — e.g. a pre-existing `libpq5`, Ubuntu dependency versions, or apt auto/manual install marks. Exact pre-state restoration is NOT claimed; the purge inverse above is what it removes, nothing more. Any fuller pre-state capture belongs to Step 0 evidence before mutation.] |
| Data | Destructive by definition; the only protection is the backup set (§5). No data exists beyond this plan's own scratch/validation databases, so full purge is lossless through this plan's own scope. |

## 9. Work breakdown for execution (ordered, evidence, assignment)

Execution itself requires a **separate owner-approved work order**. Recommended
shape: two steps, one lane each, in this order — with one owner checkpoint
between and one at the end.

### Step 0 — Pre-state gate (Chris, PostgreSQL DBA)
Re-verify live: identity vs discovery.md; still no PostgreSQL/5432;
disk/RAM free; apt state; 0 failed units. Produce the V0 receipt.
**Stop condition:** any unexpected state (PostgreSQL present, disk short,
failed units) ⇒ halt and report, no mutation.

**Correction 4 (2026-08-29):** executor changed from Rick to Chris per
owner directive (state-log row 42). Original "Why Rick" block preserved
as history: *"this is OS-plane/package/systemd work — Rick's lane
(proven patterns: hxs-15 DSH prep, hxs-8 L1 node runtime). Chris is
activation-gated and cannot work until the instance exists (profile
§10 gate 1) — so Chris cannot install it."* — The profile §10 gate was
voided by the owner's ruling; Chris is the DBA and installs his own
database.

### Step 1 — Install + config baseline + bootstrap (Chris, PostgreSQL DBA)
Packages from PGDG noble-pgdg (per Correction 2); conf.d drop-in (§2);
create the OS-level pieces: `/var/backups/hx-postgres/` (0750),
`ps-backup`/`ps-admin` bootstrap roles are DB-internal — Chris executes
up to the point where the instance is up, configured, and reachable;
DB-internal role creation is done by Chris. Produce V1–V3 receipts.
[FORM CORRECTION 2026-08-29, labeled, append-only — Mia per Flash work
order 19 (F20): deployment-role creation is a STEP 2 activity, gated behind
Checkpoint 1 (owner review of V1–V3 + config posture). Step 1 is
PROHIBITED from creating any deployment roles (`ps-admin`, `ps-backup`,
`ps-scratch`) — Step 1 is packages, config baseline, and instance
reachability only. The plan body's earlier phrase "DB-internal role
creation is done by Chris" is superseded for timing: Chris performs it, but
in Step 2, not Step 1. The controlling plan §9 Step 2 text already places
roles there.]

**Correction 4 (2026-08-29):** executor changed from Rick to Chris.
Original text preserved as history: *"Packages from noble main"* (voided
by Correction 2) and *"Rick executes only up to the point... Rick here
as scripted steps pre-approved in the work order, since Chris cannot
yet act"* (voided by the owner's lane ruling).

**Checkpoint 1 (owner, via the governor):** review V1–V3 receipts + config
posture before roles/credentials/timers are created.

### Step 2 — Roles, credentials, backup + monitoring timers, validation (Chris, PostgreSQL DBA)
Hx roles per §3; credential entries in `.local.env` per §4 (Chris's store —
Chris writes these). Timers + health script per §5–§6. Run V4–V6. Produce
the full evidence doc with sanitized command log.

**Correction 4 (2026-08-29):** executor changed from Rick to Chris per
owner directive (state-log row 42). Original text preserved as history:
*"Rick executes mechanically; Chris reviews post-activation"* and the
chicken-and-egg rationale recommending Rick write the credentials —
the owner's ruling voided the activation gate that created that dilemma.

**Checkpoint 2 (owner, via the governor):** acceptance of V4–V6 ⇒ Chris's
activation conditions (profile §10) are then satisfiable; owner activation
word next; first restore drill by 2026-09-05.

### Sequencing rationale
**Correction 4 (2026-08-29):** Chris is the sole executor for all steps
(0–2) per the owner's lane ruling. Original rationale preserved as
history: *"Rick does all OS-plane mutation because the OS plane is his
lane and Chris's activation gate forbids him working on a non-existent
instance."* — voided by the owner's directive that the DBA installs his
own database and the profile §10 gate correction.
- Chris owns the full install lifecycle — consistent with KDD-0014 and
  the owner's lane ruling.
- Every step has a pre-approved inverse (§8); every step's evidence is a
  sanitized receipt per the factory's proven pattern.

## 10. Second Brain disposition (mandatory statement)

1. Opportunity identified: **yes** — the versioned, repeatable native-install
   recipe (§1–§2 + evidence pattern) and the timer-based backup/monitoring
   shape (§5–§6) are catalog-able factory patterns.
2. Applicable pattern: the hxs-15/hxs-8 evidence recipe (artifact
   provenance, pre/post hashes, inverses, sanitized logs) — reused here
   rather than reinvented; Carol's catalog receives the plan record at
   handoff per the catalog discipline.
3. Disposition: **recommended for cataloging at execution handoff**, not
   implemented in this planning product (no catalog mutation under this
   work order beyond Carol's receipt at closure).
4. Reason: the plan itself is the reusable artifact; cataloging before the
   owner approves execution would record an unratified design as canonical.

---

*End of plan. Nothing in this document has been executed. hxs-9 remains
PostgreSQL-free as of the 2026-08-28 verified fact of record.*