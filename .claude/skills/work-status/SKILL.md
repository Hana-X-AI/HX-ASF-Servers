---
name: work-status
description: "Work status, standup, and validation reporting for the HX factory (adapted from automazeio/ccpm, MIT). Deterministic scripts report goal/work-order status across the factory: 'what's our status', 'standup', 'what's blocked', 'what's in progress', 'what's next'. For Mia's status reporting to the governor. NOT for: goal decomposition (goal-decompose), execution, or acceptance."
---

# Work Status — status, standup, and validation reporting (Mia)

Adapted from `automazeio/ccpm` (MIT) into the HX factory. Reports on the goal
and work-order tree so Mia can give the governor deterministic status without
reconstructing anything by hand.

## Script-first rule

All reporting is deterministic — run the script, present its output. Do not
reconstruct status manually. Scripts read the goal/work-order tree
(`governace/goals/`).

Run from the repo root:

```bash
bash .agents/skills/work-status/scripts/<script>.sh [args]
```

## Scripts

| What the user / governor wants | Script |
|---|---|
| Overall status (goals by state, open work) | `scripts/status.sh` |
| Daily standup report | `scripts/standup.sh` |
| What's blocked (open work with open deps) | `scripts/blocked.sh` |
| What's in progress | `scripts/in-progress.sh` |
| What's ready next | `scripts/next.sh` |
| Validate the goal tree (frontmatter, deps, orphans) | `scripts/validate.sh` |

## Reporting contract

- **Status** goes to the governor (James) — Mia reports, never gates/accepts
  (KDD-0012: management only).
- **Blocked / next / in-progress** feed Mia's breakage triage and distribution
  to the engineering lanes.
- **Validate** is a mechanical integrity check (goal frontmatter, dependency
  references, orphan files); findings route to the governor for disposition.

## Boundaries

- Read-only reporting: these scripts never mutate goal files.
- Mia never mutates an engineering lane or issues repair dispositions.
- If a goal file lacks required frontmatter, flag it — do not invent state.
