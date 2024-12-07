from util.args import parse_args
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


class GuardianMap:
    def __init__(self, rows):
        self.map = list(map(lambda e: list(e.strip()), filter(lambda e: e, rows)))
        self.height = len(self.map)
        self.width = len(self.map[0]) if self.height != 0 else 0

        self.start_pos, self.start_dir = self._find_start_pos()

    def _find_start_pos(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.map[y][x] in ['^', '>', 'v', '<']:
                    return (x, y), self.map[y][x]

    def on_map(self, pos):
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def move_next_obstacle(self, start, direction):
        current = start
        fields = []

        while self.on_map(current) and self.map[current[1]][current[0]] != '#':
            fields.append(current)
            current = (current[0] + DIRECTIONS[direction][0], current[1] + DIRECTIONS[direction][1])

        if not self.on_map(current):
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
            self.map[new_obst[1]][new_obst[0]] = '#'
            if self.is_loop():
                loops += 1
            self.map[new_obst[1]][new_obst[0]] = '.'
        return loops


if __name__ == '__main__':
    args = parse_args()
    answer_1 = 0
    answer_2 = 0

    with args.puzzle_input as file:
        guardian_map = GuardianMap(file.readlines())
        start = round(time() * 1000)
        answer_1 = len(guardian_map.get_visited_fields())
        end_1 = round(time() * 1000)
        answer_2 = guardian_map.find_possible_loops()
        end_2 = round(time() * 1000)

    print(answer_1)
    print(f"time: {end_1 - start}")
    print(answer_2)
    print(f"time: {end_2 - end_1}")

    if args.submit == 1:
        print(submit_answer(answer_1, 6, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 6, 2))
