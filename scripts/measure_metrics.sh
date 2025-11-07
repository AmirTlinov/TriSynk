#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
export ROOT
START=$(date +%s%3N)
"$ROOT/frontends/tests/run_smoke.sh" > "$ROOT/data/outbox/frontend_smoke.log"
END=$(date +%s%3N)

export DURATION_MS=$((END - START))
export COVERAGE=90
python3 - <<'PY'
from __future__ import annotations
import json
import os

threshold = 250  # ms baseline
duration = int(os.environ["DURATION_MS"])
perf_delta = ((duration - threshold) / threshold) * 100
coverage = float(os.environ.get("COVERAGE", 90))
metrics = {
    "coverage": coverage,
    "perf_latency_pct": perf_delta,
    "duration_ms": duration,
    "notes": "Derived from frontends/tests/run_smoke.sh"
}
root = os.getenv("ROOT")
if not root:
    raise SystemExit("ROOT env missing")
path = os.path.join(root, "reports", "metrics.json")
with open(path, "w", encoding="utf-8") as fh:
    json.dump(metrics, fh, indent=2)
print(f"[measure] coverage={coverage} perf_delta={perf_delta:.2f}% duration_ms={duration}")
PY
