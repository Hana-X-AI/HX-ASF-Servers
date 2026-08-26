# CI/CD workflows

`ci-cd.yml` — the p8 pipeline (owner-ratified 2026-08-26). Push-triggered on all
branches: `gates` (lint, tests, wiki-sync, catalog validation, secret scan),
`coderabbit-review` (CodeRabbit CLI gate on non-main pushes), `pr-manage`
(auto-PR, auto-label, auto-merge, PR notifications). Full documentation:
`docs/cicd-pipeline.md`.
