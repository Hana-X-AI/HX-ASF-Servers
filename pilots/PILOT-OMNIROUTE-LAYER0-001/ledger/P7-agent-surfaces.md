# P7-agent-surfaces — partition summary

- Work order: WO-OMNI-TRINITY-LEDGER-001 · Partition: P7-agent-surfaces (the disabled-by-default / control-plane-collision class)
- Producer: trinity (owner-ratified 2026-08-27, KDD-0008; first commission)
- Corpus: `/opt/tkv-local/OmniRoute-release-v3.8.51` (READ-ONLY; identity VERIFIED 2026-08-27 — 13,098/13,098 git-blob identical to upstream `diegosouzapw/OmniRoute@42a13fe…`; no writes made, no code executed, no node/npm runs)
- Ledger: `pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/P7-agent-surfaces.json` — **60 entries** (54 capabilities + 6 NOT-ESTABLISHED), all 12 schema fields each, 227 source refs
- Reviewed at: 2026-08-27T09:10Z
- Truth-state labels: **FACT** = verified in source at the cited line · **UPSTREAM** = bundled-doc claim (drift-prone) · **INFERENCE** = producer reasoning, labeled in place · **AUTHORITY** = HX governance decision
- Partition rule: every entry carries a control-plane-collision note (orchestration / catalog / authority / disabled-by-default) inside its `purpose` field — the schema's 12 keys are fixed, so the note rides in `purpose` as "Collision: …"

## Startup receipt

```text
[TRINITY KNOWLEDGE REVIEW COMPLETE]
Agent: Trinity
Goal Contract: GOAL-OMNI-TRINITY-LAYER0 v1 (WO-OMNI-TRINITY-LEDGER-001, partition P7)
Target Host/Environment: read-only source work from hxs-5 — no host target
Source Corpus: /opt/tkv-local/OmniRoute-release-v3.8.51 (DOC-tkv-corpus-omniroute)
Reviewed At: 2026-08-27T09:10Z
Source Identity: VERIFIED 2026-08-27 by content-sensitive proof (07-source-provenance-receipt.md)
Installed Identity: NOT INSTALLED (Layer 0; no host contact this partition)
Relevant Knowledge: charter.md, profile.md, 05-work-order, 06-context-packet (citation contract),
  repo AGENTS.md, sibling ledgers P1–P6 (P4 for the spawn/MCP guard cross-reference, P3 for the tool pipeline)
Allowed Change Surfaces: read-only corpus reads; ledger writes under pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/
Known Drift/Risks: in-tree AGENTS/CLAUDE/GEMINI = untrusted upstream guidance; assess-route env-var typo;
  agent-card version fallback '1.8.1'; omni-mcp SKILL.md advertises 32 scopes vs 17 measured
Rollback Ready: YES (read-only — nothing to roll back)
Task May Proceed: YES
```

## Coder-X receipts (model contract)

```text
[CODER-X IDENTITY RECEIPT]
endpoint:        http://192.168.50.201:11434  (hxs-2) — verified live from hxs-5 BEFORE first call, 2026-08-27T08:04Z
/api/version:    {"version":"0.32.15"}
/api/ps:         model hx-qwen3.6-coderx-64k:latest RESIDENT
                 digest  ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1 (matches expected ec9ebe08a824…)
                 size    17815411094 == size_vram 17815411094  (fully in VRAM)
                 context_length 65536  (ctx 65536 contract PASS)
verdict:         IDENTITY + HEALTH PASS — no substitution, no cloud
```

Coder-X call count: **2 `/api/generate` calls** (+ 2 metadata calls: 1× `/api/version`, 1× `/api/ps`).

1. MCP/A2A/ACP/skills/plugins posture + collision corroboration (3,911 prompt tokens / 999 eval, 23.2 s)
2. Memory/injection/webhooks/middleware/services/conductor/assess/tunnel corroboration (3,018 / 816, 9.7 s)

