# Goal: Provision the hxs-2 coding-inference backend (CoderX via Ollama, mutating pilot)

- Goal ID: 2026-08-26-hxs2-qwen36-coderx-backend (this file's name)
- Version: 1
- Status: in-progress — M0 authorized 2026-08-26 (plan approved; D1–D8 decided and recorded; M1 COMPLETE 13/13, handoff pending Carol receipt)
  [Status transition 2026-08-29 **[current]**: COMPLETE — hxs-2 registry
  status READY; Coder-X (Qwen2.5-Coder-32B, AWQ Int4, TP=2) deployed and
  verified per SERVER-REGISTRY. SC-08 owner sign-off recorded by
  deployment acceptance. M7b soak remains deferred per owner directive
  (issues.md). Original status preserved above as history.]
  [Labeled note 2026-08-29: D3 artifact (mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M)
  superseded by owner deployment decision (Qwen2.5-Coder-32B AWQ Int4);
  SERVER-REGISTRY confirms READY with the deployed model.]
- Owner: Agent-Zero
- Created: 2026-08-26
- Human authority: Agent-Zero
- Agent lane(s): kimi-k3 (governor), rick (Ubuntu OS plane), john/Esme (Ollama plane), carol (knowledge)
- Plan: session plan `namor-karnak-nick-fury.md` (approved 2026-08-26); source directive `agent-zero-docs/pilots/hxs-2/hxs-2-deployment.md` (DoD re-scoped Harness-free per owner, this file §SC table)

## Intent

Provision `hxs-2` as a persistent local coding-inference host using Ollama with
the exact model **`mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M`** (owner D3,
registry-verified 2026-08-26), validated end to end, exposed through an
authorized LAN-scoped endpoint, and registered in the HX Second Brain catalog
as the discoverable backend-capability of record. DeepSeek Harness does not
exist (owner-confirmed easter egg, 2026-08-26); the catalog fills the
capability-registry role. Maximum measured task quality with evidence-gated,
deterministic operations; the model is an inference backend, never an
autonomous agent; KK3 retains orchestration.

## Scope and target

- Target identity: hxs-2 (192.168.50.201). Registry role: Coding.
- Baseline: i7-5960X 8c/16t, 66 GB RAM, 2× RTX 5060 Ti 16,311 MiB (driver
  580.173.02 validated 2026-08-12, CUDA 13.0), Ubuntu 24.04.4, kernel 7.0.0-28,
  3.6 TB NVMe root, no Ollama/vLLM, ufw inactive, Wi-Fi DOWN as-found.
- In scope: OS readiness, Ollama install/pin, exact-tag pull + identity freeze,
  preload/persistence, native-defaults baseline, coding/tool/vision/health
  qualification, context ladder on the exact digest, MTP A/B grid, restart +
  reboot recovery, scoped endpoint + boundary proof, catalog registration,
  consumer-proof task, configuration.md, acceptance reconciliation.
- Out of scope: any DeepSeek Harness deployment or registration; fleet rollout;
  fine-tuning/training; the Coder sibling (a different checkpoint — deliberate
  non-selection, D3); exposure beyond the LAN boundary; model quality claims
  transferred from other models (CX-R13).
- Constraints: per-milestone work orders; one bounded correction per failed
  correctable gate; per-cycle reboot approvals (D6); commits only with
  per-instance owner approval (Alert 2, 2026-08-26).

## Owner decisions

- D1: model store per the HX-1 blueprint (root ext4) (2026-08-26).
- D2: endpoint allowlist = the entire fleet 192.168.50.0/24 — AND the same fleet
  access must hold on hxs-1 ("if not, fix it", 2026-08-26): hxs-1's loopback-only
  posture is superseded by owner directive; a bounded exposure change
  (bind + LAN boundary + proof) was executed on hxs-1 (state log rows 71–73).
  **No host firewall anywhere** (owner rule 2026-08-26): services bind to the LAN;
  the private /24 itself is the boundary. Earlier ufw-based staging is void.
- D3: model = `mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M` (CoderX, top-8,
  REAP/DERN prune; the directive's literal `…-coder:` tag is the sibling — a
  different checkpoint, deliberately not selected) (2026-08-26).
- D4: Wi-Fi formalized into an rfkill soft block, boot-persisted, same as hxs-1
  (2026-08-26).
- D5: operating context = 65,536 (64K) — decided 2026-08-26; the M6 ladder
  validates 32K (baked) then 64K on the exact digest before M6b freezes it.
- D6: cold reboots at M7 pre-approved (per-cycle within a governor-announced
  window, hxs-1 precedent) (2026-08-26).
- D7: DoD re-scope (Harness-free mapping) ratified 2026-08-26.
- D8: vision disposition deferred by owner ("a concern for another day",
  2026-08-26) — vision probes run and report evidence at M5; any shortfall's
  disposition is a future owner decision, not a pilot blocker.

## Success conditions and evidence

| ID | Property | Measurement / procedure | Expected result | Evidence | Verifier |
| --- | --- | --- | --- | --- | --- |
| SC-01 | Model identity frozen | explicit tag + full local digest, capabilities, projector, template, license | Exact approved artifact recorded (vision-Q4_K_M, ~16.1 GB + ~447M CLIP, Apache-2.0) | model evidence, ollama show | KK3 gate |
| SC-02 | GPU placement | `ollama ps` + per-GPU telemetry under load | Both 5060 Ti allocated; no unapproved CPU fallback | GPU telemetry | KK3 gate |
| SC-03 | Runtime profile | context ladder on exact digest (32K → 64K with evidence); MTP A/B grid | Operating profile frozen with capacity + latency evidence; draft_num_predict chosen at stable plateau | capacity record | KK3 gate |
| SC-04 | Boot recovery | service restart + 3 cold reboots | Model resident and ready each time within budget, no manual action | reboot evidence | KK3 gate |
| SC-05 | Workload quality | native-defaults coding/tool suites + vision probes + termination budget | Owner-confirmed thresholds met | suite results | KK3 gate |
| SC-06 | Exposure boundary | bind config (0.0.0.0, loopback preserved), reachability from /24, refusal from non-authorized source where testable; **no host firewall** (owner rule 2026-08-26 — earlier ufw wording void) | Reachable inside 192.168.50.0/24; refused outside; no external interface; the LAN itself is the boundary | security evidence | KK3 gate |
| SC-07 | Capability registration | catalog backend-capability record + retrieval package + consumer-proof task via work order | Record live; task completes end-to-end over the endpoint with evidence | catalog record, task evidence | KK3 gate |
| SC-08 | Process | sanitized packages, Carol receipts, acceptance reconciliation | Complete packages; KK3 final gate; owner sign-off | pilot record | Agent-Zero |

## Execution controls

- Pre-flight (intake existence check): DONE 2026-08-26 — baseline from
  `servers/hxs-2/discovery.md` + post-directive driver validation (records);
  live re-verification at M1.
- Active charters reviewed: rick, john, kimi-k3, carol (all active).
- Maximum iterations: 1 initial specialist run + 1 bounded correction per
  failed correctable gate.
- Stop conditions: safety, authority, model-identity, or repeated failure —
  immediate escalation.
- Rollback / containment: smallest affected layer (hxs-1 13-esme pattern).
- HITL checkpoints: M0 authorization, Gate 0 decisions, each cold reboot,
  vision/threshold confirmations, final sign-off.

## Notes and links

- KDDs: KDD-0006 (adoption). Playbook: PILOT-HX1-OLLAMA-QWEN27B-001 (pattern
  source; second validated use). Knowledge reference:
  `agent-zero-docs/pilots/hxs-2/codex_20260825_1917_qwen3.6-27b-a3b-coderx-agent-knowledge-reference.md`.
- Controlling sources: `/opt/tkv-local/servers/hxs-2/` (historical as-found,
  cross-check), `/opt/tkv-local/ollama` (john's knowledge gate), catalog
  retrieval package (M1), this file's owner decisions.
- Second Brain evaluation (standing directive): catalog becomes the factory's
  backend-capability registry (new record class, implemented M8); hxs-1
  playbook promoted toward a formal pattern (second use); retrieval package
  at M0/M1. Harness-era registration deferred (substrate does not exist).
