# KDD-0014: Chris registration — PostgreSQL systems engineer

- Date: 2026-08-29
- Status: ratified
- Decider: Agent-Zero
- Related goals: hxs-9 state-services implementation (registry target-state);
  satisfies the Bill-class pairing of KDD-0011 D3 by class

## Context

The registry assigns hxs-9 "State services: PostgreSQL + Redis; LiteLLM
database" (target-state), but nothing is deployed there (verified in the
2026-08-28 post-outage check: no PostgreSQL units, no 5432 listener). Rob's
profile names a future PostgreSQL pairing ("Bill", KDD-0011 D3). The owner's
candidate profile `agent-zero-docs/agent-profiles/chris/chris-profile.yaml`
(profile_version 2026-08-28T21:35:15Z, digest `sha256:15898cb2…5a98`,
preserved unchanged) was reviewed on request 2026-08-29 and dispositioned by
owner directive the same day: authority chain to fit the current operating
model, roster registration, implementation plan via Mia, model lane assigned,
MCP on hold. [LABELED CORRECTION 2026-08-31, append-only: the MCP hold is LIFTED per owner directive 2026-08-31; the 2026-08-29 hold is superseded.]

## Options considered

1. Register as adapted (authority retargeted, lane assigned, activation gated)
   — what the owner directed.
2. Register verbatim (Paul authority chain) — rejected by the owner's first
   disposition point; the current model is KK3 orchestrates, Mia manages,
   Agent Zero owns risk.
3. Defer until hxs-9 is implemented — rejected; registration now lets Mia's
   implementation plan name the accountable lane from day one.

## Decision

Chris is registered: `agents/chris/charter.md` + `agents/chris/profile.md`
(distilled and adapted from the candidate YAML, provenance recorded), roster
row in `agents/README.md`. Adaptations of record: (a) every "Paul" gate reads
as Agent Zero requested through Kimi-K3; escalation runs Kimi-K3 always,
never the owner directly; work distributes via Mia under Kimi-K3-issued work
orders. (b) Model lane: **Qwen 3.8 Flash** (`openrouter/qwen/qwen3.8-flash`,
upstream Alibaba Cloud International, via OmniRoute, route probed live
2026-08-29) — KDD-0013 amendment 6. (c) **MCP surface on HOLD** (owner
directive) — `postgres-mcp-mai` deferred entirely. [LABELED CORRECTION 2026-08-31, append-only: the MCP hold is LIFTED per owner directive 2026-08-31; the 2026-08-29 hold is superseded.] (d) Scope pin: PostgreSQL
only on hxs-9; Redis is explicitly outside his lane. Activation is gated
(profile §10): instance implemented + credential entries + owner word.
[OPEN CORRECTION 2026-08-29, labeled, append-only — Mia per Flash work order
19 (F12): the activation gate sentence above is VOID as an operational gate —
owner ruling the same day (state-log row 42): Chris is the DBA and installs
his own database; the "instance already implemented" precondition was a
chicken-and-egg the owner voided, and credential entries are created BY Chris
during installation, not required before it. The gate text above and in
`agents/chris/profile.md` §10 stands as history; the current single gate is:
(1) owner activation word — GIVEN 2026-08-29 ("proceed with install" + the
DBA ruling), (2) halts at the plan's Checkpoint 1 for owner review, (3) final
activation word remains an owner decision. `agents/chris/profile.md` §10
already carries this revision, labeled, dated 2026-08-29.]
[OPEN CORRECTION 2026-08-29, labeled, append-only — Mia per Flash work order
28 (review batch 2, F15): model lane **DeepSeek V4 Pro**
(`openrouter/deepseek/deepseek-v4-pro`, provider Baidu FP8, via OmniRoute
hxs-8) SUPERSEDES the Qwen 3.8 Flash lane in Decision item (b) above — owner
directive 2026-08-29, CLI-verified live same day (served id
`deepseek/deepseek-v4-pro`, Baidu provider confirmed). The Qwen 3.8 Flash
entry above and in `agents/chris/profile.md` (where it is also corrected) is
preserved as history. Authority: owner directive; `agents/README.md` lane
correction 2026-08-29.]

## Consequences

- The hxs-9 state-services target gains its accountable lane; Mia's
  implementation plan (work order 11) proceeds against this registration.
- KDD-0011 D3 (Bill pairing) is satisfied BY CLASS — the Bill profile is
  unnecessary unless a second, distinct database lane emerges; recorded
  openly for the owner's confirmation. [QUALIFICATION 2026-08-29, labeled,
  append-only — Mia per Flash work order 19 (F13): "satisfied BY CLASS" is
  CONDITIONAL pending primary-owner confirmation — the owner's confirmation
  is not yet recorded in the governance records; this statement does not
  silently amend KDD-0011, whose D3 stands as written until the owner
  confirms the class-satisfaction ruling (cross-ref: KDD-0011 D3 and
  `agents/rob/profile.md`).]
- Chris's lane is the SIXTH cloud lane in the OD-14 metering scope
  (KDD-0013 amendment 6).
- Revisit when: the instance is implemented (activation review), the MCP
  hold is lifted (Trinity's posture applies), or Redis needs a lane.
