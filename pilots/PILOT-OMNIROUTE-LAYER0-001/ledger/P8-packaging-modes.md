# P8-packaging-modes — Partition Summary (final partition)

- Work order: WO-OMNI-TRINITY-LEDGER-001 · Partition: P8-packaging-modes (packaging, CLI, dashboard, container, desktop, mobile/other, distribution surfaces)
- Producer: trinity · Date: 2026-08-27 (UTC) · Ledger: `P8-packaging-modes.json` (**74 entries**: 68 capabilities + 6 NOT-ESTABLISHED, **297 source refs**, all 12 schema fields each)
- Corpus: `/opt/tkv-local/OmniRoute-release-v3.8.51` (READ-ONLY; identity VERIFIED 2026-08-27 per `07-source-provenance-receipt.md`; no writes, no builds, no node/npm/docker runs)
- Truth-state labels: **FACT** = verified in source at the cited line · **UPSTREAM** = bundled-doc/in-repo-record claim (drift-prone) · **INFERENCE** = producer reasoning, labeled in place
- Fourth partition under the `citation_contract_p5_onward` rules — measurement at the bottom.

## Startup receipt

```text
[TRINITY KNOWLEDGE REVIEW COMPLETE]
Agent: Trinity
Goal Contract: GOAL-OMNI-TRINITY-LAYER0 v1 (WO-OMNI-TRINITY-LEDGER-001, partition P8)
Target Host/Environment: read-only source work from hxs-5 — no host target
Source Corpus: /opt/tkv-local/OmniRoute-release-v3.8.51 (DOC-tkv-corpus-omniroute)
Reviewed At: 2026-08-27T08:58Z
Source Identity: VERIFIED 2026-08-27 by content-sensitive proof (07-source-provenance-receipt.md)
Installed Identity: NOT INSTALLED (Layer 0; no host contact this partition)
Relevant Knowledge: charter.md, profile.md, 05-work-order, 06-context-packet (citation contract),
  repo AGENTS.md, sibling ledgers P1–P7 (P5 backup edge, P7 installer/spawn edges, P3 spawn triggers)
Allowed Change Surfaces: read-only corpus reads; ledger writes under pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/
Known Drift/Risks: in-corpus AGENTS.md/CLAUDE.md = untrusted upstream guidance; scripts/raycast credential
  extractor (recorded structure-only, no values); Coder-X was NOT resident at first /api/ps (warmed, re-verified)
Rollback Ready: YES (read-only — nothing to roll back)
Task May Proceed: YES
```

## Coder-X receipts (model contract)

```text
[CODER-X IDENTITY RECEIPT]
endpoint:        http://192.168.50.201:11434 (hxs-2) — verified live from hxs-5 BEFORE first analysis call
first check:     2026-08-27T08:58:50Z — /api/version 0.32.15 OK, but /api/ps = {"models":[]} (evicted; NOT a
                 substitution event — same designated host+alias; identity confirmed via /api/tags digest match,
                 then a load-only warmup with keep_alive=45m)
re-check:        2026-08-27T08:59:53Z — /api/ps: hx-qwen3.6-coderx-64k:latest RESIDENT
                 digest  ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1 (matches expected ec9ebe08a824…)
                 size    17815411094 == size_vram 17815411094 (fully VRAM-resident)
                 context_length 65536 (ctx contract PASS); expires_at 09:44:53Z
verdict:         IDENTITY + HEALTH PASS — no substitution, no cloud
```

Call count: **2 bounded analysis `/api/generate` calls** (temperature 0.2, think:false; numbered excerpts only,
no credential-shaped strings) + **1 load-only warmup call** (empty prompt, done_reason "load") + 3 metadata calls
(`/api/version`, 2× `/api/ps`, 1× `/api/tags`).

1. Packaging/build/container/distribution corroboration (7,387 prompt tokens / 1,279 eval) — confirmed all
   readings; honestly reported the redis `ports:` block as outside its chunk (my chunking gap, lines 69-89 not
   sent; already evidenced from my own read) — same lesson as P5: adjacent chunks should overlap.
