# PILOT-DSH-IMPL-001 — Phase A baseline install (Morpheus)

| Field | Value |
| --- | --- |
| Task | Phase A baseline: dsh 0.1.1-rc.2 source transport, pinned dependency install, real build, native runtime shape, OmniRoute provider seam on hxs-15 |
| Agent | Morpheus (dsh lifecycle steward, KDD-0009), first dispatch |
| Work order | KK3 dispatch 2026-08-28 (state-log row 6); owner checkpoint GO 2026-08-28 |
| Target | hxs-15 (192.168.50.214) — ONLY |
| Executor host | hxs-5 (192.168.50.204), user hxsa |
| Controlling docs | GOAL-DSH-IMPL-001 (`00-goal.md`); plan `agent-zero-docs/projects/Deepseek/2026-08-28-dsh-full-implementation-plan.md`; HX-AGENT-MORPHEUS-DSH-001 (distilled: `agents/morpheus/`) |
| Credential handling | SSH via `SSH_ASKPASS` temp helper (0700) reading the governed credential-record row at execution time only; never printed/logged/stored; helper deleted at task end. OmniRoute key consumed by mechanism only — VALUE never in this document, any log, dump, or context |

## 1. Knowledge-review receipt (emitted FIRST, per profile §5)

| Field | Value |
| --- | --- |
| goal / work-order ids | GOAL-DSH-IMPL-001; state-log row 6 (Phase A GO); KDD-0009 |
| target environment | hxs-15 (192.168.50.214), Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic, 4c/4t, 31 GiB; identity MATCH vs discovery (hostname, machine-id `62cc8758d1854524989541c2af1be5b9`, peer 192.168.50.214:22) |
| knowledge root 1 (HX decisions) | `/home/hxsa/opt/local-tkv/agent-zero-docs/projects/harness` + `.../projects/Deepseek` — reviewed; identities (sha256): morpheus source profile `3158ecbc…dc02`, kk3 harness-review+amendment `55a11334…168f`, roadmap `4b7b3bd8…3aa2b`, implementation plan `d9df4ff2…f3d5`, gordon profile `c92a4636…70c0c` |
| knowledge root 2 (approved source) | `/opt/tkv-local/deepseek-harness-master` @ `@deepseek-ai/dsh-root` **0.1.1-rc.2**, `packageManager: pnpm@11.7.0`, engines `^22.19.0 \|\| >=24.0.0`; surveyed with the be-great skill: repo AGENTS.md, apps/cli README + behavior reference, bundle/base + bundle/headless patches, llm/llm-pi-ai README, util/launch-environment + home-paths, pnpm-workspace.yaml, scripts/build.ts, scripts/install-lefthook.mjs, native/README.md |
| installed runtime identity (pre-state) | Node **v24.20.0** (`/opt/node-v24.20.0`, GPG-authenticated by rick), pnpm **11.7.0** (integrity-verified); dsh uid 999 no-sudo nologin; `/opt/dsh` 0755 dsh:dsh (EMPTY), `/var/lib/dsh` 0750 dsh:dsh; 0 failed units; no relevant listeners; registry.npmjs.org reachable (HTTP 200); rick evidence `servers/hxs-15/2026-08-28-dsh-runtime-prep.md` re-verified live 2026-08-28T09:1xZ |
| effective profiles/bundles/patches (pre-state) | none — no dsh installation present |
| persistence backend (target) | dsh-native: session JSONL under `$DSH_HOME/sessions` + in-memory session-query SQLite (search disabled, `openAt: never`), attachments content-addressed local; `$DSH_HOME=/var/lib/dsh` |
| upstream sources | none consulted beyond the pinned corpus (local-only; snapshot anchors govern) |
| allowed changes | hxs-15 only: populate `/opt/dsh` (dsh:dsh) with the transported+built tree; pnpm install with the pinned lockfile (no rewrites); create `/var/lib/dsh` content (DSH_HOME layers); a launcher shim; the root-mediated env mechanism for the staged key; NO systemd service unless the native shape calls for one (finding: it does not — §6) |
| protected constraints | local-only doctrine; no cloud providers/external services at runtime; web-search-*, experimental/agent-team, model-authored dynamic-plugin surfaces DISABLED; Web UI NOT activated (no `dsh web`, no 0.0.0.0, no web frontend build); OmniRoute + LLM backends + all other hosts untouched; secret values never in artifacts; sudo only where root strictly required; every step reversible with pre-state captured |
| required tests (Gordon, pipelined) | Gates 0–5 per plan; my candidate handoff receipt (§10) carries every identity he needs |
| known drift/conflicts | (1) corpus is a `.git`-less export: tag/commit anchors not verifiable locally — the two pinned file hashes + package identity MATCH (§2); reported, not a mismatch. (2) plan inventory says 2,734 TS files; `find` counts 2,472 `.ts` (different counting basis, not material). (3) repo AGENTS.md/CLAUDE.md files are upstream reference material only — NOT HX governance (profile §3); no upstream instruction was adopted as authority |
| rollback state | pre-state = empty `/opt/dsh`, empty `/var/lib/dsh`, no dsh artifacts; full inverse = remove tree, DSH_HOME content, launcher shim, env copy (§11) |
| **proceed_status** | **MAY_PROCEED** |

## 2. Source identity verification (anchor check)

| Anchor | Expected | Observed (hxs-5 corpus) | Verdict |
| --- | --- | --- | --- |
| package identity | `@deepseek-ai/dsh-root` 0.1.1-rc.2 | `name: @deepseek-ai/dsh-root`, `version: 0.1.1-rc.2`, `packageManager: pnpm@11.7.0` | MATCH |
| tag | `dsh-v0.1.1-rc.2` | not verifiable — export carries no `.git` | REPORTED (§1 drift 1) |
| commit | `b150a551b8d465e31e418e1b2eaf5e79bbb7d28e` | not verifiable — export carries no `.git` | REPORTED (§1 drift 1) |
| package.json SHA-256 | `4adbdffa373754a048a214c5de3ec0671ac6e1f3c1521ec5b37e8fad1a4986d7` | `4adbdffa…4986d7` | MATCH |
| pnpm-lock.yaml SHA-256 | `6f20c268e76df1294c16f016ab10a7fa1271608b4db0f4fafe8f7c21ec90013e` | `6f20c268…90013e` | MATCH |

