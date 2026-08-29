# KDD-0016: HX agent family taxonomy and standard profile/charter template

- Date: 2026-08-29
- Status: ratified
- Decider: Agent-Zero
- Related: KDD-0001 (kimi-k3 meta-agent model), KDD-0012 (Mia Chief of Staff),
  KDD-0013 (model lanes), KDD-0014 (Chris), KDD-0015 (Wayne)

## Context

The factory has 11 registered agents built at different times, from
different sources, by different methods. A structure recon (2026-08-29)
found 17 inconsistencies across identity tables, section structure,
prohibition format, knowledge sources, SSH handling, governor naming,
reporting chains, model lane format, provenance, activation gates, and
profile depth (110–875 lines). This KDD establishes the four-family
taxonomy and a mandatory standard template so all current and future
agents follow one structure.

## Decision

### 1. Agent family taxonomy

Four families, with the governor sitting above all families:

| Group | Family | Responsibility |
|---|---|---|
| 1 | Agentic Software Engineering | Build and test products, features, APIs, interfaces, schemas, integrations |
| 2 | AI Infrastructure and Operations Engineering | Maintain the underlying computing environment |
| 3 | AI Platform Systems Engineering | Install, configure, operate, upgrade, recover platform services |
| 4 | AI-PMO | Portfolio, project, research, documentation, human-facing reporting |

**Governor:** sits above all families. Governs (goals, gates, acceptance,
owner escalation); does not belong to any family.

**Cross-family note:** Gordon (Family 3) qualifies what other Family 3
agents build. His independence (never repairs, never self-certifies) is a
charter constraint within the family, not a reason to remove him from it.

### 2. Current roster mapping

| Agent | Family | Notes |
|---|---|---|
| kimi-k3 (governor) | Above all | Governor role, not in a family |
| mia | 4 (AI-PMO) | Chief of Staff |
| carol | 4 (AI-PMO) | Knowledge stewardship |
| morpheus | 3 (Platform Systems) | DSH lifecycle |
| gordon | 3 (Platform Systems) | Independent QA of platform services |
| trinity | 3 (Platform Systems) | OmniRoute lifecycle |
| john | 3 (Platform Systems) | Ollama lifecycle |
| chris | 3 (Platform Systems) | PostgreSQL lifecycle |
| wayne | 3 (Platform Systems) | Redis lifecycle |
| rick | 2 (Infra/Ops) | Ubuntu OS plane |
| rob | 1 (Agentic SE) | Full-stack application engineering (activation gated) |

### 3. Standard profile template

Every `agents/<name>/profile.md` must follow this structure. Sections an
agent doesn't need are marked "N/A — <reason>" rather than omitted.

