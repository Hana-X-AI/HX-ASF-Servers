# PILOT-OLLAMA-FLEET-REQUAL-HXS1-001 — Decomposition Plan (DRAFT)

Parent goal: `governace/goals/2026-08-31-ollama-fleet-requalification-hxs1-qwen-x.md`
Intake source: `governace/sponsor/hxs-1/2026-08-31-factory-intake-ollama-fleet-requalification-wo1-hxs1.md`
Status: goal APPROVED (2026-08-31) — Phase A dispatching; Phase B still gated on Gate A.

## 0. Target lock (001/002 lesson)

TARGET for every downstream live action is **hxs-1 (192.168.50.200)**, call-sign
Qwen-X, role Deep reasoning & synthesis, model Qwen 3.8 27B. This is Wave 1 of
the four-Ollama-server program and is scoped to hxs-1 only; hxs-2 (Coder-X),
hxs-3 (Meta-X), and hxs-4 (Chat-X) are future waves and are OUT OF SCOPE for
this package — they do not begin until hxs-1 is fully complete and Agent Zero
approves. No agent may direct the Ollama audit, remediation, DNS, test, or
qualification work at hxs-2/3/4 or hxs-5; hxs-5 is the control plane (session
host and `/opt/tkv-local` location) only, and hxs-15 is Gordon's independent
verifier only. Fail-closed: before any probe the executor verifies hostname +
machine-id + peer IP and reconciles the target with `servers/SERVER-REGISTRY.md`
(hxs-1 row = Qwen-X). A mismatch aborts the session — this is the exact defect
that failed PILOT-KK3-JOHN-OLLAMA-AUDIT-001 (wrong target hxs-5) and must not
recur.

## 1. Owner decisions (answered 2026-08-31)

| ID | Decision | Owner answer |
| --- | --- | --- |
| D1 | Service FQDN | APPROVED: `qwen-x.hx.local.arpa` |
| D2 | Upgrade authority | APPROVED auto-update: update to the latest Ollama version if a newer release exists |
| D3 | Downtime / test window | Three full reboots + one performance run; 24-hour soak removed (overkill) |
| D4 | RAG integration boundary | Full access to any system in the current RAG pipeline; no new systems installed |
| D5 | Web search / cloud posture | Ollama cloud ON and web search active (fleet-wide owner posture); test and verify on hxs-1 only; cloud-model substitution still prohibited |

## 2. Milestones and phase gates

| Milestone | Scope | Lane | Mutation |
| --- | --- | --- | --- |
| M0 | Intake and scope-lock (D1–D5 answered) | James / Agent Zero | none |
| M1 | Live TKV knowledge review | John | none (read) |
| M2 | Live hxs-1 read-only audit (all audit vectors) | John | none (read) |
| M3 | DNS / network / service-FQDN discovery and design | Rick | none (read) |
| M4 | Test, benchmark, capability-matrix, RAG/tool/web-search/reliability design | Bailey | none (read) |
| M5 | Findings register + remediation plan assembly | James / Mia | none (read) |
| **Gate A** | Approve findings, write set, upgrade, DNS alias, downtime, rollback | James + Agent Zero | gate |
| M6 | Bounded remediation (only Gate-A-approved changes) | John | approved only |
| M7 | Service FQDN / DNS alias registration | Rick | approved only |
| M8 | OmniRoute / routing registration (if in scope) | Trinity | approved only |
| M9 | Active qualification execution (capability, RAG, tool, web search) | Bailey + John | approved only |
| M10 | Independent verification + reliability (three full reboots + one performance run) | Gordon | approved only |
| M11 | Catalog reconciliation (authority/security/reusable-platform changes) | Carol | approved only |
| **Gate B** | Governor checklist + Gordon qualification + Carol receipt + owner acceptance | James + Gordon + Carol + Agent Zero | gate |

## 3. Agent routing

- James: intake, governed decomposition, gate assembly, governor verification checklist, escalation. No operational execution.
- Mia: sequencing, dependency routing, owner checkpoints.
- John: TKV review, runtime/model audit, approved Ollama/model changes, tuning, evidence. Host: hxs-1 via SSH from hxs-5.
- Rick: OS/systemd platform issues outside John's unit boundary; DNS/router/service FQDN; driver/kernel work only under separate authority.
- Bailey: test design before mutation, fixtures, benchmark schema, capability/RAG/tool/web-search/reliability suites.
- Gordon: independent live-state verification from a different host (hxs-15), regression qualification, three-reboot + performance-run acceptance.
- Trinity: OmniRoute/service routing integration if in scope.
- Raphael / Quinn: real RAG and vector/retrieval integration within the current pipeline; full access (D4) but no new systems.
- Carol: catalog disposition, reusable platform knowledge, endpoint/capability record reconciliation.

## 4. Exact write sets

Phase A (M1–M5) is read-only against hxs-1: no service, model, DNS, OS, or
repository mutation of live target state. The only Phase A writes are evidence
and plan documents at the destinations named in each work order.

Phase B write sets are fixed at Gate A. Until then, the Phase B work orders below
carry the boundary and prohibition set, with the concrete mutation allowlist
marked "to be finalized at Gate A."

## 5. Work-order package

| # | Work order | Lane | Phase | Gate dependency |
| --- | --- | --- | --- | --- |
| 01 | John TKV knowledge review | John | A | M0 |
| 03 | John live read-only audit | John | A | M1 |
| 05 | Rick DNS/FQDN discovery + design | Rick | A | M0 (parallel with M1/M2) |
| 07 | Bailey test/capability design | Bailey | A | M0 (parallel with M1/M2) |
| 09 | John bounded remediation | John | B | Gate A |
| 10 | Rick service FQDN registration | Rick | B | Gate A |
| 11 | Trinity OmniRoute routing | Trinity | B | Gate A (if in scope) |
| 12 | Bailey active qualification | Bailey | B | Gate A + M6 + M7 (+ M8 if OmniRoute routing in scope) |
| 13 | Gordon independent verification | Gordon | B | Gate A + M9 |
| 14 | Carol catalog reconciliation | Carol | B | Gate B pre-close |

Context packets 02, 04, 06, 08 pair with the four Phase A work orders. Phase B
context packets are generated at dispatch (post Gate A) once live `current_state`
is established.

## 6. Program relationship

This is Wave 1 of 4 and is scoped to hxs-1 only. hxs-2 (Coder-X), hxs-3
(Meta-X), and hxs-4 (Chat-X) are separate future waves; they do not begin until
hxs-1 is fully complete and Agent Zero records approval, and they are out of
scope for this package. Those waves reuse this method, capability schema,
evidence package, and acceptance gates; host values are never copied blindly.
