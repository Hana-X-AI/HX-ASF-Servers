# Governance Foundation Plan — HX Agentic Software Factory

- **Goal ID:** governance-foundation-plan
- **Status:** ACTIVE — implementation underway (7 workstreams; status per workstream below)
- **Owner:** Agent Zero
- **Created:** 2026-08-29
- **Human authority:** Agent Zero
- **Destination:** `governace/project-plan/` (this file) — per owner directive
- **Directive source:** owner instruction 2026-08-29 (audit input `misc/007/input.md`)

---

## Summary

Build a flawless, repeatable, trackable governance foundation for the HX agentic
software factory. The plan consolidates 7 workstreams that together enforce:
structured governance directories, a continuously-updated test log, mandatory
change documentation, a bullet-proof agent-creation checklist with skill + hooks,
skills in every agent profile, workflow diagrams, and TKV-enforcement evidence.
[OPEN CORRECTION 2026-08-30, labeled, append-only: "continuously-updated test
log" and "bullet-proof agent-creation checklist" are superseded by the accurate
current position — the test log is maintained via a fail-open advisory reminder
hook (ST-7 `test-log-append.sh` does not append; the append is a manual governor
action), and the agent-creation checklist is a 27-step mandatory checklist with
advisory (fail-open) hooks. See the WS2/WS4 corrections below. This correction
remains open.]

This document is the **controlling plan**. Each workstream's artifacts live in
`governace/`; this file records the objective, deliverables, status, and
acceptance criteria for each.

---

## Workstream 1 — Governance directory structure + file migration

**Objective:** one canonical governance tree (`governace/`) with centralized
templates and migrated records.

**Deliverables:**
- `governace/README.md` — root governance readme (DONE)
- `governace/decisions/` — KDDs moved from `knowledge/decisions/` (DONE, 30 KDD files)
- `governace/issue-tracking/issues.md` — issues moved from `knowledge/issues.md` (DONE)
- `governace/lesson-learned/lessons-learned.md` — moved from `knowledge/lessons-learned.md` (DONE)
- `governace/templates/` — single central template dir (DONE): agent/, server/,
  goal, pilot/, kdd, agent-checklist, test-log, change-record, system-config-doc
- Cross-references updated (AGENTS.md, manifest, catalog, profiles, KDDs) (DONE)

**Status:** COMPLETE (audited; canonical path is `governace/` per owner spelling;
path-fork resolved 2026-08-29 — orphan `governance/` removed).

## Workstream 2 — Consolidated test log

**Objective:** one continuously-updated log of ALL test and example results.
[OPEN CORRECTION 2026-08-30, labeled, append-only: the objective reads as
originally written; the accurate current position is "one maintained log" — the
update mechanism is a fail-open advisory reminder (ST-7 `test-log-append.sh`),
not an automatic appender. This correction remains open.]

