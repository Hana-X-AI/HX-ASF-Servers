#!/usr/bin/env python3
"""Phase A benchmark note (feeds M6) — native defaults, thinking ON.

Captures: warm generation x3 (fixed prompt), prefill at ~11K and ~31K tokens, TTFT
(split: first THINKING chunk vs first CONTENT chunk), Ollama-reported rates.
No sampling overrides. Presented beside M5 think:false numbers in the deliverable.
Usage: bench.py MODEL  (MODEL = ratified model profile alias, e.g. hx-qwen3.8-27b-64k)
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # versioned fixtures dir
from fixtures_corpus import require_model

CHAT = "http://127.0.0.1:11434/api/chat"
# MODEL is set per run in main() from the required argv alias (no silent default).

WARM_PROMPT = ("Explain in one paragraph why a loopback-only inference API is a sound "
               "security boundary for a single-node deployment, then give one sentence "
               "of operational advice for monitoring it.")

FILLER_SENT = ("Operations note: routine maintenance windows are published weekly and "
               "operators verify the checklist before each window begins. ")


def filler_prompt(target_words):
    body = FILLER_SENT * (target_words // 14)
    return body + "\n\nQuestion: In one short sentence, what should operators do before each window?"


def stream_chat(prompt, timeout=900):
    body = json.dumps({"model": MODEL, "stream": True,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(CHAT, data=body, headers={"Content-Type": "application/json"})
    t0 = time.monotonic()
    ttft_think = ttft_content = None
    think_chars = content_chars = 0
    final = {}
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for raw in r:
            if not raw.strip():
                continue
            chunk = json.loads(raw)
            msg = chunk.get("message", {})
            if msg.get("thinking"):
                think_chars += len(msg["thinking"])
                if ttft_think is None:
                    ttft_think = time.monotonic() - t0
            if msg.get("content"):
                content_chars += len(msg["content"])
                if ttft_content is None:
                    ttft_content = time.monotonic() - t0
            if chunk.get("done"):
                final = chunk
    wall = time.monotonic() - t0
    if not final:
        raise RuntimeError("stream ended without a terminal done chunk; trial failed "
                           "(null-derived benchmark evidence is not recorded)")
    pe_c = final.get("prompt_eval_count")
    pe_d = (final.get("prompt_eval_duration") or 0) / 1e9
    e_c = final.get("eval_count")
    e_d = (final.get("eval_duration") or 0) / 1e9
    return {
        "prompt_eval_count": pe_c, "eval_count": e_c,
        "ttft_thinking_s": None if ttft_think is None else round(ttft_think, 3),
        "ttft_content_s": None if ttft_content is None else round(ttft_content, 3),
        "wall_s": round(wall, 2),
        "prefill_tok_s": None if not pe_d else round(pe_c / pe_d, 1),
        "gen_tok_s": None if not e_d else round(e_c / e_d, 1),
        "thinking_chars": think_chars, "content_chars": content_chars,
        "done_reason": final.get("done_reason"),
        "load_duration_s": round((final.get("load_duration") or 0) / 1e9, 3),
    }


def main():
    global MODEL
    if len(sys.argv) != 2:
        sys.exit("usage: bench.py MODEL  (ratified model profile alias, e.g. hx-qwen3.8-27b-64k)")
    MODEL = require_model(sys.argv[1])
    out = {"model": MODEL, "config": "Phase A native defaults, thinking ON, concurrency 1", "trials": {}}
    # warm-up (ensures resident; model already pinned with keep_alive=-1)
    stream_chat("ping")
    warm = []
    for i in range(3):
        r = stream_chat(WARM_PROMPT)
        warm.append(r)
        print(f"warm[{i}] ttft_think={r['ttft_thinking_s']} ttft_content={r['ttft_content_s']} "
              f"gen={r['gen_tok_s']} tok/s eval={r['eval_count']} wall={r['wall_s']}", flush=True)
    out["trials"]["warm_x3"] = warm

    for label, words in [("prefill_11k", 8200), ("prefill_31k", 23000)]:
        r = stream_chat(filler_prompt(words))
        out["trials"][label] = r
        print(f"{label} prompt_tok={r['prompt_eval_count']} prefill={r['prefill_tok_s']} tok/s "
              f"ttft_content={r['ttft_content_s']} gen={r['gen_tok_s']} wall={r['wall_s']} "
              f"reason={r['done_reason']}", flush=True)

    os.makedirs("/tmp/esme-m5b/evidence", exist_ok=True)
    with open("/tmp/esme-m5b/evidence/bench.json", "w") as f:
        json.dump(out, f, indent=1)
    print("bench.json written")


if __name__ == "__main__":
    main()
