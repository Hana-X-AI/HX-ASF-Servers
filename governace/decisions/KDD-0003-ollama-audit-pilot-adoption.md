# KDD-0003: Adopt the Ollama audit pilot with Phase M execution note

- Date: 2026-08-24
- Status: ratified
- Decider: Agent-Zero
- Related goals: `goals/2026-08-24-ollama-audit-hxs5.md`

## Context

A pilot document defining a read-only Ollama audit on hxs-5 (501 lines) was reviewed
against the ratified Kimi-K3 profile (KDD-0001), the goal-setting guidance
(KDD-0002), and repository conventions. The pilot is well-constructed: its Goal
Contract matches the adopted guidance, its state machine is a sound HFSM
simplification, and its process acceptance matrix is a strong addition.

Four conflicts required resolution before adoption:

1. The pilot hard-codes "Kimi-K3 performs zero operational work," but John is a
   profile, not a running agent. Under Phase M, John executes as a profile-briefed
   Kimi Code sub-agent; the governor session runs no audit probes.
2. The knowledge authority path cited `/opt/tkv/ollama`; the standing decision is
   `/opt/tkv-local/ollama`.
3. The evidence destination was left to a mid-pilot pause; this repository's
   `pilots/` tree already provides the answer.
4. Goal ID and file naming did not match KDD-0002 conventions.

## Options considered

1. Adopt verbatim — rejected: conflicts 1–4.
2. Return for author rework — rejected: slower, and breaks the established
   adopt-with-recorded-amendments pattern.
3. Adopt with amendments — chosen.

## Decision

Adopt the pilot at `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-001/plan.md` with amendments:

- Section 2.1 added: Phase M execution note — John executes as a profile-briefed
  sub-agent; the Kimi-K3 governor session runs no audit probes and connects to no
  host; "zero operational work" refers to the governor session under this dispatch
  model.
- Knowledge authority corrected to `/opt/tkv-local/ollama` everywhere.
- Evidence root designated as the pilot directory itself, removing the
  propose-and-pause condition.
- Goal file created at `goals/2026-08-24-ollama-audit-hxs5.md`; pilot status table
  links it.
- `pilots/README.md` activated.

Execution of the audit itself is NOT authorized by this KDD. It requires the
pilot's own section 19 readiness gate and an explicit go from Agent-Zero.

## Consequences

- `pilots/` becomes operational with its first pilot.
- The pilot is the Phase M dogfood of KDD-0001 and KDD-0002: sub-agent dispatch as
  the fresh bounded session, owner review as verifier fallback.
- The source document remains unmodified as historical input.

## Provenance and corrections

- Source document: `/home/hxsa/opt/local-tkv/agent-zero-docs/pilots/audit-pilot.md`
  (501 lines), SHA-256
  `41eb175cac8a3389716e8767c00db298312b052bf29b7d30ec7687fb410fa425`.
- Evidence reviewed: the source in full; ratified profile, guidance, KDD-0001,
  KDD-0002; repository conventions.
- Corrections applied at adoption: the four conflict fixes listed under Decision,
  plus the section 19 readiness-item rewording for the dispatch model.
