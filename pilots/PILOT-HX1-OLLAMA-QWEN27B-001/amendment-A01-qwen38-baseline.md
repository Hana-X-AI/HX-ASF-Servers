# Adoption header (HX-ASF-Servers)

| Field | Value |
|---|---|
| Adopted | 2026-08-25 by Agent Zero ("Amendment required and completed") |
| Source | `/home/hxsa/opt/local-tkv/agent-zero-docs/qwen/codex_20260824_2125_hx-1-ollama-pilot-qwen3.8-amendment.md` (verbatim below this header) |
| Drafted | 2026-08-24 21:25 — before KDD-0004 execution and milestones M1–M4 |
| Reconciliation | SATISFIED by KDD-0004 + M1–M4: §1 baseline adoption and MLX rejection; §2.1 unchanged controls; §3 tag/alias/preload supersessions; §4.1 identity freeze (digest, quantization, size, license, Ollama version, Modelfile hash, capabilities recorded in 12-esme-m4-install-evidence.md); §4.3 context ladder; §4.4 preload/monitoring alias identity. CONFLICT: §3/§4.2 sampling baseline — the M4-frozen alias carries the plan §6.5 sampling values (temperature 0.6, top_p 0.95, top_k 40, min_p 0, repeat_penalty 1.05, repeat_last_n 256, num_predict 8192), which A01 supersedes with a native-behavior Phase A. Disposition: milestone M5b rebuilds the alias to the A01 Phase A Modelfile verbatim, re-freezes identity, and re-runs the D8 quality suites; in-flight M5 results are retained as harness/recovery/security/benchmark evidence and as the sampled-profile Phase-B comparison point — history is labeled, not rewritten. OPEN → M5b: §5.1 reasoning-control capability probes (`reasoning_effort`, `preserve_thinking` — no assumed parity), thinking-baseline and multi-turn preservation tests, environment-feedback cases, §5.2 thinking-retention boundary, §5.3 vision boundary verification, §4.1.3 upstream template record. QUEUED to rick's next hxs-1 session: §7 "Rick confirms the unchanged host-readiness controls remain valid for the frozen Ollama build." |
| Plan impact | plan.md §6.5 Modelfile superseded by A01 §4.2 (marked in plan.md); A01 §6 risk deltas A01-R01–R08 adopted into the pilot risk picture; §7 acceptance conditions added to the pilot's definition of done |

---

# Amendment 01 — Qwen3.8-27B Model Baseline for the HX-1 Ollama Pilot

## Document control

| Field | Value |
|---|---|
| Amendment ID | `PILOT-HX1-OLLAMA-QWEN27B-001-A01` |
| Parent document | *HX-1 Ollama Qwen 27B Pilot Project*, version 1.0-draft, 2026-08-24 |
| Amendment version | 1.0-draft |
| Date | 2026-08-24 |
| Status | **DRAFT — PRE-EXECUTION / OWNER APPROVAL REQUIRED** |
| Human authority | Agent Zero |
| Control plane | KK3 Meta-Agent |
| Operational owners | John-Ollama (Esme); Rick-Ubuntu-Engineer-Admin |
| Change trigger | Official Qwen3.8 repository and Ollama `qwen3.8:27b` release |

> This amendment changes model-specific guidance only. It does not constitute host configuration, deployment evidence, or pilot sign-off. The parent document remains authoritative except where this amendment explicitly supersedes it.

## 1. Amendment decision

**Amendment required.** The parent pilot selected `qwen3.5:27b` as a proposed substitute because the requested model identifiers were not then validated. Official upstream sources now establish that:

- Qwen released **Qwen3.8-27B**, a dense 27B vision-language model intended for coding, professional work, research, and long-horizon agentic tasks;
- Ollama publishes the exact non-MLX tag **`qwen3.8:27b`** with vision, tools, and thinking capabilities;
- the Ollama artifact is approximately 18 GB, Q4_K_M, and currently identifies a 27.3B language model plus a BF16 vision projector;
- Qwen documents 262,144 native context and extension up to 1,000,000 tokens, but these are model capabilities—not proof that HX-1 can sustain those contexts under the pilot's dual-16-GB-GPU constraints.

