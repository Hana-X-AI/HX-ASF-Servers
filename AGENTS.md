# AGENTS.md

## Skills and trigger words

Thirty owner-installed skills govern how work is done in this repository. Their
canonical home is `.agents/skills/` (KDD-0020, 2026-08-30). Two generated
mirrors carry them into the harnesses that read a tool-specific path —
`.kimi-code/skills/` (Kimi Code) and `.claude/skills/` (Claude Code) — plus the
user scope at `~/.kimi-code/skills/`. Author and edit skills ONLY in
`.agents/skills/`, then run `python3 scripts/skills_sync.py --write`;
`validate.py` check SY-3 fails the repo if a mirror drifts.

**Global skill inventory (D3 / Option A, ratified 2026-08-30):** this section IS
the global skill inventory. Every agent inherits ALL skills listed below by
default. Agent profiles therefore do not enumerate the common skills; a profile's
"Skills available" section lists only role-specific additions beyond this global
inventory (e.g. `create-agent`, the QA-skills subset). To change the effective
set, amend this inventory — do not list the common set per-profile.

- **be-great** — owner trigger: **"be great"**. Exhaustive, evidence-first investigation:
  establish authority, verify current facts, reconcile contradictions, follow downstream
  implications, pressure-test alternatives, and deliver a defensible verdict.
- **be-smart** — owner trigger: **"be smart"**. Clear, concise, actionable communication
  contract: banned phrases, reference-point codes, hard operational boundaries, and the
  `scr` / `eli` / `foc` / `ref` aliases.
- **evidence-first-research** — owner trigger: **"recon"**. Rigorous, source-grounded
  research with primary-source preference, an evidence ledger, explicit confidence
  levels, and traceable citations.
- **eli5** — owner trigger: **"eli5"**. Report in plain ASD-STE100-style English:
  short sentences, one idea per sentence, jargon explained immediately, and only what
  was done, whether it worked, and what to do next. Governs reporting style only —
  code, commands, and paths stay exact.
- **bro** — owner trigger: **"bro"**. Restate the last reply in plain human language,
  no jargon.
- **wait-what** — owner trigger: **"wait what"**. Re-pitch the message that lost the
  owner, with the missing context, in ASD-STE100-style English.
- **quick** — owner trigger: **"quick"**. Answer fast: action first, numbered steps,
  one next step, no preamble.
- **human** — owner trigger: **"casual"**. Talk like a friend: warmer, write like
  you speak.
- **corp** — owner trigger: **"formal"**. Executive-summary tone, formal business
  English.
- **copy** — owner trigger: **"punchy"**. Rewrite as ad copy: hooks first, short
  lines, sell do not explain.
- **archify** — owner trigger: **"archify"**. Generate polished, validated architecture,
  workflow, sequence, data-flow, and lifecycle diagrams as self-contained interactive
  HTML with inline SVG. Accept plain-language requirements, Mermaid input, or repository
  evidence. Five diagram types, four presets, dark/light themes. Requires Node.js >=18
  (v24.20.0 installed at `/opt/node/` on hxs-5). Skill at `.agents/skills/archify/`
  (canonical only — the mirrors carry a pointer stub, not a copy; it is a Node CLI
  invoked by path, not a prompt skill).
- **create-agent** — owner trigger: **"create agent" / "new agent" / "register
  agent"**. Guides the creation of a new HX factory agent: reads
  `governace/templates/agent-checklist.md` and walks each step, validating after each.
- **goal-decompose** — owner trigger: **"decompose goal" / "break the goal into
  work orders"**. Spec-driven goal decomposition for James: turns a confirmed
  scope-lock/goal contract into atomic work orders with dependency + parallelization
  metadata (adapted from automazeio/ccpm, MIT). Scripts report goal-tree status.
