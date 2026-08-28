# Gordon — Feature Coverage Ledger (Phase A: Gates 0–5)

- **Ledger state:** INITIALIZED 2026-08-28, pre-execution. Every row is
  source-referenced, disposition `NOT_RUN`, candidate identity `PENDING-INSTALL`.
  The §8.3 freeze happens at Gate 0 execution; this file updates per executed
  test with identity, evidence pointer, and disposition.
- **Candidate (review baseline, profile §3):** dsh `0.1.1-rc.2`, tag
  `dsh-v0.1.1-rc.2`, commit `b150a551b8d465e31e418e1b2eaf5e79bbb7d28e`; pinned
  source `/opt/tkv-local/deepseek-harness-master`; manifest SHA-256 verified at
  authoring against this tree (package.json `4adb…86d7`, pnpm-lock.yaml
  `6f20…013e` — match).
- **Last-tested candidate identity:** PENDING-INSTALL (frozen at G0-05/G0-07).
- **Dispositions (profile §7):** PASS · FAIL · BLOCKED · NOT_RUN ·
  NOT_APPLICABLE · NOT_IN_PINNED_VERSION · AVAILABLE_DISABLED ·
  EXPERIMENTAL_LAB_ONLY · DEFERRED_BY_POLICY.
- **Plan:** `pilots/PILOT-DSH-IMPL-001/02-gordon-phase-a-testplan.md` (test IDs,
  entry paths, oracles, evidence contracts). Scripts:
  `pilots/PILOT-DSH-IMPL-001/gordon/phase-a/`.
- **Count reconciliation (open, governor):** the plan text says "Families (23)"
  but names 20 family headings; "session (all 11)" vs 13 session packages in the
  tree. Every package is enumerated below, so coverage is exact under either
  count. Flagged as plan §10 Q1.

## How to read a row

`Family / package (source)` — gate(s) — planned test IDs — disposition —
evidence pointer — notes. Package paths are relative to
`/opt/tkv-local/deepseek-harness-master`. "Mounted" facts come from the shipped
bundle patches (`packages/bundle/base/cordis.patch.yml`,
`.../headless/cordis.patch.yml`, `.../web-app/cordis.patch.yml`).

---

### 1. boot — Gates 0, 2

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/boot/app-boot` | G0-04, G2-01..07, G2-13, G2-14 | NOT_RUN | pending | loadLayeredEnv, loadProfile, PROFILE_TEMPLATES traced (src/index.ts, profile.ts) |
| `packages/boot/cmdline` | G2-08, G2-09 | NOT_RUN | pending | cmdlineArgs service; app --help contract |

### 2. core — Gates 2–5

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/core/agent` | G3/G4/G5 routed runs (agents.create per headless/src/index.ts:100-118) | NOT_RUN | pending | Agent creation proven by every headless run |
| `packages/core/agent-loop` | G4-03 (turn lifecycle), all routed runs | NOT_RUN | pending | `agents: []` default (base row); turn/start→turn/end |
| `packages/core/system-prompt` | G2-15 | NOT_RUN | pending | persona assembly; headless bundle persona oracle |
| `packages/core/tools` | G5-15 | NOT_RUN | pending | registry + presentation modes; DSH_TOOLS_MODE seam |
| `packages/core/scope` | transitive via G3/G4/G5 scoped events | NOT_RUN | pending | library primitive (src/index.ts:1-20); no direct mount |
| `packages/core/session` | G4-01..05, G4-08 | NOT_RUN | pending | SESSION_FORMAT_VERSION=0 (types.ts:56); event map (known-event-types.ts) |
| `packages/core/agent-default-model` | G3-04..06, G4-11 | NOT_RUN | pending | settings section live read (src/index.ts:26-46) |
| `packages/core/agent-tool-presentation` | G5-15 | NOT_RUN | pending | presentation in request/header tools |

