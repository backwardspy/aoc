use std::{collections::HashSet, error::Error};

use aoc_rs::{read_input, AOCError};
use itertools::Itertools;

fn middle_split(line: &str) -> (&str, &str) {
    let mid = line.len() / 2;
    (&line[..mid], &line[mid..])
}

fn ord(c: char) -> i32 {
    // this is horrible
    let ascii_code = c as u32;
    ascii_code as i32
}

fn priority(c: char) -> i32 {
    match c {
        // hack time
        'a'..='z' => ord(c) - 96,
        'A'..='Z' => ord(c) - 65 + 27,
        _ => 0,
    }
}

fn str_to_set(string: &str) -> HashSet<char> {
    HashSet::<char>::from_iter(string.chars())
}

fn pair_to_sets(pair: (&str, &str)) -> (HashSet<char>, HashSet<char>) {
    // makes up for a lack of tuple mapping capabilities in rust as of yet
    (str_to_set(pair.0), str_to_set(pair.1))
}

fn common_priority(sets: Vec<HashSet<char>>) -> Result<i32, AOCError> {
    // TODO: look at using retain instead of intersection
    // so we can take a vec that work works because we own the hashsets now
    // that seems inefficient though...
    let intersection = sets
        .into_iter()
        .reduce(|a, b| a.intersection(&b).copied().collect())
        .ok_or(AOCError::LogicError)?;

    intersection
        .into_iter()
        .next()
        .ok_or(AOCError::LogicError)
        .map(priority)
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input("day3")?;
    let lines = input.split('\n').filter(|line| line.is_empty());

    // part 1
    let priority_sum: i32 = lines
        .clone()
        .map(middle_split)
        .map(pair_to_sets)
        .map(|pair| common_priority(vec![pair.0, pair.1]))
        .collect::<Result<Vec<_>, _>>()?
        .into_iter()
        .sum();
    println!("part 1: {priority_sum}");

    // part 2
    let priority_sum: i32 = lines
        .chunks(3)
        .into_iter()
        .map(|chunk| common_priority(chunk.map(str_to_set).collect()))
        .collect::<Result<Vec<_>, _>>()?
        .into_iter()
        .sum();
    println!("part 2: {priority_sum}");

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::priority;

    #[test]
    fn does_priority_work_properly() {
        assert_eq!(priority('a'), 1);
        assert_eq!(priority('z'), 26);
        assert_eq!(priority('A'), 27);
        assert_eq!(priority('Z'), 52);
    }
}
