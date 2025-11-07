#!/usr/bin/env bash
set -euo pipefail

required_files=(
  docs/vision.md
  docs/core-spec.md
  docs/architecture.md
  docs/intent-dsl.md
  docs/roadmap.md
  docs/issues.md
  docs/git-projects.md
  .agents/context/2025-11-06_trisynk_core_context.jsonl
  .agents/tools/intent_schema.py
  scripts/lint_intents.sh
  scripts/validate_issues.py
  scripts/export_graph.py
  scripts/sync_issues.py
  .env.example
  intents/INT-2025-0001.yaml
  data/outbox/issues_intents.json
)

for f in "${required_files[@]}"; do
  if [[ ! -s "$f" ]]; then
    echo "[FAIL] Missing or empty $f" >&2
    exit 1
  fi
  echo "[OK] $f"
done


scripts/lint_intents.sh
scripts/validate_issues.py
scripts/export_graph.py --output data/outbox/issues_intents.json
scripts/sync_issues.py > /dev/null

echo "[PASS] Documentation baseline + linting verified."
