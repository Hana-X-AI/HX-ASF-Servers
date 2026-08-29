# Governance

Central governance for the HX agentic software factory. This directory holds
the factory's decision records, issue tracking, lessons learned, process
documentation, project plans, research, status reporting, templates, and
testing artifacts.

## Directory structure

```text
governace/
├── README.md            — this file
├── decisions/           — Key Decision Documents (KDDs)
├── issue-tracking/      — open and closed issues
├── lesson-learned/      — lessons learned records
├── process/             — workflow diagrams, process docs, enforcement evidence
├── project-plan/        — project plans
├── reasearch/           — research documents (existing spelling preserved)
├── status-reporting/    — change records, status reports
├── templates/           — all templates (centralized)
└── testing/             — consolidated test log and test artifacts
```

## Purpose

This directory consolidates the factory's governance artifacts into a single
location. Previously these materials were spread across `governace/decisions/`,
`governace/issue-tracking/issues.md`, and `governace/lesson-learned/lessons-learned.md`. Those files have
been moved here and all cross-references updated.

- **decisions/** — Key Decision Documents (KDDs) record ratified owner and
  governor decisions: model lane assignments, agent registrations, pilot
  adoptions, architecture choices. Template: `templates/kdd.md`.
- **issue-tracking/** — Open and closed issues, action items, and backlog
  items that are deferred but not waived.
- **lesson-learned/** — Process learning entries: what worked, what failed,
  and what to do differently next time.
- **process/** — Workflow diagrams, process documentation, and enforcement
  evidence.
- **project-plan/** — Project plans for workstreams and initiatives.
- **reasearch/** — Research documents and investigations. (The directory name
  preserves the existing spelling.)
- **status-reporting/** — Change records and status reports.
- **templates/** — The single template directory for all artifact types:
  agent, server, goal, pilot, KDD, checklists, test logs, change records, and
  system config docs.
- **testing/** — Consolidated test log and test artifacts.
