# P4-security — partition summary

- Work order: WO-OMNI-TRINITY-LEDGER-001 (Wave 0B, read-only source-derived capability ledger)
- Producer: trinity (owner-ratified 2026-08-27, KDD-0008; first commission)
- Corpus: `/opt/tkv-local/OmniRoute-release-v3.8.51` (READ-ONLY; identity VERIFIED 2026-08-27 — 13,098/13,098 git-blob identical to upstream `diegosouzapw/OmniRoute@42a13fe…`; no writes made, no code executed)
- Ledger: `pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/P4-security.json` — **50 entries** (45 capabilities + 5 NOT-ESTABLISHED), all 12 schema fields each, 146 source refs
- Reviewed at: 2026-08-27T07:29Z (corrected 2026-08-27 per review batch 20: previously read 07:55Z — postdated this file's own completion stamp and mtime (07:29:05Z); the close/review time documented here is 07:29Z, with the Coder-X identity receipt at 07:00Z)
- Truth-state labels: **FACT** = verified in source at the cited line · **UPSTREAM** = bundled-doc claim (drift-prone) · **INFERENCE** = producer reasoning, labeled in place · **AUTHORITY** = HX governance decision

## Startup receipt

```text
[TRINITY KNOWLEDGE REVIEW COMPLETE]
Agent: Trinity
Goal Contract: GOAL-OMNI-TRINITY-LAYER0 v1 (WO-OMNI-TRINITY-LEDGER-001, partition P4)
Target Host/Environment: read-only source work from hxs-5 — no host target
Source Corpus: /opt/tkv-local/OmniRoute-release-v3.8.51 (DOC-tkv-corpus-omniroute)
Reviewed At: 2026-08-27T07:00Z
Source Identity: VERIFIED 2026-08-27 by content-sensitive proof (07-source-provenance-receipt.md)
Installed Identity: NOT INSTALLED (Layer 0)
Relevant Knowledge: charter.md, profile.md, 05-work-order, 06-context-packet, repo AGENTS.md,
  sibling ledgers P1-api-routing + P2-providers-protocol (edge cross-refs)
Allowed Change Surfaces: read-only corpus reads; ledger writes under pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/
Known Drift/Risks: db/AGENTS.md "encrypted secrets store" claim contradicted by source (CAP-P4-039);
  3x AGENTS.md + 87x CLAUDE/GEMINI in-tree = untrusted upstream guidance
Rollback Ready: YES (read-only — nothing to roll back)
Task May Proceed: YES
```

## Coder-X receipts (model contract)

```text
[CODER-X IDENTITY RECEIPT]
endpoint:        http://192.168.50.201:11434  (hxs-2) — verified live from hxs-5 BEFORE first call, 2026-08-27T07:00Z
/api/version:    {"version":"0.32.15"}
/api/ps:         model hx-qwen3.6-coderx-64k:latest RESIDENT
                 digest  ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1 (matches expected ec9ebe08a824…)
                 size    17815411094 == size_vram 17815411094  (fully in VRAM)
                 context_length 65536  (ctx 65536 contract PASS)
verdict:         IDENTITY + HEALTH PASS — no substitution, no cloud
```

Coder-X call count: **2 `/api/generate` calls** (+ 2 metadata calls: 1× `/api/version`, 1× `/api/ps`).

1. AuthN/authZ decision-chain + authenticator inventory + gap analysis (10,570 prompt tokens / 1,248 eval, 17.7 s)
2. SSRF-guard coverage + secret-handling assessment + NOT-ESTABLISHED candidates (5,290 / 1,134, 15.2 s)

Both prompts = bounded questions + source excerpts only (no credentials, tokens, or credential-shaped
strings — structure quoted, never values), `think:false`, temperature 0.2. Outputs used as corroboration
only; every cited file:line was re-verified deterministically by the producer. Two Coder-X misjudgments
corrected against source: its CHANGEME "critical" rating (kept high — documented bootstrap placeholder
with a loud warning, managementPassword.ts:79-81) and its ".internal blocked unconditionally" claim
(`.internal` is private-classified, mode-conditional; only metadata hosts are unconditional).

Bounded corrections used: **1 of 2** (first reference-check run: 1 line-range fix, 1 empty-line anchor fix, 1 schema-field fix).

## 1. authN model — what OmniRoute actually is [FACT]

There **is** a central interception layer. P1 correctly found no `middleware.ts` (CAP-P1-902), but
Next.js 16's renamed convention `src/proxy.ts` exists and runs `runAuthzPipeline(request,
{enforce:true})` (src/proxy.ts:23-24) over a matcher covering `/`, `/dashboard/*`, `/home*`, `/api/*`,
and case-insensitive `/v1*`, `/v1beta*`, `/chat/*`, `/responses*`, `/codex*`, `/models`
(src/proxy.ts:35-52). Every matched request is classified into exactly one of **PUBLIC / CLIENT_API /
MANAGEMENT** (classify.ts:58; unmatched falls back to MANAGEMENT — fail-closed), then passes body-size
check → trusted-header strip → IP filter → class policy → CSRF/Origin check for cookie-authed
mutations. Per-route `requireManagementAuth` re-checks auth inside handlers as defense-in-depth
(measured: **286 route.ts files across 56 of 102 top-level /api domains** — P1's "~100 gated domains"
is refined to these numbers; the remaining domains rely on the central policy, public classification,
or their own auth).

Authenticator inventory (management plane, evaluated in this order by
policies/management.ts:129-387): ws-bridge per-process secret → LOCAL_ONLY tier gate →
inspector-ingest / model-sync / video-bridge / internal-service self-hop tokens (loopback-scoped) →
local CLI machine token (HMAC of host machine-id, loopback-only) → `mcp:connect` carve-out →
anonymous-when-`requireLogin=false` (never for the 6 ALWAYS_PROTECTED paths) → dashboard session JWT
(HS256, httpOnly cookie, 30d) → `oma_` scoped CLI access token → manage/admin-scope API key → reject
401/403 (503 on auth-backend failure — degrades closed). Client plane (clientApi.ts:57-101): Bearer /
x-api-key / x-goog-api-key / path-scoped URL token; `REQUIRE_API_KEY=false` by default
(.env.example:357) → anonymous inference allowed, and an *invalid* key degrades to anonymous with a
warning (#2257). Dashboard password is bcrypt-12 with a documented CHANGEME bootstrap placeholder
plus boot warning. OIDC SSO exists but is inert unless fully configured (AVAILABLE-DISABLED).

## 2. authZ / guard surfaces (counts, all grep-measured) [FACT]

- **Route classification**: 3 classes + 3 method-scoped cloud routes; public surface is data, not
  convention — 6 subtree prefixes + 8 exact routes + 3 read-only CORS-relaxed + 1 read-only exact +
  3 OAuth auto-import LOCAL_ONLY exclusions (publicApiRoutes.ts; **critical**, GHSA-74g9-q8f6-793h
  shape-split).
- **Tier-1 LOCAL_ONLY**: 43 prefix entries + 4 regex patterns covering every child-process-spawning /
  host-credential route (routeGuard.ts:33-107); unconditional for non-loopback/non-private-LAN peers;
  2 GET-only exemptions. Opt-in manage-scope bypass with global kill-switch and parent/child
  spawn-prefix rejection (routeGuard.ts:271-296) — **critical**.
- **Tier-2 ALWAYS_PROTECTED**: 6 paths (credential dumps / irreversible replaces) stay authed even
  under `requireLogin=false` (routeGuard.ts:129-144) — **critical**.
- **Scope inference for `oma_` tokens**: read/write by method + 6 admin-for-all + 2 admin-on-mutation
  prefixes (accessScopes.ts:52-62).
- **CSRF**: Fetch-Metadata/Origin validation + HMAC session-bound 10-min token fallback
  (pipeline.ts:413-427, csrf.ts:63-85).
- **Locality trust**: per-process `OMNIROUTE_PEER_STAMP_TOKEN`-validated peer stamps; absent/forged →
  fail-closed "remote"; via-proxy marker downgrades loopback sockets behind reverse proxies
  (peerStamp.ts) — **critical** root of trust for every loopback gate.
- **Login throttle**: 5 failures / 15 min window → 15 min lockout, per-IP in-memory with 256-entry
  prune (loginGuard.ts:18-35).
- **IP filter**: blacklist/whitelist + temp bans, persisted, loopback-exempt, stamped-IP based —
  AVAILABLE-DISABLED (disabled by default).

## 3. CORS / SSRF / egress behavior [FACT]

- **CORS**: fail-closed central allowlist — no wildcard default; ACAO emitted only for
  env/settings-listed origins or `CORS_ALLOW_ALL=true` (origins.ts:85-97). The token-authenticated
  surface (CLIENT_API + read-only PUBLIC) relaxes to Origin-echo **only when a credential header or
  cookie is present** (GHSA-7px7-29v2-m97p; anonymous keyless case stays closed), never with
  Allow-Credentials (origins.ts:147-184). Per-route `CORS_HEADERS` carry no origin by design.
  Security headers (CSP, XFO DENY, nosniff, Referrer-Policy) in next.config.mjs:40-50.
- **SSRF**: outbound URL guard allows only http/https, rejects embedded credentials, and blocks
  cloud-metadata/link-local targets **unconditionally in every mode** (incl. IPv4-mapped IPv6
  spellings). Private/LAN targets: `none` (explicit opt-in) / `block-metadata` (**default** —
  local-first, LAN providers validate) / `public-only` (strict) — outboundUrlGuardPolicy.ts:67-102.
  Enforcement points found: provider-node baseUrl at registration (urlGuard.ts), webhook create /
  update / test / validate **and dispatch-time re-validation** (webhookDispatcher.ts:45), proxy
  subscription fetch (the only path that re-checks DNS resolution at fetch time).
- **Egress**: DefaultExecutor OpenAI-fallback credential-leak guard verified at
  open-sse/executors/index.ts:231,242 (cross-ref CAP-P2-004 — jules + all search providers hard-400;
  the fallback itself still exists for unguarded providers, ledgered **critical**). Dead-proxy-pool
  fail-closed guard (#6246) prevents silent direct-egress fallback. Native TLS termination exists but
  is strictly opt-in (`OMNIROUTE_TLS_CERT/KEY`, HTTP fallback on misconfiguration) — AVAILABLE-DISABLED.
- P1 edge resolved: `/api/openapi/try` **IS auth-gated** (requireManagementAuth at route.ts:64-66)
  with same-origin + path-prefix allowlist + hop-by-hop header stripping — the CAP-P1-013 honesty
  flag closes as VERIFIED.

## 4. Secret handling / encryption at rest [FACT]

- **Encrypted**: provider credential fields (apiKey/accessToken/refreshToken/idToken) —
  AES-256-GCM `enc:v1:` format, scrypt KDF, random IV, full 16-byte tag enforced, legacy-salt
  auto-migration (encryption.ts). **But** passthrough plaintext when `STORAGE_ENCRYPTION_KEY` is unset
  (the shipped default) and plaintext fallback on cipher failure — warnings only (CAP-P4-038, high).
- **NOT encrypted**: the auto-generated **JWT_SECRET and API_KEY_SECRET are persisted as plain JSON
  in the SQLite `key_value` table** (namespace 'secrets') by instrumentation-node.ts:125-150 +
  secrets.ts:7-28. `src/lib/db/AGENTS.md:53` claims secrets.ts is a "dedicated encrypted store" —
  **UPSTREAM-STALE, contradicted by source**. DB-file read = dashboard-session forgery + API-key HMAC
  recovery (CAP-P4-039, **critical** for the HX lane: env-provide both secrets at deployment).
- API keys stored as bare sha256 (documented perf tradeoff, apiKeys.ts:655-658); management password
  bcrypt-12; boot-time weak-secret denylist validation wired (runtimeEnv.ts:98); stale-key detection
  fails loudly as 424 instead of misleading 401s; MITM/inspector traffic masking via one maskSecret
  implementation.

## 5. NOT-ESTABLISHED items (searched, not found — honest absences)

| ID | Searched for | Result |
| --- | --- | --- |
| CAP-P4-900 | `src/**/ssrf*`, `**/*ssrf*` named modules | none by name; capability lives in outboundUrlGuard*/fetchGuard |
| CAP-P4-901 | fetch-time DNS-resolution re-check for provider base URLs | not found — provider path validates hostname string only; only the subscription path re-resolves [INFERENCE] |
| CAP-P4-902 | STORAGE_ENCRYPTION_KEY rotation tooling | not found — VERSION=v1 metadata exists; recovery is re-authentication per account |
| CAP-P4-903 | redirect-target re-validation on guarded outbound fetches | not found — fetch follows redirects with default semantics after first-URL validation [INFERENCE] |
| CAP-P4-904 | distributed/persistent login throttling | none — single-process in-memory by documented design; cli/connect throttle not found in modules read |

