# Goal: Read-only Ollama infrastructure and performance audit on hxs-4

- Goal ID: 2026-08-24-ollama-audit-hxs4 (this file's name)
- Version: 1
- Status: done — PASS (owner accepted 2026-08-24T12:50Z)
- Owner: Agent-Zero
- Created: 2026-08-24
- Human authority: Agent-Zero
- Agent lane(s): kimi-k3 (governor), john (operational audit agent, sub-agent dispatch)

## Intent

Produce a reproducible, sanitized, evidence-backed audit of the live Ollama runtime
on hxs-4: version reconciliation, effective configuration, model inventory and
residency, GPU alignment, network exposure, and material performance risks, plus
recommendation-only remediation guidance. This is the valid-target successor of
PILOT-001 (hxs-5, FAIL — invalid target; lessons in
`governace/lesson-learned/lessons-learned.md`).

## Scope and target

- Target identity: hxs-4 (192.168.50.203), service: ollama. Registry role:
  Retrieval & AI utility — consistent with Ollama presence.
- Baseline: **pre-flight verified 2026-08-24** (intake existence check): ollama
  0.32.9 at `/usr/local/bin/ollama`, service active, API `{"version":"0.32.9"}`,
  GPUs RTX 5060 Ti + RTX 5060 present. Full baseline to be established by John's
  knowledge review of `/opt/tkv-local/ollama` and read-only inspection.
- In scope: knowledge review; passive host/service/API/GPU/log inspection;
  installed/running version reconciliation against version-matched source; model
  inventory, digests, context, residency; passive performance-risk assessment;
  recommendation-only plan.
- Out of scope: any mutation; restarts/reloads; model pull/create/run/unload/delete;
  active inference, stress, load, or saturation testing; driver/OS/Ollama installs;
  remediation execution; fleet-role decisions.
- Constraints: strictly read-only; one John session, one correction session max,
  one transient retry max. Probes reach hxs-4 via SSH from the John session.

## Success conditions and evidence

Same SC-01..SC-09 contract as `governace/goals/2026-08-24-ollama-audit-hxs5.md`, evaluated by
the Kimi-K3 gate, with two additions:

| ID | Property | Measurement / procedure | Expected result | Evidence | Verifier |
| --- | --- | --- | --- | --- | --- |
| SC-10 | Version reconciliation | Installed CLI/server version vs version-matched source identity | Reconciled or explicitly unresolved and escalated | Audit matrix ID-04 | Kimi-K3 gate |
| SC-11 | Roster check first | `agents/` consulted before treating referenced profiles as current teammates | John is the only current Ollama specialist; craig treated as archived history | Knowledge review receipt | Kimi-K3 gate |

Verifier note: Kimi-K3 evidence gate is the evaluator. Final PASS requires a
recorded Agent Zero owner-review acceptance decision with timestamp after the gate.

## Execution controls

- Active charters reviewed (Phase M): `agents/john` (active), `agents/kimi-k3`
  (active). Qualified agent available: YES — john, via profile-briefed sub-agent
  dispatch.
- Pre-flight (intake existence check): DONE 2026-08-24 — see Baseline above.
- Maximum iterations / retries: 1 John session + 1 correction session; 1 transient
  read-only retry
- Stop conditions: pilot plan section 16, plus the fail-closed knowledge-review
  rule (authority/baseline NOT ESTABLISHED -> BLOCKED)
- Rollback / containment: not applicable (read-only)
- HITL checkpoints: authorization before execution; any section 16 escalation;
  completion acceptance

## Notes and links

- KDDs: KDD-0001, KDD-0002, KDD-0003
- Delta plan: `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-002/plan.md`
- Base plan: `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-001/plan.md`
- Lessons: `governace/lesson-learned/lessons-learned.md` (2026-08-24 entries)
