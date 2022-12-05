"""
the simplest solution i could think of; LUTs.
you *can* compute the outcome of a RPS game with modulo, but given that there's
only nine possible cases... this seems fine.
"""
# A = rock, B = paper, C = scissors
# X = rock, Y = paper, Z = scissors
scores_part_1 = {
    "A X": 1 + 3,
    "A Y": 2 + 6,
    "A Z": 3,
    "B X": 1,
    "B Y": 2 + 3,
    "B Z": 3 + 6,
    "C X": 1 + 6,
    "C Y": 2,
    "C Z": 3 + 3,
}

# A = rock, B = paper, C = scissors
# X = lose, Y = draw, Z = win
scores_part_2 = {
    "A X": 0 + 3,
    "A Y": 3 + 1,
    "A Z": 6 + 2,
    "B X": 0 + 1,
    "B Y": 3 + 2,
    "B Z": 6 + 3,
    "C X": 0 + 2,
    "C Y": 3 + 3,
    "C Z": 6 + 1,
}

def score(scores: dict[str, int]):
    with open("inputs/day2", "r") as inputs:
        return sum(scores[line.strip()] for line in inputs)

print(f"part 1: {score(scores_part_1)}")
print(f"part 2: {score(scores_part_2)}")
