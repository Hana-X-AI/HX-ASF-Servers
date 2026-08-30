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
    Q --> R[Run validate.py — 5/5 PASS (SY-2)]
    R --> S{All PASS?}
    S -->|Yes| T[Commit]
    S -->|No| U[Fix missing items]
    U --> Q
    T --> V[Hook: agent-creation-check.sh\nfires on Write to agents/]
    V --> W[Done]
```

[AMENDMENT 2026-08-30, labeled, append-only — VALIDATION GATE UPDATED: the active
gate in node R now reads "Run validate.py — 5/5 PASS (SY-2)" — the validator runs
5 checks including the governance-path check SY-2, effective 2026-08-30. The prior
wording is preserved verbatim here as history: "Run validate.py — 4/4 PASS". The
4/4 wording lives only in this labeled append-only amendment; 5/5 PASS (with SY-2
included) is the current rule. This correction remains open.]

## Deliverables created

- `charter.md`, `profile.md`, KDD, catalog YAMLs, roster entry, `AGENTS.md` entry, `system-mapping.md` entry, manifest entry

## Skills triggered

- **be-great** (TKV survey), **create-agent** (checklist walkthrough)

## Hooks triggered

- `agent-creation-check.sh` (PostToolUse on `agents/`)
