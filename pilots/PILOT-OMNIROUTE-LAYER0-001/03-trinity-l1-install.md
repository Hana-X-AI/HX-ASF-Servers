# Trinity — L1-M2 Install Record: OmniRoute v3.8.51 on hxs-8 (native, OD-13 secrets, four backends)

| Field | Value |
| --- | --- |
| Work order | WO-L1-TRINITY-INSTALL-001 (`09-work-order-trinity-install.yaml` + `10-context-packet-trinity-install.yaml`) |
| Goal | GOAL-OMNIROUTE-L1-SECURE-CORE (`goals/2026-08-27-omniroute-layer1-secure-core.md`) |
| Agent | Trinity (OmniRoute lifecycle engineer), session trinity-l1-install-20260827-01 (1 of 2 budgeted) |
| Target | hxs-8 (192.168.50.207) — ONLY |
| Executor | hxs-5 (192.168.50.204) |
| Execution window | 2026-08-27T16:15Z – 17:30Z (all times UTC) |
| Result | **PASS — TASK COMPLETE** (install landed, all gate evidence collected; cold-reboot deferred to L1-M3, §10.4) |

Truth-state labels: FACT = live-verified this session (command + result in §14 or cited) · SOURCE = verified in the pinned corpus at the cited line (Layer-0 ledger) · AUTHORITY = owner/governance decision · INFERENCE = producer reasoning, labeled in place. No secret value appears anywhere in this record — secrets are referenced by name, mechanism, file mode, and sha256 only.

## 1. Startup receipt

```text
[TRINITY KNOWLEDGE REVIEW COMPLETE]
Agent: Trinity
Goal Contract: GOAL-OMNIROUTE-L1-SECURE-CORE v1 (WO-L1-TRINITY-INSTALL-001, milestone L1-M2)
Target Host/Environment: hxs-8 (192.168.50.207) — native systemd install; executor hxs-5
Source Corpus: /opt/tkv-local/OmniRoute-release-v3.8.51 (DOC-tkv-corpus-omniroute)
Reviewed At: 2026-08-27T16:15-16:39Z
Source Identity: VERIFIED 2026-08-27 by content-sensitive proof (07-source-provenance-receipt.md, row 6)
Installed Identity: NOT INSTALLED on hxs-8 (L1-M1 delivered Node v24.20.0 only — rick PASS)
Relevant Knowledge: 09-work-order + 10-context-packet; ledger P4/P5/P6/P7/P8; corpus AGENTS.md +
  Dockerfile + scripts/build/*; 01-rick-l1-node-runtime.md; 04-rick-hxs8-readiness.md;
  DOC-backend-qwen-x/coder-x/meta-x/chat-x; servers/hxs-8/discovery.md
Allowed Change Surfaces: hxs-8 only — /opt/omniroute tree, one system user, omniroute systemd unit +
  versioned drop-ins, backup timer; corpus READ-ONLY; no Docker/cloud/firewall/Layer-2+
Known Drift/Risks: cloudEnabled CODE-DEFAULT TRUE (must be set false explicitly); skills execution
  default-allow; OMNIROUTE_DISABLE_BACKGROUND_SERVICES also gates the in-process backup scheduler;
  npm-registry egress from hxs-8 (verified 16:39Z); better-sqlite3 native fixup after --ignore-scripts
Rollback Ready: YES — documented inverses for every change (§11)
Task May Proceed: YES
```

## 2. Authority, identity, pre-state

Owner authorizations exercised [AUTHORITY]: OD-12 (Layer 1), OD-04 (native systemd, never Docker), OD-08 amended (all four backends), OD-13 (secrets rule), OD-07 (LAN-only + OmniRoute authN/authZ + no host firewall), OD-09 (plaintext snapshots + own encryption). Local-model-only everywhere; zero `:cloud`.

