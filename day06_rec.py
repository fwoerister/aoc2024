from util.args import parse_args
from util.submit import submit_answer

TOP = '^'
RIGHT = '>'
DOWN = 'v'
LEFT = '<'

NEXT_DIR = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^',
}


class GuardianMap:
    def __init__(self, rows):
        self.rows = list(map(lambda line: line.strip(), filter(lambda row: row, rows)))
        self.obstacles = []
        self.neighbours = {}
        self.fields_to_neighbour = {}
        self.start_pos = None
        self.start_dir = None

        self.width = len(self.rows[0])
        self.height = len(self.rows)

        self.parse_map_objects()
        self.init_neighbours()

    def parse_map_objects(self):
        for row_idx in range(self.height):
            for col_idx in range(self.width):
                if self.rows[row_idx][col_idx] == '#':
                    self.obstacles.append((col_idx, row_idx))
                if self.rows[row_idx][col_idx] in ['^', 'v', '>', '<']:
                    self.start_pos = (col_idx, row_idx)
                    self.start_dir = self.rows[row_idx][col_idx]

    def init_neighbours(self):

        neighbours = [self.start_pos]

        for obst in self.obstacles:
            for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbour = (obst[0] + offset[0], obst[1] + offset[1])
                if 0 <= neighbour[0] < self.width and 0 <= neighbour[1] < self.height:
                    neighbours.append(neighbour)

        for neighbour in neighbours:

            if not (0 <= neighbour[0] < self.width and 0 <= neighbour[1] < self.height):
                continue

            if neighbour not in self.neighbours:
                self.neighbours[neighbour] = dict()
                self.fields_to_neighbour[neighbour] = dict()

                obst_top = list(filter(lambda pos: pos[0] == neighbour[0] and pos[1] < neighbour[1],
                                       self.obstacles))
                obst_right = list(filter(lambda pos: pos[0] > neighbour[0] and pos[1] == neighbour[1],
                                         self.obstacles))
                obst_down = list(filter(lambda pos: pos[0] == neighbour[0] and pos[1] > neighbour[1],
                                        self.obstacles))
                obst_left = list(filter(lambda pos: pos[0] < neighbour[0] and pos[1] == neighbour[1],
                                        self.obstacles))

                if obst_top:
                    obst_top = max(obst_top, key=lambda pos: pos[1])
                    self.neighbours[neighbour][TOP] = (obst_top[0], obst_top[1] + 1)
                    self.fields_to_neighbour[neighbour][TOP] = [(neighbour[0], y) for y in
                                                                range(neighbour[1] - 1, obst_top[1], -1)]
                else:
                    self.fields_to_neighbour[neighbour][TOP] = [(neighbour[0], y) for y in
                                                                range(neighbour[1] - 1, -1, -1)]

                if obst_right:
                    obst_right = min(obst_right, key=lambda pos: pos[0])
                    self.neighbours[neighbour][RIGHT] = (obst_right[0] - 1, obst_right[1])
                    self.fields_to_neighbour[neighbour][RIGHT] = [(x, neighbour[1]) for x in
                                                                  range(neighbour[0] + 1, obst_right[0])]
                else:
                    self.fields_to_neighbour[neighbour][RIGHT] = [(x, neighbour[1]) for x in
                                                                  range(neighbour[0] + 1, self.width)]

                if obst_down:
                    obst_down = min(obst_down, key=lambda pos: pos[1])
                    self.neighbours[neighbour][DOWN] = (obst_down[0], obst_down[1] - 1)
                    self.fields_to_neighbour[neighbour][DOWN] = [(neighbour[0], y) for y in
                                                                 range(neighbour[1] + 1, obst_down[1])]
                else:
                    self.fields_to_neighbour[neighbour][DOWN] = [(neighbour[0], y) for y in
                                                                 range(neighbour[1] + 1, self.height)]

                if obst_left:
                    obst_left = max(obst_left, key=lambda pos: pos[0])
                    self.neighbours[neighbour][LEFT] = (obst_left[0] + 1, obst_left[1])
                    self.fields_to_neighbour[neighbour][LEFT] = [(x, neighbour[1]) for x in
                                                                 range(neighbour[1] - 1, obst_left[1], -1)]
                else:
                    self.fields_to_neighbour[neighbour][LEFT] = [(x, neighbour[1]) for x in
                                                                 range(neighbour[1] - 1, -1, -1)]

    def get_visited_fields(self):
        current_pos = self.start_pos
        current_dir = self.start_dir

        visited = []

        while current_pos:
            visited.extend(self.fields_to_neighbour[current_pos][current_dir])
            current_pos = self.neighbours[current_pos].get(current_dir, None)
            current_dir = NEXT_DIR[current_dir]

        return len(set(visited))


if __name__ == '__main__':
    args = parse_args()
    answer_1 = 0
    answer_2 = 0

    with args.puzzle_input as file:
        guardian_map = GuardianMap(file.readlines())
        answer_1 = guardian_map.get_visited_fields()

    print(answer_1)
    print(answer_2)

    if args.submit == 1:
        print(submit_answer(answer_1, 6, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 6, 2))
