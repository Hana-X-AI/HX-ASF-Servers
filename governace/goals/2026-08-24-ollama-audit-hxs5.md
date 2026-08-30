# Goal: Read-only Ollama infrastructure and performance audit on hxs-5 (process pilot)

- Goal ID: 2026-08-24-ollama-audit-hxs5 (this file's name)
- Version: 1
- Status: **abandoned** — parked, no longer applicable (readiness gate: pilot plan
  section 19 never reached)
  [Status note 2026-08-29: PARKED — hxs-5 replaced hxs-cp as the control
  workstation (owner advisory 2026-08-27). hxs-5 does not run Ollama
  (it's the governor workstation). This audit goal is no longer
  applicable. Original status preserved above as history.]
  [LABELED STATUS NORMALIZATION 2026-08-30, append-only: the PARKED state is
  recorded under the allowed terminal status `abandoned` per the goal template's
  status contract (draft | approved | in-progress | blocked | done | abandoned);
  the parked explanation above is preserved unchanged.]
- Owner: Agent-Zero
- Created: 2026-08-24
- Human authority: Agent-Zero
- Agent lane(s): kimi-k3 (governor), john (operational audit agent, sub-agent dispatch)

## Intent

Dual outcome: (1) a reproducible, sanitized, evidence-backed audit of the Ollama
runtime, hardware alignment, deployed-model configuration, network exposure,
resource posture, and material performance risks on hxs-5, plus recommendation-only
remediation guidance; (2) process proof that goal-based, fresh-session,
evidence-gated orchestration works between Kimi-K3 and John. Full plan:
`pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-001/plan.md`.

## Scope and target

- Target identity: hxs-5 (192.168.50.204), service: ollama
- Baseline: pending authorization. To be established by John's knowledge review of
  `/opt/tkv-local/ollama` and read-only host inspection after the section 19 gate
  passes; the baseline is complete only when the Knowledge Review Receipt and
  command log exist.
- In scope: knowledge review; passive host, hardware, GPU, storage, service,
  endpoint, and log inspection; installed/running version reconciliation; model
  inventory, digests, context, residency; passive capacity and performance-risk
  assessment; recommendation-only remediation plan; process validation
- Out of scope: any configuration or state mutation; restart/reload/reboot; model
  pull/create/run/copy/unload/delete; active inference, stress, load, write-I/O, or
  saturation testing; driver/kernel/Ollama/OS installs; remediation execution;
  production model selection or fleet-role decisions
- Constraints: strictly read-only and non-disruptive; one John session, one
  correction session maximum, one transient read-only retry maximum

## Success conditions and evidence

| ID | Property | Measurement / procedure | Expected result | Evidence | Verifier |
| --- | --- | --- | --- | --- | --- |
| SC-01 | Knowledge review first | Receipt timestamp vs first probe | Receipt precedes probes | Knowledge review receipt, command log | Kimi-K3 gate |
| SC-02 | Identity reconciliation | CLI, systemd ExecStart, /api/version, source compare | Reconciled or explicitly unresolved and escalated | Audit matrix ID-04 | Kimi-K3 gate |
| SC-03 | Every audit vector statused | Matrix review | PASS/FAIL/BLOCKED/NOT RUN with evidence | Audit test matrix | Kimi-K3 gate |
| SC-04 | Sanitized reproducible evidence | Sanitization and hash review | Redacted, timestamped, host-identified | Evidence package, sha256sums.txt | Kimi-K3 gate |
| SC-05 | Claim classes separated | Report structure review | Fact, authority, history, inference, recommendation separated | Audit report | Kimi-K3 gate |
| SC-06 | No prohibited mutation | Command log review | Zero mutations or disruptive operations | Command log | Kimi-K3 gate |
| SC-07 | Recommendations trace to evidence | Remediation table review | Traced to evidence, benefit, risk, validation, rollback | Remediation table | Kimi-K3 gate |
| SC-08 | Governor runs zero operational work | State log review | Only state transitions recorded (section 2.1 dispatch model) | State log | Kimi-K3 gate |
| SC-09 | Final gate reconciles artifacts | Gate checklist | Report, log, matrix, evidence, hashes reconcile | Quality gate decision | Kimi-K3 gate |

Verifier note: Kimi-K3 evidence gate is the evaluator. A final PASS additionally
requires a recorded Agent Zero owner-review acceptance decision with timestamp,
captured in the completion record after the gate; the pre-execution authorization in
this file is not final acceptance (profile section 11, Phase M fallback).

## Execution controls

- Active charters reviewed (Phase M): `agents/john` (active), `agents/kimi-k3`
  (active). Qualified agent available: YES — john, via profile-briefed sub-agent
  dispatch (pilot plan section 2.1).
- Maximum iterations / retries: 1 John session + 1 correction session; 1 transient
  read-only retry
- Time / token limits: bounded per session
- Stop conditions: pilot plan section 16 (access failure, hostname mismatch,
  authority/version conflict, unsafe command, failed mandatory test, unexpected
  state, secret exposure, possible harm, missing evidence)
- Rollback / containment: not applicable (read-only); quarantine on integrity concern
- HITL checkpoints: section 19 readiness gate before execution; any section 16
  escalation; completion record acceptance

## Notes and links

- KDDs: KDD-0001, KDD-0002, KDD-0003
- Pilot plan: `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-001/plan.md`
- Profiles: `agents/john/profile.md`, `agents/kimi-k3/profile.md`,
  `agents/kimi-k3/goal-setting-guidance.md`
