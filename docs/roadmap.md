# Roadmap & Milestones

## Phase 0 – Repository Bootstrap (Week 45 2025)
- Finalize vision, spec, architecture (see [docs](./)).
- Stand up Git Projects board (see [git-projects.md](git-projects.md)).

## Phase 1 – Core Definition (Weeks 46–50 2025)
- Deliver semantic kernel prototype per [core-spec.md#1-semantic-kernel](core-spec.md#1-semantic-kernel).
- Draft ownership/effect proof obligations (issues [ISS-001](issues.md#iss-001) and [ISS-002](issues.md#iss-002)).
- Produce baseline `.agents/context` entries for each subsystem.

## Phase 2 – Frontend & IR Tooling (Weeks 51–2 2026)
- Implement Rust & C++ frontends (issues [ISS-003](issues.md#iss-003) / [ISS-004](issues.md#iss-004)).
- Add Python/TypeScript translators (issues [ISS-005](issues.md#iss-005) / [ISS-006](issues.md#iss-006)).
- Build `clmr` optimization passes per [architecture.md#2-agent-loop](architecture.md#2-agent-loop).

## Phase 3 – Runtime & Interop (Weeks 3–8 2026)
- Ship deterministic scheduler + capability allocator ([ISS-007](issues.md#iss-007)).
- Complete HPy and V8 bridges ([ISS-008](issues.md#iss-008)).
- Validate ABI via sample workloads; require <5% overhead vs native baselines.

## Phase 4 – Agent Automation (Weeks 9–12 2026)
- Intent DSL authoring tools + verification harness per [intent-dsl.md](intent-dsl.md) ([ISS-009](issues.md#iss-009)).
- Autotuning/profiling services + telemetry feedback ([ISS-010](issues.md#iss-010)).

## Phase 5 – Hardening & Release (Weeks 13–16 2026)
- Red-team audits, capability policy enforcement ([ISS-011](issues.md#iss-011)).
- Freeze v1 ABI, publish SDKs, document upgrade path.

## Deliverable Exit Criteria
- ≥85% coverage across core modules.
- All roadmap milestones linked to closed issues with references to relevant docs.
- Telemetry dashboards prove intent→binary SLA <5 minutes on reference hardware.
