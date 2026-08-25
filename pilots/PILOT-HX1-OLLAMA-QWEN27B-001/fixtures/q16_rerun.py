#!/usr/bin/env python3
"""Q16 boundary-case rerun on the calibrated needle document + deterministic regrade.

Step 1: rerun Q16 once with the calibrated filler; guard: prompt_eval_count must be in
[28000, 32600] (fixture validity vs the 32,768 contract) and done_reason must be stop.
Step 2: regrade all saved rag-cases.json answers deterministically (no new model calls
for Q01-Q15) with the frozen citation rule from 16-esme-m5-validation.md section 6.
Thinking content is stripped via the shared fixtures_corpus helper (A01 5.2).
Usage: q16_rerun.py MODEL  (MODEL = ratified model profile alias, e.g. hx-qwen3.8-27b-64k)
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # versioned fixtures dir (corrected 2026-08-25: was the stale /tmp scratch copy)
from fixtures_corpus import QUERIES, RAG_SYSTEM, needle_document, require_model, strip_think_tags
from rag_suite import grade, q16_handled, CITE_RE

API = "http://127.0.0.1:11434/api/chat"

if len(sys.argv) != 2:
    sys.exit("usage: q16_rerun.py MODEL  (ratified model profile alias, e.g. hx-qwen3.8-27b-64k)")
MODEL = require_model(sys.argv[1])

q16 = [q for q in QUERIES if q[0] == "Q16"][0]
_, qtype, question, gold, required, forbidden = q16

user = ("Retrieved documents:\n\n[NEEDLE]\n" + needle_document() +
        "\n\nQuestion: " + question)
body = json.dumps({"model": MODEL, "stream": False,
                   "messages": [{"role": "system", "content": RAG_SYSTEM},
                                {"role": "user", "content": user}]}).encode()
req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json"})
t0 = time.monotonic()
with urllib.request.urlopen(req, timeout=600) as r:
    resp = json.loads(r.read())
wall = round(time.monotonic() - t0, 2)

msg = resp.get("message", {})
thinking = msg.get("thinking") or ""
answer = strip_think_tags(msg.get("content") or "")  # sanitized before grading/persist (A01 5.2)
cites = CITE_RE.findall(answer)
pec = resp.get("prompt_eval_count")
ok_fixture = isinstance(pec, int) and 28000 <= pec <= 32600
handled = q16_handled(ok_fixture, resp.get("done_reason"),
                      grade("Q16", qtype, gold, required, forbidden, answer, cites))

result = {
    "model": MODEL,
    "qid": "Q16", "type": qtype, "fixture": "needle document v1.0.0-RECONSTRUCTED (calibrated filler)",
    "fixture_valid": ok_fixture, "prompt_eval_count": pec,
    "handled": handled, "citations": cites, "answer": answer,
    "thinking_present": bool(thinking.strip()), "thinking_chars": len(thinking),
    "eval_count": resp.get("eval_count"), "done_reason": resp.get("done_reason"),
    "total_duration_s": round(resp.get("total_duration", 0) / 1e9, 2), "wall_s": wall,
}
os.makedirs("/tmp/esme-m5b/evidence", exist_ok=True)
with open("/tmp/esme-m5b/evidence/q16-rerun.json", "w") as f:
    json.dump(result, f, indent=1)
print(json.dumps({k: result[k] for k in ("model", "fixture_valid", "prompt_eval_count", "handled",
                                          "done_reason", "eval_count", "wall_s")}))
print("answer:", answer[:300].replace("\n", " | "))

# ---- deterministic regrade of Q01-Q15 with the frozen citation rule
d = json.load(open("/tmp/esme-m5b/evidence/rag-cases.json"))
regraded = []
for c in d["cases"]:
    q = [x for x in QUERIES if x[0] == c["qid"]][0]
    _, qt, _, g, req_s, forb = q
    ok = grade(c["qid"], qt, g, req_s, forb, c["answer"], c["citations"])
    if c["qid"] == "Q16":
        # Q16 keeps its fixture-validity gate under regrade: handled only when the grade
        # passes AND the stored prompt_eval_count is in the 32,768-contract window AND
        # generation stopped cleanly (same gate as the rerun step above).
        c_pec = c.get("prompt_eval_count")
        ok = q16_handled(isinstance(c_pec, int) and 28000 <= c_pec <= 32600,
                         c.get("done_reason"), ok)
    regraded.append({"qid": c["qid"], "type": c["type"], "handled_first_grading": c["handled"],
                     "handled_frozen_rule": ok})
    c["handled"] = ok
d["grader_note"] = ("Regraded with frozen rule (M5 section 6): gold doc cited >=1 and no non-gold "
                    "citations; duplicate case exactly one citation. First grading used an over-strict "
                    "exactly-one-citation clause for all cases (disclosed).")
d["q16_superseded_by"] = "q16-rerun.json (first Q16 fixture was oversized: 318K chars truncated at 32K; needle lost)"
with open("/tmp/esme-m5b/evidence/rag-cases.json", "w") as f:
    json.dump(d, f, indent=1)
answerable = [c for c in d["cases"] if c["type"] != "no-answer" and c["qid"] != "Q16"]
print("regrade:", json.dumps(regraded))
print("groundedness Q01-Q15 answerable:",
      f"{sum(1 for c in answerable if c['handled'])}/{len(answerable)}")
