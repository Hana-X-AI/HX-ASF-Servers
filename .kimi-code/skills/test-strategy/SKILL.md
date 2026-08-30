---
name: test-strategy
description: "Produce a multi-quarter QA strategy document for the HX factory's QA lane (Bailey): scope, risk-based prioritization, test levels (unit/integration/E2E), pyramid analysis, entry/exit criteria, quality KPIs, tool selection rationale, CI scaling levers, and a phased timeline. Use when: 'test strategy', 'QA strategy doc', 'testing approach', 'QA roadmap', 'multi-quarter QA direction'. NOT for: a single-sprint or single-release plan (test-planning), or identifying which areas carry the most risk (risk-based-testing first). Adapted from petrkindlmann/qa-skills v3.0.0 (MIT)."
---

# Test Strategy — multi-quarter QA direction (Bailey)

Adapted from `petrkindlmann/qa-skills` v3.0.0 (MIT) into the HX factory's QA workflow.
Owner: **Bailey** (Sr. AI Testing Engineer, QA family). This skill produces the
multi-quarter QA strategy document; Gordon executes and qualifies against it, Mia
coordinates, James accepts direction. Deliverable lands at
`governace/qa/<project-name>/test-strategy.md`.

**Bailey's hard boundary:** Bailey authors the strategy and its plans. She does NOT set
up environments, execute tests, fix configuration, or accept work. Execution and
qualification are Gordon's lane; acceptance is James's. A strategy is a document, not a
license to execute.

<objective>
Generate an actionable QA strategy tailored to the product, team, and risk profile — a
document that drives daily testing decisions, not a compliance artifact that collects
dust. A team with 150 E2E tests and a 52-minute pipeline thinks it has good coverage;
this skill diagnoses the inverted pyramid, prescribes the rebalance, and ties every
element to a measurable KPI.
</objective>

## Discovery Questions

Before writing a single line of strategy, gather context. Check
`governace/qa/<project-name>/qa-project-context.md` first — if it exists, use it as the
foundation and skip questions already answered there.

### Product & Business Context
- What is the product? (SaaS, e-commerce, API platform, mobile app, content site)
- Who are the users? (consumers, enterprise, internal, developers)
- What are the business-critical flows? (signup, checkout, payment, data export)
- What is the release cadence? (continuous, weekly, bi-weekly, quarterly)
- What compliance requirements exist? (SOC2, HIPAA, PCI-DSS, GDPR, EU AI Act)

### Current Testing State
- What test levels exist today, and the current count at each level?
- What frameworks and tools are in use? (Factory default: python/pytest; zod for TS
  contract tests; Playwright where browser E2E genuinely matters.)
- Current code coverage, and the target if any?
- How long does the CI pipeline take end-to-end?
- What is the current flakiness rate?

### Pain Points & Goals
- Biggest quality pain points? (regressions, slow feedback, flaky tests, gaps)
- What broke in the last 3 releases? What escaped to production?
- What does "good enough quality" look like for this team?
- Appetite for investment in test infrastructure?

### Team & Constraints
- Team composition by factory lane (Bailey/Gordon/Erwin/Mia/James) and capacity.
- Skill levels with automation tools.
- Budget constraints for tooling.
- Timeline pressure — is there a deadline driving this strategy?

> **Calibrate to maturity** (set `team_maturity` in the QA project context):
> - **startup** — Minimal pyramid: unit tests + a handful of critical E2E paths. Skip
>   contract testing and formal metrics until CI runs reliably. Phase 1 under 4 weeks.
> - **growing** — Full pyramid with defined coverage targets, flakiness thresholds, and
>   CI quality gates. Add risk-based prioritization.
> - **established** — SLA-backed quality gates, multi-environment coverage, advanced
>   tooling (contract testing, chaos, observability), and formal review cadence.

## Core Principles

