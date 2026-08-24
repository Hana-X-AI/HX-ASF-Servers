# PILOT-KK3-JOHN-OLLAMA-AUDIT-002 — hxs-4 Ollama audit (delta plan)

| Field | Value |
| --- | --- |
| Pilot ID | `PILOT-KK3-JOHN-OLLAMA-AUDIT-002` |
| Goal ID | `GOAL-OLLAMA-AUDIT-HXS4-001` |
| Goal file | `goals/2026-08-24-ollama-audit-hxs4.md` |
| Base document | `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-001/plan.md` (ratified structure) |
| Target host | hxs-4 (192.168.50.203) |
| Component | Ollama — expected PRESENT |
| Status | Draft — staged, awaiting Agent-Zero authorization |

This delta overrides the base plan only where stated. Every other section of the
base plan applies unchanged: audit matrix, read-only guardrails, evidence package
layout, command-log schema, report structure, evidence gate, process acceptance
matrix, stop conditions, completion record.

## Overrides

1. **Target**: hxs-4 (192.168.50.203), registry role Retrieval & AI utility —
   consistent with Ollama presence. Identity verification compares against
   192.168.50.203 (base plan ID-01 rule).
2. **Intake pre-flight (new, lesson L1)**: existence check required and recorded
   before `GOAL_READY`. DONE 2026-08-24: ollama 0.32.9 at `/usr/local/bin/ollama`,
   service active, API `{"version":"0.32.9"}`, RTX 5060 Ti + RTX 5060 present.
3. **Execution path**: the John session runs on hxs-5 and reaches hxs-4 via SSH
   (`hxsa@192.168.50.203`, owner-provided credential via askpass pattern; no secret
   in the repo, logs, or evidence).
4. **Roster check (new, craig lesson)**: the knowledge review consults `agents/`
   first. John is the only current Ollama specialist; craig material is archived
   history under `implementation/archive/HX-Infrastructure-main/` in the vault.
5. **Fail-closed knowledge review (new, lesson L3)**: if authority or baseline for
   Ollama on hxs-4 is NOT ESTABLISHED, the receipt is `Task May Proceed: NO` and
   the pilot moves to BLOCKED.
6. **Version reconciliation**: installed 0.32.9 must be reconciled against the
   corpus source snapshot (identified in prior material as v0.32.11); the
   version-matched source rule from John's profile applies.
7. **Evidence root**: `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-002/` with the same
   numbered artifact layout as the base plan.

## Readiness gate additions (beyond base section 19)

- Pre-flight existence check recorded and target role consistent with
  SERVER-REGISTRY?
- SSH access path from the John session to hxs-4 confirmed?
