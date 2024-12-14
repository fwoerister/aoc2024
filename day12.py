from time import time

from util.args import parse_args
from util.datastructures import Grid
from util.submit import submit_answer


class Garden(Grid):
    def __init__(self, rows):
        super().__init__(rows)

        self.garden_dict = dict()

        def parse_garden(x, y):
            if self.get_val_at(x, y) in self.garden_dict:
                self.garden_dict[self.get_val_at(x, y)].add((x, y))
            else:
                self.garden_dict[self.get_val_at(x, y)] = {(x, y)}

        self.foreach(parse_garden)

    def extract_region(self, label):
        start = self.garden_dict[label].pop()

        return self.extract_region_rec(start, label, {start})

    def extract_region_rec(self, pos, label, visited):
        region = {pos}
        neighbours = self.get_neighbours(*pos)
        neighbours = list(filter(lambda ne: ne not in visited and self.get_val_at(*ne) == label, neighbours))

        for n in neighbours:
            visited.add(n)
            region = region.union(region, self.extract_region_rec(n, label, visited))

        return region

    def get_perimeter(self, region):
        perimeter = 0
        for pos in region:
            neighbours = self.get_neighbours(*pos)
            neighbours = list(filter(lambda ne: ne in region, neighbours))
            perimeter += 4 - len(neighbours)
        return perimeter

    def get_sides(self, region):
        sides = 0

        for field in region:
            v_neighbours = self.get_vertical_neighbours(*field)
            h_neighbours = self.get_horizontal_neighbours(*field)
            v_neighbours = list(filter(lambda ne: ne in region, v_neighbours))
            h_neighbours = list(filter(lambda ne: ne in region, h_neighbours))

            if len(v_neighbours) + len(h_neighbours) == 1:
                sides += 2

            if (self.get_val_at(*field) == self.get_val_at(field[0], field[1] - 1) and
                    self.get_val_at(*field) == self.get_val_at(field[0] + 1, field[1]) and
                    self.get_val_at(*field) != self.get_val_at(field[0] + 1, field[1] - 1)):
                sides += 1

            if (self.get_val_at(*field) == self.get_val_at(field[0] + 1, field[1]) and
                    self.get_val_at(*field) == self.get_val_at(field[0], field[1] + 1) and
                    self.get_val_at(*field) != self.get_val_at(field[0] + 1, field[1] + 1)):
                sides += 1

            if (self.get_val_at(*field) == self.get_val_at(field[0], field[1] + 1) and
                    self.get_val_at(*field) == self.get_val_at(field[0] - 1, field[1]) and
                    self.get_val_at(*field) != self.get_val_at(field[0] - 1, field[1] + 1)):
                sides += 1

            if (self.get_val_at(*field) == self.get_val_at(field[0] - 1, field[1]) and
                    self.get_val_at(*field) == self.get_val_at(field[0], field[1] - 1) and
                    self.get_val_at(*field) != self.get_val_at(field[0] - 1, field[1] - 1)):
                sides += 1

            if len(v_neighbours) == 1 and len(h_neighbours) == 1:
                sides += 1

            if len(v_neighbours) == 0 and len(h_neighbours) == 0:
                sides += 4

        return sides

    def get_fence_cost(self):
        cost = 0
        for label in self.garden_dict:
            while self.garden_dict[label]:
                region = self.extract_region(label)
                self.garden_dict[label] = self.garden_dict[label].difference(region)
                cost += len(region) * self.get_perimeter(region)
        return cost

    def get_discount_fence_cost(self):
        cost = 0
        for label in self.garden_dict:
            while self.garden_dict[label]:
                region = self.extract_region(label)
                self.garden_dict[label] = self.garden_dict[label].difference(region)
                cost += len(region) * self.get_sides(region)
        return cost


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        rows = file.readlines()
        garden = Garden(rows)

        start = round(time() * 1000)

        answer_1 = garden.get_fence_cost()

        end_1 = round(time() * 1000)
        garden = Garden(rows)
        answer_2 = garden.get_discount_fence_cost()

        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 11, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 11, 2))
