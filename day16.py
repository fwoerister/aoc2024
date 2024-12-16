import heapq

from time import time

from util.args import parse_args
from util.datastructures import Grid
from util.submit import submit_answer

DIR = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
}


class Maze(Grid):
    def __init__(self, rows):
        super().__init__(rows)
        self.start = (0, 0, '<')
        self.end = (0, 0)

        def parse_tile(x, y):
            if self.get_val_at(x, y) == 'S':
                self.start = (x, y, '<')
            if self.get_val_at(x, y) == 'E':
                self.end = (x, y)

        self.foreach(parse_tile)

    def find_shortest_path_score(self):
        open_paths = []
        heapq.heappush(open_paths, (0, self.start))

        came_from = {}

        scores = {
            (self.start[0], self.start[1]): 0
        }

        while open_paths:
            current_score, pos = heapq.heappop(open_paths)

            if pos[0] == self.end[0] and pos[1] == self.end[1]:
                return current_score

            neighbours = [
                (1 if pos[2] == '<' else 1000, (pos[0] - 1, pos[1], '<')),
                (1 if pos[2] == '>' else 1000, (pos[0] + 1, pos[1], '>')),
                (1 if pos[2] == '^' else 1000, (pos[0], pos[1] - 1, '^')),
                (1 if pos[2] == 'v' else 1000, (pos[0], pos[1] + 1, 'v')),
            ]

            neighbours = list(filter(lambda n: self.get_val_at(n[1][0], n[1][1]) != '#', neighbours))

            for neighbour in neighbours:
                new_score = current_score + neighbour[0]
                if (neighbour[1][0], neighbour[1][1]) not in scores or new_score < scores[(neighbour[1][0], neighbour[1][1])]:
                    scores[(neighbour[1][0], neighbour[1][1])] = new_score

                    heapq.heappush(open_paths, (new_score, neighbour[1]))

        raise ValueError('No path found')


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        lines = file.readlines()

    start = round(time() * 1000)

    answer_1 = Maze(lines).find_shortest_path_score()

    end_1 = round(time() * 1000)

    answer_2 = 0

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 11, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 11, 2))
