# Architecture Blueprint

## 1. Layer Stack
1. **Intent Layer:** DSL + spec repository feeding agent planners (see [Intent DSL](intent-dsl.md)).
2. **Synthesis Layer:** Multi-frontend compilers (Rust/Python/C++/TS) desugaring into `clmr` IR with embedded contracts.
3. **Verification Layer:** Ownership/effect/resource passes + SMT/Lean proofs.
4. **Optimization Layer:** Profile-guided transforms, autotuners, layout synthesis.
5. **Runtime Layer:** Deterministic scheduler, capability-managed memory, interop bridges.

## 2. Agent Loop
1. Agent ingests requirements → `.agents/context` entry.
2. Generates intent DSL artifact per [intent-dsl.md](intent-dsl.md) referencing [Core Spec](core-spec.md) sections.
3. Requests compiler frontends for skeletons; receives `clmr` IR with inline contracts.
4. Runs proof and property pipelines; failures emit actionable issue templates referencing [Issues](issues.md).
5. Successful builds pass through autotuners + telemetry hooks, then get packaged with ABI manifests.

## 3. Module Breakdown
- **Frontends:** `trisynk-rs`, `trisynk-cpp`, `trisynk-py`, `trisynk-ts`.
- **IR Tooling:** `clmr-opt`, `clmr-lower`, `clmr-viz`.
- **Runtime Services:** `scheduler`, `memory`, `interop-rust`, `interop-cpp`, `interop-hpy`, `interop-js`.
- **Governance:** policy engine enforcing capability budgets defined in `docs/core-spec.md#4-abi--interoperability`.

## 4. Data Flows
- Telemetry events flow from runtime → `agents-observer` → feedback into intent planner.
- Coverage + proof artifacts stored per build and indexed by issue IDs.
- Git Projects board consumes roadmap milestones to auto-populate lanes.

## 5. Security & Safety
- Strict compartmentalization for dynamic languages; only deterministic projections cross boundaries.
- Mandatory attestation for third-party libraries (hash + capability manifest) before linking.
- Continuous monitoring hooks escalate anomalies to governance policies.

## 6. References
- Requirements: [Vision](vision.md)
- Semantics: [Core Specification](core-spec.md)
- Intent: [Intent DSL](intent-dsl.md)
- Timeline: [Roadmap](roadmap.md)
- Execution: [Issues](issues.md)
- Governance: [Git Projects Model](git-projects.md)