Subject to Agent Zero approval and Gate 0 capability verification, the amended pilot candidate is:

```text
qwen3.8:27b (non-MLX Ollama artifact) — PROPOSED BASELINE
local alias: hx-qwen3.8-27b
```

The amendment does **not** approve `qwen3.8:27b-mlx` for HX-1. MLX is an Apple-Silicon-oriented runtime path; HX-1 is an Ubuntu/NVIDIA system. The non-MLX Ollama tag is the correct baseline.

## 2. Upstream evidence and scope

| Evidence | Finding | Pilot effect |
|---|---|---|
| QwenLM/Qwen3.8 official repository, `main`; README reviewed at blob `a7896ca771e13546c9eb62b67d6e65c3dba680bf` | Qwen3.8-27B was announced 2026-08-14 and targets coding, agent execution, tool/harness compatibility, thinking control, and multimodal work | Makes Qwen3.8-27B the relevant 27B pilot candidate |
| Official Qwen model card | 27B, 64 layers, native vision encoder, 262,144 native context; thinking is default; `reasoning_effort` and `preserve_thinking` are model/runtime features | Adds reasoning-mode and multimodal qualification requirements; does not authorize maximum context on HX-1 |
| Official Ollama library | `ollama run qwen3.8:27b`; 18 GB Q4_K_M artifact; capabilities: vision, tools, thinking | Confirms exact Ollama pull/run tag and local compatibility candidate |

### 2.1 What is unchanged

The following parent controls remain in force:

- KK3 delegates execution and verifies evidence; KK3 does not perform operational work.
- Rick completes the Ubuntu/Ollama TKV review and host-readiness gate before Esme deploys.
- Ollama determines model placement automatically; `OLLAMA_NUM_GPU` and `OLLAMA_GPU_LAYERS` must not be invented.
- `CUDA_VISIBLE_DEVICES` controls GPU eligibility, not an equal split guarantee.
- The model must be preloaded by a boot-ordered unit and retained with `keep_alive=-1`.
- API exposure, systemd hardening, rollback, monitoring, and evidence requirements remain unchanged.
- The context qualification ladder remains 32K first, then 64K. Larger contexts require a separate capacity decision.

## 3. Supersession matrix

| Parent location | Original guidance | Amended guidance | Reason |
|---|---|---|---|
| Executive decision | `qwen3.5:27b` proposed baseline | `qwen3.8:27b` proposed baseline | Exact official 27B Ollama tag now exists |
| Technical specifications | Proposed model `qwen3.5:27b` | Proposed model `qwen3.8:27b`, non-MLX | Align with current upstream release |
| Modelfile | `FROM qwen3.5:27b` | `FROM qwen3.8:27b` | Correct base artifact |
| Local alias | `hx-qwen3.5-27b` | `hx-qwen3.8-27b` | Prevent ambiguity in service and monitoring |
| Preload payload | model `hx-qwen3.5-27b` | model `hx-qwen3.8-27b` | Preload exact amended alias |
| Sampling baseline | Prior fixed sampling proposal | Use upstream thinking defaults for Phase A; tune only through controlled A/B trials | Qwen3.8 publishes distinct thinking and non-thinking profiles |
| Agent qualification | Generic tool-call tests | Add thinking-control, preserved-thinking, tool-schema, environment-feedback, and loop tests | New model features affect harness behavior |
| Multimodal scope | Not part of baseline | Capability acknowledged; remains out of baseline unless separately approved | Avoid silent memory and security scope expansion |

All other parent requirements survive unchanged.

## 4. Amended implementation instructions

### 4.1 Gate 0 — freeze identity before deployment

**Owner: Esme. Reviewer: KK3. Dependency: Rick Gate 2 host readiness.**

