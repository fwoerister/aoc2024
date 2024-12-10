from time import time

from util.args import parse_args
from util.submit import submit_answer


class Puzzle:
    def __init__(self, puzzle_input):
        self.puzzle = list(map(lambda puzzle_row: puzzle_row.strip(),
                               filter(lambda puzzle_row: puzzle_row,
                                      puzzle_input)))
        self.rows = len(self.puzzle)
        self.cols = len(self.puzzle[0])

    def is_on_puzzle(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows

    def get_horizontal_word(self, x, y, word_len):
        start = (x, y)
        end = (x + (word_len - 1), y)

        if not (self.is_on_puzzle(*start) and self.is_on_puzzle(*end)):
            return ""

        line = self.puzzle[y]
        word = line[x:x + word_len]
        return word

    def get_vertical_word(self, x, y, word_len):
        start = (x, y)
        end = (x, y + (word_len - 1))

        if not (self.is_on_puzzle(*start) and self.is_on_puzzle(*end)):
            return ""

        word = ""
        for i in range(0, word_len):
            word += self.puzzle[y + i][x]

        return word

    def get_diagonal_word(self, x, y, word_len):
        start = (x, y)
        end = (x - (word_len - 1), y + (word_len - 1))

        if not (self.is_on_puzzle(*start) and self.is_on_puzzle(*end)):
            return ""

        word = ""
        for i in range(0, word_len):
            word += self.puzzle[y + i][x - i]

        return word

    def get_anti_diagonal_word(self, x, y, word_len):
        start = (x, y)
        end = (x + (word_len - 1), y + (word_len - 1))

        if not (self.is_on_puzzle(*start) and self.is_on_puzzle(*end)):
            return ""

        word = ""
        for i in range(0, word_len):
            word += self.puzzle[y + i][x + i]

        return word

    def count_xmas_instances(self):
        count = 0
        for col in range(puzzle.cols):
            for row in range(puzzle.rows):
                if puzzle.get_horizontal_word(col, row, 4) in ['XMAS', 'SAMX']:
                    count += 1
                if puzzle.get_vertical_word(col, row, 4) in ['XMAS', 'SAMX']:
                    count += 1
                if puzzle.get_diagonal_word(col, row, 4) in ['XMAS', 'SAMX']:
                    count += 1
                if puzzle.get_anti_diagonal_word(col, row, 4) in ['XMAS', 'SAMX']:
                    count += 1
        return count

    def count_mas_crosses(self):
        count = 0
        for col in range(puzzle.cols):
            for row in range(puzzle.rows):
                anti_diagonal_word = puzzle.get_anti_diagonal_word(col, row, 3)
                diagonal_word = puzzle.get_diagonal_word(col + 2, row, 3)

                if anti_diagonal_word in ['MAS', 'SAM'] and diagonal_word in ['MAS', 'SAM']:
                    count += 1
        return count


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        puzzle = Puzzle(file.readlines())

        start = round(time() * 1000)
        answer_1 = puzzle.count_xmas_instances()
        end_1 = round(time() * 1000)
        answer_2 = puzzle.count_mas_crosses()
        end_2 = round(time() * 1000)

        print(answer_1)
        print(f'time: {end_1 - start}ms')
        print(answer_2)
        print(f'time: {end_2 - end_1}ms')

        if args.submit == 1:
            print(submit_answer(answer_1, 4, 1))

        if args.submit == 2:
            print(submit_answer(answer_2, 4, 2))