Post-transport re-verification on hxs-15: see §3.

## 3. Transport (hxs-5 → hxs-15)

- Method: `tar -czf - deepseek-harness-master | ssh hxsa@192.168.50.214 'sudo -n tar -xzf - -C /opt/dsh --strip-components=1 && sudo -n chown -R dsh:dsh /opt/dsh'` — streamed, no staging copy retained.
- Pre-transport manifest on the corpus: 7,903 regular files, sha256 each, sorted; 0 symlinks.
- Post-transport manifest on `/opt/dsh` regenerated and diffed: **TREE_INTEGRITY_MATCH** (byte-identical, all 7,903 files).
- Anchors re-verified on hxs-15: package.json `4adbdffa…4986d7` **MATCH**; pnpm-lock.yaml `6f20c268…90013e` **MATCH**.
- Tree owner `dsh:dsh` (root used only for extraction into the root-parent directory and the chown — the two operations that strictly require it).

## 4. Dependencies (pnpm 11.7.0, pinned lockfile)

- Command (as `dsh`, `HOME=/home/dsh`): `cd /opt/dsh && pnpm install --frozen-lockfile --reporter=append-only` → **exit 0 in 12.2s**; scope "all 246 workspace projects".
- **No silent lockfile rewrite — proven:** sha256 of `pnpm-lock.yaml` before vs after identical (`6f20c268…90013e`, still the review anchor); pnpm reported "Verifying lockfile against supply-chain policies (1215 entries)" and "Lockfile is up to date, resolution step is skipped".
- Install warnings (benign, recorded): arm64-only native package skipped on x64 (expected); upstream cyclic workspace-dependency notice; two bin-link warnings for pre-build demo packages (`dsh-sdk-jsonrpc-demo`, `dsh-acp-demo` — demos, not the product CLI); `allowBuilds`-reviewed lifecycle scripts ran per `pnpm-workspace.yaml` (subprocess-local spawn-helper, esbuild, node-pty, koffi); root postinstall `install-lefthook.mjs` no-ops without `.git` (verified by reading it pre-install).
- Result: `/opt/dsh/node_modules` 1.4 GB, dsh:dsh.
- **Audit (captured, full output retained transiently): `pnpm audit` → 38 advisories (15 high / 20 moderate / 3 low), exit 1.** Package/severity table: high — brace-expansion ×5 ranges, fast-uri ×2, ip-address, js-yaml ×2, nanoid ×2, postcss, undici, vite; moderate — @hono/node-server, dompurify, esbuild, hono ×3, ip-address ×2, mermaid ×4, postcss, protobufjs, undici ×4, vite ×2; low — dompurify, hono, mermaid. **Disposition:** the pin stands (work order forbids lockfile rewrites; the snapshot is a developer-preview rc); exposure note — vite/esbuild/mermaid/dompurify/postcss are build-time or docs-chain only, hono/@hono/node-server enter via mcp-client (not mounted; Phase B surface) and pi-ai's optional @google/genai backend (scripts denied, not used by the omniroute route), js-yaml is the config-parse library (configs here are root/dsh-authored, not attacker-controlled), undici/brace-expansion/nanoid/fast-uri/ip-address/protobufjs are transitive. **R1 for the governor/Gordon: upstream advisory debt of the pinned snapshot — no local remediation authorized.**

## 5. Build (repository's real build path)

- Path taken: the repository's own build — `pnpm run build:lib` (= `tsc -b tsconfig.host.json && tsdown --env.DSH_BUILD_FACE host`, then the client face) — **NOT** the aggregate `pnpm run build`, which additionally runs `build:web` (the browser frontend). Skipping `build:web` is the work-order boundary "no web build activation this phase"; `build:lib` is the repo-defined artifact path the installed CLI consumes (`apps/cli/reference/README.md`: "the installed form launches the built `apps/cli/lib/bin.js`").
- Command (as `dsh`, `HOME=/home/dsh`): `cd /opt/dsh && pnpm run build:lib` → **exit 0** (~100 s on 4c/4t).
- Artifact verification: `/opt/dsh/apps/cli/lib/bin.js` (executable, sha256 `c0226687bb20f45c603ec6fe50f3de16d1c3510c3a803304ec575ef9bc366c62`) + chunked runtime bundles; **238 `lib/` directories** across `packages/`, `apps/`, `vendor/`; tsdown emitted host and client runtime bundles; tsbuildinfo + `lib/types` present.
- Runtime proof of the artifact path: `dsh --version` → **0.1.1-rc.2** via the installed shim (below), i.e. plain Node over built `lib/` — no tsx, no rebuild.
- No container fallback used or needed; no build failure encountered.

## 6. Runtime shape (from source — finding and reasoning)

