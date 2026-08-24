# 08 — John Validation Summary

| Field | Value |
| --- | --- |
| Session ID | `john-initial-20260824-01` (correction session: `initial`) |
| Work order | `WO-OLLAMA-AUDIT-HXS5-001` (sha256 `d1883f295b36161c8b9950bb807ce3946d963a261a8b3168d2993b2d08ef672d`) |
| Context hash | `725553195e9c2df97c341fdc08b54c1fcd572c0ada69f9bb376e33f01d8278aa` |
| Target | `hxs-5` / 192.168.50.204 — verified local session, no SSH, 2026-08-24T09:30:19+00:00 |
| Live evidence period | 2026-08-24T09:30:19+00:00 → 2026-08-24T09:44:32+00:00 (UTC) |
| Completion state | `PASS — AUDIT EVIDENCE PACKAGE COMPLETE` |

## What was tested

29 tests defined before execution (`04-audit-test-plan.md`) covering the full plan-§10 matrix: ID-01..04, HW-01..05, GPU-01..04, SVC-01..05, API-01..03, MOD-01..03, SEC-01..04, PERF-01.

## Results

| Outcome | Count | Tests |
| --- | ---: | --- |
| PASS | 24 | ID-01..04; HW-01..04; GPU-01, GPU-03; SVC-01..05; API-01..03; MOD-01; SEC-01..04; PERF-01 |
| FAIL | 0 | — |
| BLOCKED | 0 | — |
| NOT RUN | 5 | HW-05 (benchmark class prohibited), GPU-02 + GPU-04 (inapplicable: no NVIDIA device, no Ollama unit), MOD-02 + MOD-03 (no model, no workload target, no server) |

Every NOT RUN has a recorded justification; none conceals a failure. No mandatory test failed; no stop condition (plan §16) triggered.

## Fact vs inference

- **Verified fact:** Ollama absent across seven identity sources (CLI, dpkg, snap, install paths, systemd, API, process table); no `:11434` listener; no model store, user, group, unit, journal entries, or `OLLAMA_*` configuration; host hardware matches the 2026-08-12 discovery baseline (i5-7500 4C/4T, 31.2 GiB RAM, Intel HD 630 only, single 238.5 GB NVMe).
- **Source statement (knowledge authority):** hxs-5 role is Edge/ingress — NGINX; no ratified Ollama baseline exists for hxs-5; corpus source snapshot identified as Ollama `v0.32.11` (commit `39df91c…`); hxs-1 pin `v0.32.14` and hxs-4 historical `0.32.9` are precedent only.
- **Inference (labeled in report):** §6 capacity note (`CAPACITY INFERENCE — VALIDATION REQUIRED`) — CPU-only host suits only small models at low concurrency.
- **Recommendation:** R1–R3 in `07-audit-report.md` §8; nothing executed.
- **NOT ESTABLISHED:** storage performance (HW-05), inference performance (F6/PERF-01), proxy/auth boundary (SEC-02, by absence), context alignment (MOD-02).

## Mutation status

**Zero.** All 23 logged shell invocations are read-only; the only writes are the authorized evidence-package files in `pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-001/`. No `systemctl` mutation verb, no `ollama` model verb, no kill, no installer, no benchmark, no network/firewall/service/model writes were executed. `sudo -n` was used exactly twice, both read-only (`ss -lntp`, `ss -lnup`).

## Artifact index and hashes (sha256)

| Artifact | sha256 |
| --- | --- |
| `03-john-knowledge-review-receipt.md` | `4603304f8a4f9f48a8470e5607e956282a32353a6a0731982c72baefc2580d9a` |
| `04-audit-test-plan.md` | `118e46137110f51f33d8b3b83a87725dcbad26d3c3827a3c0d91b8e3cf2b1b8e` |
| `05-command-log.md` | `df5c77d33191d94883aac88b5208546eee9716a1a36a5bf2f28e4a78026969d0` |
| `07-audit-report.md` | `81970a8280fdcb9a04930b08024b79b443a960b3ba09b912dc16d70b1b370cf1` |
| `06-raw-evidence-sanitized/api-01-probes.txt` | `7270d6ef53382db5e7e4481feefbdf390cae8355a0848b0e530de576dc7fd9b7` |
| `06-raw-evidence-sanitized/gpu-01-inventory.txt` | `26e8d4d015c1a40124d0609670ede2e631351fe4302194c5a2c99712e177c785` |
| `06-raw-evidence-sanitized/hw-01-cpu.txt` | `120bef4be68df73d1467d18dd955a2292314d5c826b9fc221b3e99044d7065f7` |
| `06-raw-evidence-sanitized/hw-04-storage.txt` | `a49daff921deadba0d343713fcd916ded393bc940360ab3ac823531706fc7d18` |
| `06-raw-evidence-sanitized/id-01-identity.txt` | `eae098e989acaa31a6c4cd99622f8363abd0a3a62c28dff78aaf2e27f3fc8301` |
| `06-raw-evidence-sanitized/id-04-ollama-identities.txt` | `e15987bd16fcb88accbfc17a37a70fe1be9c595299cd8e869fca81ca91b9bd36` |
| `06-raw-evidence-sanitized/kr-01-knowledge-survey.txt` | `0960ac8f91f55782ac913cace35a1c163385a069aa2adfdb42e0c086059e5535` |
| `06-raw-evidence-sanitized/sec-04-hygiene.txt` | `2e82e4c62674d0cd6482d91e0882a48f222bdfba78e2e72f4de7cc9f525154d3` |
| `06-raw-evidence-sanitized/svc-01-unit.txt` | `b01ddb7e12ff357c7f6bae48eeec83346fa2dce27c243db9f89ba372d777f4a0` |
| `06-raw-evidence-sanitized/svc-03-listener.txt` | `8cbfd4c6a74606a497b7fbc66fbc0933ebe2000507b05f0f1a340aff7e4c4174` |
| `06-raw-evidence-sanitized/svc-04-env.txt` | `f15aadbe0245ec75055503339cf7e19cd2786c770a791a754b2a287f4be592a3` |

This summary (08) is excluded from its own hash list; the governor freezes the complete `sha256sums.txt` at the evidence gate (plan §12). Hashes computed 2026-08-24T09:46+00:00; any post-hoc edit to a listed artifact invalidates its row.

## Risks

- R-1: Audit is a point-in-time snapshot (09:30–09:44 UTC); later installation of Ollama would invalidate F1 without a new audit.
- R-2: SVC-04 environment scan covered the `hxsa` account and system-level files only; another user's private profile was not read (no Ollama process or store exists for any user, limiting residual risk).
- R-3: GPU-03 journal window covers the current boot; older rotations were not searched (no NVIDIA hardware exists, limiting residual risk).
- R-4: None of the NOT RUN items can produce a hidden compliance failure today, because the component each would audit does not exist on this host.

## Exact decisions needed

- **D1 (Agent Zero):** Is Ollama intended ever to run on hxs-5? If yes, ratify an authority baseline (version pin, model, store path, loopback bind) before any installation work order. If no, accept this audit as standing conformance evidence.
- **D2 (Agent Zero / governor routing, adjacent observation):** Registry assigns hxs-5 the NGINX edge/ingress role, but nginx is not installed or running (F5). Route to the role owner if that role is now due.

`PASS — AUDIT EVIDENCE PACKAGE COMPLETE`