1. **Risk-based prioritization over exhaustive coverage.** Not all code is equal — a
   payment bug costs 1000x more than a tooltip typo. Allocate testing effort
   proportional to business risk, not code volume. The risk matrix drives where to
   invest; run the risk assessment first if no matrix exists yet.
2. **Test pyramid health is the leading indicator.** A healthy suite is many fast unit
   tests, fewer integration, fewest E2E. When the shape inverts (ice cream cone)
   feedback is slow, maintenance is high, and confidence is paradoxically low.
   Diagnose the current shape before prescribing anything.
3. **Shift-left: catch defects earlier.** Every defect found later costs exponentially
   more. Push validation earlier — static analysis before tests, unit before
   integration, contract before E2E. Design reviews catch architecture bugs no test can
   find.
4. **Every strategy element has a KPI.** If you cannot measure it, you cannot improve
   it. Coverage targets, flakiness thresholds, escape-rate goals, MTTR limits — each
   section names a number and a tracking cadence.
5. **Living document, not a shelf document.** Reviewed quarterly at minimum. It carries
   a revision history, a named owner per section, and explicit re-evaluation triggers
   (new product area, team change, major incident, defect escape).

## Strategy Document Template

Walk through each section to produce the final document. Tailor depth to complexity — a
5-person startup needs 5 pages, not 50. The final document follows a 13-section
structure (Executive Summary through Revision History).

### 0. Executive Summary

A 3-5 sentence snapshot a non-technical reader can absorb in one minute: what the
strategy covers, the top 2-3 priorities, the headline quality targets, and the owner.
Write it last but place it first — it is the reader's entry point and the anchor for
the numbered sections below.

### 1. Scope & Objectives

Define boundaries clearly. Ambiguity here causes gaps and wasted effort downstream.

- **In scope:** every product area, service, and integration this strategy covers;
  functional and non-functional types; platforms and browsers/devices.
- **Out of scope:** state what is NOT covered and why — third-party services tested
  only at the contract level, legacy systems slated for deprecation.
- **Objectives:** 3-5 measurable objectives with timelines, e.g. "Reduce defect escape
  rate from 12% to under 5% within two quarters," "Achieve 80% unit coverage on all
  services launched after Q1 2026."

### 2. Test Levels & Types

Define each level, what it covers, who owns it, and expected volume. Map owners to the
factory lanes: developers (engineering lanes) own unit; Bailey authors the plan and
tests; Gordon qualifies through execution.

| Level | What It Validates | Owner | Framework | Target Count | Run Frequency |
|-------|-------------------|-------|-----------|-------------|---------------|
| **Unit** | Functions, business logic, edge cases | Developers | pytest | 70-80% of all tests | Every commit |
| **Integration** | Service interactions, DB queries, API contracts | Bailey + Gordon | pytest + Testcontainers (where authorized) | 15-20% of all tests | Every PR |
| **E2E** | Critical user journeys through the full stack | Gordon | pytest/Playwright | 5-10% of all tests | Pre-deploy + nightly |
| **API** | Contract compliance, schemas, error handling | Developers | pytest / zod (TS contract) | Per endpoint | Every PR |
| **Visual** | UI regression, layout shifts, responsive | Gordon | Playwright/Argos/Chromatic | Key pages | Nightly |
| **Performance** | Response times, throughput, resource usage | Gordon | k6/Lighthouse | Critical paths | Weekly + pre-release |
| **Security** | OWASP Top 10, dep vulns, auth flows | Gordon | OWASP ZAP/Snyk | Per release | Pre-release + scheduled |
| **Accessibility** | WCAG 2.2 AA, screen reader compat | Gordon | axe-core | Key flows | Every PR |

Adjust to what the product actually needs. Not every product needs visual regression.
Every product needs unit and integration tests.

### 3. Test Pyramid Analysis

Diagnose the current shape, then define the target.

**Shapes.** The suite takes one of four shapes — healthy pyramid (many unit, few E2E),
ice cream cone (inverted, E2E-heavy), diamond (integration-heavy), or hourglass
(unit-heavy and E2E-sparse with a missing integration middle). Each signals a different
feedback/maintenance trade-off.

