# Issue Graph

## ISS-001 – Formalize Ownership & Borrow Checker
- **Scope:** Implement affine ownership rules from [core-spec.md#1-semantic-kernel](core-spec.md#1-semantic-kernel).
- **Deliverables:** SMT lemmas, compiler diagnostics catalog.
- **Dependencies:** [ISS-002](#iss-002).

## ISS-002 – Capability Graph & Effect Contracts
- **Scope:** Build capability registry per [core-spec.md#2-type-system](core-spec.md#2-type-system).
- **Deliverables:** Contract schema + verification pass (see [architecture.md#2-agent-loop](architecture.md#2-agent-loop)).
- **Dependencies:** None.

## ISS-003 – Rust Frontend Prototype
- **Scope:** Parse Rust subset → `clmr` IR referencing [architecture.md#3-module-breakdown](architecture.md#3-module-breakdown) and [frontends.md#2-trisynk-rs-frontend](frontends.md#2-trisynk-rs-frontend).
- **Deliverables:** Frontend CLI, regression tests covering 95% grammar features.
- **Dependencies:** [ISS-001](#iss-001).

## ISS-004 – C++ Frontend Prototype
- **Scope:** Clang-based importer aligning with [core-spec.md#4-abi--interoperability](core-spec.md#4-abi--interoperability) and [frontends.md#3-trisynk-cpp-frontend](frontends.md#3-trisynk-cpp-frontend).
- **Deliverables:** Template instantiation strategy, ABI compliance suite.
- **Dependencies:** [ISS-002](#iss-002).

## ISS-005 – Python/HPy Translator
- **Scope:** Deterministic compartment wrapper referencing [architecture.md#5-security--safety](architecture.md#5-security--safety).
- **Deliverables:** HPy capsules, dynamic capability sandbox tests.
- **Dependencies:** [ISS-003](#iss-003).

## ISS-006 – TypeScript/JS Translator
- **Scope:** QuickJS/V8 integration per [core-spec.md#4-abi--interoperability](core-spec.md#4-abi--interoperability).
- **Deliverables:** d.ts → capability compiler, Promise/async bridge tests.
- **Dependencies:** [ISS-002](#iss-002).

## ISS-007 – Deterministic Runtime Core
- **Scope:** Scheduler + memory arenas per [core-spec.md#5-runtime-contracts](core-spec.md#5-runtime-contracts).
- **Deliverables:** Latency benchmarks, telemetry hooks.
- **Dependencies:** [ISS-001](#iss-001), [ISS-002](#iss-002).

## ISS-008 – Interop Bridges (HPy & V8)
- **Scope:** Runtime adapters referencing [architecture.md#3-module-breakdown](architecture.md#3-module-breakdown).
- **Deliverables:** FFI conformance harness, failure diagnostics.
- **Dependencies:** [ISS-005](#iss-005), [ISS-006](#iss-006).

## ISS-009 – Intent DSL & Agent Tooling
- **Scope:** Define DSL schema and tooling per [intent-dsl.md](intent-dsl.md) and [architecture.md#2-agent-loop](architecture.md#2-agent-loop).
- **Deliverables:** Schema, editor plugins, validation suite (`.agents/tools/intent_schema.py`).
- **Dependencies:** [ISS-003](#iss-003)–[ISS-006](#iss-006).

## ISS-010 – Autotuning & Telemetry Platform
- **Scope:** Performance services described in [architecture.md#4-data-flows](architecture.md#4-data-flows).
- **Deliverables:** Profilers, regression dashboards.
- **Dependencies:** [ISS-007](#iss-007).

## ISS-011 – Security Hardening & Policy Engine
- **Scope:** Capability enforcement + attestation, referencing [architecture.md#5-security--safety](architecture.md#5-security--safety).
- **Deliverables:** Policy DSL, automated audits.
- **Dependencies:** [ISS-007](#iss-007), [ISS-008](#iss-008).
