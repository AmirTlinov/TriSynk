# TriSynk Core Specification

## 1. Semantic Kernel
- **Memory Model:** Sequential consistency with deterministic DMA windows; data races rejected at compile time.
- **Ownership:** Affine ownership + lexical borrowing with compile-time move semantics; capability tokens encode mutability and aliasing rights.
- **Effects:** Every callable declares `effects {io, gpu, fs, net, dyn}`; effects compose via capability graph checks.
- **Determinism:** Dynamic features (Python objects, JS proxies) are wrapped inside capability compartments that expose only deterministic projections to the core.

## 2. Type System
- Unified trait system bridging Rust traits, C++ concepts, Python protocols, and TypeScript structural types.
- Trait objects carry evidence records for runtime dispatch; erased layouts follow the `CoreTraitObject` ABI (data ptr, vtable ptr, capability ptr).
- Parametric polymorphism resolved via monomorphization in performance-critical paths and via witness tables when sharing binaries across languages.

## 3. Intermediate Representation (MLIR Dialect `clmr`)
- **SSA Regions:** Multi-entry regions model async tasks and effect scopes.
- **Metadata:** Each op attaches `intent`, `resource`, and `slo` attributes for agent reasoning.
- **Verification Passes:** Ownership, effect, and resource passes must succeed before lowering.
- **Lowerings:** `clmr` → LLVM IR (native), `clmr` → WASM (sandbox), `clmr` → C++ (interop stubs).

## 4. ABI & Interoperability
- Fixed calling convention (`trisynk_fastcall`) with 128-bit capability registers.
- **Rust:** Consume `rustc` metadata (`.json`) to auto-generate capability manifests.
- **C++:** Clang AST importer builds bindings; unsupported constructs rejected with actionable diagnostics.
- **Python:** HPy + custom capsule for capability handles; prohibits borrowing beyond scope boundaries.
- **TypeScript/JS:** QuickJS/V8 isolate adapters; TypeScript declarations compile into capability traits.

## 5. Runtime Contracts
- Deterministic scheduler with priority lanes (compute, io, gpu) and deadline-aware admission control.
- Memory arenas segmented per capability; GC optional and only within dynamic compartments.
- Telemetry bus streams metrics (`latency`, `alloc`, `effect-usage`) for agent feedback loops.

## 6. Tooling Requirements
- Intent DSL schema (see `docs/architecture.md#agent-loop`).
- Formal proof artifacts stored alongside binaries; Lean/SMT scripts treated as first-class build outputs.
- Security policies expressed via capability constraints and validated in CI.
