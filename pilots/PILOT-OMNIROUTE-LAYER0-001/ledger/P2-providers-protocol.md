# P2-providers-protocol — Partition Summary

- Work order: WO-OMNI-TRINITY-LEDGER-001 · Partition: P2-providers-protocol
- Producer: trinity · Date: 2026-08-27 (UTC) · Ledger: `P2-providers-protocol.json` (23 entries, 110 source refs)
- Corpus: `/opt/tkv-local/OmniRoute-release-v3.8.51` (READ-ONLY; identity VERIFIED 2026-08-27 per `07-source-provenance-receipt.md`; no writes, no builds, no node/npm runs)
- Truth-state labels: **FACT** = verified in source at the cited line · **UPSTREAM** = bundled-doc claim (drift-prone) · **INFERENCE** = producer reasoning, labeled in place

## Startup receipt

```text
[TRINITY KNOWLEDGE REVIEW COMPLETE]
Agent: Trinity
Goal Contract: GOAL-OMNI-TRINITY-LAYER0 v1 (WO-OMNI-TRINITY-LEDGER-001, partition P2)
Target Host/Environment: read-only source work from hxs-5 — no host target
Source Corpus: /opt/tkv-local/OmniRoute-release-v3.8.51 (DOC-tkv-corpus-omniroute)
Reviewed At: 2026-08-27T06:36Z
Source Identity: VERIFIED 2026-08-27 by content-sensitive proof (07-source-provenance-receipt.md)
Installed Identity: NOT INSTALLED (Layer 0; hxs-8 has no node/npm — rick's readiness evidence)
Relevant Knowledge: charter.md, profile.md, 05-work-order, 06-context-packet, 07-provenance-receipt, repo AGENTS.md
Allowed Change Surfaces: read-only corpus reads; ledger writes under pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/
Known Drift/Risks: provider-count drift (below); 3x AGENTS.md + 87x CLAUDE/GEMINI in-tree = untrusted upstream guidance
Rollback Ready: YES (read-only — nothing to roll back)
Task May Proceed: YES
```

## Coder-X receipts (model contract)

