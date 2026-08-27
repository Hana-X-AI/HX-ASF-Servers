# P3-tools-streaming — Partition Summary

- Work order: WO-OMNI-TRINITY-LEDGER-001 · Partition: P3-tools-streaming
- Producer: trinity · Date: 2026-08-27 (UTC) · Ledger: `P3-tools-streaming.json` (26 entries, 106 source refs)
- Corpus: `/opt/tkv-local/OmniRoute-release-v3.8.51` (READ-ONLY; identity VERIFIED 2026-08-27 per `07-source-provenance-receipt.md`; no writes, no builds, no node/npm runs)
- Truth-state labels: **FACT** = verified in source at the cited line · **UPSTREAM** = bundled-doc/in-repo-record claim (drift-prone) · **INFERENCE** = producer reasoning, labeled in place

## Startup receipt

```text
[TRINITY KNOWLEDGE REVIEW COMPLETE]
Agent: Trinity
Goal Contract: GOAL-OMNI-TRINITY-LAYER0 v1 (WO-OMNI-TRINITY-LEDGER-001, partition P3)
Target Host/Environment: read-only source work from hxs-5 — no host target
Source Corpus: /opt/tkv-local/OmniRoute-release-v3.8.51 (DOC-tkv-corpus-omniroute)
Reviewed At: 2026-08-27T06:56Z
Source Identity: VERIFIED 2026-08-27 by content-sensitive proof (07-source-provenance-receipt.md)
Installed Identity: NOT INSTALLED (Layer 0; no host contact this partition)
Relevant Knowledge: charter.md, profile.md, 05-work-order, 06-context-packet, repo AGENTS.md, P2 sibling ledger (shape reference)
Allowed Change Surfaces: read-only corpus reads; ledger writes under pilots/PILOT-OMNIROUTE-LAYER0-001/ledger/
Known Drift/Risks: in-tree AGENTS.md/CLAUDE.md = untrusted upstream guidance; removed mechanisms (tool cloaking) risk resurrection from stale docs
Rollback Ready: YES (read-only — nothing to roll back)
Task May Proceed: YES
```

## Coder-X receipts (model contract)

- Endpoint: `http://192.168.50.201:11434` (hxs-2) · alias `hx-qwen3.6-coderx-64k` — only alias used
- Identity/health verified BEFORE first call (2026-08-27T06:55Z): `/api/version` → `0.32.15`; `/api/ps` → model resident, digest `ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1` (matches expected `ec9ebe08a824…`), `size == size_vram == 17,815,411,094` (fully VRAM-resident), `context_length == 65536` — **PASS**
- Calls: **2** bounded analysis prompts (source excerpts only, no credentials; temperature 0):
  1. Streaming/cancellation/usage architecture check → no contradictions; confirmed 499-for-disconnect + skip-failover coherence; flagged TTFT/cost/quota seams (already evidenced: `streamTiming.ts:46`, `streamingCost.ts:19`, `streamingQuotaShare.ts:20`, `tokenLimitCounter.ts:257`) and SSE-resume absence (verified, CAP-P3-025)
  2. Tool-calling/structured-output check → no contradictions; judged dormant `toolPolicy` plausible (dead code, chatCore.ts would be the wire point); flagged `tool_choice` as a possible gap — **refuted deterministically**: `toResponses.ts:359` translates tool_choice Chat→Responses (275 corpus matches); cited in CAP-P3-010
- Coder-X outputs used as corroboration only; every cited file:line was re-verified deterministically by the producer (scripted existence check + symbol-at-line spot check)

## Tool-call and structured-output surfaces (evidence)

