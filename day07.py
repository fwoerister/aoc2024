from util.args import parse_args
from util.submit import submit_answer


def find_ops(result, values):
    if len(values) == 1:
        return values[0] == result

    values_plus = [values[0] + values[1]] + values[2:]
    values_mult = [values[0] * values[1]] + values[2:]
    values_cat = [int(str(values[0]) + str(values[1]))] + values[2:]

    return find_ops(result, values_plus) or find_ops(result, values_mult) or find_ops(result, values_cat)


if __name__ == '__main__':
    args = parse_args()
    answer_1 = 0
    answer_2 = 0

    with args.puzzle_input as file:
        for line in file.readlines():
            result, values = line.split(': ')
            result = int(result)
            values = [int(v) for v in values.split(' ')]

            if find_ops(result, values):
                answer_1 += result

    print(answer_1)
    print(answer_2)

    if args.submit == 1:
        print(submit_answer(answer_1, 5, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 5, 2))
