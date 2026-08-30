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
reconstruct status manually.

**One engine (KDD-0021, O1).** Every script here is a thin wrapper that `exec`s
`scripts/work_state.py`. That file is the single implementation and the ONLY
source any tool may use for goal status. Never reimplement the parsing, and
never grep goal prose for a status line: goals are append-only, so the current
answer moves into a labeled correction block while the stale original stays put.
State is read from the one ` ```yaml work-state ` block each goal carries,
specified by `governace/goals/work-state.schema.yaml`.

Run from the repo root:

```bash
bash .agents/skills/work-status/scripts/<script>.sh [args]
python3 scripts/work_state.py <command> [--json]     # the engine, equivalently
```

## Scripts

| What the user / governor wants | Script | Engine command |
|---|---|---|
| Overall status (counts by state) | `scripts/status.sh` | `status` |
| Daily standup report | `scripts/standup.sh` | `standup` |
| What's blocked, with the reason | `scripts/blocked.sh` | `blocked` |
| What's in progress | `scripts/in-progress.sh` | `in-progress` |
| What's ready to dispatch (approved) | `scripts/next.sh` | `next` |
| Validate every goal against the schema | `scripts/validate.sh` | `--check` |
| Goals whose file and evidence disagree | *(engine only)* | `reconcile` |

Every command takes `--json` for machine output.

## Reconcile — the governor's queue

`reconcile` lists goals whose `reconcile` field is not `none`: the goal file and
its downstream evidence disagree. **This is not a defect list.** Recording an
unresolved conflict is the point — deciding one is a governor determination, and
a mechanical tool must never make it. Report these to James; do not resolve
them, and do not treat a non-`none` value as a validation failure.

## Reporting contract

- **Status** goes to the governor (James) — Mia reports, never gates/accepts
  (KDD-0012: management only).
- **Blocked / next / in-progress** feed Mia's breakage triage and distribution
  to the engineering lanes.
- **Validate** runs the engine's schema check (`work_state.py --check`): one
  well-formed work-state block per goal, required fields present, `status` in
  the schema enum, `id` matching the filename, ISO `status_date`, and every
  `evidence` path resolving. It does not check frontmatter, dependency graphs,
  or orphan files — none of those exist in this engine. `validate.py` runs the
  same check as sub-check **SY-4**. Findings route to the governor.

## Boundaries

- Read-only reporting: these scripts never mutate goal files.
- Mia never mutates an engineering lane or issues repair dispositions.
- If a goal's work-state block is missing or malformed, the engine reports it
  as a `WS-0x` problem on stderr and excludes the goal. Flag that — never infer
  state from prose, and never report a malformed goal as simply having no work
  in progress.
