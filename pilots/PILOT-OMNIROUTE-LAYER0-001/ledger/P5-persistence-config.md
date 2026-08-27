# P5-persistence-config — Partition Summary

- Work order: WO-OMNI-TRINITY-LEDGER-001 · Partition: P5-persistence-config
- Producer: trinity · Date: 2026-08-27 (UTC) · Ledger: `P5-persistence-config.json` (37 entries, 155 source refs)
- Corpus: `/opt/tkv-local/OmniRoute-release-v3.8.51` (READ-ONLY; identity VERIFIED 2026-08-27 per `07-source-provenance-receipt.md`; no writes, no builds, no node/npm runs)
- Truth-state labels: **FACT** = verified in source at the cited line · **UPSTREAM** = bundled-doc/in-repo-record claim (drift-prone) · **INFERENCE** = producer reasoning, labeled in place
- First partition under the `citation_contract_p5_onward` rules (numbered excerpts, anchor-free small chunks, harness verification, before/after measurement) — measurement at the bottom.

## Startup receipt

```text
[TRINITY KNOWLEDGE REVIEW COMPLETE]
Agent: Trinity
Goal Contract: GOAL-OMNI-TRINITY-LAYER0 v1 (WO-OMNI-TRINITY-LEDGER-001, partition P5)
Target Host/Environment: read-only source work from hxs-5 — no host target
Source Corpus: /opt/tkv-local/OmniRoute-release-v3.8.51 (DOC-tkv-corpus-omniroute)
Reviewed At: 2026-08-27T07:30Z
Source Identity: VERIFIED 2026-08-27 by content-sensitive proof (07-source-provenance-receipt.md)
Installed Identity: NOT INSTALLED (Layer 0; no host contact this partition)
Relevant Knowledge: charter.md, profile.md, 05-work-order, 06-context-packet (citation contract), repo AGENTS.md, P1–P3 sibling ledgers (shape + edges)
Allowed Change Surfaces: read-only corpus reads; ledger writes under pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/
Known Drift/Risks: in-tree AGENTS.md/CLAUDE.md = untrusted upstream guidance (two drift instances caught this partition, below); secret-bearing modules reviewed without quoting any secret value (none present in source)
Rollback Ready: YES (read-only — nothing to roll back)
Task May Proceed: YES
```

## Coder-X receipts (model contract)

- Endpoint: `http://192.168.50.201:11434` (hxs-2) · alias `hx-qwen3.6-coderx-64k` — only alias used
- Identity/health verified BEFORE first call (2026-08-27T07:23Z): `/api/version` → `0.32.15`; `/api/ps` → model resident, digest `ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1` (matches expected `ec9ebe08a824…`), `size == size_vram == 17,815,411,094` (fully VRAM-resident), `context_length == 65536` — **PASS**
- Calls: **2** bounded analysis prompts (temperature 0; numbered source excerpts only, no credentials):
  1. Persistence/migrations/encryption/backup-restore check (7 labeled chunks) → confirmed WAL+per-file-transaction+pre-migration-backup+AES-256-GCM-passthrough readings; flagged one **wrong refutation** (claimed no pre-restore snapshot exists — refuted deterministically: `backup.ts:413-430` forces and awaits one; the lines sat in my chunk gap, noted as a chunking lesson) and one wrong line number (below)
  2. Config-precedence/feature-flag check (6 labeled chunks) → confirmed DB>env>default chain and both env-wins exceptions; no contradictions; flagged payload-rules three-tier drift risk and watch-degradation path (both already evidenced in entries)
- Coder-X outputs used as corroboration only; every cited file:line was re-verified deterministically by the producer (scripted existence check + symbol-at-line spot check + drafted-citation check)

## Persistence engine and migrations (evidence)

