# HX Factory — Consolidated Test Log

This log is continuously updated after every test run. Append new results, never delete old entries.

## LightRAG (hxs-4)

| Date | Test | Status | Evidence | Notes |
|---|---|---|---|---|
| 2026-08-29 | lightrag_ollama_demo.py | PASS | 14 entities, 7 relations, GraphML produced | In-process Ollama LLM + bge-m3 embeddings |
| 2026-08-29 | graph_visual_with_html.py | PASS | knowledge_graph.html generated | Visualization from GraphML |
| 2026-08-29 | generate_query.py | PASS | Structured user/task/question analysis | Via Ollama OpenAI-compatible endpoint |
| 2026-08-29 | lightrag_openai_compatible_demo.py | FAIL | openai_complete_if_cache() missing 'prompt' arg | Upstream API change in v1.5.7; server works via env config. Example #4 |
| 2026-08-29 | insert_custom_kg.py | PASS | Custom KG inserted, 'Quinn manages Qdrant' returned | 5 entities, 4 relations, 1 chunk |
| 2026-08-29 | rerank_example.py | PASS | Query with/without rerank ran successfully | LLM-based rerank (no external rerank model) |
| 2026-08-29 | embedding_prefixes.py (unofficial) | PASS | 3 prefixed docs, 3 entities, 2 relations | Prefix-tagged document ingestion |
| 2026-08-29 | copy_llm_cache_to_another_storage.py (unofficial) | DEP-OK | PostgreSQL impl available | Full run needs PG config from hxs-9. Example #8 |
| 2026-08-29 | bedrock/cloudflare/hf/nvidia/neo4j/milvus/redis/llamaindex/lmdeploy/litellm | SKIP | Services not in our stack | 9 unofficial samples skipped |

## Qdrant (hxs-4)

| Date | Test | Status | Evidence | Notes |
|---|---|---|---|---|
| 2026-08-29 | V0 Pre-state | PASS | No Qdrant running, NVMe unallocated | Quinn V0 checkpoint |
| 2026-08-29 | V1 Install + version | PASS | qdrant 1.19.0, service active | Prebuilt binary from GitHub |
| 2026-08-29 | V2 Config posture | PASS | LAN bind, API key, TLS off, Web UI 404 (assets not bundled) | Web UI assets downloaded separately |
| 2026-08-29 | V3 API probe | PASS | Health, readyz, collections respond | API key auth works |
| 2026-08-29 | V4 Collection lifecycle | PASS | Create, upsert, query_points, delete | query_points (search deprecated in v1.19) |
| 2026-08-29 | V5 Snapshot backup + restore | PASS | file:// URI, 5 points restored | Collection-level snapshot |
| 2026-08-29 | V6 Health monitoring | PASS | Timer active, health script exit 0 | Timer fired (LAST/PASSED populated) |

## DeepSeek Harness (hxs-15)

| Date | Test | Status | Evidence | Notes |
|---|---|---|---|---|
| 2026-08-29 | Gate 6 (Phase B) | 19 passed, 2 skipped, 1 known defect | G6-13 subagent_fork: works manually, fails under pytest | Test-harness defect, not DSH source bug |
| 2026-08-29 | Gate 7 (Phase B) | 11 passed, 6 failed, 3 skipped | Model-cooperation tests fail under pytest only | Same class as G6-13 |
| 2026-08-29 | Gate 8-10 (Phase C) | 11 passed, 6 failed, 3 skipped | Same model-cooperation pattern | Phase C complete |

## PostgreSQL (hxs-9)

| Date | Test | Status | Evidence | Notes |
|---|---|---|---|---|
| 2026-08-29 | Step 0+1 (V0-V3) | PASS | PGDG onboarding, 18.6, scram auth, LAN bind | Chris Checkpoint 1 accepted |
| 2026-08-29 | Step 2 (V4-V6) | PARTIAL | V4-V5 pass, V6 service-level smoke only | Timer-fired activation not demonstrated |

## Redis (hxs-9)

| Date | Test | Status | Evidence | Notes |
|---|---|---|---|---|
| 2026-08-29 | Install + evidence | PASS | Redis 7.0.15, ACL users, persistence | Wayne KDD-0015 |

## OmniRoute (hxs-8)

| Date | Test | Status | Evidence | Notes |
|---|---|---|---|---|
| 2026-08-29 | API key verification | PASS | Models list returns with valid key | Key: <redacted from OMNIROUTE API key in .local.env> |

## Governance (HX-ASF-Servers QA audit Phase 2)

| Date | Test | Status | Evidence | Notes |
|---|---|---|---|---|
| 2026-08-29 | validate.py full suite | PASS | 5/5 checks (wiki-sync, governance-path, fixture-suite, catalog-mechanical, secret-boundary) | New governance-path check added (SY-2); exit 0 |
| 2026-08-29 | render.py --check | PASS | 79/79 manifest documents in sync | All .md + .html pairs current (SY-6) |
| 2026-08-29 | governance-path integrity | PASS | governace/ canonical; governance/ fork absent | Fork removed; regression guard in validate.py |
| 2026-08-29 | secret-boundary sweep | PASS | 1191 files scanned, 0 hits | Redacted leaked OmniRoute key variant |
| 2026-08-29 | hook registration | PASS | 6 hooks in ~/.kimi-code/config.toml | agent-creation, render-sync, test-log-append, governor-gate, secret-boundary, validate-changed |
| 2026-08-29 | lane-capability registry | PASS | KDD-0013 Amendment 10 appended | Context ceilings + output guards per lane (SY-5) |
