# Gordon — Phase A Verdicts (Gates 0–5)

- **Status:** CAMPAIGN EXECUTED 2026-08-28 on hxs-15 (192.168.50.214). Per-gate
  verdicts below in Gordon's completion language. Evidence pack:
  `gordon/evidence/` (40 files, 1.1 MB: `evidence-ledger.jsonl` 236 records,
  `routed-calls.jsonl` 128 routed calls, per-gate JUnit XML, artifacts).
- **Candidate identity (frozen per §8.3, 2026-08-28T10:39:17Z):** dsh
  0.1.1-rc.2; launcher `/usr/local/bin/dsh` sha256 `0b68259f…efcdba`; built bin
  `/opt/dsh/apps/cli/lib/bin.js` sha256 `c0226687…366c62`; home layer
  `/var/lib/dsh/cordis.patch.yml` sha256 `14f15b72…03f6016`; package.json
  `4adbdffa…4986d7`; pnpm-lock.yaml `6f20c268…90013e`; effective dump
  `dedda886…d518d34`; Node v24.20.0; pnpm 11.7.0; runtime `dsh` uid 999.
  All seven receipt identities re-verified live before the first test — MATCH
  (Morpheus receipt §10). Effective dump identical to the receipt: the
  candidate had not moved since install. G0-07 tree fingerprint on file for
  the end-of-campaign drift check.
- **Environment:** hxs-15 (4c/4t, 32 GB); OmniRoute 192.168.50.207:20128
  (health 200 throughout); suite run as hxsa with candidate invocations as
  `dsh` via `sudo -n -u dsh -- /usr/local/bin/gordon-run-dsh …` (env -i
  discipline; credential sourced by the service user from `/var/lib/dsh/.env`,
  value never in Gordon's context, logs, or artifacts — leak assertions in
  G3-13/G5-14 and a final evidence sweep all clean).

## Gate verdicts

### [GATE VERDICT — Gate 0 — PASS] (7/7)

Provenance and identity. Manifest hashes match the §3 baseline; runtime
versions match; `dsh --version` = 0.1.1-rc.2; service user confined (uid 999,
no sudo); identity frozen and fingerprinted. Evidence: gate0-junit.xml,
candidate-identity.json, tree-fingerprint.txt.

### [GATE VERDICT — Gate 1 — PASS WITH NAMED BLOCKS] (5 PASS direct, 4 rows closed by retest/analysis, 1 DEFERRED_BY_POLICY)

Static, build, repository quality (scratch copy, byte-verified, candidate tree
untouched). G1-01 frozen-lockfile install PASS; G1-02 typecheck PASS; G1-03
lint PASS; G1-04 build PASS on retest via the repo's documented non-Git
mechanism (`DSH_CLIENT_COMMIT_HASH` = the pinned baseline commit
`b150a551…d28e`; build records 200 client artifacts); G1-05 unit tier 14,586
PASS / 7 FAIL — all 7 in two git-metadata-dependent spec files
(`scripts/translation-pairing-merge.spec.ts` ×6, `scripts/project-doc-site.spec.ts`
×1), BLOCKED-by-environment under defect D2; G1-06 snapshot tier 124 PASS /
2 FAIL (`session-fixture-layout` git-dependent → D2; acp `agent-instructions`
symlink-flattened → D3) / 2 skip; G1-07 hygiene 12/13 sub-gates PASS, only
`vendor rescope` FAIL (hard `.git` dependency → D2); G1-08 built-bin smoke
PASS; G1-09 repo real-API e2e DEFERRED_BY_POLICY (DeepSeek-cloud keys barred
by the local-only doctrine; HX e2e ran through OmniRoute in Gate 3 instead).
Evidence: gate1-junit.xml, gate1.log, g1-diag*.log, g1-unit-*.log.

### [GATE VERDICT — Gate 2 — PASS] (14 PASS, 1 BLOCKED-by-design)

Runtime composition and entry paths. Launcher help/errors, headless default
composition (all 57 asserted bundle rows present), dump flag exclusivity,
profile auto-init, invalid/unknown profile handling, app help and task
validation, telemetry composition (DISABLED default + bounded-drain values),
DSH_HOME override isolation, system-prompt assembly into the model-visible
request header, `dsh plugin` usage errors, and the `--host 0.0.0.0` refusal
(also G5-12). G2-10 web boot: BLOCKED-by-design — the web frontend dist is
deliberately not built in Phase A (receipt §5); bind-level proof reassigned
to Phase B Gate 7. Evidence: gate2-junit.xml, dump artifacts.

### [GATE VERDICT — Gate 3 — PASS] (13 PASS, 1 BLOCKED governor-mediated)

