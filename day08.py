from time import time

from util.args import parse_args
from util.submit import submit_answer

if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        start = round(time() * 1000)

        answer_1 = 0

        end_1 = round(time() * 1000)

        answer_2 = 0

        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 8, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 8, 2))
