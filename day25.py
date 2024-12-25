from time import time

from util.args import parse_args
from util.submit import submit_answer


def is_lock(schema):
    return schema[0].count('#') == len(schema[0])


def parse_lock(schema):
    values = []

    for x in range(len(schema[0])):
        for y in range(len(schema)):
            if schema[y][x] == '.':
                values.append(y - 1)
                break

    return values


def parse_key(schema):
    values = []

    for x in range(len(schema[0])):
        for y in range(len(schema)):
            if schema[y][x] == '#':
                values.append(len(schema) - y - 1)
                break

    return values


def is_overlapping(key, lock, height):
    for x in range(len(key)):
        if key[x] + lock[x] > height:
            return True

    return False


def parse_input(file):
    keys = []
    locks = []
    height = 0
    with file as f:
        while line := f.readline():
            schema = [line.strip()]
            while (line := f.readline()) and line != '\n':
                schema.append(line.strip())
            height = len(schema) - 2
            if is_lock(schema):
                locks.append(parse_lock(schema))
            else:
                keys.append(parse_key(schema))
    return keys, locks, height


if '__main__' == __name__:
    args = parse_args()

    keys, locks, height = parse_input(args.puzzle_input)

    start = round(time() * 1000)

    answer_1 = 0
    for lock in locks:
        for key in keys:
            if not is_overlapping(key, lock, height):
                answer_1 += 1
    end_1 = round(time() * 1000)

    answer_2 = 0

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 25, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 25, 2))