- **Engine** [FACT]: process-wide SQLite singleton (`core.ts:1031`) via better-sqlite3 with node:sqlite fallback (`:192`, `:205`); WAL journaling (`:1292`), busy_timeout 2000 ms (`:1298` — capped under the host watchdog), synchronous NORMAL (`:1299`). State root resolves from `DATA_DIR` env with writability fallback (`dataPaths.ts:64,107`); files pinned at `core.ts:103-107`.
- **Base schema** [FACT]: inline SCHEMA_SQL (`core.ts:238`) with **17 base tables** (grep-counted `CREATE TABLE` at :239–:495; the db/AGENTS.md "17 base tables" claim verified), re-exec'd every open plus idempotent column ensures (`:1302-1305`).
- **Migration runner** [FACT]: `runMigrations` (`migrationRunner.ts:931`) applies **160** versioned SQL files (grep-counted `src/lib/db/migrations/*.sql`, 001→163 with gaps) in per-file transactions (`:1096`), tracked in `_omniroute_migrations` (`:182`, `:1111`); status via `getMigrationStatus` (`:1186`). **Drift noted**: db/AGENTS.md claims "148 files → 153" [UPSTREAM — stale]; the same file's header comment says tracking table `schema_migrations` while the code uses `_omniroute_migrations` (in-file doc drift, migrationRunner.ts:5 vs :182).
- **Safety rails** [FACT]: renumber detection (`:942`), gap back-fill (`:970`), FTS5 deferral (`:981`), mass-migration abort with `OMNIROUTE_MAX_PENDING_MIGRATIONS` bypass (`:1009`, `:1059`, `:1077`), duplicate-column tolerance (`:1124`). Pre-migration backup gated on `DISABLE_SQLITE_AUTO_BACKUP` (`:1085-1086`, `createPreMigrationBackup` `:892`).
- **Restart behavior** [FACT]: every boot converges — auto-seed 001 (`core.ts:1310-1318`), runMigrations (`:1320`), re-apply stored pragmas + mmap (`:1325-1338`), schema_version stamp (`:1373`), startup health check with auto-repair and pre-repair backup (`:1376-1386`, skippable via `OMNIROUTE_SKIP_DB_HEALTHCHECK=1`), legacy-encryption migration (`:1393`), health/WAL schedulers (`:1399-1400`); orchestrated from `instrumentation-node.ts:74,514,564,729`. Old-schema/probe-failure recovery preserves or renames (`core.ts:1140-1204`, `:1347-1369`); legacy `db.json` auto-imports (`:1343`, `jsonMigration.ts:54`).

## Encryption at rest (evidence; P2 sibling edge assessed)

- **Mechanism** [FACT]: AES-256-GCM, 16-byte auth tag pinned against truncation forgery, format `enc:v1:<iv>:<ct>:<tag>` (`encryption.ts:30-41`, `:196-203`); scrypt key derivation with static salt `omniroute-field-encryption-v1` (`:41`, `:128`); legacy dynamic-salt values auto-migrate at startup (`:375`, `providers/migrations.ts:29`).
- **The P2-deferred edge — connection-row encryption status** [FACT]: fully wired (encrypt on insert `providers.ts:717` and update `:955`; decrypt on read `:360`) via `encryptConnectionFields`/`decryptConnectionFields` (`encryption.ts:296,313`) — **but conditional**: both are no-ops when `isEncryptionEnabled()` is false (`:297`, `:315`), and the module runs **plaintext passthrough with a warning when `STORAGE_ENCRYPTION_KEY` is unset** (`:185-190`, header `:7-8`). Key provisioning: env, then `<DATA_DIR>/.env`, `<cwd>/.env`, `~/.hermes/.env` (`:84-94`). **Assessment: CAP-P2-014's `provider_connections` credential rows are plaintext at rest by default; AES-256-GCM protection is operator-activated (AVAILABLE-DISABLED, CAP-P5-007/009). Key loss is unrecoverable by design (`:231-237`); the compensating wipe tool `recovery.ts:21` has no production call site (tests only — LAB-ONLY, CAP-P5-011).**
- **Drift caught** [FACT]: db/AGENTS.md calls `secrets.ts` a "dedicated encrypted store" — refuted: `persistSecret` stores plain JSON with no encryption call (`secrets.ts:19-28`); the bootstrapped `JWT_SECRET`/`API_KEY_SECRET` therefore sit plaintext in `storage.sqlite` regardless of the encryption key (`instrumentation-node.ts:111-137`). Flagged critical in CAP-P5-030.

## Backup / restore (evidence)

