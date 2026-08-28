# hxs-8 — Configured State

**Phase:** Owner-authorized server implementation
**Configuration date:** 2026-08-28 (record date; implementation executed 2026-08-27 → 2026-08-28 across milestones L1-M1/L1-M2/L1-M3 of `PILOT-OMNIROUTE-LAYER0-001`)
**Assigned role:** API gateway & control (copied from `SERVER-REGISTRY.md`)
**Primary workload / model:** **OmniRoute v3.8.51 — the HX governed model-traffic plane** (Next.js 16.3.2 standalone, native systemd, no Docker), fronting the four HX LLM backends (Qwen-X hxs-1, Coder-X hxs-2, Meta-X hxs-3, Chat-X hxs-4) behind one authenticated OpenAI-compatible client plane, per the owner-authorized goal `GOAL-OMNIROUTE-L1-SECURE-CORE` (`goals/2026-08-27-omniroute-layer1-secure-core.md`).
**Approved by:** Agent-Zero (owner) — Layer 1 authorized 2026-08-27 (OD-12); L1-M3 gate GO 2026-08-28 ~05:30Z (pilot state log rows 66–67)

> Registry note (divergence recorded openly, not resolved by this record): the
> `SERVER-REGISTRY.md` Workload / Model field for hxs-8 still reads the
> target-state "LiteLLM gateway, PostgreSQL-backed on hxs-9", and its Memory
> field reads 16 GB. The owner-commissioned OmniRoute Layer-1 goal (the higher
> authority) configured the workload recorded here instead, and the 2026-08-27
> memory upgrade (48 GB, discovery addendum) supersedes the 16 GB field. The
> registry is owner-maintained and was not edited by the pilot (hxs-3
> F-REG-1 class — owner-side item).

## Discovery Reference

```text
servers/hxs-8/discovery.md
```

As-found record dated 2026-08-12 with the 2026-08-27 post-upgrade addendum;
preserved unchanged. Do not modify the discovery record.

## Role Objective

- hxs-8 is the factory's **governed model-traffic plane**: one authenticated,
  LAN-only gateway through which HX consumers reach the four HX LLM backends.
  OmniRoute provides routing, management authN/authZ, client-plane API keys,
  usage accounting, and backup/rollback for the traffic plane; it carries no
  orchestration, memory-governance, or agent authority of its own (its
  agent-like surfaces stay disabled per the goal).
- The backends remain the capability owners; hxs-8 never substitutes for them
  and never routes to cloud providers for HX workloads — with ONE
  owner-authorized exception: the OpenRouter free-tier connection `main`
  (OD-14, 2026-08-27, state-log row 39; USD 100 spend cap). Local-only remains
  the rule for agent work; the OR catalog is reachable through the gateway and
  no model allowlist currently constrains it — allowlist/scrub decisions
  remain owner-lane of record. Model reference stays alias-only per the
  backend records (`DOC-backend-*`).
- Exposure posture (OD-07): primary listener bound to the LAN interface only,
  a separate loopback listener for local semantics, OmniRoute's own
  authN/authZ, no host firewall (owner rule) — the private LAN
  192.168.50.0/24 is the boundary.

## Final Configuration

### Operating System

- Hostname: `hxs-8`
- OS: Ubuntu 24.04.4 LTS (noble); kernel `7.0.0-30-generic`
- Secure Boot: disabled (owner standing directive — never enable)
- Machine ID: `91086d5265a74450b7c2047b3b7ca2ae` (identity anchor for all
  pilot evidence; verified at every session)

### Network

- IPv4: `192.168.50.207/24` on `eno1` (sole active interface plus loopback)
- Listening services / ports: `192.168.50.207:20128` (OmniRoute primary,
  LAN-interface bind), `127.0.0.1:20128` (OmniRoute loopback listener, HX
  component), `:22` (sshd), loopback stub DNS `:53` — nothing else
- Firewall: **none** (owner rule 2026-08-26). The private LAN
  192.168.50.0/24 itself is the exposure boundary (blueprint §5); management
  endpoints sit behind OmniRoute's authN/authZ (anonymous 401, management
  session required), and the client plane requires an HX API key
