# Goal: <title>

- Goal ID: <YYYY-MM-DD>-<slug> (this file's name)
- Version: 1
- Status: draft | approved | in-progress | blocked | done | abandoned
- Owner: Agent-Zero
- Created: <YYYY-MM-DD>
- Human authority: Agent-Zero
- Agent lane(s): <who is responsible>

## Intent

<One paragraph: the outcome wanted and why. State an end state, not an activity.>

## Scope and target

- Target identity: <repository, host, service, or artifact>
- Baseline: <verified starting state, or how it will be established>
- In scope: <...>
- Out of scope: <...>
- Constraints: <architecture, policy, compatibility, security, operational limits>

## Success conditions and evidence

| ID | Property | Measurement / procedure | Expected result | Evidence | Verifier |
| --- | --- | --- | --- | --- | --- |
| SC-01 | | | | | |

## Execution controls

- Pre-flight (intake existence check): <registry role consistency + one cheap probe result, or "not required — this goal creates the component">
- Active charters reviewed (Phase M): <list checked; qualified agent available: YES | NO>
- Maximum iterations / retries:
- Time / token limits:
- Stop conditions:
- Rollback / containment:
- HITL checkpoints: <decisions reserved for Agent-Zero>

## Notes and links

- KDDs:
- Related goals:

## Amendments and history

Append-only governance record for this goal file. Every change to a prior status,
owner decision, scope, or acceptance condition is recorded here as a new labeled,
dated entry — never silently rewritten. Preserve original values and document the
correction openly (per the repository's documentation-governance contract).
Format per entry:

- **[LABELED CORRECTION <YYYY-MM-DD>, append-only — <short title>]:** <what
  changed, the prior value preserved, authority>.

Keep corrections open and clearly identified until superseded by a later entry.

Completion rule: this goal is done only when (1) every success condition passes with
its required evidence and the verifier accepts the correct artifact — not when the
work feels done — and (2) every supplied or produced document has a **recorded
catalog disposition** in `knowledge/catalog/` (DOC record + index entry + receipt),
so no produced artifact is left uncataloged. Catalog verification and its receipt or
disposition are mandatory before the goal is considered complete. The full contract
model lives in `agents/kimi-k3/goal-setting-guidance.md` (KDD-0002).
