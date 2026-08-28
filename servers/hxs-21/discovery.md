# hxs-21 — Discovery

**Phase:** 1
**Discovery date:** 2026-08-28

This record uses owner-supplied interactive terminal evidence from 2026-08-28. It was
not produced by the project collector or independently verified over SSH. The supplied
session included human preparation changes to sudo and firewall state before the final
checks shown below. Facts not present in that evidence are explicitly unavailable.

## Identity
- Record identity: hxs-21
- Observed shell prompt: `hxs-21`. A direct `hostname` or `hostnamectl` result was not supplied
- FQDN: unavailable from supplied evidence
- Manufacturer: unavailable from supplied evidence
- Model: unavailable from supplied evidence
- Baseboard: unavailable from supplied evidence
- Serial: unavailable from supplied evidence
- Machine ID: unavailable from supplied evidence
- Chassis type: unavailable from supplied evidence
- BIOS / UEFI: unavailable from supplied evidence
- Boot mode: unavailable from supplied evidence
- Secure Boot: unavailable from supplied evidence

## CPU
- Model: unavailable from supplied evidence
- Sockets: unavailable from supplied evidence
- Physical cores: unavailable from supplied evidence
- Threads: unavailable from supplied evidence
- Architecture: x86_64
- NUMA: unavailable from supplied evidence
- Virtualization: unavailable from supplied evidence

## Memory
- Installed RAM: unavailable from supplied evidence
- Current memory usage: 0 percent in the Ubuntu system-information summary
- DIMM layout: unavailable from supplied evidence
- Type / speed: unavailable from supplied evidence
- ECC: unavailable from supplied evidence
- Swap: present; 0 percent used. Capacity and backing type are unavailable from supplied evidence

## GPU / Accelerators
- GPU count: unavailable from supplied evidence
- Model(s): unavailable from supplied evidence
- VRAM per GPU: unavailable from supplied evidence
- Total VRAM: unavailable from supplied evidence
- Driver: unavailable from supplied evidence
- UUID(s): unavailable from supplied evidence
- CUDA availability: unavailable from supplied evidence

## Storage

| Device | Model | Serial | Type | Capacity | Filesystem / Role | Mount |
|---|---|---|---|---|---|---|
| unavailable | unavailable | unavailable | unavailable | 232.64 GB filesystem | root filesystem; filesystem type unavailable | / |

- Root filesystem usage: 4.7 percent of 232.64 GB
- Underlying block device, partition layout, filesystem type, additional storage, LVM, RAID and SMART state: unavailable from supplied evidence

## Network
- Primary interface: eno1
- MAC: unavailable from supplied evidence
- IPv4: 192.168.50.21; prefix length unavailable from supplied evidence
- Gateway: unavailable from supplied evidence
- DNS: unavailable from supplied evidence
- Link speed: unavailable from supplied evidence
- IPv6: unavailable from supplied evidence
- Other interfaces: unavailable from supplied evidence
- Listening services: SSH is active on TCP port 22; listener address scope was not supplied

## Operating System
- Distribution: Ubuntu
- Release: 24.04.4 LTS
- Kernel: 7.0.0-30-generic
- Architecture: x86_64
- Timezone: unavailable from supplied evidence. The system-information timestamp was displayed in UTC
- Update state: 44 updates can be applied immediately, including 1 standard security update. Expanded Security Maintenance for Applications is not enabled
- Reboot required: unavailable from supplied evidence
- Reported system temperature: 44.0 C

## Relevant Existing Software / Services
- openssh-server is active; effective SSH port is 22
- Passwordless sudo was configured for `hxsa` in `/etc/sudoers.d/90-hx-admin`; the drop-in and complete sudoers configuration passed `visudo`, and `sudo -n true` returned 0
- Firewall: ufw reports inactive; `ufw.service` is disabled and inactive
- The loaded nftables ruleset contains IPv4 and IPv6 filter chains with ACCEPT policies and no filtering rules shown
- firewalld is inactive or its unit is absent
- Other software, services, failed units and diagnostic tooling: unavailable from supplied evidence

## Capability Summary
- CPU: unavailable from supplied evidence
- Memory: installed capacity and DIMM topology unavailable; the system-information summary reported 0 percent in use
- GPU: unavailable from supplied evidence
- Storage: root filesystem capacity 232.64 GB, 4.7 percent used; device topology unavailable
- Network: eno1 carries the owner-reported address 192.168.50.21; link characteristics and remaining network configuration unavailable
- Constraints / notable characteristics:
  - the observed IPv4 address is not corroborated by a current hxs-21 registry row and must be verified before fleet registration
  - hardware, firmware and detailed storage discovery remain incomplete
  - 44 package updates are immediately available, including 1 standard security update
  - ufw is inactive and disabled, consistent with the HX no-host-firewall rule
  - SSH is active on TCP port 22
  - Expanded Security Maintenance for Applications is not enabled

## Notes
- Evidence timestamp: 2026-08-28 00:20:51 UTC
- The Ubuntu summary reported system load 0.18, 141 processes and 0 users logged in
- One sudo password attempt failed before authentication succeeded; the sudoers change then passed all reported validation checks
- The supplied session changed sudo and ufw state before verification; those values are prepared state, not an untouched as-found baseline
- No role, workload or model is assigned in this record
- Second Brain opportunity: no new capability was identified. This record applies the existing per-host discovery pattern; catalog intake remains Carol's governed lane

**Discovery Status:** IN PROGRESS

> Role assignment is not performed in this file.