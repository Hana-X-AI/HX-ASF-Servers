---
name: ai-test-generation
description: "Staged AI-assisted test authoring for the HX factory's QA lane (Bailey): extract requirements from specs/PRDs/diffs/bugs/OpenAPI, analyze risk, map coverage, design oracles, then generate traceable pytest (zod for TS contract tests) code for human review. Use when: 'generate tests', 'tests from PRD', 'tests from a bug report', 'auto-generate test cases'. NOT for: auditing a pre-existing suite, testing AI/LLM features, or setting up/executing test environments (Gordon's lane). Adapted from petrkindlmann/qa-skills v3.0.0 (MIT)."
maturity: active
---

# AI Test Generation — staged test authoring (Bailey)

Adapted from `petrkindlmann/qa-skills` v3.0.0 (MIT) into the HX factory's QA workflow.
Owner: **Bailey** (Sr. AI Testing Engineer, QA family). This skill is the **authoring**
lane of the locked test loop: Erwin installs → Bailey authors → Gordon sets up env +
executes → results to the testing log → Gordon notifies Bailey + Erwin → Erwin fixes
config → Gordon retests → max 3 iterations → James accepts on
`governace/process/governor-verification-checklist.md`.

**Bailey's hard boundary:** Bailey produces the test plan + test scripts + pinned
stack only. She does NOT set up environments, execute tests, fix configuration, or
accept work. Environment setup + execution + retest is Gordon's lane; acceptance is
James's. Work produced here lands at `governace/qa/<project-name>/`.

<objective>
LLMs will happily emit fifty plausible-looking tests that assert nothing, target
endpoints that do not exist, and duplicate each other. This skill is a staged pipeline
that forces structured intermediates — assumptions, coverage matrix, oracle
definitions — out of the model BEFORE any test code, so what you get is traceable,
reviewable, and grounded in the real codebase instead of ad-hoc generated noise.

