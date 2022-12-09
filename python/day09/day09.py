
from functools import reduce
from itertools import accumulate


DIRECTIONS = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1),
    'D': (0, 1)
}


def follow_head(
    tail: tuple[int, int], head: tuple[int, int]
) -> tuple[int, int]:
    tail_x, tail_y = tail
    head_x, head_y = head
    if max(abs(tail_x-head_x), abs(tail_y-head_y)) < 2:
        return (tail_x, tail_y)
    return (
        tail_x if head_x-tail_x == 0
        else tail_x + ((head_x-tail_x)//abs(head_x-tail_x)),
        tail_y if head_y-tail_y == 0
        else tail_y + ((head_y-tail_y)//abs(head_y-tail_y))
    )


def calculate_tail_positions(
    head_positions: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    tail_positions = [(0, 0)]
    for next_head_position in head_positions:
        tail_positions.append(follow_head(
            tail_positions[-1], next_head_position
        ))
    return [position for position in tail_positions][1:]


with open('day09/input', encoding='utf-8') as f:
    lines = [line.strip().split(' ') for line in f]
    head_movements = reduce(
        lambda x, y: x + y,
        [[DIRECTIONS[line[0]]] * int(line[1]) for line in lines]
    )
    head_positions = list(accumulate(
        head_movements, lambda x, y: (x[0]+y[0], x[1]+y[1])
    ))

print(f'Part 1: {len(set(calculate_tail_positions(head_positions)))}')
for i in range(9):
    head_positions = calculate_tail_positions(head_positions)
print(f'Part 2: {len(set(head_positions))}')
