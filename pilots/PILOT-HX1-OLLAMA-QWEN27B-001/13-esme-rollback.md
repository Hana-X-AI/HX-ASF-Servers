# Esme (john) — M4 Rollback Guide (hxs-1)

| Field | Value |
| --- | --- |
| Document | `13-esme-rollback.md` — rollback per plan §10.2 |
| Task | WO-HX1-JOHN-M4-001 (`PILOT-HX1-OLLAMA-QWEN27B-001`, M4) |
| Author | john / Esme (session `john-m4-20260825-01`), 2026-08-25 (UTC) |
| Host | `hxs-1` (192.168.50.200), Ubuntu 24.04.4 LTS, kernel 7.0.0-28-generic |
| Companion evidence | `12-esme-m4-install-evidence.md` (baseline §3, configs §6, hashes §11) |
| Pre-change state | **No Ollama installed** (FACT, captured 2026-08-25T00:42:58Z: no binary, package, user, unit, listener, or `/usr/share/ollama`) |

## 1. Rollback triggers (plan §10.2)

Roll back the **smallest affected layer** when any of these is confirmed: unresolved GPU errors,
boot failure attributable to these units, repeated OOM, security regression (any bind beyond
`127.0.0.1:11434`), model-integrity mismatch (digest drift from §4), unacceptable quality
regression, or inability to recover within the D5 budget (detection ≤2 min, recovery ≤15 min,
one bounded attempt). Do not modify governance or evidence to make the runtime appear compliant.

## 2. Preserved pre-change artifacts (plan §10.2 inventory)

| Item | Pre-change value | Where evidenced |
| --- | --- | --- |
| Prior Ollama version/method | none installed | `12-…evidence.md` §3 |
| `systemctl cat ollama` + drop-ins | unit not found; no drop-in dir | `12-…evidence.md` §3 |
| Service user/group | `ollama` absent | `12-…evidence.md` §3 |
| Model list/digests | none | `/api/tags` empty 00:46:01Z |
| Model storage path/free capacity | `/usr/share/ollama` absent; root 3.4 T free | `12-…evidence.md` §3 |
| Firewall/proxy rules | none touched (ufw inactive, nft empty — rick §6.5) | not modified by M4 |
| Driver/kernel state | 580.173.02 / 7.0.0-28 — rick's plane, untouched | `07`, `08` handoff |
| Configuration hashes | all M4 artifacts hashed at creation | `12-…evidence.md` §11 |

No reboot is required for any rollback step below. The OS plane (including rick's sleep-target
masks) is out of scope and must not be touched by this rollback.

## 3. Layered inverse procedures

Execute as `hxsa` with sudo. Each layer is independent; stop at the layer that resolves the trigger.

### Layer A — preload only (residency/boot-preload regression)

```bash
sudo systemctl stop ollama-preload.service
sudo systemctl disable ollama-preload.service
sudo rm /etc/systemd/system/ollama-preload.service
sudo rm /usr/local/libexec/hx-ollama-preload
sudo systemctl daemon-reload
```

Verify: `systemctl status ollama-preload.service` → not found; `ollama.service` still active.
Effect: model stays loaded until eviction; no boot preload. Reversal: reinstall per `12-…evidence.md` §4.7.

### Layer B — pilot alias only (model-identity/quality regression on the alias)

```bash
ollama rm hx-qwen3.8-27b
```

Verify: `ollama list` → only `qwen3.8:27b`; `/api/ps` empties after runner eviction.
Base model `qwen3.8:27b` (digest `22130167c4c2…`) is untouched. Reversal: `ollama create` from the
hashed Modelfile (`12-…evidence.md` §4.5, sha256 `dac63d7c…`).

### Layer C — hx1 drop-in only (configuration regression; revert to upstream defaults)

```bash
sudo rm /etc/systemd/system/ollama.service.d/hx1.conf
sudo rmdir /etc/systemd/system/ollama.service.d
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Verify: `systemctl show ollama -p Environment` → `PATH` only; journal startup line shows
`OLLAMA_KEEP_ALIVE:5m0s`, `OLLAMA_NO_CLOUD:false`, empty `CUDA_VISIBLE_DEVICES`; listener still
loopback. NOTE (FACT): upstream default bind is also `127.0.0.1:11434` — loopback posture survives
this layer. Reversal: reinstall `hx1.conf` (sha256 `36af1c42…`) + daemon-reload + restart.

### Layer D — full Ollama removal (return to pre-M4 state)

```bash
# 1. Stop and disable services
sudo systemctl stop ollama-preload.service ollama.service
sudo systemctl disable ollama-preload.service ollama.service

