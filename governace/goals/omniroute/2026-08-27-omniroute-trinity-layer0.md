# Goal Contract: Trinity adoption review + OmniRoute v3.8.51 Layer 0 program foundation

- Goal ID: 2026-08-27-omniroute-trinity-layer0 (this file's name)
- Version: 1
- Status: in-progress — Layer 0 (M0 authorized 2026-08-27 by p11 + approved plan `red-star-stargirl-kamala-khan` Option A)
- Status transition 2026-08-27 **[current]**: **LAYER 0 COMPLETE — PASS** (KK3 gate decision `19-kk3-gate-decision.md`; handoff catalog-closed; owner OD-12 then authorized Layer 1 — see goal `2026-08-27-omniroute-layer1-secure-core`). [open correction 2026-08-27: the original in-progress status is preserved above per the append-only convention]
- Owner: Agent Zero
- Created: 2026-08-27
- Human authority: Agent Zero
- Agent lane(s): kimi-k3 (governor/orchestrator), trinity (**active** 2026-08-27 — OmniRoute lifecycle steward, owner-ratified KDD-0008 O1), rick (host readiness, read-only), carol (catalog), Coder-X (bounded execution backend), Qwen-X (independent local verifier)

## Intent

Establish the governed foundation for Trinity's adoption and for OmniRoute
v3.8.51's later phased implementation — correct, reproducible, reviewable —
NOT to install OmniRoute quickly. Layer 0 produces: reconciled authority,
Trinity adoption packet (charter/profile/KDD drafts, candidate state),
source provenance receipt with honest identity limits, source-derived
capability ledger, reconciled program packet with owner-decision register,
independent verification, and the KK3 gate decision. Completion does not
authorize Layer 1.

## Scope — authorized (p11 §Layer 0 execution contract)

- Read-only governance and source review; source inventory and content hashing
- Capability-ledger generation; contradiction and risk analysis
- Trinity charter/profile/KDD proposal drafting
- Goal/work-order/context-packet/evidence-contract/owner-decision drafting
- Deterministic validation of created documents and schemas
- Independent local review of produced artifacts (Qwen-X; deterministic first)
- rick's read-only hxs-8 post-upgrade readiness assessment (owner acknowledges)
- Carol handoff preparation and catalog receipts

## Scope — prohibited (p11 non-negotiables, all enforced)

No OmniRoute install/start/deploy; no package/build/migration/compose/container/service-start commands; no host/runtime/service/network/DNS/TLS/firewall/credential/database/backend mutation; no OmniRoute management or inference endpoint; no remote providers or provider credentials; no workload on hxs-cp; no hxs-8 substitution; no host-dependent work before readiness + owner acknowledgement; no Trinity-active before the adoption gate; no verbatim candidate adoption; no provenance claims beyond content-sensitive proof; no duplicate Second Brain/catalog/registry; no `/opt/tkv-local/omniroute`; no OmniRoute agent-like/memory/A2A/ACP/MCP/skills/plugins/pipelines/fusion/remote-management/tunnels/embedded-services/process-execution enablement; no Trinity-instantiated subordinate agents or recursive delegation; no hidden failed checks or NOT-ESTABLISHED states; no Layer 1 without a new explicit owner authorization; no cloud models or remote inference anywhere (local-model-only boundary); no secrets in any artifact or model context.

## Authority matrix

| Role | Owns | Does not own |
| --- | --- | --- |
| Agent Zero | intent, final authority, Trinity ratification, hxs-8 selection/placement, Layer-1+ authorization, high/critical risk acceptance | — |
| KK3 (governor) | authority validation, Goal Contracts, decomposition, work orders, budgets, sequencing, state transitions, evidence gates, convergence, recovery, escalation, final recommendation; preventing second control planes | physical deployment approval |
| Trinity (**active** 2026-08-27, KDD-0008 O1) | bounded OmniRoute lifecycle engineering under issued work orders (source review, install/config DESIGN, conformance design, resilience/persistence/observability/upgrade/rollback/incident/ops evidence, handoff completeness) | orchestration, acceptance of own work, unrelated lanes, subordinate agents, agent-like feature expansion |
| rick | hxs-8 readiness evidence (read-only) | host mutation |
| john | (not engaged in Layer 0) | — |
| carol | catalog mutations, receipts, freshness | — |
| Coder-X (backend) | bounded execution: source-grounded planning, bounded source analysis, capability-ledger preparation, document/schema drafting | identity/authority; cloud substitution; unsuitable tasks (stop-and-escalate) |
| Qwen-X (verifier) | independent local review of produced artifacts | producing what it certifies |

## Layer map (entry/exit gates)

- **Layer 0 — Foundation** (this contract): authority reconciled, Trinity adoption packet, provenance receipt, capability ledger, program packet, independent verification, KK3 gate. Exit: owner review of the handoff + explicit Layer 1 authorization.
- **Layer 1 — Secure Core Gateway**: pinned runtime, persistence, authN, encrypted secrets, ONE local backend, protocol baseline, health, backup, rollback. Entry: owner authorization after Layer 0 + hxs-8 readiness acknowledged. [open correction 2026-08-27: "ONE local backend" is superseded — owner OD-08 (amended 2026-08-27, state log row 32) requires ALL FOUR HX backends registered from the start, with Chat-X's parity posture-blocked as an approved exception; see goal `2026-08-27-omniroute-layer1-secure-core` OD-08]
- **Layer 2 — Governed Routing & Resilience**: approved backends, curated routes/combos, strategy characterization, quotas/budgets/sessions/failover/telemetry. Entry: Layer 1 gate passed + owner authorization.
- **Layer 3 — Intelligence, Quality & Modalities**: compression/cache/guardrails/eval/search/retrieval/memory characterization. Entry: Layer 2 gate + owner authorization; memory/Qdrant disposition decided.
- **Layer 4 — Agent & Ecosystem Integration**: scoped MCP/A2A/ACP, skills/plugins, remote ops, sidecars. Entry: Layer 3 gate + owner authorization; control-plane collisions isolated/disabled by design.

## Owner-decision register (state at M0)

| ID | Decision | State |
| --- | --- | --- |
| OD-01 | Target host | **DECIDED — hxs-8** (owner; readiness assessment evidence to be acknowledged) |
| OD-02 | Trinity ratification (roster admission) | **DECIDED — ratified O1 (adopt as corrected) 2026-08-27; lane ACTIVE (row 5)** |
| OD-03 | hxs-8 post-upgrade readiness acknowledgement | **DECIDED — acknowledged 2026-08-27 ("Looks Good")** |
| OD-04 | Deployment mode | **DECIDED 2026-08-27 — native Node systemd service; never Docker (owner rule)** |
| OD-05 | FQDN + internal DNS | OPEN — Layer 1 |
| OD-06 | TLS termination + path separation | OPEN — Layer 1 |
| OD-07 | Allowed clients / exposure scope | OPEN — Layer 1 (no host firewalls — owner rule; /24 LAN + OmniRoute authn/authz governs) |
| OD-08 | Initial backends behind the gateway | **DECIDED AMENDED 2026-08-27 — ALL FOUR HX backends (Qwen-X, Coder-X, Meta-X, Chat-X); routing confirmation is a first-class acceptance test** |
| OD-09 | Retention, RPO/RTO, backup policy | OPEN — Layer 1 |
| OD-10 | Qdrant / memory disposition | OPEN — Layer 3 (existing-service designation candidate per plan) |
| OD-11 | Production-version policy (pre-LTS baseline) | OPEN — program-level |
| OD-12 | Layer 1 authorization | **AUTHORIZED 2026-08-27** |

Unknown owner decisions do not stop planning; they block the work that depends on them.

## Success criteria (Layer 0 acceptance, per p11 §validation)

Trinity roster state accurate; candidates reconciled not copied; Coder-X identity/status/endpoint/profile/health/limits verified; no cloud or remote inference; source identity with honest provenance limits; source instructions/metadata/lockfile/license reviewed; capability ledger reproducible from exact references; every capability owned/risked/tested/dispositioned; owner decisions carry blocking boundaries; zero mutations; hxs-8 recorded truthfully; zero secrets in any artifact or model context; repo validation green; independent verification complete and separate from production; Carol receipt cited; KK3 gate recorded; Agent Zero receives the exact decisions for Trinity ratification and any Layer 1 authorization.

## Stop and escalation

Per p11 §stop: governance conflict with candidates; Trinity lane overlap unresolvable; Coder-X identity/health/capability unestablished; no independent local verifier; source identity untieable to content-sensitive proof; evidence would expose a credential; work would require mutation; hxs-8 needed before readiness; target substitution proposed; scope beyond Layer 0; high/critical risk needing acceptance; validation fails after one bounded correction; second-control-plane proposal. Structured escalation packet to Agent Zero.

## Second Brain evaluation (standing directive)

1. Opportunity identified: **yes** — a new capability-plane program (traffic plane) entering the governed catalog; Trinity is a new roster lane; the capability ledger is catalog-native knowledge by design.
2. Roadmap capability/pattern: the adoption-gate pattern (candidate → charter/profile/KDD → owner ratification → catalog → roster) becomes the reusable path for future specialists; the backend-as-execution + independent-verifier contract is a Second Brain capability-use pattern.
3. Disposition: **implemented in this contract** — the ledger, receipts, and catalog waves are built in; nothing extra commissioned.
4. Evidence/reasoning: recorded per wave in the pilot state log and Carol receipts.

<!-- Machine-readable current state (O1, work-state.schema.yaml). The prose
     above is the historical record and is never rewritten; this block is the
     single source every status tool reads. -->

```yaml work-state
id: 2026-08-27-omniroute-trinity-layer0
status: complete
status_date: 2026-08-27
authority: >-
  Status transition 2026-08-27 [current]: LAYER 0 COMPLETE — PASS (KK3 gate decision 19-kk3-gate-decision.md; handoff catalog-closed; owner OD-12 authorized Layer 1)
reconcile: none
```