### 3. util — Gates 1, 2 (transitive 3–5)

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/util/home-paths` | G2-14 | NOT_RUN | pending | resolveDshHome precedence (src/index.ts:87-91) |
| `packages/util/launch-environment` | G4-15 | NOT_RUN | pending | trusted env layers feeding baseURL resolution |
| `packages/util/atomic-write` | G1-05 (unit tier) | NOT_RUN | pending | library; transitive via persistence writes |
| `packages/util/brand` | G1-05 | NOT_RUN | pending | branded ids; library |
| `packages/util/native-command` | G1-05 | NOT_RUN | pending | library |
| `packages/util/output-retention` | G4-13 | NOT_RUN | pending | tail-truncation + spill handoff |
| `packages/util/timeout` | G5-07, G3-03 | NOT_RUN | pending | MAX_TIMER_DELAY_MS bounds in schemas |

### 4. fs — Gate 5

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/fs/fs` + `fs-sandbox` | G5-02..06 | NOT_RUN | pending | sandboxed provider (base row `fs-sandbox`) |
| `packages/fs/fs-local` | census G2-03 | NOT_RUN | pending | not mounted in shipped headless composition (cli dep only); expect AVAILABLE_DISABLED evidence |
| `packages/fs/fs-observation-policy` | census G2-03 | NOT_RUN | pending | mounted (base row) |
| `packages/fs/tool-fs` | G5-02, G5-15 | NOT_RUN | pending | write tools under sandbox |
| `packages/fs/tool-fs-search` | G5-15 | NOT_RUN | pending | mounted with sampleOverCapGlobResults: false |
| `packages/fs/tool-str-replace-editor` | G5-15 | NOT_RUN | pending | mounted (maxOutputChars 16000) |

### 5. host — Gate 2 (behavior Phase B)

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/host/webserver` | G2-10, G5-10 | NOT_RUN | pending | loopback bind, port config (src/index.ts:58-62) |
| `packages/host/frontend-static` | G2-10 (GET /) | NOT_RUN | pending | serves built web UI |
| `packages/host/apiproxy` | census G4-14/G4-16 (web dump) | NOT_RUN | pending | web-app row; behavior Phase B |
| `packages/host/plugin-inventory` | census G4-16 | NOT_RUN | pending | web-app row; behavior Phase B |
| `packages/host/directory-picker*` | census G4-16 | NOT_RUN | pending | directory-picker-auto mounted on web; browse/native variants Phase B |

### 6. identity — Gate 4

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/identity/anonymous-user-id` | G4-10 | NOT_RUN | pending | `.anonymous-user-id` bare UUID, stable |

### 7. settings — Gates 3, 4

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/settings/settings` | G4-11 | NOT_RUN | pending | settingsNamespace + installSettingsSection mechanics |
| `packages/settings/settings-file` | G4-11, G4-15 (home layout) | NOT_RUN | pending | `$DSH_HOME/settings.yaml` (src/index.ts:51-56) |

### 8. context — Gate 4 (census; behavior Phase B for the rest)

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/context/agent-instructions` | G4-17 | NOT_RUN | pending | AGENTS.md injection, maxBytes 65536 (base row) |
| `packages/context/file-reference(-local)` | census G2-03 | NOT_RUN | pending | Phase B surfaces |
| `packages/context/session-reference` | census G2-03 | NOT_RUN | pending | cli dep; Phase B |
| `packages/context/time-context` | census G2-03 | NOT_RUN | pending | cli dep; not in base/headless bundle rows; expect AVAILABLE_DISABLED evidence |
| `packages/context/tmux-context` | census G2-03 | NOT_RUN | pending | cli dep; terminal plane, Phase B |

### 9. compaction — Gates 3/4 census (live trigger deferred, plan §11 R2)

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/compaction/compaction` + `compaction-basic` | census G2-03 | NOT_RUN | pending | mounted (base row); live trigger NOT_RUN pending governor call on fixture-cost drill |
| `packages/compaction/compaction-tool-result-pruner` | census G2-03; G4-13 adjacent | NOT_RUN | pending | mounted (thresholdChars 8192) |
| `packages/compaction/command-compact` | census G2-03 | NOT_RUN | pending | `/compact` command; interactive surface Phase B |

### 10. llm — Gate 3

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/llm/llm` | all G3 | NOT_RUN | pending | service spine; LlmError codes; TokenUsage (types.ts:135) |
| `packages/llm/llm-deepseek` | G3-02, G3-03, G3-12 (+G3-04..06 when GORDON_SEAM=deepseek) | NOT_RUN | pending | route `deepseek-official`; baseURL/apiKeyEnv catalog config (src/index.ts:79-185) |
| `packages/llm/llm-pi-ai` | G3-01, G3-04F..06F (default fixture seam) | NOT_RUN | pending | hand-declared `openai-completions` routes (src/index.ts:30-52; provider.ts:48-50); mounted dormant |
| `packages/llm/llm-retry` | G3-09 | NOT_RUN | pending | durable `llm/retry` before wait (types.ts) |
| `packages/llm/token-meter` | G3-10 | NOT_RUN | pending | replay-aware measurement over the event stream |

