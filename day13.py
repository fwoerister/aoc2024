import re
from time import time

import sympy

from util.args import parse_args
from util.submit import submit_answer


def get_machine_configs(file):
    line = file.readline()
    configs = []
    while line:
        button_a_x, button_a_y = [int(val) for val in re.findall(r'\+(\d*)', line)]
        line = file.readline()
        button_b_x, button_b_y = [int(val) for val in re.findall(r'\+(\d*)', line)]
        line = file.readline()
        price_x, price_y = [int(val) for val in re.findall(r'=(\d*)', line)]
        line = file.readline()

        configs.append({
            'ax': button_a_x,
            'ay': button_a_y,
            'bx': button_b_x,
            'by': button_b_y,
            'px': price_x,
            'py': price_y,
        })

        while line and line == '\n':
            line = file.readline()

    return configs


def get_minimal_tokens(c):
    a, b = sympy.symbols('a, b', real=True, positive=True, integer=True)
    eq = [
        sympy.Eq((a * c['ax'] + b * c['bx']), c['px']),
        sympy.Eq((a * c['ay'] + b * c['by']), c['py']),
    ]

    s = sympy.solve(eq)
    return s[a] * 3 + s[b] if s else 0


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:

        configs = get_machine_configs(file)
        answer_1 = 0

        start = round(time() * 1000)

        for config in configs:
            answer_1 += get_minimal_tokens(config)

        end_1 = round(time() * 1000)

        answer_2 = 0

        for config in configs:
            config['px'] += 10000000000000
            config['py'] += 10000000000000
            answer_2 += get_minimal_tokens(config)

        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 11, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 11, 2))
