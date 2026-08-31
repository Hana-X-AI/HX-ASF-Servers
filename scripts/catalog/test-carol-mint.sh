#!/usr/bin/env bash
# test-carol-mint.sh — offline fixture tests for scripts/catalog/carol-mint.
# Builds a sandbox catalog in a temp dir (CAROL_MINT_ROOT), exercises the
# commands and the refusal matrix. No network, no real catalog, no credentials.
set -uo pipefail

TOOL="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/carol-mint"
fx="$(mktemp -d /tmp/carol-mint-test.XXXXXX)"
trap 'rm -rf "$fx"' EXIT

pass=0; fail_n=0
ok()  { pass=$((pass+1)); printf 'PASS  %s\n' "$1"; }
bad() { fail_n=$((fail_n+1)); printf 'FAIL  %s\n' "$1"; }

export CAROL_MINT_ROOT="$fx"
mkdir -p "$fx/documents" "$fx/receipts" "$fx/src"

cat > "$fx/schema.yaml" <<'EOF'
schema:
  fields:
    validation:
      fields:
        freshness: {enum: [current, aging, stale, superseded, historical, living]}
EOF

echo "alpha one" > "$fx/src/a.md"
echo "beta one"  > "$fx/src/b.md"

mk_rec () { # id source freshness purpose
  local id="$1" src="$2" fresh="$3" purpose="$4"
  cat > "$fx/documents/$id.yaml" <<EOF
document:
  id: "$id"
  title: "$id fixture"
  type: "evidence"
  declared_purpose: "$purpose"
  source: {origin: "$fx/src/$src"}
  validation: {validated_at: "2026-08-28T00:00:00Z", freshness: "$fresh"}
  sha256: "$(sha256sum "$fx/src/$src" | cut -d' ' -f1)"
  canonical_location: "$fx/src/$src"
notes: {}
EOF
}

mk_rec DOC-fix-alpha a.md current "alpha purpose"
mk_rec DOC-fix-beta  b.md living  "beta purpose"
mk_rec DOC-fix-pending a.md current "PENDING-AGENT"

# 1. re-mint on changed source updates the record
echo "alpha two" > "$fx/src/a.md"
out="$(python3 "$TOOL" re-mint DOC-fix-alpha 2>&1)"; rc=$?
if [ $rc -eq 0 ] && printf '%s' "$out" | grep -q "re-minted"; then ok "re-mint changed source"; else bad "re-mint changed: rc=$rc out=[$out]"; fi

# 2. re-mint on unchanged source reports current
out="$(python3 "$TOOL" re-mint DOC-fix-alpha 2>&1)"; rc=$?
if [ $rc -eq 0 ] && printf '%s' "$out" | grep -q "current"; then ok "re-mint unchanged = current"; else bad "re-mint unchanged: rc=$rc out=[$out]"; fi

# 2a. freshness-only re-mint records the same hash at the mint timestamp
out="$(python3 "$TOOL" re-mint DOC-fix-alpha --set-freshness current --note "same-hash fixture" 2>&1)"; rc=$?
if [ $rc -eq 0 ] && python3 - <<'PY'
import os
import re
import yaml

path = os.path.join(os.environ["CAROL_MINT_ROOT"], "documents", "DOC-fix-alpha.yaml")
with open(path, encoding="utf-8") as fh:
  data = yaml.safe_load(fh)
doc = data["document"]
minted = data["notes"]["minted_by"]
timestamp = re.search(r" @ ([^ ]+) — ", minted).group(1)
matches = [
  event for event in doc["hash_history"]
  if event.get("sha256") == doc["sha256"]
  and event.get("timestamp") == timestamp
  and event.get("reason") == "same-hash fixture"
]
assert doc["validation"]["validated_at"] == timestamp
assert len(matches) == 1
PY
then ok "freshness-only re-mint records same-hash event"; else bad "freshness-only history: rc=$rc out=[$out]"; fi

# 2b. only an identical SHA/timestamp/reason event is idempotent
if CAROL_MINT_TOOL="$TOOL" python3 - <<'PY'
import importlib.machinery
import importlib.util
import os

loader = importlib.machinery.SourceFileLoader("carol_mint_tested", os.environ["CAROL_MINT_TOOL"])
spec = importlib.util.spec_from_loader("carol_mint_tested", loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)

digest = "a" * 64
events = {"document": {"hash_history": []}, "notes": {}}
module.append_hash_history(events, digest, digest, "reason one", "2026-08-31T05:00:00Z")
module.append_hash_history(events, digest, digest, "reason one", "2026-08-31T05:00:00Z")
module.append_hash_history(events, digest, digest, "reason two", "2026-08-31T05:00:00Z")
module.append_hash_history(events, digest, digest, "reason one", "2026-08-31T05:00:01Z")
assert len(events["document"]["hash_history"]) == 3

