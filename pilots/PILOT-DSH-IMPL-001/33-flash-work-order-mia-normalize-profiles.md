# WORK ORDER — Mia: normalize agent profiles (mechanical fixes)

- Issuer: Flash (governor), 2026-08-29.
- Executor: Mia (Chief of Staff, KDD-0012).
- Lane: `omniroute/glm-5.3-flash`.

## Intent

KDD-0016 (ratified 2026-08-29) established a standard profile template.
The charters are done. Now normalize the profiles with three mechanical fixes
that apply across 9 profiles. These are find-and-replace style edits — no
structural changes, no section additions, no content rewriting.

## Fix 1 — Governor naming: "Kimi-K3" / "KK3" → "the governor"

Replace all references to "Kimi-K3" and "KK3" with "the governor" in
these 9 profile files. Do NOT touch agents/kimi-k3/profile.md (that IS the
governor's own profile — its references are about the role, not the name).

| Agent | File | Approx refs |
|---|---|---|
| morpheus | agents/morpheus/profile.md | 6 |
| gordon | agents/gordon/profile.md | 2 |
| rick | agents/rick/profile.md | 11 |
| john | agents/john/profile.md | 9 |
| carol | agents/carol/profile.md | 8 |
| trinity | agents/trinity/profile.md | 17 |
| rob | agents/rob/profile.md | 3 |
| mia | agents/mia/profile.md | 15 |
| chris | agents/chris/profile.md | 10 |

Rules:
- Replace "Kimi-K3" with "the governor"
- Replace "KK3" with "the governor" (in escalation markers like
  "ESCALATION TO KK3" → "ESCALATION TO THE GOVERNOR")
- Preserve surrounding context — don't change anything else
- Wayne's profile already uses "the governor (Flash)" — don't touch it

## Fix 2 — Add Family field to identity tables

Add a "Family" row to the identity table in each profile. The family
assignments per KDD-0016:

| Agent | Family |
|---|---|
| morpheus | 3 (Platform Systems) |
| gordon | 3 (Platform Systems) |
| rick | 2 (Infra/Ops) |
| john | 3 (Platform Systems) |
| carol | 4 (AI-PMO) |
| trinity | 3 (Platform Systems) |
| rob | 1 (Agentic SE) |
| mia | 4 (AI-PMO) |
| chris | 3 (Platform Systems) |
| wayne | 3 (Platform Systems) — already has it, skip |

For profiles with a "Document status" table (rick, john, carol, trinity),
add the Family row to that table. For profiles with "Identity and
placement" (morpheus, gordon, rob, mia, chris), add the Family row to
that table.

Insert the Family row after the "Role" row in each table.

## Fix 3 — Add Mia to reporting chains

For these 6 profiles that don't mention Mia at all, add "work managed
through Mia (Chief of Staff)" to the "Reports to" field in their identity
table:

| Agent |
|---|
| morpheus |
| gordon |
| rick |
| john |
| carol |
| trinity |

Format: change "Reports to | Kimi-K3" (which after Fix 1 becomes
"Reports to | the governor") to "Reports to | the governor; work managed
through Mia (Chief of Staff)".

For rob, chris, and wayne — they already mention Mia. Skip them.
For mia — she IS Mia. Skip.

## Constraints

- Mechanical edits only — no structural changes, no section additions,
  no content rewriting beyond the three fixes above.
- Do NOT touch agents/kimi-k3/profile.md.
- Do NOT touch agents/wayne/profile.md (already normalized).
- Do NOT distill rick/john (that's a separate task).
- Do NOT add SSH sections (that's a separate task).
- `scripts/validate.py` 4/4 after writes.
- Render any manifest-listed profiles you change.
- Context budget: targeted edits, not whole-file reads.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with a table: agent, governor refs
fixed, family added, Mia in chain. validate.py output pasted.
