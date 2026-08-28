# Goal: hxs-6 additional-storage provisioning (owner disposition #4, 2026-08-27)

- Goal ID: 2026-08-28-hxs6-storage-provisioning (this file's name)
- Version: 1
- Status: **DRAFT — held for owner GO** (prepared per the owner's consolidated direction "prepare a separately controlled storage operation"; NOT dispatched)
- Owner: Agent-Zero
- Created: 2026-08-28
- Human authority: Agent-Zero
- Agent lane(s): kimi-k3 (governor), rick (executor), carol (catalog)

## Intent

Owner disposition 2026-08-27 #4: the additional drive in hxs-6 is expected — **reformat it and make it available** for storage or another approved use. rick's baseline wave (2026-08-27) found a second NVMe (`nvme1n1`) plus an LVM `ubuntu-vg/ubuntu-lv` that the 2026-08-13 discovery never recorded.

## Non-negotiable ordering (owner's own words)

Before ANY destructive operation: **verify the exact target device** and **confirm it contains no data that must be retained**. The `ubuntu-vg` name is the Ubuntu installer's default — the verification must PROVE the live root filesystem does not depend on that LVM before anything is wiped.

## Acceptance

1. Device-map evidence published and reviewed (governor gate) showing zero retainable data.
2. Final state recorded: filesystem, mount point, ownership, intended use.
3. hxs-6 registry + TKV records updated; Carol catalogs.

## Boundaries

Destructive class. Governor gate between verification and execution. No other host, device, or partition in scope. No Docker. Local-model rule for the executor.
