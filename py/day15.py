import re
from dataclasses import dataclass
from operator import itemgetter
from typing import Generator, Sequence

from prettyprinter import cpprint

line_re = re.compile(
    r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$"
)


Coord = tuple[int, int]


@dataclass(frozen=True)
class Sensor:
    position: Coord
    beacon: Coord
    radius: int


def manhattan_distance(a: Coord, b: Coord) -> int:
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def range_connects(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[1] + 1 and a[1] >= b[0] - 1


def parse_line(line: str) -> Sensor:
    """
    parse a line of input into sensor & beacon coordinates.
    """
    match = line_re.match(line)
    if not match:
        raise ValueError(f"{line!r} does not match {line_re!r}")

    sensor = (int(match.group(1)), int(match.group(2)))
    beacon = (int(match.group(3)), int(match.group(4)))
    return Sensor(
        position=sensor,
        beacon=beacon,
        radius=manhattan_distance(sensor, beacon),
    )


def read_inputs(test: bool = False) -> Generator[Sensor, None, None]:
    filename = "inputs/day15-test" if test else "inputs/day15"
    with open(filename, encoding="utf-8") as inputs_file:
        lines = (line.strip() for line in inputs_file)
        yield from (parse_line(line) for line in lines)


def get_bounds(sensors: Sequence[Sensor]) -> tuple[Coord, Coord]:
    min_x = min(min(sensor.position[0], sensor.beacon[0]) for sensor in sensors)
    min_y = min(min(sensor.position[1], sensor.beacon[1]) for sensor in sensors)
    max_x = max(max(sensor.position[0], sensor.beacon[0]) for sensor in sensors)
    max_y = max(max(sensor.position[1], sensor.beacon[1]) for sensor in sensors)
    return (min_x, min_y), (max_x, max_y)


def simplify_segments(segments: list[tuple[int, int]]) -> list[tuple[int, int]]:
    segments = sorted(segments, key=itemgetter(0))
    while len(segments) >= 2:
        for i, (left, right) in enumerate(zip(segments, segments[1:])):
            if range_connects(left, right):
                new_segment = (min(left[0], right[0]), max(left[1], right[1]))
                segments = [*segments[:i], new_segment, *segments[i + 2 :]]
                break
        else:
            # if we didn't break, no further changes were made to the segments.
            break

    return segments


def get_segments(
    row: int, sensors: Sequence[Sensor], minv: Coord, maxv: Coord
) -> list[tuple[int, int]]:
    segments = []

    for sensor in sensors:
        y_dist = abs(sensor.position[1] - row)
        width_at_row = (sensor.radius - y_dist) * 2 + 1

        if width_at_row > 0:
            start = sensor.position[0] - width_at_row // 2
            end = sensor.position[0] + width_at_row // 2
            segments.append((start, end))

    segments = simplify_segments(segments)

    # clamp the segments to minv/maxv
    def clamp(segment: tuple[int, int]) -> tuple[int, int] | None:
        if segment[0] > maxv[0] or segment[1] < minv[0]:
            return None
        return (max(minv[0], segment[0]), min(maxv[0], segment[1]))

    segments = [clamped for segment in segments if (clamped := clamp(segment))]

    return segments


def count_row(row: int, sensors: Sequence[Sensor], minv: Coord, maxv: Coord) -> int:
    segments = get_segments(row, sensors, minv, maxv)
    return sum(abs(segment[1] - segment[0]) for segment in segments)


def count_covered_squares(sensors: Sequence[Sensor], *, row: int) -> int:
    minv, maxv = get_bounds(sensors)
    return count_row(row, sensors, minv, maxv)


def clamp(value: int, minv: int, maxv: int) -> int:
    if value < minv:
        return minv
    if value > maxv:
        return maxv
    return value


def find_uncovered_square(sensors: Sequence[Sensor], *, max_size: int) -> Coord:
    minv, maxv = get_bounds(sensors)
    minv = (clamp(minv[0], 0, max_size), clamp(minv[1], 0, max_size))
    maxv = (clamp(maxv[0], 0, max_size), clamp(maxv[1], 0, max_size))
    for row in range(max_size + 1):
        print(f"{row} / {max_size} ({int(100 * row / max_size)}%)", end="\r")
        segments = get_segments(row, sensors, minv, maxv)
        if len(segments) == 1:
            continue

        print()
        cpprint(segments)
        start, end = segments
        mid = (start[1] + end[0]) // 2
        return (mid, row)

    raise ValueError("no uncovered squares found")


def tuning_freq(coord: Coord, *, max_size: int) -> int:
    return coord[0] * max_size + coord[1]


def main():
    TEST = False
    P1_ROW = 10 if TEST else 2000000
    P2_NORMAL_MAX_SIZE = 4000000
    P2_MAX_SIZE = 20 if TEST else P2_NORMAL_MAX_SIZE

    sensors = list(read_inputs(TEST))

    part_1 = count_covered_squares(sensors, row=P1_ROW)
    print(f"part 1: {part_1}")

    part_2 = tuning_freq(
        find_uncovered_square(sensors, max_size=P2_MAX_SIZE),
        max_size=P2_NORMAL_MAX_SIZE,
    )
    print(f"part 2: {part_2}")


if __name__ == "__main__":
    main()
