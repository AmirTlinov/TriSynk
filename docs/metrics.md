# Metrics & Dashboards

## Coverage & Performance
1. `scripts/measure_metrics.sh` builds `frontends/samples/sample.cpp` with `clang++` instrumentation, runs it, and collects coverage via `llvm-profdata`/`llvm-cov`.
2. `scripts/run_cargo_metrics.sh` (best-effort) runs `cargo-llvm-cov` and Criterion benches inside `metrics/demo/` when the tools are installed. Results are written to `reports/cargo_metrics.json`.
3. `scripts/update_metrics_history.py` appends every measurement to `reports/history/metrics_history.jsonl`.
4. `scripts/update_dashboard.py` converts the history into `reports/dashboard/metrics_dashboard.json` for visualization in Grafana/Observable.

## Dashboard Consumption
- Export `reports/dashboard/metrics_dashboard.json` to the BI system of choice (Grafana/observable) using a file-based datasource or by pushing to S3/OSS.
- Each entry contains timestamp, coverage, perf delta, and duration. Attach additional series (cargo metrics) by merging `reports/cargo_metrics.json`.

## Future Work
- Integrate `cargo-llvm-cov` in CI runners (install `cargo-llvm-cov` binary) to gather real Rust coverage.
- Configure Criterion to emit JSON and feed it into the dashboard script for latency regressions.
- Publish dashboards via GitHub Pages or internal Grafana instance.