**Current state.** Count tests at each level, compute the percentage split, identify
the shape, then capture CI duration, flaky rate, and pass rate.

**Target state.** Define target ratios (70-80% unit, 15-20% integration, 5-10% E2E)
with concrete counts, plus target CI duration and flaky rate.

**Action plan — if ice cream cone or diamond:**
1. **Freeze E2E growth** — no new E2E tests unless covering a net-new critical path.
2. **Decompose existing E2E** — find E2E tests validating logic testable at unit level
   (a checkout test asserting tax math becomes a unit test on the tax function), rewrite
   them down a level.
3. **Add unit requirements to the PR checklist** — every PR touching business logic
   ships unit tests.
4. **Set CI gates** — fail PRs where the unit:E2E ratio drops below threshold.

Before rebalancing, separate genuinely flaky E2E tests from ones exposing real bugs —
quarantining a flaky test that hides a race condition is how the regression escapes.
For flake root-cause triage and quarantine mechanics, see `test-reliability` (Gordon).

**Action plan — if hourglass:**
1. **Invest in integration infrastructure** — DB fixtures, service stubs, contract tests.
2. **Identify service boundaries** — each boundary needs integration tests for happy
   path + error cases.
3. **Use contract testing** for inter-service communication.

### 4. Risk Assessment Matrix

Map features to risk levels — this directly determines testing depth. Score each
feature as Impact (1 Negligible → 5 Catastrophic) × Likelihood (1 Rare → 5 Almost
Certain); the product (1-25) maps to LOW/MED/HIGH/CRIT bands.

| Risk Level | Testing Action | Automation | Monitoring |
|------------|---------------|------------|-------------|
| **CRITICAL (15-25)** | Full automation + manual exploratory + load test | Mandatory, every commit | Real-time alerts, synthetic monitoring |
| **HIGH (10-14)** | Full automation + periodic manual review | Mandatory, every PR | Dashboard + daily checks |
| **MEDIUM (5-9)** | Automation for happy path + key error cases | Recommended | Weekly review |
| **LOW (1-4)** | Manual testing or skip | Optional | None required |

**Example mapping:**

| Feature Area | Impact | Likelihood | Score | Testing Approach |
|-------------|--------|------------|-------|-----------------|
| Payment processing | 5 - Catastrophic | 3 - Possible | 15 - CRIT | Automated E2E + unit + contract + monitoring |
| User authentication | 5 - Catastrophic | 2 - Unlikely | 10 - HIGH | Automated E2E + security scan + unit |
| Product search | 3 - Moderate | 3 - Possible | 9 - MED | Unit + integration + happy-path E2E |
| Dashboard rendering | 2 - Minor | 3 - Possible | 6 - MED | Unit + visual regression |
| Email preferences | 1 - Negligible | 2 - Unlikely | 2 - LOW | Manual verification |

### 5. Environment Strategy

| Environment | Purpose | Test Types | Data | Deploy Trigger |
|------------|---------|------------|------|---------------|
| **Local** | Developer feedback | Unit, integration | Mocked/seeded | On save |
| **CI** | Automated validation | Unit, integration, lint, SAST | Ephemeral | On push/PR |
| **Staging** | Pre-production validation | E2E, visual, performance, security | Production-like (anonymized) | On merge to main |
| **Production** | Monitoring & smoke | Smoke tests, synthetic monitoring | Live | On deploy |

Document: how test data is managed per environment, whether environments are ephemeral
or long-lived, who has access, and how environment-specific config is managed. The
HX deployment shape is native systemd services (no Docker/containers per owner rule
2026-08-27) — see `test-environments` (Gordon) for the parity posture that follows.

### 6. Tool Selection Rationale

Do not pick tools first. Understand needs, then select tools that fit. Score each
candidate against weighted criteria.

