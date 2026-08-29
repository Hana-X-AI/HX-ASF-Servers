# PILOT-DSH-IMPL-001 — Phase C Prep: Candidate Seams & Activation

**Order:** 09a (rescoped from work order 09)
**Issuer:** Flash (governor), 2026-08-29
**Executor:** Morpheus (dsh lifecycle steward)
**Model:** `omniroute/qwen3.8-2.4t-a95b` (Qwen 3.8 2.4T A95B, provider DeepInfra, via OmniRoute hxs-8) — CLI-verified live 2026-08-29
**Parent records:** 03 Phase A prep (interop/activation), 05 Phase B prep (testing/validation/rollback framework)
**Corpus path (read-only):** `/opt/tkv-local/deepseek-harness-master`

---

## Purpose

Per the [Phase C prep plan — PILOT-DSH-IMPL-001] section "Phase C Scope" (Gates 8–10):

This product provides, for each activation candidate identified in Phase A/Gate 7:

1. **Exact source seams** from the pinned harness corpus (`file:line`).
2. **Activation mechanism** on the native composition layer (cordis class + pattern), matching the Phases A/B template: `patch-interop`, `patch-sandbox`, `deploy-remote`.
3. **Host prerequisites** for each seam and its deployment target.
4. **Risk classification** from the Phase B taxonomy (`RISK_*`).

This document also supplies **read-only testability notes for Gordon's Gate 8–10 authoring**, stating what is provable on hxs-15's frozen corpus, and what is BLOCKED-by-design (no candidate mutation).

---

## Product families (Gates 8–10 scope)

Each family maps to a Phase C gate cluster from the plan:

| Gate range | Family           | Purpose                                  |
| ---------- | ---------------- | -------------------------------------- |
| Gates 8a   | interop          | Cross-seam coordination & injection     |
| Gates 8b   | sandboxing       | Harness-level isolation & capability caps |
| Gates 9    | remote           | Remote endpoint + model discovery        |
| Gates 10   | experimental     | Feature-flagged experimentation layer     |

---

## Family 1: I/O interop (Gates 8a)

**Scope:** the plan's `interop`/`acp` family — programmatic I/O transports: the
ACP automation server, the out-of-process ACP subagent client, the MCP client
bridge, and the external-hook bridges (all four carried from Phase B with
"Phase C interop pointer" dispositions).

### Source seams

| Seam ID | Location (pinned corpus) | Role |
| --- | --- | --- |
| SEAM-INT-01 | `packages/acp/acp/src/index.ts:43-45` (plugin export: `name = 'acp'`, `inject = ['agents']`), `:71-82` (`AcpConfig` schema: optional `provider` / `model`; runtime-only `stream` test override), `:121` (`apply(ctx, config)` opens an `AgentSideConnection` on stdin/stdout) | Automation-only ACP **server**: JSON-RPC stdio; fresh agents per client; text/image prompts; committed-output delivery; one-shot permission resolution; cancellation |
| SEAM-INT-02 | `examples/acp-agent/cordis.yml` (runnable composition: llm adapter row, `sandbox-local` + `sandbox-policy` + `subprocess` + `bash-sandbox` + `approval`, demo app row `acp-agent` at line 53, fs/subagent/hooks rows) + root `package.json:144` (`demo:acp` → `node --import tsx packages/examples/acp-demo/src/bin.ts --config examples/acp-agent/cordis.yml`) | Composition of record that boots the server; documents stdout-is-protocol-frames (no logger/HMR) and the `DSH_PERMISSION_MODE` override |
| SEAM-INT-03 | `packages/subagent/subagent-acp/src/index.ts:27-32` (Config: required `command` — executable spawned per run), `:66-68` (`command: z.string().required()`), `:147` (capability caps: no `outputSchema`/`depthLimit`/`toolFilter`/`persona`), `:155-162` (spawn via `ctx.subprocess.spawn`), `:173` (`apply`) | Out-of-process ACP **client** — the matching subagent provider (per `packages/acp/README.md`: server here, client there) |
| SEAM-INT-04 | `packages/mcp/mcp-client/README.md` (one plugin instance PER server; required `serverName`/`transport`/target; no zero-server bridge shape) | MCP bridge — Phase B SURFACE INVENTORY, zero servers; carried into Phase C |
| SEAM-INT-05 | `packages/hooks/hooks-claude-code/`, `packages/hooks/hooks-codex/` (contract evidenced in `examples/acp-agent/cordis.yml` hooks rows: `configPath` read once at server-launch cwd; missing file registers nothing; separate dialect files) | CC/Codex hook bridges — Phase B AVAILABLE_DISABLED, no hook configs on host |

### Activation mechanism

Cordis class: **patch-interop** (per the work-order template).

