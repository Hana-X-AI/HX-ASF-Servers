# Quality Gate Decision — GATE-PILOT-KK3-JOHN-002

```text
[QUALITY GATE DECISION]
Gate ID: GATE-PILOT-KK3-JOHN-002
Goal ID/Version: GOAL-OLLAMA-AUDIT-HXS4-001 v1
Work Order: WO-OLLAMA-AUDIT-HXS4-001
Artifact Identities/Hashes: sha256sums.txt (regenerated at gate)
Success Conditions: SC-01..SC-11 — all proven
Evidence Reviewed: 03 receipt, 04 plan, 05 command log (12 rows),
  06 raw evidence (9 files), 07 report, 08 summary
Result: PASS
Failed/Unexecuted Requirements: 1 NOT RUN (HW-05 — no authorized storage
  benchmark; by design)
Contradictions: none blocking; F1 (corpus source 0.32.11 vs installed 0.32.9)
  correctly declared NOT version-matched, no source-based claims made
Residual Risk: load-time VRAM tightness on the 8 GB card (recoverable, watch
  item); blob-level store permissions unverifiable without privilege
Control-Plane Boundary Preserved: YES — governor executed zero operational
  commands; all probes ran in John session john-initial-20260824-02
Authorized Transition: PASSED -> PILOT_COMPLETE (pending owner acceptance)
Decision Timestamp: 2026-08-24T10:45Z
```

## Gate checks performed by the governor

| Check | Method | Result |
| --- | --- | --- |
| Governor artifact integrity | sha256 of 01/02a vs pre-dispatch values | Match — untouched |
| Knowledge review precedes probes | Receipt 10:28:39Z vs evidence window 10:32–10:37Z | Proven (SC-01) |
| Fail-closed rule | Receipt evaluated authority/baseline; G1-type stop not triggered because baseline EXISTS here | Rule exercised, correct outcome |
| Roster check | `agents/` consulted first; craig treated as archived | Proven (SC-11) |
| Target identity | hostname hxs-4, 192.168.50.203/24, machine-id matches discovery record | Proven (ID-01) |
| Matrix statuses | Count in 07 | 28 PASS / 1 NOT RUN — matches claim (SC-03) |
| Read-only compliance | Prohibited-verb scan of command log | Zero mutations (SC-06) |
| Secret hygiene | Pattern scan of evidence + askpass helper deleted, never logged | Clean (SC-04) |
| Spot checks | Loopback-only 127.0.0.1:11434; version 0.32.9 on CLI/API; single model qwen3.5:9b-q4_K_M digest 6488c96fa5fa; GPU isolation pinned to RTX 5060 with Vulkan disabled | All confirmed in raw evidence |
| Budgets | 1 session, 0 corrections, 0 retries | Within limits |
