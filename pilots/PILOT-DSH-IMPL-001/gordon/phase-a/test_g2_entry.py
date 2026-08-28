"""Gate 2 — runtime composition and product entry paths (test plan §6).

Behavioral rows use per-test scratch DSH_HOMEs. The candidate installation
and the real home are never written by these tests.
"""

from __future__ import annotations

import json
import time

import pytest

from gordon_util import (
    blocked,
    find_session_artifacts,
    latest_request_header,
    nonce,
    read_session_log,
    run_candidate,
)

# Row ids asserted in the headless default composition. Oracle:
# packages/bundle/base/cordis.patch.yml + packages/bundle/headless/cordis.patch.yml.
HEADLESS_ROWS = [
    "timer", "hmr", "llm", "session", "typert", "typert-loader", "typert-gateway",
    "session-title", "session-title-llm", "user-questions", "agent",
    "agent-default-model", "jobs", "llm-retry", "settings", "credentials",
    "llm-pi-ai", "session-persistence-jsonl", "attachment-local",
    "session-query-sqlite", "session-projection", "session-telemetry-otel",
    "subprocess", "sandbox", "sandbox-policy", "bash-sandbox", "approval",
    "permission", "shell-env", "tool-bash", "tool-jobs", "fs-observation-policy",
    "tool-fs", "tool-fs-search", "agent-instructions", "skill",
    "skill-filesystem", "tool-skill", "commands", "command-feedback", "goal",
    "goal-round-driver", "command-goal", "plan-mode", "token-meter",
    "compaction-basic", "command-compact", "subagent", "spill-local",
    "spill-policy", "session-checkpoint-policy", "tool-result-pruner",
    "tool-todo", "tool-goal", "tools", "system-prompt", "agent-loop",
    "fs-sandbox", "llm-deepseek", "headless-runner",
]


def _dump(cfg, env, profile="headless", extra=None, rec=None):
    args = ["--profile", profile, "--dump-default-config"] + (extra or [])
    run = run_candidate(cfg, args, env_extra=env)
    if rec is not None:
        rec.commands.append(run)
    return run


def test_g2_01_launcher_help(cfg, candidate_bin, scratch_env, rec):
    """G2-01: `dsh -h` prints the launcher help and exits 0."""
    run = run_candidate(cfg, ["-h"], env_extra=scratch_env)
    rec.commands.append(run)
    text = run.stdout
    ok = run.exit_code == 0 and all(
        token in text for token in ["--profile", "--patch", "web", "plugin"]
    )
    rec.finish("PASS" if ok else "FAIL", "apps/cli/src/args.ts:64-72,121-145",
               f"exit={run.exit_code}")
    assert ok, text[-500:]


def test_g2_02_profile_required(cfg, candidate_bin, scratch_env, rec):
    """G2-02: bare `dsh` errors with the exact --profile requirement."""
    run = run_candidate(cfg, [], env_extra=scratch_env)
    rec.commands.append(run)
    ok = run.exit_code != 0 and "error: --profile <name> is required" in run.stderr
    rec.finish("PASS" if ok else "FAIL", "apps/cli/src/args.ts:140",
               f"exit={run.exit_code}; stderr={run.stderr[-300:]}")
    assert ok, run.stderr[-500:]


def test_g2_03_headless_default_composition(cfg, candidate_bin, scratch_env, rec):
    """G2-03: headless default dump carries every base+headless bundle row id."""
    run = _dump(cfg, scratch_env, rec=rec)
    rec.artifact("dump-headless-default.yml", run.stdout)
    missing = [row for row in HEADLESS_ROWS if f"id: {row}" not in run.stdout]
    ok = run.exit_code == 0 and not missing
    rec.finish("PASS" if ok else "FAIL",
               "packages/bundle/base/cordis.patch.yml + headless/cordis.patch.yml row ids",
               f"exit={run.exit_code}; missing={missing}")
    assert ok, f"missing rows: {missing}"


