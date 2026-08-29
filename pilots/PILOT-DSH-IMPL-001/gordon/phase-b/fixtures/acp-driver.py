#!/usr/bin/env python3
"""Gordon G7-16 driver: ACP JSON-RPC flow over stdio against dsh-acp-demo.

Flow: initialize → session/new → session/prompt (nonce task) → collect
session/update notifications until the prompt settles → second prompt +
session/cancel for the cancellation leg. Permission requests are answered
allow-once (automation posture; the fixture policy is `never`, so none are
expected — answers are recorded if they arrive).

argv: <runtime argv...> (the acp-demo bin launch: node bin.js --config path)
env:  ACP_TASK (nonce task text), ACP_CANCEL_TASK, ACP_WORKSPACE
stdout: one JSON summary line.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time

TASK = os.environ.get("ACP_TASK", "Reply with exactly: GORDON-ACP")
CANCEL_TASK = os.environ.get("ACP_CANCEL_TASK", "Count slowly from 1 to 1000000, one number per line.")
WORKSPACE = os.environ.get("ACP_WORKSPACE", "/var/tmp")


class AcpConnection:
    def __init__(self, argv: list[str]):
        self.proc = subprocess.Popen(
            argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=False,
        )
        self.next_id = 0
        self.responses: dict[int, dict] = {}
        self.notifications: list[dict] = []
        self.server_requests: list[dict] = []
        self.stderr_lines: list[str] = []
        self._lock = threading.Lock()
        self._closed = False
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()
        self._stderr_reader = threading.Thread(target=self._stderr_loop, daemon=True)
        self._stderr_reader.start()

    def _stderr_loop(self) -> None:
        assert self.proc.stderr is not None
        for raw in self.proc.stderr:
            self.stderr_lines.append(raw.decode(errors="replace").rstrip())

    def _read_loop(self) -> None:
        assert self.proc.stdout is not None
        for raw in self.proc.stdout:
            line = raw.decode(errors="replace").strip()
            if not line:
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                self.notifications.append({"_unparsable": line[:200]})
                continue
            if "method" in message and "id" in message:
                # Server→client request (e.g. session/request_permission).
                self.server_requests.append(message)
                if message["method"] == "session/request_permission":
                    options = (message.get("params", {}).get("options") or [{}])
                    option_id = options[0].get("optionId", "allow-once")
                    self._send({
                        "jsonrpc": "2.0",
                        "id": message["id"],
                        "result": {"outcome": {"outcome": "selected", "optionId": option_id}},
                    })
            elif "method" in message:
                self.notifications.append(message)
            elif "id" in message:
                with self._lock:
                    self.responses[message["id"]] = message

    def _send(self, message: dict) -> None:
        with self._lock:
            if self._closed:
                return
            assert self.proc.stdin is not None
            try:
                self.proc.stdin.write((json.dumps(message) + "\n").encode())
                self.proc.stdin.flush()
            except (BrokenPipeError, OSError):
                pass

    def request(self, method: str, params: dict, timeout: float = 240.0) -> dict:
        self.next_id += 1
        request_id = self.next_id
        self._send({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self._lock:
                if request_id in self.responses:
                    return self.responses.pop(request_id)
            if self.proc.poll() is not None:
                raise RuntimeError(f"runtime exited during {method}: rc={self.proc.returncode}")
            time.sleep(0.05)
        raise TimeoutError(f"no response to {method} within {timeout}s")

    def notify(self, method: str, params: dict) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params})


def main() -> None:
    argv = sys.argv[1:]
    conn = AcpConnection(argv)
    summary: dict = {"steps": []}
    try:
        init = conn.request("initialize", {"protocolVersion": 1, "clientCapabilities": {}})
        summary["initialize"] = init.get("result", init.get("error"))

        session = conn.request("session/new", {"cwd": WORKSPACE, "mcpServers": []})
        session_result = session.get("result", session.get("error"))
        summary["session_new"] = session_result
        session_id = session_result.get("sessionId") if isinstance(session_result, dict) else None
        if session_id is None:
            summary["failure"] = "session/new returned no sessionId"
        else:
            prompt = conn.request(
                "session/prompt",
                {"sessionId": session_id,
                 "prompt": [{"type": "text", "text": TASK}]},
                timeout=300.0,
            )
            summary["prompt_response"] = prompt.get("result", prompt.get("error"))

            # Nonce-turn updates captured BEFORE the cancellation leg: the
            # assistant tail derives from the nonce prompt's notifications only.
            nonce_updates = [n for n in conn.notifications
                             if n.get("method") == "session/update"
                             and ((n.get("params") or {}).get("update") or {})
                             .get("sessionUpdate") == "agent_message_chunk"]
            summary["assistant_text_tail"] = [
                (u.get("params", {}).get("update", {}) or {}).get("content", {})
                for u in nonce_updates[-6:]
            ]

            # Cancellation leg: long task, cancel shortly after admission.
            conn.next_id += 1
            cancel_prompt_id = conn.next_id
            conn._send({
                "jsonrpc": "2.0", "id": cancel_prompt_id, "method": "session/prompt",
                "params": {"sessionId": session_id,
                           "prompt": [{"type": "text", "text": CANCEL_TASK}]},
            })
            time.sleep(2.0)
            conn.notify("session/cancel", {"sessionId": session_id})
            deadline = time.monotonic() + 60
            cancel_response = None
            while time.monotonic() < deadline:
                with conn._lock:
                    if cancel_prompt_id in conn.responses:
                        cancel_response = conn.responses.pop(cancel_prompt_id)
                        break
                time.sleep(0.1)
            summary["cancel_response"] = (
                cancel_response.get("result", cancel_response.get("error"))
                if cancel_response else "no-response-within-60s"
            )

            updates = [n for n in conn.notifications
                       if n.get("method") == "session/update"]
            summary["session_updates"] = len(updates)
            summary["permission_requests"] = len(conn.server_requests)
    except Exception as exc:  # any flow failure is recorded in the summary, never raised past it
        summary["failure"] = f"{type(exc).__name__}: {exc}"
    finally:
        with conn._lock:
            conn._closed = True
        try:
            if conn.proc.stdin:
                conn.proc.stdin.close()
        except OSError:
            pass
        try:
            conn.proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            conn.proc.kill()
            conn.proc.wait(timeout=10)
        summary["runtime_exit"] = conn.proc.returncode
        summary["stderr_tail"] = conn.stderr_lines[-10:]
        sys.stdout.write(json.dumps(summary) + "\n")


if __name__ == "__main__":
    main()
