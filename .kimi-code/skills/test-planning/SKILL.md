---
name: test-planning
description: "Author sprint/release test plans for the HX factory's QA lane (Bailey): feature decomposition into testable scenarios, requirements-to-test coverage mapping, effort estimation by test type, risk×effort prioritization, resource allocation, and buffered scheduling. Use when: 'sprint test plan', 'release test plan', 'what to test this sprint', 'test estimation', 'coverage mapping'. NOT for: multi-quarter strategy (test-strategy), ranking areas by risk (risk-based-testing), or the go/no-go decision itself (release-readiness / James's acceptance). Adapted from petrkindlmann/qa-skills v3.0.0 (MIT)."
---

# Test Planning — sprint and release test plans (Bailey)

Adapted from `petrkindlmann/qa-skills` v3.0.0 (MIT) into the HX factory's QA workflow.
Owner: **Bailey** (Sr. AI Testing Engineer, QA family). This skill is the **authoring**
lane: Bailey writes the plan; Gordon sets up env + executes + retests; James accepts.
Follow the locked test loop (max 3 retest iterations) and land the plan at
`governace/qa/<project-name>/test-plan-<id>.md`.

**Bailey's hard boundary:** Bailey produces the test plan + test scripts + pinned
stack only. She does NOT set up environments, execute tests, fix configuration, or
accept work. Env setup + execution + retest is Gordon's lane; acceptance is James's
(verified on `governace/process/governor-verification-checklist.md`).

<objective>
Create actionable test plans for sprints and releases. A test plan answers four
questions: what to test, how deeply, who does it, and when it must be done. The output
is a living document that tracks progress, not a bureaucratic artifact filed and
forgotten. A plan that schedules 100% of available time fails the moment the first bug
is found — buffer and prioritization are what make it survive contact with reality.
</objective>

## Quick Route

| Situation | Go to |
|-----------|-------|
| Plan a single sprint | Steps 1-6 below; keep the sprint plan to one page |
| Plan a release | Release test plan (aggregates sprint plans); the go/no-go decision itself belongs to `release-readiness` (Gordon) and James's acceptance |
| Track an in-flight plan / feed results back | Daily status + retrospective formats below |
| Decide what to cut when over capacity | Step 4 prioritization matrix |

## Discovery Questions

Before writing a test plan, gather context. Check
`governace/qa/<project-name>/qa-project-context.md` first — if it exists, use it as the
foundation and skip questions already answered there.

### Scope

- What is the scope? (single sprint, release, hotfix, feature)
- Which features are new vs. changed vs. unchanged?
- Which features are being released for the first time?
- Are there infrastructure or dependency changes (database migrations, API version
  bumps, third-party provider switches)?
- Is there a requirements document, PRD, or set of user stories to map against?

### Time and Resources

- What is the testing window? (days, hours available)
- Who is available for testing? Factory lanes: Bailey authors, Gordon executes/qualifies,
  Erwin fixes config, Mia coordinates, James accepts. Note which lanes have capacity.
- Are there shared resources that could bottleneck? (test environments, test accounts,
  devices)
- Is there a hard deadline that cannot move, or is the release date flexible?

### Risk Context

- Which areas changed the most in this cycle?
- What broke in the last release or sprint?
- Are there known fragile areas or tech debt that increase risk?

### Existing Coverage

- What automated tests already exist for the in-scope features?
- What is the current pass rate of the automated suite?
- Are there known gaps in automation that require manual testing?
- When was the last exploratory testing session on these features?

## Core Principles

### 1. Coverage-Driven: Map Every Requirement to at Least One Test

A test plan without traceability to requirements is a guess. Every user story,
acceptance criterion, or requirement must map to at least one test case. Gaps in this
mapping are untested requirements — the most dangerous kind of risk.

### 2. Time-Boxed: Plan Fits the Available Window

Testing expands to fill available time if unbounded. Set a time box for each activity
and stick to it. When the window is too short, the prioritization matrix determines
what gets cut — not gut feeling.

### 3. Prioritized: Not Everything Gets Equal Depth

A payment flow change and a tooltip fix do not deserve equal effort. Use the risk ×
effort matrix to allocate depth: some features get full regression, others a smoke
test, some nothing if low-risk and unchanged.

### 4. Buffered: Leave Room for the Unexpected

Plans that schedule 100% of available time fail when bugs are found. Allocate only
70-80% of the testing window to planned work and explicitly reserve the remaining
20-30% for bug verification, re-testing, and unplanned investigation. If buffer is not
a named line in the plan, you do not have one.

### 5. Visible: The Plan Is a Communication Tool

Developers need to know what gets tested to write testable code. Product managers need
coverage visibility to make release decisions. Mia publishes the plan where the
factory lanes can see it.

### 6. Entry and Exit Criteria Are First-Class

The most-reused part of any plan is its gate. Make it explicit, not buried: **entry** =
code-complete on staging + existing suite green + test data seeded; **exit** = every
HIGH-risk area covered + no open P0/P1 + zero unexplained GAP rows in the coverage
matrix. Everything else is detail around these two checkpoints.

