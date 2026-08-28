# hxs-6 — Storage Device Map (WO-01 phase-1 read-only verification)

| Field | Value |
| --- | --- |
| Task | WO-01-hxs6-storage, `phase_1_verification_read_only` (pilots/PILOT-HXS6-STORAGE-001) |
| Agent | Rick (Ubuntu Server Engineer), session rick-hxs6-storage-20260828-01 |
| Authority | Owner GO 2026-08-28T05:36Z ("hxs-6 disk wipe: have Rick do it now."), state-log row 2; phase 1 ONLY — phase 2 (destructive) remains LOCKED pending the governor gate |
| Target | hxs-6 = 192.168.50.205, user hxsa |
| Window | 2026-08-28T05:39–05:52Z (all times UTC; host clock Etc/UTC) |
| Executor host | hxs-5 (192.168.50.204) |
| Mutations on target | **NONE.** Read-only probes only. No lvchange/lvremove/vgremove/pvremove/wipefs/mkfs/parted/dd/mount/umount, no writes to the target disk |
| Credential handling | SSH via `SSH_ASKPASS` temp helper (mode 0700) extracting the governed credential at execution time only; value never printed/logged/stored; helper deleted at session end. Remote privilege via `sudo -n` (passwordless sudo confirmed live) |
| Host key | Pre-pinned ED25519 `SHA256:22p3IEFqoUBkJGGffuqFq/l4wGcOmwe7TBDJG3Pzkrw` — exact match to owner pre-work record (`/opt/tkv-local/servers/hxs-6/pre-work-results.md`); `StrictHostKeyChecking=yes` |

## Knowledge review receipt

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Source: /opt/tkv-local/ubuntu (exists; corpus ubuntu.com-main, refs-ubuntu-24.04, ubuntu_mcp_server-master)
Target Host/Scope: hxs-6 (192.168.50.205) — storage plane, read-only device-map verification
Reviewed At: 2026-08-28T05:39Z
Relevant Files: 3 dirs surveyed; no storage/LVM-specific ref docs in refs-ubuntu-24.04 (it covers netplan/timesyncd/ufw/systemd); task-relevant knowledge is the WO itself + servers/hxs-6/discovery.md + 2026-08-27 baseline-wave F-1
Ubuntu Release/Kernel Identified: Ubuntu 24.04.4 LTS (noble), kernel 7.0.0-30-generic (live)
Applicable Authority/Runbooks/Tests: WO-01 phase_1_verification_read_only; owner disposition 2026-08-27 #4
Configuration Owners Identified: rick (OS plane); governor Kimi-K3 (gate); owner (GO)
Contradictions or Gaps: discovery.md (2026-08-12) records a single NVMe + no LVM; live state has two NVMe + LVM (already recorded as baseline-wave F-1, 2026-08-27). This doc carries the current truth.
Task May Proceed: YES (phase 1, read-only)
```

## 1. Identity verification (MATCH)

| Fact | Live (2026-08-28T05:40Z) | discovery.md (2026-08-12) | Verdict |
| --- | --- | --- | --- |
| hostname | `hxs-6` | `hxs-6` | MATCH |
| SSH peer | connected to `192.168.50.205:22` | `192.168.50.205` | MATCH |
| machine-id | `0b899c5612f44c63ac468d2dd8dba5b5` | `0b899c5612f44c63ac468d2dd8dba5b5` | MATCH |
| OS / kernel | Ubuntu 24.04.4 LTS noble, `7.0.0-30-generic` | 24.04.4 LTS, `7.0.0-28-generic` at discovery; `7.0.0-30-generic` at 2026-08-27 baseline | CONSISTENT (kernel updated between discovery and baseline) |

## 2. Device map (live, verbatim)

`lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL,UUID,MOUNTPOINT,SERIAL,WWN`:

```text
NAME                        SIZE TYPE FSTYPE      LABEL UUID                                   MOUNTPOINT SERIAL       WWN
nvme0n1                   238.5G disk                                                                     49FF70BNF0AN eui.00000000000000018ce38e0500024c0d
├─nvme0n1p1                   1G part vfat              5E69-CD01                              /boot/efi               eui.00000000000000018ce38e0500024c0d
└─nvme0n1p2               237.4G part ext4              9408b77f-6a73-40ec-a26c-73f2709e689e   /                       eui.00000000000000018ce38e0500024c0d
nvme1n1                   238.5G disk                                                                     22170Z804761 eui.e8238fa6bf530001001b448b4b6f22e2
├─nvme1n1p1                   1G part vfat              2696-E825                                                      eui.e8238fa6bf530001001b448b4b6f22e2
├─nvme1n1p2                   2G part ext4              9de11806-959d-4ac7-8a66-33e29d0a2467                           eui.e8238fa6bf530001001b448b4b6f22e2
└─nvme1n1p3               235.4G part LVM2_member       rrc7yi-VWet-0zoq-Tu9L-INbS-y7fe-WQgrbe                         eui.e8238fa6bf530001001b448b4b6f22e2
  └─ubuntu--vg-ubuntu--lv   100G lvm  ext4              a8d18ab5-9cd3-4cb4-83db-5e569131aeae