Both prompts = bounded questions + numbered source excerpts only (`nl -ba` line numbers + `<path> lines a-b`
headers, per the citation contract; no credentials or credential-shaped strings — structure quoted, never values),
`think:false`, temperature 0.2. Outputs used as corroboration only; every cited file:line was re-verified
deterministically by the producer. Coder-X corrections applied: (a) its Surface-5 Q1 citation
"db/settings.ts line 44" is wrong — the skills gate is `src/lib/skills/executor.ts:44` (it cited executor.ts:44-46
correctly in its own Q3); recorded in the measurement below. (b) Its under-guarded finding — ACP children inherit the
full gateway env (`acp/manager.ts:67`) — was independently verified and promoted into CAP-P7-013/906. One divergence
kept on producer judgment: Coder-X called the Conductor hub "no collision — a client for an external orchestrator";
for the HX lane that IS the collision (external orchestration driving local task state), recorded as CAP-P7-048 BLOCKED.

Bounded corrections used: **1 of 2** (first reference-check run: 2 empty-line anchors fixed; spot-check pass: 1
declaration-vs-gate anchor re-anchored — all in one scripted correction cycle).

## 1. Agent-surface inventory by disabled-by-default class [FACT]

**MCP (7 entries, CAP-P7-001…006 + cross-refs).** A full in-process MCP server (`createMcpServer`,
open-sse/mcp-server/server.ts:733) exposes ~107 tools — routing/quota/budget/resilience writes plus memory, skill,
agent-skill, github-skill, plugin, pool, gamification, notion, obsidian and local-corpus families — over stdio, SSE,
and streamable-HTTP. Disabled by default: `mcpEnabled: false` (settings.ts:172); HTTP transports 503 via
`guardEnabled` (stream/route.ts:15-23); the whole `/api/mcp/` prefix is Tier-1 LOCAL_ONLY (routeGuard.ts:34) with the
`mcp:connect` scope carve-out (bypass default-enabled for `/api/mcp/`, settings.ts:228-229). Scope enforcement is
real but env-gated fail-open (`OMNIROUTE_MCP_ENFORCE_SCOPES`, scopeEnforcement.ts:107-109); per-key scope binding
exists on HTTP/SSE (httpAuthContext.ts:54-70) while stdio has no per-caller identity (:51). Audit trail appends to a
dedicated `mcp_tool_audit` table (audit.ts:4).

**A2A (5 entries, CAP-P7-007…011).** JSON-RPC `/a2a` router (v0.3 + v1.0 aliases) hard-gated on
`a2aEnabled: false` default → -32000/503 (route.ts:147-160, settings.ts:173); in-memory task manager with TTL,
concurrency cap, and GHSA-jcm5 owner hashing (keyless tasks visible to all by design); auth mirrors the /v1 keyless
local-first posture; agent card always served at `/.well-known/agent.json` with a stale `1.8.1` version fallback
(:17, UPSTREAM drift); six builtin agent skills execute through the routing pipeline.

**ACP (2 entries + 2 NOT-ESTABLISHED, CAP-P7-012/013, 901, 906).** "ACP" here is CLI-as-backend, not the wire
protocol (CAP-P7-901): a registry probing host CLIs (codex/claude/gemini/goose + custom binaries) via execFileSync,
and a spawner (`AcpManager.spawn`, manager.ts:65-69) that hands children the full gateway env. The API is LOCAL_ONLY
(routeGuard.ts:72); the spawner has **no production call site** (grep-verified — currently unwired) and no sandboxing
(CAP-P7-906).

