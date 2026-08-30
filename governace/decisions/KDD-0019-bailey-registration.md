# KDD-0019: Bailey registration — Sr. AI Testing Engineer

- Date: 2026-08-30
- Status: ratified
- Decider: Agent-Zero
- Related: KDD-0013 Amendment 11 (QA job-family lane default — Bailey, Gordon → Qwen3.8 Flash), KDD-0012 (Mia — Chief of Staff management), KDD-0018 (raphael registration — recent pattern), `governace/templates/agent-checklist.md` (registration checklist)

## Context

The factory's QA capacity is split across two roles: Gordon executes and
qualifies (KDD-0010, independent qualification), but no dedicated agent owns
test-authoring. The alignment session of 2026-08-30 locked the QA job family
(lane-config family, separate from the KDD-0016 taxonomy) as **Bailey + Gordon**,
with a family default lane of Qwen3.8 Flash (KDD-0013 Amendment 11). A dedicated
Sr. AI Testing Engineer is needed to author test plans, test scripts, and
pinned stacks for factory components without crossing into environment setup,
execution, or repair.

## Decision

Register Bailey as the Sr. AI Testing Engineer for HX-ASF, QA job family.

### Lane assignment

- Model lane: Qwen3.8 Flash (`qwen/qwen3.8-flash`, provider Alibaba Cloud
  International, via OmniRoute hxs-8) — QA family default per KDD-0013
  Amendment 11 (owner decision 2026-08-30). Same lane default as Gordon
  (Gordon override recorded 2026-08-29). Bailey's lane is a metered cloud lane
  within the OD-14 exception of record.

### Job family / placement

- QA (lane-config job family, KDD-0013 Amendment 11; NOT a KDD-0016 4-family
  taxonomy family — no taxonomy-table entry).
- Horizontal, not host-bound — no system-mapping S<N> row; added to the
  "Horizontal agents (not host-bound)" table alongside gordon.

### Adaptations from source

1. No external source document — original profile per the alignment session
   2026-08-30.
2. Default knowledge (TKV): `/opt/tkv-local/pytest-main` and
   `/opt/tkv-local/zod-main`.
3. QA-skills subset (future-lift, separate work item 4 — NOT created in this
   registration): `ai-test-generation`, `test-planning`, `test-strategy`,
   `qa-project-context` from `/opt/tkv-local/qa-skills-main` v3.0.0 (MIT);
   recorded in her profile's "Skills available" section as future-lift items.
4. Test framework default: python/pytest (zod for TS-side contracts).
5. Deliverable location: `governace/qa/<project-name>/` — separate folder per
   project.
6. Test loop (locked): Erwin installs → Bailey authors → Gordon sets up env +
   executes → results to testing log → Gordon notifies Bailey + Erwin → Erwin
   fixes config → Gordon retests → max 3 iterations → James accepts on the
   verification-checklist.

> **[OPEN CORRECTION 2026-08-30, labeled, append-only — QA-SKILLS LIFT LANDED
> (supersedes adaptation 3 above, which is preserved as history):]** the
> original adaptation 3 above described the QA-skills subset as "future-lift,
> separate work item 4 — NOT created in this registration" — preserved as the
> historical decision wording. The lift landed in this change: the QA skills
> (`ai-test-generation`, `test-planning`, `test-strategy`, `qa-project-context`,
> `test-reliability`, `test-environments`, `release-readiness`,
> `ci-cd-integration`) are created under `.kimi-code/skills/` and AGENTS.md's
> skill count reflects them. Bailey's "Skills available" is updated accordingly;
> the skills are current authority for her test-authoring work, subject to the
> activation gate below.

### Activation gate

Bailey is registered but activation-gated. Conditions:
1. Implemented testing-role usage — her test plan/script/pinned-stack
   deliverables exercised in at least one project.
2. Credential entries for her lane/route exist in `.local.env` (variable
   references only).
3. The governor's explicit activation word.

## Roster entry

`agents/bailey/` created (charter + profile, per KDD-0016 standard template).
Roster row added to `agents/README.md` (Status: registered — activation gated).
Horizontal-agent row added to `servers/system-mapping.md`. QA deliverable home
`governace/qa/` created with README. Catalog records
`DOC-agent-bailey-charter`, `DOC-agent-bailey-profile`,
`DOC-kdd-0019-bailey-registration` added to `knowledge/catalog/` and the index.

## Provenance

Original record — no external source document. Created per the alignment
session 2026-08-30 (role spec locked; KDD-0013 Amendment 11 lane-defaults
table LOCKED). Knowledge base: `/opt/tkv-local/pytest-main`,
`/opt/tkv-local/zod-main`, `/opt/tkv-local/qa-skills-main` (v3.0.0, MIT).
Model lane: Qwen3.8 Flash via OmniRoute, provider Alibaba Cloud International —
QA family default per KDD-0013 Amendment 11.
