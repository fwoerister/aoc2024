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

        self.width = len(rows[0])
        self.height = len(rows)

        for row_idx in range(len(rows)):
            for col_idx in range(len(rows[row_idx])):
                if rows[row_idx][col_idx] == '#':
                    self.obstacles.append((col_idx, row_idx))
                if rows[row_idx][col_idx] in ['^', 'v', '>', '<']:
                    self.pos = (col_idx, row_idx, rows[row_idx][col_idx])

    def is_loop(self):
        visited = [(self.pos[0], self.pos[1], self.pos[2])]
        current = (self.pos[0], self.pos[1], self.pos[2])
        next_obstacle = (-1, -1)

        while next_obstacle:
            if current[2] == '^':
                next_obstacle = list(
                    filter(lambda obst: obst[0] == current[0] and obst[1] < current[1], self.obstacles))
                if next_obstacle:
                    next_obstacle = max(next_obstacle, key=lambda pos: pos[1])
                    next_move = [(current[0], y, '^') for y in range(next_obstacle[1] + 1, current[1])]

                    if next_move and next_move[-1] in visited:
                        return True

                    visited.extend(next_move)

                    current = (next_obstacle[0], next_obstacle[1] + 1, NEXT_DIRECTION[current[2]])

            elif current[2] == '>':
                next_obstacle = list(filter(lambda obst: obst[0] > current[0] and obst[1] == current[1],
                                            self.obstacles))

                if next_obstacle:
                    next_obstacle = min(next_obstacle, key=lambda pos: pos[0])
                    next_move = [(x, current[1], '>') for x in range(current[0] + 1, next_obstacle[0])]
                    if next_move and next_move[-1] in visited:
                        return True
                    visited.extend(next_move)

                    current = (next_obstacle[0] - 1, next_obstacle[1], NEXT_DIRECTION[current[2]])

            elif current[2] == 'v':
                next_obstacle = list(filter(lambda obst: obst[0] == current[0] and obst[1] > current[1],
                                            self.obstacles))

                if next_obstacle:
                    next_obstacle = min(next_obstacle, key=lambda pos: pos[1])
                    next_move = [(current[0], y, 'v') for y in range(current[1] + 1, next_obstacle[1])]
                    if next_move and next_move[-1] in visited:
                        return True
                    visited.extend(next_move)

                    current = (next_obstacle[0], next_obstacle[1] - 1, NEXT_DIRECTION[current[2]])
            elif current[2] == '<':
                next_obstacle = list(filter(lambda obst: obst[0] < current[0] and obst[1] == current[1],
                                            self.obstacles))

                if next_obstacle:
                    next_obstacle = max(next_obstacle, key=lambda pos: pos[0])
                    next_move = [(x, current[1], '<') for x in range(next_obstacle[0] + 1, current[0])]
                    if next_move and next_move[-1] in visited:
                        return True
                    visited.extend(next_move)

                    current = (next_obstacle[0] + 1, next_obstacle[1], NEXT_DIRECTION[current[2]])

        return False

    def find_possible_loops(self):
        count = 0
        possible_obst = []
        for row_idx in range(self.height):
            for col_idx in range(self.width):
                new_obst = (col_idx, row_idx)
                if new_obst not in self.obstacles:
                    possible_obst.append(new_obst)

        for obst in possible_obst:
            self.obstacles.append(obst)
            if self.is_loop():
                count += 1
                print(obst)
            self.obstacles.remove(obst)

        return count


if __name__ == '__main__':
    args = parse_args()
    answer_1 = 0
    answer_2 = 0

    with args.puzzle_input as file:
        guardian_map = GuardianMap(file.readlines())

    print(guardian_map.is_loop())
    answer_2 = guardian_map.find_possible_loops()

    print(answer_1)
    print(answer_2)

    if args.submit == 1:
        print(submit_answer(answer_1, 6, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 6, 2))
