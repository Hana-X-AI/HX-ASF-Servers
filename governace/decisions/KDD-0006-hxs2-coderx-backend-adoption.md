# KDD-0006: Adopt the hxs-2 CoderX coding-inference backend pilot

- Date: 2026-08-26
- Status: ratified
- Decider: Agent-Zero
- Related goals: 2026-08-26-hxs2-qwen36-coderx-backend

## Context

The owner commissioned the hxs-2 mission (Alert 1, 2026-08-26) with a corrected
directive: provision hxs-2 as a persistent coding-inference host and register
the model as an approved backend. The directive's architecture named DeepSeek
Harness as the registration/governance substrate ("existing Harness
infrastructure"). Verification against all records found no deployed Harness
anywhere; the owner confirmed 2026-08-26 that DeepSeek Harness does not exist
and has never been deployed — the premise was an easter egg. The model-identity
question (directive tag `…-coder:vision-Q4_K_M` vs the supplied knowledge
reference's `…-coderx` family) was resolved by live registry evidence: both
families exist as DIFFERENT checkpoints (Coder sibling: top-10, pure
expert-selection prune; CoderX: top-8, REAP/DERN redistribution prune), and the
owner selected CoderX (D3). hxs-1's playbook (closed PASS at M8, 2026-08-26)
provides the proven pattern, fixtures, templates, and lessons.

## Options considered

1. Proceed Harness-free with the Second Brain catalog as the capability
   registry (selected) — the registry/discovery role maps to KDD-0005's
   canonical catalog; KK3 assigns through standard work orders.
2. Provision-only with no registration concept — rejected: leaves the backend
   undiscoverable and the consumer-proof unproven; the catalog fills the role
   at zero new infrastructure cost.
3. Defer the pilot until a Harness exists — rejected: the substrate is not on
   any approved roadmap for near-term deployment; the backend is needed now.

## Decision

Adopt PILOT-HXS2-CODERX-BACKEND-001: provision hxs-2 with
`mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M` (exact tag + full local digest as
identity), validated per the hxs-1 playbook, exposed via a LAN-scoped endpoint
(192.168.50.0/24 allowlist, D2), and registered in the Second Brain catalog as
the discoverable backend-capability of record. The DeepSeek Harness premise is
closed as verified-nonexistent; any future Harness-era registration is out of
scope. Owner decisions D1–D8 are recorded in the goal file.

## Consequences

Enables: the factory's second host becomes a validated inference node; the
catalog gains a backend-capability record class (Second Brain "act" stage);
the hxs-1 playbook earns its second validated use (pattern-promotion evidence).
Forecloses: any DeepSeek Harness dependency, the Coder sibling as this pilot's
model, exposure beyond the LAN boundary, cross-model quality transfer (CX-R13).
Revisit if: a real DeepSeek Harness is ever commissioned (registration mapping
would be re-evaluated), or the owner changes the exposure boundary.
