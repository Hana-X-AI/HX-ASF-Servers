# Goals

Every assignment in this repository begins as a goal file. The goal file is the work
order: scope, completion contract, and evidence requirements in one place.

## Workflow

1. Owner states intent (usually via `/goal` in a Kimi Code session).
2. The assigned agent writes or refines the goal file from `goals/_template.md`
   (the `/write-goal` pattern: a rough intention becomes a completion contract).
3. Owner approves the goal file before work begins.
4. Work proceeds; the goal file tracks status.
5. Completion requires the stated evidence, not a verbal claim.

## Conventions

- One file per goal: `goals/<YYYY-MM-DD>-<short-slug>.md`; the file name is the
  Goal ID (KDD-0002).
- Status values: `draft`, `approved`, `in-progress`, `blocked`, `done`, `abandoned`
- `goals/` is the designated durable work-state system; GitHub Projects is deferred
  (KDD-0002).
- The full goal contract model (Goal Contract, work orders, fresh sessions, gates)
  lives in `agents/kimi-k3/goal-setting-guidance.md`.
- Link decisions to `knowledge/decisions/KDD-NNNN-*` files.
- Link affected servers to `servers/<hostname>/` once that tree exists.
