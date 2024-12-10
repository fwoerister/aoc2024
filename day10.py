from time import time

from util.args import parse_args
from util.submit import submit_answer


class HikingMap:
    def __init__(self, rows):
        self.rows = list(map(lambda line: line.strip(), filter(lambda x: x, rows)))
        self.height = len(self.rows)
        self.width = 0 if self.height == 0 else len(self.rows[0])
        self.heads = self.get_heads()

    def get_heads(self):
        heads = []
        for x in range(self.width):
            for y in range(self.height):
                if self.get_height(x, y) == 0:
                    heads.append((x, y))
        return heads

    def get_height(self, x, y):
        return int(self.rows[y][x])

    def is_on_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_incremental(self, x, y, next_x, next_y):
        return self.get_height(x, y) + 1 == self.get_height(next_x, next_y)

    def is_valid_step(self, x, y, next_x, next_y):
        return self.is_on_map(next_x, next_y) and self.is_incremental(x, y, next_x, next_y)

    def get_neighbours(self, x, y):
        neighbours = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        return list(filter(lambda pos: self.is_valid_step(x, y, *pos), neighbours))

    def find_possible_trails(self, open_trails):
        for height in range(1, 10):
            new_trails = []
            for trail in open_trails:
                next_steps = self.get_neighbours(*(trail[-1]))
                for step in next_steps:
                    new_trails.append(trail + [step])
            open_trails = new_trails
        return open_trails

    def get_trail_score_level1(self, start_pos):
        return len(set(map(lambda trail: trail[-1], self.find_possible_trails([[start_pos]]))))

    def get_trail_score_level2(self, start_pos):
        return len(self.find_possible_trails([[start_pos]]))

    def get_total_score_level1(self):
        score = 0
        for pos in self.heads:
            score += self.get_trail_score_level1(pos)
        return score

    def get_total_score_level2(self):
        score = 0
        for pos in self.heads:
            score += self.get_trail_score_level2(pos)
        return score


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        hiking_map = HikingMap(file.readlines())
        start = round(time() * 1000)

        answer_1 = hiking_map.get_total_score_level1()

        end_1 = round(time() * 1000)

        answer_2 = hiking_map.get_total_score_level2()

        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 9, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 9, 2))