Providers, models, Omni integration — the routed proof, all with unique-nonce
known-answer markers (semantic-cache discipline per Trinity's gate record):

- **G3-01** seam census: native `llm-pi-ai` route `omniroute` confirmed in the
  landed composition (openai-completions + compat switches + `apiKeyEnv:
  OMNIROUTE_API_KEY` reference).
- **G3-04R** real-seam run (landed profile unmodified, credential resolved
  natively from `/var/lib/dsh/.env`): marker `GORDON-G304R-…` returned, exit 0.
- **G3-04F / G3-05F / G3-06F** routed calls to **Qwen-X** (hx-qwen3.8-27b-64k),
  **Coder-X** (hx-qwen3.6-coderx-64k), **Meta-X** (hx-muse-glimmer-64k): each
  exit 0, marker in `assistant/message`, `turn/end` reason `completed`.
- **G3-02** missing credential fails loud (`MISSING_CREDENTIAL`, exit 1).
- **G3-03** provider down: bounded `TRANSPORT` failure (fixture retry policy).
- **G3-08** dsh-side usage: `assistant/message.usage` with non-zero
  input/output tokens (inputTokens 7501-class values recorded).
- **G3-09** `llm/retry` durable events written before the bounded final failure.
- **G3-10** token measurement derivable from the event stream (non-zero folds).
- **G3-11** composed catalog matches the three fleet ids exactly.
- **G3-12** no `api.deepseek.com` base URL in any composed config.
- **G3-13** cookbook contract (owner directive): `adding-an-llm-adapter.md`'s
  declared shapes all present in the landed route; secrets cordis-native (no
  key-shaped value in the composition); usage emitted BEFORE finish in the
  durable stream.
- **G3-07** OmniRoute `usage_history` evidence: **BLOCKED** — governor-mediated
  (snapshot request below).

Evidence: gate3-junit.xml, per-run session logs, seam-census.json,
routed-calls.jsonl (128 calls with per-call model/marker/timestamp).

### [GATE VERDICT — Gate 4 — PASS] (15 PASS, 2 BLOCKED)

Sessions, events, persistence, memory. Artifact layout matches the derived
`projectKey/encodeSegment` path; header contract (`type=session`, `version=0`,
id, createdAt, delegationDepth); turn lifecycle with contiguous seq from 0;
restart durability (run-1 artifact byte-identical after run 2); checkpoint +
kill-drill prefix parse (with G5-09); corrupt sibling resilience (valid zstd
frame, corrupt JSONL inside — boot and a fresh session proceed; the backend's
fail-loud rejection of extension/compression mismatch was also recorded as a
behavior note); session-query-sqlite default posture (`:memory:`, `openAt:
never`); session title records (incl. the extra title LLM call, counted);
telemetry posture (switch set = fast exit; FULL against a closed collector
exits bounded); `.anonymous-user-id` created by its telemetry consumer, stable,
UUID-shaped; settings-driven model selection across eras (Coder-X then Meta-X
in the same composition, each visible in its era's request/header config);
attachment-local and storage composition censuses; credentials `$DSH_HOME/.env`
fallback (run succeeds with the key only in the scratch .env); session-stats /
projection-cache web-only census; AGENTS.md instructions reach the
model-visible stream (`user/message` with `agent-instructions` source).
**G4-06(b)** corrupted-current-session resume: BLOCKED-by-design (no headless
resume entry in the pinned CLI; Phase B Gate 7). **G4-13** spill on oversized
output: BLOCKED on defect D1 (no working bash executor on hxs-15).

### [GATE VERDICT — Gate 5 — PASS WITH NAMED BLOCKS] (7 PASS + 1 cross-listed, 8 BLOCKED on D1, 1 BLOCKED-by-design)

Tools, permissions, containment. PASS: G5-06 danger-full-access semantics
(out-of-workspace write succeeds in scratch; approval `never` in that mode —
also proves bash executes cleanly when no confinement is requested); G5-08
SIGINT mid-run exits 130 with a parseable committed prefix; G5-09 SIGKILL
mid-run, cold boot unaffected, killed log parses as committed prefix (one
recorded model-cooperation flake, retried green); G5-11 malformed-YAML and
schema-violation patches both fail loud at load; G5-12 public-bind refusal
(via G2-11); G5-15 tool catalog census (25 model-visible tools, bash/read/
write core present, zero pwsh); G5-16 pwsh platform-gate expressions present
(Linux); G5-17 cookbook tool contract (every census tool satisfies the
`defineTool` minimal shape).

**BLOCKED on defect D1 (8 rows):** G5-01 bash execution, G5-02 workspace
write, G5-03 workspace-escape denial, G5-04 read-only denial, G5-05 approval
fail-closed, G5-07 bash timeout, G5-13 background jobs, G5-14 managed DSH_*
environment. All eight require a usable sandbox backend; all retest after
Morpheus's fix. The containment posture itself is PROVEN by the same evidence:
the candidate fails CLOSED (`SandboxUnavailableError`, refuses to run
unconfined), and escalation without an approval channel is refused
(approval-required error, no bypass). Two initially-green rows (G5-01, G5-03)
were re-examined and corrected to BLOCKED after false-pass analysis (marker
matched the command string in tool/call arguments, not the tool result) —
recorded openly.

## Defect register (for Morpheus, severities per §12.1)

| ID | Severity | Defect | Evidence | Retest |
| --- | --- | --- | --- | --- |
| D1 | **P2** | No usable sandbox backend on hxs-15: `bwrap` not installed (chain rung 1) and the `landlock-run` prebuilt static binary is absent from the source distribution (chain rung 2; `native/landlock-run/packages/linux-x64` ships manifests only, binaries are release-assembled). Model-facing bash tool fails closed (`SandboxUnavailableError`) under workspace-write/read-only; containment posture holds (no unconfined execution, escalation refused without an approval channel) but the bash execution family is unusable in the landed config. 9 test rows blocked. | G5-02/03/04/05 evidence; probe session log (seq 112/163/346 SandboxUnavailableError); host probe (no bwrap, no binary) | Provision `bubblewrap` (apt) or the landlock-run prebuilt binary, then retest G4-13, G5-01..05, G5-07, G5-13, G5-14 |
| D2 | **P3** | The approved `.git`-less export vs git-requiring repo gates: `vendor rescope:check` (no env fallback), 7 unit specs (`translation-pairing-merge` ×6, `project-doc-site` ×1), `session-fixture-layout` snapshot (`git ls-files`), and the aggregate `pnpm run build`'s commit-hash call (documented escape `DSH_CLIENT_COMMIT_HASH` — verified working, 14,586/14,593 unit tests otherwise green). | g1-diag.log, g1-unit-fails.log, gate1.log | Carry `.git` in the distribution or add gitless fallbacks in the affected scripts |
| D3 | **P3** | The export flattens symlinks into regular files containing the link path (7,903 regular files, 0 symlinks — receipt §1). The acp `agent-instructions` snapshot fixture expects real symlinks (`AGENTS.md → AGENTS.canonical.md`) and fails with a content/digest mismatch. | g1-diag2.log snapshot section; diff captured | Restore the two scenario symlinks post-transport (or teach the fixture a fallback) |

No P0/P1 defects. No candidate product defect was found in Gates 0, 2, 3, 4, 5
beyond the three environment/distribution items above. Behavior notes (not
defects): the persistence backend rejects a sibling artifact whose extension
mismatches the configured compression at contact (fail-loud per the
pre-release stance); Qwen-X hit OmniRoute queue-expiration waves (504,
15 s `maxWaitMs`) under parallel load — transients, retried per doctrine §9
with all attempts recorded; one model-cooperation flake (G5-09 first attempt)
recorded and retried green.

## BLOCKED rows (all named, none convertible without the named resolution)

- **G3-07** usage_history evidence — governor-mediated (request below).
- **G4-06(b)** corrupted-current-session resume — no headless resume entry;
  Phase B Gate 7.
- **G4-13** spill — defect D1.
- **G5-01..05, G5-07, G5-13, G5-14** — defect D1.
- **G2-10, G5-10** — web frontend dist deliberately absent (Phase B boundary).
- **G1-09** — repo cloud e2e, DEFERRED_BY_POLICY.

## Governor request: usage_history snapshots (G3-07/G3-08 closure)

Please fetch read-only from hxs-8 (OmniRoute SQLite `usage_history`):

1. A snapshot covering the campaign window **2026-08-28T10:50Z → 13:55Z**
   (first routed wave through last Gate-5 run), with rows carrying `model`,
   `api_key_id`, `tokens_input`, `tokens_output`, `latency_ms`, `ttft_ms`,
   `success`, and timestamp.
2. Drop as JSON into the evidence area (or return it here): expected
   assertion — row count attributed to the dsh client key with models
   `ollama-local/hx-qwen3.8-27b-64k:latest`, `…hx-qwen3.6-coderx-64k…`,
   `…hx-muse-glimmer-64k…` within the window is **≥ 128** (my
   `routed-calls.jsonl` register, title-generation calls included openly).
   Per-call correlation is available via the register's
   model/marker/timestamp tuples.

On receipt I rerun the G3-07 assertion (delta vs register) and close G3-08's
Omni-side reconciliation leg.

## Campaign close

[GATE VERDICT — Gate 0 — PASS] · [GATE VERDICT — Gate 1 — PASS WITH NAMED
BLOCKS] · [GATE VERDICT — Gate 2 — PASS] · [GATE VERDICT — Gate 3 — PASS]
· [GATE VERDICT — Gate 4 — PASS] · [GATE VERDICT — Gate 5 — PASS WITH NAMED
BLOCKS]

Phase A gate completion per my §7 completion rule is NOT yet declarable: D1
(P2) rejects the affected gate (Gate 5 execution rows) until Morpheus's fix
lands and the blocked rows retest green; G3-07 awaits the governor's
snapshots. No P0/P1 open. Stop conditions: none triggered. Campaign verdict:
**PHASE A GATES EXECUTED — 2 items outstanding (D1 retest, G3-07 snapshot
closure) — evidence pack attached; the Feature Coverage Ledger carries the
per-family dispositions.**
