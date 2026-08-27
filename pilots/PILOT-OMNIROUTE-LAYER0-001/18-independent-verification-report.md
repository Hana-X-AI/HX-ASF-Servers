# Independent Verification Report — OmniRoute Layer 0 (Wave 0C)

| Field | Value |
| --- | --- |
| Date | 2026-08-27 (UTC), run window 10:41–10:53Z |
| Program | PILOT-OMNIROUTE-LAYER0-001 (p11) |
| Verdict | **VERIFIED** — all deterministic checks pass; all Qwen-X verdicts sound after adjudication; zero artifact discrepancies |
| Verifier call-sign | Qwen-X — hxs-1 (192.168.50.200) |
| Endpoint | http://192.168.50.200:11434 |
| Alias | `hx-qwen3.8-27b-64k` (only alias used; no substitution) |
| Digest | `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a` (matches expected `766cd9469fb4…`) |
| Role | independent verifier — producer/verifier independence held (producer Coder-X on hxs-2; verifier Qwen-X on hxs-1; never the same host) |
| Inference call count | 5 (3 for the ledger review incl. 2 bounded corrections, 1 for authority matrix + owner-decision register, 1 for the risk register) |
| Cloud statement | zero cloud anywhere in this run — all inference local on hxs-1; prompts contained artifact text and checklists only; zero credentials in model context |
| Budgets | ≤60 min: used ~12 min. ≤2 bounded corrections: used 2 (both on the ledger-review call). Stop conditions: none hit |

## 1. Verifier identity receipt (gate — passed before any review)

- `/api/version` → `0.32.15`.
- `/api/ps` at open (10:41Z) and at close (10:53Z): `hx-qwen3.8-27b-64k:latest` resident; digest `766cd9469fb4…` match; `size == size_vram == 20,463,789,012` (fully in VRAM); `context_length 65,536`; family qwen35, 27.3B Q4_K_M. ACTIVE M8-signed per the program roster.
- Identity failure would have stopped the run and escalated to Kimi-K3; it did not occur.

## 2. Deterministic results (acceptance authority)

F1. **Ledger recount — PASS, exact.** `08-capability-ledger.json`: 367 entries; per-partition P1–P8 = 42/23/26/50/37/55/60/74; disposition distribution ACTIVE-CANDIDATE 229, AVAILABLE-DISABLED 74, NOT-ESTABLISHED 35, LAB-ONLY 12, NOT-APPLICABLE 9, BLOCKED 8 (sums to 367, zero unlabeled); total source_refs 1,325. All match `08-capability-ledger.md`'s claims exactly. The eight partition JSONs independently sum to 367 entries / 1,325 refs, and a key-by-key comparison of every partition entry against the merged file found zero field mismatches.

F2. **Source-ref sample — PASS 25/25.** Seeded random sample (seed 20260827) of 25 source_refs spanning 7 of 8 partitions (P1, P2, P4, P5, P6, P7, P8). For each: the cited file exists under `/opt/tkv-local/OmniRoute-release-v3.8.51` and the cited line is within the file's line range. Zero failures.

F3. **Schema check — PASS.** All 367 entries carry exactly the 13 required keys (12 schema fields + `partition`): `id, partition, name, purpose, architectural_plane, owner_plane, preliminary_disposition, risk_class, dependencies, required_authorization, rollback_or_disable, test_contract, source_refs`. 367 unique ids.

F4. **Control-manifest YAML — PASS.** `10-control-manifest.yaml` parses clean (PyYAML safe_load); 12 top-level keys including `source_identity`, `hx_authority`, `owner_decisions` (OD-01..OD-13), `layer_map`, `non_negotiables_enforced_this_phase`.

F5. **Forbidden-token sweep — PASS.** Every occurrence of the four forbidden classes in the manifest and packet is correction or foreclosure context, never an ACTIVE claim: DeepSeek Harness appears only as "removed (never existed, KDD-0006)"; `/opt/tkv-local/omniroute` only as "rejected"/"no … knowledge root"; host firewall only as "removed"/"No host firewalls anywhere (owner rule)"/"no host firewall"; cloud only as "No cloud models or remote inference" and as OmniRoute product-surface names cited in foreclosure context (dead `--cloud` endpoint, cloud-agent collisions). Disk check: `/opt/tkv-local/omniroute` does not exist.

F6. **Artifact integrity — PASS.** All verified artifact mtimes (2026-08-27 06:49–10:40Z) predate the verification window (opened 10:41Z); no mutation during the run.

## 3. Qwen-X review (bounded calls, think:false, temperature 0.1)

Three planned reviews; five inference calls total after two bounded corrections.

