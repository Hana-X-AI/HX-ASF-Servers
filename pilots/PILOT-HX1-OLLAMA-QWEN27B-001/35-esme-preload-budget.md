# 35 — Esme: Preload Startup-Budget Conformance to D5 (WO-HX1-JOHN-PB-001)

| Field | Value |
| --- | --- |
| Task ID | WO-HX1-JOHN-PB-001 (parent GOAL-HX1-QWEN38-001) |
| Session | john-pb-20260825-01 |
| Agent | john / Esme (profile `agents/john/profile.md`) |
| Host | hxs-1 (192.168.50.200), Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic |
| Executed from | hxs-5 via SSH hxsa@192.168.50.200 (askpass reads credential at execution; no extracted copy; helper deleted at task end) |
| Window | 2026-08-25T21:51:24Z – 22:00:02Z (hxs-5 clock) |
| Authority | Owner directive 2026-08-25 "do it now" (state log row 53); D5 SLO (state log row 10): detect ≤ 2 min, recover ≤ 15 min (900 s), one bounded attempt |
| Result | **PASS — TASK COMPLETE** |

`[TASK START]`

## 1. Knowledge review receipt

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-1 (target); reference host hxs-5; TKV /opt/tkv-local/ollama surveyed per profile §4
Source: pilot plan.md §4.3; amendment-A01 §4.4 (SUPERSEDED marking, bare alias historical);
  29-esme-m6b-profiles.md §4 (live preload contract: exact -64k alias + digest assertion);
  30-esme-m7a-reboot-cycles.md (boot→ready 60 s ×3); 09-state-log.md rows 9-10, 52-53;
  33-work-order + 34-context-packet (this package)
Reviewed At: 2026-08-25T21:51:24Z
Relevant Files: 8 (above) + live /usr/local/libexec/hx-ollama-preload + live ollama-preload.service
Authority/Version Identified: Ollama 0.32.15 (binary == server, per 29/30); resident identity
  hx-qwen3.8-27b-64k:latest digest 766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a
Applicable Tests/Runbooks: WO §boundaries (manual non-reboot run; systemctl show; clean journal)
Contradictions or Gaps: none — live hashes equal the M6b-frozen values (drift check §3.1)
Task May Proceed: YES
```

Teammate roster (profile §4.2): `agents/` contains john, kimi-k3, rick, carol — all current. Target identity verified before any mutation: `hostname` = `hxs-1`, peer `192.168.50.200` in `$SSH_CONNECTION` (re-verified in the same command as the install), `sudo -n` OK (FACT, 21:51:51Z).

## 2. Test definition (recorded before first mutation)

| Test ID | Property | Procedure | Expected | Pass rule | Result |
| --- | --- | --- | --- | --- | --- |
| T1 | Pre-change identity | sha256sum of both live files | script `01c2a096…9b29f2`, unit `28c60c7d…52299` (M6b-frozen) | exact match | **PASS** |
| T2 | Candidate lint | ShellCheck 0.9.0 (Ubuntu noble deb via `apt download`, no install) + `sh/dash/bash -n` | zero findings; syntax OK | exit 0 | **PASS** |
| T3 | Effective unit value | `systemctl show -p TimeoutStartUSec` after `daemon-reload` | `10min` (600 s) | exact | **PASS** |
| T4 | Post-install identity | sha256sum both files; `ls -l` | candidate hashes; root:root, script 0755, unit 0644 | exact | **PASS** |
| T5 | Manual non-reboot run | `sudo -n /usr/local/libexec/hx-ollama-preload`, timed, model resident | exit 0 fast, `OK - hx-qwen3.8-27b-64k resident` | exit 0 + OK line | **PASS** (17 ms) |
| T6 | Failure semantics preserved | diff review: assertion line byte-identical; all failure paths exit nonzero with journal-visible message | preserved | review | **PASS** |
| T7 | ollama.service undisturbed | pre/post `systemctl show` markers | same `ExecMainStartTimestamp`, `NRestarts=0`, active/running | exact | **PASS** |
| T8 | Journal clean | `journalctl -u ollama-preload/-u ollama --since 21:50`; kernel Xid scan | no errors; no Xid | review | **PASS** |
| T9 | Budget arithmetic | worst-case table vs 600/900 | script worst case < TimeoutStartSec ≤ 900 s | arithmetic | **PASS** (538 < 600 ≤ 900) |
| T10 | Model identity/residency | pre/post `/api/ps` | digest `766cd946…8cc99d8a`, 100% VRAM, ctx 65536 | exact | **PASS** |

## 3. Pre-change state (FACT, captured 21:54–21:56Z)

- `/usr/local/libexec/hx-ollama-preload` — root:root 0755, sha256 `01c2a096e5b416f33d95d25c01af30a94845877ded4e95ce21ee5aea3c9b29f2` (= M6b frozen, no drift). Behavior: `curl -fsS --retry 12 --retry-all-errors --retry-delay 5 --connect-timeout 3 --max-time 900` on `/api/generate`, then `/api/ps` name assertion.
- `/etc/systemd/system/ollama-preload.service` — root:root 0644, sha256 `28c60c7d7f955ce85c36223b08691617a383451d62fc28b05b20a05caa052299` (= M6b frozen, no drift). `TimeoutStartSec=1200`; live `TimeoutStartUSec=20min`; no drop-ins.
- `ollama.service`: active/running, `NRestarts=0`, `ExecMainStartTimestamp=Tue 2026-08-25 16:23:20 UTC`, PID 1196.
- `/api/ps`: `hx-qwen3.8-27b-64k:latest`, digest `766cd946…8cc99d8a`, size == size_vram 20,463,789,012 B (100% VRAM), ctx 65536, `expires_at` year 2318 (keep_alive=-1, Forever).
- Boot timing precedent: preload OK 51 s after start this boot (16:23:20 → 16:24:11); M7a measured boot→ready 60 s in 3/3 reboot cycles, dominated by ~50 s cold runner load of the 19.06 GiB resident set.

## 4. The two changes (and nothing else)

### 4.1 Unit — one-line diff

```diff
--- a/ollama-preload.service
+++ b/ollama-preload.service
@@ -8,7 +8,7 @@
 Type=oneshot
 ExecStart=/usr/local/libexec/hx-ollama-preload
 RemainAfterExit=yes