```

Only two block devices exist on the host (no sd\*, no dm other than the LV, no loop mounts of real filesystems). GPT disk identifiers: nvme0n1 `276ED823-949B-4493-BC24-B208C1C7D2FC`, nvme1n1 `20376289-7D97-4D6D-98D3-E8E8E48FEFCF`.

### 2.1 Stable identity — TARGET DISK (anchor for all future phases)

> **Model:** `PC SN740 NVMe WD 256GB`
> **Serial:** `22170Z804761`
> **WWN (NGUID/EUI):** `eui.e8238fa6bf530001001b448b4b6f22e2`
> **Current path alias:** `/dev/nvme1n1` (kernel name — NOT stable across re-enumeration)
> **Stable udev aliases:** `/dev/disk/by-id/nvme-PC_SN740_NVMe_WD_256GB_22170Z804761` and `/dev/disk/by-id/nvme-eui.e8238fa6bf530001001b448b4b6f22e2` → both currently point to `../../nvme1n1`

Source: kernel sysfs `/sys/block/nvme1n1/device/{model,serial,wwid}` verbatim, corroborated identically by `lsblk -o SERIAL,WWN` and the udev by-id symlinks. All three sources agree.

**DEVIATION (flagged for governor):** `nvme-cli` is ABSENT on hxs-6 (consistent with discovery's "absent diagnostic tooling" note). The WO-specified `nvme list` / `nvme id-ctrl` could not be run, and installing the package would be a mutation outside phase-1 scope. The sysfs `device/serial` and `wwid` values are the kernel's rendering of the same NVMe Identify Controller data `nvme id-ctrl` would print; they are recorded verbatim above as the stable identity. Phase-2 identity revalidation can use the same sysfs path (or nvme-cli if the governor authorizes installing it beforehand).

For reference, OS disk (DO NOT TOUCH): model `KXG60ZNV256G NVMe TOSHIBA 256GB`, serial `49FF70BNF0AN`, WWN `eui.00000000000000018ce38e0500024c0d`, currently `/dev/nvme0n1` — matches discovery.md exactly.

## 3. COMPLETE target-disk topology (every signature accounted for)

Target disk `nvme1n1` (stable identity per §2.1) carries a complete Ubuntu Server LVM installation — the standard installer layout — nothing on the disk is outside the following inventory:

| # | Object | Identity | Size | Contents (read-only scan) | Mounted |
| --- | --- | --- | --- | --- | --- |
| 0 | Disk | GPT `20376289-7D97-4D6D-98D3-E8E8E48FEFCF` (+ protective MBR) | 238.47 GiB | 3 partitions, no other signatures | n/a |
| 1 | `nvme1n1p1` | vfat ESP, UUID `2696-E825`, PARTUUID `6476adc2-a91f-4650-833e-476479bd810d` | 1 GiB | Standard Ubuntu Secure Boot shim set only: `EFI/BOOT/{BOOTX64.EFI,fbx64.efi,mmx64.efi}`, `EFI/ubuntu/{shimx64.efi,grubx64.efi,mmx64.efi,BOOTX64.CSV,grub.cfg}` — 7 files + 3 dirs, all mtime 2025-10-16T19:09:46 (install time). No user data | no |
| 2 | `nvme1n1p2` | ext4, UUID `9de11806-959d-4ac7-8a66-33e29d0a2467`, PARTUUID `a752f942-7a2d-4877-9ab8-06a01bd11afc` | 2 GiB | `/boot` of the stale install ("Last mounted on: /boot"): kernels `6.14.0-35-generic` and `6.14.0-36-generic` (vmlinuz/initrd/config/System.map), `grub/` (unicode.pf2, x86_64-efi modules, locale, fonts, grub.cfg 8123 B mtime 2025-11-21, grubenv), empty `efi/`, `lost+found`. Fs created 2025-10-16, last write 2025-11-29, mount count 5, `needs_recovery` flag set (unclean final shutdown). No user data | no |
| 3 | `nvme1n1p3` | LVM2_member (PV), UUID `rrc7yi-VWet-0zoq-Tu9L-INbS-y7fe-WQgrbe`, PARTUUID `d515bff4-29fd-4c1f-b5dc-858504548c0c` | 235.42 GiB | Sole PV of VG `ubuntu-vg` (see §5) | no |
| 3a | `ubuntu-vg/ubuntu-lv` (dm-0, `ubuntu--vg-ubuntu--lv`) | ext4, UUID `a8d18ab5-9cd3-4cb4-83db-5e569131aeae`, LV UUID `IwORMt-AWsc-6YUU-Jvc0-CdXT-3Cmb-bJU0aA` | 100 GiB | **Rootfs of a lived-in foreign Ubuntu install — see §4 (user data present)** | no |

No partition, PV, VG, LV, filesystem, or signature exists on the target disk beyond this table. `file -s` signatures: disk = protective MBR/GPT; p1 = FAT32 (mkfs.fat, serial 0x2696e825); p2 = ext4 (needs journal recovery); p3 = LVM2 PV size 252783362048.

## 4. User-data scan of the stale rootfs (ubuntu-lv) — VERDICT-DRIVING EVIDENCE

Read-only scan method: `debugfs` (read-only mode, no `-w`; filesystem never mounted — mounting is prohibited this session) walking every directory; directory listings and inode metadata only, **no file content was read** (per the WO boundary). Times are UTC.

**Filesystem metadata:** UUID `a8d18ab5-…`; "Last mounted on: `/`"; created 2025-10-16T19:07:24; last mount time 2025-11-12T15:46:48; **last write time 2026-02-26T07:09:56**; mount count 5; inodes 6,553,600 total / 6,103,220 free (450,380 used); blocks 26,214,400 total / 20,141,899 free (~23% used of 100 GiB).

**Full-tree walk (complete — 57,681 directories visited, 21 levels, 0 unwalked):**

- **397,773 non-dot entries: 329,655 regular files, 57,680 directories, 9,909 symlinks, 529 other.**
- **Newest mtime: 2026-02-26T07:27 (`/var/lib/systemd/timesync/clock`)** — the filesystem was a live, running system until 2026-02-26.
- Top level: standard rootfs (`bin`→usr merge, `boot`, `etc`, `home`, `opt`, `root`, `srv`, `usr`, `var`, `swap.img` 8 GiB, …).

**Non-OS-skeleton content found (directory listings only):**

- `/home` — **three user home directories**: `administrator` (mtime 2025-10-18), `agent0` (2025-12-05), `hx-lang-server@hx.dev.local` (2025-12-04).
- `/srv/LangGraph-Server-Deployment/` — application deployment (2025-11-12).
- `/opt/hx-lang-server/` — application deployment (2025-12-04).
- `/root/` — `.ansible/` (2025-10-22), **`.git-credentials` (69 B, 2025-11-12 — a stored git credential file)**, `.pm2/` (2025-12-05), `.npm/`, `.cache/`, `.ssh/` (2025-10-16), `.local/`.
- `/etc` — `apache2/`, `X11/`, `krb5.conf` (mtime 2026-02-26), `hosts.backup-20251030-030412`, fwupd, cloud-init state — a configured, operated system, not a fresh install.

**Assessment:** the target disk does not carry a disposable installer artifact. It carries a complete, operated Ubuntu Server system from another environment (user and path names reference `hx.dev.local`, which is not the current HX `hx.local.arpa` fleet domain) with user homes, two application deployments, PM2/Node/Ansible operational state, an SSH-related `.ssh/` directory (existence only — contents not read), and a stored credential file, live as recently as 2026-02-26. Whether any of this must be retained is **not rick's call** — per the WO this is exactly the stop-and-escalate condition.

## 5. EXCLUSIVE LVM TOPOLOGY PROOF — PROVEN

(a) **ubuntu-vg contains ONLY ubuntu-lv:** `vgs -o vg_name,vg_uuid,pv_count,lv_count` → `ubuntu-vg  56xSQO-uA0s-1eQe-lw4i-YBnU-aKzc-eNDEPE  1  1` — one PV, one LV. No other LV exists.

(b) **Every extent maps to the target-disk PV and no other PV:**

```text
$ pvs -o pv_name,vg_name,pv_size,pv_free,pv_uuid,dev_size
  PV             VG        PSize   PFree   PV UUID                                DevSize
  /dev/nvme1n1p3 ubuntu-vg 235.42g 135.42g rrc7yi-VWet-0zoq-Tu9L-INbS-y7fe-WQgrbe 235.42g
