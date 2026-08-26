# scripts/hooks — Kimi Code hook scripts (pilot, owner UD3/UD4 2026-08-25)

Hook **scripts** live here, repo-versioned and reviewed like any code. Hook
**registrations** live in the user-scope `~/.kimi-code/config.toml` (`[[hooks]]`
array) — that file is personal config, never committed; this README is the
placement convention (assessment Q-C, answered 2026-08-25).

## Registered hooks

| Script | Event | Matcher | Mode | Purpose |
| --- | --- | --- | --- | --- |
| `secret-boundary.sh` | PreToolUse | `Write\|Edit\|Bash` | `secret-boundary.mode` = `warn` (pilot week; then `block`) | Intercept secret-shaped content before it lands in a file or command. Three layers: generic credential patterns (REDACTED/withheld allowed); the literal credential read at execution; protected-source copy-verb references (`cat\|cp\|dd\|tee\|scp\|rsync\|tar` + `ssh-info.md`) — read-at-execution patterns (awk/sed/grep) allowed |
| `validate-changed.sh` | PostToolUse | `Write\|Edit` | advisory only (exit 0 always) | Run `scripts/validate.py --changed <edited file>` and surface failures with the reproduction command; the U3 pilot (UD3) |

Rules for every hook here:

- repo-reviewed, stdlib/POSIX, no network, no host access, no sudo, no MCP;
- never reads protected credential files except the documented execution-time
  read in `secret-boundary.sh` (never printed/stored — see its header);
- fail-open philosophy: hook errors must never break work; they are interception
  layers, not sole barriers (official docs: hooks are fail-open by design);
- blocking (exit 2) only after a measured warn-mode pilot and owner graduation;
- the validation hook (U3, after `scripts/validate.py` lands) calls the single
  validator command — hooks never reimplement checks.