- Endpoint: `http://192.168.50.201:11434` (hxs-2) · alias `hx-qwen3.6-coderx-64k` — only alias used
- Identity/health verified BEFORE first call (2026-08-27T06:35Z): `/api/version` → `0.32.15`; `/api/ps` → model resident, digest `ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1` (matches expected `ec9ebe08a824…`), `size == size_vram == 17,815,411,094` (fully VRAM-resident), `context_length == 65536` — **PASS**
- Calls: **2** bounded analysis prompts (source excerpts only, no credentials; temperature 0):
  1. Registry-layer/count verification → confirmed 3 registry layers, arithmetic 356, doc deltas (353/354 vs 356/355; 268 vs 272)
  2. Translation architecture verification → confirmed hub-and-spoke via OpenAI; flagged pair-less formats `codex`/`openai-response`; confirmed DefaultExecutor credential-leak mechanism (#6699)
- Coder-X outputs used as corroboration only; every cited file:line was re-verified deterministically by the producer (grep + scripted existence check)

## Provider registry shape [FACT]

Three distinct registry layers exist in source:

1. **Static provider catalog** — `src/shared/constants/providers/*.ts`, 10 typed collections behind the barrel `providers.ts:5-19`, grouped into 9 dashboard categories by `STATIC_PROVIDER_CATALOG_GROUPS` (`src/lib/providers/catalog.ts:108`; resolution order at :168-178; `system` collection excluded from groups). Per-collection record counts (deterministic, two independent grep patterns, zero duplicate ids):

   | Collection | File | Records |
   |---|---|---|
   | noauth | `noauth.ts:5` | 13 |
   | oauth | `oauth.ts:7` | 25 (24 multi-line + 1 inline `github` at :134) |
   | web-cookie | `web-cookie.ts:5` | 35 |
   | local | `local.ts:5` | 14 |
   | search | `search.ts:5` | 16 |
   | audio | `audio.ts:5` | 12 |
   | upstream-proxy | `upstream-proxy.ts:5` | 2 |
   | cloud-agent | `cloud-agent.ts:5` | 3 |
   | system | `system.ts:5` | 1 (`auto`, systemOnly) |
   | apikey | `apikey/index.ts:14` (6 family files) | 235 (17+25+94+29+43+27) |
   | **Total** | | **356** (355 excl. system `auto`) |

2. **Runtime chat-model REGISTRY** — `open-sse/config/providers/index.ts:274`, **272** plain `key: provider` entries (lines 274-547, no spreads), carrying format/baseUrls/headers/oauth/models per provider; `generateLegacyProviders()` (`open-sse/config/providerRegistry.ts:34`) re-projects to the legacy PROVIDERS shape.

3. **Operator-added compatible nodes** — `resolveCompatibleProviderCatalogEntry()` (`src/lib/providers/catalog.ts:222`): openai-compatible / anthropic-compatible / claude-code-compatible endpoints persisted as provider connections (`src/lib/db/providers.ts:444`). Unbounded by definition; the HX-relevant path for LAN endpoints (e.g. Ollama).

Supporting seams: executor dispatch registry (144 aliases / 119 lazy modules, `open-sse/executors/index.ts:30`, `getExecutor` :244); translator pair registry (`open-sse/translator/registry.ts:20`); service-kind registries (search 19 at `open-sse/config/searchRegistry.ts:38`, plus audio/image/video/embedding/moderation/ocr/rerank/upscale/music).

## Adapter / translation paths (evidence)

- **Formats** [FACT]: 9 identifiers at `open-sse/translator/formats.ts:2` — openai, openai-responses, openai-response (legacy alias normalized at `open-sse/utils/streamPayloadCollector.ts:72`), claude, gemini, codex, antigravity, kiro, cursor. `codex` has no registered translation pair; codex traffic rides the openai-responses path (`open-sse/translator/request/openai-responses.ts:158` treats "codex" as an OpenAI param destination) — dormant identifier, noted not failed.
- **Engine** [FACT]: pair-keyed maps + side-effect bootstrap (`bootstrap.ts:6-24`: 9 request + 9 response modules); `translateRequest` (`index.ts:306`) with hub-and-spoke fallback via OpenAI (:456); `translateResponse` (:794, fallback :817); `needsTranslation` (:864).
- **Registered request pairs** (11): antigravity→openai (:374), claude→gemini (:322), claude→openai (:557), gemini→openai (:237), responses↔openai both ways (:895-896), openai→claude (:832), openai→cursor (:226), openai→gemini (:841), openai→antigravity (:850), openai→kiro (:1056).
- **Registered response pairs** (12): claude→openai (:405), cursor→openai (:30), gemini→claude (:367), antigravity→claude (:368), gemini→openai (:820), antigravity→openai (:821), kiro→openai (:211), responses↔openai (:1464-1465), openai→antigravity (:145), openai→claude (:545), openai→gemini (:14).
- **Responses transformer**: `createResponsesApiTransformStream` (`open-sse/transformer/responsesTransformer.ts:192`) — Chat Completions SSE → Responses API SSE for Codex-class clients.
- **Param stripping**: `stripUnsupportedParams` (`open-sse/translator/paramSupport.ts:141`, STRIP_RULES export :251), applied in DefaultExecutor (`open-sse/executors/default.ts:22`, call at :873).
- **Alternate protocol switch**: per-connection `providerSpecificData.targetFormat` against declared `alternateFormats` (`open-sse/config/providers/alternateFormats.ts:15`, `shared.ts:229`).
- **Dispatch guards** [FACT]: cloud-agent-only providers (jules) and all search providers hard-400 on the chat path (`open-sse/executors/index.ts:231,242`) — added after the #6699/#10274 incidents where DefaultExecutor's `PROVIDERS.openai` fallback sent real provider keys to OpenAI's endpoint. The fallback still exists for unguarded providers; flagged high-risk in CAP-P2-004.

## Count findings (drift register)

| Claim | Value | Source of claim | Source-derived value | Verdict |
|---|---|---|---|---|
| Registered providers | 353 | README.md:645,649 [UPSTREAM] | 356 records / 355 excl. system | **MISMATCH** (−3 / −2) |
| LLM providers | 354 | AGENTS.md:49, llm.txt:280,478 [UPSTREAM] | 356 / 355 | **MISMATCH** (−2 / −1) |
| Provider count | 339 | candidate profile §4.2 [CANDIDATE] | 356 / 355 | **MISMATCH** (−17 / −16) |
| Chat model registry | 268 | README.md:649 [UPSTREAM] | 272 REGISTRY entries | **MISMATCH** (−4) |
| Catalog-marked free | 154 | README.md:645 [UPSTREAM] | 153 `hasFree: true` lines | **MISMATCH** (−1) |

No reconciliation path (hidden=4, deprecated=2, system=1) lands exactly on any doc figure [FACT — arithmetic]. Resolution per the corpus rule: source outranks bundled docs. Ledger tests must assert source counts (356/355/272), never doc counts. No test in `tests/` asserts a provider count today [FACT — grep over tests/].

## NOT-ESTABLISHED items (searched, not found)

1. **ATEM/native protocol adapter** (CAP-P2-023): case-sensitive whole-word `ATEM` across `src/ open-sse/ packages/ docs/ config/` → zero matches; case-insensitive `atem` → substring noise only (i18n, unrelated identifiers). No ATEM adapter, format, or doc exists. The extant native paths are claude/gemini/codex/antigravity/kiro/cursor (CAP-P2-006…011).
2. **Runtime feature-flag / kill-switch for the provider registry, translator, or executor fallback**: no toggle found in source; disable paths are per-connection (delete/deactivate) or source-level [searched: registry/config/flag modules; INFERENCE that none exists beyond what is cited].
3. **Test-side provider-count assertion**: none found under `tests/` — count drift is currently undetectable by the suite.
4. **Spawn trigger path for embedded services** (9router/cliproxyapi): plugin registry and manifest seam verified (`providerPlugins/registry.ts:20`), but the operator action that starts the child process was not traced this partition — flagged INFERENCE in CAP-P2-022 for P7/P8 follow-up.

## Coverage statement

Covered: provider registry (static catalog, runtime REGISTRY, compatible nodes), provider classes (DefaultExecutor + 144-alias specialized executor surface), protocol adapters and translation paths (all 9 formats, all 23 registered pairs, transformer, param stripping, alternate-format switch), persistence/OAuth/validation/management-API couplings, service-kind registries, and the disabled-by-default classes inside this partition (web-cookie, cloud-agent, embedded upstream-proxy). Source hints `**/provider*/**`, `open-sse/**`, `src/**/adapter*`, `src/**/translat*` were swept; `adapter*`/`translat*` globs resolve to the translator/transformer modules above (no separate `src/**/adapter*` tree exists). Out of scope (flagged, not assessed): authN/authZ on management routes (P4), encryption-at-rest of connection rows (P5), cloud-agent task API (P7), packaging/installers (P8), routing strategies (P1). Nothing activated; all dispositions preliminary.

## Self-verification

- Deterministic reference check (scripted): 23/23 entries have all 12 schema fields; 110/110 source_refs — file exists and cited line in range. **PASS** (run twice; second run after 3 line corrections: `default.ts:24→22`, `executors/index.ts:255→261`, `providerPlugins/registry.ts:19→20`, plus route path `[provider]/route.ts→[provider]/[action]/route.ts` and `responsesTransformer.ts:19→192`).
- Spot content check: 19 load-bearing refs grep-verified for expected symbol at cited line. **PASS** after corrections.
- JSON validity: parsed clean both runs. Bounded corrections used: 1 of 2.

## Correction — field count (2026-08-27, review batch 19, labeled)

The certification line in this document that reads "11 schema fields" is a
wording error: the packet's entry_schema has always carried **12 keys**, and
every entry in the paired JSON carries all 12. Recorded: prior count (11,
wrong), correction (12, canonical), revalidation (governor deterministic
key-count over the JSON, 2026-08-27 — see
`field-count-revalidation-2026-08-27.txt` in this directory: PASS). The
historical "11" claim above is preserved per the append-only convention; this
addendum is the current resolution.