- Bind design (L1-M3 pre-gate task, rr-47 follow-up): the primary listener
  binds the LAN address only (`OMNIROUTE_HOSTNAME=192.168.50.207` → the
  product's own `HOSTNAME` mapping, `scripts/build/runtime-env.mjs:177`);
  loopback service is provided by a separate raw-TCP loopback listener
  (`omniroute-loopback.service` → `/opt/omniroute/ops/loopback-listener.mjs`),
  preserving loopback semantics for local clients without a wildcard bind

### Storage

- Filesystems: root ext4 on 476.9 GB NVMe (`/dev/nvme0n1p2`); ~420 GB free
  after the build tree (13 GB) and app bundle (2.2 GB)
- Role-specific layout (`/opt/omniroute`): `app/` root-owned deployed
  standalone bundle; `src/` omniroute-owned build tree (retained evidence
  cache, documented inverse); `data/` omniroute-owned 0750 DATA_DIR
  (`storage.sqlite` + `backups/`); `ops/` root-owned ops scripts and the
  root-only client-key file; `home/` service-account home; `build-logs/`

### GPU / Accelerators

- None (no discrete GPU; Intel UHD 630 integrated only — discovery). The
  traffic plane is CPU-only; inference stays on the backend hosts

### Role-Specific Software

- Runtime: Node v24.20.0 + npm 11.19.0 at `/opt/node-v24.20.0`
  (`/usr/local/bin` symlinks; rick L1-M1, engines-qualified)
- Product: **OmniRoute v3.8.51** (pinned corpus
  `/opt/tkv-local/OmniRoute-release-v3.8.51`, content-sensitive identity
  VERIFIED 2026-08-27), built `npm run build` → Next.js 16.3.2 standalone at
  `/opt/omniroute/app` (key-file hashes in `03-trinity-l1-install.md` §3.5)
- Service shape (blueprint conventions, hashes in the install record §4 and
  the gate record §G5): `omniroute.service` — `Type=notify` +
  `NotifyAccess=all` + `WatchdogSec=60` (the product's own READY/watchdog
  design), `Restart=on-failure`, hardening (`NoNewPrivileges`,
  `ProtectSystem=strict` with `ReadWritePaths` limited to the DATA_DIR and
  the app cache, `ProtectHome`, `PrivateTmp`), budgets (`LimitNOFILE=65536`,
  `MemoryMax=8G`, `TasksMax=512`), user `omniroute` (uid 999)
- Secrets design (OD-13): `JWT_SECRET`, `API_KEY_SECRET`,
  `STORAGE_ENCRYPTION_KEY`, `INITIAL_PASSWORD` generated on-host
  (`openssl rand -hex 32` class) and injected ONLY via the root-only 0600
  drop-in `/etc/systemd/system/omniroute.service.d/20-v3.8.51-secrets.conf`
  (recorded by sha256, never value). Verified by method: 0 plaintext rows in
  the DB `secrets` namespace; connection credential fields `enc:v1:`
  AES-256-GCM ciphertext; management password bcrypt at rest
- Management credential — owner-reset 2026-08-27T18:20–18:26Z (owner's
  interactive session; current drop-in hash `05638010…`, governor-recorded
  state log row 50; "distinct dashboard password at next rotation" remains a
  standing owner-lane decision)
- Registered backends (`POST /api/providers`; identity evidence in
  `03-trinity-l1-install.md` §7): Qwen-X (hxs-1), Coder-X (hxs-2), Meta-X
  (hxs-3) active; Chat-X (hxs-4) registered `is_active=0`, loopback-only
  posture PROVEN (posture-blocked per OD-08 amendment, excluded from routing)
- Owner-added connection (owner-dispositioned, state log row 48): `main`
  (provider `openrouter`, is_active=1, api_key `enc:v1:` ciphertext) with a
  USD 100 owner-set spending limit; the `/v1/models` surface therefore also
  carries the OpenRouter catalog and built-in presets (1,496 entries at gate
  close; the 22 `hx-` alias entries and zero `hx-qwen3.5` entries are
  unchanged). No gateway model allowlist directed by the owner
- Agent-like surfaces (all verified disabled at install and re-verified at
  the L1-M3 gate): `cloudEnabled:false` (explicit row — code default TRUE),
  `skillsEnabled:false`, `mcpEnabled:false`, `a2aEnabled:false`,
  `memoryEnabled:false`, `tailscaleEnabled:false`;
  `OMNIROUTE_DISABLE_BACKGROUND_SERVICES=true`; MCP 503, A2A −32000,
  plugins `[]`, skills registry empty, embedded services `not_installed`,
  no tunnel processes, conductor unset
- Backup (OD-09): plaintext SQLite snapshots via
  `omniroute-backup.timer` (daily 03:17 UTC, `Persistent=true`) →
  `omniroute-backup.service` → `/opt/omniroute/ops/sqlite-snapshot.mjs`
  (better-sqlite3 online backup API → `integrity_check` hard gate →
  single-file artifacts → keep-latest-20). Restore proven at L1-M3 by booting
  a throwaway instance against a scratch DATA_DIR (gate record §G4). Backup
  encryption wrapper: owner-decided NOT REQUIRED 2026-08-28 (state log row 66)
- Gateway response cache (recorded behavior): the product's semantic cache
  serves byte-identical repeat requests without a new usage row — cache-bust
  (unique nonce) any verification call that must prove a genuine backend
  round-trip (gate record §G1)

### Services

| Service | Purpose | Enabled | Active |
| ------- | ------- | ------- | ------ |
| `omniroute.service` | OmniRoute v3.8.51 traffic plane, primary listener `192.168.50.207:20128` | yes | yes |
| `omniroute-loopback.service` | HX loopback listener `127.0.0.1:20128` → LAN primary (raw TCP proxy) | yes | yes |
| `omniroute-backup.timer` | Daily 03:17 UTC plaintext snapshot (integrity-gated, keep-20) | yes | yes |

## Validation

```text
[x] Base system healthy        — rick L1-M1 Node runtime PASS (01-rick-l1-node-runtime.md); rick hxs-8 readiness (04-rick-hxs8-readiness.md)
[x] Network healthy            — gate posture: LAN-only primary + loopback listener; no wildcard bind; no firewall per owner rule (05-trinity-l1-gate.md pre-gate + G6)
[x] Storage healthy            — ~420 GB free; DATA_DIR integrity_check ok at every gate step (05-trinity-l1-gate.md)
[x] Role-specific runtime healthy — install PASS incl. standalone build, OD-13 secrets verification, four-backend registration (03-trinity-l1-install.md)
[x] Required services active   — all three units enabled+active; auto-start across the L1-M3 cold reboot with no human action; NRestarts=0 (05-trinity-l1-gate.md G3)
[x] Assigned workload validated — L1-M3 gate: parity deep ×3 tasks ×3 reachable backends direct-vs-routed (G1), restart ×2 (G2), cold reboot (G3), restore-to-scratch drill (G4), rollback rehearsal (G5), hygiene close-out (G6) — 05-trinity-l1-gate.md
```

Open items (recorded, owner disposition required): the standing owner-lane
rotation of the management (dashboard) password also retires the plaintext
copies of the current value in the owner's interactive `~/.bash_history` on
hxs-8 (×21, owner session) and in four sudo journal lines written by the
gate's own login probes (executor-caused, recorded openly in
`05-trinity-l1-gate.md` §G6); registry divergences above are owner-side.

