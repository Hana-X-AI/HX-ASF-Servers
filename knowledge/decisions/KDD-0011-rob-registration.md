# KDD-0011: Rob registration — full-stack engineer for the DeepSeek Harness

- Date: 2026-08-28
- Status: ratified
- Decider: Agent-Zero
- Related goals: GOAL-DSH-IMPL-001 (PILOT-DSH-IMPL-001)

## Context

The DSH full-implementation arc created the platform (Morpheus) and its
independent QA (Gordon), but no application-layer consumer — "a harness with no
developer is a race car with no driver." Kimi-K3 drafted Rob's profile at owner
request (`agent-zero-docs/projects/Deepseek/kk3_20260828_0956_rob-...md`, DRAFT,
preserved unchanged). The owner's review of per-agent model assignments
(2026-08-28) included "Rob — how did you forget Rob" with his model lane named
directly, which is the ratification word.

## Options considered

1. Register as drafted (DRAFT → ratified, distillation into `agents/rob/`) —
   keeps the activation gates and lane separation intact.
2. Redraft — unnecessary; the draft was prepared for exactly this comparison
   and the owner ratified it by directing registration.
3. Leave application work with the governor — violates Kimi-K3's bar on direct
   execution (the gap the draft exists to close).

## Decision

Rob is registered: `agents/rob/charter.md` + `agents/rob/profile.md`, roster
row in `agents/README.md`. Source §12.3 D1 (model lane) is RESOLVED as **Z.ai
GLM 5.3 Flash via OmniRoute** (owner, 2026-08-28, KDD-0013) — against the
source document's Coder-X recommendation; recorded openly. Activation remains
gated per profile §10: Gordon Gate 7 PASS **and Gate 10 entry conditions met** +
named work order + the owner's explicit activation word. Registration is not activation.

## Consequences

- The application layer now has an owner lane; the governor's direct-execution
  pressure is relieved once activation gates pass.
- D2 (product verification — Janet), D3 (Bill pairing), D4 (write targets)
  remain open owner decisions; the governor's verifier contract covers the
  interim.
- Rob's GLM lane spends against the OD-14 OpenRouter exception (USD 100 cap,
  owner-lane allowlist, metered via `usage_history`) once activated.
- Revisit when: Gate 7 signs (activation review), or the first data-heavy
  target appears (Bill), or verification load justifies Janet.