-TimeoutStartSec=1200
+TimeoutStartSec=600
```

Value justification: 600 s = 10× the measured 60 s worst boot→ready (M7a 3/3; 51 s this boot); it exceeds the new script worst case (538 s, §5) with 62 s slack; and it sits 300 s under the 900 s D5 recovery limit. Work-order-recommended value, inside the ≤ 900 s bound.

### 4.2 Script — bounded phases

```diff
--- a/hx-ollama-preload
+++ b/hx-ollama-preload
@@ -1,23 +1,46 @@
 #!/bin/sh
 # hx-ollama-preload — PILOT-HX1-OLLAMA-QWEN27B-001 (plan section 4.3)
 # Loads the exact pilot model with keep_alive=-1, then asserts /api/ps residency.
-# Bounded retry (12 retries x 5 s delay), hard per-request timeout (900 s).
-# On exhaustion it FAILS (alert path per handoff R-015/R-023); it never loops.
-# No credentials are embedded or required (loopback-only API).
+# Two bounded phases (WO-HX1-JOHN-PB-001, D5 conformance):
+#   Phase 1 API wait: at most 30 fast probes of /api/version
+#     (connect-timeout 2 s, max-time 5 s, sleep 2 s between probes);
+#     worst case 30*5 + 29*2 = 208 s.
+#   Phase 2 model load: ONE attempt, --max-time 300 (cold 64K load ~50 s
+#     measured, 6x margin); NO retry — a timeout must fail the unit, not
+#     extend the budget.
+#   Phase 3 assertion: one /api/ps read, --max-time 30.
+# Script worst case: 208 + 300 + 30 = 538 s, below TimeoutStartSec=600 in
+# ollama-preload.service, itself 300 s under the 900 s D5 recovery SLO.
+# On any exhaustion or failure it FAILS (alert path per handoff R-015/R-023);
+# it never loops. No credentials are embedded or required (loopback-only API).
 set -eu
 
 MODEL="hx-qwen3.8-27b-64k"
 API="http://127.0.0.1:11434"
+API_PROBES=30
 
