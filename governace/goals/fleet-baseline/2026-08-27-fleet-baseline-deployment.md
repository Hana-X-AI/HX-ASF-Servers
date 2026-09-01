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

[OPEN CORRECTION 2026-08-30, labeled, append-only — hxs-6 SECURE BOOT
NON-COMPLIANCE: the 2026-08-28 COMPLETE status above is CORRECTED for hxs-6.
hxs-6 is recorded with **Secure Boot ENABLED** (F-5, `servers/2026-08-27-fleet-baseline-wave.md`,
T-SB-1), which directly violates the standing owner directive — "Secure Boot stays
disabled on HX hosts, now and always — do not enable it" (owner directive
2026-08-24, confirmed 2026-08-25). hxs-6 is therefore **non-compliant** with the
fleet baseline's Secure Boot posture and is ESCALATED for an owner decision
(BIOS remediation); it must not be counted as fleet-baseline-complete until the
Secure Boot state is resolved and re-verified. The prior COMPLETE wording is
preserved as history; the fleet baseline completion claim stands corrected to
exclude hxs-6's Secure Boot posture until resolved.]

**[CURRENT STATUS 2026-08-30, labeled, append-only — PARTIAL / IN-PROGRESS:** the
fleet baseline is delivered for all in-scope hosts EXCEPT hxs-6's Secure Boot
posture, which is non-compliant and escalated for an owner BIOS decision. Current
status is **in-progress** (partial): the baseline wave evidence stands, but the
goal is NOT counted complete until hxs-6's Secure Boot is resolved and
re-verified. The COMPLETE wording above is retained only as historical context;
status consumers must read the current state as in-progress/partial, excluding
hxs-6 from completion credit.**]**

**[CURRENT STATUS 2026-08-31, labeled, append-only — COMPLETE:** owner confirmed
2026-08-31 that hxs-6 is compliant; the hxs-6 Secure Boot non-compliance that
held this goal in-progress/partial is resolved. The 2026-08-30 in-progress/partial
status is superseded; the fleet baseline is counted COMPLETE.**]**

## Objective

Bring every in-scope fleet host to the declared baseline — verified identity/OS, one timezone (Etc/UTC), one NTP source (time.cloudflare.com), the proven 4-target sleep-mask set, library selftest green — with per-host TKV records refreshed and evidence the owner can audit.

## Scope

- **Fresh (7):** hxs-6, hxs-9, hxs-10, hxs-12, hxs-13, hxs-14, hxs-15 — full baseline pass (verify, pin, mask, selftest, records).
- **Re-verify (5):** hxs-1, hxs-2, hxs-3, hxs-4, hxs-8 — confirm the proven posture holds; drift reported, fixed only within the two sanctioned classes.
- **Excluded:** hxs-5 (control plane), hxs-7 (replaced by hxs-20), hxs-20/hxs-21 (provisioning), hxs-11 (owner flag unreachable).
- hxs-6 Secure Boot ENABLED: record only — owner decision pending (BIOS). [LABELED CORRECTION 2026-08-31, append-only: hxs-6 is now COMPLIANT per owner confirmation 2026-08-31; the prior non-compliance and "owner decision pending" wording are historical — see the CURRENT STATUS 2026-08-31 block above.]

## Acceptance

1. Every in-scope host carries an evidence-backed verdict (PASS / REPORT / FAIL); REPORT names its closing direction.
2. NTP + mask post-apply re-checks green on every mutated host.
3. `/opt/tkv-local/servers/<host>/pre-work-results.md` refreshed per fresh host; evidence doc `servers/2026-08-27-fleet-baseline-wave.md` delivered.
4. Zero secret values in any artifact; catalog wave (Carol) closes the handoff with validate.py 4/4.
   [LABELED CORRECTION 2026-08-30, append-only: the acceptance gate now reads
   `validate.py 5/5 PASS` — the governance-path check SY-2 was added to the
   validation suite. The 4/4 wording above is preserved as the completed record's
   original acceptance text.]

## Boundaries

Two sanctioned mutation classes only (NTP pin, sleep-mask align). Everything else read-only; any other need stops and escalates to the governor. Local-model rule applies to the executor. No git commits without owner approval per instance.

<!-- Machine-readable current state (O1, work-state.schema.yaml). The prose
     above is the historical record and is never rewritten; this block is the
     single source every status tool reads. -->

```yaml work-state
id: 2026-08-27-fleet-baseline-deployment
status: complete
status_date: 2026-08-31
authority: >-
  [CURRENT STATUS 2026-08-31] COMPLETE — owner confirmed 2026-08-31 hxs-6 is compliant; hxs-6 Secure Boot non-compliance resolved
reconcile: none
```
