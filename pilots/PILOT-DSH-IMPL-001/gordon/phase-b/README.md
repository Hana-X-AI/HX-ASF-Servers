# Gordon Phase B — execution runbook (Gates 6–7)

Authored offline 2026-08-28, pipelined with Morpheus's Phase B activation.
Executes only after the governor releases it. Governing plan:
`pilots/PILOT-DSH-IMPL-001/06-gordon-phase-b-testplan.md`. Dispositions land in
`pilots/PILOT-DSH-IMPL-001/gordon/coverage-ledger.md` (Phase B section).

## Release preconditions

1. Morpheus's Phase B handoff receipt: activated families, composition changes,
   the built frontend (`/opt/dsh/apps/web/dist`), any new home-layer rows.
2. A FRESH §8.3 freeze: the Phase B activation changes the tree and the
   composition; the Phase A fingerprint does not carry forward.
3. Phase A green state (routed seam, bwrap sandbox) still holds.
4. Python 3 + pytest on hxs-15 (installed during Phase A).
5. For G7-12 only: Chromium for Playwright (`GORDON_CHROMIUM` or
   `npx playwright install chromium` as test tooling).

## Environment contract

Phase A's contract applies unchanged (`GORDON_*` defaults in
`phase-a/gordon_util.py`). Phase B additions:

| Variable | Default | Meaning |
| --- | --- | --- |
| `GORDON_MCP_FIXTURE` | `/opt/dsh/packages/mcp/mcp-client/tests/fixture-server.ts` | stdio MCP fixture server |
| `GORDON_CHROMIUM` | unset | Playwright browser executable (G7-12) |
| `GORDON_SDK_DEMO` | `/opt/dsh/packages/examples/sdk-jsonrpc-demo` | SDK runtime composition |

## Execution

```sh
cd pilots/PILOT-DSH-IMPL-001/gordon/phase-b
export GORDON_SCRATCH=/home/hxsa/gordon/scratch \
       GORDON_EVIDENCE_DIR=/home/hxsa/gordon/evidence \
       GORDON_WRAPPER=/usr/local/bin/gordon-run-dsh \
       GORDON_QUEUE_SPACING_S=45 GORDON_QUEUE_ATTEMPTS=4
./run-phase-b.sh        # both gates in order
./run-phase-b.sh 6      # or 7
```

Gate 6 runs first (orchestration mechanics prove before the web surface).
Rows marked BLOCKED at authoring (G7-04/06/08/14/15/16/17/19) execute in the
release window once the API envelope and demo overlays are confirmed — they
are named dependencies, never guessed.

## Stop conditions

Profile §12.2 applies: credential material in any artifact (the de-patterning
writer is the first line, the manual sweep is the second), candidate writes
outside scratch/product storage, identity drift against the fresh freeze, or
pressure to convert BLOCKED/NOT_RUN into PASS. Stop, preserve, escalate.
