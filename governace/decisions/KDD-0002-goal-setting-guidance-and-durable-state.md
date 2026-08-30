# KDD-0002: Adopt goal-setting guidance and designate goals/ as the durable state system

- Date: 2026-08-24
- Status: ratified
- Decider: Agent-Zero
- Related goals: none yet

## Context

A first-pass goal-setting and agent-invocation guidance document (735 lines) was
reviewed against the ratified Kimi-K3 profile (KDD-0001), this repository's `goals/`
conventions, and the Kimi Code sub-agent execution model.

The review found the guidance architecturally strong: its "fresh, bounded
operational session" pattern maps directly onto sub-agent dispatch, and its Goal
Contract is a superset of the existing goal template. Three conflicts required
resolution: the text assumed the full agent-fleet end state and omitted the Phase M
exception ratified in KDD-0001; it named GitHub Projects as the durable work-state
system while this repository already designates `goals/` files; and its status
("Production guidance") and Appendix A source references did not meet the
adoption-of-provided-documents rule in AGENTS.md.

## Options considered

1. Adopt verbatim — rejected: contradicts the ratified Phase M model and creates a
   second work-state authority (GitHub Projects) alongside `goals/`.
2. Defer adoption — rejected: goal-based work begins now and needs its contract.
3. Adopt with amendments — chosen: Phase M operation note added, `goals/`
   designated as the durable state system, status and provenance corrected, and the
   goal template upgraded to a Phase-M-sized subset of the contract.

## Decision

Adopt option 3.

- The guidance is adopted at `agents/kimi-k3/goal-setting-guidance.md` with
  amendments (section 4.3 Phase M operation, section 10 durable-state designation,
  status correction, goal-ID mapping, Appendix A provenance note).
- `goals/` goal files are the designated durable work-state system. GitHub Projects
  is a deferred optional layer, introducible only by owner decision with a new KDD.
  [HISTORICAL 2026-08-30, labeled: this `goals/` system-of-record designation is
  superseded by Amendment 1 below — the durable goal tree relocated to
  `governace/goals/` (2026-08-30). Read this designation as the relocated tree; do
  not treat the removed root `goals/` path as current.]
- `goals/_template.md` is upgraded to the contract subset; the goal file name
  (`<YYYY-MM-DD>-<slug>.md`) is the Goal ID.
  [HISTORICAL 2026-08-30, labeled: `goals/_template.md` now lives at
  `governace/goals/_template.md` (Amendment 1, 2026-08-30). The former path is
  preserved here as history.]

## Consequences

- One work-state authority exists: `goals/`. No board tooling is introduced now.
  [HISTORICAL 2026-08-30, labeled: the work-state authority now lives under
  `governace/goals/` per Amendment 1 (2026-08-30); this sentence is preserved as
  the original consequence wording.]
- In Phase M, a "fresh operational session" means a sub-agent dispatch, or bounded
  direct execution by Kimi-K3 under profile section 2.3 with the charter check
  recorded; owner review is the verifier fallback (profile section 11).
- Goal files gain success-condition tables, evidence contracts, budgets, and stop
  conditions; completion requires evidence, not narrative.
- Appendix A's source pattern is recorded as owner-provided historical input, not
  authority.

## Provenance and corrections

- Source document:
  `/home/hxsa/opt/local-tkv/agent-zero-docs/goals/codex_20260824_1112_kimi-k3_goal-setting-and-agent-invocation-guidance.md`
  (735 lines), SHA-256
  `8c7e1397af21360fbfa83b1f20450521f3b0cefea5c523d39267ab40712cc59e`.
- Evidence reviewed: the source in full; the ratified profile and KDD-0001; this
  repository's `goals/` and AGENTS.md conventions.
- Corrections applied at adoption:
  1. Status changed from "Production guidance" to ratified with amendments.
  2. Section 4.3 added: Phase M operation (sub-agent dispatch, section 2.3 direct
     execution, owner-review verification fallback).
  3. Durable work state designated as `goals/`; GitHub Projects deferred-optional.
  4. Goal-ID mapping to the goal file name added.
  5. Appendix A provenance noted as owner-provided historical input.
- The source document remains unmodified as historical input.

---

## Amendment 1 (labeled, append-only, 2026-08-30) — durable goal tree relocated to `governace/goals/`

**[OPEN CORRECTION 2026-08-30, labeled, append-only — GOAL TREE RELOCATED
`goals/` → `governace/goals/`:** the durable goal tree designated by this KDD
as the system of record has been relocated from the repository-root `goals/`
directory to `governace/goals/` (S1 move, completed 2026-08-30). The
designation and decision text of this KDD stand unchanged; only the physical
home of the goal files changed. All goal files, their HTML siblings, and the
goal template now live under `governace/goals/`; the root `goals/` directory
no longer exists. Live references in this repository now use
`governace/goals/`; historical references to `goals/` in this and other
decision records are preserved as written and read as the relocated tree.
Authority: S1 goal-tree move executed under the alignment batch, 2026-08-30;
recorded here append-only per the documentation-governance contract.]**
