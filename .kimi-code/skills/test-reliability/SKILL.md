---
name: test-reliability
description: "Make the HX factory's test suites trustworthy from the execution/qualification lane (Gordon): flake classification by root cause, resilient locator patterns, environment-aware and data healing, confidence-scored repair with evidence, and quarantine management. Use when: 'flaky test', 'test stability', 'self-healing locator', 'broken locator', 'unreliable test', 'quarantine flaky test'. NOT for: authoring the primary test scripts (Bailey's lane), bulk-regenerating selectors after a planned UI refactor, or accepting work (James's lane). Adapted from petrkindlmann/qa-skills v3.0.0 (MIT)."
---

# Test Reliability — flake classification and healing (Gordon)

Adapted from `petrkindlmann/qa-skills` v3.0.0 (MIT) into the HX factory's QA workflow.
Owner: **Gordon** (QA / independent qualification, QA family, KDD-0010). This skill is
the **execution/qualification** lane: Gordon classifies flakes from execution evidence,
quarantines, and feeds fix recommendations back through the locked test loop. He does
NOT author the primary test scripts (Bailey's lane) — repairs to Bailey's authored
tests go back to her through the loop, not by silent rewrite. He does NOT fix
application configuration (Erwin's lane) and does NOT accept (James's lane). Records
land at `governace/qa/<project-name>/`.

<objective>
A retried test that still flakes will eventually fail 3-of-3 during your most critical
release, and a silently auto-repaired test may now verify a different element entirely.
This skill builds suites teams can trust: resilient locators, classified flakes,
environment-aware healing, data healing, and observable repair with confidence
scoring — every automated fix produces evidence a human can review.
</objective>

## Quick Route

| Situation | Go to |
|-----------|-------|
| Test flakes in CI, root cause unknown | Flake Classification → decision tree |
| Locator broke, want resilient replacement | Locator Resilience |
| Action fails, suspect slow backend not UI bug | Environment-Aware Healing |
| 401/404/429 mid-test from stale data | Data Healing |
| Want auto-repair with review gate | Observable Repair Workflow |
| Isolate a flaky test without blocking CI | Quarantine Management |

## Discovery Questions

Check `governace/qa/<project-name>/qa-project-context.md` first — it carries known
flaky areas, selector strategy, and CI environment details. Skip any question it already
answers.

- **What is your current flaky test rate?** Check CI failure stats over the last 30
  days. Below 2% is healthy; 2-5% needs attention; above 5% is eroding team trust.
- **Where is the pain concentrated?** Locator breakage? Timing? Test data? Environment?
  If unknown, instrument first (see Flake Classification).
- **What is your current selector strategy?** data-testid everywhere, mixed CSS and
  role-based, or no strategy (whatever works)? This sets the stability-score baseline.
- **How do you handle flaky tests today?** Retry and hope, skip and forget, or
  something structured? Decides how much process you need to add.
- **What CI environment runs the tests?** Same machine every time or different runners?
  Consistent or variable resources? Drives the environment-vs-test diagnosis.
- **What is your test data strategy?** Shared database, per-test fixtures, factory
  seeding, or external services? Decides whether data healing applies.

## Core Principles

1. **Prevention over cure.** Writing a resilient test costs 1x. Investigating a flaky
   one costs 10x. Losing team trust in the suite costs 100x.
2. **Healing must be observable and reviewable.** Every automated repair produces
   evidence: what broke, what was tried, what worked, the confidence score. Silent
   fixes erode trust as fast as silent failures.
3. **Classify before fixing.** The fix for a timing issue is completely different from
   the fix for a data dependency. Wrong diagnosis wastes effort and can make things
   worse.
4. **Flaky tests are bugs.** Not annoyances to tolerate. A flaky test either has a test
   bug (fix the test), reveals an app bug (fix the app), or exposes an environment
   issue (fix the environment).
5. **Track reliability as a metric, not a feeling.** Measure flaky rate, mean time to
   heal, quarantine age, and selector stability. What gets measured gets fixed.
6. **Self-healing is a spectrum.** Start with resilient locators (Level 1), add
   fallback strategies (Level 2), then environment-aware healing (Level 3), then
   confidence-scored auto-repair (Level 4). Do not jump to Level 4 before mastering
   Level 1.

## Locator Resilience

### Multi-Attribute Selectors (Beyond Fallback Chains)

A single locator strategy is a single point of failure. Multi-attribute selectors
combine multiple signals for one element lookup — resilience without fallback-chain
complexity.

**The key insight:** instead of "try A, then B, then C," use "find element matching A
AND B AND C with tolerance for one signal missing."

```typescript
// Multi-attribute locator: tries combinations from most specific to least
const submitBtn = await multiAttributeLocator(page, {
  testId: 'checkout-submit',              // most stable signal
  role: 'button',                          // semantic signal
  name: /place order/i,                    // accessible name
  nearText: 'Order Summary',              // visual context
});
// Internally: tries testId+role+name first, then testId alone, then role+name,
// then text, then nearText+role. Returns first visible match.
// Unlike fallback chains, it combines signals for higher confidence.
```

### DOM Similarity / Neighbor Context Matching

When a locator fails, the element may still exist with changed attributes. Use
surrounding DOM context to find it:

1. **Parent + tag + type:** Find the container (by testId), then locate by tag and type
   within it.
2. **Preceding label:** Find sibling text (label), then locate the adjacent
   input/button.
3. **Nearby text context:** Find visible text near the target, then locate the element
   type in the same parent.

These are repair candidates scored by the confidence system below — not runtime
fallbacks.

### Selector Stability Scoring

Rate every selector on a 0-5 scale to prioritize refactoring.

| Score | Strategy | Survives |
|-------|----------|----------|
| 5 | `getByTestId('submit-order')` | CSS, text, and structural changes |
| 4 | `getByRole('button', { name: 'Submit' })` | CSS and structural changes |
| 3 | `getByLabel('Email')` | CSS changes; breaks on label rewording |
| 2 | `getByText('Submit Order')` | Breaks on any copy change |
| 1 | `locator('.btn-primary.submit')` | Breaks on CSS or structural change |
| 0 | `locator('//div[3]/button[1]')` | Breaks on any DOM change |

**Target:** Average score of 3.5+ across the suite. Audit monthly. Prioritize fixing
score-0 and score-1 selectors. Emit one score per locator to `selector-stability.md`
(or a CI step) and report the suite average so the 3.5 target is verifiable, not
asserted. In the factory, selector-score findings are fed back to Bailey (author) as
fix recommendations through the locked loop.

## Flake Classification Framework

Every flaky test has a root cause category. Classifying correctly determines the fix.

### Categories

| Category | Signal | Root Cause | Fix Direction |
|----------|--------|------------|---------------|
| **Timing** | Timeout errors, passes on retry, worse in CI | Race condition, animation, async operation | Wait for condition, not time |
| **Data dependency** | Fails with other tests, passes alone | Shared state, missing cleanup | Isolate per-test, fixture cleanup |
| **Environment** | Fails on specific runner, correlates with load | Resource contention, network latency | Mock externals, increase resources |
| **Order dependency** | Fails with --shard or fullyParallel | Depends on another test's side effect | Self-contained setup |
| **Time sensitivity** | Fails at specific times (midnight, month-end) | Uses real clock, date boundary | Mock clock, relative comparisons |
| **Visual rendering** | Screenshot diff flickers, subpixel differences | Font rendering, antialiasing, animation frame | Increase threshold, mask dynamic regions |
| **External service** | Correlates with third-party status | Real HTTP calls in tests | Mock external APIs |

### Classification Decision Tree

```
Test is flaky
│
├── Does it pass when run alone?
│   ├── YES → ORDER DEPENDENCY or DATA DEPENDENCY
│   │   ├── Does another test create/modify data it needs? → ORDER DEPENDENCY
│   │   └── Does it share a database/file/cache? → DATA DEPENDENCY
│   │
│   └── NO → Not order/data dependent. Continue below.
│
├── Does it fail more often in CI than locally?
│   ├── YES → TIMING or ENVIRONMENT
│   │   ├── Timeout errors? → TIMING (CI is slower)
│   │   ├── Connection errors? → ENVIRONMENT (network latency / service)
│   │   └── Resource errors (OOM, disk)? → ENVIRONMENT (resource contention)
│   │
│   └── NO → Same rate locally and CI. Continue below.
│
├── Does it fail at specific times?
│   ├── YES → TIME SENSITIVITY
│   │   ├── Near midnight? → Date boundary issue
│   │   ├── Near month/year end? → Calendar calculation
│   │   └── Specific hour? → Timezone issue
│   │
│   └── NO → Continue below.
│
├── Does it involve screenshots or visual comparison?
│   ├── YES → VISUAL RENDERING
│   │
│   └── NO → Continue below.
│
├── Does it call external HTTP APIs?
│   ├── YES → EXTERNAL SERVICE
│   │
│   └── NO → TIMING (most likely — default classification)
│       └── Investigate: what async operation is not being awaited?
```

The fix per category is applied through the locked loop: test-side fixes go back to
Bailey, environment/config fixes to Erwin, and Gordon retests (max 3 iterations).

## Environment-Aware Healing

Not all test failures are test problems. Some are environment problems.
Environment-aware healing distinguishes the two and adapts.

### Slow Backend vs True UI Failure

When an action fails, check backend health before blaming the test:

1. **Action fails** → Hit `/api/health`.
2. **Backend unhealthy (5xx or timeout)** → Retry with exponential backoff. Diagnose as
   `backend_down`. This is not a UI bug.
3. **Backend healthy (2xx)** → This is a real UI/test failure. Do not retry.

Return a structured diagnosis: `{ success: boolean; diagnosis: 'backend_down' |
'ui_failure' | 'backend_slow_recovered' }`. This feeds flake classification — backend
issues are environment issues, not test bugs, and env issues route to Erwin/Gordon's
environment skill.

### Resource Contention Detection

Before declaring a test failure in CI, check for resource contention:

- **Browser health:** Load `about:blank`. If it takes > 2s (baseline < 500ms), the
  runner is overloaded.
- **API health:** Hit `/api/health`. If it takes > 5s (baseline < 1s), the backend is
  under pressure.
- **Diagnosis:** If either check fails, classify as an environment issue and annotate
  the test result. Do not count resource-contention failures toward flaky test rates.

## Data Healing

Test data expires, gets cleaned up, or becomes invalid. Data healing detects and
regenerates stale test data.

### Common Data Failure Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| Expired auth token | 401 response during test | Regenerate token in fixture |
| Deleted test record | 404 when accessing seeded data | Re-seed before test |
| Uniqueness violation | 409 or constraint error | Generate unique identifiers per run |
| Stale cache | Wrong data returned | Clear cache in setup |
| Exceeded quota | 429 or rate limit error | Reset quotas or use dedicated test account |

### Self-Healing Test Data Fixture Pattern

Build fixtures that verify data exists and regenerate if stale. **Pick ONE contract and
follow it consistently** — do not mix a shared deterministic-user lookup with
unconditional cleanup (deleting a shared user that other tests may depend on, or deleting
a user this test did not create, corrupts the shared state).

Contract A (recommended) — **unique per-test user, delete only that user**:

```typescript
// Pattern: create (unique) → verify → heal → use → cleanup(own user only)
testUser: async ({ request }, use, testInfo) => {
  // Per-test uniqueness via testId PLUS a globally unique run+worker identifier
  // so repeated and parallel sessions (multiple workers, retries, CI re-runs)
  // cannot generate the same email. crypto.randomUUID() is the required source;
  // where the CI platform provides a unique run/worker id (e.g.
  // process.env.CI_RUN_ID + workerIndex) prefer that. Do NOT use
  // Date.now()-and-process.pid — it is not collision-safe across parallel
  // workers and is not permitted.
  const runId = process.env.CI_RUN_ID && process.env.CI_WORKER
    ? `${process.env.CI_RUN_ID}-${process.env.CI_WORKER}-${crypto.randomUUID()}`
    : crypto.randomUUID();
  const email = `test-${testInfo.testId}-${runId}@example.com`;
  // 1. Create the unique test user for THIS test
  // 2. Verify auth token is valid (GET /api/me)
  // 3. If token expired → refresh it (POST /refresh-token), mark as healed
  // 4. If user missing → recreate the unique user, mark as healed
  // 5. If healed → annotate testInfo for observability
  // 6. use(user) → run the test
  // 7. Cleanup: delete ONLY this test's user (guaranteed by fixture, even on failure)
}
```

Contract B — **shared pre-seeded user, never delete or mutate it**: lookup the shared
user, refresh its token if needed, use it, and leave it untouched — no cleanup that
deletes or mutates the shared user. Choose whichever the suite already uses, and keep the
lookup, healing, annotation, and cleanup flow consistent with that contract.

**Key patterns:**
- Use `testInfo.testId` in email/identifiers for per-test uniqueness (Contract A).
- Annotate `testInfo.annotations` when healing occurs, for observability.
- Clean up in the fixture's post-use block, not in `afterEach` — fixtures guarantee
  cleanup on failure; under Contract A, delete only the user this test created; under
  Contract B, delete nothing.

## Observable Repair Workflow

**Core guardrail:** Healing must be observable and reviewable. Every repair follows
this flow:

```
Failure Detected
  │
  ▼
Candidate Repair Generated
  │
  ▼
Confidence Score Computed (0.0 - 1.0)
  │
  ▼
Evidence Diff Produced (what changed, what was tried)
  │
  ▼
Approval Policy Applied  (descending lower-bound checks — every score falls in a band)
  │ ├── Score >= 0.9   → Auto-apply, log for batch review
  │ ├── Score >= 0.7   → Apply in quarantine, flag for individual review
  │ ├── Score >= 0.5   → Do NOT apply, open PR with evidence for review
  │ └── Score < 0.5    → Discard, manual investigation required
  │
  ▼
Intent Fidelity Check (does repaired test still test the same thing?)
  │
  ▼
Rollback if intent fidelity drops
```

In the factory, auto-applied repairs to Bailey-authored tests are held for review and
returned to the authoring lane with the evidence diff — never a silent rewrite.

### Confidence Scoring

Score each repair candidate on six dimensions (weighted sum, 0.0-1.0):

| Dimension | Weight | Scoring |
|-----------|--------|---------|
| Match specificity | 0.30 | testId=1.0, role=0.9, text=0.7, context=0.5, CSS=0.3 |
| Element visible | 0.15 | 1.0 if visible, 0.0 if not |
| Same parent container | 0.15 | 1.0 if same container, 0.0 if different |
| Same element type | 0.15 | 1.0 if same tag+role, 0.0 if different |
| Text similarity | 0.15 | 0.0-1.0 (Levenshtein ratio of accessible name) |
| Attribute overlap | 0.10 | 0.0-1.0 (Jaccard of shared attributes) |

**Score thresholds** (descending lower-bound checks — contiguous, every score 0.0-1.0
lands in exactly one tier; 0.895 and 0.695 now have defined outcomes):
- **>= 0.9** — Auto-apply, log for batch review.
- **>= 0.7** — Apply in quarantine, flag for individual review (covers 0.7-0.899).
- **>= 0.5** — Do not apply; open a PR with evidence for review (covers 0.5-0.699).
- **< 0.5** — Discard, manual investigation required.

### Repair Evidence

Every repair produces an evidence record containing: test file, test name, failure
type, original locator, candidate replacements (each with confidence, evidence string,
and intent-preserved flag), which candidate was selected, timestamp, approval path,
rollback trigger, **and a recording of the repair run** (where the tooling supports it)
— the "agentic video receipt." Without the recording, a Level-3/4 healed test asks
reviewers to trust a JSON record; with it, the diff and the runtime are both
inspectable.

**Recording guardrails (Level-3/4 "agentic video receipt"):** before enabling
Level-3 or Level-4 repair recordings, require — (1) **sensitive-data redaction or
masking** of credentials, PII, tokens, and customer data in the captured video;
(2) **restricted access controls** limiting who can view the recordings; (3) **defined
retention limits** (e.g. bounded days then auto-delete); and (4) a **deletion
procedure** for the recordings. Do not enable recordings until these four controls are
in place and documented.

### Buy vs Build

Hand Levels 3-4 to a vendor when you don't want to own a confidence-scored healer;
build in-house when you need on-prem/air-gapped deployment, an explicit AI-prompt audit
trail, or quarantine logic your tracker can't express.

- For **Selenium / Selenide / Robot Framework** suites, **Healenium** remains the
  dedicated self-healing layer.
- For **agent-driven self-healing in Playwright**, **Playwright MCP** is the canonical
  path — it gives the agent live browser control to discover replacement locators.
- Hosted platforms shipping this workflow: **Trunk Flaky Tests** (auto-quarantine + AI
  failure clustering), **CloudBees Smart Tests** (formerly Launchable), and **Datadog
  Test Optimization**. All three offer fingerprinting + clustering + auto-quarantine
  that maps onto Levels 3-4.

### Intent Fidelity Checking

After applying a repair, verify the test still exercises the same user intent:

- **Element type changed** (e.g. `button` → `a`) — intent NOT preserved, rollback.
- **ARIA role changed** (e.g. `button` → `link`) — intent NOT preserved, rollback.
- **Form action changed** (targets a different endpoint) — intent NOT preserved,
  rollback.
- **Same tag, role, and form action** — intent preserved, keep repair.

A repair that changes WHAT the test verifies (not just HOW it finds elements) must be
rolled back.

## Quarantine Management

Quarantine isolates flaky tests so they run but do not block CI. The essentials:

```typescript
// Tag the flaky test
test('intermittent WebSocket reconnect', {
  tag: ['@quarantine'],
  annotation: {
    type: 'quarantine',
    description: 'Flaky since 2026-03-15. Race condition in WebSocket handler. Ticket: BUG-1234.',
  },
}, async ({ page }) => { /* ... */ });
```

```typescript
// playwright.config.ts — separate projects
projects: [
  { name: 'stable', testMatch: /.*\.spec\.ts/, grep: /^(?!.*@quarantine)/ },  // exclude quarantine
  { name: 'quarantine', grep: /@quarantine/, retries: 3 },
],
```

In CI, run `--project=stable` as a blocking step and `--project=quarantine` with
`continue-on-error: true` so the quarantine project never blocks the pipeline.

### Quarantine Lifecycle

```
1. DETECT    — Test identified as flaky (CI reporter or manual triage)
2. TAG       — Add @quarantine annotation with ticket link and date
3. ISOLATE   — Quarantine project runs separately, does not block
4. DIAGNOSE  — Follow the flaky test classification framework
5. FIX       — Apply the fix pattern for the classified category (via the locked loop)
6. VERIFY    — Run 50x with --repeat-each, zero failures required
7. RELEASE   — Remove @quarantine tag, add annotation documenting the fix
```

### Quarantine Hygiene Rules

- **Maximum quarantine age: 14 days.** After 14 days, fix it or delete it. Permanent
  quarantine is permanent rot.
- **Every quarantine entry has a ticket link.** No anonymous quarantines.
- **Weekly review.** Check the quarantine list every sprint. Aging quarantines get
  escalated.
- **Track quarantine size.** More than 5% of tests in quarantine signals a systemic
  problem requiring process change, not just test fixes.

## Anti-Patterns

### 1. Silent Selector Replacement
Replacing a broken selector with no logging, review, or confidence scoring. The repaired
test may now verify a different element entirely. **Every repair must produce
evidence.**

### 2. "Just Retry It" as a Fix
Retries are a detection mechanism, not a fix. A test that needs retry 2-of-3 will
eventually fail 3-of-3 during your most critical release.

### 3. Disabling Flaky Tests Permanently
`test.skip('flaky, will fix later')` — "later" never comes. Either quarantine with
tracking or delete entirely. Skipped tests with no ticket are dead code.

### 4. Treating All Flakiness the Same
Timing issues and data dependencies need completely different fixes. Adding
`waitForTimeout(5000)` to a data-dependency problem makes the test slower and still
flaky.

### 5. waitForTimeout as a Stability Fix

```typescript
// NEVER the right fix
await page.waitForTimeout(5000);

// Wait for the actual condition
await expect(page.getByRole('table')).toBeVisible();
await page.waitForResponse(resp => resp.url().includes('/api/data') && resp.status() === 200);
```

### 6. Healing Without Observability
Auto-repair that produces no logs, evidence, or confidence scores. You cannot improve
what you cannot measure, and you cannot trust what you cannot review.

### 7. Over-Engineering Healing Before Writing Stable Tests
Building a complex self-healing framework before adopting basic resilient-locator
patterns. Start with multi-attribute selectors and proper waits. Add healing
infrastructure only when data shows where breakage occurs.

### 8. No Quarantine Expiry
Tests sit in quarantine for months. Quarantine is a temporary state, not a permanent
home. Enforce a 14-day maximum.

### 9. Silent Rewrites of the Authoring Lane
Gordon diagnoses and recommends; he does not silently rewrite Bailey's authored test
scripts. Fix recommendations return through the locked loop with evidence.

## Failure Modes

| Symptom | Likely cause | Fix or check |
|---------|--------------|--------------|
| Backend health check itself flaps → false `backend_down` diagnosis | Health endpoint is itself flaky/slow | Track the health endpoint's own p99 separately; don't gate diagnosis on a single probe |
| Artifact storage balloons after enabling repair video | Recording on every run, not just repairs | Record only on the repair path, not the happy path |
| Auto-repair accuracy drops below 80% | Confidence threshold too low, or intent-fidelity check skipped | Raise the auto-apply floor; never skip the intent check |
| Quarantine project blocks the pipeline | Missing `continue-on-error` on the quarantine CI step | Add it; the quarantine project must never block merges |

## Verification

Run Playwright from the project's installed, pinned dependency (never an unpinned
`npx playwright`): `npm ci` first, then use the local binary
(`./node_modules/.bin/playwright`) or `npm exec --offline -- playwright`. Pass the test
path through a quoted `SPEC` argument so spaces and shell metacharacters in the path are
not interpreted.

