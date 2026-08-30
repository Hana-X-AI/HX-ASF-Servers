# Agents

Specialist agents work in lanes. This directory holds one lane per agent:
`agents/<agent-name>/`, starting from `_template/charter.md`.

## The roster

`agents/` is the agent roster. Before treating any referenced agent, profile, or
persona as a current teammate, check this directory first: the charters here are
the authority on who exists and what they can do. Profiles found in the knowledge
vault (`/opt/tkv-local`) are reference material only and may be stale or
superseded. Precedence when sources disagree: the roster and charters in this
directory outrank any vault profile; within an agent's lane, the charter defines
existence and scope, and its linked `profile.md` is the operating contract.
(Precedence rule made explicit 2026-08-25.)

Current roster:

| Agent | Lane | Status | Capabilities |
| --- | --- | --- | --- |
| james | horizontal (control plane) | active — governor (owner appointment 2026-08-29; DeepSeek V4 Flash via OmniRoute) | Governor role: goals, gates, acceptance, owner escalation; directs work through Mia; mandatory verification-checklist; intent+constraints work orders; never the operational worker |
| kimi-k3 | horizontal (control plane) | **RETIRED as live governor lane 2026-08-29** (owner directive "kimi-k3 that model is out of here"); preserved as historical governor-role template | Goal decomposition, agent commissioning, evidence gates, recovery, escalation — the historical operating contract James's profile adapts; verification-checklist remains the standing governor gate |
| john | vertical | active | Ollama install/config/audit/troubleshoot on Linux, test-first, evidence packages |
| rick | vertical | active | Ubuntu Server OS plane: packages, systemd, Netplan, SSH/sudo, firewall, storage, kernel/drivers, backup/recovery |
| carol | horizontal (documentation) | active — bounded persistent role (owner-registered 2026-08-25) | Knowledge stewardship: catalog at `knowledge/catalog/`, classification, relationships, retrieval packages, freshness, catalog receipts completing handoffs |
| trinity | vertical | active — owner-ratified 2026-08-27 (KDD-0008, O1 adopt-as-corrected) | OmniRoute lifecycle engineering: source review, install/config design, provider/protocol conformance design, lifecycle evidence — under governor (James) work orders |
| morpheus | vertical | active — owner-directed 2026-08-28 (KDD-0009) | DeepSeek Harness lifecycle: pinned install/build/configuration, effective-config receipts, operations, upgrades/rollbacks on hxs-15 — under governor (James) work orders; never self-certifies |
| gordon | horizontal (quality) | active — owner-directed 2026-08-28 (KDD-0010) | Independent dsh qualification and regression: gate program (Gates 0–10), Feature Coverage Ledger, evidence-backed verdicts; executes + installs test tooling on hxs-15, changes no configuration, never repairs |
| rob | vertical (application layer) | registered 2026-08-28 (KDD-0011) — **activation gated** (Gordon Gate 7 PASS + Gate 10 entry conditions met + named work order + owner word) | Full-stack agentic software engineering through DeepSeek Harness: small reversible diffs, tests with code, durable dsh sessions, receipts — never platform work, never self-verification |
| mia | horizontal (control-plane staff) | active — owner-directed 2026-08-28 (KDD-0012) | Chief of Staff to the Governor: planning, coordination, work management, breakage triage and distribution to the engineering lanes, status reporting to the governor (James); management only — never gates, acceptance, or verdicts |
| chris | vertical (database systems) | registered 2026-08-29 (KDD-0014) — **activation gated** (hxs-9 PostgreSQL implemented + credential entries + owner word) | PostgreSQL systems engineer: single-instance administration, least-required roles/service accounts, pg_dump/pg_restore with validation, basic performance, schema under owner approval; MCP on HOLD (owner 2026-08-29) |
| wayne | vertical (cache/data systems) | registered 2026-08-29 (KDD-0015) — **activation gated** (hxs-9 Redis implemented + credential entries + owner word) | Redis systems engineer: single-instance administration, ACL users, persistence, health, PostgreSQL cache integration contract (Redis side); standalone topology only; MCP on HOLD; RAG/vector/stream deferred (owner 2026-08-29) |
| quinn | vertical (vector database systems) | registered 2026-08-29 (KDD-0017) — **activation gated** (hxs-4 Qdrant implemented + credential entries + owner word) | Qdrant server + Python client + MCP server (co-located) on hxs-4; lane NVIDIA Nemotron 3 Ultra (free) via OpenRouter; standalone topology only |
| raphael | vertical (RAG systems) | registered 2026-08-29 (KDD-0018) — **activation gated** (hxs-4 LightRAG implemented + bge-m3 on hxs-4 + credential entries + owner word) | LightRAG server + Web UI + lightragmcp MCP server on hxs-4; lane Qwen-X via OmniRoute; Qdrant backend (Quinn); LLM via OmniRoute (Meta-X); bge-m3 embeddings via Ollama (john) |
| bailey | horizontal (quality — test authoring) | registered 2026-08-30 (KDD-0019) — **activation gated** (implemented testing-role usage + credential entries + owner word) | Sr. AI Testing Engineer: test plans + test scripts + pinned stacks per project under `governace/qa/` (python/pytest, zod); stack-agnostic; QA job family with Gordon; lane Qwen3.8 Flash via OmniRoute |

