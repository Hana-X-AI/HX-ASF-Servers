# P1-api-routing — partition summary

- Work order: WO-OMNI-TRINITY-LEDGER-001 (Wave 0B, read-only source-derived capability ledger)
- Producer: trinity (owner-ratified 2026-08-27, KDD-0008; first commission)
- Corpus: `/opt/tkv-local/OmniRoute-release-v3.8.51` (READ-ONLY; identity VERIFIED 2026-08-27 — 13,098/13,098 git-blob identical to upstream `diegosouzapw/OmniRoute@42a13fe…`; no writes made, no code executed)
- Ledger: `pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/P1-api-routing.json` — 42 entries, all 11 schema fields each
- Reviewed at: 2026-08-27T06:53Z

## 1. What the API surface is

OmniRoute v3.8.51 serves its entire HTTP API through **Next.js 16 App Router file-system
convention** — 688 `route.ts` files measured under `src/app/api/`, across 102 top-level
domain directories. There is **no global `middleware.ts`** (searched three candidate
paths, none exist): CORS, validation, and auth are implemented per route. [FACT]

The surface splits into two planes:

- **Traffic plane** — `/api/v1/**` (98 routes, 45 subdomains) is the OpenAI-compatible
  client surface (`chat/completions`, `models`, `embeddings`, `responses`, `images`,
  `audio`, `batches`, `rerank`, `messages`, speech/video, etc.); `/api/v1beta/models/**`
  serves the Gemini-shaped surface; `GET /v1` root delegates to the unified models
  catalog. JSON 404 catch-alls under `/api/*` (#6424) and `/v1/*` (#6405) keep unknown
  routes from leaking the dashboard HTML shell to API clients.
- **Management plane** — ~100 domains (`combos`, `providers`, `keys`, `settings`,
  `quota`, `resilience`, `analytics`, `cli-tools`, `services`, …) each gated per-handler
  by `requireManagementAuth` (verified pattern in `/api/combos`). Which paths bypass
  dashboard auth is data, not convention: `src/shared/constants/publicApiRoutes.ts`
  (prefix + exact sets, shape-split after GHSA-74g9-q8f6-793h) — flagged **critical** in
  the ledger because a wrong line there silently de-gates a management route.

Route registration itself has **no central registry** — it is purely the file tree;
inventory must be derived by walking the tree (as done here), not by reading a manifest.

## 2. Routing-strategy count finding (plan claim: 19)

**VERIFIED: exactly 19 public combo routing strategies exist in source** — the
candidate plan's count of 19 is CORRECT. [FACT]

Evidence chain:

1. `src/shared/constants/routingStrategies.ts:1-21` — `ROUTING_STRATEGY_VALUES` lists
   exactly 19 values: `priority, weighted, round-robin, context-relay, fill-first, p2c,
   random, least-used, cost-optimized, reset-aware, reset-window, headroom,
   strict-random, auto, lkgp, context-optimized, cache-optimized, fusion, pipeline`.
2. `open-sse/services/combo/strategyDispatch.ts:47-68` —
   `HANDLED_COMBO_STRATEGIES` (the runtime gate tied to real dispatch code) contains
   those same 19 **plus** the internal `quota-share` = 20 dispatch implementations; its
   own comment states all 20 canonical strategies have dispatch branches.
3. Each of the 20 was located in implementation code and ledgered individually
   (CAP-P1-101…113 ordering branches in `combo/applyStrategyOrdering.ts`;
   CAP-P1-120…126 dispatch-level paths in `combo.ts`, `dispatchPrelude.ts`,
   `resolveAutoStrategy.ts`, `fusion.ts`, `pipeline.ts`).

Drift recorded (docs disagree with each other; source outranks both):

- `open-sse/services/AGENTS.md` claims **17** strategies [UPSTREAM — STALE]: its list
  omits `cache-optimized` and `pipeline`, both present in source with real dispatch.
- Corpus root `AGENTS.md` and `docs/routing/AUTO-COMBO.md` claim **19** [UPSTREAM —
  matches source].

Adjacent strategy enums, distinct from the 19 (ledgered separately): 1 internal combo
strategy (`quota-share`, never user-selectable — CAP-P1-113); 8-name auto-router enum
mapping to 5 pluggable `RouterStrategy` classes with aliases (`eco→cost`,
`fast→latency`; CAP-P1-012, CAP-P1-127); 9 account-fallback orderings (CAP-P1-011).

## 3. NOT-ESTABLISHED items (searched, not found — honest absences)

| ID | Searched for | Result |
| --- | --- | --- |
| CAP-P1-900 | `packages/**/rout*` routing modules | only `packages/browser-pool` exists; none |
| CAP-P1-901 | Express/Fastify/Koa-style router registration (`express()`, `new Router()`, `fastify(`) in `src/`, `open-sse/`, `packages/` | none found |
| CAP-P1-902 | global Next.js middleware (`src/middleware.ts`, `src/app/middleware.ts`, `middleware.ts`) | none exists — per-route interception confirmed |
| CAP-P1-903 | central route registry/manifest module (`*routeRegistry*`, `*routeManifest*`, `routes.ts`) | none found — nearest artifact is the auth-classification constants file |

## 4. Coverage statement

Covered: top-level API domain inventory (all 102 dirs enumerated; domains ledgered as
plane groups, not 688 individual routes — individual route ledgering belongs to the
owning partitions P2–P7 for their domains); route registration mechanics; both
catch-alls; v1/v1beta surfaces; management-auth and public-route classification
touchpoints (deep authZ is P4's lane — cited here only where it defines the routing
surface); **all 20 combo strategy implementations** plus the three adjacent strategy
enums; the combo engine core; auxiliary routing services (wildcard, task-aware, intent,
intelligent/tag/adaptive/reasoning modules — one entry per cluster, deeper
characterization deferred to the partitions that own their domains).

Not covered (by design / other lanes): provider executors and protocol translation (P2),
streaming/tool internals (P3), authZ mechanics (P4), persistence of routing config (P5),
health/metrics endpoints (P6), MCP/A2A/agent-surface routes (P7 — flagged: `fusion` and
`pipeline` strategies are dispositioned AVAILABLE-DISABLED per the HX charter's
disabled-by-default agent-feature class [AUTHORITY]), packaging (P8).

## 5. Model contract — Coder-X identity receipt and call count

Identity/health verification BEFORE first inference call (live, from hxs-5 over LAN):

```text
[CODER-X IDENTITY RECEIPT]
endpoint:        http://192.168.50.201:11434  (hxs-2)
/api/version:    {"version":"0.32.15"}
/api/tags:       alias hx-qwen3.6-coderx-64k:latest present, digest ec9ebe08a82447f7… (matches expected ec9ebe08a824…)
/api/ps:         model hx-qwen3.6-coderx-64k:latest RESIDENT
                 digest  ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1
                 size    17815411094 == size_vram 17815411094  (fully in VRAM)
                 context_length 65536  (ctx 65536 contract PASS)
verdict:         IDENTITY + HEALTH PASS — no substitution, no cloud
```

Coder-X call count: **7 `/api/generate` calls** (+ 4 metadata calls: 1× `/api/version`,
1× `/api/tags`, 2× `/api/ps`).

- 1 load/health probe (model load, 12.1 s load duration)
- 2 diagnostic probes (empty-response investigation — the model is a reasoning model;
  resolved by `think:false`)
- 1 first analysis attempt whose budget was consumed by the thinking channel (no output;
  counted as bounded correction 1 of 2; fixed by `think:false`, same call re-issued)
- 3 successful bounded analysis calls (ordering strategies; dispatch-level strategies;
  API surface & registration), each prompt = entry schema + source excerpts only,
  temperature 0.2, no credentials or HX secrets in any prompt

Bounded corrections used: **1 of 2** (the thinking-channel fix). No stop condition hit.

## 6. Self-verification result

Deterministic re-check executed against the corpus after assembly
(full output: `/tmp/trinity-p1/reference-check-output.txt` during session; reproducible
by re-walking the ledger): JSON valid; 42 entries; all 11 fields present on every entry;
**59/59 source refs verified — file exists, line in range, cited content matches the
claim; 0 failures**. Coder-X-drafted line numbers were wrong in 21 cases (excerpt-offset
counting); all were corrected to grep-verified lines before writing — exactly the failure
mode the deterministic gate exists to catch. Remaining honesty notes: `/api/openapi/try`
auth gating not verified (flagged in CAP-P1-013); auxiliary-router entries are
cluster-level (CAP-P1-015/016).

## Correction — field count (2026-08-27, review batch 19, labeled)

The certification line in this document that reads "11 schema fields" is a
wording error: the packet's entry_schema has always carried **12 keys**, and
every entry in the paired JSON carries all 12. Recorded: prior count (11,
wrong), correction (12, canonical), revalidation (governor deterministic
key-count over the JSON, 2026-08-27 — see
`field-count-revalidation-2026-08-27.txt` in this directory: PASS). The
historical "11" claim above is preserved per the append-only convention; this
addendum is the current resolution.
