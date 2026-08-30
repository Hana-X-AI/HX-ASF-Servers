---
name: grilling
description: "Design-tree interview that stress-tests a plan, decision, or idea in rounds. HX adaptation of mattpocock/skills grilling (MIT): question rounds are capped at 5 per round per owner directive 2026-08-30. NOT the factory scope-lock gate — that is grill-me. Use for design and product stress-testing, typically under grill-with-docs or triage."
---

# Grilling — design-tree interview (HX, ≤5 questions per round)

Interview the user until you reach a shared understanding. Map this as a
**design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose
prerequisites are already settled: the questions you can ask _now_ without
guessing at answers you haven't heard yet.

## The 5-question budget (HX correction, owner directive 2026-08-30)

Ask **at most five questions per round**. Number each and give your recommended
answer. Then wait for the user's answers before the next round.

When the frontier holds more than five questions, prioritize: ask only the
questions whose answers would change a decision in this round. Fold the
remainder into **explicit stated assumptions** the user can correct, and carry
them to the next round if they are still open.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the
frontier outward and unblock questions that depended on them. Recompute the
frontier and ask the next round. A question whose answer depends on another
question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a
fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to
find it; don't ask the user for anything you could look up yourself. Don't block
on it: a running exploration is an unsettled prerequisite, so only the questions
downstream of it wait for the sub-agent to report; ask the rest of the frontier
now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree
visited, nothing left silently assumed, and every folded assumption either
confirmed or converted into a question. Do not act on it until the user confirms
you have reached a shared understanding.

## Precedence against grill-me (binding)

`grill-me` is the **factory scope-lock gate**: the interview James runs before a
work order dispatches, confirming objective, target, boundaries, exclusions,
acceptance, and assigned lane. That gate is `grill-me` and only `grill-me`.

This skill never substitutes for it. Invoking `grilling` at the scope-lock stage
does not satisfy the gate, and the 5-question cap applies to both — there is no
interview path in this repository that asks the owner more than five questions
in a round.

Use `grilling` for design and product stress-testing inside a lane's work, where
`grill-with-docs` and `triage` call it.

## Provenance and corrections

- **Source:** `mattpocock/skills`, `skills/productivity/grilling/SKILL.md`,
  upstream commit `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`, MIT
  (Copyright (c) 2026 Matt Pocock).
- **Adopted:** 2026-08-30, KDD-0020.
- **Corrections made at intake** (AGENTS.md §"Adoption of provided documents" —
  provided documents are inputs to review, not gospel):
  1. Upstream instructs an unbounded interview ("relentlessly", "ask the whole
     frontier in one round"). Corrected to a **5-question-per-round budget**
     with explicit stated assumptions for the remainder — owner directive
     2026-08-30, the same directive that caps `grill-me`. Adopting the uncapped
     form would have reopened, through a different skill name, the exact
     behavior the owner had just bounded.
  2. Added the binding precedence rule against `grill-me` above, so the
     scope-lock gate cannot be satisfied by calling this skill instead.
  3. Upstream's `grill-me` is a one-line wrapper delegating here. This repo's
     `grill-me` is an independent HX rewrite and does **not** delegate to this
     skill; the two are separate entry points with separate scopes.
