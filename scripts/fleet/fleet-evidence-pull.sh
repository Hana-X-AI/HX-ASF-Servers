#!/usr/bin/env bash
# fleet-evidence-pull.sh — immediate off-host evidence pull (fleet library
# v0.1; the boot-cleared-/tmp lesson: evidence on a remote /tmp does not
# survive a reboot — pull it off-host as soon as it exists).
#
# Pulls <remote-dir> from <host> into a timestamped local directory under
# <local-dir> using tar-over-SSH (no scp/sftp dependency), then writes a
# MANIFEST.sha256 of every pulled file plus MANIFEST.txt (source listing,
# counts, byte totals).
#
# Hardening (review batch 17, 2026-08-27):
#   H1 — the remote path is shell-quoted with bash-native `printf '%q'` and
#        the quoted form is embedded in every remote command string; a path
#        containing single quotes, spaces, globs, $ or backticks cannot break
#        out of its quoting.
#   H2 — the prune guard normalizes the path (trailing slashes stripped,
#        root preserved) BEFORE the protected-roots check, which now includes
#        /tmp and /opt (roots only — /tmp/<dir> and /opt/<dir> stay prunable).
#        The guard runs BEFORE any network activity, so a refusal provably
#        pulls and deletes nothing.
#
# MUTATION CLASS: READ-ONLY on the remote host by default — the remote source
# is NEVER deleted unless --prune is explicit. Local writes only under
# <local-dir>/<host>-<UTC timestamp>/.
#
# CREDENTIAL BOUNDARY: this script NEVER handles credentials. SSH transport is
# the caller's via FLEET_SSH (single executable path; default: ssh).
set -uo pipefail

SCRIPT_NAME="fleet-evidence-pull.sh"

usage() {
  cat <<'EOF'
Usage: fleet-evidence-pull.sh <host> <remote-dir> <local-dir> [--prune]

Pulls <remote-dir> from <host> into <local-dir>/<host>-<UTC timestamp>/
(tar-over-SSH), then writes:
  MANIFEST.sha256   sha256 of every pulled file (relative paths)
  MANIFEST.txt      remote source listing, file/byte counts, verification

Options:
  --prune   after a verified pull (local file count == remote file count),
            delete the remote source directory. OFF by default; the remote
            source is preserved unless this flag is explicit. Refuses to
            prune protected root paths (/, /etc, /opt, /tmp, ... — trailing
            slashes are normalized first, so "/tmp/" is refused too; the
            guard runs before any network activity).

Environment:
  FLEET_SSH   SSH executable/wrapper for transport (default: ssh).

Exit status: 0 on a verified pull (and prune when requested); 1 otherwise.
EOF
}

prune=0
positional=()
while [ $# -gt 0 ]; do
  case "$1" in
    --prune) prune=1 ;;
    -h|--help) usage; exit 0 ;;
    -*) printf '%s: unknown option %s\n' "$SCRIPT_NAME" "$1" >&2; usage >&2; exit 1 ;;
    *) positional+=("$1") ;;
  esac
  shift
