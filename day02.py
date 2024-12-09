from util.args import parse_args


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

    reports_normal = [do_failsafe_report_check(r) for r in reports]

    print(sum(reports_normal))
