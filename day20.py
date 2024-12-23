from heapq import heappush, heappop
from time import time

from util.args import parse_args
from util.datastructures import Grid
from util.submit import submit_answer


class CPURace(Grid):
    def __init__(self, rows):
        super().__init__(rows)
        self.start = (-1, -1)
        self.end = (-1, -1)

        def parse_tile(x, y):
            if self.get_val_at(x, y) == 'S':
                self.start = (x, y)
            if self.get_val_at(x, y) == 'E':
                self.end = (x, y)

        self.foreach(parse_tile)

    def find_shortest_path(self):
        open_pos = []
        heappush(open_pos, (0, self.start, [self.start]))

        while open_pos:
            score, current, path = heappop(open_pos)

            if current == self.end:
                return path

            neighbours = [n for n in self.get_neighbours(*current) if n not in path]

            for n in neighbours:
                if self.get_val_at(*n) != '#':
                    heappush(open_pos, (score + 1, n, path + [n]))

        return -1, None

    def find_shortcuts(self, cheat_length):
        shortest_path = self.find_shortest_path()
        short_cuts = 0

        time_dict = {}
        for idx, pos in enumerate(shortest_path):
            time_dict[pos] = idx

        for idx, pos in enumerate(shortest_path):
            remaining_path = shortest_path[idx + 101:]

            for target in remaining_path:
                distance = abs(pos[0] - target[0]) + abs(pos[1] - target[1])

                if distance <= cheat_length and (time_dict[target] - time_dict[pos] - distance) >= 100:
                    short_cuts += 1

        return short_cuts


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        rows = file.readlines()

    race = CPURace(rows)

    start = round(time() * 1000)

    answer_1 = race.find_shortcuts(2)

    end_1 = round(time() * 1000)

    answer_2 = race.find_shortcuts(20)

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 20, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 20, 2))
