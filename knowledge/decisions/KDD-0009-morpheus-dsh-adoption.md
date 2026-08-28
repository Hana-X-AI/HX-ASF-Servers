# KDD-0009: Adopt Morpheus as DeepSeek Harness lifecycle steward

- Date: 2026-08-28
- Status: **ratified 2026-08-28** — owner directive (full DSH implementation
  approved; "the agent should be implemented first")
- Decider: Agent-Zero
- Related: plan `agent-zero-docs/projects/Deepseek/2026-08-28-dsh-full-implementation-plan.md`;
  source profile `codex_20260827_2225_morpheus-*.md` (preserved unchanged at
  `agent-zero-docs/projects/harness/`)
- Truth-state: roster and governance claims [AUTHORITY]; dsh product facts
  [CANDIDATE until source-grounded under commission]

## Context

The owner ruled 2026-08-28 that the DeepSeek Harness roadmap is the HX platform
direction (retracting the governor's earlier "superseded" verdict — amendment
recorded in `kk3_20260827_2040_*.md`) and approved the full-implementation plan:
complete capability install on hxs-15, phased baseline → intermediate →
advanced, with independent qualification. The plan requires an accountable
build/operate steward for the Harness domain. The candidate profile
HX-AGENT-MORPHEUS-DSH-001 (982 lines, codex 2026-08-27) supplies that role; its
§14 sandbox-baseline assignment was superseded by the owner's direct-implementation
directive, and the codification duty (source §15) is out of the approved arc
(owner 2026-08-28).

## Decision

**ADOPT 2026-08-28:** Morpheus joins the roster (vertical) as DeepSeek Harness
lifecycle steward — configuration, implementation, and operations on hxs-15
under Kimi-K3 work orders. `agents/morpheus/charter.md` + `profile.md`
(distilled from the preserved source) are the operating contract. Morpheus
builds and repairs; he never certifies his own work — Gordon qualifies
(KDD-0010), the governor signs off phases, the owner holds cutover.

## Consequences

Enables: an accountable lane for the full dsh capability surface; the
builder/verifier separation (with Gordon) the doctrine requires; pipelined
build-and-test execution per the approved plan.

Forecloses: Morpheus as orchestrator, self-certifier, or policy plane; upstream
core edits where an out-of-tree extension suffices; any production promotion
without the owner; convention-codification work inside this arc.

Rollback: documentation-only — remove `agents/morpheus/`, revert the roster row,
flip this KDD to superseded. No host, service, or credential state is touched by
the adoption itself (hxs-15 changes are separate work orders).

Revisit if: the owner changes the platform direction, the dsh host, or the
codification scope; or the pinned source identity changes (re-anchor per
Gordon's Gate 0).
