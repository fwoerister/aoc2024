import heapq
from time import time

from util.args import parse_args
from util.datastructures import Grid, Vector2D, DirectionVector
from util.submit import submit_answer


class Maze(Grid):
    def __init__(self, rows):
        super().__init__(rows)
        self.start = Vector2D(0, 0)
        self.end = Vector2D(0, 0)
        self.start_dir = DirectionVector.from_char('>')

        self.visited_from = {}

        for x in range(self.width):
            for y in range(self.height):
                self.visited_from[Vector2D(x, y)] = []

        def parse_tile(x, y):
            if self.get_val_at(x, y) == 'S':
                self.start = Vector2D(x, y)
            if self.get_val_at(x, y) == 'E':
                self.end = Vector2D(x, y)

        self.foreach(parse_tile)

    def find_shortest_path(self):
        open_nodes = []
        heapq.heappush(open_nodes, (0, self.start, self.start_dir, [self.start]))

        min_score = None
        min_paths = []

        score = {
            (self.start, self.start_dir): 0
        }

        while open_nodes:
            cost, current_pos, current_dir, current_path = heapq.heappop(open_nodes)

            if min_score and min_score < cost:
                return min_score, min_paths
            elif self.get_val_at(current_pos.x, current_pos.y) == 'E':
                min_score = cost
                min_paths.append(current_path)
                continue

            neighbours = [
                (cost + 1000, current_pos, current_dir.rotate_clockwise(), current_path),
                (cost + 1000, current_pos, current_dir.rotate_counter_clockwise(), current_path),
            ]

            next_straight_move = current_pos + current_dir
            if self.get_val_at(next_straight_move.x, next_straight_move.y) != '#':
                neighbours.append((cost + 1, next_straight_move, current_dir, current_path + [next_straight_move]))

            for n in neighbours:
                if (n[1], n[2]) not in score or score[n[1], n[2]] >= n[0]:
                    score[(n[1], n[2])] = n[0]
                    heapq.heappush(open_nodes, n)

        return min_score, min_paths


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        lines = file.readlines()

    start = round(time() * 1000)

    m = Maze(lines)
    answer_1, _ = m.find_shortest_path()

    end_1 = round(time() * 1000)

    _, paths = m.find_shortest_path()

    visited_nodes = set()
    for path in paths:
        for pos in path:
            visited_nodes.add(pos)

    answer_2 = len(visited_nodes)

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 11, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 11, 2))
