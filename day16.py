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

OPPOSITE_DIR = {
    '>': (-1, 0),
    '<': (1, 0),
    'v': (0, -1),
    '^': (0, 1),
}


class Maze(Grid):
    def __init__(self, rows):
        super().__init__(rows)
        self.start = (0, 0, '>')
        self.end = (0, 0)
        self.came_from = {

        }

        def parse_tile(x, y):
            if self.get_val_at(x, y) == 'S':
                self.start = (x, y, '>')
            if self.get_val_at(x, y) == 'E':
                self.end = (x, y)

        self.foreach(parse_tile)

    @staticmethod
    def get_score(pos, direction):
        if DIR[pos] == direction:
            return 1
        elif OPPOSITE_DIR[pos] == direction:
            return 2001
        else:
            return 1001

    def reconstruct_path(self, current):
        total_path = []
        while (current[0], current[1]) in self.came_from:
            current_with_dir = self.came_from[(current[0], current[1])]
            total_path = [current_with_dir] + total_path
            current = (current_with_dir[0], current_with_dir[1])
        return total_path

    def find_shortest_path_score(self):
        open_paths = []
        heapq.heappush(open_paths, (0, self.start))

        scores = {
            (self.start[0], self.start[1]): 0
        }

        while open_paths:
            current_score, pos = heapq.heappop(open_paths)
            scores[(pos[0], pos[1])] = current_score

            if pos[0] == self.end[0] and pos[1] == self.end[1]:
                return current_score, self.reconstruct_path((pos[0], pos[1]))

            neighbours = [
                (self.get_score(pos[2], DIR['<']), (pos[0] - 1, pos[1], '<')),
                (self.get_score(pos[2], DIR['>']), (pos[0] + 1, pos[1], '>')),
                (self.get_score(pos[2], DIR['^']), (pos[0], pos[1] - 1, '^')),
                (self.get_score(pos[2], DIR['v']), (pos[0], pos[1] + 1, 'v')),
            ]

            neighbours = list(filter(lambda n: self.get_val_at(n[1][0], n[1][1]) != '#', neighbours))

            for n in neighbours:
                new_score = current_score + n[0]
                if (n[1][0], n[1][1]) not in scores or new_score < scores[(n[1][0], n[1][1])]:
                    self.came_from[(n[1][0], n[1][1])] = pos
                    heapq.heappush(open_paths, (new_score, n[1]))

        raise ValueError('No path found')


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        lines = file.readlines()

    start = round(time() * 1000)

    m = Maze(lines)
    answer_1, path = m.find_shortest_path_score()

    for pos in path:
        m.set_val_at(pos[0], pos[1], pos[2])
    m.print_grid()

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
