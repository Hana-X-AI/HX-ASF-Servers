# Governor evidence-verification checklist (receipt-check)

Ratified 2026-08-25 (UD5/U7). Run for every producer deliverable **before** any
acceptance is logged. A deliverable that fails any step goes back with one bounded
correction, or escalates per the approval discipline — it is never accepted around
a failed step.

## Steps

1. **Artifact exists** — non-empty, at the path the work order named, timestamped
   inside the session window.
2. **Receipt line present** — `Task May Proceed: YES/NO` or the profile's PASS
   marker, exactly once, in the producer's own completion language.
3. **Token context check** — every `FAIL` / `BLOCKED` / `NOT RUN` token read in
   context. Benign summaries ("0 FAIL, 0 BLOCKED"), quoted script failure
   semantics, and rollback-trigger mappings are acceptable. A real failure token
   stops acceptance here.
4. **Secret sweep** — `grep -F` the protected credential string plus generic
   patterns (PEM blocks, bearer tokens, `password[:=]` assignments) across the
   deliverable: zero hits, no exceptions.
5. **Governor-artifact integrity** — the work order and context packet still hash
   to the state-log proof values; any drift means the contract moved mid-flight.
6. **Claims vs live state** — material current-state claims (timeouts, versions,
   identities, resident model, unit states) spot-verified read-only against the
   live target. The document is never sole evidence for live state.
7. **Boundary conformance** — the deliverable's own mutation disclosure matches
   the work-order allowlist; an undeclared mutation stops acceptance.
8. **Completeness** — every evidence requirement from the context packet is
   present: hashes, diffs, outputs, journal excerpts, arithmetic/checklists.
9. **Honest limitations** — disclosed near-misses, unmeasured bounds, and
   substitutions are recorded in the deliverable itself, not discovered later.
10. **Handoff rule** — deliverable goes to Carol; the handoff stays OPEN until
    her catalog receipt is cited in the state log. Only then the acceptance row
    and goal-status update.

## Escalation

- Producer defect → one bounded correction with the finding stated exactly.
- Authority, safety, or identity problem → stop and escalate to the owner.
- Repeated failure class → lessons-learned entry plus a deterministic guard where
  one exists (test, check, or hook), not a memo.
