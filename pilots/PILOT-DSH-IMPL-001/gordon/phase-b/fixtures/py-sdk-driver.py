#!/usr/bin/env python3
"""Gordon G7-15 driver: one routed turn through the Python SDK
(deepseek_harness.DeepSeekHarness) against the dsh-jsonrpc-agent runtime via
the scratch runtime_bin shim. Prints one JSON summary line.

env: G715_PROVIDER, G715_MODEL, G715_TASK, G715_WORKSPACE, G715_SESSION_ROOT,
     G715_CORDIS, G715_RUNTIME_BIN
"""

from __future__ import annotations

import json
import os
import sys

from deepseek_harness import DeepSeekHarness


def main() -> None:
    task = os.environ["G715_TASK"]
    summary: dict = {}
    with DeepSeekHarness(
        provider=os.environ["G715_PROVIDER"],
        model=os.environ["G715_MODEL"],
        cwd=os.environ["G715_WORKSPACE"],
        session_root=os.environ["G715_SESSION_ROOT"],
        cordis=os.environ["G715_CORDIS"],
        runtime_bin=os.environ["G715_RUNTIME_BIN"],
    ) as harness:
        result = harness.run(task)
    summary["sessionId"] = result.session_id
    summary["final_response"] = result.final_response
    summary["event_count"] = len(getattr(result, "events", []) or [])
    sys.stdout.write(json.dumps(summary) + "\n")


if __name__ == "__main__":
    main()