**Before starting:** Check for `governace/qa/<project-name>/qa-project-context.md`
(Bailey's `qa-project-context` skill authors it). It carries tech stack, test
frameworks, naming conventions, selector strategy, and known risk areas that
dramatically improve generated test quality.
</objective>

## Quick Route

The pipeline is the same for every input; only the Step 1 extraction emphasis changes.
Jump to the matching row, then run Steps 2-7 unchanged.

| Input type | Step 1 extracts | Watch for |
|------------|-----------------|-----------|
| PRD / feature spec | Entities, business rules, acceptance criteria, NFRs, stated assumptions | Implicit requirements inferred from "seamless"/"fast" language |
| User story + AC | Each AC → ≥1 happy + ≥1 negative scenario | ACs that hide multiple behaviors in one line |
| Code diff (`git diff main...HEAD`) | New/changed code paths, modified conditionals, removed behavior | Regression scope: test the changed paths, not the whole module |
| Bug report | Repro steps, expected vs actual, environment | Write a test asserting *expected* — fails now, passes after fix |
| OpenAPI / GraphQL SDL | Endpoints, schemas, required fields, enums, auth | Validation, auth-failure, and edge cases per endpoint, not just 200s |

## Discovery Questions

Check `governace/qa/<project-name>/qa-project-context.md` first — if it exists, use it
and skip anything already answered there. Then clarify:

1. **What is the input source?** PRD / spec, user story + AC, code diff, bug report, or
   API schema. Determines Step 1 extraction emphasis (see Quick Route). For an LLM/AI
   feature spec, stop — eval datasets belong in the factory's AI/LLM eval practice, not
   Playwright specs.
2. **What is the target test framework?** Factory default is **python/pytest** for
   Python services and **zod** for TypeScript-side contract tests. Playwright is used
   where a browser E2E journey genuinely matters (framework guidance kept generic).
3. **What project context is available?** Existing test patterns, Page Objects /
   helpers, data factories / fixtures, CI constraints (timeout, parallelism). More
   context = less cleanup.
4. **What is the review workflow?** Full pipeline → human review → hand to Gordon for
   execution (default); scenarios only → Bailey writes code; or code → human refines
   iteratively.
5. **What domain knowledge is needed?** Regulated-industry compliance, domain
   invariants (money never negative, appointments cannot overlap), known risk areas
   from past incidents.

## Core Principles

1. **Pipeline before code.** Never generate test code before establishing what to test,
   why, and how to verify it. The seven-step pipeline exists to prevent premature code
   generation that targets the wrong things.
2. **Structured intermediates are the product.** The assumptions document, coverage
   matrix, and oracle definitions are more valuable than the test code itself. They are
   reviewable, traceable, and reusable.
3. **Separate what from how.** Scenario generation (what to test) and oracle design
   (how to verify) are distinct cognitive tasks. Mixing them produces scenarios biased
   toward what is easy to assert, with assertions tacked on as afterthoughts.
4. **AI generates the first draft; a human reviews and refines.** Never ship
   AI-generated tests without human review. The AI accelerates — it does not replace
   judgment.
5. **Context is everything.** Feed the LLM your conventions, existing patterns,
   selector strategy, and data setup. The more context, the less cleanup.
6. **Quality over quantity.** Each test has a maintenance cost. Focus on critical
   paths, complex logic, and known risk areas — not test count.

## The Pipeline

**Mandatory workflow — Bailey MUST follow this order:**

```
Step 1: Extract   → Requirements, entities, business rules from input
Step 2: Analyze   → Risks, invariants, edge cases, ambiguities
Step 3: Map       → Coverage matrix (requirement → scenario → priority)
Step 4: Generate  → Candidate scenarios (happy + boundary + negative + security + a11y)
Step 5: Design    → Assertions and oracles SEPARATELY from scenarios
Step 6: Code      → Test code (only after all above exist)
Step 7: Review    → Human review with traceability back to source
```

### Step 1: Extract Requirements and Entities

Parse the input into structured elements: **Entities** (with roles/states/attributes),
**Business Rules** (numbered), **Explicit Requirements** (`[REQ-N]`, stated in source),
and **Implicit Requirements** (`[IMP-N]`, inferred — flag every one for human
confirmation). Separating explicit from inferred is the rule that prevents testing
assumptions as if they were specifications.

### Step 2: Risk Analysis and Invariants

Derive what can go wrong, what must always be true, and where the source is silent.

- **Risks** — table of `Risk | Likelihood | Impact | Source Requirement` (e.g. race
  condition on stock decrement, email delay > 30s).
- **Invariants** (must ALWAYS hold) — `stock >= 0`, `order total = sum(items) + tax +
  shipping`, `user sees only their own orders`.
- **Ambiguities** (need human answers) — "Does free shipping apply before or after
  discount codes?" Capture these explicitly; do not silently pick one.
- **Edge cases derived from risks** — two users buy the last item, payment succeeds
  but email service is down.

### Step 3: Coverage Matrix

The single most important artifact — it prevents both gaps and duplicates. Map every
requirement to scenarios with category, priority, and oracle type:

| Requirement | Scenario | Category | Priority | Oracle Type |
|-------------|----------|----------|----------|-------------|
| REQ-1 | Add single item to empty cart | Happy path | P0 | State: cart count = 1 |
| REQ-1 | Add out-of-stock item | Negative | P0 | UI: error message, cart unchanged |
| REQ-2 | Complete checkout with valid card | Happy path | P0 | State: order created, stock decremented |
| REQ-2 | Two users checkout last item | Race condition | P1 | One succeeds, one gets stock error |
| INV-1 | Stock never goes negative | Invariant | P0 | Data: stock >= 0 after any operation |

After building it, verify: every requirement has ≥1 happy and ≥1 negative scenario;
every invariant has a direct test; every Step-2 risk has a scenario; no two rows test
the same thing.

### Step 4: Generate Candidate Scenarios

For each matrix row, write the full scenario in Given/When/Then with explicit test-data
requirements (`Given: user with 99 items in cart (max 100); When: adds one more; Then:
count = 100`). Cover these categories systematically:

| Category | Description |
|----------|-------------|
| Happy path | The user does exactly what the feature is designed for |
| Boundary | Edge of valid input ranges |
| Negative | Invalid inputs, unauthorized actions |
| Security | Auth bypass, injection, privilege escalation |
| Accessibility | Screen reader, keyboard-only, contrast |
| State transition | Valid and invalid moves between states |
| Concurrency | Two users acting simultaneously |

### Step 5: Design Assertions and Oracles

**Deliberately separate from Step 4.** Scenarios describe behavior; oracles describe
how to verify it. For each scenario, define oracles across categories — a single
assertion is rarely enough to prove a behavior:

| Oracle category | Asserts | Example |
|-----------------|---------|---------|
| UI state | Visible text / element state | `cart badge toHaveText('1')` |
| Data | Persisted state via API/DB | `GET /api/cart` returns 1 item, correct total |
| Negative | What should NOT happen | no error toast; no navigation away |
| Side effect | Async/external outcomes | analytics `add_to_cart` fired; email in inbox < 30s |

**Oracle quality rules:** assert business outcomes not implementation details; use the
most specific assertion available (`toHaveText('$29.99')`, not `toBeTruthy()`); include
negative assertions; verify data integrity, not just UI; assert accessibility (focus
management, live-region announcements).

### Step 6: Generate Test Code

**Only after Steps 1-5 produce reviewed artifacts.** Code is a mechanical translation
of scenarios + oracles into framework syntax, with traceability comments linking back
to the requirement and scenario. Factory default is python/pytest; zod for TS-side
contract tests:

```python
# Scenario: SC-001 — Add single item to empty cart
# Requirement: REQ-1 (User can add items to cart)
# Priority: P0
def test_add_single_item_to_empty_cart(client, test_product):
    # Given — cart is empty, product exists (fixture)
    # When
    resp = client.post(f"/products/{test_product.id}/cart")
    # Then — state oracle
    cart = client.get("/api/cart").json()
    assert cart["count"] == 1
    # Negative oracle — no error surfaced
    assert resp.status_code == 200
```

**Code generation rules:** match project conventions (from the QA project context);
reuse existing fixtures and data factories; include traceability comments (`Scenario:
SC-XXX`, `Requirement: REQ-XX`); follow the project's selector strategy; put
setup/teardown in fixtures, not inline.

### Step 7: Human Review

Not optional — a mandatory pipeline step. This reviews **the tests this pipeline just
generated**, before they are handed to Gordon for execution. Run every generated test
against this checklist:

- [ ] **Traces to requirement:** test → scenario → coverage row → requirement is followable.
- [ ] **Tests behavior, not implementation:** survives a harmless refactor.
- [ ] **Correct abstraction level:** right test type (unit vs integration vs E2E).
- [ ] **Test naming and readability:** the test name states the behavior; a reader sees intent without decoding the body.
- [ ] **Test isolation / no shared state:** the test creates and cleans up its own data, holds no order dependency on sibling tests, and passes when run alone or in any order.
- [ ] **Realistic test data:** plausible, diverse, using `example.com`.
- [ ] **Meaningful assertions:** matches the oracle definition; specific, not `toBeTruthy()`.
- [ ] **Matches project conventions:** naming, structure, selector strategy.
- [ ] **No flakiness risks:** no hardcoded timeouts, race conditions, or order dependence.
- [ ] **Edge cases included:** goes beyond the happy path.
- [ ] **Assumptions validated:** Step-2 ambiguities were resolved before coding.

**Review outcome per test:** **KEEP** (hand to Gordon) · **MODIFY** (fix listed
issues) · **REJECT** (wrong requirement, wrong abstraction, hallucinated API) · **DEFER**
(blocked on ambiguity). KEEP/MODIFY results pass into the locked test loop as the
Bailey-authored deliverable.

## Guardrails

Hard rules. Bailey MUST follow them.

- **Code before coverage is forbidden.** Never emit test code before Steps 1-5
  (requirements, risk analysis with documented assumptions, coverage matrix,
  scenarios, and oracles) are complete AND reviewed. If an agent attempts to
  generate code before those steps exist and are reviewed: STOP, go back to the
  earliest missing or unreviewed step.
- **Assert outcomes, not implementation.** `expect(screen.getByRole('progressbar'))
  .toBeVisible()`, not `expect(component.state.isLoading).toBe(true)`. In pytest:
  assert the observable response/state, not internal call ordering.
- **Scenarios (Step 4) before oracles (Step 5), always.** Scenario = WHAT happens;
  oracle = HOW to verify. Mixing them biases scenarios toward easy assertions.
- **Always produce the intermediates** — assumptions document, uncovered ambiguities,
  oracle candidates, and the traceability chain — even in abbreviated form.

**Flag these when detected:**
- **Hallucinated APIs** — endpoints, selectors, methods, or imports that do not exist
  in the codebase. Verify mechanically (see Verification) before human review.
- **Duplicate scenarios** — same behavior, trivially different data. Consolidate or
  parametrize.
- **Low-value assertions** — `assert response.ok`, `expect(page).toHaveURL(/.*/)`.
- **Missing negative cases** — if every scenario is a happy path, the coverage matrix
  is incomplete.
- **Unrealistic test data** — `test@test.com`, `John Doe`, `password123`. Use diverse,
  plausible data on `example.com`.

## Model selection per task (QA lane default)

Bailey's QA job-family lane default (KDD-0013 Amendment 11, owner decision
2026-08-30) is **Qwen3.8 Flash** (`openrouter/qwen/qwen3.8-flash`, provider
Alibaba Cloud International, via OmniRoute hxs-8) — the same family default as
Gordon (Gordon override recorded 2026-08-29). Route the whole test-authoring
work class (Steps 1-6) on this lane by default; do not route to the legacy
per-agent Coder-X/Qwen-X/Chat-X local lanes for QA work — those assignments are
superseded for the QA family and preserved only as history.

