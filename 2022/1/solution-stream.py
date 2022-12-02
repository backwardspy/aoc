# this solution is optimised for memory usage rather than code size.
# we avoid reading the entire file in one chunk, and we only hold on to the
# bare minimum of what we need to calculate the answers.
from pathlib import Path
import re

split = re.compile("\n\n")
inputs = Path("input")

with inputs.open("r") as inputs_file:
    largest = [0, 0, 0]
    accumulator = 0
    for line in inputs_file:
        line = line.strip()
        if line:
            accumulator += int(line)
        else:
            if accumulator > min(largest):
                replace = largest.index(min(largest))
                largest[replace] = accumulator
            accumulator = 0

print(f"solution 1: {max(largest)}")
print(f"solution 2: {sum(largest)}")

