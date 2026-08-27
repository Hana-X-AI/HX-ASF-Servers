# Reconciled Program Packet — Trinity + OmniRoute v3.8.51 (Wave 0C)

| Field | Value |
| --- | --- |
| Date | 2026-08-27 (UTC) |
| Program | PILOT-OMNIROUTE-LAYER0-001 (p11) |
| Author | Kimi-K3 (governor) |
| Basis | Goal Contract (OD register), adoption packet (KDD-0008 ratified O1), source provenance receipt (identity VERIFIED), capability ledger (367 entries, 8 partitions, all governor spot-checked), hxs-8 readiness evidence, the week's state logs |
| Verdict line | The foundation is complete and defensible: authority reconciled, source identity proven, capabilities inventoried with dispositions, verifier independent, zero mutations, zero cloud, zero secrets. Layer 0 is ready for the KK3 gate and the owner's review. |

## 1. Executive verdict per candidate artifact

| Candidate artifact | Verdict | Why |
| --- | --- | --- |
| Trinity profile (1,229 lines) | **ADOPT-AS-CORRECTED** — ratified O1 2026-08-27 (KDD-0008) | lane empty; conflicts were documentation-level; 7 register corrections applied; rollback is documentation-only |
| Phased implementation plan (1,268 lines) | **REVISE** — structure adopted, assumptions corrected | the 4-layer map is sound and kept (§7); its Harness/roles/firewall/knowledge-root assumptions were wrong (corrected per the register); counts and states now source-verified where checkable (19 strategies exactly; provider counts corrected) |
| Implementation control manifest (443 lines) | **REVISE** — re-issued corrected (`10-control-manifest.yaml`) | completion semantics and OD structure kept; Harness-free, corpus-true, no-host-firewall, roster-true roles; OD-01 decided; OD-02..12 tracked with blocking boundaries |

## 2. Authority matrix (final)

| Role | Owns | State |
| --- | --- | --- |
| Agent Zero | intent, final authority, Trinity ratification (done O1), hxs-8 (decided), Layer-1+ authorization, high/critical risk acceptance | ACTIVE |
| Kimi-K3 | orchestration, Goal Contracts, decomposition, work orders, budgets, gates, convergence, escalation, final recommendation; preventing second control planes | ACTIVE |
| Trinity | bounded OmniRoute lifecycle engineering under work orders (this ledger was her first) | ACTIVE (lane) |
| rick | host OS plane; hxs-8 readiness evidence (delivered) | ACTIVE |
| john | (not engaged in Layer 0) | ACTIVE |
| Carol | catalog mutations, receipts, freshness (11 waves this program) | ACTIVE |
| Coder-X | bounded execution backend (identity/health per-task verified; candidate status until its M8) | CANDIDATE-backend |
| Qwen-X | independent local verifier (ACTIVE, M8-signed) | ACTIVE |
| Unfilled | none material at Layer 0 (Cipher/QA were mapped to the verifier contract) | — |

## 3. Source-truth matrix

| Item | State |
| --- | --- |
| Local source | `/opt/tkv-local/OmniRoute-release-v3.8.51`, 13,098 files, read-only throughout |
| Package/branch | `3.8.51` / `release/v3.8.51` (upstream DEFAULT branch) — VERIFIED |
| Commit | `42a13fedef8b…` — **VERIFIED by content-sensitive proof** (13,098/13,098 git-blob identical); branch head since moved to `c9f11d86b55d` (snapshot pinned, documented) |
| Manifest/lockfile/package hashes | `085fb94b…` / `58a9d071…` / `fe6c7dbe…` |
| License | MIT |
| Node engines | `>=22.22.2 <23 \|\| >=24.0.0 <27` — hxs-8 has none (the single Layer-1 dependency) |
| Unresolved provenance | none for identity; bundled-doc drift recorded in the ledger's drift register |

## 4. Architecture boundary (ratified)

KK3 is the control plane (sole orchestrator). OmniRoute, when deployed, is a bounded model-traffic plane — never an orchestrator, never a knowledge authority, never an execution foundation. Local backends (Qwen-X, Coder-X, Meta-X, Chat-X) are capabilities with recorded identities and limits. The catalog (Carol) is the only knowledge authority. Trinity engineers OmniRoute's lifecycle under KK3 work orders and accepts nothing she produces. Agent-like OmniRoute surfaces (MCP/A2A/ACP/Conductor/copilot/tunnels/cloud agents) are disabled-by-default, collision-noted per entry, and blocked wherever they collide with owner rules.

## 5. Owner-decision register (state at Wave 0C)