def test_g2_04_dump_flags_mutually_exclusive(cfg, candidate_bin, scratch_env, rec):
    """G2-04: --dump-config with --dump-default-config is a usage error."""
    run = run_candidate(
        cfg, ["--profile", "headless", "--dump-config", "--dump-default-config"],
        env_extra=scratch_env,
    )
    rec.commands.append(run)
    ok = run.exit_code != 0 and "mutually exclusive" in run.stderr
    rec.finish("PASS" if ok else "FAIL", "apps/cli/src/args.ts:89-91",
               f"exit={run.exit_code}; stderr={run.stderr[-300:]}")
    assert ok, run.stderr[-500:]


def test_g2_05_profile_auto_init(cfg, candidate_bin, scratch_home, scratch_env, rec):
    """G2-05: first headless boot initializes the profile directory."""
    run = _dump(cfg, scratch_env, rec=rec)
    profile = scratch_home / "profiles" / "headless"
    manifest_path = profile / "package.json"
    observed = {
        "dump_exit": run.exit_code,
        "package_json": manifest_path.exists(),
        "cordis_patch_yml": (profile / "cordis.patch.yml").exists(),
        "pnpm_workspace_yaml": (profile / "pnpm-workspace.yaml").exists(),
    }
    bundles = None
    if manifest_path.exists():
        bundles = (json.loads(manifest_path.read_text()).get("dsh") or {}).get("profile", {}).get("bundles")
    observed["bundles"] = bundles
    ok = (
        run.exit_code == 0
        and all(v for k, v in observed.items() if k != "bundles")
        and bundles == ["@deepseek-ai/dsh-base", "@deepseek-ai/dsh-headless"]
    )
    rec.finish("PASS" if ok else "FAIL",
               "packages/boot/app-boot/src/profile.ts:114-117,152-168 (PROFILE_TEMPLATES, initProfile)",
               json.dumps(observed))
    assert ok, observed


def test_g2_06_invalid_profile_name(cfg, candidate_bin, scratch_env, rec):
    """G2-06: traversal in a profile name is rejected."""
    run = run_candidate(cfg, ["--profile", "../x", "--dump-config"], env_extra=scratch_env)
    rec.commands.append(run)
    ok = run.exit_code != 0 and "invalid profile name" in run.stderr
    rec.finish("PASS" if ok else "FAIL",
               "packages/boot/app-boot/src/profile.ts:104-111 resolveProfileDir",
               f"exit={run.exit_code}; stderr={run.stderr[-300:]}")
    assert ok, run.stderr[-500:]


def test_g2_07_unknown_profile_named(cfg, candidate_bin, scratch_env, rec):
    """G2-07: a template-less profile names its creation path."""
    run = run_candidate(cfg, ["--profile", "nosuch", "--dump-config"], env_extra=scratch_env)
    rec.commands.append(run)
    ok = run.exit_code != 0 and "does not exist" in run.stderr and "dsh plugin --profile" in run.stderr
    rec.finish("PASS" if ok else "FAIL",
               "packages/boot/app-boot/src/profile.ts:376-384 loadProfile",
               f"exit={run.exit_code}; stderr={run.stderr[-300:]}")
    assert ok, run.stderr[-500:]


def test_g2_08_headless_app_help(cfg, candidate_bin, scratch_env, rec):
    """G2-08: the headless app prints its own --help."""
    run = run_candidate(cfg, ["--profile", "headless", "--help"], env_extra=scratch_env)
    rec.commands.append(run)
    ok = run.exit_code == 0 and "Answer one task" in run.stdout
    rec.finish("PASS" if ok else "FAIL",
               "packages/bundle/headless/src/startup.ts:40-52",
               f"exit={run.exit_code}")
    assert ok, run.stdout[-500:]


