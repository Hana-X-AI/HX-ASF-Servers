# OmniRoute v3.8.51 — Capability Ledger (Wave 0B merged)

| Field | Value |
| --- | --- |
| Date | 2026-08-27 (UTC) |
| Program | PILOT-OMNIROUTE-LAYER0-001 (p11) |
| Producer | trinity (owner-ratified 2026-08-27, KDD-0008) — eight partition tasks, Coder-X bounded execution under the local-model contract |
| Verification | every entry's every source_ref grep-verified by the producer's scripted pass; governor spot-checks 8/8 on all eight partitions; Qwen-X independent review at Wave 0C |
| Source identity | VERIFIED 2026-08-27 — `/opt/tkv-local/OmniRoute-release-v3.8.51` byte-identical (13,098/13,098 git-blob) to upstream `diegosouzapw/OmniRoute@42a13fedef8b…` |
| Totals | **367 entries · 1,325 source references · 8 partitions** |

Truth-state labels: FACT (verified at the cited line) / UPSTREAM (bundled-doc claim, drift-prone) / INFERENCE (producer reasoning, labeled in place). Dispositions are preliminary by design — nothing is active because it appears here.

## Disposition distribution (367 entries)

| Disposition | Count | Meaning |
| --- | ---: | --- |
| ACTIVE-CANDIDATE | 229 | source-present, candidate for its layer's activation decision |
| AVAILABLE-DISABLED | 74 | present and functional but off/inert by default or missing a switch/key |
| NOT-ESTABLISHED | 35 | searched honestly and not found (INFERENCE-labeled where the conclusion is reasoning from absence) |
| LAB-ONLY | 12 | present but test/doc-scoped only |
| NOT-APPLICABLE | 9 | out of HX's scope by role |
| BLOCKED | 8 | present but barred by owner rules (no-cloud, LAN-boundary, no host mutation) |

## Per-partition results

