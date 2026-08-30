# Goal: Replace Meta-X with OAI-X (gpt-oss-20b) on hxs-3

- Goal ID: 2026-08-29-oai-x-replace-meta-x (this file's name)
- Version: 1
- Status: draft
- Owner: Agent-Zero
- Created: 2026-08-29
- Human authority: Agent-Zero
- Agent lane(s): john (Ollama engineer, KDD-0013 lane Meta-X → OAI-X transition)

## Intent

Replace the Meta-X model (Muse Glimmer 30B) on hxs-3 with gpt-oss-20b
("OAI-X") as the factory's tooling/structured-contracts LLM. Meta-X is
hypothesized to be too slow for LLM extraction workloads (one observed
OmniRoute rate-limit timeout on LightRAG entity extraction — a routing-level
504, not yet separated from model capability; see the implementation plan's
same-basis A/B). OAI-X (gpt-oss-20b) is expected to handle tool-calling and
structured output workloads more efficiently, but its availability on
Ollama/hxs-3 and its 64K-context feasibility are UNVERIFIED. Both claims are
hypotheses pending verification: the replacement decision depends on the
implementation plan's model-availability/pullability gate and same-basis A/B
performance test, using current evidence and ratified authority. Once OAI-X
is installed, verified, and proven to meet or beat Meta-X, Meta-X is
decommissioned.

## Scope and target

- Target identity: hxs-3 (192.168.50.202), Ollama serving runtime
- Baseline: hxs-3 runs Meta-X (Muse Glimmer 30B, `hx-muse-glimmer-64k`)
  as the active tooling model via Ollama. Ollama is installed and
  running. OmniRoute routes to hxs-3 for Meta-X.
- In scope:
  - Pull gpt-oss-20b model into Ollama on hxs-3 (john's lane — model install
    and local serving verification)
  - Create Ollama Modelfile with call-sign `hx-oai-x-64k` (or owner-selected context window)
  - Verify model serves correctly via Ollama API (john's lane — access verification)
  - Verify model is accessible via OmniRoute (hxs-8 routing) — **routing
    verification is a dependency on trinity's lane** (OmniRoute owner); john
    verifies local serving, trinity verifies and updates the OmniRoute
    connection/routing; the handoff and dependency are recorded (see
    ownership boundary note)
  - Update all references: AGENTS.md, agents/README.md, KDD-0013, agent
    profiles (john, rick — both on Meta-X lane), system-mapping
  - Decommission Meta-X (remove from Ollama — john; update OmniRoute routing —
    trinity) only after all replacement gates pass (see SC-06 + SC-09)
  - Network security boundary: Ollama port 11434 is reachable only within
    the approved private LAN boundary (192.168.50.0/24) per the owner rule
    (no host firewall; the LAN is the exposure boundary). No new host
    firewall is introduced. Authentication is at the OmniRoute routing
    layer (API key), not the Ollama serving layer — Ollama itself exposes
    no per-request auth; access control is the LAN boundary plus
    OmniRoute's authenticated routing from hxs-8. Credentials required:
    the existing OmniRoute API key (from `.local.env`) for hxs-8 → hxs-3
    routing; no new Ollama serving-layer credential is added.
- Out of scope:
  - LightRAG config (already switched to Chat-X local Ollama)
  - OmniRoute itself (trinity's lane) — but OmniRoute routing changes required
    by this goal ARE in scope as a trinity-owned dependency/handoff (john does
    not modify OmniRoute; he verifies local model serving)
  - Other LLM servers (hxs-1, hxs-2, hxs-4)
- Ownership boundary (labeled note 2026-08-30): john owns model installation
  and access verification on hxs-3 (pull, Modelfile, local Ollama API serve).
  Trinity owns OmniRoute routing changes (hxs-8 → hxs-3 new model) — a
  dependency with a defined handoff: john confirms local serving (SC-03), then
  trinity updates routing and confirms OmniRoute access (SC-04). Decommission
  of Meta-X is split: john removes the Ollama artifact, trinity updates
  OmniRoute routing — and neither happens before the replacement-quality gate
  (SC-09) passes.
- Constraints:
  - No Docker (owner rule)
  - Ollama is already installed and running on hxs-3
  - Native Ollama model pull (no build from source)
  - Model must be verified working before Meta-X decommission
  - OmniRoute routing must be updated to point to the new model (trinity's lane)

## Success conditions and evidence

| ID | Property | Measurement / procedure | Expected result | Evidence | Verifier |
| --- | --- | --- | --- | --- | --- |
| SC-01 | gpt-oss-20b pulled | `ollama list \| grep gpt-oss` | Model listed | command output | governor |
| SC-02 | OAI-X Modelfile created | `ollama show hx-oai-x-64k` | Model config visible | command output | governor |
| SC-03 | OAI-X serves via Ollama | `curl http://192.168.50.202:11434/api/generate -d '{"model":"hx-oai-x-64k","prompt":"Say hello"}'` | Response generated | curl output | governor |
| SC-04 | OAI-X accessible via OmniRoute | `curl http://192.168.50.207:20128/v1/models -H "Authorization: Bearer <key>" \| grep oai-x` | Model in OmniRoute catalog | curl output | governor |
| SC-05 | OAI-X tool-calling works | Send a request declaring a tool (e.g. `{"tools":[{"type":"function","function":{"name":"get_weather","description":"...","parameters":{...}}}]}`) and verify the response contains `tool_calls` with valid arguments | Response includes `tool_calls` with well-formed arguments | test output | governor |
| SC-05b | OAI-X structured-output works | Send a structured prompt requiring JSON output | Valid JSON returned | test output | governor |
| SC-06 | Meta-X decommissioned | `ollama list \| grep muse-glimmer` (alias check) AND verify the frozen artifact is removed from the store (`ollama show muse-glimmer:30b` fails, or the FULL artifact digest — recorded from the frozen identity at baseline, e.g. `ollama show muse-glimmer:30b` digest field or the manifest in `/usr/share/ollama/.ollama/models/manifests/…` — is no longer present in `/usr/share/ollama/.ollama/models/blobs` or `ollama list` no longer references it). Do not rely on a truncated prefix; derive the complete digest from local model metadata at verification time if not already recorded | Not listed; artifact and alias removed from store | command output | governor |
| SC-07 | Records updated | AGENTS.md, README.md, KDD-0013, agent profiles carry OAI-X lane | All references updated | grep output | governor |
| SC-08 | Repo validation | `python3 scripts/validate.py` | 4/4 PASS | validate output | governor |
| SC-09 | Replacement-quality gate (added 2026-08-30) | (a) **64K-context feasibility:** serve a request with the operating 64K context window (Modelfile num_ctx + prompt at 64K) and confirm the model responds within the latency budget without OOM/refusal; (b) **same-basis A/B performance vs Meta-X:** run the same representative tooling/context workload on OAI-X (hx-oai-x-64k) and on Meta-X (before decommission), compare response quality, latency, and error behavior on the same prompts | 64K context served successfully; OAI-X meets or beats Meta-X on the measured basis (or the owner documents an accepted trade-off); measurable expected results recorded (latency, tool-call success, output validity); **SC-06 (Meta-X decommissioning) is CONTINGENT on this gate passing** | A/B evidence, context-feasibility run, metrics record | governor |

## Execution controls

- Pre-flight: Ollama running on hxs-3 (VERIFIED — Meta-X served from there)
- Active charters reviewed: john (Ollama engineer, KDD-0013) — qualified, YES
- Maximum iterations / retries: 3 per step
- Time / token limits: PT1H per session
- Stop conditions: Ollama not responding, model pull fails, OmniRoute
  routing error, validate.py FAIL
- Rollback / containment: keep Meta-X until **all** replacement gates pass —
  SC-05 (tool-calling), SC-05b (structured output), SC-04 (OmniRoute access),
  SC-09 (64K-context feasibility + same-basis A/B performance vs Meta-X) — and
  only decommission after the full replacement-quality gate completes; SC-06
  decommissioning is contingent on SC-09 passing (see the Success conditions
  table)
- HITL checkpoints: model name/call-sign confirmation (owner); context
  window size (owner — 64K recommended); OmniRoute routing update
  confirmation (trinity or governor)

## Architecture

```text
Before:
  Agents (john, rick) → OmniRoute (hxs-8) → hxs-3 Ollama → Meta-X (Muse Glimmer 30B)

After:
  Agents (john, rick) → OmniRoute (hxs-8) → hxs-3 Ollama → OAI-X (gpt-oss-20b)
  Meta-X: decommissioned (removed from Ollama)
```

## Notes and links

- KDDs: KDD-0013 (model lanes — Meta-X → OAI-X amendment pending)
- Related goals: 2026-08-29-lightrag-hxs4 (LightRAG already switched
  to Chat-X local Ollama — not affected by this change)
- System mapping: S03 Meta-X → OAI-X (update needed)
- Agent profiles: john (profile.md Meta-X lane), rick (profile.md Meta-X
  lane) — both need lane update
- Model: gpt-oss-20b (OpenAI gpt-oss, 20B params) — **display name only**; the
  canonical Ollama identifier is **`gpt-oss:20b`** (pinned tag, used for pull/
  show/registry checks; never an unpinned `:latest`). Availability on Ollama is
  **conditional on SC-01 passing** (model pull + `ollama list`); do not treat
  availability as confirmed until the pull evidence exists (or cite the
  evidence that establishes it)
- Call-sign: `hx-oai-x-64k` (or owner-selected)

Completion rule: this goal is done only when every success condition passes
with its required evidence and the verifier accepts the correct artifact —
not when the work feels done.
