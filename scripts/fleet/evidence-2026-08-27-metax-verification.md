# Meta-X verification evidence — fleet script library v0.1

**Verdict: PASS for all nine artifacts. Zero nonconformances found.**

Verification stage per owner designation 2026-08-27 (hxs-2 state log rows 44-45).
Executor: Kimi harness on hxs-5 (192.168.50.204), deterministic checks first,
Meta-X bounded review second, harness adjudication last. No fixes applied; none
were needed.

## 1. Model contract record

| Field | Value |
| --- | --- |
| Call-sign | Meta-X |
| Host | hxs-3 (192.168.50.202) |
| Endpoint | http://192.168.50.202:11434 (Ollama 0.32.15) |
| Alias | `hx-muse-glimmer-64k` (only alias used) |
| Digest | `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da` (matches expected prefix `9dffb015db40…`) |
| Role | verification (structured conformance review; harness deterministic checks are the acceptance authority) |
| Date | 2026-08-27 |
| Call count | 9 inference calls (1 per artifact), 9× HTTP 200, zero re-requests |
| One-call-per-turn (KDD-0007) | COMPLIANT — each turn carried exactly one structured request; no parallel model calls; every response contained exactly one JSON verdict object (validated with `jq`); no response required rejection |
| Zero-cloud statement | All inference ran on the hxs-3 local Ollama endpoint over the private LAN. No cloud endpoint was contacted, no backend substitution occurred. |
| Identity check at task start | `/api/version` → 0.32.15; `/api/ps` → one resident model `hx-muse-glimmer-64k:latest`, digest match, size == size_vram == 18376336340 (fully VRAM-resident), context_length == 65536. Registry attributes ACTIVE / M8-signed are consistent with the observed digest match. Identity PASS — no escalation to Kimi-K3 required. |

## 2. Requirement list (from the commission contract)

- **R1 native-commands** — bash + native Ubuntu commands only; no new packages, no python/pip, no curl/wget, no pyyaml.
- **R2 credential-boundary** — never reads/stores/logs credentials or credential paths; SSH transport via `FLEET_SSH` env or default `ssh`; no secrets in argv.
- **R3 help** — `--help` prints a Usage block.
- **R4 safe-default** — mutators default to non-mutating: ntp-pin `--dry-run` default (`--apply` explicit); sleepmasks `verify` default (`apply` explicit); evidence-pull preserves remote unless `--prune`; read-only tools mutate nothing; hostkey-pin appends to the executor's known_hosts only after exact-match verification.
- **R5 hostkey-discipline** — never `accept-new`, never disables host-key checking; pin only on exact fingerprint match against a caller-supplied record.
- **R6 sanitized** — sanitized by construction: no eval, no sourcing remote data, quoted expansions.
- **R7 standards-file** — `fleet-standard.yaml` awk/sed-parseable (no pyyaml) and carries the llm-host rules (Etc/UTC; NTP contains time.cloudflare.com; 4-target masks; firewall off via `ufw_conf in no,not-installed`; secure_boot disabled) plus the host→class map.
- **R8 readme-accuracy** — README describes the library accurately (classes, defaults, credential boundary, work-order rule, evidence claims).

## 3. Deterministic pass (acceptance authority, run first)

- **D1 shellcheck 0.10.0** (official static binary, downloaded to `/tmp`, deleted after use): **7/7 scripts CLEAN**, zero findings, overall rc=0.
- **D2 `fleet-selftest.sh`**: **26/26 PASS**, rc=0 (syntax, `--help` behavior, fixture PASS/FAIL/REPORT/SKIP rule evaluation, fingerprint-record extraction).
- **D3 grep-based contract checks:**

| Check | Result |
| --- | --- |
| G1 `--help` handling present in each script | PASS (7/7; behavior proven by D2) |
| G2 credential-token scan | PASS — all hits are comments/usage text documenting the boundary; no credential read/store/log anywhere |
| G3 mutator defaults | PASS — `mode="dry-run"` (ntp-pin:52), `action="verify"` (sleepmasks:48), `prune=0` (evidence-pull:43) |
| G4 `accept-new` / `StrictHostKeyChecking=no` / `CheckHostIP=no` / `UserKnownHostsFile=/dev/null` | PASS — zero occurrences; only documentation of the NEVER rules |
| G5 host-key options in use | PASS — `BatchMode=yes`, `StrictHostKeyChecking=yes`, keyscan + exact fingerprint compare only |
| G6 dependency hygiene | PASS — no python/pip/curl/wget/apt-install; only read-only `apt list --upgradable` (native) |
| G7 `eval` / `source` of remote data | PASS — none |
| G8 standards file content | PASS — host→class map (hxs-1..4 llm-host, hxs-5 workstation, hxs-6..15 server-default) + 10 llm-host rules incl. Etc/UTC, `time.cloudflare.com`, 4 masks, `ufw_conf in no,not-installed`, `secure_boot eq disabled`; awk parser proven by D2 fixtures |

## 4. Per-artifact verdict matrix

Meta-X columns list its JSON verdicts (deterministic result is the acceptance
authority; Meta-X output is advice until deterministic checks agree).