- **work-status** — owner trigger: **"what's our status" / "standup" / "what's
  blocked"**. Deterministic goal/work-order status, standup, blocked, in-progress,
  next, and validate reporting for Mia (adapted from automazeio/ccpm, MIT).
  Read-only reporting to the governor; never mutates goal files.
- **grill-me** — owner trigger: **"grill me"**. Scope-lock interview for James:
  clarifies objective, target, boundaries, exclusions, acceptance, and assigned
  lane before a work order dispatches. LIMITED to 5 questions (owner directive
  2026-08-30) — not relentless (adapted from mattpocock/skills, MIT).
- **ai-test-generation** (Bailey) — owner trigger: **"generate tests"**. Staged
  pipeline from specs/PRDs/diffs/bugs/OpenAPI to traceable test code: requirements
  extraction → risk analysis → coverage matrix → oracles → pytest (zod for TS
  contract tests), reviewed before Gordon executes (adapted from
  petrkindlmann/qa-skills v3.0.0, MIT).
- **test-planning** (Bailey) — owner trigger: **"sprint test plan" / "release
  test plan" / "test estimation"**. Authors sprint/release test plans: feature
  decomposition, requirements-to-test coverage mapping, effort estimation by test
  type, risk×effort prioritization, and buffered scheduling (adapted from
  petrkindlmann/qa-skills v3.0.0, MIT).
- **test-strategy** (Bailey) — owner trigger: **"test strategy" / "QA strategy
  doc" / "QA roadmap"**. Produces the multi-quarter QA strategy: scope,
  risk-based prioritization, test pyramid analysis, entry/exit criteria, quality
  gates, KPIs, and a phased timeline (adapted from petrkindlmann/qa-skills
  v3.0.0, MIT).
- **qa-project-context** (Bailey) — owner trigger: **"set up QA context" /
  "configure testing"**. Authors `governace/qa/<project-name>/qa-project-context.md`
  — the single file every other QA skill reads first for tech stack, environments,
  quality goals, and risk areas (adapted from petrkindlmann/qa-skills v3.0.0, MIT).
- **test-environments** (Gordon) — owner trigger: **"set up test environment" /
  "staging parity"**. Designs and stands up test environment tiers (dev/CI/
  preview/staging/prod), audits parity against production, and stubs external
  dependencies at the HTTP boundary (adapted from petrkindlmann/qa-skills
  v3.0.0, MIT).
- **release-readiness** (Gordon) — owner trigger: **"release ready" / "go/no-go"
  / "rollback plan"**. Evidence-based go/no-go qualification: go/no-go checklist,
  smoke suite design, staged rollout validation, rollback criteria defined before
  deploy, and post-deployment verification (adapted from petrkindlmann/qa-skills
  v3.0.0, MIT).
- **test-reliability** (Gordon) — owner trigger: **"flaky test" / "test
  stability" / "quarantine flaky test"**. Flake classification by root cause,
  resilient locator patterns, environment-aware and data healing, confidence-scored
  repair with evidence, and quarantine management (adapted from
  petrkindlmann/qa-skills v3.0.0, MIT).
- **ci-cd-integration** (Gordon) — owner trigger: **"CI/CD" / "test in CI" /
  "shard tests in CI"**. Wires the pipelines that run the test suites: trigger-to-suite
  mapping, sharding, evidence artifact storage, flaky quarantine, coverage gates,
  and keyless deploy (adapted from petrkindlmann/qa-skills v3.0.0, MIT).
- **handoff** — owner trigger: **"handoff"**. Compact the current conversation
  into a handoff document a fresh agent can resume from, naming the skills the
  next session should call; references existing artifacts by path instead of
  duplicating them (adapted from mattpocock/skills, MIT).
- **writing-for-agents** — owner trigger: **"writing for agents"**. Authoring
  contract for instructions other agents must execute: unambiguous imperatives,
  no decorative prose, explicit success and failure conditions (adapted from
  mattpocock/skills, MIT).
