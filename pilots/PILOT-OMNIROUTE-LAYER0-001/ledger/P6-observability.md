# P6-observability — partition summary

- Work order: WO-OMNI-TRINITY-LEDGER-001 (Wave 0B, read-only source-derived capability ledger)
- Producer: trinity (owner-ratified 2026-08-27, KDD-0008; first commission)
- Corpus: `/opt/tkv-local/OmniRoute-release-v3.8.51` (READ-ONLY; identity VERIFIED 2026-08-27 — 13,098/13,098 git-blob identical to upstream `diegosouzapw/OmniRoute@42a13fe…`; no writes made, no code executed)
- Ledger: `pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/P6-observability.json` — **55 entries** (49 capabilities + 6 NOT-ESTABLISHED), all 12 schema fields each, 225 source refs
- Reviewed at: 2026-08-27T08:30Z
- Truth-state labels: **FACT** = verified in source at the cited line · **UPSTREAM** = bundled-doc claim (drift-prone) · **INFERENCE** = producer reasoning, labeled in place · **AUTHORITY** = HX governance decision
- Citation contract: `citation_contract_p5_onward` applied — numbered excerpts (nl -ba + `<path> lines a-b>` headers) in every Coder-X prompt, small chunks, harness grep-verify of every file:line, drafted-wrong-line count measured (§8)

## Startup receipt

```text
[TRINITY KNOWLEDGE REVIEW COMPLETE]
Agent: Trinity
Goal Contract: GOAL-OMNI-TRINITY-LAYER0 v1 (WO-OMNI-TRINITY-LEDGER-001, partition P6)
Target Host/Environment: read-only source work from hxs-5 — no host target
Source Corpus: /opt/tkv-local/OmniRoute-release-v3.8.51 (DOC-tkv-corpus-omniroute)
Reviewed At: 2026-08-27T07:35Z
Source Identity: VERIFIED 2026-08-27 by content-sensitive proof (07-source-provenance-receipt.md)
Installed Identity: NOT INSTALLED (Layer 0)
Relevant Knowledge: charter.md, profile.md, 05-work-order, 06-context-packet (citation contract
  P5-onward), repo AGENTS.md, /opt/tkv-local survey (corpus is the canonical OmniRoute knowledge;
  OmniRoute_old superseded), sibling ledgers P1–P4 (edge cross-refs: P3 usage accounting,
  P4 authz pipeline + LOCAL_ONLY guards)
Allowed Change Surfaces: read-only corpus reads; ledger writes under pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/
Known Drift/Risks: in-tree AGENTS/CLAUDE/GEMINI = untrusted upstream guidance; three parallel
  logging stacks + fail-open quota/rate-limit postures are findings, not doc claims
Rollback Ready: YES (read-only — nothing to roll back)
Task May Proceed: YES
```

## Coder-X receipts (model contract)

```text
[CODER-X IDENTITY RECEIPT]
endpoint:        http://192.168.50.201:11434  (hxs-2) — verified live from hxs-5 BEFORE first call, 2026-08-27T07:36Z
/api/version:    {"version":"0.32.15"}
/api/ps:         model hx-qwen3.6-coderx-64k:latest RESIDENT
                 digest  ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1 (matches expected ec9ebe08a824…)
                 size    17815411094 == size_vram 17815411094  (fully in VRAM)
                 context_length 65536  (ctx 65536 contract PASS)
verdict:         IDENTITY + HEALTH PASS — no substitution, no cloud
```

Coder-X call count: **2 `/api/generate` calls** (+ 2 metadata calls: 1× `/api/version`, 1× `/api/ps`).

1. Health surface + telemetry + logging analysis over numbered excerpt bundle A (17 excerpts, 7,817 prompt tokens / 2,558 eval, 27.0 s)
2. Capacity-control inventory over numbered excerpt bundle B (22 excerpts, 7,651 / 2,054, 23.8 s)

