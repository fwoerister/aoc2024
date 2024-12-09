from util.args import parse_args
from util.submit import submit_answer

if __name__ == '__main__':
    left_list = []
    right_list = []

    args = parse_args()
    answer_1 = 0
    answer_2 = 0

    with args.puzzle_input as file:
        for line in file.readlines():
            left_val, right_val = line.split('   ')
            left_list.append(int(left_val))
            right_list.append(int(right_val))

    left_list.sort()
    right_list.sort()

    answer_1 = len(list(map(lambda id_tuple: abs(id_tuple[0] - id_tuple[1]), zip(left_list, right_list))))

    for val in left_list:
        answer_2 += val * right_list.count(val)

    print(f"level 1: {answer_1}")
    print(f"level 2: {answer_2}")

    if args.submit == 1:
        print(submit_answer(answer_1, 1, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 1, 2))