- **triage** — owner trigger: **"triage"**. Turn a raw request into scoped,
  actionable work: classify it, size it, name what is out of scope, and route it
  (adapted from mattpocock/skills, MIT).
- **diagnosing-bugs** — owner trigger: **"diagnose"**. Evidence-first debugging
  loop: reproduce, isolate, form and test one hypothesis at a time, and prove the
  fix against the original reproduction (adapted from mattpocock/skills, MIT).
- **grill-with-docs** — owner trigger: **"grill with docs"**. Design interview
  that records decisions and vocabulary as it goes; calls `grilling` and
  `domain-modeling`. NOT the scope-lock gate (adapted from mattpocock/skills, MIT).
- **grilling** — owner trigger: **"grill"**. Design-tree interview in rounds,
  frontier-first, each question carrying a recommended answer. HX-corrected to a
  **5-question-per-round budget** (owner directive 2026-08-30); the remainder
  becomes explicit stated assumptions (adapted from mattpocock/skills, MIT).
- **domain-modeling** — owner trigger: **"domain model"**. Build and sharpen a
  project's domain model: challenge terms against the glossary, stress-test with
  scenarios, record decisions. HX-corrected: inside this repository decisions are
  append-only KDDs under `governace/decisions/`, never `docs/adr/` (adapted from
  mattpocock/skills, MIT).

When the owner uses a trigger word, invoke the matching skill first and follow its
workflow in full — do not partially apply it. Project agents and sub-agents working in
this repository must honor these skills as well.

Provenance: this inventory grew 14 → 23 → 30 skills over 2026-08-30. The seven
most recent additions come from `mattpocock/skills` @
`6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` (MIT), five of them adopted-as-corrected
per §"Adoption of provided documents" with per-skill correction notes in each
SKILL.md and pins in `skills-lock.json`. Ratified by KDD-0019 (QA subset) and
KDD-0020 (canonical tree + mattpocock batch), both append-only and both carrying
the full supersession history. Flattened here 2026-08-30 per audit item F2/A1.

Default reporting voice: **corporate** (executive-summary tone). A voice trigger
overrides the default for that reply; when style skills conflict, the owner's most
recent explicit trigger wins.

## Communication contract

Always on, distilled from the **be-smart** skill (say "be smart" to load the full
contract with examples).

- Banned phrases: "load-bearing", "worth stating plainly", "here's the honest truth",
  "the real tension", "carry the argument", "that's on me".
- No flattery, no decorative headings or emoji, no motivational language. State each
  idea once. No em-dash chaining. No analogies for what is in front of us.
- Lead with the answer; end with the required action or next step.
- Reference codes for 3+ items: `F` findings, `D` decisions, `O` options, `R` risks,
  `Q` questions, `A` actions (`F1`, `D2`, ...). Keep codes stable across the
  conversation; follow-ups like "keep D1, reject O2" are valid.
- Hard boundaries: requested scope only; no unasked refactors, cleanup, or speculative
  abstractions; no completion claims without evidence; never add a co-author to
  commits.
- Aliases (expand only as exact standalone tokens): `scr` = simplify, compress, and
  repeat the response; `eli` = explain like I'm 18, simpler and shorter; `foc` = boil
  down to the one thing that matters; `ref` = rewrite with reference points.

## The ASD-STE100 rule

ASD-STE100 is a real writing standard from the 1980s aviation industry. Aircraft
maintenance manuals are written in it so that mechanics — often non-native English
speakers — cannot misread an instruction.

When a skill or reply calls for ASD-STE100-style English (for example **eli5** or
**wait-what**), apply its rules:

- limited, approved vocabulary;
- active voice;
- short sentences;
- one idea per sentence;
- no metaphors or figures of speech.

## Technical knowledge

The technical knowledge base for all agents lives at `/opt/tkv-local`. At the start of
every assignment, the assigned agent must survey the material relevant to its task
there using the **be-great** skill (evidence-first investigation) before acting.

