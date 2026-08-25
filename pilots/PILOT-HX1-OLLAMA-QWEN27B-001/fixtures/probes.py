#!/usr/bin/env python3
"""A01 5.1 probes — thinking baseline, reasoning-control A/B matrix, multi-turn preservation.

Native defaults otherwise: no sampling overrides anywhere. Verdicts are evidence-based:
HONORED only when the request is accepted AND the observable behavior matches the request;
otherwise UNSUPPORTED (with the acceptance/behavior evidence). No parity is inferred from
upstream docs. Thinking content is NEVER persisted — only presence/length/counts (A01 5.2).

The RC think-flag/level cases are ONE-SHOT probes: a bare HTTP 200 (even with non-empty
thinking) only shows the request was ACCEPTED. Whether a think level is honored is
UNESTABLISHED from these probes — that verdict would require a repeated fixed-prompt
comparison with explicit sampling controls and a predefined acceptance criterion, which
this harness does not run.

Usage: probes.py MODEL  (MODEL = ratified model profile alias, e.g. hx-qwen3.8-27b-64k)
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # versioned fixtures dir
from fixtures_corpus import require_model, strip_think_tags

CHAT = "http://127.0.0.1:11434/api/chat"
GEN = "http://127.0.0.1:11434/api/generate"
OAI = "http://127.0.0.1:11434/v1/chat/completions"
# MODEL is set per run in main() from the required argv alias (no silent default).
KA = "What is 17 × 23? Reply with just the number."
REASON = ("A farmer has 17 sheep. All but 9 run away. Then he buys 3 times as many as he has "
          "left. How many sheep does he have now? Think carefully, then give just the number.")


def post(url, body, timeout=300):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.loads(r.read())
            code = r.status
    except urllib.error.HTTPError as e:
        resp = {"http_error": e.code, "body": e.read().decode(errors="replace")[:400]}
        code = e.code
    return code, resp, round(time.monotonic() - t0, 2)


def classify_one_shot(http_code):
    """One-shot probe classification: (classification, gradation).

    A successful response or non-empty thinking is never enough for HONORED — it only
    proves the request reached the server (ACCEPTED); the behavioral gradation stays
    UNESTABLISHED absent a repeated fixed-prompt comparison with explicit sampling
    controls and a predefined acceptance criterion.
    """
    if http_code == 200:
        return "ACCEPTED", "UNESTABLISHED"
    return "REJECTED", "NOT-APPLICABLE"


def chatmeta(resp):
    msg = resp.get("message", {}) if isinstance(resp, dict) else {}
    thinking = msg.get("thinking") or ""
    content = msg.get("content") or ""
    has_think_tag = "</think>" in content or "<think>" in content
    return {
        "thinking_present": bool(thinking.strip()),
        "thinking_chars": len(thinking),
        "content": strip_think_tags(content)[:400],
        "content_has_think_tag": has_think_tag,
        "eval_count": resp.get("eval_count"),
        "prompt_eval_count": resp.get("prompt_eval_count"),
        "done_reason": resp.get("done_reason"),
        "total_duration_s": round((resp.get("total_duration") or 0) / 1e9, 2),
    }


def main():
    global MODEL
    if len(sys.argv) != 2:
        sys.exit("usage: probes.py MODEL  (ratified model profile alias, e.g. hx-qwen3.8-27b-64k)")
    MODEL = require_model(sys.argv[1])
    out = {"model": MODEL, "sampling_overrides": None, "cases": {}}
    c = out["cases"]

    # ---------- TB: thinking baseline (repeatability x3 + think:false control + parsing)
    tb = []
    for i in range(3):
        code, resp, wall = post(CHAT, {"model": MODEL, "stream": False,
                                       "messages": [{"role": "user", "content": KA}]})
        m = chatmeta(resp)
        m["http"] = code
        m["wall_s"] = wall
        tb.append(m)
        print(f"TB1[{i}] think-default http={code} thinking={m['thinking_present']} "
              f"chars={m['thinking_chars']} content={m['content'][:40]!r} eval={m['eval_count']}", flush=True)
    code, resp, wall = post(CHAT, {"model": MODEL, "stream": False, "think": False,
                                   "messages": [{"role": "user", "content": KA}]})
    m = chatmeta(resp)
    m["http"] = code
    m["wall_s"] = wall
    c["TB-baseline-x3"] = tb
    c["TB-think-false-control"] = m
    print(f"TB2 think:false http={code} thinking={m['thinking_present']} content={m['content'][:40]!r}", flush=True)

    # ---------- RC: think flag and levels on a fixed reasoning prompt
    for label, think in [("RC-think-false", False), ("RC-think-true", True),
                         ("RC-think-low", "low"), ("RC-think-medium", "medium"),
                         ("RC-think-high", "high"), ("RC-think-max", "max")]:
        code, resp, wall = post(CHAT, {"model": MODEL, "stream": False, "think": think,
                                       "messages": [{"role": "user", "content": REASON}]})
        if code == 200:
            m = chatmeta(resp)
        else:
            m = {"rejected": resp}
        m["classification"], m["gradation"] = classify_one_shot(code)
        m["http"] = code
        m["wall_s"] = wall
        c[label] = m
        print(f"{label} http={code} class={m['classification']}/{m['gradation']} "
              f"thinking={m.get('thinking_present')} "
              f"chars={m.get('thinking_chars')} eval={m.get('eval_count')}", flush=True)

    # ---------- RC: native reasoning_effort field (unknown top-level field)
    code, resp, wall = post(CHAT, {"model": MODEL, "stream": False, "reasoning_effort": "none",
                                   "messages": [{"role": "user", "content": KA}]})
    m = chatmeta(resp)
    m["http"] = code
    c["RC-native-reasoning_effort-none"] = m
    print(f"RC-native-effort-none http={code} thinking={m['thinking_present']} "
          f"(thinking present despite 'none' => field ignored)", flush=True)

    # ---------- RC: native preserve_thinking field (unknown top-level field)
    code, resp, wall = post(CHAT, {"model": MODEL, "stream": False, "preserve_thinking": True,
                                   "messages": [{"role": "user", "content": KA}]})
    m = chatmeta(resp)
    m["http"] = code
    c["RC-native-preserve_thinking"] = m
    print(f"RC-native-preserve http={code} thinking={m['thinking_present']}", flush=True)

    # ---------- RC: OpenAI-compat reasoning_effort mapping
    for effort in ("none", "high"):
        code, resp, wall = post(OAI, {"model": MODEL, "stream": False, "reasoning_effort": effort,
                                      "messages": [{"role": "user", "content": REASON}]})
        if code == 200:
            ch = resp["choices"][0]["message"]
            rc_text = ch.get("reasoning_content") or ch.get("reasoning") or ""
            m = {"reasoning_present": bool(str(rc_text).strip()),
                 "reasoning_chars": len(str(rc_text)),
                 "content": (ch.get("content") or "")[:400],
                 "usage": resp.get("usage")}
        else:
            m = {"rejected": resp}
        m["http"] = code
        m["wall_s"] = wall
        c[f"RC-openai-reasoning_effort-{effort}"] = m
        print(f"RC-openai-effort-{effort} http={code} reasoning={m.get('reasoning_present')} "
              f"chars={m.get('reasoning_chars')}", flush=True)

    # ---------- MT: multi-turn preservation
    t1 = "What is 847 × 36? Reply with just the number."
    code, r1, _ = post(CHAT, {"model": MODEL, "stream": False,
                              "messages": [{"role": "user", "content": t1}]})
    m1 = chatmeta(r1)
    a1_content = m1["content"]
    c["MT-turn1"] = m1
    print(f"MT-turn1 content={a1_content[:40]!r} think_chars={m1['thinking_chars']}", flush=True)

    # MT-A: turn 2, history WITHOUT thinking (normal client behavior)
    t2 = "Add 1000 to that number. Reply with just the number."
    hist_plain = [{"role": "user", "content": t1},
                  {"role": "assistant", "content": a1_content},
                  {"role": "user", "content": t2}]
    code, rA, _ = post(CHAT, {"model": MODEL, "stream": False, "messages": hist_plain})
    mA = chatmeta(rA)
    c["MT-turn2-plain-history"] = mA
    print(f"MT-A plain content={mA['content'][:40]!r} prompt_tok={mA['prompt_eval_count']}", flush=True)

    # MT-B: turn 2, history WITH the thinking field echoed back by the client
    hist_think = [{"role": "user", "content": t1},
                  {"role": "assistant", "content": a1_content,
                   "thinking": "<client-echoed-thinking-redacted>"},
                  {"role": "user", "content": t2}]
    code, rB, _ = post(CHAT, {"model": MODEL, "stream": False, "messages": hist_think})
    mB = chatmeta(rB)
    c["MT-turn2-thinking-echoed"] = mB
    print(f"MT-B echo  content={mB['content'][:40]!r} prompt_tok={mB['prompt_eval_count']}", flush=True)

    # MT-C: fresh-session control (no context leakage across sessions)
    code, rC, _ = post(CHAT, {"model": MODEL, "stream": False,
                              "messages": [{"role": "user", "content": t2}]})
    mC = chatmeta(rC)
    c["MT-fresh-session-control"] = mC
    print(f"MT-C fresh content={mC['content'][:60]!r}", flush=True)

    # expected chain: 847*36=30492; +1000=31492
    out["expected"] = {"turn1": "30492", "turn2": "31492"}
    ev_dir = "/tmp/esme-m5b/evidence"
    os.makedirs(ev_dir, exist_ok=True)
    ev_path = os.path.join(ev_dir, time.strftime("probes-%Y%m%dT%H%M%SZ", time.gmtime()) + ".json")
    with open(ev_path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"{ev_path} written")


if __name__ == "__main__":
    main()
