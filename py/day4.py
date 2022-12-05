from collections import namedtuple

InclusiveRange = namedtuple("InclusiveRange", "start stop")


def input_lines():
    with open("inputs/day4") as f:
        lines = (line.strip() for line in f)
        yield from lines


def str_to_range(string):
    start, stop = string.split("-")
    return InclusiveRange(int(start), int(stop))


def str_to_ranges(string):
    first, second = string.split(",")
    return str_to_range(first), str_to_range(second)


def range_is_subset(a, b):
    return a.start >= b.start and a.stop <= b.stop


def ranges_are_subsets(a, b):
    return range_is_subset(a, b) or range_is_subset(b, a)


def ranges_overlap(a, b):
    return a.stop >= b.start and a.start <= b.stop


def line_has_overlaps(line, predicate):
    left, right = str_to_ranges(line)
    return predicate(left, right)


part_1 = sum(1 for line in input_lines() if line_has_overlaps(line, ranges_are_subsets))
print(f"part 1: {part_1}")

part_2 = sum(1 for line in input_lines() if line_has_overlaps(line, ranges_overlap))
print(f"part 2: {part_2}")
