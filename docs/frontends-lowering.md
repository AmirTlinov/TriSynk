# Frontend Lowering Plan

## Goals
- Leverage native toolchains (`rustc`, `clang++`) to emit MIR/AST and convert them into the `clmr` dialect.
- Attach precise capability/ABI metadata while preserving provenance (source spans, traits, templates).
- Provide integration tests that invoke real compilers on curated samples.

## Roadmap
1. **Rust Staging Driver**
   - Use `rustc --emit=mir -Zunstable-options --mir-json` (nightly) against samples in `frontends/samples/*.rs`.
   - Parse MIR JSON in Python/Rust to build the `clmr` tree; emit artifacts under `data/outbox/rust_lowering/` for inspection.
   - Integration test `frontends/tests/run_toolchain.sh` ensures `rustc` availability and compiles fixtures.
2. **Clang Importer**
   - Execute `clang++ -Xclang -ast-dump=json` on `frontends/samples/*.cpp` to obtain structured AST.
   - Implement translator that converts AST nodes (FunctionDecl, ParmVarDecl, TemplateDecl) into IR ops with capability manifests.
3. **Consistency Checks**
   - Compare prototype JSON (regex-based) with real lowering results; add regression tests in `frontends/tests/run_toolchain.sh`.
   - Extend `schema/frontend_ir.schema.json` with compiler-specific metadata (hashes, provenance IDs).
4. **Performance Harness**
   - Run compiled binaries with `LLVM_PROFILE_FILE` instrumentation and feed results into `scripts/measure_metrics.sh` for real coverage/perf tracking.

## Dependencies
- `rustc` nightly toolchain (for MIR JSON) and `clang++` (>=15) with `llvm-cov`, `llvm-profdata`.
- Python bindings for schema validation (already provided via `scripts/test_frontends.py`).

## Next Steps
- Implement MIR JSON parser in Rust crate under `frontends/trisynk-rs/driver/`.
- Prototype Clang AST ingestion script and connect it to `frontends/tests/run_toolchain.sh`.
- Feed resulting artifacts into `reports/history/metrics_history.jsonl` for visibility.

## Current Automation
- `scripts/run_lowering.sh` produces baseline artifacts:
  - Rust MIR dump → `data/outbox/lowering/rust/sample.mir` (via `rustc -Zunpretty=mir`).
  - Clang AST JSON → `data/outbox/lowering/clang/sample.ast.json` (`clang++ -Xclang -ast-dump=json`).
- These files seed the upcoming lowerers and are invoked automatically from `scripts/run_checks.sh`.
