from time import time

from util.args import parse_args
from util.submit import submit_answer


def do_failsafe_report_check(report):
    idx = 0

    if check_report(report):
        return True

    while idx < len(report):
        fixed_report = report[:idx] + report[idx + 1:]

        if check_report(fixed_report):
            return True
        idx += 1

    return False


def check_report(report):
    shifted_reports = report[1:] + [0]
    diffs = list(map(lambda elem: elem[1] - elem[0], zip(report, shifted_reports)))[:-1]
    decreasing_steps = sum([elem < 0 for elem in diffs])
    out_of_bound_vals = sum([0 < abs(elem) <= 3 for elem in diffs])
    return decreasing_steps in [0, len(diffs)] and out_of_bound_vals == len(diffs)


if __name__ == '__main__':
    reports = []

    args = parse_args()

    with args.puzzle_input as file:
        for line in file.readlines():
            reports.append([int(val) for val in line.split(' ')])

    start = round(time() * 1000)
    answer_1 = sum([check_report(r) for r in reports])
    end_1 = round(time() * 1000)
    answer_2 = sum([do_failsafe_report_check(r) for r in reports])
    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 2, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 2, 2))
