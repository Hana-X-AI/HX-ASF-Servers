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
| kimi-k3 | horizontal (control plane) | active — Phase M | Goal decomposition, agent commissioning, evidence gates, recovery, escalation; bounded direct execution under section 2.3 |
| john | vertical | active | Ollama install/config/audit/troubleshoot on Linux, test-first, evidence packages |
| rick | vertical | active | Ubuntu Server OS plane: packages, systemd, Netplan, SSH/sudo, firewall, storage, kernel/drivers, backup/recovery |
| carol | horizontal (documentation) | active — bounded persistent role (owner-registered 2026-08-25) | Knowledge stewardship: catalog at `knowledge/catalog/`, classification, relationships, retrieval packages, freshness, catalog receipts completing handoffs |
| trinity | vertical | active — owner-ratified 2026-08-27 (KDD-0008, O1 adopt-as-corrected) | OmniRoute lifecycle engineering: source review, install/config design, provider/protocol conformance design, lifecycle evidence — under Kimi-K3 work orders |
| morpheus | vertical | active — owner-directed 2026-08-28 (KDD-0009) | DeepSeek Harness lifecycle: pinned install/build/configuration, effective-config receipts, operations, upgrades/rollbacks on hxs-15 — under Kimi-K3 work orders; never self-certifies |
| gordon | horizontal (quality) | active — owner-directed 2026-08-28 (KDD-0010) | Independent dsh qualification and regression: gate program (Gates 0–10), Feature Coverage Ledger, evidence-backed verdicts; executes + installs test tooling on hxs-15, changes no configuration, never repairs |
| rob | vertical (application layer) | registered 2026-08-28 (KDD-0011) — **activation gated** (Gordon Gate 7 PASS + Gate 10 entry conditions met + named work order + owner word) | Full-stack agentic software engineering through DeepSeek Harness: small reversible diffs, tests with code, durable dsh sessions, receipts — never platform work, never self-verification |
| mia | horizontal (control-plane staff) | active — owner-directed 2026-08-28 (KDD-0012) | Chief of Staff to the Governor: planning, coordination, work management, breakage triage and distribution to the engineering lanes, status reporting to Kimi-K3; management only — never gates, acceptance, or verdicts |

Model lanes (owner-assigned 2026-08-28, KDD-0013): kimi-k3 `moonshot-ai/kimi-k3` (meta-agent exception) · morpheus Coder-X · gordon Qwen-X · rick Meta-X · john Meta-X · carol Chat-X · trinity GLM 5.3 Flash · rob GLM 5.3 Flash · mia GLM 5.3 Flash — all local/GLM lanes route via OmniRoute (hxs-8).

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
