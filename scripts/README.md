# Scripts

Operations scripts for the HX fleet. Approved pattern only: native Bash/SSH from the
control workstation (`hxs-5`, 192.168.50.204 — replaced `hxs-cp` per owner
advisory 2026-08-27). Ansible is not part of this architecture.

## Fleet-control conventions

- SSH user: `hxsa`
- Explicit server/IP mapping; no magic discovery in scripts
- `scp` the script to `/tmp` on the target, then execute remotely
- Privilege via passwordless sudo on the target
- Three modes where applicable: `host` (one target), `fleet` (all targets),
  `verify` (check, change nothing)

## Rules

- Scripts must be idempotent or say clearly why not.
- No secrets in this directory.
- Every script header: purpose, target(s), mode usage, rollback note.

## Script index

### Fleet library (`scripts/fleet/`)

| Script | Purpose | Mode |
|---|---|---|
| `fleet-inventory.sh` | READ-ONLY fleet host inventory | fleet, host |
| `fleet-verify-baseline.sh` | READ-ONLY actual-vs-declared fleet verification | fleet, verify |
| `fleet-hostkey-pin.sh` | Verified SSH host-key pinning ceremony | fleet |
| `fleet-ntp-pin.sh` | Staged fail-closed NTP source pin | fleet |
| `fleet-sleepmasks.sh` | LLM-host 4-target sleep-mask set | host |
| `fleet-evidence-pull.sh` | Immediate off-host evidence pull | host |
| `fleet-selftest.sh` | Offline self-test for the fleet script library | offline |

### Hooks (`scripts/hooks/`)

Declared in `governace/hooks/manifest.yaml` and verified against the live
registrations by `scripts/hooks_verify.py` (`validate.py` sub-check SY-5).

| Script | Purpose | Trigger | Enforcement |
|---|---|---|---|
| `secret-boundary.sh` | Secret-value boundary scanner | PreToolUse | enforcing (mode file: `warn` today) |
| `validate-changed.sh` | Runs `validate.py` on changed files | PostToolUse | advisory |
| `agent-creation-check.sh` | Flags an incomplete agent registration | PostToolUse | advisory |
| `render-sync.sh` | Flags wiki HTML drift | PostToolUse | advisory |
| `test-log-append.sh` | Reminds to append a test-log row | PostToolUse | advisory |
| `governor-gate.sh` | Reminds to run the verification checklist | PostToolUse | advisory |
| `claude-payload-shim.sh` | Payload translator — a helper, not a registered hook | — | — |

### Catalog tooling (`scripts/catalog/`)

| Tool | Purpose |
|---|---|
| `carol-mint` | Flock-serialized single-writer catalog record minter |
| `carol-mint-SPEC.md` | Minting specification |
| `test-carol-mint.sh` | Catalog minting test |

### Wiki (`scripts/wiki/`)

| Tool | Purpose |
|---|---|
| `render.py` | Renders manifest-listed `.md` to `.html` (`--check` verifies sync) |
| `test_render.py` | Render test suite (12 tests) |
| `manifest.txt` | List of documents to render (63 docs) |

### Validator (`scripts/`)

| Tool | Purpose |
|---|---|
| `validate.py` | 5-check authoritative validator (wiki-sync, governance-path, fixture-suite, catalog-mechanical, secret-boundary). `governance-path` carries sub-checks SY-2 canonical spelling, SY-3 skill mirrors, SY-4 goal work-state, SY-5 hook manifest, SY-6 skill registry |

## Onboarding note

Hook registrations live in `~/.kimi-code/config.toml` (user-scoped, never
committed). A fresh machine or user does not inherit hooks automatically —
run `kimi config` to register `secret-boundary.sh` (PreToolUse) and
`validate-changed.sh` (PostToolUse). See `scripts/hooks/README.md` for
the registration convention.