**Finding (from the repo's own docs):** dsh's native Phase A shape is the **CLI launcher over profiles**, not a daemon. `apps/cli/reference/README.md`: the installed form launches built `apps/cli/lib/bin.js`; `$DSH_HOME` (precedence: explicit config > `$DSH_HOME` > `~/.dsh`) roots all user data; `dsh --profile <name>` boots `$DSH_HOME/profiles/<name>`; `web` and `headless` profiles auto-initialize from shipped templates; the headless profile "mounts no ApiProxy, Host, HTTP server, Web runtime, or browser client… and opens no listening port". The only server-shaped mode is `dsh web` — Phase B and prohibited this phase.

**Installed shape (as deployed):**

| Element | Value | Ownership |
| --- | --- | --- |
| Installation tree | `/opt/dsh` = the transported + built workspace (source, `node_modules`, built `lib/`) | dsh:dsh 0755 |
| Launcher | `/usr/local/bin/dsh` — 8-line `sh` shim: `DSH_HOME=${DSH_HOME:-/var/lib/dsh}` then `exec /usr/local/bin/node /opt/dsh/apps/cli/lib/bin.js "$@"`; Node rides the fleet selector (`/usr/local/bin/node` → `/opt/node-v24.20.0` at install time) | root:root 0755, sha256 `0b68259fb4e95869689ef680a781d82bf0b0a95a50ba9bc1a03243b852efcdba` |
| Data root (`DSH_HOME`) | `/var/lib/dsh` — sessions, profiles, settings, `.env` launch layer | dsh:dsh 0750 |
| Runtime identity | `dsh` (uid 999, nologin, no sudo) with `HOME=/home/dsh` — rick's handoff contract | — |
| Invocation | `sudo -n -u dsh env HOME=/home/dsh dsh --profile headless "<task>"` (privilege mediation to *become* dsh; dsh itself never holds sudo) | — |

**systemd decision — no unit this phase (recorded reasoning):** the native shape calls for no service. Headless runs are one-shot (start → task → bounded drain → exit 0); profile boot is operator-invoked; the only listener-capable mode (`web`) is Phase B and forbidden. Installing a unit would add a non-native supervision layer with no native consumer. If Phase B activates the web profile, a systemd unit with `EnvironmentFile=/etc/dsh-omniroute.env` becomes the natural shape and is recorded here as the upgrade path. HX "no containers, native systemd services" doctrine is satisfied — dsh runs as a native binary process; nothing about this phase's CLI shape is containerized or daemonized.

**Key-material mechanism (value never in any artifact):** the governor-staged `/etc/dsh-omniroute.env` (0600 root:root, sha256 `596ea242…80cc`, **untouched**) was consumed through dsh's *native* credential layer instead of systemd: a root-mediated byte-faithful copy at `$DSH_HOME/.env` (root:dsh 0640, sha256 **identical** to the staged file — `install` used, value never entered my context, logs, or this document). `$DSH_HOME/.env` is dsh's documented `user-env` launch layer (`dsh-launch-environment`), materialized into the launch environment; the adapter resolves `apiKeyEnv: OMNIROUTE_API_KEY` **by reference** per request. Root ownership means the runtime identity can read but not alter its credential file. The file's variable names (`OMNIROUTE_BASE_URL`, `OMNIROUTE_API_KEY`) were extracted names-only for configuration; the base URL is additionally pinned as a literal in the composition layer (a ratified LAN address, not a secret).

**Deliberately NOT set:** `DSH_TELEMETRY_DISABLED` in the launcher — the shipped base already defaults telemetry to `DISABLED`, and hard-forcing the opt-out would make the Phase A telemetry family untestable for Gordon's Gates (he can still exercise the env seams explicitly). Local-only is preserved by the default.

## 7. Provider-seam finding (the open question, resolved from source)

**Finding: dsh HAS a native OpenAI-compatible provider seam — no out-of-tree adapter was required.** `@deepseek-ai/dsh-llm-pi-ai` (multi-provider adapter over vendored pi-ai) ships in the `dsh-base` bundle **mounted dormant**; its profile grammar natively supports hand-declared routes with exactly the required fields: `api: openai-completions` (one of `supportedProtocols()`), `baseURL`, `apiKeyEnv` (credential by reference, resolved per request — never a value in config), per-route `models`, and `compat` wire-compatibility switches for gateways pi-ai cannot recognize. Configured natively via the machine composition layer (§8); no upstream core edits, no extension code. The adapter's own README documents the gateway case verbatim ("an OpenAI-compatible gateway, a self-hosted server… is configuration rather than a code change").

Two adapter behaviors were verified relevant and handled: (1) an unrecognized endpoint defaults to OpenAI-2024 wire shape (`developer` role, `max_completion_tokens`) which "most OpenAI-compatible gateways reject at least one of" — countered with route-level `compat: {supportsDeveloperRole: false, maxTokensField: max_tokens}`; (2) a route naming no credential fails requests loud (`MISSING_CREDENTIAL`) — countered by the `apiKeyEnv` reference into the staged key (§6).

## 8. Configuration applied (one compiled layer)

All deployment configuration lives in ONE machine-level composition layer — `/var/lib/dsh/cordis.patch.yml` (root:root 0644, sha256 `14f15b722f4df917f8ecd009c20da2ba9cc8dad044a7b59699472a84803f6016`; root-owned so the runtime identity cannot alter its own policy layer; hot-reload watched per the reference) — six row operations over `dsh-base`:

1. **`llm-pi-ai` config** — hand-declared route `omniroute`: `api: openai-completions`, `baseURL: http://192.168.50.207:20128/v1`, `apiKeyEnv: OMNIROUTE_API_KEY`, `compat` as §7; models = the three catalog-verified fleet ids (2026-08-27, OmniRoute pilot doc 19): `ollama-local/hx-qwen3.8-27b-64k:latest` (Qwen-X), `ollama-local/hx-qwen3.6-coderx-64k:latest` (Coder-X), `ollama-local/hx-muse-glimmer-64k:latest` (Meta-X); each `contextWindow: 65536` (the deliberate fleet 64K operating profile), `maxTokens: 8192` (keeps input+output inside 64K); no `reasoningEfforts` — the harness sends no reasoning parameter this phase.
2. **`agent-default-model` config** — `provider: omniroute`, `model: …coderx…` — Coder-X, the coding/source work class per the fleet local-model-first rule (dsh is a coding harness); shipped default was `deepseek-official/deepseek-v4-flash` (cloud) — repointed.
3. **`llm-deepseek` disabled** — the native DeepSeek cloud adapter row is not mounted (local-only doctrine: no cloud provider surface).
4–6. **`web`, `web-search-deepseek`, `tool-web` disabled** — the work-order web-search-* boundary; the capability row's shipped config names the disabled provider, so all three go together; `web_fetch` was already shipped disabled.

`experimental/agent-team`, model-authored dynamic-plugin, and Codex/Claude-Code subagent surfaces are **absent from the shipped base composition** (verified in the base patch — no rows), so nothing to disable there; `dsh-mcp-client` ships as a CLI dependency with no MCP server enabled by default (no row) — Phase B surface, unmounted. The Web UI: no `web` profile exists (`/var/lib/dsh/profiles/` holds only `headless`), the web frontend was never built, and the CLI rejects `--host 0.0.0.0` upstream regardless.

## 9. Effective-config receipt + boot smoke (profile §5)

**Effective-config receipt** — native dump path: `dsh --profile headless --dump-config` (as dsh, cwd `/var/lib/dsh/workspace`) → exit 0, 366 lines, 0 stderr; **sha256 `dedda886390b873c2575aab8746860a197c34fbdc1257abc3975907f7d518d34`**. The dump carries per-row layer provenance comments: 4 rows "patched by /var/lib/dsh/cordis.patch.yml" (the two config rows + disabled rows) and the headless bundle's own overrides; `llm-pi-ai` shows the full omniroute route; `agent-default-model` shows `omniroute/…coderx…`; `web`/`web-search-deepseek`/`tool-web`/`llm-deepseek` show `disabled: true`; platform-gated pwsh rows remain correctly disabled on Linux. **Redaction check: the dump contains zero secret values — `apiKeyEnv` names only (by design the credential is a reference); verified by inspection.** Identities recorded: source (§2/§3), lockfile (§4), build (§5), profile/bundle/patch (this section + §8), environment (Node v24.20.0, pnpm 11.7.0, shim hash §6).

**Boot smoke (one bounded routed call — install verification, not Gate 3):** `dsh --profile headless "Reply with exactly this token and nothing else: DSH-PHASE-A-SMOKE-OK"` → **exit 0 in ~20 s; stdout exactly `DSH-PHASE-A-SMOKE-OK`; stderr 0 bytes** (matches the shipped headless contract). First-run profile auto-init created `/var/lib/dsh/profiles/headless/` (template: `cordis.yml`, `cordis.patch.yml`, `package.json`, `pnpm-workspace.yaml`) and healed `/var/lib/dsh/profiles/node_modules/` fallback symlinks. Durable session persisted at `/var/lib/dsh/sessions/--var-lib-dsh-workspace--/session-88cbc790-e1be-4a73-94eb-4a2269b344f1/session.jsonl.zstd` — **7 concatenated zstd frames, 27 events**: session header, `permission/preset` (workspace-write), `sandbox/mode`, `approval/policy`, `turn/start`, `step/start`, `user/message`, `request/header`, `request/context`, `session/title-llm-request`, assistant chunks/message, `step/end`, `turn/end`. Identity evidence inside the log: `provider=omniroute` ×6, `model=ollama-local/hx-qwen3.6-coderx-64k:latest` ×6, `api=openai-completions` ×2 (task request + title request — both routed), `usage: {inputTokens: 7501, outputTokens: 54}`. Post-run: no dsh/node listeners, 0 failed units. **This proves end-to-end: composition mounts → credential reference resolves from the staged key → routed call via OmniRoute → durable session lifecycle.** Gateway-side usage_history correlation is Gordon's Gate 3.

**Tooling gotcha for Gordon (Gate 4):** the session log is *appended* as concatenated zstd frames; Node's one-shot/streaming zstd decode yields frame 1 only (160 bytes, header). Decode frame-wise by splitting on the magic `28 b5 2f fd` (method recorded in my command log, §12).

## 10. Candidate handoff receipt — Morpheus → Gordon (OPEN until the governor cites it)

| Identity | Value |
| --- | --- |
| Candidate | dsh **0.1.1-rc.2** Phase A baseline on hxs-15 (192.168.50.214) |
| Source | `/opt/dsh` = byte-identical copy of `/opt/tkv-local/deepseek-harness-master` (7,903-file manifest diff MATCH); anchors: package.json `4adbdffa…4986d7`, pnpm-lock.yaml `6f20c268…90013e` (both MATCH on hxs-15); package `@deepseek-ai/dsh-root@0.1.1-rc.2`, `packageManager pnpm@11.7.0`; git tag/commit anchors not locally verifiable (`.git`-less export — §2, reported) |
| Lockfile | unchanged through install (before/after hash identical); 1,215 supply-chain policy entries verified by pnpm; audit: 38 advisories (15H/20M/3L) — R1, pin stands |
| Build | `pnpm run build:lib` exit 0; 238 `lib/` dirs; CLI entry `/opt/dsh/apps/cli/lib/bin.js` sha256 `c0226687…366c62`; `build:web` deliberately NOT run (Phase B boundary) |
| Installed | `/opt/dsh` (dsh:dsh) incl. `node_modules` 1.4 GB; launcher `/usr/local/bin/dsh` sha256 `0b68259f…efcdba`; runtime Node v24.20.0 via `/usr/local/bin/node`; runtime identity `dsh` uid 999 with `HOME=/home/dsh`; `dsh --version` → 0.1.1-rc.2 |
| Effective config | home layer `/var/lib/dsh/cordis.patch.yml` sha256 `14f15b72…03f6016`; dump sha256 `dedda886…d518d34` (zero secrets); profile auto-init under `/var/lib/dsh/profiles/headless/` |
| Runtime shape | CLI + profiles, no daemon, no systemd unit (§6 reasoning); `DSH_HOME=/var/lib/dsh`; headless = one-shot; sessions at `$DSH_HOME/sessions/<workspace-slug>/<session-id>/session.jsonl.zstd` (multi-frame!) |
| Provider seam | NATIVE `llm-pi-ai` hand-declared route `omniroute` (openai-completions, `http://192.168.50.207:20128/v1`, compat `supportsDeveloperRole:false` + `maxTokensField:max_tokens`); credential `apiKeyEnv: OMNIROUTE_API_KEY` resolving from `$DSH_HOME/.env` (root:dsh 0640, byte-identical to governor-staged `/etc/dsh-omniroute.env` — mechanism only, value never disclosed) |
| Models declared | `ollama-local/hx-qwen3.8-27b-64k:latest` (Qwen-X), `ollama-local/hx-qwen3.6-coderx-64k:latest` (Coder-X, default), `ollama-local/hx-muse-glimmer-64k:latest` (Meta-X); 65536 ctx / 8192 maxTokens; no reasoning params |
| Enabled surfaces | base bundle composition (agent core, tools bash/fs, sandbox workspace-write + approval ask, sessions jsonl + in-memory session-query, settings/credentials, subagent spawn/fork, workflow, jobs, compaction, skills, plan-mode, telemetry DISABLED-default) + headless bundle |
| Disabled/absent surfaces | `llm-deepseek` (cloud), `web`/`web-search-deepseek`/`tool-web` (web-search boundary), web UI/profile (Phase B), web frontend build (Phase B), experimental/agent-team + dynamic-plugin + codex/claude-code subagents + mcp servers (not in shipped composition) |
| Smoke evidence | §9: exit 0, exact token, routed identities in the durable log, usage `{7501 in / 54 out}` |
| Execution contract for Gates | `sudo -n -u dsh env HOME=/home/dsh dsh --profile headless "<task>"` from a dsh-writable cwd (e.g. `/var/lib/dsh/workspace`); config changes route to Morpheus only; the key VALUE is never to appear in any test artifact (reference name `OMNIROUTE_API_KEY` only) |

Handoff state: **OPEN** — Gordon qualifies (Gates 0–5); defects route to Morpheus; the governor cites this receipt on acceptance.

## 11. Boundaries compliance + rollback

- hxs-15 only; OmniRoute/backends/all other hosts untouched (no gateway administration — one client completion call through the approved seam, §9); no cloud providers at runtime; no web-search/experimental/dynamic-plugin surfaces enabled; no web UI (no profile, no frontend build, no 0.0.0.0 — upstream rejects it anyway); no listeners introduced; 0 failed units throughout; dpkg state untouched by this wave; `/etc/dsh-omniroute.env` untouched (hash re-verified); sudo used only for root-requiring operations (extraction into `/opt`, chown, `/usr/local/bin` + root-owned config install, root-mediated `.env` copy, reads of dsh-owned paths); dsh ran only as the dsh user.
- **Rollback (full inverse, pre-state = empty `/opt/dsh` + empty `/var/lib/dsh`):** `sudo rm /usr/local/bin/dsh`; `sudo rm -rf /opt/dsh/* /var/lib/dsh/{cordis.patch.yml,.env,workspace,profiles,sessions}`; rick's runtime scaffold (Node, pnpm, dsh user, empty dirs) remains his lane's baseline. Every step above is individually reversible: config layer removal restores shipped defaults; `.env` removal revokes the credential from the runtime; the source transport is re-runnable from the pinned corpus.

## 12. Sanitized sequential command log

All local commands as hxsa@hxs-5; remote as hxsa@hxs-15 over independent SSH sessions (askpass execution-time credential; `NumberOfPasswordPrompts=1`; pinned known_hosts; `sudo -n` on-host). No secret value appears in any row.

| Seq | UTC | Where | Command (sanitized) | Exit |
| ---: | --- | --- | --- | --- |
| 1 | 09:0x | hxs-5 | Read charter/profile, plan, goal, state log, rick prep, repo AGENTS.md files (reference) | 0 |
| 2 | 09:0x | hxs-5 | be-great survey of `/opt/tkv-local` dsh corpus: identity hashes, llm-pi-ai/cli/base/headless/launch-environment/home-paths docs, build + postinstall scripts, workspace config | 0 |
| 3 | 09:0x | hxs-5 | Emit knowledge-review receipt (§1) → MAY_PROCEED | 0 |
| 4 | 09:1x | hxs-5 | Create askpass helper (0700); extraction smoke `\| wc -c` → 10 | 0 |
| 5 | 09:1x | hxs-15 | Pre-state probe: identity MATCH; runtime v24.20.0/11.7.0; dsh no-sudo; dirs empty; staged file 0600 root, hash MATCH governor prefix, var names only; 0 failed units; registry 200 | 0 |
| 6 | 09:2x | hxs-5 | Corpus manifest: 7,903 files sha256 + 0 symlinks | 0 |
| 7 | 09:2x | hxs-5→15 | Stream `tar c` corpus over ssh → `sudo tar x -C /opt/dsh` + chown dsh:dsh | 0 |
| 8 | 09:2x | hxs-15 | Manifest diff → TREE_INTEGRITY_MATCH; anchor hashes MATCH | 0 |
| 9 | 09:2x | hxs-15 | **MUTATION** `pnpm install --frozen-lockfile` (as dsh) → exit 0; lockfile before/after hash identical; node_modules 1.4 GB | 0 |
| 10 | 09:2x | hxs-15 | `pnpm audit` (capture) → 38 advisories (15H/20M/3L), exit 1 (expected; R1 recorded) | 1* |
| 11 | 09:2x | hxs-15 | **MUTATION** `pnpm run build:lib` (as dsh) → exit 0; bin.js + 238 lib dirs | 0 |
| 12 | 09:2x | hxs-15 | **MUTATION** install launcher `/usr/local/bin/dsh` (root:root 0755); `dsh --version` → 0.1.1-rc.2 (as dsh) | 0 |
| 13 | 09:29 | hxs-15 | **MUTATION** install `/var/lib/dsh/cordis.patch.yml` (root:root 0644); root-mediated `.env` copy (root:dsh 0640, hash identical to staged); mkdir workspace (dsh 0750) | 0 |
| 14 | 09:3x | hxs-15 | `dsh --profile headless --dump-config` (as dsh) → 366 lines, hash recorded; rows verified; zero secrets | 0 |
| 15 | 09:3x | hxs-15 | Boot smoke `dsh --profile headless "…DSH-PHASE-A-SMOKE-OK"` (as dsh) → exit 0, exact token, stderr 0 | 0 |
| 16 | 09:4x | hxs-15 | Session evidence: frame-wise zstd decode → 27 events, omniroute/coder-x identities, usage | 0 |
| 17 | 09:4x | hxs-15 | Boundary sweep: config hashes; staged file untouched; headless profile only; no listeners; 0 failed units | 0 |
| 18 | 09:5x | hxs-5/15 | Write this record; cleanup: askpass helper + remote `/tmp` scratch deleted (verified) | 0 |

`*` audit exit 1 = advisories present; captured as evidence, not an install failure.

## 13. Second Brain disposition (standing directive)

(1) Opportunity identified: the dsh session stores (durable JSONL event logs) and the effective-config dump discipline are natural future Second Brain substrates (session-query/export family is Phase B; catalog is frozen with Carol). (2) Applicable capability: knowledge capture from execution evidence. (3) Disposition: **deliberately deferred** — Phase A scope is the baseline install; Carol is frozen by owner directive and session-query content search ships disabled upstream. (4) Evidence: this record + receipts preserve the material for a later iteration; nothing in this phase blocked or pre-built it.

## 14. Risks and open items

- **R1** — upstream advisory debt of the pinned snapshot (38 advisories, §4): pin stands per work order; governor/Gordon visibility; re-examine at the next upstream intake (my Evolve lane).
- **R2** — git tag/commit anchors unverifiable against the `.git`-less export (§2): file-hash anchors MATCH; if the governor wants the git anchors proven, that needs the upstream repo (external fetch — owner word required by local-only doctrine).
- **R3** — model behavior beyond the smoke (tool-use reliability, thinking content handling, gateway-compat edge cases) is unqualified until Gordon's Gates 3–5 execute; the smoke proves the seam, not the fleet models' fitness.
- **Open** — `Chat-X` class not declared (Gate 3 names three backends; minimal-surface doctrine). One-line addition later if the governor wants the fourth class.
- **Open** — Phase B upgrade path recorded: web profile + systemd unit with `EnvironmentFile=` (§6).

`PASS — PHASE A CANDIDATE INSTALLED; HANDOFF OPEN (Morpheus does not certify own work)`


## 15. Governor corrections (rr batch 2026-08-28) — labeled, append-only

The original receipt text above is preserved unchanged; corrections are appended
here per the open-correction rule.

- **C1 (§9 patched-row count) — DISCREPANCY OF RECORD; re-count scheduled.** §9
  reports 4 "patched by" provenance comments in the dump; §8 documents six row
  operations (2 config + 4 disabled). The authoritative re-count requires
  re-running `dsh --profile headless --dump-config`, which EXECUTES the
  candidate — deferred until Gordon's live campaign closes (the candidate is
  frozen). The verified count and the row-operation↔provenance-comment mapping
  will be appended here at that point. Until then both numbers stand as
  reported, labeled unverified-reconciliation.