- **Backup** [FACT]: native SQLite online backup API (`backup.ts:294`) into `<DATA_DIR>/db_backups`, with cloud/build short-circuit, env + persisted-toggle disable gates (`:250`, `:254`), 4 KiB floor (`:258`), throttle (`:265`), and >50% shrink skip (`:282`). Retention: keep-latest 20, age unlimited by default (`backupRetention.ts:20-21`, prune `:104`).
- **Restore** [FACT]: id validated against traversal, candidate must pass `integrity_check` (`backup.ts:400`), **forced awaited pre-restore snapshot** (`:413-430` — the step Coder-X missed in the chunk gap), singleton + module state reset (`:433`, `:436`), WAL sidecar deletion to prevent stale-frame replay (`:448-457`), copy + reopen + row-count report (`:460-484`).
- **Management/API** [FACT]: `/api/db-backups` PUT/GET/POST/DELETE (`route.ts:44,65,84,163`), import with `OMNIROUTE_DB_IMPORT_MAX_MB` cap (`import/route.ts:32`), exportAll with credentials excluded and keys masked to 8 chars (`exportAll/route.ts:17`, `backup.ts:497-505`). Scheduled backups: `backup-schedule.json` cron evaluated by `backupScheduleJob.ts:69` (wired `instrumentation-node.ts:729`); the schedule's cloud/encrypt options execute in the CLI (`bin/cli/commands/backup.mjs` — P8 scope, unassessed).

## Configuration precedence and feature flags (evidence)

