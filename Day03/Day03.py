# %%
from pathlib import Path
import re

import numpy as np

INPUT_FILE = Path(__file__).parent / "puzzle.input"
INPUT_TEXT = open(INPUT_FILE).read()


# %%
# Part 1
regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


def part1(input_text) -> int:
    matches = regex.findall(input_text)
    matches = [(int(a), int(b)) for a, b in matches]
    return np.sum([a * b for a, b in matches])


# %%
# test
test = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
print(part1(test))


# %%
print(part1(INPUT_TEXT))

# %%
# Part 2
regex = re.compile(r"((?:mul\((\d{1,3}),(\d{1,3})\))|(?:do\(\))|(?:don't\(\)))")
test = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
matches = regex.findall(test)


def part2(input_text):
    matches = regex.findall(input_text)
    accumulator = 0
    active_multiplication = True
    for matched in matches:
        instruction = matched[0][:3]
        if active_multiplication and (instruction == "mul"):
            a, b = int(matched[1]), int(matched[2])
            accumulator += a * b
        elif instruction == "do(":
            active_multiplication = True
        elif instruction == "don":
            active_multiplication = False
    return accumulator


# %%
print(part2(test))


# %%
print(part2(INPUT_TEXT))

# %%