Its contents are reference material, not current truth: verify versions, state, and
applicability against the live environment before converting them into configuration,
and label them per the truth-state rules.

## Documentation conventions

- Use workflow diagrams (process flow, dataflow) in documentation where they make a
  process or relationship materially easier for a human to read. Default format:
  Mermaid in Markdown, rendered in the HTML output.
- Major documents — specs, designs, READMEs, and other human-facing decision or
  reference documents — are delivered in both `.md` (agent-readable source of truth)
  and a matching `.html` (human-facing rendering). Not every document: logs, notes,
  and routine records stay Markdown-only.
- Dual-format implemented 2026-08-25 (owner ratified Q2): `scripts/wiki/render.py`
  (stdlib-only, deterministic) renders every document in `scripts/wiki/manifest.txt`
  to a sibling `.html` — semantic, self-contained, HX-Wiki-ready; `--check` verifies
  hash synchronization. Markdown stays the source of truth; never hand-edit HTML.

## Adoption of provided documents

Documents supplied for adoption are inputs to review, not gospel. Before a provided
document becomes part of this repository's operating material:

- verify its claims against current evidence and ratified authority;
- reconcile conflicts instead of blending them;
- bring it up to our standards: truth-state labels, naming, the communication
  contract, and the documentation conventions above;
- record provenance and the corrections made.

Quality applies to inputs and outputs alike. Historical evidence records (for example
as-found discovery files) keep their provenance and are corrected openly per the
server records contract, never silently rewritten.

## Approval discipline

The factory's goal is automation. At every gate, ask: are the ratified rules,
process, and audit trail in place for this step? If yes, proceed — approval is
pre-granted. Halt and escalate only when a step has potential for serious harm to
the codebase or the infrastructure, or could bring work to a halt or cause serious
system downtime. Destructive or irreversible actions, governance changes, new
external shared state, and scope expansion count as serious-harm potential. When in
doubt, act reversibly and report rather than pause.

## Infrastructure posture directives

- Secure Boot stays disabled on HX hosts, now and always — do not enable it
  (owner directive, 2026-08-24). Confirmed by owner 2026-08-25: the directive
  stands as written. Proposals to convert it to a scoped risk acceptance (or any
  softening) are rejected; do not escalate them again.
- **No host firewalls (ufw or equivalent) on HX hosts** (owner rule, 2026-08-26).
  The exposure boundary is the private LAN (192.168.50.0/24) itself: services
  bind to the LAN interface as authorized; reachability is governed by the
  network, not by host firewall rulesets. Any prior ufw design or enablement is
  void.
- LLM server deployments follow the blueprint: `servers/BLUEPRINT-llm-server.md`
  (hxs-1 proven; hxs-2 at its M8). It includes the downstream-consumer contract
  that shapes how other ecosystem components are configured at deployment —
  retrieve it before designing anything that consumes an HX LLM endpoint
  (owner standing instruction, 2026-08-26).
- **No Docker/containers for HX deployments** unless the owner explicitly
  authorizes otherwise (owner rule, 2026-08-27) — native services on systemd
  are the deployment shape.
