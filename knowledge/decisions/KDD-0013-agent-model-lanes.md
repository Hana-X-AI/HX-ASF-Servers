# KDD-0013: Per-agent model lane assignments

- Date: 2026-08-28
- Status: ratified
- Decider: Agent-Zero
- Related goals: factory operating model; supersedes Trinity's KDD-0008-era
  Coder-X designation

## Context

The local-model-first rule (owner, 2026-08-27) requires the backend for each
task recorded with call-sign, endpoint, alias, identity, and role. In practice
only Trinity carried a standing designation (Coder-X primary, Qwen-X verifier,
KDD-0008); every other agent's inference defaulted to the kimi-k3 session
substrate. The owner closed this on 2026-08-28 by assigning each agent a
standing model lane directly, including Gordon (Qwen-X) and Mia (GLM 5.3
Flash), which he confirmed when asked.

## Options considered

1. Standing per-agent assignments recorded in profiles + roster + this KDD —
   what the owner directed.
2. Keep per-task recording only — rejected by the owner's directive; recurring
   lanes deserve standing records.
3. Uniform single backend for all agents — rejected; the assignments are
   deliberately per-lane (work class fit), and three lanes ride the ratified
   GLM exception.

## Decision

Standing model lanes, all local lanes routed via OmniRoute (hxs-8,
`192.168.50.207:20128`):

| Agent | Model lane | Notes |
| --- | --- | --- |
| Kimi-K3 | `moonshot-ai/kimi-k3` | Meta-agent exception (orchestration/governance only), unchanged |
| Morpheus | Coder-X (`ollama-local/hx-qwen3.6-coderx-64k`, hxs-2; immutable identity: manifest digest `ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1`, recorded 2026-08-28) | Verifier Qwen-X (hxs-1) |
| Gordon | Qwen-X (`ollama-local/hx-qwen3.8-27b-64k`, hxs-1; immutable identity: manifest digest `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a`, recorded 2026-08-28) | Deterministic oracles remain first-tool |
| Rick | Meta-X (`ollama-local/hx-muse-glimmer-64k`, hxs-3; immutable identity: manifest digest `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da`, recorded 2026-08-28) | Work class largely deterministic; lane covers analysis/drafting |
| John | Meta-X (`ollama-local/hx-muse-glimmer-64k`, hxs-3; same immutable identity as rick's row) | Same deterministic caveat as rick |
| Carol | Chat-X (`ollama-local/hx-qwen3.5-9b-64k`, hxs-4; immutable identity: manifest digest `5936a390c6c22594ce49e8c77187fc92f4a81126fd04a4eabad7c000b30447d2`, recorded 2026-08-28) | Schema/mechanical validation stays deterministic (validate.py); currently frozen by owner directive |
| Trinity | Z.ai GLM 5.3 Flash (`openrouter/z-ai/glm-5.3-flash`) | OD-14 exception; supersedes her Coder-X designation |
| Rob | Z.ai GLM 5.3 Flash | OD-14 exception; resolves his profile's D1 against its Coder-X recommendation — recorded openly |
| Mia | Z.ai GLM 5.3 Flash | OD-14 exception |

Controls carried into every profile: per-task identity/health verification;
stop-and-escalate on backend failure with re-assignment control at Kimi-K3; no
automatic substitution; cloud substitution prohibited except the three explicit
GLM assignments, which ride the OD-14 OpenRouter exception of record (USD 100
cap, owner-lane allowlist, metered via `usage_history`). Identity validation
FAILS CLOSED: the `:latest` tag is a mutable alias only — per-task verification
resolves the served model's manifest digest and compares it against the
immutable digest recorded in the table above (digests captured live from the
backends 2026-08-28); a mismatch, an unresolvable identity, or an unhealthy
endpoint stops the task before any inference and escalates to Kimi-K3.

## Consequences

- Every agent lane now has a standing backend record; the local-model-first
  rule's per-task recording continues on top of it.
- Trinity's KDD-0008-era Coder-X designation is superseded (preserved as
  history in her profile and charter); her verifier stays Qwen-X.
- GLM lanes (trinity, rob, mia) spend OpenRouter credit when their lanes
  perform inference; the cap and metering are the control, reviewed at each
  usage report.
- `omniroute/chat-x` was added to the kimi-code CLI config so Carol's lane is
  routable; the other aliases already existed.
- Revisit when: a backend's fitness proves wrong for a lane, the GLM cap
  pressure changes the exception, or new agents are registered (they must
  receive a lane at registration).
