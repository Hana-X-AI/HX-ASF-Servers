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
| Gordon | Qwen-X (`ollama-local/hx-qwen3.8-27b-64k`, hxs-1; immutable identity: manifest digest `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a`, recorded 2026-08-28) [SUPERSEDED 2026-08-28 — see amendment 2 below] | Deterministic oracles remain first-tool |
| Rick | Meta-X (`ollama-local/hx-muse-glimmer-64k`, hxs-3; immutable identity: manifest digest `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da`, recorded 2026-08-28) | Work class largely deterministic; lane covers analysis/drafting |
| John | Meta-X (`ollama-local/hx-muse-glimmer-64k`, hxs-3; same immutable identity as rick's row) | Same deterministic caveat as rick |
| Carol | Chat-X (`ollama-local/hx-qwen3.5-9b-64k`, hxs-4; immutable identity: manifest digest `5936a390c6c22594ce49e8c77187fc92f4a81126fd04a4eabad7c000b30447d2`, recorded 2026-08-28) [SUPERSEDED 2026-08-28 — see amendment 4 below] | Schema/mechanical validation stays deterministic (validate.py); currently frozen by owner directive |
| Trinity | Z.ai GLM 5.3 Flash (`openrouter/z-ai/glm-5.3-flash`; identity of record per amendment 3: served id `z-ai/glm-5.3-flash`, upstream provider Modal, route probed live 2026-08-28) | OD-14 exception; supersedes her Coder-X designation |
| Rob | Z.ai GLM 5.3 Flash (`openrouter/z-ai/glm-5.3-flash`; identity of record per amendment 3: served id `z-ai/glm-5.3-flash`, upstream provider Modal, route probed live 2026-08-28) | OD-14 exception; resolves his profile's D1 against its Coder-X recommendation — recorded openly |
| Mia | Z.ai GLM 5.3 Flash (`openrouter/z-ai/glm-5.3-flash`; identity of record per amendment 3: served id `z-ai/glm-5.3-flash`, upstream provider Modal, route probed live 2026-08-28) | OD-14 exception |

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

[Amendment 2026-08-28, labeled — owner directive: the 2026-08-27 substrate
exception is RETRACTED. Only Kimi-K3 runs on `moonshot-ai/kimi-k3`; every other
agent's work sessions run on its assigned lane via standalone
`kimi -m omniroute/<lane> --agent-file …` sessions (or dsh sessions on hxs-15
for harness-side work). Agent-tool sub-agent dispatches inherit the governor's
moonshot model and are therefore no longer an execution path for agent work.
See AGENTS.md local-model-first section for the full labeled correction.]

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

[Amendment 2 — 2026-08-28, labeled — owner directive: Gordon's lane changes from
Qwen-X (local, hxs-1) to **DeepSeek V4 Pro** (`openrouter/deepseek/deepseek-v4-pro-0813`,
upstream provider StreamLake, via OmniRoute hxs-8). The OpenRouter connection of
record (OD-14 exception) carries the key; route probed live before activation
(`ROUTE-OK`, reasoning tokens flowing, 109 tokens on the probe). Identity
verification for this lane = exact served-model id echoed by the gateway plus a
routed probe at session start (no local manifest digest exists for a cloud
model); the fail-closed rule applies to the probe. Deterministic oracles remain
Gordon's first tool; Qwen-X remains the designated VERIFIER backend where a
separate-host verifier is required. The Qwen-X row above is preserved as
history.]

[Amendment 3 — 2026-08-28, labeled: (a) OD-14 model identity for the GLM lanes
(trinity, rob, mia): served model id `z-ai/glm-5.3-flash`, upstream provider
**Modal** (owner directive 2026-08-28: "GLM 5.3 Flash the provider = Modal");
route probed live same day (`ROUTE-OK`, exact served id echoed by the gateway).
No local manifest digest exists for a cloud-served model; the verifiable
immutable identity of record is the exact served-model id plus a session-start
routed probe — the fail-closed rule applies to that probe (exact-id mismatch or
an unhealthy endpoint stops the task before inference). (b) OD-14 scope
correction: gordon's DeepSeek V4 Pro lane (amendment 2) rides the SAME OD-14
OpenRouter exception and metering scope — the cloud-substitution controls and
Consequences now cover FOUR cloud lanes (trinity, rob, mia, gordon); the
Consequences sentence "GLM lanes (trinity, rob, mia) spend OpenRouter credit…"
is amended accordingly, original preserved here. (c) the three GLM table rows
above now carry their identity-of-record pointers; prior wording preserved in
git history.]

[Amendment 4 — 2026-08-28, labeled — owner directive: Carol's lane changes from
Chat-X (local, hxs-4) to **OpenAI gpt-oss-120b** (`openrouter/openai/gpt-oss-120b`,
upstream provider **AkashML**, via OmniRoute hxs-8). Route probed live before
activation: model served exactly as named, coherent reasoning stream (the empty
`content` on tiny probes is a token-cap artifact of a reasoning model —
`finish_reason=length`, reasoning field healthy; normal session budgets are
unaffected). Identity verification per amendment 2's cloud pattern: exact
served-model id echo plus session-start probe, fail closed. Context of record:
the Chat-X gateway connection was already INACTIVE (posture-blocked, state-log
row 28), so the local lane was unrouteable regardless; her row above is
preserved as history. OD-14 scope: the exception and its metering now cover
FIVE cloud lanes (trinity, rob, mia, gordon, carol) — amendment 3(b)'s "four
cloud lanes" is corrected here, original preserved. Carol remains FROZEN by
owner directive: this lane is registered, not yet exercised.]

[Amendment 5 — 2026-08-29, labeled: (a) Carol's freeze is LIFTED to
**background-class** by owner directive ("you can run carol but not on the
critical path… does not block any work"): her gpt-oss-120b lane (amendment 4)
is ACTIVE for catalog catch-up, asynchronous — no gate, handoff, or lane blocks
on her output; her table row's "currently frozen by owner directive" note is
superseded, original preserved. (b) PENDING owner instruction of record: "once
deepseek is up and running we will change your model to point to openrouter
model also" — Kimi-K3's own lane moves off moonshot-ai to an OpenRouter model
when the owner declares the DeepSeek work up and running; the model-selection
plan comes to the owner at that trigger. NO config change now.]

[Amendment 6 — 2026-08-29, labeled — owner directive: **Chris** is registered
(KDD-0014) with lane **Qwen 3.8 Flash** (`openrouter/qwen/qwen3.8-flash`,
upstream provider **Alibaba Cloud International**, via OmniRoute hxs-8). Route
probed live before activation (exact served id echoed). Identity verification
per the amendment-2 cloud pattern: exact served-model id + session-start
probe, fail closed. OD-14 scope: the exception and its metering now cover SIX
cloud lanes (trinity, rob, mia, gordon, carol, chris) — amendment 4's "five"
is corrected here, original preserved. New-agent rule of record satisfied: he
received his lane at registration. His table row is appended below this
amendment.]

[Form note 2026-08-29, labeled, Mia per Flash work order 19 — F11: the Chris
row below was appended as a bare table fragment (no header), which does not
render as a table. It is now presented as a headered standalone Markdown
table per the reviewer's alternative; values unchanged, and it is NOT merged
into the main table at line 34 (that table is frozen as of the original
decision; amendments are appended, not inserted — append-only convention).]

| Agent | Model lane | Notes |
| --- | --- | --- |
| Chris | Qwen 3.8 Flash (`openrouter/qwen/qwen3.8-flash`; upstream Alibaba Cloud International; identity of record per amendment 2's cloud pattern, route probed live 2026-08-29) | OD-14 exception; registered KDD-0014; activation gated |

[Amendment 7 — 2026-08-29, labeled — owner directive: the GOVERNOR's lane
changes from `moonshot-ai/kimi-k3` to **Z.ai GLM 5.2**
(`openrouter/z-ai/glm-5.2`, upstream provider **Decart**, via OmniRoute hxs-8).
Route probed live before the change (exact served id echoed, reasoning
flowing); `default_model` in the kimi CLI config now reads
`omniroute/glm-5.2` (next-session effect); `kimi doctor` valid; a live
no-`-m` session answered on the new lane. The moonshot meta-agent exception
for the governor (owner rule 2026-08-27) is SUPERSEDED by this directive and
preserved as history — the substrate-retraction rule stands unchanged for
every other agent (no moonshot sub-agents). Governor traffic joins the OD-14
metering scope: SEVEN cloud lanes now (trinity, rob, mia, gordon, carol,
chris, kimi-k3) — amendment 6's "six" is corrected here, original preserved.
The `omniroute/glm-5.2` alias carries max_output_size=16384 per the row-33
guard class.]

[Amendment 8 — 2026-08-29, labeled — GOVERNOR TRANSITION: the governor ROLE
transfers from kimi-k3 to **Flash** (owner/Agent Zero appointment reported
2026-08-29 via Flash's work order to the Chief of Staff). Flash runs on
**DeepSeek V4 Flash** via OmniRoute. Amendment 7's GLM 5.2 governor lane is
SUPERSEDED for the governor role and preserved as history; the
substrate-retraction rule (no moonshot sub-agents; no Agent-tool dispatch for
agent work) stands unchanged for every agent. Governance references to
"Kimi-K3" as the governor (Chief of Staff reporting line, checkpoint routing,
state-log triage agent fields) read as the GOVERNOR role — currently Flash.
SCOPE NOTE: this amendment records a reported appointment; the owner's
primary confirmation in records is pending and the appointment is carried at
intent-level evidence (Flash-issued work order 14,
`pilots/PILOT-DSH-IMPL-001/14-flash-work-order-mia-hxs9-transition-records.md`).
No OD-14 metering change is implied beyond amendment 7's seven-lane scope
until the owner rules on Flash's lane.]

[Amendment 9 — 2026-08-29, labeled — WAYNE REGISTERED: Wayne (Redis systems
engineer, KDD-0015) registered with lane OpenAI gpt-oss-120b
(`openrouter/openai/gpt-oss-120b`, provider AkashML, via OmniRoute hxs-8) —
same lane as Carol; owner-assigned 2026-08-29. The source profile's
`coder-x` primary backend is superseded. CLI alias `omniroute/gpt-oss-120b`
already exists (established for Carol, row 33 guard class). OD-14 exception
scope now covers EIGHT metered cloud lanes: trinity, rob, mia, gordon,
carol, chris, kimi-k3, wayne. Amendment 7's seven-lane scope is superseded;
preserved as history. Lane corrections in the same window: morpheus →
Qwen 3.8 2.4T A95B (DeepInfra) superseding Coder-X; chris → DeepSeek V4 Pro
(Baidu FP8) superseding Qwen 3.8 Flash — both owner directives 2026-08-29.]

[Amendment 10 — 2026-08-29, labeled, append-only — LANE CAPABILITY REGISTRY
(QA-audit SY-5): the verified capability/context profile of each lane, so
every work order is pre-scoped. Entries are VERIFIED facts from state-log
rows and config; re-probe at dispatch. Fail-closed: a capped lane's work
order must carry the context_budget + capability_probe fields (work-order
template, ST-5).]

| Lane | Verified context ceiling | Output guard | Capability note (evidence) |
| --- | --- | --- | --- |
| gpt-oss-120b (carol, wayne) | 131072 total | `max_output_size=16384` (row-33 guard) | Session-overhead overflow at start if unguarded (state-log rows 32-33) |
| Qwen 3.8 2.4T A95B (morpheus) | 65536 (half of carol's) | apply same guard class | Driver-lane failure class on long synthesis (rows 34, 40-41); WRITE-FIRST discipline |
| Meta-X (rick, john) | 65536 | none recorded | Deterministic work; analysis/drafting |
| Chat-X (carol prior) | 131072 | — | Superseded for carol; used by LightRAG LLM binding |
| DeepSeek V4 Pro (gordon, chris) | 1048576/1310720 metadata | — | High ceiling; gordon campaign-verified |
| GLM 5.3 Flash (trinity, rob, mia) | per metadata | row-33 guard class if overflow | Omnicontext metadata-driven |
| DeepSeek V4 Flash (governor/Flash) | per metadata | row-33 guard class if overflow | Governor lane |
| Nemotron 3 Ultra (quinn) | free tier | — | Unmetered; capability probe at dispatch |

Rule: every work order on a capped lane must include the context_budget +
capability_probe fields and a 4-token pre-dispatch probe (row-33 fix). No
automatic lane substitution on failure — stop and escalate (KDD-0013).

[Amendment 11 — 2026-08-30, labeled, append-only — JOB-FAMILY LANE DEFAULTS
(owner decision, multi-agent alignment session): lane defaults are now assigned
per JOB FAMILY (lane-config view, separate from the KDD-0016 taxonomy). These
supersede the per-agent lanes recorded in amendments above for the affected
agents; prior lanes preserved as history. Per-agent overrides within a family
are supported and recorded as such.]

| Job family | Members | Default lane | Model / provider | Status |
| --- | --- | --- | --- | --- |
| Governor (above all) | James | DeepSeek V4 Flash | via OmniRoute | pinned |
| PMO | Mia, Carol | GPT-OSS 120B | `openai/gpt-oss-120b`, AkashML | replaces prior per-agent lanes |
| QA | Bailey, Gordon | Qwen3.8 Flash | `qwen/qwen3.8-flash`, Alibaba Cloud Intl | Gordon override recorded 2026-08-29 |
| Agentic SWE | Rob | Coder-X | `ollama-local/hx-qwen3.6-coderx-64k` (hxs-2) | supersedes GLM 5.3 Flash (amendment 3) |
| Infra / Ops | Rick | Coder-X | `ollama-local/hx-qwen3.6-coderx-64k` (hxs-2) | supersedes Meta-X (original row) |
| Platform Systems | Trinity, Morpheus, John, Chris, Wayne, Quinn, Raphael, Erwin (+ future SE) | Z.ai GLM 5.2 free | `z-ai/glm-5.2:free`, Decart | REPLACES current per-agent lanes (GLM 5.3 Flash / Qwen 3.8 2.4T / Meta-X / DeepSeek V4 Pro / GPT-OSS 120B / Nemotron / Qwen-X) — all fold into GLM 5.2 free |

Notes: (1) Rob and Rick move to the local Coder-X lane (hxs-2); their prior
lanes (GLM 5.3 Flash, Meta-X) are superseded. (2) Platform Systems members move
from their ratified per-agent lanes to the cloud-free GLM 5.2 lane; Quinn's
Nemotron 3 Ultra free tier folds in. (3) These are lane-default changes for
future dispatch; no running campaign is interrupted. (4) The capability registry
in Amendment 10 stands but its lane column is superseded by this table for the
affected agents. Authority: owner decision 2026-08-30 (multi-agent alignment
session, lane-defaults table LOCKED).

[Amendment 12 — 2026-08-30, labeled, append-only — BAILEY QA LANE ON OD-14
ALLOWLIST: the QA family default (Amendment 11) assigns Bailey Qwen3.8 Flash
(`openrouter/qwen/qwen3.8-flash`, provider Alibaba Cloud International, via
OmniRoute hxs-8) — the same provider lane as chris's original registration
(KDD-0014, amendment 6). Reconciliation per CodeRabbit review: Bailey's lane is
now included in the OD-14 owner-lane allowlist and metering scope. OD-14 scope
is now TEN cloud lanes — trinity, rob, mia, gordon, carol, chris, kimi-k3,
wayne, quinn (unmetered), bailey (metered) — superseding amendment 9's
eight-lane scope and AGENTS.md's nine-lane scope for Bailey (preserved as
history). Activation-gated: Bailey's lane is registered and allowlisted but NOT
exercised until her activation gate clears (KDD-0019 activation gate:
implemented usage, `.local.env` credential references, governor activation
word). No metered spend accrues before activation. Usage control: same OD-14
USD 100 cap and metered `usage_history` control; per-task identity verification
per the amendment-2 cloud pattern (exact served-model id + session-start probe,
fail closed). Authority: owner decision 2026-08-30 (QA job-family lane default,
KDD-0013 Amendment 11, LOCKED) + Bailey registration KDD-0019; recorded here
append-only to keep the OD-14 authorization data authoritative and consistent
with KDD-0019.]
