# PILOT-DSH-IMPL-001 — Phase B activation (Morpheus)

| Field | Value |
| --- | --- |
| Task | Phase B (intermediate) family activation on hxs-15: plan/goal/todo/workflow/skill/hooks/guard/jobs/schedule/subagent/preset/bundle/extensions/mcp-client/session-query/lsp/code-runtime/terminal/feedback + client/web + api/sdk surfaces; web frontend build; web profile with OmniRoute-posture bind; systemd decision |
| Agent | Morpheus (dsh lifecycle steward, KDD-0009), third dispatch |
| Work order | KK3 Phase B dispatch 2026-08-28 (state-log row 13: Phase A SIGNED, Phase B RELEASED) |
| Target | hxs-15 (192.168.50.214) — ONLY |
| Executor host | hxs-5 (192.168.50.204), user hxsa |
| Controlling docs | GOAL-DSH-IMPL-001; the approved plan; `03-morpheus-phase-a-install.md` (Phase A record incl. §16 fixes); `04-gordon-phase-a-verdicts.md` |
| Credential handling | unchanged from Phase A (askpass lane, execution-time only, deleted at end; OmniRoute key by mechanism only — zero values anywhere) |

## 1. Knowledge-review receipt (emitted FIRST, Phase B window)

| Field | Value |
| --- | --- |
| goal / work-order ids | GOAL-DSH-IMPL-001; state-log row 13 (Phase A SIGNED — QUALIFIED_WITH_EXCEPTIONS D2-class; Phase B RELEASED); this dispatch |
| target environment | hxs-15 — the signed Phase A candidate + D1/D3 fixes: launcher `0b68259f…efcdba`, bin.js `c0226687…366c62`, home layer `14f15b72…03f6016`, effective dump `dedda886…d518d34`, Node v24.20.0, pnpm 11.7.0, dsh uid 999, bwrap 0.9.0-1ubuntu0.1 + `/etc/apparmor.d/bwrap` (R4, ratified), corpus-scope symlinks 2 |
| arc state read | state-log rows 1–13 (incl. D1/D3 fix row 12, Phase A sign-off row 13); Gordon's `04-gordon-phase-a-verdicts.md` full register |
| Phase-B-pointed blocks noted | **G4-06(b)** corrupted-current-session resume — no headless entry; the web/API path evaluation is in this window (§6). **G2-10 + G5-10** web dist contingencies — in scope now (build:web this window). Gordon's ledger Phase B NOT_RUN rows activate per family below |
| knowledge roots | unchanged identities (§1 of the Phase A record; re-verified this window: plan `d9df4ff2…f3d5`, corpus anchors `4adbdffa…4986d7` / `6f20c268…90013e` MATCH) |
| Phase B source survey (be-great, this window) | `packages/bundle/web-app/cordis.patch.yml` (full web composition); `packages/host/webserver/README.md` + `src/index.ts:61,75,233` (**host schema = `z.union([z.const('127.0.0.1'), z.const('0.0.0.0')])`** — schema-enforced, single listener); `packages/bundle/web-app/src/startup.ts:74-75` (CLI rejects `--host 0.0.0.0`); `apps/web` (= `@deepseek-ai/dsh-web-frontend`, vite → dist); `apps/cli/config/agent-presets/{standard,minimal}` (agent-plane compositions: standard = full coding agent incl. a `tool-web` row; minimal = fixed-prompt + persistent PTY shell); `packages/mcp/mcp-client/README.md` (one plugin instance PER server — no zero-server bridge shape); `packages/lsp/{lsp,lsp-stdio,tool-lsp}` (seam; stdio provider takes a configured server table — "not a language-server catalog or installer"); `packages/hooks/*` (CC/Codex hook bridges — compat paths needing user hook configs); `packages/sdk/server/README.md` (stdio JSON-RPC server; jsonrpc-demo example supplies the cordis.yml app); `packages/api` (typert-gateway row already active since Phase A; apiproxy/connection/api-remotes activate with the web profile) |
| installed runtime identity (pre-state) | as above; web frontend dist ABSENT (Phase A boundary); no web profile; no systemd units for dsh; listeners: none on 3080 |
| effective profiles/bundles/patches (pre-state) | Phase A §8 home layer (six row operations), unchanged |
| allowed changes | hxs-15 only; build:web via the repo's own path (with the documented `DSH_CLIENT_COMMIT_HASH` escape for the `.git`-less tree — Gordon's G1-04 verified mechanism); machine-layer composition additions (home `cordis.patch.yml` — hash re-recorded); a deployment preset under the NATIVE user root `$DSH_HOME/.agent-presets` (never an edit of shipped files); systemd unit(s) if the native shape calls for a service (it now does — the web profile is a long-running listener); an out-of-tree LAN forwarder IF the source bind constraint requires it (it does — see the seam finding §3); NO upstream file edits; NO new apt packages (nothing pre-approved beyond bubblewrap; none needed — the forwarder is Node, already installed) |
| protected constraints | LAN IP primary + loopback, NEVER 0.0.0.0 (the source makes 0.0.0.0 the only schema-valid non-loopback — it stays refused; the CLI flag also rejects it); web-search-* STAY disabled (incl. the standard preset's `tool-web` row — handled natively via a deployment preset, §4); experimental/agent-team/dynamic-plugin surfaces stay absent/disabled (codex/claude-code subagent tool rows stay disabled — cloud-tied external CLIs, local-only doctrine); pwsh stays NOT_APPLICABLE; mcp-client: bridge inventoried, ZERO servers; D2-class deferred items not re-litigated; secrets by mechanism only; fail-closed postures untouched |
| required tests | Gordon Gates 6–7 (authoring in parallel per row 13); my bounded activation smokes are install verification, not qualification |
| known drift/conflicts | **C-1 (work order vs source, RESOLVED within authority):** the work order mandates LAN-IP-primary bind; the shipped webserver schema accepts ONLY `127.0.0.1` or `0.0.0.0` — LAN-IP direct bind is natively impossible and 0.0.0.0 is boundary-prohibited. Resolution: native loopback bind + out-of-tree HX TCP forwarder on the LAN IP (extension doctrine: out-of-tree over upstream edits; no new packages). Recorded with evidence in §3; the governor may later prefer nginx (needs dpkg approval) or an upstream schema change (next intake). **C-2:** the shipped standard preset mounts `tool-web` (web-search-* surface) — resolved natively via a user-root deployment preset minus that row (§4), never an edit of the shipped preset |
| rollback state | pre-state = the signed Phase A candidate (identities above) + no dist + no web service; inverses per step in §7 |
| **proceed_status** | **MAY_PROCEED** |

<!-- Sections: 2 build:web · 3 bind posture + systemd decision · 4 composition changes (machine layer + hx preset) · 5 per-family activation records · 6 G4-06(b) evaluation · 7 rollback/inverses · 8 effective-config receipt + activation smokes · 9 updated identities · 10 candidate handoff (Gates 6-7) · 11 command log · 12 risks/open items -->
## 2. Web frontend build (deferred from Phase A; the repo's own path)

- Command (as `dsh`, `HOME=/home/dsh`): `DSH_CLIENT_COMMIT_HASH=b150a551b8d465e31e418e1b2eaf5e79bbb7d28e pnpm run build` — the FULL aggregate (`build:lib` incremental + `build:web` vite + client build record), using the documented commit-hash escape for the `.git`-less tree (identical mechanism to Gordon's verified G1-04 scratch run; the pinned baseline commit is the anchor value, never a fabricated one).
- Result: **exit 0**; vite built in 2.58 s; `build: recorded 200 client artifact(s) with 1 public value(s)` — the same 200-artifact count Gordon recorded on his scratch copy.
- Artifacts: `/opt/dsh/apps/web/dist/` (114 files: `index.html`, `assets/`, `favicon.svg`, `manifest.webmanifest`); client build record `/opt/dsh/.dsh-build/client-build-environment.json`. The dsh-web-app bundle resolves the dist as an assembly fact (never user config).
- Closes the Phase-B-pointed contingencies **G2-10** and **G5-10** (dist now exists; Gordon retests at Gate 7).

## 3. Bind posture + systemd decision (the source finding and the resolution)

**Source finding (C-1):** the shipped webserver's bind schema is `host: z.union([z.const('127.0.0.1'), z.const('0.0.0.0')]).required()` (`packages/host/webserver/src/index.ts:75`, single `server.listen(port, host)` at :233) — ONLY loopback or wildcard, single listener; the CLI flag separately rejects `--host 0.0.0.0` with a safety error (`packages/bundle/web-app/src/startup.ts:74-75`); the webserver README owns the posture ("No TLS, auth, or origin policy — binding a non-loopback address exposes the server to that network"). **A direct LAN-IP bind is natively impossible, and 0.0.0.0 is boundary-prohibited.**

**Resolution (out-of-tree, no upstream edits, no new packages):** dsh binds native loopback; an HX-owned forwarder provides the LAN face.

| Layer | Listener | Evidence |
| --- | --- | --- |
| `hx-dsh-lan-forward.service` (out-of-tree TCP pipe, Node, `/usr/local/libexec/hx-dsh-lan-forward.mjs` root:root 0755, sha256 `bb618566…32cd0`) | **192.168.50.214:3080** (LAN primary) → 127.0.0.1:3080 | `ss` line of record; journal "listening 192.168.50.214:3080 -> 127.0.0.1:3080" |
| `dsh-web.service` (`dsh web --no-open --trusted-host 192.168.50.214:3080`) | **127.0.0.1:3080** (native loopback) | `ss`; journal "dsh web: http://127.0.0.1:3080" |
| wildcard | **NONE** | `ss` sweep: no `0.0.0.0:3080` |

- **Management/UI access posture (proposal of record):** LAN + loopback only, exactly mirroring the accepted OmniRoute posture; no TLS/auth native (upstream v1 limitation, README-owned); the `/api` browser-trust fence (`api-request-trust.ts`: Host must be loopback or a declared authority, WHATWG-normalized, DNS-rebinding defense) is the reachability policy — `--trusted-host 192.168.50.214:3080` declares exactly the LAN authority. Fence evidence: index 200 via LAN AND loopback (identical 14,555 B), dist asset 200, trusted-authority `/api/` passes the fence (404 route-absent), **bogus `Host: evil.example.com` → 403 on BOTH faces**. Anything beyond LAN+loopback (TLS termination, auth proxy, exposure past the LAN) STOPS for the owner — not requested, not built.
- **systemd decision — services ARE the native shape now (Phase A's recorded upgrade path taken):** the web profile is a long-running listener, so the CLI shape gains two units: `dsh-web.service` (User=dsh, `EnvironmentFile=/etc/dsh-omniroute.env` — the governor-staged file consumed DIRECTLY by systemd as designed, `WorkingDirectory=/var/lib/dsh/workspace`, `Restart=on-failure`, enabled) and `hx-dsh-lan-forward.service` (User=dsh, After/Wants=dsh-web, enabled). The `/var/lib/dsh/.env` copy remains for CLI invocations (Gordon's headless path); both mechanisms reference the same staged file, zero values in any artifact. **Correction caught by my own smoke:** the unit's first form had no WorkingDirectory — `host.describe` reported `cwd:"/"`, which would have made the sandbox-policy default workspace the filesystem root; fixed before any session ran, re-proven (`cwd:"/var/lib/dsh/workspace"`). Unit hashes: dsh-web `4e659cd5…6c53` (supersedes `85702454…d5ab`), forwarder `c3257852…257ca`.
- **Forwarder rationale:** TCP-level pipe (HTTP, `/api` SSE, WebSocket upgrades all flow as bytes; no TLS termination, no header rewriting — the fence still sees the original Host). Alternatives recorded for the governor: nginx/caddy via apt (needs new dpkg approval), or an upstream schema change at next intake (D2-class distribution conversation). ~30 lines, syntax-checked (`node --check`), hash-recorded, runs as dsh (no new privilege).

## 4. Composition changes (all via the machine layer + the native preset root; zero shipped-file edits)

`/var/lib/dsh/cordis.patch.yml` (root:root 0644; **hash changed** `14f15b72…03f6016` → `d4ac2f19…40f83f`; Phase A rows byte-preserved, verified in the dump):

1. `session-query-sqlite` config → `path: !!js dshHomePath('session-query.sqlite')`, `openAt: first-search` — session-query family activated: durable, local full-text index (upstream posture `:memory:`+`never` kept through Phase A; the web-app bundle's restatement is overridden by this later layer, provenance comment of record).
2. `agent-presets` config → `default: hx-standard` — the default agent-plane roster entry becomes the HX deployment preset.
3. INSERT `schedule` (`@deepseek-ai/dsh-schedule`) + `time-context` (`@deepseek-ai/dsh-time-context`) — the schedule family (durable reminders; upstream's official Web-overlay pattern), both from the shipped CLI closure.

**HX deployment preset** (`/var/lib/dsh/.agent-presets/hx-standard/`, root:root 0644, the NATIVE user preset root — never an edit of the shipped `standard`): `agent.cordis.yml` sha256 `56c71037…9eb0` = the shipped standard composition minus exactly its `tool-web` row (223-byte block, removal asserted programmatically; 15 top-level rows vs 16) — keeps web-search-* disabled inside web sessions, where the shipped default would have mounted the model-facing web tool against a disabled backend; `preset.yml` sha256 `c5b863c8…4677` (name "HX Standard", order 0). Shipped `standard`/`minimal` presets remain installed and selectable.

**Deliberately NOT mounted (recorded postures):** `mcp-client` — its grammar is one plugin instance PER server with required `serverName`/`transport`/target; there is no zero-server bridge shape, so the bridge stays inventoried in the CLI closure with ZERO instances (no concrete local target this phase, per the work order). `lsp` — `lsp-stdio`'s schema requires `servers` with **at least one entry** (README §Configuration) and no language server exists on hxs-15; installing one is an unapproved dependency addition → seam stays unmounted, mount recipe of record in §5. `hooks` (CC/Codex bridges) — compatibility paths that need a user's Claude Code/Codex hook config; none exists (cloud-tied external CLIs, local-only doctrine) → surface inventory only. `codex`/`claude-code` subagent tool rows — stay `disabled: true` in the preset (shipped default; cloud-tied; the optional provider Bundles are not installed). `web-search-*` — rows stay disabled everywhere (base + web-app + preset). `experimental/agent-team`, dynamic-plugin surfaces — absent from all compositions. `pwsh` — NOT_APPLICABLE (platform-gated rows remain correctly disabled on Linux).

## 5. Per-family activation records

| Family | Disposition | What was mounted/configured | Evidence |
| --- | --- | --- | --- |
| plan | ACTIVE (web: per-session preset realm) | `plan-mode` group in hx-standard preset (isolate realm); host row stays disabled per web-app design | dump §8; preset file hash §4 |
| goal | ACTIVE (already host-active Phase A; web Remote endpoints) | goal service/driver/command (base, host plane) + `tool-goal` per session (preset) | dump rows; §4 |
| todo | ACTIVE | `tool-todo` per session (preset; base host row disabled per web-app design) | preset hash §4 |
| workflow | ACTIVE | `workflow-worker-thread` + `tool-workflow` in preset delegation realm; `ui-workflow-run` client module | dump; preset §4 |
| skill | ACTIVE | skill registry (host) + `skill-filesystem` + `tool-skill` per session (preset); `ui-skill` module | dump; preset §4 |
| hooks | AVAILABLE_DISABLED | bridge packages in tree; zero instances (no CC/Codex hook configs; cloud-tied CLIs not installed) | §4 reasoning; hooks READMEs |
| guard | ACTIVE (since Phase A) | `repeat-tool-reminder` + `tool-call-timeout-policy` (base rows) | dump rows (Phase A §9) |
| jobs | ACTIVE | jobs registry (host) + `tool-jobs` per session (preset); `ui-jobs` module | dump; preset §4 |
| schedule | ACTIVE (this window) | `dsh-schedule` + `dsh-time-context` inserted at machine layer | dump lines 540-543; §4 |
| subagent | ACTIVE (spawn/fork); codex/claude-code AVAILABLE_DISABLED | registry + spawn/fork providers (host); delegation tools per session (preset); external-CLI rows stay disabled | dump; preset §4; local-only reasoning §4 |
| preset | ACTIVE | roster `agent-presets` row, default `hx-standard`; user root populated; shipped presets intact | dump line 534-539; §4 |
| bundle | ACTIVE (mechanism) | bundle patch layers resolve and compose (base + web-app + home); `dsh plugin` management available | dump provenance comments |
| extensions (Cordis runtime) | ACTIVE (since Phase A) | loader/hmr(include/timer) runtime is the composition engine itself; client-hmr idle row in web profile | dump rows |
| mcp-client | SURFACE INVENTORY (bridge, zero servers) | package in CLI closure; no instance mountable without a concrete server | §4 reasoning |
| session-query | ACTIVE (this window) | sqlite index durable at `$DSH_HOME/session-query.sqlite`, `openAt: first-search` | dump lines 89-93; §4 |
| lsp | AVAILABLE_DISABLED | seam packages built; `lsp-stdio` requires ≥1 configured language server, none on host; mount recipe: insert `dsh-lsp` + `dsh-lsp-stdio` with a `servers` entry (`command` + `extensionToLanguage`) + `dsh-tool-lsp` in the preset | §4 reasoning; lsp-stdio README §Configuration |
| code-runtime | ACTIVE | `code-runtime-worker-thread` mounted by BOTH the headless and web-app bundles | dump (both profiles) |
| terminal | ACTIVE (preset-mounted) | `dsh-terminal` (PTY) + `terminal-bash` stack ships in the `minimal` preset's persistent-shell realm; node-pty backend built (allow-listed) | minimal preset file; Phase A install |
| feedback | ACTIVE | `command-feedback` (base) + `message-feedback` + `ui-message-feedback` (web profile) | dump rows |
| client (~40 ui-*) + apps/web + packages/web | ACTIVE | full web-app browser roster (34 client rows in the dump) over built dist | dump; §2; serve evidence §8 |
| api | ACTIVE | typert-gateway (base, since Phase A) + `api-gateway` (apiproxy) + `connection` (/api bridge + WS downlinks) + `api-remotes` (web profile) | dump; RPC proof §8 |
| sdk | ACTIVE (surface) | `dsh-jsonrpc-agent` built bin boots an external cordis.yml (`$DSH_CORDIS_CONFIG`/argv) — compositions are consumer/Gordon fixtures (Phase A precedent: his scratch compositions); the omniroute route is registered and available to any composition; sdk protocol/server/client packages built | sdk README; built artifacts |

## 6. G4-06(b) evaluation (corrupted-current-session resume — the web/API path)

The headless CLI has no resume entry (Gordon's G4-06(b), BLOCKED-by-design in Phase A). The web/API path DOES carry the resume shape: sessions are durable roots (Phase A G4 evidence: restart durability, kill-drill prefix parse), the web host lists existing sessions from the persisted projection (sidebar/projection-cache) and opening one continues it through the same agent-loop; the persistence backend's fail-loud contact rules for corrupt artifacts were Gordon's own G4 findings (valid zstd frame + corrupt JSONL inside → boot and a fresh session proceed; extension/compression mismatch rejected loud). The corrupted-CURRENT-session resume case therefore has a native entry to test at Gate 7 (web session open → continue), with the fail-loud behaviors already dispositioned. No extra configuration was required; the path activates with the web profile. Gordon owns the verdict.

## 7. Rollback / inverses (Phase B window)

- Services: `sudo systemctl disable --now hx-dsh-lan-forward.service dsh-web.service`; `sudo rm /etc/systemd/system/{hx-dsh-lan-forward,dsh-web}.service /usr/local/libexec/hx-dsh-lan-forward.mjs`; `sudo systemctl daemon-reload`.
- Composition: restore the Phase A home layer (content of record at `14f15b72…03f6016`, Phase A doc §8) over `/var/lib/dsh/cordis.patch.yml`; `sudo rm -rf /var/lib/dsh/.agent-presets`.
- Build artifacts: dist + client build record are additive; removal (`sudo -u dsh rm -rf /opt/dsh/apps/web/dist /opt/dsh/.dsh-build`) restores the Phase A artifact state (web boot then fails loud with the documented build instruction — the Phase A posture).
- Session-query index: `sudo rm -f /var/lib/dsh/session-query.sqlite*` (created on first search).
- Phase A surfaces (headless, CLI, seam) are untouched by every inverse above; the web profile directory (`/var/lib/dsh/profiles/web`) is regenerable auto-init state.

## 8. Effective-config receipt + activation smokes

**Effective-config receipt (web profile):** `dsh --profile web --dump-config` (as dsh) → exit 0, 543 lines, 0 stderr; **sha256 `e5e0e5371bb99cec83ef036795c02ace8a5fcb72e4d055565d5a472de0711b38`**. Layer provenance of record: 6 "patched by /var/lib/dsh/cordis.patch.yml" comments — 5 over `@deepseek-ai/dsh-base` rows (llm-pi-ai, agent-default-model, session-query-sqlite, web, llm-deepseek) + 1 over the `@deepseek-ai/dsh-web-app` row (agent-presets). Verified in the dump: session-query `path`/`openAt: first-search`; `default: hx-standard`; `schedule` + `time-context` inserted; `web`/`web-search-deepseek`/`tool-web`/`llm-deepseek` all `disabled: true`; the full 34-row browser roster; zero secret values (apiKeyEnv names only). Headless-profile dump after the layer change: exit 0 (regression-clean; hash in §11 log).

**Activation smokes (bounded install verification; Gordon qualifies at Gates 6–7):**

1. Boot: both units `active`; journal shows `dsh web: http://127.0.0.1:3080` and the forwarder line; zero warnings/errors since start; 0 failed units.
2. Bind posture: §3 table — LAN primary + loopback, no wildcard; fence: trusted authority admitted, bogus authority **403 both faces**.
3. Serve: index 200 via LAN (from hxs-5) AND loopback — byte-identical 14,555 B SPA shell with the module-loader boot payload; dist asset 200.
4. Real RPC through the LAN face + fence: `POST /api/host.describe` (envelope learned from the validator's own bad-request diagnostics) → `ok:true`, `provider:"omniroute"`, `model:"ollama-local/hx-qwen3.6-coderx-64k:latest"`, `home:"/home/dsh"`, `cwd:"/var/lib/dsh/workspace"` (after the WorkingDirectory correction), `attachedSessions:0`. This is the wire path Gordon's Gate 7 builds on; envelope of record: `{"type":"client-request","rpcId":"<string>","method":"<ns.method>","payload":{…}}` → `{"type":"server-response","rpcId":…,"result":{"ok",…}}`.
5. Headless regression under the new layer: see §11 (ran after the doc body was drafted — result inlined there and in §9 identities).

<!-- §9 identities, §10 handoff, §11 command log, §12 risks appended at completion -->
## 9. Updated identities (Phase B window)

| Identity | Value | Change |
| --- | --- | --- |
| package.json / pnpm-lock.yaml anchors | `4adbdffa…4986d7` / `6f20c268…90013e` | UNCHANGED |
| launcher `/usr/local/bin/dsh` / built `bin.js` | `0b68259f…efcdba` / `c0226687…366c62` | UNCHANGED |
| home layer `/var/lib/dsh/cordis.patch.yml` | `d4ac2f191cda7980ee79db45248546e0349015ea392719b1f96a65155b40f83f` | CHANGED (Phase B rows added; Phase A rows byte-preserved) |
| effective dump — WEB profile | `e5e0e5371bb99cec83ef036795c02ace8a5fcb72e4d055565d5a472de0711b38` | NEW (receipt §8) |
| effective dump — headless profile | `6f52cd6d296098e1c8c0e35df51dc1b737511ddef517113f5184a14ce17fdf39` | CHANGED (same layer; Phase A path regression-clean) |
| hx-standard preset | agent.cordis.yml `56c710375f9b41c44cac8c2cf6e388f09abc5d627f7751a95a382b9e66c89eb0`; preset.yml `c5b863c84dbb51513d9545a58b3afc6acba236cff1f91587c2699bd2e2084677` | NEW |
| frontend dist `/opt/dsh/apps/web/dist` | 114 files; client build record `/opt/dsh/.dsh-build/client-build-environment.json` (200 artifacts, 1 public value) | NEW |
| forwarder `/usr/local/libexec/hx-dsh-lan-forward.mjs` | `bb6185660dbdc5bff8762607a5db095ce4d2e538bfe534e26fab29a15d632cd0` | NEW |
| `dsh-web.service` | `4e659cd5b0a75f3d88defe87938161417a130d892766bdf21fa45d55554b6c53` (supersedes `85702454…d5ab` — WorkingDirectory correction §3) | NEW |
| `hx-dsh-lan-forward.service` | `c32578526596229763b444790b8bf7690a15112e6a257737c35f5da62db257ca` | NEW |
| listeners | 192.168.50.214:3080 (forwarder) + 127.0.0.1:3080 (dsh); NO 0.0.0.0 | NEW |
| sandbox backend | bwrap 0.9.0-1ubuntu0.1 + `/etc/apparmor.d/bwrap` (R4) | UNCHANGED |
| `/var/lib/dsh/.env`, `/etc/dsh-omniroute.env` | both `596ea242…80cc` (mechanism only) | UNCHANGED/UNTOUCHED |

## 10. Candidate handoff — Morpheus → Gordon, Gates 6–7 (OPEN until the governor cites it)

| Item | Value |
| --- | --- |
| Candidate | dsh 0.1.1-rc.2 Phase B on hxs-15: Phase A signed baseline + web UI + Phase B families per §5 |
| Entry paths | headless CLI (unchanged, regression-clean); **web UI `http://192.168.50.214:3080`** (LAN) and `http://127.0.0.1:3080` on-host; `/api` Typert bridge on both (fence: loopback + declared LAN authority only); sdk `dsh-jsonrpc-agent` bin + external cordis.yml |
| Services | `dsh-web.service`, `hx-dsh-lan-forward.service` (enabled, active, Restart=on-failure); journald owns logs (`journalctl -u dsh-web`); headless invocations unchanged (`sudo -n -u dsh env HOME=/home/dsh dsh …`) |
| Composition | home layer `d4ac2f19…40f83f` (Phase A rows + §4 additions); web dump `e5e0e537…71b38`; headless dump `6f52cd6d…17fdf39`; hx-standard default preset (`56c71037…9eb0`) minus tool-web; shipped presets intact |
| RPC envelope (for Gate 7 fixtures) | `POST /api/<ns.method>` body `{"type":"client-request","rpcId":"<string>","method":"<ns.method>","payload":{}}` → `{"type":"server-response","rpcId",…,"result":{"ok",…}}`; WS downlinks `/api/events.mux` + `/api/events.host` (upgrade; plain GET → 426); fence needs `Host:` = loopback authority or `192.168.50.214:3080` |
| New-testable surfaces | web session lifecycle (preset-mounted agent plane: bash/fs/jobs/skill/goal/plan/todo/subagent/workflow/ralph per §5), schedule tools (schedule_create/list/delete + time-context), session-query content search (durable index, first-search open), feedback (message + command), storage (json/domain), session-log export, directory picker, settings/credentials RPC plane (privileged method set pinned server-side), terminal stack (minimal preset), G4-06(b) web-resume path (§6), G2-10/G5-10 dist now present |
| Staying disabled/absent | web-search-* (all compositions), llm-deepseek, codex/claude-code subagent tools, mcp servers (zero), lsp backends (mount recipe §5), hooks bridges (no targets), experimental/agent-team, dynamic plugins, pwsh, 0.0.0.0 binds |
| Defect channel | defects route to Morpheus; no config changes by Gordon; key VALUE never in any artifact (mechanism: `/var/lib/dsh/.env` for CLI, `EnvironmentFile` for the service) |
| Watch items for Gates 6–7 | (i) schedule tools act on LIVE ROOT agents — headless one-shots and web sessions qualify; (ii) session-query sqlite file materializes on FIRST search; (iii) the forwarder is protocol-agnostic TCP — WS/SSE behave identically to loopback; (iv) `standard` preset (shipped) still mounts tool-web against a disabled backend — by design it is NOT the default; if a test selects it deliberately, expect loud search failures, not a defect of the HX posture |

Handoff state: **OPEN** — the governor cites on acceptance; defects to Morpheus; retest through Gordon only.

**Pointer (appended 2026-08-28T21:2xZ, post-outage freeze window):** all §9/§10 identities re-verified MATCH on hxs-15, EXCEPT the headless-dump row, which is SUPERSEDED per the OPEN CORRECTION in §13.1 (new value `c88664a8…ded4e`; byte-exact record-artifact explanation in §13.3). Refreshed identities with full hashes: §13.2.

## 11. Sanitized sequential command log (Phase B window)

All local commands as hxsa@hxs-5; remote as hxsa@hxs-15 (askpass execution-time credential; `sudo -n` on-host). No secret values in any row.

| Seq | UTC | Where | Command (sanitized) | Exit |
| ---: | --- | --- | --- | --- |
| 1 | 14:4x | hxs-5 | Read state log rows 1-13, Gordon verdicts; be-great survey: web-app bundle, webserver schema/startup, presets, mcp/lsp/hooks/sdk/schedule sources | 0 |
| 2 | 15:0x | hxs-5 | Emit knowledge-review receipt (§1) → MAY_PROCEED; recreate askpass lane (smoke → 10) | 0 |
| 3 | 14:55 | hxs-15 | **MUTATION** `DSH_CLIENT_COMMIT_HASH=b150a551… pnpm run build` (as dsh) → exit 0; dist 114 files; 200 client artifacts recorded | 0 |
| 4 | 15:0x | hxs-5 | Stage artifacts: home layer (YAML ok), hx-standard preset (tool-web block removal asserted), forwarder (`node --check` remote), 2 units | 0 |
| 5 | 15:0x | hxs-15 | **MUTATION** install home layer (root 0644), hx-standard preset (root 0644), forwarder (root 0755), units (root 0644); hashes recorded; pre-state hash captured first | 0 |
| 6 | 15:0x | hxs-15 | `dsh --profile web --dump-config` (as dsh) → exit 0, 543 lines; receipt hash `e5e0e537…`; all Phase B rows + disabled postures verified | 0 |
| 7 | 15:03 | hxs-15 | **MUTATION** `systemctl daemon-reload`; `systemctl enable --now dsh-web hx-dsh-lan-forward` → both active; journal clean | 0 |
| 8 | 15:0x | hxs-5/15 | Bind evidence: ss (LAN+loopback, no wildcard); curl LAN index 200 = loopback 200 (14,555 B); dist asset 200; fence bogus-Host → 403 both faces; trusted → pass | 0 |
| 9 | 15:0x | hxs-5 | RPC probe `/api/host.describe` → ok:true, provider omniroute, model coder-x; FOUND cwd:"/" (unit defect) | 0 |
| 10 | 15:07 | hxs-15 | **MUTATION** unit corrected (+WorkingDirectory=/var/lib/dsh/workspace), daemon-reload, restart; re-probe → cwd fixed; new unit hash | 0 |
| 11 | 15:1x | hxs-15 | Headless regression: dump exit 0 (`6f52cd6d…`); smoke "PHASE-B-REGRESSION-OK" exit 0, stderr 0 | 0 |
| 12 | 15:2x | hxs-5/15 | Write this record; cleanup askpass + scratch (both hosts, verified) | 0 |

## 12. Risks and open items

- **R5** — The LAN face is an HX out-of-tree forwarder, not an upstream bind (C-1): if the governor prefers a distro proxy (nginx/caddy — needs dpkg approval) or an upstream schema change (next intake), the swap is contained to `hx-dsh-lan-forward.service`. The forwarder carries no TLS/auth — same trust plane as the upstream v1 (README-owned limitation); anything beyond LAN+loopback stops for the owner.
- **R6** — The web `/api` privileged method set (settings/credentials plane) is reachable by any LAN client that presents the trusted authority — the fence is a reachability policy, not authentication (upstream decision record). This is the accepted LAN-boundary posture (owner rule: the LAN is the exposure boundary); flagging for the owner's visibility at cutover.
- **R7** — hx-standard is a derived preset: when the shipped `standard` changes at an upstream intake, the HX copy must be re-derived (the derivation is a 223-byte asserted removal, re-runnable; recorded §4).
- **Open** — lsp activates the day an owner-approved language server exists on hxs-15 (recipe §5). hooks/mcp activate the day a concrete local target exists. Chat-X model declaration remains open from Phase A.
- **Deferred (unchanged):** D2 class; R1 advisory debt; codex/claude-code providers (cloud-tied).

`PASS — PHASE B CANDIDATE ACTIVE; HANDOFF OPEN (Morpheus does not certify own work)`

## 13. Post-outage fresh freeze + headless-dump hash OPEN CORRECTION (2026-08-28T21:2xZ) — labeled, append-only

Work order: KK3 issue 2026-08-28 (state-log row 24; Assignment Packet A via Mia): (1) fresh freeze on hxs-15 against the §9/§10 identity set; (2) explain the headless-dump hash record gap (state-log row 16) with discriminating evidence; (3) record both append-only here. Bounds honored: hxs-15 only; executor hxs-5 as hxsa (askpass lane: 0700 helper reading the governed credential-record row at execution time only, SSH_ASKPASS_REQUIRE=force, StrictHostKeyChecking=yes, sudo -n on-host; helper deleted and verified absent at end); non-mutating to configuration, services, and the tree — the only writes were dsh's own constant profile-root rewrites at `/var/lib/dsh/profiles/*/cordis.yml` (mechanism of record in §13.3-F1; mtimes 21:19:49Z/21:19:50Z) plus transient `/tmp` scratch on both hosts (removed, verified absent). No service was down; nothing mismatched beyond the known headless row, so no stop/escalate condition triggered.

### 13.1 OPEN CORRECTION — §9 row "effective dump — headless profile" (and its §10 reference)

- **Recorded value** `6f52cd6d296098e1c8c0e35df51dc1b737511ddef517113f5184a14ce17fdf39` (§9 and §11 seq 11) is **SUPERSEDED** by **`c88664a83a87f00106b81c8153d273713cc9addbb9b9efd5b13bc19d1b5ded4e`** (full hash, re-baselined this window).
- **Reason:** invocation/record artifact at §11 seq 11 — the hashed byte stream was the dump's 76-byte stderr warning line merged ahead of its stdout (a `2>&1`-class capture), not the dump alone. Byte-exact proof in §13.3-F3. The dump CONTENT at 15:1x was already the correct Phase B composition — the same stdout bytes that hash `c88664a8` today; only the recorded hash described the wrong stream.
- The §10 composition row's "headless dump `6f52cd6d…17fdf39`" reference is superseded by the same value.
- **Original 15:1x capture bytes: unrecoverable** (§11 seq 12 cleanup removed the scratch dumps) — stated plainly per the work order. The explanation is bounded to mechanism + reproduction attempts; the governor's ruling of record (mechanism-level explanation plus labeled re-baseline to the content-verified current dump SUFFICES) is satisfied with margin, because one reproduction landed byte-exact.
- Nothing else in §9/§10 changes; every other identity re-verified MATCH in the fresh freeze (§13.2).

### 13.2 Fresh freeze (2026-08-28T21:18–21:24Z, hxs-15; hash values are full sha256)

[wording correction 2026-08-28, labeled per the append-only rule: this heading originally read "all values sha256 in full" — only the hash values are full sha256; the table also carries non-hash values (file counts, service states, listeners). Original wording preserved here.]

| Identity | Value | Verdict |
| --- | --- | --- |
| `/opt/dsh/package.json` anchor | `4adbdffa373754a048a214c5de3ec0671ac6e1f3c1521ec5b37e8fad1a4986d7` | MATCH |
| `/opt/dsh/pnpm-lock.yaml` anchor | `6f20c268e76df1294c16f016ab10a7fa1271608b4db0f4fafe8f7c21ec90013e` | MATCH |
| launcher `/usr/local/bin/dsh` | `0b68259fb4e95869689ef680a781d82bf0b0a95a50ba9bc1a03243b852efcdba` | MATCH |
| built `/opt/dsh/apps/cli/lib/bin.js` | `c0226687bb20f45c603ec6fe50f3de16d1c3510c3a803304ec575ef9bc366c62` | MATCH |
| home layer `/var/lib/dsh/cordis.patch.yml` | `d4ac2f191cda7980ee79db45248546e0349015ea392719b1f96a65155b40f83f` | MATCH |
| hx-standard `agent.cordis.yml` | `56c710375f9b41c44cac8c2cf6e388f09abc5d627f7751a95a382b9e66c89eb0` | MATCH |
| hx-standard `preset.yml` | `c5b863c84dbb51513d9545a58b3afc6acba236cff1f91587c2699bd2e2084677` | MATCH |
| frontend dist `/opt/dsh/apps/web/dist` | 114 files | MATCH |
| client build record `/opt/dsh/.dsh-build/client-build-environment.json` | `7dd6b82094c89bc90452adaac0b641906461d133d2f449db174dd1e5f566ec8f` (214 B) | RECORDED (first full hash of record for this file) |
| forwarder `/usr/local/libexec/hx-dsh-lan-forward.mjs` | `bb6185660dbdc5bff8762607a5db095ce4d2e538bfe534e26fab29a15d632cd0` | MATCH |
| `dsh-web.service` | `4e659cd5b0a75f3d88defe87938161417a130d892766bdf21fa45d55554b6c53` | MATCH |
| `hx-dsh-lan-forward.service` | `c32578526596229763b444790b8bf7690a15112e6a257737c35f5da62db257ca` | MATCH |
| service state | both units enabled + active; `NRestarts=0` ×2; ActiveEnterTimestamp 2026-08-28T16:34:37Z both (post-boot auto-recovery); 0 failed units host-wide | MATCH |
| listeners | `127.0.0.1:3080` (dsh) + `192.168.50.214:3080` (forwarder); wildcard `:3080` count 0 | MATCH |
| sandbox backend | bubblewrap 0.9.0-1ubuntu0.1 (only dpkg add of record); `/usr/bin/bwrap` `52231e1caf55bcbc667b269f49c63599a6f7db4767ae6a039580d0ff853db712`; `/etc/apparmor.d/bwrap` `66de2da55f4e573cfa4d747f836fd2846cd5641f3e3be4ffa19be7732db62819`, loaded (`aa-status` lists `bwrap`) | MATCH |
| key mechanisms (hashes only — NEVER values) | `/var/lib/dsh/.env` `596ea242e3105f2d49a562dfcf72624c97a112676aec90c51fd46bec521680cc`; `/etc/dsh-omniroute.env` `596ea242e3105f2d49a562dfcf72624c97a112676aec90c51fd46bec521680cc` | MATCH |
| `dsh --version` | 0.1.1-rc.2 | MATCH |
| **effective dump — headless profile** | **`c88664a83a87f00106b81c8153d273713cc9addbb9b9efd5b13bc19d1b5ded4e`** — run twice, identical both runs (373 lines) | **RE-BASELINE (supersedes §9 row per §13.1)** |
| effective dump — web profile | `e5e0e5371bb99cec83ef036795c02ace8a5fcb72e4d055565d5a472de0711b38` — run twice, identical both runs (543 lines) | MATCH |
| dump idempotency / sensitivity | identical hashes across repeats per profile; identical from `cwd=/`; identical with a bogus `DSH_CLIENT_COMMIT_HASH` set | PROVEN |
| profile root anchors `/var/lib/dsh/profiles/{headless,web}/cordis.yml` | both `c300dcf2ebc5f02062d6591268d29d3db6fe45e0cb138f5467276fe2ba06076e` — byte-identical to each other (mechanism: §13.3-F1) | MATCH |

Headless-dump content re-verified by me this window (reproducing the governor's row-16 check): diff vs the Phase A evidence dump (`dedda886…d518d34`, held in Gordon's evidence) shows EXACTLY the documented Phase B additions — session-query `path: !!js dshHomePath('session-query.sqlite')` + `openAt: first-search` with its fifth provenance comment, and the `schedule` + `time-context` inserts; `apiKeyEnv: OMNIROUTE_API_KEY` name only; zero secret values.

### 13.3 Hash-gap explanation (mechanism + discriminating evidence)

**F1 — hypothesis (a) "stale composed-profile cache" is ruled out by construction: no composition cache exists in the dump path (source-cited).** `runDumpConfig` (`apps/cli/src/dump-config.ts:30-52`) reads every patch layer fresh at invocation (`loadOptionalPatches`/`loadOverlayPatches` → `readFileSync`). `prepareProfile` (`apps/cli/src/profile-boot.ts:98-103`) REWRITES `profiles/<name>/cordis.yml` with the constant empty-root anchor (`profile-boot.ts:60-64`) on EVERY invocation, dump or boot — the vendored Loader can otherwise bake composed rows into it, and the rewrite is the deliberate guard. `renderConfigDump` (`packages/boot/app-boot/src/index.ts:379-442`) then composes over that constant root and renders; it reads no state besides the layer files. Byte proof: a locally computed sha256 of the source constant equals `c300dcf2ebc5f02062d6591268d29d3db6fe45e0cb138f5467276fe2ba06076e` — exactly the live hash of BOTH profile roots on hxs-15. Their byte-identity to each other is by construction (same constant), not by composition convergence. Refinement of record for state-log row 19: those two files are the constant root anchor rewritten per invocation, not "composed profile caches"; the governor's byte-identity observation stands, the label is corrected.

**F2 — at 15:1x the dump's stdout was already the correct Phase B composition.** The home layer `d4ac2f19…40f83f` was installed at §11 seq 5 (15:0x); the seq-6 web dump (`e5e0e537…71b38`, re-verified byte-identical this window) proves the layer was in effect from 15:0x. With no cache (F1), unchanged render code (`bin.js` `c0226687…366c62`, MATCH), and unchanged layer files (all MATCH), any genuine `dsh --profile headless --dump-config` at 15:1x had to emit exactly the stdout bytes that hash `c88664a8…ded4e` today. The recorded `6f52cd6d…17fdf39` therefore described different BYTES, never a different composition.

**F3 — those bytes are byte-exactly identified: the seq-11 hash was computed over a merged stdout+stderr capture (hypothesis (b), PROVEN).** Since Phase B, every headless dump emits a 76-byte stderr warning BEFORE the stdout write: `dsh: [/var/lib/dsh/cordis.patch.yml] patch: entry "agent-presets" not found` — the home layer's `agent-presets` patch (§4 row 2, `default: hx-standard`) has no target row in the headless composition (that row exists only via the web-app bundle), and `renderConfigDump`'s documented warn path reports unmatched patches during composition, before `process.stdout.write` emits the dump (`app-boot/src/index.ts:424-441`, `dump-config.ts:51`). Reproduction this window: `sha256( <that warning line> + <current canonical dump> )` = **`6f52cd6d296098e1c8c0e35df51dc1b737511ddef517113f5184a14ce17fdf39`** — EXACTLY the recorded §11 seq-11 value. The current dump's own stderr is exactly this one line (76 bytes, verified ×2). So the 15:1x hash measured a `2>&1`-class capture (warning first, dump second), while the content I verified and asserted regression-clean was the stdout — which was then, and is now, the correct Phase B composition.

**F4 — alternatives ruled out with evidence.** `--dump-default-config` (bundle layers only) hashes `a0a0e9f380872097cb7f8b7356f36433a2afeb8de5044a9e63d4ed47b4bee9f5` live — identical to Gordon's Phase A G2-03 evidence file (bundle layers unchanged), ≠ `6f52cd6d`. A home-less scratch-`DSH_HOME` headless dump (fresh template profile layer, no home layer) was predicted and observed to equal the same `a0a0e9f3…` (an empty profile patch layer is render-invisible) and carries the shipped `deepseek-official/deepseek-v4-flash` default model — the discriminator a home-less dump would have shown; it is not the observed composition. Unknown profile names fail loud (`dsh: profile "…" does not exist`), so no wrong-profile dump can exist. Byte transforms of the canonical dump — CRLF `e513e149…653c`, extra trailing newline `db041099…e293`, stripped trailing newline `7d05a3d0…1571`, stderr SUFFIXED `f833484a…03f4` — none matches `6f52cd6d`. Hypothesis (c) dump non-determinism is REFUTED: identical hashes ×2 per profile in my window (and ×2 in the governor's), insensitive to cwd and to the commit-hash env; the dump path does not even load the layered environment (`bin.ts:45-48` never calls `loadLayeredEnv`), so there is no env input to drift.

**F5 — why only the headless row was affected.** The web composition contains the `agent-presets` row (web-app bundle), so the home-layer patch matches, no warning is emitted (0 stderr), and the seq-6 web hash was clean stdout — it matched then and matches now. The headless composition lacks the row, so only headless dumps carry the warning, and only the headless seq-11 hash captured it. **Datum for Gates 6–7:** this warning is benign and upstream-designed (`parsePatchList`: an unmatched patch in a shared overlay "stays a per-entry Loader warning, so one overlay shared across surfaces does not have to match every tree"); it will appear on every headless `--dump-config` stderr until/unless the row is split — recorded so it is not mistaken for a defect, and so future dump hashing always separates stdout from stderr.

**Re-baseline:** the §9 headless-dump identity is re-baselined to `c88664a83a87f00106b81c8153d273713cc9addbb9b9efd5b13bc19d1b5ded4e` — content-verified by the governor (row 16) and re-verified by me (§13.2 diff); idempotent and environment-insensitive (§13.2, F4).

### 13.4 Second Brain disposition (standing directive)

(1) Opportunity identified: none new beyond the Phase A §13 record (session stores + dump discipline as future substrates). (2) The applicable pattern is the existing one: evidence-first receipts with hash identities — this window extended it with a byte-exact artifact explanation. (3) Disposition: deferred as before (Carol frozen by owner directive); the corrected mechanism facts (constant profile-root anchor; unmatched-patch warning on headless dumps) are recorded here for the catalog when Carol unfreezes. (4) Evidence: this section and §13.2–13.3.

### 13.5 Sanitized sequential command log (this window)

All local commands as hxsa@hxs-5; remote as hxsa@hxs-15 (askpass execution-time credential; StrictHostKeyChecking=yes; sudo -n on-host). No secret values in any row; key material touched by hash only.

| Seq | UTC | Where | Command (sanitized) | Exit |
| ---: | --- | --- | --- | --- |
| 13 | 21:0x | hxs-5 | Read state log rows 14–24 (full), governor row-16 detail; be-great mechanism survey of the pinned source: `dump-config.ts`, `profile-boot.ts`, app-boot `index.ts`/`profile.ts`, `args.ts`, `bin.ts`; local sha256 of the profile-root constant → `c300dcf2…6076e` (later confirmed live) | 0 |
| 14 | 21:1x | hxs-5 | Re-verify knowledge-root identities (plan `d9df4ff2…f3d5`, corpus anchors `4adbdffa…4986d7`/`6f20c268…90013e` — all MATCH); hash Gordon evidence dumps (Phase A headless dump = `dedda886…d518d34` confirmed) | 0 |
| 15 | 21:17 | hxs-5 | Create askpass helper (0700, execution-time credential row read); extraction smoke `\| wc -c` → 10 | 0 |
| 16 | 21:17 | hxs-15 | SSH + `sudo -n` smoke: hostname hxs-15, SUDO_OK | 0 |
| 17 | 21:1x | hxs-15 | Fresh freeze reads: all §9/§10 identities, service state (`enabled`/`active`, NRestarts 0 ×2), listeners (LAN+loopback, wildcard count 0), bwrap + AppArmor presence/hashes, key-mechanism hashes only — all identities MATCH (exception of record: the headless profile was RE-BASELINE at this seq — baseline reset, not identity drift) | 0 |
| 18 | 21:1x | hxs-15 | Dumps ×2 per profile: headless `c88664a8…ded4e` ×2 (373 lines, 5 provenance comments, 76-byte stderr warning), web `e5e0e537…71b38` ×2 (543 lines, 6 comments, 0 stderr); sensitivity re-proofs (cwd=/, bogus commit-hash env → identical); `--dump-default-config` datum `a0a0e9f3…`; profile-root re-hash post-dump (constant, mtimes recorded) | 0 |
| 19 | 21:2x | hxs-15 | Reproductions: scratch-`DSH_HOME` headless dump = `a0a0e9f3…` (predicted, home-less discriminator confirmed); unknown-profile dump fails loud; byte transforms — stderr-PREFIXED capture = `6f52cd6d…17fdf39` EXACT (record gap explained); CRLF/extra-newline/stripped/stderr-suffixed transforms all ≠ | 0 |
| 20 | 21:2x | hxs-5/15 | Fetch current dump to hxs-5; diff vs Phase A evidence dump = exactly the documented Phase B additions; zero secret values confirmed; cleanup: remote scratch + repro home + local copy removed (verified absent); profile roots re-verified constant | 0 |
| 21 | 21:2x | hxs-5 | Askpass helper deleted (verified absent, no residue); write §13 + §10 pointer (append-only); `python3 scripts/validate.py` → 4/4 PASS | 0 |

`PASS — POST-OUTAGE FREEZE COMPLETE; HEADLESS-DUMP ROW CORRECTED OPENLY (append-only); HANDOFF REMAINS OPEN (Morpheus does not certify own work)`
