"""day 12: hill climbing algorithm"""
from dataclasses import dataclass
from typing import Generator, cast

Coord = tuple[int, int]


@dataclass
class Graph:
    """
    models the input data with all the information & functions we need to solve
    the puzzle.
    """

    edges: dict[Coord, list[Coord]]
    width: int
    height: int
    start: Coord
    end: Coord
    all_starts: list[Coord]

    def is_in_bounds(self, pos: Coord) -> bool:
        """return true if `pos` is in-bounds, otherwise false."""
        return (
            pos[0] >= 0 and pos[1] >= 0 and pos[0] < self.height and pos[1] < self.width
        )

    def prune(self, coords: list[Coord]) -> list[Coord]:
        """return the input list with all out-of-bounds coordinates removed."""
        return [pos for pos in coords if self.is_in_bounds(pos)]

    def all_neighbours(self, pos: Coord) -> list[Coord]:
        """return reachable neighbours of `pos`."""
        return self.edges[pos]


def all_neighbours(pos: Coord) -> list[Coord]:
    """yield neighbours in every direction from `pos`."""
    return [
        (pos[0] + 1, pos[1]),
        (pos[0] - 1, pos[1]),
        (pos[0], pos[1] + 1),
        (pos[0], pos[1] - 1),
    ]


def read_graph() -> Graph:
    """
    read the input and parse it into a dictionary mapping coordinates to
    attainable adjacent coordinates.
    """
    with open("inputs/day12", encoding="utf-8") as inputs_file:
        lines = [line.strip() for line in inputs_file]

    def char_at(pos: Coord) -> str:
        return lines[pos[0]][pos[1]]

    def height_at(pos: Coord) -> int:
        char = char_at(pos)
        if char == "E":
            char = "z"
        return ord(char) - ord("a")

    def reachable(level: str, coords: list[Coord]) -> list[Coord]:
        height = ord(level) - ord("a")
        return [pos for pos in coords if height_at(pos) - height < 2]

    graph = Graph(
        edges={},
        width=len(lines[0]),
        height=len(lines),
        start=(0, 0),
        end=(0, 0),
        all_starts=[],
    )
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            coord = (row, col)

            match char:
                case "S":  # starting position
                    # everywhere is accessible from the start
                    graph.start = coord
                    graph.edges[coord] = graph.prune(all_neighbours(coord))
                case "E":  # target
                    # we never need to leave the target, so we don't need to add any edges.
                    graph.end = coord
                case char if "a" <= char <= "z":
                    # we can travel to neighbouring cells within one character of ours
                    graph.edges[coord] = reachable(
                        char, graph.prune(all_neighbours(coord))
                    )
                case _:
                    raise ValueError(f"unexpected character in input: {char}")

            if char == "a":
                graph.all_starts.append(coord)

    return graph


def bfs(graph: Graph, start: Coord) -> list[Coord] | None:
    """returns the shortest route from `start` to `graph.end`."""
    routes = [[start]]
    visited = set()

    while routes:
        route = routes.pop(0)

        pos = route[-1]
        if pos == graph.end:
            return route

        if pos in visited:
            continue

        for neighbour in graph.all_neighbours(pos):
            routes.append([*route, neighbour])

        visited.add(pos)

    return None


def all_routes(graph: Graph) -> Generator[list[Coord], None, None]:
    """yield all valid routes on the graph from all possible starting points."""
    for start in graph.all_starts:
        if route := bfs(graph, start):
            yield route


def solve(all_starts: bool) -> int:
    """
    solve the puzzle and return the answer.
    `all_starts` controls whether to use the indicated start or all possible
    starts, aka part 1 and part 2 of the puzzle.
    """
    graph = read_graph()
    if all_starts:
        return min(len(route) for route in all_routes(graph)) - 1
    return len(cast(Coord, bfs(graph, graph.start))) - 1


part_1 = solve(False)
print(f"part 1: {part_1}")
part_2 = solve(True)
print(f"part 2: {part_2}")
