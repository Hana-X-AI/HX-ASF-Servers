# hxs-3 — OAI-X Configuration

**Configuration date:** 2026-08-29
**Agent lane:** john (Ollama engineer, KDD-0013)
**Status:** PROPOSED — NOT EXECUTED (config doc describes the TARGET configuration, not current state)

> **[OPEN CORRECTION 2026-08-29, labeled, append-only — status corrected from
> "Operational (OAI-X deployed, Meta-X decommissioned)" to PROPOSED.]** This
> document described OAI-X as deployed and operational, which is NOT evidenced
> and is contradicted by the governing records: the goal
> (`goals/2026-08-29-oai-x-replace-meta-x.md`) is `draft` and the implementation
> plan (`servers/hxs-3/2026-08-29-oai-x-implementation-plan.md`) is
> `NOT APPROVED / NOT EXECUTED`. This is the TARGET configuration the plan would
> produce once approved and executed; the current hxs-3 configuration remains
> Meta-X (`hx-muse-glimmer-64k`) per `servers/hxs-3/configuration.md`. Update
> this file to a real "operational" state only after execution evidence exists
> (ollama list, digest, preload pin, state-log row).
>
> [LABELED CORRECTION 2026-08-30, append-only — GOAL PATH RELOCATED: the goal
> reference above records the historical `goals/2026-08-29-oai-x-replace-meta-x.md`
> path as written at the 2026-08-29 correction. The goal tree was relocated to
> `governace/goals/` on 2026-08-30 (KDD-0002 Amendment 1); the current path is
> `governace/goals/2026-08-29-oai-x-replace-meta-x.md`. The historical `goals/`
> entry above is preserved unchanged; read it as the relocated tree.]

## Functional role

OAI-X (gpt-oss-20b) serves as the factory's
tooling/structured-contracts LLM. It provides tool-calling,
structured JSON output, and general LLM inference for the RAG
pipeline and factory workloads. It is a sequential,
one-tool-call-per-turn specialist — the model proposes at most one
tool call per turn and never authorizes or executes; the governor
retains orchestration, parallelization-above-the-model, acceptance,
and evidence.

## Technical configuration

| Property | Value |
| --- | --- |
| Host | hxs-3 (192.168.50.202) |
| Ollama version | 0.32.15 (pinned) |
| Ollama endpoint | `192.168.50.202:11434` |
| Model | `gpt-oss:20b` |
| Alias | `hx-oai-x-64k` |
| Context window | 65536 (64K) |
| Model store size | 13 GB (single model + alias) |
| Model store path | `/usr/share/ollama/.ollama/models` (ollama:ollama) |
| Preload service | `ollama-preload.service` (pins `hx-oai-x-64k`, keep_alive=-1) |

## Capabilities

- Tool-calling (structured output)
- Structured JSON output
- General LLM inference

## Dependencies

| Dependency | Provider | Status |
| --- | --- | --- |
| Ollama runtime | john (Ollama engineer) | Active on hxs-3 |
| OmniRoute routing | trinity (OmniRoute engineer) | PENDING — route refresh from Meta-X to OAI-X not yet applied |

## Disabled / decommissioned

| Feature | Status | Reason |
| --- | --- | --- |
| Meta-X (Muse Glimmer 30B) | Decommissioned | Too slow for LightRAG entity extraction (OmniRoute 504 timeout). All 5 muse-glimmer models removed from the Ollama model store. |

## Rollback

If OAI-X fails in production, re-pull the Meta-X artifact:

```bash
ollama pull muse-glimmer:30b
```

Then restore the `hx-muse-glimmer-64k` alias and repoint
`ollama-preload.service` to the Meta-X digest
(`9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da`).

## Discovery reference

```text
servers/hxs-3/discovery.md
```

As-found record dated 2026-08-12; preserved unchanged. Do not
modify the discovery record.

## Sources

- `servers/hxs-3/configuration.md` (pre-change configured state)
- `servers/hxs-3/2026-08-29-oai-x-implementation-plan.md` (execution plan)
- `governace/status-reporting/change-meta-x-to-oai-x-2026-08-29.md` (change record)
- `governace/goals/2026-08-29-oai-x-replace-meta-x.md`
- `governace/decisions/KDD-0007-hxs3-muse-glimmer-tooling-adoption.md`
