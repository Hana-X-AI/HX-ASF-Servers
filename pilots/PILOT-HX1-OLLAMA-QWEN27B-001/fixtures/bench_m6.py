#!/usr/bin/env python3
"""M6 stage benchmark per plan 5.4 — Phase A native defaults, thinking ON, concurrency 1.

Derived from the frozen fixture bench.py (M5b); only the depth set is parameterized.
Captures: warm generation x3 (fixed prompt, same as fixture bench.py), prefill at several
depths up to ~95% of the stage context, TTFT (split: first THINKING chunk vs first CONTENT
chunk), Ollama-reported rates, done_reason. Cold-load timing is captured separately at the
preload-reload step (preload unit wall time); RAM/swap and dmon telemetry are captured by
the wrapper. No sampling overrides. Thinking content is never persisted (A01 5.2).
Usage: bench_m6.py OUTJSON MODEL TARGET_TOKEN [TARGET_TOKEN...]
       (MODEL = ratified model profile alias, e.g. hx-qwen3.8-27b-64k)
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

# Measured on this host in M5b: 11,215 tok / 8,200 words and 31,298 tok / 23,000 words.
TOK_PER_WORD = 1.365

# Ratified pilot requirement (plan 6.1): 128K cold ingest measured ~158 s; first content
# must arrive within 240 s or the trial fails. The 900 s total urlopen timeout is unchanged.
FIRST_CONTENT_DEADLINE_S = 240


def filler_prompt(target_tokens):
    words = int(target_tokens / TOK_PER_WORD)
    body = FILLER_SENT * (words // 14)
    return body + "\n\nQuestion: In one short sentence, what should operators do before each window?"


def trial_label(target_tokens):
    """Trial key carries the exact target — near targets (64000 vs 64500) must not collide."""
    return f"prefill_{target_tokens}"


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
            if ttft_content is None and time.monotonic() - t0 > FIRST_CONTENT_DEADLINE_S:
                # Deadline evaluated BEFORE accepting content: a first content chunk
                # arriving after 240 s fails the trial like any late chunk. Enforcement
                # stays loop-level on purpose — urlopen's timeout already bounds every
                # socket read (an inter-chunk gap cannot exceed 900 s), so a separate
                # socket-level first-content read timeout would add no guarantee.
                raise RuntimeError(f"no content chunk within {FIRST_CONTENT_DEADLINE_S} s "
                                   "(plan 6.1 first-content deadline); trial failed")
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
    if len(sys.argv) < 4:
        sys.exit("usage: bench_m6.py OUTJSON MODEL TARGET_TOKEN [TARGET_TOKEN...]  "
                 "(MODEL = ratified model profile alias, e.g. hx-qwen3.8-27b-64k)")
    outpath = sys.argv[1]
    MODEL = require_model(sys.argv[2])
    targets = [int(x) for x in sys.argv[3:]]
    out = {"model": MODEL, "config": "Phase A native defaults, thinking ON, concurrency 1", "trials": {}}
    # warm-up (ensures resident; model pinned with keep_alive=-1)
    stream_chat("ping")
    warm = []
    for i in range(3):
        r = stream_chat(WARM_PROMPT)
        warm.append(r)
        print(f"warm[{i}] ttft_think={r['ttft_thinking_s']} ttft_content={r['ttft_content_s']} "
              f"gen={r['gen_tok_s']} tok/s eval={r['eval_count']} wall={r['wall_s']}", flush=True)
    out["trials"]["warm_x3"] = warm

    for t in targets:
        label = trial_label(t)
        r = stream_chat(filler_prompt(t))
        r["target_tokens"] = t
        out["trials"][label] = r
        print(f"{label} target={t} prompt_tok={r['prompt_eval_count']} "
              f"prefill={r['prefill_tok_s']} tok/s ttft_think={r['ttft_thinking_s']} "
              f"ttft_content={r['ttft_content_s']} gen={r['gen_tok_s']} wall={r['wall_s']} "
              f"reason={r['done_reason']}", flush=True)

    with open(outpath, "w") as f:
        json.dump(out, f, indent=1)
    print("bench written:", outpath)


if __name__ == "__main__":
    main()
