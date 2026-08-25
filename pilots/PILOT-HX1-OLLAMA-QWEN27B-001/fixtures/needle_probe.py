#!/usr/bin/env python3
"""M6 capacity-proof needle probe at ~95% of stage context C.

Builds the frozen needle document (fixtures_corpus.needle_document) scaled to a
token target, asks the frozen Q16 question, and asserts:
  - prompt_eval_count within [LO, HI] (fixture validity vs the stage contract)
  - done_reason == stop (no truncation)
  - needle code present in the answer (quality signal at depth, reported either way)
Thinking content is stripped immediately (shared fixtures_corpus helper); only counts
are persisted (A01 5.2).
Usage: needle_probe.py TOTAL_LINES NEEDLE_LINE LO HI OUTJSON MODEL
       (MODEL = ratified model profile alias, e.g. hx-qwen3.8-27b-64k)
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # versioned fixtures dir (corrected 2026-08-25: was the stale /tmp scratch copy)
from fixtures_corpus import RAG_SYSTEM, needle_document, require_model, strip_think_tags

API = "http://127.0.0.1:11434/api/chat"
QUESTION = "What is the authorization code for the HX-1 pilot gate?"

if len(sys.argv) != 7:
    sys.exit("usage: needle_probe.py TOTAL_LINES NEEDLE_LINE LO HI OUTJSON MODEL  "
             "(MODEL = ratified model profile alias, e.g. hx-qwen3.8-27b-64k)")
total_lines, needle_line, lo, hi, outpath = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
MODEL = require_model(sys.argv[6])

user = ("Retrieved documents:\n\n[NEEDLE]\n" + needle_document(total_lines, needle_line) +
        "\n\nQuestion: " + QUESTION)
body = json.dumps({"model": MODEL, "stream": False,
                   "messages": [{"role": "system", "content": RAG_SYSTEM},
                                {"role": "user", "content": user}]}).encode()
req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json"})
t0 = time.monotonic()
with urllib.request.urlopen(req, timeout=900) as r:
    resp = json.loads(r.read())
wall = round(time.monotonic() - t0, 2)

msg = resp.get("message", {})
thinking = msg.get("thinking") or ""
answer = strip_think_tags(msg.get("content") or "")  # sanitized before any use/persist (A01 5.2)
pec = resp.get("prompt_eval_count")
ped = (resp.get("prompt_eval_duration") or 0) / 1e9
result = {
    "model": MODEL,
    "stage_probe": "needle@~95%ctx", "total_lines": total_lines, "needle_line": needle_line,
    "needle_depth_pct": round(100.0 * needle_line / total_lines, 1),
    "fixture_valid": isinstance(pec, int) and lo <= pec <= hi, "window": [lo, hi],
    "prompt_eval_count": pec, "prefill_tok_s": None if not ped else round(pec / ped, 1),
    "done_reason": resp.get("done_reason"), "eval_count": resp.get("eval_count"),
    "needle_found": "FALCON-61803" in answer,
    "answer": answer[:600], "thinking_present": bool(thinking.strip()),
    "thinking_chars": len(thinking),
    "total_duration_s": round(resp.get("total_duration", 0) / 1e9, 2), "wall_s": wall,
}
# Acceptance: fixture validity AND clean stop AND needle recovered; diagnostics stay either way.
result["pass"] = bool(result["fixture_valid"] and result["done_reason"] == "stop"
                      and result["needle_found"])
with open(outpath, "w") as f:
    json.dump(result, f, indent=1)
print(json.dumps({k: result[k] for k in ("model", "fixture_valid", "prompt_eval_count", "prefill_tok_s",
                                          "done_reason", "needle_found", "eval_count", "wall_s")}))
print("answer:", answer[:300].replace("\n", " | "))
sys.exit(0 if result["pass"] else 1)
