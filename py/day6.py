def find_marker(stream: str, length: int) -> int:
    for i in range(0, len(stream) - length):
        if len(set(stream[i : i + length])) == length:
            return i + length
    raise ValueError("no solution")


with open("inputs/day6") as inputs_file:
    stream = inputs_file.read()


print(f"part 1: {find_marker(stream, 4)}")
print(f"part 2: {find_marker(stream, 14)}")
