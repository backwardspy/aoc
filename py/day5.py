"""
aoc day 5 - moving stacks of crates with a giant cargo crane!
"""
import re
from dataclasses import dataclass
from typing import Generator

FileLines = Generator[str, None, None]

# first dimension; columns
# second dimension; stacks of crates
CrateStacks = list[list[str]]


@dataclass(frozen=True)
class Instruction:
    """a single instruction for the crane to move a number of crates."""

    from_column: int
    to_column: int
    quantity: int


move_pattern = re.compile(r"^move (\d+) from (\d+) to (\d+)$")


def input_lines() -> FileLines:
    """yield lines from the input file with trailing newlinews removed."""
    with open("inputs/day5", "r", encoding="utf-8") as input_file:
        lines = (line.rstrip("\n") for line in input_file)
        yield from lines


def read_header_lines(lines: FileLines) -> FileLines:
    """
    consume & yield lines from the file until the first blank line is found.
    """
    for line in lines:
        if not line:
            return
        yield line


def parse_crate_stacks(lines: FileLines) -> tuple[FileLines, CrateStacks]:
    """
    parse the graphic at the top of the input file into a list of crate stacks.
    """
    header_lines = list(read_header_lines(lines))

    # we don't really need this last line, but might as well use it to
    # figure out how many columns to expect.
    n_columns = len(header_lines.pop().split())

    stacks: CrateStacks = [[] for _ in range(n_columns)]
    for line in header_lines:
        for i, crate in enumerate(line[1::4]):
            if crate != " ":
                # we're building the columns top-down, so we have to insert at the bottom
                stacks[i].insert(0, crate)

    return lines, stacks


def parse_instruction(line: str) -> Instruction:
    """parse a line like "move 4 from 9 to 3" into an Instruction type."""
    if match := move_pattern.match(line):
        return Instruction(
            from_column=int(match.group(2)) - 1,
            to_column=int(match.group(3)) - 1,
            quantity=int(match.group(1)),
        )
    raise ValueError(f"line doesn't match {move_pattern.pattern}: {line}")


def run_instructions(
    stacks: CrateStacks, instructions: list[Instruction], reverse_stacks: bool
):
    """
    apply a list of instructions to the given stacks.
    `reverse_stacks` indicates the order in which the crates should be moved.
    """
    for instruction in instructions:
        crates = [
            stacks[instruction.from_column].pop() for _ in range(instruction.quantity)
        ]
        if reverse_stacks:
            stacks[instruction.to_column].extend(reversed(crates))
        else:
            stacks[instruction.to_column].extend(crates)


def get_tops(stacks: CrateStacks) -> str:
    """get the top crate of each stack as a string"""
    return "".join(column[-1] for column in stacks)


def solve(*, reverse_stacks: bool = False) -> str:
    """
    load stacks & instructions from the input file, apply the instructions, and
    return the top crate of each stack as a string.

    `reverse_stacks` flips the order that crates are moved from one column to
    another. this is all that's required to solve part 2.
    """
    # part of the generator is consumed by parsing the stacks
    lines, stacks = parse_crate_stacks(input_lines())

    # the rest is consumed as crane instructions
    instructions = [parse_instruction(line) for line in lines]

    run_instructions(stacks, instructions, reverse_stacks)

    return get_tops(stacks)


print(f"part 1: {solve()}")
print(f"part 2: {solve(reverse_stacks=True)}")