prose = {"document": {}, "notes": {"hash_history": "seed"}}
module.append_hash_history(prose, digest, digest, "reason one", "2026-08-31T05:00:00Z")
module.append_hash_history(prose, digest, digest, "reason one", "2026-08-31T05:00:00Z")
module.append_hash_history(prose, digest, digest, "reason two", "2026-08-31T05:00:00Z")
module.append_hash_history(prose, digest, digest, "reason one", "2026-08-31T05:00:01Z")
chain = prose["notes"]["hash_history"]
assert chain.count("aaaaaaaa… (2026-08-31T05:00:00Z, reason one)") == 1
assert chain.count("aaaaaaaa… (2026-08-31T05:00:00Z, reason two)") == 1
assert chain.count("aaaaaaaa… (2026-08-31T05:00:01Z, reason one)") == 1
PY
then ok "hash-history exact-event idempotence: list + prose"; else bad "hash-history exact-event idempotence"; fi

# 3. refusal: unknown record
out="$(python3 "$TOOL" re-mint DOC-nope 2>&1)"; rc=$?
if [ $rc -eq 1 ] && printf '%s' "$out" | grep -q "REFUSED"; then ok "refusal: unknown record"; else bad "refusal unknown: rc=$rc out=[$out]"; fi

# 4. refusal: missing source
python3 - <<'PY'
import yaml
p = "%s/documents/DOC-fix-alpha.yaml" % __import__("os").environ["CAROL_MINT_ROOT"]
d = yaml.safe_load(open(p))
d["document"]["canonical_location"] = "/nonexistent/nope.md"
yaml.safe_dump(d, open(p, "w"), sort_keys=False)
PY
out="$(python3 "$TOOL" re-mint DOC-fix-alpha 2>&1)"; rc=$?
if [ $rc -eq 1 ] && printf '%s' "$out" | grep -q "REFUSED"; then ok "refusal: missing source"; else bad "refusal missing source: rc=$rc out=[$out]"; fi
python3 - <<'PY'
import yaml, os
p = "%s/documents/DOC-fix-alpha.yaml" % os.environ["CAROL_MINT_ROOT"]
d = yaml.safe_load(open(p))
d["document"]["canonical_location"] = "%s/src/a.md" % os.environ["CAROL_MINT_ROOT"]
yaml.safe_dump(d, open(p, "w"), sort_keys=False)
PY

# 5. new scaffolds; gate FAILS on PENDING-AGENT until an agent fills it
out="$(python3 "$TOOL" new DOC-fix-gamma --source "$fx/src/b.md" --type evidence 2>&1)"; rc=$?
if [ $rc -eq 0 ] && [ -f "$fx/documents/DOC-fix-gamma.yaml" ]; then ok "new scaffolds record"; else bad "new: rc=$rc out=[$out]"; fi
out="$(python3 "$TOOL" gate --ids DOC-fix-gamma 2>&1)"; rc=$?
if [ $rc -eq 1 ] && printf '%s' "$out" | grep -q "PENDING-AGENT"; then ok "gate catches PENDING-AGENT"; else bad "gate pending: rc=$rc out=[$out]"; fi
python3 - <<'PY'
import yaml, os
p = "%s/documents/DOC-fix-gamma.yaml" % os.environ["CAROL_MINT_ROOT"]
d = yaml.safe_load(open(p))
d["document"]["declared_purpose"] = "agent-filled purpose"
yaml.safe_dump(d, open(p, "w"), sort_keys=False)
PY
out="$(python3 "$TOOL" gate --ids DOC-fix-gamma 2>&1)"; rc=$?
if [ $rc -eq 0 ] && printf '%s' "$out" | grep -q "PASS"; then ok "gate passes after agent fill"; else bad "gate after fill: rc=$rc out=[$out]"; fi

# 6. refusal: new with existing id
out="$(python3 "$TOOL" new DOC-fix-alpha --source "$fx/src/a.md" --type evidence 2>&1)"; rc=$?
if [ $rc -eq 1 ] && printf '%s' "$out" | grep -q "REFUSED"; then ok "refusal: new existing id"; else bad "refusal new existing: rc=$rc out=[$out]"; fi

# 7. refusal: lock contention (single-writer rule)
python3 - <<'PY' &
import fcntl, time, os
fh = open(os.path.join(os.environ["CAROL_MINT_ROOT"], ".mint.lock"), "a+")
fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
time.sleep(4)
PY
sleep 0.5
out="$(python3 "$TOOL" re-mint DOC-fix-beta 2>&1)"; rc=$?
if [ $rc -eq 1 ] && printf '%s' "$out" | grep -q "single-writer"; then ok "refusal: lock contention"; else bad "refusal lock: rc=$rc out=[$out]"; fi
wait 2>/dev/null

