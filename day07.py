from time import time
from util.args import parse_args
from util.submit import submit_answer


def find_ops(result, values, operations):
    if len(values) == 1:
        return values[0] == result

    if sum(values) > result:
        return False

    if int(''.join([str(val) for val in values])) < result:
        return False

    for op in operations:
        new_values = [op(values[0], values[1])] + values[2:]
        if find_ops(result, new_values, operations):
            return True
    return False


if __name__ == '__main__':
    args = parse_args()
    answer_1 = 0
    answer_2 = 0

    with args.puzzle_input as file:
        equations = file.readlines()

        start = round(time() * 1000)
        for line in equations:
            result, values = line.split(': ')
            result = int(result)
            values = [int(v) for v in values.split(' ')]

            if find_ops(result, values, [lambda x, y: x + y, lambda x, y: x * y]):
                answer_1 += result

        end_1 = round(time() * 1000)
        for line in equations:
            result, values = line.split(': ')
            result = int(result)
            values = [int(v) for v in values.split(' ')]

            if find_ops(result, values, [lambda x, y: x + y, lambda x, y: x * y, lambda x, y: int(str(x) + str(y))]):
                answer_2 += result
        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 7, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 7, 2))
