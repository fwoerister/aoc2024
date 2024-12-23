from time import time

from util.args import parse_args
from util.datastructures import Grid
from util.submit import submit_answer


class HikingGrid(Grid):
    def __init__(self, rows):
        super().__init__(rows)

        self.convert_to_int_vals()

        self.heads = []

        def add_head_if_val_is_zero(x, y):
            if self.get_val_at(x, y) == 0:
                self.heads.append((x, y))

        self.foreach(add_head_if_val_is_zero)

    def is_incremental(self, x, y, next_x, next_y):
        return self.get_val_at(x, y) + 1 == self.get_val_at(next_x, next_y)

    def is_valid_step(self, x, y, next_x, next_y):
        return self.is_on_grid(next_x, next_y) and self.is_incremental(x, y, next_x, next_y)

    def get_next_single_step_climbs(self, x, y):
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
                next_steps = self.get_next_single_step_climbs(*(trail[-1]))
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
        hiking_map = HikingGrid(file.readlines())
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
