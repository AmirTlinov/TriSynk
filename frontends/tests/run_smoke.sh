#!/usr/bin/env bash
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
rs_out="$root/frontends/samples/sample.rs.json"
cpp_out="$root/frontends/samples/sample.cpp.json"

python3 "$root/frontends/trisynk-rs/frontend.py" "$root/frontends/samples/sample.rs" --output "$rs_out"
python3 "$root/frontends/trisynk-cpp/frontend.py" "$root/frontends/samples/sample.cpp" --output "$cpp_out"

for file in "$rs_out" "$cpp_out"; do
  [[ -s "$file" ]] || { echo "[smoke] Missing $file"; exit 1; }
  echo "[smoke] Generated $file"
  python3 -m json.tool "$file" > /dev/null
  rm "$file"
done