## Material Change Record

| Timestamp (UTC) | Previous State | Change | Files / Commands | Validation | Rollback | Unresolved Issues |
| --------------- | -------------- | ------ | ---------------- | ---------- | -------- | ----------------- |
| 2026-08-27T16:15Z–17:30Z | No OmniRoute; Node runtime only | L1-M2 install: corpus copy → npm ci/build → standalone deploy → systemd units + OD-13 secrets drop-in → posture rows → 4 backend registrations → HX client key → parity ×3 → backup design + drill | `03-trinity-l1-install.md` (hashes §3–§5, inverses §11) | Install gate evidence §10 (parity, health, restart intact) | Documented inverses for every change (§11) | Chat-X posture-blocked (approved exception); Coder-X candidate status |
| 2026-08-27T18:20Z–18:26Z | Install-time management password | Owner interactive password reset (`/tmp/omni-pw-reset.sh`, scripts since removed by the owner); drop-in content hash → `05638010…`; service restarted | sudo journal 18:20:54Z–18:26:07Z; state log row 48 (distinct dashboard password at next rotation) | Login functional with the reset credential; bcrypt at rest verified at the gate | Owner-lane; rotation decision stands | Plaintext copies in owner bash_history (×21) — retires with rotation |
| 2026-08-28T00:11Z | Drop-in 0640 | Governor hardening: chmod 0600 root:root, content unchanged | State log row 50 | 0600 verified at the gate | — | — |
| 2026-08-28T06:06Z–06:07Z | Primary listener `0.0.0.0:20128` | L1-M3 pre-gate rebind: `30-v3.8.51-bind.conf` (`OMNIROUTE_HOSTNAME=192.168.50.207`) + `omniroute-loopback.service` + `loopback-listener.mjs` (all hash-recorded) | `05-trinity-l1-gate.md` pre-gate section | Post-bind battery: no wildcard, non-LAN interfaces unexposed, authN/authZ intact, posture effective | Rehearsed in G5 (checkpoint rollback + forward, zero loss) | — |
| 2026-08-28T06:08Z–06:35Z | Installed state | L1-M3 gate executed: G1 parity deep, G2 restart ×2, G3 cold reboot, G4 restore drill, G5 rollback rehearsal, G6 hygiene | `05-trinity-l1-gate.md` (per-gate evidence) | All gate tests PASS (G6 with two recorded plaintext-residue exceptions for owner rotation) | G5 proof; G4 scratch restore proof | Owner-lane items above |

## Sources

- `servers/hxs-8/discovery.md` (as-found, 2026-08-12 + 2026-08-27 addendum; preserved)
- `pilots/PILOT-OMNIROUTE-LAYER0-001/`: `01-state-log.md` (rows 66–67 GO), `03-trinity-l1-install.md` (L1-M2 install record), `05-trinity-l1-gate.md` (L1-M3 gate record), `09-work-order-trinity-install.yaml`, `10-context-packet-trinity-install.yaml`, `11-work-order-trinity-gate.yaml`, `12-context-packet-trinity-gate.yaml`
- `goals/2026-08-27-omniroute-layer1-secure-core.md` (owner decisions OD-04/OD-07/OD-08/OD-09/OD-12/OD-13; gate items 1–7)
- `servers/BLUEPRINT-llm-server.md` (§5 exposure boundary; §8 backend call-signs)
- `servers/SERVER-REGISTRY.md` (assigned role; owner-maintained)
- `servers/hxs-3/configuration.md` (first-of-class template)
