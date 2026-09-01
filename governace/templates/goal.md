# Goal: <title>

- Goal ID: <YYYY-MM-DD>-<slug> (this file's name)
- Version: 1
- Status: draft | approved | in-progress | blocked | done | complete | abandoned
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

Deferred success-condition exception: a goal MAY be marked COMPLETE while one or more
success conditions remain unpassed ONLY when all of the following are recorded in the
goal's status block as a labeled, dated, append-only `[LABELED COMPLETION EXCEPTION]`
entry:
- **Owner approval** — the deferral is a documented owner decision (date + authority,
  e.g. a state-log row or explicit owner word), never an agent's unilateral call.
- **Rationale** — why the condition is deferred rather than failing (e.g. capability
  gap, owner-scoped future work window, dependency not yet authorized).
- **Scope** — exactly which success condition(s) are deferred and what remains
  in-scope for the current completion claim.
- **Tracked reopen** — the deferred condition is recorded in
  `governace/issue-tracking/issues.md` (or an equivalent owner-visible tracker) and
  reopens as owner work when its gating window arrives.
The `COMPLETE — PASS` status is only consistent under this rule when the exception
entry above is present; without it, a goal with an unpassed success condition must
remain incomplete. This exception clause is the governing authority for the
`[LABELED COMPLETION EXCEPTION]` blocks used by goals such as
`2026-08-24-hx1-ollama-qwen38-27b.md` (SC-05/AC-008/AC-016) and
`2026-08-26-hxs3-muse-glimmer-tooling.md` (SC-06).

<!-- REQUIRED. Machine-readable current state (work-state.schema.yaml).
     Prose above is history and is never rewritten; this block is the single
     source every status tool reads. validate.py SY-4 enforces it. -->

```yaml work-state
id: <goal-filename-without-.md>
status: draft            # draft|approved|in-progress|blocked|done|complete|abandoned
status_date: <YYYY-MM-DD>
authority: >-
  <the owner decision, correction, or evidence establishing this status>
reconcile: none          # or a one-line statement of a conflict with downstream evidence
```
