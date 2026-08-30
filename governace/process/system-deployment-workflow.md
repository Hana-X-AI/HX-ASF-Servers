# System Deployment Workflow

```mermaid
flowchart TD
    A[Owner directive] --> B[Create goal from template\ngovernace/templates/goal.md]
    B --> C[Author implementation plan\nfrom server template]
    C --> D[V0: Pre-state verification\nSSH to target, confirm clean state]
    D --> E{V0 PASS?}
    E -->|No| F[HALT: report to governor]
    E -->|Yes| G[Install system\nbinary, pip, apt, etc.]
    G --> H[Configure\nconfig file, env vars, systemd unit]
    H --> I[V1-V2: Version + Config posture]
    I --> J{V1-V2 PASS?}
    J -->|No| F
    J -->|Yes| K[V3-V4: API probe + Lifecycle]
    K --> L{V3-V4 PASS?}
    L -->|No| F
    L -->|Yes| M[V5-V6: Snapshot + Health monitoring]
    M --> N{V5-V6 PASS?}
    N -->|No| F
    N -->|Yes| O[Write credentials to .local.env]
    O --> P[Write evidence doc\nservers/host/system-evidence.md]
    P --> Q[Write change record\ngovernace/status-reporting/]
    Q --> R[Write system config doc\nservers/host/system-config.md]
    R --> S[Update test log\ngovernace/testing/test-log.md]
    S --> T[Run render.py]
    T --> U[Run validate.py — 4/4 PASS]
    U --> V{All PASS?}
    V -->|Yes| W[Commit]
    V -->|No| X[Fix issues]
    X --> T
    W --> Y[Done]
```

[AMENDMENT 2026-08-30, labeled: the "Run validate.py" gate above reads 4/4 PASS
as originally written; the validator now runs 5 checks (the governance-path
check, SY-2, was added to the full suite) — the gate reads 5/5 PASS effective
2026-08-30. Original diagram wording preserved; current reading: 5/5 PASS.]

## Deliverables created

- goal, plan, evidence doc, change record, system config doc, test log update, credentials

## Skills triggered

- **be-great** (TKV survey before install)

## Hooks triggered

- `validate-changed.sh` (PostToolUse), `secret-boundary.sh` (PreToolUse)