| Criteria (weight) | Tool A | Tool B | Tool C |
|-------------------|--------|--------|--------|
| **Fits tech stack** (25%) | | | |
| **Team familiarity** (20%) | | | |
| **Community & docs** (15%) | | | |
| **CI integration** (15%) | | | |
| **Maintenance cost** (10%) | | | |
| **Speed of execution** (10%) | | | |
| **License cost** (5%) | | | |
| **Weighted total** | | | |

Score each 1-5, multiply by weight, sum for the weighted total. Beyond license fees,
account for **total cost of ownership**: setup time, writing time, maintenance time,
debug time, and infrastructure cost.

**Common stack starting points** — document why you chose or deviated:

| Product Type | Unit | Integration | E2E | API | Visual |
|-------------|------|-------------|-----|-----|--------|
| Python API | pytest | pytest + Testcontainers (where authorized) | pytest + requests | Schemathesis | N/A |
| React/Next SaaS | Vitest | Testing Library + MSW | Playwright | Supertest | Playwright screenshots |
| TS services | Vitest/Jest | pytest/zod contract tests | Playwright | zod / Supertest | Playwright screenshots |
| Mobile (RN) | Jest | Testing Library + MSW | Detox / Maestro / Appium 3.x | Supertest | Appium screenshots |
| AI/LLM features | Vitest | DeepEval | Playwright + Promptfoo evals | Promptfoo / Ragas | N/A |

For AI/LLM features, add explicit risk testing for hallucinations, bias, prompt
injection, and privacy — directly relevant to the HX LLM-server fleet.

**Reference frameworks (citations kept from upstream):**
- **CTAL-AT v2.0** (ISTQB, Advanced Agile Tester, 2026) — test strategy and approach,
  whole-team approach, shift-left, end-to-end testing, test smells, exploratory +
  AI-assisted testing.
- **CT-GenAI v1.1** (ISTQB, 2026-04-27) — LLM-powered test infrastructure as a
  discipline; AI-specific risk classes (hallucinations, reasoning errors, bias,
  privacy, AI regulations).
- **CTFL v4.0** (ISTQB) — foundational vocabulary for aligning teams from different
  testing traditions.
- **HTSM v6.3** (Bach) — Heuristic Test Strategy Model; state-based testing and
  boundary heuristics.
- **World Quality Report 2025-26** (Capgemini, 17th ed.) — benchmark data for placing
  your AI-adoption stage.

### 7. CI Scaling Levers

When the suite or team grows, CI wall-clock time is the constraint that breaks the
strategy. Pull these levers before deleting tests:

- **Sharding** — split the suite across N parallel runners (Playwright `--shard`,
  pytest-xdist, etc.). Linear speedup until per-shard fixed costs dominate.
- **Test impact analysis** — run only tests affected by the diff instead of the whole
  suite on every PR. Keep the full suite on a nightly/merge gate so nothing rots.
- **Caching** — cache dependencies, build artifacts, and browser binaries between runs.
- **Selective E2E on PR** — run smoke E2E on PRs, full E2E on merge/nightly.

Measure the payoff, do not assume it. **Parallel efficiency = summed test-run time ÷
wall-clock time**; target a value approaching the shard count (e.g. >3x on 4 shards).
Track **CI-minutes-per-PR** to catch parallelization that cuts wall-clock time but
balloons billed compute.

### 8. Entry/Exit Criteria

Define what must be true before testing starts (entry) and before it is done (exit) at
each level.

**Unit** — Entry: code compiles, function has a documented contract (inputs/outputs).
Exit: all branches covered, edge cases tested, no skipped tests, coverage target met.

**Integration** — Entry: unit tests pass, dependent services available or stubbed, test
data seeded. Exit: all service boundaries tested, error paths validated, no flaky tests.

**E2E** — Entry: integration tests pass, staging deployed, test accounts provisioned.
Exit: all critical user journeys pass, no P0/P1 defects open, performance within SLA.

