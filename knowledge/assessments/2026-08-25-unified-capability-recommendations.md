# Unified Capability Recommendation List (KK3 assessment × Codex assessment, reconciled)

| Field | Value |
| --- | --- |
| Date | 2026-08-25 |
| Author | Kimi-K3 (governor), at owner request: "review tool-belt, come back with a unified recommendation list" |
| Inputs | (a) `knowledge/assessments/2026-08-25-capability-assessment-read-only.md` (KK3, O1–O10); (b) `/home/hxsa/opt/local-tkv/agent-zero-docs/tool-belt/codex_20260825_2207_hx-asf-servers-read-only-project-capability-assessment.md` (Codex/Copilot, 657 lines, R1–R7 + O1–O17 + D1–D7) |
| Reconciliation rules | AGENTS.md adoption-of-provided-documents: verify claims against current evidence and ratified authority; reconcile conflicts, never blend; record corrections with provenance. Product facts verified against official Kimi Code hooks/MCP docs fetched 2026-08-25 |
| Status | Recommendation only. Nothing here is implemented or authorized by this document. |

## 1. Where the two assessments agree (high confidence, no reconciliation needed)

- The project needs no new platform, knowledge store, orchestrator, database,
  vector/graph index, always-on agent, second control plane, or Ansible.
- No MCP additions now: Mobbin stays disabled; no catalog/GitHub/fleet/SSH MCP;
  no Ollama MCP (ratified loopback-only posture; owner D1/OmniRoute is the gate).
- No session-start context-injection hook; no hooks that mutate the catalog or
  make authority/phase decisions; no auto-writing receipts.
- No new catalog/Carol skill (duplicates charter/profile/CAT/CB).
- Executable custom agents stay deferred to a phase-transition KDD.
- CI only after a local validator proves a low false-positive rate and the owner
  approves GitHub-hosted execution.
- Marketplace: nothing adopted as a project gate; editor aids stay optional.

## 2. Corrections to the Codex document (recorded per convention)

- **C-C1 — Hook lifecycle: VERIFICATION REQUIRED → VERIFIED.** Codex could not
  establish Kimi hook events/paths from primary docs. KK3 fetched the official
  page 2026-08-25: `[[hooks]]` in `~/.kimi-code/config.toml` (fields event,
  matcher, command, timeout 1–600 s); blockable events = PreToolUse, Stop,
  UserPromptSubmit (exit 2 = block); all others observation-only; hooks are
  **fail-open by design** (error/timeout = allow) — interception layers, never
  sole barriers. Codex's D3 precondition is satisfied.
- **C-C2 — Catalog-validation dependency is nearer than assessed.** Codex: Python
  stdlib does not parse YAML, so executable CAT checks need an approved parser
  first. Evidence: PyYAML is installed on hxs-5 and has been in proven governor
  use all week (every CAT mechanical re-check, rows 35–57, parsed all 172 records
  with `yaml.safe_load`). CAT-01/03/04/07/08 are mechanizable today by
  consolidating the governor's per-run scripts into one governed command — no ad
  hoc parser, no new dependency. Codex's D2 can be answered "yes, in scope"
  instead of "after schema/parser approval."
