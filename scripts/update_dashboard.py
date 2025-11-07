#!/usr/bin/env python3
"""Generate lightweight dashboard data from metrics history."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "reports" / "history" / "metrics_history.jsonl"
DASHBOARD = ROOT / "reports" / "dashboard" / "metrics_dashboard.json"


def main() -> int:
    entries = []
    if HISTORY.exists():
        with HISTORY.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    DASHBOARD.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD.write_text(json.dumps({"series": entries[-100:]}, indent=2), encoding="utf-8")
    print(f"[dashboard] wrote {DASHBOARD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