- **Local-model-first rule** (owner, 2026-08-27). At every task or work order the
  first questions are mandatory: (1) can this be accomplished with a local LLM —
  allowed answers: yes (name the backend), not model-required (deterministic
  work), or no (capability gap, documented and escalated to the owner — never
  cloud, never silently absorbed); (2) which local backend fits the work class —
  Qwen-X deep reasoning/synthesis, Coder-X coding/source analysis, Meta-X
  tooling/structured contracts, Chat-X basic utility — with call-sign, endpoint,
  alias, identity, and role recorded per task. Controls: on backend failure the
  session STOPS the affected branch and escalates to the governor —
  re-assignment control stays with the governor, no automatic substitution; the
  verifying backend is always a different host than the producing backend when
  one is available, deterministic checks first regardless. The rule governs
  model-inference work products.

  **How this rule relates to the assigned cloud lanes below.** The prohibition
  is on *unapproved* cloud use: a session may never substitute a cloud backend
  for its assigned lane, and a capability gap is escalated to the owner rather
  than resolved by reaching for a cloud model. It is NOT a prohibition on the
  lanes the owner has already ratified. The metered and zero-cost cloud lanes in
  the job-family table below are the **owner-approved exception of record**
  (OD-14, KDD-0013), assigned per agent by owner decision and bounded by the
  USD 100 cap and the owner-lane allowlist. Answering question (1) with "yes"
  means the assigned lane — local or the allowlisted cloud lane — not a lane of
  the session's choosing. Anything outside the allowlist stays prohibited
  without exception. (A substrate exception for the meta-agent's own
  orchestration was retracted 2026-08-28 and is void — see the moonshot rule
  below.)
- **No agent runs on moonshot-ai** (owner directive 2026-08-28: "i dont want any
  sub-agents running through moonshot-ai… no expections"). The only
  moonshot-bound lane was ever the Kimi-K3 identity, and that lane is retired
  (2026-08-29), so **no moonshot execution path remains** — including for the
  governor, who runs on DeepSeek V4 Flash via OmniRoute. Every agent's work
  sessions run on that agent's assigned job-family lane below, launched as
  standalone `kimi` sessions bound at launch
  (`kimi -m omniroute/<lane> --agent-file agents/<name>/profile.md`) or as dsh
  sessions on hxs-15 for harness-side work. Product fact of record: Kimi Code
  sub-agents always inherit the main session's model (agent files carry no model
  field), so Agent-tool dispatch is not an execution path for agent work — a
  bound standalone session is. History: this directive retracted an earlier
  substrate exception; both are preserved in Git and KDD-0013.
- **Model lanes by job family** (owner decision 2026-08-30; KDD-0013 Amendments
  11–12). Lane defaults are assigned per JOB FAMILY. Per-agent overrides within a
  family are supported and recorded in KDD-0013. Cloud lanes route via OmniRoute
  on hxs-8.

  | Job family | Members | Default lane | Model / provider |
  | --- | --- | --- | --- |
  | Governor (above all families) | James | DeepSeek V4 Flash | via OmniRoute — pinned |
  | PMO | Mia, Carol | GPT-OSS 120B | `openai/gpt-oss-120b`, AkashML |
  | QA | Bailey, Gordon | Qwen3.8 Flash | `qwen/qwen3.8-flash`, Alibaba Cloud International |
  | Agentic SWE | Rob | Coder-X — **local** | `ollama-local/hx-qwen3.6-coderx-64k`, hxs-2 |
  | Infra / Ops | Rick | Coder-X — **local** | `ollama-local/hx-qwen3.6-coderx-64k`, hxs-2 |
  | Platform Systems | Trinity, Morpheus, John, Chris, Wayne, Quinn, Raphael, Erwin (pending registration) | Z.ai GLM 5.2 **free** | `z-ai/glm-5.2:free`, Decart |

  **OD-14 OpenRouter exception of record** — USD 100 cap, owner-lane allowlist:

  - **Metered — 5 lanes:** James, Mia, Carol, Gordon, Bailey. Bailey's lane is
    activation-gated (KDD-0019, KDD-0013 Amendment 12): no metered spend before
    her activation gate clears.
  - **Zero-cost cloud — 8 lanes:** the Platform Systems family on
    `z-ai/glm-5.2:free`. On the allowlist, no metered spend.
  - **Local — 2 lanes, outside OD-14:** Rob and Rick on Coder-X (hxs-2).
  - Cloud substitution outside this allowlist stays prohibited. New agents
    receive a lane at registration.

  **Kimi-K3 is retired as a live lane** (owner directive 2026-08-29,
  "kimi-k3 that model is out of here"). The identity is preserved in KDD-0013 as
  the historical governor-role template only.

  Provenance: the table above is the current state, stated once. The full
  supersession history — the original 2026-08-28 per-agent assignments, the
  governor transitions (kimi-k3 → GLM 5.2 → DeepSeek V4 Flash), and every
  intermediate lane change — is preserved in
  `governace/decisions/KDD-0013-agent-model-lanes.md` (Amendments 1–12), which is
  append-only. Flattened here 2026-08-30 per audit item F2/A1: a current-state
  document presents one current instruction, and Git preserves the rest.