1. **ACP server = separate-process composition, not a profile row.** Stdout is
   reserved for protocol frames (`packages/acp/acp/README.md`), so the server
   cannot mount inside the headless/web CLI profiles. HX activation follows the
   Phase B sdk pattern (composition launched by its app bin over an external
   `cordis.yml`): an HX-authored composition = the `examples/acp-agent` shape
   with the llm row **swapped from the shipped `llm-deepseek`/`deepseek-official`
   default to the landed `omniroute` route** (config-layer change, never a code
   edit), plus `provider: omniroute` + `model: <catalogued fleet id>` on the
   `acp` row — both required for a runnable composition (README: "The runnable
   ACP composition requires both").
2. **ACP subagent client = machine-layer INSERT row** (Phase B
   `schedule`/`time-context` precedent): INSERT `- id: subagent-acp` /
   `name: '@deepseek-ai/dsh-subagent-acp'` into `/var/lib/dsh/cordis.patch.yml`
   with `command:` = the ACP server launch line; it registers beside the
   landed spawn/fork providers. A preset row exposes it to sessions.
3. **mcp-client / hooks** stay target-gated (Phase B disposition): mount
   recipes of record — one `mcp-client` row per concrete local server; hooks
   rows with `configPath` pointing at a governed hooks file (missing file =
   no-op by design, so rows may be staged before a target exists).

### Host prerequisites

- **No new apt packages.** Node v24.20.0, pnpm 11.7.0, built tree
  (`apps/cli/lib/bin.js` + demo bins), dsh uid 999 — all landed Phase A/B.
- **ACP server:** a resolvable provider/model route (omniroute present since
  Phase A, credential by reference `OMNIROUTE_API_KEY`); a dsh-writable cwd for
  session persistence (`persistenceRoot` in the composition).
- **subagent-acp:** the spawn target must exist and be executable — the source
  probes the path and fails loud rather than falling back (spawn EACCES/ENOENT
  handling, `src/index.ts:90-128`); child processes run through
  `ctx.subprocess` as dsh (no new privilege).
- **Daemon state:** none new — ACP is one-shot stdio per client connection; no
  listener is introduced (contrast with Family 3).

### Risk classification

Taxonomy derivation (of record): no prior document enumerates `RISK_*` codes;
they are derived here from the Phase A/B risk register (03 §14 R1–R4, 05 §12
R5–R7, 05 §16.6 R4): RISK_ADVISORY_DEBT (R1), RISK_ANCHOR_PROVENANCE (R2),
RISK_MODEL_BEHAVIOR (R3), RISK_HOST_POLICY_GRANT (R4),
RISK_OUT_OF_TREE_COMPONENT (R5), RISK_TRUST_PLANE (R6),
RISK_DERIVED_ARTIFACT_DRIFT (R7).

| Seam | Code | Rationale |
| --- | --- | --- |
| SEAM-INT-01/-02 | RISK_MODEL_BEHAVIOR | Live prompt/image/permission/cancel flows over ACP exercise fleet-model tool behavior that Gates 3–7 only smoke-proved; qualification is new surface. |
| SEAM-INT-01 | RISK_TRUST_PLANE | `session/request_permission` lets the automation client answer approvals automatically (README protocol table) — the policy boundary moves from operator to client code. |
| SEAM-INT-03 | RISK_OUT_OF_TREE_COMPONENT | A spawned child process with its own cwd/credentials reference extends the process boundary; source mitigates with loud spawn validation, but host-side command identity is ours to manage. [OPEN CORRECTION 2026-08-29, labeled, append-only — review batch 2, F20: the risk code originally read `RISK_OUT_OF_TREE_COMPONENT-adjacent`, which is not an enum code of record; corrected to the `RISK_OUT_OF_TREE_COMPONENT` code with the "adjacent" character retained in this rationale.] |
| SEAM-INT-02 | RISK_DERIVED_ARTIFACT_DRIFT | The HX ACP composition is a derivation of the shipped example (route swap); it must be re-derived at every upstream intake (R7-class). |
| SEAM-INT-04/-05 | RISK_ADVISORY_DEBT (baseline) | No activation risk until a target exists; inherited upstream advisory exposure applies to any mounted server/bridge. |

---

## Family 2: Sandbox activation (Gates 8b)

**Scope:** the plan's `sandboxing` family — harness-level confinement for shell
and filesystem execution: the runner-selection chain in `sandbox-local`, the
session policy plane in `sandbox-policy`, the sandbox-consuming `bash-sandbox`
executor, and the write-fencing `fs-sandbox` backend. All four already have
rows in the landed hxs-15 composition (Phase A/B); this family documents the
seams and the rung-2 activation question (landlock).

### Source seams

| Seam ID | Location (pinned corpus) | Role |
| --- | --- | --- |
| SEAM-SBX-01 | `packages/sandbox/sandbox-local/src/index.ts:2` (doc: "selects the platform runner chain (Linux bwrap then landlock)… Missing or unusable confinement fails closed"), `:67-69` (functional bwrap probe: cached `spawnSync('bwrap', …, '--', 'true')`), `:141` (`SelectedRunner = 'bwrap' \| 'landlock' \| 'seatbelt' \| 'windows-acl'`), `:159-165` (`PLATFORM_CHAINS`: `linux: ['bwrap', 'landlock']`, `darwin: ['seatbelt']`, `win32: ['windows-acl']` — probes arbitrate only when a platform has >1 candidate), `:325` (`selectRunner(policy.mode)`), `:338-339` (argv construction per runner), `:492-495` (fail-closed: `selectedRunner === 'unavailable'` → `throw new SandboxUnavailableError(mode)`) | Runner-selection and confinement launch core of `sandbox-local` |
| SEAM-SBX-02 | `packages/sandbox/sandbox-local/src/index.ts:31-33` (landlock launcher imported from external addon `@deepseek-ai/node-addon-landlock-run`), `:116-134` (test-seam overrides: platform/chain/probe replacement points), `:265` (cached probe verdict) | Landlock rung (chain position 2 on Linux) + the test-override seams Gordon exercises |
| SEAM-SBX-03 | `packages/sandbox/sandbox-local/src/index.ts:40` (`windows-acl` import), `:94-98` (windows-acl probe docs: win32-only); package at `packages/sandbox/sandbox-windows-acl/` | Windows restricted-token runner — **NOT_APPLICABLE on Linux**: the `win32` chain is selected by platform first and is never probed on a Linux host (platform-chain table, `:159-165`). N/A evidenced, not assumed. |
| SEAM-SBX-04 | `packages/sandbox/sandbox-policy/README.md` (single owner of `ctx.sandboxPolicy`; modes `read-only` [fail-safe default] / `workspace-write` / `danger-full-access`; `resolve({session?,mode?})` precedence: explicit grant > session `sandbox/mode` event fold > default; session cwd is the immutable workspace root; per-session override = one log-only `sandbox/mode` event via `setSandboxMode`; invariant companion rejects forged mode events) | Session policy plane — decides WHICH mode the runner enforces |
| SEAM-SBX-05 | `packages/shell/bash-sandbox/README.md` (sandbox-consuming bash executor; load INSTEAD of `bash-local`, together with sandbox-local + sandbox-policy; fail-closed structured `SANDBOX_UNAVAILABLE` — never silent unconfined execution; denial dialects EROFS/bwrap, EACCES/landlock, EPERM/seatbelt; deny-only at this seam, approval lives in the tool layer; reference YAML block carries the three composition rows) | Bash execution path that consumes SEAM-SBX-01/-04 |
| SEAM-SBX-06 | `packages/fs/README.md` backend table (`fs-sandbox` extends `fs-local`, registers `ctx.fs`, fences write/edit by per-call mode + root; tools unchanged across backends) | Filesystem write fencing (read paths unaffected) |

### Activation mechanism

Cordis class: **patch-sandbox** (per the work-order template).

1. **Rung 1 (bwrap) — already ACTIVE.** The landed hxs-15 composition rows
   (`sandbox-local` + `sandbox-policy` + `bash-sandbox` + `fs-sandbox`) resolve
   to `bwrap` as first chain candidate on Linux; the Phase A D1 fix landed
   `bubblewrap 0.9.0-1ubuntu0.1` plus the `/etc/apparmor.d/bwrap` policy grant
   (RISK_HOST_POLICY_GRANT retired for rung 1). No further mutation needed —
   Phase C Gate 8b is verification of an active rung, not activation.
2. **Rung 2 (landlock) — DEFERRED, approval-gated.** Landlock is not a config
   row: the launcher comes from the external addon `@deepseek-ai/node-addon-landlock-run`
   (SEAM-SBX-02) and its prebuilt binary is git-ignored in the corpus (built
   per-arch by upstream CI, per the Phase A record). Activating rung 2 means
   either building the addon from source (musl-tools toolchain) or admitting an
   external prebuilt artifact — both are provenance decisions under
   RISK_ANCHOR_PROVENANCE / pin doctrine and require explicit approval before
   any mutation. It is fallback-only anyway (chain order `['bwrap', 'landlock']`).
3. **windows-acl — NOT_APPLICABLE.** Platform selection is by-platform-first
   (`PLATFORM_CHAINS`, `:159-165`); the `win32` chain is unreachable on the
   Linux hxs-15 host. Documented as evidence-backed N/A, no action.
4. **Policy plane — configuration layer only.** Mode selection flows through
   `sandbox-policy` (`read-only` default); any per-session escalation is a
   log-only `sandbox/mode` event that the invariant companion validates against
   forgery. HX posture: keep `read-only` default; `workspace-write` grants only
   via governed preset rows, `danger-full-access` never without separate owner
   approval (profile §3 prohibitions).

### Host prerequisites

- **Nothing new for rung 1:** bubblewrap + apparmor profile landed Phase A
  (D1); Node v24.20.0 / pnpm 11.7.0 / built tree / dsh uid 999 from Phase A/B.
  Landlock kernel support (Ubuntu 24.04 ships LSM landlock) is present but
  unused until rung 2 is approved.
- **Rung 2 (if ever approved):** musl-tools for a from-source addon build, OR a
  pinned, hash-verified external artifact admission path (neither exists today —
  this is the open item, not a landed prerequisite).
- **Daemon state:** none — confinement is per-spawn, no listener introduced.

### Risk classification

| Seam | Code | Rationale |
| --- | --- | --- |
| SEAM-SBX-01 (rung 1) | RISK_HOST_POLICY_GRANT (retired state) | The apparmor/bwrap grant was the Phase A D1 risk; landed and verified — Gate 8b re-proves it read-only. |
| SEAM-SBX-02 (rung 2) | RISK_ANCHOR_PROVENANCE | Landlock activation requires a from-source build or an external prebuilt artifact; both need provenance/pin approval before any mutation. |
| SEAM-SBX-03 | — (NOT_APPLICABLE) | Platform-chain table makes the win32 runner unreachable on Linux; no risk surface on this host. |
| SEAM-SBX-04 | RISK_TRUST_PLANE | Mode escalation is a single log-only event; the invariant companion is the only forgery defense — its behavior is qualification-worthy. |
| SEAM-SBX-05/-06 | RISK_MODEL_BEHAVIOR | Denial dialects (EROFS/EACCES/EPERM) surface to the model as tool errors; fleet-model behavior under structured `SANDBOX_UNAVAILABLE` is new qualification surface. |

---

## Family 3: Remote endpoint deployment (Gate 9)

**Scope:** the plan's `remote` family — the E2B remote-runtime POC
(`packages/e2b/`): one filesystem/process execution world relocated to an E2B
Linux sandbox behind two OS adapters (`ctx.fs`, `ctx.subprocess`). HX
doctrine for this family is **local-only**: Gate 9 proves the local posture of
the seam (source identity, fail-closed key handling, absence from shipped
compositions) and does NOT activate a cloud endpoint. Activation of any remote
endpoint requires explicit owner word; until then every row here stays absent.

### Source seams

| Seam ID | Location (pinned corpus) | Role |
| --- | --- | --- |
| SEAM-RMT-01 | `packages/e2b/README.md` (family map: `e2b` → `ctx.e2b` lifecycle owner; `fs-e2b` → `ctx.fs`; `subprocess-e2b` → `ctx.subprocess`; consumers `bash-local`/`terminal-bash`/`lsp-stdio` "need no E2B-specific forks" — they delegate to `ctx.fs`/`ctx.subprocess`; boundary: harness process, cordis objects, model calls, session state/persistence, skills stay HOST-side) | Family boundary definition — what a remote endpoint would and would not move |
| SEAM-RMT-02 | `packages/e2b/e2b/src/index.ts:44-45` (`apiKey?: string` — "omission reads `E2B_API_KEY`"; never forwarded into the sandbox), `:94` (`config.apiKey ?? process.env.E2B_API_KEY`), `:140-141` (fail-closed: empty key → `throw new Error('dsh-e2b: configure apiKey or set E2B_API_KEY')`); `packages/e2b/e2b/package.json:39` (`"e2b": "2.29.1"` — pinned SDK) | Sandbox lifecycle owner + credential seam (reference-only: field name `apiKey` / env reference `E2B_API_KEY`; no value exists anywhere in HX records) |
| SEAM-RMT-03 | `packages/e2b/e2b/README.md:9-23` (config block: `cwd` absolute POSIX default `/home/user/workspace`; `timeoutMs` default 300000, expiry deletes sandbox), `:25-29` (setup verifies `.dsh-e2b` state dir is a real directory, mode `0700`; disposal deletes sandbox; `SandboxNotFoundError` accepted as quiescence; provider plugins must load after owner and dispose before it) | Lifecycle contract: create-once / delete-on-timeout-or-disposal; ephemeral by design |
| SEAM-RMT-04 | `packages/e2b/fs-e2b/README.md` (implements `dsh-fs` provider contract; no config of its own; load after `dsh-e2b`, in place of `dsh-fs-local`; remote identity via GNU `realpath -mz`; atomic publish via same-fs rename; limitations: no host synchronization, host-process-local mutation coordination, default-Linux-image assumptions), plus `packages/fs/README.md` backend table (cross-link recorded in Family 2, SEAM-SBX-06) | Filesystem adapter over the remote endpoint |
| SEAM-RMT-05 | `packages/e2b/e2b/README.md:39-44` Known Limitations: not a whole-harness runtime; sandbox state ephemeral (no reconnect/pause/templates/volumes/snapshots); **no deployment platform configured** (network policy, host-workspace sync, discovery all out of scope); "`cwd` is a resolution convention, not containment" | POC maturity record — the direct basis for DEFERRED_BY_POLICY |

### Activation mechanism

Cordis class: **deploy-remote** (per the work-order template).

1. **Mechanism of record (if ever authorized):** mount the three composition
   rows from `packages/e2b/e2b/README.md:9-21` (`e2b` lifecycle owner first,
   then `subprocess-e2b` and `fs-e2b` replacing the local adapters) into the
   target composition via a `patch-interop`-shaped INSERT — activation is
   config-layer; credential supplied ONLY by env reference (`E2B_API_KEY`) or
   the `apiKey` field pointing at a governed secret reference; a literal key
   value is prohibited in any dump, patch, or log (profile §3).
2. **Current disposition: DEFERRED_BY_POLICY.** No activation row is staged.
   HX local-only doctrine (plan Phase C): Gate 9 proves local posture —
   source identity of the seam, fail-closed behavior on absent credentials
   (`:140-141`), and continued absence of e2b rows from every shipped/landed
   composition. Activating any remote endpoint requires explicit owner word
   plus a separate approval covering egress policy and secret provisioning.
3. **Model-discovery note (Gate 9 pairing):** remote execution does not change
   the model route — LLM requests remain host-side (SEAM-RMT-01 boundary), so
   the omniroute row is untouched by this family.

### Host prerequisites

- **Nothing to install on hxs-15 for Gate 9** — the posture proof is
  source-read-only (absence checks + fail-closed reading). No e2b SDK account,
  key, or network egress is provisioned; none exists today.
- **If ever authorized (future, gated):** an E2B account + API key provisioned
  by reference only; egress policy approval for the host→E2B controller path;
  acceptance of ephemeral state (no snapshots/volumes in the pinned POC).
- **Daemon state:** none now; an activated endpoint would add an outbound SDK
  connection (no local listener), bounded by `timeoutMs`.

### Risk classification

| Seam | Code | Rationale |
| --- | --- | --- |
| SEAM-RMT-02 | RISK_HOST_POLICY_GRANT | Activation is a new external-egress grant plus a cloud credential — both separately approved surfaces (profile §3). |
| SEAM-RMT-01/-03 | RISK_TRUST_PLANE | Execution moves to an external controller whose image/network policy HX does not govern ("`cwd` is a resolution convention, not containment"; base-image network policy retained). |
| SEAM-RMT-05 | RISK_DERIVED_ARTIFACT_DRIFT | Pinned `e2b@2.29.1` SDK + POC-scoped adapters will drift against upstream platform changes; re-derivation needed at every intake if ever activated. |
| SEAM-RMT-04 | RISK_MODEL_BEHAVIOR | Remote file/tool latency and error mapping (`FsError` vocabulary over controller failures) change model-visible behavior versus local backends. |
| All | (doctrine guard) | DEFERRED_BY_POLICY: no row staged, no key material, no egress — Gate 9 is a local posture proof only. |

---

## Family 4: Experimental layer (Gate 10)

**Scope:** the plan's `experimental` family — `packages/experimental/`:
private, release-excluded prototypes that run on the real runtime
(`experimental/README.md`: "use the repository's real runtime without joining
an official release… no stability or support promise"). Two packages:
`agent-team` (the domain: roster/mailbox/DAG, `ctx.agentTeams`) and
`tool-agent-team` (scoped model-facing tools). HX disposition:
EXPERIMENTAL_LAB_ONLY — verified ABSENT from every shipped/landed composition
(Phase A/B), stays absent; activation is a separately-approved surface
(profile §3: experimental teams require separate approval).

### Source seams

| Seam ID | Location (pinned corpus) | Role |
| --- | --- | --- |
| SEAM-EXP-01 | `packages/experimental/README.md` (family charter: private packages, no stability promise, retain full engineering/security/lifecycle requirements; subtree `AGENTS.md` owns dependency isolation, release exclusion, promotion) | Family governance seam — release exclusion is upstream's own rule |
| SEAM-EXP-02 | `packages/experimental/agent-team/README.md:9-18` (config block: `maxMembers: 8`, `maxTasks: 256`, `maxPendingMessagesPerMember: 64`, `maxMessageBytes: 65536`, `disposalTimeoutMs: 5000` — every limit a positive safe integer), `:22` (requires Agent, Session, Session persistence, and continuable-subagent services; "A composition without durable Session storage does not activate it"), `:26-28` (implicit Lead: every runtime root is Lead of the Team whose `TeamId` = its `SessionId`; teammates are named continuable direct children; provisioning is durable and crash-safe), `:52` (`./invariant` companion replays candidate Team events against the committed Session prefix and rejects forged/invalid transitions before append) | Agent Teams domain service — implicit-root roster, durable peer mailbox, shared task DAG |
| SEAM-EXP-03 | `packages/experimental/README.md:10` (`tool-agent-team`: scoped model-facing Agent Teams tools and collaboration guidance; no ctx key of its own) | Model-facing tool surface over SEAM-EXP-02 |
| SEAM-EXP-04 | `packages/experimental/agent-team/README.md:70-76` Known Limitations: one process / one shared checkout (no worktree, merge, or fs lock); advisory `writeScopes` are hints, not locks — Bash and direct writers bypass them; flat immutable roster; no automatic ownership release; mailbox not cross-process exactly-once | Maturity record — the basis for the lab-only disposition |

### Activation mechanism

Cordis class: **patch-interop**-shaped config-row INSERT (the only mechanism —
no daemon, no endpoint), but the operative control is the approval gate, not
the mechanism:

1. **Current disposition: ABSENT, no row staged.** Verified in Phase A/B that
   no shipped composition and no landed hxs-15 composition carries an
   `agent-team` row; Gate 10 re-proves that absence read-only.
2. **Activation recipe of record (only if separately approved):** INSERT an
   `agent-team` row (config block per SEAM-EXP-02) into a dedicated lab
   composition — never into the production/landed profile — with the four
   prerequisite services present (Agent, Session, durable Session persistence,
   continuable-subagent; the package refuses activation without durable
   storage, `:22`). `tool-agent-team` mounts beside it for the model surface.
3. **Approval chain:** owner word first (profile §3 lists experimental teams
   among separately-approved-only surfaces), then a bounded lab task overlay;
   the subtree's own promotion rules (`experimental/AGENTS.md`) govern any
   eventual move out of `experimental/` — HX does not edit upstream core to
   shortcut that.

### Host prerequisites

- **Nothing new on hxs-15.** The landed stack already satisfies every runtime
  prerequisite the package demands (Agent/Session/persistence/continuable
  services are the core composition) — the blocker is policy, not host state.
- **No daemon state** — Teams state lives in Session logs (durable events), so
  activation adds no listener; concurrency is single-process by design
  (SEAM-EXP-04: concurrent harness processes over one Team are unsupported).

### Risk classification

| Seam | Code | Rationale |
| --- | --- | --- |
| SEAM-EXP-02 | RISK_MODEL_BEHAVIOR | Multi-agent peer traffic (user-role `Team message` injections, cold-resume wakeups) is wholly new fleet-model behavior; nothing in Gates 3–7 exercised it. |
| SEAM-EXP-02/-03 | RISK_TRUST_PLANE | Teammates are continuable children with tool access in a SHARED cwd; advisory `writeScopes` do not fence (SEAM-EXP-04), so the coordination plane is the only isolation. |
| SEAM-EXP-01 | RISK_OUT_OF_TREE_COMPONENT-adjacent | Private, release-excluded, no stability promise — mounting it means depending on a surface upstream itself labels non-production. |
| SEAM-EXP-02 | RISK_ANCHOR_PROVENANCE | Experimental subtree has its own promotion/isolation rules; any HX pinning of it must survive upstream reshuffles without a release contract. |
| All | (doctrine guard) | EXPERIMENTAL_LAB_ONLY: stays absent from landed compositions; activation requires owner word + separate approval per profile §3. |


## Testability matrix (Gordon's Gate 8–10 authoring reference)

Scope rule: the candidate on hxs-15 is FROZEN while Gordon's campaign runs.
PROVABLE = verifiable read-only against the frozen corpus/host (source reads,
presence/absence checks, static schema inspection, `--dump-config` row
inspection without executing the candidate). BLOCKED-by-design = requires
candidate mutation or running the candidate. Host-status reads (package
presence, kernel features) go through the governor, never via candidate touch.

| Family | Seam ID | Provability | BLOCKED-by-design? | Rationale |
| ------ | ------- | ----------- | ------------------ | --------- |
| interop | SEAM-INT-01 | PROVABLE | No | Read pinned source: plugin export/`inject` at `:43-45`, `AcpConfig` schema at `:71-82`, stdio connection at `:121`. |
| interop | SEAM-INT-02 | PROVABLE | No | Read `examples/acp-agent/cordis.yml` row shape + `package.json:144` demo script existence. Booting the server / client handshake = candidate execution → BLOCKED-by-design. |
| interop | SEAM-INT-03 | PROVABLE | No | Read required `command` config + spawn-validation source `:27-32/:155-162`; absence of an ACP server spawn target on host is a read-only presence check. Live spawn = candidate execution → BLOCKED. |
| interop | SEAM-INT-04 | PROVABLE | No | README contract (one instance per server) + absence of any MCP server target on host — both read-only. Mounting a live bridge = activation → BLOCKED. |
| interop | SEAM-INT-05 | PROVABLE | No | Absence of hook config files on host is read-only (Phase B AVAILABLE_DISABLED posture). Registering live hooks = activation → BLOCKED. |
| sandbox | SEAM-SBX-01 | PROVABLE | No | Read `PLATFORM_CHAINS` (`:159-165`) and fail-closed throw (`:492-495`); bwrap binary + apparmor grant presence is a host-status read via governor (Phase A D1). A live confined run = candidate execution → BLOCKED. |
| sandbox | SEAM-SBX-02 | PROVABLE (posture) | Partial | Absence of a landlock addon binary in-tree is a read-only corpus check (git-ignored, built per-arch). Activating rung 2 = mutation + provenance approval → BLOCKED-by-design AND by policy. |
| sandbox | SEAM-SBX-03 | PROVABLE (as N/A) | No | Platform-chain table + host `uname` (via governor) prove the win32 runner unreachable on Linux — no mutation needed. |
| sandbox | SEAM-SBX-04 | PROVABLE | No | Mode table, `resolve()` precedence, and forged-event invariant are all documented in the pinned README — static inspection. Behavioral mode-event replay = candidate execution → BLOCKED. |
| sandbox | SEAM-SBX-05/-06 | PROVABLE | No | Composition-row contract (three rows; `fs-sandbox` fencing) from pinned READMEs; denial-dialect behavior = candidate execution → BLOCKED. |
| remote | SEAM-RMT-01/-03/-05 | PROVABLE | No | Boundary and lifecycle contracts are pinned-README text; absence of any e2b row in shipped/landed compositions is a read-only grep. |
| remote | SEAM-RMT-02 | PROVABLE | No | Fail-closed credential handling is readable at `src/index.ts:140-141`; pinned `e2b@2.29.1` at `package.json:39`. Any live endpoint needs a key + egress = policy-blocked, and execution = BLOCKED-by-design. |
| remote | SEAM-RMT-04 | PROVABLE | No | Adapter contract + limitations are pinned-README text; behavioral parity vs local backends = candidate execution → BLOCKED. |
| experimental | SEAM-EXP-01/-03 | PROVABLE | No | Family charter and package roles are pinned-README text; release-exclusion is upstream's own rule. |
| experimental | SEAM-EXP-02 | PROVABLE | No | Config limits, prerequisite services, and invariant-companion contract are pinned-README text; absence from all landed compositions is a read-only grep. Activating a Team = mutation + separate owner approval → BLOCKED-by-design AND by policy. |
| experimental | SEAM-EXP-04 | PROVABLE | No | Limitations are pinned-README text; multi-agent behavior under real fleet models = candidate execution → BLOCKED. |

Each PROVABLE row lists exact command(s)/test(s) Gordon can run read-only
against the frozen hxs-15 corpus to validate readiness. Each BLOCKED-by-design
row notes what requires candidate mutation and why those are deferred.

## Open risks & items (Phase C pre-check)

<!-- Filled at last, after all families assessed -->

- [x] Risk gap (resolved): no prior document enumerated `RISK_*` codes — the
  taxonomy was derived of record in Family 1 from 03 §14 / 05 §12 / 05 §16.6
  (R1–R7) and all four families reuse those codes.
- [ ] **OPEN-1 (approval-gated):** Family 2 rung 2 (landlock) has no in-tree
  binary; activation needs a from-source build or an external pinned artifact —
  both provenance decisions requiring approval before any mutation
  (RISK_ANCHOR_PROVENANCE). It is fallback-only behind bwrap.
- [ ] **OPEN-2 (policy-gated):** Family 3 e2b rows stay absent; activation
  needs owner word + egress approval + secret provisioning by reference.
  Nothing is staged (DEFERRED_BY_POLICY).
- [ ] **OPEN-3 (policy-gated):** Family 4 agent-team stays absent; activation
  needs owner word + separate approval per profile §3, and lab-only use.
- [ ] **OPEN-4 (qualification surface):** all behavioral rows in the
  testability matrix are BLOCKED-by-design while the candidate is frozen —
  Gordon's Gates 8–10 prove POSTURE read-only; behavioral qualification of ACP
  flows, denial dialects, and multi-agent traffic lands in a later, unfrozen
  phase.
- [x] Validation scope: complete — targeted reads held to ≤3 corpus files per
  family; no partial-doc risk materialized.

## Knowledge-review receipt

Per KDD-0009 working order for Morpheus sessions (Phase A/B precedent):

- **Goal / work-order ids:** GOAL-DSH-IMPL-001; work orders 09a (controlling,
  as corrected for the new lane) and 20 (this product, issuer Flash
  2026-08-29).
- **Target environment:** OFF-CANDIDATE prep only. No hxs-15 mutation of any
  kind this session; no hxs-15 contact at all — any host-status read goes
  through the governor.
- **Knowledge roots reviewed:**
  1. HX decisions/conventions root `/home/hxsa/opt/local-tkv/agent-zero-docs/projects/harness`
     — Phase C scope read from
     `projects/Deepseek/2026-08-28-dsh-full-implementation-plan.md` (Gates 8–10
     section); 03/05 Phase A/B records and 00-goal/state-log consulted for
     taxonomy and dispositions.
  2. Approved source snapshot `/opt/tkv-local/deepseek-harness-master` —
     re-verified this session: `package.json` sha256
     `4adbdffa…4986d7`, `pnpm-lock.yaml` sha256 `6f20c268…90013e` (both match
     Phase A anchors; snapshot identity `0.1.1-rc.2`).
- **Installed runtime identity (record-only, not touched):** Node v24.20.0,
  pnpm 11.7.0, built tree from the pinned snapshot, dsh uid 999 — per Phase A/B
  records; nothing installed or changed this session.
- **Effective profiles/bundles/patches:** unchanged — landed
  `/var/lib/dsh/cordis.patch.yml` from Phase B (recorded there); no patch
  emitted this session.
- **Persistence backend:** unchanged (landed persistence root, Phase A).
- **Upstream sources consulted:** pinned local corpus only. No live upstream
  fetch this session.
- **Allowed changes:** writes to
  `pilots/PILOT-DSH-IMPL-001/10-morpheus-phase-c-prep.md` only.
- **Protected constraints honored:** no candidate mutation; read-only corpus;
  no credential-shaped literals (credential seams recorded as field names /
  env references only); append-only governance records.
- **Required tests:** `python3 scripts/validate.py` from repo root, 4/4 PASS.
- **Known drift/conflicts:** none found; corpus anchors match Phase A record.
- **Rollback state:** document-only change; pre-state = skeleton revision
  recoverable from git history.
- **proceed_status:** MAY_PROCEED (all fields available and consistent).

- **Receipt emitter**: This session closes first. The governor's receiving agent
  scans `pilots/PILOT-DSH-IMPL-001` for new material and catalogs it into
  `/home/hxsa/opt/HX-ASF-Servers/knowledge/catalog/PILOT-DSH-IMPL-001`.
- **Content**: Phase C prep findings (candidate seams, activation mechanism,
  risk taxonomy applied to Gates 8–10).
- **Citation format**: `PILOT-DSH-IMPL-001/10-morpheus-phase-c-prep.md` with
  section path and line ranges.

## Sanitized command log

All harness-side commands executed read-only against the corpus. Any mutations
are limited to new document files under this pilot project in `pilots/`.

| Command | Host   | Purpose                    | Status    |
| ------- | ------ | -------------------------- | --------- |
| Read of `pilots/PILOT-DSH-IMPL-001/{00-goal,03,05,09a,20,state-log}*` | hxs-15 (repo files) | Governance context for orders 09a/20 and Phase A/B records | OK (read-only) |
| `sed -n '95,135p' agent-zero-docs/projects/Deepseek/2026-08-28-dsh-full-implementation-plan.md` | hxs-15 (repo files) | Phase C scope (Gates 8–10) family mapping | OK (read-only) |
| `sha256sum packages/package.json packages/pnpm-lock.yaml` (corpus) | hxs-15 (corpus) | Anchor re-verification vs Phase A record (`4adbdffa…4986d7` / `6f20c268…90013e`). [OPEN CORRECTION 2026-08-29, labeled, append-only — review batch 2, F19: the `packages/` prefix is INTENTIONAL — the DSH corpus resolves its manifest anchors inside `packages/` (the monorepo manifest files are not at the repo root); root-level `package.json`/`pnpm-lock.yaml` do not exist in this corpus. Original row preserved verbatim above.] | OK — MATCH |
| `ls /opt/tkv-local/deepseek-harness-master/packages/` (+ `packages/sandbox/`, `packages/e2b/`, `packages/experimental/`) | hxs-15 (corpus) | Package locations for all four families | OK (read-only) |
| Reads: `packages/acp/acp/src/index.ts`, `packages/acp/acp/README.md`, `examples/acp-agent/cordis.yml`, root `package.json` (demo script), `packages/subagent/subagent-acp/src/index.ts`, `packages/mcp/mcp-client/README.md` | hxs-15 (corpus) | Family 1 seams (SEAM-INT-01..05) | OK (read-only) |
| Reads: `packages/sandbox/sandbox-local/src/index.ts` (ranges incl. 148-168 chain table), `packages/sandbox/sandbox-policy/README.md`, `packages/shell/bash-sandbox/README.md`, `packages/fs/README.md` | hxs-15 (corpus) | Family 2 seams (SEAM-SBX-01..06) | OK (read-only) |
| Reads: `packages/e2b/README.md`, `packages/e2b/e2b/README.md`, `packages/e2b/fs-e2b/README.md`; `grep -n` key/config anchors in `packages/e2b/e2b/src/index.ts` + version in `package.json` | hxs-15 (corpus) | Family 3 seams (SEAM-RMT-01..05); credential seams recorded as field/env references only, no values | OK (read-only) |
| Reads: `packages/experimental/README.md`, `packages/experimental/agent-team/README.md` | hxs-15 (corpus) | Family 4 seams (SEAM-EXP-01..04) | OK (read-only) |
| `python3 scripts/validate.py` (repo root) | hxs-15 (repo) | Gate for this product | PASS — 4/4 checks (wiki-sync render --check, fixture-suite, catalog-mechanical, secret-boundary), manual gates noted, exit 0 — 2026-08-29 [OPEN CORRECTION 2026-08-29, labeled, append-only — review batch 2, F22: placeholder "see result below" replaced with the actual gate result of record.] |

No hxs-15 candidate mutation, no daemon contact, no network egress, no
credential values in any command or output.

---

**Previous product:** 05 Phase B prep (testing/validation, rollback)
**Next product:** 09c Phase C fill (targeted reads & seed writes per family)
**Closed by:** Morpheus (dsh lifecycle steward, KDD-0009), 2026-08-29, lane
`omniroute/qwen3.8-2.4t-a95b` (Qwen 3.8 2.4T A95B via OmniRoute hxs-8)