## Workflow

Six workflow steps. The decision prose stays here; Bailey fills the plan document as
she goes.

### Step 1: Feature Analysis and Decomposition

Break each in-scope feature into testable units. A "testable unit" is a specific
behavior that can be verified with a clear pass/fail outcome. Walk every feature
against these scenario categories so none gets skipped:

- **Happy path** — the primary success flow.
- **Validation** — required fields empty, format violations, boundary values.
- **Error conditions** — server 5xx, network timeout, rejected input.
- **Edge cases** — unicode, oversized payloads, unsupported formats.
- **Concurrency / race conditions** — two users edit the same record simultaneously,
  double-submit, retry-after-timeout. These hide the worst data-corruption bugs and are
  the category most often missed.
- **Integration points** — behavior across each boundary the feature crosses.

> **AI decomposition cross-check.** When an agent decomposes features, have it
> immediately map its own scenarios back against the Step 2 coverage matrix. Any
> requirement with no scenario, or any scenario category above with no entry, is a
> decomposition gap the agent must surface before estimation — this is how you catch
> the agent's blind spots, not after Gordon does in CI.

### Step 2: Requirements-to-Test Coverage Mapping

Create a traceability matrix that maps every requirement to its test cases.

Rules for the coverage matrix:
- Every requirement must appear in the matrix (target: 100% mapping)
- "GAP" status triggers a decision: write a test, accept the risk, or defer
- Automated tests get test IDs that link to the actual test file/function
- Manual tests reference the test case document or charter

### Step 3: Effort Estimation

Estimate effort for each test type using historical data. If no historical data exists,
use the reference estimates below and calibrate after the first sprint.

**Estimation reference (per test case):**

| Test Type | Write Time | Execute Time | Maintenance (per quarter) |
|-----------|-----------|-------------|--------------------------|
| Unit test | 0.5 hr | < 1 sec | 5 min |
| Integration test | 1 hr | 5-30 sec | 15 min |
| E2E test (pytest/Playwright) | 2-3 hours | 30s-2 min | 30 min |
| Manual test case (write) | 0.25 hr | 5-15 min per execution | 10 min |
| Exploratory session (charter) | 15 min | 1.5 hrs per session | N/A |
| Accessibility review (manual) | 0.5-1 hr per area | included in write | 15 min |
| Visual regression test | 30-60 min | 10-30 sec | 20 min (baseline updates) |
| Performance test (k6 script) | 2-4 hours | 5-30 min per run | 30 min |
| Setup & test data (per feature) | 0.5-2 hrs | one-time | re-seed per env |

Write Time is authoring only. The "Setup & test data" row is the line planners most
often omit — environment, fixtures, and mock configuration routinely run 20-40% of
total effort, so budget it as a real line rather than discovering it mid-sprint. In the
HX factory this is Gordon's lane (env setup + seeding), but Bailey must budget for it
in the plan.

> **AI authoring trade-off.** Using an agent to author tests cuts *Write Time* by
> roughly 40-60%, but add a *Review Time* line of similar size per case — the
> speed-up evaporates when an agent ships plausible-but-broken tests that pass a casual
> review and fail in CI. See `ai-test-generation` Step 7 for the review checklist.

> **Test-smells review.** Budget a recurring 30-min "test-smells review" per sprint.
> Cheap, and it finds maintenance debt before it compounds.

Use a sprint estimation worksheet to roll per-case estimates up to a
capacity-utilization figure (target: 70-80%, leaving 20-30% buffer).

### Step 4: Prioritization Matrix (Risk x Effort)

When the estimated effort exceeds available capacity (it usually does), use the risk ×
effort matrix to decide what to cut.

For each test case, plot it on the matrix using the risk score and the effort estimate
from Step 3, then consume capacity in priority order: **DO FIRST → DO SECOND → DO THIRD
→ DEFER → SKIP**.

**Tie-break rule:** within HIGH risk, low-effort beats high-effort — a HIGH-risk /
low-effort test (DO FIRST) outranks a HIGH-risk / high-effort test (DO THIRD), because
it buys the most risk reduction per hour. Medium-risk items defer before you cut any
HIGH-risk coverage; low-risk items defer or skip entirely. Never cut buffer to fit more
planned work.

### Step 5: Resource Allocation

Assign testing work based on skill match and availability — in the factory this means
lane match, not personal assignment.

**Allocation principles (factory-mapped):**
- Test plan + scripts → Bailey (author).
- Environment setup, seeding, execution, retest → Gordon (qualification).
- Configuration fixes surfaced by failures → Erwin.
- Coordination and status reporting → Mia.
- Final acceptance → James on the governor verification checklist.
- New feature testing benefits from fresh eyes — the independent qualification lane
  (Gordon) is deliberately separate from the authoring lane.
- Each lane's load stays at 70-80% utilization, not 100% — the rest is buffer.

### Step 6: Schedule with Buffers

Map testing activities to the sprint timeline. Testing should not be back-loaded to the
last two days.