### 11. session — Gate 4 (plan says "all 11"; the tree holds 13 — Q1)

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/session/session-persistence` | G4-01..06 (seam contract) | NOT_RUN | pending | persistence seam definitions + version refusal |
| `packages/session/session-persistence-jsonl` | G4-01..06, G5-08, G5-09 | NOT_RUN | pending | zstd default (index.ts:38); layout (format.ts:176-208); root 0700 |
| `packages/session/session-persistence-sqlite` | census G2-03 | NOT_RUN | pending | NOT mounted in shipped profiles at rc.2; expect AVAILABLE_DISABLED |
| `packages/session/session-projection` | census G2-03; G4-16 | NOT_RUN | pending | mounted (base row) |
| `packages/session/session-projection-cache` | G4-16 | NOT_RUN | pending | web-only mount (web-app rows 76-77) |
| `packages/session/session-checkpoint-policy` | G4-05, G5-09 | NOT_RUN | pending | mounted (base row) |
| `packages/session/session-stats` | G4-16 | NOT_RUN | pending | web-only mount (web-app rows 90-91) |
| `packages/session/session-telemetry` | G2-13, G4-09 | NOT_RUN | pending | seam definitions |
| `packages/session/session-telemetry-otel` | G2-13, G4-09 | NOT_RUN | pending | mounted, DISABLED default; AVAILABLE_DISABLED evidence planned |
| `packages/session/session-title` | G4-08 | NOT_RUN | pending | mounted (fallback bounds in base row) |
| `packages/session/session-title-llm` | G4-08 | NOT_RUN | pending | seam for LLM title strategies |
| `packages/session/session-title-first-prompt-llm` | G4-08 | NOT_RUN | pending | mounted; one extra provider call per session (G3-07 count) |
| `packages/session/session-title-all-prompts-llm` | census G2-03 | NOT_RUN | pending | NOT mounted in shipped profiles; expect AVAILABLE_DISABLED |

### 12. storage — Gate 4 census (behavior Phase B)

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/storage/storage` + `storage-domain` | G4-14 | NOT_RUN | pending | web-plane mounts |
| `packages/storage/storage-json` | G4-14 | NOT_RUN | pending | root `dshHomePath('storages')` |
| `packages/storage/storage-sqlite` | G4-14 | NOT_RUN | pending | unmounted at rc.2; expect AVAILABLE_DISABLED |

### 13. credentials — Gates 3, 4

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/credentials/credentials` | G3-02, G4-15 | NOT_RUN | pending | credentialRef seam; per-request resolution |
| `packages/credentials/credentials-local` | G4-15, G5-14 (no-leak) | NOT_RUN | pending | layering env > `$DSH_HOME/.credentials.yaml` > cwd/.env > home/.env (src/index.ts:2-17) |
| `packages/credentials/authorization` | census G2-03 | NOT_RUN | pending | OAuth-conversation seam (src/index.ts:1-12); no Phase A flow; behavior Phase B (pi-ai login) |

### 14. shell — Gate 5

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/shell/shell` | G5-01..07 | NOT_RUN | pending | request/spec split; DSH_ENV_PREFIX (`DSH_`) |
| `packages/shell/shell-env` | G5-14 | NOT_RUN | pending | managed DSH_* variables (src/index.ts:71-75) |
| `packages/shell/bash-sandbox` | G5-03..07 | NOT_RUN | pending | mounted (timeoutMs 60000); denial marker contract |
| `packages/shell/bash-local` | census G2-03 | NOT_RUN | pending | not mounted (sandboxed executor ships); expect AVAILABLE_DISABLED |
| `packages/shell/tool-bash` | G5-01..07, G5-13 | NOT_RUN | pending | schema + background + escalation pairing (src/index.ts:44-93) |
| `packages/shell/tool-bash-persistent` | census G2-03 | NOT_RUN | pending | cli dep; not in base rows; Phase B |
| `packages/shell/pwsh-local`, `pwsh-sandbox`, `tool-pwsh`, `tool-pwsh-persistent` | G5-16 | NOT_RUN | pending | Windows-only family; target disposition NOT_APPLICABLE (Linux) with G5-16/G5-15 evidence |

