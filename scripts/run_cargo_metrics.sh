#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
CDIR="$ROOT/metrics/demo"
OUT="$ROOT/reports/cargo_metrics.json"
mkdir -p "$(dirname "$OUT")"

if ! command -v cargo >/dev/null; then
  echo "[cargo-metrics] cargo not found; writing placeholder" >&2
  echo '{"status":"missing_cargo"}' > "$OUT"
  exit 0
fi

if ! cargo llvm-cov --version >/dev/null 2>&1; then
  echo "[cargo-metrics] cargo llvm-cov not installed; writing placeholder" >&2
  echo '{"status":"missing_cargo_llvm_cov"}' > "$OUT"
  exit 0
fi

pushd "$CDIR" >/dev/null
cargo test >/dev/null
cargo llvm-cov --json --output-path coverage.json >/dev/null
if command -v cargo >/dev/null; then
  cargo bench -- --noplot >/dev/null || true
fi
popd >/dev/null

cat > "$OUT" <<JSON
{
  "status": "ok",
  "project": "trisynk-demo",
  "coverage_report": "metrics/demo/coverage.json"
}
JSON
