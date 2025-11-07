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
  scripts/check_metrics.py
  .env.example
  AGENTS.md
  docs/frontends.md
  intents/INT-2025-0001.yaml
  intents/INT-2025-0002.yaml
  intents/INT-2025-0003.yaml
  intents/INT-2025-0004.yaml
  intents/INT-2025-0005.yaml
  intents/INT-2025-0006.yaml
  intents/INT-2025-0007.yaml
  intents/INT-2025-0008.yaml
  intents/INT-2025-0009.yaml
  intents/INT-2025-0010.yaml
  intents/INT-2025-0011.yaml
  data/outbox/issues_intents.json
  reports/metrics.json
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
scripts/check_metrics.py

echo "[PASS] Documentation baseline + linting verified."
