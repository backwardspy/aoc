use std::error::Error;

use aoc_rs::read_input;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input("day1")?;
    let mut sums = input
        .split("\n\n")
        .map(|block| {
            block
                .split('\n')
                .map(|number| number.parse::<i32>())
                .collect::<Result<Vec<_>, _>>()
                .map(|counts| counts.into_iter().sum())
        })
        .collect::<Result<Vec<i32>, _>>()?;

    sums.sort_by(|a, b| b.cmp(a));

    let solution_1 = sums[0];
    println!("solution 1: {solution_1}");

    let solution_2: i32 = sums[..3].iter().sum();
    println!("solution 2: {solution_2}");

    Ok(())
}
