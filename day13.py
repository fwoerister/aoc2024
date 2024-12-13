import functools
import re
from time import time
import sympy

from util.args import parse_args
from util.submit import submit_answer


def get_machine_configs(file):
    line = file.readline()
    configs = []
    while line:
        a_x, a_y = [int(val) for val in re.findall(r'\+(\d*)', line)]
        line = file.readline()
        b_x, b_y = [int(val) for val in re.findall(r'\+(\d*)', line)]
        line = file.readline()
        price_x, price_y = [int(val) for val in re.findall(r'=(\d*)', line)]
        line = file.readline()

        configs.append((a_x, a_y, b_x, b_y, price_x, price_y))

        while line and line == '\n':
            line = file.readline()

    return configs


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:

        configs = get_machine_configs(file)
        answer_1 = 0

        start = round(time() * 1000)

        for config in configs:
            a, b = sympy.symbols('a, b', real=True, positive=True, integer=True)
            equations = [
                sympy.Eq((a * config[0] + b * config[2]), config[4]),
                sympy.Eq((a * config[1] + b * config[3]), config[5]),
            ]

            solution = sympy.solve(equations)
            if solution:
                answer_1 += solution[a] * 3 + solution[b]

        end_1 = round(time() * 1000)

        answer_2 = 0
        for config in configs:
            a, b = sympy.symbols('a, b', real=True, positive=True, integer=True)
            equations = [
                sympy.Eq((a * config[0] + b * config[2]), config[4] + 10000000000000),
                sympy.Eq((a * config[1] + b * config[3]), config[5] + 10000000000000),
            ]

            solution = sympy.solve(equations)
            if solution:
                answer_2 += solution[a] * 3 + solution[b]

        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 11, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 11, 2))
