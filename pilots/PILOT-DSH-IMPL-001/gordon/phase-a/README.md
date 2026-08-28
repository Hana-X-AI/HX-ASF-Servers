# Gordon Phase A — execution runbook (Gates 0–5)

Static artifacts authored 2026-08-28. Nothing here has executed. Execution
starts only after Morpheus's install lands on hxs-15 and the governor releases
this suite. The governing plan is
`pilots/PILOT-DSH-IMPL-001/02-gordon-phase-a-testplan.md`; dispositions land in
`pilots/PILOT-DSH-IMPL-001/gordon/coverage-ledger.md`.

## Prerequisites on hxs-15

1. Morpheus's handoff receipt: candidate binary path, install root, source
   tree path (if present), landed seam identity, OmniRoute model ids.
2. Python 3 with pytest (owner ruling 2026-08-28 permits test tooling;
   `GORDON_BOOTSTRAP_VENV=1` lets the runner create a venv under the scratch
   area and pip-install pytest).
3. The governor exports the OmniRoute client key under the name in
   `GORDON_OMNI_KEY_ENV` (default `OMNIROUTE_CLIENT_KEY`). The suite checks
   presence only; values are never read, logged, or written to evidence.
4. Executor identity: root, the `dsh` user, or an account with passwordless
   `sudo -u dsh`. Candidate invocations always run as `dsh`.

## Environment contract

See `gordon_util.py:ENV_DEFAULTS` for the full table. The inputs that decide
BLOCKED vs executable:

| Variable | When unset |
| --- | --- |
| `GORDON_DSH_BIN`, `GORDON_DSH_ROOT` | candidate rows BLOCKED (install pending) |
| `GORDON_DSH_SRC` | G1 static rows BLOCKED (no source on host) |
| `GORDON_OMNI_KEY_ENV` value | all routed rows BLOCKED (governor input) |
| `GORDON_MODEL_QWEN/CODER/META` | per-model routed rows BLOCKED (handoff input) |
| `GORDON_SEAM` | `auto` → fixtures use the in-tree pi-ai seam; set `deepseek` to use the llm-deepseek seam; `custom` needs Morpheus's contract |

## Governor-mediated usage evidence (G3-07/G3-08)

`usage_history` lives in OmniRoute's SQLite on hxs-8 (Trinity's plane). This
suite never reaches across. Protocol:

1. Before Gate 3 starts, the governor drops `before.json` into
   `$GORDON_SCRATCH/omni-usage/`.
2. After Gate 3 completes, the governor drops `after.json` at the same path.
3. Contract: `{"count": <total usage_history rows>, "rows": [ ... ]}` where
   `rows` optionally carries per-row `model`, `api_key_id`, `tokens_input`,
   `tokens_output`, `latency_ms`, `ttft_ms` (Trinity gate record, install
   §usage accounting). `rows` may be omitted; the count delta is the minimum
   assertion and per-model attribution strengthens it.
4. Without snapshots, G3-07 records BLOCKED-by-design with the dependency
   named. It is never skipped silently and never passed on dsh-side evidence
   alone.

## Execution

```sh
cd pilots/PILOT-DSH-IMPL-001/gordon/phase-a
./run-phase-a.sh            # all gates, in order
./run-phase-a.sh 0 2        # selected gates
```

Gate 0 runs first and freezes the candidate identity into
`$GORDON_SCRATCH/evidence/candidate-identity.json`. Per-test evidence records
land in `evidence-ledger.jsonl`; pytest dispositions land in
`pytest-outcomes.json`; JUnit XML per gate alongside. The runner prints
`[GATE VERDICT — <gate> — <verdict>]` lines.

## Stop conditions (profile §12.2)

Stop immediately, preserve the evidence area, and escalate to Kimi-K3 on:
credential material appearing in any artifact or log; any candidate write
outside the scratch area and the product's own session storage; candidate
identity drift against the G0-07 fingerprint; any pressure to convert a
BLOCKED/NOT_RUN into PASS.

## Retest rules

Defects route to Morpheus with the test ID, evidence record, and artifact
pointers. A fix retests the affected rows plus every row sharing the fixture
or seam; the ledger's `last-tested candidate identity` updates on every
retest. A moving candidate inside one campaign voids the campaign (G0-07).
