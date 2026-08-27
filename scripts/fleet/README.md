# scripts/fleet — HX fleet script library v0.1

Owner directive 2026-08-27 ("it would be a great idea for rick to script much of
the repetitive work… a class library that can be called when needed… base
verification rick can execute now across the fleet"; hxs-2 state log row 44).
Codifies the proven patterns from `servers/2026-08-26-fleet-time-and-mask-pass.md`
(audit, staged fail-closed change, verify, final sweep) and
`pilots/PILOT-OMNIROUTE-LAYER0-001/04-rick-hxs8-readiness.md` (readiness inventory).

Bash + native Ubuntu commands only. No new packages anywhere. No Python, no
pyyaml — the standards file is parsed with awk.

## Files

| File | Class | Purpose |
| --- | --- | --- |
| `fleet-inventory.sh` | READ-ONLY | Per-host inventory → JSON (default), `--human` table, `--kv` flat projection |
| `fleet-verify-baseline.sh` | READ-ONLY | Actual-vs-declared matrix against `fleet-standard.yaml` (the owner's "base verification") |
| `fleet-ntp-pin.sh` | MUTATING with `--apply` | Staged fail-closed pin of `NTP=time.cloudflare.com`, `FallbackNTP=` empty; defaults to `--dry-run` |
| `fleet-sleepmasks.sh` | `verify` READ-ONLY (default); `apply` MUTATING | Proven 4-target sleep-mask set |
| `fleet-evidence-pull.sh` | READ-ONLY remote (default) | Timestamped tar-over-SSH evidence pull + sha256 manifest; `--prune` deletes the remote source only when explicit and verified |
| `fleet-hostkey-pin.sh` | Executor known_hosts only | Verified host-key pinning ceremony; NEVER accept-new, NEVER disables checking |
| `fleet-selftest.sh` | offline | 42-check self-test (syntax, `--help`, fixtures PASS/FAIL/REPORT/SKIP, fingerprint extraction, quoting contract, prune-guard matrix, mock-transport flow tests) |
| `fleet-standard.yaml` | data | Declared expected state: host→class map + per-class rules (`eq`/`ne`/`contains`/`in`, `enforce`/`report`) |

## Credential boundary (hard rule)

The scripts NEVER handle credentials — no password reads, no credential paths,
no secret storage, nothing in argv. SSH transport is the caller's:

```bash
export FLEET_SSH=/path/to/your-ssh-wrapper   # single executable; default: ssh
```

- With plain `ssh`, your agent/keys/`~/.ssh/config` govern.
- With a wrapper (e.g. an `SSH_ASKPASS` shim), the wrapper owns the secret.
- Name resolution is a transport concern: `known_hosts` entries and ssh config
  are per-address — pass the address your transport understands (the proof
  wrapper mapped fleet names to registry IPs; plain `ssh` callers can use
  `~/.ssh/config` Host entries).
- Mutators use remote `sudo -S` with stdin passthrough
  (`your-askpass | fleet-ntp-pin.sh <host> --apply`) or passwordless sudo.
  Read-only scripts attempt DIMM topology via `sudo -n dmidecode` and degrade
  cleanly to `unavailable` when interactive sudo would be required.

## Mutator work-order rule

`fleet-ntp-pin.sh --apply` and `fleet-sleepmasks.sh apply` run ONLY under an
explicit work order naming the target host. Both default to a non-mutating
mode (dry-run / verify) and print their exact rollback inverse in `--help`.
`fleet-evidence-pull.sh --prune` is the only destructive option in the
library: it refuses protected paths and requires a verified pull first.

## Usage sketches

```bash
scripts/fleet/fleet-inventory.sh hxs-1                 # JSON
scripts/fleet/fleet-inventory.sh hxs-8 --human         # table
scripts/fleet/fleet-verify-baseline.sh hxs-1 hxs-2 hxs-3 hxs-4 hxs-8
scripts/fleet/fleet-ntp-pin.sh hxs-8                   # dry-run (default)
scripts/fleet/fleet-sleepmasks.sh hxs-4 verify         # verify (default)
scripts/fleet/fleet-evidence-pull.sh hxs-2 /tmp/some-evidence ./pulled
scripts/fleet/fleet-hostkey-pin.sh 192.168.50.207 /opt/tkv-local/servers/hxs-8/pre-work-results.md
scripts/fleet/fleet-selftest.sh                        # offline, 42 checks
```

## Proving evidence (2026-08-27, live fleet)

- **(a) shellcheck 0.10.0 CLEAN** (zero findings incl. info) on all seven
  scripts; `fleet-selftest.sh` 42/42 PASS (extended to 42 for the batch-17
  hardening checks below). The repo CI gate
  (`shellcheck scripts/hooks/*.sh`) can be extended to `scripts/fleet/*.sh`
  unchanged. Tooling note: shellcheck is not installed on hxs-5 and no
  packages may be added — the proof used the official static binary in
  `/tmp` (executor-only, deleted after; no system change).
- **(b) inventory** JSON captured for hxs-1..4 + hxs-8 (plus `--human`
  sample): DIMM topology resolved where `sudo -n` is available (hxs-1's
  4×32 GB DDR5; hxs-8's 32+16 GB DDR4), `unavailable` cleanly elsewhere.
- **(c) verify-baseline matrix:** hxs-1..4 **10/10 PASS** (llm-host rules:
  Etc/UTC, NTP enabled+synchronized+time.cloudflare.com, 4 masks, ufw
  `ENABLED=no`, Secure Boot disabled); hxs-8 **1 PASS + 1 REPORT** (Etc/UTC;
  NTP honestly on `ntp.ubuntu.com` — owner call pending, NOT changed).
  `OVERALL: hosts=5, hosts-with-FAIL=0`.
- **(d) ntp-pin `--dry-run` on hxs-8:** staged diff produced
  (`#NTP=`→`NTP=time.cloudflare.com`, `#FallbackNTP=ntp.ubuntu.com`→
  `FallbackNTP=`), staged file removed, host verified untouched.
- **(e) sleepmasks verify:** hxs-1..4 ALIGNED (rc 0); hxs-8 DIVERGED (rc 1,
  all `static` — correct for a non-LLM host, report-only).
- **(f) evidence-pull:** 2-file fixture pulled from hxs-2 verified
  (count match, sha256 manifest), remote preserved without `--prune`,
  fixture cleaned after.
- **(g) hostkey-pin vs hxs-8 record:** `ALREADY-PINNED-VERIFIED` — exact
  fingerprint match against the owner pre-work record, known_hosts
  byte-identical (no re-pin). A first run against the fleet name correctly
  failed name resolution (documented: pin per-address).

## Review batch 17 hardening (2026-08-27)

Four verified-valid findings, fixed and proven (mutators proven in
dry-run/verify mode only; no `--apply` anywhere):

- **H1 — remote-path quoting rule (all current and future scripts):** any
  caller-supplied value embedded in a remote command string MUST be
  shell-quoted with bash-native `printf '%q'` first, and the quoted form used
  at every embedding site (never `'$var'` — a single quote in the value
  breaks out). Pinned offline by round-trip tests (quotes, spaces, globs,
  `$`, backticks, brackets) and live by pulling and pruning
  `/tmp/rick's-test` on hxs-2.
- **H2 — prune protected roots:** `fleet-evidence-pull.sh` normalizes the
  path (trailing slashes stripped, `/` preserved) and refuses to prune these
  exact roots: `` / /bin /boot /dev /etc /home /lib /lib64 /opt /proc /root
  /run /sbin /srv /sys /tmp /usr /var (empty included). Roots only —
  `/tmp/<dir>` and `/opt/<dir>` stay prunable by design. The guard runs
  BEFORE any network activity, so a refusal provably pulls and deletes
  nothing. Live refusal matrix: `/`, `/tmp`, `/tmp/`, `/etc/`, `/etc`, empty
  — all refuse rc 1; hxs-2's roots verified intact after.
- **H3 — mktemp staging contract (fleet-ntp-pin.sh):** the staged file is
  created by remote `mktemp /tmp/.fleet-ntp-pin.XXXXXXXX` (unprivileged,
  mode 600, transport-user-owned; /tmp chosen over /root so `--dry-run`
  staging needs no privilege). The stage emits `STAGED_PATH=<path>`; the
  script parses it, validates the shape (`/tmp/.fleet-ntp-pin.*`), and uses
  the parsed value for the diff, the apply install, and every cleanup. No
  fixed path anywhere. Proof: two dry-runs on hxs-2 produced different
  staged paths, both cleaned. Residual risk (documented in the script
  header): between diff-review and apply, only the transport user or root
  can touch the staged file.
- **H4 — already-compliant path (fleet-ntp-pin.sh):** an empty diff
  (`diff-rc=0`) means the host already matches the pin — the script reports
  `already-compliant`, cleans the staged file, and exits 0. The added-line
  check still guards NON-empty diffs, so genuinely missing NTP content
  still aborts. Live proof: hxs-1 (already pinned) reports
  already-compliant rc 0 with its config byte-identical after; hxs-8 (not
  pinned) still shows the real diff rc 0.

Self-test extended to 42 checks (mock transport replays the pull/prune and
ntp-pin stage flows offline). shellcheck 0.10.0 CLEAN on all seven scripts
after the edits.

## Field notes for future revisions

- `firewall.ufw_conf` (from `/etc/ufw/ufw.conf` `ENABLED=`) is the
  authoritative firewall switch; `ufw.service` unit state is informational
  only (hxs-1's unit is boot-enabled with the firewall OFF — no owner-rule
  conflict, cosmetic unit-state difference vs peers, report-only).
- `security.secure_boot` reads `mokutil --sb-state` when present (worked on
  all five proof hosts) and degrades to `unknown` → NOT-ESTABLISHED.
- `timedatectl show -p a,b,c` (comma-joined) prints nothing on systemd 255;
  the library only ever queries single properties.
- v0.1 limitations: `fleet-verify-baseline.sh` keys classes on fleet names
  (transport may need an address mapping, see credential boundary);
  evidence-pull verifies counts, not per-file content equality with the
  remote (sha256 manifest is of the pulled copies).