| ID | Decision | State |
| --- | --- | --- |
| OD-01 | Target host | **DECIDED — hxs-8** (online, readiness evidence delivered) |
| OD-02 | Trinity ratification | **DECIDED — O1 adopt-as-corrected** (active) |
| OD-03 | hxs-8 readiness acknowledgement | OPEN — evidence in `04-rick-hxs8-readiness.md`; owner's ack required before host-dependent work |
| OD-04 | Deployment mode | OPEN — recommendation: native Node service (systemd) over container for Layer 1 (fewer moving parts on a clean host; container flavor carries a BLOCKED variant) |
| OD-05 | FQDN + internal DNS | OPEN — Layer 1 |
| OD-06 | TLS termination + path separation | OPEN — Layer 1 |
| OD-07 | Allowed clients/exposure | OPEN — recommendation: bind LAN only, management endpoints behind OmniRoute's own authN/authZ (the proven proxy.ts pipeline), no host firewall (owner rule); O1 monitoring tripwire stands |
| OD-08 | Initial backends behind the gateway | OPEN — recommendation: exactly one local backend first (Qwen-X, ACTIVE) per the plan's Secure Core shape; others added per layer |
| OD-09 | Retention/RPO/RTO/backup policy | OPEN — **with the ledger's finding that backup encryption and remote upload are effectively nonexistent** (write-only encryption, dead --cloud endpoint): plan plaintext-snapshot backups + our own encryption if needed |
| OD-10 | Qdrant/memory disposition | OPEN — Layer 3 (memory engine is catalog-collision-noted) |
| OD-11 | Production-version policy (pre-LTS) | OPEN — snapshot pinned at 42a13fe; upgrade policy per release with re-verification |
| OD-12 | Layer 1 authorization | OPEN — after this packet + the KK3 gate |
| OD-13 | **Secrets at rest** (new, from the ledger) | **RATIFIED 2026-08-27**: env-provision `JWT_SECRET` + `API_KEY_SECRET` and set `STORAGE_ENCRYPTION_KEY` at install; never accept defaults |

Unknown owner decisions block only the work that depends on them (all Layer-1+).

## 6. Risk register (top, with evidence pointers)

| Risk | Class | Mitigation on record |
| --- | --- | --- |
| Plaintext secrets at rest (CAP-P4-039/P5-030) | security — critical | OD-13 ratified (env-provision + encryption key) |
| Copilot LLM driver executes model output as host CLI (CAP-P7-053) | security — critical | disabled-by-default; LOCAL_ONLY tier; HX install keeps it off |
| Backup encryption write-only + dead --cloud (CAP-P8-905/906) | data-integrity | treat as nonexistent (OD-09); our own snapshot+encryption if required |
| Authority collision surfaces (Conductor hub, cloud agents, MCP write tools, tunnels) | authority | disabled-by-default; 8 BLOCKED entries; KDD-0008 lane bounds |
| Skills execution + background jobs not code-disabled | authority | explicit deployment settings at Layer 1 (OD-04 config) |
| Provider-doc drift (counts, strategies, encrypted-store claim) | knowledge | drift register in the ledger; source outranks docs |
| Protocol loss for Meta-X (no ATEM adapter) | capability | OpenAI-compatible path or future adapter (Layer 3/4) |
| Node runtime absent on hxs-8 | dependency | rick's readiness; install at Layer 1 within engines range |
| Rate-limit fail-open classes (Redis-outage client-key, quota engine) | resilience | documented; accept or configure at Layer 2 |
| Restart/migration (160 migrations, convergent restart) | operations | proven design; snapshot before upgrade (OD-11) |
| Pre-LTS product posture | compatibility | pre-LTS characterization baseline; characterization evidence from this ledger governs acceptance |
| Snapshot age vs upstream head | currency | pinned + documented; upgrade decisions per OD-11 |

## 7. Layer map (entry/exit gates, reconciled)

- **L0 Foundation (this program) — COMPLETE pending the KK3 gate.** Exit: owner review + explicit L1 authorization.
- **L1 Secure Core Gateway** (pinned runtime, persistence, authN, encrypted secrets per OD-13, ONE local backend, protocol baseline, health, backup, rollback). Entry: OD-12 + OD-03 + Node present. Gate: direct/routed parity, restart, backup, rollback proofs.
- **L2 Governed Routing & Resilience** (approved backends, curated routes/combos, strategy characterization (19 verified), quotas/budgets/sessions/failover, telemetry). Gate: failure matrix + route policy pass.
- **L3 Intelligence, Quality & Modalities** (compression/cache/guardrails/eval/search/retrieval; memory characterization incl. OD-10). Gate: quality delta + data-boundary gates.
- **L4 Agent & Ecosystem Integration** (scoped MCP/A2A/ACP, skills/plugins, remote ops, sidecars) — the collision class; most surfaces stay disabled or blocked by design. Gate: the ledger's collision table closed entry-by-entry.

## 8. Local-model execution contract (final, as exercised)

Coder-X executed bounded analysis under per-task identity/health verification (0 identity failures; one eviction handled by re-verification, never substitution). Verifier independence held (producer hxs-2 ≠ verifier hxs-1). The owner-ratified citation contract (numbered excerpts + anchor citation + harness verification) took Coder-X's drafted-line error rate from 35.6% (P1 baseline) to **0.0% (P8)** — the contract is proven and is a Wave-0C skill candidate. Zero cloud anywhere; zero credentials in model context; every call recorded with call-sign/endpoint/alias/identity/role.

## 9. Test strategy (for later layers)

Direct-vs-routed protocol fixtures per capability's test_contract field (every ledger entry carries one); negative tests per the authn/authz split evidence (401 classes verified in source); persistence/recovery drills per P5's backup/restore/restart evidence; restart/reboot per the hxs-1/2/3 M8 pattern; upgrade/rollback per OD-11 snapshot policy; failure injection per P6's rate-limit semantics; built-artifact tests per P8's packaging gates. The deterministic-first rule stands: model output is advice until checks agree.

## 10. Rollback and containment strategy

No phase proceeds without a deterministic inverse and a bounded affected surface. Layer 0 itself is read-only (rollback = documentation-only, exercised zero times). For later layers: per-capability rollback_or_disable fields (all 367 entries carry one); snapshot-before-change per OD-11; the pre-restore snapshot + integrity_check pattern from P5's own evidence as the backup shape; stop conditions per work order with escalation to KK3; no silent fixes ever (every correction is labeled).