### New agents pending registration (per system-mapping 2026-08-29)

| Agent | Family | System | Server | Notes |
|---|---|---|---|---|
| sage | 3 (Platform Systems) | FastMCP | hxs-20 | MCP gateway — discovery, routing, cloud proxy |
| iris | 3 (Platform Systems) | Open WebUI | hxs-10 | Web frontend |
| scout | 3 (Platform Systems) | Crawl4AI | hxs-6 | Ingestion — crawling |
| piper | 3 (Platform Systems) | Docling | hxs-12 | Ingestion — parsing |
| ripple | 3 (Platform Systems) | n8n | hxs-13 | Automation |
| erwin | 3 (Platform Systems) | LangGraph | hxs-11 | Agent runtime; deferred |
| nexus | 2 (Infra/Ops) | NGINX | hxs-21 | Reverse proxy / web edge |

**System-to-server mapping:** see `servers/system-mapping.md` for the
authoritative mapping of all systems to servers, agent assignments, MCP
co-location architecture, and placement principles.

**Model lanes.** Lane defaults are assigned per JOB FAMILY (owner decision
2026-08-30, KDD-0013 Amendment 11). `AGENTS.md` §"Infrastructure posture
directives" carries the authoritative table; each agent's own profile carries its
assigned lane. Summary:

| Job family | Members | Default lane |
| --- | --- | --- |
| Governor | james | DeepSeek V4 Flash (pinned) |
| PMO | mia, carol | GPT-OSS 120B |
| QA | bailey, gordon | Qwen3.8 Flash (gordon overrides to DeepSeek V4 Pro) |
| Agentic SWE | rob | Coder-X, **local** (hxs-2) |
| Infra / Ops | rick | Coder-X, **local** (hxs-2) |
| Platform Systems | trinity, morpheus, john, chris, wayne, quinn, raphael, erwin (pending registration) | Z.ai GLM 5.2 **free** |

OD-14 OpenRouter exception (USD 100 cap, owner-lane allowlist): **5 metered**
lanes — james, mia, carol, gordon, bailey (bailey activation-gated, KDD-0019);
**8 zero-cost cloud** lanes — the Platform Systems family on `z-ai/glm-5.2:free`;
**2 local** lanes outside OD-14 — rob and rick. kimi-k3 is retired as a live lane
(2026-08-29). Cloud substitution outside the allowlist stays prohibited.

Provenance: the full supersession history — the 2026-08-28 per-agent
assignments, the governor transitions (kimi-k3 → Flash → James), and every
intermediate lane change — is preserved in
`governace/decisions/KDD-0013-agent-model-lanes.md` (append-only). Flattened here
2026-08-30 per audit item F2/A1.

## Two lane types

- **Horizontal** — one domain, across the whole project. Examples: security,
  documentation, testing, validation.
- **Vertical** — one infrastructure or functional lane. Examples: a specific server
  role, storage, networking, GPU/compute.

An agent owns its lane's evidence and drafts. It does not silently rewrite governance,
contracts, or another agent's lane; it escalates to the coordinator (the main Kimi
session) with evidence instead.

## Adding an agent

1. Copy `_template/` to `agents/<kebab-case-name>/`.
2. Fill in the charter. Keep it to one page.
3. Get owner sign-off before the agent does scoped work.

## Manual phase

Agents are currently instructed per session by the coordinator. When the project moves
to executable sub-agents, their definition files will live in `.kimi-code/agents/`
(Kimi Code's scanned location) and link back to these charters. The charter remains
the authority on what the agent owns.

[2026-08-30: the `.kimi-code/agents/` placeholder directory was removed as
non-operational. Re-add it when the phase-transition KDD lands; see
`knowledge/assessments/2026-08-27-second-brain-feature-review.md`.]
