# Scripts

Operations scripts for the HX fleet. Approved pattern only: native Bash/SSH from the
control plane (`hxs-cp`). Ansible is not part of this architecture.

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