-# Step 1: bounded load request; empty prompt only loads and pins the model.
-curl -fsS --retry 12 --retry-all-errors --retry-delay 5 \
-  --connect-timeout 3 --max-time 900 \
+# Phase 1: bounded fast probes until the API answers (no side effects).
+tries=0
+until curl -fsS --connect-timeout 2 --max-time 5 "$API/api/version" -o /dev/null 2>&1; do
+  tries=$((tries + 1))
+  if [ "$tries" -ge "$API_PROBES" ]; then
+    echo "hx-ollama-preload: FAIL - $API not ready after $API_PROBES bounded probes" >&2
+    exit 1
+  fi
+  sleep 2
+done
+
+# Phase 2: single bounded load request; empty prompt only loads and pins the model.
+if ! curl -fsS --connect-timeout 3 --max-time 300 \
   "$API/api/generate" \
   -H 'Content-Type: application/json' \
   -d "{\"model\":\"$MODEL\",\"prompt\":\"\",\"stream\":false,\"keep_alive\":-1}" \
-  -o /dev/null
+  -o /dev/null; then
+  echo "hx-ollama-preload: FAIL - single-attempt load of $MODEL failed (--max-time 300)" >&2
+  exit 1
+fi
 
-# Step 2: readiness assertion — the exact model must be resident.
+# Phase 3: readiness assertion — the exact model must be resident.
 ps_json=$(curl -fsS --connect-timeout 3 --max-time 30 "$API/api/ps")
 printf '%s' "$ps_json" | grep -q "\"name\":\"$MODEL:" || {
   echo "hx-ollama-preload: FAIL - $MODEL not resident in /api/ps after bounded load" >&2
```

Preserved exactly (diff-visible): `MODEL="hx-qwen3.8-27b-64k"`; the generate payload (`keep_alive:-1`, empty prompt, `stream:false` — no `keep_alive:0`); the `/api/ps` assertion line `grep -q "\"name\":\"$MODEL:"` (byte-identical; the alias it pins carries frozen digest `766cd946…8cc99d8a` per 29 §3); the FAIL/OK message formats and nonzero-exit semantics. Changed: retry machinery replaced by (1) bounded fast API probes and (2) a single-attempt load with `--max-time 300` and no retry-on-timeout. Probe stderr is suppressed per iteration so a slow boot cannot spam the journal; exhaustion emits one explicit FAIL line.

### 4.3 Hashes and ownership

| File | sha256 (pre) | sha256 (post) | Owner/mode |
| --- | --- | --- | --- |
| `/usr/local/libexec/hx-ollama-preload` | `01c2a096e5b416f33d95d25c01af30a94845877ded4e95ce21ee5aea3c9b29f2` | `95f174da30d38e9854e4c0e10c2a23fff8e224aecd8f633405fb89387d427cb7` | root:root 0755 (unchanged) |
| `/etc/systemd/system/ollama-preload.service` | `28c60c7d7f955ce85c36223b08691617a383451d62fc28b05b20a05caa052299` | `8ce6d9c113f42439a79a90a8f8bd55f7c90959079034610d42187184e4fa4305` | root:root 0644 (unchanged) |

Install method: `sudo -n install -o root -g root -m 0755/0644` from hash-verified candidates (remote `/tmp` copies matched local candidates before install; removed after). Then `sudo -n systemctl daemon-reload`. No other host writes.

## 5. Worst-case budget arithmetic vs 900 s

Old design: 1 + 12 attempts × `--max-time 900` + 12 × 5 s retry-delay = **11,760 s** (+ 30 s `/api/ps`) — ~9.8× its own unit timeout; systemd would SIGTERM at 1200 s, itself **300 s over** the D5 recovery SLO.

New design:

| Phase | Mechanism | Worst-case calc | Budget |
| --- | --- | --- | ---: |
| 1. API wait | 30 probes, `--connect-timeout 2 --max-time 5`, `sleep 2` between | 30×5 + 29×2 | 208 s |
| 2. Model load | single attempt, `--connect-timeout 3 --max-time 300`, no retry | 1×300 | 300 s |
| 3. `/api/ps` assertion | single read, `--connect-timeout 3 --max-time 30` | 1×30 | 30 s |
| **Script total** | | | **538 s** |
| Unit `TimeoutStartSec` | | | **600 s** (62 s slack over script) |
| **D5 recovery SLO** | | | **900 s** (300 s margin over unit; 362 s over script) |

Load-call sizing: measured cold 64K load ~50 s (M7a, 3/3 cycles; 51 s boot→ready today) → `--max-time 300` = 6× margin. A slower-than-300 s cold load now fails the unit loudly (D5 "one bounded attempt" alert path) instead of silently stretching recovery past the SLO.

## 6. Verification output (FACT, 21:59–22:00Z)

Lint (T2): ShellCheck 0.9.0 (`shellcheck_0.9.0-1_amd64.deb` from the Ubuntu noble archive via `apt download`, extracted in a volatile hxs-5 workspace, not installed — closes carried limitation F-E6 for this change): **zero findings, exit 0** on the candidate and on the pre-change script. `sh -n`, `dash -n`, `bash -n`: PASS on candidate and on the installed copy.

Effective timeout (T3), after daemon-reload:

```text
TimeoutStartUSec=10min
Result=success
ActiveState=active
```

Manual non-reboot run (T5), model resident:

```text
start: 2026-08-25T21:59:46+00:00
hx-ollama-preload: OK - hx-qwen3.8-27b-64k resident
exit=0 elapsed_ms=17
end: 2026-08-25T21:59:46+00:00
```

ollama.service undisturbed (T7): `ExecMainStartTimestamp=Tue 2026-08-25 16:23:20 UTC` pre == post; `NRestarts=0`; active/running. No restart, no reload of the service itself.

Model identity (T10): `/api/ps` post-run — same digest `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a`, size == size_vram 20,463,789,012 B, ctx 65536. `expires_at` advanced within year 2318 (keep_alive=-1 re-pin from the manual run's generate call — the same pin the boot preload performs; Forever semantics unchanged).

Journal (T8): `journalctl -u ollama-preload.service --since 21:50` — no entries (the manual run is a direct exec; its output went to the invoking session, and the next boot's run will journal normally). `journalctl -u ollama.service --since 21:50` — only the three expected 200-OK requests from the manual run (`GET /api/version` 40 µs, `POST /api/generate` 1.2 ms, `GET /api/ps` 26 µs) plus evidence polls. Kernel scan since boot: **zero Xid**; NVRM `nvAssertFailedNoLog` lines only, all at 16:23:40–58 (runner lifecycle boundaries — the carried MONITOR-ONLY class per 30 §7, not triggered by this change).

## 7. What changed / what did not change

Changed: exactly the two named files (§4.3 hashes); effective `TimeoutStartUSec` 20min → 10min; preload failure budget 11,790 s → 538 s worst case.

Not changed: `ollama.service` (no restart), no reboot, no `keep_alive:0`, model store and all frozen identities (base `22130167…`, aliases `-32k`/`-64k`/`-128k`), `hx1.conf` drop-in (`OLLAMA_CONTEXT_LENGTH=65536`), listener (loopback-only), enablement (both units enabled), `NRestarts=0`, residency (100% VRAM), swap 0 B, rick's entire plane.

## 8. Rollback (exact inverse)

1. Restore the pre-change file versions: byte-copies of both files retained in the session evidence workspace `hxs-5:~/.cache/hx-pb-work/before/` (sha256 in §4.3); the pre-change script is also fully reconstructable from the post-change content plus the §4.2 reverse diff.
2. `sudo install -o root -g root -m 0755 <before-script> /usr/local/libexec/hx-ollama-preload`; `sudo install -o root -g root -m 0644 <before-unit> /etc/systemd/system/ollama-preload.service`.
3. `sudo systemctl daemon-reload`; verify `TimeoutStartUSec=20min` and sha256 == pre values.

No other state to unwind (no service restarts, no model operations, no reboot).

## 9. Stop conditions

None triggered. Service state as expected throughout; assertion passed after the fix; zero Xid; no unexpected drift (T1 matched the M6b-frozen hashes exactly). Transient-retry budget: 0 of 1 used.

## 10. Command log (sequential, sanitized)

| Seq | Time (Z) | Host | Command (shape) | Exit | Evidence |
| ---: | --- | --- | --- | ---: | --- |
| 1 | 21:51:24 | hxs-5 | `hostname; date; whoami` | 0 | §1 |
| 2 | 21:51 | hxs-5 | ssh-info.md structure probe (line 2 field count; value REDACTED, never printed) | 0 | §1 |
| 3 | 21:51 | hxs-5 | create askpass helper (0600→0700, mktemp, `awk 'NR==2{print $3}'` at execution) | 0 | §1 |
| 4 | 21:51:51 | hxs-1 | ssh: `hostname`, `date`, `$SSH_CONNECTION`, `hostname -I`, `sudo -n true` | 0 | §1 |
| 5 | 21:53 | hxs-5 | read pilot controlling docs (plan §4.3, A01 §4.4, state log rows, 29/30) | 0 | §1 |
| 6 | 21:54 | hxs-1 | `cat` live script; `ls -l`; `sha256sum` | 0 | §3 |
| 7 | 21:54 | hxs-1 | `systemctl cat/show ollama-preload.service`; fragment sha256 | 0 | §3 |
| 8 | 21:55 | hxs-5+hxs-1 | shellcheck availability probes (both absent) | 1 | §6 note |
| 9 | 21:56 | hxs-5 | `apt download shellcheck` → `dpkg-deb -x` volatile workspace; `--version` | 0 | §6 |
| 10 | 21:56 | hxs-1 | capture pre files to hxs-5 evidence workspace; markers; `/api/ps`; `uptime -s` | 0 | §3 |
| 11 | 21:57–58 | hxs-5 | write candidates; ShellCheck + `sh/dash/bash -n`; unified diffs | 0 | §4, §6 |
| 12 | 21:58 | hxs-1 | `scp` candidates to `/tmp`; remote sha256 == local | 0 | §4.3 |
| 13 | 21:59 | hxs-1 | re-verify hostname+peer; `sudo -n install` ×2; `rm /tmp` copies; `sudo -n systemctl daemon-reload` | 0 | §4.3 |
| 14 | 21:59 | hxs-1 | post sha256/ls; `systemctl show -p TimeoutStartUSec`; syntax check installed copy | 0 | §6 |
| 15 | 21:59:46 | hxs-1 | timed `sudo -n /usr/local/libexec/hx-ollama-preload` | 0 | §6 (T5) |
| 16 | 22:00 | hxs-1 | post markers; `/api/ps`; journal excerpts; kernel Xid scan | 0 | §6 (T7/T8/T10) |

Sanitization confirmed: no secret value was printed, logged, stored, or placed on any command line; the askpass helper reads `ssh-info.md` line 2 field 3 at execution time only, and was deleted at task end along with the volatile tool workspace contents.

## 11. Validation summary

- What was tested: T1–T10 (§2) — identity, lint, effective timeout, post-install identity, manual run, failure-semantics preservation, service non-disturbance, journal/kernel cleanliness, budget arithmetic, model identity.
- Passed: 10/10. Failed: 0. Not run: none. Unexecuted: a true cold-load timing test — impossible without a reboot/model unload, both out of scope; cold behavior is bounded by `--max-time 300` + `TimeoutStartSec=600` instead of measured.
- Current Ollama state: 0.32.15, active/running since boot 16:23:20 UTC, `NRestarts=0`, loopback-only.
- Current model state: `hx-qwen3.8-27b-64k:latest` resident, digest `766cd946…8cc99d8a`, 100% VRAM, ctx 65536, keep-alive Forever.
- Endpoint/security state: unchanged (loopback-only; no credentials in either file).
- Resource state: unchanged (swap 0 B; model resident 20.46 GB VRAM).
- Rollback readiness: exact inverse recorded (§8); pre-change byte-copies and hashes retained.
- Remaining risks: none new. Carried, unchanged: F-M6-1-class boot-time API race is now absorbed by the probe loop (30 × 5 s budget vs 1 retry observed per boot in M7a); NVRM assertion class remains MONITOR-ONLY (rick's plane).
- Handoff: this deliverable goes to Carol for catalog receipt; handoff OPEN until the receipt lands in the state log.

`[TASK COMPLETE — EVIDENCE ATTACHED]`

`PASS — TASK COMPLETE`
