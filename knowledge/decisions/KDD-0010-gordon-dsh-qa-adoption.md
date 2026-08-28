# KDD-0010: Adopt Gordon as independent DeepSeek Harness qualification specialist

- Date: 2026-08-28
- Status: **ratified 2026-08-28** — owner directive ("You will implement Gordon,
  aka G, and he will plan and execute all testing after each phase. G will
  produce evidence for your review and sign-off"; "G should be working in
  parallel with Morp — this should not be serial activity")
- Decider: Agent-Zero
- Related: plan `agent-zero-docs/projects/Deepseek/2026-08-28-dsh-full-implementation-plan.md`;
  source profile `codex_20260828_0739_gordon-*.md` (preserved unchanged at
  `agent-zero-docs/projects/Deepseek/`)
- Truth-state: roster and governance claims [AUTHORITY]; dsh product facts
  [CANDIDATE until candidate-grounded under commission]

## Context

The approved DSH full-implementation plan requires independent qualification:
the builder must not judge the build. The owner's profile for Gordon (726
lines, codex 2026-08-28) defines that role — a gate program (Gates 0–10), a
Feature Coverage Ledger with nine dispositions, severity/stop rules, and
evidence contracts. Owner rulings recorded: Gordon works IN PARALLEL with
Morpheus (authors test plans/scripts while Morpheus builds; executes as
capabilities land); Gordon may execute dsh and install test tooling on hxs-15
but changes NO configuration — every fix routes to Morpheus.

## Decision

**ADOPT 2026-08-28:** Gordon ("G") joins the roster (horizontal — quality) as
the independent dsh qualification and regression specialist.
`agents/gordon/charter.md` + `profile.md` (distilled from the preserved source)
are the operating contract. Gordon tests and reports; he never repairs, never
approves his own harness, never decides production risk. The governor reviews
his evidence and signs off each phase; the owner holds the final word.

## Consequences

Enables: the builder/verifier separation the doctrine requires; a single
coverage surface (the ledger) for phase sign-off; regression discipline that
survives the implementation arc into operations.

Forecloses: Gordon as developer, operator, orchestrator, or incident commander;
skip-to-pass inflation; certification of a candidate by its builder; production
promotion on builder self-report.

Rollback: documentation-only — remove `agents/gordon/`, revert the roster row,
flip this KDD to superseded.

Revisit if: the owner changes the qualification authority, the gate program, or
Gordon's rights on the system under test.
