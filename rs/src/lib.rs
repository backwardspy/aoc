use std::{
    error::Error,
    fmt::{self, Display},
    fs, io,
    path::Path,
};

pub fn read_input(day: &str) -> Result<String, io::Error> {
    let path = Path::new("../inputs").join(day);
    fs::read_to_string(path)
}

#[derive(Debug, Clone, Copy)]
pub enum AOCError {
    BadInput,
    LogicError,
}

impl Display for AOCError {
    fn fmt(&self, writer: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::BadInput => write!(
                writer,
                "bad input data, make sure you're loading the correct day's input"
            ),
            Self::LogicError => write!(
                writer,
                "something is wrong with your solution's logic, dummy"
            ),
        }
    }
}

impl Error for AOCError {}
