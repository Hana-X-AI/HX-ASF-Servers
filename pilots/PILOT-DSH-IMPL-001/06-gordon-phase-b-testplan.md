# Gordon — Phase B Test Plan (Gates 6–7)

- **Status:** authored 2026-08-28, offline, PIPELINED with Morpheus's Phase B
  activation. Nothing below has executed; no row is a finding. Execution begins
  on the governor's release after Morpheus's Phase B handoff, with a fresh
  §8.3 freeze (his activation changes the composition and the frontend dist —
  the Phase A fingerprint does not carry forward).
- **Contract:** GOAL-DSH-IMPL-001 (`00-goal.md`), arc plan Phase B
  (`2026-08-28-dsh-full-implementation-plan.md`: 19 families, Gates 6–7),
  Phase A verdicts (`04-gordon-phase-a-verdicts.md`: candidate qualified,
  D1/D3 fixed, D2 deferred).
- **Carried rows:** G4-06(b) corrupted-current-session resume (entry evaluation
  here, G7-07); G2-10 + G5-10 web-dist contingencies (frontend built this
  phase, closure here, G7-01/G7-12).
- **Owner directive (standing):** cookbook is first-class test material.
  Phase B recipe conversions: `adding-a-tool` (G6-22), `adding-a-package`
  (G6-23), `adding-a-conversation-node` (G7-09), `adding-a-settings-card`
  (G7-08). `adding-an-llm-adapter` closed in Phase A (G3-13).
- **Baseline:** the Phase A green state — routed OmniRoute seam (route
  `omniroute`, three fleet models), working bwrap sandbox, frozen identities.
  Every routed probe keeps the unique-nonce discipline and the queue-transient
  retry policy from Phase A.

## 1. Phase B surface map (from the pinned source)

Gate 6 orchestration families and their shipped mounting at rc.2:

- **Mounted in the headless/base composition:** `plan-mode` (section config),
  `goal` + `goal-round-driver` + `command-goal` + `tool-goal`, `tool-todo`,
  `workflow` + `workflow-worker-thread` + `tool-workflow`, `tool-ralph`,
  `skill` + `skill-filesystem` + `tool-skill` (+`skill-badge` disabled),
  `jobs-local` + `tool-jobs`, `subagent` + `subagent-spawn-in-process` +
  `subagent-fork-in-process` + `tool-subagent`(+`-fork`) +
  `tool-subagent-control`(+`list-agents`) + `tool-subagent-report`,
  `repeat-tool-reminder` (thresholds 3/5/8), `tool-call-timeout-policy`,
  `code-runtime-worker-thread` (headless bundle), `command-feedback`
  (slash surface is interactive).
- **Not mounted in shipped profiles (fixture-patch or Morpheus activation):**
  `schedule` (durable reminders), `hooks-claude-code`/`hooks-codex` +
  `hook-protocol`, `mcp-client`, `lsp` + `lsp-stdio` + `tool-lsp`, `terminal` +
  `terminal-bash` + `tool-terminal`, `agent-presets` + `persona` (web-app row;
  launcher appends the shipped preset root when the row exists,
  `apps/cli/src/profile-boot.ts:159-167`), `message-feedback`.
- **Gate 7 surface (web-app bundle, ~84 rows):** `webserver`, `api-gateway`,
  `api-remotes`, `connection`, host/client runners, `modules`,
  `session-projection-cache`, `session-stats`, `storage-json`
  (`dshHomePath('storages')`), `directory-picker-auto`, `plugin-inventory`,
  `session-log-download`, `locale`, `message-feedback`, ~35 `ui-*` client
  modules (layout, sidebar, conversation, trajectory, settings×4,
  model-selection, permission, plan, goal, jobs, workflow-run, subagent,
  skill, tool, renderer, theme, workspace…), `web-runtime`. The web profile
  also mounts `agent-presets` and `code-runtime-worker-thread`.
- **SDK/ACP bins:** TS client `@deepseek-ai/dsh-sdk-client` spawns a stdio
  JSON-RPC runtime (`dsh-sdk-jsonrpc-server`); examples ship
  `dsh-sdk-jsonrpc-demo` and `acp-demo` compositions; Python SDK at
  `python/sdk` + `python/sdk-runtime`.
