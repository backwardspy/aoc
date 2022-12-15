import itertools
from dataclasses import dataclass
from enum import Enum, auto
from typing import Generator


@dataclass(frozen=True)
class Vec2:
    x: int
    y: int


class Element(Enum):
    AIR = auto()
    SAND = auto()
    ROCK = auto()

    @property
    def is_solid(self) -> bool:
        return self in [self.SAND, self.ROCK]


SOURCE = Vec2(500, 0)

Path = list[Vec2]
Space = list[list[Element]]


def line_to_points(line: str) -> Generator[Vec2, None, None]:
    for coords in line.split(" -> "):
        x, y = coords.split(",")
        yield Vec2(int(x), int(y))


def sign(value: int) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def between(a: Vec2, b: Vec2) -> Generator[Vec2, None, None]:
    """
    yields every point between a & b inclusive.
    only works for horizontal & vertical lines!
    """
    assert a.x == b.x or a.y == b.y, "diagonal lines are unsupported"
    dx = sign(b.x - a.x)
    dy = sign(b.y - a.y)
    x = a.x
    y = a.y
    yield Vec2(x, y)
    while x != b.x or y != b.y:
        x += dx
        y += dy
        yield Vec2(x, y)


def yield_paths() -> Generator[Path, None, None]:
    with open("inputs/day14", encoding="utf-8") as inputs_file:
        lines = (line.strip() for line in inputs_file)
        yield from (list(line_to_points(line)) for line in lines)


def find_extents(paths: list[Path]) -> tuple[Vec2, Vec2]:
    points = [point for path in paths for point in path]
    points.append(SOURCE)

    min_x = min(point.x for point in points)
    min_y = min(point.y for point in points)
    max_x = max(point.x for point in points)
    max_y = max(point.y for point in points)

    return (Vec2(min_x, min_y), Vec2(max_x, max_y))


def print_space(space: Space, minv: Vec2, maxv: Vec2) -> None:
    for y in range(maxv.y - minv.y + 1):
        for x in range(maxv.x - minv.x + 1):
            if space[y][x] == Element.ROCK:
                print("##", end="")
            elif space[y][x] == Element.SAND:
                print("<>", end="")
            elif space[y][x] == Element.AIR:
                print("  ", end="")
            elif x == SOURCE.x - minv.x and y == SOURCE.y - minv.y:
                print("\\/", end="")
            else:
                raise ValueError(f"unknown value in {space[y][x]=}")
        print()
    print()


def draw_rocks(space: Space, paths: list[Path], origin: Vec2) -> None:
    for path in paths:
        for a, b in zip(path, path[1:]):
            for point in between(a, b):
                space[point.y - origin.y][point.x - origin.x] = Element.ROCK


def drop_sand(space: Space, minv: Vec2, maxv: Vec2) -> bool:
    """
    drop a piece of sand from the source until it comes to rest or falls into the void.
    returns true if the sand fell into the void or came to rest on top of the source.
    """

    sx = SOURCE.x
    sy = SOURCE.y

    def get(x: int, y: int) -> bool:
        if x < minv.x or y < minv.y or x > maxv.x or y > maxv.y:
            return False
        return space[y - minv.y][x - minv.x].is_solid

    def set(x: int, y: int) -> None:
        if x < minv.x or y < minv.y or x > maxv.x or y > maxv.y:
            raise ValueError(f"set out of bounds: ({x}, {y})")
        space[y - minv.y][x - minv.x] = Element.SAND

    while sx >= minv.x and sy >= minv.y and sx <= maxv.x and sy <= maxv.y:
        if get(sx, sy + 1) is False:
            sy += 1
        elif get(sx - 1, sy + 1) is False:
            sy += 1
            sx -= 1
        elif get(sx + 1, sy + 1) is False:
            sy += 1
            sx += 1
        else:
            # we're at rest, add the sand and return.
            set(sx, sy)
            return sx == SOURCE.x and sy == SOURCE.y

    # we completed the loop, which means we're in the void
    return True


def simulate(space: Space, minv: Vec2, maxv: Vec2) -> int:
    """
    drops sand until one falls into the void.
    returns the number of settled sand particles.
    """
    step = 0
    while True:
        stop = drop_sand(space, minv, maxv)
        step += 1
        if stop:
            return step


def new_space(minv: Vec2, maxv: Vec2):
    return [
        [Element.AIR for x in range(minv.x, maxv.x + 1)]
        for y in range(minv.y, maxv.y + 1)
    ]


def part1() -> None:
    paths = list(yield_paths())
    minv, maxv = find_extents(paths)
    space = new_space(minv, maxv)
    draw_rocks(space, paths, minv)

    # the void sand is counted as one step of the sim, so we roll that one back
    # to get the answer.
    part_1 = simulate(space, minv, maxv) - 1

    # uncomment if you want a fun visualisation :)
    # this needs a large space to print correctly!
    # print_space(space, minv, maxv)

    print(f"part 1: {part_1}")


def part2() -> None:
    paths = list(yield_paths())
    minv, maxv = find_extents(paths)

    # sand stacks at 45 degrees, so at most we will need a floor twice as wide as the space is high.
    # add 2 since the floor is meant to be 2 below the lowest point in the paths
    height = maxv.y - minv.y + 2
    paths.append(
        [Vec2(SOURCE.x - height, maxv.y + 2), Vec2(SOURCE.x + height, maxv.y + 2)]
    )

    # recalculate bounds with floor in place
    minv, maxv = find_extents(paths)

    space = new_space(minv, maxv)
    draw_rocks(space, paths, minv)

    part_2 = simulate(space, minv, maxv)

    # uncomment if you want a fun visualisation :)
    # this needs a HUGE space to print correctly!
    # set your font size to around 3-4px for any chance of seeing this properly.
    # print_space(space, minv, maxv)

    print(f"part 2: {part_2}")


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
