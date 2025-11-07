# TriSynk Agent Charter

## Communication & Artifacts
- **User-facing dialogue:** Russian only. Technical artifacts (code, docs, configs) must be English.
- **Traceability:** Every automated action logs a summary into `.agents/context/YYYY-MM-DD_topic_context.jsonl` referencing concrete files/anchors.

## Mission
Deliver flagship-grade TriSynk Core platform: deterministic semantics, multi-frontend interoperability (Rust/C++/Python/TypeScript), and agent-centric automation with ≥85% coverage and <5% perf regression vs native baselines.

## Priorities
1. **Correctness & Formalism** – no undefined behaviour, every module tied to specs/tests/proofs.
2. **Performance First** – optimise memory/layout/runtime before readability; document trade-offs succinctly.
3. **Autonomy** – plan tasks >30 minutes, avoid waiting for user approval, keep working beyond “small” goals.
4. **Security & Compliance** – enforce capability policies, zero mocks/fakes in production paths.

## Workflow
1. **Plan** – decompose tasks, log plan via `update_plan` or dedicated context entry.
2. **Specify** – update/consult docs (`docs/*.md`, `docs/frontends.md`, `docs/intent-dsl.md`) before coding.
3. **Implement** – prefer MCP tools, apply_patch; keep code modular (DDD, Ports & Adapters, ModularMonolith_First).
4. **Validate** – run `scripts/run_checks.sh` plus relevant linters/tests; add new tests to keep ≥85% coverage.
5. **Record & Commit** – update `.agents/context`, commit with Conventional Commits, push immediately; reference issues/intents in messages.

## Tools & Scripts
- `scripts/run_checks.sh` – baseline docs + lint + export + sync dry-run.
- `scripts/lint_intents.sh`, `scripts/validate_issues.py` – governance for intents/issues.
- `scripts/export_graph.py`, `scripts/sync_issues.py` – keep GitHub Project in sync.
- Secrets: store local tokens under `.agents/secrets/` (ignored) and reference them via env vars when running sync scripts; production workflows consume repository secret `SYNC_GH_TOKEN`.
- `scripts/check_metrics.py` (coverage/perf), `scripts/test_frontends.py` (валидирует JSON прототипов) и `scripts/update_metrics_history.py` (архивирование), плюс специализированные инструменты под `scripts/` или `.agents/tools/`.
- Шаблоны и схемы лежат в `schema/` (например, `frontend_ir.schema.json`).

## Documentation & Specs
- Vision/strategy: `docs/vision.md`, `docs/architecture.md`, `docs/roadmap.md`, `docs/frontends.md`.
- Semantics: `docs/core-spec.md`, `docs/intent-dsl.md`, `docs/issues.md` (+ `intents/*.yaml`).
- Governance: `docs/git-projects.md`, AGENTS.md (this file).

## Quality Gates
- **Coverage:** ≥85% per deliverable; enforce via metrics in CI.
- **Performance:** ≤5% latency regression vs native baseline; record telemetry in `reports/`.
- **CI Enforcement:** `.github/workflows/ci.yml` + `.github/workflows/sync-issues.yml` must pass before merge.

## Prohibited Practices
- Introducing mocks/fakes/stubs in production.
- Reverting user changes without explicit direction.
- Skipping specs/tests or leaving undocumented behaviour.

## Escalation Protocol
- If blockers (missing secrets, upstream outage) arise, document in `.agents/context/...` and propose mitigation before pausing.
- Never request user to run commands unless no other options exist; instead, provide automation/scripts.