# 2. Remove pilot and upstream units, drop-in, preload script
sudo rm /etc/systemd/system/ollama-preload.service
sudo rm /etc/systemd/system/ollama.service.d/hx1.conf
sudo rmdir /etc/systemd/system/ollama.service.d 2>/dev/null || true
sudo rm /etc/systemd/system/ollama.service
sudo rm /usr/local/libexec/hx-ollama-preload
sudo systemctl daemon-reload
sudo systemctl reset-failed 2>/dev/null || true

# 3. Remove binary and libraries (installer placed them under /usr/local)
sudo rm /usr/local/bin/ollama
sudo rm -rf /usr/local/lib/ollama

# 4. Remove service account and group memberships the installer created
sudo gpasswd -d hxsa ollama        # installer added hxsa to ollama
sudo userdel ollama                # removes ollama login; group ollama removed with it if empty

# 5. Model data — SEPARATE APPROVAL REQUIRED (profile §14: no model-data deletion
#    without explicit approval; D1 storage plane). Only on Kimi-K3/owner instruction:
# sudo rm -rf /usr/share/ollama
```

Verify (must match the 00:42:58Z baseline):

```bash
command -v ollama || echo NO_OLLAMA_BIN
systemctl status ollama ollama-preload --no-pager 2>&1 | head -4   # not found
id ollama 2>&1                                                     # no such user
ls -ld /usr/share/ollama 2>&1                                      # absent (only after approved step 5)
ss -lnt | grep 11434 || echo NO_11434_LISTENER
ls /usr/local/lib/ollama 2>&1                                      # absent
```

Effect: **scoped 2026-08-25** — steps 1–4 remove the runtime only; the model store
persists on disk, so steps 1–4 alone do NOT restore the M1/M2 baseline. That claim
(`07-rick-os-readiness.md` §6 + sleep masks) holds only after the separately-approved
step 5, which requires: explicit Kimi-K3/owner instruction, pre-deletion capture of
`ollama list` + digests (model-integrity provenance), and post-deletion verification
(`/usr/share/ollama` absent, capacity reclaimed). GPUs remain at 0 MiB used;
driver/kernel untouched; uptime preserved.

## 4. Frozen identities to restore against

| Artifact | Identity |
| --- | --- |
| Installer | sha256 `25f64b810b947145095956533e1bdf56eacea2673c55a7e586be4515fc882c9f` (== TKV `scripts/install.sh`) |
| Ollama | 0.32.15 (binary == server) |
| Base model | `qwen3.8:27b` digest `22130167c4c20e20c7b71454612966ca8e8171e9b3cc8ab6ce8aa6cbfec79643`, Q4_K_M, 17,741,872,154 B |
| Alias | `hx-qwen3.8-27b:latest` digest `23508b9c243979f6538b2e71c69ccbcd4f905d5a6313e64b6b108069a15185a8` |
| Modelfile | sha256 `dac63d7c3e096585c8b65261bbf139201e384280e40369536963d8439db1d1df` (plan §6.5 verbatim) |
| Drop-in | sha256 `36af1c4212d4797eaa455013ce02f853d3c913554c3b42bde4e6f52783460f38` |
| Preload script | sha256 `79571d639b6acee53d08692b1d1538d506a145784236e2413f681d1a7eb7262a` |
| Preload unit | sha256 `28c60c7d7f955ce85c36223b08691617a383451d62fc28b05b20a05caa052299` |

## 5. Recovery-path operational notes (from M4 evidence)

- Use `systemctl restart ollama-preload.service` (not `start`) to re-run the preload when the unit
  is `active (exited)` — `RemainAfterExit=yes` makes `start` a no-op (evidence F-E4).
- After any `ollama.service` restart, allow ~45–60 s for GPU discovery before judging API readiness
  (observed ≈47 s restart→API-ready; F-E1/F-E2).
- One bounded recovery attempt per incident (D5): restart `ollama.service` once, then
  `systemctl restart ollama-preload.service`, assert `/api/ps`; if it fails, stop and escalate —
  no retry loop (plan §4.5, R-022).
- If the NVRM assertions of evidence F-E3 recur during rollback or recovery, stop and hand to rick
  (driver plane) before further GPU work.

Signed: **john / Esme** — Expert Ollama Engineer
Session `john-m4-20260825-01` · WO-HX1-JOHN-M4-001 · 2026-08-25 (UTC)