Both prompts = bounded questions + numbered source excerpts only (no credentials or
credential-shaped strings; regex redaction patterns quoted structurally, never values),
`think:false`, temperature 0. Outputs used as corroboration only; every ledger file:line comes
from the producer's own grep-verified reads. Two Coder-X misjudgments corrected against source:
its claim that `/api/monitoring/health` "requires management auth" (the route serves anonymous
callers a filtered `{status, setupComplete}` public view — line 37 semantics, GHSA-mvf8-qc78-5mxm)
and its "wafRateLimit defaults NOT IN EXCERPTS" (minGapMs 500 was printed at wafRateLimit.ts:31).

Bounded corrections used: **0 of 2** (4 anchor re-points caught by the producer's own scripted
spot-check before finalization — same convention as P3: not governor-disagreement corrections).

## 1. Health surface [FACT]

OmniRoute exposes a **layered** health surface, split public-vs-authenticated by design:

- **Public liveness tier (no auth, deliberately minimal)**:
  - `GET/HEAD /healthz` — lifecycle-phase probe: 200 `ok` only when the global phase is `ready`,
    503 with `starting`/`stopping` otherwise (src/app/healthz/route.ts:12-24; phase flag at
    src/lib/serverLifecycle.ts:7). Every GET also runs an event-loop-lag observer that logs a
    throttled warning when mean lag > 200ms — "HTTP 200 is not healthy; busy != ready" (#10303,
    src/lib/healthzLag.ts:4,33).
  - `GET /api/health` — canonical liveness `{status, timestamp}` only; the in-source doc states
    version/uptime/memory are deliberately withheld from this surface (src/app/api/health/route.ts:21-29).
  - `GET /api/health/ping` — liveness + `pingDb()` with `latencyMs`, 503 `db_query_failed` on DB
    failure; built for high-frequency polling (src/app/api/health/ping/route.ts:18-40).
- **Aggregated observability tier**: `GET /api/monitoring/health` joins 8+ subsystems (circuit
  breakers, rate-limit status + learned limits, model lockouts, quota monitor, active sessions,
  credential health, local providers, adaptive + structural chat admission, dedup inflight) behind
  a 1s TTL cache; **anonymous callers get only `{status, setupComplete}`** (GHSA-mvf8-qc78-5mxm
  host-fingerprinting fix; full view requires management auth — route.ts:28-37). `DELETE` resets
  all circuit breakers (authed) and invalidates the cache (route.ts:247-268). P4 cross-ref: the
  management-auth layer itself is CAP-P4's pipeline; this endpoint's anonymous/full split is the
  guard/telemetry intersection.
