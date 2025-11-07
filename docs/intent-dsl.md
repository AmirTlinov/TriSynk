# Intent DSL & Agent Workflow

## 1. Goals
- Provide a machine-friendly contract that captures problem statements, SLOs, resource budgets, and interop needs.
- Drive automated synthesis → verification → deployment without human intervention.
- Ensure each intent links to roadmap phase, issue ID, and documentation anchors.

## 2. Document Structure
```yaml
intent: trisynk.v1
meta:
  id: INT-2025-0001
  owner: agent://builder-alpha
  issue: ISS-003
  roadmap: Phase-2
  state: open
  docs:
    - core-spec.md#1-semantic-kernel
    - intent-dsl.md#3-schema
requirements:
  goal: "Translate Rust borrowing rules into clmr IR"
  success_metrics:
    coverage: ">=0.9"
    latency_ms: 50
constraints:
  effects: [io, gpu]
  resources:
    memory_mb: 512
    time_min: 5
interop:
  consumes: ["crate://serde", "npm://buffer"]
  produces: ["abi://trisynk_fastcall"]
verifications:
  proofs: ["lean://ownership_soundness"]
  tests: ["suite://frontend_rust"]
telemetry:
  slos:
    intent_to_binary_min: 5
    crash_free_pct: 100
```

## 3. Schema
- `intent`: DSL version.
- `meta`: identifiers and traceability info linking to [roadmap.md](roadmap.md) and [issues.md](issues.md). Optional `state` (`open`, `in_progress`, `closed`) drives GitHub issue status during synchronization.
- `requirements`: natural language goal + structured metrics.
- `constraints`: effect sets + resource budgets, validated against [core-spec.md#2-type-system](core-spec.md#2-type-system).
- `interop`: declares external assets; compiler generates capability manifests.
- `verifications`: required proof/test artifacts; CI rejects intents lacking references.
- `telemetry`: SLAs feeding runtime policy engine described in [architecture.md#4-data-flows](architecture.md#4-data-flows).

## 4. Agent Workflow Hooks
1. **Ingest:** agent creates YAML intent and stores pointer in `.agents/context`.
2. **Plan:** map intent `meta.issue` to roadmap tasks.
3. **Synthesize:** frontends generate `clmr` IR skeletons with embedded metadata.
4. **Verify:** run proofs/tests; results logged back into intent record.
5. **Deploy:** attach ABI manifest + telemetry configuration.

## 5. Validation Rules
- YAML must pass schema in `.agents/tools/intent_schema.py` (enforced by [ISS-009](issues.md#iss-009)).
- Missing `docs` references cause CI failure.
- Resource budgets enforced at runtime via capability governance (see [core-spec.md#5-runtime-contracts](core-spec.md#5-runtime-contracts)).

## 6. References
- [Vision](vision.md)
- [Core Specification](core-spec.md)
- [Architecture](architecture.md)
- [Roadmap](roadmap.md)
- [Issues](issues.md)
