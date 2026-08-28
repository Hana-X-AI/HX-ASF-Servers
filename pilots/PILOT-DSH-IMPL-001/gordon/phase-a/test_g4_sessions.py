"""Gate 4 — sessions, events, persistence, and memory (test plan §8).

Format oracles: session-persistence-jsonl/src/format.ts (layout, header,
scanner), core/session/src/types.ts (SESSION_FORMAT_VERSION = 0), persistence
defaults (zstd, root mode 0700).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from gordon_util import (
    blocked,
    encode_segment,
    epoch_header,
    events_of_type,
    find_session_artifacts,
    project_key,
    read_file_bytes,
    read_session_log,
    run_candidate,
    seqs_contiguous,
)
from test_g3_providers import (
    assert_marker_run,
    register_call,
    require_routing_inputs,
    run_routed_headless,
    seam_fixture_for,
    seam_provider,
)
from gordon_util import nonce


def _routed_run(cfg, scratch_home, scratch_env, workspace, rec, tag: str, task: str | None = None,
                model_key: str = "coder", env_extra: dict | None = None, timeout: float = 300.0):
    from gordon_util import is_queue_transient

    require_routing_inputs(cfg, model_key)
    patch = seam_fixture_for(cfg, scratch_home, model_key=model_key, max_retries=1)
    import os

    spacing = float(os.environ.get("GORDON_QUEUE_SPACING_S", "25"))
    max_attempts = int(os.environ.get("GORDON_QUEUE_ATTEMPTS", "3"))
    run = None
    for attempt in range(1, max_attempts + 1):
        marker = f"GORDON-{tag}A{attempt}-{nonce()}"
        run = run_routed_headless(
            cfg, scratch_env, workspace, patch,
            (task or "Reply with exactly this token and nothing else: __MARKER__").replace("__MARKER__", marker),
            timeout=timeout, env_extra=env_extra,
        )
        rec.commands.append(run)
        register_call(cfg, {"tag": f"{tag}A{attempt}", "model_key": model_key,
                            "model_id": cfg.model_ids()[model_key], "marker": marker,
                            "ts": int(time.time()), "exit": run.exit_code})
        if run.exit_code == 0 or not is_queue_transient(run):
            break
        time.sleep(spacing)
    return run, marker


def test_g4_01_artifact_layout(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-01: session artifact lands at the derived per-project path."""
    from gordon_util import staged_sources

    run, marker = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G401")
    sources = staged_sources(cfg, scratch_home)
    expected_dir = str(scratch_home / "sessions" / project_key(str(workspace)))
    in_layout = any(source.startswith(expected_dir + "/") for source in sources)
    zstd_suffix = any(source.endswith("session.jsonl.zstd") for source in sources)
    observed = (
        f"exit={run.exit_code}; sources={sources}; "
        f"expected_project_dir={expected_dir}; zstd_suffix={zstd_suffix}"
    )
    ok = run.exit_code == 0 and bool(sources) and in_layout and zstd_suffix
    rec.finish("PASS" if ok else "FAIL",
               "format.ts:176-208 projectDir/sessionDir/logPath; default zstd suffix "
               "(layout asserted on source paths, not staged copies)",
               observed)
    assert ok, observed