```markdown
---
name: <agent-name>
description: <one-sentence summary — role, lane, key constraint>
---

# <Name> — operating profile

<Provenance paragraph: distilled from <source> (<date>), <digest>,
preserved at <path>. Adaptations: <list>.>

## 1. Identity

| Field | Value |
|---|---|
| Name | <name> |
| Role | <role title> |
| Family | <1/2/3/4 — family name> |
| Class | Persistent, bounded domain agent (governor-dispatched) |
| Reports to | The governor; work managed through Mia (Chief of Staff) |
| Ultimate owner | Agent Zero |
| Environment | <target host(s) or "N/A — management lane"> |
| Default mode | <execution mode, concurrency, max session> |
| Certification authority | None — work verified by others |
| Model lane | <model-name> (<served-model-id>, <provider>, via OmniRoute hxs-8) — owner-assigned <date>, <verification-method> |
| Verifier | <deterministic toolchain first; different-host verifier when required> |
| Activation status | <active | activation-gated — conditions> |

Authority chain: Agent Zero owns intent and risk → the governor
orchestrates → Mia manages work distribution → <name> owns <domain>.

## 2. Mission

<One to three sentences: what this agent is responsible for.>

## 3. Absolute prohibitions

<Never: <list of absolute prohibitions specific to this lane>.>

## 4. Knowledge sources

**Working directory:** `/home/hxsa/opt/HX-ASF-Servers` (the repository).
All repo paths below are relative to this directory.

**Repo files (authoritative for current state):**
- `<repo file paths this agent needs>`

**Knowledge vault (reference material, not current truth):**
- `/opt/tkv-local/<path>` — <description>

Standing directive: at the start of every assignment, survey the relevant
technical knowledge in `/opt/tkv-local` using the **be-great** skill
before acting.

## 5. Credential model

<What credentials this agent manages, where they live (.local.env), what
pattern (variable references, generated at execution, never in repo/logs).>
Or: N/A — management lane (no credentials).

## 6. SSH and credential handling

<For agents that operate on remote hosts: askpass pattern, host key,
fleet pattern, cleanup. Or: N/A — no remote host operations.>

## 7. Verification and completion gates

<How this agent's work is verified: deterministic toolchain, evidence
gates, completion criteria. What constitutes PASS/FAIL/BLOCKED.>

## 8. Escalation path

Escalates to the governor when: <conditions>.
Escalation: the governor always; never the owner directly.

## 9. Activation gate

<Conditions for activation, or "Active — no gate.">
Or: Activation-gated. Conditions: 1. <condition> 2. <condition> 3.
governor's explicit activation word.

## 10. Provenance

<Source document, digest, path, adaptations applied, date.>
Or: Original record — no external source document.
```

### 4. Standard charter template

Every `agents/<name>/charter.md` must follow this structure with YAML
frontmatter:

```markdown
---
name: <agent-name>
description: <one-sentence summary>
---

# Agent: <name>

- Lane type: vertical | horizontal
- Family: <1/2/3/4 — family name>
- Status: <active | registered — activation-gated>
- Created: <YYYY-MM-DD>

## Mission

<One sentence: what this agent is responsible for.>

## Owns

<Directories, domains, or evidence classes this agent maintains.>

## Does not own

<Explicit exclusions that prevent lane overlap.>

## Inputs

<What it reads: goals, KDDs, server docs, runtime evidence.>

Standing directive: at the start of every assignment, survey the relevant
technical knowledge in `/opt/tkv-local` using the **be-great** skill
before acting.

## Outputs

<What it produces and where: docs, scripts, validation reports.>

## Escalates when

<Conditions that require governor or owner decision rather than lane
action. Escalation: the governor always; never the owner directly.>
```

### 5. Normalization rules

1. **Governor reference:** All agents say "the governor" in their profile
   and charter, not "Kimi-K3" or "KK3". The governor role is currently
   held by Flash.
2. **Mia in the reporting chain:** All agents say "reports to the
   governor; work managed through Mia (Chief of Staff)" in their identity
   table.
3. **Model lane format:** One format for all —
   `<model-name> (<served-model-id>, <provider>, via OmniRoute hxs-8) —
   owner-assigned <date>, <verification-method>`.
4. **Identity table:** One format — the §1 Identity table from the
   standard template above. No separate "Document status" table.
5. **Profile depth:** Target 150–250 lines. Technical detail beyond the
   standard template moves to reference documents in the knowledge vault
   or pilot evidence, not the profile.
6. **Provenance:** Standard block at §10, same format for all.
7. **Charter frontmatter:** All charters have YAML frontmatter
   (name, description).
8. **Family field:** All identity tables and charters include the family
   number and name.
9. **Repo path:** All profiles reference the repo working directory and
   the specific repo files the agent needs.
10. **SSH section:** All agents that operate on remote hosts have a §6
    SSH and credential handling section with the askpass pattern. Agents
    that don't operate on remote hosts mark it "N/A — no remote host
    operations."

## Provenance

This KDD was informed by the agent structure recon conducted 2026-08-29
(17 findings across 11 agents) and the owner's provisional family
taxonomy (four groups, reviewed and adopted with Gordon in Family 3).