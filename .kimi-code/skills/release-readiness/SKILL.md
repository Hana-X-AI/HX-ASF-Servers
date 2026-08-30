---
name: release-readiness
description: "Validate release readiness with evidence-based go/no-go qualification for the HX factory's QA lane (Gordon): go/no-go checklist with evidence, sub-5-minute smoke suite, staged rollout validation, rollback criteria defined before deploy, and post-deployment verification. Use when: 'release ready', 'go/no-go', 'smoke test', 'release checklist', 'rollback plan', 'staged rollout', 'canary deploy'. NOT for: the final acceptance call (James's governor lane), safe-release techniques applied during the rollout itself, or continuous synthetic monitoring. Adapted from petrkindlmann/qa-skills v3.0.0 (MIT)."
---

# Release Readiness — evidence-based go/no-go qualification (Gordon)

Adapted from `petrkindlmann/qa-skills` v3.0.0 (MIT) into the HX factory's QA workflow.
Owner: **Gordon** (QA / independent qualification, QA family, KDD-0010). This skill
produces the **qualification evidence** for a release; James makes the final acceptance
call on `governace/process/governor-verification-checklist.md`. Gordon does not author
the primary test plan/scripts (Bailey's lane), does not fix application configuration
(Erwin's lane), and does not accept (James's lane). Evidence and checklists land at
`governace/qa/<project-name>/`.

<objective>
"I think it's fine" ships the bug that the rollback you never practiced can't undo at
6 PM on a Friday. This skill turns "ready to ship" into something measurable: a
go/no-go checklist with evidence for each item, a sub-5-minute smoke suite, a staged
rollout with metric-gated promotion, rollback thresholds defined before deploy, and
post-deployment verification. Every section gives concrete criteria, not aspirations.
</objective>

## Discovery Questions

Check `governace/qa/<project-name>/qa-project-context.md` first — if it exists, use it
and skip anything answered there. Then ask only what's missing.

**Release cadence and process:**
- How often do you release, and who makes the go/no-go call? In the factory: Gordon
  qualifies the evidence; James accepts. The checklist weight matches the cadence.
- Is there a release train schedule or is it ad-hoc?
- How many environments exist between dev and production? (staging, pre-prod, canary)

**Current state:**
- What does the current go/no-go process look like, and is it documented?
- Has a release ever been rolled back? How long did it take? (Reveals whether rollback
  is real or aspirational.)
- What was the last release incident and its root cause? Any release-blocking bugs
  right now?

**Infrastructure and capabilities:**
- Do you have rollback capability, and how long does a rollback take?
- Can you do staged/canary deployments?
- Do you have feature flags, and how are they managed? (Decides flag-based vs
  infra-level rollout.)
- What monitoring and alerting is in place? Are database migrations reversible?

**Team and communication:**
- Who is on-call during and after releases?
- How are stakeholders notified, and is there a release communication channel?
- How are release notes generated?

## Core Principles

### 1. Release confidence comes from evidence, not feelings
"I think it's fine" is not a go/no-go criterion. Evidence means: all CI pipelines green,
smoke tests pass on staging, performance budgets met, no open P0/P1 bugs. If you can't
point to data, you're not ready.

### 2. Smoke tests are the last safety net, not the only safety net
Smoke tests catch catastrophic failures. They are not a substitute for thorough testing
throughout the development cycle. If your smoke test suite is the only thing between you
and production, you have a process problem upstream.

### 3. Staged rollouts reduce blast radius
Deploying to 100% of users simultaneously means 100% of users are affected by any bug.
Staged rollouts (canary, percentage-based, ring-based) let you catch issues when they
affect 1% of users instead of all of them.

### 4. Rollback criteria must be defined BEFORE release
If you wait until something is on fire to decide whether to roll back, you'll waste
critical minutes debating. Define the criteria in advance, relative to baseline: "If
error rate exceeds 2x baseline within 15 minutes, we roll back. No discussion needed."
Tie the trigger to your DORA targets.

### 5. Every release is a learning opportunity
Post-deployment verification isn't just about catching bugs. Track what went well, what
was slow, what was stressful. Improve the process continuously.

## Go/No-Go Checklist

Use this as a template. Adapt it to your context. Every item should be verifiable with
evidence, not just "I checked." Store the completed checklist as a versioned artifact
(e.g. `RELEASE-<version>.md`) at `governace/qa/<project-name>/` so sign-off is
auditable.

### Automated Checks (Must Pass)

- [ ] **All CI pipelines green** — Unit tests, integration tests, E2E tests, type
      checking, linting
- [ ] **Smoke test suite passes on staging** — Critical user journeys verified in the
      staging environment
- [ ] **No open P0/P1 bugs for this release** — Check issue tracker, filter by
      milestone/label
- [ ] **Performance budgets met** — API response times and bundle size within
      thresholds; Lighthouse CI for frontend releases (skip Lighthouse for
      API/backend-only releases)
- [ ] **Security scan clean** — No high/critical vulnerabilities in `npm audit` / Snyk /
      Dependabot
- [ ] **API contract tests pass** — No breaking changes to public APIs
- [ ] **Visual regression tests pass** — No unintended visual changes
- [ ] **Accessibility checks pass** — axe-core scan shows no new violations

### Manual Checks (Verify Before Go)

- [ ] **Feature flags reviewed** — Document which flags are enabled/disabled in this
      release; confirm flag states for production
- [ ] **Monitoring and alerts configured** — New features have corresponding alerts
      (error rate, latency, business metrics)
- [ ] **Rollback plan documented and tested** — Written procedure exists; rollback has
      been practiced on staging
- [ ] **Database migrations tested** — Tested forward migration; backward migration
      verified if schema change is reversible
- [ ] **Third-party dependency changes reviewed** — New or upgraded external
      dependencies checked for breaking changes
- [ ] **Release notes prepared** — Changelog updated, stakeholder-facing summary written
- [ ] **On-call engineer identified** — Named person is available and has context on the
      release contents
- [ ] **Communication plan ready** — Stakeholders know the release is happening; support
      team briefed on changes
- [ ] **No conflicting releases** — Other teams aren't deploying simultaneously
- [ ] **Deploy window confirmed** — Not deploying during peak traffic or before a
      weekend (unless continuous deployment)

### Risk Assessment

- [ ] **Change scope categorized** — Small (config change, copy update), Medium (new
      feature, refactor), Large (architecture change, migration)
- [ ] **Blast radius estimated** — What percentage of users could be affected if
      something goes wrong?
- [ ] **Revert complexity assessed** — Can this be reverted in <5 minutes? Does
      reverting require a data migration?

## Smoke Test Suite Design

### What to Include

Smoke tests cover **critical user journeys only**. If these fail, the application is
fundamentally broken.

**Typical smoke test suite (5-8 tests):**

1. **Application health** — Homepage loads, returns 200, no JavaScript errors in console
2. **Authentication** — User can log in with valid credentials, session is established
3. **Core workflow** — The primary value-delivering action works (create a document,
   submit a form, complete a purchase flow)
4. **Data retrieval** — Key data loads correctly (dashboard populates, search returns
   results, product page loads)
5. **Payment/transaction** (if applicable) — Payment flow completes with test credentials
6. **API health** — Primary API endpoints return valid responses with correct schemas
7. **Navigation** — Critical navigation paths work (deep links, redirects, menu items)
8. **Error handling** — Application shows a user-friendly error page for invalid routes
   (404)

### What NOT to Include

- Edge cases (those belong in regression tests)
- Visual perfection (that belongs in visual regression tests)
- Performance benchmarks (that belongs in performance tests)
- Exhaustive form validation (that belongs in unit/integration tests)

### Keeping It Fast

Target: **under 5 minutes** for the entire smoke suite.

- Run tests in parallel where possible
- Use API calls instead of UI interactions for setup (create test user via API, not
  through a registration form)
- Skip non-critical assertions (don't check exact copy text, check that elements exist)
- Use a dedicated test account with pre-created data (don't create data from scratch
  each run)
- Avoid unnecessary waits — use smart waiting (wait for element, not `sleep(3000)` /
  `waitForTimeout`)

### Environment-Specific Smoke Tests

**Staging smoke tests:**
- Full smoke suite (all 5-8 tests)
- Can use test payment providers
- Can test with feature flags in upcoming release configuration
- Can test database migrations

**Production smoke tests:**
- Subset of staging smoke tests (3-5 tests)
- Use synthetic test accounts (clearly labeled, won't affect analytics)
- Never test with real payment transactions (use sandbox mode or skip)
- Focus on: app loads, auth works, core read operations work, API responds

**Post-deployment smoke tests:**
- Run immediately after deploy completes (within 60 seconds)
- Same as production smoke tests
- If any fail, trigger alert and begin rollback evaluation

Staging is not production: it has different data volumes, traffic patterns,
third-party configurations, and infrastructure scale. That gap is exactly why production
and post-deployment smoke tests exist on top of staging verification.

## Staged Rollout Validation

### Rollout Stages

A typical staged rollout. The same ladder expressed for flag-based rollouts adds a 25%
step (see below):

| Stage | Traffic % | Duration | Purpose |
|-------|-----------|----------|---------|
| Canary | 1% | 15-30 min | Catch crashes, exceptions, obvious failures |
| Early adopters | 10% | 1-2 hours | Validate error rates, latency, business metrics |
| Partial rollout | 25-50% | 2-4 hours | Confirm stability at scale |
| Full rollout | 100% | — | Monitor for 24 hours post-deployment |

### What to Monitor Between Stages

Before promoting to the next stage, verify **all** of these:

**Error metrics:**
- Error rate (HTTP 5xx) is not higher than baseline
- Exception count is not higher than baseline
- No new error types appearing in logs

**Performance metrics:**
- P50 and P95 latency are within acceptable range (relative to baseline, not an absolute
  ceiling)
- No increase in timeout errors
- Database query times are stable

**Business metrics:**
- Conversion rate is not dropping
- User engagement (page views, actions) is stable
- Revenue/transaction volume is normal (if applicable)

**Infrastructure metrics:**
- CPU and memory usage are normal
- No increase in queue depth or message backlog
- No disk space issues from new logging

### Automated Promotion Criteria

Define rules for automatic promotion between stages. Each gate combines an error-rate
ceiling, a latency ceiling expressed **relative to baseline**, a stability window, and
(at higher stages) business-metric guardrails.

### Feature Flag Gradual Rollout

An alternative to infrastructure-level canary deploys:

1. Deploy new code to 100% with the feature flag OFF
2. Enable the flag for internal users first (dogfooding)
3. Enable for 1% of users (canary equivalent)
4. Gradually increase: 10%, 25%, 50%, 100%
5. Remove the flag after full rollout is stable for 1 week

**Advantages:** Faster rollback (just flip the flag), no infrastructure changes, can
target specific user segments.

**Disadvantages:** Code complexity (branching logic), stale flags become tech debt,
doesn't catch infrastructure issues.

#### Tooling

| Platform | Best at | Notes |
|----------|---------|-------|
| **LaunchDarkly** | Enterprise scale; Guarded Rollouts (auto-canary analysis); AI Configs for prompt/model rollouts | Acquired Highlight.io in 2025 — observability tied to flags |
| **Statsig** | Experiment-first culture; Switchback experiments for two-sided marketplaces | Acquired by OpenAI Sept 2025; weigh acquisition/roadmap risk |
| **GrowthBook** | OSS-first; stale-flag detection with code-reference scanning | Strong fit when you want to self-host |
| **Unleash** | OSS, GitOps-style flag definition, environment scoping | Apache 2 license |
| **Flagsmith** | Kill switches as first-class concept; canary alerts; OSS option | |
| **Harness FME** (formerly Split) | Targeted rollouts + monitoring tied to deploy pipelines | Rebranded after Harness acquisition |

Vendor-native canary analysis is now common — if your platform offers it, prefer it over
hand-rolled rollout-policy YAML. Given the vendor churn this table documents, prefer
OpenFeature-compatible SDKs so flag tooling stays swappable.

#### Rolling Out AI/LLM Features

AI features need a distinct rollout pattern — directly relevant to the HX LLM-server
fleet: prompt versions and model IDs are configurable separately from code, and a kill
switch is mandatory.

1. Pin the prompt template version and model ID in your AI Configs platform (or
   feature-flag JSON).
2. Roll out the prompt/model combo behind a flag — internal first, then 1%, 10%, etc.
3. Watch eval metrics (hallucination rate, jailbreak success rate, cost per request)
   per cohort, not just error rate.
4. Cost guardrail: a budget circuit breaker that fails the feature open (graceful
   fallback) when a model's per-request cost spikes.
5. Kill switch: a single flag that disables the AI path and routes to a deterministic
   fallback or a "feature unavailable" state — testable in staging before launch.

## Rollback Criteria and Process

### Automated Rollback Triggers

Define these thresholds BEFORE deployment. When any trigger fires, rollback begins
automatically. All thresholds are relative to the measured baseline, not absolute
ceilings.

| Metric | Threshold | Action |
|--------|-----------|--------|
| Error rate (5xx) | >2x baseline for 5 min | Auto-rollback |
| P95 latency | >3x baseline for 5 min | Auto-rollback |
| Health check | 3 consecutive failures | Auto-rollback |
| Crash rate (mobile) | >0.5% | Auto-rollback |
| Error budget | >50% burned in 1 hour | Auto-rollback |

### Manual Rollback Triggers

These require human judgment but should have clear guidelines:

- **Customer-reported critical issue** — Multiple users reporting the same problem
- **Data integrity concern** — Evidence of corrupted or incorrect data
- **Security vulnerability discovered** — Active exploitation or high-severity CVE
- **Monitoring blind spots** — You realize you can't monitor a critical metric for the
  new feature
- **On-call engineer judgment** — The on-call engineer always has authority to trigger
  a rollback

### Rollback Procedure

**Step 1: Decide (< 2 minutes)**
- Is the trigger automated or manual?
- If manual: does the issue meet rollback criteria? If yes, proceed. Don't debate.

**Step 2: Execute rollback (< 5 minutes)**
- **Kill switch (fastest, prefer if available):** Flip the dedicated kill-switch flag
  for the affected feature. Test the kill switch in staging before every release; an
  untested switch is not a switch.
- **Feature flag rollback:** Disable the feature flag for the new code path.
- **Code rollback:** Revert to the previous deployment (re-deploy previous
  image/artifact).
- **Database rollback:** Run backward migration if applicable. If migration is
  irreversible, skip this step and handle data separately.
- **Cache invalidation:** Clear CDN and application caches if the old version would
  serve stale/incorrect data.

**Step 3: Verify (< 5 minutes)**
- Run production smoke tests
- Verify error rate returns to baseline
- Check that the rolled-back version serves correctly

**Step 4: Communicate (< 10 minutes)**
- Notify the release channel using the rollback skeleton below
- Update status page if user-facing impact occurred
- Brief the support team

**Step 5: Investigate (next business day)**
- Root cause analysis
- Write a regression test that would have caught the issue
- Update the go/no-go checklist if a check was missing
- Schedule the fix and re-release

#### Rollback announcement skeleton

Drop this in the release channel during Step 4.

```
Subject: [Rollback] v{version} — {date} {time}
Status: ROLLED BACK
Reason: {one line — e.g. error rate 4x baseline within 8 min}
Impact: {who was affected, for how long}
Current state: Running previous version v{prev_version}
Next steps:
- Root cause investigation: {owner}
- Fix ETA: {estimate or "investigating"}
```

### Data Considerations

When a migration can't be rolled back:

- **Forward-fix:** Deploy a fix on top of the current (broken) version instead of
  rolling back
- **Dual-write:** During migration, write to both old and new schemas. Rollback must
  **preserve and reconcile accepted mutations** made against the new schema — do not
  simply drop the new writes (that silently loses accepted data). Use a **tested
  expand/contract rollback**: (expand) write to both schemas while the new path is
  active; on rollback, reconcile — replay or backfill the new-schema mutations into the
  old schema so no accepted write is lost, verify consistency (e.g. row counts,
  checksum/summary comparison, replay log drained) before switching back to the old
  path; (contract) only after reconciliation passes, stop dual-writing and remove the
  new schema. Exercise the reconcile-and-return path in staging before relying on it
  for a live rollback.
- **Shadow migration:** Migrate in the background, validate, then cut over. Rollback
  just stops the cutover
- **Point-in-time recovery:** Restore database from backup (last resort, causes data
  loss for changes since backup)

## Post-Deployment Verification

### Immediate (0-15 minutes)

- [ ] Production smoke tests pass
- [ ] Error rate is at or below pre-deployment baseline
- [ ] No new exception types in error tracker
- [ ] Health check endpoints return healthy
- [ ] Key pages load correctly (spot check 2-3 pages manually)

### Short-term (15 minutes - 2 hours)

- [ ] Synthetic monitoring confirms all critical paths working
- [ ] Error rate trend is flat or declining (not increasing)
- [ ] P50 and P95 latency are within expected range
- [ ] No increase in support ticket volume
- [ ] Business metrics (conversions, revenue, signups) are normal
- [ ] No memory leaks or resource exhaustion trends

### Medium-term (2-24 hours)

- [ ] Overnight batch jobs complete successfully (if applicable)
- [ ] No time-zone-dependent issues surfacing as other regions wake up
- [ ] Email/notification delivery is normal
- [ ] Third-party integrations are functioning
- [ ] No gradual performance degradation

## Anti-Patterns

### "It worked on staging"
Staging is not production — different data volumes, traffic patterns, third-party
configurations, and infrastructure scale. Staging success is necessary but not
sufficient evidence of readiness.
**Fix:** Use production smoke tests and staged rollouts in addition to staging
verification.

### No rollback plan
"We'll figure it out if something goes wrong" means you'll figure it out under pressure,
sleep-deprived, with users complaining.
**Fix:** Document the rollback procedure. Practice it quarterly. Time it. Make it a
checklist, not tribal knowledge.

### Deploying on Friday afternoon
You deploy at 4 PM on Friday. An issue surfaces at 6 PM. Your team is at dinner.
**Fix:** Deploy early in the week, early in the day, when the full team is available to
monitor. If you must deploy on Friday, deploy before noon with extra monitoring.

### Skipping smoke tests because "the pipeline is green"
CI pipelines test against test data in test environments. Smoke tests verify the
deployed application works with production configuration, data, and infrastructure.
**Fix:** Smoke tests are non-negotiable. If they're slow, make them faster. If they're
flaky, fix them. Never skip them.

### Big-bang releases instead of incremental
Accumulating 6 weeks of changes into one mega-release means more can break, harder to
identify the cause, higher risk, longer rollback.
**Fix:** Release smaller, more frequently. Aim for weekly or bi-weekly releases with
small, well-understood changesets.

### No post-deployment verification
You deploy and move on to the next feature. An hour later, users are experiencing errors
that nobody is watching for.
**Fix:** Assign someone to monitor dashboards for 30-60 minutes post-deploy. Set up
automated alerts. Run post-deployment smoke tests.

### Rollback aversion
"We're so close to fixing it, let's just push a hotfix forward." Meanwhile, users are
affected for another 45 minutes.
**Fix:** Roll back first, investigate second. A working previous version is better than
a broken current version.

### Feature flag accumulation
You use feature flags for safe rollouts (good!) but never remove them (bad).
**Fix:** Use platform-level stale detection, not calendar reminders. Pair with a
quarterly review where flags older than the threshold are either archived or get a
documented owner + reason to keep.

### Canary alerts that lie
Auto-rollback wired to a metric that's noisy, late-arriving, or partially aggregated.
**Fix:** Treat the canary alert like any other test — it has a false-positive rate and a
false-negative rate, and you measure both. Run a "shadow" period where the alert
publishes its decision but doesn't actually rollback; promote to auto-rollback only
after the false-positive rate is below your tolerance.

### Switchback experiments for two-sided systems
Standard A/B fails on marketplaces and other systems where the treatment group affects
the control group through shared state.
**Fix:** Use a switchback design — alternate the entire system between control and
treatment over short windows (minutes to hours).

### Crossing the boundary
Gordon qualifies; James accepts. A qualification document is not an acceptance; do not
substitute Gordon's evidence for James's governor decision.

## Verification

Run these immediately after the deploy completes, smallest check first.

```bash
# Health endpoint returns healthy — finite timeout, fail on HTTP errors,
# assert HTTP 200 AND the expected healthy body (no curl hang on a stuck endpoint)
health_body="$(curl --max-time 10 --fail-with-body -s https://your-app.com/health)" \
  && echo "$health_body" | jq -e '.status == "healthy" or .status == "ok"' >/dev/null \
  && echo "health OK: HTTP 200 with healthy body"

# Response time + status in one shot — same finite-timeout, fail-on-HTTP-error rule
curl --max-time 10 --fail-with-body -o /dev/null -s \
  -w "HTTP %{http_code} in %{time_total}s\n" https://your-app.com

# New errors since deploy — should be empty
# (error-tracker CLI, e.g. sentry-cli issues list --query "firstSeen:>15m")

# Compare 5xx count for the service before vs after deploy — must not increase
```

Both probes use `--max-time` (finite timeout so a hung endpoint fails fast, not a
forever-blocking curl) and `--fail-with-body` (curl exits non-zero on any HTTP error).
Pass criteria: the health probe exits 0 **and** asserts HTTP 200 **and** the expected
healthy response body; the status probe returns HTTP 200 within your latency budget; the
error-tracker query returns no new issues; and the post-deploy 5xx count is at or below
the pre-deploy baseline.

## Done When

- Go/no-go checklist completed with evidence for each item and stored as a versioned
  artifact (`RELEASE-<version>.md`) at `governace/qa/<project-name>/`, with sign-off
  recorded.
- Smoke test suite run against the release candidate in staging — all tests pass
  (exit code 0).
- Rollback criteria documented as specific baseline-relative thresholds, and the
  rollback procedure practiced on staging at least once.
- Staged rollout plan defined with traffic percentages, per-stage promotion criteria,
  and guardrail metrics for each stage.
- Post-deployment verification commands run and passing (health 200, no new error-tracker
  issues, 5xx count at or below baseline).
- The qualification package is handed to James for the final acceptance call.

## Related Skills (factory lanes)

- **test-environments** / **ci-cd-integration** / **test-reliability** (Gordon) — the
  staging stack, pipeline gates, and flake triage that supply this skill's evidence.
- **ai-test-generation** / **test-planning** / **test-strategy** / **qa-project-context**
  (Bailey) — the authoring side that produced the tests this qualification executes.
- **qa-metrics** concepts — DORA evidence (change failure rate, MTTR) and error/pass
  rates cited in go/no-go decisions and rollback thresholds.
- When releasing AI/LLM features (HX LLM-server fleet): prompt-version eval tests and
  kill-switch design are mandatory.
- When a release goes wrong, the postmortem feeds the missing check back into this
  go/no-go checklist.
