fn increment(mut value: i64) -> i64 {
    value += 1;
    value
}

fn consume_slice(slice: &[u8]) -> usize {
    slice.len()
}
