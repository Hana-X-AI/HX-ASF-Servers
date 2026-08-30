# HX-ASF-Servers

Infrastructure repository for the HX AI Software Factory: 16 active servers
plus development workstations, operated by Hana-X. Work here is mostly
infrastructure deployment with pilot programs to validate, executed by AI
agents under human checkpoints. (hxs-7 decommissioned 2026-08-27; hxs-20
and hxs-21 added 2026-08-28.)

## How this repository works

- Every assignment begins as a goal in `governace/goals/`. See `governace/goals/README.md`.
- Agents work in lanes under `agents/<agent-name>/`. See `agents/README.md`.
- Decisions are recorded as Key Decision Documents (KDDs) in `governace/decisions/`.
- Issues, action items, and lessons live in `knowledge/`.
- Operations scripts live in `scripts/` and follow the approved Bash/SSH
  fleet-control pattern. Ansible is not part of this architecture.
- Agent alignment (skills, trigger words, communication contract) is in `AGENTS.md`.

## Truth-state labels

Every factual claim about infrastructure state carries one of these labels:

- `TARGET-STATE` — approved design, not yet built
- `AS-BUILT` — implemented and verified in this repository
- `DISCOVERED` — observed on a running system, with evidence and date
- `PROPOSED` — under discussion, not approved
- `LEGACY` — historical, kept for rationale only

A design document is not evidence that something is installed. Runtime claims require
current evidence with a date.

## Layout

Operational now: `governace/goals/`, `knowledge/`, `agents/`, `scripts/`, `servers/`,
`pilots/`.
Future placeholders: `tests/`.
[2026-08-30: the `.kimi-code/agents/` placeholder was removed — executable
sub-agent definitions will be re-added here when the phase-transition KDD lands
(see `agents/README.md`).]