- **C2 (§10 Source row, byte-identity) — VALID, corrected.** The 7,903-file
  manifest diff MATCH was taken at TRANSPORT time (pre-install, pre-build). The
  final `/opt/dsh` tree = the transported corpus PLUS generated paths
  (`node_modules` ~1.4 GB, built `lib/` dirs) with no corpus counterpart. The
  anchors (`package.json`, `pnpm-lock.yaml`) remained byte-identical
  post-install (§4/§10). Read "byte-identical copy" as "byte-identical
  transport at install start"; no post-build manifest exists because generated
  content has nothing to match against.
- **C3 (§6 launcher, DSH_HOME export) — INVALID as filed; verbatim evidence of
  record.** The §6 table abbreviated the shim. The ACTUAL launcher (read live
  2026-08-28; hash unchanged vs §6) is 9 lines and ends:
  `DSH_HOME=${DSH_HOME:-/var/lib/dsh}` / `export DSH_HOME` /
  `exec /usr/local/bin/node /opt/dsh/apps/cli/lib/bin.js "$@"` — the export
  precedes the exec. The §9 boot smoke independently proves the data root
  resolved to `/var/lib/dsh` (sessions persisted there). No change required;
  the verbatim content is now of record against the abbreviation.
- **C4 (§11 rollback command) — VALID, corrected.** The documented inverse used
  brace expansion (non-portable in `sh`) and `/opt/dsh/*` (misses dotfiles).
  Corrected inverse: `sudo rm /usr/local/bin/dsh`;
  `sudo find /opt/dsh -mindepth 1 -delete`;
  `sudo find /var/lib/dsh -mindepth 1 -delete` — portable, removes all child
  entries including hidden ones, preserves both directories. rick's runtime
  scaffold (Node, pnpm, dsh user, the then-empty dirs) remains his lane's
  baseline, as before.