**Release** — Entry: all test levels pass, no CRITICAL/HIGH defects open, release notes
drafted. Exit: smoke tests pass in production, monitoring shows no anomalies for an
agreed bake window (30 min is a reasonable default), rollback plan verified.

### 9. Quality Gates & Definition of Done

Automated gates that prevent bad code from moving forward.

**PR gate** (every PR): unit tests pass; integration tests pass; coverage does not
decrease (or meets minimum); no new lint errors; SAST scan passes (no new
high/critical); bundle size within threshold; at least one reviewer approval.

**Merge gate** (merge to main): all PR-gate checks pass; E2E smoke suite passes against
a preview deployment; no merge conflicts; branch up to date with main.

**Deploy gate** (before production): full E2E suite passes on staging; performance
benchmarks within range; security scan passes; feature flags configured; rollback plan
documented and tested.

**Nightly gate** (scheduled): full E2E including edge cases; visual regression;
performance/load tests; accessibility scan; dependency vulnerability scan. Results
reviewed by the QA lane next morning.

Every gate names a concrete pass/fail threshold and is enforced in CI — a gate that can
be clicked past is documentation, not a gate.

### 10. Metrics & KPIs

| Metric | Definition | Target | Cadence |
|--------|-----------|--------|---------|
| **Code Coverage** | Lines/branches covered by unit + integration | >80% critical services, >60% overall | Per PR |
| **Test Pyramid Ratio** | Unit:Integration:E2E split | 70:20:10 (±10% tolerance) | Monthly |
| **Flakiness Rate** | % of runs with non-deterministic failures | <2% | Weekly |
| **Defect Escape Rate** | % of defects found in prod vs. total | <5% | Per release |
| **MTTR** | Detection to fix deployed | <4h P0, <24h P1 | Per incident |
| **CI Pipeline Duration** | Push to green/red signal | <15 min PR, <30 min full | Weekly |
| **CI Parallel Efficiency** | Summed test time ÷ wall-clock time | Approaching shard count (>3x on 4 shards) | Weekly |
| **CI-Minutes-per-PR** | Billed compute minutes per PR run | Flat or decreasing | Monthly |
| **Defect Density** | Defects per 1000 LOC | Decreasing trend | Monthly |
| **Automation Rate** | % of test cases automated | >80% for regression suite | Quarterly |
| **False Positive Rate** | % of failures that are not real bugs | <5% | Weekly |

**Using metrics:** track trends over time, not absolute numbers. Set realistic targets
from current state. Review quarterly with the lanes; celebrate improvements.
Investigate spikes — a sudden flakiness jump signals infrastructure, not laziness.
Never use metrics to punish teams.

### 11. Timeline & Milestones

Roll out in phases. Doing everything at once guarantees nothing gets done well.

**Phase 1 — Foundation (Weeks 1-4):** risk assessment for all product areas; CI
pipeline with unit-test gate; baseline metrics; unit tests for top 5 highest-risk
areas; select and configure the E2E framework. *Exit: CI runs unit tests on every PR,
baseline metrics documented.*

**Phase 2 — Coverage Expansion (Weeks 5-10):** integration tests for all service
boundaries; E2E for top 10 critical journeys; visual regression for key pages; test
data management; nightly runs. *Exit: all critical paths have E2E coverage, integration
tests cover all APIs.*

**Phase 3 — Quality Gates (Weeks 11-14):** coverage gates on PRs; performance
benchmarks in CI; security scanning; monitoring dashboards for all KPIs. *Exit: all four
gates (PR, merge, deploy, nightly) active and enforced.*

**Phase 4 — Optimization (Weeks 15-20):** fix or quarantine flaky tests; CI scaling
levers; synthetic monitoring in production; first quarterly strategy review. *Exit: CI
under 15 min, flakiness under 2%, first strategy revision published.*

**Ongoing:** quarterly strategy review and revision; monthly metrics review;
continuous maintenance (refactor, de-flake, retire).

### 12. Revision History

