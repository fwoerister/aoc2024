import functools
from heapq import heappush, heappop
from time import time

from util.args import parse_args
from util.submit import submit_answer

positions = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}

shortest_path = {
    "AA": ["A"],
    "^^": ["A"],
    ">>": ["A"],
    "vv": ["A"],
    "<<": ["A"],
    "A^": ["<A"],
    "A>": ["vA"],
    "Av": ["v<A", "<vA"],
    "A<": ["v<<A", "<v<A"],
    "^A": [">A"],
    "^>": [">vA", "v>A"],
    "^v": ["vA"],
    "^<": ["v<A"],
    ">A": ["^A"],
    ">^": ["<^A", "^<A"],
    ">v": ["<A"],
    "><": ["<<A"],
    "vA": [">^A", "^>A"],
    "v^": ["^A"],
    "v>": [">A"],
    "v<": ["<A"],
    "<A": [">>^A"],
    "<^": [">^A"],
    "<>": [">>A"],
    "<v": [">A"],
}


def get_instructions_for_next_level(instructions):
    pos = "A"
    sub_instructions = []

    for direction in instructions:
        sub_instructions.append(shortest_path[pos + direction])
        pos = direction

    return sub_instructions


def dir_to_sym(direction):
    match direction:
        case (0, 1):
            return "v"
        case (0, -1):
            return "^"
        case (1, 0):
            return ">"
        case (-1, 0):
            return "<"
    raise ValueError()


def find_shortest_path(start_digit, end_digit, level):
    start = positions[start_digit]
    end = positions[end_digit]
    open_nodes = []
    heappush(open_nodes, (0, start, ""))

    while open_nodes:
        score, current, directions = heappop(open_nodes)

        if directions.endswith('A'):
            return score
        if current == end:
            new_score = get_instruction_length(directions + "A", level)
            heappush(open_nodes, (new_score, current, directions + "A"))
            continue

        h_dir = end[0] - current[0]
        if h_dir != 0:
            h_dir = h_dir // abs(end[0] - current[0])
        v_dir = (end[1] - current[1])
        if v_dir != 0:
            v_dir = v_dir // abs(end[1] - current[1])

        neighbours = [(current[0] + h_dir, current[1]), (current[0], current[1] + v_dir)]
        neighbours = [n for n in neighbours if 0 <= n[0] <= 2 and 0 <= n[1] <= 3 and n not in [current, (0, 3)]]

        for n in neighbours:
            next_direction = (n[0] - current[0], n[1] - current[1])
            if next_direction != (0, 0):
                new_score = get_instruction_length(directions + dir_to_sym(next_direction), level)
            heappush(open_nodes, (new_score, n, directions + dir_to_sym(next_direction)))


@functools.cache
def get_instruction_length(instructions, level):
    if level == 0:
        return len(instructions)

    length = 0

    for sub_instructions in get_instructions_for_next_level(instructions):
        scores = []
        for inst in sub_instructions:
            scores.append(get_instruction_length(inst, level - 1))

        length += min(scores)

    return length


if '__main__' == __name__:
    args = parse_args()

    with args.puzzle_input as file:
        codes = [code.strip() for code in file.readlines() if code]

    start = round(time() * 1000)

    answer_1 = 0

    for code in codes:
        prev = "A"
        complexity = 0
        for digit in code:
            complexity += find_shortest_path(prev, digit, 2)
            prev = digit
        answer_1 += complexity * int(code.replace('A', ''))

    end_1 = round(time() * 1000)

    answer_2 = 0
    for code in codes:
        prev = "A"
        complexity = 0
        for digit in code:
            complexity += find_shortest_path(prev, digit, 25)
            prev = digit
        answer_2 += complexity * int(code.replace('A', ''))

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 21, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 21, 2))
