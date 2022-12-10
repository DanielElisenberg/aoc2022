
from functools import reduce
from itertools import accumulate


with open('day10/input', encoding='utf-8') as f:
    instructions = [line.strip().split(' ') for line in f]
instructions = ([[1]] + [
    [0] if instruction == ['noop'] else [0, int(instruction[1])]
    for instruction in instructions
])
cycles = list(accumulate(
    list(reduce(lambda l1, l2: l1+l2, instructions)),
    lambda x1, x2: x1+x2
))

signal_strength_sum = sum([
    x*(index+1) for index, x in enumerate(cycles)
    if index+1 in [20, 60, 100, 140, 180, 220]
])
print(f'Part 1: {signal_strength_sum}')

pixels = [
    '#' if index % 40 in range(x-1, x+2) else '.'
    for index, x in enumerate(cycles)
]
display = '\n'.join(
    [''.join([pixels[(y*40)+x] for x in range(39)]) for y in range(6)]
)
print(f'Part 2:\n{display}')