Track every change to the strategy so readers can see what moved and when. Each entry:
date, author/owner, a one-line summary of the change, and the trigger (quarterly review,
incident, new product area, team change). The first entry records creation; later entries
are appended — never silently rewrite a prior status, target, or decision (append-only
governance, consistent with the repository's documentation conventions).

## Anti-Patterns

**100% coverage targets.** Diminishing returns past 80%. Set coverage per module by
risk, not a blanket number.

**Ice cream cone (inverted pyramid).** Too many E2E, too few unit. Fix by freezing E2E
growth and decomposing existing E2E into lower levels.

**Strategy as a one-time document.** Written once and never updated is worse than none.
Build in review triggers: quarterly calendar review, post-incident, new product area,
team composition change.

**Tool-first thinking.** "We should use Playwright" is a tool choice masquerading as a
plan. Start from what you need to validate, then pick tools that fit.

**No metrics = no accountability.** A strategy without measurable targets is a wish
list. Every section connects to a KPI.

**Testing in isolation.** A strategy living only in the QA folder is invisible to the
engineering lanes. It must live in PR templates, CI gates, and the Definition of Done.

**Copy-paste strategy.** Templates are starting points; every section is tailored to the
factory's risk profile, lanes, and constraints.

**Automating everything immediately.** Manual exploratory testing has enormous value,
especially early. Automate regression, keep exploration manual.

**Crossing the boundary.** Bailey writes the strategy; Gordon executes and qualifies;
James accepts. A strategy document does not grant execution authority.

## Verification

Prove the produced document is complete before calling it done. Run against the saved
strategy file (`governace/qa/<project-name>/test-strategy.md`):

```bash
DOC=governace/qa/<project-name>/test-strategy.md
# 1. All 13 numbered section headings present (Executive Summary → Revision History)
grep -cE '^### [0-9]+\.' "$DOC"          # expect 13
# 2. Every row in the Metrics & KPIs table has a non-empty Target cell — visually scan
grep -nE '^\|' "$DOC" | grep -iE 'target|coverage|flak|mttr|escape'
# 3. A revision history and a named owner exist
grep -niE 'revision history|owner:' "$DOC"
```

Then sanity-check the pyramid math by hand: target unit% + integration% + E2E% should
sum to ~100%. If the document recommends sharding, confirm a parallel-efficiency or
CI-minutes target appears in the Metrics table — an optimization with no metric is a
guess.

## Done When

- [ ] A strategy document exists at `governace/qa/<project-name>/test-strategy.md` and
      `grep -cE '^### [0-9]+\.'` returns 13 (all sections Executive Summary → Revision
      History populated).
- [ ] Test pyramid target ratios are defined with concrete counts and a timeline to
      reach them; unit+integration+E2E percentages sum to ~100%.
- [ ] Entry and exit criteria are written for each level (unit, integration, E2E, release).
- [ ] Tool selection is documented with a scored, weighted rationale matrix — not just
      tool names.
- [ ] Quality gates are defined for all four stages (PR, merge, deploy, nightly), each
      with a concrete pass/fail threshold.
- [ ] Every Metrics & KPIs row has a non-empty Target and a tracking cadence.
- [ ] The strategy is handed to Gordon (execution/qualification) and Mia
      (coordination); Bailey authors, Gordon qualifies, James accepts.

## Related Skills (factory lanes)

- **qa-project-context** (Bailey) — the Risk Areas, Quality Goals, and Team input this
  strategy consumes.
- **test-planning** (Bailey) — single sprint/release plans; test-strategy is the
  multi-quarter umbrella above them.
- **test-reliability** / **test-environments** / **ci-cd-integration** (Gordon) — flake
  triage, env parity, and pipeline wiring the strategy prescribes.
- **release-readiness** (Gordon) — go/no-go checklists and release confidence scoring
  for the release gate.
- When the strategy covers AI/LLM features (HX LLM-server fleet), define the eval-suite
  layer explicitly.