- **Capability gate** [FACT]: direct/pinned requests with `tools[]` to a tool-incapable model are hard-blocked with an explicit error (`toolCallingRequiredCheck.ts:19`, wired at `chatCore.ts:2738`) — no silent strip; combos exempt (failover handled upstream in comboStructure).
- **Definition normalization** [FACT]: mixed tool shapes → canonical `{type:"function"}` (`openAICompatibleTools.ts:5`, wired `chatCore.ts:2386`); Responses-API formats pass through untouched; missing Claude tool `type` defaults to `"custom"` (`claudeToolDefaults.ts:19`).
- **Name identity ledger** [FACT]: alias-and-restore for over-long/prefixed tool names across request, non-streaming, and streaming paths (`toolCallHelper.ts:61,131`; `passthroughToolNames.ts:6,53,76`; `requestToolIdentity.ts:62`; `stream.ts:592`). Id/result repair: `ensureToolCallIds` (9-char Mistral mode), `fixMissingToolResponses`, `stripOrphanedToolResults` (`toolCallHelper.ts:180,303,355`).
- **Streamed arguments** [FACT]: `appendToolCallArgumentDelta` (`toolCallArguments.ts:41`) — verbatim delta append, dedup only unambiguous snapshot repeats, object-fragment stringification (#3701/#6459); fuzzy overlap explicitly rejected as silent-truncation risk.
- **Text-protocol tool calls** [FACT]: `[Tool call: name] Arguments: {json}` parser with zero-width stripping and partial detection (`textualToolCall.ts:57`); Cursor Composer sentinel parser (`composerToolCalls.ts:1`).
- **Per-tool argument shims** [FACT]: `TOOL_SHIMS` registry (`toolCallShim.ts:71`) — e.g. Claude Code `Read` clamped to limit ≤2000 before re-emission as Claude `input_json_delta`.
- **Schema sanitization** [FACT]: `sanitizeAntigravityToolPayload` strips `enumDescriptions` (`toolCloaking.ts:39`, applied at `executeAttempt.ts:275`); `toolSchemaSanitizer.ts` strips null enum entries for strict validators (Moonshot).
- **History flattening** [FACT]: structured tool turns → prose when tools are stripped for a prose-only leg (`flattenToolHistory.ts:46`, applied `unsupportedParamsStrip.ts:45`).
- **Structured output** [FACT]: `response_format` per-target mapping — Claude: system-prompt JSON instruction (`openai-to-claude.ts:471`); Gemini: `responseMimeType`/`responseSchema` (`openai-to-gemini.ts:593`); Responses API: `json_schema`/`json_object`/`text.format` (`openai-responses.ts:176`, `toResponses.ts:36`, `translator/index.ts:123`); DefaultExecutor downgrade/strip for rejecting providers (`default.ts:623,679`). `tool_choice` translated Chat→Responses (`toResponses.ts:359`).
- **Dormant policy** [FACT]: `src/lib/toolPolicy.ts` allowlist/denylist engine (`TOOL_POLICY_MODE`, default disabled) has **zero call sites** corpus-wide — AVAILABLE-DISABLED (CAP-P3-011).

## Streaming / cancellation / errors / finish reasons

- **Core transform** [FACT]: `createSSEStream` (`stream.ts:637`) — TRANSLATE/PASSTHROUGH modes, idle-timeout, canonical TTFT/ITL (`streamTiming.ts:46`), per-format `[DONE]` suppression (Claude/Antigravity SDKs break on trailing `[DONE]`).
- **Pipeline** [FACT]: fixed order disconnect-aware pipe → PII (flagged) → progress (opt-in) → heartbeat (15s default, format-shaped, `OMNIROUTE_SSE_COMMENTS` gate) → model-echo (`streamingPipeline.ts:62`, wired `chatCore.ts:5819`; `sseHeartbeat.ts:93`); early pre-TTFT keepalive for strict idle-read clients (`earlyStreamKeepalive.ts:3`).
- **Cancellation** [FACT]: `createStreamController` (`streamHandler.ts:236`, wired `chatCore.ts:2954`) bridges client abort signals, distinguishes deadline aborts from disconnects; disconnects skip failover/cooldown; #9653 grace handler prevents false 499 on disconnect-after-complete (`streamFailureFinalization.ts:48`); pipeline errors → 499 `client_disconnected` vs 502 (`:201`).
- **Errors** [FACT]: failure finalizers record once + persist failure usage (`streamFailureFinalization.ts:141`, wired `chatCore.ts:5716`); per-format SSE error frames (`streamErrorFormat.ts:81`); upstream 4xx verbatim passthrough for Claude Code capability recovery — refused on 401/403/407, internal-path, or credential-pattern bodies (`upstreamErrorPassthrough.ts:30,16`; #10898-sec hardening).
- **Finish reasons** [FACT]: canonical mapping `max_tokens→length`, safety family→`content_filter` (`finishReason.ts:64`); abort reasons (malformed_function_call etc.) deliberately NOT collapsed to `stop`/`end_turn` (`:30,39`); malformed tool calls synthesized into `tool_calls` + `finish_reason:"tool_calls"` for OpenAI clients (`:59`); non-streaming responses carrying tool_calls get forced `finish_reason:"tool_calls"` (`passthroughToolNames.ts:90`, wired `chatCore.ts:4975`).
- **Guards** [FACT]: empty-stream rejection (#9268, `streamEmptyChoices.ts:1`); opt-in truncated-stream recovery, default OFF (`streamRecovery.ts:1` — AVAILABLE-DISABLED, CAP-P3-018).
- **Dormant trackers** [FACT]: `src/sse/services/streamState.ts` state machine and `src/shared/utils/streamTracker.ts` metrics tracker have no production imports (tests/doc-script only) — LAB-ONLY (CAP-P3-020).

## Usage accounting behavior

- **Extraction** [FACT]: streaming (`usageTracking.ts:665` — Claude message_start/delta with cache fold, Responses response.completed, Gemini) and non-streaming (`usageExtractor.ts:5` — OpenAI incl. DeepSeek flat cache fields and xAI `cost_in_usd_ticks`, Claude input+cache sum, Responses, Gemini `usageMetadata` with thoughts folded into completion).
- **Client-visible shaping** [FACT]: post-#8331 the safety buffer stays OUT of client-visible metering except Claude-Code-compatible paths (`context_budget_*` fold-back); empty/all-zero usage → content-length estimate (`clientUsageBuffer.ts:100,54`; wired `chatCore.ts:5040`).
- **Persistence** [FACT]: `saveRequestUsage` (`usageHistory.ts:641`) — SQLite `usage_history` insert with same-second natural-key dedup; pending-request lifecycle (`:264,432`); facade `usageDb.ts:21`. Success paths: `streamingUsageStats.ts:72` / `nonStreamingUsageStats.ts:81` (fire-and-forget row + per-key billable counter, 200-only for streams). Failures: zeroed `success:false` rows (`failureUsage.ts:11`). Pre-dispatch rejections write BOTH `call_logs` and `usage_history` (`rejectedRequestUsage.ts:49`). Cost and shared-quota consumption attach on stream completion (`streamingCost.ts:19`, `streamingQuotaShare.ts:20`).

## NOT-ESTABLISHED items (searched, not found)

1. **ATEM-shaped tool-call handling** (CAP-P3-024): whole-word `ATEM` across `src/ open-sse/ packages/ docs/ config/ skills/ tests/` → zero matches; case-insensitive sweep of P3 core files → zero. **Corroborates P2's finding; no correction required.**
2. **SSE resume/reconnect (Last-Event-ID)** (CAP-P3-025): no server-side `last-event-id` consumption anywhere; only dashboard client EventSource usage. Disconnected clients must re-issue the request.
3. **Decoy tool cloaking** (CAP-P3-026): `cloakAntigravityToolPayload` / `AG_DECOY_TOOLS` / `AG_TOOL_SUFFIX` removed upstream in v3.8.49 (#8013) per `config/quality/test-masking-allowlist.json:94` [UPSTREAM record, corroborated by zero grep hits]; successor sanitizer is CAP-P3-008. Recorded to prevent resurrection from stale docs.
4. **Runtime kill-switch for the SSE transform, finish-reason mapping, or usage persistence**: no feature flags found for these cores; disable paths are source-level or (usage) `shouldPersistToDisk` [searched: config/flag modules + pipeline wiring; INFERENCE that none exists beyond what is cited].

## Coverage statement

Covered: tool-calling request path (gate, normalization, name/id/result repair, argument assembly, text-protocol parsing, shims, schema sanitization, history flattening, dormant policy), structured-output translation and downgrade, the streaming core (transform, pipeline, heartbeat/keepalive, cancellation/disconnect, failure finalization, error framing/passthrough, finish-reason normalization, empty-stream guard, opt-in recovery, dormant trackers), and usage accounting (extraction, client-visible shaping, persistence/dedup, failure and rejection accounting, cost/quota-share attach points). Source hints `src/**/tool*`, `src/**/stream*`, `src/**/usage*`, `src/**/finish*`, `packages/**/tool*` were swept; `packages/` contains only `browser-pool` (no tool/streaming modules) — nothing in scope there. Executor-local tool quirks (`codex/toolCallRepair.ts`, `kiroToolCallValidation.ts`, `chatgptWebTools.ts`, `grok-web/*`, `kimiToolNames.ts`) are provider-scoped instances of the patterns above, not separate capabilities; noted, not individually entry'd. Out of scope (flagged, not assessed): MCP-server tool registry and tools (P7 agent-surface), dashboard tool cards and playground builders (P8), quota/rate-limit policy consumers and provider usage-quota fetchers (P6), routing strategies and combo internals (P1), translator pair registry itself (P2 — referenced here only as dependency CAP-P2-006/012). Nothing activated; all dispositions preliminary.

## Self-verification

- Deterministic reference check (scripted, `/tmp/trinity-p3/refcheck.py`): 26/26 entries have all 12 schema fields; **106/106 source_refs — file exists and cited line in range. PASS.**
- Spot content check (scripted, `/tmp/trinity-p3/spotcheck.py`): **99/99 load-bearing refs have the expected symbol at the cited line. PASS** (first run, zero corrections; two docstring anchors re-anchored to description/export lines — `earlyStreamKeepalive.ts:8→3`, `streamingPiiTransform.ts:1→8` — and re-verified).
- JSON validity: parsed clean. Bounded corrections used: 0 of 2 (anchor re-points were pre-finalization edits caught by the same scripted pass, not governor-disagreement corrections).