## 6. Coverage statement

Covered: central pipeline + classification + all three route policies; every authenticator family
(dashboard JWT, bcrypt password, OIDC, manage-scope API keys, `oma_` tokens, CLI machine token,
internal/self-hop tokens); the 3-tier route guard incl. bypass machinery; scope models
(manage/admin/mcp:connect, read/write/admin inference); CSRF/Origin; peer-stamp locality; IP filter;
login throttle; body-size guard; prompt-injection facade; CORS (central allowlist, token-surface
relaxation, per-route headers, security headers); SSRF/egress (outbound guard + policy + all three
enforcement points found, DefaultExecutor leak guard, proxy fail-closed, optional TLS); secret
handling end-to-end (field encryption, passthrough defaults, plaintext signing-secret persistence,
key hashing, weak-secret validation, stale-key detection, masking). Source-hint globs swept: `auth*`
(90 files), `guard*` (22), `cors*` (2), `ssrf*` (0 — CAP-P4-900), `secret*` (4), `encrypt*`/`crypto*`
(2), `config/**` (20 files — all quality/release baselines except payloadRules.json, an empty
payload-transform rule set: not security configuration). Small adjacent guards swept but not
ledgered individually: cliConfigWriteGuard, containerConfigGuard, videoBridgeBrokerAuth (folded into
CAP-P4-012), requireCliToolsAuth (thin requireManagementAuth alias). Deferred to siblings: provider
credential lifecycle (P2), encryption-of-DB-file/backups (P5), rate limits/quotas (P6),
MCP/A2A/plugin/MITM surfaces themselves (P7 — their auth posture cross-referenced at CAP-P4-012/043/044),
packaging (P8). Nothing activated; all dispositions preliminary.