**Deliverables:**
- `governace/testing/test-log.md` (+ `.html`) — seeded with current results (DONE)
- Covers: LightRAG (7 PASS, 1 FAIL #4, 1 DEP-OK #8, 9 SKIP), Qdrant (V0-V6 PASS),
  DSH (Gates 6-10), PostgreSQL (Step 0+1 PASS, Step 2 PARTIAL), Redis (PASS),
  OmniRoute (PASS)
- Manifest-listed + rendered (DONE)
- Secret-sweep clean (DONE 2026-08-29 — key literal redacted)

**Status:** COMPLETE (append mechanism added via workflow — see WS7/ST-7).
[OPEN CORRECTION 2026-08-30, labeled, append-only: "append mechanism added via
workflow" is superseded by the accurate current position — ST-7
`test-log-append.sh` is a fail-open advisory reminder that prompts a dated row be
added to `governace/testing/test-log.md`; it does not append the row itself (the
append is a manual governor action). See WS4 for the advisory-hook treatment.
This correction remains open.]

## Workstream 3 — Change documentation

**Objective:** every major change produces a change record + system config doc.

**Deliverables:**
- 3 change records in `governace/status-reporting/` — Meta-X→OAI-X, LightRAG,
  Qdrant (DONE; OAI-X status corrected to PROPOSED 2026-08-29)
- 3 system config docs — `servers/hxs-3/oai-x-config.md`,
  `servers/hxs-4/lightrag-config.md`, `servers/hxs-4/qdrant-config.md` (DONE;
  OAI-X marked target-state)
- Templates: `governace/templates/change-record.md`,
  `governace/templates/system-config-doc.md` (DONE)

**Status:** COMPLETE with corrections (change-record lifecycle gate added — ST-6).

## Workstream 4 — Agent creation checklist + skill + hooks

**Objective:** eliminate missed-registration errors when creating agents.

**Deliverables:**
- `governace/templates/agent-checklist.md` — mandatory 27-step checklist (DONE)
  [OPEN CORRECTION 2026-08-30, labeled, append-only: the deliverable above was
  originally worded "mandatory 22-step checklist" — that count is superseded.
  The checklist has 27 steps (items 1-27, validating after each step, fail
  closed). The 22-step wording is preserved here as history; 27 is the active
  count. This correction remains open.]
- `.kimi-code/skills/create-agent/SKILL.md` — agent-creation skill (DONE;
  installed to user scope 2026-08-29)
- `scripts/hooks/agent-creation-check.sh` — PostToolUse hook, fail-open (DONE;
  registered in `~/.kimi-code/config.toml` 2026-08-29, interface fixed to read
  stdin payload)
- Test with Nancy (QA agent) — PENDING owner word

**Status:** COMPLETE (enforcement wired). Test remains owner-gated.
[AMENDMENT 2026-08-30, labeled: the "enforcement wired" wording above overstates
mechanical strength — five of six hooks are fail-open advisory guardrails
(test-log-append reminds, agent-creation-check warns, governor-gate reminds).
Current reading: COMPLETE (mechanics in place; enforcement advisory — hooks are
fail-open), Test remains owner-gated. Original wording preserved above; this is
the current status.]

## Workstream 5 — Skills in every agent profile

**Objective:** every agent profile lists its available skills.

**Deliverables:**
- "Skills available" section (be-great, eli5, bro, wait-what, quick, human,
  corp, copy) added to all 13 agent profiles (DONE)
- Added to agent template (`governace/templates/agent/profile.md`) (DONE)

**Status:** COMPLETE.

## Workstream 6 — Workflow diagrams

**Objective:** 3 Mermaid workflow diagrams showing deliverables + skills/hooks.

**Deliverables (all in `governace/process/`):**
- `agent-creation-workflow.md` (DONE)
- `system-deployment-workflow.md` (DONE)
- `system-validation-testing.md` (DONE)

**Status:** COMPLETE.

## Workstream 7 — TKV enforcement evidence

**Objective:** empirical evidence every agent has a specific TKV directive,
enforced.

**Deliverables:**
- `governace/process/tkv-enforcement-evidence.md` — 13-agent evidence table
  (DONE)
- All 13 agents have: specific `/opt/tkv-local` path + be-great reference +
  standing directive (DONE; carol/kimi-k3/mia fixed)

**Status:** COMPLETE.

---

## Enforcement additions (post-audit 2026-08-29)

The QA audit (misc/007/audit-*.md) found the original execution committed the
artifacts but did not wire enforcement and fabricated one completion. This plan
adds:

- **Verification-checklist gate:** `governace/process/governor-verification-checklist.md`
  (role-neutral location, moved from `agents/kimi-k3/` 2026-08-30)
  (governor evidence receipt-check) is the mandatory pre-acceptance gate for
  every producer deliverable (R-6).
- **Agent-creation hook** registered (WS4) — fires on `agents/` writes.
- **render-sync / manifest-drift hook** — added (ST-4) to catch path drift
  before commit.
- **Change-record lifecycle** — `PROPOSED → IN PROGRESS → COMPLETE`, gated on
  goal/plan status + execution evidence (ST-6).
- **Context-budget + lane-probe** fields in the work-order template (ST-5).
- **Test-log append hook** (ST-7) — fail-open advisory reminder: `test-log-append.sh`
  prompts the governor to add a dated row to `governace/testing/test-log.md`; it does
  not append the row itself (the append is a manual governor action).
- **Dual-format compliance** (SY-6) — every manifest-listed document keeps a
  rendered `.html` sibling; enforced mechanically by
  `python3 scripts/wiki/render.py --check` (79/79 in sync at acceptance).
- **Per-wave read-only audit** (SY-7) — after each material remediation wave,
  the governor re-runs the 4-domain QA audit (governance/process/docs/hooks)
  as read-only review; findings become the next wave's work orders, and this
  plan's acceptance criteria are re-checked before any new wave is opened.
- **Governance-path integrity check** (SY-2) — `validate.py` fails if the
  rejected `governance/` fork exists or the canonical `governace/` tree is
  missing.

## Acceptance criteria

1. `python3 scripts/validate.py` → 5/5 PASS.
2. `python3 scripts/wiki/render.py --check` → all manifest docs in sync.
3. `governace/project-plan/` contains this controlling plan (this file).
4. Agent-creation hook + skill verified registered (grep config.toml).
5. No secret literal in any tracked file (secret-boundary 0 hits).
6. Change records never claim COMPLETE without matching executed evidence.
7. A new agent (Nancy) passes the full checklist when the owner gives the word.

## Completion rule

This goal is done only when every acceptance criterion passes with evidence and
the owner accepts — not when the work feels done. Per KDD-0002 goal-setting
contract.
