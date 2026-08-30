---
name: goal-decompose
description: "Spec-driven goal decomposition for the HX factory (adapted from automazeio/ccpm, MIT). Turns an authorized goal contract into a bounded execution graph of work orders with dependency + parallelization metadata. Use after the scope-lock is confirmed: 'decompose goal X', 'break the goal into work orders', 'what work orders does this goal need'. NOT for: scope-lock (governor's grill-me flow), execution, or acceptance."
---

# Goal Decompose — spec-driven goal decomposition (James)

Adapted from `automazeio/ccpm` (MIT) into the HX factory's governance model.
Requirements live in the goal file, not in heads. A goal contract becomes
atomic work orders with full traceability.

## Core flow

1. **Read the goal contract** — the confirmed scope-lock + goal file
   (`governace/goals/<id>.md` after the S1 move; `goals/<id>.md` currently).
   The six scope-lock fields are already locked (objective, target, boundaries,
   exclusions, acceptance, assigned family/lane).
2. **Identify work types** — setup, config, install, data, integration, tests,
   docs, evidence. Map to the actual lane families from the locked lane table.
3. **Decompose into atomic work orders** — each work order is one bounded
   contribution (per `governace/templates/pilot/work-order.yaml`): exact success
   criteria, authoritative inputs, permitted target/tools, prohibitions,
   deliverable schema + destination, evidence obligations, budgets, rollback,
   escalation path.
4. **Encode dependency + parallelization metadata** — which work orders block
   others, which can run in parallel. Small (≤5) → sequential; medium (5–10) →
   batch 2–3 groups; large (>10) → analyze dependencies first, max 5 parallel.
5. **Validate the decomposition** — every work order is atomic, independently
   decidable, has bounded typed output, obtainable evidence, contained failure.
   No node starts until its predecessors pass; no circular deps; no recursive
   spawning without authorization; agents never silently expand scope.

## Work-order contract (mandatory fields)

Every work order inherits from the goal: relevant goal version, exact success
criteria advanced, authoritative inputs, permitted target and tools, prohibited
actions, expected deliverable schema, evidence obligations, budget and stop
conditions, rollback/containment requirement, escalation path to the governor.

The worker decides HOW within those boundaries. It may not redefine the goal,
broaden scope, waive tests, or declare factory completion.

## Deterministic tooling

Scripts in `scripts/` read the goal/work-order tree for status, dependency, and
readiness. Run them directly (script-first rule), do not reconstruct by hand:

- `scripts/status.sh` — goal/work-order counts by status
- `scripts/next.sh` — ready work orders (open, deps satisfied)
- `scripts/blocked.sh` — work orders blocked by open deps
- `scripts/validate.sh` — goal-tree integrity (frontmatter, deps, orphans)

Run from the repo root: `bash .kimi-code/skills/goal-decompose/scripts/<script>.sh`

## Boundaries

- The governor decomposes; workers execute under work orders; Mia manages.
- Never dispatch without a confirmed scope-lock record.
- Never redefine the goal or expand scope during decomposition.
- Every change to a ratified governance record is a labeled append-only
  correction, never a silent rewrite.
