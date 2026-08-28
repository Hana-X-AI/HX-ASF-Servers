"""Gate 3 — providers, models, and Omni integration (test plan §7).

The routed proof: real calls from the candidate through OmniRoute to Qwen-X,
Coder-X, and Meta-X, with usage_history evidence mediated by the governor.

Seam facts traced at 0.1.1-rc.2:
- llm-deepseek: route `deepseek-official`; baseURL config → DEEPSEEK_BASE_URL →
  https://api.deepseek.com; POST <baseURL>/chat/completions, Bearer auth.
- llm-pi-ai: route dict; hand-declared routes take api: openai-completions,
  baseURL, apiKeyEnv, explicit models. Mounted dormant in the shipped base.
- agent-default-model: composition config + live settings section.

Every routed probe carries a unique nonce (OmniRoute semantic-cache discipline,
Trinity gate record). Credential values are never read: only the presence of
the variable named by GORDON_OMNI_KEY_ENV is checked.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from gordon_util import (
    blocked,
    events_of_type,
    find_session_artifacts,
    latest_request_header,
    nonce,
    read_session_log,
    render_fixture,
    run_candidate,
)

CALL_REGISTER = "routed-calls.jsonl"
DOWN_URL = "http://127.0.0.1:9"  # discard port: connection refused, deterministic


def seam_choice(cfg) -> str:
    """Which in-tree seam the fixture overlays use. `auto` defaults to the
    pi-ai openai-completions route (the generic in-tree seam); Morpheus's
    landed seam is recorded by G3-01 independently."""
    seam = cfg.seam
    if seam == "auto":
        return "pi-ai"
    if seam == "custom":
        blocked(
            "GORDON_SEAM=custom: out-of-tree adapter needs row id + config keys "
            "from Morpheus's handoff (GORDON_CUSTOM_ROW_ID and contract)"
        )
    if seam not in ("pi-ai", "deepseek"):
        blocked(f"GORDON_SEAM={seam!r} not in auto|pi-ai|deepseek|custom")
    return seam


def seam_provider(cfg) -> str:
    """The provider route name the fixture composition registers (matches the
    landed machine layer's route name, Morpheus receipt §8)."""
    return "omniroute" if seam_choice(cfg) == "pi-ai" else "deepseek-official"


def require_routing_inputs(cfg, model_key: str) -> str:
    """Presence-gated inputs for a routed run. Never reads secret values."""
    if not cfg.omni_key_present():
        blocked(
            f"credential value absent: governor must export the variable named "
            f"{cfg.omni_key_env_name} at execution time (existence checked, value never read)"
        )
    model_id = cfg.model_ids()[model_key]
    if not model_id:
        blocked(
            f"GORDON_MODEL_{model_key.upper()} unset: OmniRoute model id for this "
            f"call-sign is a Morpheus/Trinity handoff input"
        )
    return model_id


def seam_fixture_for(
    cfg,
    dest_dir: Path,
    *,
    model_key: str = "qwen",
    max_retries: int = 1,
    base_url: str | None = None,
    model_id: str | None = None,
    key_env: str | None = None,
    context_window: int = 65_536,
    max_tokens: int = 8_192,
) -> Path:
    """Render the routed-provider patch overlay for one fixture run.

    Capacity defaults mirror the landed fleet operating profile (receipt §8:
    65536 context, 8192 maxTokens, keeping input+output inside 64K)."""
    seam = seam_choice(cfg)
    url = base_url or cfg.omni_base_url
    mid = model_id or cfg.model_ids()[model_key] or "gordon-unset-model"
    mapping = {
        "KEY_ENV": key_env or cfg.omni_key_env_name,
        "BASE_URL": url,
        "MODEL_ID": mid,
        "MAX_RETRIES": str(max_retries),
        "CTX": str(context_window),
        "MAX_TOKENS": str(max_tokens),
    }
    template = "patch-pi-ai-route.yml.tmpl" if seam == "pi-ai" else "patch-deepseek-route.yml.tmpl"
    return render_fixture(template, mapping, dest_dir)


def register_call(cfg, entry: dict) -> None:
    path = cfg.evidence_dir / CALL_REGISTER
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")


def load_call_register(cfg) -> list[dict]:
    path = cfg.evidence_dir / CALL_REGISTER
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def run_routed_headless(
    cfg,
    scratch_env,
    workspace: Path,
    patch: Path,
    task: str,
    *,
    timeout: float = 300.0,
    extra_args: list[str] | None = None,
    env_extra: dict[str, str] | None = None,
):
    env = dict(scratch_env)
    if env_extra:
        env.update(env_extra)
    args = ["--profile", "headless", "--patch", str(patch), *(extra_args or []), task]
    return run_candidate(cfg, args, env_extra=env, cwd=str(workspace), timeout=timeout)


def assert_marker_run(cfg, scratch_home, run, marker: str) -> tuple[bool, str, dict]:
    """Shared routed-run oracle: exit 0, marker in an assistant/message event,
    turn/end reason completed. Returns (ok, observed, parsed_log)."""
    artifacts = find_session_artifacts(scratch_home, cfg)
    if not artifacts:
        return False, f"exit={run.exit_code}; no session artifact", {}
    log = read_session_log(cfg, artifacts[-1])
    records = log["records"]
    assistant = events_of_type(records, "assistant/message")
    marker_seen = any(
        marker in json.dumps(event.get("data", {})) for event in assistant
    )
    ends = events_of_type(records, "turn/end")
    completed = any(
        isinstance(e.get("data"), dict)
        and isinstance(e["data"].get("reason"), dict)
        and e["data"]["reason"].get("kind") == "completed"
        for e in ends
    )
    observed = (
        f"exit={run.exit_code}; marker_in_assistant_message={marker_seen}; "
        f"turn_end_completed={completed}; artifact={artifacts[-1].name}; "
        f"stderr={run.stderr[-200:]}"
    )
    return run.exit_code == 0 and marker_seen and completed, observed, log


def _read_real_file(cfg, path: str) -> str:
    """Read a file from the real home as the service user (read-only)."""
    from gordon_util import _runner_prefix, run_host

    prefix = _runner_prefix(cfg)
    proc = run_host(prefix + ["cat", path], timeout=30)
    return proc.stdout if proc.exit_code == 0 else ""


def test_g3_01_seam_census(cfg, candidate_bin, rec):
    """G3-01: record which seam the landed installation uses for Omni routing.

    Reads the real home's composition and settings (read-only). Never fails on
    WHICH seam; BLOCKED when nothing landed. Fail is reserved for evidence
    corruption (unreadable artifacts), not for the seam choice."""
    # Real-home dump: HOME=/home/dsh, no DSH_HOME override.
    run = run_candidate(cfg, ["--profile", "headless", "--dump-config"], env_extra={})
    rec.commands.append(run)
    rec.artifact("dump-real-home.yml", run.stdout + "\n--- STDERR ---\n" + run.stderr)
    settings_text = _read_real_file(cfg, f"{cfg.values['GORDON_REAL_HOME']}/settings.yaml")
    rec.artifact("real-settings.yaml", settings_text or "(absent or unreadable)")
    findings = {
        "dump_exit": run.exit_code,
        "pi_ai_row": "id: llm-pi-ai" in run.stdout,
        "deepseek_row": "id: llm-deepseek" in run.stdout,
        "omni_base_in_dump": cfg.omni_base_url in run.stdout,
        "omni_base_in_settings": cfg.omni_base_url in settings_text,
        "declared_seam_env": cfg.seam,
    }
    rec.artifact("seam-census.json", json.dumps(findings, indent=2))
    landed = findings["omni_base_in_dump"] or findings["omni_base_in_settings"] or cfg.seam != "auto"
    observed = json.dumps(findings)
    if not landed:
        rec.finish("BLOCKED", "composed config carries an OmniRoute seam",
                   observed, note="Morpheus seam handoff pending")
        blocked("no OmniRoute seam visible in the landed composition (Morpheus handoff pending)")
    rec.finish("PASS", "landed composition identifies its routing seam", observed)


def _seam_landed(cfg) -> bool:
    """Guard for runs that would send the OmniRoute client key somewhere:
    the census must have confirmed an OmniRoute seam before any real-home run."""
    census = cfg.evidence_dir / "test_g3_01_seam_census-seam-census.json"
    if not census.exists():
        return False
    findings = json.loads(census.read_text())
    return bool(
        findings.get("omni_base_in_dump")
        or findings.get("omni_base_in_settings")
        or (findings.get("declared_seam_env") not in (None, "", "auto"))
    )


def test_g3_02_missing_credential_fails_loud(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G3-02: no key for the route → MISSING_CREDENTIAL at request time, exit 1."""
    patch = seam_fixture_for(
        cfg, scratch_home, max_retries=0, key_env="GORDON_DELIBERATELY_UNSET_KEY"
    )
    run = run_routed_headless(
        cfg, scratch_env, workspace, patch,
        f"Reply with exactly: GORDON-G302-{nonce()}", timeout=180,
    )
    rec.commands.append(run)
    observed = f"exit={run.exit_code}; stderr={run.stderr[-300:]}"
    ok = run.exit_code == 1 and "MISSING_CREDENTIAL" in run.stderr
    rec.finish("PASS" if ok else "FAIL",
               "llm-deepseek/src/index.ts:427-431 LlmError MISSING_CREDENTIAL; "
               "headless fail path prints `dsh: <code>: <message>`",
               observed)
    assert ok, observed


def test_g3_03_provider_down_transport(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G3-03: unreachable provider → bounded TRANSPORT failure, exit 1."""
    if not cfg.omni_key_present():
        blocked(f"credential value absent ({cfg.omni_key_env_name}); down-drill still "
                "needs a key-shaped value to pass credential resolution")
    patch = seam_fixture_for(cfg, scratch_home, max_retries=1, base_url=DOWN_URL)
    started = time.monotonic()
    run = run_routed_headless(
        cfg, scratch_env, workspace, patch,
        f"Reply with exactly: GORDON-G303-{nonce()}", timeout=240,
    )
    elapsed = time.monotonic() - started
    rec.commands.append(run)
    observed = f"exit={run.exit_code}; elapsed={elapsed:.1f}s; stderr={run.stderr[-300:]}"
    ok = run.exit_code == 1 and "TRANSPORT" in run.stderr and elapsed < 240
    rec.finish("PASS" if ok else "FAIL",
               "llm-deepseek adapter.ts:498 LlmError TRANSPORT; retry bounded by fixture policy",
               observed)
    assert ok, observed


def _routed_model_run(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec,
                      model_key: str, tag: str):
    """One fixture-seam routed run against one call-sign model."""
    model_id = require_routing_inputs(cfg, model_key)
    marker = f"GORDON-{tag}-{nonce()}"
    patch = seam_fixture_for(cfg, scratch_home, model_key=model_key, max_retries=1)
    run = run_routed_headless(
        cfg, scratch_env, workspace, patch,
        f"Reply with exactly this token and nothing else: {marker}",
    )
    rec.commands.append(run)
    register_call(cfg, {
        "tag": tag, "model_key": model_key, "model_id": model_id,
        "marker": marker, "ts": int(time.time()), "exit": run.exit_code,
    })
    ok, observed, log = assert_marker_run(cfg, scratch_home, run, marker)
    if log:
        rec.artifact(f"{tag}-session-log.json", json.dumps(log)[:200000])
    rec.finish("PASS" if ok else "FAIL",
               "known-answer marker oracle (Gordon-chosen); headless turn/end completed; "
               "fixture seam openai-completions via OmniRoute",
               observed)
    assert ok, observed


def test_g3_04r_real_seam_run(cfg, candidate_bin, workspace, rec):
    """G3-04R: the landed profile, unmodified, drives one routed call.

    Uses the real home exactly as Morpheus configured it (the product's own
    session writes excepted; no config touch). Guard: runs only after G3-01
    confirmed an OmniRoute seam, so the client key can never travel to the
    public cloud default endpoint."""
    if not _seam_landed(cfg):
        rec.finish("BLOCKED", "G3-01 census confirms an OmniRoute seam",
                   "census absent or seam not landed",
                   note="guard prevents the client key reaching api.deepseek.com")
        blocked("G3-01 has not confirmed a landed OmniRoute seam")
    # No executor-side key needed: the landed home resolves the credential
    # natively from $DSH_HOME/.env (root:dsh 0640, receipt §6). The run uses
    # the landed default model (Coder-X per receipt §8).
    marker = f"GORDON-G304R-{nonce()}"
    run = run_candidate(
        cfg,
        ["--profile", "headless", f"Reply with exactly this token and nothing else: {marker}"],
        env_extra={}, cwd=str(workspace), timeout=300,
    )
    rec.commands.append(run)
    register_call(cfg, {
        "tag": "G304R", "model_key": "real-default", "model_id": "landed-default",
        "marker": marker, "ts": int(time.time()), "exit": run.exit_code,
    })
    marker_seen = marker in run.stdout
    observed = f"exit={run.exit_code}; marker_in_stdout={marker_seen}; stderr={run.stderr[-200:]}"
    ok = run.exit_code == 0 and marker_seen
    rec.finish("PASS" if ok else "FAIL",
               "landed seam, unmodified: routed call completes with the known-answer marker",
               observed)
    assert ok, observed


def test_g3_04f_routed_qwen(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G3-04F: fixture-seam routed call to Qwen-X."""
    _routed_model_run(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, "qwen", "G304F")


def test_g3_05f_routed_coder(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G3-05F: fixture-seam routed call to Coder-X."""
    _routed_model_run(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, "coder", "G305F")


def test_g3_06f_routed_meta(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G3-06F: fixture-seam routed call to Meta-X."""
    _routed_model_run(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, "meta", "G306F")


def test_g3_07_usage_history_evidence(cfg, rec):
    """G3-07: OmniRoute usage_history rows evidence this suite's routed calls.

    Governor-mediated: before/after snapshots dropped into GORDON_USAGE_DIR.
    Contract: JSON {"count": int, "rows": [{model, api_key_id, ts?, tokens_input,
    tokens_output, ...}]}. Without snapshots: BLOCKED-by-design (Trinity plane)."""
    before_path = cfg.usage_dir / "before.json"
    after_path = cfg.usage_dir / "after.json"
    if not (before_path.exists() and after_path.exists()):
        rec.finish(
            "BLOCKED",
            "Trinity gate record: usage_history rows with tokens_input/tokens_output/"
            "latency_ms/ttft_ms/api_key_id",
            "snapshots absent",
            note="named dependency: governor/Trinity usage_history snapshots "
                 f"at {cfg.usage_dir}/before.json + after.json",
        )
        blocked("governor usage_history snapshots absent (Trinity plane, governor-mediated)")
    before = json.loads(before_path.read_text())
    after = json.loads(after_path.read_text())
    calls = load_call_register(cfg)
    rec.artifact("usage-delta-input.json", json.dumps(
        {"before_count": before.get("count"), "after_count": after.get("count"),
         "suite_calls": len(calls)}, indent=2))
    delta = (after.get("count") or 0) - (before.get("count") or 0)
    rows = after.get("rows") or []
    our_models = {c["model_id"] for c in calls if c["model_id"] != "landed-default"}
    attributed = [r for r in rows if not our_models or r.get("model") in our_models]
    observed = (
        f"count_delta={delta}; suite_routed_calls={len(calls)}; "
        f"attributed_rows={len(attributed)}; our_models={sorted(our_models)}"
    )
    ok = bool(calls) and delta >= len(calls)
    rec.finish("PASS" if ok else "FAIL",
               "usage_history delta >= suite routed calls (nonce discipline makes "
               "every call a genuine backend round-trip)",
               observed,
               note="title-generation calls add to the provider side; counted openly")
    assert ok, observed


def test_g3_08_usage_reconciliation(cfg, scratch_home, rec):
    """G3-08: dsh-side TokenUsage vs OmniRoute accounting, same run.

    dsh side: assistant/message events carry usage (session types.ts:277).
    Requires a routed run in this test's own scratch home for independence."""
    require_routing_inputs(cfg, "qwen")
    marker = f"GORDON-G308-{nonce()}"
    patch = seam_fixture_for(cfg, scratch_home, model_key="qwen", max_retries=1)
    from pathlib import Path as _P

    ws = scratch_home.parent / "g308-workspace"
    ws.mkdir(exist_ok=True)
    run = run_routed_headless(
        cfg, {"HOME": str(scratch_home), "DSH_HOME": str(scratch_home)}, ws, patch,
        f"Reply with exactly this token and nothing else: {marker}",
    )
    rec.commands.append(run)
    register_call(cfg, {"tag": "G308", "model_key": "qwen",
                        "model_id": cfg.model_ids()["qwen"], "marker": marker,
                        "ts": int(time.time()), "exit": run.exit_code})
    ok_marker, observed_run, log = assert_marker_run(cfg, scratch_home, run, marker)
    usage_records = []
    if log:
        for event in events_of_type(log["records"], "assistant/message"):
            data = event.get("data") or {}
            usage = data.get("usage")
            if isinstance(usage, dict):
                usage_records.append(usage)
    rec.artifact("g308-usage.json", json.dumps(usage_records, indent=2))
    non_zero = any(
        (u.get("inputTokens") or 0) > 0 and (u.get("outputTokens") or 0) > 0
        for u in usage_records
    )
    observed = f"{observed_run}; usage_events={len(usage_records)}; non_zero={non_zero}"
    ok = ok_marker and non_zero
    rec.finish("PASS" if ok else "FAIL",
               "session types.ts:277 assistant/message.usage (TokenUsage: inputTokens/"
               "outputTokens disjoint, llm/types.ts:135)",
               observed,
               note="Omni-side comparison rows are G3-07's attributed delta")
    assert ok, observed


def test_g3_09_retry_events_durable(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G3-09: llm-retry writes durable llm/retry events before the final failure."""
    if not cfg.omni_key_present():
        blocked(f"credential value absent ({cfg.omni_key_env_name})")
    patch = seam_fixture_for(cfg, scratch_home, max_retries=2, base_url=DOWN_URL)
    run = run_routed_headless(
        cfg, scratch_env, workspace, patch,
        f"Reply with exactly: GORDON-G309-{nonce()}", timeout=300,
    )
    rec.commands.append(run)
    artifacts = find_session_artifacts(scratch_home, cfg)
    if not artifacts:
        rec.finish("FAIL", "session artifact after retry drill", "no artifact")
        pytest.fail("no session artifact under scratch home")
    log = read_session_log(cfg, artifacts[-1])
    rec.artifact("g309-session-log.json", json.dumps(log)[:200000])
    retry_events = events_of_type(log["records"], "llm/retry")
    observed = (
        f"exit={run.exit_code}; llm/retry_events={len(retry_events)}; "
        f"stderr={run.stderr[-200:]}"
    )
    ok = run.exit_code == 1 and len(retry_events) >= 1
    rec.finish("PASS" if ok else "FAIL",
               "llm-retry types.ts: each scheduled retry durable ('llm/retry') before "
               "its cancellable wait; final outcome failure",
               observed)
    assert ok, observed


def test_g3_10_token_measurement_derivable(cfg, rec):
    """G3-10: token measurement is derivable from the routed run's event stream.

    token-meter is replay-aware over session events (its module doc); the
    offline reconstruction path replays usage-bearing events. Evidence: the
    G3-08 artifact's usage events fold into a non-zero measurement."""
    usage_path = cfg.evidence_dir / "test_g3_08_usage_reconciliation-g308-usage.json"
    if not usage_path.exists():
        blocked("G3-08 usage artifact absent (run order or G3-08 disposition)")
    usage_records = json.loads(usage_path.read_text())
    total_in = sum(u.get("inputTokens") or 0 for u in usage_records)
    total_out = sum(u.get("outputTokens") or 0 for u in usage_records)
    observed = f"usage_events={len(usage_records)}; input={total_in}; output={total_out}"
    ok = bool(usage_records) and total_in > 0 and total_out > 0
    rec.finish("PASS" if ok else "FAIL",
               "token-meter replay-aware measurement over the session event stream",
               observed)
    assert ok, observed


def test_g3_11_catalog_self_consistency(cfg, candidate_bin, scratch_env, rec):
    """G3-11: the fixture composition's declared catalog matches the handoff ids."""
    models = {k: v for k, v in cfg.model_ids().items() if v}
    if not models:
        blocked("no GORDON_MODEL_* ids provided (handoff input)")
    run = _dump_with_fixture(cfg, scratch_env, rec)
    missing = [mid for mid in models.values() if mid not in run.stdout]
    observed = f"declared={sorted(models.values())}; missing_from_dump={missing}"
    ok = run.exit_code == 0 and not missing
    rec.finish("PASS" if ok else "FAIL",
               "fixture catalog == handoff model ids (identity self-consistency)",
               observed)
    assert ok, observed


def _dump_with_fixture(cfg, scratch_env, rec):
    from pathlib import Path as _P

    dest = _P(cfg.scratch) / "g311"
    dest.mkdir(parents=True, exist_ok=True)
    patch = seam_fixture_for(cfg, dest, model_key="qwen",
                             model_id=cfg.model_ids()["qwen"] or "gordon-unset-model")
    run = run_candidate(
        cfg, ["--profile", "headless", "--patch", str(patch), "--dump-config"],
        env_extra=scratch_env,
    )
    rec.commands.append(run)
    rec.artifact("g311-dump.yml", run.stdout)
    return run


def test_g3_12_no_cloud_baseurl(cfg, candidate_bin, scratch_env, rec):
    """G3-12: no composed baseURL points at the DeepSeek public cloud."""
    run = _dump_with_fixture(cfg, scratch_env, rec)
    leak = "api.deepseek.com" in run.stdout
    observed = f"public_cloud_baseurl_present={leak}"
    ok = run.exit_code == 0 and not leak
    rec.finish("PASS" if ok else "FAIL",
               "llm-deepseek PUBLIC_BASE_URL must not be the effective endpoint "
               "(local-only doctrine; dynamic leg is G3-07 attribution)",
               observed)
    assert ok, observed
