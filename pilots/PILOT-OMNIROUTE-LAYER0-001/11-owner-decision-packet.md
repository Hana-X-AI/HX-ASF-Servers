# Owner Decision Packet — OmniRoute program (Wave 0C)

| Field | Value |
| --- | --- |
| Date | 2026-08-27 (UTC) |
| From | Kimi-K3 (governor) |
| For | Agent Zero |
| Basis | goal contract OD register, the capability ledger (367 entries), hxs-8 readiness, the week's governance evidence |

Every item carries the exact decision needed, the governor's recommendation, and what it blocks. Nothing here is decided for you.

## Decided (for the record — no action)

- **OD-01 target host: hxs-8** (your selection; online; readiness evidence delivered).
- **OD-02 Trinity ratification: O1 adopt-as-corrected** (active; her first commission produced the ledger).
- **OD-13 secrets at rest: RATIFIED 2026-08-27** — env-provision `JWT_SECRET` + `API_KEY_SECRET` and set `STORAGE_ENCRYPTION_KEY` at install, never accept defaults (the ledger proved the product's defaults persist secrets plaintext and its encrypted-store doc claim is stale).

## Open — needed for Layer 1

| ID | Decision needed | Governor recommendation | Blocks |
| --- | --- | --- | --- |
| OD-03 | Acknowledge hxs-8 readiness evidence | Read `04-rick-hxs8-readiness.md` (SUITABLE-WITH-FINDINGS; memory resolved 32+16 GB both channels non-ECC; ports free; Node absent) and acknowledge | any host-dependent work |
| OD-04 | Deployment mode | **Native Node systemd service** on hxs-8 (clean host, fewer moving parts; the runner-cli container flavor is BLOCKED anyway; compose stays LAB-ONLY) | install shape |
| OD-05 | FQDN + internal DNS | `omniroute.hx.local.arpa` via the fleet DNS (rick's plane at Layer 1) | naming |
| OD-06 | TLS termination | host TLS via a small reverse proxy or OmniRoute's own TLS; management and inference paths separated (P4 evidence shows the split exists) | transport security |
| OD-07 | Allowed clients / exposure | **LAN bind only** (192.168.50.0/24), management endpoints behind OmniRoute's own authN/authZ (its proven proxy.ts pipeline), **no host firewall** (your rule); the O1 monitoring tripwire stands | exposure |
| OD-08 | Initial backend(s) | **Exactly one local backend first: Qwen-X** (ACTIVE, M8-signed, loopback-proven LAN health) — the Secure Core shape; Coder-X/Meta-X join at Layer 2 after their own M8s | routing start |
| OD-09 | Backup / retention / RPO / RTO | Plaintext SQLite snapshots to a managed dir + **our own encryption** if required — the product's backup encryption is write-only and its cloud upload is a dead endpoint (CAP-P8-905/906); retention 20 snapshots matches its default | data safety |
| OD-12 | **Layer 1 authorization** | Authorize after reviewing this packet + `18-independent-verification-report.md` + the KK3 gate decision | the install itself |

## Open — later layers

| ID | Decision needed | When |
| --- | --- | --- |
| OD-10 | Qdrant / memory disposition (existing-service designation vs disabled) | Layer 3 |
| OD-11 | Production-version policy (upgrade cadence from the pinned snapshot) | program-level |

## Deliberate non-decisions (recorded so they stay closed)

- No DeepSeek Harness anything — it never existed (KDD-0006).
- No `/opt/tkv-local/omniroute` knowledge root — corpus + catalog stand.
- No host firewalls — the LAN plus OmniRoute authN/authZ is the boundary.
- No cloud models or remote inference anywhere in the program (local-model-first rule).
- No activation of OmniRoute agent-like surfaces (MCP/A2A/ACP/Conductor/copilot/tunnels/cloud agents) — disabled-by-default; 8 BLOCKED entries; the copilot driver and Conductor hub are the two highest-risk surfaces and stay off.
- No backup encryption or cloud-upload reliance — proven nonfunctional.
- No ATEM routing assumption for Meta-X (no adapter exists).