1. Confirm the approved Ollama release supports the model on HX-1.
2. Pull only the exact non-MLX tag.
3. Capture `ollama show` output, local manifest/digest evidence, artifact size, capabilities, parameters, template, license, Ollama version, and timestamp.
4. Hash the approved Modelfile and store the evidence in the pilot index.
5. Block deployment if the tag resolves to a materially different architecture, quantization, license, or capability set than reviewed.

```bash
ollama --version
ollama pull qwen3.8:27b
ollama show qwen3.8:27b
ollama show --modelfile qwen3.8:27b
ollama list
```

Expected upstream characteristics—**verify locally; do not treat as runtime evidence**:

```text
tag:          qwen3.8:27b
artifact:     approximately 18 GB
quantization: Q4_K_M
capabilities: vision, tools, thinking
```

### 4.2 Two-phase Modelfile strategy

The first model alias must preserve the upstream artifact's generation behavior while applying only the context and system contract necessary for the pilot. Do not copy Qwen3.5 sampling values into Qwen3.8 without comparative evidence.

**Phase A — native-behavior baseline**

```Dockerfile
FROM qwen3.8:27b

PARAMETER num_ctx 32768

SYSTEM """
You are the HX-1 local engineering model. Follow the supplied task contract.
Use retrieved evidence when provided, distinguish evidence from inference,
emit tool calls only through the declared schema, and never claim that a tool
ran unless a tool result is present. Stop and report a blocked condition when
required authority or evidence is missing.
"""
```

```bash
ollama create hx-qwen3.8-27b -f ./Modelfile
ollama show hx-qwen3.8-27b
```

**Phase B — controlled sampling qualification**

Qwen recommends different profiles by mode:

| Mode | Upstream starting profile | Pilot rule |
|---|---|---|
| Thinking | temperature 1.0; top_p 0.95; top_k 20; min_p 0; presence penalty 0; repetition penalty 1 | Test against native Ollama defaults; adopt only if tool validity, groundedness, coding, and retry metrics improve |
| Non-thinking | temperature 0.7; top_p 0.80; top_k 20; min_p 0; presence penalty 1.5; repetition penalty 1 | Treat as a separate alias/profile; never silently change the reasoning baseline |

Framework parameter names and support vary. Esme must first prove which settings Ollama accepts and how they map. Unsupported fields must not be placed in a Modelfile or client request.

### 4.3 Context policy

The model's advertised context is not HX-1's approved operating context. KV cache, multimodal projector state, parallel requests, GPU topology, and Ollama implementation determine practical capacity.

| Stage | Context | Decision rule |
|---|---|---:|
| Baseline | 32,768 | Mandatory first run; must pass residency, RAG, tool, coding, reboot, and soak gates |
| Target | 65,536 | Promote only after no OOM, no unapproved CPU fallback, acceptable accuracy, and stable dual-GPU evidence |
| Extended experiment | 131,072 | Separate owner-approved experiment; not pilot acceptance |
| Upstream maximum | 262,144 native | Capability reference only; not a deployment target for HX-1 |
| Extended model claim | up to 1,000,000 | Out of scope; runtime-specific and unsuitable as an HX-1 acceptance assumption |

> Correction 2026-08-25 (review finding; provenance preserved): the "Extended
> experiment" row above (131,072 as a separate owner-approved experiment, not pilot
> acceptance) is **superseded** by the owner's three-profile disposition
> (`23-kk3-m6-capacity-decision.md` Revision 2): 131,072 is a **qualified
> extended-context profile — explicitly selected**, inside pilot acceptance; 65,536 is
> the operating default; 32,768 the recovery baseline. The original row text is
> retained unchanged as the as-adopted record.

Keep `OLLAMA_CONTEXT_LENGTH=32768` through the baseline. A change to 65,536 requires a versioned configuration change and rerun of all capacity-dependent tests.

### 4.4 Amended preload and monitoring identity

Every systemd preload request, `/api/ps` assertion, readiness probe, dashboard filter, and alert must use the exact alias `hx-qwen3.8-27b`.

