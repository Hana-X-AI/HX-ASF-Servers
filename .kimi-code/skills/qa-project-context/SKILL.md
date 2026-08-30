---
name: qa-project-context
description: "Create and fill the QA project context file at governace/qa/<project-name>/qa-project-context.md — the single file every other QA skill reads first for the project's tech stack, test frameworks, environments, quality goals, risk areas, and conventions (Bailey authors it). Use when: 'set up QA context', 'configure testing', first use of any QA skill on a project. NOT for: bootstrapping a brand-new project's QA end-to-end, or setting up/executing test environments (Gordon's lane). Adapted from petrkindlmann/qa-skills v3.0.0 (MIT)."
maturity: active
---

# QA Project Context — the one file every QA skill reads (Bailey)

Adapted from `petrkindlmann/qa-skills` v3.0.0 (MIT) into the HX factory's QA workflow.
Owner: **Bailey** (Sr. AI Testing Engineer, QA family). This skill authors the QA
project context file at `governace/qa/<project-name>/qa-project-context.md` — the
factory's replacement for the upstream repo's `.agents/qa-project-context.md`
convention.

**Bailey's hard boundary:** Bailey authors the context file (and its sibling plan/
scripts). She does NOT set up environments, execute tests, fix configuration, or accept
work. Env setup + execution + retest is Gordon's lane; acceptance is James's.

<objective>
This skill writes the single file every other QA skill reads. Without it, each skill
re-asks "what framework? what CI? where do tests live?" from scratch and gives generic
advice. It produces `governace/qa/<project-name>/qa-project-context.md`, capturing
product, tech stack, test stack, CI/CD, environments, quality goals, risk areas, team,
and conventions — with no `[bracketed placeholders]` left behind.
</objective>

Downstream skills consume specific sections: Risk Areas feeds the risk-based strategy;
Conventions feeds test authoring and reliability; Quality Goals feeds the metrics
practice; Tech Stack feeds every automation skill. Fill those sections well and the
rest of the library gets sharper for free.

## Discovery Questions

First, check whether the context file already exists — if it does, read it and skip
every section already filled (no `[brackets]`). Then scan the repo for config files (see
Codebase Detection) and present detected values for confirmation rather than asking
blind. Walk the remaining questions **section by section**, never all at once.

### Product
- What is the product called, and what does it do in one sentence?
- What type is it? (SaaS, e-commerce, media, mobile app, API service, internal tool) —
  changes which flows matter.