- **Subsystem tier**: `/api/db/health` (GET diagnosis / POST auto-repair with backup reporting,
  authenticated — route.ts:6-29), `/api/health/degradation` (feature degradation registry report,
  domain/degradation.ts:16), `/api/memory/health` (management-auth extraction-pipeline verify),
  `/api/storage/health` (DB driver/path/size/backup/retention), `/api/token-health` (OAuth token
  aggregate), plus settings-adjacent probes (qdrant/proxies/cache-health — noted, not entry'd).
- **Background pollers**: local provider_nodes poll (GET /models, 5s timeout, 30→60→120→300s
  backoff, in-memory — src/lib/localHealthCheck.ts:31-33); embedded-services HealthChecker (5s
  timeout, 3-failure threshold, unref'd timer — src/lib/services/healthCheck.ts:5-29); 60s OAuth
  token sweep via JobRegistry with OMNIROUTE_DISABLE_TOKEN_HEALTHCHECK kill switch
  (src/lib/jobs/tokenHealthCheckJob.ts:16-39); credential-health TTL cache feeding the monitoring
  payload (src/lib/credentialHealth/cache.ts:12-22).
- **Analysis/remediation tier**: provider health matrix (per-account/per-model success, latency,
  lockout state over 1h/24h/7d/30d, management-auth — providerHealthMatrix.ts:11-21) and health
  autopilots that *propose* typed remediation actions (clear breaker/cooldown/lockout,
  reactivate/deactivate connection) with risk labels and precondition hashes
  (providerHealthAutopilot.ts:14-28; combo variant joins forecast + health).

## 2. Telemetry / metrics pipeline [FACT]

- **Request phase telemetry**: `RequestTelemetry` times 7 phases (parse → validate → policy →
  resolve → connect → stream → finalize) per request; a process-local aggregator keeps the last
  **1000** summaries (FIFO) and computes count/avg/p50/p95/p99 + per-phase breakdowns over a
  sliding window (src/shared/utils/requestTelemetry.ts:20,115,149). Served at
  `GET /api/telemetry/summary?windowMs=` joined with quota-monitor summary, active sessions,
  uptime and `process.memoryUsage()` (src/app/api/telemetry/summary/route.ts:6-24). Note: this
  endpoint exposes memory/uptime without the publicView filtering that /api/monitoring/health
  applies [INFERENCE — its anonymity depends on the P4 central classification, not this file].
- **OTLP/GenAI sink (AVAILABLE-DISABLED)**: when `OMNIROUTE_OTEL_ENDPOINT` or
  `OTEL_EXPORTER_OTLP_ENDPOINT` is set, routing events flush as GenAI semantic-convention spans to
  a collector's OTLP/HTTP `/v1/traces` via plain fetch — **no @opentelemetry SDK**, bounded buffer,
  oldest-dropped under overload, batch 64, and a documented no-secrets/no-prompts serialization
  boundary (open-sse/services/routing/otel.ts:30-33,63-77; wired at routing/index.ts:65). Shipped
  default: fully inert.
- **Combo metrics**: in-memory per-combo counters (requests/success/failure/fallback, latency,
  per-model/per-target) read by getComboMetrics (open-sse/services/comboMetrics.ts:28,407);
  combo-health aggregation joins those with usage-history performance rows and quota snapshots for
  the dashboard (src/lib/usage/comboHealth.ts:1-4). Cross-ref P3: billable usage extraction and
  usage_history persistence are CAP-P3's; P6 ledgered only the health/metrics read side.
- **Export surfaces NOT FOUND**: no Prometheus/OpenMetrics `/metrics` (grep-verified zero),
  no OTel-SDK request tracing, no external log drain — see §5.

## 3. Logging model [FACT]

Three parallel logging implementations coexist (a finding in itself):

1. **Pino primary** (src/shared/utils/logger.ts): ISO timestamps, base `{service:'omniroute'}`,
   level from APP_LOG_LEVEL, and a `hooks.logMethod` wrapper that runs **every** log call through
   the redaction net before emission (logger.ts:35-39). File transport via worker-thread streams
   with an error listener that drops failed writes instead of crashing the process (#6360).
2. **Legacy structured logger** (src/shared/utils/structuredLogger.ts): 5-level JSON/human output
   that independently appends JSON lines to the same app log file when APP_LOG_TO_FILE is on.
3. **open-sse traffic-plane console logger** (open-sse/utils/logger.ts): tag/request-scoped,
   APP_LOG_FORMAT text|json, request-id correlation (`req_<ts>_<counter>`).

Redaction is **layered**: call-site payload masking for persisted call-log artifacts (fixed
SENSITIVE_KEYS set incl. cookies/storageState/runtimeKey, deliberately scoped so `capabilities`
survives — src/lib/logPayloads.ts:3-36) underneath the final pino-hook safety net (bounded,
ReDoS-guarded patterns for Bearer/x-api-key/Telegram/sk-* — src/shared/utils/logRedaction.ts:14-36).

Retention/rotation defaults (all env-overridable): file logging **ON by default** to
`DATA_DIR/logs/application/app.log`, rotate at **50MB**, keep **7 days** / **20 files**, 60s
rotation checks (src/lib/logEnv.ts:4-7,66; src/lib/logRotation.ts:29-43). Compliance: per-key
no-log set from `NO_LOG_API_KEY_IDS` + runtime `setNoLog` + optional `api_keys.no_log` column
(PRAGMA-probed once, 30s cache — src/lib/compliance/noLog.ts:16-45). Proxy events use a 200-entry
ring buffer + SQLite persistence with both inbound clientIp and **outbound egressIp**
(src/lib/proxyLogger.ts:13-36).

## 4. Capacity-control inventory (exact mechanisms) [FACT]

**Rate limits:**

| Mechanism | Algorithm | Default | Storage | Failure posture |
| --- | --- | --- | --- | --- |
| Client API-key request limit (CAP-P6-027) | multi-rule **fixed window**, atomic Redis Lua, window keys TTL 2× | per-key custom, else DEFAULT+ENV rules + maxRequestsPerDay/Minute | Redis if REDIS_URL, else process memory w/ bounded eviction | **FAIL-OPEN** on Redis error (rateLimiter.ts:266-268) |
| Per-key token limits (CAP-P6-028) | windowed token counters (provider/model scope) | configured per key | tokenLimitCounter windows + reset log | **FAIL-CLOSED** 503 on check error (apiKeyPolicy.ts:608-610) |
| Relay-token limit (CAP-P6-048) | epoch-aligned minute+day buckets in SQLite | per relay token | SQLite relay usage rows | closed (unknown token → denied) |
| Provider adaptive limit (CAP-P6-030) | Bottleneck per provider+connection, learns from x-ratelimit-*/retry-after headers | ON for API-key providers, OFF for OAuth; 200 learned-limit cap, 60s debounced persist | in-memory + debounced persistence + rate_limited_until DB column (CAP-P6-031) | wedge watchdog replaces stuck limiters |
| Provider static fallback (CAP-P6-032) | sliding window for headerless providers | nvidia 40 req/60s + concurrency 6 only; no-op otherwise | in-memory | n/a (proactive throttle) |
| Per-model semaphore (CAP-P6-033) | FIFO concurrency gate, pause-on-429, optional maxQueueSize → SEMAPHORE_QUEUE_FULL | unbounded queue historically | in-memory | queue-depth reject cascades combo |
| WAF burst guard (CAP-P6-034) | per-provider serialization + min gap | 500ms minGap (agentrouter.org) | in-memory | adds latency floor |
| Gemini tracker (CAP-P6-035) | RPD daily + RPM/TPM sliding-60s counters vs published limits | classification-only | in-memory | n/a (error-classification) |

**Process admission (the heap defenses):** structural chat gate — ONE global heavyweight budget,
threshold 256KB, hard cap 50MB, 1 heavy in flight, 2s bounded queue wait, 4MB queued-bytes budget
(chatBodyAdmission.ts:55-93) — fed by the auto-derived ingest byte budget
(min(v8 heap, cgroup) × 0.25 ÷ 8, clamp [8MB, 2GB], OMNIROUTE_CHAT_MAX_INFLIGHT_BYTES override,
admissionBudget.ts:17-30). Adaptive admission controller ships in **shadow mode** (min 8 /
initial 64 / max 1000, queue 128/2000, 5s wait, ADAPTIVE_ADMISSION_* envs,
admission/runtime.ts:33-43) — AVAILABLE-DISABLED, telemetry-only until an owner flips enforce.

**Quotas:** Quota Sharing Engine — pre-request `enforceQuotaShare` (wired chatCore.ts:2852,
embeddings.ts:388) resolves pool allocation + plan dimensions, per-(key,model) hourly caps with
429 + quota.exceeded webhook, fair-share with 0.5 saturation threshold; post-response
`recordConsumption` fire-and-forget; **FAIL-OPEN by fixed design (B16)** (enforce.ts:5-9,62,292).
Storage: 2-bucket sliding window per (key, dimension) with per-key mutex, SQLite default / Redis
optional via settings or env, never-throws fallback (sqliteQuotaStore.ts:4-58,
storeFactory.ts:4-13,80). Pools/allocations CRUD auto-mints quotaShared-* combos
(quotaPools.ts:14-22). Active-session quota monitor polls 60s→15s at ≥80%/≥95% with 5-min alert
suppression, opt-in per connection, default **off** (quotaMonitor.ts:5,21-24 — AVAILABLE-DISABLED).
Registered-key issuance dry-run at /api/v1/quotas/check (CAP-P6-049).

**Budgets:** pure evaluator (global/provider/model/pool scope; daily/weekly/monthly;
currency/tokens/requests; allow/warn/deny, deny on invalid config — budgetGuard.ts:31-66);
per-key USD budgets with scheduled resets, enforced in the API-key policy chain **fail-closed**
(503 on budget-store error — apiKeyPolicy.ts:590-591, costRules.ts:349,437), management API at
/api/usage/budget; per-key daily/weekly USD usage limits with UTC-3-anchored windows
(apiKeyUsageLimits.ts:11-30); budget_reset JobRegistry job every 10min
(budgetResetJob.ts:20-42). Cross-ref P3: cost/token measurement feeding these is CAP-P3's usage
accounting; P6 ledgered the enforcement/policy side only.

**Sessions:** fingerprint sticky sessions (model+provider+system+first-message+tools hash),
in-memory, **200-cap**, **15-min TTL**, oldest-evicted, per-key sets (sessionManager.ts:39-103);
exclusive connection leases via POST /api/v1/session-leases (acquire/renew/release, generation
fencing, OWNER_EXIT/CLIENT_CANCELLED, SQLite occupancy authority — session-leases/route.ts:28-55,
surfaced in /api/sessions:32-33). Cross-ref P4: lease API-key auth and the LOCAL_ONLY guards
around spawn-capable session surfaces are CAP-P4's entries.

## 5. NOT-ESTABLISHED items (searched, not found — honest absences)

| ID | Searched for | Result |
| --- | --- | --- |
| CAP-P6-900 | Prometheus/OpenMetrics exporter (`prometheus\|openmetrics` across src/open-sse/packages/package.json) | zero matches; only OTLP traces sink exists (CAP-P6-016) |
| CAP-P6-901 | distributed/persistent session store | none — sessionManager is a process-local Map + local sweeper; contrast quota store's optional Redis driver |
| CAP-P6-902 | per-IP rate limit on the /v1 traffic plane | none — client limiter keys on apiKeyInfo.id (`rl:api_key:*`); anonymous keyless traffic has no per-IP brake short of the admission gate; P4's per-IP loginGuard is management-plane only |
| CAP-P6-903 | external log shipping (syslog/fluentd/loki/HTTP drain) | none — destinations are stdout, app.log file, SQLite |
| CAP-P6-904 | OpenTelemetry SDK request tracing (@opentelemetry/* deps) | none in package.json; request pipeline not span-instrumented; SDK-free OTLP sink only |
| CAP-P6-905 | quota fail-closed option (QUOTA_FAIL*/failClosed grep) | none — fail-open is fixed design decision B16; needs a code change to flip |

## 6. Coverage statement

Covered: the full health surface (healthz + lag watchdog, public liveness tier, aggregated
monitoring snapshot incl. its anonymous-view control and DELETE breaker reset, degradation
registry, db health diagnosis/repair, memory/storage/token probes, local-provider and
embedded-service pollers, credential-health cache + token sweep job, health matrix, both health
autopilots); telemetry/metrics (phase telemetry + summary endpoint, OTLP sink, combo metrics and
combo-health aggregation); the logging model end-to-end (all three logger implementations, both
redaction layers, file transport + rotation/retention defaults, no-log compliance, proxy hybrid
logger, payload masking); capacity controls (8 distinct rate-limit mechanisms, both admission
gates + the byte-budget autocalibration, the quota-share engine + store + pools + monitor +
issuance check, all three budget mechanisms + reset job, sessions + exclusive leases, relay-token
limits). Source-hint globs swept: `src/**/health*` (30+ files), `src/**/metrics` (combos/metrics,
provider-metrics, plugin_metrics, cache-metrics, cc-discovery-metrics), `src/**/telemetry`,
`src/**/log*` (all runtime loggers + purges + rotation), `src/**/rate*`, `src/**/quota*` — plus
open-sse equivalents and the session/budget families. Swept but not individually entry'd
(dashboard-only projections, provider-scoped instances of ledgered patterns, or sibling-lane
ownership): provider-metrics/cache-metrics/cc-discovery-metrics routes, webSessionPoolHealth
(provider-lane instance), quota fetcher family (~15 provider-specific fetchers — provider-adapter
instances of the quotaMonitor pattern), compression budgets (P5/compression lane), thinkingBudget
(translator concern, P2/P3), outputTokenBudget (P3 streaming), usage analytics pages (P3/P8),
vncSession/volcengine sessions (provider-lane), traffic-inspector sessions (P7 surface — its auth
posture is CAP-P4-012). Deferred to siblings per the DAG: usage/billing accounting internals (P3),
authN/Z and LOCAL_ONLY guard mechanics (P4), persistence/migrations of the tables cited here (P5 —
migrations 013/052/078/085-088/106-108/123/125/148 noted as the schema base, not re-ledgered),
MCP/A2A/agent surfaces incl. /api/v1/agents/health (P7), packaging modes (P8). Nothing activated;
all dispositions preliminary.

## 7. Self-verification result

- Deterministic reference check (scripted, `/tmp/trinity-p6/refcheck.py`, output saved to
  `P6-observability.reference-check.txt`): JSON valid; 55/55 entries have all 12 schema fields;
  **225/225 source refs — file exists, cited line in range, line non-empty. PASS.**
- Spot content check (scripted, `/tmp/trinity-p6/spotcheck.py`): **128/128 load-bearing refs have
  the expected symbol at the cited line. PASS** (second run; first run caught 4 anchor-precision
  errors — doc-comment line cited instead of symbol line — re-anchored and re-verified:
  credentialHealth/cache.ts:21→22, rateLimitSemaphore.ts:29→35, session-leases/route.ts:31→32,
  budgetGuard.ts:48→49).

## 8. Citation-contract measurement (P5-onward contract, MEASURE clause)

Coder-X drafted **~70 line-specific citations** across its 2 analysis responses (numbered
excerpts supplied; model copied numbers). **Wrong: 2 (~3%)** — rateLimiter.ts:109 for the Lua
script (script opens at :112; :109 is its doc comment) and rateLimitManager.ts:99 for
DEFAULT_RESILIENCE_SETTINGS (use site is :98). Both were caught in producer review and never
entered the ledger (all ledger refs are producer grep-verified). **Baseline comparison: P1 was
21/59 ≈ 36% wrong; P6 is 2/70 ≈ 3% wrong — the numbered-excerpt contract removed the
excerpt-offset arithmetic failure mode as designed.** Separately, 2 semantic misjudgments
(§Coder-X receipts) were corrected against source — analysis still requires the deterministic
gate, the contract removes arithmetic, not review.

## 9. Ten-line summary

1. Entries: 55 (49 capabilities + 6 NOT-ESTABLISHED), 225 refs, all 12 schema fields each; refcheck PASS, spot-check PASS.
2. Health surface is layered: public liveness tier (/healthz lifecycle + lag watchdog, /api/health, /api/health/ping DB probe) vs aggregated /api/monitoring/health (8+ subsystems, 1s cache, anonymous→{status,setupComplete} per GHSA-mvf8, DELETE resets breakers) vs subsystem/matrix/autopilot tiers.
3. Telemetry: 7-phase request timing (1000-entry window, p50/p95/p99) at /api/telemetry/summary; OTLP GenAI routing-event sink is SDK-free, oldest-dropped, endpoint-env-gated → AVAILABLE-DISABLED; combo metrics in-memory.
4. Logging: three parallel stacks (pino + legacy structured + open-sse console); universal pino-hook redaction net over call-site payload masking; file logging ON by default (50MB/7d/20-files rotation); per-key no-log compliance set; proxy logs ring+SQLite with egress-IP capture.
5. Rate limits: 8 mechanisms — client-key Redis Lua fixed-window (FAIL-OPEN on Redis outage, in-memory fallback), token limits (fail-closed), provider Bottleneck header-learning (ON for API-key, OFF for OAuth), static nvidia sliding window, per-model FIFO semaphore, WAF 500ms gap, Gemini RPD/RPM/TPM classifier, relay-token SQLite windows.
6. Admission: global heavyweight chat gate (256KB/50MB/1-in-flight/2s-queue/4MB-queued) on an auto-derived ingest byte budget (heap×0.25÷8, [8MB,2GB]); adaptive admission ships shadow-mode → AVAILABLE-DISABLED.
7. Quotas: pool-based sharing engine, fail-open by fixed design (B16), sliding-window SQLite store (Redis optional), per-model caps with 429+webhook, opt-in 60s→15s session monitor (default off) → AVAILABLE-DISABLED; no fail-closed toggle exists (CAP-P6-905).
8. Budgets/sessions: evaluator + per-key USD schedules (fail-closed 503 on store error) + 10-min reset job + daily/weekly USD limits; sessions 200-cap/15-min-TTL in-memory; exclusive connection leases with generation fencing over SQLite occupancy.
9. NOT-ESTABLISHED: Prometheus/OpenMetrics export, distributed session store, per-IP traffic-plane rate limit, external log shipping, OTel-SDK request tracing, quota fail-closed option (CAP-P6-900…905).
10. Coder-X: identity/health PASS (digest ec9ebe08a824…, size==size_vram, ctx 65536); 2 analysis calls + 2 metadata calls, corroboration only; drafted wrong lines 2/70 ≈ 3% vs P1 baseline 36%; bounded corrections 0 of 2; no stop condition hit; no git commit.

## Correction — authorization metadata on three entries (2026-08-27, review batch 21, labeled)

Three entries' `required_authorization` fields read `none` where the source gates
management/authenticated access (their `test_contract` fields already carried the
correct behavior — the metadata field alone was wrong). Corrected in
`P6-observability.json`: CAP-P6-005 → GET anonymous = liveness only
({status, setupComplete} per GHSA-mvf8-qc78-5mxm), GET full view = management,
DELETE = management only with 401 (route.ts:37, :247-249); CAP-P6-010 → management
(requireManagementAuth; route.ts:21-22); CAP-P6-049 → authenticated
(isAuthenticated — 401 'Authentication required'; route.ts:8-10). JSON re-validated:
55 entries, 12 fields each, all three test_contracts intact. No other entry changed.

## Correction — the batch-21 authorization addendum is superseded (2026-08-27, governor, labeled)

The "Correction — authorization metadata on three entries" addendum above
(batch 21) moved product-auth prose INTO `required_authorization`. Batch 22
established that the field is the **HX activation enum**
(`none|owner|layer-N|specialist-review`), not product auth — so the prose state
described there was itself a contract violation and was reverted the same day:
all three entries (`CAP-P6-005/010/049`) are back to `required_authorization:
"none"`. The product behavior never moved: it lives in `purpose` (the
GHSA-mvf8-qc78-5mxm anonymous-vs-management split) and `test_contract`
(management gate, unauthenticated DELETE → 401) — verified present in the
current JSON. Batch 23 then settled the semantics permanently with a note in
the context packet's entry_schema (state-log row 27). Treat the batch-21
addendum as historical; this addendum is the current resolution.