```bash
curl -fsS --retry 12 --retry-all-errors --retry-delay 5 \
  --connect-timeout 3 --max-time 900 \
  http://127.0.0.1:11434/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"model":"hx-qwen3.8-27b","prompt":"","stream":false,"keep_alive":-1}'

curl -fsS http://127.0.0.1:11434/api/ps
```

The preload script must fail if the exact alias is absent, if the server returns an error, or if readiness exceeds the approved budget. Model residence is still proven by `/api/ps` plus GPU/RAM telemetry—not by a successful health endpoint alone.

> Correction 2026-08-25 (review finding; provenance preserved): this §4.4 bare-alias
> directive (`hx-qwen3.8-27b` in preload requests, `/api/ps` assertions, readiness
> probes, dashboards, alerts, and the commands above) is **superseded** by the owner's
> three-profile disposition (`23-kk3-m6-capacity-decision.md` Revision 2). The ratified
> operating identity is `hx-qwen3.8-27b-64k`; profile aliases `-32k`/`-64k`/`-128k`
> exist (M6b), and the bare alias is retired (tags only, deterministic inverse). The
> commands above are **historical, non-executable**; the live preload contract asserts
> the exact 64K alias and digest (`29-esme-m6b-profiles.md`). Original text retained
> unchanged as the as-adopted record.

## 5. Agentic, reasoning, and tool qualification addendum

Qwen3.8's upstream claims are promising but are not acceptance evidence for the HX factory. Esme owns execution; KK3 owns the test contract and evidence decision.

### 5.1 Mandatory test matrix

| Test | Required evidence | Pass condition |
|---|---|---|
| Thinking baseline | Raw API request/response metadata, latency, token counts, model identity | Thinking behavior is known, repeatable, and does not corrupt final-answer parsing |
| Reasoning control | A/B cases for each Ollama-supported reasoning control | Requested setting is honored or explicitly documented as unsupported; no inferred compatibility |
| Multi-turn preservation | Fixed task split across multiple turns, fresh-session control, retry counts | No context leakage; preserved reasoning improves or does not degrade task completion |
| Valid tool call | JSON Schema tool definition and captured call | Correct tool name and valid arguments; no fabricated execution result |
| Invalid/unauthorized tool | Denied tool and adversarial prompt | Model does not bypass authorization; controller rejects invalid call deterministically |
| Environment feedback | Tool returns error, partial result, and changed state | Model replans within retry budget and stops at convergence/escalation threshold |
| RAG groundedness | Frozen retrieval set, citations, answer score | Meets parent thresholds and identifies insufficient evidence |
| Coding | Frozen repository tasks, tests, static analysis, patch review | Deterministic evidence passes; no natural-language-only success claim |
| 24-hour residency | `/api/ps`, GPU/RAM samples, journal, restart/OOM counters | No unexplained unload, restart loop, or silent CPU fallback |

### 5.2 Harness boundary

The controller—not the model—owns tool authorization, schema validation, retry count, timeouts, state transitions, and stop conditions. Qwen3.8's stronger agent execution does not justify relaxing KK3's hierarchical finite-state machine, evidence gates, or deterministic failure replay.

Never store or expose hidden reasoning as a required audit artifact. Retain task inputs, tool calls, tool results, state transitions, output, deterministic telemetry, and evaluation decisions. If the runtime exposes thinking content, apply the project's data-handling and retention policy before logging it.

### 5.3 Vision is a controlled extension

Vision support is acknowledged but **disabled as a pilot acceptance requirement**. Enabling it requires:

1. an approved image/video ingestion threat model;
2. memory and latency requalification with the vision projector active;
3. content-size, MIME, origin, and decompression limits;
4. prompt-injection and document-instruction tests;
5. a separate acceptance decision.

## 6. Risk-register deltas

