#!/usr/bin/env python3
"""Guard rail for coverage and performance metrics."""
from __future__ import annotations

import json
import sys
from pathlib import Path

METRICS_PATH = Path("reports/metrics.json")
TARGET_COVERAGE = 85.0
MAX_LATENCY_DELTA = 5.0  # percent over baseline


def main() -> int:
    if not METRICS_PATH.exists():
        raise SystemExit(f"Missing metrics file: {METRICS_PATH}")
    data = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    coverage = float(data.get("coverage", 0))
    latency = float(data.get("perf_latency_pct", 100))
    ok = True
    if coverage < TARGET_COVERAGE:
        print(f"[metrics] Coverage {coverage}% < target {TARGET_COVERAGE}%")
        ok = False
    if latency > MAX_LATENCY_DELTA:
        print(f"[metrics] Perf latency delta {latency}% > {MAX_LATENCY_DELTA}%")
        ok = False
    if ok:
        print(
            f"[metrics] OK – coverage={coverage}%, perf_latency={latency}% (targets: >= {TARGET_COVERAGE}%, <= {MAX_LATENCY_DELTA}%)"
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