2. CLI backup/cloud/encrypt + electron secrets + update + supervisor corroboration (6,399 / 1,622) — confirmed
   every assessment conclusion, including "cannot confirm the server endpoint exists" for /api/db-backups/cloud
   and "restore cannot restore an encrypted backup".

Coder-X outputs used as corroboration only; every ledger citation was drafted and verified deterministically by
the producer (refcheck + spotcheck below). Its path slips never entered the ledger.

## Packaging / build model (evidence)

- **Distribution unit** [FACT]: single npm package `omniroute@3.8.51` (MIT) with two bin entries
  (`omniroute`, `omniroute-reset-password`), files-allowlist packaging, npm workspaces (open-sse,
  packages/browser-pool), Node engines `>=22.22.2 <23 || >=24.0.0 <27` (package.json:2-63) — matches the
  context packet's verified-facts block.
- **Build model** [FACT]: `npm run build` → isolated `next build` (build-next-isolated.mjs:94,108) with
  `output: "standalone"` into `.build/next` (next.config.mjs:185,15); assembleStandalone.mjs is the declared
  single source of truth for the bundle's native/extra modules (:68,114,163); deterministic pure-Node tarballs
  (standaloneTarball.mjs:1,14); profiles `build:secure` (minimal) and `build:backend` (package.json:101-102);
  release chain stamps build SHA (package.json:105). The CLI tarball is a separate prepublish.ts chain with
  pack-artifact + pack-boot + install-upgrade gates (package.json:103,158-160,251). Every runtime mode
  (Docker runner, electron bundle, npm package) consumes the SAME standalone artifact — one build, many skins.
- **Install-time execution** [FACT]: postinstall native-binary fixup runs on every install
  (scripts/build/postinstall.mjs:121,138) — the supply-chain-sensitive moment; the Docker build mirrors the
  posture with `--ignore-scripts` + explicit rebuilds (Dockerfile:117-124).
- **Optional weight** [FACT]: optionalDependencies (better-sqlite3, keytar, sqlite-vec, tls-client-node,
  onnxruntime/SLM stack) + the #10321 checksummed runtime-packs system install heavy closures on first use
  into DATA_DIR/packs (optionalPackManifest.mjs:5-19, electron/main.js:133-156).

## CLI surface inventory (evidence)

