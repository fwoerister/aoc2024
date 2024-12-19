import functools
from time import time

from util.args import parse_args
from util.submit import submit_answer


class TowelPuzzleSolver:
    def __init__(self, available_patterns):
        self.available_patterns = available_patterns

    def find_towel_combination_for(self, design):
        if design == "":
            return []

        for pattern in self.available_patterns:
            if design.startswith(pattern):
                towels = self.find_towel_combination_for(design[len(pattern):])
                if towels is not None:
                    return [pattern] + towels

    @functools.cache
    def count_possible_towel_combinations_for(self, design):
        if design == "":
            return 1

        count = 0

        for pattern in self.available_patterns:
            if design.startswith(pattern):
                count += self.count_possible_towel_combinations_for(design[len(pattern):])

        return count


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        towel_patterns = [towel.strip() for towel in file.readline().split(',')]
        file.readline()

        designs = [design.strip() for design in file.readlines() if design]

    towel_puzzle_solver = TowelPuzzleSolver(towel_patterns)

    start = round(time() * 1000)

    answer_1 = 0

    for design in designs:
        solution = towel_puzzle_solver.find_towel_combination_for(design)
        if solution:
            answer_1 += 1

    end_1 = round(time() * 1000)

    answer_2 = 0

    for design in designs:
        answer_2 += towel_puzzle_solver.count_possible_towel_combinations_for(design)

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 19, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 19, 2))
