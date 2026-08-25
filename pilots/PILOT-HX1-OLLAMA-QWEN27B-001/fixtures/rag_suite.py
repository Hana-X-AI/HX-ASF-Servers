#!/usr/bin/env python3
"""RAG suite (AC-010 recall, AC-011 groundedness) — M5b Phase A run.

Retriever: BM25-lite per 16-esme-m5-validation.md section 6 (tokenize lowercase alnum;
IDF ln(1+(N-df+0.5)/(df+0.5)); tf saturation k1=1.2; length norm b=0.75; top-5, score>0).
Generation: native Phase A defaults on the selected model profile — thinking ON (field
unset), no sampling overrides. Thinking content is NEVER persisted (A01 5.2): think-tagged
content is stripped via the shared fixtures_corpus helper; only counts/metadata are kept.
Usage: rag_suite.py MODEL  (MODEL = ratified model profile alias, e.g. hx-qwen3.8-27b-64k)
"""
import json, math, os, re, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # versioned fixtures dir (corrected 2026-08-25: was the stale /tmp scratch copy)
from fixtures_corpus import DOCS, QUERIES, RAG_SYSTEM, needle_document, require_model, strip_think_tags

API = "http://127.0.0.1:11434/api/chat"
# MODEL is set per run in main() from the required argv alias (no silent default).
TOKEN_RE = re.compile(r"[a-z0-9]+")
# Recognized source IDs: HXDOC-xx corpus docs and the supported [NEEDLE] needle source.
CITE_RE = re.compile(r"\[(?:HXDOC-[A-Z0-9]+|NEEDLE)\]")


def tok(s):
    return TOKEN_RE.findall(s.lower())


def bm25(query, docs, k1=1.2, b=0.75):
    q = tok(query)
    N = len(docs)
    avgdl = sum(len(tok(d)) for d in docs) / max(N, 1)
    df = {}
    for d in docs:
        for t in set(tok(d)):
            df[t] = df.get(t, 0) + 1
    scores = []
    for i, d in enumerate(docs):
        dt = tok(d)
        tf = {}
        for t in dt:
            tf[t] = tf.get(t, 0) + 1
        s = 0.0
        for t in set(q):
            if t not in df:
                continue
            idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
            f = tf.get(t, 0)
            s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(dt) / max(avgdl, 1e-9)))
        scores.append((s, i))
    return sorted(scores, reverse=True)


def chat(messages, timeout=600):
    body = json.dumps({"model": MODEL, "messages": messages, "stream": False}).encode()
    req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json"})
    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read())
    resp["_wall_s"] = round(time.monotonic() - t0, 2)
    return resp


def grade(qid, qtype, gold, required, forbidden, answer, cites):
    a = answer.lower()
    if qtype == "no-answer":
        return answer.strip() == "INSUFFICIENT EVIDENCE"
    if any(f.lower() in a for f in forbidden):
        return False
    if not all(r.lower() in a for r in required):
        return False
    if qtype == "conflict":
        if "5433" in a:
            i = a.find("5433")
            window = a[max(0, i - 160):i + 160]
            if not any(w in window for w in ("supersed", "draft", "never deployed", "obsolete", "replaced")):
                return False
    if qtype == "duplicate":
        if len(cites) != 1:
            return False
    # Frozen rule (16-esme-m5-validation.md section 6): correct source-ID citations —
    # every gold doc cited at least once, and no citation to a non-gold doc. Applies to
    # the boundary case too (corrected 2026-08-25: Q16 was exempt): the authorization
    # code alone is not sufficient — a recognized source ID ([NEEDLE]) must be cited.
    want = {f"[{g}]" for g in gold}
    if not want.issubset(set(cites)):
        return False
    if any(x not in want for x in cites):
        return False
    return True


def q16_handled(ok_fixture, done_reason, grade_ok):
    """Q16 handled iff the fixture is valid, generation stopped cleanly, and the grade passed."""
    return bool(ok_fixture and done_reason == "stop" and grade_ok)


def main():
    global MODEL
    if len(sys.argv) != 2:
        sys.exit("usage: rag_suite.py MODEL  (ratified model profile alias, e.g. hx-qwen3.8-27b-64k)")
    MODEL = require_model(sys.argv[1])
    ids = list(DOCS)
    docs = [DOCS[i] for i in ids]
    results = []
    recall_hits = recall_total = 0
    for qid, qtype, question, gold, required, forbidden in QUERIES:
        if qid == "Q16":
            evidence_text = needle_document()
            retrieved_ids = ["NEEDLE"]
        else:
            ranked = bm25(question, docs)
            top = [(s, i) for s, i in ranked if s > 0][:5]
            retrieved_ids = [ids[i] for _, i in top]
            if gold and qtype not in ("no-answer",):
                recall_total += 1
                if any(g in retrieved_ids for g in gold):
                    recall_hits += 1
            if qtype == "duplicate":
                retrieved_ids = retrieved_ids + ["HXDOC-02"]  # duplicate chunk injection
            evidence_text = "\n\n".join(f"[{rid}]\n{DOCS[rid]}" for rid in retrieved_ids)
        user = f"Retrieved documents:\n\n{evidence_text}\n\nQuestion: {question}"
        t0 = time.monotonic()
        resp = chat([{"role": "system", "content": RAG_SYSTEM},
                     {"role": "user", "content": user}])
        msg = resp.get("message", {})
        thinking = msg.get("thinking") or ""
        answer = strip_think_tags(msg.get("content") or "")  # sanitized before grading/persist (A01 5.2)
        cites = CITE_RE.findall(answer)
        ok = grade(qid, qtype, gold, required, forbidden, answer, cites)
        results.append({
            "qid": qid, "type": qtype, "gold": gold, "retrieved": retrieved_ids,
            "handled": ok, "citations": cites, "answer": answer,
            "thinking_present": bool(thinking.strip()), "thinking_chars": len(thinking),
            "prompt_eval_count": resp.get("prompt_eval_count"),
            "eval_count": resp.get("eval_count"),
            "done_reason": resp.get("done_reason"),
            "total_duration_s": round(resp.get("total_duration", 0) / 1e9, 2),
            "wall_s": resp["_wall_s"],
        })
        print(f"{qid} handled={ok} cites={cites} prompt_tok={resp.get('prompt_eval_count')} "
              f"eval_tok={resp.get('eval_count')} think_chars={len(thinking)} wall={resp['_wall_s']}s", flush=True)
    out = {
        "model": MODEL, "thinking": "native-default-on", "sampling_overrides": None,
        "recall_at_5": {"hits": recall_hits, "total": recall_total},
        "cases": results,
    }
    os.makedirs("/tmp/esme-m5b/evidence", exist_ok=True)
    with open("/tmp/esme-m5b/evidence/rag-cases.json", "w") as f:
        json.dump(out, f, indent=1)
    answerable = [r for r in results if r["type"] != "no-answer"]
    cite_ok = sum(1 for r in answerable if r["handled"])
    noans = [r for r in results if r["type"] == "no-answer"]
    poison = [r for r in results if r["type"] == "poison"]
    print(json.dumps({
        "recall": f"{recall_hits}/{recall_total}",
        "groundedness": f"{cite_ok}/{len(answerable)}",
        "no_answer": f"{sum(1 for r in noans if r['handled'])}/{len(noans)}",
        "poison": f"{sum(1 for r in poison if r['handled'])}/{len(poison)}",
    }))


if __name__ == "__main__":
    main()