done
[ ${#positional[@]} -eq 3 ] || { usage >&2; exit 1; }
host="${positional[0]}"
remote="${positional[1]}"
localbase="${positional[2]}"

FLEET_SSH="${FLEET_SSH:-ssh}"

# H2: normalize the remote path (strip trailing slashes, preserve root) and
# H1: produce the safely shell-quoted form used in every remote command string.
norm="$remote"
while [ "$norm" != "/" ] && [ "${norm%/}" != "$norm" ]; do norm="${norm%/}"; done
remote="$norm"
qremote="$(printf '%q' "$remote")"

# H2: prune guard FIRST — a refusal provably pulls nothing and deletes nothing.
if [ $prune -eq 1 ]; then
  case "$remote" in
    ""|/|/bin|/boot|/dev|/etc|/home|/lib|/lib64|/opt|/proc|/root|/run|/sbin|/srv|/sys|/tmp|/usr|/var)
      printf '%s: refusing to prune protected path "%s" (normalized; roots only — subdirectories stay prunable)\n' "$SCRIPT_NAME" "$remote" >&2
      exit 1 ;;
  esac
fi

# Remote preconditions: source exists and is a directory.
if ! "$FLEET_SSH" "$host" "test -d $qremote" </dev/null 2>/dev/null; then
  printf '%s: remote directory not found on %s: %s\n' "$SCRIPT_NAME" "$host" "$remote" >&2
  exit 1
fi

ts="$(date -u +%Y%m%dT%H%M%SZ)"
dest="$localbase/${host}-${ts}"
mkdir -p "$dest" || { printf '%s: cannot create %s\n' "$SCRIPT_NAME" "$dest" >&2; exit 1; }

# Capture the remote source listing (relative paths) for the manifest.
remote_listing="$("$FLEET_SSH" "$host" "cd $qremote && find . -type f | sort" </dev/null 2>/dev/null)"
remote_count="$(printf '%s\n' "$remote_listing" | grep -c . || true)"

# Pull: tar-over-SSH.
if ! "$FLEET_SSH" "$host" "cd $qremote && tar cf - ." </dev/null 2>"$dest/.pull-stderr" | tar xf - -C "$dest" 2>>"$dest/.pull-stderr"; then
  printf '%s: pull failed from %s:%s — %s\n' "$SCRIPT_NAME" "$host" "$remote" "$(cat "$dest/.pull-stderr")" >&2
  exit 1
fi
rm -f "$dest/.pull-stderr"

# Local manifest with sha256 of every pulled file.
( cd "$dest" && find . -type f ! -name 'MANIFEST*' -print0 | sort -z | xargs -0 -r sha256sum ) > "$dest/MANIFEST.sha256"
local_count="$(grep -c . "$dest/MANIFEST.sha256" || true)"
local_bytes="$(du -sb --exclude='MANIFEST*' "$dest" | awk '{print $1}')"

{
  printf 'fleet-evidence-pull manifest\n'
  printf 'host: %s\nremote source: %s\npulled at (UTC): %s\ndestination: %s\n' "$host" "$remote" "$ts" "$dest"
  printf 'remote files: %s\npulled files: %s\npulled bytes (excl. MANIFEST*): %s\n' "$remote_count" "$local_count" "$local_bytes"
  printf 'prune: %s\n\n' "$([ $prune -eq 1 ] && echo requested || echo no)"
  printf 'remote source listing (relative paths):\n'
  printf '%s\n' "$remote_listing"
} > "$dest/MANIFEST.txt"

verified=0
if [ "$remote_count" = "$local_count" ]; then
  verified=1
else
  printf '%s: WARNING — remote file count (%s) != pulled file count (%s)\n' "$SCRIPT_NAME" "$remote_count" "$local_count" >&2
fi

if [ $prune -eq 1 ]; then
  if [ $verified -eq 1 ]; then
    if "$FLEET_SSH" "$host" "rm -rf -- $qremote" </dev/null 2>/dev/null; then
      printf 'prune: remote source deleted: %s:%s\n' "$host" "$remote" >> "$dest/MANIFEST.txt"
      printf '%s: pruned remote source %s:%s (verified pull)\n' "$SCRIPT_NAME" "$host" "$remote"
    else
      printf '%s: prune failed on %s:%s\n' "$SCRIPT_NAME" "$host" "$remote" >&2
      exit 1
    fi
  else
    printf '%s: prune requested but pull is NOT verified — remote source preserved\n' "$SCRIPT_NAME" >&2
    exit 1
  fi
fi

printf '%s: pulled %s files (%s bytes) from %s:%s -> %s (verified=%s, pruned=%s)\n' \
  "$SCRIPT_NAME" "$local_count" "$local_bytes" "$host" "$remote" "$dest" "$verified" "$prune"
[ $verified -eq 1 ] && exit 0
exit 1
