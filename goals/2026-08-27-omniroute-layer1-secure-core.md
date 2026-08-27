# Goal: OmniRoute Layer 1 — Secure Core Gateway on hxs-8 (native, owner-authorized)

- Goal ID: 2026-08-27-omniroute-layer1-secure-core (this file's name)
- Version: 1
- Status: in-progress — M0 authorized 2026-08-27 (OD-12 owner-authorized; OD-03 acknowledged)
- Owner: Agent Zero
- Created: 2026-08-27
- Human authority: Agent Zero
- Agent lane(s): kimi-k3 (governor), trinity (OmniRoute lifecycle engineer), rick (host OS plane), john (backend integration checks), carol (catalog)
- Parent program: goals/2026-08-27-omniroute-trinity-layer0.md (COMPLETE); manifest `pilots/PILOT-OMNIROUTE-LAYER0-001/10-control-manifest.yaml`

## Intent

Install and qualify OmniRoute v3.8.51 on hxs-8 as the HX governed model-traffic
plane: pinned runtime, encrypted-secrets deployment (OD-13), all four HX
backends registered behind it with routing confirmed (OD-08 amended), LAN-only
exposure with OmniRoute's own authN/authZ (OD-07), health and backup/rollback
proven. Native systemd service — **never Docker** (owner rule, 2026-08-27).

## Owner parameters (ratified 2026-08-27)

- OD-04: native Node systemd service; **never Docker** (owner rule; runner-cli flavor BLOCKED, compose paths void).
- OD-08 (amended): register **all four HX backends** — Qwen-X (hxs-1), Coder-X (hxs-2), Meta-X (hxs-3), Chat-X (hxs-4) — behind the gateway from the start; routing confirmation across all four is a first-class acceptance test. [amendment 2026-08-27: Chat-X on hxs-4 is loopback-only by standing security posture — its registration stands, and its parity check is **posture-blocked (an approved posture exception), not a failed acceptance test**. It remains so unless the owner explicitly authorizes a scoped exposure change for hxs-4; all other backends carry full parity requirements. Scope of this exception: hxs-8's view of hxs-4 only.]
- OD-13: env-provision `JWT_SECRET` + `API_KEY_SECRET` (generated locally, provisioned via the service environment, never accepted from product defaults) **and** set `STORAGE_ENCRYPTION_KEY` (activates the AES-256-GCM field encryption — the product ships plaintext-passthrough without it). [amendment 2026-08-27 — approved injection mechanism and prohibited locations, matching the deployed L1-M2 reality: values are generated on-host and injected ONLY via a root-only 0640 systemd drop-in, recorded by sha256 never value. PROHIBITED at rest: repository files, world-readable unit files, logs/journals/receipts/artifacts, and the database (secrets namespace must hold 0 plaintext rows; connection fields must be `enc:v1:` ciphertext). ALLOWED: plaintext in process memory and the service's own runtime environment — that is inherent to env injection and is not a violation.]
- OD-07: LAN bind only (192.168.50.0/24), management endpoints behind OmniRoute's own authN/authZ (its proven proxy.ts pipeline), **no host firewall** (owner rule); O1 monitoring tripwire stands.
- Local-model-only everywhere: no cloud providers, no cloud agent features; OmniRoute agent-like surfaces (MCP/A2A/ACP/Conductor/copilot/tunnels/cloud agents) stay disabled/blocked per the ledger register; skills execution and background jobs get explicit deployment settings (the ledger's not-code-enforced finding).
- Backup (OD-09): plaintext SQLite snapshots to a managed directory plus our own encryption if required — the product's backup encryption is write-only and its cloud upload is a dead endpoint (CAP-P8-905/906); never rely on either.

## Layer-1 gate (acceptance)

1. Runtime: Node within engines (`>=22.22.2 <23 || >=24.0.0 <27`), systemd service up after reboot with no human action, native (no Docker).
2. Secrets: no plaintext secret values at rest in the database (secrets namespace 0 rows; connection rows `enc:v1:`), in repository files, in world-readable unit files, or in any log/journal/receipt/artifact (OD-13 verified: values generated on-host, injected via a root-only 0640 drop-in recorded by hash, STORAGE_ENCRYPTION_KEY active). Plaintext in process memory/the runtime environment is inherent to env injection and explicitly allowed.
3. Routing: all four backends registered with identity evidence; **direct-vs-routed parity** — a known-answer task through each backend direct vs routed through OmniRoute, with response-shape comparison and usage accounting visible in the ledger's own evidence paths.
4. Health: the layered health surface answers correctly (public liveness vs management views with the documented auth split).
5. Backup/rollback: a snapshot restores to a working state; rollback of the install is a documented, rehearsed inverse.
6. Restart: two service restarts and one cold reboot return to ready state with the four-backend routing intact.
7. No cloud models, no `:cloud` tags anywhere (O1 tripwire); no agent-like surfaces enabled.

## Out of scope for this goal

Layer 2+ (route combos, strategy characterization, quotas/budgets/sessions),
Layer 3 (intelligence/memory/modalities), Layer 4 (agent/ecosystem surfaces),
any Docker/container work, any host other than hxs-8, any cloud provider.

## Second Brain evaluation (standing directive)

1. Opportunity identified: **yes** — the first governed traffic plane joins the catalog; the deployment's configuration.md is the second of its class (hxs-3 was first); the four-backend routing evidence becomes the fleet's routing-capability record.
2. Roadmap capability/pattern: capability registration through the Second Brain catalog — the backend records gain their first consumer-of-record; the OD-13 secrets pattern becomes the reference for future service deployments.
3. Disposition: **implemented** — built into the gate criteria (identity evidence, parity records, configuration.md, catalog waves).
4. Evidence/reasoning: recorded per work order and in the pilot state log.