- **Chief of Staff** (owner directive 2026-08-28, KDD-0012). **Mia**
  (`agents/mia/`) manages the work — planning, coordination, distribution to the
  engineering lanes, breakage triage, and status reporting to the governor. The
  Governor governs (goals, gates, acceptance, owner escalation); Mia manages.
  Broken items go to Mia first: characterize, then coordinate or distribute with
  evidence. She never mutates an engineering lane and never issues repair
  dispositions; repairs execute only under a **governor-issued work order**.
  **Distribution and assignments execute only under a governor-issued work
  order** — this rule grants Mia coordination and triage, NOT independent
  self-dispatch authority (consistent with `agents/mia/charter.md` and
  `agents/mia/profile.md`). History: the rule was written when Kimi-K3 held the
  governor role and originally permitted "repair in-lane"; both are superseded
  and preserved in Git and KDD-0012.

## Documentation governance and knowledge stewardship

Owner amendment, 2026-08-25. **Carol** (`agents/carol/`) is the factory's
documentation and knowledge steward — a **bounded persistent role** (owner-registered
2026-08-25): knowledge-only, writes scoped to `knowledge/catalog/`, no sub-agent
dispatch, no host probes; persistent through her catalog, session-based execution.
The catalog is the start of
a second brain for the whole HX team, humans and agents (owner, 2026-08-25).

- Every supplied or produced document gets a recorded disposition in the catalog —
  none is treated as an unstructured attachment, silently ignored, or left
  uncataloged.
- Originals are preserved unchanged; the catalog describes and connects. Provenance
  to source document and section is mandatory; conflicts are preserved,
  authority-ranked, and escalated — never guess-resolved. No secret values in the
  catalog (existence, owner, retrieval mechanism only).
- Kimi-K3 consults the catalog before assigning work and cites consulted records in
  context packets. Agents return new reusable facts and artifacts after execution.
- **Handoff closure is two-stage** (owner directive 2026-08-30; KDD-0024).
  **`execution_accepted`** — evidence produced and the deterministic gates passed.
  The work is done: the acceptance row is written, goal status updates, and the
  next work order may dispatch. **`catalog_pending` / `catalog_complete`** — the
  knowledge projection, tracked separately and never gating. Carol's receipt is
  still required; waiting on it is not, because non-critical-path work must never
  block critical path and Carol is background-class (KDD-0013 Amendment 5).
  SYNCHRONOUS EXCEPTION: a change to authority, security, schemas, agent
  identities, or reusable platform knowledge takes the receipt before closure.
  Where the class is unclear, treat it as synchronous. Everything else batches at
  merge or the scheduled consolidation window.
  History: this rule replaced the 2026-08-25 "a material handoff is incomplete
  without Carol's catalog receipt" line on 2026-08-30; both are preserved in Git
  and in KDD-0024.
- Governing principle: retrieve before investigating; reuse before recomputing;
  verify before trusting; catalog before closing — cataloguing routine work does
  not block closing it.

## Second Brain roadmap integration (standing directive)

Owner directive, 2026-08-25. The HX Second Brain Roadmap is an active consideration
in all planning and implementation workflows. Whenever a feature, server, service,
agent, model, tool, or solution is introduced or materially changed, evaluating
whether the work is a justified opportunity to advance the Second Brain
architecture is **mandatory**; implementation is **not automatic**. Any proposed
Second Brain capability must align with the active goal and approved architecture,
provide clear measurable value, fit the current maturity and sequence, avoid scope
expansion and premature complexity, preserve authority/security/provenance
boundaries, and be presented for approval when it exceeds the work order's
authority.

