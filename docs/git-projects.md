# Git Projects Operating Model

## Board Layout
1. **Backlog (Linked to Roadmap):** auto-filled from [issues.md](issues.md) when `status=draft`.
2. **Spec Work:** tasks needing updates to [vision](vision.md), [core spec](core-spec.md), or [architecture](architecture.md).
3. **Execution:** implementation + verification tasks; blocked cards must cite capability/policy reason.
4. **Review & Proof:** formal verification, coverage, performance sign-off.
5. **Release:** only cards with telemetry + proof artifacts attached.

## Automation Rules
- Every card references at least one doc section anchor (e.g., `core-spec.md#3-intermediate-representation`).
- CI bots update card metrics (coverage, perf delta) after each pipeline run.
- When an issue closes, board card auto-moves to Release and records commit hash.

## Reporting
- Weekly snapshots stored in `.agents/context/YYYY-MM-DD_projects_context.jsonl`.
- Metrics exported: cycle time, verification duration, performance regressions.

## Governance
- Board steward ensures backlog stays ≤2 phases ahead of roadmap.
- Security reviews cannot be bypassed; cards without capability manifests are rejected.

## CI Integration
- Workflow [.github/workflows/ci.yml](../.github/workflows/ci.yml) blocks merges unless documentation, intent, and issue linting pass.
- Status checks surface coverage/perf metrics collected by future steps referenced in [roadmap.md](roadmap.md).