```bash
# Bind the spec path from the first argument, or the environment variable.
SPEC="${1:-$SPEC}"
[ -n "$SPEC" ] || { echo "usage: verify-reliability.sh <spec-path> (or set \$SPEC)"; exit 2; }
[ -x ./node_modules/.bin/playwright ] || npm ci

# Reproduce the flake — it must fail at least once before you trust any fix.
./node_modules/.bin/playwright test "$SPEC" --repeat-each=20 --workers=4 --trace=on

# After fixing, prove stability — require 50/50 passes, in CI conditions too.
./node_modules/.bin/playwright test "$SPEC" --repeat-each=50 --workers=4

# Confirm quarantine routing: --project=stable excludes @quarantine tests and
# --project=quarantine runs only them.
./node_modules/.bin/playwright test --project=stable
./node_modules/.bin/playwright test --project=quarantine
```

Confirm selector audit emits numbers: the stability report lists a score per locator
and a suite average.

## Done When

- Every flaky test is identified and categorized by root cause (timing, data
  dependency, environment, etc.).
- Each flaky test is quarantined or fixed — no test silently retried without a
  documented plan and ticket reference.
- `selector-stability.md` (or the CI report) lists a stability score per locator and
  reports a suite average >= 3.5.
- The flaky-test-rate metric (% of tests passing on retry) is published to the CI
  dashboard and visible to the team.
- Every quarantine entry has a ticket reference and an expiry date <= 14 days out.
- Fix recommendations are routed through the locked loop (test fixes to Bailey, env/
  config fixes to Erwin), and Gordon retests to qualification before James accepts.

## Related Skills (factory lanes)

- **test-environments** (Gordon) — environment diagnosis and parity that separate env
  flakes from test bugs.
- **ci-cd-integration** (Gordon) — pipeline configuration, parallel execution, and the
  quarantine job wiring referenced above.
- **ai-test-generation** / **test-planning** / **qa-project-context** (Bailey) — the
  authoring side that produces the tests Gordon triages; context carries selector
  strategy and known flaky areas.
- **release-readiness** (Gordon) — flake health feeds release qualification; a flaky
  suite cannot ship a qualified release.
- When flake investigation reveals a real app bug, hand the failure to the factory
  triage/issue flow to classify and report it.