- What are the production, staging, and development URLs?
- What are the 5–10 most critical user journeys? ("If this breaks, we get paged at
  2am.") This list drives every other skill's coverage priorities.

### Tech Stack
- Frontend framework and language? Backend framework, language, and API style (REST,
  GraphQL, tRPC, gRPC)?
- Database, cache layer, ORM? Hosting, CDN, monitoring?
- Monorepo? If yes, list each app separately — sharding and detection differ.

### Test Stack
- E2E tests today? Framework, config location, test directory. Same for unit, API,
  visual, performance.
- If a framework is detected from config files, populate Test Stack with its name +
  version + path — don't re-ask.
- Zero test infrastructure? That's a valid answer; record "None selected yet" and note
  a default (see Core Principle 3). Factory default is python/pytest (zod for TS-side
  contract tests).
- Note which lane authors vs. executes each level (Bailey authors, Gordon qualifies).

### CI/CD
- Platform? When do tests run (every push, PR only, nightly, manual)? Sharding?
- What blocks a deploy, and what artifacts are saved (screenshots, reports, coverage)?

### Environments
- How many environments, with URLs? How close is staging to production (infra, data
  shape, third-party integrations)?
- HX posture: native systemd services (no Docker/containers per owner rule 2026-08-27);
  record the deployment shape so environment parity is assessed against it.
- Mock services or real APIs in development? — environment parity drives test reliability.

### Quality Goals
- Coverage targets today? Flake tolerance? Suite-duration budgets? Metrics tracked or
  wanted?
- No targets yet? Suggest realistic ones by maturity (see Quality Goals section).

### Risk Areas
- Which parts cause the most production incidents? Which integrations are flakiest
  (payment, email, third-party APIs)?
- Where is churn high and coverage low? Score everything with Impact × Likelihood (see
  Risk Areas section).

### Team
- Factory lanes that touch this project: Bailey (author), Gordon (env + execution +
  qualification), Erwin (config/fix), Mia (coordination), James (acceptance).
- When does QA engage (shift-left during spec, or after dev)? — sets the automation
  ownership model.

### Conventions
- Test file naming pattern? Co-located or separate? Branching strategy and PR
  requirements?
- Selector strategy for E2E? Test-data strategy (factories, fixtures, seeded DB,
  API-per-test)?

## Core Principles

1. **One file is the source of truth for the whole library.** Every skill reads
   `governace/qa/<project-name>/qa-project-context.md` first. Duplicating its facts into
   other docs guarantees drift — keep stack, goals, and risks here and let other skills
   reference them.

2. **Capture the real state, not the aspiration.** If there are no E2E tests, write
   "None selected yet," not a wish. Downstream skills route on what's true: a missing
   framework triggers a setup suggestion; a fake one sends them building on sand.

3. **Detect before you ask; recommend a default only when there's nothing to detect.**
   Read config files first and confirm what you find. Tool *recommendations* belong to
   the specialized skills — the one exception is a project with zero test
   infrastructure, where Bailey notes **pytest** (unit/integration, Python) and
   **Playwright** (E2E where a browser journey genuinely matters) as defaults and hands
   off to the relevant skill. This is the single carve-out to the "no recommendations"
   rule; everywhere else, just record.

4. **Risk Areas is the highest-leverage section — never skip it.** It is the direct
   input to the risk-based strategy. Push for at least 3–4 entries scored by impact and
   likelihood even when the user says "everything's fine."

## Codebase Detection

Scan for these before asking about the stack. Present detected values for confirmation;
when a test config is found, write the framework name into Test Stack rather than
re-asking.

| File | Indicates |
|------|-----------|
| `package.json` | Node.js project — check `dependencies` for the framework |
| `next.config.*` | Next.js |
| `nuxt.config.*` | Nuxt/Vue |
| `angular.json` | Angular |
| `astro.config.*` | Astro |
| `requirements.txt` / `pyproject.toml` | Python project (factory default: pytest) |
| `go.mod` | Go project |
| `playwright.config.*` | Playwright is set up → populate Test Stack E2E |
| `cypress.config.*` | Cypress is set up → populate Test Stack E2E |
| `pytest.ini` / `tox.ini` / `pyproject.toml [tool.pytest]` | pytest is set up → populate Test Stack |
| `.github/workflows/` | GitHub Actions CI |
| `.gitlab-ci.yml` | GitLab CI |
| `Jenkinsfile` | Jenkins |
| `docker-compose.*` | Docker-based environments (authorized use only per owner rule) |
| `systemd/*.service` / `systemd/` | Native systemd service shape (HX deployment norm) |
| `pnpm-workspace.yaml` / `turbo.json` / `nx.json` | Monorepo — handle per the Monorepo note |
| `AGENTS.md` | Multi-agent workflow conventions (HX factory repo) |

## Workflow: Creating the Context File

1. **Check for existing context.** Look for
   `governace/qa/<project-name>/qa-project-context.md`.
2. **If absent:** create the `governace/qa/<project-name>/` folder if needed, scaffold
   the section structure, run the Discovery Questions starting with Product, and write
   the file once filled.
3. **If present with placeholders:** read it, list which sections are complete vs.
   unfilled, ask only about the unfilled sections, then update — preserve completed
   sections untouched, and record any changed value as a dated, clearly labeled
   correction/change entry appended to the existing record rather than overwriting the
   original.
4. **If present and complete:** summarize the current context, ask what changed (new
   tools, team changes, shifted goals), and update only the deltas — each delta is a
   dated, clearly labeled correction/change entry appended to the existing record; the
   original context stays intact.
5. **After completion:** confirm the file path, run Verification (below), and suggest
   the next skill from the context (no E2E → E2E setup; no strategy → `test-strategy`;
   no unit tests → unit testing).

## Section Guidance

What makes a good entry in each section.

**Product.** Key user flows must be specific and testable: "Buyer searches products,
adds to cart, checks out with Stripe, receives confirmation email" — not "user uses the
app." This list is what every test skill uses to prioritize. Aim for 5–10.

**Tech Stack.** Record frontend, backend, database, hosting separately. Pin versions
only when they change the testing approach. Don't copy a version just because an example
shows one — read it from the actual config.

**Test Stack.** For each tool: framework name + version, config location, test
directory. No infrastructure yet is valid — write "None selected yet" and the
recommended default (Principle 3).

**Monorepo.** List each frontend app as its own Tech Stack and Test Stack entry; keep
the shared API/backend as one entry. Shard E2E **per app** and note in CI/CD which path
filters gate which app's suite.

**CI/CD.** Answer what other skills need: what blocks a deploy, how fast feedback is,
what evidence is preserved.

**Environments.** Note how staging diverges from production — a different DB engine in
staging means staging-green tests can still fail in prod. Record the deployment shape
(systemd native norm).

**Quality Goals.** Concrete and measurable only. Pick starting targets by maturity:

| Maturity | Unit coverage | E2E | Flakiness | Suite duration |
|----------|--------------|-----|-----------|----------------|
| Early-stage startup | 60% on business logic | Top 5 critical flows | <2% | Unit <3 min, E2E <15 min |
| Growth-stage | 80% | All critical paths | <2% | Unit <3 min, E2E <15 min |
| Enterprise | 90%+ | Comprehensive + perf budgets | <1% | Unit <3 min, E2E <15 min |

Write them as numbers: "80% line coverage measured by coverage.py," "flake rate <2%
over a rolling 30-day window," "full E2E under 15 min with 4 shards." Never "we want
great quality."

**Risk Areas.** Use the table — columns Area, Impact, Likelihood, Score, Notes — with
every entry carrying explicit **Impact** and **Likelihood** ratings (each on a numeric
1–5 scale) and a numeric **Score** calculated as **Score = Impact × Likelihood**. The
**Score is reporting data, not the classifier** — the tier comes from the impact ×
likelihood **combination**, so test-strategy can reproduce the ranking deterministically:

- **Critical (test first):** High impact (4–5) AND high likelihood (4–5) — e.g.
  Impact 5 × Likelihood 5 = 25; payment flow with known edge cases.
- **Important:** High impact (4–5) AND low likelihood (1–3) — e.g. Impact 5 ×
  Likelihood 2 = 10; auth — catastrophic if broken, rarely changes. Never Critical.
- **Monitor:** Low impact (1–3) AND high likelihood (4–5) — e.g. Impact 2 ×
  Likelihood 5 = 10; notification formatting — breaks often, low severity. Never
  Important.
- **Backlog:** Low impact (1–3) AND low likelihood (1–3) — e.g. Impact 2 ×
  Likelihood 2 = 4; admin settings — stable, rarely used.

**Complete combination-to-tier mapping (authoritative, shared with `test-strategy`):**
classify by the Impact band (High = 4–5, Low = 1–3) and the Likelihood band
(High = 4–5, Low = 1–3), never by the raw Score alone:

| Likelihood \ Impact | Impact High (4–5) | Impact Low (1–3) |
| --- | --- | --- |
| Likelihood High (4–5) | **Critical** | **Monitor** |
| Likelihood Low (1–3) | **Important** | **Backlog** |

This mapping is deterministic and identical across QA skills: any feature with the same
Impact and Likelihood ratings lands in the same tier everywhere.

At least 3 entries, each with Impact, Likelihood, and Score populated, never vague
("everything breaks").

**Team.** Record the factory lanes engaged and the dev:QA shape — it sets the
automation ownership model:

| Dev:QA shape | Ownership model |
|--------------|-----------------|
| Solo / zero dedicated QA | Devs own all tests; QA lane (Bailey/Gordon) = strategy + critical-path E2E + qualification |
| High dev:QA | Developers write tests; Bailey owns strategy + authoring plans; Gordon owns critical-path qualification |
| Balanced | Bailey authors E2E, devs own unit, integration shared; Gordon qualifies |
| QA-heavy | Dedicated automation (Bailey) + qualification (Gordon) lanes; comprehensive regression suites |

**Conventions.** Selector strategy especially — the authoring and reliability skills
read it to generate matching selectors. Default to `data-testid` for stability
(`data-testid="invoice-create-button"`, kebab-case). If the team prefers semantic/ARIA
selectors, record concrete tokens and the tradeoff.

## Anti-Patterns

### 1. Asking all questions at once
Dumping 30 questions is overwhelming and gets shallow answers. Walk section by section,
Product first.

### 2. Leaving `[brackets]` in the final file
If the user has no answer, record the actual state ("None — no E2E framework selected
yet"), not a placeholder. Placeholders left in the file silently break every downstream
skill that parses it.

**Placeholder token.** A placeholder is a bracketed, lowercase, descriptive **multi-word
phrase** (contains a space) with no dots and no uppercase, e.g. `[user flow]`,
`[component name]`, `[tool version]`. Valid configuration section headers such as
`[tool.pytest]` or the single-word `[pytest]` are NOT placeholders — they are legitimate
content and must pass the completeness check.

### 3. Inventing information
Detect the stack from config files — then confirm before writing. Don't guess a
database or hosting provider.

### 4. Skipping Risk Areas
The single most valuable section for downstream skills. Push for at least 3–4 scored
entries even when the user insists everything is fine.

### 5. Recommending tools beyond the zero-infra default
This skill records current state; tool selection belongs to the specialized skills. The
*only* recommendation Bailey makes here is the pytest/Playwright default when there is
no test infrastructure at all (Principle 3).

### 6. Crossing the boundary
Bailey writes the context file; she does not stand up environments or execute tests
from it. Context records state; Gordon's environment skill acts on it.

## Verification

Prove the produced file is complete, smallest check first. From the repo root. The
completeness check looks for the defined placeholder token — a bracketed, lowercase,
dot-free descriptive phrase (multi-word, containing a space) — NOT any square-bracket
text, so valid config identifiers such as `[tool.pytest]` and `[pytest]` pass:

```bash
# Bind QA_DIR from the first argument, or default to the environment variable.
QA_DIR="${1:-$QA_DIR}"
[ -n "$QA_DIR" ] || { echo "usage: verify-qa-context.sh <project-name> (or set \$QA_DIR)"; exit 2; }
F="governace/qa/$QA_DIR/qa-project-context.md"
[ -r "$F" ] || { echo "error: context file missing or unreadable: $F"; exit 1; }

# The completeness check scans ONLY the ACTIVE record — the file content before
# the first labeled historical/correction block. Append-only history (labeled
# [HISTORICAL]/[OPEN CORRECTION]/[LABELED CORRECTION] blocks appended below) may
# legitimately retain bracketed placeholders from prior states and must not fail
# the active-record check.
ACTIVE_RECORD="$(sed '/^> \*\*\[\(HISTORICAL\|OPEN CORRECTION\|LABELED\)/,$d' "$F")"

# Placeholder tokens are multi-word phrases — the regex requires at least one
# space inside the brackets (e.g. `[user flow]`), so single-word configuration
# identifiers such as `[pytest]` are never flagged. grep -oE extracts each
# candidate and the final grep reports whether any genuine placeholder remains:
# 0 = placeholders found (incomplete), 1 = none (complete). Capture the last
# exit status so a read/scan error can never be misreported as "context complete".
printf '%s\n' "$ACTIVE_RECORD" \
  | grep -oE '\[[a-z][a-z -]* [a-z -]*\]' \
  | grep -q .
gs=$?
case "$gs" in
  0) echo "context incomplete: placeholders present in the active record"; exit 1 ;;
  1) echo "context complete: active record has no placeholders" ;;
  *) echo "error: could not scan the context file (exit $gs)"; exit 1 ;;
esac
```

**Regression case — `[pytest]` must pass.** Create a context file whose active record
contains the valid `[pytest]` header and no genuine placeholder; the check must report
`context complete` (exit 0):

```bash
F="governace/qa/$QA_DIR/qa-project-context.md"
printf '## Test Stack\n- pytest is configured via `[pytest]` in pyproject.toml\n' > "$F"
printf '%s\n' "$(sed '/^> \*\*\[\(HISTORICAL\|OPEN CORRECTION\|LABELED\)/,$d' "$F")" \
  | grep -oE '\[[a-z][a-z -]* [a-z -]*\]' \
  | grep -q .
gs=$?
case "$gs" in
  0) echo "REGRESSION FAIL: [pytest] flagged as placeholder"; exit 1 ;;
  1) echo "REGRESSION PASS: [pytest] is valid content" ;;
  *) echo "REGRESSION ERROR: placeholder scan failed (exit $gs)"; exit 1 ;;
esac
```

Exit 0 with the message means the file exists, is readable, and the ACTIVE record
has no `[bracketed placeholder]` (per the placeholder token above). Placeholders in
labeled historical/correction blocks are append-only history and are not checked.
Bracketed config identifiers like `[tool.pytest]` and `[pytest]` are acceptable content
and do not fail the check. Then eyeball that all nine section headers are present in the
active record:

```bash
sed '/^> \*\*\[\(HISTORICAL\|OPEN CORRECTION\|LABELED\)/,$d' "$F" | grep -c '^## '   # expect >= 9
```

## Done When

- `governace/qa/<project-name>/qa-project-context.md` exists, is readable, and the
  placeholder-token grep over the **active record** returns status 1 (no bracketed
  placeholders remain); placeholders in labeled historical/correction blocks are
  append-only history and do not fail the check; valid config identifiers like
  `[tool.pytest]` and `[pytest]` do not fail it either (regression-covered).
- All nine sections are present: Product, Tech Stack, Test Stack, CI/CD, Environments,
  Quality Goals, Risk Areas, Team, Conventions.
- Product lists at least 5 specific, testable key user flows (no "user uses the app").
- Test Stack names the actual frameworks + versions + paths in use, or states "None
  selected yet" with the recommended default noted.
- Risk Areas table has at least 3 entries, each with explicit Impact, Likelihood, and
  numeric Score (Score = Impact × Likelihood) populated — the three dimensions are
  present and the Score matches the product so test-strategy can reproduce the ranking.
- Quality Goals are concrete numbers (coverage %, flake %, durations) — not
  aspirational prose.
- Team section shows the factory lanes engaged (Bailey author, Gordon qualification,
  Erwin config, Mia coordination, James acceptance).
- The file is handed off through the locked test loop; Bailey does not execute or accept.

## Related Skills (factory lanes)

- **ai-test-generation** / **test-planning** / **test-strategy** (Bailey) — the
  authoring skills that consume this context file.
- **test-environments** / **test-reliability** / **ci-cd-integration** (Gordon) — the
  execution and qualification skills that act on the CI/CD, Environments, and
  Conventions sections.
- **release-readiness** (Gordon) — the qualification evidence path gated by this
  context's Quality Goals and Risk Areas.
- When a project's QA exists end-to-end already, use this skill directly to (re)fill
  context rather than bootstrapping from scratch.
