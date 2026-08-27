#!/usr/bin/env bash
# fleet-inventory.sh — READ-ONLY fleet host inventory (fleet library v0.1,
# owner directive 2026-08-27; hxs-2 state log row 44).
#
# Collects identity, OS, kernel, uptime/boot, CPU, RAM, DIMM topology (via
# passwordless-sudo dmidecode when readable; degrades cleanly to "unavailable"
# when not), disks, root usage, upgradable-package count, timezone, NTP
# state + current server, sleep-target states, failed units, and ollama
# presence — using only native Ubuntu commands over the caller's SSH.
#
# CREDENTIAL BOUNDARY: this script NEVER handles credentials. SSH transport is
# the caller's: set FLEET_SSH to a single executable (e.g. your askpass
# wrapper) or leave the default "ssh" (agent/keys/config are yours).
#
# MUTATION CLASS: none. Every remote command is read-only.
set -uo pipefail

SCRIPT_NAME="fleet-inventory.sh"

usage() {
  cat <<'EOF'
Usage: fleet-inventory.sh <host> [--json|--human|--kv]

Collects a READ-ONLY inventory of <host> over SSH and prints it.

Output modes (default --json):
  --json   JSON document to stdout (machine mode)
  --human  human-readable table
  --kv     flat "path<TAB>value" lines (consumed by fleet-verify-baseline.sh)

Environment:
  FLEET_SSH   SSH executable/wrapper used for transport (default: ssh).
              Must be a single command path; any credential mechanism belongs
              to that wrapper, never to this script.

Exit status: 0 on success; 1 on usage/transport failure.
EOF
}

mode="json"
host=""
while [ $# -gt 0 ]; do
  case "$1" in
    --json) mode="json" ;;
    --human) mode="human" ;;
    --kv) mode="kv" ;;
    -h|--help) usage; exit 0 ;;
    -*) printf '%s: unknown option %s\n' "$SCRIPT_NAME" "$1" >&2; usage >&2; exit 1 ;;
    *) if [ -z "$host" ]; then host="$1"; else printf '%s: unexpected extra argument %s\n' "$SCRIPT_NAME" "$1" >&2; exit 1; fi ;;
  esac
  shift
done
[ -z "$host" ] && { usage >&2; exit 1; }

FLEET_SSH="${FLEET_SSH:-ssh}"

# Remote probe: read-only native commands only. Emits key=value lines grouped
# under SECTION: markers; SECTION:lsblk carries raw lsblk lines.
REMOTE_PROBE="$(cat <<'EOS'
echo "SECTION:id"
printf 'hostname=%s\n' "$(hostname)"
printf 'machine_id=%s\n' "$(cat /etc/machine-id 2>/dev/null)"
printf 'boot_id=%s\n' "$(cat /proc/sys/kernel/random/boot_id 2>/dev/null)"
printf 'uptime_since=%s\n' "$(uptime -s 2>/dev/null)"
echo "SECTION:os"
sed -n 's/^PRETTY_NAME=//p' /etc/os-release | tr -d '"' | sed 's/^/pretty_name=/'
printf 'kernel=%s\n' "$(uname -r)"
printf 'arch=%s\n' "$(uname -m)"
echo "SECTION:cpu"
lscpu | sed -n 's/^Model name:[[:space:]]*/cpu_model=/p; s/^CPU(s):[[:space:]]*/cpus=/p; s/^Socket(s):[[:space:]]*/sockets=/p; s/^Core(s) per socket:[[:space:]]*/cores_per_socket=/p; s/^Thread(s) per core:[[:space:]]*/threads_per_core=/p'
echo "SECTION:mem"
awk '{k=tolower($1); sub(/:/,"",k); printf "%s_kb=%s\n", k, $2}' /proc/meminfo | grep -E '^(memtotal|memavailable|swaptotal)_kb='
echo "SECTION:df"
df -P / | awk 'NR==2 {gsub(/%/,"",$5); printf "root_size_kb=%s\nroot_used_kb=%s\nroot_avail_kb=%s\nroot_use_pct=%s\n", $2, $3, $4, $5}'
echo "SECTION:lsblk"
lsblk -n -o NAME,SIZE,FSTYPE,MOUNTPOINTS 2>/dev/null | grep -v '^loop' | grep -v ' loop'
echo "SECTION:time"
timedatectl show -p Timezone --value 2>/dev/null | sed 's/^/timezone=/'
timedatectl show -p NTP --value 2>/dev/null | sed 's/^/ntp_enabled=/'
timedatectl show -p NTPSynchronized --value 2>/dev/null | sed 's/^/ntp_synchronized=/'
srv=$(timedatectl timesync-status 2>/dev/null | sed -n 's/^ *Server: //p')
printf 'ntp_server=%s\n' "${srv:-unknown}"
echo "SECTION:targets"
for t in suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target sleep.target; do
  key=$(printf '%s' "$t" | sed 's/\.target$//; s/-/_/g')
  st=$(systemctl is-enabled "$t" 2>/dev/null)
  printf '%s=%s\n' "$key" "${st:-unknown}"