Every material implementation handoff must state: (1) whether a Second Brain
opportunity was identified; (2) which roadmap capability or pattern applies;
(3) whether it was implemented, recommended for a future iteration, or deliberately
deferred; (4) the evidence and reasoning for the disposition.

Governing question for every material change: **does this work create a justified
opportunity to advance the HX Second Brain while delivering the current goal?**

## Agent family taxonomy and standard template (KDD-0016, 2026-08-29)

All HX agents belong to one of four families. The governor sits above all
families. New agents are created within a family only when the platform
needs them. The standard profile and charter templates at
`agents/_template/` are mandatory for all agents.

| Group | Family | Responsibility | Current agents |
|---|---|---|---|
| 1 | Agentic Software Engineering | Build and test products, features, APIs, interfaces, schemas, integrations | rob (gated) |
| 2 | AI Infrastructure and Operations Engineering | Maintain the underlying computing environment | rick |
| 3 | AI Platform Systems Engineering | Install, configure, operate, upgrade, recover platform services | morpheus (DSH), gordon (QA), trinity (OmniRoute), john (Ollama), chris (PostgreSQL), wayne (Redis), quinn (Qdrant), raphael (LightRAG) |
| 4 | AI-PMO | Portfolio, project, research, documentation, human-facing reporting | mia, carol |

**QA lane-config placement (cross-family note, KDD-0019):** Bailey belongs to the
QA lane-config job family (KDD-0013 Amendment 11), which is not a KDD-0016
taxonomy family — so she has no taxonomy-table row. Gordon is the **explicit
exception**: although he also maps under the QA lane-config family as the
execution/qualification lane, he additionally keeps his Family 3 Platform
Systems taxonomy row (qualification role) — that row is his, and it does not
imply Bailey has a row. Bailey is the horizontal test-authoring QA lane and is
mapped with Gordon under the QA lane-config family only. Per-agent lane
assignments (including the QA Qwen3.8 Flash default) live in KDD-0013.

**Governor:** above all families. Governs (goals, gates, acceptance, owner
escalation); does not belong to any family.

**Standard template:** every `agents/<name>/profile.md` and
`agents/<name>/charter.md` must follow the templates in
`agents/_template/`. See KDD-0016 for the full specification, mandatory
sections, normalization rules, and the standard identity table fields.

## System-to-server mapping (2026-08-29)

The authoritative mapping of systems to servers lives at
`servers/system-mapping.md`. It records which system runs on which host,
the MCP co-location architecture, placement principles, and the agent
assignments for each system. `servers/SERVER-REGISTRY.md` owns durable host
identity and role; `servers/system-mapping.md` owns system placement.
Both documents must stay reconciled — changes to one require a labeled
correction in the other.

## Governor role

The governor role is held by **James**, running on **DeepSeek V4 Flash** via
OmniRoute (KDD-0013 Amendment 11, owner decision 2026-08-30 — the lane is
pinned). The governor governs: goals, gates, acceptance, and owner escalation.
It sits above all four agent families and belongs to none of them.

History, preserved in Git and in `governace/decisions/KDD-0013-agent-model-lanes.md`
(append-only): the role passed from **Kimi-K3** to **Flash** (owner appointment
2026-08-29, recorded at the time as intent-level pending owner confirmation in
records), and the persona was renamed **Flash → James** on 2026-08-30. The
pending qualifier is satisfied by KDD-0013 Amendment 11, an owner decision of
record that names James as Governor with a pinned lane. "DeepSeek V4 Flash" is a
third-party model id, not the persona name.

Flattened 2026-08-30 per audit item F2/A1.