## 7. Self-verification result

- Deterministic reference check (scripted, `/tmp/trinity-p4/refcheck.py`, output saved to
  `P4-security.reference-check.txt`): JSON valid; 50/50 entries have all 12 schema fields; **146/146
  source refs — file exists, cited line in range, line non-empty. PASS** (second run; first run
  caught 3 anchor errors, fixed as bounded correction 1).
- Spot content check: 27 load-bearing refs grep-verified for the expected symbol at the cited line
  (proxy export, policy objects, guard functions, hash/encrypt lines). **PASS**.
- Coder-X drafted no line numbers this partition (used for analysis only); all anchors were taken
  from direct reads and grep output.

## 8. Ten-line summary

1. Entries: 50 (45 capabilities + 5 NOT-ESTABLISHED), 146 refs, all schema fields present.
2. authN model: central Next-16 `proxy.ts` pipeline (3-class fail-closed classification) + per-route defense-in-depth; 10 distinct authenticator types identified and ordered.
3. authZ surfaces: 43+4 LOCAL_ONLY spawn guards, 6 ALWAYS_PROTECTED, manage/admin/mcp:connect scopes, oma_ read/write/admin inference — measured counts in §2.
4. Guard measurement refined P1: requireManagementAuth in 286 routes / 56 top-level domains; `/api/openapi/try` gating VERIFIED (P1 flag closed); P1-902 refined — central interception exists via proxy.ts.
5. Secret-handling finding (critical): JWT_SECRET + API_KEY_SECRET persist PLAINTEXT in SQLite key_value 'secrets'; db/AGENTS.md "encrypted store" claim is stale; field-level AES-256-GCM exists but defaults to passthrough without STORAGE_ENCRYPTION_KEY.
6. CORS: fail-closed allowlist + credentialed-only token-surface relaxation (GHSA-7px7); no wildcard default.
7. SSRF/egress: metadata blocked unconditionally; LAN allowed by default (local-first); provider-path DNS re-check and redirect re-validation NOT-ESTABLISHED.
8. NOT-ESTABLISHED list: CAP-P4-900 ssrf-named module; 901 provider DNS re-check; 902 key rotation; 903 redirect re-validation; 904 distributed throttling.
9. Coder-X: identity/health PASS (digest ec9ebe08a824…, size==size_vram, ctx 65536); 2 analysis calls + 2 metadata calls; corroboration only.
10. Self-verification: 146/146 refs PASS on second run; 27-ref content spot-check PASS; bounded corrections 1 of 2; no stop condition hit; no git commit.