done
echo "SECTION:firewall"
ua=$(systemctl is-active ufw 2>/dev/null)
printf 'ufw_active=%s\n' "${ua:-unknown}"
ue=$(systemctl is-enabled ufw 2>/dev/null)
case "$ue" in enabled|disabled|masked|static|indirect) ;; *) ue=not-installed;; esac
printf 'ufw_enabled=%s\n' "$ue"
uc=$(sed -n 's/^ENABLED=//p' /etc/ufw/ufw.conf 2>/dev/null)
case "$uc" in yes|no) ;; *) uc=not-installed;; esac
printf 'ufw_conf=%s\n' "$uc"
echo "SECTION:security"
if command -v mokutil >/dev/null 2>&1; then
  sb=$(mokutil --sb-state 2>/dev/null | head -1)
  case "$sb" in
    *disabled*|*Disabled*) sb=disabled ;;
    *enabled*|*Enabled*) sb=enabled ;;
    *) sb=unknown ;;
  esac
elif [ -d /sys/firmware/efi ]; then sb=unknown
else sb=not-efi; fi
printf 'secure_boot=%s\n' "$sb"
echo "SECTION:units"
printf 'failed_units=%s\n' "$(systemctl list-units --failed --no-legend --no-pager 2>/dev/null | wc -l)"
if systemctl list-unit-files ollama.service --no-legend 2>/dev/null | grep -q ollama; then
  oa=$(systemctl is-active ollama 2>/dev/null)
  printf 'ollama_present=true\nollama_active=%s\n' "${oa:-unknown}"
else
  printf 'ollama_present=false\nollama_active=absent\n'
fi
echo "SECTION:updates"
printf 'upgradable_count=%s\n' "$(apt list --upgradable 2>/dev/null | grep -c upgradable)"
echo "SECTION:end"
EOS
)"

probe_out="$("$FLEET_SSH" "$host" "$REMOTE_PROBE" </dev/null 2>/dev/null)"
[ -z "$probe_out" ] && { printf '%s: no data from %s (transport or auth failure)\n' "$SCRIPT_NAME" "$host" >&2; exit 1; }
printf '%s\n' "$probe_out" | grep -q '^SECTION:end$' || { printf '%s: truncated probe from %s\n' "$SCRIPT_NAME" "$host" >&2; exit 1; }

# DIMM topology: passwordless-sudo read when available; degrade cleanly.
dimm_raw="$("$FLEET_SSH" "$host" 'sudo -n dmidecode -t memory 2>/dev/null' </dev/null 2>/dev/null)"
dimm_status="ok"
if [ -z "$dimm_raw" ] || ! printf '%s' "$dimm_raw" | grep -q '^Memory Device'; then
  dimm_status="unavailable"
  dimm_detail="dmidecode not readable without interactive sudo; scripts never handle credentials"
else
  dimm_detail="dmidecode -t memory via sudo -n"
fi

workdir="$(mktemp -d)" || exit 1
trap 'rm -rf "$workdir"' EXIT

# Flatten probe output: key=value pairs -> kv.tsv (path<TAB>value); raw lsblk lines -> lsblk.txt
printf '%s\n' "$probe_out" | awk -v kvf="$workdir/kv.tsv" -v lsf="$workdir/lsblk.txt" '
  /^SECTION:/ {
    section = substr($0, 9)
    next
  }
  section == "lsblk" { print $0 > lsf; next }
  /^[a-z_0-9]+=/ {
    eq = index($0, "=")
    key = substr($0, 1, eq - 1)
    val = substr($0, eq + 1)
    gsub(/-/, "_", key)
    printf "%s\t%s\n", key, val > kvf
  }
'
[ -f "$workdir/lsblk.txt" ] || : > "$workdir/lsblk.txt"

kv_get() {
  # kv_get <key> — value or empty string
  awk -F'\t' -v k="$1" '$1 == k {print $2; exit}' "$workdir/kv.tsv"
}

