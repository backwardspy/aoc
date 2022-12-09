"""day 9: rope bridge"""
from typing import Generator

InputLines = Generator[str, None, None]
Coord = tuple[int, int]


letter_to_direction = {
    "R": (1, 0),
    "U": (0, 1),
    "L": (-1, 0),
    "D": (0, -1),
}


def input_lines() -> InputLines:
    """yields lines from the puzzle input file."""
    with open("inputs/day9", encoding="utf-8") as inputs_file:
        lines = (line.strip() for line in inputs_file)
        yield from lines


def sign(num: int) -> int:
    """
    returns the sign of the number.
    + -> 1
    0 -> 0
    - -> -1
    """
    if num == 0:
        return 0
    return num // abs(num)


class Rope:
    """a rope is a collection of nodes that move together."""

    def __init__(self, nodes: int) -> None:
        """create a new rope with the given number of nodes."""
        # [0] is head, [-1] is tail
        self.nodes = [(0, 0) for _ in range(nodes)]

    @property
    def head(self) -> Coord:
        """the head is the first node in the rope."""
        return self.nodes[0]

    @head.setter
    def head(self, value: Coord) -> None:
        """set a new head position."""
        self.nodes[0] = value

    @property
    def tail(self) -> Coord:
        """the tail is the last node in the rope."""
        return self.nodes[-1]

    def move(self, direction: Coord):
        """
        move the head of the rope in the given direction, then update the other
        nodes accordingly.
        """
        self.head = (self.head[0] + direction[0], self.head[1] + direction[1])

        # each node behind gets updated
        follow = self.head
        for i, node in enumerate(self.nodes[1:], start=1):
            delta_x = follow[0] - node[0]
            delta_y = follow[1] - node[1]

            if abs(delta_x) > 1 or abs(delta_y) > 1:
                self.nodes[i] = (node[0] + sign(delta_x), node[1] + sign(delta_y))

            follow = self.nodes[i]


def simulate(rope: Rope, moves: Generator[tuple[Coord, int], None, None]) -> set[Coord]:
    """
    moves the head of the rope with the given sequence of moves.
    returns a set of all coordinates visited by the tail.
    """
    tail_visited = {rope.tail}
    for direction, count in moves:
        for _ in range(count):
            rope.move(direction)
            tail_visited.add(rope.tail)
    return tail_visited


def line_to_move(line: str) -> tuple[Coord, int]:
    """
    "R 4" -> ((1, 0), 4)
    """
    letter, count = line.split()
    return letter_to_direction[letter], int(count)


def solve(nodes: int) -> int:
    """
    run the input moves on a rope with the given number of nodes.
    return the number of unique locations visited by the tail.
    """
    rope = Rope(nodes)
    moves = (line_to_move(line) for line in input_lines())
    tail_visited = simulate(rope, moves)
    return len(tail_visited)


print(f"part 1: {solve(2)}")
print(f"part 2: {solve(10)}")
