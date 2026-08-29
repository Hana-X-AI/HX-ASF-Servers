# KDD-0008: Adopt Trinity as OmniRoute lifecycle engineer (candidate)

- Date: 2026-08-27
- Status: **ratified 2026-08-27** — owner decision O1 (adopt as corrected); Trinity's lane is ACTIVE (Layer 1 still requires OD-12 + OD-03)
- Decider: Agent-Zero
- Related goals: 2026-08-27-omniroute-trinity-layer0
- Truth-state: roster, governance, and correction claims [AUTHORITY]; candidate
  documents [CANDIDATE — not ratified authority, preserved unchanged]; option
  trade-offs [INFERENCE — labeled]
- Provenance: candidate inputs (preserved unchanged) —
  `/home/hxsa/opt/local-tkv/agent-zero-docs/pilots/omniroute/agent/codex_20260826_1508_trinity-expert-omniroute-engineer-steward-agent-profile.md`,
  `/home/hxsa/opt/local-tkv/agent-zero-docs/pilots/omniroute/plan/codex_20260826_1548_omniroute-v3.8.51-full-capability-phased-implementation-plan.md`,
  `/home/hxsa/opt/local-tkv/agent-zero-docs/pilots/omniroute/plan/codex_20260826_1548_omniroute-v3.8.51-implementation-control-manifest.yaml`.
  Full reconciliation: `pilots/PILOT-OMNIROUTE-LAYER0-001/03-trinity-adoption-assessment.md`.
  Drafts under decision: `agents/trinity/charter.md`, `agents/trinity/profile.md`
  (both **candidate — not ratified authority**).

## Context

p11 (owner directive, 2026-08-27) commissioned Layer 0 of the OmniRoute program
with Wave 0A producing a Trinity adoption packet: reconciliation report,
charter draft, corrected profile draft, and this KDD. The candidate material is
a 1,229-line operating profile plus a phased plan and control manifest prepared
by codex on 2026-08-26 against the OmniRoute v3.8.51 corpus.

The roster today is kimi-k3 (orchestration), rick (Ubuntu OS), john (Ollama),
carol (knowledge) — Trinity is absent (`agents/README.md`; verified at the M0
gate, state log row 1). The OmniRoute lane is empty and the surface is large:
13,098 corpus files and 102 API domains (DOC-tkv-corpus-omniroute; manifest
`api_domains.expected_count`).

Governor verification found the candidate documents conflict with current
authority in seven places. The reconciliation register (assessment §3, C1–C7)
is applied to the drafts, not re-litigated:

| Code | Candidate claim | Corrected authority | Evidence |
| --- | --- | --- | --- |
| C1 | Knowledge root `/opt/tkv-local/omniroute` | Corpus `/opt/tkv-local/OmniRoute-release-v3.8.51` (DOC-tkv-corpus-omniroute); `knowledge/catalog/` canonical; Carol owns catalog mutations | KDD-0005; AGENTS.md amendment 2026-08-25 |
| C2 | "DeepSeek Harness" execution foundation | Never existed; mapped to KK3-orchestrated subagent sessions (the factory's execution substrate) | KDD-0006 (owner-confirmed 2026-08-26) |
| C3 | "Cipher" / "Independent QA" roles | Mapped to the p11 verifier contract: deterministic checks → Qwen-X (independent local model, ACTIVE, M8-signed) → owner review | Goal contract authority matrix |
| C4 | Host-firewall controls | No host firewalls anywhere (owner rule 2026-08-26); boundary is the 192.168.50.0/24 LAN | AGENTS.md; BLUEPRINT-llm-server.md §5 |
| C5 | Target host NOT-ESTABLISHED (manifest OD-01) | hxs-8 selected by the owner; online; readiness ack is OD-03 | Goal OD-01; state log row 1 |
| C6 | Broad "100% accountability" scope | Lane = OmniRoute lifecycle engineering only; explicit exclusions (orchestration, own-work acceptance, other lanes, subordinate agents, agent-like feature expansion) | Register item 6; goal authority matrix |
| C7 | Execution/verification via Harness / Independent QA | Coder-X primary execution backend (per-task identity/health verification, stop-and-escalate, no cloud substitution ever); Qwen-X independent verifier | Register item 7; state log row 1 |

One honesty limit rides with the adoption: the candidate's pinned upstream
commit is CANDIDATE-claimed provenance — the corpus is not a git checkout and
upstream commit identity is unavailable (DOC-tkv-corpus-omniroute notes). The
drafts carry it as unverified.

**Resolution 2026-08-27: this honesty limit is CLOSED.** The snapshot's identity
was VERIFIED by content-sensitive proof — 13,098/13,098 files git-blob identical
to upstream `diegosouzapw/OmniRoute@42a13fedef8b…` (pilot log row 6;
`pilots/PILOT-OMNIROUTE-LAYER0-001/07-source-provenance-receipt.md`). The
drafting-time carry above stands as history.

## Options considered

1. **Adopt-as-corrected** (recommended) — ratify the charter and profile
   drafts as produced, add trinity to the roster (vertical), record this KDD as
   ratified. The corrections are governor-verified and already applied; the
   lane is empty; the candidate's operating discipline (startup receipt,
   rollback-first, two-person integrity, conformance suites, stop conditions)
   matches factory standards. Cost [INFERENCE]: owner review effort now;
   candidate product claims remain CANDIDATE-labeled until source-grounded
   verification under commission.
