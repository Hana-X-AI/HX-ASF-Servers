# TKV Enforcement Evidence

**Date:** 2026-08-29
**Purpose:** Verify that every agent profile has a specific `/opt/tkv-local` path in its standing directive with a **be-great** skill reference.

## Summary

All 13 agent profiles now have a standing directive with a specific `/opt/tkv-local` path and a **be-great** skill reference. Two profiles were fixed in this pass:

- **carol** — standing directive referenced only `knowledge/catalog/` without `/opt/tkv-local`; updated to include both.
- **kimi-k3** — section 5 mentioned `/opt/tkv-local` in passing but section 23 (Standing directives) had no TKV-specific directive; added Directive 6.

mia was already compliant (standing directive at line 116 names `/opt/tkv-local` with be-great).

## Evidence table

| Agent | TKV path | be-great ref | Standing directive |
|---|---|---|---|
| carol | `/opt/tkv-local` | YES | YES |
| chris | `/opt/tkv-local/postgres-mcp-mai`, `/opt/tkv-local/npostgres-master` | YES | YES |
| gordon | `/opt/tkv-local/deepseek-harness-master` | YES | YES |
| john | `/opt/tkv-local/ollama` | YES | YES |
| kimi-k3 | `/opt/tkv-local` | YES | YES |
| mia | `/opt/tkv-local` | YES | YES |
| morpheus | `/opt/tkv-local/deepseek-harness-master` | YES | YES |
| quinn | `/opt/tkv-local/qdrant-master`, `/opt/tkv-local/qdrant-client-master`, `/opt/tkv-local/mcp-server-qdrant-master` | YES | YES |
| raphael | `/opt/tkv-local/LightRAG-main/`, `/opt/tkv-local/lightragmcp-main/`, `/opt/tkv-local/daniel-lightrag-mcp-main/` | YES | YES |
| rick | `/opt/tkv-local/ubuntu` | YES | YES |
| rob | `/opt/tkv-local/deepseek-harness-master` | YES | YES |
| trinity | `/opt/tkv-local/OmniRoute-release-v3.8.51` | YES | YES |
| wayne | `/opt/tkv-local/redis-unstable`, `/opt/tkv-local/mcp-redis-main` | YES | YES |

## Verification method

Each profile was read in full. The standing directive section was checked for:
1. A specific `/opt/tkv-local` path (not generic or absent).
2. A **be-great** skill reference.
3. The standing directive label or equivalent structured directive section.

Profiles with domain-specific subdirectories (chris, gordon, john, morpheus, quinn, raphael, rick, rob, trinity, wayne) name their specific subdirectory paths. Profiles with general access (carol, kimi-k3, mia) name `/opt/tkv-local` as the root — appropriate for the knowledge steward, governor, and Chief of Staff roles.
