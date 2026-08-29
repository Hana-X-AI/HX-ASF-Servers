# Change Record — <change-name>

**Status lifecycle (QA-audit ST-6, 2026-08-29):** a change record moves
`PROPOSED → IN PROGRESS → COMPLETE`. **No record may claim COMPLETE unless the
governing goal/plan status AND execution evidence agree** (audit AG-01/DC-02:
a fabricated COMPLETE was corrected to PROPOSED on 2026-08-29 because the goal
was draft and the plan NOT-APPROVED/NOT-EXECUTED). Status flips require a
labeled, dated correction line preserving the prior status verbatim.

| Field | Value |
| --- | --- |
| Date | <YYYY-MM-DD> |
| Host | <host (IP)> |
| Change type | <model replacement | deployment | configuration | ...> |
| Agent lane | <owner lane> |
| Status | **PROPOSED** — NOT EXECUTED (until owner approval + execution evidence) |
| Governing goal | <goals/<file>.md — status: draft/active/complete> |
| Governing plan | <servers/<host>/<plan>.md — status: approved/not-approved> |
| Execution evidence | <artifact path(s): ollama list, digests, state-log row, validate output> |

## What changed

<Describe the proposed change. For the PROPOSED state, this is the TARGET; for
COMPLETE, describe what was actually executed.>

## Why

<Problem being solved, with evidence (e.g., a recorded timeout/504, an owner
directive).>

## Before state

<Table: call-sign, model/version, alias, digest, config, service state.>

## After state

<For COMPLETE: the verified end state with digests/evidence. For PROPOSED: the
intended target state, clearly labeled as target.>

## Verification

<For COMPLETE: the actual evidence (commands, outputs, hashes). For PROPOSED:
what will be run at execution.>

## Conclusion

<Only write "COMPLETE — deployed / decommissioned" when the governing goal/plan
and the execution evidence all support it. Otherwise: "PROPOSED — awaiting owner
approval and execution.">

## Rollback

<Deterministic inverse for each mutation.>

## Open items

<List pending owner decisions, cross-lane handoffs (e.g., OmniRoute routing is
trinity's lane), and verification steps.>

## Sources

<Controlling goal, plan, configuration.md, KDDs, install/evidence docs.>
