# CI/CD workflows

`ci-cd.yml` — the p8 pipeline (owner-ratified 2026-08-26; amended 2026-08-28).
Push-triggered on **all branches**: `gates` (lint, tests, wiki-sync, catalog
validation, secret scan), `coderabbit-review` (CodeRabbit CLI gate on **ALL
pushes incl. main** — owner directive 2026-08-28: "coderabbit should run on
every commit regardless of the type"; blocking = critical+major+minor,
zero-tolerance), `pr-manage` (auto-PR, auto-label, auto-merge, PR
notifications; non-main pushes). Full documentation: `docs/cicd-pipeline.md`.
