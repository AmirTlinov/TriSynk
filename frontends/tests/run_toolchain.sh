#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
SAMPLE_RS="$ROOT/frontends/samples/borrows.rs"
SAMPLE_CPP="$ROOT/frontends/samples/sample.cpp"
TEMPLATE_CPP="$ROOT/frontends/samples/templates.cpp"
TMP_DIR="$ROOT/data/outbox/toolchain"
mkdir -p "$TMP_DIR"

rustc --version > "$TMP_DIR/rustc_version.txt"
clang++ --version > "$TMP_DIR/clang_version.txt"

rustc "$SAMPLE_RS" -o "$TMP_DIR/borrows_bin"
"$TMP_DIR/borrows_bin" > "$TMP_DIR/borrows.out"

clang++ -std=c++20 "$TEMPLATE_CPP" -c -o "$TMP_DIR/templates.o"
clang++ -std=c++20 -fprofile-instr-generate -fcoverage-mapping "$SAMPLE_CPP" -o "$TMP_DIR/sample_bin"
LLVM_PROFILE_FILE="$TMP_DIR/sample.profraw" "$TMP_DIR/sample_bin"