json_str() {
  # json_str <value> — JSON-escaped string content
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

json_num() {
  # json_num <value> — emit number or 0
  case "$1" in ''|*[!0-9]*) printf '0' ;; *) printf '%s' "$1" ;; esac
}

# Parse DIMM devices into TSV: locator, size, manufacturer, part, type, configured_speed
: > "$workdir/dimms.tsv"
dimm_count=0
if [ "$dimm_status" = "ok" ]; then
  printf '%s\n' "$dimm_raw" | awk '
    /^Memory Device/ {
      if (size != "" && size !~ /No Module/) {
        gsub(/^[ \t]+|[ \t]+$/, "", part)
        printf "%s\t%s\t%s\t%s\t%s\t%s\n", loc, size, man, part, type, cfg
      }
      loc=""; size=""; man=""; part=""; type=""; cfg=""
      indev=1
      next
    }
    indev && /^\tLocator:/        { loc=$2 }
    indev && /^\tSize:/           { sub(/^\tSize:[ \t]*/,""); size=$0 }
    indev && /^\tManufacturer:/   { sub(/^\tManufacturer:[ \t]*/,""); man=$0 }
    indev && /^\tPart Number:/    { sub(/^\tPart Number:[ \t]*/,""); part=$0 }
    indev && /^\tType:/           { sub(/^\tType:[ \t]*/,""); type=$0 }
    indev && /^\tConfigured Memory Speed:/ { sub(/^\tConfigured Memory Speed:[ \t]*/,""); cfg=$0 }
    END {
      if (indev && size != "" && size !~ /No Module/) {
        gsub(/^[ \t]+|[ \t]+$/, "", part)
        printf "%s\t%s\t%s\t%s\t%s\t%s\n", loc, size, man, part, type, cfg
      }
    }
  ' > "$workdir/dimms.tsv"
  dimm_count=$(wc -l < "$workdir/dimms.tsv" | tr -d ' ')
  [ "$dimm_count" = "0" ] && { dimm_status="unavailable"; dimm_detail="dmidecode readable but no populated Memory Device parsed"; }
fi

collected_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

