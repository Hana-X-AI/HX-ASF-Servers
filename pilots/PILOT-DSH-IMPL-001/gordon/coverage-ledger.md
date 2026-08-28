# Gordon — Feature Coverage Ledger (Phase A: Gates 0–5)

- **Ledger state:** EXECUTED 2026-08-28 (campaign 10:39Z freeze → 13:55Z close
  on hxs-15). Every row carries source reference, disposition, test IDs, and
  evidence pointer (`gordon/evidence/`, 236 records; per-gate JUnit XML).
  Verdicts document: `pilots/PILOT-DSH-IMPL-001/04-gordon-phase-a-verdicts.md`.
- **Last-tested candidate identity (frozen per §8.3, 2026-08-28T10:39:17Z):**
  dsh 0.1.1-rc.2; shim `/usr/local/bin/dsh` `0b68259f…efcdba`; built bin
  `/opt/dsh/apps/cli/lib/bin.js` `c0226687…366c62`; home layer
  `/var/lib/dsh/cordis.patch.yml` `14f15b72…03f6016`; package.json
  `4adbdffa…4986d7`; pnpm-lock.yaml `6f20c268…90013e`; dump `dedda886…d518d34`;
  Node v24.20.0; pnpm 11.7.0; `dsh` uid 999. All receipt identities MATCH at
  freeze; G0-07 fingerprint on file.
- **Defect register:** D1 (P2, sandbox backend absent), D2 (P3, gitless export
  vs git-requiring gates), D3 (P3, symlink-flattened export) — details and
  retest plan in the verdicts document.
- **Dispositions (profile §7):** PASS · FAIL · BLOCKED · NOT_RUN ·
  NOT_APPLICABLE · NOT_IN_PINNED_VERSION · AVAILABLE_DISABLED ·
  EXPERIMENTAL_LAB_ONLY · DEFERRED_BY_POLICY.
- **Count reconciliation (closed):** governor ruled 2026-08-28 — this ledger's
  package-level enumeration is authoritative; the plan's family grouping was
  indicative.

---

### 1. boot — Gates 0, 2

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/boot/app-boot` | G0-04, G2-01..07, G2-13, G2-14 | **PASS** | layered env, profile load/init all exercised and verified |
| `packages/boot/cmdline` | G2-08, G2-09 | **PASS** | app-level cmdline parse + usage errors |

### 2. core — Gates 2–5

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/core/agent` | all routed runs (G3/G4/G5) | **PASS** | agents.create per headless driver, proven repeatedly |
| `packages/core/agent-loop` | G4-03 + all routed runs | **PASS** | turn lifecycle durable and contiguous |
| `packages/core/system-prompt` | G2-15 | **PASS** | persona in request/header with model/cwd substituted |
| `packages/core/tools` | G5-15, G5-17 | **PASS** | 25-tool census; cookbook defineTool contract holds |
| `packages/core/scope` | transitive (G3/G4/G5 scoped events) | **PASS** | library primitive; exercised through every scoped session |
| `packages/core/session` | G4-01..05, G4-08 | **PASS** | format version 0, header contract, seq contiguity |
| `packages/core/agent-default-model` | G3-04..06, G4-11 | **PASS** | settings-driven per-era selection verified in request headers |
| `packages/core/agent-tool-presentation` | G5-15, G5-17 | **PASS** | tool schemas in request/header satisfy the contract |

### 3. util — Gates 1, 2 (transitive 3–5)

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/util/home-paths` | G2-14 | **PASS** | DSH_HOME override isolation verified |
| `packages/util/launch-environment` | G4-15 | **PASS** | trusted env layers incl. $DSH_HOME/.env fallback |
| `packages/util/atomic-write` | G1-05 | **PASS** | unit tier |
| `packages/util/brand` | G1-05 | **PASS** | unit tier |
| `packages/util/native-command` | G1-05 | **PASS** | unit tier |
| `packages/util/output-retention` | G4-13 | **PASS (retest 2026-08-28T14:3xZ)** | spill file written + reported after the D1 fix (bwrap live) |
| `packages/util/timeout` | G5-07, G3-03 | **PASS** | bounded TRANSPORT (G3-03); executor timeout-kill verified in the D1 retest (G5-07) |

### 4. fs — Gate 5

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/fs/fs` + `fs-sandbox` | G5-02..06 | **PASS** | workspace-write allow/deny, read-only deny, danger-full-access all verified post-D1-fix |
| `packages/fs/fs-local` | census G2-03 | **AVAILABLE_DISABLED** | not mounted in the shipped headless composition |
| `packages/fs/fs-observation-policy` | census G2-03 | **PASS** (composition) | mounted; behavior rides the tool rows |
| `packages/fs/tool-fs` | G5-02, G5-15 | **PASS** | census + workspace write (byte-exact) both green |
| `packages/fs/tool-fs-search` | G5-15 | **PASS** (census) | present in the model-visible catalog |
| `packages/fs/tool-str-replace-editor` | G5-15, G5-17 | **PASS** (census) | `edit` + `str_replace_editor` in catalog, contract-valid |