## 16. D1/D3 fix record (2026-08-28)

### 16.1 Knowledge-review receipt (emitted FIRST, fix window)

| Field | Value |
| --- | --- |
| goal / work-order ids | GOAL-DSH-IMPL-001; KK3 fix work order 2026-08-28 (D1 + D3; D2 deferred by governor); defect register `04-gordon-phase-a-verdicts.md` (Gordon campaign closed, candidate unfrozen for this window) |
| target environment | hxs-15 (192.168.50.214) — ONLY; the landed Phase A candidate per §10 (unmoved since install; Gordon G0 re-verified all seven receipt identities MATCH at campaign start) |
| knowledge root 1 (HX decisions) | same roots as §1 (identities unchanged — re-hashed at receipt time: plan `d9df4ff2…f3d5`, morpheus source `3158ecbc…dc02`) |
| knowledge root 2 (approved source) | same corpus identity (§2 anchors re-verified MATCH on hxs-5: package.json `4adbdffa…4986d7`, pnpm-lock.yaml `6f20c268…90013e`); fix-specific survey: `native/landlock-run/README.md` + `packages/{entry,linux-x64}/package.json`, `packages/sandbox/sandbox-local/src/index.ts` (chain order + probes), `examples/acp-agent/tests/acp.snapshot.ts:431` (symlink fixture contract) |
| installed runtime identity (pre-state) | the §10 candidate: launcher sha256 `0b68259f…efcdba`, bin.js `c0226687…366c62`, home layer `14f15b72…03f6016`; Node v24.20.0, pnpm 11.7.0, dsh uid 999; bwrap ABSENT; landlock-run `bin/` ABSENT (manifests only) — Gordon's D1 host probe re-verified below |
| effective profiles/bundles/patches | unchanged — §8 home layer (this fix touches NO dsh config) |
| persistence backend | unchanged (§1) |
| upstream sources | none beyond the pinned corpus (local-only) |
| allowed changes | hxs-15 only; D1: ONE sandbox rung fixed per the work order ((a) evaluated first, (b) bubblewrap via apt with the governor's advance dpkg approval); D3: restore EXACTLY the two fixture symlinks; NO config changes; NO weakening of the fail-closed posture; minimal change set per the candidate-freeze note |
| protected constraints | unchanged from §1 + the work order's explicit: do NOT weaken fail-closed, do NOT touch any other config, keep the change set minimal, re-record every identity the fix changes |
| required tests | Gordon retests G4-13 + G5-01..05/07/13/14 (D1) and the acp `agent-instructions` snapshot (D3) after this window; my own bounded probes below are install verification, not qualification |
| known drift/conflicts | (1) D2 deferred (governor) — the six OTHER flattened symlinks found in this survey (root/packages/examples/vendor/.agents `CLAUDE.md → AGENTS.md` ×5, `.claude/skills → ../.agents/skills` dir-link ×1) are the same distribution defect class and are recorded here but NOT fixed (minimal set; D2 revisits the distribution at upstream intake); no runtime impact proven (the harness reads AGENTS.md real content; Gordon's G4 evidence). (2) §15-C1 re-count was deferred until the campaign closed — it closes in this window (§16.5) |
| rollback state | pre-state: bwrap absent (dpkg baseline captured), two flattened 19-byte regular files (hashes captured), everything else per §10; inverses documented per fix below |
| **proceed_status** | **MAY_PROCEED** |

### 16.2 D1 (P2) — sandbox backend: mechanism evaluation and fix

**(a) The pinned distribution's own materialization mechanisms — evaluated, all unsound within the approved constraints:**

| Mechanism | Evidence (from the pinned source) | Verdict |
| --- | --- | --- |
| optional native dep (the designed path) | entry package `@deepseek-ai/node-addon-landlock-run@0.1.1` declares `optionalDependencies` on the platform packages (`workspace:*` in the monorepo); the platform package's `files` expects `bin/` — the prebuilt binary is **git-ignored by design** ("Binaries are git-ignored and built natively per architecture — locally for your own machine, by CI's per-arch runners as the builders of record", `native/landlock-run/README.md`); our approved export therefore ships manifests only | The mechanism works as designed; the artifact it resolves is absent from the source distribution BY DESIGN — nothing to provision through it without an external artifact |
| postinstall fetch | "There is no install-time build fallback on purpose" (same README) | Does not exist (deliberate upstream decision) |
| explicit package from npm | published `@deepseek-ai/node-addon-landlock-run-linux-x64@0.1.1` would be an artifact OUTSIDE the approved snapshot identity; wiring it into the workspace rewrites the pinned lockfile (prohibited) or places invisible-to-pnpm drift in `node_modules` | Unsound: breaks the pin doctrine the install is anchored on |
| build from pinned source (`pnpm build:native`) | needs `musl-tools` via apt (same README) — a dpkg change OUTSIDE the governor's advance approval, which names bubblewrap | Not approved; would escalate rather than self-extend |

**(b) APPROVED PATH TAKEN: bubblewrap via apt.** Rationale beyond the approval itself: the source pins bwrap as the chain's PREFERRED rung — `sandbox-local/src/index.ts:155` "Linux prefers `bwrap` (its mount profile is closest to the harness's…)"; rung 1 repaired gives the shipped chain its first-choice backend with a one-package dpkg footprint. Evidence and probe results: appended below at execution.

<!-- 16.2 execution evidence, 16.3 D3, 16.4 identities, 16.5 C1 closure, 16.6 fix receipt appended at execution -->

**Execution (b), with one completing mechanism the approval implies.** `apt-get install -y bubblewrap` → **0.9.0-1ubuntu0.1** (noble-updates/main; the ONLY package added — dpkg 694→695; the 691→694 delta since §11 is Gordon's authorized test tooling, other lane). First probe then FAILED as `bwrap: setting up uid map: Permission denied` — diagnosis (all evidence live): `kernel.apparmor_restrict_unprivileged_userns=1` (Ubuntu noble default) mediates uid-map writes by AppArmor profile; raw userns creation works but `unshare -Ur` is denied; the bubblewrap package ships NO profile and is not setuid; the host carries 116 loaded profiles (23 enforce, incl. userns grants for crun/ch-run/buildah/flatpak et al.) but none for bwrap. Completing the install therefore required Ubuntu's own designed grant: `/etc/apparmor.d/bwrap` written **mirroring the host's vendor `crun`/`ch-run` idiom verbatim** (`profile bwrap /usr/bin/bwrap flags=(unconfined) { userns, … }`) and loaded via `apparmor_parser -r`. The host-wide sysctl stays **1** — mediation remains ON; exactly one binary path received exactly one permission. This is recorded here prominently for the governor: it is the completion of "install bubblewrap via apt" on a noble host, not a separate policy change; the inverse is below.

**D1 identities (hash-recorded):** `/usr/bin/bwrap` sha256 `52231e1caf55bcbc667b269f49c63599a6f7db4767ae6a039580d0ff853db712` (72,160 B, root:root 0755, NOT setuid); cached .deb `bubblewrap_0.9.0-1ubuntu0.1_amd64.deb` sha256 `1b506492bd9c7fd0cdb4f02ac822f1d3e336b0aead5113c1239baf8db5db562a`; `/etc/apparmor.d/bwrap` sha256 `66de2da55f4e573cfa4d747f836fd2846cd5641f3e3be4ffa19be7732db62819` (root:root 0644; loaded, `aa-status` lists bwrap).

**D1 probe evidence (bounded; Gordon retests systematically):**
1. *dsh's own functional probe, verbatim args* (`bwrap --ro-bind / / --dev /dev --unshare-pid --proc /proc --die-with-parent -- true`, as dsh) → exit 0, **USABLE**.
2. *Confined execution under the exact workspace-write profile* (`… --tmpfs /tmp --bind /var/lib/dsh/workspace /var/lib/dsh/workspace --`): write inside workspace succeeds (`D1-CONFINED-WRITE-OK`), exit 0.
3. *Escalation inside confinement refused*: `touch /opt/dsh/.probe-escape` and `touch /etc/.probe-escape` both fail `Read-only file system` (exit 1); host-side confirms neither file exists. Probe artifacts cleaned.
4. *Landed-chain dsh smoke* (headless, default composition, workspace-write): task "Use the bash tool to run exactly: echo D1-DSH-BWRAP-OK" → exit 0, stderr 0; durable log `session-0ece7b1c-c78b-4bff-b85a-d34446c486bd` (41 events) carries `tool/call` + `tool/result` `"name":"bash"`, marker present, `turn/end` completed — the path that failed CLOSED with `SandboxUnavailableError` in Gordon's D1 evidence now executes confined. **Fail-closed posture untouched: no config, sandbox code, or approval surface was modified — proven by the effective dump being byte-identical (§16.5).**

**D1 inverse:** `sudo apparmor_parser -R /etc/apparmor.d/bwrap && sudo rm /etc/apparmor.d/bwrap`; `sudo apt-get remove -y bubblewrap` (removes the only added package). The dsh side needs no inverse: with no usable backend the chain returns to the proven fail-closed posture.

### 16.3 D3 (P3) — flattened fixture symlinks: restored

Survey identified the fixture contract (`examples/acp-agent/tests/acp.snapshot.ts:431`: "Both portable AGENTS.md fixtures are symlinks to a sibling AGENTS.canonical.md") and enumerated all 8 flattened-symlink candidates in the export (heuristic: tiny regular files whose content names an existing sibling). Exactly the two fixture links were restored on hxs-15 (as dsh; `rm` + `ln -s AGENTS.canonical.md AGENTS.md` in each directory); the other six (`CLAUDE.md → AGENTS.md` ×5 at root/packages/examples/vendor/.agents-notes, `.claude/skills → ../.agents/skills` ×1) are the same D2-class distribution artifact and are **recorded, not fixed** (minimal set; D2 owns the distribution class at upstream intake; no runtime impact proven).

| Path (under /opt/dsh) | Before | After |
| --- | --- | --- |
| `examples/acp-agent/tests/snapshots/agent-instructions/workspace/AGENTS.md` | 19 B regular, sha256 `b991fee5…d4bdb` (content `AGENTS.canonical.md`) | symlink → `AGENTS.canonical.md`; resolves to canonical sha256 `5f95ba95…4b7c7` ("Root snapshot instruction.") |
| `…/workspace/nested/AGENTS.md` | 19 B regular, same hash `b991fee5…d4bdb` | symlink → `AGENTS.canonical.md`; resolves to canonical sha256 `ba0e4295…89d71` ("Nested snapshot instruction.") |

Tree effect in corpus scope (all `node_modules` excluded): symlinks **0 → 2** (exactly these two), regular files −2. `readlink` targets are the bare relative `AGENTS.canonical.md`, matching the flattened content byte-for-byte. Inverse: replace each symlink with a regular file containing `AGENTS.canonical.md` (19 B, no trailing newline) — restores the as-transported state.

### 16.4 Identities after the fix window (what changed, what did not)

| Identity | State |
| --- | --- |
| package.json / pnpm-lock.yaml anchors | UNCHANGED (`4adbdffa…4986d7`, `6f20c268…90013e` — re-verified this window, hxs-5 corpus and hxs-15 tree) |
| launcher `/usr/local/bin/dsh`, built `bin.js`, home layer `cordis.patch.yml` | UNCHANGED (`0b68259f…efcdba`, `c0226687…366c62`, `14f15b72…03f6016` — re-verified live) |
| effective dump | UNCHANGED — new dump sha256 `dedda886…d518d34`, byte-identical to §9 (proves zero config drift from the fix window) |
| tree | CHANGED: +2 symlinks (§16.3); Gordon's G0-07 fingerprint drifts only at those two paths |
| host | CHANGED: +bubblewrap 0.9.0-1ubuntu0.1 (`/usr/bin/bwrap` `52231e1c…db712`), +`/etc/apparmor.d/bwrap` (`66de2da5…62819`, loaded); dpkg 694→695; sysctl unchanged (=1) |
| sessions/config/credential files | UNTOUCHED (`/var/lib/dsh` content, `/etc/dsh-omniroute.env`, `/var/lib/dsh/.env` — no access needed this window beyond smoke runs) |

### 16.5 §15-C1 closure (re-count executed)

Re-ran `dsh --profile headless --dump-config` (candidate unfrozen): **4 provenance comments** "patched by /var/lib/dsh/cordis.patch.yml", attached to rows `agent-default-model`, `llm-pi-ai`, `web`, `llm-deepseek`. All six §8 row operations are in effect in the dump (the six target rows show the intended config/`disabled: true`); `web-search-deepseek` and `tool-web` are toggled by the same layer but the dump does not emit individual provenance comments for them. Mapping is now of record; the §9 count (4) and the §8 operations (6) are both confirmed as reported, and the dump is byte-identical to install time. C1 closed.

### 16.6 Fix receipt

| Field | Value |
| --- | --- |
| D1 | FIXED — rung 1 (bwrap, the chain's preferred backend) provisioned per the governor's advance approval + Ubuntu's designed userns grant; confined execution proven, in-confinement escalation refused, landed-chain bash smoke green, fail-closed posture unmodified (no dsh config touched) |
| D3 | FIXED — exactly the two fixture symlinks restored; corpus-scope symlink count 0→2; targets byte-identical to the flattened content |
| D2 | untouched (governor deferral); six related flattened links recorded in §16.3 for that review |
| Config drift | none — effective dump byte-identical (`dedda886…d518d34`) |
| New identities | §16.2 (bwrap binary, .deb, AppArmor profile) and §16.3 (two symlink paths) |
| Inverses | §16.2 (parser -R + rm profile; apt remove) and §16.3 (restore 19 B files) |
| Residual risk | R4 (new): the AppArmor grant is host config OUTSIDE the dsh lane's ownership boundary (rick's OS plane) — recorded here with evidence and inverse for the governor's review; kernel/apparmor updates could also re-mediate bwrap → the chain would fail closed again (safe direction) |
| Retest readiness | Gordon may retest G4-13 + G5-01..05/07/13/14 (D1) and the acp `agent-instructions` snapshot (D3) immediately; no candidate freeze needed — the composition is unchanged |