| Risk ID | Area | Risk description | Level | Mitigation | Owner |
|---|---|---|---|---|---|
| A01-R01 | Release maturity | Qwen3.8/Ollama support is newly released and may change quickly | High | Freeze Ollama version, tag, digest, Modelfile hash, and test evidence; retest on any change | Esme → KK3 |
| A01-R02 | Runtime feature mapping | `reasoning_effort` or `preserve_thinking` may not map identically through Ollama | High | Capability-probe the actual API; treat unsupported behavior explicitly; never infer parity | Esme |
| A01-R03 | Context overcommit | Upstream 262K/1M claims could be misread as safe HX-1 settings | Critical | Enforce 32K→64K capacity ladder and owner gate for anything larger | KK3 / Rick / Esme |
| A01-R04 | MLX mismatch | Selecting `-mlx` on Ubuntu/NVIDIA introduces an inappropriate runtime path | High | Pin non-MLX `qwen3.8:27b`; reject alias drift at Gate 0 | Esme |
| A01-R05 | Sampling regression | Copying older model parameters may reduce Qwen3.8 reasoning/tool quality | Medium | Native-default baseline, frozen A/B corpus, evidence-based promotion | Esme / KK3 |
| A01-R06 | Thinking leakage | Reasoning content may enter logs, RAG stores, or user outputs | High | Log only governed artifacts; redact/disable thinking retention where policy requires | KK3 / Esme |
| A01-R07 | Vision scope expansion | Multimodal input increases memory, attack surface, and test burden | High | Keep out of baseline; require separate threat model and capacity gate | KK3 / Rick |
| A01-R08 | Benchmark transfer | Vendor benchmark scores may not predict HX factory outcomes | Medium | Use factory-specific frozen tasks, deterministic graders, and failure replay | KK3 |

## 7. Amended acceptance conditions

In addition to every surviving parent criterion, Amendment 01 passes only when:

- [ ] Agent Zero approves `qwen3.8:27b` as the pilot candidate.
- [ ] Rick confirms the unchanged host-readiness controls remain valid for the frozen Ollama build.
- [ ] Esme records the resolved model digest, quantization, size, capabilities, template, parameters, license, and Ollama version.
- [ ] All service, preload, monitoring, and test references use `hx-qwen3.8-27b`.
- [ ] Native/default sampling is baselined before any override is accepted.
- [ ] Ollama's actual reasoning and thinking controls are capability-tested; unsupported upstream features are recorded without workaround-by-assumption.
- [ ] Tool-schema, unauthorized-tool, environment-feedback, RAG, coding, reboot, and 24-hour residency tests pass.
- [ ] 32K passes before 64K is attempted; no 262K or 1M setting is treated as accepted.
- [ ] Vision remains disabled or completes its separate security and capacity gate.
- [ ] KK3 reconciles Amendment 01 into the final unified pilot record and Agent Zero signs off.

## 8. Implementation disposition

| Item | Disposition |
|---|---|
| Adopt Qwen3.8-27B as candidate | **YES — owner approval and Gate 0 required** |
| Use Ollama `qwen3.8:27b` | **YES — pin resolved digest** |
| Use `qwen3.8:27b-mlx` on HX-1 | **NO** |
| Preserve parent OS/service/security plan | **YES** |
| Increase baseline context to 262K | **NO** |
| Qualify 64K after 32K | **YES** |
| Assume upstream reasoning controls work through Ollama | **NO — test actual API** |
| Add vision to baseline | **NO — separate controlled extension** |

## 9. References

1. [QwenLM/Qwen3.8 — official repository](https://github.com/QwenLM/Qwen3.8)
2. [Qwen/Qwen3.8-27B — official model card](https://huggingface.co/Qwen/Qwen3.8-27B)
3. [Ollama library — qwen3.8:27b](https://ollama.com/library/qwen3.8:27b)

---

**Amendment rule:** If the resolved Ollama artifact, runtime capability report, or upstream safety/compatibility guidance changes after approval, reopen Gate 0 and issue a new amendment. Do not edit the evidence history in place.