- **Repo web lanes (test tooling):** `pnpm run test:gui` (client component +
  host suites, no browser) and `DSH_SNAPSHOT=replay pnpm run test:web`
  (Playwright Chromium against the built frontend; keyless replay + real-host
  smokes self-skip without keys).

## 2. Execution model

Same discipline as Phase A: scratch `DSH_HOME` per test; fixture `--patch`
overlays for rows the shipped composition omits (schedule, mcp-client,
agent-presets, session-query search, hooks); the real home read-only except
product-own writes; model-cooperation rows get recorded attempts (3) with
queue-transient spacing; evidence per §13 with the de-patterning writer
(governor directive, 2026-08-28). Web tests boot the web profile on loopback
with OS-assigned ports in scratch homes; the frontend dist comes from
Morpheus's Phase B build (`build:web` — its absence is G2-10's recorded
BLOCKED-by-design and flips to FAIL if missing at release).

Environment contract: Phase A's, plus `GORDON_WEB_PORT_BASE=0` (OS-assigned),
`GORDON_MCP_FIXTURE` (default
`/opt/dsh/packages/mcp/mcp-client/tests/fixture-server.ts`),
`GORDON_CHROMIUM` (Playwright executable; installed as test tooling at
release), `GORDON_SDK_DEMO` (default
`/opt/dsh/packages/examples/sdk-jsonrpc-demo`).

## 3. Gate 6 — goals, orchestration mechanics, agent integrations

