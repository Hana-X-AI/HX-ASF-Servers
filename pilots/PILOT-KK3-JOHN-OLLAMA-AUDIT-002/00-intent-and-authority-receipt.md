# Intent and Authority Receipt — PILOT-KK3-JOHN-OLLAMA-AUDIT-002

- Task ID: GOAL-OLLAMA-AUDIT-HXS4-001 (goal file: `goals/2026-08-24-ollama-audit-hxs4.md`)
- Requested Outcome: read-only audit of the live Ollama runtime on hxs-4, plus recommendation-only remediation guidance
- Human Authority: Agent Zero ("prep for real run against hxs4", 2026-08-24; approval discipline per AGENTS.md)
- Authoritative Inputs: `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-002/plan.md` (delta), base plan 001, `agents/john/profile.md`, KDD-0001..0003, lessons 2026-08-24
- In Scope / Out of Scope: per delta plan; all mutations prohibited
- Acceptance Criteria: SC-01..SC-09 plus SC-10 (version reconciliation), SC-11 (roster check)
- Constraints: strictly read-only; 1 session, 1 correction max, 1 transient retry max
- Risk Class: low (read-only on a live service; no load tests)
- Irreversible or Destructive Actions: none authorized
- Required Human Decisions: completion acceptance (pending)
- Knowledge Sources Identified: `/opt/tkv-local/ollama`; roster `agents/`
- Pre-flight (intake existence check): DONE 2026-08-24 — ollama 0.32.9, service active, API responding, both GPUs present on hxs-4
- Active Charters Reviewed: `agents/john` (active), `agents/kimi-k3` (active)
- Qualified Operational Agent Available: YES — john, via profile-briefed sub-agent dispatch
- Execution Authorized: YES — owner instruction plus approval-discipline rule; 2026-08-24T10:22Z