### 5. host — Gate 2 (behavior Phase B)

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/host/webserver` | G2-10, G5-10 | **BLOCKED-by-design** | frontend dist deliberately absent in Phase A (receipt §5); bind+signal proof reassigned to Phase B Gate 7 |
| `packages/host/frontend-static` | G2-10 | **BLOCKED-by-design** | same boundary |
| `packages/host/apiproxy` | census G4-14/16 | **NOT_RUN (Phase B)** | web-plane; composition captured in web dump |
| `packages/host/plugin-inventory` | census G4-16 | **NOT_RUN (Phase B)** | web-app row |
| `packages/host/directory-picker*` | census G4-16 | **NOT_RUN (Phase B)** | directory-picker-auto mounts on web; browse/native Phase B |

### 6. identity — Gate 4

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/identity/anonymous-user-id` | G4-10 | **PASS** | created by its telemetry consumer, stable, UUID-shaped |

### 7. settings — Gates 3, 4

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/settings/settings` | G4-11 | **PASS** | namespace section read per Agent creation |
| `packages/settings/settings-file` | G4-11, G4-15 | **PASS** | `$DSH_HOME/settings.yaml` drives selection; home layout verified |

### 8. context — Gate 4 (rest Phase B)

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/context/agent-instructions` | G4-17 | **PASS** | workspace AGENTS.md reaches the model-visible stream |
| `packages/context/file-reference(-local)` | census G2-03 | **NOT_RUN (Phase B)** | surfaces land with Phase B |
| `packages/context/session-reference` | census G2-03 | **NOT_RUN (Phase B)** | as above |
| `packages/context/time-context` | census G2-03 | **AVAILABLE_DISABLED** | cli dep; not mounted in Phase A shipped profiles |
| `packages/context/tmux-context` | census G2-03 | **NOT_RUN (Phase B)** | terminal plane |

### 9. compaction — census (live trigger deferred, plan §11 R2)

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/compaction/compaction` + `compaction-basic` | census G2-03 | **NOT_RUN (behavior)** | mounted; live trigger needs the fixture-cost drill — governor decision pending (R2) |
| `packages/compaction/compaction-tool-result-pruner` | census G2-03 | **PASS** (composition) | mounted (thresholdChars 8192) |
| `packages/compaction/command-compact` | census G2-03 | **NOT_RUN (Phase B)** | interactive `/compact` surface |

### 10. llm — Gate 3

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/llm/llm` | all G3 | **PASS** | service spine, error codes, TokenUsage in stream |
| `packages/llm/llm-deepseek` | G3-02, G3-03, G3-12 | **PASS** | error contracts verified; row disabled in landed composition (AVAILABLE_DISABLED for the cloud route; no-cloud assert G3-12 green) |
| `packages/llm/llm-pi-ai` | G3-01, G3-04F..06F, G3-13 | **PASS** | native openai-completions seam; all three call signs routed; cookbook contract green |
| `packages/llm/llm-retry` | G3-09 | **PASS** | durable `llm/retry` before bounded final failure |
| `packages/llm/token-meter` | G3-10 | **PASS** | measurement derivable from the event stream |

