---
name: domain-modeling
description: "Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording a decision. HX adaptation of mattpocock/skills domain-modeling (MIT): in HX-ASF-Servers decisions are KDDs under governace/decisions/, never docs/adr/."
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily: only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## Where decisions go in HX (binding placement rule)

The upstream layout above applies to **application projects** — the codebases
Rob builds in the Agentic Software Engineering lane. There, `CONTEXT.md` and
`docs/adr/` live inside the app project.

Inside **this** repository (HX-ASF-Servers, the governance and evidence control
plane) the layout above does **not** apply:

- Decisions are **Key Decision Documents (KDDs)** under `governace/decisions/`,
  authored from `governace/templates/kdd.md`. Do not create `docs/adr/` here.
- KDDs are **append-only**. A superseded decision is amended with a dated,
  labeled correction that preserves the original text; it is never rewritten.
- A KDD is a major document, so it ships `.md` plus a generated `.html` via
  `scripts/wiki/render.py` and must be listed in `scripts/wiki/manifest.txt`.
- Domain vocabulary for the factory lives in the catalog
  (`knowledge/catalog/`), stewarded by Carol — not in a root `CONTEXT.md`.
  Propose terms through a catalog record, not by creating a parallel glossary.

The `ADR-FORMAT.md` and `CONTEXT-FORMAT.md` companions in this skill describe
the upstream formats. Use them in application projects; use
`governace/templates/kdd.md` here.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up: capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md)
in application projects, or `governace/templates/kdd.md` inside HX-ASF-Servers
(see the placement rule above).

## Provenance and corrections

- **Source:** `mattpocock/skills`, `skills/engineering/domain-modeling/`,
  upstream commit `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`, MIT
  (Copyright (c) 2026 Matt Pocock).
- **Adopted:** 2026-08-30, KDD-0020.
- **Corrections made at intake** (AGENTS.md §"Adoption of provided documents"):
  1. Added the binding placement rule above. Upstream directs decisions to
     `docs/adr/` and vocabulary to a root `CONTEXT.md`; in this repository
     decisions are append-only KDDs under `governace/decisions/` and vocabulary
     is Carol's catalog. Adopting the upstream layout unamended would have
     created a second, ungoverned decision record alongside the KDD series.
  2. Noted the KDD dual-format and manifest requirements, which have no
     upstream equivalent.
