"""
this is the most obvious solution, which is to say splitting the file on \n\n,
summing each block of numbers, and then picking the top 1/top 3.

it is not very efficient, and large files could cause excessive memory usage.
"""

with open("inputs/day1", "r") as f:
    blocks = f.read().split("\n\n")

counts = [[int(number.strip()) for number in block.split("\n")] for block in blocks]
sums = sorted((sum(count) for count in counts), reverse=True)

print(f"solution 1: {sums[0]}")
print(f"solution 2: {sum(sums[:3])}")
