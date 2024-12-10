from util.args import parse_args
from util.datastructures import Grid
from util.submit import submit_answer
from time import time

DIRECTIONS = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}

NEXT_DIRECTION = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^',
}


class GuardianGrid(Grid):
    def __init__(self, rows):
        super().__init__(rows)

        self.start_pos = None
        self.start_dir = None

        def find_and_store_start_pos(x, y):
            if self.rows[y][x] in ['^', '>', 'v', '<']:
                self.start_pos = (x, y)
                self.start_dir = self.rows[y][x]

        self.foreach(find_and_store_start_pos)

    def move_next_obstacle(self, start, direction):
        current = start
        fields = []

        while self.is_on_grid(*current) and self.rows[current[1]][current[0]] != '#':
            fields.append(current)
            current = (current[0] + DIRECTIONS[direction][0], current[1] + DIRECTIONS[direction][1])

        if not self.is_on_grid(*current):
            current = None
        elif len(fields) == 1:
            current = None
            fields = []
        else:
            current = fields[-1]
            fields = fields[:-1]

        return current, fields

    def get_visited_fields(self, exclude_start=False):
        current_pos = self.start_pos
        current_dir = self.start_dir

        visited_fields = set()

        while current_pos:
            current_pos, traversed_fields = self.move_next_obstacle(current_pos, current_dir)
            visited_fields.update(traversed_fields)
            current_dir = NEXT_DIRECTION[current_dir]

        if exclude_start:
            visited_fields.remove(self.start_pos)

        return visited_fields

    def is_loop(self):
        current_pos = self.start_pos
        current_dir = self.start_dir

        visited_pos = set()

        while current_pos and current_pos not in visited_pos:
            visited_pos.add(current_pos)
            current_pos, fields = self.move_next_obstacle(current_pos, current_dir)
            current_dir = NEXT_DIRECTION[current_dir]

        return current_pos is not None

    def find_possible_loops(self):
        loops = 0
        for new_obst in self.get_visited_fields(exclude_start=True):
            self.rows[new_obst[1]][new_obst[0]] = '#'
            if self.is_loop():
                loops += 1
            self.rows[new_obst[1]][new_obst[0]] = '.'
        return loops


if __name__ == '__main__':
    args = parse_args()
    answer_1 = 0
    answer_2 = 0

    with args.puzzle_input as file:
        guardian_map = GuardianGrid(file.readlines())
        start = round(time() * 1000)
        answer_1 = len(guardian_map.get_visited_fields())
        end_1 = round(time() * 1000)
        answer_2 = guardian_map.find_possible_loops()
        end_2 = round(time() * 1000)

    print(answer_1)
    print(f"time: {end_1 - start}ms")
    print(answer_2)
    print(f"time: {end_2 - end_1}ms")

    if args.submit == 1:
        print(submit_answer(answer_1, 6, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 6, 2))