- **C-C3 — "Markdownlint installed" is editor-host state**, not project state
  (owner's VS Code environment; Codex correctly labeled it marketplace metadata).
  It stays an optional editor aid, never a project gate.
- **C-C4 — Fixture hygiene note confirmed:** `q16_rerun.py` unclosed-file
  ResourceWarning (also flagged by the batch-7 fixer as R3). Housekeeping at the
  next fixture touch; not a capability question.

## 3. Where they conflicted, and the resolution

- **KK3 O2 (auto-render HTML on edit) vs Codex O17 (reject auto-mutating hooks).**
  Resolved to Codex's model: hooks do not mutate. Wiki sync becomes a *check*
  inside the unified validator plus an advisory hook warning — rendering stays an
  intentional act; `render.py --check` stays the audit. (U3 covers.)
- **KK3 O4/O5 (new dispatch + receipt-check skills) vs Codex R5 (no new skills).**
  Resolved: the *content* is adopted, the *form* changes. Work-order/context-
  packet format becomes template files carrying the standing directive's
  mandatory Second Brain evaluation block (U6); the governor verification ritual
  becomes a checklist document (U7). No new skills now; a validation skill only
  after two lanes consume the validator (U8) — both assessments' rule.
- **KK3 O7 (pilot read-only TKV filesystem MCP) vs Codex (no filesystem MCP).**
  Resolved to Codex's position: defer. TKV surveys over Bash work; the tool-layer
  read-only argument is defense-in-depth, not a measured need, and it carries an
  unverified node/npx dependency plus an unresolved YOLO-vs-deny-rule question.
  Trigger to revisit: a demonstrated survey access-control need or a second
  consumer. Verification items stay recorded in the KK3 assessment.

## 4. The unified list

### Track A — Validation foundation (Codex model, KK3-verified)

- **U1 (P0, owner decision): ratify the one-command validation contract.** One
  read-only repo-root command with stable exit codes composing: `render.py
  --check` (wiki sync), `test_fixtures.py` (57 tests), fixture manifest
  verification, secret-boundary sweep — and CAT-01..08/CB-01 labeled honestly
  (mechanized where executable, `MANUAL GATE REQUIRED` where judgmental). No
  network, no mutation, sanitized output. Basis: Codex §8; dependency answer
  per C-C2.
- **U2 (P1, bounded work order): implement `scripts/validate.py`** consolidating
  the governor's per-run CAT scripts into the governed single command.
- **U3 (P1, pilot): advisory validation hook** — PostToolUse/PreToolUse on
  changed relevant paths; advisory only (exit 0, exact reproduction command);
  no mutation, no host/network/protected-file access, bounded timeout; ≥10
  representative change sets of evidence before any enforcement talk. Lifecycle
  facts VERIFIED (C-C1).
- **U4 (P2/P3, separate owner decisions): enforcing-mode hook, then PR CI** —
  each decided independently on U3 evidence; CI gets least-privilege
  `contents: read`, no fleet secrets, no untrusted privileged workflows.

### Track B — Security interception (KK3 item, hardened by Codex guardrails)

- **U5 (P1, pilot, independent track): secret-boundary PreToolUse hook** —
  matcher Write|Edit|Bash; repo-versioned script under `scripts/hooks/`;
  warn-mode one week, then block-mode (exit 2); false-positive log; never reads
  protected credential files; fail-open caveat applies (not a sole barrier —
  CAT-05 and the protected-resource convention remain). The only item in either
  assessment that prevents a demonstrated incident class (F-M5-1; 0600
  extractions ×2) instead of containing it.

### Track C — Workflow codification (merged form)

- **U6 (P1): work-order/context-packet template files with the standing
  directive's Second Brain evaluation block built in** (answers the mandatory
  4-point disposition structurally). Replaces KK3's dispatch-skill proposal.
- **U7 (P1): governor evidence-verification checklist** (artifact → receipt →
  token-context check → secret sweep → hash integrity → live-state claims).
  Replaces KK3's receipt-check skill proposal.
- **U8 (defer): `hx-validation` skill** — only after U2 has two independent
  lane consumers (both assessments' two-consumer rule).

### Track D — Hold / defer / reject (both agree)

- **U9:** MCP posture frozen — Mobbin disabled; no catalog/GitHub/fleet/SSH/
  filesystem MCP; no Ollama MCP (owner D1/OmniRoute gate).
- **U10:** no databases/vector/graph (G-06 benchmark gate); no always-on
  automation; no session-start injection; no auto-mutating hooks; no custom-
  agent executables (phase-transition KDD); no Ansible; no new catalog root.
- **U11 (extensions):** markdownlint retain-optional; Red Hat YAML conditional
  pilot only after an executable schema association exists (U2 may supply it)
  and owner review of version/telemetry/update policy; Mermaid preview
  user-optional; GitHub PR extension not recommended.
- **U12 (housekeeping):** fix the `q16_rerun.py` ResourceWarning at the next
  fixture touch (trivial `with open`; regression suite must stay green).

## 5. Owner decisions requested

| ID | Decision | Recommendation |
| --- | --- | --- |
| UD1 | Ratify the U1 validation contract as the design basis? | Yes |
| UD2 | Approve the U2 bounded work order (`scripts/validate.py`)? | Yes |
| UD3 | Approve the U3 advisory-hook pilot (after U2)? | Yes, advisory-only |
| UD4 | Approve the U5 secret-boundary hook pilot? | Yes — highest-value single item |
| UD5 | Approve U6/U7 template + checklist authoring? | Yes |
| UD6 | CI decision | Defer until U3 evidence exists |
| UD7 | Extension posture (U11) | Confirm as written |

## 6. Second Brain disposition (standing directive, mandatory)

1. **Opportunity identified?** Yes — two.
2. **Capabilities/patterns:** (a) the U6 work-order template operationalizes the
   standing directive itself (every future dispatch carries the evaluation);
   (b) U1/U2's composition of `render.py --check` and manifest verification is
   canonical-state synchronization proof — the roadmap's externalized-state
   principle made executable.
3. **Dispositions:** (a) recommended for this iteration (UD5); (b) recommended
   next iteration (UD1/UD2). Nothing SB-architectural is added; the canonical
   home, Carol's bounds, and the deferred-capability list are untouched.
4. **Evidence/reasoning:** this reconciliation plus both source assessments;
   the catalog stays file-backed at 19× measured economy, so no roadmap gate
   opens as a side effect.

## 7. Provenance and queued actions

Codex document read end-to-end (657 lines) and verified against current repo
state and official product docs. Corrections C-C1..C-C4 recorded in section 2.
Queued to Carol's next run (standing governance; no implementation): catalog
records for the Codex assessment (supplied document, owner-docs tree) with the
correction notes, and for this unified list. State-log citation: row 59.