emit_json() {
  local j_host j_hostname j_mid j_boot j_up j_os j_kernel j_arch j_cpu j_tz j_ntpsrv j_ue j_ua j_sb j_oa
  j_host="$(json_str "$host")"
  j_hostname="$(json_str "$(kv_get hostname)")"
  j_mid="$(json_str "$(kv_get machine_id)")"
  j_boot="$(json_str "$(kv_get boot_id)")"
  j_up="$(json_str "$(kv_get uptime_since)")"
  j_os="$(json_str "$(kv_get pretty_name)")"
  j_kernel="$(json_str "$(kv_get kernel)")"
  j_arch="$(json_str "$(kv_get arch)")"
  j_cpu="$(json_str "$(kv_get cpu_model)")"
  j_tz="$(json_str "$(kv_get timezone)")"
  j_ntpsrv="$(json_str "$(kv_get ntp_server)")"
  j_ua="$(json_str "$(kv_get ufw_active)")"
  j_ue="$(json_str "$(kv_get ufw_enabled)")"
  j_uc="$(json_str "$(kv_get ufw_conf)")"
  j_sb="$(json_str "$(kv_get secure_boot)")"
  j_oa="$(json_str "$(kv_get ollama_active)")"

  printf '{\n'
  printf '  "schema": "fleet-inventory/0.1",\n'
  printf '  "host": "%s",\n' "$j_host"
  printf '  "collected_at_utc": "%s",\n' "$collected_at"
  printf '  "identity": {"hostname": "%s", "machine_id": "%s", "boot_id": "%s"},\n' "$j_hostname" "$j_mid" "$j_boot"
  printf '  "os": {"pretty_name": "%s", "kernel": "%s", "arch": "%s"},\n' "$j_os" "$j_kernel" "$j_arch"
  printf '  "uptime_since": "%s",\n' "$j_up"
  printf '  "cpu": {"model": "%s", "cpus": %s, "sockets": %s, "cores_per_socket": %s, "threads_per_core": %s},\n' \
    "$j_cpu" "$(json_num "$(kv_get cpus)")" "$(json_num "$(kv_get sockets)")" "$(json_num "$(kv_get cores_per_socket)")" "$(json_num "$(kv_get threads_per_core)")"
  printf '  "memory": {"total_kb": %s, "available_kb": %s, "swap_total_kb": %s},\n' \
    "$(json_num "$(kv_get memtotal_kb)")" "$(json_num "$(kv_get memavailable_kb)")" "$(json_num "$(kv_get swaptotal_kb)")"
  printf '  "dimms": {"status": "%s", "detail": "%s", "devices": [' "$dimm_status" "$(json_str "$dimm_detail")"
  local first=1 line loc size man part type cfg
  while IFS=$'\t' read -r loc size man part type cfg; do
    [ -z "$loc" ] && continue
    [ $first -eq 0 ] && printf ', '
    first=0
    printf '{"locator": "%s", "size": "%s", "manufacturer": "%s", "part": "%s", "type": "%s", "configured_speed": "%s"}' \
      "$(json_str "$loc")" "$(json_str "$size")" "$(json_str "$man")" "$(json_str "$part")" "$(json_str "$type")" "$(json_str "$cfg")"
  done < "$workdir/dimms.tsv"
  printf ']},\n'
  printf '  "storage": {"root": {"size_kb": %s, "used_kb": %s, "avail_kb": %s, "use_pct": "%s%%"}, "devices": [' \
    "$(json_num "$(kv_get root_size_kb)")" "$(json_num "$(kv_get root_used_kb)")" "$(json_num "$(kv_get root_avail_kb)")" "$(json_str "$(kv_get root_use_pct)")"
  first=1
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    [ $first -eq 0 ] && printf ', '
    first=0
    printf '"%s"' "$(json_str "$line")"
  done < "$workdir/lsblk.txt"
  printf ']},\n'
  printf '  "updates": {"upgradable_count": %s},\n' "$(json_num "$(kv_get upgradable_count)")"
  printf '  "time": {"timezone": "%s", "ntp_enabled": "%s", "ntp_synchronized": "%s", "ntp_server": "%s"},\n' \
    "$j_tz" "$(json_str "$(kv_get ntp_enabled)")" "$(json_str "$(kv_get ntp_synchronized)")" "$j_ntpsrv"
  printf '  "sleep_targets": {"suspend": "%s", "hibernate": "%s", "hybrid_sleep": "%s", "suspend_then_hibernate": "%s", "sleep": "%s"},\n' \
    "$(json_str "$(kv_get suspend)")" "$(json_str "$(kv_get hibernate)")" "$(json_str "$(kv_get hybrid_sleep)")" "$(json_str "$(kv_get suspend_then_hibernate)")" "$(json_str "$(kv_get sleep)")"
  printf '  "firewall": {"ufw_active": "%s", "ufw_enabled": "%s", "ufw_conf": "%s"},\n' "$j_ua" "$j_ue" "$j_uc"
  printf '  "security": {"secure_boot": "%s"},\n' "$j_sb"
  printf '  "failed_units": %s,\n' "$(json_num "$(kv_get failed_units)")"
  printf '  "ollama": {"present": %s, "active": "%s"}\n' "$(kv_get ollama_present)" "$j_oa"
  printf '}\n'
}

emit_kv() {
  # Flat path<TAB>value projection (fleet-verify-baseline.sh consumes this).
  printf 'identity.hostname\t%s\n' "$(kv_get hostname)"
  printf 'identity.machine_id\t%s\n' "$(kv_get machine_id)"
  printf 'identity.boot_id\t%s\n' "$(kv_get boot_id)"
  printf 'os.pretty_name\t%s\n' "$(kv_get pretty_name)"
  printf 'os.kernel\t%s\n' "$(kv_get kernel)"
  printf 'os.arch\t%s\n' "$(kv_get arch)"
  printf 'uptime_since\t%s\n' "$(kv_get uptime_since)"
  printf 'cpu.model\t%s\n' "$(kv_get cpu_model)"
  printf 'cpu.cpus\t%s\n' "$(kv_get cpus)"
  printf 'cpu.sockets\t%s\n' "$(kv_get sockets)"
  printf 'cpu.cores_per_socket\t%s\n' "$(kv_get cores_per_socket)"
  printf 'cpu.threads_per_core\t%s\n' "$(kv_get threads_per_core)"
  printf 'memory.total_kb\t%s\n' "$(kv_get memtotal_kb)"
  printf 'memory.available_kb\t%s\n' "$(kv_get memavailable_kb)"
  printf 'memory.swap_total_kb\t%s\n' "$(kv_get swaptotal_kb)"
  printf 'dimms.status\t%s\n' "$dimm_status"
  printf 'dimms.count\t%s\n' "$dimm_count"
  printf 'storage.root.use_pct\t%s\n' "$(kv_get root_use_pct)"
  printf 'storage.root.avail_kb\t%s\n' "$(kv_get root_avail_kb)"
  printf 'updates.upgradable_count\t%s\n' "$(kv_get upgradable_count)"
  printf 'time.timezone\t%s\n' "$(kv_get timezone)"
  printf 'time.ntp_enabled\t%s\n' "$(kv_get ntp_enabled)"
  printf 'time.ntp_synchronized\t%s\n' "$(kv_get ntp_synchronized)"
  printf 'time.ntp_server\t%s\n' "$(kv_get ntp_server)"
  printf 'sleep_targets.suspend\t%s\n' "$(kv_get suspend)"
  printf 'sleep_targets.hibernate\t%s\n' "$(kv_get hibernate)"
  printf 'sleep_targets.hybrid_sleep\t%s\n' "$(kv_get hybrid_sleep)"
  printf 'sleep_targets.suspend_then_hibernate\t%s\n' "$(kv_get suspend_then_hibernate)"
  printf 'sleep_targets.sleep\t%s\n' "$(kv_get sleep)"
  printf 'firewall.ufw_active\t%s\n' "$(kv_get ufw_active)"
  printf 'firewall.ufw_enabled\t%s\n' "$(kv_get ufw_enabled)"
  printf 'firewall.ufw_conf\t%s\n' "$(kv_get ufw_conf)"
  printf 'security.secure_boot\t%s\n' "$(kv_get secure_boot)"
  printf 'failed_units\t%s\n' "$(kv_get failed_units)"
  printf 'ollama.present\t%s\n' "$(kv_get ollama_present)"
  printf 'ollama.active\t%s\n' "$(kv_get ollama_active)"
}