| Test ID | Entry path | Oracle source | Required evidence | Acceptable dispositions |
| --- | --- | --- | --- | --- |
| G6-01 | goal lifecycle: routed run instructed to `create_goal` with a known-answer title | `goal/src/index.ts` (event-sourced CAS domain); tool-goal census row | `goal/*` events durable; goal folds with the title; `get_goal` reads it back | PASS, FAIL, BLOCKED |
| G6-02 | goal round-driver continuation | `goal-round-driver/src/index.ts` + `renderGoalRoundPrompt` | a second turn carries the goal continuation section without a new user message; round identity (goalId, revision, round) in the log | PASS, FAIL, BLOCKED |
| G6-03 | plan mode: census + `exit_plan_mode` behavior | `plan/plan-mode/src/index.ts` (`plan/mode` event, `EXIT_PLAN_MODE`); base bundle section config | tool present in census; instructed plan-mode run: `exit_plan_mode` carries a plan payload; headless review channel outcome recorded (`unavailable` per user-approval semantics) with mutation refusal evidence | PASS, FAIL, BLOCKED |
| G6-04 | todo_write lifecycle | `todo/tool-todo` (base row `allowParallelInProgress: true`) | todo events/records in the log; a later turn reflects the same list | PASS, FAIL, BLOCKED |
| G6-05 | workflow run: instructed `tool-workflow` with a known-answer script | `workflow/workflow` seam; `workflow-worker-thread` config (vm timeout 5000 ms default, force-settle on overrun) | workflow lifecycle events; result matches the script's known answer; worker settles | PASS, FAIL, BLOCKED |
| G6-06 | skill catalog: fixture SKILL.md via `skill-filesystem` roots patch | `skill/skill` (registry, name regex), `skill/skill-filesystem` (roots config) | fixture skill appears in the model-visible skill surface; invocation metadata valid (`verify-skill-invocation-metadata` gate) | PASS, FAIL, BLOCKED |
| G6-07 | hooks bridge: fixture Claude Code hook (SessionStart echo) in a fixture workspace | `hooks/hooks-claude-code/src/index.ts` (SessionStart + prompt/tool pre/post + Stop + subagent start/stop; `updatedInput` logged-not-honored) | hook execution evidence in the session/log; decision mapping recorded | PASS, FAIL, BLOCKED (bridge config surface unset at author time) |
| G6-08 | repeat-tool-reminder at threshold 3 | `guard/repeat-tool-reminder` (thresholds [3,5,8], previewChars 500) | reminder injected after the third identical call; durable event/user-message | PASS, FAIL, BLOCKED (model-cooperation) |
| G6-09 | tool-call-timeout-policy | `guard/timeout-policy` (cooperative enforcement) | covered by G5-07 evidence + census | PASS (cross-ref G5-07) |
| G6-10 | jobs lifecycle: background start → `job_list` → `job_kill` | `jobs/jobs-local` (process-local registry; disposal cancels live work) | job id in list; kill settles the record; no orphan after teardown | PASS, FAIL, BLOCKED |
| G6-11 | schedule: fixture-mounted `schedule` row; instructed one-shot reminder (~5 s) | `schedule/schedule` (`schedule/change` events, SCHEDULE_CHANGE_VERSION, reminder framing) | schedule record durable; reminder delivered as a later turn within a bounded window | PASS, FAIL, BLOCKED (unmounted in shipped composition; fixture row) |
| G6-12 | subagent spawn delegation: instructed tiny child task | `subagent/subagent` (named-provider registry); base rows (spawn) | child session with `parentSession`, `origin: 'subagent'`, `delegationDepth: 1`; child result reaches the parent turn | PASS, FAIL, BLOCKED |
| G6-13 | subagent fork delegation | base rows (`tool-subagent-fork`, one-shot fork) | fork child session origin + inherited-history evidence (request prefix overlap) | PASS, FAIL, BLOCKED |
| G6-14 | subagent-control: `list_agents` + `send_message` on a continuable child | base rows (`tool-subagent-control`, continuable default) | child listed with catalog identity; followup delivered and answered | PASS, FAIL, BLOCKED |
| G6-15 | preset composition: fixture-mounted `agent-presets`; agent created with shipped preset | `preset/agent-presets` (standing mount per preset); `profile-boot.ts` shipped root append; `apps/cli/config/agent-presets/{minimal,standard,code}` | child session's persona/tools differ per preset vocabulary (known-answer: minimal vs standard persona section) | PASS, FAIL, BLOCKED |
| G6-16 | persona row behavior | `preset/persona` (scope-only row; global mount collides loud) | preset-scoped persona shadows the deployment persona in the child request header; global-mount collision error recorded from a fixture dump/boot | PASS, FAIL, BLOCKED |
| G6-17 | bundle layer precedence: profile patch over bundle row config | `boot/app-boot/src/profile.ts` (layer order); dump-config renderer | two-layer dump shows the profile layer winning the targeted row's config | PASS, FAIL |
| G6-18 | extensions (Cordis runtime): live recomposition on user-layer edit during a long-lived web boot | `apps/cli/src/profile-boot.ts` (`watchUserPatches`, HMR) | editing scratch profile `cordis.patch.yml` mid-boot recomposes (log/event evidence); no restart | PASS, FAIL, BLOCKED |
| G6-19 | mcp round-trip: fixture `mcp-client` row → stdio fixture server | `mcp/mcp-client/src/index.ts` (server-qualified names `mcp__<server>__<tool>`); `tests/fixture-server.ts` | `mcp__fixture__*` tool in census; one call round-trips with the fixture's known answer | PASS, FAIL, BLOCKED |
| G6-20 | tool-ralph bounded invocation | `workflow/tool-ralph` (subagentProvider spawn, maxRounds config) | ralph run starts structured-output children within the round cap; events recorded | PASS, FAIL, BLOCKED (model-cooperation heavy) |
| G6-21 | feedback composition census | `feedback/command-feedback` (log-only feedback event; eager unflushed ack) | composition row present; behavioral producer is the interactive slash surface → G7-17 (web) | PASS (composition), NOT_RUN (headless behavior) |
| G6-22 | cookbook `adding-a-tool`: duplicate-registration conflict fails loud | cookbook recipe + `packages/AGENTS.md` (registration discipline); tool registry duplicate error (commands registry precedent: "already registered") | fixture patch with a duplicate tool name → boot fails naming the conflict | PASS, FAIL |
| G6-23 | cookbook `adding-a-package`: invariant + skill-metadata gates | cookbook recipe; `scripts/verify-package-invariants.ts`, `verify-skill-invocation-metadata.ts` | both gates exit 0 in the refreshed scratch copy (build present) | PASS, FAIL, BLOCKED |

