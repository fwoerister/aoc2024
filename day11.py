import functools
from time import time

from util.args import parse_args
from util.submit import submit_answer


@functools.cache
def get_evolution_steps(stone, steps):
    if steps == 0:
        return 1

    if stone == 0:
        return get_evolution_steps(1, steps - 1)
    elif len(str(stone)) % 2 == 0:
        stone_left = int(str(stone)[:len(str(stone)) // 2])
        stone_right = int(str(stone)[len(str(stone)) // 2:])

        return get_evolution_steps(stone_left, steps - 1) + get_evolution_steps(stone_right, steps - 1)

    return get_evolution_steps(stone * 2024, steps - 1)


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        stones = [int(val) for val in file.readline().split(' ')]

        start = round(time() * 1000)

        answer_1 = sum([get_evolution_steps(stone, 25) for stone in stones])

        end_1 = round(time() * 1000)

        answer_2 = sum([get_evolution_steps(stone, 75) for stone in stones])

        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 11, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 11, 2))
