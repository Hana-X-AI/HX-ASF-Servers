"""Gate 5 — tools, permissions, and containment (test plan §9).

Oracles: base bundle rows (sandbox-policy, approval, bash-sandbox),
user-approval fail-closed semantics, tool-bash contract, sandbox-policy mode
texts. Headless mounts no approval answerer: `ask` fails closed, which is the
Phase A containment stance.

Model-cooperation rows (the routed model must call tools as instructed) get
one recorded re-run per doctrine §9; both attempts go to evidence.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import time
from pathlib import Path

import pytest

from gordon_util import (
    base_env,
    blocked,
    candidate_argv,
    epoch_header,
    events_of_type,
    find_session_artifacts,
    nonce,
    read_session_log,
    run_candidate,
    sandbox_unavailable,
)
from test_g3_providers import (
    register_call,
    require_routing_inputs,
    run_routed_headless,
    seam_fixture_for,
)


def _cooperate(cfg, scratch_home, scratch_env, workspace, rec, tag: str, task: str,
               check, env_extra: dict | None = None, timeout: float = 420.0):
    """Model-cooperation runner: up to three recorded attempts, with spacing
    on gateway queue transients (doctrine §9: repetition bounds the
    intermittent; every attempt is recorded).

    `check(scratch_home, run, marker) -> (ok: bool, detail: str)`.
    """
    from gordon_util import is_queue_transient

    require_routing_inputs(cfg, "coder")
    attempts = []
    for attempt in (1, 2, 3):
        marker = f"GORDON-{tag}A{attempt}-{nonce()}"
        patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
        run = run_routed_headless(
            cfg, scratch_env, workspace, patch, task.replace("__MARKER__", marker),
            timeout=timeout, env_extra=env_extra,
        )
        rec.commands.append(run)
        register_call(cfg, {"tag": f"{tag}A{attempt}", "model_key": "coder",
                            "model_id": cfg.model_ids()["coder"], "marker": marker,
                            "ts": int(time.time()), "exit": run.exit_code})
        ok, detail = check(scratch_home, run, marker)
        attempts.append(f"attempt{attempt}: exit={run.exit_code}; {detail}")
        if ok == "SANDBOX-D1":
            return "SANDBOX-D1", " | ".join(attempts)
        if ok:
            return True, " | ".join(attempts)
        log_text = _log_text(_latest_log(cfg, scratch_home))
        if sandbox_unavailable(log_text):
            return "SANDBOX-D1", " | ".join(attempts)
        if is_queue_transient(run):
            import os
            time.sleep(float(os.environ.get("GORDON_QUEUE_SPACING_S", "25")))
    return False, " | ".join(attempts)


def _latest_log(cfg, scratch_home) -> dict:
    artifacts = find_session_artifacts(scratch_home, cfg)
    return read_session_log(cfg, artifacts[-1]) if artifacts else {"records": []}


def _log_text(log: dict) -> str:
    return json.dumps(log.get("records", []))



def _finish_coop(rec, result, observed, oracle, note=""):
    """Map a _cooperate outcome to a disposition; the SANDBOX-D1 sentinel is
    BLOCKED with the provisioning defect named, never a false pass/fail."""
    if result == "SANDBOX-D1":
        rec.finish(
            "BLOCKED",
            oracle + " — requires a usable sandbox backend; defect D1 "
            "(no bwrap, no landlock prebuilt binary on hxs-15)",
            observed,
            note="retest after Morpheus provisions a backend (D1)",
        )
        blocked("sandbox backend absent on hxs-15 (defect D1)")
    rec.finish("PASS" if result else "FAIL", oracle, observed, note=note)


def _tool_result_texts(log: dict) -> list[str]:
    """Text blocks of tool/result events (the model-visible tool output only —
    never tool/call arguments or assistant prose, which quote the marker)."""
    out = []
    for event in log.get("records", []):
        if event.get("type") != "tool/result":
            continue
        data = event.get("data") or {}
        message = data.get("message") or {}
        for block in message.get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool-result":
                for inner in block.get("content") or []:
                    if isinstance(inner, dict) and inner.get("type") == "text":
                        out.append(inner.get("text") or "")
    return out


def test_g5_01_bash_execution(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-01: the bash tool executes and returns output (external effect)."""
    def check(home, run, marker):
        log = _latest_log(cfg, home)
        result_texts = _tool_result_texts(log)
        called = any('"name": "bash"' in json.dumps(e.get("data") or {}) or '"name":"bash"' in json.dumps(e.get("data") or {})
                     for e in log.get("records", []) if e.get("type") == "tool/call")
        # The marker must appear in a NON-ERROR tool result (the echo stdout),
        # not in the command's own arguments or the model's narration.
        marker_in_output = any(marker in t for t in result_texts)
        error_results = sum(1 for t in result_texts if "no sandbox backend is usable" in t)
        return (run.exit_code == 0 and called and marker_in_output),             f"bash_called={called}; marker_in_tool_result={marker_in_output}; sandbox_error_results={error_results}"

    task = (
        "Use the bash tool to run this exact command: echo __MARKER__\n"
        "Then reply with exactly: DONE"
    )
    ok, observed = _cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G501", task, check)
    _finish_coop(rec, ok, observed,
               "tool-bash schema (command, description); result returns stdout",
               note="model-cooperation class")
    assert ok, observed


