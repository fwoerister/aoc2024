from time import time

from util.args import parse_args
from util.datastructures import Grid
from util.submit import submit_answer

DIR = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}


class Warehouse(Grid):
    def __init__(self, rows):
        super().__init__(rows)
        self.current = (0, 0)

        def set_start_pos(x, y):
            if self.get_val_at(x, y) == '@':
                self.current = (x, y)

        self.foreach(set_start_pos)

    def get_next_empty_position(self, direction):
        next_free = self.current
        next_free = (next_free[0] + direction[0], next_free[1] + direction[1])
        while self.get_val_at(*next_free) in ['O', '[', ']']:
            next_free = (next_free[0] + direction[0], next_free[1] + direction[1])

        return next_free if self.get_val_at(*next_free) == '.' else None

    def move_l1(self, direction):
        next_free = self.get_next_empty_position(direction)
        if next_free and self.get_val_at(*next_free) == '.':
            self.set_val_at(*self.current, '.')
            self.current = (self.current[0] + direction[0], self.current[1] + direction[1])
            self.set_val_at(*self.current, '@')

            if next_free != self.current:
                self.set_val_at(*next_free, 'O')

    def move_box_vertical(self, x, y, v_dir):
        if self.get_val_at(x, y) == '[':
            second_box_tile = (x + 1, y)
        else:
            second_box_tile = (x - 1, y)

        if self.get_val_at(x, y + v_dir) in ['[', ']']:
            self.move_box_vertical(x, y + v_dir, v_dir)

        if self.get_val_at(second_box_tile[0], y + v_dir) in ['[', ']']:
            self.move_box_vertical(second_box_tile[0], y + v_dir, v_dir)

        self.set_val_at(x, y + v_dir, self.get_val_at(x, y))
        self.set_val_at(second_box_tile[0], y + v_dir, self.get_val_at(second_box_tile[0], y))

        self.set_val_at(x, y, '.')
        self.set_val_at(second_box_tile[0], y, '.')

    def move_box_horizontal(self, x, y, h_dir):
        free_spot = self.get_next_empty_position((h_dir, 0))

        if free_spot and self.get_val_at(*free_spot) == '.':
            for idx in range(free_spot[0], x, -h_dir):
                self.set_val_at(idx, y, self.get_val_at(idx - h_dir, y))

    def can_move(self, x, y, direction):
        if self.get_val_at(x, y) == '[':
            x += 1

        if direction == (-1, 0):
            neighbour_tile = self.get_val_at(x - 2, y)
            if neighbour_tile == '.':
                return True
            if neighbour_tile == '#':
                return False
            return self.can_move(x - 2, y, direction)
        if direction == (1, 0):
            neighbour_tile = self.get_val_at(x + 1, y)
            if neighbour_tile == '.':
                return True
            if neighbour_tile == '#':
                return False
            return self.can_move(x + 1, y, direction)

        neighbour_tiles = [self.get_val_at(x - 1, y + direction[1]), self.get_val_at(x, y + direction[1])]

        if neighbour_tiles == ['.', '.']:
            return True
        if '#' in neighbour_tiles:
            return False
        if neighbour_tiles == ['[', ']']:
            return self.can_move(x, y + direction[1], direction)

        if neighbour_tiles[0] == ']' and not self.can_move(x - 1, y + direction[1], direction):
            return False
        if neighbour_tiles[1] == '[' and not self.can_move(x, y + direction[1], direction):
            return False
        return True

    def move_l2(self, direction):
        new_pos = (self.current[0] + direction[0], self.current[1] + direction[1])

        if self.get_val_at(*new_pos) == '.':
            self.set_val_at(*new_pos, self.get_val_at(*self.current))
            self.set_val_at(*self.current, '.')
            self.current = new_pos
        elif self.get_val_at(*new_pos) == '#':
            return
        elif self.can_move(*new_pos, direction):
            if direction in [(1, 0), (-1, 0)]:
                self.move_box_horizontal(*new_pos, direction[0])
            else:
                self.move_box_vertical(*new_pos, direction[1])

            self.set_val_at(*self.current, '.')
            self.current = (self.current[0] + direction[0], self.current[1] + direction[1])
            self.set_val_at(*self.current, '@')

    def count_box_cluster(self, x, y, dir):
        if self.get_val_at(x, y) == '[':
            x -= 1

        if dir in [(1, 0), (-1, 0)]:
            next_free = self.get_next_empty_position(dir)
            return abs(self.current[0] - next_free[0]) // 2

    def calculate_gps_coordinates(self):
        gps = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.get_val_at(x, y) in ['[', 'O']:
                    gps += 100 * y + x

        return gps


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        grid = []
        directions = ''
        while (line := file.readline()) != '\n':
            grid.append(line.strip())

        while line := file.readline():
            directions += line.strip()

    warehouse_l1 = Warehouse(grid)
    grid = list(map(lambda l: l.replace('.', '..').replace('#', '##').replace('O', '[]').replace('@', '@.'), grid))
    warehouse_l2 = Warehouse(grid)

    start = round(time() * 1000)

    for direction in directions:
        warehouse_l1.move_l1(DIR[direction])

    answer_1 = warehouse_l1.calculate_gps_coordinates()

    end_1 = round(time() * 1000)

    for direction in directions:
        warehouse_l2.move_l2(DIR[direction])

    answer_2 = warehouse_l2.calculate_gps_coordinates()

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 11, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 11, 2))