2. **Adopt-with-changes-specified** — ratify with a written amendment list
   recorded in this KDD (e.g., different lane bounds, different backend or
   verifier designation). Same mechanics as option 1 plus the amendments.
   Cost [INFERENCE]: amendments re-open reconciliation work already verified;
   use only where the owner wants materially different bounds.
3. **Defer** — hold the candidate; revisit after Layer 0 closes (capability
   ledger, program packet). Cost [INFERENCE]: Layer 1 design work would have no
   accountable engineering lane; deferral buys no new evidence because the
   corrections are already verified and applied.
4. **Reject** — discard the candidate; OmniRoute engineering stays with the
   governor. Cost [INFERENCE]: concentrates a 102-domain traffic-plane surface
   in the orchestration lane, against KK3's own charter bar on direct
   installation and configuration execution; discards a prepared discipline
   corpus that survives correction intact.

## Decision

**DECIDED 2026-08-27 — owner chose RATIFY option 1 (adopt as corrected):** "if so I
ratify as corrected (O1). You may proceed." The governor executed the gate
(roster row, charter/profile active, this KDD ratified; pilot state log row 5).
The decision that was required from Agent Zero (goal OD-02, now closed) was:

Choose one, in writing (a reply naming the option suffices; the governor
records it here and in the goal contract):

- **RATIFY option 1** — approve `agents/trinity/charter.md` and
  `agents/trinity/profile.md` as drafted; authorize the governor to add trinity
  to `agents/README.md` (vertical, status active) and flip this KDD to
  ratified; or
- **RATIFY option 2** — same, plus the owner's amendment list, which the
  governor applies to the drafts before roster admission; or
- **DEFER (option 3)** — name the re-entry trigger; the drafts stay
  candidate-labeled and inert; or
- **REJECT (option 4)** — record the reason; the governor removes the drafts
  and Carol records the rejection disposition for the candidate documents.

Until this decision, Trinity remains a candidate: no roster entry, no work
orders, no activation. Ratification activates the lane only — Layer 1 (any
installation or host mutation) still requires separate owner authorization
(OD-12) and hxs-8 readiness acknowledgement (OD-03).

## Consequences

Enables: an accountable, bounded engineering lane for the OmniRoute traffic
plane; Layer 1 design work under work orders once authorized; the
adoption-gate pattern (candidate → reconciliation → charter/profile/KDD → owner
ratification → catalog → roster) validated as the reusable path for future
specialists; the Coder-X execution + Qwen-X verification contract exercised on
a standing lane.

Forecloses: `/opt/tkv-local/omniroute` as a knowledge root and any duplicate
catalog; any DeepSeek Harness dependency; Trinity-instantiated subordinate
agents or pre-qualified specialist cells as roster entities; Trinity
self-acceptance; unapproved enablement of OmniRoute agent-like, memory,
workflow, or process-spawning features; cloud-model substitution for Coder-X.

Rollback: adoption is reversible. To unwind: remove `agents/trinity/`, revert
the `agents/README.md` roster row, flip this KDD to superseded or rejected, and
have Carol record the disposition. Adoption itself touches no host, service,
network, credential, or infrastructure state; Layer 0 is read-only, so rollback
is a documentation-only operation.

Revisit if: the owner changes the traffic-plane scope, the verifier contract,
or the execution-backend designation; OmniRoute agent-like features are
proposed for enablement (separate decision required); or the corpus identity
changes (re-hash per DOC-tkv-corpus-omniroute review_due 2026-09-24).
