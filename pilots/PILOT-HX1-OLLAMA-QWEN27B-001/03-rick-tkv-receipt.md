# Rick — TKV Knowledge Review Receipt (M1)

- Session: `rick-m1-20260824-01`
- Work order: `WO-HX1-RICK-M1-001` (sha256 `c6c32003d9222087ca7c25caa3090c3b6fb8b243fc863bddb65a7e2b03d5cd34`)
- Pilot: `PILOT-HX1-OLLAMA-QWEN27B-001`

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Host: HX-1 (192.168.50.200 — target; review executed from hxs-5)
Source: /opt/tkv-local/ubuntu (ubuntu.com-main corpus)
Reviewed At: 2026-08-24T23:37:46+00:00
Relevant Files: 8 reviewed (targeted: release/security/hardware content for a 24.04 LTS GPU host):
  - /opt/tkv-local/ubuntu/ubuntu.com-main/AGENTS.md
  - /opt/tkv-local/ubuntu/ubuntu.com-main/releases.yaml
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/about/release-cycle.html
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/about/release_cycles/ubuntu-eol.html
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/about/release_cycles/kernel-eol.html
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/security/ (index, oval.html, osv.html, vex.html, cves/, notices/)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/certified/ (index.html, servers.html, components/, hardware-details/)
  - /opt/tkv-local/ubuntu/ubuntu.com-main/templates/server/ (index.html, base_server.html)
Applicable Requirements/Runbooks:
  - agents/rick/profile.md (startup protocol §5, lifecycle §6, authority order §4, sanitization §11)
  - pilots/PILOT-HX1-OLLAMA-QWEN27B-001/plan.md §2.1 (TKV gate), §3/§3.1 (specs + immutable inventory), §7 (Rick requirements)
  - Corpus-derived facts applied to this pilot:
    * releases.yaml: 24.04 "Noble Numbat" current point release 24.04.4; standard-maintenance EOL April 2029; 26.04 "Resolute Raccoon" is latest LTS (April 2026) — release-matching mandatory; latest-LTS guidance must not be applied to HX-1's 24.04.
    * release-cycle.html: LTS = 5 years standard security maintenance + 5 years ESM (Ubuntu Pro) + 5 years Legacy add-on.
    * security/OVAL, OSV, VEX, CVE/notice feeds: machine-readable Ubuntu security status per release — vulnerability status is judged from Ubuntu release-specific security data, not upstream version numbers (profile §3.6).
    * certified/ catalogue: Ubuntu certified server/component registry — reference for hardware support posture, not a per-host guarantee.
Contradictions or Gaps:
  - GAP (known, non-blocking): corpus is the ubuntu.com web application tree, not the Ubuntu OS source tree and not an NVIDIA driver runbook (profile §2.1 states this explicitly). NVIDIA driver installation/verification on 24.04 must follow profile authority order: live host evidence → release-matched man pages/package metadata → current official sources (docs.nvidia.com, documentation.ubuntu.com). No corpus content authorizes any host mutation.
  - MINOR DISCREPANCY (non-blocking): releases.yaml lists 24.04 EOL "April 2029"; rick profile §Appendix B cites Canonical release-cycle "standard security maintenance through May 2029". Both agree on the 5-year window (April 2024 release); month precision differs between web-app metadata and release-cycle page. No operational impact for M1 (read-only inventory).
  - No HX-fleet-specific runbooks in corpus (expected — fleet governance lives in this repository, not the TKV).
Task May Proceed: YES
```