| Artifact | Deterministic | Meta-X verdicts | Adjudication | Final |
| --- | --- | --- | --- | --- |
| fleet-inventory.sh | PASS (D1-D3) | R1-R4,R6 pass; R5,R7,R8 na | AGREEMENT | **PASS** |
| fleet-verify-baseline.sh | PASS (D1-D3; awk parser exercised by D2) | R1-R4,R6,R7 pass; R5,R8 na | AGREEMENT | **PASS** |
| fleet-ntp-pin.sh | PASS (D1-D3; dry-run default, fail-closed stage guard, `--apply` gated) | R1-R4,R6 pass; R5,R7,R8 na | AGREEMENT | **PASS** |
| fleet-sleepmasks.sh | PASS (D1-D3; verify default, apply gated) | R1-R4,R6 pass; R5,R7,R8 na | AGREEMENT | **PASS** |
| fleet-evidence-pull.sh | PASS (D1-D3; prune default-off, protected-path refusal, verified-pull gate) | R1-R4,R6 pass; R5,R7,R8 na | AGREEMENT | **PASS** |
| fleet-hostkey-pin.sh | PASS (D1-D3; strict-only options, exact-match gate before pin) | R1-R6 pass; R7,R8 na | AGREEMENT | **PASS** |
| fleet-selftest.sh | PASS (D1; executed: 26/26) | R1-R4,R6 pass; R5,R7,R8 na | AGREEMENT | **PASS** |
| fleet-standard.yaml | PASS (D2 fixtures + G8) | R7 pass; others na | AGREEMENT | **PASS** |
| README.md | PASS (claims re-verified against D1/D2/G-checks) | R1,R2,R3,R4,R5,R7,R8 pass; R6 na | AGREEMENT | **PASS** |

## 5. Adjudication record

- Meta-X raised **zero fail verdicts** across 9 artifacts × 8 requirements (72
  verdict cells). Every applicable cell agreed with the deterministic pass; the
  `na` cells match the per-artifact applicability of R5/R7/R8. No disagreement
  required resolution.
- Meta-X evidence lines were spot-checked against the artifacts (e.g.
  `mode="dry-run"`, `action="verify"`, `prune=0`, `StrictHostKeyChecking=yes`)
  and are accurate citations.

## 6. Findings and observations

- **Findings: none.** No real nonconformance exists; nothing was fixed or altered.
- **O1 (observation, not a nonconformance):** `fleet-evidence-pull.sh`
  interpolates the caller-supplied `<remote-dir>` into a single-quoted remote
  shell string (e.g. `test -d '$remote'`). A path containing a single quote
  would break the remote command. Adjudication: R6 as commissioned covers
  untrusted-input sanitization (no eval, no unquoted local expansion of remote
  output — both clean, shellcheck-clean); the path is caller-supplied within
  the caller's own trust domain and transport. Noted for a future revision,
  not a contract violation. Meta-X did not flag it; the harness flags it
  openly per the no-silent-findings rule.

## 7. Compliance notes

- Prompts to Meta-X contained only the requirement list plus the artifact
  text. No credentials, secrets, host records, or credential-file content
  entered model context.
- SSH to hxs-3 was not needed: identity and inference ran over the LAN HTTP
  API. The askpass helper was therefore never created; nothing to delete.
  Credential record `ssh-info.md` was never read.
- shellcheck 0.10.0 static binary was downloaded to `/tmp` (not present from
  the build) and deleted after use, per contract; no system change on hxs-5.
- Artifacts under review were not modified; this evidence file is the only
  addition to the directory.

---

## Addendum A — corrections after batch-17/18 hardening (2026-08-27, governor, labeled)

### A.1 Selftest version: 26/26 → 42/42 (review batch 18 finding)

The D2 result above ("26/26 PASS") is the **historical v0.1 result at Meta-X
verification time** and stands unchanged. After the batch-17 H1–H4 hardening
and the batch-18 selftest corrections, the accepted artifact is
`fleet-selftest.sh` **v0.1.2**: **42/42 PASS** (rick's proof, 2026-08-27) —
the original 26 checks plus 16 new: %q quoting contract (see A.2), the
prune-guard refusal matrix (7 cases, zero transport — now genuinely proven,
see F7 below), mock-transport pull/prune flows, and ntp-pin mktemp staging /
empty-diff mock replays. Shellcheck 0.10.0 CLEAN (7/7) throughout.

Batch-18 corrections inside the selftest itself: **F6** — an `eval`-based %q
round-trip assertion was removed (the selftest now contains zero eval in
command position, verified by grep) and replaced with a live-pinned literal
(`printf '%q'` generated once on this host's bash 5.2.21 — the value
`/tmp/a\ b\*\$x\`echo pwn\`\?\[\!z\]` — pinned as a constant with the
bash-version variance noted; SC2016 resolved by a byte-identical
double-quoted escaped constant). **F7** — the prune-guard refusal matrix now
sets `FLEET_SSH="$fx/mock-ssh"` so the empty-MOCK_LOG assertion genuinely
proves zero transport; rick's throwaway-reorder proof (guard moved after
`test -d` in a discarded copy) confirmed the test **fails as designed** on a
guard-ordering regression.

### A.2 O1 (remote-path quoting) — RESOLVED

The O1 observation above (single-quote interpolation of the caller-supplied
remote path, adjudicated not-a-violation at verification time) is **closed by
batch-17 H1** and no longer active: `fleet-evidence-pull.sh` now shell-quotes
`$remote` via `printf '%q'` at every interpolation site (test -d, find, tar,
rm -rf --, incl. the --prune path). Validation: the hostile path
`/tmp/rick's-test` was created on hxs-2, pulled successfully (verified=1),
then deleted via `--prune` — with the remote command carrying the escaped
form `/tmp/rick\'s-test`, never the break-out raw form (offline mock
assertion + live run); README §"Review batch 17 hardening" documents the
quoting rule for all future scripts; the %q contract is pinned in the
selftest (A.1/F6). The H2 prune-guard additionally normalizes trailing
slashes and protects the `/tmp` and `/opt` roots (bypass class closed);
`/tmp/<dir>` targets like the evidence directories remain prunable by
design, proven live.