## 4. Gate 7 — web, API, SDK, ACP, telemetry, user experience

| Test ID | Entry path | Oracle source | Required evidence | Acceptable dispositions |
| --- | --- | --- | --- | --- |
| G7-01 | web boot with built dist: GET `/` on loopback | `apps/web/index.html`; `host/frontend-static`; web-app startup rows | 200 HTML app shell; **closes G2-10/G5-10 contingencies**; BLOCKED-by-design flips to FAIL if dist absent at release | PASS, FAIL |
| G7-02 | API gateway RPC over `/api` | `api/gateway` (Typert dispatch); `dsh-client-connection` envelope | a sessions-list RPC returns the smoke session; JSON-RPC envelope, 200 | PASS, FAIL, BLOCKED (envelope traced at exec) |
| G7-03 | web round-trip: create session, prompt, SSE reply | web-app `api-remotes` + connection SSE | assistant reply for a nonce task visible in the SSE stream; session durable on disk | PASS, FAIL, BLOCKED |
| G7-04 | trajectory data after a tool-call chat | `ui-trajectory` data layer; web layer = pure presentation (client AGENTS.md §red lines) | trajectory/session window data carries the tool-call events; replay recompute identical | PASS, FAIL, BLOCKED |
| G7-05 | session-query search: shipped default vs enabled | `session-query-sqlite` (`openAt: never|first-search|startup`; SESSION_QUERY_SEARCH_DISABLED under never) | default: search call fails with the named code; patched `first-search` + durable path: marker phrase found across sessions | PASS, FAIL, BLOCKED |
| G7-06 | session export/download | `session-log-export` (web `/export` command + download endpoint) | downloaded log bytes == the durable artifact bytes | PASS, FAIL, BLOCKED |
| G7-07 | **G4-06(b) closure attempt:** corrupted-current-session via the web read path | scanner prefix semantics (`format.ts:337-344`); `core/session/src/repair.ts` | torn-tail session opens with committed prefix; corrupt-middle behavior recorded as found; if no web read entry tolerates it, carried with the rationale recorded | PASS, FAIL, BLOCKED (carried) |
| G7-08 | cookbook `adding-a-settings-card`: Models settings card read + fenced write | cookbook recipe (settingsNamespace, `role('secret')`, revision-fenced `settingsScope`); `ui-settings-models` row | llm-pi-ai card exposes the omniroute route fields; a settings write through the web surface updates scratch `settings.yaml` and the next request reflects it | PASS, FAIL, BLOCKED |
| G7-09 | cookbook `adding-a-conversation-node`: durable event family → keyed chat nodes | cookbook recipe (match/update/replay determinism; stable business ids) | after a goal/todo session, the session window data carries goal/todo nodes with stable ids; re-read replay yields identical ids | PASS, FAIL, BLOCKED |
| G7-10 | model selection surface | `ui-model-selection` row; llm configurable-provider directory | provider/model list == landed catalog (omniroute ×3); per-session selection persists in settings | PASS, FAIL, BLOCKED |
| G7-11 | lsp seam | `lsp/lsp` (provider registry, four operations, no escape hatch); `lsp-stdio` provider | census; AVAILABLE_DISABLED unless a provider is mounted; if mounted: goToDefinition round-trip on a fixture TS file | PASS (census), AVAILABLE_DISABLED, BLOCKED |
| G7-12 | repo web e2e lane: `DSH_SNAPSHOT=replay pnpm run test:web` | `vitest.web.config.ts`; committed goldens | suite exit 0 (Playwright Chromium, test tooling) | PASS, FAIL, BLOCKED (browser install) |
| G7-13 | repo GUI lane: `pnpm run test:gui` | client AGENTS.md testing tiers | suite exit 0 in the refreshed scratch copy | PASS, FAIL, BLOCKED |
| G7-14 | TypeScript SDK: client → stdio runtime, one routed turn | `sdk/client` (`DeepSeekHarness`/`HarnessClient`); `sdk/server` (JSON-RPC stdio, `shutdown` answers exit 0) | turn completes; notifications stream; session durable; runtime exits 0 on shutdown | PASS, FAIL, BLOCKED |
| G7-15 | Python SDK: protocol handshake + one turn over the same channel | `python/sdk` (`deepseek_harness`); `python/sdk-runtime` channel contract | initialize + prompt + reply via the Python client | PASS, FAIL, BLOCKED (runtime provisioning) |
| G7-16 | ACP automation server: initialize → session/new → prompt (+ cancellation) | `acp/acp` (automation-only; prompt text, committed assistant text, cancellation, one-shot permissions) | JSON-RPC flow returns assistant text for a nonce task; cancel path recorded; fixture omni route patch | PASS, FAIL, BLOCKED |
| G7-17 | message-feedback via web | `feedback/message-feedback` + `command-feedback` (log-only feedback event) | feedback event durable; FEEDBACK_ONLY sharing posture respected | PASS, FAIL, BLOCKED |
| G7-18 | terminal: persistent PTY keeps state across sends | `terminal/terminal` (owner-scoped PTY registry); `terminal-bash` backend | `cd` persists between sends (the fresh-shell bash tool contrast); teardown awaited | PASS, FAIL, BLOCKED (mount state at release) |
| G7-19 | telemetry sharing modes against a local OTLP capture | base telemetry row (`DSH_TELEMETRY_MODE` FULL/FEEDBACK_ONLY; exporter config) | fixture collector on localhost: FEEDBACK_ONLY exports feedback-class only; FULL exports session records; frames captured and classified | PASS, FAIL, BLOCKED |
| G7-20 | locale/boot payload | `ui-locale` row; client AGENTS.md (Chinese product copy) | boot payload/index carries locale resources; no missing-translation marker in the served shell | PASS, FAIL, BLOCKED |

