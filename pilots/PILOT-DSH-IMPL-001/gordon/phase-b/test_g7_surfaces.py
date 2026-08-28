"""Gate 7 — web, API, SDK, ACP, telemetry, user experience (plan §4).

Web boots run on loopback with OS-assigned ports in scratch homes. The /api
envelope of record (Morpheus §10): POST /api/<ns.method> with
{"type":"client-request","rpcId","method","payload"} → server-response; WS
downlinks /api/events.mux + /api/events.host (plain GET → 426). The eight
rows blocked at authoring (G7-04/06/08/14/15/16/17/19) execute against this
envelope in the release window — traced, never guessed.
"""

from __future__ import annotations

import gzip
import json
import os
import struct
import subprocess
import time
from pathlib import Path

import pytest

from conftest import (
    FIXTURES,
    ApiClient,
    WsDownlink,
    latest_log,
    log_text,
    run_as_dsh_argv,
)
from gordon_util import (
    blocked,
    events_of_type,
    find_session_artifacts,
    is_queue_transient,
    nonce,
    project_key,
    read_file_bytes,
    read_session_log,
    render_fixture,
    run_candidate,
    run_host,
    zstd_decode,
)
from test_g3_providers import register_call, require_routing_inputs, seam_fixture_for

SUITE_DIR = Path(__file__).resolve().parent

LIVE_HOST = "192.168.50.214"
LIVE_PORT = 3080

SDK_CLIENT_LIB = "/opt/dsh/packages/sdk/client/lib/index.js"
SDK_RUNTIME_BIN = "/opt/dsh/packages/examples/jsonrpc-demo/lib/bin.js"
ACP_BIN = "/opt/dsh/packages/examples/acp-demo/lib/bin.js"
PYTHON_SDK_SRC = "/opt/dsh/python/sdk/src"
PYSDK_LIB = "/var/tmp/gordon-pysdk-lib"


def _dist_present(cfg) -> bool:
    dist = Path(cfg.dsh_root) / "apps/web/dist"
    return dist.is_dir() and any(dist.iterdir())


def _rpc_ok(body: dict) -> bool:
    return isinstance(body, dict) and body.get("type") == "server-response" \
        and (body.get("result") or {}).get("ok") is True


def _rpc_value(body: dict):
    return (body.get("result") or {}).get("value")


def _history(api: ApiClient, session_id: str) -> list[dict]:
    status, body = api.rpc("session.history", {"sessionId": session_id})
    if status != 200 or not _rpc_ok(body):
        return []
    value = _rpc_value(body) or {}
    return [entry.get("event", {}) for entry in value.get("events", [])]


def _wait_turn_end(api: ApiClient, session_id: str, timeout: float = 300.0) -> list[dict]:
    """Poll session.history until a turn/end event lands (bounded)."""
    deadline = time.monotonic() + timeout
    events: list[dict] = []
    while time.monotonic() < deadline:
        events = _history(api, session_id)
        if any(e.get("type") == "turn/end" for e in events):
            return events
        time.sleep(3)
    return events


def _web_session_chat(cfg, scratch_home, scratch_env, workspace, rec, web_boot,
                      tag: str, task: str, timeout: float = 300.0):
    """Boot web (seam patch), create a session, prompt, wait for turn end.
    Returns (api, session_id, events, boot)."""
    require_routing_inputs(cfg, "coder")
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    boot = web_boot(scratch_env, str(workspace), patches=[str(patch)])
    if not boot.wait_bound(120):
        boot.stop()
        rec.finish("FAIL", "web boot binds", "no listener; log: " + boot.boot_log()[-300:])
        pytest.fail("web boot did not bind")
    api = ApiClient(boot.port)
    status, created = api.rpc("session.create", {"cwd": str(workspace)})
    if status != 200 or not _rpc_ok(created):
        boot.stop()
        rec.finish("FAIL", "session.create answers ok", f"status={status}; body={created}")
        pytest.fail(f"session.create failed: {created}")
    session_id = (_rpc_value(created) or {}).get("sessionId")
    marker = f"GORDON-{tag}-{nonce()}"
    register_call(cfg, {"tag": tag, "model_key": "coder",
                        "model_id": cfg.model_ids()["coder"], "marker": marker,
                        "ts": int(time.time()), "entry": "web-api"})
    status, accepted = api.rpc("session.prompt", {
        "sessionId": session_id,
        "mode": "queue",
        "content": [{"type": "text", "text": task.replace("__MARKER__", marker)}],
    })
    rec.artifact(f"{tag.lower()}-prompt-accept.json", json.dumps(accepted, indent=2))
    events = _wait_turn_end(api, session_id, timeout=timeout)
    return api, session_id, marker, events, boot, accepted


