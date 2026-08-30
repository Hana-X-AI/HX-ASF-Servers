# Agent Creation Workflow

```mermaid
flowchart TD
    A[Owner directive or governor work order] --> B[Survey TKV knowledge dir\nbe-great skill]
    B --> C[Confirm: name, family, model lane, host]
    C --> D[Create agents/name/ directory]
    D --> E[Create charter.md from template]
    E --> F[Create profile.md from template]
    F --> G[Fill mandatory sections\nIdentity, TKV, be-great, SSH, Skills, Provenance]
    G --> H[Register: agents/README.md roster]
    H --> I[Register: AGENTS.md taxonomy + lanes]
    I --> J[Register: system-mapping.md S-N row]
    J --> K[Register: SERVER-REGISTRY.md if host-bound]
    K --> L[Create KDD registration document]
    L --> M[Add KDD to wiki manifest]
    M --> N[Create catalog records\ncharter + profile + KDD YAML]
    N --> O[Add catalog records to index.yaml]
    O --> P[Verify model lane via OmniRoute]
    P --> Q[Run render.py]
    Q --> R[Run validate.py — 5/5 PASS]
    R --> S{All PASS?}
    S -->|Yes| T[Commit]
    S -->|No| U[Fix missing items]
    U --> Q
    T --> V[Hook: agent-creation-check.sh\nfires on Write to agents/]
    V --> W[Done]
```

Revision note (2026-08-30, A3 artifact-class policy): the gate reads 5/5 PASS
(governance-path check SY-2 added to the suite). Prior 4/4 wording is retained in
Git history.

## Deliverables created

- `charter.md`, `profile.md`, KDD, catalog YAMLs, roster entry, `AGENTS.md` entry, `system-mapping.md` entry, manifest entry

## Skills triggered

- **be-great** (TKV survey), **create-agent** (checklist walkthrough)

## Hooks triggered

- `agent-creation-check.sh` (PostToolUse on `agents/`)
