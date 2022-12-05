use std::{
    error::Error,
    fmt::{self, Display},
};

use aoc_rs::{read_input, AOCError};
use bimap::BiMap;

#[derive(PartialEq, Eq, Clone, Copy, Hash)]
enum Shape {
    Rock,
    Paper,
    Scissors,
}

impl Display for Shape {
    fn fmt(&self, writer: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::Rock => write!(writer, "rock"),
            Self::Paper => write!(writer, "paper"),
            Self::Scissors => write!(writer, "scissors"),
        }
    }
}

impl Shape {
    fn score(&self) -> i32 {
        match self {
            Self::Rock => 1,
            Self::Paper => 2,
            Self::Scissors => 3,
        }
    }

    fn associativity() -> BiMap<Shape, Shape> {
        BiMap::from_iter(
            [
                (Shape::Rock, Shape::Scissors),
                (Shape::Paper, Shape::Rock),
                (Shape::Scissors, Shape::Paper),
            ]
            .into_iter(),
        )
    }

    fn beats(&self) -> Result<Self, AOCError> {
        Ok(*Self::associativity()
            .get_by_left(self)
            .ok_or(AOCError::LogicError)?)
    }

    fn loses_to(&self) -> Result<Self, AOCError> {
        Ok(*Self::associativity()
            .get_by_right(self)
            .ok_or(AOCError::LogicError)?)
    }

    fn from_symbol(sym: char) -> Result<Self, AOCError> {
        match sym {
            'A' | 'X' => Ok(Self::Rock),
            'B' | 'Y' => Ok(Self::Paper),
            'C' | 'Z' => Ok(Self::Scissors),
            _ => Err(AOCError::BadInput),
        }
    }
}

fn line_symbols(line: &str) -> Result<(char, char), AOCError> {
    if line.len() != 3 {
        return Err(AOCError::BadInput);
    }

    let mut chars = line.chars();
    let first = chars.next().ok_or(AOCError::BadInput)?;
    chars.next();
    let second = chars.next().ok_or(AOCError::BadInput)?;

    Ok((first, second))
}

mod part1 {
    use crate::AOCError;

    use super::{line_symbols, Shape};

    pub struct Turn {
        opponent: Shape,
        strategy: Shape,
    }

    impl Turn {
        pub fn score(&self) -> Result<i32, AOCError> {
            Ok((if self.opponent.beats()? == self.strategy {
                0
            } else if self.strategy.beats()? == self.opponent {
                6
            } else {
                3
            }) + self.strategy.score())
        }
    }

    pub fn line_to_turn(line: &str) -> Result<Turn, AOCError> {
        let (opponent_symbol, strategy_symbol) = line_symbols(line)?;
        Ok(Turn {
            opponent: Shape::from_symbol(opponent_symbol)?,
            strategy: Shape::from_symbol(strategy_symbol)?,
        })
    }

    pub fn line_to_score(line: &str) -> Result<i32, AOCError> {
        line_to_turn(line)?.score()
    }
}

mod part2 {
    use crate::AOCError;

    use super::{line_symbols, Shape};

    enum Outcome {
        Lose,
        Draw,
        Win,
    }

    impl Outcome {
        fn from_symbol(symbol: char) -> Result<Self, AOCError> {
            match symbol {
                'X' => Ok(Outcome::Lose),
                'Y' => Ok(Outcome::Draw),
                'Z' => Ok(Outcome::Win),
                _ => Err(AOCError::BadInput),
            }
        }
    }

    pub struct Turn {
        opponent: Shape,
        strategy: Outcome,
    }

    impl Turn {
        pub fn score(&self) -> Result<i32, AOCError> {
            let shape = match self.strategy {
                Outcome::Lose => self.opponent.beats()?,
                Outcome::Draw => self.opponent,
                Outcome::Win => self.opponent.loses_to()?,
            };

            Ok((match self.strategy {
                Outcome::Lose => 0,
                Outcome::Draw => 3,
                Outcome::Win => 6,
            }) + shape.score())
        }
    }

    pub fn line_to_turn(line: &str) -> Result<Turn, AOCError> {
        let (opponent_symbol, strategy_symbol) = line_symbols(line)?;
        Ok(Turn {
            opponent: Shape::from_symbol(opponent_symbol)?,
            strategy: Outcome::from_symbol(strategy_symbol)?,
        })
    }

    pub fn line_to_score(line: &str) -> Result<i32, AOCError> {
        line_to_turn(line)?.score()
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input("day2")?;
    let part_1: i32 = input
        .split("\n")
        .filter(|line| line.len() > 0)
        .map(part1::line_to_score)
        .collect::<Result<Vec<i32>, AOCError>>()?
        .into_iter()
        .sum();
    println!("part 1: {}", part_1);

    let part_2: i32 = input
        .split("\n")
        .filter(|line| line.len() > 0)
        .map(part2::line_to_score)
        .collect::<Result<Vec<i32>, AOCError>>()?
        .into_iter()
        .sum();
    println!("part 2: {}", part_2);

    Ok(())
}
