import re
from time import time

from util.args import parse_args
from util.submit import submit_answer


def analyse_memory(memory, consider_conditionals=False):
    add_mul_to_result = True
    result = 0

    for group in re.findall(r"mul\((\d+,\d+)\)|(do\(\))|(don't\(\))", memory):
        if group[0] != "" and add_mul_to_result:
            left = int(group[0].split(',')[0])
            right = int(group[0].split(',')[1])
            result += left * right
        elif consider_conditionals and group[1] == "do()":
            add_mul_to_result = True
        elif consider_conditionals and group[2] == "don't()":
            add_mul_to_result = False

    return result


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        memory = ''.join(file.readlines())

        start = round(time() * 1000)
        answer_1 = analyse_memory(memory, consider_conditionals=False)
        end_1 = round(time() * 1000)
        answer_2 = analyse_memory(memory, consider_conditionals=True)
        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 3, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 3, 2))
