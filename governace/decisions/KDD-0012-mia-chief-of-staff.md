# KDD-0012: Mia — Chief of Staff to the Governor

- Date: 2026-08-28
- Status: ratified
- Decider: Agent-Zero
- Related goals: factory operating model; applies to all active arcs

## Context

Owner directive 2026-08-28, verbatim: "kk3 as the Governor you will not do work
as real Governor's do in human life. you will hire/ create a Chief of Staff
agent Mia who's role is planning and coordination and management of the work
and report back to you. if something is broken you will give it to Mia to fix.
or to distribute to the Engineering agents."

Until now the governor carried both governance (goals, gates, evidence
acceptance) and work management (sequencing, routing, follow-up, triage)
directly. The owner separated the two: the Governor governs; a Chief of Staff
manages.

## Options considered

1. Chief of Staff as a registered horizontal agent (Mia) — explicit lane,
   charter-bounded, no governance authority.
2. Keep management inside Kimi-K3 — rejected by the owner's directive itself.
3. Fold management into an existing agent — every existing lane is a domain
   lane; none is chartered for cross-lane coordination, and adding it would
   blur an existing boundary.

## Decision

Mia is created and active: `agents/mia/charter.md` + `agents/mia/profile.md`,
roster row in `agents/README.md`. Her class is **management, not governance**:
planning, coordination, distribution, tracking, breakage triage, and reporting
to Kimi-K3. Gates, sign-off, evidence acceptance, verdicts, and owner
escalation remain Kimi-K3's alone. Broken items go to Mia first: she
characterizes and coordinates or distributes with evidence; she never mutates
an engineering lane or issues repair dispositions herself — repair
authorization and dispositions stay with Kimi-K3 and execute only under
Kimi-K3-issued work orders. [Corrected 2026-08-28, labeled: this passage
originally read "she characterizes, repairs in-lane, or distributes to the
owning engineering lane with evidence" — the repair-in-lane phrasing
overreached her management-only mandate; original preserved here.] Model lane: **Z.ai GLM 5.3 Flash via OmniRoute** (owner,
2026-08-28, KDD-0013). No external source document exists; her profile is the
original record of the role.

## Consequences

- The standing flow becomes Kimi-K3 → Mia → engineering agent for managed work;
  gates and ratified pilot contracts (including the DSH arc's Morpheus/Gordon
  pipeline and its checkpoints) are unchanged — Mia carries coordination, not
  verdicts.
- Mia's GLM lane spends against the OD-14 OpenRouter exception (USD 100 cap,
  metered) when her lane performs inference.
- Revisit if: the management/governance boundary blurs in practice, or her
  reporting shape fails the governor's gate needs.
