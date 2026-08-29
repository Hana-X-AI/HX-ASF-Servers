# KDD-0001: Adopt the Kimi-K3 meta-agent control model with phased activation

- Date: 2026-08-24
- Status: ratified
- Decider: Agent-Zero
- Related goals: none yet

## Context

The HX AI Software Factory needs a control-plane governance model for multi-agent
work: decomposition of goals, agent supervision, evidence gates, recovery, and
escalation. A first-pass Kimi-K3 meta-agent profile was reviewed against the
ai-software-factory reference architecture and this repository's current state.

The review found the profile architecturally sound but self-violating under the
current operating model: its section 2.1 prohibits the meta-agent from all
operational work, while the current phase is manual-first and the only operational
agent lane is john. Adopted as written, every current task would be a governance
breach. The review also found that the prohibition would initially be prompt-only,
since Kimi-K3 holds execution tools until an executable agent definition with
tool-level controls exists.

## Options considered

1. Adopt as written — rejected: prohibits the work Kimi-K3 currently performs, and no
   operational agents exist to delegate to.
2. Defer adoption until the agent fleet exists — rejected: leaves the manual phase
   ungoverned and delays the evidence and gate discipline that is already needed.
3. Adopt with phased activation — control model active now with a documented Phase M
   execution exception; prohibitions engage per capability as agent charters
   activate; full control-plane-only operation once the fleet can carry execution.

## Decision

Adopt option 3. `agents/kimi-k3/profile.md` is ratified with the phased activation
clause (section 2.3):

- Phase M (current): Kimi-K3 may perform bounded operational work directly when no
  qualified operational agent exists, under evidence discipline and human
  checkpoints, with owner pre-approval for destructive or irreversible actions.
- Phase A: section 2.1 prohibitions engage per capability area as agent charters in
  `agents/` are activated. Work with a qualified agent must be delegated.
- Phase C: full control-plane-only operation, enforced by tool-level controls in an
  executable agent definition (`.kimi-code/agents/`).

Phase transitions require owner approval and a new KDD entry for each transition;
appending to an existing KDD does not satisfy this.

## Consequences

- Kimi-K3's direct work during Phase M is compliant, not a governance breach.
- Agent charters in `agents/` become the delegation activation mechanism.
- Run records map to existing repository homes: Intent and Authority Receipts to
  `goals/`, process learning to `governace/lesson-learned/lessons-learned.md`. No second registry
  plane is created.
- The prompt-only enforcement gap is explicitly recorded until Phase C tooling
  exists.
- Independent verification of Kimi-K3's own Phase M work uses owner review as the
  verifier of last resort, with the required verification evidence and a recorded
  approval (profile section 14).

## Provenance and corrections

Per the repository's adoption-of-provided-documents rule (AGENTS.md):

- Source document:
  `/home/hxsa/opt/local-tkv/agent-zero-docs/agent-profiles/meta-agent/codex_20260824_1050_kimi-k3-meta-agent-profile.md`
  (first pass, 701 lines), SHA-256
  `7c355b689703544a6ee15d9f606c26aa2ab2cb4d91b4ca8df52bdd6a9a3eea5c`.
- Evidence reviewed: the source profile in full; the ai-software-factory-main
  reference architecture (README, `docs/book/01-concepts.md`); this repository's
  state and conventions (AGENTS.md, `agents/`, `goals/`, `knowledge/`).
- Adopted documents: `agents/kimi-k3/profile.md` (ratified revision) and
  `agents/kimi-k3/charter.md`, both linking back to this record.
- Corrections applied in the ratified revision:
  1. Added section 2.3 phased activation (M/A/C) with the phase-transition rule.
  2. Status changed from "Production-ready" to ratified with phased activation.
  3. Control artifacts mapped to repository homes (`goals/`,
     `governace/lesson-learned/lessons-learned.md`); no second registry plane.
  4. Authority model extended with repository authorities (AGENTS.md, KDDs,
     SERVER-REGISTRY.md, ratified goal files).
  5. Prompt-only enforcement gap recorded explicitly (section 7.1).
  6. Post-adoption review fixes: Phase M charter-check recording (section 2.3 and
     the Intent and Authority Receipt), new-KDD-per-transition wording, explicit
     HFSM non-completion transitions, owner-review verifier fallback in Phase M,
     and this provenance record.
- The source first pass remains unmodified as historical input.

[OPEN CORRECTION 2026-08-29, labeled, append-only: the GOVERNOR ROLE has
transferred from kimi-k3 to **Flash** (owner/Agent Zero appointment,
2026-08-29), running on DeepSeek V4 Flash via OmniRoute. This KDD
recorded the original adoption of the kimi-k3 meta-agent model; the
governor-transition is recorded in AGENTS.md labeled correction blocks
and KDD-0013 Amendment 8. kimi-k3 is now an identity-specific model lane
(`moonshot-ai/kimi-k3`), not the governor. The ratified status and
Phase M/A/C framework above are preserved as history — the governor role
and its authority chain are defined in the current AGENTS.md. Authority:
AGENTS.md governor-transition correction; KDD-0013 Amendment 8;
state-log row 46.]
