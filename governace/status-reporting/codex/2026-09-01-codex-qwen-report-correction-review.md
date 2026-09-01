# Codex Correction Review — Qwen Governor Report

## Status

Control-plane correction only. The hxs-1 factory remains **STOPPED**. This
review is the pre-edit write-set manifest for the owner-authorized correction
session on 2026-09-01. It does not authorize worker dispatch, canary execution,
server access, or a phase/gate transition.

## Confirmed Qwen-report discrepancies

- **D1 — dispatch evidence:** `/root/m1_john_clean` is a canonical agent-task
  identifier, not filesystem-cwd evidence. The PATH-alias read-only-filesystem
  warning also does not establish cwd. P3 is not currently best-supported.
- **D2 — blocker classification:** the intake soak supersession, parent-path
  corrections, and causal-label clarification may ride this batch, but are not
  independent Phase A blockers.
- **D3 — approval basis:** the unsupported count phrase is not used. Approval
  and final reconciliation use the actual file-by-file write set below.

## Pre-edit write-set manifest

| File | Classification | Intended bounded correction |
| --- | --- | --- |
| `AGENTS.md` | Phase A blocker | Harmonize defined-agent dispatch language; distinguish authorized factory mechanisms from unproven third-party harness behavior; retain profile/charter-read requirement. |
| `pilots/PILOT-OLLAMA-FLEET-REQUAL-HXS1-001/01-work-order-john-tkv-review.yaml` | Phase A blocker | Preserve completed M1 receipts through a versioned receipt or dated amendment. |
| `pilots/PILOT-OLLAMA-FLEET-REQUAL-HXS1-001/02-context-packet-john-tkv-review.yaml` | Phase A blocker | Fail closed: M2 requires the exact M1 receipt line `Task May Proceed: YES`; correct the Gate B Carol-receipt contradiction. |
| `pilots/PILOT-OLLAMA-FLEET-REQUAL-HXS1-001/03-work-order-john-live-audit.yaml` | Phase A blocker | Require the exact M1 YES receipt before live audit and preserve prior completed receipt/evidence relationships. |
| `pilots/PILOT-OLLAMA-FLEET-REQUAL-HXS1-001/plan.md` | Phase B blocker | Correct parent goal path, OmniRoute dependency, and Gate B citation requirement. |
| `pilots/PILOT-OLLAMA-FLEET-REQUAL-HXS1-001/12-work-order-bailey-qualification.yaml` | Phase B blocker | Require Gate A, M6, and M7; require M8 when routing is in scope. |
| `pilots/PILOT-OLLAMA-FLEET-REQUAL-HXS1-001/14-work-order-carol-catalog.yaml` | Phase B blocker | Correct the parent-goal controlling-source path. |
| `pilots/PILOT-OLLAMA-FLEET-REQUAL-HXS1-001/15-gate-a-findings-register.md` | Phase B blocker | Correct the parent-goal path. |
| `governace/sponsor/hxs-1/2026-08-31-factory-intake-ollama-fleet-requalification-wo1-hxs1.md` | Ride-along hygiene/record integrity | Append-only D3 supersession note; preserve the original intake. |
| `governace/lesson-learned/lessons-learned.md` | Ride-along hygiene/record integrity | Append-only epistemic clarification separating observation from unverified causal hypotheses. |
| `agents/james/profile.md` | Ride-along hygiene/record integrity | Make James’s durable identity and authority model-agnostic; record the current owner-approved runtime binding as replaceable. |
| `agents/james/charter.md` | Ride-along hygiene/record integrity | Remove provider-specific identity language from the durable governor charter. |
| `governace/decisions/KDD-0013-agent-model-lanes.md` | Ride-along hygiene/record integrity | Append a current-binding amendment preserving historical DeepSeek assignment. |
| `knowledge/catalog/documents/DOC-goal-ollama-fleet-requalification-hxs1-qwen-x.yaml` | Generated mirror/catalog consequence | Correct lifecycle and approved-goal applicability metadata, then re-mint. |
| `knowledge/catalog/index.yaml` | Generated mirror/catalog consequence | Update only through the targeted catalog re-mint. |
| `AGENTS.html` | Generated mirror/catalog consequence | Re-render from changed `AGENTS.md`. |
| `agents/james/profile.html` | Generated mirror/catalog consequence | Re-render from changed profile. |
| `agents/james/charter.html` | Generated mirror/catalog consequence | Re-render from changed charter. |
| `governace/lesson-learned/lessons-learned.html` | Generated mirror/catalog consequence | Re-render from changed lessons source. |
| `governace/decisions/KDD-0013-agent-model-lanes.html` | Generated mirror/catalog consequence | Re-render from changed KDD source. |
| `governace/status-reporting/codex/2026-09-01-codex-qwen-report-correction-review.md` | Ride-along hygiene/record integrity | This correction receipt and pre-edit manifest. |

No other file is authorized for modification by this session. In particular,
`knowledge/catalog/documents/DOC-backend-qwen-x.yaml` remains unchanged because
its live-state reconciliation is an M11 activity and the factory is stopped.

## Catalog-consequence addendum

The first full validation identified the five catalog records that directly
describe the changed governance sources. They are affected catalog consequences,
not unrelated catalog regeneration. This addendum is entered before their
re-mint:

| File | Classification | Intended bounded correction |
| --- | --- | --- |
| `knowledge/catalog/documents/DOC-repo-governance-agents-md.yaml` | Generated mirror/catalog consequence | Re-mint the record after the dispatch-governance correction. |
| `knowledge/catalog/documents/DOC-agent-james-profile.yaml` | Generated mirror/catalog consequence | Re-mint the record after the durable-identity/runtime-binding correction. |
| `knowledge/catalog/documents/DOC-agent-james-charter.yaml` | Generated mirror/catalog consequence | Re-mint the record after the durable-identity/runtime-binding correction. |
| `knowledge/catalog/documents/DOC-kdd-0013-agent-model-lanes.yaml` | Generated mirror/catalog consequence | Re-mint the record after Amendment 13. |
| `knowledge/catalog/documents/DOC-knowledge-lessons-learned.yaml` | Generated mirror/catalog consequence | Re-mint the record after the epistemic clarification. |

`knowledge/catalog/index.yaml` remains the single generated index consequence
for these targeted re-mints. No other catalog record is in scope.

### 2026-09-01 amendment — five-record catalog write boundary

This amendment supersedes the `No other file is authorized` boundary above only
to admit the five catalog records listed in this addendum. It does not expand
the authorized write set to any other catalog record or file; the existing
`knowledge/catalog/index.yaml` entry remains governed by the pre-edit manifest.

### 2026-09-01 amendment — paired historical-path context packet

The verified historical M8 precedent correction additionally admits
`pilots/PILOT-OLLAMA-FLEET-REQUAL-HXS1-001/04-context-packet-john-live-audit.yaml`
solely to keep its cited precedent path identical to work order 03. No other
context packet or work order is admitted by this amendment.

## Evidence basis

- Owner authorization dated 2026-09-01.
- `governace/status-reporting/qwen/2026-09-01-qwen-governor-session-report.md`
  findings 1–8 and D1–D3 correction review.
- `governace/status-reporting/2026-09-01-dispatch-defect-evidence.md` observed
  payload submission, worker responses, and the explicit `UNVERIFIED` cause
  state.