def test_g2_09_empty_task_rejected(cfg, candidate_bin, scratch_env, rec):
    """G2-09: a whitespace-only task is a usage error."""
    run = run_candidate(cfg, ["--profile", "headless", ""], env_extra=scratch_env, timeout=120)
    rec.commands.append(run)
    ok = run.exit_code != 0 and "a task is required" in run.stderr
    rec.finish("PASS" if ok else "FAIL",
               "packages/bundle/headless/src/startup.ts:58-61",
               f"exit={run.exit_code}; stderr={run.stderr[-300:]}")
    assert ok, run.stderr[-500:]


def test_g2_10_web_boot_serve_sigterm(cfg, candidate_bin, scratch_env, rec):
    """G2-10: web profile boots, binds a loopback listener, exits 0 on SIGTERM.

    Entry-path proof only. The web FRONTEND build is deliberately absent in
    Phase A (Morpheus receipt §5: build:web not run), so an early exit naming
    the missing frontend dist is BLOCKED-by-design, and the HTTP status is
    recorded observationally, never asserted."""
    import signal
    import socket
    import subprocess
    import urllib.request

    from gordon_util import base_env, candidate_argv

    port = 23_991
    env = base_env(cfg, {**scratch_env})
    argv = candidate_argv(
        cfg, ["--profile", "web", "--host", "127.0.0.1", "--port", str(port)], env
    )
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    bound = False
    http_status = "not-attempted"
    try:
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=3):
                    bound = True
                    break
            except OSError:
                if proc.poll() is not None:
                    break
                time.sleep(2)
        if bound:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5) as resp:
                    http_status = str(resp.status)
            except Exception as exc:  # recorded, not asserted (frontend is Phase B)
                http_status = f"error: {exc}"
        rec.artifact("web-boot-http.txt", f"bound={bound}\nhttp={http_status}\n")
        if proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
        try:
            _, stderr = proc.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            stderr = "TIMEOUT on SIGTERM"
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.communicate()
    observed = (
        f"bound={bound}; http={http_status}; exit={proc.returncode}; "
        f"stderr={stderr[-300:]}"
    )
    if not bound and proc.returncode not in (0, None):
        missing_frontend = any(
            token in stderr.lower() for token in ("dist", "frontend", "static")
        )
        if missing_frontend:
            rec.finish(
                "BLOCKED",
                "web-app boot requires the frontend dist, deliberately not built in "
                "Phase A (Morpheus receipt §5)",
                observed,
                note="reassigned: Phase B Gate 7 web boot with built frontend",
            )
            blocked("web frontend dist absent by Phase A boundary (build:web not run)")
    ok = bound and proc.returncode == 0
    rec.finish("PASS" if ok else "FAIL",
               "web-app/src/startup.ts:51-59; profile-boot.ts:221 (SIGTERM→0); "
               "bind is the Phase A entry-path proof (frontend content is Phase B)",
               observed)
    assert ok, observed


def test_g2_11_web_public_bind_refused(cfg, candidate_bin, scratch_env, rec):
    """G2-11: --host 0.0.0.0 is refused with the exact safety text."""
    run = run_candidate(
        cfg, ["--profile", "web", "--host", "0.0.0.0", "--port", "0"],
        env_extra=scratch_env, timeout=120,
    )
    rec.commands.append(run)
    ok = run.exit_code != 0 and "intentionally not supported yet for safety" in run.stderr
    rec.finish("PASS" if ok else "FAIL", "packages/bundle/web-app/src/startup.ts:75",
               f"exit={run.exit_code}; stderr={run.stderr[-300:]}")
    assert ok, run.stderr[-500:]


def test_g2_12_plugin_needs_pnpm_args(cfg, candidate_bin, scratch_env, rec):
    """G2-12: `dsh plugin` without pnpm arguments is a usage error."""
    run = run_candidate(cfg, ["plugin", "--profile", "headless"], env_extra=scratch_env)
    rec.commands.append(run)
    ok = run.exit_code != 0 and "plugin needs pnpm arguments" in run.stderr
    rec.finish("PASS" if ok else "FAIL", "apps/cli/src/args.ts:179-180",
               f"exit={run.exit_code}; stderr={run.stderr[-300:]}")
    assert ok, run.stderr[-500:]


