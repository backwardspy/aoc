import math

coord = tuple[int, int]
each_direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def input_grid() -> list[str]:
    with open("inputs/day8") as inputs_file:
        lines = inputs_file.read().split("\n")
        # sometimes there's a blank line at the end
        return [line for line in lines if line]


def is_in_bounds(tree: coord, *, grid: list[str]) -> bool:
    return 0 <= tree[0] < len(grid) and 0 <= tree[1] < len(grid[0])


def height(tree: coord, *, grid: list[str]) -> int:
    return int(grid[tree[0]][tree[1]])


def visible_in_direction(
    tree: coord, *, grid: list[str], direction: coord
) -> tuple[bool, int]:
    reference = height(tree, grid=grid)
    coord = tree
    dist = 0
    while True:
        coord = (coord[0] + direction[0], coord[1] + direction[1])

        if not is_in_bounds(coord, grid=grid):
            # we reached the edge
            return (True, dist)

        dist += 1

        if height(coord, grid=grid) >= reference:
            # we are blocked in this direction
            return (False, dist)


def visible(tree: coord, *, grid: list[str]) -> bool:
    return any(
        visible_in_direction(tree, grid=grid, direction=direction)[0]
        for direction in each_direction
    )


def score(tree: coord, *, grid: list[str]) -> int:
    return math.prod(
        visible_in_direction(tree, grid=grid, direction=direction)[1]
        for direction in each_direction
    )


grid = input_grid()

part_1 = sum(
    visible((y, x), grid=grid) for y in range(len(grid)) for x in range(len(grid[y]))
)
print(f"part 1: {part_1}")

part_2 = max(
    score((y, x), grid=grid) for y in range(len(grid)) for x in range(len(grid[y]))
)
print(f"part 2: {part_2}")
