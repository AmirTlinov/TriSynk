#!/usr/bin/env bash
set -euo pipefail

required_files=(
  docs/vision.md
  docs/core-spec.md
  docs/architecture.md
  docs/roadmap.md
  docs/issues.md
  docs/git-projects.md
  .agents/context/2025-11-06_trisynk_core_context.jsonl
)

for f in "${required_files[@]}"; do
  if [[ ! -s "$f" ]]; then
    echo "[FAIL] Missing or empty $f" >&2
    exit 1
  fi
  echo "[OK] $f"
done

echo "[PASS] Documentation baseline verified."
