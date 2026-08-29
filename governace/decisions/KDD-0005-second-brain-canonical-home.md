# KDD-0005: Second Brain canonical home is the HX-ASF-Servers repository

- Date: 2026-08-25
- Status: ratified
- Decider: Agent-Zero
- Related goals: factory-wide (Second Brain / documentation governance)

## Context

The Second Brain guidance document (hx-second-brain-guidance-001, draft strategic
reference, not ratified for implementation) flags an open decision — its G-01:
canonical knowledge root, recommending `/opt/tkv-local`. As-built reality: the
operating Second Brain (Carol's catalog — records, index, receipts, retrieval
packages, CAT battery; 167 records as of 2026-08-25) lives at `knowledge/catalog/`
inside the HX-ASF-Servers repository, which is versioned, review-gated, and backed
up to GitHub (first pushed 2026-08-25). `/opt/tkv-local` is reference source corpus
(server records, knowledge trees) that the catalog points to. The governor
assessment (`knowledge/assessments/2026-08-25-hx-second-brain-guidance-001-review.md`,
recommendation R1) proposed ratifying the as-built split. Owner, 2026-08-25: "Why
is this a question — leave this in the repo."

## Options considered

1. Repository as canonical home (as-built) — version control, change gates, GitHub
   backup, review-tool coverage; catalog records reference TKV sources by pointer.
2. `/opt/tkv-local` as canonical home (guidance-document G-01 recommendation) —
   matches the document, but puts the brain in a reference tree without change
   control or review gates; migration cost for no measured benefit.

## Decision

The canonical Second Brain home is `knowledge/catalog/` in the HX-ASF-Servers
repository. `/opt/tkv-local` remains referenced source corpus, never the catalog's
home. The guidance document's G-01 is answered adapted: its `/opt/tkv-local`
recommendation is rejected in favor of the as-built repo home.

## Consequences

Enables: change-controlled, backed-up knowledge operations; G-01 closed (adapted).
Forecloses: any catalog migration to `/opt/tkv-local`; no second catalog root may
be created — one canonical root, per the guidance document's own "never both" rule.
Revisit only if the repository's own role changes.