**Memory (4 entries, CAP-P7-014…017).** Per-api-key memory store with decay/TTL, default `enabled: false`
(memory/settings.ts:33,101); injection into every chat request with the `x-omniroute-no-memory` opt-out header
(chatCore.ts:1246-1253); pluggable backends (sqlite default, external Qdrant, Obsidian vault file writes); embeddings
service with a private/LAN trusted-no-auth posture (#6925).

**Skills (7 entries, CAP-P7-018…024).** Registry + executor whose gate blocks only when
`settings.skillsEnabled === false` — **no hardcoded default exists, so execution is default-allow** (executor.ts:44;
grep-verified across src/lib/db). Skills inject as provider-native tools (`omr_skill_` encoding) and intercept model
tool calls gateway-side; container sandbox (docker/apple/wsl/podman) with network-off/read-only defaults;
skills.sh external installs (provider-switch gated); GitHub collector that writes into *other agents'* directories;
LOCAL_ONLY CLI detection probes plus one PUBLIC chaos dispatch route with per-handler Bearer auth.

**Plugins (5 entries + 1 NOT-ESTABLISHED, CAP-P7-027…031, 903).** Manager with path-containment delete guard;
child-process loader over IPC with permission-filtered env and SRI integrity hashing; manifest permission enum
(network|file-read|file-write|env|exec) — **declared but not runtime-enforced beyond env filtering** (CAP-P7-903);
marketplace installs guarded by A+AAAA DNS-resolution SSRF checks; traffic-path hooks with fs-watch hot reload.
The whole API tree is LOCAL_ONLY (routeGuard.ts:56-57).

**Evaluation (3 entries, CAP-P7-033…035).** Eval suites running through the local chat route (management-gated,
LAB-ONLY); router-eval observation records; and `/api/assess` — a one-POST fleet-wide model probe with **no
route-level auth** (central MANAGEMENT fallback applies) and a misspelled self-auth env var `OMNIROUTe_API_KEY`
(route.ts:15,147 — FACT, recorded as drift).

**Tunnels (3 entries, all BLOCKED, CAP-P7-036…038).** cloudflared (GitHub-release binary, sha256-pinned),
Tailscale Serve/Funnel, ngrok — each publishes the **whole** gateway publicly (no path restriction found,
CAP-P7-905), colliding with the owner LAN-boundary rule; all mutation endpoints are LOCAL_ONLY-listed and
tailscaleEnabled defaults false.

**Webhooks (2 entries + 1 NOT-ESTABLISHED, CAP-P7-039/040, 902).** HMAC-SHA256-signed dispatcher with dispatch-time
SSRF re-validation and 3 retries; management CRUD for slack/telegram/discord/custom kinds; delivery history persisted
but **no durable retry queue** (fire-and-forget, CAP-P7-902).

**Embedded services (3 entries, CAP-P7-041…043).** Generic child-process supervisor with health probes and
SIGTERM stop-all; npm/binary installers for 9router, cliproxyapi, dario, bifrost — and **mux, self-described as "a
local agent-orchestration daemon"** (installers/mux.ts:4); supervised daemons register as passthrough providers,
nesting an unverifiable second routing layer behind OmniRoute routes. `/api/services/` is LOCAL_ONLY (routeGuard.ts:42).

**Remote administration (4 entries, CAP-P7-044…047).** restart/shutdown SIGTERM endpoints (management-auth only —
no feature-flag disable found, CAP-P7-904); LOCAL_ONLY job registry with a default-RUNNING background-services
posture (`OMNIROUTE_DISABLE_BACKGROUND_SERVICES` unset = run, instrumentation-node.ts:105-109); PUBLIC-classified
Telegram bot gateway (503 unless a bot token is configured); admin concurrency inspect/reset.

**Process-spawning intersection with P4 (cross-reference, not duplication).** P4 measured 43+4 LOCAL_ONLY guard
entries; P7 read the same list (routeGuard.ts:33-77) and confirms it covers every spawn-capable P7 surface found:
`/api/mcp/`, `/api/services/`, `/api/tunnels/*` (5 entries), `/api/plugins(+/)`, `/api/middleware/`, `/api/jobs(+/)`,
`/api/acp/agents`, `/api/skills/collect/`, `/api/vnc-session/*`, `/api/tools/agent-bridge/`, `/api/settings/mitm`,
`/api/copilot/`, `/api/issue-agent/`, oauth auto-imports, plus the dynamic Playwright-spawn patterns. P3's tool
pipeline owns the streaming/tool-call mechanics; P7 ledgered only the agent-surface wiring (injection/interception)
and cross-references, per the work order.

## 2. Collision analysis per class (orchestration / catalog / authority / disabled-rule)

- **Orchestration collisions (KK3):** Conductor hub (CAP-P7-048 — external hub mirroring tasks into local A2A
  state; BLOCKED); cloud agent providers (CAP-P7-049 — BLOCKED, also no-cloud); mux installer (CAP-P7-042);
  ACP spawner (CAP-P7-013); A2A endpoint + task manager (CAP-P7-007/008); MCP write tools (CAP-P7-001);
  middleware vm hooks and plugin hooks as ungoverned second routing brains (CAP-P7-032/031).
- **Catalog/knowledge collisions (Carol):** memory engine + memory builtins (CAP-P7-014/021 — a second long-term
  memory with model-driven writes); agent-skills SKILL.md corpus advertising the full control surface
  (CAP-P7-025); GitHub collector writing foreign agent dirs (CAP-P7-023).
- **Owner authority-plane collisions:** tunnels (CAP-P7-036…038 — boundary widening; BLOCKED); MITM agent bridge
  (CAP-P7-051 — host trust-store/DNS mutation, also rick's lane; BLOCKED); VNC credential harvest (CAP-P7-052);
  copilot LLM-with-CLI-execution (CAP-P7-053); OAuth host-credential imports (CAP-P7-054); restart/shutdown
  (CAP-P7-044); Telegram public ingress (CAP-P7-046).
- **Disabled-by-default rule status:** code-enforced defaults exist for MCP (`mcpEnabled:false`), A2A
  (`a2aEnabled:false`), memory (`enabled:false`), Tailscale (`tailscaleEnabled:false`) and OIDC — but **skills
  execution is default-allow** (no `skillsEnabled` default; executor blocks only on explicit `false`,
  CAP-P7-018) and **background jobs default to running** (kill-switch default-off, CAP-P7-045). Both need an
  explicit deployment-time setting to honor the HX rule [FACT].

## 3. Disable / quarantine paths (evidence)

| Surface | Disable/quarantine | Evidence |
| --- | --- | --- |
| MCP server | `mcpEnabled=false` default → 503; LOCAL_ONLY prefix; scope env gate | settings.ts:172; stream/route.ts:15-23; routeGuard.ts:34; server.ts:104 |
| A2A | `a2aEnabled=false` default → -32000/503 | settings.ts:173; a2a/route.ts:147-160; tasks/route.ts:119 |
| ACP | LOCAL_ONLY API; registry whitelist; spawner unwired | routeGuard.ts:72; manager.ts:54; grep: no callers |
| Memory | `memoryEnabled=false` default; per-request no-memory header | memory/settings.ts:33,101; chatCore.ts:1250-1252 |
| Skills | explicit `skillsEnabled=false` (default-allow!); per-skill enabled flag | executor.ts:44; registry.ts:413-420 |
| Skill sandbox | fail-closed when no container runtime on host | containerProvider.ts:71-79 |
| Plugins | nothing installed by default; LOCAL_ONLY API; deactivate/uninstall | scanner.ts:27-30; routeGuard.ts:56-57; manager.ts:77-81 |
| Middleware hooks | registry empty without configured hooks; LOCAL_ONLY API | registry.ts:29-38; routeGuard.ts:58 |
| Tunnels | not installed/started; LOCAL_ONLY mutations; BLOCKED by HX rule | routeGuard.ts:43-48; settings.ts:146 |
| Webhooks | no rows → no dispatch; SSRF guard at create+dispatch | webhookDispatcher.ts:45,78; webhooks/route.ts:31-40 |
| Embedded services | LOCAL_ONLY API; supervisor stop; not installed by default | routeGuard.ts:42; registry.ts:20-42 |
| Jobs | `OMNIROUTE_DISABLE_BACKGROUND_SERVICES=1`; per-job disable; LOCAL_ONLY | instrumentation-node.ts:105-109; routeGuard.ts:64-65 |
| Telegram | `TELEGRAM_BOT_TOKEN` unset → 503 | telegram/update/route.ts:11 |
| Conductor | `CONDUCTOR_HUB_URL` unset → null config, degraded offline | hubProxy.ts:84-87 |
| Cloud agents | no credentials → not callable; BLOCKED by no-cloud rule | registry.ts:7-14 |
| Copilot/MITM/VNC/cli-tools | LOCAL_ONLY tiers incl. bypass kill-switch | routeGuard.ts:50-53,71 |

## 4. NOT-ESTABLISHED items (searched, not found — honest absences)

| ID | Searched for | Result |
| --- | --- | --- |
| CAP-P7-901 | true ACP wire-protocol (session/initialize handshake) | none — "ACP" is CLI-as-backend transport naming [INFERENCE] |
| CAP-P7-902 | durable webhook retry queue | none — fire-and-forget dispatch; history persisted, retries are not (webhookDispatcher.ts:132-141) |
| CAP-P7-903 | runtime enforcement of plugin permissions beyond env filtering | none found — network/file/exec permissions are declarations only (loader.ts:165,386-395) [INFERENCE] |
| CAP-P7-904 | feature-flag disable for restart/shutdown | none — management auth is the only gate |
| CAP-P7-905 | path-restricted tunnel exposure (publish /v1 only) | none — tunnels publish the whole gateway incl. management plane [INFERENCE] |
| CAP-P7-906 | sandboxing for ACP-spawned agent processes | none — full gateway env inheritance, no rlimits/container (manager.ts:65-69) |

## 5. Coverage statement

Covered: MCP (server core, three transports, scope enforcement + per-key binding, audit, introspection routes, tool
families); A2A (JSON-RPC router, task manager, auth posture, agent card, builtin skills); ACP (registry, spawner,
call-site check); memory (engine, injection, backends, embeddings); skills (registry/executor, injection/interception,
sandbox, builtins, skills.sh, GitHub collector, CLI detection + chaos); agent-skills (catalog, generator, skills/
corpus); plugins (manager, loader, manifest, marketplace, hooks/watcher); middleware vm hooks; evaluation (eval
framework, router-eval, assess loop); tunnels (all three); webhooks (dispatcher, management API, integrations,
deliveries); embedded services (supervisor, installers, passthrough backends); remote administration (restart,
shutdown, jobs, telegram, admin concurrency); orchestration-adjacent (conductor hub, cloud agents, issue agent);
interception (MITM bridge, VNC sessions, copilot driver, OAuth auto-imports). Source-hint globs swept: `skills/**`
(45 dirs + README), `src/**/mcp*` (open-sse/mcp-server + /api/mcp + mcpScopes), `src/**/a2a*`, `src/**/acp*`,
`src/**/memory*`, `src/**/plugin*`, `src/**/tunnel*`, `src/**/webhook*`, plus `embed*` (embeddings), evaluation,
remote-admin, and spawn surfaces via a 45-file child_process sweep cross-referenced against P4's guard inventory.
Adjacent spawn surfaces NOT ledgered here (owned elsewhere or folded into the P4 cross-ref): provider login
Playwright patterns, cli-tools settings writers, headroom proxy, redis launcher, db-backups tar, system/version
auto-update, video bridge, cursor renewal probes. Out of scope (flagged): packaging/CLI entry mechanics (P8),
client-protocol streaming internals (P3), guard-tier machinery itself (P4). Nothing activated; all dispositions
preliminary.

## 6. Self-verification result

- Deterministic reference check (scripted, `/tmp/trinity-p7/refcheck.py`, output saved to
  `P7-agent-surfaces.reference-check.txt`): JSON valid; 60/60 entries have all 12 schema fields; **227/227 source
  refs — file exists, cited line in range, line non-empty. PASS** (second run; first run caught 2 empty-line
  anchors, fixed as bounded correction 1).
- Spot content check (scripted, `/tmp/trinity-p7/spotcheck.py`): **45/45 load-bearing refs have the expected symbol
  at the cited line. PASS** (one declaration-vs-gate anchor re-anchored in the same correction cycle).
- ID stability/uniqueness: CAP-P7-001…054 + CAP-P7-901…906, unique, verified programmatically.
- Disposition histogram: AVAILABLE-DISABLED 34 · ACTIVE-CANDIDATE 8 · LAB-ONLY 6 · BLOCKED 6 · NOT-ESTABLISHED 6.

## 7. Citation-contract measurement (P7, second contract partition)

- Contract applied: every Coder-X prompt excerpt carried `nl -ba` absolute line numbers plus `<path> lines a-b`
  headers; small labeled chunks (10 + 10); no anchor citations needed; harness verified everything regardless.
- Coder-X-drafted line citations: **1 wrong of 32 drafted (3.1%)** — call 1 cited "db/settings.ts line 44" for the
  skills gate (nonexistent; the gate is executor.ts:44, which it cited correctly elsewhere in the same answer);
  caught in deterministic drafted-citation review before writing. Call 2: 0 wrong of 12. The wrong citation was a
  file-attribution slip, not offset arithmetic — the contract's target failure class (excerpt-offset math) did not
  recur.
- **Baselines: P1 21/59 wrong (35.6%) → P5 1/25 (4.0%) → P6 2/70 (~3%) → P7 1/32 (3.1%).** Contract holds at ~1-32 error rate.
- Analysis-level (not line-number) divergences, both resolved against source: the Conductor collision severity
  (kept BLOCKED — mechanism FACT, severity INFERENCE labeled) and the ACP env-inheritance finding (verified,
  promoted to CAP-P7-013/906).

## 8. Ten-line summary

1. Entries: 60 (54 capabilities + 6 NOT-ESTABLISHED), 227 refs, all 12 schema fields, every entry collision-noted.
2. Collision breakdown: orchestration 9 (Conductor, cloud agents, mux, ACP, A2A×2, MCP writes, hook engines ×2), catalog 4 (memory engine, memory builtins, SKILL.md corpus, GitHub collector), authority 9 (tunnels×3, MITM, VNC, copilot, OAuth imports, restart, Telegram public ingress CAP-P7-046), disabled-rule gaps 2 (skills default-allow, jobs default-run).
3. Highest-risk surface: **CAP-P7-053 copilot LLM driver — model output executes as host CLI commands** (copilot/tools.ts:4-8), loopback-confined only by the LOCAL_ONLY tier (routeGuard.ts:50); runners-up: CAP-P7-048 Conductor (external orchestrator mirroring local task state, hubProxy.ts:84, bridge.ts:1-8) and CAP-P7-013 ACP spawner (children inherit full gateway env, manager.ts:67).
4. BLOCKED (6): all three tunnels (LAN-boundary rule), Conductor hub, cloud agents (no-cloud rule), MITM bridge (host trust mutation).
5. Disabled-by-default rule is NOT code-enforced for two surfaces: skills execution (no `skillsEnabled` default — executor.ts:44 blocks only explicit false) and background jobs (kill-switch default-off — instrumentation-node.ts:105-109); both need explicit deployment settings.
6. NOT-ESTABLISHED: ACP wire protocol, durable webhook retry queue, plugin permission runtime enforcement, restart/shutdown disable flag, path-restricted tunnels, ACP spawn sandboxing (CAP-P7-901…906).
7. Drift recorded: `/api/assess` env-var typo `OMNIROUTe_API_KEY` (route.ts:15,147) defeats its own key config; agent-card version fallback '1.8.1'; omni-mcp SKILL.md claims 32 scopes vs 17 measured (mcpScopes.ts:11-21).
8. Coder-X: identity/health PASS (digest ec9ebe08a824…, size==size_vram, ctx 65536); 2 analysis calls + 2 metadata calls; corroboration only; 1 of its citations corrected, 1 finding promoted.
9. Self-verification: 227/227 refs PASS + 45/45 symbol spot-checks PASS (second scripted run); bounded corrections 1 of 2; no stop condition hit; corpus untouched; no git commit.
10. Citation-contract measurement: 1/32 Coder-X-drafted lines wrong (3.1%) vs the P1 baseline 21/59 (35.6%), P5 1/25 (4.0%), and P6 2/70 (~3%) — contract holds; residual class is file-attribution slips, not offset arithmetic.
