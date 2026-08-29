# WORK ORDER — Mia: normalize all 11 agent charters per KDD-0016

- Issuer: Flash (governor), 2026-08-29.
- Executor: Mia (Chief of Staff, KDD-0012).
- Lane: `omniroute/glm-5.3-flash`.

## Intent

KDD-0016 (ratified 2026-08-29) established a standard charter template.
All 11 agent charters need normalization:

1. **Add YAML frontmatter** (name, description) to all 11 charters.
2. **Add Family field** to the header (1/2/3/4 — family name).
3. **Update governor references**: replace "Kimi-K3" and "KK3" with "the
   governor" throughout. Exception: kimi-k3's own charter references the
   governor role — those stay as "the governor" (they already do, since
   kimi-k3 IS the governor).
4. **Update status field** to match current state (some say "draft" that
   should be "active" or "registered — activation-gated").
5. **Update the Escalates section** to say "the governor always; never the
   owner directly" if it doesn't already.

## Family assignments

| Agent | Family |
|---|---|
| kimi-k3 | Above all (governor) |
| mia | 4 (AI-PMO) |
| carol | 4 (AI-PMO) |
| morpheus | 3 (Platform Systems) |
| gordon | 3 (Platform Systems) |
| trinity | 3 (Platform Systems) |
| john | 3 (Platform Systems) |
| chris | 3 (Platform Systems) |
| wayne | 3 (Platform Systems) |
| rick | 2 (Infra/Ops) |
| rob | 1 (Agentic SE) |

## Template (from KDD-0016 / agents/_template/charter.md)

```markdown
---
name: <name>
description: <one-sentence summary>
---

# Agent: <name>

- Lane type: vertical | horizontal
- Family: <family>
- Status: <active | registered — activation-gated>
- Created: <date>

## Mission
## Owns
## Does not own
## Inputs
## Outputs
## Escalates when
```

## Constraints

- Preserve all existing content — only add frontmatter, family field, and
  update governor naming.
- Do NOT rewrite the charter — normalize in place.
- `scripts/validate.py` 4/4 after writes.
- Render any manifest-listed changes.
- Context budget: targeted, mechanical edits.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with a table: agent, frontmatter
added, family added, governor refs updated, status corrected.
