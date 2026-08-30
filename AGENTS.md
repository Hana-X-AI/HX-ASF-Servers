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

[OPEN CORRECTION 2026-08-30, labeled, append-only — SKILL INVENTORY GROWTH 14 → 23:
the inventory above grew from fourteen (14) to twenty-three (23) skills. The nine (9)
additions are: **grill-me**, **ai-test-generation**, **test-planning**,
**test-strategy**, **qa-project-context**, **test-environments**, **release-readiness**,
**test-reliability**, and **ci-cd-integration** — the base fourteen (be-great through
work-status) are preserved in the inventory above. Authority: owner directive
2026-08-30 (grill-me limited to 5 questions) and owner ratification of the QA skill
subset (KDD-0019); effective 2026-08-30. The prior fourteen-skill state is preserved as
history above; the current inventory is authoritative.]

[OPEN CORRECTION 2026-08-30, labeled, append-only — SKILL INVENTORY GROWTH
23 → 30 AND CANONICAL LOCATION CHANGE: (a) COUNT — the inventory above grew from
twenty-three (23) to thirty (30) skills. The seven (7) additions are:
**handoff**, **writing-for-agents**, **triage**, **diagnosing-bugs**,
**grill-with-docs**, **grilling**, and **domain-modeling** — the base
twenty-three (be-great through ci-cd-integration) are preserved in the inventory
above. (b) LOCATION — the canonical skill tree moved from `.kimi-code/skills/` to
`.agents/skills/`; `.kimi-code/skills/` and `.claude/skills/` are now GENERATED
mirrors rebuilt by `scripts/skills_sync.py --write` and enforced by `validate.py`
SY-3. The prior location wording is superseded in the section opening above and
preserved in this correction. `archify` is canonical-only, with a pointer stub in
each mirror; it is a Node CLI invoked by path, not a prompt skill.
(c) PRECEDENCE — `grill-me` remains the ONLY factory scope-lock gate. `grilling`
and `grill-with-docs` never satisfy that gate, and the owner's 5-question limit
(directive 2026-08-30) applies to every interview path in this repository, not
only to `grill-me`; upstream's unbounded "relentless" form was corrected at
intake rather than adopted. (d) PROVENANCE — the seven additions come from
`mattpocock/skills` at upstream commit
`6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` (MIT, Copyright (c) 2026 Matt Pocock),
recorded with per-skill correction notes in each SKILL.md and pinned in
`skills-lock.json`. Authority: KDD-0020; effective 2026-08-30. The prior
twenty-three-skill state and its location are preserved as history above; the
current inventory is authoritative.]

Default reporting voice: **corporate** (executive-summary tone). A voice trigger
overrides the default for that reply; when style skills conflict, the owner's most
recent explicit trigger wins.

## Communication contract

Always on, distilled from the **be-smart** skill (say "be smart" to load the full
contract with examples).

- Banned phrases: "load-bearing", "worth stating plainly", "here's the honest truth",
  "the real tension", "carry the argument".
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
  session STOPS the affected branch and escalates to the meta-agent —
  re-assignment control stays with KK3, no automatic substitution, cloud
  substitution always prohibited; the verifying backend is always a different
  host than the producing backend when one is available, deterministic checks
  first regardless. Exception: KK3's own orchestration and governance runs on
  the meta-agent model; subagent session substrates are orchestration
  mechanics, not "the LLM for the work" — the rule governs model-inference
  work products.
- **Substrate exception RETRACTED** (owner directive 2026-08-28, labeled
  correction — the exception sentence inside the rule above is VOID from this
  date, original preserved there as history): "i dont want any sub-agents
  running through moonshot-ai.. the only agent to run throug moonshot-ai is
  you… no expections." Only Kimi-K3 runs on `moonshot-ai/kimi-k3`. Every other
  agent's work sessions run on that agent's assigned model lane (KDD-0013),
  executed as standalone `kimi` sessions bound at launch
  (`kimi -m omniroute/<lane> --agent-file agents/<name>/profile.md`) or as dsh
  sessions on hxs-15 for harness-side work. Product fact of record: Kimi Code
  sub-agents always inherit the main session's model (agent files have no
  model field), so Agent-tool dispatches from the governor's moonshot session
  are NO LONGER an execution path for agent work — the governor's own bounded
  direct execution (KK3 itself) remains moonshot-legal.
