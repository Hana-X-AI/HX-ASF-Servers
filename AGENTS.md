# AGENTS.md

## Skills and trigger words

Ten owner-installed skills govern how work is done in this repository. They live in
`.kimi-code/skills/` (project scope) and also at user scope in `~/.kimi-code/skills/`.

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

When the owner uses a trigger word, invoke the matching skill first and follow its
workflow in full — do not partially apply it. Project agents and sub-agents working in
this repository must honor these skills as well.

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
