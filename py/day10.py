"""day 10: cathode-ray tube"""
from dataclasses import dataclass
from typing import Callable, Generator

InputLines = Generator[str, None, None]


def input_lines() -> InputLines:
    """yield lines from the inputs file."""
    with open("inputs/day10", encoding="utf-8") as inputs_file:
        lines = (line.strip() for line in inputs_file)
        yield from lines


class Machine:
    """virtual machine to emulate the elven device."""

    def __init__(
        self,
        hsync_probe: Callable[["Machine"], None],
        step_probe: Callable[["Machine"], None],
    ):
        self.x_reg = 1
        self.cycles = 0
        self.hysnc_probe = hsync_probe
        self.step_probe = step_probe

        self.crt_col = 0
        self.crt_row = 0
        self.crt_lit = False

    def noop(self) -> None:
        """do nothing. takes one cycle to complete."""
        self.step()

    def addx(self, arg: int) -> None:
        """add ARG to X. takes 2 cycles to complete."""
        for _ in range(2):
            self.step()

        self.x_reg += arg

    def step(self) -> None:
        """performs a single step of the emulation."""
        # fire the crt and call the step probe
        self.crt_lit = self.x_reg - 1 <= self.crt_col <= self.x_reg + 1
        self.step_probe(self)

        # update crt beam position
        self.crt_col += 1
        if self.crt_col == 40:
            self.crt_col = 0
            self.crt_row += 1

        # step the cpu
        self.cycles += 1
        if (self.cycles - 20) % 40 == 0:
            self.hysnc_probe(self)

    def dispatch(self, instr: str) -> None:
        """
        execute an instruction.
        supported instructions:
         * noop
         * addx INT
        """
        match instr.split():
            case ["noop"]:
                self.noop()
            case ["addx", arg]:
                self.addx(int(arg))


@dataclass
class EmulationResult:
    """
    result of running an emulation.

    signal strength is defined as X * cycles summed every 40 cycles starting at
    cycle 20.

    render_lines is a 2d list of characters displayed on the 40x6 crt.
    """

    signal_strength: int
    render_lines: list[list[str]]


def run() -> EmulationResult:
    """run the emulation and return the results."""
    result = EmulationResult(signal_strength=0, render_lines=[[] for _ in range(6)])

    def hsync_probe(machine: Machine):
        result.signal_strength += machine.x_reg * machine.cycles

    def step_probe(machine: Machine):
        sym = "█" if machine.crt_lit else " "
        result.render_lines[machine.crt_row].append(sym)

    machine = Machine(hsync_probe, step_probe)
    for line in input_lines():
        machine.dispatch(line)

    return result


def solve() -> None:
    """
    run the emulation and print the results for parts 1 and 2 of the puzzle.
    """
    result = run()
    print(f"part 1: {result.signal_strength}")
    print("part 2:")
    print("\n".join(["".join(line) for line in result.render_lines]))


if __name__ == "__main__":
    solve()