$ lvs -o lv_name,vg_name,lv_size,seg_count,devices,lv_uuid
  LV        VG        LSize   #Seg Devices           LV UUID
  ubuntu-lv ubuntu-vg 100.00g    1 /dev/nvme1n1p3(0) IwORMt-AWsc-6YUU-Jvc0-CdXT-3Cmb-bJU0aA
$ pvdisplay -m
  PV Name /dev/nvme1n1p3 — VG ubuntu-vg — Total PE 60268, Allocated 25600, Free 34668
  Physical extent 0 to 25599:  Logical volume /dev/ubuntu-vg/ubuntu-lv, Logical extents 0 to 25599
  Physical extent 25600 to 60267:  FREE
$ dmsetup table
  ubuntu--vg-ubuntu--lv: 0 209715200 linear 259:6 2048
```

`259:6` resolves via `/sys/dev/block/259:6` → `…/nvme1/nvme1n1/nvme1n1p3` — the LV's single segment is linear on `/dev/nvme1n1p3`, which is a child of the target disk. `pvs` shows exactly one PV on the entire host. No extent of ubuntu-vg touches the OS disk or any other device.

(c) **Exact PV path intended for pvremove, recorded WITH the stable identity:**

> PV path: **`/dev/nvme1n1p3`** (PV UUID `rrc7yi-VWet-0zoq-Tu9L-INbS-y7fe-WQgrbe`) — child of the disk whose stable identity is **model `PC SN740 NVMe WD 256GB`, serial `22170Z804761`, WWN `eui.e8238fa6bf530001001b448b4b6f22e2`** (§2.1). Per the WO, phase 2 must re-match this stable identity live immediately before any destructive command and use only the path whose live serial/WWN matches.

## 6. Root/boot-critical sources are NOT on the target disk — PROVEN

```text
$ findmnt /            → /dev/nvme0n1p2  ext4  rw,relatime
$ findmnt /boot        → NOT-A-SEPARATE-MOUNT (directory on /, i.e. nvme0n1p2)
$ findmnt /boot/efi    → /dev/nvme0n1p1  vfat
$ findmnt --real       → only / (nvme0n1p2) and /boot/efi (nvme0n1p1) — no other real mounts
$ swapon --show        → /swap.img  file  4G  (a file on /, i.e. on nvme0n1p2)
$ /etc/fstab           → references ONLY UUID 9408b77f-… (nvme0n1p2, /), UUID 5E69-CD01 (nvme0n1p1, /boot/efi), /swap.img
$ grep for every target-disk UUID (2696-E825, 9de11806-…, rrc7yi-…, a8d18ab5-…, PTUUID 20376289-…) in /etc/fstab → NONE
$ /etc/crypttab        → EMPTY (no encrypted dependencies anywhere)
```

`/`, `/boot` (a directory on `/`), `/boot/efi`, and the active swap file all live on the OS disk `nvme0n1` (serial `49FF70BNF0AN` — matches discovery). Nothing boot-critical is on the target disk or any child partition of it. Nothing on the live system mounts, or is configured to mount, anything from the target disk.

## 7. Verdict

# **RETAINABLE-DATA-FOUND — STOP, ESCALATE.**

Both safety proofs PASS (§5 exclusive LVM topology; §6 root/boot-critical outside the target). The blocker is §4: the target disk carries a complete, previously operated foreign Ubuntu system with three user home directories, two application deployments (`/srv/LangGraph-Server-Deployment`, `/opt/hx-lang-server`), operational state (Ansible, PM2, npm), an SSH-related `.ssh/` directory (existence only — contents not read), and a stored git-credential file — live until 2026-02-26. This is not the "expected empty additional drive" the operation assumed. Per WO-01 (`RETAINABLE-DATA-FOUND → stop, escalate`), phase 1 ends here. **Phase 2 remains LOCKED.** The destructive phase must not be released on the basis of this device map without the governor escalating the §4 inventory to the owner for an explicit retain/discard decision.

## 8. Anomalies and deviations

1. **RETAINABLE-DATA-FOUND** (§4) — the controlling anomaly.
2. `nvme-cli` absent on hxs-6; `nvme list`/`nvme id-ctrl` not runnable without an (unauthorized) package install. Stable identity recorded verbatim from kernel sysfs, corroborated by lsblk and udev by-id (§2.1).
3. Discovery drift (already known as baseline F-1): discovery.md records one NVMe and no LVM; live state is two NVMes plus LVM. New fact from this pass: the second disk's content is a foreign lived-in system last written 2026-02-26 (content evidence, recorded separately in §4). The disk's ATTACHMENT date to hxs-6 is UNKNOWN — no independent inventory record establishes it, and the filesystem last-write does not bound when the disk was physically attached: it may have been present-but-unrecorded at the 2026-08-12 discovery or attached at any time since.
4. The stale rootfs and its /boot carry `needs_recovery` (unclean final shutdown) — consistent with a disk pulled from a running/powered-off machine. Read-only scan unaffected.
5. The stale install's user/path naming (`agent0`, `hx-lang-server@hx.dev.local`, `hx.dev.local`) does not match current fleet naming — treated as inference from directory names only; no file content was read to confirm the foreign system's identity (WO content-read boundary).

## 9. Sequential command log (all hxsa@hxs-5 → hxsa@hxs-6 over SSH unless noted; all read-only)

| Seq | UTC | Command (sanitized) | Exit |
| ---: | --- | --- | --- |
| 1 | 05:38–05:39 | Read charter/profile/AGENTS.md/goal/WO/state-log/discovery/servers-contract/baseline-wave/pre-work; TKV survey | 0 |
| 2 | 05:39 | Local preflight: hostname, date, keydoc existence, known_hosts `ssh-keygen -F` (pinned), ED25519 fingerprint vs pre-work record → MATCH | 0 |
| 3 | 05:39 | Create `/tmp/rick-hxs6-storage-askpass.sh` (0700); extraction smoke test → 10 chars | 0 |
| 4 | 05:40 | Identity probe: hostname, SSH_CONNECTION, machine-id, date, os-release, kernel, `sudo -n true` | 0 |
| 5 | 05:41 | `lsblk -o NAME,SIZE,TYPE,FSTYPE,LABEL,UUID,MOUNTPOINT,SERIAL,WWN`; `command -v nvme` (ABSENT); `blkid`; `blkid -p` both disks | 0 |
| 6 | 05:42 | sysfs model/serial/wwid both disks; `ls -l /dev/disk/by-id`; `pvs/vgs/lvs -o …devices…`; `pvdisplay -m`; `dmsetup table` | 0 |
| 7 | 05:43 | `lsblk -o NAME,MAJ:MIN`; `/sys/dev/block/259:6` resolve; `findmnt /`, `/boot`, `/boot/efi`, `--real`; `swapon --show`; `/proc/swaps`; `/etc/fstab`; `/etc/crypttab`; fstab target-UUID grep → NONE | 0 |
| 8 | 05:45 | `fdisk -l` both disks (read-only print); `file -s` target disk + children + LV; listing-tool availability | 0 |
| 9 | 05:46 | `debugfs -R stats` + `ls -l /` + recursive attempt on nvme1n1p2 (18 entries; `-r` non-recursive in this build) | 0 |
| 10 | 05:47 | First LV BFS walk (parse bug — no re.M; zero results, rerun) | 0 |
| 11 | 05:47 | Raw `debugfs -f` format check on p2 and LV root listing | 0 |
| 12 | 05:49 | Full LV BFS walk via sudo python3 stdin script driving read-only debugfs: 57,681 dirs, 397,773 entries, newest mtime 2026-02-26T07:27 | 0 |
| 13 | 05:51 | `debugfs ls -l /efi /grub` on p2; read-only python3 FAT32 directory walk of ESP (11 entries) | 0 |
| 14 | 05:52 | Write this evidence doc (repo, on hxs-5); delete askpass helper; verify absent | 0 |

Second Brain statement (standing directive): (1) opportunity identified: none new — the task consumed existing records (discovery, baseline F-1, credential record) per the retrieve-before-investigating rule; (2) capability: n/a; (3) disposition: deferred — the only durable artifact is this evidence doc; Carol's catalog receipt is the governor's dispatch; (4) reasoning: a read-only verification pass inside an existing pilot creates no new Second Brain capability.

---

**End of phase 1. Rick stops here per WO-01: no destructive command was issued, and none will be, without the governor's dual-gate release.**