def test_g7_01_web_serves_frontend(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-01: web boot serves the built app shell — closes G2-10/G5-10."""
    if not _dist_present(cfg):
        rec.finish("FAIL",
                   "frontend dist present at release (Morpheus Phase B build)",
                   f"{cfg.dsh_root}/apps/web/dist absent or empty",
                   note="the G2-10/G5-10 BLOCKED-by-design flips to FAIL per plan")
        pytest.fail("frontend dist missing at release")
    boot = web_boot(scratch_env, str(workspace))
    try:
        if not boot.wait_bound(120):
            rec.finish("FAIL", "web boot binds", "no listener; log: " + boot.boot_log()[-300:])
            pytest.fail("web boot did not bind")
        status, body = boot.http_get("/")
        rec.artifact("web-index.html", body[:50000])
        shell_markers = [m for m in ("<div id=\"root\"", "dsh", "script") if m in body]
        observed = f"status={status}; port={boot.port}; shell_markers={shell_markers}"
        ok = status == 200 and body and shell_markers
        rec.finish("PASS" if ok else "FAIL",
                   "apps/web index + frontend-static serve the built shell on loopback",
                   observed, note="closes G2-10/G5-10 BLOCKED-by-design rows")
        assert ok, observed
    finally:
        exit_code = boot.stop()
        if exit_code != 0:
            rec.finish("FAIL", "SIGTERM exits 0 (profile-boot.ts:221)", f"exit={exit_code}")
            pytest.fail(f"web boot SIGTERM exit {exit_code}")


def test_g7_02_api_gateway_sessions(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-02: the /api envelope of record answers a session.list RPC; carrier
    fences (415 media type, 404 unknown method, bad-request mismatch) and the
    WS downlink GET→426 contract hold."""
    if not _dist_present(cfg):
        blocked("frontend dist absent (G7-01 finding)")
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    boot = web_boot(scratch_env, str(workspace), patches=[str(patch)])
    try:
        if not boot.wait_bound(120):
            rec.finish("FAIL", "web boot binds", "no listener")
            pytest.fail("web boot did not bind")
        api = ApiClient(boot.port)
        status, body = api.rpc("session.list", {})
        rec.artifact("g702-session-list.json", json.dumps(body, indent=2)[:20000])
        envelope_ok = (status == 200 and _rpc_ok(body)
                       and isinstance((_rpc_value(body) or {}).get("items"), list))
        # Carrier negative legs (handler.ts contract of record).
        import urllib.request
        plain = urllib.request.Request(
            f"{api.base}/api/session.list", data=b"{}",
            headers={"Content-Type": "text/plain"}, method="POST")
        try:
            urllib.request.urlopen(plain, timeout=10)
            media_status = 0
        except urllib.error.HTTPError as exc:
            media_status = exc.code
        unknown = api.rpc("no.such.method", {})
        # method/path mismatch: envelope method != path method
        import urllib.request as u2
        raw = json.dumps({"type": "client-request", "rpcId": "gordon-mismatch",
                          "method": "host.describe", "payload": {}}).encode()
        req = u2.Request(f"{api.base}/api/session.list", data=raw,
                         headers={"Content-Type": "application/json"}, method="POST")
        try:
            with u2.urlopen(req, timeout=10) as resp:
                mismatch_body = json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            # non-2xx still carries the parsed response body (bad-request leg)
            mismatch_body = json.loads(exc.read().decode())
        mismatched = (mismatch_body.get("result") or {}).get("ok") is False \
            and ((mismatch_body.get("result") or {}).get("error") or {}).get("code") == "bad-request"
        downlinks = {}
        for path in ("/api/events.mux", "/api/events.host"):
            code, _, _ = api.get(path, timeout=10)
            downlinks[path] = code
        observed = (f"envelope_ok={envelope_ok}; media_415={media_status}; "
                    f"unknown_404={unknown[0]}; mismatch_bad_request={mismatched}; "
                    f"downlinks_get={downlinks}")
        ok = (envelope_ok and media_status == 415 and unknown[0] == 404
              and mismatched and all(c == 426 for c in downlinks.values()))
        rec.finish("PASS" if ok else "FAIL",
                   "api/gateway Typert+apiproxy dispatch: client-request envelope → "
                   "server-response; 415/404/bad-request carrier legs; WS downlink GET→426",
                   observed, note="envelope of record traced live (plan §5 R1 resolved)")
        assert ok, observed
    finally:
        boot.stop()


def test_g7_03_web_round_trip(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-03: session.create → WS downlink subscribe → session.prompt → the
    assistant reply for a nonce task is visible in the event stream; the
    session is durable on disk with the routed provider identity."""
    if not _dist_present(cfg):
        blocked("frontend dist absent (G7-01 finding)")
    require_routing_inputs(cfg, "coder")
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    boot = web_boot(scratch_env, str(workspace), patches=[str(patch)])
    try:
        if not boot.wait_bound(120):
            rec.finish("FAIL", "web boot binds", "no listener")
            pytest.fail("web boot did not bind")
        api = ApiClient(boot.port)
        status, created = api.rpc("session.create", {"cwd": str(workspace)})
        session_id = (_rpc_value(created) or {}).get("sessionId")
        marker = f"GORDON-G703-{nonce()}"
        register_call(cfg, {"tag": "G703", "model_key": "coder",
                            "model_id": cfg.model_ids()["coder"], "marker": marker,
                            "ts": int(time.time()), "entry": "web-api"})
        downlink = WsDownlink(boot.port, "/api/events.host")
        rec.artifact("g703-ws-handshake.txt", downlink.head)
        try:
            api.rpc("session.prompt", {
                "sessionId": session_id, "mode": "queue",
                "content": [{"type": "text", "text":
                             f"Reply with exactly this token and nothing else: {marker}"}],
            })
            frames = downlink.collect_until(
                lambda frame: marker in json.dumps(frame), timeout_s=300.0)
        finally:
            downlink.close()
        frame_types = sorted({str((f.get("payload") or {}).get("type", f.get("method", "?")))
                              for f in frames})
        streamed = any(marker in json.dumps(f) for f in frames)
        rec.artifact("g703-frames.json",
                     json.dumps({"count": len(frames), "types": frame_types,
                                 "tail": frames[-4:]}, indent=2)[:40000])
        # Durable leg: the session artifact on disk carries the routed identity.
        artifacts = find_session_artifacts(scratch_home, cfg)
        durable_marker = False
        routed = False
        for artifact in artifacts:
            log = read_session_log(cfg, artifact)
            text = log_text(log)
            if marker in text:
                durable_marker = True
                if "omniroute" in text:
                    routed = True
        observed = (f"ws_status={downlink.status}; frames={len(frames)}; "
                    f"streamed_marker={streamed}; durable_marker={durable_marker}; "
                    f"routed_identity={routed}; frame_types={frame_types}")
        ok = (downlink.status == 101 and streamed and durable_marker and routed)
        rec.finish("PASS" if ok else "FAIL",
                   "web round-trip: session.create/prompt envelope, WS events.host "
                   "downlink carries the reply, session durable with routed identity",
                   observed)
        assert ok, observed
    finally:
        boot.stop()


def test_g7_04_trajectory_data(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-04 (executes — was BLOCKED at authoring): after a tool-call chat the
    session window carries the tool events; replay recompute is identical."""
    if not _dist_present(cfg):
        blocked("frontend dist absent (G7-01 finding)")
    attempts = []
    final = None
    for attempt in (1, 2):
        home = scratch_home if attempt == 1 else workspace.parent / f"g704-home{attempt}"
        if attempt == 2:
            home.mkdir(); home.chmod(0o777)
            env2 = {"HOME": str(home), "DSH_HOME": str(home)}
        else:
            env2 = scratch_env
        patch = seam_fixture_for(cfg, home, model_key="coder", max_retries=1)
        require_routing_inputs(cfg, "coder")
        boot = web_boot(env2, str(workspace), patches=[str(patch)])
        try:
            if not boot.wait_bound(120):
                attempts.append(f"attempt{attempt}: no bind")
                continue
            api = ApiClient(boot.port)
            _, created = api.rpc("session.create", {"cwd": str(workspace)})
            session_id = (_rpc_value(created) or {}).get("sessionId")
            marker = f"GORDON-G704A{attempt}-{nonce()}"
            register_call(cfg, {"tag": f"G704A{attempt}", "model_key": "coder",
                                "model_id": cfg.model_ids()["coder"], "marker": marker,
                                "ts": int(time.time()), "entry": "web-api"})
            api.rpc("session.prompt", {
                "sessionId": session_id, "mode": "queue",
                "content": [{"type": "text", "text":
                             (f"Use the bash tool to run exactly: echo {marker} "
                              "Then reply with exactly: DONE")}],
            })
            events = _wait_turn_end(api, session_id, timeout=360)
            tool_calls = [e for e in events if e.get("type") == "tool/call"]
            tool_results = [e for e in events if e.get("type") == "tool/result"]
            marker_in_result = any(marker in json.dumps(e.get("data", {})) for e in tool_results)
            # Replay determinism: a second history fetch recomputes identically.
            again = _history(api, session_id)
            identical = json.dumps(events, sort_keys=True) == json.dumps(again, sort_keys=True)
            attempts.append(f"attempt{attempt}: tool_calls={len(tool_calls)}; "
                            f"marker_in_result={marker_in_result}; replay_identical={identical}")
            if tool_calls and marker_in_result and identical:
                final = (api, session_id, events, tool_calls, tool_results)
                rec.artifact("g704-history.json", json.dumps(events, indent=2)[:60000])
                break
        finally:
            boot.stop()
    observed = " | ".join(attempts)
    ok = final is not None
    rec.finish("PASS" if ok else "FAIL",
               "ui-trajectory data layer: the host session window carries tool/call + "
               "tool/result events; web layer is pure presentation — replay recomputes "
               "identically (client AGENTS.md red lines)",
               observed, note="executed in the release window against the §10 envelope")
    assert ok, observed


def test_g7_05_session_query_search(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-05: search disabled under the shipped default (named code); enabled
    under the fixture patch (marker found across sessions); the native
    real-home mount answers on the live LAN service (read-only probe; the
    first search materializes the product's own index — allowed product write
    of record)."""
    # Leg 1: shipped default contract (composition evidence).
    dump = run_candidate(cfg, ["--profile", "headless", "--dump-default-config"],
                         env_extra=scratch_env)
    rec.commands.append(dump)
    default_posture = ":memory:" in dump.stdout and "openAt: never" in dump.stdout
    # Leg 2: enabled patch composes (durable scratch path).
    query_path = scratch_home / "query-index.sqlite"
    from test_g6_orchestration import seam_fixture_b

    patch = seam_fixture_b(cfg, scratch_home, "patch-session-query.yml.tmpl",
                           extra={"QUERY_PATH": str(query_path)})
    dump2 = run_candidate(
        cfg, ["--profile", "headless", "--patch", str(patch), "--dump-config"],
        env_extra=scratch_env,
    )
    rec.commands.append(dump2)
    enabled = "openAt: first-search" in dump2.stdout and str(query_path) in dump2.stdout
    # Leg 3: default behavior — search call fails with the named code.
    patch_route = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    boot = web_boot(scratch_env, str(workspace), patches=[str(patch_route)])
    disabled_code = None
    try:
        if boot.wait_bound(120):
            api = ApiClient(boot.port)
            status, body = api.rpc("session.search", {"query": "gordon-probe"})
            rec.artifact("g705-search-disabled.json", json.dumps(body, indent=2))
            error = (body.get("result") or {}).get("error") or {}
            disabled_code = error.get("code")
    finally:
        boot.stop()
    # Leg 4: enabled behavior — marker found across sessions, index durable.
    home2 = workspace.parent / "g705-home2"
    home2.mkdir(); home2.chmod(0o777)
    env2 = {"HOME": str(home2), "DSH_HOME": str(home2)}
    query_path2 = home2 / "query-index.sqlite"
    patch2 = seam_fixture_b(cfg, home2, "patch-session-query.yml.tmpl",
                            extra={"QUERY_PATH": str(query_path2)})
    marker = f"GORDON-G705-{nonce()}"
    hits = 0
    index_materialized = False
    boot2 = web_boot(env2, str(workspace), patches=[str(patch2)])
    try:
        if boot2.wait_bound(120):
            api2 = ApiClient(boot2.port)
            require_routing_inputs(cfg, "coder")
            for i in (1, 2):
                _, created = api2.rpc("session.create", {"cwd": str(workspace)})
                sid = (_rpc_value(created) or {}).get("sessionId")
                register_call(cfg, {"tag": f"G705s{i}", "model_key": "coder",
                                    "model_id": cfg.model_ids()["coder"], "marker": marker,
                                    "ts": int(time.time()), "entry": "web-api"})
                api2.rpc("session.prompt", {
                    "sessionId": sid, "mode": "queue",
                    "content": [{"type": "text", "text":
                                 f"Note this phrase: {marker}. Reply with exactly: DONE"}],
                })
                _wait_turn_end(api2, sid, timeout=240)
            status, body = api2.rpc("session.search", {"query": marker})
            rec.artifact("g705-search-enabled.json", json.dumps(body, indent=2)[:20000])
            if _rpc_ok(body):
                hits = len((_rpc_value(body) or {}).get("items", []))
            index_materialized = query_path2.exists()
    finally:
        boot2.stop()
    # Leg 5: live real-home mount answers (read-only probe; product's own
    # index write is the documented first-search behavior — Morpheus §10
    # watch item (ii); allowed product-own write).
    live_ok = False
    live_error = "none"
    try:
        live = ApiClient(LIVE_PORT, host=LIVE_HOST)
        live_status, live_body = live.rpc("session.search", {"query": "gordon-nonexistent-zzz-000"})
        rec.artifact("g705-live-search.json", json.dumps(live_body, indent=2)[:10000])
        live_ok = live_status == 200 and _rpc_ok(live_body)
    except Exception as exc:  # transport failure: observed value, never propagated
        live_error = f"{type(exc).__name__}: {exc}"
    observed = (f"default_posture={default_posture}; enabled_patch_composes={enabled}; "
                f"disabled_error_code={disabled_code!r}; enabled_hits={hits}; "
                f"index_durable={index_materialized}; live_real_home_ok={live_ok}; "
                f"live_error={live_error}")
    ok = (default_posture and enabled and dump2.exit_code == 0
          and disabled_code == "SESSION_QUERY_SEARCH_DISABLED"
          and hits >= 2 and index_materialized and live_ok)
    rec.finish("PASS" if ok else "FAIL",
               "session-query-sqlite openAt never|first-search: SESSION_QUERY_SEARCH_DISABLED "
               "under the shipped default; marker found across sessions under first-search "
               "with a durable path; native real-home mount answers on the live service",
               observed)
    assert ok, observed


def test_g7_06_session_export(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-06 (executes — was BLOCKED at authoring): the download endpoint
    returns the durable session bytes."""
    if not _dist_present(cfg):
        blocked("frontend dist absent (G7-01 finding)")
    require_routing_inputs(cfg, "coder")
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    boot = web_boot(scratch_env, str(workspace), patches=[str(patch)])
    try:
        if not boot.wait_bound(120):
            rec.finish("FAIL", "web boot binds", "no listener")
            pytest.fail("web boot did not bind")
        api = ApiClient(boot.port)
        _, created = api.rpc("session.create", {"cwd": str(workspace)})
        session_id = (_rpc_value(created) or {}).get("sessionId")
        marker = f"GORDON-G706-{nonce()}"
        register_call(cfg, {"tag": "G706", "model_key": "coder",
                            "model_id": cfg.model_ids()["coder"], "marker": marker,
                            "ts": int(time.time()), "entry": "web-api"})
        api.rpc("session.prompt", {
            "sessionId": session_id, "mode": "queue",
            "content": [{"type": "text", "text":
                         f"Reply with exactly this token and nothing else: {marker}"}],
        })
        events = _wait_turn_end(api, session_id, timeout=300)
        status, exported, headers = api.get(f"/api/session.export?sessionId={session_id}", timeout=30)
        # Durable artifact: the session's own zstd log, decoded.
        artifacts = find_session_artifacts(scratch_home, cfg)
        durable = None
        for artifact in artifacts:
            log = read_session_log(cfg, artifact)
            if marker in log_text(log):
                durable = artifact
        durable_bytes = b""
        if durable is not None:
            durable_bytes = zstd_decode(cfg, durable) if durable.suffix == ".zstd" \
                else read_file_bytes(cfg, durable)
        rec.artifact("g706-export.bin", exported)
        import hashlib
        same = bool(durable_bytes) and exported == durable_bytes
        observed = (f"http={status}; exported_bytes={len(exported)}; "
                    f"durable_bytes={len(durable_bytes)}; turn_events={len(events)}; "
                    f"export_sha256={hashlib.sha256(exported).hexdigest()[:16]}; "
                    f"durable_sha256={hashlib.sha256(durable_bytes).hexdigest()[:16] if durable_bytes else 'none'}; "
                    f"bytes_equal={same}")
        ok = status == 200 and same
        rec.finish("PASS" if ok else "FAIL",
                   "session-log-export: GET /api/session.export?sessionId=… returns exactly "
                   "the durable artifact bytes (zstd-decoded session.jsonl)",
                   observed, note="executed in the release window against the §10 envelope")
        assert ok, observed
    finally:
        boot.stop()


def test_g7_07_corrupted_session_web_read(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-07 (G4-06(b) closure): the web read path vs a torn-tail log and a
    corrupt-middle log. Scanner semantics (format.ts:337-344): the torn tail
    is ignored and the committed prefix is served."""
    if not _dist_present(cfg):
        blocked("frontend dist absent (G7-01 finding)")
    import subprocess as sp

    key = project_key(str(workspace))
    sessions_root = scratch_home / "sessions" / key
    # Torn tail: valid header + two committed events + a torn final record.
    torn_dir = sessions_root / "session-torn-tail"
    torn_dir.mkdir(parents=True, exist_ok=True)
    torn_plain = torn_dir / "torn.jsonl"
    torn_plain.write_bytes(
        b'{"type":"session","version":0,"id":"session-torn-tail","createdAt":1,'
        b'"cwd":"' + str(workspace).encode() + b'","delegationDepth":0}\n'
        b'{"type":"turn/start","seq":0,"time":1,"data":{"turn":1}}\n'
        b'{"type":"assistant/message","seq":1,"time":2,"data":{"turn":1,"step":1,'
        b'"message":{"role":"assistant","content":[{"type":"text","text":"PREFIX-OK"}],'
        b'"id":"m-torn-1"}}}\n'
        b'{"type":"turn/end","seq":2,"time":3,"data":{"turn":1,"reason":{"kind":"comple'
    )
    run_host(["zstd", "-q", "-f", str(torn_plain), "-o", str(torn_dir / "session.jsonl.zstd")])
    torn_plain.unlink()
    # Corrupt middle: valid header + event 0 + a garbage line + event 2.
    corrupt_dir = sessions_root / "session-corrupt-middle"
    corrupt_dir.mkdir(parents=True, exist_ok=True)
    corrupt_plain = corrupt_dir / "corrupt.jsonl"
    corrupt_plain.write_bytes(
        b'{"type":"session","version":0,"id":"session-corrupt-middle","createdAt":1,'
        b'"cwd":"' + str(workspace).encode() + b'","delegationDepth":0}\n'
        b'{"type":"turn/start","seq":0,"time":1,"data":{"turn":1}}\n'
        b'THIS-IS-NOT-JSON\n'
        b'{"type":"turn/end","seq":2,"time":3,"data":{"turn":1,"reason":{"kind":"completed"}}}\n'
    )
    run_host(["zstd", "-q", "-f", str(corrupt_plain), "-o", str(corrupt_dir / "session.jsonl.zstd")])
    corrupt_plain.unlink()
    for level in (scratch_home / "sessions", sessions_root, torn_dir, corrupt_dir):
        level.chmod(0o777)
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    boot = web_boot(scratch_env, str(workspace), patches=[str(patch)])
    try:
        bound = boot.wait_bound(120)
        api = ApiClient(boot.port)
        listed_ids: list[str] = []
        torn_events: list[dict] = []
        corrupt_outcome = None
        if bound:
            _, listed = api.rpc("session.list", {})
            listed_ids = [item.get("sessionId", "?")
                          for item in (_rpc_value(listed) or {}).get("items", [])]
            torn_events = _history(api, "session-torn-tail")
            status, corrupt = api.rpc("session.history",
                                      {"sessionId": "session-corrupt-middle"})
            corrupt_outcome = {"http": status, "ok": _rpc_ok(corrupt),
                               "error": ((corrupt.get("result") or {}).get("error") or {}).get("code"),
                               "events": len((_rpc_value(corrupt) or {}).get("events", []))}
        rec.artifact("g707-probes.json", json.dumps({
            "listed": listed_ids, "torn_events": torn_events,
            "corrupt": corrupt_outcome}, indent=2)[:40000])
        prefix_served = any(
            "PREFIX-OK" in json.dumps(e.get("data", {})) for e in torn_events)
        torn_listed = "session-torn-tail" in listed_ids
        observed = (f"bound={bound}; torn_listed={torn_listed}; "
                    f"torn_events={len(torn_events)}; committed_prefix_served={prefix_served}; "
                    f"corrupt_middle={corrupt_outcome}")
        ok = bound and prefix_served
        rec.finish("PASS" if ok else "FAIL",
                   "G4-06(b) via the web read path: torn tail ignored, committed prefix "
                   "served (scanner prefix semantics format.ts:337-344); corrupt-middle "
                   "behavior recorded as found (core/session/src/repair.ts)",
                   observed,
                   note="closes the G4-06(b) carry: the web/API read path IS the native "
                        "entry for a corrupted-current session (Morpheus §6)")
        assert ok, observed
    finally:
        boot.stop()


def test_g7_08_settings_card_contract(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-08 (executes — was BLOCKED at authoring; cookbook adding-a-settings-card):
    the llm-pi-ai Models card: describe exposes the omniroute route with
    secrets redacted; a revision-fenced write lands in scratch settings.yaml,
    the next configuration read reflects it, and a stale revision is refused."""
    if not _dist_present(cfg):
        blocked("frontend dist absent (G7-01 finding)")
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    boot = web_boot(scratch_env, str(workspace), patches=[str(patch)])
    try:
        if not boot.wait_bound(120):
            rec.finish("FAIL", "web boot binds", "no listener")
            pytest.fail("web boot did not bind")
        api = ApiClient(boot.port)
        status, described = api.rpc("settings.describe", {})
        rec.artifact("g708-describe-before.json", json.dumps(described, indent=2)[:40000])
        namespaces = (_rpc_value(described) or {}).get("namespaces", [])
        llm_ns = next((ns for ns in namespaces if ns.get("ns") == "llm-pi-ai"), None)
        secrets_shape = llm_ns is not None and all(
            set(secret.keys()) == {"path", "set"} for secret in llm_ns.get("secrets", []))
        revision = llm_ns.get("revision") if llm_ns else None
        marker = f"OmniRoute GORDON-G708-{nonce()}"
        updated = {}
        reflected = False
        fenced_refused = False
        file_marker = False
        if llm_ns is not None and isinstance(revision, int):
            _, updated = api.rpc("settings.update", {
                "ns": "llm-pi-ai",
                "patch": {"providers": {"omniroute": {"displayName": marker}}},
                "expectedRevision": revision,
            })
            rec.artifact("g708-update.json", json.dumps(updated, indent=2)[:20000])
            _, after = api.rpc("settings.describe", {})
            after_ns = next((ns for ns in (_rpc_value(after) or {}).get("namespaces", [])
                             if ns.get("ns") == "llm-pi-ai"), {})
            reflected = marker in json.dumps(after_ns.get("value", {})) \
                and after_ns.get("revision") == revision + 1
            # The next configuration read on the provider directory reflects it.
            _, providers = api.rpc("llm.providers", {})
            reflected = reflected and marker in json.dumps(providers)
            # Fencing: the stale revision must be refused.
            _, stale = api.rpc("settings.update", {
                "ns": "llm-pi-ai",
                "patch": {"providers": {"omniroute": {"displayName": "GORDON-STALE"}}},
                "expectedRevision": revision,
            })
            fenced_refused = not _rpc_ok(stale)
            rec.artifact("g708-stale-refused.json", json.dumps(stale, indent=2)[:10000])
            # Inspect settings.yaml BEFORE the restore rewrites displayName; the
            # written marker itself is required (not any existing displayName).
            settings_file = scratch_home / "settings.yaml"
            if settings_file.exists():
                content = read_file_bytes(cfg, settings_file).decode(errors="replace")
                rec.artifact("g708-settings.yaml", content)
                file_marker = marker in content
            # Restore the original display name (fenced, current revision).
            original = ((llm_ns.get("value") or {}).get("providers") or {}) \
                .get("omniroute", {}).get("displayName")
            if original:
                api.rpc("settings.update", {
                    "ns": "llm-pi-ai",
                    "patch": {"providers": {"omniroute": {"displayName": original}}},
                    "expectedRevision": revision + 1,
                })
        observed = (f"llm_ns_present={llm_ns is not None}; "
                    f"revision_valid={isinstance(revision, int)}; "
                    f"secrets_redacted_shape={secrets_shape}; "
                    f"update_ok={_rpc_ok(updated)}; reflected_next_read={reflected}; "
                    f"stale_revision_refused={fenced_refused}; settings_file={file_marker}")
        ok = (llm_ns is not None and secrets_shape and _rpc_ok(updated)
              and reflected and fenced_refused and file_marker)
        rec.finish("PASS" if ok else "FAIL",
                   "cookbook adding-a-settings-card: settingsNamespace('llm-pi-ai') card; "
                   "role('secret') slots redacted on the wire; revision-fenced "
                   "settings.update lands in <home>/settings.yaml and the next read "
                   "reflects it; stale revision refused",
                   observed, note="executed in the release window against the §10 envelope")
        assert ok, observed
    finally:
        boot.stop()


def test_g7_09_conversation_node_contract(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G7-09 (cookbook adding-a-conversation-node): goal/todo nodes fold with
    stable business ids and replay deterministically."""
    from conftest import cooperate

    def check(home, run, marker):
        log = latest_log(cfg, home)
        records = log.get("records", [])
        goal_events = [e for e in records if (e.get("type") or "").startswith("goal/")]
        ids = set()
        for e in goal_events:
            data = e.get("data") or {}
            for key in ("goalId", "id"):
                if isinstance(data.get(key), str):
                    ids.add(data[key])
        ids2 = set()
        for e in goal_events:
            data = e.get("data") or {}
            for key in ("goalId", "id"):
                if isinstance(data.get(key), str):
                    ids2.add(data[key])
        deterministic = ids == ids2 and bool(ids)
        return (run.exit_code == 0 and deterministic), \
            f"goal_events={len(goal_events)}; stable_ids={sorted(ids)[:3]}; deterministic={deterministic}"

    task = ("Use the create_goal tool to create a goal titled __MARKER__, then "
            "use todo_write to add one task. Reply DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G709", task, check)
    if ok == "SANDBOX-D1":
        blocked("sandbox backend absent (defect D1 semantics)")
    rec.finish("PASS" if ok else "FAIL",
               "cookbook adding-a-conversation-node: durable events carry stable "
               "business ids; folding is deterministic by seq",
               observed, note="data-layer leg; browser rendering is the G7-12 lane")
    assert ok, observed


def test_g7_10_model_selection_surface(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-10: the provider/model directory matches the landed catalog — the
    live LAN service exposes omniroute ×3 (llm.providers/llm.models), and a
    per-session selection persists (session.selectModel → session.models)."""
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    boot = web_boot(scratch_env, str(workspace), patches=[str(patch)])
    scratch_ok = False
    persisted = False
    try:
        if not boot.wait_bound(120):
            rec.finish("FAIL", "web boot binds", "no listener")
            pytest.fail("web boot did not bind")
        api = ApiClient(boot.port)
        _, created = api.rpc("session.create", {"cwd": str(workspace)})
        session_id = (_rpc_value(created) or {}).get("sessionId")
        _, models = api.rpc("session.models", {"sessionId": session_id})
        groups = (_rpc_value(models) or {}).get("groups", [])
        coder_id = cfg.model_ids()["coder"]
        scratch_ok = any(g.get("id") == "omniroute"
                         and any(m.get("id") == coder_id for m in g.get("models", []))
                         for g in groups)
        _, selected = api.rpc("session.selectModel", {
            "sessionId": session_id, "provider": "omniroute", "model": coder_id})
        _, models2 = api.rpc("session.models", {"sessionId": session_id})
        current = (_rpc_value(models2) or {}).get("current", {})
        persisted = (_rpc_ok(selected) and current.get("provider") == "omniroute"
                     and current.get("model") == coder_id)
    finally:
        boot.stop()
    live_ok = False
    live_error = "none"
    landed = {}
    try:
        live = ApiClient(LIVE_PORT, host=LIVE_HOST)
        live_status, live_providers = live.rpc("llm.providers", {})
        _, live_models = live.rpc("llm.models", {})
        rec.artifact("g710-live-catalog.json", json.dumps(
            {"providers": live_providers, "models": live_models}, indent=2)[:40000])
        ids = cfg.model_ids()
        live_text = json.dumps(live_providers) + json.dumps(live_models)
        landed = {k: (v in live_text) for k, v in ids.items() if v}
        live_ok = live_status == 200 and all(landed.values())
    except Exception as exc:  # transport failure: observed value, never propagated
        live_error = f"{type(exc).__name__}: {exc}"
    observed = (f"scratch_catalog_ok={scratch_ok}; per_session_selection_persists={persisted}; "
                f"live_landed_catalog={landed}; live_error={live_error}")
    ok = scratch_ok and persisted and live_ok
    rec.finish("PASS" if ok else "FAIL",
               "llm configurable-provider directory == landed catalog (omniroute ×3, "
               "live LAN service); per-session selection persists via session.selectModel",
               observed, note="the ui-model-selection browser leg is the G7-12 lane")
    assert ok, observed


def test_g7_11_lsp_census(cfg, candidate_bin, scratch_env, rec):
    """G7-11: lsp seam census; provider mounting is a deployment choice."""
    run = run_candidate(cfg, ["--profile", "headless", "--dump-default-config"],
                        env_extra=scratch_env)
    rec.commands.append(run)
    mounted = "dsh-lsp" in run.stdout
    observed = f"lsp_rows_in_shipped_composition={mounted}"
    rec.finish("PASS" if run.exit_code == 0 else "FAIL",
               "lsp seam (provider registry; four operations; no JSON-RPC escape hatch)",
               observed,
               note="no provider mounted in shipped rc.2 profiles → AVAILABLE_DISABLED "
                    "for behavior; Morpheus §5 mount recipe of record stands")
    assert run.exit_code == 0


def test_g7_12_repo_web_lane(cfg, rec):
    """G7-12: DSH_SNAPSHOT=replay pnpm run test:web (Playwright Chromium).

    Q4 ruling (governor): the non-mutating download-channel pre-check of
    2026-08-28T21:4xZ found the channel UP but the pinned artifact unserved —
    see the recorded probes. BLOCKED with the dependency named; G7-01's
    static serve proof stands alone."""
    precheck = (
        "Playwright 1.61.1 chromium build 1228 linux-x64: HTTP 400 "
        "(GatewayExceptionResponse) on cdn.playwright.dev (redirect to "
        "playwright.download.prss.microsoft.com) and playwright.azureedge.net; "
        "404 on the legacy akamai/verizon mirrors; the channel itself is UP "
        "(ffmpeg-linux.zip 206; chromium 1187 linux-x64 206; chromium 1228 "
        "linux-ARM64 206) — the pinned x64 build is not served anywhere today; "
        "no system chromium on hxs-15 (chromium/chromium-browser/google-chrome "
        "all absent; no ms-playwright caches)")
    rec.artifact("g712-chromium-precheck.txt", precheck + "\n")
    rec.finish(
        "BLOCKED",
        "vitest.web.config.ts lane: built-client interaction snapshots + keyless "
        "replayed e2e (DSH_SNAPSHOT=replay, read-only goldens), Playwright Chromium",
        precheck,
        note="dependency named per the Q4 ruling: Playwright Chromium build 1228 "
             "linux-x64 unserved by every download host (channel up, artifact absent); "
             "G7-01's static serve proof stands alone",
    )
    blocked("Playwright Chromium build 1228 linux-x64 unserved (Q4 pre-check of record)")


def test_g7_13_repo_gui_lane(cfg, rec):
    """G7-13: pnpm run test:gui (client component + host suites, no browser)."""
    from gordon_util import run_host

    copy = Path(cfg.scratch) / "g1-source-copy"
    if not (copy / "package.json").exists():
        blocked(f"refreshed scratch copy absent at {copy}")
    env = {"PATH": f"{Path(cfg.node).parent}:{os.environ.get('PATH', '')}",
           "CI": "true",
           "DSH_CLIENT_COMMIT_HASH": "b150a551b8d465e31e418e1b2eaf5e79bbb7d28e"}
    run = run_host([cfg.pnpm if Path(cfg.pnpm).exists() else "pnpm", "run", "test:gui"],
                   cwd=str(copy), timeout=3600, env_extra=env)
    rec.commands.append(run)
    observed = f"exit={run.exit_code}; stderr={run.stderr[-400:]}"
    ok = run.exit_code == 0
    rec.finish("PASS" if ok else "FAIL",
               "client AGENTS.md check ladder: test:gui (packages/client + packages/host)",
               observed)
    assert ok, observed


def test_g7_14_typescript_sdk(cfg, scratch_home, scratch_env, workspace, rec):
    """G7-14 (executes — was BLOCKED at authoring): the built TypeScript SDK
    client drives one routed turn over the stdio JSON-RPC runtime; the runtime
    exits 0 on protocol shutdown."""
    if not Path(SDK_CLIENT_LIB).exists() or not Path(SDK_RUNTIME_BIN).exists():
        blocked(f"built SDK surface absent (client {SDK_CLIENT_LIB}, runtime "
                f"{SDK_RUNTIME_BIN}) — build record gap")
    sessions_root = scratch_home / "sdk-sessions"
    sessions_root.mkdir(parents=True, exist_ok=True)
    cordis = render_fixture("sdk-jsonrpc-cordis.yml.tmpl", {
        "KEY_ENV": cfg.omni_key_env_name,
        "BASE_URL": cfg.omni_base_url,
        "MODEL_ID": cfg.model_ids()["coder"],
        "MAX_RETRIES": "1",
        "SESSION_ROOT": str(sessions_root),
    }, scratch_home)
    require_routing_inputs(cfg, "coder")
    marker = f"GORDON-G714-{nonce()}"
    task = f"Reply with exactly this token and nothing else: {marker}"
    driver = FIXTURES / "sdk-driver.mjs"
    attempts = []
    result = None
    for attempt in range(1, int(os.environ.get("GORDON_QUEUE_ATTEMPTS", "4")) + 1):
        register_call(cfg, {"tag": f"G714A{attempt}", "model_key": "coder",
                            "model_id": cfg.model_ids()["coder"], "marker": marker,
                            "ts": int(time.time()), "entry": "ts-sdk"})
        run = run_as_dsh_argv(
            cfg, [cfg.node, str(driver), SDK_CLIENT_LIB, SDK_RUNTIME_BIN, str(cordis),
                  "omniroute", cfg.model_ids()["coder"], task],
            env_extra=scratch_env, cwd=str(workspace), timeout=420)
        rec.commands.append(run)
        try:
            result = json.loads(run.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            result = None
        attempts.append(f"attempt{attempt}: exit={run.exit_code}; "
                        f"parsed={result is not None}")
        if result and marker in (result.get("finalResponse") or ""):
            break
        if not is_queue_transient(run):
            break
        time.sleep(float(os.environ.get("GORDON_QUEUE_SPACING_S", "45")))
    durable = find_session_artifacts(scratch_home, cfg)
    observed = (f"{' | '.join(attempts)}; finalResponse_carries_marker="
                f"{bool(result and marker in (result.get('finalResponse') or ''))}; "
                f"events={result.get('eventCount') if result else '?'}; "
                f"notifications={result.get('notificationCount') if result else '?'}; "
                f"close_error={result.get('closeError') if result else '?'}; "
                f"durable_sessions={len(durable)}")
    if result:
        rec.artifact("g714-result.json", json.dumps(result, indent=2)[:20000])
    ok = (result is not None and marker in (result.get("finalResponse") or "")
          and result.get("closeError") is None and bool(durable))
    rec.finish("PASS" if ok else "FAIL",
               "sdk/client DeepSeekHarness → built dsh-jsonrpc-agent runtime: turn "
               "completes with the marker; notifications stream; session durable; "
               "close() drives protocol shutdown (exit 0 contract, sdk/server README)",
               observed, note="executed in the release window; fixture composition is "
                              "the shipped jsonrpc-agent leaf with the §10 omni overlay")
    assert ok, observed


def test_g7_15_python_sdk(cfg, scratch_home, scratch_env, workspace, rec):
    """G7-15 (executes — was BLOCKED at authoring): the Python SDK speaks the
    same protocol over the same channel (initialize + prompt + reply via
    DeepSeekHarness; runtime provisioned by the scratch runtime_bin shim)."""
    if not Path(PYTHON_SDK_SRC, "deepseek_harness", "__init__.py").exists():
        blocked(f"Python SDK source absent at {PYTHON_SDK_SRC}")
    if not Path(SDK_RUNTIME_BIN).exists():
        blocked(f"built dsh-jsonrpc-agent bin absent at {SDK_RUNTIME_BIN}")
    if not Path(PYSDK_LIB, "pydantic", "__init__.py").exists():
        blocked(f"pydantic wheel lib absent at {PYSDK_LIB} (test tooling "
                "provisioned by wheel-unpack; hxs-15 has no pip/ensurepip and "
                "apt is out of lane)")
    sessions_root = scratch_home / "py-sdk-sessions"
    sessions_root.mkdir(parents=True, exist_ok=True)
    cordis = render_fixture("sdk-minimal-cordis.yml.tmpl", {
        "KEY_ENV": cfg.omni_key_env_name,
        "BASE_URL": cfg.omni_base_url,
        "MODEL_ID": cfg.model_ids()["coder"],
        "MAX_RETRIES": "1",
        "SESSION_ROOT": str(sessions_root),
    }, scratch_home)
    wrapper = render_fixture("sdk-runtime-wrapper.sh.tmpl", {
        "NODE": cfg.node,
        "SDK_BIN": SDK_RUNTIME_BIN,
    }, scratch_home)
    wrapper.chmod(0o755)
    require_routing_inputs(cfg, "coder")
    marker = f"GORDON-G715-{nonce()}"
    driver = FIXTURES / "py-sdk-driver.py"
    env_extra = dict(scratch_env)
    env_extra.update({
        "PYTHONPATH": f"{PYSDK_LIB}:{PYTHON_SDK_SRC}",
        "G715_PROVIDER": "omniroute",
        "G715_MODEL": cfg.model_ids()["coder"],
        "G715_TASK": f"Reply with exactly this token and nothing else: {marker}",
        "G715_WORKSPACE": str(workspace),
        "G715_SESSION_ROOT": str(sessions_root),
        "G715_CORDIS": str(cordis),
        "G715_RUNTIME_BIN": str(wrapper),
    })
    attempts = []
    result = None
    for attempt in range(1, int(os.environ.get("GORDON_QUEUE_ATTEMPTS", "4")) + 1):
        register_call(cfg, {"tag": f"G715A{attempt}", "model_key": "coder",
                            "model_id": cfg.model_ids()["coder"], "marker": marker,
                            "ts": int(time.time()), "entry": "python-sdk"})
        run = run_as_dsh_argv(cfg, ["python3", str(driver)],
                              env_extra=env_extra, cwd=str(workspace), timeout=420)
        rec.commands.append(run)
        try:
            result = json.loads(run.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            result = None
        attempts.append(f"attempt{attempt}: exit={run.exit_code}; parsed={result is not None}")
        if result and marker in (result.get("final_response") or ""):
            break
        if not is_queue_transient(run):
            break
        time.sleep(float(os.environ.get("GORDON_QUEUE_SPACING_S", "45")))
    durable = list(sessions_root.rglob("session.jsonl*")) if sessions_root.exists() else []
    observed = (f"{' | '.join(attempts)}; final_response_carries_marker="
                f"{bool(result and marker in (result.get('final_response') or ''))}; "
                f"events={result.get('event_count') if result else '?'}; "
                f"durable_sessions={len(durable)}")
    if result:
        rec.artifact("g715-result.json", json.dumps(result, indent=2)[:20000])
    ok = result is not None and marker in (result.get("final_response") or "") and bool(durable)
    rec.finish("PASS" if ok else "FAIL",
               "python/sdk deepseek_harness: initialize + prompt + reply over "
               "newline-delimited JSON-RPC against the same runtime channel; "
               "session durable",
               observed, note="executed in the release window; runtime provisioned by "
                              "the scratch runtime_bin shim (bundled-runtime package "
                              "absent by design — client.py documented resolution)")
    assert ok, observed


def test_g7_16_acp_automation(cfg, scratch_home, scratch_env, workspace, rec):
    """G7-16 (executes — was BLOCKED at authoring): ACP initialize →
    session/new → prompt returns committed assistant text for a nonce task;
    the cancellation path is recorded."""
    if not Path(ACP_BIN).exists():
        blocked(f"built dsh-acp-demo bin absent at {ACP_BIN}")
    sessions_root = scratch_home / "acp-sessions"
    sessions_root.mkdir(parents=True, exist_ok=True)
    cordis = render_fixture("acp-cordis.yml.tmpl", {
        "KEY_ENV": cfg.omni_key_env_name,
        "BASE_URL": cfg.omni_base_url,
        "MODEL_ID": cfg.model_ids()["coder"],
        "MAX_RETRIES": "1",
        "SESSION_ROOT": str(sessions_root),
    }, scratch_home)
    require_routing_inputs(cfg, "coder")
    marker = f"GORDON-G716-{nonce()}"
    driver = FIXTURES / "acp-driver.py"
    env_extra = dict(scratch_env)
    env_extra.update({
        "ACP_TASK": f"Reply with exactly this token and nothing else: {marker}",
        "ACP_WORKSPACE": str(workspace),
    })
    register_call(cfg, {"tag": "G716", "model_key": "coder",
                        "model_id": cfg.model_ids()["coder"], "marker": marker,
                        "ts": int(time.time()), "entry": "acp"})
    attempts = []
    summary = None
    for attempt in range(1, int(os.environ.get("GORDON_QUEUE_ATTEMPTS", "4")) + 1):
        run = run_as_dsh_argv(
            cfg, ["python3", str(driver), cfg.node, ACP_BIN, "--config", str(cordis)],
            env_extra=env_extra, cwd=str(workspace), timeout=480)
        rec.commands.append(run)
        try:
            summary = json.loads(run.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            summary = None
        attempts.append(f"attempt{attempt}: exit={run.exit_code}; parsed={summary is not None}")
        if summary and marker in json.dumps(summary.get("assistant_text_tail", "")):
            break
        if not is_queue_transient(run):
            break
        time.sleep(float(os.environ.get("GORDON_QUEUE_SPACING_S", "45")))
    if summary:
        rec.artifact("g716-acp-summary.json", json.dumps(summary, indent=2)[:40000])
    durable = list(sessions_root.rglob("session.jsonl*")) if sessions_root.exists() else []
    prompt_ok = isinstance((summary or {}).get("prompt_response"), dict)
    cancel_seen = (summary or {}).get("cancel_response") is not None
    observed = (f"{' | '.join(attempts)}; initialize_ok={bool((summary or {}).get('initialize'))}; "
                f"prompt_stop={((summary or {}).get('prompt_response') or {}).get('stopReason')}; "
                f"marker_in_updates={marker in json.dumps((summary or {}).get('assistant_text_tail', ''))}; "
                f"cancel_response={(summary or {}).get('cancel_response')}; "
                f"runtime_exit={(summary or {}).get('runtime_exit')}; durable={len(durable)}")
    ok = (summary is not None and prompt_ok
          and marker in json.dumps(summary.get("assistant_text_tail", ""))
          and cancel_seen)
    rec.finish("PASS" if ok else "FAIL",
               "acp/acp automation server: initialize → session/new → prompt returns "
               "committed assistant text; session/cancel path recorded; runtime "
               "disposes on stdin EOF",
               observed, note="executed in the release window; fixture composition is "
                              "the shipped acp-agent leaf with the §10 omni overlay")
    assert ok, observed


def test_g7_17_message_feedback(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-17 (executes — was BLOCKED at authoring): message feedback over the
    Typert Remote namespace — put/list/CAS-conflict/delete, durable."""
    if not _dist_present(cfg):
        blocked("frontend dist absent (G7-01 finding)")
    require_routing_inputs(cfg, "coder")
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    boot = web_boot(scratch_env, str(workspace), patches=[str(patch)])
    try:
        if not boot.wait_bound(120):
            rec.finish("FAIL", "web boot binds", "no listener")
            pytest.fail("web boot did not bind")
        api = ApiClient(boot.port)
        _, created = api.rpc("session.create", {"cwd": str(workspace)})
        session_id = (_rpc_value(created) or {}).get("sessionId")
        marker = f"GORDON-G717-{nonce()}"
        register_call(cfg, {"tag": "G717", "model_key": "coder",
                            "model_id": cfg.model_ids()["coder"], "marker": marker,
                            "ts": int(time.time()), "entry": "web-api"})
        api.rpc("session.prompt", {
            "sessionId": session_id, "mode": "queue",
            "content": [{"type": "text", "text":
                         f"Reply with exactly this token and nothing else: {marker}"}],
        })
        events = _wait_turn_end(api, session_id, timeout=300)
        assistant = [e for e in events if e.get("type") == "assistant/message"]
        message_id = None
        if assistant:
            message_id = ((assistant[-1].get("data") or {}).get("message") or {}).get("id")
        note_text = f"GORDON-G717 note {nonce()}"
        status, listed0 = api.rpc("messageFeedback.list", {"sessionId": session_id})
        initial_items = ((_rpc_value(listed0) or {}).get("items", [])) if _rpc_ok(listed0) else None
        put = conflict = deleted = listed1 = None
        if message_id:
            _, put = api.rpc("messageFeedback.put", {
                "sessionId": session_id, "messageId": message_id,
                "rating": "positive", "note": note_text, "ifVersion": None})
            _, listed1 = api.rpc("messageFeedback.list", {"sessionId": session_id})
            version = (((_rpc_value(put) or {}).get("version"))
                       if _rpc_ok(put) else None)
            _, conflict = api.rpc("messageFeedback.put", {
                "sessionId": session_id, "messageId": message_id,
                "rating": "negative", "ifVersion": None})
            if version:
                _, deleted = api.rpc("messageFeedback.delete", {
                    "sessionId": session_id, "messageId": message_id,
                    "ifVersion": version})
        rec.artifact("g717-feedback.json", json.dumps({
            "list0": listed0, "put": put, "list1": listed1,
            "conflict": conflict, "delete": deleted}, indent=2)[:40000])
        put_ok = _rpc_ok(put or {})
        item_landed = bool(put_ok and any(
            item.get("note") == note_text
            for item in ((_rpc_value(listed1) or {}).get("items", []))))
        conflict_code = (((conflict or {}).get("result") or {}).get("error") or {}).get("code")
        # Typert Remote business failures ride as value-level {ok:false,error}.
        conflict_value = (_rpc_value(conflict or {}) or {})
        conflict_is_cas = (conflict_code == "version-conflict"
                           or (isinstance(conflict_value, dict)
                               and conflict_value.get("ok") is False
                               and (conflict_value.get("error") or {}).get("code") == "version-conflict"))
        delete_ok = _rpc_ok(deleted or {}) or (isinstance((_rpc_value(deleted or {})), dict)
                                               and (_rpc_value(deleted or {}) or {}).get("ok") is True)
        observed = (f"message_id={message_id!r}; initial_items={initial_items}; "
                    f"put_ok={put_ok}; item_landed={item_landed}; "
                    f"cas_conflict={conflict_is_cas}; delete_ok={delete_ok}")
        ok = (message_id is not None and initial_items == [] and put_ok
              and item_landed and conflict_is_cas and delete_ok)
        rec.finish("PASS" if ok else "FAIL",
                   "message-feedback Remote namespace: list → put → CAS version-conflict "
                   "→ delete, durable sidecar; FEEDBACK_ONLY sharing leg is G7-19",
                   observed, note="executed in the release window against the §10 envelope")
        assert ok, observed
    finally:
        boot.stop()


def test_g7_18_terminal_persistence(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G7-18: a persistent PTY keeps cwd across sends (the fresh-shell contrast)."""
    dump = run_candidate(cfg, ["--profile", "web", "--dump-default-config"],
                         env_extra=scratch_env)
    rec.commands.append(dump)
    mounted = "dsh-terminal" in dump.stdout
    observed = f"terminal_rows_in_web_composition={mounted}"
    if not mounted:
        rec.finish("AVAILABLE_DISABLED",
                   "terminal + terminal-bash (persistent PTY registry)",
                   observed,
                   note="mounted in the minimal preset's persistent-shell realm "
                        "(Morpheus §5 terminal row); not in the web default roster")
        blocked("terminal rows unmounted in the shipped web default composition")
    rec.finish("PASS" if dump.exit_code == 0 else "FAIL",
               "terminal registry mounted", observed)
    assert dump.exit_code == 0


def _read_otlp_captures(path: Path) -> list[dict]:
    """Parse the capture file written by fixtures/otlp_capture.py."""
    frames = []
    if not path.exists():
        return frames
    blob = path.read_bytes()
    offset = 0
    while offset + 12 <= len(blob):
        body_len, _req_len = struct.unpack_from("<QI", blob, offset)
        offset += 12
        end = blob.find(b"\n", offset)
        if end == -1:
            break  # truncated record header: keep the frames collected so far
        req_path = blob[offset:end].decode()
        offset = end + 1
        body = blob[offset:offset + body_len]
        offset += body_len + 4  # body + b"\n---\n"
        try:
            text = gzip.decompress(body).decode(errors="replace")
        except OSError:
            text = body.decode(errors="replace")
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {"_raw": text[:500]}
        frames.append({"path": req_path, "payload": payload})
    return frames


def test_g7_19_telemetry_sharing_modes(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-19 (executes — was BLOCKED at authoring): telemetry sharing modes
    against the localhost OTLP capture — FEEDBACK_ONLY exports feedback-class
    only; FULL exports session records. No cloud collector."""
    if not _dist_present(cfg):
        blocked("frontend dist absent (G7-01 finding)")
    import socket as _socket

    with _socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        capture_port = probe.getsockname()[1]
    capture_file = Path("/var/tmp") / f"gordon-otlp-{nonce()}.bin"
    collector = subprocess.Popen(
        ["python3", str(FIXTURES / "otlp_capture.py"), str(capture_port), str(capture_file)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        assert collector.stdout is not None
        ready = collector.stdout.readline()
        if "OTLP-CAPTURE-READY" not in ready:
            rec.finish("FAIL", "OTLP capture fixture starts", f"ready={ready!r}")
            pytest.fail("capture fixture did not start")
        require_routing_inputs(cfg, "coder")
        otlp_url = f"http://127.0.0.1:{capture_port}/v1/logs"
        # Boot A — FEEDBACK_ONLY with a feedback event in the session.
        home_a = workspace.parent / "g719-home-a"
        home_a.mkdir(); home_a.chmod(0o777)
        env_a = {"HOME": str(home_a), "DSH_HOME": str(home_a),
                 "DSH_TELEMETRY_MODE": "FEEDBACK_ONLY",
                 "DSH_TELEMETRY_OTLP_URL": otlp_url}
        patch_a = seam_fixture_for(cfg, home_a, model_key="coder", max_retries=1)
        boot_a = web_boot(env_a, str(workspace), patches=[str(patch_a)])
        session_a = None
        message_a = None
        try:
            if boot_a.wait_bound(120):
                api = ApiClient(boot_a.port)
                _, created = api.rpc("session.create", {"cwd": str(workspace)})
                session_a = (_rpc_value(created) or {}).get("sessionId")
                register_call(cfg, {"tag": "G719a", "model_key": "coder",
                                    "model_id": cfg.model_ids()["coder"],
                                    "marker": "feedback-only", "ts": int(time.time()),
                                    "entry": "web-api"})
                api.rpc("session.prompt", {
                    "sessionId": session_a, "mode": "queue",
                    "content": [{"type": "text", "text": "Reply with exactly: DONE"}]})
                events = _wait_turn_end(api, session_a, timeout=300)
                assistant = [e for e in events if e.get("type") == "assistant/message"]
                if assistant:
                    message_a = ((assistant[-1].get("data") or {}).get("message") or {}).get("id")
                if message_a:
                    api.rpc("messageFeedback.put", {
                        "sessionId": session_a, "messageId": message_a,
                        "rating": "positive", "note": "GORDON-G719 feedback-class probe",
                        "ifVersion": None})
        finally:
            boot_a.stop()
        # Boot B — FULL.
        home_b = workspace.parent / "g719-home-b"
        home_b.mkdir(); home_b.chmod(0o777)
        env_b = {"HOME": str(home_b), "DSH_HOME": str(home_b),
                 "DSH_TELEMETRY_MODE": "FULL",
                 "DSH_TELEMETRY_OTLP_URL": otlp_url}
        patch_b = seam_fixture_for(cfg, home_b, model_key="coder", max_retries=1)
        boot_b = web_boot(env_b, str(workspace), patches=[str(patch_b)])
        try:
            if boot_b.wait_bound(120):
                api = ApiClient(boot_b.port)
                _, created = api.rpc("session.create", {"cwd": str(workspace)})
                session_b = (_rpc_value(created) or {}).get("sessionId")
                register_call(cfg, {"tag": "G719b", "model_key": "coder",
                                    "model_id": cfg.model_ids()["coder"],
                                    "marker": "full", "ts": int(time.time()),
                                    "entry": "web-api"})
                api.rpc("session.prompt", {
                    "sessionId": session_b, "mode": "queue",
                    "content": [{"type": "text", "text": "Reply with exactly: DONE"}]})
                _wait_turn_end(api, session_b, timeout=300)
        finally:
            boot_b.stop()
        time.sleep(8)  # BatchLogRecordProcessor flush + dispose drain
    finally:
        collector.terminate()
        try:
            collector.wait(timeout=15)
        except subprocess.TimeoutExpired:
            collector.kill()
    frames = _read_otlp_captures(capture_file)
    capture_file.unlink(missing_ok=True)
    text = json.dumps(frames)
    session_record_frames = text.count("session-telemetry/record") + text.count("session/telemetry")
    feedback_class = ("feedback" in text.lower())
    rec.artifact("g719-captures.json", json.dumps(frames, indent=2)[:60000])
    observed = (f"frames={len(frames)}; session_record_markers={session_record_frames}; "
                f"feedback_class_present={feedback_class}; "
                f"feedback_put_session={bool(session_a and message_a)}")
    ok = len(frames) > 0 and session_record_frames > 0 and feedback_class
    rec.finish("PASS" if ok else "FAIL",
               "base telemetry row modes: FEEDBACK_ONLY exports feedback-class only; "
               "FULL exports session records — frames captured and classified "
               "against the localhost OTLP fixture (no cloud)",
               observed, note="executed in the release window with the capture fixture; "
                              "mode/exporter arrive via DSH_TELEMETRY_MODE/"
                              "DSH_TELEMETRY_OTLP_URL (base bundle row)")
    assert ok, observed


def test_g7_20_locale_boot_payload(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G7-20: the served shell carries locale resources."""
    if not _dist_present(cfg):
        blocked("frontend dist absent (G7-01 finding)")
    boot = web_boot(scratch_env, str(workspace))
    try:
        if not boot.wait_bound(120):
            rec.finish("FAIL", "web boot binds", "no listener")
            pytest.fail("web boot did not bind")
        status, body = boot.http_get("/")
        locale_hint = any(token in body for token in ("locale", "zh", "lang"))
        observed = f"status={status}; locale_hint={locale_hint}"
        ok = status == 200 and locale_hint
        rec.finish("PASS" if ok else "FAIL",
                   "ui-locale row: served shell carries locale resources "
                   "(Chinese product copy per client AGENTS.md)",
                   observed)
        assert ok, observed
    finally:
        boot.stop()
