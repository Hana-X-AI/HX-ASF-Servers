# System Validation Testing Workflow

Separate from deployment.

```mermaid
flowchart TD
    A[Select test plan\nfrom system config doc] --> B[Identify test cases\nV0-V6 gates + example scripts]
    B --> C[Execute test case]
    C --> D{Result}
    D -->|PASS| E[Append to test-log.md\nPASS + evidence]
    D -->|FAIL| F[Append to test-log.md\nFAIL + evidence + error]
    D -->|SKIP| G[Append to test-log.md\nSKIP + reason]
    E --> H{More tests?}
    F --> I{Fixable?}
    G --> H
    I -->|Yes| J[Fix issue]
    J --> C
    I -->|No| K[Escalate to governor\nwith evidence]
    H -->|Yes| C
    H -->|No| L[Update system config doc\nwith final test status]
    L --> M[Update change record\nwith verification result]
    M --> N[Run render.py]
    N --> O[Run validate.py — 4/4 PASS]
    O --> P[Commit]
    P --> Q[Done]
```

## Deliverables updated

- `test-log.md`, `system-config-doc.md`, `change-record.md`

## Skills triggered

- **be-great** (investigate failures)

## Hooks triggered

- `validate-changed.sh` (PostToolUse on `test-log.md`)
- `test-log-append.sh` (PostToolUse on test/evidence writes — reminds to append a dated row; added 2026-08-29, QA-audit ST-7)
- `render-sync.sh` (PostToolUse on `.md`/manifest writes — flags manifest drift before commit; added 2026-08-29, QA-audit ST-4)
