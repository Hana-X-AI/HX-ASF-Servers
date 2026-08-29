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
| `agent-creation-check.sh` | PostToolUse | `Write\|Edit` | advisory (exit 0 always) | On writes under `agents/`: warn if a new agent dir is missing charter/profile/roster/AGENTS.md taxonomy/system-mapping/KDD/catalog items (QA-audit AG-05, registered 2026-08-29) |
| `render-sync.sh` | PostToolUse | `Write\|Edit` | advisory (exit 0 always) | On `.md`/manifest writes: run `render.py --check`, surface MISSING/DRIFT with the repair command (QA-audit ST-4, registered 2026-08-29) |
| `test-log-append.sh` | PostToolUse | `Write\|Edit` | advisory (exit 0 always) | On test/evidence writes: remind to append a dated row to `governace/testing/test-log.md` (QA-audit ST-7, registered 2026-08-29) |
| `governor-gate.sh` | PostToolUse | `Write\|Edit` | advisory (exit 0 always) | On evidence/deliverable writes: remind the governor to run the mandatory verification-checklist before acceptance (QA-audit R-6, registered 2026-08-29) |

## Registration checklist (QA-audit SY-4, 2026-08-29)

Every new hook or skill deliverable is **not complete until registered and
verified**. Delivery process:

1. **Hook:** add the `[[hooks]]` block to `~/.kimi-code/config.toml`
   (event, matcher, command, timeout).
2. **Verify registration:** `grep -c '<hook-name>' ~/.kimi-code/config.toml` → ≥ 1.
3. **Skill (repo):** create `.kimi-code/skills/<name>/SKILL.md`.
4. **Skill (user scope):** copy to `~/.kimi-code/skills/<name>/SKILL.md`
   (`cp -a .kimi-code/skills/<name> ~/.kimi-code/skills/`).
5. **Verify skill loadable:** `ls ~/.kimi-code/skills/<name>/SKILL.md`.
6. **Reference it:** add to the agent template skills section
   (`governace/templates/agent/profile.md`) and this README table.
7. **Functional smoke:** test the hook with a stdin-payload pipe AND a direct
   path arg (both interfaces) — see each hook header.

A hook/skill that is built but not registered does not count as delivered
(AG-05/AG-06 failure class).

Rules for every hook here:

- repo-reviewed, stdlib/POSIX, no network, no host access, no sudo, no MCP;
- never reads protected credential files except the documented execution-time
  read in `secret-boundary.sh` (never printed/stored — see its header);
- fail-open philosophy: hook errors must never break work; they are interception
  layers, not sole barriers (official docs: hooks are fail-open by design);
- blocking (exit 2) only after a measured warn-mode pilot and owner graduation;
- the validation hook (U3, after `scripts/validate.py` lands) calls the single
  validator command — hooks never reimplement checks.
