---
name: grill-me
description: "Scope-lock interview for the HX factory (adapted from mattpocock/skills grill-me/grilling, MIT). James interviews Zero before a work order dispatches: clarifies the objective, target, boundaries, exclusions, acceptance, and assigned lane. LIMITED to 5 questions per owner directive — not relentless. Use at the scope-lock stage before goal decomposition. NOT for: decomposition (goal-decompose), status (work-status), or execution."
maturity: active
---

# Grill-Me — scope-lock interview (James, ≤5 questions)

Adapted from `mattpocock/skills` grill-me/grilling (MIT). In the HX factory
this is the **scope-lock step**: James interviews Zero to confirm a work-order
intent before anything dispatches. Per owner directive 2026-08-30, James asks
**5 or fewer** questions — not relentless.

## When to use

At the scope-lock stage (Case A: harness = governor James). Zero has stated an
intent that is work (not conversational, not agent-proposed). James needs to
confirm the six scope-lock fields before writing the goal contract.

## The six fields to confirm

1. **Objective** — what changes, in one sentence.
2. **Target** — exact system + host (read from server-mapping, not guessed).
3. **Boundaries** — what's in scope (explicit allowlist).
4. **Exclusions** — what's NOT in scope.
5. **Acceptance** — the single-line "done when" statement.
6. **Assigned family/lane** — which job family (from the locked lane table).

## Method — the 5-question budget

1. **Find facts yourself** — never ask Zero for anything you can look up
   (server-mapping, TKV, current state). Use sub-agent/tools to fetch facts;
   don't burn a question on them.
2. **Prioritize the frontier** — ask only questions whose answers would change
   one of the six fields. The 5-question budget forces hard prioritization.
3. **Recommend an answer** for each question — give Zero a default to accept or
   correct (fast async confirmation; S3 = async-capable).
4. **Fold the rest into assumptions** — anything beyond 5 questions becomes an
   explicit assumption James states; Zero can correct at confirmation.
5. **Stop at shared understanding** — when the six fields are confirmed, the
   scope-lock record is complete. Do NOT act (decompose/dispatch) until Zero
   confirms.

## Question format

```
❓ Q1 — <field>: <question, choices>
➡️ <recommended answer>
```

Ask all ≤5 questions in one round; wait for Zero's answers before the next
round (if a second round is needed within the budget).

## Output

A confirmed scope-lock record: the six fields + the ≤5 questions/answers + the
stated assumptions. This becomes the first section of the goal contract
(`governace/goals/<id>.md`).

## Boundaries

- Max 5 questions — owner directive, non-negotiable.
- Facts are found, not asked. Decisions are Zero's.
- Never dispatch before shared understanding is confirmed.
- Minor scope change later = amend in place with a labeled note; material =
  re-lock (S4).