- **Default:** Qwen3.8 Flash (QA family default) for all Steps 1-6. One lane for
  the authoring task keeps the produced suite internally consistent.
- **Approved override rules:** per-agent overrides within a family remain
  supported and are recorded as such (e.g. Gordon's QA override on his own
  campaign lane). Bailey runs on the family default unless the governor records
  a per-task override; no automatic substitution and no unrecorded lane changes.
- **Backend failure:** the session STOPS the affected branch and escalates to
  the meta-agent (governor) — no automatic substitution, no silent cloud
  fallback beyond the authorized OD-14 lane.

Provenance per task (local-model-first rule, AGENTS.md): record the served
model, provider, route, call-sign, endpoint, alias, identity, and role for every
task on this lane — including the related per-task recording guidance in
AGENTS.md's local-model-first section.

## Verification

Convert the "hallucinated APIs" warning into a mechanical gate. After Step 6, before
human review, Bailey runs the author-side checks only — she does NOT execute the test
suite (suite execution is a Gordon-owned gate, per the KDD-0019 test loop):

1. **Resolve imports / types.** Python: `python -m pyflakes <files>` or `ruff check`.
   TypeScript: use the repository's pinned compiler from the installed dependency —
   `npm ci` first, then `./node_modules/.bin/tsc --noEmit` (or
   `npm exec --offline -- tsc --noEmit`) — never a network-enabled `npx tsc`.
   Fabricated imports and wrong signatures fail here.