### 11. session — Gate 4 (13 packages; governor-closed count)

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/session/session-persistence` | G4-01..06 | **PASS** | seam contract incl. version refusal path |
| `packages/session/session-persistence-jsonl` | G4-01..06, G5-08, G5-09 | **PASS** | layout, zstd frames, contiguous seq, torn-tail prefix, corrupt-sibling resilience |
| `packages/session/session-persistence-sqlite` | census G2-03 | **AVAILABLE_DISABLED** | not mounted in shipped profiles at rc.2 |
| `packages/session/session-projection` | census G2-03, G4-16 | **PASS** (composition) | mounted |
| `packages/session/session-projection-cache` | G4-16 | **AVAILABLE_DISABLED (headless)** | web-only mount |
| `packages/session/session-checkpoint-policy` | G4-05, G5-09 | **PASS** | killed log parses as committed prefix |
| `packages/session/session-stats` | G4-16 | **AVAILABLE_DISABLED (headless)** | web-only mount |
| `packages/session/session-telemetry` | G2-13, G4-09 | **PASS** | seam posture verified |
| `packages/session/session-telemetry-otel` | G2-13, G4-09 | **AVAILABLE_DISABLED** | DISABLED default + kill switch + bounded drain all proven |
| `packages/session/session-title` | G4-08 | **PASS** | title records in stream |
| `packages/session/session-title-llm` | G4-08 | **PASS** | LLM title request recorded; extra call counted |
| `packages/session/session-title-first-prompt-llm` | G4-08 | **PASS** | as above |
| `packages/session/session-title-all-prompts-llm` | census G2-03 | **AVAILABLE_DISABLED** | not mounted |

### 12. storage — Gate 4 census (behavior Phase B)

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/storage/storage` + `storage-domain` | G4-14 | **PASS** (composition) | web-plane mounts captured |
| `packages/storage/storage-json` | G4-14 | **PASS** (composition); behavior **NOT_RUN (Phase B)** | root `dshHomePath('storages')` |
| `packages/storage/storage-sqlite` | G4-14 | **AVAILABLE_DISABLED** | unmounted at rc.2 |

### 13. credentials — Gates 3, 4

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/credentials/credentials` | G3-02, G4-15 | **PASS** | per-request reference resolution; MISSING_CREDENTIAL contract |
| `packages/credentials/credentials-local` | G4-15, G5-14 (leak leg) | **PASS** | .env fallback verified; no credential value in the model-visible stream (G5-14 retest) |
| `packages/credentials/authorization` | census G2-03 | **NOT_RUN (Phase B)** | OAuth-conversation seam; pi-ai login flows are Phase B surface |

### 14. shell — Gate 5

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/shell/shell` | G5-01..07 | **PASS** | execution, workspace modes, timeout kill all green post-D1-fix |
| `packages/shell/shell-env` | G5-14 | **PASS (retest)** | managed DSH_* variables present; zero credential values in the model-visible stream |
| `packages/shell/bash-sandbox` | G5-03..07 | **PASS (retest)** | bwrap backend live: policy denials, timeout kill verified; fail-closed contract on record from the D1 window |
| `packages/shell/bash-local` | census G2-03 | **AVAILABLE_DISABLED** | unsandboxed alternative, not mounted |
| `packages/shell/tool-bash` | G5-01..07, G5-13 | **PASS (retest)** | echo execution, workspace write/escape, read-only denial, approval fail-closed (`unavailable` outcome), timeout kill, background jobs — all green post-D1-fix |
| `packages/shell/tool-bash-persistent` | census G2-03 | **NOT_RUN (Phase B)** | not in base rows |
| `packages/shell/pwsh-local`, `pwsh-sandbox`, `tool-pwsh`, `tool-pwsh-persistent` | G5-16, G5-15 | **NOT_APPLICABLE** | Windows-only; platform-gate expressions + zero pwsh tools on Linux, both verified |

### 15. subprocess — Gate 5

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/subprocess/subprocess` | G5-01, G5-13 | **PASS (retest)** | spawn + background process trees verified (G5-01, G5-13) |
| `packages/subprocess/subprocess-local` | G5-01, G5-13 | **PASS (retest)** | as above |

### 16. interaction — Gate 5

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/interaction/permission-presets` | G5-03..06 | **PASS (retest)** | workspace-write escape denied with the policy marker; read-only denies writes |
| `packages/interaction/user-approval` | G5-05, G5-06 | **PASS (retest)** | ask-with-no-answerer resolves `unavailable` (fail-closed, no write); `never` policy under danger mode verified |
| `packages/interaction/commands` | census G2-03 | **NOT_RUN (Phase B)** | interactive slash surface |
| `packages/interaction/user-questions` | census G2-03 | **NOT_RUN (Phase B)** | mounted; interactive surface |
| `packages/interaction/tool-ask-user` | census G2-03 | **NOT_RUN (Phase B)** | interactive surface |