Identity verified live 16:37Z against `servers/hxs-8/discovery.md` before any mutation [FACT]:

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| Hostname | hxs-8 | hxs-8 | MATCH |
| Peer | SSH from hxs-5 (192.168.50.204) to 192.168.50.207 | `$SSH_CONNECTION` peer 192.168.50.204, connected to .207 | MATCH |
| Machine ID | 91086d5265a74450b7c2047b3b7ca2ae | 91086d5265a74450b7c2047b3b7ca2ae | MATCH |
| Host key | pinned in hxs-5 `~/.ssh/known_hosts` (rick's ceremony vs owner console record) | `StrictHostKeyChecking=yes`, entry line 20 | MATCH |

Access mechanics: askpass helper READ the credential at execution time from the credential-record row of `/home/hxsa/opt/local-tkv/agent-zero-docs/keys.md/ssh-info.md` (`awk -F'|'` on the `SSH password` row, markdown backticks stripped — the first helper revision missed the backticks, one auth failure, corrected; smoke check `wc -c` = 10). Never printed/logged/stored; helper deleted at task end (§15). sudo on hxs-8: passwordless (preparation), used as `sudo -n`.

Pre-state [FACT]: Ubuntu 24.04.4, kernel 7.0.0-30; Node v24.20.0 + npm 11.19.0 at `/opt/node-v24.20.0` + `/usr/local/bin` symlinks (rick L1-M1, used as-is, no other Node installed); no `omniroute` user, no `/opt/omniroute`, ports 20128/20132 free, 436 GB free on `/`; gcc/g++/make ABSENT (relevant to §3.3); egress to registry.npmjs.org + github.com verified (200s).

## 3. Source and build evidence

### 3.1 Corpus hash-witness (READ-ONLY contract)

Method (recorded, used identically for all three witnesses): from the corpus root —
`find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum` (sorted per-file sha256 manifest, digest of the manifest).

| Witness | Time (UTC) | Files | Bytes | Manifest sha256 |
| --- | --- | --- | --- | --- |
| Corpus pre-state (hxs-5) | 2026-08-27T16:39:40Z | 13,098 | 222,322,233 | `f1d3b28346a576e761dcd56300400979a8fdf28b533ebab7d0720f5d65ffc956` |
| hxs-8 copy post-extract | 2026-08-27T16:41Z | 13,098 | 222,322,233 | `f1d3b283…ffc956` (identical) |
| Corpus post-state (hxs-5, task close) | 2026-08-27T17:26:26Z | 13,098 | 222,322,233 | `f1d3b283…ffc956` (identical) |

The corpus is byte-identical before and after [FACT]. Copy transport: `tar c -C /opt/tkv-local OmniRoute-release-v3.8.51 | ssh … 'sudo tar x -C /opt/omniroute/src --strip-components=1'`.

### 3.2 Dependency install

`npm ci --include=optional --no-audit --no-fund --legacy-peer-deps --ignore-scripts` as the `omniroute` user — the Dockerfile's exact invocation (Dockerfile:117-118) [FACT]: **added 2444 packages in 54 s, zero `npm error` lines** (log: `/opt/omniroute/build-logs/npm-ci.log` on hxs-8).

### 3.3 Native-binary fixup (CAP-P8-006), as actually resolved

- **better-sqlite3 13.0.3**: the GitHub-release prebuild path is CLOSED for Node 24 (`prebuild-install`: "No prebuilt binaries found (target=24.20.0 …)" — recorded), and hxs-8 has no C toolchain for the Dockerfile's `node-gyp rebuild` path (Dockerfile:73 installs `python3 make g++` in the image builder). **Resolution: better-sqlite3 13.0.3 ships prebuilt bindings inside the npm tarball** (`prebuilds/linux-x64.node` et al.); its loader selects them automatically (`lib/binding.js` `getPrebuildPath`). Smoke: in-memory open/create/close against the build tree → `SQLITE_SMOKE_OK` [FACT]. Anticipating the node-gyp path I had installed `make g++` via apt (17:0xZ); they turned out unnecessary and were **removed 17:26Z** — host package state restored (§11).
- **tls-client-node 0.2.0**: postinstall run explicitly per the Dockerfile posture; fetched `bin/tls-client-linux-ubuntu-amd64-1.15.1.so` [FACT]. (Serves only web-session providers — all out of HX scope; fetched anyway so the bundle is complete and the class fails loud, never silent.)

### 3.4 Standalone build (product's own contract)

`npm run build` → `scripts/build/build-next-isolated.mjs` → `next build --turbopack` (Next.js 16.3.2, `output: "standalone"` into `.build/next`, `OMNIROUTE_BUILDING=1`, heap 8 GB default) as the `omniroute` user [FACT]:

- `✓ Compiled successfully in 2.9min`; page-data + static generation 591/591 pages in 3.8 s; `Assembling standalone bundle (static + public + natives + extras)…` completed; TPROXY addon skipped (non-fatal, opt-in Linux capture mode — out of scope); zero build errors (the 24 `error`-pattern lines in the log are quoted source excerpts in type output, verified benign).
- Output: `.build/next/standalone/` 2.2 GB — `server.js`, `server-ws.mjs` (WS/peer-stamp wrapper), `dev/run-standalone.mjs`, `healthcheck.mjs`, `migrations/` (160 files — matches P5's source count), `node_modules/` incl. better-sqlite3 with `prebuilds/linux-x64.node`, docs, public, `.next`.
- Build log: `/opt/omniroute/build-logs/build.log` on hxs-8.

### 3.5 Deployment

`/opt/omniroute/src/.build/next/standalone/.` → `/opt/omniroute/app/` (root:root), plus the Dockerfile runner-stage parity copy of the complete `better-sqlite3` package from the build tree's `node_modules` (Dockerfile:246 rationale: guarantee the full package independent of trace behavior); `/opt/omniroute/app/.next/cache` created omniroute-owned (the unit's only writable app-dir path). Deployed-tree smoke: `APP_TREE_SQLITE_OK` [FACT].

Deployed key-file hashes [FACT]:

| File | sha256 |
| --- | --- |
| `/opt/omniroute/app/server.js` | `c786b39e26ba4089f20c46cc7da5b3e6253a0d7183d0a3f66c71d9abbb2ec103` |
| `/opt/omniroute/app/server-ws.mjs` | `87b2a6254b2df98311139fe25bd02e7481a604f6ed7a399d0e745671658f594f` |
| `…/node_modules/better-sqlite3/prebuilds/linux-x64.node` | `6fd4292c6c5f352436cd85c9e1cb286978efa43c20ae350973f83414ced9991d` |

Layout: `/opt/omniroute/{app}` root-owned (deployed bundle), `{src}` omniroute-owned (build tree, kept as L1-M3 evidence/cache — inverse in §11), `{data}` omniroute-owned 0750 (DATA_DIR), `{ops}` root-owned scripts, `{build-logs}`, `{home}` (service-account home/npm cache).

## 4. Service deployment (native systemd, versioned drop-ins)

System user `omniroute` (uid 999, nologin, home `/opt/omniroute/home`) created for the service [FACT]. Unit files, all root-owned, hashes verified identical on hxs-5 staging and hxs-8 [FACT]:

| File | Mode | sha256 |
| --- | --- | --- |
| `/etc/systemd/system/omniroute.service` | 0644 | `d6ab0a60c1aca89f3d014e176d3e01117070b1eb6414c17e706d7602145a83e0` |
| `/etc/systemd/system/omniroute.service.d/10-v3.8.51-runtime.conf` | 0644 | `a2f2012bf5aa34ffc03601a65d53e0c7142c951e0c3facbc182e55345d3389ad` |
| `/etc/systemd/system/omniroute.service.d/20-v3.8.51-secrets.conf` | **0640 root:root** | `73e99d16607f5b941f2c5b5f5f56be22de8abb71c44766cfd7997cf1a402d001` |
| `/etc/systemd/system/omniroute-backup.service` | 0644 | `068a2e0ba2725c77d6c5233e4772e615ead8d39a5ff9ec51a539f3dce3c789f7` |
| `/etc/systemd/system/omniroute-backup.timer` | 0644 | `c4415bba337d6b1b80143cfa8afdda4917e9a796502bfde3f4b987d68b399c47` |
| `/opt/omniroute/ops/db-set-posture.mjs` | 0755 | `ca7a69c0f3f838627db7c4e5fc5b3cbc7c9f91e2cfaff588934006ebeba7a440` |
| `/opt/omniroute/ops/sqlite-snapshot.mjs` | 0755 | `9190ea559feeb1314b5d8dfbfbf40935b449ac3228872cbe0aee2d7a45d29e5f` |

Unit shape (blueprint conventions): `Type=notify` with `NotifyAccess=all` + `WatchdogSec=60` — the product's own readiness/watchdog design (`standalone-server-ws.mjs` sends READY once the listener accepts, then arms watchdog keep-alive; the wrapper `run-standalone.mjs` supervises the server child, so READY arrives from the child PID — hence `all`, not `main`); `Restart=on-failure`, `RestartSec=5`, `TimeoutStartSec=180`; budgets `LimitNOFILE=65536`, `MemoryMax=8G`, `TasksMax=512`; hardening `NoNewPrivileges`, `ProtectSystem=strict` with `ReadWritePaths=/opt/omniroute/data /opt/omniroute/app/.next/cache`, `ProtectHome`, `PrivateTmp`. No `RemainAfterExit` anywhere. `ExecStart=/opt/node-v24.20.0/bin/node dev/run-standalone.mjs` from `WorkingDirectory=/opt/omniroute/app`.

Effective environment **by NAME** [FACT] (values of the four secret names live only in the 0640 drop-in and appear in no artifact): `NODE_ENV`, `DATA_DIR`, `HOSTNAME`, `PORT`, `OMNIROUTE_MIGRATIONS_DIR`, `OMNIROUTE_MEMORY_MB`, `OMNIROUTE_DISABLE_BACKGROUND_SERVICES`, `NEXT_TELEMETRY_DISABLED` (non-secret, `10-v3.8.51-runtime.conf`) + `JWT_SECRET`, `API_KEY_SECRET`, `STORAGE_ENCRYPTION_KEY`, `INITIAL_PASSWORD` (secret, `20-v3.8.51-secrets.conf`).

Non-secret values (recorded): `DATA_DIR=/opt/omniroute/data`, `HOSTNAME=0.0.0.0`, `PORT=20128`, `OMNIROUTE_MIGRATIONS_DIR=/opt/omniroute/app/migrations`, `OMNIROUTE_MEMORY_MB=4096`, `OMNIROUTE_DISABLE_BACKGROUND_SERVICES=true`, `NEXT_TELEMETRY_DISABLED=1`, `NODE_ENV=production`.

Bind decision [INFERENCE from FACT]: `HOSTNAME=0.0.0.0` on hxs-8 binds exactly eno1 (LAN 192.168.50.207) + loopback — the host has no other active interface (discovery §Network). That IS the OD-07 posture: LAN-only by topology, loopback preserved (the peer-stamp LOCAL_ONLY machinery and local healthcheck depend on loopback semantics), no host firewall (owner rule) — the LAN is the boundary. Verified post-start: single listener `0.0.0.0:20128` [FACT].

One transient-remediation cycle was used (budget 1): first start failed on (a) the env validator rejecting `OMNIROUTE_DISABLE_BACKGROUND_SERVICES=1` — the runtimeEnv schema accepts only `"true"|"false"` though the gate function itself accepts `1` too (source-noted product inconsistency; fixed to `true`); (b) `Type=notify` READY rejected (`NotifyAccess=main` vs the supervised child PID; fixed to `all`). Both fixes are in the hashed files above; journal evidence in §14.

## 5. OD-13 secrets verification (method only — no values anywhere)

Generation: on hxs-8, root, `openssl rand -hex 32` per key (64-char hex class) written directly into the 0640 drop-in by a script that never echoes; metadata-only check confirmed 4 names × 64 chars [FACT]. The values never entered an artifact, log, receipt, command echo, or model context.

Post-start verification, by METHOD [FACT]:

1. **No plaintext signing secrets in the DB** (the CAP-P4-039/CAP-P5-030 finding): `key_value` namespace `'secrets'` contains **0 rows** (`SELECT key FROM key_value WHERE namespace='secrets'` → empty). Boot journal contains NO `JWT_SECRET/API_KEY_SECRET auto-generated and persisted` or `restored from persistent store` lines — `ensureSecrets()` was a no-op because both were env-provisioned (instrumentation-node.ts:111-150 semantics).
2. **Connection-row credential fields are ciphertext**: a probe connection was registered with a dummy `apiKey` (a literal non-credential string), its DB row read back: `api_key` field = `enc:v1:`-prefixed AES-256-GCM ciphertext (format + length only, never the value) — the STORAGE_ENCRYPTION_KEY wiring is ACTIVE (CAP-P5-007/009). Probe connection then deleted via the API (200) and verified gone; exactly the four HX connections remain.
3. **Management credential**: `INITIAL_PASSWORD` env consumed at first boot — journal: `[AUTH] Migrated INITIAL_PASSWORD to bcrypt hash during startup`; settings row `password` holds a `$2`-prefixed bcrypt hash (format check only); `setupComplete=true`, `requireLogin=true` (headless path, settings.ts:280-287).

Credential artifacts on hxs-8 (existence + mechanism only): the 0640 drop-in (hash above); `/opt/omniroute/ops/.hx-client-key` 0600 root:root — the HX client-plane inference key created via `POST /api/keys` (key id `5a2aefa4-5ed0-4b4d-b293-a18eb6d571e0`, prefix `sk-cbea2…`, sha256 of the file `d8aa9c371b5ea6e0a5bfd18ed845a0e9bed3308e9387575bb502cb20b0b2431c`; retrieval mechanism: root read on hxs-8; value appears nowhere else). The transient management cookie jar was 0600 root, used only from loopback, destroyed at task end (§12.1 for the stateless-JWT nuance).

## 6. Management authN/authZ and exposure evidence

Management login from hxs-8 loopback: `POST /api/auth/login` 200 `{success:true}` with the env-provisioned credential (password passed via stdin, never argv) [FACT].

The P4 proxy.ts split, verified live [FACT]:

| Surface | Anonymous | Management (session cookie) |
| --- | --- | --- |
| `GET /api/settings` | **401** | 200, full object |
| `GET /api/providers` | 401 (LAN probe) | 200 |
| `GET /api/monitoring/health` | 200 with **exactly `{status, setupComplete}`** (2 keys — the GHSA-mvf8-qc78-5mxm split) | 200 with **25 keys** (full subsystem view) |
| `GET /api/settings` posture keys (management read) | — | `cloudEnabled:false, skillsEnabled:false, mcpEnabled:false, a2aEnabled:false, memoryEnabled:false, tailscaleEnabled:false, requireLogin:true, setupComplete:true` |

Exposure battery from hxs-5 over the LAN (192.168.50.207:20128) [FACT]: `/healthz` 200 `ok`; `/api/health` 200 `{status,timestamp}`; `/api/monitoring/health` anonymous 2-key view; `/api/settings`, `/api/providers`, `/api/services/9router/status`, `/api/mcp/stream`, `/api/plugins`, `/v1/models` — all **401** anonymous. LOCAL_ONLY semantics per P4 [SOURCE]: the loopback-or-private-LAN peer class passes locality and falls to the auth policy (hence 401 on-LAN); peers beyond the LAN would be refused unconditionally (403) — the LAN is the boundary (owner rule, no host firewall). Client plane: anonymous inference is OFF (`requireLogin=true` headless default); inference requires the HX client key (`/v1/models` 401 anonymous → 200 with `Authorization: Bearer`) [FACT].

## 7. Backend registration and identity evidence

Live identity verification from hxs-8 BEFORE registering (per backend record; Ollama 0.32.15 on all three) [FACT]:

| Backend | Endpoint | Model alias | Expected digest | Live evidence | Verdict |
| --- | --- | --- | --- | --- | --- |
| Qwen-X (hxs-1) | `http://192.168.50.200:11434` | `hx-qwen3.8-27b-64k` | `766cd9469fb4…` | `/api/ps`: resident, digest `766cd9469fb4`, size==size_vram 20,463,789,012, ctx 65536 | PASS |
| Coder-X (hxs-2) | `http://192.168.50.201:11434` | `hx-qwen3.6-coderx-64k` | `ec9ebe08a824…` | `/api/ps` empty (evicted) → identity via `/api/tags` digest MATCH → load-only warmup (`done_reason=load`) → `/api/ps`: resident, digest `ec9ebe08a824`, 17,815,411,094, ctx 65536 | PASS |
| Meta-X (hxs-3) | `http://192.168.50.202:11434` | `hx-muse-glimmer-64k` | `9dffb015db40…` | `/api/ps`: resident, digest `9dffb015db40`, 18,376,336,340, ctx 65536 | PASS |
| Chat-X (hxs-4) | `http://192.168.50.203:11434` | `hx-qwen3.5-9b-64k` | `5936a390c6c2…` | curl rc=7 (connection refused), http_code 000 — loopback-only posture CONFIRMED from hxs-8 | POSTURE-BLOCKED (not failed) |

Registration (`POST /api/providers`, management session, `provider:"ollama-local"`, no apiKey — LAN Ollama has no service-layer auth per the backend records; `providerSpecificData.baseUrl=<endpoint>/v1`) [FACT]:

| Connection id | Name | is_active | Product live-test | Notes |
| --- | --- | --- | --- | --- |
| `286edd71-db72-45be-a23d-1d21dd77976d` | Qwen-X (hxs-1) | 1 | test=active | ctx 65536 server-profile; NUM_PARALLEL=1 — consumers serialize (DOC-backend-qwen-x) |
| `1b602ba0-dcad-4ddd-ab85-ad4803d261b0` | Coder-X (hxs-2) | 1 | test=active | candidate status until hxs-2 M8 — usable per owner designation; vision PRESENT-but-DEFERRED, never relied on |
| `8e06d5f2-26a1-4cae-b7a9-93951d8a7064` | Meta-X (hxs-3) | 1 | test=active | LIMIT parallel_tool_calling:false (DOC-backend-meta-x) |
| `a6035f8d-0cd6-4877-a176-179bd7963958` | Chat-X (hxs-4) [loopback-only — posture-blocked] | **0** | unreachable | registered with posture recorded; excluded from routing; 0 models surfaced |

Routed model surface (`GET /v1/models` with the HX key) [FACT]: `ollama-local/hx-qwen3.8-27b-{32k,64k,128k}:latest`, `ollama-local/hx-qwen3.6-coderx{,-32k,-64k,-128k}:latest`, `ollama-local/hx-muse-glimmer{,-32k,-64k,-128k}:latest` (plus the `ollama/` alias prefix for the same set, 22 `hx-` entries total); **zero `hx-qwen3.5` entries** (Chat-X never synced — correct for posture). Model reference stays alias-only per the backend records.

## 8. Agent surfaces — verified disabled

Settings made explicit (the ledger's not-code-enforced finding): `skillsEnabled=false` written as a durable settings row (the executor is default-ALLOW without it, CAP-P7-018) and `OMNIROUTE_DISABLE_BACKGROUND_SERVICES=true` set in the unit env (jobs default-run, CAP-P7-045). Mechanism: the settings-API zod schema strips `cloudEnabled`/`skillsEnabled`/`memoryEnabled` (absent from `updateSettingsSchema` [SOURCE]), so the rows were written directly into `key_value` namespace `'settings'` by `/opt/omniroute/ops/db-set-posture.mjs` (hash above) replicating `updateSettings()` semantics with the service STOPPED, then verified through the product's own `GET /api/settings` after start (§6) [FACT]. Rows written: `cloudEnabled:false` (**the code default is TRUE** — settings.ts [SOURCE]; this is the O1-tripwire-critical explicit override), `skillsEnabled:false`, `mcpEnabled:false`, `a2aEnabled:false`, `memoryEnabled:false`, `tailscaleEnabled:false`.

Behavioral verification [FACT]:

| Surface | Evidence |
| --- | --- |
| MCP | `POST /api/mcp/stream` → **503** (`mcpEnabled=false` guard) |
| A2A | `POST /a2a` JSON-RPC → `{code:-32000, "A2A endpoint is disabled"}` |
| ACP | spawner unwired corpus-wide [SOURCE P7]; API LOCAL_ONLY [SOURCE P4] |
| Plugins | `GET /api/plugins` → `{"plugins":[]}` |
| Skills | `GET /api/skills` → empty registry; `skillsEnabled=false` durable row |
| Embedded services | `GET /api/services/9router/status` + `/mux/status` → `state:"not_installed"` (mux = the "local agent-orchestration daemon" — not installed) |
| Tunnels (cloudflared/tailscale/ngrok) | `tailscaleEnabled:false`; no tunnel binaries/processes on the host (`pgrep` sweep: none); all mutation endpoints LOCAL_ONLY [SOURCE P7]; BLOCKED class by the LAN rule |
| Conductor | `CONDUCTOR_HUB_URL` unset (0 conductor env vars) → null config [SOURCE P7] |
| Cloud agents | no credentials configured; `cloudEnabled:false` gates the sync call sites [SOURCE: isCloudEnabled, settings.ts:361] |
| Copilot/MITM/VNC/cli-tools | LOCAL_ONLY tiers [SOURCE P4/P7]; nothing installed or invoked |
| Background jobs | `OMNIROUTE_DISABLE_BACKGROUND_SERVICES=true`; boot-B journal shows NONE of the gated jobs (quota refresh, provider-limits sync, cloud-sync bootstrap, batch processor, embedded-services bootstrap, models.dev sync, backup schedule job, WS daemon) started — the kill switch is effective [FACT] |

**O1 tripwire (`:cloud`) sweep** [FACT]: `connection_providers = ["ollama-local"]` only; `cloud_tagged_connections=0`; zero cloud-tagged models; no cloud agent/env configuration anywhere. First-boot note (honest record): before the posture rows existed, boot A logged `[STARTUP] Synced migrated Codex connection defaults to cloud` — cosmetic: `syncToCloud()` early-returns when `NEXT_PUBLIC_CLOUD_URL` is unset (cloudSync.ts:89-91 [SOURCE]), zero egress occurred, and boot B (posture applied) is clean of the line [FACT].

## 9. Backup design (OD-09) and drill

Design [FACT as deployed; rationale INFERENCE labeled]: plaintext SQLite snapshots on a schedule to the managed dir `/opt/omniroute/data/backups` (0750, omniroute), retention keep-latest-20 (the product default, backupRetention.ts:20-21). Mechanism: `omniroute-backup.timer` (daily 03:17 UTC, `Persistent=true`) → `omniroute-backup.service` (oneshot, `User=omniroute`, same hardening shape) → `/opt/omniroute/ops/sqlite-snapshot.mjs`: better-sqlite3 online backup API (same class as the product's `backup.ts:294` [SOURCE]) → `integrity_check` on the snapshot (hard gate, exit 1 on failure) → `journal_mode=DELETE` so each artifact is one self-contained file → prune to 20.

Why not the product's own scheduler: the in-process backup-schedule job lives inside the `OMNIROUTE_DISABLE_BACKGROUND_SERVICES`-gated boot block (instrumentation-node.ts:588 [SOURCE]) — honoring the background-jobs finding (§8) disables it as collateral. The schedule therefore moved to a versioned systemd timer (the native HX shape), using the same online-backup mechanism and the product's default retention. `backup-schedule.json` confirmed ABSENT (in-process scheduler never armed) [FACT]. The product's `--cloud` flag and backup encryption are treated as nonexistent per OD-09 (CAP-P8-905 dead endpoint; CAP-P8-906 write-only) — never invoked.

Drill [FACT]: two oneshot runs — `SNAPSHOT_OK … bytes=2068480 kept=1`, then `kept=2`; both integrity-checked; sidecar cleanup verified; timer `enabled`, next fire 2026-08-28T03:17Z. Restore inverse (documented, drill deferred to L1-M3 per the context packet): stop `omniroute.service` → copy the chosen snapshot over `/opt/omniroute/data/storage.sqlite` (remove `-wal/-shm` sidecars) → start → verify `/api/health/ping` + connection list.

## 10. L1-gate evidence section

### 10.1 Direct-vs-routed parity (gate item 3)

Known-answer task per reachable backend, identical parameters both ways: `POST /v1/chat/completions`, model = operating 64k alias, `messages=[{user: "Compute 6*7. Reply with only the number, nothing else."}]`, `max_tokens=2048`, `temperature=0`; direct = backend's own `:11434`, routed = `127.0.0.1:20128` with the HX client key, model id `ollama-local/<alias>:latest`. Strictly sequential (Qwen-X serializes admission) [FACT]:

| Backend | Direct (shape/finish/content/usage pt/ct/tt) | Routed | Verdict |
| --- | --- | --- | --- |
| Qwen-X | chat.completion · stop · `42` · 99/32/131 | chat.completion · stop · `42` · 99/32/131 | PARITY PASS (identical) |
| Coder-X | chat.completion · stop · `42` · 25/134/159 | chat.completion · stop · `42` · 25/134/159 | PARITY PASS (identical) |
| Meta-X | chat.completion · stop · `42` · 71/75/146 | chat.completion · stop · `42` · 71/75/146 | PARITY PASS (identical) |
| Chat-X | — | — | POSTURE-BLOCKED (loopback-only; not a failure) |

Usage accounting visible in the ledger's own evidence path [FACT]: `usage_history` holds exactly the 3 routed calls, one per backend model, with token/latency columns and api-key attribution (`tokens_input`, `tokens_output`, `latency_ms`, `ttft_ms`, `api_key_id`).

### 10.2 Health surface (gate item 4)

Layered health verified [FACT]: `/healthz` 200 `ok` (ready-phase liveness), `/api/health` 200 minimal `{status,timestamp}`, `/api/health/ping` 200 with `latencyMs` (DB live), `/api/monitoring/health` anonymous 2-key vs management 25-key split (§6) — the documented public-vs-management layering holds over loopback AND LAN.

### 10.3 Service-restart routing-intact (gate item 6, partial per this WO)

`systemctl restart omniroute.service` at ~17:21Z [FACT]: back `active` (READY accepted), `/healthz` 200 within 12 s; all four connections present with correct active flags; routed Qwen-X call post-restart → `42`/stop/131 (identical to pre-restart); posture rows still effective (`cloudEnabled:false, skillsEnabled:false, mcpEnabled:false, a2aEnabled:false`); no watchdog events, zero unexpected restarts in the journal since boot B. The second restart and the reboot cycle are L1-M3 scope (§10.4).

### 10.4 Cold-reboot cycle — disposition: belongs to L1-M3

Choice: **defer to the L1-M3 gate work order** [AUTHORITY + INFERENCE]. The context packet assigns "cold reboot" to L1-M3 explicitly (with restart ×2, backup+restore drill, rollback drill, configuration.md, owner sign-off). It is not "trivially safe" here: a reboot mid-session severs the executor's SSH evidence chain with the build tree and drill state in flight, and the reboot's value is proving the WHOLE gate posture (unit enabled + routing + secrets + backups) returns together — which is exactly the gate's acceptance test, best run once, witnessed, against the finished L1 state. What this WO establishes for it: the unit is `enabled` (`WantedBy=multi-user.target`, verified), boot-start ordering (`After=network-online.target`), and READY-gated startup semantics — the reboot proof itself lands in L1-M3.

## 11. Pre/post hashes and documented inverses

| Change | Pre-state | Post-state (evidence) | Exact inverse |
| --- | --- | --- | --- |
| Corpus READ-ONLY | manifest `f1d3b283…` 16:39:40Z | identical 17:26:26Z | none needed — never mutated |
| Corpus copy at `/opt/omniroute/src` | absent | 13,098 files, digest `f1d3b283…` (16:41Z) | `sudo rm -rf /opt/omniroute/src` |
| User `omniroute` (uid 999) | no such user | system user, nologin | `sudo userdel omniroute` |
| `/opt/omniroute` tree | absent | app 2.2G + src 13G + data + ops + build-logs | `sudo systemctl disable --now omniroute.service omniroute-backup.timer && sudo rm -rf /opt/omniroute` |
| Unit + drop-ins | absent | hashes in §4 | `sudo rm /etc/systemd/system/omniroute.service /etc/systemd/system/omniroute-backup.{service,timer} && sudo rm -rf /etc/systemd/system/omniroute.service.d && sudo systemctl daemon-reload` |
| Secrets drop-in | absent | 0640 root:root, hash `73e99d16…` | covered by unit removal; rotation = regenerate in place + `systemctl restart omniroute` (invalidates all sessions/keys signed under the old secrets — documented behavior) |
| 4 backend connections | `provider_connections=0` | ids in §7 | `DELETE /api/providers/<id>` per id (management session), verified by list |
| HX client API key | none | id `5a2aefa4…` | `DELETE /api/keys/5a2aefa4-5ed0-4b4d-b293-a18eb6d571e0` + `sudo rm /opt/omniroute/ops/.hx-client-key` |
| Posture settings rows | absent | 6 rows, verified via API | `DELETE FROM key_value WHERE namespace='settings' AND key IN ('cloudEnabled','skillsEnabled','mcpEnabled','a2aEnabled','memoryEnabled','tailscaleEnabled')` with service stopped (reverts to code defaults — note: cloudEnabled default TRUE) |
| `make` + `g++` apt install | absent (dpkg 0) | installed 17:0xZ, **removed 17:26Z** (dpkg 0) | already inverted; reinstall = `apt-get install -y --no-install-recommends make g++` if a future rebuild needs node-gyp |
| Backups | absent | 2 drill snapshots + timer | `sudo systemctl disable --now omniroute-backup.timer && sudo rm -rf /opt/omniroute/data/backups` |
| Store wipe (full rollback) | — | — | all of the above in order: unit stop+remove → backup timer remove → `/opt/omniroute` remove → `userdel omniroute` → backend unregistration is moot once the store is gone |

Rollback readiness: every inverse is a one-command-class operation against recorded hashes; no rollback was needed; nothing was rolled back. Node runtime (rick's layer) untouched — its inverse lives in `01-rick-l1-node-runtime.md` §7.

## 12. Observations, drift, residual risks

1. **Stateless management sessions** [FACT, product semantics]: `POST /api/auth/logout` only deletes the cookie client-side (logout/route.ts) — the HS256 session JWT (30 d) is not server-side invalidated (post-logout probe with the held cookie still returned 200). The executor's only copy (cookie jar, 0600 root) was destroyed; practical exposure closed. If a session ever must be killed server-side, rotate the management credential or JWT_SECRET (inverse documented §11). Recorded for the owner; no action taken.
2. **Chat-X `test_status` display inconsistency** [FACT]: the row reads `test_status='active'` while the endpoint is demonstrably unreachable (curl rc=7) and `is_active=0` excludes it from routing with zero models surfaced. Effective posture is correct; the display string is an upstream state-semantics quirk (last_tested froze at registration time). Recorded as SEV-4-class drift for the upstream watch list.
3. **First-boot cosmetic cloud log** [FACT]: boot A logged a `Synced … to cloud` line with zero egress (CLOUD_URL unset early-return; §8). Boot B clean. The `cloudEnabled` code-default-TRUE is the sharpest default found this session — the explicit row closes it; keep it in every future deployment template.
4. **Upstream cleanup bug** [FACT, non-fatal]: boot-time auto-cleanup logs `Error cleaning compression_run_telemetry: SqliteError: no such table` on a fresh DB, then completes (`0 deleted, 1 errors`). Upstream SEV-4; no HX action.
5. **Env-validator inconsistency** [SOURCE]: `isBackgroundServicesDisabled()` accepts `1/true/yes/on` but the runtimeEnv validator accepts only `true/false` — the failure is loud and boot-blocking (good); deployment uses `true` (recorded §4).
6. **Build tree retained**: `/opt/omniroute/src` (13 GB incl. `node_modules` + `.build`) kept as L1-M3 evidence/cache; removal documented §11. Disk: 420 GB free [FACT].
7. Residual risks for the owner: none high/critical. Coder-X remains candidate-status until hxs-2 M8 (owner-designated usable). Chat-X LAN posture is a parked blueprint-alignment item — its connection row activates cleanly if the posture changes (no re-registration needed; a product re-test/model sync will surface it).

## 13. Second Brain evaluation (per the work order)

1. Opportunity identified: **yes** — the first governed traffic plane + the first secrets-design deployment; the install record, OD-13 secrets pattern, and four backend registration records are catalog content at handoff.
2. Roadmap capability/pattern: capability registration through the Second Brain catalog — the DOC-backend-* records gained their first consumer-of-record (this gateway); the OD-13 env-provision + root-only-drop-in + method-only-verification pattern is the reference shape for every future service deployment; hxs-8's configuration.md (L1-M3 deliverable) becomes the second of its class.
3. Disposition: **implemented** — built into the deployment (hashed versioned units, posture rows, registration records); this document goes to Carol for catalog receipt; handoff stays OPEN until the receipt is cited in the pilot state log.
4. Evidence/reasoning: every later service deployment reuses this secrets-and-native-systemd shape (§4–§5, §11 inverses).

## 14. Sanitized sequential command log

All local commands as hxsa@hxs-5; remote as hxsa@hxs-8 over independent SSH sessions (pinned host key, `StrictHostKeyChecking=yes`); password via execution-time askpass only (never argv/history/logs); sudo `sudo -n` (passwordless from preparation); secrets generated on-host into a 0640 file, never echoed. No credential value appears in any command or output.

| Seq | Time (UTC) | Where | Command (sanitized) | Exit |
| ---: | --- | --- | --- | --- |
| 1 | 16:15–16:35 | hxs-5 | Read charter/profile/work order/context packet/goal/AGENTS.md chain; ledger P4–P8 summaries; rick's two L1 reports; discovery; four DOC-backend records; corpus build/packaging source (AGENTS.md, Dockerfile, build scripts, proxy/authz, settings, backup) | 0 |
| 2 | 16:36 | hxs-5 | Corpus layout survey (`du`, `ls`; 250 MB, no node_modules); ssh-info row-structure probes (field LENGTHS only); known_hosts pin check (entry present) | 0 |
| 3 | 16:37 | hxs-5 | Create askpass + ssh helpers (0700); smoke `wc -c` → 12 (backtick bug) → fix → 10 | 0 |
| 4 | 16:37 | hxs-5→hxs-8 | First ssh → `Permission denied` (helper bug from seq 3) | 255 |
| 5 | 16:37 | hxs-8 | Identity + pre-state probe (hostname/peer/machine-id MATCH; node/npm present; gcc/g++/make ABSENT; ports free; 436 GB free; sudo -n OK) | 0 |
| 6 | 16:38 | hxs-8 | Egress probes: registry.npmjs.org 200, github.com 200 | 0 |
| 7 | 16:39:40 | hxs-5 | Corpus pre-state witness (method §3.1) → `f1d3b283…` | 0 |
| 8 | 16:40 | hxs-8 | **MUTATION** `useradd omniroute`; mkdir `/opt/omniroute/{src,app,data/backups,home,build-logs}`; ownership/0750 | 0 |
| 9 | 16:41 | hxs-5→hxs-8 | tar-stream corpus → `/opt/omniroute/src`; chown omniroute; re-witness on hxs-8 → `f1d3b283…` MATCH | 0 |
| 10 | 16:42–16:43 | hxs-8 | **MUTATION** `npm ci --include=optional --no-audit --no-fund --legacy-peer-deps --ignore-scripts` (as omniroute, logged) → 2444 pkgs, 0 errors | 0 |
| 11 | 16:44 | hxs-8 | better-sqlite3 prebuild-install → "No prebuilt binaries found (node 24)" — path closed, recorded | 0 |
| 12 | 16:45 | hxs-8 | **MUTATION** `apt-get install -y --no-install-recommends make g++` (Dockerfile:73 contract; dpkg pre-state 0) | 0 |
| 13 | 16:46 | hxs-8 | Shipped-prebuild discovery (`prebuilds/linux-x64.node` in tarball); build-tree smoke `SQLITE_SMOKE_OK`; node-gyp path unnecessary | 0 |
| 14 | 16:47 | hxs-8 | tls-client-node postinstall → `tls-client-linux-ubuntu-amd64-1.15.1.so` | 0 |
| 15 | 16:48–16:53 | hxs-8 | **MUTATION** `npm run build` (as omniroute, logged) → compiled 2.9 min, 591/591 pages, standalone assembled 16:53:28Z | 0 |
| 16 | 16:55 | hxs-8 | Standalone verification (server.js/server-ws/run-standalone/migrations×160/prebuild present) | 0 |
| 17 | 16:56 | hxs-8 | **MUTATION** deploy standalone → `/opt/omniroute/app` + Dockerfile-parity better-sqlite3 copy + `.next/cache`; root-owned; `APP_TREE_SQLITE_OK`; key-file hashes | 0 |
| 18 | 16:58 | hxs-8 | **MUTATION** install unit + `10-runtime.conf`; generate `20-secrets.conf` on-host (`openssl rand -hex 32` ×4, 0640, metadata-only check, hash recorded) | 0 |
| 19 | 16:59 | hxs-8 | Push ops scripts + backup units; `daemon-reload`; hash-verify all staged files | 0 |
| 20 | 17:00–17:02 | hxs-8 | First start FAIL (env validator: `=1` → `Invalid option`; NotifyAccess=main READY rejected) → fix drop-in (`=true`) + unit (`NotifyAccess=all`), re-hash, `reset-failed`, start | 1→0 |
| 21 | 17:02:36 | hxs-8 | Service `active`; listener `0.0.0.0:20128`; `/healthz` `/api/health` `/api/health/ping` 200; `/api/monitoring/health` anon 2-key | 0 |
| 22 | 17:03 | hxs-8 | Boot journal review (env-provisioned secrets: no persist lines; INITIAL_PASSWORD→bcrypt; DB driver better-sqlite3; DATA_DIR anchored) | 0 |
| 23 | 17:04 | hxs-8 | DB method-check (as omniroute, readonly): secrets namespace 0 rows; settings keys; bcrypt format; 160 migrations; 0 connections | 0 |
| 24 | 17:06–17:08 | hxs-8 | **MUTATION** stop → `db-set-posture.mjs` (6 rows written) → start (boot B); boot-B journal clean (no cloud line, no env error) | 0 |
| 25 | 17:09 | hxs-8 | Management login (password via stdin; first attempt 401 — my field-extraction bug, fixed `$2`→`$3`, no product issue) → 200 | 0 |
| 26 | 17:09 | hxs-8 | Settings as management: posture rows effective; anon settings 401; monitoring mgmt 25-key vs anon 2 | 0 |
| 27 | 17:10 | hxs-8 | Backend identity from hxs-8: Qwen-X PASS, Meta-X PASS, Coder-X (evicted→tags digest→warmup→ps) PASS, Chat-X rc=7 posture confirmed | 0 |
| 28 | 17:10–17:12 | hxs-8 | **MUTATION** register 4 backends (POST /api/providers); product live-test active ×3, Chat-X unreachable | 0 |
| 29 | 17:12 | hxs-8 | Encryption probe: dummy-key connection → DB `api_key` = `enc:v1:` ciphertext (format only) → DELETE → verified gone | 0 |
| 30 | 17:13 | hxs-8 | **MUTATION** create HX client API key (root-only file, id/prefix/hash recorded); `/v1/models` 401 anon → 200 with key; routed surface mapped (22 hx- entries, 0 qwen3.5) | 0 |
| 31 | 17:14–17:19 | hxs-8 | Parity battery: Qwen-X/Coder-X/Meta-X direct vs routed — identical shape/content/usage ×3; usage_history 3 rows; `:cloud` sweep 0 | 0 |
| 32 | 17:15–17:17 | hxs-8 | Agent-surface probes: MCP 503; A2A −32000; plugins []; skills []; services not_installed; tunnels off + no processes; conductor unset | 0 |
| 33 | 17:17 | hxs-5 | LAN exposure battery vs 192.168.50.207 (public 200s; management/LOCAL_ONLY/client-plane 401 anonymous) | 0 |
| 34 | 17:21 | hxs-8 | **MUTATION** `systemctl restart omniroute` — restart-intact: active, healthz 200, 4 connections, routed Qwen-X 42/stop/131, posture effective | 0 |
| 35 | 17:22 | hxs-8 | Chat-X row audit: is_active=0, test_status quirk recorded; 0 hx-qwen3.5 models | 0 |
| 36 | 17:23–17:24 | hxs-8 | Backup drill: no backup-schedule.json; oneshot ×2 SNAPSHOT_OK (integrity-gated, single-file, kept=2); timer enabled (next 2026-08-28T03:17Z); script v2 (sidecar fold) re-hashed | 0 |
| 37 | 17:25 | hxs-8 | Journal hygiene: 0 watchdog/kill/OOM events (2 grep hits = "headroom" false positives); env-by-NAME capture | 0 |
| 38 | 17:26 | hxs-8 | **MUTATION (inverse)** `apt-get remove -y make g++` — host package state restored (dpkg 0) | 0 |
| 39 | 17:26:26 | hxs-5 | Corpus post-state witness → `f1d3b283…` byte-identical | 0 |
| 40 | 17:27 | hxs-8 | Logout (200; stateless-JWT nuance recorded §12.1); cookie jar destroyed; final sweep (service active+enabled, timer enabled, listener, 22 hx- models) | 0 |
| 41 | 17:28–17:3x | hxs-5 | Deliverable written; helper + staging cleanup; final verification | 0 |

## 15. Task May Proceed receipt / handoff

```text
[TRINITY TASK COMPLETE — L1-M2 INSTALL]
Agent: Trinity
Work Order: WO-L1-TRINITY-INSTALL-001 (GOAL-OMNIROUTE-L1-SECURE-CORE, milestone L1-M2)
Target: hxs-8 (192.168.50.207) — identity verified (hostname/peer/machine-id/host-key)
Source Corpus: /opt/tkv-local/OmniRoute-release-v3.8.51 — READ-ONLY honored;
  manifest f1d3b28346a576e761dcd56300400979a8fdf28b533ebab7d0720f5d65ffc956
  (13,098 files / 222,322,233 bytes) identical at 16:39:40Z and 17:26:26Z
Installed Identity: omniroute v3.8.51, Next.js 16.3.2 standalone, Node v24.20.0,
  /opt/omniroute/app (hashes §3.5), native systemd omniroute.service (enabled, Type=notify)
Secrets (OD-13): env-provisioned JWT_SECRET + API_KEY_SECRET + STORAGE_ENCRYPTION_KEY +
  INITIAL_PASSWORD (openssl rand -hex 32 class; 0640 root:root drop-in sha256 73e99d16…);
  VERIFIED BY METHOD: 0 plaintext rows in key_value 'secrets'; connection credential fields
  enc:v1 AES-256-GCM; management password bcrypt at rest; zero values in any artifact
Backends: 4 registered (Qwen-X/Coder-X/Meta-X active with live identity PASS; Chat-X
  posture-blocked, recorded); parity ×3 identical direct-vs-routed; usage accounting visible
Management/exposure: auth split proven (anon-limited vs management-full ×2 surfaces);
  LAN-only posture (0.0.0.0 on LAN+loopback topology, no firewall per owner rule);
  client plane requires the HX key (401 anonymous)
Agent surfaces: MCP/A2A/plugins/skills/services/tunnels/conductor/cloud agents verified
  disabled/absent; skillsEnabled=false + OMNIROUTE_DISABLE_BACKGROUND_SERVICES=true explicit;
  cloudEnabled=false explicit (code default TRUE); zero :cloud anywhere
Backup: plaintext snapshots, systemd timer daily 03:17 UTC, keep-latest-20, integrity-gated;
  2 drill snapshots PASS; product --cloud/--encrypt treated as nonexistent
Rollback Ready: YES — documented inverse for every change (§11); no rollback needed
Retry budget: transient 1 of 1 used (env-syntax + NotifyAccess remediation, one cycle)
Stop conditions hit: NONE (corpus intact; secrets verification PASS; no backend identity failure)
Recommended state: ACCEPT — handoff to Carol for catalog receipt (handoff OPEN until cited
  in the pilot state log); L1-M3 gate work order follows (parity ×4 deep, restart ×2,
  cold reboot §10.4, backup+restore drill, rollback drill, configuration.md, owner sign-off)
```

`PASS — TASK COMPLETE`
