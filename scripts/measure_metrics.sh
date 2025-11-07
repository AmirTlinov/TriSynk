#!/usr/bin/env bash
set -euo pipefail
find_tool() {
  local name="$1"
  if command -v "$name" >/dev/null 2>&1; then
    command -v "$name"
    return 0
  fi
  for path in /usr/bin/$name-* /usr/lib/llvm-*/bin/$name; do
    if [[ -x "$path" ]]; then
      echo "$path"
      return 0
    fi
  done
  return 1
}

ROOT="$(git rev-parse --show-toplevel)"
export ROOT
COV_DIR="$ROOT/data/outbox/coverage"
SAMPLE_CPP="$ROOT/frontends/samples/sample.cpp"
INPUT_BIN="$COV_DIR/sample_cov"
PROFILE_RAW="$COV_DIR/sample.profraw"
PROFILE_DATA="$COV_DIR/sample.profdata"
REPORT_TXT="$COV_DIR/llvm_cov_report.txt"
mkdir -p "$COV_DIR"

CLANGPP=$(find_tool clang++) || { echo "clang++ not found" >&2; exit 1; }
LLVM_PROFDATA=$(find_tool llvm-profdata) || { echo "llvm-profdata not found" >&2; exit 1; }
LLVM_COV=$(find_tool llvm-cov) || { echo "llvm-cov not found" >&2; exit 1; }

"$CLANGPP" -std=c++20 -fprofile-instr-generate -fcoverage-mapping "$SAMPLE_CPP" -o "$INPUT_BIN"
LLVM_PROFILE_FILE="$PROFILE_RAW" "$INPUT_BIN" >/dev/null
"$LLVM_PROFDATA" merge -sparse "$PROFILE_RAW" -o "$PROFILE_DATA"
"$LLVM_COV" report "$INPUT_BIN" -instr-profile="$PROFILE_DATA" > "$REPORT_TXT"
COVERAGE=$(awk '/TOTAL/{print $(NF-3)}' "$REPORT_TXT" | tr -d '%')
START=$(date +%s%3N)
"$ROOT/frontends/tests/run_smoke.sh" > "$ROOT/data/outbox/frontend_smoke.log"
END=$(date +%s%3N)
export DURATION_MS=$((END - START))
export COVERAGE
BASELINE=150
export BASELINE
PERF_DELTA=$(python3 - <<PY
from __future__ import annotations
import os
baseline = int(os.environ["BASELINE"])
duration = int(os.environ["DURATION_MS"])
print(((duration - baseline) / baseline) * 100)
PY
)
export PERF_DELTA
python3 - <<PY
import json, os
root = os.getenv("ROOT")
metrics = {
    "coverage": float(os.environ["COVERAGE"]),
    "perf_latency_pct": float(os.environ["PERF_DELTA"]),
    "duration_ms": int(os.environ["DURATION_MS"]),
    "notes": "Coverage via llvm-cov on frontends/samples/sample.cpp"
}
with open(os.path.join(root, "reports", "metrics.json"), "w", encoding="utf-8") as fh:
    json.dump(metrics, fh, indent=2)
print(f"[measure] coverage={metrics['coverage']:.2f}% perf_delta={metrics['perf_latency_pct']:.2f}% duration_ms={metrics['duration_ms']}")
PY