## 5. Risks and carry notes

- **R1 — web API envelope discovery.** G7-02..04, G7-08..10 depend on the
  Typert RPC envelope (`dsh-client-connection`). The scripts discover methods
  from the served boot payload and the `api-remotes` assembly at execution;
  any row whose envelope cannot be traced goes BLOCKED with the discovery
  output, never guessed.
- **R2 — model-cooperation density.** Gate 6 is tool-use heavy (goal, todo,
  workflow, subagent, ralph). Three recorded attempts with queue spacing per
  row; persistent failure records FAIL with transcripts.
- **R3 — Chromium for G7-12.** Playwright's browser install is test tooling
  (owner ruling). If the download channel is blocked at release, G7-12 is
  BLOCKED with the dependency named; G7-01's static serve proof stands alone.
- **R4 — SDK/ACP demo compositions ship their own provider defaults.**
  G7-14..16 route them through the omni fixture via the documented config
  overlays; if a demo composition cannot take an overlay, the row records the
  adapter Morpheus lands for it or goes BLOCKED.
- **Carry:** G7-07 is the G4-06(b) evaluation — if neither web nor API opens a
  corrupted-current session, the row stays BLOCKED-by-design with the exact
  read-path evidence and moves to the Phase C sandbox/DR discussion.

## 6. Script inventory

All under `pilots/PILOT-DSH-IMPL-001/gordon/phase-b/` (static artifacts):

- `conftest.py` — Phase B fixtures: imports `gordon_util` from `../phase-a`,
  web-boot harness (loopback, OS port, log capture), API/SSE helpers,
  settings-file reader, scratch skill/hook/mcp fixture builders.
- `test_g6_orchestration.py` — G6-01..23.
- `test_g7_surfaces.py` — G7-01..20.
- `fixtures/` — patch templates (`patch-schedule.yml.tmpl`,
  `patch-mcp.yml.tmpl`, `patch-presets.yml.tmpl`,
  `patch-session-query.yml.tmpl`, `patch-hooks.yml.tmpl`), fixture
  `SKILL.md`, fixture Claude hook settings, OTLP capture helper
  (`otlp_capture.py`).
- `run-phase-b.sh` — orchestrator (same contract as Phase A).
- `README.md` — runbook: release preconditions (Phase B handoff, frontend
  dist, Chromium), env contract, per-gate commands.

Completion language at execution: `[GATE VERDICT — Gate 6 — <verdict>]`,
`[GATE VERDICT — Gate 7 — <verdict>]`, campaign close per §12.3.
