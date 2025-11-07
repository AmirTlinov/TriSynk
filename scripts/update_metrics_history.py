#!/usr/bin/env python3
"""Append current metrics.json to history log."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "reports" / "metrics.json"
HISTORY_DIR = ROOT / "reports" / "history"
HISTORY_FILE = HISTORY_DIR / "metrics_history.jsonl"


def main() -> int:
    if not METRICS.exists():
        raise SystemExit(f"Missing metrics file: {METRICS}")
    data = json.loads(METRICS.read_text(encoding="utf-8"))
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **data,
    }
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    with HISTORY_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
    print(f"[metrics-history] appended entry, coverage={data.get('coverage')} perf={data.get('perf_latency_pct')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
