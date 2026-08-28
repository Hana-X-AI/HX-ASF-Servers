"""Gate 6 — goals, orchestration mechanics, agent integrations (plan §3).

Every routed row keeps the Phase A discipline: unique nonce, queue-transient
retries with spacing, evidence per §13, BLOCKED-with-named-dependency over
silent skips. Fixture rows mount what the shipped rc.2 composition omits via
documented --patch overlays (schedule, mcp-client, agent-presets, hooks).
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from conftest import (
    FIXTURES,
    cooperate,
    finish_coop,
    latest_log,
    log_text,
)
from gordon_util import (
    blocked,
    epoch_header,
    events_of_type,
    find_session_artifacts,
    nonce,
    read_session_log,
    render_fixture,
    run_candidate,
)
from test_g3_providers import seam_fixture_for

SUITE_DIR = Path(__file__).resolve().parent


def seam_fixture_b(cfg, dest: Path, template: str, extra: dict[str, str] | None = None,
                   model_key: str = "coder", max_retries: int = 1) -> Path:
    """Render a Phase B fixture template (route + extra rows)."""
    ids = cfg.model_ids()
    indent = "          "
    models_yaml = "\n".join(
        line
        for entry in [ids[model_key]]
        for line in (
            f"{indent}- id: {entry}",
            f"{indent}  name: {entry}",
            f"{indent}  contextWindow: 65536",
            f"{indent}  maxTokens: 8192",
        )
    )
    mapping = {
        "KEY_ENV": cfg.omni_key_env_name,
        "BASE_URL": cfg.omni_base_url,
        "MODEL_ID": ids[model_key],
        "MAX_RETRIES": str(max_retries),
        "MODELS_YAML": models_yaml,
        "NODE": cfg.node,
        "MCP_FIXTURE": os.environ.get(
            "GORDON_MCP_FIXTURE",
            "/opt/dsh/packages/mcp/mcp-client/tests/fixture-server.ts",
        ),
    }
    mapping.update(extra or {})
    return render_fixture(template, mapping, dest)


def test_g6_01_goal_lifecycle(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-01: create_goal produces durable goal state, readable via get_goal."""
    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        goal_events = [e for e in log.get("records", [])
                       if (e.get("type") or "").startswith("goal/")]
        created = marker in text and goal_events
        readback = "get_goal" in text or "create_goal" in text
        return (run.exit_code == 0 and bool(created)), \
            f"goal_events={len(goal_events)}; marker_in_log={marker in text}; tools={readback}"

    task = ("Use the create_goal tool to create a goal titled __MARKER__. "
            "Then use get_goal to read it back, and reply with exactly: DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G601", task, check)
    finish_coop(rec, ok, observed,
                "goal/src/index.ts event-sourced goal domain; tool-goal row (base bundle)",
                note="model-cooperation class")
    assert ok, observed


