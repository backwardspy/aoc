//! this solution is effectively the same as bulk python one.
//! the main difference is we let the compiler just embed the whole file into
//! the binary rather than reading it at runtime. there's not really a good
//! reason for this, other than to offer another alternative method.
//! i also use rust's functional idioms rather than the more imperative
//! approach taken in the python implementations.
use std::error::Error;

const INPUT: &'static str = include_str!("input");

fn main() -> Result<(), Box<dyn Error>> {
    let mut sums = INPUT
        .split("\n\n")
        .map(|block| {
            block
                .split("\n")
                .map(|number| number.parse::<i32>())
                .collect::<Result<Vec<_>, _>>()
                .map(|counts| counts.into_iter().sum())
        })
        .collect::<Result<Vec<i32>, _>>()?;

    sums.sort_by(|a, b| b.cmp(a));

    let solution_1 = sums[0];
    println!("solution 1: {solution_1}");

    let solution_2: i32 = sums[..3].into_iter().sum();
    println!("solution 2: {solution_2}");

    Ok(())
}