### 17. attachment — Gate 4 census (behavior Phase B)

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/attachment/attachment` | G4-12 | **PASS** (composition) | seam mounted |
| `packages/attachment/attachment-local` | G4-12 | **PASS** (composition); behavior **NOT_RUN (Phase B)** | root `$DSH_HOME/attachments/v1`; no headless attach entry |

### 18. spill — Gate 4

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/spill/spill` | G4-13 | **PASS (retest)** | spillPath reported in the model-visible result; file holds the full output |
| `packages/spill/spill-local` | G4-13 | **PASS (retest)** | private spill root written (`/tmp/dsh-subprocess-*`) |
| `packages/spill/spill-policy` | G4-13 | **PASS (retest)** | oversized output spills per policy; tail retained in the result |

### 19. runtime-diagnostics — Gate 1

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `packages/runtime-diagnostics/invariants` | G1-05, G1-07 | **PASS** | 227 compiled companions pass plain-Node Loader checks (post-build retest) |

### 20. apps/cli — Gates 0–5

| Package (source) | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| `apps/cli` | G0-04, G1-08, all G2, signal drills | **PASS** | dispatch, args, profile boot, plugin forwarder, dump, bounded shutdown |

---

## Cross-cutting rows

| Row | Tests | Disposition | Notes |
| --- | --- | --- | --- |
| Cookbook: `adding-an-llm-adapter.md` | G3-13 | **PASS** | declared shapes, cordis-native secrets, usage-before-finish — all verified against the landed route |
| Cookbook: `adding-a-tool.md` | G5-17 | **PASS** | every census tool satisfies the minimal defineTool shape |
| Cookbook: `adding-a-package.md`, `packages/AGENTS.md` | G1-07 | **PASS** | conventions enforced by the hygiene gates |
| Cookbook: `adding-a-settings-card.md`, `adding-a-conversation-node.md`, `extension-cookbook.md` | — | **NOT_RUN (Phase B)** | web/client/extension surfaces |
| Cookbook: `adding-a-vendored-package.md` | G1 pointer | **PASS** (informational) | vendoring procedure; no runtime oracle; G1 hygiene covers the vendored set |
| Cookbook: `maintaining-dsh-code-review.md`, `responding-to-pr-review-on-a-stack.md` | — | **NOT_APPLICABLE** | contributor process docs, not candidate behavior |
| Repo real-API e2e tier | G1-09 | **DEFERRED_BY_POLICY** | DeepSeek-cloud keys barred; HX e2e ran via OmniRoute in Gate 3 |
| Corrupted-current-session resume | G4-06(b) | **BLOCKED-by-design** | Phase B Gate 7 |
| Web frontend dist | G2-10, G5-10 | **BLOCKED-by-design** | Phase B boundary (receipt §5) |
| usage_history routed evidence | G3-07, G3-08 | **PASS (closed 2026-08-28T14:20Z)** | windowed snapshot (474 attributed rows ≥ 128 register calls; per-model ✓; zero zero-token success rows; input median 7,712 matches dsh-side class) — arithmetic in `evidence/omni-usage/g307-g308-closure.json`; verdicts doc Appendix A |
| Live compaction trigger | census only | **NOT_RUN** | fixture-cost drill; governor decision (R2) |
| Telemetry reporting | G2-13, G4-09 | **AVAILABLE_DISABLED** | default-off + switch + bounded drain proven |
| Upstream advisory debt (38: 15H/20M/3L) | informational | recorded | receipt R1; governor risk register |

## Ledger close-out rule status

Every row above has source reference, owner, disposition, test IDs, evidence
pointer, and last-tested candidate identity. G3-07/G3-08 closed
2026-08-28T14:20Z (Appendix A). **D1/D3 retest 2026-08-28T14:3xZ (Appendix B):
all 9 D1-blocked rows PASS post-fix (bwrap 0.9.0 + AppArmor grant, fix record
§16), the acp agent-instructions snapshot row PASS (D3), and the G0-07 drift
close-out is DRIFT-CLEAN (reconstructed fingerprint == frozen; the only tree
delta is the two documented symlink paths).** Remaining dispositions are all
governor-approved classes: D2 (P3, governor-deferred to upstream intake),
by-design Phase B blocks, AVAILABLE_DISABLED / NOT_APPLICABLE /
DEFERRED_BY_POLICY / NOT_RUN-with-phase-pointer rows, and the R2 compaction
decision. Zero P0/P1 open. Flakes and harness/oracle corrections are recorded
openly in the verdicts document; no skip was silent and no non-pass was
converted.
