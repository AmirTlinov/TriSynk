pub fn accumulate(input: &[i64]) -> i64 {
    input.iter().copied().sum()
}

#[cfg(test)]
mod tests {
    use super::accumulate;

    #[test]
    fn sums_values() {
        assert_eq!(accumulate(&[1, 2, 3]), 6);
    }
}
