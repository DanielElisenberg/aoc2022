def manhattan_distance(
    point_a: tuple[int, int], point_b: tuple[int, int]
) -> int:
    return abs(point_a[0]-point_b[0]) + abs(point_a[1]-point_b[1])


def find_shortest_path(
    start: tuple[int, int],
    goal: tuple[int, int],
    walk_map: dict[tuple[int, int]: list[tuple[int, int]]]
) -> int:
    found = {start: manhattan_distance(start, goal)}
    explored = {}
    step_weight = 2
    while True:
        if not found:
            return None
        current = min(found, key=found.get)
        current_score = found[current]
        current_manhattan_distance = manhattan_distance(current, goal)
        current_step_score = current_score - current_manhattan_distance
        del found[current]
        explored[current] = current_score
        if goal in walk_map[current]:
            break
        for walkable in walk_map[current]:
            if walkable in explored:
                continue
            walkable_manhattan_distance = manhattan_distance(walkable, goal)
            walkable_score = (
                walkable_manhattan_distance + current_step_score + step_weight
            )
            if walkable in found and found[walkable] <= walkable_score:
                continue
            found[walkable] = walkable_score

    path = [goal]
    while True:
        if path[-1] == start:
            break
        walkables = [
            square for square in walk_map if path[-1] in walk_map[square]
        ]
        walkable_dict = {
            square: explored.get(square, None) for square in walkables
            if explored.get(square, None) is not None
        }
        path += [min(walkable_dict, key=walkable_dict.get)]
    return path


def find_walkable(x: int, y: int, height_map: list[list[str]]) -> list[str]:
    return [
        (to_y, to_x) for to_y, to_x in [
            (y, x-1), (y, x+1), (y-1, x), (y+1, x)
        ]
        if 0 <= to_y < len(height_map)
        and 0 <= to_x < len(height_map[to_y])
        and ord(height_map[to_y][to_x]) <= ord(height_map[y][x]) + 1
    ]


def generate_walk_map(
    height_map: list[list[int]]
) -> dict[tuple[int, int]: list]:
    all_squares = sum(
        (
            [(y, x) for x, _ in enumerate(row)]
            for y, row in enumerate(height_map)
        ), []
    )
    return {
        (y, x): find_walkable(x, y, height_map)
        for y, x in all_squares
    }


def find_start_and_goal(
    height_map: list[list[str]]
) -> tuple[tuple[int, int], tuple[int, int]]:
    start = sum([
        [(y, x) for x, _ in enumerate(row) if height_map[y][x] == 'S']
        for y, row in enumerate(height_map)
    ], [])[0]
    goal = sum([
        [(y, x) for x, _ in enumerate(row) if height_map[y][x] == 'E']
        for y, row in enumerate(height_map)
    ], [])[0]
    return start, goal


with open('day12/input', encoding='utf-8') as f:
    height_map = [[character for character in line.strip()] for line in f]
start, goal = find_start_and_goal(height_map)
height_map[start[0]][start[1]] = 'a'
height_map[goal[0]][goal[1]] = 'z'
walk_map = generate_walk_map(height_map)

shortest_path = find_shortest_path(start, goal, walk_map)
print(f'Part 1: {len(shortest_path) - 1}')

a_paths = [
    find_shortest_path(a_square, goal, walk_map)
    for a_square in [(y, x) for y, x in walk_map if height_map[y][x] == 'a']
]
shortest_a_path = min([
    len(path)-1 for path in
    [path for path in a_paths if path is not None]
])
print(f'Part 2: {shortest_a_path}')
