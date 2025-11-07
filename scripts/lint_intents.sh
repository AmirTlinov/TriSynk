#!/usr/bin/env bash
set -euo pipefail

shopt -s nullglob
files=(intents/*.yaml)

if (( ${#files[@]} == 0 )); then
  echo "[lint-intents] No intent files found; skipping" >&2
  exit 0
fi

for file in "${files[@]}"; do
  echo "[lint-intents] Validating $file"
  .agents/tools/intent_schema.py < "$file"
done

echo "[lint-intents] All intents valid"
