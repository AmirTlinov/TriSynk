# Frontend Prototype & ABI Contract

## 1. Overview
TriSynk frontends translate language-specific syntax (Rust/C++/Python/TypeScript) into the `clmr` IR while emitting ABI manifests that guarantee deterministic behaviour across runtimes. The initial focus is on `trisynk-rs` and `trisynk-cpp` to unlock high-performance systems code.

## 2. `trisynk-rs` Frontend
- **Scope:** Rust 2021 subset with ownership/lifetime semantics mapped 1:1 to the TriSynk affine model.
- **Pipeline:**
  1. Parse via `rustc` driver in incremental mode.
  2. Lower HIR → MIR → `clmr` using ownership/effect annotations from attributes.
  3. Emit ABI manifest describing layout, capabilities, and effect sets.
- **Prototype:** `frontends/trisynk-rs/frontend.py` parses sample Rust files and emits JSON approximating `clmr` IR; tests run via `frontends/tests/run_smoke.sh` and `scripts/test_frontends.py`.
- **Key Contracts:**
  - Lifetimes map to TriSynk borrow regions; unsafe blocks rejected unless annotated with capability tokens.
  - Traits compile to capability manifests referencing [`docs/core-spec.md#2-type-system`](core-spec.md#2-type-system).

- **Prototype:** `frontends/trisynk-cpp/frontend.py` inspects AST-like patterns and outputs ABI manifests referencing `trisynk_fastcall`; validated by the same smoke/tests pipeline.
## 3. `trisynk-cpp` Frontend
- **Scope:** C++20 core subset without UB-prone constructs (no raw pointer arithmetic without capability wrappers).
- **Pipeline:**
  1. Clang LibTooling AST exporter.
  2. Template instantiations resolved via policy described in [issues.md#iss-004](issues.md#iss-004).
  3. Generate `clmr` plus ABI manifest referencing `trisynk_fastcall` convention.
- **Key Contracts:**
  - Multiple inheritance flattened via trait object layout defined in [`docs/core-spec.md#4-abi--interoperability`](core-spec.md#4-abi--interoperability).
  - `constexpr` evaluated at compile time; side-effects flagged as violations.

## 4. Shared ABI/IR Requirements
- **Schema:** JSON outputs conform to `schema/frontend_ir.schema.json`; enforced by `scripts/test_frontends.py`.
- **IR Ops:** Each frontend must emit `clmr.module` with `intent`/`resource`/`slo` attributes for all functions.
- **ABI Manifests:** YAML/JSON descriptors listing exported symbols, layout hashes, capability requirements, telemetry hooks.
- **Validation:** `clmr-verify` pass ensures ownership/effect correctness before runtime linking.

## 5. Testing Roadmap
- Unit suites for parser/lowering (≥95% grammar coverage).
- Property tests comparing source semantics vs TriSynk runtime behaviour.
- Performance baselines stored in `reports/perf/baseline.json` per frontend.

## 6. References
- [Architecture Blueprint](architecture.md)
- [Core Specification](core-spec.md)
- [Issue Graph](issues.md)
- [Intent DSL](intent-dsl.md)