**Key scheduling rules:**
- Testing starts as soon as features are code-complete, not at sprint end
- Environment setup and test data preparation happen on Day 1, not Day 3
- Bug verification is continuous, not batched
- The last day is for confirmation, not for starting new testing
- The locked test loop allows max 3 retest iterations; schedule them explicitly

## Plan Documents

- **Sprint Test Plan (1-Page)** — scope, coverage summary, effort budget, entry/exit
  criteria, plan risks. Keep a sprint plan to one page.
- **Release Test Plan** — aggregates sprint plans and adds release-specific concerns
  (full regression, perf benchmark, security scan, smoke test) plus go/no-go criteria.
  The go/no-go *decision* itself belongs to `release-readiness` (Gordon) and James's
  acceptance.
- **Feature Coverage Matrix** — per-feature scenario list with priority, test type,
  location, and status.
- **Test Estimation Worksheet** — new-test development, existing-suite execution,
  manual testing, and a summary delta vs. available capacity.

Deliverables land at `governace/qa/<project-name>/`. Before a plan is marked complete,
register it in the document catalog (`knowledge/catalog/` — DOC record + index line) and
record its disposition, so the plan has a catalog receipt; a plan is not complete until
the catalog registration and disposition are recorded. The other QA skills in this
library apply the same catalog-registration requirement to their generated deliverables.

## Tracking Progress During the Sprint

A test plan is useless if nobody checks it after Day 1. Track progress daily, and feed
the results back into future planning at sprint end.

- **Daily test status** — completed, blocked, bugs found, tomorrow's plan, coverage
  percentage, and buffer consumed. Gordon's execution results go to the testing log and
  Gordon notifies Bailey + Erwin per the locked test loop.
- **Sprint retrospective inputs** — estimation accuracy broken out by test type,
  coverage delta, bug counts by severity, and lessons. Feed these data points into the
  next sprint's estimates.

## Anti-Patterns

### Planning Without Risk Assessment

Treating every feature with equal depth wastes effort on low-risk areas and under-tests
critical paths. Always run the prioritization matrix (Step 4) before allocating effort.

### No Buffer for Bug Discovery

Scheduling 100% of available hours for planned activities leaves no time for
verification when bugs are found. Reserve 20-30% as buffer and track consumption daily.

### Back-Loading Testing to Sprint End

Leaving all testing for the last two days rushes coverage and surfaces bugs too late to
fix. Start testing as features become available; continuous testing beats batch testing.

### Test Plan as Compliance Artifact

A 30-page plan filed and forgotten helps nobody. The plan should be one page for a
sprint, actively tracked, and updated daily. If the plan is not changing, nobody is
using it.

### Estimating Without Historical Data

Effort estimates pulled from thin air are unreliable. Track actual time spent — broken
out by test type — and use that data for future estimates. After 2-3 sprints, estimates
become reliable.

### Ignoring Environment and Data Setup

Environment setup, test data creation, and mock configuration can consume 20-40% of
testing effort. Include the "Setup & test data" row from Step 3 in the estimate or the
plan will always run over.

### Single-Person Coverage on Critical Path

A single lane covering all critical-path work is a failure point. The author/qualifier
split (Bailey authors, Gordon qualifies) exists exactly to keep critical-path coverage
independent. Do not collapse it.

## Verification

Open the produced plan and confirm: every in-scope ticket ID from the sprint board
appears in the Scope table; the coverage matrix has zero unexplained GAP rows (each GAP
carries an accept/defer note); allocated capacity sums to 70-80% with a named buffer
line; and the entry/exit criteria checklists are filled, not placeholder. If any of
these fails, the plan is not done.

## Done When

- [ ] A sprint or release test plan document exists at `governace/qa/<project-name>/`
      with scope table, coverage summary, effort budget, and entry/exit criteria all
      filled in — no placeholders
- [ ] Every in-scope feature is decomposed into specific testable scenarios with
      pass/fail criteria, covering happy path, validation, error, edge, and concurrency
      categories
- [ ] A requirements-to-test coverage matrix exists with no unexplained GAP entries
      (every GAP has an accept-risk or defer note)
- [ ] Each scenario is estimated and plotted on the risk × effort matrix, with deferred
      items explicitly listed
- [ ] Allocated capacity is 70-80% with 20-30% buffer explicitly reserved as a named line
- [ ] Test data requirements, environment details, and resource allocation (by factory
      lane) are documented in the plan
- [ ] The plan is handed to Mia for coordination and Gordon for execution; Bailey does
      not execute or accept

## Related Skills (factory lanes)

- **test-strategy** (Bailey) — the broader QA strategy that test plans execute against;
  strategy defines the approach, plans implement it per sprint.
- **ai-test-generation** (Bailey) — the authoring pipeline that produces the test code a
  plan schedules.
- **qa-project-context** (Bailey) — the project context file that provides baseline
  answers to discovery questions.
- **test-environments** / **test-reliability** / **ci-cd-integration** (Gordon) — env
  setup, flake triage, and pipeline wiring the plan's execution depends on.
- **release-readiness** (Gordon) — the go/no-go decision that the release test plan's
  exit criteria feed into; this skill builds the plan, that one makes the ship call,
  James accepts.
