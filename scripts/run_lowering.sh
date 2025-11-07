#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
RUST_SAMPLE="$ROOT/frontends/samples/sample.rs"
CLANG_SAMPLE="$ROOT/frontends/samples/sample.cpp"
RUST_OUT="$ROOT/data/outbox/lowering/rust/sample.mir"
CLANG_OUT="$ROOT/data/outbox/lowering/clang/sample.ast.json"

log() { printf '[lowering] %s\n' "$1"; }

run_rust_lowering() {
  if ! command -v rustc >/dev/null 2>&1; then
    echo 'rustc not found; install Rust toolchain' > "$RUST_OUT"
    log "rustc missing"
    return
  fi

  if rustc --version | grep -qi nightly; then
    if rustc -Zunpretty=mir "$RUST_SAMPLE" > "$RUST_OUT" 2>"$RUST_OUT.err"; then
      rm -f "$RUST_OUT.err"
      log "wrote MIR via rustc nightly"
      return
    fi
  fi

  if command -v rustup >/dev/null 2>&1 && rustup toolchain list | grep -q nightly; then
    if rustup run nightly rustc -Zunpretty=mir "$RUST_SAMPLE" > "$RUST_OUT" 2>"$RUST_OUT.err"; then
      rm -f "$RUST_OUT.err"
      log "wrote MIR via rustup nightly"
      return
    fi
  fi

  echo 'nightly rustc not available; install with `rustup toolchain install nightly`' > "$RUST_OUT"
  log "rust MIR generation skipped (nightly unavailable)"
}

run_clang_lowering() {
  if ! command -v clang++ >/dev/null 2>&1; then
    echo 'clang++ not found; install LLVM/Clang >=15' > "$CLANG_OUT"
    log "clang++ missing"
    return
  fi

  if clang++ -std=c++20 -Xclang -ast-dump=json -fsyntax-only "$CLANG_SAMPLE" > "$CLANG_OUT" 2>"$CLANG_OUT.err"; then
    rm -f "$CLANG_OUT.err"
    log "wrote Clang AST JSON"
  else
    echo 'failed to dump AST; see .err' > "$CLANG_OUT"
    log "clang AST dump failed"
  fi
}

mkdir -p "$(dirname "$RUST_OUT")" "$(dirname "$CLANG_OUT")"
run_rust_lowering
run_clang_lowering