def test_g2_13_telemetry_composition(cfg, candidate_bin, scratch_env, rec):
    """G2-13: the default headless composition mounts session-telemetry-otel
    with the DISABLED-default mode expression and the bounded-drain exporter
    values. The launcher disable patch is boot-time only (profile-boot.ts),
    so the switch leg lives in G4-09's runtime drill."""
    run = _dump(cfg, scratch_env, rec=rec)
    rec.artifact("dump-telemetry.yml", run.stdout)
    row_present = "id: session-telemetry-otel" in run.stdout
    mode_expr = "DSH_TELEMETRY_MODE" in run.stdout
    bounded = "shutdownTimeoutMillis" in run.stdout
    observed = f"row={row_present}; mode_expr={mode_expr}; bounded_drain_config={bounded}"
    ok = run.exit_code == 0 and row_present and mode_expr and bounded
    rec.finish("PASS" if ok else "FAIL",
               "base bundle rows 129-161 (telemetry default-off + bounded drain); "
               "dump-config.ts (boot-free dump cannot show the launcher telemetry patch)",
               observed,
               note="AVAILABLE_DISABLED by default; switch runtime proof in G4-09")
    assert ok, observed


def test_g2_14_dsh_home_override(cfg, candidate_bin, scratch_home, scratch_env, rec):
    """G2-14: DSH_HOME override routes all artifacts into the scratch home."""
    from pathlib import Path as _P

    run = _dump(cfg, scratch_env, rec=rec)
    scratch_profiles = (scratch_home / "profiles").exists()
    real_home = _P(cfg.values["GORDON_REAL_HOME"])
    observed = (
        f"dump_exit={run.exit_code}; scratch_profiles={scratch_profiles}; "
        f"real_home={real_home} drift guarded by G0-07 fingerprint"
    )
    ok = run.exit_code == 0 and scratch_profiles
    rec.finish("PASS" if ok else "FAIL",
               "packages/util/home-paths/src/index.ts:87-91 resolveDshHome",
               observed)
    assert ok, observed


def test_g2_15_system_prompt_assembly(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G2-15: the headless persona reaches the model-visible request header.

    Requires routing (Gate 3 seam). Model-cooperation class: none (deterministic
    given a completed routed run)."""
    from test_g3_providers import seam_fixture_for

    patch = seam_fixture_for(cfg, scratch_home, model_key="qwen", max_retries=0)
    task = f"Reply with exactly: GORDON-G215-{nonce()}"
    run = run_candidate(
        cfg,
        ["--profile", "headless", "--patch", str(patch), task],
        env_extra=scratch_env, cwd=str(workspace), timeout=300,
    )
    rec.commands.append(run)
    if run.exit_code != 0:
        rec.finish("BLOCKED", "routed run required (Gate 3 seam + key)",
                   f"exit={run.exit_code}; stderr={run.stderr[-300:]}",
                   note="rerun after G3 routing is green")
        blocked("routed run failed; see G3 dispositions first")
    artifacts = find_session_artifacts(scratch_home, cfg)
    if not artifacts:
        rec.finish("FAIL", "session artifact after routed run", "no artifact found")
        pytest.fail("no session artifact under scratch home")
    log = read_session_log(cfg, artifacts[-1])
    rec.artifact("session-log.json", json.dumps(log)[:200000])
    header = latest_request_header(log["records"])
    persona_found = False
    if header and isinstance(header.get("data"), dict):
        system = header["data"].get("system") or ""
        persona_found = "coding agent" in system and str(workspace) in system
    ok = persona_found
    rec.finish("PASS" if ok else "FAIL",
               "headless bundle persona (cordis.patch.yml); model-visible ⟺ logged (repo AGENTS.md)",
               f"persona_in_request_header={persona_found}")
    assert ok, "persona not found in request/header system prompt"
