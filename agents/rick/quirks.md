# Rick — Quirks Register

**Standing input to every rick assignment.** Read at startup alongside
`agents/rick/profile.md`. This register is where discovered platform quirks
become permanent knowledge: each entry is a fact with an evidence pointer —
never a guess, never folklore. Rules:

- Every future F-class quirk discovered during a task gets an entry at that
  task's handoff (one line, evidence pointer mandatory).
- Entries are applied, not just recorded: if a rule here covers the current
  work, cite the entry in the deliverable instead of re-deriving it.
- Entries are never silently rewritten; corrections append a dated note.
- Format: **name | symptom | root cause | rule to apply | evidence pointer |
  date added.**

| # | Name | Symptom | Root cause | Rule to apply | Evidence pointer | Date added |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | timedatectl comma-`-p` quirk (systemd 255) | `timedatectl show -p NTP,NTPSynchronized,Timezone` prints nothing, exit 0 | systemd 255 does not split a comma-joined value in a single `-p` | Query single properties: `timedatectl show -p NTP -p NTPSynchronized -p Timezone`; never trust an empty `show` as a negative result | `servers/2026-08-26-fleet-time-and-mask-pass.md` §4 note + §7 F-2 | 2026-08-27 |
| 2 | ufw unit-state artifact | `systemctl is-active ufw` can read `active` while the firewall is OFF (hxs-1: active/enabled unit, `ENABLED=no`) | ufw.service is a boot oneshot; unit state is not the firewall switch | Rule firewall state on `/etc/ufw/ufw.conf` `ENABLED=` (library field `firewall.ufw_conf`); unit state is informational only | `scripts/fleet/README.md` Field notes; `scripts/fleet/fleet-standard.yaml` firewall rule | 2026-08-27 |
| 3 | Boot-cleared `/tmp` (hxs-3) | Evidence staged on hxs-3 `/tmp` does not survive reboots (mechanism UNCONFIRMED — investigate when next authorized) | Unestablished; recorded as fact-of-loss risk from the M5/M8 cycles | Pull evidence off-host immediately at capture (`fleet-evidence-pull.sh`); never treat remote `/tmp` as retention | hxs-3 state log row 23 (F-M5-1 fact), row 25 (M8 evidence streamed at capture) | 2026-08-27 |
| 4 | Sleep-mask proven set | Fleet drift risk in both directions (hxs-2 missing hybrid-sleep; hxs-2's extra sleep.target; hxs-4 once fully unmasked) | LLM-host blueprint set vs ad-hoc per-host work orders | Proven LLM-host set = `suspend`/`hibernate`/`hybrid-sleep`/`suspend-then-hibernate` masked ×4 (hxs-1/3/4 aligned); hxs-2's extra `sleep.target` mask = documented harmless superset; non-LLM hosts static by default. Manage via `fleet-sleepmasks.sh`, never ad-hoc | `servers/2026-08-26-fleet-time-and-mask-pass.md` §5 item 3 + Addendum; hxs-2 state log row 6; hxs-3 state log row 5 | 2026-08-27 |
| 5 | DMI capacity under-report | hxs-8 DMI type-16 "Maximum Capacity: 32 GB" while 48 GB is installed and 46 GiB is OS-visible | Firmware-reported field not updated for the actual configuration | Trust OS-level data (`free`, `/proc/meminfo`) and per-module dmidecode type-17 records over the DMI array capacity field; record the mismatch as observation, not defect | `pilots/PILOT-OMNIROUTE-LAYER0-001/04-rick-hxs8-readiness.md` §3 + F-5 | 2026-08-27 |
| 6 | NVRM teardown assertions | `pIOVAS`, `Sysmemdesc`, `iovaspaceDestruct` NVRM lines at GPU teardown/runner-start windows on hxs-3 (also hxs-1 class) | Driver teardown chatter on 580.173.02; small, non-growing, confined to load windows | Recorded chatter class: monitor-only, NOT a halt trigger (Xid remains the stop class); count and confine per sweep, escalate only on growth or Xid | `pilots/PILOT-HXS3-MUSE-GLIMMER-TOOLING-001/09-esme-m7-ladder-profiles.md` (line ~235); `15-esme-m8-signoff.md` (lines ~141, ~263) | 2026-08-27 |
| 7 | set-timezone vs running processes | After `timedatectl set-timezone`, a running daemon's log timestamps keep the OLD zone label (ollama on hxs-3 printed EST cosmetically after the UTC switch) | tzset applies at process start; running processes keep their cached TZ until restart | Expect cosmetic stale-zone labels from long-running processes post-switch; do not "fix" by restarting services outside the work order — record the label shift and its end | hxs-3 state log row 20 (explained); fleet-pass §5 item 1 (EST-class end 23:52:40Z) | 2026-08-27 |
