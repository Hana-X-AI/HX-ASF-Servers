# hxs-6 — Configured State

**Phase:** Owner-authorized server implementation (scoped: additional-storage provisioning only)
**Configuration date:** 2026-08-28 (executed and recorded same day under `PILOT-HXS6-STORAGE-001`, WO-01)
**Assigned role:** Ingestion — crawling (copied from `SERVER-REGISTRY.md`, owner-ratified 2026-08-13, TARGET-STATE)
**Primary workload / model:** Crawl4AI (+ MCP) per registry — **NOT IMPLEMENTED by this record**; role implementation remains a later owner-authorized phase. This record covers the storage plane only.
**Approved by:** Agent-Zero (owner) — disposition 2026-08-27 #4; GO 2026-08-28T05:36Z (state-log row 2); discard ruling + governor gate 2026-08-28T06:07Z (state-log row 4)

## Discovery Reference

```text
servers/hxs-6/discovery.md
```

As-found record dated 2026-08-12; preserved unchanged. Known drift recorded openly:
discovery lists a single NVMe and no LVM; the second NVMe (added after
2026-02-26, before 2026-08-12 or between discovery and this provisioning) is the
subject of this record (baseline-wave F-1, 2026-08-27).

## Role Objective

- Registry TARGET-STATE: ingestion/crawling node (Crawl4AI + MCP). Deferred;
  nothing in this record installs or configures that workload.
- This record's scope: provision the additional 238.5 GB NVMe as bulk storage
  available for the owner's approved use (TBD by owner).

## Final Configuration

### Storage (the material change)

- OS disk (unchanged): `/dev/nvme0n1` KXG60ZNV256G TOSHIBA 256GB, serial
  `49FF70BNF0AN` — p1 vfat `/boot/efi`, p2 ext4 `/`; UUIDs, mounts, swap file
  byte-identical to discovery/baseline.
- Data disk (provisioned 2026-08-28): `/dev/nvme1n1` PC SN740 NVMe WD 256GB,
  serial `22170Z804761`, WWN `eui.e8238fa6bf530001001b448b4b6f22e2`:
  - new GPT (disk GUID `A5165993-E225-455F-B67F-C44FE20F77E0`), single
    partition p1 (238.5 GiB, type 8300, PARTUUID
    `7f5e765b-a27e-4fd2-9fdd-6614d6e4cdc4`);
  - ext4, LABEL `hxs-6-data`, UUID `c9241770-b75d-4a71-881c-b1fd1349f647`;
  - mounted `/srv/data` (0755, `hxsa:hxsa`), fstab by UUID with
    `defaults,nofail,noatime` (pre-change fstab backup on host:
    `/etc/fstab.hx-bak-20260828`);
  - prior content (foreign lived-in Ubuntu system, 397,773 entries) discarded
    by explicit owner ruling 2026-08-28 after phase-1 evidence
    (`servers/hxs-6/2026-08-28-storage-device-map.md` §4) — retain/archive
    foreclosed by the owner.
- LVM: none host-wide (stale `ubuntu-vg/ubuntu-lv` removed under the dual gate).

### Operating System / Network (unchanged by this record)

- Ubuntu 24.04.4 LTS (noble), kernel `7.0.0-30-generic`; hostname `hxs-6`;
  machine-id `0b899c5612f44c63ac468d2dd8dba5b5`
- IPv4 `192.168.50.205/24` on `eno1`; SSH :22; no host firewall (owner rule)
- Time: `Etc/UTC`, NTP pinned `time.cloudflare.com` (fleet baseline wave
  2026-08-27); sleep-target mask set ×4 applied same wave
- Secure Boot: ENABLED — recorded-only; remediation is an owner BIOS decision
  (baseline-wave F-5)

## Validation

```text
[x] Base system healthy        — 0 failed units before and after; no reboot (uptime since 2026-08-25 16:23:10 UTC)
[x] Identity discipline        — serial/WWN re-matched live immediately before LVM teardown (06:10:40Z PASS) and again before wipefs (06:13:35Z MATCH); destructive commands only on the identity-validated path
[x] Pre-change proofs          — proof 1 (root/boot-critical on nvme0n1 only) and proof 2 (exclusive LVM topology) PASS, governor-approved (state-log row 4)
[x] Destructive steps          — lvchange/lvremove/vgremove/pvremove/wipefs/sgdisk/mkfs: all OK, zero retries
[x] Final state                — /srv/data mounted rw,noatime from /dev/nvme1n1p1 (ext4 hxs-6-data); fstab by UUID; findmnt --verify 0 errors; probe file write/read/remove as unprivileged hxsa OK
```

## Material Change Record

| Timestamp (UTC) | Previous State | Change | Files / Commands | Validation | Rollback | Unresolved Issues |
| --------------- | -------------- | ------ | ---------------- | ---------- | -------- | ----------------- |
| 2026-08-28T06:11:34Z | Stale LVM `ubuntu-vg/ubuntu-lv` on second NVMe | LVM stack removed (dual-gate released, state-log row 4) | `lvchange -an`; `lvremove`; `vgremove`; `pvremove /dev/nvme1n1p3` | pvs/vgs/lvs empty host-wide | None — destructive, owner discard ruling | — |
| 2026-08-28T06:13:35Z | Old GPT + vfat/ext4/LVM signatures | Signatures wiped | `wipefs -a` (disk + 3 partitions) | Zero signatures on re-probe | None | — |
| 2026-08-28T06:14:05Z | Bare disk | New GPT, single 238.5 GiB partition, ext4 `hxs-6-data` | `sgdisk -o -n 1:0:0 -t 1:8300`; `mkfs.ext4 -L hxs-6-data` | blkid/lsblk confirm UUID `c9241770-…` | Repartition/reformat (dataless volume) | mkfs defaults kept (5% reserved blocks) — tuning is a later decision |
| 2026-08-28T06:14:53Z | No /srv/data | Mount + fstab persistence | fstab +1 line (backup `/etc/fstab.hx-bak-20260828`); `mount /srv/data`; chown/chmod | findmnt --verify 0 errors; probe OK | Remove fstab line, `umount /srv/data`, restore backup | — |

## Sources

- `servers/hxs-6/discovery.md` (as-found, 2026-08-12; preserved)
- `servers/hxs-6/2026-08-28-storage-device-map.md` (phase-1 verification + phase-2 execution evidence)
- `pilots/PILOT-HXS6-STORAGE-001/`: `00-goal.md`, `01-work-order-rick-storage.yaml` (WO-01), `02-state-log.md` (rows 1–4)
- `servers/2026-08-27-fleet-baseline-wave.md` (F-1 storage drift; F-5 Secure Boot)
- `servers/SERVER-REGISTRY.md` (assigned role; owner-maintained)
