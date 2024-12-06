from util.args import parse_args
from util.submit import submit_answer

NEXT_DIRECTION = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^'
}


class GuardianMap:
    def __init__(self, rows):
        rows = list(map(lambda line: line.strip(), filter(lambda row: row, rows)))
        self.obstacles = []
        self.pos = None
        self.dir = ''

        self.width = len(rows[0])
        self.height = len(rows)

        for row_idx in range(len(rows)):
            for col_idx in range(len(rows[row_idx])):
                if rows[row_idx][col_idx] == '#':
                    self.obstacles.append((col_idx, row_idx))
                if rows[row_idx][col_idx] in ['^', 'v', '>', '<']:
                    self.pos = (col_idx, row_idx)
                    self.dir = rows[row_idx][col_idx]

    def get_possible_loops(self, path, visited):
        possible_loops = 0

        for field in path:
            match field[2]:
                case '^':
                    loopable_field = list(filter(lambda pos: pos[0] > field[0]
                                                             and pos[1] == field[1]
                                                             and pos[2] == NEXT_DIRECTION[field[2]], visited))

                    next_obstacle = list(filter(lambda pos: pos[0] > field[0]
                                                            and pos[1] == field[1], self.obstacles))

                    if loopable_field:
                        loopable_field = min(loopable_field, key=lambda t: t[0])

                        if not next_obstacle:
                            possible_loops += 1
                        else:
                            next_obstacle = min(next_obstacle, key=lambda t: t[0])
                            if loopable_field[0] < next_obstacle[0]:
                                possible_loops += 1

                case '>':
                    loopable_field = list(filter(lambda pos: pos[0] == field[0]
                                                             and pos[1] > field[1]
                                                             and pos[2] == NEXT_DIRECTION[field[2]], visited))

                    next_obstacle = list(filter(lambda pos: pos[0] == field[0]
                                                            and pos[1] > field[1], self.obstacles))

                    if loopable_field:
                        loopable_field = min(loopable_field, key=lambda t: t[1])

                        if not next_obstacle:
                            possible_loops += 1
                        else:
                            next_obstacle = min(next_obstacle, key=lambda t: t[1])
                            if loopable_field[1] < next_obstacle[1]:
                                possible_loops += 1

                case 'v':
                    loopable_field = list(filter(lambda pos: pos[0] < field[0]
                                                             and pos[1] == field[1]
                                                             and pos[2] == NEXT_DIRECTION[field[2]], visited))

                    next_obstacle = list(filter(lambda pos: pos[0] < field[0]
                                                            and pos[1] == field[1], self.obstacles))

                    if loopable_field:
                        loopable_field = max(loopable_field, key=lambda t: t[0])

                        if not next_obstacle:
                            possible_loops += 1
                        else:
                            next_obstacle = max(next_obstacle, key=lambda t: t[0])
                            if loopable_field[0] > next_obstacle[0]:
                                possible_loops += 1

                case '<':
                    loopable_field = list(filter(lambda pos: pos[0] == field[0]
                                                             and pos[1] < field[1]
                                                             and pos[2] == NEXT_DIRECTION[field[2]], visited))

                    next_obstacle = list(filter(lambda pos: pos[0] == field[0]
                                                            and pos[1] < field[1], self.obstacles))

                    if loopable_field:
                        loopable_field = max(loopable_field, key=lambda t: t[1])

                        if not next_obstacle:
                            possible_loops += 1
                        else:
                            next_obstacle = max(next_obstacle, key=lambda t: t[1])
                            if loopable_field[1] > next_obstacle[1]:
                                possible_loops += 1

        return possible_loops

    def calculate_route_length(self):
        visited = [(self.pos[0], self.pos[1], self.dir)]
        next_obstacle = (-1, -1)
        loops_possible = 0

        while next_obstacle:
            if self.dir == '^':
                next_obstacle = list(
                    filter(lambda obst: obst[0] == self.pos[0] and obst[1] < self.pos[1], self.obstacles))
                if next_obstacle:
                    next_obstacle = max(next_obstacle, key=lambda pos: pos[1])

                    next_move = [(self.pos[0], y, '^') for y in range(next_obstacle[1] + 1, self.pos[1])]

                    loops_possible += self.get_possible_loops(next_move, visited)

                    visited.extend(next_move)

                    self.pos = (next_obstacle[0], next_obstacle[1] + 1)
                    self.dir = NEXT_DIRECTION[self.dir]

            elif self.dir == '>':
                next_obstacle = list(
                    filter(lambda obst: obst[0] > self.pos[0] and obst[1] == self.pos[1], self.obstacles))

                if next_obstacle:
                    next_obstacle = min(next_obstacle, key=lambda pos: pos[0])
                    next_move = [(x, self.pos[1], '>') for x in range(self.pos[0] + 1, next_obstacle[0])]

                    loops_possible += self.get_possible_loops(next_move, visited)

                    visited.extend(next_move)

                    self.pos = (next_obstacle[0] - 1, next_obstacle[1])
                    self.dir = NEXT_DIRECTION[self.dir]
            elif self.dir == 'v':
                next_obstacle = list(
                    filter(lambda obst: obst[0] == self.pos[0] and obst[1] > self.pos[1], self.obstacles))

                if next_obstacle:
                    next_obstacle = min(next_obstacle, key=lambda pos: pos[1])

                    next_move = [(self.pos[0], y, 'v') for y in range(self.pos[1] + 1, next_obstacle[1])]

                    loops_possible += self.get_possible_loops(next_move, visited)

                    visited.extend(next_move)

                    self.pos = (next_obstacle[0], next_obstacle[1] - 1)
                    self.dir = NEXT_DIRECTION[self.dir]

            elif self.dir == '<':
                next_obstacle = list(
                    filter(lambda obst: obst[0] < self.pos[0] and obst[1] == self.pos[1], self.obstacles))

                if next_obstacle:
                    next_obstacle = max(next_obstacle, key=lambda pos: pos[0])

                    next_move = [(x, self.pos[1], '<') for x in range(next_obstacle[0] + 1, self.pos[0])]

                    loops_possible += self.get_possible_loops(next_move, visited)

                    visited.extend(next_move)

                    self.pos = (next_obstacle[0] + 1, next_obstacle[1])
                    self.dir = NEXT_DIRECTION[self.dir]

        if self.dir == '^':
            next_move = [(self.pos[0], y, '^') for y in range(self.pos[1])]
            loops_possible += self.get_possible_loops(next_move, visited)
            visited.extend(next_move)
        elif self.dir == '>':
            next_move = [(x, self.pos[1], '>') for x in range(self.pos[0] + 1, self.width)]
            loops_possible += self.get_possible_loops(next_move, visited)
            visited.extend(next_move)
        elif self.dir == 'v':
            next_move = [(self.pos[0], y, 'v') for y in range(self.pos[1] + 1, self.height)]
            loops_possible += self.get_possible_loops(next_move, visited)
            visited.extend(next_move)
        elif self.dir == '<':
            next_move = [(x, self.pos[1], '<') for x in range(self.pos[0])]
            loops_possible += self.get_possible_loops(next_move, visited)
            visited.extend(next_move)

        visited = set(map(lambda tuple: (tuple[0], tuple[1]), visited))

        return len(visited), loops_possible


if __name__ == '__main__':
    args = parse_args()
    answer_1 = 0
    answer_2 = 0

    with args.puzzle_input as file:
        guardian_map = GuardianMap(file.readlines())

    answer_1, answer_2 = guardian_map.calculate_route_length()

    print(answer_1)
    print(answer_2)

    if args.submit == 1:
        print(submit_answer(answer_1, 6, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 6, 2))