- **Per-agent model lanes** (owner-assigned 2026-08-28, KDD-0013; all local/GLM
  lanes route via OmniRoute on hxs-8): kimi-k3 `moonshot-ai/kimi-k3` (meta-agent
  exception) · morpheus Coder-X (hxs-2) · gordon Qwen-X (hxs-1) · rick Meta-X
  (hxs-3) · john Meta-X (hxs-3) · carol Chat-X (hxs-4) · trinity GLM 5.3 Flash ·
  rob GLM 5.3 Flash · mia GLM 5.3 Flash. [Correction 2026-08-28, labeled:
  gordon's lane is now DeepSeek V4 Pro (`openrouter/deepseek/deepseek-v4-pro-0813`,
  provider StreamLake, via OmniRoute) — owner directive same day, superseding
  the Qwen-X assignment printed above, which is preserved as history.]
  [Correction 2026-08-28, labeled: carol's lane is now OpenAI gpt-oss-120b
  (`openrouter/openai/gpt-oss-120b`, provider AkashML, via OmniRoute) — owner
  directive same day, superseding the Chat-X assignment printed above; she
  remains frozen.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only: Carol is UNFROZEN to
  background-class status (owner plan GO, state-log row 31) — she runs catalog
  catch-up batches on her lane without blocking any gate, handoff, or lane;
  the frozen wording above and in the Carol section below is preserved as
  history. Authority: state-log row 31; owner: "run carol but not on the
  critical path… does not block any work."] The three
  GLM lanes plus gordon's DeepSeek lane ride the OD-14
  OpenRouter exception of record (USD 100 cap, owner-lane allowlist, metered);
  cloud substitution otherwise stays prohibited. New agents receive a lane at
  registration.
  [OPEN CORRECTION 2026-08-29, labeled, append-only: the GOVERNOR's lane is now
  Z.ai GLM 5.2 (`openrouter/z-ai/glm-5.2`, provider Decart, via OmniRoute) —
  owner directive same day, superseding the `moonshot-ai/kimi-k3` meta-agent
  exception printed above, which is preserved as history. The
  substrate-retraction rule (no moonshot sub-agents) stands unchanged. OD-14
  scope: SEVEN cloud lanes — trinity, rob, mia, gordon, carol, chris, kimi-k3.
  Authority: KDD-0013 Amendment 7.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only: the OD-14 owner-lane
  allowlist and metering scope now covers all five cloud lanes: Trinity, Rob,
  Mia, Gordon, and Carol. Authority: KDD-0013 Amendment 4 and
  `pilots/PILOT-DSH-IMPL-001/01-state-log.md` row 30. The preceding four-lane
  scope remains preserved as historical text.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only: the scope now covers SIX
  cloud lanes — chris is registered (KDD-0014) with lane Qwen 3.8 Flash
  (`openrouter/qwen/qwen3.8-flash`, provider Alibaba Cloud International, via
  OmniRoute). Authority: KDD-0013 Amendment 6. The preceding five-lane note
  remains preserved as historical text.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only: the GOVERNOR ROLE is now
  held by **Flash** (owner/Agent Zero appointment, 2026-08-29), running on
  **DeepSeek V4 Flash** via OmniRoute — superseding the GLM 5.2 governor lane
  of Amendment 7 (preserved as history). Governing references to "Kimi-K3" as
  the governor (Chief of Staff reporting line, Checkpoint routing, state-log
  triage fields) read as the GOVERNOR role — currently Flash — not the
  kimi-k3 identity. Authority: owner appointment reported by Flash
  (work order 14, `pilots/PILOT-DSH-IMPL-001/`); RECORD OF THE APPOINTMENT IS
  INTENT-LEVEL PENDING PRIMARY OWNER CONFIRMATION IN RECORDS.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only (review batch 2, F1):
  morpheus's lane is now **Qwen 3.8 2.4T A95B** (`openrouter/qwen/qwen3.8-2.4t-a95b`,
  provider DeepInfra, via OmniRoute hxs-8) — owner directive 2026-08-29,
  superseding the Coder-X assignment printed above (preserved as history).
  Reason: two consecutive Coder-X failures on the Phase C prep order
  (state-log rows 34/40); recorded in the Morpheus profile amendment and
  `agents/README.md`.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only (review batch 2, F2):
  the substrate-retraction paragraph above describes the governor's bounded
  direct execution as "(KK3 itself)". The GOVERNOR ROLE is now held by Flash
  (see the governor correction above) — the moonshot-legal direct-execution
  clause reads as the GOVERNOR ROLE, and the current governor runs on
  DeepSeek V4 Flash via OmniRoute, not moonshot-ai. Kimi-K3 remains an
  identity-specific model lane on `moonshot-ai/kimi-k3` per KDD-0013.
  Original clause preserved above as history.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only (review batch 2, F3):
  the OD-14 OpenRouter exception scope is now **EIGHT** metered cloud lanes —
  trinity, rob, mia, gordon, carol, chris, kimi-k3, **wayne** (KDD-0015,
  registered 2026-08-29, lane `openrouter/openai/gpt-oss-120b`) — superseding
  the seven-lane scope of Amendment 7 (preserved as history) and matching
  `agents/README.md`. Authority: KDD-0015 + owner registration 2026-08-29.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only (review batch 2, F6):
  chris's lane is now **DeepSeek V4 Pro** (`openrouter/deepseek/deepseek-v4-pro`,
  provider Baidu FP8, via OmniRoute hxs-8) — owner directive 2026-08-29,
  superseding the Qwen 3.8 Flash lane of the six-lane note above (preserved
  as history). Authority: KDD-0014 open correction, same date.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only (CodeRabbit review batch):
  within the OD-14 allowlist above, the `moonshot-ai/kimi-k3` provider lane is
  SUPERSEDED as an authoritative provider lane — the governor role runs on
  GLM 5.2, then Flash/DeepSeek V4 Flash, via OmniRoute per the correction
  blocks above. Kimi-K3 remains a registered identity-specific lane reference
  but moonshot-ai is not the operative provider for the governor. Original
  allowlist text preserved above as history.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only: quinn is registered
  (KDD-0017) with lane NVIDIA Nemotron 3 Ultra
  (`openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`, provider NVIDIA, via
  OmniRoute hxs-8) — owner-assigned 2026-08-29, CLI-verified live. Quinn's
  lane is free-tier on OpenRouter (no metered spend); it rides the OD-14
  exception unmetered as a zero-cost cloud lane. OD-14 scope: NINE cloud
  lanes — trinity, rob, mia, gordon, carol, chris, kimi-k3, wayne, quinn
  (quinn unmetered). Authority: KDD-0017.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only: raphael is registered
  (KDD-0018) with lane Qwen-X (`ollama-local/hx-qwen3.8-27b-64k`, hxs-1,
  via OmniRoute hxs-8) — owner-assigned 2026-08-29. Qwen-X is a local
  lane (no OD-14 cloud metering). OD-14 scope unchanged (nine cloud lanes;
  raphael is local). Authority: KDD-0018.]
  [OPEN CORRECTION 2026-08-30, labeled, append-only — JOB-FAMILY LANE DEFAULTS
  (owner decision, multi-agent alignment session; KDD-0013 Amendment 11): lane
  defaults are now per JOB FAMILY. This supersedes the per-agent lanes above for
  the affected agents (prior lanes preserved as history): Rob (Agentic SWE) →
  Coder-X (hxs-2, local) · Rick (Infra/Ops) → Coder-X (hxs-2, local) · Platform
  Systems (Trinity, Morpheus, John, Chris, Wayne, Quinn, Raphael, Erwin +
  future SE) → Z.ai GLM 5.2 free (`z-ai/glm-5.2:free`, Decart), replacing their
  prior per-agent lanes. Governor (James) → DeepSeek V4 Flash (pinned); PMO
  (Mia, Carol) → GPT-OSS 120B; QA (Bailey, Gordon) → Qwen3.8 Flash. Per-agent
  overrides within a family remain supported. Authority: owner decision
  2026-08-30; KDD-0013 Amendment 11.] [Note: "Governor (James)" reads as the
  GOVERNOR ROLE — the persona renamed from Flash to James (governor-rename
  correction below, 2026-08-30); the model lane DeepSeek V4 Flash is unchanged.]
  [OPEN CORRECTION 2026-08-30, labeled, append-only — BAILEY QA LANE ON OD-14
  ALLOWLIST: Bailey's QA-family lane Qwen3.8 Flash
  (`openrouter/qwen/qwen3.8-flash`, provider Alibaba Cloud International, via
  OmniRoute hxs-8) is included in the OD-14 owner-lane allowlist and metering
  scope. OD-14 scope is now TEN cloud lanes — trinity, rob, mia, gordon,
  carol, chris, kimi-k3, wayne, quinn (unmetered), bailey (metered) —
  superseding the nine-lane scope above for Bailey (preserved as history).
  Activation-gated: not exercised until Bailey's activation gate clears
  (KDD-0019); no metered spend before activation. Authority: owner decision
  2026-08-30 (KDD-0013 Amendment 11) + KDD-0019; KDD-0013 Amendment 12.]
