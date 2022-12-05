"""
as with the previous days, both parts of this puzzle can be solved essentially
the same way, with the only variation being how the input is treated.
"""
from functools import reduce
from itertools import chain
from operator import and_
from typing import Generator, Iterable, Iterator


def char_range(start: str, stop: str) -> Generator[str, None, None]:
    """
    returns a range of characters from a to b.
    """
    assert ord(start) < ord(stop), "start must come before stop"
    yield from (chr(i) for i in range(ord(start), ord(stop) + 1))


priorities = {
    c: i + 1 for i, c in enumerate(chain(char_range("a", "z"), char_range("A", "Z")))
}


def midsplit(line: str) -> tuple[str, str]:
    """splits the given line in half and returns both ends."""
    mid = len(line) // 2
    return line[:mid], line[mid:]


def chunks(iterable: Iterable, size: int) -> Iterator:
    """returns an iterator over even sized chunks of the input iterator."""
    iterator = [iter(iterable)] * size
    return zip(*iterator)


def find_duplicate(*groups: str) -> str:
    """
    finds & returns the single duplicate character from the given strings.
    raises an assertion error if there is more than one duplicate.
    """
    duplicates = reduce(and_, (set(items) for items in groups))
    duplicate = duplicates.pop()
    assert len(duplicates) == 0, "more than one duplicate found"
    return duplicate


def iter_input() -> Iterator[str]:
    """yields lines from the input file."""
    with open("inputs/day3", encoding="utf-8") as input_file:
        yield from (line.strip() for line in input_file)


def sum_priorities(*duplicates: str) -> int:
    """returns the sum of the priorities of the given duplicates."""
    return sum(priorities[duplicate] for duplicate in duplicates)


print("part 1: ", end="")
dupes = (find_duplicate(*midsplit(line)) for line in iter_input())
print(sum_priorities(*dupes))

print("part 2: ", end="")
dupes = (find_duplicate(a, b, c) for a, b, c in chunks(iter_input(), 3))
print(sum_priorities(*dupes))
