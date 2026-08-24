# Process Learning Record — PILOT-KK3-JOHN-OLLAMA-AUDIT-002

## Run telemetry

- John sessions: 1; corrections: 0; retries: 0
- Commands logged: 12 (all read-only, all via SSH to hxs-4)
- Tests: 29 defined, 28 executed, 28 PASS, 1 NOT RUN
- Gate outcome: PASS first pass
- Wall time: receipt 10:28Z, evidence 10:37Z, gate 10:45Z

## What the 001 FAIL fixed

- Intake pre-flight ran before commissioning (one SSH command) — the target was
  verified to actually have the component.
- Roster check happened first — zero time spent on craig; he was correctly
  treated as archived history.
- Fail-closed knowledge review was exercised and passed legitimately, because a
  baseline exists here — the rule did not have to fire to prove it works.
- Valid target made the full audit matrix meaningful: models, residency, GPU
  isolation, exposure, journals.

## New findings for the process

- SSH-based remote execution from the John session worked cleanly with the
  askpass pattern; credential never logged. This is the reusable pattern for
  fleet-wide audits until key-based access is deployed.
- John froze his own sha256sums.txt this run; the governor regenerated it at the
  gate. Keep it that way: artifact freezing is a governor function.
- The version-matched source rule produced an honest F1 declaration instead of
  quiet source-based claims — the discipline held under a real mismatch.

## Ratification needs (owner)

- D1: OmniRoute remote-consumption mechanism (open since 2026-08-14 per John).
- D2: acquire 0.32.9-matched source, or authorize a deliberate pinned upgrade.
- D3: document the default-context contract (num_ctx must be set explicitly;
  OLLAMA_CONTEXT_LENGTH=65536 did not change the observed 4096 default).