- **Call 1 — disposition distribution + five sample entries** (CAP-P1-014 ACTIVE-CANDIDATE, CAP-P1-101 ACTIVE-CANDIDATE, CAP-P1-113 AVAILABLE-DISABLED, CAP-P4-900 NOT-ESTABLISHED, CAP-P7-037 BLOCKED), each presented with numbered source excerpts. Final verdicts: **6/6 sound**, each with an excerpt-line evidence_ref.
- **Call 2 — authority matrix (A1–A9) + owner-decision register (O1–O13)** against the stated program rules. Verdicts: **22/22 sound**.
- **Call 3 — risk register (R1–R12)**: does each mitigation address the stated risk within program rules. Verdicts: **12/12 sound**.

Corrections (recorded per contract): call 1 initially returned a single JSON object instead of the required array, and a hardened re-ask repeated the truncation with an unstable verdict flip on item 1 (sound → unsupported). Root cause: the `format: json` request parameter induced single-object output — an incomplete-structured-answer instance of the known reasoning-model empty-response class. Re-asked without `format` and with an explicit output template: complete 6-item array, stable verdicts. The item-1 flip was adjudicated deterministically (D1 below); the model's final "sound" agrees with the deterministic evidence.

## 4. Adjudications (deterministic, against the artifacts)

No unsound/unsupported flags survived into the final responses; the one unstable intermediate flag and the load-bearing claims were adjudicated by direct source evidence:

- D1. **Disposition distribution (call-1 item 1) — sound.** Recount (F1) proves the six classes partition all 367 entries with zero unlabeled; the intermediate "unsupported" flip was a format-failure artifact, not evidence. Resolved by discriminating evidence (the recount), not confidence.
- D2. **CAP-P4-900 (no ssrf-named module) — sound.** `find src -iname '*ssrf*'` returns zero implementation files; matches exist only under `tests/` (test-scoped, consistent with the entry's stated scope). The SSRF guard lives at `src/shared/network/outboundUrlGuard.ts:9` as cited.
- D3. **CAP-P1-113 (quota-share internal-only) — sound.** `src/shared/constants/routingStrategies.ts:31` places `quota-share` solely in `INTERNAL_ROUTING_STRATEGY_VALUES`; the public `ROUTING_STRATEGY_VALUES` array contains exactly 19 strategies — corroborating the P1 headline "19 public strategies verified exactly (+1 internal)".
- D4. **CAP-P4-039 / CAP-P5-030 (plaintext secrets at rest) — sound, source-confirmed.** `src/lib/db/secrets.ts:19-24` persists with `JSON.stringify(value)` and no encryption call; `src/instrumentation-node.ts:125-135` auto-generates and persists JWT_SECRET at boot. The packet's risk R1 and ratified OD-13 rest on a verified fact.
- D5. **P4 headline (requireManagementAuth in 286 routes) — exact.** `grep -rl requireManagementAuth src/app --include=route.ts | wc -l` = 286.
- D6. **P1 headline (688 route.ts / 102 domains) — exact.** `find src/app/api -name route.ts` = 688; top-level domains under `src/app/api/` = 102. (A naive `src/app`-wide count yields 697; the 9-file delta is non-API routes — `.well-known`, livez/healthz/readyz, a2a, authorize, docs, dashboard-embed — the ledger's API-scoped basis reconciles exactly.)

## 5. Observations (do not affect the verdict)

- O1. A reference checkout `/opt/tkv-local/deepseek-harness-master` (the upstream DeepSeek open-source project, developer preview) exists in the knowledge base. KDD-0006's "never existed" is scoped to a *deployed* HX execution foundation — per `PILOT-HXS2-CODERX-BACKEND-001/01-state-log.md` row 1, "verification found no deployed DeepSeek Harness anywhere; owner confirmed 2026-08-26 it has never existed". The manifest's correction stands within its scope; the checkout is reference material, not a deployment. No contradiction; recorded for precision.
- O2. Qwen-X + Ollama `format: json` interacts badly with array-output instructions (single-object truncation, verdict instability). Verifier harnesses should omit `format` and supply an explicit output template with a stated object count. Recorded as a tooling lesson for the Wave-0C skill candidate.

## 6. Final verdict

**VERIFIED.** Exact reasons: (1) every quantitative claim in the ledger .md reproduces exactly from the machine form (F1); (2) sampled citations resolve to real files and in-range lines (F2); (3) schema, manifest parse, and forbidden-token constraints hold without exception (F3–F5); (4) artifacts were static throughout verification (F6); (5) the independent verifier's 40 structured verdicts are uniformly sound, and the single instability was resolved by discriminating deterministic evidence (D1); (6) headline security and routing claims were independently re-derived from source (D3–D6). Layer 0's evidence base stands as presented.

Next step: this report is Markdown-only per the routine-record convention; if KK3 classifies it as a major document, queue it for the wiki manifest and dual-format render.
