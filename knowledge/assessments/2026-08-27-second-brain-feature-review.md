# Second Brain feature review — what's assessed, what's implemented, the count (2026-08-27)

| Field | Value |
| --- | --- |
| Date | 2026-08-27 (UTC) |
| Author | Kimi-K3 (governor), owner-question review |
| Question | "Were Second Brain features/capabilities assessed for this run? Outcome? How many have we actually implemented to date?" |
| Method | Every line carries a live, checkable pointer (file, record, or receipt). **Counting rule:** a feature counts as *implemented* only if it is live in production with evidence — ratified-but-not-built does not count. |
| Truth-state | FACT (live evidence) / AUTHORITY (ratified decisions) / INFERENCE (labeled) |

## 1. Were they assessed? — yes, continuously (FACT)

Assessment is not a one-time event here; it runs on three tracks:

1. **Formal assessments:** [`2026-08-25-capability-assessment-read-only.md`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/assessments/2026-08-25-capability-assessment-read-only.md) (O1–O10), [`2026-08-25-unified-capability-recommendations.md`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/assessments/2026-08-25-unified-capability-recommendations.md) (U1–U7 with UD decisions), [`2026-08-25-hx-second-brain-guidance-001-review.md`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/assessments/2026-08-25-hx-second-brain-guidance-001-review.md) (the roadmap document's review), [KDD-0005](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/decisions/KDD-0005-second-brain-canonical-home.md) (canonical split ratified: Second Brain lives in this repo; `/opt/tkv-local` is source corpus).
2. **The standing directive (mandatory 4-point evaluation):** every material handoff must state whether a Second Brain opportunity was identified, which capability applies, the disposition (implemented / recommended / deferred), and the evidence. It is present in **73 artifacts** across the repo (counted 2026-08-27).
3. **Per-decision gates:** every backend registration, agent adoption, and pipeline gate carries its own evaluation (KDD-0006 through KDD-0008, the goal contracts).

## 2. The outcome — 12 feature-classes IMPLEMENTED and live (FACT)

| # | Feature-class | Implemented evidence (click to open) |
| ---: | --- | --- |
| 1 | Canonical catalog (the Second Brain core) | [`knowledge/catalog/`](https://github.com/hanax-ai/HX-ASF-Servers/tree/main/knowledge/catalog) — **254 records**, receipts closing every handoff, relations, freshness labels ([KDD-0005](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/decisions/KDD-0005-second-brain-canonical-home.md); validator 4/4 PASS) |
| 2 | Standing directive (mandatory 4-point evaluation) | 73 artifacts carry `second_brain_evaluation`; baked into [`pilots/_templates/`](https://github.com/hanax-ai/HX-ASF-Servers/tree/main/pilots/_templates) |
| 3 | Catalog schema + agent profile foundations (U1) | [`knowledge/catalog/schema.yaml`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/catalog/schema.yaml), [`agents/carol/profile.md`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/agents/carol/profile.md) |
| 4 | Catalog validator (U2) | [`scripts/validate.py`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/scripts/validate.py) — 4 checks + `--ci` portable mode (runs locally and in CI gates) |
| 5 | Local validation hooks (U3/U5 pilots → live) | [`scripts/hooks/secret-boundary.sh`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/scripts/hooks/secret-boundary.sh), [`scripts/hooks/validate-changed.sh`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/scripts/hooks/validate-changed.sh) — shellcheck-clean, CI-gated |
| 6 | Verification checklist + triage tiers (U7) | tiered review in force (T0–T3 eligibility per handoff; state-log triage lines) |
| 7 | p7-lite agent-performance ledger | [`knowledge/agent-performance.md`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/agent-performance.md) — accuracy counts, tier eligibility, 8-item review log, boundary calibration |
| 8 | Carol run-tier system | T-micro/T-standard/T-full + carry-forward window + owner-ratified calibration (bundle budgets) |
| 9 | Dual-format wiki publishing (Q2) | [`scripts/wiki/render.py`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/scripts/wiki/render.py) + [`manifest`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/scripts/wiki/manifest.txt) — 42 documents rendered deterministically, `--check` drift gate in CI |
| 10 | Backend-capability records (capability registry) | [`DOC-backend-qwen-x`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/catalog/documents/DOC-backend-qwen-x.yaml), [`-coder-x`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/catalog/documents/DOC-backend-coder-x.yaml), [`-meta-x`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/catalog/documents/DOC-backend-meta-x.yaml), [`-chat-x`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/catalog/documents/DOC-backend-chat-x.yaml) — the [KDD-0006](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/decisions/KDD-0006-hxs2-coderx-backend-adoption.md) role ("the catalog fills the capability-registry role") |
| 11 | Adoption-gate pattern (new specialist path) | Trinity: candidate → reconciliation → charter/profile/KDD → owner ratification → catalog → roster ([KDD-0008](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/knowledge/decisions/KDD-0008-trinity-omniroute-adoption.md), validated as reusable) |
| 12 | Fleet standards-as-data | [`scripts/fleet/fleet-standard.yaml`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/scripts/fleet/fleet-standard.yaml) + [`fleet-verify-baseline.sh`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/scripts/fleet/fleet-verify-baseline.sh) — actual-vs-declared fleet verification (landed 2026-08-27; formally evaluated below) |

**The count: 12 feature-classes implemented** by the counting rule above. If the owner counts the CI/CD pipeline's review-and-gate machinery as a thirteenth Second Brain-class capability, that is defensible — it is recorded separately below, not folded into the 12.

## 3. Deferred or recommended — none silently dropped (AUTHORITY)

| Feature | State | Reason on record |
| --- | --- | --- |
| CI/CD pipeline (gates, CodeRabbit review, auto-merge) | **Live since 2026-08-26** — a Second Brain-class capability in practice; listed separately from the 12 | p8; its run-receipts-to-catalog idea stays deferred (next row) |
| CI run receipts → catalog evidence | deferred | p8 Second Brain evaluation: revisit after a month of run history ([`docs/cicd-pipeline.md`](https://github.com/hanax-ai/HX-ASF-Servers/blob/main/docs/cicd-pipeline.md) §Second Brain) |
| Executable custom agents (`.kimi-code/agents/`) | deferred | phase-transition KDD required (unified recommendations UD) |
| Ollama MCP server | deferred | ratified loopback-era posture; the OmniRoute program is the traffic-plane gate |
| Memory/Qdrant-side Second Brain features | deferred | OD-10 — OmniRoute Layer 3 territory |
| Unified doc's deferred-capability list | carried | untouched by this review |

## 4. Gap dispositions closed by this review

1. **Fleet library (landed 2026-08-27 without the formal 4-point evaluation):** evaluated now — opportunity identified: yes (standards-as-data verification is a Second Brain pattern); capability: catalog-adjacent verification evidence; disposition: **implemented** (row 47, hxs-2 log; baseline matrix: **hxs-1 through hxs-4 all-PASS on the llm-host rules; hxs-8 is 1 PASS plus one honest REPORT — NTP still `ntp.ubuntu.com`, unchanged, the owner's pending call**); reasoning: it converts repeated admin judgment into declared, checkable data — the same pattern class as `validate.py`.
2. **CI receipts deferral** existed only in the pipeline doc — now recorded at the review level (§3, row 2 of the deferred register).
3. **No single place answered "what's implemented"** — this artifact is now that place; see the cadence recommendation.

## 5. Cadence recommendation (for owner ratification or amendment)

At every milestone close and every feature-wave close: refresh this review's implemented count and deferred register in one pass (the pattern is the same one the catalog's living-document rule already uses). Cost: minutes per milestone; benefit: the owner never has to ask "how many" again — the answer is always one file deep.

## 6. Provenance

Built from: the three 2026-08-25 assessments, KDD-0005/0006/0008, 73 evaluated artifacts (grep count 2026-08-27), the week's state logs (hxs-1/hxs-2/hxs-3/OmniRoute pilots), and live catalog state (254 records, validator 4/4). No secrets; all pointers checkable.