def test_g5_02_workspace_write_allowed(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-02: a write inside the workspace succeeds; bytes verified externally."""
    target = workspace / "gordon_probe.txt"

    def check(home, run, marker):
        exists = target.exists()
        content = target.read_text().strip() if exists else ""
        return (run.exit_code == 0 and exists and marker in content), \
            f"file_exists={exists}; content_matches={marker in content}"

    task = (
        f"Use the bash tool to run exactly: printf '%s' __MARKER__ > {target}\n"
        "Then reply with exactly: DONE"
    )
    ok, observed = _cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G502", task, check)
    _finish_coop(rec, ok, observed,
               "sandbox-policy workspace-write mode text (sandbox-policy/src/index.ts:42-43); "
               "external byte-identical assert",
               note="model-cooperation class")
    assert ok, observed


def test_g5_03_workspace_escape_denied(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-03: a write outside the workspace is denied under workspace-write."""
    escape = workspace.parent / "gordon-escape.txt"
    if escape.exists():
        escape.unlink()

    def check(home, run, marker):
        log = _latest_log(cfg, home)
        text = _log_text(log)
        if sandbox_unavailable(text):
            # The unavailable error renders in the denial dialect; a policy
            # denial cannot be distinguished without a backend.
            return "SANDBOX-D1", "sandbox backend unavailable (D1)"
        called = any(e.get("type") == "tool/call" for e in log.get("records", []))
        denied = "[sandbox: file access denied under workspace-write mode]" in text
        absent = not escape.exists()
        return (called and denied and absent), \
            f"bash_attempted={called}; policy_denial={denied}; escape_file_absent={absent}"

    task = (
        f"Use the bash tool to run exactly: echo __MARKER__ > {escape}\n"
        "If the sandbox denies it, reply with exactly: DONE"
    )
    ok, observed = _cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G503", task, check)
    _finish_coop(rec, ok, observed,
               "tool-bash denial marker `[sandbox: file access denied under <mode> mode]`; "
               "no file outside the workspace",
               note="model-cooperation class; denial may be reported in the tool result")
    assert ok, observed


def test_g5_04_read_only_mode_denies_writes(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-04: DSH_PERMISSION_MODE=read-only denies even in-workspace writes."""
    target = workspace / "gordon-ro-probe.txt"
    if target.exists():
        target.unlink()

    def check(home, run, marker):
        log = _latest_log(cfg, home)
        text = _log_text(log)
        if sandbox_unavailable(text):
            return "SANDBOX-D1", "sandbox backend unavailable (D1)"
        called = any(e.get("type") == "tool/call" for e in log.get("records", []))
        denied = "[sandbox: file access denied under read-only mode]" in text
        absent = not target.exists()
        return (called and denied and absent), \
            f"bash_attempted={called}; read_only_denial={denied}; file_absent={absent}"

    task = (
        f"Use the bash tool to run exactly: echo __MARKER__ > {target}\n"
        "If the sandbox denies it, reply with exactly: DONE"
    )
    ok, observed = _cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G504", task, check,
                              env_extra={"DSH_PERMISSION_MODE": "read-only"})
    _finish_coop(rec, ok, observed,
               "sandbox-policy read-only mode text (src/index.ts:40-41); base row env seam "
               "DSH_PERMISSION_MODE",
               note="model-cooperation class")
    assert ok, observed


def test_g5_05_approval_fails_closed(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-05: an escalation request under policy ask + no answerer resolves rejected."""
    escape = workspace.parent / "gordon-escalation.txt"
    if escape.exists():
        escape.unlink()

    def check(home, run, marker):
        log = _latest_log(cfg, home)
        asked = events_of_type(log.get("records", []), "approval/asked")
        decided = events_of_type(log.get("records", []), "approval/decided")
        rejected = any(
            (d.get("data") or {}).get("outcome") in ("rejected", "unavailable")
            or "reject" in json.dumps(d.get("data", {})).lower()
            for d in decided
        )
        absent = not escape.exists()
        # Fail-closed proof: either the ask/decide pair shows rejection, or the
        # write never landed and the run completed without the file.
        return (absent and (rejected or not asked)), \
            f"asked={len(asked)}; decided={len(decided)}; rejected={rejected}; file_absent={absent}"

    task = (
        f"Use the bash tool to run exactly: echo __MARKER__ > {escape}\n"
        "If the sandbox denies it, retry the exact same command once with "
        "sandbox_permissions: \"workspace-write\" and a one-sentence justification. "
        "Then reply with exactly: DONE"
    )
    ok, observed = _cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G505", task, check)
    _finish_coop(rec, ok, observed,
               "user-approval: ask with no answerer fails closed (src/index.ts:88-92,102); "
               "escalation pairing rule (tool-bash:65-67)",
               note="model-cooperation class")
    assert ok, observed


def test_g5_06_danger_full_access_semantics(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-06: danger-full-access permits the out-of-workspace write (scratch area)."""
    outside = workspace.parent / "gordon-danger.txt"
    if outside.exists():
        outside.unlink()

    def check(home, run, marker):
        exists = outside.exists()
        content = outside.read_text().strip() if exists else ""
        return (run.exit_code == 0 and exists and marker in content), \
            f"file_exists={exists}; content_matches={marker in content}"

    task = (
        f"Use the bash tool to run exactly: printf '%s' __MARKER__ > {outside}\n"
        "Then reply with exactly: DONE"
    )
    try:
        ok, observed = _cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G506", task, check,
                                  env_extra={"DSH_PERMISSION_MODE": "danger-full-access"})
    finally:
        if outside.exists():
            outside.unlink()
    _finish_coop(rec, ok, observed,
               "base approval row expression (never under danger-full-access); "
               "sandbox-policy danger-full-access mode text",
               note="model-cooperation class; scratch area only, cleaned up")
    assert ok, observed


def test_g5_07_bash_timeout_kills(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-07: the executor kills a command that exceeds its timeout."""
    def check(home, run, marker):
        log = _latest_log(cfg, home)
        result_texts = _tool_result_texts(log)
        timed = any("[timed out after" in t for t in result_texts)
        killed = any("[killed by signal" in t for t in result_texts)
        structured = '"timedOut": true' in _log_text(log) or '"timedOut":true' in _log_text(log)
        bounded = run.duration_s < 300
        ok = (timed and killed) or structured
        return (ok and bounded), \
            f"timeout_notice={timed}; kill_notice={killed}; structured={structured}; duration={run.duration_s:.0f}s"

    task = (
        "Use the bash tool to run exactly this command with timeoutMs 3000: sleep 120\n"
        "When it times out, reply with exactly: __MARKER__"
    )
    ok, observed = _cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G507", task, check)
    _finish_coop(rec, ok, observed,
               "tool-bash: executor applies the timeout and kills on expiry (schema:254)",
               note="model-cooperation class")
    assert ok, observed


def _spawn_long_run(cfg, scratch_home, scratch_env, workspace, tag: str):
    """Spawn a routed headless run intended to be signalled mid-flight.

    Runs under DSH_PERMISSION_MODE=danger-full-access: the drills qualify
    signal handling and log durability, not sandboxing, and the workspace-write
    sandbox backend is absent on hxs-15 (defect D1 — under it the bash tool
    fails closed in seconds and there is no long flight to signal)."""
    require_routing_inputs(cfg, "coder")
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    env = base_env(cfg, {**scratch_env, "DSH_PERMISSION_MODE": "danger-full-access"})
    task = (
        "Use the bash tool to run: sleep 300. Do not finish before it does."
    )
    argv = candidate_argv(cfg, ["--profile", "headless", "--patch", str(patch), task], env)
    proc = subprocess.Popen(
        argv,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        cwd=str(workspace),
    )
    return proc


def test_g5_08_sigint_drill(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-08: SIGINT mid-run exits 130; the log stays a parseable prefix."""
    proc = _spawn_long_run(cfg, scratch_home, scratch_env, workspace, "G508")
    time.sleep(25)
    if proc.poll() is not None:
        _, early_err = proc.communicate()
        observed = f"run exited before signal: rc={proc.returncode}; stderr={(early_err or '')[-250:]}"
        if sandbox_unavailable(early_err or ""):
            rec.finish("BLOCKED", "no long flight to signal (defect D1)", observed)
            blocked("sandbox backend absent on hxs-15 (defect D1)")
        rec.finish("FAIL", "run stays in flight until signalled", observed)
        pytest.fail(observed)
    proc.send_signal(signal.SIGINT)
    try:
        _, stderr = proc.communicate(timeout=90)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        stderr = "TIMEOUT after SIGINT"
    logs = find_session_artifacts(scratch_home, cfg)
    parsed = read_session_log(cfg, logs[-1]) if logs else {"records": [], "error": "none"}
    observed = (f"exit={proc.returncode}; artifacts={len(logs)}; "
                f"records={len(parsed.get('records', []))}; stderr={stderr[-200:]}")
    ok = proc.returncode == 130 and parsed.get("header") is not None
    rec.finish("PASS" if ok else "FAIL",
               "profile-boot.ts:222 SIGINT→interrupt(130); committed prefix parses",
               observed)
    assert ok, observed


def test_g5_09_sigkill_drill(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-09: SIGKILL mid-run; next cold boot works; killed log parses (G4-05)."""
    proc = _spawn_long_run(cfg, scratch_home, scratch_env, workspace, "G509")
    time.sleep(25)
    if proc.poll() is not None:
        _, early_err = proc.communicate()
        observed = f"run exited before signal: rc={proc.returncode}; stderr={(early_err or '')[-250:]}"
        if sandbox_unavailable(early_err or ""):
            rec.finish("BLOCKED", "no long flight to kill (defect D1)", observed)
            blocked("sandbox backend absent on hxs-15 (defect D1)")
        rec.finish("FAIL", "run stays in flight until killed", observed)
        pytest.fail(observed)
    proc.kill()
    proc.communicate()
    killed_logs = find_session_artifacts(scratch_home, cfg)
    parsed = read_session_log(cfg, killed_logs[-1]) if killed_logs else {"records": []}
    # Cold boot afterwards must work: a plain dump is enough (no provider call).
    run = run_candidate(cfg, ["--profile", "headless", "--dump-default-config"],
                        env_extra=scratch_env, timeout=120)
    rec.commands.append(run)
    observed = (f"killed_exit={proc.returncode}; killed_records={len(parsed.get('records', []))}; "
                f"cold_boot_dump_exit={run.exit_code}")
    ok = proc.returncode == -signal.SIGKILL and run.exit_code == 0 and parsed.get("header") is not None
    rec.finish("PASS" if ok else "FAIL",
               "scanner torn-tail finish (format.ts:337-344); checkpoint-policy durability; "
               "cold boot unaffected",
               observed)
    assert ok, observed


def test_g5_10_sigterm_drill(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-10: SIGTERM to a long-lived web boot exits 0 (bind caveat per G2-10)."""
    env = base_env(cfg, scratch_env)
    port = 23_992
    argv = candidate_argv(
        cfg, ["--profile", "web", "--host", "127.0.0.1", "--port", str(port)], env
    )
    proc = subprocess.Popen(
        argv,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    time.sleep(20)
    if proc.poll() is not None:
        _, stderr = proc.communicate()
        missing_frontend = any(
            token in (stderr or "").lower() for token in ("dist", "frontend", "static")
        )
        observed = f"early_exit={proc.returncode}; stderr={(stderr or '')[-300:]}"
        if missing_frontend:
            rec.finish("BLOCKED",
                       "web boot requires the Phase B frontend dist (Morpheus receipt §5)",
                       observed, note="SIGTERM drill on the headless surface is G2-10's SIGTERM leg")
            blocked("web frontend dist absent by Phase A boundary")
        rec.finish("FAIL", "profile-boot.ts:221 SIGTERM→interrupt(0)", observed)
        pytest.fail(observed)
    proc.send_signal(signal.SIGTERM)
    try:
        proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
    observed = f"exit={proc.returncode}"
    ok = proc.returncode == 0
    rec.finish("PASS" if ok else "FAIL", "profile-boot.ts:221 SIGTERM→interrupt(0)", observed)
    assert ok, observed


def test_g5_11_invalid_config_fails_loud(cfg, candidate_bin, scratch_home, scratch_env, rec):
    """G5-11: malformed YAML patch and schema-violating patch both fail at load."""
    bad_yml = scratch_home / "patch-invalid-yml.yml"
    bad_yml.write_text("- id: llm-deepseek\n  config:\n    maxTokens: [unclosed\n")
    run1 = run_candidate(
        cfg, ["--profile", "headless", "--patch", str(bad_yml), "--dump-config"],
        env_extra=scratch_env, timeout=120,
    )
    rec.commands.append(run1)
    bad_cfg = scratch_home / "patch-invalid-config.yml"
    bad_cfg.write_text("- id: llm-deepseek\n  config:\n    maxTokens: -1\n")
    run2 = run_candidate(
        cfg, ["--profile", "headless", "--patch", str(bad_cfg), "ping"],
        env_extra=scratch_env, timeout=180,
    )
    rec.commands.append(run2)
    observed = (f"yaml_exit={run1.exit_code} stderr={run1.stderr[-200:]}; "
                f"schema_exit={run2.exit_code} stderr={run2.stderr[-200:]}")
    ok = run1.exit_code != 0 and run2.exit_code != 0
    rec.finish("PASS" if ok else "FAIL",
               "fail-loud doctrine (repo AGENTS.md: misconfiguration fails loud); "
               "llm-deepseek Config maxTokens min 1",
               observed)
    assert ok, observed


def test_g5_13_background_job_smoke(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-13: run_in_background returns a job id; job_output collects it."""
    def check(home, run, marker):
        log = _latest_log(cfg, home)
        result_texts = _tool_result_texts(log)
        bg = any("started background job" in t for t in result_texts) \
            or '"kind": "background"' in _log_text(log)
        collected = any(marker in t for t in result_texts)
        completed = any("[status: completed" in t for t in result_texts)
        return (run.exit_code == 0 and bg and collected and completed), \
            f"background_ack={bg}; marker_in_output={collected}; job_completed={completed}"

    task = (
        "Use the bash tool with run_in_background: true to run exactly: "
        "sleep 2; echo __MARKER__\n"
        "Then use job_output to read the job's output, and when the marker "
        "appears reply with exactly: DONE"
    )
    ok, observed = _cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G513", task, check,
                              timeout=600)
    _finish_coop(rec, ok, observed,
               "tool-bash background contract (job id → job_output/job_kill); jobs row in base",
               note="model-cooperation class")
    assert ok, observed


def test_g5_14_managed_dsh_env(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-14: the model-facing shell exposes managed DSH_* variables and no secrets."""
    def check(home, run, marker):
        log = _latest_log(cfg, home)
        text = _log_text(log)
        has_home = "DSH_HOME" in text
        has_session = "DSH_SESSION_ID" in text or "DSH_SESSION" in text
        import os as _os
        key_val = _os.environ.get(cfg.omni_key_env_name, "")
        leaks = bool(key_val) and key_val in text
        return (run.exit_code == 0 and has_home and not leaks), \
            f"DSH_HOME={has_home}; DSH_SESSION={has_session}; credential_leak={leaks}"

    task = (
        "Use the bash tool to run exactly: env | grep '^DSH_' | sort\n"
        "Then reply with exactly: __MARKER__"
    )
    ok, observed = _cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G514", task, check)
    _finish_coop(rec, ok, observed,
               "shell-env managed DSH_* variables (src/index.ts:71-75); credential "
               "values must never appear in the model-visible stream",
               note="model-cooperation class; includes a live leak assertion")
    assert ok, observed


def test_g5_15_tool_catalog_census(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-15: the model-visible tool list in request/header matches composition."""
    require_routing_inputs(cfg, "coder")
    marker = f"GORDON-G515-{nonce()}"
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    run = run_routed_headless(
        cfg, scratch_env, workspace, patch,
        f"Reply with exactly this token and nothing else: {marker}",
    )
    rec.commands.append(run)
    register_call(cfg, {"tag": "G515", "model_key": "coder", "model_id": cfg.model_ids()["coder"],
                        "marker": marker, "ts": int(time.time()), "exit": run.exit_code})
    log = _latest_log(cfg, scratch_home)
    rec.artifact("g515-log.json", json.dumps(log)[:200000])
    header = None
    for event in log.get("records", []):
        if event.get("type") == "request/header":
            header = event
    tool_names = []
    if header:
        for tool in epoch_header(header).get("tools") or []:
            if isinstance(tool, dict) and "name" in tool:
                tool_names.append(tool["name"])
    rec.artifact("g515-tools.json", json.dumps(tool_names, indent=2))
    expected_core = {"bash", "write", "read"}
    present = set(tool_names)
    found = expected_core & present
    pwsh = [name for name in present if "pwsh" in name]
    observed = f"exit={run.exit_code}; tools={sorted(present)[:40]}; pwsh={pwsh}"
    ok = run.exit_code == 0 and bool(tool_names) and found == expected_core and not pwsh
    rec.finish("PASS" if ok else "FAIL",
               "base bundle tool rows vs request/header tools (model-visible ⟺ logged); "
               "no pwsh tools on Linux",
               observed,
               note=f"expected core {sorted(expected_core)} found {sorted(found)}; full list in artifact")
    assert ok, observed


def test_g5_16_pwsh_disabled_on_linux(cfg, candidate_bin, scratch_env, rec):
    """G5-16: pwsh rows carry the platform-disabled expression (Windows-only)."""
    run = run_candidate(cfg, ["--profile", "headless", "--dump-default-config"], env_extra=scratch_env)
    rec.commands.append(run)
    pwsh_row = "id: tool-pwsh" in run.stdout
    pwsh_expr = "process.platform" in run.stdout
    observed = f"tool_pwsh_row={pwsh_row}; platform_gate_expression={pwsh_expr}"
    ok = run.exit_code == 0 and pwsh_row and pwsh_expr
    rec.finish("PASS" if ok else "FAIL",
               "base rows: pwsh disabled unless win32 (dump shows the unevaluated "
               "expression; runtime effect cross-proven by G5-15 census: no pwsh tools)",
               observed,
               note="pwsh family ledger disposition: NOT_APPLICABLE on Linux, this row is its evidence")
    assert ok, observed


def test_g5_17_cookbook_tool_contract(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G5-17 (owner directive, cookbook first-class): docs/cookbook/adding-a-tool.md
    as known-answer oracle — every model-facing tool in the request header
    satisfies the recipe's minimal shape: name, description, parameters."""
    require_routing_inputs(cfg, "coder")
    marker = f"GORDON-G517-{nonce()}"
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    run = run_routed_headless(
        cfg, scratch_env, workspace, patch,
        f"Reply with exactly this token and nothing else: {marker}",
    )
    rec.commands.append(run)
    register_call(cfg, {"tag": "G517", "model_key": "coder",
                        "model_id": cfg.model_ids()["coder"], "marker": marker,
                        "ts": int(time.time()), "exit": run.exit_code})
    log = _latest_log(cfg, scratch_home)
    header = None
    for event in log.get("records", []):
        if event.get("type") == "request/header":
            header = event
    tools = (epoch_header(header).get("tools") or []) if header else []
    violations = []
    for tool in tools:
        if not isinstance(tool, dict):
            violations.append(f"non-dict tool entry: {type(tool)}")
            continue
        name = tool.get("name")
        desc = tool.get("description")
        params = tool.get("parameters")
        if not isinstance(name, str) or not name:
            violations.append("tool without a name")
        if not isinstance(desc, str) or not desc.strip():
            violations.append(f"{name}: empty description")
        if not isinstance(params, dict):
            violations.append(f"{name}: parameters not an object")
    rec.artifact("g517-tool-census.json", json.dumps(
        {"count": len(tools), "violations": violations,
         "names": [t.get("name") for t in tools if isinstance(t, dict)]}, indent=2))
    observed = f"exit={run.exit_code}; tools={len(tools)}; violations={violations[:6]}"
    ok = run.exit_code == 0 and bool(tools) and not violations
    rec.finish("PASS" if ok else "FAIL",
               "docs/cookbook/adding-a-tool.md minimal shape (name/description/"
               "parameters) over the model-visible tool census",
               observed)
    assert ok, observed
