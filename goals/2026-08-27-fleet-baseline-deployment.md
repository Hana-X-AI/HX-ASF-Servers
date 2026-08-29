# Goal: Fleet Baseline Deployment

**Date:** 2026-08-27 · **Owner directive:** "complete the baseline platform deployment" (GO same day) · **Governor:** Kimi-K3 [OPEN CORRECTION 2026-08-29, labeled: governor role now held by Flash per AGENTS.md transition; original wording preserved as history] · **Executor:** rick
**Sequencing (owner, OmniRoute log row 43):** this goal FIRST; OmniRoute L1-M3 closure follows its completion.

[OPEN CORRECTION 2026-08-29, labeled, append-only: **Status:** COMPLETE —
2026-08-28. Fleet baseline waves delivered across three evidence docs:
`servers/2026-08-26-fleet-time-mask.md` (wave 1: time + mask),
`servers/2026-08-27-fleet-baseline-wave.md` (wave 2: full baseline),
`servers/2026-08-28-fleet-baseline-hxs11-20-21.md` (wave 3: hxs-11/20/21).
hxs-7 excluded (decommissioned); hxs-6 Secure Boot recorded (owner decision).
Registry FQDN census 2026-08-28: 16 active hosts, 16 FQDNs resolving.
Original header lines preserved above unchanged.]

## Objective

Bring every in-scope fleet host to the declared baseline — verified identity/OS, one timezone (Etc/UTC), one NTP source (time.cloudflare.com), the proven 4-target sleep-mask set, library selftest green — with per-host TKV records refreshed and evidence the owner can audit.

## Scope

- **Fresh (7):** hxs-6, hxs-9, hxs-10, hxs-12, hxs-13, hxs-14, hxs-15 — full baseline pass (verify, pin, mask, selftest, records).
- **Re-verify (5):** hxs-1, hxs-2, hxs-3, hxs-4, hxs-8 — confirm the proven posture holds; drift reported, fixed only within the two sanctioned classes.
- **Excluded:** hxs-5 (control plane), hxs-7 (replaced by hxs-20), hxs-20/hxs-21 (provisioning), hxs-11 (owner flag unreachable).
- hxs-6 Secure Boot ENABLED: record only — owner decision pending (BIOS).

## Acceptance

1. Every in-scope host carries an evidence-backed verdict (PASS / REPORT / FAIL); REPORT names its closing direction.
2. NTP + mask post-apply re-checks green on every mutated host.
3. `/opt/tkv-local/servers/<host>/pre-work-results.md` refreshed per fresh host; evidence doc `servers/2026-08-27-fleet-baseline-wave.md` delivered.
4. Zero secret values in any artifact; catalog wave (Carol) closes the handoff with validate.py 4/4.

## Boundaries

Two sanctioned mutation classes only (NTP pin, sleep-mask align). Everything else read-only; any other need stops and escalates to the governor. Local-model rule applies to the executor. No git commits without owner approval per instance.
