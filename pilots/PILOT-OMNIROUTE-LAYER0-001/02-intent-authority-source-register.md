# Intent & Authority Receipt + Authoritative Source Register — Wave 0A

| Field | Value |
| --- | --- |
| Program | Trinity adoption review + OmniRoute v3.8.51 Layer 0 (PILOT-OMNIROUTE-LAYER0-001) |
| Date | 2026-08-27 (UTC) |
| Governor | Kimi-K3 (control plane) |
| Owner directive | p11 (`/home/hxsa/opt/local-tkv/agent-zero-docs/prompts/p11.md`, read 2026-08-27) |
| Plan | `red-star-stargirl-kamala-khan` — Option A approved (full Layer 0 in gated waves) |
| Goal Contract | `goals/2026-08-27-omniroute-trinity-layer0.md` |

Truth-state labels: FACT / AUTHORITY / CANDIDATE / INFERENCE / NOT-ESTABLISHED.

## 1. Intent and authority receipt (AUTHORITY)

- p11 authorizes **Trinity adoption review and Layer 0 program-foundation work only** — no deployment, installation, mutation, exposure, provider activation, or Layer 1+ progression (p11 §1, §Non-Negotiable Boundaries).
- Owner selections recorded: **hxs-8** as the OmniRoute target (OD-01 decided); **Coder-X** as Trinity's primary execution backend; local-model-only boundary for all program inference.
- p11's stale premise corrected at the gate (FACT): hxs-8 is **online** (ping 1.1 ms, SSH open; owner session 2026-08-27T01:26Z; discovery updated 16 → 46 GiB) — recorded as returned, readiness assessment commissioned to rick (read-only), owner acknowledgement still required before any host-dependent work.
- Trinity roster state (FACT): **absent** from `agents/README.md` (roster: kimi-k3, john, rick, carol). She is a **candidate**; nothing in this program activates her before the p11 adoption gate (charter+profile agree, no lane overlap, Coder-X/verifier bounded, no candidate doc mistaken for authority, owner approval, Carol catalogs, roster updated).

## 2. Authoritative source register (the ratified split)

| Source | Role | State |
| --- | --- | --- |
| `goals/2026-08-27-omniroute-trinity-layer0.md` | Goal Contract (this program's spine) | AUTHORITY (this program) |
| `AGENTS.md`, `agents/README.md`, `agents/*/charter.md` | roster + governance truth | AUTHORITY |
| `governace/decisions/KDD-0001..0007` | ratified decisions (incl. KDD-0006: the DeepSeek Harness never existed) | AUTHORITY |
| `servers/BLUEPRINT-llm-server.md` | LLM-server contract incl. §5 boundary (no host firewalls; /24 LAN) and §8 capability table | AUTHORITY |
| `knowledge/catalog/` (245 records, validator 4/4) | canonical governed catalog (Carol-owned) | AUTHORITY |
| `/opt/tkv-local/OmniRoute-release-v3.8.51` | OmniRoute source snapshot (13,098 files, package 3.8.51, no .git) — **read-only this program** | PRIMARY SOURCE (read-only) |
| `/opt/tkv-local/OmniRoute_old/` | prior wrapper: 4 HX evaluation docs (cataloged DOC-tkv-omniroute-hx-evaluation) + nested duplicate of v3.8.51 + hidden v3.8.50 backup | HISTORICAL EVIDENCE |
| `agent-zero-docs/pilots/omniroute/{agent,plan}/` (3 docs) | Trinity candidate profile (1,229 lines), phased plan (1,268), control manifest (443) | CANDIDATE — review input, preserved unchanged |
| `github.com/diegosouzapw/OmniRoute` @ `release/v3.8.51`, `omniroute.online` | public upstream for commit verification attempts (manifest-declared) | EXTERNAL REFERENCE |
| `/opt/tkv-local/omniroute` | **REJECTED as a knowledge root** (p11 non-negotiable + ratified split) | NOT TO BE CREATED |

## 3. Candidate-document reconciliation register (AUTHORITY-corrected, governor-verified)

1. `knowledge_root: /opt/tkv-local/omniroute` → **rejected**; corpus path above + canonical catalog.
2. "DeepSeek Harness as execution foundation" → **never existed** (owner 2026-08-26, KDD-0006); all references map to KK3-orchestrated subagent sessions.
3. Unrostered roles ("Cipher", "independent QA") → mapped to the p11 verifier contract (deterministic → Qwen-X → owner).
4. "Firewall default deny + allowlist" → **owner rule: no host firewalls**; boundary = 192.168.50.0/24 + OmniRoute authn/authz.
5. OD-01 target host NOT-ESTABLISHED → **decided: hxs-8**; readiness supersedes via rick + owner ack.
6. Reported commit `42a13fedef8b…` → **REPORTED, not verified locally** (no .git); content-sensitive verification attempted in Wave 0B against the public upstream; labeled honestly either way.

## 4. Local-model identity and health receipts (FACT, 2026-08-27T03:5xZ probes)

| Role | Call-sign | Host/endpoint | Profile alias | Digest | Health evidence | Limits/notes |
| --- | --- | --- | --- | --- | --- | --- |
| Execution (owner-designated) | **Coder-X** | hxs-2 / `http://192.168.50.201:11434` | `hx-qwen3.6-coderx-64k` (operating) | `ec9ebe08a824…` | 0.32.15; restored resident via frozen preload path (F-M5-1 class eviction 01:45Z — interactive-load fit; pin re-asserted, size==size_vram, ctx 65536); 0 `:cloud` tags | catalog status `candidate` (M8 pending owner); per-task re-verification; stop-and-escalate; NO cloud substitution |
| Independent verifier | **Qwen-X** | hxs-1 / `http://192.168.50.200:11434` | `hx-qwen3.8-27b-64k` (operating) | `766cd9469fb4…` | 0.32.15; resident (size==size_vram, ctx 65536); 0 `:cloud` tags; ACTIVE, M8-signed | produces nothing it certifies; disagreement resolved by discriminating evidence |

Alternate for structured checks: Meta-X (ACTIVE, tooling). Excluded: Chat-X (parked posture; A-1 class). Local-model-only compliance: every model-assisted task records call-sign/endpoint/alias/identity/role; no cloud or remote inference anywhere; no credentials into model context.

## 5. Wave 0A in-flight register

- Trinity adoption drafting (assessment, charter/profile drafts, KDD-0008): background session, governor-briefed with the reconciliation register.
- rick hxs-8 post-upgrade readiness assessment (read-only): background session.
- Then: Wave 0A Carol catalog wave; owner gate — Trinity ratification (program continues regardless under KK3 + Coder-X).