emit_human() {
  printf 'Fleet inventory: %s  (collected %s)\n' "$host" "$collected_at"
  printf '%-28s %s\n' 'hostname / machine-id' "$(kv_get hostname) / $(kv_get machine_id)"
  printf '%-28s %s\n' 'os / kernel' "$(kv_get pretty_name) / $(kv_get kernel) ($(kv_get arch))"
  printf '%-28s %s\n' 'up since / boot-id' "$(kv_get uptime_since) / $(kv_get boot_id)"
  printf '%-28s %s\n' 'cpu' "$(kv_get cpu_model) — $(kv_get cpus) cpus, $(kv_get sockets)s x $(kv_get cores_per_socket)c x $(kv_get threads_per_core)t"
  printf '%-28s %s\n' 'memory (kB)' "total $(kv_get memtotal_kb), available $(kv_get memavailable_kb), swap $(kv_get swaptotal_kb)"
  printf '%-28s %s\n' 'dimms' "$dimm_status ($dimm_count populated) — $dimm_detail"
  if [ "$dimm_count" != "0" ]; then
    while IFS=$'\t' read -r loc size man part type cfg; do
      [ -z "$loc" ] && continue
      printf '%-28s %s\n' '' "$loc: $size $man $part $type @ $cfg"
    done < "$workdir/dimms.tsv"
  fi
  printf '%-28s %s\n' 'root fs' "use $(kv_get root_use_pct)%, avail $(kv_get root_avail_kb) kB"
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    printf '%-28s %s\n' '' "$line"
  done < "$workdir/lsblk.txt"
  printf '%-28s %s\n' 'upgradable packages' "$(kv_get upgradable_count)"
  printf '%-28s %s\n' 'timezone' "$(kv_get timezone)"
  printf '%-28s %s\n' 'ntp' "enabled=$(kv_get ntp_enabled) synchronized=$(kv_get ntp_synchronized) server=$(kv_get ntp_server)"
  printf '%-28s %s\n' 'sleep targets' "suspend=$(kv_get suspend) hibernate=$(kv_get hibernate) hybrid-sleep=$(kv_get hybrid_sleep) suspend-then-hibernate=$(kv_get suspend_then_hibernate) sleep=$(kv_get sleep)"
  printf '%-28s %s\n' 'firewall (ufw)' "conf ENABLED=$(kv_get ufw_conf) (authoritative switch); unit active=$(kv_get ufw_active) enabled=$(kv_get ufw_enabled)"
  printf '%-28s %s\n' 'secure boot' "$(kv_get secure_boot)"
  printf '%-28s %s\n' 'failed units' "$(kv_get failed_units)"
  printf '%-28s %s\n' 'ollama' "present=$(kv_get ollama_present) active=$(kv_get ollama_active)"
}

case "$mode" in
  json) emit_json ;;
  kv) emit_kv ;;
  human) emit_human ;;
esac
exit 0
