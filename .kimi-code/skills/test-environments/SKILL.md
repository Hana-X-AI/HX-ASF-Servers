---
name: test-environments
description: "Design and stand up test environments for the HX factory's QA lane (Gordon): environment tiers (dev/CI/preview/staging/prod), parity auditing against production, seed-data lifecycle, and external-dependency stubbing at the HTTP boundary. Use when: 'set up test environment', 'staging parity', 'environment tiers', 'spin up test infra'. NOT for: choosing mock-vs-stub per dependency, factory/fixture data patterns, or authoring the test plan/scripts (Bailey's lane). Adapted from petrkindlmann/qa-skills v3.0.0 (MIT)."
---

# Test Environments — environment strategy and setup (Gordon)

Adapted from `petrkindlmann/qa-skills` v3.0.0 (MIT) into the HX factory's QA workflow.
Owner: **Gordon** (QA / independent qualification, QA family, KDD-0010). This skill is
the **environment lane** of the locked test loop: Erwin installs → Bailey authors →
**Gordon sets up env + executes** → results to the testing log → Gordon notifies
Bailey + Erwin → Erwin fixes config → Gordon retests → max 3 iterations → James accepts
on `governace/process/governor-verification-checklist.md`.

**Gordon's boundary:** Gordon sets up/qualifies test environments and executes/
qualifies tests (independent qualification). He does NOT author the primary test
plan/scripts (Bailey's lane), does NOT fix application configuration (Erwin's lane),
and does NOT accept (James's lane). Deliverables land at
`governace/qa/<project-name>/`.

<objective>
Staging on SQLite passes tests that break on prod Postgres; a shared staging box becomes
a queue where one broken deploy blocks the whole team; an unmocked external call flakes
CI at random. This skill prevents those by designing environment tiers that mirror
production where it matters, isolate per-PR, and stub external dependencies at the HTTP
boundary. It delivers an environment inventory, a parity checklist, and a stubbing
strategy keyed to dependency type.
</objective>

## Factory deployment posture (labeled note)

The HX factory deploys **native services on systemd** — no Docker/containers for HX
deployments unless the owner explicitly authorizes otherwise (owner rule 2026-08-27).
Test environments must mirror the production deployment shape where it matters, so the
default HX test stack is a **native systemd service stack**, not a container stack.
Where this skill preserves generic container methodology (Compose/Testcontainers), it
applies only where the owner has authorized containerization; Gordon records the
authorization per project in `governace/qa/<project-name>/`. Environment *parity* is
judged against the real production shape, whatever it is.

## Discovery Questions

Check `governace/qa/<project-name>/qa-project-context.md` first — if it exists, use it
and skip anything already answered there. Then:

1. **How many environments exist today?** Local dev, CI, staging, preview, production?
   Map what you have before designing what you need.
2. **What is the deployment shape?** Native systemd services (factory norm)? Record the
   unit files, ports, and dependencies so parity can be assessed against production.
3. **How is test data seeded?** Manual SQL, migration-based, factory libraries, or
   production snapshots? This decides whether seed scripts are a quick win or a rewrite.
4. **How close is staging to production?** Same DB engine, queue, cache, auth provider,
   orchestration? Each mismatch is a class of bugs staging can never catch.
5. **External dependencies:** How many third-party APIs does the system call, and are
   they stubbed in non-prod? Unstubbed third parties are the top source of CI flake.

## Core Principles

**1. Staging must mirror production where bugs hide.** If staging uses SQLite and
production uses PostgreSQL, staging tests prove nothing about prod behavior. Match the
database engine *and version*, the queue system, the cache layer, and the auth provider
— those are where environment-specific bugs live.

**2. Ephemeral environments beat long-lived ones.** A shared staging environment becomes
a bottleneck where one broken deploy blocks the entire team. Per-PR preview environments
give isolation and parallel testing; keep staging only for final pre-release validation.

**3. Deterministic seed data, not production copies.** Production snapshots carry PII,
stale references, and non-reproducible state. Build seed data from factories that
generate consistent, valid, minimal datasets.

**4. Stub external dependencies at the boundary, not deep inside.** Third-party APIs are
unreliable, rate-limited, and expensive. Stub them at the HTTP boundary (MSW/WireMock or
a stubbing proxy) — never by mocking internal service classes, which hides integration
bugs between your own code.

**5. Environment config is code.** Every environment difference (URLs, flags,
credentials, resource limits) must be version-controlled and reviewable. No manual setup
that cannot be reproduced from the repo.

## Environment Strategy

### Environment Tiers

| Environment | Purpose | Data | External Deps | Lifecycle |
|-------------|---------|------|---------------|-----------|
| **Local dev** | Fast inner loop | Seeded fixtures, minimal | Stubbed | Developer-managed |
| **CI** | Automated validation | Seeded per-run, ephemeral | Stubbed or service-local | Created/destroyed per pipeline |
| **Preview** | PR-level review & E2E | Seeded from factories | Stubbed or sandbox | Created on PR, destroyed on close |
| **Staging** | Pre-production validation | Anonymized production-like | Real integrations (sandbox accounts) | Long-lived, regularly reset |
| **Production** | Live users | Real | Real | Permanent |

### Local Development

Fast feedback, zero shared state. Developers must be able to run the full stack locally
in under two minutes. Factory default: the local test stack is brought up as native
processes (systemd user units or the project's own dev script); where the owner has
authorized containers, the source skill's `docker compose -f docker-compose.test.yml up
-d` + `db:seed` pattern applies. External APIs are stubbed with MSW-style handlers
loaded in dev mode.

### CI Environment

Fully isolated, created fresh per pipeline run, destroyed after. Database and cache
services are provisioned per run with health checks gating test start — a service that
only *started* but is not *ready* makes tests race the database. In the HX native
posture, CI provisions service-local instances (or authorized container services) with
health-gated startup.

### Preview Environments (Per-PR)

Each pull request gets its own isolated environment; reviewers click a link and test the
exact changes without interfering with other PRs. For each preview, pair the env
lifecycle with a **database branch** — create a branch on PR open, drop it on close —
so every preview has an isolated DB copy instead of a shared staging DB. Previews are
auto-created on PR open and auto-torn-down on close.

### Staging

Long-lived environment that mirrors production infrastructure. Reset weekly or on-demand
to prevent drift. The reset procedure is scripted: drop/recreate the schema, run
migrations (which MUST recreate extensions + grants — a bare schema drop also drops
default privileges and installed extensions), seed anonymized production-like data, then
verify health.

**Caveat:** `DROP SCHEMA public CASCADE` removes the schema's **schema-scoped default
privileges** (those granted on the `public` schema itself), while **global default
privileges** (database/role-level defaults set outside the schema) remain — do not assume
a bare drop removes everything, or that `CREATE SCHEMA public` restores the schema-scoped
grants (it does not). Avoid claiming the drop always removes installed extensions:
extensions (`uuid-ossp`, `pgcrypto`, …) drop only if their objects live in the dropped
schema; extensions installed in other schemas (e.g. `pg_catalog` or a dedicated schema)
survive. The migration pipeline must recreate or preserve extension-owned objects as
needed (`CREATE EXTENSION IF NOT EXISTS …`, re-grant schema-scoped defaults), or the
migrate step fails. Document and test the supported reset sequence (drop → recreate →
migrate → re-grant → re-seed) so extension and grant requirements are verified, not
assumed.

## Test Infrastructure Patterns

Two details that matter for any test stack (native or authorized-container):

- **Health checks gate readiness.** `depends_on`-style ordering (or service-local
  equivalents) without a healthcheck only waits for the service to *start*, not to
  accept connections — tests then race the database and fail with connection errors.
- **Seed is a one-shot step, not a long-running service.** The app starts only after
  seeding *exits 0*. Modeling seed as a long-running process gets a race where the app
  boots mid-seed.

Where the owner has authorized containerization, the source skill's full
`docker-compose.test.yml` (app, Postgres, Redis, one-shot seed, Mailpit), multi-stage
Dockerfile, and Testcontainers guidance apply unchanged — Testcontainers is the 2026
default for "ephemeral infra owned by the test" (a throwaway Postgres per test class),
and is a strong alternative to hand-rolled compose + trap scripts. Reach for a
declarative stack when humans and many tests share it; reach for per-test disposable
infra when each test wants its own copy.

## External Dependency Management

### Stubbing Strategy by Dependency Type

| Dependency Type | Local/CI Strategy | Staging Strategy |
|----------------|-------------------|------------------|
| Payment (Stripe) | HTTP stub returning mock responses | Test mode with `sk_test_` keys |
| Email (SendGrid) | **Mailpit** capturing SMTP (web UI on :8025, SMTP on :1025) | Sandbox mode |
| Auth (Auth0/OIDC) | Local JWT issuer with test keys | Dev tenant |
| Storage (S3) | **Native MinIO or a local stub** (default for local/CI); MinIO **container** only with explicit HX owner authorization | Dedicated test bucket with lifecycle policy |
| Search (Elasticsearch) | Local instance | Dedicated test index with reset script |
| SMS (Twilio) | HTTP stub | Test credentials |

**Avoid: MailHog** — unmaintained, last release 2020. Use Mailpit
(`axllent/mailpit`); it is a drop-in on the same ports (1025 SMTP / 8025 UI).

### HTTP Stubs

Stub external APIs at the HTTP boundary with a modern handler library (e.g. MSW 2.x:
`http` + `HttpResponse`, server lifecycle wired through setup/teardown hooks). Set
`onUnhandledRequest: "error"` so an unmocked external call fails the test loudly instead
of leaking a real network request.

### MinIO as an S3 Substitute

Run S3-compatible storage locally instead of hitting real AWS in local/CI tests. Point
the SDK at it with `endpoint`, env-var credentials, and `forcePathStyle: true`
(required for MinIO).

### Contract Testing as Stub Validation

Stubs drift from reality. Pair every stub with a contract test that verifies the stub
matches the real API shape.

## Environment Parity Checklist

Run this when setting up or auditing a non-production environment.

| Dimension | Question | Red Flag |
|-----------|----------|----------|
| **Database engine** | Same engine and version as production? | SQLite in test, PostgreSQL in prod |
| **Database schema** | Same migration pipeline applied? | Manual schema changes in staging |
| **Data shape** | Seed data covers all entity states? | Only "happy path" records, no edge cases |
| **Infrastructure** | Same service shape as production? | Container stack in CI, native systemd in prod (or vice versa) |
| **Network** | Same internal service topology? | Monolith in test, microservices in prod |
| **Config** | Env vars documented and version-controlled? | Undocumented env vars, manual setup |
| **Auth** | Same auth provider/flow? | Bypassed auth in test with hardcoded tokens |
| **Feature flags** | Same flag evaluation engine? | Hardcoded flags in test, real engine in prod |
| **TLS/HTTPS** | Same certificate handling? | HTTP in staging, HTTPS in prod |
| **Timeouts/Limits** | Same rate limits, pools, timeouts? | Infinite timeouts in test hide perf issues |

## Anti-Patterns

**Shared staging as the only test environment.** One developer's broken deploy blocks
everyone. Use ephemeral per-PR environments for isolation and keep staging for final
pre-release validation only.

**Production database copies for test data.** PII risk, non-reproducible state, massive
datasets that slow tests. Build minimal seed data from factories with deterministic
values.

**Environment-specific code paths.** `if (env == "test") { skipAuth(); }` means you are
not testing the real auth flow. Swap implementations via dependency injection or config,
not environment conditionals.

**Manual environment setup.** If setup needs a 15-step wiki page, it will be wrong
within a week. Script everything: one command should be the only step.

**Stubbing internal services instead of external ones.** Stub at the HTTP boundary where
your system talks to the outside world. Stubbing internal modules hides integration bugs
between your own services.

**No health checks.** Readiness that only checks "started" not "ready" makes tests race
the database.

**Long-lived preview environments.** Previews that persist after merge waste resources
and accumulate stale state. Automate teardown on PR close.

**Crossing the boundary.** Gordon qualifies environments and executes; he does not author
the primary test plan/scripts (Bailey), does not fix application config (Erwin), and
does not accept (James).

## Verification

Run these against the artifacts you produce, smallest check first:

1. **Stack config is valid** — the compose/test-stack config validates (e.g.
   `docker compose -f docker-compose.test.yml config -q` exits 0 where containers are
   authorized; the native equivalent is that every systemd unit parses and every
   dependency is declared).
2. **Stack comes up healthy** — every service reaches a passing health check within the
   timeout; a non-zero exit means a healthcheck never went green.
3. **Database accepts connections** — a `pg_isready`-style probe reports
   `accepting connections`.
4. **Stubs fail loud** — run the suite with `onUnhandledRequest: "error"`; any real
   outbound call should error the test, not pass silently.
5. **Seed is idempotent** — running twice exits 0 with no duplicate-key errors.

## Done When

- Environment inventory documented (dev, CI, preview, staging, production) with
  characteristics and access notes per tier at `governace/qa/<project-name>/`.
- The test stack config validates and brings every service to a passing healthcheck.
- Seed scripts are idempotent (running twice exits 0, no duplicate-key errors) and
  checked into the repository.
- External dependencies are stubbed at the HTTP boundary with loud-fail unhandled
  requests; no real third-party credentials in non-prod.
- Environment parity gaps documented (e.g. SQLite in CI vs PostgreSQL in prod) with
  mitigations in place or tracked as issues.
- Preview environments auto-created for PRs and auto-torn-down on close.
- Execution results go to the testing log; Gordon notifies Bailey + Erwin and retests
  per the locked loop (max 3 iterations). James accepts.

## Related Skills (factory lanes)

- **test-reliability** / **ci-cd-integration** (Gordon) — flake triage and pipeline
  wiring that run against the environments this skill stands up.
- **release-readiness** (Gordon) — the go/no-go qualification that consumes staging
  verification evidence.
- **ai-test-generation** / **test-planning** / **qa-project-context** (Bailey) — the
  authoring side of the loop; Gordon executes against Bailey's plan and scripts.
- **test-data-management** concepts (factories, DB branching) — feed the deterministic
  seed-data lifecycle this skill wires into each tier.
- **contract-testing** — consumer-driven contracts that verify stubs match real APIs.
