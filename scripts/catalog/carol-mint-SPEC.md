# SPEC — `carol-mint`: mechanical catalog minting tool

**Status:** SPEC, owner-approved 2026-08-28 ("yes create the spec — better late than never") · **Author:** Kimi-K3 (governor) · **Audience:** Morpheus-era implementer (DSH codification row) or an earlier owner-authorized build
**Problem class:** convention-to-software (living-contract wave, 2026-08-28)

## 1. Problem statement

Carol's waves average 30–60 minutes for ≤10 record updates. Decomposition of that time shows ~90% is *mechanical* — hashing sources, re-minting records, index bookkeeping, running the validator — and ~10% is *judgment* (declared_purpose, relations, conflict flags). The mechanical share is performed by an LLM issuing hundreds of shell calls per wave. Deploy-side work (rick's 12-host baseline: 26 min) outpaces audit-side bookkeeping by ~2–3×, and the per-wave re-mint doctrine generated the dominant rr finding class (metadata about metadata) before the living-contract retired its largest slice. The audit value is real (chronology catches, drift detection); the *cost structure* is the defect.

## 2. Scope

Mechanize the mechanical 90%. Carol (and the governor) invoke a tool that performs the deterministic work in seconds; agents keep only the judgment fields.

**In scope:** single-writer enforcement (mechanical), record re-mint from source, new-record scaffold, index update, receipt skeleton, stale-record sweep, living-class consolidation, wave-scaled validation ladder.

**Out of scope (stays with the agent):** `declared_purpose` prose, `relations` notes, conflict adjudication, flags, review_due judgment, receipt narrative. The tool NEVER generates semantic content.

## 3. Design

### 3.1 CLI surface (no third-party deps beyond the existing pyyaml)

```
carol-mint re-mint <DOC-id> [--note "<provenance>"]     # re-hash one record from its source
carol-mint new --source <path> --type <t> --id <slug>   # scaffold a new record (mechanical fields only)
carol-mint index                                        # rebuild index.yaml from documents/ (count, lines, updated field)
carol-mint receipt <wave-name> --items <ids...>         # receipt skeleton with before->after hashes pre-filled
carol-mint sweep-stale                                  # list records whose live source hash != recorded hash
carol-mint consolidate                                  # re-mint all freshness=living records whose source changed
carol-mint gate [--ids <ids...>]                        # write-set validation ladder (see 3.5)
```

### 3.2 Single-writer, made mechanical

`flock` on `knowledge/catalog/.mint.lock` for every mutation. Convention becomes enforceable: **only the tool writes `documents/` and `index.yaml`** (agents invoke it; direct hand edits are convention violations). The lock makes the write-race rule a property of the filesystem, not of dispatch discipline.

### 3.3 Mutation semantics

- Source access strictly read-only; all writes atomic (temp file + rename).
- On `re-mint`: recompute source sha256; update `sha256`, `validated_at`, index line; append the living_document chain entry **only** for `freshness: living` records at consolidation; preserve all notes/provenance untouched.
- On `new`: scaffold with required fields only; `declared_purpose: "PENDING-AGENT"` (a wave is not complete until an agent fills it — the tool enforces this as a gate item).
- Tool stamps every mutation: `notes.minted_by: "carol-mint <version> @ <utc>"`.

### 3.4 Living-class consolidation

`carol-mint consolidate` (manual now; cron later — daily 04:00Z): re-mints every `freshness: living` record whose live source hash differs from the recorded consolidation, stamps the new consolidation point, and refreshes index lines. Arc-close and owner-call invocations are the same command.

### 3.5 Validation ladder (replaces full-battery-per-wave)

- `carol-mint gate --ids ...` — write-set gate: YAML parse + required fields + freshness enum + index 1:1 for the touched records + their relation targets resolve. Target: seconds. Default for T-micro/T-standard waves.
- `scripts/validate.py` (full 4/4) runs at consolidation, arc close, and owner call — not per micro wave. (Carol profile §12/§T-micro updated to match at implementation.)

### 3.6 Receipts

`carol-mint receipt` emits the skeleton: wave name, UTC window, per-record before→after hashes (auto-filled from the pre/post state), validator output slot, flags section. The agent completes the judgment fields; "receipts close handoffs" is unchanged.

## 4. Acceptance

1. A 5-record wave's mechanical work completes in < 2 minutes end-to-end (vs 30–60 today); agent time is spent on judgment only.
2. `validate.py` 4/4 PASS after every tool-driven wave; write-set gate output reproducible.
3. No direct-write bypass: `documents/` + `index.yaml` mutations provably carry the tool stamp (spot-auditable).
4. Living consolidation is one command and produces a receipt the owner can read without interpretation.

## 5. Phasing

| Phase | Deliverable | Value |
| --- | --- | --- |
| 1 | `re-mint`, `sweep-stale`, lock, gate | kills the bulk of wave time |
| 2 | `receipt` skeleton, `index` rebuild | closes the bookkeeping tail |
| 3 | `consolidate` + daily trigger | living contract becomes self-driving |
| 4 | validator guard: reject unstamped catalog writes in CI | single-writer enforced in CI |

## 6. Placement and governance

- Lives at `scripts/catalog/carol-mint` (Python 3 stdlib + pyyaml); `scripts/catalog/README.md` documents the contract; `AGENTS.md` tooling note updated at adoption.
- The tool is itself cataloged (DOC-scripts-carol-mint) and fixture-tested like the fleet library (refusal matrix: no lock → refuse; unknown record → refuse; semantic field in a mechanical command → refuse).
- Carol's profile gains a §13 at adoption: "mechanical minting is delegated to carol-mint; the agent owns judgment, relations, conflicts, and flags."
- Builder: Morpheus-era codification row (proven convention → software) unless the owner authorizes an earlier build. Spec-to-build estimate: ~400 lines + fixtures; one focused session.