- **Flag chain** [FACT]: `DB override > process.env > definition.defaultValue` (`utils/featureFlags.ts:9-19`); overrides in key_value namespace `feature_flags` (`db/featureFlags.ts:13,41,52`), validated against the registry pre-write; security wrappers fail closed on store errors (`utils/featureFlags.ts:59-69,91-101`).
- **Exceptions** [FACT]: two flags resolve **env-wins-over-db** — `EXPOSE_CC_DISCOVERY_ALIASES` (`route.ts:72-75`) and `OMNIROUTE_CHAT_VIRTUAL_LANES` (`route.ts:79-82`, #9654 U7: DB override gates only at next boot; `admissionVirtualLanes.ts:23,42`). The API reports each gate's true source so the dashboard matches behavior.
- **Flag inventory** [FACT]: **52 defined flags** (deterministic count) — security 10, network 10, runtime 19, policies 5, cli 5, health 3; **7 require restart**: ENABLE_TLS_FINGERPRINT, MITM_DISABLE_TLS_VERIFY, ENABLE_CC_COMPATIBLE_PROVIDER, OMNIROUTE_DISABLE_BACKGROUND_SERVICES, OMNIROUTE_ENABLE_LIVE_WS, OMNIROUTE_CHAT_VIRTUAL_LANES, CLI_COMPAT_ALL (`featureFlagDefinitions.ts:14`; management API `route.ts:59,112`).
- **Other precedence chains** [FACT]: payload rules resolve **runtime in-memory override > DB-persisted > config/payloadRules.json file** (`payloadRules.ts:236-249`, file path overridable via `OMNIROUTE_PAYLOAD_RULES_PATH` `:134-139`); runtime settings hot-apply from the DB store via poll (5 s default, `OMNIROUTE_CONFIG_HOT_RELOAD_MS` `hotReload.ts:16`) + fs.watch (`:83`), degrading to poll-only on watch failure; persisted DB optimization pragmas re-apply at every boot (`core.ts:1325-1338`). Boot-time secrets resolve **env > persisted DB row > generate-and-persist** (`instrumentation-node.ts:111-137`).

## NOT-ESTABLISHED items (searched, not found)

1. **Down-migrations / automated migration rollback** (CAP-P5-034): runner is forward-only; rollback = restore the pre-migration snapshot (data-level inverse). Compensating control exists (CAP-P5-006).
2. **Point-in-time recovery / WAL archiving** (CAP-P5-035): whole-file snapshots only; scheduled WAL TRUNCATE actively discards frames; loss window = snapshot interval.
3. **Server-side cloud/encrypted remote backup** (CAP-P5-036): server writes plaintext local snapshots only; cloud/encrypt fields execute in the CLI (P8 scope — flagged for P8 follow-up, not assessed here).
4. **Multi-replica / shared-state HA** (CAP-P5-037): explicitly unsupported — the #3147 init log exists to diagnose split-state replicas (`core.ts:1401-1408`); single-replica state file is the supported posture.
5. **Runtime kill-switch for the migration runner or hot-reload loop**: no flag found for either (runner abort is tunable only via `OMNIROUTE_MAX_PENDING_MIGRATIONS=0`; hot-reload cadence only via `OMNIROUTE_CONFIG_HOT_RELOAD_MS`) [searched: flag registry + runner/reload modules; INFERENCE that none exists beyond what is cited].

## Sibling edges closed

- **From P2 (CAP-P2-014)**: connection-row encryption assessed above — wired but conditional, plaintext passthrough default; recorded in CAP-P5-007/009 with the dependency edge answered.
- **From P3 (CAP-P3-023)**: usage persistence (SQLite `usage_history`, same-second dedup, `usageHistory.ts:641`) stays owned by P3; P5 records only the facade cross-reference (CAP-P5-033, `usageDb.ts:18,21`) — no duplication.

## Coverage statement

Covered: persistence engine and path resolution, base schema and migration machinery (runner, rails, pre-migration backup), field-level encryption (mechanism, key provisioning, connection-row wiring, legacy migration, recovery tool), backup/restore/retention/scheduling and their APIs, startup/restart convergence (init sequence, health check auto-repair, old-schema and probe-failure recovery, db.json import, WAL/vacuum maintenance), settings/runtime-settings/database-settings stores with hot reload, the full feature-flag system (registry, precedence, exceptions, API), payload-rules precedence, and secrets bootstrap persistence. Source hints `src/**/db*`, `src/**/migrat*`, `src/**/backup*`, `src/**/config*`, `config/**`, `src/**/flag*` were swept; `config/` holds only payloadRules.json (ledgered), i18n assets, quality/release records (not configuration-precedence surfaces). The ~110 remaining `src/lib/db/*.ts` modules are domain-table CRUD modules (same engine, same patterns) — provider/model/combo/key domain rows belong to their owning partitions (P1/P2/P6/P7); `versionManager.ts` is CLI-tool version tracking (P8-adjacent, noted). Out of scope (flagged, not assessed): management-route authN/authZ (P4), CLI backup cloud/encrypt semantics (P8), MCP/agent-table domains (P7), quota/rate-limit tables' policy consumers (P6). Nothing activated; all dispositions preliminary.

## Self-verification

- Deterministic reference check (scripted, `/tmp/trinity-p5/refcheck.py`): 37/37 entries have all 12 schema fields; **155/155 source_refs — file exists and cited line in range. PASS.**
- Spot content check (scripted, `/tmp/trinity-p5/spotcheck.py`): **105/105 load-bearing refs have the expected symbol at the cited line. PASS** (first run flagged 9 refs off by 1-3 lines — docstring-vs-declaration anchors — all re-anchored and re-verified in the same scripted pass, pre-finalization).
- JSON validity: parsed clean. Bounded corrections used: 0 of 2 (the 9 re-anchors were caught by my own scripted pass before writing, same convention as P3).
- Combined artifact: `P5-persistence-config.reference-check.txt` in this directory.

## Citation-contract measurement (P5 = first contract partition)

- Contract applied: every Coder-X prompt excerpt carried `nl -ba`-style absolute line numbers plus `<path> lines a-b` headers; small labeled chunks (7 + 6); no anchor citations were needed (all regions were numberable); harness verified everything regardless.
- Coder-X-drafted line numbers: **1 wrong of 25 drafted citations (4.0%)** — `backup.ts:461` cited for the restore copy that actually sits at `:460` (blank line cited). Deterministic drafted-citation check: `/tmp/trinity-p5/coderx-drafted-check.py`, output in the reference-check artifact.
- **P1 baseline: 21/59 wrong (35.6%) → P5: 1/25 wrong (4.0%).** The contract removed the excerpt-offset arithmetic failure class; the residual error is a one-line-off boundary read.
- Analysis-level (not line-number) error also caught by the harness: Coder-X refuted the pre-restore snapshot because lines 413-430 fell between my two backup.ts chunks — chunk-boundary gap, corrected from source before writing (CAP-P5-014 cites `:426`). Lesson for the skill candidate: adjacent chunks should overlap by ~10 lines.

## Correction — truth-state labels on negative-search entries (2026-08-27, review batch 20, labeled)

The four NOT-ESTABLISHED entries CAP-P5-034…037 now carry the declared label
**(INFERENCE — bounded negative search; the search evidence is FACT)** in their
purpose text: the documented searches are verified facts; the absence
conclusions are producer reasoning and are now labeled as such. Conclusions
unchanged. **CAP-P5-009 stays FACT** — the finding's inclusion of it as
"producer reasoning" over-reached: `encryptConnectionFields` is called on every
write path (insert `providers.ts:717`, update `:955`, `_updateConnectionRow`
`:595`; migrations note `:54-58`), governor-verified by grep 2026-08-27 — the
wiring claim is source-verified, not inferred. The 12-field schema is unchanged
(labels live inside the purpose text, per the truth-state contract).
