from functools import cmp_to_key
from typing import Generator

PacketList = list[tuple[list[int], list[int]]]


def read_inputs() -> PacketList:
    with open("inputs/day13", encoding="utf-8") as inputs_file:
        pairs = inputs_file.read().strip().split("\n\n")

    def iter_pairs() -> Generator[tuple[str, str], None, None]:
        yield from (tuple(pair.split()) for pair in pairs)

    return [(eval(left), eval(right)) for left, right in iter_pairs()]


class OutOfOrder(Exception):
    ...


def compare_order(left: list[int] | int, right: list[int] | int) -> bool:
    """
    returns true if the packet data is in order.
    returns false if further comparisons are needed.
    raises OutOfOrder if the packet is out of order.
    """

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            raise OutOfOrder
        return False

    if isinstance(left, list) and isinstance(right, list):
        if any(compare_order(l, r) for l, r in zip(left, right)):
            return True

        if len(left) < len(right):
            return True

        if len(left) == len(right):
            # same length > keep checking
            return False

        raise OutOfOrder

    if isinstance(left, int):
        return compare_order([left], right)

    if isinstance(right, int):
        return compare_order(left, [right])

    raise ValueError(f"missing case: {left=!r} {right=!r}")


def all_in_order(left: list[int], right: list[int]) -> bool:
    """return true if left < right as per the puzzle rules, otherwise false."""
    try:
        compare_order(left, right)
    except OutOfOrder:
        return False
    else:
        return True


def reorder(packets: PacketList) -> list[list[int]]:
    all_packets = [packet for pair in packets for packet in pair]
    all_packets.extend([[[2]], [[6]]])
    key = cmp_to_key(lambda l, r: 1 if all_in_order(l, r) else -1)
    return sorted(all_packets, key=key, reverse=True)


def main():
    packets = read_inputs()

    part_1 = sum(
        i
        for i, (left, right) in enumerate(packets, start=1)
        if all_in_order(left, right)
    )
    print(f"part 1: {part_1}")

    sorted_packets = reorder(packets)
    div_1 = sorted_packets.index([[2]]) + 1
    div_2 = sorted_packets.index([[6]]) + 1
    print(f"part 2: {div_1 * div_2}")


if __name__ == "__main__":
    main()
