use criterion::{criterion_group, criterion_main, Criterion};
use trisynk_demo::accumulate;

fn bench_accumulate(c: &mut Criterion) {
    let data: Vec<i64> = (0..10_000).collect();
    c.bench_function("accumulate", |b| b.iter(|| accumulate(&data)));
}

criterion_group!(benches, bench_accumulate);
criterion_main!(benches);
