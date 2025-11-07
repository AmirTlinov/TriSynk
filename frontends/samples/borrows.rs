fn increment(mut value: i64) -> i64 {
    value += 1;
    value
}

fn consume_slice(slice: &[u8]) -> usize {
    slice.len()
}

fn main() {
    let value = 41i64;
    let _ = increment(value);
    let data = [1u8, 2, 3, 4];
    let _ = consume_slice(&data);
}
