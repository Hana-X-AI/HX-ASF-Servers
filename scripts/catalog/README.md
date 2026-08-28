# scripts/catalog — catalog tooling

## carol-mint

Mechanical catalog minting tool (spec: `carol-mint-SPEC.md`, owner-approved 2026-08-28).
It performs the deterministic 90% of catalog waves — hashing, re-minting, index
rebuilds, receipt skeletons, stale sweeps, living-class consolidation, and the
write-set gate — in seconds, so the agent (Carol) keeps only the judgment fields
(`declared_purpose`, `relations` notes, conflict flags, receipt narrative).

**Single-writer, mechanically enforced:** every mutating command takes an
exclusive `flock` on `knowledge/catalog/.mint.lock`. Only the tool writes
`documents/` and `index.yaml`; a second concurrent writer is refused. All
writes are atomic (temp + rename). Sources are strictly read-only.

```
carol-mint re-mint <DOC-id> [--note "..."] [--set-freshness X]
carol-mint new <DOC-id> --source <path> --type <t> [--title ...]
carol-mint index [--note "..."]
carol-mint receipt <wave> --items <DOC-id,...> [--validator "..."]
carol-mint sweep-stale
carol-mint consolidate
carol-mint gate [--ids <DOC-id,...>]
```

- `new` scaffolds with `declared_purpose: PENDING-AGENT`; `gate` FAILS on any
  PENDING-AGENT record — a wave is not complete until an agent fills semantics.
- `consolidate` re-mints only `freshness: living` records whose source changed
  (daily 04:00Z when changed, work-arc close, owner call — profile §12).
- `sweep-stale` tags living records as expected-between-consolidations.
- Exit codes: 0 ok/current, 1 refused/stale/gate-fail, 2 usage.

Tests: `bash scripts/catalog/test-carol-mint.sh` — 15 checks incl. the refusal
matrix (unknown record, missing source, existing id, lock contention, duplicate
receipt, PENDING-AGENT gate). Offline, sandboxed via `CAROL_MINT_ROOT`.