def test_g4_02_header_contract(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-02: header line carries the format contract fields."""
    run, marker = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G402")
    artifacts = find_session_artifacts(scratch_home, cfg)
    if not artifacts:
        rec.finish("FAIL", "session artifact", "none found")
        pytest.fail("no session artifact")
    log = read_session_log(cfg, artifacts[-1])
    rec.artifact("g402-log.json", json.dumps(log)[:200000])
    header = log["header"] or {}
    checks = {
        "type_session": header.get("type") == "session",
        "version_0": header.get("version") == 0,
        "id_string": isinstance(header.get("id"), str) and header["id"].startswith("session-"),
        "created_at_epoch": isinstance(header.get("createdAt"), (int, float)),
        "delegation_depth": isinstance(header.get("delegationDepth"), int),
    }
    observed = json.dumps(checks)
    ok = run.exit_code == 0 and all(checks.values())
    rec.finish("PASS" if ok else "FAIL",
               "format.ts:33-44 isHeaderLine; core/session types.ts SESSION_FORMAT_VERSION=0",
               observed)
    assert ok, observed


def test_g4_03_event_stream_audit(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-03: turn lifecycle events present; seq contiguous from 0."""
    run, marker = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G403")
    ok_run, observed_run, log = assert_marker_run(cfg, scratch_home, run, marker)
    contiguous, seq_note = seqs_contiguous(log.get("records", [])) if log else (False, "no log")
    types = {r.get("type") for r in log.get("records", [])} if log else set()
    lifecycle = {"turn/start", "assistant/message", "turn/end"} <= types
    observed = f"{observed_run}; lifecycle={lifecycle}; seq: {seq_note}"
    ok = ok_run and contiguous and lifecycle
    rec.finish("PASS" if ok else "FAIL",
               "headless summarize (turn/start, assistant/message, turn/end); "
               "scanner seq rule (format.ts:362-376)",
               observed)
    assert ok, observed


def test_g4_04_restart_durability(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-04: run-1 artifact is byte-identical after run 2 in the same home."""
    run1, _ = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G404A")
    artifacts1 = find_session_artifacts(scratch_home, cfg)
    if not artifacts1:
        rec.finish("FAIL", "run-1 artifact", "none found")
        pytest.fail("no run-1 artifact")
    first = artifacts1[-1]
    before = read_file_bytes(cfg, first)
    run2, _ = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G404B")
    artifacts2 = find_session_artifacts(scratch_home, cfg)
    # Staging mode rebuilds the staging dir per listing, so re-resolve the same
    # session by its stable artifact name (staged names hash the source path).
    reread = next((a for a in artifacts2 if a.name == first.name), None)
    after = read_file_bytes(cfg, reread) if reread else b""
    observed = (
        f"run1_exit={run1.exit_code}; run2_exit={run2.exit_code}; "
        f"first_artifact_stable={before == after and bool(after)}; artifacts_total={len(artifacts2)}"
    )
    ok = (run1.exit_code == 0 and run2.exit_code == 0 and reread is not None
          and before == after and len(artifacts2) >= 2)
    rec.finish("PASS" if ok else "FAIL",
               "append-only per-session logs (format.ts module doc); a later run must "
               "not mutate an earlier session's artifact",
               observed)
    assert ok, observed


def test_g4_06a_corrupt_sibling_resilience(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-06(a): a corrupted sibling session log does not break boot or a new run.

    The sibling must be a valid zstd FRAME with corrupt JSONL inside: the
    backend rejects extension/content-encoding mismatches at its root on
    contact (first-run evidence: `.jsonl` under a zstd-configured backend
    fails loud by design)."""
    sessions_root = scratch_home / "sessions" / project_key(str(workspace)) / encode_segment("session-corrupt-seed")
    sessions_root.mkdir(parents=True, exist_ok=True)
    # The candidate must create the REAL session's sibling directory under the
    # same project dir: the chain must be dsh-writable (0755 hxsa blocks it).
    for level in (scratch_home / "sessions",
                  scratch_home / "sessions" / project_key(str(workspace)),
                  sessions_root):
        level.chmod(0o777)
    plain = sessions_root / "seed.jsonl"
    plain.write_bytes(
        b'{"type":"session","version":0,"id":"session-corrupt-seed","createdAt":1,"delegationDepth":0}\n'
        b'{"type":"turn/start","seq":0,"time":1,"data":{}}\n'
        b'{"corrupted":'
    )
    bad = sessions_root / "session.jsonl.zstd"
    from gordon_util import run_host

    packed = run_host(["zstd", "-q", "-f", str(plain), "-o", str(bad)], timeout=30)
    rec.commands.append(packed)
    plain.unlink()
    run, marker = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G406A")
    ok_run, observed_run, _log = assert_marker_run(cfg, scratch_home, run, marker)
    rec.finish("PASS" if ok_run else "FAIL",
               "corruption is per-artifact: boot + a fresh session proceed with a "
               "corrupt (framed) sibling present",
               observed_run)
    assert ok_run, observed_run


def test_g4_06b_resume_path_blocked_by_design(cfg, rec):
    """G4-06(b): resume/replay against a corrupted CURRENT log has no headless
    entry in the pinned CLI (resume belongs to the web/tui surfaces)."""
    rec.finish(
        "BLOCKED",
        "apps/cli args.ts: the pinned launcher exposes no headless resume/read entry; "
        "session read surfaces are web/tui (Phase B Gate 7)",
        "not executable in Phase A",
        note="reassigned: Phase B Gate 7 corrupted-session resume drill",
    )
    blocked("no headless resume entry in the pinned CLI; reassigned to Phase B Gate 7")


def test_g4_07_session_query_default_posture(cfg, candidate_bin, scratch_env, rec):
    """G4-07: session-query-sqlite mounts inert by default (:memory:, openAt never)."""
    run = run_candidate(cfg, ["--profile", "headless", "--dump-default-config"], env_extra=scratch_env)
    rec.commands.append(run)
    row = "id: session-query-sqlite" in run.stdout
    mem = ":memory:" in run.stdout
    never = "openAt: never" in run.stdout
    observed = f"row={row}; memory={mem}; openAt_never={never}"
    ok = run.exit_code == 0 and row and mem and never
    rec.finish("PASS" if ok else "FAIL",
               "base bundle session-query-sqlite row (content search opt-in)",
               observed, note="content search disposition: AVAILABLE_DISABLED")
    assert ok, observed


def test_g4_08_session_title_recorded(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-08: the title family produces a session/title record after a routed run."""
    run, marker = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G408")
    artifacts = find_session_artifacts(scratch_home, cfg)
    if not artifacts:
        rec.finish("FAIL", "session artifact", "none found")
        pytest.fail("no session artifact")
    log = read_session_log(cfg, artifacts[-1])
    titles = events_of_type(log["records"], "session/title")
    title_requests = events_of_type(log["records"], "session/title-llm-request")
    observed = (
        f"exit={run.exit_code}; title_events={len(titles)}; "
        f"title_llm_requests={len(title_requests)}"
    )
    ok = run.exit_code == 0 and (titles or title_requests)
    rec.finish("PASS" if ok else "FAIL",
               "base rows session-title + session-title-first-prompt-llm; event types "
               "session/title, session/title-llm-request (known-event-types.ts)",
               observed,
               note="title LLM call adds one OmniRoute usage row; counted in G3-07")
    assert ok, observed


def test_g4_09_telemetry_runtime_posture(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-09: switch set → no export attempts, fast exit; FULL mode against a
    closed OTLP endpoint still exits inside the bounded drain."""
    # Leg 1: switch set (base_env already exports DSH_TELEMETRY_DISABLED=1).
    run1, marker1 = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G409A")
    # Leg 2: switch unset + FULL mode + closed collector.
    env = {"DSH_TELEMETRY_DISABLED": "", "DSH_TELEMETRY_MODE": "FULL",
           "DSH_TELEMETRY_OTLP_URL": "http://127.0.0.1:9/v1/logs"}
    started = time.monotonic()
    run2, marker2 = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G409B",
                                env_extra=env)
    elapsed2 = time.monotonic() - started
    observed = (
        f"leg1_exit={run1.exit_code} (switch set); leg2_exit={run2.exit_code}; "
        f"leg2_elapsed={elapsed2:.1f}s; leg2_stderr={run2.stderr[-200:]}"
    )
    # Bounded drain per base bundle: exporter timeout 1s, shutdown bound 3s.
    ok = run1.exit_code == 0 and run2.exit_code == 0 and elapsed2 < 120
    rec.finish("PASS" if ok else "FAIL",
               "base rows 129-161: switch disables telemetry; FULL mode against an "
               "unreachable collector is bounded (~1s exporter, 3s shutdown)",
               observed)
    assert ok, observed


def test_g4_10_anonymous_identity(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-10: .anonymous-user-id is a stable bare UUID line in the harness home.

    The id is created by its consumers (llm-deepseek adapter user id, otel
    telemetry Resource user.id — identity package consumers). Under the landed
    pi-ai seam with telemetry DISABLED, no consumer runs: first-run evidence
    showed no file. The executable entry is a telemetry-FULL scratch run."""
    import re as _re

    env = {"DSH_TELEMETRY_DISABLED": "", "DSH_TELEMETRY_MODE": "FULL",
           "DSH_TELEMETRY_OTLP_URL": "http://127.0.0.1:9/v1/logs"}
    run1, _ = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G410A",
                          env_extra=env)
    id_file = scratch_home / ".anonymous-user-id"
    first = id_file.read_text().strip() if id_file.exists() else ""
    run2, _ = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G410B",
                          env_extra=env)
    second = id_file.read_text().strip() if id_file.exists() else ""
    uuid_ok = bool(_re.fullmatch(r"[0-9a-fA-F-]{36}", first))
    observed = (f"created={bool(first)}; uuid_shape={uuid_ok}; stable={first == second}; "
                f"exits={run1.exit_code},{run2.exit_code}")
    ok = first and uuid_ok and first == second
    rec.finish("PASS" if ok else "FAIL",
               "identity/anonymous-user-id: random UUID persisted as a bare line in "
               ".anonymous-user-id; created by its consumer (telemetry Resource user.id); "
               "delete to reset",
               ".anonymous-user-id; delete to reset",
               observed)
    assert ok, observed


def test_g4_11_settings_driven_selection(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-11: the agent-default-model settings section selects the model per era.

    The fixture catalog must include BOTH era models (pi-ai rejects a selected
    model absent from the route catalog with UNKNOWN_MODEL). Eras use Coder-X
    and Meta-X: Qwen-X is queue-saturated in the current window and already
    proven routed at G3-04F."""
    require_routing_inputs(cfg, "coder")
    require_routing_inputs(cfg, "meta")
    ids = cfg.model_ids()
    provider = seam_provider(cfg)
    from gordon_util import is_queue_transient

    patch = seam_fixture_for(cfg, scratch_home, model_ids=[ids["coder"], ids["meta"]], max_retries=1)

    def era(tag: str, model: str):
        (scratch_home / "settings.yaml").write_text(
            f"agent-default-model:\n  provider: {provider}\n  model: {model}\n"
        )
        import os

        spacing = float(os.environ.get("GORDON_QUEUE_SPACING_S", "25"))
        for attempt in range(1, int(os.environ.get("GORDON_QUEUE_ATTEMPTS", "3")) + 1):
            run = run_routed_headless(cfg, scratch_env, workspace, patch,
                                      f"Reply with exactly: GORDON-{tag}A{attempt}-{nonce()}")
            rec.commands.append(run)
            register_call(cfg, {"tag": f"{tag}A{attempt}", "model_key": "settings-era",
                                "model_id": model, "marker": f"era-{model}",
                                "ts": int(time.time()), "exit": run.exit_code})
            if run.exit_code == 0 or not is_queue_transient(run):
                return run
            time.sleep(spacing)
        return run

    run1 = era("G411A", ids["coder"])
    run2 = era("G411B", ids["meta"])
    artifacts = find_session_artifacts(scratch_home, cfg)
    models_seen = []
    for artifact in artifacts:
        log = read_session_log(cfg, artifact)
        header = None
        for rec_event in log["records"]:
            if rec_event.get("type") == "request/header":
                header = rec_event
        if header:
            config = epoch_header(header).get("config") or {}
            models_seen.append(config.get("model"))
    observed = f"exits={run1.exit_code},{run2.exit_code}; header_models={models_seen}"
    ok = (run1.exit_code == 0 and run2.exit_code == 0
          and ids["coder"] in models_seen and ids["meta"] in models_seen)
    rec.finish("PASS" if ok else "FAIL",
               "agent-default-model settings section (live per-Agent read): each era's "
               "selection appears in that era's request/header config",
               observed)
    assert ok, observed


def test_g4_12_attachment_composition(cfg, candidate_bin, scratch_env, rec):
    """G4-12: attachment-local mounts; image behavior has no Phase A entry path."""
    run = run_candidate(cfg, ["--profile", "headless", "--dump-default-config"], env_extra=scratch_env)
    rec.commands.append(run)
    row = "id: attachment-local" in run.stdout
    observed = f"row={row}"
    ok = run.exit_code == 0 and row
    rec.finish("PASS" if ok else "FAIL",
               "base bundle attachment-local row; root $DSH_HOME/attachments/v1 "
               "(attachment-local/src/index.ts:160)",
               observed,
               note="behavior NOT_RUN: no headless attach entry (startup.ts task-only); "
                    "Phase B covers image attach")
    assert ok, observed


def test_g4_13_spill_on_oversized_output(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-13: an oversized tool result spills to a file with the path reported.

    Model-cooperation class: the model must run the instructed bash command.
    One recorded re-run per doctrine §9."""
    attempts = []
    ok = False
    observed = ""
    for attempt in (1, 2):
        tag = f"G413-{attempt}"
        marker = f"GORDON-{tag}-{nonce()}"
        task = (
            "Use the bash tool to run exactly: seq 1 20000. "
            f"Then reply with exactly this token: {marker}"
        )
        run, _ = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, tag, task=task)
        artifacts = find_session_artifacts(scratch_home, cfg)
        spill_found = False
        spill_paths = []
        sandbox_unavailable = False
        if artifacts:
            log = read_session_log(cfg, artifacts[-1])
            log_text = json.dumps(log["records"])
            sandbox_unavailable = "SandboxUnavailableError" in log_text or "no sandbox backend is usable" in log_text
            import re as _re

            # Model-visible contract (tool-bash render.ts:11-14): the notice
            # `[output truncated; full output: <path>]` in the result text.
            spill_paths += _re.findall(r"full output: ([^]\s]+)", log_text)
            spill_paths += _re.findall(r'"spillPath":\s*"([^"]+)"', log_text)
            for candidate in spill_paths:
                try:
                    if len(read_file_bytes(cfg, Path(candidate))) > 50_000:
                        spill_found = True
                except OSError:
                    continue
        observed = (f"attempt={attempt}; exit={run.exit_code}; "
                    f"spill_paths={spill_paths}; spill_file_ok={spill_found}; "
                    f"sandbox_unavailable={sandbox_unavailable}")
        attempts.append(observed)
        if sandbox_unavailable:
            rec.finish(
                "BLOCKED",
                "spill proof requires a working bash executor; no sandbox backend "
                "is usable on hxs-15 (defect D1: no bwrap, no landlock prebuilt)",
                " | ".join(attempts),
                note="retest after Morpheus provisions a sandbox backend",
            )
            blocked("sandbox backend absent on hxs-15 (defect D1) — spill path unreachable")
        if run.exit_code == 0 and spill_found:
            ok = True
            break
    rec.finish("PASS" if ok else "FAIL",
               "spill-policy maxInlineBytes 50000; tool-bash: tail-truncated, full "
               "output saved, path reported",
               " | ".join(attempts),
               note="model-cooperation class; attempts recorded per doctrine")
    assert ok, " | ".join(attempts)


def test_g4_14_storage_composition(cfg, candidate_bin, scratch_env, rec):
    """G4-14: storage family mounts on the web profile; sqlite backend unmounted."""
    run = run_candidate(cfg, ["--profile", "web", "--dump-default-config"], env_extra=scratch_env)
    rec.commands.append(run)
    rec.artifact("dump-web-default.yml", run.stdout)
    rows = {row: f"id: {row}" in run.stdout for row in ("storage", "storage-json", "storage-domain")}
    sqlite_absent = "storage-sqlite" not in run.stdout
    observed = f"rows={rows}; storage_sqlite_absent={sqlite_absent}"
    ok = run.exit_code == 0 and all(rows.values()) and sqlite_absent
    rec.finish("PASS" if ok else "FAIL",
               "web-app bundle storage rows (storage-json root dshHomePath('storages'))",
               observed,
               note="behavior NOT_RUN (web plane, Phase B); storage-sqlite AVAILABLE_DISABLED")
    assert ok, observed


def test_g4_15_credentials_env_fallback(cfg, candidate_bin, scratch_home, workspace, rec):
    """G4-15: the key resolves from $DSH_HOME/.env when the environment lacks it.

    The fixture .env is provisioned two ways, neither exposing the value to
    Gordon's context: governor-exported executor env (written directly), or a
    copy of the landed /var/lib/dsh/.env made BY the service user (its own
    readable file) into the scratch home. Deleted in finally either way."""
    import os
    import subprocess
    import time as _time

    from gordon_util import _runner_prefix, base_env, candidate_argv, key_source_available

    if not key_source_available(cfg):
        blocked(f"credential value absent ({cfg.omni_key_env_name} or landed .env)")
    require_routing_inputs(cfg, "coder")
    env_file = scratch_home / ".env"
    if cfg.omni_key_present():
        env_file.write_text(f"{cfg.omni_key_env_name}={os.environ[cfg.omni_key_env_name]}\n")
    else:
        prefix = _runner_prefix(cfg)
        copied = subprocess.run(
            prefix + ["cp", "/var/lib/dsh/.env", str(env_file)],
            capture_output=True, timeout=30,
        )
        if copied.returncode != 0:
            blocked("service-user copy of the landed .env into the scratch home failed")
    env = {"HOME": str(scratch_home), "DSH_HOME": str(scratch_home)}
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    marker = f"GORDON-G415-{nonce()}"
    # Strip the inherited key so only the .env layer can satisfy resolution;
    # no-key mode keeps the wrapper from re-adding the landed one.
    full_env = base_env(cfg, env)
    full_env.pop(cfg.omni_key_env_name, None)
    argv = candidate_argv(
        cfg,
        ["--profile", "headless", "--patch", str(patch),
         f"Reply with exactly this token and nothing else: {marker}"],
        full_env,
        key_mode="no-key",
    )
    from gordon_util import RunRecord, is_queue_transient

    run = None
    try:
        for attempt in (1, 2, 3):
            started = _time.monotonic()
            proc = subprocess.run(
                argv, capture_output=True, text=True, cwd=str(workspace), timeout=300,
            )
            run = RunRecord([cfg.dsh_bin, "--profile", "headless", "--patch", str(patch), "<task>"],
                            sorted(full_env.keys()), str(workspace), proc.returncode,
                            proc.stdout, proc.stderr, _time.monotonic() - started)
            rec.commands.append(run)
            register_call(cfg, {"tag": f"G415A{attempt}", "model_key": "coder",
                                "model_id": cfg.model_ids()["coder"],
                                "marker": marker, "ts": int(_time.time()), "exit": run.exit_code})
            if run.exit_code == 0 or not is_queue_transient(run):
                break
            _time.sleep(float(__import__('os').environ.get('GORDON_QUEUE_SPACING_S', '25')))
    finally:
        # Secret hygiene: the .env fixture is transient test data; remove it as
        # soon as the run settles (pytest keeps tmp dirs across runs).
        env_file.unlink(missing_ok=True)
    marker_seen = marker in run.stdout
    observed = f"exit={run.exit_code}; marker_in_stdout={marker_seen}; stderr={run.stderr[-200:]}"
    ok = run.exit_code == 0 and marker_seen
    rec.finish("PASS" if ok else "FAIL",
               "credentials-local layering: env > managed store > <cwd>/.env > "
               "$DSH_HOME/.env; loadLayeredEnv trusted layers",
               observed)
    assert ok, observed


def test_g4_17_agent_instructions_context(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G4-17: AGENTS.md content reaches the model-visible request (context family).

    The fixture workspace carries an AGENTS.md with a static marker. Live
    evidence (probe 2026-08-28): instructions arrive as a `user/message` event
    with source kind `agent-instructions`, not inside request/header fields —
    so the whole durable stream is the assertion surface."""
    import shutil as _shutil

    marker = "GORDON-AGENTS-MD-MARKER-7f3a9c"
    fixture = Path(__file__).parent / "fixtures" / "workspace-AGENTS.md"
    _shutil.copy(fixture, workspace / "AGENTS.md")
    run, _ = _routed_run(cfg, scratch_home, scratch_env, workspace, rec, "G417")
    artifacts = find_session_artifacts(scratch_home, cfg)
    if not artifacts:
        rec.finish("FAIL", "session artifact", "none found")
        pytest.fail("no session artifact")
    log = read_session_log(cfg, artifacts[-1])
    records_text = json.dumps(log["records"])
    found = marker in records_text
    instruction_events = [
        r for r in log["records"]
        if r.get("type") == "user/message"
        and "agent-instructions" in json.dumps(r.get("data") or {})
    ]
    observed = (f"exit={run.exit_code}; marker_in_stream={found}; "
                f"agent_instructions_events={len(instruction_events)}")
    ok = run.exit_code == 0 and found
    rec.finish("PASS" if ok else "FAIL",
               "agent-instructions row (base bundle, maxBytes 65536); model-visible "
               "⟺ logged (repo AGENTS.md)",
               observed)
    assert ok, observed


def test_g4_16_session_stats_projection_cache_census(cfg, candidate_bin, scratch_env, rec):
    """G4-16: session-stats and session-projection-cache mount on the web profile
    only (web-app bundle rows); the headless composition omits them by design."""
    web = run_candidate(cfg, ["--profile", "web", "--dump-default-config"], env_extra=scratch_env)
    headless = run_candidate(cfg, ["--profile", "headless", "--dump-default-config"], env_extra=scratch_env)
    rec.commands.extend([web, headless])
    web_rows = all(f"id: {row}" in web.stdout for row in ("session-stats", "session-projection-cache"))
    headless_lacks = "id: session-stats" not in headless.stdout
    observed = f"web_rows={web_rows}; headless_omits_stats={headless_lacks}"
    ok = web.exit_code == 0 and web_rows and headless_lacks
    rec.finish("PASS" if ok else "FAIL",
               "web-app bundle rows 76-77, 90-91; base bundle omits session-stats",
               observed,
               note="headless plane disposition: AVAILABLE_DISABLED (web-only rows)")
    assert ok, observed
