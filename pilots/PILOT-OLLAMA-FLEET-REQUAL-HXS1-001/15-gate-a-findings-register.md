# Gate A — findings register and remediation plan (DRAFT template)

Parent goal: `governace/goals/ollama/2026-08-31-ollama-fleet-requalification-hxs1-qwen-x.md`
Status: template only — populated from M1–M4 evidence and submitted to James + Agent Zero before Phase B.

## Required contents

- Severity-ranked findings register: every finding states evidence, exact change,
  expected benefit, risk, prerequisites, validation, rollback, owning lane, and
  authorized / not-authorized.
- Remediation plan: the concrete Phase B write set (Ollama, DNS, routing) derived
  only from the findings.
- Decisions for James + Agent Zero: service FQDN (D1), upgrade authority (D2),
  downtime/test window (D3), RAG boundary (D4), web-search/cloud posture (D5),
  and any unexpected OS/driver/DNS/router/storage/network change that must
  become a separate Rick order.
- Rollback plan: smallest affected layer and deterministic inverse per change.

## Gate rule

Phase B cannot begin on an inferred or open-ended scope. The write set is fixed
here; nothing outside it is executed.