### 15. subprocess — Gate 5

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/subprocess/subprocess` | G5-01, G5-13 | NOT_RUN | pending | seam; DSH_ENV_PREFIX definition (types.ts:13) |
| `packages/subprocess/subprocess-local` | G5-01, G5-13 | NOT_RUN | pending | detached process trees (src/index.ts:1-9); proven via bash runs |

### 16. interaction — Gate 5

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/interaction/permission-presets` | G5-03..06 | NOT_RUN | pending | read-only/workspace-write/danger-full-access; DSH_PERMISSION_MODE |
| `packages/interaction/user-approval` | G5-05, G5-06 | NOT_RUN | pending | ask/never; fail-closed without answerer (src/index.ts:85-102) |
| `packages/interaction/commands` | census G2-03 | NOT_RUN | pending | slash-command registry; interactive use Phase B |
| `packages/interaction/user-questions` | census G2-03 | NOT_RUN | pending | mounted (base row); interactive surface Phase B |
| `packages/interaction/tool-ask-user` | census G2-03 | NOT_RUN | pending | cli dep; interactive surface Phase B |

### 17. attachment — Gate 4 census (behavior Phase B)

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/attachment/attachment` | G4-12 | NOT_RUN | pending | seam definitions |
| `packages/attachment/attachment-local` | G4-12 | NOT_RUN | pending | root `$DSH_HOME/attachments/v1` (src/index.ts:160); no headless attach entry |

### 18. spill — Gate 4

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/spill/spill` | G4-13 | NOT_RUN | pending | SpillLocator/SpillStore seam |
| `packages/spill/spill-local` | G4-13 | NOT_RUN | pending | private 0700 root default (src/index.ts:24-43) |
| `packages/spill/spill-policy` | G4-13 | NOT_RUN | pending | maxInlineBytes 50000 (base row) |

### 19. runtime-diagnostics — Gate 1

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `packages/runtime-diagnostics/invariants` | G1-05, G1-07 (verify-package-invariants within repo gates) | NOT_RUN | pending | registry service; static gate coverage via repo hygiene |

### 20. apps/cli — Gates 0–5

| Package (source) | Planned tests | Disposition | Evidence | Notes |
| --- | --- | --- | --- | --- |
| `apps/cli` | G0-04, G1-08, all G2, all signal drills | NOT_RUN | pending | bin dispatch (src/bin.ts), args (src/args.ts), profile boot (src/profile-boot.ts), plugin forwarder (src/plugin.ts), dump (src/dump-config.ts) |

---

## Cross-cutting rows

| Row | Planned tests | Disposition | Notes |
| --- | --- | --- | --- |
| Repo real-API e2e tier (`pnpm run test:e2e`) | G1-09 | DEFERRED_BY_POLICY (planned) | DeepSeek-cloud keys barred by local-only doctrine; HX e2e runs through OmniRoute in Gate 3 |
| Corrupted-current-session resume | G4-06(b) | BLOCKED-by-design (planned) | no headless resume entry in the pinned CLI; reassigned Phase B Gate 7 |
| usage_history routed evidence | G3-07, G3-08 | BLOCKED-by-design risk (R1) | governor-mediated snapshots; Trinity plane |
| Live compaction trigger | census only | NOT_RUN (planned) | fixture-cost drill deferred to governor decision (R2) |
| Telemetry reporting | G2-13, G4-09 | AVAILABLE_DISABLED target | DISABLED default + kill switch proven; reporting itself never enabled in qualification |
| pwsh family (4 packages) | G5-16 | NOT_APPLICABLE target (Windows-only) | evidence: platform-gated rows + Linux tool census |

## Ledger maintenance rules (profile §4, §9)

1. A row moves from NOT_RUN only with an executed test ID, candidate identity,
   environment identity, oracle source, and artifact pointer.
2. Every non-PASS disposition carries a named reason and owner.
3. Flakes are appended to the row's evidence, never deleted.
4. The ledger closes Phase A only when every row has a disposition with
   traceable record, every required test is PASS, zero P0/P1 defects are open,
   and the governor has signed the evidence pack.