- **Entry** [FACT]: bin/omniroute.mjs — fast-path `--version`, `--mcp` stdout-guard + bypass, tsx registration,
  four-file env chain with shadow warnings and the Electron server.env→.env migration (#7302),
  STORAGE_ENCRYPTION_KEY auto-provision with the existing-DB refusal guard (:222-228), update-notifier
  (suppressible), then Commander.
- **Command surface** [FACT]: ~80 hand-written register functions (registry.mjs:1-85) + a generated
  `omniroute api` tree of 31 OpenAPI tags (api-commands/registry.mjs:34; generator + build:cli-api gate).
  Lifecycle: serve (default, daemon, PID files) / stop / restart + ServerSupervisor (maxRestarts default 2,
  bounded resurrection). Clients: dashboard browser opener, ink TUI (`--tui`), tray, autostart.
  Data: backup/restore/sync/env. Integrations: 15 setup-* writers into third-party tool configs.
  Agent-adjacent commands (mcp/a2a/skills/memory/cloud/tunnel/plugin) are P7 surfaces; P8 ledgered only
  their CLI packaging mechanics with cross-references.
- **Self-update** [FACT]: `omniroute update` = `npm install -g omniroute@latest` with pre-update bin backup
  and post-update version re-read against PATH shadowing (update.mjs:185-215) — AVAILABLE-DISABLED for HX
  (owner-managed change control supersedes in-place self-update).

## CLI-backup assessment (the mandated P5 edge — closed)

1. **Plaintext default** [FACT]: `omniroute backup` copies storage.sqlite (online-backup API), settings.json,
   combos.json, providers.json into `<DATA_DIR>/backups/` unencrypted (backup.mjs:27-32,231) — a SECOND,
   less-governed plaintext artifact location alongside P5's server-side `<DATA_DIR>/db_backups`.
2. **--encrypt** [FACT]: real AES-256-GCM with scrypt passphrase KDF and salt+iv+tag+ciphertext format
   (:131-154); passphrase only via --key-file or interactive prompt — so the server's scheduled-backup job
   REFUSES encrypt:true schedules (no non-interactive passphrase source; backupScheduleJob.ts:82-88 — an
   honest fail-closed guard, not a silent gap).
3. **--cloud** [FACT]: uploads the backup dir to `${baseUrl}/api/db-backups/cloud` (:295) with API-key +
   CLI-token auth — **and that route does not exist in the pinned server source** (grep-verified: the only
   `db-backups/cloud` occurrence in the corpus is the client line). The flag dead-letters with a warning.
   This closes P5's CAP-P5-036: server-side cloud/encrypted remote backup is NOT-ESTABLISHED (CAP-P8-905).
4. **Restore gap** [FACT + labeled INFERENCE]: `createDecipheriv` is imported (:13) and never called; the
   restore loop matches only plaintext filenames (:453-459) — **`omniroute restore` silently restores nothing
   from an encrypted backup** while printing success. Encrypted CLI backups are write-only with the shipped
   CLI (CAP-P8-906). INFERENCE: unfinished feature, not deliberate refusal. Mitigation until fixed: plaintext
   backups + filesystem protection, or bin/snapshot-data.sh + server-side restore (P5's integrity-checked path).
5. **Schedule execution** [FACT]: the server job imports the CLI's runBackupCommand IN-PROCESS (no spawn) —
   P5's "cloud/encrypt execute in the CLI" confirmed and sharpened (backupScheduleJob.ts:12,69,100-110).

## Dashboard mode (evidence)

Next.js 16 (16.3.2) standalone app serving dashboard + management + traffic planes in one process; dev port
20128; compile-time basePath for reverse-proxy subpaths (next.config.mjs:116, Dockerfile:146-147); compile-time
embed policy (DASHBOARD_ALLOW_EMBED, default deny per in-source comment, Dockerfile:149-159); PWA mode
(public/sw.js:1-8 app-shell cache excluding /api/, src/app/manifest.ts:4-10 installable standalone) — the only
mobile-adjacent surface.

## Container model (evidence)

- **Five-stage Dockerfile** [FACT] on node:26-trixie-slim: base (OS CVE patches + npm-internal CVE overlay
  :43-57) → builder (lockfile enforced :94, `npm ci --ignore-scripts` :117-118, explicit better-sqlite3
  node-gyp rebuild and fail-loud tls-client fetch :119-124, Turbopack default, MITM stub :164, memory/worker
  caps :177-200) → runner-base (non-root node:263, EXPOSE 20128, DATA_DIR=/app/data, HEALTHCHECK :269-270,
  CMD dev/run-standalone.mjs :272) → runner-web (+Chromium/Playwright :289-312) / runner-cli.
- **runner-cli is BLOCKED preliminary** [FACT + collision note]: it bakes @openai/codex, claude-code, droid,
  openclaw into the image (:337-338) and its compose profile bind-mounts the host docker.sock
  (docker-compose.yml:173) — the P7 agent-CLI class plus host-level Docker control; owner no-cloud rule and
  KK3 orchestration authority both collide.
- **Compose profiles** [FACT]: base/web/cli/host + opt-in sidecars (redis loopback-only-by-default :81,
  qdrant, bifrost, cliproxyapi, codex-app-server with capability-token volume :318). prod compose = isolated
  second instance on 20130 (LAB-ONLY; note its default target is runner-cli). Bun-runtime variant is LAB-ONLY.
- **Upstream image release** [FACT]: multi-arch base/web/bun pushes to Docker Hub + GHCR with advisory
  CycloneDX SBOM (docker-publish.yml:118-160,403-411); no image signing found (CAP-P8-902).

## Desktop mode (electron) (evidence)

Electron 43 shell embedding the same standalone server as a child process: ELECTRON_RUN_AS_NODE spawn with
HOSTNAME pinned to 127.0.0.1 (main.js:833-849 — loopback-only embedded posture, a positive for the LAN rule),
zero-config plaintext secrets bootstrap to `<DATA_DIR>/server.env` with the hasEncryptedCredentials refusal
(:750-793 — the desktop genesis of the secrets whose storage P5 flagged), remote-server attach mode,
single-instance lock, electron-builder targets win/mac/linux publishing to GitHub releases, electron-updater
with autoDownload=false. Two labeled findings: **no code-signing/notarization steps exist in
electron-release.yml** [INFERENCE from grep absence — unsigned auto-updatable artifacts upstream] and the
updater is therefore AVAILABLE-DISABLED for HX. P3's embedded-service spawn note: the desktop mode's only
child process is the server itself; the embedded-services supervisor/installers stay P7-class (LOCAL_ONLY,
not installed by default) in all packaging modes.

## Mobile / other modes (searched honestly)

- **Native mobile: NOT-ESTABLISHED** (CAP-P8-901) — no capacitor/react-native/tauri/cordova artifacts; PWA is
  the answer.
- **Other modes found**: fly.io PaaS config (fly.toml — NOT-APPLICABLE under the no-cloud rule), upstream VPS
  SSH deploy + self-hosted release runner (deploy-vps.yml, scripts/vps — NOT-APPLICABLE), contrib Podman
  quadlets + VPS compose (AVAILABLE-DISABLED), Raycast scripts including a **macOS Keychain credential
  extractor** (scripts/raycast/extract-credentials.mjs — LAB-ONLY, high-risk dev utility; recorded
  structure-only, zero secret values in any artifact), devin-bridge test containers (LAB-ONLY).
- **Distribution surfaces**: public/ = 239 static assets incl. served openapi.yaml (drift watch vs P1's route
  authority); .github = 35 upstream workflows incl. the Claude Code CI agent (agent-surface class, recorded
  NOT-APPLICABLE with collision note); Makefile = thin npm-script wrapper.

## NOT-ESTABLISHED items (searched, not found)

| ID | Searched for | Result |
| --- | --- | --- |
| CAP-P8-901 | native iOS/Android clients | none — PWA only (grep: capacitor/react-native/tauri/cordova) [INFERENCE from bounded negative search] |
| CAP-P8-902 | artifact signing (cosign/GPG/notarize) | none — SBOM + npm provenance exist, signing does not [INFERENCE from grep absence] |
| CAP-P8-903 | Kubernetes/Helm packaging | none — compose profiles + quadlets only [INFERENCE] |
| CAP-P8-904 | Homebrew formula in-repo | none — comment-level reference only (update.mjs:13) [INFERENCE] |
| CAP-P8-905 | server endpoint /api/db-backups/cloud | none — grep-verified absence; closes P5 CAP-P5-036 [FACT-grade absence] |
| CAP-P8-906 | CLI decrypt/restore path for .enc backups | none — createDecipheriv imported, never called (backup.mjs:13) [FACT mechanism + INFERENCE conclusion] |

## Sibling edges closed

- **P5 (CAP-P5-036)**: CLI backup/cloud/encryption assessed in full — five findings above; the schedule's
  cloud/encrypt booleans confirmed to execute via in-process import of the CLI implementation.
- **P7 (CAP-P7-042 mux installer, CAP-P7-049 cloud agents, CAP-P7-052 VNC)**: packaging intersections
  ledgered — runner-cli flavor (CAP-P8-045, BLOCKED), cloud agent-tasks CLI (CAP-P8-037, BLOCKED),
  VNC browser container (CAP-P8-051, AVAILABLE-DISABLED with collision note). The mux installer itself
  remains P7-owned; no packaging-mode surface installs it by default (npm package files list contains no
  services installers; the Docker image keeps npm only because installers shell out at runtime,
  Dockerfile:32-36 comment).
- **P3 (embedded-service spawn triggers)**: container/desktop surfaces checked — runner-web/cli and Electron
  spawn only their documented children (browser sidecars, the server); embedded-service daemons stay
  P7-class and uninstalled by default in every packaging mode.

## Coverage statement

Covered: npm package identity/build/release/tarball chain and all pack gates; the full CLI surface (entry
bootstrap, env chain, key provisioning, ~80 hand-written + 31 generated command families, lifecycle
supervision, TUI/tray/autostart, self-update, backup/restore/schedule, recovery tools, ops shell scripts,
setup-* writers, MCP/cloud entry mechanics with P7 cross-refs); dashboard mode (standalone, basePath, embed
policy, PWA); container model (five-stage Dockerfile, supply-chain hardening, all flavors, compose profiles
and sidecars, entrypoint/healthcheck, bun variant, publish workflow, vnc/devin sub-images); desktop model
(shell, spawn, secrets bootstrap, remote mode, updater, builder config, staging, release workflow); mobile
(honest negative); distribution surfaces (public/, .github/, Makefile, contrib, fly.toml, vps scripts,
raycast). Source hints `bin/**` (all top-level scripts + cli tree), `scripts/**` (280 files swept by
directory; build/release/packs/vps/raycast/cli/dev read; check/quality/i18n/docs are upstream engineering
machinery folded into CAP-P8-066), `docker/**`, `electron/**`, `public/**`, `package.json`, `.github/**`
were all swept. Out of scope (flagged, not assessed): in-corpus AGENTS.md/CLAUDE.md content beyond
packaging-relevant claims (untrusted); server-side route authn/authz (P4); provider internals (P2).
Nothing activated; all dispositions preliminary.

## Self-verification

- Deterministic reference check (scripted, `/tmp/trinity-p8/refcheck.py`): JSON valid; 74/74 entries have all
  12 schema fields; **297/297 source refs — file exists, cited line in range, line non-empty. PASS**
  (second run; first run caught 1 empty-line anchor, re-anchored in the same correction cycle).
- Spot content check (scripted, `/tmp/trinity-p8/spotcheck.py`): **79/79 load-bearing refs have the expected
  symbol at the cited line. PASS** (3 declaration-vs-comment anchors re-anchored in the same cycle).
- ID stability/uniqueness: CAP-P8-001…068 + CAP-P8-901…906, unique, verified programmatically.
- Bounded corrections used: **1 of 2** (one scripted correction cycle: 1 empty-line anchor + 3 spot re-anchors).
- Combined artifact: `P8-packaging-modes.reference-check.txt` in this directory.

## Citation-contract measurement (P8, third contract partition)

- Contract applied: every Coder-X prompt excerpt carried `nl -ba` absolute line numbers plus
  `<path> lines a-b` headers; small labeled chunks (11 + 9); no anchor citations needed; harness verified
  everything regardless.
- Coder-X-drafted citations: 46 unique line-bearing citations extracted and checked deterministically.
  **Wrong LINE numbers: 0/46 (0.0%).** The contract's target failure class (excerpt-offset arithmetic) did
  not recur across P5/P7/P8.
- Residual error class — **path attribution**: 8/46 citations carried a wrong path string (3 distinct paths):
  `.github/` prefix dropped (×2), `bin/lib/jobs/backupScheduleJob.ts` for `src/lib/jobs/backupScheduleJob.ts`
  (×2, incl. one garbled two-path citation whose LINE numbers 102-106 were correct for the intended file),
  `bin/electron/main.js` for `electron/main.js` (×4). All caught by the deterministic existence check
  (file-not-found-as-cited / content review); none entered the ledger. Skill-candidate note: the contract
  fixes lines; the remaining class needs a "copy the path from the chunk header verbatim" instruction or a
  path-existence post-check in the harness (mine caught all of them).
- Analysis-level divergences: none unresolved — Coder-X's two honest "outside the excerpt" reports (redis
  ports block, backup-dir path construction) were chunk-coverage gaps on my side, already evidenced from
  direct reads.
- **Baselines: P1 21/59 wrong lines (35.6%) → P5 1/25 (4.0%) → P7 1/32 (3.1%) → P8 0/46 (0.0%).**
  Contract holds; drafted-line error is now below measurable residual.

## Ten-line summary

1. Entries: 74 (68 capabilities + 6 NOT-ESTABLISHED), 297 refs, all 12 schema fields, IDs CAP-P8-001…068 + 901…906.
2. Packaging model: one npm package + one Next-16 standalone build feeds every mode (npm tarball, Docker image, electron bundle); isolated builder, files-allowlist, deterministic tarballs, pack-artifact/boot/install-upgrade gates, postinstall native fixup; optional weight via optionalDependencies + checksummed runtime packs.
3. CLI surface: bin/omniroute.mjs bootstrap (fast-path, env chain, key auto-provision with DB guard) + ~80 hand-written and 31 OpenAPI-generated command families; supervised serve/stop/restart; TUI/tray/autostart; npm self-update (AVAILABLE-DISABLED for HX).
4. CLI-backup finding (P5 edge): plaintext backups by default into DATA_DIR/backups; --encrypt is real AES-256-GCM but the scheduler refuses encrypt:true (no non-interactive passphrase); --cloud POSTs to a server endpoint that DOES NOT EXIST (CAP-P8-905); restore cannot read .enc files — encrypted CLI backups are write-only (CAP-P8-906, high risk).
5. Desktop: Electron shell spawns the standalone server loopback-only (HOSTNAME 127.0.0.1), zero-config plaintext secrets to server.env; updater autoDownload=false; unsigned upstream artifacts [INFERENCE]; AVAILABLE-DISABLED updater.
6. Container: five-stage hardened Dockerfile (non-root, healthcheck, ignore-scripts + CVE overlay); compose profiles with loopback-pinned redis; runner-cli flavor BLOCKED (agent CLIs + host docker.sock); bun variant LAB-ONLY.
7. BLOCKED (2): runner-cli container flavor, cloud agent-tasks CLI. NOT-ESTABLISHED (6): native mobile, artifact signing, Helm/k8s, Homebrew formula, /api/db-backups/cloud endpoint, CLI .enc restore path.
8. Coder-X: identity/health PASS after warmup re-verification (digest ec9ebe08a824…, size==size_vram, ctx 65536); 2 analysis calls + 1 load warmup + metadata; corroboration only; all its path slips caught deterministically.
9. Self-verification: 297/297 refs PASS + 79/79 symbol spot-checks PASS (second scripted run); bounded corrections 1 of 2; corpus untouched; no git commit.
10. Citation-contract measurement: 0/46 Coder-X-drafted lines wrong (0.0%) vs P1 baseline 35.6%, P5 4.0%, P7 3.1%; residual class = path-attribution slips (8/46), harness-caught — recommend adding "copy path verbatim from chunk header" + path post-check to the skill candidate.

## Correction record — cross-reference identifiers (2026-08-27, review batch 22, labeled)

Four cross-references inside `P8-packaging-modes.json` pointed at the wrong CAP
IDs and are corrected here and in the JSON (the entry IDs themselves are
unchanged): (1) `CAP-P8-004`'s dependency `CAP-P8-006` → **`CAP-P8-005`** (the
CLI npm tarball prepublish, which is the dependency the release chain actually
uses); (2) the write-only-restore reference `CAP-P8-036` → **`CAP-P8-906`**
(the CLI decrypt/restore gap — 036 is `--mcp stdio` mechanics); (3) three
electron-standalone bundle/staging references `CAP-P8-063` → **`CAP-P8-059`**
(063 is the VPS deploy workflow); (4) the unsigned-artifact reference
`CAP-P8-064` → **`CAP-P8-060`** (064 is contrib Podman quadlets). JSON
re-validated after the edits (74 entries, 12 fields each). Recorded per the
ledger's labeled-correction mechanism; history is in the state log and the
catalog hash chain.
