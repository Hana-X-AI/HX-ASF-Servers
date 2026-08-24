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

- One file per goal: `goals/<YYYY-MM-DD>-<short-slug>.md`
- Status values: `draft`, `approved`, `in-progress`, `blocked`, `done`, `abandoned`
- Link decisions to `knowledge/decisions/KDD-NNNN-*` files.
- Link affected servers to `servers/<hostname>/` once that tree exists.