2. **Grep generated selectors/endpoints against the codebase.** Confirm every
   `getByTestId('...')` id and every API path the test calls actually exists in source.
   Read the configured generated-artifact root and source root from the documented
   governance QA project context file (`governace/qa/<project-name>/qa-project-context.md`)
   — not a `qa-project-context.json` in the current directory — or derive them from the
   repository layout when the context file is unavailable; never hardcode `generated/`
   and `src/`:
   ```bash
   set -o pipefail
   # Derive the project name from the first argument or $PROJECT_NAME; build the
   # context path and quote it so shell metacharacters are not interpreted.
   PROJECT_NAME="${1:-$PROJECT_NAME}"
   [ -n "$PROJECT_NAME" ] || { echo "usage: verify-selectors.sh <project-name> (or set \$PROJECT_NAME)"; exit 2; }
   CTX="governace/qa/$PROJECT_NAME/qa-project-context.md"
   GEN_ROOT="$(grep -iE 'generated_artifact_root|generated.*root|artifact.*root' "$CTX" 2>/dev/null | head -1 | sed -E 's/.*[|:] *([^ ]+).*/\1/')"
   SRC_ROOT="$(grep -iE 'source_root|src.*root|root.*src' "$CTX" 2>/dev/null | head -1 | sed -E 's/.*[|:] *([^ ]+).*/\1/')"
   # Documented repository-layout fallback when the context file is unavailable:
   # resolve the roots from the repo before the directory checks so empty values
   # can never reach them.
   if [ -z "$GEN_ROOT" ] || [ -z "$SRC_ROOT" ]; then
     echo "context roots unresolved in $CTX — deriving from repo layout"
     GEN_ROOT="${GEN_ROOT:-$(find . -maxdepth 3 -type d \( -name generated -o -name dist -o -name build \) 2>/dev/null | head -1)}"
     SRC_ROOT="${SRC_ROOT:-$(find . -maxdepth 3 -type d -name src 2>/dev/null | head -1)}"
   fi
   [ -n "$GEN_ROOT" ] && [ -n "$SRC_ROOT" ] || { echo "FATAL: cannot resolve generated/source roots from context or repo layout"; exit 1; }
   [ -d "$GEN_ROOT" ] || { echo "FATAL: generated root missing: $GEN_ROOT"; exit 1; }
   [ -d "$SRC_ROOT" ] || { echo "FATAL: source root missing: $SRC_ROOT"; exit 1; }
   # grep exit status: 0 = selectors found, 1 = no selectors (valid empty set),
   # 2+ = scan error — treat only 2+ as a failure and let it propagate.
   # Extract every supported literal form — single-quoted, double-quoted, and
   # template-literal arguments. Inside this double-quoted pattern the
   # backslashes keep the quote/backtick characters literal for bash.
   grep -roE "getByTestId\((['\"\`])[^'\`\"]*\1\)" "$GEN_ROOT" > /tmp/selectors-raw.txt
   gs=$?
   if [ "$gs" -gt 1 ]; then echo "FATAL: selector scan error (grep exit $gs)"; exit 1; fi
   if [ "$gs" -eq 1 ]; then echo "no getByTestId selectors found (valid empty set)"; fi
   # Pull the argument out of each matched form (strip the quote characters).
   sed -E "s/.*getByTestId\((['\"\`])([^'\`\"]*)\1\).*/\2/" /tmp/selectors-raw.txt \
     | sort -u > /tmp/selectors-ids.txt
   # Verify each ID exists in source with literal fixed-string matching: a
   # leading dash in an ID is data, not an option (--), and -F disables regex
   # interpretation so dots/brackets in IDs are matched literally. Any missing
   # ID fails the gate with exit 1.
   missing=0
   while read -r id; do
     [ -z "$id" ] && continue
     grep -rFq -- "$id" "$SRC_ROOT" || { echo "MISSING testid: $id"; missing=1; }
   done < /tmp/selectors-ids.txt
   [ "$missing" -eq 0 ] || { echo "FATAL: one or more generated selectors are missing from source"; exit 1; }
   ```
   Both resolved directories must exist before scanning (fail, don't silently fall back);
   grep exit status 1 (no selectors) is a valid empty set while actual scan errors (2+)
   propagate; the roots used are reported so the verification is reproducible.

Any `MISSING` line or lint error is a hallucination to fix before a human spends review
time. After human review, the suite run is a **Gordon-owned gate**: Gordon sets up the
environment and executes (results to `governace/testing/test-log.md`); tests that
reference nonexistent routes/selectors fail fast there and are quarantined. Bailey does
not execute the suite.

## Anti-Patterns

1. **Skipping to code.** The most common failure: an agent gets a PRD and immediately
   writes tests. Without the coverage matrix it misses scenarios and duplicates others.
2. **Asserting implementation instead of behavior.** Assert what the user observes, not
   internal state.
3. **Mixing scenarios and assertions.** Separate *what to test* from *how to verify it*.
4. **No project context in the prompt.** Without conventions and existing patterns, you
   get generic tests. The QA project context file exists for exactly this.
5. **Over-generating.** AI will write 50 tests for a simple function. Each carries
   maintenance cost. Use the coverage matrix to bound generation.
6. **Copy-paste without understanding.** If you cannot explain what a generated test
   does and why, do not ship it.
7. **Shipping without review.** Step 7 is not optional. AI tests routinely contain
   hallucinated APIs, wrong selectors, incorrect business logic, and flakiness only
   human review catches.
8. **Crossing the boundary.** Bailey authors; she does not execute, set up environments,
   or accept. Hand the deliverable to Gordon through the locked test loop.

## Done When

- All seven artifacts exist: requirements document, risk & invariants, coverage matrix,
  scenario set, oracle definitions, test code, and review notes with a
  KEEP/MODIFY/REJECT/DEFER decision per test.
- The coverage matrix was produced and reviewed before any test code file was written.
- Verification passed: lint exits 0 and the selector/endpoint grep reports zero `MISSING`
  lines.
- Each generated test has a recorded human review decision; no test is marked KEEP
  without one.
- The suite is handed to Gordon for environment setup + execution via the locked test
  loop (deliverables in `governace/qa/<project-name>/`), with no KEEP/MODIFY test left
  executing or accepting in Bailey's lane.
- Reproducibility metadata recorded: the exact local model ID + call-sign, input source
  hash, and the version of any skill / CLI / MCP server invoked.

## Related Skills (factory lanes)

- **qa-project-context** (Bailey) — authors the context file this skill reads first.
- **test-planning** / **test-strategy** (Bailey) — decide *what* to test and at which
  level before generating.
- **test-environments** / **ci-cd-integration** / **test-reliability** (Gordon) — env
  setup, pipeline wiring, and flake triage that consume Bailey's generated tests.
- **release-readiness** (Gordon) — the qualification evidence path when generated tests
  gate a release.
- When generated tests find real bugs, feed them to the factory triage/issue flow —
  classification is not acceptance.