# 8. index rebuild: count matches; idempotent; hand-maintained titles preserved
python3 "$TOOL" index >/dev/null 2>&1
n1="$(grep -c '^  - id:' "$fx/index.yaml")"
python3 - <<'PY'
import yaml, os
p = "%s/documents/DOC-fix-alpha.yaml" % os.environ["CAROL_MINT_ROOT"]
d = yaml.safe_load(open(p))
d["document"]["title"] = "alpha CHANGED title"
yaml.safe_dump(d, open(p, "w"), sort_keys=False)
PY
python3 "$TOOL" index >/dev/null 2>&1
n2="$(grep -c '^  - id:' "$fx/index.yaml")"
kept="$(grep -c 'DOC-fix-alpha fixture' "$fx/index.yaml")"
python3 "$TOOL" index --rebuild-titles >/dev/null 2>&1
rebuilt="$(grep -c 'alpha CHANGED title' "$fx/index.yaml")"
if [ "$n1" = 4 ] && [ "$n2" = 4 ] && [ "$kept" = 1 ] && [ "$rebuilt" = 1 ]; then ok "index count + idempotent + titles preserved/rebuilt"; else bad "index: n1=$n1 n2=$n2 kept=$kept rebuilt=$rebuilt"; fi

# 9. sweep-stale detects drift and tags living
echo "beta two" > "$fx/src/b.md"
echo "alpha three" > "$fx/src/a.md"
out="$(python3 "$TOOL" sweep-stale 2>&1)"; rc=$?
if [ $rc -eq 1 ] && printf '%s' "$out" | grep -q "DOC-fix-beta.*living"; then ok "sweep-stale detects + tags living"; else bad "sweep: rc=$rc out=[$out]"; fi

# 10. consolidate re-mints ONLY living records
out="$(python3 "$TOOL" consolidate 2>&1)"; rc=$?
beta_hash="$(grep 'sha256:' "$fx/documents/DOC-fix-beta.yaml" | head -1 | grep -o '[a-f0-9]\{64\}')"
live_b="$(sha256sum "$fx/src/b.md" | cut -d' ' -f1)"
alpha_stale="$(python3 "$TOOL" sweep-stale 2>&1 | grep -c 'DOC-fix-alpha')" || true
if [ $rc -eq 0 ] && [ "$beta_hash" = "$live_b" ] && [ "$alpha_stale" -ge 1 ]; then ok "consolidate: living only, non-living left stale"; else bad "consolidate: rc=$rc beta=$beta_hash live=$live_b alpha_stale=$alpha_stale"; fi

# 11. receipt skeleton created; duplicate refused
out="$(python3 "$TOOL" receipt testwave --items DOC-fix-alpha,DOC-fix-beta 2>&1)"; rc=$?
if [ $rc -eq 0 ] && ls "$fx/receipts/"*-carol-testwave.md >/dev/null 2>&1; then ok "receipt skeleton"; else bad "receipt: rc=$rc out=[$out]"; fi
out="$(python3 "$TOOL" receipt testwave --items DOC-fix-alpha 2>&1)"; rc=$?
if [ $rc -eq 1 ] && printf '%s' "$out" | grep -q "REFUSED"; then ok "refusal: duplicate receipt"; else bad "refusal dup receipt: rc=$rc out=[$out]"; fi

# 12. full gate passes on a clean sandbox (after fixing remaining drift)
python3 "$TOOL" re-mint DOC-fix-alpha >/dev/null 2>&1
python3 "$TOOL" re-mint DOC-fix-gamma >/dev/null 2>&1
python3 - <<'PY'
import yaml, os
p = "%s/documents/DOC-fix-pending.yaml" % os.environ["CAROL_MINT_ROOT"]
d = yaml.safe_load(open(p))
d["document"]["declared_purpose"] = "filled"
yaml.safe_dump(d, open(p, "w"), sort_keys=False)
PY
python3 "$TOOL" re-mint DOC-fix-pending >/dev/null 2>&1
python3 "$TOOL" index >/dev/null 2>&1
out="$(python3 "$TOOL" gate 2>&1)"; rc=$?
if [ $rc -eq 0 ] && printf '%s' "$out" | grep -q "PASS"; then ok "full gate PASS"; else bad "full gate: rc=$rc out=[$out]"; fi

echo
echo "carol-mint tests: $pass passed, $fail_n failed"
[ "$fail_n" -eq 0 ]
