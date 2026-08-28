#!/bin/bash
# Gordon test wrapper (deployed to $GORDON_SCRATCH/bin/run-dsh, 0755).
# Runs as the service user via the privilege prefix. In with-key mode it
# sources the landed /var/lib/dsh/.env — readable by that user, never by
# Gordon's context — and appends only OMNIROUTE_API_KEY to the assignment
# list. no-key mode never sources. The value never enters the executor's
# environment, logs, or evidence.
# argv: <with-key|no-key> [K=V ...] -- <candidate argv...>
mode="$1"; shift
assign=()
while [ "$#" -gt 0 ] && [ "$1" != "--" ]; do
  assign+=("$1")
  shift
done
[ "${1:-}" = "--" ] && shift
if [ "$mode" = "with-key" ] && [ -r /var/lib/dsh/.env ]; then
  have=0
  for a in ${assign[@]+"${assign[@]}"}; do
    case "$a" in OMNIROUTE_API_KEY=*) have=1 ;; esac
  done
  if [ "$have" -eq 0 ]; then
    set -a
    . /var/lib/dsh/.env 2>/dev/null
    set +a
    if [ -n "${OMNIROUTE_API_KEY:-}" ]; then
      assign+=("OMNIROUTE_API_KEY=$OMNIROUTE_API_KEY")
    fi
  fi
fi
exec env -i ${assign[@]+"${assign[@]}"} "$@"