- **Chief of Staff** (owner directive 2026-08-28, KDD-0012). **Mia**
  (`agents/mia/`) manages the work — planning, coordination, distribution to the
  engineering lanes, breakage triage, and status reporting to Kimi-K3. The
  Governor governs (goals, gates, acceptance, owner escalation); Mia manages.
  Broken items go to Mia first: characterize, then coordinate or distribute
  with evidence — she never mutates an engineering lane or issues repair
  dispositions; repairs execute only under a Kimi-K3-issued work order.
  [Corrected 2026-08-28, labeled: previously "characterize, repair in-lane, or
  distribute with evidence" — overreach vs her management-only mandate;
  original preserved here.] **Distribution and assignments execute only under a
  Kimi-K3-issued work order** — this rule grants Mia coordination and triage,
  NOT independent self-dispatch authority (consistent with
  `agents/mia/charter.md` and `agents/mia/profile.md`).
  [OPEN CORRECTION 2026-08-29, labeled, append-only (review batch 2, F4):
  the issuer phrase "Kimi-K3-issued work order" in this rule reads as the
  GOVERNOR-issued work order — the governor role is currently held by Flash
  (see the governor correction above), under whose authority Kimi-K3's
  original issuing rule was established. The Kimi-K3 wording is preserved
  as history.]
  [OPEN CORRECTION 2026-08-29, labeled, append-only (review batch 2, F5):
  the governor-transition correction above records the Flash appointment as
  "INTENT-LEVEL PENDING PRIMARY OWNER CONFIRMATION IN RECORDS" — that
  qualifier stands: the appointment is not presented as owner-confirmed.
  This entry changes no status; the pending qualifier remains the operative
  record until the owner confirms in records.]

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
- A material handoff is **incomplete without Carol's catalog receipt**, referenced
  in the governing log.
- Governing principle: retrieve before investigating; reuse before recomputing;
  verify before trusting; catalog before closing.

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

## Governor rename (labeled correction, 2026-08-30)

[OPEN CORRECTION 2026-08-30, labeled, append-only — GOVERNOR PERSONA RENAMED
FROM FLASH TO JAMES: the governor role is now referred to as **James**
(owner decision 2026-08-30), superseding the "Flash" persona name for the
governor role. The governor still runs on **DeepSeek V4 Flash** via OmniRoute
(model lane unchanged — the model name is a factual third-party id, not the
persona). All historical references to "Flash" as the governor persona in the
correction blocks above are preserved as history and read as the governor
role — currently James. Kimi-K3 references remain preserved as earlier
governor-role history. Authority: owner decision 2026-08-30; recorded
append-only; no governance scope change.]