| Partition | Entries | Headline findings |
| --- | ---: | --- |
| P1 API/routing | 42 | 688 route.ts files / 102 top-level domains; `/api/v1` traffic plane vs ~100 management domains; **19 public strategies verified exactly** (+1 internal `quota-share`); docs drift (17 vs 19) recorded |
| P2 Providers/protocol | 23 | static registry **356 records / 355 excl. `auto`** vs runtime chat registry **272** vs doc claims 353/354/268/339 — all mismatch; 9 format identifiers, hub-and-spoke OpenAI translation; **zero ATEM adapter corpus-wide** |
| P3 Tools/streaming | 26 | full tool-call pipeline (assembly/repair/alias-ledger/structured-output per-target translation with documented downgrades); SSE core with per-format suppression + abort discrimination; usage accounting with billing-field hygiene; **dormant toolPolicy engine (zero call sites)** |
| P4 Security | 50 | central `src/proxy.ts` authz pipeline (fail-closed 3-class); `requireManagementAuth` in 286 routes / 56 domains; **JWT_SECRET + API_KEY_SECRET persist PLAINTEXT in SQLite** (doc claim of encrypted store is stale); AES-256-GCM ships passthrough without STORAGE_ENCRYPTION_KEY; SSRF metadata blocked, LAN default-allowed |
| P5 Persistence/config | 37 | 160 versioned migrations (docs' 148–153 = drift); convergent restart; backup API with pre-restore snapshot + integrity_check + WAL purge; config precedence DB > env > default (2 env-wins exceptions); 52 feature flags (7 restart-required); connection-row encryption wired but **plaintext-passthrough by default** |
| P6 Observability | 55 | layered health (public liveness vs aggregated monitoring with GHSA anonymous-view split); 8 rate-limit mechanisms with exact fail-open/fail-closed semantics (incl. fail-OPEN-on-Redis-outage by design); 3 logging stacks + universal redaction net; quota engine fail-open by design; budget evaluator fail-closed |
| P7 Agent surfaces | 60 | collision breakdown (orchestration ×9, catalog ×4, authority ×9 — distinct CAP IDs per the P7 §2 lists, batch-22 corrected); **highest-risk: copilot LLM driver executes model output as host CLI commands** (LOCAL_ONLY tier only); Conductor hub + ACP env-inheritance runners-up; 6 BLOCKED by owner rules; disabled-by-default NOT code-enforced for skills execution + background jobs |
| P8 Packaging/modes | 74 | one npm package + one Next-16 standalone build feeds all modes; CLI ~80 command families + 31-tag OpenAPI tree; **encrypted CLI backups are WRITE-ONLY** (no restore path); **`--cloud` backup flag POSTs to a nonexistent endpoint**; runner-cli container flavor BLOCKED; Electron shell loopback-pinned |

## Data-integrity / security findings for the owner-decision packet

1. **Plaintext secrets at rest** (CAP-P4-039, CAP-P5-030): auto-generated `JWT_SECRET`/`API_KEY_SECRET` persist plaintext in SQLite `key_value`; the "dedicated encrypted store" doc claim is refuted drift. **Layer-1 requirement (owner-ratified 2026-08-27): env-provision both secrets AND set `STORAGE_ENCRYPTION_KEY`** — never accept defaults.
2. **Backup encryption is theater end-to-end**: server scheduler refuses encrypted schedules (no non-interactive passphrase); CLI `--encrypt` writes genuine AES-256-GCM but **no restore path exists** (`createDecipheriv` imported, never called; restore matches plaintext names only); CLI `--cloud` POSTs to `/api/db-backups/cloud`, **an endpoint absent from the pinned source**. Treat backup encryption/remote-upload as nonexistent (CAP-P8-905/906, CAP-P5-036).
3. **No ATEM adapter** (P2, corroborated P3): Meta-X traffic through OmniRoute would be OpenAI-compatible only, or a future adapter (Layer-3/4 question).
4. **Dormant capabilities worth deliberate decisions**: `toolPolicy.ts` allowlist/denylist engine (zero call sites), adaptive admission (shadow-mode), 60s→15s session monitor, OTLP telemetry sink, npm self-update, desktop autoDownload.
5. **Owner-rule BLOCKED surfaces**: 3 tunnels, Conductor hub, cloud agents/CLI, MITM bridge, runner-cli container flavor — 8 BLOCKED entries with evidence.

## Citation-contract measurement (owner-ratified experiment)

| Partition | Coder-X drafted lines wrong | Rate |
| --- | ---: | ---: |
| P1 (baseline, pre-contract) | 21/59 | 35.6% |
| P5 (first contract run) | 1/25 | 4.0% |
| P6 | 2/70 | ~3% |
| P7 | 1/32 | 3.1% |
| P8 | **0/46** | **0.0%** |

The numbered-excerpt + anchor-citation contract eliminated the offset-arithmetic failure class. Residual class: path-attribution slips (harness-caught) — the Wave-0C skill candidate should add "copy the path verbatim from the chunk header" + a path-existence post-check and ~10-line chunk overlap.

## Drift register (bundled-doc claims refuted by source)

`3.8.40/3.8.50` version strings in `docs/ops/*`; provider counts 353/354/268/339 (source: 356/355 static, 272 runtime); strategy count 17 in `open-sse/services/AGENTS.md` (source: 19); "dedicated encrypted store" in `src/lib/db/AGENTS.md` (source: plaintext); migration count 148–153 (source: 160); omni-mcp "32 scopes" (measured: 17); `OMNIROUTe_API_KEY` env-var typo in `/api/assess`; agent-card version fallback `1.8.1`.

## NOT-ESTABLISHED policy

35 entries record honest absences (searched-not-found), each with its search scope. Where the conclusion is producer reasoning from absence rather than a directly verified fact, the entry carries the declared INFERENCE label (batch-20 convention). Absence at this commit is evidence, not a permanent verdict.

## Machine form

`08-capability-ledger.json` — all 367 entries (12 schema fields + partition), merged deterministically from the eight partition JSONs (which remain the per-partition source of record alongside their summaries and reference-check outputs).
