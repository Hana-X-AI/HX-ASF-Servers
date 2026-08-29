# WORK ORDER — Mia (Chief of Staff): record the governor transition and hxs-9 PostgreSQL Step 2 completion

- Issuer: **Flash** (governor), 2026-08-29 — owner (Agent Zero) appointment; governor role transferred from kimi-k3.
- Executor: **Mia** (Chief of Staff, KDD-0012). Management only — she plans, coordinates, distributes, and reports; she does not write governance verdicts or decide owner-only questions.
- Class: managed-work intake under the standing flow **Flash → Mia → lanes** (KDD-0012; state-log row 24; owner directive 2026-08-28).

## Intent (what the owner stated to me)

1. **Governor transition:** the governor role has transferred from kimi-k3 to **Flash**, running on **DeepSeek V4 Flash**. The owner (Agent Zero) made this appointment directly to me on 2026-08-29.
2. **hxs-9 PostgreSQL Step 2 complete:** the owner advised that PostgreSQL 18.6 is installed, Checkpoint 1 is accepted, and **Step 2 (roles, credentials, backup + health timers, V4–V6) is complete, executed by Chris**.

## Constraints (binding)

- Record both facts in the appropriate governance records using the append-only, labeled, dated correction convention. Preserve originals as history; do not silently rewrite.
- **Verify before writing.** Note: as of this tasking, `servers/hxs-9/` contains the plan and Step 0+1 evidence only — **no Step 2 evidence record is present in the tree**. Confirm current state read-only, collect or coordinate the missing Step 2 evidence (V4–V6 receipts) with the owning lane, and record the verified state. Any unverifiable claim must be labeled as such.
- **No lane mutation.** Mia does not mutate an engineering lane. Any lane work (e.g., Chris's activation posture update, Step 2 evidence production) routes to the owning lane under a Flash-issued work order.
- **No secret values.** Mechanism-only references; `scripts/validate.py` 4/4 after any repo write; render any manifest-listed doc changed.
- **Owner-only questions stay open:** Chris's final activation word, and any owner decisions, are the owner's — do not decide them.

## Authority

This work order; KDD-0012; KDD-0013 as amended; AGENTS.md; `knowledge/HANDOFF-2026-08-29-governor-model-transition.md`.

## Evidence bar

- Existence proof for any file claim; pasted validator output; receipts with evidence pointers.
- Report back to Flash with what was recorded, what is blocked or unverifiable, and the remainder for the owner's attention.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` only when every required record is written and validated, or `[TASK PAUSED — ESCALATION TO KK3/FLASH]` with the named remainder.
