# Servers

One directory per fleet server: `servers/hxs-N/`. The fleet has 15 servers at
192.168.50.200–214, plus `hxs-cp` (192.168.50.215), the control plane, which holds no
registry row.

- `SERVER-REGISTRY.md` — fleet-level source of truth for discovery status and
  owner-assigned roles.
- `hxs-N/discovery.md` — as-found evidence per server. Imported 2026-08-24 from
  `/opt/tkv-local/servers`; records dated 2026-08-11 through 2026-08-13.
- `_templates/` — discovery and configuration record templates.
- `AGENTS.md` — the server records contract governing this directory.

Rules: records are factual, dated, and carry truth-state labels per
`knowledge/README.md`. Agents never assign roles. `configuration.md` files are created
only in the owner-authorized server implementation phase. Network model and current
DNS state: `knowledge/network.md`.