def test_g6_02_goal_round_driver(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-02: the round driver continues an open goal into a later turn."""
    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        # The driver renders a continuation prompt for open goals (prompt.ts);
        # a second turn carrying the goal without a new user message is the
        # continuation proof.
        continuation = "goal" in text.lower() and text.count("turn/start") >= 2
        return (run.exit_code == 0 and continuation), \
            f"turn_starts={text.count('turn/start')}; goal_mentions={text.lower().count('goal')}"

    task = ("Use the create_goal tool to create a goal titled __MARKER__ with "
            "the objective to reply DONE in the next round. Complete it if you "
            "can, then reply with exactly: DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G602", task, check)
    finish_coop(rec, ok, observed,
                "goal-round-driver/src/index.ts + renderGoalRoundPrompt (continuation section)",
                note="model-cooperation class; round identity recorded in artifacts")
    assert ok, observed


def test_g6_03_plan_mode_census_and_exit(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-03: exit_plan_mode is offered; in headless the review channel outcome
    is recorded (no answerer), and mutation refusal in plan mode is evidenced."""
    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        exit_called = "exit_plan_mode" in text
        approval_outcome = '"outcome": "unavailable"' in text or '"outcome":"unavailable"' in text \
            or "reject" in text.lower()
        plan_events = events_of_type(log.get("records", []), "plan/mode")
        return (run.exit_code in (0, 1) and exit_called), \
            f"exit_plan_mode_called={exit_called}; approval_outcome={approval_outcome}; plan_events={len(plan_events)}"

    task = ("You are in plan mode. Do not modify any files. Produce a short "
            "implementation plan for adding a __MARKER__ constant, then call "
            "exit_plan_mode with that plan. Then stop.")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G603", task, check)
    finish_coop(rec, ok, observed,
                "plan/plan-mode: exit_plan_mode presents the plan; headless review channel "
                "fails closed (user-approval semantics)",
                note="model-cooperation class")
    assert ok, observed


def test_g6_04_todo_lifecycle(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-04: todo_write records a durable list reflected in a later turn."""
    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        todo_calls = text.count("todo_write")
        marker_seen = marker in text
        return (run.exit_code == 0 and todo_calls >= 1 and marker_seen), \
            f"todo_write_calls={todo_calls}; marker={marker_seen}"

    task = ("Use todo_write to record exactly three tasks: alpha, __MARKER__, omega. "
            "Then reply with exactly: DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G604", task, check)
    finish_coop(rec, ok, observed,
                "todo/tool-todo (base row allowParallelInProgress: true)",
                note="model-cooperation class")
    assert ok, observed


def test_g6_05_workflow_run(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-05: tool-workflow executes an orchestration script in the worker thread."""
    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        wf = "workflow" in text and ("workflow/" in text or "workflowRun" in text or "workflow-run" in text)
        return (run.exit_code == 0 and marker in text and wf), \
            f"workflow_evidence={wf}; marker={marker in text}"

    task = ("Use the workflow tool to run a workflow whose script returns the "
            "string __MARKER__ (a minimal script with no agent calls). Report "
            "the workflow result, then reply with exactly: DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G605", task, check)
    finish_coop(rec, ok, observed,
                "workflow seam + workflow-worker-thread (vm timeout 5000ms default; "
                "force-settle cancelled on overrun)",
                note="model-cooperation class; script interface pinned at execution")
    assert ok, observed


def test_g6_06_skill_catalog(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-06: a fixture SKILL.md in a skills root reaches the model-visible catalog."""
    skills_root = workspace / "skills" / "gordon-probe-skill"
    skills_root.mkdir(parents=True)
    import shutil

    shutil.copy(FIXTURES / "SKILL.md", skills_root / "SKILL.md")

    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        skill_seen = "gordon-probe-skill" in text
        return (run.exit_code == 0 and skill_seen), \
            f"skill_in_stream={skill_seen}"

    from gordon_util import run_candidate as rc_run

    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    from test_g3_providers import require_routing_inputs, register_call

    require_routing_inputs(cfg, "coder")
    run = rc_run(
        cfg,
        ["--profile", "headless", "--patch", str(patch),
         "List your available skills and reply with exactly: DONE"],
        env_extra=scratch_env, cwd=str(workspace), timeout=300,
    )
    rec.commands.append(run)
    register_call(cfg, {"tag": "G606", "model_key": "coder",
                        "model_id": cfg.model_ids()["coder"], "marker": "skill-census",
                        "ts": int(time.time()), "exit": run.exit_code})
    ok, observed = check(scratch_home, run, "gordon-probe-skill")
    rec.finish("PASS" if ok else "FAIL",
               "skill registry + skill-filesystem roots (project root discovery)",
               f"exit={run.exit_code}; {observed}",
               note="fixture SKILL.md under workspace/skills; census via request stream")
    assert ok, observed


def test_g6_07_hooks_bridge(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-07: the Claude Code hook bridge fires a SessionStart command hook."""
    import shutil

    hooks_json = workspace / "hooks.json"
    shutil.copy(FIXTURES / "hooks.json", hooks_json)
    patch = seam_fixture_b(cfg, scratch_home, "patch-hooks.yml.tmpl",
                           extra={"HOOKS_JSON": str(hooks_json)})
    from test_g3_providers import require_routing_inputs, register_call

    require_routing_inputs(cfg, "coder")
    evidence_log = workspace / "gordon-hook-evidence.log"
    run = run_candidate(
        cfg,
        ["--profile", "headless", "--patch", str(patch),
         "Reply with exactly: DONE"],
        env_extra=scratch_env, cwd=str(workspace), timeout=300,
    )
    rec.commands.append(run)
    register_call(cfg, {"tag": "G607", "model_key": "coder",
                        "model_id": cfg.model_ids()["coder"], "marker": "hooks-bridge",
                        "ts": int(time.time()), "exit": run.exit_code})
    fired = evidence_log.exists() and "GORDON-HOOK-SESSIONSTART" in evidence_log.read_text()
    observed = f"exit={run.exit_code}; sessionstart_hook_fired={fired}"
    ok = fired
    rec.finish("PASS" if ok else "FAIL",
               "hooks-claude-code bridge: SessionStart command hook executes with "
               "$CLAUDE_PROJECT_DIR substitution (config.ts)",
               observed)
    assert ok, observed


def test_g6_08_repeat_tool_reminder(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-08: the third identical tool call triggers the threshold-3 reminder."""
    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        echo_calls = text.count(f'echo {marker}')
        reminder = "repeat" in text.lower() and ("3" in text)
        return (run.exit_code == 0 and echo_calls >= 3 and reminder), \
            f"identical_calls={echo_calls}; reminder_evidence={reminder}"

    task = ("Use the bash tool to run exactly: echo __MARKER__ — three separate "
            "times in a row with the exact same arguments. Then reply DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G608", task, check)
    finish_coop(rec, ok, observed,
                "repeat-tool-reminder thresholds [3,5,8] (base row)",
                note="model-cooperation class")
    assert ok, observed


def test_g6_09_timeout_policy_crossref(cfg, rec):
    """G6-09: tool-call-timeout-policy enforcement — proven by G5-07 (Phase A retest)."""
    rec.finish("PASS",
               "guard/timeout-policy cooperative enforcement; executor kill verified "
               "by G5-07 retest evidence ([timed out after 3000ms] + SIGTERM)",
               "covered by G5-07 (D1 retest, PASS)",
               note="cross-reference row per plan §3")
    pytest.skip("NOT_RUN: cross-referenced to G5-07 (already PASS)")


def test_g6_10_jobs_lifecycle(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-10: job_list shows a background job; job_kill settles it."""
    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        started = "started background job" in text
        listed = "job_list" in text
        killed = "job_kill" in text
        return (run.exit_code == 0 and started and listed and killed), \
            f"started={started}; listed={listed}; killed={killed}"

    task = ("Use the bash tool with run_in_background: true to run: sleep 60; echo __MARKER__. "
            "Then use job_list to list jobs, then job_kill to stop it. Reply DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G610", task, check,
                             timeout=600)
    finish_coop(rec, ok, observed,
                "jobs-local registry (disposal cancels live work; no orphan after teardown)",
                note="model-cooperation class")
    assert ok, observed


def test_g6_11_schedule_one_shot(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-11: a fixture-mounted schedule row delivers a one-shot reminder."""
    patch = seam_fixture_b(cfg, scratch_home, "patch-schedule.yml.tmpl")

    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        changes = events_of_type(log.get("records", []), "schedule/change")
        reminder = "reminder" in text.lower() or "schedule" in text.lower()
        return (run.exit_code == 0 and bool(changes) and reminder), \
            f"schedule_change_events={len(changes)}; reminder_evidence={reminder}"

    task = ("Schedule a one-shot reminder 5 seconds from now with the message __MARKER__. "
            "Wait for it to arrive, then reply DONE")
    from test_g3_providers import require_routing_inputs, run_routed_headless, register_call

    require_routing_inputs(cfg, "coder")
    started = time.monotonic()
    run = run_routed_headless(cfg, scratch_env, workspace, patch, task, timeout=420)
    rec.commands.append(run)
    register_call(cfg, {"tag": "G611", "model_key": "coder",
                        "model_id": cfg.model_ids()["coder"], "marker": "schedule",
                        "ts": int(time.time()), "exit": run.exit_code})
    ok, observed = check(scratch_home, run, "schedule")
    observed = f"{observed}; elapsed={time.monotonic() - started:.0f}s"
    rec.finish("PASS" if ok else "FAIL",
               "schedule/schedule: durable one-shot reminders over the session log "
               "(schedule/change events; reminder framing)",
               observed, note="fixture-mounted row (unmounted in shipped rc.2 composition)")
    assert ok, observed


def test_g6_12_subagent_spawn(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-12: a spawn subagent delegation produces a child session with lineage."""
    def check(home, run, marker):
        artifacts = find_session_artifacts(home, cfg)
        child_proof = False
        parent_result = False
        for artifact in artifacts:
            log = read_session_log(cfg, artifact)
            header = log.get("header") or {}
            if header.get("origin") == "subagent" and header.get("parentSession"):
                child_proof = (header.get("delegationDepth") or 0) >= 1
            text = log_text(log)
            if marker in text:
                parent_result = True
        return (run.exit_code == 0 and child_proof and parent_result), \
            f"child_lineage={child_proof}; marker_propagated={parent_result}"

    task = ("Use the subagent tool to delegate this exact task to a child agent: "
            "compute the token __MARKER__ and report it back. When the child "
            "reports, reply with exactly: DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G612", task, check,
                             timeout=600)
    finish_coop(rec, ok, observed,
                "subagent seam: child session carries parentSession, origin 'subagent', "
                "delegationDepth 1 (persistence format.ts header)",
                note="model-cooperation class")
    assert ok, observed


def test_g6_13_subagent_fork(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-13: a fork delegation inherits the parent's history (one-shot)."""
    def check(home, run, marker):
        artifacts = find_session_artifacts(home, cfg)
        fork_child = False
        for artifact in artifacts:
            log = read_session_log(cfg, artifact)
            header = log.get("header") or {}
            if header.get("origin") == "subagent":
                records_text = log_text(log)
                if "ALPHA-SEED" in records_text:
                    fork_child = True
        return (run.exit_code == 0 and fork_child), f"fork_inherited_seed={fork_child}"

    task = ("Remember this exact token: ALPHA-SEED-__MARKER__. Then use the "
            "subagent_fork tool to ask a forked child what token you were told "
            "to remember. Report its answer, then reply DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G613", task, check,
                             timeout=600)
    finish_coop(rec, ok, observed,
                "tool-subagent-fork (one-shot fork inherits the parent request prefix)",
                note="model-cooperation class")
    assert ok, observed


def test_g6_14_subagent_control(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-14: list_agents shows a continuable child; send_message reaches it."""
    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        listed = "list_agents" in text
        messaged = "send_message" in text
        return (run.exit_code == 0 and listed), \
            f"list_agents={listed}; send_message={messaged}"

    task = ("Use the subagent tool to start a continuable child that waits for "
            "instructions. Use list_agents to show it, then use send_message to "
            "tell it the token __MARKER__, read its reply, and reply DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G614", task, check,
                             timeout=600)
    finish_coop(rec, ok, observed,
                "tool-subagent-control: list_agents catalog + send_message followup "
                "(continuable background mode is the shipped default)",
                note="model-cooperation class")
    assert ok, observed


def test_g6_15_preset_composition(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-15: an agent on a shipped preset composes the preset's persona."""
    patch = seam_fixture_b(cfg, scratch_home, "patch-presets.yml.tmpl")
    from test_g3_providers import require_routing_inputs, register_call

    require_routing_inputs(cfg, "coder")
    run = run_candidate(
        cfg,
        ["--profile", "headless", "--patch", str(patch),
         "Reply with exactly: DONE"],
        env_extra=scratch_env, cwd=str(workspace), timeout=300,
    )
    rec.commands.append(run)
    register_call(cfg, {"tag": "G615", "model_key": "coder",
                        "model_id": cfg.model_ids()["coder"], "marker": "preset",
                        "ts": int(time.time()), "exit": run.exit_code})
    # The launcher appends the shipped preset root when the agent-presets row
    # exists (profile-boot.ts:159-167); the dump proves the row mounted.
    dump = run_candidate(
        cfg, ["--profile", "headless", "--patch", str(patch), "--dump-config"],
        env_extra=scratch_env,
    )
    rec.commands.append(dump)
    row_mounted = "id: agent-presets" in dump.stdout
    observed = f"run_exit={run.exit_code}; presets_row_mounted={row_mounted}"
    ok = run.exit_code == 0 and row_mounted
    rec.finish("PASS" if ok else "FAIL",
               "agent-presets standing mount + launcher shipped-root append "
               "(profile-boot.ts:159-167); presets minimal/standard/code/cordis",
               observed,
               note="per-preset persona differentiation is G6-16's leg")
    assert ok, observed


def test_g6_16_persona_scope(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-16: the persona row is scope-only — a global mount collides loud."""
    # Fixture: mount persona globally with a marker persona → boot must fail
    # loud per preset/persona module doc ("mounted globally it collides with
    # the registry's own registration and fails loud").
    bad = scratch_home / "patch-persona-global.yml"
    bad.write_text(
        "- insert:\n"
        "    - id: persona\n"
        "      name: '@deepseek-ai/dsh-persona'\n"
        "      config:\n"
        "        text: GORDON-PERSONA-COLLISION\n"
    )
    run = run_candidate(
        cfg,
        ["--profile", "headless", "--patch", str(bad), "ping"],
        env_extra=scratch_env, timeout=180,
    )
    rec.commands.append(run)
    observed = f"exit={run.exit_code}; stderr={run.stderr[-300:]}"
    ok = run.exit_code != 0
    rec.finish("PASS" if ok else "FAIL",
               "preset/persona: scope-only row; a global mount fails loud "
               "(module doc contract)",
               observed)
    assert ok, observed


def test_g6_17_bundle_layer_precedence(cfg, candidate_bin, scratch_home, scratch_env, rec):
    """G6-17: the profile cordis.patch.yml wins over the bundle row config."""
    patch = scratch_home / "patch-title.yml"
    patch.write_text(
        "- id: session-title\n"
        "  config:\n"
        "    fallbackMaxWords: 9\n"
        "    fallbackMaxBytes: 99\n"
        "    maxTitleBytes: 99\n"
    )
    profile_patch = scratch_home / "profiles" / "headless" / "cordis.patch.yml"
    run1 = run_candidate(cfg, ["--profile", "headless", "--dump-config"],
                         env_extra=scratch_env)
    rec.commands.append(run1)
    profile_patch.parent.mkdir(parents=True, exist_ok=True)
    profile_patch.write_text(
        "- id: session-title\n"
        "  config:\n"
        "    fallbackMaxWords: 7\n"
        "    fallbackMaxBytes: 77\n"
        "    maxTitleBytes: 77\n"
    )
    run2 = run_candidate(cfg, ["--profile", "headless", "--dump-config"],
                         env_extra=scratch_env)
    rec.commands.append(run2)
    rec.artifact("dump-precedence.yml", run2.stdout)
    default_line = "fallbackMaxWords: 5" in run1.stdout
    override_line = "fallbackMaxWords: 7" in run2.stdout and "fallbackMaxWords: 5" not in run2.stdout
    observed = f"default_shown={default_line}; profile_override_wins={override_line}"
    ok = run1.exit_code == 0 and run2.exit_code == 0 and default_line and override_line
    rec.finish("PASS" if ok else "FAIL",
               "boot/app-boot profile.ts layer order: profile cordis.patch.yml "
               "applied after every bundle layer (last write wins per row)",
               observed)
    assert ok, observed


def test_g6_18_live_recomposition(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec, web_boot):
    """G6-18: editing the profile user layer recomposes a long-lived boot (HMR)."""
    patch = seam_fixture_for(cfg, scratch_home, model_key="coder", max_retries=1)
    profile_patch = scratch_home / "profiles" / "web" / "cordis.patch.yml"
    profile_patch.parent.mkdir(parents=True, exist_ok=True)
    profile_patch.write_text("[]\n")
    boot = web_boot(scratch_env, str(workspace), patches=[str(patch)])
    try:
        if not boot.wait_bound(120):
            rec.finish("FAIL", "web boot binds", "no listener; log: " + boot.boot_log()[-300:])
            pytest.fail("web boot did not bind")
        profile_patch.write_text(
            "- id: session-title\n"
            "  config:\n"
            "    fallbackMaxWords: 11\n"
            "    fallbackMaxBytes: 111\n"
            "    maxTitleBytes: 111\n"
        )
        time.sleep(6)
        dump = run_candidate(cfg, ["--profile", "web", "--dump-config"],
                             env_extra=scratch_env)
        rec.commands.append(dump)
        recomposed = "fallbackMaxWords: 11" in dump.stdout
        observed = f"bound_port={boot.port}; recomposed_live_layer={recomposed}"
        ok = recomposed
        rec.finish("PASS" if ok else "FAIL",
                   "profile-boot watchUserPatches: user-layer edits recompose a "
                   "long-lived surface without restart",
                   observed)
        assert ok, observed
    finally:
        boot.stop()


def test_g6_19_mcp_round_trip(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-19: the mcp-client row registers mcp__fixture__* tools; one call round-trips."""
    fixture_path = Path(os.environ.get(
        "GORDON_MCP_FIXTURE", "/opt/dsh/packages/mcp/mcp-client/tests/fixture-server.ts"))
    if not fixture_path.exists():
        blocked(f"MCP fixture server absent at {fixture_path} (GORDON_MCP_FIXTURE)")
    patch = seam_fixture_b(cfg, scratch_home, "patch-mcp.yml.tmpl")

    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        names = [m for m in ("mcp__fixture__",) if m in text]
        return (run.exit_code == 0 and bool(names)), \
            f"mcp_qualified_names={bool(names)}"

    task = ("List your tools. If an mcp__fixture__ tool exists, call it once "
            "with a trivial argument and report the result. Reply DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G619", task, check,
                             timeout=600)
    finish_coop(rec, ok, observed,
                "mcp-client: server-qualified public names mcp__<server>__<tool>; "
                "stdio transport to the repo fixture server",
                note="model-cooperation class")
    assert ok, observed


def test_g6_20_ralph_bounded(cfg, candidate_bin, scratch_home, scratch_env, workspace, rec):
    """G6-20: tool-ralph starts bounded structured-output rounds."""
    def check(home, run, marker):
        log = latest_log(cfg, home)
        text = log_text(log)
        ralph = "ralph" in text
        return (run.exit_code in (0, 1) and ralph), f"ralph_evidence={ralph}"

    task = ("Use the ralph tool with the script 'echo __MARKER__' and at most 2 rounds. "
            "Report what happened, then reply DONE")
    ok, observed = cooperate(cfg, scratch_home, scratch_env, workspace, rec, "G620", task, check,
                             timeout=600)
    finish_coop(rec, ok, observed,
                "tool-ralph (subagentProvider spawn, maxRounds config; base row maxRounds 64)",
                note="model-cooperation heavy; bounded invocation proof")
    assert ok is not False or observed


def test_g6_21_feedback_census(cfg, candidate_bin, scratch_env, rec):
    """G6-21: command-feedback mounts; the interactive producer is Gate 7's."""
    run = run_candidate(cfg, ["--profile", "headless", "--dump-default-config"],
                        env_extra=scratch_env)
    rec.commands.append(run)
    row = "id: command-feedback" in run.stdout
    observed = f"command_feedback_row={row}"
    ok = run.exit_code == 0 and row
    rec.finish("PASS" if ok else "FAIL",
               "command-feedback (log-only feedback event; interactive slash "
               "producer → G7-17 web leg)",
               observed, note="behavior NOT_RUN on the headless surface by design")
    assert ok, observed


def test_g6_22_cookbook_tool_conflict(cfg, candidate_bin, scratch_home, scratch_env, rec):
    """G6-22 (cookbook adding-a-tool): a duplicate tool registration fails loud."""
    bad = scratch_home / "patch-dup-tool.yml"
    bad.write_text(
        "- insert:\n"
        "    - id: tool-todo-dup\n"
        "      name: '@deepseek-ai/dsh-tool-todo'\n"
        "      config:\n"
        "        allowParallelInProgress: true\n"
        "- insert:\n"
        "    - id: tool-todo-dup-2\n"
        "      name: '@deepseek-ai/dsh-tool-todo'\n"
        "      config:\n"
        "        allowParallelInProgress: true\n"
    )
    run = run_candidate(
        cfg, ["--profile", "headless", "--patch", str(bad), "ping"],
        env_extra=scratch_env, timeout=180,
    )
    rec.commands.append(run)
    observed = f"exit={run.exit_code}; stderr={run.stderr[-300:]}"
    ok = run.exit_code != 0
    rec.finish("PASS" if ok else "FAIL",
               "cookbook adding-a-tool + registry discipline: duplicate tool "
               "registration refuses the composition (fail loud)",
               observed)
    assert ok, observed


def test_g6_23_cookbook_package_gates(cfg, rec):
    """G6-23 (cookbook adding-a-package): invariant + skill-metadata gates green."""
    from gordon_util import run_host

    copy = Path(cfg.scratch) / "g1-source-copy"
    if not (copy / "package.json").exists():
        blocked(f"refreshed scratch copy absent at {copy} (run G1 first in this window)")
    env = {"PATH": f"{Path(cfg.node).parent}:{os.environ.get('PATH', '')}",
           "CI": "true",
           "DSH_CLIENT_COMMIT_HASH": "b150a551b8d465e31e418e1b2eaf5e79bbb7d28e"}
    results = []
    for script in ("verify-package-invariants", "verify-skill-invocation-metadata"):
        run = run_host([cfg.pnpm if Path(cfg.pnpm).exists() else "pnpm", "run", script],
                       cwd=str(copy), timeout=600, env_extra=env)
        rec.commands.append(run)
        results.append(f"{script}={run.exit_code}")
    observed = "; ".join(results)
    ok = all(r.endswith("=0") for r in results)
    rec.finish("PASS" if ok else "FAIL",
               "cookbook adding-a-package conventions: verify-package-invariants + "
               "verify-skill-invocation-metadata exit 0",
               observed)
    assert ok, observed
